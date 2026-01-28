-- =============================================
-- Script SQL per aggiungere le traduzioni
-- Modulo: Gestione Voci Task Manutenzione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- =============================================

USE [Traceability_RS];
GO

-- =============================================
-- submenu_manage_task_cycles (Voce Menu)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_manage_task_cycles' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'submenu_manage_task_cycles', N'it', N'Gestione Voci Task');
    PRINT 'Aggiunta traduzione IT per submenu_manage_task_cycles';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_manage_task_cycles' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'submenu_manage_task_cycles', N'en', N'Manage Task Cycles');
    PRINT 'Aggiunta traduzione EN per submenu_manage_task_cycles';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_manage_task_cycles' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'submenu_manage_task_cycles', N'ro', N'Gestionare Cicluri Task');
    PRINT 'Aggiunta traduzione RO per submenu_manage_task_cycles';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_manage_task_cycles' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'submenu_manage_task_cycles', N'de', N'Aufgabenzyklen Verwalten');
    PRINT 'Aggiunta traduzione DE per submenu_manage_task_cycles';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'submenu_manage_task_cycles' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'submenu_manage_task_cycles', N'sv', N'Hantera Uppgiftscykler');
    PRINT 'Aggiunta traduzione SV for submenu_manage_task_cycles';
END

-- =============================================
-- task_cycles_management_title (Titolo Finestra)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'task_cycles_management_title' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'task_cycles_management_title', N'it', N'Gestione Voci Task Manutenzione');
    PRINT 'Aggiunta traduzione IT per task_cycles_management_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'task_cycles_management_title' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'task_cycles_management_title', N'en', N'Maintenance Task Cycles Management');
    PRINT 'Aggiunta traduzione EN per task_cycles_management_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'task_cycles_management_title' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'task_cycles_management_title', N'ro', N'Gestionare Cicluri Task Întreținere');
    PRINT 'Aggiunta traduzione RO per task_cycles_management_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'task_cycles_management_title' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'task_cycles_management_title', N'de', N'Wartungsaufgabenzyklen Verwaltung');
    PRINT 'Aggiunta traduzione DE per task_cycles_management_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'task_cycles_management_title' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'task_cycles_management_title', N'sv', N'Hantering av Underhållsuppgiftscykler');
    PRINT 'Aggiunta traduzione SV per task_cycles_management_title';
END

-- =============================================
-- cycles_list_label (Etichetta Lista)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycles_list_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycles_list_label', N'it', N'Lista Cicli');
    PRINT 'Aggiunta traduzione IT per cycles_list_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycles_list_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycles_list_label', N'en', N'Cycles List');
    PRINT 'Aggiunta traduzione EN per cycles_list_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycles_list_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycles_list_label', N'ro', N'Listă Cicluri');
    PRINT 'Aggiunta traduzione RO per cycles_list_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycles_list_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycles_list_label', N'de', N'Zyklusliste');
    PRINT 'Aggiunta traduzione DE per cycles_list_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycles_list_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycles_list_label', N'sv', N'Cykellista');
    PRINT 'Aggiunta traduzione SV per cycles_list_label';
END

-- =============================================
-- cycle_description_label (Campo Descrizione)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_description_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_description_label', N'it', N'Descrizione (*)');
    PRINT 'Aggiunta traduzione IT per cycle_description_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_description_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_description_label', N'en', N'Description (*)');
    PRINT 'Aggiunta traduzione EN per cycle_description_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_description_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_description_label', N'ro', N'Descriere (*)');
    PRINT 'Aggiunta traduzione RO per cycle_description_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_description_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_description_label', N'de', N'Beschreibung (*)');
    PRINT 'Aggiunta traduzione DE per cycle_description_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_description_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_description_label', N'sv', N'Beskrivning (*)');
    PRINT 'Aggiunta traduzione SV per cycle_description_label';
END

-- =============================================
-- cycle_value_label (Campo Valore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_value_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_value_label', N'it', N'Valore (*)');
    PRINT 'Aggiunta traduzione IT per cycle_value_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_value_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_value_label', N'en', N'Value (*)');
    PRINT 'Aggiunta traduzione EN for cycle_value_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_value_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_value_label', N'ro', N'Valoare (*)');
    PRINT 'Aggiunta traduzione RO per cycle_value_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_value_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_value_label', N'de', N'Wert (*)');
    PRINT 'Aggiunta traduzione DE per cycle_value_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'cycle_value_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'cycle_value_label', N'sv', N'Värde (*)');
    PRINT 'Aggiunta traduzione SV per cycle_value_label';
END

