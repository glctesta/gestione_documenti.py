# -*- coding: utf-8 -*-
"""Smoke test READ-ONLY del layer dati giacenze/consumi.
Verifica che vista, tabelle e query funzionino sul DB reale.
Non invia email e non modifica dati.
Esegui: python test_stock_smoke.py
"""
import sys, os, threading
sys.path.insert(0, r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation')
os.environ['DISPLAY'] = ''

import pyodbc
from config_manager import ConfigManager

config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
c = config_mgr.load_config()
CONN = (f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
        f"UID={c['username']};PWD={c['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")


class DBShim:
    """Wrapper minimale compatibile con le funzioni del layer dati."""
    def __init__(self, conn_str):
        self.conn = pyodbc.connect(conn_str, autocommit=True)
        self.cursor = self.conn.cursor()
        self._lock = threading.RLock()

    def _ensure_connection(self):
        pass

    def fetch_all(self, query, params=None):
        with self._lock:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            if self.cursor.description is None:
                return []
            return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        with self._lock:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            if self.cursor.description is None:
                return None
            return self.cursor.fetchone()

    def fetch_setting(self, attribute):
        row = self.fetch_one(
            "SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = ?",
            (attribute,))
        return row[0] if row else None


def main():
    db = DBShim(CONN)
    import indirect_materials_stock_data as sd
    import indirect_materials_consumption as cons

    print("=" * 60)
    print("1) GIACENZE (vista vw_GiacenzaCorrente)")
    giac = sd.get_giacenze(db)
    print(f"   Materiali con giacenza: {len(giac)}")
    for r in giac[:5]:
        print(f"   - {r['codice']:<16} giac={r['giacenza']:>10.2f} "
              f"min={r['livello_minimo']} attivo={r['is_riordino_attivo']} "
              f"sotto={r['sotto_soglia']}")

    print("\n2) SOTTO SCORTA MINIMA")
    below = sd.get_giacenze(db, only_below=True)
    print(f"   Codici sotto soglia: {len(below)}")
    for r in below[:5]:
        print(f"   - {r['codice']:<16} giac={r['giacenza']:.2f} < min={r['livello_minimo']:.2f}")

    print("\n3) MOVIMENTI primo materiale")
    if giac:
        mid = giac[0]['materiale_id']
        movs = sd.get_movimenti(db, mid, limit=5)
        print(f"   Materiale {giac[0]['codice']}: {len(movs)} movimenti (ultimi 5)")
        for m in movs:
            print(f"   - {m['data']} {m['tipo']:<10} {m['qty']:+.2f} {m['note']}")

    print("\n4) CONFIG SCORTA MINIMA primo materiale")
    if giac:
        cfg = sd.get_min_config(db, giac[0]['materiale_id'])
        print(f"   {cfg}")

    print("\n5) CONSUMI mensili / settimanali / annuali")
    print(f"   Settimanali (righe): {len(cons.get_weekly_consumption(db))}")
    print(f"   Mensili (righe):     {len(cons.get_monthly_consumption(db))}")
    yr = cons.get_yearly_consumption(db)
    print(f"   Annuali (righe):     {len(yr)}")
    for r in yr:
        print(f"   - {r['anno']}: consumo={r['consumo']:.2f} movimenti={r['n_mov']}")

    print("\n6) BUDGET anno prossimo (top 5)")
    bud = cons.get_budget_proposal(db, growth_pct=5.0)
    print(f"   Codici con consumo 12m: {len(bud)}")
    for r in bud[:5]:
        print(f"   - {r['codice']:<16} 12m={r['consumo_12m']:.2f} "
              f"budget_anno={r['budget_annuo']:.2f} mese={r['budget_mensile']:.2f}")

    print("\n7) DESTINATARI RIORDINO (sys_email_acquista_indiretti)")
    rec = sd._get_reorder_recipients(db)
    print(f"   Destinatari configurati: {rec if rec else 'NESSUNO (configurare in Settings)'}")

    print("\n" + "=" * 60)
    print("SMOKE TEST OK (nessuna email inviata, nessun dato modificato)")
    db.conn.close()


if __name__ == "__main__":
    main()
