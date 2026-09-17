-- Script SQL per la gestione multipla dei documenti di calibrazione
-- Tabella: [Traceability_RS].[eqp].[CalibrationDocuments] (uno-a-molti rispetto a eqp.Calibrations)
-- Data: 2026-09-16
-- Nota: la colonna legacy eqp.Calibrations.NrCertificate NON viene svuotata:
--       i dati esistenti restano leggibili dai lettori "vecchi" e vengono
--       copiati (idempotentemente) nella nuova tabella.

USE [Traceability_RS];
GO

-- ============================================================================
-- 1. Creazione tabella CalibrationDocuments
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM sys.tables t
               INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
               WHERE s.name = N'eqp' AND t.name = N'CalibrationDocuments')
BEGIN
    CREATE TABLE [eqp].[CalibrationDocuments] (
        [Id]            INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [CalibrationId] INT NOT NULL,
        [FileName]      NVARCHAR(255) NOT NULL,
        [DocumentData]  VARBINARY(MAX) NULL,
        [UploadedBy]    NVARCHAR(100) NULL,
        [UploadedOn]    DATETIME NOT NULL CONSTRAINT [DF_CalibrationDocuments_UploadedOn] DEFAULT (GETDATE()),
        CONSTRAINT [FK_CalibrationDocuments_Calibrations]
            FOREIGN KEY ([CalibrationId]) REFERENCES [eqp].[Calibrations] ([CalibrationId])
    );
END
GO

-- ============================================================================
-- 2. Migrazione dati esistenti: NrCertificate -> CalibrationDocuments
--    (idempotente: salta le calibrazioni che hanno gia' almeno un documento)
-- ============================================================================

INSERT INTO [eqp].[CalibrationDocuments] ([CalibrationId], [FileName], [DocumentData], [UploadedBy], [UploadedOn])
SELECT c.[CalibrationId],
       N'certificato.pdf',
       c.[NrCertificate],
       c.[User],
       ISNULL(c.[DateSys], GETDATE())
FROM [eqp].[Calibrations] AS c
WHERE c.[NrCertificate] IS NOT NULL
  AND NOT EXISTS (SELECT 1
                  FROM [eqp].[CalibrationDocuments] AS cd
                  WHERE cd.[CalibrationId] = c.[CalibrationId]);
GO

-- Indice per lookup rapido per calibrazione
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = N'IX_CalibrationDocuments_CalibrationId'
                 AND object_id = OBJECT_ID(N'[eqp].[CalibrationDocuments]'))
BEGIN
    CREATE INDEX [IX_CalibrationDocuments_CalibrationId]
        ON [eqp].[CalibrationDocuments] ([CalibrationId]);
END
GO
