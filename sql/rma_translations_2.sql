-- ============================================================
-- Traduzioni RMA Knowledge Base — PARTE 2 (Tab Inserimento + Messaggi)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv
-- NOTA: Emoji rimosse per compatibilità SQL Server NVARCHAR
-- Generato il: 2026-03-27
-- ============================================================

-- rma_auth_required
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_auth_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_auth_required', N'Accesso riservato. Effettuare il login per inserire nuove soluzioni.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_auth_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_auth_required', N'Restricted access. Please log in to insert new solutions.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_auth_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_auth_required', N'Acces restricționat. Autentificați-vă pentru a adăuga soluții noi.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_auth_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_auth_required', N'Eingeschränkter Zugang. Bitte melden Sie sich an, um neue Lösungen einzufügen.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_auth_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_auth_required', N'Begränsad åtkomst. Logga in för att lägga till nya lösningar.');

-- rma_verify_label
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_verify_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_verify_label', N'Verifica Etichetta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_verify_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_verify_label', N'Verify Label');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_verify_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_verify_label', N'Verificare Etichetă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_verify_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_verify_label', N'Etikett prüfen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_verify_label')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_verify_label', N'Verifiera etikett');

-- rma_verify_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_verify_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_verify_btn', N'Verifica');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_verify_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_verify_btn', N'Verify');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_verify_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_verify_btn', N'Verifică');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_verify_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_verify_btn', N'Prüfen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_verify_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_verify_btn', N'Verifiera');

-- rma_fault_section
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_section', N'Guasto');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_section', N'Fault');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_section', N'Defect');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_section', N'Fehler');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_section', N'Fel');

-- rma_fault_desc
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_desc')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_desc', N'Descrizione Guasto:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_desc')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_desc', N'Fault Description:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_desc')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_desc', N'Descrierea Defectului:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_desc')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_desc', N'Fehlerbeschreibung:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_desc')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_desc', N'Felbeskrivning:');

-- rma_fault_detail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_detail', N'Dettaglio:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_detail', N'Detail:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_detail', N'Detaliu:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_detail', N'Detail:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_detail', N'Detalj:');

-- rma_solution_section
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_solution_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_solution_section', N'Soluzione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_solution_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_solution_section', N'Solution');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_solution_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_solution_section', N'Soluție');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_solution_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_solution_section', N'Lösung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_solution_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_solution_section', N'Lösning');

-- rma_fault_notes
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_notes')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_notes', N'Note Guasto / Soluzione *:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_notes')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_notes', N'Fault Notes / Solution *:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_notes')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_notes', N'Note Defect / Soluție *:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_notes')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_notes', N'Fehlerhinweise / Lösung *:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_notes')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_notes', N'Felanmärkningar / Lösning *:');

-- rma_corrective
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_corrective')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_corrective', N'Azione correttiva:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_corrective')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_corrective', N'Corrective Action:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_corrective')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_corrective', N'Acțiune Corectivă:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_corrective')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_corrective', N'Korrekturmaßnahme:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_corrective')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_corrective', N'Korrigerande åtgärd:');

-- rma_cause_code
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_cause_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_cause_code', N'Codice Causa:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_cause_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_cause_code', N'Cause Code:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_cause_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_cause_code', N'Cod Cauză:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_cause_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_cause_code', N'Ursachencode:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_cause_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_cause_code', N'Orsakskod:');

-- rma_cause_text
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_cause_text')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_cause_text', N'Causa (testo):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_cause_text')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_cause_text', N'Cause (text):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_cause_text')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_cause_text', N'Cauză (text):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_cause_text')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_cause_text', N'Ursache (Text):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_cause_text')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_cause_text', N'Orsak (text):');

-- rma_extra_section
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_extra_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_extra_section', N'Produzione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_extra_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_extra_section', N'Production');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_extra_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_extra_section', N'Producție');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_extra_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_extra_section', N'Produktion');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_extra_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_extra_section', N'Produktion');

