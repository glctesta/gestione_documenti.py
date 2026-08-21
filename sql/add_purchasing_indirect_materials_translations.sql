-- Traduzioni per gestione conferma acquisti materiali indiretti e WorkStation

-- Menu: Configura WorkStation (sostituisce la vecchia voce Conferma WH WorkStation)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'submenu_workstation_config')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'submenu_workstation_config', N'Configura WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'submenu_workstation_config')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'submenu_workstation_config', N'Configura WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'submenu_workstation_config')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'submenu_workstation_config', N'Configure WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'submenu_workstation_config')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'submenu_workstation_config', N'Arbeitsstation konfigurieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'submenu_workstation_config')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'submenu_workstation_config', N'Konfigurera arbetsstation');

-- Menu: Conferma ordini
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'submenu_purchasing_order_confirmation')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'submenu_purchasing_order_confirmation', N'Confirmare comenzi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'submenu_purchasing_order_confirmation')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'submenu_purchasing_order_confirmation', N'Conferma ordini');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'submenu_purchasing_order_confirmation')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'submenu_purchasing_order_confirmation', N'Confirm orders');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'submenu_purchasing_order_confirmation')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'submenu_purchasing_order_confirmation', N'Bestellungen bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'submenu_purchasing_order_confirmation')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'submenu_purchasing_order_confirmation', N'Bekräfta beställningar');

-- WorkStation config window
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_config_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_config_title', N'Configura WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_config_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_config_title', N'Configura WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_config_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_config_title', N'Configure WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_config_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_config_title', N'Arbeitsstation konfigurieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_config_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_config_title', N'Konfigurera arbetsstation');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_config_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_config_header', N'Configurare WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_config_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_config_header', N'Configurazione WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_config_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_config_header', N'WorkStation Configuration');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_config_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_config_header', N'Arbeitsstation-Konfiguration');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_config_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_config_header', N'Arbetsstationskonfiguration');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_config_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_config_desc', N'Identifica acest computer ca post de primire comenzi (WH) sau ca post de achiziții materiale indirecte.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_config_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_config_desc', N'Identifica questo computer come postazione ricevente ordini (WH) o come postazione acquisti materiali indiretti.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_config_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_config_desc', N'Identify this computer as a warehouse order receiving workstation (WH) or as an indirect materials purchasing workstation.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_config_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_config_desc', N'Identifizieren Sie diesen Computer als Arbeitsstation für Wareneingangsbestellungen (WH) oder als Arbeitsstation für den Einkauf indirekter Materialien.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_config_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_config_desc', N'Identifiera denna dator som en lagerorder-mottagningsarbetsstation (WH) eller som en arbetsstation för inköp av indirekta material.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_type', N'Tip WorkStation:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_type', N'Tipo WorkStation:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_type', N'WorkStation type:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_type', N'Arbeitsstation-Typ:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_type', N'Arbetsstationstyp:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_status_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_status_label', N'Stare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_status_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_status_label', N'Stato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_status_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_status_label', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_status_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_status_label', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_status_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_status_label', N'Status');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_create')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_create', N'Activează WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_create')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_create', N'Attiva WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_create')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_create', N'Activate WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_create')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_create', N'Arbeitsstation aktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_create')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_create', N'Aktivera arbetsstation');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_delete', N'Dezactivează WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_delete', N'Disattiva WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_delete', N'Deactivate WorkStation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_delete', N'Arbeitsstation deaktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_delete', N'Avaktivera arbetsstation');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_active', N'✅ WorkStation ACTIVĂ\nHost: {0}\nActivată: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_active', N'✅ WorkStation ATTIVA\nHost: {0}\nAttivata: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_active', N'✅ WorkStation ACTIVE\nHost: {0}\nActivated: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_active', N'✅ Arbeitsstation AKTIV\nHost: {0}\nAktiviert: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_active', N'✅ Arbetsstation AKTIV\nHost: {0}\nAktiverad: {1}');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_inactive', N'❌ WorkStation NU este activă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_inactive', N'❌ WorkStation NON attiva');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_inactive', N'❌ WorkStation NOT active');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_inactive', N'❌ Arbeitsstation NICHT aktiv');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_inactive', N'❌ Arbetsstation INTE aktiv');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_file_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_file_error', N'⚠️ Fișier prezent dar ilizibil');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_file_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_file_error', N'⚠️ File presente ma non leggibile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_file_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_file_error', N'⚠️ File present but not readable');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_file_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_file_error', N'⚠️ Datei vorhanden, aber nicht lesbar');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_file_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_file_error', N'⚠️ Filen finns men är inte läsbar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_created', N'WorkStation activată cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_created', N'WorkStation attivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_created', N'WorkStation activated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_created', N'Arbeitsstation erfolgreich aktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_created', N'Arbetsstation aktiverad.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_deleted', N'WorkStation dezactivată cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_deleted', N'WorkStation disattivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_deleted', N'WorkStation deactivated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_deleted', N'Arbeitsstation erfolgreich deaktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_deleted', N'Arbetsstation avaktiverad.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_permission_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_permission_error', N'Permisiuni insuficiente.\nRulați aplicația ca Administrator.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_permission_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_permission_error', N'Permessi insufficienti.\nEseguire il programma come Amministratore.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_permission_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_permission_error', N'Insufficient permissions.\nRun the application as Administrator.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_permission_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_permission_error', N'Unzureichende Berechtigungen.\nStarten Sie die Anwendung als Administrator.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_permission_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_permission_error', N'Otillräckliga behörigheter.\nKör programmet som administratör.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_generic_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_generic_error', N'Eroare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_generic_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_generic_error', N'Errore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_generic_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_generic_error', N'Error');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_generic_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_generic_error', N'Fehler');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_generic_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_generic_error', N'Fel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'workstation_confirm_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'workstation_confirm_delete', N'Sunteți sigur că doriți dezactivarea WorkStation?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'workstation_confirm_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'workstation_confirm_delete', N'Sei sicuro di voler disattivare la WorkStation?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'workstation_confirm_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'workstation_confirm_delete', N'Are you sure you want to deactivate the WorkStation?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'workstation_confirm_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'workstation_confirm_delete', N'Sind Sie sicher, dass Sie die Arbeitsstation deaktivieren möchten?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'workstation_confirm_delete')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'workstation_confirm_delete', N'Är du säker på att du vill avaktivera arbetsstationen?');

