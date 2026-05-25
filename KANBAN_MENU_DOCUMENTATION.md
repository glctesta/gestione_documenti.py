# Documentazione Modulo KanBan — Menu e Funzioni
*Documento generato il 21/05/2026 — Basato su `main.py`*

---

## Struttura Gerarchica del Menu KanBan

Il menu KanBan è un sottomenu del menu principale **Produzione**, gestito dalla funzione `_update_kanban_submenus()` (riga 16151 di `main.py`). La gerarchia è la seguente:

```
Produzione
└── KanBan
    ├── Locazioni
    │   ├── Crea                        → open_kanban_locations_create()
    │   ├── Modifica...                 → open_kanban_locations_modify()
    │   ├── Etichette                   → open_kanban_locations_labels()
    │   ├── ─────────────
    │   └── Impostazioni stampante...   → open_printer_setup()
    ├── Materiali
    │   ├── Materiali - Gestione        → open_kanban_materials_management()
    │   ├── Gestione regole             → open_kanban_rules_management()
    │   └── Report                      → open_kanban_materials_report()
    └── KanBan
        ├── Movimenta                   → open_kanban_move()
        └── Ricarica (TEST)             → open_kanban_load()
```

> **Nota:** Le voci **Verifica** (`_schedule_kanban_refill_check`) e **Gestione** (`open_kanban_manage`) sono **commentate** nel codice e non appaiono nel menu.

---

## Funzione di Aggiornamento Menu

### `_update_kanban_submenus()` — riga 16151
Svuota e ricostruisce tutti e tre i sottomenu KanBan ad ogni refresh del menu principale.  
Opera su tre istanze di `tk.Menu` già create in `_init_production_submenus()`:
- `self.kanban_root_submenu`
- `self.kanban_locations_submenu`
- `self.kanban_materials_submenu`
- `self.kanban_core_submenu`

---

## Sezione 1 — Locazioni KanBan

### 1.1 `open_kanban_locations_create()` → `KanbanLocationCreateForm`
**File:** `main.py` — riga 12321 (launcher), riga 8190 (form)  
**Accesso:** Diretto, senza login aggiuntivo

**Scopo:** Crea una nuova locazione KanBan associando un codice alfanumerico (max 8 caratteri, sempre maiuscolo) ad un'area produttiva.

**Form:** `KanbanLocationCreateForm` — finestra modale 500×260, non ridimensionabile

**Campi:**
| Campo | Tipo | Vincoli |
|---|---|---|
| Area | Combobox (readonly) | Obbligatorio — carica da `dbo.ParentPhases` (CodCDC in 10, 30, 90) |
| Codice Locazione | Entry | Max 8 caratteri, auto-uppercase, obbligatorio |

**Funzionalità:**
- Mostra il contatore totale locazioni in basso a sinistra (aggiornato dopo ogni salvataggio)
- Il pulsante Salva è abilitato solo se entrambi i campi sono validi
- Gestisce i duplicati: se la locazione esiste già nell'area selezionata, mostra un avviso

**Tabelle DB coinvolte:**
- `dbo.ParentPhases` — lettura aree (IDParentPhase, ParentPhaseName)
- `knb.KanBanLocations` — inserimento nuova locazione, conteggio totale

---

### 1.2 `open_kanban_locations_modify()` → `KanbanLocationModifyForm`
**File:** `main.py` — riga 12324 (launcher), riga 8621 (form)  
**Accesso:** Diretto, senza login aggiuntivo

**Scopo:** Permette di **spostare** componenti KanBan tra locazioni diverse — sia singolarmente che in blocco (tutta una locazione).

**Form:** `KanbanLocationModifyForm` — finestra modale 720×420, con 2 tab

**Tab 1 — "Sposta componente":**
- Campo codice componente + pulsante Cerca
- Treeview risultati: ID, Locazione attuale, Quantità, Descrizione
- Combobox destinazione + pulsante "Sposta"

**Tab 2 — "Sposta locazione":**
- Combobox locazione di origine
- Combobox locazione di destinazione
- Pulsante "Sposta tutto"

