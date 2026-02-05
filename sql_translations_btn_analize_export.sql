-- =============================================
-- Script: Add translations for btn_analize and btn_export_pdf
-- Table: [Traceability_RS].[dbo].[AppTranslations]
-- Languages: ro, it, en, de, sv
-- Date: 2026-02-05
-- =============================================

-- Translation: btn_analize
-- Romanian
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'btn_analize')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'btn_analize', N'Analizează');
END

-- Italian
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'btn_analize')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'btn_analize', N'Analizza');
END

-- English
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'btn_analize')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'btn_analize', N'Analyze');
END

-- German
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'btn_analize')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'btn_analize', N'Analysieren');
END

-- Swedish
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'btn_analize')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'btn_analize', N'Analysera');
END

-- Translation: btn_export_pdf
-- Romanian
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'btn_export_pdf')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'btn_export_pdf', N'Exportă PDF');
END

-- Italian
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'btn_export_pdf')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'btn_export_pdf', N'Esporta PDF');
END

-- English
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'btn_export_pdf')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'btn_export_pdf', N'Export PDF');
END

-- German
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'btn_export_pdf')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'btn_export_pdf', N'PDF exportieren');
END

-- Swedish
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] 
               WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'btn_export_pdf')
BEGIN
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'btn_export_pdf', N'Exportera PDF');
END

-- =============================================
-- End of script
-- =============================================
