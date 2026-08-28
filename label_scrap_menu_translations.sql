-- ============================================================================
-- Traduzioni per voce di menu Assegna Famiglia (scarti etichette)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-08-28
-- ============================================================================

-- submenu_assign_material_families
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_assign_material_families' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_assign_material_families', 'Assegna Famiglia');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_assign_material_families' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_assign_material_families', 'Assign Family');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_assign_material_families' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_assign_material_families', N'Atribuie Familie');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_assign_material_families' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_assign_material_families', 'Familie zuweisen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_assign_material_families' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_assign_material_families', 'Tilldela Familj');

PRINT 'Traduzioni voce di menu Assegna Famiglia inserite con successo.';
