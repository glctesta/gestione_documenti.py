-- ============================================================
-- Traduzioni report Analisi FAIL (All-FAIL + Tassi Scrap/Rework)
-- Lingue: it, en, ro, de, sv
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- ============================================================

-- fa_subtitle
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_subtitle')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_subtitle', N'Tutti i FAIL di tutte le fasi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_subtitle')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_subtitle', N'All FAILs from all phases');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_subtitle')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_subtitle', N'Toate FAIL-urile din toate fazele');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_subtitle')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_subtitle', N'Alle FAILs aus allen Phasen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_subtitle')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_subtitle', N'Alla FAIL från alla faser');

-- fa_tab_allfail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_tab_allfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_tab_allfail', N'Tutti i FAIL');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_tab_allfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_tab_allfail', N'All FAILs');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_tab_allfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_tab_allfail', N'Toate FAIL-urile');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_tab_allfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_tab_allfail', N'Alle FAILs');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_tab_allfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_tab_allfail', N'Alla FAIL');

-- fa_tab_refail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_tab_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_tab_refail', N'Riparate → ri-fallite');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_tab_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_tab_refail', N'Repaired → re-failed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_tab_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_tab_refail', N'Reparate → re-eșuate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_tab_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_tab_refail', N'Repariert → erneut fehlerhaft');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_tab_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_tab_refail', N'Reparerade → omfall');

-- fa_filter_status
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_filter_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_filter_status', N'Stato:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_filter_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_filter_status', N'Status:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_filter_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_filter_status', N'Stare:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_filter_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_filter_status', N'Status:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_filter_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_filter_status', N'Status:');

-- fa_filter_refail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_filter_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_filter_refail', N'Solo riparate → ri-fallite');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_filter_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_filter_refail', N'Only repaired → re-failed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_filter_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_filter_refail', N'Doar reparate → re-eșuate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_filter_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_filter_refail', N'Nur repariert → erneut fehlerhaft');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_filter_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_filter_refail', N'Endast reparerade → omfall');

-- fa_all_count
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_all_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_all_count', N'{0} di {1} righe');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_all_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_all_count', N'{0} of {1} rows');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_all_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_all_count', N'{0} din {1} rânduri');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_all_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_all_count', N'{0} von {1} Zeilen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_all_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_all_count', N'{0} av {1} rader');

-- fa_col_failcount
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_col_failcount')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_col_failcount', N'N. Fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_col_failcount')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_col_failcount', N'Fail count');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_col_failcount')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_col_failcount', N'Nr. Fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_col_failcount')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_col_failcount', N'Fehleranzahl');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_col_failcount')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_col_failcount', N'Antal fel');

-- fa_col_status
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_col_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_col_status', N'Stato');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_col_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_col_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_col_status', N'Stare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_col_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_col_status')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_col_status', N'Status');

-- fa_col_refail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_col_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_col_refail', N'Ri-fallita');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_col_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_col_refail', N'Re-failed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_col_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_col_refail', N'Re-eșuat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_col_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_col_refail', N'Erneut fehlerhaft');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_col_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_col_refail', N'Omfall');

-- fa_col_firstfail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_col_firstfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_col_firstfail', N'Primo Fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_col_firstfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_col_firstfail', N'First Fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_col_firstfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_col_firstfail', N'Primul Fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_col_firstfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_col_firstfail', N'Erster Fehler');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_col_firstfail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_col_firstfail', N'Första fel');

-- fa_col_lastscan
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_col_lastscan')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_col_lastscan', N'Ultima Scan');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_col_lastscan')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_col_lastscan', N'Last Scan');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_col_lastscan')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_col_lastscan', N'Ultima Scanare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_col_lastscan')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_col_lastscan', N'Letzter Scan');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_col_lastscan')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_col_lastscan', N'Senaste skanning');

