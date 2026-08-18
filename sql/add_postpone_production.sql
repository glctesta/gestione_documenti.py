-- -*- sql -*-
-- add_postpone_production.sql
-- 1. Crea la tabella storico posticipi ordini di produzione.
-- 2. Registra la chiave di autorizzazione 'posponi_produzione' in AppTranslations
--    con MenuValue valorizzato (richiesto da _execute_authorized_action / GUI permessi).

USE Traceability_RS;
GO

-- ── 1. Tabella posticipi ─────────────────────────────────────────────────
IF OBJECT_ID('dbo.kit_order_postponements', 'U') IS NULL
CREATE TABLE dbo.kit_order_postponements (
    id            INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    order_number  NVARCHAR(30)      NOT NULL,
    idorder       INT               NULL,
    reason_code   NVARCHAR(50)      NOT NULL,
    reason_label  NVARCHAR(200)     NOT NULL,  -- motivazione sintetica
    reason_text   NVARCHAR(MAX)     NOT NULL,  -- spiegazione estesa
    days          INT               NOT NULL,
    postponed_by  NVARCHAR(100)     NOT NULL,  -- nome login / utente
    postponed_at  DATETIME          NOT NULL DEFAULT GETDATE(),
    expires_at    DATETIME          NOT NULL,
    CONSTRAINT CHK_kit_postpone_days CHECK (days > 0)
);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_kit_order_postponements_order_number')
    CREATE NONCLUSTERED INDEX IX_kit_order_postponements_order_number
    ON dbo.kit_order_postponements (order_number);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_kit_order_postponements_expires')
    CREATE NONCLUSTERED INDEX IX_kit_order_postponements_expires
    ON dbo.kit_order_postponements (expires_at) INCLUDE (order_number);
GO

-- ── 2. Traduzioni autorizzazione ─────────────────────────────────────────
DECLARE @MenuValue NVARCHAR(100) = N'Posponi produzione';

DECLARE @Translations TABLE (Lang CHAR(2), Value NVARCHAR(200));
INSERT INTO @Translations VALUES
('it', N'Posponi inizio produzione'),
('en', N'Postpone production start'),
('ro', N'Amână începerea producției'),
('de', N'Produktionsstart verschieben'),
('sv', N'Skjut upp produktionsstart');

DECLARE @Lang CHAR(2), @Value NVARCHAR(200);
DECLARE cur CURSOR FOR SELECT Lang, Value FROM @Translations;
OPEN cur;
FETCH NEXT FROM cur INTO @Lang, @Value;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations
                   WHERE LanguageCode = @Lang AND TranslationKey = N'posponi_produzione')
    BEGIN
        INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
        VALUES (@Lang, N'posponi_produzione', @Value, @MenuValue);
    END
    ELSE
    BEGIN
        UPDATE dbo.AppTranslations
           SET MenuValue = ISNULL(MenuValue, @MenuValue)
         WHERE LanguageCode = @Lang AND TranslationKey = N'posponi_produzione';
    END
    FETCH NEXT FROM cur INTO @Lang, @Value;
END
CLOSE cur;
DEALLOCATE cur;
GO

PRINT 'Tabella kit_order_postponements e traduzione posponi_produzione create/aggiornate.';
GO
