-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_DATE_DEPENDENCIES_VALIDATION.sql
-- Descrizione: Aggiunge traduzioni per la validazione delle date con dipendenze
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- error_start_after_project_end
-- ========================================

-- IT: La data di inizio non può essere successiva alla data fine progetto.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_start_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_start_after_project_end', 'La data di inizio non può essere successiva alla data fine progetto.');
    PRINT 'Traduzione IT aggiunta: error_start_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_start_after_project_end';
END
GO

-- RO: Data de început nu poate fi ulterioară datei de finalizare a proiectului.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_start_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_start_after_project_end', 'Data de început nu poate fi ulterioară datei de finalizare a proiectului.');
    PRINT 'Traduzione RO aggiunta: error_start_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_start_after_project_end';
END
GO

-- EN: The start date cannot be later than the project end date.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_start_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_start_after_project_end', 'The start date cannot be later than the project end date.');
    PRINT 'Traduzione EN aggiunta: error_start_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_start_after_project_end';
END
GO

-- DE: Das Startdatum darf nicht nach dem Projektende liegen.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_start_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_start_after_project_end', 'Das Startdatum darf nicht nach dem Projektende liegen.');
    PRINT 'Traduzione DE aggiunta: error_start_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_start_after_project_end';
END
GO

-- SV: Startdatumet kan inte vara senare än projektets slutdatum.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_start_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_start_after_project_end', 'Startdatumet kan inte vara senare än projektets slutdatum.');
    PRINT 'Traduzione SV aggiunta: error_start_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_start_after_project_end';
END
GO

-- ========================================
-- error_due_after_project_end
-- ========================================

-- IT: La data di scadenza non può essere successiva alla data fine progetto.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_due_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_due_after_project_end', 'La data di scadenza non può essere successiva alla data fine progetto.');
    PRINT 'Traduzione IT aggiunta: error_due_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_due_after_project_end';
END
GO

-- RO: Data scadenței nu poate fi ulterioară datei de finalizare a proiectului.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_due_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_due_after_project_end', 'Data scadenței nu poate fi ulterioară datei de finalizare a proiectului.');
    PRINT 'Traduzione RO aggiunta: error_due_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_due_after_project_end';
END
GO

-- EN: The due date cannot be later than the project end date.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_due_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_due_after_project_end', 'The due date cannot be later than the project end date.');
    PRINT 'Traduzione EN aggiunta: error_due_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_due_after_project_end';
END
GO

-- DE: Das Fälligkeitsdatum darf nicht nach dem Projektende liegen.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_due_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_due_after_project_end', 'Das Fälligkeitsdatum darf nicht nach dem Projektende liegen.');
    PRINT 'Traduzione DE aggiunta: error_due_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_due_after_project_end';
END
GO

-- SV: Förfallodatumet kan inte vara senare än projektets slutdatum.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_due_after_project_end'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_due_after_project_end', 'Förfallodatumet kan inte vara senare än projektets slutdatum.');
    PRINT 'Traduzione SV aggiunta: error_due_after_project_end';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_due_after_project_end';
END
GO

-- ========================================
-- error_start_before_dependency
-- ========================================
-- Nota: Questo messaggio include parametri dinamici (nome task e data)
-- La traduzione base è fornita, i parametri verranno sostituiti a runtime

-- IT: La data di inizio non può essere precedente alla data fine del task dipendente.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_start_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_start_before_dependency', 'La data di inizio non può essere precedente alla data fine del task dipendente.');
    PRINT 'Traduzione IT aggiunta: error_start_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_start_before_dependency';
END
GO

-- RO: Data de început nu poate fi anterioară datei de finalizare a taskului dependent.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_start_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_start_before_dependency', 'Data de început nu poate fi anterioară datei de finalizare a taskului dependent.');
    PRINT 'Traduzione RO aggiunta: error_start_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_start_before_dependency';
END
GO

-- EN: The start date cannot be earlier than the end date of the dependent task.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_start_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_start_before_dependency', 'The start date cannot be earlier than the end date of the dependent task.');
    PRINT 'Traduzione EN aggiunta: error_start_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_start_before_dependency';
END
GO

-- DE: Das Startdatum darf nicht vor dem Enddatum der abhängigen Aufgabe liegen.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_start_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_start_before_dependency', 'Das Startdatum darf nicht vor dem Enddatum der abhängigen Aufgabe liegen.');
    PRINT 'Traduzione DE aggiunta: error_start_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_start_before_dependency';
END
GO

-- SV: Startdatumet kan inte vara tidigare än slutdatumet för den beroende uppgiften.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_start_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_start_before_dependency', 'Startdatumet kan inte vara tidigare än slutdatumet för den beroende uppgiften.');
    PRINT 'Traduzione SV aggiunta: error_start_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_start_before_dependency';
END
GO

-- ========================================
-- error_due_before_dependency
-- ========================================
-- Nota: Questo messaggio include parametri dinamici (nome task e data)
-- La traduzione base è fornita, i parametri verranno sostituiti a runtime

-- IT: La data di scadenza non può essere precedente alla data fine del task dipendente.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_due_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_due_before_dependency', 'La data di scadenza non può essere precedente alla data fine del task dipendente.');
    PRINT 'Traduzione IT aggiunta: error_due_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_due_before_dependency';
END
GO

-- RO: Data scadenței nu poate fi anterioară datei de finalizare a taskului dependent.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_due_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_due_before_dependency', 'Data scadenței nu poate fi anterioară datei de finalizare a taskului dependent.');
    PRINT 'Traduzione RO aggiunta: error_due_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_due_before_dependency';
END
GO

-- EN: The due date cannot be earlier than the end date of the dependent task.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_due_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_due_before_dependency', 'The due date cannot be earlier than the end date of the dependent task.');
    PRINT 'Traduzione EN aggiunta: error_due_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_due_before_dependency';
END
GO

-- DE: Das Fälligkeitsdatum darf nicht vor dem Enddatum der abhängigen Aufgabe liegen.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_due_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_due_before_dependency', 'Das Fälligkeitsdatum darf nicht vor dem Enddatum der abhängigen Aufgabe liegen.');
    PRINT 'Traduzione DE aggiunta: error_due_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_due_before_dependency';
END
GO

-- SV: Förfallodatumet kan inte vara tidigare än slutdatumet för den beroende uppgiften.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_due_before_dependency'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_due_before_dependency', 'Förfallodatumet kan inte vara tidigare än slutdatumet för den beroende uppgiften.');
    PRINT 'Traduzione SV aggiunta: error_due_before_dependency';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_due_before_dependency';
END
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per validazione date con dipendenze verificate/aggiunte per:';
PRINT '  - error_start_after_project_end';
PRINT '  - error_due_after_project_end';
PRINT '  - error_start_before_dependency';
PRINT '  - error_due_before_dependency';
PRINT 'Lingue: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
