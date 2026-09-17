-- ============================================================
-- Traduzioni GUI del modulo Ricezione (incoming)
-- Chiavi inc_* / incoming_setup_* / incoming_ws_*
-- Lingue: it, en, ro, de, sv — idempotente (IF NOT EXISTS)
-- Generato da script; pattern identico agli altri script del modulo.
-- ============================================================

USE [Traceability_RS];
GO

-- inc_col_age
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_age')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_age',N'Età (min)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_age')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_age',N'Age (min)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_age')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_age',N'Vârstă (min)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_age')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_age',N'Alter (Min)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_age')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_age',N'Ålder (min)');
GO

-- inc_col_answered_by
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_answered_by',N'Risposta di');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_answered_by',N'Answered by');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_answered_by',N'Răspuns de');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_answered_by',N'Beantwortet von');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_answered_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_answered_by',N'Besvarad av');
GO

-- inc_col_answered_on
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_answered_on',N'Risposto il');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_answered_on',N'Answered on');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_answered_on',N'Răspuns la');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_answered_on',N'Beantwortet am');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_answered_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_answered_on',N'Besvarad den');
GO

-- inc_col_by
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_by',N'Richiesto da');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_by',N'Requested by');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_by',N'Solicitat de');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_by',N'Angefragt von');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_by')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_by',N'Begärd av');
GO

-- inc_col_ddt
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_ddt')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_ddt',N'DDT');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_ddt')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_ddt',N'Del. note');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_ddt')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_ddt',N'Aviz');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_ddt')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_ddt',N'Lieferschein');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_ddt')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_ddt',N'Fraktsedel');
GO

-- inc_col_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_mpn',N'MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_mpn',N'MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_mpn',N'MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_mpn',N'MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_mpn',N'MPN');
GO

-- inc_col_number
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_number',N'Numero');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_number',N'Number');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_number',N'Număr');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_number',N'Nummer');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_number',N'Nummer');
GO

-- inc_col_po
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_po',N'P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_po',N'P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_po',N'P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_po',N'B.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_po',N'P.O.');
GO

-- inc_col_qty
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_qty',N'Q.tà');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_qty',N'Qty');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_qty',N'Cant.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_qty',N'Menge');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_qty')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_qty',N'Antal');
GO

-- inc_col_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_status',N'Stato');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_status',N'Status');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_status',N'Stare');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_status',N'Status');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_status',N'Status');
GO

-- inc_col_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_supplier',N'Fornitore');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_supplier',N'Supplier');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_supplier',N'Furnizor');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_supplier',N'Lieferant');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_supplier',N'Leverantör');
GO

-- inc_col_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_col_type',N'Tipo');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_col_type',N'Type');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_col_type',N'Tip');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_col_type',N'Typ');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_col_type',N'Typ');
GO

-- inc_conf_already_confirmed
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_already_confirmed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_already_confirmed',N'Richiesta già confermata da un altro operatore.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_already_confirmed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_already_confirmed',N'Request already confirmed by another operator.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_already_confirmed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_already_confirmed',N'Cerere deja confirmată de alt operator.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_already_confirmed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_already_confirmed',N'Anfrage bereits von einem anderen Bediener bestätigt.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_already_confirmed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_already_confirmed',N'Begäran redan bekräftad av en annan operatör.');
GO

-- inc_conf_answer
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_answer',N'Risposta ricevuta:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_answer',N'Answer received:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_answer',N'Răspuns primit:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_answer',N'Antwort erhalten:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_answer')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_answer',N'Svar mottaget:');
GO

-- inc_conf_confirm_ko
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_confirm_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_confirm_ko',N'Segnalare la soluzione di {0} come NON risolutiva?
La richiesta tornerà in stato KO.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_confirm_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_confirm_ko',N'Report the solution for {0} as NOT resolving?
The request will be marked KO.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_confirm_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_confirm_ko',N'Marcați soluția pentru {0} ca NEREZOLVANTĂ?
Cererea va trece în stare KO.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_confirm_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_confirm_ko',N'Lösung für {0} als NICHT lösend melden?
Die Anfrage wird als KO markiert.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_confirm_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_confirm_ko',N'Ange lösningen för {0} som EJ lönsam?
Begäran markeras KO.');
GO

