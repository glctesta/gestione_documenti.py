-- =============================================
-- Stored Procedure Helper per GetManagerID
-- Questa SP accetta un singolo EmployeeHireHistoryId
-- e chiama GetManagerID con il tipo corretto
-- =============================================

USE [Employee]
GO

IF OBJECT_ID('dbo.GetManagerForSingleEmployee', 'P') IS NOT NULL
    DROP PROCEDURE dbo.GetManagerForSingleEmployee;
GO

CREATE PROCEDURE dbo.GetManagerForSingleEmployee
    @EmployeeHireHistoryId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Dichiara la variabile del tipo corretto
    DECLARE @Ids dbo.EmployeeIdTableType;
    
    -- Inserisce il singolo ID
    INSERT INTO @Ids (EmployeeHireHistoryId)
    VALUES (@EmployeeHireHistoryId);
    
    -- Crea temp table per i risultati
    IF OBJECT_ID('tempdb..#ManagerResults') IS NOT NULL
        DROP TABLE #ManagerResults;
        
    CREATE TABLE #ManagerResults (
        EmployeeHireHistoryId INT
    );
    
    -- Chiama la stored procedure originale
    INSERT INTO #ManagerResults (EmployeeHireHistoryId)
    EXEC dbo.GetManagerID @Ids;
    
    -- Restituisce i risultati
    SELECT EmployeeHireHistoryId 
    FROM #ManagerResults
    WHERE EmployeeHireHistoryId IS NOT NULL;
    
    -- Pulizia
    DROP TABLE #ManagerResults;
END
GO

PRINT 'Stored Procedure GetManagerForSingleEmployee creata con successo!'
GO

-- Test (opzionale - commentato)
-- EXEC dbo.GetManagerForSingleEmployee @EmployeeHireHistoryId = 2086;
