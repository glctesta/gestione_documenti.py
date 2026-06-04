-- Traduzioni per Material Consumption Report GUI (alloy/flux -- PTHM)
USE [Traceability_RS];
GO

;WITH T AS (
    SELECT * FROM (VALUES
        (N'it', N'mcr_window_title',     N'Report Consumi Alloy / Flux -- Fase PTHM'),
        (N'en', N'mcr_window_title',     N'Alloy / Flux Consumption Report -- PTHM Phase'),
        (N'de', N'mcr_window_title',     N'Legierung / Flux Verbrauchsbericht -- PTHM Phase'),
        (N'ro', N'mcr_window_title',     N'Raport Consum Aliaj / Flux -- Faza PTHM'),
        (N'sv', N'mcr_window_title',     N'Legering / Flux forbrukningsrapport -- PTHM-fas'),

        (N'it', N'mcr_email_info',       N'Email automatica giornaliera: chiave "Sys_missing_data_alloy" in Settings  |  Schedule: Lun-Sab alle 08:05'),
        (N'en', N'mcr_email_info',       N'Automated daily email: key "Sys_missing_data_alloy" in Settings  |  Schedule: Mon-Sat at 08:05'),
        (N'de', N'mcr_email_info',       N'Automatische tagliche E-Mail: Schlussel "Sys_missing_data_alloy" in Einstellungen  |  Zeitplan: Mo-Sa um 08:05'),
        (N'ro', N'mcr_email_info',       N'Email automata zilnica: cheia "Sys_missing_data_alloy" in Settings  |  Programare: Lun-Sam la 08:05'),
        (N'sv', N'mcr_email_info',       N'Automatisk daglig e-post: nyckel "Sys_missing_data_alloy" i Installningar  |  Schema: Man-Lor kl. 08:05'),

        (N'it', N'mcr_filter_title',     N'Filtri di ricerca'),
        (N'en', N'mcr_filter_title',     N'Search filters'),
        (N'de', N'mcr_filter_title',     N'Suchfilter'),
        (N'ro', N'mcr_filter_title',     N'Filtre de cautare'),
        (N'sv', N'mcr_filter_title',     N'Sokfilter'),

        (N'it', N'mcr_date_from',        N'Da (gg/mm/aaaa):'),
        (N'en', N'mcr_date_from',        N'From (dd/mm/yyyy):'),
        (N'de', N'mcr_date_from',        N'Von (TT/MM/JJJJ):'),
        (N'ro', N'mcr_date_from',        N'De la (zz/ll/aaaa):'),
        (N'sv', N'mcr_date_from',        N'Fran (dd/mm/yyyy):'),

        (N'it', N'mcr_date_to',          N'A (gg/mm/aaaa):'),
        (N'en', N'mcr_date_to',          N'To (dd/mm/yyyy):'),
        (N'de', N'mcr_date_to',          N'Bis (TT/MM/JJJJ):'),
        (N'ro', N'mcr_date_to',          N'Pana la (zz/ll/aaaa):'),
        (N'sv', N'mcr_date_to',          N'Till (dd/mm/yyyy):'),

        (N'it', N'mcr_product_code',     N'Codice prodotto (opzionale):'),
        (N'en', N'mcr_product_code',     N'Product code (optional):'),
        (N'de', N'mcr_product_code',     N'Produktcode (optional):'),
        (N'ro', N'mcr_product_code',     N'Cod produs (optional):'),
        (N'sv', N'mcr_product_code',     N'Produktkod (valfritt):'),

        (N'it', N'mcr_btn_search',       N'Cerca'),
        (N'en', N'mcr_btn_search',       N'Search'),
        (N'de', N'mcr_btn_search',       N'Suchen'),
        (N'ro', N'mcr_btn_search',       N'Cauta'),
        (N'sv', N'mcr_btn_search',       N'Sok'),

        (N'it', N'mcr_btn_export_excel', N'Esporta Excel'),
        (N'en', N'mcr_btn_export_excel', N'Export Excel'),
        (N'de', N'mcr_btn_export_excel', N'Excel exportieren'),
        (N'ro', N'mcr_btn_export_excel', N'Exporta Excel'),
        (N'sv', N'mcr_btn_export_excel', N'Exportera Excel'),

        (N'it', N'mcr_invalid_dates',    N'Inserire date valide nel formato gg/mm/aaaa.'),
        (N'en', N'mcr_invalid_dates',    N'Please enter valid dates in dd/mm/yyyy format.'),
        (N'de', N'mcr_invalid_dates',    N'Bitte gultige Daten im Format TT/MM/JJJJ eingeben.'),
        (N'ro', N'mcr_invalid_dates',    N'Introduceti date valide in formatul zz/ll/aaaa.'),
        (N'sv', N'mcr_invalid_dates',    N'Ange giltiga datum i formatet dd/mm/yyyy.'),

        (N'it', N'mcr_date_order',       N'La data "Da" deve essere uguale o precedente alla data "A".'),
        (N'en', N'mcr_date_order',       N'"From" date must be on or before the "To" date.'),
        (N'de', N'mcr_date_order',       N'Das "Von"-Datum muss gleich oder vor dem "Bis"-Datum liegen.'),
        (N'ro', N'mcr_date_order',       N'Data "De la" trebuie sa fie egala sau anterioara datei "Pana la".'),
        (N'sv', N'mcr_date_order',       N'"Fran"-datum maste vara pa eller fore "Till"-datum.'),

        (N'it', N'mcr_no_results',       N'Nessun dato trovato per il periodo selezionato.'),
        (N'en', N'mcr_no_results',       N'No data found for the selected period.'),
        (N'de', N'mcr_no_results',       N'Keine Daten fur den ausgewahlten Zeitraum gefunden.'),
        (N'ro', N'mcr_no_results',       N'Nu au fost gasite date pentru perioada selectata.'),
        (N'sv', N'mcr_no_results',       N'Inga data hittades for den valda perioden.'),

        (N'it', N'mcr_day_total',        N'Totale giorno (gr):'),
        (N'en', N'mcr_day_total',        N'Day total (gr):'),
        (N'de', N'mcr_day_total',        N'Tagesgesamt (gr):'),
        (N'ro', N'mcr_day_total',        N'Total zi (gr):'),
        (N'sv', N'mcr_day_total',        N'Dagtotal (gr):'),

        (N'it', N'mcr_summary_with',     N'Codici CON peso: {0}'),
        (N'en', N'mcr_summary_with',     N'Codes WITH weight: {0}'),
        (N'de', N'mcr_summary_with',     N'Codes MIT Gewicht: {0}'),
        (N'ro', N'mcr_summary_with',     N'Coduri CU greutate: {0}'),
        (N'sv', N'mcr_summary_with',     N'Koder MED vikt: {0}'),

        (N'it', N'mcr_summary_without',  N'Codici SENZA peso: {0}'),
        (N'en', N'mcr_summary_without',  N'Codes WITHOUT weight: {0}'),
        (N'de', N'mcr_summary_without',  N'Codes OHNE Gewicht: {0}'),
        (N'ro', N'mcr_summary_without',  N'Coduri FARA greutate: {0}'),
        (N'sv', N'mcr_summary_without',  N'Koder UTAN vikt: {0}'),

        (N'it', N'mcr_summary_diff',     N'Differenza (con - senza): {0}'),
        (N'en', N'mcr_summary_diff',     N'Difference (with - without): {0}'),
        (N'de', N'mcr_summary_diff',     N'Differenz (mit - ohne): {0}'),
        (N'ro', N'mcr_summary_diff',     N'Diferenta (cu - fara): {0}'),
        (N'sv', N'mcr_summary_diff',     N'Skillnad (med - utan): {0}'),

        (N'it', N'mcr_no_data_export',   N'Nessun dato da esportare. Eseguire prima una ricerca.'),
        (N'en', N'mcr_no_data_export',   N'No data to export. Run a search first.'),
        (N'de', N'mcr_no_data_export',   N'Keine Daten zum Exportieren. Bitte zuerst eine Suche durchfuhren.'),
        (N'ro', N'mcr_no_data_export',   N'Nu exista date de exportat. Efectuati mai intai o cautare.'),
        (N'sv', N'mcr_no_data_export',   N'Inga data att exportera. Kor en sokning forst.'),

        (N'it', N'mcr_export_ok',        N'File salvato:{0}'),
        (N'en', N'mcr_export_ok',        N'File saved:{0}'),
        (N'de', N'mcr_export_ok',        N'Datei gespeichert:{0}'),
        (N'ro', N'mcr_export_ok',        N'Fisier salvat:{0}'),
        (N'sv', N'mcr_export_ok',        N'Fil sparad:{0}')
    ) AS X([LanguageCode], [TranslationKey], [TranslationValue])
)
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT T.[LanguageCode], T.[TranslationKey], T.[TranslationValue]
FROM T
WHERE NOT EXISTS (
    SELECT 1
    FROM [dbo].[AppTranslations] A
    WHERE A.[LanguageCode] = T.[LanguageCode]
      AND A.[TranslationKey] = T.[TranslationKey]
);
GO
