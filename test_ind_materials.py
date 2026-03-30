"""Test diretto della query materiali indiretti usando ConfigManager."""
import sys, os
sys.path.insert(0, r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation')

# Disable tkinter
os.environ['DISPLAY'] = ''

import pyodbc, threading
from config_manager import ConfigManager

config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
db_credentials = config_mgr.load_config()
DB_CONN_STR = (f"DRIVER={db_credentials['driver']};SERVER={db_credentials['server']};"
               f"DATABASE={db_credentials['database']};UID={db_credentials['username']};"
               f"PWD={db_credentials['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")

conn = pyodbc.connect(DB_CONN_STR, autocommit=True)
cursor = conn.cursor()

# Test 1: count
cursor.execute('SELECT COUNT(*) FROM ind.Materiali WHERE IsActive = 1')
print(f"Materiali attivi: {cursor.fetchone()[0]}")

# Test 2: full query (identica alla form)
query = """
    SELECT m.MaterialeId, m.CodiceMateriale, m.DescrizioneMateriale,
           ISNULL(t.Tipo, 'Generico') AS Tipo,
           ISNULL(s.Qty, 0) AS QtaStock,
           ISNULL(t.QtaConfezione, 1) AS QtaConfezione,
           ISNULL(t.IsFrazionabile, 0) AS IsFrazionabile,
           t.TipoMaterialeId
    FROM ind.Materiali m
    LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
    LEFT JOIN ind.MaterialiStock s ON m.MaterialeId = s.MaterialeId AND s.DateOut IS NULL
    WHERE m.IsActive = 1
    ORDER BY m.CodiceMateriale
"""
try:
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Query form: {len(rows)} risultati")
    for r in rows[:5]:
        print(f"  ID={r[0]} | Codice={r[1]} | Desc={r[2]} | Tipo={r[3]}")
except Exception as e:
    print(f"ERRORE query: {e}")

conn.close()
print("DONE")
