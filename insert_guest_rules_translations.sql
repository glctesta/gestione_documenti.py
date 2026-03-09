-- ============================================================
-- Traduzioni per guest_rules_gui.py (Regole Ospiti)
-- Tabella: Traceability_RS.dbo.AppTranslations
-- ============================================================

-- guest_rules_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_rules_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_rules_title', 'Regole Ospiti — Rapporti Attività');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_rules_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_rules_title', N'Reguli oaspeți — Rapoarte de activitate');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_rules_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_rules_title', 'Guest Rules — Activity Reports');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_rules_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_rules_title', 'Gastregeln — Tätigkeitsberichte');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_rules_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_rules_title', 'Gästregler — Aktivitetsrapporter');

-- tab_config
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='tab_config')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'tab_config', '⚙ Configurazione');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='tab_config')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'tab_config', N'⚙ Configurare');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='tab_config')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'tab_config', '⚙ Configuration');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='tab_config')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'tab_config', '⚙ Konfiguration');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='tab_config')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'tab_config', '⚙ Konfiguration');

-- tab_history
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='tab_history')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'tab_history', '📋 Storico Rapporti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='tab_history')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'tab_history', N'📋 Istoric rapoarte');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='tab_history')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'tab_history', '📋 Report History');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='tab_history')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'tab_history', '📋 Berichtshistorie');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='tab_history')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'tab_history', '📋 Rapporthistorik');

-- config_vr_signatory
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='config_vr_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'config_vr_signatory', 'Firmatario Vandewiele Romania (Chi Richiede)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='config_vr_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'config_vr_signatory', N'Semnatar Vandewiele Romania (Solicitant)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='config_vr_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'config_vr_signatory', 'Vandewiele Romania Signatory (Requester)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='config_vr_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'config_vr_signatory', 'Unterzeichner Vandewiele Romania (Antragsteller)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='config_vr_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'config_vr_signatory', 'Undertecknare Vandewiele Romania (Sökande)');

-- config_ext_signatory
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='config_ext_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'config_ext_signatory', 'Firmatario Società Esterna (Chi Invia)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='config_ext_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'config_ext_signatory', N'Semnatar societate externă (Expeditor)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='config_ext_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'config_ext_signatory', 'External Company Signatory (Sender)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='config_ext_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'config_ext_signatory', 'Unterzeichner Externe Firma (Absender)');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='config_ext_signatory')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'config_ext_signatory', 'Undertecknare Externt Företag (Avsändare)');

-- config_contracts
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='config_contracts')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'config_contracts', 'Contratti Società Fatturanti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='config_contracts')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'config_contracts', N'Contracte societăți facturate');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='config_contracts')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'config_contracts', 'Billing Company Contracts');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='config_contracts')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'config_contracts', 'Verträge abrechnender Firmen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='config_contracts')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'config_contracts', 'Faktureringsföretags kontrakt');

-- lbl_name, lbl_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='lbl_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'lbl_name', 'Nome e Cognome:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='lbl_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'lbl_name', N'Nume și prenume:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='lbl_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'lbl_name', 'Full Name:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='lbl_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'lbl_name', 'Vor- und Nachname:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='lbl_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'lbl_name', 'Fullständigt namn:');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='lbl_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'lbl_title', 'Funzione/Titolo:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='lbl_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'lbl_title', N'Funcție/Titlu:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='lbl_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'lbl_title', 'Function/Title:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='lbl_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'lbl_title', 'Funktion/Titel:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='lbl_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'lbl_title', 'Befattning/Titel:');

