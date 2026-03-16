-- =============================================================
-- Traduzioni per il pannello Log Stampe (label_printing_gui.py)
-- Lingue: it, ro, en, sv, de
-- =============================================================

-- print_log_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'print_log_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'print_log_title', '📋 Log Stampe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'print_log_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'print_log_title', N'📋 Jurnal Tipărire');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'print_log_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'print_log_title', '📋 Print Log');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'print_log_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'print_log_title', '📋 Utskriftslogg');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'print_log_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'print_log_title', '📋 Druckprotokoll');

-- col_time
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'col_time', 'Ora');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'col_time', N'Oră');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'col_time', 'Time');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'col_time', 'Tid');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'col_time', 'Uhrzeit');

-- col_component
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_component')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'col_component', 'Componente');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_component')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'col_component', N'Componentă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_component')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'col_component', 'Component');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_component')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'col_component', 'Komponent');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_component')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'col_component', 'Komponente');

-- col_qty
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_qty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'col_qty', 'Qty');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_qty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'col_qty', N'Cantitate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_qty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'col_qty', 'Qty');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_qty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'col_qty', 'Antal');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_qty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'col_qty', 'Menge');
