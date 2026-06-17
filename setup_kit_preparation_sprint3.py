"""
setup_kit_preparation_sprint3.py
Sprint 3 del modulo Kit Preparation (spec docs/PlanRespect_KitPreparation_Spec_v1.2.md
§5.2, §7): oggetti DB per verifica ingresso Preformatura e notifiche.

- kit_item_checks: esito verifica per riga e per fase (PREFORMING/PRODUCTION)
- kit_popup_queue: coda popup (categoria DIRECT_MATERIAL, §7.2) consumata dal
  monitor in-app; target 'WH_HOST' (postazione con wh_host.json) o hostname
- ALTER material_requests: nota, computer richiedente, timestamp notifiche
  (per popup "pronto" e reminder 10 minuti)

Uso:
  .venv\\Scripts\\python.exe setup_kit_preparation_sprint3.py [--dry-run]
"""
import sys, io, os, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

TABLES = [
    ("kit_item_checks", """
CREATE TABLE dbo.kit_item_checks (
    id                  INT IDENTITY PRIMARY KEY,
    item_id             INT NOT NULL REFERENCES dbo.picking_list_items(id),
    phase               NVARCHAR(20) NOT NULL,           -- PREFORMING, PRODUCTION
    qty_expected        DECIMAL(12,3) NOT NULL,          -- qty consegnata dalla fase precedente
    qty_actual          DECIMAL(12,3) NOT NULL,
    check_status        NVARCHAR(20) NOT NULL,           -- OK, MISMATCH
    checked_by          INT NOT NULL,
    checked_date        DATETIME DEFAULT GETDATE(),
    CONSTRAINT UQ_kit_item_checks UNIQUE (item_id, phase)
)"""),
    ("kit_popup_queue", """
CREATE TABLE dbo.kit_popup_queue (
    id                  INT IDENTITY PRIMARY KEY,
    category            NVARCHAR(30) DEFAULT 'DIRECT_MATERIAL',
    target              NVARCHAR(100) NOT NULL,          -- 'WH_HOST' o hostname richiedente
    title               NVARCHAR(200) NOT NULL,
    message             NVARCHAR(1000) NOT NULL,
    order_number        NVARCHAR(30),
    created_date        DATETIME DEFAULT GETDATE(),
    displayed_date      DATETIME,                        -- claim atomico del monitor
    displayed_on        NVARCHAR(100)
)"""),
]

INDEXES = [
    ("IX_kit_popup_queue_pending", "kit_popup_queue",
     "CREATE INDEX IX_kit_popup_queue_pending ON dbo.kit_popup_queue (target, displayed_date)"),
    ("IX_kit_item_checks_item", "kit_item_checks",
     "CREATE INDEX IX_kit_item_checks_item ON dbo.kit_item_checks (phase, check_status)"),
]

# (tabella, colonna, definizione)
ALTERS = [
    ("material_requests", "note", "NVARCHAR(500)"),
    ("material_requests", "requester_computer", "NVARCHAR(100)"),
    ("material_requests", "wh_last_notified", "DATETIME"),
    ("material_requests", "requester_last_notified", "DATETIME"),
]


def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
    )


def main():
    parser = argparse.ArgumentParser(description='Setup Sprint 3 Kit Preparation')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    conn = get_conn()
    cursor = conn.cursor()
    print(f"Connesso a {cursor.execute('SELECT DB_NAME()').fetchone()[0]}."
          f"{' (DRY-RUN)' if args.dry_run else ''}")

    for name, ddl in TABLES:
        if cursor.execute("SELECT OBJECT_ID(?, 'U')", (f"dbo.{name}",)).fetchone()[0]:
            print(f"  [=] dbo.{name} esiste gia'")
            continue
        if not args.dry_run:
            cursor.execute(ddl)
        print(f"  [+] dbo.{name} creata")

    for ix_name, table, ddl in INDEXES:
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sys.indexes WHERE name=? AND object_id=OBJECT_ID(?)",
            (ix_name, f"dbo.{table}")).fetchone()[0]
        if exists:
            print(f"  [=] {ix_name} esiste gia'")
        else:
            if not args.dry_run:
                cursor.execute(ddl)
            print(f"  [+] {ix_name} creato")

    for table, col, definition in ALTERS:
        exists = cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=? AND COLUMN_NAME=?
        """, (table, col)).fetchone()[0]
        if exists:
            print(f"  [=] {table}.{col} esiste gia'")
        else:
            if not args.dry_run:
                cursor.execute(f"ALTER TABLE dbo.{table} ADD {col} {definition}")
            print(f"  [+] {table}.{col} aggiunta")

    if args.dry_run:
        conn.rollback()
        print("\nDRY-RUN: rollback eseguito.")
    else:
        conn.commit()
        print("\nCommit eseguito.")
    conn.close()


if __name__ == '__main__':
    main()
