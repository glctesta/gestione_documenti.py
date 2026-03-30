-- =============================================================================
-- Aggiunge VisitorId a VisitorArrivalDetails per creare un legame diretto
-- tra ogni visitatore e i suoi dettagli di arrivo/booking.
--
-- Attualmente il legame è implicito (match per date), questa modifica
-- rende la relazione esplicita con FK.
--
-- Il campo è NULLABLE per backward-compatibility con i record esistenti.
-- =============================================================================

-- Step 1: Aggiungi colonna VisitorId (nullable)
IF NOT EXISTS (
    SELECT 1
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'VisitorArrivalDetails'
      AND COLUMN_NAME = 'VisitorId'
)
BEGIN
    ALTER TABLE Employee.dbo.VisitorArrivalDetails
        ADD VisitorId INT NULL;

    PRINT 'Colonna VisitorId aggiunta a VisitorArrivalDetails.';
END
ELSE
BEGIN
    PRINT 'Colonna VisitorId già presente in VisitorArrivalDetails.';
END
GO

-- Step 2: Aggiungi Foreign Key verso Visitors
IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_VisitorArrivalDetails_Visitors'
)
BEGIN
    ALTER TABLE Employee.dbo.VisitorArrivalDetails
        ADD CONSTRAINT FK_VisitorArrivalDetails_Visitors
        FOREIGN KEY (VisitorId)
        REFERENCES Employee.dbo.Visitors (VisitorId);

    PRINT 'FK_VisitorArrivalDetails_Visitors creata.';
END
ELSE
BEGIN
    PRINT 'FK_VisitorArrivalDetails_Visitors già presente.';
END
GO

-- Step 3: Indice per performance sui JOIN
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_VisitorArrivalDetails_VisitorId'
      AND object_id = OBJECT_ID('Employee.dbo.VisitorArrivalDetails')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_VisitorArrivalDetails_VisitorId
        ON Employee.dbo.VisitorArrivalDetails (VisitorId)
        WHERE VisitorId IS NOT NULL;

    PRINT 'Indice IX_VisitorArrivalDetails_VisitorId creato.';
END
GO

-- Step 4: Backfill — Popola VisitorId per i record esistenti (best-effort via date match)
UPDATE vad
SET vad.VisitorId = v.VisitorId
FROM Employee.dbo.VisitorArrivalDetails vad
CROSS APPLY (
    SELECT TOP 1 v2.VisitorId
    FROM Employee.dbo.Visitors v2
    WHERE CAST(v2.StartVisit AS DATE) = CAST(vad.DateTimeArrival AS DATE)
      AND v2.EndVisit >= vad.DateOut
    ORDER BY v2.VisitorId DESC
) v
WHERE vad.VisitorId IS NULL;

PRINT 'Backfill completato: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' record aggiornati.';
GO
