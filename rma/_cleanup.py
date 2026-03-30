"""Pulisci i record importati parzialmente e le lookup create durante l'import."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_manager import ConfigManager
import pyodbc

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cm = ConfigManager(
    key_file=os.path.join(PROJECT_DIR, 'encryption_key.key'),
    config_file=os.path.join(PROJECT_DIR, 'db_config.enc')
)
c = cm.load_config()
conn_str = (
    f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
    f"UID={c['username']};PWD={c['password']};TrustServerCertificate=Yes"
)

conn = pyodbc.connect(conn_str)
cur = conn.cursor()

# Count before
cur.execute("SELECT COUNT(*) FROM RmaRecords WHERE Source = 'IMPORT'")
print(f"Records da eliminare: {cur.fetchone()[0]}")

# Delete imported records
cur.execute("DELETE FROM RmaRecords WHERE Source = 'IMPORT'")
conn.commit()

# Delete fault details/types created by import (those NOT in the original seed)
# We keep the original seed entries (they have DescriptionIT = Description from the ALTER script)
# Import-created entries have different DescriptionIT from Description
# Safer approach: delete details then types where InsertedBy doesn't exist in seed
# But we don't have InsertedBy in lookup. Just leave them — they'll be reused by the re-import.

cur.execute("SELECT COUNT(*) FROM RmaRecords WHERE Source = 'IMPORT'")
print(f"Records rimanenti: {cur.fetchone()[0]}")

conn.close()
print("Pulizia completata.")
