-- ============================================================
-- Traduzioni per le nuove funzionalità aggiunte in questa sessione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv
-- Generato il: 2026-02-18
-- ============================================================

-- ============================================================
-- 1. SCARTI GUI — ScrapReasonsManagerWindow
-- ============================================================

-- scrap_reasons_mgmt_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'scrap_reasons_mgmt_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'scrap_reasons_mgmt_title', N'Gestione Tipi Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'scrap_reasons_mgmt_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'scrap_reasons_mgmt_title', N'Scrap Types Management');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'scrap_reasons_mgmt_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'scrap_reasons_mgmt_title', N'Gestionare Tipuri Rebut');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'scrap_reasons_mgmt_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'scrap_reasons_mgmt_title', N'Ausschusstypen Verwaltung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'scrap_reasons_mgmt_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'scrap_reasons_mgmt_title', N'Hantering av skrottyper');

-- scrap_reasons_list_label
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'scrap_reasons_list_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'scrap_reasons_list_label', N'Elenco motivi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'scrap_reasons_list_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'scrap_reasons_list_label', N'Reasons list');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'scrap_reasons_list_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'scrap_reasons_list_label', N'Lista motive');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'scrap_reasons_list_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'scrap_reasons_list_label', N'Grundliste');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'scrap_reasons_list_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'scrap_reasons_list_label', N'Lista över orsaker');

-- scrap_reason_label
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'scrap_reason_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'scrap_reason_label', N'Motivo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'scrap_reason_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'scrap_reason_label', N'Reason');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'scrap_reason_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'scrap_reason_label', N'Motiv');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'scrap_reason_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'scrap_reason_label', N'Grund');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'scrap_reason_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'scrap_reason_label', N'Orsak');

-- scrap_use_ref_label  (colonna "Usa rif." + checkbox "Usa riferimenti scheda")
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'scrap_use_ref_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'scrap_use_ref_label', N'Usa riferimenti scheda');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'scrap_use_ref_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'scrap_use_ref_label', N'Use card references');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'scrap_use_ref_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'scrap_use_ref_label', N'Utilizare referințe card');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'scrap_use_ref_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'scrap_use_ref_label', N'Kartenreferenzen verwenden');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'scrap_use_ref_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'scrap_use_ref_label', N'Använd kortreferenser');

-- error_reason_required
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'error_reason_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'error_reason_required', N'Inserire un motivo valido.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'error_reason_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'error_reason_required', N'Please enter a valid reason.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'error_reason_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'error_reason_required', N'Introduceți un motiv valid.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'error_reason_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'error_reason_required', N'Bitte einen gültigen Grund eingeben.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'error_reason_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'error_reason_required', N'Ange en giltig orsak.');

-- warning_select_reason
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'warning_select_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'warning_select_reason', N'Seleziona un motivo da cancellare.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'warning_select_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'warning_select_reason', N'Please select a reason to delete.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'warning_select_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'warning_select_reason', N'Selectați un motiv de șters.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'warning_select_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'warning_select_reason', N'Bitte einen zu löschenden Grund auswählen.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'warning_select_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'warning_select_reason', N'Välj en orsak att ta bort.');

-- confirm_delete_reason
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'confirm_delete_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'confirm_delete_reason', N'Sei sicuro di voler cancellare il motivo selezionato?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'confirm_delete_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'confirm_delete_reason', N'Are you sure you want to delete the selected reason?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'confirm_delete_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'confirm_delete_reason', N'Sigur doriți să ștergeți motivul selectat?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'confirm_delete_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'confirm_delete_reason', N'Sind Sie sicher, dass Sie den ausgewählten Grund löschen möchten?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'confirm_delete_reason')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'confirm_delete_reason', N'Är du säker på att du vill ta bort den valda orsaken?');

-- info_saved_ok
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'info_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'info_saved_ok', N'Salvataggio eseguito.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'info_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'info_saved_ok', N'Saved successfully.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'info_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'info_saved_ok', N'Salvare efectuată.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'info_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'info_saved_ok', N'Erfolgreich gespeichert.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'info_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'info_saved_ok', N'Sparad.');