-- =============================================
-- error_cycle_in_use (Messaggio Errore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_cycle_in_use' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_cycle_in_use', N'it', N'Impossibile cancellare: questo ciclo è già utilizzato in task di manutenzione.');
    PRINT 'Aggiunta traduzione IT per error_cycle_in_use';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_cycle_in_use' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_cycle_in_use', N'en', N'Cannot delete: this cycle is already used in maintenance tasks.');
    PRINT 'Aggiunta traduzione EN per error_cycle_in_use';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_cycle_in_use' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_cycle_in_use', N'ro', N'Nu se poate șterge: acest ciclu este deja utilizat în task-uri de întreținere.');
    PRINT 'Aggiunta traduzione RO per error_cycle_in_use';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_cycle_in_use' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_cycle_in_use', N'de', N'Löschen nicht möglich: Dieser Zyklus wird bereits in Wartungsaufgaben verwendet.');
    PRINT 'Aggiunta traduzione DE per error_cycle_in_use';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_cycle_in_use' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_cycle_in_use', N'sv', N'Kan inte radera: denna cykel används redan i underhållsuppgifter.');
    PRINT 'Aggiunta traduzione SV per error_cycle_in_use';
END

-- =============================================
-- ordine_prn_label (Campo Ordine)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'ordine_prn_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'ordine_prn_label', N'it', N'Ordine (*)');
    PRINT 'Aggiunta traduzione IT per ordine_prn_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'ordine_prn_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'ordine_prn_label', N'en', N'Order (*)');
    PRINT 'Aggiunta traduzione EN per ordine_prn_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'ordine_prn_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'ordine_prn_label', N'ro', N'Ordine (*)');
    PRINT 'Aggiunta traduzione RO per ordine_prn_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'ordine_prn_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'ordine_prn_label', N'de', N'Reihenfolge (*)');
    PRINT 'Aggiunta traduzione DE per ordine_prn_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'ordine_prn_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'ordine_prn_label', N'sv', N'Ordning (*)');
    PRINT 'Aggiunta traduzione SV per ordine_prn_label';
END

-- =============================================
-- no_cycle_label (Campo Numero Cicli)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_cycle_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'no_cycle_label', N'it', N'N° Cicli');
    PRINT 'Aggiunta traduzione IT per no_cycle_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_cycle_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'no_cycle_label', N'en', N'N° Cycles');
    PRINT 'Aggiunta traduzione EN per no_cycle_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_cycle_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'no_cycle_label', N'ro', N'Nr. Cicluri');
    PRINT 'Aggiunta traduzione RO per no_cycle_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_cycle_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'no_cycle_label', N'de', N'Anzahl Zyklen');
    PRINT 'Aggiunta traduzione DE per no_cycle_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'no_cycle_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'no_cycle_label', N'sv', N'Antal Cykler');
    PRINT 'Aggiunta traduzione SV per no_cycle_label';
END

-- =============================================
-- is_fixture_label (Checkbox Fixture)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_fixture_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_fixture_label', N'it', N'È per Fixture');
    PRINT 'Aggiunta traduzione IT per is_fixture_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_fixture_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_fixture_label', N'en', N'Is for Fixture');
    PRINT 'Aggiunta traduzione EN per is_fixture_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_fixture_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_fixture_label', N'ro', N'Este pentru Dispozitiv');
    PRINT 'Aggiunta traduzione RO per is_fixture_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_fixture_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_fixture_label', N'de', N'Ist für Vorrichtung');
    PRINT 'Aggiunta traduzione DE per is_fixture_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_fixture_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_fixture_label', N'sv', N'Är för Fixtur');
    PRINT 'Aggiunta traduzione SV per is_fixture_label';
END

-- =============================================
-- is_stensil_label (Checkbox Stencil)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_stensil_label' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_stensil_label', N'it', N'È per Stencil');
    PRINT 'Aggiunta traduzione IT per is_stensil_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_stensil_label' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_stensil_label', N'en', N'Is for Stencil');
    PRINT 'Aggiunta traduzione EN per is_stensil_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_stensil_label' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_stensil_label', N'ro', N'Este pentru Șablon');
    PRINT 'Aggiunta traduzione RO per is_stensil_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_stensil_label' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_stensil_label', N'de', N'Ist für Schablone');
    PRINT 'Aggiunta traduzione DE per is_stensil_label';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'is_stensil_label' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'is_stensil_label', N'sv', N'Är för Stencil');
    PRINT 'Aggiunta traduzione SV per is_stensil_label';
END

