@echo off
REM Rimuove il task di avvio automatico del servizio notifiche.

set "TASK_NAME=TraceabilityRS Background Notifications"

echo Rimozione task "%TASK_NAME%"...
schtasks /DELETE /TN "%TASK_NAME%" /F

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: impossibile rimuovere il task. Forse e' gia' assente o servono privilegi elevati.
    pause
    exit /b 1
)

echo.
echo Task rimosso con successo.
pause
