-- recovery_password_email_translations.sql
-- Password recovery: email obbligatoria (CNP non piu obbligatorio). Lingue it/en/ro/de/sv

-- password_recovery_instructions
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='it')
    UPDATE [dbo].[AppTranslations] SET TranslationValue='Inserire l''email aziendale (OBBLIGATORIA). Gli altri campi sono opzionali e servono solo a restringere la ricerca. Le credenziali saranno inviate all''email aziendale registrata.' WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='it';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','password_recovery_instructions','Inserire l''email aziendale (OBBLIGATORIA). Gli altri campi sono opzionali e servono solo a restringere la ricerca. Le credenziali saranno inviate all''email aziendale registrata.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='en')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Enter your company email (REQUIRED). All other fields are optional and only narrow the search. Credentials will be sent to the registered company email.' WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='en';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','password_recovery_instructions',N'Enter your company email (REQUIRED). All other fields are optional and only narrow the search. Credentials will be sent to the registered company email.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='ro')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Introduceți emailul de companie (OBLIGATORIU). Celelalte câmpuri sunt opționale și doar restrâng căutarea. Credențialele vor fi trimise la emailul de companie înregistrat.' WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','password_recovery_instructions',N'Introduceți emailul de companie (OBLIGATORIU). Celelalte câmpuri sunt opționale și doar restrâng căutarea. Credențialele vor fi trimise la emailul de companie înregistrat.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='de')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Geben Sie Ihre Firmen-E-Mail ein (PFLICHT). Alle anderen Felder sind optional und schränken nur die Suche ein. Die Zugangsdaten werden an die registrierte Firmen-E-Mail gesendet.' WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='de';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','password_recovery_instructions',N'Geben Sie Ihre Firmen-E-Mail ein (PFLICHT). Alle anderen Felder sind optional und schränken nur die Suche ein. Die Zugangsdaten werden an die registrierte Firmen-E-Mail gesendet.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='sv')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Ange din företagsmejl (OBLIGATORISKT). Övriga fält är valfria och avgränsar bara sökningen. Inloggningsuppgifterna skickas till den registrerade företagsmejlen.' WHERE TranslationKey='password_recovery_instructions' AND LanguageCode='sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','password_recovery_instructions',N'Ange din företagsmejl (OBLIGATORISKT). Övriga fält är valfria och avgränsar bara sökningen. Inloggningsuppgifterna skickas till den registrerade företagsmejlen.');

-- label_work_email_required
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_work_email_required' AND LanguageCode='it')
    UPDATE [dbo].[AppTranslations] SET TranslationValue='Email Aziendale (obbligatoria):' WHERE TranslationKey='label_work_email_required' AND LanguageCode='it';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','label_work_email_required','Email Aziendale (obbligatoria):');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_work_email_required' AND LanguageCode='en')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Company Email (required):' WHERE TranslationKey='label_work_email_required' AND LanguageCode='en';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','label_work_email_required',N'Company Email (required):');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_work_email_required' AND LanguageCode='ro')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Email companie (obligatoriu):' WHERE TranslationKey='label_work_email_required' AND LanguageCode='ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','label_work_email_required',N'Email companie (obligatoriu):');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_work_email_required' AND LanguageCode='de')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Firmen-E-Mail (Pflicht):' WHERE TranslationKey='label_work_email_required' AND LanguageCode='de';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','label_work_email_required',N'Firmen-E-Mail (Pflicht):');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='label_work_email_required' AND LanguageCode='sv')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Företagsmejl (obligatoriskt):' WHERE TranslationKey='label_work_email_required' AND LanguageCode='sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','label_work_email_required',N'Företagsmejl (obligatoriskt):');

-- recovery_email_required
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_required' AND LanguageCode='it')
    UPDATE [dbo].[AppTranslations] SET TranslationValue='L''email aziendale è obbligatoria per il recupero password.' WHERE TranslationKey='recovery_email_required' AND LanguageCode='it';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','recovery_email_required','L''email aziendale è obbligatoria per il recupero password.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_required' AND LanguageCode='en')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'The company email is required for password recovery.' WHERE TranslationKey='recovery_email_required' AND LanguageCode='en';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','recovery_email_required',N'The company email is required for password recovery.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_required' AND LanguageCode='ro')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Emailul de companie este obligatoriu pentru recuperarea parolei.' WHERE TranslationKey='recovery_email_required' AND LanguageCode='ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','recovery_email_required',N'Emailul de companie este obligatoriu pentru recuperarea parolei.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_required' AND LanguageCode='de')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Die Firmen-E-Mail ist für die Passwortwiederherstellung erforderlich.' WHERE TranslationKey='recovery_email_required' AND LanguageCode='de';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','recovery_email_required',N'Die Firmen-E-Mail ist für die Passwortwiederherstellung erforderlich.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_required' AND LanguageCode='sv')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Företagsmejlen krävs för lösenordsåterställning.' WHERE TranslationKey='recovery_email_required' AND LanguageCode='sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','recovery_email_required',N'Företagsmejlen krävs för lösenordsåterställning.');

-- recovery_email_invalid
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='it')
    UPDATE [dbo].[AppTranslations] SET TranslationValue='Formato email non valido.' WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='it';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('it','recovery_email_invalid','Formato email non valido.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='en')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Invalid email format.' WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='en';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('en','recovery_email_invalid',N'Invalid email format.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='ro')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Format de email invalid.' WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='ro';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro','recovery_email_invalid',N'Format de email invalid.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='de')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Ungültiges E-Mail-Format.' WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='de';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('de','recovery_email_invalid',N'Ungültiges E-Mail-Format.');
IF EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='sv')
    UPDATE [dbo].[AppTranslations] SET TranslationValue=N'Ogiltigt e-postformat.' WHERE TranslationKey='recovery_email_invalid' AND LanguageCode='sv';
ELSE
    INSERT INTO [dbo].[AppTranslations] (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv','recovery_email_invalid',N'Ogiltigt e-postformat.');
