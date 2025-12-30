#!/usr/bin/env python3
# Test rapido per verificare se le traduzioni sono accessibili

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import Database, LanguageManager

# Connessione
conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=vandewiele.local\\emsreset;"
    "DATABASE=Traceability_rs;"
    "UID=emsreset;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
    "MARS_Connection=Yes;"
    "TrustServerCertificate=Yes"
)

print("Connessione al database...")
db = Database(conn_str)
if not db.connect():
    print(f"❌ Errore: {db.last_error_details}")
    sys.exit(1)

print("✅ Connesso\n")

# Crea LanguageManager
print("Creazione LanguageManager...")
lang = LanguageManager(db)

print(f"\n📊 Statistiche:")
print(f"   Lingua corrente: {lang.current_language}")
print(f"   Lingue disponibili: {list(lang.translations.keys())}")

for l in lang.translations:
    print(f"   {l.upper()}: {len(lang.translations[l])} chiavi")

# Test chiavi NPI
print(f"\n🔍 Test chiavi NPI (lingua: {lang.current_language}):")
test_keys = [
    'project_window_title',
    'col_task', 
    'status_todo',
    'btn_import_tasks',
    'save_doc'
]

for key in test_keys:
    value = lang.get(key)
    status = "✅" if value != key else "❌"
    print(f"   {status} {key}: '{value}'")

db.conn.close()
