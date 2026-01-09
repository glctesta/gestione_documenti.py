-- Traduzioni per il modulo di Recupero Password
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Da eseguire sul database per aggiungere le traduzioni necessarie

USE [Traceability_RS]
GO

-- ========================================
-- Voce menu: Recupera Password
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'menu_recover_password')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'menu_recover_password', 'Recupera Password');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'menu_recover_password')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'menu_recover_password', 'Recover Password');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'menu_recover_password')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'menu_recover_password', N'Recuperează Parola');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'menu_recover_password')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'menu_recover_password', 'Passwort Wiederherstellen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'menu_recover_password')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'menu_recover_password', 'Återställ Lösenord');

GO

-- ========================================
-- Titolo finestra
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_title', 'Recupera Password');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_title', 'Recover Password');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_title', N'Recuperare Parolă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_title', 'Passwort Wiederherstellen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_title', 'Återställ Lösenord');

GO

-- ========================================
-- Header finestra
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_header', 'Recupero Credenziali');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_header', 'Credentials Recovery');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_header', N'Recuperare Credențiale');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_header', 'Anmeldedaten Wiederherstellen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_header', 'Återställning av Inloggningsuppgifter');

GO

-- ========================================
-- Istruzioni
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_instructions')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_instructions', 'Inserire almeno uno dei seguenti campi per recuperare le credenziali:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_instructions')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_instructions', 'Enter at least one of the following fields to recover credentials:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_instructions')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_instructions', N'Introduceți cel puțin unul din următoarele câmpuri pentru a recupera credențialele:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_instructions')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_instructions', 'Geben Sie mindestens eines der folgenden Felder ein, um die Anmeldedaten wiederherzustellen:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_instructions')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_instructions', 'Ange minst ett av följande fält för att återställa inloggningsuppgifter:');

GO

-- ========================================
-- Etichette campi
-- ========================================

-- ID Utente
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'label_user_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'label_user_id', 'ID Utente:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'label_user_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'label_user_id', 'User ID:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'label_user_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'label_user_id', N'ID Utilizator:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'label_user_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'label_user_id', 'Benutzer-ID:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'label_user_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'label_user_id', 'Användar-ID:');

GO

-- Numero Badge
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'label_badge_number')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'label_badge_number', 'Numero Badge:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'label_badge_number')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'label_badge_number', 'Badge Number:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'label_badge_number')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'label_badge_number', N'Număr Ecuson:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'label_badge_number')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'label_badge_number', 'Ausweisnummer:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'label_badge_number')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'label_badge_number', 'Kordnummer:');

GO

-- Nome e Cognome
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'label_full_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'label_full_name', 'Nome e Cognome:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'label_full_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'label_full_name', 'Full Name:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'label_full_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'label_full_name', N'Nume Complet:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'label_full_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'label_full_name', 'Vollständiger Name:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'label_full_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'label_full_name', 'Fullständigt Namn:');

GO

-- Email Aziendale
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'label_work_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'label_work_email', 'Email Aziendale:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'label_work_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'label_work_email', 'Work Email:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'label_work_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'label_work_email', N'Email Profesional:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'label_work_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'label_work_email', 'Geschäftliche E-Mail:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'label_work_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'label_work_email', 'Jobbmail:');

GO

-- CNP (Codice Numerico Personale)
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'label_cnp')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'label_cnp', 'CNP (Codice Numerico Personale):');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'label_cnp')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'label_cnp', 'CNP (Personal Numeric Code):');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'label_cnp')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'label_cnp', 'CNP:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'label_cnp')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'label_cnp', 'CNP (Persönliche Nummer):');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'label_cnp')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'label_cnp', 'CNP (Personligt Nummer):');

GO

-- ========================================
-- Bottoni
-- ========================================

-- Recupera
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'button_recover')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'button_recover', 'Recupera');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'button_recover')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'button_recover', 'Recover');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'button_recover')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'button_recover', N'Recuperează');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'button_recover')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'button_recover', 'Wiederherstellen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'button_recover')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'button_recover', 'Återställ');

GO

