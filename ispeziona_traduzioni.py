"""
Script per verificare i valori attuali delle traduzioni e correggerli
"""
import pyodbc

# Configurazione database
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = "emsreset"
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
               f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')

# Chiavi da verificare
KEYS = [
    'optional_upgrade_message',
    'force_upgrade_message_mandatory',
    'force_upgrade_message_max_skips'
]

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    
    print("VALORI ATTUALI NEL DATABASE:")
    print("=" * 100)
    
    for key in KEYS:
        print(f"\nChiave: {key}")
        print("-" * 100)
        
        cursor.execute("""
            SELECT LanguageCode, TranslationValue 
            FROM [dbo].[AppTranslations] 
            WHERE TranslationKey = ?
            ORDER BY LanguageCode
        """, key)
        
        results = cursor.fetchall()
        
        for row in results:
            value = row.TranslationValue
            # Mostra solo lingua italiana per brevità
            if row.LanguageCode == 'it':
                print(f"[{row.LanguageCode}] {repr(value)}")
                
                # Cerca placeholder malformati
                if '{(0)}' in value or '{(1)}' in value or '{(2)}' in value:
                    print("  ^^^ TROVATO PLACEHOLDER MALFORMATO: {(0)}, {(1)} o {(2)}")
                elif '{0}' in value and '{1}' in value:
                    print("  Placeholder corretti trovati: {0}, {1}")
                else:
                    print("  Nessun placeholder trovato")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERRORE: {e}")
    import traceback
    traceback.print_exc()
