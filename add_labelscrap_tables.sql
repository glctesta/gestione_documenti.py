/*
    add_labelscrap_tables.sql

    Scarti etichette (Operazioni > Materiali > Dichiarazione scarti / Report).

    - dbo.LabelScrapReasons : motivi di scarto etichette (dedicati, separati da
      ScrapResons che riguarda i difetti schede). Motivi in rumeno.
    - dbo.labelscrap        : una riga per etichetta scartata (per scansione).
    - settings 'sys_email_labelScrap' : destinatari email fine turno / settimanale.

    Idempotente: rieseguibile.
*/

SET NOCOUNT ON;
GO

-- ── Motivi di scarto etichette ───────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM traceability_rs.sys.tables t
               INNER JOIN traceability_rs.sys.schemas s ON s.schema_id = t.schema_id
               WHERE t.name = 'LabelScrapReasons' AND s.name = 'dbo')
BEGIN
    CREATE TABLE traceability_rs.dbo.LabelScrapReasons (
        LabelScrapReasonId INT IDENTITY(1,1) NOT NULL,
        Reason             NVARCHAR(150) NOT NULL,
        IsActive           BIT NOT NULL CONSTRAINT DF_LSR_IsActive DEFAULT (1),
        CONSTRAINT PK_LabelScrapReasons PRIMARY KEY (LabelScrapReasonId)
    );
    PRINT 'Creata traceability_rs.dbo.LabelScrapReasons';
END
ELSE
    PRINT 'traceability_rs.dbo.LabelScrapReasons gia'' presente';
GO

-- Motivi di default (in rumeno) — inseriti solo se la tabella e' vuota
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.LabelScrapReasons)
BEGIN
    INSERT INTO traceability_rs.dbo.LabelScrapReasons (Reason)
    VALUES
        (N'Blocaj imprimantă'),
        (N'Date greșite'),
        (N'Etichetă deteriorată'),
        (N'Cod ilizibil'),
        (N'Reimprimare'),
        (N'Ribon/toner epuizat'),
        (N'Aliniere greșită'),
        (N'Altele');
    PRINT 'Inseriti motivi di default (rumeno)';
END
GO

-- ── Scarti etichette ─────────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM traceability_rs.sys.tables t
               INNER JOIN traceability_rs.sys.schemas s ON s.schema_id = t.schema_id
               WHERE t.name = 'labelscrap' AND s.name = 'dbo')
BEGIN
    CREATE TABLE traceability_rs.dbo.labelscrap (
        LabelScrapId       INT IDENTITY(1,1) NOT NULL,
        LabelCode          NVARCHAR(150) NOT NULL,
        IDLabelCode        INT NULL,                 -- FK LabelCodes se noto
        ScrapDate          DATE NOT NULL,
        LabelScrapReasonId INT NOT NULL,
        Category           NVARCHAR(20) NOT NULL,    -- 'Production' / 'Print'
        Operator           NVARCHAR(200) NOT NULL,
        Shift              NVARCHAR(10) NULL,         -- 07:30 / 15:30 / 23:30
        Hostname           NVARCHAR(100) NULL,
        Printed            DATETIME NULL,             -- NULL = riepilogo non stampato
        DateIn             DATETIME NOT NULL CONSTRAINT DF_labelscrap_DateIn DEFAULT (GETDATE()),
        CONSTRAINT PK_labelscrap PRIMARY KEY (LabelScrapId),
        CONSTRAINT FK_labelscrap_Reason FOREIGN KEY (LabelScrapReasonId)
            REFERENCES traceability_rs.dbo.LabelScrapReasons (LabelScrapReasonId),
        CONSTRAINT CK_labelscrap_Category CHECK (Category IN ('Production', 'Print'))
    );
    CREATE INDEX IX_labelscrap_ScrapDate ON traceability_rs.dbo.labelscrap (ScrapDate);
    CREATE INDEX IX_labelscrap_Operator ON traceability_rs.dbo.labelscrap (Operator);
    CREATE INDEX IX_labelscrap_Printed ON traceability_rs.dbo.labelscrap (Printed);
    PRINT 'Creata traceability_rs.dbo.labelscrap';
END
ELSE
    PRINT 'traceability_rs.dbo.labelscrap gia'' presente';
GO

-- ── Setting email destinatari ────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'sys_email_labelScrap')
BEGIN
    INSERT INTO traceability_rs.dbo.settings (atribute, [value])
    VALUES ('sys_email_labelScrap', '');
    PRINT 'Creata setting sys_email_labelScrap (vuota, da popolare)';
END
GO

SELECT LabelScrapReasonId, Reason, IsActive FROM traceability_rs.dbo.LabelScrapReasons ORDER BY LabelScrapReasonId;
GO
