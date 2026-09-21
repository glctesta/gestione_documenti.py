@echo off
REM  Avvia il server MioProgetto (porta XXXX)
cd /d "%~dp0"
:loop
echo [%date% %time%] Avvio server window kanban >> console_output.log
.venv\Scripts\python.exe display_server.py >> console_output.log 2>&1
echo [%date% %time%] Server arrestato con codice %errorlevel%. Riavvio in corso... >> console_output.log
ping 127.0.0.1 -n 6 >nul
goto loop