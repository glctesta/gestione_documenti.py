# PlanRespect — Kit Preparation & Verification Module
## Specifiche Funzionali per Implementazione

**Progetto:** PlanRespect — Estensione Modulo Preparazione Kit Produzione  
**Percorso progetto:** `C:\Users\gtesta\PythonProjects\Python\PlanRespect`  
**Versione documento:** 1.0  
**Data:** 2026-06-11  
**Autore:** G. Testa  
**Destinatario:** Claude Code (implementazione) / Team sviluppo  

---

## 1. Contesto e Obiettivo

Il programma PlanRespect gestisce attualmente la preparazione del materiale relativo agli ordini di produzione pianificati. L'obiettivo di questo documento è definire analiticamente le estensioni da implementare per garantire la **completezza e tracciabilità dei kit di produzione**, dalla fase di prelievo in magazzino fino alla consegna in linea di produzione.

### 1.1 Problema da Risolvere

I ritardi di produzione dovuti a materiali mancanti nei kit non derivano sempre da una effettiva mancanza fisica del materiale. Le cause principali identificate sono:

| # | Causa | Descrizione |
|---|-------|-------------|
| 1 | **Mancanza comunicazione turno** | Il responsabile di linea non ha ricevuto istruzioni chiare dal capolinea del turno precedente |
| 2 | **Posizionamento sconosciuto** | Il materiale è presente ma il responsabile non ricorda dove si trova |
| 3 | **Scrap eccedente** | Materiali scartati in fase di lavorazione con quantità superiore al fattore di scrap calcolato in BOM |
| 4 | **Errore di prelievo WH** | Quantità prelevata non corretta dal magazzino |
| 5 | **Materiale non trasferito** | Il kit fisico non è stato completamente trasferito da magazzino a produzione |

### 1.2 Strategia della Soluzione

Separare logicamente e cronologicamente le attività in **tre macro-fasi verificabili**:

1. **FASE WH** — Prelievo fisico e verifica quantità in magazzino
2. **FASE PREFORMATURA** — Presa in carico e verifica in ingresso
3. **FASE PRODUZIONE** — Verifica in linea e gestione materiale aggiuntivo

---

## 2. Architettura Generale del Sistema

### 2.1 Fonti Dati Principali

```
┌─────────────────────────────────────────────────────────────────┐
│                    FONTI DATI DEL SISTEMA                        │
├─────────────────────┬───────────────────────────────────────────┤
│ Piano Produzione    │ File di programmazione esistente           │
│                     │ (già utilizzato da PlanRespect)            │
├─────────────────────┼───────────────────────────────────────────┤
│ Lista Prelievo XLSX │ File generato da sistema Essegi            │
│                     │ Codici materiale + Unique Number + Qty     │
├─────────────────────┼───────────────────────────────────────────┤
│ DB traceability_rb  │ Query per qty effettive per ordine         │
│                     │ (interpolazione con lista prelievo)        │
├─────────────────────┼───────────────────────────────────────────┤
│ Sistema Popup       │ Già attivo per materiali indiretti         │
│                     │ (estendere per notifiche dirette)          │
└─────────────────────┴───────────────────────────────────────────┘
```

### 2.2 Interfaccia Browser

Il modulo deve essere **accessibile via browser**, lanciabile direttamente dall'applicazione PlanRespect esistente. Ogni fase espone una pagina/scheda dedicata con autenticazione separata per ruolo.

### 2.3 Ruoli e Login

| Ruolo | Codice | Fasi di accesso |
|-------|--------|-----------------|
| Operatore Magazzino | `WH_OP` | Fase WH — Prelievo |
| Responsabile Magazzino | `WH_MGR` | Supervisione WH + ricezione richieste |
| Operatore Preformatura | `PF_OP` | Fase Preformatura — Scansione ingresso |
| Responsabile Preformatura | `PF_MGR` | Supervisione Preformatura |
| Responsabile Linea Produzione | `PROD_OP` | Fase Produzione — Verifica ricevuto |
| Supervisore Produzione | `PROD_MGR` | Supervisione Produzione + escalation |
| Pianificatore | `PLAN` | Gestione priorità ordini |

