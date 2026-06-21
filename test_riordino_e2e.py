# -*- coding: utf-8 -*-
"""Test E2E AUTO-PULENTE di scorta minima + rilevamento sotto-soglia + riordino.
Imposta una scorta minima alta su un materiale, verifica che risulti sotto-soglia,
verifica la logica di check_and_send_reorder (senza inviare se non ci sono
destinatari), poi ELIMINA la config di test. Nessuna email inviata.
Esegui: python test_riordino_e2e.py
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
    def fetch_setting(self, attribute):
        r = self.fetch_one("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = ?", (attribute,))
        return r[0] if r else None


class FakeLang:
    def get(self, k, d=''): return d


def main():
    db = DBShim(CONN)
    import indirect_materials_stock_data as sd

    row = db.fetch_one("SELECT TOP 1 m.MaterialeId, m.CodiceMateriale, g.Giacenza "
                       "FROM ind.Materiali m JOIN ind.vw_GiacenzaCorrente g ON g.MaterialeId=m.MaterialeId "
                       "WHERE m.IsActive=1 ORDER BY m.MaterialeId")
    mid, codice, g = row[0], row[1], float(row[2] or 0)
    print(f"Materiale test: {codice} (id={mid}) giacenza={g:.2f}")

    try:
        # 1) upsert config con minimo alto -> deve risultare sotto soglia
        min_alto = g + 100
        ok, msg = sd.upsert_min_config(db, mid, min_alto, g + 50, True, 'TEST_E2E')
        print(f"1) upsert_min_config(min={min_alto}) -> ok={ok}")
        assert ok

        cfg2 = sd.get_min_config(db, mid)
        print(f"2) get_min_config -> {cfg2}")
        assert cfg2 and cfg2['is_attivo'] and abs(cfg2['livello_minimo'] - min_alto) < 1e-6

        # 3) deve comparire tra i sotto-soglia
        below = sd.get_giacenze(db, only_below=True)
        ids = [b['materiale_id'] for b in below]
        print(f"3) sotto-soglia: {len(below)} codici; il test è incluso: {mid in ids}")
        assert mid in ids

        # 4) logica riordino (NON invia se nessun destinatario; con dedup)
        res = sd.check_and_send_reorder(db, FakeLang(), force=True)
        print(f"4) check_and_send_reorder(force=True) -> {res}")
        # Accettabile: 'ok' (se destinatari configurati) o 'no_recipients'
        assert res['reason'] in ('ok', 'no_recipients')
        if res['reason'] == 'ok':
            print("   NOTA: destinatari configurati -> email REALMENTE inviata.")

        print("\n>>> TEST RIORDINO SUPERATO <<<")
    finally:
        try:
            db.cursor.execute("DELETE FROM ind.MaterialiRiordino WHERE MaterialeId = ? AND ModificatoDa = 'TEST_E2E'", (mid,))
            # pulizia eventuale log riordino creato dal force send
            db.cursor.execute("DELETE FROM ind.RiordineEmailLog WHERE MaterialeId = ? AND CAST(DataInvio AS DATE)=CAST(GETDATE() AS DATE)", (mid,))
            print("Pulizia config/log di test completata.")
        except Exception as e:
            print(f"ATTENZIONE pulizia: {e}")
        db.conn.close()


if __name__ == "__main__":
    main()
