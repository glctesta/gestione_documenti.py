-- Colonna conteggio stampe del documento di ricezione materiali indiretti.
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.MaterialiRichieste')
      AND name = 'StampeRicezione'
)
    ALTER TABLE [Traceability_RS].[ind].[MaterialiRichieste]
        ADD StampeRicezione INT NOT NULL CONSTRAINT DF_MatRich_StampeRicezione DEFAULT (0);
