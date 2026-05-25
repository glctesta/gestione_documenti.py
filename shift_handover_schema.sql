-- ============================================================
-- shift_handover_schema.sql
-- Crea le tabelle per il modulo Cambio Turno nel DB Employee
-- Eseguire su: Employee
-- ============================================================

USE [Employee];
GO

-- ── Tabella principale: report consegna turno ─────────────────────────────
IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.ShiftHandoverReports') AND type = 'U'
)
BEGIN
    CREATE TABLE [dbo].[ShiftHandoverReports] (
        HandoverReportId    INT           IDENTITY(1,1) PRIMARY KEY,
        ShiftDate           DATE          NOT NULL,
        -- 1 = fine 15:30  |  2 = fine 23:30  |  3 = fine 07:30 (opzionale)
        ShiftNumber         TINYINT       NOT NULL CHECK (ShiftNumber IN (1,2,3)),
        Department          NVARCHAR(100) NOT NULL,
        SubCdcId            INT           NULL
            REFERENCES [dbo].[CdcSub](SubCdcId),
        CompiledBy          NVARCHAR(100) NOT NULL,
        CompiledByEmpId     INT           NULL
            REFERENCES [dbo].[EmployeeHireHistory](EmployeeHireHistoryId),
        ComputerName        NVARCHAR(100) NOT NULL,
        CompiledAt          DATETIME      NOT NULL DEFAULT GETDATE(),

        -- Sezioni del report
        ProductionStatus    NVARCHAR(500) NULL,   -- Stare productie
        LinesStatus         NVARCHAR(MAX) NULL,   -- Linii / echipamente
        QtyPlanned          DECIMAL(10,2) NULL,
        QtyProduced         DECIMAL(10,2) NULL,
        QualityIssues       NVARCHAR(MAX) NULL,   -- Probleme calitate + actiuni
        MaterialStatus      NVARCHAR(500) NULL,   -- Materiale disponibile/lipsa
        OpenIssues          NVARCHAR(MAX) NULL,   -- Probleme deschise
        FreeNotes           NVARCHAR(MAX) NULL,   -- Note libere

        IsConfirmed         BIT           NOT NULL DEFAULT 0,
        ConfirmedBy         NVARCHAR(100) NULL,
        ConfirmedAt         DATETIME      NULL,
        ConfirmedByEmpId    INT           NULL
            REFERENCES [dbo].[EmployeeHireHistory](EmployeeHireHistoryId)
    );
    PRINT 'Tabella ShiftHandoverReports creata.';
END
ELSE
    PRINT 'Tabella ShiftHandoverReports gia'' esistente — skip.';
GO

-- ── Tabella conferme (una per ogni accesso capo entrante) ─────────────────
IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.ShiftHandoverConfirmations') AND type = 'U'
)
BEGIN
    CREATE TABLE [dbo].[ShiftHandoverConfirmations] (
        ConfirmationId      INT           IDENTITY(1,1) PRIMARY KEY,
        HandoverReportId    INT           NOT NULL
            REFERENCES [dbo].[ShiftHandoverReports](HandoverReportId),
        ConfirmedBy         NVARCHAR(100) NOT NULL,
        ConfirmedByEmpId    INT           NULL
            REFERENCES [dbo].[EmployeeHireHistory](EmployeeHireHistoryId),
        ConfirmedAt         DATETIME      NOT NULL DEFAULT GETDATE(),
        ComputerName        NVARCHAR(100) NOT NULL,
        Notes               NVARCHAR(500) NULL
    );
    PRINT 'Tabella ShiftHandoverConfirmations creata.';
END
ELSE
    PRINT 'Tabella ShiftHandoverConfirmations gia'' esistente — skip.';
GO

-- ── Indici utili per le query frequenti ───────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_SHR_Date_Dept_Shift' AND object_id = OBJECT_ID('dbo.ShiftHandoverReports'))
    CREATE INDEX IX_SHR_Date_Dept_Shift
        ON dbo.ShiftHandoverReports (ShiftDate, Department, ShiftNumber);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_SHR_IsConfirmed' AND object_id = OBJECT_ID('dbo.ShiftHandoverReports'))
    CREATE INDEX IX_SHR_IsConfirmed
        ON dbo.ShiftHandoverReports (IsConfirmed, ShiftDate)
        INCLUDE (Department, ShiftNumber, CompiledBy, OpenIssues);
GO

-- ── Riga settings per email alert (inserisci l'indirizzo se non esiste) ───
USE [Traceability_RS];
GO
IF NOT EXISTS (SELECT 1 FROM dbo.settings WHERE atribute = 'sys_email_Allert_Shift')
    INSERT INTO dbo.settings (atribute, [value])
    VALUES ('sys_email_Allert_Shift', '');  -- da popolare con email responsabili
GO

PRINT 'Setup Cambio Turno completato.';
GO