-- inc_conf_confirm_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_confirm_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_confirm_ok',N'Confermare la soluzione per {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_confirm_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_confirm_ok',N'Confirm the solution for {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_confirm_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_confirm_ok',N'Confirmați soluția pentru {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_confirm_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_confirm_ok',N'Lösung für {0} bestätigen?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_confirm_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_confirm_ok',N'Bekräfta lösningen för {0}?');
GO

-- inc_conf_confirmed_on
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_confirmed_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_confirmed_on',N'Confermato il');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_confirmed_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_confirmed_on',N'Confirmed on');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_confirmed_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_confirmed_on',N'Confirmat la');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_confirmed_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_confirmed_on',N'Bestätigt am');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_confirmed_on')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_confirmed_on',N'Bekräftad den');
GO

-- inc_conf_detail
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_detail',N'Dettaglio richiesta e risposta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_detail',N'Request and answer detail');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_detail',N'Detalii cerere și răspuns');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_detail',N'Details zur Anfrage und Antwort');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_detail',N'Detalj för begäran och svar');
GO

-- inc_conf_filter_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_filter_status',N'Stato:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_filter_status',N'Status:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_filter_status',N'Stare:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_filter_status',N'Status:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_filter_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_filter_status',N'Status:');
GO

-- inc_conf_ko
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_ko',N'✘ Soluzione non risolutiva');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_ko',N'✘ Solution not resolving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_ko',N'✘ Soluție nerezolvativă');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_ko',N'✘ Lösung nicht lösend');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_ko')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_ko',N'✘ Lösning inte lönsam');
GO

-- inc_conf_ok
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_ok',N'✔ Conferma soluzione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_ok',N'✔ Confirm solution');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_ok',N'✔ Confirmă soluția');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_ok',N'✔ Lösung bestätigen');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_ok')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_ok',N'✔ Bekräfta lösning');
GO

-- inc_conf_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_conf_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_conf_title',N'Conferma soluzioni — Ricezione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_conf_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_conf_title',N'Confirm solutions — Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_conf_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_conf_title',N'Confirmare soluții — Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_conf_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_conf_title',N'Lösungen bestätigen — Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_conf_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_conf_title',N'Bekräfta lösningar — Inleverans');
GO

-- inc_req_data
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_data')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_data',N'Dati richiesta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_data')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_data',N'Request data');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_data')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_data',N'Date cerere');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_data')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_data',N'Anfragedaten');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_data')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_data',N'Begärandata');
GO

-- inc_req_ddt_date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_ddt_date',N'Data DDT:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_ddt_date',N'Delivery note date:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_ddt_date',N'Data aviz:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_ddt_date',N'Lieferscheindatum:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_ddt_date')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_ddt_date',N'Fraktsedeldatum:');
GO

-- inc_req_ddt_date_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_ddt_date_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_ddt_date_required',N'Inserire la data DDT.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_ddt_date_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_ddt_date_required',N'Enter the delivery note date.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_ddt_date_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_ddt_date_required',N'Introduceți data avizului.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_ddt_date_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_ddt_date_required',N'Lieferscheindatum eingeben.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_ddt_date_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_ddt_date_required',N'Ange fraktsedeldatum.');
GO

-- inc_req_ddt_number
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_ddt_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_ddt_number',N'Numero DDT:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_ddt_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_ddt_number',N'Delivery note no.:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_ddt_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_ddt_number',N'Număr aviz:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_ddt_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_ddt_number',N'Lieferschein-Nr.:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_ddt_number')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_ddt_number',N'Fraktsedelnr:');
GO

