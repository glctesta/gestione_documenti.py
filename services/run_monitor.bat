@echo off
REM ============================================================================
REM Monitor kanban WIP/REPAIR — avvio senza Python.
REM Legge display_config.json (stessa cartella di questo .bat) e apre il display
REM del server :6505 in Chrome kiosk (a schermo intero). Se Chrome non e' presente
REM apre il browser predefinito.
REM
REM Installazione sul PC monitor:
REM   1. copiare questo .bat e display_config.json (da wip_kanban\display_config.example.json)
REM      in una cartella qualsiasi, es. C:\KanbanMonitor\
REM   2. modificare display_config.json: area = "WIP" oppure "REPAIR", deposit, server
REM   3. (opzionale) creare un collegamento a questo .bat in shell:startup per l'avvio automatico
REM ============================================================================
set "MONITOR_DIR=%~dp0"
if not exist "%MONITOR_DIR%display_config.json" (
    echo [ERRORE] display_config.json non trovato in %MONITOR_DIR%
    echo Copiare wip_kanban\display_config.example.json in display_config.json e adattarlo.
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = Get-Content '%MONITOR_DIR%display_config.json' -Raw | ConvertFrom-Json; $u = 'http://{0}:{1}/display?area={2}&deposit={3}' -f $c.server, $c.port, $c.area, $c.deposit; $k = @($env:ProgramFiles + '\Google\Chrome\Application\chrome.exe', ${env:ProgramFiles(x86)} + '\Google\Chrome\Application\chrome.exe', $env:LOCALAPPDATA + '\Google\Chrome\Application\chrome.exe') | Where-Object { Test-Path $_ } | Select-Object -First 1; if ($k) { Start-Process $k -ArgumentList '--kiosk', $u } else { Start-Process $u }"
