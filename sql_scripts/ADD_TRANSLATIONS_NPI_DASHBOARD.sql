-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_DASHBOARD.sql
-- Descrizione: Aggiunge traduzioni per il NPI Dashboard Window
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- npi_dashboard_title
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'npi_dashboard_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'npi_dashboard_title', 'Dashboard Progetti NPI');
    PRINT 'Traduzione IT aggiunta: npi_dashboard_title';
END
ELSE PRINT 'Traduzione IT già esistente: npi_dashboard_title';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'npi_dashboard_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'npi_dashboard_title', 'Dashboard Proiecte NPI');
    PRINT 'Traduzione RO aggiunta: npi_dashboard_title';
END
ELSE PRINT 'Traduzione RO già esistente: npi_dashboard_title';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'npi_dashboard_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'npi_dashboard_title', 'NPI Projects Dashboard');
    PRINT 'Traduzione EN aggiunta: npi_dashboard_title';
END
ELSE PRINT 'Traduzione EN già esistente: npi_dashboard_title';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'npi_dashboard_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'npi_dashboard_title', 'NPI-Projekte Dashboard');
    PRINT 'Traduzione DE aggiunta: npi_dashboard_title';
END
ELSE PRINT 'Traduzione DE già esistente: npi_dashboard_title';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'npi_dashboard_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'npi_dashboard_title', 'NPI-projekt Dashboard');
    PRINT 'Traduzione SV aggiunta: npi_dashboard_title';
END
ELSE PRINT 'Traduzione SV già esistente: npi_dashboard_title';
GO

-- ========================================
-- active_npi_projects
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'active_npi_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'active_npi_projects', 'Progetti NPI Attivi');
    PRINT 'Traduzione IT aggiunta: active_npi_projects';
END
ELSE PRINT 'Traduzione IT già esistente: active_npi_projects';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'active_npi_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'active_npi_projects', 'Proiecte NPI Active');
    PRINT 'Traduzione RO aggiunta: active_npi_projects';
END
ELSE PRINT 'Traduzione RO già esistente: active_npi_projects';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'active_npi_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'active_npi_projects', 'Active NPI Projects');
    PRINT 'Traduzione EN aggiunta: active_npi_projects';
END
ELSE PRINT 'Traduzione EN già esistente: active_npi_projects';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'active_npi_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'active_npi_projects', 'Aktive NPI-Projekte');
    PRINT 'Traduzione DE aggiunta: active_npi_projects';
END
ELSE PRINT 'Traduzione DE già esistente: active_npi_projects';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'active_npi_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'active_npi_projects', 'Aktiva NPI-projekt');
    PRINT 'Traduzione SV aggiunta: active_npi_projects';
END
ELSE PRINT 'Traduzione SV già esistente: active_npi_projects';
GO

-- ========================================
-- col_project_end_date (NUOVA TRADUZIONE)
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'col_project_end_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'col_project_end_date', 'Data Fine Progetto');
    PRINT 'Traduzione IT aggiunta: col_project_end_date';
END
ELSE PRINT 'Traduzione IT già esistente: col_project_end_date';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'col_project_end_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'col_project_end_date', 'Data Finalizare Proiect');
    PRINT 'Traduzione RO aggiunta: col_project_end_date';
END
ELSE PRINT 'Traduzione RO già esistente: col_project_end_date';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'col_project_end_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'col_project_end_date', 'Project End Date');
    PRINT 'Traduzione EN aggiunta: col_project_end_date';
END
ELSE PRINT 'Traduzione EN già esistente: col_project_end_date';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'col_project_end_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'col_project_end_date', 'Projektende');
    PRINT 'Traduzione DE aggiunta: col_project_end_date';
END
ELSE PRINT 'Traduzione DE già esistente: col_project_end_date';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'col_project_end_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'col_project_end_date', 'Projektets Slutdatum');
    PRINT 'Traduzione SV aggiunta: col_project_end_date';
END
ELSE PRINT 'Traduzione SV già esistente: col_project_end_date';
GO