-- inc_req_ddt_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_ddt_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_ddt_required',N'Inserire il numero DDT.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_ddt_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_ddt_required',N'Enter the delivery note number.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_ddt_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_ddt_required',N'Introduceți numărul avizului.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_ddt_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_ddt_required',N'Lieferscheinnummer eingeben.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_ddt_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_ddt_required',N'Ange fraktsedelnummer.');
GO

-- inc_req_field_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_field_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_field_required',N'Compilare il campo richiesto ({0}).');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_field_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_field_required',N'Fill in the required field ({0}).');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_field_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_field_required',N'Completați câmpul obligatoriu ({0}).');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_field_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_field_required',N'Pflichtfeld ausfüllen ({0}).');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_field_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_field_required',N'Fyll i obligatoriskt fält ({0}).');
GO

-- inc_req_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_mpn',N'Codice MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_mpn',N'MPN code');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_mpn',N'Cod MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_mpn',N'MPN-Code');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_mpn',N'MPN-kod');
GO

-- inc_req_po
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_po',N'Numero P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_po',N'P.O. number');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_po',N'Număr P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_po',N'B.O.-Nummer');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_po')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_po',N'P.O.-nummer');
GO

-- inc_req_popup_msg
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_popup_msg',N'{0} — Fornitore: {1} — DDT: {2} — Da: {3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_popup_msg',N'{0} — Supplier: {1} — Del. note: {2} — From: {3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_popup_msg',N'{0} — Furnizor: {1} — Aviz: {2} — De la: {3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_popup_msg',N'{0} — Lieferant: {1} — Lieferschein: {2} — Von: {3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_popup_msg',N'{0} — Leverantör: {1} — Fraktsedel: {2} — Från: {3}');
GO

-- inc_req_popup_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_popup_title',N'Nuova richiesta Ricezione — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_popup_title',N'New receiving request — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_popup_title',N'Cerere nouă Recepție — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_popup_title',N'Neue Wareneingang-Anfrage — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_popup_title',N'Ny inleveransförfrågan — {0}');
GO

-- inc_req_qty_expected
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_qty_expected',N'Quantità attesa da P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_qty_expected',N'Qty expected per P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_qty_expected',N'Cantitate așteptată P.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_qty_expected',N'Erwartete Menge laut B.O.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_qty_expected')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_qty_expected',N'Antal enligt P.O.');
GO

-- inc_req_qty_invalid
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_qty_invalid',N'Quantità non valida in {0}.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_qty_invalid',N'Invalid quantity in {0}.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_qty_invalid',N'Cantitate invalidă în {0}.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_qty_invalid',N'Ungültige Menge in {0}.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_qty_invalid')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_qty_invalid',N'Ogiltigt antal i {0}.');
GO

-- inc_req_qty_receive
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_qty_receive',N'Quantità da ricevere');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_qty_receive',N'Qty to receive');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_qty_receive',N'Cantitate de recepționat');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_qty_receive',N'Zu erhaltende Menge');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_qty_receive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_qty_receive',N'Antal att ta emot');
GO

-- inc_req_reset
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_reset')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_reset',N'Azzera campi');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_reset')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_reset',N'Clear fields');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_reset')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_reset',N'Resetează câmpuri');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_reset')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_reset',N'Felder leeren');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_reset')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_reset',N'Rensa fält');
GO

-- inc_req_save_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_save_error',N'Errore durante il salvataggio della richiesta:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_save_error',N'Error saving the request:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_save_error',N'Eroare la salvarea cererii:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_save_error',N'Fehler beim Speichern der Anfrage:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_save_error',N'Fel vid sparande av begäran:
{0}');
GO

-- inc_req_select_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_select_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_select_supplier',N'Seleziona un fornitore dall''elenco.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_select_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_select_supplier',N'Select a supplier from the list.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_select_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_select_supplier',N'Selectați un furnizor din listă.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_select_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_select_supplier',N'Lieferanten aus der Liste wählen.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_select_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_select_supplier',N'Välj en leverantör från listan.');
GO

