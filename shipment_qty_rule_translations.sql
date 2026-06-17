-- shipment_qty_rule_translations.sql
-- Nuove chiavi per la regola quantità conferma spedizioni:
--   il tetto è la quantità residua dell'ordine di produzione (Orders.OrderQuantity
--   meno il già spedito/confermato dello stesso ordine), non più la quantità prodotta.
-- Lingue: it, en, ro, de, sv

-- shipment_qty_hint
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_hint' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','shipment_qty_hint','(prodotta: {0} | richiesta: {1} | max ordine: {2})');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_hint' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','shipment_qty_hint','(produced: {0} | requested: {1} | order max: {2})');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_hint' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro',N'shipment_qty_hint',N'(produs: {0} | cerut: {1} | max comandă: {2})');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_hint' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de',N'shipment_qty_hint',N'(produziert: {0} | angefordert: {1} | Auftrag max: {2})');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_hint' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv',N'shipment_qty_hint',N'(producerad: {0} | begärd: {1} | order max: {2})');

-- shipment_qty_over_order
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_over_order' AND LanguageCode='it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','shipment_qty_over_order',N'La quantità confermata ({0}) non può superare la quantità residua dell''ordine ({1}) = quantità ordine ({2}) − già spedito ({3}).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_over_order' AND LanguageCode='en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en',N'shipment_qty_over_order',N'The confirmed quantity ({0}) cannot exceed the order remaining ({1}) = order quantity ({2}) − already shipped ({3}).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_over_order' AND LanguageCode='ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro',N'shipment_qty_over_order',N'Cantitatea confirmată ({0}) nu poate depăși cantitatea rămasă a comenzii ({1}) = cantitate comandă ({2}) − deja expediat ({3}).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_over_order' AND LanguageCode='de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de',N'shipment_qty_over_order',N'Die bestätigte Menge ({0}) darf die Restmenge des Auftrags ({1}) nicht überschreiten = Auftragsmenge ({2}) − bereits versandt ({3}).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey='shipment_qty_over_order' AND LanguageCode='sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv',N'shipment_qty_over_order',N'Den bekräftade kvantiteten ({0}) kan inte överstiga orderns återstående ({1}) = orderkvantitet ({2}) − redan skickat ({3}).');
