# -*- coding: utf-8 -*-
"""
setup_npi_commerciali.py — Migrazione schema per la gestione Commerciali NPI (idempotente).

- dbo.Soggetti: +Telefono NVARCHAR(30), +IsCommercial BIT (default 0), +IdSite SMALLINT
  (società del commerciale, FK logica a Sites.IDSite con IsSupplier IS NULL).
- dbo.CommercialeCliente: associazione commerciale↔cliente (per stringa Prodotti.Cliente),
  UN solo commerciale per cliente (ClienteNome come PK).

Uso:  .venv\\Scripts\\python.exe setup_npi_commerciali.py
Spec: docs/NPI_Commerciali_Spec_v1.0.md
"""
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

DDL = [
    # ── Soggetti: nuove colonne ──────────────────────────────────────────
    """
    IF COL_LENGTH('dbo.Soggetti','Telefono') IS NULL
        ALTER TABLE dbo.Soggetti ADD Telefono NVARCHAR(30) NULL;
    """,
    """
    IF COL_LENGTH('dbo.Soggetti','IsCommercial') IS NULL
        ALTER TABLE dbo.Soggetti ADD IsCommercial BIT NOT NULL
            CONSTRAINT DF_Soggetti_IsCommercial DEFAULT 0 WITH VALUES;
    """,
    """
    IF COL_LENGTH('dbo.Soggetti','IdSite') IS NULL
        ALTER TABLE dbo.Soggetti ADD IdSite SMALLINT NULL;
    """,
    """
    IF COL_LENGTH('dbo.Soggetti','AutoEmail') IS NULL
        ALTER TABLE dbo.Soggetti ADD AutoEmail BIT NOT NULL
            CONSTRAINT DF_Soggetti_AutoEmail DEFAULT 0 WITH VALUES;
    """,
    # ── CommercialeCliente: un commerciale per cliente (PK su ClienteNome) ─
    """
    IF OBJECT_ID('dbo.CommercialeCliente','U') IS NULL
    CREATE TABLE dbo.CommercialeCliente (
        ClienteNome NVARCHAR(255) NOT NULL PRIMARY KEY,
        SoggettoID  INT           NOT NULL,
        DateSys     DATETIME      NOT NULL DEFAULT GETDATE()
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
    # report colonne Soggetti
    cur.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                   WHERE TABLE_NAME='Soggetti' AND TABLE_SCHEMA='dbo'
                     AND COLUMN_NAME IN ('Telefono','IsCommercial','IdSite','AutoEmail')
                   ORDER BY COLUMN_NAME""")
    print("Colonne Soggetti aggiunte:", [r[0] for r in cur.fetchall()])
    cur.execute("SELECT CASE WHEN OBJECT_ID('dbo.CommercialeCliente','U') IS NULL THEN 0 ELSE 1 END")
    print("Tabella CommercialeCliente:", "presente" if cur.fetchone()[0] else "MANCANTE")
    conn.close()
    print("Setup completato.")


if __name__ == "__main__":
    main()
