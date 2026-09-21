# -*- coding: utf-8 -*-
"""
kanban_logic.py — Logica pura del kanban WIP/REPAIR (nessuna dipendenza Tk/Flask).

Le funzioni ricevono un cursor pyodbc gia' posizionato sulla connessione;
la gestione di connessione/commit/rollback e' responsabilita' del chiamante
(routes_kanban.py). Stesso pattern di touchup_logic.py.

Tabelle (sql/create_wip_kanban_tables.sql):
  ind.WipKanbanLocations  — posizioni (WP1A1...)
  ind.WipKanbanBoards     — schede caricate (DateOut = prelevata)
  ind.WipKanbanAudit      — audit IN/OUT/CREATE
"""
import logging
import pyodbc

logger = logging.getLogger("WipKanban")

AREA_LETTERS = {"WIP": "W", "REPAIR": "R"}
LETTER_AREAS = {v: k for k, v in AREA_LETTERS.items()}
COLUMNS = "ABCD"
LEVELS = range(1, 5)

# ─────────────────────────────────────────────────────────────────────────────
# LabelCode → scheda (riuso logica di verifica di line_validation_gui /
# touchup_logic: LabelCodes → Boards → Orders → Products, ultima scansione)
# ─────────────────────────────────────────────────────────────────────────────

_Q_BOARD_INFO = """
SELECT l.IDBoard, l.LabelCod, o.IDOrder, o.OrderNumber, pr.ProductCode,
       ph.PhaseName,
       CASE WHEN ls.IsPass IS NULL THEN NULL WHEN ls.IsPass = 0 THEN 'FAIL' ELSE 'PASS' END AS ScanResult,
       ls.ScanTimeFinish
FROM Traceability_RS.dbo.LabelCodes l
JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = l.IDBoard
JOIN Traceability_RS.dbo.Orders o ON o.IDOrder = b.IDOrder
JOIN Traceability_RS.dbo.Products pr ON pr.IDProduct = o.IDProduct
CROSS APPLY (
    SELECT TOP 1 s.IsPass, s.ScanTimeFinish, s.IDOrderPhase
    FROM Traceability_RS.dbo.Scannings s
    WHERE s.IDBoard = b.IDBoard
    ORDER BY s.IDScan DESC
) ls
LEFT JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrderPhase = ls.IDOrderPhase
LEFT JOIN Traceability_RS.dbo.Phases ph ON ph.IDPhase = op.IDPhase
WHERE l.LabelCod = ?
"""

_Q_BOARDS_IN_POSITION = """
SELECT wl.PositionCode, wb.LabelCode, wb.OrderNumber, wb.ProductCode, wb.DateIn, wb.[User] AS LoadedBy,
       ph.PhaseName,
       CASE WHEN ls.IsPass IS NULL THEN NULL WHEN ls.IsPass = 0 THEN 'FAIL' ELSE 'PASS' END AS ScanResult,
       ls.ScanTimeFinish
FROM Traceability_RS.ind.WipKanbanBoards wb
JOIN Traceability_RS.ind.WipKanbanLocations wl ON wl.LocationId = wb.LocationId
JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = wb.IDBoard
CROSS APPLY (
    SELECT TOP 1 s.IsPass, s.ScanTimeFinish, s.IDOrderPhase
    FROM Traceability_RS.dbo.Scannings s
    WHERE s.IDBoard = b.IDBoard
    ORDER BY s.IDScan DESC
) ls
LEFT JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrderPhase = ls.IDOrderPhase
LEFT JOIN Traceability_RS.dbo.Phases ph ON ph.IDPhase = op.IDPhase
{where}
ORDER BY wl.PositionCode, wb.DateIn
"""


