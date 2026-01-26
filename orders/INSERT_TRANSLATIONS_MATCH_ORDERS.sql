-- Script per aggiungere le traduzioni per Match Production Orders
-- Database: Traceability_RS
-- Tabella: dbo.AppTranslations
-- Struttura: LanguageCode, TranslationKey, TranslationValue

USE [Traceability_RS]
GO

BEGIN TRANSACTION;

-- Traduzioni per Match Production Orders
DECLARE @translations TABLE (
    LanguageCode NVARCHAR(10),
    TranslationKey NVARCHAR(255),
    TranslationValue NVARCHAR(MAX)
);

-- Inserisci tutte le traduzioni
INSERT INTO @translations (LanguageCode, TranslationKey, TranslationValue) VALUES
-- ITALIANO (IT)
('IT', 'match_production_orders_title', 'Accoppia Ordini di Produzione'),
('IT', 'btn_match_production_orders', 'Accoppia Ordini Produzione'),
('IT', 'sale_orders', 'Ordini di Vendita'),
('IT', 'association', 'Associazione Ordini'),
('IT', 'filters', 'Filtri'),
('IT', 'so_number', 'N. Ordine:'),
('IT', 'customer', 'Cliente:'),
('IT', 'product', 'Prodotto:'),
('IT', 'date_from', 'Data Da:'),
('IT', 'date_to', 'Data A:'),
('IT', 'btn_apply_filter', 'Applica Filtri'),
('IT', 'btn_reset_filter', 'Resetta Filtri'),
('IT', 'col_qty_assigned', 'Qtà Assegnata'),
('IT', 'col_qty_remaining', 'Qtà Rimanente'),
('IT', 'col_production_order', 'Ordine Produzione'),
('IT', 'col_date_in', 'Data Ins.'),
('IT', 'selected_sale_order', 'Ordine di Vendita Selezionato'),
('IT', 'no_selection', 'Nessun ordine selezionato'),
('IT', 'add_production_order', 'Aggiungi Ordine di Produzione'),
('IT', 'production_order', 'Ordine di Produzione:'),
('IT', 'quantity', 'Quantità:'),
('IT', 'btn_add_association', 'Aggiungi Associazione'),
('IT', 'existing_associations', 'Associazioni Esistenti'),
('IT', 'btn_delete_association', 'Elimina Associazione'),
('IT', 'select_sale_order_first', 'Seleziona prima un ordine di vendita'),
('IT', 'select_production_order', 'Seleziona un ordine di produzione'),
('IT', 'invalid_quantity', 'Quantità non valida'),
('IT', 'qty_exceeds_remaining', 'La quantità eccede quella rimanente'),
('IT', 'association_created', 'Associazione creata con successo'),
('IT', 'select_association', 'Seleziona un''associazione da eliminare'),
('IT', 'confirm_delete_association', 'Confermare eliminazione associazione?'),
('IT', 'association_deleted', 'Associazione eliminata'),

-- INGLESE (EN)
('EN', 'match_production_orders_title', 'Match Production Orders'),
('EN', 'btn_match_production_orders', 'Match Production Orders'),
('EN', 'sale_orders', 'Sales Orders'),
('EN', 'association', 'Orders Association'),
('EN', 'filters', 'Filters'),
('EN', 'so_number', 'Order No:'),
('EN', 'customer', 'Customer:'),
('EN', 'product', 'Product:'),
('EN', 'date_from', 'Date From:'),
('EN', 'date_to', 'Date To:'),
('EN', 'btn_apply_filter', 'Apply Filters'),
('EN', 'btn_reset_filter', 'Reset Filters'),
('EN', 'col_qty_assigned', 'Qty Assigned'),
('EN', 'col_qty_remaining', 'Qty Remaining'),
('EN', 'col_production_order', 'Production Order'),
('EN', 'col_date_in', 'Date In'),
('EN', 'selected_sale_order', 'Selected Sales Order'),
('EN', 'no_selection', 'No order selected'),
('EN', 'add_production_order', 'Add Production Order'),
('EN', 'production_order', 'Production Order:'),
('EN', 'quantity', 'Quantity:'),
('EN', 'btn_add_association', 'Add Association'),
('EN', 'existing_associations', 'Existing Associations'),
('EN', 'btn_delete_association', 'Delete Association'),
('EN', 'select_sale_order_first', 'Select a sales order first'),
('EN', 'select_production_order', 'Select a production order'),
('EN', 'invalid_quantity', 'Invalid quantity'),
('EN', 'qty_exceeds_remaining', 'Quantity exceeds remaining'),
('EN', 'association_created', 'Association created successfully'),
('EN', 'select_association', 'Select an association to delete'),
('EN', 'confirm_delete_association', 'Confirm association deletion?'),
('EN', 'association_deleted', 'Association deleted'),

