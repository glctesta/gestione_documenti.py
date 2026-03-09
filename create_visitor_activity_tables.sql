-- ============================================================
-- Tabelle e Settings per Rapporti Attività Ospiti
-- ============================================================

-- 1. Tabella VisitorContractInfo
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'VisitorContractInfo' AND TABLE_CATALOG = 'Employee')
BEGIN
    CREATE TABLE Employee.dbo.VisitorContractInfo (
        VisitorContractInfoId   INT IDENTITY(1,1) PRIMARY KEY,
        VisitorPlanToChargeID   INT NOT NULL,
        ContractNumber          NVARCHAR(50),
        ContractDate            DATE,
        ContractDescription     NVARCHAR(500),
        CONSTRAINT FK_ContractInfo_PlanToCharge
            FOREIGN KEY (VisitorPlanToChargeID)
            REFERENCES Employee.dbo.VisitorPlanToCharges(VisitorPlanToChargeID)
    );
    PRINT 'Tabella VisitorContractInfo creata.';
END
ELSE
    PRINT 'Tabella VisitorContractInfo già esistente.';

-- 2. Tabella VisitorActivityReports
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'VisitorActivityReports' AND TABLE_CATALOG = 'Employee')
BEGIN
    CREATE TABLE Employee.dbo.VisitorActivityReports (
        VisitorActivityReportId INT IDENTITY(1,1) PRIMARY KEY,
        VisitorId               INT NOT NULL,
        -- Documenti Word (VARBINARY)
        RequestLetterDoc        VARBINARY(MAX),
        AcceptanceLetterDoc     VARBINARY(MAX),
        ActivityReportDoc       VARBINARY(MAX),
        -- Date documenti
        RequestLetterDate       DATE,
        AcceptanceLetterDate    DATE,
        ActivityReportDate      DATE,
        -- Descrizione attività
        ActivityDescription     NVARCHAR(MAX),
        -- Email tracking
        EmailSentDate           DATETIME,
        EmailSentTo             NVARCHAR(500),
        -- Metadata
        CreatedAt               DATETIME DEFAULT GETDATE(),
        CreatedBy               NVARCHAR(100),
        CONSTRAINT FK_ActivityReport_Visitor
            FOREIGN KEY (VisitorId)
            REFERENCES Employee.dbo.Visitors(VisitorId)
    );
    PRINT 'Tabella VisitorActivityReports creata.';
END
ELSE
    PRINT 'Tabella VisitorActivityReports già esistente.';

-- 3. Settings per firmatari
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_richiede')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_richiede', '');

IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_richiede_titolo')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_richiede_titolo', '');

IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_richiede_email')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_richiede_email', '');

IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_invia')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_invia', '');

IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_invia_titolo')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_invia_titolo', '');

IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = 'chi_invia_email')
    INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES ('chi_invia_email', '');

PRINT 'Settings firmatari inseriti.';
