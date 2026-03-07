-- ============================================================
-- Traduzioni per Guest Booking (Volo, Shuttle, Hotel)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-03-07
-- ============================================================

-- guest_booking_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='guest_booking_title')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','guest_booking_title','Booking Ospiti — Volo, Shuttle, Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='guest_booking_title')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','guest_booking_title',N'Rezervări Oaspeți — Zbor, Shuttle, Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='guest_booking_title')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','guest_booking_title','Guest Booking — Flight, Shuttle, Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='guest_booking_title')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','guest_booking_title','Bokning — Flyg, Shuttle, Hotell');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='guest_booking_title')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','guest_booking_title','Buchung — Flug, Shuttle, Hotel');

-- flight_tab
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='flight_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','flight_tab','✈ Volo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='flight_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','flight_tab',N'✈ Zbor');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='flight_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','flight_tab','✈ Flight');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='flight_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','flight_tab','✈ Flyg');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='flight_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','flight_tab','✈ Flug');

-- shuttle_tab
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='shuttle_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','shuttle_tab','🚐 Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='shuttle_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','shuttle_tab','🚐 Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='shuttle_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','shuttle_tab','🚐 Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='shuttle_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','shuttle_tab','🚐 Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='shuttle_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','shuttle_tab','🚐 Shuttle');

-- hotel_tab
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='hotel_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','hotel_tab','🏨 Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='hotel_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','hotel_tab','🏨 Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='hotel_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','hotel_tab','🏨 Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='hotel_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','hotel_tab','🏨 Hotell');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='hotel_tab')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','hotel_tab','🏨 Hotel');

-- btn_send_bookings
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='btn_send_bookings')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','btn_send_bookings','📧 Invia Prenotazioni');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='btn_send_bookings')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','btn_send_bookings',N'📧 Trimite Rezervări');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='btn_send_bookings')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','btn_send_bookings','📧 Send Bookings');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='btn_send_bookings')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','btn_send_bookings','📧 Skicka Bokningar');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='btn_send_bookings')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','btn_send_bookings','📧 Buchungen senden');

-- btn_skip_booking
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='btn_skip_booking')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','btn_skip_booking','Salta Booking');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='btn_skip_booking')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','btn_skip_booking',N'Sări peste rezervare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='btn_skip_booking')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','btn_skip_booking','Skip Booking');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='btn_skip_booking')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','btn_skip_booking',N'Hoppa över bokning');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='btn_skip_booking')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','btn_skip_booking',N'Buchung überspringen');

-- airline
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','airline','Compagnia Aerea');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','airline',N'Companie Aeriană');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','airline','Airline');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','airline','Flygbolag');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','airline','Fluggesellschaft');

-- flight_number
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','flight_number','Numero Volo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','flight_number',N'Număr Zbor');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','flight_number','Flight Number');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','flight_number','Flygnummer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','flight_number','Flugnummer');

-- btn_search_flight
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='btn_search_flight')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','btn_search_flight','🔍 Cerca Orario');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='btn_search_flight')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','btn_search_flight',N'🔍 Caută Orar');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='btn_search_flight')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','btn_search_flight','🔍 Search Time');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='btn_search_flight')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','btn_search_flight',N'🔍 Sök Tid');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='btn_search_flight')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','btn_search_flight','🔍 Zeit suchen');

-- arrival_date
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='arrival_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','arrival_date','Data Arrivo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='arrival_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','arrival_date','Data Sosire');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='arrival_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','arrival_date','Arrival Date');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='arrival_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','arrival_date','Ankomstdatum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='arrival_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','arrival_date','Ankunftsdatum');

-- arrival_time
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='arrival_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','arrival_time','Ora Arrivo (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='arrival_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','arrival_time','Ora Sosire (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='arrival_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','arrival_time','Arrival Time (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='arrival_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','arrival_time','Ankomsttid (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='arrival_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','arrival_time','Ankunftszeit (HH:MM)');

-- departure_date
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='departure_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','departure_date','Data Partenza');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='departure_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','departure_date','Data Plecare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='departure_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','departure_date','Departure Date');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='departure_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','departure_date',N'Avgångsdatum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='departure_date')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','departure_date','Abreisedatum');

-- departure_time
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='departure_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','departure_time','Ora Partenza (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='departure_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','departure_time','Ora Plecare (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='departure_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','departure_time','Departure Time (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='departure_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','departure_time',N'Avgångstid (HH:MM)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='departure_time')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','departure_time','Abreisezeit (HH:MM)');

