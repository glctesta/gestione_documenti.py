-- ============================================================
-- Repairs Analysis Cache — tabella per i dati di riparazione
-- Schema: Traceability_RS.fls
-- ============================================================
USE [Traceability_RS];
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
    WHERE t.name = 'RepairsAnalysisCache' AND s.name = 'fls'
)
BEGIN
    CREATE TABLE [fls].[RepairsAnalysisCache] (
        [ID]             INT IDENTITY(1,1) NOT NULL CONSTRAINT [PK_RepairsCache] PRIMARY KEY,
        [IDBoard]        INT               NULL,
        [Labels]         NVARCHAR(2000)    NOT NULL,
        [ProductCode]    NVARCHAR(200)     NULL,
        [OrderNumber]    NVARCHAR(200)     NULL,
        [PhaseName]      NVARCHAR(400)     NULL,
        [ResultRepair]   NVARCHAR(20)      NULL,   -- 'REPAIRED' or 'SCRAP'
        [DateRepair]     DATETIME          NULL,
        [CodRiferimento] NVARCHAR(500)     NULL,
        [Defect]         NVARCHAR(1000)    NULL,
        [QueryFrom]      DATETIME          NOT NULL,
        [QueryTo]        DATETIME          NOT NULL,
        [CachedAt]       DATETIME          NOT NULL CONSTRAINT [DF_RepairsCache_CachedAt] DEFAULT GETDATE()
    );
    CREATE INDEX [IX_RepairsCache_Labels]     ON [fls].[RepairsAnalysisCache] ([Labels]);
    CREATE INDEX [IX_RepairsCache_QueryRange] ON [fls].[RepairsAnalysisCache] ([QueryFrom],[QueryTo]);
    CREATE INDEX [IX_RepairsCache_Result]     ON [fls].[RepairsAnalysisCache] ([ResultRepair]);
    PRINT 'Tabella [fls].[RepairsAnalysisCache] creata.';
END
ELSE
    PRINT 'Tabella [fls].[RepairsAnalysisCache] gia'' esistente.';
GO

-- Aggiunge ResolvedAs a FailsAnalysisCache se mancante
IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    INNER JOIN sys.tables t ON t.object_id = c.object_id
    INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
    WHERE s.name='fls' AND t.name='FailsAnalysisCache' AND c.name='ResolvedAs'
)
BEGIN
    ALTER TABLE [fls].[FailsAnalysisCache] ADD [ResolvedAs] NVARCHAR(20) NULL;
    PRINT 'Colonna ResolvedAs aggiunta a FailsAnalysisCache.';
END
GO
