-- Script per verificare e creare il setting Npi_full_access
-- Database: Traceability_RS

USE [Traceability_RS]
GO

-- 1. Verifica se il setting esiste
SELECT [atribute], [value]
FROM [dbo].[settings]
WHERE [atribute] = 'Npi_full_access';

-- 2. Se non esiste, crealo con l'UserID 2086 (Gianluca Testa)
IF NOT EXISTS (SELECT 1 FROM [dbo].[settings] WHERE [atribute] = 'Npi_full_access')
BEGIN
    INSERT INTO [dbo].[settings] ([atribute], [value])
    VALUES ('Npi_full_access', '2086');
    
    PRINT '✅ Setting Npi_full_access creato con UserID 2086';
END
ELSE
BEGIN
    -- Se esiste, verifica se contiene 2086
    DECLARE @current_value NVARCHAR(MAX);
    SELECT @current_value = [value] FROM [dbo].[settings] WHERE [atribute] = 'Npi_full_access';
    
    IF @current_value NOT LIKE '%2086%'
    BEGIN
        -- Aggiungi 2086 al valore esistente
        UPDATE [dbo].[settings]
        SET [value] = @current_value + ';2086'
        WHERE [atribute] = 'Npi_full_access';
        
        PRINT '✅ UserID 2086 aggiunto al setting Npi_full_access';
    END
    ELSE
    BEGIN
        PRINT 'ℹ️ UserID 2086 già presente nel setting Npi_full_access';
    END
END

-- 3. Verifica finale
SELECT [atribute], [value]
FROM [dbo].[settings]
WHERE [atribute] = 'Npi_full_access';

-- 4. Verifica che l'utente esista nella tabella Soggetto
SELECT [SoggettoId], [Nome], [Email]
FROM [dbo].[Soggetto]
WHERE [SoggettoId] = 2086;

GO
