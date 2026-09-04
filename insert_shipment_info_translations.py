# -*- coding: utf-8 -*-
"""
insert_shipment_info_translations.py
Inserisce le traduzioni del modulo "Info Spedizioni" (shipment_info_gui.py,
menu e chiave di autorizzazione) in Traceability_rs.dbo.AppTranslations.
Eseguire con:
  .venv\\Scripts\\python.exe insert_shipment_info_translations.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    conn_str = (f"DRIVER={cfg['driver']};SERVER={cfg['server']};"
                f"DATABASE={cfg['database']};UID={cfg['username']};PWD={cfg['password']};"
                f"MARS_Connection=Yes;TrustServerCertificate=Yes")
    return pyodbc.connect(conn_str)

# (key, IT, EN, RO, DE, SV)
TRANSLATIONS = [
    # ── Menu ──────────────────────────────────────────────────────────────────
    ('submenu_shipment_info',
        'ℹ️ Info Spedizioni',
        'ℹ️ Shipping Info',
        'ℹ️ Informații Expediții',
        'ℹ️ Versandinfo',
        'ℹ️ Fraktinfo'),

    # ── Chiave autorizzazione (_execute_authorized_action) ────────────────────
    ('indirizzi_email_per_spedizioni',
        'Info Spedizioni',
        'Shipping Info',
        'Informații Expediții',
        'Versandinfo',
        'Fraktinfo'),

    # ── Form ──────────────────────────────────────────────────────────────────
    ('ship_info_title',
        'Info Spedizioni',
        'Shipping Info',
        'Informații Expediții',
        'Versandinfo',
        'Fraktinfo'),
    ('ship_info_config',
        'Configurazione sito',
        'Site configuration',
        'Configurare site',
        'Standortkonfiguration',
        'Webbplatskonfiguration'),
    ('ship_info_site',
        'Sito:',
        'Site:',
        'Site:',
        'Standort:',
        'Plats:'),
    ('ship_info_dir',
        'Directory:',
        'Directory:',
        'Director:',
        'Verzeichnis:',
        'Katalog:'),
    ('ship_info_to',
        'Email TO:',
        'Email TO:',
        'Email TO:',
        'E-Mail AN:',
        'E-post TILL:'),
    ('ship_info_cc',
        'Email CC:',
        'Email CC:',
        'Email CC:',
        'E-Mail CC:',
        'E-post CC:'),
    ('ship_info_sep_hint',
        '(separate da ; o ,)',
        '(separated by ; or ,)',
        '(separate prin ; sau ,)',
        '(getrennt durch ; oder ,)',
        '(separerade med ; eller ,)'),
    ('ship_info_active',
        'Servizio attivo',
        'Service active',
        'Serviciu activ',
        'Dienst aktiv',
        'Tjänst aktiv'),
    ('ship_info_active_col',
        'Attivo',
        'Active',
        'Activ',
        'Aktiv',
        'Aktiv'),
    ('ship_info_list',
        'Configurazioni attive',
        'Active configurations',
        'Configurări active',
        'Aktive Konfigurationen',
        'Aktiva konfigurationer'),

    # ── Messaggi ──────────────────────────────────────────────────────────────
    ('ship_info_no_site',
        'Selezionare un sito.',
        'Please select a site.',
        'Vă rugăm să selectați un site.',
        'Bitte einen Standort auswählen.',
        'Välj en plats.'),
    ('ship_info_no_dir',
        'Inserire la directory.',
        'Please enter the directory.',
        'Vă rugăm să introduceți directorul.',
        'Bitte das Verzeichnis eingeben.',
        'Ange katalogen.'),
    ('ship_info_no_to',
        'Inserire almeno un indirizzo TO.',
        'Please enter at least one TO address.',
        'Vă rugăm să introduceți cel puțin o adresă TO.',
        'Bitte mindestens eine AN-Adresse eingeben.',
        'Ange minst en TILL-adress.'),
    ('ship_info_bad_email',
        'Indirizzi non validi:',
        'Invalid addresses:',
        'Adrese nevalide:',
        'Ungültige Adressen:',
        'Ogiltiga adresser:'),
    ('ship_info_saved',
        'Configurazione salvata.',
        'Configuration saved.',
        'Configurare salvată.',
        'Konfiguration gespeichert.',
        'Konfiguration sparad.'),
    ('ship_info_del_title',
        'Elimina configurazione',
        'Delete configuration',
        'Șterge configurare',
        'Konfiguration löschen',
        'Radera konfiguration'),
    ('ship_info_del_msg',
        'Eliminare la configurazione del sito selezionato?',
        'Delete the configuration of the selected site?',
        'Ștergeți configurarea site-ului selectat?',
        'Konfiguration des ausgewählten Standorts löschen?',
        'Radera konfigurationen för den valda platsen?'),

    # ── Generiche ─────────────────────────────────────────────────────────────
    ('new',
        'Nuovo',
        'New',
        'Nou',
        'Neu',
        'Ny'),
    ('save',
        'Salva',
        'Save',
        'Salvează',
        'Speichern',
        'Spara'),
    ('delete',
        'Elimina',
        'Delete',
        'Șterge',
        'Löschen',
        'Radera'),
    ('warning',
        'Attenzione',
        'Warning',
        'Atenție',
        'Warnung',
        'Varning'),
    ('success',
        'Successo',
        'Success',
        'Succes',
        'Erfolg',
        'Framgång'),
    ('error',
        'Errore',
        'Error',
        'Eroare',
        'Fehler',
        'Fel'),
    ('close',
        'Chiudi',
        'Close',
        'Închide',
        'Schließen',
        'Stäng'),
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
    skipped = 0

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
    print(f"[OK] Completato - Inserite: {inserted}  |  Gia' presenti (skip): {skipped}")


if __name__ == '__main__':
    main()
