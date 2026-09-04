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

def eligible_lists(cursor, date_from=None, date_to=None) -> List[dict]:
    """Kit chiusi dal WH (completamente o con deroga) e pronti per il ricevimento
    in produzione. Include anche kit gia' verificati in preformatura (IN_PREFORMING)
    e bloccati in produzione per ri-verifica. Esclude kit gia' ricevuti
    (RECEIVED_IN_PRODUCTION, COMPLETED) o ancora aperti WH.
    Filtrabili per closed_date della picking list.
    """
    # Diagnostica: conteggio stato kit_status per supporto troubleshooting
    try:
        cursor.execute("""
            SELECT status, COUNT(*) AS cnt
            FROM Traceability_RS.dbo.kit_status
            GROUP BY status
            ORDER BY cnt DESC
        """)
        status_counts = cursor.fetchall()
        logger.info("[KitProd] kit_status counts: %s",
                    [(r[0], r[1]) for r in status_counts])
    except Exception as e:
        logger.warning("[KitProd] diagnostic count failed: %s", e)

    params = []
    date_filter = ""
    if date_from:
        date_filter += " AND pl.closed_date >= ?"
        params.append(date_from)
    if date_to:
        date_filter += " AND pl.closed_date <= ?"
        params.append(date_to)

    cursor.execute(f"""
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
        WHERE ks.status IN ('WH_CLOSED', 'WH_PARTIAL', 'IN_PREFORMING', 'BLOCKED_MISSING_MATERIAL')
          {date_filter}
        GROUP BY pl.id, pl.source_file_name, pl.status, pl.closed_date
        ORDER BY pl.closed_date DESC
    """, tuple(params))
    cols = ('id', 'file_name', 'status', 'closed_date', 'orders', 'prio_rank', 'blocked')
    rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
    logger.info("[KitProd] eligible_lists returned %d rows", len(rows))
    return rows


# ───────────────────── Righe da verificare in linea ───────────────────── #

