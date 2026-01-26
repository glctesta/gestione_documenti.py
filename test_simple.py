"""Test semplice delle traduzioni"""
import pyodbc

DB_CONN_STR = ('DRIVER={SQL Server Native Client 11.0};'
               'SERVER=roghipsql01.vandewiele.local\\emsreset;'
               'DATABASE=Traceability_rs;'
               'UID=emsreset;'
               'PWD=E6QhqKUxHFXTbkB7eA8c9ya;'
               'MARS_Connection=Yes;TrustServerCertificate=Yes')

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    
    # Test 1: Leggi la traduzione italiana del messaggio opzionale
    cursor.execute("""
        SELECT TranslationValue FROM [dbo].[AppTranslations] 
        WHERE LanguageCode = 'it' AND TranslationKey = 'optional_upgrade_message'
    """)
    
    result = cursor.fetchone()
    if result:
        template = result[0]
        
        # Simula la sostituzione dei placeholder come fa il codice reale
        try:
            message = template.format("2.3.0.0", "2.2.9.8", 2)
            
            # Verifica che i valori siano presenti
            checks = [
                ("2.3.0.0" in message, "Versione nuova"),
                ("2.2.9.8" in message, "Versione attuale"),
                ("2" in message, "Numero rinvii"),
                ("{0}" not in message, "No placeholder {0}"),
                ("{1}" not in message, "No placeholder {1}"),
                ("{2}" not in message, "No placeholder {2}"),
            ]
            
            all_ok = all(check[0] for check in checks)
            
            if all_ok:
                print("OK - Test superato!")
                print(f"Messaggio formattato correttamente:")
                print(message)
            else:
                print("ERRORE - Test fallito!")
                for check, desc in checks:
                    status = "OK" if check else "FAIL"
                    print(f"  [{status}] {desc}")
                print(f"\nMessaggio:")
                print(message)
                
        except Exception as e:
            print(f"ERRORE nel formatting: {e}")
            print(f"Template: {template}")
    else:
        print("ERRORE - Traduzione non trovata nel database")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERRORE: {e}")
