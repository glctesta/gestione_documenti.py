-- ============================================================================
-- ALTER TABLE ind.MaterialiRichieste - Aggiungi campi per notifiche e tracking
-- Database: Traceability_RS
-- Data: 2026-03-18
-- ============================================================================

-- ComputerRichiedente
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='ind' AND TABLE_NAME='MaterialiRichieste' AND COLUMN_NAME='ComputerRichiedente')
BEGIN
    ALTER TABLE ind.MaterialiRichieste ADD ComputerRichiedente NVARCHAR(100) NULL;
    PRINT 'Aggiunto ComputerRichiedente.';
END
GO

-- ComputerPreparatore
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='ind' AND TABLE_NAME='MaterialiRichieste' AND COLUMN_NAME='ComputerPreparatore')
BEGIN
    ALTER TABLE ind.MaterialiRichieste ADD ComputerPreparatore NVARCHAR(100) NULL;
    PRINT 'Aggiunto ComputerPreparatore.';
END
GO

-- DataUltimaNotificaWH: quando il WH e' stato notificato l'ultima volta
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='ind' AND TABLE_NAME='MaterialiRichieste' AND COLUMN_NAME='DataUltimaNotificaWH')
BEGIN
    ALTER TABLE ind.MaterialiRichieste ADD DataUltimaNotificaWH DATETIME NULL;
    PRINT 'Aggiunto DataUltimaNotificaWH.';
END
GO

-- DataUltimaNotificaRichiedente: quando il richiedente e' stato notificato l'ultima volta
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='ind' AND TABLE_NAME='MaterialiRichieste' AND COLUMN_NAME='DataUltimaNotificaRichiedente')
BEGIN
    ALTER TABLE ind.MaterialiRichieste ADD DataUltimaNotificaRichiedente DATETIME NULL;
    PRINT 'Aggiunto DataUltimaNotificaRichiedente.';
END
GO

PRINT 'ALTER TABLE ind.MaterialiRichieste completato.';