---

## 3. Gestione Priorità Ordini

### 3.1 Schema di Priorità

Al piano di produzione esistente viene aggiunta una colonna **`PRIORITY`** con i seguenti valori:

| Valore | Significato | Logica di esecuzione |
|--------|-------------|----------------------|
| `0` | Nessuna priorità speciale | Ordinamento per data piano |
| `1` | Massima priorità | Da evadere per primo, sopra qualsiasi altro |
| `2` | Alta priorità | Dopo tutti i P1 |
| `3` | Priorità media | Dopo tutti i P2 |

### 3.2 Regole di Ordinamento Lista

La lista degli ordini visualizzata agli operatori WH è ordinata secondo questa logica:

```sql
ORDER BY
    CASE PRIORITY
        WHEN 0 THEN 4      -- posizionato come ultimo per data
        ELSE PRIORITY       -- 1, 2, 3 in ordine
    END ASC,
    CASE PRIORITY
        WHEN 0 THEN PLANNED_DATE  -- ordina per data solo i P0
        ELSE NULL
    END ASC,
    PLANNED_DATE ASC
```

### 3.3 UI Assegnazione Priorità

- Accessibile dal modulo pianificazione (ruolo `PLAN`)
- Dropdown per ogni ordine: `[0] Normale | [1] Urgente | [2] Alta | [3] Media`
- Modifica priorità in tempo reale — la lista WH si aggiorna immediatamente
- Badge colorato sulla riga: rosso=P1, arancione=P2, giallo=P3, grigio=P0

---

## 4. Processo Flow Completo

```
                         PIANIFICAZIONE
                              │
                    [Assegna Priorità P0-P3]
                              │
                    [Genera Lista Ordini WH]
                              │
                   ┌──────────▼──────────┐
                   │  FASE 1: MAGAZZINO  │
                   │   (Login WH_OP)     │
                   └──────────┬──────────┘
                              │
                  [Carica Lista Prelievo XLSX Essegi]
                              │
                  [Interpola con DB traceability_rb]
                              │
                  [Scansione: Unique# + Materiale + Qty]
                              │
              ┌───────────────▼───────────────┐
              │     VERIFICA QUANTITÀ WH       │
              │  🟢 Verde = prelevato OK       │
              │  🟠 Arancione = parziale       │
              │  🔴 Rosso = non prelevato      │
              └───────────────┬───────────────┘
                              │
              ┌───────────────▼───────────────┐
              │   TUTTE LE QUANTITÀ OK?        │
              └──────┬────────────────┬───────┘
                  SÌ │                │ NO
                     │      ┌─────────▼──────────┐
                     │      │  DEROGA WH_MGR?     │
                     │      └──────┬──────────────┘
                     │          SÌ │          NO
                     │             │     [Rimane aperto,
                     │             │      attesa completamento]
                     │    [Annota mancanze]
                     │    [Chiude con flag PARZIALE]
                     │             │
                   ┌─▼─────────────▼──────────────┐
                   │   FASE 2: PREFORMATURA        │
                   │   (Login PF_OP)               │
                   └──────────────┬────────────────┘
                                  │
                  [Scansione: Unique# + Qty Ricevuta]
                                  │
              ┌───────────────────▼────────────────┐
              │     VERIFICA INGRESSO PREFORMATURA  │
              └──────────┬─────────────────┬───────┘
                      OK │                 │ NON OK
                         │      ┌──────────▼──────────┐
                         │      │ ALERT → WH_OP + MGR  │
                         │      │ Email + Popup         │
                         │      │ Riapre lista WH       │
                         │      └─────────────────────┘
                         │
              ┌──────────▼───────────────────────────┐
              │     DURANTE PREFORMATURA              │
              │   Scarto > atteso BOM?                │
              └──────────┬───────────────────────────┘
                         │
          [Richiesta Materiale Aggiuntivo → WH_MGR]
          [Email + Popup WH_MGR]
          [WH conferma prelievo]
          [Popup produzione: materiale disponibile]
                         │
                   ┌─────▼──────────────────────────┐
                   │   FASE 3: PRODUZIONE            │
                   │   (Login PROD_OP)               │
                   └─────────────┬──────────────────┘
                                 │
                  [Ricezione Kit in Linea]
                  [Scansione: Unique# + Qty]
                                 │
              ┌──────────────────▼─────────────────┐
              │     VERIFICA RICEVUTO PRODUZIONE    │
              └──────────┬──────────────────┬──────┘
                      OK │                  │ NON OK
                         │     ┌────────────▼──────────┐
                         │     │ ALERT → PF_OP + MGR    │
                         │     │ Email + Popup           │
                         │     │ Ordine bloccato         │
                         │     └───────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │     DURANTE PRODUZIONE                 │
              │   Materiale deteriorato/perso?         │
              └──────────┬────────────────────────────┘
                         │
          [Richiesta aggiuntiva → WH_MGR]
          [WH preleva + conferma disponibilità]
          [Popup PROD_OP: materiale pronto]
                         │
          [Se materiale "mancante" ritrovato]
          [PROD_OP aggiorna stato nel sistema]
                         │
                   ┌─────▼─────────┐
                   │  ORDINE OK    │
                   │  Kit completo │
                   └───────────────┘
```

