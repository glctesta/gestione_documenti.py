@echo off
REM Avvia il server web Kanban produzione (porta 6500) in background, senza console.
REM La directory di lavoro viene impostata sulla cartella del progetto (root),
REM dove devono trovarsi db_config.enc, encryption_key.key ecc.

REM Il batch risiede in services\, quindi risaliamo di un livello.
cd /d "%~dp0.."

REM Usa pythonw.exe dall'ambiente virtuale locale, se presente.
REM Altrimenti prova il pythonw di sistema. Se il tuo ambiente Python è altrove,
REM modifica la riga sottostante con il percorso corretto.
if exist ".venv\Scripts\pythonw.exe" (
    ".venv\Scripts\pythonw.exe" wip_kanban\web_server.py
) else (
    pythonw.exe wip_kanban\web_server.py
)
