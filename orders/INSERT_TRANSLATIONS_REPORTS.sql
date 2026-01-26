-- Script per aggiungere le traduzioni per Orders Reports
-- Database: Traceability_RS
-- Tabella: dbo.AppTranslations
-- Struttura: LanguageCode, TranslationKey, TranslationValue

USE [Traceability_RS]
GO

BEGIN TRANSACTION;

DECLARE @translations TABLE (
    LanguageCode NVARCHAR(10),
    TranslationKey NVARCHAR(255),
    TranslationValue NVARCHAR(MAX)
);

-- Inserisci tutte le traduzioni
INSERT INTO @translations (LanguageCode, TranslationKey, TranslationValue) VALUES
-- ITALIANO (IT)
('IT', 'orders_reports_title', 'Rapporti Ordini'),
('IT', 'tab_summary', 'Riepilogo Generale'),
('IT', 'tab_customer', 'Per Cliente'),
('IT', 'tab_associations', 'Associazioni Produzione'),
('IT', 'tab_workload', 'Carichi di Lavoro'),
('IT', 'period', 'Periodo'),
('IT', 'btn_generate', 'Genera Rapporto'),
('IT', 'btn_export_excel', 'Esporta Excel'),
('IT', 'btn_load_customers', 'Carica Clienti'),
('IT', 'select_customer', 'Seleziona Cliente'),
('IT', 'customer_stats', 'Statistiche Cliente'),
('IT', 'select_customer_first', 'Seleziona un cliente'),
('IT', 'kpi', 'Indicatori Chiave'),
('IT', 'total_orders', 'Ordini Totali'),
('IT', 'open_orders', 'Ordini Aperti'),
('IT', 'completed_orders', 'Ordini Completati'),
('IT', 'overdue_orders', 'Ordini in Ritardo'),
('IT', 'total_value', 'Valore Totale (€)'),
('IT', 'col_status', 'Stato'),
('IT', 'col_value', 'Valore (€)'),
('IT', 'col_sale_product', 'Prodotto Vendita'),
('IT', 'col_prod_product', 'Prodotto Produzione'),
('IT', 'col_total_ordered', 'Qtà Totale Ordinata'),
('IT', 'col_total_assigned', 'Qtà Totale Assegnata'),
('IT', 'col_total_remaining', 'Qtà Rimanente'),
('IT', 'col_orders_count', 'N. Ordini'),
('IT', 'col_avg_value', 'Valore Medio'),
('IT', 'status_completed', 'Completato'),
('IT', 'status_in_progress', 'In Corso'),
('IT', 'status_overdue', 'In Ritardo'),
('IT', 'save_excel', 'Salva Excel'),
('IT', 'file_saved', 'File salvato'),

-- INGLESE (EN)
('EN', 'orders_reports_title', 'Orders Reports'),
('EN', 'tab_summary', 'General Summary'),
('EN', 'tab_customer', 'By Customer'),
('EN', 'tab_associations', 'Production Associations'),
('EN', 'tab_workload', 'Workload'),
('EN', 'period', 'Period'),
('EN', 'btn_generate', 'Generate Report'),
('EN', 'btn_export_excel', 'Export Excel'),
('EN', 'btn_load_customers', 'Load Customers'),
('EN', 'select_customer', 'Select Customer'),
('EN', 'customer_stats', 'Customer Statistics'),
('EN', 'select_customer_first', 'Select a customer'),
('EN', 'kpi', 'Key Indicators'),
('EN', 'total_orders', 'Total Orders'),
('EN', 'open_orders', 'Open Orders'),
('EN', 'completed_orders', 'Completed Orders'),
('EN', 'overdue_orders', 'Overdue Orders'),
('EN', 'total_value', 'Total Value (€)'),
('EN', 'col_status', 'Status'),
('EN', 'col_value', 'Value (€)'),
('EN', 'col_sale_product', 'Sale Product'),
('EN', 'col_prod_product', 'Production Product'),
('EN', 'col_total_ordered', 'Total Ordered Qty'),
('EN', 'col_total_assigned', 'Total Assigned Qty'),
('EN', 'col_total_remaining', 'Remaining Qty'),
('EN', 'col_orders_count', 'Orders Count'),
('EN', 'col_avg_value', 'Average Value'),
('EN', 'status_completed', 'Completed'),
('EN', 'status_in_progress', 'In Progress'),
('EN', 'status_overdue', 'Overdue'),
('EN', 'save_excel', 'Save Excel'),
('EN', 'file_saved', 'File saved'),

-- RUMENO (RO) - con N prefix per Unicode
('RO', 'orders_reports_title', 'Rapoarte Comenzi'),
('RO', 'tab_summary', 'Rezumat General'),
('RO', 'tab_customer', 'Pe Client'),
('RO', 'tab_associations', N'Asocieri Producție'),
('RO', 'tab_workload', N'Sarcină de Lucru'),
('RO', 'period', N'Perioadă'),
('RO', 'btn_generate', N'Generează Raport'),
('RO', 'btn_export_excel', N'Exportă Excel'),
('RO', 'btn_load_customers', N'Încarcă Clienți'),
('RO', 'select_customer', N'Selectează Client'),
('RO', 'customer_stats', 'Statistici Client'),
('RO', 'select_customer_first', N'Selectați un client'),
('RO', 'kpi', 'Indicatori Cheie'),
('RO', 'total_orders', 'Comenzi Totale'),
('RO', 'open_orders', 'Comenzi Deschise'),
('RO', 'completed_orders', 'Comenzi Finalizate'),
('RO', 'overdue_orders', N'Comenzi Întârziate'),
('RO', 'total_value', N'Valoare Totală (€)'),
('RO', 'col_status', 'Stare'),
('RO', 'col_value', N'Valoare (€)'),
('RO', 'col_sale_product', N'Produs Vânzare'),
('RO', 'col_prod_product', N'Produs Producție'),
('RO', 'col_total_ordered', N'Cantitate Totală Comandată'),
('RO', 'col_total_assigned', N'Cantitate Totală Alocată'),
('RO', 'col_total_remaining', N'Cantitate Rămasă'),
('RO', 'col_orders_count', 'Nr. Comenzi'),
('RO', 'col_avg_value', 'Valoare Medie'),
('RO', 'status_completed', 'Finalizat'),
('RO', 'status_in_progress', N'În Desfășurare'),
('RO', 'status_overdue', N'Întârziat'),
('RO', 'save_excel', N'Salvează Excel'),
('RO', 'file_saved', N'Fișier salvat'),

