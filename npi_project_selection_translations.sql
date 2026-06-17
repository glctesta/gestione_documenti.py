-- npi_project_selection_translations.sql
-- Combo selezione progetti NPI: scadenza + stato (aperto/chiuso) e bottone Torna alla selezione
-- Lingue it/en/ro/de/sv

-- npi_project_deadline
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_project_deadline' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','npi_project_deadline','Scadenza');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_project_deadline' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','npi_project_deadline',N'Deadline');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_project_deadline' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','npi_project_deadline',N'Termen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_project_deadline' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','npi_project_deadline',N'Frist');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_project_deadline' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','npi_project_deadline',N'Deadline');

-- npi_no_deadline
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_no_deadline' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','npi_no_deadline','n/d');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_no_deadline' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','npi_no_deadline',N'n/a');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_no_deadline' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','npi_no_deadline',N'nespecificat');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_no_deadline' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','npi_no_deadline',N'k.A.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_no_deadline' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','npi_no_deadline',N'ej angivet');

-- npi_status_closed
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_closed' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','npi_status_closed','Chiuso');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_closed' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','npi_status_closed',N'Closed');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_closed' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','npi_status_closed',N'Închis');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_closed' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','npi_status_closed',N'Geschlossen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_closed' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','npi_status_closed',N'Stängt');

-- npi_status_open
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_open' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','npi_status_open','Aperto');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_open' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','npi_status_open',N'Open');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_open' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','npi_status_open',N'Deschis');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_open' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','npi_status_open',N'Offen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='npi_status_open' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','npi_status_open',N'Öppet');

-- btn_back_to_selection
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_back_to_selection' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','btn_back_to_selection','⬅ Torna alla selezione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_back_to_selection' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','btn_back_to_selection',N'⬅ Back to selection');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_back_to_selection' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','btn_back_to_selection',N'⬅ Înapoi la selecție');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_back_to_selection' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','btn_back_to_selection',N'⬅ Zurück zur Auswahl');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_back_to_selection' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','btn_back_to_selection',N'⬅ Tillbaka till val');
