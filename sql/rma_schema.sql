-- ============================================================================
-- RMA Knowledge Base — Schema Tabelle
-- Database: Traceability_RS
-- Creato: 2026-03-27
-- ============================================================================

USE [Traceability_RS];
GO

-- ============================================================================
-- 1. Tabella Lookup: Tipi di Guasto
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'RmaFaultTypes')
BEGIN
    CREATE TABLE [dbo].[RmaFaultTypes] (
        [RmaFaultTypeId]    INT IDENTITY(1,1)  NOT NULL,
        [Code]              NVARCHAR(20)       NULL,       -- es. CC03, NDF, S01...
        [Description]       NVARCHAR(200)      NOT NULL,   -- es. 'Problema di componente'
        [DateOut]           DATE               NULL,       -- soft-delete
        CONSTRAINT [PK_RmaFaultTypes] PRIMARY KEY CLUSTERED ([RmaFaultTypeId])
    );
    PRINT 'Tabella RmaFaultTypes creata.';
END
GO

-- ============================================================================
-- 2. Tabella Lookup: Dettagli Tipo Guasto (sotto-categorie)
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'RmaFaultDetails')
BEGIN
    CREATE TABLE [dbo].[RmaFaultDetails] (
        [RmaFaultDetailId]  INT IDENTITY(1,1)  NOT NULL,
        [RmaFaultTypeId]    INT                NOT NULL,   -- FK verso RmaFaultTypes
        [Code]              NVARCHAR(20)       NULL,       -- es. FCMP03, FCMP01...
        [Description]       NVARCHAR(200)      NOT NULL,   -- es. 'componente difettoso'
        [DateOut]           DATE               NULL,       -- soft-delete
        CONSTRAINT [PK_RmaFaultDetails] PRIMARY KEY CLUSTERED ([RmaFaultDetailId]),
        CONSTRAINT [FK_RmaFaultDetails_Type] FOREIGN KEY ([RmaFaultTypeId])
            REFERENCES [dbo].[RmaFaultTypes] ([RmaFaultTypeId])
    );
    PRINT 'Tabella RmaFaultDetails creata.';
END
GO

-- ============================================================================
-- 3. Tabella Lookup: Siti di Produzione
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'RmaProductionSites')
BEGIN
    CREATE TABLE [dbo].[RmaProductionSites] (
        [RmaProductionSiteId] INT IDENTITY(1,1) NOT NULL,
        [Name]                 NVARCHAR(100)     NOT NULL,  -- es. 'Eutron', 'Vandewiele Romania'
        [DateOut]              DATE              NULL,       -- soft-delete
        CONSTRAINT [PK_RmaProductionSites] PRIMARY KEY CLUSTERED ([RmaProductionSiteId])
    );
    PRINT 'Tabella RmaProductionSites creata.';
END
GO

