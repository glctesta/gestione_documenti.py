-- Script SQL completo traduzioni Dynamic Shipping Management
-- N davanti a tutte le traduzioni per Unicode

-- Titoli e sezioni
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'dynamic_shipping_title')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'dynamic_shipping_title', N'Gestione Spedizioni Dinamiche'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'dynamic_shipping_title')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'dynamic_shipping_title', N'Dynamic Shipping Management'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'dynamic_shipping_title')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'dynamic_shipping_title', N'Gestionarea Expedierilor Dinamice'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'orders_data')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'orders_data', N'Dati Ordini'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'orders_data')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'orders_data', N'Orders Data'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'orders_data')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'orders_data', N'Date Comenzi'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'shipping_rules')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'shipping_rules', N'Regole di Spedizione'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'shipping_rules')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'shipping_rules', N'Shipping Rules'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'shipping_rules')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'shipping_rules', N'Reguli de Expediere'); END

-- Colonne
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_remain')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_remain', N'Rimanenti'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_remain')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_remain', N'Remaining'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_remain')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_remain', N'Rămase'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_qty_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_qty_to_ship', N'Qtà da Spedire'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_qty_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_qty_to_ship', N'Qty to Ship'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_qty_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_qty_to_ship', N'Cant. de Expediat'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_date_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_date_to_ship', N'Data Spedizione'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_date_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_date_to_ship', N'Ship Date'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_date_to_ship')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_date_to_ship', N'Data Expediere'); END

-- Bottoni
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_add_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'btn_add_rule', N'Aggiungi Regola'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_add_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'btn_add_rule', N'Add Rule'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_add_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'btn_add_rule', N'Adaugă Regulă'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_filter')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'btn_filter', N'Filtra'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_filter')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'btn_filter', N'Filter'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_filter')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'btn_filter', N'Filtrează'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_reset_filters')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'btn_reset_filters', N'Reset Filtri'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_reset_filters')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'btn_reset_filters', N'Reset Filters'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_reset_filters')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'btn_reset_filters', N'Resetare Filtre'); END

-- Messaggi
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'select_order_first')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'select_order_first', N'Seleziona un ordine sopra'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'select_order_first')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'select_order_first', N'Select an order above'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'select_order_first')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'select_order_first', N'Selectați o comandă mai sus'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'rule_saved')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'rule_saved', N'Regola salvata con successo'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'rule_saved')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'rule_saved', N'Rule saved successfully'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'rule_saved')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'rule_saved', N'Regulă salvată cu succes'); END

-- Verifica
SELECT [TranslationKey], [LanguageCode], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] LIKE '%shipping%' OR [TranslationKey] LIKE '%rule%'
ORDER BY [TranslationKey], [LanguageCode];
