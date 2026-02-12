-- =============================================
-- Script per creare tabella OverTime_Reason
-- Database: ResetServices
-- =============================================

USE [ResetServices]
GO

-- Crea la tabella se non esiste
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[OverTime_Reason]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[OverTime_Reason](
        [IdMotivo] [int] NOT NULL,
        [OverTime_Reason] [nvarchar](100) NOT NULL,
        [Ordine] [int] NOT NULL,
        [ObbgligoOrdine] [nvarchar](3) NOT NULL,
        [MaxIterazioniMese] [int] NOT NULL,
        [Justify] [nvarchar](3) NOT NULL,
        CONSTRAINT [PK_OverTime_Reason] PRIMARY KEY CLUSTERED ([IdMotivo] ASC)
    ) ON [PRIMARY]
    
    PRINT N'Tabella OverTime_Reason creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella OverTime_Reason già esistente'
END
GO

-- Inserisci i dati (con controllo per evitare duplicati)
IF NOT EXISTS (SELECT 1 FROM [dbo].[OverTime_Reason])
BEGIN
    INSERT INTO [dbo].[OverTime_Reason] (IdMotivo, OverTime_Reason, Ordine, ObbgligoOrdine, MaxIterazioniMese, Justify)
    VALUES
        (13, N'Customer request [urgent order]', 0, N'Yes', 0, N'Yes'),
        (1, N'Complete order on late', 1, N'Yes', 50, N'No'),
        (7, N'Quality activity', 2, N'Yes', 1, N'No'),
        (8, N'Rework order', 3, N'No', 1, N'No'),
        (9, N'Maintenance', 4, N'No', 2, N'Yes'),
        (10, N'Machine breakdown', 5, N'No', 9999, N'No'),
        (11, N'Technical support', 6, N'No', 999, N'Yes'),
        (2, N'Substitute a couleague', 7, N'No', 3, N'No'),
        (3, N'Cleaning department', 8, N'No', 2, N'No'),
        (4, N'Changing Layout', 9, N'No', 1, N'No'),
        (5, N'Training', 10, N'No', 2, N'Yes'),
        (6, N'Inventory', 11, N'No', 3, N'No'),
        (12, N'Preformat material', 12, N'Yes', 4, N'No'),
        (15, N'Kitting', 13, N'No', 0, N'No'),
        (16, N'Incoming', 14, N'No', 0, N'No'),
        (14, N'Controller overtime activity', 15, N'No', 0, N'No');
    
    PRINT N'16 motivi straordinario inseriti con successo'
END
ELSE
BEGIN
    PRINT N'Dati già presenti nella tabella OverTime_Reason'
END
GO

-- Verifica i dati inseriti
SELECT COUNT(*) AS TotalRecords FROM [dbo].[OverTime_Reason]
GO

SELECT * FROM [dbo].[OverTime_Reason] ORDER BY Ordine
GO

PRINT N'Script completato con successo!'
