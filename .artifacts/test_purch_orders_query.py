# -*- coding: utf-8 -*-
"""Test query tab 'Ordini di acquisto' su DB reale."""
import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
conn_str = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
            f"UID={creds['username']};PWD={creds['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")

cnxn = pyodbc.connect(conn_str, autocommit=False)
cnxn.timeout = 120
cur = cnxn.cursor()
cur.execute("""
    SELECT TOP 20 l.DataConferma, l.ConfermatoDa, m.CodiceMateriale, m.DescrizioneMateriale,
           ISNULL(t.Tipo, 'Generico') AS Tipo, l.QtaSuggerita, l.QtaOrdinata, l.NumeroPO,
           l.DataPrevistaArrivo, l.DataInvio, l.Stato
    FROM ind.RiordineEmailLog l
    JOIN ind.Materiali m ON l.MaterialeId = m.MaterialeId
    LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
    WHERE l.Stato = 'CONFERMATO'
    ORDER BY l.DataConferma DESC
""")
rows = cur.fetchall()
print(f"CONFERMATI: {len(rows)} righe")
for r in rows[:10]:
    print(tuple(str(x)[:28] for x in r))

cur.execute("SELECT Stato, COUNT(*) FROM ind.RiordineEmailLog GROUP BY Stato")
print("Stati:", cur.fetchall())
cur.close(); cnxn.close()
