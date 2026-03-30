-- =============================================
-- Script per aggiungere colonne soglie monitoraggio
-- a Employee.dbo.OverTimeRules e creare tabella log decisioni
-- =============================================

USE [Employee]
GO

-- =============================================
-- 1. Aggiungi colonne soglie a OverTimeRules (se non esistono)
-- =============================================
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.OverTimeRules') AND name = 'WeeklyLimitHours')
BEGIN
    ALTER TABLE dbo.OverTimeRules ADD WeeklyLimitHours DECIMAL(10,2) NOT NULL DEFAULT 48.0;
    PRINT N'Colonna WeeklyLimitHours aggiunta a OverTimeRules'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.OverTimeRules') AND name = 'WarningThresholdHours')
BEGIN
    ALTER TABLE dbo.OverTimeRules ADD WarningThresholdHours DECIMAL(10,2) NOT NULL DEFAULT 44.0;
    PRINT N'Colonna WarningThresholdHours aggiunta a OverTimeRules'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.OverTimeRules') AND name = 'CriticalThresholdHours')
BEGIN
    ALTER TABLE dbo.OverTimeRules ADD CriticalThresholdHours DECIMAL(10,2) NOT NULL DEFAULT 47.0;
    PRINT N'Colonna CriticalThresholdHours aggiunta a OverTimeRules'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.OverTimeRules') AND name = 'MonitoringMonths')
BEGIN
    ALTER TABLE dbo.OverTimeRules ADD MonitoringMonths INT NOT NULL DEFAULT 4;
    PRINT N'Colonna MonitoringMonths aggiunta a OverTimeRules'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.OverTimeRules') AND name = 'MaxDailyHours')
BEGIN
    ALTER TABLE dbo.OverTimeRules ADD MaxDailyHours DECIMAL(10,2) NOT NULL DEFAULT 12.0;
    PRINT N'Colonna MaxDailyHours aggiunta a OverTimeRules'
END
GO

-- =============================================
-- 2. Tabella log decisioni in ResetServices
-- =============================================
USE [ResetServices]
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[OvertimeDecisionLog]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[OvertimeDecisionLog](
        [DecisionId] [int] IDENTITY(1,1) NOT NULL,
        [EmployeeHireHistoryId] [int] NOT NULL,
        [DecisionDate] [date] NOT NULL,
        [DecisionType] [varchar](20) NOT NULL,          -- 'SUPPLEMENTARI','PREMI','SPLIT'
        [WeeklyAvg4Months] [decimal](10,2) NULL,
        [MonthlyHours] [decimal](10,2) NULL,
        [HasWeekendHours] [bit] DEFAULT 0,
        [Notes] [nvarchar](500) NULL,
        [DecidedBy] [nvarchar](100) NULL,
        [DateSys] [datetime] DEFAULT GETDATE(),
        CONSTRAINT [PK_OvertimeDecisionLog] PRIMARY KEY CLUSTERED ([DecisionId] ASC)
    ) ON [PRIMARY]
    
    PRINT N'Tabella OvertimeDecisionLog creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella OvertimeDecisionLog già esistente'
END
GO

PRINT N'Script completato con successo!'
