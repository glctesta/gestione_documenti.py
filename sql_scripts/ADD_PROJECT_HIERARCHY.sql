-- =============================================
-- Script: ADD_PROJECT_HIERARCHY.sql
-- Descrizione: Aggiunge supporto per gerarchia progetti NPI (Parent-Child)
-- Autore: Gianluca Testa
-- Data: 2026-01-21
-- Versione: 1.0
-- =============================================

USE [Traceability_RS]
GO

PRINT '=========================================='
PRINT 'INIZIO: Aggiunta gerarchia progetti NPI'
PRINT '=========================================='
PRINT ''

-- =============================================
-- 1. Aggiungi colonna ParentProjectID
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID(N'[dbo].[ProgettiNPI]') 
    AND name = 'ParentProjectID'
)
BEGIN
    PRINT '1. Aggiunta colonna ParentProjectID...'
    
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD [ParentProjectID] INT NULL;
    
    PRINT '   ✅ Colonna ParentProjectID aggiunta con successo'
END
ELSE
BEGIN
    PRINT '   ⚠️  Colonna ParentProjectID già esistente, skip'
END
PRINT ''

-- =============================================
-- 2. Aggiungi Foreign Key per ParentProjectID
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.foreign_keys 
    WHERE name = 'FK_ProgettiNPI_ParentProject'
)
BEGIN
    PRINT '2. Aggiunta Foreign Key FK_ProgettiNPI_ParentProject...'
    
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD CONSTRAINT FK_ProgettiNPI_ParentProject
        FOREIGN KEY ([ParentProjectID])
        REFERENCES [dbo].[ProgettiNPI]([ProgettoID])
        ON DELETE NO ACTION
        ON UPDATE NO ACTION;
    
    PRINT '   ✅ Foreign Key aggiunta con successo'
END
ELSE
BEGIN
    PRINT '   ⚠️  Foreign Key FK_ProgettiNPI_ParentProject già esistente, skip'
END
PRINT ''

-- =============================================
-- 3. Aggiungi indice per performance
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.indexes 
    WHERE name = 'IX_ProgettiNPI_ParentProjectID'
    AND object_id = OBJECT_ID(N'[dbo].[ProgettiNPI]')
)
BEGIN
    PRINT '3. Creazione indice IX_ProgettiNPI_ParentProjectID...'
    
    CREATE NONCLUSTERED INDEX IX_ProgettiNPI_ParentProjectID
    ON [dbo].[ProgettiNPI]([ParentProjectID])
    INCLUDE ([ProgettoID], [NomeProgetto], [StatoProgetto]);
    
    PRINT '   ✅ Indice creato con successo'
END
ELSE
BEGIN
    PRINT '   ⚠️  Indice IX_ProgettiNPI_ParentProjectID già esistente, skip'
END
PRINT ''

-- =============================================
-- 4. Aggiungi colonna HierarchyLevel
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID(N'[dbo].[ProgettiNPI]') 
    AND name = 'HierarchyLevel'
)
BEGIN
    PRINT '4. Aggiunta colonna HierarchyLevel...'
    
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD [HierarchyLevel] INT NULL DEFAULT 0;
    
    -- Inizializza tutti i progetti esistenti a livello 0
    UPDATE [dbo].[ProgettiNPI]
    SET [HierarchyLevel] = 0
    WHERE [HierarchyLevel] IS NULL;
    
    PRINT '   ✅ Colonna HierarchyLevel aggiunta e inizializzata'
END
ELSE
BEGIN
    PRINT '   ⚠️  Colonna HierarchyLevel già esistente, skip'
END
PRINT ''

-- =============================================
-- 5. Aggiungi colonna ProjectType
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.columns 
    WHERE object_id = OBJECT_ID(N'[dbo].[ProgettiNPI]') 
    AND name = 'ProjectType'
)
BEGIN
    PRINT '5. Aggiunta colonna ProjectType...'
    
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD [ProjectType] VARCHAR(50) NULL DEFAULT 'Standard';
    
    -- Inizializza tutti i progetti esistenti come 'Standard'
    UPDATE [dbo].[ProgettiNPI]
    SET [ProjectType] = 'Standard'
    WHERE [ProjectType] IS NULL;
    
    PRINT '   ✅ Colonna ProjectType aggiunta e inizializzata'
END
ELSE
BEGIN
    PRINT '   ⚠️  Colonna ProjectType già esistente, skip'
END
PRINT ''

