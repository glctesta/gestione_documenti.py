-- ============================================================
-- NPI Checklist (Summary Sheet MD.RAQ.089) — Database Schema
-- Tabelle per la digitalizzazione della checklist NPI
-- ============================================================
USE Traceability_RS
GO

-- ============================================================
-- 1. NpiChecklistSessions — Intestazione / sessione principale
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistSessions')
BEGIN
    CREATE TABLE dbo.NpiChecklistSessions (
        SessionId           INT IDENTITY(1,1) PRIMARY KEY,
        ProgettoID          INT NOT NULL,
        OrderId             INT NULL,               -- Nr. KIT (da dbo.Orders)
        ProductCode         NVARCHAR(100) NULL,      -- PN (copia per stampa)
        OrderQuantity       INT NULL,                -- QTY
        CheckDate           DATETIME NULL,           -- Data del check
        Status              NVARCHAR(50) NOT NULL DEFAULT 'InLavorazione',  -- InLavorazione / Completato
        -- Fasi abilitate (opzionali per prodotto)
        HasSMT_TOP          BIT NOT NULL DEFAULT 1,
        HasSMT_BOTTOM       BIT NOT NULL DEFAULT 0,
        HasPTH              BIT NOT NULL DEFAULT 1,
        HasICT              BIT NOT NULL DEFAULT 1,
        HasFCT              BIT NOT NULL DEFAULT 1,
        HasCoating          BIT NOT NULL DEFAULT 0,
        -- Approvazione finale
        FinalApproval       BIT NULL,                -- Da / Nu (page 3 bottom)
        ResponsabileQualita NVARCHAR(255) NULL,
        ResponsabileProduzione NVARCHAR(255) NULL,
        ResponsabileIngegneria NVARCHAR(255) NULL,
        ApprovedBy          NVARCHAR(255) NULL,      -- Owner progetto NPI
        ApprovedDate        DATETIME NULL,
        -- Audit
        CreatedBy           NVARCHAR(255) NULL,
        CreatedDate         DATETIME NOT NULL DEFAULT GETDATE(),
        LastModifiedBy      NVARCHAR(255) NULL,
        LastModifiedDate    DATETIME NULL,
        DateOut             DATETIME NULL
    );
    PRINT '✅ Tabella NpiChecklistSessions creata'
END
ELSE PRINT '⚠️ NpiChecklistSessions già esistente'
GO

-- ============================================================
-- 2. NpiChecklistPrograms — Programmi per processo/fase
--    (SMT TOP/BOTTOM: Printing, SPI, Pick&Place, Reflow, AOI)
--    (PTH: Machine/Program)
--    (ICT, FCT: Line/Machine + Program)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistPrograms')
BEGIN
    CREATE TABLE dbo.NpiChecklistPrograms (
        ProgramId           INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        ProcessSection      NVARCHAR(50) NOT NULL,   -- SMT_TOP, SMT_BOTTOM, PTH, ICT, FCT
        ProcessStep         NVARCHAR(50) NOT NULL,   -- Printing, SPI, PickPlace, Reflow, AOI, Machine, DepanelingBeforeICT, etc.
        LineNr              NVARCHAR(50) NULL,        -- Line / Machine nr
        ProgramName         NVARCHAR(255) NULL,
        Result              NVARCHAR(20) NULL,        -- OK, Not OK
        ResponsabileName    NVARCHAR(255) NULL,
        ProcessDate         DATETIME NULL,
        Note                NVARCHAR(MAX) NULL,
        ProgramFile         VARBINARY(MAX) NULL,      -- Upload opzionale del programma
        ProgramFileName     NVARCHAR(255) NULL
    );
    PRINT '✅ Tabella NpiChecklistPrograms creata'
END
ELSE PRINT '⚠️ NpiChecklistPrograms già esistente'
GO

-- ============================================================
-- 3. NpiChecklistMaterials — Materiali / Attrezzature / Tools
--    (SMT: Solder paste, Glue, Stencil TOP/BOTTOM)
--    (PTH: Solder Bar, Solder Wire, Wave Frame, AOI Tool, Dep.Tool)
--    (ICT: Assembly tool, ICT Fixture, Mech.assembly, FCT fixture)
--    (Coating: Lăcuire, Coating tool)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistMaterials')
BEGIN
    CREATE TABLE dbo.NpiChecklistMaterials (
        MaterialId          INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        ProcessSection      NVARCHAR(50) NOT NULL,   -- SMT, PTH, ICT_FCT, COATING
        MaterialType        NVARCHAR(100) NOT NULL,   -- Solder paste, Glue, Stencil TOP, etc.
        CodePN              NVARCHAR(255) NULL,
        Note                NVARCHAR(MAX) NULL
    );
    PRINT '✅ Tabella NpiChecklistMaterials creata'
