-- ============================================================
-- Traduzioni per guest_settings_gui.py (Hotels, Shuttle, Airlines)
-- Tabella: Traceability_RS.dbo.AppTranslations
-- ============================================================

-- hotel_settings_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='hotel_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'hotel_settings_title', 'Gestione Hotels');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='hotel_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'hotel_settings_title', N'Gestionare hoteluri');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='hotel_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'hotel_settings_title', 'Hotel Management');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='hotel_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'hotel_settings_title', 'Hotelverwaltung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='hotel_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'hotel_settings_title', 'Hotellhantering');

-- shuttle_settings_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='shuttle_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'shuttle_settings_title', 'Gestione Shuttle');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='shuttle_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'shuttle_settings_title', N'Gestionare navetă');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='shuttle_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'shuttle_settings_title', 'Shuttle Management');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='shuttle_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'shuttle_settings_title', 'Shuttle-Verwaltung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='shuttle_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'shuttle_settings_title', 'Shuttlehantering');

-- airline_settings_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='airline_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'airline_settings_title', 'Gestione Compagnie Aeree');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='airline_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'airline_settings_title', N'Gestionare companii aeriene');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='airline_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'airline_settings_title', 'Airline Management');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='airline_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'airline_settings_title', 'Fluggesellschaftsverwaltung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='airline_settings_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'airline_settings_title', 'Flygbolagshantering');

-- col_name
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_name', 'Nome');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_name', 'Nume');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_name', 'Name');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_name', 'Name');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_name', 'Namn');

-- col_city
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_city')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_city', 'Città');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_city')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_city', N'Oraș');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_city')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_city', 'City');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_city')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_city', 'Stadt');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_city')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_city', 'Stad');

-- edit_details
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='edit_details')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'edit_details', 'Dettagli');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='edit_details')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'edit_details', 'Detalii');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='edit_details')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'edit_details', 'Details');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='edit_details')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'edit_details', 'Details');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='edit_details')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'edit_details', 'Detaljer');

-- btn_new
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_new')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_new', '➕ Nuovo');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_new')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_new', N'➕ Nou');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_new')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_new', '➕ New');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_new')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_new', '➕ Neu');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_new')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_new', '➕ Ny');

-- btn_save
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_save')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_save', '💾 Salva');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_save')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_save', N'💾 Salvează');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_save')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_save', '💾 Save');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_save')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_save', '💾 Speichern');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_save')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_save', '💾 Spara');

-- btn_deactivate
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_deactivate', '🚫 Disattiva');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_deactivate', N'🚫 Dezactivează');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_deactivate', '🚫 Deactivate');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_deactivate', '🚫 Deaktivieren');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_deactivate', '🚫 Inaktivera');

-- btn_delete
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_delete', '🗑 Elimina');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_delete', N'🗑 Șterge');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_delete', '🗑 Delete');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_delete', '🗑 Löschen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_delete', '🗑 Ta bort');

-- col_airline_name
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_airline_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_airline_name', 'Compagnia');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_airline_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_airline_name', N'Companie aeriană');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_airline_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_airline_name', 'Airline');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_airline_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_airline_name', 'Fluggesellschaft');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_airline_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_airline_name', 'Flygbolag');

-- col_iata_code
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_iata_code')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_iata_code', 'Codice IATA');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_iata_code')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_iata_code', 'Cod IATA');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_iata_code')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_iata_code', 'IATA Code');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_iata_code')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_iata_code', 'IATA-Code');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_iata_code')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_iata_code', 'IATA-kod');

-- name_required
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'name_required', 'Il campo Nome è obbligatorio.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'name_required', N'Câmpul Nume este obligatoriu.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'name_required', 'The Name field is required.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'name_required', 'Das Feld Name ist erforderlich.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'name_required', 'Fältet Namn är obligatoriskt.');

-- airline_name_required
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='airline_name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'airline_name_required', 'Il nome della compagnia è obbligatorio.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='airline_name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'airline_name_required', N'Numele companiei aeriene este obligatoriu.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='airline_name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'airline_name_required', 'The airline name is required.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='airline_name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'airline_name_required', 'Der Name der Fluggesellschaft ist erforderlich.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='airline_name_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'airline_name_required', 'Flygbolagets namn är obligatoriskt.');

-- data_saved
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'data_saved', 'Dati salvati con successo.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'data_saved', N'Datele au fost salvate cu succes.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'data_saved', 'Data saved successfully.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'data_saved', 'Daten erfolgreich gespeichert.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'data_saved', 'Data sparades.');

-- select_record
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='select_record')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'select_record', 'Selezionare un record dalla lista.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='select_record')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'select_record', N'Selectați o înregistrare din listă.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='select_record')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'select_record', 'Select a record from the list.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='select_record')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'select_record', 'Wählen Sie einen Eintrag aus der Liste.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='select_record')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'select_record', 'Välj en post från listan.');

-- confirm_deactivate
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='confirm_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'confirm_deactivate', 'Disattivare questo record?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='confirm_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'confirm_deactivate', N'Dezactivați această înregistrare?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='confirm_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'confirm_deactivate', 'Deactivate this record?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='confirm_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'confirm_deactivate', 'Diesen Eintrag deaktivieren?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='confirm_deactivate')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'confirm_deactivate', 'Inaktivera denna post?');

-- confirm_delete
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='confirm_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'confirm_delete', 'Eliminare questo record?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='confirm_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'confirm_delete', N'Ștergeți această înregistrare?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='confirm_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'confirm_delete', 'Delete this record?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='confirm_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'confirm_delete', 'Diesen Eintrag löschen?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='confirm_delete')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'confirm_delete', 'Ta bort denna post?');

-- guest_settings_hotels
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_settings_hotels')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_settings_hotels', 'Hotels');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_settings_hotels')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_settings_hotels', 'Hoteluri');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_settings_hotels')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_settings_hotels', 'Hotels');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_settings_hotels')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_settings_hotels', 'Hotels');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_settings_hotels')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_settings_hotels', 'Hotell');

-- guest_settings_shuttle
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_settings_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_settings_shuttle', 'Shuttle');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_settings_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_settings_shuttle', N'Navetă');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_settings_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_settings_shuttle', 'Shuttle');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_settings_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_settings_shuttle', 'Shuttle');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_settings_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_settings_shuttle', 'Shuttle');

-- guest_settings_airlines
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_settings_airlines')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_settings_airlines', 'Compagnie Aeree');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_settings_airlines')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_settings_airlines', N'Companii aeriene');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_settings_airlines')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_settings_airlines', 'Airlines');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_settings_airlines')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_settings_airlines', 'Fluggesellschaften');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_settings_airlines')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_settings_airlines', 'Flygbolag');

PRINT 'Traduzioni guest settings inserite con successo.';