---

## 5. Specifiche Dettagliate per Fase

### 5.1 FASE 1 — Prelievo Magazzino

#### 5.1.1 Caricamento Lista Prelievo Essegi

- Formato input: file `.xlsx` generato dal sistema Essegi
- Il file può contenere **uno o più ordini di produzione** (es. `PR000123` oppure `PR000123/PR000124`)
- Se ordini multipli, i materiali comuni hanno **quantità cumulate**
- La lista deve essere caricata tramite upload nel sistema (interfaccia browser)

#### 5.1.2 Interpolazione con DB traceability_rb

Dopo il caricamento della lista Essegi, il sistema esegue automaticamente una query sul database `traceability_rb` per determinare le quantità effettive per ogni singolo ordine di produzione:

```sql
-- Query di riferimento (da adattare allo schema effettivo)
SELECT
    lp.material_code,
    lp.unique_number,
    lp.total_qty_essegi,
    tb.order_id,
    tb.qty_per_order,
    tb.lot_number
FROM lista_prelievo lp
JOIN traceability_rb.dbo.materials tb
    ON lp.material_code = tb.material_code
WHERE lp.picking_list_id = @picking_list_id
ORDER BY tb.order_id, lp.material_code;
```

> **Nota implementativa:** La query deve gestire il caso di ordini multipli nella stessa lista, disaggregando le quantità cumulate per singolo ordine di produzione.

#### 5.1.3 Interfaccia di Scansione WH

**Elementi UI richiesti:**

```
┌─────────────────────────────────────────────────────┐
│  PRELIEVO KIT  │  Ordine: PR000123 / PR000124        │
│  Operatore: [nome]  │  Data: 2026-06-11  10:32       │
├─────────────────────────────────────────────────────┤
│  Scansiona Unique Number Etichetta:  [___________]   │
│  Quantità prelevata:                 [___________]   │
│                                      [CONFERMA]      │
├──────┬──────────────────┬──────────┬────────────────┤
│ Stato│ Codice Materiale │ UN       │ Qty Req / Prel │
├──────┼──────────────────┼──────────┼────────────────┤
│  🟢  │ C4703-100nF-0402 │ UN001234 │  500 / 500     │
│  🟠  │ R1002-10K-0603   │ UN001235 │  200 / 120     │
│  🔴  │ IC-STM32F4-LQFP  │          │  10  / 0       │
└──────┴──────────────────┴──────────┴────────────────┘
│  [CHIUDI LISTA]  (disponibile solo se tutto 🟢)     │
│  [CHIUDI CON DEROGA] (richiede login WH_MGR)        │
└─────────────────────────────────────────────────────┘
```

