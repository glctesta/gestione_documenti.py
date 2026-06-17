# -*- coding: utf-8 -*-
"""
setup_kit_dashboard.py — Crea le tabelle della Kit Dashboard (idempotente).

Tabelle (Traceability_RS.dbo):
  - kit_dashboard_snapshot          stato corrente per ordine (riscritto ogni sync)
  - kit_dashboard_snapshot_missing  materiali mancanti per ordine (drill-down)
  - kit_dashboard_history           storico esiti persistente (D8)
  - kit_dashboard_controller        elezione controller + heartbeat
  - kit_dashboard_alert_log         dedup alert "server down" cross-PC

Uso:  .venv\\Scripts\\python.exe setup_kit_dashboard.py
Spec: docs/KitDashboard_WebServer_Spec_v1.0.md (§5)
"""
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager


DDL = [
    # ── snapshot stato corrente ──────────────────────────────────────────
    """
    IF OBJECT_ID('Traceability_RS.dbo.kit_dashboard_snapshot','U') IS NULL
    CREATE TABLE Traceability_RS.dbo.kit_dashboard_snapshot (
        order_number        NVARCHAR(30)  NOT NULL PRIMARY KEY,
        product_code        NVARCHAR(100) NULL,
        order_qty           DECIMAL(12,3) NULL,
        priority            TINYINT       NOT NULL DEFAULT 0,
        kit_status          NVARCHAR(40)  NULL,
        phase               NVARCHAR(20)  NULL,
        items_total         INT           NOT NULL DEFAULT 0,
        items_done          INT           NOT NULL DEFAULT 0,
        pct_complete        DECIMAL(5,2)  NOT NULL DEFAULT 0,
        missing_codes       INT           NOT NULL DEFAULT 0,
        open_requests       INT           NOT NULL DEFAULT 0,
        is_ready_for_prod   BIT           NOT NULL DEFAULT 0,
        is_late             BIT           NOT NULL DEFAULT 0,
        is_incomplete       BIT           NOT NULL DEFAULT 0,
        eta_minutes         INT           NULL,
        eta_ready_at        DATETIME      NULL,
        planned_start       DATETIME      NULL,
        list_id             INT           NULL,
        started_date        DATETIME      NULL,
        last_activity_date  DATETIME      NULL,
        snapshot_date       DATETIME      NOT NULL DEFAULT GETDATE()
    );
    """,
    # ── dettaglio materiali mancanti ─────────────────────────────────────
    """
    IF OBJECT_ID('Traceability_RS.dbo.kit_dashboard_snapshot_missing','U') IS NULL
    CREATE TABLE Traceability_RS.dbo.kit_dashboard_snapshot_missing (
        order_number   NVARCHAR(30)  NOT NULL,
        material_code  NVARCHAR(100) NOT NULL,
        qty_required   DECIMAL(12,3) NULL,
        qty_picked     DECIMAL(12,3) NULL,
        qty_missing    DECIMAL(12,3) NULL,
        pick_status    NVARCHAR(20)  NULL,
        snapshot_date  DATETIME      NOT NULL DEFAULT GETDATE(),
        CONSTRAINT PK_kit_dash_missing PRIMARY KEY (order_number, material_code)
    );
    """,
    # ── storico esiti (persistente) ──────────────────────────────────────
    """
    IF OBJECT_ID('Traceability_RS.dbo.kit_dashboard_history','U') IS NULL
    CREATE TABLE Traceability_RS.dbo.kit_dashboard_history (
        order_number    NVARCHAR(30)  NOT NULL PRIMARY KEY,
        product_code    NVARCHAR(100) NULL,
        planned_start   DATETIME      NULL,
        first_seen_date DATETIME      NOT NULL DEFAULT GETDATE(),
        ready_date      DATETIME      NULL,
        completed_date  DATETIME      NULL,
        was_on_time     BIT           NULL,
        was_complete    BIT           NULL,
        final_status    NVARCHAR(40)  NULL,
        updated_date    DATETIME      NOT NULL DEFAULT GETDATE()
    );
    """,
    # ── controller / heartbeat ───────────────────────────────────────────
    """
    IF OBJECT_ID('Traceability_RS.dbo.kit_dashboard_controller','U') IS NULL
    CREATE TABLE Traceability_RS.dbo.kit_dashboard_controller (
        lock_name       NVARCHAR(50)  NOT NULL PRIMARY KEY,
        controller_host NVARCHAR(100) NULL,
        controller_ip   NVARCHAR(45)  NULL,
        heartbeat_date  DATETIME      NULL,
        server_state    NVARCHAR(20)  NULL,
        server_pid      INT           NULL,
        last_check_date DATETIME      NULL
    );
    """,
    # riga di lock iniziale
    """
    IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.kit_dashboard_controller WHERE lock_name='KIT_DASHBOARD')
        INSERT INTO Traceability_RS.dbo.kit_dashboard_controller (lock_name) VALUES ('KIT_DASHBOARD');
    """,
    # ── dedup alert server-down ──────────────────────────────────────────
    """
    IF OBJECT_ID('Traceability_RS.dbo.kit_dashboard_alert_log','U') IS NULL
    CREATE TABLE Traceability_RS.dbo.kit_dashboard_alert_log (
        alert_key   NVARCHAR(100) NOT NULL PRIMARY KEY,  -- es. 'SERVER_DOWN|2026-06-13T10:35'
        created_by  NVARCHAR(100) NULL,
        created_date DATETIME     NOT NULL DEFAULT GETDATE()
    );
    """,
]


def main():
    cfg = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
    conn = pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};TrustServerCertificate=Yes"
    )
    cur = conn.cursor()
    for i, ddl in enumerate(DDL, 1):
        cur.execute(ddl)
        print(f"  [{i}/{len(DDL)}] OK")
    conn.commit()
    # report
    cur.execute("""SELECT name FROM Traceability_RS.sys.tables
                   WHERE name LIKE 'kit_dashboard%' ORDER BY name""")
    print("Tabelle kit_dashboard presenti:")
    for r in cur.fetchall():
        print("  -", r[0])
    conn.close()
    print("Setup completato.")


if __name__ == "__main__":
    main()
