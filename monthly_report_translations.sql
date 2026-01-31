-- Script SQL per aggiungere traduzioni per il sistema di Report Mensile
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO (Rumeno), IT (Italiano), EN (Inglese), DE (Tedesco), SV (Svedese)

USE [Traceability_RS];
GO

-- ========================================
-- TRADUZIONI PER EMAIL MENSILE
-- ========================================

-- Titolo Email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'monthly_email_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'monthly_email_title', N'Raport Lunar - Defecte după Validarea Plăcilor');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'monthly_email_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'monthly_email_title', N'Rapporto Mensile - Difetti dopo la Validazione delle Schede');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'monthly_email_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'monthly_email_title', N'Monthly Review - Fail after Board Validation');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'monthly_email_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'monthly_email_title', N'Monatsbericht - Fehler nach Platinen-Validierung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'monthly_email_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'monthly_email_title', N'Månadsrapport - Fel efter Kortvalidering');

-- Corpo Email - Paragrafo 1
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'monthly_email_body1')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'monthly_email_body1', N'Acest email rezumă situația referitoare la plăcile care au fost validate PASS pentru procesele de PTH, COATING și SMT.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'monthly_email_body1')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'monthly_email_body1', N'Questa email riepiloga la situazione afferente alle schede che sono state validate PASS per i processi di PTH, COATING e SMT.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'monthly_email_body1')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'monthly_email_body1', N'This email summarizes the situation regarding boards that were validated PASS for PTH, COATING and SMT processes.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'monthly_email_body1')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'monthly_email_body1', N'Diese E-Mail fasst die Situation bezüglich der Platinen zusammen, die für PTH-, COATING- und SMT-Prozesse als PASS validiert wurden.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'monthly_email_body1')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'monthly_email_body1', N'Detta e-postmeddelande sammanfattar situationen för kort som validerades PASS för PTH-, COATING- och SMT-processer.');

-- Corpo Email - Paragrafo 2
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'monthly_email_body2')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'monthly_email_body2', N'În atașament găsiți raportul detaliat cu statisticile PPM (Parts Per Million) pe utilizator.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'monthly_email_body2')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'monthly_email_body2', N'In allegato trovate il report dettagliato con le statistiche PPM (Parts Per Million) per utente.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'monthly_email_body2')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'monthly_email_body2', N'Attached you will find the detailed report with PPM (Parts Per Million) statistics per user.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'monthly_email_body2')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'monthly_email_body2', N'Im Anhang finden Sie den detaillierten Bericht mit PPM-Statistiken (Parts Per Million) pro Benutzer.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'monthly_email_body2')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'monthly_email_body2', N'Bifogat hittar du den detaljerade rapporten med PPM-statistik (Parts Per Million) per användare.');

-- Saluti Email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'monthly_email_closing')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'monthly_email_closing', N'Cu stimă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'monthly_email_closing')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'monthly_email_closing', N'Cordiali saluti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'monthly_email_closing')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'monthly_email_closing', N'Best regards');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'monthly_email_closing')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'monthly_email_closing', N'Mit freundlichen Grüßen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'monthly_email_closing')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'monthly_email_closing', N'Med vänliga hälsningar');

-- Firma Email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'monthly_email_signature')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'monthly_email_signature', N'Sistem de Trasabilitate');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'monthly_email_signature')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'monthly_email_signature', N'Sistema di Tracciabilità');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'monthly_email_signature')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'monthly_email_signature', N'Traceability System');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'monthly_email_signature')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'monthly_email_signature', N'Rückverfolgbarkeitssystem');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'monthly_email_signature')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'monthly_email_signature', N'Spårbarhetssystem');

-- ========================================
-- TRADUZIONI PER INTERFACCIA GRAFICA
-- ========================================

-- Intestazione colonna PPM
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'stats_failed_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'stats_failed_ppm', N'PPM Defecte');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'stats_failed_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'stats_failed_ppm', N'PPM Difetti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'stats_failed_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'stats_failed_ppm', N'Failed PPM');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'stats_failed_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'stats_failed_ppm', N'Fehler PPM');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'stats_failed_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'stats_failed_ppm', N'Fel PPM');

-- Titolo grafico Excel
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'chart_title_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'chart_title_ppm', N'Plăci Verificate vs PPM Defecte pe Utilizator');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'chart_title_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'chart_title_ppm', N'Schede Verificate vs PPM Difetti per Utente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'chart_title_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'chart_title_ppm', N'Verified Boards vs Failed PPM by User');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'chart_title_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'chart_title_ppm', N'Verifizierte Platinen vs Fehler PPM nach Benutzer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'chart_title_ppm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'chart_title_ppm', N'Verifierade Kort vs Fel PPM per Användare');

-- ========================================
-- MESSAGGI DI LOG
-- ========================================

-- Background task avviato
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'log_monthly_report_started')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'log_monthly_report_started', N'Sarcină de fundal pentru raportul lunar pornită');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'log_monthly_report_started')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'log_monthly_report_started', N'Background task per report mensile avviato');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'log_monthly_report_started')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'log_monthly_report_started', N'Background task for monthly report started');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'log_monthly_report_started')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'log_monthly_report_started', N'Hintergrundaufgabe für Monatsbericht gestartet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'log_monthly_report_started')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'log_monthly_report_started', N'Bakgrundsuppgift för månadsrapport startad');

-- Report inviato con successo
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'log_monthly_report_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'log_monthly_report_sent', N'Raport lunar trimis cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'log_monthly_report_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'log_monthly_report_sent', N'Report mensile inviato con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'log_monthly_report_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'log_monthly_report_sent', N'Monthly report sent successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'log_monthly_report_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'log_monthly_report_sent', N'Monatsbericht erfolgreich gesendet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'log_monthly_report_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'log_monthly_report_sent', N'Månadsrapport skickad framgångsrikt');

GO

PRINT 'Traduzioni per il sistema di Report Mensile aggiunte con successo!';
PRINT 'Totale chiavi di traduzione: 8';
PRINT 'Totale lingue: 5 (RO, IT, EN, DE, SV)';
PRINT 'Totale record inseriti: 40';
