-- ============================================================================
-- Traduzioni per Richiesta Materiali Indiretti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-03-18
-- ============================================================================

-- ind_req_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_title', 'Richiesta Materiali Indiretti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_title', 'Request Indirect Materials');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_title', N'Cerere Materiale Indirecte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_title', 'Anfrage Indirektes Material');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_title', N'Begäran Indirekta Material');

-- ind_req_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_header', 'Richiesta Materiali Indiretti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_header', 'Request Indirect Materials');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_header', N'Cerere Materiale Indirecte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_header', 'Anfrage Indirektes Material');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_header', N'Begäran Indirekta Material');

-- ind_req_filters
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filters' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_filters', 'Filtri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filters' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_filters', 'Filters');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filters' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_filters', N'Filtre');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filters' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_filters', 'Filter');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filters' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_filters', 'Filter');

-- ind_req_filter_code
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_code' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_filter_code', 'Codice:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_code' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_filter_code', 'Code:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_code' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_filter_code', N'Cod:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_code' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_filter_code', 'Code:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_code' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_filter_code', 'Kod:');

-- ind_req_filter_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_desc' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_filter_desc', 'Descrizione:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_desc' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_filter_desc', 'Description:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_desc' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_filter_desc', N'Descriere:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_desc' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_filter_desc', 'Beschreibung:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_filter_desc' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_filter_desc', 'Beskrivning:');

-- ind_req_btn_clear
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_clear', 'Pulisci');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_clear', 'Clear');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_clear', N'Șterge filtre');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_clear', N'Löschen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_clear', 'Rensa');

-- ind_req_col_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_type' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_type', 'Tipo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_type' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_type', 'Type');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_type' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_type', N'Tip');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_type' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_type', 'Typ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_type' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_type', 'Typ');

-- ind_req_col_stock
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_stock' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_stock', 'Stock');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_stock' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_stock', 'Stock');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_stock' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_stock', N'Stoc');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_stock' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_stock', 'Bestand');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_stock' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_stock', 'Lager');

-- ind_req_col_package
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_package' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_package', 'Confezione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_package' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_package', 'Package');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_package' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_package', N'Ambalaj');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_package' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_package', 'Verpackung');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_package' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_package', N'Förpackning');

-- ind_req_col_fractional
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_fractional' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_fractional', 'Frazionabile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_fractional' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_fractional', 'Fractional');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_fractional' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_fractional', N'Fracționabil');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_fractional' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_fractional', 'Teilbar');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_fractional' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_fractional', 'Delbar');

-- ind_req_no_selection
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_no_selection' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_no_selection', 'Seleziona un materiale dalla lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_no_selection' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_no_selection', 'Select a material from the list');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_no_selection' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_no_selection', N'Selectați un material din listă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_no_selection' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_no_selection', N'Wählen Sie ein Material aus der Liste');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_no_selection' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_no_selection', N'Välj ett material från listan');

-- ind_req_qty
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_qty' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_qty', N'Quantità:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_qty' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_qty', 'Quantity:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_qty' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_qty', N'Cantitate:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_qty' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_qty', 'Menge:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_qty' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_qty', 'Antal:');

-- ind_req_btn_send
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_send', 'Invia Richiesta');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_send', 'Send Request');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_send', N'Trimite Cererea');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_send', 'Anfrage senden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_send', N'Skicka förfrågan');

-- ind_req_btn_history
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_history' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_history', 'Storico Richieste');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_history' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_history', 'Request History');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_history' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_history', N'Istoric Cereri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_history' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_history', 'Anfragenverlauf');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_history' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_history', N'Förfrågningshistorik');

-- ind_req_confirm_send
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_confirm_send', 'Inviare richiesta per:

{0} - {1}
Quantità: {2}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_confirm_send', 'Send request for:

{0} - {1}
Quantity: {2}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_confirm_send', N'Trimiteți cererea pentru:

{0} - {1}
Cantitate: {2}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_confirm_send', N'Anfrage senden für:

{0} - {1}
Menge: {2}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_confirm_send', N'Skicka förfrågan för:

{0} - {1}
Antal: {2}');

-- ind_req_sent_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_ok' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_sent_ok', 'Richiesta inviata con successo!
Il magazzino verrà notificato.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_ok' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_sent_ok', 'Request sent successfully!
The warehouse will be notified.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_ok' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_sent_ok', N'Cererea a fost trimisă cu succes!
Depozitul va fi notificat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_ok' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_sent_ok', 'Anfrage erfolgreich gesendet!
Das Lager wird benachrichtigt.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_ok' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_sent_ok', N'Förfrågan skickad!
Lagret kommer att meddelas.');

