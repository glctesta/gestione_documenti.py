"""
insert_shift_handover_translations.py
Inserisce le traduzioni del modulo Cambio Turno in AppTranslations.
Usa lo stesso sistema criptato di config_manager.py.
Eseguire con:
  .venv\Scripts\python.exe insert_shift_handover_translations.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

# ─── Connessione ─────────────────────────────────────────────────────────────
def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    conn_str = (f"DRIVER={cfg['driver']};SERVER={cfg['server']};"
                f"DATABASE={cfg['database']};UID={cfg['username']};PWD={cfg['password']};"
                f"MARS_Connection=Yes;TrustServerCertificate=Yes")
    return pyodbc.connect(conn_str)

# ─── Traduzioni (chiave, IT, EN, RO, DE, SV) ─────────────────────────────────
TRANSLATIONS = [
    # ── Form principale Cambio Turno ──────────────────────────────────────────
    ('cambio_turni',            'Cambio Turno',                               'Shift Handover',                                    'Predare Schimb',                                     'Schichtwechsel',                                     'Skiftbyte'),
    ('shift_handover_title',    'Cambio Turno \u2014 Predare Schimb',          'Shift Handover',                                    'Predare Schimb',                                     'Schicht\u00fcbergabe',                                  'Skift\u00f6verl\u00e4mning'),
    ('sh_tab_compile',          'Compila Consegna',                           'Fill Handover',                                     'Completeaza Predarea',                               '\u00dcbergabe ausf\u00fcllen',                          'Fyll i \u00f6verl\u00e4mning'),
    ('sh_tab_history',          'Storico / Conferma',                         'History / Confirm',                                 'Istoric / Confirmare',                               'Verlauf / Best\u00e4tigung',                            'Historik / Bekr\u00e4fta'),
    ('sh_header',               'Intestazione turno',                         'Shift header',                                      'Antet schimb',                                       'Schicht-Kopfzeile',                                  'Skift rubrik'),
    ('sh_date',                 'Data:',                                      'Date:',                                             'Data:',                                              'Datum:',                                             'Datum:'),
    ('sh_shift',                'Turno:',                                     'Shift:',                                            'Schimb:',                                            'Schicht:',                                           'Skift:'),
    ('sh_dept',                 'Reparto:',                                   'Department:',                                       'Sectie:',                                            'Abteilung:',                                         'Avdelning:'),
    ('sh_compiled_by',          'Compilato da:',                              'Compiled by:',                                      'Completat de:',                                      'Ausgef\u00fcllt von:',                                 'Ifyllt av:'),
    ('sh_field_prod_status',    'Stare produc\u0163ie',                       'Production status',                                 'Stare productie',                                    'Produktionsstatus',                                  'Produktionsstatus'),
    ('sh_field_lines',          'Linii / echipamente',                        'Lines / equipment',                                 'Linii / echipamente',                                'Linien / Ausr\u00fcstung',                             'Linjer / utrustning'),
    ('sh_field_qty',            'Cantit\u0103\u0163i',                        'Quantities',                                        'Cantitati',                                          'Mengen',                                             'Kvantiteter'),
    ('sh_qty_plan',             'Planificat:',                                'Planned:',                                          'Planificat:',                                        'Geplant:',                                           'Planerat:'),
    ('sh_qty_prod',             'Realizat:',                                  'Produced:',                                         'Realizat:',                                          'Produziert:',                                        'Producerat:'),
    ('sh_field_quality',        'Calitate \u2014 Probleme + Ac\u0163iuni',    'Quality \u2014 Issues + Actions',                   'Calitate \u2014 Probleme + Actiuni',                 'Qualit\u00e4t \u2014 Probleme + Aktionen',             'Kvalitet \u2014 Problem + \u00c5tg\u00e4rder'),
    ('sh_field_materials',      'Materiale (disponibile/lips\u0103)',          'Materials (available/missing)',                     'Materiale (disponibile/lipsa)',                       'Materialien (verf\u00fcgbar/fehlend)',                 'Material (tillg\u00e4ngligt/saknas)'),
    ('sh_field_open',           'Probleme deschise',                          'Open issues',                                       'Probleme deschise',                                  'Offene Probleme',                                    '\u00d6ppna \u00e4renden'),
    ('sh_field_notes',          'Note libere',                                'Free notes',                                        'Note libere',                                        'Freie Notizen',                                      'Fritext'),
    ('sh_btn_save',             'Salva Consegna Turno',                       'Save Shift Handover',                               'Salveaza Predarea',                                  '\u00dcbergabe speichern',                              'Spara skift\u00f6verl\u00e4mning'),
    ('sh_filter_date',          'Data:',                                      'Date:',                                             'Data:',                                              'Datum:',                                             'Datum:'),
    ('sh_filter_dept',          'Reparto:',                                   'Department:',                                       'Sectie:',                                            'Abteilung:',                                         'Avdelning:'),
    ('sh_detail',               'Dettaglio consegna selezionata',             'Selected handover detail',                          'Detaliu predare selectata',                          'Ausgew\u00e4hlte \u00dcbergabe Details',              'Vald \u00f6verl\u00e4mning detalj'),
    ('sh_btn_confirm',          'Ho letto e preso nota della consegna',       'I have read and acknowledged',                      'Am citit si luat la cunostinta',                     'Gelesen und zur Kenntnis genommen',                  'L\u00e4st och bekr\u00e4ftat'),
    ('sh_confirm_title',        'Conferma Lettura',                           'Reading Confirmation',                              'Confirmare citire',                                  'Lesebest\u00e4tigung',                                'L\u00e4sbekr\u00e4ftelse'),
    ('sh_confirm_msg',          'Confermo di aver letto e preso nota\ndella consegna del turno precedente.', 'I confirm having read the shift handover.', 'Confirm ca am citit predarea schimbului.', 'Ich best\u00e4tige die Schicht\u00fcbergabe gelesen zu haben.', 'Jag bekr\u00e4ftar att jag l\u00e4st skift\u00f6verl\u00e4mningen.'),
    ('sh_confirm_notes',        'Note aggiuntive (facoltativo):',             'Additional notes (optional):',                      'Note suplimentare (optional):',                      'Zus\u00e4tzliche Hinweise (optional):',               'Extra anteckningar (valfritt):'),
    ('sh_btn_confirm_ok',       'Confermo',                                   'Confirm',                                           'Confirmar',                                          'Best\u00e4tigen',                                     'Bekr\u00e4fta'),
    ('sh_saved_ok',             'Consegna turno salvata con successo.\nIl prossimo capo turno dovr\u00e0 confermare la lettura.', 'Shift handover saved successfully.\nThe incoming shift leader must confirm reading.', 'Predarea schimbului salvata cu succes.\nSeful de schimb urmator trebuie sa confirme citirea.', 'Schicht\u00fcbergabe erfolgreich gespeichert.\nDer n\u00e4chste Schichtleiter muss die Lekt\u00fcre best\u00e4tigen.', 'Skift\u00f6verl\u00e4mning sparad.\nN\u00e4sta skiftledare m\u00e5ste bekr\u00e4fta l\u00e4sning.'),
    ('sh_saved_err',            'Errore durante il salvataggio.',             'Error saving.',                                     'Eroare la salvare.',                                 'Fehler beim Speichern.',                             'Fel vid sparning.'),
    ('sh_confirmed_ok',         'Conferma registrata con successo.',          'Confirmation recorded successfully.',               'Confirmare inregistrata cu succes.',                  'Best\u00e4tigung erfolgreich gespeichert.',           'Bekr\u00e4ftelse registrerad.'),
    ('sh_err_dept',             'Selezionare un reparto.',                    'Please select a department.',                       'Selectati o sectie.',                                'Bitte eine Abteilung ausw\u00e4hlen.',                'V\u00e4lj en avdelning.'),
    # ── Menu ─────────────────────────────────────────────────────────────────
    ('sh_report_menu',          '\U0001f4ca Report Cambio Turno',             '\U0001f4ca Shift Handover Report',                  '\U0001f4ca Raport Predare Schimb',                   '\U0001f4ca Schicht\u00fcbergabe-Bericht',              '\U0001f4ca Skift\u00f6verl\u00e4mningsrapport'),
    ('sh_report_title',         'Report Cambio Turno',                        'Shift Handover Report',                             'Raport Predare Schimb',                              'Schicht\u00fcbergabe-Bericht',                        'Skift\u00f6verl\u00e4mningsrapport'),
    ('sh_rep_filters',          'Filtri',                                     'Filters',                                           'Filtre',                                             'Filter',                                             'Filter'),
    ('sh_rep_from',             'Dal:',                                       'From:',                                             'De la:',                                             'Von:',                                               'Fr\u00e5n:'),
    ('sh_rep_to',               'Al:',                                        'To:',                                               'Pana la:',                                           'Bis:',                                               'Till:'),
    ('sh_rep_btn_excel',        '\U0001f4e5 Export Excel',                    '\U0001f4e5 Export Excel',                           '\U0001f4e5 Export Excel',                            '\U0001f4e5 Excel exportieren',                        '\U0001f4e5 Exportera Excel'),
    ('sh_rep_no_data',          'Nessun dato da esportare.',                  'No data to export.',                                'Nu exista date de exportat.',                        'Keine Daten zum Exportieren.',                       'Inga data att exportera.'),
    ('sh_rep_open_file',        'File salvato. Aprire il file?',              'File saved. Open the file?',                        'Fisier salvat. Deschideti fisierul?',                'Datei gespeichert. Datei \u00f6ffnen?',               'Fil sparat. \u00d6ppna filen?'),
    # ── SCT WorkStation config ────────────────────────────────────────────────
    ('sct_config_menu',         '\u2699\ufe0f Configura SCT WorkStation',     '\u2699\ufe0f Configure SCT WorkStation',            '\u2699\ufe0f Configurare SCT WorkStation',            '\u2699\ufe0f SCT WorkStation konfigurieren',           '\u2699\ufe0f Konfigurera SCT WorkStation'),
    ('sct_config_title',        'Configurazione SCT WorkStation',             'SCT WorkStation Setup',                             'Configurare SCT WorkStation',                        'SCT WorkStation Einrichtung',                        'SCT WorkStation-konfiguration'),
    ('sct_config_header',       'Configurazione SCT WorkStation',             'SCT WorkStation Configuration',                     'Configurare SCT WorkStation',                        'SCT WorkStation Konfiguration',                      'SCT WorkStation Konfiguration'),
    ('sct_config_desc',         'Identifica questo PC come postazione Capo Turno (SCT Host).\nI popup di fine turno appariranno solo su questo PC.', 'Identifies this PC as a Shift Leader workstation (SCT Host).\nEnd-of-shift popups will appear only on this PC.', 'Identifica acest PC ca statie Sef de Schimb (SCT Host).\nPopup-urile de sfarsit de schimb vor aparea doar pe acest PC.', 'Kennzeichnet diesen PC als Schichtleiter-Arbeitsstation (SCT Host).\nSchichtenende-Popups erscheinen nur auf diesem PC.', 'Identifierar denna PC som skiftledare-arbetsstation (SCT Host).\nSkiftslutspopupar visas bara p\u00e5 denna PC.'),
    ('sct_config_params',       'Parametri workstation',                      'Workstation parameters',                            'Parametri statie',                                   'Arbeitsstation-Parameter',                           'Arbetsparametrar'),
    ('sct_config_activate',     'Attiva SCT WorkStation',                     'Activate SCT WorkStation',                          'Activeaza SCT WorkStation',                          'SCT WorkStation aktivieren',                         'Aktivera SCT WorkStation'),
    ('sct_config_deactivate',   'Disattiva SCT WorkStation',                  'Deactivate SCT WorkStation',                        'Dezactiveaza SCT WorkStation',                       'SCT WorkStation deaktivieren',                       'Inaktivera SCT WorkStation'),
    ('sct_config_inactive',     '\u274c  SCT WorkStation INATTIVA',          '\u274c  SCT WorkStation INACTIVE',                  '\u274c  SCT WorkStation INACTIVA',                   '\u274c  SCT WorkStation INAKTIV',                     '\u274c  SCT WorkStation INAKTIV'),
    ('sct_config_created',      'SCT WorkStation attivata con successo.',     'SCT WorkStation activated successfully.',           'SCT WorkStation activata cu succes.',                'SCT WorkStation erfolgreich aktiviert.',              'SCT WorkStation aktiverad.'),
    ('sct_config_deleted',      'SCT WorkStation disattivata con successo.',  'SCT WorkStation deactivated successfully.',         'SCT WorkStation dezactivata cu succes.',              'SCT WorkStation erfolgreich deaktiviert.',            'SCT WorkStation inaktiverad.'),
    ('sct_config_confirm_delete','Disattivare la SCT WorkStation?\nI popup di fine turno non appariranno pi\u00f9 su questo PC.', 'Deactivate the SCT WorkStation?\nEnd-of-shift popups will no longer appear on this PC.', 'Dezactivati SCT WorkStation?\nPopup-urile de sfarsit de schimb nu vor mai aparea pe acest PC.', 'SCT WorkStation deaktivieren?\nSchichtenende-Popups erscheinen nicht mehr auf diesem PC.', 'Inaktivera SCT WorkStation?\nSkiftslutspopupar visas inte l\u00e4ngre p\u00e5 denna PC.'),
    ('sct_config_err_dept',     'Selezionare un reparto.',                    'Please select a department.',                       'Selectati o sectie.',                                'Bitte eine Abteilung ausw\u00e4hlen.',                'V\u00e4lj en avdelning.'),
    ('sct_config_err_shifts',   'Selezionare almeno un turno.',               'Please select at least one shift.',                 'Selectati cel putin un schimb.',                     'Bitte mindestens eine Schicht ausw\u00e4hlen.',       'V\u00e4lj minst ett skift.'),
]

LANGS = ['it', 'en', 'ro', 'de', 'sv']


def main():
    print("Connessione al database...")
    try:
        conn = get_conn()
    except Exception as e:
        print(f"Errore connessione: {e}")
        sys.exit(1)

    cursor = conn.cursor()
    inserted = 0
    skipped  = 0

    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            value = row[i + 1]
            cursor.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode=? AND TranslationKey=?",
                (lang, key)
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?,?,?)",
                    (lang, key, value)
                )
                inserted += 1
            else:
                skipped += 1

    conn.commit()
    conn.close()
    print(f"✅ Completato — Inserite: {inserted}  |  Già presenti (skip): {skipped}")
    print(f"   Totale chiavi: {len(TRANSLATIONS)}  x  {len(LANGS)} lingue = {len(TRANSLATIONS)*len(LANGS)} record")


if __name__ == '__main__':
    main()