-- fa_refail_hint
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_refail_hint')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_refail_hint', N'Schede RIPARATE (PASS in riparazione) e poi RI-FALLITE alla stessa fase — indicatore di inefficienza della riparazione.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_refail_hint')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_refail_hint', N'Boards REPAIRED (PASS at repair) and then RE-FAILED at the same phase — indicator of repair inefficiency.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_refail_hint')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_refail_hint', N'Plăci REPARATE (PASS la reparație) și apoi RE-EȘUATE la aceeași fază — indicator al ineficienței reparației.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_refail_hint')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_refail_hint', N'Platinen REPARIERT (PASS bei Reparatur) und dann an derselben Phase ERNEUT FEHLGESCHLAGEN — Indikator für Reparatur-Ineffizienz.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_refail_hint')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_refail_hint', N'Kort REPARERADE (PASS vid reparation) och sedan OMFALL i samma fas — indikator på reparationsineffektivitet.');

-- fa_status_ready2
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_status_ready2', N'{0} schede/fase FAIL — {1} eventi — Wait {2} · Repaired {3} · Scrap {4} · Ri-fallite {5}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_status_ready2', N'{0} board/phase FAILs — {1} events — Wait {2} · Repaired {3} · Scrap {4} · Re-failed {5}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_status_ready2', N'{0} plăci/fază FAIL — {1} evenimente — Wait {2} · Repaired {3} · Scrap {4} · Re-eșuate {5}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_status_ready2', N'{0} Platine/Phase FAIL — {1} Ereignisse — Wait {2} · Repaired {3} · Scrap {4} · Erneut fehlerhaft {5}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_status_ready2', N'{0} kort/fas FAIL — {1} händelser — Wait {2} · Repaired {3} · Scrap {4} · Omfall {5}');

-- fa_stats_title2
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_stats_title2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_stats_title2', N'FAIL — RIEPILOGO PER FASE (tutti i FAIL, riparati e non)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_stats_title2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_stats_title2', N'FAIL — SUMMARY BY PHASE (all FAILs, repaired and not)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_stats_title2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_stats_title2', N'FAIL — SUMAR PE FAZĂ (toate FAIL-urile, reparate sau nu)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_stats_title2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_stats_title2', N'FAIL — ZUSAMMENFASSUNG NACH PHASE (alle FAILs, repariert oder nicht)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_stats_title2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_stats_title2', N'FAIL — SAMMANFATTNING PER FAS (alla FAIL, reparerade eller ej)');

-- fa_h_phase
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_phase')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_phase', N'Fase');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_phase')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_phase', N'Phase');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_phase')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_phase', N'Fază');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_phase')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_phase', N'Phase');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_phase')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_phase', N'Fas');

-- fa_h_boards
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_boards')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_boards', N'Schede');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_boards')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_boards', N'Boards');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_boards')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_boards', N'Plăci');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_boards')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_boards', N'Platinen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_boards')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_boards', N'Kort');

-- fa_h_events
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_events')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_events', N'Eventi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_events')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_events', N'Events');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_events')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_events', N'Evenim.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_events')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_events', N'Ereign.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_events')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_events', N'Händ.');

-- fa_h_repaired
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_repaired')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_repaired', N'Riparate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_repaired')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_repaired', N'Repaired');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_repaired')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_repaired', N'Reparate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_repaired')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_repaired', N'Repariert');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_repaired')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_repaired', N'Reparer.');

-- fa_h_wait
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_wait', N'Aperte');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_wait', N'Wait');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_wait', N'Wait');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_wait', N'Offen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_wait', N'Väntar');

-- fa_h_scrap
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_scrap', N'Scrap');

-- fa_h_refail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_refail', N'Ri-fallite');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_refail', N'Re-failed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_refail', N'Re-eșuate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_refail', N'Erneut F.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_refail', N'Omfall');

-- fa_h_multi
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_multi')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_multi', N'Multi-fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_multi')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_multi', N'Multi-fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_multi')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_multi', N'Multi-fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_multi')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_multi', N'Multi-fail');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_multi')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_multi', N'Multi-fail');

-- fa_h_total
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_total', N'TOTALE');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_total', N'TOTAL');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_total', N'TOTAL');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_total', N'GESAMT');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_total', N'TOTALT');

-- fa_stats_rates
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_stats_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_stats_rates', N'Indicatori (interni al set FAIL):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_stats_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_stats_rates', N'Indicators (within the FAIL set):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_stats_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_stats_rates', N'Indicatori (în cadrul setului FAIL):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_stats_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_stats_rates', N'Indikatoren (innerhalb der FAIL-Menge):');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_stats_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_stats_rates', N'Indikatorer (inom FAIL-uppsättningen):');

