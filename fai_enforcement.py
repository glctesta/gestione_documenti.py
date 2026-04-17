# -*- coding: utf-8 -*-
"""
FAI Compliance Enforcement & Escalation System.

Monitora la compilazione obbligatoria dei FAI ad ogni inizio turno
e per ogni nuovo ordine in produzione. Implementa escalation a 3 livelli
con generazione automatica di REFERAT (nota disciplinare) al livello finale.

Turni monitorati: 07:30, 15:30, 23:30 (notturno solo se produzione attiva)
Escalation: L1 +60min (Capo Reparto), L2 +90min (Capo Produzione),
            L3 +120min (Qualità + Amministratore + REFERAT)
"""
import logging
import os
import time
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger("TraceabilityRS")


def _execute_with_deadlock_retry(conn, query, params=None, max_retries=3):
    """Esegue una query con retry automatico in caso di deadlock (errore 40001).

    SQL Server sceglie un processo come 'deadlock victim' — il retry è la
    soluzione standard raccomandata da Microsoft.
    """
    for attempt in range(1, max_retries + 1):
        try:
            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            error_code = getattr(e, 'args', [None])[0] if hasattr(e, 'args') else None
            if error_code == '40001' and attempt < max_retries:
                # Dopo un deadlock SQL Server ha gia' rollbackato server-side:
                # allineiamo lo stato client per permettere il retry pulito.
                try:
                    conn.rollback()
                except Exception:
                    pass
                wait = attempt * 2  # 2s, 4s, 6s
                logger.warning(
                    f"Deadlock detected (attempt {attempt}/{max_retries}), "
                    f"retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise  # Non è un deadlock oppure tentativi esauriti

# ================================================================
# CONFIGURAZIONE
# ================================================================

SHIFT_TIMES = {
    'morning': {
        'start_hour': 7, 'start_min': 30,
        'presence_from': '06:40',
        'label': '07:30',
    },
    'afternoon': {
        'start_hour': 15, 'start_min': 30,
        'presence_from': '14:40',
        'label': '15:30',
    },
    'night': {
        'start_hour': 23, 'start_min': 30,
        'presence_from': '22:40',
        'label': '23:30',
    },
}

# Minuti dopo inizio turno per ogni livello di escalation
ESCALATION_LEVELS = {
    1: {'delay_min': 60,  'label': 'Capo Reparto'},
    2: {'delay_min': 90,  'label': 'Capo Produzione'},
    3: {'delay_min': 120, 'label': 'Qualità + Amministratore'},
}

ARTICOLO_LEGALE_ID = 33  # Non osservanza del regolamento interno
REGISTRO_TYPE_ID = 60    # Referat
EMPLOYER_ID = 2          # Vandewiele Romania


# ================================================================
# 1. IDENTIFICAZIONE RESPONSABILI (riuso da fai_autocheck)
# ================================================================

SQL_RECIPIENTS = """
    SELECT h.EmployeeHireHistoryId,
           e.EmployeeSurname + ' ' + e.EmployeeName AS Employee,
           a.WorkEmail,
           f.FunctionCode,
           cs.SubCdcDescription,
           ee.IDEmployee
    FROM Employee.dbo.EmployeeHireHistory h
    LEFT JOIN Employee.dbo.Employees e
        ON e.EmployeeId = h.EmployeeId
       AND h.EmployeerID = 2
       AND h.EndWorkDate IS NULL
    INNER JOIN Employee.dbo.EmployeeCdcStories ec
        ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
    INNER JOIN Employee.dbo.Functions f
        ON ec.FunctionId = f.FunctionId
    INNER JOIN Employee.dbo.CdcSub cs
        ON ec.SubCdcId = cs.SubCdcId
    INNER JOIN Employee.dbo.EmployeeAddress a
        ON e.EmployeeId = a.EmployeeId
       AND a.DateOut IS NULL
    INNER JOIN Timeclocking.dbo.Employee ee
        ON ee.UniqueID COLLATE database_default = e.EmployeeNID
       AND ee.DataStop IS NULL
    WHERE cs.SubCdcDescription = 'pthm'
      AND f.FunctionCode BETWEEN 21 AND 80
    ORDER BY f.FunctionCode
"""


def get_responsible_employees(conn) -> List[Dict]:
    """Restituisce la lista dei responsabili FAI (capi turno/capilinea)."""
    employees = []
    try:
        rows = _execute_with_deadlock_retry(conn, SQL_RECIPIENTS)
        for r in rows:
            email = (r.WorkEmail or '').strip()
            if not email or '@' not in email:
                continue
            employees.append({
                'EmployeeHireHistoryId': r.EmployeeHireHistoryId,
                'Employee': r.Employee,
                'WorkEmail': email,
                'FunctionCode': r.FunctionCode or 0,
                'SubCdc': r.SubCdcDescription or '',
                'IDEmployee': r.IDEmployee,
            })
        logger.info(f"FAI Enforcement: {len(employees)} responsabili trovati")
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_responsible_employees: {e}", exc_info=True)
    return employees


# ================================================================
# 2. VERIFICA PRESENZA IN TURNO (riuso da fai_autocheck)
# ================================================================

def check_presence(conn, id_employee: int, shift_key: str) -> bool:
    """Verifica presenza del dipendente nel turno corrente."""
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    shift = SHIFT_TIMES.get(shift_key, {})
    from_dt = f"{today_str} {shift.get('presence_from', '06:40')}:00"
    to_dt = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with conn.cursor() as cur:
            cur.execute(
                "EXEC [Timeclocking].[dbo].[GetEmployeesTimeclockReal] ?, ?, ?",
                (from_dt, to_dt, id_employee))
            result = cur.fetchone()
        return result is not None
    except Exception as e:
        logger.warning(f"FAI Enforcement: errore verifica presenza ID {id_employee}: {e}")
        return False


# ================================================================
# 3. VERIFICA PRODUZIONE NOTTURNA
# ================================================================

SQL_NIGHT_PRODUCTION = """
    SELECT DISTINCT o.IDOrder 
    FROM Traceability_RS.dbo.Scannings S 
    INNER JOIN Traceability_RS.dbo.Boards B ON s.IDBoard = b.IDBoard 
    INNER JOIN Traceability_RS.dbo.Orders o ON o.IDOrder = b.IDOrder
    WHERE s.ScanTimeStart > CAST(CAST(CAST(GETDATE() AS date) AS nvarchar(10)) 
          + ' 23:35:00' AS smalldatetime)
"""


def check_night_shift_active(conn) -> bool:
    """Verifica se c'è produzione attiva per il turno notturno."""
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_NIGHT_PRODUCTION)
            row = cur.fetchone()
        active = row is not None
        logger.info(f"FAI Enforcement: turno notturno attivo = {active}")
        return active
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check night shift: {e}", exc_info=True)
        return False


# ================================================================
# 4. VERIFICA FAI COMPILATO
# ================================================================