-- inc_req_select_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_select_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_select_type',N'Seleziona il tipo di richiesta.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_select_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_select_type',N'Select the request type.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_select_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_select_type',N'Selectați tipul cererii.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_select_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_select_type',N'Anfrageart wählen.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_select_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_select_type',N'Välj förfrågningstyp.');
GO

-- inc_req_send
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_send',N'📨 Invia richiesta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_send',N'📨 Send request');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_send',N'📨 Trimite cererea');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_send',N'📨 Anfrage senden');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_send',N'📨 Skicka förfrågan');
GO

-- inc_req_sent
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_sent',N'Richiesta {0} inviata.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_sent',N'Request {0} sent.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_sent',N'Cererea {0} a fost trimisă.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_sent',N'Anfrage {0} gesendet.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_sent')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_sent',N'Begäran {0} skickad.');
GO

-- inc_req_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_supplier',N'Fornitore:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_supplier',N'Supplier:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_supplier',N'Furnizor:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_supplier',N'Lieferant:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_supplier',N'Leverantör:');
GO

-- inc_req_suppliers_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_suppliers_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_suppliers_error',N'Impossibile caricare l''elenco fornitori.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_suppliers_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_suppliers_error',N'Unable to load the supplier list.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_suppliers_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_suppliers_error',N'Imposibil de încărcat lista furnizori.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_suppliers_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_suppliers_error',N'Lieferantenliste konnte nicht geladen werden.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_suppliers_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_suppliers_error',N'Det gick inte att läsa in leverantörslistan.');
GO

-- inc_req_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_title',N'Nuova richiesta — Ricezione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_title',N'New request — Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_title',N'Cerere nouă — Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_title',N'Neue Anfrage — Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_title',N'Ny förfrågan — Inleverans');
GO

-- inc_req_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_type',N'Tipo richiesta:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_type',N'Request type:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_type',N'Tip cerere:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_type',N'Anfrageart:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_type',N'Förfrågningstyp:');
GO

-- inc_req_wrong_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_req_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_req_wrong_mpn',N'MPN errato');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_req_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_req_wrong_mpn',N'Wrong MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_req_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_req_wrong_mpn',N'MPN greșit');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_req_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_req_wrong_mpn',N'Falsche MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_req_wrong_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_req_wrong_mpn',N'Felaktig MPN');
GO

-- inc_sol_all_types
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_all_types')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_all_types',N'(tutti)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_all_types')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_all_types',N'(all)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_all_types')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_all_types',N'(toate)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_all_types')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_all_types',N'(alle)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_all_types')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_all_types',N'(alla)');
GO

-- inc_sol_already_answered
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_already_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_already_answered',N'Richiesta già risolta da un altro operatore.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_already_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_already_answered',N'Request already resolved by another operator.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_already_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_already_answered',N'Cerere deja rezolvată de alt operator.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_already_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_already_answered',N'Anfrage bereits von einem anderen Bediener gelöst.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_already_answered')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_already_answered',N'Begäran redan löst av en annan operatör.');
GO

-- inc_sol_answer_mpn
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_answer_mpn',N'MPN corretto');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_answer_mpn',N'Correct MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_answer_mpn',N'MPN corect');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_answer_mpn',N'Korrekte MPN');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_answer_mpn')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_answer_mpn',N'Korrekt MPN');
GO

-- inc_sol_answer_text
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_answer_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_answer_text',N'Soluzione / nota:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_answer_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_answer_text',N'Solution / note:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_answer_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_answer_text',N'Soluție / notă:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_answer_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_answer_text',N'Lösung / Anmerkung:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_answer_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_answer_text',N'Lösning / anteckning:');
GO

