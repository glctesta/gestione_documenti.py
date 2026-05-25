-- ============================================================
-- Migration: aggiunge colonne di conferma spedizione urgente
-- Tabella: [Traceability_RS].[dyn].[DynamicShippingRules]
-- ============================================================

-- Colonna: nome utente che ha confermato la spedizione
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[DynamicShippingRules]')
      AND name = 'ConfirmedByUser'
)
    ALTER TABLE [Traceability_RS].[dyn].[DynamicShippingRules]
        ADD ConfirmedByUser NVARCHAR(100) NULL;
GO

-- Colonna: quantità confermata dall'operatore (può differire da QtyToShip)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[DynamicShippingRules]')
      AND name = 'ConfirmedQty'
)
    ALTER TABLE [Traceability_RS].[dyn].[DynamicShippingRules]
        ADD ConfirmedQty INT NULL;
GO

-- Colonna: data/ora completa della conferma
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[DynamicShippingRules]')
      AND name = 'ConfirmedAt'
)
    ALTER TABLE [Traceability_RS].[dyn].[DynamicShippingRules]
        ADD ConfirmedAt DATETIME NULL;
GO

-- Colonna: ultimo timestamp di notifica popup su postazioni spedizioni
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[DynamicShippingRules]')
      AND name = 'LastShipmentNotify'
)
    ALTER TABLE [Traceability_RS].[dyn].[DynamicShippingRules]
        ADD LastShipmentNotify DATETIME NULL;
GO

-- Inserimento attributo email in traceability_rs.dbo.settings (se non esiste)
-- Sostituire '<indirizzo@email.it>' con l'indirizzo reale prima di eseguire
IF NOT EXISTS (
    SELECT 1 FROM traceability_rs.dbo.settings
    WHERE atribute = 'Sys_shipment_email'
)
    INSERT INTO traceability_rs.dbo.settings (atribute, [VALUE])
    VALUES ('Sys_shipment_email', '<indirizzo@email.it>');
GO