-- =============================================
-- header_ordine (Header Treeview)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_ordine' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_ordine', N'it', N'Ord');
    PRINT 'Aggiunta traduzione IT per header_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_ordine' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_ordine', N'en', N'Ord');
    PRINT 'Aggiunta traduzione EN per header_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_ordine' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_ordine', N'ro', N'Ord');
    PRINT 'Aggiunta traduzione RO per header_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_ordine' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_ordine', N'de', N'Ord');
    PRINT 'Aggiunta traduzione DE per header_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_ordine' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_ordine', N'sv', N'Ord');
    PRINT 'Aggiunta traduzione SV per header_ordine';
END

-- =============================================
-- header_flags (Header Treeview)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_flags' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_flags', N'it', N'Flag');
    PRINT 'Aggiunta traduzione IT per header_flags';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_flags' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_flags', N'en', N'Flags');
    PRINT 'Aggiunta traduzione EN per header_flags';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_flags' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_flags', N'ro', N'Indicatori');
    PRINT 'Aggiunta traduzione RO per header_flags';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_flags' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_flags', N'de', N'Flags');
    PRINT 'Aggiunta traduzione DE per header_flags';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_flags' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_flags', N'sv', N'Flaggor');
    PRINT 'Aggiunta traduzione SV per header_flags';
END

-- =============================================
-- error_required_ordine (Messaggio Errore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_ordine' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_ordine', N'it', N'L''ordine di visualizzazione è obbligatorio.');
    PRINT 'Aggiunta traduzione IT per error_required_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_ordine' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_ordine', N'en', N'Display order is required.');
    PRINT 'Aggiunta traduzione EN per error_required_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_ordine' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_ordine', N'ro', N'Ordinea de afișare este obligatorie.');
    PRINT 'Aggiunta traduzione RO per error_required_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_ordine' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_ordine', N'de', N'Anzeigereihenfolge ist erforderlich.');
    PRINT 'Aggiunta traduzione DE per error_required_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_ordine' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_ordine', N'sv', N'Visningsordning krävs.');
    PRINT 'Aggiunta traduzione SV per error_required_ordine';
END

-- =============================================
-- error_invalid_ordine (Messaggio Errore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_ordine' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_ordine', N'it', N'L''ordine deve essere un numero intero.');
    PRINT 'Aggiunta traduzione IT per error_invalid_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_ordine' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_ordine', N'en', N'Order must be an integer.');
    PRINT 'Aggiunta traduzione EN per error_invalid_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_ordine' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_ordine', N'ro', N'Ordinea trebuie să fie un număr întreg.');
    PRINT 'Aggiunta traduzione RO per error_invalid_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_ordine' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_ordine', N'de', N'Reihenfolge muss eine ganze Zahl sein.');
    PRINT 'Aggiunta traduzione DE per error_invalid_ordine';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_ordine' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_ordine', N'sv', N'Ordning måste vara ett heltal.');
    PRINT 'Aggiunta traduzione SV per error_invalid_ordine';
END

-- =============================================
-- error_invalid_no_cycle (Messaggio Errore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_no_cycle' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_no_cycle', N'it', N'Il numero di cicli deve essere un numero intero.');
    PRINT 'Aggiunta traduzione IT per error_invalid_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_no_cycle' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_no_cycle', N'en', N'Number of cycles must be an integer.');
    PRINT 'Aggiunta traduzione EN per error_invalid_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_no_cycle' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_no_cycle', N'ro', N'Numărul de cicluri trebuie să fie un număr întreg.');
    PRINT 'Aggiunta traduzione RO per error_invalid_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_no_cycle' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_no_cycle', N'de', N'Anzahl der Zyklen muss eine ganze Zahl sein.');
    PRINT 'Aggiunta traduzione DE per error_invalid_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_invalid_no_cycle' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_invalid_no_cycle', N'sv', N'Antal cykler måste vara ett heltal.');
    PRINT 'Aggiunta traduzione SV per error_invalid_no_cycle';
END

-- =============================================
-- confirm_deactivate_title (Titolo Conferma)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_title' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_title', N'it', N'Conferma Disattivazione');
    PRINT 'Aggiunta traduzione IT per confirm_deactivate_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_title' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_title', N'en', N'Confirm Deactivation');
    PRINT 'Aggiunta traduzione EN per confirm_deactivate_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_title' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_title', N'ro', N'Confirmă Dezactivarea');
    PRINT 'Aggiunta traduzione RO per confirm_deactivate_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_title' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_title', N'de', N'Deaktivierung Bestätigen');
    PRINT 'Aggiunta traduzione DE per confirm_deactivate_title';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_title' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_title', N'sv', N'Bekräfta Inaktivering');
    PRINT 'Aggiunta traduzione SV per confirm_deactivate_title';
END

-- =============================================
-- confirm_deactivate_message (Messaggio Conferma)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_message' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_message', N'it', N'Sei sicuro di voler disattivare questo ciclo?

