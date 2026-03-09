-- =============================================================
-- Traduzioni nuovi pulsanti/messaggi per Guest Management GUI
-- Eseguire in SSMS su traceability_rs
-- =============================================================

-- btn_generate_booking
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_generate_booking' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_generate_booking', 'it', N'➕ Genera Booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_generate_booking' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_generate_booking', 'ro', N'➕ Generează Booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_generate_booking' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_generate_booking', 'en', N'➕ Generate Booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_generate_booking' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_generate_booking', 'de', N'➕ Buchung Erstellen');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_generate_booking' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_generate_booking', 'sv', N'➕ Skapa Bokning');

-- select_guests_booking
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_guests_booking' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_guests_booking', 'it', N'Seleziona ospiti per booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_guests_booking' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_guests_booking', 'ro', N'Selectați oaspeții pentru booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_guests_booking' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_guests_booking', 'en', N'Select guests for booking');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_guests_booking' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_guests_booking', 'de', N'Gäste für Buchung auswählen');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_guests_booking' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_guests_booking', 'sv', N'Välj gäster för bokning');

-- guests_without_booking (label nella dialog di selezione)
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_without_booking' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_without_booking', 'it', N'Ospiti senza prenotazione:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_without_booking' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_without_booking', 'ro', N'Oaspeți fără rezervare:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_without_booking' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_without_booking', 'en', N'Guests without booking:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_without_booking' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_without_booking', 'de', N'Gäste ohne Buchung:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_without_booking' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_without_booking', 'sv', N'Gäster utan bokning:');

-- no_visitors_without_booking
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_visitors_without_booking' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_visitors_without_booking', 'it', N'Tutti gli ospiti attivi hanno già una prenotazione.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_visitors_without_booking' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_visitors_without_booking', 'ro', N'Toți oaspeții activi au deja o rezervare.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_visitors_without_booking' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_visitors_without_booking', 'en', N'All active guests already have a booking.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_visitors_without_booking' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_visitors_without_booking', 'de', N'Alle aktiven Gäste haben bereits eine Buchung.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_visitors_without_booking' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_visitors_without_booking', 'sv', N'Alla aktiva gäster har redan en bokning.');

-- select_at_least_one
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_at_least_one' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_at_least_one', 'it', N'Selezionare almeno un ospite.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_at_least_one' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_at_least_one', 'ro', N'Selectați cel puțin un oaspete.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_at_least_one' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_at_least_one', 'en', N'Select at least one guest.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_at_least_one' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_at_least_one', 'de', N'Wählen Sie mindestens einen Gast aus.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_at_least_one' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_at_least_one', 'sv', N'Välj minst en gäst.');

-- all_bookings_generated
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'all_bookings_generated' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('all_bookings_generated', 'it', N'Tutti i booking sono stati generati.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'all_bookings_generated' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('all_bookings_generated', 'ro', N'Toate rezervările au fost generate.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'all_bookings_generated' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('all_bookings_generated', 'en', N'All bookings have been generated.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'all_bookings_generated' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('all_bookings_generated', 'de', N'Alle Buchungen wurden erstellt.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'all_bookings_generated' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('all_bookings_generated', 'sv', N'Alla bokningar har genererats.');

-- guests_no_email_warning
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_no_email_warning' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_no_email_warning', 'it', N'Alcuni ospiti non hanno email registrata e NON riceveranno la conferma. Procedere?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_no_email_warning' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_no_email_warning', 'ro', N'Unii oaspeți nu au email înregistrat și NU vor primi confirmarea. Continuați?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_no_email_warning' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_no_email_warning', 'en', N'Some guests have no registered email and will NOT receive confirmations. Proceed?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_no_email_warning' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_no_email_warning', 'de', N'Einige Gäste haben keine registrierte E-Mail und erhalten KEINE Bestätigungen. Fortfahren?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'guests_no_email_warning' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('guests_no_email_warning', 'sv', N'Vissa gäster har ingen registrerad e-post och kommer INTE att få bekräftelse. Fortsätt?');

-- btn_cancel
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_cancel' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_cancel', 'it', N'Annulla');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_cancel' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_cancel', 'ro', N'Anulare');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_cancel' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_cancel', 'en', N'Cancel');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_cancel' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_cancel', 'de', N'Abbrechen');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_cancel' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('btn_cancel', 'sv', N'Avbryt');

