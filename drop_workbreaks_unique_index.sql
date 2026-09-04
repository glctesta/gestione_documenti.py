-- ============================================================================
-- Rimuove l'indice unique obsoleto su WorkBreaks.
-- Dopo la ristrutturazione i valori multipli (CDC, SubCDC, Funzioni) sono
-- gestiti tramite WorkBreakData, quindi il vincolo di unicità sul padre
-- includeva colonne nullable e impediva inserimenti validi.
-- ============================================================================

IF EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'NonClusteredIndex-20260828-131608'
      AND object_id = OBJECT_ID(N'[Employee].[dbo].[WorkBreaks]')
)
BEGIN
    DROP INDEX [NonClusteredIndex-20260828-131608] ON [Employee].[dbo].[WorkBreaks];
    PRINT 'Indice unique NonClusteredIndex-20260828-131608 rimosso.';
END
ELSE
BEGIN
    PRINT 'Indice NonClusteredIndex-20260828-131608 non trovato.';
END
GO
