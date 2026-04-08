# -*- coding: utf-8 -*-
"""
Modulo per la gestione delle escalation relative alle discrepanze del piano di produzione.

Funzionalità:
- Pulizia duplicati PlanAlerts (CTE DELETE)
- Recupero alert senza risposta
- Invio email di sollecitazione (max 3 livelli, poi escalation management)
- Report mensile riepilogativo
- Report settimanale per pattern ricorrenti
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import os

logger = logging.getLogger("TraceabilityRS")

TEST_EMAIL = 'gianluca.testa@vandewiele.com'


def get_plan_check_mode(conn) -> str:
    """Legge il valore di Sys_enable_control_plan_check da settings.
    
    Returns:
        'True'  - Funzionalità attiva normalmente
        'False' - Tutto disabilitato (menu + background)
        'Test'  - Attivo ma email reindirizzate a gianluca.testa@vandewiele.com
    """
    try:
        query = """
        SELECT TOP 1 [value]
        FROM traceability_rs.dbo.settings
        WHERE atribute = 'Sys_enable_control_plan_check'
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row and row[0]:
                val = str(row[0]).strip()
                logger.info(f"Plan check mode: '{val}'")
                return val
    except Exception as e:
        logger.warning(f"Errore lettura Sys_enable_control_plan_check: {e}")
    return 'False'  # Default: disabilitato per sicurezza


def _apply_test_mode_override(mode: str, to_emails: list, cc_emails: list,
                              subject: str) -> tuple:
    """In modalità Test, reindirizza tutte le email a TEST_EMAIL.
    
    Args:
        mode: 'True', 'False' o 'Test'
        to_emails: lista destinatari TO originali
        cc_emails: lista destinatari CC originali
        subject: oggetto email originale
    
    Returns:
        (to_emails, cc_emails, subject) — modificati se Test
    """
    if mode == 'Test':
        original_to = '; '.join(to_emails) if to_emails else 'N/A'
        original_cc = '; '.join(cc_emails) if cc_emails else 'N/A'
        subject = f"[TEST] {subject}"
        logger.info(f"TEST MODE: email reindirizzata a {TEST_EMAIL} "
                     f"(originali TO: {original_to}, CC: {original_cc})")
        return [TEST_EMAIL], [], subject
    return to_emails, cc_emails, subject


# ============================================================
# PULIZIA DUPLICATI
# ============================================================

