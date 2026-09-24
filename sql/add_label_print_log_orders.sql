-- Tabella di associazione tra log di stampa etichette e ordini.
-- Necessaria per la stampa generica con più ordini selezionati:
-- LabelPrintLog.OrderId registra solo il primo ordine, qui si tracciano tutti.

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'LabelPrintLogOrders'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.LabelPrintLogOrders (
        LabelPrintLogOrderId INT IDENTITY(1,1) PRIMARY KEY,
        LabelPrintLogId INT NOT NULL,
        OrderId INT NOT NULL,
        DateIn DATETIME NOT NULL DEFAULT GETDATE(),
        [User] NVARCHAR(255) NULL,
        CONSTRAINT FK_LabelPrintLogOrders_LabelPrintLog FOREIGN KEY (LabelPrintLogId)
            REFERENCES Traceability_RS.ind.LabelPrintLog(LabelPrintLogId)
    );
    CREATE INDEX IX_LabelPrintLogOrders_OrderId
        ON Traceability_RS.ind.LabelPrintLogOrders (OrderId);
    PRINT 'Creata tabella Traceability_RS.ind.LabelPrintLogOrders';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.LabelPrintLogOrders già esistente';
END
GO
