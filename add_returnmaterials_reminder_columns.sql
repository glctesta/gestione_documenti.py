-- add_returnmaterials_reminder_columns.sql
-- Colonne per il sollecito di validazione scorie/rientri (>8 ore pendenti):
--   DateCreated    = timestamp preciso di creazione (DateReturn e' solo DATE, non basta
--                    per la soglia "pendente da > N ore")
--   ReminderSentAt = ultimo sollecito inviato (claim atomico anti-duplicato, cross-PC)
-- Idempotente.

-- 1) colonna nullable SENZA default: le righe esistenti restano NULL (non se ne resetta l'eta')
IF COL_LENGTH('dbo.ReturnMaterials', 'DateCreated') IS NULL
    ALTER TABLE dbo.ReturnMaterials ADD DateCreated DATETIME NULL;
GO

-- 2) backfill righe esistenti dalla data dichiarazione (mezzanotte), coerente con l'eta' reale
UPDATE dbo.ReturnMaterials
SET DateCreated = CAST(DateReturn AS DATETIME)
WHERE DateCreated IS NULL;
GO

-- 3) default per gli inserimenti futuri (l'INSERT dell'app non elenca DateCreated)
IF NOT EXISTS (SELECT 1 FROM sys.default_constraints WHERE name = 'DF_ReturnMaterials_DateCreated')
    ALTER TABLE dbo.ReturnMaterials
        ADD CONSTRAINT DF_ReturnMaterials_DateCreated DEFAULT GETDATE() FOR DateCreated;
GO

IF COL_LENGTH('dbo.ReturnMaterials', 'ReminderSentAt') IS NULL
    ALTER TABLE dbo.ReturnMaterials ADD ReminderSentAt DATETIME NULL;
GO
