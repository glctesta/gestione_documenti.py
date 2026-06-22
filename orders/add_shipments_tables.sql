-- ============================================================
-- Migration: Conferma Spedizioni v2 — testata spedizione + pallet
-- Schema: [Traceability_RS].[dyn]
-- Tabelle: Shipments (header), ShipmentPallets (righe pallet x ordine)
-- Idempotente (IF NOT EXISTS). Vedi DESIGN_shipment_confirmation_v2.md
-- ============================================================

-- ------------------------------------------------------------
-- 1) Testata spedizione: raggruppa piu' ordini/pallet in un evento
-- ------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[Shipments]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[Shipments] (
        ShipmentId          INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_Shipments PRIMARY KEY,
        ShipmentDate        DATE          NOT NULL,   -- data della spedizione (editabile)
        Status              NVARCHAR(20)  NOT NULL
            CONSTRAINT DF_dyn_Shipments_Status DEFAULT ('OPEN'), -- OPEN | CLOSED | CORRECTED
        CreatedByUser       NVARCHAR(100) NULL,
        CreatedAt           DATETIME      NOT NULL
            CONSTRAINT DF_dyn_Shipments_CreatedAt DEFAULT (GETDATE()),
        ClosedByUser        NVARCHAR(100) NULL,
        ClosedAt            DATETIME      NULL,
        LastModifiedByUser  NVARCHAR(100) NULL,
        LastModifiedAt      DATETIME      NULL,
        Notes               NVARCHAR(MAX) NULL,
        PdfPalletPath       NVARCHAR(400) NULL,   -- ultimo PDF "lista per pallet"
        PdfSummaryPath      NVARCHAR(400) NULL    -- ultimo PDF "riepilogo spedizione"
    );
    PRINT 'Creata tabella dyn.Shipments';

    CREATE NONCLUSTERED INDEX IX_dyn_Shipments_Date
        ON [Traceability_RS].[dyn].[Shipments] (ShipmentDate);
    CREATE NONCLUSTERED INDEX IX_dyn_Shipments_Status
        ON [Traceability_RS].[dyn].[Shipments] (Status);
    PRINT 'Creati indici su dyn.Shipments (Date, Status)';
END
ELSE
    PRINT 'Tabella dyn.Shipments gia'' presente';
GO

-- ------------------------------------------------------------
-- 2) Righe: quantita' confermata per (pallet x ordine di produzione)
--    Un ordine su piu' pallet -> piu' righe stesso ordine, PalletCode diversi.
--    Un pallet con piu' ordini -> piu' righe stesso PalletCode, ordini diversi.
-- ------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[ShipmentPallets]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[ShipmentPallets] (
        ShipmentPalletId            INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_ShipmentPallets PRIMARY KEY,
        ShipmentId                  INT           NOT NULL
            CONSTRAINT FK_dyn_ShipmentPallets_Shipment
            FOREIGN KEY REFERENCES [Traceability_RS].[dyn].[Shipments](ShipmentId),
        PalletCode                  NVARCHAR(50)  NOT NULL,  -- inserito dall'operatore
        DynamicProductionOrderID    INT           NOT NULL
            CONSTRAINT FK_dyn_ShipmentPallets_DPO
            FOREIGN KEY REFERENCES [Traceability_RS].[dyn].[DynamicProductionOrders](DynamicProductionOrderID),
        ConfirmedQty                INT           NOT NULL,
        ConfirmedByUser             NVARCHAR(100) NULL,
        ConfirmedAt                 DATETIME      NOT NULL
            CONSTRAINT DF_dyn_ShipmentPallets_ConfirmedAt DEFAULT (GETDATE()),
        -- snapshot per documenti/ristampe stabili
        ProductionOrderNumber       NVARCHAR(50)  NULL,
        SONumber                    NVARCHAR(50)  NULL,
        CustomerName                NVARCHAR(200) NULL,
        ItemCode                    NVARCHAR(50)  NULL,
        ItemName                    NVARCHAR(200) NULL,
        ShipTo                      NVARCHAR(200) NULL,
        -- unicita': un ordine non puo' comparire 2 volte sullo stesso pallet della
        -- stessa spedizione (lo si aggiorna sommando). Codici pallet uguali sono
        -- ammessi tra spedizioni/giorni diversi e tra ordini diversi nello stesso pallet.
        CONSTRAINT UQ_dyn_ShipmentPallets_Ship_Pallet_Order
            UNIQUE (ShipmentId, PalletCode, DynamicProductionOrderID)
    );
    PRINT 'Creata tabella dyn.ShipmentPallets';

    CREATE NONCLUSTERED INDEX IX_dyn_ShipmentPallets_Shipment
        ON [Traceability_RS].[dyn].[ShipmentPallets] (ShipmentId);
    CREATE NONCLUSTERED INDEX IX_dyn_ShipmentPallets_DPO
        ON [Traceability_RS].[dyn].[ShipmentPallets] (DynamicProductionOrderID);
    PRINT 'Creati indici su dyn.ShipmentPallets (ShipmentId, DynamicProductionOrderID)';
END
ELSE
    PRINT 'Tabella dyn.ShipmentPallets gia'' presente';
GO
