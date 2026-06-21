-- ============================================================================
-- Permesso: Invio Riordino Materiali Indiretti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Chiave permesso (TranslationKey): riordine_materiali_indiretti
--
-- Protegge il pulsante "Invia riordino ora" nella finestra Verifica Giacenze.
-- I permessi sono righe di AppTranslations con MenuValue NON NULL (la riga 'it'
-- e' obbligatoria per l'assegnazione). L'autorizzazione runtime verifica
-- dbo.AutorizedUsers per questa TranslationKey.
--
-- Idempotente: rieseguibile senza creare duplicati.
-- DOPO l'esecuzione: assegnare il permesso agli utenti dalla gestione permessi.
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'riordine_materiali_indiretti' AND LanguageCode = 'it')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('it', 'riordine_materiali_indiretti',
            N'Invio Riordino Materiali Indiretti',
            N'Invio Riordino Materiali Indiretti');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'riordine_materiali_indiretti' AND LanguageCode = 'en')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('en', 'riordine_materiali_indiretti',
            N'Send Indirect Materials Reorder',
            N'Send Indirect Materials Reorder');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'riordine_materiali_indiretti' AND LanguageCode = 'ro')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('ro', 'riordine_materiali_indiretti',
            N'Trimitere Recomandă Materiale Indirecte',
            N'Trimitere Recomandă Materiale Indirecte');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'riordine_materiali_indiretti' AND LanguageCode = 'de')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('de', 'riordine_materiali_indiretti',
            N'Nachbestellung Indirektes Material senden',
            N'Nachbestellung Indirektes Material senden');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'riordine_materiali_indiretti' AND LanguageCode = 'sv')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('sv', 'riordine_materiali_indiretti',
            N'Skicka beställning indirekta material',
            N'Skicka beställning indirekta material');

PRINT 'Permesso riordine_materiali_indiretti registrato in AppTranslations.';
