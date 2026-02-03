-- Script per aggiungere traduzioni per Rapporti Fixtures
-- Eseguire su database Traceability_RS

USE [Traceability_RS]
GO

-- Sottomenu Rapporti (header)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_reports_header' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'submenu_reports_header', N'Rapporti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_reports_header' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'submenu_reports_header', N'Reports');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_reports_header' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'submenu_reports_header', N'Berichte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_reports_header' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'submenu_reports_header', N'Rapoarte');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_reports_header' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'submenu_reports_header', N'Rapporter');

-- Rapporti Fixtures (menu item)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_fixtures_report' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'submenu_fixtures_report', N'Rapporti Fixtures');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_fixtures_report' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'submenu_fixtures_report', N'Fixtures Report');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_fixtures_report' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'submenu_fixtures_report', N'Vorrichtungsbericht');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_fixtures_report' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'submenu_fixtures_report', N'Raport Dispozitive');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'submenu_fixtures_report' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'submenu_fixtures_report', N'Fixturrapport');

-- Titolo finestra
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'fixtures_report_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'fixtures_report_title', N'Rapporti Fixtures');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'fixtures_report_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'fixtures_report_title', N'Fixtures Report');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'fixtures_report_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'fixtures_report_title', N'Vorrichtungsbericht');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'fixtures_report_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'fixtures_report_title', N'Raport Dispozitive');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'fixtures_report_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'fixtures_report_title', N'Fixturrapport');

-- Colonne
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_equipment' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_equipment', N'Equipaggiamento');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_equipment' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_equipment', N'Equipment');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_equipment' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_equipment', N'Ausrüstung');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_equipment' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_equipment', N'Echipament');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_equipment' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_equipment', N'Utrustning');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_qty_scan' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_qty_scan', N'Cicli Totali');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_qty_scan' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_qty_scan', N'Total Cycles');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_qty_scan' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_qty_scan', N'Gesamtzyklen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_qty_scan' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_qty_scan', N'Cicluri Totale');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_qty_scan' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_qty_scan', N'Totala Cykler');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_critical_status' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_critical_status', N'Stato Critico');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_critical_status' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_critical_status', N'Critical Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_critical_status' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_critical_status', N'Kritischer Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_critical_status' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_critical_status', N'Stare Critică');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_critical_status' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_critical_status', N'Kritisk Status');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_maintenance_msg' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_maintenance_msg', N'Messaggio Manutenzione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_maintenance_msg' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_maintenance_msg', N'Maintenance Message');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_maintenance_msg' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_maintenance_msg', N'Wartungsnachricht');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_maintenance_msg' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_maintenance_msg', N'Mesaj Întreținere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_maintenance_msg' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_maintenance_msg', N'Underhållsmeddelande');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_last_maint' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_last_maint', N'Ultima Manutenzione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_last_maint' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_last_maint', N'Last Maintenance');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_last_maint' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_last_maint', N'Letzte Wartung');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_last_maint' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_last_maint', N'Ultima Întreținere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_last_maint' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_last_maint', N'Senaste Underhåll');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_no_cycle' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'col_no_cycle', N'Cicli Previsti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_no_cycle' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'col_no_cycle', N'Expected Cycles');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_no_cycle' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'col_no_cycle', N'Erwartete Zyklen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_no_cycle' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'col_no_cycle', N'Cicluri Așteptate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'col_no_cycle' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'col_no_cycle', N'Förväntade Cykler');

-- Filtri
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'equipment_filter' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'equipment_filter', N'Equipaggiamento:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'equipment_filter' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'equipment_filter', N'Equipment:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'equipment_filter' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'equipment_filter', N'Ausrüstung:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'equipment_filter' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'equipment_filter', N'Echipament:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'equipment_filter' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'equipment_filter', N'Utrustning:');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'no_cycle_filter' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'no_cycle_filter', N'Cicli Previsti:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'no_cycle_filter' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'no_cycle_filter', N'Expected Cycles:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'no_cycle_filter' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'no_cycle_filter', N'Erwartete Zyklen:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'no_cycle_filter' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'no_cycle_filter', N'Cicluri Așteptate:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'no_cycle_filter' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'no_cycle_filter', N'Förväntade Cykler:');

