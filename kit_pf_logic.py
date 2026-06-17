"""
kit_pf_logic.py
Logica DB della Fase 2 (Presa in Carico Preformatura) — Sprint 3
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.2).

Come kit_wh_logic: funzioni su cursor pyodbc, nessun commit interno.
Le notifiche popup vengono accodate nella stessa transazione; le email
vanno inviate dal chiamante DOPO il commit (kit_notifications).
"""
import logging
from typing import List, Optional, Tuple

import kit_wh_logic as whl
import kit_notifications as notif

logger = logging.getLogger("PlanMonitor")

PHASE_PF = 'PREFORMING'

CHECK_OK = 'OK'
CHECK_MISMATCH = 'MISMATCH'


# ───────────────────────── Liste eleggibili ───────────────────────────── #

def eligible_lists(cursor) -> List[dict]:
    """Liste chiuse dal WH (anche con deroga) con kit non ancora preso in
    carico dalla preformatura, ordinate per priorita' poi data."""
    cursor.execute("""
        SELECT pl.id, pl.source_file_name, pl.status, pl.closed_date,
               STUFF((SELECT '/' + plo.order_number
                      FROM Traceability_RS.dbo.picking_list_orders plo
                      WHERE plo.picking_list_id = pl.id
                      FOR XML PATH('')), 1, 1, '') AS orders,
               MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) AS prio_rank
        FROM Traceability_RS.dbo.picking_lists pl
        INNER JOIN Traceability_RS.dbo.picking_list_orders plo2
                ON plo2.picking_list_id = pl.id
        INNER JOIN Traceability_RS.dbo.kit_status ks
                ON ks.order_number = plo2.order_number
        LEFT JOIN Traceability_RS.dbo.order_priority op
               ON op.order_number = plo2.order_number
        WHERE pl.status IN ('CLOSED', 'PARTIAL')
          AND ks.status IN ('WH_CLOSED', 'WH_PARTIAL')
        GROUP BY pl.id, pl.source_file_name, pl.status, pl.closed_date
        ORDER BY MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) ASC,
                 pl.closed_date ASC
    """)
    cols = ('id', 'file_name', 'status', 'closed_date', 'orders', 'prio_rank')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


# ───────────────── Righe da verificare in ingresso ────────────────────── #

def get_pf_items(cursor, list_id: int) -> List[dict]:
    """Righe consegnate dal WH (qty_picked > 0) con esito verifica PF."""
    cursor.execute("""
        SELECT i.id, i.material_code, i.unique_number, i.qty_picked,
               c.qty_actual, c.check_status
        FROM Traceability_RS.dbo.picking_list_items i
        LEFT JOIN Traceability_RS.dbo.kit_item_checks c
               ON c.item_id = i.id AND c.phase = ?
        WHERE i.picking_list_id = ?
          AND i.qty_picked > 0
          AND i.pick_status NOT IN (?, ?)
        ORDER BY CASE WHEN c.check_status IS NULL THEN 0
                      WHEN c.check_status = 'MISMATCH' THEN 1 ELSE 2 END,
                 i.material_code
    """, (PHASE_PF, list_id, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    cols = ('item_id', 'material_code', 'unique_number', 'qty_picked',
            'qty_received', 'check_status')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def pf_state(cursor, list_id: int) -> dict:
    items = get_pf_items(cursor, list_id)
    total = len(items)
    ok = sum(1 for i in items if i['check_status'] == CHECK_OK)
    mismatch = sum(1 for i in items if i['check_status'] == CHECK_MISMATCH)
    unchecked = total - ok - mismatch
    return {'total': total, 'ok': ok, 'mismatch': mismatch,
            'unchecked': unchecked,
            'all_ok': total > 0 and ok == total,
            'has_mismatch': mismatch > 0}


# ───────────────────────── Scansione ingresso ─────────────────────────── #

def apply_pf_check(cursor, list_id: int, unique_number: str, qty_received: float,
                   operator_id: int, session_id: int) -> Tuple[str, Optional[dict]]:
    """
    Verifica una scatola in ingresso preformatura: confronta la quantita'
    ricevuta con quella chiusa dal WH (qty_picked). Esiti:
      'ok' / 'mismatch' / 'not_found'.
    """
    info = whl.get_list_info(cursor, list_id)
    lbl = whl.orders_label(info['orders'])

    cursor.execute("""
        SELECT id, material_code, qty_picked, order_number
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ? AND unique_number = ?
          AND qty_picked > 0 AND pick_status NOT IN (?, ?)
    """, (list_id, unique_number, whl.ST_MISSING_FROM_LIST, whl.ST_REMOVED))
    r = cursor.fetchone()
    if r is None:
        whl.log_event(cursor, lbl, 'UNKNOWN_UNIQUE_NUMBER', phase=PHASE_PF,
                      unique_number=unique_number, qty_actual=qty_received,
                      operator_id=operator_id, notes=f"list={list_id}")
        whl.touch_session(cursor, session_id)
        return 'not_found', None

    item_id, material_code, qty_picked, order_number = r
    qty_received = float(qty_received)
    qty_picked = float(qty_picked)
    status = CHECK_OK if qty_received == qty_picked else CHECK_MISMATCH

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
    """, (item_id, PHASE_PF,
          qty_picked, qty_received, status, operator_id,
          qty_picked, qty_received, status, operator_id))

    whl.log_event(cursor, order_number or lbl, 'SCAN', phase=PHASE_PF,
                  material_code=material_code, unique_number=unique_number,
                  qty_expected=qty_picked, qty_actual=qty_received,
                  operator_id=operator_id,
                  notes=f"list={list_id}; check={status}")
    whl.touch_session(cursor, session_id)
    return ('ok' if status == CHECK_OK else 'mismatch'), {
        'item_id': item_id, 'material_code': material_code,
        'qty_picked': qty_picked, 'qty_received': qty_received,
        'check_status': status}


# ───────────────────────── Esiti verifica (§5.2.2) ────────────────────── #

def finalize_pf_ok(cursor, list_id: int, operator_id: int) -> None:
    """Caso A: tutto OK -> kit IN_PREFORMING, si sblocca la Fase 3."""
    info = whl.get_list_info(cursor, list_id)
    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='IN_PREFORMING', updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'IN_PREFORMING', ?);
        """, (order, operator_id, operator_id))
        whl.log_event(cursor, order, 'VERIFY_OK', phase=PHASE_PF,
                      operator_id=operator_id, notes=f"list={list_id}")
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status='COMPLETED', last_activity_date=GETDATE()
        WHERE picking_list_id=? AND phase=? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_PF))


