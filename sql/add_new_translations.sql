-- ============================================================
-- Traduzioni: nuove voci aggiunte nelle modifiche recenti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue:   ro, it, en, de, sv
-- ============================================================

USE [Traceability_RS];
GO

-- Helper macro: inserisce solo se la chiave non esiste per quella lingua
-- IF NOT EXISTS per ogni voce

-- ============================================================
-- 1. menu_reset_login  (Help → Reset Login)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'menu_reset_login')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'menu_reset_login', N'Resetare Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'menu_reset_login')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'menu_reset_login', N'Reset Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'menu_reset_login')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'menu_reset_login', N'Reset Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'menu_reset_login')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'menu_reset_login', N'Login zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'menu_reset_login')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'menu_reset_login', N'Återställ inloggning');

-- ============================================================
-- 2. reset_login_title  (titolo popup conferma reset)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'reset_login_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'reset_login_title', N'Resetare Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'reset_login_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'reset_login_title', N'Reset Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'reset_login_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'reset_login_title', N'Reset Login');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'reset_login_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'reset_login_title', N'Login zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'reset_login_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'reset_login_title', N'Återställ inloggning');

-- ============================================================
-- 3. reset_login_msg  (messaggio popup conferma reset)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'reset_login_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'reset_login_msg', N'Login resetat. La urmatoarea operatiune va fi necesar un nou login.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'reset_login_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'reset_login_msg', N'Login reimpostato. Al prossimo accesso verrà richiesto un nuovo login.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'reset_login_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'reset_login_msg', N'Login reset. A new login will be required for the next operation.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'reset_login_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'reset_login_msg', N'Login wurde zurückgesetzt. Beim nächsten Zugriff ist eine neue Anmeldung erforderlich.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'reset_login_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'reset_login_msg', N'Inloggning återställd. Vid nästa åtkomst krävs en ny inloggning.');

GO

-- Verifica inserimenti
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN (
    'menu_reset_login',
    'reset_login_title',
    'reset_login_msg'
)
ORDER BY [TranslationKey], [LanguageCode];
