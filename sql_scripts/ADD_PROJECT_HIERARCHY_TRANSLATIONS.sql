-- =============================================
-- Script: ADD_PROJECT_HIERARCHY_TRANSLATIONS.sql
-- Descrizione: Aggiungi traduzioni per UI gerarchia progetti NPI
-- Autore: Gianluca Testa
-- Data: 2026-01-21
-- Versione: 1.0
-- =============================================

USE [Traceability_RS]
GO

PRINT '=========================================='
PRINT 'INIZIO: Aggiunta traduzioni gerarchia progetti'
PRINT '=========================================='
PRINT ''

-- =============================================
-- ETICHETTE SEZIONE GERARCHIA
-- =============================================

-- Titolo frame gerarchia
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_frame_title' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'hierarchy_frame_title', '🔗 Gerarchia Progetti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_frame_title' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'hierarchy_frame_title', N'🔗 Ierarhia Proiectelor');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_frame_title' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'hierarchy_frame_title', '🔗 Project Hierarchy');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_frame_title' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'hierarchy_frame_title', '🔗 Projekthierarchie');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_frame_title' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'hierarchy_frame_title', '🔗 Projekthierarki');

-- Label "Progetto Padre"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'parent_project_label' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'parent_project_label', 'Progetto Padre:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'parent_project_label' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'parent_project_label', N'Proiect Părinte:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'parent_project_label' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'parent_project_label', 'Parent Project:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'parent_project_label' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'parent_project_label', 'Übergeordnetes Projekt:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'parent_project_label' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'parent_project_label', 'Föräldraprojekt:');

-- Opzione "(Nessuno - Progetto Root)"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_parent_option' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'no_parent_option', '(Nessuno - Progetto Root)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_parent_option' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'no_parent_option', N'(Nici unul - Proiect Rădăcină)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_parent_option' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'no_parent_option', '(None - Root Project)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_parent_option' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'no_parent_option', '(Keins - Root-Projekt)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_parent_option' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'no_parent_option', '(Ingen - Rotprojekt)');

-- Label "Progetto Root (nessun padre)"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'root_project_status' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'root_project_status', '✅ Progetto Root (nessun padre)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'root_project_status' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'root_project_status', N'✅ Proiect Rădăcină (fără părinte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'root_project_status' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'root_project_status', '✅ Root Project (no parent)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'root_project_status' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'root_project_status', '✅ Root-Projekt (kein Elternteil)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'root_project_status' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'root_project_status', '✅ Rotprojekt (ingen förälder)');

-- Label "Nessun progetto figlio"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_child_projects' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'no_child_projects', 'Nessun progetto figlio');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_child_projects' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'no_child_projects', N'Niciun proiect copil');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_child_projects' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'no_child_projects', 'No child projects');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_child_projects' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'no_child_projects', 'Keine Unterprojekte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_child_projects' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'no_child_projects', 'Inga underprojekt');

-- Pulsante "Mostra Figli"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'show_children_button' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'show_children_button', '📋 Mostra Figli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'show_children_button' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'show_children_button', N'📋 Afișează Copiii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'show_children_button' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'show_children_button', '📋 Show Children');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'show_children_button' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'show_children_button', '📋 Unterprojekte anzeigen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'show_children_button' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'show_children_button', '📋 Visa underprojekt');

-- =============================================
-- MESSAGGI E DIALOG
-- =============================================

-- Dialog "Conferma Modifica"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_title' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'confirm_parent_change_title', 'Conferma Modifica');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_title' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'confirm_parent_change_title', N'Confirmă Modificarea');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_title' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'confirm_parent_change_title', 'Confirm Change');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_title' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'confirm_parent_change_title', 'Änderung bestätigen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_title' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'confirm_parent_change_title', 'Bekräfta ändring');

-- Messaggio "Vuoi modificare il progetto padre"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_message' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'confirm_parent_change_message', 'Vuoi modificare il progetto padre a:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_message' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'confirm_parent_change_message', N'Doriți să modificați proiectul părinte la:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_message' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'confirm_parent_change_message', 'Do you want to change the parent project to:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_message' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'confirm_parent_change_message', 'Möchten Sie das übergeordnete Projekt ändern zu:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_parent_change_message' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'confirm_parent_change_message', 'Vill du ändra föräldraprojektet till:');

