"""
kit_prod_logic.py
Logica DB della Fase 3 (Ricezione e Verifica in Produzione) — Sprint 4
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.3, §9.3).

Come le altre fasi: funzioni su cursor pyodbc, nessun commit interno;
email inviate dal chiamante DOPO il commit, popup accodati in transazione.

La quantita' attesa in produzione e' quella PRESA IN CARICO dalla
preformatura (kit_item_checks fase PREFORMING); fallback qty_picked WH.
"""
import logging
from typing import List, Optional, Tuple

import kit_wh_logic as whl
import kit_notifications as notif

logger = logging.getLogger("PlanMonitor")

PHASE_PROD = 'PRODUCTION'

CHECK_OK = 'OK'
CHECK_MISMATCH = 'MISMATCH'


# ───────────────────────── Liste eleggibili ───────────────────────────── #

def eligible_lists(cursor) -> List[dict]:
    """Kit presi in carico dalla preformatura (o bloccati, per ri-verifica),
    ordinati per priorita' poi data."""
    cursor.execute("""
        SELECT pl.id, pl.source_file_name, pl.status, pl.closed_date,
               STUFF((SELECT '/' + plo.order_number
                      FROM Traceability_RS.dbo.picking_list_orders plo
                      WHERE plo.picking_list_id = pl.id
                      FOR XML PATH('')), 1, 1, '') AS orders,
               MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) AS prio_rank,
               MAX(CASE WHEN ks.status = 'BLOCKED_MISSING_MATERIAL' THEN 1 ELSE 0 END) AS blocked
        FROM Traceability_RS.dbo.picking_lists pl
        INNER JOIN Traceability_RS.dbo.picking_list_orders plo2
                ON plo2.picking_list_id = pl.id
        INNER JOIN Traceability_RS.dbo.kit_status ks
                ON ks.order_number = plo2.order_number
        LEFT JOIN Traceability_RS.dbo.order_priority op
               ON op.order_number = plo2.order_number
        WHERE ks.status IN ('IN_PREFORMING', 'BLOCKED_MISSING_MATERIAL')
        GROUP BY pl.id, pl.source_file_name, pl.status, pl.closed_date
        ORDER BY MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) ASC,
                 pl.closed_date ASC
    """)
    cols = ('id', 'file_name', 'status', 'closed_date', 'orders', 'prio_rank', 'blocked')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


# ───────────────────── Righe da verificare in linea ───────────────────── #

