-- Script SQL per creare la tabella EquipmentFixtureDocuments
-- Tabella per gestire i documenti di manutenzione delle fixture

USE [Traceability_RS];
GO

-- Crea la tabella per i documenti delle fixture
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'EquipmentFixtureDocuments' AND schema_id = SCHEMA_ID('eqp'))
BEGIN
    CREATE TABLE [eqp].[EquipmentFixtureDocuments] (
        [FixtureDocumentId] INT IDENTITY(1,1) PRIMARY KEY,
        [EquipmentFixtureRuleId] INT NOT NULL,
        [DocumentName] NVARCHAR(255) NOT NULL,
        [DocumentPath] NVARCHAR(500) NOT NULL,
        [DocumentType] NVARCHAR(10) NOT NULL CHECK (DocumentType IN ('docx', 'pdf', 'xlsx', 'txt')),
        [Revision] NVARCHAR(50) NULL,
        [CreatedDate] DATETIME NOT NULL DEFAULT GETDATE(),
        [CreatedBy] NVARCHAR(100) NOT NULL,
        [ApprovedBy] NVARCHAR(100) NULL,
        [ApprovedDate] DATETIME NULL,
        [Notes] NVARCHAR(MAX) NULL,
        
        -- Foreign key constraint
        CONSTRAINT FK_FixtureDocuments_FixtureRules 
            FOREIGN KEY ([EquipmentFixtureRuleId]) 
            REFERENCES [eqp].[EquipmentFixtureRules]([EquipmentFixtureRuleId])
            ON DELETE CASCADE
    );
    
    PRINT 'Tabella eqp.EquipmentFixtureDocuments creata con successo';
END
ELSE
BEGIN
    PRINT 'Tabella eqp.EquipmentFixtureDocuments già esistente';
END
GO

-- Crea indici per migliorare le performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_FixtureDocuments_RuleId' AND object_id = OBJECT_ID('eqp.EquipmentFixtureDocuments'))
BEGIN
    CREATE INDEX IX_FixtureDocuments_RuleId 
    ON [eqp].[EquipmentFixtureDocuments]([EquipmentFixtureRuleId]);
    
    PRINT 'Indice IX_FixtureDocuments_RuleId creato con successo';
END
GO

-- Rimuovi la colonna MaintenanceDocument dalla tabella EquipmentFixtureRules se esiste
IF EXISTS (SELECT * FROM sys.columns 
           WHERE object_id = OBJECT_ID('eqp.EquipmentFixtureRules') 
           AND name = 'MaintenanceDocument')
BEGIN
    ALTER TABLE [eqp].[EquipmentFixtureRules]
    DROP COLUMN [MaintenanceDocument];
    
    PRINT 'Colonna MaintenanceDocument rimossa da eqp.EquipmentFixtureRules';
END
GO

-- Query di esempio per verificare la struttura
PRINT '';
PRINT 'Struttura tabella EquipmentFixtureDocuments:';
EXEC sp_help 'eqp.EquipmentFixtureDocuments';
GO

PRINT '';
PRINT '=== Script completato con successo ===';
PRINT 'Tabella: eqp.EquipmentFixtureDocuments';
PRINT 'Campi:';
PRINT '  - FixtureDocumentId (PK, IDENTITY)';
PRINT '  - EquipmentFixtureRuleId (FK)';
PRINT '  - DocumentName (nome file)';
PRINT '  - DocumentPath (percorso completo)';
PRINT '  - DocumentType (docx, pdf, xlsx, txt)';
PRINT '  - Revision (numero revisione)';
PRINT '  - CreatedDate (data creazione)';
PRINT '  - CreatedBy (utente creatore)';
PRINT '  - ApprovedBy (utente approvatore)';
PRINT '  - ApprovedDate (data approvazione)';
PRINT '  - Notes (note aggiuntive)';
GO
