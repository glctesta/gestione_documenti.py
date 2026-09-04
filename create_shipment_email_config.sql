-- Tabella di configurazione per il servizio "Info Spedizioni":
-- accoppia 1-1 un sito (dbo.Sites) alla sua directory su \\192.168.10.110\Shipping
-- e memorizza i destinatari TO / CC delle email automatiche.
-- DateOut NULL = record corrente e valido; DateOut valorizzato = storico.
-- Eseguire una volta sola come amministratore del DB.

USE Traceability_RS;
GO

IF OBJECT_ID('dbo.ShipmentEmailConfig', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ShipmentEmailConfig (
        ConfigId      INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IDSite        INT               NOT NULL,
        DirectoryName NVARCHAR(200)     NOT NULL,
        ToEmails      NVARCHAR(MAX)     NULL,
        CcEmails      NVARCHAR(MAX)     NULL,
        IsActive      BIT               NOT NULL DEFAULT 1,
        [User]        NVARCHAR(100)     NULL,
        DateIn        DATETIME          NOT NULL DEFAULT GETDATE(),
        DateOut       DATETIME          NULL,
        CONSTRAINT FK_ShipmentEmailConfig_Sites
            FOREIGN KEY (IDSite) REFERENCES dbo.Sites (IDSite)
    );
END
GO

-- Un solo record attivo per sito (rapporto 1-1)
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'UX_ShipmentEmailConfig_IDSite_Active'
                 AND object_id = OBJECT_ID('dbo.ShipmentEmailConfig'))
BEGIN
    CREATE UNIQUE NONCLUSTERED INDEX UX_ShipmentEmailConfig_IDSite_Active
    ON dbo.ShipmentEmailConfig (IDSite)
    WHERE DateOut IS NULL;
END
GO

-- Tabella anti-duplicati: un file (per sito) registrato qui NON verra' MAI riproposto,
-- indipendentemente dalla rename. Status: SENT = email inviata, ERROR = invio fallito.
IF OBJECT_ID('dbo.ShipmentProcessedFiles', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ShipmentProcessedFiles (
        ProcessedFileId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IDSite          INT               NOT NULL,
        FileName        NVARCHAR(300)     NOT NULL,
        Status          VARCHAR(20)       NOT NULL DEFAULT 'SENT',
        SentTo          NVARCHAR(MAX)     NULL,
        ErrorMessage    NVARCHAR(500)     NULL,
        ProcessedAt     DATETIME          NOT NULL DEFAULT GETDATE(),
        CONSTRAINT UQ_ShipmentProcessedFiles_Site_File UNIQUE (IDSite, FileName)
    );
END
GO
