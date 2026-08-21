-- Aggiunge colonne per tracciare le righe etichetta inserite automaticamente
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.dbo.picking_list_items')
      AND name = 'Source'
)
    ALTER TABLE [Traceability_RS].[dbo].[picking_list_items]
        ADD Source NVARCHAR(20) NULL DEFAULT 'FILE';
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.dbo.picking_list_items')
      AND name = 'LabelRequestData'
)
    ALTER TABLE [Traceability_RS].[dbo].[picking_list_items]
        ADD LabelRequestData NVARCHAR(MAX) NULL;
GO

PRINT 'Colonne Source e LabelRequestData aggiornate su dbo.picking_list_items.';
