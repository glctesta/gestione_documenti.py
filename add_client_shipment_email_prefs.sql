-- ============================================================
-- Preferenze invio email spedizioni per cliente finale.
-- 2 flag per cliente: invio agli Account Manager (TO) e ai destinatari CC
-- (settings Sys_email_<FinalClientName>). Riga assente => entrambi attivi.
-- Idempotente.
-- ============================================================
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dbo].[ClientShipmentEmailPrefs]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dbo].[ClientShipmentEmailPrefs] (
        IDFinalClient        SMALLINT NOT NULL
            CONSTRAINT PK_ClientShipmentEmailPrefs PRIMARY KEY,
        SendToAccountManager BIT NOT NULL
            CONSTRAINT DF_CSEP_AM DEFAULT (1),
        SendToCc             BIT NOT NULL
            CONSTRAINT DF_CSEP_CC DEFAULT (1),
        LastUpdate           DATETIME NULL,
        UpdatedBy            NVARCHAR(100) NULL,
        CONSTRAINT FK_CSEP_FinalClient FOREIGN KEY (IDFinalClient)
            REFERENCES [Traceability_RS].[dbo].[FinalClients](IDFinalClient)
    );
    PRINT 'Creata tabella dbo.ClientShipmentEmailPrefs';
END
ELSE
    PRINT 'Tabella dbo.ClientShipmentEmailPrefs gia'' presente';
GO
