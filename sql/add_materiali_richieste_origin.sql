-- Aggiunge origine e riferimenti ordini alle richieste di materiali indiretti
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.MaterialiRichieste')
      AND name = 'Origin'
)
    ALTER TABLE [Traceability_RS].[ind].[MaterialiRichieste]
        ADD Origin NVARCHAR(10) NULL CONSTRAINT CK_MatRich_Origin CHECK (Origin IN ('MANUALE', 'AUTO'));
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.MaterialiRichieste')
      AND name = 'ReferenceOrderIds'
)
    ALTER TABLE [Traceability_RS].[ind].[MaterialiRichieste]
        ADD ReferenceOrderIds NVARCHAR(MAX) NULL;
GO

PRINT 'Colonne Origin e ReferenceOrderIds aggiornate su ind.MaterialiRichieste.';
