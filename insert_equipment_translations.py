"""
insert_equipment_translations.py
Inserisce le traduzioni per i campi Brand e Company nella form EditMachine.
Usa IF NOT EXISTS e N'' per Unicode. Idempotente.
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
    ("brand_label", {
        "it": "Marca:",
        "en": "Brand:",
        "ro": "Marca:",
        "de": "Marke:",
        "sv": "Varumärke:",
    }),
    ("company_label", {
        "it": "Azienda:",
        "en": "Company:",
        "ro": "Companie:",
        "de": "Unternehmen:",
        "sv": "Företag:",
    }),
]

# --- Inserimento con N prefix e IF NOT EXISTS ---------------------------------
inserted = 0
skipped  = 0
errors   = 0

for key, langs in TRANSLATIONS:
    for lang, value in langs.items():
        # Escape singoli apici nei valori
        safe_value = value.replace("'", "''")
        safe_key = key.replace("'", "''")
        safe_lang = lang.replace("'", "''")
        
        sql = f"""
        IF NOT EXISTS (
            SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations]
            WHERE [LanguageCode] = N'{safe_lang}' AND [TranslationKey] = N'{safe_key}'
        )
        INSERT INTO [Traceability_RS].[dbo].[AppTranslations]
            ([LanguageCode], [TranslationKey], [TranslationValue])
        VALUES (N'{safe_lang}', N'{safe_key}', N'{safe_value}')
        """
        try:
            cursor.execute(sql)
            if cursor.rowcount > 0:
                print(f"  [INSERT] {lang:4s} | {key} = {value}")
                inserted += 1
            else:
                print(f"  [SKIP]   {lang:4s} | {key} (gia' presente)")
                skipped += 1
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
