-- ============================================================================
-- Script: ADD_TRANSLATIONS_NPI_DELETE_TASK.sql
-- Descrizione: Aggiunge traduzioni per l'eliminazione task dal progetto
-- Data: 2026-01-14
-- Autore: Sistema
-- ============================================================================

USE [Traceability_RS];
GO

-- ========================================
-- btn_delete_task
-- ========================================

-- IT: Elimina Task
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'btn_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'btn_delete_task', 'Elimina Task');
    PRINT 'Traduzione IT aggiunta: btn_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: btn_delete_task';
END
GO

-- RO: Șterge Task
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'btn_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'btn_delete_task', 'Șterge Task');
    PRINT 'Traduzione RO aggiunta: btn_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: btn_delete_task';
END
GO

-- EN: Delete Task
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'btn_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'btn_delete_task', 'Delete Task');
    PRINT 'Traduzione EN aggiunta: btn_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: btn_delete_task';
END
GO

-- DE: Task Löschen
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'btn_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'btn_delete_task', 'Task Löschen');
    PRINT 'Traduzione DE aggiunta: btn_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: btn_delete_task';
END
GO

-- SV: Ta bort Uppgift
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'btn_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'btn_delete_task', 'Ta bort Uppgift');
    PRINT 'Traduzione SV aggiunta: btn_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: btn_delete_task';
END
GO

-- ========================================
-- error_cannot_delete_task_has_dependents
-- ========================================
-- Nota: Messaggio con parametri dinamici (nomi task)

-- IT: Impossibile eliminare il task. Altri task dipendono da esso.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'error_cannot_delete_task_has_dependents'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'error_cannot_delete_task_has_dependents', 'Impossibile eliminare il task. Altri task dipendono da esso.');
    PRINT 'Traduzione IT aggiunta: error_cannot_delete_task_has_dependents';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: error_cannot_delete_task_has_dependents';
END
GO

-- RO: Nu se poate șterge taskul. Alte taskuri depind de acesta.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'error_cannot_delete_task_has_dependents'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'error_cannot_delete_task_has_dependents', 'Nu se poate șterge taskul. Alte taskuri depind de acesta.');
    PRINT 'Traduzione RO aggiunta: error_cannot_delete_task_has_dependents';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: error_cannot_delete_task_has_dependents';
END
GO

-- EN: Cannot delete task. Other tasks depend on it.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'error_cannot_delete_task_has_dependents'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'error_cannot_delete_task_has_dependents', 'Cannot delete task. Other tasks depend on it.');
    PRINT 'Traduzione EN aggiunta: error_cannot_delete_task_has_dependents';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: error_cannot_delete_task_has_dependents';
END
GO

-- DE: Task kann nicht gelöscht werden. Andere Tasks hängen davon ab.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'error_cannot_delete_task_has_dependents'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'error_cannot_delete_task_has_dependents', 'Task kann nicht gelöscht werden. Andere Tasks hängen davon ab.');
    PRINT 'Traduzione DE aggiunta: error_cannot_delete_task_has_dependents';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: error_cannot_delete_task_has_dependents';
END
GO

-- SV: Kan inte ta bort uppgiften. Andra uppgifter beror på den.
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'error_cannot_delete_task_has_dependents'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'error_cannot_delete_task_has_dependents', 'Kan inte ta bort uppgiften. Andra uppgifter beror på den.');
    PRINT 'Traduzione SV aggiunta: error_cannot_delete_task_has_dependents';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: error_cannot_delete_task_has_dependents';
END
GO

-- ========================================
-- confirm_delete_task
-- ========================================

-- IT: Sei sicuro di voler eliminare questo task dal progetto?
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'IT' AND [TranslationKey] = 'confirm_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('IT', 'confirm_delete_task', 'Sei sicuro di voler eliminare questo task dal progetto?');
    PRINT 'Traduzione IT aggiunta: confirm_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione IT già esistente: confirm_delete_task';
END
GO

-- RO: Ești sigur că vrei să ștergi acest task din proiect?
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'RO' AND [TranslationKey] = 'confirm_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('RO', 'confirm_delete_task', 'Ești sigur că vrei să ștergi acest task din proiect?');
    PRINT 'Traduzione RO aggiunta: confirm_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione RO già esistente: confirm_delete_task';
END
GO

-- EN: Are you sure you want to delete this task from the project?
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'EN' AND [TranslationKey] = 'confirm_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('EN', 'confirm_delete_task', 'Are you sure you want to delete this task from the project?');
    PRINT 'Traduzione EN aggiunta: confirm_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione EN già esistente: confirm_delete_task';
END
GO

-- DE: Sind Sie sicher, dass Sie diesen Task aus dem Projekt löschen möchten?
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'DE' AND [TranslationKey] = 'confirm_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('DE', 'confirm_delete_task', 'Sind Sie sicher, dass Sie diesen Task aus dem Projekt löschen möchten?');
    PRINT 'Traduzione DE aggiunta: confirm_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione DE già esistente: confirm_delete_task';
END
GO

-- SV: Är du säker på att du vill ta bort denna uppgift från projektet?
IF NOT EXISTS (
    SELECT 1 FROM [dbo].[AppTranslations] 
    WHERE [LanguageCode] = 'SV' AND [TranslationKey] = 'confirm_delete_task'
)
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES ('SV', 'confirm_delete_task', 'Är du säker på att du vill ta bort denna uppgift från projektet?');
    PRINT 'Traduzione SV aggiunta: confirm_delete_task';
END
ELSE
BEGIN
    PRINT 'Traduzione SV già esistente: confirm_delete_task';
END
GO

PRINT '';
PRINT '============================================================================';
PRINT 'Script completato con successo!';
PRINT 'Traduzioni per eliminazione task verificate/aggiunte per:';
PRINT '  - btn_delete_task';
PRINT '  - error_cannot_delete_task_has_dependents';
PRINT '  - confirm_delete_task';
PRINT 'Lingue: IT, RO, EN, DE, SV';
PRINT '============================================================================';
GO