-- =============================================
-- 6. Aggiungi constraint per evitare cicli
-- =============================================
IF NOT EXISTS (
    SELECT 1 
    FROM sys.check_constraints 
    WHERE name = 'CK_ProgettiNPI_NoCycles'
)
BEGIN
    PRINT '6. Aggiunta constraint per evitare cicli...'
    
    ALTER TABLE [dbo].[ProgettiNPI]
    ADD CONSTRAINT CK_ProgettiNPI_NoCycles
        CHECK ([ProgettoID] <> [ParentProjectID]);
    
    PRINT '   ✅ Constraint CK_ProgettiNPI_NoCycles aggiunto'
END
ELSE
BEGIN
    PRINT '   ⚠️  Constraint CK_ProgettiNPI_NoCycles già esistente, skip'
END
PRINT ''

-- =============================================
-- 7. Crea vista helper per gerarchia
-- =============================================
PRINT '7. Creazione vista vw_ProjectHierarchy...'

IF OBJECT_ID(N'[dbo].[vw_ProjectHierarchy]', 'V') IS NOT NULL
    DROP VIEW [dbo].[vw_ProjectHierarchy];
GO

CREATE VIEW [dbo].[vw_ProjectHierarchy]
AS
WITH ProjectTree AS (
    -- Anchor: Progetti root (senza padre)
    SELECT 
        p.ProgettoID,
        p.NomeProgetto,
        p.ParentProjectID,
        p.StatoProgetto,
        p.HierarchyLevel,
        p.ProjectType,
        0 AS ActualLevel,
        CAST(p.NomeProgetto AS VARCHAR(MAX)) AS HierarchyPath,
        CAST(CAST(p.ProgettoID AS VARCHAR(10)) AS VARCHAR(MAX)) AS IDPath
    FROM [dbo].[ProgettiNPI] p
    WHERE p.ParentProjectID IS NULL
    
    UNION ALL
    
    -- Recursive: Progetti figli
    SELECT 
        p.ProgettoID,
        p.NomeProgetto,
        p.ParentProjectID,
        p.StatoProgetto,
        p.HierarchyLevel,
        p.ProjectType,
        pt.ActualLevel + 1,
        CAST(pt.HierarchyPath + ' > ' + p.NomeProgetto AS VARCHAR(MAX)),
        CAST(pt.IDPath + '/' + CAST(p.ProgettoID AS VARCHAR(10)) AS VARCHAR(MAX))
    FROM [dbo].[ProgettiNPI] p
    INNER JOIN ProjectTree pt ON p.ParentProjectID = pt.ProgettoID
)
SELECT 
    ProgettoID,
    NomeProgetto,
    ParentProjectID,
    StatoProgetto,
    HierarchyLevel,
    ProjectType,
    ActualLevel,
    HierarchyPath,
    IDPath,
    REPLICATE('  ', ActualLevel) + NomeProgetto AS IndentedName
FROM ProjectTree;
GO

PRINT '   ✅ Vista vw_ProjectHierarchy creata con successo'
PRINT ''

-- =============================================
-- 8. Crea funzione helper per verificare completamento
-- =============================================
PRINT '8. Creazione funzione fn_AreAllChildrenCompleted...'

IF OBJECT_ID(N'[dbo].[fn_AreAllChildrenCompleted]', 'FN') IS NOT NULL
    DROP FUNCTION [dbo].[fn_AreAllChildrenCompleted];
GO

CREATE FUNCTION [dbo].[fn_AreAllChildrenCompleted]
(
    @ProgettoID INT
)
RETURNS BIT
AS
BEGIN
    DECLARE @AllCompleted BIT = 1;
    
    -- Verifica se ci sono figli non completati
    IF EXISTS (
        SELECT 1 
        FROM [dbo].[ProgettiNPI] 
        WHERE ParentProjectID = @ProgettoID 
        AND StatoProgetto != 'Completato'
    )
    BEGIN
        SET @AllCompleted = 0;
    END
    
    RETURN @AllCompleted;
END
GO

PRINT '   ✅ Funzione fn_AreAllChildrenCompleted creata con successo'
PRINT ''

-- =============================================
-- 9. Crea stored procedure per validazione completamento
-- =============================================
PRINT '9. Creazione stored procedure sp_ValidateProjectCompletion...'

IF OBJECT_ID(N'[dbo].[sp_ValidateProjectCompletion]', 'P') IS NOT NULL
    DROP PROCEDURE [dbo].[sp_ValidateProjectCompletion];
GO

