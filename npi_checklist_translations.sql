-- ============================================================
-- NPI Checklist Translations
-- Languages: IT, RO (N''), EN, SV, DE
-- ============================================================
USE Traceability_RS
GO

-- btn_checklist
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_checklist')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','btn_checklist','📋 Checklist');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_checklist')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','btn_checklist',N'📋 Checklist');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_checklist')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','btn_checklist','📋 Checklist');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_checklist')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','btn_checklist','📋 Checklista');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_checklist')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','btn_checklist','📋 Checkliste');
GO

-- cl_session
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_session')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_session','Sessione:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_session')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_session',N'Sesiune:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_session')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_session','Session:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_session')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_session','Session:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_session')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_session','Sitzung:');
GO

-- cl_new, cl_save, cl_delete, cl_approve
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_new','➕ Nuova');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_new',N'➕ Nouă');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_new','➕ New');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_new','➕ Ny');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_new','➕ Neu');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_save')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_save','💾 Salva');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_save')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_save',N'💾 Salvează');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_save')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_save','💾 Save');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_save')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_save','💾 Spara');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_save')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_save','💾 Speichern');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_delete','🗑️ Elimina');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_delete',N'🗑️ Șterge');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_delete','🗑️ Delete');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_delete','🗑️ Radera');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_delete','🗑️ Löschen');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_approve','✅ Approva');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_approve',N'✅ Aprobă');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_approve','✅ Approve');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_approve','✅ Godkänn');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_approve','✅ Genehmigen');
GO

-- Tab names
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_tab_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_tab_header','📋 Intestazione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_tab_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_tab_header',N'📋 Antet');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_tab_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_tab_header','📋 Header');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_tab_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_tab_header','📋 Huvud');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_tab_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_tab_header','📋 Kopfzeile');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_tab_smt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_tab_smt','🔧 SMT');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_tab_smt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_tab_smt',N'🔧 SMT');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_tab_smt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_tab_smt','🔧 SMT');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_tab_smt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_tab_smt','🔧 SMT');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_tab_smt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_tab_smt','🔧 SMT');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_tab_pth')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_tab_pth','🔩 PTH');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_tab_pth')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_tab_pth',N'🔩 PTH');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_tab_pth')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_tab_pth','🔩 PTH');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_tab_pth')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_tab_pth','🔩 PTH');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_tab_pth')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_tab_pth','🔩 PTH');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_tab_ict')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_tab_ict','⚡ ICT/FCT/Coating');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_tab_ict')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_tab_ict',N'⚡ ICT/FCT/Coating');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_tab_ict')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_tab_ict','⚡ ICT/FCT/Coating');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_tab_ict')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_tab_ict','⚡ ICT/FCT/Coating');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_tab_ict')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_tab_ict','⚡ ICT/FCT/Coating');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_tab_actions')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_tab_actions','📝 Azioni/Rework');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_tab_actions')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_tab_actions',N'📝 Acțiuni/Rework');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_tab_actions')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_tab_actions','📝 Actions/Rework');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_tab_actions')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_tab_actions','📝 Åtgärder/Omarbetning');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_tab_actions')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_tab_actions','📝 Aktionen/Nacharbeit');
GO

-- cl_saved, cl_header_info, cl_phases, cl_responsabili, cl_date
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_saved')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_saved','Sessione salvata con successo.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_saved')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_saved',N'Sesiune salvată cu succes.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_saved')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_saved','Session saved successfully.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_saved')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_saved','Sessionen sparad.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_saved')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_saved','Sitzung erfolgreich gespeichert.');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_header_info')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_header_info','Informazioni Progetto');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_header_info')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_header_info',N'Informații Proiect');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_header_info')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_header_info','Project Information');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_header_info')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_header_info','Projektinformation');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_header_info')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_header_info','Projektinformation');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_phases')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_phases','Fasi Processo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_phases')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_phases',N'Faze Proces');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_phases')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_phases','Process Phases');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_phases')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_phases','Processfaser');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_phases')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_phases','Prozessphasen');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_responsabili')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_responsabili','Responsabili');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_responsabili')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_responsabili',N'Responsabili');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_responsabili')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_responsabili','Responsible Persons');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_responsabili')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_responsabili','Ansvariga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_responsabili')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_responsabili','Verantwortliche');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='cl_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','cl_date','Data:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='cl_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','cl_date',N'Dată:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='cl_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','cl_date','Date:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='cl_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','cl_date','Datum:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='cl_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','cl_date','Datum:');
GO

PRINT '✅ Traduzioni NPI Checklist completate'
GO
