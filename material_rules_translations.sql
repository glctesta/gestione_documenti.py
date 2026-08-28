-- ============================================================================
-- Traduzioni per finestra Gestione Regole Materiali (scorie/rientri)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-08-28
-- ============================================================================

-- submenu_material_rules
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_material_rules' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_material_rules', 'Regole Scorie/Rientri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_material_rules' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_material_rules', 'Scrap/Return Rules');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_material_rules' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_material_rules', N'Reguli Deșeuri/Reveniri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_material_rules' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_material_rules', 'Regeln für Schrott/Rückläufe');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_material_rules' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_material_rules', 'Regler för skrot/returer');

-- material_rules_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_title', 'Gestione Regole Materiali');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_title', 'Material Rules Management');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_title', N'Gestionare Reguli Materiale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_title', 'Verwaltung von Materialregeln');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_title', 'Hantering av materialregler');

-- material_rules_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_header', 'Definisci quali materiali richiedono una consegna/scoria');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_header', 'Define which materials require a scrap/return delivery');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_header', N'Definiți materialele care necesită o livrare de deșeu/returnare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_header', 'Definieren Sie Materialien, die eine Schrott-/Rücklauflieferung erfordern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_header', 'Definiera material som kräver en skrot-/returleverans');

-- material_rules_new
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_new' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_new', 'Nuova regola');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_new' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_new', 'New rule');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_new' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_new', N'Regulă nouă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_new' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_new', 'Neue Regel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_new' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_new', 'Ny regel');

-- material_rules_requested
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_requested' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_requested', 'Materiale richiesto:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_requested' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_requested', 'Requested material:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_requested' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_requested', N'Material solicitat:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_requested' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_requested', 'Angefordertes Material:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_requested' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_requested', 'Begärt material:');

-- material_rules_scrap
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_scrap' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_scrap', 'Materiale scoria richiesto:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_scrap' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_scrap', 'Required scrap material:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_scrap' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_scrap', N'Material deșeu necesar:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_scrap' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_scrap', 'Erforderliches Schrottmaterial:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_scrap' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_scrap', 'Skrotmaterial som krävs:');

-- material_rules_add
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_add', 'Aggiungi regola');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_add', 'Add rule');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_add', N'Adaugă regulă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_add', 'Regel hinzufügen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_add', 'Lägg till regel');

-- material_rules_col_req_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_code' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_col_req_code', 'Cod. richiesto');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_code' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_col_req_code', 'Req. code');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_code' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_col_req_code', N'Cod. solicitat');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_code' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_col_req_code', 'Anfr. Code');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_code' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_col_req_code', 'Beg. kod');

-- material_rules_col_req_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_desc' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_col_req_desc', 'Descrizione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_desc' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_col_req_desc', 'Description');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_desc' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_col_req_desc', N'Descriere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_desc' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_col_req_desc', 'Beschreibung');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_req_desc' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_col_req_desc', 'Beskrivning');

-- material_rules_col_scrap_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_code' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_col_scrap_code', 'Cod. scoria');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_code' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_col_scrap_code', 'Scrap code');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_code' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_col_scrap_code', N'Cod. deșeu');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_code' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_col_scrap_code', 'Schrottcode');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_code' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_col_scrap_code', 'Skrotkod');

-- material_rules_col_scrap_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_desc' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_col_scrap_desc', 'Descrizione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_desc' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_col_scrap_desc', 'Description');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_desc' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_col_scrap_desc', N'Descriere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_desc' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_col_scrap_desc', 'Beschreibung');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_col_scrap_desc' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_col_scrap_desc', 'Beskrivning');

-- material_rules_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_delete', 'Elimina regola selezionata');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_delete', 'Delete selected rule');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_delete', N'Șterge regula selectată');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_delete', 'Ausgewählte Regel löschen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_delete', 'Ta bort vald regel');

