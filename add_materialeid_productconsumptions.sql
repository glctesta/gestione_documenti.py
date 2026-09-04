-- Aggiunge la colonna MaterialeId a ProductConsumptions (link al materiale indiretto in ind.Materiali)
-- Eseguire una volta sola come amministratore del DB.

USE Traceability_RS;
GO

-- 1. Colonna (NULL per i record esistenti)
IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID('dbo.ProductConsumptions')
                 AND name = 'MaterialeId')
BEGIN
    ALTER TABLE dbo.ProductConsumptions ADD MaterialeId INT NULL;
END
GO

-- 2. Foreign key verso il catalogo materiali indiretti (stesso database, schema ind)
--    Verificare che ind.Materiali.MaterialeId sia la PK prima di eseguire.
IF EXISTS (SELECT 1 FROM sys.tables WHERE object_id = OBJECT_ID('ind.Materiali'))
   AND NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_ProductConsumptions_Materiali')
BEGIN
    ALTER TABLE dbo.ProductConsumptions WITH CHECK
    ADD CONSTRAINT FK_ProductConsumptions_Materiali
    FOREIGN KEY (MaterialeId) REFERENCES ind.Materiali (MaterialeId);
END
GO

-- 3. Indice per le join su MaterialeId
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'IX_ProductConsumptions_MaterialeId'
                 AND object_id = OBJECT_ID('dbo.ProductConsumptions'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_ProductConsumptions_MaterialeId
    ON dbo.ProductConsumptions (MaterialeId)
    WHERE MaterialeId IS NOT NULL;
END
GO
