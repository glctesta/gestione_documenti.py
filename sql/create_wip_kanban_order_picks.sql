-- ============================================================================
-- Kanban WIP — "prelievo per ordine" con scarico differito al passaggio PTHM
--
-- 1. WipKanbanOrderPicks: richiesta di prelievo di un ordine WIP; le schede
--    restano fisicamente in kanban (PendingPickId su WipKanbanBoards) e vengono
--    scaricate (DateOut) dallo sweep PTHM quando passano la fase PTHM.
-- 2. WipKanbanBoards.PendingPickId: riferimento al pick aperto della scheda.
-- ============================================================================

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'WipKanbanOrderPicks'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.WipKanbanOrderPicks (
        PickId       INT IDENTITY(1,1) PRIMARY KEY,
        OrderNumber  NVARCHAR(50)  NOT NULL,
        ProductCode  NVARCHAR(50)  NULL,
        RequestedBy  NVARCHAR(100) NOT NULL,
        RequestedOn  DATETIME      NOT NULL DEFAULT GETDATE(),
        BoardCount   INT           NOT NULL,
        PassedCount  INT           NOT NULL DEFAULT(0)
    );
    CREATE INDEX IX_WKOP_Order ON Traceability_RS.ind.WipKanbanOrderPicks (OrderNumber);
    PRINT 'Creata tabella Traceability_RS.ind.WipKanbanOrderPicks';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.WipKanbanOrderPicks già esistente';
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.WipKanbanBoards')
      AND name = 'PendingPickId'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.WipKanbanBoards
        ADD PendingPickId INT NULL;
    PRINT 'Aggiunta colonna PendingPickId a WipKanbanBoards';
END
ELSE
BEGIN
    PRINT 'Colonna PendingPickId già presente su WipKanbanBoards';
END
GO

-- Indice filtrato: schede pending (in attesa di scarico PTHM)
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('Traceability_RS.ind.WipKanbanBoards')
      AND name = 'IX_WKB_PendingPick'
)
BEGIN
    CREATE INDEX IX_WKB_PendingPick
        ON Traceability_RS.ind.WipKanbanBoards (PendingPickId)
        WHERE DateOut IS NULL;
    PRINT 'Creato indice IX_WKB_PendingPick';
END
ELSE
BEGIN
    PRINT 'Indice IX_WKB_PendingPick già esistente';
END
GO

PRINT 'Schema prelievo-per-ordine kanban aggiornato.';
