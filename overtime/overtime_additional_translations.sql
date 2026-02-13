-- =====================================================
-- SQL Script: Overtime Module - Additional Translations
-- =====================================================
-- Adds translations for overtime request form fields
-- Languages: IT, EN, RO, DE, SV

-- employee_selection
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_selection' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'employee_selection', N'Selezione Dipendente');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_selection' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'employee_selection', N'Employee Selection');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_selection' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'employee_selection', N'Selectare Angajat');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_selection' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'employee_selection', N'Mitarbeiterauswahl');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_selection' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'employee_selection', N'Val av Anställd');

-- start_datetime
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'start_datetime' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'start_datetime', N'Data/Ora Inizio');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'start_datetime' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'start_datetime', N'Start Date/Time');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'start_datetime' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'start_datetime', N'Data/Ora Început');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'start_datetime' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'start_datetime', N'Startdatum/-zeit');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'start_datetime' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'start_datetime', N'Startdatum/Tid');

-- end_datetime
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'end_datetime' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'end_datetime', N'Data/Ora Fine');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'end_datetime' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'end_datetime', N'End Date/Time');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'end_datetime' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'end_datetime', N'Data/Ora Sfârșit');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'end_datetime' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'end_datetime', N'Enddatum/-zeit');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'end_datetime' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'end_datetime', N'Slutdatum/Tid');

-- justification
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'justification' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'justification', N'Giustificazione');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'justification' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'justification', N'Justification');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'justification' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'justification', N'Justificare');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'justification' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'justification', N'Begründung');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'justification' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'justification', N'Motivering');

-- add_employee
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'add_employee' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'add_employee', N'Aggiungi Dipendente');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'add_employee' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'add_employee', N'Add Employee');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'add_employee' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'add_employee', N'Adaugă Angajat');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'add_employee' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'add_employee', N'Mitarbeiter Hinzufügen');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'add_employee' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'add_employee', N'Lägg till Anställd');

-- employee_list (employees_list)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employees_list' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'employees_list', N'Dipendenti Aggiunti');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employees_list' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'employees_list', N'Added Employees');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employees_list' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'employees_list', N'Angajați Adăugați');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employees_list' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'employees_list', N'Hinzugefügte Mitarbeiter');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employees_list' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'employees_list', N'Tillagda Anställda');

-- submit_request
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submit_request' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'submit_request', N'Invia Richiesta');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submit_request' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'submit_request', N'Submit Request');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submit_request' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'submit_request', N'Trimite Cerere');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submit_request' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'submit_request', N'Anfrage Senden');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'submit_request' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'submit_request', N'Skicka Begäran');

-- remove_selected
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'remove_selected' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'remove_selected', N'Rimuovi Selezionato');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'remove_selected' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'remove_selected', N'Remove Selected');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'remove_selected' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'remove_selected', N'Elimină Selectat');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'remove_selected' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'remove_selected', N'Ausgewählte Entfernen');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'remove_selected' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'remove_selected', N'Ta bort Vald');

-- hours
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'hours' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'hours', N'Ore');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'hours' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'hours', N'Hours');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'hours' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'hours', N'Ore');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'hours' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'hours', N'Stunden');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'hours' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'hours', N'Timmar');

PRINT 'Additional overtime translations added successfully';
GO