-- Buttons and labels
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_save_settings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_save_settings', '💾 Salva Impostazioni');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_save_settings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_save_settings', N'💾 Salvează setările');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_save_settings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_save_settings', '💾 Save Settings');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_save_settings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_save_settings', '💾 Einstellungen speichern');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_save_settings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_save_settings', '💾 Spara inställningar');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_generate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_generate', '🔄 Genera Documenti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_generate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_generate', N'🔄 Generează documente');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_generate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_generate', '🔄 Generate Documents');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_generate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_generate', '🔄 Dokumente generieren');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_generate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_generate', '🔄 Generera dokument');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_send_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_send_email', '📧 Invia Email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_send_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_send_email', N'📧 Trimite email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_send_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_send_email', '📧 Send Email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_send_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_send_email', '📧 E-Mail senden');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_send_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_send_email', '📧 Skicka e-post');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_download_docs')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_download_docs', '📥 Scarica Documenti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_download_docs')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_download_docs', N'📥 Descarcă documente');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_download_docs')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_download_docs', '📥 Download Documents');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_download_docs')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_download_docs', '📥 Dokumente herunterladen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_download_docs')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_download_docs', '📥 Ladda ner dokument');

-- Column headers
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_contract_no')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_contract_no', 'N. Contratto');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_contract_no')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_contract_no', 'Nr. Contract');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_contract_no')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_contract_no', 'Contract No.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_contract_no')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_contract_no', 'Vertragsnr.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_contract_no')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_contract_no', 'Avtalsnr.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_contract_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_contract_date', 'Data Contratto');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_contract_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_contract_date', 'Data contract');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_contract_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_contract_date', 'Contract Date');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_contract_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_contract_date', 'Vertragsdatum');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_contract_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_contract_date', 'Avtalsdatum');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_description')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_description', 'Descrizione');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_description')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_description', 'Descriere');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_description')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_description', 'Description');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_description')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_description', 'Beschreibung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_description')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_description', 'Beskrivning');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_period')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_period', 'Periodo');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_period')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_period', N'Perioadă');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_period')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_period', 'Period');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_period')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_period', 'Zeitraum');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_period')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_period', 'Period');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_report_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_report_date', 'Data Rapporto');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_report_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_report_date', 'Data raport');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_report_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_report_date', 'Report Date');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_report_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_report_date', 'Berichtsdatum');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_report_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_report_date', 'Rapportdatum');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_email_sent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_email_sent', 'Email Inviata');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_email_sent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_email_sent', N'Email trimis');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_email_sent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_email_sent', 'Email Sent');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_email_sent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_email_sent', 'E-Mail gesendet');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_email_sent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_email_sent', 'E-post skickad');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_created')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_created', 'Creato');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_created')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_created', 'Creat');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_created')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_created', 'Created');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_created')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_created', 'Erstellt');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_created')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_created', 'Skapad');

-- Messages
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='settings_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'settings_saved', 'Impostazioni salvate con successo.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='settings_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'settings_saved', N'Setările au fost salvate cu succes.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='settings_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'settings_saved', 'Settings saved successfully.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='settings_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'settings_saved', 'Einstellungen erfolgreich gespeichert.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='settings_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'settings_saved', 'Inställningarna sparades.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='confirm_regenerate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'confirm_regenerate', 'Rigenerare i documenti? I precedenti saranno sovrascritti.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='confirm_regenerate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'confirm_regenerate', N'Regenerați documentele? Cele anterioare vor fi suprascrise.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='confirm_regenerate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'confirm_regenerate', 'Regenerate documents? Previous ones will be overwritten.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='confirm_regenerate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'confirm_regenerate', 'Dokumente neu generieren? Vorherige werden überschrieben.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='confirm_regenerate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'confirm_regenerate', 'Återskapa dokument? Tidigare kommer att skrivas över.');

IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='confirm_send_report')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'confirm_send_report', 'Inviare il rapporto via email?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='confirm_send_report')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'confirm_send_report', N'Trimiteți raportul prin email?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='confirm_send_report')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'confirm_send_report', 'Send the report by email?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='confirm_send_report')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'confirm_send_report', 'Bericht per E-Mail senden?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='confirm_send_report')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'confirm_send_report', 'Skicka rapporten via e-post?');

-- guest_settings_rules (menu)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_settings_rules')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_settings_rules', 'Regole');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_settings_rules')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_settings_rules', 'Reguli');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_settings_rules')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_settings_rules', 'Rules');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_settings_rules')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_settings_rules', 'Regeln');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_settings_rules')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_settings_rules', 'Regler');

PRINT 'Traduzioni guest rules inserite con successo.';
