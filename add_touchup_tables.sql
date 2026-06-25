-- ============================================================
-- Touch-Up: segnalazione problemi schede + instradamento ai tecnici.
-- Tutte in [Traceability_RS].[dbo]. Idempotente. Vedi docs/TouchUp_Spec_v1.0.md
-- ============================================================

-- 1) Catalogo problemi (combo del menu 1)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpProblems]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpProblems] (
        TouchUpProblemId    INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpProblems PRIMARY KEY,
        ProblemCode         NVARCHAR(30)  NULL,
        ProblemDescription  NVARCHAR(200) NOT NULL,
        Severity            TINYINT       NULL,
        DateOut             DATETIME      NULL          -- attivo = NULL
    );
    PRINT 'Creata dbo.TouchUpProblems';
END
GO

-- 2) Instradamento problema -> reparto (CdcId/SubCdcId)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpProblemRouting]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpProblemRouting] (
        TouchUpRoutingId    INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpProblemRouting PRIMARY KEY,
        TouchUpProblemId    INT NOT NULL
            CONSTRAINT FK_TUPRouting_Problem FOREIGN KEY
            REFERENCES [Traceability_RS].[dbo].[TouchUpProblems](TouchUpProblemId),
        CdcId               INT NOT NULL,
        SubCdcId            INT NULL,
        DateOut             DATETIME NULL
    );
    CREATE NONCLUSTERED INDEX IX_TUPRouting_Problem
        ON [Traceability_RS].[dbo].[TouchUpProblemRouting](TouchUpProblemId);
    PRINT 'Creata dbo.TouchUpProblemRouting';
END
GO

-- 3) Testata segnalazione
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpReports]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpReports] (
        TouchUpReportId     INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpReports PRIMARY KEY,
        CreatedAt           DATETIME NOT NULL CONSTRAINT DF_TUReports_CreatedAt DEFAULT (GETDATE()),
        CreatedByUser       NVARCHAR(100) NULL,
        ComputerSrc         NVARCHAR(100) NULL,
        Status              NVARCHAR(20)  NOT NULL CONSTRAINT DF_TUReports_Status DEFAULT ('NEW'),
        EscalationLevel     INT NOT NULL CONSTRAINT DF_TUReports_Esc DEFAULT (0),
        FirstResponseAt     DATETIME NULL,
        ClosedAt            DATETIME NULL,
        ReopenCount         INT NOT NULL CONSTRAINT DF_TUReports_Reopen DEFAULT (0),
        EmailSentCount      INT NOT NULL CONSTRAINT DF_TUReports_Email DEFAULT (0),
        BossEscalated       BIT NOT NULL CONSTRAINT DF_TUReports_Boss DEFAULT (0),
        Notes               NVARCHAR(MAX) NULL
    );
    CREATE NONCLUSTERED INDEX IX_TUReports_Status ON [Traceability_RS].[dbo].[TouchUpReports](Status);
    PRINT 'Creata dbo.TouchUpReports';
END
GO

-- 4) Schede segnalate (1..N per report)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpReportLabels]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpReportLabels] (
        TouchUpReportLabelId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpReportLabels PRIMARY KEY,
        TouchUpReportId      INT NOT NULL
            CONSTRAINT FK_TURLabels_Report FOREIGN KEY
            REFERENCES [Traceability_RS].[dbo].[TouchUpReports](TouchUpReportId),
        IDLabelCode          INT NULL,
        LabelCod             NVARCHAR(50) NULL,
        IDOrder              INT NULL,
        OrderNumber          NVARCHAR(50) NULL,
        IDProduct            INT NULL,
        ProductCode          NVARCHAR(50) NULL
    );
    CREATE NONCLUSTERED INDEX IX_TURLabels_Report ON [Traceability_RS].[dbo].[TouchUpReportLabels](TouchUpReportId);
    CREATE NONCLUSTERED INDEX IX_TURLabels_Order  ON [Traceability_RS].[dbo].[TouchUpReportLabels](OrderNumber);
    PRINT 'Creata dbo.TouchUpReportLabels';
END
GO

-- 5) Problemi del report (1..N per report)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpReportProblems]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpReportProblems] (
        TouchUpReportProblemId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpReportProblems PRIMARY KEY,
        TouchUpReportId        INT NOT NULL
            CONSTRAINT FK_TURProblems_Report FOREIGN KEY
            REFERENCES [Traceability_RS].[dbo].[TouchUpReports](TouchUpReportId),
        TouchUpProblemId       INT NOT NULL
            CONSTRAINT FK_TURProblems_Problem FOREIGN KEY
            REFERENCES [Traceability_RS].[dbo].[TouchUpProblems](TouchUpProblemId)
    );
    CREATE NONCLUSTERED INDEX IX_TURProblems_Report ON [Traceability_RS].[dbo].[TouchUpReportProblems](TouchUpReportId);
    PRINT 'Creata dbo.TouchUpReportProblems';
END
GO

-- 6) Risposte del tecnico
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpResponses]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpResponses] (
        TouchUpResponseId  INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_TouchUpResponses PRIMARY KEY,
        TouchUpReportId    INT NOT NULL
            CONSTRAINT FK_TUResponses_Report FOREIGN KEY
            REFERENCES [Traceability_RS].[dbo].[TouchUpReports](TouchUpReportId),
        RespondedByUser    NVARCHAR(100) NULL,
        RespondedAt        DATETIME NOT NULL CONSTRAINT DF_TUResponses_At DEFAULT (GETDATE()),
        ReactionSeconds    INT NULL,
        ActionsTaken       NVARCHAR(MAX) NULL
    );
    CREATE NONCLUSTERED INDEX IX_TUResponses_Report ON [Traceability_RS].[dbo].[TouchUpResponses](TouchUpReportId);
    PRINT 'Creata dbo.TouchUpResponses';
END
GO

-- 7) Config globale (riga singola Id=1)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[TouchUpConfig]'))
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[TouchUpConfig] (
        Id INT NOT NULL CONSTRAINT PK_TouchUpConfig PRIMARY KEY,
        NoResponseEscalationMinutes INT NOT NULL CONSTRAINT DF_TUCfg_NoResp DEFAULT (30),
        DayRecurrenceThreshold      INT NOT NULL CONSTRAINT DF_TUCfg_DayThr DEFAULT (3)
    );
    INSERT INTO [Traceability_RS].[dbo].[TouchUpConfig] (Id, NoResponseEscalationMinutes, DayRecurrenceThreshold)
        VALUES (1, 30, 3);
    PRINT 'Creata dbo.TouchUpConfig (default 30 min / 3)';
END
GO

-- 8) Chiave email warning (se non presente)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].dbo.Settings WHERE atribute = 'Sys_email_TouchUp_warning')
    INSERT INTO [Traceability_RS].dbo.Settings (Atribute, Value, Name, LastCheck)
        VALUES ('Sys_email_TouchUp_warning', '', 'Destinatari warning Touch-Up', GETDATE());
GO
