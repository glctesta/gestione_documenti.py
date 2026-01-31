-- Script SQL per aggiungere traduzioni per il sistema di Gestione Fixture
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO (Rumeno), IT (Italiano), EN (Inglese), DE (Tedesco), SV (Svedese)

USE [Traceability_RS];
GO

-- ========================================
-- TRADUZIONI PER MENU FIXTURE
-- ========================================

-- Menu principale Fixture
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_fixture', N'Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_fixture', N'Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_fixture', N'Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_fixture', N'Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_fixture', N'Fixture');

-- Sottomenu: Regole Fixture
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_fixture_rules')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_fixture_rules', N'Reguli Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_fixture_rules')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_fixture_rules', N'Regole Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_fixture_rules')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_fixture_rules', N'Fixture Rules');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_fixture_rules')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_fixture_rules', N'Fixture-Regeln');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_fixture_rules')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_fixture_rules', N'Fixture-regler');

-- Sottomenu: Assegnazione prodotti
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'submenu_assign_products_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'submenu_assign_products_fixture', N'Atribuire produse');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'submenu_assign_products_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'submenu_assign_products_fixture', N'Assegnazione prodotti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'submenu_assign_products_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'submenu_assign_products_fixture', N'Product Assignment');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'submenu_assign_products_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'submenu_assign_products_fixture', N'Produktzuweisung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'submenu_assign_products_fixture')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'submenu_assign_products_fixture', N'Produkttilldelning');

-- ========================================
-- TRADUZIONI PER FINESTRA REGOLE FIXTURE
-- ========================================

-- Titolo finestra principale
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'fixture_rules_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'fixture_rules_window_title', N'Gestionare Reguli Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'fixture_rules_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'fixture_rules_window_title', N'Gestione Regole Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'fixture_rules_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'fixture_rules_window_title', N'Fixture Rules Management');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'fixture_rules_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'fixture_rules_window_title', N'Fixture-Regeln Verwaltung');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'fixture_rules_window_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'fixture_rules_window_title', N'Fixture-regler Hantering');

-- Titolo dialog aggiungi
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'add_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'add_fixture_rule_title', N'Adaugă Regulă Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'add_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'add_fixture_rule_title', N'Aggiungi Regola Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'add_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'add_fixture_rule_title', N'Add Fixture Rule');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'add_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'add_fixture_rule_title', N'Fixture-Regel Hinzufügen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'add_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'add_fixture_rule_title', N'Lägg till Fixture-regel');

-- Titolo dialog modifica
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'edit_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'edit_fixture_rule_title', N'Modifică Regulă Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'edit_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'edit_fixture_rule_title', N'Modifica Regola Fixture');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'edit_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'edit_fixture_rule_title', N'Edit Fixture Rule');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'edit_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'edit_fixture_rule_title', N'Fixture-Regel Bearbeiten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'edit_fixture_rule_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'edit_fixture_rule_title', N'Redigera Fixture-regel');

-- ========================================
-- TRADUZIONI PER ETICHETTE CAMPI
-- ========================================

-- Numero di Cicli
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'number_of_cycles_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'number_of_cycles_label', N'Număr de Cicluri');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'number_of_cycles_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'number_of_cycles_label', N'Numero di Cicli');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'number_of_cycles_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'number_of_cycles_label', N'Number of Cycles');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'number_of_cycles_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'number_of_cycles_label', N'Anzahl der Zyklen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'number_of_cycles_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'number_of_cycles_label', N'Antal cykler');

-- Data Scadenza
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'date_out_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'date_out_label', N'Data Expirare');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'date_out_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'date_out_label', N'Data Scadenza');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'date_out_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'date_out_label', N'Expiration Date');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'date_out_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'date_out_label', N'Ablaufdatum');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'date_out_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'date_out_label', N'Utgångsdatum');

-- Numero Documenti
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'documents_count_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'documents_count_label', N'Nr. Documente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'documents_count_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'documents_count_label', N'N° Documenti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'documents_count_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'documents_count_label', N'# Documents');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'documents_count_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'documents_count_label', N'Anz. Dokumente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'documents_count_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'documents_count_label', N'Antal dokument');

-- ========================================
-- TRADUZIONI PER PULSANTI
-- ========================================

-- Pulsante Pulisci filtro
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'clear_filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'clear_filter_button', N'Curăță');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'clear_filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'clear_filter_button', N'Pulisci');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'clear_filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'clear_filter_button', N'Clear');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'clear_filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'clear_filter_button', N'Löschen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'clear_filter_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'clear_filter_button', N'Rensa');

-- Pulsante Gestisci Documenti
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'manage_docs_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'manage_docs_button', N'Gestionează Documente');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'manage_docs_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'manage_docs_button', N'Gestisci Documenti');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'manage_docs_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'manage_docs_button', N'Manage Documents');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'manage_docs_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'manage_docs_button', N'Dokumente Verwalten');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'manage_docs_button')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'manage_docs_button', N'Hantera dokument');

-- ========================================
-- TRADUZIONI PER MESSAGGI
-- ========================================

-- Conferma eliminazione regola
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'confirm_delete_rule', N'Confirmați ștergerea regulii?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'confirm_delete_rule', N'Confermi eliminazione della regola?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'confirm_delete_rule', N'Confirm rule deletion?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'confirm_delete_rule', N'Löschen der Regel bestätigen?');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'confirm_delete_rule', N'Bekräfta radering av regel?');

-- Regola salvata con successo
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'rule_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'rule_saved_success', N'Regulă salvată cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'rule_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'rule_saved_success', N'Regola salvata con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'rule_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'rule_saved_success', N'Rule saved successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'rule_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'rule_saved_success', N'Regel erfolgreich gespeichert');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'rule_saved_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'rule_saved_success', N'Regel sparad framgångsrikt');

-- Regola eliminata con successo
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'rule_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'rule_deleted_success', N'Regulă ștearsă cu succes');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'rule_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'rule_deleted_success', N'Regola eliminata con successo');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'rule_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'rule_deleted_success', N'Rule deleted successfully');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'rule_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'rule_deleted_success', N'Regel erfolgreich gelöscht');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'rule_deleted_success')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'rule_deleted_success', N'Regel raderad framgångsrikt');

-- Errore: nessun tipo equipaggiamento selezionato
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'error_no_equipment_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'error_no_equipment_type', N'Selectați un tip de echipament');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'error_no_equipment_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'error_no_equipment_type', N'Seleziona un tipo di equipaggiamento');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'error_no_equipment_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'error_no_equipment_type', N'Select an equipment type');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'error_no_equipment_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'error_no_equipment_type', N'Wählen Sie einen Gerätetyp');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'error_no_equipment_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'error_no_equipment_type', N'Välj en utrustningstyp');

-- Errore: numero cicli non valido
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'error_invalid_cycles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'error_invalid_cycles', N'Număr de cicluri invalid');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'error_invalid_cycles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'error_invalid_cycles', N'Numero di cicli non valido');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'error_invalid_cycles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'error_invalid_cycles', N'Invalid number of cycles');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'error_invalid_cycles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'error_invalid_cycles', N'Ungültige Anzahl von Zyklen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'error_invalid_cycles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'error_invalid_cycles', N'Ogiltigt antal cykler');

GO

PRINT 'Traduzioni per il sistema Fixture aggiunte con successo!';
PRINT 'Totale chiavi di traduzione: 13';
PRINT 'Totale lingue: 5 (RO, IT, EN, DE, SV)';
PRINT 'Totale record inseriti: 65';
