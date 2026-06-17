"""
setup_kit_preparation_sprint1.py
Sprint 1 del modulo Kit Preparation (spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §6):
crea le tabelle del modulo in Traceability_RS (idempotente: salta le esistenti).

Le colonne operatore (*_by, operator_id) contengono EmployeeHireHistoryId
(identita' restituita da _execute_authorized_action); nessuna FK cross-database.

Uso:
  .venv\\Scripts\\python.exe setup_kit_preparation_sprint1.py [--dry-run]
"""
import sys, io, os, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

TABLES = [
    ("picking_lists", """
CREATE TABLE dbo.picking_lists (
    id                  INT IDENTITY PRIMARY KEY,
    source_file_name    NVARCHAR(260) NOT NULL,
    source_file_path    NVARCHAR(500) NOT NULL,
    source_file_hash    CHAR(64) NOT NULL,
    source_file_date    DATETIME NOT NULL,
    upload_date         DATETIME DEFAULT GETDATE(),
    uploaded_by         INT NOT NULL,
    status              NVARCHAR(30) DEFAULT 'OPEN',     -- OPEN, PARTIAL, CLOSED, REOPENED
    closed_date         DATETIME,
    closed_by           INT,
    derogation_by       INT,
    derogation_note     NVARCHAR(500)
)"""),
    ("picking_list_orders", """
CREATE TABLE dbo.picking_list_orders (
    picking_list_id     INT NOT NULL REFERENCES dbo.picking_lists(id),
    order_number        NVARCHAR(30) NOT NULL,
    PRIMARY KEY (picking_list_id, order_number)
)"""),
    ("order_priority", """
CREATE TABLE dbo.order_priority (
    order_number        NVARCHAR(30) PRIMARY KEY,
    priority            TINYINT NOT NULL DEFAULT 0 CHECK (priority IN (0,1,2,3)),
    set_by              INT NOT NULL,
    set_date            DATETIME DEFAULT GETDATE()
)"""),
    ("picking_list_items", """
CREATE TABLE dbo.picking_list_items (
    id                  INT IDENTITY PRIMARY KEY,
    picking_list_id     INT NOT NULL REFERENCES dbo.picking_lists(id),
    order_number        NVARCHAR(30),                    -- NULL finche' non disaggregato
    material_code       NVARCHAR(100) NOT NULL,          -- ITEM CODE
    unique_number       NVARCHAR(100),                   -- REEL CODE
    qty_required        DECIMAL(12,3) NOT NULL,
    qty_picked          DECIMAL(12,3) DEFAULT 0,
    pick_status         NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, PARTIAL, COMPLETE,
                                                         -- NOT_IN_BOM, MISSING_FROM_LIST
    picked_by           INT,
    picked_date         DATETIME,
    notes               NVARCHAR(500)
)"""),
    ("kit_verification_log", """
CREATE TABLE dbo.kit_verification_log (
    id                  INT IDENTITY PRIMARY KEY,
    order_number        NVARCHAR(30) NOT NULL,
    phase               NVARCHAR(20) NOT NULL,           -- WH, PREFORMING, PRODUCTION
    event_type          NVARCHAR(40) NOT NULL,           -- SCAN, VERIFY_OK, VERIFY_FAIL,
                                                         -- REQUEST_MATERIAL, MATERIAL_FOUND,
                                                         -- UNKNOWN_UNIQUE_NUMBER,
                                                         -- SOURCE_FILE_CHANGED,
                                                         -- SESSION_SUSPENDED, SESSION_RESUMED
    material_code       NVARCHAR(100),
    unique_number       NVARCHAR(100),
    qty_expected        DECIMAL(12,3),
    qty_actual          DECIMAL(12,3),
    operator_id         INT,
    event_date          DATETIME DEFAULT GETDATE(),
    notes               NVARCHAR(1000)
)"""),
    ("kit_status", """
CREATE TABLE dbo.kit_status (
    order_number        NVARCHAR(30) PRIMARY KEY,
    status              NVARCHAR(40) NOT NULL,           -- WH_OPEN, WH_PARTIAL, WH_CLOSED,
                                                         -- REOPENED, IN_PREFORMING,
                                                         -- RECEIVED_IN_PRODUCTION,
                                                         -- BLOCKED_MISSING_MATERIAL, COMPLETED
    updated_by          INT,
    updated_date        DATETIME DEFAULT GETDATE()
)"""),
    ("kit_sessions", """
CREATE TABLE dbo.kit_sessions (
    id                  INT IDENTITY PRIMARY KEY,
    picking_list_id     INT REFERENCES dbo.picking_lists(id),
    phase               NVARCHAR(20) NOT NULL,           -- WH, PREFORMING, PRODUCTION
    operator_id         INT NOT NULL,
    started_date        DATETIME DEFAULT GETDATE(),
    last_activity_date  DATETIME,
    status              NVARCHAR(20) DEFAULT 'ACTIVE',   -- ACTIVE, SUSPENDED, COMPLETED, ABORTED
    source_file_hash    CHAR(64) NOT NULL,
    resume_decision     NVARCHAR(30),                    -- KEEP_OLD_FILE, ADOPT_NEW_FILE
    resume_note         NVARCHAR(500)
)"""),
    ("material_requests", """
CREATE TABLE dbo.material_requests (
    id                  INT IDENTITY PRIMARY KEY,
    order_number        NVARCHAR(30) NOT NULL,
    requesting_phase    NVARCHAR(20) NOT NULL,           -- PREFORMING, PRODUCTION
    material_code       NVARCHAR(100) NOT NULL,
    qty_requested       DECIMAL(12,3) NOT NULL,
    requested_by        INT NOT NULL,
    request_date        DATETIME DEFAULT GETDATE(),
    wh_status           NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, CONFIRMED, CANCELLED
    confirmed_by        INT,
    confirmed_date      DATETIME,
    resolution          NVARCHAR(30),                    -- PROVIDED, FOUND_IN_PRODUCTION, CANCELLED
    resolved_date       DATETIME
)"""),
]

