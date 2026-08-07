-- Tabelle per il modulo Etichette Produzione
-- Eseguire su Traceability_RS

-- Sessioni web per l'accesso dalle pagine di DocumentManagement
IF OBJECT_ID('Traceability_RS.ind.PrintLabelWebSessions', 'U') IS NULL
CREATE TABLE Traceability_RS.ind.PrintLabelWebSessions (
    Token NVARCHAR(64) NOT NULL PRIMARY KEY,
    UserId INT NOT NULL,
    UserName NVARCHAR(255) NOT NULL,
    Permission NVARCHAR(255) NOT NULL,
    Page NVARCHAR(50) NOT NULL,
    IssuedAt DATETIME NOT NULL DEFAULT GETDATE(),
    ExpiresAt DATETIME NOT NULL,
    UsedAt DATETIME NULL,
    ClientIP NVARCHAR(50) NULL
);
GO

-- Stampanti configurate per la stampa etichette
IF OBJECT_ID('Traceability_RS.ind.LabelPrinters', 'U') IS NULL
CREATE TABLE Traceability_RS.ind.LabelPrinters (
    LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
    PrinterName NVARCHAR(255) NOT NULL,
    PrinterType NVARCHAR(50) NOT NULL,
    ConnectionString NVARCHAR(500),
    PrinterIP NVARCHAR(50),
    PrinterPort INT,
    PrinterLocation NVARCHAR(255),
    PrinterModel NVARCHAR(100),
    LastRevisionDate DATETIME NULL,
    IsDefault BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL
);
GO

-- Associazione Label <-> Ribbon
IF OBJECT_ID('Traceability_RS.dbo.LinkedMaterials', 'U') IS NULL
CREATE TABLE Traceability_RS.dbo.LinkedMaterials (
    LinkedMaterialId INT IDENTITY(1,1) PRIMARY KEY,
    LabelId INT NOT NULL,
    RibbonId INT NOT NULL,
    dateout DATETIME NULL,
    dateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);
GO

-- Associazione Label <-> Stampante (stampa attiva per etichetta)
IF OBJECT_ID('Traceability_RS.dbo.LabelPrinterAssociations', 'U') IS NULL
CREATE TABLE Traceability_RS.dbo.LabelPrinterAssociations (
    LabelPrinterAssociationId INT IDENTITY(1,1) PRIMARY KEY,
    LabelId INT NOT NULL,
    LabelPrinterId INT NOT NULL,
    dateout DATETIME NULL,
    dateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);
GO

-- Script da inviare alla stampante per ogni accoppiamento BOM-label
IF OBJECT_ID('Traceability_RS.ind.LabelScripts', 'U') IS NULL
CREATE TABLE Traceability_RS.ind.LabelScripts (
    LabelScriptId INT IDENTITY(1,1) PRIMARY KEY,
    BomIndirectMaterialId INT NOT NULL,
    ScriptToPrint NVARCHAR(MAX) NULL,
    DateOut DATETIME NULL,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);
GO
