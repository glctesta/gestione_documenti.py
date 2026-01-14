-- =====================================================
-- Script traduzioni per Miglioramenti Form Reclami
-- Data: 2026-01-12
-- Descrizione: Aggiunge traduzioni per:
--              - Filtro LabelCode
--              - Modifica testata salvata
-- Lingue: IT, RO, EN, DE, SV
-- =====================================================

USE [Traceability_RS]
GO

-- ========== ITALIANO ==========

-- Filtro LabelCode
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'lbl_filter_labelcode')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'lbl_filter_labelcode', 'Filtra per Label Code:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_clear_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_clear_filter', 'X');

-- Modifica testata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_edit_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_edit_header', 'Modifica Testata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_update_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_update_header', 'Aggiorna Testata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'msg_header_updated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'msg_header_updated', 'Testata aggiornata con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'err_update_failed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'err_update_failed', 'Errore nell''aggiornamento della testata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'err_update_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'err_update_error', 'Errore durante l''aggiornamento');

-- ========== RUMENO (con N per caratteri speciali Unicode) ==========

-- Filtro LabelCode
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'lbl_filter_labelcode')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'lbl_filter_labelcode', N'Filtrează după Label Code:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_clear_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_clear_filter', 'X');

-- Modifica testata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_edit_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_edit_header', N'Modifică Antet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_update_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_update_header', N'Actualizează Antet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'msg_header_updated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'msg_header_updated', N'Antet actualizat cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'err_update_failed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'err_update_failed', N'Eroare la actualizarea antetului');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'err_update_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'err_update_error', N'Eroare în timpul actualizării');

-- ========== INGLESE ==========

-- Filtro LabelCode
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'lbl_filter_labelcode')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'lbl_filter_labelcode', 'Filter by Label Code:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_clear_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_clear_filter', 'X');

-- Modifica testata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_edit_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_edit_header', 'Edit Header');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_update_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_update_header', 'Update Header');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'msg_header_updated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'msg_header_updated', 'Header updated successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'err_update_failed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'err_update_failed', 'Error updating header');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'err_update_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'err_update_error', 'Error during update');

-- ========== TEDESCO ==========

-- Filtro LabelCode
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'lbl_filter_labelcode')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'lbl_filter_labelcode', 'Nach Label Code filtern:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'btn_clear_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_clear_filter', 'X');

-- Modifica testata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'btn_edit_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_edit_header', 'Kopfzeile bearbeiten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'btn_update_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_update_header', 'Kopfzeile aktualisieren');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'msg_header_updated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'msg_header_updated', 'Kopfzeile erfolgreich aktualisiert');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'err_update_failed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'err_update_failed', 'Fehler beim Aktualisieren der Kopfzeile');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'err_update_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'err_update_error', 'Fehler während der Aktualisierung');

-- ========== SVEDESE ==========

-- Filtro LabelCode
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'lbl_filter_labelcode')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'lbl_filter_labelcode', 'Filtrera efter Label Code:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'btn_clear_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_clear_filter', 'X');

-- Modifica testata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'btn_edit_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_edit_header', 'Redigera rubrik');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'btn_update_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_update_header', 'Uppdatera rubrik');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'msg_header_updated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'msg_header_updated', 'Rubrik uppdaterad framgångsrikt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'err_update_failed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'err_update_failed', 'Fel vid uppdatering av rubrik');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'err_update_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'err_update_error', 'Fel under uppdatering');

GO

PRINT '✅ Traduzioni per miglioramenti form reclami aggiunte con successo!';
PRINT '   - Lingue supportate: IT, RO, EN, DE, SV';
PRINT '   - Funzionalità: Filtro LabelCode + Modifica Testata';
PRINT '   - Totale chiavi: 7 per lingua (35 record totali)';
GO
