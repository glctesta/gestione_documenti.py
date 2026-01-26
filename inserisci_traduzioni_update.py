"""
Script semplificato per inserire le traduzioni mancanti
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

# Traduzioni da inserire
translations = [
    # upgrade_required_title
    ('it', 'upgrade_required_title', 'Aggiornamento Richiesto'),
    ('en', 'upgrade_required_title', 'Update Required'),
    ('ro', 'upgrade_required_title', 'Actualizare Necesară'),
    ('de', 'upgrade_required_title','Update Erforderlich'),
    ('sv', 'upgrade_required_title', 'Uppdatering Krävs'),
    
    # upgrade_available_title
    ('it', 'upgrade_available_title', 'Aggiornamento Disponibile'),
    ('en', 'upgrade_available_title', 'Update Available'),
    ('ro', 'upgrade_available_title', 'Actualizare Disponibilă'),
    ('de', 'upgrade_available_title', 'Update Verfügbar'),
    ('sv', 'upgrade_available_title', 'Uppdatering Tillgänglig'),
    
    # force_upgrade_message_mandatory
    ('it', 'force_upgrade_message_mandatory', 
     'È disponibile una nuova versione OBBLIGATORIA ({0}).\nLa versione attuale è obsoleta ({1}).\n\nIl programma si chiuderà per avviare l\'aggiornamento automatico.'),
    ('en', 'force_upgrade_message_mandatory', 
     'A new MANDATORY version is available ({0}).\nThe current version is outdated ({1}).\n\nThe program will close to start the automatic update.'),
    ('ro', 'force_upgrade_message_mandatory', 
     'Este disponibilă o nouă versiune OBLIGATORIE ({0}).\nVersiunea curentă este depășită ({1}).\n\nProgramul se va închide pentru a începe actualizarea automată.'),
    ('de', 'force_upgrade_message_mandatory', 
     'Eine neue OBLIGATORISCHE Version ist verfügbar ({0}).\nDie aktuelle Version ist veraltet ({1}).\n\nDas Programm wird geschlossen, um das automatische Update zu starten.'),
    ('sv', 'force_upgrade_message_mandatory', 
     'En ny OBLIGATORISK version är tillgänglig ({0}).\nDen nuvarande versionen är föråldrad ({1}).\n\nProgrammet kommer att stängas för att starta den automatiska uppdateringen.'),
    
    # force_upgrade_message_max_skips
    ('it', 'force_upgrade_message_max_skips', 
     'È disponibile una nuova versione ({0}).\nLa versione attuale è obsoleta ({1}).\n\nHai raggiunto il numero massimo di rinvii (3).\nIl programma si chiuderà per avviare l\'aggiornamento automatico.'),
    ('en', 'force_upgrade_message_max_skips', 
     'A new version is available ({0}).\nThe current version is outdated ({1}).\n\nYou have reached the maximum number of postponements (3).\nThe program will close to start the automatic update.'),
    ('ro', 'force_upgrade_message_max_skips', 
     'Este disponibilă o nouă versiune ({0}).\nVersiunea curentă este depășită ({1}).\n\nAți atins numărul maxim de amânări (3).\nProgramul se va închide pentru a începe actualizarea automată.'),
    ('de', 'force_upgrade_message_max_skips', 
     'Eine neue Version ist verfügbar ({0}).\nDie aktuelle Version ist veraltet ({1}).\n\nSie haben die maximale Anzahl von Verschiebungen erreicht (3).\nDas Programm wird geschlossen, um das automatische Update zu starten.'),
    ('sv', 'force_upgrade_message_max_skips', 
     'En ny version är tillgänglig ({0}).\nDen nuvarande versionen är föråldrad ({1}).\n\nDu har nått det maximala antalet uppskjutningar (3).\nProgrammet kommer att stängas för att starta den automatiska uppdateringen.'),
    
    # optional_upgrade_message
    ('it', 'optional_upgrade_message', 
     'È disponibile una nuova versione ({0}).\nLa versione attuale è ({1}).\n\nVuoi aggiornare ora?\n\nPuoi ancora rinviare l\'aggiornamento {2} volte.'),
    ('en', 'optional_upgrade_message', 
     'A new version is available ({0}).\nThe current version is ({1}).\n\nDo you want to update now?\n\nYou can still postpone the update {2} times.'),
    ('ro', 'optional_upgrade_message', 
     'Este disponibilă o nouă versiune ({0}).\nVersiunea curentă este ({1}).\n\nDoriți să actualizați acum?\n\nPuteți amâna încă actualizarea de {2} ori.'),
    ('de', 'optional_upgrade_message', 
     'Eine neue Version ist verfügbar ({0}).\nDie aktuelle Version ist ({1}).\n\nMöchten Sie jetzt aktualisieren?\n\nSie können das Update noch {2} Mal verschieben.'),
    ('sv', 'optional_upgrade_message', 
     'En ny version är tillgänglig ({0}).\nDen nuvarande versionen är ({1}).\n\nVill du uppdatera nu?\n\nDu kan fortfarande skjuta upp uppdateringen {2} gånger.'),
]

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for lang, key, value in translations:
        # Controlla se esiste
        cursor.execute("""
            SELECT COUNT(*) FROM [dbo].[AppTranslations] 
            WHERE LanguageCode = ? AND TranslationKey = ?
        """, lang, key)
        
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Inserisci
            cursor.execute("""
                INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
                VALUES (?, ?, ?)
            """, lang, key, value)
            inserted += 1
            print(f"[+] Inserito: {lang} - {key}")
        else:
            skipped += 1
            print(f"[=] Gia presente: {lang} - {key}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\nRISULTATO:")
    print(f"  Inseriti: {inserted}")
    print(f"  Saltati (gia presenti): {skipped}")
    print(f"  Totale: {len(translations)}")
    print("\nOK - Traduzioni aggiunte con successo!")
    
except Exception as e:
    print(f"ERRORE: {e}")
    import traceback
    traceback.print_exc()
