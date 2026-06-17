"""
kit_wh_logic.py
Logica DB della Fase 1 (Prelievo Magazzino) del modulo Kit Preparation —
Sprint 2 (spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.1, §5.4, §9.2).

Tutte le funzioni ricevono un cursor pyodbc e NON committano: il commit e' a
carico del chiamante (la GUI committa a ogni scansione confermata, §11.3).
Separato dalla GUI per essere testabile senza Tkinter.
"""
import logging
import os
from typing import Dict, List, Optional, Set, Tuple

import kit_essegi_parser as kep

logger = logging.getLogger("PlanMonitor")

PHASE_WH = 'WH'

# pick_status
ST_PENDING = 'PENDING'
ST_PARTIAL = 'PARTIAL'
ST_COMPLETE = 'COMPLETE'
ST_NOT_IN_BOM = 'NOT_IN_BOM'
ST_MISSING_FROM_LIST = 'MISSING_FROM_LIST'
ST_PENDING_COMPLETION = 'PENDING_COMPLETION'
ST_REMOVED = 'REMOVED'

# Stati che bloccano la chiusura normale
BLOCKING_STATUSES = (ST_PENDING, ST_PARTIAL, ST_MISSING_FROM_LIST, ST_PENDING_COMPLETION)


def base_code(code: str) -> str:
    """Codice senza suffisso variante '|n' (rilevazione Sprint 0)."""
    return code.split('|')[0]


# ──────────────────────────── Info lista ──────────────────────────────── #

def get_list_info(cursor, list_id: int) -> Optional[dict]:
    cursor.execute("""
        SELECT id, source_file_name, source_file_path, source_file_hash,
               source_file_date, status, uploaded_by, upload_date
        FROM Traceability_RS.dbo.picking_lists WHERE id = ?
    """, (list_id,))
    r = cursor.fetchone()
    if not r:
        return None
    cursor.execute(
        "SELECT order_number FROM Traceability_RS.dbo.picking_list_orders "
        "WHERE picking_list_id = ? ORDER BY order_number", (list_id,))
    orders = [row[0] for row in cursor.fetchall()]
    return {
        'id': r[0], 'file_name': r[1], 'file_path': r[2], 'file_hash': r[3],
        'file_date': r[4], 'status': r[5], 'uploaded_by': r[6],
        'upload_date': r[7], 'orders': orders,
    }


def orders_label(orders: List[str], max_len: int = 30) -> str:
    """Etichetta ordini per kit_verification_log.order_number (NVARCHAR(30))."""
    joined = '/'.join(o.lstrip('PR').lstrip('0') for o in orders)
    label = 'PR' + joined
    return label if len(label) <= max_len else f"{orders[0]}+{len(orders) - 1}"


def get_items(cursor, list_id: int) -> List[dict]:
    cursor.execute("""
        SELECT id, order_number, material_code, unique_number,
               qty_required, qty_picked, pick_status, picked_by, picked_date, notes
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ?
        ORDER BY CASE pick_status
                     WHEN 'PENDING' THEN 0 WHEN 'PARTIAL' THEN 1
                     WHEN 'PENDING_COMPLETION' THEN 2
                     WHEN 'MISSING_FROM_LIST' THEN 3
                     WHEN 'COMPLETE' THEN 4 ELSE 5 END,
                 material_code, unique_number
    """, (list_id,))
    cols = ('id', 'order_number', 'material_code', 'unique_number',
            'qty_required', 'qty_picked', 'pick_status', 'picked_by',
            'picked_date', 'notes')
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


# ──────────────────────────── Log eventi ──────────────────────────────── #

