-- ===================================================================
-- kit_workstation_translations.sql
-- Traduzioni per le postazioni esplicite del flusso Kit Preparation:
--   Formazione Kit            (prefisso chiavi: kit_prep_ws)
--   Ricezione Kit Produzione  (prefisso chiavi: kit_prod_ws)
-- Voci di menu: submenu_confirm_kit_prep_workstation / _prod_
-- Le chiavi generiche (stato, errori) sono condivise con wh_workstation_*.
-- Lingue: it, en, ro, de, sv
-- ===================================================================

-- ───────────────────────── Voci di menu ──────────────────────────

-- menu_kit_preparation_manual (voce nel menu Aiuto > Manuali)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_preparation_manual' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_kit_preparation_manual', N'Preparazione Kit Produzione (Manuale)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_preparation_manual' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_kit_preparation_manual', N'Production Kit Preparation (Manual)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_preparation_manual' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_kit_preparation_manual', N'Pregătire Kit Producție (Manual)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_preparation_manual' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_kit_preparation_manual', N'Produktionskit-Vorbereitung (Handbuch)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_preparation_manual' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_kit_preparation_manual', N'Förberedelse av produktionskit (Manual)');

-- kit_alert_mute (checkbox 'non mostrare in seguito' sull'avviso server down)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_alert_mute' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_alert_mute', 'Non mostrare in seguito questo avviso su questo PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_alert_mute' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_alert_mute', 'Do not show this alert again on this PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_alert_mute' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_alert_mute', N'Nu mai afișa acest avertisment pe acest PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_alert_mute' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_alert_mute', N'Diesen Hinweis auf diesem PC nicht mehr anzeigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_alert_mute' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_alert_mute', N'Visa inte denna varning igen på denna dator');

-- menu_kit_dashboard_web (voce nel menu Kit: apre la dashboard web nel browser)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_dashboard_web' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_kit_dashboard_web', 'Dashboard Web (Produzione)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_dashboard_web' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_kit_dashboard_web', 'Web Dashboard (Production)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_dashboard_web' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_kit_dashboard_web', N'Dashboard Web (Producție)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_dashboard_web' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_kit_dashboard_web', 'Web-Dashboard (Produktion)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kit_dashboard_web' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_kit_dashboard_web', N'Webbpanel (Produktion)');

-- submenu_confirm_kit_prep_workstation
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prep_workstation' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_confirm_kit_prep_workstation', 'Conferma Postazione Formazione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prep_workstation' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_confirm_kit_prep_workstation', 'Confirm Kit Preparation Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prep_workstation' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_confirm_kit_prep_workstation', N'Confirmă Postul de Formare Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prep_workstation' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_confirm_kit_prep_workstation', 'Kit-Vorbereitungsstation bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prep_workstation' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_confirm_kit_prep_workstation', N'Bekräfta Kit-förberedelsestation');

-- submenu_confirm_kit_prod_workstation
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prod_workstation' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_confirm_kit_prod_workstation', 'Conferma Postazione Ricezione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prod_workstation' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_confirm_kit_prod_workstation', 'Confirm Kit Receiving Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prod_workstation' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_confirm_kit_prod_workstation', N'Confirmă Postul de Recepție Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prod_workstation' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_confirm_kit_prod_workstation', 'Kit-Empfangsstation bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_confirm_kit_prod_workstation' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_confirm_kit_prod_workstation', N'Bekräfta Kit-mottagningsstation');

-- ════════════════ Finestra: Formazione Kit (kit_prep_ws) ════════════════

-- kit_prep_ws_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_title', 'Conferma Postazione Formazione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_title', 'Confirm Kit Preparation Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_title', N'Confirmă Postul de Formare Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_title', 'Kit-Vorbereitungsstation bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_title', N'Bekräfta Kit-förberedelsestation');

-- kit_prep_ws_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_header', 'Configurazione Postazione Formazione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_header', 'Kit Preparation Station Configuration');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_header', N'Configurare Post de Formare Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_header', 'Konfiguration Kit-Vorbereitungsstation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_header', N'Konfiguration Kit-förberedelsestation');

