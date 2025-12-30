-- =============================================
-- Script Traduzioni: Change Password Feature
-- Data: 2025-12-17
-- Autore: Antigravity AI Assistant
-- Descrizione: Traduzioni per la funzionalità di cambio password
-- =============================================

USE [Traceability_RS]
GO

-- =============================================
-- MENU: Cambia Password
-- =============================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'menu_change_password')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'menu_change_password', 'Cambia Password');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'menu_change_password')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'menu_change_password', N'Schimbă Parola');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'menu_change_password')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'menu_change_password', 'Change Password');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'menu_change_password')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'menu_change_password', 'Passwort ändern');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'menu_change_password')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'menu_change_password', 'Ändra Lösenord');
END

-- =============================================
-- FINESTRA: Titoli
-- =============================================

-- change_password_title
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'it', 'change_password_title', 'Cambio Password'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'change_password_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'ro', 'change_password_title', N'Schimbare Parolă'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'change_password_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'en', 'change_password_title', 'Change Password'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'change_password_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'de', 'change_password_title', 'Passwort ändern'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'change_password_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'sv', 'change_password_title', 'Ändra Lösenord'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'change_password_title');

-- password_expired_title
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'it', 'password_expired_title', '⚠️ Password Scaduta - Cambio Obbligatorio'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'password_expired_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'ro', 'password_expired_title', N'⚠️ Parolă Expirată - Schimbare Obligatorie'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'password_expired_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'en', 'password_expired_title', '⚠️ Password Expired - Mandatory Change'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'password_expired_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'de', 'password_expired_title', '⚠️ Passwort Abgelaufen - Änderung Erforderlich'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'password_expired_title');

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT 'sv', 'password_expired_title', '⚠️ Lösenord Utgånget - Obligatorisk Ändring'
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'password_expired_title');

-- =============================================
-- LABELS: Campi Form
-- =============================================

-- user_id_label
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'user_id_label', 'User ID:'),
    ('ro', 'user_id_label', N'ID Utilizator:'),
    ('en', 'user_id_label', 'User ID:'),
    ('de', 'user_id_label', 'Benutzer-ID:'),
    ('sv', 'user_id_label', 'Användar-ID:')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- current_password_label
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'current_password_label', 'Password Corrente:'),
    ('ro', 'current_password_label', N'Parolă Curentă:'),
    ('en', 'current_password_label', 'Current Password:'),
    ('de', 'current_password_label', 'Aktuelles Passwort:'),
    ('sv', 'current_password_label', 'Nuvarande Lösenord:')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- new_password_label
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'new_password_label', 'Nuova Password:'),
    ('ro', 'new_password_label', N'Parolă Nouă:'),
    ('en', 'new_password_label', 'New Password:'),
    ('de', 'new_password_label', 'Neues Passwort:'),
    ('sv', 'new_password_label', 'Nytt Lösenord:')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- confirm_password_label
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'confirm_password_label', 'Conferma Password:'),
    ('ro', 'confirm_password_label', N'Confirmă Parola:'),
    ('en', 'confirm_password_label', 'Confirm Password:'),
    ('de', 'confirm_password_label', 'Passwort Bestätigen:'),
    ('sv', 'confirm_password_label', 'Bekräfta Lösenord:')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- =============================================