def check_shift_fai_completed(conn, operator_name: str, shift_start_dt: datetime) -> bool:
    """Verifica se l'operatore ha compilato almeno un FAI Autocheck dopo l'inizio turno.
    
    Filtra solo FaiLogs collegati a template con Autocheck=1 tramite la catena:
    FaiLogs → FaiStepDetails → FaiSteps → FaiTemplates.
    """
    query = """
        SELECT TOP 1 l.FaiLogId 
        FROM [Traceability_RS].[fai].[FaiLogs] l
        INNER JOIN [Traceability_RS].[fai].[FaiStepDetails] d
            ON l.FaiStepDetailId = d.FaiStepDetailId
        INNER JOIN [Traceability_RS].[fai].[FaiSteps] s
            ON d.FatStepId = s.FatStepId
        INNER JOIN [Traceability_RS].[fai].[FaiTemplates] t
            ON s.FaiTemplateId = t.FaiTemplateId
        WHERE l.Operator = ? 
          AND l.DateIn >= ?
          AND l.DateOut IS NULL
          AND t.Autocheck = 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (operator_name, shift_start_dt))
            row = cur.fetchone()
        return row is not None
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check FAI completato: {e}", exc_info=True)
        return False


def check_order_fai_completed(conn, order_id: int) -> bool:
    """Verifica se esiste un FAI Autocheck compilato per un dato ordine.
    
    Filtra solo FaiLogs collegati a template con Autocheck=1 tramite la catena:
    FaiLogs → FaiStepDetails → FaiSteps → FaiTemplates.
    """
    query = """
        SELECT TOP 1 l.FaiLogId 
        FROM [Traceability_RS].[fai].[FaiLogs] l
        INNER JOIN [Traceability_RS].[fai].[FaiStepDetails] d
            ON l.FaiStepDetailId = d.FaiStepDetailId
        INNER JOIN [Traceability_RS].[fai].[FaiSteps] s
            ON d.FatStepId = s.FatStepId
        INNER JOIN [Traceability_RS].[fai].[FaiTemplates] t
            ON s.FaiTemplateId = t.FaiTemplateId
        WHERE l.OrderId = ?
          AND l.DateOut IS NULL
          AND t.Autocheck = 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (order_id,))
            row = cur.fetchone()
        return row is not None
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check FAI ordine {order_id}: {e}", exc_info=True)
        return False


def check_order_fai_completed_by_number(conn, order_number: str, id_phase: int) -> bool:
    """Verifica se esiste un FAI Autocheck compilato per ordine (per OrderNumber + IdPhase).
    
    Usato dal planning-based enforcement dove abbiamo OrderNumber dal file Excel.
    """
    query = """
        SELECT TOP 1 l.FaiLogId 
        FROM [Traceability_RS].[fai].[FaiLogs] l
        INNER JOIN [Traceability_RS].[fai].[FaiStepDetails] d
            ON l.FaiStepDetailId = d.FaiStepDetailId
        INNER JOIN [Traceability_RS].[fai].[FaiSteps] s
            ON d.FatStepId = s.FatStepId
        INNER JOIN [Traceability_RS].[fai].[FaiTemplates] t
            ON s.FaiTemplateId = t.FaiTemplateId
        INNER JOIN [Traceability_RS].[dbo].[Orders] o
            ON l.OrderId = o.IDOrder
        WHERE o.OrderNumber = ?
          AND t.IdPhase = ?
          AND l.DateOut IS NULL
          AND t.Autocheck = 1
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (order_number, id_phase))
            row = cur.fetchone()
        return row is not None
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check FAI ordine {order_number}/fase {id_phase}: {e}",
                     exc_info=True)
        return False


# ================================================================
# 5. RILEVAMENTO NUOVI ORDINI
# ================================================================

SQL_NEW_ORDERS = """
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    SELECT DISTINCT o.IDOrder, o.OrderNumber, op.IDPhase,
           ft.FaiTemplateId, ft.FaiTitle
    FROM Traceability_RS.dbo.Scannings S
    INNER JOIN Traceability_RS.dbo.Boards B ON s.IDBoard = b.IDBoard
    INNER JOIN Traceability_RS.dbo.Orders o ON o.IDOrder = b.IDOrder
    INNER JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrder = o.IDOrder
    INNER JOIN Traceability_RS.fai.FaiTemplates ft ON ft.IdPhase = op.IDPhase
    WHERE s.ScanTimeStart >= DATEADD(HOUR, -1, GETDATE())
      AND ft.Autocheck = 1
      AND b.IDOrder NOT IN (
          SELECT DISTINCT b2.IDOrder
          FROM Traceability_RS.dbo.Scannings s2
          INNER JOIN Traceability_RS.dbo.Boards b2 ON s2.IDBoard = b2.IDBoard
          WHERE s2.ScanTimeStart >= DATEADD(HOUR, -2, GETDATE())
            AND s2.ScanTimeStart < DATEADD(HOUR, -1, GETDATE())
      );
    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
"""


def detect_new_orders(conn) -> List[Dict]:
    """Rileva nuovi ordini con template FAI nell'ultima ora."""
    new_orders = []
    try:
        rows = _execute_with_deadlock_retry(conn, SQL_NEW_ORDERS)
        for r in rows:
            new_orders.append({
                'IDOrder': r.IDOrder,
                'OrderNumber': r.OrderNumber,
                'IDPhase': r.IDPhase,
                'FaiTemplateId': r.FaiTemplateId,
                'FaiTitle': r.FaiTitle,
            })
        if new_orders:
            logger.info(f"FAI Enforcement: {len(new_orders)} nuovi ordini rilevati con template FAI")
    except Exception as e:
        logger.error(f"FAI Enforcement: errore detect_new_orders: {e}", exc_info=True)
    return new_orders


# ================================================================
# 6. DESTINATARI ESCALATION PER LIVELLO
# ================================================================

def get_escalation_recipients(conn, level: int, employees: List[Dict],
                               employee_hhid: int = None) -> List[str]:
    """
    Restituisce le email dei destinatari per il livello di escalation.
    L1: FunctionCode 60-69 (Capo Reparto / PTHM)
    L2: FunctionCode 70-79 (Capo Produzione / PTHM)
    L3: Qualità (CdcId=2) + Dipendente + Suo capo + Amministratore
    
    Args:
        employee_hhid: EmployeeHireHistoryId del dipendente oggetto del referat (solo L3)
    """
    recipients = []
    
    if level == 1:
        recipients = [e['WorkEmail'] for e in employees if 60 <= e['FunctionCode'] <= 69]
    elif level == 2:
        recipients = [e['WorkEmail'] for e in employees if 70 <= e['FunctionCode'] <= 79]
    elif level == 3:
        # 1. Reparto Qualità (CdcId=2, responsabili con FunctionCode >= 40)
        quality_emails = get_quality_department_emails(conn)
        recipients.extend(quality_emails)
        
        # 2. Dipendente che ha ricevuto il referat + suo capo diretto
        if employee_hhid:
            emp_email = get_employee_email_by_hhid(conn, employee_hhid)
            if emp_email:
                recipients.append(emp_email)
            
            supervisor_email = get_employee_supervisor_email(conn, employee_hhid)
            if supervisor_email:
                recipients.append(supervisor_email)
        
        # 3. Amministratore
        try:
            admin = get_administrator_info(conn)
            if admin and admin.get('email'):
                recipients.append(admin['email'])
        except Exception:
            pass
    
    result = list(dict.fromkeys(recipients))  # Deduplica preservando ordine
    logger.info(f"FAI Enforcement: destinatari L{level}: {result}")
    return result