END
ELSE PRINT '⚠️ NpiChecklistMaterials già esistente'
GO

-- ============================================================
-- 4. NpiChecklistProductionData — Dati quantitativi di produzione
--    Per ogni sotto-processo: date, produced, inspected, pass, fail
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistProductionData')
BEGIN
    CREATE TABLE dbo.NpiChecklistProductionData (
        ProductionDataId    INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        ProcessName         NVARCHAR(100) NOT NULL,   -- SMT_AOI_TOP, XRAY_SMT, SMT_AOI_BOTTOM, PTH_IPQC, etc.
        ProcessDate         DATETIME NULL,
        ProducedQty         INT NULL,
        InspectedQty        INT NULL,
        PassQty             INT NULL,
        FailQty             INT NULL,
        Note                NVARCHAR(MAX) NULL,
        IsAutoPopulated     BIT NOT NULL DEFAULT 0    -- 1 se i dati vengono da SP traceability
    );
    PRINT '✅ Tabella NpiChecklistProductionData creata'
END
ELSE PRINT '⚠️ NpiChecklistProductionData già esistente'
GO

-- ============================================================
-- 5. NpiChecklistVerifications — Verifiche BOM e FQC
--    (Sezioni: BOM_SMT, BOM_PTH, FQC_SMT, FQC_PTH, FQC_COATING, IONIC_CONTAM)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistVerifications')
BEGIN
    CREATE TABLE dbo.NpiChecklistVerifications (
        VerificationId      INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        SectionName         NVARCHAR(100) NOT NULL,
        ConformStatus       NVARCHAR(20) NULL,        -- Conform / Neconform
        InspectedQty        INT NULL,
        InspectionResult    NVARCHAR(20) NULL,        -- OK / NC
        CQResponsible       NVARCHAR(255) NULL,
        VerificationDate    DATETIME NULL,
        Note                NVARCHAR(MAX) NULL
    );
    PRINT '✅ Tabella NpiChecklistVerifications creata'
END
ELSE PRINT '⚠️ NpiChecklistVerifications già esistente'
GO

-- ============================================================
-- 6. NpiChecklistPreformingChecks — Checklist PTH Preforming
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistPreformingChecks')
BEGIN
    CREATE TABLE dbo.NpiChecklistPreformingChecks (
        CheckId             INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        CheckItem           NVARCHAR(255) NOT NULL,   -- Preforming instructions, fixtures, tools, etc.
        Result              NVARCHAR(20) NULL,        -- OK / Not OK
        Note                NVARCHAR(MAX) NULL
    );
    PRINT '✅ Tabella NpiChecklistPreformingChecks creata'
END
ELSE PRINT '⚠️ NpiChecklistPreformingChecks già esistente'
GO

-- ============================================================
-- 7. NpiChecklistActions — Commenti / Azioni correttive (page 4)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistActions')
BEGIN
    CREATE TABLE dbo.NpiChecklistActions (
        ActionId            INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        Comment             NVARCHAR(MAX) NULL,
        Responsabil         NVARCHAR(255) NULL,
        DataChiusura        DATETIME NULL,
        Status              NVARCHAR(50) NULL         -- Aperto / Chiuso
    );
    PRINT '✅ Tabella NpiChecklistActions creata'
END
ELSE PRINT '⚠️ NpiChecklistActions già esistente'
GO

-- ============================================================
-- 8. NpiChecklistRework — Log Rework (page 4)
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NpiChecklistRework')
BEGIN
    CREATE TABLE dbo.NpiChecklistRework (
        ReworkId            INT IDENTITY(1,1) PRIMARY KEY,
        SessionId           INT NOT NULL FOREIGN KEY REFERENCES dbo.NpiChecklistSessions(SessionId),
        SerialNr            NVARCHAR(100) NULL,
        FailICT             NVARCHAR(MAX) NULL,
        FailFCT             NVARCHAR(MAX) NULL,
        Diagnoza            NVARCHAR(MAX) NULL,
        Referinta           NVARCHAR(255) NULL,
        ReworkResp          NVARCHAR(255) NULL
    );
    PRINT '✅ Tabella NpiChecklistRework creata'
END
ELSE PRINT '⚠️ NpiChecklistRework già esistente'
GO

PRINT '✅ Schema NPI Checklist completato — 8 tabelle create'
GO
