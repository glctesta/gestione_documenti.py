# -*- coding: utf-8 -*-
"""
web_data.py — Accesso dati (sola lettura) per il web server Kit Dashboard.

Legge dallo SNAPSHOT (riscritto ogni 5 min dal sync) e dallo STORICO.
"""
import logging

logger = logging.getLogger("KitDashboard")

_SNAP_COLS = ('order_number', 'product_code', 'order_qty', 'priority', 'kit_status',
              'phase', 'items_total', 'items_done', 'pct_complete', 'missing_codes',
              'open_requests', 'is_ready_for_prod', 'is_late', 'is_incomplete',
              'eta_minutes', 'eta_ready_at', 'planned_start', 'list_id',
              'started_date', 'last_activity_date', 'snapshot_date')

_SNAP_SELECT = "SELECT " + ", ".join(_SNAP_COLS) + " FROM Traceability_RS.dbo.kit_dashboard_snapshot"


def _rows(cur):
    return [dict(zip(_SNAP_COLS, r)) for r in cur.fetchall()]


def _active_postponements(cur):
    """Restituisce dict order_number -> info posticipo attivo (expires_at > GETDATE()).
    Se la tabella non esiste ancora, logga un warning e continua senza posticipi."""
    out = {}
    try:
        cur.execute("""
            SELECT order_number, reason_code, reason_label, reason_text,
                   days, postponed_by, postponed_at, expires_at
            FROM Traceability_RS.dbo.kit_order_postponements
            WHERE expires_at > GETDATE()
        """)
        for r in cur.fetchall():
            out[str(r[0]).strip()] = {
                'postponed_days': int(r[4] or 0),
                'postponed_until': r[7],
                'postponed_by': r[5],
                'postponed_reason_label': r[2],
                'postponed_reason_text': r[3],
            }
    except Exception as e:
        logger.warning("kit_order_postponements non leggibile (%s); proseguo senza posticipi.", e)
    return out


def _apply_postponements(rows, postponements):
    """Applica i posticipi attivi: non lampeggia; aggiunge campi postponed_*"""
    for r in rows:
        p = postponements.get(r['order_number'])
        if p:
            r.update(p)
            r['is_late'] = 0
    return rows


def snapshot_date(cur):
    cur.execute("SELECT MAX(snapshot_date) FROM Traceability_RS.dbo.kit_dashboard_snapshot")
    r = cur.fetchone()
    return r[0] if r else None


def warehouse_rows(cur):
    """Ordini in preparazione (lato magazzino), ordinati per priorità poi ETA."""
    cur.execute(_SNAP_SELECT + """
        WHERE phase IN ('WH','PREFORMING')
        ORDER BY CASE WHEN priority = 0 THEN 4 ELSE priority END ASC,
                 is_late DESC, eta_minutes DESC, order_number
    """)
    return _rows(cur)


def production_ready(cur):
    cur.execute(_SNAP_SELECT + """
        WHERE is_ready_for_prod = 1
          AND kit_status <> 'RECEIVED_IN_PRODUCTION'
        ORDER BY CASE WHEN priority = 0 THEN 4 ELSE priority END ASC, order_number
    """)
    rows = _rows(cur)
    post = _active_postponements(cur)
    return _apply_postponements(rows, post)


def production_next(cur):
    """Ordini non ancora pronti (esclusi quelli già ricevuti in produzione), ordinati per data pianificata / ETA."""
    cur.execute(_SNAP_SELECT + """
        WHERE is_ready_for_prod = 0
          AND phase <> 'DONE'
          AND kit_status <> 'RECEIVED_IN_PRODUCTION'
        ORDER BY is_late DESC,
                 CASE WHEN planned_start IS NULL THEN 1 ELSE 0 END,
                 planned_start ASC, eta_minutes ASC, order_number
    """)
    rows = _rows(cur)
    post = _active_postponements(cur)
    return _apply_postponements(rows, post)


def production_received(cur):
    """Ordini già confermati (ricevuti) in produzione, con nome dell'operatore."""
    cur.execute("""
        SELECT ks.order_number,
               ks.updated_date AS received_date,
               e.EmployeeName + ' ' + e.EmployeeSurname AS user_name
        FROM Traceability_RS.dbo.kit_status ks
        LEFT JOIN Employee.dbo.EmployeeHireHistory h
               ON h.EmployeeHireHistoryId = ks.updated_by
        LEFT JOIN Employee.dbo.employees e
               ON e.EmployeeId = h.EmployeeId
        WHERE ks.status = 'RECEIVED_IN_PRODUCTION'
        ORDER BY ks.updated_date DESC
    """)
    cols = ('order_number', 'received_date', 'user_name')
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def postponed_orders(cur):
    """Ordini con posticipo attivo (expires_at > GETDATE())."""
    try:
        cur.execute("""
            SELECT p.order_number,
                   prod.ProductCode AS product_code,
                   p.reason_code,
                   p.reason_label,
                   p.reason_text,
                   p.days,
                   p.postponed_by,
                   p.postponed_at,
                   p.expires_at
            FROM Traceability_RS.dbo.kit_order_postponements p
            LEFT JOIN Traceability_RS.dbo.Orders o ON o.OrderNumber = p.order_number
            LEFT JOIN Traceability_RS.dbo.Products prod ON prod.IDProduct = o.IDProduct
            WHERE p.expires_at > GETDATE()
            ORDER BY p.expires_at ASC
        """)
        cols = ('order_number', 'product_code', 'reason_code', 'reason_label',
                'reason_text', 'days', 'postponed_by', 'postponed_at', 'expires_at')
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception as e:
        logger.warning("kit_order_postponements non leggibile (%s); proseguo senza posticipi.", e)
        return []