-- inc_sol_confirm_send
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_confirm_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_confirm_send',N'Inviare la risposta a {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_confirm_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_confirm_send',N'Send the answer to {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_confirm_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_confirm_send',N'Trimiteți răspunsul către {0}?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_confirm_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_confirm_send',N'Antwort an {0} senden?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_confirm_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_confirm_send',N'Skicka svaret till {0}?');
GO

-- inc_sol_detail
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_detail',N'Dettaglio richiesta e soluzione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_detail',N'Request and solution detail');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_detail',N'Detalii cerere și soluție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_detail',N'Details zur Anfrage und Lösung');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_detail')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_detail',N'Detalj för begäran och lösning');
GO

-- inc_sol_filter_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_filter_type',N'Tipo:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_filter_type',N'Type:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_filter_type',N'Tip:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_filter_type',N'Typ:');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_filter_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_filter_type',N'Typ:');
GO

-- inc_sol_mpn_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_mpn_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_mpn_required',N'Inserire il codice MPN corretto.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_mpn_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_mpn_required',N'Enter the correct MPN code.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_mpn_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_mpn_required',N'Introduceți codul MPN corect.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_mpn_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_mpn_required',N'Korrekten MPN-Code eingeben.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_mpn_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_mpn_required',N'Ange korrekt MPN-kod.');
GO

-- inc_sol_pending
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_pending',N'in attesa');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_pending',N'pending');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_pending',N'în așteptare');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_pending',N'ausstehend');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_pending')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_pending',N'väntar');
GO

-- inc_sol_popup_msg
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_popup_msg',N'La richiesta {0} ha una risposta da {1}.
MPN: {2}
{3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_popup_msg',N'Request {0} has an answer from {1}.
MPN: {2}
{3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_popup_msg',N'Cererea {0} are un răspuns de la {1}.
MPN: {2}
{3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_popup_msg',N'Anfrage {0} hat eine Antwort von {1}.
MPN: {2}
{3}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_popup_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_popup_msg',N'Begäran {0} har ett svar från {1}.
MPN: {2}
{3}');
GO

-- inc_sol_popup_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_popup_title',N'Risposta pronta — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_popup_title',N'Answer ready — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_popup_title',N'Răspuns gata — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_popup_title',N'Antwort bereit — {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_popup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_popup_title',N'Svar klart — {0}');
GO

-- inc_sol_refresh
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_refresh')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_refresh',N'🔄 Aggiorna');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_refresh')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_refresh',N'🔄 Refresh');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_refresh')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_refresh',N'🔄 Actualizează');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_refresh')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_refresh',N'🔄 Aktualisieren');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_refresh')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_refresh',N'🔄 Uppdatera');
GO

-- inc_sol_select
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_select',N'Seleziona una richiesta.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_select',N'Select a request.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_select',N'Selectați o cerere.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_select',N'Anfrage auswählen.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_select')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_select',N'Välj en begäran.');
GO

-- inc_sol_send
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_send',N'✉ Invia risposta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_send',N'✉ Send answer');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_send',N'✉ Trimite răspuns');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_send',N'✉ Antwort senden');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_send')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_send',N'✉ Skicka svar');
GO

-- inc_sol_text_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_text_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_text_required',N'Inserire una descrizione della soluzione.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_text_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_text_required',N'Enter a description of the solution.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_text_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_text_required',N'Introduceți o descriere a soluției.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_text_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_text_required',N'Beschreibung der Lösung eingeben.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_text_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_text_required',N'Ange en beskrivning av lösningen.');
GO

-- inc_sol_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='inc_sol_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'inc_sol_title',N'Soluzioni — Ricezione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='inc_sol_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'inc_sol_title',N'Solutions — Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='inc_sol_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'inc_sol_title',N'Soluții — Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='inc_sol_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'inc_sol_title',N'Lösungen — Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='inc_sol_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'inc_sol_title',N'Lösningar — Inleverans');
GO

-- incoming_setup_col_emails
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_col_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_col_emails',N'Email destinatari (separate da ; o ,)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_col_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_col_emails',N'Recipient emails (separated by ; or ,)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_col_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_col_emails',N'Email destinatari (separate prin ; sau ,)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_col_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_col_emails',N'Empfänger-E-Mails (getrennt durch ; oder ,)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_col_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_col_emails',N'Mottagarens e-post (separerade med ; eller ,)');
GO

