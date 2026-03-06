"""
Script per inserire le traduzioni relative ai rapporti straordinari.
Tabella: [Traceability_RS].[dbo].[AppTranslations]
Lingue: ro, it, en, de, sv
"""

import pyodbc
import sys

# Connessione al database
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=RS-RUNSERVER;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

# (key, ro, it, en, de, sv)
translations = [
    ('day_of_week', 'Ziua', 'Giorno', 'Day', 'Tag', 'Dag'),
    ('overtime_reports_title', 'Rapoarte ore suplimentare', 'Rapporti Straordinari', 'Overtime Reports', 'Überstundenberichte', 'Övertidsrapporter'),
    ('filters', 'Filtre', 'Filtri', 'Filters', 'Filter', 'Filter'),
    ('period', 'Perioadă:', 'Periodo:', 'Period:', 'Zeitraum:', 'Period:'),
    ('from', 'De la:', 'Da:', 'From:', 'Von:', 'Från:'),
    ('to', 'Până la:', 'A:', 'To:', 'Bis:', 'Till:'),
    ('report_type', 'Tip raport:', 'Tipo Rapporto:', 'Report Type:', 'Berichtstyp:', 'Rapporttyp:'),
    ('summary_report', 'Rezumat general', 'Riepilogo Generale', 'Summary Report', 'Gesamtübersicht', 'Sammanfattning'),
    ('by_employee', 'Pe angajat', 'Per Dipendente', 'By Employee', 'Nach Mitarbeiter', 'Per anställd'),
    ('by_reason', 'Pe motiv', 'Per Motivo', 'By Reason', 'Nach Grund', 'Per orsak'),
    ('by_department', 'Pe departament', 'Per Reparto', 'By Department', 'Nach Abteilung', 'Per avdelning'),
    ('generate_report', 'Generează raport', 'Genera Rapporto', 'Generate Report', 'Bericht erstellen', 'Generera rapport'),
    ('results', 'Rezultate', 'Risultati', 'Results', 'Ergebnisse', 'Resultat'),
    ('table_view', 'Vizualizare tabel', 'Vista Tabella', 'Table View', 'Tabellenansicht', 'Tabellvy'),
    ('statistics', 'Statistici', 'Statistiche', 'Statistics', 'Statistiken', 'Statistik'),
    ('export_excel', 'Exportă Excel', 'Esporta Excel', 'Export Excel', 'Excel exportieren', 'Exportera Excel'),
    ('export_pdf', 'Exportă PDF', 'Esporta PDF', 'Export PDF', 'PDF exportieren', 'Exportera PDF'),
    ('no_data_to_export', 'Nu există date de exportat', 'Nessun dato da esportare', 'No data to export', 'Keine Daten zum Exportieren', 'Inga data att exportera'),
    ('save_excel', 'Salvează Excel', 'Salva Excel', 'Save Excel', 'Excel speichern', 'Spara Excel'),
    ('excel_exported', 'Fișier Excel exportat cu succes', 'File Excel esportato con successo', 'Excel file exported successfully', 'Excel-Datei erfolgreich exportiert', 'Excel-fil exporterad'),
]

def main():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        inserted = 0
        skipped = 0
        
        for row in translations:
            key = row[0]
            lang_values = {
                'ro': row[1],
                'it': row[2],
                'en': row[3],
                'de': row[4],
                'sv': row[5],
            }
            
            for lang_code, value in lang_values.items():
                sql = """
                IF NOT EXISTS (
                    SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations]
                    WHERE [LanguageCode] = ? AND [TranslationKey] = ?
                )
                INSERT INTO [Traceability_RS].[dbo].[AppTranslations]
                    ([LanguageCode], [TranslationKey], [TranslationValue])
                VALUES (?, ?, N'' + ?)
                """
                cursor.execute(sql, (lang_code, key, lang_code, key, value))
                if cursor.rowcount > 0:
                    inserted += 1
                    print(f"  [OK] {lang_code}/{key} = {value}")
                else:
                    skipped += 1
                    print(f"  [SKIP] {lang_code}/{key} already exists")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\nInserted: {inserted}, Skipped: {skipped}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