-- info_deleted_ok
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'info_deleted_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'info_deleted_ok', N'Cancellazione eseguita.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'info_deleted_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'info_deleted_ok', N'Deleted successfully.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'info_deleted_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'info_deleted_ok', N'Ștergere efectuată.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'info_deleted_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'info_deleted_ok', N'Erfolgreich gelöscht.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'info_deleted_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'info_deleted_ok', N'Borttagen.');

-- error_db_operation
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'error_db_operation')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'error_db_operation', N'Errore database.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'error_db_operation')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'error_db_operation', N'Database error.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'error_db_operation')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'error_db_operation', N'Eroare bază de date.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'error_db_operation')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'error_db_operation', N'Datenbankfehler.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'error_db_operation')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'error_db_operation', N'Databasfel.');

-- error_ref_must_be_from_list  (dichiarazione scarto)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'error_ref_must_be_from_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'error_ref_must_be_from_list', N'Selezionare un riferimento dall''elenco.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'error_ref_must_be_from_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'error_ref_must_be_from_list', N'Please select a reference from the list.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'error_ref_must_be_from_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'error_ref_must_be_from_list', N'Selectați o referință din listă.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'error_ref_must_be_from_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'error_ref_must_be_from_list', N'Bitte eine Referenz aus der Liste auswählen.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'error_ref_must_be_from_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'error_ref_must_be_from_list', N'Välj en referens från listan.');

-- new_button_short
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'new_button_short')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'new_button_short', N'Nuovo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'new_button_short')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'new_button_short', N'New');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'new_button_short')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'new_button_short', N'Nou');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'new_button_short')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'new_button_short', N'Neu');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'new_button_short')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'new_button_short', N'Ny');

-- save_button
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'save_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'save_button', N'Salva');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'save_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'save_button', N'Save');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'save_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'save_button', N'Salvează');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'save_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'save_button', N'Speichern');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'save_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'save_button', N'Spara');

-- delete_button
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'delete_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'delete_button', N'Cancella');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'delete_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'delete_button', N'Delete');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'delete_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'delete_button', N'Șterge');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'delete_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'delete_button', N'Löschen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'delete_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'delete_button', N'Ta bort');

-- cancel_button
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'cancel_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'cancel_button', N'Chiudi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'cancel_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'cancel_button', N'Close');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'cancel_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'cancel_button', N'Închide');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'cancel_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'cancel_button', N'Schließen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'cancel_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'cancel_button', N'Stäng');


-- ============================================================
-- 2. NPI CONFIG WINDOW — Pre-check default tasks
-- ============================================================

-- msg_no_default_tasks_precheck
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'msg_no_default_tasks_precheck')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'msg_no_default_tasks_precheck', N'⚠️ Nessuna categoria/task di default configurata.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Il progetto verrà creato SENZA task.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Per aggiungere task di default, vai nella scheda "Default Catalogo" e marca le categorie/task desiderati.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Vuoi procedere comunque con la creazione del progetto vuoto?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'msg_no_default_tasks_precheck')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'msg_no_default_tasks_precheck', N'⚠️ No default categories/tasks configured.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'The project will be created WITHOUT tasks.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'To add default tasks, go to the "Default Catalog" tab and mark the desired categories/tasks.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Do you want to proceed anyway and create an empty project?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'msg_no_default_tasks_precheck')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'msg_no_default_tasks_precheck', N'⚠️ Nicio categorie/sarcină implicită configurată.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Proiectul va fi creat FĂRĂ sarcini.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Pentru a adăuga sarcini implicite, accesați fila "Catalog implicit" și marcați categoriile/sarcinile dorite.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Doriți să continuați oricum cu crearea unui proiect gol?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'msg_no_default_tasks_precheck')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'msg_no_default_tasks_precheck', N'⚠️ Keine Standard-Kategorien/Aufgaben konfiguriert.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Das Projekt wird OHNE Aufgaben erstellt.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Um Standardaufgaben hinzuzufügen, gehen Sie zur Registerkarte "Standard-Katalog" und markieren Sie die gewünschten Kategorien/Aufgaben.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Möchten Sie trotzdem ein leeres Projekt erstellen?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'msg_no_default_tasks_precheck')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'msg_no_default_tasks_precheck', N'⚠️ Inga standardkategorier/uppgifter konfigurerade.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Projektet skapas UTAN uppgifter.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'För att lägga till standarduppgifter, gå till fliken "Standardkatalog" och markera önskade kategorier/uppgifter.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Vill du ändå fortsätta och skapa ett tomt projekt?');