**Logica colori:**
- **Verde** `🟢`: quantità prelevata = quantità richiesta
- **Arancione** `🟠`: 0 < quantità prelevata < quantità richiesta
- **Rosso** `🔴`: quantità prelevata = 0

#### 5.1.4 Chiusura con Deroga

Se non tutte le righe sono verdi, il pulsante "Chiudi Lista" è disabilitato. È disponibile il pulsante **"Chiudi con Deroga"** che:
1. Richiede autenticazione del `WH_MGR`
2. Registra nel DB: `picking_status = 'PARTIAL'`, `derogation_by = WH_MGR_ID`, `missing_items = [lista codici mancanti]`
3. Le righe incomplete rimangono in stato `PENDING_COMPLETION` e sono visibili nella dashboard WH fino a completamento

---

### 5.2 FASE 2 — Presa in Carico Preformatura

#### 5.2.1 Scansione Ingresso

L'operatore Preformatura, sotto login `PF_OP`, scansiona ogni materiale ricevuto:
- **Unique Number** dell'etichetta
- **Quantità fisica ricevuta**

Il sistema verifica che i valori corrispondano a quanto chiuso nella Fase WH.

#### 5.2.2 Esito Verifica

**Caso A — Tutto OK:**
- Il kit passa in stato `IN_PREFORMING`
- Si sblocca l'accesso alla Fase 3

**Caso B — Discrepanza rilevata:**
- Il sistema invia automaticamente:
  - **Email** a `WH_OP` che ha effettuato il prelievo e al suo diretto superiore `WH_MGR`
  - **Popup** sul laptop di `WH_OP` e `WH_MGR`
- Il messaggio indica: `"Ordine PR000123: verifica fallita in ingresso preformatura. Codici non conformi: [lista]"`
- La lista di prelievo WH viene riaperta in stato `REOPENED` per permettere verifica dei codici non conformi

#### 5.2.3 Richiesta Materiale Aggiuntivo durante Preformatura

Se durante la preformatura dei materiali vengono rilevati componenti **persi o inutilizzabili** (scrap eccedente BOM):

1. L'operatore `PF_OP` inserisce nel sistema la richiesta di materiale aggiuntivo
2. Il sistema invia **Email + Popup** al `WH_MGR`
3. Il magazzino preleva il materiale e conferma nel sistema che è `AVAILABLE_FOR_PICKUP`
4. Il sistema invia **Popup** alla postazione `PF_OP`: `"Materiale [codice] disponibile per prelievo in magazzino"`

---

### 5.3 FASE 3 — Ricezione e Verifica in Produzione

#### 5.3.1 Presa in Carico Linea

Il responsabile di linea (`PROD_OP`), sotto login separato, scansiona il kit ricevuto:
- **Unique Number** di ogni materiale
- **Quantità fisica**

#### 5.3.2 Esito Verifica

**Caso A — Tutto confermato:**
- Kit in stato `RECEIVED_IN_PRODUCTION`
- Produzione può procedere

**Caso B — Mancanza rilevata:**
- Il sistema invia **Email + Popup** a `PF_OP` + `PF_MGR` (chi ha effettuato la verifica preformatura)
- Messaggio: `"Ordine PR000123 non avanzabile: kit incompleto in ricevimento linea. Codici: [lista]"`
- L'ordine entra in stato `BLOCKED_MISSING_MATERIAL`

#### 5.3.3 Richiesta Materiale Aggiuntivo durante Produzione

Se durante la produzione vengono deteriorati o persi materiali:

1. `PROD_OP` crea richiesta nel sistema indicando codice e quantità aggiuntiva
2. **Email + Popup** al `WH_MGR` con lista delle richieste pendenti
3. `WH_MGR` verifica disponibilità e preleva
4. Conferma nel sistema: stato `READY_FOR_PICKUP`
5. **Popup** su postazione `PROD_OP`: `"Materiale pronti per prelievo in magazzino"`

#### 5.3.4 Recupero Materiale "Dichiarato Mancante"

Se materiale precedentemente dichiarato mancante viene **ritrovato** in produzione:

