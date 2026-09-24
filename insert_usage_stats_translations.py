# -*- coding: utf-8 -*-
"""Traduzioni per la finestra Statistiche uso form (Strumenti > Statistiche uso form)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('menu_usage_statistics',
     '📊 Statistiche uso form',
     '📊 Form usage statistics',
     '📊 Statistici utilizare formulare',
     '📊 Formular-Nutzungsstatistik',
     '📊 Statistik över formuläranvändning'),
    ('us_title',
     'Statistiche uso form',
     'Form usage statistics',
     'Statistici utilizare formulare',
     'Formular-Nutzungsstatistik',
     'Statistik över formuläranvändning'),
    ('us_month',
     'Mese', 'Month', 'Lună', 'Monat', 'Månad'),
    ('us_year',
     'Anno', 'Year', 'An', 'Jahr', 'År'),
    ('us_whole_year',
     'Tutto l\'anno', 'Whole year', 'Tot anul', 'Ganzes Jahr', 'Hela året'),
    ('us_generate',
     'Genera', 'Generate', 'Generează', 'Generieren', 'Generera'),
    ('us_excel',
     '📊 Excel', '📊 Excel', '📊 Excel', '📊 Excel', '📊 Excel'),
    ('us_col_form',
     'Form', 'Form', 'Formular', 'Formular', 'Formulär'),
    ('us_col_key',
     'Chiave/Funzione', 'Key/Function', 'Cheie/Funcție', 'Schlüssel/Funktion', 'Nyckel/Funktion'),
    ('us_col_opens',
     'Aperture', 'Opens', 'Deschideri', 'Öffnungen', 'Öppningar'),
    ('us_col_users',
     'Utenti unici', 'Unique users', 'Utilizatori unici', 'Eindeutige Benutzer', 'Unika användare'),
    ('us_col_pct',
     '% del totale', '% of total', '% din total', '% vom Gesamt', '% av totalt'),
    ('us_total',
     'Totale', 'Total', 'Total', 'Gesamt', 'Totalt'),
    ('us_no_data',
     'Nessun dato da esportare per il periodo selezionato.',
     'No data to export for the selected period.',
     'Nu există date de exportat pentru perioada selectată.',
     'Keine Daten für den ausgewählten Zeitraum zum Exportieren.',
     'Inga data att exportera för den valda perioden.'),
    ('us_forms_found',
     '{0} form aperte nel periodo (totale aperture: {1})',
     '{0} forms opened in the period (total opens: {1})',
     '{0} formulare deschise în perioadă (deschideri totale: {1})',
     '{0} Formulare im Zeitraum geöffnet (Öffnungen gesamt: {1})',
     '{0} formulär öppnade under perioden (totalt antal öppningar: {1})'),
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
    print(f"[OK] Usage stats translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