-- rma_warranty
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_warranty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_warranty', N'Garanzia:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_warranty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_warranty', N'Warranty:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_warranty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_warranty', N'Garanție:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_warranty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_warranty', N'Garantie:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_warranty')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_warranty', N'Garanti:');

-- rma_site
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_site')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_site', N'Sito Produzione:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_site')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_site', N'Production Site:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_site')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_site', N'Loc Producție:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_site')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_site', N'Produktionsstandort:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_site')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_site', N'Produktionsplats:');

-- rma_resp
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_resp')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_resp', N'Resp. Processo:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_resp')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_resp', N'Process Responsible:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_resp')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_resp', N'Responsabil Proces:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_resp')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_resp', N'Prozessverantwortlicher:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_resp')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_resp', N'Processansvarig:');

-- rma_repair_time
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_repair_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_repair_time', N'Tempo (min):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_repair_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_repair_time', N'Time (min):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_repair_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_repair_time', N'Timp (min):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_repair_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_repair_time', N'Zeit (Min):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_repair_time')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_repair_time', N'Tid (min):');

-- rma_attach_section
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_attach_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_attach_section', N'Allegati');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_attach_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_attach_section', N'Attachments');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_attach_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_attach_section', N'Atașamente');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_attach_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_attach_section', N'Anhänge');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_attach_section')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_attach_section', N'Bilagor');

-- rma_photo
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_photo', N'Foto difetto:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_photo', N'Defect photo:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_photo', N'Foto defect:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_photo', N'Fehlerfoto:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_photo', N'Felfoto:');

-- rma_browse
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_browse')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_browse', N'Sfoglia');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_browse')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_browse', N'Browse');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_browse')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_browse', N'Răsfoiește');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_browse')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_browse', N'Durchsuchen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_browse')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_browse', N'Bläddra');

-- rma_doc_links
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_doc_links')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_doc_links', N'Link documenti:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_doc_links')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_doc_links', N'Document links:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_doc_links')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_doc_links', N'Linkuri documente:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_doc_links')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_doc_links', N'Dokumentenlinks:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_doc_links')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_doc_links', N'Dokumentlänkar:');

-- rma_save
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_save')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_save', N'Salva');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_save')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_save', N'Save');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_save')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_save', N'Salvează');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_save')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_save', N'Speichern');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_save')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_save', N'Spara');

-- rma_clear
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_clear')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_clear', N'Pulisci');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_clear')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_clear', N'Clear');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_clear')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_clear', N'Curăță');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_clear')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_clear', N'Leeren');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_clear')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_clear', N'Rensa');

-- rma_select_photo
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_select_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_select_photo', N'Seleziona foto difetto');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_select_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_select_photo', N'Select defect photo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_select_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_select_photo', N'Selectați foto defect');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_select_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_select_photo', N'Fehlerfoto auswählen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_select_photo')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_select_photo', N'Välj felfoto');

-- rma_serial_required
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_serial_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_serial_required', N'Il Serial Number è obbligatorio.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_serial_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_serial_required', N'Serial Number is required.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_serial_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_serial_required', N'Numărul Serial este obligatoriu.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_serial_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_serial_required', N'Seriennummer ist erforderlich.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_serial_required')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_serial_required', N'Serienummer krävs.');

-- rma_saved_ok
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_saved_ok', N'Soluzione RMA salvata con successo.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_saved_ok', N'RMA solution saved successfully.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_saved_ok', N'Soluția RMA a fost salvată cu succes.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_saved_ok', N'RMA-Lösung erfolgreich gespeichert.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_saved_ok')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_saved_ok', N'RMA-lösning sparad.');

-- rma_save_error
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_save_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_save_error', N'Errore nel salvataggio. Controllare i log.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_save_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_save_error', N'Save error. Check the logs.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_save_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_save_error', N'Eroare la salvare. Verificați jurnalele.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_save_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_save_error', N'Fehler beim Speichern. Prüfen Sie die Protokolle.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_save_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_save_error', N'Sparfel. Kontrollera loggarna.');

GO
PRINT 'RMA Translations Part 2 (Inserimento + Messaggi) inserite con successo.';