-- TEDESCO (DE)
('DE', 'orders_reports_title', 'Auftragsberichte'),
('DE', 'tab_summary', 'Allgemeine Übersicht'),
('DE', 'tab_customer', 'Nach Kunde'),
('DE', 'tab_associations', 'Produktionszuordnungen'),
('DE', 'tab_workload', 'Arbeitsbelastung'),
('DE', 'period', 'Zeitraum'),
('DE', 'btn_generate', 'Bericht erstellen'),
('DE', 'btn_export_excel', 'Excel exportieren'),
('DE', 'btn_load_customers', 'Kunden laden'),
('DE', 'select_customer', 'Kunde auswählen'),
('DE', 'customer_stats', 'Kundenstatistiken'),
('DE', 'select_customer_first', 'Wählen Sie einen Kunden'),
('DE', 'kpi', 'Schlüsselindikatoren'),
('DE', 'total_orders', 'Gesamtaufträge'),
('DE', 'open_orders', 'Offene Aufträge'),
('DE', 'completed_orders', 'Abgeschlossene Aufträge'),
('DE', 'overdue_orders', 'Überfällige Aufträge'),
('DE', 'total_value', 'Gesamtwert (€)'),
('DE', 'col_status', 'Status'),
('DE', 'col_value', 'Wert (€)'),
('DE', 'col_sale_product', 'Verkaufsprodukt'),
('DE', 'col_prod_product', 'Produktionsprodukt'),
('DE', 'col_total_ordered', 'Gesamt bestellte Menge'),
('DE', 'col_total_assigned', 'Gesamt zugewiesene Menge'),
('DE', 'col_total_remaining', 'Verbleibende Menge'),
('DE', 'col_orders_count', 'Anzahl Aufträge'),
('DE', 'col_avg_value', 'Durchschnittswert'),
('DE', 'status_completed', 'Abgeschlossen'),
('DE', 'status_in_progress', 'In Bearbeitung'),
('DE', 'status_overdue', 'Überfällig'),
('DE', 'save_excel', 'Excel speichern'),
('DE', 'file_saved', 'Datei gespeichert'),

-- SVEDESE (SV)
('SV', 'orders_reports_title', 'Orderrapporter'),
('SV', 'tab_summary', 'Allmän sammanfattning'),
('SV', 'tab_customer', 'Efter kund'),
('SV', 'tab_associations', 'Produktionskopplingar'),
('SV', 'tab_workload', 'Arbetsbelastning'),
('SV', 'period', 'Period'),
('SV', 'btn_generate', 'Generera rapport'),
('SV', 'btn_export_excel', 'Exportera Excel'),
('SV', 'btn_load_customers', 'Ladda kunder'),
('SV', 'select_customer', 'Välj kund'),
('SV', 'customer_stats', 'Kundstatistik'),
('SV', 'select_customer_first', 'Välj en kund'),
('SV', 'kpi', 'Nyckelindikatorer'),
('SV', 'total_orders', 'Totalt antal order'),
('SV', 'open_orders', 'Öppna order'),
('SV', 'completed_orders', 'Slutförda order'),
('SV', 'overdue_orders', 'Försenade order'),
('SV', 'total_value', 'Totalt värde (€)'),
('SV', 'col_status', 'Status'),
('SV', 'col_value', 'Värde (€)'),
('SV', 'col_sale_product', 'Försäljningsprodukt'),
('SV', 'col_prod_product', 'Produktionsprodukt'),
('SV', 'col_total_ordered', 'Total beställd kvantitet'),
('SV', 'col_total_assigned', 'Total tilldelad kvantitet'),
('SV', 'col_total_remaining', 'Återstående kvantitet'),
('SV', 'col_orders_count', 'Antal order'),
('SV', 'col_avg_value', 'Genomsnittligt värde'),
('SV', 'status_completed', 'Slutförd'),
('SV', 'status_in_progress', 'Pågående'),
('SV', 'status_overdue', 'Försenad'),
('SV', 'save_excel', 'Spara Excel'),
('SV', 'file_saved', 'Fil sparad');

-- Inserisci solo le traduzioni che non esistono già
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
SELECT t.LanguageCode, t.TranslationKey, t.TranslationValue
FROM @translations t
WHERE NOT EXISTS (
    SELECT 1 
    FROM [Traceability_RS].[dbo].[AppTranslations] a 
    WHERE a.LanguageCode = t.LanguageCode 
      AND a.TranslationKey = t.TranslationKey
);

DECLARE @InsertedCount INT = @@ROWCOUNT;
PRINT 'Inserite ' + CAST(@InsertedCount AS NVARCHAR(10)) + ' nuove traduzioni per Orders Reports';

-- Verifica traduzioni inserite
SELECT 
    LanguageCode,
    TranslationKey,
    TranslationValue
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE TranslationKey IN (SELECT DISTINCT TranslationKey FROM @translations)
ORDER BY TranslationKey, LanguageCode;

COMMIT TRANSACTION;

PRINT 'Script completato con successo!';
GO
