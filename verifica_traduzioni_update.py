"""
Script per verificare e inserire le traduzioni mancanti per i messaggi di aggiornamento
"""
import sys
import io

# Forza UTF-8 encoding per l'output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
TRANSLATION_KEYS = [
    'upgrade_required_title',
    'upgrade_available_title',
    'force_upgrade_message_mandatory',
    'force_upgrade_message_max_skips',
    'optional_upgrade_message'
]

print("=" * 80)
print("VERIFICA TRADUZIONI MESSAGGI AGGIORNAMENTO")
print("=" * 80)

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    
    print("\n1. Controllando traduzioni esistenti...")
    for key in TRANSLATION_KEYS:
        query = """
            SELECT LanguageCode, TranslationKey, TranslationValue 
            FROM [dbo].[AppTranslations] 
            WHERE TranslationKey = ?
            ORDER BY LanguageCode
        """
        cursor.execute(query, key)
        results = cursor.fetchall()
        
        print(f"\n  Chiave: {key}")
        if results:
            for row in results:
                # Mostra solo i primi 50 caratteri del valore
                value_preview = row.TranslationValue[:50] + "..." if len(row.TranslationValue) > 50 else row.TranslationValue
                print(f"    [{row.LanguageCode}] {value_preview}")
        else:
            print(f"    ⚠️  MANCANTE - Nessuna traduzione trovata!")
    
    print("\n" + "=" * 80)
    print("2. Eseguendo inserimento SQL dal file...")
    print("=" * 80)
    
    # Leggi e esegui il file SQL
    with open('TRADUZIONI_AGGIORNAMENTO_VERSIONE.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Dividi lo script per i GO statements
    batches = sql_script.split('GO')
    
    for i, batch in enumerate(batches, 1):
        batch = batch.strip()
        if batch and not batch.startswith('--') and batch != 'USE [Traceability_RS]':
            try:
                cursor.execute(batch)
                conn.commit()
                print(f"  ✓ Batch {i}/{len(batches)} eseguito con successo")
            except Exception as e:
                print(f"  ✗ Errore nel batch {i}: {e}")
    
    print("\n" + "=" * 80)
    print("3. VERIFICA FINALE - Controllando traduzioni dopo l'inserimento...")
    print("=" * 80)
    
    for key in TRANSLATION_KEYS:
        query = """
            SELECT LanguageCode, TranslationValue 
            FROM [dbo].[AppTranslations] 
            WHERE TranslationKey = ?
            ORDER BY LanguageCode
        """
        cursor.execute(query, key)
        results = cursor.fetchall()
        
        print(f"\n  Chiave: {key}")
        if results:
            for row in results:
                # Mostra i primi 80 caratteri
                value_preview = row.TranslationValue[:80].replace('\n', ' ') + "..." if len(row.TranslationValue) > 80 else row.TranslationValue.replace('\n', ' ')
                print(f"    [{row.LanguageCode}] {value_preview}")
        else:
            print(f"    ⚠️  ANCORA MANCANTE!")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ OPERAZIONE COMPLETATA CON SUCCESSO!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