-- select_shuttle
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='select_shuttle')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','select_shuttle','Servizio Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='select_shuttle')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','select_shuttle','Serviciu Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='select_shuttle')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','select_shuttle','Shuttle Service');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='select_shuttle')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','select_shuttle','Shuttle Service');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='select_shuttle')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','select_shuttle','Shuttle Service');

-- shuttle_notes
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='shuttle_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','shuttle_notes','Note Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='shuttle_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','shuttle_notes',N'Observații Shuttle');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='shuttle_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','shuttle_notes','Shuttle Notes');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='shuttle_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','shuttle_notes','Shuttle Anteckningar');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='shuttle_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','shuttle_notes','Shuttle Notizen');

-- shuttle_info
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='shuttle_info')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','shuttle_info','⚠ Se l''arrivo è dopo le 16:00 la destinazione sarà l''Hotel. Altrimenti la fabbrica.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='shuttle_info')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','shuttle_info',N'⚠ Dacă sosirea este după ora 16:00, destinația va fi Hotelul. Altfel, fabrica.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='shuttle_info')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','shuttle_info','⚠ If arrival is after 16:00, destination will be the Hotel. Otherwise, the factory.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='shuttle_info')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','shuttle_info',N'⚠ Om ankomst är efter 16:00, destination blir hotellet. Annars fabriken.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='shuttle_info')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','shuttle_info','⚠ Bei Ankunft nach 16:00 Uhr ist das Ziel das Hotel. Sonst die Fabrik.');

-- select_hotel
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='select_hotel')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','select_hotel','Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='select_hotel')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','select_hotel','Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='select_hotel')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','select_hotel','Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='select_hotel')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','select_hotel','Hotell');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='select_hotel')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','select_hotel','Hotel');

-- hotel_notes
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='hotel_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','hotel_notes','Note Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='hotel_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','hotel_notes',N'Observații Hotel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='hotel_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','hotel_notes','Hotel Notes');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='hotel_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','hotel_notes','Hotell Anteckningar');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='hotel_notes')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','hotel_notes','Hotel Notizen');

-- enter_flight_number
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='enter_flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','enter_flight_number','Inserire il numero del volo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='enter_flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','enter_flight_number',N'Introduceți numărul zborului');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='enter_flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','enter_flight_number','Enter the flight number');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='enter_flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','enter_flight_number','Ange flygnumret');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='enter_flight_number')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','enter_flight_number','Flugnummer eingeben');

-- flight_search_manual
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='flight_search_manual')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','flight_search_manual','Ricerca automatica non disponibile. Inserire data e ora manualmente.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='flight_search_manual')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','flight_search_manual',N'Căutare automată indisponibilă. Introduceți data și ora manual.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='flight_search_manual')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','flight_search_manual','Automatic search not available. Enter date and time manually.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='flight_search_manual')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','flight_search_manual',N'Automatisk sökning ej tillgänglig. Ange datum och tid manuellt.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='flight_search_manual')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','flight_search_manual',N'Automatische Suche nicht verfügbar. Datum und Uhrzeit manuell eingeben.');

-- confirm_new_airline
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='confirm_new_airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','confirm_new_airline','La compagnia aerea non esiste. Crearla?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='confirm_new_airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','confirm_new_airline',N'Compania aeriană nu există. O creați?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='confirm_new_airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','confirm_new_airline','The airline does not exist. Create it?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='confirm_new_airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','confirm_new_airline',N'Flygbolaget finns inte. Skapa det?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='confirm_new_airline')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','confirm_new_airline','Die Fluggesellschaft existiert nicht. Erstellen?');

-- no_booking_selected
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='no_booking_selected')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','no_booking_selected','Nessuna prenotazione selezionata.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='no_booking_selected')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','no_booking_selected',N'Nicio rezervare selectată.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='no_booking_selected')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','no_booking_selected','No booking selected.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='no_booking_selected')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','no_booking_selected','Ingen bokning vald.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='no_booking_selected')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','no_booking_selected',N'Keine Buchung ausgewählt.');

-- confirm_new_company (usato in guests_gui.py)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='confirm_new_company')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('it','confirm_new_company','La società non esiste. Crearla?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='confirm_new_company')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('ro','confirm_new_company',N'Compania nu există. O creați?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='confirm_new_company')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('en','confirm_new_company','The company does not exist. Create it?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='confirm_new_company')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('sv','confirm_new_company',N'Företaget finns inte. Skapa det?');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='confirm_new_company')
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES ('de','confirm_new_company','Das Unternehmen existiert nicht. Erstellen?');

PRINT 'Traduzioni Guest Booking inserite con successo.';
