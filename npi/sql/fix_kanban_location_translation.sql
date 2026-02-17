-- Script SQL per correggere traduzione Kanban "Select Location"
-- Eseguire su database TraceabilityRS

-- Italiano
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'it')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Seleziona una locazione valida.'
    WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'it';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'move_err_select_location', N'Seleziona una locazione valida.');

-- Inglese
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'en')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Select a valid location.'
    WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'en';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'move_err_select_location', N'Select a valid location.');

-- Tedesco
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'de')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Wählen Sie einen gültigen Standort aus.'
    WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'de';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'move_err_select_location', N'Wählen Sie einen gültigen Standort aus.');

-- Rumeno
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'ro')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Selectați o locație validă.'
    WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'move_err_select_location', N'Selectați o locație validă.');

-- Svedese
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'sv')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Välj en giltig plats.'
    WHERE [TranslationKey] = N'move_err_select_location' AND [LanguageCode] = N'sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'move_err_select_location', N'Välj en giltig plats.');

GO

-- Verifica traduzioni corrette
SELECT LanguageCode, TranslationKey, TranslationValue
FROM [dbo].[AppTranslations]
WHERE TranslationKey = 'move_err_select_location'
ORDER BY LanguageCode;
