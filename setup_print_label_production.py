"""
setup_print_label_production.py

Setup database per il modulo Etichette Produzione:
1. Crea la tabella sessioni web (PrintLabelWebSessions).
2. Crea la tabella stampanti (LabelPrinters) - proposta.
3. Inserisce le traduzioni di menu e la chiave di autorizzazione.

Uso:
  .venv\\Scripts\\python.exe setup_print_label_production.py [--dry-run]
"""
import sys
import io
import os
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

LANGS = ["it", "en", "ro", "de", "sv"]

MENU_TRANSLATIONS = {
    "submenu_production_labels": {
        "it": "Etichette Produzione",
        "en": "Production Labels",
        "ro": "Etichete Producție",
        "de": "Produktionsetiketten",
        "sv": "Produktionsetiketter",
    },
    "submenu_production_labels_generic_print": {
        "it": "1. Stampa generica",
        "en": "1. Generic print",
        "ro": "1. Tipărire generică",
        "de": "1. Allgemeiner Druck",
        "sv": "1. Generisk utskrift",
    },
    "submenu_production_labels_order_print": {
        "it": "2. Stampa per ordini",
        "en": "2. Print by order",
        "ro": "2. Tipărire după comenzi",
        "de": "2. Druck nach Aufträgen",
        "sv": "2. Utskrift efter order",
    },
    "submenu_production_labels_bom": {
        "it": "3. Gestione etichette",
        "en": "3. Label management",
        "ro": "3. Gestionare etichete",
        "de": "3. Etikettenverwaltung",
        "sv": "3. Etiketthantering",
    },
}

AUTH_KEY = "gestione_stampa_etichette_produzione"
AUTH_MENU_VALUE = "Etichette Produzione"
AUTH_TRANSLATIONS = {
    "it": "Etichette Produzione",
    "en": "Production Labels",
    "ro": "Etichete Producție",
    "de": "Produktionsetiketten",
    "sv": "Produktionsetiketter",
}

PRINT_WINDOW_TRANSLATIONS = {
    "enter_usb_printer_name": {
        "it": "Seleziona o scrivi il nome della stampante USB",
        "en": "Select or type the USB printer name",
        "ro": "Selectați sau tastați numele imprimantei USB",
        "de": "USB-Druckernamen auswählen oder eingeben",
        "sv": "Välj eller skriv USB-skrivarens namn",
    },
    "printer_config_required": {
        "it": "Configurazione stampante assente o incompleta. Inserire il nome della stampante.",
        "en": "Printer configuration missing or incomplete. Please enter the printer name.",
        "ro": "Configurația imprimantei lipsește sau este incompletă. Introduceți numele imprimantei.",
        "de": "Druckerkonfiguration fehlt oder ist unvollständig. Bitte Druckernamen eingeben.",
        "sv": "Skrivarkonfiguration saknas eller är ofullständig. Ange skrivarens namn.",
    },
    "manual_usb_printer": {
        "it": "Oppure scrivi nome stampante",
        "en": "Or type printer name",
        "ro": "Sau tastați numele imprimantei",
        "de": "Oder Druckernamen eingeben",
        "sv": "Eller skriv skrivarens namn",
    },
}


def get_conn():
    # Prima tentativo: ConfigManager (db_config.enc)
    cfg = None
    try:
        cfg = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
    except Exception as e:
        print(f"ConfigManager non disponibile: {e}")

    # Secondo tentativo: database_config.py (variabili d'ambiente / .env.db)
    if cfg is None:
        try:
            from database_config import db_config
            conn_str = db_config.get_connection_string()
            print("Connessione tramite database_config.py")
            return pyodbc.connect(conn_str, autocommit=True)
        except Exception as e:
            print(f"database_config.py non disponibile: {e}")

    if cfg is None:
        raise RuntimeError("Impossibile ottenere la configurazione del database")

    available = pyodbc.drivers()
    driver = cfg.get("driver", "").strip()
    if not driver or driver not in available:
        for d in (
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server",
            "SQL Server Native Client 11.0",
            "SQL Server",
        ):
            if d in available:
                driver = d
                break
        if not driver and available:
            driver = available[0]
    if not driver:
        raise RuntimeError("Nessun driver ODBC per SQL Server trovato")

    # Normalizza il driver: pyodbc richiede le graffe solo se il nome contiene spazi,
    # ma la connection string usa sempre DRIVER={nome};. Se il driver e' gia' tra
    # graffe lo usiamo cosi', altrimenti lo wrappiamo.
    if not (driver.startswith("{") and driver.endswith("}")):
        driver = "{" + driver + "}"
    print(f"Uso driver ODBC: {driver}")

    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={cfg['server']};"
        f"DATABASE={cfg['database']};"
        f"UID={cfg['username']};"
        f"PWD={cfg['password']};"
        "MARS_Connection=Yes;TrustServerCertificate=Yes"
    )
    return pyodbc.connect(conn_str, autocommit=True)


