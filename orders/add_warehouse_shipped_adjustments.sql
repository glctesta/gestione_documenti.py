/*
    add_warehouse_shipped_adjustments.sql

    Ledger di allineamento transitorio per le spedizioni da magazzino
    (form _orders_reports_placeholder / DynamicShippingWindow).

    Durante la transizione, finche' non tutte le spedizioni passano dal sistema,
    l'operatore puo' dichiarare quanta parte di un ordine di produzione e' gia'
    stata spedita fuori dal sistema. Questa quantita' viene SOTTRATTA dalla
    disponibilita' a magazzino, cosi' la merce gia' spedita non risulta ancora
    da spedire.

    Append-only con audit: piu' correzioni sullo stesso ordine si sommano.
    Chiave logica = IDOrder (ordine di produzione, dbo.Orders). ProductCode e'
    solo snapshot per verifica/audit.

    Idempotente: rieseguibile.
*/

SET NOCOUNT ON;
GO

IF NOT EXISTS (
    SELECT 1 FROM Traceability_RS.sys.tables t
    INNER JOIN Traceability_RS.sys.schemas s ON s.schema_id = t.schema_id
    WHERE t.name = 'WarehouseShippedAdjustments' AND s.name = 'dyn'
)
BEGIN
    CREATE TABLE Traceability_RS.dyn.WarehouseShippedAdjustments (
        AdjustmentId    INT IDENTITY(1,1) NOT NULL,
        IDOrder         INT           NOT NULL,
        ProductCode     NVARCHAR(100) NULL,
        Qty             INT           NOT NULL,
        Note            NVARCHAR(400) NULL,
        AdjustedByUser  NVARCHAR(200) NOT NULL,
        AdjustedAt      DATETIME      NOT NULL
            CONSTRAINT DF_WSA_AdjustedAt DEFAULT (GETDATE()),
        CONSTRAINT PK_WarehouseShippedAdjustments PRIMARY KEY (AdjustmentId),
        -- La correzione rappresenta pezzi gia' spediti: deve essere positiva.
        CONSTRAINT CK_WSA_Qty CHECK (Qty > 0)
    );
    CREATE INDEX IX_WSA_IDOrder
        ON Traceability_RS.dyn.WarehouseShippedAdjustments (IDOrder);
    PRINT 'Creata Traceability_RS.dyn.WarehouseShippedAdjustments';
END
ELSE
    PRINT 'Traceability_RS.dyn.WarehouseShippedAdjustments gia'' presente';
GO
