-- SQL Script per aggiungere traduzioni per FAI Fails Report
-- Eseguire su database Traceability_RS

USE [Traceability_RS]
GO

-- Rapporto FAI fails (menu label)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'rapporto_fai_fails' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'rapporto_fai_fails', N'Rapporto FAI fails')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'rapporto_fai_fails' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'rapporto_fai_fails', N'FAI Fails Report')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'rapporto_fai_fails' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'rapporto_fai_fails', N'Raport Eșecuri FAI')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'rapporto_fai_fails' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'rapporto_fai_fails', N'FAI-Fehler-Bericht')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'rapporto_fai_fails' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'rapporto_fai_fails', N'FAI-felrapport')

-- Filtro operatore
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_operator_filter' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'fai_fails_operator_filter', N'Operatore')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_operator_filter' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'fai_fails_operator_filter', N'Operator')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_operator_filter' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'fai_fails_operator_filter', N'Operator')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_operator_filter' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'fai_fails_operator_filter', N'Bediener')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_operator_filter' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'fai_fails_operator_filter', N'Operatör')

-- Totale Record
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_total_records' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'fai_fails_total_records', N'Totale Record')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_total_records' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'fai_fails_total_records', N'Total Records')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_total_records' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'fai_fails_total_records', N'Total Înregistrări')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_total_records' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'fai_fails_total_records', N'Gesamtdatensätze')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_total_records' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'fai_fails_total_records', N'Totalt Antal Poster')

-- Record Falliti
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failed_records' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'fai_fails_failed_records', N'Record Falliti')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failed_records' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'fai_fails_failed_records', N'Failed Records')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failed_records' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'fai_fails_failed_records', N'Înregistrări Eșuate')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failed_records' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'fai_fails_failed_records', N'Fehlgeschlagene Datensätze')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failed_records' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'fai_fails_failed_records', N'Misslyckade Poster')

-- Tasso di Fallimento
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failure_rate' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'fai_fails_failure_rate', N'Tasso di Fallimento (%)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failure_rate' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'fai_fails_failure_rate', N'Failure Rate (%)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failure_rate' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'fai_fails_failure_rate', N'Rata de Eșec (%)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failure_rate' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'fai_fails_failure_rate', N'Fehlerrate (%)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_fails_failure_rate' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'fai_fails_failure_rate', N'Felfrekvens (%)')

-- Solo Fails (checkbox filter)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_only_fails' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'fai_only_fails', N'Solo Fails')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_only_fails' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'fai_only_fails', N'Fails Only')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_only_fails' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'fai_only_fails', N'Doar Eșecuri')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_only_fails' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'fai_only_fails', N'Nur Fehler')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'fai_only_fails' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'fai_only_fails', N'Endast Fel')

GO

PRINT 'Traduzioni per FAI Fails Report aggiunte con successo!'
