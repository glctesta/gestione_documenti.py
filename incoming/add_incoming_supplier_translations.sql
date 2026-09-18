-- Script SQL per le traduzioni dell'inserimento rapido fornitore (Ricezione)
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-09-17
USE [Traceability_RS];
GO

-- inc_req_new_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_new_supplier', N'Nuovo fornitore…');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_new_supplier', N'New supplier…');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_new_supplier', N'Furnizor nou…');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_new_supplier', N'Neuer Lieferant…');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_new_supplier', N'Ny leverantör…');

-- inc_req_new_supplier_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_new_supplier_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_new_supplier_title', N'Inserimento nuovo fornitore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_new_supplier_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_new_supplier_title', N'Add new supplier');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_new_supplier_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_new_supplier_title', N'Adăugare furnizor nou');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_new_supplier_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_new_supplier_title', N'Neuen Lieferanten erfassen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_new_supplier_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_new_supplier_title', N'Lägg till ny leverantör');

-- inc_req_offer_new_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_offer_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_offer_new_supplier', N'Il fornitore "{0}" non e'' in elenco.
Inserirlo ora?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_offer_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_offer_new_supplier', N'Supplier "{0}" is not in the list.
Add it now?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_offer_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_offer_new_supplier', N'Furnizorul "{0}" nu este în listă.
Îl adăugați acum?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_offer_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_offer_new_supplier', N'Lieferant "{0}" ist nicht in der Liste.
Jetzt erfassen?');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_offer_new_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_offer_new_supplier', N'Leverantören "{0}" finns inte i listan.
Lägga till nu?');

-- inc_req_supplier_name
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_supplier_name')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_supplier_name', N'Ragione sociale:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_supplier_name')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_supplier_name', N'Company name:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_supplier_name')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_supplier_name', N'Denumire:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_supplier_name')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_supplier_name', N'Firmenname:');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_supplier_name')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_supplier_name', N'Företagsnamn:');

-- inc_req_supplier_vat
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_supplier_vat')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_supplier_vat', N'Codice IVA / P.IVA (*):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_supplier_vat')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_supplier_vat', N'VAT code (*):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_supplier_vat')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_supplier_vat', N'Cod TVA (*):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_supplier_vat')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_supplier_vat', N'USt-IdNr. (*):');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_supplier_vat')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_supplier_vat', N'Momsnummer (*):');

-- inc_req_vat_mandatory
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_vat_mandatory')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_vat_mandatory', N'(*) Il codice IVA e'' obbligatorio: viene verificato che non esista gia''.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_vat_mandatory')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_vat_mandatory', N'(*) The VAT code is mandatory: it is checked that it does not already exist.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_vat_mandatory')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_vat_mandatory', N'(*) Codul TVA este obligatoriu: se verifică dacă nu există deja.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_vat_mandatory')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_vat_mandatory', N'(*) Die USt-IdNr. ist Pflicht: Es wird geprüft, ob sie bereits existiert.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_vat_mandatory')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_vat_mandatory', N'(*) Momsnumret är obligatoriskt: det kontrolleras att det inte redan finns.');

-- inc_req_save_supplier
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_save_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_save_supplier', N'Salva fornitore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_save_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_save_supplier', N'Save supplier');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_save_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_save_supplier', N'Salvează furnizorul');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_save_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_save_supplier', N'Lieferant speichern');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_save_supplier')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_save_supplier', N'Spara leverantör');

-- inc_req_name_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_name_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_name_required', N'Inserire la ragione sociale del fornitore.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_name_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_name_required', N'Enter the supplier company name.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_name_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_name_required', N'Introduceți denumirea furnizorului.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_name_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_name_required', N'Firmenname des Lieferanten eingeben.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_name_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_name_required', N'Ange leverantörens företagsnamn.');

-- inc_req_vat_required
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_vat_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_vat_required', N'Inserire il codice IVA del fornitore (obbligatorio).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_vat_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_vat_required', N'Enter the supplier VAT code (mandatory).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_vat_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_vat_required', N'Introduceți codul TVA al furnizorului (obligatoriu).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_vat_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_vat_required', N'USt-IdNr. des Lieferanten eingeben (Pflicht).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_vat_required')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_vat_required', N'Ange leverantörens momsnummer (obligatoriskt).');

-- inc_req_name_too_long
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_name_too_long')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_name_too_long', N'Ragione sociale troppo lunga (max 250 caratteri).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_name_too_long')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_name_too_long', N'Company name too long (max 250 characters).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_name_too_long')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_name_too_long', N'Denumire prea lungă (max 250 de caractere).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_name_too_long')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_name_too_long', N'Firmenname zu lang (max. 250 Zeichen).');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_name_too_long')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_name_too_long', N'Företagsnamnet är för långt (max 250 tecken).');