def create_tables(cursor, dry_run):
    tables = [
        (
            "PrintLabelWebSessions",
            """
            CREATE TABLE Traceability_RS.ind.PrintLabelWebSessions (
                Token NVARCHAR(64) NOT NULL PRIMARY KEY,
                UserId INT NOT NULL,
                UserName NVARCHAR(255) NOT NULL,
                Permission NVARCHAR(255) NOT NULL,
                Page NVARCHAR(50) NOT NULL,
                IssuedAt DATETIME NOT NULL DEFAULT GETDATE(),
                ExpiresAt DATETIME NOT NULL,
                UsedAt DATETIME NULL,
                ClientIP NVARCHAR(50) NULL
            );
            """,
        ),
        (
            "LabelPrinters",
            """
            CREATE TABLE Traceability_RS.ind.LabelPrinters (
                LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
                PrinterName NVARCHAR(255) NOT NULL,
                PrinterType NVARCHAR(50) NOT NULL,
                ConnectionString NVARCHAR(500),
                PrinterIP NVARCHAR(50),
                PrinterPort INT,
                PrinterLocation NVARCHAR(255),
                PrinterModel NVARCHAR(100),
                LastRevisionDate DATETIME NULL,
                IsDefault BIT NOT NULL DEFAULT 0,
                DateIn DATETIME NOT NULL DEFAULT GETDATE(),
                DateOut DATETIME NULL,
                [User] NVARCHAR(255) NULL
            );
            """,
        ),
        (
            "LinkedMaterials",
            "dbo",
            """
            CREATE TABLE Traceability_RS.dbo.LinkedMaterials (
                LinkedMaterialId INT IDENTITY(1,1) PRIMARY KEY,
                LabelId INT NOT NULL,
                RibbonId INT NOT NULL,
                dateout DATETIME NULL,
                dateIn DATETIME NOT NULL DEFAULT GETDATE(),
                [User] NVARCHAR(255) NULL
            );
            """,
        ),
        (
            "LabelTypeParameters",
            "ind",
            """
            CREATE TABLE Traceability_RS.ind.LabelTypeParameters (
                LabelTypeParameterId INT IDENTITY(1,1) PRIMARY KEY,
                MaterialeId INT NOT NULL,
                ScartoType NVARCHAR(10) NOT NULL DEFAULT 'FIXED',
                ScartoValue DECIMAL(10,4) NOT NULL DEFAULT 0,
                ScartoMinimo DECIMAL(10,4) NOT NULL DEFAULT 0,
                Arrotondamento DECIMAL(10,4) NOT NULL DEFAULT 1,
                DateIn DATETIME NOT NULL DEFAULT GETDATE(),
                DateOut DATETIME NULL,
                [User] NVARCHAR(255) NULL,
                CONSTRAINT FK_LabelTypeParameters_Materiali FOREIGN KEY (MaterialeId)
                    REFERENCES Traceability_RS.ind.Materiali(MaterialeId)
            );
            """,
        ),
        (
            "LabelScripts",
            "ind",
            """
            CREATE TABLE Traceability_RS.ind.LabelScripts (
                LabelScriptId INT IDENTITY(1,1) PRIMARY KEY,
                BomIndirectMaterialId INT NOT NULL,
                ScriptToPrint NVARCHAR(MAX) NULL,
                DateOut DATETIME NULL,
                DateIn DATETIME NOT NULL DEFAULT GETDATE(),
                [User] NVARCHAR(255) NULL
            );
            """,
        ),
        (
            "LabelPrinterAssociations",
            "dbo",
            """
            CREATE TABLE Traceability_RS.dbo.LabelPrinterAssociations (
                LabelPrinterAssociationId INT IDENTITY(1,1) PRIMARY KEY,
                LabelId INT NOT NULL,
                LabelPrinterId INT NOT NULL,
                dateout DATETIME NULL,
                dateIn DATETIME NOT NULL DEFAULT GETDATE(),
                [User] NVARCHAR(255) NULL
            );
            """,
        ),
    ]
    for item in tables:
        if len(item) == 3:
            table_name, schema, ddl = item
        else:
            table_name, ddl = item
            schema = "ind"
        cursor.execute(
            "SELECT COUNT(*) FROM sys.tables t JOIN sys.schemas s ON t.schema_id = s.schema_id "
            "WHERE s.name = ? AND t.name = ?",
            (schema, table_name),
        )
        exists = cursor.fetchone()[0] > 0
        if exists:
            print(f"  Tabella {schema}.{table_name} già esistente.")
            continue
        print(f"  Creazione tabella {schema}.{table_name}...")
        if not dry_run:
            cursor.execute(ddl)


