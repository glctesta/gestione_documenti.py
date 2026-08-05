# -*- coding: utf-8 -*-
"""
Traduzione della colonna "N. prelievi" dell'Analisi Consumi.

L'analisi non conta piu' i movimenti di scarico ma i prelievi effettivi
(richieste in stato PRELEVATA), quindi l'intestazione 'ind_cons_col_moves'
("N. movimenti") sarebbe fuorviante: nuova chiave 'ind_cons_col_pickups'.

Idempotente. Credenziali da database_config.
"""
import sys

import pyodbc

import database_config as dc

TABLE = '[dbo].[AppTranslations]'

translations = [
    ('it', 'ind_cons_col_pickups', "N. prelievi"),
    ('en', 'ind_cons_col_pickups', "No. pickups"),
    ('ro', 'ind_cons_col_pickups', "Nr. ridicări"),
    ('de', 'ind_cons_col_pickups', "Anz. Entnahmen"),
    ('sv', 'ind_cons_col_pickups', "Antal uttag"),
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
