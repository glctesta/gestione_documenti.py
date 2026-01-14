-- ============================================================================
-- Script: CREATE_NPI_TASK_NOTIFICATIONS_TABLE.sql
-- Descrizione: Crea tabella per tracciare le notifiche automatiche inviate
--              per evitare duplicazioni
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- Tabella: NpiTaskNotifications
-- Scopo: Tracciare le email automatiche inviate per task in scadenza/scaduti
--        per evitare duplicazioni
-- ========================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[NpiTaskNotifications]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[NpiTaskNotifications] (
        [NotificationID] INT IDENTITY(1,1) PRIMARY KEY,
        
        -- Riferimenti
        [TaskProdottoID] INT NOT NULL,
        [ProgettoID] INT NOT NULL,
        [RecipientSoggettoID] INT NOT NULL,
        
        -- Tipo notifica
        [NotificationType] VARCHAR(50) NOT NULL, -- 'TaskDueTomorrow', 'TaskOverdue'
        [NotificationDate] DATE NOT NULL,        -- Data per cui è stata inviata la notifica
        
        -- Dettagli invio
        [SentDateTime] DATETIME NOT NULL DEFAULT GETDATE(),
        [RecipientEmail] VARCHAR(255) NOT NULL,
        [RecipientName] VARCHAR(255) NULL,
        [RecipientType] VARCHAR(50) NULL,       -- 'TaskOwner', 'ProjectOwner'
        
        -- Status
        [DeliveryStatus] VARCHAR(50) NOT NULL,  -- 'Sent', 'Failed', 'Skipped'
        [ErrorMessage] TEXT NULL,
        
        -- Metadata
        [CreatedBy] VARCHAR(100) DEFAULT 'AutoNotificationService',
        [CreatedDate] DATETIME DEFAULT GETDATE(),
        
        -- Foreign Keys
        CONSTRAINT FK_NpiTaskNotifications_TaskProdotto 
            FOREIGN KEY ([TaskProdottoID]) REFERENCES [dbo].[TaskProdotto]([TaskProdottoID]),
        
        CONSTRAINT FK_NpiTaskNotifications_Progetto 
            FOREIGN KEY ([ProgettoID]) REFERENCES [dbo].[ProgettiNPI]([ProgettoID])
    );
    
    PRINT 'Tabella NpiTaskNotifications creata con successo.';
END
ELSE
BEGIN
    PRINT 'Tabella NpiTaskNotifications già esistente.';
END
GO

-- ========================================
-- Indici per performance
-- ========================================

-- Indice per evitare duplicati
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_NpiTaskNotifications_Unique' AND object_id = OBJECT_ID('dbo.NpiTaskNotifications'))
BEGIN
    CREATE UNIQUE NONCLUSTERED INDEX IX_NpiTaskNotifications_Unique
    ON [dbo].[NpiTaskNotifications] (
        [TaskProdottoID],
        [RecipientSoggettoID],
        [NotificationType],
        [NotificationDate]
    );
    PRINT 'Indice univoco creato: IX_NpiTaskNotifications_Unique';
END
GO

-- Indice per query di ricerca
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_NpiTaskNotifications_Lookup' AND object_id = OBJECT_ID('dbo.NpiTaskNotifications'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_NpiTaskNotifications_Lookup
    ON [dbo].[NpiTaskNotifications] (
        [NotificationDate],
        [NotificationType],
        [DeliveryStatus]
    )
    INCLUDE ([TaskProdottoID], [RecipientEmail]);
    PRINT 'Indice di ricerca creato: IX_NpiTaskNotifications_Lookup';
END
GO

-- ========================================
-- Vista per statistiche
-- ========================================

IF OBJECT_ID('dbo.vw_NpiTaskNotificationsStats', 'V') IS NOT NULL
    DROP VIEW dbo.vw_NpiTaskNotificationsStats;
GO

CREATE VIEW dbo.vw_NpiTaskNotificationsStats AS
SELECT 
    CAST(NotificationDate AS DATE) AS NotificationDate,
    NotificationType,
    DeliveryStatus,
    COUNT(*) AS NotificationCount,
    COUNT(DISTINCT TaskProdottoID) AS UniqueTasksCount,
    COUNT(DISTINCT RecipientSoggettoID) AS UniqueRecipientsCount
FROM dbo.NpiTaskNotifications
GROUP BY CAST(NotificationDate AS DATE), NotificationType, DeliveryStatus;
GO

PRINT 'Vista vw_NpiTaskNotificationsStats creata con successo.';
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Setup completato!';
PRINT 'Tabella: NpiTaskNotifications';
PRINT 'Indici: IX_NpiTaskNotifications_Unique, IX_NpiTaskNotifications_Lookup';
PRINT 'Vista: vw_NpiTaskNotificationsStats';
PRINT '============================================================================';
GO
