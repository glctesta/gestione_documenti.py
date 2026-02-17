-- Script SQL per correggere traduzione Kanban "Select Component"
-- Eseguire su database TraceabilityRS

-- Italiano
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'it')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Seleziona un componente valido.'
    WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'it';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'move_err_select_component', N'Seleziona un componente valido.');

-- Inglese
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'en')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Select a valid component.'
    WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'en';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'move_err_select_component', N'Select a valid component.');

-- Tedesco
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'de')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Wählen Sie eine gültige Komponente aus.'
    WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'de';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'move_err_select_component', N'Wählen Sie eine gültige Komponente aus.');

-- Rumeno
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'ro')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Selectați o componentă validă.'
    WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'move_err_select_component', N'Selectați o componentă validă.');

-- Svedese
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'sv')
    UPDATE [dbo].[AppTranslations]
    SET [TranslationValue] = N'Välj en giltig komponent.'
    WHERE [TranslationKey] = N'move_err_select_component' AND [LanguageCode] = N'sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'move_err_select_component', N'Välj en giltig komponent.');

GO

-- Verifica traduzioni corrette
SELECT LanguageCode, TranslationKey, TranslationValue
FROM [dbo].[AppTranslations]
WHERE TranslationKey = 'move_err_select_component'
ORDER BY LanguageCode;
