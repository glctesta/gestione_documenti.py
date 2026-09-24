-- ============================================================
-- Migration: Modulo Ricezione (incoming) — richieste tra PC
-- Schema: [Traceability_RS].[dyn]
-- Tabelle: IncomingRequest (richieste), IncomingReminderLog (log reminder)
-- Seed:    settings (reminder/giorno di default per tipo richiesta)
-- Idempotente (IF NOT EXISTS). Vedi incoming/incoming_db.py per l'accesso dati.
-- Nota: settings.atribute e' VARCHAR(30) — i nomi attributo rispettano il limite.
-- ============================================================

USE [Traceability_RS];
GO

-- ------------------------------------------------------------
-- 1) Richieste incoming
-- ------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[IncomingRequest]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[IncomingRequest] (
        Id                   INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_IncomingRequest PRIMARY KEY,
        RequestNumber        NVARCHAR(20)  NOT NULL
            CONSTRAINT UQ_dyn_IncomingRequest_Number UNIQUE,  -- INC-YYYYMMDD-####
        RequestType          NVARCHAR(30)  NOT NULL,          -- MPN_MANCANTE | MPN_SBAGLIATO | PO_MANCANTE | PO_QUANTITA
        SupplierId           INT           NULL,
        SupplierName         NVARCHAR(200) NULL,
        DdtNumber            NVARCHAR(50)  NULL,
        DdtDate              DATE          NULL,
        PurOrderNumber       NVARCHAR(50)  NULL,
        MpnCode              NVARCHAR(100) NULL,              -- MPN atteso / da verificare
        WrongMpn             NVARCHAR(100) NULL,              -- MPN ricevuto errato (MPN_SBAGLIATO)
        ComponentCode        NVARCHAR(100) NULL,              -- codice interno (dbo.Components, IDCOMPONENTTYPE = 1)
        QtyToReceive         DECIMAL(18,3) NULL,              -- quantita' effettivamente arrivata
        QtyExpectedPerPo     DECIMAL(18,3) NULL,              -- quantita' attesa dal P.O.
        RequestedBy          NVARCHAR(100) NULL,
        RequestedOn          DATETIME      NOT NULL
            CONSTRAINT DF_dyn_IncomingRequest_RequestedOn DEFAULT (GETDATE()),
        RequesterHost        NVARCHAR(100) NULL,              -- PC che ha inviato la richiesta (target popup risposta)
        Status               NVARCHAR(20)  NOT NULL
            CONSTRAINT DF_dyn_IncomingRequest_Status DEFAULT ('PENDING'),
            -- PENDING | ANSWERED | CONFIRMED_OK | CONFIRMED_KO
        AnswerMpnCode        NVARCHAR(100) NULL,
        AnswerText           NVARCHAR(1000) NULL,
        AnsweredBy           NVARCHAR(100) NULL,
        AnsweredOn           DATETIME      NULL,
        ConfirmedOk          BIT           NULL,
        ConfirmedBy          NVARCHAR(100) NULL,
        ConfirmedOn          DATETIME      NULL,
        LastEscalationPopup  DATETIME      NULL
    );
    PRINT 'Creata tabella dyn.IncomingRequest';

    CREATE NONCLUSTERED INDEX IX_dyn_IncomingRequest_Status
        ON [Traceability_RS].[dyn].[IncomingRequest] (Status, RequestedOn);
    CREATE NONCLUSTERED INDEX IX_dyn_IncomingRequest_RequestedOn
        ON [Traceability_RS].[dyn].[IncomingRequest] (RequestedOn);
    PRINT 'Creati indici su dyn.IncomingRequest (Status, RequestedOn)';
END
ELSE
BEGIN
    PRINT 'Tabella dyn.IncomingRequest gia'' esistente';
END
GO

