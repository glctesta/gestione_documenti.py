-- ============================================================
-- Creazione tabelle mancanti per modulo Rapporti Attività Ospiti
-- Database: Employee
-- Data: 2026-03-12
-- ============================================================

USE [Employee]
GO

-- ============================================================
-- 1. VisitorContractInfo
--    Contratti delle società fatturanti (VisitorPlanToCharges)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.VisitorContractInfo') AND type = 'U')
BEGIN
    CREATE TABLE dbo.VisitorContractInfo (
        VisitorContractInfoId   INT IDENTITY(1,1) PRIMARY KEY,
        VisitorPlanToChargeID   BIGINT NOT NULL,
        ContractNumber          NVARCHAR(100) NULL,
        ContractDate            DATE NULL,
        ContractDescription     NVARCHAR(500) NULL
    );

    PRINT 'Tabella VisitorContractInfo creata con successo.';
END
ELSE
    PRINT 'Tabella VisitorContractInfo già esistente.';
GO

-- ============================================================
-- 2. VisitorActivityReports
--    Rapporti di attività generati per gli ospiti
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.VisitorActivityReports') AND type = 'U')
BEGIN
    CREATE TABLE dbo.VisitorActivityReports (
        VisitorActivityReportId INT IDENTITY(1,1) PRIMARY KEY,
        VisitorId               INT NOT NULL,
        RequestLetterDoc        VARBINARY(MAX) NULL,
        AcceptanceLetterDoc     VARBINARY(MAX) NULL,
        ActivityReportDoc       VARBINARY(MAX) NULL,
        RequestLetterDate       DATE NULL,
        AcceptanceLetterDate    DATE NULL,
        ActivityReportDate      DATE NULL,
        ActivityDescription     NVARCHAR(MAX) NULL,
        EmailSentDate           DATETIME NULL,
        EmailSentTo             NVARCHAR(500) NULL,
        CreatedBy               NVARCHAR(100) NULL,
        CreatedAt               DATETIME DEFAULT GETDATE(),

        CONSTRAINT FK_VisitorActivityReports_Visitors
            FOREIGN KEY (VisitorId)
            REFERENCES dbo.Visitors(VisitorId)
    );

    PRINT 'Tabella VisitorActivityReports creata con successo.';
END
ELSE
    PRINT 'Tabella VisitorActivityReports già esistente.';
GO
