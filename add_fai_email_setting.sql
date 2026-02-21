-- ============================================================
-- Script: add_fai_email_setting.sql
-- Scopo:  Aggiunge la voce "Sys_verifica_linea" nella tabella
--         Settings per abilitare l'invio email FAI di validazione
--         di linea.
--
-- ⚠️  ISTRUZIONI:
--     1. Sostituire 'email1@tuodominio.com' con gli indirizzi
--        reali separati da punto e virgola (;)
--     2. Eseguire questo script sul database Traceability_RS
-- ============================================================

USE Traceability_RS;
GO

-- Verifica se la voce esiste già
IF NOT EXISTS (
    SELECT 1
    FROM dbo.settings
    WHERE atribute = 'Sys_verifica_linea'
)
BEGIN
    -- Inserisce la voce con i destinatari email desiderati.
    -- Per più destinatari usa il punto e virgola come separatore:
    -- es. 'email1@azienda.com;email2@azienda.com'
    INSERT INTO dbo.settings (atribute, [VALUE])
    VALUES ('Sys_verifica_linea', 'email1@tuodominio.com');

    PRINT '✅ Voce Sys_verifica_linea inserita correttamente.';
END
ELSE
BEGIN
    -- Se esiste già, mostra il valore attuale
    SELECT atribute, [VALUE]
    FROM dbo.settings
    WHERE atribute = 'Sys_verifica_linea';

    PRINT '⚠️  Voce Sys_verifica_linea già presente. Aggiorna il campo VALUE se necessario.';
END
GO

-- Verifica finale
SELECT atribute, [VALUE]
FROM dbo.settings
WHERE atribute = 'Sys_verifica_linea';
GO
