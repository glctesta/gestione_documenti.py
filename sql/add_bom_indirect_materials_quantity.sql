-- Aggiunge la quantità di etichette per pezzo nella BOM indiretta
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.BomIndirectMaterials')
      AND name = 'QuantityPerPiece'
)
    ALTER TABLE [Traceability_RS].[ind].[BomIndirectMaterials]
        ADD QuantityPerPiece DECIMAL(10,4) NOT NULL CONSTRAINT DF_BomIndMat_QtyPerPiece DEFAULT (1);
GO

PRINT 'Colonna QuantityPerPiece aggiornata su ind.BomIndirectMaterials.';