-- Annulla
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'button_cancel')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'button_cancel', 'Annulla');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'button_cancel')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'button_cancel', 'Cancel');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'button_cancel')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'button_cancel', 'Anulare');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'button_cancel')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'button_cancel', 'Abbrechen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'button_cancel')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'button_cancel', 'Avbryt');

GO

-- ========================================
-- Messaggi di avviso
-- ========================================

-- Campi vuoti
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_empty_fields')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_empty_fields', 'Inserire almeno un campo per effettuare la ricerca');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_empty_fields')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_empty_fields', 'Enter at least one field to perform the search');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_empty_fields')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_empty_fields', N'Introduceți cel puțin un câmp pentru a efectua căutarea');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_empty_fields')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_empty_fields', 'Geben Sie mindestens ein Feld ein, um die Suche durchzuführen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_empty_fields')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_empty_fields', 'Ange minst ett fält för att utföra sökningen');

GO

-- Utente non trovato
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_not_found')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_not_found', 'Nessun utente trovato con i criteri specificati');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_not_found')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_not_found', 'No user found with the specified criteria');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_not_found')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_not_found', N'Niciun utilizator găsit cu criteriile specificate');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_not_found')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_not_found', 'Kein Benutzer mit den angegebenen Kriterien gefunden');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_not_found')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_not_found', 'Ingen användare hittades med de angivna kriterierna');

GO

-- Email non presente
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_no_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_no_email', 'Non è possibile recuperare la password perché nel database dei dipendenti NON è stata registrata una WorkEmail valida per questo utente.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_no_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_no_email', 'Cannot recover password because a valid WorkEmail has NOT been registered in the employee database for this user.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_no_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_no_email', N'Nu se poate recupera parola deoarece o adresă de email profesională validă NU a fost înregistrată în baza de date a angajaților pentru acest utilizator.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_no_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_no_email', 'Das Passwort kann nicht wiederhergestellt werden, da in der Mitarbeiterdatenbank KEINE gültige WorkEmail für diesen Benutzer registriert wurde.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_no_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_no_email', 'Kan inte återställa lösenordet eftersom en giltig WorkEmail INTE har registrerats i personaldatabasen för denna användare.');

GO

-- ========================================
-- Messaggi di successo
-- ========================================

-- Oggetto email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_email_subject')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_email_subject', 'Recupero Credenziali - Traceability RS');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_email_subject')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_email_subject', 'Credentials Recovery - Traceability RS');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_email_subject')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_email_subject', N'Recuperare Credențiale - Traceability RS');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_email_subject')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_email_subject', 'Anmeldedaten Wiederherstellung - Traceability RS');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_email_subject')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_email_subject', 'Återställning av Inloggningsuppgifter - Traceability RS');

GO

-- Email inviata
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'password_recovery_email_sent')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'password_recovery_email_sent', 'Le credenziali sono state inviate all''indirizzo email: {0}');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'password_recovery_email_sent')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'password_recovery_email_sent', 'Credentials have been sent to the email address: {0}');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'password_recovery_email_sent')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'password_recovery_email_sent', N'Credențialele au fost trimise la adresa de email: {0}');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'password_recovery_email_sent')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'password_recovery_email_sent', 'Die Anmeldedaten wurden an die E-Mail-Adresse gesendet: {0}');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'password_recovery_email_sent')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'password_recovery_email_sent', 'Inloggningsuppgifterna har skickats till e-postadressen: {0}');

GO

-- ========================================
-- Contenuto email HTML
-- ========================================

-- Saluto
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_greeting')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_greeting', 'Gentile');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_greeting')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_greeting', 'Dear');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_greeting')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_greeting', 'Stimate');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_greeting')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_greeting', 'Sehr geehrte/r');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_greeting')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_greeting', 'Bäste');

GO

-- Header credenziali
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_credentials_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_credentials_header', 'Ecco le tue credenziali di accesso:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_credentials_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_credentials_header', 'Here are your login credentials:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_credentials_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_credentials_header', N'Iată credențialele dvs. de autentificare:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_credentials_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_credentials_header', 'Hier sind Ihre Anmeldedaten:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_credentials_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_credentials_header', 'Här är dina inloggningsuppgifter:');

GO

