-- =============================================
-- Script: Traduzioni per Filtri Gantt
-- Descrizione: Aggiunge le chiavi di traduzione per i filtri
--              cliente e prodotto nella finestra di selezione
--              del progetto Gantt
-- Data: 2026-01-22
-- =============================================

USE [Traceability_RS]
GO

-- Verifica se le traduzioni esistono già
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_select_client')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_select_client', 'Cliente:'),
    ('EN', 'gantt_select_client', 'Client:'),
    ('RO', 'gantt_select_client', 'Client:');
    
    PRINT 'Traduzione "gantt_select_client" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_select_client" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_all_clients')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_all_clients', 'Tutti i Clienti'),
    ('EN', 'gantt_all_clients', 'All Clients'),
    ('RO', 'gantt_all_clients', 'Toți Clienții');
    
    PRINT 'Traduzione "gantt_all_clients" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_all_clients" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_select_product')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_select_product', 'Prodotto:'),
    ('EN', 'gantt_select_product', 'Product:'),
    ('RO', 'gantt_select_product', 'Produs:');
    
    PRINT 'Traduzione "gantt_select_product" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_select_product" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_all_products')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_all_products', 'Tutti i Prodotti'),
    ('EN', 'gantt_all_products', 'All Products'),
    ('RO', 'gantt_all_products', 'Toate Produsele');
    
    PRINT 'Traduzione "gantt_all_products" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_all_products" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_select_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_select_project', 'Seleziona Progetto'),
    ('EN', 'gantt_select_project', 'Select Project'),
    ('RO', 'gantt_select_project', 'Selectează Proiect');
    
    PRINT 'Traduzione "gantt_select_project" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_select_project" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_choose_project')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_choose_project', 'Scegli un progetto per visualizzare il Gantt:'),
    ('EN', 'gantt_choose_project', 'Choose a project to view the Gantt:'),
    ('RO', 'gantt_choose_project', 'Alege un proiect pentru a vizualiza Gantt:');
    
    PRINT 'Traduzione "gantt_choose_project" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_choose_project" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'gantt_select_project_warning')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'gantt_select_project_warning', 'Seleziona un progetto dalla lista.'),
    ('EN', 'gantt_select_project_warning', 'Select a project from the list.'),
    ('RO', 'gantt_select_project_warning', 'Selectează un proiect din listă.');
    
    PRINT 'Traduzione "gantt_select_project_warning" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "gantt_select_project_warning" già esistente.';

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'filters')
BEGIN
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES
    ('IT', 'filters', 'Filtri'),
    ('EN', 'filters', 'Filters'),
    ('RO', 'filters', 'Filtre');
    
    PRINT 'Traduzione "filters" aggiunta con successo.';
END
ELSE
    PRINT 'Traduzione "filters" già esistente.';

PRINT '';
PRINT '========================================';
PRINT 'Script completato con successo!';
PRINT 'Tutte le traduzioni per i filtri Gantt sono state aggiunte.';
PRINT '========================================';
GO
