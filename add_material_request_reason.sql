-- ============================================================
-- Richieste materiale kit: categoria/motivazione strutturata.
--
-- Aggiunge dbo.material_requests.reason: codice della motivazione
-- (KIT_INCOMPLETE, SCRAP, DAMAGED, MISSING, OTHER). La nota testuale
-- libera resta in material_requests.note.
--
-- Idempotente. NULL consentito: le richieste create prima di questa
-- modifica (e i flussi che non la impostano) restano valide.
-- ============================================================

USE [Traceability_RS];
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID('dbo.material_requests') AND name = 'reason')
BEGIN
    ALTER TABLE dbo.material_requests ADD reason NVARCHAR(40) NULL;
    PRINT 'Aggiunta colonna material_requests.reason';
END
ELSE
    PRINT 'material_requests.reason gia'' presente';
GO
