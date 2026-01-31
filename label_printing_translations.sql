-- Script SQL per aggiungere traduzioni per Sistema Stampa Etichette
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO (Rumeno), IT (Italiano), EN (Inglese), DE (Tedesco), SV (Svedese)

USE [Traceability_RS];
GO

-- ========================================
-- TRADUZIONI PER STAMPA ETICHETTE
-- ========================================

-- menu_materials
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'menu_materials')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'menu_materials', N'Materiale');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'menu_materials')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'menu_materials', N'Materiali');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'menu_materials')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'menu_materials', N'Materials');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'menu_materials')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'menu_materials', N'Materialien');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'menu_materials')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'menu_materials', N'Material');

-- submenu_labels
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_labels')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_labels', N'Etichete');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_labels')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_labels', N'Etichette');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_labels')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_labels', N'Labels');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_labels')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_labels', N'Etiketten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_labels')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_labels', N'Etiketter');

-- submenu_printer_settings
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_printer_settings')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_printer_settings', N'Imprimantă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_printer_settings')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_printer_settings', N'Stampante');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_printer_settings')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_printer_settings', N'Printer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_printer_settings')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_printer_settings', N'Drucker');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_printer_settings')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_printer_settings', N'Skrivare');

-- label_print_window_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'label_print_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'label_print_window_title', N'Tipărire Etichete');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'label_print_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'label_print_window_title', N'Stampa Etichette');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'label_print_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'label_print_window_title', N'Print Labels');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'label_print_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'label_print_window_title', N'Etiketten Drucken');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'label_print_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'label_print_window_title', N'Skriv ut Etiketter');

-- printer_settings_window_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'printer_settings_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'printer_settings_window_title', N'Setări Imprimantă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'printer_settings_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'printer_settings_window_title', N'Impostazioni Stampante');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'printer_settings_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'printer_settings_window_title', N'Printer Settings');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'printer_settings_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'printer_settings_window_title', N'Druckereinstellungen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'printer_settings_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'printer_settings_window_title', N'Skrivarinställningar');

-- order_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'order_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'order_label', N'Comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'order_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'order_label', N'Ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'order_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'order_label', N'Order');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'order_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'order_label', N'Auftrag');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'order_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'order_label', N'Order');

-- print_button
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'print_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'print_button', N'Tipărește');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'print_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'print_button', N'Stampa');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'print_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'print_button', N'Print');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'print_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'print_button', N'Drucken');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'print_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'print_button', N'Skriv ut');

-- cancel_button
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'cancel_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'cancel_button', N'Anulează');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'cancel_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'cancel_button', N'Annulla');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'cancel_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'cancel_button', N'Cancel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'cancel_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'cancel_button', N'Abbrechen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'cancel_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'cancel_button', N'Avbryt');

-- close_button
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'close_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'close_button', N'Închide');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'close_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'close_button', N'Chiudi');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'close_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'close_button', N'Close');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'close_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'close_button', N'Schließen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'close_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'close_button', N'Stäng');

-- select_order
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'select_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'select_order', N'Selectează o comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'select_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'select_order', N'Seleziona un ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'select_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'select_order', N'Select an order');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'select_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'select_order', N'Wählen Sie einen Auftrag');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'select_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'select_order', N'Välj en order');

-- no_orders_found
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'no_orders_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'no_orders_found', N'Nicio comandă găsită din 2025-08-01');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'no_orders_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'no_orders_found', N'Nessun ordine trovato dal 2025-08-01');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'no_orders_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'no_orders_found', N'No orders found from 2025-08-01');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'no_orders_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'no_orders_found', N'Keine Aufträge ab 2025-08-01 gefunden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'no_orders_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'no_orders_found', N'Inga ordrar hittades från 2025-08-01');

-- printer_settings_placeholder
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'printer_settings_placeholder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'printer_settings_placeholder', N'Setări imprimantă

Această funcționalitate va fi implementată ulterior.

Setările vor fi salvate într-un fișier JSON.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'printer_settings_placeholder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'printer_settings_placeholder', N'Impostazioni stampante

