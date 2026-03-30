-- ============================================================================
-- RMA Knowledge Base — ALTER TABLE per colonne originali italiane
-- Da eseguire DOPO rma_schema.sql
-- Generato: 2026-03-27
-- ============================================================================

USE [Traceability_RS];
GO

-- Colonne IT per salvare l'originale italiano (il campo principale conterrà la traduzione RO)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.RmaRecords') AND name = 'FaultDescriptionIT')
    ALTER TABLE [dbo].[RmaRecords] ADD [FaultDescriptionIT] NVARCHAR(MAX) NULL;
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.RmaRecords') AND name = 'FaultCauseIT')
    ALTER TABLE [dbo].[RmaRecords] ADD [FaultCauseIT] NVARCHAR(200) NULL;
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.RmaRecords') AND name = 'FaultNotesIT')
    ALTER TABLE [dbo].[RmaRecords] ADD [FaultNotesIT] NVARCHAR(MAX) NULL;
GO

-- Colonne IT per le lookup tables
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.RmaFaultTypes') AND name = 'DescriptionIT')
    ALTER TABLE [dbo].[RmaFaultTypes] ADD [DescriptionIT] NVARCHAR(200) NULL;
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.RmaFaultDetails') AND name = 'DescriptionIT')
    ALTER TABLE [dbo].[RmaFaultDetails] ADD [DescriptionIT] NVARCHAR(200) NULL;
GO

-- Aggiorna i seed esistenti con le versioni IT (già in italiano nel seed originale)
UPDATE [dbo].[RmaFaultTypes] SET [DescriptionIT] = [Description] WHERE [DescriptionIT] IS NULL;
GO

UPDATE [dbo].[RmaFaultDetails] SET [DescriptionIT] = [Description] WHERE [DescriptionIT] IS NULL;
GO

PRINT 'Colonne IT aggiunte con successo.';
GO
