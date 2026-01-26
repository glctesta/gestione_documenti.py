-- Script SQL traduzioni aggiuntive Dynamic Shipping Management
-- N davanti a tutte le traduzioni per Unicode

-- all_customers
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'all_customers')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'all_customers', N'Tutti i Clienti'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'all_customers')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'all_customers', N'All Customers'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'all_customers')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'all_customers', N'Toți Clienții'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'all_customers')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('de', 'all_customers', N'Alle Kunden'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'all_customers')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('sv', 'all_customers', N'Alla Kunder'); END

-- sale_order
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'sale_order', N'Ordine Vendita'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'sale_order', N'Sale Order'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'sale_order', N'Comandă Vânzare'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('de', 'sale_order', N'Verkaufsauftrag'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('sv', 'sale_order', N'Försäljningsorder'); END

-- all_products
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'all_products')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'all_products', N'Tutti i Prodotti'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'all_products')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'all_products', N'All Products'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'all_products')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'all_products', N'Toate Produsele'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'all_products')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('de', 'all_products', N'Alle Produkte'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'all_products')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('sv', 'all_products', N'Alla Produkter'); END

-- ship_date_from
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'ship_date_from')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'ship_date_from', N'Data Spedizione Da'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'ship_date_from')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'ship_date_from', N'Ship Date From'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'ship_date_from')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'ship_date_from', N'Data Expediere De la'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'ship_date_from')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('de', 'ship_date_from', N'Versanddatum Von'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'ship_date_from')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('sv', 'ship_date_from', N'Fraktdatum Från'); END

-- ship_date_to
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'ship_date_to')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'ship_date_to', N'A'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'ship_date_to')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'ship_date_to', N'To'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'ship_date_to')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'ship_date_to', N'Până la'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'ship_date_to')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('de', 'ship_date_to', N'Bis'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'ship_date_to')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('sv', 'ship_date_to', N'Till'); END

-- col_sale_order
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_sale_order', N'Ord. Vendita'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_sale_order', N'Sale Order'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_sale_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_sale_order', N'Cmd. Vânzare'); END

-- col_item_code
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_item_code')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_item_code', N'Codice'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_item_code')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_item_code', N'Item Code'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_item_code')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_item_code', N'Cod Articol'); END

-- col_item_name
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_item_name')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_item_name', N'Prodotto'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_item_name')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_item_name', N'Product'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_item_name')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_item_name', N'Produs'); END

-- col_associate
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_associate')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_associate', N'Associate'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_associate')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_associate', N'Associate'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_associate')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_associate', N'Asociat'); END

-- col_smt, col_pthm, col_ict, col_fct (acronimi uguali in tutte le lingue)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_smt')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_smt', N'SMT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_smt')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_smt', N'SMT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_smt')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_smt', N'SMT'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_pthm')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_pthm', N'PTHM'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_pthm')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_pthm', N'PTHM'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_pthm')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_pthm', N'PTHM'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_ict')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_ict', N'ICT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_ict')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_ict', N'ICT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_ict')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_ict', N'ICT'); END

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_fct')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_fct', N'FCT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_fct')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_fct', N'FCT'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_fct')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_fct', N'FCT'); END

-- col_coating
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_coating')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_coating', N'Coating'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_coating')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_coating', N'Coating'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_coating')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_coating', N'Acoperire'); END

-- col_outofbox
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_outofbox')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_outofbox', N'OutOfBox'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_outofbox')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_outofbox', N'Out Of Box'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_outofbox')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_outofbox', N'Din Cutie'); END

-- col_shipped
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_shipped')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_shipped', N'Spediti'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_shipped')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_shipped', N'Shipped'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_shipped')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_shipped', N'Expediate'); END

-- btn_edit_rule
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_edit_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'btn_edit_rule', N'Modifica'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_edit_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'btn_edit_rule', N'Edit'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_edit_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'btn_edit_rule', N'Modifică'); END

-- btn_delete_rule
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_delete_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'btn_delete_rule', N'Elimina'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_delete_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'btn_delete_rule', N'Delete'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_delete_rule')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'btn_delete_rule', N'Șterge'); END

-- selected_order
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'selected_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'selected_order', N'Ordine selezionato'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'selected_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'selected_order', N'Selected order'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'selected_order')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'selected_order', N'Comandă selectată'); END

-- col_added_by
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_added_by')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_added_by', N'Aggiunto Da'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_added_by')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_added_by', N'Added By'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_added_by')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_added_by', N'Adăugat De'); END

-- col_date_added
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_date_added')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('it', 'col_date_added', N'Data Inserimento'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_date_added')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('en', 'col_date_added', N'Date Added'); END
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_date_added')
BEGIN INSERT INTO [Traceability_RS].[dbo].[AppTranslations] VALUES ('ro', 'col_date_added', N'Data Adăugării'); END

-- Verifica
SELECT [TranslationKey], [LanguageCode], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] IN ('all_customers', 'sale_order', 'all_products', 'ship_date_from', 'ship_date_to',
                            'col_sale_order', 'col_item_code', 'col_item_name', 'col_associate', 'col_smt',
                            'col_pthm', 'col_ict', 'col_fct', 'col_coating', 'col_outofbox', 'col_shipped',
                            'btn_edit_rule', 'btn_delete_rule', 'selected_order', 'col_added_by', 'col_date_added')
ORDER BY [TranslationKey], [LanguageCode];
