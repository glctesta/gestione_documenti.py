# PlanRespect — Kit Preparation & Verification Module
## Specifiche Funzionali per Implementazione

**Progetto:** PlanRespect — Estensione Modulo Preparazione Kit Produzione
**Percorso progetto:** `C:\Users\gtesta\PythonProjetcs\Python\PlanRespect`
**Versione documento:** 1.2
**Data:** 2026-06-12
**Autore:** G. Testa
**Destinatario:** Claude Code (implementazione) / Team sviluppo

> **Novità v1.2** — recepiti gli esiti della revisione del 12.06.2026:
> chiave autorizzazione corretta in `verifica_kit_materiale`; normalizzazione OrderNumber a 9 caratteri (§5.1.1); destinatari email da `settings` `Sys_email_Kit_materiali` (§7.4); popup via mapping postazioni di `wh_workstation_config.py` (§7.2); reminder richieste materiale default 10 minuti (§7.1); traduzioni dinamiche multilingua (§11.4); §12 convertita da "Punti Aperti" a "Decisioni di Revisione".

> **Novità v1.1** rispetto alla v1.0:
> 1. Autenticazione tramite la funzione esistente `_execute_authorized_action` (DocumentManagement, `main.py`) con le chiavi `verifica_kit_materiale` e `conferma_kit_completamento` — sostituisce il sistema di ruoli/login dedicato ipotizzato in v1.0 (§2.3).
> 2. Sorgente lista prelievo Essegi definita: file in `T:\KITTING` (XLSX preferito, PDF "Reels traceability" come riferimento) con tracciato colonne reale (§5.1.1).
> 3. Matching materiali tramite la query già usata per la stampa etichette (`label_printing_gui.py`), database **`Traceability_RS`** — corregge il riferimento errato a `traceability_rb` della v1.0 (§5.1.2).
> 4. Nuova funzionalità **Ripresa Lavoro** per sessioni di check/conferma interrotte (§5.4).
> 5. Correzioni incongruenze v1.0: tabella notifiche §7.1, SQL ordinamento §3.2, priorità su tabella di affiancamento §6.3, tabella ponte ordini §6.1, stato kit per ordine §6.6.
> 6. Nuova sezione **Punti Aperti** (§12).

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

### 1.3 Rapporto con il Modulo Kit Esistente

PlanRespect contiene già un modulo kit (`kit_preparation.py`, `kit.html`) che calcola le date di preparazione (lead days per fase SMT/PTHM) e gestisce i flag `is_prepared` / `is_verified` con operatore e timestamp. Il nuovo flusso a 3 fasi **estende** quel modulo:

| Concetto esistente | Mappatura nel nuovo flusso |
|--------------------|----------------------------|
| `is_prepared` (kit "PREGATIT") | Equivale alla chiusura della **Fase WH** (lista prelievo `CLOSED` o `PARTIAL` con deroga) |
| `is_verified` | Equivale alla verifica di ingresso **Preformatura** superata (`IN_PREFORMING`) |
| Lista kit per data dovuta | Resta la vista di pianificazione; la nuova lista WH ordinata per priorità (§3) ne è il dettaglio operativo |

I flag esistenti non vengono duplicati: vengono **alimentati** dalle transizioni di stato del nuovo flusso, così le viste attuali continuano a funzionare.

---

## 2. Architettura Generale del Sistema

### 2.1 Fonti Dati Principali

```
┌─────────────────────────────────────────────────────────────────┐
│                    FONTI DATI DEL SISTEMA                        │
├─────────────────────┬───────────────────────────────────────────┤
│ Piano Produzione    │ File Excel di programmazione esistente     │
│                     │ (PlanningMachine, già usato da PlanRespect)│
├─────────────────────┼───────────────────────────────────────────┤
│ Lista Prelievo      │ File generati da sistema Essegi in         │
│ T:\KITTING          │ T:\KITTING — XLSX (preferito) o PDF        │
│                     │ "Reels traceability" (AutoSMD)             │
├─────────────────────┼───────────────────────────────────────────┤
│ DB Traceability_RS  │ Query BOM/componenti per ordine            │
│                     │ (la stessa della stampa etichette)         │
├─────────────────────┼───────────────────────────────────────────┤
│ Sistema Popup       │ Già attivo per materiali indiretti         │
│                     │ (estendere per notifiche dirette)          │
└─────────────────────┴───────────────────────────────────────────┘
```

### 2.2 Interfaccia

Il modulo è raggiungibile dal menu di PlanRespect / DocumentManagement. Ogni fase espone una pagina/scheda dedicata. Le operazioni che modificano lo stato del kit (verifiche, conferme, prelievi) sono **sempre precedute da login** tramite il meccanismo descritto in §2.3.

### 2.3 Autorizzazioni — `_execute_authorized_action`

> **Sostituisce** il sistema di 7 ruoli con login separato della v1.0.

Le operazioni protette usano la funzione **già esistente** `_execute_authorized_action(menu_translation_key, action_callback)` (DocumentManagement, `main.py`), che gestisce: LoginWindow, `db.authenticate_and_authorize(user_id, password, key)`, cache autorizzazioni, verifica scadenza password e logging dell'operatore (`last_authenticated_user_name`, `last_authorized_user_id`).

**Chiavi di autorizzazione (nuove, da registrare nelle tabelle autorizzazioni come le altre menu key):**

| Chiave | Operazioni coperte |
|--------|--------------------|
| `verifica_kit_materiale` | Tutte le **verifiche** (ingresso Preformatura §5.2, ricevimento Produzione §5.3) e **tutte le operazioni della sezione Produzione** (richieste materiale aggiuntivo, materiale ritrovato, sblocco ordine) |
| `conferma_kit_completamento` | **Esecuzione prelievo WH** (apertura sessione di scansione) e **conferma dell'avvenuto completamento del kit** (chiusura lista, chiusura con deroga) |

Note:
- La chiave è stata **corretta in revisione** (12.06.2026) da `verifica_kit_materile` a **`verifica_kit_materiale`**: usare quest'ultima, identica ovunque (DB, codice, script di setup).
- L'identità dell'operatore registrata in `picked_by` / `verified_by` / `confirmed_by` proviene da `_execute_authorized_action` (nessun campo operatore inserito a mano).
- I ruoli organizzativi della v1.0 (`WH_OP`, `WH_MGR`, `PF_OP`, ...) restano come **destinatari delle notifiche** (§7), non come ruoli di login: gli indirizzi email si ricavano dalla setting `Sys_email_Kit_materiali` (§7.4), i popup usano il mapping postazioni di `wh_workstation_config.py` (§7.2).

---

## 3. Gestione Priorità Ordini

### 3.1 Schema di Priorità

Al piano di produzione viene affiancata una priorità per ordine:

