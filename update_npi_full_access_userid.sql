-- Aggiorna il setting Npi_full_acces con l'UserID corretto (26 invece di 2086)
-- Database: Traceability_RS

USE [Traceability_RS]
GO

-- Aggiorna il valore
UPDATE [dbo].[settings]
SET [value] = '26;1930'
WHERE [atribute] = 'Npi_full_acces';

-- Verifica
SELECT [IDSettings], [Atribute], [Value], [Name]
FROM [dbo].[settings]
WHERE [atribute] = 'Npi_full_acces';

PRINT '✅ Setting aggiornato: UserID 2086 → 26';

GO
