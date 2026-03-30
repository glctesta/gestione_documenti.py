-- ============================================================
-- NPI Budget Management System - Database Schema
-- ============================================================
USE Traceability_RS
GO

-- 1. Tabella categorie budget (lookup configurabile)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.NpiBudgetCategories') AND type = 'U')
BEGIN
    CREATE TABLE dbo.NpiBudgetCategories (
        CategoryId      INT IDENTITY(1,1) PRIMARY KEY,
        CategoryName     NVARCHAR(255) NOT NULL,
        DateOut          DATETIME NULL  -- Soft-delete
    )
    PRINT '✅ Tabella NpiBudgetCategories creata'

    -- Inserisci categorie di default
    INSERT INTO dbo.NpiBudgetCategories (CategoryName) VALUES ('Attrezzatura')
    INSERT INTO dbo.NpiBudgetCategories (CategoryName) VALUES ('Materiale')
    INSERT INTO dbo.NpiBudgetCategories (CategoryName) VALUES ('Servizio')
    INSERT INTO dbo.NpiBudgetCategories (CategoryName) VALUES ('Altro')
    PRINT '✅ Categorie di default inserite'
END
GO

-- 2. Tabella budget header (più budget per progetto, uno solo attivo)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.NpiBudgets') AND type = 'U')
BEGIN
    CREATE TABLE dbo.NpiBudgets (
        BudgetId          INT IDENTITY(1,1) PRIMARY KEY,
        ProgettoID        INT NOT NULL FOREIGN KEY REFERENCES dbo.ProgettiNPI(ProgettoID),
        BudgetName        NVARCHAR(255) NOT NULL,
        BudgetStatus      NVARCHAR(50) NOT NULL DEFAULT 'Bozza',        -- Bozza, InLavorazione, Terminato
        ApprovalStatus    NVARCHAR(50) NOT NULL DEFAULT 'DaApprovare',   -- DaApprovare, Approvato, Rifiutato
        IsActive          BIT NOT NULL DEFAULT 0,
        CreatedBy         NVARCHAR(255),
        CreatedDate       DATETIME NOT NULL DEFAULT GETDATE(),
        ApprovedBy        NVARCHAR(255) NULL,
        ApprovedDate      DATETIME NULL,
        RejectionNote     NVARCHAR(MAX) NULL,
        DateOut           DATETIME NULL
    )
    PRINT '✅ Tabella NpiBudgets creata'
END
GO

-- 3. Tabella righe budget
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.NpiBudgetItems') AND type = 'U')
BEGIN
    CREATE TABLE dbo.NpiBudgetItems (
        BudgetItemId      INT IDENTITY(1,1) PRIMARY KEY,
        BudgetId          INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiBudgets(BudgetId),
        ItemDescription   NVARCHAR(500) NOT NULL,
        CategoryId        INT NULL FOREIGN KEY REFERENCES dbo.NpiBudgetCategories(CategoryId),
        Quantity          DECIMAL(18,2) NOT NULL DEFAULT 1,
        UnitPrice         DECIMAL(18,2) NOT NULL DEFAULT 0,
        TotalPrice        AS (Quantity * UnitPrice) PERSISTED,
        ItemStatus        NVARCHAR(50) NOT NULL DEFAULT 'InLavorazione',  -- InLavorazione, Terminato
        ItemApproval      NVARCHAR(50) NOT NULL DEFAULT 'DaApprovare',   -- DaApprovare, Approvato, Rifiutato
        ApprovedBy        NVARCHAR(255) NULL,
        ApprovedDate      DATETIME NULL,
        RejectionNote     NVARCHAR(MAX) NULL,
        Note              NVARCHAR(MAX) NULL,
        DateOut           DATETIME NULL
    )
    PRINT '✅ Tabella NpiBudgetItems creata'
END
GO

PRINT '✅ Schema NPI Budget completato'
GO
