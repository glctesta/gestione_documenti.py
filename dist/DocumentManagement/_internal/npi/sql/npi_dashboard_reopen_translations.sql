-- Script SQL per aggiungere traduzioni per "Riapri Progetto" nel dashboard
-- Eseguire questo script sul database per aggiungere le chiavi di traduzione

USE [TraceabilityRS]
GO

-- Chiave per il menu contestuale
IF NOT EXISTS (SELECT 1 FROM [dbo].[Traduzioni] WHERE [Chiave] = 'npi_reopen_project')
BEGIN
    INSERT INTO [dbo].[Traduzioni] ([Chiave], [TestoItaliano], [TestoInglese])
    VALUES ('npi_reopen_project', 'Riapri Progetto', 'Reopen Project');
    PRINT 'Aggiunta traduzione: npi_reopen_project';
END
ELSE
BEGIN
    PRINT 'Traduzione npi_reopen_project già esistente';
END
GO

-- Chiave per il messaggio di conferma
IF NOT EXISTS (SELECT 1 FROM [dbo].[Traduzioni] WHERE [Chiave] = 'npi_reopen_project_confirm')
BEGIN
    INSERT INTO [dbo].[Traduzioni] ([Chiave], [TestoItaliano], [TestoInglese])
    VALUES ('npi_reopen_project_confirm', 
            'Sei sicuro di voler riaprire il progetto ''{0}''?\n\nIl progetto tornerà allo stato ''Attivo''.', 
            'Are you sure you want to reopen project ''{0}''?\n\nThe project will return to ''Active'' status.');
    PRINT 'Aggiunta traduzione: npi_reopen_project_confirm';
END
ELSE
BEGIN
    PRINT 'Traduzione npi_reopen_project_confirm già esistente';
END
GO

-- Chiave per il messaggio di successo
IF NOT EXISTS (SELECT 1 FROM [dbo].[Traduzioni] WHERE [Chiave] = 'npi_reopen_project_success')
BEGIN
    INSERT INTO [dbo].[Traduzioni] ([Chiave], [TestoItaliano], [TestoInglese])
    VALUES ('npi_reopen_project_success', 
            'Progetto ''{0}'' riaperto con successo.', 
            'Project ''{0}'' reopened successfully.');
    PRINT 'Aggiunta traduzione: npi_reopen_project_success';
END
ELSE
BEGIN
    PRINT 'Traduzione npi_reopen_project_success già esistente';
END
GO

-- Chiave per il messaggio di errore
IF NOT EXISTS (SELECT 1 FROM [dbo].[Traduzioni] WHERE [Chiave] = 'npi_reopen_project_failed')
BEGIN
    INSERT INTO [dbo].[Traduzioni] ([Chiave], [TestoItaliano], [TestoInglese])
    VALUES ('npi_reopen_project_failed', 
            'Impossibile riaprire il progetto.', 
            'Unable to reopen the project.');
    PRINT 'Aggiunta traduzione: npi_reopen_project_failed';
END
ELSE
BEGIN
    PRINT 'Traduzione npi_reopen_project_failed già esistente';
END
GO

PRINT 'Script completato con successo!';
GO
