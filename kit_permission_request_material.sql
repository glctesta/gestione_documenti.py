-- ============================================================================
-- Permesso: Richiedi materiale kit (produzione)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Chiave permesso (TranslationKey): richiedi_materiale_kit
--
-- Protegge il pulsante "Nuova richiesta" nel tab Richieste Materiale della
-- finestra Priorita' Ordini Kit: la produzione puo' richiedere integrazioni
-- solo dopo login AUTORIZZATO (_execute_authorized_action).
--
-- I permessi sono righe di AppTranslations con MenuValue NON NULL (la riga 'it'
-- e' obbligatoria per l'assegnazione). L'autorizzazione runtime verifica
-- dbo.AutorizedUsers per questa TranslationKey.
--
-- Idempotente: rieseguibile senza creare duplicati.
-- DOPO l'esecuzione: assegnare il permesso agli operatori di produzione dalla
-- gestione permessi, altrimenti nessuno potra' creare richieste.
-- ============================================================================

USE [Traceability_RS];
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'richiedi_materiale_kit' AND LanguageCode = 'it')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('it', 'richiedi_materiale_kit',
            N'Richiedi Materiale Kit', N'Richiedi Materiale Kit');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'richiedi_materiale_kit' AND LanguageCode = 'en')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('en', 'richiedi_materiale_kit',
            N'Request Kit Material', N'Request Kit Material');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'richiedi_materiale_kit' AND LanguageCode = 'ro')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('ro', 'richiedi_materiale_kit',
            N'Cerere Material Kit', N'Cerere Material Kit');

PRINT 'Permesso richiedi_materiale_kit registrato in AppTranslations.';
PRINT 'Ricordarsi di assegnarlo agli operatori di produzione.';
GO
