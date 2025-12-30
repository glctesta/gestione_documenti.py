-- Script SQL per aggiungere i campi Owner e Descrizione alla tabella ProgettiNPI
-- Database: Traceability_rs
-- Tabella: dbo.ProgettiNPI

USE Traceability_rs;
GO

-- ============================================================================
-- AGGIUNGI CAMPO DESCRIZIONE
-- ============================================================================

IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID('dbo.ProgettiNPI') 
    AND name = 'Descrizione'
)
BEGIN
    ALTER TABLE dbo.ProgettiNPI
    ADD Descrizione NVARCHAR(MAX) NULL;
    
    PRINT 'Campo Descrizione aggiunto con successo';
END
ELSE
BEGIN
    PRINT 'Campo Descrizione già esistente';
END
GO

-- ============================================================================
-- AGGIUNGI CAMPO OWNERID
-- ============================================================================

IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID('dbo.ProgettiNPI') 
    AND name = 'OwnerID'
)
BEGIN
    ALTER TABLE dbo.ProgettiNPI
    ADD OwnerID INT NULL;
    
    PRINT 'Campo OwnerID aggiunto con successo';
END
ELSE
BEGIN
    PRINT 'Campo OwnerID già esistente';
END
GO

-- ============================================================================
-- AGGIUNGI FOREIGN KEY CONSTRAINT (Opzionale ma consigliato)
-- ============================================================================

-- Nota: vw_Soggetti è una VIEW, quindi la FK non può essere creata direttamente
-- Se esiste una tabella base per i soggetti, usa quella invece

-- Esempio se esiste una tabella Soggetti:
/*
IF NOT EXISTS (
    SELECT 1 
    FROM sys.foreign_keys 
    WHERE name = 'FK_ProgettiNPI_Owner'
)
BEGIN
    ALTER TABLE dbo.ProgettiNPI
    ADD CONSTRAINT FK_ProgettiNPI_Owner 
    FOREIGN KEY (OwnerID) REFERENCES dbo.Soggetti(SoggettoId);
    
    PRINT 'Foreign Key FK_ProgettiNPI_Owner creata con successo';
END
ELSE
BEGIN
    PRINT 'Foreign Key FK_ProgettiNPI_Owner già esistente';
END
GO
*/

-- ============================================================================
-- AGGIUNGI COMMENTI DESCRITTIVI
-- ============================================================================

IF NOT EXISTS (
    SELECT 1 
    FROM sys.extended_properties 
    WHERE major_id = OBJECT_ID('dbo.ProgettiNPI') 
    AND minor_id = (SELECT column_id FROM sys.columns WHERE object_id = OBJECT_ID('dbo.ProgettiNPI') AND name = 'Descrizione')
    AND name = 'MS_Description'
)
BEGIN
    EXEC sp_addextendedproperty 
        @name = N'MS_Description', 
        @value = N'Descrizione dettagliata del progetto NPI', 
        @level0type = N'SCHEMA', @level0name = 'dbo',
        @level1type = N'TABLE',  @level1name = 'ProgettiNPI',
        @level2type = N'COLUMN', @level2name = 'Descrizione';
    
    PRINT 'Commento per Descrizione aggiunto';
END
GO

IF NOT EXISTS (
    SELECT 1 
    FROM sys.extended_properties 
    WHERE major_id = OBJECT_ID('dbo.ProgettiNPI') 
    AND minor_id = (SELECT column_id FROM sys.columns WHERE object_id = OBJECT_ID('dbo.ProgettiNPI') AND name = 'OwnerID')
    AND name = 'MS_Description'
)
BEGIN
    EXEC sp_addextendedproperty 
        @name = N'MS_Description', 
        @value = N'ID del responsabile/owner del progetto (FK a vw_Soggetti)', 
        @level0type = N'SCHEMA', @level0name = 'dbo',
        @level1type = N'TABLE',  @level1name = 'ProgettiNPI',
        @level2type = N'COLUMN', @level2name = 'OwnerID';
    
    PRINT 'Commento per OwnerID aggiunto';
END
GO

-- ============================================================================
-- VERIFICA MODIFICHE
-- ============================================================================

SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME = 'ProgettiNPI'
AND COLUMN_NAME IN ('Descrizione', 'OwnerID')
ORDER BY ORDINAL_POSITION;

PRINT 'Script completato con successo!';
GO