_HIST_COLS = ('order_number', 'product_code', 'planned_start', 'ready_date',
              'completed_date', 'was_on_time', 'was_complete', 'final_status', 'updated_date')


def history_rows(cur, days: int = 3, search: str = ''):
    """Storico esiti: default ultimi N giorni; con search ignora il limite giorni."""
    params, where = [], []
    if search:
        where.append("(order_number LIKE ? OR product_code LIKE ?)")
        params += [f"%{search}%", f"%{search}%"]
    else:
        where.append("updated_date >= DATEADD(DAY, -?, GETDATE())")
        params.append(int(days))
    cur.execute("SELECT " + ", ".join(_HIST_COLS) +
                " FROM Traceability_RS.dbo.kit_dashboard_history WHERE " +
                " AND ".join(where) +
                " ORDER BY ISNULL(completed_date, updated_date) DESC", params)
    return [dict(zip(_HIST_COLS, r)) for r in cur.fetchall()]


def order_detail(cur, order_number: str):
    """Snapshot dell'ordine + materiali mancanti + richieste aperte."""
    cur.execute(_SNAP_SELECT + " WHERE order_number = ?", (order_number,))
    rows = _rows(cur)
    snap = rows[0] if rows else None

    cur.execute("""
        SELECT material_code, qty_required, qty_picked, qty_missing, pick_status
        FROM Traceability_RS.dbo.kit_dashboard_snapshot_missing
        WHERE order_number = ? ORDER BY material_code
    """, (order_number,))
    missing = [dict(zip(('material_code', 'qty_required', 'qty_picked',
                         'qty_missing', 'pick_status'), r)) for r in cur.fetchall()]

    cur.execute("""
        SELECT material_code, qty_requested, requesting_phase, wh_status,
               request_date, note
        FROM Traceability_RS.dbo.material_requests
        WHERE order_number = ? AND resolution IS NULL
        ORDER BY request_date DESC
    """, (order_number,))
    requests = [dict(zip(('material_code', 'qty_requested', 'requesting_phase',
                          'wh_status', 'request_date', 'note'), r)) for r in cur.fetchall()]

    # Lista COMPLETA dei materiali PTH dell'ordine (lista di prelievo più recente),
    # in ordine alfabetico. Esclusi reel vuoto e componenti SMT (solo PTH).
    # HU = reel, Codice = material_code, Descrizione = dbo.Components,
    # qtà prelevata = qty_picked, qtà verificata = qty_picked se pick_status='COMPLETE'.
    cur.execute("""
        SELECT i.material_code, i.unique_number, c.ComponentDescription AS descr,
               i.qty_required, i.qty_picked, i.pick_status
        FROM Traceability_RS.dbo.picking_list_items i
        LEFT JOIN Traceability_RS.dbo.Components c ON c.ComponentCode = i.material_code
        WHERE i.picking_list_id = (
                SELECT TOP 1 pl.id
                FROM Traceability_RS.dbo.picking_list_orders plo
                JOIN Traceability_RS.dbo.picking_lists pl ON pl.id = plo.picking_list_id
                WHERE plo.order_number = ? ORDER BY pl.upload_date DESC)
          AND i.unique_number IS NOT NULL AND LTRIM(RTRIM(i.unique_number)) <> ''
          AND NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.Components c2
                          WHERE c2.ComponentCode = i.material_code
                            AND c2.ComponentDescription LIKE '%SMT%')
        ORDER BY i.material_code, i.unique_number
    """, (order_number,))
    materials = []
    for r in cur.fetchall():
        picked = float(r[4] or 0)
        materials.append({
            'material_code': r[0], 'hu': r[1], 'descr': r[2] or '',
            'qty_required': float(r[3] or 0), 'qty_picked': picked,
            'qty_verified': picked if r[5] == 'COMPLETE' else 0.0,
            'pick_status': r[5],
        })

    # se non in snapshot, prova lo storico (ordine già completato)
    hist = None
    if not snap:
        cur.execute("SELECT " + ", ".join(_HIST_COLS) +
                    " FROM Traceability_RS.dbo.kit_dashboard_history WHERE order_number = ?",
                    (order_number,))
        h = cur.fetchone()
        if h:
            hist = dict(zip(_HIST_COLS, h))

    return {'snap': snap, 'missing': missing, 'requests': requests,
            'materials': materials, 'history': hist}
