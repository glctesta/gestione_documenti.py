#!/usr/bin/env python3
# Script per verificare le traduzioni nel database

import pyodbc

# Stringa di connessione (usa la stessa dell'applicazione)
conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=vandewiele.local\\emsreset;"
    "DATABASE=Traceability_rs;"
    "UID=emsreset;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
    "MARS_Connection=Yes;"
    "TrustServerCertificate=Yes"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Verifica se la tabella esiste
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'dbo' 
        AND TABLE_NAME = 'AppTranslations'
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists == 0:
        print("❌ ERRORE: La tabella [dbo].[AppTranslations] NON ESISTE!")
        print("\nDevi creare la tabella prima di inserire le traduzioni.")
        print("\nScript SQL per creare la tabella:")
        print("""
CREATE TABLE [Traceability_RS].[dbo].[AppTranslations] (
    [TranslationID] INT IDENTITY(1,1) PRIMARY KEY,
    [LanguageCode] NVARCHAR(10) NOT NULL,
    [TranslationKey] NVARCHAR(255) NOT NULL,
    [TranslationValue] NVARCHAR(MAX) NOT NULL,
    CONSTRAINT UQ_AppTranslations_Lang_Key UNIQUE ([LanguageCode], [TranslationKey])
);
        """)
    else:
        print("✅ La tabella [dbo].[AppTranslations] esiste\n")
        
        # Conta totale traduzioni
        cursor.execute("SELECT COUNT(*) FROM [Traceability_RS].[dbo].[AppTranslations]")
        total = cursor.fetchone()[0]
        print(f"📊 Totale traduzioni nel database: {total}\n")
        
        # Conta per lingua
        cursor.execute("""
            SELECT LanguageCode, COUNT(*) as Count
            FROM [Traceability_RS].[dbo].[AppTranslations]
            GROUP BY LanguageCode
            ORDER BY LanguageCode
        """)
        print("📋 Traduzioni per lingua:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} traduzioni")
        
        # Verifica alcune chiavi NPI specifiche
        print("\n🔍 Verifica chiavi NPI:")
        test_keys = ['project_window_title', 'col_task', 'status_todo', 'btn_import_tasks']
        
        for key in test_keys:
            cursor.execute("""
                SELECT LanguageCode, TranslationValue 
                FROM [Traceability_RS].[dbo].[AppTranslations]
                WHERE TranslationKey = ?
                ORDER BY LanguageCode
            """, key)
            results = cursor.fetchall()
            
            if results:
                print(f"\n   ✅ '{key}':")
                for lang, value in results:
                    print(f"      {lang}: {value}")
            else:
                print(f"\n   ❌ '{key}': NON TROVATA")
        
        # Mostra prime 10 chiavi per IT
        print("\n📝 Prime 10 chiavi italiane:")
        cursor.execute("""
            SELECT TOP 10 TranslationKey, TranslationValue
            FROM [Traceability_RS].[dbo].[AppTranslations]
            WHERE LanguageCode = 'it'
            ORDER BY TranslationKey
        """)
        for key, value in cursor.fetchall():
            print(f"   {key}: {value}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERRORE: {e}")
