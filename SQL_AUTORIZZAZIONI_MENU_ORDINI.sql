-- Script SQL per aggiungere le chiavi di autorizzazione per il menu Ordini
-- Data: 2026-01-19
-- Nota: Questo script aggiunge le chiavi di autorizzazione che devono essere configurate
-- nella tabella delle autorizzazioni utente/menu

USE [Traceability_RS];
GO

PRINT '=========================================================================';
PRINT 'IMPORTANTE: Configurazione chiavi autorizzazione menu Ordini';
PRINT '=========================================================================';
PRINT '';
PRINT 'Le seguenti chiavi di autorizzazione sono state implementate nel codice:';
PRINT '';
PRINT '1. Aggiungi_Ordini';
PRINT '   - Menu: Ordini -> Carica Ordini';
PRINT '   - Descrizione: Permette di caricare nuovi ordini nel sistema';
PRINT '';
PRINT '2. Accoppia_ordini_produzione';
PRINT '   - Menu: Ordini -> Accoppia Ordini Produzione';
PRINT '   - Descrizione: Permette di associare ordini a ordini di produzione';
PRINT '';
PRINT '3. Rapporti (NO autorizzazione richiesta)';
PRINT '   - Menu: Ordini -> Rapporti';
PRINT '   - Descrizione: Visualizza rapporti sugli ordini';
PRINT '';
PRINT '=========================================================================';
PRINT 'AZIONI NECESSARIE:';
PRINT '=========================================================================';
PRINT '';
PRINT '1. Aggiungere le chiavi "Aggiungi_Ordini" e "Accoppia_ordini_produzione"';
PRINT '   alla tabella delle autorizzazioni menu (es: MenuAuthorizations o simile)';
PRINT '';
PRINT '2. Assegnare agli utenti appropriati i permessi per queste funzionalità';
PRINT '';
PRINT '3. Esempio di query per aggiungere le chiavi (adattare al proprio schema):';
PRINT '';
PRINT '   INSERT INTO [MenuAuthorizations] (MenuKey, MenuDescription)';
PRINT '   VALUES (''Aggiungi_Ordini'', ''Permesso per caricare ordini'');';
PRINT '';
PRINT '   INSERT INTO [MenuAuthorizations] (MenuKey, MenuDescription)';
PRINT '   VALUES (''Accoppia_ordini_produzione'', ''Permesso per accoppiare ordini produzione'');';
PRINT '';
PRINT '=========================================================================';
PRINT '';

-- Se esiste una tabella specifica per le chiavi menu, decommentare e adattare:
/*
-- Esempio di inserimento chiavi (ADATTARE AL PROPRIO SCHEMA)
IF NOT EXISTS (SELECT 1 FROM [dbo].[MenuKeys] WHERE [MenuKey] = 'Aggiungi_Ordini')
    INSERT INTO [dbo].[MenuKeys] ([MenuKey], [Description], [MenuGroup])
    VALUES ('Aggiungi_Ordini', 'Carica Ordini', 'Ordini');

IF NOT EXISTS (SELECT 1 FROM [dbo].[MenuKeys] WHERE [MenuKey] = 'Accoppia_ordini_produzione')
    INSERT INTO [dbo].[MenuKeys] ([MenuKey], [Description], [MenuGroup])
    VALUES ('Accoppia_ordini_produzione', 'Accoppia Ordini Produzione', 'Ordini');
*/

GO