-- Label nome utente nell'email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_username_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_username_label', 'Nome utente');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_username_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_username_label', 'Username');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_username_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_username_label', N'Nume utilizator');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_username_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_username_label', 'Benutzername');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_username_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_username_label', 'Användarnamn');

GO

-- Label badge nell'email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_badge_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_badge_label', 'Numero Badge');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_badge_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_badge_label', 'Badge Number');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_badge_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_badge_label', N'Număr Ecuson');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_badge_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_badge_label', 'Ausweisnummer');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_badge_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_badge_label', 'Kordnummer');

GO

-- Label CNP nell'email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_cnp_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_cnp_label', 'CNP');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_cnp_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_cnp_label', 'CNP');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_cnp_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_cnp_label', 'CNP');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_cnp_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_cnp_label', 'CNP');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_cnp_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_cnp_label', 'CNP');

GO

-- Footer email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_footer_text')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_footer_text', 'Questa è un''email automatica. Per favore non rispondere a questo messaggio.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_footer_text')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_footer_text', 'This is an automated email. Please do not reply to this message.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_footer_text')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_footer_text', N'Acesta este un email automat. Vă rugăm să nu răspundeți la acest mesaj.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_footer_text')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_footer_text', 'Dies ist eine automatisierte E-Mail. Bitte antworten Sie nicht auf diese Nachricht.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_footer_text')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_footer_text', 'Detta är ett automatiskt e-postmeddelande. Vänligen svara inte på detta meddelande.');

GO

-- Nota sicurezza
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_security_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_security_note', 'Per motivi di sicurezza, la password non viene mostrata. Se hai dimenticato la password, contatta l''amministratore di sistema.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_security_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_security_note', 'For security reasons, the password is not shown. If you have forgotten your password, contact the system administrator.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_security_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_security_note', N'Din motive de securitate, parola nu este afișată. Dacă ați uitat parola, contactați administratorul de sistem.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_security_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_security_note', 'Aus Sicherheitsgründen wird das Passwort nicht angezeigt. Wenn Sie Ihr Passwort vergessen haben, wenden Sie sich an den Systemadministrator.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_security_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_security_note', 'Av säkerhetsskäl visas inte lösenordet. Om du har glömt ditt lösenord, kontakta systemadministratören.');

GO

-- Nota titolo
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'note_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'note_title', 'Nota');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'note_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'note_title', 'Note');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'note_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'note_title', 'Notă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'note_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'note_title', 'Hinweis');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'note_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'note_title', 'Anteckning');

GO

-- ========================================
-- Messaggi di errore
-- ========================================

-- Errore recupero
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'recovery_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'recovery_error', 'Errore durante il recupero');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'recovery_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'recovery_error', 'Error during recovery');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'recovery_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'recovery_error', N'Eroare în timpul recuperării');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'recovery_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'recovery_error', 'Fehler beim Wiederherstellen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'recovery_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'recovery_error', 'Fel under återställning');

GO

-- Errore invio email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_send_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_send_error', 'Errore durante l''invio dell''email');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_send_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_send_error', 'Error sending email');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_send_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_send_error', N'Eroare la trimiterea email-ului');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_send_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_send_error', 'Fehler beim Senden der E-Mail');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_send_error')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_send_error', 'Fel vid skickande av e-post');


GO

-- Label password nell'email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'email_password_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'email_password_label', 'Password');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'email_password_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'email_password_label', 'Password');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'email_password_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'email_password_label', N'Parolă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'email_password_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'email_password_label', 'Passwort');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'email_password_label')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'email_password_label', 'Lösenord');

GO

-- Messaggio di stato: Preparazione email
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'preparing_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'preparing_email', 'Dati trovati! Preparazione email in corso...');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'preparing_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'preparing_email', 'Data found! Preparing email...');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'preparing_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'preparing_email', N'Date găsite! Pregătirea email-ului în curs...');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'preparing_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'preparing_email', 'Daten gefunden! E-Mail wird vorbereitet...');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'preparing_email')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'preparing_email', 'Data hittad! Förbereder e-post...');

GO

PRINT 'Traduzioni per Recupero Password installate con successo!'
PRINT 'Totale chiavi inserite: 30 x 5 lingue = 150 traduzioni'
GO
