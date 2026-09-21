@echo off
REM Variante di debug: avvia il server kanban CON console, per vedere i log in tempo reale.
REM Utile per la prima installazione o in caso di problemi.
REM Chiudere la finestra ferma il server.

cd /d "%~dp0.."

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" wip_kanban\web_server.py
) else (
    python.exe wip_kanban\web_server.py
)

pause
