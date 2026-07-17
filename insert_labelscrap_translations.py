# -*- coding: utf-8 -*-
"""
insert_labelscrap_translations.py
Traduzioni per gli scarti etichette (dichiarazione + report). 5 lingue. Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    # Menu
    ('submenu_label_scrap_declare', 'Dichiarazione scarti', 'Scrap declaration',
     'Declarare rebuturi', 'Ausschussmeldung', 'Kassationsdeklaration'),
    ('submenu_label_scrap_report', 'Report scarti etichette', 'Label scrap report',
     'Raport rebuturi etichete', 'Etiketten-Ausschussbericht', 'Etikettkassationsrapport'),
    # Dichiarazione
    ('lsc_title', 'Dichiarazione Scarti Etichette', 'Label Scrap Declaration',
     'Declarare Rebuturi Etichete', 'Etiketten-Ausschussmeldung', 'Deklaration Etikettkassation'),
    ('lsc_operator', 'Operatore', 'Operator', 'Operator', 'Bediener', 'Operatör'),
    ('lsc_date', 'Data', 'Date', 'Data', 'Datum', 'Datum'),
    ('lsc_reason', 'Motivo', 'Reason', 'Motiv', 'Grund', 'Orsak'),
    ('lsc_category', 'Categoria', 'Category', 'Categorie', 'Kategorie', 'Kategori'),
    ('lsc_cat_production', 'Produzione', 'Production', 'Producție', 'Produktion', 'Produktion'),
    ('lsc_cat_print', 'Stampa', 'Print', 'Tipărire', 'Druck', 'Utskrift'),
    ('lsc_scan', 'Scansiona etichetta', 'Scan label', 'Scanează eticheta', 'Etikett scannen', 'Skanna etikett'),
    ('lsc_add', 'Aggiungi', 'Add', 'Adaugă', 'Hinzufügen', 'Lägg till'),
    ('lsc_counters', 'Contatori', 'Counters', 'Contoare', 'Zähler', 'Räknare'),
    ('lsc_c_session', 'Sessione', 'Session', 'Sesiune', 'Sitzung', 'Session'),
    ('lsc_c_week', 'Settimana (tu)', 'Week (you)', 'Săptămână (tu)', 'Woche (Sie)', 'Vecka (du)'),
    ('lsc_c_month', 'Mese (tu)', 'Month (you)', 'Lună (tu)', 'Monat (Sie)', 'Månad (du)'),
    ('lsc_c_year', 'Anno (tu)', 'Year (you)', 'An (tu)', 'Jahr (Sie)', 'År (du)'),
    ('lsc_c_general', 'Generale (tutti)', 'General (all)', 'General (toți)', 'Gesamt (alle)', 'Allmänt (alla)'),
    ('lsc_time', 'Ora', 'Time', 'Ora', 'Zeit', 'Tid'),
    ('lsc_shift', 'Turno', 'Shift', 'Tură', 'Schicht', 'Skift'),
    ('lsc_undo', '↩ Annulla ultima', '↩ Undo last', '↩ Anulează ultima', '↩ Letzte rückgängig', '↩ Ångra senaste'),
    ('lsc_manage_reasons', '⚙ Motivi', '⚙ Reasons', '⚙ Motive', '⚙ Gründe', '⚙ Orsaker'),
    ('lsc_close_print', '🖨 Chiudi e stampa', '🖨 Close and print', '🖨 Închide și tipărește',
     '🖨 Schließen und drucken', '🖨 Stäng och skriv ut'),
    ('lsc_pick_reason', 'Selezionare un motivo.', 'Select a reason.', 'Selectați un motiv.',
     'Wählen Sie einen Grund.', 'Välj en orsak.'),
    ('lsc_undo_confirm', 'Annullare l\'ultima scansione ({0})?', 'Undo last scan ({0})?',
     'Anulați ultima scanare ({0})?', 'Letzten Scan rückgängig machen ({0})?', 'Ångra senaste skanning ({0})?'),
    ('lsc_print_q_title', 'Stampa riepilogo', 'Print summary', 'Tipărire rezumat',
     'Zusammenfassung drucken', 'Skriv ut sammanfattning'),
    ('lsc_print_q', 'Vuoi stampare il riepilogo della dichiarazione?', 'Print the declaration summary?',
     'Tipăriți rezumatul declarației?', 'Zusammenfassung der Meldung drucken?', 'Skriv ut deklarationssammanfattningen?'),
    ('lsc_print_err', 'Impossibile stampare il riepilogo', 'Cannot print the summary',
     'Nu se poate tipări rezumatul', 'Zusammenfassung kann nicht gedruckt werden', 'Kan inte skriva ut sammanfattningen'),
    ('lsc_open_err', 'Impossibile aprire la dichiarazione scarti', 'Cannot open the scrap declaration',
     'Nu se poate deschide declararea rebuturilor', 'Ausschussmeldung kann nicht geöffnet werden',
     'Kan inte öppna kassationsdeklarationen'),
    ('lsc_reasons_title', 'Motivi scarto etichette', 'Label scrap reasons', 'Motive rebut etichete',
     'Etiketten-Ausschussgründe', 'Orsaker etikettkassation'),
    ('lsc_active', 'Attivo', 'Active', 'Activ', 'Aktiv', 'Aktiv'),
    ('lsc_toggle', 'Attiva/Disattiva', 'Enable/Disable', 'Activează/Dezactivează', 'Aktivieren/Deaktivieren', 'Aktivera/Inaktivera'),
    # Report
    ('lsr_title', 'Report Scarti Etichette', 'Label Scrap Report', 'Raport Rebuturi Etichete',
     'Etiketten-Ausschussbericht', 'Etikettkassationsrapport'),
    ('lsr_from', 'Da', 'From', 'De la', 'Von', 'Från'),
    ('lsr_to', 'A', 'To', 'Până la', 'Bis', 'Till'),
    ('lsr_generate', 'Genera', 'Generate', 'Generează', 'Erstellen', 'Generera'),
    ('lsr_excel', '📊 Excel', '📊 Excel', '📊 Excel', '📊 Excel', '📊 Excel'),
    ('lsr_pdf', '📄 PDF', '📄 PDF', '📄 PDF', '📄 PDF', '📄 PDF'),
    ('lsr_count', '{0} scarti nel periodo', '{0} scraps in the period', '{0} rebuturi în perioadă',
     '{0} Ausschüsse im Zeitraum', '{0} kassationer under perioden'),
    ('lsr_bad_dates', 'Date non valide.', 'Invalid dates.', 'Date invalide.', 'Ungültige Daten.', 'Ogiltiga datum.'),
    ('lsr_no_data', 'Nessun dato da esportare.', 'No data to export.', 'Niciun date de exportat.',
     'Keine Daten zum Exportieren.', 'Inga data att exportera.'),
    ('lsr_open_err', 'Impossibile aprire il report scarti', 'Cannot open the scrap report',
     'Nu se poate deschide raportul rebuturilor', 'Ausschussbericht kann nicht geöffnet werden',
     'Kan inte öppna kassationsrapporten'),
    ('all_operators', 'Tutti', 'All', 'Toți', 'Alle', 'Alla'),
    # Config postazione stampa
    ('submenu_label_scrap_ws', '🖥 PC stampa scarti (config)', '🖥 Scrap print PC (config)',
     '🖥 PC tipărire rebuturi (config)', '🖥 Ausschussdruck-PC (Konfig)', '🖥 Kassationsutskrift-PC (konfig)'),
    ('lsw_title', 'Postazione Stampa Scarti Etichette', 'Label Scrap Print Workstation',
     'Stație Tipărire Rebuturi Etichete', 'Etiketten-Ausschussdruck-Station', 'Utskriftsstation Etikettkassation'),
    ('lsw_header', 'Postazione Stampa Scarti Etichette', 'Label Scrap Print Workstation',
     'Stație Tipărire Rebuturi Etichete', 'Etiketten-Ausschussdruck-Station', 'Utskriftsstation Etikettkassation'),
    ('lsw_desc',
     'Attivando questa funzione, a fine turno (15:15 / 23:15) questo PC\nstamperà i riepiloghi scarti etichette non stampati e invierà l\'email.\nDesignare un solo PC per evitare stampe/invii duplicati.',
     'When enabled, at shift end (15:15 / 23:15) this PC will print the\nunprinted label scrap summaries and send the email.\nDesignate only one PC to avoid duplicate prints/sends.',
     'Când este activat, la sfârșitul turei (15:15 / 23:15) acest PC va tipări\nrezumatele rebuturilor netipărite și va trimite email-ul.\nDesemnați un singur PC pentru a evita tipăririle/trimiterile duplicate.',
     'Wenn aktiviert, druckt dieser PC bei Schichtende (15:15 / 23:15) die\nnicht gedruckten Ausschusszusammenfassungen und sendet die E-Mail.\nNur einen PC festlegen, um doppelte Ausdrucke/Sendungen zu vermeiden.',
     'När aktiverad skriver denna PC vid skiftslut (15:15 / 23:15) ut de\nej utskrivna kassationssammanfattningarna och skickar e-post.\nUtse endast en PC för att undvika dubbla utskrifter/sändningar.'),
    ('lsw_active', '✅ ATTIVA\nHost: {0}\nAttivata da: {1}  —  {2}', '✅ ACTIVE\nHost: {0}\nActivated by: {1}  —  {2}',
     '✅ ACTIVĂ\nHost: {0}\nActivată de: {1}  —  {2}', '✅ AKTIV\nHost: {0}\nAktiviert von: {1}  —  {2}',
     '✅ AKTIV\nHost: {0}\nAktiverad av: {1}  —  {2}'),
    ('lsw_file_error', '⚠️ File presente ma non leggibile', '⚠️ File present but not readable',
     '⚠️ Fișier prezent dar necitibil', '⚠️ Datei vorhanden aber nicht lesbar', '⚠️ Fil finns men går ej att läsa'),
    ('lsw_inactive', '❌ NON attiva', '❌ NOT active', '❌ NU este activă', '❌ NICHT aktiv', '❌ INTE aktiv'),
    ('lsw_activate', '✅ Attiva', '✅ Activate', '✅ Activează', '✅ Aktivieren', '✅ Aktivera'),
    ('lsw_deactivate', '❌ Disattiva', '❌ Deactivate', '❌ Dezactivează', '❌ Deaktivieren', '❌ Inaktivera'),
    ('lsw_activated', 'Postazione attivata.', 'Workstation activated.', 'Stație activată.',
     'Station aktiviert.', 'Station aktiverad.'),
    ('lsw_confirm_deactivate', 'Disattivare questa postazione?', 'Deactivate this workstation?',
     'Dezactivați această stație?', 'Diese Station deaktivieren?', 'Inaktivera denna station?'),
    ('lsw_deactivated', 'Postazione disattivata.', 'Workstation deactivated.', 'Stație dezactivată.',
     'Station deaktiviert.', 'Station inaktiverad.'),
    # Comuni (solo se mancanti)
    ('open_file_question', 'Aprire il file?', 'Open the file?', 'Deschideți fișierul?',
     'Datei öffnen?', 'Öppna filen?'),
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
    conn.commit()
    conn.close()
    print(f"[OK] Label scrap translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
