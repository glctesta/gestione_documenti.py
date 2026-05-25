-- ============================================================
-- Analisi Fails — Schema e tabella di cache
-- Schema: Traceability_RS.fls
-- Eseguire una volta sola su ogni ambiente (script idempotente)
-- ============================================================

USE [Traceability_RS];
GO

-- 1. Crea lo schema fls se non esiste
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'fls')
BEGIN
    EXEC('CREATE SCHEMA [fls]');
    PRINT 'Schema [fls] creato.';
END
ELSE
BEGIN
    PRINT 'Schema [fls] già esistente.';
END
GO

-- 2. Crea la tabella di cache se non esiste
IF NOT EXISTS (
    SELECT 1
    FROM sys.tables t
    INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
    WHERE t.name = 'FailsAnalysisCache' AND s.name = 'fls'
)
BEGIN
    CREATE TABLE [Traceability_RS].[fls].[FailsAnalysisCache] (
        [ID]             INT IDENTITY(1,1)  NOT NULL,
        [IDBoard]        INT                NOT NULL,
        [LabelCode]      NVARCHAR(100)      NOT NULL,
        [OrderNumber]    NVARCHAR(100)      NULL,
        [ProductCode]    NVARCHAR(100)      NULL,
        [OrderQuantity]  INT                NULL,
        [PhaseName]      NVARCHAR(200)      NULL,
        [Labels]         NVARCHAR(500)      NULL,
        [ScanResult]     NVARCHAR(10)       NULL,
        [ScanTime]       DATETIME           NULL,
        [RepairResult]   NVARCHAR(20)       NULL,
        [DefectNameRO]   NVARCHAR(300)      NULL,
        [CodRiferimento] NVARCHAR(200)      NULL,
        [QueryFrom]      DATETIME           NOT NULL,
        [QueryTo]        DATETIME           NOT NULL,
        [CachedAt]       DATETIME           NOT NULL CONSTRAINT [DF_FailsCache_CachedAt] DEFAULT GETDATE(),
        [ResolvedAt]     DATETIME           NULL,      -- valorizzato quando la scheda non compare più nella query del giorno
        CONSTRAINT [PK_FailsAnalysisCache] PRIMARY KEY CLUSTERED ([ID] ASC)
    );

    -- Indici per le query più frequenti
    CREATE NONCLUSTERED INDEX [IX_FailsCache_LabelCode]
        ON [Traceability_RS].[fls].[FailsAnalysisCache] ([LabelCode]);

    CREATE NONCLUSTERED INDEX [IX_FailsCache_IDBoard]
        ON [Traceability_RS].[fls].[FailsAnalysisCache] ([IDBoard]);

    CREATE NONCLUSTERED INDEX [IX_FailsCache_ResolvedAt]
        ON [Traceability_RS].[fls].[FailsAnalysisCache] ([ResolvedAt]);

    CREATE NONCLUSTERED INDEX [IX_FailsCache_QueryRange]
        ON [Traceability_RS].[fls].[FailsAnalysisCache] ([QueryFrom], [QueryTo]);

    PRINT 'Tabella [fls].[FailsAnalysisCache] creata con successo.';
END
ELSE
BEGIN
    PRINT 'Tabella [fls].[FailsAnalysisCache] già esistente.';
END
GO
