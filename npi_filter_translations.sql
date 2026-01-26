-- Script per inserire traduzioni filtro cliente NPI
-- Lingue: it, ro, en, de, sv

-- ========================================
-- 1. filters (Filtri)
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'filters')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'filters', N'Filtri');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'filters')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'filters', N'Filtre');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'filters')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'filters', N'Filters');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'filters')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'filters', N'Filter');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'filters')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'filters', N'Filter');
END

-- ========================================
-- 2. npi_client_filter (Cliente:)
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'npi_client_filter')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_client_filter', N'Cliente:');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'npi_client_filter')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_client_filter', N'Client:');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'npi_client_filter')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_client_filter', N'Client:');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'npi_client_filter')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_client_filter', N'Kunde:');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'npi_client_filter')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_client_filter', N'Kund:');
END

-- ========================================
-- 3. npi_all_clients (Tutti i Clienti)
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'npi_all_clients')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_all_clients', N'Tutti i Clienti');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'npi_all_clients')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_all_clients', N'Toți clienții');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'npi_all_clients')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_all_clients', N'All Clients');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'npi_all_clients')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_all_clients', N'Alle Kunden');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'npi_all_clients')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_all_clients', N'Alla kunder');
END

-- ========================================
-- 4. npi_project_label (Progetto:)
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'npi_project_label')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_project_label', N'Progetto:');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'npi_project_label')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_project_label', N'Proiect:');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'npi_project_label')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_project_label', N'Project:');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'npi_project_label')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_project_label', N'Projekt:');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'npi_project_label')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_project_label', N'Projekt:');
END

-- ========================================
-- Verifica inserimenti
-- ========================================
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] IN (N'filters', N'npi_client_filter', N'npi_all_clients', N'npi_project_label')
ORDER BY [TranslationKey], [LanguageCode];
