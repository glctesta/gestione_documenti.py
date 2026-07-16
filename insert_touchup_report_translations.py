# -*- coding: utf-8 -*-
"""
insert_touchup_report_translations.py
Traduzioni per la finestra Report Touch-up (touchup_report_gui). 5 lingue
(it, en, ro, de, sv). Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('touchup_report_title', 'Report Touch-up', 'Touch-up Report', 'Raport Touch-up',
     'Touch-up-Bericht', 'Touch-up-rapport'),
    ('touchup_report_filters', 'Filtri', 'Filters', 'Filtre', 'Filter', 'Filter'),
    ('touchup_report_from', 'Da:', 'From:', 'De la:', 'Von:', 'Från:'),
    ('touchup_report_to', 'A:', 'To:', 'Până la:', 'Bis:', 'Till:'),
    ('touchup_report_client', 'Cliente:', 'Client:', 'Client:', 'Kunde:', 'Kund:'),
    ('touchup_report_product', 'Prodotto:', 'Product:', 'Produs:', 'Produkt:', 'Produkt:'),
    ('touchup_report_defect', 'Difetto:', 'Defect:', 'Defect:', 'Fehler:', 'Defekt:'),
    ('touchup_report_status', 'Stato:', 'Status:', 'Stare:', 'Status:', 'Status:'),
    ('touchup_report_status_all', 'Tutti', 'All', 'Toate', 'Alle', 'Alla'),
    ('touchup_report_status_open', 'Aperti', 'Open', 'Deschise', 'Offen', 'Öppna'),
    ('touchup_report_status_closed', 'Chiusi', 'Closed', 'Închise', 'Geschlossen', 'Stängda'),
    ('touchup_report_status_reopened', 'Riaperti', 'Reopened', 'Redeschise', 'Wiedereröffnet', 'Återöppnade'),
    ('touchup_report_boss_only', 'Solo escalation capo', 'Boss escalation only',
     'Doar escaladare șef', 'Nur Chef-Eskalation', 'Endast chefseskalering'),
    ('touchup_report_search', '🔍 Cerca', '🔍 Search', '🔍 Caută', '🔍 Suchen', '🔍 Sök'),
    ('touchup_report_export_xls', '📊 Esporta Excel', '📊 Export Excel', '📊 Export Excel',
     '📊 Excel exportieren', '📊 Exportera Excel'),
    ('touchup_report_export_pdf', '📄 Esporta PDF', '📄 Export PDF', '📄 Export PDF',
     '📄 PDF exportieren', '📄 Exportera PDF'),
    ('touchup_report_tab_detail', 'Dettaglio', 'Detail', 'Detaliu', 'Detail', 'Detalj'),
    ('touchup_report_tab_summary', 'Sintesi', 'Summary', 'Sinteză', 'Zusammenfassung', 'Sammanfattning'),
    ('touchup_report_kpi',
     'Totale: {total}   Aperte: {open}   Chiuse: {closed}   Riaperte: {reopened}   '
     'Escalation capo: {boss}   Tempo medio 1ª risposta: {avg} min   % entro {thr} min: {pct}',
     'Total: {total}   Open: {open}   Closed: {closed}   Reopened: {reopened}   '
     'Boss escalation: {boss}   Avg first response: {avg} min   % within {thr} min: {pct}',
     'Total: {total}   Deschise: {open}   Închise: {closed}   Redeschise: {reopened}   '
     'Escaladare șef: {boss}   Timp mediu primul răspuns: {avg} min   % în {thr} min: {pct}',
     'Gesamt: {total}   Offen: {open}   Geschlossen: {closed}   Wiedereröffnet: {reopened}   '
     'Chef-Eskalation: {boss}   Ø erste Antwort: {avg} min   % in {thr} min: {pct}',
     'Totalt: {total}   Öppna: {open}   Stängda: {closed}   Återöppnade: {reopened}   '
     'Chefseskalering: {boss}   Snitt första svar: {avg} min   % inom {thr} min: {pct}'),
    ('touchup_report_bad_dates', 'Date non valide (gg/mm/aaaa).', 'Invalid dates (dd/mm/yyyy).',
     'Date invalide (zz/ll/aaaa).', 'Ungültige Daten (TT/MM/JJJJ).', 'Ogiltiga datum (dd/mm/åååå).'),
    ('touchup_report_date_order', 'La data "Da" deve precedere "A".', '"From" date must precede "To".',
     'Data "De la" trebuie să preceadă "Până la".', '"Von" muss vor "Bis" liegen.',
     '"Från" måste vara före "Till".'),
    ('touchup_report_no_data', 'Nessun dato da esportare. Esegui una ricerca.',
     'No data to export. Run a search first.', 'Nu există date de exportat. Rulați o căutare.',
     'Keine Daten zum Export. Zuerst suchen.', 'Inga data att exportera. Gör en sökning först.'),
    ('touchup_report_saved', 'File salvato:\n{0}', 'File saved:\n{0}', 'Fișier salvat:\n{0}',
     'Datei gespeichert:\n{0}', 'Fil sparad:\n{0}'),
    ('touchup_report_open_error', 'Impossibile aprire il Report Touch-up',
     'Cannot open the Touch-up Report', 'Nu se poate deschide Raportul Touch-up',
     'Touch-up-Bericht kann nicht geöffnet werden', 'Kan inte öppna Touch-up-rapporten'),
    # colonne dettaglio
    ('tur_c_date', 'Data/ora', 'Date/time', 'Dată/oră', 'Datum/Zeit', 'Datum/tid'),
    ('tur_c_id', 'N°', 'No.', 'Nr.', 'Nr.', 'Nr.'),
    ('tur_c_status', 'Stato', 'Status', 'Stare', 'Status', 'Status'),
    ('tur_c_client', 'Cliente', 'Client', 'Client', 'Kunde', 'Kund'),
    ('tur_c_product', 'Prodotto', 'Product', 'Produs', 'Produkt', 'Produkt'),
    ('tur_c_order', 'Ordine', 'Order', 'Comandă', 'Auftrag', 'Order'),
    ('tur_c_label', 'Scheda', 'Card', 'Fișă', 'Karte', 'Kort'),
    ('tur_c_defect', 'Difetto', 'Defect', 'Defect', 'Fehler', 'Defekt'),
    ('tur_c_sev', 'Sev.', 'Sev.', 'Sev.', 'Schw.', 'Allv.'),
    ('tur_c_dept', 'Reparto', 'Department', 'Departament', 'Abteilung', 'Avdelning'),
    ('tur_c_user', 'Operatore', 'Operator', 'Operator', 'Bediener', 'Operatör'),
    ('tur_c_resp', '1ª risp.(min)', '1st resp.(min)', 'Prim răsp.(min)', '1. Antw.(min)', '1:a svar(min)'),
    ('tur_c_reopen', 'Riap.', 'Reop.', 'Redesch.', 'Wied.', 'Åter.'),
    ('tur_c_boss', 'Capo', 'Boss', 'Șef', 'Chef', 'Chef'),
    ('tur_c_actions', 'Azioni', 'Actions', 'Acțiuni', 'Aktionen', 'Åtgärder'),
    ('tur_c_period', 'Periodo', 'Period', 'Perioadă', 'Zeitraum', 'Period'),
    # sintesi
    ('tur_sum_defect', 'Per difetto', 'By defect', 'După defect', 'Nach Fehler', 'Per defekt'),
    ('tur_sum_client', 'Per cliente', 'By client', 'După client', 'Nach Kunde', 'Per kund'),
    ('tur_sum_product', 'Per prodotto', 'By product', 'După produs', 'Nach Produkt', 'Per produkt'),
    ('tur_sum_dept', 'Per reparto', 'By department', 'După departament', 'Nach Abteilung', 'Per avdelning'),
    ('tur_sum_period', 'Per periodo', 'By period', 'După perioadă', 'Nach Zeitraum', 'Per period'),
    ('tur_sc_count', 'Segnalazioni', 'Reports', 'Raportări', 'Meldungen', 'Rapporter'),
    ('tur_sc_avgresp', 'Tempo medio (min)', 'Avg time (min)', 'Timp mediu (min)',
     'Ø Zeit (min)', 'Snitt-tid (min)'),
    ('tur_sc_reopen', 'Riaperti', 'Reopened', 'Redeschise', 'Wiedereröffnet', 'Återöppnade'),
    ('tur_group_by', 'Raggruppa per:', 'Group by:', 'Grupare după:', 'Gruppieren nach:', 'Gruppera efter:'),
    ('tur_gb_day', 'Giorno', 'Day', 'Zi', 'Tag', 'Dag'),
    ('tur_gb_week', 'Settimana', 'Week', 'Săptămână', 'Woche', 'Vecka'),
    ('tur_gb_month', 'Mese', 'Month', 'Lună', 'Monat', 'Månad'),
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
    conn.commit()
    conn.close()
    print(f"[OK] TouchUp report translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
