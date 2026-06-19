# -*- coding: utf-8 -*-
"""
insert_economics_translations.py
Inserisce le chiavi di traduzione della scheda "Convenienza Economica"
(analisi straordinari) in Traceability_RS.dbo.AppTranslations (it, en, ro, de, sv).

Esecuzione una tantum:  python overtime/insert_economics_translations.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_conn():
    import pyodbc
    from config_manager import ConfigManager
    cm = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
    c = cm.load_config()
    cs = (f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
          f"UID={c['username']};PWD={c['password']};TrustServerCertificate=Yes")
    return pyodbc.connect(cs, timeout=15)


# (key, it, en, ro, de, sv)
TRANSLATIONS = [
    ('overtime_detail_tab',
     'Dettaglio Straordinari', 'Overtime Detail', 'Detalii Ore Suplimentare',
     'Überstunden-Details', 'Övertidsdetaljer'),
    ('economics_tab',
     'Convenienza Economica', 'Economic Convenience', 'Eficiență Economică',
     'Wirtschaftlichkeit', 'Ekonomisk Lönsamhet'),
    ('economics_run_hint',
     "Premi 'Genera Analisi' per calcolare la convenienza economica.",
     "Press 'Generate Analysis' to compute economic convenience.",
     "Apăsați 'Generează Analiza' pentru a calcula eficiența economică.",
     "Auf 'Analyse erstellen' klicken, um die Wirtschaftlichkeit zu berechnen.",
     "Tryck 'Generera analys' för att beräkna ekonomisk lönsamhet."),
    ('economics_kpi', 'Indicatori', 'Indicators', 'Indicatori', 'Indikatoren', 'Indikatorer'),
    ('eco_people', 'Persone in straordinario', 'People on overtime',
     'Persoane în ore suplimentare', 'Personen mit Überstunden', 'Personer på övertid'),
    ('eco_ot_hours', 'Ore straordinario (svolte / appr.)', 'Overtime hours (done / appr.)',
     'Ore suplimentare (efectuate / aprob.)', 'Überstunden (geleistet / genehm.)',
     'Övertidstimmar (utförda / godk.)'),
    ('eco_ot_cost', 'Costo straordinario', 'Overtime cost', 'Cost ore suplimentare',
     'Überstundenkosten', 'Övertidskostnad'),
    ('eco_finalized', 'Pezzi finalizzati', 'Finalized pieces', 'Piese finalizate',
     'Fertiggestellte Stück', 'Färdiga stycken'),
    ('eco_finalized_value', 'Valore finalizzato', 'Finalized value', 'Valoare finalizată',
     'Wert fertiggestellt', 'Värde färdigt'),
    ('eco_wip', 'WIP (schede / pezzi-eq.)', 'WIP (boards / pieces-eq.)',
     'WIP (plăci / piese-ech.)', 'WIP (Platinen / Stück-Äq.)', 'WIP (kort / styck-ekv.)'),
    ('eco_wip_value', 'Valore WIP', 'WIP value', 'Valoare WIP', 'WIP-Wert', 'WIP-värde'),
    ('eco_total_value', 'Valore prodotto totale', 'Total produced value', 'Valoare totală produsă',
     'Gesamtproduktionswert', 'Totalt produktionsvärde'),
    ('eco_margin', 'Margine (valore - costo)', 'Margin (value - cost)', 'Marjă (valoare - cost)',
     'Marge (Wert - Kosten)', 'Marginal (värde - kostnad)'),
    ('eco_index', 'Indice convenienza (valore/costo)', 'Convenience index (value/cost)',
     'Indice eficiență (valoare/cost)', 'Wirtschaftlichkeitsindex (Wert/Kosten)',
     'Lönsamhetsindex (värde/kostnad)'),
    ('eco_per_person', 'Valore / persona', 'Value / person', 'Valoare / persoană',
     'Wert / Person', 'Värde / person'),
    ('eco_per_hour', 'Valore / ora straordinario', 'Value / overtime hour',
     'Valoare / oră suplimentară', 'Wert / Überstunde', 'Värde / övertidstimme'),
    ('economics_missing_price',
     '⚠️ {0} ordini/prodotti senza prezzo (valorizzati a 0): ',
     '⚠️ {0} orders/products without price (valued at 0): ',
     '⚠️ {0} comenzi/produse fără preț (evaluate la 0): ',
     '⚠️ {0} Aufträge/Produkte ohne Preis (mit 0 bewertet): ',
     '⚠️ {0} order/produkter utan pris (värderade till 0): '),
    ('economics_per_day', 'Dettaglio per giorno', 'Daily detail', 'Detaliu pe zi',
     'Tagesdetail', 'Daglig detalj'),
    ('eco_people_short', 'Persone', 'People', 'Persoane', 'Personen', 'Personer'),
    ('eco_hours_short', 'Ore straord.', 'OT hours', 'Ore supl.', 'Überstd.', 'Övertid'),
    ('eco_cost_short', 'Costo straord.', 'OT cost', 'Cost supl.', 'Kosten', 'Kostnad'),
    ('eco_finalized_value_short', 'Valore finalizzato', 'Finalized value',
     'Valoare finalizată', 'Wert fertig', 'Värde färdigt'),
    ('economics_error',
     'Errore calcolo convenienza economica: ', 'Economic convenience computation error: ',
     'Eroare calcul eficiență economică: ', 'Fehler bei Wirtschaftlichkeitsberechnung: ',
     'Fel vid beräkning av ekonomisk lönsamhet: '),
    ('economics_d365_file', 'Prezzi da: ', 'Prices from: ', 'Prețuri din: ',
     'Preise aus: ', 'Priser från: '),
    ('economics_no_d365',
     '⚠️ File prezzi D365 non trovato in T:\\D365 data — valori a 0.',
     '⚠️ D365 price file not found in T:\\D365 data — values at 0.',
     '⚠️ Fișierul de prețuri D365 nu a fost găsit în T:\\D365 data — valori la 0.',
     '⚠️ D365-Preisdatei nicht gefunden in T:\\D365 data — Werte 0.',
     '⚠️ D365-prisfil hittades inte i T:\\D365 data — värden 0.'),

    # ── Metriche affinate / sezioni ──────────────────────────────────────────────
    ('economics_prod_section',
     'Produzione del periodo (tutte le ore)', 'Period production (all hours)',
     'Producția perioadei (toate orele)', 'Produktion im Zeitraum (alle Stunden)',
     'Produktion under perioden (alla timmar)'),
    ('economics_ot_section', 'Straordinario', 'Overtime', 'Ore suplimentare',
     'Überstunden', 'Övertid'),
    ('eco_labor_hours', 'Ore lavorate (produzione)', 'Worked hours (production)',
     'Ore lucrate (producție)', 'Arbeitsstunden (Produktion)', 'Arbetade timmar (produktion)'),
    ('eco_productivity', 'Produttività media (valore/ora)', 'Average productivity (value/hour)',
     'Productivitate medie (valoare/oră)', 'Durchschn. Produktivität (Wert/Stunde)',
     'Genomsnittlig produktivitet (värde/timme)'),
    ('eco_ot_incidence', 'Incidenza ore straord. (%)', 'Overtime hours share (%)',
     'Pondere ore suplimentare (%)', 'Anteil Überstunden (%)', 'Andel övertidstimmar (%)'),
    ('eco_ot_cost_per_hour', 'Costo medio straord. (/h)', 'Avg overtime cost (/h)',
     'Cost mediu ore supl. (/h)', 'Durchschn. Überstundenkosten (/h)', 'Genomsnittlig övertidskostnad (/h)'),
    ('eco_ot_value', 'Valore attribuibile allo straord.', 'Value attributable to overtime',
     'Valoare atribuibilă orelor supl.', 'Den Überstunden zurechenbarer Wert',
     'Värde hänförligt till övertid'),
    ('eco_ot_margin', 'Margine straordinario (valore - costo)', 'Overtime margin (value - cost)',
     'Marjă ore suplimentare (valoare - cost)', 'Überstunden-Marge (Wert - Kosten)',
     'Övertidsmarginal (värde - kostnad)'),
    ('eco_ot_roi', 'ROI straordinario (valore/costo)', 'Overtime ROI (value/cost)',
     'ROI ore suplimentare (valoare/cost)', 'Überstunden-ROI (Wert/Kosten)',
     'Övertids-ROI (värde/kostnad)'),
    ('eco_roi_good', '✓ Straordinario conveniente', '✓ Overtime is worthwhile',
     '✓ Ore suplimentare convenabile', '✓ Überstunden lohnenswert', '✓ Övertid lönsamt'),
    ('eco_roi_bad', '✗ Straordinario non conveniente', '✗ Overtime not worthwhile',
     '✗ Ore suplimentare neconvenabile', '✗ Überstunden nicht lohnenswert', '✗ Övertid ej lönsamt'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = _get_conn()
    cur = conn.cursor()
    inserted = skipped = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            val = row[i + 1]
            cur.execute(
                "SELECT COUNT(*) FROM [Traceability_RS].[dbo].[AppTranslations] "
                "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO [Traceability_RS].[dbo].[AppTranslations] "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                    (lang, key, val))
                inserted += 1
            else:
                skipped += 1
    conn.commit()
    conn.close()
    print(f'[OK] Economics translations — Inserted: {inserted}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