1. `PROD_OP` aggiorna lo stato del materiale nel sistema: `FOUND_IN_PRODUCTION`
2. Il sistema annulla/aggiorna la richiesta pendente verso il magazzino
3. Notifica automatica al `WH_MGR` per evitare prelievo duplicato
4. Il log mantiene traccia dell'evento per analisi futura

---

## 6. Database — Estensioni Schema

### 6.1 Nuova Tabella: `picking_lists`

```sql
CREATE TABLE picking_lists (
    id                  INT IDENTITY PRIMARY KEY,
    essegi_list_id      NVARCHAR(50) NOT NULL,          -- ID univoco lista Essegi
    order_ids           NVARCHAR(500) NOT NULL,          -- 'PR000123' o 'PR000123/PR000124'
    upload_date         DATETIME DEFAULT GETDATE(),
    uploaded_by         INT REFERENCES users(id),
    status              NVARCHAR(30) DEFAULT 'OPEN',     -- OPEN, PARTIAL, CLOSED, REOPENED
    closed_date         DATETIME,
    closed_by           INT REFERENCES users(id),
    derogation_by       INT REFERENCES users(id),
    derogation_note     NVARCHAR(500)
);
```

### 6.2 Nuova Tabella: `picking_list_items`

```sql
CREATE TABLE picking_list_items (
    id                  INT IDENTITY PRIMARY KEY,
    picking_list_id     INT REFERENCES picking_lists(id),
    order_id            NVARCHAR(30) NOT NULL,           -- singolo PR000...
    material_code       NVARCHAR(100) NOT NULL,
    unique_number       NVARCHAR(100),                   -- Unique# etichetta
    qty_required        DECIMAL(10,3) NOT NULL,
    qty_picked          DECIMAL(10,3) DEFAULT 0,
    pick_status         NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, PARTIAL, COMPLETE
    picked_by           INT REFERENCES users(id),
    picked_date         DATETIME,
    notes               NVARCHAR(500)
);
```

### 6.3 Estensione Tabella: Piano Produzione

Aggiungere colonna priorità alla tabella del piano di produzione esistente:

```sql
ALTER TABLE production_plan
ADD priority TINYINT DEFAULT 0
    CHECK (priority IN (0, 1, 2, 3));

-- Indice per ottimizzare l'ordinamento
CREATE INDEX IX_production_plan_priority_date
    ON production_plan (priority, planned_date);
```

### 6.4 Nuova Tabella: `kit_verification_log`

```sql
CREATE TABLE kit_verification_log (
    id                  INT IDENTITY PRIMARY KEY,
    order_id            NVARCHAR(30) NOT NULL,
    phase               NVARCHAR(20) NOT NULL,           -- WH, PREFORMING, PRODUCTION
    event_type          NVARCHAR(30) NOT NULL,           -- SCAN, VERIFY_OK, VERIFY_FAIL,
                                                         -- REQUEST_MATERIAL, MATERIAL_FOUND
    material_code       NVARCHAR(100),
    unique_number       NVARCHAR(100),
    qty_expected        DECIMAL(10,3),
    qty_actual          DECIMAL(10,3),
    operator_id         INT REFERENCES users(id),
    event_date          DATETIME DEFAULT GETDATE(),
    notes               NVARCHAR(1000)
);
```

### 6.5 Nuova Tabella: `material_requests`

```sql
CREATE TABLE material_requests (
    id                  INT IDENTITY PRIMARY KEY,
    order_id            NVARCHAR(30) NOT NULL,
    requesting_phase    NVARCHAR(20) NOT NULL,           -- PREFORMING, PRODUCTION
    material_code       NVARCHAR(100) NOT NULL,
    qty_requested       DECIMAL(10,3) NOT NULL,
    requested_by        INT REFERENCES users(id),
    request_date        DATETIME DEFAULT GETDATE(),
    wh_status           NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, CONFIRMED, CANCELLED
    confirmed_by        INT REFERENCES users(id),
    confirmed_date      DATETIME,
    resolution          NVARCHAR(30),                    -- PROVIDED, FOUND_IN_PRODUCTION, CANCELLED
    resolved_date       DATETIME
);
```