-- material_rules_loaded
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_loaded' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_loaded', 'regole attive');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_loaded' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_loaded', 'active rules');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_loaded' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_loaded', N'reguli active');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_loaded' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_loaded', 'aktive Regeln');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_loaded' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_loaded', 'aktiva regler');

-- material_rules_load_err
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_load_err' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_load_err', 'Errore caricamento');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_load_err' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_load_err', 'Loading error');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_load_err' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_load_err', N'Eroare la încărcare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_load_err' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_load_err', 'Ladefehler');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_load_err' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_load_err', 'Inläsningsfel');

-- material_rules_select_requested
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_requested' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_select_requested', 'Seleziona il materiale richiesto.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_requested' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_select_requested', 'Please select the requested material.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_requested' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_select_requested', N'Selectați materialul solicitat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_requested' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_select_requested', 'Bitte wählen Sie das angeforderte Material aus.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_requested' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_select_requested', 'Välj det begärda materialet.');

-- material_rules_select_scrap
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_scrap' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_select_scrap', 'Seleziona il materiale scoria richiesto.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_scrap' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_select_scrap', 'Please select the required scrap material.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_scrap' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_select_scrap', N'Selectați materialul deșeu necesar.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_scrap' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_select_scrap', 'Bitte wählen Sie das erforderliche Schrottmaterial aus.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_scrap' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_select_scrap', 'Välj det nödvändiga skrotmaterialet.');

-- material_rules_same_material
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_same_material' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_same_material', 'Il materiale richiesto e quello scoria devono essere diversi.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_same_material' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_same_material', 'The requested material and the scrap material must be different.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_same_material' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_same_material', N'Materialul solicitat și materialul deșeu trebuie să fie diferite.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_same_material' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_same_material', 'Das angeforderte Material und das Schrottmaterial müssen unterschiedlich sein.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_same_material' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_same_material', 'Det begärda materialet och skrotmaterialet måste vara olika.');

-- material_rules_exists
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_exists' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_exists', 'Esiste già una regola attiva per questo materiale.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_exists' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_exists', 'An active rule already exists for this material.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_exists' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_exists', N'Există deja o regulă activă pentru acest material.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_exists' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_exists', 'Für dieses Material existiert bereits eine aktive Regel.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_exists' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_exists', 'Det finns redan en aktiv regel för detta material.');

-- material_rules_select_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_select_delete', 'Seleziona una regola da eliminare.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_select_delete', 'Please select a rule to delete.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_select_delete', N'Selectați o regulă de șters.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_select_delete', 'Bitte wählen Sie eine zu löschende Regel aus.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_select_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_select_delete', 'Välj en regel att ta bort.');

-- material_rules_confirm_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_confirm_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_confirm_delete', 'Confermi l\'eliminazione della regola selezionata?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_confirm_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_confirm_delete', 'Confirm deletion of the selected rule?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_confirm_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_confirm_delete', N'Confirmați ștergerea regulii selectate?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_confirm_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_confirm_delete', 'Löschen der ausgewählten Regel bestätigen?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_confirm_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_confirm_delete', 'Bekräfta borttagning av vald regel?');

-- material_rules_add_err
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add_err' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_add_err', 'Errore inserimento regola');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add_err' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_add_err', 'Error adding rule');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add_err' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_add_err', N'Eroare la adăugarea regulii');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add_err' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_add_err', 'Fehler beim Hinzufügen der Regel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_add_err' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_add_err', 'Fel vid tillägg av regel');

-- material_rules_delete_err
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete_err' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'material_rules_delete_err', 'Errore eliminazione regola');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete_err' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'material_rules_delete_err', 'Error deleting rule');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete_err' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'material_rules_delete_err', N'Eroare la ștergerea regulii');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete_err' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'material_rules_delete_err', 'Fehler beim Löschen der Regel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'material_rules_delete_err' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'material_rules_delete_err', 'Fel vid borttagning av regel');

PRINT 'Traduzioni Gestione Regole Materiali inserite con successo.';