def cleanup_duplicate_alerts(conn) -> int:
    """Elimina i duplicati dalla tabella PlanAlerts usando CTE con ROW_NUMBER.
    
    Mantiene solo il primo record (AlertId minore) per ogni combinazione univoca di
    IdOrder, ProductName, PhaseName, QtyInXls, QtyProduced, QtyExpected,
    ProjectedEnd, Deficit, StatusColor, AlertDate (solo data), OnFuture.
    
    Returns:
        Numero di record eliminati.
    """
    try:
        query = """
        WITH CTE AS (
            SELECT 
                AlertId,
                ROW_NUMBER() OVER (
                    PARTITION BY 
                        IdOrder, ProductName, PhaseName,
                        QtyInXls, QtyProduced, QtyExpected,
                        ProjectedEnd, Deficit, StatusColor,
                        CAST(AlertDate AS DATE), OnFuture
                    ORDER BY AlertId
                ) AS RowNum
            FROM [Traceability_RS].[dbo].[PlanAlerts]
        )
        DELETE FROM [Traceability_RS].[dbo].[PlanAlerts]
        WHERE AlertId IN (
            SELECT AlertId FROM CTE WHERE RowNum > 1
        )
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            deleted = cursor.rowcount
            conn.commit()
        if deleted > 0:
            logger.info(f"PlanAlerts: eliminati {deleted} record duplicati")
        return deleted
    except Exception as e:
        logger.error(f"Errore pulizia duplicati PlanAlerts: {e}")
        return 0


def get_unresponded_alerts_summary(conn) -> list:
    """Recupera un riepilogo raggruppato per Ordine+Prodotto degli alert senza risposta.
    
    Returns:
        Lista di righe con: OrderNumber, ProductName, TotalAlerts,
        RedCount, OutOfPlanCount, TotalDeficit, Phases, FirstAlertDate, LastAlertDate
    """
    query = """
    SELECT
        o.ordernumber AS OrderNumber,
        AL.ProductName,
        COUNT(DISTINCT AL.PhaseName + '|' + CONVERT(VARCHAR(10), AL.AlertDate, 120)) AS TotalAlerts,
        SUM(CASE WHEN AL.StatusColor = 'red' THEN 1 ELSE 0 END) AS RedCount,
        SUM(CASE WHEN AL.StatusColor <> 'red' THEN 1 ELSE 0 END) AS OutOfPlanCount,
        SUM(ISNULL(AL.Deficit, 0)) AS TotalDeficit,
        STUFF((
            SELECT DISTINCT ', ' + AL2.PhaseName
            FROM [Traceability_RS].[dbo].[PlanAlerts] AL2
            INNER JOIN traceability_rs.dbo.orders o2 ON o2.idorder = AL2.idorder
            LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa2 ON pa2.AlertId = AL2.AlertId
            WHERE pa2.AlertId IS NULL
              AND o2.ordernumber = o.ordernumber
              AND AL2.ProductName = AL.ProductName
              AND NOT EXISTS (
                  SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AX2
                  INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PX2 ON PX2.AlertId = AX2.AlertId
                  WHERE AX2.idorder = AL2.idorder AND AX2.ProductName = AL2.ProductName
                    AND AX2.PhaseName = AL2.PhaseName
                    AND CAST(AX2.AlertDate AS DATE) = CAST(AL2.AlertDate AS DATE)
              )
            FOR XML PATH(''), TYPE
        ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS Phases,
        MIN(CAST(AL.AlertDate AS DATE)) AS FirstAlertDate,
        MAX(CAST(AL.AlertDate AS DATE)) AS LastAlertDate
    FROM [Traceability_RS].[dbo].[PlanAlerts] AL
    INNER JOIN traceability_rs.dbo.orders o ON o.idorder = AL.idorder
    LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa ON pa.AlertId = AL.AlertId
    WHERE pa.AlertId IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AX
          INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PX ON PX.AlertId = AX.AlertId
          WHERE AX.idorder = AL.idorder AND AX.ProductName = AL.ProductName
            AND AX.PhaseName = AL.PhaseName
            AND CAST(AX.AlertDate AS DATE) = CAST(AL.AlertDate AS DATE)
      )
    GROUP BY o.ordernumber, AL.ProductName
    ORDER BY o.ordernumber, AL.ProductName
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Errore recupero riepilogo alert: {e}")
        return []


def get_alerts_for_order_product(conn, order_number: str, product_name: str) -> list:
    """Recupera tutti gli alert dettagliati per un ordine+prodotto specifico."""
    query = """
    SELECT DISTINCT
        AL.AlertId,
        o.ordernumber AS OrderNumber,
        AL.ProductName,
        p.PhaseName,
        AL.QtyInXls,
        AL.QtyProduced,
        AL.QtyExpected,
        AL.ProjectedEnd,
        AL.Deficit,
        AL.StatusColor,
        CAST(AL.AlertDate AS DATE) AS AlertDate,
        p.PhaseOrder,
        AL.OnFuture
    FROM [Traceability_RS].[dbo].[PlanAlerts] AL
    INNER JOIN traceability_rs.dbo.orders o ON o.idorder = AL.idorder
    INNER JOIN traceability_rs.dbo.Phases P ON p.phasename = AL.Phasename
    LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa ON pa.AlertId = AL.AlertId
    WHERE pa.AlertId IS NULL
      AND o.ordernumber = ?
      AND AL.ProductName = ?
      AND NOT EXISTS (
          SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AX
          INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PX ON PX.AlertId = AX.AlertId
          WHERE AX.idorder = AL.idorder AND AX.ProductName = AL.ProductName
            AND AX.PhaseName = AL.PhaseName
            AND CAST(AX.AlertDate AS DATE) = CAST(AL.AlertDate AS DATE)
      )
    ORDER BY p.phaseorder, CAST(AL.AlertDate AS DATE)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (order_number, product_name))
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Errore recupero alert dettaglio per {order_number}/{product_name}: {e}")
        return []


def get_all_alert_ids_for_order_product(conn, order_number: str,
                                         product_name: str) -> list:
    """Recupera TUTTI gli AlertId non giustificati per un ordine+prodotto."""
    query = """
    SELECT AL.AlertId
    FROM [Traceability_RS].[dbo].[PlanAlerts] AL
    INNER JOIN traceability_rs.dbo.orders o ON o.idorder = AL.idorder
    LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa ON pa.AlertId = AL.AlertId
    WHERE pa.AlertId IS NULL
      AND o.ordernumber = ?
      AND AL.ProductName = ?
      AND NOT EXISTS (
          SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AX
          INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PX ON PX.AlertId = AX.AlertId
          WHERE AX.idorder = AL.idorder AND AX.ProductName = AL.ProductName
            AND AX.PhaseName = AL.PhaseName
            AND CAST(AX.AlertDate AS DATE) = CAST(AL.AlertDate AS DATE)
      )
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (order_number, product_name))
            return [row.AlertId for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Errore recupero AlertId per {order_number}/{product_name}: {e}")
        return []


def get_unresponded_alerts(conn) -> list:
    """Recupera gli alert PlanAlerts senza risposta, DISTINCT per data (no ore).
    
    Esclude automaticamente ordini/prodotto/fase per i quali è stata inserita
    una giustificazione oggi (CAST(ResponseDate AS DATE) = oggi),
    indipendentemente dalla data dell'alert originale.
    Se il problema si ripresenta il giorno dopo, il ciclo riparte.
    """
    query = """
    SELECT DISTINCT
        AL.AlertId,
        o.ordernumber AS OrderNumber,
        AL.ProductName,
        p.PhaseName,
        AL.QtyInXls,
        AL.QtyProduced,
        AL.QtyExpected,
        AL.ProjectedEnd,
        AL.Deficit,
        AL.StatusColor,
        CAST(AL.AlertDate AS DATE) AS AlertDate,
        p.PhaseOrder,
        AL.OnFuture
    FROM [Traceability_RS].[dbo].[PlanAlerts] AL
    INNER JOIN traceability_rs.dbo.orders o ON o.idorder = AL.idorder
    INNER JOIN traceability_rs.dbo.Phases P ON p.phasename = AL.Phasename
    LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa ON pa.AlertId = AL.AlertId
    WHERE pa.AlertId IS NULL
      -- Escludi alert con risposta per stessa data alert
      AND NOT EXISTS (
          SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AX
          INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PX ON PX.AlertId = AX.AlertId
          WHERE AX.idorder = AL.idorder AND AX.ProductName = AL.ProductName
            AND AX.PhaseName = AL.PhaseName
            AND CAST(AX.AlertDate AS DATE) = CAST(AL.AlertDate AS DATE)
      )
      -- Escludi ordini giustificati OGGI: se qualcuno ha risposto oggi
      -- per lo stesso ordine/prodotto/fase, non rinviare fino a domani
      AND NOT EXISTS (
          SELECT 1 FROM [Traceability_RS].[dbo].[PlanAlerts] AY
          INNER JOIN [Traceability_RS].[dbo].[PlanAlertResponses] PY ON PY.AlertId = AY.AlertId
          WHERE AY.idorder = AL.idorder AND AY.ProductName = AL.ProductName
            AND AY.PhaseName = AL.PhaseName
            AND CAST(PY.ResponseDate AS DATE) = CAST(GETDATE() AS DATE)
      )
    ORDER BY o.ordernumber, p.phaseorder, CAST(AL.AlertDate AS DATE)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Errore recupero alert senza risposta: {e}")
        return []


def get_alert_ids_for_row(conn, order_number: str, product_name: str,
                          phase_name: str, alert_date) -> list:
    """Recupera tutti gli AlertId che corrispondono a una riga DISTINCT.
    
    Serve perché la GUI mostra dati DISTINCT per data, ma nella tabella
    ci possono essere più record con ore diverse.
    """
    query = """
    SELECT AL.AlertId
    FROM [Traceability_RS].[dbo].[PlanAlerts] AL
    INNER JOIN traceability_rs.dbo.orders o ON o.idorder = AL.idorder
    LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa ON pa.AlertId = AL.AlertId
    WHERE o.ordernumber = ?
      AND AL.ProductName = ?
      AND AL.PhaseName = ?
      AND CAST(AL.AlertDate AS DATE) = ?
      AND pa.AlertId IS NULL
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (order_number, product_name, phase_name, alert_date))
            return [row.AlertId for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Errore recupero AlertId per riga: {e}")
        return []


def save_response(conn, alert_ids: list, plan_response_id: int,
                  operator: str, notes: str = '') -> bool:
    """Salva la risposta per tutti gli AlertId associati a una riga."""
    try:
        query = """
        INSERT INTO traceability_rs.dbo.PlanAlertResponses
            (AlertId, PlanResponseId, Operator, ResponseDate, Notes)
        VALUES (?, ?, ?, GETDATE(), ?)
        """
        with conn.cursor() as cursor:
            for alert_id in alert_ids:
                cursor.execute(query, (alert_id, plan_response_id, operator, notes))
        conn.commit()
        logger.info(f"Salvate {len(alert_ids)} risposte per operatore {operator}, "
                     f"motivazione ID={plan_response_id}")
        return True
    except Exception as e:
        logger.error(f"Errore salvataggio risposta: {e}")
        return False


def get_response_reasons(conn) -> list:
    """Recupera le motivazioni attive dalla tabella PlanRespect."""
    try:
        query = """
        SELECT PlanResponseId, ResponseDescription
        FROM traceability_rs.dbo.PlanRespect
        WHERE IsActive = 1
        ORDER BY ResponseDescription
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Errore caricamento motivazioni PlanRespect: {e}")
        return []


# ============================================================
# DESTINATARI EMAIL
# ============================================================

def get_phase_leaders(conn, phase_name: str) -> List[Dict]:
    """Recupera leader e manager della fase di produzione.
    
    Returns:
        Lista di dict con: Employee, FunctionDescription, PhaseName,
        LeaderEmail, ManagerEmail
    """
    # Mapping fase -> CDC (equivalente al CASE SQL, spostato in Python
    # per evitare DECLARE che causa 'Invalid cursor state' in pyodbc)
    phase_upper = (phase_name or '').upper().strip()
    phase_map = {
        'ICT': 'PTHM',
        'TOUC-UP': 'PTHM',
        'TOUCH-UP': 'PTHM',
        'FCT': 'PTHM',
        'PTHM': 'PTHM',
        'TESTE': 'PTHM',
        'TEST': 'PTHM',
        'PROGRAMARE': 'PTHM',
        'FINAL ASSEMBLY': 'PTHM',
        'AOI': 'SMT',
        'SMT': 'SMT',
    }
    
    # Cerca match esatto, poi match LIKE per COATING%
    mapped_phase = phase_map.get(phase_upper)
    if mapped_phase is None and phase_upper.startswith('COATING'):
        mapped_phase = 'PTHM'
    
    if mapped_phase is None:
        logger.warning(f"Fase '{phase_name}' non mappata a nessun CDC")
        return []

    query = """
    WITH Manager (SubCdcId, FunctionCode, MainCdcId, WorkEmail)
    AS (
        SELECT cs.SubCdcId, f.FunctionCode, c.CdcId, a.WorkEmail
        FROM employee.dbo.EmployeeCdcStories cs
        INNER JOIN employee.dbo.CdcSub c ON c.SubCdcId = cs.SubCdcId
            AND cs.DateOut IS NULL
        INNER JOIN Employee.dbo.Functions F ON cs.FunctionId = F.FunctionId
            AND cs.DateOut IS NULL AND f.FunctionCode > 61
        INNER JOIN employee.dbo.employeehirehistory h
            ON cs.employeehirehistoryid = h.employeehirehistoryid
        INNER JOIN employee.dbo.employeeaddress a
            ON a.employeeid = h.employeeid AND a.dateout IS NULL
    )
    SELECT DISTINCT
        h.EmployeeHireHistoryId,
        UPPER(e.EmployeeName + ' ' + e.EmployeeSurname) AS Employee,
        f.FunctionDescription,
        s.SubCdcDescription AS PhaseName,
        a.WorkEmail AS LeaderEmail,
        m.WorkEmail AS ManagerEmail
    FROM employee.dbo.EmployeeHireHistory h
    INNER JOIN employee.dbo.EmployeeCdcStories css
        ON h.EmployeeHireHistoryId = css.EmployeeHireHistoryId
        AND css.DateOut IS NULL AND h.EndWorkDate IS NULL AND h.employeerid = 2
    INNER JOIN employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
    INNER JOIN employee.dbo.CdcSub s ON s.SubCdcId = css.SubCdcId
    INNER JOIN employee.dbo.Functions f ON f.FunctionId = css.FunctionId
    INNER JOIN employee.dbo.CostCenters c ON c.CdcId = s.CdcId
    LEFT JOIN Manager m ON m.MainCdcId = s.CdcId AND m.FunctionCode > 20
    INNER JOIN employee.dbo.EmployeeAddress A
        ON a.employeeid = h.employeeid AND a.dateout IS NULL
    WHERE f.FunctionCode BETWEEN 40 AND 70
        AND s.SubCdcId = (
            SELECT TOP 1 [SubCdcId]
            FROM [Traceability_RS].[dbo].[Phases]
            WHERE PhaseName = ?
        )
        AND m.WorkEmail IS NOT NULL
    ORDER BY UPPER(e.EmployeeName + ' ' + e.EmployeeSurname)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (mapped_phase,))
            results = []
            for row in cursor.fetchall():
                results.append({
                    'employee': row.Employee,
                    'function': row.FunctionDescription,
                    'phase': f"{row.PhaseName} [{phase_name}]",
                    'leader_email': row.LeaderEmail,
                    'manager_email': row.ManagerEmail
                })
            return results
    except Exception as e:
        logger.error(f"Errore recupero leader fase '{phase_name}': {e}")
        return []


