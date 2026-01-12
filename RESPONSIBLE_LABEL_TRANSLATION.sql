-- =====================================================
-- Script traduzioni per Label Responsabile Piano Manutenzione
-- Data: 2026-01-12
-- Descrizione: Aggiunge traduzione per la label che mostra
--              il responsabile del piano di manutenzione
-- Lingue: IT, RO, EN, DE, SV
-- =====================================================

USE [Traceability_RS]
GO

-- ========== ITALIANO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'responsible_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('it', 'responsible_label', 'Responsabile');

-- ========== RUMENO (con N per caratteri speciali Unicode) ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'responsible_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('ro', 'responsible_label', 'Responsabil');

-- ========== INGLESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'responsible_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('en', 'responsible_label', 'Responsible');

-- ========== TEDESCO ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'responsible_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('de', 'responsible_label', 'Verantwortlicher');

-- ========== SVEDESE ==========
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'responsible_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) 
    VALUES ('sv', 'responsible_label', 'Ansvarig');

GO

PRINT '✅ Traduzione per label responsabile piano manutenzione aggiunta con successo!';
PRINT '   - Lingue supportate: IT, RO, EN, DE, SV';
PRINT '   - Chiave: responsible_label';
GO