-- MESSAGGI: Requisiti Password
-- =============================================

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_requirements', 'Requisiti password:
• Minimo 6 caratteri
• Almeno una lettera maiuscola
• Almeno un numero'),
    ('ro', 'password_requirements', N'Cerințe parolă:
• Minim 6 caractere
• Cel puțin o literă mare
• Cel puțin un număr'),
    ('en', 'password_requirements', 'Password requirements:
• Minimum 6 characters
• At least one uppercase letter
• At least one number'),
    ('de', 'password_requirements', 'Passwortanforderungen:
• Mindestens 6 Zeichen
• Mindestens ein Großbuchstabe
• Mindestens eine Zahl'),
    ('sv', 'password_requirements', 'Lösenordskrav:
• Minst 6 tecken
• Minst en stor bokstav
• Minst ett nummer')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- =============================================
-- PULSANTI
-- =============================================

INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'button_change_password', 'Cambia Password'),
    ('ro', 'button_change_password', N'Schimbă Parola'),
    ('en', 'button_change_password', 'Change Password'),
    ('de', 'button_change_password', 'Passwort Ändern'),
    ('sv', 'button_change_password', 'Ändra Lösenord')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = Source.[LanguageCode] 
    AND [TranslationKey] = Source.[TranslationKey]
);

-- =============================================
-- MESSAGGI: Errori e Validazioni
-- =============================================

-- userid_required
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'userid_required', 'Inserire User ID'),
    ('ro', 'userid_required', N'Introduceți ID-ul utilizatorului'),
    ('en', 'userid_required', 'Enter User ID'),
    ('de', 'userid_required', 'Benutzer-ID eingeben'),
    ('sv', 'userid_required', 'Ange Användar-ID')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- current_password_required
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'current_password_required', 'Inserire la password corrente'),
    ('ro', 'current_password_required', N'Introduceți parola curentă'),
    ('en', 'current_password_required', 'Enter current password'),
    ('de', 'current_password_required', 'Aktuelles Passwort eingeben'),
    ('sv', 'current_password_required', 'Ange nuvarande lösenord')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- new_password_required
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'new_password_required', 'Inserire la nuova password'),
    ('ro', 'new_password_required', N'Introduceți noua parolă'),
    ('en', 'new_password_required', 'Enter new password'),
    ('de', 'new_password_required', 'Neues Passwort eingeben'),
    ('sv', 'new_password_required', 'Ange nytt lösenord')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- passwords_dont_match
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'passwords_dont_match', 'Le password non coincidono'),
    ('ro', 'passwords_dont_match', N'Parolele nu se potrivesc'),
    ('en', 'passwords_dont_match', 'Passwords do not match'),
    ('de', 'passwords_dont_match', 'Passwörter stimmen nicht überein'),
    ('sv', 'passwords_dont_match', 'Lösenorden matchar inte')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_too_short
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_too_short', 'La password deve essere di almeno 6 caratteri'),
    ('ro', 'password_too_short', N'Parola trebuie să aibă cel puțin 6 caractere'),
    ('en', 'password_too_short', 'Password must be at least 6 characters'),
    ('de', 'password_too_short', 'Passwort muss mindestens 6 Zeichen lang sein'),
    ('sv', 'password_too_short', 'Lösenordet måste vara minst 6 tecken')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_no_uppercase
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_no_uppercase', 'La password deve contenere almeno una lettera maiuscola'),
    ('ro', 'password_no_uppercase', N'Parola trebuie să conțină cel puțin o literă mare'),
    ('en', 'password_no_uppercase', 'Password must contain at least one uppercase letter'),
    ('de', 'password_no_uppercase', 'Passwort muss mindestens einen Großbuchstaben enthalten'),
    ('sv', 'password_no_uppercase', 'Lösenordet måste innehålla minst en stor bokstav')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_no_number
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_no_number', 'La password deve contenere almeno un numero'),
    ('ro', 'password_no_number', N'Parola trebuie să conțină cel puțin un număr'),
    ('en', 'password_no_number', 'Password must contain at least one number'),
    ('de', 'password_no_number', 'Passwort muss mindestens eine Zahl enthalten'),
    ('sv', 'password_no_number', 'Lösenordet måste innehålla minst ett nummer')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- user_not_found
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'user_not_found', 'Utente non trovato'),
    ('ro', 'user_not_found', N'Utilizator negăsit'),
    ('en', 'user_not_found', 'User not found'),
    ('de', 'user_not_found', 'Benutzer nicht gefunden'),
    ('sv', 'user_not_found', 'Användare hittades inte')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- wrong_current_password
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'wrong_current_password', 'Password corrente errata'),
    ('ro', 'wrong_current_password', N'Parolă curentă greșită'),
    ('en', 'wrong_current_password', 'Wrong current password'),
    ('de', 'wrong_current_password', 'Falsches aktuelles Passwort'),
    ('sv', 'wrong_current_password', 'Fel nuvarande lösenord')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_changed_successfully
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_changed_successfully', 'Password cambiata con successo!'),
    ('ro', 'password_changed_successfully', N'Parolă schimbată cu succes!'),
    ('en', 'password_changed_successfully', 'Password changed successfully!'),
    ('de', 'password_changed_successfully', 'Passwort erfolgreich geändert!'),
    ('sv', 'password_changed_successfully', 'Lösenordet har ändrats!')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_change_required
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_change_required', 'Il cambio password è obbligatorio. Non puoi annullare.'),
    ('ro', 'password_change_required', N'Schimbarea parolei este obligatorie. Nu poți anula.'),
    ('en', 'password_change_required', 'Password change is mandatory. You cannot cancel.'),
    ('de', 'password_change_required', 'Passwortänderung ist obligatorisch. Sie können nicht abbrechen.'),
    ('sv', 'password_change_required', 'Lösenordsändring är obligatorisk. Du kan inte avbryta.')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_expired_message
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_expired_message', 'La tua password è scaduta.
{0}

Devi cambiarla per continuare.'),
    ('ro', 'password_expired_message', N'Parola ta a expirat.
{0}

Trebuie să o schimbi pentru a continua.'),
    ('en', 'password_expired_message', 'Your password has expired.
{0}

You must change it to continue.'),
    ('de', 'password_expired_message', 'Ihr Passwort ist abgelaufen.
{0}

Sie müssen es ändern, um fortzufahren.'),
    ('sv', 'password_expired_message', 'Ditt lösenord har utgått.
{0}

Du måste ändra det för att fortsätta.')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- new_password_same_as_current
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'new_password_same_as_current', 'La nuova password non può essere uguale a quella attuale'),
    ('ro', 'new_password_same_as_current', N'Noua parolă nu poate fi aceeași cu cea curentă'),
    ('en', 'new_password_same_as_current', 'The new password cannot be the same as the current one'),
    ('de', 'new_password_same_as_current', 'Das neue Passwort darf nicht mit dem aktuellen identisch sein'),
    ('sv', 'new_password_same_as_current', 'Det nya lösenordet kan inte vara detsamma som det nuvarande')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

-- password_already_used_recently
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    ('it', 'password_already_used_recently', 'Questa password è già stata utilizzata negli ultimi 6 mesi. Sceglierne una diversa.'),
    ('ro', 'password_already_used_recently', N'Această parolă a fost deja utilizată în ultimele 6 luni. Vă rugăm să alegeți una diferită.'),
    ('en', 'password_already_used_recently', 'This password has already been used in the last 6 months. Please choose a different one.'),
    ('de', 'password_already_used_recently', 'Dieses Passwort wurde bereits in den letzten 6 Monaten verwendet. Bitte wählen Sie ein anderes.'),
    ('sv', 'password_already_used_recently', 'Detta lösenord har redan använts under de senaste 6 månaderna. Välj ett annat.')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = Source.[LanguageCode] AND [TranslationKey] = Source.[TranslationKey]);

PRINT '✅ Script traduzioni cambio password completato con successo!';
PRINT '🌍 Lingue supportate: IT, RO, EN, DE, SV';
PRINT '⚠️  Ricorda di riavviare l''applicazione per caricare le nuove traduzioni!';

GO