-- Purchasing popup monitor
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_title', N'Reminder achiziții materiale indirecte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_title', N'Reminder acquisti materiali indiretti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_title', N'Indirect materials purchase reminder');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_title', N'Erinnerung indirekter Materialeinkauf');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_title', N'Påminnelse inköp indirekt material');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_header', N'⚠️ Cereri de achiziție în așteptare ({0} materiale)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_header', N'⚠️ Richieste di acquisto in attesa ({0} materiali)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_header', N'⚠️ Pending purchase requests ({0} materials)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_header', N'⚠️ Ausstehende Kaufanfragen ({0} Materialien)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_header', N'⚠️ Väntande inköpsbegäranden ({0} material)');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_intro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_intro', N'Următoarele materiale indirecte sunt sub stoc minim și necesită o comandă de achiziție.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_intro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_intro', N'I seguenti materiali indiretti sono sotto scorta e richiedono un ordine di acquisto.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_intro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_intro', N'The following indirect materials are below minimum stock and require a purchase order.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_intro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_intro', N'Die folgenden indirekten Materialien sind unter dem Mindestbestand und erfordern eine Bestellung.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_intro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_intro', N'Följande indirekta materialer ligger under minimilager och kräver en beställning.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_date', N'Data trimitere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_date', N'Data invio');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_date', N'Sent date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_date', N'Sendedatum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_date', N'Skickat datum');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_days', N'Zile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_days', N'Giorni');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_days', N'Days');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_days', N'Tage');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_days', N'Dagar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_excel')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_excel', N'Descarcă Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_excel')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_excel', N'Scarica Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_excel')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_excel', N'Download Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_excel')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_excel', N'Excel herunterladen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_excel')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_excel', N'Ladda ner Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_popup_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_popup_close', N'Închide');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_popup_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_popup_close', N'Chiudi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_popup_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_popup_close', N'Close');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_popup_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_popup_close', N'Schließen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_popup_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_popup_close', N'Stäng');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_excel_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_excel_error', N'Eroare export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_excel_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_excel_error', N'Errore esportazione Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_excel_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_excel_error', N'Excel export error');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_excel_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_excel_error', N'Excel-Export-Fehler');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_excel_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_excel_error', N'Excel-exportfel');

