# -*- coding: utf-8 -*-
"""
Traduzioni della finestra "preparazione aggiornamento" (_show_update_prep_splash):

  update_prep_can_work  rassicurazione: l'operatore puo' continuare a lavorare
  update_prep_minimize  etichetta del pulsante che riduce a icona la finestra

Idempotente: inserisce solo le chiavi mancanti. Le credenziali arrivano da
database_config (.env.db), non sono scritte qui dentro.
"""
import sys

import pyodbc

import database_config as dc

TABLE = '[dbo].[AppTranslations]'

translations = [
    # update_prep_can_work
    ('it', 'update_prep_can_work',
     "Puoi continuare a lavorare: ti avviso io quando è tutto pronto."),
    ('en', 'update_prep_can_work',
     "You can keep working: I'll let you know when everything is ready."),
    ('ro', 'update_prep_can_work',
     "Puteți continua să lucrați: vă anunț eu când totul este gata."),
    ('de', 'update_prep_can_work',
     "Sie können weiterarbeiten: Ich sage Bescheid, sobald alles bereit ist."),
    ('sv', 'update_prep_can_work',
     "Du kan fortsätta arbeta: jag säger till när allt är klart."),

    # update_prep_minimize
    ('it', 'update_prep_minimize', "Riduci a icona"),
    ('en', 'update_prep_minimize', "Minimize"),
    ('ro', 'update_prep_minimize', "Minimizează"),
    ('de', 'update_prep_minimize', "Minimieren"),
    ('sv', 'update_prep_minimize', "Minimera"),
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
