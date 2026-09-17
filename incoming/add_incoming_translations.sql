-- ============================================================
-- Script SQL per le traduzioni del modulo Ricezione (incoming)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv — idempotente (IF NOT EXISTS)
-- Chiavi con prefisso 'incoming_'. Vedi incoming/incoming_db.py.
-- ============================================================

USE [Traceability_RS];
GO

-- ============================================================================
-- Translation Key: incoming_module_title
-- Descrizione: Titolo del modulo Ricezione
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_module_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_module_title', N'Ricezione');
    PRINT 'Aggiunta traduzione: incoming_module_title (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_module_title (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_module_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_module_title', N'Receiving');
    PRINT 'Aggiunta traduzione: incoming_module_title (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_module_title (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_module_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_module_title', N'Recepție');
    PRINT 'Aggiunta traduzione: incoming_module_title (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_module_title (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_module_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_module_title', N'Wareneingang');
    PRINT 'Aggiunta traduzione: incoming_module_title (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_module_title (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_module_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_module_title', N'Mottagning');
    PRINT 'Aggiunta traduzione: incoming_module_title (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_module_title (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_type_mpn_mancante
-- Descrizione: Tipo richiesta: MPN mancante
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_type_mpn_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_type_mpn_mancante', N'MPN Mancante');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_mancante (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_mancante (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_type_mpn_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_type_mpn_mancante', N'Missing MPN');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_mancante (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_mancante (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_type_mpn_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_type_mpn_mancante', N'MPN lipsă');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_mancante (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_mancante (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_type_mpn_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_type_mpn_mancante', N'Fehlende MPN');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_mancante (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_mancante (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_type_mpn_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_type_mpn_mancante', N'MPN saknas');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_mancante (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_mancante (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_type_mpn_sbagliato
-- Descrizione: Tipo richiesta: MPN errato
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_type_mpn_sbagliato')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_type_mpn_sbagliato', N'MPN Sbagliato');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_sbagliato (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_sbagliato (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_type_mpn_sbagliato')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_type_mpn_sbagliato', N'Wrong MPN');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_sbagliato (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_sbagliato (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_type_mpn_sbagliato')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_type_mpn_sbagliato', N'MPN greșit');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_sbagliato (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_sbagliato (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_type_mpn_sbagliato')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_type_mpn_sbagliato', N'Falsche MPN');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_sbagliato (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_sbagliato (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_type_mpn_sbagliato')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_type_mpn_sbagliato', N'Fel MPN');
    PRINT 'Aggiunta traduzione: incoming_type_mpn_sbagliato (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_mpn_sbagliato (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_type_po_mancante
-- Descrizione: Tipo richiesta: P.O. mancante
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_type_po_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_type_po_mancante', N'Mancanza P.O.');
    PRINT 'Aggiunta traduzione: incoming_type_po_mancante (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_mancante (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_type_po_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_type_po_mancante', N'Missing P.O.');
    PRINT 'Aggiunta traduzione: incoming_type_po_mancante (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_mancante (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_type_po_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_type_po_mancante', N'Lipsă P.O.');
    PRINT 'Aggiunta traduzione: incoming_type_po_mancante (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_mancante (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_type_po_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_type_po_mancante', N'Fehlende Bestellnr.');
    PRINT 'Aggiunta traduzione: incoming_type_po_mancante (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_mancante (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_type_po_mancante')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_type_po_mancante', N'Saknad beställning');
    PRINT 'Aggiunta traduzione: incoming_type_po_mancante (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_mancante (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_type_po_quantita
-- Descrizione: Tipo richiesta: quantità P.O.
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_type_po_quantita')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_type_po_quantita', N'P.O. Quantità');
    PRINT 'Aggiunta traduzione: incoming_type_po_quantita (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_quantita (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_type_po_quantita')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_type_po_quantita', N'P.O. Quantity');
    PRINT 'Aggiunta traduzione: incoming_type_po_quantita (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_quantita (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_type_po_quantita')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_type_po_quantita', N'Cantitate P.O.');
    PRINT 'Aggiunta traduzione: incoming_type_po_quantita (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_quantita (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_type_po_quantita')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_type_po_quantita', N'Bestellmenge');
    PRINT 'Aggiunta traduzione: incoming_type_po_quantita (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_quantita (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_type_po_quantita')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_type_po_quantita', N'Beställningskvantitet');
    PRINT 'Aggiunta traduzione: incoming_type_po_quantita (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_type_po_quantita (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_status_pending
