"""
kit_dashboard_logic.py
Logica DB Dashboard e Reporting del modulo Kit Preparation — Sprint 5
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §8.2, roadmap Sprint 5).

Sola lettura: dashboard stato kit per ordine, storico eccezioni,
analisi cause ricorrenti (mappata sulle 5 cause della §1.1).
"""
import logging
from typing import List, Optional

logger = logging.getLogger("PlanMonitor")

# Mappa kit_status -> (WH, Preformatura, Produzione) come simboli logici
# G=verde, O=arancione, R=rosso, '-'=non iniziata
PHASE_MAP = {
    'WH_OPEN':                  ('R', '-', '-'),
    'WH_PARTIAL':               ('O', '-', '-'),
    'REOPENED':                 ('R', 'O', '-'),
    'WH_CLOSED':                ('G', '-', '-'),
    'IN_PREFORMING':            ('G', 'G', '-'),
    'BLOCKED_MISSING_MATERIAL': ('G', 'G', 'R'),
    'RECEIVED_IN_PRODUCTION':   ('G', 'G', 'G'),
    'COMPLETED':                ('G', 'G', 'G'),
}

ALERT_STATUSES = ('REOPENED', 'BLOCKED_MISSING_MATERIAL')

EXCEPTION_EVENT_TYPES = (
    'VERIFY_FAIL', 'UNKNOWN_UNIQUE_NUMBER', 'CLOSE_DEROGATION',
    'REQUEST_MATERIAL', 'MATERIAL_FOUND', 'SOURCE_FILE_CHANGED',
)


def dashboard_rows(cursor) -> List[dict]:
    """Una riga per ordine in lavorazione, ordinata per priorita'."""
    cursor.execute("""
        SELECT ks.order_number, ks.status, ks.updated_date,
               ISNULL(op.priority, 0) AS priority,
               pl.id AS list_id, pl.status AS list_status, pl.upload_date,
               ses.phase AS session_phase, ses.status AS session_status,
               (SELECT COUNT(*) FROM Traceability_RS.dbo.kit_verification_log l
                WHERE l.order_number = ks.order_number
                  AND l.event_type = 'VERIFY_FAIL'
                  AND l.event_date >= DATEADD(DAY, -7, GETDATE())) AS recent_fails,
               (SELECT COUNT(*) FROM Traceability_RS.dbo.material_requests r
                WHERE r.order_number = ks.order_number
                  AND r.wh_status = 'PENDING' AND r.resolution IS NULL) AS open_requests
        FROM Traceability_RS.dbo.kit_status ks
        LEFT JOIN Traceability_RS.dbo.order_priority op
               ON op.order_number = ks.order_number
        OUTER APPLY (
            SELECT TOP 1 pl2.id, pl2.status, pl2.upload_date
            FROM Traceability_RS.dbo.picking_list_orders plo
            JOIN Traceability_RS.dbo.picking_lists pl2 ON pl2.id = plo.picking_list_id
            WHERE plo.order_number = ks.order_number
            ORDER BY pl2.upload_date DESC
        ) pl(id, status, upload_date)
        OUTER APPLY (
            SELECT TOP 1 s.phase, s.status
            FROM Traceability_RS.dbo.kit_sessions s
            WHERE s.picking_list_id = pl.id AND s.status IN ('ACTIVE','SUSPENDED')
            ORDER BY s.started_date DESC
        ) ses(phase, status)
        ORDER BY CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END ASC,
                 ks.order_number
    """)
    rows = []
    for r in cursor.fetchall():
        status = r[1]
        wh, pf, prod = PHASE_MAP.get(status, ('-', '-', '-'))
        alert = status in ALERT_STATUSES or (r[9] or 0) > 0 or (r[10] or 0) > 0 \
            if len(r) > 10 else status in ALERT_STATUSES
        rows.append({
            'order_number': r[0], 'kit_status': status, 'updated_date': r[2],
            'priority': int(r[3] or 0),
            'list_id': r[4], 'list_status': r[5], 'upload_date': r[6],
            'session_phase': r[7], 'session_status': r[8],
            'recent_fails': r[9] or 0, 'open_requests': r[10] or 0,
            'wh': wh, 'pf': pf, 'prod': prod,
            'alert': status in ALERT_STATUSES or (r[9] or 0) > 0,
        })
    return rows


