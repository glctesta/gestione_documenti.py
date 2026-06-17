# -*- coding: utf-8 -*-
"""
sync_service.py — Ricalcolo periodico (5 min) dello snapshot Kit Dashboard.

Sorgente: DB Traceability_RS + file di pianificazione T:\\Planning (fase PTHM).
Output: tabelle kit_dashboard_snapshot, kit_dashboard_snapshot_missing,
        kit_dashboard_history (upsert).

NB: gli item di prelievo sono legati alla LISTA (picking_list_id), non
all'ordine (picking_list_items.order_number è NULL). L'avanzamento si calcola
per lista e si attribuisce a ciascun ordine della lista (picking_list_orders).
"""
import logging
from datetime import datetime, timedelta

import fai_autocheck as fa
from . import eta as eta_mod
from . import planning as planning_mod

logger = logging.getLogger("KitDashboard")

MISSING_STATUSES = ('PENDING', 'PARTIAL', 'MISSING_FROM_LIST', 'PENDING_COMPLETION')
ALERT_STATUSES = ('REOPENED', 'BLOCKED_MISSING_MATERIAL')

# kit_status -> fase logica per la dashboard
PHASE_OF_STATUS = {
    'WH_OPEN': 'WH', 'WH_PARTIAL': 'WH', 'WH_CLOSED': 'WH', 'REOPENED': 'WH',
    'IN_PREFORMING': 'PREFORMING',
    'BLOCKED_MISSING_MATERIAL': 'PRODUCTION',
    'RECEIVED_IN_PRODUCTION': 'DONE', 'COMPLETED': 'DONE',
}

_MAIN_QUERY = """
SELECT ks.order_number, ks.status, ks.updated_date,
       ISNULL(op.priority, 0) AS priority,
       pl.id AS list_id, pl.status AS list_status, pl.upload_date,
       ses.phase AS session_phase, ses.session_status,
       ses.started_date, ses.last_activity_date,
       ISNULL(it.items_total, 0)  AS items_total,
       ISNULL(it.items_done, 0)   AS items_done,
       ISNULL(it.missing_codes, 0) AS missing_codes,
       (SELECT COUNT(*) FROM Traceability_RS.dbo.material_requests r
        WHERE r.order_number = ks.order_number
          AND r.wh_status = 'PENDING' AND r.resolution IS NULL) AS open_requests,
       prod.ProductCode, ord.OrderQuantity
FROM Traceability_RS.dbo.kit_status ks
LEFT JOIN Traceability_RS.dbo.order_priority op ON op.order_number = ks.order_number
OUTER APPLY (
    SELECT TOP 1 pl2.id, pl2.status, pl2.upload_date
    FROM Traceability_RS.dbo.picking_list_orders plo
    JOIN Traceability_RS.dbo.picking_lists pl2 ON pl2.id = plo.picking_list_id
    WHERE plo.order_number = ks.order_number
    ORDER BY pl2.upload_date DESC
) pl(id, status, upload_date)
OUTER APPLY (
    SELECT TOP 1 s.phase, s.status AS session_status, s.started_date, s.last_activity_date
    FROM Traceability_RS.dbo.kit_sessions s
    WHERE s.picking_list_id = pl.id AND s.status IN ('ACTIVE', 'SUSPENDED')
    ORDER BY s.started_date DESC
) ses(phase, session_status, started_date, last_activity_date)
OUTER APPLY (
    SELECT COUNT(*) AS items_total,
           SUM(CASE WHEN i.pick_status = 'COMPLETE' THEN 1 ELSE 0 END) AS items_done,
           COUNT(DISTINCT CASE WHEN i.pick_status IN ('PENDING','PARTIAL','MISSING_FROM_LIST','PENDING_COMPLETION')
                                AND i.qty_picked < i.qty_required THEN i.material_code END) AS missing_codes
    FROM Traceability_RS.dbo.picking_list_items i
    WHERE i.picking_list_id = pl.id
) it(items_total, items_done, missing_codes)
OUTER APPLY (
    SELECT TOP 1 O.OrderQuantity, O.IDProduct
    FROM Traceability_RS.dbo.Orders O WHERE O.OrderNumber = ks.order_number
) ord(OrderQuantity, IDProduct)
OUTER APPLY (
    SELECT TOP 1 P.ProductCode FROM Traceability_RS.dbo.Products P
    WHERE P.IDProduct = ord.IDProduct
) prod(ProductCode)
"""


