# -*- coding: utf-8 -*-
"""Traduzioni per la form Gestione Account Manager clienti (client_account_managers_gui)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('submenu_account_managers', '👤 Account Manager Clienti', '👤 Client Account Managers',
     '👤 Account Manageri Clienti', '👤 Kunden-Account-Manager', '👤 Kundansvariga'),
    ('cam_title', 'Gestione Account Manager Clienti', 'Client Account Manager Management',
     'Gestionare Account Manageri Clienti', 'Verwaltung Kunden-Account-Manager', 'Hantering av kundansvariga'),
    ('cam_final_clients', 'Clienti finali', 'Final clients', 'Clienti finali', 'Endkunden', 'Slutkunder'),
    ('cam_col_client', 'Cliente finale', 'Final client', 'Client final', 'Endkunde', 'Slutkund'),
    ('cam_col_acronym', 'Acronimo', 'Acronym', 'Acronim', 'Akronym', 'Akronym'),
    ('cam_select_client', 'Seleziona un cliente finale', 'Select a final client',
     'Selectati un client final', 'Endkunde auswaehlen', 'Vaelj en slutkund'),
    ('cam_managers', 'Account Manager (destinatari TO)', 'Account Managers (TO recipients)',
     'Account Manageri (destinatari TO)', 'Account-Manager (TO-Empfaenger)', 'Kundansvariga (TO-mottagare)'),
    ('cam_col_name', 'Nome', 'Name', 'Nume', 'Vorname', 'Foernamn'),
    ('cam_col_surname', 'Cognome', 'Surname', 'Prenume', 'Nachname', 'Efternamn'),
    ('cam_col_email', 'Email', 'Email', 'Email', 'Email', 'E-post'),
    ('cam_col_phone', 'Telefono', 'Phone', 'Telefon', 'Telefon', 'Telefon'),
    ('cam_col_manager', 'Account Manager', 'Account Manager', 'Account Manager',
     'Account-Manager', 'Kundansvarig'),
    ('cam_new', 'Nuovo + associa', 'New + associate', 'Nou + asociaza', 'Neu + zuordnen', 'Ny + koppla'),
    ('cam_associate', 'Associa', 'Associate', 'Asociaza', 'Zuordnen', 'Koppla'),
    ('cam_edit', 'Modifica', 'Edit', 'Modifica', 'Bearbeiten', 'Redigera'),
    ('cam_remove', 'Rimuovi associazione', 'Remove association', 'Elimina asociere',
     'Zuordnung entfernen', 'Ta bort koppling'),
    ('cam_cc', 'Destinatari in CC (Sys_email_<cliente>)', 'CC recipients (Sys_email_<client>)',
     'Destinatari CC (Sys_email_<client>)', 'CC-Empfaenger (Sys_email_<Kunde>)', 'CC-mottagare (Sys_email_<kund>)'),
    ('cam_save_cc', 'Salva CC', 'Save CC', 'Salveaza CC', 'CC speichern', 'Spara CC'),
    ('cam_send_prefs', 'Invio automatico email', 'Automatic email sending', 'Trimitere automata email',
     'Automatischer E-Mail-Versand', 'Automatiskt e-postutskick'),
    ('cam_send_am', 'Invia agli Account Manager (TO)', 'Send to Account Managers (TO)',
     'Trimite catre Account Manageri (TO)', 'An Account-Manager senden (TO)', 'Skicka till kundansvariga (TO)'),
    ('cam_send_cc', 'Invia ai destinatari CC', 'Send to CC recipients', 'Trimite catre destinatarii CC',
     'An CC-Empfaenger senden', 'Skicka till CC-mottagare'),
    ('cam_saved', 'Salvato.', 'Saved.', 'Salvat.', 'Gespeichert.', 'Sparat.'),
    ('cam_cc_saved', 'CC salvati per {0}.', 'CC saved for {0}.', 'CC salvate pentru {0}.',
     'CC fuer {0} gespeichert.', 'CC sparat foer {0}.'),
    ('cam_prefs_saved', 'Preferenze invio salvate.', 'Sending preferences saved.',
     'Preferinte de trimitere salvate.', 'Sendeeinstellungen gespeichert.', 'Skicksinstaellningar sparade.'),
    ('cam_no_unassociated', 'Nessun account manager disponibile da associare.',
     'No account manager available to associate.', 'Niciun account manager disponibil de asociat.',
     'Kein Account-Manager zum Zuordnen verfuegbar.', 'Ingen kundansvarig tillgaenglig att koppla.'),
    ('cam_select_mgr', 'Seleziona un account manager.', 'Select an account manager.',
     'Selectati un account manager.', 'Account-Manager auswaehlen.', 'Vaelj en kundansvarig.'),
    ('cam_confirm_remove', 'Rimuovere "{0}" da questo cliente?', 'Remove "{0}" from this client?',
     'Eliminati "{0}" de la acest client?', '"{0}" von diesem Kunden entfernen?',
     'Ta bort "{0}" fraan denna kund?'),
    ('cam_mgr_dialog', 'Account Manager', 'Account Manager', 'Account Manager',
     'Account-Manager', 'Kundansvarig'),
    ('cam_mgr_invalid', 'Inserire nome, cognome ed email valida.', 'Enter name, surname and a valid email.',
     'Introduceti nume, prenume si email valid.', 'Name, Nachname und gueltige E-Mail eingeben.',
     'Ange foernamn, efternamn och giltig e-post.'),
    ('cam_pick', 'Associa Account Manager', 'Associate Account Manager', 'Asociaza Account Manager',
     'Account-Manager zuordnen', 'Koppla kundansvarig'),
]
LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = 0
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
            else:
                skip += 1
    conn.commit(); conn.close()
    print(f"[OK] Account managers translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
