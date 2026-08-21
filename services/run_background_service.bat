@echo off
REM Avvia il servizio di notifiche popup in background (nessuna console).
REM La directory di lavoro viene impostata sulla cartella del progetto (root).

REM Il batch risiede in services\, quindi risaliamo di un livello.
cd /d "%~dp0.."

REM Usa pythonw.exe dall'ambiente virtuale locale, se presente.
REM Altrimenti prova il pythonw di sistema. Se il tuo ambiente Python è altrove,
REM modifica la riga sottostante con il percorso corretto.
if exist ".venv\Scripts\pythonw.exe" (
    ".venv\Scripts\pythonw.exe" background_notification_service.py
) else (
    pythonw.exe background_notification_service.py
)
