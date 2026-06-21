-- ============================================================================
-- Schema ind - Materiali Indiretti - Redesign Giacenze (Libro Movimenti)
-- Database: Traceability_RS
-- Data: 2026-06-21
--
-- Aggiunge:
--   1. ind.MaterialiMovimenti   - libro movimenti append-only (fonte di verita')
--   2. ind.vw_GiacenzaCorrente  - vista giacenza corrente = SUM(Qty)
--   3. ind.MaterialiRiordino    - configurazione scorta minima / riordino
--   4. ind.RiordineEmailLog     - log invii email riordino (dedup)
--   5. Migrazione una-tantum da ind.MaterialiStock -> movimento INVENTARIO
--
-- Idempotente: rieseguibile senza effetti collaterali.
-- NB: NON modifica ind.MaterialiStock (resta in sola lettura per storico).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. ind.MaterialiMovimenti
-- ----------------------------------------------------------------------------
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
               WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiMovimenti')
BEGIN
    CREATE TABLE ind.MaterialiMovimenti (
        MovimentoId   INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId   INT NOT NULL,
        Qty           DECIMAL(18,4) NOT NULL,          -- +carico / -scarico (con segno)
        TipoMovimento NVARCHAR(20) NOT NULL,           -- CARICO / SCARICO / RETTIFICA / INVENTARIO
        RichiestaId   INT NULL,                        -- collegamento allo scarico da richiesta
        DataMovimento DATETIME NOT NULL DEFAULT GETDATE(),
        EseguitoDa    NVARCHAR(100),
        ComputerSrc   NVARCHAR(100),
        Note          NVARCHAR(500),
        CONSTRAINT FK_Movimenti_Materiali
            FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId),
        CONSTRAINT FK_Movimenti_Richieste
            FOREIGN KEY (RichiestaId) REFERENCES ind.MaterialiRichieste(RichiestaId),
        CONSTRAINT CK_Movimenti_Tipo
            CHECK (TipoMovimento IN ('CARICO','SCARICO','RETTIFICA','INVENTARIO'))
    );

    CREATE INDEX IX_Movimenti_Materiale
        ON ind.MaterialiMovimenti (MaterialeId, DataMovimento);

    -- Indice filtrato per ritrovare velocemente lo scarico di una richiesta
    CREATE INDEX IX_Movimenti_Richiesta
        ON ind.MaterialiMovimenti (RichiestaId) WHERE RichiestaId IS NOT NULL;

    PRINT 'Tabella [ind].[MaterialiMovimenti] creata.';
END
ELSE
    PRINT 'Tabella [ind].[MaterialiMovimenti] esistente.';
GO

-- ----------------------------------------------------------------------------
-- 2. ind.vw_GiacenzaCorrente - giacenza = SUM(Qty) sui movimenti
-- ----------------------------------------------------------------------------
IF OBJECT_ID('ind.vw_GiacenzaCorrente', 'V') IS NOT NULL
    DROP VIEW ind.vw_GiacenzaCorrente;
GO
CREATE VIEW ind.vw_GiacenzaCorrente AS
SELECT
    m.MaterialeId,
    m.CodiceMateriale,
    m.DescrizioneMateriale,
    m.TipoMaterialeId,
    CAST(ISNULL(SUM(mv.Qty), 0) AS DECIMAL(18,4)) AS Giacenza,
    MAX(mv.DataMovimento)                          AS UltimoMovimento
FROM ind.Materiali m
LEFT JOIN ind.MaterialiMovimenti mv ON mv.MaterialeId = m.MaterialeId
WHERE m.IsActive = 1
GROUP BY m.MaterialeId, m.CodiceMateriale, m.DescrizioneMateriale, m.TipoMaterialeId;
GO
PRINT 'Vista [ind].[vw_GiacenzaCorrente] creata.';
GO

-- ----------------------------------------------------------------------------
-- 3. ind.MaterialiRiordino - configurazione scorta minima
-- ----------------------------------------------------------------------------
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
               WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiRiordino')
BEGIN
    CREATE TABLE ind.MaterialiRiordino (
        MaterialeId   INT NOT NULL PRIMARY KEY,
        LivelloMinimo DECIMAL(18,4) NOT NULL,         -- soglia sotto cui scatta il riordino
        LottoRiordino DECIMAL(18,4) NULL,             -- qty proposta da riordinare
        IsAttivo      BIT NOT NULL DEFAULT 1,
        DataModifica  DATETIME DEFAULT GETDATE(),
        ModificatoDa  NVARCHAR(100),
        CONSTRAINT FK_Riordino_Materiali
            FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId)
    );
    PRINT 'Tabella [ind].[MaterialiRiordino] creata.';
END
ELSE
    PRINT 'Tabella [ind].[MaterialiRiordino] esistente.';
GO

-- ----------------------------------------------------------------------------
-- 4. ind.RiordineEmailLog - dedup invii email riordino
-- ----------------------------------------------------------------------------
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
               WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'RiordineEmailLog')
BEGIN
    CREATE TABLE ind.RiordineEmailLog (
        RiordineLogId    INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId      INT NOT NULL,
        GiacenzaRilevata DECIMAL(18,4),
        LivelloMinimo    DECIMAL(18,4),
        DataInvio        DATETIME NOT NULL DEFAULT GETDATE(),
        InviatoA         NVARCHAR(255),
        CONSTRAINT FK_RiordineLog_Materiali
            FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId)
    );
    CREATE INDEX IX_RiordineLog_Materiale_Data
        ON ind.RiordineEmailLog (MaterialeId, DataInvio);
    PRINT 'Tabella [ind].[RiordineEmailLog] creata.';
END
ELSE
    PRINT 'Tabella [ind].[RiordineEmailLog] esistente.';
GO

-- ----------------------------------------------------------------------------
-- 5. Migrazione una-tantum: giacenza attiva di MaterialiStock -> INVENTARIO
--    Eseguita SOLO per i materiali che non hanno ancora alcun movimento,
--    cosi' e' sicura da rieseguire.
-- ----------------------------------------------------------------------------
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_SCHEMA = 'ind' AND TABLE_NAME = 'MaterialiStock')
BEGIN
    INSERT INTO ind.MaterialiMovimenti
        (MaterialeId, Qty, TipoMovimento, DataMovimento, EseguitoDa, Note)
    SELECT s.MaterialeId,
           s.Qty,
           'INVENTARIO',
           ISNULL(s.DateIn, GETDATE()),
           ISNULL(s.CaricatoDa, 'MIGRAZIONE'),
           N'Giacenza iniziale migrata da ind.MaterialiStock'
    FROM ind.MaterialiStock s
    WHERE s.DateOut IS NULL
      AND NOT EXISTS (SELECT 1 FROM ind.MaterialiMovimenti mv
                      WHERE mv.MaterialeId = s.MaterialeId);

    PRINT 'Migrazione giacenze iniziali completata (movimenti INVENTARIO inseriti dove mancanti).';
END
ELSE
    PRINT 'ind.MaterialiStock non presente: migrazione saltata.';
GO

PRINT 'Setup redesign giacenze [ind] completato.';
