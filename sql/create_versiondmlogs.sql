-- Tabella per la sintesi (changelog) delle modifiche/aggiunte per versione.
-- Mostrata all'utente (popup una volta dopo l'update + viewer LIFO da Help/About).
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
    WHERE s.name = 'dbo' AND t.name = 'VersionDMLogs'
)
BEGIN
    CREATE TABLE traceability_rs.dbo.VersionDMLogs (
        VersionDMLogId INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_VersionDMLogs PRIMARY KEY,
        NameProgram    NVARCHAR(100)  NOT NULL,
        Version        NVARCHAR(10)   NOT NULL,
        Summary        NVARCHAR(MAX)  NOT NULL,
        CreatedAt      DATETIME       NOT NULL
            CONSTRAINT DF_VersionDMLogs_CreatedAt DEFAULT (GETDATE()),
        CreatedBy      NVARCHAR(150)  NULL,
        DateOut        DATETIME       NULL   -- soft delete
    );

    CREATE INDEX IX_VersionDMLogs_Program_Created
        ON traceability_rs.dbo.VersionDMLogs (NameProgram, CreatedAt DESC);
END