-- ind_req_history_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_history_title', 'Storico Richieste Materiali');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_history_title', 'Material Request History');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_history_title', N'Istoric Cereri Materiale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_history_title', 'Materialanfragen-Verlauf');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_history_title', N'Historik Materialförfrågningar');

-- ind_req_col_date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_date' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_date', 'Data');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_date' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_date', 'Date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_date' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_date', N'Data');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_date' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_date', 'Datum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_date' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_date', 'Datum');

-- ind_req_col_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_status' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_status', 'Stato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_status' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_status', 'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_status' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_status', N'Stare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_status' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_status', 'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_status' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_status', 'Status');

-- ind_req_col_requester
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_requester' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_requester', 'Richiedente');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_requester' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_requester', 'Requester');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_requester' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_requester', N'Solicitant');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_requester' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_requester', 'Anforderer');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_requester' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_requester', N'Beställare');

-- ind_req_col_preparer
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_preparer' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_col_preparer', 'Preparatore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_preparer' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_col_preparer', 'Preparer');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_preparer' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_col_preparer', N'Pregătitor');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_preparer' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_col_preparer', 'Vorbereiter');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_col_preparer' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_col_preparer', N'Förberedare');

-- ind_req_btn_reprint
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_reprint' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_reprint', 'Ristampa PDF');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_reprint' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_reprint', 'Reprint PDF');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_reprint' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_reprint', N'Retipărește PDF');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_reprint' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_reprint', 'PDF Nachdruck');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_reprint' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_reprint', N'Skriv ut PDF igen');

-- ind_req_fraz_rule
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_fraz_rule' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_fraz_rule', N'Quantità deve essere divisibile per {0} senza resto');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_fraz_rule' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_fraz_rule', 'Quantity must be divisible by {0} without remainder');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_fraz_rule' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_fraz_rule', N'Cantitatea trebuie să fie divizibilă cu {0} fără rest');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_fraz_rule' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_fraz_rule', 'Menge muss ohne Rest durch {0} teilbar sein');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_fraz_rule' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_fraz_rule', N'Antal måste vara delbart med {0} utan rest');

-- ind_req_nonfraz_rule
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_nonfraz_rule' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_nonfraz_rule', N'Quantità in multipli di {0} (confezione intera)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_nonfraz_rule' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_nonfraz_rule', 'Quantity in multiples of {0} (full package)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_nonfraz_rule' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_nonfraz_rule', N'Cantitatea în multipli de {0} (ambalaj complet)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_nonfraz_rule' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_nonfraz_rule', N'Menge in Vielfachen von {0} (ganze Verpackung)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_nonfraz_rule' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_nonfraz_rule', N'Antal i multiplar av {0} (hel förpackning)');

-- ind_req_ready_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_ready_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_ready_title', N'📦 Materiale pronto per il ritiro!');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_ready_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_ready_title', N'📦 Material ready for pickup!');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_ready_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_ready_title', N'📦 Materialul este pregătit!');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_ready_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_ready_title', N'📦 Material zur Abholung bereit!');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_ready_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_ready_title', N'📦 Material redo för upphämtning!');

-- ind_req_btn_pickup
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_pickup' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_pickup', N'✅ Ritirato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_pickup' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_pickup', N'✅ Picked up');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_pickup' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_pickup', N'✅ Ridicat');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_pickup' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_pickup', N'✅ Abgeholt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_pickup' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_pickup', N'✅ Upphämtad');

-- ind_req_btn_later
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_later' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_later', N'⏳ Dopo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_later' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_later', N'⏳ Later');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_later' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_later', N'⏳ Mai târziu');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_later' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_later', N'⏳ Später');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_later' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_later', N'⏳ Senare');

-- ind_wh_btn_prepare
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_prepare' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_wh_btn_prepare', N'✅ Prepara e Conferma');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_prepare' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_wh_btn_prepare', N'✅ Prepare & Confirm');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_prepare' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_wh_btn_prepare', N'✅ Pregătește și Confirmă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_prepare' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_wh_btn_prepare', N'✅ Vorbereiten & Bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_prepare' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_wh_btn_prepare', N'✅ Förbered & Bekräfta');

-- ind_wh_btn_print_only
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_print_only' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_wh_btn_print_only', N'🖨️ Stampa');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_print_only' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_wh_btn_print_only', N'🖨️ Print');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_print_only' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_wh_btn_print_only', N'🖨️ Tipărește');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_print_only' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_wh_btn_print_only', N'🖨️ Drucken');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_print_only' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_wh_btn_print_only', N'🖨️ Skriv ut');

