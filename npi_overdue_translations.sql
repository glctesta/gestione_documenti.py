-- NPI Overdue Tasks Translations
-- npi_overdue_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_title', 'NPI — Task Scaduti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_title', 'NPI — Overdue Tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_title', N'NPI — Taskuri Restante');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_title', 'NPI — Überfällige Tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_title', N'NPI — Försenade Uppgifter');
-- btn_overdue_tasks
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'btn_overdue_tasks' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_overdue_tasks', N'⚠️ Task Scaduti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'btn_overdue_tasks' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_overdue_tasks', N'⚠️ Overdue Tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'btn_overdue_tasks' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_overdue_tasks', N'⚠️ Taskuri Restante');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'btn_overdue_tasks' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_overdue_tasks', N'⚠️ Überfällige Tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'btn_overdue_tasks' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_overdue_tasks', N'⚠️ Försenade Uppgifter');
-- npi_overdue_filters / filter labels / filter_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filters' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filters', 'Filtri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filters' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filters', 'Filters');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filters' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filters', 'Filtre');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filters' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filters', 'Filter');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filters' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filters', 'Filter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_all' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filter_all', 'Tutti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_all' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filter_all', 'All');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_all' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filter_all', 'Toate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_all' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filter_all', 'Alle');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_all' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filter_all', 'Alla');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_customer' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filter_customer', 'Cliente:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_customer' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filter_customer', 'Customer:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_customer' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filter_customer', 'Client:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_customer' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filter_customer', 'Kunde:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_customer' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filter_customer', 'Kund:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_owner' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filter_owner', 'Responsabile:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_owner' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filter_owner', 'Owner:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_owner' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filter_owner', 'Responsabil:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_owner' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filter_owner', N'Verantwortlicher:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_owner' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filter_owner', 'Ansvarig:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_product' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filter_product', 'Prodotto:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_product' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filter_product', 'Product:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_product' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filter_product', 'Produs:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_product' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filter_product', 'Produkt:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_product' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filter_product', 'Produkt:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_task' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_filter_task', 'Task:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_task' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_filter_task', 'Task:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_task' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_filter_task', 'Task:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_task' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_filter_task', 'Aufgabe:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_filter_task' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_filter_task', 'Uppgift:');
-- Column headers
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_project' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_project', 'Progetto NPI');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_project' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_project', 'NPI Project');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_project' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_project', 'Proiect NPI');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_project' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_project', 'NPI Projekt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_project' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_project', 'NPI Projekt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_customer' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_customer', 'Cliente');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_customer' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_customer', 'Customer');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_customer' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_customer', 'Client');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_customer' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_customer', 'Kunde');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_customer' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_customer', 'Kund');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_product' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_product', 'Prodotto');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_product' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_product', 'Product');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_product' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_product', 'Produs');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_product' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_product', 'Produkt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_product' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_product', 'Produkt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_family' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_family', 'Famiglia');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_family' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_family', 'Family');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_family' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_family', 'Familie');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_family' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_family', 'Familie');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_family' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_family', 'Familj');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_task' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_task', 'Task');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_task' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_task', 'Task');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_task' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_task', 'Task');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_task' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_task', 'Aufgabe');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_task' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_task', 'Uppgift');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_owner' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_owner', 'Responsabile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_owner' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_owner', 'Owner');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_owner' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_owner', 'Responsabil');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_owner' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_owner', N'Verantwortlicher');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_owner' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_owner', 'Ansvarig');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_due_date' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_due_date', 'Scadenza');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_due_date' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_due_date', 'Due Date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_due_date' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_due_date', 'Termen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_due_date' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_due_date', N'Fälligkeitsdatum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_due_date' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_due_date', 'Deadline');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_days_late' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_days_late', 'Giorni Ritardo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_days_late' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_days_late', 'Days Late');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_days_late' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_days_late', N'Zile Întârziere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_days_late' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_days_late', N'Verzugstage');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_days_late' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_days_late', N'Förseningsdagar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_status' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_col_status', 'Stato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_status' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_col_status', 'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_status' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_col_status', 'Stare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_status' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_col_status', 'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_col_status' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_col_status', 'Status');
-- Buttons
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_reset' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_btn_reset', 'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_reset' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_btn_reset', 'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_reset' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_btn_reset', 'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_reset' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_btn_reset', N'Zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_reset' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_btn_reset', N'Återställ');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_all' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_btn_remind_all', N'📧 Sollecita tutti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_all' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_btn_remind_all', N'📧 Remind All');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_all' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_btn_remind_all', N'📧 Amintire tuturor');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_all' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_btn_remind_all', N'📧 Alle erinnern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_all' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_btn_remind_all', N'📧 Påminn alla');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_selected' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_btn_remind_selected', N'📧 Sollecita selezionati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_selected' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_btn_remind_selected', N'📧 Remind Selected');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_selected' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_btn_remind_selected', N'📧 Amintire selectați');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_selected' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_btn_remind_selected', N'📧 Auswahl erinnern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_remind_selected' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_btn_remind_selected', N'📧 Påminn valda');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_export' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'npi_overdue_btn_export', N'📊 Esporta Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_export' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'npi_overdue_btn_export', N'📊 Export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_export' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'npi_overdue_btn_export', N'📊 Export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_export' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'npi_overdue_btn_export', N'📊 Excel exportieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_btn_export' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'npi_overdue_btn_export', N'📊 Exportera Excel');
-- Status bar + messages
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_overdue' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_status_overdue', 'task scaduti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_overdue' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_status_overdue', 'overdue tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_overdue' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_status_overdue', N'taskuri restante');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_overdue' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_status_overdue', N'überfällige Tasks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_overdue' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_status_overdue', N'försenade uppgifter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_owners' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_status_owners', 'responsabili');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_owners' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_status_owners', 'owners');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_owners' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_status_owners', 'responsabili');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_owners' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_status_owners', N'Verantwortliche');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_owners' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_status_owners', 'ansvariga');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_total' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_status_total', 'Totale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_total' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_status_total', 'Total');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_total' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_status_total', 'Total');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_total' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_status_total', 'Gesamt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_status_total' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_status_total', 'Totalt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_tasks' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_no_tasks', 'Nessun task in lista.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_tasks' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_no_tasks', 'No tasks in list.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_tasks' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_no_tasks', N'Nicio sarcină în listă.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_tasks' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_no_tasks', 'Keine Tasks in der Liste.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_tasks' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_no_tasks', N'Inga uppgifter i listan.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_select_task' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_select_task', 'Selezionare almeno un task.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_select_task' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_select_task', 'Please select at least one task.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_select_task' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_select_task', N'Selectați cel puțin un task.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_select_task' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_select_task', 'Bitte mindestens einen Task ausw.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_select_task' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_select_task', N'Välj minst en uppgift.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_email' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_no_email', 'Nessun responsabile con indirizzo email trovato.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_email' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_no_email', 'No owner with email address found.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_email' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_no_email', N'Niciun responsabil cu email găsit.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_email' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_no_email', N'Kein Verantwortlicher mit E-Mail gefunden.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_no_email' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_no_email', N'Ingen ansvarig med e-post hittades.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_title' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_confirm_title', 'Conferma invio');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_title' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_confirm_title', 'Confirm Send');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_title' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_confirm_title', 'Confirmare trimitere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_title' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_confirm_title', 'Senden bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_title' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_confirm_title', N'Bekräfta sändning');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_msg' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_confirm_msg', 'Inviare email di sollecito a');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_msg' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_confirm_msg', 'Send reminder email to');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_msg' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_confirm_msg', 'Trimite email de reminder la');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_msg' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_confirm_msg', 'Erinnerung senden an');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_confirm_msg' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_confirm_msg', N'Skicka påminnelse till');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_sent' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_email_sent', 'Email inviate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_sent' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_email_sent', 'Emails sent');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_sent' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_email_sent', 'Email-uri trimise');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_sent' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_email_sent', 'E-Mails gesendet');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_sent' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_email_sent', 'E-post skickade');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_failed' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_email_failed', 'Fallite');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_failed' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_email_failed', 'Failed');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_failed' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_email_failed', 'Eșuate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_failed' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_email_failed', 'Fehlgeschlagen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_email_failed' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_email_failed', 'Misslyckades');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_excel_saved' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_excel_saved', 'Excel salvato in');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_excel_saved' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_excel_saved', 'Excel saved to');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_excel_saved' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_excel_saved', N'Excel salvat în');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_excel_saved' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_excel_saved', 'Excel gespeichert in');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_excel_saved' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_excel_saved', 'Excel sparad i');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_open_now' AND LanguageCode = 'it') INSERT INTO [dbo].[AppTranslations] VALUES ('it', 'npi_overdue_open_now', 'Aprirlo ora?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_open_now' AND LanguageCode = 'en') INSERT INTO [dbo].[AppTranslations] VALUES ('en', 'npi_overdue_open_now', 'Open it now?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_open_now' AND LanguageCode = 'ro') INSERT INTO [dbo].[AppTranslations] VALUES ('ro', 'npi_overdue_open_now', N'Deschideți acum?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_open_now' AND LanguageCode = 'de') INSERT INTO [dbo].[AppTranslations] VALUES ('de', 'npi_overdue_open_now', 'Jetzt öffnen?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'npi_overdue_open_now' AND LanguageCode = 'sv') INSERT INTO [dbo].[AppTranslations] VALUES ('sv', 'npi_overdue_open_now', N'Öppna nu?');

PRINT 'NPI Overdue Tasks translations inserted.';