---

## 7. Sistema di Notifiche

### 7.1 Canali di Notifica

| Canale | Trigger | Destinatario |
|--------|---------|--------------|
| **Email** | Verifica WH fallita | `WH_OP` + `WH_MGR` |
| **Popup laptop** | Verifica WH fallita | `WH_OP` + `WH_MGR` |
| **Email** | Verifica Preformatura fallita | `PF_OP` + `PF_MGR` |
| **Popup laptop** | Verifica Preformatura fallita | `PF_OP` + `PF_MGR` |
| **Email** | Verifica Produzione fallita | `PROD_OP` + `PROD_MGR` |
| **Popup laptop** | Richiesta materiale aggiuntivo | `WH_MGR` |
| **Popup laptop** | Materiale pronto per prelievo | `PF_OP` o `PROD_OP` (richiedente) |
| **Popup laptop** | Materiale ritrovato (cancel richiesta) | `WH_MGR` |

### 7.2 Integrazione con Sistema Popup Esistente

Il sistema di popup è già attivo per i materiali indiretti. L'estensione deve:
1. Riutilizzare lo stesso meccanismo di invio popup
2. Aggiungere una **categoria** al messaggio popup: `DIRECT_MATERIAL` (per distinguere dai materiali indiretti)
3. Il popup deve includere link diretto alla pagina dell'ordine coinvolto

### 7.3 Template Notifiche

#### Verifica WH Fallita (Email/Popup → WH_OP + WH_MGR)
```
OGGETTO: [ALERT] Verifica Kit NON CONFORME — Ordine {order_id}

La verifica di ingresso in Preformatura per l'ordine {order_id}
ha rilevato discrepanze.

Codici non conformi:
{lista_codici_con_quantita}

La lista di prelievo è stata RIAPERTA.
Accedi al sistema per effettuare le correzioni.

→ Link diretto: {url_lista_prelievo}
```

#### Richiesta Materiale Aggiuntivo (Email/Popup → WH_MGR)
```
OGGETTO: [RICHIESTA] Materiale aggiuntivo richiesto — Ordine {order_id}

{richiedente} ha richiesto materiale aggiuntivo per l'ordine {order_id}
da fase: {fase}

Materiale: {material_code}
Quantità: {qty}
Motivazione: {nota}

→ Link diretto: {url_richiesta}
```

---

## 8. Interfaccia Web — Struttura Pagine

### 8.1 Struttura Navigazione

```
PlanRespect
└── [Menu] Kit Preparation
    ├── 📋 Piano Produzione + Priorità     (ruolo: PLAN)
    ├── 📦 Prelievo Magazzino              (ruolo: WH_OP, WH_MGR)
    ├── 🔧 Preformatura — Ingresso         (ruolo: PF_OP, PF_MGR)
    ├── 🏭 Produzione — Ricevimento        (ruolo: PROD_OP, PROD_MGR)
    ├── 🔔 Richieste Materiale             (ruolo: WH_MGR, tutti)
    └── 📊 Dashboard Stato Kit             (tutti i ruoli)
```

### 8.2 Dashboard Stato Kit

Vista riepilogativa di tutti gli ordini in lavorazione con stato per fase:

| Ordine | Priorità | Data Piano | WH | Preformatura | Produzione | Alert |
|--------|----------|------------|-----|--------------|------------|-------|
| PR000123 | 🔴 P1 | 12/06 | 🟢 OK | 🟠 IN CORSO | ⬜ | — |
| PR000124 | 🟠 P2 | 12/06 | 🟢 OK | 🔴 FAIL | ⬜ | ⚠️ |
| PR000125 | ⬜ P0 | 14/06 | 🔴 APERTA | ⬜ | ⬜ | — |

---

## 9. Gestione Eccezioni e Casi Speciali

### 9.1 Lista Essegi con Ordini Multipli

