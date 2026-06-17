# Kit Production Dashboard — Web Intranet + Server Supervisionato
## Documento di analisi e progettazione — v1.0 (BOZZA, in attesa di conferma)

> **Stato:** analisi pre-implementazione. **Nessuna modifica al codice è stata fatta.**
> Attendo la tua conferma (e le risposte alle *Decisioni aperte*, §13) prima di scrivere codice.

---

## 1. Obiettivi

Realizzare un'applicazione **web su intranet** con due pagine, alimentata e sincronizzata
dal programma desktop esistente (`main.py`, TraceabilityRS):

1. **Pagina Magazzino** — avanzamento in tempo (quasi) reale della preparazione dei kit:
   ordini da preparare, stato di avanzamento, **stima in minuti** al completamento.
2. **Pagina Produzione** — lista dei kit **pronti e disponibili** al prelievo dalla linea,
   stima di quando saranno pronti i prossimi ordini, con **ricerca/filtri**. Gli ordini
   **in ritardo o incompleti** sono evidenziati in **rosso e lampeggianti**, con il **numero
   di codici materiale mancanti**; cliccando sul numero ordine si apre il **dettaglio**
   (materiali richiesti / prelevati / mancanti con quantità).

Vincoli infrastrutturali:

- Il web gira su un **server hostato sul PC `192.168.10.72`** (IP configurabile via file JSON,
  creato con default se assente).
- I dati sono **sincronizzati ogni 5 minuti** dal programma principale (è la sorgente unica).
- **Una sola istanza** del programma (la prima che "vince") avvia e controlla il server,
  evitando sovrapposizioni tra istanze su PC diversi in rete.
- L'installazione su `192.168.10.72` è **manuale**, ma il programma deve poter **verificare**
  che il server sia in esecuzione, **rilanciarlo se inattivo** e — se non è rilanciabile da
  remoto — **avvisare via email/popup** i PC abilitati alla formazione kit (`KIT_PREP`).

---

## 2. Mappatura sui dati esistenti (nessuna invenzione)

Tutto il necessario esiste già nel DB `Traceability_RS`. Tabelle chiave (da setup sprint 1/3):

