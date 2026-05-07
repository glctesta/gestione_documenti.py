import pyodbc, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from config_manager import ConfigManager

cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
creds = cfg.load_config()
conn_str = f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};UID={creds['username']};PWD={creds['password']}"
conn = pyodbc.connect(conn_str)
cur = conn.cursor()

# 1. Ordine PR0000335
cur.execute("""
    SELECT o.IDOrder, o.OrderNumber, op.IDPhase,
           ft.FaiTemplateId, ft.FaiTitle, ft.Autocheck
    FROM Traceability_RS.dbo.Orders o
    INNER JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrder = o.IDOrder
    LEFT JOIN Traceability_RS.fai.FaiTemplates ft ON ft.IdPhase = op.IDPhase
    WHERE o.OrderNumber = 'PR0000335'
""")
print("=== Ordine PR0000335: Fasi e Template FAI ===")
for r in cur.fetchall():
    print(f"  IDOrder={r[0]}, Phase={r[2]}, TemplateId={r[3]}, Title={r[4]}, Autocheck={r[5]}")

# 2. Ordine PR0000350
cur.execute("""
    SELECT o.IDOrder, o.OrderNumber, op.IDPhase,
           ft.FaiTemplateId, ft.FaiTitle, ft.Autocheck
    FROM Traceability_RS.dbo.Orders o
    INNER JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrder = o.IDOrder
    LEFT JOIN Traceability_RS.fai.FaiTemplates ft ON ft.IdPhase = op.IDPhase
    WHERE o.OrderNumber = 'PR0000350'
""")
print("\n=== Ordine PR0000350: Fasi e Template FAI ===")
for r in cur.fetchall():
    print(f"  IDOrder={r[0]}, Phase={r[2]}, TemplateId={r[3]}, Title={r[4]}, Autocheck={r[5]}")

# 3. Template Autocheck=1
cur.execute("""
    SELECT FaiTemplateId, FaiTitle, IdPhase, Autocheck
    FROM Traceability_RS.fai.FaiTemplates
    WHERE Autocheck = 1
""")
print("\n=== Template con Autocheck=1 ===")
for r in cur.fetchall():
    print(f"  TemplateId={r[0]}, Title={r[1]}, Phase={r[2]}")

conn.close()
