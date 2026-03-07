-- ============================================================
-- Traduzioni per guest_management_gui.py (Gestione Ospiti)
-- Tabella: Traceability_RS.dbo.AppTranslations
-- ============================================================

-- guest_management_title
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_management_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_management_title', 'Gestione Ospiti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_management_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_management_title', N'Gestionare oaspeți');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_management_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_management_title', 'Guest Management');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_management_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_management_title', 'Gästeverwaltung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_management_title')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_management_title', 'Gästhantering');

-- tab_bookings
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='tab_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'tab_bookings', '📋 Booking');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='tab_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'tab_bookings', N'📋 Rezervări');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='tab_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'tab_bookings', '📋 Bookings');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='tab_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'tab_bookings', '📋 Buchungen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='tab_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'tab_bookings', '📋 Bokningar');

-- tab_guest_data
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='tab_guest_data')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'tab_guest_data', '👤 Dati Ospiti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='tab_guest_data')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'tab_guest_data', N'👤 Date oaspeți');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='tab_guest_data')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'tab_guest_data', '👤 Guest Data');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='tab_guest_data')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'tab_guest_data', '👤 Gästedaten');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='tab_guest_data')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'tab_guest_data', '👤 Gästdata');

-- show_all_bookings
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='show_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'show_all_bookings', 'Mostra anche confermati');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='show_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'show_all_bookings', N'Arată și confirmate');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='show_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'show_all_bookings', 'Show confirmed too');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='show_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'show_all_bookings', 'Auch bestätigte anzeigen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='show_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'show_all_bookings', 'Visa även bekräftade');

-- btn_confirm_booking
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_confirm_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_confirm_booking', '✅ Segna Confermato');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_confirm_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_confirm_booking', N'✅ Marchează confirmat');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_confirm_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_confirm_booking', '✅ Mark Confirmed');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_confirm_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_confirm_booking', '✅ Als bestätigt markieren');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_confirm_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_confirm_booking', '✅ Markera bekräftad');

-- btn_resend_email
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_resend_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_resend_email', '📧 Reinvia Email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_resend_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_resend_email', N'📧 Retrimite email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_resend_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_resend_email', '📧 Resend Email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_resend_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_resend_email', '📧 Email erneut senden');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_resend_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_resend_email', '📧 Skicka om e-post');

-- col_flight
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_flight')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_flight', 'Volo');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_flight')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_flight', 'Zbor');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_flight')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_flight', 'Flight');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_flight')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_flight', 'Flug');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_flight')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_flight', 'Flyg');

-- col_arrival_date
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_arrival_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_arrival_date', 'Data Arrivo');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_arrival_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_arrival_date', N'Data sosirii');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_arrival_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_arrival_date', 'Arrival Date');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_arrival_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_arrival_date', 'Ankunftsdatum');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_arrival_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_arrival_date', 'Ankomstdatum');

-- col_departure_date
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_departure_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_departure_date', 'Data Partenza');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_departure_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_departure_date', N'Data plecării');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_departure_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_departure_date', 'Departure Date');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_departure_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_departure_date', 'Abreisedatum');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_departure_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_departure_date', 'Avresedatum');

-- col_service_email
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_service_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_service_email', 'Email Servizio');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_service_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_service_email', 'Email serviciu');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_service_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_service_email', 'Service Email');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_service_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_service_email', 'Service-E-Mail');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_service_email')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_service_email', 'Tjänstens e-post');

-- col_sent_date
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_sent_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_sent_date', 'Inviato');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_sent_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_sent_date', 'Trimis');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_sent_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_sent_date', 'Sent');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_sent_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_sent_date', 'Gesendet');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_sent_date')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_sent_date', 'Skickat');

-- col_confirmed
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_confirmed', 'Confermato');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_confirmed', 'Confirmat');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_confirmed', 'Confirmed');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_confirmed', 'Bestätigt');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_confirmed', 'Bekräftad');

