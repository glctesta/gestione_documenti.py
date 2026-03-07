"""Inserisce setting Sys_email_overtimeNotAuth se non esiste."""
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
cur.execute("""
    IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'Sys_email_overtimeNotAuth')
    INSERT INTO traceability_rs.dbo.settings (atribute, [value])
    VALUES ('Sys_email_overtimeNotAuth', 'gianluca.testa@vandewiele.com')
""")
conn.commit()
print("Setting Sys_email_overtimeNotAuth inserito/verificato.")
conn.close()