def log_event(cursor, order_number: str, event_type: str, phase: str = PHASE_WH,
              material_code: str = None, unique_number: str = None,
              qty_expected=None, qty_actual=None, operator_id: int = None,
              notes: str = None):
    cursor.execute("""
        INSERT INTO Traceability_RS.dbo.kit_verification_log
            (order_number, phase, event_type, material_code, unique_number,
             qty_expected, qty_actual, operator_id, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_number[:30], phase, event_type, material_code, unique_number,
          qty_expected, qty_actual, operator_id,
          notes[:1000] if notes else None))


# ──────────────────────── Matching BOM (§5.1.2) ───────────────────────── #

def bom_codes_for_orders(cursor, orders: List[str]) -> Dict[str, Set[str]]:
    """BOM (ComponentCode) per ciascun ordine, dalla query etichette."""
    out = {}
    for order in orders:
        cursor.execute("""
            SELECT DISTINCT C.ComponentCode
            FROM Traceability_RS.dbo.Orders O
            INNER JOIN Traceability_RS.dbo.Products P ON P.IDProduct = O.IDProduct
            INNER JOIN Traceability_RS.dbo.ProductComponentsErp PCE ON PCE.IDProduct = P.IDProduct
            INNER JOIN Traceability_RS.dbo.ProductRiferiments PR ON PR.IDProductCompErp = PCE.IDProductCompErp
            INNER JOIN Traceability_RS.dbo.Components C ON PCE.IDComponent = C.IDComponent
            WHERE O.OrderNumber = ?
        """, (order,))
        out[order] = {r[0] for r in cursor.fetchall()}
    return out


def classify_items(cursor, list_id: int, operator_id: int) -> dict:
    """
    Matching del contenuto lista con le BOM degli ordini (unione):
      - codice file assente da TUTTE le BOM -> pick_status NOT_IN_BOM (warning)
      - codice BOM (per ordine) assente dal file -> riga MISSING_FROM_LIST
    Idempotente: righe MISSING gia' presenti non vengono duplicate; il
    confronto codici gestisce il suffisso variante '|n'.
    Ritorna {'not_in_bom': [...], 'missing': {order: [...]}}.
    """
    info = get_list_info(cursor, list_id)
    boms = bom_codes_for_orders(cursor, info['orders'])
    union_bom = set().union(*boms.values()) if boms else set()
    union_base = {base_code(c) for c in union_bom}

    items = get_items(cursor, list_id)
    file_codes = {i['material_code'] for i in items
                  if i['pick_status'] != ST_MISSING_FROM_LIST}

    # 1. NOT_IN_BOM (solo su righe ancora PENDING senza prelievi)
    not_in_bom = sorted({i['material_code'] for i in items
                         if i['pick_status'] == ST_PENDING
                         and not (i['qty_picked'] or 0)
                         and i['material_code'] not in union_bom
                         and i['material_code'] not in union_base
                         and base_code(i['material_code']) not in union_base})
    for code in not_in_bom:
        cursor.execute("""
            UPDATE Traceability_RS.dbo.picking_list_items
            SET pick_status = ?, notes = 'Non presente nelle BOM degli ordini'
            WHERE picking_list_id = ? AND material_code = ? AND pick_status = ?
        """, (ST_NOT_IN_BOM, list_id, code, ST_PENDING))

    # 2. MISSING_FROM_LIST per ordine
    file_base = {base_code(c) for c in file_codes}
    missing = {}
    for order, codes in boms.items():
        miss = sorted({c for c in codes
                       if c not in file_codes and base_code(c) not in file_base})
        if not miss:
            continue
        missing[order] = miss
        for code in miss:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.picking_list_items
                               WHERE picking_list_id = ? AND material_code = ?
                                 AND pick_status = ?)
                INSERT INTO Traceability_RS.dbo.picking_list_items
                    (picking_list_id, order_number, material_code, qty_required, pick_status, notes)
                VALUES (?, ?, ?, 0, ?, 'In BOM ma assente dalla lista Essegi')
            """, (list_id, code, ST_MISSING_FROM_LIST,
                  list_id, order, code, ST_MISSING_FROM_LIST))

    if not_in_bom or missing:
        log_event(cursor, orders_label(info['orders']), 'BOM_CHECK',
                  operator_id=operator_id,
                  notes=f"list={list_id}; not_in_bom={len(not_in_bom)}; "
                        f"missing={sum(len(v) for v in missing.values())}")
    return {'not_in_bom': not_in_bom, 'missing': missing}


# ───────────────────────── Sessioni (§5.4) ────────────────────────────── #

def find_open_session(cursor, list_id: int, phase: str = PHASE_WH) -> Optional[dict]:
    cursor.execute("""
        SELECT TOP 1 id, operator_id, started_date, last_activity_date,
               status, source_file_hash
        FROM Traceability_RS.dbo.kit_sessions
        WHERE picking_list_id = ? AND phase = ? AND status IN ('ACTIVE','SUSPENDED')
        ORDER BY started_date DESC
    """, (list_id, phase))
    r = cursor.fetchone()
    if not r:
        return None
    return {'id': r[0], 'operator_id': r[1], 'started_date': r[2],
            'last_activity_date': r[3], 'status': r[4], 'file_hash': r[5]}