def get_prod_items(cursor, list_id: int) -> List[dict]:
    """Righe del kit aggregate per codice materiale.

    La quantita' attesa e' la somma di quanto prelevato WH / preso in carico
    PF per quel materiale. La quantita' ricevuta e' la somma dei check PROD
    gia' registrati. Si mostrano accettati e mancanti per consentire ricezioni
    parziali.
    """
    cursor.execute("""
        WITH ig AS (
            SELECT i.material_code,
                   SUM(ISNULL(cpf.qty_actual, i.qty_picked)) AS qty_expected,
                   MIN(i.id) AS representative_item_id
            FROM Traceability_RS.dbo.picking_list_items i
            LEFT JOIN Traceability_RS.dbo.kit_item_checks cpf
                   ON cpf.item_id = i.id AND cpf.phase = 'PREFORMING'
            WHERE i.picking_list_id = ? AND i.qty_picked > 0
              AND i.pick_status NOT IN (?, ?)
            GROUP BY i.material_code
        )
        SELECT ig.representative_item_id,
               ig.material_code,
               ig.qty_expected,
               ISNULL(SUM(cp.qty_actual), 0) AS qty_received,
               CASE
                   WHEN ISNULL(SUM(cp.qty_actual), 0) >= ig.qty_expected THEN 'OK'
                   WHEN ISNULL(SUM(cp.qty_actual), 0) > 0 THEN 'MISMATCH'
                   ELSE NULL
               END AS check_status
        FROM ig
        LEFT JOIN Traceability_RS.dbo.picking_list_items i2
               ON i2.picking_list_id = ? AND i2.material_code = ig.material_code
        LEFT JOIN Traceability_RS.dbo.kit_item_checks cp
               ON cp.item_id = i2.id AND cp.phase = ?
        WHERE i2.qty_picked > 0 AND i2.pick_status NOT IN (?, ?)
        GROUP BY ig.representative_item_id, ig.material_code, ig.qty_expected
        ORDER BY CASE WHEN ISNULL(SUM(cp.qty_actual), 0) >= ig.qty_expected THEN 2
                      WHEN ISNULL(SUM(cp.qty_actual), 0) > 0 THEN 1 ELSE 0 END,
                 ig.material_code
    """, (list_id, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED,
          list_id, PHASE_PROD, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    cols = ('item_id', 'material_code', 'qty_expected',
            'qty_received', 'check_status')
    rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
    for r in rows:
        r['qty_missing'] = max(
            float(r['qty_expected'] or 0) - float(r['qty_received'] or 0), 0)
    return rows


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

def apply_prod_check(cursor, list_id: int, material_code: str, qty_received: float,
                     operator_id: int, session_id: int) -> Tuple[str, Optional[dict]]:
    """Verifica un materiale al ricevimento in linea ('ok'/'mismatch'/'not_found').

    La verifica avviene per codice materiale (non per HU), accumulando le
    quantita' ricevute anche parzialmente. Tutti i check PROD del materiale
    vengono consolidati su una sola riga rappresentativa.
    """
    info = whl.get_list_info(cursor, list_id)
    lbl = whl.orders_label(info['orders'])

    cursor.execute("""
        WITH ig AS (
            SELECT material_code,
                   SUM(ISNULL(cpf.qty_actual, qty_picked)) AS qty_expected,
                   MIN(id) AS representative_item_id,
                   MAX(i.order_number) AS order_number
            FROM Traceability_RS.dbo.picking_list_items i
            LEFT JOIN Traceability_RS.dbo.kit_item_checks cpf
                   ON cpf.item_id = i.id AND cpf.phase = 'PREFORMING'
            WHERE i.picking_list_id = ? AND i.material_code = ?
              AND i.qty_picked > 0 AND i.pick_status NOT IN (?, ?)
            GROUP BY i.material_code
        )
        SELECT representative_item_id, qty_expected, order_number FROM ig
    """, (list_id, material_code, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    r = cursor.fetchone()
    if r is None:
        whl.log_event(cursor, lbl, 'UNKNOWN_MATERIAL', phase=PHASE_PROD,
                      material_code=material_code, qty_actual=qty_received,
                      operator_id=operator_id, notes=f"list={list_id}")
        whl.touch_session(cursor, session_id)
        return 'not_found', None

    item_id, qty_expected, order_number = r
    qty_expected = float(qty_expected)

    cursor.execute("""
        SELECT ISNULL(SUM(cp.qty_actual), 0)
        FROM Traceability_RS.dbo.picking_list_items i
        LEFT JOIN Traceability_RS.dbo.kit_item_checks cp
               ON cp.item_id = i.id AND cp.phase = ?
        WHERE i.picking_list_id = ? AND i.material_code = ?
          AND i.qty_picked > 0 AND i.pick_status NOT IN (?, ?)
    """, (PHASE_PROD, list_id, material_code,
          whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    qty_received_total = float(cursor.fetchone()[0]) + float(qty_received)
    status = CHECK_OK if qty_received_total >= qty_expected else CHECK_MISMATCH

    # Consolidamento: un unico check per materiale sulla riga rappresentativa.
    cursor.execute("""
        DELETE FROM Traceability_RS.dbo.kit_item_checks
        WHERE phase = ? AND item_id IN (
            SELECT id FROM Traceability_RS.dbo.picking_list_items
            WHERE picking_list_id = ? AND material_code = ?
        )
    """, (PHASE_PROD, list_id, material_code))

    cursor.execute("""
        INSERT INTO Traceability_RS.dbo.kit_item_checks
            (item_id, phase, qty_expected, qty_actual, check_status, checked_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item_id, PHASE_PROD, qty_expected, qty_received_total,
          status, operator_id))

    whl.log_event(cursor, order_number or lbl, 'SCAN', phase=PHASE_PROD,
                  material_code=material_code, qty_expected=qty_expected,
                  qty_actual=qty_received_total, operator_id=operator_id,
                  notes=f"list={list_id}; check={status}; added={qty_received}")
    whl.touch_session(cursor, session_id)
    return ('ok' if status == CHECK_OK else 'mismatch'), {
        'item_id': item_id, 'material_code': material_code,
        'qty_expected': qty_expected, 'qty_received': qty_received_total,
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