def finalize_pf_fail(cursor, list_id: int, operator_id: int) -> dict:
    """
    Caso B: discrepanze -> lista WH riaperta (REOPENED), righe non conformi
    tornano da verificare al WH, popup accodato per la postazione WH.
    Ritorna i dati per l'email (da inviare dopo il commit).
    """
    info = whl.get_list_info(cursor, list_id)
    lbl = whl.orders_label(info['orders'])

    items = get_pf_items(cursor, list_id)
    bad = [i for i in items if i['check_status'] == CHECK_MISMATCH]
    bad_codes = sorted({f"{i['material_code']} (att. {i['qty_picked']:g} / "
                        f"ric. {float(i['qty_received']):g})" for i in bad})

    # Righe non conformi -> tornano PENDING per la ri-verifica WH (§5.2.2)
    for i in bad:
        cursor.execute("""
            UPDATE Traceability_RS.dbo.picking_list_items
            SET pick_status = ?, notes = 'Non conforme in ingresso preformatura'
            WHERE id = ?
        """, (whl.ST_PENDING, i['item_id']))

    cursor.execute(
        "UPDATE Traceability_RS.dbo.picking_lists SET status='REOPENED' WHERE id=?",
        (list_id,))

    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='REOPENED', updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'REOPENED', ?);
        """, (order, operator_id, operator_id))
        whl.log_event(cursor, order, 'VERIFY_FAIL', phase=PHASE_PF,
                      operator_id=operator_id,
                      notes=f"list={list_id}; non_conformi={len(bad)}")

    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status='COMPLETED', last_activity_date=GETDATE()
        WHERE picking_list_id=? AND phase=? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_PF))

    msgs = notif.verify_fail_pf_messages(lbl, bad_codes)
    notif.queue_popup(cursor, notif.TARGET_KIT_PREP, msgs['popup_title'],
                      msgs['popup_msg'], order_number=lbl)
    return {'messages': msgs, 'bad_codes': bad_codes, 'orders_label': lbl}


# ─────────────── Richiesta materiale aggiuntivo (§5.2.3) ──────────────── #

def create_material_request(cursor, order_number: str, phase: str,
                            material_code: str, qty: float, requested_by: int,
                            requester_name: str, note: str,
                            requester_computer: str) -> dict:
    """Inserisce la richiesta, accoda il popup WH e ritorna i messaggi email."""
    cursor.execute("""
        INSERT INTO Traceability_RS.dbo.material_requests
            (order_number, requesting_phase, material_code, qty_requested,
             requested_by, note, requester_computer)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_number, phase, material_code, qty, requested_by,
          note[:500] if note else None, requester_computer))
    request_id = cursor.fetchone()[0]

    whl.log_event(cursor, order_number, 'REQUEST_MATERIAL', phase=phase,
                  material_code=material_code, qty_actual=qty,
                  operator_id=requested_by,
                  notes=f"request={request_id}; nota={note or '-'}")

    msgs = notif.material_request_messages(order_number, phase, material_code,
                                           f"{qty:g}", requester_name, note)
    notif.queue_popup(cursor, notif.TARGET_KIT_PREP, msgs['popup_title'],
                      msgs['popup_msg'], order_number=order_number)
    return {'request_id': request_id, 'messages': msgs}