-- msg_no_default_tasks  (messaggio post-creazione)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'msg_no_default_tasks')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'msg_no_default_tasks', N'Nessuna categoria/task default configurata. Progetto creato senza task di default.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'msg_no_default_tasks')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'msg_no_default_tasks', N'No default categories/tasks configured. Project created without default tasks.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'msg_no_default_tasks')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'msg_no_default_tasks', N'Nicio categorie/sarcină implicită configurată. Proiect creat fără sarcini implicite.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'msg_no_default_tasks')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'msg_no_default_tasks', N'Keine Standard-Kategorien/Aufgaben konfiguriert. Projekt ohne Standardaufgaben erstellt.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'msg_no_default_tasks')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'msg_no_default_tasks', N'Inga standardkategorier/uppgifter konfigurerade. Projekt skapat utan standarduppgifter.');

-- msg_project_exists_update
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'msg_project_exists_update')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'msg_project_exists_update', N'Il progetto esiste già. Vuoi aggiornare i dati (owner, descrizione) e aggiungere documenti?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'msg_project_exists_update')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'msg_project_exists_update', N'The project already exists. Do you want to update its data (owner, description) and add documents?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'msg_project_exists_update')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'msg_project_exists_update', N'Proiectul există deja. Doriți să actualizați datele (proprietar, descriere) și să adăugați documente?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'msg_project_exists_update')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'msg_project_exists_update', N'Das Projekt existiert bereits. Möchten Sie die Daten (Eigentümer, Beschreibung) aktualisieren und Dokumente hinzufügen?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'msg_project_exists_update')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'msg_project_exists_update', N'Projektet finns redan. Vill du uppdatera data (ägare, beskrivning) och lägga till dokument?');

-- msg_project_updated
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'msg_project_updated')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'msg_project_updated', N'Progetto aggiornato con successo.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'msg_project_updated')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'msg_project_updated', N'Project updated successfully.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'msg_project_updated')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'msg_project_updated', N'Proiect actualizat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'msg_project_updated')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'msg_project_updated', N'Projekt erfolgreich aktualisiert.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'msg_project_updated')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'msg_project_updated', N'Projekt uppdaterat.');

-- npi_owner_required_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'npi_owner_required_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'npi_owner_required_title', N'Owner Obbligatorio');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'npi_owner_required_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'npi_owner_required_title', N'Owner Required');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'npi_owner_required_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'npi_owner_required_title', N'Proprietar Obligatoriu');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'npi_owner_required_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'npi_owner_required_title', N'Eigentümer Erforderlich');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'npi_owner_required_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'npi_owner_required_title', N'Ägare Krävs');

-- npi_owner_required_message
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'npi_owner_required_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'npi_owner_required_message', N'⚠️ OWNER PROGETTO OBBLIGATORIO' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Non è possibile creare un progetto senza un Owner.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Seleziona un Owner dal menu a tendina prima di salvare.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'npi_owner_required_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'npi_owner_required_message', N'⚠️ PROJECT OWNER REQUIRED' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'A project cannot be created without an Owner.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Please select an Owner from the dropdown before saving.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'npi_owner_required_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'npi_owner_required_message', N'⚠️ PROPRIETAR PROIECT OBLIGATORIU' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Nu se poate crea un proiect fără un Proprietar.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Selectați un Proprietar din meniu înainte de a salva.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'npi_owner_required_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'npi_owner_required_message', N'⚠️ PROJEKTEIGENTÜMER ERFORDERLICH' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Ein Projekt kann nicht ohne Eigentümer erstellt werden.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Bitte wählen Sie vor dem Speichern einen Eigentümer aus der Dropdown-Liste.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'npi_owner_required_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'npi_owner_required_message', N'⚠️ PROJEKTÄGARE KRÄVS' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Ett projekt kan inte skapas utan en ägare.' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Välj en ägare från rullgardinsmenyn innan du sparar.');

