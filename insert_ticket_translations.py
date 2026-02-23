"""
insert_ticket_translations.py
Inserisce le traduzioni del modulo Ticket in AppTranslations (5 lingue).
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
# Formato: (TranslationKey, {lang: value})
TRANSLATIONS = [
    ("menu_tickets", {
        "it": "Tickets",
        "en": "Tickets",
        "ro": "Tichete",
        "de": "Tickets",
        "sv": "\u00c4renden",
    }),
    ("ticket_window_title", {
        "it": "Nuovo Ticket",
        "en": "New Ticket",
        "ro": "Tichet nou",
        "de": "Neues Ticket",
        "sv": "Nytt \u00e4rende",
    }),
    ("ticket_window_title_error", {
        "it": "Errore \u2013 Apri Ticket",
        "en": "Error \u2013 Open Ticket",
        "ro": "Eroare \u2013 Deschide Tichet",
        "de": "Fehler \u2013 Ticket \u00f6ffnen",
        "sv": "Fel \u2013 \u00d6ppna \u00e4rende",
    }),
    ("ticket_auto_error_banner", {
        "it": "Errore rilevato automaticamente \u2013 compila il ticket per segnalarlo.",
        "en": "Error detected automatically \u2013 fill in the ticket to report it.",
        "ro": "Eroare detectat\u0103 automat \u2013 completa\u021bi tichetul pentru a raporta.",
        "de": "Fehler automatisch erkannt \u2013 f\u00fcllen Sie das Ticket aus, um ihn zu melden.",
        "sv": "Fel uppt\u00e4ckt automatiskt \u2013 fyll i \u00e4rendet f\u00f6r att rapportera det.",
    }),
    ("ticket_title_label", {
        "it": "Titolo (*)",
        "en": "Title (*)",
        "ro": "Titlu (*)",
        "de": "Titel (*)",
        "sv": "Titel (*)",
    }),
    ("ticket_type_label", {
        "it": "Tipo",
        "en": "Type",
        "ro": "Tip",
        "de": "Typ",
        "sv": "Typ",
    }),
    ("ticket_type_exception", {
        "it": "\u26a0 Eccezione automatica",
        "en": "\u26a0 Automatic exception",
        "ro": "\u26a0 Excep\u021bie automat\u0103",
        "de": "\u26a0 Automatische Ausnahme",
        "sv": "\u26a0 Automatiskt undantag",
    }),
    ("ticket_type_manual", {
        "it": "\u2705 Manuale",
        "en": "\u2705 Manual",
        "ro": "\u2705 Manual",
        "de": "\u2705 Manuell",
        "sv": "\u2705 Manuellt",
    }),
    ("ticket_description_label", {
        "it": "Descrizione (*)",
        "en": "Description (*)",
        "ro": "Descriere (*)",
        "de": "Beschreibung (*)",
        "sv": "Beskrivning (*)",
    }),
    ("ticket_error_detail_label", {
        "it": "Dettaglio errore",
        "en": "Error detail",
        "ro": "Detaliu eroare",
        "de": "Fehlerdetail",
        "sv": "Feldetalj",
    }),
    ("ticket_log_label", {
        "it": "Log recente (ultime 50 righe)",
        "en": "Recent log (last 50 lines)",
        "ro": "Jurnal recent (ultimele 50 r\u00e2nduri)",
        "de": "Aktuelles Log (letzte 50 Zeilen)",
        "sv": "Senaste logg (sista 50 rader)",
    }),
    ("ticket_capture_btn", {
        "it": "\U0001f4f7 Cattura Screenshot",
        "en": "\U0001f4f7 Capture Screenshot",
        "ro": "\U0001f4f7 Captureaz\u0103 ecran",
        "de": "\U0001f4f7 Screenshot aufnehmen",
        "sv": "\U0001f4f7 Ta sk\u00e4rmbild",
    }),
    ("ticket_no_screenshot", {
        "it": "(nessuno screenshot)",
        "en": "(no screenshot)",
        "ro": "(f\u0103r\u0103 captur\u0103 de ecran)",
        "de": "(kein Screenshot)",
        "sv": "(ingen sk\u00e4rmbild)",
    }),
    ("ticket_screenshot_failed", {
        "it": "\u26a0 Screenshot non riuscito",
        "en": "\u26a0 Screenshot failed",
        "ro": "\u26a0 Captur\u0103 e\u015fuat\u0103",
        "de": "\u26a0 Screenshot fehlgeschlagen",
        "sv": "\u26a0 Sk\u00e4rmbild misslyckades",
    }),
    ("ticket_send_btn", {
        "it": "\U0001f4e8 Invia Ticket",
        "en": "\U0001f4e8 Send Ticket",
        "ro": "\U0001f4e8 Trimite Tichet",
        "de": "\U0001f4e8 Ticket senden",
        "sv": "\U0001f4e8 Skicka \u00e4rende",
    }),
    ("ticket_sending", {
        "it": "\u23f3 Invio in corso...",
        "en": "\u23f3 Sending...",
        "ro": "\u23f3 Se trimite...",
        "de": "\u23f3 Wird gesendet...",
        "sv": "\u23f3 Skickar...",
    }),
    ("ticket_title_required", {
        "it": "Inserire un titolo per il ticket.",
        "en": "Please enter a title for the ticket.",
        "ro": "Introduce\u021bi un titlu pentru tichet.",
        "de": "Bitte geben Sie einen Titel f\u00fcr das Ticket ein.",
        "sv": "Ange en rubrik f\u00f6r \u00e4rendet.",
    }),
    ("ticket_description_required", {
        "it": "Inserire una descrizione del problema.",
        "en": "Please enter a description of the issue.",
        "ro": "Introduce\u021bi o descriere a problemei.",
        "de": "Bitte geben Sie eine Beschreibung des Problems ein.",
        "sv": "Ange en beskrivning av problemet.",
    }),
    ("ticket_save_error", {
        "it": "Errore durante il salvataggio del ticket nel database.",
        "en": "Error saving the ticket to the database.",
        "ro": "Eroare la salvarea tichetului \u00een baza de date.",
        "de": "Fehler beim Speichern des Tickets in der Datenbank.",
        "sv": "Fel vid sparande av \u00e4rendet i databasen.",
    }),
    ("ticket_sent_ok", {
        "it": "Ticket #{id} registrato con successo.",
        "en": "Ticket #{id} registered successfully.",
        "ro": "Tichet #{id} \u00eenregistrat cu succes.",
        "de": "Ticket #{id} erfolgreich registriert.",
        "sv": "\u00c4rende #{id} registrerat.",
    }),
    ("ticket_send_error", {
        "it": "Errore durante invio ticket",
        "en": "Error sending ticket",
        "ro": "Eroare la trimiterea tichetului",
        "de": "Fehler beim Senden des Tickets",
        "sv": "Fel vid s\u00e4ndande av \u00e4rende",
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
            # Verifica esistenza
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

