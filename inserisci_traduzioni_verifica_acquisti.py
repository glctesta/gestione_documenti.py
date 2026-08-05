# -*- coding: utf-8 -*-
"""
Traduzioni del tab "Verifica Acquisti" del report materiali indiretti
(indirect_materials_report.py): tracciamento delle richieste di riordino per
codice e riscontro empirico dell'arrivo della merce.

Idempotente: inserisce solo cio' che manca. Credenziali da database_config.
"""
import sys

import pyodbc

import database_config as dc

TABLE = '[dbo].[AppTranslations]'

translations = [
    ('it', 'ind_rep_tab_purchases', "Verifica Acquisti"),
    ('en', 'ind_rep_tab_purchases', "Purchase Check"),
    ('ro', 'ind_rep_tab_purchases', "Verificare Achiziții"),
    ('de', 'ind_rep_tab_purchases', "Einkaufsprüfung"),
    ('sv', 'ind_rep_tab_purchases', "Inköpskontroll"),

    ('it', 'ind_rep_col_n_reorders', "# Richieste"),
    ('en', 'ind_rep_col_n_reorders', "# Requests"),
    ('ro', 'ind_rep_col_n_reorders', "# Cereri"),
    ('de', 'ind_rep_col_n_reorders', "# Anforderungen"),
    ('sv', 'ind_rep_col_n_reorders', "# Förfrågningar"),

    ('it', 'ind_rep_col_last_reorder', "Ultima richiesta"),
    ('en', 'ind_rep_col_last_reorder', "Last request"),
    ('ro', 'ind_rep_col_last_reorder', "Ultima cerere"),
    ('de', 'ind_rep_col_last_reorder', "Letzte Anforderung"),
    ('sv', 'ind_rep_col_last_reorder', "Senaste förfrågan"),

    ('it', 'ind_rep_col_stock_at_req', "Giacenza alla richiesta"),
    ('en', 'ind_rep_col_stock_at_req', "Stock at request"),
    ('ro', 'ind_rep_col_stock_at_req', "Stoc la cerere"),
    ('de', 'ind_rep_col_stock_at_req', "Bestand bei Anforderung"),
    ('sv', 'ind_rep_col_stock_at_req', "Lager vid förfrågan"),

    ('it', 'ind_rep_col_stock_last_load', "Giacenza ultimo carico"),
    ('en', 'ind_rep_col_stock_last_load', "Stock at last upload"),
    ('ro', 'ind_rep_col_stock_last_load', "Stoc la ultima încărcare"),
    ('de', 'ind_rep_col_stock_last_load', "Bestand beim letzten Import"),
    ('sv', 'ind_rep_col_stock_last_load', "Lager vid senaste import"),

    ('it', 'ind_rep_col_last_load', "Data ultimo carico"),
    ('en', 'ind_rep_col_last_load', "Last upload date"),
    ('ro', 'ind_rep_col_last_load', "Data ultimei încărcări"),
    ('de', 'ind_rep_col_last_load', "Datum letzter Import"),
    ('sv', 'ind_rep_col_last_load', "Datum senaste import"),

    ('it', 'ind_rep_col_difference', "Differenza"),
    ('en', 'ind_rep_col_difference', "Difference"),
    ('ro', 'ind_rep_col_difference', "Diferență"),
    ('de', 'ind_rep_col_difference', "Differenz"),
    ('sv', 'ind_rep_col_difference', "Skillnad"),

    ('it', 'ind_rep_col_incoming', "Entrata rilevata"),
    ('en', 'ind_rep_col_incoming', "Detected inbound"),
    ('ro', 'ind_rep_col_incoming', "Intrare detectată"),
    ('de', 'ind_rep_col_incoming', "Erkannter Zugang"),
    ('sv', 'ind_rep_col_incoming', "Upptäckt inleverans"),

    ('it', 'ind_rep_col_incoming_date', "Data entrata"),
    ('en', 'ind_rep_col_incoming_date', "Inbound date"),
    ('ro', 'ind_rep_col_incoming_date', "Data intrării"),
    ('de', 'ind_rep_col_incoming_date', "Zugangsdatum"),
    ('sv', 'ind_rep_col_incoming_date', "Inleveransdatum"),

    ('it', 'ind_rep_col_outcome', "Esito"),
    ('en', 'ind_rep_col_outcome', "Outcome"),
    ('ro', 'ind_rep_col_outcome', "Rezultat"),
    ('de', 'ind_rep_col_outcome', "Ergebnis"),
    ('sv', 'ind_rep_col_outcome', "Resultat"),

    ('it', 'ind_rep_outcome_ok', "Acquisto rilevato"),
    ('en', 'ind_rep_outcome_ok', "Purchase detected"),
    ('ro', 'ind_rep_outcome_ok', "Achiziție detectată"),
    ('de', 'ind_rep_outcome_ok', "Einkauf erkannt"),
    ('sv', 'ind_rep_outcome_ok', "Inköp upptäckt"),

    ('it', 'ind_rep_outcome_wait', "In attesa di carico"),
    ('en', 'ind_rep_outcome_wait', "Waiting for stock upload"),
    ('ro', 'ind_rep_outcome_wait', "În așteptarea încărcării"),
    ('de', 'ind_rep_outcome_wait', "Warten auf Bestandsimport"),
    ('sv', 'ind_rep_outcome_wait', "Väntar på lagerimport"),

    ('it', 'ind_rep_outcome_ko', "Nessun acquisto"),
    ('en', 'ind_rep_outcome_ko', "No purchase"),
    ('ro', 'ind_rep_outcome_ko', "Nicio achiziție"),
    ('de', 'ind_rep_outcome_ko', "Kein Einkauf"),
    ('sv', 'ind_rep_outcome_ko', "Inget inköp"),

    ('it', 'ind_rep_total_purchases',
     "Codici sollecitati: {0}  |  arrivati: {1}  |  in attesa: {2}  |  senza acquisto: {3}"),
    ('en', 'ind_rep_total_purchases',
     "Reordered codes: {0}  |  received: {1}  |  waiting: {2}  |  not purchased: {3}"),
    ('ro', 'ind_rep_total_purchases',
     "Coduri solicitate: {0}  |  sosite: {1}  |  în așteptare: {2}  |  fără achiziție: {3}"),
    ('de', 'ind_rep_total_purchases',
     "Angeforderte Codes: {0}  |  eingetroffen: {1}  |  wartend: {2}  |  ohne Einkauf: {3}"),
    ('sv', 'ind_rep_total_purchases',
     "Beställda koder: {0}  |  mottagna: {1}  |  väntande: {2}  |  utan inköp: {3}"),

    ('it', 'ind_rep_purch_note',
     "L'entrata è misurata sugli aumenti di giacenza fra un carico Excel (stock D365) e il successivo, dopo la data della richiesta."),
    ('en', 'ind_rep_purch_note',
     "Inbound quantity is measured from stock increases between one Excel upload (D365 stock) and the next, after the request date."),
    ('ro', 'ind_rep_purch_note',
     "Intrarea este măsurată din creșterile de stoc între o încărcare Excel (stoc D365) și următoarea, după data cererii."),
    ('de', 'ind_rep_purch_note',
     "Der Zugang wird aus den Bestandserhöhungen zwischen zwei Excel-Importen (D365-Bestand) nach dem Anforderungsdatum ermittelt."),
    ('sv', 'ind_rep_purch_note',
     "Inleveransen mäts från lagerökningar mellan en Excel-import (D365-lager) och nästa, efter förfrågningsdatumet."),

    ('it', 'ind_stock_col_min', "Scorta minima"),
    ('en', 'ind_stock_col_min', "Minimum stock"),
    ('ro', 'ind_stock_col_min', "Stoc minim"),
    ('de', 'ind_stock_col_min', "Mindestbestand"),
    ('sv', 'ind_stock_col_min', "Minimilager"),
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