| Valore | Significato | Logica di esecuzione |
|--------|-------------|----------------------|
| `0` | Nessuna priorità speciale | Ordinamento per data piano |
| `1` | Massima priorità | Da evadere per primo, sopra qualsiasi altro |
| `2` | Alta priorità | Dopo tutti i P1 |
| `3` | Priorità media | Dopo tutti i P2 |

> Il piano di produzione vive su **file Excel**, non su tabella DB: la priorità è salvata nella tabella di affiancamento `order_priority` (§6.3), con chiave `order_number` — stesso pattern di `KitLeadTimeOverride`.

### 3.2 Regole di Ordinamento Lista

```sql
ORDER BY
    CASE WHEN priority = 0 THEN 4 ELSE priority END ASC,
    planned_date ASC,
    order_number ASC
```

(Semplificato rispetto alla v1.0: il secondo `CASE` su `PLANNED_DATE` era ridondante.)

### 3.3 UI Assegnazione Priorità

- Accessibile dal modulo pianificazione
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
                   │ (login: conferma_   │
                   │  kit_completamento) │
                   └──────────┬──────────┘
                              │
              [Seleziona file da T:\KITTING (XLSX)]
                              │
              [Match con query etichette Traceability_RS]
                              │
              [Scansione: ReelCode + Materiale + Qty]
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
                     │      │  DEROGA RESP. WH?   │
                     │      └──────┬──────────────┘
                     │          SÌ │          NO
                     │             │     [Rimane aperto: sessione
                     │             │      sospesa → Ripresa Lavoro §5.4]
                     │    [Annota mancanze]
                     │    [Chiude con flag PARZIALE]
                     │             │
                   ┌─▼─────────────▼──────────────┐
                   │   FASE 2: PREFORMATURA        │
                   │ (login: verifica_kit_materiale)│
                   └──────────────┬────────────────┘
                                  │
                  [Scansione: ReelCode + Qty Ricevuta]
                                  │
              ┌───────────────────▼────────────────┐
              │     VERIFICA INGRESSO PREFORMATURA  │
              └──────────┬─────────────────┬───────┘
                      OK │                 │ NON OK
                         │      ┌──────────▼──────────┐
                         │      │ ALERT → operatore WH │
                         │      │ + resp. WH           │
                         │      │ Email + Popup        │
                         │      │ Riapre lista WH      │
                         │      └─────────────────────┘
                         │
              ┌──────────▼───────────────────────────┐
              │     DURANTE PREFORMATURA              │
              │   Scarto > atteso BOM?                │
              └──────────┬───────────────────────────┘
                         │
          [Richiesta Materiale Aggiuntivo → resp. WH]
          [Email + Popup]
          [WH conferma prelievo]
          [Popup richiedente: materiale disponibile]
                         │
                   ┌─────▼──────────────────────────┐
                   │   FASE 3: PRODUZIONE            │
                   │ (login: verifica_kit_materiale)  │
                   └─────────────┬──────────────────┘
                                 │
                  [Ricezione Kit in Linea]
                  [Scansione: ReelCode + Qty]
                                 │
              ┌──────────────────▼─────────────────┐
              │     VERIFICA RICEVUTO PRODUZIONE    │
              └──────────┬──────────────────┬──────┘
                      OK │                  │ NON OK
                         │     ┌────────────▼──────────┐
                         │     │ ALERT → operatore PF   │
                         │     │ + resp. PF             │
                         │     │ Email + Popup          │
                         │     │ Ordine bloccato        │
                         │     └───────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │     DURANTE PRODUZIONE                 │
              │   Materiale deteriorato/perso?         │
              └──────────┬────────────────────────────┘
                         │
          [Richiesta aggiuntiva → resp. WH]
          [WH preleva + conferma disponibilità]
          [Popup richiedente: materiale pronto]
                         │
          [Se materiale "mancante" ritrovato]
          [Operatore produzione aggiorna stato]
                         │
                   ┌─────▼─────────┐
                   │  ORDINE OK    │
                   │  Kit completo │
                   └───────────────┘
```

> Il fallimento della verifica in fase N notifica **gli attori della fase N-1** (chi ha consegnato), non quelli della fase corrente. Vedi tabella notifiche §7.1 (corretta rispetto alla v1.0).

---

## 5. Specifiche Dettagliate per Fase

### 5.1 FASE 1 — Prelievo Magazzino

#### 5.1.1 Sorgente Lista Prelievo Essegi — `T:\KITTING`

I file della lista di prelievo sono salvati dal sistema Essegi in **`T:\KITTING`** in due formati con la stessa impaginazione:

- **PDF** — report "Reels traceability" (AutoSMD v4.4.x), il documento più dettagliato (include descrizione, brand, date code, supplier, partnumber)
- **XLSX** — stesso layout, **formato preferito per l'import** perché a parsing deterministico

**Formato scelto per l'import: XLSX.** Il PDF resta il documento di riferimento umano/stampa; il parsing PDF di un report impaginato (righe a capo, descrizioni multilinea) è fragile e non aggiunge dati necessari al matching.

**Tracciato XLSX:**

| Intestazione colonna | Contenuto | Note |
|----------------------|-----------|------|
| `REEL CODE` | **Unique Number** | Codice univoco della scatola/bobina, es. `HU000004744`, `HU000013367_01`. Esistono anche codici brevi numerici (es. `000229`) |
| `ITEM CODE` | **MaterialCode** | Codice materiale come in SQL (`Components.ComponentCode`), es. `COPO+150N63V` |
| `QT` | **Quantity** | Quantità nella scatola/bobina |

> **Rilevazione Sprint 0 (file reale `Traceability.xlsx`):** le posizioni delle colonne **non sono fisse** — nel campione reale i dati partono dalla colonna B (`REEL CODE`=B, `ITEM CODE`=C, `QT`=E) anziché dalla A. Il parser deve **individuare la riga di intestazione `REEL CODE`** (entro le prime ~20 righe) e ricavare gli indici di colonna dai nomi delle intestazioni, non da posizioni fisse (già implementato in `validate_essegi_xlsx.py`).

**Ordini di produzione:** la **prima riga di ogni pagina** riporta gli ordini che compongono la lista, in formato compatto, es.:

```
PR554/553/552/551
PFVO+VOR-791/790        ← riga successiva: famiglia prodotto
```

Il parser deve espandere il formato compatto: `PR554/553/552/551` → `PR554`, `PR553`, `PR552`, `PR551` (il prefisso `PR` si applica a tutti i segmenti).

**Normalizzazione OrderNumber (decisione di revisione):** tra `PR` e il numero d'ordine vanno inseriti tanti zeri quanti servono per ottenere una lunghezza totale di **9 caratteri** (`PR` incluso). Esempio: `PR554` → **`PR0000554`**, `PR12345` → `PR0012345`. Gli ordini normalizzati vanno validati contro `Traceability_RS.dbo.Orders.OrderNumber`.
ATTENZIONE Gli ordini in sisitema non si troveranno con '=' ma con like 'PR%[numero del file excel] dato che la loro formattazione corretta e' di 9 caratteri compreri PR e il numero quindi potresti usare questa regola per trasformare il numeo PR554 in PR0000554.


**Selezione file:**
1. Il sistema elenca i file presenti in `T:\KITTING` (filtro `*.xlsx`)
2. Se esiste **un solo file**, viene proposto direttamente (con conferma)
3. Se esistono **più file**, si apre una finestra di scelta con: nome file, data modifica, ordini rilevati dall'intestazione — l'utente seleziona quello corretto
4. Il file scelto viene registrato sulla lista di prelievo: nome, percorso, **hash SHA-256**, data modifica (necessario per la Ripresa Lavoro §5.4)

#### 5.1.2 Matching con DB `Traceability_RS` (query etichette)

> Corregge la v1.0: il database è **`Traceability_RS`**, non `traceability_rb`, e la query di riferimento è quella **già esistente** usata dalla stampa etichette (`label_printing_gui.py`, funzione `_load_order_data`, aperta via `open_label_print_with_login`).

Per ogni ordine estratto dall'intestazione del file, il sistema esegue la query etichette che restituisce la BOM per ordine:

```sql
-- Query esistente (label_printing_gui.py) — riassunto delle colonne usate
DECLARE @Ordernumber VARCHAR(250) = ?;
SELECT
    P.ProductCode,
    O.OrderNumber,
    O.OrderQuantity,
    C.ComponentCode,          -- ← chiave di match con colonna B del file
    C.ComponentDescription,
    AR.CodRiferimentiConcatenati,
    pp.ParentPhaseName