-- incoming_setup_col_reminders
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_col_reminders')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_col_reminders',N'Reminder/giorno');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_col_reminders')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_col_reminders',N'Reminders/day');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_col_reminders')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_col_reminders',N'Reminder/zi');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_col_reminders')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_col_reminders',N'Erinnerungen/Tag');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_col_reminders')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_col_reminders',N'Påminnelser/dag');
GO

-- incoming_setup_col_type
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_col_type',N'Tipo richiesta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_col_type',N'Request type');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_col_type',N'Tip cerere');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_col_type',N'Anfrageart');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_col_type')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_col_type',N'Förfrågningstyp');
GO

-- incoming_setup_email_frame
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_email_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_email_frame',N'Destinatari email e reminder per tipo di richiesta');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_email_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_email_frame',N'Email recipients and reminders per request type');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_email_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_email_frame',N'Destinatari email și reminder pe tip cerere');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_email_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_email_frame',N'E-Mail-Empfänger und Erinnerungen pro Anfrageart');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_email_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_email_frame',N'E-postmottagare och påminnelser per förfrågningstyp');
GO

-- incoming_setup_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_header',N'Configurazione modulo Ricezione (Incoming)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_header',N'Receiving module configuration');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_header',N'Configurare modul Recepție (Incoming)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_header',N'Konfiguration Wareneingang-Modul');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_header',N'Konfiguration inleveransmodul');
GO

-- incoming_setup_invalid_emails
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_invalid_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_invalid_emails',N'I seguenti indirizzi non sono validi e non verranno salvati:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_invalid_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_invalid_emails',N'The following addresses are invalid and will not be saved:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_invalid_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_invalid_emails',N'Următoarele adrese nu sunt valide și nu vor fi salvate:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_invalid_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_invalid_emails',N'Die folgenden Adressen sind ungültig und werden nicht gespeichert:
{0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_invalid_emails')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_invalid_emails',N'Följande adresser är ogiltiga och sparas inte:
{0}');
GO

-- incoming_setup_monthly_frame
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_monthly_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_monthly_frame',N'Destinatari report mensile (soluzione problemi)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_monthly_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_monthly_frame',N'Monthly report recipients (problem solving)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_monthly_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_monthly_frame',N'Destinatari raport lunar (soluționare probleme)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_monthly_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_monthly_frame',N'Empfänger des Monatsberichts (Problemlösung)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_monthly_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_monthly_frame',N'Mottagare av månadsrapport (problemlösning)');
GO

-- incoming_setup_reminders_hint
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_reminders_hint')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_reminders_hint',N'I reminder sono popup/email ripetuti giornalmente per ogni richiesta ancora in sospeso.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_reminders_hint')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_reminders_hint',N'Reminders are popup/emails repeated daily for each request still pending.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_reminders_hint')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_reminders_hint',N'Reminder-ele sunt popup/email repetate zilnic pentru fiecare cerere încă în suspensie.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_reminders_hint')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_reminders_hint',N'Erinnerungen sind Popup/E-Mails, die täglich für jede ausstehende Anfrage wiederholt werden.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_reminders_hint')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_reminders_hint',N'Påminnelser är popup/e-post som upprepas dagligen för varje väntande begäran.');
GO

-- incoming_setup_save_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_save_error',N'Errore durante il salvataggio');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_save_error',N'Error while saving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_save_error',N'Eroare la salvare');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_save_error',N'Fehler beim Speichern');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_save_error',N'Fel vid sparande');
GO

-- incoming_setup_saved
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_saved',N'Configurazione salvata con successo.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_saved',N'Configuration saved successfully.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_saved',N'Configurare salvată cu succes.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_saved',N'Konfiguration erfolgreich gespeichert.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_saved')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_saved',N'Konfigurationen sparades.');
GO