def insert_translation(cursor, key, lang, value, menu_value=None, dry_run=False):
    cursor.execute(
        "SELECT COUNT(*) FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode = ? AND TranslationKey = ?",
        (lang, key),
    )
    if cursor.fetchone()[0] > 0:
        cursor.execute(
            "SELECT TranslationValue FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode = ? AND TranslationKey = ?",
            (lang, key),
        )
        current = cursor.fetchone()[0]
        if (current or "") != value:
            print(f"  [{key}] Traduzione aggiornata per {lang}")
            if not dry_run:
                cursor.execute(
                    "UPDATE Traceability_RS.dbo.AppTranslations SET TranslationValue = ? WHERE LanguageCode = ? AND TranslationKey = ?",
                    (value, lang, key),
                )
        if menu_value is not None:
            cursor.execute(
                "UPDATE Traceability_RS.dbo.AppTranslations SET MenuValue = ? WHERE LanguageCode = ? AND TranslationKey = ? AND (MenuValue IS NULL OR MenuValue = '')",
                (menu_value, lang, key),
            )
            if cursor.rowcount:
                print(f"  [{key}] MenuValue aggiornato per {lang}")
        return
    print(f"  Inserimento traduzione {key}/{lang}")
    if not dry_run:
        if menu_value is not None:
            cursor.execute(
                "INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES (?, ?, ?, ?)",
                (lang, key, value, menu_value),
            )
        else:
            cursor.execute(
                "INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                (lang, key, value),
            )


def setup_menu_translations(cursor, dry_run):
    print("\nTraduzioni menu...")
    for key, translations in MENU_TRANSLATIONS.items():
        for lang in LANGS:
            insert_translation(cursor, key, lang, translations[lang], dry_run=dry_run)


def setup_auth_translations(cursor, dry_run):
    print("\nChiave autorizzazione...")
    for lang in LANGS:
        insert_translation(
            cursor, AUTH_KEY, lang, AUTH_TRANSLATIONS[lang],
            menu_value=AUTH_MENU_VALUE, dry_run=dry_run
        )


def setup_print_window_translations(cursor, dry_run):
    print("\nTraduzioni finestra stampa...")
    for key, translations in PRINT_WINDOW_TRANSLATIONS.items():
        for lang in LANGS:
            insert_translation(cursor, key, lang, translations[lang], dry_run=dry_run)


def alter_label_printers(cursor, dry_run):
    """Aggiunge le colonne mancanti a LabelPrinters se la tabella esiste già."""
    print("\nVerifica colonne su LabelPrinters...")
    columns = ["PrinterIP", "PrinterPort", "PrinterLocation", "LastRevisionDate"]
    for col in columns:
        cursor.execute(
            """SELECT COUNT(*) FROM sys.columns c
               JOIN sys.tables t ON c.object_id = t.object_id
               JOIN sys.schemas s ON t.schema_id = s.schema_id
               WHERE s.name = 'ind' AND t.name = 'LabelPrinters' AND c.name = ?""",
            (col,),
        )
        exists = cursor.fetchone()[0] > 0
        if exists:
            print(f"  Colonna {col} già presente.")
            continue
        print(f"  Aggiunta colonna {col}...")
        if not dry_run:
            if col == "PrinterPort":
                cursor.execute(
                    f"ALTER TABLE Traceability_RS.ind.LabelPrinters ADD {col} INT"
                )
            elif col == "LastRevisionDate":
                cursor.execute(
                    f"ALTER TABLE Traceability_RS.ind.LabelPrinters ADD {col} DATETIME NULL"
                )
            else:
                cursor.execute(
                    f"ALTER TABLE Traceability_RS.ind.LabelPrinters ADD {col} NVARCHAR(255)"
                )


