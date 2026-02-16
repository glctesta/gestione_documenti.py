-- Script per inserire traduzioni funzionalità riapri progetto NPI
-- Lingue: it, en, ro, de, sv

INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT * FROM (VALUES 
    -- Pulsante riapri progetto
    (N'it', N'btn_reopen_project', N'Riapri Progetto'),
    (N'en', N'btn_reopen_project', N'Reopen Project'),
    (N'ro', N'btn_reopen_project', N'Redeschide Proiect'),
    (N'de', N'btn_reopen_project', N'Projekt wiedereröffnen'),
    (N'sv', N'btn_reopen_project', N'Återöppna Projekt'),
    
    -- Conferma riapertura
    (N'it', N'confirm_reopen_project', N'Sei sicuro di voler riaprire questo progetto?'),
    (N'en', N'confirm_reopen_project', N'Are you sure you want to reopen this project?'),
    (N'ro', N'confirm_reopen_project', N'Sigur doriți să redeschideți acest proiect?'),
    (N'de', N'confirm_reopen_project', N'Möchten Sie dieses Projekt wirklich wiedereröffnen?'),
    (N'sv', N'confirm_reopen_project', N'Är du säker på att du vill återöppna detta projekt?'),
    
    -- Messaggio successo
    (N'it', N'project_reopened', N'Progetto riaperto con successo'),
    (N'en', N'project_reopened', N'Project reopened successfully'),
    (N'ro', N'project_reopened', N'Proiect redeschis cu succes'),
    (N'de', N'project_reopened', N'Projekt erfolgreich wiedereröffnet'),
    (N'sv', N'project_reopened', N'Projekt återöppnat'),
    
    -- Messaggio auto-chiusura
    (N'it', N'project_auto_closed', N'Progetto chiuso automaticamente'),
    (N'en', N'project_auto_closed', N'Project automatically closed'),
    (N'ro', N'project_auto_closed', N'Proiect închis automat'),
    (N'de', N'project_auto_closed', N'Projekt automatisch geschlossen'),
    (N'sv', N'project_auto_closed', N'Projekt automatiskt stängt'),
    
    -- Titolo conferma
    (N'it', N'confirm_reopen_title', N'Conferma Riapertura'),
    (N'en', N'confirm_reopen_title', N'Confirm Reopen'),
    (N'ro', N'confirm_reopen_title', N'Confirmă Redeschidere'),
    (N'de', N'confirm_reopen_title', N'Wiedereröffnung bestätigen'),
    (N'sv', N'confirm_reopen_title', N'Bekräfta Återöppning'),
    
    -- Messaggio errore
    (N'it', N'error_reopen_project', N'Errore durante la riapertura del progetto'),
    (N'en', N'error_reopen_project', N'Error reopening project'),
    (N'ro', N'error_reopen_project', N'Eroare la redeschiderea proiectului'),
    (N'de', N'error_reopen_project', N'Fehler beim Wiedereröffnen des Projekts'),
    (N'sv', N'error_reopen_project', N'Fel vid återöppning av projekt')
) AS Source([LanguageCode], [TranslationKey], [TranslationValue])
WHERE NOT EXISTS (
    SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] t
    WHERE t.[LanguageCode] = Source.[LanguageCode] 
    AND t.[TranslationKey] = Source.[TranslationKey]
);
