/*
Tabella di appoggio per dichiarazioni operatore in base al template FAI.

Obiettivo:
- Mantenere invariata la logica storica (5 flag in FaiLogHeathers).
- Permettere etichette diverse per template (es. PTHM vs SMT) senza cambiare la form.

Regole:
- FaiTemplateId NULL = configurazione default.
- FaiTemplateId valorizzato = override per uno specifico template.
- DeclarationKey deve essere uno tra:
  NPI, Test, PRODUCTION, StandardProcessDeviation, Others
*/

USE [Traceability_RS];
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.objects
    WHERE object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
      AND type = N'U'
)
BEGIN
    CREATE TABLE [fai].[FaiTemplateDeclarations](
        [FaiTemplateDeclarationId] INT IDENTITY(1,1) NOT NULL,
        [FaiTemplateId] INT NULL,
        [DeclarationKey] NVARCHAR(64) NOT NULL,
        [DeclarationLabel] NVARCHAR(200) NOT NULL,
        [DisplayOrder] INT NOT NULL CONSTRAINT [DF_FaiTemplateDeclarations_DisplayOrder] DEFAULT (1),
        [DateIn] DATETIME NOT NULL CONSTRAINT [DF_FaiTemplateDeclarations_DateIn] DEFAULT (GETDATE()),
        [DateOut] DATETIME NULL,
        CONSTRAINT [PK_FaiTemplateDeclarations] PRIMARY KEY CLUSTERED ([FaiTemplateDeclarationId] ASC)
    );

    ALTER TABLE [fai].[FaiTemplateDeclarations]
    ADD CONSTRAINT [FK_FaiTemplateDeclarations_FaiTemplates]
        FOREIGN KEY ([FaiTemplateId]) REFERENCES [fai].[FaiTemplates]([FaiTemplateId]);
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.check_constraints
    WHERE name = 'CK_FaiTemplateDeclarations_DeclarationKey'
      AND parent_object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
)
BEGIN
    ALTER TABLE [fai].[FaiTemplateDeclarations]
    ADD CONSTRAINT [CK_FaiTemplateDeclarations_DeclarationKey]
    CHECK ([DeclarationKey] IN ('NPI', 'Test', 'PRODUCTION', 'StandardProcessDeviation', 'Others'));
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_FaiTemplateDeclarations_Template_DateOut'
      AND object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
)
BEGIN
    CREATE NONCLUSTERED INDEX [IX_FaiTemplateDeclarations_Template_DateOut]
        ON [fai].[FaiTemplateDeclarations]([FaiTemplateId], [DateOut], [DisplayOrder]);
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM [fai].[FaiTemplateDeclarations]
    WHERE [FaiTemplateId] IS NULL
      AND [DateOut] IS NULL
)
BEGIN
    INSERT INTO [fai].[FaiTemplateDeclarations]
        ([FaiTemplateId], [DeclarationKey], [DeclarationLabel], [DisplayOrder])
    VALUES
        (NULL, 'NPI', 'NPI (PRESERIE)', 1),
        (NULL, 'Test', 'TEST', 2),
        (NULL, 'PRODUCTION', 'PRODUCȚIE', 3),
        (NULL, 'StandardProcessDeviation', 'VARIAȚIA STANDARD A PROCESULUI', 4),
        (NULL, 'Others', 'Others', 5);
END
GO

/*
Esempio override per template SMT (adattare la clausola WHERE al template corretto):

DECLARE @SmtTemplateId INT;
SELECT TOP 1 @SmtTemplateId = FaiTemplateId
FROM [fai].[FaiTemplates]
WHERE NrDocument = 'MD.RST.002'
ORDER BY FaiTemplateId DESC;

-- Chiudi eventuali override precedenti
UPDATE [fai].[FaiTemplateDeclarations]
SET DateOut = GETDATE()
WHERE FaiTemplateId = @SmtTemplateId
  AND DateOut IS NULL;

-- Inserisci etichette specifiche SMT
INSERT INTO [fai].[FaiTemplateDeclarations]
    ([FaiTemplateId], [DeclarationKey], [DeclarationLabel], [DisplayOrder])
VALUES
    (@SmtTemplateId, 'NPI', 'NPI (PRESERIE)', 1),
    (@SmtTemplateId, 'Test', 'TEST', 2),
    (@SmtTemplateId, 'PRODUCTION', 'PRODUCȚIE', 3),
    (@SmtTemplateId, 'StandardProcessDeviation', 'VARIAȚIA STANDARD A PROCESULUI', 4),
    (@SmtTemplateId, 'Others', 'ALTELE', 5);
*/
