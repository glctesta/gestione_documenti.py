-- =============================================
-- Script per setup FAI Fails Auto-Email System
-- =============================================

USE [Traceability_RS]
GO

-- 1. Aggiungi campo IsAnalized alla tabella FaiLogs (se non esiste)
IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID(N'[fai].[FaiLogs]') 
    AND name = 'IsAnalized'
)
BEGIN
    ALTER TABLE [fai].[FaiLogs]
    ADD IsAnalized BIT DEFAULT 0
    
    PRINT 'Campo IsAnalized aggiunto alla tabella [fai].[FaiLogs]'
END
ELSE
BEGIN
    PRINT 'Campo IsAnalized già esistente nella tabella [fai].[FaiLogs]'
END
GO

-- 2. Aggiungi setting per destinatari CC email FAI fails
IF NOT EXISTS (
    SELECT 1 
    FROM [dbo].[Settings] 
    WHERE atribute = N'Sys_email_fai_fails'
)
BEGIN
    INSERT INTO [dbo].[Settings] (atribute, [VALUE])
    VALUES (N'Sys_email_fai_fails', N'gianluca.testa@vandewiele.com')
    
    PRINT 'Setting Sys_email_fai_fails aggiunto'
END
ELSE
BEGIN
    PRINT 'Setting Sys_email_fai_fails già esistente'
END
GO

PRINT ''
PRINT '✅ Setup FAI Fails Auto-Email System completato con successo!'
PRINT ''
PRINT 'Note:'
PRINT '- Campo IsAnalized aggiunto/verificato in [fai].[FaiLogs]'
PRINT '- Setting Sys_email_fai_fails configurato per destinatari CC'
PRINT '- Modifica il valore del setting per aggiungere altri destinatari CC (separati da ;)'
GO
