# -*- coding: utf-8 -*-
"""
Traduzione del pulsante "Azzera filtri" (btn_clear_filters), usato dalla form
Configura Scorte Minime dopo l'aggiunta del filtro sulla descrizione.

Idempotente. Credenziali da database_config.
"""
import sys

import pyodbc

import database_config as dc

TABLE = '[dbo].[AppTranslations]'

translations = [
    ('it', 'btn_clear_filters', "Azzera filtri"),
    ('en', 'btn_clear_filters', "Clear filters"),
    ('ro', 'btn_clear_filters', "Șterge filtrele"),
    ('de', 'btn_clear_filters', "Filter zurücksetzen"),
    ('sv', 'btn_clear_filters', "Rensa filter"),
]


def main():
    conn = pyodbc.connect(dc.db_config.get_connection_string(), timeout=15)
    cursor = conn.cursor()
    inserted = skipped = 0
    try:
        for lang, key, value in translations:
            cursor.execute(
                f"SELECT COUNT(*) FROM {TABLE} WHERE LanguageCode = ? AND TranslationKey = ?",
                lang, key)
            if cursor.fetchone()[0]:
                skipped += 1
                print(f"[=] gia' presente: {lang} - {key}")
                continue
            cursor.execute(
                f"INSERT INTO {TABLE} (LanguageCode, TranslationKey, TranslationValue) "
                f"VALUES (?, ?, ?)", lang, key, value)
            inserted += 1
            print(f"[+] inserita:      {lang} - {key}")
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    print(f"\nInserite: {inserted}   Gia' presenti: {skipped}   Totale: {len(translations)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
