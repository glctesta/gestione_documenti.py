-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_DATE_VALIDATION.sql
-- Descrizione: Aggiunge traduzioni per la validazione delle date nei task NPI
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- Traduzione: error_due_date_before_start
-- IT: La data di scadenza non può essere precedente alla data di inizio.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_due_date_before_start'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_due_date_before_start', 'La data di scadenza non può essere precedente alla data di inizio.');
    PRINT 'Traduzione IT aggiunta: error_due_date_before_start';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_due_date_before_start';
END
GO

-- RO: Data scadenței nu poate fi anterioară datei de început.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_due_date_before_start'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_due_date_before_start', 'Data scadenței nu poate fi anterioară datei de început.');
    PRINT 'Traduzione RO aggiunta: error_due_date_before_start';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_due_date_before_start';
END
GO

-- EN: The due date cannot be earlier than the start date.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_due_date_before_start'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_due_date_before_start', 'The due date cannot be earlier than the start date.');
    PRINT 'Traduzione EN aggiunta: error_due_date_before_start';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_due_date_before_start';
END
GO

-- DE: Das Fälligkeitsdatum darf nicht vor dem Startdatum liegen.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_due_date_before_start'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_due_date_before_start', 'Das Fälligkeitsdatum darf nicht vor dem Startdatum liegen.');
    PRINT 'Traduzione DE aggiunta: error_due_date_before_start';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_due_date_before_start';
END
GO

-- SV: Förfallodatumet kan inte vara tidigare än startdatumet.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_due_date_before_start'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_due_date_before_start', 'Förfallodatumet kan inte vara tidigare än startdatumet.');
    PRINT 'Traduzione SV aggiunta: error_due_date_before_start';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_due_date_before_start';
END
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per error_due_date_before_start verificate/aggiunte per: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
