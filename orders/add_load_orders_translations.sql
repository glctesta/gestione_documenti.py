-- Script SQL per aggiungere le traduzioni dei nuovi campi della finestra Load Orders
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Nuovi translation keys: days_filter, col_last_update, col_linked

USE [Traceability_RS];
GO

-- ============================================================================
-- Translation Key: days_filter
-- Descrizione: Etichetta per il filtro giorni dalla data odierna
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'days_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'days_filter', N'Giorni dalla data odierna:');
    PRINT 'Aggiunta traduzione: days_filter (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: days_filter (it)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'days_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'days_filter', N'Zile de la data curentă:');
    PRINT 'Aggiunta traduzione: days_filter (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: days_filter (ro)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'days_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'days_filter', N'Days from today:');
    PRINT 'Aggiunta traduzione: days_filter (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: days_filter (en)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'days_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'days_filter', N'Tage ab heute:');
    PRINT 'Aggiunta traduzione: days_filter (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: days_filter (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'days_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'days_filter', N'Dagar från idag:');
    PRINT 'Aggiunta traduzione: days_filter (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: days_filter (sv)';
END
GO

-- ============================================================================
-- Translation Key: linked_filter
-- Descrizione: Etichetta per il filtro stato collegamento
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'linked_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'linked_filter', N'Collegato:');
    PRINT 'Aggiunta traduzione: linked_filter (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: linked_filter (it)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'linked_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'linked_filter', N'Conectat:');
    PRINT 'Aggiunta traduzione: linked_filter (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: linked_filter (ro)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'linked_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'linked_filter', N'Linked:');
    PRINT 'Aggiunta traduzione: linked_filter (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: linked_filter (en)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'linked_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'linked_filter', N'Verknüpft:');
    PRINT 'Aggiunta traduzione: linked_filter (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: linked_filter (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'linked_filter')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'linked_filter', N'Länkad:');
    PRINT 'Aggiunta traduzione: linked_filter (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: linked_filter (sv)';
END
GO

-- ============================================================================
-- Translation Key: col_last_update
-- Descrizione: Intestazione colonna per ultimo aggiornamento
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_last_update')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'col_last_update', N'Ultimo Agg.');
    PRINT 'Aggiunta traduzione: col_last_update (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_last_update (it)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_last_update')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'col_last_update', N'Ultima Actualizare');
    PRINT 'Aggiunta traduzione: col_last_update (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_last_update (ro)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_last_update')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'col_last_update', N'Last Update');
    PRINT 'Aggiunta traduzione: col_last_update (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_last_update (en)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_last_update')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'col_last_update', N'Letzte Aktualisierung');
    PRINT 'Aggiunta traduzione: col_last_update (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_last_update (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_last_update')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'col_last_update', N'Senaste Uppdatering');
    PRINT 'Aggiunta traduzione: col_last_update (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_last_update (sv)';
END
GO

-- ============================================================================
-- Translation Key: col_linked
-- Descrizione: Intestazione colonna per stato collegamento a produzione
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_linked')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'col_linked', N'Collegato');
    PRINT 'Aggiunta traduzione: col_linked (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_linked (it)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_linked')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'col_linked', N'Conectat');
    PRINT 'Aggiunta traduzione: col_linked (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_linked (ro)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_linked')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'col_linked', N'Linked');
    PRINT 'Aggiunta traduzione: col_linked (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_linked (en)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_linked')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'col_linked', N'Verknüpft');
    PRINT 'Aggiunta traduzione: col_linked (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_linked (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] 
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_linked')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'col_linked', N'Länkad');
    PRINT 'Aggiunta traduzione: col_linked (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: col_linked (sv)';
END
GO

-- ============================================================================
-- Verifica traduzioni aggiunte
-- ============================================================================

PRINT '';
PRINT '============================================================================';
PRINT 'Riepilogo traduzioni aggiunte per Load Orders Window';
PRINT '============================================================================';
PRINT '';

SELECT 
    [TranslationKey],
    [LanguageCode],
    [TranslationValue]
FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN ('days_filter', 'linked_filter', 'col_last_update', 'col_linked')
ORDER BY [TranslationKey], [LanguageCode];

PRINT '';
PRINT 'Script completato con successo!';
GO