-- Descrizione: Stato: in attesa
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_status_pending')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_status_pending', N'In attesa');
    PRINT 'Aggiunta traduzione: incoming_status_pending (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_pending (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_status_pending')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_status_pending', N'Pending');
    PRINT 'Aggiunta traduzione: incoming_status_pending (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_pending (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_status_pending')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_status_pending', N'În așteptare');
    PRINT 'Aggiunta traduzione: incoming_status_pending (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_pending (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_status_pending')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_status_pending', N'Ausstehend');
    PRINT 'Aggiunta traduzione: incoming_status_pending (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_pending (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_status_pending')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_status_pending', N'Väntar');
    PRINT 'Aggiunta traduzione: incoming_status_pending (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_pending (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_status_answered
-- Descrizione: Stato: risposta pronta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_status_answered')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_status_answered', N'Risposta pronta');
    PRINT 'Aggiunta traduzione: incoming_status_answered (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_answered (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_status_answered')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_status_answered', N'Answered');
    PRINT 'Aggiunta traduzione: incoming_status_answered (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_answered (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_status_answered')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_status_answered', N'Răspuns disponibil');
    PRINT 'Aggiunta traduzione: incoming_status_answered (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_answered (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_status_answered')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_status_answered', N'Beantwortet');
    PRINT 'Aggiunta traduzione: incoming_status_answered (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_answered (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_status_answered')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_status_answered', N'Besvarad');
    PRINT 'Aggiunta traduzione: incoming_status_answered (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_answered (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_status_confirmed_ok
-- Descrizione: Stato: confermata OK
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_status_confirmed_ok')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_status_confirmed_ok', N'Confermata OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ok (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ok (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_status_confirmed_ok')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_status_confirmed_ok', N'Confirmed OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ok (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ok (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_status_confirmed_ok')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_status_confirmed_ok', N'Confirmat OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ok (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ok (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_status_confirmed_ok')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_status_confirmed_ok', N'Bestätigt OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ok (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ok (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_status_confirmed_ok')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_status_confirmed_ok', N'Bekräftad OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ok (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ok (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_status_confirmed_ko
-- Descrizione: Stato: confermata KO
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_status_confirmed_ko')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_status_confirmed_ko', N'Confermata KO');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ko (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ko (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_status_confirmed_ko')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_status_confirmed_ko', N'Confirmed KO');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ko (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ko (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_status_confirmed_ko')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_status_confirmed_ko', N'Confirmat KO');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ko (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ko (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_status_confirmed_ko')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_status_confirmed_ko', N'Bestätigt NOK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ko (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ko (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_status_confirmed_ko')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_status_confirmed_ko', N'Bekräftad ej OK');
    PRINT 'Aggiunta traduzione: incoming_status_confirmed_ko (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_status_confirmed_ko (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_request_number
-- Descrizione: Etichetta numero richiesta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_request_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_request_number', N'Numero richiesta');
    PRINT 'Aggiunta traduzione: incoming_request_number (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_number (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_request_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_request_number', N'Request number');
    PRINT 'Aggiunta traduzione: incoming_request_number (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_number (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_request_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_request_number', N'Număr solicitare');
    PRINT 'Aggiunta traduzione: incoming_request_number (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_number (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_request_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_request_number', N'Anfragenummer');
    PRINT 'Aggiunta traduzione: incoming_request_number (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_number (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_request_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_request_number', N'Begäransnummer');
    PRINT 'Aggiunta traduzione: incoming_request_number (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_number (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_supplier
-- Descrizione: Etichetta fornitore
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_supplier')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_supplier', N'Fornitore');
    PRINT 'Aggiunta traduzione: incoming_supplier (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_supplier (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_supplier')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_supplier', N'Supplier');
    PRINT 'Aggiunta traduzione: incoming_supplier (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_supplier (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_supplier')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_supplier', N'Furnizor');
    PRINT 'Aggiunta traduzione: incoming_supplier (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_supplier (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_supplier')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_supplier', N'Lieferant');
    PRINT 'Aggiunta traduzione: incoming_supplier (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_supplier (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_supplier')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_supplier', N'Leverantör');
    PRINT 'Aggiunta traduzione: incoming_supplier (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_supplier (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_ddt_number