def create_session(cursor, list_id: int, operator_id: int, file_hash: str,
                   phase: str = PHASE_WH) -> int:
    cursor.execute("""
        INSERT INTO Traceability_RS.dbo.kit_sessions
            (picking_list_id, phase, operator_id, source_file_hash,
             last_activity_date)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, GETDATE())
    """, (list_id, phase, operator_id, file_hash))
    return cursor.fetchone()[0]


def resume_session(cursor, session_id: int, operator_id: int,
                   orders_lbl: str) -> None:
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status = 'ACTIVE', operator_id = ?, last_activity_date = GETDATE()
        WHERE id = ?
    """, (operator_id, session_id))
    log_event(cursor, orders_lbl, 'SESSION_RESUMED', operator_id=operator_id,
              notes=f"session={session_id}")


def touch_session(cursor, session_id: int) -> None:
    cursor.execute(
        "UPDATE Traceability_RS.dbo.kit_sessions SET last_activity_date = GETDATE() WHERE id = ?",
        (session_id,))


def set_session_status(cursor, session_id: int, status: str,
                       operator_id: int = None, orders_lbl: str = None) -> None:
    cursor.execute(
        "UPDATE Traceability_RS.dbo.kit_sessions SET status = ?, last_activity_date = GETDATE() WHERE id = ?",
        (status, session_id))
    if status == 'SUSPENDED' and orders_lbl:
        log_event(cursor, orders_lbl, 'SESSION_SUSPENDED',
                  operator_id=operator_id, notes=f"session={session_id}")


def set_resume_decision(cursor, session_id: int, decision: str, note: str) -> None:
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET resume_decision = ?, resume_note = ?
        WHERE id = ?
    """, (decision, note[:500] if note else None, session_id))


def check_source_file(cursor, list_id: int) -> dict:
    """
    Confronta il file registrato sulla lista con quello attuale su disco.
    Ritorna {'state': 'SAME'|'CHANGED'|'MISSING', 'stored_hash', 'current_hash'}.
    """
    info = get_list_info(cursor, list_id)
    path = info['file_path']
    if not os.path.isfile(path):
        return {'state': 'MISSING', 'stored_hash': info['file_hash'],
                'current_hash': None, 'path': path}
    current = kep.file_sha256(path)
    state = 'SAME' if current == info['file_hash'] else 'CHANGED'
    return {'state': state, 'stored_hash': info['file_hash'],
            'current_hash': current, 'path': path}


def adopt_new_file(cursor, list_id: int, operator_id: int) -> dict:
    """
    Adotta il file attuale come nuova sorgente (decisione ADOPT_NEW_FILE §5.4.2):
    diff per unique_number — aggiorna qty_required variate, inserisce righe
    nuove, marca REMOVED le righe sparite (le gia' prelevate restano visibili).
    Ritorna riepilogo {'added': n, 'updated': n, 'removed': n, 'parsed': EssegiFile}.
    """
    info = get_list_info(cursor, list_id)
    parsed = kep.parse_essegi_file(info['file_path'])

    items = get_items(cursor, list_id)
    by_unique = {i['unique_number']: i for i in items if i['unique_number']}
    new_by_unique = {r.unique_number: r for r in parsed.rows}

    added = updated = removed = 0
    for un, row in new_by_unique.items():
        old = by_unique.get(un)
        if old is None:
            cursor.execute("""
                INSERT INTO Traceability_RS.dbo.picking_list_items
                    (picking_list_id, material_code, unique_number, qty_required)
                VALUES (?, ?, ?, ?)
            """, (list_id, row.material_code, un, row.quantity))
            added += 1
        elif float(old['qty_required']) != row.quantity:
            new_status = old['pick_status']
            if new_status in (ST_COMPLETE, ST_PARTIAL, ST_PENDING):
                picked = float(old['qty_picked'] or 0)
                new_status = (ST_COMPLETE if picked >= row.quantity
                              else ST_PARTIAL if picked > 0 else ST_PENDING)
            cursor.execute("""
                UPDATE Traceability_RS.dbo.picking_list_items
                SET qty_required = ?, pick_status = ?
                WHERE id = ?
            """, (row.quantity, new_status, old['id']))
            updated += 1
    for un, old in by_unique.items():
        if un not in new_by_unique and old['pick_status'] not in (ST_REMOVED,):
            cursor.execute("""
                UPDATE Traceability_RS.dbo.picking_list_items
                SET pick_status = ?, notes = 'Riga non piu'' presente nel nuovo file'
                WHERE id = ?
            """, (ST_REMOVED, old['id']))
            removed += 1

    cursor.execute("""
        UPDATE Traceability_RS.dbo.picking_lists
        SET source_file_hash = ?, source_file_date = ?
        WHERE id = ?
    """, (parsed.file_hash, parsed.file_date, list_id))

    log_event(cursor, orders_label(info['orders']), 'SOURCE_FILE_CHANGED',
              operator_id=operator_id,
              notes=f"list={list_id}; old_hash={info['file_hash'][:12]}; "
                    f"new_hash={parsed.file_hash[:12]}; "
                    f"added={added}; updated={updated}; removed={removed}")
    return {'added': added, 'updated': updated, 'removed': removed, 'parsed': parsed}


