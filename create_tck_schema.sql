-- ============================================================
--  create_tck_schema.sql
--  Crea lo schema 'tck' e la tabella 'tck.Tickets'
--  nel database Traceability_RS.
--  Script idempotente: sicuro per esecuzioni ripetute.
-- ============================================================

USE [Traceability_RS];
GO

-- 1. Crea lo schema tck se non esiste
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'tck')
BEGIN
    EXEC('CREATE SCHEMA tck AUTHORIZATION dbo');
    PRINT 'Schema tck creato.';
END
ELSE
    PRINT 'Schema tck già esistente – nessuna modifica.';
GO

-- 2. Crea la tabella tck.Tickets se non esiste
IF NOT EXISTS (
    SELECT 1
    FROM   sys.tables  t
    JOIN   sys.schemas s ON t.schema_id = s.schema_id
    WHERE  s.name = N'tck' AND t.name = N'Tickets'
)
BEGIN
    CREATE TABLE tck.Tickets (
        TicketID        INT            IDENTITY(1,1) NOT NULL
                        CONSTRAINT PK_tck_Tickets PRIMARY KEY CLUSTERED,
        CreatedAt       DATETIME2(0)   NOT NULL DEFAULT GETDATE(),
        UserName        NVARCHAR(100)  NULL,
        Title           NVARCHAR(255)  NOT NULL,
        Description     NVARCHAR(MAX)  NULL,
        ErrorType       NVARCHAR(50)   NOT NULL DEFAULT N'manual',
            -- 'manual'    → aperto dall'utente via menu
            -- 'exception' → aperto automaticamente da sys.excepthook
        ErrorMessage    NVARCHAR(MAX)  NULL,   -- stacktrace / messaggio eccezione
        LogSnippet      NVARCHAR(MAX)  NULL,   -- ultime 50 righe del log
        ScreenshotPath  NVARCHAR(512)  NULL,   -- percorso locale file PNG
        EmailSent       BIT            NOT NULL DEFAULT 0,
        Status          NVARCHAR(50)   NOT NULL DEFAULT N'open'
            -- 'open' | 'closed' | 'in_progress'
    );
    PRINT 'Tabella tck.Tickets creata.';
END
ELSE
    PRINT 'Tabella tck.Tickets già esistente – nessuna modifica.';
GO

-- 3. (Opzionale) Indice sullo stato per query di ricerca
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE  object_id = OBJECT_ID(N'tck.Tickets')
      AND  name      = N'IX_tck_Tickets_Status'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_tck_Tickets_Status
        ON tck.Tickets (Status, CreatedAt DESC);
    PRINT 'Indice IX_tck_Tickets_Status creato.';
END
GO

-- 4. Traduzioni menu (idempotente)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = N'it' AND TranslationKey = N'menu_tickets')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'menu_tickets', N'Tickets');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = N'en' AND TranslationKey = N'menu_tickets')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'menu_tickets', N'Tickets');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = N'ro' AND TranslationKey = N'menu_tickets')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'menu_tickets', N'Tichete');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = N'de' AND TranslationKey = N'menu_tickets')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'menu_tickets', N'Tickets');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = N'sv' AND TranslationKey = N'menu_tickets')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'menu_tickets', N'Ärenden');
PRINT 'Traduzioni menu_tickets inserite.';
GO

PRINT '=== Setup tck schema completato ===';
GO
