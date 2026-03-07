"""Check AutorizedUsers table for manage_check_rules entries."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config_manager import ConfigManager
import pyodbc

cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
c = cfg.load_config()
conn = pyodbc.connect(
    f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
    f"UID={c['username']};PWD={c['password']};TrustServerCertificate=Yes"
)
cur = conn.cursor()

# Check manage_check_rules
cur.execute("SELECT * FROM dbo.AutorizedUsers WHERE TranslationKey = 'manage_check_rules'")
rows = cur.fetchall()
print(f"=== manage_check_rules: {len(rows)} rows ===")
for r in rows:
    print(r)

print()

# Check manage_product_check  
cur.execute("SELECT * FROM dbo.AutorizedUsers WHERE TranslationKey = 'manage_product_check'")
rows2 = cur.fetchall()
print(f"=== manage_product_check: {len(rows2)} rows ===")
for r in rows2:
    print(r)

print()

# Check submenu_permissions (working reference)
cur.execute("SELECT TOP 3 * FROM dbo.AutorizedUsers WHERE TranslationKey = 'submenu_permissions'")
rows3 = cur.fetchall()
print(f"=== submenu_permissions: {len(rows3)} rows ===")
for r in rows3:
    print(r)

print()

# Check columns
cur.execute("SELECT TOP 1 * FROM dbo.AutorizedUsers")
cols = [d[0] for d in cur.description]
print(f"Columns: {cols}")

conn.close()