def keep_old_file(cursor, list_id: int, operator_id: int, current_hash: str) -> None:
    """Decisione KEEP_OLD_FILE: si continua coi dati salvati; solo log."""
    info = get_list_info(cursor, list_id)
    log_event(cursor, orders_label(info['orders']), 'SOURCE_FILE_CHANGED',
              operator_id=operator_id,
              notes=f"list={list_id}; decisione=KEEP_OLD_FILE; "
                    f"hash_attuale={(current_hash or 'FILE_ASSENTE')[:12]}")


# ───────────────────────── Scansioni (§5.1.3) ─────────────────────────── #

def apply_scan(cursor, list_id: int, unique_number: str, qty: float,
               operator_id: int, session_id: int) -> Tuple[str, Optional[dict]]:
    """
    Registra una scansione: qty e' la quantita' fisica contata per la
    scatola/bobina (valore assoluto). Ritorna (esito, item):
      'ok'         scansione registrata
      'duplicate'  riga gia' COMPLETE (warning §11.3, nessun doppio conteggio)
      'not_found'  unique number assente dalla lista (§9.2, loggato)
    """
    info = get_list_info(cursor, list_id)
    lbl = orders_label(info['orders'])

    cursor.execute("""
        SELECT id, material_code, qty_required, qty_picked, pick_status, order_number
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ? AND unique_number = ?
          AND pick_status NOT IN (?, ?)
    """, (list_id, unique_number, ST_MISSING_FROM_LIST, ST_REMOVED))
    r = cursor.fetchone()

    if r is None:
        log_event(cursor, lbl, 'UNKNOWN_UNIQUE_NUMBER',
                  unique_number=unique_number, qty_actual=qty,
                  operator_id=operator_id, notes=f"list={list_id}")
        touch_session(cursor, session_id)
        return 'not_found', None

    item_id, material_code, qty_required, qty_picked, status, order_number = r
    if status == ST_COMPLETE and qty is None:
        return 'duplicate', {'id': item_id, 'material_code': material_code}

    qty = float(qty)
    qty_required = float(qty_required)
    new_status = (ST_COMPLETE if qty >= qty_required
                  else ST_PARTIAL if qty > 0 else ST_PENDING)
    cursor.execute("""
        UPDATE Traceability_RS.dbo.picking_list_items
        SET qty_picked = ?, pick_status = ?, picked_by = ?, picked_date = GETDATE()
        WHERE id = ?
    """, (qty, new_status, operator_id, item_id))

    log_event(cursor, order_number or lbl, 'SCAN',
              material_code=material_code, unique_number=unique_number,
              qty_expected=qty_required, qty_actual=qty,
              operator_id=operator_id, notes=f"list={list_id}; status={new_status}")
    touch_session(cursor, session_id)
    return 'ok', {'id': item_id, 'material_code': material_code,
                  'qty_required': qty_required, 'qty_picked': qty,
                  'pick_status': new_status}


def find_item_by_unique(cursor, list_id: int, unique_number: str) -> Optional[dict]:
    """Lookup per anteprima alla scansione (senza scrivere)."""
    cursor.execute("""
        SELECT id, material_code, qty_required, qty_picked, pick_status
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ? AND unique_number = ?
          AND pick_status NOT IN (?, ?)
    """, (list_id, unique_number, ST_MISSING_FROM_LIST, ST_REMOVED))
    r = cursor.fetchone()
    if not r:
        return None
    return {'id': r[0], 'material_code': r[1], 'qty_required': float(r[2]),
            'qty_picked': float(r[3] or 0), 'pick_status': r[4]}


