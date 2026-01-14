-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_ANALYSIS_WINDOW.sql
-- Descrizione: Aggiunge traduzioni per la finestra di Analisi Progetti NPI
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- analysis_window_title
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'analysis_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'analysis_window_title', 'Analisi Progetto');
    PRINT 'Traduzione IT aggiunta: analysis_window_title';
END
ELSE PRINT 'Traduzione IT già esistente: analysis_window_title';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'analysis_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'analysis_window_title', 'Analiză Proiect');
    PRINT 'Traduzione RO aggiunta: analysis_window_title';
END
ELSE PRINT 'Traduzione RO già esistente: analysis_window_title';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'analysis_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'analysis_window_title', 'Project Analysis');
    PRINT 'Traduzione EN aggiunta: analysis_window_title';
END
ELSE PRINT 'Traduzione EN già esistente: analysis_window_title';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'analysis_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'analysis_window_title', 'Projektanalyse');
    PRINT 'Traduzione DE aggiunta: analysis_window_title';
END
ELSE PRINT 'Traduzione DE già esistente: analysis_window_title';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'analysis_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'analysis_window_title', 'Projektanalys');
    PRINT 'Traduzione SV aggiunta: analysis_window_title';
END
ELSE PRINT 'Traduzione SV già esistente: analysis_window_title';
GO

-- ========================================
-- late_tasks_summary
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'late_tasks_summary')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'late_tasks_summary', 'Riepilogo Task in Ritardo');
    PRINT 'Traduzione IT aggiunta: late_tasks_summary';
END
ELSE PRINT 'Traduzione IT già esistente: late_tasks_summary';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'late_tasks_summary')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'late_tasks_summary', 'Rezumat Taskuri Întârziate');
    PRINT 'Traduzione RO aggiunta: late_tasks_summary';
END
ELSE PRINT 'Traduzione RO già esistente: late_tasks_summary';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'late_tasks_summary')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'late_tasks_summary', 'Overdue Tasks Summary');
    PRINT 'Traduzione EN aggiunta: late_tasks_summary';
END
ELSE PRINT 'Traduzione EN già esistente: late_tasks_summary';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'late_tasks_summary')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'late_tasks_summary', 'Übersicht Verspätete Aufgaben');
    PRINT 'Traduzione DE aggiunta: late_tasks_summary';
END
ELSE PRINT 'Traduzione DE già esistente: late_tasks_summary';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'late_tasks_summary')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'late_tasks_summary', 'Sammanfattning Försenade Uppgifter');
    PRINT 'Traduzione SV aggiunta: late_tasks_summary';
END
ELSE PRINT 'Traduzione SV già esistente: late_tasks_summary';
GO

-- ========================================
-- col_late_tasks_count
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'col_late_tasks_count')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'col_late_tasks_count', 'N. Task in Ritardo');
    PRINT 'Traduzione IT aggiunta: col_late_tasks_count';
END
ELSE PRINT 'Traduzione IT già esistente: col_late_tasks_count';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'col_late_tasks_count')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'col_late_tasks_count', 'Nr. Taskuri Întârziate');
    PRINT 'Traduzione RO aggiunta: col_late_tasks_count';
END
ELSE PRINT 'Traduzione RO già esistente: col_late_tasks_count';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'col_late_tasks_count')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'col_late_tasks_count', 'No. Overdue Tasks');
    PRINT 'Traduzione EN aggiunta: col_late_tasks_count';
END
ELSE PRINT 'Traduzione EN già esistente: col_late_tasks_count';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'col_late_tasks_count')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'col_late_tasks_count', 'Anz. Verspätete Aufgaben');
    PRINT 'Traduzione DE aggiunta: col_late_tasks_count';
END
ELSE PRINT 'Traduzione DE già esistente: col_late_tasks_count';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'col_late_tasks_count')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'col_late_tasks_count', 'Antal Försenade Uppgifter');
    PRINT 'Traduzione SV aggiunta: col_late_tasks_count';
END
ELSE PRINT 'Traduzione SV già esistente: col_late_tasks_count';
GO

-- ========================================
-- btn_send_reminders
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'btn_send_reminders')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'btn_send_reminders', 'Invia Solleciti');
    PRINT 'Traduzione IT aggiunta: btn_send_reminders';
END
ELSE PRINT 'Traduzione IT già esistente: btn_send_reminders';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'btn_send_reminders')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'btn_send_reminders', 'Trimite Memento-uri');
    PRINT 'Traduzione RO aggiunta: btn_send_reminders';
END
ELSE PRINT 'Traduzione RO già esistente: btn_send_reminders';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'btn_send_reminders')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'btn_send_reminders', 'Send Reminders');
    PRINT 'Traduzione EN aggiunta: btn_send_reminders';
END
ELSE PRINT 'Traduzione EN già esistente: btn_send_reminders';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'btn_send_reminders')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'btn_send_reminders', 'Erinnerungen Senden');
    PRINT 'Traduzione DE aggiunta: btn_send_reminders';
END
ELSE PRINT 'Traduzione DE già esistente: btn_send_reminders';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'btn_send_reminders')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'btn_send_reminders', 'Skicka Påminnelser');
    PRINT 'Traduzione SV aggiunta: btn_send_reminders';
END
ELSE PRINT 'Traduzione SV già esistente: btn_send_reminders';
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per Analysis Window verificate/aggiunte per:';
PRINT '  - analysis_window_title';
PRINT '  - late_tasks_summary';
PRINT '  - col_late_tasks_count';
PRINT '  - btn_send_reminders';
PRINT 'Lingue: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
