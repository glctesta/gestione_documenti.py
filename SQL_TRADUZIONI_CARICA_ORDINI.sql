-- Script SQL per aggiungere le traduzioni del modulo CARICA ORDINI
-- Data: 2026-01-19

USE [Traceability_RS];
GO

-- =========================================================================
-- TRADUZIONI FINESTRA CARICA ORDINI
-- =========================================================================

-- Titolo finestra
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'load_orders_title' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'load_orders_title', 'Carica Ordini');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'load_orders_title' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'load_orders_title', 'Load Orders');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'load_orders_title' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'load_orders_title', N'Încarcă Comenzi');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'load_orders_title' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'load_orders_title', 'Bestellungen laden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'load_orders_title' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'load_orders_title', 'Ladda beställningar');

-- Elenco ordini dinamici
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'dynamic_orders_list' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'dynamic_orders_list', 'Elenco Ordini Dinamici');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'dynamic_orders_list' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'dynamic_orders_list', 'Dynamic Orders List');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'dynamic_orders_list' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'dynamic_orders_list', N'Listă Comenzi Dinamice');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'dynamic_orders_list' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'dynamic_orders_list', 'Dynamische Bestellungsliste');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'dynamic_orders_list' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'dynamic_orders_list', 'Dynamisk beställningslista');

-- =========================================================================
-- TRADUZIONI BOTTONI
-- =========================================================================

-- Importa da Excel
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_import_excel' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_import_excel', 'Importa da Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_import_excel' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_import_excel', 'Import from Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_import_excel' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_import_excel', N'Importă din Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_import_excel' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_import_excel', 'Aus Excel importieren');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_import_excel' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_import_excel', 'Importera från Excel');

-- Aggiorna
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_refresh' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'btn_refresh', 'Aggiorna');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_refresh' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'btn_refresh', 'Refresh');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_refresh' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'btn_refresh', N'Actualizează');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_refresh' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'btn_refresh', 'Aktualisieren');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'btn_refresh' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'btn_refresh', 'Uppdatera');

-- =========================================================================
-- TRADUZIONI COLONNE TREEVIEW
-- =========================================================================

-- N. Ordine
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_so_number' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_so_number', 'N. Ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_so_number' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_so_number', 'SO Number');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_so_number' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_so_number', N'Nr. Comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_so_number' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_so_number', 'Bestellnummer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_so_number' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_so_number', 'Ordernummer');

-- Cliente
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_customer' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_customer', 'Cliente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_customer' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_customer', 'Customer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_customer' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_customer', N'Client');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_customer' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_customer', 'Kunde');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_customer' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_customer', 'Kund');

-- Cod. Prodotto
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_code' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_product_code', 'Cod. Prodotto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_code' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_product_code', 'Product Code');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_code' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_product_code', N'Cod Produs');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_code' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_product_code', 'Produktcode');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_code' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_product_code', 'Produktkod');

-- Nome Prodotto
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_name' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_product_name', 'Nome Prodotto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_name' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_product_name', 'Product Name');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_name' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_product_name', N'Nume Produs');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_name' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_product_name', 'Produktname');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_product_name' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_product_name', 'Produktnamn');

-- Data Spedizione
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_ship_date' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_ship_date', 'Data Spedizione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_ship_date' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_ship_date', 'Ship Date');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_ship_date' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_ship_date', N'Data Livrare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_ship_date' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_ship_date', 'Lieferdatum');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_ship_date' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_ship_date', 'Leveransdatum');

-- Qtà Ordinata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_order' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_qty_order', 'Qtà Ordinata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_order' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_qty_order', 'Order Qty');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_order' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_qty_order', N'Cant. Comandată');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_order' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_qty_order', 'Bestellmenge');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_order' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_qty_order', 'Beställd mängd');

-- Qtà da Spedire  
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_to_ship' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_qty_to_ship', 'Qtà da Spedire');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_to_ship' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_qty_to_ship', 'Remaining Qty');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_to_ship' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_qty_to_ship', N'Cant. de Livrat');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_to_ship' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_qty_to_ship', 'Zu liefernde Menge');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_to_ship' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_qty_to_ship', 'Återstående mängd');

-- Qtà in Stock
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_stock' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_qty_stock', 'Qtà in Stock');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_stock' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_qty_stock', 'Stock Qty');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_stock' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_qty_stock', N'Cant. în Stoc');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_stock' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_qty_stock', 'Lagermenge');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_qty_stock' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_qty_stock', 'Lagermängd');

-- Valuta
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_currency' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_currency', 'Valuta');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_currency' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_currency', 'Currency');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_currency' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_currency', N'Monedă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_currency' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_currency', 'Währung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_currency' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_currency', 'Valuta');

-- Prezzo Unitario
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_unit_price' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'col_unit_price', 'Prezzo Unit.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_unit_price' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'col_unit_price', 'Unit Price');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_unit_price' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'col_unit_price', N'Preț Unitar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_unit_price' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'col_unit_price', 'Stückpreis');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'col_unit_price' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'col_unit_price', 'Enhetspris');

-- =========================================================================
-- TRADUZIONI MESSAGGI
-- =========================================================================