-- Descrizione: Etichetta numero DDT
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_ddt_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_ddt_number', N'Numero DDT');
    PRINT 'Aggiunta traduzione: incoming_ddt_number (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_number (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_ddt_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_ddt_number', N'Delivery note no.');
    PRINT 'Aggiunta traduzione: incoming_ddt_number (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_number (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_ddt_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_ddt_number', N'Nr. aviz');
    PRINT 'Aggiunta traduzione: incoming_ddt_number (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_number (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_ddt_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_ddt_number', N'Lieferschein-Nr.');
    PRINT 'Aggiunta traduzione: incoming_ddt_number (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_number (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_ddt_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_ddt_number', N'Leveransnotanummer');
    PRINT 'Aggiunta traduzione: incoming_ddt_number (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_number (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_ddt_date
-- Descrizione: Etichetta data DDT
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_ddt_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_ddt_date', N'Data DDT');
    PRINT 'Aggiunta traduzione: incoming_ddt_date (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_date (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_ddt_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_ddt_date', N'Delivery note date');
    PRINT 'Aggiunta traduzione: incoming_ddt_date (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_date (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_ddt_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_ddt_date', N'Data aviz');
    PRINT 'Aggiunta traduzione: incoming_ddt_date (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_date (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_ddt_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_ddt_date', N'Lieferscheindatum');
    PRINT 'Aggiunta traduzione: incoming_ddt_date (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_date (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_ddt_date')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_ddt_date', N'Leveransdatum');
    PRINT 'Aggiunta traduzione: incoming_ddt_date (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_ddt_date (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_po_number
-- Descrizione: Etichetta P.O.
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_po_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_po_number', N'P.O.');
    PRINT 'Aggiunta traduzione: incoming_po_number (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_po_number (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_po_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_po_number', N'P.O.');
    PRINT 'Aggiunta traduzione: incoming_po_number (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_po_number (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_po_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_po_number', N'P.O.');
    PRINT 'Aggiunta traduzione: incoming_po_number (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_po_number (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_po_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_po_number', N'Bestellnr.');
    PRINT 'Aggiunta traduzione: incoming_po_number (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_po_number (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_po_number')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_po_number', N'Beställning');
    PRINT 'Aggiunta traduzione: incoming_po_number (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_po_number (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_mpn
-- Descrizione: Etichetta MPN
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_mpn', N'MPN');
    PRINT 'Aggiunta traduzione: incoming_mpn (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_mpn (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_mpn', N'MPN');
    PRINT 'Aggiunta traduzione: incoming_mpn (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_mpn (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_mpn', N'MPN');
    PRINT 'Aggiunta traduzione: incoming_mpn (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_mpn (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_mpn', N'MPN');
    PRINT 'Aggiunta traduzione: incoming_mpn (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_mpn (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_mpn', N'MPN');
    PRINT 'Aggiunta traduzione: incoming_mpn (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_mpn (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_wrong_mpn
-- Descrizione: Etichetta MPN errato
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_wrong_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_wrong_mpn', N'MPN errato');
    PRINT 'Aggiunta traduzione: incoming_wrong_mpn (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_wrong_mpn (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_wrong_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_wrong_mpn', N'Wrong MPN');
    PRINT 'Aggiunta traduzione: incoming_wrong_mpn (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_wrong_mpn (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_wrong_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_wrong_mpn', N'MPN greșit');
    PRINT 'Aggiunta traduzione: incoming_wrong_mpn (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_wrong_mpn (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_wrong_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_wrong_mpn', N'Falsche MPN');
    PRINT 'Aggiunta traduzione: incoming_wrong_mpn (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_wrong_mpn (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_wrong_mpn')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_wrong_mpn', N'Fel MPN');
    PRINT 'Aggiunta traduzione: incoming_wrong_mpn (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_wrong_mpn (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_qty_to_receive