def get_all_production_leaders(conn) -> List[Dict]:
    """Recupera tutti i leader di produzione (SubCdcId=15, FunctionCode 60-70)."""
    query = """
    SELECT DISTINCT
        UPPER(e.EmployeeName + ' ' + e.EmployeeSurname) AS Employee,
        f.FunctionDescription,
        s.SubCdcDescription AS PhaseName,
        a.WorkEmail AS LeaderEmail
    FROM employee.dbo.EmployeeHireHistory h
    INNER JOIN employee.dbo.EmployeeCdcStories css
        ON h.EmployeeHireHistoryId = css.EmployeeHireHistoryId
        AND css.DateOut IS NULL AND h.EndWorkDate IS NULL AND h.employeerid = 2
    INNER JOIN employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
    INNER JOIN employee.dbo.CdcSub s ON s.SubCdcId = css.SubCdcId
    INNER JOIN employee.dbo.Functions f ON f.FunctionId = css.FunctionId
    INNER JOIN employee.dbo.CostCenters c ON c.CdcId = s.CdcId
    INNER JOIN employee.dbo.EmployeeAddress A
        ON a.employeeid = h.employeeid AND a.dateout IS NULL
    WHERE f.FunctionCode BETWEEN 60 AND 70
        AND s.SubCdcId = 15
    ORDER BY UPPER(e.EmployeeName + ' ' + e.EmployeeSurname)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return [{'employee': r.Employee, 'function': r.FunctionDescription,
                     'phase': r.PhaseName, 'email': r.LeaderEmail}
                    for r in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Errore recupero leader produzione: {e}")
        return []


def get_escalation_recipients(conn) -> List[str]:
    """Legge i destinatari management da settings (Sys_Alert_not_responce_plan)."""
    from utils import get_email_recipients
    return get_email_recipients(conn, attribute='Sys_Alert_not_responce_plan')


# ============================================================
# ESCALATION LOGIC
# ============================================================

def get_escalation_count(conn, alert_id: int) -> int:
    """Conta quante escalation sono già state inviate per un alert."""
    try:
        query = """
        SELECT ISNULL(MAX(EscalationLevel), 0) AS MaxLevel
        FROM traceability_rs.dbo.PlanAlertEscalations
        WHERE AlertId = ?
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (alert_id,))
            row = cursor.fetchone()
            return row.MaxLevel if row else 0
    except Exception as e:
        logger.error(f"Errore conteggio escalation per alert {alert_id}: {e}")
        return 0


