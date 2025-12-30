-- Script SQL per creare la tabella ProgettoDocumenti
-- Database: Traceability_rs
-- Scopo: Gestione documenti allegati ai progetti NPI

USE Traceability_rs;
GO

-- ============================================================================
-- CREAZIONE TABELLA ProgettoDocumenti
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ProgettoDocumenti' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.ProgettoDocumenti (
        DocumentoID INT PRIMARY KEY IDENTITY(1,1),
        ProgettoID INT NOT NULL,
        NomeFile NVARCHAR(255) NOT NULL,
        TipoFile NVARCHAR(50) NULL,
        Dimensione INT NULL,
        Contenuto VARBINARY(MAX) NOT NULL,
        Descrizione NVARCHAR(500) NULL,
        CaricatoDa NVARCHAR(255) NULL,
        DataCaricamento DATETIME NOT NULL DEFAULT GETDATE(),
        
        CONSTRAINT FK_ProgettoDocumenti_Progetto 
            FOREIGN KEY (ProgettoID) REFERENCES dbo.ProgettiNPI(ProgettoID)
            ON DELETE CASCADE
    );
    
    PRINT 'Tabella ProgettoDocumenti creata con successo';
END
ELSE
BEGIN
    PRINT 'Tabella ProgettoDocumenti già esistente';
END
GO

-- ============================================================================
-- CREAZIONE INDICE PER PERFORMANCE
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_ProgettoDocumenti_ProgettoID')
BEGIN
    CREATE INDEX IX_ProgettoDocumenti_ProgettoID 
        ON dbo.ProgettoDocumenti(ProgettoID);
    
    PRINT 'Indice IX_ProgettoDocumenti_ProgettoID creato con successo';
END
ELSE
BEGIN
    PRINT 'Indice IX_ProgettoDocumenti_ProgettoID già esistente';
END
GO

-- ============================================================================
-- AGGIUNGI COMMENTI DESCRITTIVI
-- ============================================================================

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabella per la gestione dei documenti allegati ai progetti NPI', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'ID univoco del documento', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'DocumentoID';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'ID del progetto NPI a cui appartiene il documento', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'ProgettoID';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Nome originale del file', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'NomeFile';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'MIME type del file (es: image/png, application/pdf)', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'TipoFile';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Dimensione del file in bytes', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'Dimensione';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Contenuto binario del file', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'Contenuto';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Descrizione opzionale del documento', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'Descrizione';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Nome dell''utente che ha caricato il documento', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'CaricatoDa';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Data e ora di caricamento del documento', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettoDocumenti',
    @level2type = N'COLUMN', @level2name = 'DataCaricamento';

PRINT 'Commenti descrittivi aggiunti con successo';
GO

-- ============================================================================
-- VERIFICA CREAZIONE
-- ============================================================================

SELECT 
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.IS_NULLABLE,
    CAST(ep.value AS NVARCHAR(500)) AS Description
FROM INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN sys.extended_properties ep 
    ON ep.major_id = OBJECT_ID('dbo.ProgettoDocumenti')
    AND ep.minor_id = c.ORDINAL_POSITION
    AND ep.name = 'MS_Description'
WHERE c.TABLE_SCHEMA = 'dbo'
AND c.TABLE_NAME = 'ProgettoDocumenti'
ORDER BY c.ORDINAL_POSITION;

-- Verifica FK
SELECT 
    fk.name AS ForeignKeyName,
    OBJECT_NAME(fk.parent_object_id) AS TableName,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ColumnName,
    OBJECT_NAME(fk.referenced_object_id) AS ReferencedTable,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ReferencedColumn
FROM sys.foreign_keys fk
INNER JOIN sys.foreign_key_columns fkc 
    ON fk.object_id = fkc.constraint_object_id
WHERE fk.parent_object_id = OBJECT_ID('dbo.ProgettoDocumenti');

-- Verifica indici
SELECT 
    i.name AS IndexName,
    i.type_desc AS IndexType,
    COL_NAME(ic.object_id, ic.column_id) AS ColumnName
FROM sys.indexes i
INNER JOIN sys.index_columns ic 
    ON i.object_id = ic.object_id 
    AND i.index_id = ic.index_id
WHERE i.object_id = OBJECT_ID('dbo.ProgettoDocumenti')
ORDER BY i.name, ic.key_ordinal;

PRINT 'Script completato con successo!';
GO
