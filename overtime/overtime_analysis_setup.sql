-- =====================================================
-- SQL Script: Overtime Analysis Feature - Database Setup
-- =====================================================

-- 1. Add email recipients setting for overtime issues
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.Settings WHERE AttributeName = 'Sys_email_overtime_issues')
BEGIN
    INSERT INTO Traceability_RS.dbo.Settings (AttributeName, AttributeValue, Description)
    VALUES (
        'Sys_email_overtime_issues',
        'your.email@company.com',  -- REPLACE WITH ACTUAL EMAIL(S), comma-separated
        'Email recipients for weekly unauthorized overtime reports'
    )
    PRINT 'Setting Sys_email_overtime_issues created'
END
ELSE
BEGIN
    PRINT 'Setting Sys_email_overtime_issues already exists'
END
GO

-- 2. Add translations for overtime analysis feature
-- Italian
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis', N'it', N'Analisi Straordinari');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis_title' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis_title', N'it', N'Analisi Straordinari');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'filter_type' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'filter_type', N'it', N'Tipo Filtro');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'generate_analysis' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'generate_analysis', N'it', N'Genera Analisi');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_done' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_done', N'it', N'Min Presenza');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_approved' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_approved', N'it', N'Min Approvati');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'no_retroactive_requests' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'no_retroactive_requests', N'it', N'Le richieste di straordinario non possono essere retroattive.\nLa data/ora di inizio deve essere nel futuro.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'end_before_start' AND LanguageCode = 'it')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'end_before_start', N'it', N'La data/ora di fine deve essere successiva alla data/ora di inizio.');

-- English
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis', N'en', N'Overtime Analysis');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis_title' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis_title', N'en', N'Overtime Analysis');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'filter_type' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'filter_type', N'en', N'Filter Type');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'generate_analysis' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'generate_analysis', N'en', N'Generate Analysis');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_done' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_done', N'en', N'Min Presence');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_approved' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_approved', N'en', N'Min Approved');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'no_retroactive_requests' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'no_retroactive_requests', N'en', N'Overtime requests cannot be retroactive.\nThe start date/time must be in the future.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'end_before_start' AND LanguageCode = 'en')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'end_before_start', N'en', N'The end date/time must be after the start date/time.');

-- Romanian
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis', N'ro', N'Analiza Ore Suplimentare');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'overtime_analysis_title' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'overtime_analysis_title', N'ro', N'Analiza Ore Suplimentare');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'filter_type' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'filter_type', N'ro', N'Tip Filtru');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'generate_analysis' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'generate_analysis', N'ro', N'Generează Analiză');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_done' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_done', N'ro', N'Min Prezență');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'min_approved' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'min_approved', N'ro', N'Min Aprobate');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'no_retroactive_requests' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'no_retroactive_requests', N'ro', N'Cererile de ore suplimentare nu pot fi retroactive.\nData/ora de început trebuie să fie în viitor.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE TranslationKey = 'end_before_start' AND LanguageCode = 'ro')
    INSERT INTO Traceability_RS.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue)
    VALUES (N'end_before_start', N'ro', N'Data/ora de sfârșit trebuie să fie după data/ora de început.');

PRINT 'Translations added successfully'
GO
