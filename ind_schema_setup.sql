-- ============================================================================
-- Schema ind - Materiali Indiretti (Redesign 4 tabelle)
-- Database: Traceability_RS
-- Data: 2026-03-18
-- ============================================================================

-- 1. Creazione schema ind
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ind')
BEGIN
    EXEC('CREATE SCHEMA ind');
    PRINT 'Schema [ind] creato.';
END
ELSE
    PRINT 'Schema [ind] esistente.';
GO

-- 2. ind.TipoMateriali - Tipi di materiale
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'TipoMateriali')
BEGIN
    CREATE TABLE ind.TipoMateriali (
        TipoMaterialeId   INT IDENTITY(1,1) PRIMARY KEY,
        Tipo               NVARCHAR(100) NOT NULL,
        IsFrazionabile     BIT DEFAULT 0,
        QtaConfezione      DECIMAL(18,2) DEFAULT 1
    );
    PRINT 'Tabella [ind].[TipoMateriali] creata.';

    -- Inserisci tipo default
    INSERT INTO ind.TipoMateriali (Tipo, IsFrazionabile, QtaConfezione)
    VALUES (N'Generico', 0, 1);
    PRINT 'Tipo default "Generico" inserito.';
END
ELSE
    PRINT 'Tabella [ind].[TipoMateriali] esistente.';
GO

-- 3. ind.Materiali - Anagrafica materiali (master)
-- Se esiste la vecchia versione senza IsActive, la ricreiamo
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'Materiali')
   AND NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'Materiali' AND COLUMN_NAME = 'IsActive')
BEGIN
    -- Rimuovi FK dipendenti se esistono
    IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiStock')
        DROP TABLE ind.MaterialiStock;
    IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiLogs')
        DROP TABLE ind.MaterialiLogs;
    DROP TABLE ind.Materiali;
    PRINT 'Vecchia tabella [ind].[Materiali] rimossa per upgrade.';
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'Materiali')
BEGIN
    CREATE TABLE ind.Materiali (
        MaterialeId          INT IDENTITY(1,1) PRIMARY KEY,
        CodiceMateriale      NVARCHAR(50) NOT NULL,
        DescrizioneMateriale NVARCHAR(255),
        TipoMaterialeId      INT NULL,
        DateCreated          DATETIME DEFAULT GETDATE(),
        IsActive             BIT DEFAULT 1,
        CONSTRAINT UQ_ind_Materiali_Codice UNIQUE (CodiceMateriale),
        CONSTRAINT FK_Materiali_TipoMateriali
            FOREIGN KEY (TipoMaterialeId) REFERENCES ind.TipoMateriali(TipoMaterialeId)
    );

    CREATE INDEX IX_ind_Materiali_Active
        ON ind.Materiali (IsActive) WHERE IsActive = 1;

    PRINT 'Tabella [ind].[Materiali] creata.';
END
ELSE
    PRINT 'Tabella [ind].[Materiali] esistente.';
GO

-- 4. ind.MaterialiStock - Giacenze storicizzate
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiStock')
BEGIN
    CREATE TABLE ind.MaterialiStock (
        StockId          INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId      INT NOT NULL,
        Qty              DECIMAL(18,4) DEFAULT 0,
        DateIn           DATETIME DEFAULT GETDATE(),
        DateOut          DATETIME NULL,
        CaricatoDa       NVARCHAR(100),
        CONSTRAINT FK_MaterialiStock_Materiali
            FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId)
    );

    CREATE INDEX IX_ind_MaterialiStock_Active
        ON ind.MaterialiStock (MaterialeId) WHERE DateOut IS NULL;

    PRINT 'Tabella [ind].[MaterialiStock] creata.';
END
ELSE
    PRINT 'Tabella [ind].[MaterialiStock] esistente.';
GO

-- 5. ind.MaterialiRichieste - Workflow richieste
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiRichieste')
BEGIN
    CREATE TABLE ind.MaterialiRichieste (
        RichiestaId        INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId        INT NOT NULL,
        QtaRichiesta       DECIMAL(18,4) NOT NULL,
        QtaStockAlMomento  DECIMAL(18,4),
        Stato              NVARCHAR(20) DEFAULT 'RICHIESTA',
        DataRichiesta      DATETIME DEFAULT GETDATE(),
        RichiestoDa        NVARCHAR(100),
        DataPreparazione   DATETIME NULL,
        PreparatoDa        NVARCHAR(100) NULL,
        DataPrelievo       DATETIME NULL,
        Note               NVARCHAR(500),
        CONSTRAINT FK_MaterialiRichieste_Materiali
            FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId),
        CONSTRAINT CK_MaterialiRichieste_Stato
            CHECK (Stato IN ('RICHIESTA','PREPARATA','PRONTA','PRELEVATA','ANNULLATA'))
    );

    CREATE INDEX IX_ind_MaterialiRichieste_Stato
        ON ind.MaterialiRichieste (Stato) WHERE Stato IN ('RICHIESTA','PREPARATA','PRONTA');

    PRINT 'Tabella [ind].[MaterialiRichieste] creata.';
END
ELSE
    PRINT 'Tabella [ind].[MaterialiRichieste] esistente.';
GO

PRINT 'Setup schema ind completato (4 tabelle).';
