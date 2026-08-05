# -*- coding: utf-8 -*-
"""
Traduzioni delle nuove voci del report scarti etichette (label_scrap_report_gui):
quantita' nel dettaglio e riquadro "scarti a fronte del prelevato dal magazzino".

Le chiavi gia' esistenti (lsc_qty, lsc_material, lsr_*) non vengono toccate.
Idempotente: inserisce solo cio' che manca. Credenziali da database_config.
"""
import sys

import pyodbc

import database_config as dc

TABLE = '[dbo].[AppTranslations]'

translations = [
    # riga di conteggio: righe E etichette
    ('it', 'lsr_count_qty', "{0} righe ({1} etichette) nel periodo"),
    ('en', 'lsr_count_qty', "{0} rows ({1} labels) in the period"),
    ('ro', 'lsr_count_qty', "{0} rânduri ({1} etichete) în perioadă"),
    ('de', 'lsr_count_qty', "{0} Zeilen ({1} Etiketten) im Zeitraum"),
    ('sv', 'lsr_count_qty', "{0} rader ({1} etiketter) under perioden"),

    # titolo del riquadro di confronto
    ('it', 'lsr_vs_title', "Scarti a fronte del prelevato dal magazzino"),
    ('en', 'lsr_vs_title', "Scrap against quantity withdrawn from the warehouse"),
    ('ro', 'lsr_vs_title', "Rebuturi raportate la cantitatea ridicată din magazie"),
    ('de', 'lsr_vs_title', "Ausschuss im Verhältnis zur Lagerentnahme"),
    ('sv', 'lsr_vs_title', "Kassation i förhållande till uttag från lagret"),

    ('it', 'lsr_descr', "Descrizione"),
    ('en', 'lsr_descr', "Description"),
    ('ro', 'lsr_descr', "Descriere"),
    ('de', 'lsr_descr', "Beschreibung"),
    ('sv', 'lsr_descr', "Beskrivning"),

    ('it', 'lsr_withdrawn', "Prelevate"),
    ('en', 'lsr_withdrawn', "Withdrawn"),
    ('ro', 'lsr_withdrawn', "Ridicate"),
    ('de', 'lsr_withdrawn', "Entnommen"),
    ('sv', 'lsr_withdrawn', "Uttagna"),

    ('it', 'lsr_scrapped', "Scartate"),
    ('en', 'lsr_scrapped', "Scrapped"),
    ('ro', 'lsr_scrapped', "Rebutate"),
    ('de', 'lsr_scrapped', "Ausschuss"),
    ('sv', 'lsr_scrapped', "Kasserade"),

    ('it', 'lsr_rate', "% scarto"),
    ('en', 'lsr_rate', "Scrap %"),
    ('ro', 'lsr_rate', "% rebut"),
    ('de', 'lsr_rate', "Ausschuss %"),
    ('sv', 'lsr_rate', "Kassation %"),

    ('it', 'lsr_total', "Totale"),
    ('en', 'lsr_total', "Total"),
    ('ro', 'lsr_total', "Total"),
    ('de', 'lsr_total', "Gesamt"),
    ('sv', 'lsr_total', "Totalt"),

    ('it', 'lsr_vs_note',
     "Prelievi da richieste materiali indiretti (stato PRELEVATA) nel periodo — tutti gli operatori"),
    ('en', 'lsr_vs_note',
     "Withdrawals from indirect material requests (status PRELEVATA) in the period — all operators"),
    ('ro', 'lsr_vs_note',
     "Ridicări din cererile de materiale indirecte (stare PRELEVATA) în perioadă — toți operatorii"),
    ('de', 'lsr_vs_note',
     "Entnahmen aus Anforderungen indirekter Materialien (Status PRELEVATA) im Zeitraum — alle Bediener"),
    ('sv', 'lsr_vs_note',
     "Uttag från förfrågningar om indirekt material (status PRELEVATA) under perioden — alla operatörer"),

    ('it', 'lsr_vs_none', "Nessun prelievo di etichette dal magazzino nel periodo"),
    ('en', 'lsr_vs_none', "No label withdrawal from the warehouse in the period"),
    ('ro', 'lsr_vs_none', "Nicio ridicare de etichete din magazie în perioadă"),
    ('de', 'lsr_vs_none', "Keine Etikettenentnahme aus dem Lager im Zeitraum"),
    ('sv', 'lsr_vs_none', "Inga etikettuttag från lagret under perioden"),
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
