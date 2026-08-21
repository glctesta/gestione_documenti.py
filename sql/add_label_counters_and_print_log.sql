-- Schema dati per la stampa etichette produzione (counter + log + flag tracciabilità)

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'LabelCounters'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.LabelCounters (
        LabelCounterId INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId INT NOT NULL,
        Prefix NVARCHAR(50) NULL,
        Suffix NVARCHAR(50) NULL,
        LastCounter INT NOT NULL DEFAULT 0,
        DateIn DATETIME NOT NULL DEFAULT GETDATE(),
        DateOut DATETIME NULL,
        [User] NVARCHAR(255) NULL,
        CONSTRAINT FK_LabelCounters_Materiali FOREIGN KEY (MaterialeId)
            REFERENCES Traceability_RS.ind.Materiali(MaterialeId)
    );
    PRINT 'Creata tabella Traceability_RS.ind.LabelCounters';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.LabelCounters già esistente';
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'LabelPrintLog'
)
BEGIN
    CREATE TABLE Traceability_RS.ind.LabelPrintLog (
        LabelPrintLogId INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId INT NOT NULL,
        LabelPrinterId INT NOT NULL,
        OrderId INT NULL,
        Quantity INT NOT NULL DEFAULT 1,
        CounterFrom INT NULL,
        CounterTo INT NULL,
        Prefix NVARCHAR(50) NULL,
        Suffix NVARCHAR(50) NULL,
        ScriptSnapshot NVARCHAR(MAX) NULL,
        PrintedAt DATETIME NOT NULL DEFAULT GETDATE(),
        [User] NVARCHAR(255) NULL
    );
    PRINT 'Creata tabella Traceability_RS.ind.LabelPrintLog';
END
ELSE
BEGIN
    PRINT 'Tabella Traceability_RS.ind.LabelPrintLog già esistente';
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'ind' AND t.name = 'LabelTypeParameters' AND c.name = 'IsTraceabilityLabel'
)
BEGIN
    ALTER TABLE Traceability_RS.ind.LabelTypeParameters
    ADD IsTraceabilityLabel BIT NOT NULL DEFAULT 0;
    PRINT 'Aggiunta colonna IsTraceabilityLabel a LabelTypeParameters';
END
ELSE
BEGIN
    PRINT 'Colonna IsTraceabilityLabel già presente';
END
GO
