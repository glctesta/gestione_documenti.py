-- Script SQL per aggiungere le traduzioni del menu Ordini e filtro persone NPI
-- Data: 2026-01-19

USE [Traceability_RS];
GO

-- =========================================================================
-- TRADUZIONI MENU ORDINI
-- =========================================================================

-- Menu principale "Ordini"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'menu_orders' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'menu_orders', 'Ordini');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'menu_orders' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'menu_orders', 'Orders');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'menu_orders' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'menu_orders', N'Comenzi');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'menu_orders' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'menu_orders', 'Bestellungen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'menu_orders' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'menu_orders', 'Beställningar');

-- Sottomenu "Carica Ordini"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_load_orders' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'submenu_load_orders', 'Carica Ordini');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_load_orders' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'submenu_load_orders', 'Load Orders');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_load_orders' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'submenu_load_orders', N'Încarcă Comenzi');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_load_orders' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'submenu_load_orders', 'Bestellungen laden');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_load_orders' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'submenu_load_orders', 'Ladda beställningar');

-- Sottomenu "Accoppia Ordini Produzione"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_match_production_orders' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'submenu_match_production_orders', 'Accoppia Ordini Produzione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_match_production_orders' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'submenu_match_production_orders', 'Match Production Orders');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_match_production_orders' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'submenu_match_production_orders', N'Potrivește Comenzi Producție');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_match_production_orders' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'submenu_match_production_orders', 'Produktionsaufträge zuordnen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_match_production_orders' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'submenu_match_production_orders', 'Matcha produktionsorder');

-- Sottomenu "Rapporti"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_orders_reports' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'submenu_orders_reports', 'Rapporti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_orders_reports' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'submenu_orders_reports', 'Reports');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_orders_reports' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'submenu_orders_reports', N'Rapoarte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_orders_reports' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'submenu_orders_reports', 'Berichte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_orders_reports' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'submenu_orders_reports', 'Rapporter');

-- =========================================================================
-- TRADUZIONI FILTRO PERSONE NPI
-- =========================================================================

-- Label "Assegnato a:"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'filter_owner' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'filter_owner', 'Assegnato a:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'filter_owner' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'filter_owner', 'Assigned to:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'filter_owner' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'filter_owner', N'Atribuit către:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'filter_owner' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'filter_owner', 'Zugewiesen an:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'filter_owner' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'filter_owner', 'Tilldelad till:');

-- Opzione "Tutte le persone"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'all_owners' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'all_owners', 'Tutte le persone');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'all_owners' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'all_owners', 'All people');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'all_owners' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'all_owners', N'Toate persoanele');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'all_owners' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'all_owners', 'Alle Personen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'all_owners' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'all_owners', 'Alla personer');

-- =========================================================================
-- TRADUZIONI GENERICHE (per messagebox, etc)
-- =========================================================================

-- "Funzionalità in fase di sviluppo"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'feature_coming_soon' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'feature_coming_soon', 'Funzionalità in fase di sviluppo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'feature_coming_soon' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'feature_coming_soon', 'Feature under development');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'feature_coming_soon' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'feature_coming_soon', N'Funcționalitate în dezvoltare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'feature_coming_soon' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'feature_coming_soon', 'Funktion in Entwicklung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'feature_coming_soon' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'feature_coming_soon', 'Funktion under utveckling');

-- "Informazione"
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'info' AND [LanguageCode] = 'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'info', 'Informazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'info' AND [LanguageCode] = 'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'info', 'Information');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'info' AND [LanguageCode] = 'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'info', N'Informație');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'info' AND [LanguageCode] = 'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'info', 'Information');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'info' AND [LanguageCode] = 'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'info', 'Information');

GO

PRINT 'Traduzioni menu Ordini e filtro persone NPI aggiunte con successo!';
PRINT '';
PRINT 'Riepilogo traduzioni aggiunte:';
PRINT '- menu_orders (Menu principale Ordini)';
PRINT '- submenu_load_orders (Carica Ordini)';
PRINT '- submenu_match_production_orders (Accoppia Ordini Produzione)';
PRINT '- submenu_orders_reports (Rapporti)';
PRINT '- filter_owner (Assegnato a:)';
PRINT '- all_owners (Tutte le persone)';
PRINT '- feature_coming_soon (Funzionalità in fase di sviluppo)';
PRINT '- info (Informazione)';
PRINT '';
PRINT 'Lingue: IT, EN, RO, DE, SV';
