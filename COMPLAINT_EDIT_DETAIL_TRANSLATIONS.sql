-- =====================================================
-- Script traduzioni per funzionalità modifica dettagli reclamo
-- Data: 2026-01-11
-- Descrizione: Aggiunge traduzioni per i nuovi pulsanti e finestre
--              di modifica dei dettagli delle schede reclamo
-- Lingue: IT, RO, EN, DE, SV
-- =====================================================

USE [Traceability_RS]
GO

-- Elimina eventuali traduzioni esistenti per evitare duplicati
DELETE FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN (
    'title_edit_detail',
    'title_add_detail',
    'btn_edit_detail_row'
);
GO

-- Inserisci le nuove traduzioni solo se non esistono già

-- ========== ITALIANO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'title_edit_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'title_edit_detail', 'Modifica Dettaglio');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'title_add_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'title_add_detail', 'Aggiungi Dettaglio');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_edit_detail_row')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_edit_detail_row', 'Modifica Riga');

-- ========== RUMENO (con N per caratteri speciali Unicode) ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'title_edit_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'title_edit_detail', N'Modifică Detaliu');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'title_add_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'title_add_detail', N'Adaugă Detaliu');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_edit_detail_row')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_edit_detail_row', N'Modifică Rând');

-- ========== INGLESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'title_edit_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'title_edit_detail', 'Edit Detail');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'title_add_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'title_add_detail', 'Add Detail');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_edit_detail_row')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_edit_detail_row', 'Edit Row');

-- ========== TEDESCO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'title_edit_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'title_edit_detail', 'Detail bearbeiten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'title_add_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'title_add_detail', 'Detail hinzufügen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'btn_edit_detail_row')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_edit_detail_row', 'Zeile bearbeiten');

-- ========== SVEDESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'title_edit_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'title_edit_detail', 'Redigera detalj');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'title_add_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'title_add_detail', 'Lägg till detalj');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'btn_edit_detail_row')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_edit_detail_row', 'Redigera rad');

GO

PRINT '✅ Traduzioni per modifica dettagli reclamo aggiunte con successo!';
PRINT '   - Lingue supportate: IT, RO, EN, DE, SV';
PRINT '   - Script eseguito con controllo IF NOT EXISTS';
GO