-- select_booking
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='select_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'select_booking', 'Selezionare un booking dalla lista.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='select_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'select_booking', N'Selectați o rezervare din listă.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='select_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'select_booking', 'Select a booking from the list.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='select_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'select_booking', 'Wählen Sie eine Buchung aus der Liste.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='select_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'select_booking', 'Välj en bokning från listan.');

-- already_confirmed
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='already_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'already_confirmed', 'Questo booking è già confermato.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='already_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'already_confirmed', N'Această rezervare este deja confirmată.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='already_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'already_confirmed', 'This booking is already confirmed.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='already_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'already_confirmed', 'Diese Buchung ist bereits bestätigt.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='already_confirmed')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'already_confirmed', 'Denna bokning är redan bekräftad.');

-- no_email_for_booking
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='no_email_for_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'no_email_for_booking', 'Nessuna email associata a questo booking.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='no_email_for_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'no_email_for_booking', N'Nicio adresă de email asociată acestei rezervări.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='no_email_for_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'no_email_for_booking', 'No email associated with this booking.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='no_email_for_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'no_email_for_booking', 'Keine E-Mail mit dieser Buchung verknüpft.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='no_email_for_booking')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'no_email_for_booking', 'Ingen e-post kopplad till denna bokning.');

-- confirm_resend
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='confirm_resend')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'confirm_resend', 'Reinviare l''email di prenotazione?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='confirm_resend')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'confirm_resend', N'Retrimiteți emailul de rezervare?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='confirm_resend')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'confirm_resend', 'Resend the booking email?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='confirm_resend')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'confirm_resend', 'Buchungs-E-Mail erneut senden?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='confirm_resend')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'confirm_resend', 'Skicka om bokningsmeddelandet?');

-- email_resent
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='email_resent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'email_resent', 'Email reinviata con successo.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='email_resent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'email_resent', N'Emailul a fost retrimis cu succes.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='email_resent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'email_resent', 'Email resent successfully.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='email_resent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'email_resent', 'E-Mail erfolgreich erneut gesendet.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='email_resent')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'email_resent', 'E-post skickades om.');

-- filter_company
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='filter_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'filter_company', 'Filtra per società:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='filter_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'filter_company', N'Filtrează după companie:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='filter_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'filter_company', 'Filter by company:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='filter_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'filter_company', 'Nach Firma filtern:');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='filter_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'filter_company', 'Filtrera efter företag:');

-- btn_show_all
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_show_all')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_show_all', 'Mostra Tutti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_show_all')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_show_all', N'Arată toți');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_show_all')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_show_all', 'Show All');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_show_all')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_show_all', 'Alle anzeigen');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_show_all')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_show_all', 'Visa alla');

-- col_guest_name
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_guest_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_guest_name', 'Nome Ospite');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_guest_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_guest_name', N'Nume oaspete');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_guest_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_guest_name', 'Guest Name');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_guest_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_guest_name', 'Gastname');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_guest_name')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_guest_name', 'Gästnamn');

-- col_phone
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_phone')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_phone', 'Telefono');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_phone')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_phone', 'Telefon');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_phone')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_phone', 'Phone');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_phone')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_phone', 'Telefon');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_phone')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_phone', 'Telefon');

-- col_company
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='col_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'col_company', 'Società');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='col_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'col_company', 'Companie');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='col_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'col_company', 'Company');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='col_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'col_company', 'Firma');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='col_company')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'col_company', 'Företag');

-- edit_guest
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='edit_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'edit_guest', 'Modifica Ospite');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='edit_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'edit_guest', N'Modifică oaspete');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='edit_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'edit_guest', 'Edit Guest');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='edit_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'edit_guest', 'Gast bearbeiten');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='edit_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'edit_guest', 'Redigera gäst');

-- btn_save_guest
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_save_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'btn_save_guest', '💾 Salva');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_save_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'btn_save_guest', N'💾 Salvează');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_save_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'btn_save_guest', '💾 Save');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_save_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'btn_save_guest', '💾 Speichern');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_save_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'btn_save_guest', '💾 Spara');