def get_employee_email_by_hhid(conn, employee_hhid: int) -> Optional[str]:
    """Recupera la WorkEmail di un dipendente tramite EmployeeHireHistoryId."""
    query = """
        SELECT a.WorkEmail
        FROM Employee.dbo.EmployeeHireHistory h
        INNER JOIN Employee.dbo.Employees e 
            ON e.EmployeeId = h.EmployeeId
        INNER JOIN Employee.dbo.EmployeeAddress a 
            ON a.EmployeeId = e.EmployeeId AND a.DateOut IS NULL
        WHERE h.EmployeeHireHistoryId = ?
            AND h.EmployeerID = 2
            AND h.EndWorkDate IS NULL
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (employee_hhid,))
            row = cur.fetchone()
        if row and row.WorkEmail:
            email = row.WorkEmail.strip()
            if '@' in email:
                return email
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_employee_email_by_hhid({employee_hhid}): {e}")
    return None


def get_employee_supervisor_email(conn, employee_hhid: int) -> Optional[str]:
    """Trova il capo diretto del dipendente (stesso SubCdc, FunctionCode più alto)."""
    query = """
        SELECT TOP 1 a_sup.WorkEmail
        FROM Employee.dbo.EmployeeCdcStories ec_emp
        -- SubCdc del dipendente
        INNER JOIN Employee.dbo.EmployeeCdcStories ec_sup
            ON ec_sup.SubCdcId = ec_emp.SubCdcId
            AND ec_sup.DateOut IS NULL
            AND ec_sup.EmployeeHireHistoryId != ec_emp.EmployeeHireHistoryId
        -- FunctionCode del supervisore > FunctionCode del dipendente
        INNER JOIN Employee.dbo.Functions f_emp ON ec_emp.FunctionId = f_emp.FunctionId
        INNER JOIN Employee.dbo.Functions f_sup ON ec_sup.FunctionId = f_sup.FunctionId
            AND f_sup.FunctionCode > f_emp.FunctionCode
        -- Dati supervisore
        INNER JOIN Employee.dbo.EmployeeHireHistory h_sup
            ON h_sup.EmployeeHireHistoryId = ec_sup.EmployeeHireHistoryId
            AND h_sup.EmployeerID = 2
            AND h_sup.EndWorkDate IS NULL
        INNER JOIN Employee.dbo.Employees e_sup ON e_sup.EmployeeId = h_sup.EmployeeId
        INNER JOIN Employee.dbo.EmployeeAddress a_sup
            ON a_sup.EmployeeId = e_sup.EmployeeId AND a_sup.DateOut IS NULL
        WHERE ec_emp.EmployeeHireHistoryId = ?
            AND ec_emp.DateOut IS NULL
        ORDER BY f_sup.FunctionCode ASC
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (employee_hhid,))
            row = cur.fetchone()
        if row and row.WorkEmail:
            email = row.WorkEmail.strip()
            if '@' in email:
                logger.info(f"FAI Enforcement: supervisore per HHID {employee_hhid}: {email}")
                return email
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_employee_supervisor_email({employee_hhid}): {e}")
    return None


def get_quality_department_emails(conn) -> List[str]:
    """Recupera le email dei responsabili del reparto Qualità (CdcId=2, FunctionCode >= 40)."""
    query = """
        SELECT DISTINCT a.WorkEmail
        FROM Employee.dbo.EmployeeHireHistory h
        INNER JOIN Employee.dbo.Employees e 
            ON e.EmployeeId = h.EmployeeId
            AND h.EmployeerID = 2
            AND h.EndWorkDate IS NULL
        INNER JOIN Employee.dbo.EmployeeCdcStories ec
            ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
            AND ec.DateOut IS NULL
        INNER JOIN Employee.dbo.Functions f
            ON ec.FunctionId = f.FunctionId
        INNER JOIN Employee.dbo.CdcSub cs
            ON ec.SubCdcId = cs.SubCdcId
        INNER JOIN Employee.dbo.CostCenters cc
            ON cc.CdcId = cs.CdcId
        INNER JOIN Employee.dbo.EmployeeAddress a
            ON a.EmployeeId = e.EmployeeId AND a.DateOut IS NULL
        WHERE cc.CdcId = 2  -- QUALITY
            AND f.FunctionCode >= 40
            AND a.WorkEmail IS NOT NULL
    """
    emails = []
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            for row in cur.fetchall():
                email = (row.WorkEmail or '').strip()
                if email and '@' in email:
                    emails.append(email)
        logger.info(f"FAI Enforcement: {len(emails)} email reparto Qualità trovate")
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_quality_department_emails: {e}")
    return emails


def get_administrator_info(conn) -> Optional[Dict]:
    """Recupera le informazioni dell'amministratore attivo."""
    query = """
        SELECT TOP 1 a.AdminId, e.EmployeeName, e.EmployeeSurname,
               e.EmployeeId, a.Firma,
               ea.WorkEmail
        FROM Employee.dbo.Administrators a
        INNER JOIN Employee.dbo.Employees e ON a.EmployeeId = e.EmployeeId
        INNER JOIN Employee.dbo.EmployeeHireHistory h 
            ON e.EmployeeId = h.EmployeeId AND h.EmployeerId = 2 AND h.EndWorkDate IS NULL
        LEFT JOIN Employee.dbo.EmployeeAddress ea
            ON e.EmployeeId = ea.EmployeeId AND ea.DateOut IS NULL
        WHERE a.DateOut IS NULL
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
        if row:
            return {
                'AdminId': row.AdminId,
                'name': f"{row.EmployeeSurname} {row.EmployeeName}",
                'full_name': f"{row.EmployeeName} {row.EmployeeSurname}",
                'EmployeeId': row.EmployeeId,
                'firma': row.Firma,
                'email': (row.WorkEmail or '').strip(),
            }
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_administrator_info: {e}", exc_info=True)
    return None


# ================================================================
# 7. TRACKING LOG
# ================================================================

def log_enforcement_event(conn, event_type: str, employee_hhid: int = None,
                          employee_name: str = None, order_id: int = None,
                          order_number: str = None, shift_time: str = None,
                          escalation_level: int = 0, notes: str = None) -> Optional[int]:
    """Registra un evento di enforcement nel DB. Ritorna l'ID generato."""
    query = """
        INSERT INTO [Traceability_RS].[fai].[FaiEnforcementLog]
            (EventType, EmployeeHireHistoryId, EmployeeName, OrderId, OrderNumber,
             ShiftTime, EscalationLevel, NotificationSent, NotificationTime, Notes)
        OUTPUT INSERTED.EnforcementLogId
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), ?)
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (event_type, employee_hhid, employee_name,
                                order_id, order_number, shift_time,
                                escalation_level, notes))
            row = cur.fetchone()
            conn.commit()
        log_id = int(row[0]) if row else None
        logger.info(f"FAI Enforcement: evento registrato ID={log_id}, "
                     f"tipo={event_type}, livello={escalation_level}")
        return log_id
    except Exception as e:
        logger.error(f"FAI Enforcement: errore log_enforcement_event: {e}", exc_info=True)
        try:
            conn.rollback()
        except Exception:
            pass
        return None


def update_enforcement_event(conn, log_id: int, **kwargs):
    """Aggiorna un evento esistente (es. escalation_level, fai_completed, referat)."""
    set_parts = []
    params = []
    for key, value in kwargs.items():
        set_parts.append(f"{key} = ?")
        params.append(value)
    
    if not set_parts:
        return
    
    params.append(log_id)
    query = f"""
        UPDATE [Traceability_RS].[fai].[FaiEnforcementLog]
        SET {', '.join(set_parts)}
        WHERE EnforcementLogId = ?
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            conn.commit()
    except Exception as e:
        logger.error(f"FAI Enforcement: errore update evento {log_id}: {e}", exc_info=True)
        try:
            conn.rollback()
        except Exception:
            pass


def check_already_escalated(conn, event_type: str, shift_time: str = None,
                            employee_hhid: int = None, order_id: int = None,
                            level: int = 0) -> bool:
    """Verifica se un evento di escalation è già stato registrato oggi."""
    query = """
        SELECT TOP 1 EnforcementLogId
        FROM [Traceability_RS].[fai].[FaiEnforcementLog]
        WHERE EventType = ?
          AND CheckDate = CAST(GETDATE() AS DATE)
          AND EscalationLevel = ?
          AND DateOut IS NULL
    """
    params = [event_type, level]
    
    if shift_time:
        query += " AND ShiftTime = ?"
        params.append(shift_time)
    if employee_hhid:
        query += " AND EmployeeHireHistoryId = ?"
        params.append(employee_hhid)
    if order_id:
        query += " AND OrderId = ?"
        params.append(order_id)
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            return cur.fetchone() is not None
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check_already_escalated: {e}", exc_info=True)
        return False