-- Descrizione: Etichetta quantità da ricevere
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_qty_to_receive')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_qty_to_receive', N'Q.tà da ricevere');
    PRINT 'Aggiunta traduzione: incoming_qty_to_receive (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_to_receive (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_qty_to_receive')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_qty_to_receive', N'Qty to receive');
    PRINT 'Aggiunta traduzione: incoming_qty_to_receive (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_to_receive (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_qty_to_receive')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_qty_to_receive', N'Cant. de primit');
    PRINT 'Aggiunta traduzione: incoming_qty_to_receive (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_to_receive (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_qty_to_receive')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_qty_to_receive', N'Zu erhaltene Menge');
    PRINT 'Aggiunta traduzione: incoming_qty_to_receive (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_to_receive (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_qty_to_receive')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_qty_to_receive', N'Kvantitet att motta');
    PRINT 'Aggiunta traduzione: incoming_qty_to_receive (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_to_receive (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_qty_expected
-- Descrizione: Etichetta quantità attesa da P.O.
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_qty_expected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_qty_expected', N'Q.tà attesa da P.O.');
    PRINT 'Aggiunta traduzione: incoming_qty_expected (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_expected (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_qty_expected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_qty_expected', N'Qty expected per P.O.');
    PRINT 'Aggiunta traduzione: incoming_qty_expected (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_expected (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_qty_expected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_qty_expected', N'Cant. așteptată P.O.');
    PRINT 'Aggiunta traduzione: incoming_qty_expected (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_expected (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_qty_expected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_qty_expected', N'Erwartete Menge (P.O.)');
    PRINT 'Aggiunta traduzione: incoming_qty_expected (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_expected (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_qty_expected')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_qty_expected', N'Förväntad kvantitet (P.O.)');
    PRINT 'Aggiunta traduzione: incoming_qty_expected (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_qty_expected (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_requested_by
-- Descrizione: Etichetta richiesta da
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_requested_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_requested_by', N'Richiesta da');
    PRINT 'Aggiunta traduzione: incoming_requested_by (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_by (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_requested_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_requested_by', N'Requested by');
    PRINT 'Aggiunta traduzione: incoming_requested_by (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_by (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_requested_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_requested_by', N'Solicitat de');
    PRINT 'Aggiunta traduzione: incoming_requested_by (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_by (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_requested_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_requested_by', N'Angefordert von');
    PRINT 'Aggiunta traduzione: incoming_requested_by (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_by (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_requested_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_requested_by', N'Begärd av');
    PRINT 'Aggiunta traduzione: incoming_requested_by (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_by (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_requested_on
-- Descrizione: Etichetta data richiesta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_requested_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_requested_on', N'Data richiesta');
    PRINT 'Aggiunta traduzione: incoming_requested_on (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_on (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_requested_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_requested_on', N'Requested on');
    PRINT 'Aggiunta traduzione: incoming_requested_on (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_on (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_requested_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_requested_on', N'Data solicitării');
    PRINT 'Aggiunta traduzione: incoming_requested_on (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_on (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_requested_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_requested_on', N'Angefordert am');
    PRINT 'Aggiunta traduzione: incoming_requested_on (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_on (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_requested_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_requested_on', N'Begärd den');
    PRINT 'Aggiunta traduzione: incoming_requested_on (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_requested_on (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_answer
-- Descrizione: Etichetta risposta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_answer')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_answer', N'Risposta');
    PRINT 'Aggiunta traduzione: incoming_answer (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_answer')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_answer', N'Answer');
    PRINT 'Aggiunta traduzione: incoming_answer (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_answer')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_answer', N'Răspuns');
    PRINT 'Aggiunta traduzione: incoming_answer (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_answer')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_answer', N'Antwort');
    PRINT 'Aggiunta traduzione: incoming_answer (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_answer')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_answer', N'Svar');
    PRINT 'Aggiunta traduzione: incoming_answer (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_answered_by
-- Descrizione: Etichetta risposto da
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_answered_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_answered_by', N'Risposto da');
    PRINT 'Aggiunta traduzione: incoming_answered_by (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answered_by (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_answered_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_answered_by', N'Answered by');
    PRINT 'Aggiunta traduzione: incoming_answered_by (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answered_by (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_answered_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_answered_by', N'Răspuns de');
    PRINT 'Aggiunta traduzione: incoming_answered_by (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answered_by (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_answered_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_answered_by', N'Beantwortet von');
    PRINT 'Aggiunta traduzione: incoming_answered_by (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answered_by (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_answered_by')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_answered_by', N'Besvarad av');
    PRINT 'Aggiunta traduzione: incoming_answered_by (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answered_by (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_confirmed_on