**Regole di business:**
- Il sistema impedisce di spostare verso la stessa locazione (sorgente = destinazione)
- Lo spostamento singolo richiede la selezione di una riga nel Treeview
- Lo spostamento in blocco gestisce il caso "locazione già vuota" (`"nothing_to_move"`)

**Tabelle DB coinvolte:**
- `knb.KanBanLocations` — lettura locazioni per i combo
- `knb.KanBanRecords` — ricerca per codice componente, spostamento singolo, spostamento in blocco

---

### 1.3 `open_kanban_locations_labels()` → `KanbanLocationLabelsForm`
**File:** `main.py` — riga 12330 (launcher), riga 8360 (form)  
**Accesso:** Diretto, senza login aggiuntivo

**Scopo:** Stampa etichette **ZPL** con QR code per le locazioni KanBan, inviandole direttamente su stampante di rete via TCP/IP.

**Form:** `KanbanLocationLabelsForm` — finestra modale 520×260

**Campi:**
| Campo | Tipo | Note |
|---|---|---|
| Stampante | Label (verde) | Mostra nome, IP:porta, DPI della stampante configurata |
| Locazione | Combobox (readonly) | Tutte le locazioni attive |
| Copie | Spinbox | Valore 1–99 |

**Funzionalità:**
- Se nessuna stampante è configurata all'apertura, avvia obbligatoriamente `PrinterSetupDialog`; se l'utente annulla, la form si chiude
- Il pulsante "Imposta..." permette di riconfigurare la stampante in qualsiasi momento
- Il QR code nell'etichetta codifica il codice della locazione selezionata
- La dimensione dell'etichetta è fissa 5×5 cm; i calcoli ZPL si adattano ai DPI configurati

**Configurazione stampante:** Salvata localmente in `%LOCALAPPDATA%\TraceabilityRS\printer_config.json`

**Funzioni di supporto (globali, definite vicino alla classe):**
- `build_zpl_label(location_code, copies, cfg)` — genera il codice ZPL II
- `send_raw_to_printer(ip, port, payload)` — invia via TCP socket
- `load_printer_config()` / `save_printer_config(cfg)` — I/O del file JSON (scrittura atomica con backup)

**Tabelle DB coinvolte:**
- `knb.KanBanLocations` — lettura di tutte le locazioni (LocationCode)

---

### 1.4 `open_printer_setup()` → `PrinterSetupDialog`
**File:** `main.py` — riga 12307 (launcher), riga 10018 (form)  
**Accesso:** Diretto, senza login aggiuntivo

**Scopo:** Configura la stampante di rete ZPL per la stampa delle etichette KanBan.

**Form:** `PrinterSetupDialog` — finestra modale, non ridimensionabile

**Campi:**
| Campo | Valore default | Vincoli |
|---|---|---|
| Nome stampante | — | Obbligatorio |
| Indirizzo IP | — | Obbligatorio, formato IPv4 valido |
| Porta | 9100 | Obbligatorio, intero |
| DPI | 203 | Obbligatorio, intero |
| Dimensione testo (pt) | 12 | Obbligatorio, intero |