class KitDashboardSync:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.pthm_phase_id = int(cfg.get('pthm_phase_id', 4))
        self.pthm_phase_name = cfg.get('pthm_phase_name', 'PTHM')
        self.planning_path = cfg.get('planning_path') or None
        self.fallback_min = float(cfg.get('eta_fallback_minutes_per_item', 1.5))

    # ------------------------------------------------------------------ #
    def run_once(self, conn) -> dict:
        """Ricalcola e riscrive lo snapshot. Ritorna un riepilogo."""
        now = datetime.now()
        cur = conn.cursor()

        planned = planning_mod.pthm_planned_starts(self.pthm_phase_name, self.planning_path)
        avg_item = eta_mod.avg_minutes_per_item(cur, fallback=self.fallback_min)
        avg_req = eta_mod.avg_request_confirm_minutes(cur)

        cur.execute(_MAIN_QUERY)
        cols = [d[0] for d in cur.description]
        raw = [dict(zip(cols, r)) for r in cur.fetchall()]

        snapshot_rows, history_ops, missing_lists = [], [], {}
        for o in raw:
            order = o['order_number']
            status = o['status']
            phase = PHASE_OF_STATUS.get(status, 'WH')
            items_total = int(o['items_total'] or 0)
            items_done = int(o['items_done'] or 0)
            missing_codes = int(o['missing_codes'] or 0)
            open_requests = int(o['open_requests'] or 0)
            pct = round(items_done * 100.0 / items_total, 2) if items_total else 0.0

            is_ready = (status == 'IN_PREFORMING') and open_requests == 0
            is_incomplete = (status in ALERT_STATUSES) or (missing_codes > 0) \
                or (o['list_status'] == 'PARTIAL')

            remaining = max(0, items_total - items_done)
            if is_ready or phase in ('PREFORMING', 'PRODUCTION', 'DONE'):
                eta_min = 0
            else:
                eta_min = eta_mod.estimate_minutes(remaining, avg_item, open_requests, avg_req)
            eta_ready_at = now + timedelta(minutes=eta_min)

            planned_start = planned.get(order)
            is_late = False
            if status in ALERT_STATUSES:
                is_late = True
            elif planned_start and not is_ready:
                pthm_started = fa.check_production_started(conn, order, self.pthm_phase_id) > 0
                if not pthm_started and (now > planned_start or eta_ready_at > planned_start):
                    is_late = True

            if status != 'RECEIVED_IN_PRODUCTION':
                snapshot_rows.append({
                    'order_number': order, 'product_code': o.get('ProductCode'),
                    'order_qty': o.get('OrderQuantity'), 'priority': int(o['priority'] or 0),
                    'kit_status': status, 'phase': phase,
                    'items_total': items_total, 'items_done': items_done,
                    'pct_complete': pct, 'missing_codes': missing_codes,
                    'open_requests': open_requests,
                    'is_ready_for_prod': 1 if is_ready else 0,
                    'is_late': 1 if is_late else 0,
                    'is_incomplete': 1 if is_incomplete else 0,
                    'eta_minutes': eta_min if not is_ready else 0,
                    'eta_ready_at': eta_ready_at if (eta_min and not is_ready) else None,
                    'planned_start': planned_start,
                    'list_id': o['list_id'], 'started_date': o['started_date'],
                    'last_activity_date': o['last_activity_date'],
                })
                if o['list_id'] and missing_codes > 0:
                    missing_lists.setdefault(o['list_id'], []).append(order)

            history_ops.append({
                'order': order, 'product_code': o.get('ProductCode'),
                'planned_start': planned_start, 'status': status,
                'is_complete': (items_total > 0 and items_done >= items_total
                                and o['list_status'] != 'PARTIAL' and missing_codes == 0),
            })

        self._write_snapshot(cur, snapshot_rows, now)
        self._write_missing(cur, missing_lists, now)
        self._upsert_history(cur, history_ops, now)
        conn.commit()

        summary = {
            'orders': len(snapshot_rows),
            'ready': sum(1 for r in snapshot_rows if r['is_ready_for_prod']),
            'late': sum(1 for r in snapshot_rows if r['is_late']),
            'avg_item_min': round(avg_item, 2),
            'snapshot_date': now,
        }
        logger.info("KitDashboardSync: %s", summary)
        return summary

    # ------------------------------------------------------------------ #
    def _write_snapshot(self, cur, rows, now):
        cur.execute("DELETE FROM Traceability_RS.dbo.kit_dashboard_snapshot")
        if not rows:
            return
        cur.fast_executemany = True
        cur.executemany("""
            INSERT INTO Traceability_RS.dbo.kit_dashboard_snapshot
                (order_number, product_code, order_qty, priority, kit_status, phase,
                 items_total, items_done, pct_complete, missing_codes, open_requests,
                 is_ready_for_prod, is_late, is_incomplete, eta_minutes, eta_ready_at,
                 planned_start, list_id, started_date, last_activity_date, snapshot_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [(
            r['order_number'], r['product_code'], r['order_qty'], r['priority'],
            r['kit_status'], r['phase'], r['items_total'], r['items_done'],
            r['pct_complete'], r['missing_codes'], r['open_requests'],
            r['is_ready_for_prod'], r['is_late'], r['is_incomplete'],
            r['eta_minutes'], r['eta_ready_at'], r['planned_start'], r['list_id'],
            r['started_date'], r['last_activity_date'], now,
        ) for r in rows])

    def _write_missing(self, cur, missing_lists, now):
        cur.execute("DELETE FROM Traceability_RS.dbo.kit_dashboard_snapshot_missing")
        if not missing_lists:
            return
        out = []
        for list_id, orders in missing_lists.items():
            cur.execute("""
                SELECT material_code,
                       SUM(qty_required) AS qty_required,
                       SUM(qty_picked)   AS qty_picked,
                       MAX(pick_status)  AS pick_status
                FROM Traceability_RS.dbo.picking_list_items
                WHERE picking_list_id = ?
                  AND pick_status IN ('PENDING','PARTIAL','MISSING_FROM_LIST','PENDING_COMPLETION')
                  AND qty_picked < qty_required
                GROUP BY material_code
            """, (list_id,))
            items = cur.fetchall()
            for order in orders:
                for m in items:
                    req = float(m[1] or 0); pk = float(m[2] or 0)
                    out.append((order, m[0], req, pk, max(0.0, req - pk), m[3], now))
        if out:
            cur.fast_executemany = True
            cur.executemany("""
                INSERT INTO Traceability_RS.dbo.kit_dashboard_snapshot_missing
                    (order_number, material_code, qty_required, qty_picked,
                     qty_missing, pick_status, snapshot_date)
                VALUES (?,?,?,?,?,?,?)
            """, out)

    def _upsert_history(self, cur, ops, now):
        for h in ops:
            ready = h['status'] in ('IN_PREFORMING', 'RECEIVED_IN_PRODUCTION', 'COMPLETED')
            completed = h['status'] in ('RECEIVED_IN_PRODUCTION', 'COMPLETED')
            cur.execute("""
                MERGE Traceability_RS.dbo.kit_dashboard_history AS t
                USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
                WHEN MATCHED THEN UPDATE SET
                    product_code = ?,
                    planned_start = ?,
                    ready_date = CASE WHEN t.ready_date IS NULL AND ? = 1 THEN ? ELSE t.ready_date END,
                    completed_date = CASE WHEN t.completed_date IS NULL AND ? = 1 THEN ? ELSE t.completed_date END,
                    was_complete = CASE WHEN ? = 1 THEN ? ELSE t.was_complete END,
                    was_on_time = CASE
                        WHEN ? = 1 AND ? IS NOT NULL THEN
                            CASE WHEN ISNULL(t.ready_date, ?) <= ? THEN 1 ELSE 0 END
                        ELSE t.was_on_time END,
                    final_status = ?,
                    updated_date = ?
                WHEN NOT MATCHED THEN INSERT
                    (order_number, product_code, planned_start, first_seen_date,
                     ready_date, completed_date, was_complete, was_on_time,
                     final_status, updated_date)
                    VALUES (?, ?, ?, ?,
                            CASE WHEN ? = 1 THEN ? ELSE NULL END,
                            CASE WHEN ? = 1 THEN ? ELSE NULL END,
                            CASE WHEN ? = 1 THEN ? ELSE NULL END,
                            NULL, ?, ?);
            """, (
                h['order'],
                # UPDATE
                h['product_code'], h['planned_start'],
                1 if ready else 0, now,
                1 if completed else 0, now,
                1 if completed else 0, 1 if h['is_complete'] else 0,
                1 if ready else 0, h['planned_start'], now, h['planned_start'],
                h['status'], now,
                # INSERT
                h['order'], h['product_code'], h['planned_start'], now,
                1 if ready else 0, now,
                1 if completed else 0, now,
                1 if completed else 0, (1 if h['is_complete'] else 0),
                h['status'], now,
            ))


def run_sync(conn=None) -> dict:
    """Helper standalone: apre la connessione se non fornita."""
    from . import server_config
    cfg = server_config.load_config()
    own_conn = False
    if conn is None:
        import pyodbc
        from config_manager import ConfigManager
        c = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
        conn = pyodbc.connect(
            f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
            f"UID={c['username']};PWD={c['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
        )
        own_conn = True
    try:
        return KitDashboardSync(cfg).run_once(conn)
    finally:
        if own_conn:
            conn.close()


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print(run_sync())