| Tabella | Uso per la dashboard |
|---|---|
| `picking_lists` (`id, status, upload_date, closed_date, source_file_name`) | stato lista, inizio/fine fase magazzino |
| `picking_list_items` (`picking_list_id, order_number, material_code, qty_required, qty_picked, pick_status, picked_date`) | avanzamento per riga, codici mancanti, quantità |
| `picking_list_orders` (`picking_list_id, order_number`) | mapping lista↔ordini (liste multi-ordine) |
| `kit_status` (`order_number, status, updated_date`) | stato per ordine (vedi lifecycle §2.1) |
| `kit_sessions` (`picking_list_id, phase, started_date, last_activity_date, status`) | timing fasi (WH/PREFORMING/PRODUCTION) |
| `kit_verification_log` (`order_number, event_type, event_date, ...`) | eventi storici per ETA e anomalie |
| `kit_item_checks` (`item_id, phase, qty_expected, qty_actual, check_status`) | verifiche preformatura/produzione (OK/MISMATCH) |
| `material_requests` (`order_number, material_code, qty_requested, wh_status, resolution`) | richieste aperte (bloccano l'avanzamento) |
| `order_priority` (`order_number, priority`) | P0 e ordinamento |
| `Orders`/`Products`/BOM (`ProductComponentsErp`…) | numero ordine, prodotto, quantità, BOM atteso |

### 2.1 Lifecycle stato kit (per ordine, `kit_status.status`)

```
WH_OPEN → WH_PARTIAL/WH_CLOSED → IN_PREFORMING → RECEIVED_IN_PRODUCTION
                 │                      │
                 └──(verifica KO)→ REOPENED       └──(verifica linea KO)→ BLOCKED_MISSING_MATERIAL
```

- **Kit "pronto per la produzione"** = `kit_status.status = 'IN_PREFORMING'` **e** nessuna
  `material_requests` aperta per l'ordine (`resolution IS NULL`).
- **Incompleto/bloccato** = `BLOCKED_MISSING_MATERIAL` oppure `REOPENED` oppure presenza di
  righe con `pick_status IN ('PENDING','PARTIAL','MISSING_FROM_LIST','PENDING_COMPLETION')`.
- **Codici mancanti per ordine** = `COUNT(DISTINCT material_code)` sulle righe con quei
  `pick_status` (e `qty_picked < qty_required`).

### 2.2 Pattern già disponibili da riusare

- **Claim atomico** (`UPDATE … WHERE … IS NULL`, `rowcount`) — usato in
  `kit_popup_monitor.py` e `kit_requests_reminder.py`. Base per l'**elezione del controller**.
- **Flag postazione** (`%LOCALAPPDATA%\*.json`, es. `kit_prep_host.json`) e helper
  `is_kit_prep_workstation()` — per indirizzare gli **alert**.
- **Email**: `utils.get_email_recipients(conn, 'Sys_email_Kit_materiali')` + `utils.send_email(...)`.
- **Popup**: tabella `kit_popup_queue` + `kit_notifications.queue_popup(...)`, target `KIT_PREP`.
- **DB standalone**: `ConfigManager('encryption_key.key','db_config.enc').load_config()` + `pyodbc`.
- **Config JSON con default-se-assente**: pattern `_load/_save_*_setting` in `main.py`
  (lettura, `mkdir parents`, scrittura atomica tmp→replace).
- **Monitor periodici**: pattern `self.after(POLL_INTERVAL_MS, self._poll)` + `threading.Thread(daemon=True)`.
- **Dedup email cross-PC** (memoria `email-dedup-pattern`): claim su tabella di log, no dedup in memoria.

---

## 3. Architettura

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  PC 192.168.10.72  (HOST del server — installazione manuale)           │
   │                                                                        │
   │   main.py (istanza "CONTROLLER", eletta)                               │
   │     ├─ KitDashboardSync   → ogni 5 min: calcola snapshot, scrive in DB │
   │     ├─ KitServerSupervisor→ avvia/sorveglia il processo web (locale)   │
   │     │                        rilancio se morto                         │
   │     └─ heartbeat controller in DB                                      │
   │                                                                        │
   │   kit_web_server.py (Flask)  ── legge lo SNAPSHOT dal DB e serve HTML  │
   │     :8090  /magazzino   /produzione   /ordine/<n>   /health  /api/*    │
   └───────────────────────────▲────────────────────────────────────────────┘
                                │ HTTP intranet
        ┌───────────────────────┼───────────────────────────────────┐
        │                       │                                    │
   Monitor TV magazzino    Monitor TV produzione              PC operatori
   (browser fullscreen)    (browser fullscreen)               (browser)

   ┌──────────────────────────────────────────────────────────────────────┐
   │  Altre istanze main.py (altri PC)  → ruolo STANDBY                     │
   │     └─ KitServerWatcher: ping http://192.168.10.72:8090/health        │
   │         se down e non rilanciabile da remoto → alert KIT_PREP         │
   │         (subentrano come controller se l'host .72 non risponde)       │
   └──────────────────────────────────────────────────────────────────────┘
```

**Principio di sincronizzazione:** la sorgente è il DB. L'istanza **controller** ricalcola
ogni 5 minuti uno **snapshot** (tabelle `kit_dashboard_snapshot*`, §5) che il web server
serve. Così "tutti i dati sono legati al programma" e "sincronizzati ogni 5 minuti", e il web
resta leggero/robusto (legge solo lo snapshot, non query pesanti live).

---

## 4. Componenti software (nuovi file proposti)

| File | Ruolo |
|---|---|
| `kit_dashboard/server_config.py` | lettura/scrittura `kit_server_config.json` (IP, porta, intervalli); crea default se assente |
| `kit_dashboard/sync_service.py` | `KitDashboardSync`: calcolo snapshot + ETA ogni 5 min; scrive in DB |
| `kit_dashboard/eta.py` | modello di stima ETA (vedi §8) |
| `kit_dashboard/controller.py` | elezione controller (claim+heartbeat), avvio sync + supervisor |
| `kit_dashboard/server_supervisor.py` | avvia/sorveglia/rilancia il processo Flask **locale** (solo sull'host) |
| `kit_dashboard/server_watcher.py` | (istanze remote) ping `/health`, takeover, alert |
| `kit_web_server.py` | app **Flask** (entry-point eseguibile sul .72): route + render template |
| `kit_dashboard/templates/*.html` | pagine `magazzino`, `produzione`, `ordine` (Jinja2) |
| `kit_dashboard/static/*` | CSS/JS (auto-refresh, blink, ordinamento client) |
| `setup_kit_dashboard.py` | crea tabelle snapshot + tabella controller/heartbeat |
| `kit_dashboard_translations.sql` | (eventuali) etichette UI multilingua |

Integrazione in `main.py`: una sola riga di avvio nel blocco monitor
(`_start_indirect_materials_monitors` o analogo) che istanzia `KitDashboardController`.

---

## 5. Modello dati — nuove tabelle (snapshot + controllo)

> Nessuna modifica alle tabelle kit esistenti. Solo aggiunte.

### 5.1 `kit_dashboard_snapshot` (1 riga per ordine attivo, riscritta ogni sync)
```
order_number        NVARCHAR(30)  PK
product_code        NVARCHAR(100)
order_qty           DECIMAL(12,3)
priority            TINYINT
kit_status          NVARCHAR(40)        -- WH_OPEN…RECEIVED_IN_PRODUCTION
phase               NVARCHAR(20)         -- WH | PREFORMING | PRODUCTION | DONE
items_total         INT
items_done          INT
pct_complete        DECIMAL(5,2)
missing_codes       INT                  -- # codici mancanti (per badge produzione)
open_requests       INT
is_ready_for_prod   BIT                  -- IN_PREFORMING & nessuna richiesta aperta
is_late             BIT                  -- vedi §7.1 (definizione "in ritardo")
is_incomplete       BIT
eta_minutes         INT                  -- stima al completamento (NULL se ignota)
eta_ready_at        DATETIME             -- ora prevista di disponibilità
list_id             INT
started_date        DATETIME
last_activity_date  DATETIME
snapshot_date       DATETIME             -- timestamp del calcolo (per "aggiornato alle…")
```

### 5.2 `kit_dashboard_snapshot_missing` (dettaglio materiali mancanti per drill-down)
```
order_number    NVARCHAR(30)
material_code   NVARCHAR(100)
qty_required    DECIMAL(12,3)
qty_picked      DECIMAL(12,3)
qty_missing     DECIMAL(12,3)
pick_status     NVARCHAR(20)
snapshot_date   DATETIME
PK (order_number, material_code)
```

> **Aggiunte per D1=B / D8:** `kit_dashboard_snapshot` include anche
> `planned_start DATETIME NULL` (da `T:\Planning`). Lo snapshot rappresenta lo **stato corrente**
> degli ordini attivi; lo **storico** è gestito da `kit_dashboard_history` (§5.4).

### 5.4 `kit_dashboard_history` (storico esiti — D8, persistente)
Upsert ad ogni sync; **non** viene cancellato quando l'ordine completa (a differenza dello snapshot).
```
order_number     NVARCHAR(30) PK
product_code     NVARCHAR(100)
planned_start    DATETIME NULL      -- da T:\Planning
first_seen_date  DATETIME           -- prima comparsa nel kit flow
ready_date       DATETIME NULL      -- quando il kit è diventato pronto (IN_PREFORMING ok)
completed_date   DATETIME NULL      -- RECEIVED_IN_PRODUCTION
was_on_time      BIT NULL           -- ready_date <= planned_start
was_complete     BIT NULL           -- completato senza deroga/mancanti
final_status     NVARCHAR(40)
updated_date     DATETIME
```
La pagina Produzione interroga `kit_dashboard_history` per la vista storica (default 3 giorni su
`completed_date`/`updated_date`, ricerca su ordini più vecchi), con colonne *In tempo* / *Completo*.

### 5.3 `kit_dashboard_controller` (elezione + heartbeat, 1 sola riga logica)
```
lock_name       NVARCHAR(50) PK   -- es. 'KIT_DASHBOARD'
controller_host NVARCHAR(100)     -- hostname dell'istanza controller
controller_ip   NVARCHAR(45)
heartbeat_date  DATETIME          -- aggiornato ogni ~60s
server_state    NVARCHAR(20)      -- RUNNING | DOWN | STARTING | UNREACHABLE
server_pid      INT NULL
last_check_date DATETIME
```
Takeover: se `heartbeat_date` è più vecchio di N minuti (es. 3), un'altra istanza può
reclamare il lock con `UPDATE … WHERE heartbeat_date < DATEADD(MINUTE,-3,GETDATE())` (claim atomico).

---

## 6. Pagina Magazzino (`/magazzino`)

**Scopo:** monitor a parete in magazzino. Auto-refresh ogni 60s (lato browser) sui dati dello
snapshot (ricalcolato ogni 5 min lato controller).

**Contenuto (per ogni ordine in lavorazione, ordinato per priorità poi ETA):**

| Colonna | Fonte |
|---|---|
| Ordine / Prodotto / Qtà | snapshot |
| Stato fase (WH/Preformatura/…) | `kit_status` mappato |
| Avanzamento | barra `pct_complete` (items_done/items_total) |
| Codici mancanti | `missing_codes` (se >0) |
| Stima completamento | `eta_minutes` ("~25 min") + `eta_ready_at` ("pronto ~14:35") |
| Sessione | ACTIVE/SUSPENDED, operatore, ultima attività |

**Indicatori:** P0 evidenziato; sessione SUSPENDED segnalata; ordini fermi da troppo tempo
(nessuna attività da > soglia) evidenziati.

Header con "**Aggiornato alle HH:MM**" (= `snapshot_date`) per chiarezza sul 5-min.

---

## 7. Pagina Produzione (`/produzione`)

**Scopo:** monitor a parete / consultazione lato linea. Due blocchi:

1. **Kit pronti al prelievo** (`is_ready_for_prod = 1`): elenco con ordine, prodotto,
   quantità, da quando è pronto.
2. **Prossimi in arrivo**: ordini non ancora pronti con **ETA** ("pronto ~15:10").

**Ricerca/filtri** (lato client + endpoint `/api/produzione`): per numero ordine, prodotto,
stato, solo-pronti, solo-in-ritardo.

### 7.1 Evidenziazione rosso + blink
- **In ritardo o incompleto** → riga in **rosso lampeggiante** (CSS animation, JS che attiva
  `blink` quando `is_late || is_incomplete`).
- Mostra il **numero di codici mancanti** (`missing_codes`) come badge cliccabile.
- **Definizione "in ritardo" (D1=B, confermata):** il kit è in ritardo se non sarà/è stato
  pronto entro il **`PlannedStart`** dell'ordine, letto dal file `T:\Planning` (tab `PlanningMachine`,
  via `fai_autocheck.read_planning_excel()`). In dettaglio:
  - `is_late = 1` se `NOW > planned_start` e il kit non è ancora pronto, **oppure** `eta_ready_at > planned_start`.
  - Stati `BLOCKED_MISSING_MATERIAL`/`REOPENED` → sempre rosso (incompleto/bloccato).
  - Ordine assente dal file di pianificazione → nessun flag di ritardo (mostra solo lo stato).
  - `planned_start` viene salvato nello snapshot per il confronto e per lo storico.

### 7.2 Drill-down ordine (`/ordine/<order_number>`)
Click sul numero ordine (o sul badge codici mancanti) → pagina dettaglio che elenca, da
`kit_dashboard_snapshot_missing`:

| Codice materiale | Richiesto | Prelevato | Mancante | Stato |
|---|---|---|---|---|
| … | qty_required | qty_picked | qty_missing | PENDING/PARTIAL/… |

Più eventuali **richieste materiale aperte** per quell'ordine (da `material_requests`).

---

## 8. Stima ETA (minuti al completamento)

**Idea:** ETA = (item rimanenti) × (tempo medio per item) + buffer per richieste materiale aperte.

- **Item rimanenti** per la lista/ordine: righe con `pick_status` non COMPLETE.
- **Tempo medio per item** (`avg_min_per_item`): da storico, due possibili sorgenti:
  - delta tra `picked_date` consecutivi nella stessa sessione WH, oppure
  - `(closed_date − upload_date)/items_total` su liste WH chiuse di recente (es. ultime 20).
- **Buffer richieste**: se ci sono `material_requests` aperte, aggiungere il tempo medio
  storico richiesta→conferma (`AVG(DATEDIFF(MIN, request_date, confirmed_date))`).
- **Fattori**: se sessione `SUSPENDED` o nessuna sessione attiva, l'ETA parte dal momento di
  ripresa stimato (o marcata "in attesa"); P0 non cambia la durata ma l'ordine in coda.
- `eta_ready_at = GETDATE() + eta_minutes`. Se dati storici insufficienti → ETA = NULL
  ("n/d") con fallback su una **media fissa configurabile** per item.

> L'ETA è una **stima statistica**, ricalcolata ad ogni sync (5 min). Robustezza > precisione.
> Affinamento del modello previsto come iterazione successiva (vedi §12, Fase 4).

---

## 9. Configurazione (`kit_server_config.json`)

Posizione proposta: cartella applicazione (accanto a `db_config.enc`), oppure
`%LOCALAPPDATA%\TraceabilityRS\`. **Creato con default se assente** (pattern già in uso).

```json
{
  "server_host_ip": "192.168.10.72",
  "server_port": 8090,
  "sync_interval_minutes": 5,
  "heartbeat_seconds": 60,
  "controller_takeover_minutes": 3,
  "health_path": "/health",
  "late_threshold_minutes": 120,
  "alert_targets": ["KIT_PREP"],
  "email_setting": "Sys_email_Kit_materiali"
}
```

---

## 10. Server INDIPENDENTE + autostart (architettura finale)

> **Decisione utente:** il web server deve restare attivo **anche se l'app desktop sul .72
> viene chiusa**. Quindi il server è un **processo autonomo**, non un figlio dell'app.

### 10.1 Web server autonomo (sul .72)
- `kit_web_server.py` gira come **processo a sé**, avviato da una **Scheduled Task** al logon
  (vedi §16). Fa **da sé il sync** ogni `sync_interval_minutes` (thread interno) → non dipende
  dall'app desktop per l'aggiornamento dei dati.
- Scrive il proprio **heartbeat** in `kit_dashboard_controller` (`server_state='RUNNING'`,
  `heartbeat_date`, `server_pid`) a ogni sync → stato visibile a chiunque dal DB.
- Trigger al **logon dell'utente** (non a system startup) così la mappatura `T:\Planning` è
  disponibile; **riavvio automatico** in caso di crash (RestartOnFailure, ogni 1 min).

### 10.2 App desktop = solo WATCHER (tutti i PC)
- `KitDashboardController` non avvia né chiude più il server. Fa solo da **watcher**: ping
  `/health`; se **DOWN** → alert (popup `KIT_PREP` + email) con **dedup atomico** (§11).
- Nessuna sovrapposizione/elezione necessaria: il sync lo fa **solo** il web server.

---

## 11. Health-check, relaunch e alert

- **Health endpoint**: `GET /health` → 200 + `{status, snapshot_date}`.
- **Watcher (tutte le istanze, anche standby)**: ping periodico `http://<ip>:<porta>/health`.
- **Logica**:
  1. Server **UP** → ok, nessuna azione.
  2. Server **DOWN** e io sono il **controller sul .72** → relaunch **locale** (supervisor).
  3. Server **DOWN** e io **non** sono sul .72:
     - tentativo di rilancio remoto **se abilitato** (vedi §13-D2: serve un meccanismo —
       agent locale sul .72 / Scheduled Task / PsExec / WinRM; di default **non assumiamo**
       rilancio remoto possibile),
     - se non rilanciabile da remoto → **alert** ai PC `KIT_PREP` (popup via `kit_popup_queue`)
       **e** email ai destinatari `Sys_email_Kit_materiali`.
- **Dedup alert** cross-PC: claim atomico su tabella di log (pattern `email-dedup-pattern`),
  così l'allarme parte **una sola volta** per finestra anche con più watcher.

---

## 12. Fasi di implementazione (proposta)

| Fase | Contenuto | Esito verificabile |
|---|---|---|
| 0 | `setup_kit_dashboard.py` (tabelle snapshot+controller), `server_config.py` | tabelle create; json default creato |
| 1 | `KitDashboardSync` + ETA base; popolamento snapshot | snapshot corretto in DB ogni 5 min |
| 2 | `kit_web_server.py` (Flask) + pagine **Magazzino** e **Produzione** (read-only) | pagine navigabili in intranet |
| 3 | Ricerca/filtri, rosso+blink, badge codici mancanti, drill-down `/ordine/<n>` | comportamento UI completo |
| 4 | Controller+heartbeat, supervisor (relaunch locale), watcher+alert email/popup | resilienza server, notifiche |
| 5 | Rifinitura ETA (storico), traduzioni UI, auto-refresh, hardening | release |

---

## 13. Decisioni — RISOLTE (confermate dall'utente)

- **D1 — "in ritardo" → soluzione B**, ma la **data pianificata NON viene da `Orders`**: si usa il
  **file Excel di pianificazione in `T:\Planning`** (tab `PlanningMachine`, col. K=ordine, col. O=`PlannedStart`,
  col. E=fase), già letto da `fai_autocheck.read_planning_excel()`. La data di riferimento è l'**ora
  pianificata della PRIMA fase `PTHM`** dell'ordine (il primo `PlannedStart` con fase == `PTHM` esatto —
  **escluso** `PTHM SELECTIVE`; PTHM = `IdPhase 4`). Verifica confermata: il file contiene fasi
  `AOI/PTHM/PTHM SELECTIVE/ICT/FCT/...` con ordine e `PlannedStart`.
  - Il deadline è "pendente" finché **la produzione PTHM non è avviata**, cioè finché **non è stata
    prodotta alcuna scheda** per la fase PTHM dell'ordine → si usa `fai_autocheck.check_production_started(conn, order, 4)`
    (conta board via `Scannings/OrderPhases/Phases`); `0` = non avviata.
  - `is_late = 1` se PTHM **non avviata** e (`NOW > planned_start_PTHM` **oppure** `eta_ready_at > planned_start_PTHM`).
  - Stati `BLOCKED_MISSING_MATERIAL`/`REOPENED` → sempre rosso. Ordine assente dal planning o senza
    riga PTHM → nessun flag di ritardo (solo stato). Quando PTHM risulta avviata, l'ordine esce dalla
    vista "in attesa" e nello storico `was_on_time = (ready_date <= planned_start_PTHM)`.
- **D2 — soluzione A:** **nessun rilancio remoto**. Se il server è giù e l'app host (.72) non gira,
  si emette **solo alert** (popup `KIT_PREP` + email `Sys_email_Kit_materiali`).
- **D3 — Flask.** **D4 — porta `8090`, nessuna autenticazione.**
- **D5 — snapshot ogni 5 min** + **pulsante "Aggiorna ora"** sulle pagine (forza un ricalcolo immediato).
- **D6 — `kit_server_config.json` nella stessa directory dell'eseguibile** (accanto a `db_config.enc`).
- **D7 — sì**, aggiungere `Flask` (+ `requests` per i ping) a `requirements.txt` e al build PyInstaller.
- **D8 — storico:** la pagina Produzione mostra di **default gli ultimi 3 giorni**, con ricerca anche
  su ordini più vecchi. Per ogni ordine storico si indica **se preparato in tempo** (vs `PlannedStart`)
  e **se era completo**. → richiede tabella storico persistente (vedi §5.4).

---

## 14. Rischi e note

- **Rilancio remoto**: il punto più delicato. Senza un agent/Scheduled Task sul .72, il
  "rilancio da remoto" non è realizzabile in modo affidabile → ci si affida all'**alert**.
  La scelta in D2 determina la complessità della Fase 4.
- **Blink/rosso** su monitor a parete: usare CSS animation lato browser, non polling pesante.
- **Carico DB**: lo snapshot disaccoppia il web dal DB; le query pesanti girano 1 volta/5 min
  sul solo controller.
- **PyInstaller**: il web server e i template vanno inclusi tra i data files del build.
- **Fuso/orari**: tutte le stime usano `GETDATE()` del SQL Server (coerenza con il resto app).

---

## 15. Stato implementazione (v1.0 — IMPLEMENTATO)

Tutte le fasi §12 sono state realizzate e verificate sul DB reale.

**File creati**
- `setup_kit_dashboard.py` — crea le 5 tabelle (`kit_dashboard_snapshot`, `_snapshot_missing`,
  `_history`, `_controller`, `_alert_log`). Idempotente. ✅ eseguito.
- `kit_server_config.json` — generato con i default nella dir dell'eseguibile.
- `kit_dashboard/server_config.py` — config (load/save atomico, default-se-assente).
- `kit_dashboard/planning.py` — `pthm_planned_starts()`: ora pianificata prima fase **PTHM**
  da `T:\Planning` (riusa `fai_autocheck`). ✅ legge 48 ordini PTHM dal file reale.
- `kit_dashboard/eta.py` — stima minuti/ETA da storico liste chiuse + buffer richieste.
- `kit_dashboard/sync_service.py` — `KitDashboardSync`: ricalcolo snapshot + missing + history.
  ⚠️ gli item sono per **lista** (`picking_list_items.order_number` è NULL) → progresso per
  lista attribuito agli ordini via `picking_list_orders`. ✅ snapshot popolato (4 ordini, 1 late).
- `kit_dashboard/web_data.py` — query read-only per le pagine.
- `kit_dashboard/web_templates.py` — template Jinja2 (RO) come dict (no file su disco).
- `kit_web_server.py` — Flask: `/magazzino`, `/produzione`, `/ordine/<n>`, `/refresh` (POST),
  `/health`. **Autonomo**: thread interno che fa il **sync ogni 5 min** + heartbeat in DB.
  ✅ testato standalone (self-sync popola lo snapshot, heartbeat RUNNING, health 200).
- `kit_dashboard/server_watcher.py` — `check_health` + alert (popup KIT_PREP + email) con
  **dedup atomico** su `kit_dashboard_alert_log`. ✅ dedup verificato (2° claim = False).
- `kit_dashboard/controller.py` — **watcher** (ping `/health` + alert se down). Non avvia né
  chiude il server. ✅ avviato da main.py su ogni PC.
- `install_kit_dashboard_autostart.py` — registra la Scheduled Task `KitDashboardServer`
  (logon trigger + restart-on-failure) che avvia il web server al boot/logon del .72.
  ✅ generazione XML verificata.
- Voce di menu *Kit → Dashboard Web (Produzione)* (`_open_kit_dashboard_web` in `main.py`) apre
  l'URL del server nel browser.

**Modifiche a file esistenti**
- `main.py`: (1) flag `--kit-web-server` in testa a `__main__` (avvia solo il web server, per il
  build frozen) + esclusione del child dalla kill-orfani; (2) avvio `KitDashboardController` nel
  blocco monitor; (3) stop del controller in `_on_closing`.
- `requirements.txt`: aggiunti Flask, Werkzeug, Jinja2, MarkupSafe, blinker, click, itsdangerous,
  requests (+ certifi, idna, urllib3).

## 16. Deploy e build

**Installazione sul PC `192.168.10.72` (SYSTEM, senza login — manuale, una volta):**
1. `python setup_kit_dashboard.py` — crea le tabelle (già fatto sul DB condiviso).
2. Verificare in `kit_server_config.json` (dir dell'eseguibile) che `planning_path` punti alla
   share **UNC** (default `\\192.168.10.110\InternalApplications\Planning`) — SYSTEM non ha `T:`.
3. Da prompt **Amministratore**: `python install_kit_dashboard_autostart.py` → registra la
   Scheduled Task `KitDashboardServer` come **SYSTEM**, trigger **all'avvio del PC** (ritardo
   1 min), **restart-on-failure**, e la avvia subito.
4. Aprire la **porta** nel firewall:
   `netsh advfirewall firewall add rule name="KitDashboard 8090" dir=in action=allow protocol=TCP localport=8090`
5. Monitor a parete: `http://192.168.10.72:8090/magazzino` e `/produzione` a schermo intero.

> ⚠️ **Permessi (SYSTEM):** girando come SYSTEM, l'accesso alla share di pianificazione e al DB
> usa l'**account macchina** (`<PC72>$`). IT deve garantire a quell'account la **lettura** su
> `\\192.168.10.110\InternalApplications` e l'accesso al DB. Se non è possibile, usare la variante
> **al logon** (`install_kit_dashboard_autostart.py --logon`, PC con auto-login) che usa il
> profilo utente con `T:` mappato.

Il server resta attivo **indipendentemente** dall'app desktop (sopravvive a chiusura app, riparte
al boot e dopo crash) e fa da sé il sync ogni 5 min. Sugli altri PC nessuna azione: l'app fa da
**watcher** e avvisa `KIT_PREP` (popup + email) se il server non risponde. La voce di menu
*Kit → Dashboard Web (Produzione)* apre la pagina nel browser.

**Disinstallare l'autostart:** `python install_kit_dashboard_autostart.py --remove`.

**Build PyInstaller:** `main.spec` è stato aggiornato con gli hidden import necessari
(Flask/Werkzeug/Jinja2/Click/MarkupSafe/blinker/itsdangerous/requests + `kit_web_server` +
`kit_dashboard.*` + `fai_autocheck`). La cartella `docs/` (già inclusa) porta con sé il manuale
e gli screenshot; i template web sono stringhe Python (nessun data-file). Ricompilare:
`pyinstaller --noconfirm --clean main.spec`. `kit_server_config.json` viene creato a runtime
accanto all'eseguibile (al primo avvio del web server).

---

*Documento allineato all'implementazione v1.0.*
