#!/usr/bin/env python3
# Script per verificare le traduzioni usando la connessione dell'app

import sys
import os

# Aggiungi il path corrente
sys.path.insert(0, os.path.dirname(__file__))

from main import Database

# Crea connessione
conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=vandewiele.local\\emsreset;"
    "DATABASE=Traceability_rs;"
    "UID=emsreset;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
    "MARS_Connection=Yes;"
    "TrustServerCertificate=Yes"
)

db = Database(conn_str)
if not db.connect():
    print(f"❌ Errore connessione: {db.last_error_details}")
    sys.exit(1)

print("✅ Connesso al database\n")

try:
    # Verifica se la tabella esiste
    db.cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'dbo' 
        AND TABLE_NAME = 'AppTranslations'
    """)
    table_exists = db.cursor.fetchone()[0]
    
    if table_exists == 0:
        print("❌ ERRORE: La tabella [dbo].[AppTranslations] NON ESISTE!")
        print("\nDevi creare la tabella prima di inserire le traduzioni.")
    else:
        print("✅ La tabella [dbo].[AppTranslations] esiste\n")
        
        # Conta totale traduzioni
        db.cursor.execute("SELECT COUNT(*) FROM [Traceability_RS].[dbo].[AppTranslations]")
        total = db.cursor.fetchone()[0]
        print(f"📊 Totale traduzioni nel database: {total}\n")
        
        if total == 0:
            print("⚠️  ATTENZIONE: La tabella è vuota!")
            print("   Le traduzioni non sono state inserite.")
            print("   Esegui lo script SQL: NPI_ALL_TRANSLATIONS.sql")
        else:
            # Conta per lingua
            db.cursor.execute("""
                SELECT LanguageCode, COUNT(*) as Count
                FROM [Traceability_RS].[dbo].[AppTranslations]
                GROUP BY LanguageCode
                ORDER BY LanguageCode
            """)
            print("📋 Traduzioni per lingua:")
            for row in db.cursor.fetchall():
                print(f"   {row[0]}: {row[1]} traduzioni")
            
            # Verifica alcune chiavi NPI specifiche
            print("\n🔍 Verifica chiavi NPI:")
            test_keys = ['project_window_title', 'col_task', 'status_todo', 'btn_import_tasks']
            
            for key in test_keys:
                db.cursor.execute("""
                    SELECT LanguageCode, TranslationValue 
                    FROM [Traceability_RS].[dbo].[AppTranslations]
                    WHERE TranslationKey = ?
                    ORDER BY LanguageCode
                """, key)
                results = db.cursor.fetchall()
                
                if results:
                    print(f"\n   ✅ '{key}':")
                    for lang, value in results:
                        print(f"      {lang}: {value}")
                else:
                    print(f"\n   ❌ '{key}': NON TROVATA")

except Exception as e:
    print(f"❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
finally:
    if db.conn:
        db.conn.close()