-- select_guest
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='select_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'select_guest', 'Selezionare un ospite dalla lista.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='select_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'select_guest', N'Selectați un oaspete din listă.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='select_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'select_guest', 'Select a guest from the list.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='select_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'select_guest', 'Wählen Sie einen Gast aus der Liste.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='select_guest')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'select_guest', 'Välj en gäst från listan.');

-- guest_data_saved
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_data_saved', 'Dati ospite salvati con successo.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_data_saved', N'Datele oaspetelui au fost salvate cu succes.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_data_saved', 'Guest data saved successfully.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_data_saved', 'Gästedaten erfolgreich gespeichert.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_data_saved')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_data_saved', 'Gästdata sparades.');

-- skip_shuttle (from guest_booking_gui.py)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='skip_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'skip_shuttle', 'Non richiedere servizio shuttle');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='skip_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'skip_shuttle', N'Nu solicita serviciul de naveta');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='skip_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'skip_shuttle', 'Do not request shuttle service');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='skip_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'skip_shuttle', 'Kein Shuttle-Service anfordern');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='skip_shuttle')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'skip_shuttle', 'Begär inte shuttletjänst');

-- skip_hotel (from guest_booking_gui.py)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='skip_hotel')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'skip_hotel', 'Non richiedere servizio hotel');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='skip_hotel')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'skip_hotel', N'Nu solicita serviciul de hotel');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='skip_hotel')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'skip_hotel', 'Do not request hotel service');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='skip_hotel')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'skip_hotel', 'Kein Hotel-Service anfordern');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='skip_hotel')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'skip_hotel', 'Begär inte hotelltjänst');

-- skip_all_bookings (from guest_booking_gui.py)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='skip_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'skip_all_bookings', 'Entrambi i servizi sono disattivati. Chiudere senza prenotazioni?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='skip_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'skip_all_bookings', N'Ambele servicii sunt dezactivate. Închideți fără rezervări?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='skip_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'skip_all_bookings', 'Both services are disabled. Close without bookings?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='skip_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'skip_all_bookings', 'Beide Dienste sind deaktiviert. Ohne Buchungen schließen?');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='skip_all_bookings')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'skip_all_bookings', 'Båda tjänsterna är inaktiverade. Stäng utan bokningar?');

-- shuttle_required (from guest_booking_gui.py)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='shuttle_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'shuttle_required', 'Selezionare un servizio shuttle oppure disattivare il servizio.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='shuttle_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'shuttle_required', N'Selectați un serviciu de navetă sau dezactivați serviciul.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='shuttle_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'shuttle_required', 'Select a shuttle service or disable the service.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='shuttle_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'shuttle_required', 'Wählen Sie einen Shuttle-Dienst oder deaktivieren Sie den Dienst.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='shuttle_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'shuttle_required', 'Välj en shuttletjänst eller inaktivera tjänsten.');

-- hotel_required (from guest_booking_gui.py)
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='hotel_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'hotel_required', 'Selezionare un hotel oppure disattivare il servizio.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='hotel_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'hotel_required', N'Selectați un hotel sau dezactivați serviciul.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='hotel_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'hotel_required', 'Select a hotel or disable the service.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='hotel_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'hotel_required', 'Wählen Sie ein Hotel oder deaktivieren Sie den Dienst.');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='hotel_required')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'hotel_required', 'Välj ett hotell eller inaktivera tjänsten.');

-- guest_settings_management
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='guest_settings_management')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'guest_settings_management', 'Gestione Ospiti');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='guest_settings_management')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'guest_settings_management', N'Gestionare oaspeți');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='guest_settings_management')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'guest_settings_management', 'Guest Management');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='guest_settings_management')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'guest_settings_management', 'Gästeverwaltung');
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='guest_settings_management')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'guest_settings_management', 'Gästhantering');

PRINT 'Traduzioni guest management inserite con successo.';
