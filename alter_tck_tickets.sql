-- ============================================================
--  alter_tck_tickets.sql
--  Aggiunge le colonne per tracking apertura/chiusura e stati
--  al sistema di ticketing tck.Tickets.
--  Script idempotente: sicuro per esecuzioni ripetute.
-- ============================================================

USE [Traceability_RS];
GO

-- 1. Colonna OpenedByEmployeeId (EmployeeHireHistoryId di chi apre il ticket)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'OpenedByEmployeeId'
)
BEGIN
    ALTER TABLE tck.Tickets ADD OpenedByEmployeeId INT NULL;
    PRINT 'Colonna OpenedByEmployeeId aggiunta.';
END
GO

-- 2. Colonna OpenedByName (Nome completo dell'utente)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'OpenedByName'
)
BEGIN
    ALTER TABLE tck.Tickets ADD OpenedByName NVARCHAR(200) NULL;
    PRINT 'Colonna OpenedByName aggiunta.';
END
GO

-- 3. Colonna OpenedByEmail (WorkEmail se disponibile)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'OpenedByEmail'
)
BEGIN
    ALTER TABLE tck.Tickets ADD OpenedByEmail NVARCHAR(200) NULL;
    PRINT 'Colonna OpenedByEmail aggiunta.';
END
GO

-- 4. Colonna ClosedAt (Data/ora chiusura)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'ClosedAt'
)
BEGIN
    ALTER TABLE tck.Tickets ADD ClosedAt DATETIME2(0) NULL;
    PRINT 'Colonna ClosedAt aggiunta.';
END
GO

-- 5. Colonna ClosedBy (EmployeeHireHistoryId di chi chiude)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'ClosedBy'
)
BEGIN
    ALTER TABLE tck.Tickets ADD ClosedBy INT NULL;
    PRINT 'Colonna ClosedBy aggiunta.';
END
GO

-- 6. Colonna ClosedByName (Nome di chi chiude il ticket)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'ClosedByName'
)
BEGIN
    ALTER TABLE tck.Tickets ADD ClosedByName NVARCHAR(200) NULL;
    PRINT 'Colonna ClosedByName aggiunta.';
END
GO

-- 7. Colonna ClosureNote (Nota di risposta/risoluzione)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'ClosureNote'
)
BEGIN
    ALTER TABLE tck.Tickets ADD ClosureNote NVARCHAR(MAX) NULL;
    PRINT 'Colonna ClosureNote aggiunta.';
END
GO

-- 8. Colonna ClosureNotified (1 se utente è stato notificato)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID(N'tck.Tickets') AND name = N'ClosureNotified'
)
BEGIN
    ALTER TABLE tck.Tickets ADD ClosureNotified BIT NOT NULL DEFAULT 0;
    PRINT 'Colonna ClosureNotified aggiunta.';
END
GO

-- 9. Aggiornare il DEFAULT dello Status da 'open' ai nuovi valori ammessi
-- I valori ammessi sono: 'open', 'on_working', 'closed'
-- Il default rimane 'open', ma aggiorniamo il commento
PRINT 'Stati ammessi per Status: open, on_working, closed';
GO

-- 10. Indice su OpenedByEmployeeId per query rapide sullo storico utente
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE  object_id = OBJECT_ID(N'tck.Tickets')
      AND  name      = N'IX_tck_Tickets_OpenedBy'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_tck_Tickets_OpenedBy
        ON tck.Tickets (OpenedByEmployeeId, Status, CreatedAt DESC);
    PRINT 'Indice IX_tck_Tickets_OpenedBy creato.';
END
GO

-- 11. Indice su ClosureNotified per la query di notifica al login
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE  object_id = OBJECT_ID(N'tck.Tickets')
      AND  name      = N'IX_tck_Tickets_ClosureNotified'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_tck_Tickets_ClosureNotified
        ON tck.Tickets (OpenedByEmployeeId, ClosureNotified)
        WHERE Status = N'closed' AND ClosureNotified = 0;
    PRINT 'Indice IX_tck_Tickets_ClosureNotified creato.';
END
GO

PRINT '=== Alterazione tck.Tickets completata ===';
GO
