-- Script SQL per le traduzioni del modulo calibrazioni
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-09-16
-- Chiavi: calibration_search_hint, calib_docs_label, calib_add_pdf,
--         calib_remove_selected, calib_no_documents, calib_open_document

USE [Traceability_RS];
GO

-- ============================================================================
-- calibration_search_hint
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calibration_search_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calibration_search_hint', N'Ricerca l''attrezzatura per aggiungere le informazioni di calibrazione.');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calibration_search_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calibration_search_hint', N'Search for the equipment to add calibration information.');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calibration_search_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calibration_search_hint', N'Căutați echipamentul pentru a adăuga informațiile de calibrare.');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calibration_search_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calibration_search_hint', N'Gerät suchen, um Kalibrierungsinformationen hinzuzufügen.');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calibration_search_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calibration_search_hint', N'Sök utrustningen för att lägga till kalibreringsinformation.');
END

-- ============================================================================
-- calib_docs_label
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calib_docs_label')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calib_docs_label', N'Documenti allegati:');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calib_docs_label')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calib_docs_label', N'Attached documents:');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calib_docs_label')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calib_docs_label', N'Documente atașate:');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calib_docs_label')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calib_docs_label', N'Angehängte Dokumente:');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calib_docs_label')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calib_docs_label', N'Bifogade dokument:');
END

-- ============================================================================
-- calib_add_pdf
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calib_add_pdf')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calib_add_pdf', N'Aggiungi PDF');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calib_add_pdf')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calib_add_pdf', N'Add PDF');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calib_add_pdf')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calib_add_pdf', N'Adaugă PDF');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calib_add_pdf')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calib_add_pdf', N'PDF hinzufügen');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calib_add_pdf')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calib_add_pdf', N'Lägg till PDF');
END

-- ============================================================================
-- calib_remove_selected
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calib_remove_selected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calib_remove_selected', N'Rimuovi selezionato');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calib_remove_selected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calib_remove_selected', N'Remove selected');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calib_remove_selected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calib_remove_selected', N'Elimină selecția');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calib_remove_selected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calib_remove_selected', N'Ausgewählte entfernen');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calib_remove_selected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calib_remove_selected', N'Ta bort vald');
END

-- ============================================================================
-- calib_no_documents
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calib_no_documents')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calib_no_documents', N'Nessun documento allegato');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calib_no_documents')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calib_no_documents', N'No attached documents');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calib_no_documents')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calib_no_documents', N'Nicio document atașat');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calib_no_documents')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calib_no_documents', N'Keine Dokumente angehängt');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calib_no_documents')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calib_no_documents', N'Inga bifogade dokument');
END

-- ============================================================================
-- calib_open_document
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'calib_open_document')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'calib_open_document', N'Apri documento');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'calib_open_document')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'calib_open_document', N'Open document');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'calib_open_document')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'calib_open_document', N'Deschide documentul');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'calib_open_document')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'calib_open_document', N'Dokument öffnen');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'calib_open_document')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'calib_open_document', N'Öppna dokument');
END
