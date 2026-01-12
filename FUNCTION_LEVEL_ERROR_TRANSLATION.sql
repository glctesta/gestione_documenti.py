-- =====================================================
-- Script traduzioni per Controllo Livello Funzionale Manutenzione
-- Data: 2026-01-12
-- Descrizione: Aggiunge traduzioni per il messaggio di errore
--              quando l'utente non ha il livello funzionale
--              richiesto per eseguire un'operazione di manutenzione
-- Lingue: IT, RO, EN, DE, SV
-- =====================================================

USE [Traceability_RS]
GO

-- ========== ITALIANO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'function_level_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'function_level_error', 'L''operazione di manutenzione è stata assegnata a una funzione superiore [{0}]. Questa attività non può essere eseguita dal tuo livello funzionale.');

-- ========== RUMENO (con N per caratteri speciali Unicode) ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'function_level_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'function_level_error', N'Operațiunea de întreținere a fost atribuită unei funcții superioare [{0}]. Această activitate nu poate fi executată de nivelul tău funcțional.');

-- ========== INGLESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'function_level_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'function_level_error', 'The maintenance operation has been assigned to a higher function [{0}]. This activity cannot be performed by your functional level.');

-- ========== TEDESCO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'function_level_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'function_level_error', 'Der Wartungsvorgang wurde einer höheren Funktion [{0}] zugewiesen. Diese Aktivität kann von Ihrer Funktionsebene nicht ausgeführt werden.');

-- ========== SVEDESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'function_level_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'function_level_error', 'Underhållsoperationen har tilldelats en högre funktion [{0}]. Denna aktivitet kan inte utföras av din funktionsnivå.');

GO

PRINT '✅ Traduzioni per controllo livello funzionale aggiunte con successo!';
PRINT '   - Lingue supportate: IT, RO, EN, DE, SV';
PRINT '   - Chiave: function_level_error';
PRINT '   - Supporta placeholder {0} per nome funzione richiesta';
GO
