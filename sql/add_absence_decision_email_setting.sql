-- ============================================================
-- Aggiunge la voce di settings per le email di notifica
-- approvazione/rifiuto richieste di assenza.
-- Modificare il campo value con gli indirizzi email desiderati
-- separati da virgola o punto e virgola.
-- ============================================================

USE traceability_rs;
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.settings WHERE atribute = 'Sys_email_absence_decision'
)
BEGIN
    INSERT INTO dbo.settings (atribute, [value], [description])
    VALUES (
        'Sys_email_absence_decision',
        '',   -- <-- inserire qui gli indirizzi email HR/CC separati da virgola
        'Indirizzi email in CC per notifiche di approvazione/rifiuto richieste di assenza (separati da virgola o punto e virgola)'
    );
    PRINT 'Setting Sys_email_absence_decision inserito.';
END
ELSE
BEGIN
    PRINT 'Setting Sys_email_absence_decision gia'' presente. Nessuna modifica.';
END
GO