**Funzionalità:**
- **Salva** — valida i campi, salva la config JSON (scrittura atomica + backup `.bak`)
- **Annulla** — chiude senza salvare, restituisce `result = None`
- **Apri cartella** — apre in Esplora Risorse la cartella `%LOCALAPPDATA%\TraceabilityRS\`
- **Test stampa** — invia un'etichetta di test ZPL all'IP/porta inseriti (senza salvare le modifiche)

**Nessuna interazione con il DB** — tutta la persistenza è su file JSON locale.

---

## Sezione 2 — Materiali KanBan

### 2.1 `open_kanban_materials_management()` → `KanbanMaterialsManagementForm`
**File:** `main.py` — riga 12334 (launcher), riga 8801 (form)  
**Accesso:** Richiede autorizzazione (`_execute_authorized_action`, chiave `'kanban_move'`)

**Scopo:** Associa/disassocia le **regole di riordino** ai componenti KanBan. Permette di filtrare i componenti per tipologia e di vedere la regola attiva corrente.

**Form:** `KanbanMaterialsManagementForm` — finestra modale 760×420

**Layout:**
- Combobox tipo componente (filtro opzionale: "Tutti" / tipo specifico)
- Combobox componente (formato: `"CODICE - Descrizione"`)
- Labelframe **"Regola attiva"** — mostra la regola correntemente associata al componente
- Labelframe **"Associa regola"** — combobox regola disponibile + pulsanti Assegna / Rimuovi

**Regole di business:**
- Un componente può avere **una sola regola attiva** alla volta
- La rimozione della regola non cancella il record, ma imposta una data di chiusura (soft-delete)
- Quando si seleziona un componente, la sua regola attiva viene pre-selezionata nel combo regole
- `assign_rule_to_component(comp_id, None)` segnala la rimozione; il DB handler gestisce la logica di chiusura

**Tabelle DB coinvolte:**
- `dbo.ComponentTypes` — lettura tipi componente
- `dbo.Components` — lettura elenco componenti
- `knb.KanBanRules` — lettura regole attive
- `knb.KanBanRuleComponents` — lettura/scrittura associazione regola-componente

---

### 2.2 `open_kanban_rules_management()` → `KanbanRulesManagementForm`
**File:** `main.py` — riga 12304 (launcher), riga 489 (form)  
**Accesso:** Diretto, senza login aggiuntivo

**Scopo:** Gestisce le **regole di soglia di riordino** KanBan: crea, modifica e disattiva le regole che definiscono quando scatta l'alert di ricarica.

**Form:** `KanbanRulesManagementForm` — finestra modale 640×460, non ridimensionabile

**Tipi di regola:**
| Tipo | Descrizione | Validazione |
|---|---|---|
| Percentuale | Soglia = % della prima quantità caricata | Valore intero 1–100 |
| Quantità assoluta | Soglia = numero fisso di pezzi | Valore intero > 0 |

**Layout:**
- Treeview: ID, Tipo, Valore, Stato (Attiva/Chiusa), Data chiusura
- Radio button Tipo (Percentuale / Quantità) + Entry valore
- Pulsanti: Nuovo, Salva, Elimina, Pulisci

**Regole di business:**
- Una regola può essere di tipo **percentuale** (calcolo dinamico sulla prima quantità caricata) oppure **quantità assoluta** — mai entrambe
- L'eliminazione è **soft-delete** (imposta `DateOut`): una regola già chiusa non può essere eliminata nuovamente
- Le regole chiuse restano visibili in lista con stato "Chiusa"

**Tabelle DB coinvolte:**
- `knb.KanBanRules` — CRUD completo (KanBanRuleID, MinimumProcent, MinimumQty, DateOut)

---

### 2.3 `open_kanban_materials_report()` — Report Excel
**File:** `main.py` — riga 12197  
**Accesso:** Diretto, senza login aggiuntivo  
**Nessuna form modale** — esecuzione inline, genera direttamente un file Excel

**Scopo:** Genera un report Excel dei componenti KanBan con le rispettive locazioni, salvato in `C:\Temp\`.

**Contenuto del report (colonne):**
| Colonna | Sorgente |
|---|---|
| Codice componente | `ComponentCode` |
| Descrizione | `ComponentDescription` |
| Locazione | `LocationCode` |
| Area | `KanBanLocation` |

**Formattazione Excel:**
- Intestazione: sfondo azzurro tenue (#DDEBF7), grassetto, centrato
- Righe alternate (zebra stripes): sfondo #F7FBFF per le righe pari
- Bordi sottili su tutte le celle
- Auto-filtro e blocca riga 1 (freeze panes)
- Larghezza colonne auto-calcolata (max 60 caratteri)

**Output:** `C:\Temp\KanBan_Materiali_Report_YYYYMMDD_HHMMSS.xlsx`  
Dopo il salvataggio viene chiesto se aprire il file (sì/no).

**Tabelle DB coinvolte:**
- Query tramite `db.fetch_components_locations_report()` — join tra componenti e locazioni KanBan

---

## Sezione 3 — Operazioni KanBan (Core)

### 3.1 `open_kanban_move()` → `KanbanMoveForm(mode='unload')`
**File:** `main.py` — riga 12353 (launcher), riga 9011 (form)  
**Accesso:** Richiede autorizzazione (`_execute_authorized_action`, chiave `'kanban_move'`)

**Scopo:** **Prelievo materiali** KanBan — registra l'uscita di componenti da una locazione (delta negativo nel DB).

---

### 3.2 `open_kanban_load()` → `KanbanMoveForm(mode='load')`
**File:** `main.py` — riga 12342 (launcher), riga 9011 (form)  
**Accesso:** Richiede autorizzazione (`_execute_authorized_action`, chiave `'kanban_load'`)  
**Etichetta menu:** "Ricarica (TEST)" — indica che la funzione è ancora in fase di test

**Scopo:** **Caricamento materiali** KanBan — registra l'ingresso di componenti in una locazione (delta positivo nel DB).

---

### `KanbanMoveForm` — Dettaglio Completo
**File:** `main.py` — riga 9011  
**Modalità:** `'load'` (carico), `'unload'` (prelievo), `'both'` (default — mostra radio per scelta)

**Form:** Finestra modale 720×420

**Layout:**
- Radio buttons opzione (Load / Unload) — nascosti se mode è `'load'` o `'unload'`
- Labelframe "Selezione":
  - Combobox **Area** (filtra i successivi)
  - Combobox **Componente** (formato: `"CODICE - Descrizione"`)
  - Entry **Quantità**
  - Combobox **Locazione** (formato: `"COD [stock]"`)
- Label saldo: **"Saldo qui"** e **"Altrove"** (aggiornati in tempo reale)
- Pulsanti:
  - **Esegui** — esegue il movimento
  - **Genera Template Excel** (solo in modalità load) — crea un file .xlsx precompilato per importazione massiva
  - **Importa da Excel** — importa movimenti da CSV o XLSX
  - **Chiudi**
- Area log (Text widget, altezza 10 righe) — mostra l'esito di ogni operazione con timestamp

**Comportamento per modalità:**

| Aspetto | mode='unload' (Movimenta) | mode='load' (Ricarica) |
|---|---|---|
| Autorizzazione | Al lancio della form (kanban_move) | Al lancio della form (kanban_load) |
| Utente registrato | Utente di sessione applicazione | Utente autorizzato al carico |
| Locazioni mostrate | Solo quelle con stock del componente | Tutte, con `(***)` per quelle in uso |
| Controllo disponibilità | Sì — impedisce stock negativo | No |
| Template Excel | Non disponibile | Disponibile |

**Comportamento intelligente locazioni:**
- Al cambio componente, le locazioni vengono filtrate/ordinate per stock decrescente
- In unload mode, viene auto-selezionata la locazione con più stock
- Il campo Quantità (invio/focus-out) ri-ordina le locazioni per stock e auto-seleziona la migliore

**Importazione da Excel/CSV:**
- Intestazioni accettate (case-insensitive): `location`/`locazione`, `component`/`componente`/`codice`, `quantity`/`quantita`/`qty`/`qta`
- Normalizzazione quantità: supporta formato italiano (`1.500,00`), inglese (`1,500.00`) e intero puro
- Per ogni riga, il sistema risolve component e locazione via lookup su cache o DB
- Riporta un riepilogo finale: righe elaborate, successi, errori

**Alias disponibili:** `open_kanban_refill()`, `open_kanban_reload()`, `kanban_load()` — tutti puntano a `open_kanban_load()`

**Tabelle DB coinvolte:**
- `knb.KanBanLocations` — aree e locazioni
- `dbo.Components` — elenco componenti
- `knb.KanBanRecords` — stock corrente per componente/locazione
- `knb.KanBanMovements` — inserimento movimento (load/unload)

---

## Sezione 4 — Funzioni Commentate (Non Attive nel Menu)

### `open_kanban_manage()` — riga 12378
Attualmente mostra solo `_not_implemented('KanBan', 'Gestione')`.  
**Stato:** Voce commentata nel menu — placeholder per future funzionalità di gestione avanzata.

---

### `_schedule_kanban_refill_check()` — riga 11849
**Stato:** Voce commentata nel menu ma la funzione è **pienamente implementata** e attiva come scheduler automatico in background.

**Scopo:** Controllo automatico periodico dello stock KanBan e invio email di richiesta ricarica.

**Schedulazione:**
- Intervallo fisso: **60 minuti**
- Eseguito solo in giorni lavorativi (`should_send_notification(country_code='IT')`)
- Esecuzione in thread separato (`KanbanRefillCheck`) per non bloccare la UI

**Regole di esecuzione:**
1. **Una sola email al giorno** — verifica su DB prima di procedere (`has_kanban_refill_email_sent_today()`)
2. **Soppressa se `AskForRefill=0`** per tutte le locazioni
3. **Deduplicazione per record** — `has_refill_request_today(kanban_record_id)` evita richieste duplicate per lo stesso materiale nella stessa giornata

**Algoritmo di calcolo componenti da ricaricare:**
1. Lettura stock corrente per componente (`fetch_kanban_current_stock_by_component`)
2. Lettura regole attive (`fetch_active_rules_by_component`)
3. Per regole percentuali: calcolo soglia = `(prima_quantità × percentuale) / 100`
4. Per regole assolute: soglia = valore fisso
5. Se `stock_corrente ≤ soglia` → aggiunge alla lista di ricarica con `qty = max_carico_singolo`

**Output:**
- File Excel in memoria (openpyxl) con lista componenti da ricaricare
- Email a destinatari da `utils.get_email_recipients(attribute='Sys_email_KanBanRefill')`
- Registrazione dell'invio su DB (`log_kanban_refill_email_sent`)
- Inserimento richieste su DB **prima** dell'invio email (per protezione race-condition multi-thread)

**Tabelle DB coinvolte:**
- `knb.KanBanLocations` — flag `AskForRefill`
- `knb.KanBanRecords` — stock corrente aggregato per componente
- `knb.KanBanRules` / `knb.KanBanRuleComponents` — regole attive
- `knb.KanBanRefillRequests` — log richieste giornaliere
- `knb.KanBanRefillEmailLog` — log invio email (indice UNIQUE su data)

---

## Riepilogo Tabelle DB Utilizzate dal Modulo KanBan

| Schema | Tabella | Usata da |
|---|---|---|
| `dbo` | `ParentPhases` | LocationCreateForm (aree) |
| `dbo` | `Components` | MoveForm, MaterialsManagementForm |
| `dbo` | `ComponentTypes` | MaterialsManagementForm |
| `knb` | `KanBanLocations` | Create, Labels, Modify, Move, Refill |
| `knb` | `KanBanRecords` | Modify, Move |
| `knb` | `KanBanMovements` | MoveForm (insert) |
| `knb` | `KanBanRules` | RulesManagementForm, MaterialsManagementForm |
| `knb` | `KanBanRuleComponents` | MaterialsManagementForm |
| `knb` | `KanBanRefillRequests` | Refill scheduler |
| `knb` | `KanBanRefillEmailLog` | Refill scheduler |

---

## Riepilogo Autorizzazioni

| Funzione | Tipo accesso | Chiave autorizzazione |
|---|---|---|
| Crea locazione | Libero | — |
| Modifica/sposta locazione | Libero | — |
| Stampa etichette | Libero | — |
| Imposta stampante | Libero | — |
| Gestione regole | Libero | — |
| Report materiali | Libero | — |
| Gestione materiali/regole | Autorizzazione | `kanban_move` |
| Movimenta (prelievo) | Autorizzazione | `kanban_move` |
| Ricarica (carico) | Autorizzazione | `kanban_load` |

---

*Fine documento — `KANBAN_MENU_DOCUMENTATION.md`*
