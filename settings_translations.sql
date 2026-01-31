-- Script SQL per aggiungere traduzioni per Gestione Impostazioni Email
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO (Rumeno), IT (Italiano), EN (Inglese), DE (Tedesco), SV (Svedese)

USE [Traceability_RS];
GO

-- ========================================
-- TRADUZIONI PER GESTIONE IMPOSTAZIONI EMAIL
-- ========================================

-- submenu_settings_email
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_settings_email')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_settings_email', N'Gestionare Setări Email');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_settings_email')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_settings_email', N'Gestione Impostazioni Email');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_settings_email')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_settings_email', N'Manage Email Settings');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_settings_email')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_settings_email', N'E-Mail-Einstellungen Verwalten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_settings_email')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_settings_email', N'Hantera E-postinställningar');

-- settings_email_window_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'settings_email_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'settings_email_window_title', N'Gestionare Setări Email');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'settings_email_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'settings_email_window_title', N'Gestione Impostazioni Email');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'settings_email_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'settings_email_window_title', N'Email Settings Management');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'settings_email_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'settings_email_window_title', N'E-Mail-Einstellungen Verwaltung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'settings_email_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'settings_email_window_title', N'E-postinställningar Hantering');

-- add_setting_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'add_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'add_setting_title', N'Adaugă Setare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'add_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'add_setting_title', N'Aggiungi Impostazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'add_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'add_setting_title', N'Add Setting');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'add_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'add_setting_title', N'Einstellung Hinzufügen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'add_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'add_setting_title', N'Lägg till Inställning');

-- edit_setting_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'edit_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'edit_setting_title', N'Modifică Setare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'edit_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'edit_setting_title', N'Modifica Impostazione');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'edit_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'edit_setting_title', N'Edit Setting');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'edit_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'edit_setting_title', N'Einstellung Bearbeiten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'edit_setting_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'edit_setting_title', N'Redigera Inställning');

-- attribute_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'attribute_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'attribute_label', N'Atribut');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'attribute_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'attribute_label', N'Attributo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'attribute_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'attribute_label', N'Attribute');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'attribute_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'attribute_label', N'Attribut');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'attribute_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'attribute_label', N'Attribut');

-- last_check_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'last_check_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'last_check_label', N'Ultima Verificare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'last_check_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'last_check_label', N'Ultimo Controllo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'last_check_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'last_check_label', N'Last Check');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'last_check_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'last_check_label', N'Letzte Prüfung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'last_check_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'last_check_label', N'Senaste kontroll');

-- last_check_auto_update
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'last_check_auto_update')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'last_check_auto_update', N'Câmpul "Ultima Verificare" va fi actualizat automat la salvare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'last_check_auto_update')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'last_check_auto_update', N'Il campo "Ultimo Controllo" verrà aggiornato automaticamente al salvataggio');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'last_check_auto_update')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'last_check_auto_update', N'The "Last Check" field will be automatically updated on save');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'last_check_auto_update')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'last_check_auto_update', N'Das Feld "Letzte Prüfung" wird beim Speichern automatisch aktualisiert');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'last_check_auto_update')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'last_check_auto_update', N'Fältet "Senaste kontroll" uppdateras automatiskt vid sparande');

-- Messages
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'setting_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'setting_saved_success', N'Setare salvată cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'setting_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'setting_saved_success', N'Impostazione salvata con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'setting_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'setting_saved_success', N'Setting saved successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'setting_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'setting_saved_success', N'Einstellung erfolgreich gespeichert');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'setting_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'setting_saved_success', N'Inställning sparad framgångsrikt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'setting_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'setting_deleted_success', N'Setare ștearsă cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'setting_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'setting_deleted_success', N'Impostazione eliminata con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'setting_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'setting_deleted_success', N'Setting deleted successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'setting_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'setting_deleted_success', N'Einstellung erfolgreich gelöscht');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'setting_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'setting_deleted_success', N'Inställning raderad framgångsrikt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'confirm_delete_setting')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'confirm_delete_setting', N'Confirmați ștergerea setării?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'confirm_delete_setting')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'confirm_delete_setting', N'Confermi eliminazione dell''impostazione?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'confirm_delete_setting')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'confirm_delete_setting', N'Confirm setting deletion?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'confirm_delete_setting')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'confirm_delete_setting', N'Löschen der Einstellung bestätigen?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'confirm_delete_setting')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'confirm_delete_setting', N'Bekräfta radering av inställning?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'error_no_attribute')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'error_no_attribute', N'Introduceți un atribut');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'error_no_attribute')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'error_no_attribute', N'Inserisci un attributo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'error_no_attribute')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'error_no_attribute', N'Enter an attribute');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'error_no_attribute')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'error_no_attribute', N'Geben Sie ein Attribut ein');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'error_no_attribute')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'error_no_attribute', N'Ange ett attribut');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'error_no_value')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'error_no_value', N'Introduceți o valoare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'error_no_value')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'error_no_value', N'Inserisci un valore');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'error_no_value')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'error_no_value', N'Enter a value');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'error_no_value')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'error_no_value', N'Geben Sie einen Wert ein');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'error_no_value')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'error_no_value', N'Ange ett värde');

GO

PRINT 'Traduzioni per gestione impostazioni email aggiunte con successo!';
PRINT 'Totale chiavi di traduzione: 12';
PRINT 'Totale lingue: 5 (RO, IT, EN, DE, SV)';
PRINT 'Totale record inseriti: 60';
