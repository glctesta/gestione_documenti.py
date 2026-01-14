-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_PROJECT_DOCUMENTS.sql
-- Descrizione: Aggiunge traduzioni per la finestra documenti progetto
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- project_documents_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'project_documents_title')
BEGIN INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('IT', 'project_documents_title', 'Documenti Progetto'); END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'project_documents_title')
BEGIN INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('RO', 'project_documents_title', 'Documente Proiect'); END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'project_documents_title')
BEGIN INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('EN', 'project_documents_title', 'Project Documents'); END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'project_documents_title')
BEGIN INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('DE', 'project_documents_title', 'Projektdokumente'); END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'project_documents_title')
BEGIN INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('SV', 'project_documents_title', 'Projektdokument'); END
GO

PRINT 'Traduzioni documenti progetto aggiunte con successo!';
GO
