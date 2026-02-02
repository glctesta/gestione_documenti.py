-- Script SQL per aggiungere le traduzioni per la gestione tipi macchine
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-02-02

USE [Traceability_RS];
GO

-- ============================================================================
-- submenu_equipment_types
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'submenu_equipment_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'submenu_equipment_types', N'Gestione Tipi Macchine');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'submenu_equipment_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'submenu_equipment_types', N'Equipment Types Management');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'submenu_equipment_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'submenu_equipment_types', N'Geräteverwaltung');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'submenu_equipment_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'submenu_equipment_types', N'Gestionarea Tipurilor de Echipamente');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'submenu_equipment_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'submenu_equipment_types', N'Hantering av Utrustningstyper');
END

-- ============================================================================
-- equipment_type
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'equipment_type', N'Tipo Equipaggiamento');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'equipment_type', N'Equipment Type');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'equipment_type', N'Gerätetyp');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'equipment_type', N'Tip Echipament');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'equipment_type', N'Utrustningstyp');
END

-- ============================================================================
-- is_test
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'is_test')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'is_test', N'Test');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'is_test')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'is_test', N'Test');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'is_test')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'is_test', N'Test');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'is_test')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'is_test', N'Test');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'is_test')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'is_test', N'Test');
END

-- ============================================================================
-- end_of_life_cycle
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'end_of_life_cycle')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'end_of_life_cycle', N'Fine Ciclo Vita');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'end_of_life_cycle')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'end_of_life_cycle', N'End of Life Cycle');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'end_of_life_cycle')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'end_of_life_cycle', N'Ende des Lebenszyklus');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'end_of_life_cycle')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'end_of_life_cycle', N'Sfârșitul Ciclului de Viață');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'end_of_life_cycle')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'end_of_life_cycle', N'Slutet av Livscykeln');
END

-- ============================================================================
-- select_item_first
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'select_item_first')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'select_item_first', N'Seleziona prima un elemento');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'select_item_first')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'select_item_first', N'Select an item first');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'select_item_first')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'select_item_first', N'Wählen Sie zuerst ein Element aus');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'select_item_first')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'select_item_first', N'Selectați mai întâi un element');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'select_item_first')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'select_item_first', N'Välj ett objekt först');
END

-- ============================================================================
-- add_equipment_type
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'add_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'add_equipment_type', N'Aggiungi Tipo');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'add_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'add_equipment_type', N'Add Type');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'add_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'add_equipment_type', N'Typ Hinzufügen');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'add_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'add_equipment_type', N'Adaugă Tip');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'add_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'add_equipment_type', N'Lägg till Typ');
END

-- ============================================================================
-- edit_equipment_type
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'edit_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'edit_equipment_type', N'Modifica Tipo');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'edit_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'edit_equipment_type', N'Edit Type');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'edit_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'edit_equipment_type', N'Typ Bearbeiten');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'edit_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'edit_equipment_type', N'Modifică Tip');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'edit_equipment_type')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'edit_equipment_type', N'Redigera Typ');
END

-- ============================================================================
-- equipment_type_required
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'equipment_type_required')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'equipment_type_required', N'Il nome del tipo è obbligatorio');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'equipment_type_required')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'equipment_type_required', N'Type name is required');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'equipment_type_required')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'equipment_type_required', N'Typname ist erforderlich');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'equipment_type_required')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'equipment_type_required', N'Numele tipului este obligatoriu');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'equipment_type_required')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'equipment_type_required', N'Typnamn krävs');
END

-- ============================================================================
-- invalid_number
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'invalid_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'invalid_number', N'Deve essere un numero intero');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'invalid_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'invalid_number', N'Must be an integer');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'invalid_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'invalid_number', N'Muss eine ganze Zahl sein');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'invalid_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'invalid_number', N'Trebuie să fie un număr întreg');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'invalid_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'invalid_number', N'Måste vara ett heltal');
END

GO

PRINT 'Traduzioni aggiunte con successo!';
PRINT 'Totale chiavi tradotte: 9';
PRINT 'Lingue: IT, EN, DE, RO, SV';
