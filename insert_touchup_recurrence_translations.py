# -*- coding: utf-8 -*-
"""Traduzioni per la sezione 'Ricorrenze prodotto×errore' del report Touch-up. 5 lingue. Idempotente."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('tur_sum_recurr', 'Ricorrenze prodotto×errore', 'Product×error recurrence',
     'Recurență produs×eroare', 'Produkt×Fehler-Wiederholung', 'Produkt×fel-återkommande'),
    ('tur_recurr_hint',
     'Coppie prodotto+errore che ricorrono (≥{0} segnalazioni): se persistono nonostante le soluzioni dichiarate, le azioni correttive vanno verificate.',
     'Product+error pairs that recur (≥{0} reports): if they persist despite the declared solutions, the corrective actions must be verified.',
     'Perechi produs+eroare care se repetă (≥{0} raportări): dacă persistă în ciuda soluțiilor declarate, acțiunile corective trebuie verificate.',
     'Produkt+Fehler-Paare, die wiederkehren (≥{0} Meldungen): bestehen sie trotz der erklärten Lösungen fort, sind die Korrekturmaßnahmen zu überprüfen.',
     'Produkt+fel-par som återkommer (≥{0} rapporter): om de kvarstår trots deklarerade lösningar måste korrigerande åtgärder verifieras.'),
    ('tur_rc_count', 'Occorrenze', 'Occurrences', 'Apariții', 'Vorkommen', 'Förekomster'),
    ('tur_rc_reopen', 'Riaperture', 'Reopenings', 'Redeschideri', 'Wiedereröffnungen', 'Återöppningar'),
    ('tur_rc_nsol', 'N. sol.', 'N. sol.', 'Nr. sol.', 'Anz. Lös.', 'Antal lösn.'),
    ('tur_rc_solutions', 'Soluzioni dichiarate', 'Declared solutions', 'Soluții declarate',
     'Erklärte Lösungen', 'Deklarerade lösningar'),
    ('tur_rc_first', 'Prima', 'First', 'Prima', 'Erste', 'Första'),
    ('tur_rc_last', 'Ultima', 'Last', 'Ultima', 'Letzte', 'Sista'),
    ('tur_rc_flag', 'Segnale', 'Flag', 'Semnal', 'Signal', 'Signal'),
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
                        "WHERE LanguageCode=? AND TranslationKey=?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                skip += 1
    conn.commit()
    conn.close()
    print(f"[OK] Touch-up recurrence translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
