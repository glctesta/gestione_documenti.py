# -*- coding: utf-8 -*-
"""Traduzioni per la maschera Piano Produzione — Discrepanze:
pannello urgenze di spedizione (priorita' 1) + sezione discrepanze fasi finali."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('plan_section_urgencies',
     '⚠ 1. Urgenze di spedizione non rispettate — da giustificare per prime',
     '⚠ 1. Unmet urgent shipments — to be justified first',
     '⚠ 1. Urgențe de livrare nerespectate — de justificat primele',
     '⚠ 1. Nicht eingehaltene Eillieferungen — zuerst zu begründen',
     '⚠ 1. Ej uppfyllda brådskande leveranser — motivera dessa först'),
    ('plan_section_discrepancies',
     '2. Discrepanze di piano — fasi finali',
     '2. Plan discrepancies — final phases',
     '2. Discrepanțe de plan — faze finale',
     '2. Planabweichungen — Endphasen',
     '2. Planavvikelser — slutfaser'),
    ('col_customer', 'Cliente', 'Customer', 'Client', 'Kunde', 'Kund'),
    ('col_item', 'Articolo', 'Item', 'Articol', 'Artikel', 'Artikel'),
    ('col_ship_date', 'Data spedizione', 'Ship date', 'Data livrării',
     'Lieferdatum', 'Leveransdatum'),
    ('col_qty', 'Quantità', 'Quantity', 'Cantitate', 'Menge', 'Kvantitet'),
    ('col_state', 'Stato', 'Status', 'Stare', 'Status', 'Status'),
    ('col_justification', 'Giustificazione', 'Justification', 'Justificare',
     'Begründung', 'Motivering'),
    ('not_justified', 'NON GIUSTIFICATA', 'NOT JUSTIFIED', 'NEJUSTIFICAT',
     'NICHT BEGRÜNDET', 'EJ MOTIVERAD'),
    ('overdue', 'IN RITARDO', 'OVERDUE', 'ÎNTÂRZIAT', 'ÜBERFÄLLIG', 'FÖRSENAD'),
    ('on_time', 'Nei termini', 'On time', 'În termen', 'Fristgerecht', 'I tid'),
    ('urgencies_to_justify', 'da giustificare', 'to justify', 'de justificat',
     'zu begründen', 'att motivera'),
    ('btn_justify_urgency',
     '✅ Giustifica le urgenze selezionate', '✅ Justify selected urgencies',
     '✅ Justifică urgențele selectate', '✅ Ausgewählte Dringlichkeiten begründen',
     '✅ Motivera valda brådskande poster'),
    ('select_urgency',
     'Selezionare almeno un\'urgenza dalla lista.',
     'Select at least one urgency from the list.',
     'Selectați cel puțin o urgență din listă.',
     'Wählen Sie mindestens eine Dringlichkeit aus der Liste.',
     'Välj minst en brådskande post i listan.'),
    ('confirm_justify_urgency',
     'Salvare la giustificazione per {n} urgenze di spedizione?',
     'Save the justification for {n} urgent shipments?',
     'Salvați justificarea pentru {n} urgențe de livrare?',
     'Begründung für {n} Eillieferungen speichern?',
     'Spara motiveringen för {n} brådskande leveranser?'),
    ('close_with_urgencies',
     'Ci sono ancora {count} urgenze di spedizione non giustificate.\nChiudere?',
     'There are still {count} unjustified urgent shipments.\nClose?',
     'Mai există {count} urgențe de livrare nejustificate.\nÎnchideți?',
     'Es gibt noch {count} unbegründete Eillieferungen.\nSchließen?',
     'Det finns fortfarande {count} omotiverade brådskande leveranser.\nStäng?'),
    ('urgency_save_error',
     'Salvataggio della giustificazione non riuscito.',
     'Saving the justification failed.',
     'Salvarea justificării nu a reușit.',
     'Speichern der Begründung fehlgeschlagen.',
     'Det gick inte att spara motiveringen.'),
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
    print(f"[OK] Plan urgency translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
