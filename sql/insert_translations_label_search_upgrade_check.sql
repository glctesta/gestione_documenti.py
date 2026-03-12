-- ============================================================
-- Traduzioni per: Ricerca ordini etichette + Verifica upgrade
-- Data: 2026-03-12
-- ============================================================

-- search_button
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'search_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'search_button', '🔍 Cerca');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'search_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'search_button', N'🔍 Caută');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'search_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'search_button', '🔍 Search');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'search_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'search_button', '🔍 Sök');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'search_button')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'search_button', '🔍 Suchen');

-- enter_order_search
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'enter_order_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'enter_order_search', 'Inserisci un numero ordine o parte di esso');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'enter_order_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'enter_order_search', N'Introduceți un număr de comandă sau o parte din acesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'enter_order_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'enter_order_search', 'Enter an order number or part of it');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'enter_order_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'enter_order_search', 'Ange ett ordernummer eller en del av det');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'enter_order_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'enter_order_search', 'Geben Sie eine Bestellnummer oder einen Teil davon ein');

-- no_orders_found_search
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'no_orders_found_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'no_orders_found_search', 'Nessun ordine trovato per "{0}"');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'no_orders_found_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'no_orders_found_search', N'Nicio comandă găsită pentru „{0}"');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'no_orders_found_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'no_orders_found_search', 'No orders found for "{0}"');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'no_orders_found_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'no_orders_found_search', 'Inga ordrar hittades för "{0}"');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'no_orders_found_search')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'no_orders_found_search', 'Keine Bestellungen gefunden für "{0}"');

-- update_postponed_title
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_postponed_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'update_postponed_title', 'Aggiornamento Posticipato');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_postponed_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'update_postponed_title', N'Actualizare Amânată');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_postponed_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'update_postponed_title', 'Update Postponed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_postponed_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'update_postponed_title', 'Uppdatering Uppskjuten');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_postponed_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'update_postponed_title', 'Aktualisierung Verschoben');

-- update_postponed_message
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'update_postponed_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('it', 'update_postponed_message', 'L''aggiornamento è stato posticipato perché il file sorgente non è ancora pronto.

Motivo: {0}

L''aggiornamento verrà riprovato automaticamente.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'update_postponed_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('ro', 'update_postponed_message', N'Actualizarea a fost amânată deoarece fișierul sursă nu este încă pregătit.

Motiv: {0}

Actualizarea va fi reîncercată automat.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'update_postponed_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('en', 'update_postponed_message', 'The update has been postponed because the source file is not ready yet.

Reason: {0}

The update will be retried automatically.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'update_postponed_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('sv', 'update_postponed_message', 'Uppdateringen har skjutits upp eftersom källfilen inte är klar ännu.

Anledning: {0}

Uppdateringen kommer att försökas igen automatiskt.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'update_postponed_message')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES ('de', 'update_postponed_message', 'Die Aktualisierung wurde verschoben, da die Quelldatei noch nicht bereit ist.

Grund: {0}

Die Aktualisierung wird automatisch erneut versucht.');
