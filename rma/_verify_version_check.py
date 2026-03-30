import os, sys
sys.path.insert(0, r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation')
from config_manager import ConfigManager
import pyodbc

cm = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
c = cm.load_config()
conn_str = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={};TrustServerCertificate=Yes".format(
    c['driver'], c['server'], c['database'], c['username'], c['password'])
conn = pyodbc.connect(conn_str)
cur = conn.cursor()

# Columns
cur.execute("SELECT TOP 1 * FROM traceability_rs.dbo.SwVersions")
cols = [d[0] for d in cur.description]
print("COLS:", cols)

# Active records
cur.execute("SELECT NameProgram, Version, MainPath, ISNULL(Must,0) as Must FROM traceability_rs.dbo.SwVersions WHERE dateout IS NULL")
rows = cur.fetchall()
for r in rows:
    print(f"ACTIVE: {r.NameProgram} | v{r.Version} | Must={r.Must} | Path={r.MainPath}")

# Check for DocumentManagement.exe
app_name = "DocumentManagement.exe"
app_ver = "2.3.9.8.1"
cur.execute("SELECT Version, MainPath, ISNULL(Must,0) as Must FROM traceability_rs.dbo.SwVersions WHERE NameProgram=? AND dateout IS NULL", app_name)
r = cur.fetchone()
if r:
    from packaging import version
    need = version.parse(r.Version) > version.parse(app_ver)
    print(f"APP={app_ver} DB={r.Version} NEED_UPDATE={need} PATH_EXISTS={os.path.exists(r.MainPath)}")
    if os.path.exists(r.MainPath):
        exe = os.path.join(r.MainPath, app_name)
        print(f"EXE_EXISTS={os.path.exists(exe)}")
else:
    print(f"NO RECORD for {app_name}")
    cur.execute("SELECT DISTINCT NameProgram FROM traceability_rs.dbo.SwVersions WHERE dateout IS NULL")
    print("REGISTERED:", [r[0] for r in cur.fetchall()])
conn.close()