-- incoming_setup_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_title',N'Setup — Ricezione (Incoming)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_title',N'Setup — Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_title',N'Configurare — Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_title',N'Einrichtung — Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_title',N'Inställningar — Inleverans');
GO

-- incoming_setup_workstation_frame
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_workstation_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_workstation_frame',N'Postazione (questo PC)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_workstation_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_workstation_frame',N'Workstation (this PC)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_workstation_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_workstation_frame',N'Stație (acest PC)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_workstation_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_workstation_frame',N'Workstation (dieser PC)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_workstation_frame')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_workstation_frame',N'Workstation (den här datorn)');
GO

-- incoming_setup_ws_none
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_ws_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_ws_none',N'nessuno');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_ws_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_ws_none',N'none');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_ws_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_ws_none',N'niciunul');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_ws_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_ws_none',N'keiner');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_ws_none')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_ws_none',N'ingen');
GO

-- incoming_setup_ws_open
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_ws_open')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_ws_open',N'Configura postazione…');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_ws_open')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_ws_open',N'Configure workstation…');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_ws_open')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_ws_open',N'Configurează stația…');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_ws_open')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_ws_open',N'Workstation konfigurieren…');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_ws_open')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_ws_open',N'Konfigurera workstation…');
GO

-- incoming_setup_ws_roles
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_setup_ws_roles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_setup_ws_roles',N'Ruoli attivi: {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_setup_ws_roles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_setup_ws_roles',N'Active roles: {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_setup_ws_roles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_setup_ws_roles',N'Roluri active: {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_setup_ws_roles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_setup_ws_roles',N'Aktive Rollen: {0}');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_setup_ws_roles')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_setup_ws_roles',N'Aktiva roller: {0}');
GO

-- incoming_ws_activate
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_activate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_activate',N'✅ Attiva');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_activate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_activate',N'✅ Activate');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_activate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_activate',N'✅ Activează');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_activate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_activate',N'✅ Aktivieren');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_activate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_activate',N'✅ Aktivera');
GO

-- incoming_ws_activated
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_activated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_activated',N'Ruolo attivato con successo.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_activated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_activated',N'Role activated successfully.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_activated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_activated',N'Rol activat cu succes.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_activated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_activated',N'Rolle erfolgreich aktiviert.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_activated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_activated',N'Roll aktiverad.');
GO

-- incoming_ws_confirm_deactivate
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_confirm_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_confirm_deactivate',N'Sei sicuro di voler disattivare questo ruolo?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_confirm_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_confirm_deactivate',N'Are you sure you want to deactivate this role?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_confirm_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_confirm_deactivate',N'Sigur doriți să dezactivați acest rol?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_confirm_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_confirm_deactivate',N'Diese Rolle wirklich deaktivieren?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_confirm_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_confirm_deactivate',N'Vill du verkligen inaktivera den här rollen?');
GO

-- incoming_ws_confirm_deactivate_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_confirm_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_confirm_deactivate_all',N'Disattivare TUTTI i ruoli Incoming su questo PC?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_confirm_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_confirm_deactivate_all',N'Deactivate ALL Incoming roles on this PC?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_confirm_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_confirm_deactivate_all',N'Dezactivați TOATE rolurile Incoming pe acest PC?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_confirm_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_confirm_deactivate_all',N'ALLE Incoming-Rollen auf diesem PC deaktivieren?');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_confirm_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_confirm_deactivate_all',N'Inaktivera ALLA Incoming-roller på den här datorn?');
GO

-- incoming_ws_deactivate
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_deactivate',N'❌ Disattiva');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_deactivate',N'❌ Deactivate');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_deactivate',N'❌ Dezactivează');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_deactivate',N'❌ Deaktivieren');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_deactivate')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_deactivate',N'❌ Inaktivera');
GO

-- incoming_ws_deactivate_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_deactivate_all',N'Disattiva tutto');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_deactivate_all',N'Deactivate all');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_deactivate_all',N'Dezactivează tot');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_deactivate_all',N'Alle deaktivieren');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_deactivate_all')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_deactivate_all',N'Inaktivera alla');
GO