-- kit_prep_ws_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_desc' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_desc', N'Questa funzione identifica il computer corrente
come postazione di Formazione Kit.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_desc' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_desc', N'This function identifies the current computer
as a Kit Preparation station.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_desc' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_desc', N'Această funcție identifică computerul curent
ca post de Formare Kit.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_desc' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_desc', N'Diese Funktion identifiziert den aktuellen Computer
als Kit-Vorbereitungsstation.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_desc' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_desc', N'Denna funktion identifierar den aktuella datorn
som en Kit-förberedelsestation.');

-- kit_prep_ws_create
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_create' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_create', 'Attiva Postazione Formazione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_create' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_create', 'Activate Kit Preparation Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_create' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_create', N'Activează Postul de Formare Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_create' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_create', 'Kit-Vorbereitungsstation aktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_create' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_create', N'Aktivera Kit-förberedelsestation');

-- kit_prep_ws_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_delete', 'Disattiva Postazione Formazione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_delete', 'Deactivate Kit Preparation Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_delete', N'Dezactivează Postul de Formare Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_delete', 'Kit-Vorbereitungsstation deaktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_delete', N'Inaktivera Kit-förberedelsestation');

-- kit_prep_ws_active
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_active' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_active', N'✅ Postazione Formazione Kit ATTIVA
Host: {0}
Attivata: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_active' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_active', N'✅ Kit Preparation Station ACTIVE
Host: {0}
Activated: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_active' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_active', N'✅ Post de Formare Kit ACTIV
Host: {0}
Activat: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_active' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_active', N'✅ Kit-Vorbereitungsstation AKTIV
Host: {0}
Aktiviert: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_active' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_active', N'✅ Kit-förberedelsestation AKTIV
Host: {0}
Aktiverad: {1}');

-- kit_prep_ws_inactive
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_inactive' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_inactive', N'❌ Postazione Formazione Kit NON attiva');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_inactive' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_inactive', N'❌ Kit Preparation Station NOT active');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_inactive' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_inactive', N'❌ Post de Formare Kit INACTIV');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_inactive' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_inactive', N'❌ Kit-Vorbereitungsstation NICHT aktiv');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_inactive' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_inactive', N'❌ Kit-förberedelsestation INTE aktiv');

-- kit_prep_ws_created
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_created' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_created', 'Postazione Formazione Kit attivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_created' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_created', 'Kit Preparation Station activated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_created' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_created', N'Post de Formare Kit activat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_created' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_created', 'Kit-Vorbereitungsstation erfolgreich aktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_created' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_created', 'Kit-förberedelsestation aktiverad framgångsrikt.');

-- kit_prep_ws_deleted
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_deleted' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_deleted', 'Postazione Formazione Kit disattivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_deleted' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_deleted', 'Kit Preparation Station deactivated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_deleted' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_deleted', N'Post de Formare Kit dezactivat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_deleted' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_deleted', 'Kit-Vorbereitungsstation erfolgreich deaktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_deleted' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_deleted', N'Kit-förberedelsestation inaktiverad framgångsrikt.');

-- kit_prep_ws_confirm_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_confirm_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prep_ws_confirm_delete', 'Sei sicuro di voler disattivare la Postazione Formazione Kit?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_confirm_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prep_ws_confirm_delete', 'Are you sure you want to deactivate the Kit Preparation Station?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_confirm_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prep_ws_confirm_delete', N'Sigur doriți să dezactivați Postul de Formare Kit?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_confirm_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prep_ws_confirm_delete', N'Möchten Sie die Kit-Vorbereitungsstation wirklich deaktivieren?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prep_ws_confirm_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prep_ws_confirm_delete', N'Är du säker på att du vill inaktivera Kit-förberedelsestationen?');

-- ════════════ Finestra: Ricezione Kit Produzione (kit_prod_ws) ════════════

-- kit_prod_ws_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_title', 'Conferma Postazione Ricezione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_title', 'Confirm Kit Receiving Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_title', N'Confirmă Postul de Recepție Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_title', 'Kit-Empfangsstation bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_title', N'Bekräfta Kit-mottagningsstation');

