-- ============================================================
-- Plan Discrepancy Justification — Database Schema
-- Eseguire su Traceability_RS
-- ============================================================

-- 1. Tabella motivazioni predefinite
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='PlanRespect')
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[PlanRespect] (
        PlanResponseId SMALLINT IDENTITY(1,1) PRIMARY KEY,
        ResponseDescription NVARCHAR(200) NOT NULL,
        IsActive BIT DEFAULT 1,
        DateIn DATETIME DEFAULT GETDATE()
    );

    -- Valori iniziali
    INSERT INTO [Traceability_RS].[dbo].[PlanRespect] (ResponseDescription) VALUES
        (N'Eroare de planificare / Planning error'),
        (N'Lipsă material / Material shortage'),
        (N'Defecțiune mașină / Machine breakdown'),
        (N'Probleme calitate / Quality issues'),
        (N'Lipsă personal / Staff shortage'),
        (N'Modificare prioritate client / Customer priority change'),
        (N'Întârziere furnizor / Supplier delay'),
        (N'Ciclu de producție incorect / Incorrect production cycle'),
        (N'Reprogramare producție / Production rescheduling'),
        (N'Altele / Other');

    PRINT 'Tabella PlanRespect creata con 10 motivazioni iniziali';
END
GO

-- 2. Tabella risposte operatore (se non esiste già)
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='PlanAlertResponses')
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[PlanAlertResponses] (
        AlertResponseId INT IDENTITY(1,1) PRIMARY KEY,
        AlertId INT NOT NULL,
        PlanResponseId SMALLINT NOT NULL,
        Operator NVARCHAR(100),
        ResponseDate DATETIME DEFAULT GETDATE(),
        Notes NVARCHAR(500)
    );

    CREATE INDEX IX_PlanAlertResponses_AlertId ON [Traceability_RS].[dbo].[PlanAlertResponses] (AlertId);

    PRINT 'Tabella PlanAlertResponses creata';
END
ELSE
BEGIN
    -- Se esiste, verifica che abbia il campo PlanResponseId
    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME='PlanAlertResponses' AND COLUMN_NAME='PlanResponseId')
    BEGIN
        ALTER TABLE [Traceability_RS].[dbo].[PlanAlertResponses]
        ADD PlanResponseId SMALLINT NULL;
        PRINT 'Colonna PlanResponseId aggiunta a PlanAlertResponses';
    END

    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME='PlanAlertResponses' AND COLUMN_NAME='Operator')
    BEGIN
        ALTER TABLE [Traceability_RS].[dbo].[PlanAlertResponses]
        ADD Operator NVARCHAR(100) NULL;
        PRINT 'Colonna Operator aggiunta a PlanAlertResponses';
    END

    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME='PlanAlertResponses' AND COLUMN_NAME='Notes')
    BEGIN
        ALTER TABLE [Traceability_RS].[dbo].[PlanAlertResponses]
        ADD Notes NVARCHAR(500) NULL;
        PRINT 'Colonna Notes aggiunta a PlanAlertResponses';
    END
END
GO

-- 3. Tabella tracking escalation email
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='PlanAlertEscalations')
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[PlanAlertEscalations] (
        EscalationId INT IDENTITY(1,1) PRIMARY KEY,
        AlertId INT NOT NULL,
        EscalationLevel SMALLINT NOT NULL DEFAULT 1,
        SentDate DATETIME DEFAULT GETDATE(),
        Recipients NVARCHAR(500),
        PhaseName NVARCHAR(100)
    );

    CREATE INDEX IX_PlanAlertEscalations_AlertId ON [Traceability_RS].[dbo].[PlanAlertEscalations] (AlertId);

    PRINT 'Tabella PlanAlertEscalations creata';
END
GO

-- 4. Tabella tracking check settimanali
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='PlanAlertWeeklyChecks')
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[PlanAlertWeeklyChecks] (
        WeeklyCheckId INT IDENTITY(1,1) PRIMARY KEY,
        CheckDate DATETIME DEFAULT GETDATE(),
        ProductName NVARCHAR(200),
        PhaseName NVARCHAR(100),
        OccurrenceCount INT DEFAULT 0,
        SentDate DATETIME DEFAULT GETDATE()
    );

    PRINT 'Tabella PlanAlertWeeklyChecks creata';
END
GO

-- 5. Setting email management escalation
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'Sys_Alert_not_responce_plan')
BEGIN
    INSERT INTO traceability_rs.dbo.settings (atribute, [value])
    VALUES ('Sys_Alert_not_responce_plan', 'manager@vandewiele.com');

    PRINT 'Setting Sys_Alert_not_responce_plan creato — AGGIORNARE con email reali';
END
GO

-- 6. Setting feature flag per abilitare/disabilitare il modulo piano produzione
-- Valori ammessi: 'True' (attivo), 'False' (disabilitato), 'Test' (email a gianluca.testa@vandewiele.com)
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'Sys_enable_control_plan_check')
BEGIN
    INSERT INTO traceability_rs.dbo.settings (atribute, [value])
    VALUES ('Sys_enable_control_plan_check', 'Test');

    PRINT 'Setting Sys_enable_control_plan_check creato con valore Test';
END
GO

PRINT '=== Schema Plan Discrepancy completato ==='
