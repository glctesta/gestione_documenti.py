-- add_returnmaterials_override_columns.sql
-- Colonne di audit per l'azione "Forza conforme" (override supervisore) delle
-- scorie/rientri: sblocco di una riga NON conforme (IsOk=0) tracciando chi/perche'/quando.
-- Idempotente. Eseguire sul DB applicativo (dbo.ReturnMaterials).

IF COL_LENGTH('dbo.ReturnMaterials', 'OverrideBy') IS NULL
    ALTER TABLE dbo.ReturnMaterials ADD OverrideBy NVARCHAR(150) NULL;

IF COL_LENGTH('dbo.ReturnMaterials', 'OverrideReason') IS NULL
    ALTER TABLE dbo.ReturnMaterials ADD OverrideReason NVARCHAR(400) NULL;

IF COL_LENGTH('dbo.ReturnMaterials', 'OverrideDate') IS NULL
    ALTER TABLE dbo.ReturnMaterials ADD OverrideDate DATETIME NULL;
GO
