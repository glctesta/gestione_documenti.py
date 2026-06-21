# -*- coding: utf-8 -*-
"""Test E2E AUTO-PULENTE del percorso scarico su PRELEVATA.
Crea una richiesta di test, esegue lo scarico, verifica giacenza/idempotenza,
poi ELIMINA i dati di test (movimento + richiesta). Nessuna email.
Esegui: python test_scarico_e2e.py
"""
import sys, os, threading
sys.path.insert(0, r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation')
os.environ['DISPLAY'] = ''

import pyodbc
from config_manager import ConfigManager

cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
CONN = (f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")


class DBShim:
    def __init__(self, conn_str):
        self.conn = pyodbc.connect(conn_str, autocommit=True)
        self.cursor = self.conn.cursor()
        self._lock = threading.RLock()
    def _ensure_connection(self): pass
    def fetch_all(self, q, p=None):
        with self._lock:
            self.cursor.execute(q, p) if p else self.cursor.execute(q)
            return self.cursor.fetchall() if self.cursor.description else []
    def fetch_one(self, q, p=None):
        with self._lock:
            self.cursor.execute(q, p) if p else self.cursor.execute(q)
            return self.cursor.fetchone() if self.cursor.description else None


def giacenza(db, mid):
    row = db.fetch_one("SELECT Giacenza FROM ind.vw_GiacenzaCorrente WHERE MaterialeId = ?", (mid,))
    return float(row[0]) if row and row[0] is not None else 0.0


def main():
    db = DBShim(CONN)
    import indirect_materials_stock_data as sd

    # Materiale di test
    row = db.fetch_one("SELECT TOP 1 MaterialeId, CodiceMateriale FROM ind.Materiali WHERE IsActive = 1 ORDER BY MaterialeId")
    mid, codice = row[0], row[1]
    g0 = giacenza(db, mid)
    print(f"Materiale test: {codice} (id={mid}) — giacenza iniziale = {g0:.2f}")

    rid = None
    try:
        # 1) Crea richiesta di test (qty 1) in stato RICHIESTA
        db.cursor.execute(
            "INSERT INTO ind.MaterialiRichieste "
            "(MaterialeId, QtaRichiesta, QtaStockAlMomento, Stato, DataRichiesta, RichiestoDa) "
            "OUTPUT INSERTED.RichiestaId VALUES (?, 1, ?, 'RICHIESTA', GETDATE(), 'TEST_E2E')",
            (mid, g0))
        rid = db.cursor.fetchone()[0]
        print(f"1) Creata richiesta test RichiestaId={rid} (qty 1)")

        # 2) Scarico su PRELEVATA
        ok, code = sd.registra_scarico_richiesta(db, rid, 'TEST_E2E')
        print(f"2) registra_scarico_richiesta -> ok={ok} code={code}")
        assert ok and code == 'ok', "Scarico fallito"

        # 3) Verifica stato + giacenza
        st = db.fetch_one("SELECT Stato, DataPrelievo FROM ind.MaterialiRichieste WHERE RichiestaId = ?", (rid,))
        g1 = giacenza(db, mid)
        print(f"3) Stato richiesta={st[0]} DataPrelievo={st[1]} | giacenza ora={g1:.2f} (attesa {g0-1:.2f})")
        assert st[0] == 'PRELEVATA', "Stato non PRELEVATA"
        assert abs(g1 - (g0 - 1)) < 1e-6, "Giacenza non decrementata correttamente"

        # 4) Idempotenza: secondo scarico non deve duplicare
        ok2, code2 = sd.registra_scarico_richiesta(db, rid, 'TEST_E2E')
        nmov = db.fetch_one("SELECT COUNT(*) FROM ind.MaterialiMovimenti WHERE RichiestaId = ? AND TipoMovimento='SCARICO'", (rid,))[0]
        print(f"4) Secondo scarico -> ok={ok2} code={code2} | movimenti SCARICO per richiesta={nmov} (atteso 1)")
        assert code2 == 'already' and nmov == 1, "Idempotenza non rispettata"

        print("\n>>> TEST E2E SUPERATO <<<")
    finally:
        # Pulizia: elimina movimento di test poi la richiesta
        if rid is not None:
            try:
                db.cursor.execute("DELETE FROM ind.MaterialiMovimenti WHERE RichiestaId = ?", (rid,))
                db.cursor.execute("DELETE FROM ind.MaterialiRichieste WHERE RichiestaId = ?", (rid,))
                gz = giacenza(db, mid)
                print(f"Pulizia completata. Giacenza ripristinata = {gz:.2f} (iniziale {g0:.2f})")
            except Exception as e:
                print(f"ATTENZIONE: pulizia fallita per RichiestaId={rid}: {e}")
        db.conn.close()


if __name__ == "__main__":
    main()