-- ============================================================================
-- 4. Tabella Principale: Record RMA
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'RmaRecords')
BEGIN
    CREATE TABLE [dbo].[RmaRecords] (
        [RmaRecordId]          INT IDENTITY(1,1)  NOT NULL,
        -- Identificativi scheda
        [SerialNumber]         NVARCHAR(50)       NULL,
        [PartCode]             NVARCHAR(50)       NULL,      -- codice parte PFZA/PFEX...
        [CustomerPartCode]     NVARCHAR(50)       NULL,      -- codice parte cliente
        [PartDescription]      NVARCHAR(300)      NULL,      -- descrizione completa PCBA
        [RmaNumber]            NVARCHAR(50)       NULL,      -- numero ordine RMA
        -- Cliente
        [CustomerId]           INT                NULL,      -- codice cliente numerico
        [CustomerName]         NVARCHAR(200)      NULL,      -- denominazione
        -- Guasto
        [FaultDescription]     NVARCHAR(MAX)      NULL,      -- descrizione guasto
        [FaultCauseCode]       NVARCHAR(10)       NULL,      -- FC01..FC04
        [FaultCause]           NVARCHAR(200)      NULL,      -- testo causa
        [RmaFaultTypeId]       INT                NULL,      -- FK tipo guasto
        [RmaFaultDetailId]     INT                NULL,      -- FK dettaglio guasto
        [Reference]            NVARCHAR(100)      NULL,      -- componente es. J8, U33, DISPLAY
        [Assembly]             NVARCHAR(100)      NULL,      -- codice assembly
        [FaultNotes]           NVARCHAR(MAX)      NULL,      -- NOTE GUASTO = SOLUZIONE
        -- Azione correttiva (campo aggiuntivo per inserimento manuale)
        [CorrectiveAction]     NVARCHAR(MAX)      NULL,      -- azione correttiva
        -- Produzione
        [ProductionWeek]       NVARCHAR(10)       NULL,      -- YYYY/WW
        [RmaProductionSiteId]  INT                NULL,      -- FK sito produzione
        [ProcessResponsible]   NVARCHAR(100)      NULL,      -- resp. processo
        -- Garanzia e costi
        [WarrantyType]         NVARCHAR(20)       NULL,      -- Warranty YES/NO/Scrap
        [Origin]               NVARCHAR(50)       NULL,      -- Supply line/Front line
        [RepairTimeMinutes]    INT                NULL,      -- tempo riparazione
        [Cost]                 FLOAT              NULL,      -- costo riparazione
        [AlreadyRepaired]      BIT                NULL,      -- già riparata
        -- Operatore e test
        [Operator]             NVARCHAR(100)      NULL,      -- operatore
        [TestType]             NVARCHAR(50)       NULL,      -- Visual/ICT/FCT
        -- Date
        [OrderDate]            DATETIME           NULL,      -- data ordine
        [DeliveryDate]         DATETIME           NULL,      -- data consegna
        [CloseDate]            DATETIME           NULL,      -- data chiusura
        [TestDate]             DATETIME           NULL,      -- data test
        -- Allegati (campi aggiuntivi per inserimento manuale)
        [PhotoPath]            NVARCHAR(500)      NULL,      -- percorso foto difetto
        [DocumentLinks]        NVARCHAR(MAX)      NULL,      -- link documenti (JSON/testo)
        -- Tracciabilità interna
        [IDLabelCode]          INT                NULL,      -- FK verso LabelCodes (se TI)
        [IDOrder]              INT                NULL,      -- FK verso Orders (se TI)
        [ProductCode]          NVARCHAR(50)       NULL,      -- codice prodotto tracciabilità
        -- Metadati
        [InsertedBy]           NVARCHAR(100)      NULL,      -- utente che ha inserito
        [InsertedAt]           DATETIME           NULL DEFAULT GETDATE(),
        [Source]               NVARCHAR(20)       NULL DEFAULT 'MANUAL', -- IMPORT/MANUAL
        [DateOut]              DATE               NULL,       -- soft-delete

        CONSTRAINT [PK_RmaRecords] PRIMARY KEY CLUSTERED ([RmaRecordId]),
        CONSTRAINT [FK_RmaRecords_FaultType] FOREIGN KEY ([RmaFaultTypeId])
            REFERENCES [dbo].[RmaFaultTypes] ([RmaFaultTypeId]),
        CONSTRAINT [FK_RmaRecords_FaultDetail] FOREIGN KEY ([RmaFaultDetailId])
            REFERENCES [dbo].[RmaFaultDetails] ([RmaFaultDetailId]),
        CONSTRAINT [FK_RmaRecords_Site] FOREIGN KEY ([RmaProductionSiteId])
            REFERENCES [dbo].[RmaProductionSites] ([RmaProductionSiteId])
    );
    PRINT 'Tabella RmaRecords creata.';
END
GO

