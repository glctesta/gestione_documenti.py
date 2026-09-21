-- ============================================================================
-- Kanban produzione WIP/REPAIR — colonne per il display di reparto (porta 6505)
--
-- 1. Deposit    : quale deposito fisico (futuri depositi multipli; oggi = 1)
-- 2. RowIndex    : posizione del pallet nella fila (da sinistra, da 1),
--                  per Area+Deposit; uguale per tutte le 16 posizioni del pallet
-- ============================================================================

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.WipKanbanLocations')
      AND name = 'Deposit'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.WipKanbanLocations
        ADD Deposit INT NOT NULL
        CONSTRAINT DF_WipKanbanLocations_Deposit DEFAULT(1);
    PRINT 'Aggiunta colonna Deposit a WipKanbanLocations';
END
ELSE
BEGIN
    PRINT 'Colonna Deposit già presente su WipKanbanLocations';
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.WipKanbanLocations')
      AND name = 'RowIndex'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.WipKanbanLocations
        ADD RowIndex INT NULL;
    PRINT 'Aggiunta colonna RowIndex a WipKanbanLocations';
END
ELSE
BEGIN
    PRINT 'Colonna RowIndex già presente su WipKanbanLocations';
END
GO

-- Le righe esistenti ereditano Deposit = 1 tramite il default con valore fisso:
-- con ADD COLUMN ... DEFAULT su SQL Server il default si applica anche alle
-- righe preesistenti (stored nel metadata, nessuna scansione).
-- RowIndex resta NULL per i pallet esistenti: va valorizzato dalla pagina
-- Carica ("Salva posizione in fila") o lasciato NULL (il display li mostra
-- in fondo, ordinati per PalletNumber).

PRINT 'Schema display kanban aggiornato.';
