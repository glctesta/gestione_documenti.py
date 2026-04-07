-- Aggiunge la colonna SentEmailToManagement alla tabella Visitors
-- per tracciare se l'email di notifica al management è stata inviata.
-- Eseguire una sola volta.

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'dbo' 
      AND TABLE_NAME = 'Visitors' 
      AND COLUMN_NAME = 'SentEmailToManagement'
      AND TABLE_CATALOG = 'Employee'
)
BEGIN
    ALTER TABLE Employee.dbo.Visitors
    ADD SentEmailToManagement BIT NULL DEFAULT 0;
    PRINT 'Colonna SentEmailToManagement aggiunta con successo.';
END
ELSE
BEGIN
    PRINT 'Colonna SentEmailToManagement già esistente.';
END
GO
