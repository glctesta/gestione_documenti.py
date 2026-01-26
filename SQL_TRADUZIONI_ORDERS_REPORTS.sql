-- Script SQL per inserire traduzioni Orders Reports Window
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: IT, RO, EN, DE, SV

-- Titolo finestra
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'orders_reports_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'orders_reports_title', 'Rapporti Ordini');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'orders_reports_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'orders_reports_title', N'Rapoarte Comenzi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'orders_reports_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'orders_reports_title', 'Orders Reports');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'orders_reports_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'orders_reports_title', 'Auftragsberichte');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'orders_reports_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'orders_reports_title', 'Orderrapporter');

-- Tab Riepilogo
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'tab_summary')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'tab_summary', 'Riepilogo Generale');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'tab_summary')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'tab_summary', N'Rezumat General');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'tab_summary')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'tab_summary', 'General Summary');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'tab_summary')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'tab_summary', 'Allgemeine Zusammenfassung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'tab_summary')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'tab_summary', 'Allmän sammanfattning');

-- Tab Cliente
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'tab_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'tab_customer', 'Per Cliente');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'tab_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'tab_customer', N'Pe Client');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'tab_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'tab_customer', 'By Customer');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'tab_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'tab_customer', 'Nach Kunde');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'tab_customer')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'tab_customer', 'Per kund');

-- Tab Associazioni
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'tab_associations')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'tab_associations', 'Associazioni Produzione');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'tab_associations')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'tab_associations', N'Asocieri Producție');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'tab_associations')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'tab_associations', 'Production Associations');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'tab_associations')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'tab_associations', 'Produktionszuordnungen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'tab_associations')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'tab_associations', 'Produktionsassociationer');

-- Tab Carichi Lavoro
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'tab_workload')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'tab_workload', 'Carichi di Lavoro');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'tab_workload')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'tab_workload', N'Sarcini de Lucru');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'tab_workload')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'tab_workload', 'Workload');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'tab_workload')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'tab_workload', 'Arbeitsbelastung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'tab_workload')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'tab_workload', 'Arbetsbelastning');

-- Bottoni
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'btn_generate')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'btn_generate', 'Genera Rapporto');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'btn_generate')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'btn_generate', N'Generează Raport');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'btn_generate')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'btn_generate', 'Generate Report');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'btn_generate')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'btn_generate', 'Bericht erstellen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'btn_generate')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'btn_generate', 'Generera rapport');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'btn_export_excel')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'btn_export_excel', 'Esporta Excel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'btn_export_excel')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'btn_export_excel', N'Exportă Excel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'btn_export_excel')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'btn_export_excel', 'Export Excel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'btn_export_excel')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'btn_export_excel', 'Excel exportieren');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'btn_export_excel')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'btn_export_excel', 'Exportera Excel');

-- KPI Labels
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'kpi_total_orders')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'kpi_total_orders', 'Ordini Totali');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'kpi_total_orders')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'kpi_total_orders', N'Comenzi Totale');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'kpi_total_orders')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'kpi_total_orders', 'Total Orders');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'kpi_total_orders')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'kpi_total_orders', 'Gesamtbestellungen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'kpi_total_orders')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'kpi_total_orders', 'Totala beställningar');

-- Colonne
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'IT' AND TranslationKey = 'col_so_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('IT', 'col_so_number', 'N. Ordine');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'RO' AND TranslationKey = 'col_so_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('RO', 'col_so_number', N'Nr. Comandă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'EN' AND TranslationKey = 'col_so_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('EN', 'col_so_number', 'Order No.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'DE' AND TranslationKey = 'col_so_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('DE', 'col_so_number', 'Bestellnr.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE LanguageCode = 'SV' AND TranslationKey = 'col_so_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('SV', 'col_so_number', 'Ordernr.');

PRINT 'Traduzioni Orders Reports Window inserite con successo!';
