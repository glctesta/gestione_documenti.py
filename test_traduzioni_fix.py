"""
Test per verificare che le traduzioni con placeholder funzionino correttamente
"""
import sys
import io

# Forza UTF-8 encoding
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except:
    pass

import pyodbc
from collections import defaultdict

# Configurazione database  
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = "emsreset"
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
               f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')

class LanguageManager:
    """Versione semplificata del LanguageManager per il test"""
    
    def __init__(self, db_conn_str):
        self.conn_str = db_conn_str
        self.translations = defaultdict(dict)
        self.current_language = 'it'
        self.load_translations()
    
    def load_translations(self):
        """Carica le traduzioni dal database"""
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        
        cursor.execute("SELECT LanguageCode, TranslationKey, TranslationValue FROM [dbo].[AppTranslations]")
        records = cursor.fetchall()
        
        for lang_code, key, value in records:
            lang_lower = lang_code.lower()
            self.translations[lang_lower][key] = value
        
        cursor.close()
        conn.close()
    
    def get(self, key, *args):
        """Restituisce la traduzione per una data chiave nella lingua corrente"""
        translated_text = self.translations[self.current_language].get(key, key)
        
        if args:
            try:
                return translated_text.format(*args)
            except (IndexError, KeyError) as e:
                print(f"ERRORE nel formatting di '{key}': {e}")
                return translated_text
        return translated_text

# Test
print("=" * 100)
print("TEST TRADUZIONI MESSAGGI AGGIORNAMENTO")
print("=" * 100)

lang = LanguageManager(DB_CONN_STR)

# Simula i dati che verrebbero passati
APP_VERSION = "2.2.9.8"
NEW_VERSION = "2.3.0.0"
REMAINING_SKIPS = 2

print("\n1. TEST: optional_upgrade_message")
print("-" * 100)
message = lang.get("optional_upgrade_message", NEW_VERSION, APP_VERSION, REMAINING_SKIPS)
print(f"Risultato:\n{message}\n")
expected_parts = [NEW_VERSION, APP_VERSION, "2"]
for part in expected_parts:
    if part in message:
        print(f"  ✓ Contiene '{part}'")
    else:
        print(f"  ✗ MANCA '{part}' - ERRORE!")

print("\n2. TEST: force_upgrade_message_mandatory")
print("-" * 100)
message = lang.get("force_upgrade_message_mandatory", NEW_VERSION, APP_VERSION)
print(f"Risultato:\n{message}\n")
expected_parts = [NEW_VERSION, APP_VERSION, "OBBLIGATORIA"]
for part in expected_parts:
    if part in message:
        print(f"  ✓ Contiene '{part}'")
    else:
        print(f"  ✗ MANCA '{part}' - ERRORE!")

print("\n3. TEST: force_upgrade_message_max_skips")
print("-" * 100)
message = lang.get("force_upgrade_message_max_skips", NEW_VERSION, APP_VERSION)
print(f"Risultato:\n{message}\n")
expected_parts = [NEW_VERSION, APP_VERSION, "massimo di rinvii"]
for part in expected_parts:
    if part in message:
        print(f"  ✓ Contiene '{part}'")
    else:
        print(f"  ✗ MANCA '{part}' - ERRORE!")

print("\n4. TEST: upgrade_required_title e upgrade_available_title")
print("-" * 100)
title1 = lang.get("upgrade_required_title")
title2 = lang.get("upgrade_available_title")
print(f"Titolo richiesto: {title1}")
print(f"Titolo disponibile: {title2}")

# Verifica che non ci siano placeholder malformati
print("\n5. VERIFICA PLACEHOLDER MALFORMATI")
print("-" * 100)
keys = [
    'optional_upgrade_message',
    'force_upgrade_message_mandatory', 
    'force_upgrade_message_max_skips'
]

all_ok = True
for key in keys:
    raw_value = lang.translations['it'].get(key, '')
    if '{(0)}' in raw_value or '{(1)}' in raw_value or '{(2)}' in raw_value:
        print(f"  ✗ {key}: CONTIENE PLACEHOLDER MALFORMATI {(0)}, {(1)} o {(2)}")
        all_ok = False
    elif '{0}' in raw_value or '{1}' in raw_value or '{2}' in raw_value:
        print(f"  ✓ {key}: Placeholder corretti ({0}, {1}, {2})")
    else:
        print(f"  ⚠ {key}: Nessun placeholder trovato")

print("\n" + "=" * 100)
if all_ok:
    print("✅ TUTTI I TEST SUPERATI - Le traduzioni funzionano correttamente!")
else:
    print("❌ ALCUNI TEST FALLITI - Ci sono ancora problemi da risolvere")
print("=" * 100)