def board_info(cur, labelcode):
    """Restituisce dict con i dati della scheda (ordine, prodotto, fase, esito)
    o None se il LabelCode non e' riconosciuto."""
    cur.execute(_Q_BOARD_INFO, (labelcode,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [d[0] for d in cur.description]
    return {c: row[i] for i, c in enumerate(cols)}


# ─────────────────────────────────────────────────────────────────────────────
# Locazioni
# ─────────────────────────────────────────────────────────────────────────────

def parse_master(master_code):
    """'WP1' -> ('WIP', 1). None se il formato non e' valido."""
    if not master_code or len(master_code) < 3:
        return None
    letter, rest = master_code[0].upper(), master_code[1:].upper()
    if letter not in LETTER_AREAS or not rest.startswith("P"):
        return None
    digits = rest[1:]
    if not digits.isdigit():
        return None
    return LETTER_AREAS[letter], int(digits)


def master_code(area, pallet_number):
    return f"{AREA_LETTERS[area]}P{pallet_number}"


def _row_index_taken(cur, area, deposit, row_index, exclude_pallet=None):
    """True se un altro pallet (Area+Deposit) ha già questo RowIndex
    (i RowIndex NULL non contano). exclude_pallet esclude il master stesso
    (per la modifica post-creazione)."""
    sql = """SELECT COUNT(DISTINCT PalletNumber)
           FROM Traceability_RS.ind.WipKanbanLocations
           WHERE Area = ? AND Deposit = ? AND RowIndex = ?"""
    params = [area, deposit, row_index]
    if exclude_pallet is not None:
        sql += " AND PalletNumber <> ?"
        params.append(exclude_pallet)
    cur.execute(sql, params)
    return int(cur.fetchone()[0]) > 0


def create_location(cur, area, user, row_index=None, deposit=1):
    """Crea un nuovo pallet (16 posizioni) per l'area. Restituisce il codice
    master (es. 'WP1'). Il vincolo UNIQUE su PositionCode impedisce duplicati.
    row_index = posizione del pallet nella fila (display di reparto): OBBLIGATORIO
    (>= 1) e univoco per Area+Deposit. deposit = deposito fisico (default 1)."""
    area = (area or "").upper().strip()
    if area not in AREA_LETTERS:
        raise ValueError(f"Area non valida: {area!r} (attese: {list(AREA_LETTERS)})")
    if row_index is None or int(row_index) < 1:
        raise ValueError("missing_row_index")
    row_index = int(row_index)
    if _row_index_taken(cur, area, deposit, row_index):
        raise ValueError("duplicate_row_index")

    cur.execute(
        """SELECT ISNULL(MAX(PalletNumber), 0) + 1
           FROM Traceability_RS.ind.WipKanbanLocations WHERE Area = ?""",
        (area,),
    )
    pallet = int(cur.fetchone()[0])
    letter = AREA_LETTERS[area]
    for col in COLUMNS:
        for level in LEVELS:
            cur.execute(
                """INSERT INTO Traceability_RS.ind.WipKanbanLocations
                   (Area, PalletNumber, PositionCode, DateIn, [User], RowIndex, Deposit)
                   VALUES (?, ?, ?, GETDATE(), ?, ?, ?)""",
                (area, pallet, f"{letter}P{pallet}{col}{level}", user, row_index, deposit),
            )

    code = master_code(area, pallet)
    _audit(cur, "CREATE", None, code, None, None, user)
    return code


def set_master_rowindex(cur, master, row_index, deposit=1):
    """Aggiorna il RowIndex delle 16 posizioni di un master esistente
    (per posizionare i pallet creati prima del display). Restituisse True
    se il master esiste. Il RowIndex deve essere >= 1 e univoco per
    Area+Deposit (escluso il master stesso)."""
    parsed = parse_master(master)
    if not parsed:
        return False
    area, pallet = parsed
    if row_index is None or int(row_index) < 1:
        raise ValueError("missing_row_index")
    row_index = int(row_index)
    if _row_index_taken(cur, area, deposit, row_index, exclude_pallet=pallet):
        raise ValueError("duplicate_row_index")
    cur.execute(
        """UPDATE Traceability_RS.ind.WipKanbanLocations
           SET RowIndex = ?
           WHERE Area = ? AND PalletNumber = ? AND Deposit = ?""",
        (row_index, area, pallet, deposit),
    )
    return cur.rowcount > 0


def list_masters(cur, deposit=1):
    """Restituisce la lista dei master presenti:
    [{'code','area','pallet','row_index'}] (row_index = MIN per pallet)."""
    cur.execute(
        """SELECT Area, PalletNumber, MIN(RowIndex)
           FROM Traceability_RS.ind.WipKanbanLocations
           WHERE Deposit = ?
           GROUP BY Area, PalletNumber
           ORDER BY Area, PalletNumber""",
        (deposit,),
    )
    return [
        {"code": master_code(area, pn), "area": area, "pallet": pn,
         "row_index": row_index}
        for area, pn, row_index in cur.fetchall()
    ]


def list_positions(cur, master):
    """Tutte le posizioni di un master, ordinate (WP1A1...WP1D4)."""
    parsed = parse_master(master)
    if not parsed:
        return []
    area, pallet = parsed
    cur.execute(
        """SELECT PositionCode FROM Traceability_RS.ind.WipKanbanLocations
           WHERE Area = ? AND PalletNumber = ?
           ORDER BY PositionCode""",
        (area, pallet),
    )
    return [r[0] for r in cur.fetchall()]


def counts(cur):
    """Conteggi per la riga in basso: master totali per area + schede presenti."""
    cur.execute(
        """SELECT Area, COUNT(DISTINCT PalletNumber)
           FROM Traceability_RS.ind.WipKanbanLocations GROUP BY Area"""
    )
    per_area = {area: n for area, n in cur.fetchall()}
    cur.execute(
        "SELECT COUNT(*) FROM Traceability_RS.ind.WipKanbanBoards WHERE DateOut IS NULL"
    )
    boards = int(cur.fetchone()[0])
    return {
        "wip": per_area.get("WIP", 0),
        "repair": per_area.get("REPAIR", 0),
        "boards": boards,
    }


def boards_in_position(cur, position_code):
    """Schede attive in una posizione, con fase corrente ed esito."""
    cur.execute(_Q_BOARDS_IN_POSITION.format(where="WHERE wl.PositionCode = ? AND wb.DateOut IS NULL"),
                (position_code,))
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


def boards_in_master(cur, master):
    """Schede attive in tutte le posizioni di un master (per conteggio)."""
    parsed = parse_master(master)
    if not parsed:
        return []
    area, pallet = parsed
    cur.execute(_Q_BOARDS_IN_POSITION.format(
        where="WHERE wl.Area = ? AND wl.PalletNumber = ? AND wb.DateOut IS NULL"), (area, pallet))
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


# ─────────────────────────────────────────────────────────────────────────────
# Carica / preleva
# ─────────────────────────────────────────────────────────────────────────────

def _position_exists(cur, position_code):
    cur.execute(
        "SELECT LocationId FROM Traceability_RS.ind.WipKanbanLocations WHERE PositionCode = ?",
        (position_code,),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _find_active_board(cur, labelcode):
    cur.execute(
        """SELECT wb.BoardKanbanId, wl.PositionCode
           FROM Traceability_RS.ind.WipKanbanBoards wb
           JOIN Traceability_RS.ind.WipKanbanLocations wl ON wl.LocationId = wb.LocationId
           WHERE wb.LabelCode = ? AND wb.DateOut IS NULL""",
        (labelcode,),
    )
    return cur.fetchone()


def load_board(cur, position_code, labelcode, user):
    """Carica una scheda in una posizione. Restituisce (ok, errore, info)."""
    labelcode = (labelcode or "").strip()
    if not labelcode:
        return False, "invalid_labelcode", None
    location_id = _position_exists(cur, position_code)
    if location_id is None:
        return False, "invalid_position", None

    existing = _find_active_board(cur, labelcode)
    if existing:
        return False, "board_already_in", {"position": existing[1]}

    info = board_info(cur, labelcode)
    if not info:
        return False, "invalid_labelcode", None

    cur.execute(
        """INSERT INTO Traceability_RS.ind.WipKanbanBoards
           (LocationId, IDBoard, LabelCode, IDOrder, OrderNumber, ProductCode, DateIn, [User])
           VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?)""",
        (location_id, info["IDBoard"], labelcode, info["IDOrder"],
         info["OrderNumber"], info["ProductCode"], user),
    )
    _audit(cur, "IN", labelcode, position_code,
           info["OrderNumber"], info["ProductCode"], user)
    return True, None, info


_Q_KANBAN_STATUS = """
SELECT wb.LabelCode, wb.OrderNumber, wb.ProductCode, wb.DateIn, wb.[User] AS LoadedBy,
       wl.PositionCode, wl.Area
FROM Traceability_RS.ind.WipKanbanBoards wb
JOIN Traceability_RS.ind.WipKanbanLocations wl ON wl.LocationId = wb.LocationId
WHERE wb.LabelCode = ? AND wb.DateOut IS NULL
"""


def kanban_status(cur, labelcode):
    """Dati della scheda attualmente in kanban (posizione, data inserimento, ecc.)
    o None se la scheda non e' presente."""
    labelcode = (labelcode or "").strip()
    if not labelcode:
        return None
    cur.execute(_Q_KANBAN_STATUS, (labelcode,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [d[0] for d in cur.description]
    return {c: row[i] for i, c in enumerate(cols)}


def withdraw_board(cur, labelcode, user):
    """Preleva una scheda dal kanban (DateOut + audit OUT)."""
    labelcode = (labelcode or "").strip()
    if not labelcode:
        return False, "invalid_labelcode", None
    row = _find_active_board(cur, labelcode)
    if not row:
        return False, "not_in_kanban", None
    board_kanban_id, position_code = row
    cur.execute(
        """UPDATE Traceability_RS.ind.WipKanbanBoards
           SET DateOut = GETDATE(), OutUser = ?
           WHERE BoardKanbanId = ?""",
        (user, board_kanban_id),
    )
    cur.execute(
        """SELECT OrderNumber, ProductCode, DateIn, [User]
           FROM Traceability_RS.ind.WipKanbanBoards
           WHERE BoardKanbanId = ?""",
        (board_kanban_id,),
    )
    info = {"position": position_code}
    info_row = cur.fetchone()
    if info_row:
        info.update({"OrderNumber": info_row[0], "ProductCode": info_row[1],
                     "DateIn": info_row[2], "LoadedBy": info_row[3]})
    _audit(cur, "OUT", labelcode, position_code,
           info.get("OrderNumber"), info.get("ProductCode"), user)
    return True, None, info


# ─────────────────────────────────────────────────────────────────────────────
# Ricerca (pagina Preleva) e lista completa (PDF)
# ─────────────────────────────────────────────────────────────────────────────

def search_locations(cur, order=None, product=None, labelcode=None):
    """Posizioni che contengono schede attive dell'ordine / del prodotto / del LabelCode."""
    clauses, params = ["wb.DateOut IS NULL"], []
    if order:
        clauses.append("wb.OrderNumber LIKE ?")
        params.append(f"%{order.strip()}%")
    if product:
        clauses.append("wb.ProductCode LIKE ?")
        params.append(f"%{product.strip()}%")
    if labelcode:
        clauses.append("wb.LabelCode LIKE ?")
        params.append(f"%{labelcode.strip()}%")
    if len(clauses) == 1:
        return []
    cur.execute(
        f"""SELECT DISTINCT wl.PositionCode, wb.OrderNumber, wb.ProductCode, wb.LabelCode
            FROM Traceability_RS.ind.WipKanbanBoards wb
            JOIN Traceability_RS.ind.WipKanbanLocations wl ON wl.LocationId = wb.LocationId
            WHERE {' AND '.join(clauses)}
            ORDER BY wl.PositionCode""",
        params,
    )
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


def list_all_boards(cur):
    """Tutte le schede attive, raggruppate per posizione (ordine alfabetico)."""
    cur.execute(_Q_BOARDS_IN_POSITION.format(where="WHERE wb.DateOut IS NULL"))
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


_Q_ALL_BY_AREA = """
SELECT wl.PositionCode, wb.LabelCode, wb.OrderNumber, wb.ProductCode, wb.DateIn,
       wb.[User] AS LoadedBy,
       ph.PhaseName,
       CASE WHEN ls.IsPass IS NULL THEN NULL WHEN ls.IsPass = 0 THEN 'FAIL' ELSE 'PASS' END AS ScanResult,
       ls.ScanTimeFinish
FROM Traceability_RS.ind.WipKanbanLocations wl
LEFT JOIN Traceability_RS.ind.WipKanbanBoards wb
       ON wb.LocationId = wl.LocationId AND wb.DateOut IS NULL
LEFT JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = wb.IDBoard
OUTER APPLY (
    SELECT TOP 1 s.IsPass, s.ScanTimeFinish, s.IDOrderPhase
    FROM Traceability_RS.dbo.Scannings s
    WHERE s.IDBoard = b.IDBoard
    ORDER BY s.IDScan DESC
) ls
LEFT JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrderPhase = ls.IDOrderPhase
LEFT JOIN Traceability_RS.dbo.Phases ph ON ph.IDPhase = op.IDPhase
WHERE wl.Area = ?
ORDER BY wl.PositionCode, wb.DateIn
"""


def list_all_boards_by_area(cur, area):
    """Tutte le posizioni di un'area (anche vuote) con le schede attive contenute."""
    cur.execute(_Q_ALL_BY_AREA, (area,))
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


# ─────────────────────────────────────────────────────────────────────────────
# Report Excel (pagina pubblica /kanban/report)
# ─────────────────────────────────────────────────────────────────────────────

_Q_REPORT = """
SELECT wb.ProductCode, wl.Area, wl.PositionCode,
       LEFT(wl.PositionCode, LEN(wl.PositionCode) - 2) AS Pallet,
       wb.OrderNumber, wb.LabelCode,
       ph.PhaseName,
       CASE WHEN ls.IsPass IS NULL THEN NULL WHEN ls.IsPass = 0 THEN 'FAIL' ELSE 'PASS' END AS ScanResult,
       wb.DateIn, wb.[User] AS LoadedBy
FROM Traceability_RS.ind.WipKanbanBoards wb
JOIN Traceability_RS.ind.WipKanbanLocations wl ON wl.LocationId = wb.LocationId
JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = wb.IDBoard
CROSS APPLY (
    SELECT TOP 1 s.IsPass, s.ScanTimeFinish, s.IDOrderPhase
    FROM Traceability_RS.dbo.Scannings s
    WHERE s.IDBoard = b.IDBoard
    ORDER BY s.IDScan DESC
) ls
LEFT JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrderPhase = ls.IDOrderPhase
LEFT JOIN Traceability_RS.dbo.Phases ph ON ph.IDPhase = op.IDPhase
{where}
ORDER BY wb.ProductCode, wl.PositionCode, wb.OrderNumber, wl.Area, wb.LabelCode
"""


def report_boards(cur, order='', wip_type='all', product='', state='all'):
    """Schede attive (DateOut IS NULL) per il report Excel.

    Filtri: order/product = match esatti (vuoto = nessun filtro);
    wip_type = 'wip'/'repair' (altro = tutto); state = 'fail' -> ScanResult='FAIL',
    'wip' -> ScanResult PASS o NULL (ls.IsPass IS NULL OR ls.IsPass <> 0)."""
    clauses, params = ["wb.DateOut IS NULL"], []
    order = (order or "").strip()
    product = (product or "").strip()
    if order:
        clauses.append("wb.OrderNumber = ?")
        params.append(order)
    if product:
        clauses.append("wb.ProductCode = ?")
        params.append(product)
    if wip_type == "wip":
        clauses.append("wl.Area = 'WIP'")
    elif wip_type == "repair":
        clauses.append("wl.Area = 'REPAIR'")
    if state == "fail":
        clauses.append("ls.IsPass = 0")
    elif state == "wip":
        clauses.append("(ls.IsPass IS NULL OR ls.IsPass <> 0)")
    cur.execute(_Q_REPORT.format(where="WHERE " + " AND ".join(clauses)), params)
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


def report_filter_values(cur):
    """OrderNumber e ProductCode distinti delle schede attive (dropdown report)."""
    cur.execute(
        """SELECT DISTINCT OrderNumber FROM Traceability_RS.ind.WipKanbanBoards
           WHERE DateOut IS NULL ORDER BY OrderNumber"""
    )
    orders = [r[0] for r in cur.fetchall()]
    cur.execute(
        """SELECT DISTINCT ProductCode FROM Traceability_RS.ind.WipKanbanBoards
           WHERE DateOut IS NULL ORDER BY ProductCode"""
    )
    products = [r[0] for r in cur.fetchall()]
    return {"orders": orders, "products": products}


# ─────────────────────────────────────────────────────────────────────────────
# Audit
# ─────────────────────────────────────────────────────────────────────────────

def _audit(cur, action, labelcode, position_code, order_number, product_code, user):
    cur.execute(
        """INSERT INTO Traceability_RS.ind.WipKanbanAudit
           (Action, LabelCode, PositionCode, OrderNumber, ProductCode, [User], DateIn)
           VALUES (?, ?, ?, ?, ?, ?, GETDATE())""",
        (action, labelcode, position_code, order_number, product_code, user),
    )


def movements_between(cur, start, end):
    """Movimenti IN/OUT nel periodo [start, end) per l'email di fine turno."""
    cur.execute(
        """SELECT Action, LabelCode, PositionCode, OrderNumber, ProductCode, [User], DateIn
           FROM Traceability_RS.ind.WipKanbanAudit
           WHERE DateIn >= ? AND DateIn < ? AND Action IN ('IN', 'OUT')
           ORDER BY DateIn""",
        (start, end),
    )
    cols = [d[0] for d in cur.description]
    return [{c: row[i] for i, c in enumerate(cols)} for row in cur.fetchall()]


# ─────────────────────────────────────────────────────────────────────────────
# Display di reparto (server :6505) — stato 3D + dashboard
# ─────────────────────────────────────────────────────────────────────────────

_Q_DISPLAY_POSITIONS = """
SELECT wl.PositionCode,
       wb.LabelCode,
       CASE WHEN ls.IsPass IS NULL THEN NULL WHEN ls.IsPass = 0 THEN 'FAIL' ELSE 'PASS' END AS ScanResult
FROM Traceability_RS.ind.WipKanbanLocations wl
OUTER APPLY (
    SELECT TOP 1 LabelCode, IDBoard
    FROM Traceability_RS.ind.WipKanbanBoards wb2
    WHERE wb2.LocationId = wl.LocationId AND wb2.DateOut IS NULL
    ORDER BY wb2.DateIn DESC
) wb
LEFT JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = wb.IDBoard
OUTER APPLY (
    SELECT TOP 1 s.IsPass
    FROM Traceability_RS.dbo.Scannings s
    WHERE s.IDBoard = b.IDBoard
    ORDER BY s.IDScan DESC
) ls
WHERE wl.Area = ? AND wl.Deposit = ?
ORDER BY wl.PositionCode
"""


def _iso(value):
    """Serializzazione JSON-safe: datetime → ISO string, resto invariato."""
    from datetime import datetime, date
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()
    return value


def display_state(cur, area, deposit=1):
    """Stato completo per il display di reparto (area+deposit):
    pallet con le 16 posizioni (occupazione + esito ultima scansione),
    conteggi dashboard e movimenti IN/OUT di oggi."""
    area = (area or "").upper().strip()
    if area not in AREA_LETTERS:
        raise ValueError(f"Area non valida: {area!r} (attese: {list(AREA_LETTERS)})")
    letter = AREA_LETTERS[area]

    # Pallet della fila (RowIndex NULL → in fondo, per PalletNumber)
    cur.execute(
        """SELECT Area, PalletNumber, MIN(RowIndex)
           FROM Traceability_RS.ind.WipKanbanLocations
           WHERE Area = ? AND Deposit = ?
           GROUP BY Area, PalletNumber
           ORDER BY CASE WHEN MIN(RowIndex) IS NULL THEN 1 ELSE 0 END,
                    MIN(RowIndex), PalletNumber""",
        (area, deposit),
    )
    pallets = [
        {"code": master_code(a, pn), "pallet": pn, "row_index": ri}
        for a, pn, ri in cur.fetchall()
    ]

    # Posizioni con occupazione (scheda più recente) ed esito ultima scansione
    cur.execute(_Q_DISPLAY_POSITIONS, (area, deposit))
    cols = [d[0] for d in cur.description]
    by_code = {}
    for row in cur.fetchall():
        d = {c: row[i] for i, c in enumerate(cols)}
        by_code[d["PositionCode"]] = d
    for p in pallets:
        prefix = p["code"]
        p["positions"] = [by_code.get(f"{prefix}{col}{level}") or
                          {"PositionCode": f"{prefix}{col}{level}", "LabelCode": None,
                           "ScanResult": None}
                          for col in COLUMNS for level in LEVELS]

    # Conteggi dashboard (per area+deposit)
    cur.execute(
        """SELECT COUNT(DISTINCT wl.PalletNumber),
                  COUNT(DISTINCT wl.LocationId),
                  COUNT(wb.BoardKanbanId),
                  COUNT(DISTINCT wb.OrderNumber),
                  COUNT(DISTINCT wb.ProductCode)
           FROM Traceability_RS.ind.WipKanbanLocations wl
           LEFT JOIN Traceability_RS.ind.WipKanbanBoards wb
                  ON wb.LocationId = wl.LocationId AND wb.DateOut IS NULL
           WHERE wl.Area = ? AND wl.Deposit = ?""",
        (area, deposit),
    )
    n_pallets, n_positions, n_boards, n_orders, n_products = cur.fetchone()

    # Movimenti IN/OUT di oggi (area ricavata dalla prima lettera del PositionCode)
    cur.execute(
        """SELECT Action, COUNT(*)
           FROM Traceability_RS.ind.WipKanbanAudit
           WHERE Action IN ('IN', 'OUT')
             AND CAST(DateIn AS DATE) = CAST(GETDATE() AS DATE)
             AND LEFT(PositionCode, 1) = ?
           GROUP BY Action""",
        (letter,),
    )
    today = {"IN": 0, "OUT": 0}
    for action, n in cur.fetchall():
        today[action] = int(n)

    # Ultima operazione IN/OUT (sempre per questa area)
    cur.execute(
        """SELECT TOP 1 Action, LabelCode, PositionCode, OrderNumber,
                  ProductCode, [User], DateIn
           FROM Traceability_RS.ind.WipKanbanAudit
           WHERE Action IN ('IN', 'OUT') AND LEFT(PositionCode, 1) = ?
           ORDER BY DateIn DESC""",
        (letter,),
    )
    row = cur.fetchone()
    last = None
    if row:
        last = {"Action": row[0], "LabelCode": row[1], "PositionCode": row[2],
                "OrderNumber": row[3], "ProductCode": row[4], "User": row[5],
                "DateIn": _iso(row[6])}

    return {
        "area": area,
        "deposit": deposit,
        "pallets": pallets,
        "counts": {
            "pallets": int(n_pallets or 0),
            "positions": int(n_positions or 0),
            "boards": int(n_boards or 0),
            "orders": int(n_orders or 0),
            "products": int(n_products or 0),
            "in_today": today["IN"],
            "out_today": today["OUT"],
        },
        "last_operation": last,
    }