-- fa_pct_wait
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_wait', N'% ancora aperte (Wait) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_wait', N'% still open (Wait) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_wait', N'% încă deschise (Wait) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_wait', N'% noch offen (Wait) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_wait')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_wait', N'% fortfarande öppna (Wait) :');

-- fa_pct_rep
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_rep')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_rep', N'% riparate (Repaired) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_rep')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_rep', N'% repaired (Repaired) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_rep')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_rep', N'% reparate (Repaired) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_rep')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_rep', N'% repariert (Repaired) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_rep')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_rep', N'% reparerade (Repaired) :');

-- fa_pct_scrap
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_scrap', N'% scrap :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_scrap', N'% scrap :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_scrap', N'% scrap :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_scrap', N'% Ausschuss :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_scrap', N'% skrot :');

-- fa_pct_refail
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_refail', N'% ri-fallite su riparate :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_refail', N'% re-failed of repaired :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_refail', N'% re-eșuate din reparate :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_refail', N'% erneut fehlerhaft von repariert :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_refail')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_refail', N'% omfall av reparerade :');

-- fa_pct_refail_note
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_refail_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_refail_note', N'(efficienza riparazione)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_refail_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_refail_note', N'(repair efficiency)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_refail_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_refail_note', N'(eficiența reparației)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_refail_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_refail_note', N'(Reparatur-Effizienz)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_refail_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_refail_note', N'(reparationseffektivitet)');

-- fa_tab_rates
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_tab_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_tab_rates', N'Tassi Scrap/Rework');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_tab_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_tab_rates', N'Scrap/Rework Rates');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_tab_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_tab_rates', N'Rate Scrap/Rework');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_tab_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_tab_rates', N'Ausschuss-/Nacharbeitsrate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_tab_rates')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_tab_rates', N'Skrot-/omarbetningsfrekvens');

-- fa_target_scrap
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_target_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_target_scrap', N'Target Scrap %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_target_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_target_scrap', N'Scrap target %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_target_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_target_scrap', N'Țintă Scrap %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_target_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_target_scrap', N'Ausschuss-Ziel %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_target_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_target_scrap', N'Skrotmål %:');

-- fa_target_rework
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_target_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_target_rework', N'Target Rework %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_target_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_target_rework', N'Rework target %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_target_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_target_rework', N'Țintă Rework %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_target_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_target_rework', N'Nacharbeitsziel %:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_target_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_target_rework', N'Omarbetningsmål %:');

-- fa_calc_btn
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_calc_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_calc_btn', N'Calcola tassi');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_calc_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_calc_btn', N'Calculate rates');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_calc_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_calc_btn', N'Calculează ratele');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_calc_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_calc_btn', N'Raten berechnen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_calc_btn')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_calc_btn', N'Beräkna frekvenser');

-- fa_rates_loading
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rates_loading')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rates_loading', N'Calcolo tassi in corso...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rates_loading')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rates_loading', N'Calculating rates...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rates_loading')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rates_loading', N'Se calculează ratele...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rates_loading')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rates_loading', N'Raten werden berechnet...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rates_loading')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rates_loading', N'Beräknar frekvenser...');

-- fa_rates_done
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rates_done')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rates_done', N'Calcolo completato');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rates_done')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rates_done', N'Calculation completed');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rates_done')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rates_done', N'Calcul finalizat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rates_done')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rates_done', N'Berechnung abgeschlossen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rates_done')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rates_done', N'Beräkning klar');

-- fa_rates_note
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rates_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rates_note', N'Prodotto = schede distinte scansionate nel periodo. Scrap/Rework = schede distinte con esito riparazione SCRAP/REPAIRED. Verde = entro target, rosso = oltre target.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rates_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rates_note', N'Produced = distinct boards scanned in the period. Scrap/Rework = distinct boards with SCRAP/REPAIRED repair result. Green = within target, red = over target.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rates_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rates_note', N'Produs = plăci distincte scanate în perioadă. Scrap/Rework = plăci distincte cu rezultat reparație SCRAP/REPAIRED. Verde = în țintă, roșu = peste țintă.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rates_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rates_note', N'Produziert = eindeutige im Zeitraum gescannte Platinen. Scrap/Rework = eindeutige Platinen mit Reparaturergebnis SCRAP/REPAIRED. Grün = im Ziel, rot = über Ziel.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rates_note')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rates_note', N'Producerat = unika kort skannade under perioden. Scrap/Rework = unika kort med reparationsresultat SCRAP/REPAIRED. Grönt = inom mål, rött = över mål.');

