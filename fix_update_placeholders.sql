-- ========================================
-- FIX UPDATE NOTIFICATION PLACEHOLDERS
-- ========================================
-- Questo script corregge i placeholder nelle traduzioni dei messaggi di aggiornamento
-- Problema: i placeholder {0}, {1}, {2} non vengono sostituiti correttamente

USE [Traceability_RS];
GO

-- ========================================
-- 1. FORCE UPGRADE MESSAGE - MANDATORY
-- ========================================

-- Italiano
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'È disponibile una nuova versione OBBLIGATORIA ({0}).
La versione attuale è obsoleta ({1}).

Il programma si chiuderà per avviare l''aggiornamento automatico.'
WHERE [TranslationKey] = 'force_upgrade_message_mandatory' AND [LanguageCode] = 'it';

-- English
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'A new MANDATORY version is available ({0}).
Your current version is obsolete ({1}).

The program will close to start the automatic update.'
WHERE [TranslationKey] = 'force_upgrade_message_mandatory' AND [LanguageCode] = 'en';

-- Romanian
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'O nouă versiune OBLIGATORIE este disponibilă ({0}).
Versiunea curentă este învechită ({1}).

Programul se va închide pentru a începe actualizarea automată.'
WHERE [TranslationKey] = 'force_upgrade_message_mandatory' AND [LanguageCode] = 'ro';

-- German
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'Eine neue OBLIGATORISCHE Version ist verfügbar ({0}).
Ihre aktuelle Version ist veraltet ({1}).

Das Programm wird geschlossen, um das automatische Update zu starten.'
WHERE [TranslationKey] = 'force_upgrade_message_mandatory' AND [LanguageCode] = 'de';

-- Swedish
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'En ny OBLIGATORISK version är tillgänglig ({0}).
Din nuvarande version är föråldrad ({1}).

Programmet kommer att stängas för att starta den automatiska uppdateringen.'
WHERE [TranslationKey] = 'force_upgrade_message_mandatory' AND [LanguageCode] = 'sv';

-- ========================================
-- 2. FORCE UPGRADE MESSAGE - MAX SKIPS
-- ========================================

-- Italiano
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'È disponibile una nuova versione ({0}).
La versione attuale è obsoleta ({1}).

Hai rinviato l''aggiornamento troppe volte.
Il programma si chiuderà per avviare l''aggiornamento automatico.'
WHERE [TranslationKey] = 'force_upgrade_message_max_skips' AND [LanguageCode] = 'it';

-- English
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'A new version is available ({0}).
Your current version is obsolete ({1}).

You have postponed the update too many times.
The program will close to start the automatic update.'
WHERE [TranslationKey] = 'force_upgrade_message_max_skips' AND [LanguageCode] = 'en';

-- Romanian
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'O nouă versiune este disponibilă ({0}).
Versiunea curentă este învechită ({1}).

Ați amânat actualizarea de prea multe ori.
Programul se va închide pentru a începe actualizarea automată.'
WHERE [TranslationKey] = 'force_upgrade_message_max_skips' AND [LanguageCode] = 'ro';

-- German
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'Eine neue Version ist verfügbar ({0}).
Ihre aktuelle Version ist veraltet ({1}).

Sie haben das Update zu oft verschoben.
Das Programm wird geschlossen, um das automatische Update zu starten.'
WHERE [TranslationKey] = 'force_upgrade_message_max_skips' AND [LanguageCode] = 'de';

-- Swedish
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'En ny version är tillgänglig ({0}).
Din nuvarande version är föråldrad ({1}).

Du har skjutit upp uppdateringen för många gånger.
Programmet kommer att stängas för att starta den automatiska uppdateringen.'
WHERE [TranslationKey] = 'force_upgrade_message_max_skips' AND [LanguageCode] = 'sv';

-- ========================================
-- 3. UPDATE NOTIFICATION MESSAGE (Dialog)
-- ========================================

-- Italiano
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'È disponibile una nuova versione ({0}).
La tua versione attuale è la {1}.

Cosa vuoi fare?'
WHERE [TranslationKey] = 'update_notification_message' AND [LanguageCode] = 'it';

-- English
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'A new version is available ({0}).
Your current version is {1}.

What would you like to do?'
WHERE [TranslationKey] = 'update_notification_message' AND [LanguageCode] = 'en';

-- Romanian
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'O nouă versiune este disponibilă ({0}).
Versiunea ta curentă este {1}.

Ce vrei să faci?'
WHERE [TranslationKey] = 'update_notification_message' AND [LanguageCode] = 'ro';

-- German
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'Eine neue Version ist verfügbar ({0}).
Ihre aktuelle Version ist {1}.

Was möchten Sie tun?'
WHERE [TranslationKey] = 'update_notification_message' AND [LanguageCode] = 'de';

-- Swedish
UPDATE [dbo].[AppTranslations]
SET [TranslationValue] = N'En ny version är tillgänglig ({0}).
Din nuvarande version är {1}.

Vad vill du göra?'
WHERE [TranslationKey] = 'update_notification_message' AND [LanguageCode] = 'sv';

PRINT '✅ PLACEHOLDER AGGIORNAMENTO CORRETTI!';
PRINT '   - force_upgrade_message_mandatory: 5 lingue';
PRINT '   - force_upgrade_message_max_skips: 5 lingue';
PRINT '   - update_notification_message: 5 lingue';
PRINT '   - TOTALE: 15 traduzioni aggiornate';