-- Bottoni
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_apply_filters' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'btn_apply_filters', N'Applica Filtri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_apply_filters' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'btn_apply_filters', N'Apply Filters');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_apply_filters' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'btn_apply_filters', N'Filter Anwenden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_apply_filters' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'btn_apply_filters', N'Aplică Filtre');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_apply_filters' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'btn_apply_filters', N'Tillämpa Filter');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_export_excel' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'btn_export_excel', N'Esporta Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_export_excel' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'btn_export_excel', N'Export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_export_excel' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'btn_export_excel', N'Excel Exportieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_export_excel' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'btn_export_excel', N'Exportă Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_export_excel' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'btn_export_excel', N'Exportera Excel');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_reset' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'btn_reset', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_reset' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'btn_reset', N'Reset');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_reset' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'btn_reset', N'Zurücksetzen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_reset' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'btn_reset', N'Resetare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'btn_reset' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'btn_reset', N'Återställ');

-- Ordinamento
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'sorted_by' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'sorted_by', N'Ordinato per: ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'sorted_by' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'sorted_by', N'Sorted by: ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'sorted_by' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'sorted_by', N'Sortiert nach: ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'sorted_by' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'sorted_by', N'Sortat după: ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'sorted_by' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'sorted_by', N'Sorterat efter: ');

-- Messaggi
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'invalid_no_cycle' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'invalid_no_cycle', N'Cicli Previsti deve essere un numero');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'invalid_no_cycle' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'invalid_no_cycle', N'Expected Cycles must be a number');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'invalid_no_cycle' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'invalid_no_cycle', N'Erwartete Zyklen muss eine Zahl sein');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'invalid_no_cycle' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'invalid_no_cycle', N'Cicluri Așteptate trebuie să fie un număr');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'invalid_no_cycle' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'invalid_no_cycle', N'Förväntade Cykler måste vara ett nummer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'export_success' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'export_success', N'Esportazione completata');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'export_success' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'export_success', N'Export completed');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'export_success' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'export_success', N'Export abgeschlossen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'export_success' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'export_success', N'Export finalizat');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'export_success' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'export_success', N'Export slutförd');

-- Messaggi caricamento
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'loading', N'Caricamento...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'loading', N'Loading...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'loading', N'Laden...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'loading', N'Se încarcă...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'loading', N'Laddar...');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading_fixtures_data' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'loading_fixtures_data', N'Caricamento dati fixtures in corso...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading_fixtures_data' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'loading_fixtures_data', N'Loading fixtures data...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading_fixtures_data' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'loading_fixtures_data', N'Lade Vorrichtungsdaten...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading_fixtures_data' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'loading_fixtures_data', N'Se încarcă datele dispozitivelor...');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'loading_fixtures_data' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'loading_fixtures_data', N'Laddar fixturdata...');

-- Domanda apertura file
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'open_file_question' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'open_file_question', N'Vuoi aprire il file?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'open_file_question' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'open_file_question', N'Do you want to open the file?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'open_file_question' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'open_file_question', N'Möchten Sie die Datei öffnen?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'open_file_question' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'open_file_question', N'Doriți să deschideți fișierul?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'open_file_question' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'open_file_question', N'Vill du öppna filen?');

-- Errore apertura file
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'cannot_open_file' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'cannot_open_file', N'Impossibile aprire il file');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'cannot_open_file' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'cannot_open_file', N'Cannot open file');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'cannot_open_file' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'cannot_open_file', N'Datei kann nicht geöffnet werden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'cannot_open_file' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'cannot_open_file', N'Nu se poate deschide fișierul');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'cannot_open_file' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'cannot_open_file', N'Kan inte öppna filen');

GO

PRINT N'✅ Traduzioni per Rapporti Fixtures aggiunte con successo!'
PRINT N'   - 18 chiavi di traduzione'
PRINT N'   - 5 lingue (IT, EN, DE, RO, SV)'
PRINT N'   - Totale: 90 traduzioni inserite'
PRINT N''
PRINT N'Chiavi tradotte:'
PRINT N'  • submenu_reports_header'
PRINT N'  • submenu_fixtures_report'
PRINT N'  • fixtures_report_title'
PRINT N'  • col_equipment'
PRINT N'  • col_qty_scan'
PRINT N'  • col_critical_status'
PRINT N'  • col_maintenance_msg'
PRINT N'  • col_last_maint'
PRINT N'  • col_no_cycle'
PRINT N'  • equipment_filter'
PRINT N'  • no_cycle_filter'
PRINT N'  • btn_apply_filters'
PRINT N'  • btn_export_excel'
PRINT N'  • btn_reset'
PRINT N'  • sorted_by'
PRINT N'  • invalid_no_cycle'
PRINT N'  • export_success'
PRINT N'  • loading'
PRINT N'  • loading_fixtures_data'
PRINT N'  • open_file_question'
PRINT N'  • cannot_open_file'