-- Ordini caricati
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'orders_loaded' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'orders_loaded', 'ordini caricati');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'orders_loaded' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'orders_loaded', 'orders loaded');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'orders_loaded' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'orders_loaded', N'comenzi încărcate');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'orders_loaded' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'orders_loaded', 'Bestellungen geladen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'orders_loaded' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'orders_loaded', 'beställningar laddade');

-- Seleziona file Excel
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'select_excel_file' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'select_excel_file', 'Seleziona file Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'select_excel_file' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'select_excel_file', 'Select Excel file');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'select_excel_file' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'select_excel_file', N'Selectează fișier Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'select_excel_file' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'select_excel_file', 'Excel-Datei auswählen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'select_excel_file' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'select_excel_file', 'Välj Excel-fil');

-- Conferma importazione
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'confirm_import', 'Conferma Importazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'confirm_import', 'Confirm Import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'confirm_import', N'Confirmă Import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'confirm_import', 'Import bestätigen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'confirm_import', 'Bekräfta import');

-- Importare X righe
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import_rows' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'confirm_import_rows', 'Importare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import_rows' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'confirm_import_rows', 'Import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import_rows' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'confirm_import_rows', N'Importă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import_rows' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'confirm_import_rows', 'Importieren');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_import_rows' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'confirm_import_rows', 'Importera');

-- righe
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'rows' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'rows', 'righe');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'rows' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'rows', 'rows');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'rows' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'rows', N'rânduri');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'rows' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'rows', 'Zeilen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'rows' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'rows', 'rader');

-- Importazione in corso
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'importing' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'importing', 'Importazione in corso...');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'importing' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'importing', 'Importing...');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'importing' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'importing', N'Import în curs...');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'importing' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'importing', 'Importiere...');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'importing' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'importing', 'Importerar...');

-- Importazione completata
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_completed' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'import_completed', 'Importazione completata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_completed' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'import_completed', 'Import completed');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_completed' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'import_completed', N'Import finalizat');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_completed' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'import_completed', 'Import abgeschlossen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_completed' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'import_completed', 'Import klar');

-- Inseriti
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'inserted' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'inserted', 'Inseriti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'inserted' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'inserted', 'Inserted');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'inserted' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'inserted', N'Inserate');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'inserted' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'inserted', 'Eingefügt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'inserted' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'inserted', 'Insatta');

-- Aggiornati
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'updated' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'updated', 'Aggiornati');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'updated' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'updated', 'Updated');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'updated' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'updated', N'Actualizate');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'updated' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'updated', 'Aktualisiert');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'updated' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'updated', 'Uppdaterade');

-- Errori
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'errors' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'errors', 'Errori');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'errors' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'errors', 'Errors');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'errors' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'errors', N'Erori');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'errors' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'errors', 'Fehler');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'errors' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'errors', 'Fel');

-- Altri messaggi comuni
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_data_in_excel' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'no_data_in_excel', 'Nessun dato trovato nel file Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_data_in_excel' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'no_data_in_excel', 'No data found in Excel file');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_data_in_excel' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'no_data_in_excel', N'Nu s-au găsit date în fișierul Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_data_in_excel' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'no_data_in_excel', 'Keine Daten in Excel-Datei gefunden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_data_in_excel' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'no_data_in_excel', 'Inga data hittades i Excel-filen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_result' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'import_result', 'Risultato Importazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_result' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'import_result', 'Import Result');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_result' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'import_result', N'Rezultat Import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_result' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'import_result', 'Import-Ergebnis');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'import_result' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'import_result', 'Importresultat');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'see_log_for_details' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'see_log_for_details', 'Vedere il log per i dettagli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'see_log_for_details' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'see_log_for_details', 'See log for details');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'see_log_for_details' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'see_log_for_details', N'Vezi jurnalul pentru detalii');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'see_log_for_details' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'see_log_for_details', 'Siehe Log für Details');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'see_log_for_details' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'see_log_for_details', 'Se logg för detaljer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_loading_orders' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'error_loading_orders', 'Errore caricamento ordini');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_loading_orders' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'error_loading_orders', 'Error loading orders');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_loading_orders' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'error_loading_orders', N'Eroare încărcare comenzi');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_loading_orders' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'error_loading_orders', 'Fehler beim Laden der Bestellungen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_loading_orders' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'error_loading_orders', 'Fel vid laddning av beställningar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_importing_excel' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'error_importing_excel', 'Errore importazione Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_importing_excel' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'error_importing_excel', 'Error importing Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_importing_excel' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'error_importing_excel', N'Eroare import Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_importing_excel' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'error_importing_excel', 'Fehler beim Excel-Import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_importing_excel' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'error_importing_excel', 'Fel vid Excel-import');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_opening_window' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'error_opening_window', 'Errore apertura finestra');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_opening_window' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'error_opening_window', 'Error opening window');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_opening_window' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'error_opening_window', N'Eroare deschidere fereastră');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_opening_window' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'error_opening_window', 'Fehler beim Öffnen des Fensters');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_opening_window' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'error_opening_window', 'Fel vid öppning av fönster');

GO

PRINT 'Traduzioni modulo Carica Ordini aggiunte con successo!';
PRINT '';
PRINT 'Totale traduzioni aggiunte: ~40 chiavi x 5 lingue = ~200 traduzioni';
PRINT 'Lingue: IT, EN, RO, DE, SV';
PRINT 'Prefisso N applicato a tutte le stringhe rumene';
