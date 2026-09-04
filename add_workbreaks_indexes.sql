-- ============================================================================
-- Indici per velocizzare il caricamento della maschera Gestione Orari
-- ============================================================================

-- Indice su WorkBreaks per filtrare rapidamente le regole attive
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_WorkBreaks_DateOut'
      AND object_id = OBJECT_ID(N'[Employee].[dbo].[WorkBreaks]')
)
BEGIN
    CREATE NONCLUSTERED INDEX [IX_WorkBreaks_DateOut]
        ON [Employee].[dbo].[WorkBreaks] ([DateOut])
        INCLUDE ([IsForChangeShift], [Shift], [FromTime], [ToTime], [EmployeerId], [WorkBreakReasonId]);
    PRINT 'Indice IX_WorkBreaks_DateOut creato.';
END
ELSE
BEGIN
    PRINT 'Indice IX_WorkBreaks_DateOut gia esistente.';
END
GO

-- Indice su WorkBreakData per filtrare i figli attivi di un WorkBreakId
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_WorkBreakData_WorkBreakId_DateOut'
      AND object_id = OBJECT_ID(N'[Employee].[dbo].[WorkBreakData]')
)
BEGIN
    CREATE NONCLUSTERED INDEX [IX_WorkBreakData_WorkBreakId_DateOut]
        ON [Employee].[dbo].[WorkBreakData] ([WorkBreakId], [DateOut])
        INCLUDE ([CdcId], [SubCdcId], [FunctionId]);
    PRINT 'Indice IX_WorkBreakData_WorkBreakId_DateOut creato.';
END
ELSE
BEGIN
    PRINT 'Indice IX_WorkBreakData_WorkBreakId_DateOut gia esistente.';
END
GO
