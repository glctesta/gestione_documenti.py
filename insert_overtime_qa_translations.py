"""
insert_overtime_qa_translations.py
Inserisce le traduzioni del modulo Overtime Q&A in AppTranslations (5 lingue).
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
    # === Menu ===
    ("overtime_responses", {
        "it": "Risposte",
        "en": "Responses",
        "ro": "R\u0103spunsuri",
        "de": "Antworten",
        "sv": "Svar",
    }),

    # === Approval GUI - Ask Question Button ===
    ("ask_question", {
        "it": "Fai una domanda",
        "en": "Ask Question",
        "ro": "Pune o \u00eentrebare",
        "de": "Frage stellen",
        "sv": "St\u00e4ll fr\u00e5ga",
    }),

    # === Ask Question Dialog ===
    ("ask_question_title", {
        "it": "Domanda sulla richiesta straordinario",
        "en": "Question about Overtime Request",
        "ro": "\u00centrebare despre cererea de ore suplimentare",
        "de": "Frage zur \u00dcberstundenanfrage",
        "sv": "Fr\u00e5ga om \u00f6vertidsbeg\u00e4ran",
    }),
    ("request_reference", {
        "it": "Riferimento richiesta",
        "en": "Request Reference",
        "ro": "Referin\u021b\u0103 cerere",
        "de": "Antragsreferenz",
        "sv": "Beg\u00e4ransreferens",
    }),
    ("select_employee_optional", {
        "it": "Seleziona dipendente (opzionale)",
        "en": "Select Employee (optional)",
        "ro": "Selecta\u021bi angajatul (op\u021bional)",
        "de": "Mitarbeiter ausw\u00e4hlen (optional)",
        "sv": "V\u00e4lj anst\u00e4lld (valfritt)",
    }),
    ("your_question", {
        "it": "La tua domanda",
        "en": "Your Question",
        "ro": "\u00centrebarea dumneavoastr\u0103",
        "de": "Ihre Frage",
        "sv": "Din fr\u00e5ga",
    }),
    ("send_question", {
        "it": "Invia domanda",
        "en": "Send Question",
        "ro": "Trimite \u00eentrebarea",
        "de": "Frage senden",
        "sv": "Skicka fr\u00e5ga",
    }),
    ("question_empty", {
        "it": "Inserire il testo della domanda.",
        "en": "Please enter your question text.",
        "ro": "Introduce\u021bi textul \u00eentreb\u0103rii.",
        "de": "Bitte geben Sie Ihren Fragetext ein.",
        "sv": "Ange din fr\u00e5getext.",
    }),
    ("question_sent_ok", {
        "it": "Domanda inviata con successo.",
        "en": "Question sent successfully.",
        "ro": "\u00centrebarea a fost trimis\u0103 cu succes.",
        "de": "Frage erfolgreich gesendet.",
        "sv": "Fr\u00e5gan har skickats.",
    }),
    ("question_send_error", {
        "it": "Errore durante l'invio della domanda.",
        "en": "Error sending the question.",
        "ro": "Eroare la trimiterea \u00eentreb\u0103rii.",
        "de": "Fehler beim Senden der Frage.",
        "sv": "Fel vid s\u00e4ndning av fr\u00e5gan.",
    }),
    ("none_all", {
        "it": "-- Nessuno (generale) --",
        "en": "-- None (general) --",
        "ro": "-- Niciunul (general) --",
        "de": "-- Keiner (allgemein) --",
        "sv": "-- Ingen (allm\u00e4n) --",
    }),

    # === Responses (QA) Window ===
    ("overtime_qa_title", {
        "it": "Risposte Straordinari",
        "en": "Overtime Responses",
        "ro": "R\u0103spunsuri ore suplimentare",
        "de": "\u00dcberstunden-Antworten",
        "sv": "\u00d6vertidssvar",
    }),
    ("pending_questions", {
        "it": "Domande in attesa",
        "en": "Pending Questions",
        "ro": "\u00centreb\u0103ri \u00een a\u0219teptare",
        "de": "Offene Fragen",
        "sv": "V\u00e4ntande fr\u00e5gor",
    }),
    ("question_date", {
        "it": "Data domanda",
        "en": "Question Date",
        "ro": "Data \u00eentreb\u0103rii",
        "de": "Fragedatum",
        "sv": "Fr\u00e5gedatum",
    }),
    ("asked_by", {
        "it": "Chiesto da",
        "en": "Asked By",
        "ro": "\u00centrebat de",
        "de": "Gefragt von",
        "sv": "Fr\u00e5gad av",
    }),
    ("question_text", {
        "it": "Domanda",
        "en": "Question",
        "ro": "\u00centrebare",
        "de": "Frage",
        "sv": "Fr\u00e5ga",
    }),
    ("answer_status", {
        "it": "Stato",
        "en": "Status",
        "ro": "Stare",
        "de": "Status",
        "sv": "Status",
    }),
    ("pending", {
        "it": "In attesa",
        "en": "Pending",
        "ro": "\u00cen a\u0219teptare",
        "de": "Ausstehend",
        "sv": "V\u00e4ntar",
    }),
    ("answered", {
        "it": "Risposto",
        "en": "Answered",
        "ro": "R\u0103spuns",
        "de": "Beantwortet",
        "sv": "Besvarad",
    }),
    ("reply", {
        "it": "Rispondi",
        "en": "Reply",
        "ro": "R\u0103spunde",
        "de": "Antworten",
        "sv": "Svara",
    }),
    ("select_question", {
        "it": "Selezionare una domanda.",
        "en": "Please select a question.",
        "ro": "Selecta\u021bi o \u00eentrebare.",
        "de": "Bitte w\u00e4hlen Sie eine Frage.",
        "sv": "V\u00e4lj en fr\u00e5ga.",
    }),
    ("already_answered", {
        "it": "Questa domanda ha gi\u00e0 una risposta.",
        "en": "This question has already been answered.",
        "ro": "Aceast\u0103 \u00eentrebare a primit deja r\u0103spuns.",
        "de": "Diese Frage wurde bereits beantwortet.",
        "sv": "Denna fr\u00e5ga har redan besvarats.",
    }),

    # === Reply Dialog ===
    ("reply_title", {
        "it": "Rispondi alla domanda",
        "en": "Reply to Question",
        "ro": "R\u0103spunde la \u00eentrebare",
        "de": "Auf Frage antworten",
        "sv": "Svara p\u00e5 fr\u00e5ga",
    }),
    ("original_question", {
        "it": "Domanda originale",
        "en": "Original Question",
        "ro": "\u00centrebarea original\u0103",
        "de": "Urspr\u00fcngliche Frage",
        "sv": "Ursprunglig fr\u00e5ga",
    }),
    ("regarding_employee", {
        "it": "Riguardo al dipendente",
        "en": "Regarding Employee",
        "ro": "Referitor la angajatul",
        "de": "Betreffend Mitarbeiter",
        "sv": "G\u00e4llande anst\u00e4lld",
    }),
    ("your_answer", {
        "it": "La tua risposta",
        "en": "Your Answer",
        "ro": "R\u0103spunsul dumneavoastr\u0103",
        "de": "Ihre Antwort",
        "sv": "Ditt svar",
    }),
    ("send_answer", {
        "it": "Invia risposta",
        "en": "Send Answer",
        "ro": "Trimite r\u0103spunsul",
        "de": "Antwort senden",
        "sv": "Skicka svar",
    }),
    ("answer_empty", {
        "it": "Inserire il testo della risposta.",
        "en": "Please enter your answer text.",
        "ro": "Introduce\u021bi textul r\u0103spunsului.",
        "de": "Bitte geben Sie Ihren Antworttext ein.",
        "sv": "Ange ditt svarstext.",
    }),
    ("answer_sent_ok", {
        "it": "Risposta inviata con successo.",
        "en": "Answer sent successfully.",
        "ro": "R\u0103spunsul a fost trimis cu succes.",
        "de": "Antwort erfolgreich gesendet.",
        "sv": "Svaret har skickats.",
    }),
    ("answer_send_error", {
        "it": "Errore durante l'invio della risposta.",
        "en": "Error sending the answer.",
        "ro": "Eroare la trimiterea r\u0103spunsului.",
        "de": "Fehler beim Senden der Antwort.",
        "sv": "Fel vid s\u00e4ndning av svaret.",
    }),
    ("no_pending_questions", {
        "it": "Non ci sono domande in attesa di risposta.",
        "en": "There are no pending questions.",
        "ro": "Nu exist\u0103 \u00eentreb\u0103ri \u00een a\u0219teptare.",
        "de": "Es gibt keine offenen Fragen.",
        "sv": "Det finns inga v\u00e4ntande fr\u00e5gor.",
    }),
    ("employee_reference", {
        "it": "Dipendente di riferimento",
        "en": "Referenced Employee",
        "ro": "Angajatul de referin\u021b\u0103",
        "de": "Referenzierter Mitarbeiter",
        "sv": "Refererad anst\u00e4lld",
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