-- Descrizione: Etichetta data conferma
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_confirmed_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_confirmed_on', N'Data conferma');
    PRINT 'Aggiunta traduzione: incoming_confirmed_on (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_confirmed_on (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_confirmed_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_confirmed_on', N'Confirmed on');
    PRINT 'Aggiunta traduzione: incoming_confirmed_on (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_confirmed_on (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_confirmed_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_confirmed_on', N'Data confirmării');
    PRINT 'Aggiunta traduzione: incoming_confirmed_on (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_confirmed_on (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_confirmed_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_confirmed_on', N'Bestätigt am');
    PRINT 'Aggiunta traduzione: incoming_confirmed_on (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_confirmed_on (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_confirmed_on')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_confirmed_on', N'Bekräftad den');
    PRINT 'Aggiunta traduzione: incoming_confirmed_on (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_confirmed_on (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_new_request_title
-- Descrizione: Titolo popup nuova richiesta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_new_request_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_new_request_title', N'Nuova richiesta Ricezione');
    PRINT 'Aggiunta traduzione: incoming_new_request_title (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_new_request_title (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_new_request_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_new_request_title', N'New receiving request');
    PRINT 'Aggiunta traduzione: incoming_new_request_title (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_new_request_title (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_new_request_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_new_request_title', N'Solicitare nouă Recepție');
    PRINT 'Aggiunta traduzione: incoming_new_request_title (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_new_request_title (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_new_request_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_new_request_title', N'Neue Wareneingang-Anfrage');
    PRINT 'Aggiunta traduzione: incoming_new_request_title (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_new_request_title (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_new_request_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_new_request_title', N'Ny mottagningsbegäran');
    PRINT 'Aggiunta traduzione: incoming_new_request_title (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_new_request_title (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_answer_ready_title
-- Descrizione: Titolo popup risposta pronta
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_answer_ready_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_answer_ready_title', N'Risposta pronta — Ricezione');
    PRINT 'Aggiunta traduzione: incoming_answer_ready_title (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer_ready_title (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_answer_ready_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_answer_ready_title', N'Answer ready — Receiving');
    PRINT 'Aggiunta traduzione: incoming_answer_ready_title (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer_ready_title (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_answer_ready_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_answer_ready_title', N'Răspuns disponibil — Recepție');
    PRINT 'Aggiunta traduzione: incoming_answer_ready_title (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer_ready_title (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_answer_ready_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_answer_ready_title', N'Antwort verfügbar — Wareneingang');
    PRINT 'Aggiunta traduzione: incoming_answer_ready_title (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer_ready_title (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_answer_ready_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_answer_ready_title', N'Svar klart — Mottagning');
    PRINT 'Aggiunta traduzione: incoming_answer_ready_title (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_answer_ready_title (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_escalation_title
-- Descrizione: Titolo popup escalation
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_escalation_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_escalation_title', N'Escalation richiesta Ricezione');
    PRINT 'Aggiunta traduzione: incoming_escalation_title (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_escalation_title (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_escalation_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_escalation_title', N'Receiving request escalation');
    PRINT 'Aggiunta traduzione: incoming_escalation_title (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_escalation_title (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_escalation_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_escalation_title', N'Escalare solicitare Recepție');
    PRINT 'Aggiunta traduzione: incoming_escalation_title (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_escalation_title (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_escalation_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_escalation_title', N'Eskalation Wareneingang-Anfrage');
    PRINT 'Aggiunta traduzione: incoming_escalation_title (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_escalation_title (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_escalation_title')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_escalation_title', N'Eskalering mottagningsbegäran');
    PRINT 'Aggiunta traduzione: incoming_escalation_title (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_escalation_title (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_db_error
