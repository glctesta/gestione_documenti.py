-- =============================================
-- Add Translations for TSPL Configuration UI
-- =============================================
-- Adds translations for new TSPL and QR code configuration fields
-- Languages: it, ro, en, de, sv
-- =============================================

USE [Traceability_RS]
GO

-- =============================================
-- Menu Translations
-- =============================================

-- submenu_configurations
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_configurations' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'submenu_configurations', N'Configurazioni');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_configurations' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'submenu_configurations', N'Configurări');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_configurations' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'submenu_configurations', N'Configurations');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_configurations' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'submenu_configurations', N'Konfigurationen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_configurations' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'submenu_configurations', N'Konfigurationer');

-- submenu_label_config
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_label_config' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'submenu_label_config', N'Configurazione Etichette');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_label_config' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'submenu_label_config', N'Configurare Etichete');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_label_config' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'submenu_label_config', N'Label Configuration');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_label_config' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'submenu_label_config', N'Etikettenkonfiguration');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_label_config' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'submenu_label_config', N'Etikettkonfiguration');

-- =============================================
-- TSPL Settings Section
-- =============================================

-- tspl_settings_section
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_settings_section' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_settings_section', N'Impostazioni TSPL (Stampanti ZJIANG)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_settings_section' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_settings_section', N'Setări TSPL (Imprimante ZJIANG)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_settings_section' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_settings_section', N'TSPL Settings (ZJIANG Printers)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_settings_section' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_settings_section', N'TSPL-Einstellungen (ZJIANG-Drucker)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_settings_section' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_settings_section', N'TSPL-inställningar (ZJIANG-skrivare)');

-- tspl_info
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_info' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_info', N'Parametri per stampanti ZJIANG (203 DPI: 8 dots/mm, 1mm ≈ 8 dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_info' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_info', N'Parametri pentru imprimante ZJIANG (203 DPI: 8 puncte/mm, 1mm ≈ 8 puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_info' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_info', N'Parameters for ZJIANG printers (203 DPI: 8 dots/mm, 1mm ≈ 8 dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_info' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_info', N'Parameter für ZJIANG-Drucker (203 DPI: 8 Punkte/mm, 1mm ≈ 8 Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_info' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_info', N'Parametrar för ZJIANG-skrivare (203 DPI: 8 punkter/mm, 1mm ≈ 8 punkter)');

-- =============================================
-- TSPL Text Parameters
-- =============================================

-- tspl_x_offset
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_x_offset' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_x_offset', N'X Offset (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_x_offset' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_x_offset', N'Offset X (puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_x_offset' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_x_offset', N'X Offset (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_x_offset' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_x_offset', N'X-Versatz (Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_x_offset' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_x_offset', N'X-förskjutning (punkter)');

-- tspl_y_offset
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_y_offset' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_y_offset', N'Y Offset (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_y_offset' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_y_offset', N'Offset Y (puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_y_offset' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_y_offset', N'Y Offset (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_y_offset' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_y_offset', N'Y-Versatz (Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_y_offset' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_y_offset', N'Y-förskjutning (punkter)');

-- tspl_line_spacing
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_line_spacing' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_line_spacing', N'Spaziatura Righe (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_line_spacing' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_line_spacing', N'Spațiere Linii (puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_line_spacing' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_line_spacing', N'Line Spacing (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_line_spacing' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_line_spacing', N'Zeilenabstand (Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_line_spacing' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_line_spacing', N'Radavstånd (punkter)');

-- tspl_font_size
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_size' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_font_size', N'Dimensione Font');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_size' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_font_size', N'Dimensiune Font');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_size' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_font_size', N'Font Size');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_size' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_font_size', N'Schriftgröße');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_size' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_font_size', N'Teckenstorlek');

-- tspl_font_mul_x
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_x' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_font_mul_x', N'Moltiplicatore X');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_x' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_font_mul_x', N'Multiplicator X');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_x' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_font_mul_x', N'X Multiplier');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_x' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_font_mul_x', N'X-Multiplikator');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_x' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_font_mul_x', N'X-multiplikator');

-- tspl_font_mul_y
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_y' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'tspl_font_mul_y', N'Moltiplicatore Y');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_y' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'tspl_font_mul_y', N'Multiplicator Y');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_y' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'tspl_font_mul_y', N'Y Multiplier');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_y' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'tspl_font_mul_y', N'Y-Multiplikator');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'tspl_font_mul_y' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'tspl_font_mul_y', N'Y-multiplikator');

-- =============================================
-- QR Code Parameters
-- =============================================

-- qr_code_settings
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_code_settings' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'qr_code_settings', N'Posizione QR Code');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_code_settings' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'qr_code_settings', N'Poziție Cod QR');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_code_settings' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'qr_code_settings', N'QR Code Position');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_code_settings' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'qr_code_settings', N'QR-Code-Position');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_code_settings' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'qr_code_settings', N'QR-kodsposition');

-- qr_x_position
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_x_position' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'qr_x_position', N'QR X Position (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_x_position' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'qr_x_position', N'Poziție QR X (puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_x_position' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'qr_x_position', N'QR X Position (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_x_position' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'qr_x_position', N'QR X-Position (Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_x_position' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'qr_x_position', N'QR X-position (punkter)');

-- qr_y_position
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_y_position' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'qr_y_position', N'QR Y Position (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_y_position' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'qr_y_position', N'Poziție QR Y (puncte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_y_position' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'qr_y_position', N'QR Y Position (dots)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_y_position' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'qr_y_position', N'QR Y-Position (Punkte)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_y_position' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'qr_y_position', N'QR Y-position (punkter)');

-- qr_cell_width
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_cell_width' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'qr_cell_width', N'QR Dimensione Celle');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_cell_width' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'qr_cell_width', N'Dimensiune Celule QR');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_cell_width' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'qr_cell_width', N'QR Cell Size');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_cell_width' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'qr_cell_width', N'QR-Zellengröße');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'qr_cell_width' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'qr_cell_width', N'QR-cellstorlek');

GO

PRINT 'All TSPL and QR Code translations added successfully!';
PRINT '';
PRINT 'Translation keys added:';
PRINT '- submenu_configurations';
PRINT '- submenu_label_config';
PRINT '- tspl_settings_section';
PRINT '- tspl_info';
PRINT '- tspl_x_offset';
PRINT '- tspl_y_offset';
PRINT '- tspl_line_spacing';
PRINT '- tspl_font_size';
PRINT '- tspl_font_mul_x';
PRINT '- tspl_font_mul_y';
PRINT '- qr_code_settings';
PRINT '- qr_x_position';
PRINT '- qr_y_position';
PRINT '- qr_cell_width';
PRINT '';
PRINT 'Languages: it, ro, en, de, sv';
GO
