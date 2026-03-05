"""Inserisce traduzioni per la feature X-Ray verification in en, ro, it, de, sv."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config_manager import ConfigManager
import pyodbc

cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
c = cfg.load_config()
conn = pyodbc.connect(
    f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
    f"UID={c['username']};PWD={c['password']};TrustServerCertificate=Yes"
)
cur = conn.cursor()

translations = [
    # ip_user_pass_label
    ('en', 'ip_user_pass_label', 'Data source/userid/pass'),
    ('ro', 'ip_user_pass_label', 'Preluare date/userid/parol\u0103'),
    ('it', 'ip_user_pass_label', 'Prelievodati/userid/pass'),
    ('de', 'ip_user_pass_label', 'Datenabruf/Benutzer/Passwort'),
    ('sv', 'ip_user_pass_label', 'Datak\u00e4lla/anv\u00e4ndare/l\u00f6senord'),

    # xray_enter_label_first
    ('en', 'xray_enter_label_first', 'Please enter the Label Code before checking this task.'),
    ('ro', 'xray_enter_label_first', 'V\u0103 rug\u0103m s\u0103 introduce\u021bi Codul etichetei \u00eenainte de a bifa aceast\u0103 sarcin\u0103.'),
    ('it', 'xray_enter_label_first', 'Inserire il codice etichetta prima di biffarre questo task.'),
    ('de', 'xray_enter_label_first', 'Bitte geben Sie den Etikettencode ein, bevor Sie diese Aufgabe abhaken.'),
    ('sv', 'xray_enter_label_first', 'Ange etikettkoden innan du markerar denna uppgift.'),

    # xray_pdf_found
    ('en', 'xray_pdf_found', 'X-Ray PDF report found and will be saved with the verification.'),
    ('ro', 'xray_pdf_found', 'Raportul PDF X-Ray a fost g\u0103sit \u0219i va fi salvat \u00eempreun\u0103 cu verificarea.'),
    ('it', 'xray_pdf_found', 'Rapporto PDF X-Ray trovato e verr\u00e0 salvato con la verifica.'),
    ('de', 'xray_pdf_found', 'R\u00f6ntgen-PDF-Bericht gefunden und wird mit der Pr\u00fcfung gespeichert.'),
    ('sv', 'xray_pdf_found', 'R\u00f6ntgen-PDF-rapport hittad och kommer att sparas med verifieringen.'),

    # xray_connection_error
    ('en', 'xray_connection_error', 'Cannot connect to the X-Ray report directory. Please check the network connection and try again.'),
    ('ro', 'xray_connection_error', 'Nu se poate conecta la directorul de rapoarte X-Ray. Verifica\u021bi conexiunea de re\u021bea \u0219i \u00eencerca\u021bi din nou.'),
    ('it', 'xray_connection_error', 'Impossibile connettersi alla directory dei report X-Ray. Verificare la connessione di rete e riprovare.'),
    ('de', 'xray_connection_error', 'Verbindung zum R\u00f6ntgenbericht-Verzeichnis nicht m\u00f6glich. Bitte Netzwerkverbindung pr\u00fcfen und erneut versuchen.'),
    ('sv', 'xray_connection_error', 'Kan inte ansluta till r\u00f6ntgenrapportmappen. Kontrollera n\u00e4tverksanslutningen och f\u00f6rs\u00f6k igen.'),

    # xray_pdf_not_found_msg
    ('en', 'xray_pdf_not_found_msg', 'The X-Ray PDF report for Label Code "{label_code}" was not found in the verification directory.\n\nIMPORTANT: The PDF document MUST be saved using the Label Code as the file name (e.g. "{label_code}.pdf").\n\nYou cannot check this task without the verification document.\nDo you still want to proceed? (The check will be marked as NOT verified and a notification email will be sent.)'),
    ('ro', 'xray_pdf_not_found_msg', 'Raportul PDF X-Ray pentru Codul etichetei "{label_code}" nu a fost g\u0103sit \u00een directorul de verificare.\n\nIMPORTANT: Documentul PDF TREBUIE salvat folosind Codul etichetei ca nume de fi\u0219ier (ex. "{label_code}.pdf").\n\nNu pute\u021bi bifa aceast\u0103 sarcin\u0103 f\u0103r\u0103 documentul de verificare.\nDori\u021bi s\u0103 continua\u021bi? (Controlul va fi marcat ca NEVERIFICAT \u0219i un email de notificare va fi trimis.)'),
    ('it', 'xray_pdf_not_found_msg', 'Il rapporto PDF X-Ray per il Codice Etichetta "{label_code}" non \u00e8 stato trovato nella directory di verifica.\n\nIMPORTANTE: Il documento PDF DEVE essere salvato usando il Codice Etichetta come nome file (es. "{label_code}.pdf").\n\nNon \u00e8 possibile biffarre questo controllo senza il documento di verifica.\nSi desidera comunque procedere? (Il controllo verr\u00e0 salvato come NON verificato e verr\u00e0 inviata una email di notifica.)'),
    ('de', 'xray_pdf_not_found_msg', 'Der R\u00f6ntgen-PDF-Bericht f\u00fcr Etikettencode "{label_code}" wurde im Pr\u00fcfverzeichnis nicht gefunden.\n\nWICHTIG: Das PDF-Dokument MUSS mit dem Etikettencode als Dateiname gespeichert werden (z.B. "{label_code}.pdf").\n\nSie k\u00f6nnen diese Aufgabe nicht ohne das Pr\u00fcfdokument abhaken.\nM\u00f6chten Sie trotzdem fortfahren? (Die Pr\u00fcfung wird als NICHT verifiziert markiert und eine Benachrichtigungs-E-Mail wird gesendet.)'),
    ('sv', 'xray_pdf_not_found_msg', 'R\u00f6ntgen-PDF-rapporten f\u00f6r etikettkod "{label_code}" hittades inte i verifieringsmappen.\n\nVIKTIGT: PDF-dokumentet M\u00c5STE sparas med etikettkoden som filnamn (t.ex. "{label_code}.pdf").\n\nDu kan inte markera denna uppgift utan verifieringsdokumentet.\nVill du \u00e4nd\u00e5 forts\u00e4tta? (Kontrollen markeras som EJ verifierad och ett meddelande skickas via e-post.)'),
]

count = 0
for lang, key, value in translations:
    cur.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations]
            WHERE LanguageCode = ? AND TranslationKey = ?
        )
        INSERT INTO [Traceability_RS].[dbo].[AppTranslations]
            (LanguageCode, TranslationKey, TranslationValue)
        VALUES (?, ?, ?)
    """, lang, key, lang, key, value)
    count += 1

conn.commit()
print(f"Inserted/verified {count} translations.")
conn.close()
