-- =============================================
-- Script SQL: Traduzioni NPI Project Management
-- Aggiunge traduzioni per i nuovi messaggi
-- Lingue: IT, EN, RO, DE, SV
-- =============================================

-- 1. Messaggio: Owner Progetto Mancante (Titolo)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_title' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_missing_owner_title', N'Owner Progetto Mancante');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_title' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_missing_owner_title', N'Project Owner Missing');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_title' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_missing_owner_title', N'Proprietar Proiect Lipsă');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_title' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_missing_owner_title', N'Projektbesitzer Fehlt');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_title' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_missing_owner_title', N'Projektägare Saknas');

-- 2. Messaggio: Owner Progetto Mancante (Messaggio)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_message' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_missing_owner_message', N'⚠️ OWNER PROGETTO MANCANTE

Questo progetto non può essere gestito perché non ha un Owner assegnato.

Per risolvere:
1. Vai alla configurazione progetti NPI
2. Assegna un Owner al progetto
3. Riprova ad aprire il progetto');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_message' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_missing_owner_message', N'⚠️ PROJECT OWNER MISSING

This project cannot be managed because it has no assigned Owner.

To resolve:
1. Go to NPI project configuration
2. Assign an Owner to the project
3. Try to open the project again');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_message' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_missing_owner_message', N'⚠️ PROPRIETAR PROIECT LIPSĂ

Acest proiect nu poate fi gestionat deoarece nu are un proprietar atribuit.

Pentru a rezolva:
1. Accesați configurarea proiectelor NPI
2. Atribuiți un proprietar proiectului
3. Încercați din nou să deschideți proiectul');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_message' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_missing_owner_message', N'⚠️ PROJEKTBESITZER FEHLT

Dieses Projekt kann nicht verwaltet werden, da kein Besitzer zugewiesen ist.

Zur Behebung:
1. Gehen Sie zur NPI-Projektkonfiguration
2. Weisen Sie dem Projekt einen Besitzer zu
3. Versuchen Sie erneut, das Projekt zu öffnen');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_missing_owner_message' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_missing_owner_message', N'⚠️ PROJEKTÄGARE SAKNAS

Detta projekt kan inte hanteras eftersom det inte har någon tilldelad ägare.

För att lösa:
1. Gå till NPI-projektkonfiguration
2. Tilldela en ägare till projektet
3. Försök öppna projektet igen');

-- 3. Messaggio: Accesso Negato - Nessun Task (Titolo)
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_title' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_no_tasks_title', N'Accesso Negato');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_title' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_no_tasks_title', N'Access Denied');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_title' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_no_tasks_title', N'Acces Refuzat');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_title' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_no_tasks_title', N'Zugriff Verweigert');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_title' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_no_tasks_title', N'Åtkomst Nekad');

-- 4. Messaggio: Accesso Negato - Nessun Task (Messaggio)
-- Nota: Questo messaggio usa una f-string in Python, quindi la traduzione è generica
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_message' AND [LanguageCode] = 'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_no_tasks_message', N'⚠️ ACCESSO NEGATO AL PROGETTO

L''utente "{0}" non ha task assegnati in questo progetto.

Non è possibile accedere alle risorse del progetto senza task assegnati.

Contatta il Project Owner per richiedere l''assegnazione di task.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_message' AND [LanguageCode] = 'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_no_tasks_message', N'⚠️ PROJECT ACCESS DENIED

User "{0}" has no assigned tasks in this project.

Cannot access project resources without assigned tasks.

Contact the Project Owner to request task assignment.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_message' AND [LanguageCode] = 'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_no_tasks_message', N'⚠️ ACCES LA PROIECT REFUZAT

Utilizatorul "{0}" nu are sarcini atribuite în acest proiect.

Nu se poate accesa resursele proiectului fără sarcini atribuite.

Contactați proprietarul proiectului pentru a solicita atribuirea de sarcini.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_message' AND [LanguageCode] = 'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_no_tasks_message', N'⚠️ PROJEKTZUGRIFF VERWEIGERT

Benutzer "{0}" hat keine zugewiesenen Aufgaben in diesem Projekt.

Zugriff auf Projektressourcen ohne zugewiesene Aufgaben nicht möglich.

Kontaktieren Sie den Projektbesitzer, um eine Aufgabenzuweisung anzufordern.');

IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [TranslationKey] = 'npi_no_tasks_message' AND [LanguageCode] = 'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_no_tasks_message', N'⚠️ PROJEKTÅTKOMST NEKAD

Användare "{0}" har inga tilldelade uppgifter i detta projekt.

Kan inte komma åt projektresurser utan tilldelade uppgifter.

Kontakta projektägaren för att begära uppgiftstilldelning.');

GO

PRINT '✅ Traduzioni NPI aggiunte con successo!';
PRINT 'Chiavi aggiunte:';
PRINT '  - npi_missing_owner_title';
PRINT '  - npi_missing_owner_message';
PRINT '  - npi_no_tasks_title';
PRINT '  - npi_no_tasks_message';