def get_pending_escalations(conn, event_type: str, current_level: int,
                            shift_time: str = None) -> List[Dict]:
    """Recupera eventi aperti per un livello che necessitano escalation.

    Safety filter: per eventi legati a un ordine (OrderId non NULL) include
    SOLO eventi il cui ordine ha almeno un template FAI con Autocheck=1.
    Questo evita che eventi storici creati prima dell'introduzione del filtro
    Autocheck (pre v2.4.0.2.3) continuino a escalare fino a L3.
    Gli eventi SHIFT_CHECK (senza OrderId) passano inalterati: la loro
    validità Autocheck=1 è gia' verificata in fase di generazione.
    """
    query = """
        SELECT l.EnforcementLogId, l.EmployeeHireHistoryId, l.EmployeeName,
               l.OrderId, l.OrderNumber, l.ShiftTime, l.EscalationLevel
        FROM [Traceability_RS].[fai].[FaiEnforcementLog] l
        WHERE l.EventType = ?
          AND l.CheckDate = CAST(GETDATE() AS DATE)
          AND l.EscalationLevel = ?
          AND l.FaiCompleted = 0
          AND l.DateOut IS NULL
          AND (
              l.OrderId IS NULL
              OR EXISTS (
                  SELECT 1
                  FROM [Traceability_RS].[dbo].[OrderPhases] op
                  INNER JOIN [Traceability_RS].[fai].[FaiTemplates] ft
                      ON ft.IdPhase = op.IDPhase
                  WHERE op.IDOrder = l.OrderId
                    AND ft.Autocheck = 1
              )
          )
    """
    params = [event_type, current_level]

    if shift_time:
        query += " AND l.ShiftTime = ?"
        params.append(shift_time)
    
    results = []
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
        for r in rows:
            results.append({
                'EnforcementLogId': r.EnforcementLogId,
                'EmployeeHireHistoryId': r.EmployeeHireHistoryId,
                'EmployeeName': r.EmployeeName,
                'OrderId': r.OrderId,
                'OrderNumber': r.OrderNumber,
                'ShiftTime': r.ShiftTime,
                'EscalationLevel': r.EscalationLevel,
            })
    except Exception as e:
        logger.error(f"FAI Enforcement: errore get_pending_escalations: {e}", exc_info=True)
    return results


# ================================================================
# 8. EMAIL ESCALATION
# ================================================================

