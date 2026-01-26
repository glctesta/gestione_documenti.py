-- Script SQL per aggiungere traduzioni per il bottone "Configura Ordinamento"
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, ro, en, de, sv
-- NOTA: N davanti a tutte le traduzioni per supporto Unicode

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'config_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'config_sort', N'⚙️ Configura Ordinamento');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'config_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'config_sort', N'⚙️ Configurare Sortare');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'config_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'config_sort', N'⚙️ Configure Sorting');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'config_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'config_sort', N'⚙️ Sortierung Konfigurieren');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'config_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'config_sort', N'⚙️ Konfigurera Sortering');
END

-- Verifica inserimenti
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] = 'config_sort'
ORDER BY [LanguageCode];
