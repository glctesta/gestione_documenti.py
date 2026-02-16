-- =============================================
-- Script SQL per traduzioni Dashboard NPI
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: RO, IT, EN, DE, SV
-- =============================================

USE [Traceability_RS]
GO

-- =============================================
-- Chiave: npi_reopen_project
-- Descrizione: Etichetta menu contestuale per riaprire progetto
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_reopen_project', N'Redeschide Proiect');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_reopen_project', N'Riapri Progetto');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_reopen_project', N'Reopen Project');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_reopen_project', N'Projekt wiedereröffnen');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_reopen_project', N'Återöppna projekt');

GO

-- =============================================
-- Chiave: npi_reopen_project_confirm
-- Descrizione: Messaggio di conferma riapertura progetto
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_confirm' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_reopen_project_confirm', N'Sigur doriți să redeschideți proiectul ''{0}''?

Proiectul va reveni la starea ''Activ''.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_confirm' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_reopen_project_confirm', N'Sei sicuro di voler riaprire il progetto ''{0}''?

Il progetto tornerà allo stato ''Attivo''.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_confirm' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_reopen_project_confirm', N'Are you sure you want to reopen project ''{0}''?

The project will return to ''Active'' status.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_confirm' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_reopen_project_confirm', N'Sind Sie sicher, dass Sie das Projekt ''{0}'' wiedereröffnen möchten?

Das Projekt kehrt zum Status ''Aktiv'' zurück.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_confirm' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_reopen_project_confirm', N'Är du säker på att du vill återöppna projektet ''{0}''?

Projektet återgår till status ''Aktiv''.');

GO

-- =============================================
-- Chiave: npi_reopen_project_success
-- Descrizione: Messaggio di successo riapertura progetto
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_success' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_reopen_project_success', N'Proiectul ''{0}'' a fost redeschis cu succes.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_success' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_reopen_project_success', N'Progetto ''{0}'' riaperto con successo.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_success' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_reopen_project_success', N'Project ''{0}'' reopened successfully.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_success' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_reopen_project_success', N'Projekt ''{0}'' erfolgreich wiedereröffnet.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_success' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_reopen_project_success', N'Projektet ''{0}'' återöppnades framgångsrikt.');

GO

-- =============================================
-- Chiave: npi_reopen_project_failed
-- Descrizione: Messaggio di errore riapertura progetto
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_failed' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_reopen_project_failed', N'Imposibil de redeschis proiectul.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_failed' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_reopen_project_failed', N'Impossibile riaprire il progetto.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_failed' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_reopen_project_failed', N'Unable to reopen the project.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_failed' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_reopen_project_failed', N'Projekt kann nicht wiedereröffnet werden.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_reopen_project_failed' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_reopen_project_failed', N'Det går inte att återöppna projektet.');

GO

-- =============================================
-- Chiave: npi_project_auto_closed
-- Descrizione: Messaggio quando progetto viene auto-chiuso
-- =============================================

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_auto_closed' AND [LanguageCode] = N'ro')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'npi_project_auto_closed', N'Task actualizat cu succes.

✅ PROIECT FINALIZAT!

Toate task-urile alocate au fost finalizate.
Proiectul a fost închis automat.

Pentru a redeschide proiectul folosește Dashboard-ul.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_auto_closed' AND [LanguageCode] = N'it')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'npi_project_auto_closed', N'Task aggiornato con successo.

✅ PROGETTO COMPLETATO!

Tutti i task assegnati sono stati completati.
Il progetto è stato automaticamente chiuso.

Per riaprire il progetto usa il Dashboard.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_auto_closed' AND [LanguageCode] = N'en')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'npi_project_auto_closed', N'Task updated successfully.

✅ PROJECT COMPLETED!

All assigned tasks have been completed.
The project has been automatically closed.

To reopen the project use the Dashboard.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_auto_closed' AND [LanguageCode] = N'de')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'npi_project_auto_closed', N'Aufgabe erfolgreich aktualisiert.

✅ PROJEKT ABGESCHLOSSEN!

Alle zugewiesenen Aufgaben wurden abgeschlossen.
Das Projekt wurde automatisch geschlossen.

Um das Projekt wiederzueröffnen, verwenden Sie das Dashboard.');

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = N'npi_project_auto_closed' AND [LanguageCode] = N'sv')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'npi_project_auto_closed', N'Uppgift uppdaterad framgångsrikt.

✅ PROJEKT SLUTFÖRT!

Alla tilldelade uppgifter har slutförts.
Projektet har stängts automatiskt.

För att återöppna projektet använd Dashboard.');

GO

PRINT N'Script completato! Aggiunte traduzioni per funzionalità Dashboard NPI.';
PRINT N'Chiavi tradotte: npi_reopen_project, npi_reopen_project_confirm, npi_reopen_project_success, npi_reopen_project_failed, npi_project_auto_closed';
PRINT N'Lingue: RO, IT, EN, DE, SV';
GO
