-- Script SQL per le traduzioni della finestra Report del modulo Ricezione
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-09-16
USE [Traceability_RS];
GO

-- ============================================================================
-- helper macro: non disponibile in T-SQL puro; ogni chiave/lingua e' esplicita
-- ============================================================================

-- incoming_menu_report
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'incoming_menu_report')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'incoming_menu_report', N'Report');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'incoming_menu_report')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'incoming_menu_report', N'Report');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'incoming_menu_report')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'incoming_menu_report', N'Raport');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'incoming_menu_report')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'incoming_menu_report', N'Bericht');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'incoming_menu_report')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'incoming_menu_report', N'Rapport');

-- inc_rep_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_title', N'Report Ricezione — situazione MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_title', N'Receiving report — MPN situation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_title', N'Raport Recepție — situație MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_title', N'Wareneingang-Bericht — MPN-Situation');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_title', N'Rapport mottagning — MPN-läge');

-- inc_rep_filters
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filters')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filters', N'Filtri');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filters')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filters', N'Filters');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filters')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filters', N'Filtre');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filters')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filters', N'Filter');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filters')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filters', N'Filter');

-- inc_rep_filter_from
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_from')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_from', N'Da:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_from')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_from', N'From:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_from')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_from', N'De la:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_from')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_from', N'Von:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_from')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_from', N'Från:');

-- inc_rep_filter_to
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_to')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_to', N'A:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_to')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_to', N'To:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_to')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_to', N'Până la:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_to')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_to', N'Bis:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_to')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_to', N'Till:');

-- inc_rep_filter_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_status', N'Stato:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_status', N'Status:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_status', N'Stare:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_status', N'Status:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_status', N'Status:');

-- inc_rep_filter_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_type', N'Tipo:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_type', N'Type:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_type', N'Tip:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_type', N'Typ:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_type', N'Typ:');

-- inc_rep_filter_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_supplier', N'Fornitore:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_supplier', N'Supplier:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_supplier', N'Furnizor:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_supplier', N'Lieferant:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_supplier', N'Leverantör:');

-- inc_rep_filter_product
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_product', N'Codice prodotto (MPN):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_product', N'Product code (MPN):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_product', N'Cod produs (MPN):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_product', N'Produktcode (MPN):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_product', N'Produktkod (MPN):');

-- inc_rep_filter_wrong
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_wrong')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_wrong', N'MPN errato:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_wrong')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_wrong', N'Wrong MPN:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_wrong')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_wrong', N'MPN greșit:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_wrong')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_wrong', N'Falsche MPN:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_wrong')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_wrong', N'Fel MPN:');

-- inc_rep_filter_answer
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_filter_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_filter_answer', N'MPN soluzione:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_filter_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_filter_answer', N'Solution MPN:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_filter_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_filter_answer', N'MPN soluție:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_filter_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_filter_answer', N'Lösungs-MPN:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_filter_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_filter_answer', N'Lösnings-MPN:');

-- inc_rep_status_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_status_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_status_all', N'(tutte)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_status_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_status_all', N'(all)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_status_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_status_all', N'(toate)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_status_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_status_all', N'(alle)');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_status_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_status_all', N'(alla)');

-- inc_rep_status_answered
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_status_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_status_answered', N'Evase');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_status_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_status_answered', N'Answered');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_status_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_status_answered', N'Rezolvate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_status_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_status_answered', N'Erledigt');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_status_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_status_answered', N'Besvarade');

-- inc_rep_status_pending
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_status_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_status_pending', N'Non evase');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_status_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_status_pending', N'Pending');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_status_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_status_pending', N'Nerezolvate');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_status_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_status_pending', N'Offen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_status_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_status_pending', N'Öppna');

-- inc_rep_confirmed_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_confirmed_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_confirmed_ok', N'Confermata OK');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_confirmed_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_confirmed_ok', N'Confirmed OK');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_confirmed_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_confirmed_ok', N'Confirmat OK');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_confirmed_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_confirmed_ok', N'Bestätigt OK');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_confirmed_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_confirmed_ok', N'Bekräftad OK');

