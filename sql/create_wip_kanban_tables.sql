-- ============================================================================
-- Kanban produzione WIP/REPAIR — tabelle dedicate
-- Server web dedicato su porta 6500 (package wip_kanban)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Locazioni: pallet (Area + PalletNumber) con 16 posizioni (colonne A-D,
--    livelli 1-4). PositionCode es. 'WP1A1' ... 'WP1D4', 'RP1A1' ...
-- ----------------------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'WipKanbanLocations'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.WipKanbanLocations (
        LocationId    INT IDENTITY(1,1) PRIMARY KEY,
        Area          NVARCHAR(10)  NOT NULL,   -- 'WIP' | 'REPAIR'
        PalletNumber  INT           NOT NULL,   -- sequenza per area (WP1, WP2... / RP1, RP2...)
        PositionCode  NVARCHAR(10)  NOT NULL,   -- 'WP1A1'
        DateIn        DATETIME      NOT NULL DEFAULT GETDATE(),
        [User]        NVARCHAR(255) NULL,
        CONSTRAINT UQ_WipKanban_PositionCode UNIQUE (PositionCode)
    );
    PRINT 'Creata tabella Traceability_RS.ind.WipKanbanLocations';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.WipKanbanLocations già esistente';
END
GO

-- ----------------------------------------------------------------------------
-- 2. Schede caricate/prelevate. Prelievo = DateOut valorizzato (storico
--    conservato). Dati ordine/prodotto denormalizzati per semplicità di
--    ricerca.
-- ----------------------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'WipKanbanBoards'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.WipKanbanBoards (
        BoardKanbanId INT IDENTITY(1,1) PRIMARY KEY,
        LocationId    INT           NOT NULL,
        IDBoard       INT           NOT NULL,   -- da LabelCodes -> Boards
        LabelCode     NVARCHAR(100) NOT NULL,
        IDOrder       INT           NULL,
        OrderNumber   NVARCHAR(50)  NULL,
        ProductCode   NVARCHAR(100) NULL,
        DateIn        DATETIME      NOT NULL DEFAULT GETDATE(),
        [User]        NVARCHAR(255) NULL,
        DateOut       DATETIME      NULL,
        OutUser       NVARCHAR(255) NULL,
        CONSTRAINT FK_WipKanbanBoards_Locations FOREIGN KEY (LocationId)
            REFERENCES Traceability_RS.ind.WipKanbanLocations(LocationId)
    );
    CREATE INDEX IX_WKB_Location ON Traceability_RS.ind.WipKanbanBoards (LocationId, DateOut);
    CREATE INDEX IX_WKB_Order    ON Traceability_RS.ind.WipKanbanBoards (OrderNumber) WHERE DateOut IS NULL;
    CREATE INDEX IX_WKB_Product  ON Traceability_RS.ind.WipKanbanBoards (ProductCode) WHERE DateOut IS NULL;
    PRINT 'Creata tabella Traceability_RS.ind.WipKanbanBoards';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.WipKanbanBoards già esistente';
END
GO

-- ----------------------------------------------------------------------------
-- 3. Audit: chi / quando / cosa (IN = carica scheda, OUT = preleva,
--    CREATE = creazione locazione)
-- ----------------------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'WipKanbanAudit'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.WipKanbanAudit (
        AuditId      INT IDENTITY(1,1) PRIMARY KEY,
        Action       NVARCHAR(10)  NOT NULL,    -- 'IN' | 'OUT' | 'CREATE'
        LabelCode    NVARCHAR(100) NULL,
        PositionCode NVARCHAR(10)  NULL,
        OrderNumber  NVARCHAR(50)  NULL,
        ProductCode  NVARCHAR(100) NULL,
        [User]       NVARCHAR(255) NULL,
        DateIn       DATETIME      NOT NULL DEFAULT GETDATE()
    );
    CREATE INDEX IX_WKA_Date ON Traceability_RS.ind.WipKanbanAudit (DateIn);
    PRINT 'Creata tabella Traceability_RS.ind.WipKanbanAudit';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.WipKanbanAudit già esistente';
END
GO

-- ----------------------------------------------------------------------------
-- 4. Sessioni web (token monouso), isolate dal server etichette
-- ----------------------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'WipKanbanWebSessions'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.WipKanbanWebSessions (
        Token      NVARCHAR(64)  PRIMARY KEY,
        UserId     INT           NULL,
        UserName   NVARCHAR(255) NULL,
        Permission NVARCHAR(100) NULL,
        Page       NVARCHAR(50)  NULL,
        IssuedAt   DATETIME      NOT NULL DEFAULT GETDATE(),
        ExpiresAt  DATETIME      NOT NULL,
        UsedAt     DATETIME      NULL
    );
    PRINT 'Creata tabella Traceability_RS.ind.WipKanbanWebSessions';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.WipKanbanWebSessions già esistente';
END
GO

PRINT 'Schema Kanban produzione WIP/REPAIR aggiornato.';