CREATE PROCEDURE [dbo].[sp_ValidateProjectCompletion]
    @ProgettoID INT,
    @CanComplete BIT OUTPUT,
    @Message NVARCHAR(500) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ChildCount INT;
    DECLARE @CompletedChildCount INT;
    
    -- Conta i progetti figli
    SELECT @ChildCount = COUNT(*)
    FROM [dbo].[ProgettiNPI]
    WHERE ParentProjectID = @ProgettoID;
    
    -- Conta i progetti figli completati
    SELECT @CompletedChildCount = COUNT(*)
    FROM [dbo].[ProgettiNPI]
    WHERE ParentProjectID = @ProgettoID
    AND StatoProgetto = 'Completato';
    
    -- Verifica
    IF @ChildCount = 0
    BEGIN
        -- Nessun figlio, può essere completato
        SET @CanComplete = 1;
        SET @Message = 'Il progetto può essere completato (nessun progetto figlio)';
    END
    ELSE IF @ChildCount = @CompletedChildCount
    BEGIN
        -- Tutti i figli sono completati
        SET @CanComplete = 1;
        SET @Message = 'Il progetto può essere completato (tutti i ' + CAST(@ChildCount AS NVARCHAR(10)) + ' progetti figli sono completati)';
    END
    ELSE
    BEGIN
        -- Ci sono figli non completati
        SET @CanComplete = 0;
        SET @Message = 'Il progetto NON può essere completato: ' + 
                      CAST(@ChildCount - @CompletedChildCount AS NVARCHAR(10)) + 
                      ' progetti figli su ' + CAST(@ChildCount AS NVARCHAR(10)) + 
                      ' non sono ancora completati';
    END
END
GO

PRINT '   ✅ Stored procedure sp_ValidateProjectCompletion creata con successo'
PRINT ''

-- =============================================
-- 10. Test di verifica
-- =============================================
PRINT '=========================================='
PRINT 'VERIFICA FINALE'
PRINT '=========================================='

-- Conta progetti esistenti
DECLARE @TotalProjects INT;
SELECT @TotalProjects = COUNT(*) FROM [dbo].[ProgettiNPI];
PRINT 'Progetti totali nel database: ' + CAST(@TotalProjects AS NVARCHAR(10));

-- Conta progetti root
DECLARE @RootProjects INT;
SELECT @RootProjects = COUNT(*) FROM [dbo].[ProgettiNPI] WHERE ParentProjectID IS NULL;
PRINT 'Progetti root (senza padre): ' + CAST(@RootProjects AS NVARCHAR(10));

-- Conta progetti figli
DECLARE @ChildProjects INT;
SELECT @ChildProjects = COUNT(*) FROM [dbo].[ProgettiNPI] WHERE ParentProjectID IS NOT NULL;
PRINT 'Progetti figli (con padre): ' + CAST(@ChildProjects AS NVARCHAR(10));

PRINT ''
PRINT '=========================================='
PRINT '✅ COMPLETATO CON SUCCESSO!'
PRINT '=========================================='
PRINT ''
PRINT 'Modifiche applicate:'
PRINT '  ✅ Colonna ParentProjectID'
PRINT '  ✅ Colonna HierarchyLevel'
PRINT '  ✅ Colonna ProjectType'
PRINT '  ✅ Foreign Key e Constraints'
PRINT '  ✅ Indice per performance'
PRINT '  ✅ Vista vw_ProjectHierarchy'
PRINT '  ✅ Funzione fn_AreAllChildrenCompleted'
PRINT '  ✅ Stored procedure sp_ValidateProjectCompletion'
PRINT ''
PRINT 'La gerarchia progetti NPI è ora attiva!'
PRINT ''

-- Query di esempio
PRINT '=========================================='
PRINT 'QUERY DI ESEMPIO'
PRINT '=========================================='
PRINT ''
PRINT '-- Visualizza tutti i progetti con la loro gerarchia:'
PRINT 'SELECT * FROM [dbo].[vw_ProjectHierarchy] ORDER BY HierarchyPath;'
PRINT ''
PRINT '-- Verifica se un progetto può essere completato:'
PRINT 'DECLARE @CanComplete BIT, @Message NVARCHAR(500);'
PRINT 'EXEC sp_ValidateProjectCompletion @ProgettoID = 1, @CanComplete = @CanComplete OUTPUT, @Message = @Message OUTPUT;'
PRINT 'SELECT @CanComplete AS CanComplete, @Message AS Message;'
PRINT ''

GO
