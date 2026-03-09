-- Script SQL per traduzioni Owner Progetto Obbligatorio
-- Eseguire su database TraceabilityRS

-- Titolo errore: Owner Progetto Mancante
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_missing_owner_title', N'Owner Progetto Mancante');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_missing_owner_title', N'Project Owner Missing');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_missing_owner_title', N'Projektbesitzer fehlt');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_missing_owner_title', N'Proprietar Proiect Lipsă');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_missing_owner_title', N'Projektägare saknas');

-- Messaggio errore: Owner Progetto Mancante
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_message' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_missing_owner_message', N'⚠️ OWNER PROGETTO MANCANTE

Questo progetto non può essere gestito perché non ha un Owner assegnato.

Per risolvere:
1. Vai alla configurazione progetti NPI
2. Assegna un Owner al progetto
3. Riprova ad aprire il progetto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_message' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_missing_owner_message', N'⚠️ PROJECT OWNER MISSING

This project cannot be managed because it has no assigned Owner.

To resolve:
1. Go to NPI project configuration
2. Assign an Owner to the project
3. Try opening the project again');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_message' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_missing_owner_message', N'⚠️ PROJEKTBESITZER FEHLT

Dieses Projekt kann nicht verwaltet werden, da kein Besitzer zugewiesen ist.

Zur Behebung:
1. Gehen Sie zur NPI-Projektkonfiguration
2. Weisen Sie dem Projekt einen Besitzer zu
3. Versuchen Sie erneut, das Projekt zu öffnen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_message' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_missing_owner_message', N'⚠️ PROPRIETAR PROIECT LIPSĂ

Acest proiect nu poate fi gestionat deoarece nu are un proprietar alocat.

Pentru a rezolva:
1. Mergi la configurarea proiectelor NPI
2. Alocă un proprietar proiectului
3. Încearcă să deschizi din nou proiectul');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_missing_owner_message' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_missing_owner_message', N'⚠️ PROJEKTÄGARE SAKNAS

Detta projekt kan inte hanteras eftersom det inte har någon tilldelad ägare.

För att lösa:
1. Gå till NPI-projektkonfiguration
2. Tilldela en ägare till projektet
3. Försök öppna projektet igen');

-- Titolo errore: Owner Obbligatorio (per creazione)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_title' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_owner_required_title', N'Owner Obbligatorio');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_title' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_owner_required_title', N'Owner Required');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_title' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_owner_required_title', N'Besitzer erforderlich');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_title' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_owner_required_title', N'Proprietar Obligatoriu');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_title' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_owner_required_title', N'Ägare krävs');

-- Messaggio errore: Owner Obbligatorio (per creazione)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_message' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_owner_required_message', N'⚠️ OWNER PROGETTO OBBLIGATORIO

Non è possibile creare un progetto senza un Owner.

Seleziona un Owner dal menu a tendina prima di salvare.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_message' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_owner_required_message', N'⚠️ PROJECT OWNER REQUIRED

Cannot create a project without an Owner.

Select an Owner from the dropdown before saving.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_message' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_owner_required_message', N'⚠️ PROJEKTBESITZER ERFORDERLICH

Ein Projekt kann nicht ohne Besitzer erstellt werden.

Wählen Sie einen Besitzer aus dem Dropdown-Menü, bevor Sie speichern.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_message' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_owner_required_message', N'⚠️ PROPRIETAR PROIECT OBLIGATORIU

Nu se poate crea un proiect fără un proprietar.

Selectați un proprietar din meniul derulant înainte de a salva.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_owner_required_message' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_owner_required_message', N'⚠️ PROJEKTÄGARE KRÄVS

Kan inte skapa ett projekt utan en ägare.

Välj en ägare från rullgardinsmenyn innan du sparar.');

-- Label: Owner Progetto
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_owner_label' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_project_owner_label', N'Owner Progetto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_owner_label' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_project_owner_label', N'Project Owner');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_owner_label' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_project_owner_label', N'Projektbesitzer');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_owner_label' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_project_owner_label', N'Proprietar Proiect');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_owner_label' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_project_owner_label', N'Projektägare');

GO