-- inc_rep_confirmed_ko
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_confirmed_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_confirmed_ko', N'Confermata KO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_confirmed_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_confirmed_ko', N'Confirmed KO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_confirmed_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_confirmed_ko', N'Confirmat KO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_confirmed_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_confirmed_ko', N'Bestätigt KO');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_confirmed_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_confirmed_ko', N'Bekräftad KO');

-- inc_rep_search
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_search')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_search', N'🔍 Cerca');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_search')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_search', N'🔍 Search');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_search')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_search', N'🔍 Caută');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_search')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_search', N'🔍 Suchen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_search')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_search', N'🔍 Sök');

-- inc_rep_export
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_export')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_export', N'⬇ Esporta Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_export')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_export', N'⬇ Export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_export')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_export', N'⬇ Export Excel');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_export')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_export', N'⬇ Excel exportieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_export')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_export', N'⬇ Exportera Excel');

-- inc_rep_export_done
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_export_done')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_export_done', N'Report esportato con successo:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_export_done')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_export_done', N'Report exported successfully:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_export_done')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_export_done', N'Raport exportat cu succes:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_export_done')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_export_done', N'Bericht erfolgreich exportiert:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_export_done')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_export_done', N'Rapport exporterad:
{0}');

-- inc_rep_export_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_export_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_export_error', N'Errore durante l''esportazione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_export_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_export_error', N'Error during export');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_export_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_export_error', N'Eroare la export');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_export_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_export_error', N'Fehler beim Exportieren');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_export_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_export_error', N'Fel vid export');

-- inc_rep_col_ddt_date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_ddt_date', N'Data DDT');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_ddt_date', N'DDT date');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_ddt_date', N'Data DDT');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_ddt_date', N'DDT-Datum');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_ddt_date', N'DDT-datum');

-- inc_rep_col_wrong_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_wrong_mpn', N'MPN errato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_wrong_mpn', N'Wrong MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_wrong_mpn', N'MPN greșit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_wrong_mpn', N'Falsche MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_wrong_mpn', N'Fel MPN');

-- inc_rep_col_qty_receive
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_qty_receive', N'Q.tà da ricevere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_qty_receive', N'Qty to receive');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_qty_receive', N'Cant. de primit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_qty_receive', N'Zu erhaltende Menge');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_qty_receive', N'Antal att motta');

-- inc_rep_col_qty_expected
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_qty_expected', N'Q.tà attesa P.O.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_qty_expected', N'Expected P.O. qty');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_qty_expected', N'Cant. așteptată C.C.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_qty_expected', N'Erwartete B.M.-Menge');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_qty_expected', N'Förväntat P.O.-antal');

-- inc_rep_col_requested_on
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_requested_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_requested_on', N'Data richiesta');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_requested_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_requested_on', N'Requested on');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_requested_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_requested_on', N'Data cerere');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_requested_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_requested_on', N'Angefragt am');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_requested_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_requested_on', N'Begärd den');

-- inc_rep_col_host
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_host')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_host', N'PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_host')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_host', N'PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_host')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_host', N'PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_host')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_host', N'PC');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_host')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_host', N'PC');

-- inc_rep_col_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_status', N'Stato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_status', N'Stare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_status', N'Status');

-- inc_rep_col_answer_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_answer_mpn', N'MPN soluzione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_answer_mpn', N'Solution MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_answer_mpn', N'MPN soluție');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_answer_mpn', N'Lösungs-MPN');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_answer_mpn', N'Lösnings-MPN');

-- inc_rep_col_answered_by
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_answered_by', N'Evasa da');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_answered_by', N'Answered by');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_answered_by', N'Rezolvat de');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_answered_by', N'Erledigt von');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_answered_by', N'Besvarad av');

-- inc_rep_col_answered_on
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_answered_on', N'Data evasione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_answered_on', N'Answered on');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_answered_on', N'Data rezolvare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_answered_on', N'Erledigt am');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_answered_on', N'Besvarad den');

-- inc_rep_col_elapsed
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_rep_col_elapsed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_rep_col_elapsed', N'Tempo trascorso');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_rep_col_elapsed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_rep_col_elapsed', N'Elapsed time');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_rep_col_elapsed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_rep_col_elapsed', N'Timp scurs');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_rep_col_elapsed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_rep_col_elapsed', N'Verstrichene Zeit');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_rep_col_elapsed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_rep_col_elapsed', N'Förfluten tid');