-- kit_prod_ws_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_header', 'Configurazione Postazione Ricezione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_header', 'Kit Receiving Station Configuration');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_header', N'Configurare Post de Recepție Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_header', 'Konfiguration Kit-Empfangsstation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_header', N'Konfiguration Kit-mottagningsstation');

-- kit_prod_ws_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_desc' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_desc', N'Questa funzione identifica il computer corrente
come postazione di Ricezione Kit in produzione.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_desc' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_desc', N'This function identifies the current computer
as a production Kit Receiving station.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_desc' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_desc', N'Această funcție identifică computerul curent
ca post de Recepție Kit în producție.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_desc' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_desc', N'Diese Funktion identifiziert den aktuellen Computer
als Kit-Empfangsstation in der Produktion.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_desc' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_desc', N'Denna funktion identifierar den aktuella datorn
som en Kit-mottagningsstation i produktionen.');

-- kit_prod_ws_create
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_create' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_create', 'Attiva Postazione Ricezione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_create' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_create', 'Activate Kit Receiving Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_create' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_create', N'Activează Postul de Recepție Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_create' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_create', 'Kit-Empfangsstation aktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_create' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_create', N'Aktivera Kit-mottagningsstation');

-- kit_prod_ws_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_delete', 'Disattiva Postazione Ricezione Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_delete', 'Deactivate Kit Receiving Station');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_delete', N'Dezactivează Postul de Recepție Kit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_delete', 'Kit-Empfangsstation deaktivieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_delete', N'Inaktivera Kit-mottagningsstation');

-- kit_prod_ws_active
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_active' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_active', N'✅ Postazione Ricezione Kit ATTIVA
Host: {0}
Attivata: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_active' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_active', N'✅ Kit Receiving Station ACTIVE
Host: {0}
Activated: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_active' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_active', N'✅ Post de Recepție Kit ACTIV
Host: {0}
Activat: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_active' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_active', N'✅ Kit-Empfangsstation AKTIV
Host: {0}
Aktiviert: {1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_active' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_active', N'✅ Kit-mottagningsstation AKTIV
Host: {0}
Aktiverad: {1}');

-- kit_prod_ws_inactive
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_inactive' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_inactive', N'❌ Postazione Ricezione Kit NON attiva');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_inactive' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_inactive', N'❌ Kit Receiving Station NOT active');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_inactive' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_inactive', N'❌ Post de Recepție Kit INACTIV');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_inactive' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_inactive', N'❌ Kit-Empfangsstation NICHT aktiv');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_inactive' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_inactive', N'❌ Kit-mottagningsstation INTE aktiv');

-- kit_prod_ws_created
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_created' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_created', 'Postazione Ricezione Kit attivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_created' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_created', 'Kit Receiving Station activated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_created' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_created', N'Post de Recepție Kit activat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_created' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_created', 'Kit-Empfangsstation erfolgreich aktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_created' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_created', 'Kit-mottagningsstation aktiverad framgångsrikt.');

-- kit_prod_ws_deleted
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_deleted' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_deleted', 'Postazione Ricezione Kit disattivata con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_deleted' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_deleted', 'Kit Receiving Station deactivated successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_deleted' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_deleted', N'Post de Recepție Kit dezactivat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_deleted' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_deleted', 'Kit-Empfangsstation erfolgreich deaktiviert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_deleted' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_deleted', N'Kit-mottagningsstation inaktiverad framgångsrikt.');

-- kit_prod_ws_confirm_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_confirm_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'kit_prod_ws_confirm_delete', 'Sei sicuro di voler disattivare la Postazione Ricezione Kit?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_confirm_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'kit_prod_ws_confirm_delete', 'Are you sure you want to deactivate the Kit Receiving Station?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_confirm_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'kit_prod_ws_confirm_delete', N'Sigur doriți să dezactivați Postul de Recepție Kit?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_confirm_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'kit_prod_ws_confirm_delete', N'Möchten Sie die Kit-Empfangsstation wirklich deaktivieren?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'kit_prod_ws_confirm_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'kit_prod_ws_confirm_delete', N'Är du säker på att du vill inaktivera Kit-mottagningsstationen?');