-- Descrizione: Messaggio errore database
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_db_error')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_db_error', N'Errore database');
    PRINT 'Aggiunta traduzione: incoming_db_error (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_db_error (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_db_error')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_db_error', N'Database error');
    PRINT 'Aggiunta traduzione: incoming_db_error (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_db_error (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_db_error')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_db_error', N'Eroare bază de date');
    PRINT 'Aggiunta traduzione: incoming_db_error (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_db_error (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_db_error')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_db_error', N'Datenbankfehler');
    PRINT 'Aggiunta traduzione: incoming_db_error (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_db_error (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_db_error')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_db_error', N'Databasfel');
    PRINT 'Aggiunta traduzione: incoming_db_error (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_db_error (sv)';
END
GO

-- ============================================================================
-- Translation Key: incoming_request_created
-- Descrizione: Messaggio richiesta creata
-- ============================================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_request_created')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'incoming_request_created', N'Richiesta creata');
    PRINT 'Aggiunta traduzione: incoming_request_created (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_created (it)';
END
GO

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_request_created')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'incoming_request_created', N'Request created');
    PRINT 'Aggiunta traduzione: incoming_request_created (en)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_created (en)';
END
GO

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_request_created')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'incoming_request_created', N'Solicitare creată');
    PRINT 'Aggiunta traduzione: incoming_request_created (ro)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_created (ro)';
END
GO

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_request_created')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'incoming_request_created', N'Anfrage erstellt');
    PRINT 'Aggiunta traduzione: incoming_request_created (de)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_created (de)';
END
GO

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_request_created')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'incoming_request_created', N'Begäran skapad');
    PRINT 'Aggiunta traduzione: incoming_request_created (sv)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_request_created (sv)';
END
GO

-- ============================================================================
-- CHIAVI DI AUTORIZZAZIONE (permessi)
-- Colonna MenuValue OBBLIGATORIA (la riga 'it' con MenuValue NON NULL e'
-- richiesta da grant_permission per l'assegnazione in Strumenti > Permessi).
-- Pattern: ind_permission_riordino.sql
-- ============================================================================

-- Chiave: incoming_richiesta — apertura finestra Richiesta (invio richieste incoming)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_richiesta')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'it', N'incoming_richiesta', N'Ricezione — Richiesta', N'Ricezione — Richiesta');
    PRINT 'Aggiunta traduzione: incoming_richiesta (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_richiesta (it)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_richiesta')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'en', N'incoming_richiesta', N'Receiving — Request', N'Receiving — Request');
    PRINT 'Aggiunta traduzione: incoming_richiesta (en)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_richiesta')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'ro', N'incoming_richiesta', N'Recepție — Cerere', N'Recepție — Cerere');
    PRINT 'Aggiunta traduzione: incoming_richiesta (ro)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_richiesta')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'de', N'incoming_richiesta', N'Wareneingang — Anfrage', N'Wareneingang — Anfrage');
    PRINT 'Aggiunta traduzione: incoming_richiesta (de)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_richiesta')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'sv', N'incoming_richiesta', N'Inleverans — Förfrågan', N'Inleverans — Förfrågan');
    PRINT 'Aggiunta traduzione: incoming_richiesta (sv)';
END
GO

-- Chiave: incoming_soluzioni — apertura finestra Soluzioni (risposta alle richieste)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_soluzioni')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'it', N'incoming_soluzioni', N'Ricezione — Soluzioni', N'Ricezione — Soluzioni');
    PRINT 'Aggiunta traduzione: incoming_soluzioni (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_soluzioni (it)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_soluzioni')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'en', N'incoming_soluzioni', N'Receiving — Solutions', N'Receiving — Solutions');
    PRINT 'Aggiunta traduzione: incoming_soluzioni (en)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_soluzioni')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'ro', N'incoming_soluzioni', N'Recepție — Soluții', N'Recepție — Soluții');
    PRINT 'Aggiunta traduzione: incoming_soluzioni (ro)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_soluzioni')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'de', N'incoming_soluzioni', N'Wareneingang — Lösungen', N'Wareneingang — Lösungen');
    PRINT 'Aggiunta traduzione: incoming_soluzioni (de)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_soluzioni')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'sv', N'incoming_soluzioni', N'Inleverans — Lösningar', N'Inleverans — Lösningar');
    PRINT 'Aggiunta traduzione: incoming_soluzioni (sv)';