def exceptions_history(cursor, date_from=None, date_to=None,
                       order_filter: str = '') -> List[dict]:
    """Storico eventi eccezione dal log, con nome operatore."""
    where = ["l.event_type IN ({})".format(
        ','.join(f"'{t}'" for t in EXCEPTION_EVENT_TYPES))]
    params = []
    if date_from:
        where.append("l.event_date >= ?")
        params.append(date_from)
    if date_to:
        where.append("l.event_date < DATEADD(DAY, 1, ?)")
        params.append(date_to)
    if order_filter:
        where.append("l.order_number LIKE ?")
        params.append(f"%{order_filter}%")
    cursor.execute(f"""
        SELECT l.event_date, l.order_number, l.phase, l.event_type,
               l.material_code, l.unique_number, l.qty_expected, l.qty_actual,
               ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '') AS operator,
               l.notes
        FROM Traceability_RS.dbo.kit_verification_log l
        LEFT JOIN employee.dbo.EmployeeHireHistory h
               ON h.EmployeeHireHistoryId = l.operator_id
        LEFT JOIN employee.dbo.employees e ON e.EmployeeId = h.EmployeeId
        WHERE {' AND '.join(where)}
        ORDER BY l.event_date DESC
    """, params)
    cols = ('event_date', 'order_number', 'phase', 'event_type',
            'material_code', 'unique_number', 'qty_expected', 'qty_actual',
            'operator', 'notes')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def cause_analysis(cursor, date_from=None, date_to=None) -> dict:
    """
    Analisi cause ricorrenti, mappata sulle cause della §1.1:
      #2 Posizionamento sconosciuto  -> MATERIAL_FOUND
      #3 Scrap eccedente             -> REQUEST_MATERIAL fase PREFORMING
      #4 Errore di prelievo WH       -> VERIFY_FAIL fase PREFORMING
      #5 Materiale non trasferito    -> VERIFY_FAIL fase PRODUCTION
      Altro: deroghe, sconosciuti, perso/deteriorato in produzione.
    """
    where, params = ["1=1"], []
    if date_from:
        where.append("event_date >= ?")
        params.append(date_from)
    if date_to:
        where.append("event_date < DATEADD(DAY, 1, ?)")
        params.append(date_to)
    wsql = ' AND '.join(where)

    cursor.execute(f"""
        SELECT event_type, phase, COUNT(*)
        FROM Traceability_RS.dbo.kit_verification_log
        WHERE {wsql}
        GROUP BY event_type, phase
    """, params)
    counts = {(r[0], r[1]): r[2] for r in cursor.fetchall()}

    def c(event, phase=None):
        if phase:
            return counts.get((event, phase), 0)
        return sum(v for (e, _), v in counts.items() if e == event)

    # 'key' = chiave di traduzione (AppTranslations); 'cause' = fallback IT.
    # La GUI risolve l'etichetta con lang.get(key, cause) nella lingua attiva.
    causes = [
        {'key': 'kit_cause_found',
         'cause': '#2 Posizionamento sconosciuto (ritrovati)',
         'count': c('MATERIAL_FOUND')},
        {'key': 'kit_cause_scrap_pf',
         'cause': '#3 Scrap eccedente BOM (richieste da preformatura)',
         'count': c('REQUEST_MATERIAL', 'PREFORMING')},
        {'key': 'kit_cause_pick_error',
         'cause': '#4 Errore di prelievo WH (verifiche fallite ingresso PF)',
         'count': c('VERIFY_FAIL', 'PREFORMING')},
        {'key': 'kit_cause_not_transferred',
         'cause': '#5 Materiale non trasferito (verifiche fallite in linea)',
         'count': c('VERIFY_FAIL', 'PRODUCTION')},
        {'key': 'kit_cause_lost_prod',
         'cause': 'Perso/deteriorato in produzione (richieste da linea)',
         'count': c('REQUEST_MATERIAL', 'PRODUCTION')},
        {'key': 'kit_cause_derogations',
         'cause': 'Chiusure con deroga (prelievi incompleti)',
         'count': c('CLOSE_DEROGATION')},
        {'key': 'kit_cause_unknown_scans',
         'cause': 'Scansioni con unique number sconosciuto',
         'count': c('UNKNOWN_UNIQUE_NUMBER')},
        {'key': 'kit_cause_file_changes',
         'cause': 'Cambi file sorgente in corso d\'opera',
         'count': c('SOURCE_FILE_CHANGED')},
    ]

    # Top materiali piu' richiesti (scrap/mancanze)
    rwhere, rparams = ["1=1"], []
    if date_from:
        rwhere.append("request_date >= ?")
        rparams.append(date_from)
    if date_to:
        rwhere.append("request_date < DATEADD(DAY, 1, ?)")
        rparams.append(date_to)
    cursor.execute(f"""
        SELECT TOP 15 material_code, COUNT(*) AS n_req, SUM(qty_requested) AS tot_qty
        FROM Traceability_RS.dbo.material_requests
        WHERE {' AND '.join(rwhere)}
        GROUP BY material_code
        ORDER BY COUNT(*) DESC, SUM(qty_requested) DESC
    """, rparams)
    top_materials = [{'material_code': r[0], 'n_requests': r[1],
                      'total_qty': float(r[2] or 0)} for r in cursor.fetchall()]

    # Ordini con piu' eccezioni
    cursor.execute(f"""
        SELECT TOP 15 order_number, COUNT(*) AS n
        FROM Traceability_RS.dbo.kit_verification_log
        WHERE {wsql} AND event_type IN ({','.join(f"'{t}'" for t in EXCEPTION_EVENT_TYPES)})
        GROUP BY order_number
        ORDER BY COUNT(*) DESC
    """, params)
    top_orders = [{'order_number': r[0], 'n_exceptions': r[1]}
                  for r in cursor.fetchall()]

    return {'causes': causes, 'top_materials': top_materials,
            'top_orders': top_orders}


def export_exceptions_xlsx(rows: List[dict], path: str) -> None:
    """Esporta lo storico eccezioni in un file Excel."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Eccezioni Kit"
    headers = ['Data', 'Ordine', 'Fase', 'Evento', 'Materiale', 'Unique Nr',
               'Qty attesa', 'Qty effettiva', 'Operatore', 'Note']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for r in rows:
        ws.append([
            r['event_date'].strftime('%d/%m/%Y %H:%M') if r['event_date'] else '',
            r['order_number'], r['phase'], r['event_type'],
            r['material_code'] or '', r['unique_number'] or '',
            float(r['qty_expected']) if r['qty_expected'] is not None else None,
            float(r['qty_actual']) if r['qty_actual'] is not None else None,
            r['operator'], r['notes'] or '',
        ])
    widths = [16, 12, 12, 22, 22, 16, 11, 11, 22, 50]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = w
    wb.save(path)
    logger.info("Export eccezioni: %d righe in %s", len(rows), path)