-- inc_req_vat_check_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_vat_check_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_vat_check_error', N'Impossibile verificare il codice IVA:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_vat_check_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_vat_check_error', N'Unable to verify the VAT code:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_vat_check_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_vat_check_error', N'Imposibil de verificat codul TVA:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_vat_check_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_vat_check_error', N'USt-IdNr. konnte nicht geprüft werden:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_vat_check_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_vat_check_error', N'Det gick inte att verifiera momsnumret:
{0}');

-- inc_req_vat_exists
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_vat_exists')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_vat_exists', N'Esiste gia'' una societa'' con questo codice IVA:
{0}

Inserimento rifiutato: selezionare la societa'' esistente.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_vat_exists')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_vat_exists', N'A company with this VAT code already exists:
{0}

Insert rejected: please select the existing company.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_vat_exists')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_vat_exists', N'Există deja o societate cu acest cod TVA:
{0}

Inserare respinsă: selectați societatea existentă.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_vat_exists')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_vat_exists', N'Es existiert bereits ein Unternehmen mit dieser USt-IdNr.:
{0}

Erfassung abgelehnt: Bitte das bestehende Unternehmen auswählen.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_vat_exists')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_vat_exists', N'Det finns redan ett företag med detta momsnummer:
{0}

Infogning nekades: välj det befintliga företaget.');

-- inc_req_similar_title
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_similar_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_similar_title', N'Possibili fornitori esistenti');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_similar_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_similar_title', N'Possible existing suppliers');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_similar_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_similar_title', N'Posibili furnizori existenți');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_similar_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_similar_title', N'Mögliche vorhandene Lieferanten');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_similar_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_similar_title', N'Möjliga befintliga leverantörer');

-- inc_req_similar_msg
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_similar_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_similar_msg', N'Esistono fornitori con nome simile. Verificare che non sia lo stesso prima di inserirne uno nuovo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_similar_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_similar_msg', N'There are suppliers with a similar name. Check that it is not the same one before adding a new one.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_similar_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_similar_msg', N'Există furnizori cu nume similar. Verificați că nu este același înainte de a adăuga unul nou.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_similar_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_similar_msg', N'Es gibt Lieferanten mit ähnlichem Namen. Prüfen Sie, ob es nicht derselbe ist, bevor Sie einen neuen erfassen.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_similar_msg')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_similar_msg', N'Det finns leverantörer med liknande namn. Kontrollera att det inte är samma innan du lägger till en ny.');

-- inc_req_similar_use
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_similar_use')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_similar_use', N'Usa selezionato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_similar_use')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_similar_use', N'Use selected');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_similar_use')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_similar_use', N'Folosește selectatul');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_similar_use')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_similar_use', N'Ausgewählten verwenden');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_similar_use')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_similar_use', N'Använd vald');

-- inc_req_similar_proceed
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_similar_proceed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_similar_proceed', N'Inserisci nuovo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_similar_proceed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_similar_proceed', N'Insert new');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_similar_proceed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_similar_proceed', N'Inserează nou');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_similar_proceed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_similar_proceed', N'Neu erfassen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_similar_proceed')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_similar_proceed', N'Lägg in ny');

-- inc_req_similar_pick
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_similar_pick')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_similar_pick', N'Selezionare un fornitore dall''elenco.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_similar_pick')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_similar_pick', N'Select a supplier from the list.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_similar_pick')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_similar_pick', N'Selectați un furnizor din listă.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_similar_pick')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_similar_pick', N'Wählen Sie einen Lieferanten aus der Liste.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_similar_pick')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_similar_pick', N'Välj en leverantör från listan.');

-- inc_req_supplier_save_error
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_supplier_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_supplier_save_error', N'Errore durante l''inserimento del fornitore:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_supplier_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_supplier_save_error', N'Error while adding the supplier:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_supplier_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_supplier_save_error', N'Eroare la adăugarea furnizorului:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_supplier_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_supplier_save_error', N'Fehler beim Erfassen des Lieferanten:
{0}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_supplier_save_error')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_supplier_save_error', N'Fel vid tillägg av leverantören:
{0}');

-- inc_req_supplier_created
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'inc_req_supplier_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'it', N'inc_req_supplier_created', N'Fornitore "{0}" inserito correttamente.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'inc_req_supplier_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'en', N'inc_req_supplier_created', N'Supplier "{0}" added successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'inc_req_supplier_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'ro', N'inc_req_supplier_created', N'Furnizorul "{0}" a fost adăugat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'inc_req_supplier_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'de', N'inc_req_supplier_created', N'Lieferant "{0}" erfolgreich erfasst.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'inc_req_supplier_created')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue]) VALUES (N'sv', N'inc_req_supplier_created', N'Leverantören "{0}" lades till.');