FROM Orders O
INNER JOIN Products P              ON P.IDProduct = O.IDProduct
INNER JOIN ProductComponentsErp PCE ON PCE.IDProduct = P.IDProduct
INNER JOIN ProductRiferiments PR    ON PR.IDProductCompErp = PCE.IDProductCompErp
INNER JOIN Components C             ON PCE.IDComponent = C.IDComponent
INNER JOIN ParentPhases pp          ON pp.IDParentPhase = PR.IDParentPhase
LEFT JOIN AggregatedRiferimenti AR  ON ...
WHERE O.OrderNumber = @Ordernumber
```

**Chiave di matching:** `file.MaterialCode (col. B)` ⇔ `Components.ComponentCode`, nel contesto dell'ordine. Il `Unique Number` (col. A) identifica la singola scatola/bobina e viene registrato a ogni scansione. di fatto la scansione deve matchare il CODICE UNICO 'Unique numer' che si trova nella label della confezione del prodotto. Dopo la scansione effettuata dall'operatore, il distema verifichera' che si tratta dello stesso codice che risulta dalla query e dal file excle caricato. 

**Regole:**
- Un materiale presente nel file ma assente nella BOM dell'ordine → riga segnalata `NOT_IN_BOM` (warning, non bloccante, loggata)
- Un materiale in BOM ma assente nel file → riga `MISSING_FROM_LIST` (resta 🔴 finché non scansionata o derogata)
- Più scatole (Unique Number diversi) dello stesso `ComponentCode` → le quantità si **sommano** sul fabbisogno del materiale
- Liste multi-ordine: le quantità del file sono cumulate; la disaggregazione per ordine usa `OrderQuantity` × coefficiente BOM per ordine; allocazione proporzionale con correzione manuale (decisione di revisione §12 #1)
- **Suffisso variante `|n` (rilevazione Sprint 0):** il `ComponentCode` a DB può avere un suffisso `|n` assente nel report Essegi (es. file `CSVO+VOR-791>A` ⇔ DB `CSVO+VOR-791>A|1`). Il matching deve prima tentare l'uguaglianza esatta, poi il match come prefisso `codice + '|%'` (già implementato in `validate_essegi_xlsx.py`)

#### 5.1.3 Interfaccia di Scansione WH

Login preventivo: **`conferma_kit_completamento`** via `_execute_authorized_action`.

```
┌─────────────────────────────────────────────────────┐
│  PRELIEVO KIT  │  Ordini: PR554/553/552/551          │
│  File: KIT_PR554.xlsx │ Operatore: [da login]        │
├─────────────────────────────────────────────────────┤
│  Scansiona Unique Number (Reel Code): [___________]  │
│  Quantità prelevata:                  [___________]  │
│                                       [CONFERMA]     │
├──────┬──────────────────┬─────────────┬─────────────┤
│ Stato│ Codice Materiale │ Unique Nr   │ Req / Prel  │
├──────┼──────────────────┼─────────────┼─────────────┤
│  🟢  │ COPO+150N63V     │ HU000004744 │  435 / 435  │
│  🟠  │ RET5+3.9K        │ HU000016711 │   90 / 40   │
│  🔴  │ FURA+1.6A        │             │ 1530 / 0    │
└──────┴──────────────────┴─────────────┴─────────────┘
│  [SOSPENDI SESSIONE]  (salva stato → Ripresa §5.4)  │
│  [CHIUDI LISTA]  (solo se tutto 🟢)                 │
│  [CHIUDI CON DEROGA] (login responsabile WH)        │
└─────────────────────────────────────────────────────┘
```

**Logica colori:**
- **Verde** `🟢`: quantità prelevata = quantità richiesta
- **Arancione** `🟠`: 0 < quantità prelevata < quantità richiesta
- **Rosso** `🔴`: quantità prelevata = 0

**Comportamento scansione:** alla lettura del barcode il sistema cerca il `unique_number` nelle righe del file caricato; se trovato propone materiale e quantità attesa, l'operatore conferma o corregge la quantità fisica. Se non trovato → §9.2.

#### 5.1.4 Chiusura con Deroga

Se non tutte le righe sono verdi, "Chiudi Lista" è disabilitato. Il pulsante **"Chiudi con Deroga"**:
1. Richiede un **nuovo** `_execute_authorized_action` (stessa chiave `conferma_kit_completamento`) eseguito dal responsabile WH — l'identità del derogante è quella di questo secondo login
2. Registra: `picking_status = 'PARTIAL'`, `derogation_by`, `missing_items` (lista codici mancanti), nota obbligatoria
3. Le righe incomplete restano `PENDING_COMPLETION`, visibili in dashboard fino a completamento

---

### 5.2 FASE 2 — Presa in Carico Preformatura

Login preventivo: **`verifica_kit_materiale`** via `_execute_authorized_action`.

#### 5.2.1 Scansione Ingresso

L'operatore Preformatura scansiona ogni materiale ricevuto: **Unique Number** + **quantità fisica ricevuta**. Il sistema confronta con quanto chiuso in Fase WH.

#### 5.2.2 Esito Verifica

**Caso A — Tutto OK:**
- Kit in stato `IN_PREFORMING` (e flag `is_verified` del modulo kit esistente impostato)
- Si sblocca l'accesso alla Fase 3

**Caso B — Discrepanza rilevata:**
- Email + Popup all'operatore WH che ha effettuato il prelievo e al responsabile WH
- Messaggio: `"Ordine {order}: verifica fallita in ingresso preformatura. Codici non conformi: [lista]"`
- La lista di prelievo WH viene riaperta in stato `REOPENED`
- Le scansioni Preformatura già effettuate **restano valide**: alla ripresa si riverificano solo i codici non conformi (decisione di revisione)

#### 5.2.3 Richiesta Materiale Aggiuntivo durante Preformatura

1. L'operatore inserisce la richiesta (codice, quantità, motivazione)
2. Email + Popup al responsabile WH
3. Il magazzino preleva e conferma `AVAILABLE_FOR_PICKUP`
4. Popup alla postazione richiedente: `"Materiale [codice] disponibile per prelievo in magazzino"`

---

### 5.3 FASE 3 — Ricezione e Verifica in Produzione

Login preventivo: **`verifica_kit_materiale`** — la stessa chiave copre **tutte le operazioni della sezione Produzione** (verifica ricevuto, richieste materiale, materiale ritrovato).

#### 5.3.1 Presa in Carico Linea

Il responsabile di linea scansiona il kit ricevuto: **Unique Number** + **quantità fisica**.

#### 5.3.2 Esito Verifica

**Caso A — Tutto confermato:** kit in stato `RECEIVED_IN_PRODUCTION`, produzione procede.

**Caso B — Mancanza rilevata:**
- Email + Popup all'**operatore Preformatura** e al suo responsabile (attori della fase precedente)
- Messaggio: `"Ordine {order} non avanzabile: kit incompleto in ricevimento linea. Codici: [lista]"`
- Ordine in stato `BLOCKED_MISSING_MATERIAL`

#### 5.3.3 Richiesta Materiale Aggiuntivo durante Produzione

1. L'operatore crea la richiesta (codice e quantità)
2. Email + Popup al responsabile WH con lista richieste pendenti, o ai computer che sono stati gia' marcati per il popup del prelievo materiali indiretti (procedura gia' presente nel progtramma. Eventualmente, utilizzando la stessa procedura si potrebbero distinguere le macchine destinate ai materiali indiretti e ai materiali di produzioni, magari usando una diversa chiave di setup.)
3. Il WH verifica disponibilità, preleva e conferma `READY_FOR_PICKUP`
4. Popup alla postazione richiedente: `"Materiale pronto per prelievo in magazzino"`
5. in ogni caso i computer che lavoreranno per questa procedura devono essere dichiarati, tramite il programma, al pari della funzione che dichiara i computer per i materiali indiretti. (vedi nota precedente)

#### 5.3.4 Recupero Materiale "Dichiarato Mancante"

1. L'operatore aggiorna lo stato: `FOUND_IN_PRODUCTION` (nota obbligatoria)
2. Il sistema annulla/aggiorna la richiesta pendente verso il magazzino
3. Notifica al responsabile WH per evitare prelievo duplicato
4. Il log mantiene traccia dell'evento

---

### 5.4 Ripresa Lavoro (sessioni interrotte) — NUOVO in v1.1

Le operazioni di check e conferma possono essere sospese o interrotte (cambio turno, crash, chiusura applicazione, deroga negata). Il sistema deve permettere di **riprendere esattamente da dove si era rimasti**, sapendo **quale file** era stato usato per il confronto.

#### 5.4.1 Persistenza dello stato di sessione

Ogni sessione di scansione (WH, Preformatura, Produzione) salva su DB **a ogni scansione confermata** (non solo alla chiusura):

- riferimento lista/ordine e fase
- file sorgente usato: percorso, nome, **hash SHA-256**, data modifica
- righe già scansionate con quantità e timestamp
- operatore (da `_execute_authorized_action`)
- stato sessione: `ACTIVE`, `SUSPENDED`, `COMPLETED`, `ABORTED`

Tabella dedicata `kit_sessions` (§6.7). Nessun lavoro è perso: la chiusura inattesa dell'app lascia la sessione `ACTIVE` e la riapertura la propone come da riprendere.

#### 5.4.2 Flusso di ripresa

1. All'apertura della pagina di fase, il sistema cerca sessioni `ACTIVE`/`SUSPENDED` per gli ordini visibili
2. Se trovata: prompt *"Sessione interrotta il {data} da {operatore} — file: {nome file}. Riprendere?"*
3. Alla ripresa il sistema **ricarica il file registrato** e ne ricalcola l'hash:
   - **Hash identico** → ripresa trasparente dal punto esatto (righe già scansionate restano confermate)
   - **File assente o hash diverso** (file rigenerato da Essegi, o utente che seleziona un altro file) → **avviso esplicito** all'utente: *"Il file differisce da quello usato nella sessione precedente"* con confronto (righe aggiunte/rimosse/quantità variate)
4. L'utente sceglie: continuare col **vecchio** dato salvato, oppure adottare il **nuovo** file
5. La scelta viene **registrata** in `kit_verification_log` (`event_type = 'SOURCE_FILE_CHANGED'`, con vecchio/nuovo hash, nomi file e nota) e su `kit_sessions.resume_decision`
6. Se si adotta il nuovo file, le scansioni già fatte vengono ri-validate contro le nuove righe: le righe non più presenti vengono marcate e mostrate all'utente

---

## 6. Database — Estensioni Schema

### 6.1 Nuova Tabella: `picking_lists`

```sql
CREATE TABLE picking_lists (
    id                  INT IDENTITY PRIMARY KEY,
    source_file_name    NVARCHAR(260) NOT NULL,
    source_file_path    NVARCHAR(500) NOT NULL,          -- T:\KITTING\...
    source_file_hash    CHAR(64) NOT NULL,               -- SHA-256
    source_file_date    DATETIME NOT NULL,               -- LastWriteTime del file
    upload_date         DATETIME DEFAULT GETDATE(),
    uploaded_by         INT NOT NULL,                    -- da _execute_authorized_action
    status              NVARCHAR(30) DEFAULT 'OPEN',     -- OPEN, PARTIAL, CLOSED, REOPENED
    closed_date         DATETIME,
    closed_by           INT,
    derogation_by       INT,
    derogation_note     NVARCHAR(500)
);
```

### 6.2 Nuova Tabella: `picking_list_orders` (ponte — sostituisce `order_ids` stringa della v1.0)

```sql
CREATE TABLE picking_list_orders (
    picking_list_id     INT NOT NULL REFERENCES picking_lists(id),
    order_number        NVARCHAR(30) NOT NULL,           -- es. 'PR554' (validato su Traceability_RS.dbo.Orders)
    PRIMARY KEY (picking_list_id, order_number)
);
```

### 6.3 Nuova Tabella: `order_priority` (sostituisce l'ALTER su `production_plan` della v1.0 — il piano vive su Excel)

```sql
CREATE TABLE order_priority (
    order_number        NVARCHAR(30) PRIMARY KEY,
    priority            TINYINT NOT NULL DEFAULT 0 CHECK (priority IN (0,1,2,3)),
    set_by              INT NOT NULL,
    set_date            DATETIME DEFAULT GETDATE()
);
```

### 6.4 Nuova Tabella: `picking_list_items`

```sql
CREATE TABLE picking_list_items (
    id                  INT IDENTITY PRIMARY KEY,
    picking_list_id     INT NOT NULL REFERENCES picking_lists(id),
    order_number        NVARCHAR(30),                    -- NULL finché non disaggregato
    material_code       NVARCHAR(100) NOT NULL,          -- col. B = ComponentCode
    unique_number       NVARCHAR(100),                   -- col. A = Reel Code
    qty_required        DECIMAL(12,3) NOT NULL,          -- col. E
    qty_picked          DECIMAL(12,3) DEFAULT 0,
    pick_status         NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, PARTIAL, COMPLETE,
                                                         -- NOT_IN_BOM, MISSING_FROM_LIST
    picked_by           INT,
    picked_date         DATETIME,
    notes               NVARCHAR(500)
);
```

### 6.5 Nuova Tabella: `kit_verification_log`

```sql
CREATE TABLE kit_verification_log (
    id                  INT IDENTITY PRIMARY KEY,
    order_number        NVARCHAR(30) NOT NULL,
    phase               NVARCHAR(20) NOT NULL,           -- WH, PREFORMING, PRODUCTION
    event_type          NVARCHAR(40) NOT NULL,           -- SCAN, VERIFY_OK, VERIFY_FAIL,
                                                         -- REQUEST_MATERIAL, MATERIAL_FOUND,
                                                         -- UNKNOWN_UNIQUE_NUMBER,
                                                         -- SOURCE_FILE_CHANGED,
                                                         -- SESSION_SUSPENDED, SESSION_RESUMED
    material_code       NVARCHAR(100),
    unique_number       NVARCHAR(100),
    qty_expected        DECIMAL(12,3),
    qty_actual          DECIMAL(12,3),
    operator_id         INT,
    event_date          DATETIME DEFAULT GETDATE(),
    notes               NVARCHAR(1000)
);
```

### 6.6 Nuova Tabella: `kit_status` (stato kit per ordine — colmava una lacuna della v1.0)

```sql
CREATE TABLE kit_status (
    order_number        NVARCHAR(30) PRIMARY KEY,
    status              NVARCHAR(40) NOT NULL,           -- WH_OPEN, WH_PARTIAL, WH_CLOSED,
                                                         -- REOPENED, IN_PREFORMING,
                                                         -- RECEIVED_IN_PRODUCTION,
                                                         -- BLOCKED_MISSING_MATERIAL, COMPLETED
    updated_by          INT,
    updated_date        DATETIME DEFAULT GETDATE()
);
```

### 6.7 Nuova Tabella: `kit_sessions` (Ripresa Lavoro §5.4)

```sql
CREATE TABLE kit_sessions (
    id                  INT IDENTITY PRIMARY KEY,
    picking_list_id     INT REFERENCES picking_lists(id),
    phase               NVARCHAR(20) NOT NULL,           -- WH, PREFORMING, PRODUCTION
    operator_id         INT NOT NULL,
    started_date        DATETIME DEFAULT GETDATE(),
    last_activity_date  DATETIME,
    status              NVARCHAR(20) DEFAULT 'ACTIVE',   -- ACTIVE, SUSPENDED, COMPLETED, ABORTED
    source_file_hash    CHAR(64) NOT NULL,               -- hash del file al momento della sessione
    resume_decision     NVARCHAR(30),                    -- KEEP_OLD_FILE, ADOPT_NEW_FILE
    resume_note         NVARCHAR(500)
);
```

> Le scansioni puntuali stanno già in `picking_list_items` + `kit_verification_log`; `kit_sessions` tiene solo il contesto di sessione (chi, quando, quale file, esito ripresa).

### 6.8 Nuova Tabella: `material_requests`

```sql
CREATE TABLE material_requests (
    id                  INT IDENTITY PRIMARY KEY,
    order_number        NVARCHAR(30) NOT NULL,
    requesting_phase    NVARCHAR(20) NOT NULL,           -- PREFORMING, PRODUCTION
    material_code       NVARCHAR(100) NOT NULL,
    qty_requested       DECIMAL(12,3) NOT NULL,
    requested_by        INT NOT NULL,
    request_date        DATETIME DEFAULT GETDATE(),
    wh_status           NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, CONFIRMED, CANCELLED
    confirmed_by        INT,
    confirmed_date      DATETIME,
    resolution          NVARCHAR(30),                    -- PROVIDED, FOUND_IN_PRODUCTION, CANCELLED
    resolved_date       DATETIME
);
```

> I campi `*_by` referenziano l'utente restituito da `_execute_authorized_action`; la FK puntuale dipende dalla tabella utenti effettiva del sistema di autorizzazioni esistente (da confermare in implementazione).

---

## 7. Sistema di Notifiche

### 7.1 Canali di Notifica (corretta rispetto alla v1.0)

Regola generale: **il fallimento in fase N notifica gli attori della fase N-1**.

| Canale | Trigger | Destinatario |
|--------|---------|--------------|
| Email + Popup | Verifica **Preformatura** fallita | Operatore WH del prelievo + responsabile WH |
| Email + Popup | Verifica **Produzione** fallita | Operatore Preformatura + responsabile Preformatura |
| Email + Popup | Richiesta materiale aggiuntivo | Responsabile WH |
| Popup | Materiale pronto per prelievo | Richiedente (Preformatura o Produzione) |
| Popup | Materiale ritrovato (annullo richiesta) | Responsabile WH |
| Popup | Lista WH riaperta (`REOPENED`) | Operatore WH del prelievo |
| Email + Popup | **Reminder**: richiesta materiale ancora `PENDING` oltre il timeout — default **10 minuti**, configurabile | Responsabile WH |

Il reminder viene ripetuto a ogni scadenza del timeout finché la richiesta non passa a `CONFIRMED` o `CANCELLED` (gestito dallo scheduler esistente).

### 7.2 Integrazione con Sistema Popup Esistente

Il sistema di popup è già attivo per i materiali indiretti. L'estensione deve:
1. Riutilizzare lo stesso meccanismo di invio popup dei materiali indiretti, **incluso il mapping utente→postazione gestito da `wh_workstation_config.py`** (decisione di revisione)
2. Aggiungere una **categoria** al messaggio: `DIRECT_MATERIAL`
3. Includere link/riferimento diretto all'ordine coinvolto

### 7.3 Template Notifiche

#### Verifica Fallita (Email/Popup → attori fase precedente)
```
OGGETTO: [ALERT] Verifica Kit NON CONFORME — Ordine {order_number}

