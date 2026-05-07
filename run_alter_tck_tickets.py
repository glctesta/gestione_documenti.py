"""
run_alter_tck_tickets.py
Esegue lo script SQL alter_tck_tickets.sql sul database.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
import pyodbc

cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
creds = cfg.load_config()
conn_str = (
    f"DRIVER={creds['driver']};"
    f"SERVER={creds['server']};"
    f"DATABASE={creds['database']};"
    f"UID={creds['username']};"
    f"PWD={creds['password']};"
    "MARS_Connection=Yes;TrustServerCertificate=Yes"
)
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

sql_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alter_tck_tickets.sql')
with open(sql_file, 'r', encoding='utf-8') as f:
    sql = f.read()

# Split by GO on its own line
import re
batches = re.split(r'^\s*GO\s*$', sql, flags=re.MULTILINE | re.IGNORECASE)

for i, batch in enumerate(batches):
    batch = batch.strip()
    if not batch or batch.startswith('--'):
        continue
    # Remove comment-only lines
    lines = [l for l in batch.splitlines() if l.strip() and not l.strip().startswith('--')]
    if not lines:
        continue
    try:
        cursor.execute(batch)
        print(f"Batch {i+1}: OK")
    except Exception as e:
        print(f"Batch {i+1}: ERROR - {e}")

conn.close()
print("=== alter_tck_tickets.sql eseguito con successo ===")