def get_requests(cursor, only_open: bool = True) -> List[dict]:
    where = "WHERE r.wh_status IN ('PENDING','CONFIRMED') AND r.resolution IS NULL" \
        if only_open else ""
    cursor.execute(f"""
        SELECT r.id, r.order_number, r.requesting_phase, r.material_code,
               r.qty_requested, r.request_date, r.wh_status, r.note,
               ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '') AS requester,
               r.requester_computer, r.confirmed_date, r.resolution
        FROM Traceability_RS.dbo.material_requests r
        LEFT JOIN employee.dbo.EmployeeHireHistory h ON h.EmployeeHireHistoryId = r.requested_by
        LEFT JOIN employee.dbo.employees e ON e.EmployeeId = h.EmployeeId
        {where}
        ORDER BY CASE r.wh_status WHEN 'PENDING' THEN 0 ELSE 1 END, r.request_date ASC
    """)
    cols = ('id', 'order_number', 'phase', 'material_code', 'qty',
            'request_date', 'wh_status', 'note', 'requester',
            'requester_computer', 'confirmed_date', 'resolution')
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def confirm_material_request(cursor, request_id: int, manager_id: int) -> bool:
    """WH conferma il prelievo: AVAILABLE_FOR_PICKUP -> popup al richiedente."""
    cursor.execute("""
        SELECT order_number, material_code, qty_requested, requester_computer,
               requesting_phase
        FROM Traceability_RS.dbo.material_requests
        WHERE id = ? AND wh_status = 'PENDING'
    """, (request_id,))
    r = cursor.fetchone()
    if not r:
        return False
    order_number, material_code, qty, requester_computer, phase = r

    cursor.execute("""
        UPDATE Traceability_RS.dbo.material_requests
        SET wh_status='CONFIRMED', confirmed_by=?, confirmed_date=GETDATE()
        WHERE id=? AND wh_status='PENDING'
    """, (manager_id, request_id))

    whl.log_event(cursor, order_number, 'REQUEST_CONFIRMED', phase=phase,
                  material_code=material_code, qty_actual=qty,
                  operator_id=manager_id, notes=f"request={request_id}")

    msgs = notif.material_ready_messages(order_number, material_code, f"{float(qty):g}")
    target = requester_computer or notif.TARGET_KIT_PREP
    notif.queue_popup(cursor, target, msgs['popup_title'], msgs['popup_msg'],
                      order_number=order_number)
    return True


def cancel_material_request(cursor, request_id: int, operator_id: int,
                            reason: str, resolution: str = 'CANCELLED') -> bool:
    """Annulla una richiesta (anche per 'materiale ritrovato', Sprint 4)."""
    cursor.execute("""
        SELECT order_number, material_code, requesting_phase, wh_status
        FROM Traceability_RS.dbo.material_requests
        WHERE id = ? AND resolution IS NULL
    """, (request_id,))
    r = cursor.fetchone()
    if not r:
        return False
    order_number, material_code, phase, wh_status = r

    cursor.execute("""
        UPDATE Traceability_RS.dbo.material_requests
        SET wh_status = CASE WHEN wh_status='PENDING' THEN 'CANCELLED' ELSE wh_status END,
            resolution = ?, resolved_date = GETDATE()
        WHERE id = ?
    """, (resolution, request_id))

    whl.log_event(cursor, order_number,
                  'MATERIAL_FOUND' if resolution == 'FOUND_IN_PRODUCTION' else 'REQUEST_CANCELLED',
                  phase=phase, material_code=material_code,
                  operator_id=operator_id,
                  notes=f"request={request_id}; motivo={reason}")

    msgs = notif.request_cancelled_messages(order_number, material_code, reason)
    notif.queue_popup(cursor, notif.TARGET_KIT_PREP, msgs['popup_title'],
                      msgs['popup_msg'], order_number=order_number)
    return True
