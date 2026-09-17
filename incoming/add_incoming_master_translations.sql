-- Script SQL per le traduzioni del master ticket e del report Ricezione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-09-16
-- Chiavi master: incoming_setup_master_frame, incoming_setup_master_hint,
--                inc_sol_master_view, inc_sol_limited_view, inc_sol_no_types
-- Chiavi report: incoming_menu_report, inc_rep_title, inc_rep_filter_*,
--                inc_rep_status_*, inc_rep_search, inc_rep_export, inc_rep_col_*

USE [Traceability_RS];
GO

-- ============================================================================
-- incoming_setup_master_frame
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'incoming_setup_master_frame')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_setup_master_frame', N'Master ticket (vede tutti i ticket aperti)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'incoming_setup_master_frame')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_setup_master_frame', N'Ticket master (sees all open tickets)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'incoming_setup_master_frame')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_setup_master_frame', N'Master tichet (vede toate tichetele deschise)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'incoming_setup_master_frame')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_setup_master_frame', N'Ticket-Master (sieht alle offenen Tickets)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'incoming_setup_master_frame')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_setup_master_frame', N'Ticketmaster (ser alla öppna ärenden)');
END

-- ============================================================================
-- incoming_setup_master_hint
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'incoming_setup_master_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_setup_master_hint', N'Email degli utenti abilitati a vedere tutti i ticket, indipendentemente dai destinatari configurati per tipo.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'incoming_setup_master_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_setup_master_hint', N'Email addresses allowed to see all tickets, regardless of the per-type recipients.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'incoming_setup_master_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_setup_master_hint', N'Adresele de email care pot vedea toate tichetele, indiferent de destinatarii configurați pe tip.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'incoming_setup_master_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_setup_master_hint', N'E-Mail-Adressen mit Zugriff auf alle Tickets, unabhängig von den Empfängern pro Typ.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'incoming_setup_master_hint')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_setup_master_hint', N'E-postadresser som får se alla ärenden, oavsett mottagare per typ.');
END

-- ============================================================================
-- inc_sol_master_view
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_sol_master_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'inc_sol_master_view', N'(master — vista completa)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_sol_master_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'inc_sol_master_view', N'(master — full view)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_sol_master_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'inc_sol_master_view', N'(master — vizualizare completă)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_sol_master_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'inc_sol_master_view', N'(Master — volle Ansicht)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_sol_master_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'inc_sol_master_view', N'(master — full vy)');
END

-- ============================================================================
-- inc_sol_limited_view
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_sol_limited_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'inc_sol_limited_view', N'(solo tipi assegnati)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_sol_limited_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'inc_sol_limited_view', N'(assigned types only)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_sol_limited_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'inc_sol_limited_view', N'(doar tipurile alocate)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_sol_limited_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'inc_sol_limited_view', N'(nur zugewiesene Typen)');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_sol_limited_view')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'inc_sol_limited_view', N'(endast tilldelade typer)');
END

-- ============================================================================
-- inc_sol_no_types
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_sol_no_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'inc_sol_no_types', N'Nessun tipo di richiesta assegnato alla tua email. Contatta il master del modulo.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_sol_no_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'inc_sol_no_types', N'No request type assigned to your email. Contact the module master.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_sol_no_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'inc_sol_no_types', N'Niciun tip de cerere alocat adresei tale de email. Contactează masterul modulului.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_sol_no_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'inc_sol_no_types', N'Kein Anfragetyp deiner E-Mail zugeordnet. Wende dich an den Master des Moduls.');
END
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_sol_no_types')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'inc_sol_no_types', N'Ingen ärendetyp tilldelad din e-post. Kontakta modulens master.');
END
