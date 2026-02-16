-- Script per inserire traduzioni gestione famiglie NPI
-- Lingue: it, en, ro, de, sv

-- Tab titles and UI elements
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    -- Tab titles
    (N'it', N'tab_families_title', N'Famiglie'),
    (N'en', N'tab_families_title', N'Families'),
    (N'ro', N'tab_families_title', N'Familii'),
    (N'de', N'tab_families_title', N'Familien'),
    (N'sv', N'tab_families_title', N'Familjer'),
    
    (N'it', N'tab_family_links_title', N'Collegamenti Famiglie'),
    (N'en', N'tab_family_links_title', N'Family Links'),
    (N'ro', N'tab_family_links_title', N'Legături Familii'),
    (N'de', N'tab_family_links_title', N'Familienverknüpfungen'),
    (N'sv', N'tab_family_links_title', N'Familjelänkar'),
    
    -- Family Management Frame
    (N'it', N'family_list_title', N'Famiglie'),
    (N'en', N'family_list_title', N'Families'),
    (N'ro', N'family_list_title', N'Familii'),
    (N'de', N'family_list_title', N'Familien'),
    (N'sv', N'family_list_title', N'Familjer'),
    
    (N'it', N'family_details_title', N'Dettagli Famiglia'),
    (N'en', N'family_details_title', N'Family Details'),
    (N'ro', N'family_details_title', N'Detalii Familie'),
    (N'de', N'family_details_title', N'Familiendetails'),
    (N'sv', N'family_details_title', N'Familjedetaljer'),
    
    (N'it', N'label_family_name', N'Nome Famiglia:'),
    (N'en', N'label_family_name', N'Family Name:'),
    (N'ro', N'label_family_name', N'Nume Familie:'),
    (N'de', N'label_family_name', N'Familienname:'),
    (N'sv', N'label_family_name', N'Familjenamn:'),
    
    (N'it', N'col_family_name', N'Nome Famiglia'),
    (N'en', N'col_family_name', N'Family Name'),
    (N'ro', N'col_family_name', N'Nume Familie'),
    (N'de', N'col_family_name', N'Familienname'),
    (N'sv', N'col_family_name', N'Familjenamn'),
    
    -- Messages
    (N'it', N'family_name_required', N'Il nome della famiglia è obbligatorio'),
    (N'en', N'family_name_required', N'Family name is required'),
    (N'ro', N'family_name_required', N'Numele familiei este obligatoriu'),
    (N'de', N'family_name_required', N'Familienname ist erforderlich'),
    (N'sv', N'family_name_required', N'Familjenamn krävs'),
    
    (N'it', N'family_created', N'Famiglia creata con successo'),
    (N'en', N'family_created', N'Family created successfully'),
    (N'ro', N'family_created', N'Familie creată cu succes'),
    (N'de', N'family_created', N'Familie erfolgreich erstellt'),
    (N'sv', N'family_created', N'Familj skapad'),
    
    (N'it', N'family_updated', N'Famiglia aggiornata con successo'),
    (N'en', N'family_updated', N'Family updated successfully'),
    (N'ro', N'family_updated', N'Familie actualizată cu succes'),
    (N'de', N'family_updated', N'Familie erfolgreich aktualisiert'),
    (N'sv', N'family_updated', N'Familj uppdaterad'),
    
    (N'it', N'family_deleted', N'Famiglia eliminata con successo'),
    (N'en', N'family_deleted', N'Family deleted successfully'),
    (N'ro', N'family_deleted', N'Familie ștearsă cu succes'),
    (N'de', N'family_deleted', N'Familie erfolgreich gelöscht'),
    (N'sv', N'family_deleted', N'Familj borttagen'),
    
    (N'it', N'confirm_delete_family', N'Sei sicuro di voler eliminare questa famiglia?'),
    (N'en', N'confirm_delete_family', N'Are you sure you want to delete this family?'),
    (N'ro', N'confirm_delete_family', N'Sigur doriți să ștergeți această familie?'),
    (N'de', N'confirm_delete_family', N'Möchten Sie diese Familie wirklich löschen?'),
    (N'sv', N'confirm_delete_family', N'Är du säker på att du vill ta bort denna familj?'),
    
    (N'it', N'select_family_first', N'Seleziona prima una famiglia'),
    (N'en', N'select_family_first', N'Please select a family first'),
    (N'ro', N'select_family_first', N'Selectați mai întâi o familie'),
    (N'de', N'select_family_first', N'Bitte wählen Sie zuerst eine Familie'),
    (N'sv', N'select_family_first', N'Välj en familj först'),
    
    -- Family Links Frame
    (N'it', N'select_family_title', N'Seleziona Famiglia'),
    (N'en', N'select_family_title', N'Select Family'),
    (N'ro', N'select_family_title', N'Selectați Familie'),
    (N'de', N'select_family_title', N'Familie auswählen'),
    (N'sv', N'select_family_title', N'Välj Familj'),
    
    (N'it', N'label_family', N'Famiglia:'),
    (N'en', N'label_family', N'Family:'),
    (N'ro', N'label_family', N'Familie:'),
    (N'de', N'label_family', N'Familie:'),
    (N'sv', N'label_family', N'Familj:'),
    
    (N'it', N'linked_tasks_title', N'Task Collegati'),
    (N'en', N'linked_tasks_title', N'Linked Tasks'),
    (N'ro', N'linked_tasks_title', N'Sarcini Legate'),
    (N'de', N'linked_tasks_title', N'Verknüpfte Aufgaben'),
    (N'sv', N'linked_tasks_title', N'Länkade Uppgifter'),
    
    (N'it', N'available_tasks_title', N'Task Disponibili'),
    (N'en', N'available_tasks_title', N'Available Tasks'),
    (N'ro', N'available_tasks_title', N'Sarcini Disponibile'),
    (N'de', N'available_tasks_title', N'Verfügbare Aufgaben'),
    (N'sv', N'available_tasks_title', N'Tillgängliga Uppgifter'),
    
    (N'it', N'btn_link', N'Collega'),
    (N'en', N'btn_link', N'Link'),
    (N'ro', N'btn_link', N'Leagă'),
    (N'de', N'btn_link', N'Verknüpfen'),
    (N'sv', N'btn_link', N'Länka'),
    
    (N'it', N'btn_unlink', N'Scollega'),
    (N'en', N'btn_unlink', N'Unlink'),
    (N'ro', N'btn_unlink', N'Dezleagă'),
    (N'de', N'btn_unlink', N'Trennen'),
    (N'sv', N'btn_unlink', N'Avlänka'),
    
    (N'it', N'link_created', N'Collegamento creato con successo'),
    (N'en', N'link_created', N'Link created successfully'),
    (N'ro', N'link_created', N'Legătură creată cu succes'),
    (N'de', N'link_created', N'Verknüpfung erfolgreich erstellt'),
    (N'sv', N'link_created', N'Länk skapad'),
    
    (N'it', N'link_deleted', N'Collegamento eliminato con successo'),
    (N'en', N'link_deleted', N'Link deleted successfully'),
    (N'ro', N'link_deleted', N'Legătură ștearsă cu succes'),
    (N'de', N'link_deleted', N'Verknüpfung erfolgreich gelöscht'),
    (N'sv', N'link_deleted', N'Länk borttagen'),
    
    (N'it', N'confirm_unlink_task', N'Sei sicuro di voler scollegare questo task?'),
    (N'en', N'confirm_unlink_task', N'Are you sure you want to unlink this task?'),
    (N'ro', N'confirm_unlink_task', N'Sigur doriți să dezlegați această sarcină?'),
    (N'de', N'confirm_unlink_task', N'Möchten Sie diese Aufgabe wirklich trennen?'),
    (N'sv', N'confirm_unlink_task', N'Är du säker på att du vill avlänka denna uppgift?'),
    
    (N'it', N'select_task_first', N'Seleziona prima un task'),
    (N'en', N'select_task_first', N'Please select a task first'),
    (N'ro', N'select_task_first', N'Selectați mai întâi o sarcină'),
    (N'de', N'select_task_first', N'Bitte wählen Sie zuerst eine Aufgabe'),
    (N'sv', N'select_task_first', N'Välj en uppgift först'),
    
    (N'it', N'select_link_first', N'Seleziona prima un collegamento'),
    (N'en', N'select_link_first', N'Please select a link first'),
    (N'ro', N'select_link_first', N'Selectați mai întâi o legătură'),
    (N'de', N'select_link_first', N'Bitte wählen Sie zuerst eine Verknüpfung'),
    (N'sv', N'select_link_first', N'Välj en länk först')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] t
    WHERE t.[LanguageCode] = Source.[LanguageCode] 
    AND t.[TranslationKey] = Source.[TranslationKey]
);