-- ind_wh_btn_dismiss
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_dismiss' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_wh_btn_dismiss', 'Chiudi');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_dismiss' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_wh_btn_dismiss', 'Close');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_dismiss' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_wh_btn_dismiss', N'Închide');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_dismiss' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_wh_btn_dismiss', N'Schließen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_wh_btn_dismiss' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_wh_btn_dismiss', N'Stäng');

-- ind_req_history_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_history_header', 'Storico Richieste');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_history_header', 'Request History');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_history_header', N'Istoric Cereri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_history_header', 'Anfragenverlauf');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_history_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_history_header', N'Förfrågningshistorik');

-- ind_req_btn_add_cart
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_add_cart' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_add_cart', N'➕ Aggiungi alla lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_add_cart' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_add_cart', N'➕ Add to list');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_add_cart' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_add_cart', N'➕ Adaugă în listă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_add_cart' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_add_cart', N'➕ Zur Liste hinzufügen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_add_cart' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_add_cart', N'➕ Lägg till i listan');

-- ind_req_cart_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_cart_title', 'Lista Richieste da Inviare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_cart_title', 'Requests to Send');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_cart_title', N'Lista Cereri de Trimis');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_cart_title', 'Anfragen zum Senden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_cart_title', N'Förfrågningar att skicka');

-- ind_req_btn_remove
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_remove' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_remove', N'🗑️ Rimuovi selezionati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_remove' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_remove', N'🗑️ Remove selected');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_remove' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_remove', N'🗑️ Elimină selectate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_remove' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_remove', N'🗑️ Ausgewählte entfernen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_remove' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_remove', N'🗑️ Ta bort valda');

-- ind_req_btn_clear_cart
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear_cart' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_clear_cart', N'❌ Svuota lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear_cart' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_clear_cart', N'❌ Clear list');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear_cart' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_clear_cart', N'❌ Golește lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear_cart' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_clear_cart', N'❌ Liste leeren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_clear_cart' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_clear_cart', N'❌ Rensa listan');

-- ind_req_btn_send_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send_all' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_btn_send_all', N'📤 Invia tutte le richieste');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send_all' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_btn_send_all', N'📤 Send all requests');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send_all' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_btn_send_all', N'📤 Trimite toate cererile');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send_all' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_btn_send_all', N'📤 Alle Anfragen senden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_btn_send_all' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_btn_send_all', N'📤 Skicka alla förfrågningar');

-- ind_req_cart_count
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_count' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_cart_count', '{0} materiali in lista');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_count' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_cart_count', '{0} materials in list');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_count' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_cart_count', N'{0} materiale în listă');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_count' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_cart_count', '{0} Materialien in der Liste');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_cart_count' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_cart_count', N'{0} material i listan');

-- ind_req_select_to_remove
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_select_to_remove' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_select_to_remove', 'Selezionare almeno un elemento da rimuovere.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_select_to_remove' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_select_to_remove', 'Select at least one item to remove.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_select_to_remove' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_select_to_remove', N'Selectați cel puțin un element de eliminat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_select_to_remove' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_select_to_remove', N'Wählen Sie mindestens ein Element zum Entfernen aus.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_select_to_remove' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_select_to_remove', N'Välj minst ett objekt att ta bort.');

-- ind_req_confirm_clear
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_clear' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_confirm_clear', 'Svuotare la lista delle richieste?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_clear' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_confirm_clear', 'Clear the request list?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_clear' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_confirm_clear', N'Goliți lista de cereri?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_clear' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_confirm_clear', 'Anfragenliste leeren?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_clear' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_confirm_clear', N'Rensa förfrågningslistan?');

-- ind_req_confirm_send_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send_all' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_confirm_send_all', 'Inviare {0} richieste?