Quando la lista Essegi contiene più ordini (`PR000123/PR000124`):
- Le quantità cumulate vengono disaggregate tramite query su `traceability_rb`
- Le scansioni WH vengono associate all'ordine corretto in base al `unique_number`
- La chiusura della lista richiede che **tutti gli ordini** siano completamente prelevati (o con deroga)

### 9.2 Unique Number Non Trovato in DB

Se il barcode scansionato non corrisponde a nessun `unique_number` nel DB:
- Il sistema mostra un **alert visivo** nell'interfaccia di scansione
- Logga l'evento in `kit_verification_log` con `event_type = 'UNKNOWN_UNIQUE_NUMBER'`
- Non blocca la sessione ma impedisce la chiusura della lista fino a risoluzione

### 9.3 Materiale Ritrovato dopo Dichiarazione Mancante

Flusso specifico per annullare una richiesta già inviata al WH:
1. `PROD_OP` seleziona la richiesta aperta dalla lista
2. Conferma che il materiale è stato ritrovato (con nota obbligatoria)
3. Il sistema aggiorna `material_requests.resolution = 'FOUND_IN_PRODUCTION'`
4. Invia notifica a `WH_MGR` per evitare prelievo inutile
5. Se il WH aveva già confermato il prelievo, `WH_MGR` deve manualmente chiudere il ciclo

---

## 10. Roadmap di Implementazione Suggerita

### Fase A — Fondamenta (Sprint 1)
- [ ] Aggiunta colonna `priority` al piano di produzione
- [ ] UI di assegnazione priorità (pianificatore)
- [ ] Ordinamento lista WH per priorità
- [ ] Caricamento file Essegi XLSX

### Fase B — Prelievo WH (Sprint 2)
- [ ] Query di interpolazione con `traceability_rb`
- [ ] Interfaccia scansione barcode (colori verde/arancione/rosso)
- [ ] Logica chiusura lista e chiusura con deroga
- [ ] Log eventi `kit_verification_log`

### Fase C — Preformatura (Sprint 3)
- [ ] Interfaccia presa in carico preformatura
- [ ] Verifica ingresso e logica di mismatch
- [ ] Sistema notifiche Email + Popup (estensione sistema esistente)
- [ ] Richiesta materiale aggiuntivo preformatura

### Fase D — Produzione (Sprint 4)
- [ ] Interfaccia ricevimento kit in linea
- [ ] Verifica e gestione ordine bloccato
- [ ] Richiesta materiale aggiuntivo produzione
- [ ] Flusso materiale ritrovato

### Fase E — Dashboard e Reporting (Sprint 5)
- [ ] Dashboard stato kit centralizzata
- [ ] Report storico eccezioni e scrap
- [ ] Analisi cause ricorrenti di mancanza materiale

---

## 11. Note Tecniche per Implementazione

### 11.1 Stack Tecnologico Suggerito

Allineato con il progetto PlanRespect esistente:

| Layer | Tecnologia |
|-------|-----------|
| Backend | Python (Flask/FastAPI) |
| Frontend | HTML + JavaScript (compatibile con avvio da browser) |
| Database | SQL Server (`traceability_rb` esistente) |
| Barcode scan | Input da scanner USB HID (simula tastiera) |
| Notifiche popup | Estensione sistema popup indiretto esistente |
| Notifiche email | SMTP / integrazione esistente |

### 11.2 Avvio da Browser tramite PlanRespect

Il modulo deve essere raggiungibile tramite un URL interno (es. `http://localhost:XXXX/kit-prep`) oppure un link nel menu principale di PlanRespect. L'autenticazione usa le credenziali già gestite dall'applicazione, con mapping a ruoli specifici.

### 11.3 Scanner Barcode

Gli scanner barcode USB HID inviano il codice come input tastiera — nessun driver speciale necessario. L'interfaccia deve:
- Avere il campo input sempre in focus durante la sessione di scansione
- Accettare sia scansione barcode che inserimento manuale
- Validare il formato `unique_number` prima della scrittura a DB

---

*Documento generato il 2026-06-11 — Versione 1.0*  
*Da aggiornare dopo revisione con il team di implementazione*
