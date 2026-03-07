-- ============================================================
-- Crea tabella di log per tracciare l'invio email Kanban Refill
-- Una sola email al giorno consentita (indice UNIQUE su SentDate)
-- ============================================================

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'knb' AND TABLE_NAME = 'KanBanRefillEmailLog'
)
BEGIN
    CREATE TABLE [knb].[KanBanRefillEmailLog] (
        [LogId]           INT IDENTITY(1,1) PRIMARY KEY,
        [SentDate]        DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
        [SentAt]          DATETIME NOT NULL DEFAULT GETDATE(),
        [RecipientsCount] INT NULL,
        [MaterialsCount]  INT NULL,
        [Notes]           NVARCHAR(500) NULL
    );

    CREATE UNIQUE INDEX UX_KanBanRefillEmailLog_SentDate 
        ON [knb].[KanBanRefillEmailLog]([SentDate]);

    PRINT 'Tabella knb.KanBanRefillEmailLog creata con successo.';
END
ELSE
BEGIN
    PRINT 'Tabella knb.KanBanRefillEmailLog esiste già.';
END
GO
