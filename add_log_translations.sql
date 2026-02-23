-- ============================================================
-- Traduzioni per le voci del Log Viewer (menu Aiuto > Logs)
-- Chiavi: menu_logs, select_log_to_open, open_in_notepad, no_logs_found
-- Lingue: IT, EN, DE, RO, SV
-- ============================================================

-- ---- IT ----
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'menu_logs')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'menu_logs', N'Logs');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'select_log_to_open')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'select_log_to_open', N'Seleziona il log da aprire:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'open_in_notepad')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'open_in_notepad', N'Apri in Notepad');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'IT' AND [TranslationKey] = N'no_logs_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'IT', N'no_logs_found', N'Nessun file log trovato.');

-- ---- EN ----
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'menu_logs')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'menu_logs', N'Logs');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'select_log_to_open')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'select_log_to_open', N'Select the log to open:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'open_in_notepad')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'open_in_notepad', N'Open in Notepad');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'EN' AND [TranslationKey] = N'no_logs_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'EN', N'no_logs_found', N'No log files found.');

-- ---- DE ----
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'menu_logs')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'menu_logs', N'Protokolle');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'select_log_to_open')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'select_log_to_open', N'Protokolldatei zum Öffnen auswählen:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'open_in_notepad')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'open_in_notepad', N'In Notepad öffnen');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'DE' AND [TranslationKey] = N'no_logs_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'DE', N'no_logs_found', N'Keine Protokolldateien gefunden.');

-- ---- RO ----
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'menu_logs')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'menu_logs', N'Jurnale');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'select_log_to_open')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'select_log_to_open', N'Selectați jurnalul de deschis:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'open_in_notepad')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'open_in_notepad', N'Deschide în Notepad');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'RO' AND [TranslationKey] = N'no_logs_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'RO', N'no_logs_found', N'Nu s-au găsit fișiere jurnal.');

-- ---- SV ----
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'menu_logs')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'menu_logs', N'Loggar');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'select_log_to_open')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'select_log_to_open', N'Välj loggfil att öppna:');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'open_in_notepad')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'open_in_notepad', N'Öppna i Notepad');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = N'SV' AND [TranslationKey] = N'no_logs_found')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'SV', N'no_logs_found', N'Inga loggfiler hittades.');

-- ============================================================
-- Verifica risultato
-- ============================================================
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] IN (N'menu_logs', N'select_log_to_open', N'open_in_notepad', N'no_logs_found')
ORDER BY [TranslationKey], [LanguageCode];
