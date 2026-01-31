-- =============================================
-- Label Configuration Translation Keys
-- =============================================
-- Description: Adds translation keys for the Label Configuration window
--              in all supported languages (IT, RO, EN, DE, SV)
-- =============================================

USE [Traceability_RS]
GO

-- Label Configuration Window Title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'label_config_window_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'label_config_window_title', N'it', N'Configurazione Etichetta'),
        (N'label_config_window_title', N'en', N'Label Configuration'),
        (N'label_config_window_title', N'ro', N'Configurare Etichetă'),
        (N'label_config_window_title', N'de', N'Etikettenkonfiguration'),
        (N'label_config_window_title', N'sv', N'Etikettkonfiguration');
    PRINT 'Added translation: label_config_window_title';
END

-- Label Dimensions Section
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'label_dimensions_section')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'label_dimensions_section', N'it', N'Dimensioni Etichetta'),
        (N'label_dimensions_section', N'en', N'Label Dimensions'),
        (N'label_dimensions_section', N'ro', N'Dimensiuni Etichetă'),
        (N'label_dimensions_section', N'de', N'Etikettenabmessungen'),
        (N'label_dimensions_section', N'sv', N'Etikettstorlek');
    PRINT 'Added translation: label_dimensions_section';
END

-- Label Width
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'label_width')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'label_width', N'it', N'Larghezza (cm)'),
        (N'label_width', N'en', N'Width (cm)'),
        (N'label_width', N'ro', N'Lățime (cm)'),
        (N'label_width', N'de', N'Breite (cm)'),
        (N'label_width', N'sv', N'Bredd (cm)');
    PRINT 'Added translation: label_width';
END

-- Label Height
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'label_height')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'label_height', N'it', N'Altezza (cm)'),
        (N'label_height', N'en', N'Height (cm)'),
        (N'label_height', N'ro', N'Înălțime (cm)'),
        (N'label_height', N'de', N'Höhe (cm)'),
        (N'label_height', N'sv', N'Höjd (cm)');
    PRINT 'Added translation: label_height';
END

-- Fields to Print Section
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'fields_to_print_section')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'fields_to_print_section', N'it', N'Campi da Stampare'),
        (N'fields_to_print_section', N'en', N'Fields to Print'),
        (N'fields_to_print_section', N'ro', N'Câmpuri de Tipărit'),
        (N'fields_to_print_section', N'de', N'Zu druckende Felder'),
        (N'fields_to_print_section', N'sv', N'Fält att skriva ut');
    PRINT 'Added translation: fields_to_print_section';
END

-- Field Name
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'field_name')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'field_name', N'it', N'Campo'),
        (N'field_name', N'en', N'Field'),
        (N'field_name', N'ro', N'Câmp'),
        (N'field_name', N'de', N'Feld'),
        (N'field_name', N'sv', N'Fält');
    PRINT 'Added translation: field_name';
END

-- Print Field
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'print_field')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'print_field', N'it', N'Stampa'),
        (N'print_field', N'en', N'Print'),
        (N'print_field', N'ro', N'Tipărește'),
        (N'print_field', N'de', N'Drucken'),
        (N'print_field', N'sv', N'Skriv ut');
    PRINT 'Added translation: print_field';
END

-- Field Position
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'field_position')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'field_position', N'it', N'Posizione'),
        (N'field_position', N'en', N'Position'),
        (N'field_position', N'ro', N'Poziție'),
        (N'field_position', N'de', N'Position'),
        (N'field_position', N'sv', N'Position');
    PRINT 'Added translation: field_position';
END

-- Print Order Number
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'print_order_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'print_order_number', N'it', N'Numero Ordine'),
        (N'print_order_number', N'en', N'Order Number'),
        (N'print_order_number', N'ro', N'Număr Comandă'),
        (N'print_order_number', N'de', N'Auftragsnummer'),
        (N'print_order_number', N'sv', N'Ordernummer');
    PRINT 'Added translation: print_order_number';
END

-- Print Material Code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'print_material_code')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'print_material_code', N'it', N'Codice Materiale'),
        (N'print_material_code', N'en', N'Material Code'),
        (N'print_material_code', N'ro', N'Cod Material'),
        (N'print_material_code', N'de', N'Materialcode'),
        (N'print_material_code', N'sv', N'Materialkod');
    PRINT 'Added translation: print_material_code';
END

-- Print Component Quantity
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'print_component_qty')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'print_component_qty', N'it', N'Quantità Componenti'),
        (N'print_component_qty', N'en', N'Component Quantity'),
        (N'print_component_qty', N'ro', N'Cantitate Componente'),
        (N'print_component_qty', N'de', N'Komponentenmenge'),
        (N'print_component_qty', N'sv', N'Komponentkvantitet');
    PRINT 'Added translation: print_component_qty';
END

-- Print References
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'print_references')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'print_references', N'it', N'Riferimenti Scheda'),
        (N'print_references', N'en', N'Board References'),
        (N'print_references', N'ro', N'Referințe Placă'),
        (N'print_references', N'de', N'Platinen-Referenzen'),
        (N'print_references', N'sv', N'Kortreferenser');
    PRINT 'Added translation: print_references';
END

-- Position Info
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'position_info')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'position_info', N'it', N'La posizione determina l''ordine di stampa (1=primo, 4=ultimo)'),
        (N'position_info', N'en', N'Position determines print order (1=first, 4=last)'),
        (N'position_info', N'ro', N'Poziția determină ordinea de tipărire (1=primul, 4=ultimul)'),
        (N'position_info', N'de', N'Position bestimmt Druckreihenfolge (1=zuerst, 4=zuletzt)'),
        (N'position_info', N'sv', N'Position bestämmer utskriftsordning (1=först, 4=sist)');
    PRINT 'Added translation: position_info';
END

-- Invalid Dimensions
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'invalid_dimensions')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'invalid_dimensions', N'it', N'Le dimensioni devono essere maggiori di zero'),
        (N'invalid_dimensions', N'en', N'Dimensions must be greater than zero'),
        (N'invalid_dimensions', N'ro', N'Dimensiunile trebuie să fie mai mari decât zero'),
        (N'invalid_dimensions', N'de', N'Abmessungen müssen größer als Null sein'),
        (N'invalid_dimensions', N'sv', N'Dimensioner måste vara större än noll');
    PRINT 'Added translation: invalid_dimensions';
END

-- Select At Least One Field
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'select_at_least_one_field')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (TranslationKey, LanguageCode, TranslationValue)
    VALUES 
        (N'select_at_least_one_field', N'it', N'Seleziona almeno un campo da stampare'),
        (N'select_at_least_one_field', N'en', N'Select at least one field to print'),
        (N'select_at_least_one_field', N'ro', N'Selectați cel puțin un câmp de tipărit'),
        (N'select_at_least_one_field', N'de', N'Wählen Sie mindestens ein zu druckendes Feld'),
        (N'select_at_least_one_field', N'sv', N'Välj minst ett fält att skriva ut');
    PRINT 'Added translation: select_at_least_one_field';
END

PRINT 'All label configuration translation keys added successfully!';
GO