INDEXES = [
    ("IX_picking_lists_status", "picking_lists",
     "CREATE INDEX IX_picking_lists_status ON dbo.picking_lists (status)"),
    ("IX_picking_list_items_list", "picking_list_items",
     "CREATE INDEX IX_picking_list_items_list ON dbo.picking_list_items (picking_list_id, pick_status)"),
    ("IX_kit_verification_log_order", "kit_verification_log",
     "CREATE INDEX IX_kit_verification_log_order ON dbo.kit_verification_log (order_number, event_date)"),
    ("IX_material_requests_status", "material_requests",
     "CREATE INDEX IX_material_requests_status ON dbo.material_requests (wh_status, request_date)"),
    ("IX_kit_sessions_status", "kit_sessions",
     "CREATE INDEX IX_kit_sessions_status ON dbo.kit_sessions (status, picking_list_id)"),
]


def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
    )


def main():
    parser = argparse.ArgumentParser(description='Setup Sprint 1 Kit Preparation (tabelle DB)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    conn = get_conn()
    cursor = conn.cursor()
    db_name = cursor.execute("SELECT DB_NAME()").fetchone()[0]
    print(f"Connesso a {db_name}.{' (DRY-RUN)' if args.dry_run else ''}")

    created, skipped = 0, 0
    for name, ddl in TABLES:
        if cursor.execute("SELECT OBJECT_ID(?, 'U')", (f"dbo.{name}",)).fetchone()[0]:
            print(f"  [=] dbo.{name} esiste gia'")
            skipped += 1
            continue
        if not args.dry_run:
            cursor.execute(ddl)
        print(f"  [+] dbo.{name} creata")
        created += 1

    for ix_name, table, ddl in INDEXES:
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sys.indexes WHERE name=? AND object_id=OBJECT_ID(?)",
            (ix_name, f"dbo.{table}")
        ).fetchone()[0]
        if exists:
            print(f"  [=] {ix_name} esiste gia'")
            continue
        table_exists = cursor.execute("SELECT OBJECT_ID(?, 'U')", (f"dbo.{table}",)).fetchone()[0]
        if not args.dry_run and (table_exists or created):
            cursor.execute(ddl)
            print(f"  [+] {ix_name} creato")
        elif args.dry_run:
            print(f"  [+] {ix_name} (dry-run)")

    if args.dry_run:
        conn.rollback()
        print(f"\nDRY-RUN: rollback. {created} tabelle da creare, {skipped} gia' presenti.")
    else:
        conn.commit()
        print(f"\nCommit eseguito: {created} tabelle create, {skipped} gia' presenti.")
    conn.close()


if __name__ == '__main__':
    main()
