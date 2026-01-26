"""
Script finale per correggere/aggiornare le traduzioni con i placeholder corretti
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

# Traduzioni corrette (quelle già presenti verranno aggiornate se necessario)
translations_correct = {
    # upgrade_required_title
    'upgrade_required_title': {
        'it': 'Aggiornamento Richiesto',
        'en': 'Update Required',
        'ro': 'Actualizare Necesară',
        'de': 'Update Erforderlich',
        'sv': 'Uppdatering Krävs',
    },
    
    # upgrade_available_title
    'upgrade_available_title': {
        'it': 'Aggiornamento Disponibile',
        'en': 'Update Available',
        'ro': 'Actualizare Disponibilă',
        'de': 'Update Verfügbar',
        'sv': 'Uppdatering Tillgänglig',
    },
    
    # force_upgrade_message_mandatory
    'force_upgrade_message_mandatory': {
        'it': 'È disponibile una nuova versione OBBLIGATORIA ({0}).\nLa versione attuale è obsoleta ({1}).\n\nIl programma si chiuderà per avviare l\'aggiornamento automatico.',
        'en': 'A new MANDATORY version is available ({0}).\nThe current version is outdated ({1}).\n\nThe program will close to start the automatic update.',
        'ro': 'Este disponibilă o nouă versiune OBLIGATORIE ({0}).\nVersiunea curentă este depășită ({1}).\n\nProgramul se va închide pentru a începe actualizarea automată.',
        'de': 'Eine neue OBLIGATORISCHE Version ist verfügbar ({0}).\nDie aktuelle Version ist veraltet ({1}).\n\nDas Programm wird geschlossen, um das automatische Update zu starten.',
        'sv': 'En ny OBLIGATORISK version är tillgänglig ({0}).\nDen nuvarande versionen är föråldrad ({1}).\n\nProgrammet kommer att stängas för att starta den automatiska uppdateringen.',
    },
    
    # force_upgrade_message_max_skips
    'force_upgrade_message_max_skips': {
        'it': 'È disponibile una nuova versione ({0}).\nLa versione attuale è obsoleta ({1}).\n\nHai raggiunto il numero massimo di rinvii (3).\nIl programma si chiuderà per avviare l\'aggiornamento automatico.',
        'en': 'A new version is available ({0}).\nThe current version is outdated ({1}).\n\nYou have reached the maximum number of postponements (3).\nThe program will close to start the automatic update.',
        'ro': 'Este disponibilă o nouă versiune ({0}).\nVersiunea curentă este depășită ({1}).\n\nAți atins numărul maxim de amânări (3).\nProgramul se va închide pentru a începe actualizarea automată.',
        'de': 'Eine neue Version ist verfügbar ({0}).\nDie aktuelle Version ist veraltet ({1}).\n\nSie haben die maximale Anzahl von Verschiebungen erreicht (3).\nDas Programm wird geschlossen, um das automatische Update zu starten.',
        'sv': 'En ny version är tillgänglig ({0}).\nDen nuvarande versionen är föråldrad ({1}).\n\nDu har nått det maximala antalet uppskjutningar (3).\nProgrammet kommer att stängas för att starta den automatiska uppdateringen.',
    },
    
    # optional_upgrade_message
    'optional_upgrade_message': {
        'it': 'È disponibile una nuova versione ({0}).\nLa versione attuale è ({1}).\n\nVuoi aggiornare ora?\n\nPuoi ancora rinviare l\'aggiornamento {2} volte.',
        'en': 'A new version is available ({0}).\nThe current version is ({1}).\n\nDo you want to update now?\n\nYou can still postpone the update {2} times.',
        'ro': 'Este disponibilă o nouă versiune ({0}).\nVersiunea curentă este ({1}).\n\nDoriți să actualizați acum?\n\nPuteți amâna încă actualizarea de {2} ori.',
        'de': 'Eine neue Version ist verfügbar ({0}).\nDie aktuelle Version ist ({1}).\n\nMöchten Sie jetzt aktualisieren?\n\nSie können das Update noch {2} Mal verschieben.',
        'sv': 'En ny version är tillgänglig ({0}).\nDen nuvarande versionen är ({1}).\n\nVill du uppdatera nu?\n\nDu kan fortfarande skjuta upp uppdateringen {2} gånger.',
    },
}

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    
    updated = 0
    inserted = 0
    unchanged = 0
    
    print("AGGIORNAMENTO TRADUZIONI")
    print("=" * 80)
    
    for key, lang_values in translations_correct.items():
        print(f"\nChiave: {key}")
        
        for lang, value in lang_values.items():
            # Verifica se esiste
            cursor.execute("""
                SELECT TranslationValue FROM [dbo].[AppTranslations] 
                WHERE LanguageCode = ? AND TranslationKey = ?
            """, lang, key)
            
            result = cursor.fetchone()
            
            if result:
                # Esiste - confronta e aggiorna se necessario
                current_value = result[0]
                if current_value != value:
                    cursor.execute("""
                        UPDATE [dbo].[AppTranslations]
                        SET TranslationValue = ?
                        WHERE LanguageCode = ? AND TranslationKey = ?
                    """, value, lang, key)
                    updated += 1
                    print(f"  [~] Aggiornato: {lang}")
                else:
                    unchanged += 1
                    print(f"  [=] Invariato: {lang}")
            else:
                # Non esiste - inserisci
                cursor.execute("""
                    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
                    VALUES (?, ?, ?)
                """, lang, key, value)
                inserted += 1
                print(f"  [+] Inserito: {lang}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("RISULTATO:")
    print(f"  Inseriti:   {inserted}")
    print(f"  Aggiornati: {updated}")
    print(f"  Invariati:  {unchanged}")
    print(f"  Totale:     {inserted + updated + unchanged}")
    print("\n OK - Operazione completata!")
    
except Exception as e:
    print(f"ERRORE: {e}")
    import traceback
    traceback.print_exc()
