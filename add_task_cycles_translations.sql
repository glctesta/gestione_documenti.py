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
PRINT 'Lingue: IT, EN, RO, DE, SV';
PRINT '=============================================';

GO