-- fa_rc_month
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_month')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_month', N'Mese');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_month')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_month', N'Month');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_month')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_month', N'Luna');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_month')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_month', N'Monat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_month')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_month', N'Månad');

-- fa_rc_produced
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_produced')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_produced', N'Prodotto');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_produced')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_produced', N'Produced');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_produced')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_produced', N'Produs');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_produced')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_produced', N'Produziert');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_produced')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_produced', N'Producerat');

-- fa_rc_scrap
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_scrap', N'Scrap');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_scrap', N'Ausschuss');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_scrap')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_scrap', N'Skrot');

-- fa_rc_rework
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_rework', N'Rework');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_rework', N'Rework');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_rework', N'Rework');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_rework', N'Nacharbeit');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_rework')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_rework', N'Omarbetning');

-- fa_rc_scrappct
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_scrappct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_scrappct', N'Scrap %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_scrappct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_scrappct', N'Scrap %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_scrappct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_scrappct', N'Scrap %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_scrappct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_scrappct', N'Ausschuss %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_scrappct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_scrappct', N'Skrot %');

-- fa_rc_reworkpct
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_reworkpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_reworkpct', N'Rework %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_reworkpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_reworkpct', N'Rework %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_reworkpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_reworkpct', N'Rework %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_reworkpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_reworkpct', N'Nacharbeit %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_reworkpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_reworkpct', N'Omarbetning %');

-- fa_rc_failpct
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rc_failpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rc_failpct', N'Fail %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rc_failpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rc_failpct', N'Fail %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rc_failpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rc_failpct', N'Fail %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rc_failpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rc_failpct', N'Fehler %');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rc_failpct')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rc_failpct', N'Fel %');

-- fa_rates_total
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_rates_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_rates_total', N'TOTALE periodo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_rates_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_rates_total', N'Period TOTAL');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_rates_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_rates_total', N'TOTAL perioadă');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_rates_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_rates_total', N'GESAMT Zeitraum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_rates_total')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_rates_total', N'TOTALT period');

-- ===== Split Repaired/Recovered (delta) =====

-- fa_h_recovered
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_h_recovered')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_h_recovered', N'Recuperate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_h_recovered')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_h_recovered', N'Recovered');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_h_recovered')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_h_recovered', N'Recuperate');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_h_recovered')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_h_recovered', N'Erholt');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_h_recovered')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_h_recovered', N'Återst.');

-- fa_pct_recov
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_pct_recov')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_pct_recov', N'% recuperate (Recovered) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_pct_recov')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_pct_recov', N'% recovered (Recovered) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_pct_recov')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_pct_recov', N'% recuperate (Recovered) :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_pct_recov')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_pct_recov', N'% wiederhergestellt :');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_pct_recov')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_pct_recov', N'% återställda :');

-- fa_status_ready2
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'it' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'fa_status_ready2', N'{0} schede/fase FAIL — {1} eventi — Wait {2} · Repaired {3} · Recovered {4} · Scrap {5} · Ri-fallite {6}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'en' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'fa_status_ready2', N'{0} board/phase FAILs — {1} events — Wait {2} · Repaired {3} · Recovered {4} · Scrap {5} · Re-failed {6}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'ro' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'fa_status_ready2', N'{0} plăci/fază FAIL — {1} evenimente — Wait {2} · Repaired {3} · Recovered {4} · Scrap {5} · Re-eșuate {6}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'de' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'fa_status_ready2', N'{0} Platine/Phase FAIL — {1} Ereignisse — Wait {2} · Repaired {3} · Recovered {4} · Scrap {5} · Erneut fehlerhaft {6}');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode]=N'sv' AND [TranslationKey]=N'fa_status_ready2')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'fa_status_ready2', N'{0} kort/fas FAIL — {1} händelser — Wait {2} · Repaired {3} · Recovered {4} · Scrap {5} · Omfall {6}');
