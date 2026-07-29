# Kit Dashboard web server dai SORGENTI Python (server 192.168.10.72)

Obiettivo: far girare il web server della dashboard dai file `.py` invece che
dall'eseguibile frozen, così i **prossimi aggiornamenti web** sono una semplice
copia di file + riavvio del task (niente ricompilazione dell'app).

Il task `KitDashboardServer` lancerà `pythonw.exe kit_web_server.py` (vedi
`install_kit_dashboard_autostart.py` → `_command_and_args`, ramo non-frozen).

---

## Prerequisiti sul server
1. **Python 3.11** installato **"for all users"** (il task gira come SYSTEM: deve
   vedere Python; installazione per-utente NON basta). Spuntare "Add to PATH".
2. Driver **ODBC SQL Server** già presente (lo usa già l'exe).
3. Porta **8090** già aperta nel firewall (invariata).

## Passi (una tantum)

1. **Cartella sorgenti** sul server, es. `C:\KitDashboardSrc\`.

2. **Copia i sorgenti** del progetto in quella cartella: tutti i `.py` + la
   cartella `kit_dashboard\` + `requirements.txt`. (Per sicurezza copia l'intero
   progetto; NON servono `build\`, `dist\`, `.venv\` del PC di sviluppo.)

3. **Copia i 3 file di config** dalla cartella dell'app frozen già presente sul
   server (accanto a `DocumentManagement.exe`) dentro `C:\KitDashboardSrc\`:
   - `db_config.enc`
   - `encryption_key.key`
   - `kit_server_config.json`
   (Il web server legge le credenziali DB da qui, dalla working directory.)

4. **Crea il venv e installa le dipendenze** (prompt come Amministratore):
   ```
   cd /d C:\KitDashboardSrc
   py -3.11 -m venv .venv
   .venv\Scripts\python.exe -m pip install --upgrade pip
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. **Prova manuale** (deve rispondere il web):
   ```
   .venv\Scripts\python.exe kit_web_server.py
   ```
   Apri `http://192.168.10.72:8090/produzione`. Se ok, ferma con Ctrl+C.

6. **Sostituisci il task** (da exe a sorgenti): fermare quello attuale e
   reinstallarlo con il python del venv (così registra il comando corretto):
   ```
   schtasks /End /TN KitDashboardServer
   .venv\Scripts\python.exe install_kit_dashboard_autostart.py
   ```
   Lo script crea il task che lancia
   `C:\KitDashboardSrc\.venv\Scripts\pythonw.exe C:\KitDashboardSrc\kit_web_server.py`
   con WorkingDirectory `C:\KitDashboardSrc`, e lo avvia.
   (In alternativa riavvia il PC, oppure `schtasks /Run /TN KitDashboardServer`.)

7. **Verifica**: `http://192.168.10.72:8090/produzione`.

---

## Aggiornamenti web futuri (semplice copia file)
1. Copia i `.py` cambiati di `kit_dashboard\` (o il contenuto di
   `kit_dashboard_server_update.zip`) SOVRASCRIVENDO in
   `C:\KitDashboardSrc\kit_dashboard\`.
2. Riavvia il servizio:
   ```
   schtasks /End /TN KitDashboardServer
   schtasks /Run /TN KitDashboardServer
   ```
3. Lo snapshot si rigenera entro 5 min (o subito col Refresh nella pagina).

## Note / avvertenze
- Il task gira come **SYSTEM**: Python "for all users", venv su disco **locale**;
  l'account macchina (PC$) deve avere accesso al DB e alla share Planning UNC
  (già così per l'exe).
- Se in futuro cambi anche i moduli importati dal server (es. `fai_autocheck.py`,
  `config_manager.py`), copia anche quelli.
- Per **tornare all'exe**: reinstalla il task dall'app frozen
  (`DocumentManagement.exe --install-kit-dashboard` o rilancia l'installer frozen),
  oppure `schtasks` con il comando exe `--kit-web-server`.
