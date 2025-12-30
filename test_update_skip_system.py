"""
Script di Test per il Sistema di Rinvio Aggiornamenti
======================================================
Questo script permette di testare tutti gli scenari del sistema
di rinvio aggiornamenti senza dover modificare il database o
ricompilare l'applicazione.
"""

import os
import json
import sys
from datetime import datetime

# Percorso del file JSON di test
TEST_JSON_FILE = "update_skip_count_TEST.json"


def create_test_json(skip_count, version):
    """Crea un file JSON di test con i parametri specificati."""
    data = {
        'skip_count': skip_count,
        'last_version': version,
        'last_skip_date': datetime.now().isoformat()
    }
    with open(TEST_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✓ File JSON di test creato: skip_count={skip_count}, version={version}")


def read_test_json():
    """Legge il file JSON di test."""
    if not os.path.exists(TEST_JSON_FILE):
        print("✗ File JSON di test non trovato")
        return None
    
    with open(TEST_JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📄 Contenuto file JSON:")
    print(f"   Skip Count: {data.get('skip_count', 0)}")
    print(f"   Last Version: {data.get('last_version', 'N/A')}")
    print(f"   Last Skip Date: {data.get('last_skip_date', 'N/A')}")
    return data


def delete_test_json():
    """Elimina il file JSON di test."""
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)
        print("✓ File JSON di test eliminato")
    else:
        print("✗ File JSON di test non trovato")


def print_scenario_header(scenario_num, title):
    """Stampa l'intestazione di uno scenario di test."""
    print("\n" + "=" * 70)
    print(f"SCENARIO {scenario_num}: {title}")
    print("=" * 70)


def print_test_instructions(db_version, db_must, current_version, skip_count=None):
    """Stampa le istruzioni per configurare il test."""
    print("\n📋 CONFIGURAZIONE TEST:")
    print(f"   Database:")
    print(f"      - Version: {db_version}")
    print(f"      - Must: {db_must}")
    print(f"   Applicazione:")
    print(f"      - APP_VERSION: {current_version}")
    if skip_count is not None:
        print(f"   File JSON:")
        print(f"      - skip_count: {skip_count}")
        print(f"      - last_version: {db_version}")


def print_expected_behavior(behavior):
    """Stampa il comportamento atteso."""
    print(f"\n✅ COMPORTAMENTO ATTESO:")
    for line in behavior:
        print(f"   {line}")


def main():
    """Menu principale per i test."""
    print("\n" + "=" * 70)
    print("SISTEMA DI TEST - RINVIO AGGIORNAMENTI")
    print("=" * 70)
    
    while True:
        print("\n📌 MENU PRINCIPALE:")
        print("   1. Test Scenario 1: Aggiornamento Obbligatorio (Must=True)")
        print("   2. Test Scenario 2: Primo Rinvio (0/3)")
        print("   3. Test Scenario 3: Secondo Rinvio (1/3)")
        print("   4. Test Scenario 4: Terzo Rinvio (2/3)")
        print("   5. Test Scenario 5: Limite Raggiunto (3/3)")
        print("   6. Test Scenario 6: Nuova Versione Disponibile (Reset)")
        print("   7. Test Scenario 7: Nessun Aggiornamento Necessario")
        print("   ---")
        print("   8. Crea File JSON Personalizzato")
        print("   9. Leggi File JSON Corrente")
        print("   10. Elimina File JSON")
        print("   ---")
        print("   0. Esci")
        
        choice = input("\n👉 Scegli un'opzione: ").strip()
        
        if choice == '0':
            print("\n👋 Arrivederci!")
            break
        
        elif choice == '1':
            # Scenario 1: Aggiornamento Obbligatorio
            print_scenario_header(1, "Aggiornamento Obbligatorio (Must=True)")
            print_test_instructions(
                db_version="2.2.0",
                db_must="True (1)",
                current_version="2.1.8"
            )
            print_expected_behavior([
                "→ Messaggio: 'È disponibile una nuova versione OBBLIGATORIA'",
                "→ Nessuna scelta per l'utente",
                "→ Avvio automatico updater",
                "→ Chiusura applicazione"
            ])
            print("\n⚠️  Per questo test NON serve creare un file JSON")
            print("    Il campo Must=True forza l'aggiornamento indipendentemente dai rinvii")
        
        elif choice == '2':
            # Scenario 2: Primo Rinvio
            print_scenario_header(2, "Primo Rinvio (0/3)")
            print_test_instructions(
                db_version="2.2.0",
                db_must="False (0)",
                current_version="2.1.8",
                skip_count=0
            )
            create_test_json(skip_count=0, version="2.2.0")
            print_expected_behavior([
                "→ Messaggio: 'Vuoi aggiornare ora? Puoi rinviare 3 volte'",
                "→ Utente sceglie Sì/No",
                "→ Se No: skip_count diventa 1, app continua",
                "→ Se Sì: avvio updater, chiusura app"
            ])
        
        elif choice == '3':
            # Scenario 3: Secondo Rinvio
            print_scenario_header(3, "Secondo Rinvio (1/3)")
            print_test_instructions(
                db_version="2.2.0",
                db_must="False (0)",
                current_version="2.1.8",
                skip_count=1
            )
            create_test_json(skip_count=1, version="2.2.0")
            print_expected_behavior([
                "→ Messaggio: 'Vuoi aggiornare ora? Puoi rinviare 2 volte'",
                "→ Utente sceglie Sì/No",
                "→ Se No: skip_count diventa 2, app continua",
                "→ Se Sì: avvio updater, chiusura app"
            ])
        
        elif choice == '4':
            # Scenario 4: Terzo Rinvio
            print_scenario_header(4, "Terzo Rinvio (2/3)")
            print_test_instructions(
                db_version="2.2.0",
                db_must="False (0)",
                current_version="2.1.8",
                skip_count=2
            )
            create_test_json(skip_count=2, version="2.2.0")
            print_expected_behavior([
                "→ Messaggio: 'Vuoi aggiornare ora? Puoi rinviare 1 volta'",
                "→ Utente sceglie Sì/No",
                "→ Se No: skip_count diventa 3, app continua",
                "→ Se Sì: avvio updater, chiusura app"
            ])
        
        elif choice == '5':
            # Scenario 5: Limite Raggiunto
            print_scenario_header(5, "Limite Raggiunto (3/3)")
            print_test_instructions(
                db_version="2.2.0",
                db_must="False (0)",
                current_version="2.1.8",
                skip_count=3
            )
            create_test_json(skip_count=3, version="2.2.0")
            print_expected_behavior([
                "→ Messaggio: 'Hai raggiunto il numero massimo di rinvii'",
                "→ Nessuna scelta per l'utente",
                "→ Avvio automatico updater",
                "→ Chiusura applicazione"
            ])
        
        elif choice == '6':
            # Scenario 6: Nuova Versione
            print_scenario_header(6, "Nuova Versione Disponibile (Reset)")
            print_test_instructions(
                db_version="2.3.0",  # Versione cambiata!
                db_must="False (0)",
                current_version="2.1.8",
                skip_count=3  # Aveva già 3 rinvii per la versione precedente
            )
            create_test_json(skip_count=3, version="2.2.0")  # Versione vecchia
            print_expected_behavior([
                "→ Sistema rileva che la versione è cambiata (2.2.0 → 2.3.0)",
                "→ skip_count viene resettato automaticamente a 0",
                "→ Messaggio: 'Vuoi aggiornare ora? Puoi rinviare 3 volte'",
                "→ Nuovo ciclo di rinvii inizia"
            ])
        
        elif choice == '7':
            # Scenario 7: Nessun Aggiornamento
            print_scenario_header(7, "Nessun Aggiornamento Necessario")
            print_test_instructions(
                db_version="2.1.8",  # Stessa versione dell'app
                db_must="False (0)",
                current_version="2.1.8"
            )
            create_test_json(skip_count=2, version="2.1.8")
            print_expected_behavior([
                "→ Nessun aggiornamento necessario",
                "→ File JSON viene eliminato (reset)",
                "→ App continua normalmente",
                "→ Messaggio console: 'Versione applicazione (2.1.8) aggiornata.'"
            ])
        
        elif choice == '8':
            # Crea JSON Personalizzato
            print("\n📝 CREA FILE JSON PERSONALIZZATO")
            try:
                skip_count = int(input("   Skip Count (0-3): ").strip())
                version = input("   Versione (es. 2.2.0): ").strip()
                create_test_json(skip_count, version)
            except ValueError:
                print("✗ Errore: inserire un numero valido per skip_count")
        
        elif choice == '9':
            # Leggi JSON
            print("\n📖 LETTURA FILE JSON")
            read_test_json()
        
        elif choice == '10':
            # Elimina JSON
            print("\n🗑️  ELIMINAZIONE FILE JSON")
            delete_test_json()
        
        else:
            print("✗ Opzione non valida")


def print_database_setup_instructions():
    """Stampa le istruzioni per configurare il database per i test."""
    print("\n" + "=" * 70)
    print("ISTRUZIONI PER CONFIGURARE IL DATABASE")
    print("=" * 70)
    print("""
Per testare correttamente il sistema, devi configurare il database:

1. Assicurati che il campo 'Must' esista nella tabella SwVersions:
   
   Esegui: ADD_MUST_FIELD_TO_SWVERSIONS.sql

2. Per testare diversi scenari, modifica il record nel database:

   -- Aggiornamento OBBLIGATORIO (Scenario 1)
   UPDATE [dbo].[SwVersions]
   SET [Version] = '2.2.0', [Must] = 1
   WHERE [NameProgram] = 'main.exe' AND [dateout] IS NULL;

   -- Aggiornamento OPZIONALE (Scenari 2-7)
   UPDATE [dbo].[SwVersions]
   SET [Version] = '2.2.0', [Must] = 0
   WHERE [NameProgram] = 'main.exe' AND [dateout] IS NULL;

   -- Nessun aggiornamento (Scenario 7)
   UPDATE [dbo].[SwVersions]
   SET [Version] = '2.1.8', [Must] = 0
   WHERE [NameProgram] = 'main.exe' AND [dateout] IS NULL;

3. Verifica la configurazione:

   SELECT [NameProgram], [Version], [Must], [MainPath]
   FROM [dbo].[SwVersions]
   WHERE [NameProgram] = 'main.exe' AND [dateout] IS NULL;

NOTA: Ricorda di modificare anche APP_VERSION in main.py se necessario
      per simulare versioni diverse dell'applicazione.
""")


if __name__ == "__main__":
    print_database_setup_instructions()
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Questo script crea file JSON di TEST")
    print("   - Il file si chiama: update_skip_count_TEST.json")
    print("   - L'applicazione usa: update_skip_count.json")
    print("   - Per testare, rinomina il file TEST in update_skip_count.json")
    print("   - Oppure modifica get_update_skip_file_path() per usare il file TEST")
    
    input("\n👉 Premi INVIO per continuare...")
    main()
