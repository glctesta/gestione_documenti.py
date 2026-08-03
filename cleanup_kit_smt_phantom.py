# -*- coding: utf-8 -*-
"""
cleanup_kit_smt_phantom.py — rimuove le righe fantasma SMT dalle liste di kit.

Perche' esistono: il filtro SMT era applicato solo all'IMPORT del file Essegi e
ai conteggi di chiusura, ma NON al confronto con la BOM. Risultato: ogni codice
SMT della BOM veniva reinserito in picking_list_items come MISSING_FROM_LIST con
quantita' 0 — righe rosse che l'operatore vedeva senza poterle verificare.
Il filtro e' ora unico (kit_wh_logic.SQL_NOT_SMT, usato anche in
bom_codes_for_orders): questo script ripulisce le righe gia' create.

Le righe NON vengono cancellate ma marcate REMOVED (audit preservato) e solo
sulle liste ancora aperte; le liste chiuse restano storia.

Run:  python cleanup_kit_smt_phantom.py           (mostra cosa farebbe)
      python cleanup_kit_smt_phantom.py --apply   (applica)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from database_config import DatabaseConfig

SELECT_PHANTOM = """
SELECT i.id, i.picking_list_id, l.status, i.order_number, i.material_code,
       c.ComponentDescription
FROM Traceability_RS.dbo.picking_list_items i
INNER JOIN Traceability_RS.dbo.picking_lists l ON l.id = i.picking_list_id
INNER JOIN Traceability_RS.dbo.Components c ON c.ComponentCode = i.material_code
WHERE i.pick_status = 'MISSING_FROM_LIST'
  AND ISNULL(i.qty_picked, 0) = 0
  AND (i.unique_number IS NULL OR LTRIM(RTRIM(i.unique_number)) = '')
  AND c.ComponentDescription LIKE '%SMT%'
"""


def main(apply_changes: bool):
    conn = pyodbc.connect(DatabaseConfig().get_connection_string(), timeout=60)
    cur = conn.cursor()

    cur.execute(SELECT_PHANTOM + " ORDER BY i.picking_list_id, i.material_code")
    rows = cur.fetchall()
    open_rows = [r for r in rows if (r.status or '').upper() not in ('CLOSED', 'PARTIAL')]

    print(f"Righe fantasma SMT totali : {len(rows)}")
    print(f"   su liste ancora aperte : {len(open_rows)}")
    by_list = {}
    for r in open_rows:
        by_list.setdefault((r.picking_list_id, r.status), []).append(r.material_code)
    for (lid, st), codes in sorted(by_list.items()):
        print(f"   lista {lid} ({st}): {len(codes)} righe — es. {', '.join(codes[:3])}")

    if not apply_changes:
        print("\n[DRY-RUN] Nessuna modifica. Rilanciare con --apply per applicare.")
        conn.close()
        return

    ids = [r.id for r in open_rows]
    updated = 0
    CHUNK = 500
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i:i + CHUNK]
        ph = ','.join('?' * len(chunk))
        cur.execute(
            "UPDATE Traceability_RS.dbo.picking_list_items "
            "SET pick_status = 'REMOVED', "
            "    notes = LEFT(ISNULL(notes,'') + ' [rimossa: componente SMT, "
            "non fa parte del kit PTH]', 500) "
            f"WHERE id IN ({ph})", chunk)
        updated += cur.rowcount
    conn.commit()
    conn.close()
    print(f"\n[OK] Righe marcate REMOVED: {updated}")


if __name__ == '__main__':
    main(apply_changes='--apply' in sys.argv)
