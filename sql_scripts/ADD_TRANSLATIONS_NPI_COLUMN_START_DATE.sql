-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_COLUMN_START_DATE.sql
-- Descrizione: Aggiunge traduzioni per la colonna "Data Inizio" nella Treeview NPI
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- Traduzione: col_start_date (colonna Data Inizio nella Treeview)
-- IT: Inizio
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'col_start_date'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'col_start_date', 'Inizio');
    PRINT 'Traduzione IT aggiunta: col_start_date';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: col_start_date';
END
GO

-- RO: Început
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'col_start_date'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'col_start_date', 'Început');
    PRINT 'Traduzione RO aggiunta: col_start_date';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: col_start_date';
END
GO

-- EN: Start
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'col_start_date'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'col_start_date', 'Start');
    PRINT 'Traduzione EN aggiunta: col_start_date';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: col_start_date';
END
GO

-- DE: Anfang
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'col_start_date'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'col_start_date', 'Anfang');
    PRINT 'Traduzione DE aggiunta: col_start_date';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: col_start_date';
END
GO

-- SV: Start
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'col_start_date'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'col_start_date', 'Start');
    PRINT 'Traduzione SV aggiunta: col_start_date';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: col_start_date';
END
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per col_start_date verificate/aggiunte per: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
