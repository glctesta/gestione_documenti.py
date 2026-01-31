# Test per verificare il problema dei placeholder nelle traduzioni
import pyodbc

# Connessione al database
conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=EMSRESET;"
    "DATABASE=Traceability_RS;"
    "UID=sa;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Query per ottenere le traduzioni dei messaggi di aggiornamento
query = """
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] IN (
    'force_upgrade_message_mandatory',
    'force_upgrade_message_max_skips',
    'update_notification_message'
)
ORDER BY [TranslationKey], [LanguageCode]
"""

cursor.execute(query)
results = cursor.fetchall()

print("=" * 80)
print("TRADUZIONI MESSAGGI DI AGGIORNAMENTO")
print("=" * 80)

for lang, key, value in results:
    print(f"\nChiave: {key}")
    print(f"Lingua: {lang}")
    print(f"Valore: {repr(value)}")
    print(f"Lunghezza: {len(value)} caratteri")
    
    # Test formattazione
    try:
        formatted = value.format("2.3.1.5", "2.3.1.4", "test")
        print(f"✅ Formattazione OK: {formatted[:50]}...")
    except Exception as e:
        print(f"❌ Errore formattazione: {e}")
    print("-" * 80)

cursor.close()
conn.close()
