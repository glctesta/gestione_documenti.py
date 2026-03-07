"""Insert manage_check_rules + manage_product_check authorization for same users as submenu_permissions."""
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

# Get all authorized users for submenu_permissions (reference)
cur.execute("""
    SELECT Employeehirehistoryid FROM dbo.AutorizedUsers 
    WHERE TranslationKey = 'submenu_permissions' AND DateOut IS NULL
""")
users = [r[0] for r in cur.fetchall()]
print(f"Users authorized for submenu_permissions: {users}")

# Insert for manage_check_rules
count = 0
for emp_id in users:
    cur.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM dbo.AutorizedUsers 
            WHERE Employeehirehistoryid = ? AND TranslationKey = 'manage_check_rules' AND DateOut IS NULL
        )
        INSERT INTO dbo.AutorizedUsers (Employeehirehistoryid, TranslationKey, DateIn)
        VALUES (?, 'manage_check_rules', GETDATE())
    """, emp_id, emp_id)
    count += 1

# Insert for manage_product_check
for emp_id in users:
    cur.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM dbo.AutorizedUsers 
            WHERE Employeehirehistoryid = ? AND TranslationKey = 'manage_product_check' AND DateOut IS NULL
        )
        INSERT INTO dbo.AutorizedUsers (Employeehirehistoryid, TranslationKey, DateIn)
        VALUES (?, 'manage_product_check', GETDATE())
    """, emp_id, emp_id)
    count += 1

conn.commit()
print(f"Inserted {count} authorization entries for manage_check_rules + manage_product_check")

# Verify
cur.execute("SELECT * FROM dbo.AutorizedUsers WHERE TranslationKey IN ('manage_check_rules', 'manage_product_check') AND DateOut IS NULL")
rows = cur.fetchall()
print(f"\nVerification - {len(rows)} active entries:")
for r in rows:
    print(f"  ID={r[0]}, Key={r[1]}, EmpHH={r[2]}")

conn.close()
