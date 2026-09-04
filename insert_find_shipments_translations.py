# -*- coding: utf-8 -*-
"""
insert_find_shipments_translations.py
Inserisce le traduzioni del modulo "Trova spedizioni" (find_shipments_gui.py,
voce di menu inclusa) in Traceability_rs.dbo.AppTranslations.
Eseguire con:
  .venv\\Scripts\\python.exe insert_find_shipments_translations.py
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
    ('submenu_find_shipments',
        '🔎 Trova spedizioni',
        '🔎 Find shipments',
        '🔎 Găsește expedieri',
        '🔎 Sendungen finden',
        '🔎 Hitta försändelser'),

    # ── Form ──────────────────────────────────────────────────────────────────
    ('find_ship_title',
        'Trova spedizioni',
        'Find shipments',
        'Găsește expedieri',
        'Sendungen finden',
        'Hitta försändelser'),
    ('find_ship_search',
        'Criteri di ricerca (tutti opzionali, corrispondenza esatta)',
        'Search criteria (all optional, exact match)',
        'Criterii de căutare (toate opționale, potrivire exactă)',
        'Suchkriterien (alle optional, genaue Übereinstimmung)',
        'Sökkriterier (alla valfria, exakt matchning)'),
    ('find_ship_product',
        'Product Code',
        'Product Code',
        'Cod produs',
        'Produktcode',
        'Produktkod'),
    ('find_ship_pallet',
        'Pallet',
        'Pallet',
        'Palet',
        'Palette',
        'Pall'),
    ('find_ship_commercial',
        'Commercial Number',
        'Commercial Number',
        'Număr comercial',
        'Handelsnummer',
        'Kommersiellt nummer'),
    ('find_ship_unique',
        'Unique Number',
        'Unique Number',
        'Număr unic',
        'Eindeutige Nummer',
        'Unikt nummer'),
    ('find_ship_prod_order',
        'Ord. Produzione',
        'Prod. Order',
        'Comandă producție',
        'Prod.-Auftrag',
        'Prod.order'),
    ('find_ship_date',
        'Data PL:',
        'PL Date:',
        'Data PL:',
        'PL-Datum:',
        'PL-datum:'),
    ('find_ship_found',
        '{n} righe trovate',
        '{n} rows found',
        '{n} rânduri găsite',
        '{n} Zeilen gefunden',
        '{n} rader hittade'),
    ('find_ship_export',
        '📊 Esporta Excel',
        '📊 Export Excel',
        '📊 Exportă Excel',
        '📊 Excel exportieren',
        '📊 Exportera Excel'),

    # ── Messaggi ──────────────────────────────────────────────────────────────
    ('find_ship_no_criteria',
        'Inserire almeno un criterio di ricerca.',
        'Please enter at least one search criterion.',
        'Vă rugăm să introduceți cel puțin un criteriu de căutare.',
        'Bitte geben Sie mindestens ein Suchkriterium ein.',
        'Ange minst ett sökkriterium.'),
    ('find_ship_nothing',
        'Nessun risultato da esportare.',
        'No results to export.',
        'Niciun rezultat de exportat.',
        'Keine Ergebnisse zum Exportieren.',
        'Inga resultat att exportera.'),

    # ── Generiche ─────────────────────────────────────────────────────────────
    ('search',
        'Cerca',
        'Search',
        'Caută',
        'Suchen',
        'Sök'),
    ('warning',
        'Attenzione',
        'Warning',
        'Atenție',
        'Warnung',
        'Varning'),
    ('info',
        'Informazione',
        'Info',
        'Informație',
        'Info',
        'Info'),
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
