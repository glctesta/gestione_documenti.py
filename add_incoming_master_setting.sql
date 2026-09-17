-- Script SQL per l'attributo settings del master ticket del modulo Ricezione
-- Tabella: [Traceability_RS].[dbo].[Settings]
-- Data: 2026-09-16
-- Scopo: gli utenti la cui email e' elencata in 'Sys_master_for_tikets'
--        vedono TUTTI i ticket aperti nella finestra Soluzioni.
-- Valore vuoto = nessun master configurato (tutti gli utenti vedono solo
-- i tipi richiesta per cui la loro email e' tra i destinatari per tipo).

USE [Traceability_RS];
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[Settings] WHERE [atribute] = 'Sys_master_for_tikets')
BEGIN
    INSERT INTO [dbo].[Settings] ([atribute], [value])
    VALUES ('Sys_master_for_tikets', '');
    PRINT 'Voce Sys_master_for_tikets inserita (valore vuoto). Configurare le email master.';
END
ELSE
BEGIN
    PRINT 'Voce Sys_master_for_tikets gia'' presente.';
END
GO