# ───────────────────── Chiusura lista (§5.1.4) ────────────────────────── #

def closure_state(cursor, list_id: int) -> dict:
    """Conteggi per stato + scansioni sconosciute, per abilitare i pulsanti."""
    cursor.execute("""
        SELECT pick_status, COUNT(*)
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ?
        GROUP BY pick_status
    """, (list_id,))
    counts = {r[0]: r[1] for r in cursor.fetchall()}
    cursor.execute("""
        SELECT COUNT(*) FROM Traceability_RS.dbo.kit_verification_log
        WHERE event_type = 'UNKNOWN_UNIQUE_NUMBER' AND notes LIKE ?
    """, (f"list={list_id}%",))
    unknown = cursor.fetchone()[0]
    blocking = sum(counts.get(s, 0) for s in BLOCKING_STATUSES)
    return {'counts': counts, 'unknown_scans': unknown,
            'blocking': blocking, 'can_close': blocking == 0}


def close_list(cursor, list_id: int, operator_id: int) -> None:
    """Chiusura normale: tutte le righe verdi (validare prima con closure_state)."""
    info = get_list_info(cursor, list_id)
    cursor.execute("""
        UPDATE Traceability_RS.dbo.picking_lists
        SET status = 'CLOSED', closed_date = GETDATE(), closed_by = ?
        WHERE id = ?
    """, (operator_id, list_id))
    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='WH_CLOSED', updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'WH_CLOSED', ?);
        """, (order, operator_id, operator_id))
        log_event(cursor, order, 'VERIFY_OK', operator_id=operator_id,
                  notes=f"list={list_id}; chiusura completa")
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status = 'COMPLETED', last_activity_date = GETDATE()
        WHERE picking_list_id = ? AND phase = ? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_WH))


def close_with_derogation(cursor, list_id: int, manager_id: int, note: str) -> List[str]:
    """
    Chiusura con deroga (§5.1.4): righe incomplete -> PENDING_COMPLETION,
    lista PARTIAL, ordini WH_PARTIAL. Ritorna i codici mancanti registrati.
    """
    info = get_list_info(cursor, list_id)
    cursor.execute("""
        SELECT DISTINCT material_code
        FROM Traceability_RS.dbo.picking_list_items
        WHERE picking_list_id = ? AND pick_status IN (?, ?, ?)
    """, (list_id, ST_PENDING, ST_PARTIAL, ST_MISSING_FROM_LIST))
    missing = sorted(r[0] for r in cursor.fetchall())

    cursor.execute("""
        UPDATE Traceability_RS.dbo.picking_list_items
        SET pick_status = ?
        WHERE picking_list_id = ? AND pick_status IN (?, ?, ?)
    """, (ST_PENDING_COMPLETION, list_id, ST_PENDING, ST_PARTIAL, ST_MISSING_FROM_LIST))

    cursor.execute("""
        UPDATE Traceability_RS.dbo.picking_lists
        SET status = 'PARTIAL', closed_date = GETDATE(), closed_by = ?,
            derogation_by = ?, derogation_note = ?
        WHERE id = ?
    """, (manager_id, manager_id, note[:500], list_id))

    missing_txt = ', '.join(missing)
    for order in info['orders']:
        cursor.execute("""
            MERGE Traceability_RS.dbo.kit_status AS t
            USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
            WHEN MATCHED THEN UPDATE SET status='WH_PARTIAL', updated_by=?, updated_date=GETDATE()
            WHEN NOT MATCHED THEN INSERT (order_number, status, updated_by)
                VALUES (s.order_number, 'WH_PARTIAL', ?);
        """, (order, manager_id, manager_id))
        log_event(cursor, order, 'CLOSE_DEROGATION', operator_id=manager_id,
                  notes=f"list={list_id}; nota={note}; mancanti={missing_txt}")
    cursor.execute("""
        UPDATE Traceability_RS.dbo.kit_sessions
        SET status = 'COMPLETED', last_activity_date = GETDATE()
        WHERE picking_list_id = ? AND phase = ? AND status IN ('ACTIVE','SUSPENDED')
    """, (list_id, PHASE_WH))
    return missing
