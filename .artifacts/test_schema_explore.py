# -*- coding: utf-8 -*-
"""Esplora schema: Orders (stato chiusura?) e BomIndirectMaterials (associazioni)."""
import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
conn_str = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
            f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes")
cnxn = pyodbc.connect(conn_str, autocommit=True)
cur = cnxn.cursor()

print("=== dbo.Orders colonne (candidate stato) ===")
cur.execute("""SELECT c.name, t.name FROM sys.columns c
    JOIN sys.tables tb ON c.object_id = tb.object_id
    JOIN sys.schemas s ON tb.schema_id = s.schema_id
    JOIN sys.types t ON c.user_type_id = t.user_type_id
    WHERE s.name='dbo' AND tb.name='Orders' ORDER BY c.column_id""")
for r in cur.fetchall():
    print(" ", r[0], r[1])

print("=== ind.BomIndirectMaterials colonne ===")
cur.execute("""SELECT c.name, t.name FROM sys.columns c
    JOIN sys.tables tb ON c.object_id = tb.object_id
    JOIN sys.schemas s ON tb.schema_id = s.schema_id
    JOIN sys.types t ON c.user_type_id = t.user_type_id
    WHERE s.name='ind' AND tb.name='BomIndirectMaterials' ORDER BY c.column_id""")
for r in cur.fetchall():
    print(" ", r[0], r[1])

cur.close(); cnxn.close()
