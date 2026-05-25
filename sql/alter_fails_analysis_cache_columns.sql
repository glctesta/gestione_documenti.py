-- ============================================================
-- Allarga le colonne della tabella fls.FailsAnalysisCache
-- per evitare errori di truncation (22001) su dati reali.
-- Script idempotente - sicuro da eseguire più volte.
-- ============================================================

USE [Traceability_RS];
GO

ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [LabelCode]      NVARCHAR(1000) NOT NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [OrderNumber]    NVARCHAR(200)  NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [ProductCode]    NVARCHAR(200)  NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [PhaseName]      NVARCHAR(400)  NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [Labels]         NVARCHAR(2000) NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [ScanResult]     NVARCHAR(20)   NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [RepairResult]   NVARCHAR(40)   NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [DefectNameRO]   NVARCHAR(1000) NULL;
ALTER TABLE [fls].[FailsAnalysisCache]
    ALTER COLUMN [CodRiferimento] NVARCHAR(500)  NULL;

PRINT 'Colonne allargate con successo.';
GO
