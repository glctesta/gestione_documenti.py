-- =============================================
-- Script per creare tabelle Straordinari
-- Database: ResetServices
-- =============================================

USE [ResetServices]
GO

-- =============================================
-- 1. Tabella ExtraTimeApproval (Richieste Straordinario)
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ExtraTimeApproval]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ExtraTimeApproval](
        [ExtraHourApprovalId] [int] IDENTITY(1,1) NOT NULL,
        [IdChief] [int] NOT NULL,
        [IdRegistro] [int] NOT NULL,
        [DateCreated] [datetime] NOT NULL DEFAULT GETDATE(),
        [Status] [nvarchar](20) NULL DEFAULT N'Pending',
        [ApprovedBy] [int] NULL,
        [ApprovedDate] [datetime] NULL,
        [Notes] [nvarchar](500) NULL,
        CONSTRAINT [PK_ExtraTimeApproval] PRIMARY KEY CLUSTERED ([ExtraHourApprovalId] ASC)
    ) ON [PRIMARY]
    
    PRINT N'Tabella ExtraTimeApproval creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella ExtraTimeApproval già esistente'
END
GO

-- =============================================
-- 2. Tabella ExtraTimeApprovalStory (Dettagli Dipendenti)
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ExtraTimeApprovalStory]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ExtraTimeApprovalStory](
        [ExtraTimeApprovalStoryId] [int] IDENTITY(1,1) NOT NULL,
        [ExtraHourApprovalId] [int] NOT NULL,
        [IdEmployee] [int] NOT NULL,
        [Descriptionreasons] [nvarchar](200) NOT NULL,
        [DateStart] [datetime] NOT NULL,
        [DateEnd] [datetime] NOT NULL,
        [SuperVisorId] [int] NULL,
        [Justify] [nvarchar](500) NULL,
        [IdOrder] [int] NULL,
        [QtyTarget] [decimal](18, 2) NULL,
        CONSTRAINT [PK_ExtraTimeApprovalStory] PRIMARY KEY CLUSTERED ([ExtraTimeApprovalStoryId] ASC),
        CONSTRAINT [FK_ExtraTimeApprovalStory_ExtraTimeApproval] FOREIGN KEY ([ExtraHourApprovalId])
            REFERENCES [dbo].[ExtraTimeApproval] ([ExtraHourApprovalId])
    ) ON [PRIMARY]
    
    PRINT N'Tabella ExtraTimeApprovalStory creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella ExtraTimeApprovalStory già esistente'
END
GO

-- =============================================
-- 3. Tabella ExtratimeOrders (Ordini Associati)
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ExtratimeOrders]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ExtratimeOrders](
        [ExtratimeOrderId] [int] IDENTITY(1,1) NOT NULL,
        [IdOrder] [int] NOT NULL,
        [NoQuantityToAchieve] [decimal](18, 2) NULL,
        [ExtraHourApprovalId] [int] NOT NULL,
        CONSTRAINT [PK_ExtratimeOrders] PRIMARY KEY CLUSTERED ([ExtratimeOrderId] ASC),
        CONSTRAINT [FK_ExtratimeOrders_ExtraTimeApproval] FOREIGN KEY ([ExtraHourApprovalId])
            REFERENCES [dbo].[ExtraTimeApproval] ([ExtraHourApprovalId])
    ) ON [PRIMARY]
    
    PRINT N'Tabella ExtratimeOrders creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella ExtratimeOrders già esistente'
END
GO

-- =============================================
-- Verifica tabelle create
-- =============================================
SELECT 
    'ExtraTimeApproval' AS TableName,
    COUNT(*) AS RecordCount
FROM [dbo].[ExtraTimeApproval]
UNION ALL
SELECT 
    'ExtraTimeApprovalStory' AS TableName,
    COUNT(*) AS RecordCount
FROM [dbo].[ExtraTimeApprovalStory]
UNION ALL
SELECT 
    'ExtratimeOrders' AS TableName,
    COUNT(*) AS RecordCount
FROM [dbo].[ExtratimeOrders]
GO

PRINT N'Script completato con successo!'
PRINT N'Tutte le tabelle per il modulo straordinari sono state create.'