-- col_service
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_service' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('col_service', 'it', N'Servizio');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_service' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('col_service', 'ro', N'Serviciu');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_service' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('col_service', 'en', N'Service');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_service' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('col_service', 'de', N'Dienst');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_service' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('col_service', 'sv', N'Tjänst');

-- close_without_booking
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'close_without_booking' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('close_without_booking', 'it', N'Chiudere senza inviare le prenotazioni?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'close_without_booking' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('close_without_booking', 'ro', N'Închideți fără a trimite rezervările?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'close_without_booking' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('close_without_booking', 'en', N'Close without sending bookings?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'close_without_booking' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('close_without_booking', 'de', N'Schließen ohne Buchungen zu senden?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'close_without_booking' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('close_without_booking', 'sv', N'Stäng utan att skicka bokningar?');

-- confirm_flight
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight', 'it', N'Conferma Volo');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight', 'ro', N'Confirmă Zborul');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight', 'en', N'Confirm Flight');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight', 'de', N'Flug Bestätigen');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight', 'sv', N'Bekräfta Flyg');

-- confirm_flight_details
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight_details' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight_details', 'it', N'Confermi questo volo?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight_details' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight_details', 'ro', N'Confirmați acest zbor?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight_details' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight_details', 'en', N'Do you confirm this flight?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight_details' AND LanguageCode = 'de')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight_details', 'de', N'Diesen Flug bestätigen?');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'confirm_flight_details' AND LanguageCode = 'sv')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('confirm_flight_details', 'sv', N'Bekräfta detta flyg?');

PRINT 'Traduzioni guest management nuovi bottoni inserite con successo.';

-- select_flight (titolo dialog selezione voli)
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_flight' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_flight', 'it', N'Seleziona Volo');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_flight' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_flight', 'ro', N'Selectați Zborul');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_flight' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('select_flight', 'en', N'Select Flight');

-- multiple_flights_found
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'multiple_flights_found' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('multiple_flights_found', 'it', N'Trovati più voli. Selezionarne uno:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'multiple_flights_found' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('multiple_flights_found', 'ro', N'Mai multe zboruri găsite. Selectați unul:');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'multiple_flights_found' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('multiple_flights_found', 'en', N'Multiple flights found. Select one:');

-- no_flights_found
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_flights_found' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_flights_found', 'it', N'Nessun volo trovato. Inserire data e ora manualmente.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_flights_found' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_flights_found', 'ro', N'Niciun zbor găsit. Introduceți data și ora manual.');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'no_flights_found' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('no_flights_found', 'en', N'No flights found. Enter date and time manually.');

-- booking_in_progress
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'booking_in_progress' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('booking_in_progress', 'it', N'Invio prenotazioni in corso...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'booking_in_progress' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('booking_in_progress', 'ro', N'Trimiterea rezervărilor în curs...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'booking_in_progress' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('booking_in_progress', 'en', N'Sending bookings...');

-- sending_shuttle
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_shuttle' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_shuttle', 'it', N'Invio prenotazione shuttle...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_shuttle' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_shuttle', 'ro', N'Trimitere rezervare shuttle...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_shuttle' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_shuttle', 'en', N'Sending shuttle booking...');

-- sending_hotel
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_hotel' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_hotel', 'it', N'Invio prenotazione hotel...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_hotel' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_hotel', 'ro', N'Trimitere rezervare hotel...');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'sending_hotel' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('sending_hotel', 'en', N'Sending hotel booking...');

-- force_factory (checkbox destinazione fabbrica)
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'force_factory' AND LanguageCode = 'it')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('force_factory', 'it', N'Destinazione fabbrica (anche dopo le 16:00)');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'force_factory' AND LanguageCode = 'ro')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('force_factory', 'ro', N'Destinația fabrică (chiar și după 16:00)');
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'force_factory' AND LanguageCode = 'en')
INSERT INTO traceability_rs.dbo.AppTranslations (TranslationKey, LanguageCode, TranslationValue) VALUES ('force_factory', 'en', N'Factory destination (even after 4 PM)');

PRINT 'Traduzioni flight dialog e progress bar inserite con successo.';
