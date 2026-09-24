# -*- coding: utf-8 -*-
"""Test completo kanban_logic su DB reale + generazione PDF. Pulizia alla fine."""
import pyodbc
from config_manager import ConfigManager
from wip_kanban import kanban_logic, pdf_gen

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
cs = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
      f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes;MARS_Connection=Yes")
cn = pyodbc.connect(cs, autocommit=False)
cn.timeout = 120
cur = cn.cursor()

# verifica tabelle
cur.execute("""SELECT t.name FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id
               WHERE s.name='ind' AND t.name LIKE 'WipKanban%'""")
print("Tabelle:", [r[0] for r in cur.fetchall()])

# LabelCode reale
cur.execute("SELECT TOP 1 LabelCod FROM Traceability_RS.dbo.LabelCodes ORDER BY IDLabelCode DESC")
label = cur.fetchone()[0]
print("LabelCode di test:", label)

try:
    # 1. creazione locazioni
    m1 = kanban_logic.create_location(cur, "WIP", "TEST")
    m2 = kanban_logic.create_location(cur, "REPAIR", "TEST")
    print("Creati master:", m1, m2)
    assert m1 == "WP1" and m2 == "RP1", (m1, m2)
    positions = kanban_logic.list_positions(cur, m1)
    print(f"Posizioni {m1}: {len(positions)} -> {positions[0]} ... {positions[-1]}")
    assert len(positions) == 16 and positions[0] == "WP1A1" and positions[-1] == "WP1D4"

    # 2. board_info
    info = kanban_logic.board_info(cur, label)
    print("Board info:", {k: str(v)[:30] for k, v in (info or {}).items()})
    assert info, "LabelCode non risolto"

    # 3. caricamento scheda
    ok, err, _ = kanban_logic.load_board(cur, "WP1A1", label, "TEST")
    print("Load:", ok, err)
    assert ok
    ok, err, dup = kanban_logic.load_board(cur, "WP1A2", label, "TEST")
    print("Load duplicato:", ok, err, dup)
    assert not ok and err == "board_already_in"

    # 4. boards nella posizione + conteggi
    boards = kanban_logic.boards_in_position(cur, "WP1A1")
    print("Boards in WP1A1:", [(b['LabelCode'], b['OrderNumber'], b['ScanResult']) for b in boards])
    c = kanban_logic.counts(cur)
    print("Counts:", c)
    assert c["boards"] == 1 and c["wip"] == 1 and c["repair"] == 1

    # 5. ricerca
    locs = kanban_logic.search_locations(cur, order=boards[0]["OrderNumber"])
    print("Search per ordine:", [(l["PositionCode"], l["LabelCode"]) for l in locs])
    assert any(l["PositionCode"] == "WP1A1" for l in locs)
    locs2 = kanban_logic.search_locations(cur, product=boards[0]["ProductCode"])
    print("Search per prodotto:", [(l["PositionCode"], l["LabelCode"]) for l in locs2])

    # 6. prelievo
    ok, err, wi = kanban_logic.withdraw_board(cur, label, "TEST2")
    print("Withdraw:", ok, wi)
    assert ok and wi["position"] == "WP1A1"
    ok, err, _ = kanban_logic.withdraw_board(cur, label, "TEST2")
    print("Withdraw di nuovo:", ok, err)
    assert not ok and err == "not_in_kanban"

    # 7. PDF
    p1 = pdf_gen.labels_pdf(kanban_logic.list_positions(cur, m1))
    rows = kanban_logic.list_all_boards(cur)
    p2 = pdf_gen.list_pdf(rows, title="Test lista kanban")
    import os
    print("PDF labels:", p1, os.path.getsize(p1), "bytes")
    print("PDF lista:", p2, os.path.getsize(p2), "bytes, righe:", len(rows))

    cn.rollback()
    print("ROLLBACK dati di test.")
except Exception:
    cn.rollback()
    raise
finally:
    cur.close(); cn.close()
print("TEST OK")
