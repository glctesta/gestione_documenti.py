-- npi_commerciali_translations.sql
-- TAB Commerciale NPI: gestione commerciali + associazione cliente. Lingue it/en/ro/de/sv

-- tab_commerciale_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='tab_commerciale_title' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','tab_commerciale_title','Commerciale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='tab_commerciale_title' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','tab_commerciale_title',N'Sales');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='tab_commerciale_title' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','tab_commerciale_title',N'Comercial');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='tab_commerciale_title' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','tab_commerciale_title',N'Vertrieb');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='tab_commerciale_title' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','tab_commerciale_title',N'Säljare');

-- commerciale_details_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_details_title' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','commerciale_details_title','Dettagli Commerciale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_details_title' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','commerciale_details_title',N'Sales rep details');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_details_title' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','commerciale_details_title',N'Detalii comercial');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_details_title' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','commerciale_details_title',N'Vertriebsdetails');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_details_title' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','commerciale_details_title',N'Säljaruppgifter');

-- label_commerciale_name
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale_name' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_commerciale_name','Nome:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale_name' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_commerciale_name',N'Name:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale_name' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_commerciale_name',N'Nume:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale_name' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_commerciale_name',N'Name:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale_name' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_commerciale_name',N'Namn:');

-- label_phone
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_phone' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_phone','Telefono:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_phone' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_phone',N'Phone:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_phone' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_phone',N'Telefon:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_phone' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_phone',N'Telefon:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_phone' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_phone',N'Telefon:');

-- label_company
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_company' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_company','Società:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_company' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_company',N'Company:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_company' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_company',N'Companie:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_company' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_company',N'Firma:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_company' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_company',N'Företag:');

-- col_phone
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_phone' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','col_phone','Telefono');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_phone' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','col_phone',N'Phone');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_phone' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','col_phone',N'Telefon');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_phone' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','col_phone',N'Telefon');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_phone' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','col_phone',N'Telefon');

-- col_company
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_company' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','col_company','Società');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_company' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','col_company',N'Company');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_company' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','col_company',N'Companie');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_company' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','col_company',N'Firma');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_company' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','col_company',N'Företag');

-- label_email_col
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_email_col' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_email_col','Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_email_col' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_email_col',N'Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_email_col' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_email_col',N'Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_email_col' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_email_col',N'E-Mail');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_email_col' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_email_col',N'E-post');

-- commerciale_assoc_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_assoc_title' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','commerciale_assoc_title','Associazione Cliente → Commerciale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_assoc_title' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','commerciale_assoc_title',N'Client → Sales rep assignment');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_assoc_title' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','commerciale_assoc_title',N'Asociere Client → Comercial');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_assoc_title' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','commerciale_assoc_title',N'Zuordnung Kunde → Vertrieb');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='commerciale_assoc_title' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','commerciale_assoc_title',N'Koppling Kund → Säljare');

-- label_client
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_client' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_client','Cliente:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_client' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_client',N'Client:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_client' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_client',N'Client:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_client' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_client',N'Kunde:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_client' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_client',N'Kund:');

-- label_commerciale
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_commerciale','Commerciale:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_commerciale',N'Sales rep:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_commerciale',N'Comercial:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_commerciale',N'Vertrieb:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_commerciale' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_commerciale',N'Säljare:');

-- btn_assign
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_assign' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','btn_assign','Assegna');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_assign' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','btn_assign',N'Assign');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_assign' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','btn_assign',N'Asociază');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_assign' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','btn_assign',N'Zuweisen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_assign' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','btn_assign',N'Tilldela');

-- btn_remove_assoc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_remove_assoc' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','btn_remove_assoc','Rimuovi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_remove_assoc' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','btn_remove_assoc',N'Remove');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_remove_assoc' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','btn_remove_assoc',N'Elimină');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_remove_assoc' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','btn_remove_assoc',N'Entfernen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='btn_remove_assoc' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','btn_remove_assoc',N'Ta bort');

-- col_client
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_client' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','col_client','Cliente');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_client' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','col_client',N'Client');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_client' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','col_client',N'Client');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_client' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','col_client',N'Kunde');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_client' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','col_client',N'Kund');

-- col_commerciale
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_commerciale' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','col_commerciale','Commerciale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_commerciale' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','col_commerciale',N'Sales rep');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_commerciale' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','col_commerciale',N'Comercial');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_commerciale' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','col_commerciale',N'Vertrieb');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_commerciale' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','col_commerciale',N'Säljare');

-- validation_error_name_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='validation_error_name_required' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','validation_error_name_required','Il nome è obbligatorio.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='validation_error_name_required' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','validation_error_name_required',N'Name is required.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='validation_error_name_required' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','validation_error_name_required',N'Numele este obligatoriu.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='validation_error_name_required' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','validation_error_name_required',N'Name ist erforderlich.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='validation_error_name_required' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','validation_error_name_required',N'Namn krävs.');

-- warning_select_to_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_to_delete' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','warning_select_to_delete','Selezionare un elemento da eliminare.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_to_delete' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','warning_select_to_delete',N'Select an item to delete.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_to_delete' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','warning_select_to_delete',N'Selectați un element de șters.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_to_delete' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','warning_select_to_delete',N'Element zum Löschen auswählen.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_to_delete' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','warning_select_to_delete',N'Välj ett objekt att radera.');

-- warning_select_client_comm
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_client_comm' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','warning_select_client_comm','Seleziona cliente e commerciale.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_client_comm' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','warning_select_client_comm',N'Select client and sales rep.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_client_comm' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','warning_select_client_comm',N'Selectați client și comercial.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_client_comm' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','warning_select_client_comm',N'Kunde und Vertrieb auswählen.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='warning_select_client_comm' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','warning_select_client_comm',N'Välj kund och säljare.');

-- AutoEmail (campo commerciale)
-- label_auto_email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_auto_email' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_auto_email','Invia email automatica (venerdì)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_auto_email' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_auto_email',N'Send automatic email (Friday)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_auto_email' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_auto_email',N'Trimite email automat (vineri)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_auto_email' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_auto_email',N'Automatische E-Mail senden (Freitag)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_auto_email' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_auto_email',N'Skicka automatiskt e-post (fredag)');

-- col_auto_email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_auto_email' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','col_auto_email','Auto Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_auto_email' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','col_auto_email',N'Auto Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_auto_email' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','col_auto_email',N'Auto Email');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_auto_email' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','col_auto_email',N'Auto-E-Mail');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='col_auto_email' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','col_auto_email',N'Auto e-post');