def send_escalation_email(level: int, employee_name: str, shift_label: str,
                          recipients: List[str], order_info: str = None,
                          logo_path: str = "logo.png",
                          referat_pdf_path: str = None):
    """Invia email di escalation con formattazione HTML."""
    from utils import send_email
    
    level_info = ESCALATION_LEVELS.get(level, {})
    level_label = level_info.get('label', f'Livello {level}')
    
    # Colori per livello
    colors = {1: '#FFA500', 2: '#FF6600', 3: '#CC0000'}
    color = colors.get(level, '#CC0000')
    
    # Icone per livello
    icons = {1: '🟡', 2: '🟠', 3: '🔴'}
    icon = icons.get(level, '🔴')
    
    subject = (f"{icon} FAI Enforcement - Escalation Livello {level} - "
               f"{employee_name} - Turno {shift_label}")
    
    if order_info:
        subject += f" - Ordine {order_info}"
    
    referat_note = ""
    if level == 3:
        referat_note = """
        <div style="background-color: #FFCCCC; padding: 15px; margin: 15px 0; 
                    border-left: 5px solid #CC0000; border-radius: 5px;">
            <h3 style="color: #CC0000; margin: 0 0 10px 0;">
                ⚠️ REFERAT DISCIPLINAR GENERAT AUTOMAT</h3>
            <p style="margin: 0;">Un referat disciplinar è stato emesso automaticamente per 
            <b>non osservanza del regolamento interno</b> relativo alla compilazione 
            obbligatoria dei FAI ad inizio turno.</p>
            <p style="margin: 5px 0 0 0;">Il documento PDF è allegato a questa email.</p>
        </div>
        """
    
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; font-size: 13px; }}
            .header {{ background-color: {color}; color: white; padding: 20px; 
                       border-radius: 8px 8px 0 0; }}
            .content {{ padding: 20px; background-color: #f9f9f9; 
                        border: 1px solid #ddd; border-top: none; 
                        border-radius: 0 0 8px 8px; }}
            .info-table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            .info-table td {{ padding: 10px; border: 1px solid #ddd; }}
            .info-table td:first-child {{ font-weight: bold; background: #f0f0f0; width: 35%; }}
            .escalation-badge {{ display: inline-block; padding: 5px 15px; 
                                 background: {color}; color: white; border-radius: 20px;
                                 font-weight: bold; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>{icon} FAI Compliance Enforcement</h2>
            <p>Escalation Livello {level} — {level_label}</p>
        </div>
        <div class="content">
            <p>Il seguente responsabile <b>non ha compilato</b> il FAI obbligatorio 
            entro i tempi previsti:</p>
            
            <table class="info-table">
                <tr><td>Responsabile:</td><td><b>{employee_name}</b></td></tr>
                <tr><td>Turno:</td><td>{shift_label}</td></tr>
                <tr><td>Livello Escalation:</td>
                    <td><span class="escalation-badge">LIVELLO {level} — {level_label}</span></td></tr>
                <tr><td>Data/Ora Rilevamento:</td>
                    <td>{datetime.now().strftime('%d/%m/%Y %H:%M')}</td></tr>
                {"<tr><td>Ordine:</td><td><b>" + (order_info or '') + "</b></td></tr>" if order_info else ""}
            </table>
            
            {referat_note}
            
            <p style="margin-top: 20px;">
                <b>Azione richiesta:</b> Assicurarsi che il FAI venga compilato immediatamente.
            </p>
            
            <p style="color: #888; font-size: 11px; margin-top: 30px;">
                Questa è una notifica automatica del sistema FAI Compliance Enforcement.<br>
                TraceabilityRS — Vandewiele Romania
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        attachments = []
        if referat_pdf_path and os.path.exists(referat_pdf_path):
            attachments.append(referat_pdf_path)
        
        send_email(
            recipients=recipients,
            subject=subject,
            body=html_body,
            is_html=True,
            attachments=attachments if attachments else None
        )
        logger.info(f"FAI Enforcement: email L{level} inviata a {recipients}")
        return True
    except Exception as e:
        logger.error(f"FAI Enforcement: errore invio email L{level}: {e}", exc_info=True)
        return False


# ================================================================
# 9. GENERAZIONE AUTOMATICA REFERAT
# ================================================================

def create_automatic_referat(conn, employee_hhid: int, employee_name: str,
                             shift_label: str, admin_info: Dict,
                             order_info: str = None) -> Optional[str]:
    """
    Genera un REFERAT automatico per mancata compilazione FAI.
    Ritorna il percorso del PDF generato, o None.
    """
    try:
        # Validazione: EmployeeHireHistoryId obbligatorio per il referat
        if not employee_hhid:
            logger.warning(
                f"FAI Enforcement: impossibile generare REFERAT per "
                f"'{employee_name}' — EmployeeHireHistoryId mancante. "
                f"Possibile evento NEW_ORDER senza dipendente specifico.")
            return None
        
        admin_name = admin_info.get('name', 'Amministratore')
        now = datetime.now()
        
        # 1. Genera numero documento via SP
        with conn.cursor() as cur:
            cur.execute("""
                EXEC Employee.dbo.Registro
                    @RegistryTypeId = ?,
                    @anno = ?,
                    @DataDocumento = ?,
                    @iussedBy = ?,
                    @EmployeerId = ?,
                    @Accessid = NULL,
                    @DocumentTypeId = NULL
            """, REGISTRO_TYPE_ID,
                 now.year,
                 now.strftime('%Y-%m-%d'),
                 admin_name,
                 EMPLOYER_ID)
        
        # 2. Recupera RegistroId e DocName
        with conn.cursor() as cur:
            cur.execute("""
                SELECT TOP 1 RegistroId, DocName
                FROM Employee.dbo.Registry
                WHERE RegistryTypeId = ?
                ORDER BY RegistroId DESC
            """, REGISTRO_TYPE_ID)
            reg_row = cur.fetchone()
        
        if not reg_row:
            raise Exception("SP Registro non ha generato il numero documento")
        
        registro_id = reg_row.RegistroId
        doc_name = reg_row.DocName
        
        # 3. Motivo del referat
        order_text = f" per l'ordine {order_info}" if order_info else ""
        reason_text = (
            f"{employee_name} nu a completat verificarea FAI obligatorie la "
            f"începutul turei de la ora {shift_label}{order_text}. "
            f"Acest lucru constituie o abatere disciplinară conform "
            f"regulamentului intern al companiei."
        )
        
        # 4. Insert in EmployeeDisciplinaryHistory
        with conn.cursor() as cur:
            cur.execute("""
                IF NOT EXISTS (
                    SELECT [RegistroId] FROM Employee.[dbo].[EmployeeDisciplinaryHistory]
                    WHERE [RegistroId] = ?
                )
                INSERT INTO Employee.[dbo].[EmployeeDisciplinaryHistory]
                    ([EmployeeHireHistoryId], [RegistroId], [DocSavedOn],
                     [ExplicationNote], [ArticoloLegaleId], [SefID],
                     [DataAvvenimento], [OraAvvenimento])
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, registro_id,
                 employee_hhid,
                 registro_id,
                 now.strftime('%Y-%m-%d'),
                 reason_text.replace("'", "''"),
                 ARTICOLO_LEGALE_ID,
                 admin_info.get('EmployeeId'),
                 now.strftime('%Y-%m-%d'),
                 shift_label)
        
        conn.commit()
        logger.info(f"FAI Enforcement: REFERAT registrato - RegistroId={registro_id}, "
                     f"DocName={doc_name}, Employee={employee_name}")
        
        # 5. Genera PDF
        pdf_path = _generate_referat_pdf(
            doc_name=doc_name,
            date_ref=now,
            employee_name=employee_name,
            admin_name=admin_name,
            admin_department="Administrație",
            reason_text=reason_text,
            shift_label=shift_label,
            admin_firma=admin_info.get('firma')
        )
        
        return pdf_path
        
    except Exception as e:
        logger.error(f"FAI Enforcement: errore create_automatic_referat: {e}", exc_info=True)
        try:
            conn.rollback()
        except Exception:
            pass
        return None


def _generate_referat_pdf(doc_name: str, date_ref: datetime, employee_name: str,
                          admin_name: str, admin_department: str,
                          reason_text: str, shift_label: str,
                          admin_firma=None) -> Optional[str]:
    """Genera il PDF del REFERAT automatico usando ReportLab."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import Paragraph, Image as RLImage
        import io
        
        font_dir = r'C:\Windows\Fonts'
        if 'Arial' not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont('Arial', os.path.join(font_dir, 'arial.ttf')))
            pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(font_dir, 'arialbd.ttf')))
            pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(font_dir, 'ariali.ttf')))
        
        output_dir = r"C:\Temp"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        safe_doc_name = (doc_name or "referat").replace("/", "-").replace("\\", "-")
        filename = f"Referat_FAI_{safe_doc_name}.pdf"
        file_path = os.path.join(output_dir, filename)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'ab') as _t:
                    pass
            except PermissionError:
                ts = datetime.now().strftime('%H%M%S')
                filename = f"Referat_FAI_{safe_doc_name}_{ts}.pdf"
                file_path = os.path.join(output_dir, filename)
        
        page_w, page_h = A4
        c = canvas.Canvas(file_path, pagesize=A4)
        
        # Logo
        logo_path = "Logo.png"
        if os.path.exists(logo_path):
            try:
                c.drawImage(logo_path, 2 * cm, page_h - 3 * cm,
                            width=3 * cm, height=1.5 * cm,
                            preserveAspectRatio=True, mask='auto')
            except Exception:
                pass
        
        # Titolo
        y = page_h - 4 * cm
        c.setFont("Arial-Bold", 18)
        c.drawCentredString(page_w / 2, y, "REFERAT")
        
        y -= 0.6 * cm
        c.setFont("Arial-Italic", 10)
        c.drawCentredString(page_w / 2, y, "(Generat automat — FAI Compliance Enforcement)")
        
        # Numero documento
        y -= 1.2 * cm
        c.setFont("Arial", 11)
        c.drawString(2 * cm, y, f"Nr. {doc_name} / {date_ref.strftime('%d-%m-%Y')}")
        
        # Destinatario
        y -= 1.5 * cm
        c.drawString(2 * cm, y, f"În atenția Domnului ADMINISTRATOR {admin_name},")
        
        # Corpo principale
        y -= 1.5 * cm
        body_style = ParagraphStyle(
            'Body', fontName='Arial', fontSize=11,
            leading=16, firstLineIndent=1 * cm
        )
        
        body_text = (
            f"Subsemnatul <b>{admin_name}</b>, prin intermediul sistemului automat "
            f"TraceabilityRS, în virtutea regulamentului "
            f"intern privind verificările FAI obligatorii, "
            f"dorește să Vă aducă la cunoștință următoarele:"
        )
        body_para = Paragraph(body_text, body_style)
        w_avail = page_w - 4 * cm
        bw, bh = body_para.wrap(w_avail, 900)
        body_para.drawOn(c, 2 * cm, y - bh)
        y -= bh + 0.8 * cm
        
        # Descrizione evento
        event_text = (
            f"În data de {date_ref.strftime('%d-%m-%Y')}, la începutul turei de ora "
            f"{shift_label}, salariatul <b>{employee_name}</b> nu a efectuat "
            f"verificarea FAI (First Article Inspection) obligatorie conform "
            f"procedurilor interne. După 3 nivele de escaladare (Șef secție, "
            f"Șef producție, Calitate), verificarea nu a fost finalizată în "
            f"termenul de 120 de minute prevăzut de regulament."
        )
        event_para = Paragraph(event_text, body_style)
        ew, eh = event_para.wrap(w_avail, 900)
        event_para.drawOn(c, 2 * cm, y - eh)
        y -= eh + 0.8 * cm
        
        # Motivo
        reason_style = ParagraphStyle(
            'Reason', fontName='Arial', fontSize=11, leading=15
        )
        reason_para = Paragraph(reason_text.replace('\n', '<br/>'), reason_style)
        rw, rh = reason_para.wrap(w_avail, 400)
        if y - rh < 5 * cm:
            rh = y - 5 * cm
        reason_para.drawOn(c, 2 * cm, y - rh)
        y -= rh + 1.5 * cm
        
        # Footer
        y = max(y, 4 * cm)
        c.setFont("Arial", 11)
        c.drawString(2 * cm, y, f"Data GHIRODA, {date_ref.strftime('%d-%m-%Y')}")
        
        y -= 1 * cm
        c.drawString(2 * cm, y, "Semnătura,")
        
        # Firma immagine dell'amministratore (se disponibile)
        if admin_firma:
            try:
                y -= 0.3 * cm
                firma_stream = io.BytesIO(admin_firma)
                c.drawImage(firma_stream, 2 * cm, y - 2 * cm,
                            width=4 * cm, height=2 * cm,
                            preserveAspectRatio=True, mask='auto')
                y -= 2.3 * cm
            except Exception as firma_err:
                logger.warning(f"FAI Enforcement: impossibile inserire firma: {firma_err}")
                y -= 0.8 * cm
        else:
            y -= 0.8 * cm
        
        c.setFont("Arial-Bold", 11)
        c.drawString(2 * cm, y, admin_name.upper())
        
        y -= 0.8 * cm
        c.setFont("Arial", 11)
        c.drawString(2 * cm, y, "______________________")
        
        c.save()
        logger.info(f"FAI Enforcement: PDF Referat generato: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"FAI Enforcement: errore generazione PDF referat: {e}", exc_info=True)
        return None


# ================================================================
# 10. ORCHESTRATORI PRINCIPALI
# ================================================================

def get_current_shift(now: datetime = None) -> Optional[str]:
    """Determina il turno corrente in base all'ora."""
    if now is None:
        now = datetime.now()
    h, m = now.hour, now.minute
    
    if 7 <= h < 15 or (h == 15 and m < 30):
        return 'morning'
    elif 15 <= h < 23 or (h == 23 and m < 30):
        return 'afternoon'
    else:
        return 'night'


def get_shift_start_datetime(shift_key: str, now: datetime = None) -> datetime:
    """Calcola il datetime di inizio del turno corrente."""
    if now is None:
        now = datetime.now()
    shift = SHIFT_TIMES[shift_key]
    
    shift_start = now.replace(
        hour=shift['start_hour'],
        minute=shift['start_min'],
        second=0, microsecond=0
    )
    
    # Per il turno notturno, se siamo dopo mezzanotte, l'inizio era ieri
    if shift_key == 'night' and now.hour < 6:
        shift_start -= timedelta(days=1)
    
    return shift_start


def should_check_shift(now: datetime = None) -> Optional[str]:
    """
    Verifica se è il momento di fare il check del turno (60 min dopo inizio).
    Ritorna il shift_key se è il momento, None altrimenti.
    Finestra di tolleranza: ±2 minuti.
    """
    if now is None:
        now = datetime.now()
    h, m = now.hour, now.minute
    
    # 08:30 ± 2 → check turno mattutino
    if h == 8 and 28 <= m <= 32:
        return 'morning'
    # 16:30 ± 2 → check turno pomeridiano
    elif h == 16 and 28 <= m <= 32:
        return 'afternoon'
    # 00:30 ± 2 → check turno notturno
    elif h == 0 and 28 <= m <= 32:
        return 'night'
    
    return None


def should_escalate(now: datetime = None) -> Optional[Tuple[str, int]]:
    """
    Verifica se è il momento di fare escalation.
    Ritorna (shift_key, target_level) o None.
    """
    if now is None:
        now = datetime.now()
    h, m = now.hour, now.minute
    
    checks = [
        # 09:00 ± 2 → L1→L2 mattutino
        (9, 'morning', 2),
        # 09:30 ± 2 → L2→L3 mattutino
        (9, 'morning', 3),
        # 17:00 ± 2 → L1→L2 pomeridiano
        (17, 'afternoon', 2),
        # 17:30 ± 2 → L2→L3 pomeridiano
        (17, 'afternoon', 3),
        # 01:00 ± 2 → L1→L2 notturno
        (1, 'night', 2),
        # 01:30 ± 2 → L2→L3 notturno
        (1, 'night', 3),
    ]
    
    for check_h, shift, level in checks:
        target_m = 0 if level == 2 else 30
        if h == check_h and target_m - 2 <= m <= target_m + 2:
            return (shift, level)
    
    return None


def run_shift_check(conn, logo_path: str = "logo.png"):
    """
    Orchestratore principale per il check FAI ad inizio turno.
    Chiamato 60 minuti dopo ogni inizio turno.
    """
    now = datetime.now()
    shift_key = should_check_shift(now)
    
    if not shift_key:
        return
    
    shift = SHIFT_TIMES[shift_key]
    shift_label = shift['label']
    
    # Turno notturno: verifica produzione attiva
    if shift_key == 'night' and not check_night_shift_active(conn):
        logger.info("FAI Enforcement: turno notturno senza produzione, skip check")
        return
    
    logger.info(f"FAI Enforcement: ===== SHIFT CHECK turno {shift_label} =====")
    
    # Recupera responsabili
    employees = get_responsible_employees(conn)
    if not employees:
        logger.warning("FAI Enforcement: nessun responsabile trovato")
        return
    
    shift_start_dt = get_shift_start_datetime(shift_key, now)
    violations = []
    
    for emp in employees:
        # Solo capi turno e capilinea (FunctionCode < 60)
        if emp['FunctionCode'] >= 60:
            continue
        
        # Verifica presenza
        if not check_presence(conn, emp['IDEmployee'], shift_key):
            logger.debug(f"FAI Enforcement: {emp['Employee']} non presente, skip")
            continue
        
        # Verifica FAI compilato
        if check_shift_fai_completed(conn, emp['Employee'], shift_start_dt):
            logger.debug(f"FAI Enforcement: {emp['Employee']} ha compilato FAI ✓")
            continue
        
        # Anti-duplicazione
        if check_already_escalated(conn, 'SHIFT_CHECK', shift_label,
                                    emp['EmployeeHireHistoryId'], level=1):
            logger.debug(f"FAI Enforcement: escalation già registrata per {emp['Employee']}")
            continue
        
        # Violazione trovata!
        violations.append(emp)
        logger.warning(f"FAI Enforcement: ⚠️ {emp['Employee']} NON ha compilato FAI "
                        f"per turno {shift_label}")
        
        # Log evento
        log_enforcement_event(
            conn, 'SHIFT_CHECK',
            employee_hhid=emp['EmployeeHireHistoryId'],
            employee_name=emp['Employee'],
            shift_time=shift_label,
            escalation_level=1,
            notes=f"FAI non compilato entro 60 min dal turno {shift_label}"
        )
    
    # Invia email L1 per tutte le violazioni
    if violations:
        l1_recipients = get_escalation_recipients(conn, 1, employees)
        for emp in violations:
            send_escalation_email(
                level=1,
                employee_name=emp['Employee'],
                shift_label=shift_label,
                recipients=l1_recipients,
                logo_path=logo_path
            )
    
    logger.info(f"FAI Enforcement: shift check completato - {len(violations)} violazioni")


def process_pending_escalations(conn, logo_path: str = "logo.png"):
    """
    Controlla eventi aperti e processa escalation L1→L2 e L2→L3.
    Chiamato ad ogni ciclo del worker.
    """
    now = datetime.now()
    esc_info = should_escalate(now)
    
    if not esc_info:
        return
    
    shift_key, target_level = esc_info
    source_level = target_level - 1
    shift_label = SHIFT_TIMES[shift_key]['label']
    shift_start_dt = get_shift_start_datetime(shift_key, now)
    
    logger.info(f"FAI Enforcement: ===== ESCALATION L{source_level}→L{target_level} "
                 f"turno {shift_label} =====")
    
    # Recupera eventi aperti al livello precedente
    pending = get_pending_escalations(conn, 'SHIFT_CHECK', source_level, shift_label)
    
    if not pending:
        logger.info(f"FAI Enforcement: nessun evento pendente per escalation")
        return
    
    employees = get_responsible_employees(conn)
    admin_info = get_administrator_info(conn)
    
    for event in pending:
        # Re-check: forse il FAI è stato compilato nel frattempo
        if check_shift_fai_completed(conn, event['EmployeeName'], shift_start_dt):
            logger.info(f"FAI Enforcement: ✅ {event['EmployeeName']} ha compilato FAI - "
                         f"chiudo evento {event['EnforcementLogId']}")
            update_enforcement_event(conn, event['EnforcementLogId'],
                                     FaiCompleted=1,
                                     FaiCompletedTime=datetime.now(),
                                     DateOut=datetime.now())
            continue
        
        # Anti-duplicazione
        if check_already_escalated(conn, 'SHIFT_CHECK', shift_label,
                                    event['EmployeeHireHistoryId'],
                                    level=target_level):
            continue
        
        # Escalation!
        logger.warning(f"FAI Enforcement: 🔺 ESCALATION L{target_level} per "
                        f"{event['EmployeeName']}")
        
        recipients = get_escalation_recipients(conn, target_level, employees,
                                                employee_hhid=event['EmployeeHireHistoryId'])
        
        referat_pdf = None
        referat_registro_id = None
        
        # Livello 3: genera REFERAT automatico
        if target_level == 3 and admin_info:
            referat_pdf = create_automatic_referat(
                conn,
                employee_hhid=event['EmployeeHireHistoryId'],
                employee_name=event['EmployeeName'],
                shift_label=shift_label,
                admin_info=admin_info
            )
            if referat_pdf:
                logger.info(f"FAI Enforcement: REFERAT generato: {referat_pdf}")
        
        # Invia email
        send_escalation_email(
            level=target_level,
            employee_name=event['EmployeeName'],
            shift_label=shift_label,
            recipients=recipients,
            logo_path=logo_path,
            referat_pdf_path=referat_pdf
        )
        
        # Log nuovo evento di escalation
        log_enforcement_event(
            conn, 'SHIFT_CHECK',
            employee_hhid=event['EmployeeHireHistoryId'],
            employee_name=event['EmployeeName'],
            shift_time=shift_label,
            escalation_level=target_level,
            notes=f"Escalation L{target_level} - FAI ancora non compilato"
        )
        
        # Aggiorna evento precedente
        update_kwargs = {'EscalationLevel': target_level}
        if target_level == 3 and referat_pdf:
            update_kwargs['ReferatGenerated'] = 1
        update_enforcement_event(conn, event['EnforcementLogId'], **update_kwargs)


def run_new_order_check(conn, logo_path: str = "logo.png"):
    """
    Orchestratore per il monitoraggio di nuovi ordini.
    Rileva nuovi ordini con template FAI e avvia il ciclo di enforcement.
    """
    now = datetime.now()
    shift_key = get_current_shift(now)
    shift_label = SHIFT_TIMES.get(shift_key, {}).get('label', '??:??')
    
    logger.info("FAI Enforcement: ===== NEW ORDER CHECK =====")
    
    new_orders = detect_new_orders(conn)
    
    if not new_orders:
        logger.info("FAI Enforcement: nessun nuovo ordine con FAI")
        return
    
    employees = get_responsible_employees(conn)
    
    for order in new_orders:
        order_id = order['IDOrder']
        order_number = order['OrderNumber']
        
        # Verifica se FAI già compilato per questo ordine
        if check_order_fai_completed(conn, order_id):
            logger.debug(f"FAI Enforcement: ordine {order_number} ha FAI compilato ✓")
            continue
        
        # Anti-duplicazione
        if check_already_escalated(conn, 'NEW_ORDER', order_id=order_id, level=1):
            continue
        
        logger.warning(f"FAI Enforcement: ⚠️ Nuovo ordine {order_number} "
                        f"({order['FaiTitle']}) senza FAI!")
        
        # Log evento
        log_enforcement_event(
            conn, 'NEW_ORDER',
            order_id=order_id,
            order_number=order_number,
            shift_time=shift_label,
            escalation_level=1,
            notes=f"Nuovo ordine rilevato senza FAI - Template: {order['FaiTitle']}"
        )
        
        # Invia email L1
        l1_recipients = get_escalation_recipients(conn, 1, employees)
        send_escalation_email(
            level=1,
            employee_name="(Responsabile linea)",
            shift_label=shift_label,
            recipients=l1_recipients,
            order_info=f"{order_number} ({order['FaiTitle']})",
            logo_path=logo_path
        )
    
    logger.info(f"FAI Enforcement: new order check completato")


def process_new_order_escalations(conn, logo_path: str = "logo.png"):
    """Processa escalation per nuovi ordini senza FAI."""
    now = datetime.now()
    employees = get_responsible_employees(conn)
    admin_info = get_administrator_info(conn)
    
    # Check L1→L2 (eventi di 30+ min fa)
    for target_level in [2, 3]:
        source_level = target_level - 1
        pending = get_pending_escalations(conn, 'NEW_ORDER', source_level)
        
        for event in pending:
            if not event['OrderId']:
                continue
            
            # Re-check FAI
            if check_order_fai_completed(conn, event['OrderId']):
                update_enforcement_event(conn, event['EnforcementLogId'],
                                         FaiCompleted=1,
                                         FaiCompletedTime=datetime.now(),
                                         DateOut=datetime.now())
                continue
            
            # Anti-duplicazione
            if check_already_escalated(conn, 'NEW_ORDER',
                                        order_id=event['OrderId'],
                                        level=target_level):
                continue
            
            recipients = get_escalation_recipients(conn, target_level, employees,
                                                    employee_hhid=event.get('EmployeeHireHistoryId'))
            
            referat_pdf = None
            if target_level == 3 and admin_info:
                # Per ordini, il referat è generico (non su un dipendente specifico)
                referat_pdf = create_automatic_referat(
                    conn,
                    employee_hhid=event.get('EmployeeHireHistoryId'),
                    employee_name=event.get('EmployeeName', 'Responsabile linea'),
                    shift_label=event.get('ShiftTime', ''),
                    admin_info=admin_info,
                    order_info=event.get('OrderNumber')
                )
            
            send_escalation_email(
                level=target_level,
                employee_name=event.get('EmployeeName', 'Responsabile linea'),
                shift_label=event.get('ShiftTime', ''),
                recipients=recipients,
                order_info=event.get('OrderNumber'),
                logo_path=logo_path,
                referat_pdf_path=referat_pdf
            )
            
            log_enforcement_event(
                conn, 'NEW_ORDER',
                order_id=event['OrderId'],
                order_number=event['OrderNumber'],
                shift_time=event.get('ShiftTime'),
                escalation_level=target_level,
                notes=f"Escalation L{target_level} - Ordine {event['OrderNumber']} senza FAI"
            )
            
            update_kwargs = {'EscalationLevel': target_level}
            if target_level == 3 and referat_pdf:
                update_kwargs['ReferatGenerated'] = 1
            update_enforcement_event(conn, event['EnforcementLogId'], **update_kwargs)


# ================================================================
# 11. ENFORCEMENT BASATO SUL PIANO DI PRODUZIONE
# ================================================================

# Livelli di escalation basati su PlannedStart:
#   Deadline FAI = PlannedStart - 3h
#   L1 = PlannedStart - 2h  (1h dopo deadline → Capo Reparto)
#   L2 = PlannedStart - 1h  (2h dopo deadline → Capo Produzione)
#   L3 = PlannedStart       (3h dopo deadline → Qualità + REFERAT)
PLANNING_ESCALATION = {
    1: {'hours_before_start': 2, 'label': 'Capo Reparto'},
    2: {'hours_before_start': 1, 'label': 'Capo Produzione'},
    3: {'hours_before_start': 0, 'label': 'Qualità + Amministratore + REFERAT'},
}


def _resolve_order_id(conn, order_number: str) -> Optional[int]:
    """Risolve un OrderNumber in IDOrder dal database."""
    query = """
        SELECT TOP 1 IDOrder
        FROM [Traceability_RS].[dbo].[Orders]
        WHERE OrderNumber = ?
        ORDER BY IDOrder DESC
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (order_number,))
            row = cur.fetchone()
        return row.IDOrder if row else None
    except Exception as e:
        logger.warning(f"FAI Enforcement: errore resolve OrderNumber '{order_number}': {e}")
        return None


def determine_planning_escalation_level(now: datetime, planned_start: datetime) -> Optional[int]:
    """Determina il livello di escalation basato su PlannedStart.
    
    Deadline FAI = PlannedStart - 3h
    L1 scatta a PlannedStart - 2h (1h dopo deadline)
    L2 scatta a PlannedStart - 1h (2h dopo deadline)
    L3 scatta a PlannedStart      (3h dopo deadline → REFERAT)
    
    Ritorna il livello massimo raggiunto, o None se troppo presto.
    """
    deadline = planned_start - timedelta(hours=3)
    
    if now < deadline:
        return None  # Troppo presto, FAI non ancora dovuto
    
    l1_time = planned_start - timedelta(hours=2)
    l2_time = planned_start - timedelta(hours=1)
    l3_time = planned_start
    
    if now >= l3_time:
        return 3
    elif now >= l2_time:
        return 2
    elif now >= l1_time:
        return 1
    else:
        # Tra deadline e L1 (prima ora di monitoraggio) — ancora in fase di grazia
        return None


def get_planning_violations(conn) -> List[Dict]:
    """Legge il piano di produzione Excel e identifica ordini Autocheck=1
    con FAI mancante che richiedono enforcement.
    
    Per ogni ordine nel PlanningMachine:
    1. Verifica se il template della fase ha Autocheck=1
    2. Verifica se now >= PlannedStart - 3h (deadline FAI scaduta)
    3. Verifica se il FAI è stato compilato
    4. Determina il livello di escalation attuale
    
    Restituisce lista di violazioni con dettagli per l'escalation.
    """
    try:
        import fai_autocheck
    except ImportError:
        logger.error("FAI Enforcement: impossibile importare fai_autocheck")
        return []
    
    now = datetime.now()
    violations = []
    
    # 1. Carica template Autocheck=1
    try:
        templates = fai_autocheck.get_autocheck_templates(conn)
    except Exception as e:
        logger.error(f"FAI Enforcement: errore caricamento template autocheck: {e}")
        return []
    
    if not templates:
        logger.debug("FAI Enforcement: nessun template con Autocheck=1")
        return []
    
    # 2. Leggi piano produzione dal file Excel
    #    lookback_hours=1: include ordini con PlannedStart fino a 1h nel passato
    #    per catturare L3 escalation (che scatta a PlannedStart)
    try:
        planning_rows = fai_autocheck.read_planning_excel(lookback_hours=1)
    except Exception as e:
        logger.error(f"FAI Enforcement: errore lettura planning Excel: {e}")
        return []
    
    if not planning_rows:
        logger.debug("FAI Enforcement: nessuna riga nel planning Excel")
        return []
    
    # 3. Per ogni riga del planning
    for pr in planning_rows:
        phase_upper = pr['phase'].upper()
        template = templates.get(phase_upper)
        if not template:
            continue  # Fase senza template Autocheck
        
        planned_start = pr['planned_start']
        
        # 4. Determina livello di escalation
        level = determine_planning_escalation_level(now, planned_start)
        if level is None:
            continue  # Troppo presto o nella fase di grazia
        
        order_number = pr['order_number']
        id_phase = template['IdPhase']
        
        # 5. Verifica se FAI già compilato
        try:
            if check_order_fai_completed_by_number(conn, order_number, id_phase):
                logger.debug(
                    f"FAI Enforcement: ordine {order_number} fase {phase_upper} "
                    f"ha FAI Autocheck compilato ✓")
                continue
        except Exception as e:
            logger.warning(
                f"FAI Enforcement: errore verifica FAI per {order_number}: {e}")
            continue
        
        # 6. Violazione trovata!
        deadline = planned_start - timedelta(hours=3)
        violations.append({
            'order_number': order_number,
            'phase': pr['phase'],
            'phase_upper': phase_upper,
            'planned_start': planned_start,
            'deadline': deadline,
            'current_level': level,
            'id_phase': id_phase,
            'template': template,
        })
    
    if violations:
        logger.info(
            f"FAI Enforcement: {len(violations)} violazioni planning rilevate")
    
    return violations


def run_planning_based_enforcement(conn, logo_path: str = "logo.png"):
    """Orchestratore principale per enforcement basato sul piano di produzione.
    
    Logica temporale per ogni ordine Autocheck=1 nel PlanningMachine:
      - Deadline FAI = PlannedStart - 3h (il FAI deve essere compilato entro qui)
      - L1 a PlannedStart - 2h → email Capo Reparto
      - L2 a PlannedStart - 1h → email Capo Produzione  
      - L3 a PlannedStart → email Qualità + Amministratore + REFERAT
    
    Esempio: produzione programmata alle 15:00
      → FAI deve essere compilato entro le 12:00
      → L1 alle 13:00, L2 alle 14:00, L3 alle 15:01
    """
    logger.info("FAI Enforcement: ===== PLANNING-BASED ENFORCEMENT CHECK =====")
    
    # 1. Trova violazioni dal planning
    violations = get_planning_violations(conn)
    if not violations:
        logger.info("FAI Enforcement: nessuna violazione planning rilevata")
        return
    
    # 2. Recupera dati necessari per le notifiche
    employees = get_responsible_employees(conn)
    admin_info = get_administrator_info(conn)
    
    for v in violations:
        order_number = v['order_number']
        level = v['current_level']
        template = v['template']
        planned_start = v['planned_start']
        planned_str = planned_start.strftime('%d/%m/%Y %H:%M')
        
        # Risolvi IDOrder per il tracking
        order_id = _resolve_order_id(conn, order_number)
        
        # Anti-duplicazione: controlla se già inviata escalation per questo livello
        if check_already_escalated(conn, 'PLANNING_CHECK',
                                    order_id=order_id, level=level):
            logger.debug(
                f"FAI Enforcement: escalation L{level} già registrata per "
                f"ordine {order_number}")
            continue
        
        logger.warning(
            f"FAI Enforcement: ⚠️ PLANNING VIOLATION L{level} — "
            f"Ordine {order_number} ({template['FaiTitle']}), "
            f"PlannedStart={planned_str}, "
            f"Deadline FAI={v['deadline'].strftime('%H:%M')}")
        
        # 3. Determina destinatari per il livello
        recipients = get_escalation_recipients(conn, level, employees)
        
        shift_key = get_current_shift()
        shift_label = SHIFT_TIMES.get(shift_key, {}).get('label', '??:??')
        
        order_info = (
            f"{order_number} ({template['FaiTitle']}) — "
            f"Produzione programmata: {planned_str}"
        )
        
        # 4. L3: genera REFERAT automatico
        referat_pdf = None
        if level == 3 and admin_info:
            # Per violazioni planning, il referat è generico (non su dipendente specifico)
            referat_pdf = create_automatic_referat(
                conn,
                employee_hhid=None,
                employee_name=f"Responsabile linea — Ordine {order_number}",
                shift_label=shift_label,
                admin_info=admin_info,
                order_info=order_number
            )
            if referat_pdf:
                logger.info(f"FAI Enforcement: REFERAT generato: {referat_pdf}")
        
        # 5. Invia email escalation
        send_escalation_email(
            level=level,
            employee_name=f"(Responsabile linea)",
            shift_label=shift_label,
            recipients=recipients,
            order_info=order_info,
            logo_path=logo_path,
            referat_pdf_path=referat_pdf
        )
        
        # 6. Log evento
        log_enforcement_event(
            conn, 'PLANNING_CHECK',
            order_id=order_id,
            order_number=order_number,
            shift_time=shift_label,
            escalation_level=level,
            notes=(
                f"Planning-based enforcement L{level} — "
                f"Template: {template['FaiTitle']}, "
                f"PlannedStart: {planned_str}, "
                f"Deadline FAI: {v['deadline'].strftime('%H:%M')}"
            )
        )
    
    logger.info(
        f"FAI Enforcement: planning enforcement completato — "
        f"{len(violations)} violazioni processate")
