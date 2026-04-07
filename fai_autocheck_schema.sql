-- ============================================================
-- FAI Autocheck Notifications — Schema DDL
-- Database: Traceability_RS, Schema: fai
-- ============================================================

USE [Traceability_RS]
GO

-- Creazione tabella tracking
IF NOT EXISTS (SELECT 1 FROM sys.tables t
               INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
               WHERE s.name = 'fai' AND t.name = 'FaiAutocheckNotifications')
BEGIN
    CREATE TABLE [fai].[FaiAutocheckNotifications] (
        IdNotification            BIGINT IDENTITY(1,1) PRIMARY KEY,
        OrderNumber               NVARCHAR(50)      NOT NULL,
        IdPhase                   INT               NOT NULL,
        PhaseName                 NVARCHAR(100)     NOT NULL,
        FaiTemplateId             INT               NOT NULL,
        FaiTitle                  NVARCHAR(255)     NULL,
        NrDocument                NVARCHAR(100)     NULL,
        Revision                  NVARCHAR(50)      NULL,
        PlannedStart              DATETIME          NOT NULL,
        DetectionTime             DATETIME          NOT NULL DEFAULT GETDATE(),
        EmailSentTime             DATETIME          NULL,
        EmailTo                   NVARCHAR(MAX)     NULL,
        EmailCc                   NVARCHAR(MAX)     NULL,
        ProductionQtyAtCheck      INT               NULL,
        PresenceChecked           BIT               NOT NULL DEFAULT 0,
        NotificationStatus        NVARCHAR(30)      NOT NULL,
        VerificationCompleted     BIT               NOT NULL DEFAULT 0,
        VerificationCompletedTime DATETIME          NULL,
        NonComplianceFlag         BIT               NOT NULL DEFAULT 0,
        Notes                     NVARCHAR(1000)    NULL
    );

    PRINT 'Tabella fai.FaiAutocheckNotifications creata con successo.'
END
ELSE
    PRINT 'Tabella fai.FaiAutocheckNotifications già esistente.'
GO

-- Indice univoco anti-duplicazione
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'UX_FaiAutocheck_Unique'
                 AND object_id = OBJECT_ID('[fai].[FaiAutocheckNotifications]'))
BEGIN
    CREATE UNIQUE INDEX UX_FaiAutocheck_Unique
    ON [fai].[FaiAutocheckNotifications] (
        OrderNumber,
        IdPhase,
        FaiTemplateId,
        PlannedStart
    );

    PRINT 'Indice univoco UX_FaiAutocheck_Unique creato.'
END
ELSE
    PRINT 'Indice UX_FaiAutocheck_Unique già esistente.'
GO

-- Indice per query di ricerca per data
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'IX_FaiAutocheck_DetectionTime'
                 AND object_id = OBJECT_ID('[fai].[FaiAutocheckNotifications]'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_FaiAutocheck_DetectionTime
    ON [fai].[FaiAutocheckNotifications] (DetectionTime DESC)
    INCLUDE (OrderNumber, NotificationStatus);

    PRINT 'Indice IX_FaiAutocheck_DetectionTime creato.'
END
GO

PRINT 'Schema FAI Autocheck completato.'
