import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config_manager import ConfigManager
import pyodbc
cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
c = cfg.load_config()
conn = pyodbc.connect(f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};UID={c['username']};PWD={c['password']};TrustServerCertificate=Yes")
cur = conn.cursor()
cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='Registry' AND TABLE_CATALOG='employee' ORDER BY ORDINAL_POSITION")
rows = cur.fetchall()
if rows:
    print("employee.dbo.Registry columns:")
    for r in rows:
        print(f"  {r[0]}")
else:
    print("Table not found or no columns. Trying ResetServices...")
    cur.execute("SELECT COLUMN_NAME FROM ResetServices.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='TbRegistro' ORDER BY ORDINAL_POSITION")
    for r in cur.fetchall():
        print(f"  {r[0]}")
conn.close()