{1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send_all' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_confirm_send_all', 'Send {0} requests?

{1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send_all' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_confirm_send_all', N'Trimiteți {0} cereri?

{1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send_all' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_confirm_send_all', N'{0} Anfragen senden?

{1}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_confirm_send_all' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_confirm_send_all', N'Skicka {0} förfrågningar?

{1}');

-- ind_req_sent_all_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_all_ok' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'ind_req_sent_all_ok', '{0} richieste inviate con successo!
Il magazzino verrà notificato.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_all_ok' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'ind_req_sent_all_ok', '{0} requests sent successfully!
The warehouse will be notified.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_all_ok' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'ind_req_sent_all_ok', N'{0} cereri trimise cu succes!
Depozitul va fi notificat.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_all_ok' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'ind_req_sent_all_ok', '{0} Anfragen erfolgreich gesendet!
Das Lager wird benachrichtigt.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'ind_req_sent_all_ok' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'ind_req_sent_all_ok', N'{0} förfrågningar skickade!
Lagret kommer att meddelas.');

-- menu_materials_general (Help menu)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_materials_general' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_materials_general', 'Materiali (Generale)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_materials_general' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_materials_general', 'Materials (General)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_materials_general' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_materials_general', N'Materiale (General)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_materials_general' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_materials_general', 'Materialien (Allgemein)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_materials_general' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_materials_general', 'Material (Allmänt)');

-- menu_indirect_materials_manual (Help menu)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_indirect_materials_manual' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_indirect_materials_manual', 'Materiali Indiretti (Manuale)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_indirect_materials_manual' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_indirect_materials_manual', 'Indirect Materials (Manual)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_indirect_materials_manual' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_indirect_materials_manual', N'Materiale Indirecte (Manual)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_indirect_materials_manual' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_indirect_materials_manual', 'Indirekte Materialien (Handbuch)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_indirect_materials_manual' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_indirect_materials_manual', N'Indirekta Material (Handbok)');

-- ═══════════════════════════════════════════════════════════════
-- Traduzioni: Gestione Check Errati
-- ═══════════════════════════════════════════════════════════════

-- submenu_manage_wrong_checks
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_manage_wrong_checks' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_manage_wrong_checks', 'Gestione Check errati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_manage_wrong_checks' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_manage_wrong_checks', 'Manage Wrong Checks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_manage_wrong_checks' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_manage_wrong_checks', N'Gestionare Verificări Eronate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_manage_wrong_checks' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_manage_wrong_checks', N'Fehlerhafte Prüfungen verwalten');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_manage_wrong_checks' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_manage_wrong_checks', N'Hantera felaktiga kontroller');

-- wrong_checks_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_title' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_title', 'Gestione Check Errati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_title' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_title', 'Manage Wrong Checks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_title' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_title', N'Gestionare Verificări Eronate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_title' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_title', N'Fehlerhafte Prüfungen verwalten');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_title' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_title', N'Hantera felaktiga kontroller');

-- wrong_checks_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_header' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_header', N'Verifiche in attesa — selezionare e cancellare quelle errate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_header' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_header', N'Pending checks — select and delete wrong ones');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_header' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_header', N'Verificări în așteptare — selectați și ștergeți cele eronate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_header' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_header', N'Ausstehende Prüfungen — fehlerhafte auswählen und löschen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_header' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_header', N'Väntande kontroller — välj och ta bort felaktiga');

-- wrong_checks_btn_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_btn_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_btn_delete', N'🗑️ Cancella selezionati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_btn_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_btn_delete', N'🗑️ Delete selected');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_btn_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_btn_delete', N'🗑️ Șterge selectate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_btn_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_btn_delete', N'🗑️ Ausgewählte löschen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_btn_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_btn_delete', N'🗑️ Ta bort valda');

-- wrong_checks_pending
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_pending' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_pending', 'verifiche in attesa');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_pending' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_pending', 'pending checks');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_pending' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_pending', N'verificări în așteptare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_pending' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_pending', N'ausstehende Prüfungen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_pending' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_pending', N'väntande kontroller');

-- wrong_checks_confirm_delete
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_confirm_delete' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_confirm_delete', N'Cancellare {0} verifiche selezionate?

{1}

Questa operazione è irreversibile.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_confirm_delete' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_confirm_delete', N'Delete {0} selected checks?

{1}

This operation is irreversible.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_confirm_delete' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_confirm_delete', N'Ștergeți {0} verificări selectate?

{1}

Această operațiune este ireversibilă.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_confirm_delete' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_confirm_delete', N'{0} ausgewählte Prüfungen löschen?

{1}

Dieser Vorgang ist unwiderruflich.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_confirm_delete' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_confirm_delete', N'Ta bort {0} valda kontroller?

{1}

Denna åtgärd är oåterkallelig.');

-- wrong_checks_deleted_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_deleted_ok' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'wrong_checks_deleted_ok', '{0} verifiche cancellate con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_deleted_ok' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'wrong_checks_deleted_ok', '{0} checks deleted successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_deleted_ok' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'wrong_checks_deleted_ok', N'{0} verificări șterse cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_deleted_ok' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'wrong_checks_deleted_ok', N'{0} Prüfungen erfolgreich gelöscht.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'wrong_checks_deleted_ok' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'wrong_checks_deleted_ok', N'{0} kontroller har tagits bort.');

PRINT 'Traduzioni Richiesta Materiali Indiretti e Gestione Check Errati inserite con successo.';
