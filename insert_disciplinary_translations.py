"""
Script per inserire le traduzioni per la funzione Note Disciplinari.
Tabella: [Traceability_RS].[dbo].[AppTranslations]
Lingue: ro, it, en, de, sv
"""
import pyodbc
import sys

conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=RS-RUNSERVER;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

translations = [
    ('submenu_disciplinary_notes', 'Note disciplinare', 'Note disciplinari', 'Disciplinary Notes', 'Disziplinarische Notizen', 'Disciplinära anteckningar'),
    ('submenu_disciplinary_commission', 'Comisie disciplinară', 'Commissione disciplinare', 'Disciplinary Commission', 'Disziplinarkommission', 'Disciplinärt utskott'),
    ('emissione_note_disciplinari', 'Emitere notă disciplinară', 'Emissione nota disciplinare', 'Issue Disciplinary Note', 'Disziplinarische Notiz ausstellen', 'Utfärda disciplinärt meddelande'),
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
                'ro': row[1], 'it': row[2], 'en': row[3],
                'de': row[4], 'sv': row[5],
            }
            for lang_code, value in lang_values.items():
                sql = """
                IF NOT EXISTS (
                    SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations]
                    WHERE [LanguageCode] = ? AND [TranslationKey] = ?
                )
                INSERT INTO [Traceability_RS].[dbo].[AppTranslations]
                    ([LanguageCode], [TranslationKey], [TranslationValue])
                VALUES (?, ?, ?)
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
