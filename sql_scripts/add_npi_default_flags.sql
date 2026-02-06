-- Add default flags for Categories and TaskCatalogo (if missing)
IF COL_LENGTH('dbo.Categories', 'DefaultCategory') IS NULL
BEGIN
    ALTER TABLE dbo.Categories
    ADD DefaultCategory bit NOT NULL CONSTRAINT DF_Categories_DefaultCategory DEFAULT(0);
END

IF COL_LENGTH('dbo.TaskCatalogo', 'DefaultTask') IS NULL
BEGIN
    ALTER TABLE dbo.TaskCatalogo
    ADD DefaultTask bit NOT NULL CONSTRAINT DF_TaskCatalogo_DefaultTask DEFAULT(0);
END