La verifica di ingresso in {fase} per l'ordine {order_number}
ha rilevato discrepanze.

Codici non conformi:
{lista_codici_con_quantita}

La lista di prelievo è stata RIAPERTA.
Accedi al sistema per effettuare le correzioni.

→ Riferimento: {riferimento_lista}
```

#### Richiesta Materiale Aggiuntivo (Email/Popup → responsabile WH)
```
OGGETTO: [RICHIESTA] Materiale aggiuntivo richiesto — Ordine {order_number}

{richiedente} ha richiesto materiale aggiuntivo per l'ordine {order_number}
da fase: {fase}

Materiale: {material_code}
Quantità: {qty}
Motivazione: {nota}

→ Riferimento: {riferimento_richiesta}
```

### 7.4 Destinatari Email

Gli indirizzi dei destinatari si ottengono con la **stessa logica delle altre comunicazioni email** del programma: interrogazione di `traceability_rs.dbo.settings` con `Atribute = 'Sys_email_Kit_materiali'` (riuso dell'helper esistente `utils.get_email_recipients`, stesso pattern di `Sys_email_management` / `Sys_email_referat`). La creazione della setting è a carico dello Sprint 0.

---

## 8. Interfaccia — Struttura

### 8.1 Struttura Navigazione

```
Kit Preparation
├── 📋 Piano Produzione + Priorità      (pianificatore)
├── 📦 Prelievo Magazzino               (login: conferma_kit_completamento)
├── 🔧 Preformatura — Ingresso          (login: verifica_kit_materiale)
├── 🏭 Produzione — Ricevimento         (login: verifica_kit_materiale)
├── 🔔 Richieste Materiale              (login: verifica_kit_materiale)
└── 📊 Dashboard Stato Kit              (sola lettura, nessun login)
```

### 8.2 Dashboard Stato Kit

| Ordine | Priorità | Data Piano | WH | Preformatura | Produzione | Sessione | Alert |
|--------|----------|------------|-----|--------------|------------|----------|-------|
| PR554 | 🔴 P1 | 12/06 | 🟢 OK | 🟠 IN CORSO | ⬜ | — | — |
| PR553 | 🟠 P2 | 12/06 | 🟢 OK | 🔴 FAIL | ⬜ | — | ⚠️ |
| PR552 | ⬜ P0 | 14/06 | 🟠 SOSPESA | ⬜ | ⬜ | ⏸ riprendibile | — |

---

## 9. Gestione Eccezioni e Casi Speciali

### 9.1 Lista con Ordini Multipli

Quando il file contiene più ordini (es. `PR554/553/552/551`):
- Le quantità cumulate vengono disaggregate per ordine tramite la query etichette (BOM × `OrderQuantity`)
- Le scansioni vengono associate all'ordine in base al `unique_number` quando univoco; altrimenti vedi Punti Aperti §12
- La chiusura della lista richiede che **tutti gli ordini** siano completamente prelevati (o con deroga)

### 9.2 Unique Number Non Trovato

Se il barcode scansionato non corrisponde a nessuna riga del file caricato:
- Alert visivo nell'interfaccia di scansione
- Log in `kit_verification_log` con `event_type = 'UNKNOWN_UNIQUE_NUMBER'`
- Non blocca la sessione ma impedisce la chiusura della lista fino a risoluzione

### 9.3 Materiale Ritrovato dopo Dichiarazione Mancante

1. L'operatore produzione seleziona la richiesta aperta
2. Conferma il ritrovamento (nota obbligatoria)
3. `material_requests.resolution = 'FOUND_IN_PRODUCTION'`
4. Notifica al responsabile WH per evitare prelievo inutile
5. Se il WH aveva già confermato il prelievo, il responsabile WH chiude manualmente il ciclo

### 9.4 File Sorgente Cambiato durante Sessione

Vedi §5.4.2 — avviso, scelta dell'utente, registrazione della scelta (`SOURCE_FILE_CHANGED`).

---

## 10. Roadmap di Implementazione Suggerita

### Sprint 0 — Prerequisiti — **COMPLETATO il 12.06.2026**
- [x] Registrazione chiavi autorizzazione `verifica_kit_materiale` e `conferma_kit_completamento` — script `setup_kit_preparation_sprint0.py` eseguito: 5 lingue + MenuValue a DB
- [x] Verifica accesso `T:\KITTING` (raggiungibile; presente campione reale `Traceability.xlsx`)
- [x] Validazione tracciato su file reale — script `validate_essegi_xlsx.py`: 133 righe, 4/4 ordini (`PR0000554/553/552/551`), 40/40 codici materiale (1 via suffisso `|n`) → **TRACCIATO OK**
- [x] Creazione setting `Sys_email_Kit_materiali` (creata con valore vuoto)
- [x] Verifica integrazione popup: meccanismo `wh_workstation_config.py` confermato (flag `wh_host.json` in LOCALAPPDATA per postazione)

**Passi manuali residui (non bloccanti per Sprint 1):**
- [ ] Assegnare le due chiavi agli utenti dalla GUI permessi
- [ ] Compilare i destinatari in `Sys_email_Kit_materiali` (necessario entro Sprint 3)
- [ ] Attivare il flag WH WorkStation sulle postazioni che riceveranno i popup

### Sprint 1 — Fondamenta — **COMPLETATO il 12.06.2026**
- [x] Tabelle DB (§6): 8 tabelle + 5 indici creati in `Traceability_RS` — script `setup_kit_preparation_sprint1.py` (idempotente, `--dry-run`)
- [x] Tabella `order_priority` + UI assegnazione priorità — `kit_preparation_gui.py`, scheda "Priorità Ordini" (ricerca ordine, P0–P3 con badge colorati, MERGE con `set_by`/`set_date`)
- [x] Ordinamento lista WH per priorità — scheda "Liste Prelievo": P1→P2→P3→P0, poi data (query verificata con test end-to-end)
- [x] Parser XLSX da `T:\KITTING` — modulo `kit_essegi_parser.py` (colonne da intestazione `REEL CODE`, ordini normalizzati a 9 caratteri, SHA-256, warnings); finestra scelta file se più di uno; guardia anti-duplicato su hash; testato sul file reale (133 righe, 4 ordini)
- [x] Chiavi di traduzione del modulo: 43 chiavi × 5 lingue inserite — script `insert_kit_preparation_translations.py`
- [x] Integrazione menu: `Materiali → Preparazione Kit Produzione` con due voci — "Priorità Ordini Kit" (login semplice) e "Prelievo Magazzino (Kit)" (login autorizzato `conferma_kit_completamento`)

> **Nota implementativa:** l'UI priorità è protetta da login semplice (identificazione operatore, registrato in `set_by`); se in futuro servirà restringerla, si potrà aggiungere una chiave di autorizzazione dedicata al pianificatore. All'import della lista ogni ordine viene inizializzato in `kit_status` = `WH_OPEN`.

### Sprint 2 — Prelievo WH — **COMPLETATO il 12.06.2026**
- [x] Matching con query etichette — `kit_wh_logic.classify_items`: confronto con l'**unione delle BOM di tutti gli ordini della lista** (rilevazione: i codici di un ordine VOR-790 non sono nella BOM del VOR-791 e viceversa), gestione suffisso `|n`, righe `NOT_IN_BOM` (⚪ informative, scansionabili) e `MISSING_FROM_LIST` (🔴 bloccanti)
- [x] Interfaccia scansione barcode — `kit_scan_gui.py`: campo sempre in focus, semaforo 🟢/🟠/🔴, anteprima quantità alla scansione, warning duplicati, alert + log per unique number sconosciuti (§9.2)
- [x] Chiusura lista / chiusura con deroga — chiusura solo a tutto verde; deroga con **secondo login** `_execute_authorized_action` del responsabile + nota obbligatoria; righe incomplete → `PENDING_COMPLETION`; `kit_status` → `WH_CLOSED`/`WH_PARTIAL`
- [x] Persistenza sessione + Ripresa Lavoro — `kit_sessions`: commit a ogni scansione, sospensione esplicita o alla chiusura finestra, prompt di ripresa, confronto hash SHA-256 con scelta `KEEP_OLD_FILE`/`ADOPT_NEW_FILE` (diff per unique number: aggiunte/aggiornate/`REMOVED`) e log `SOURCE_FILE_CHANGED`
- [x] Log eventi `kit_verification_log` — `SCAN`, `VERIFY_OK`, `CLOSE_DEROGATION`, `UNKNOWN_UNIQUE_NUMBER`, `SOURCE_FILE_CHANGED`, `SESSION_SUSPENDED`/`RESUMED`, `BOM_CHECK`
- [x] Test end-to-end su dati reali (24 verifiche, transazione con rollback): lista 133 righe / 4 ordini — scansioni, deroga (39 mancanti), chiusura completa, ripresa con file cambiato

> **Note implementative Sprint 2:**
> - La logica DB è separata dalla GUI (`kit_wh_logic.py`, funzioni su cursor senza commit) per essere testabile.
> - §9.2 "impedisce la chiusura fino a risoluzione": implementato come **conferma esplicita** in chiusura — con scansioni sconosciute registrate, la chiusura normale chiede conferma e l'evento resta a log; la deroga le copre con la nota.
> - Caso reale: il PCB `CSVO+VOR-791>A` non risulta nella BOM-etichette degli ordini → marcato ⚪ `NOT_IN_BOM`, resta scansionabile e non blocca la chiusura.

### Sprint 3 — Preformatura — **COMPLETATO il 12.06.2026**
- [x] Interfaccia presa in carico — `kit_pf_gui.py`: elenco kit chiusi dal WH ordinato per priorità, verifica ingresso con scansione (consegnato WH vs ricevuto), sessioni `PREFORMING` con sospensione/ripresa; menu `Materiali → Preparazione Kit → Preformatura — Ingresso (Kit)` con login `verifica_kit_materiale`
- [x] Verifica ingresso e mismatch — `kit_pf_logic.py` + tabella `kit_item_checks` (esito per riga/fase, MERGE ri-verificabile): Caso A tutto OK → `IN_PREFORMING`; Caso B discrepanze → righe non conformi tornano `PENDING` al WH, lista `REOPENED`, `kit_status REOPENED`, log `VERIFY_FAIL`
- [x] Notifiche Email + Popup — `kit_notifications.py` (email da `Sys_email_Kit_materiali`, invio in thread post-commit) + tabella `kit_popup_queue` (categoria `DIRECT_MATERIAL`) consumata da `kit_popup_monitor.py` (avviato con i monitor materiali indiretti; target `WH_HOST` via `wh_host.json` o hostname richiedente; **claim atomico**: un popup appare su una sola postazione)
- [x] Richiesta materiale aggiuntivo — dialog in `kit_pf_gui` (ordine, codice, qty, motivazione obbligatoria) → `material_requests` + Email/Popup al WH; scheda **Richieste Materiale** nella finestra Kit (conferma disponibilità → popup al PC richiedente; annullo con motivo)
- [x] Reminder 10 minuti — `kit_requests_reminder.py` schedulabile (Task Scheduler), timeout da setting `Sys_kit_reminder_minutes` (default 10), claim atomico su `wh_last_notified` per istanze concorrenti
- [x] Test end-to-end su dati reali (29 verifiche con rollback): eleggibilità, check OK/mismatch/sconosciuto, riapertura WH con popup, ciclo correzione → `IN_PREFORMING`, richieste (crea/conferma/annulla), claim reminder e popup

> **Note implementative Sprint 3:**
> - `material_requests` estesa con `note`, `requester_computer`, `wh_last_notified`, `requester_last_notified` (setup `setup_kit_preparation_sprint3.py`, idempotente).
> - Le email partono **dopo il commit** della transazione; i popup sono accodati **nella** transazione.
> - Prerequisiti operativi: flag WH WorkStation (`wh_host.json`) sulla postazione magazzino per i popup; setting `Sys_email_Kit_materiali` compilata per le email; `kit_requests_reminder.py` schedulato (es. ogni 5 min).

### Sprint 4 — Produzione — **COMPLETATO il 12.06.2026**
- [x] Interfaccia ricevimento — `kit_prod_gui.py`: elenco kit `IN_PREFORMING` (e bloccati, evidenziati per ri-verifica) per priorità; verifica con scansione dove la **quantità attesa è quella presa in carico dalla preformatura** (`kit_item_checks` fase `PREFORMING`, fallback `qty_picked`); sessioni `PRODUCTION` con sospensione/ripresa; menu `Materiali → Preparazione Kit → Produzione — Ricevimento (Kit)` con login `verifica_kit_materiale`
- [x] Verifica e ordine bloccato — `kit_prod_logic.py`: Caso A tutto confermato → `RECEIVED_IN_PRODUCTION`; Caso B mancanze → ordini `BLOCKED_MISSING_MATERIAL` + Email/Popup alla preformatura (`VERIFY_FAIL` fase `PRODUCTION` a log); il kit bloccato resta ri-verificabile e si sblocca rifacendo la verifica a posto
- [x] Richiesta materiale aggiuntivo produzione — riuso di `create_material_request` con fase `PRODUCTION` (Email + Popup al WH, conferma WH → popup al PC di linea); visibile nella scheda Richieste Materiale
- [x] Flusso materiale ritrovato (§5.3.4/§9.3) — dialog "Materiale Ritrovato" sulle richieste aperte degli ordini del kit, nota obbligatoria → `resolution='FOUND_IN_PRODUCTION'`, log `MATERIAL_FOUND`, popup al WH per evitare il prelievo; se il WH aveva **già confermato**, la conferma è preservata e l'operatore è avvisato che il responsabile WH deve chiudere manualmente il ciclo
- [x] Test end-to-end su dati reali (22 verifiche con rollback): attesa=qty PF, check OK/mismatch/sconosciuto, blocco con popup, correzione → `RECEIVED_IN_PRODUCTION`, richiesta da produzione, ritrovato pre/post conferma WH

> **Nota implementativa Sprint 4:** il popup del Caso B è indirizzato alla postazione `WH_HOST` (non esiste una postazione "preformatura" mappata); l'email arriva ai destinatari di `Sys_email_Kit_materiali`. Se servirà un mapping postazione-preformatura dedicato, basterà un flag analogo a `wh_host.json`.

### Sprint 5 — Dashboard e Reporting — **COMPLETATO il 12.06.2026**
- [x] Dashboard stato kit centralizzata — `kit_dashboard_gui.py` + `kit_dashboard_logic.py`: una riga per ordine con semaforo per fase (WH / Preformatura / Produzione derivato da `kit_status`), priorità, **sessioni riprendibili** (⏸ con fase e stato), richieste aperte e colonna Alert (stati `REOPENED`/`BLOCKED` o `VERIFY_FAIL` negli ultimi 7 giorni); menu `Materiali → Preparazione Kit → Dashboard Stato Kit` — **sola lettura, nessun login** (§8.1)
- [x] Report storico eccezioni — scheda con filtri data/ordine sugli eventi `VERIFY_FAIL`, `UNKNOWN_UNIQUE_NUMBER`, `CLOSE_DEROGATION`, `REQUEST_MATERIAL`, `MATERIAL_FOUND`, `SOURCE_FILE_CHANGED` (con nome operatore) + **export Excel** (`openpyxl`)
- [x] Analisi cause ricorrenti — conteggi **mappati sulle 5 cause della §1.1** (#2 ritrovati ← `MATERIAL_FOUND`, #3 scrap ← richieste da preformatura, #4 errore prelievo ← `VERIFY_FAIL` PF, #5 non trasferito ← `VERIFY_FAIL` produzione) + deroghe/sconosciuti/cambi file, top 15 materiali più richiesti, ordini con più eccezioni; periodo filtrabile (default 90 giorni)
- [x] Test end-to-end su dati reali (18 verifiche con rollback): percorso completo con eccezioni → dashboard (fasi G/G/R, alert, sessione sospesa), storico con filtri, analisi cause (#2–#5 valorizzate), export Excel verificato

**Il modulo Kit Preparation è completo: tutti gli sprint della roadmap sono chiusi.**

---

## 11. Note Tecniche per Implementazione

### 11.1 Stack Tecnologico

| Layer | Tecnologia |
|-------|-----------|
| Backend | Python (allineato a PlanRespect: Flask) |
| Frontend | HTML + JavaScript per le pagine web; le azioni protette passano da `_execute_authorized_action` |
| Database | SQL Server — **`Traceability_RS`** (query etichette esistente) + nuove tabelle §6 |
| Import lista | `openpyxl` su XLSX in `T:\KITTING` (PDF solo come documento umano) |
| Barcode scan | Scanner USB HID (input tastiera) |
| Notifiche popup | Estensione sistema popup materiali indiretti esistente |
| Notifiche email | SMTP / integrazione esistente (`email_alerter.py`) |

### 11.2 Scanner Barcode

- Campo input sempre in focus durante la sessione di scansione
- Accettare sia scansione che inserimento manuale
- Validazione formato `unique_number` prima della scrittura a DB: pattern osservati `HU\d{9}(_\d{2})?` e codici brevi `\d{6}` — confermare con campioni reali (§12)

### 11.3 Robustezza Sessioni

- Ogni scansione confermata è una **transazione DB autonoma**: nessuna perdita in caso di crash
- Heartbeat `last_activity_date` su `kit_sessions`; sessioni `ACTIVE` senza attività da N ore vengono proposte come `SUSPENDED`
- Doppia conferma sullo stesso `unique_number` → warning duplicato (no doppio conteggio)

### 11.4 Traduzioni

Tutte le stringhe UI e i template di notifica seguono il **sistema di traduzioni dinamiche esistente**: l'utente vede il modulo nella lingua selezionata in quel momento, come tutto il resto del programma. Vanno create tutte le chiavi di traduzione necessarie in tutte le lingue supportate.

---

## 12. Decisioni di Revisione (12.06.2026)

I punti aperti della v1.1 sono stati tutti risolti in revisione; le decisioni sono già integrate nelle sezioni indicate.

| # | Punto | Decisione | Sezione |
|---|-------|-----------|---------|
| 1 | Allocazione bobina multi-ordine | **Approvata** l'allocazione proporzionale a `OrderQuantity` × coeff. BOM, con correzione manuale | §5.1.2, §9.1 |
| 2 | Chiave autorizzazione con refuso | **Corretta** in `verifica_kit_materiale` | §2.3 |
| 3 | Login prelievo WH | **Confermato**: apertura sessione di scansione con `conferma_kit_completamento` | §5.1.3 |
| 4 | Destinatari email | Stessa logica delle altre email: `traceability_rs.dbo.settings`, `Atribute = 'Sys_email_Kit_materiali'` | §7.4 |
| 5 | Indirizzamento popup | Stesso sistema dei materiali indiretti: mapping postazioni di `wh_workstation_config.py` | §7.2 |
| 6 | Formato OrderNumber | Normalizzazione a **9 caratteri totali**: `PR` + zeri di padding + numero (`PR554` → `PR0000554`) | §5.1.1 |
| 7 | Pattern unique number | **Confermati** i pattern osservati (`HU\d{9}(_\d{2})?`, codici brevi `\d{6}`) | §11.2 |
| 8 | Escalation temporale | Reminder automatico al responsabile WH, default **10 minuti**, configurabile | §7.1 |
| 9 | Lingue UI/notifiche | Traduzioni dinamiche secondo la lingua selezionata dall'utente, come il resto del programma; creare tutte le traduzioni necessarie | §11.4 |
| 10 | Riapertura lista `REOPENED` | **Approvata** la proposta: le scansioni Preformatura restano valide, si riverificano solo i codici non conformi | §5.2.2 |

---

*Documento aggiornato il 2026-06-12 — Versione 1.2 (sostituisce 1.0 e 1.1)*
*Revisione del 12.06.2026 recepita — pronto per implementazione*
