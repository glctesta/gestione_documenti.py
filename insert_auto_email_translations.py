# -*- coding: utf-8 -*-
"""
insert_auto_email_translations.py
Traduzioni per la gestione iscrizioni email automatiche (auto_email_settings_gui)
e la voce di menu Strumenti. 5 lingue (it, en, ro, de, sv). Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('submenu_auto_email_subscriptions', 'Iscrizioni email automatiche',
     'Automatic email subscriptions', 'Abonări email automate',
     'Automatische E-Mail-Abos', 'Automatiska e-postprenumerationer'),
    ('aes_title', 'Iscrizioni Email Automatiche', 'Automatic Email Subscriptions',
     'Abonări Email Automate', 'Automatische E-Mail-Abos', 'Automatiska e-postprenumerationer'),
    ('aes_open_error', 'Impossibile aprire le iscrizioni email',
     'Cannot open email subscriptions', 'Nu se pot deschide abonările email',
     'E-Mail-Abos können nicht geöffnet werden', 'Kan inte öppna e-postprenumerationer'),
    ('aes_user_info', 'Utente: {0}   —   Email: {1}', 'User: {0}   —   Email: {1}',
     'Utilizator: {0}   —   Email: {1}', 'Benutzer: {0}   —   E-Mail: {1}',
     'Användare: {0}   —   E-post: {1}'),
    ('aes_no_email', '(non trovata)', '(not found)', '(negăsit)', '(nicht gefunden)', '(hittades inte)'),
    ('aes_hint',
     'Iscriviti ai servizi che ti interessano o disiscriviti da quelli che non vuoi più ricevere. '
     'Per disiscriversi da un servizio obbligatorio serve un super user.',
     'Subscribe to the services you want or unsubscribe from those you no longer want. '
     'Unsubscribing from a mandatory service requires a super user.',
     'Abonează-te la serviciile dorite sau dezabonează-te de la cele nedorite. '
     'Dezabonarea de la un serviciu obligatoriu necesită un super user.',
     'Abonnieren Sie gewünschte Dienste oder bestellen Sie nicht mehr gewünschte ab. '
     'Das Abbestellen eines Pflicht-Dienstes erfordert einen Superuser.',
     'Prenumerera på tjänster du vill ha eller avsluta dem du inte vill ha. '
     'Att avsluta en obligatorisk tjänst kräver en superanvändare.'),
    ('aes_search', 'Cerca', 'Search', 'Caută', 'Suchen', 'Sök'),
    ('aes_clear_filter', '✖ Azzera', '✖ Clear', '✖ Șterge', '✖ Zurücksetzen', '✖ Rensa'),
    ('aes_f_all', 'Tutti', 'All', 'Toate', 'Alle', 'Alla'),
    ('aes_f_sub', 'Solo iscritti', 'Subscribed only', 'Doar abonate',
     'Nur abonnierte', 'Endast prenumererade'),
    ('aes_f_unsub', 'Solo non iscritti', 'Not subscribed only', 'Doar neabonate',
     'Nur nicht abonnierte', 'Endast ej prenumererade'),
    ('aes_count', '{0} di {1} servizi', '{0} of {1} services', '{0} din {1} servicii',
     '{0} von {1} Diensten', '{0} av {1} tjänster'),
    ('aes_c_sub', 'Iscritto', 'Subscribed', 'Abonat', 'Abonniert', 'Prenumererad'),
    ('aes_btn_sub', '✅ Iscriviti', '✅ Subscribe', '✅ Abonează-te',
     '✅ Abonnieren', '✅ Prenumerera'),
    ('aes_sub_confirm', 'Vuoi iscriverti a "{0}"?', 'Subscribe to "{0}"?',
     'Vă abonați la "{0}"?', '"{0}" abonnieren?', 'Prenumerera på "{0}"?'),
    ('aes_sub_done', 'Riceverai questa email.', 'You will now receive this email.',
     'Veți primi acest email.', 'Sie erhalten diese E-Mail ab jetzt.',
     'Du kommer nu att få detta e-postmeddelande.'),
    ('aes_already_sub', 'Sei già iscritto a questo servizio.',
     'You are already subscribed to this service.', 'Sunteți deja abonat la acest serviciu.',
     'Sie haben diesen Dienst bereits abonniert.', 'Du prenumererar redan på denna tjänst.'),
    ('aes_not_sub', 'Non sei iscritto a questo servizio.',
     'You are not subscribed to this service.', 'Nu sunteți abonat la acest serviciu.',
     'Sie haben diesen Dienst nicht abonniert.', 'Du prenumererar inte på denna tjänst.'),
    ('aes_c_attr', 'Servizio (attributo)', 'Service (attribute)', 'Serviciu (atribut)',
     'Dienst (Attribut)', 'Tjänst (attribut)'),
    ('aes_c_name', 'Descrizione', 'Description', 'Descriere', 'Beschreibung', 'Beskrivning'),
    ('aes_c_value', 'Destinatari', 'Recipients', 'Destinatari', 'Empfänger', 'Mottagare'),
    ('aes_c_mand', 'Obbligatoria', 'Mandatory', 'Obligatoriu', 'Pflicht', 'Obligatorisk'),
    ('aes_btn_unsub', '🚫 Non ricevere più', '🚫 Unsubscribe', '🚫 Dezabonare',
     '🚫 Abbestellen', '🚫 Avsluta prenumeration'),
    ('aes_btn_admin', '🔧 Gestione servizi (super user)', '🔧 Manage services (super user)',
     '🔧 Gestionare servicii (super user)', '🔧 Dienste verwalten (Superuser)',
     '🔧 Hantera tjänster (superanvändare)'),
    ('aes_select_row', 'Seleziona un servizio.', 'Select a service.', 'Selectați un serviciu.',
     'Wählen Sie einen Dienst.', 'Välj en tjänst.'),
    ('aes_unsub_confirm', 'Vuoi smettere di ricevere "{0}"?', 'Stop receiving "{0}"?',
     'Nu mai primiți "{0}"?', '"{0}" nicht mehr erhalten?', 'Sluta ta emot "{0}"?'),
    ('aes_unsub_done', 'Non riceverai più questa email.', 'You will no longer receive this email.',
     'Nu veți mai primi acest email.', 'Sie erhalten diese E-Mail nicht mehr.',
     'Du kommer inte längre att få detta e-postmeddelande.'),
    ('aes_mand_needs_super',
     'Questo servizio è obbligatorio: serve l\'autorizzazione di un super user.',
     'This service is mandatory: super user authorization is required.',
     'Acest serviciu este obligatoriu: necesită autorizarea unui super user.',
     'Dieser Dienst ist Pflicht: Superuser-Autorisierung erforderlich.',
     'Denna tjänst är obligatorisk: superanvändare krävs.'),
    ('aes_no_email_msg',
     'Impossibile determinare la tua email aziendale.\nNessun servizio da mostrare.',
     'Cannot determine your work email.\nNo services to show.',
     'Nu se poate determina emailul dvs. de serviciu.\nNiciun serviciu de afișat.',
     'Ihre Arbeits-E-Mail konnte nicht ermittelt werden.\nKeine Dienste anzuzeigen.',
     'Kan inte fastställa din arbetsmejl.\nInga tjänster att visa.'),
    ('aes_no_auth', 'Autorizzazione non disponibile.', 'Authorization not available.',
     'Autorizare indisponibilă.', 'Autorisierung nicht verfügbar.', 'Auktorisering ej tillgänglig.'),
    ('aes_admin_title', 'Gestione Servizi Email Automatiche (super user)',
     'Automatic Email Services Management (super user)',
     'Gestionare Servicii Email Automate (super user)',
     'Verwaltung automatischer E-Mail-Dienste (Superuser)',
     'Hantering av automatiska e-posttjänster (superanvändare)'),
    ('aes_editor', 'Modifica servizio selezionato', 'Edit selected service',
     'Editează serviciul selectat', 'Ausgewählten Dienst bearbeiten', 'Redigera vald tjänst'),
    ('aes_mandatory', 'Obbligatoria (non disattivabile dagli utenti)',
     'Mandatory (users cannot opt out)', 'Obligatoriu (utilizatorii nu pot renunța)',
     'Pflicht (Benutzer können nicht abbestellen)', 'Obligatorisk (användare kan inte avstå)'),
    ('aes_btn_save', '💾 Salva modifiche', '💾 Save changes', '💾 Salvează modificările',
     '💾 Änderungen speichern', '💾 Spara ändringar'),
    ('aes_btn_add', '➕ Aggiungi servizio', '➕ Add service', '➕ Adaugă serviciu',
     '➕ Dienst hinzufügen', '➕ Lägg till tjänst'),
    ('aes_saved', 'Modifiche salvate.', 'Changes saved.', 'Modificări salvate.',
     'Änderungen gespeichert.', 'Ändringar sparade.'),
    ('aes_add_title', 'Nuovo servizio email', 'New email service', 'Serviciu email nou',
     'Neuer E-Mail-Dienst', 'Ny e-posttjänst'),
    ('aes_btn_create', 'Crea', 'Create', 'Creează', 'Erstellen', 'Skapa'),
    ('aes_attr_required', 'Il nome attributo è obbligatorio.', 'The attribute name is required.',
     'Numele atributului este obligatoriu.', 'Der Attributname ist erforderlich.',
     'Attributnamnet är obligatoriskt.'),
    ('aes_attr_dup', 'Esiste già un servizio con questo attributo.',
     'A service with this attribute already exists.', 'Există deja un serviciu cu acest atribut.',
     'Ein Dienst mit diesem Attribut existiert bereits.', 'En tjänst med detta attribut finns redan.'),
    ('aes_added', 'Servizio aggiunto.', 'Service added.', 'Serviciu adăugat.',
     'Dienst hinzugefügt.', 'Tjänst tillagd.'),
    # chiavi comuni (inserite solo se mancanti)
    ('yes', 'Sì', 'Yes', 'Da', 'Ja', 'Ja'),
    ('no', 'No', 'No', 'Nu', 'Nein', 'Nej'),
    ('confirm', 'Conferma', 'Confirm', 'Confirmare', 'Bestätigen', 'Bekräfta'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')

# Chiavi il cui testo e' cambiato: vanno riscritte anche se gia' presenti.
REFRESH = {'aes_hint'}


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = upd = skip = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            elif key in REFRESH:
                cur.execute("UPDATE Traceability_rs.dbo.AppTranslations SET TranslationValue = ? "
                            "WHERE LanguageCode = ? AND TranslationKey = ?",
                            (row[i + 1], lang, key))
                upd += 1
            else:
                skip += 1
    conn.commit()
    conn.close()
    print(f"[OK] Auto-email translations - Inserite: {ins}, Aggiornate: {upd}, Saltate: {skip}")


if __name__ == '__main__':
    main()
