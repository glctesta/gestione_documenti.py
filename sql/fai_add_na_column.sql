-- ============================================================
-- Aggiunge colonna IsNA (Not Applicable) alla tabella FaiLogs
-- Quando IsNA = 1, lo step NON viene conteggiato nella 
-- validazione finale (né come OK, né come mancante)
-- ============================================================

IF NOT EXISTS (
    SELECT 1 FROM sys.columns 
    WHERE object_id = OBJECT_ID('Traceability_RS.fai.FaiLogs') 
    AND name = 'IsNA'
)
BEGIN
    ALTER TABLE [Traceability_RS].[fai].[FaiLogs]
    ADD IsNA BIT NOT NULL CONSTRAINT DF_FaiLogs_IsNA DEFAULT 0;
    
    PRINT 'Colonna IsNA aggiunta a fai.FaiLogs';
END
ELSE
BEGIN
    PRINT 'Colonna IsNA già esistente in fai.FaiLogs';
END
GO
