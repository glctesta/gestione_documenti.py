-- Aggiornamento traduzioni per Produzione — Ricevimento Kit (filtro date + nuovo header)

-- Header aggiornato
UPDATE [dbo].[AppTranslations] SET [TranslationValue] = N'Kit chiusi WH / verificati in attesa di ricevimento in linea'
WHERE [TranslationKey] = N'kit_prod_header' AND [LanguageCode] = N'it';
UPDATE [dbo].[AppTranslations] SET [TranslationValue] = N'WH closed / verified kits awaiting line receiving'
WHERE [TranslationKey] = N'kit_prod_header' AND [LanguageCode] = N'en';
UPDATE [dbo].[AppTranslations] SET [TranslationValue] = N'Kituri închise WH / verificate în așteptarea recepției pe linie'
WHERE [TranslationKey] = N'kit_prod_header' AND [LanguageCode] = N'ro';
UPDATE [dbo].[AppTranslations] SET [TranslationValue] = N'Vom WH geschlossene / verifizierte Kits, die auf Linienempfang warten'
WHERE [TranslationKey] = N'kit_prod_header' AND [LanguageCode] = N'de';
UPDATE [dbo].[AppTranslations] SET [TranslationValue] = N'WH-stängda / verifierade kit som väntar på mottagning vid linjen'
WHERE [TranslationKey] = N'kit_prod_header' AND [LanguageCode] = N'sv';

-- Nuova chiave: filtro date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'kit_prod_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'kit_prod_filter', N'Filtro data chiusura lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'kit_prod_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'kit_prod_filter', N'List closing date filter');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'kit_prod_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'kit_prod_filter', N'Filtru dată închidere listă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'kit_prod_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'kit_prod_filter', N'Filter Listenabschlussdatum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'kit_prod_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'kit_prod_filter', N'Filter för listans stängningsdatum');

-- Nuova chiave: reset filtro
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'kit_prod_reset_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'kit_prod_reset_filter', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'kit_prod_reset_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'kit_prod_reset_filter', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'kit_prod_reset_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'kit_prod_reset_filter', N'Resetare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'kit_prod_reset_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'kit_prod_reset_filter', N'Zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'kit_prod_reset_filter')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'kit_prod_reset_filter', N'Återställ');

PRINT 'Traduzioni kit produzione aggiornate.';
GO
