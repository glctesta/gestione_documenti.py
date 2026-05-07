-- ============================================================
-- Fix: FaiLogs.DateIn tipo colonna DATE -> DATETIME
-- 
-- Rimuove constraint/indici dipendenti, altera la colonna,
-- poi li ricrea.
-- ============================================================

USE [Traceability_RS];
GO

-- 1. Rimuovi il DEFAULT constraint
IF EXISTS (SELECT 1 FROM sys.default_constraints WHERE name = 'DF_FaiLogs_DateIn')
BEGIN
    ALTER TABLE [fai].[FaiLogs] DROP CONSTRAINT [DF_FaiLogs_DateIn];
    PRINT 'Rimosso constraint DF_FaiLogs_DateIn';
END
GO

-- 2. Rimuovi l'indice non-clustered
IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'NonClusteredIndex-20260114-174033' AND object_id = OBJECT_ID('fai.FaiLogs'))
BEGIN
    DROP INDEX [NonClusteredIndex-20260114-174033] ON [fai].[FaiLogs];
    PRINT 'Rimosso indice NonClusteredIndex-20260114-174033';
END
GO

-- 3. Ora altera la colonna da DATE a DATETIME
ALTER TABLE [fai].[FaiLogs]
ALTER COLUMN [DateIn] DATETIME NOT NULL;
PRINT '✅ Colonna DateIn convertita da DATE a DATETIME';
GO

-- 4. Ricrea il DEFAULT constraint
ALTER TABLE [fai].[FaiLogs]
ADD CONSTRAINT [DF_FaiLogs_DateIn] DEFAULT (GETDATE()) FOR [DateIn];
PRINT 'Ricreato constraint DF_FaiLogs_DateIn';
GO

-- 5. Ricrea l'indice (stessa colonna)
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20260114-174033] 
ON [fai].[FaiLogs] ([DateIn] ASC);
PRINT 'Ricreato indice su DateIn';
GO

-- 6. Fix anche DateOut se necessario
IF EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'fai' AND TABLE_NAME = 'FaiLogs' 
      AND COLUMN_NAME = 'DateOut' AND DATA_TYPE = 'date'
)
BEGIN
    -- Rimuovi eventuali constraint su DateOut
    DECLARE @defName NVARCHAR(200);
    SELECT @defName = d.name
    FROM sys.default_constraints d
    INNER JOIN sys.columns c ON d.parent_column_id = c.column_id 
        AND d.parent_object_id = c.object_id
    WHERE d.parent_object_id = OBJECT_ID('fai.FaiLogs')
        AND c.name = 'DateOut';
    
    IF @defName IS NOT NULL
    BEGIN
        EXEC('ALTER TABLE [fai].[FaiLogs] DROP CONSTRAINT [' + @defName + ']');
        PRINT 'Rimosso constraint su DateOut: ' + @defName;
    END

    ALTER TABLE [fai].[FaiLogs] ALTER COLUMN [DateOut] DATETIME NULL;
    PRINT '✅ Colonna DateOut convertita da DATE a DATETIME';
END
GO

-- 7. Verifica finale
SELECT 
    c.COLUMN_NAME, c.DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_SCHEMA = 'fai' AND c.TABLE_NAME = 'FaiLogs'
  AND c.COLUMN_NAME IN ('DateIn', 'DateOut');
GO

PRINT '=== Fix completato ===';
GO
