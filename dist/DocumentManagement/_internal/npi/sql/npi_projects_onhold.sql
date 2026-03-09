-- ============================================================
-- Script: npi_projects_onhold.sql
-- Aggiunge la colonna OnHold alla tabella ProgettiNPI
-- e inserisce le traduzioni per il tab Progetti nel setup NPI
-- ============================================================

-- 1. ALTER TABLE: aggiunge colonna OnHold (BIT, default 0)
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'ProgettiNPI'
      AND COLUMN_NAME = 'OnHold'
)
BEGIN
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD [OnHold] BIT NOT NULL DEFAULT 0;
    PRINT 'Colonna OnHold aggiunta a ProgettiNPI';
END
ELSE
    PRINT 'Colonna OnHold già esistente';
GO

-- 2. Traduzioni per il tab Progetti e i controlli OnHold
-- tab_projects_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'tab_projects_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'tab_projects_title', N'Progetti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'tab_projects_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'tab_projects_title', N'Proiecte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'tab_projects_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'tab_projects_title', N'Projects');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'tab_projects_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'tab_projects_title', N'Projekte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'tab_projects_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'tab_projects_title', N'Projekt');

-- btn_toggle_onhold
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'btn_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'btn_toggle_onhold', N'Sospendi / Riattiva');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'btn_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'btn_toggle_onhold', N'Suspendă / Reactivează');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'btn_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'btn_toggle_onhold', N'Suspend / Reactivate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'btn_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'btn_toggle_onhold', N'Aussetzen / Reaktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'btn_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'btn_toggle_onhold', N'Pausa / Återaktivera');

-- onhold_status_on
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'onhold_status_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'onhold_status_on', N'SOSPESO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'onhold_status_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'onhold_status_on', N'SUSPENDAT');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'onhold_status_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'onhold_status_on', N'ON HOLD');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'onhold_status_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'onhold_status_on', N'AUSGESETZT');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'onhold_status_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'onhold_status_on', N'PAUSAD');

-- onhold_status_off
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'onhold_status_off')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'onhold_status_off', N'ATTIVO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'onhold_status_off')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'onhold_status_off', N'ACTIV');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'onhold_status_off')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'onhold_status_off', N'ACTIVE');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'onhold_status_off')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'onhold_status_off', N'AKTIV');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'onhold_status_off')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'onhold_status_off', N'AKTIV');

-- confirm_toggle_onhold
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'confirm_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'confirm_toggle_onhold', N'Impostare il progetto ''{project}'' come {status}?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'confirm_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'confirm_toggle_onhold', N'Setați proiectul ''{project}'' ca {status}?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'confirm_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'confirm_toggle_onhold', N'Set project ''{project}'' as {status}?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'confirm_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'confirm_toggle_onhold', N'Projekt ''{project}'' als {status} setzen?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'confirm_toggle_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'confirm_toggle_onhold', N'Ställ in projekt ''{project}'' som {status}?');

-- show_closed_projects
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'show_closed_projects')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'show_closed_projects', N'Mostra chiusi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'show_closed_projects')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'show_closed_projects', N'Arată închise');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'show_closed_projects')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'show_closed_projects', N'Show closed');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'show_closed_projects')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'show_closed_projects', N'Geschlossene anzeigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'show_closed_projects')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'show_closed_projects', N'Visa stängda');

-- filter_project
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'filter_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'filter_project', N'Filtro progetto:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'filter_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'filter_project', N'Filtru proiect:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'filter_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'filter_project', N'Filter project:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'filter_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'filter_project', N'Projekt filtern:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'filter_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'filter_project', N'Filtrera projekt:');

-- col_onhold
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'col_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'col_onhold', N'Sospeso');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'col_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'col_onhold', N'Suspendat');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'col_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'col_onhold', N'On Hold');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'col_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'col_onhold', N'Ausgesetzt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'col_onhold')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'col_onhold', N'Pausad');

-- warning_select_project
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'warning_select_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'warning_select_project', N'Seleziona un progetto dalla lista.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'warning_select_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'warning_select_project', N'Selectați un proiect din listă.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'warning_select_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'warning_select_project', N'Select a project from the list.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'warning_select_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'warning_select_project', N'Wählen Sie ein Projekt aus der Liste.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'warning_select_project')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'warning_select_project', N'Välj ett projekt från listan.');

PRINT 'Traduzioni OnHold inserite con successo.';
GO
