-- =============================================
-- Traduzioni per FAI Fails Email Menu Item
-- =============================================

USE [Traceability_RS]
GO

-- send_fai_fails_email (menu item)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'send_fai_fails_email' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'send_fai_fails_email', N'📧 Invia Email FAI Fails')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'send_fai_fails_email' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'send_fai_fails_email', N'📧 Send FAI Fails Email')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'send_fai_fails_email' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'send_fai_fails_email', N'📧 Trimite Email Defecte FAI')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'send_fai_fails_email' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'send_fai_fails_email', N'📧 FAI-Fehler-E-Mail senden')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'send_fai_fails_email' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'send_fai_fails_email', N'📧 Skicka FAI-fel-e-post')

GO

PRINT 'Traduzioni per menu FAI Fails Email aggiunte con successo!'