def alter_linked_materials(cursor, dry_run):
    """Rimuove la colonna LabelPrinterId da LinkedMaterials se presente (ora la relazione è su LabelPrinterAssociations)."""
    print("\nVerifica colonna LabelPrinterId su LinkedMaterials...")
    cursor.execute(
        """SELECT COUNT(*) FROM sys.columns c
           JOIN sys.tables t ON c.object_id = t.object_id
           JOIN sys.schemas s ON t.schema_id = s.schema_id
           WHERE s.name = 'dbo' AND t.name = 'LinkedMaterials' AND c.name = 'LabelPrinterId'"""
    )
    exists = cursor.fetchone()[0] > 0
    if not exists:
        print("  Colonna LabelPrinterId non presente.")
        return
    print("  Rimozione colonna LabelPrinterId...")
    if not dry_run:
        cursor.execute(
            "ALTER TABLE Traceability_RS.dbo.LinkedMaterials DROP COLUMN LabelPrinterId"
        )


def alter_bom_indirect_materials(cursor, dry_run):
    """Aggiunge QuantityPerPiece a BomIndirectMaterials se mancante."""
    print("\nVerifica colonne su BomIndirectMaterials...")
    cursor.execute(
        """SELECT COUNT(*) FROM sys.columns c
           JOIN sys.tables t ON c.object_id = t.object_id
           JOIN sys.schemas s ON t.schema_id = s.schema_id
           WHERE s.name = 'ind' AND t.name = 'BomIndirectMaterials' AND c.name = 'QuantityPerPiece'"""
    )
    exists = cursor.fetchone()[0] > 0
    if exists:
        print("  Colonna QuantityPerPiece già presente.")
        return
    print("  Aggiunta colonna QuantityPerPiece...")
    if not dry_run:
        cursor.execute(
            "ALTER TABLE Traceability_RS.ind.BomIndirectMaterials "
            "ADD QuantityPerPiece DECIMAL(10,4) NOT NULL DEFAULT 1"
        )


def alter_materiali_richieste(cursor, dry_run):
    """Aggiunge Origin e ReferenceOrderIds a MaterialiRichieste se mancanti."""
    print("\nVerifica colonne su MaterialiRichieste...")
    for col, sql in (
        ("Origin", "ALTER TABLE Traceability_RS.ind.MaterialiRichieste ADD Origin NVARCHAR(10) NULL"),
        ("ReferenceOrderIds", "ALTER TABLE Traceability_RS.ind.MaterialiRichieste ADD ReferenceOrderIds NVARCHAR(MAX) NULL"),
    ):
        cursor.execute(
            """SELECT COUNT(*) FROM sys.columns c
               JOIN sys.tables t ON c.object_id = t.object_id
               JOIN sys.schemas s ON t.schema_id = s.schema_id
               WHERE s.name = 'ind' AND t.name = 'MaterialiRichieste' AND c.name = ?""",
            (col,),
        )
        exists = cursor.fetchone()[0] > 0
        if exists:
            print(f"  Colonna {col} già presente.")
            continue
        print(f"  Aggiunta colonna {col}...")
        if not dry_run:
            cursor.execute(sql)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simula senza modificare il DB")
    args = parser.parse_args()

    print("Connessione al database...")
    conn = get_conn()
    cursor = conn.cursor()

    print("\nCreazione tabelle...")
    create_tables(cursor, args.dry_run)

    alter_label_printers(cursor, args.dry_run)
    alter_linked_materials(cursor, args.dry_run)
    alter_bom_indirect_materials(cursor, args.dry_run)
    alter_materiali_richieste(cursor, args.dry_run)

    setup_menu_translations(cursor, args.dry_run)
    setup_auth_translations(cursor, args.dry_run)
    setup_print_window_translations(cursor, args.dry_run)

    if not args.dry_run:
        conn.commit()
    print("\nSetup completato.")


if __name__ == "__main__":
    main()
