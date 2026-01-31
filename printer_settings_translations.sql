-- =============================================
-- Script per aggiungere traduzioni sistema configurazione stampanti
-- Lingue: ro, it, en, de, sv
-- =============================================

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

-- Printer Config
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_config' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'printer_config', N'Configurazione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_config' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'printer_config', N'Configuration');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_config' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'printer_config', N'Configurare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_config' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'printer_config', N'Konfiguration');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_config' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'printer_config', N'Konfiguration');

-- Current Default Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'current_default_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'current_default_printer', N'Stampante di default corrente:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'current_default_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'current_default_printer', N'Current default printer:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'current_default_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'current_default_printer', N'Imprimanta implicită curentă:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'current_default_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'current_default_printer', N'Aktueller Standarddrucker:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'current_default_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'current_default_printer', N'Nuvarande standardskrivare:');

-- Refresh
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'refresh' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'refresh', N'Aggiorna');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'refresh' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'refresh', N'Refresh');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'refresh' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'refresh', N'Actualizare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'refresh' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'refresh', N'Aktualisieren');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'refresh' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'refresh', N'Uppdatera');

-- Default Printer Info
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer_info' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'default_printer_info', N'La stampante di default di Windows verrà utilizzata per la stampa.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer_info' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'default_printer_info', N'The Windows default printer will be used for printing.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer_info' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'default_printer_info', N'Imprimanta implicită Windows va fi utilizată pentru imprimare.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer_info' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'default_printer_info', N'Der Windows-Standarddrucker wird zum Drucken verwendet.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'default_printer_info' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'default_printer_info', N'Windows standardskrivare kommer att användas för utskrift.');

-- Select USB Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_usb_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'select_usb_printer', N'Seleziona stampante USB:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_usb_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'select_usb_printer', N'Select USB printer:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_usb_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'select_usb_printer', N'Selectați imprimanta USB:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_usb_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'select_usb_printer', N'USB-Drucker auswählen:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'select_usb_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'select_usb_printer', N'Välj USB-skrivare:');

-- Detect Printers
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'detect_printers' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'detect_printers', N'Rileva Stampanti');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'detect_printers' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'detect_printers', N'Detect Printers');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'detect_printers' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'detect_printers', N'Detectare Imprimante');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'detect_printers' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'detect_printers', N'Drucker Erkennen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'detect_printers' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'detect_printers', N'Upptäck Skrivare');

-- Printer Model
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_model' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'printer_model', N'Modello:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_model' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'printer_model', N'Model:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_model' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'printer_model', N'Model:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_model' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'printer_model', N'Modell:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_model' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'printer_model', N'Modell:');

-- Printer IP
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_ip' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'printer_ip', N'Indirizzo IP:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_ip' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'printer_ip', N'IP Address:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_ip' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'printer_ip', N'Adresă IP:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_ip' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'printer_ip', N'IP-Adresse:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_ip' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'printer_ip', N'IP-adress:');

-- Printer Port
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_port' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'printer_port', N'Porta:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_port' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'printer_port', N'Port:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_port' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'printer_port', N'Port:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_port' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'printer_port', N'Port:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'printer_port' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'printer_port', N'Port:');

-- IP Printer Info
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer_info' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'ip_printer_info', N'(Porta standard: 9100 per Zebra, 9100 per Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer_info' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'ip_printer_info', N'(Standard port: 9100 for Zebra, 9100 for Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer_info' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'ip_printer_info', N'(Port standard: 9100 pentru Zebra, 9100 pentru Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer_info' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'ip_printer_info', N'(Standardport: 9100 für Zebra, 9100 für Brother)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'ip_printer_info' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'ip_printer_info', N'(Standardport: 9100 för Zebra, 9100 för Brother)');

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

-- Connection Test Success
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_success' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'connection_test_success', N'Test connessione riuscito!\n\n');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_success' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'connection_test_success', N'Connection test successful!\n\n');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_success' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'connection_test_success', N'Test conexiune reușit!\n\n');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_success' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'connection_test_success', N'Verbindungstest erfolgreich!\n\n');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_success' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'connection_test_success', N'Anslutningstestet lyckades!\n\n');

-- Connection Test Failed
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_failed' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'connection_test_failed', N'Test connessione fallito');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_failed' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'connection_test_failed', N'Connection test failed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_failed' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'connection_test_failed', N'Test conexiune eșuat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_failed' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'connection_test_failed', N'Verbindungstest fehlgeschlagen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_test_failed' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'connection_test_failed', N'Anslutningstestet misslyckades');

-- Connection Error
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_error' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'connection_error', N'Errore di connessione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_error' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'connection_error', N'Connection error');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_error' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'connection_error', N'Eroare de conexiune');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_error' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'connection_error', N'Verbindungsfehler');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'connection_error' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'connection_error', N'Anslutningsfel');

-- Config Saved
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'config_saved' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'config_saved', N'Configurazione salvata con successo!');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'config_saved' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'config_saved', N'Configuration saved successfully!');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'config_saved' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'config_saved', N'Configurare salvată cu succes!');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'config_saved' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'config_saved', N'Konfiguration erfolgreich gespeichert!');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'config_saved' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'config_saved', N'Konfigurationen sparades framgångsrikt!');

-- Save Error
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'save_error' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'save_error', N'Errore durante il salvataggio');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'save_error' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'save_error', N'Error during save');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'save_error' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'save_error', N'Eroare în timpul salvării');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'save_error' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'save_error', N'Fehler beim Speichern');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'save_error' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'save_error', N'Fel vid sparande');

-- No Default Printer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_default_printer' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'no_default_printer', N'Nessuna stampante di default');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_default_printer' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'no_default_printer', N'No default printer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_default_printer' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'no_default_printer', N'Nicio imprimantă implicită');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_default_printer' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'no_default_printer', N'Kein Standarddrucker');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_default_printer' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'no_default_printer', N'Ingen standardskrivare');

-- No Printers Found
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_printers_found' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'no_printers_found', N'Nessuna stampante rilevata sul sistema');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_printers_found' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'no_printers_found', N'No printers detected on system');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_printers_found' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'no_printers_found', N'Nicio imprimantă detectată pe sistem');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_printers_found' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'no_printers_found', N'Keine Drucker im System erkannt');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'no_printers_found' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'no_printers_found', N'Inga skrivare hittades på systemet');

-- Enter IP
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_ip' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'enter_ip', N'Inserisci l''indirizzo IP');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_ip' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'enter_ip', N'Enter IP address');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_ip' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'enter_ip', N'Introduceți adresa IP');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_ip' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'enter_ip', N'IP-Adresse eingeben');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_ip' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'enter_ip', N'Ange IP-adress');

-- Invalid Port
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'invalid_port' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'invalid_port', N'Porta non valida');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'invalid_port' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'invalid_port', N'Invalid port');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'invalid_port' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'invalid_port', N'Port invalid');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'invalid_port' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'invalid_port', N'Ungültiger Port');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'invalid_port' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'invalid_port', N'Ogiltig port');

-- Test Error
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_error' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'test_error', N'Errore durante il test');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_error' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'test_error', N'Error during test');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_error' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'test_error', N'Eroare în timpul testului');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_error' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'test_error', N'Fehler beim Test');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'test_error' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'test_error', N'Fel vid test');

PRINT 'Traduzioni per sistema configurazione stampanti aggiunte con successo!';
