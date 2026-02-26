"""
insert_external_programs_translations.py
Inserisce le traduzioni per il modulo Programmi Esterni in AppTranslations (5 lingue).
Usa IF NOT EXISTS per idempotenza. Eseguire una sola volta.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- Connessione DB -----------------------------------------------------------
try:
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
except Exception as e:
    print(f"ERRORE connessione: {e}")
    sys.exit(1)


# --- Traduzioni ---------------------------------------------------------------
TRANSLATIONS = [
    # Menu
    ("submenu_external_programs", {
        "it": "Programmi Esterni",
        "en": "External Programs",
        "ro": "Programe Externe",
        "de": "Externe Programme",
        "sv": "Externa Program",
    }),
    ("ext_setup_ip", {
        "it": "SetUp IP",
        "en": "SetUp IP",
        "ro": "Configurare IP",
        "de": "IP einrichten",
        "sv": "Konfigurera IP",
    }),
    ("ext_open_browser", {
        "it": "Apri Programma",
        "en": "Open Program",
        "ro": "Deschide Programul",
        "de": "Programm \u00f6ffnen",
        "sv": "\u00d6ppna Program",
    }),
    # SetUp IP Window
    ("ext_programs_setup_title", {
        "it": "SetUp IP - Programmi Esterni",
        "en": "SetUp IP - External Programs",
        "ro": "Configurare IP - Programe Externe",
        "de": "IP einrichten - Externe Programme",
        "sv": "Konfigurera IP - Externa Program",
    }),
    ("ext_program_name", {
        "it": "Programma",
        "en": "Program",
        "ro": "Program",
        "de": "Programm",
        "sv": "Program",
    }),
    ("ext_select_row", {
        "it": "Seleziona un record",
        "en": "Select a record",
        "ro": "Selecta\u021bi o \u00eenregistrare",
        "de": "Bitte einen Eintrag ausw\u00e4hlen",
        "sv": "V\u00e4lj en post",
    }),
    ("ext_confirm_delete", {
        "it": "Disattivare il programma",
        "en": "Deactivate the program",
        "ro": "Dezactiva\u021bi programul",
        "de": "Programm deaktivieren",
        "sv": "Inaktivera programmet",
    }),
    ("ext_deleted_ok", {
        "it": "Programma disattivato con successo",
        "en": "Program deactivated successfully",
        "ro": "Program dezactivat cu succes",
        "de": "Programm erfolgreich deaktiviert",
        "sv": "Programmet har inaktiverats",
    }),
    ("ext_add_title", {
        "it": "Aggiungi Programma Esterno",
        "en": "Add External Program",
        "ro": "Ad\u0103uga\u021bi Program Extern",
        "de": "Externes Programm hinzuf\u00fcgen",
        "sv": "L\u00e4gg till externt program",
    }),
    ("ext_edit_title", {
        "it": "Modifica Programma Esterno",
        "en": "Edit External Program",
        "ro": "Modifica\u021bi Program Extern",
        "de": "Externes Programm bearbeiten",
        "sv": "Redigera externt program",
    }),
    ("ext_all_fields_required", {
        "it": "Tutti i campi sono obbligatori",
        "en": "All fields are required",
        "ro": "Toate c\u00e2mpurile sunt obligatorii",
        "de": "Alle Felder sind erforderlich",
        "sv": "Alla f\u00e4lt \u00e4r obligatoriska",
    }),
    ("ext_saved_ok", {
        "it": "Salvato con successo",
        "en": "Saved successfully",
        "ro": "Salvat cu succes",
        "de": "Erfolgreich gespeichert",
        "sv": "Sparat",
    }),
    # Browser Launcher Window
    ("ext_browser_title", {
        "it": "Apri Programma Esterno",
        "en": "Open External Program",
        "ro": "Deschide Program Extern",
        "de": "Externes Programm \u00f6ffnen",
        "sv": "\u00d6ppna externt program",
    }),
    ("ext_select_program", {
        "it": "Seleziona un programma:",
        "en": "Select a program:",
        "ro": "Selecta\u021bi un program:",
        "de": "Programm ausw\u00e4hlen:",
        "sv": "V\u00e4lj ett program:",
    }),
    ("ext_open_browser_btn", {
        "it": "\U0001f310 Apri nel Browser",
        "en": "\U0001f310 Open in Browser",
        "ro": "\U0001f310 Deschide \u00een Browser",
        "de": "\U0001f310 Im Browser \u00f6ffnen",
        "sv": "\U0001f310 \u00d6ppna i webbl\u00e4saren",
    }),
]

# --- Inserimento --------------------------------------------------------------
CHECK_SQL = """
SELECT COUNT(1) FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [LanguageCode] = ? AND [TranslationKey] = ?
"""

INSERT_SQL = """
INSERT INTO [Traceability_RS].[dbo].[AppTranslations]
    ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES (?, ?, ?)
"""

inserted = 0
skipped  = 0
errors   = 0

for key, langs in TRANSLATIONS:
    for lang, value in langs.items():
        try:
            cursor.execute(CHECK_SQL, (lang, key))
            exists = cursor.fetchone()[0]
            if exists:
                print(f"  [SKIP]   {lang:4s} | {key}")
                skipped += 1
            else:
                cursor.execute(INSERT_SQL, (lang, key, value))
                print(f"  [INSERT] {lang:4s} | {key}")
                inserted += 1
        except Exception as e:
            print(f"  [ERROR]  {lang:4s} | {key} -> {e}")
            errors += 1

try:
    conn.commit()
    print(f"\n=== Completato: {inserted} inseriti, {skipped} gia' presenti, {errors} errori ===")
except Exception as e:
    print(f"ERRORE commit: {e}")
finally:
    conn.close()