-- ========================================
-- no_active_projects
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'no_active_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'no_active_projects', 'Nessun progetto attivo trovato.');
    PRINT 'Traduzione IT aggiunta: no_active_projects';
END
ELSE PRINT 'Traduzione IT già esistente: no_active_projects';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'no_active_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'no_active_projects', 'Niciun proiect activ găsit.');
    PRINT 'Traduzione RO aggiunta: no_active_projects';
END
ELSE PRINT 'Traduzione RO già esistente: no_active_projects';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'no_active_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'no_active_projects', 'No active projects found.');
    PRINT 'Traduzione EN aggiunta: no_active_projects';
END
ELSE PRINT 'Traduzione EN già esistente: no_active_projects';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'no_active_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'no_active_projects', 'Keine aktiven Projekte gefunden.');
    PRINT 'Traduzione DE aggiunta: no_active_projects';
END
ELSE PRINT 'Traduzione DE già esistente: no_active_projects';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'no_active_projects')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'no_active_projects', 'Inga aktiva projekt hittades.');
    PRINT 'Traduzione SV aggiunta: no_active_projects';
END
ELSE PRINT 'Traduzione SV già esistente: no_active_projects';
GO

-- ========================================
-- manage_project
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'manage_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'manage_project', 'Gestisci Dettagli Task...');
    PRINT 'Traduzione IT aggiunta: manage_project';
END
ELSE PRINT 'Traduzione IT già esistente: manage_project';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'manage_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'manage_project', 'Gestionare Detalii Task...');
    PRINT 'Traduzione RO aggiunta: manage_project';
END
ELSE PRINT 'Traduzione RO già esistente: manage_project';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'manage_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'manage_project', 'Manage Task Details...');
    PRINT 'Traduzione EN aggiunta: manage_project';
END
ELSE PRINT 'Traduzione EN già esistente: manage_project';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'manage_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'manage_project', 'Aufgabendetails verwalten...');
    PRINT 'Traduzione DE aggiunta: manage_project';
END
ELSE PRINT 'Traduzione DE già esistente: manage_project';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'manage_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'manage_project', 'Hantera Uppgiftsdetaljer...');
    PRINT 'Traduzione SV aggiunta: manage_project';
END
ELSE PRINT 'Traduzione SV già esistente: manage_project';
GO

-- ========================================
-- npi_view_gantt
-- ========================================

-- IT
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'npi_view_gantt')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'npi_view_gantt', 'Visualizza Gantt...');
    PRINT 'Traduzione IT aggiunta: npi_view_gantt';
END
ELSE PRINT 'Traduzione IT già esistente: npi_view_gantt';
GO

-- RO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'npi_view_gantt')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'npi_view_gantt', 'Vizualizare Gantt...');
    PRINT 'Traduzione RO aggiunta: npi_view_gantt';
END
ELSE PRINT 'Traduzione RO già esistente: npi_view_gantt';
GO

-- EN
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'npi_view_gantt')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'npi_view_gantt', 'View Gantt...');
    PRINT 'Traduzione EN aggiunta: npi_view_gantt';
END
ELSE PRINT 'Traduzione EN già esistente: npi_view_gantt';
GO

-- DE
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'npi_view_gantt')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'npi_view_gantt', 'Gantt anzeigen...');
    PRINT 'Traduzione DE aggiunta: npi_view_gantt';
END
ELSE PRINT 'Traduzione DE già esistente: npi_view_gantt';
GO

-- SV
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'npi_view_gantt')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'npi_view_gantt', 'Visa Gantt...');
    PRINT 'Traduzione SV aggiunta: npi_view_gantt';
END
ELSE PRINT 'Traduzione SV già esistente: npi_view_gantt';
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per Dashboard NPI verificate/aggiunte per:';
PRINT '  - npi_dashboard_title';
PRINT '  - active_npi_projects';
PRINT '  - col_project_end_date (NUOVA)';
PRINT '  - no_active_projects';
PRINT '  - manage_project';
PRINT '  - npi_view_gantt';
PRINT 'Lingue: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
