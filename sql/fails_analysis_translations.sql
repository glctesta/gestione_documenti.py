-- ============================================================
-- Analisi Fails — Traduzioni UI (IT, RO, EN, DE, SV)
-- Script idempotente
-- ============================================================

USE [Traceability_RS];
GO

DECLARE @keys TABLE (lang NVARCHAR(5), k NVARCHAR(100), v NVARCHAR(500));
INSERT INTO @keys VALUES
-- IT
('it','menu_analisi_fails',N'📈 Analisi Fails'),
('it','fa_title',N'Analisi Schede FAIL'),
('it','fa_date_from',N'Da:'),
('it','fa_date_to',N'A:'),
('it','fa_load_btn',N'🔄 Carica / Aggiorna'),
('it','fa_export_btn',N'📊 Esporta Excel'),
('it','fa_tab_raw',N'Dati Grezzi'),
('it','fa_tab_repaired',N'Schede Riparate'),
('it','fa_tab_stats',N'Statistiche'),
('it','fa_status_loading',N'Caricamento in corso...'),
('it','fa_status_ready',N'{0} schede FAIL — {1} riparate ({2:.1f}%)'),
('it','fa_no_data',N'Nessun dato trovato per il periodo selezionato'),
('it','fa_confirm_reload',N'Cache esistente'),
('it','fa_confirm_reload_msg',N'Trovati {0} record in cache per questo periodo.\nRicaricare dal database?'),
-- RO
('ro','menu_analisi_fails',N'📈 Analiză Eșecuri'),
('ro','fa_title',N'Analiză Fișe FAIL'),
('ro','fa_date_from',N'De la:'),
('ro','fa_date_to',N'Până la:'),
('ro','fa_load_btn',N'🔄 Încarcă / Actualizează'),
('ro','fa_export_btn',N'📊 Export Excel'),
('ro','fa_tab_raw',N'Date Brute'),
('ro','fa_tab_repaired',N'Fișe Reparate'),
('ro','fa_tab_stats',N'Statistici'),
('ro','fa_status_loading',N'Se încarcă...'),
('ro','fa_status_ready',N'{0} fișe FAIL — {1} reparate ({2:.1f}%)'),
('ro','fa_no_data',N'Niciun date găsite pentru perioada selectată'),
('ro','fa_confirm_reload',N'Cache existent'),
('ro','fa_confirm_reload_msg',N'Găsite {0} înregistrări în cache.\nReîncarcă din baza de date?'),
-- EN
('en','menu_analisi_fails',N'📈 Fail Analysis'),
('en','fa_title',N'FAIL Board Analysis'),
('en','fa_date_from',N'From:'),
('en','fa_date_to',N'To:'),
('en','fa_load_btn',N'🔄 Load / Refresh'),
('en','fa_export_btn',N'📊 Export Excel'),
('en','fa_tab_raw',N'Raw Data'),
('en','fa_tab_repaired',N'Repaired Boards'),
('en','fa_tab_stats',N'Statistics'),
('en','fa_status_loading',N'Loading...'),
('en','fa_status_ready',N'{0} FAIL boards — {1} repaired ({2:.1f}%)'),
('en','fa_no_data',N'No data found for the selected period'),
('en','fa_confirm_reload',N'Existing cache'),
('en','fa_confirm_reload_msg',N'Found {0} cached records for this period.\nReload from database?'),
-- DE
('de','menu_analisi_fails',N'📈 Fehleranalyse'),
('de','fa_title',N'FAIL-Platinen Analyse'),
('de','fa_date_from',N'Von:'),
('de','fa_date_to',N'Bis:'),
('de','fa_load_btn',N'🔄 Laden / Aktualisieren'),
('de','fa_export_btn',N'📊 Excel Export'),
('de','fa_tab_raw',N'Rohdaten'),
('de','fa_tab_repaired',N'Reparierte Platinen'),
('de','fa_tab_stats',N'Statistiken'),
('de','fa_status_loading',N'Wird geladen...'),
('de','fa_status_ready',N'{0} FAIL-Platinen — {1} repariert ({2:.1f}%)'),
('de','fa_no_data',N'Keine Daten für den gewählten Zeitraum gefunden'),
('de','fa_confirm_reload',N'Cache vorhanden'),
('de','fa_confirm_reload_msg',N'{0} Datensätze im Cache gefunden.\nAus Datenbank neu laden?'),
-- SV
('sv','menu_analisi_fails',N'📈 Felanalys'),
('sv','fa_title',N'FAIL-kort Analys'),
('sv','fa_date_from',N'Från:'),
('sv','fa_date_to',N'Till:'),
('sv','fa_load_btn',N'🔄 Ladda / Uppdatera'),
('sv','fa_export_btn',N'📊 Exportera Excel'),
('sv','fa_tab_raw',N'Rådata'),
('sv','fa_tab_repaired',N'Reparerade kort'),
('sv','fa_tab_stats',N'Statistik'),
('sv','fa_status_loading',N'Laddar...'),
('sv','fa_status_ready',N'{0} FAIL-kort — {1} reparerade ({2:.1f}%)'),
('sv','fa_no_data',N'Inga data hittades för den valda perioden'),
('sv','fa_confirm_reload',N'Cache finns'),
('sv','fa_confirm_reload_msg',N'Hittade {0} cachade poster.\nLadda om från databasen?');

INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
SELECT k.lang, k.k, k.v
FROM @keys k
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] t
    WHERE t.LanguageCode = k.lang AND t.TranslationKey = k.k
);

PRINT 'Traduzioni Analisi Fails inserite: ' + CAST(@@ROWCOUNT AS NVARCHAR(10)) + ' righe.';
GO

-- Colonne Treeview (aggiunte v2)
DECLARE @keys2 TABLE (lang NVARCHAR(5), k NVARCHAR(100), v NVARCHAR(500));
INSERT INTO @keys2 VALUES
('it','fa_col_order',    N'N. Ordine'),
('it','fa_col_product',  N'Prodotto'),
('it','fa_col_qty',      N'Qty'),
('it','fa_col_phase',    N'Fase'),
('it','fa_col_idboard',  N'IDBoard'),
('it','fa_col_labels',   N'Label'),
('it','fa_col_scanres',  N'Risultato'),
('it','fa_col_scantime', N'Data Scan'),
('it','fa_col_repair',   N'Riparazione'),
('it','fa_col_defect',   N'Difetto'),
('it','fa_col_codref',   N'Cod.Rif.'),
('it','fa_col_resolved', N'Data Risoluz.'),
('it','fa_col_days',     N'Giorni'),
('ro','fa_col_order',    N'Nr. Comanda'),
('ro','fa_col_product',  N'Produs'),
('ro','fa_col_qty',      N'Cant.'),
('ro','fa_col_phase',    N'Faza'),
('ro','fa_col_idboard',  N'IDBoard'),
('ro','fa_col_labels',   N'Eticheta'),
('ro','fa_col_scanres',  N'Rezultat'),
('ro','fa_col_scantime', N'Data Scan'),
('ro','fa_col_repair',   N'Reparatie'),
('ro','fa_col_defect',   N'Defect'),
('ro','fa_col_codref',   N'Cod.Ref.'),
('ro','fa_col_resolved', N'Data Rezolvare'),
('ro','fa_col_days',     N'Zile'),
('en','fa_col_order',    N'Order No.'),
('en','fa_col_product',  N'Product'),
('en','fa_col_qty',      N'Qty'),
('en','fa_col_phase',    N'Phase'),
('en','fa_col_idboard',  N'IDBoard'),
('en','fa_col_labels',   N'Label'),
('en','fa_col_scanres',  N'Result'),
('en','fa_col_scantime', N'Scan Date'),
('en','fa_col_repair',   N'Repair'),
('en','fa_col_defect',   N'Defect'),
('en','fa_col_codref',   N'Ref.Code'),
('en','fa_col_resolved', N'Resolved On'),
('en','fa_col_days',     N'Days');

INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
SELECT k.lang, k.k, k.v FROM @keys2 k
WHERE NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] t
    WHERE t.LanguageCode = k.lang AND t.TranslationKey = k.k
);
GO