-- RUMENO (RO) - con N prefix per Unicode
('RO', 'match_production_orders_title', N'Asociază Ordine de Producție'),
('RO', 'btn_match_production_orders', N'Asociază Ordine Producție'),
('RO', 'sale_orders', N'Ordine de Vânzare'),
('RO', 'association', 'Asociere Ordine'),
('RO', 'filters', 'Filtre'),
('RO', 'so_number', N'Nr. Comandă:'),
('RO', 'customer', 'Client:'),
('RO', 'product', 'Produs:'),
('RO', 'date_from', 'Data De la:'),
('RO', 'date_to', N'Data Până la:'),
('RO', 'btn_apply_filter', N'Aplică Filtre'),
('RO', 'btn_reset_filter', N'Resetează Filtre'),
('RO', 'col_qty_assigned', N'Cantitate Alocată'),
('RO', 'col_qty_remaining', N'Cantitate Rămasă'),
('RO', 'col_production_order', N'Ordin Producție'),
('RO', 'col_date_in', 'Data Intrare'),
('RO', 'selected_sale_order', N'Ordin de Vânzare Selectat'),
('RO', 'no_selection', 'Niciun ordin selectat'),
('RO', 'add_production_order', N'Adaugă Ordin de Producție'),
('RO', 'production_order', N'Ordin de Producție:'),
('RO', 'quantity', 'Cantitate:'),
('RO', 'btn_add_association', N'Adaugă Asociere'),
('RO', 'existing_associations', 'Asocieri Existente'),
('RO', 'btn_delete_association', N'Șterge Asociere'),
('RO', 'select_sale_order_first', N'Selectați mai întâi un ordin de vânzare'),
('RO', 'select_production_order', N'Selectați un ordin de producție'),
('RO', 'invalid_quantity', N'Cantitate invalidă'),
('RO', 'qty_exceeds_remaining', N'Cantitatea depășește restul'),
('RO', 'association_created', N'Asociere creată cu succes'),
('RO', 'select_association', N'Selectați o asociere de șters'),
('RO', 'confirm_delete_association', N'Confirmați ștergerea asocierii?'),
('RO', 'association_deleted', N'Asociere ștearsă'),

-- TEDESCO (DE)
('DE', 'match_production_orders_title', 'Produktionsaufträge zuordnen'),
('DE', 'btn_match_production_orders', 'Produktionsaufträge zuordnen'),
('DE', 'sale_orders', 'Verkaufsaufträge'),
('DE', 'association', 'Auftragszuordnung'),
('DE', 'filters', 'Filter'),
('DE', 'so_number', 'Auftragsnr.:'),
('DE', 'customer', 'Kunde:'),
('DE', 'product', 'Produkt:'),
('DE', 'date_from', 'Datum Von:'),
('DE', 'date_to', 'Datum Bis:'),
('DE', 'btn_apply_filter', 'Filter anwenden'),
('DE', 'btn_reset_filter', 'Filter zurücksetzen'),
('DE', 'col_qty_assigned', 'Zugewiesene Menge'),
('DE', 'col_qty_remaining', 'Verbleibende Menge'),
('DE', 'col_production_order', 'Produktionsauftrag'),
('DE', 'col_date_in', 'Eingangsdatum'),
('DE', 'selected_sale_order', 'Ausgewählter Verkaufsauftrag'),
('DE', 'no_selection', 'Kein Auftrag ausgewählt'),
('DE', 'add_production_order', 'Produktionsauftrag hinzufügen'),
('DE', 'production_order', 'Produktionsauftrag:'),
('DE', 'quantity', 'Menge:'),
('DE', 'btn_add_association', 'Zuordnung hinzufügen'),
('DE', 'existing_associations', 'Bestehende Zuordnungen'),
('DE', 'btn_delete_association', 'Zuordnung löschen'),
('DE', 'select_sale_order_first', 'Wählen Sie zuerst einen Verkaufsauftrag'),
('DE', 'select_production_order', 'Wählen Sie einen Produktionsauftrag'),
('DE', 'invalid_quantity', 'Ungültige Menge'),
('DE', 'qty_exceeds_remaining', 'Menge überschreitet verbleibende'),
('DE', 'association_created', 'Zuordnung erfolgreich erstellt'),
('DE', 'select_association', 'Wählen Sie eine Zuordnung zum Löschen'),
('DE', 'confirm_delete_association', 'Zuordnungslöschung bestätigen?'),
('DE', 'association_deleted', 'Zuordnung gelöscht'),

-- SVEDESE (SV)
('SV', 'match_production_orders_title', 'Koppla produktionsorder'),
('SV', 'btn_match_production_orders', 'Koppla produktionsorder'),
('SV', 'sale_orders', 'Försäljningsorder'),
('SV', 'association', 'Orderkoppling'),
('SV', 'filters', 'Filter'),
('SV', 'so_number', 'Ordernr:'),
('SV', 'customer', 'Kund:'),
('SV', 'product', 'Produkt:'),
('SV', 'date_from', 'Datum Från:'),
('SV', 'date_to', 'Datum Till:'),
('SV', 'btn_apply_filter', 'Tillämpa filter'),
('SV', 'btn_reset_filter', 'Återställ filter'),
('SV', 'col_qty_assigned', 'Tilldelad kvantitet'),
('SV', 'col_qty_remaining', 'Återstående kvantitet'),
('SV', 'col_production_order', 'Produktionsorder'),
('SV', 'col_date_in', 'Datum In'),
('SV', 'selected_sale_order', 'Vald försäljningsorder'),
('SV', 'no_selection', 'Ingen order vald'),
('SV', 'add_production_order', 'Lägg till produktionsorder'),
('SV', 'production_order', 'Produktionsorder:'),
('SV', 'quantity', 'Kvantitet:'),
('SV', 'btn_add_association', 'Lägg till koppling'),
('SV', 'existing_associations', 'Befintliga kopplingar'),
('SV', 'btn_delete_association', 'Ta bort koppling'),
('SV', 'select_sale_order_first', 'Välj en försäljningsorder först'),
('SV', 'select_production_order', 'Välj en produktionsorder'),
('SV', 'invalid_quantity', 'Ogiltig kvantitet'),
('SV', 'qty_exceeds_remaining', 'Kvantiteten överstiger återstående'),
('SV', 'association_created', 'Koppling skapad framgångsrikt'),
('SV', 'select_association', 'Välj en koppling att ta bort'),
('SV', 'confirm_delete_association', 'Bekräfta borttagning av koppling?'),
('SV', 'association_deleted', 'Koppling borttagen');

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
PRINT 'Inserite ' + CAST(@InsertedCount AS NVARCHAR(10)) + ' nuove traduzioni per Match Production Orders';

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
