-- ============================================================
-- NPI Budget Approval Requests Table
-- Tabella per il monitoring delle richieste di approvazione budget
-- ============================================================
USE Traceability_RS
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiBudgetApprovalRequests')
BEGIN
    CREATE TABLE dbo.NpiBudgetApprovalRequests (
        RequestId           INT IDENTITY(1,1) PRIMARY KEY,
        BudgetId            INT NOT NULL,
        ItemIds             NVARCHAR(MAX) NULL,         -- CSV degli ItemId coinvolti
        RequestType         NVARCHAR(50) NOT NULL,      -- 'Righe' | 'Budget'
        RequestedBy         NVARCHAR(200) NULL,
        RequestedDate       DATETIME NOT NULL DEFAULT GETDATE(),
        ComputerRichiedente NVARCHAR(100) NULL,
        Status              NVARCHAR(50) NOT NULL DEFAULT 'Pending',   -- 'Pending','Processed','Approved','Rejected'
        ProcessedBy         NVARCHAR(200) NULL,
        ProcessedDate       DATETIME NULL,
        RejectionNote       NVARCHAR(500) NULL,
        DataUltimaNotifica  DATETIME NULL,              -- Per ri-notifica monitor

        CONSTRAINT FK_ApprovalReq_Budget
            FOREIGN KEY (BudgetId) REFERENCES dbo.NpiBudgets(BudgetId)
    );

    PRINT '✅ Tabella NpiBudgetApprovalRequests creata'
END
ELSE
    PRINT '⚠️ Tabella NpiBudgetApprovalRequests già esistente'
GO