-- "Errore Validazione"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'validation_error_title' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'validation_error_title', 'Errore Validazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'validation_error_title' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'validation_error_title', N'Eroare de Validare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'validation_error_title' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'validation_error_title', 'Validation Error');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'validation_error_title' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'validation_error_title', 'Validierungsfehler');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'validation_error_title' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'validation_error_title', 'Valideringsfel');

-- "Gerarchia progetti aggiornata con successo!"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_updated_success' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'hierarchy_updated_success', 'Gerarchia progetti aggiornata con successo!');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_updated_success' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'hierarchy_updated_success', N'Ierarhia proiectelor a fost actualizată cu succes!');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_updated_success' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'hierarchy_updated_success', 'Project hierarchy updated successfully!');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_updated_success' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'hierarchy_updated_success', 'Projekthierarchie erfolgreich aktualisiert!');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'hierarchy_updated_success' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'hierarchy_updated_success', 'Projekthierarkin har uppdaterats!');

-- =============================================
-- DIALOG PROGETTI FIGLI
-- =============================================

-- "Progetti Figli"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'child_projects_title' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'child_projects_title', 'Progetti Figli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'child_projects_title' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'child_projects_title', N'Proiecte Copii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'child_projects_title' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'child_projects_title', 'Child Projects');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'child_projects_title' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'child_projects_title', 'Unterprojekte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'child_projects_title' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'child_projects_title', 'Underprojekt');

-- "Questo progetto non ha progetti figli."
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_children_message' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'no_children_message', 'Questo progetto non ha progetti figli.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_children_message' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'no_children_message', N'Acest proiect nu are proiecte copii.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_children_message' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'no_children_message', 'This project has no child projects.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_children_message' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'no_children_message', 'Dieses Projekt hat keine Unterprojekte.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_children_message' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'no_children_message', 'Detta projekt har inga underprojekt.');

-- =============================================
-- COLONNE TREEVIEW
-- =============================================

-- "Nome Progetto"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_project_name' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'column_project_name', 'Nome Progetto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_project_name' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'column_project_name', N'Nume Proiect');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_project_name' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'column_project_name', 'Project Name');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_project_name' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'column_project_name', 'Projektname');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_project_name' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'column_project_name', 'Projektnamn');

-- "Livello"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_level' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'column_level', 'Livello');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_level' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'column_level', N'Nivel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_level' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'column_level', 'Level');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_level' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'column_level', 'Ebene');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_level' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'column_level', 'Nivå');

-- "Tipo"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_type' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'column_type', 'Tipo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_type' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'column_type', N'Tip');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_type' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'column_type', 'Type');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_type' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'column_type', 'Typ');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'column_type' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'column_type', 'Typ');

PRINT ''
PRINT '=========================================='
PRINT '✅ TRADUZIONI GERARCHIA PROGETTI COMPLETATE!'
PRINT '=========================================='
PRINT ''
PRINT 'Traduzioni aggiunte per 5 lingue:'
PRINT '  ✅ Italiano (it)'
PRINT '  ✅ Rumeno (ro) - con prefisso N'
PRINT '  ✅ Inglese (en)'
PRINT '  ✅ Tedesco (de)'
PRINT '  ✅ Svedese (sv)'
PRINT ''
PRINT 'Chiavi tradotte:'
PRINT '  - hierarchy_frame_title'
PRINT '  - parent_project_label'
PRINT '  - no_parent_option'
PRINT '  - root_project_status'
PRINT '  - no_child_projects'
PRINT '  - show_children_button'
PRINT '  - confirm_parent_change_title'
PRINT '  - confirm_parent_change_message'
PRINT '  - validation_error_title'
PRINT '  - hierarchy_updated_success'
PRINT '  - child_projects_title'
PRINT '  - no_children_message'
PRINT '  - column_project_name'
PRINT '  - column_level'
PRINT '  - column_type'
PRINT ''

GO
