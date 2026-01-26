-- Script SQL per aggiungere traduzioni per il bottone "Reset Ordinamento"
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, ro, en, de, sv
-- NOTA: N davanti a tutte le traduzioni per supporto Unicode

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'reset_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('it', 'reset_sort', N'🔄 Reset Ordinamento');
END

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'reset_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('ro', 'reset_sort', N'🔄 Resetare Sortare');
END

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'reset_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('en', 'reset_sort', N'🔄 Reset Sorting');
END

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'reset_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('de', 'reset_sort', N'🔄 Sortierung Zurücksetzen');
END

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'reset_sort')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('sv', 'reset_sort', N'🔄 Återställ Sortering');
END

-- Verifica inserimenti
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE [TranslationKey] = 'reset_sort'
ORDER BY [LanguageCode];
