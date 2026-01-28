-- =============================================
-- Script SQL per aggiungere le traduzioni
-- Modulo: Gestione Macchine (Maintenance)
-- Campo: production_year_label
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- =============================================

USE [Traceability_RS];
GO

-- =============================================
-- production_year_label (Anno Produzione)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'production_year_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'production_year_label', N'it', N'Anno Produzione');
    PRINT 'Aggiunta traduzione IT per production_year_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'production_year_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'production_year_label', N'en', N'Production Year');
    PRINT 'Aggiunta traduzione EN per production_year_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'production_year_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'production_year_label', N'ro', N'An Producție');
    PRINT 'Aggiunta traduzione RO per production_year_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'production_year_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'production_year_label', N'de', N'Produktionsjahr');
    PRINT 'Aggiunta traduzione DE per production_year_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'production_year_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'production_year_label', N'sv', N'Produktionsår');
    PRINT 'Aggiunta traduzione SV per production_year_label';
END

-- =============================================
-- Riepilogo
-- =============================================

PRINT '';
PRINT '=============================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzione aggiunta per: production_year_label';
PRINT 'Lingue: IT, EN, RO, DE, SV';
PRINT '=============================================';

GO
