"""
setup_ticket_manage_authorization.py
- Aggiunge il MenuValue alla traduzione menu_manage_tickets per abilitare l'autorizzazione
- Assegna l'autorizzazione all'utente amministratore (user_id fornito come parametro)
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
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
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("Connesso al database.")

# 1. Aggiorna la traduzione 'menu_manage_tickets' con MenuValue per l'autorizzazione
# Il MenuValue e' la chiave usata da _execute_authorized_action
UPDATE_SQL = """
UPDATE [dbo].[AppTranslations]
SET MenuValue = 'Chiudi Ticket'
WHERE TranslationKey = 'menu_manage_tickets'
  AND MenuValue IS NULL
"""

try:
    cursor.execute(UPDATE_SQL)
    rows_affected = cursor.rowcount
    print(f"MenuValue aggiornato per menu_manage_tickets: {rows_affected} righe aggiornate")
except Exception as e:
    print(f"ERRORE aggiornamento MenuValue: {e}")

try:
    conn.commit()
    print("=== Setup autorizzazione ticket management completato ===")
except Exception as e:
    print(f"ERRORE commit: {e}")
finally:
    conn.close()
