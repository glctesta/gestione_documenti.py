# -*- coding: utf-8 -*-
"""
insert_task_catalog_export_translations.py
Chiavi di traduzione per l'export Excel del Catalogo Task NPI
(bottone nel tab "Catalogo Task" della finestra di configurazione NPI).

Idempotente: salta le chiavi gia' presenti.
Run: python insert_task_catalog_export_translations.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from database_config import DatabaseConfig

# (key, it, en, ro, de, sv)
TRANSLATIONS = [
    ('btn_export_task_catalog',
     '📥 Esporta Excel (per categoria)', '📥 Export to Excel (by category)',
     '📥 Export Excel (pe categorii)', '📥 Nach Excel exportieren (nach Kategorie)',
     '📥 Exportera till Excel (per kategori)'),
    ('col_default_task', 'Default', 'Default', 'Implicit', 'Standard', 'Standard'),
    ('col_task_count', 'Numero task', 'Task count', 'Număr sarcini',
     'Anzahl Aufgaben', 'Antal uppgifter'),
    ('no_category', '(senza categoria)', '(no category)', '(fără categorie)',
     '(ohne Kategorie)', '(utan kategori)'),
    ('summary', 'Riepilogo', 'Summary', 'Rezumat', 'Zusammenfassung', 'Sammanfattning'),
    ('total', 'Totale', 'Total', 'Total', 'Gesamt', 'Totalt'),
    ('yes', 'Sì', 'Yes', 'Da', 'Ja', 'Ja'),
    ('no', 'No', 'No', 'Nu', 'Nein', 'Nej'),
    ('export_no_data',
     'Nessun task da esportare.', 'No tasks to export.',
     'Nu există sarcini de exportat.', 'Keine Aufgaben zum Exportieren.',
     'Inga uppgifter att exportera.'),
    ('export_file_locked',
     'Impossibile salvare: il file è aperto in Excel. Chiudilo e riprova.',
     'Cannot save: the file is open in Excel. Close it and try again.',
     'Salvarea nu este posibilă: fișierul este deschis în Excel. Închideți-l și reîncercați.',
     'Speichern nicht möglich: Die Datei ist in Excel geöffnet. Schließen Sie sie und versuchen Sie es erneut.',
     'Kan inte spara: filen är öppen i Excel. Stäng den och försök igen.'),
    ('export_done_open',
     'Export completato ({count} task).\n\n{path}\n\nVuoi aprire il file?',
     'Export completed ({count} tasks).\n\n{path}\n\nDo you want to open the file?',
     'Export finalizat ({count} sarcini).\n\n{path}\n\nDoriți să deschideți fișierul?',
     'Export abgeschlossen ({count} Aufgaben).\n\n{path}\n\nMöchten Sie die Datei öffnen?',
     'Exporten är klar ({count} uppgifter).\n\n{path}\n\nVill du öppna filen?'),
    ('excel_lib_missing',
     "La libreria 'openpyxl' non è installata.",
     "The 'openpyxl' library is not installed.",
     "Biblioteca 'openpyxl' nu este instalată.",
     "Die Bibliothek 'openpyxl' ist nicht installiert.",
     "Biblioteket 'openpyxl' är inte installerat."),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    inserted = skipped = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            val = row[i + 1]
            cur.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode = ? AND TranslationKey = ?",
                (lang, key),
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                    (lang, key, val),
                )
                inserted += 1
            else:
                skipped += 1
    conn.commit()
    conn.close()
    print(f"[OK] Task catalog export translations - Inserite: {inserted}, "
          f"Saltate (gia' presenti): {skipped}")


if __name__ == '__main__':
    main()
