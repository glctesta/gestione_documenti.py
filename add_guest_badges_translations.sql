-- Traduzioni per Gestione Badges visitatori / non dipendenti
USE [Traceability_RS];
GO

;WITH T AS (
    SELECT * FROM (VALUES
        (N'it', N'gestione_badge_visitatori', N'Gestione Badge Visitatori'),
        (N'en', N'gestione_badge_visitatori', N'Visitor Badge Management'),
        (N'de', N'gestione_badge_visitatori', N'Verwaltung Besucher-Badges'),
        (N'ro', N'gestione_badge_visitatori', N'Gestionare Badge Vizitatori'),
        (N'sv', N'gestione_badge_visitatori', N'Hantering av besökarbrickor'),

        (N'it', N'guest_settings_badges', N'Gestione Badges'),
        (N'en', N'guest_settings_badges', N'Badge Management'),
        (N'de', N'guest_settings_badges', N'Badge-Verwaltung'),
        (N'ro', N'guest_settings_badges', N'Gestionare Badge-uri'),
        (N'sv', N'guest_settings_badges', N'Badgehantering'),

        (N'it', N'guest_badges_title', N'Gestione Badges'),
        (N'en', N'guest_badges_title', N'Guest Badges Management'),
        (N'de', N'guest_badges_title', N'Verwaltung Besucherausweise'),
        (N'ro', N'guest_badges_title', N'Gestionare Badge-uri Vizitatori'),
        (N'sv', N'guest_badges_title', N'Hantering av besöksbrickor'),

        (N'it', N'guest_badges_editor', N'Inserimento / Modifica Badge'),
        (N'en', N'guest_badges_editor', N'Add / Edit Badge'),
        (N'de', N'guest_badges_editor', N'Badge hinzufügen / bearbeiten'),
        (N'ro', N'guest_badges_editor', N'Adăugare / Modificare Badge'),
        (N'sv', N'guest_badges_editor', N'Lägg till / redigera badge'),

        (N'it', N'badge_number', N'Numero Badge'),
        (N'en', N'badge_number', N'Badge Number'),
        (N'de', N'badge_number', N'Badge-Nummer'),
        (N'ro', N'badge_number', N'Număr Badge'),
        (N'sv', N'badge_number', N'Badgenummer'),

        (N'it', N'guest_worker_flag', N'Worker'),
        (N'en', N'guest_worker_flag', N'Worker'),
        (N'de', N'guest_worker_flag', N'Mitarbeiter'),
        (N'ro', N'guest_worker_flag', N'Lucrător'),
        (N'sv', N'guest_worker_flag', N'Arbetare'),

        (N'it', N'confirm_worker_enable', N'Attivare Worker per questo ospite e sincronizzare i dati su Timeclocking?'),
        (N'en', N'confirm_worker_enable', N'Enable Worker for this guest and synchronize data to Timeclocking?'),
        (N'de', N'confirm_worker_enable', N'Worker für diesen Gast aktivieren und Daten mit Timeclocking synchronisieren?'),
        (N'ro', N'confirm_worker_enable', N'Activați Worker pentru acest oaspete și sincronizați datele în Timeclocking?'),
        (N'sv', N'confirm_worker_enable', N'Aktivera Worker för denna gäst och synkronisera data till Timeclocking?'),

        (N'it', N'worker_badge_required', N'Per Worker=1 è obbligatorio assegnare un badge al visitatore.'),
        (N'en', N'worker_badge_required', N'For Worker=1, assigning a badge to the guest is mandatory.'),
        (N'de', N'worker_badge_required', N'Für Worker=1 muss dem Besucher ein Badge zugewiesen werden.'),
        (N'ro', N'worker_badge_required', N'Pentru Worker=1 este obligatorie atribuirea unui badge vizitatorului.'),
        (N'sv', N'worker_badge_required', N'För Worker=1 är det obligatoriskt att tilldela gästen en badge.'),

        (N'it', N'worker_no_active_visit', N'Nessuna visita attiva o futura per questo ospite (Worker).'),
        (N'en', N'worker_no_active_visit', N'No active or future visit found for this guest (Worker).'),
        (N'de', N'worker_no_active_visit', N'Für diesen Gast wurde kein aktiver oder zukünftiger Besuch gefunden (Worker).'),
        (N'ro', N'worker_no_active_visit', N'Nu există nicio vizită activă sau viitoare pentru acest oaspete (Worker).'),
        (N'sv', N'worker_no_active_visit', N'Ingen aktiv eller framtida vistelse hittades för denna gäst (Worker).'),

        (N'it', N'worker_company_required', N'CompanyName mancante per sync Worker.'),
        (N'en', N'worker_company_required', N'CompanyName is missing for Worker sync.'),
        (N'de', N'worker_company_required', N'CompanyName fehlt für die Worker-Synchronisierung.'),
        (N'ro', N'worker_company_required', N'CompanyName lipsește pentru sincronizarea Worker.'),
        (N'sv', N'worker_company_required', N'CompanyName saknas för Worker-synkronisering.'),

        (N'it', N'worker_company_create_failed', N'Creazione Company Timeclocking fallita.'),
        (N'en', N'worker_company_create_failed', N'Failed to create Timeclocking company.'),
        (N'de', N'worker_company_create_failed', N'Erstellen der Timeclocking-Firma fehlgeschlagen.'),
        (N'ro', N'worker_company_create_failed', N'Crearea companiei Timeclocking a eșuat.'),
        (N'sv', N'worker_company_create_failed', N'Skapande av Timeclocking-företag misslyckades.'),

        (N'it', N'badge_number_required', N'Inserire il numero badge.'),
        (N'en', N'badge_number_required', N'Enter the badge number.'),
        (N'de', N'badge_number_required', N'Bitte Badge-Nummer eingeben.'),
        (N'ro', N'badge_number_required', N'Introduceți numărul badge-ului.'),
        (N'sv', N'badge_number_required', N'Ange badge-numret.'),

        (N'it', N'badge_number_exists', N'Questo numero badge esiste già.'),
        (N'en', N'badge_number_exists', N'This badge number already exists.'),
        (N'de', N'badge_number_exists', N'Diese Badge-Nummer existiert bereits.'),
        (N'ro', N'badge_number_exists', N'Acest număr de badge există deja.'),
        (N'sv', N'badge_number_exists', N'Detta badgenummer finns redan.'),

        (N'it', N'badge_saved_ok', N'Badge salvato con successo.'),
        (N'en', N'badge_saved_ok', N'Badge saved successfully.'),
        (N'de', N'badge_saved_ok', N'Badge erfolgreich gespeichert.'),
        (N'ro', N'badge_saved_ok', N'Badge salvat cu succes.'),
        (N'sv', N'badge_saved_ok', N'Badge sparades.'),

        (N'it', N'badge_deleted_ok', N'Badge eliminato con successo.'),
        (N'en', N'badge_deleted_ok', N'Badge deleted successfully.'),
        (N'de', N'badge_deleted_ok', N'Badge erfolgreich gelöscht.'),
        (N'ro', N'badge_deleted_ok', N'Badge șters cu succes.'),
        (N'sv', N'badge_deleted_ok', N'Badge borttaget.'),

        (N'it', N'select_badge', N'Selezionare un badge dalla lista.'),
        (N'en', N'select_badge', N'Select a badge from the list.'),
        (N'de', N'select_badge', N'Bitte einen Badge aus der Liste auswählen.'),
        (N'ro', N'select_badge', N'Selectați un badge din listă.'),
        (N'sv', N'select_badge', N'Välj ett badge från listan.'),

        (N'it', N'badge_delete_blocked', N'Il badge è assegnato a un visitatore e non può essere eliminato.'),
        (N'en', N'badge_delete_blocked', N'The badge is assigned to a visitor and cannot be deleted.'),
        (N'de', N'badge_delete_blocked', N'Der Badge ist einem Besucher zugewiesen und kann nicht gelöscht werden.'),
        (N'ro', N'badge_delete_blocked', N'Badge-ul este atribuit unui vizitator și nu poate fi șters.'),
        (N'sv', N'badge_delete_blocked', N'Badgen är tilldelad en besökare och kan inte tas bort.'),

        (N'it', N'confirm_delete_badge', N'Eliminare il badge selezionato?'),
        (N'en', N'confirm_delete_badge', N'Delete the selected badge?'),
        (N'de', N'confirm_delete_badge', N'Ausgewählten Badge löschen?'),
        (N'ro', N'confirm_delete_badge', N'Ștergeți badge-ul selectat?'),
        (N'sv', N'confirm_delete_badge', N'Ta bort valt badge?'),

        (N'it', N'badge_status_available', N'Disponibile'),
        (N'en', N'badge_status_available', N'Available'),
        (N'de', N'badge_status_available', N'Verfügbar'),
        (N'ro', N'badge_status_available', N'Disponibil'),
        (N'sv', N'badge_status_available', N'Tillgänglig'),

        (N'it', N'badge_status_assigned', N'Assegnato'),
        (N'en', N'badge_status_assigned', N'Assigned'),
        (N'de', N'badge_status_assigned', N'Zugewiesen'),
        (N'ro', N'badge_status_assigned', N'Atribuit'),
        (N'sv', N'badge_status_assigned', N'Tilldelad'),

        (N'it', N'assigned_on', N'Assegnato Il'),
        (N'en', N'assigned_on', N'Assigned On'),
        (N'de', N'assigned_on', N'Zugewiesen am'),
        (N'ro', N'assigned_on', N'Atribuit La'),
        (N'sv', N'assigned_on', N'Tilldelad den'),

        (N'it', N'valid_up_to', N'Valido Fino Al'),
        (N'en', N'valid_up_to', N'Valid Until'),
        (N'de', N'valid_up_to', N'Gültig bis'),
        (N'ro', N'valid_up_to', N'Valabil Până La'),
        (N'sv', N'valid_up_to', N'Giltig till'),

        (N'it', N'guest_badges_loaded', N'Badge caricati: {0}'),
        (N'en', N'guest_badges_loaded', N'Loaded badges: {0}'),
        (N'de', N'guest_badges_loaded', N'Geladene Badges: {0}'),
        (N'ro', N'guest_badges_loaded', N'Badge-uri încărcate: {0}'),
        (N'sv', N'guest_badges_loaded', N'Laddade badges: {0}'),

        (N'it', N'guest_badge_no_active_visit', N'Nessuna visita attiva o futura per questo ospite.'),
        (N'en', N'guest_badge_no_active_visit', N'No active or future visit found for this guest.'),
        (N'de', N'guest_badge_no_active_visit', N'Für diesen Gast wurde kein aktiver oder zukünftiger Besuch gefunden.'),
        (N'ro', N'guest_badge_no_active_visit', N'Nu există nicio vizită activă sau viitoare pentru acest oaspete.'),
        (N'sv', N'guest_badge_no_active_visit', N'Ingen aktiv eller framtida vistelse hittades för denna gäst.'),

        (N'it', N'guest_badge_current_assignment', N'Badge attuale: {0} - valido fino al {1}'),
        (N'en', N'guest_badge_current_assignment', N'Current badge: {0} - valid until {1}'),
        (N'de', N'guest_badge_current_assignment', N'Aktueller Badge: {0} - gültig bis {1}'),
        (N'ro', N'guest_badge_current_assignment', N'Badge curent: {0} - valabil până la {1}'),
        (N'sv', N'guest_badge_current_assignment', N'Aktuellt badge: {0} - giltigt till {1}'),

        (N'it', N'guest_badge_available_hint', N'Seleziona un badge disponibile per il visitatore.'),
        (N'en', N'guest_badge_available_hint', N'Select an available badge for the guest.'),
        (N'de', N'guest_badge_available_hint', N'Wählen Sie einen verfügbaren Badge für den Besucher.'),
        (N'ro', N'guest_badge_available_hint', N'Selectați un badge disponibil pentru vizitator.'),
        (N'sv', N'guest_badge_available_hint', N'Välj ett tillgängligt badge för besökaren.'),

        (N'it', N'select_valid_badge', N'Selezionare un badge valido.'),
        (N'en', N'select_valid_badge', N'Select a valid badge.'),
        (N'de', N'select_valid_badge', N'Bitte einen gültigen Badge auswählen.'),
        (N'ro', N'select_valid_badge', N'Selectați un badge valid.'),
        (N'sv', N'select_valid_badge', N'Välj ett giltigt badge.'),

        (N'it', N'badge_already_assigned', N'Il badge selezionato è già assegnato a un altro visitatore.'),
        (N'en', N'badge_already_assigned', N'The selected badge is already assigned to another guest.'),
        (N'de', N'badge_already_assigned', N'Der ausgewählte Badge ist bereits einem anderen Besucher zugewiesen.'),
        (N'ro', N'badge_already_assigned', N'Badge-ul selectat este deja atribuit altui vizitator.'),
        (N'sv', N'badge_already_assigned', N'Det valda badget är redan tilldelat en annan besökare.'),

        (N'it', N'date_in', N'Data Inserimento'),
        (N'en', N'date_in', N'Created On'),
        (N'de', N'date_in', N'Erstellt am'),
        (N'ro', N'date_in', N'Data Inserării'),
        (N'sv', N'date_in', N'Skapad den')
    ) AS X([LanguageCode], [TranslationKey], [TranslationValue])
)
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT T.[LanguageCode], T.[TranslationKey], T.[TranslationValue]
FROM T
WHERE NOT EXISTS (
    SELECT 1
    FROM [dbo].[AppTranslations] A
    WHERE A.[LanguageCode] = T.[LanguageCode]
      AND A.[TranslationKey] = T.[TranslationKey]
);
GO