-- incoming_ws_deactivated
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_deactivated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_deactivated',N'Ruolo disattivato con successo.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_deactivated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_deactivated',N'Role deactivated successfully.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_deactivated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_deactivated',N'Rol dezactivat cu succes.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_deactivated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_deactivated',N'Rolle erfolgreich deaktiviert.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_deactivated')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_deactivated',N'Roll inaktiverad.');
GO

-- incoming_ws_desc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_desc',N'Identifica questo computer come postazione del modulo Ricezione.
"Ricevitore" mostra i popup delle nuove richieste ed escalation;
"Mittente" invia le richieste dal magazzino incoming.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_desc',N'Identify this computer as a Receiving module workstation.
"Receiver" shows popups for new requests and escalations;
"Sender" sends requests from the incoming warehouse.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_desc',N'Identifică acest computer ca stație a modulului Recepție.
"Receptor" afișează popup-uri pentru cereri noi și escaladări;
"Expeditor" trimite cererile de la depozitul incoming.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_desc',N'Diesen Computer als Workstation des Wareneingang-Moduls festlegen.
"Empfänger" zeigt Popups für neue Anfragen und Eskalationen;
"Absender" sendet Anfragen aus dem Wareneingang-Lager.');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_desc')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_desc',N'Identifiera den här datorn som en workstation för inleveransmodulen.
"Mottagare" visar popup för nya förfrågningar och eskaleringar;
"Avsändare" skickar förfrågningar från incoming-lagret.');
GO

-- incoming_ws_header
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_header',N'Configurazione Postazione Ricezione');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_header',N'Receiving workstation configuration');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_header',N'Configurare stație Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_header',N'Konfiguration Wareneingang-Workstation');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_header')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_header',N'Konfiguration inleveransworkstation');
GO

-- incoming_ws_inactive
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_inactive',N'❌ Ruolo NON attivo');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_inactive',N'❌ Role NOT active');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_inactive',N'❌ Rol NU este activ');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_inactive',N'❌ Rolle NICHT aktiv');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_inactive')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_inactive',N'❌ Roll EJ aktiv');
GO

-- incoming_ws_receiver_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_receiver_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_receiver_label',N'Ricevitore richieste (popup nuove richieste + escalation)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_receiver_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_receiver_label',N'Request receiver (new request + escalation popups)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_receiver_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_receiver_label',N'Receptor cereri (popup cereri noi + escaladare)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_receiver_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_receiver_label',N'Anfragen-Empfänger (Popups neue Anfragen + Eskalation)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_receiver_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_receiver_label',N'Förfrågningsmottagare (popup nya förfrågningar + eskalering)');
GO

-- incoming_ws_sender_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_sender_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_sender_label',N'Mittente richieste (WH incoming; popup di risposta)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_sender_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_sender_label',N'Request sender (WH incoming; answer popup)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_sender_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_sender_label',N'Expeditor cereri (WH incoming; popup răspuns)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_sender_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_sender_label',N'Anfragen-Absender (WH incoming; Antwort-Popup)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_sender_label')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_sender_label',N'Förfrågningsavsändare (WH incoming; svarspopup)');
GO

-- incoming_ws_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='it' AND [TranslationKey]='incoming_ws_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it',N'incoming_ws_title',N'Configurazione Postazione — Ricezione (Incoming)');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='en' AND [TranslationKey]='incoming_ws_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en',N'incoming_ws_title',N'Workstation configuration — Receiving');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='ro' AND [TranslationKey]='incoming_ws_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro',N'incoming_ws_title',N'Configurare stație — Recepție');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='de' AND [TranslationKey]='incoming_ws_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de',N'incoming_ws_title',N'Workstation-Konfiguration — Wareneingang');
GO
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode]='sv' AND [TranslationKey]='incoming_ws_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv',N'incoming_ws_title',N'Workstation-konfiguration — Inleverans');
GO