-- ------------------------------------------------------------
-- 1b) Colonna ComponentCode (idempotente): installazioni pre-esistenti
-- ------------------------------------------------------------
IF COL_LENGTH('[Traceability_RS].[dyn].[IncomingRequest]', 'ComponentCode') IS NULL
BEGIN
    ALTER TABLE [Traceability_RS].[dyn].[IncomingRequest]
        ADD ComponentCode NVARCHAR(100) NULL;
    PRINT 'Aggiunta colonna ComponentCode a dyn.IncomingRequest';
END
ELSE
BEGIN
    PRINT 'Colonna ComponentCode gia'' presente';
END
GO

-- ------------------------------------------------------------
-- 2) Log reminder inviati (popup/email) per richiesta
-- ------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[IncomingReminderLog]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[IncomingReminderLog] (
        Id          INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_IncomingReminderLog PRIMARY KEY,
        RequestId   INT      NOT NULL,
        SentAt      DATETIME NOT NULL
            CONSTRAINT DF_dyn_IncomingReminderLog_SentAt DEFAULT (GETDATE()),
        Channel     NVARCHAR(20) NULL,  -- popup | email
        CONSTRAINT FK_dyn_IncomingReminderLog_Request
            FOREIGN KEY (RequestId) REFERENCES [Traceability_RS].[dyn].[IncomingRequest] (Id)
    );
    PRINT 'Creata tabella dyn.IncomingReminderLog';

    CREATE NONCLUSTERED INDEX IX_dyn_IncomingReminderLog_Request_SentAt
        ON [Traceability_RS].[dyn].[IncomingReminderLog] (RequestId, SentAt);
    PRINT 'Creato indice su dyn.IncomingReminderLog (RequestId, SentAt)';
END
ELSE
BEGIN
    PRINT 'Tabella dyn.IncomingReminderLog gia'' esistente';
END
GO

-- ------------------------------------------------------------
-- 3) Seed settings: reminder/giorno di default per tipo richiesta
--    Attributi (<= 30 char): Incoming_rem_<TIPO>
--    I destinatari email si configurano da GUI (incoming_setup_gui.py):
--      - per tipo richiesta: Incoming_email_<TIPO>
--      - report mensile:     Incoming_soluzione_problemi
-- ------------------------------------------------------------
DECLARE @seed TABLE (atribute VARCHAR(30), val VARCHAR(10));
INSERT INTO @seed (atribute, val) VALUES
    ('Incoming_rem_MPN_MANCANTE',  '2'),
    ('Incoming_rem_MPN_SBAGLIATO', '2'),
    ('Incoming_rem_PO_MANCANTE',   '2'),
    ('Incoming_rem_PO_QUANTITA',   '2');

DECLARE @a VARCHAR(30), @v VARCHAR(10);
DECLARE seed_cur CURSOR LOCAL FAST_FORWARD FOR SELECT atribute, val FROM @seed;
OPEN seed_cur;
FETCH NEXT FROM seed_cur INTO @a, @v;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = @a)
    BEGIN
        INSERT INTO traceability_rs.dbo.settings (atribute, [value]) VALUES (@a, @v);
        PRINT 'Seed settings: ' + @a + ' = ' + @v;
    END
    ELSE
        PRINT 'Settings gia'' presente: ' + @a;
    FETCH NEXT FROM seed_cur INTO @a, @v;
END
CLOSE seed_cur;
DEALLOCATE seed_cur;
GO

-- ------------------------------------------------------------
-- Verifica finale
-- ------------------------------------------------------------
SELECT 'IncomingRequest'    AS TableName, COUNT(*) AS RecordCount
FROM [Traceability_RS].[dyn].[IncomingRequest]
UNION ALL
SELECT 'IncomingReminderLog' AS TableName, COUNT(*) AS RecordCount
FROM [Traceability_RS].[dyn].[IncomingReminderLog]
UNION ALL
SELECT 'settings incoming'   AS TableName, COUNT(*) AS RecordCount
FROM traceability_rs.dbo.settings
WHERE atribute LIKE 'Incoming[_]%';
GO
