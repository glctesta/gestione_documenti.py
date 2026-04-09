-- ============================================================
-- FAI Compliance Enforcement - Schema
-- Tabella per tracking eventi di enforcement e escalation
-- ============================================================

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'FaiEnforcementLog' AND schema_id = SCHEMA_ID('fai'))
BEGIN
    CREATE TABLE [Traceability_RS].[fai].[FaiEnforcementLog] (
        EnforcementLogId      INT IDENTITY(1,1) PRIMARY KEY,
        EventType             NVARCHAR(30) NOT NULL,       -- 'SHIFT_CHECK' | 'NEW_ORDER'
        EmployeeHireHistoryId INT NULL,
        EmployeeName          NVARCHAR(200) NULL,
        OrderId               INT NULL,
        OrderNumber           NVARCHAR(50) NULL,
        ShiftTime             NVARCHAR(10) NULL,            -- '07:30' | '15:30' | '23:30'
        EscalationLevel       INT NOT NULL DEFAULT 0,
        FaiCompleted          BIT NOT NULL DEFAULT 0,
        FaiCompletedTime      DATETIME NULL,
        ReferatGenerated      BIT NOT NULL DEFAULT 0,
        ReferatRegistroId     INT NULL,
        NotificationSent      BIT NOT NULL DEFAULT 0,
        NotificationTime      DATETIME NULL,
        CheckDate             DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
        DateIn                DATETIME NOT NULL DEFAULT GETDATE(),
        DateOut               DATETIME NULL,
        Notes                 NVARCHAR(MAX) NULL
    );

    CREATE INDEX IX_FaiEnforcementLog_Date 
        ON [Traceability_RS].[fai].[FaiEnforcementLog] (CheckDate, EventType, EscalationLevel);
    
    CREATE INDEX IX_FaiEnforcementLog_Employee 
        ON [Traceability_RS].[fai].[FaiEnforcementLog] (EmployeeHireHistoryId, CheckDate);
    
    CREATE INDEX IX_FaiEnforcementLog_Order 
        ON [Traceability_RS].[fai].[FaiEnforcementLog] (OrderId, CheckDate);

    PRINT 'Tabella fai.FaiEnforcementLog creata con successo';
END
ELSE
BEGIN
    PRINT 'Tabella fai.FaiEnforcementLog esiste già';
END
