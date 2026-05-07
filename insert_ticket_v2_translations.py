"""
insert_ticket_v2_translations.py
Inserisce le traduzioni v2 del modulo Ticket (sottomenu, storico, gestione, notifiche).
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
    # ── Menu voci ──
    ("menu_open_ticket", {
        "it": "Apri Ticket",
        "en": "Open Ticket",
        "ro": "Deschide Tichet",
        "de": "Ticket \u00f6ffnen",
        "sv": "\u00d6ppna \u00e4rende",
    }),
    ("menu_view_tickets", {
        "it": "Visualizza Ticket",
        "en": "View Tickets",
        "ro": "Vizualizeaz\u0103 Tichete",
        "de": "Tickets anzeigen",
        "sv": "Visa \u00e4renden",
    }),
    ("menu_manage_tickets", {
        "it": "Chiudi Ticket",
        "en": "Manage Tickets",
        "ro": "\u00cenchide Tichete",
        "de": "Tickets verwalten",
        "sv": "Hantera \u00e4renden",
    }),

    # ── Finestra apertura ticket ──
    ("ticket_user_label", {
        "it": "Utente",
        "en": "User",
        "ro": "Utilizator",
        "de": "Benutzer",
        "sv": "Anv\u00e4ndare",
    }),

    # ── Storico ticket ──
    ("ticket_history_title", {
        "it": "Storico Ticket",
        "en": "Ticket History",
        "ro": "Istoric Tichete",
        "de": "Ticket-Verlauf",
        "sv": "\u00c4rendehistorik",
    }),
    ("ticket_history_header", {
        "it": "I tuoi Ticket",
        "en": "Your Tickets",
        "ro": "Tichetele tale",
        "de": "Deine Tickets",
        "sv": "Dina \u00e4renden",
    }),

    # ── Colonne treeview ──
    ("ticket_col_date", {
        "it": "Data Apertura",
        "en": "Opened Date",
        "ro": "Data Deschidere",
        "de": "Er\u00f6ffnungsdatum",
        "sv": "\u00d6ppningsdatum",
    }),
    ("ticket_col_title", {
        "it": "Titolo",
        "en": "Title",
        "ro": "Titlu",
        "de": "Titel",
        "sv": "Titel",
    }),
    ("ticket_col_type", {
        "it": "Tipo",
        "en": "Type",
        "ro": "Tip",
        "de": "Typ",
        "sv": "Typ",
    }),
    ("ticket_col_status", {
        "it": "Stato",
        "en": "Status",
        "ro": "Stare",
        "de": "Status",
        "sv": "Status",
    }),
    ("ticket_col_closed_at", {
        "it": "Data Chiusura",
        "en": "Closed Date",
        "ro": "Data \u00cenchidere",
        "de": "Schlie\u00dfdatum",
        "sv": "St\u00e4ngningsdatum",
    }),
    ("ticket_col_closed_by", {
        "it": "Chiuso da",
        "en": "Closed by",
        "ro": "\u00cenchis de",
        "de": "Geschlossen von",
        "sv": "St\u00e4ngd av",
    }),
    ("ticket_col_closure_note", {
        "it": "Nota Chiusura",
        "en": "Closure Note",
        "ro": "Not\u0103 \u00cenchidere",
        "de": "Abschlussnotiz",
        "sv": "St\u00e4ngningsnotering",
    }),
    ("ticket_col_opened_by", {
        "it": "Aperto da",
        "en": "Opened by",
        "ro": "Deschis de",
        "de": "Er\u00f6ffnet von",
        "sv": "\u00d6ppnad av",
    }),
    ("ticket_col_email", {
        "it": "Email",
        "en": "Email",
        "ro": "Email",
        "de": "E-Mail",
        "sv": "E-post",
    }),

    # ── Stati ticket ──
    ("ticket_status_open", {
        "it": "Aperto",
        "en": "Open",
        "ro": "Deschis",
        "de": "Offen",
        "sv": "\u00d6ppen",
    }),
    ("ticket_status_on_working", {
        "it": "In Lavorazione",
        "en": "On Working",
        "ro": "\u00cen Lucru",
        "de": "In Bearbeitung",
        "sv": "Under Arbete",
    }),
    ("ticket_status_closed", {
        "it": "Chiuso",
        "en": "Closed",
        "ro": "\u00cenchis",
        "de": "Geschlossen",
        "sv": "St\u00e4ngd",
    }),

    # ── Gestione ticket (admin) ──
    ("ticket_manage_title", {
        "it": "Gestione Ticket",
        "en": "Ticket Management",
        "ro": "Gestionare Tichete",
        "de": "Ticket-Verwaltung",
        "sv": "\u00c4rendehantering",
    }),
    ("ticket_manage_header", {
        "it": "Gestione Ticket \u2013 Tutti i ticket",
        "en": "Ticket Management \u2013 All tickets",
        "ro": "Gestionare Tichete \u2013 Toate tichetele",
        "de": "Ticket-Verwaltung \u2013 Alle Tickets",
        "sv": "\u00c4rendehantering \u2013 Alla \u00e4renden",
    }),
    ("ticket_filter_status", {
        "it": "Stato:",
        "en": "Status:",
        "ro": "Stare:",
        "de": "Status:",
        "sv": "Status:",
    }),
    ("ticket_filter_all", {
        "it": "Tutti",
        "en": "All",
        "ro": "Toate",
        "de": "Alle",
        "sv": "Alla",
    }),
    ("ticket_btn_set_working", {
        "it": "\U0001f527 In Lavorazione",
        "en": "\U0001f527 On Working",
        "ro": "\U0001f527 \u00cen Lucru",
        "de": "\U0001f527 In Bearbeitung",
        "sv": "\U0001f527 Under Arbete",
    }),
    ("ticket_btn_close_ticket", {
        "it": "\u2705 Chiudi Ticket",
        "en": "\u2705 Close Ticket",
        "ro": "\u2705 \u00cenchide Tichet",
        "de": "\u2705 Ticket schlie\u00dfen",
        "sv": "\u2705 St\u00e4ng \u00e4rende",
    }),
    ("ticket_btn_reopen", {
        "it": "\U0001f504 Riapri",
        "en": "\U0001f504 Reopen",
        "ro": "\U0001f504 Redeschide",
        "de": "\U0001f504 Wieder\u00f6ffnen",
        "sv": "\U0001f504 \u00c5ter\u00f6ppna",
    }),
    ("ticket_btn_view_detail", {
        "it": "\U0001f4cb Dettagli",
        "en": "\U0001f4cb Details",
        "ro": "\U0001f4cb Detalii",
        "de": "\U0001f4cb Details",
        "sv": "\U0001f4cb Detaljer",
    }),
    ("ticket_btn_refresh", {
        "it": "\U0001f504 Aggiorna",
        "en": "\U0001f504 Refresh",
        "ro": "\U0001f504 Actualizeaz\u0103",
        "de": "\U0001f504 Aktualisieren",
        "sv": "\U0001f504 Uppdatera",
    }),
    ("ticket_select_one", {
        "it": "Selezionare un ticket dalla lista.",
        "en": "Select a ticket from the list.",
        "ro": "Selecta\u021bi un tichet din list\u0103.",
        "de": "W\u00e4hlen Sie ein Ticket aus der Liste.",
        "sv": "V\u00e4lj ett \u00e4rende fr\u00e5n listan.",
    }),
    ("ticket_already_status", {
        "it": "Il ticket \u00e8 gi\u00e0 in questo stato.",
        "en": "The ticket is already in this status.",
        "ro": "Tichetul este deja \u00een aceast\u0103 stare.",
        "de": "Das Ticket ist bereits in diesem Status.",
        "sv": "\u00c4rendet \u00e4r redan i denna status.",
    }),
    ("ticket_closed_cannot_change", {
        "it": "Un ticket chiuso pu\u00f2 solo essere riaperto.",
        "en": "A closed ticket can only be reopened.",
        "ro": "Un tichet \u00eenchis poate fi doar redeschis.",
        "de": "Ein geschlossenes Ticket kann nur wieder ge\u00f6ffnet werden.",
        "sv": "Ett st\u00e4ngt \u00e4rende kan bara \u00e5ter\u00f6ppnas.",
    }),
    ("ticket_status_update_error", {
        "it": "Errore durante il cambio stato del ticket.",
        "en": "Error changing ticket status.",
        "ro": "Eroare la schimbarea st\u0103rii tichetului.",
        "de": "Fehler beim \u00c4ndern des Ticket-Status.",
        "sv": "Fel vid \u00e4ndring av \u00e4rendestatus.",
    }),
    ("ticket_already_closed", {
        "it": "Il ticket \u00e8 gi\u00e0 chiuso.",
        "en": "The ticket is already closed.",
        "ro": "Tichetul este deja \u00eenchis.",
        "de": "Das Ticket ist bereits geschlossen.",
        "sv": "\u00c4rendet \u00e4r redan st\u00e4ngt.",
    }),

    # ── Dialogo chiusura ticket ──
    ("ticket_close_dialog_title", {
        "it": "Chiudi Ticket",
        "en": "Close Ticket",
        "ro": "\u00cenchide Tichet",
        "de": "Ticket schlie\u00dfen",
        "sv": "St\u00e4ng \u00e4rende",
    }),
    ("ticket_closing_header", {
        "it": "Chiusura Ticket",
        "en": "Closing Ticket",
        "ro": "\u00cenchidere Tichet",
        "de": "Ticket-Abschluss",
        "sv": "St\u00e4ngning av \u00e4rende",
    }),
    ("ticket_closure_note_label", {
        "it": "Nota di risoluzione (*):",
        "en": "Resolution note (*):",
        "ro": "Not\u0103 de rezolvare (*):",
        "de": "L\u00f6sungshinweis (*):",
        "sv": "L\u00f6sningsanteckning (*):",
    }),
    ("ticket_closure_note_required", {
        "it": "Inserire una nota di risoluzione per chiudere il ticket.",
        "en": "Please enter a resolution note to close the ticket.",
        "ro": "Introduce\u021bi o not\u0103 de rezolvare pentru a \u00eenchide tichetul.",
        "de": "Bitte geben Sie einen L\u00f6sungshinweis ein, um das Ticket zu schlie\u00dfen.",
        "sv": "Ange en l\u00f6sningsanteckning f\u00f6r att st\u00e4nga \u00e4rendet.",
    }),
    ("ticket_close_error", {
        "it": "Errore durante la chiusura del ticket.",
        "en": "Error closing the ticket.",
        "ro": "Eroare la \u00eenchiderea tichetului.",
        "de": "Fehler beim Schlie\u00dfen des Tickets.",
        "sv": "Fel vid st\u00e4ngning av \u00e4rendet.",
    }),
    ("ticket_btn_confirm_close", {
        "it": "\u2705 Conferma Chiusura",
        "en": "\u2705 Confirm Close",
        "ro": "\u2705 Confirm\u0103 \u00cenchiderea",
        "de": "\u2705 Schlie\u00dfung best\u00e4tigen",
        "sv": "\u2705 Bekr\u00e4fta st\u00e4ngning",
    }),
    ("ticket_closed_ok", {
        "it": "Ticket #{id} chiuso con successo.",
        "en": "Ticket #{id} closed successfully.",
        "ro": "Tichet #{id} \u00eenchis cu succes.",
        "de": "Ticket #{id} erfolgreich geschlossen.",
        "sv": "\u00c4rende #{id} st\u00e4ngt.",
    }),

    # ── Notifica popup ticket chiuso ──
    ("ticket_closed_popup_title", {
        "it": "Ticket Risolto",
        "en": "Ticket Resolved",
        "ro": "Tichet Rezolvat",
        "de": "Ticket gel\u00f6st",
        "sv": "\u00c4rende l\u00f6st",
    }),
    ("ticket_closed_popup_header", {
        "it": "Il tuo ticket \u00e8 stato risolto!",
        "en": "Your ticket has been resolved!",
        "ro": "Tichetul t\u0103u a fost rezolvat!",
        "de": "Dein Ticket wurde gel\u00f6st!",
        "sv": "Ditt \u00e4rende har l\u00f6sts!",
    }),
    ("ticket_closed_by", {
        "it": "Chiuso da",
        "en": "Closed by",
        "ro": "\u00cenchis de",
        "de": "Geschlossen von",
        "sv": "St\u00e4ngd av",
    }),
    ("ticket_closed_at", {
        "it": "Data chiusura",
        "en": "Closed date",
        "ro": "Data \u00eenchidere",
        "de": "Abschlussdatum",
        "sv": "St\u00e4ngningsdatum",
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