-- Order confirmation form
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirmation_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirmation_title', N'Confirmare comenzi materiale indirecte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirmation_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirmation_title', N'Conferma ordini materiali indiretti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirmation_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirmation_title', N'Indirect materials order confirmation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirmation_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirmation_title', N'Bestellbestätigung indirekte Materialien');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirmation_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirmation_title', N'Beställningsbekräftelse indirekt material');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirmation_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirmation_header', N'Introduceți pentru fiecare material cantitatea comandată, numărul PO și data estimată de sosire.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirmation_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirmation_header', N'Inserire per ogni materiale la quantità ordinata, il numero PO e la data prevista arrivo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirmation_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirmation_header', N'Enter for each material the ordered quantity, PO number and expected arrival date.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirmation_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirmation_header', N'Geben Sie für jedes Material die bestellte Menge, die PO-Nummer und das voraussichtliche Ankunftsdatum ein.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirmation_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirmation_header', N'Ange för varje material beställd kvantitet, PO-nummer och förväntat ankomstdatum.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_select', N'Anulează');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_select', N'Annulla');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_select', N'Cancel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_select', N'Stornieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_select', N'Avbryt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_ordered_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_ordered_qty', N'Cantitate comandată');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_ordered_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_ordered_qty', N'Quantità ordinata');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_ordered_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_ordered_qty', N'Ordered qty');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_ordered_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_ordered_qty', N'Bestellte Menge');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_ordered_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_ordered_qty', N'Beställd kvantitet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_po', N'Număr PO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_po', N'Numero PO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_po', N'PO number');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_po', N'PO-Nummer');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_po', N'PO-nummer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_eta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_eta', N'Data sosire');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_eta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_eta', N'Data arrivo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_eta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_eta', N'Arrival date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_eta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_eta', N'Ankunftsdatum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_eta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_eta', N'Ankomstdatum');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_days', N'Zile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_days', N'Giorni');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_days', N'Days');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_days', N'Tage');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_days')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_days', N'Dagar');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_save')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_save', N'Salvează confirmări');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_save')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_save', N'Salva conferme');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_save')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_save', N'Save confirmations');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_save')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_save', N'Bestätigungen speichern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_save')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_save', N'Spara bekräftelser');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_reload')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_reload', N'Actualizează');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_reload')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_reload', N'Aggiorna');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_reload')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_reload', N'Reload');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_reload')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_reload', N'Aktualisieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_reload')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_reload', N'Uppdatera');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_close', N'Închide');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_close', N'Chiudi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_close', N'Close');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_close', N'Schließen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_close')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_close', N'Stäng');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_load_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_load_error', N'Eroare încărcare date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_load_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_load_error', N'Errore caricamento dati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_load_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_load_error', N'Data load error');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_load_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_load_error', N'Fehler beim Laden der Daten');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_load_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_load_error', N'Fel vid inläsning av data');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_none', N'Nu există comenzi de confirmat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_none', N'Nessun ordine da confermare.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_none', N'No orders to confirm.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_none', N'Keine Bestellungen zur Bestätigung.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_none', N'Inga beställningar att bekräfta.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_qty_invalid', N'Cantitate invalidă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_qty_invalid', N'Quantità non valida');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_qty_invalid', N'Invalid quantity');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_qty_invalid', N'Ungültige Menge');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_qty_invalid', N'Ogiltig kvantitet');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_no_changes')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_no_changes', N'Nu există modificări de salvat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_no_changes')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_no_changes', N'Nessuna modifica da salvare.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_no_changes')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_no_changes', N'No changes to save.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_no_changes')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_no_changes', N'Keine Änderungen zu speichern.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_no_changes')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_no_changes', N'Inga ändringar att spara.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_saved', N'Confirmări salvate.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_saved', N'Conferme salvate.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_saved', N'Confirmations saved.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_saved', N'Bestätigungen gespeichert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_saved', N'Bekräftelser sparade.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'purchasing_confirm_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'purchasing_confirm_save_error', N'Eroare salvare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'purchasing_confirm_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'purchasing_confirm_save_error', N'Errore salvataggio');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'purchasing_confirm_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'purchasing_confirm_save_error', N'Save error');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'purchasing_confirm_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'purchasing_confirm_save_error', N'Speicherfehler');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'purchasing_confirm_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'purchasing_confirm_save_error', N'Sparfel');

PRINT 'Traduzioni per gestione acquisti materiali indiretti inserite.';
GO