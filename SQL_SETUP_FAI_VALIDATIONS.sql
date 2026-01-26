/*
Script SQL per la gestione delle validazioni di linea (FAI - First Article Inspection)
Assicura che tutte le tabelle e relazioni necessarie esistano
*/

USE [Traceability_RS];
GO

-- Verifica che lo schema fai esista
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'fai')
BEGIN
    EXEC('CREATE SCHEMA fai');
    PRINT 'Schema fai creato';
END
GO

-- Tabella FaiLogHeathers (intestazioni log validazione)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[fai].[FaiLogHeathers]') AND type in (N'U'))
BEGIN
    CREATE TABLE [fai].[FaiLogHeathers](
        [FaiLogId] [int] IDENTITY(1,1) NOT NULL,
        [NPI] [bit] NULL DEFAULT(0),
        [Test] [bit] NULL DEFAULT(0),
        [PRODUCTION] [bit] NULL DEFAULT(0),
        [StandardProcessDeviation] [bit] NULL DEFAULT(0),
        [Others] [bit] NULL DEFAULT(0),
        [DateIn] [datetime] NOT NULL DEFAULT(GETDATE()),
        [UserIn] [nvarchar](50) NULL,
        [DateOut] [datetime] NULL,
        [UserOut] [nvarchar](50) NULL,
        CONSTRAINT [PK_FaiLogHeathers] PRIMARY KEY CLUSTERED ([FaiLogId] ASC)
    );
    PRINT 'Tabella FaiLogHeathers creata';
END
GO

-- Tabella FaiLogs (dettagli log per ogni step)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[fai].[FaiLogs]') AND type in (N'U'))
BEGIN
    CREATE TABLE [fai].[FaiLogs](
        [FaiLogDetailId] [int] IDENTITY(1,1) NOT NULL,
        [FaiLogId] [int] NOT NULL,
        [FaiStepDetailId] [int] NOT NULL,
        [isOK] [bit] NOT NULL DEFAULT(1),
        [DateIn] [datetime] NOT NULL DEFAULT(GETDATE()),
        [UserIn] [nvarchar](50) NULL,
        [DateOut] [datetime] NULL,
        [UserOut] [nvarchar](50) NULL,
        [Notes] [nvarchar](500) NULL,
        CONSTRAINT [PK_FaiLogs] PRIMARY KEY CLUSTERED ([FaiLogDetailId] ASC),
        CONSTRAINT [FK_FaiLogs_FaiLogHeathers] FOREIGN KEY([FaiLogId]) 
            REFERENCES [fai].[FaiLogHeathers] ([FaiLogId]),
        CONSTRAINT [FK_FaiLogs_FaiStepDetails] FOREIGN KEY([FaiStepDetailId]) 
            REFERENCES [fai].[FaiStepDetails] ([FaiStepDetailId])
    );
    PRINT 'Tabella FaiLogs creata';
END
GO

-- Indici per performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_FaiLogs_FaiLogId' AND object_id = OBJECT_ID('fai.FaiLogs'))
BEGIN
    CREATE NONCLUSTERED INDEX [IX_FaiLogs_FaiLogId] ON [fai].[FaiLogs]
    (
        [FaiLogId] ASC
    );
    PRINT 'Indice IX_FaiLogs_FaiLogId creato';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_FaiLogs_FaiStepDetailId' AND object_id = OBJECT_ID('fai.FaiLogs'))
BEGIN
    CREATE NONCLUSTERED INDEX [IX_FaiLogs_FaiStepDetailId] ON [fai].[FaiLogs]
    (
        [FaiStepDetailId] ASC
    );
    PRINT 'Indice IX_FaiLogs_FaiStepDetailId creato';
END
GO

PRINT 'Setup database per validazioni FAI completato con successo';
GO
