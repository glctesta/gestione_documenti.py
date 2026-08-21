-- Schema dati per gestione conferma acquisti materiali indiretti

-- Estende RiordineEmailLog per tracciare codici/quantità inviate e stato conferma
IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'QtaSuggerita'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD QtaSuggerita DECIMAL(10,4) NULL;
    PRINT 'Aggiunta colonna QtaSuggerita';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'QtaOrdinata'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD QtaOrdinata DECIMAL(10,4) NULL;
    PRINT 'Aggiunta colonna QtaOrdinata';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'NumeroPO'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD NumeroPO NVARCHAR(100) NULL;
    PRINT 'Aggiunta colonna NumeroPO';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'DataPrevistaArrivo'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD DataPrevistaArrivo DATE NULL;
    PRINT 'Aggiunta colonna DataPrevistaArrivo';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'Stato'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD Stato NVARCHAR(20) NOT NULL DEFAULT 'INVIATO';
    PRINT 'Aggiunta colonna Stato';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'DataConferma'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD DataConferma DATETIME NULL;
    PRINT 'Aggiunta colonna DataConferma';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'ConfermatoDa'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD ConfermatoDa NVARCHAR(255) NULL;
    PRINT 'Aggiunta colonna ConfermatoDa';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'ReminderCount'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD ReminderCount INT NOT NULL DEFAULT 0;
    PRINT 'Aggiunta colonna ReminderCount';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'RiordineEmailLog' AND c.name = 'DataUltimoReminder'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.RiordineEmailLog
    ADD DataUltimoReminder DATETIME NULL;
    PRINT 'Aggiunta colonna DataUltimoReminder';
END

PRINT 'Schema per gestione conferma acquisti materiali indiretti aggiornato.';
GO
