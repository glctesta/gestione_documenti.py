-- ============================================================================
-- Rende nullable le colonne IdCdc, IdSubCdc e functionId di WorkBreaks
-- perché i valori multipli sono ora gestiti tramite WorkBreakData.
-- ============================================================================

IF EXISTS (
    SELECT 1
    FROM Employee.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'WorkBreaks'
      AND COLUMN_NAME = 'IdCdc'
      AND IS_NULLABLE = 'NO'
)
BEGIN
    ALTER TABLE [Employee].[dbo].[WorkBreaks] ALTER COLUMN [IdCdc] INT NULL;
    PRINT 'Colonna IdCdc resa nullable.';
END
ELSE
BEGIN
    PRINT 'Colonna IdCdc già nullable o non esistente.';
END
GO

IF EXISTS (
    SELECT 1
    FROM Employee.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'WorkBreaks'
      AND COLUMN_NAME = 'IdSubCdc'
      AND IS_NULLABLE = 'NO'
)
BEGIN
    ALTER TABLE [Employee].[dbo].[WorkBreaks] ALTER COLUMN [IdSubCdc] INT NULL;
    PRINT 'Colonna IdSubCdc resa nullable.';
END
ELSE
BEGIN
    PRINT 'Colonna IdSubCdc già nullable o non esistente.';
END
GO

IF EXISTS (
    SELECT 1
    FROM Employee.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'WorkBreaks'
      AND COLUMN_NAME = 'functionId'
      AND IS_NULLABLE = 'NO'
)
BEGIN
    ALTER TABLE [Employee].[dbo].[WorkBreaks] ALTER COLUMN [functionId] INT NULL;
    PRINT 'Colonna functionId resa nullable.';
END
ELSE
BEGIN
    PRINT 'Colonna functionId già nullable o non esistente.';
END
GO
