-- ============================================================
-- Scarti etichette: materiale indiretto + quantita' manuale
--
-- Aggiunge a traceability_rs.dbo.labelscrap:
--   MaterialeId      -> ind.Materiali(MaterialeId)
--   CodiceMateriale  -> copia del codice al momento dello scarto
--   Qty              -> quantita' (1 per ogni etichetta scansionata)
--
-- Idempotente: si puo' rieseguire senza effetti.
-- Non modifica alcuna riga esistente se non per valorizzare Qty = 1,
-- che e' esattamente quanto valevano prima (una riga = una etichetta),
-- quindi tutti i conteggi storici restano identici.
-- ============================================================

USE [traceability_rs];
GO

-- --- MaterialeId -------------------------------------------------------
-- NULL consentito: le righe gia' registrate non hanno un materiale e non
-- e' possibile dedurlo a posteriori. L'obbligatorieta' e' applicata dalla
-- form per le righe NUOVE.
IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID('dbo.labelscrap') AND name = 'MaterialeId')
BEGIN
    ALTER TABLE dbo.labelscrap ADD MaterialeId INT NULL;
    PRINT 'Aggiunta colonna MaterialeId';
END
ELSE PRINT 'MaterialeId gia'' presente';
GO

-- --- CodiceMateriale ---------------------------------------------------
-- Denormalizzato di proposito: se un domani il codice in anagrafica viene
-- rinominato, lo storico deve continuare a mostrare il codice usato al
-- momento della dichiarazione (che e' quello finito sui documenti firmati).
IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID('dbo.labelscrap') AND name = 'CodiceMateriale')
BEGIN
    ALTER TABLE dbo.labelscrap ADD CodiceMateriale NVARCHAR(50) NULL;
    PRINT 'Aggiunta colonna CodiceMateriale';
END
ELSE PRINT 'CodiceMateriale gia'' presente';
GO

-- --- Qty ---------------------------------------------------------------
-- Due passaggi: prima NULL, poi backfill a 1, poi NOT NULL. Aggiungerla
-- direttamente NOT NULL DEFAULT 1 funzionerebbe, ma cosi' e' esplicito
-- che le righe storiche valgono 1 e non un default implicito.
IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID('dbo.labelscrap') AND name = 'Qty')
BEGIN
    ALTER TABLE dbo.labelscrap ADD Qty INT NULL;
    PRINT 'Aggiunta colonna Qty';
END
ELSE PRINT 'Qty gia'' presente';
GO

UPDATE dbo.labelscrap SET Qty = 1 WHERE Qty IS NULL;
PRINT 'Righe storiche portate a Qty = 1: ' + CAST(@@ROWCOUNT AS VARCHAR(10));
GO

IF EXISTS (SELECT 1 FROM sys.columns
           WHERE object_id = OBJECT_ID('dbo.labelscrap') AND name = 'Qty' AND is_nullable = 1)
BEGIN
    ALTER TABLE dbo.labelscrap ALTER COLUMN Qty INT NOT NULL;
    PRINT 'Qty resa NOT NULL';
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.default_constraints
               WHERE parent_object_id = OBJECT_ID('dbo.labelscrap') AND name = 'DF_labelscrap_Qty')
BEGIN
    ALTER TABLE dbo.labelscrap ADD CONSTRAINT DF_labelscrap_Qty DEFAULT (1) FOR Qty;
    PRINT 'Aggiunto default 1 su Qty';
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.check_constraints
               WHERE parent_object_id = OBJECT_ID('dbo.labelscrap') AND name = 'CK_labelscrap_Qty')
BEGIN
    ALTER TABLE dbo.labelscrap ADD CONSTRAINT CK_labelscrap_Qty CHECK (Qty > 0);
    PRINT 'Aggiunto vincolo Qty > 0';
END
GO

-- --- FK verso l'anagrafica materiali indiretti -------------------------
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_labelscrap_Materiale')
   AND EXISTS (SELECT 1 FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id
               WHERE s.name = 'ind' AND t.name = 'Materiali')
BEGIN
    ALTER TABLE dbo.labelscrap WITH NOCHECK
        ADD CONSTRAINT FK_labelscrap_Materiale
        FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali(MaterialeId);
    PRINT 'Aggiunta FK_labelscrap_Materiale';
END
ELSE PRINT 'FK gia'' presente o ind.Materiali non raggiungibile';
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'IX_labelscrap_Materiale'
                 AND object_id = OBJECT_ID('dbo.labelscrap'))
    CREATE NONCLUSTERED INDEX IX_labelscrap_Materiale
        ON dbo.labelscrap (MaterialeId) WHERE MaterialeId IS NOT NULL;
GO

-- --- Verifica ----------------------------------------------------------
SELECT c.name AS Colonna, t.name AS Tipo, c.max_length AS Lunghezza, c.is_nullable AS Nullable
FROM sys.columns c
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.labelscrap')
ORDER BY c.column_id;

-- Quanti materiali indiretti verranno proposti nel combo
SELECT COUNT(*) AS MaterialiLAB
FROM ind.Materiali
WHERE IsActive = 1 AND DescrizioneMateriale LIKE '%LAB%';
GO

-- Per tornare indietro:
--   ALTER TABLE dbo.labelscrap DROP CONSTRAINT FK_labelscrap_Materiale;
--   DROP INDEX IX_labelscrap_Materiale ON dbo.labelscrap;
--   ALTER TABLE dbo.labelscrap DROP CONSTRAINT CK_labelscrap_Qty;
--   ALTER TABLE dbo.labelscrap DROP CONSTRAINT DF_labelscrap_Qty;
--   ALTER TABLE dbo.labelscrap DROP COLUMN Qty, CodiceMateriale, MaterialeId;
