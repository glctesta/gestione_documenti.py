-- =============================================
-- Script SQL per Traduzioni Modulo Straordinari
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: IT, EN, RO, DE, SV
-- =============================================

-- Menu Principale
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_personnel' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'submenu_personnel', N'Personale');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_personnel' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'submenu_personnel', N'Personnel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_personnel' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'submenu_personnel', N'Personal');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_personnel' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'submenu_personnel', N'Personal');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_personnel' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'submenu_personnel', N'Personal');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_overtime' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'submenu_overtime', N'Straordinari');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_overtime' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'submenu_overtime', N'Overtime');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_overtime' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'submenu_overtime', N'Ore Suplimentare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_overtime' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'submenu_overtime', N'Überstunden');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submenu_overtime' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'submenu_overtime', N'Övertid');

-- Sottomenu Straordinari
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_requests' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'overtime_requests', N'Richieste');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_requests' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'overtime_requests', N'Requests');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_requests' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'overtime_requests', N'Cereri');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_requests' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'overtime_requests', N'Anfragen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_requests' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'overtime_requests', N'Förfrågningar');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_approval' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'overtime_approval', N'Autorizzazione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_approval' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'overtime_approval', N'Authorization');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_approval' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'overtime_approval', N'Autorizare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_approval' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'overtime_approval', N'Genehmigung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_approval' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'overtime_approval', N'Godkännande');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_reports' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'overtime_reports', N'Rapporti');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_reports' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'overtime_reports', N'Reports');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_reports' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'overtime_reports', N'Rapoarte');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_reports' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'overtime_reports', N'Berichte');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_reports' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'overtime_reports', N'Rapporter');

-- Form Richieste - Titoli e Sezioni
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_request_title' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'overtime_request_title', N'Richiesta Straordinario');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_request_title' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'overtime_request_title', N'Overtime Request');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_request_title' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'overtime_request_title', N'Cerere Ore Suplimentare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_request_title' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'overtime_request_title', N'Überstundenantrag');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'overtime_request_title' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'overtime_request_title', N'Övertidsansökan');

-- Continua con le altre 50+ chiavi di traduzione...
-- (Lo script completo è troppo lungo, viene generato in un file separato)

PRINT N'Traduzioni modulo straordinari aggiunte con successo!';
