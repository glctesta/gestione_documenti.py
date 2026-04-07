-- ============================================================
-- Traduzioni per Stock Value + setting email
-- Eseguire su database Traceability_RS
-- ============================================================

USE [Traceability_RS]
GO

-- ================================================================
-- SETTING EMAIL
-- ================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[settings] WHERE [atribute] = N'Sys_email_stock_value')
    INSERT INTO [dbo].[settings] ([atribute], [Value])
    VALUES (N'Sys_email_stock_value', N'gianluca.testa@vandewiele.com')
GO

-- ================================================================
-- MENU
-- ================================================================

-- menu_stock_value
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'menu_stock_value' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'menu_stock_value', N'Valore Stock')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'menu_stock_value' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'menu_stock_value', N'Stock Value')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'menu_stock_value' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'menu_stock_value', N'Valoare Stoc')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'menu_stock_value' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'menu_stock_value', N'Bestandswert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'menu_stock_value' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'menu_stock_value', N'Lagervärde')

-- valore_stock (chiave autorizzazione)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'valore_stock' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'valore_stock', N'Valore Stock')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'valore_stock' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'valore_stock', N'Stock Value')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'valore_stock' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'valore_stock', N'Valoare Stoc')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'valore_stock' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'valore_stock', N'Bestandswert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'valore_stock' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'valore_stock', N'Lagervärde')

-- ================================================================
-- LABELS FORM
-- ================================================================

-- stock_item
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_item' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_item', N'Articolo')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_item' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_item', N'Item')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_item' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_item', N'Articol')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_item' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_item', N'Artikel')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_item' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_item', N'Artikel')

-- stock_value_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_value_label' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_value_label', N'Valore')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_value_label' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_value_label', N'Value')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_value_label' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_value_label', N'Valoare')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_value_label' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_value_label', N'Wert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_value_label' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_value_label', N'Värde')

-- stock_fill_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_fill_all' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_fill_all', N'Compilare tutti gli articoli e salvare')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_fill_all' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_fill_all', N'Fill in all items and save')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_fill_all' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_fill_all', N'Completați toate articolele și salvați')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_fill_all' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_fill_all', N'Alle Artikel ausfüllen und speichern')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_fill_all' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_fill_all', N'Fyll i alla artiklar och spara')

-- stock_save_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_save_all' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_save_all', N'✅ Salva Tutto')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_save_all' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_save_all', N'✅ Save All')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_save_all' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_save_all', N'✅ Salvează Tot')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_save_all' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_save_all', N'✅ Alles speichern')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_save_all' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_save_all', N'✅ Spara allt')

-- stock_filled
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_filled' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_filled', N'compilati')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_filled' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_filled', N'filled')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_filled' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_filled', N'completate')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_filled' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_filled', N'ausgefüllt')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_filled' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_filled', N'ifyllda')

-- stock_editable
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_editable' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_editable', N'Modificabile')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_editable' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_editable', N'Editable')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_editable' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_editable', N'Editabil')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_editable' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_editable', N'Bearbeitbar')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_editable' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_editable', N'Redigerbar')

-- stock_empty
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_empty' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_empty', N'Da compilare')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_empty' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_empty', N'Empty')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_empty' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_empty', N'De completat')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_empty' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_empty', N'Leer')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_empty' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_empty', N'Tom')

-- ================================================================
-- MESSAGGI
-- ================================================================

-- stock_invalid_number
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_invalid_number' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_invalid_number', N'Numero non valido per l''articolo: {item}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_invalid_number' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_invalid_number', N'Invalid number for item: {item}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_invalid_number' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_invalid_number', N'Număr invalid pentru articolul: {item}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_invalid_number' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_invalid_number', N'Ungültige Zahl für Artikel: {item}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_invalid_number' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_invalid_number', N'Ogiltigt nummer för artikel: {item}')

-- stock_missing_items
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_missing_items' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_missing_items', N'Compilare tutti gli articoli. Mancanti: {items}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_missing_items' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_missing_items', N'Please fill in all items. Missing: {items}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_missing_items' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_missing_items', N'Completați toate articolele. Lipsă: {items}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_missing_items' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_missing_items', N'Bitte alle Artikel ausfüllen. Fehlend: {items}')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_missing_items' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_missing_items', N'Fyll i alla artiklar. Saknas: {items}')

-- stock_confirm_save
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_confirm_save' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_confirm_save', N'Salvare i valori per {count} articoli?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_confirm_save' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_confirm_save', N'Save values for {count} items?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_confirm_save' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_confirm_save', N'Salvați valorile pentru {count} articole?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_confirm_save' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_confirm_save', N'Werte für {count} Artikel speichern?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_confirm_save' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_confirm_save', N'Spara värden för {count} artiklar?')

-- stock_select_date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_select_date' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_select_date', N'Data')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_select_date' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_select_date', N'Date')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_select_date' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_select_date', N'Dată')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_select_date' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_select_date', N'Datum')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_select_date' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_select_date', N'Datum')

-- stock_today
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_today' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'stock_today', N'📌 Oggi')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_today' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'stock_today', N'📌 Today')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_today' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'stock_today', N'📌 Astăzi')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_today' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'stock_today', N'📌 Heute')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'stock_today' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'stock_today', N'📌 Idag')

GO

PRINT 'Traduzioni per Stock Value aggiunte con successo!'
