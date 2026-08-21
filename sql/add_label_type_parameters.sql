-- Parametri di scarto tecnico per codice etichetta
IF OBJECT_ID('Traceability_RS.ind.LabelTypeParameters', 'U') IS NULL
BEGIN
    CREATE TABLE [Traceability_RS].[ind].[LabelTypeParameters] (
        LabelTypeParameterId INT IDENTITY(1,1) PRIMARY KEY,
        MaterialeId INT NOT NULL,
        ScartoType NVARCHAR(10) NOT NULL CONSTRAINT DF_LabelTypeParam_ScartoType DEFAULT ('FIXED')
            CONSTRAINT CK_LabelTypeParam_ScartoType CHECK (ScartoType IN ('FIXED', 'PERC')),
        ScartoValue DECIMAL(10,4) NOT NULL CONSTRAINT DF_LabelTypeParam_ScartoValue DEFAULT (0),
        ScartoMinimo DECIMAL(10,4) NOT NULL CONSTRAINT DF_LabelTypeParam_ScartoMinimo DEFAULT (0),
        Arrotondamento DECIMAL(10,4) NOT NULL CONSTRAINT DF_LabelTypeParam_Arrotondamento DEFAULT (1),
        DateIn DATETIME NOT NULL DEFAULT GETDATE(),
        DateOut DATETIME NULL,
        [User] NVARCHAR(255) NULL,
        CONSTRAINT FK_LabelTypeParameters_Materiali FOREIGN KEY (MaterialeId)
            REFERENCES [Traceability_RS].[ind].[Materiali](MaterialeId)
    );
    PRINT 'Tabella ind.LabelTypeParameters creata.';
END
ELSE
    PRINT 'Tabella ind.LabelTypeParameters già esistente.';
GO
