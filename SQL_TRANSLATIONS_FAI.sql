/*
Script SQL per aggiungere le traduzioni necessarie per il modulo di Validazione Linea FAI
*/

USE [Traceability_RS];
GO

-- Traduzioni Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'line_validation_title' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('line_validation_title', 'it', 'FAI - Validazione Linea');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_header' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_header', 'it', 'Informazioni Validazione');


IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_template' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_template', 'it', 'Template FAI:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order', 'it', 'Seleziona Ordine:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_checklist' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_checklist', 'it', 'Checklist Validazione');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_save' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_save', 'it', 'Salva Validazione');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_print' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_print', 'it', 'Stampa');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_close' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_close', 'it', 'Chiudi');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order_first' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order_first', 'it', 'Seleziona prima un ordine');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_validation_type' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_validation_type', 'it', 'Seleziona almeno un tipo di validazione');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'validation_saved' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('validation_saved', 'it', 'Validazione salvata con successo');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'print_not_implemented' AND LanguageCode = 'it')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('print_not_implemented', 'it', 'Funzione di stampa da implementare');

-- Traduzioni Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_template' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_template', 'en', 'FAI Template:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'line_validation_title' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('line_validation_title', 'en', 'FAI - Line Validation');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_header' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_header', 'en', 'Validation Information');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order', 'en', 'Select Order:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_checklist' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_checklist', 'en', 'Validation Checklist');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_save' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_save', 'en', 'Save Validation');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_print' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_print', 'en', 'Print');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_close' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_close', 'en', 'Close');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order_first' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order_first', 'en', 'Please select an order first');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_validation_type' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_validation_type', 'en', 'Select at least one validation type');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'validation_saved' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('validation_saved', 'en', 'Validation saved successfully');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'print_not_implemented' AND LanguageCode = 'en')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('print_not_implemented', 'en', 'Print function to be implemented');

-- Traduzioni Romeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_template' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_template', 'ro', N'Șablon FAI:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'line_validation_title' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('line_validation_title', 'ro', N'FAI - Validare Linie');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_header' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_header', 'ro', N'Informații Validare');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order', 'ro', N'Selectează Comandă:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'fai_checklist' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('fai_checklist', 'ro', N'Listă Verificare Validare');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_save' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_save', 'ro', N'Salvează Validare');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_print' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_print', 'ro', N'Imprimă');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'btn_close' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('btn_close', 'ro', N'Închide');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_order_first' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_order_first', 'ro', N'Vă rugăm să selectați mai întâi o comandă');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'select_validation_type' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('select_validation_type', 'ro', N'Selectați cel puțin un tip de validare');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'validation_saved' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('validation_saved', 'ro', N'Validare salvată cu succes');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = 'print_not_implemented' AND LanguageCode = 'ro')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
VALUES ('print_not_implemented', 'ro', N'Funcția de imprimare urmează să fie implementată');

PRINT 'Traduzioni FAI aggiunte con successo';
GO
