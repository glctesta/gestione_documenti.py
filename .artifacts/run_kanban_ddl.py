# -*- coding: utf-8 -*-
"""Esegue create_wip_kanban_tables.sql sul DB reale (idempotente)."""
import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
cs = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
      f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes")
cn = pyodbc.connect(cs, autocommit=True)
sql = open('sql/create_wip_kanban_tables.sql', encoding='utf-8').read()
cur = cn.cursor()
# sqlcmd-style GO separator
for batch in sql.split('\nGO'):
    batch = batch.strip()
    if batch:
        cur.execute(batch)
        while True:
            try:
                row = cur.fetchone()
                if not row:
                    break
                print(row[0])
            except pyodbc.ProgrammingError:
                break
cur.close(); cn.close()
print("DDL eseguito.")