Questa funzionalità verrà implementata in seguito.

Le impostazioni saranno salvate in un file JSON.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'printer_settings_placeholder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'printer_settings_placeholder', N'Printer settings

This functionality will be implemented later.

Settings will be saved to a JSON file.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'printer_settings_placeholder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'printer_settings_placeholder', N'Druckereinstellungen

Diese Funktion wird später implementiert.

Die Einstellungen werden in einer JSON-Datei gespeichert.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'printer_settings_placeholder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'printer_settings_placeholder', N'Skrivarinställningar

Denna funktion kommer att implementeras senare.

Inställningarna kommer att sparas i en JSON-fil.');


GO

-- order_info
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'order_info')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'order_info', N'Informații Comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'order_info')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'order_info', N'Informazioni Ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'order_info')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'order_info', N'Order Information');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'order_info')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'order_info', N'Auftragsinformationen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'order_info')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'order_info', N'Orderinformation');

-- order_number
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'order_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'order_number', N'Număr Comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'order_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'order_number', N'Numero Ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'order_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'order_number', N'Order Number');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'order_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'order_number', N'Auftragsnummer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'order_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'order_number', N'Ordernummer');

-- product_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'product_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'product_code', N'Cod Produs');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'product_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'product_code', N'Codice Prodotto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'product_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'product_code', N'Product Code');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'product_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'product_code', N'Produktcode');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'product_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'product_code', N'Produktkod');

-- quantity
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'quantity')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'quantity', N'Cantitate');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'quantity')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'quantity', N'Quantità');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'quantity')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'quantity', N'Quantity');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'quantity')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'quantity', N'Menge');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'quantity')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'quantity', N'Kvantitet');

-- phase_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'phase_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'phase_label', N'Fază');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'phase_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'phase_label', N'Fase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'phase_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'phase_label', N'Phase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'phase_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'phase_label', N'Phase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'phase_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'phase_label', N'Fas');

-- select_phase
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'select_phase')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'select_phase', N'Selectează o fază');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'select_phase')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'select_phase', N'Seleziona una fase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'select_phase')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'select_phase', N'Select a phase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'select_phase')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'select_phase', N'Wählen Sie eine Phase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'select_phase')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'select_phase', N'Välj en fas');

-- no_data_for_order
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'no_data_for_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'no_data_for_order', N'Nicio dată găsită pentru această comandă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'no_data_for_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'no_data_for_order', N'Nessun dato trovato per questo ordine');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'no_data_for_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'no_data_for_order', N'No data found for this order');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'no_data_for_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'no_data_for_order', N'Keine Daten für diesen Auftrag gefunden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'no_data_for_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'no_data_for_order', N'Ingen data hittades för denna order');

GO

-- component_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'component_code', N'Cod Componentă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'component_code', N'Codice Componente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'component_code', N'Component Code');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'component_code', N'Komponentencode');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'component_code', N'Komponentkod');

-- enter_component_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'enter_component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'enter_component_code', N'Introduceți codul componentei');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'enter_component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'enter_component_code', N'Inserisci il codice componente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'enter_component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'enter_component_code', N'Enter component code');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'enter_component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'enter_component_code', N'Geben Sie den Komponentencode ein');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'enter_component_code')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'enter_component_code', N'Ange komponentkod');

-- component_not_found
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'component_not_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'component_not_found', N'Componentă nu a fost găsită pentru faza selectată');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'component_not_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'component_not_found', N'Componente non trovato per la fase selezionata');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'component_not_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'component_not_found', N'Component not found for selected phase');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'component_not_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'component_not_found', N'Komponente für ausgewählte Phase nicht gefunden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'component_not_found')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'component_not_found', N'Komponent hittades inte för vald fas');

GO

PRINT 'Traduzioni per sistema stampa etichette aggiunte con successo!';
PRINT 'Totale chiavi di traduzione: 21';
PRINT 'Totale lingue: 5 (RO, IT, EN, DE, SV)';
PRINT 'Totale record inseriti: 105';