def get_last_escalation_time(conn, alert_id: int) -> Optional[datetime]:
    """Restituisce la data/ora dell'ultima escalation per un alert."""
    try:
        query = """
        SELECT MAX(SentDate) AS LastSent
        FROM traceability_rs.dbo.PlanAlertEscalations
        WHERE AlertId = ?
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (alert_id,))
            row = cursor.fetchone()
            return row.LastSent if row and row.LastSent else None
    except Exception as e:
        logger.error(f"Errore recupero ultima escalation: {e}")
        return None


def record_escalation(conn, alert_id: int, level: int,
                      recipients: str, phase_name: str) -> bool:
    """Registra una escalation inviata."""
    try:
        query = """
        INSERT INTO traceability_rs.dbo.PlanAlertEscalations
            (AlertId, EscalationLevel, SentDate, Recipients, PhaseName)
        VALUES (?, ?, GETDATE(), ?, ?)
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (alert_id, level, recipients, phase_name))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Errore registrazione escalation: {e}")
        return False


def _build_escalation_html(alerts_by_phase: Dict[str, list], level: int,
                           max_level: int = 3) -> str:
    """Costruisce il corpo HTML dell'email di escalation."""
    now = datetime.now()
    
    is_final = level > max_level
    
    title = ("⚠️ ESCALARE — Nicio răspuns la alertele planului de producție"
             if is_final else
             f"🔔 Solicitare {level}/{max_level} — Alerte plan producție nevalidate")
    
    urgency_html = ""
    if is_final:
        urgency_html = """
        <div style="background-color: #FFCDD2; border-left: 4px solid #B71C1C; 
             padding: 12px; margin: 15px 0;">
            <p style="color: #B71C1C; font-weight: bold; font-size: 14px;">
                ⚠️ ATENȚIE: Au fost trimise 3 solicitări fără niciun răspuns!</p>
            <p style="color: #333;">Responsabilii de fază nu au justificat discrepanțele
                raportate de planul de producție în termenul prevăzut de 60 de minute.
                Este necesară intervenția managementului.</p>
        </div>
        """
    
    # Costruisci tabella per fase
    tables_html = ""
    for phase, alerts in alerts_by_phase.items():
        rows = ""
        for a in alerts:
            color_badge = ('#F44336' if a.get('status_color') == 'red'
                           else '#FF9800')
            status_label = ('🔴 Întârziere' if a.get('status_color') == 'red'
                            else '🟠 În afara planului')
            rows += f"""
            <tr>
                <td style="padding: 6px 10px;">{a.get('order_number', '')}</td>
                <td style="padding: 6px 10px;">{a.get('product_name', '')}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    {a.get('qty_expected', 0)}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    {a.get('qty_produced', 0)}</td>
                <td style="padding: 6px 10px; text-align: center; font-weight: bold; 
                    color: #B71C1C;">{a.get('deficit', 0)}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    <span style="background-color: {color_badge}; color: white; 
                        padding: 2px 8px; border-radius: 4px; font-size: 11px;">
                        {status_label}</span></td>
                <td style="padding: 6px 10px; text-align: center;">
                    {a.get('alert_date', '')}</td>
            </tr>
            """
        
        tables_html += f"""
        <h4 style="color: #1565C0; margin-top: 20px;">📋 Faza: {phase}</h4>
        <table style="border-collapse: collapse; width: 100%; font-size: 12px; 
               border: 1px solid #ddd;">
            <tr style="background-color: #1565C0; color: white;">
                <th style="padding: 8px 10px; text-align: left;">Comandă</th>
                <th style="padding: 8px 10px; text-align: left;">Produs</th>
                <th style="padding: 8px 10px; text-align: center;">Cant. Așteptată</th>
                <th style="padding: 8px 10px; text-align: center;">Cant. Produsă</th>
                <th style="padding: 8px 10px; text-align: center;">Deficit</th>
                <th style="padding: 8px 10px; text-align: center;">Status</th>
                <th style="padding: 8px 10px; text-align: center;">Data Alertă</th>
            </tr>
            {rows}
        </table>
        """
    
    logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 12px; color: #333;">
        <img src="cid:company_logo" alt="Logo" 
             style="width: 150px; margin-bottom: 10px;" /><br/>
        <h2 style="color: #1565C0;">{title}</h2>
        
        <p>Bună ziua,</p>
        <p>Următoarele discrepanțe față de planul de producție 
           <strong>nu au fost justificate</strong> de responsabili în termenul 
           prevăzut de 60 de minute:</p>
        
        {urgency_html}
        {tables_html}
        
        <div style="background-color: #E3F2FD; border-left: 4px solid #1565C0; 
             padding: 10px; margin: 15px 0;">
            <p style="font-weight: bold;">
                📌 Acțiune necesară:</p>
            <p>Vă rugăm să accesați aplicația TraceabilityRS → 
               <strong>Piano produzione</strong> și să completați justificările 
               pentru alertele de mai sus.</p>
        </div>
        
        <hr style="border: 1px solid #ddd;"/>
        <p style="color: #888; font-size: 10px;">
            Email generat automat de TraceabilityRS — 
            {now.strftime('%d/%m/%Y %H:%M')}</p>
    </body>
    </html>
    """
    return body


def check_and_escalate(conn, logo_path: str = None, mode: str = 'True') -> int:
    """Controlla alert non giustificati e invia escalation se necessario.
    
    Logica:
    - Trova alert senza risposta (PlanAlertResponses IS NULL)
    - Alert giustificati oggi (ResponseDate = oggi) vengono esclusi automaticamente
    - Raggruppa TUTTI gli alert in UN'UNICA email ogni 3 ore
    - Per ogni fase, verifica:
      a) Se sono passate >= 3 ore dall'AlertDate (o dall'ultima escalation)
      b) Se le escalation inviate sono < 3 → invia a leader + manager fase
      c) Se >= 3 → invia a Sys_Alert_not_responce_plan (TO) + leader (CC)
    
    Args:
        mode: 'True' (produzione), 'Test' (email a gianluca.testa@vandewiele.com)
    
    Returns:
        Numero di email inviate (0 o 1, poiché raggruppata).
    """
    from email_connector import EmailSender
    
    ESCALATION_INTERVAL_SECONDS = 10800  # 3 ore
    
    if logo_path is None:
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    
    alerts = get_unresponded_alerts(conn)
    if not alerts:
        return 0
    
    now = datetime.now()
    
    # Raggruppa alert per PhaseName
    phase_alerts = {}  # {phase: [{alert_data}, ...]}
    for row in alerts:
        phase = row.PhaseName
        alert_data = {
            'alert_id': row.AlertId,
            'order_number': row.OrderNumber,
            'product_name': row.ProductName,
            'phase_name': phase,
            'qty_in_xls': row.QtyInXls,
            'qty_produced': row.QtyProduced,
            'qty_expected': row.QtyExpected,
            'deficit': row.Deficit,
            'status_color': row.StatusColor,
            'alert_date': str(row.AlertDate),
            'on_future': row.OnFuture
        }
        if phase not in phase_alerts:
            phase_alerts[phase] = []
        phase_alerts[phase].append(alert_data)
    
    # Filtra solo le fasi per cui è scaduto il timer di 3 ore
    phases_ready = {}  # fasi pronte per l'invio
    max_level = 0
    all_leader_emails = set()
    all_manager_emails = set()
    
    for phase, alerts_list in phase_alerts.items():
        # Usa il primo alert come riferimento per il timing
        first_alert_id = alerts_list[0]['alert_id']
        
        # Conta escalation già inviate per questa fase
        current_level = get_escalation_count(conn, first_alert_id)
        last_sent = get_last_escalation_time(conn, first_alert_id)
        
        # Se mai inviata → la prima escalation parte 3 ore dopo AlertDate
        if last_sent is None:
            alert_date_str = alerts_list[0]['alert_date']
            try:
                alert_dt = datetime.strptime(alert_date_str, '%Y-%m-%d')
                alert_dt = alert_dt.replace(hour=now.hour, minute=0)
            except ValueError:
                alert_dt = now - timedelta(hours=4)  # fallback
            
            if (now - alert_dt).total_seconds() < ESCALATION_INTERVAL_SECONDS:
                continue  # Non sono ancora passate 3 ore
        else:
            # Sono passate 3 ore dall'ultima escalation?
            if (now - last_sent).total_seconds() < ESCALATION_INTERVAL_SECONDS:
                continue
        
        next_level = current_level + 1
        if next_level > max_level:
            max_level = next_level
        
        # Raccogli destinatari per questa fase
        leaders = get_phase_leaders(conn, phase)
        leader_emails = set(
            l['leader_email'] for l in leaders if l.get('leader_email'))
        manager_emails = set(
            l['manager_email'] for l in leaders if l.get('manager_email'))
        
        all_leader_emails.update(leader_emails)
        all_manager_emails.update(manager_emails)
        
        phases_ready[phase] = {
            'alerts': alerts_list,
            'next_level': next_level
        }
    
    if not phases_ready:
        return 0
    
    # Determina destinatari per l'email unica raggruppata
    if max_level <= 3:
        # Livelli 1-3: TO ai leader, CC ai manager
        to_emails = list(all_leader_emails)
        cc_emails = list(all_manager_emails)
    else:
        # Livello 4+: TO al management, CC ai leader + manager
        mgmt_emails = get_escalation_recipients(conn)
        to_emails = mgmt_emails
        cc_emails = list(all_leader_emails | all_manager_emails)
    
    if not to_emails:
        logger.warning("Nessun destinatario per escalation raggruppata")
        return 0
    
    # Costruisci email unica con TUTTE le fasi raggruppate
    all_phase_alerts = {}
    for phase, info in phases_ready.items():
        all_phase_alerts[phase] = info['alerts']
    
    body_html = _build_escalation_html(all_phase_alerts, max_level)
    
    try:
        sender = EmailSender()
        attachments = []
        if os.path.exists(logo_path):
            attachments.append(('inline', logo_path, 'company_logo'))
        
        to_addr_list = to_emails
        all_cc = to_emails[1:] + cc_emails if len(to_emails) > 1 else cc_emails
        
        level_label = (f"Solicitare {max_level}/3"
                       if max_level <= 3 else "ESCALARE MANAGEMENT")
        
        phases_str = ', '.join(phases_ready.keys())
        total_alerts = sum(len(info['alerts']) for info in phases_ready.values())
        subj = f"[{level_label}] Alerte plan producție — {total_alerts} alerte ({phases_str})"
        
        # Applica override in modalità Test
        to_addr_list, all_cc, subj = _apply_test_mode_override(
            mode, to_addr_list, all_cc, subj)
        
        sender.send_email(
            to_email=to_addr_list[0],
            subject=subj,
            body=body_html,
            is_html=True,
            attachments=attachments if attachments else None,
            cc_emails=all_cc if all_cc else None
        )
        
        # Registra escalation per tutti gli alert di tutte le fasi
        recipients_log = '; '.join(to_emails + cc_emails)
        for phase, info in phases_ready.items():
            for alert_data in info['alerts']:
                record_escalation(conn, alert_data['alert_id'],
                                  info['next_level'], recipients_log, phase)
        
        logger.info(f"Escalation raggruppata (livello max {max_level}) inviata: "
                    f"{total_alerts} alert in {len(phases_ready)} fasi a {to_addr_list}")
        
        return 1
        
    except Exception as e:
        logger.error(f"Errore invio escalation raggruppata: {e}")
        return 0


# ============================================================
# REPORT MENSILE
# ============================================================

def send_monthly_summary(conn, logo_path: str = None, mode: str = 'True') -> bool:
    """Invia il report mensile riepilogativo delle discrepanze piano.
    
    Contenuto:
    - Totale alert nel mese precedente
    - Suddivisione per fase/prodotto
    - Tasso di risposta (% giustificati)
    - Top 5 motivazioni
    - Alert rimasti senza risposta
    
    Args:
        mode: 'True' (produzione), 'Test' (email a gianluca.testa@vandewiele.com)
    """
    from email_connector import EmailSender
    
    if logo_path is None:
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    
    now = datetime.now()
    first_of_month = now.replace(day=1)
    last_month_end = first_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    month_label = last_month_start.strftime('%B %Y')
    
    try:
        # Statistiche totali
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) AS TotalAlerts,
                    SUM(CASE WHEN pa.AlertId IS NOT NULL THEN 1 ELSE 0 END) 
                        AS Responded,
                    SUM(CASE WHEN pa.AlertId IS NULL THEN 1 ELSE 0 END) 
                        AS NotResponded,
                    SUM(CASE WHEN AL.StatusColor = 'red' THEN 1 ELSE 0 END) 
                        AS RedAlerts,
                    SUM(CASE WHEN AL.StatusColor = 'out_of_plan' THEN 1 ELSE 0 END) 
                        AS OutOfPlanAlerts
                FROM [Traceability_RS].[dbo].[PlanAlerts] AL
                LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa 
                    ON pa.AlertId = AL.AlertId
                WHERE CAST(AL.AlertDate AS DATE) 
                    BETWEEN ? AND ?
            """, (last_month_start.date(), last_month_end.date()))
            stats = cursor.fetchone()
        
        if not stats or stats.TotalAlerts == 0:
            logger.info("Report mensile: nessun alert nel mese precedente")
            return False
        
        total = stats.TotalAlerts
        responded = stats.Responded or 0
        not_responded = stats.NotResponded or 0
        response_rate = (responded / total * 100) if total > 0 else 0
        
        # Per fase
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    AL.PhaseName,
                    COUNT(*) AS Cnt,
                    SUM(CASE WHEN pa.AlertId IS NOT NULL THEN 1 ELSE 0 END) 
                        AS Resp
                FROM [Traceability_RS].[dbo].[PlanAlerts] AL
                LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa 
                    ON pa.AlertId = AL.AlertId
                WHERE CAST(AL.AlertDate AS DATE) BETWEEN ? AND ?
                GROUP BY AL.PhaseName
                ORDER BY COUNT(*) DESC
            """, (last_month_start.date(), last_month_end.date()))
            phase_stats = cursor.fetchall()
        
        # Top motivazioni
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT TOP 5
                    pr.ResponseDescription,
                    COUNT(*) AS Cnt
                FROM traceability_rs.dbo.PlanAlertResponses pa
                INNER JOIN traceability_rs.dbo.PlanRespect pr 
                    ON pa.PlanResponseId = pr.PlanResponseId
                INNER JOIN [Traceability_RS].[dbo].[PlanAlerts] AL 
                    ON AL.AlertId = pa.AlertId
                WHERE CAST(AL.AlertDate AS DATE) BETWEEN ? AND ?
                GROUP BY pr.ResponseDescription
                ORDER BY COUNT(*) DESC
            """, (last_month_start.date(), last_month_end.date()))
            top_reasons = cursor.fetchall()
        
        # Costruisci HTML
        phase_rows = ""
        for ps in phase_stats:
            rate = (ps.Resp / ps.Cnt * 100) if ps.Cnt > 0 else 0
            color = '#4CAF50' if rate >= 80 else '#FF9800' if rate >= 50 else '#F44336'
            phase_rows += f"""
            <tr>
                <td style="padding: 6px 10px;">{ps.PhaseName}</td>
                <td style="padding: 6px 10px; text-align: center;">{ps.Cnt}</td>
                <td style="padding: 6px 10px; text-align: center;">{ps.Resp}</td>
                <td style="padding: 6px 10px; text-align: center; font-weight: bold; 
                    color: {color};">{rate:.1f}%</td>
            </tr>
            """
        
        reasons_rows = ""
        for r in top_reasons:
            reasons_rows += f"""
            <tr>
                <td style="padding: 6px 10px;">{r.ResponseDescription}</td>
                <td style="padding: 6px 10px; text-align: center; 
                    font-weight: bold;">{r.Cnt}</td>
            </tr>
            """
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 12px; color: #333;">
            <img src="cid:company_logo" alt="Logo" 
                 style="width: 150px; margin-bottom: 10px;" /><br/>
            <h2 style="color:  #1565C0;">📊 Raport Lunar — Alerte Plan Producție</h2>
            <h3 style="color: #555;">{month_label}</h3>
            
            <h4>Rezumat General</h4>
            <table style="border-collapse: collapse; font-size: 13px; 
                   border: 1px solid #ddd; margin: 10px 0;">
                <tr style="background-color: #E3F2FD;">
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Total alerte</td>
                    <td style="padding: 8px 15px; text-align: center;">
                        {total}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Justificate</td>
                    <td style="padding: 8px 15px; text-align: center; 
                        color: #4CAF50;">{responded}</td>
                </tr>
                <tr style="background-color: #E3F2FD;">
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Fără răspuns</td>
                    <td style="padding: 8px 15px; text-align: center; 
                        color: #F44336; font-weight: bold;">{not_responded}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Rată răspuns</td>
                    <td style="padding: 8px 15px; text-align: center; 
                        font-weight: bold;">{response_rate:.1f}%</td>
                </tr>
                <tr style="background-color: #E3F2FD;">
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Alerte 🔴 Red</td>
                    <td style="padding: 8px 15px; text-align: center;">
                        {stats.RedAlerts or 0}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 15px; font-weight: bold;">
                        Alerte 🟠 Out of Plan</td>
                    <td style="padding: 8px 15px; text-align: center;">
                        {stats.OutOfPlanAlerts or 0}</td>
                </tr>
            </table>
            
            <h4>Statistici pe Faze</h4>
            <table style="border-collapse: collapse; width: 100%; font-size: 12px; 
                   border: 1px solid #ddd;">
                <tr style="background-color: #1565C0; color: white;">
                    <th style="padding: 8px 10px; text-align: left;">Fază</th>
                    <th style="padding: 8px 10px; text-align: center;">Total</th>
                    <th style="padding: 8px 10px; text-align: center;">
                        Justificate</th>
                    <th style="padding: 8px 10px; text-align: center;">Rată</th>
                </tr>
                {phase_rows}
            </table>
            
            <h4>Top 5 Motivații</h4>
            <table style="border-collapse: collapse; font-size: 12px; 
                   border: 1px solid #ddd;">
                <tr style="background-color: #2E7D32; color: white;">
                    <th style="padding: 8px 10px; text-align: left;">Motivație</th>
                    <th style="padding: 8px 10px; text-align: center;">Nr.</th>
                </tr>
                {reasons_rows}
            </table>
            
            <hr style="border: 1px solid #ddd; margin-top: 20px;"/>
            <p style="color: #888; font-size: 10px;">
                Raport generat automat de TraceabilityRS — 
                {now.strftime('%d/%m/%Y %H:%M')}</p>
        </body>
        </html>
        """
        
        # Destinatari
        mgmt_emails = get_escalation_recipients(conn)
        leader_list = get_all_production_leaders(conn)
        leader_emails = list(set(l['email'] for l in leader_list if l.get('email')))
        all_to = list(set(mgmt_emails + leader_emails))
        
        if not all_to:
            logger.warning("Report mensile: nessun destinatario")
            return False
        
        sender = EmailSender()
        attachments = []
        if os.path.exists(logo_path):
            attachments.append(('inline', logo_path, 'company_logo'))
        
        subj = f"📊 Raport Lunar Plan Producție — {month_label}"
        to_list = [all_to[0]]
        cc_list = all_to[1:] if len(all_to) > 1 else []
        
        # Applica override in modalità Test
        to_list, cc_list, subj = _apply_test_mode_override(
            mode, to_list, cc_list, subj)
        
        sender.send_email(
            to_email=to_list[0],
            subject=subj,
            body=body_html,
            is_html=True,
            attachments=attachments if attachments else None,
            cc_emails=cc_list if cc_list else None
        )
        logger.info(f"Report mensile piano produzione inviato a {len(all_to)} destinatari")
        return True
        
    except Exception as e:
        logger.error(f"Errore invio report mensile piano: {e}")
        return False


# ============================================================
# REPORT SETTIMANALE — PATTERN RICORRENTI
# ============================================================

def send_weekly_pattern_check(conn, logo_path: str = None, mode: str = 'True') -> bool:
    """Analizza pattern ricorrenti (stessi prodotti+fasi con warning ripetuti).
    
    Cerca nelle ultime 4 settimane prodotti/fasi che appaiono >=3 volte
    negli alert, soprattutto con StatusColor='red'.
    Suggerisce possibili errori nei cicli dello schedulatore.
    
    Args:
        mode: 'True' (produzione), 'Test' (email a gianluca.testa@vandewiele.com)
    """
    from email_connector import EmailSender
    
    if logo_path is None:
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    
    now = datetime.now()
    four_weeks_ago = now - timedelta(weeks=4)
    
    try:
        # Trova pattern ricorrenti
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    AL.ProductName,
                    AL.PhaseName,
                    AL.StatusColor,
                    COUNT(DISTINCT CAST(AL.AlertDate AS DATE)) AS DaysWithAlert,
                    MIN(CAST(AL.AlertDate AS DATE)) AS FirstAlert,
                    MAX(CAST(AL.AlertDate AS DATE)) AS LastAlert,
                    SUM(CASE WHEN pa.AlertId IS NOT NULL THEN 1 ELSE 0 END) 
                        AS TimesResponded,
                    COUNT(*) AS TotalAlerts
                FROM [Traceability_RS].[dbo].[PlanAlerts] AL
                LEFT JOIN traceability_rs.dbo.PlanAlertResponses pa 
                    ON pa.AlertId = AL.AlertId
                WHERE CAST(AL.AlertDate AS DATE) >= ?
                GROUP BY AL.ProductName, AL.PhaseName, AL.StatusColor
                HAVING COUNT(DISTINCT CAST(AL.AlertDate AS DATE)) >= 3
                ORDER BY 
                    CASE WHEN AL.StatusColor = 'red' THEN 0 ELSE 1 END,
                    COUNT(DISTINCT CAST(AL.AlertDate AS DATE)) DESC
            """, (four_weeks_ago.date(),))
            patterns = cursor.fetchall()
        
        if not patterns:
            logger.info("Report settimanale: nessun pattern ricorrente trovato")
            return False
        
        # Salva in PlanAlertWeeklyChecks
        with conn.cursor() as cursor:
            for p in patterns:
                cursor.execute("""
                    INSERT INTO traceability_rs.dbo.PlanAlertWeeklyChecks
                        (CheckDate, ProductName, PhaseName, OccurrenceCount)
                    VALUES (GETDATE(), ?, ?, ?)
                """, (p.ProductName, p.PhaseName, p.DaysWithAlert))
        conn.commit()
        
        # Costruisci tabella HTML
        rows_html = ""
        for i, p in enumerate(patterns):
            bg = ' style="background-color: #FFF3E0;"' if i % 2 == 0 else ''
            color_badge = '#F44336' if p.StatusColor == 'red' else '#FF9800'
            status_label = '🔴 Red' if p.StatusColor == 'red' else '🟠 Out of Plan'
            
            rows_html += f"""
            <tr{bg}>
                <td style="padding: 6px 10px;">{p.ProductName}</td>
                <td style="padding: 6px 10px;">{p.PhaseName}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    <span style="background-color: {color_badge}; color: white; 
                        padding: 2px 8px; border-radius: 4px; font-size: 11px;">
                        {status_label}</span></td>
                <td style="padding: 6px 10px; text-align: center; font-weight: bold; 
                    color: #B71C1C;">{p.DaysWithAlert}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    {p.FirstAlert} — {p.LastAlert}</td>
                <td style="padding: 6px 10px; text-align: center;">
                    {p.TimesResponded}/{p.TotalAlerts}</td>
            </tr>
            """
        
        red_count = sum(1 for p in patterns if p.StatusColor == 'red')
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 12px; color: #333;">
            <img src="cid:company_logo" alt="Logo" 
                 style="width: 150px; margin-bottom: 10px;" /><br/>
            <h2 style="color: #B71C1C;">
                🔍 Analiza Săptămânală — Probleme Recurente Plan Producție</h2>
            
            <p>Stimați colegi,</p>
            
            <p>Analiza ultimelor 4 săptămâni a identificat 
               <strong>{len(patterns)} combinații produs/fază</strong> cu 
               avertismente recurente în planul de producție
               {f', dintre care <strong style="color: #B71C1C;">{red_count} cu status RED (întârziere)</strong>' if red_count > 0 else ''}.</p>
            
            <div style="background-color: #FFF3E0; border-left: 4px solid #E65100; 
                 padding: 12px; margin: 15px 0;">
                <p style="color: #E65100; font-weight: bold; font-size: 13px;">
                    ⚠️ Atenție — Posibile erori în ciclurile schedulatorului</p>
                <p>Repetarea acelorași probleme pentru aceleași produse și faze poate 
                   indica faptul că <strong>ciclurile de producție configurate în 
                   schedulatorul de planificare sunt incorecte</strong>. Vă rugăm să 
                   verificați și să corectați parametrii relevanți pentru a preveni 
                   recidivarea acestor discrepanțe.</p>
            </div>
            
            <h4>Probleme Recurente (≥ 3 zile cu alerte în ultimele 4 săptămâni)</h4>
            <table style="border-collapse: collapse; width: 100%; font-size: 12px; 
                   border: 1px solid #ddd;">
                <tr style="background-color: #E65100; color: white;">
                    <th style="padding: 8px 10px; text-align: left;">Produs</th>
                    <th style="padding: 8px 10px; text-align: left;">Fază</th>
                    <th style="padding: 8px 10px; text-align: center;">Status</th>
                    <th style="padding: 8px 10px; text-align: center;">
                        Nr. Zile</th>
                    <th style="padding: 8px 10px; text-align: center;">Perioadă</th>
                    <th style="padding: 8px 10px; text-align: center;">
                        Răspunsuri</th>
                </tr>
                {rows_html}
            </table>
            
            <div style="background-color: #E8F5E9; border-left: 4px solid #2E7D32; 
                 padding: 10px; margin: 20px 0;">
                <p style="font-weight: bold; color: #2E7D32;">
                    📌 Acțiune recomandată:</p>
                <p>Vă rugăm să investigați cauzele problemelor recurente de mai sus 
                   și să luați măsuri corective urgente, în special pentru produsele 
                   cu status <strong>RED</strong>. Verificați ciclurile schedulatorului 
                   și actualizați parametrii de planificare.</p>
            </div>
            
            <hr style="border: 1px solid #ddd; margin-top: 20px;"/>
            <p style="color: #888; font-size: 10px;">
                Raport generat automat de TraceabilityRS — 
                {now.strftime('%d/%m/%Y %H:%M')}</p>
        </body>
        </html>
        """
        
        # Destinatari
        mgmt_emails = get_escalation_recipients(conn)
        leader_list = get_all_production_leaders(conn)
        leader_emails = list(set(l['email'] for l in leader_list if l.get('email')))
        
        to_emails = mgmt_emails if mgmt_emails else leader_emails
        cc_emails = leader_emails if mgmt_emails else []
        
        if not to_emails:
            logger.warning("Report settimanale: nessun destinatario")
            return False
        
        sender = EmailSender()
        attachments = []
        if os.path.exists(logo_path):
            attachments.append(('inline', logo_path, 'company_logo'))
        
        subj = (f"🔍 Analiza Săptămânală — Probleme Recurente Plan Producție — "
                f"{now.strftime('%d/%m/%Y')}")
        all_cc = (to_emails[1:] + cc_emails) if (to_emails[1:] + cc_emails) else []
        to_list = [to_emails[0]]
        
        # Applica override in modalità Test
        to_list, all_cc, subj = _apply_test_mode_override(
            mode, to_list, all_cc, subj)
        
        sender.send_email(
            to_email=to_list[0],
            subject=subj,
            body=body_html,
            is_html=True,
            attachments=attachments if attachments else None,
            cc_emails=all_cc if all_cc else None
        )
        logger.info(f"Report settimanale pattern ricorrenti inviato "
                     f"({len(patterns)} pattern trovati)")
        return True
        
    except Exception as e:
        logger.error(f"Errore invio report settimanale pattern: {e}")
        return False
