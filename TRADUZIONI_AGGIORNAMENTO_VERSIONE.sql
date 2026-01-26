-- Traduzioni per i messaggi di aggiornamento versione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Da eseguire sul database per aggiungere le traduzioni necessarie

USE [Traceability_RS]
GO

-- ========================================
-- Titoli finestre di aggiornamento
-- ========================================

-- Titolo: Aggiornamento Richiesto
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'upgrade_required_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'upgrade_required_title', 'Aggiornamento Richiesto');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'upgrade_required_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'upgrade_required_title', 'Update Required');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'upgrade_required_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'upgrade_required_title', N'Actualizare Necesară');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'upgrade_required_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'upgrade_required_title', 'Update Erforderlich');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'upgrade_required_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'upgrade_required_title', 'Uppdatering Krävs');

GO

-- Titolo: Aggiornamento Disponibile
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'upgrade_available_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'upgrade_available_title', 'Aggiornamento Disponibile');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'upgrade_available_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'upgrade_available_title', 'Update Available');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'upgrade_available_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'upgrade_available_title', N'Actualizare Disponibilă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'upgrade_available_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'upgrade_available_title', 'Update Verfügbar');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'upgrade_available_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'upgrade_available_title', 'Uppdatering Tillgänglig');

GO

-- ========================================
-- Messaggi di aggiornamento obbligatorio
-- ========================================

-- Messaggio: Update obbligatorio (versione mandatoria)
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'force_upgrade_message_mandatory')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'force_upgrade_message_mandatory', N'È disponibile una nuova versione OBBLIGATORIA ({0}).
La versione attuale è obsoleta ({1}).

Il programma si chiuderà per avviare l''aggiornamento automatico.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'force_upgrade_message_mandatory')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'force_upgrade_message_mandatory', N'A new MANDATORY version is available ({0}).
The current version is outdated ({1}).

The program will close to start the automatic update.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'force_upgrade_message_mandatory')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'force_upgrade_message_mandatory', N'Este disponibilă o nouă versiune OBLIGATORIE ({0}).
Versiunea curentă este depășită ({1}).

Programul se va închide pentru a începe actualizarea automată.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'force_upgrade_message_mandatory')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'force_upgrade_message_mandatory', N'Eine neue OBLIGATORISCHE Version ist verfügbar ({0}).
Die aktuelle Version ist veraltet ({1}).

Das Programm wird geschlossen, um das automatische Update zu starten.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'force_upgrade_message_mandatory')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'force_upgrade_message_mandatory', N'En ny OBLIGATORISK version är tillgänglig ({0}).
Den nuvarande versionen är föråldrad ({1}).

Programmet kommer att stängas för att starta den automatiska uppdateringen.');

GO

-- Messaggio: Update obbligatorio (massimo rinvii raggiunto)
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'force_upgrade_message_max_skips')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'force_upgrade_message_max_skips', N'È disponibile una nuova versione ({0}).
La versione attuale è obsoleta ({1}).

Hai raggiunto il numero massimo di rinvii (3).
Il programma si chiuderà per avviare l''aggiornamento automatico.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'force_upgrade_message_max_skips')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'force_upgrade_message_max_skips', N'A new version is available ({0}).
The current version is outdated ({1}).

You have reached the maximum number of postponements (3).
The program will close to start the automatic update.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'force_upgrade_message_max_skips')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'force_upgrade_message_max_skips', N'Este disponibilă o nouă versiune ({0}).
Versiunea curentă este depășită ({1}).

Ați atins numărul maxim de amânări (3).
Programul se va închide pentru a începe actualizarea automată.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'force_upgrade_message_max_skips')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'force_upgrade_message_max_skips', N'Eine neue Version ist verfügbar ({0}).
Die aktuelle Version ist veraltet ({1}).

Sie haben die maximale Anzahl von Verschiebungen erreicht (3).
Das Programm wird geschlossen, um das automatische Update zu starten.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'force_upgrade_message_max_skips')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'force_upgrade_message_max_skips', N'En ny version är tillgänglig ({0}).
Den nuvarande versionen är föråldrad ({1}).

Du har nått det maximala antalet uppskjutningar (3).
Programmet kommer att stängas för att starta den automatiska uppdateringen.');

GO

-- ========================================
-- Messaggio di aggiornamento opzionale
-- ========================================

-- Messaggio: Update opzionale (con rinvii rimanenti)
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'optional_upgrade_message')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'optional_upgrade_message', N'È disponibile una nuova versione ({0}).
La versione attuale è ({1}).

Vuoi aggiornare ora?

Puoi ancora rinviare l''aggiornamento {2} volte.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'optional_upgrade_message')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'optional_upgrade_message', N'A new version is available ({0}).
The current version is ({1}).

Do you want to update now?

You can still postpone the update {2} times.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'optional_upgrade_message')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'optional_upgrade_message', N'Este disponibilă o nouă versiune ({0}).
Versiunea curentă este ({1}).

Doriți să actualizați acum?

Puteți amâna încă actualizarea de {2} ori.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'optional_upgrade_message')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'optional_upgrade_message', N'Eine neue Version ist verfügbar ({0}).
Die aktuelle Version ist ({1}).

Möchten Sie jetzt aktualisieren?

Sie können das Update noch {2} Mal verschieben.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'optional_upgrade_message')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'optional_upgrade_message', N'En ny version är tillgänglig ({0}).
Den nuvarande versionen är ({1}).

Vill du uppdatera nu?

Du kan fortfarande skjuta upp uppdateringen {2} gånger.');

GO

PRINT 'Traduzioni per l''aggiornamento versione aggiunte con successo!'