-- confirm_unset_default_category  (DefaultCatalogFrame)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'confirm_unset_default_category')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'confirm_unset_default_category', N'Disattivare la categoria di default? Tutti i task di questa categoria verranno azzerati.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'confirm_unset_default_category')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'confirm_unset_default_category', N'Disable the default category? All tasks in this category will be reset.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'confirm_unset_default_category')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'confirm_unset_default_category', N'Dezactivați categoria implicită? Toate sarcinile din această categorie vor fi resetate.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'confirm_unset_default_category')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'confirm_unset_default_category', N'Standardkategorie deaktivieren? Alle Aufgaben dieser Kategorie werden zurückgesetzt.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'confirm_unset_default_category')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'confirm_unset_default_category', N'Inaktivera standardkategorin? Alla uppgifter i denna kategori återställs.');

-- add_defaults  (checkbox label in ProductManagementFrame)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'add_defaults')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'add_defaults', N'Aggiungi defaults');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'add_defaults')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'add_defaults', N'Add defaults');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'add_defaults')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'add_defaults', N'Adaugă implicite');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'add_defaults')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'add_defaults', N'Standards hinzufügen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'add_defaults')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'add_defaults', N'Lägg till standardvärden');

GO
PRINT 'Traduzioni inserite con successo.';

-- ============================================================
-- 3. NPI CONFIG WINDOW — Soft-delete progetto
-- ============================================================

-- btn_delete_npi_project
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'btn_delete_npi_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'btn_delete_npi_project', N'🗑 Elimina Progetto');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'btn_delete_npi_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'btn_delete_npi_project', N'🗑 Delete Project');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'btn_delete_npi_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'btn_delete_npi_project', N'🗑 Șterge Proiect');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'btn_delete_npi_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'btn_delete_npi_project', N'🗑 Projekt löschen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'btn_delete_npi_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'btn_delete_npi_project', N'🗑 Ta bort projekt');

-- confirm_delete_project
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'confirm_delete_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'confirm_delete_project', N'⚠️ Sei sicuro di voler cancellare il progetto NPI?' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Il progetto verrà marcato come eliminato e non sarà più visibile.' + CHAR(13)+CHAR(10) + 'Questa operazione è consentita solo se il progetto non ha task con dati registrati.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'confirm_delete_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'confirm_delete_project', N'⚠️ Are you sure you want to delete the NPI project?' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'The project will be marked as deleted and will no longer be visible.' + CHAR(13)+CHAR(10) + 'This operation is only allowed if the project has no tasks with recorded data.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'confirm_delete_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'confirm_delete_project', N'⚠️ Sigur doriți să ștergeți proiectul NPI?' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Proiectul va fi marcat ca șters și nu va mai fi vizibil.' + CHAR(13)+CHAR(10) + 'Această operație este permisă numai dacă proiectul nu are sarcini cu date înregistrate.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'confirm_delete_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'confirm_delete_project', N'⚠️ Sind Sie sicher, dass Sie das NPI-Projekt löschen möchten?' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Das Projekt wird als gelöscht markiert und ist nicht mehr sichtbar.' + CHAR(13)+CHAR(10) + 'Dieser Vorgang ist nur zulässig, wenn das Projekt keine Aufgaben mit erfassten Daten hat.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'confirm_delete_project')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'confirm_delete_project', N'⚠️ Är du säker på att du vill ta bort NPI-projektet?' + CHAR(13)+CHAR(10) + CHAR(13)+CHAR(10) + 'Projektet markeras som borttaget och visas inte längre.' + CHAR(13)+CHAR(10) + 'Denna åtgärd är endast tillåten om projektet inte har uppgifter med registrerade data.');

-- msg_project_deleted
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'msg_project_deleted')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'msg_project_deleted', N'Progetto eliminato con successo.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'msg_project_deleted')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'msg_project_deleted', N'Project deleted successfully.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'msg_project_deleted')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'msg_project_deleted', N'Proiect șters cu succes.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'msg_project_deleted')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'msg_project_deleted', N'Projekt erfolgreich gelöscht.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'msg_project_deleted')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'msg_project_deleted', N'Projekt borttaget.');

GO
PRINT 'Traduzioni soft-delete progetto inserite con successo.';
