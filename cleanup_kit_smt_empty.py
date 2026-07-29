"""
cleanup_kit_smt_empty.py — Pulizia una-tantum delle liste di prelievo kit.

Elimina da dbo.picking_list_items le righe che d'ora in poi vengono già escluse
in import (vedi kit_preparation_gui._exclude_smt_and_empty):
  - righe SENZA reel code (unique_number vuoto/NULL);
  - codici SMT: material_code la cui descrizione in dbo.Components contiene 'SMT'.

Uso:
    python cleanup_kit_smt_empty.py            # DRY-RUN: mostra solo i conteggi
    python cleanup_kit_smt_empty.py --apply    # esegue davvero la cancellazione

DRY-RUN di default: non modifica nulla finché non passi --apply.
"""
import sys

from database_config import DatabaseConfig
import pyodbc

# NB: material_code (Essegi ITEM CODE) = dbo.Components.ComponentCode.
_EMPTY = "(unique_number IS NULL OR LTRIM(RTRIM(unique_number)) = '')"
_SMT = ("material_code IN (SELECT ComponentCode FROM Traceability_RS.dbo.Components "
        "WHERE ComponentDescription LIKE '%SMT%')")
_WHERE = f"({_EMPTY} OR {_SMT})"


def main(apply: bool):
    conn = pyodbc.connect(DatabaseConfig().get_connection_string(), timeout=60)  # autocommit=False
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM dbo.picking_list_items")
    tot = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM dbo.picking_list_items WHERE {_EMPTY}")
    n_empty = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM dbo.picking_list_items WHERE {_SMT}")
    n_smt = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM dbo.picking_list_items WHERE {_WHERE}")
    n_del = cur.fetchone()[0]

    print(f"Totale righe picking_list_items : {tot}")
    print(f"  senza reel code (empty)       : {n_empty}")
    print(f"  codici SMT (Components)        : {n_smt}")
    print(f"  DA ELIMINARE (unione)          : {n_del}")

    cur.execute(f"""
        SELECT pl.id, pl.status, COUNT(*) AS removed
        FROM dbo.picking_list_items i
        JOIN dbo.picking_lists pl ON pl.id = i.picking_list_id
        WHERE {_WHERE}
        GROUP BY pl.id, pl.status ORDER BY pl.id""")
    rows = cur.fetchall()
    print("\nListe impattate (id, stato, righe rimosse):")
    for r in rows:
        print(f"  #{r.id}  {r.status}  -> {r.removed}")

    if not apply:
        print("\n[DRY-RUN] Nessuna modifica eseguita. Rilancia con --apply per cancellare.")
        conn.close()
        return

    cur.execute(f"DELETE FROM dbo.picking_list_items WHERE {_WHERE}")
    deleted = cur.rowcount
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dbo.picking_list_items")
    tot_after = cur.fetchone()[0]
    print(f"\n[APPLICATO] Eliminate {deleted} righe. Totale ora: {tot_after}")
    conn.close()


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
