/*
Seed dichiarazioni operatore per template SMT.

Prerequisito:
- Eseguire prima: add_fai_template_declarations.sql

Questo script:
1) individua il template SMT reale in fai.FaiTemplates
2) chiude eventuali override SMT precedenti (DateOut)
3) inserisce le 5 dichiarazioni operatore per SMT

Compatibilita':
- Non modifica il template PTHM esistente.
- Agisce solo su fai.FaiTemplateDeclarations del template SMT selezionato.
*/

USE [Traceability_RS];
GO

SET NOCOUNT ON;

/*
Se la tabella di configurazione non esiste, la crea.
Questo evita dipendenza obbligatoria da add_fai_template_declarations.sql.
*/
IF NOT EXISTS (
    SELECT 1
    FROM sys.objects
    WHERE object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
      AND type = N'U'
)
BEGIN
    CREATE TABLE [fai].[FaiTemplateDeclarations](
        [FaiTemplateDeclarationId] INT IDENTITY(1,1) NOT NULL,
        [FaiTemplateId] SMALLINT NULL,
        [DeclarationKey] NVARCHAR(64) NOT NULL,
        [DeclarationLabel] NVARCHAR(200) NOT NULL,
        [DisplayOrder] INT NOT NULL CONSTRAINT [DF_FaiTemplateDeclarations_DisplayOrder] DEFAULT (1),
        [DateIn] DATETIME NOT NULL CONSTRAINT [DF_FaiTemplateDeclarations_DateIn] DEFAULT (GETDATE()),
        [DateOut] DATETIME NULL,
        CONSTRAINT [PK_FaiTemplateDeclarations] PRIMARY KEY CLUSTERED ([FaiTemplateDeclarationId] ASC)
    );
END

/*
Se la tabella esiste già ma FaiTemplateId non è SMALLINT, lo converte.
*/
IF EXISTS (
    SELECT 1
    FROM sys.columns c
    INNER JOIN sys.types ty ON c.user_type_id = ty.user_type_id
    WHERE c.object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
      AND c.name = 'FaiTemplateId'
      AND ty.name <> 'smallint'
)
BEGIN
    IF EXISTS (
        SELECT 1
        FROM [fai].[FaiTemplateDeclarations]
        WHERE [FaiTemplateId] IS NOT NULL
          AND ([FaiTemplateId] < -32768 OR [FaiTemplateId] > 32767)
    )
    BEGIN
        RAISERROR('Conversione FaiTemplateId a SMALLINT impossibile: valori fuori range.', 16, 1);
        RETURN;
    END

    IF EXISTS (
        SELECT 1
        FROM sys.foreign_keys
        WHERE name = 'FK_FaiTemplateDeclarations_FaiTemplates'
          AND parent_object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
    )
    BEGIN
        ALTER TABLE [fai].[FaiTemplateDeclarations]
        DROP CONSTRAINT [FK_FaiTemplateDeclarations_FaiTemplates];
    END

    ALTER TABLE [fai].[FaiTemplateDeclarations]
    ALTER COLUMN [FaiTemplateId] SMALLINT NULL;
END

IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FaiTemplateDeclarations_FaiTemplates'
      AND parent_object_id = OBJECT_ID(N'[fai].[FaiTemplateDeclarations]')
)
BEGIN
    ALTER TABLE [fai].[FaiTemplateDeclarations]
    WITH CHECK ADD CONSTRAINT [FK_FaiTemplateDeclarations_FaiTemplates]
        FOREIGN KEY ([FaiTemplateId]) REFERENCES [fai].[FaiTemplates]([FaiTemplateId]);
END

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

DECLARE @SmtTemplateId INT;

/*
Ricerca template SMT:
- Priorita' 1: NrDocument = MD.RST.002
- Priorita' 2: titolo che contiene SMT
Sceglie il piu' recente per RevisionDate/FaiTemplateId.
*/
SELECT TOP 1
    @SmtTemplateId = t.FaiTemplateId
FROM [fai].[FaiTemplates] t
WHERE t.NrDocument = 'MD.RST.002'
ORDER BY ISNULL(t.RevisionDate, '19000101') DESC, t.FaiTemplateId DESC;

IF @SmtTemplateId IS NULL
BEGIN
    SELECT TOP 1
        @SmtTemplateId = t.FaiTemplateId
    FROM [fai].[FaiTemplates] t
    WHERE UPPER(ISNULL(t.FaiTitle, '')) LIKE '%SMT%'
    ORDER BY ISNULL(t.RevisionDate, '19000101') DESC, t.FaiTemplateId DESC;
END

IF @SmtTemplateId IS NULL
BEGIN
    RAISERROR('Template SMT non trovato. Verificare fai.FaiTemplates (NrDocument/FaiTitle).', 16, 1);
    RETURN;
END

PRINT CONCAT('Template SMT individuato: FaiTemplateId=', @SmtTemplateId);

BEGIN TRY
    BEGIN TRAN;

    -- Chiude override attivi precedenti per SMT
    UPDATE [fai].[FaiTemplateDeclarations]
    SET DateOut = GETDATE()
    WHERE FaiTemplateId = @SmtTemplateId
      AND DateOut IS NULL;

    -- Inserisce override SMT (etichette dichiarazioni operatore)
    INSERT INTO [fai].[FaiTemplateDeclarations]
        ([FaiTemplateId], [DeclarationKey], [DeclarationLabel], [DisplayOrder])
    VALUES
        (@SmtTemplateId, 'NPI', 'NPI (PRESERIE)', 1),
        (@SmtTemplateId, 'Test', 'TEST', 2),
        (@SmtTemplateId, 'PRODUCTION', 'PRODUCȚIE', 3),
        (@SmtTemplateId, 'StandardProcessDeviation', 'VARIAȚIA STANDARD A PROCESULUI', 4),
        (@SmtTemplateId, 'Others', 'ALTELE', 5);

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRAN;

    DECLARE @ErrMsg NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @ErrNum INT = ERROR_NUMBER();
    RAISERROR('Errore seed SMT [%d]: %s', 16, 1, @ErrNum, @ErrMsg);
    RETURN;
END CATCH;

-- Verifica finale
SELECT
    d.FaiTemplateDeclarationId,
    d.FaiTemplateId,
    d.DeclarationKey,
    d.DeclarationLabel,
    d.DisplayOrder,
    d.DateIn,
    d.DateOut
FROM [fai].[FaiTemplateDeclarations] d
WHERE d.FaiTemplateId = @SmtTemplateId
  AND d.DateOut IS NULL
ORDER BY d.DisplayOrder, d.FaiTemplateDeclarationId;
GO
