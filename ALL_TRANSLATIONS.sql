-- =============================================
-- Script COMPLETO per tutte le traduzioni
-- Sistema Configurazione Stampanti + Shipping Rules
-- Lingue: ro, it, en, de, sv
-- =============================================

-- ========================================
-- SEZIONE 1: PRINTER SETTINGS TRANSLATIONS
-- ========================================

-- Printer Settings Window Title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_settings_window_title' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'printer_settings_window_title', N'Impostazioni Stampante');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_settings_window_title' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'printer_settings_window_title', N'Printer Settings');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_settings_window_title' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'printer_settings_window_title', N'Setări Imprimantă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_settings_window_title' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'printer_settings_window_title', N'Druckereinstellungen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_settings_window_title' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'printer_settings_window_title', N'Skrivarinställningar');

-- Select Printer Type
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_printer_type' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'select_printer_type', N'Seleziona tipo di connessione stampante:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_printer_type' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'select_printer_type', N'Select printer connection type:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_printer_type' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'select_printer_type', N'Selectați tipul de conexiune imprimantă:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_printer_type' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'select_printer_type', N'Druckerverbindungstyp auswählen:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_printer_type' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'select_printer_type', N'Välj skrivaranslutningstyp:');

-- Default Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'default_printer', N'🖨️ Stampante di Default Windows');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'default_printer', N'🖨️ Windows Default Printer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'default_printer', N'🖨️ Imprimanta Implicită Windows');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'default_printer', N'🖨️ Windows-Standarddrucker');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'default_printer', N'🖨️ Windows Standardskrivare');

-- USB Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'usb_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'usb_printer', N'🔌 Stampante USB (Zebra/Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'usb_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'usb_printer', N'🔌 USB Printer (Zebra/Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'usb_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'usb_printer', N'🔌 Imprimantă USB (Zebra/Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'usb_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'usb_printer', N'🔌 USB-Drucker (Zebra/Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'usb_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'usb_printer', N'🔌 USB-skrivare (Zebra/Brother)');

-- IP Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'ip_printer', N'🌐 Stampante IP/Network');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'ip_printer', N'🌐 IP/Network Printer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'ip_printer', N'🌐 Imprimantă IP/Rețea');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'ip_printer', N'🌐 IP/Netzwerkdrucker');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'ip_printer', N'🌐 IP/Nätverksskrivare');

-- Test Connection
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_connection' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'test_connection', N'Test Connessione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_connection' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'test_connection', N'Test Connection');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_connection' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'test_connection', N'Test Conexiune');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_connection' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'test_connection', N'Verbindung Testen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_connection' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'test_connection', N'Testa Anslutning');

-- ========================================
-- SEZIONE 2: SHIPPING RULES COLUMNS
-- ========================================

-- Prod Order
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_prod_order', N'Ordine Prod.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_prod_order', N'Prod. Order');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_prod_order', N'Comandă Prod.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_prod_order', N'Prod. Auftrag');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_prod_order', N'Prod. Order');

-- Requested On
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_requested_on', N'Richiesto Il');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_requested_on', N'Requested On');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_requested_on', N'Solicitat Pe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_requested_on', N'Angefordert Am');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_requested_on', N'Begärd Den');

-- Request Date To Ship
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_request_date_to_ship', N'Data Spedizione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_request_date_to_ship', N'Ship Date');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_request_date_to_ship', N'Data Expediere');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_request_date_to_ship', N'Versanddatum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_request_date_to_ship', N'Leveransdatum');

-- Request Qty
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_request_qty', N'Qtà Richiesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_request_qty', N'Request Qty');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_request_qty', N'Cant. Solicitată');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_request_qty', N'Angeforderte Menge');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_request_qty', N'Begärd Kvantitet');

-- Remain Over PO
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_remain_over_po', N'Rim. su PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_remain_over_po', N'Remain on PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_remain_over_po', N'Rămas pe PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_remain_over_po', N'Verbleibend auf PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_remain_over_po', N'Kvar på PO');

-- Remain Over Request
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_remain_over_request', N'Rim. su Richiesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_remain_over_request', N'Remain on Request');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_remain_over_request', N'Rămas pe Solicitare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_remain_over_request', N'Verbleibend auf Anfrage');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_remain_over_request', N'Kvar på Begäran');

-- ========================================
-- SEZIONE 3: EXCEL EXPORT PROMPTS
-- ========================================

-- Open File Question
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'open_file_question' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'open_file_question', N'Vuoi aprire il file?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'open_file_question' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'open_file_question', N'Do you want to open the file?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'open_file_question' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'open_file_question', N'Doriți să deschideți fișierul?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'open_file_question' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'open_file_question', N'Möchten Sie die Datei öffnen?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'open_file_question' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'open_file_question', N'Vill du öppna filen?');

PRINT '✅ TUTTE LE TRADUZIONI AGGIUNTE CON SUCCESSO!';
PRINT '   - Printer Settings: 6 chiavi x 5 lingue = 30 traduzioni';
PRINT '   - Shipping Rules Columns: 6 chiavi x 5 lingue = 30 traduzioni';
PRINT '   - Excel Export Prompts: 1 chiave x 5 lingue = 5 traduzioni';
PRINT '   - TOTALE: 65 traduzioni';
