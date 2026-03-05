"""Run ALTER TABLE and INSERT setting for X-Ray verification feature."""
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

# 1. Add AttachmentDoc column
cur.execute("""
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = 'PeriodicalProductCheckLogs'
          AND COLUMN_NAME = 'AttachmentDoc'
    )
    ALTER TABLE [Traceability_RS].[dbo].[PeriodicalProductCheckLogs]
    ADD AttachmentDoc VARBINARY(MAX) NULL
""")
conn.commit()
print("1. AttachmentDoc column: OK")

# 2. Add PriodicalProductCheckListId column
cur.execute("""
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = 'PeriodicalProductCheckLogs'
          AND COLUMN_NAME = 'PriodicalProductCheckListId'
    )
    ALTER TABLE [Traceability_RS].[dbo].[PeriodicalProductCheckLogs]
    ADD PriodicalProductCheckListId INT NULL
""")
conn.commit()
print("2. PriodicalProductCheckListId column: OK")

# 3. Insert setting
cur.execute("""
    IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'sys_email_NoXrayInChekControl')
    INSERT INTO traceability_rs.dbo.settings (atribute, [value])
    VALUES ('sys_email_NoXrayInChekControl', 'gianluca.testa@vandewiele.com')
""")
conn.commit()
print("3. Setting sys_email_NoXrayInChekControl: OK")

conn.close()
print("\nAll DB changes applied successfully.")
