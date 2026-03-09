-- Script SQL per traduzione pulsante "Aggiorna Progetto"
-- Eseguire su database TraceabilityRS

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_update_npi_project' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'btn_update_npi_project', N'Aggiorna Progetto');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_update_npi_project' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'btn_update_npi_project', N'Update Project');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_update_npi_project' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'btn_update_npi_project', N'Projekt aktualisieren');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_update_npi_project' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'btn_update_npi_project', N'Actualizează Proiect');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_update_npi_project' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'btn_update_npi_project', N'Uppdatera projekt');

GO
