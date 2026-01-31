-- =============================================
-- Script per aggiungere traduzioni colonne shipping rules
-- Lingue: ro, it, en, de, sv
-- =============================================

-- Prod Order
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_prod_order', N'Ordine Prod.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_prod_order', N'Prod. Order');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_prod_order', N'Comandă Prod.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_prod_order', N'Prod. Auftrag');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_prod_order' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_prod_order', N'Prod. Order');

-- Requested On
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_requested_on', N'Richiesto Il');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_requested_on', N'Requested On');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_requested_on', N'Solicitat Pe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_requested_on', N'Angefordert Am');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_requested_on' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_requested_on', N'Begärd Den');

-- Request Date To Ship
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_request_date_to_ship', N'Data Spedizione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_request_date_to_ship', N'Ship Date');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_request_date_to_ship', N'Data Expediere');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_request_date_to_ship', N'Versanddatum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_date_to_ship' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_request_date_to_ship', N'Leveransdatum');

-- Request Qty
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_request_qty', N'Qtà Richiesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_request_qty', N'Request Qty');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_request_qty', N'Cant. Solicitată');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_request_qty', N'Angeforderte Menge');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_request_qty' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_request_qty', N'Begärd Kvantitet');

-- Remain Over PO
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_remain_over_po', N'Rim. su PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_remain_over_po', N'Remain on PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_remain_over_po', N'Rămas pe PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_remain_over_po', N'Verbleibend auf PO');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_po' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_remain_over_po', N'Kvar på PO');

-- Remain Over Request
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_remain_over_request', N'Rim. su Richiesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_remain_over_request', N'Remain on Request');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_remain_over_request', N'Rămas pe Solicitare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_remain_over_request', N'Verbleibend auf Anfrage');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'col_remain_over_request' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_remain_over_request', N'Kvar på Begäran');

PRINT 'Traduzioni per colonne shipping rules aggiunte con successo!';
