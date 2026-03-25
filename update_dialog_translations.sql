-- ============================================================
-- Traduzioni per il dialogo di aggiornamento applicazione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, ro, en, sv, de
-- ============================================================

-- update_ready_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_ready_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'update_ready_title', 'Aggiornamento Pronto');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_ready_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'update_ready_title', N'Actualizare Disponibilă');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_ready_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'update_ready_title', 'Update Ready');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_ready_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'update_ready_title', 'Uppdatering Klar');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_ready_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'update_ready_title', 'Update Bereit');
GO

-- update_ready_msg_mandatory
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_ready_msg_mandatory')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'update_ready_msg_mandatory', 'L''aggiornamento è pronto.

Puoi salvare le attività in corso nelle finestre aperte,
poi clicca ''Salva e Aggiorna''.

⚠  L''aggiornamento è obbligatorio e non può essere rimandato.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_ready_msg_mandatory')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'update_ready_msg_mandatory', N'Actualizarea este disponibilă.

Puteți salva activitățile în curs în ferestrele deschise,
apoi faceți clic pe ''Salvează și Actualizează''.

⚠  Actualizarea este obligatorie și nu poate fi amânată.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_ready_msg_mandatory')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'update_ready_msg_mandatory', 'The update is ready.

You can save your work in the open windows,
then click ''Save and Update''.

⚠  This update is mandatory and cannot be postponed.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_ready_msg_mandatory')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'update_ready_msg_mandatory', 'Uppdateringen är klar.

Du kan spara ditt arbete i de öppna fönstren,
klicka sedan på ''Spara och Uppdatera''.

⚠  Denna uppdatering är obligatorisk och kan inte skjutas upp.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_ready_msg_mandatory')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'update_ready_msg_mandatory', 'Das Update ist bereit.

Sie können Ihre Arbeit in den geöffneten Fenstern speichern,
dann klicken Sie auf ''Speichern und Aktualisieren''.

⚠  Dieses Update ist obligatorisch und kann nicht verschoben werden.');
GO

-- update_ready_msg_optional
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_ready_msg_optional')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'update_ready_msg_optional', 'L''aggiornamento è pronto.

Puoi salvare le attività in corso nelle finestre aperte,
poi clicca ''Salva e Aggiorna''.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_ready_msg_optional')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'update_ready_msg_optional', N'Actualizarea este disponibilă.

Puteți salva activitățile în curs în ferestrele deschise,
apoi faceți clic pe ''Salvează și Actualizează''.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_ready_msg_optional')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'update_ready_msg_optional', 'The update is ready.

You can save your work in the open windows,
then click ''Save and Update''.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_ready_msg_optional')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'update_ready_msg_optional', 'Uppdateringen är klar.

Du kan spara ditt arbete i de öppna fönstren,
klicka sedan på ''Spara och Uppdatera''.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_ready_msg_optional')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'update_ready_msg_optional', 'Das Update ist bereit.

Sie können Ihre Arbeit in den geöffneten Fenstern speichern,
dann klicken Sie auf ''Speichern und Aktualisieren''.');
GO

-- update_save_and_update_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_save_and_update_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'update_save_and_update_btn', '💾 Salva e Aggiorna');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_save_and_update_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'update_save_and_update_btn', N'💾 Salvează și Actualizează');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_save_and_update_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'update_save_and_update_btn', '💾 Save and Update');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_save_and_update_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'update_save_and_update_btn', '💾 Spara och Uppdatera');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_save_and_update_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'update_save_and_update_btn', '💾 Speichern und Aktualisieren');
GO

-- update_now_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_now_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'update_now_btn', '⚡ Aggiorna Subito');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_now_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'update_now_btn', N'⚡ Actualizează Acum');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_now_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'update_now_btn', '⚡ Update Now');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_now_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'update_now_btn', '⚡ Uppdatera Nu');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_now_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'update_now_btn', '⚡ Jetzt Aktualisieren');
GO

PRINT '✅ Traduzioni dialogo aggiornamento inserite con successo.';
