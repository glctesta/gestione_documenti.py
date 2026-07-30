# -*- coding: utf-8 -*-
"""Traduzioni per il conteggio giorni nella maschera Autorizzazione Assenze:
giorni lavorativi (weekend e festivi rumeni esclusi) + festivi del periodo."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('col_working_days', 'Giorni lav.', 'Work days', 'Zile lucr.',
     'Arbeitstage', 'Arbetsdagar'),
    ('col_holidays_in_period', 'Festivi', 'Holidays', 'Sărbători',
     'Feiertage', 'Helgdagar'),
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
    print(f"[OK] Absence days translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
