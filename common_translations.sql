-- Script SQL per aggiungere traduzioni comuni mancanti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO (Rumeno), IT (Italiano), EN (Inglese), DE (Tedesco), SV (Svedese)

USE [Traceability_RS];
GO

-- ========================================
-- TRADUZIONI COMUNI
-- ========================================

-- equipment_type_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'equipment_type_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'equipment_type_label', N'Tip Echipament');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'equipment_type_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'equipment_type_label', N'Tipo Equipaggiamento');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'equipment_type_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'equipment_type_label', N'Equipment Type');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'equipment_type_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'equipment_type_label', N'Gerätetyp');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'equipment_type_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'equipment_type_label', N'Utrustningstyp');

-- required_fields
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'required_fields')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'required_fields', N'Câmpuri obligatorii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'required_fields')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'required_fields', N'Campi obbligatori');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'required_fields')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'required_fields', N'Required fields');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'required_fields')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'required_fields', N'Pflichtfelder');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'required_fields')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'required_fields', N'Obligatoriska fält');

-- filter_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'filter_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'filter_label', N'Filtru');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'filter_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'filter_label', N'Filtro');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'filter_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'filter_label', N'Filter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'filter_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'filter_label', N'Filter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'filter_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'filter_label', N'Filter');

-- filter_button
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'filter_button', N'Filtrează');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'filter_button', N'Filtra');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'filter_button', N'Filter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'filter_button', N'Filtern');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'filter_button', N'Filtrera');

GO

PRINT 'Traduzioni comuni aggiunte con successo!';
PRINT 'Totale chiavi di traduzione: 4';
PRINT 'Totale lingue: 5 (RO, IT, EN, DE, SV)';
PRINT 'Totale record inseriti: 20';
