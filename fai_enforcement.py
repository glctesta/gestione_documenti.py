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
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger("TraceabilityRS")

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
       AND h.EmployerId = 2
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
        with conn.cursor() as cur:
            cur.execute(SQL_RECIPIENTS)
            rows = cur.fetchall()
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
    """Verifica se l'operatore ha compilato almeno un FAI dopo l'inizio turno."""
    query = """
        SELECT TOP 1 FaiLogId 
        FROM [Traceability_RS].[fai].[FaiLogs]
        WHERE Operator = ? 
          AND DateIn >= ?
          AND DateOut IS NULL
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
    """Verifica se esiste un FAI compilato per un dato ordine."""
    query = """
        SELECT TOP 1 FaiLogId 
        FROM [Traceability_RS].[fai].[FaiLogs]
        WHERE OrderId = ?
          AND DateOut IS NULL
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (order_id,))
            row = cur.fetchone()
        return row is not None
    except Exception as e:
        logger.error(f"FAI Enforcement: errore check FAI ordine {order_id}: {e}", exc_info=True)
        return False


# ================================================================
# 5. RILEVAMENTO NUOVI ORDINI
# ================================================================

SQL_NEW_ORDERS = """
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
      )
"""


def detect_new_orders(conn) -> List[Dict]:
    """Rileva nuovi ordini con template FAI nell'ultima ora."""
    new_orders = []
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_NEW_ORDERS)
            rows = cur.fetchall()
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

def get_escalation_recipients(conn, level: int, employees: List[Dict]) -> List[str]:
    """
    Restituisce le email dei destinatari per il livello di escalation.
    L1: FunctionCode 60-69 (Capo Reparto)
    L2: FunctionCode 70-79 (Capo Produzione)
    L3: FunctionCode >= 80 (Qualità) + Amministratore
    """
    recipients = []
    
    if level == 1:
        recipients = [e['WorkEmail'] for e in employees if 60 <= e['FunctionCode'] <= 69]
    elif level == 2:
        recipients = [e['WorkEmail'] for e in employees if 70 <= e['FunctionCode'] <= 79]
    elif level == 3:
        # Qualità (FunctionCode >= 80)
        recipients = [e['WorkEmail'] for e in employees if e['FunctionCode'] >= 80]
        # + Amministratore
        try:
            admin = get_administrator_info(conn)
            if admin and admin.get('email'):
                recipients.append(admin['email'])
        except Exception:
            pass
    
    return list(dict.fromkeys(recipients))  # Deduplica


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
    """Recupera eventi aperti per un livello che necessitano escalation."""
    query = """
        SELECT EnforcementLogId, EmployeeHireHistoryId, EmployeeName,
               OrderId, OrderNumber, ShiftTime, EscalationLevel
        FROM [Traceability_RS].[fai].[FaiEnforcementLog]
        WHERE EventType = ?
          AND CheckDate = CAST(GETDATE() AS DATE)
          AND EscalationLevel = ?
          AND FaiCompleted = 0
          AND DateOut IS NULL
    """
    params = [event_type, current_level]
    
    if shift_time:
        query += " AND ShiftTime = ?"
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
            f"Subsemnatul sistemul automat TraceabilityRS, în virtutea regulamentului "
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
        
        recipients = get_escalation_recipients(conn, target_level, employees)
        
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
            
            recipients = get_escalation_recipients(conn, target_level, employees)
            
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
