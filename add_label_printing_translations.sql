-- =============================================
-- Script SQL per aggiungere le traduzioni
-- Modulo: Stampa Etichette (Label Printing)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- =============================================

USE [Traceability_RS];
GO

-- =============================================
-- 1. components_count_label (Componenti disponibili)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'components_count_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'components_count_label', N'it', N'Componenti disponibili');
    PRINT 'Aggiunta traduzione IT per components_count_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'components_count_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'components_count_label', N'en', N'Available components');
    PRINT 'Aggiunta traduzione EN per components_count_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'components_count_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'components_count_label', N'ro', N'Componente disponibile');
    PRINT 'Aggiunta traduzione RO per components_count_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'components_count_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'components_count_label', N'de', N'Verfügbare Komponenten');
    PRINT 'Aggiunta traduzione DE per components_count_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'components_count_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'components_count_label', N'sv', N'Tillgängliga komponenter');
    PRINT 'Aggiunta traduzione SV per components_count_label';
END

-- =============================================
-- 2. order_info (Informazioni Ordine)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'order_info' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'order_info', N'it', N'Informazioni Ordine');
    PRINT 'Aggiunta traduzione IT per order_info';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'order_info' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'order_info', N'en', N'Order Information');
    PRINT 'Aggiunta traduzione EN per order_info';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'order_info' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'order_info', N'ro', N'Informații Comandă');
    PRINT 'Aggiunta traduzione RO per order_info';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'order_info' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'order_info', N'de', N'Bestellinformationen');
    PRINT 'Aggiunta traduzione DE per order_info';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'order_info' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'order_info', N'sv', N'Orderinformation');
    PRINT 'Aggiunta traduzione SV per order_info';
END

-- =============================================
-- 3. enter_component_code (Inserisci il codice componente)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_component_code' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'enter_component_code', N'it', N'Inserisci il codice componente');
    PRINT 'Aggiunta traduzione IT per enter_component_code';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_component_code' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'enter_component_code', N'en', N'Enter the component code');
    PRINT 'Aggiunta traduzione EN per enter_component_code';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_component_code' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'enter_component_code', N'ro', N'Introduceți codul componentei');
    PRINT 'Aggiunta traduzione RO per enter_component_code';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_component_code' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'enter_component_code', N'de', N'Geben Sie den Komponentencode ein');
    PRINT 'Aggiunta traduzione DE per enter_component_code';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'enter_component_code' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'enter_component_code', N'sv', N'Ange komponentkoden');
    PRINT 'Aggiunta traduzione SV per enter_component_code';
END

-- =============================================
-- Riepilogo
-- =============================================

PRINT '';
PRINT '=============================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni aggiunte per:';
PRINT '  - components_count_label';
PRINT '  - order_info';
PRINT '  - enter_component_code';
PRINT 'Lingue: IT, EN, RO, DE, SV';
PRINT '=============================================';

GO
