@echo off
REM Installa il servizio di notifiche in Task Scheduler Windows.
REM Il servizio si avvia automaticamente all'accesso dell'utente.
REM Esegui come Amministratore se vuoi impostare "Esegui con i privilegi massimi".

set "TASK_NAME=TraceabilityRS Background Notifications"
set "SCRIPT_DIR=%~dp0"
set "RUN_SCRIPT=%SCRIPT_DIR%run_background_service.bat"

echo Creazione task "%TASK_NAME%"...
echo Script avviato: %RUN_SCRIPT%

schtasks /CREATE /TN "%TASK_NAME%" /TR "\"%RUN_SCRIPT%\"" /SC ONLOGON /F

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: impossibile creare il task. Prova a eseguire questo batch come Amministratore.
    pause
    exit /b 1
)

echo.
echo Task creato con successo.
echo.
echo Per testare subito il servizio usa:
echo   schtasks /RUN /TN "%TASK_NAME%"
echo.
pause
