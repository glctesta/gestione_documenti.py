-- ============================================================
-- Fix: dbo.ReturnMaterials.RichiestaId deve ammettere NULL.
-- Le scorie/rientri vengono dichiarate con RichiestaId = NULL
-- (non ancora consumate) e collegate a una richiesta in un secondo
-- momento via UPDATE (vedi indirect_materials_request._link_scrap_to_request).
-- La colonna era stata creata NOT NULL per errore, rompendo il salvataggio
-- nella form "Gestione scorie / rientri" (scrap_returns_gui.py).
-- La FK FK_ReturnMaterials_MaterialiRichieste resta valida: i NULL non la violano.
-- Idempotente.
-- ============================================================
IF EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Traceability_RS.dbo.ReturnMaterials')
      AND name = 'RichiestaId'
      AND is_nullable = 0
)
BEGIN
    ALTER TABLE [Traceability_RS].[dbo].[ReturnMaterials]
        ALTER COLUMN [RichiestaId] INT NULL;
    PRINT 'RichiestaId reso NULLABLE';
END
ELSE
    PRINT 'RichiestaId gia'' NULLABLE (nessuna azione)';
GO