-- ============================================================================
-- 5. Indici per query performanti
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_SerialNumber')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_SerialNumber]
    ON [dbo].[RmaRecords] ([SerialNumber]);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_PartCode')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_PartCode]
    ON [dbo].[RmaRecords] ([PartCode]);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_CustomerName')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_CustomerName]
    ON [dbo].[RmaRecords] ([CustomerName]);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_FaultType')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_FaultType]
    ON [dbo].[RmaRecords] ([RmaFaultTypeId]);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_OrderDate')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_OrderDate]
    ON [dbo].[RmaRecords] ([OrderDate]);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_RmaRecords_Reference')
    CREATE NONCLUSTERED INDEX [IX_RmaRecords_Reference]
    ON [dbo].[RmaRecords] ([Reference]);
GO

-- ============================================================================
-- 6. Seed Lookup: Tipi Guasto (dai dati Excel)
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[RmaFaultTypes])
BEGIN
    INSERT INTO [dbo].[RmaFaultTypes] ([Code], [Description]) VALUES
        ('CC03',  N'Problema di componente'),
        ('DSL01', N'Difetto di saldatura'),
        ('AGG',   N'Aggiornamento'),
        ('SCRAP', N'Rottamato'),
        ('DAM01', N'Difetto di assemblaggio'),
        ('NDF',   N'No Defect Found'),
        ('ESD',   N'Danno ESD'),
        ('DES',   N'Difetto di design/progetto'),
        ('CC01',  N'Contaminazione'),
        ('ALT',   N'Altro');
    PRINT 'Lookup RmaFaultTypes popolata.';
END
GO

-- ============================================================================
-- 7. Seed Lookup: Dettagli Guasto (collegati ai tipi)
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[RmaFaultDetails])
BEGIN
    -- Problema di componente (CC03)
    DECLARE @CC03 INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'CC03');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@CC03, 'FCMP03', N'componente difettoso'),
        (@CC03, 'FCMP01', N'componente danneggiato'),
        (@CC03, 'FCMP04', N'componente errato'),
        (@CC03, 'FCMP02', N'componente bruciato'),
        (@CC03, 'FCMP05', N'componente mancante'),
        (@CC03, 'FCMP06', N'componente fuori specifica');

    -- Difetto di saldatura (DSL01)
    DECLARE @DSL01 INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'DSL01');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@DSL01, 'FSLD01', N'saldatura/risalita mancante'),
        (@DSL01, 'FSLD02', N'corto circuito'),
        (@DSL01, 'FSLD03', N'saldatura fredda');

    -- Aggiornamento (AGG)
    DECLARE @AGG INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'AGG');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@AGG, 'FAGG01', N'aggiornamento hardware'),
        (@AGG, 'FAGG02', N'aggiornamento software');

    -- Difetto di assemblaggio (DAM01)
    DECLARE @DAM INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'DAM01');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@DAM, 'FASM01', N'assemblaggio errato'),
        (@DAM, 'FASM02', N'assemblaggio mancante'),
        (@DAM, 'FASM03', N'inversione componente');

    -- NDF
    DECLARE @NDF INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'NDF');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@NDF, 'FNDF01', N'No Defect Found');

    -- Danno ESD
    DECLARE @ESD INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'ESD');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@ESD, 'FESD01', N'danno da scarica elettrostatica');

    -- Design
    DECLARE @DES INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'DES');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@DES, 'FDES01', N'errore di progetto');

    -- Contaminazione
    DECLARE @CC01 INT = (SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = 'CC01');
    INSERT INTO [dbo].[RmaFaultDetails] ([RmaFaultTypeId], [Code], [Description]) VALUES
        (@CC01, 'FCNT01', N'contaminazione da liquidi'),
        (@CC01, 'FCNT02', N'contaminazione da polvere');

    PRINT 'Lookup RmaFaultDetails popolata.';
END
GO

-- ============================================================================
-- 8. Seed Lookup: Siti di Produzione
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM [dbo].[RmaProductionSites])
BEGIN
    INSERT INTO [dbo].[RmaProductionSites] ([Name]) VALUES
        (N'Eutron'),
        (N'Vandewiele Romania'),
        (N'Meba'),
        (N'Megatronic'),
        (N'Kunshan');
    PRINT 'Lookup RmaProductionSites popolata.';
END
GO

PRINT '== RMA Knowledge Base schema completato con successo ==';
GO