END
GO

-- Chiave: incoming_setup — apertura finestra Setup (operatori + workstations)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'incoming_setup')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'it', N'incoming_setup', N'Ricezione — Setup', N'Ricezione — Setup');
    PRINT 'Aggiunta traduzione: incoming_setup (it)';
END
ELSE
BEGIN
    PRINT 'Traduzione già esistente: incoming_setup (it)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'incoming_setup')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'en', N'incoming_setup', N'Receiving — Setup', N'Receiving — Setup');
    PRINT 'Aggiunta traduzione: incoming_setup (en)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'incoming_setup')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'ro', N'incoming_setup', N'Recepție — Configurare', N'Recepție — Configurare');
    PRINT 'Aggiunta traduzione: incoming_setup (ro)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'incoming_setup')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'de', N'incoming_setup', N'Wareneingang — Einrichtung', N'Wareneingang — Einrichtung');
    PRINT 'Aggiunta traduzione: incoming_setup (de)';
END
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations]
               WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'incoming_setup')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
    VALUES (N'sv', N'incoming_setup', N'Inleverans — Inställningar', N'Inleverans — Inställningar');
    PRINT 'Aggiunta traduzione: incoming_setup (sv)';
END
GO

-- ============================================================================
-- CHIAVI MENU / POPUP Ricezione (etichette voci di menu e pulsanti popup)
-- ============================================================================

-- menu_receiving
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='menu_receiving')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'menu_receiving',N'Ricezione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='menu_receiving')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'menu_receiving',N'Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='menu_receiving')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'menu_receiving',N'Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='menu_receiving')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'menu_receiving',N'Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='menu_receiving')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'menu_receiving',N'Inleverans');
GO

-- incoming_menu_richiesta
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_menu_richiesta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_menu_richiesta',N'Richiesta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_menu_richiesta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_menu_richiesta',N'Request');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_menu_richiesta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_menu_richiesta',N'Cerere');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_menu_richiesta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_menu_richiesta',N'Anfrage');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_menu_richiesta')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_menu_richiesta',N'Förfrågan');
GO

-- incoming_menu_soluzioni
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_menu_soluzioni')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_menu_soluzioni',N'Soluzioni');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_menu_soluzioni')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_menu_soluzioni',N'Solutions');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_menu_soluzioni')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_menu_soluzioni',N'Soluții');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_menu_soluzioni')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_menu_soluzioni',N'Lösungen');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_menu_soluzioni')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_menu_soluzioni',N'Lösningar');
GO

-- incoming_menu_order
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_menu_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_menu_order',N'Ordine');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_menu_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_menu_order',N'Order');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_menu_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_menu_order',N'Comandă');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_menu_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_menu_order',N'Bestellung');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_menu_order')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_menu_order',N'Order');
GO

-- incoming_menu_setup_operators
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_menu_setup_operators')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_menu_setup_operators',N'Gestione operatori');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_menu_setup_operators')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_menu_setup_operators',N'Operators management');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_menu_setup_operators')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_menu_setup_operators',N'Gestionare operatori');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_menu_setup_operators')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_menu_setup_operators',N'Operatorenverwaltung');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_menu_setup_operators')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_menu_setup_operators',N'Operatörshantering');
GO

-- incoming_menu_setup_workstations
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_menu_setup_workstations')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_menu_setup_workstations',N'Gestione workstations');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_menu_setup_workstations')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_menu_setup_workstations',N'Workstations management');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_menu_setup_workstations')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_menu_setup_workstations',N'Gestionare stații de lucru');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_menu_setup_workstations')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_menu_setup_workstations',N'Workstation-Verwaltung');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_menu_setup_workstations')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_menu_setup_workstations',N'Workstation-hantering');
GO

-- incoming_popup_open_confirm
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_popup_open_confirm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_popup_open_confirm',N'Apri finestra conferma soluzione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_popup_open_confirm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_popup_open_confirm',N'Open solution confirmation window');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_popup_open_confirm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_popup_open_confirm',N'Deschide fereastra de confirmare');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_popup_open_confirm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_popup_open_confirm',N'Bestätigungsfenster öffnen');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_popup_open_confirm')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_popup_open_confirm',N'Öppna bekräftelsefönster');
GO