Nota: Il ciclo non verrà cancellato ma marcato come disattivato (DateOut).');
    PRINT 'Aggiunta traduzione IT per confirm_deactivate_message';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_message' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_message', N'en', N'Are you sure you want to deactivate this cycle?

Note: The cycle will not be deleted but marked as deactivated (DateOut).');
    PRINT 'Aggiunta traduzione EN per confirm_deactivate_message';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_message' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_message', N'ro', N'Sigur doriți să dezactivați acest ciclu?

Notă: Ciclul nu va fi șters, ci marcat ca dezactivat (DateOut).');
    PRINT 'Aggiunta traduzione RO per confirm_deactivate_message';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_message' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_message', N'de', N'Sind Sie sicher, dass Sie diesen Zyklus deaktivieren möchten?

Hinweis: Der Zyklus wird nicht gelöscht, sondern als deaktiviert markiert (DateOut).');
    PRINT 'Aggiunta traduzione DE per confirm_deactivate_message';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'confirm_deactivate_message' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'confirm_deactivate_message', N'sv', N'Är du säker på att du vill inaktivera denna cykel?

Obs: Cykeln kommer inte att raderas utan markeras som inaktiverad (DateOut).');
    PRINT 'Aggiunta traduzione SV per confirm_deactivate_message';
END

-- =============================================
-- header_no_cycle (Header Treeview)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_no_cycle' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_no_cycle', N'it', N'N°Cicli');
    PRINT 'Aggiunta traduzione IT per header_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_no_cycle' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_no_cycle', N'en', N'N°Cycles');
    PRINT 'Aggiunta traduzione EN per header_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_no_cycle' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_no_cycle', N'ro', N'Nr.Cicluri');
    PRINT 'Aggiunta traduzione RO per header_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_no_cycle' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_no_cycle', N'de', N'Anz.Zyklen');
    PRINT 'Aggiunta traduzione DE per header_no_cycle';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'header_no_cycle' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'header_no_cycle', N'sv', N'Ant.Cykler');
    PRINT 'Aggiunta traduzione SV per header_no_cycle';
END

-- =============================================
-- error_required_no_cycle_when_flag (Messaggio Errore)
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_no_cycle_when_flag' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_no_cycle_when_flag', N'it', N'Il numero di cicli è obbligatorio quando IsFixture o IsStensil è selezionato.');
    PRINT 'Aggiunta traduzione IT per error_required_no_cycle_when_flag';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_no_cycle_when_flag' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_no_cycle_when_flag', N'en', N'Number of cycles is required when IsFixture or IsStensil is selected.');
    PRINT 'Aggiunta traduzione EN per error_required_no_cycle_when_flag';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_no_cycle_when_flag' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_no_cycle_when_flag', N'ro', N'Numărul de cicluri este obligatoriu când IsFixture sau IsStensil este selectat.');
    PRINT 'Aggiunta traduzione RO per error_required_no_cycle_when_flag';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_no_cycle_when_flag' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_no_cycle_when_flag', N'de', N'Anzahl der Zyklen ist erforderlich, wenn IsFixture oder IsStensil ausgewählt ist.');
    PRINT 'Aggiunta traduzione DE per error_required_no_cycle_when_flag';
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'error_required_no_cycle_when_flag' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([TranslationKey], [LanguageCode], [TranslationValue])
    VALUES (N'error_required_no_cycle_when_flag', N'sv', N'Antal cykler krävs när IsFixture eller IsStensil är vald.');
    PRINT 'Aggiunta traduzione SV per error_required_no_cycle_when_flag';
END

-- =============================================
-- Riepilogo
-- =============================================

PRINT '';
PRINT '=============================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni aggiunte per:';
PRINT '  - submenu_manage_task_cycles';
PRINT '  - task_cycles_management_title';
PRINT '  - cycles_list_label';
PRINT '  - cycle_description_label';
PRINT '  - cycle_value_label';
PRINT '  - error_cycle_in_use';
PRINT '  - ordine_prn_label';
PRINT '  - no_cycle_label';
PRINT '  - is_fixture_label';
PRINT '  - is_stensil_label';
PRINT '  - header_ordine';
PRINT '  - header_flags';
PRINT '  - header_no_cycle';
PRINT '  - error_required_ordine';
PRINT '  - error_invalid_ordine';
PRINT '  - error_invalid_no_cycle';
PRINT '  - error_required_no_cycle_when_flag';
PRINT '  - confirm_deactivate_title';
PRINT '  - confirm_deactivate_message';
PRINT 'Lingue: IT, EN, RO, DE, SV';
PRINT '=============================================';

GO
