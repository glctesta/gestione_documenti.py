-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_PROJECT_VALIDATIONS.sql
-- Descrizione: Aggiunge traduzioni per validazioni date progetto e milestone
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- error_project_end_before_tasks
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_project_end_before_tasks')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_project_end_before_tasks', 'La data fine progetto non può essere precedente all''ultima data di scadenza dei task.');
    PRINT 'Traduzione IT aggiunta: error_project_end_before_tasks';
END
ELSE PRINT 'Traduzione IT già esistente: error_project_end_before_tasks';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_project_end_before_tasks')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_project_end_before_tasks', 'Data finalizare proiect nu poate fi înainte de ultima dată de scadență a taskurilor.');
    PRINT 'Traduzione RO aggiunta: error_project_end_before_tasks';
END
ELSE PRINT 'Traduzione RO già esistente: error_project_end_before_tasks';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_project_end_before_tasks')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_project_end_before_tasks', 'The project end date cannot be before the latest task due date.');
    PRINT 'Traduzione EN aggiunta: error_project_end_before_tasks';
END
ELSE PRINT 'Traduzione EN già esistente: error_project_end_before_tasks';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_project_end_before_tasks')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_project_end_before_tasks', 'Das Projektende kann nicht vor dem letzten Aufgabenfälligkeitsdatum liegen.');
    PRINT 'Traduzione DE aggiunta: error_project_end_before_tasks';
END
ELSE PRINT 'Traduzione DE già esistente: error_project_end_before_tasks';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_project_end_before_tasks')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_project_end_before_tasks', 'Projektets slutdatum kan inte vara före senaste uppgiftens förfallodatum.');
    PRINT 'Traduzione SV aggiunta: error_project_end_before_tasks';
END
ELSE PRINT 'Traduzione SV già esistente: error_project_end_before_tasks';
GO

-- ========================================
-- warning_no_milestone_defined
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'warning_no_milestone_defined')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'warning_no_milestone_defined', '⚠ Nessun task definito come milestone finale');
    PRINT 'Traduzione IT aggiunta: warning_no_milestone_defined';
END
ELSE PRINT 'Traduzione IT già esistente: warning_no_milestone_defined';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'warning_no_milestone_defined')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'warning_no_milestone_defined', '⚠ Niciun task definit ca milestone final');
    PRINT 'Traduzione RO aggiunta: warning_no_milestone_defined';
END
ELSE PRINT 'Traduzione RO già esistente: warning_no_milestone_defined';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'warning_no_milestone_defined')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'warning_no_milestone_defined', '⚠ No task defined as final milestone');
    PRINT 'Traduzione EN aggiunta: warning_no_milestone_defined';
END
ELSE PRINT 'Traduzione EN già esistente: warning_no_milestone_defined';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'warning_no_milestone_defined')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'warning_no_milestone_defined', '⚠ Keine Aufgabe als finaler Meilenstein definiert');
    PRINT 'Traduzione DE aggiunta: warning_no_milestone_defined';
END
ELSE PRINT 'Traduzione DE già esistente: warning_no_milestone_defined';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'warning_no_milestone_defined')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'warning_no_milestone_defined', '⚠ Ingen uppgift definierad som slutlig milstolpe');
    PRINT 'Traduzione SV aggiunta: warning_no_milestone_defined';
END
ELSE PRINT 'Traduzione SV già esistente: warning_no_milestone_defined';
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per validazioni progetto verificate/aggiunte per:';
PRINT '  - error_project_end_before_tasks';
PRINT '  - warning_no_milestone_defined';
PRINT 'Lingue: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
