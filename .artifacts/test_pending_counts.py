import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
cs = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
      f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes")
cn = pyodbc.connect(cs, autocommit=True)
cur = cn.cursor()

cur.execute("""SELECT COUNT(*) FROM Traceability_RS.ind.RiordineEmailLog
               WHERE Stato = 'INVIATO' AND DataInvio >= DATEADD(DAY, -60, GETDATE())""")
print("INVIATO ultimi 60gg (popup):", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM Traceability_RS.ind.MaterialiRichieste")
print("MaterialiRichieste (tab Dettaglio):", cur.fetchone()[0])

# Verifica acquisti: materiali distinti in RiordineEmailLog
cur.execute("SELECT COUNT(DISTINCT MaterialeId) FROM Traceability_RS.ind.RiordineEmailLog")
print("Materiali distinti in RiordineEmailLog (tab Verifica acquisti):", cur.fetchone()[0])

cur.execute("""SELECT COUNT(*) FROM Traceability_RS.ind.RiordineEmailLog
               WHERE Stato = 'INVIATO'""")
print("INVIATO totali (senza finestra 60gg):", cur.fetchone()[0])

# il tab Verifica acquisti ha filtri data? guarda come filtra (lo verifico via codice)
cur.close(); cn.close()
