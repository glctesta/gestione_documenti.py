-- Script SQL per inserire traduzioni NPI Hierarchy
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: IT, EN, DE, RO, SV
-- Data: 2026-02-17

USE [Traceability_RS]
GO

-- ============================================
-- HIERARCHY SECTION TRANSLATIONS
-- ============================================

-- hierarchy_title: "🔗 Gerarchia"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_title', N'🔗 Gerarchia');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_title', N'🔗 Hierarchy');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_title', N'🔗 Hierarchie');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_title', N'🔗 Ierarhie');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_title', N'🔗 Hierarki');

-- hierarchy_parent_label: "Questo progetto è il PADRE"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_parent_label' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_parent_label', N'Questo progetto è il PADRE');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_parent_label' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_parent_label', N'This project is the PARENT');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_parent_label' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_parent_label', N'Dieses Projekt ist das ELTERNPROJEKT');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_parent_label' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_parent_label', N'Acest proiect este PĂRINTELE');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_parent_label' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_parent_label', N'Detta projekt är FÖRÄLDERPROJEKTET');

-- hierarchy_children_count: "Figli: {count}"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_count' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_children_count', N'Figli: {count}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_count' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_children_count', N'Children: {count}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_count' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_children_count', N'Kinder: {count}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_count' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_children_count', N'Copii: {count}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_count' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_children_count', N'Barn: {count}');

-- hierarchy_manage_children: "⚙️ Gestisci Figli"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_manage_children' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_manage_children', N'⚙️ Gestisci Figli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_manage_children' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_manage_children', N'⚙️ Manage Children');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_manage_children' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_manage_children', N'⚙️ Kinder verwalten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_manage_children' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_manage_children', N'⚙️ Gestionează Copii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_manage_children' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_manage_children', N'⚙️ Hantera Barn');

-- ============================================
-- DIALOG TRANSLATIONS
-- ============================================

-- hierarchy_children_title: "Progetti Figli"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_children_title', N'Progetti Figli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_children_title', N'Child Projects');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_children_title', N'Kinderprojekte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_children_title', N'Proiecte Copii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_children_title', N'Barnprojekt');

-- hierarchy_no_children: "Questo progetto non ha progetti figli."
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_no_children' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_no_children', N'Questo progetto non ha progetti figli.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_no_children' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_no_children', N'This project has no child projects.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_no_children' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_no_children', N'Dieses Projekt hat keine Kinderprojekte.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_no_children' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_no_children', N'Acest proiect nu are proiecte copii.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_no_children' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_no_children', N'Detta projekt har inga barnprojekt.');

-- hierarchy_children_of: "Progetti Figli di: {project}"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_of' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_children_of', N'Progetti Figli di: {project}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_of' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_children_of', N'Child Projects of: {project}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_of' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_children_of', N'Kinderprojekte von: {project}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_of' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_children_of', N'Proiecte Copii ale: {project}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_children_of' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_children_of', N'Barnprojekt av: {project}');

-- ============================================
-- TREEVIEW COLUMN HEADERS
-- ============================================

-- project_name: "Nome Progetto"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'project_name' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'project_name', N'Nome Progetto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'project_name' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'project_name', N'Project Name');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'project_name' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'project_name', N'Projektname');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'project_name' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'project_name', N'Nume Proiect');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'project_name' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'project_name', N'Projektnamn');

-- status: "Stato"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'status' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'status', N'Stato');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'status' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'status', N'Status');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'status' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'status', N'Status');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'status' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'status', N'Stare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'status' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'status', N'Status');

-- hierarchy_level: "Livello"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_level' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_level', N'Livello');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_level' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_level', N'Level');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_level' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_level', N'Ebene');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_level' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_level', N'Nivel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_level' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_level', N'Nivå');

-- type: "Tipo"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'type' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'type', N'Tipo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'type' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'type', N'Type');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'type' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'type', N'Typ');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'type' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'type', N'Tip');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'type' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'type', N'Typ');

-- ============================================
-- ERROR MESSAGES
-- ============================================

-- error_title: "Errore"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'error_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'error_title', N'Errore');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'error_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'error_title', N'Error');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'error_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'error_title', N'Fehler');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'error_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'error_title', N'Eroare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'error_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'error_title', N'Fel');

-- hierarchy_error_save: "Impossibile salvare:\n{error}"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_save' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_error_save', N'Impossibile salvare:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_save' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_error_save', N'Unable to save:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_save' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_error_save', N'Speichern nicht möglich:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_save' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_error_save', N'Imposibil de salvat:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_save' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_error_save', N'Kan inte spara:\n{error}');

-- hierarchy_error_view_children: "Impossibile visualizzare i progetti figli:\n{error}"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_view_children' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_error_view_children', N'Impossibile visualizzare i progetti figli:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_view_children' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_error_view_children', N'Unable to display child projects:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_view_children' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_error_view_children', N'Kinderprojekte können nicht angezeigt werden:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_view_children' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_error_view_children', N'Imposibil de afișat proiectele copii:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_view_children' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_error_view_children', N'Kan inte visa barnprojekt:\n{error}');

-- hierarchy_error_load: "Errore caricamento gerarchia:\n{error}"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_load' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'it', N'hierarchy_error_load', N'Errore caricamento gerarchia:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_load' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'en', N'hierarchy_error_load', N'Error loading hierarchy:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_load' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'de', N'hierarchy_error_load', N'Fehler beim Laden der Hierarchie:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_load' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'ro', N'hierarchy_error_load', N'Eroare la încărcarea ierarhiei:\n{error}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'hierarchy_error_load' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES (N'sv', N'hierarchy_error_load', N'Fel vid laddning av hierarki:\n{error}');

-- ============================================
-- VERIFICATION QUERY
-- ============================================

-- Verifica traduzioni inserite
SELECT [TranslationKey], [LanguageCode], [TranslationValue]
FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN (
    N'hierarchy_title',
    N'hierarchy_parent_label',
    N'hierarchy_children_count',
    N'hierarchy_manage_children',
    N'hierarchy_children_title',
    N'hierarchy_no_children',
    N'hierarchy_children_of',
    N'project_name',
    N'status',
    N'hierarchy_level',
    N'type',
    N'error_title',
    N'hierarchy_error_save',
    N'hierarchy_error_view_children',
    N'hierarchy_error_load'
)
ORDER BY [TranslationKey], [LanguageCode];

PRINT N'✅ Script completato! Inserite ' + CAST(@@ROWCOUNT AS NVARCHAR(10)) + N' traduzioni.';

GO