def get_prod_items(cursor, list_id: int) -> List[dict]:
    """Righe del kit con quantita' attesa (= presa in carico preformatura)
    ed esito verifica produzione."""
    cursor.execute("""
        SELECT i.id, i.material_code, i.unique_number,
               ISNULL(cpf.qty_actual, i.qty_picked) AS qty_expected,
               cp.qty_actual, cp.check_status
        FROM Traceability_RS.dbo.picking_list_items i
        LEFT JOIN Traceability_RS.dbo.kit_item_checks cpf
               ON cpf.item_id = i.id AND cpf.phase = 'PREFORMING'
        LEFT JOIN Traceability_RS.dbo.kit_item_checks cp
               ON cp.item_id = i.id AND cp.phase = ?
        WHERE i.picking_list_id = ?
          AND i.qty_picked > 0
          AND i.pick_status NOT IN (?, ?)
        ORDER BY CASE WHEN cp.check_status IS NULL THEN 0
                      WHEN cp.check_status = 'MISMATCH' THEN 1 ELSE 2 END,
                 i.material_code
    """, (PHASE_PROD, list_id, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    cols = ('item_id', 'material_code', 'unique_number', 'qty_expected',
            'qty_received', 'check_status')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def prod_state(cursor, list_id: int) -> dict:
    items = get_prod_items(cursor, list_id)
    total = len(items)
    ok = sum(1 for i in items if i['check_status'] == CHECK_OK)
    mismatch = sum(1 for i in items if i['check_status'] == CHECK_MISMATCH)
    return {'total': total, 'ok': ok, 'mismatch': mismatch,
            'unchecked': total - ok - mismatch,
            'all_ok': total > 0 and ok == total,
            'has_mismatch': mismatch > 0}


# ───────────────────────── Scansione ricevimento ──────────────────────── #

def apply_prod_check(cursor, list_id: int, unique_number: str, qty_received: float,
                     operator_id: int, session_id: int) -> Tuple[str, Optional[dict]]:
    """Verifica una scatola al ricevimento in linea ('ok'/'mismatch'/'not_found')."""
    info = whl.get_list_info(cursor, list_id)
    lbl = whl.orders_label(info['orders'])

    cursor.execute("""
        SELECT i.id, i.material_code,
               ISNULL(cpf.qty_actual, i.qty_picked) AS qty_expected,
               i.order_number
        FROM Traceability_RS.dbo.picking_list_items i
        LEFT JOIN Traceability_RS.dbo.kit_item_checks cpf
               ON cpf.item_id = i.id AND cpf.phase = 'PREFORMING'
        WHERE i.picking_list_id = ? AND i.unique_number = ?
          AND i.qty_picked > 0 AND i.pick_status NOT IN (?, ?)
    """, (list_id, unique_number, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    r = cursor.fetchone()
    if r is None:
        whl.log_event(cursor, lbl, 'UNKNOWN_UNIQUE_NUMBER', phase=PHASE_PROD,
                      unique_number=unique_number, qty_actual=qty_received,
                      operator_id=operator_id, notes=f"list={list_id}")
        whl.touch_session(cursor, session_id)
        return 'not_found', None

    item_id, material_code, qty_expected, order_number = r
    qty_received = float(qty_received)
    qty_expected = float(qty_expected)
    status = CHECK_OK if qty_received == qty_expected else CHECK_MISMATCH

    cursor.execute("""
        MERGE Traceability_RS.dbo.kit_item_checks AS t
        USING (SELECT ? AS item_id, ? AS phase) AS s
            ON t.item_id = s.item_id AND t.phase = s.phase
        WHEN MATCHED THEN
            UPDATE SET qty_expected=?, qty_actual=?, check_status=?,
                       checked_by=?, checked_date=GETDATE()
        WHEN NOT MATCHED THEN
            INSERT (item_id, phase, qty_expected, qty_actual, check_status, checked_by)
            VALUES (s.item_id, s.phase, ?, ?, ?, ?);
    """, (item_id, PHASE_PROD,
          qty_expected, qty_received, status, operator_id,
          qty_expected, qty_received, status, operator_id))

    whl.log_event(cursor, order_number or lbl, 'SCAN', phase=PHASE_PROD,
                  material_code=material_code, unique_number=unique_number,
                  qty_expected=qty_expected, qty_actual=qty_received,
                  operator_id=operator_id,
                  notes=f"list={list_id}; check={status}")
    whl.touch_session(cursor, session_id)
    return ('ok' if status == CHECK_OK else 'mismatch'), {
        'item_id': item_id, 'material_code': material_code,
        'qty_expected': qty_expected, 'qty_received': qty_received,
        'check_status': status}


# ───────────────────────── Esiti verifica (§5.3.2) ────────────────────── #

def finalize_prod_ok(cursor, list_id: int, operator_id: int) -> None:
    """Caso A: tutto confermato -> RECEIVED_IN_PRODUCTION, produzione procede."""
    info = whl.get_list_info(cursor, list_id)
    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='RECEIVED_IN_PRODUCTION',
                                         updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'RECEIVED_IN_PRODUCTION', ?);
        """, (order, operator_id, operator_id))
        whl.log_event(cursor, order, 'VERIFY_OK', phase=PHASE_PROD,
                      operator_id=operator_id, notes=f"list={list_id}")
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status='COMPLETED', last_activity_date=GETDATE()
        WHERE picking_list_id=? AND phase=? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_PROD))


def finalize_prod_fail(cursor, list_id: int, operator_id: int) -> dict:
    """
    Caso B: mancanze -> ordini BLOCKED_MISSING_MATERIAL + notifica alla
    preformatura (Email + Popup). Le righe MISMATCH restano ri-verificabili:
    a correzione avvenuta si puo' rifare la verifica e sbloccare con
    finalize_prod_ok. Ritorna i dati per l'email (post-commit).
    """
    info = whl.get_list_info(cursor, list_id)
    lbl = whl.orders_label(info['orders'])

    items = get_prod_items(cursor, list_id)
    bad = [i for i in items if i['check_status'] == CHECK_MISMATCH]
    bad_codes = sorted({f"{i['material_code']} (att. {float(i['qty_expected']):g} / "
                        f"ric. {float(i['qty_received']):g})" for i in bad})

    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='BLOCKED_MISSING_MATERIAL',
                                         updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'BLOCKED_MISSING_MATERIAL', ?);
        """, (order, operator_id, operator_id))
        whl.log_event(cursor, order, 'VERIFY_FAIL', phase=PHASE_PROD,
                      operator_id=operator_id,
                      notes=f"list={list_id}; non_conformi={len(bad)}")

    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status='COMPLETED', last_activity_date=GETDATE()
        WHERE picking_list_id=? AND phase=? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_PROD))

    msgs = notif.verify_fail_prod_messages(lbl, bad_codes)
    notif.queue_popup(cursor, notif.TARGET_KIT_PROD, msgs['popup_title'],
                      msgs['popup_msg'], order_number=lbl)
    return {'messages': msgs, 'bad_codes': bad_codes, 'orders_label': lbl}


# ─────────────── Materiale ritrovato (§5.3.4 / §9.3) ──────────────────── #

def open_requests_for_orders(cursor, orders: List[str]) -> List[dict]:
    """Richieste aperte (PENDING o CONFIRMED) per gli ordini del kit."""
    placeholders = ','.join('?' * len(orders))
    cursor.execute(f"""
        SELECT id, order_number, requesting_phase, material_code,
               qty_requested, wh_status, request_date, note
        FROM Traceability_RS.dbo.material_requests
        WHERE order_number IN ({placeholders}) AND resolution IS NULL
        ORDER BY request_date ASC
    """, orders)
    cols = ('id', 'order_number', 'phase', 'material_code', 'qty',
            'wh_status', 'request_date', 'note')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def mark_material_found(cursor, request_id: int, operator_id: int,
                        note: str) -> dict:
    """
    Flusso 'materiale ritrovato': resolution=FOUND_IN_PRODUCTION, popup al
    WH per evitare il prelievo (gia' gestito da cancel_material_request).
    Ritorna info su eventuale conferma WH gia' avvenuta (§9.3 punto 5).
    """
    cursor.execute("""
        SELECT wh_status FROM Traceability_RS.dbo.material_requests
        WHERE id = ? AND resolution IS NULL
    """, (request_id,))
    r = cursor.fetchone()
    if not r:
        return {'done': False, 'was_confirmed': False}
    was_confirmed = (r[0] == 'CONFIRMED')

    import kit_pf_logic as pfl
    done = pfl.cancel_material_request(cursor, request_id, operator_id,
                                       note, resolution='FOUND_IN_PRODUCTION')
    return {'done': done, 'was_confirmed': was_confirmed}
