-- ============================================================
-- Traduzioni RMA Knowledge Base — PARTE 1 (Menu + Tab Ricerca)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv
-- NOTA: Emoji rimosse per compatibilità SQL Server NVARCHAR
-- Generato il: 2026-03-27
-- ============================================================

-- menu_rma_kb
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'menu_rma_kb')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_rma_kb', N'RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'menu_rma_kb')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_rma_kb', N'RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'menu_rma_kb')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_rma_kb', N'RMA Bază de Cunoștințe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'menu_rma_kb')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_rma_kb', N'RMA Wissensdatenbank');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'menu_rma_kb')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_rma_kb', N'RMA Kunskapsbas');

-- rma_open_error
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_open_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_open_error', N'Errore apertura RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_open_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_open_error', N'Error opening RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_open_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_open_error', N'Eroare la deschiderea RMA Bază de Cunoștințe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_open_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_open_error', N'Fehler beim Öffnen der RMA Wissensdatenbank');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_open_error')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_open_error', N'Fel vid öppning av RMA Kunskapsbas');

-- rma_kb_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_kb_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_kb_title', N'RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_kb_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_kb_title', N'RMA Knowledge Base');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_kb_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_kb_title', N'RMA Bază de Cunoștințe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_kb_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_kb_title', N'RMA Wissensdatenbank');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_kb_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_kb_title', N'RMA Kunskapsbas');

-- rma_tab_search
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_tab_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_tab_search', N'Ricerca Soluzioni');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_tab_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_tab_search', N'Search Solutions');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_tab_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_tab_search', N'Căutare Soluții');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_tab_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_tab_search', N'Lösungen suchen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_tab_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_tab_search', N'Sök lösningar');

-- rma_tab_insert
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_tab_insert')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_tab_insert', N'Inserisci Soluzione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_tab_insert')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_tab_insert', N'Insert Solution');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_tab_insert')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_tab_insert', N'Adăugare Soluție');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_tab_insert')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_tab_insert', N'Lösung einfügen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_tab_insert')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_tab_insert', N'Lägg till lösning');

-- rma_filters
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_filters')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_filters', N'Filtri (combinabili)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_filters')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_filters', N'Filters (combinable)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_filters')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_filters', N'Filtre (combinabile)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_filters')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_filters', N'Filter (kombinierbar)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_filters')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_filters', N'Filter (kombinerbara)');

-- rma_serial
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_serial')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_serial', N'Serial Number:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_serial')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_serial', N'Serial Number:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_serial')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_serial', N'Număr Serial:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_serial')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_serial', N'Seriennummer:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_serial')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_serial', N'Serienummer:');

-- rma_part_code
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_part_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_part_code', N'Codice Parte:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_part_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_part_code', N'Part Code:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_part_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_part_code', N'Cod Piesă:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_part_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_part_code', N'Teilenummer:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_part_code')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_part_code', N'Artikelkod:');

-- rma_customer
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_customer', N'Cliente:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_customer', N'Customer:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_customer', N'Client:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_customer', N'Kunde:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_customer', N'Kund:');

-- rma_fault_contains
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_contains')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_contains', N'Guasto contiene:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_contains')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_contains', N'Fault contains:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_contains')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_contains', N'Defectul conține:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_contains')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_contains', N'Fehler enthält:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_contains')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_contains', N'Fel innehåller:');

-- rma_fault_type
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_fault_type')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_fault_type', N'Tipo Guasto:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_fault_type')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_fault_type', N'Fault Type:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_fault_type')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_fault_type', N'Tip Defect:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_fault_type')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_fault_type', N'Fehlertyp:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_fault_type')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_fault_type', N'Feltyp:');

-- rma_reference
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_reference')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_reference', N'Reference:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_reference')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_reference', N'Reference:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_reference')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_reference', N'Referință:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_reference')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_reference', N'Referenz:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_reference')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_reference', N'Referens:');

-- rma_search_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_search_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_search_btn', N'Cerca');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_search_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_search_btn', N'Search');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_search_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_search_btn', N'Caută');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_search_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_search_btn', N'Suchen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_search_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_search_btn', N'Sök');

-- rma_reset_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_reset_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_reset_btn', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_reset_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_reset_btn', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_reset_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_reset_btn', N'Resetare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_reset_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_reset_btn', N'Zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_reset_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_reset_btn', N'Återställ');

-- rma_detail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_detail', N'Dettaglio Selezionato');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_detail', N'Selected Detail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_detail', N'Detaliu Selectat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_detail', N'Ausgewähltes Detail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_detail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_detail', N'Vald detalj');

-- rma_open_traceability
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_open_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_open_traceability', N'Apri Tracciabilità');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_open_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_open_traceability', N'Open Traceability');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_open_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_open_traceability', N'Deschide Trasabilitate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_open_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_open_traceability', N'Rückverfolgbarkeit öffnen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_open_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_open_traceability', N'Öppna spårbarhet');

-- rma_traceability
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_traceability', N'Tracciabilità');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_traceability', N'Traceability');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_traceability', N'Trasabilitate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_traceability', N'Rückverfolgbarkeit');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_traceability')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_traceability', N'Spårbarhet');

-- rma_trace_not_found
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rma_trace_not_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'rma_trace_not_found', N'Informazioni di tracciabilità non trovate.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rma_trace_not_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'rma_trace_not_found', N'Traceability information not found.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rma_trace_not_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'rma_trace_not_found', N'Informațiile de trasabilitate nu au fost găsite.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rma_trace_not_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'rma_trace_not_found', N'Rückverfolgbarkeitsinformationen nicht gefunden.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rma_trace_not_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'rma_trace_not_found', N'Spårbarhetsinformation hittades inte.');

GO
PRINT 'RMA Translations Part 1 (Menu + Ricerca) inserite con successo.';
