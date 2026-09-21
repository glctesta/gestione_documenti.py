-- ============================================================================
-- Kanban produzione — traduzioni menu + chiave permesso
-- Chiave permesso: 'crea_kanBan_produzione' (MenuValue obbligatorio per 'it',
-- altrimenti grant_permission rifiuta la concessione)
-- ============================================================================

-- menu_kanban_produzione
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kanban_produzione' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'menu_kanban_produzione', 'Kanban produzione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kanban_produzione' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'menu_kanban_produzione', 'Production Kanban');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kanban_produzione' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'menu_kanban_produzione', 'Kanban producție');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kanban_produzione' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'menu_kanban_produzione', 'Produktionskanban');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'menu_kanban_produzione' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'menu_kanban_produzione', 'Produktionskanban');

-- submenu_kanban_carica_schede
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_carica_schede' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_kanban_carica_schede', 'Carica schede');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_carica_schede' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_kanban_carica_schede', 'Load boards');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_carica_schede' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_kanban_carica_schede', 'Încarcă plăci');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_carica_schede' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_kanban_carica_schede', 'Platinen einlagern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_carica_schede' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_kanban_carica_schede', 'Ladda kort');

-- submenu_kanban_preleva_schede
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_preleva_schede' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('it', 'submenu_kanban_preleva_schede', 'Preleva schede');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_preleva_schede' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('en', 'submenu_kanban_preleva_schede', 'Pick boards');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_preleva_schede' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro', 'submenu_kanban_preleva_schede', 'Ridică plăci');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_preleva_schede' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('de', 'submenu_kanban_preleva_schede', 'Platinen entnehmen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'submenu_kanban_preleva_schede' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv', 'submenu_kanban_preleva_schede', 'Plocka kort');

-- crea_kanBan_produzione (chiave permesso — MenuValue 'it' OBBLIGATORIO)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'crea_kanBan_produzione' AND LanguageCode = 'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES ('it', 'crea_kanBan_produzione', 'Kanban produzione', 'Kanban produzione');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'crea_kanBan_produzione' AND LanguageCode = 'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES ('en', 'crea_kanBan_produzione', 'Production Kanban', 'Production Kanban');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'crea_kanBan_produzione' AND LanguageCode = 'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES ('ro', 'crea_kanBan_produzione', 'Kanban producție', 'Kanban producție');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'crea_kanBan_produzione' AND LanguageCode = 'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES ('de', 'crea_kanBan_produzione', 'Produktionskanban', 'Produktionskanban');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = 'crea_kanBan_produzione' AND LanguageCode = 'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue, MenuValue) VALUES ('sv', 'crea_kanBan_produzione', 'Produktionskanban', 'Produktionskanban');

PRINT 'Traduzioni Kanban produzione inserite.';
PRINT 'NOTA: configurare i destinatari email inserendo righe in dbo.settings:';
PRINT '  atribute = sys_mail_wip_kanban, VALUE = indirizzo email (una riga per destinatario)';
PRINT 'NOTA: concedere il permesso con insert in dbo.AutorizedUsers (EmployeeHireHistoryId, TranslationKey = crea_kanBan_produzione).';
