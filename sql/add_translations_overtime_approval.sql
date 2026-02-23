-- ============================================================
-- Traduzioni per modulo Overtime Approval
-- Lingue: it, en, ro, de, sv
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- ============================================================

-- ── overtime_approval_title ─────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'overtime_approval_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'overtime_approval_title', N'Approvazione Straordinari');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'overtime_approval_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'overtime_approval_title', N'Overtime Approval');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'overtime_approval_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'overtime_approval_title', N'Aprobare Ore Suplimentare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'overtime_approval_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'overtime_approval_title', N'Überstunden-Genehmigung');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'overtime_approval_title')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'overtime_approval_title', N'Godkännande av övertid');

-- ── request_list ────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'request_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'request_list', N'Lista Richieste');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'request_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'request_list', N'Request List');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'request_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'request_list', N'Listă Cereri');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'request_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'request_list', N'Anforderungsliste');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'request_list')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'request_list', N'Begäranslista');

-- ── request_number ──────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'request_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'request_number', N'N° Richiesta');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'request_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'request_number', N'Request No.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'request_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'request_number', N'Nr. Cerere');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'request_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'request_number', N'Anforderungsnr.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'request_number')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'request_number', N'Begäransnr');

-- ── supervisor ──────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'supervisor')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'supervisor', N'Supervisore');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'supervisor')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'supervisor', N'Supervisor');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'supervisor')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'supervisor', N'Supervizor');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'supervisor')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'supervisor', N'Vorgesetzter');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'supervisor')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'supervisor', N'Handledare');

-- ── employees_count ─────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'employees_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'employees_count', N'N° Dipendenti');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'employees_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'employees_count', N'Employees Count');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'employees_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'employees_count', N'Nr. Angajați');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'employees_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'employees_count', N'Mitarbeiteranzahl');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'employees_count')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'employees_count', N'Antal anställda');

-- ── total_hours ─────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'total_hours')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'total_hours', N'Ore Totali');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'total_hours')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'total_hours', N'Total Hours');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'total_hours')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'total_hours', N'Total Ore');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'total_hours')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'total_hours', N'Gesamtstunden');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'total_hours')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'total_hours', N'Totala timmar');

-- ── view_details ────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'view_details')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'view_details', N'Vedi Dettagli');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'view_details')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'view_details', N'View Details');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'view_details')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'view_details', N'Vizualizare Detalii');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'view_details')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'view_details', N'Details anzeigen');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'view_details')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'view_details', N'Visa detaljer');
