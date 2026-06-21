-- ============================================================================
-- Permesso: Configurazione Scorte Minime Materiali Indiretti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Chiave permesso (TranslationKey): Stock_minimo_met_indiretti
--
-- I permessi sono righe di AppTranslations con MenuValue NON NULL: cosi' la
-- chiave compare nella UI di assegnazione permessi (fetch_available_permissions)
-- e puo' essere concessa agli utenti (grant_permission richiede la riga 'it').
-- L'autorizzazione runtime verifica dbo.AutorizedUsers per questa TranslationKey.
--
-- Idempotente: rieseguibile senza creare duplicati.
-- DOPO l'esecuzione: assegnare il permesso agli utenti dalla gestione permessi.
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'Stock_minimo_met_indiretti' AND LanguageCode = 'it')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('it', 'Stock_minimo_met_indiretti',
            N'Configura Scorte Minime Materiali Indiretti',
            N'Configura Scorte Minime Materiali Indiretti');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'Stock_minimo_met_indiretti' AND LanguageCode = 'en')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('en', 'Stock_minimo_met_indiretti',
            N'Configure Indirect Materials Minimum Stock',
            N'Configure Indirect Materials Minimum Stock');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'Stock_minimo_met_indiretti' AND LanguageCode = 'ro')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('ro', 'Stock_minimo_met_indiretti',
            N'Configurare Stoc Minim Materiale Indirecte',
            N'Configurare Stoc Minim Materiale Indirecte');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'Stock_minimo_met_indiretti' AND LanguageCode = 'de')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('de', 'Stock_minimo_met_indiretti',
            N'Mindestbestand Indirektes Material konfigurieren',
            N'Mindestbestand Indirektes Material konfigurieren');

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
               WHERE TranslationKey = 'Stock_minimo_met_indiretti' AND LanguageCode = 'sv')
    INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('sv', 'Stock_minimo_met_indiretti',
            N'Konfigurera minimilager indirekta material',
            N'Konfigurera minimilager indirekta material');

PRINT 'Permesso Stock_minimo_met_indiretti registrato in AppTranslations.';
