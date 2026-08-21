# Piano di implementazione — Gestione integrata Etichette di Produzione

> **⚠️ Documento obsoleto:** il piano è stato realizzato. Vedere `PrintLabelForProduction_Spec_v2.0.md` per la documentazione aggiornata del modulo Etichette Produzione.

## Stato attuale (post modifiche strutturali del menu)

- Il sotto-menu `Materiali → Etichette Produzione` ha 3 voci:
  1. **Stampa generica** — login semplice → `/print/generic`
  2. **Stampa per ordini** — login semplice → `/print/orders`
  3. **Gestione etichette** — autorizzato → `/bom` (pagina BOM esistente, rinominata a livello di menu)
- La vecchia voce `Stampa Etichette` che apriva la form Tk duplicata è stata rimossa.
- Le pagine `/print/generic` e `/print/orders` esistono già come placeholder.
- La pagina `/bom` resta la fonte dati per:
  - associazioni `Prodotto → Etichetta/e → Ribbon → Stampante`
  - parametri di scarto tecnico per tipo etichetta
  - script di stampa per etichetta
  - apertura di `/printers` per la gestione delle stampanti

## Risposte alle domande aperte

1. **Counter** — deve essere **persistente** nel DB (tabella `LabelCounters`).
2. **Etichette per tracciabilità** — aggiungere un flag `IsTraceabilityLabel`. Per queste etichette il counter non viene gestito tramite `LabelCounters` (non deve generare/sovrapporsi a `traceability_rs.dbo.labels.labelcod`).
3. **Stampa fisica** — protocollo principale: **ZPL/EPL/CPCL via socket TCP** per stampanti Zebra/simili. Prevedere anche un'opzione per stampanti "esotiche" tramite driver dedicato (USB/Windows o file `.prn`).
4. **Gestione etichette (`/bom`)** — continua a mostrare la selezione prodotto, perché serve per abbinare: prodotto → etichetta → ribbon → script → stampante.
5. **Stampa per ordini** — quantità default = qta ordine + scarto tecnico. Previsto un flag per stampare tutte le etichette insieme oppure una per volta. In molti casi la stampa partirà dopo la scansione dell'etichetta di tracciabilità già registrata nel sistema di tracciabilità (vedi integrazione FAI).
6. **Intestazioni colonne** — nessuna mancante, la questione è già risolta.

## 1. Gestione etichette (`/bom`)

### Cosa mantenere
- Selezione prodotto con filtro.
- Sezione "Etichette associate al prodotto" con `Qty per pezzo`.
- Sezione "Parametri scarto tecnico".
- Sezione Labels / Ribbons / Stampanti con:
  - filtro sul codice/descrizione Labels (già presente)
  - associazione label ↔ ribbon ↔ stampante
  - salvataggio script per etichetta
  - bottone per aprire `/printers`

### Cosa aggiungere
- Flag `IsTraceabilityLabel` nella tabella `LabelTypeParameters` (o nuova tabella `LabelFlags`) per distinguere le etichette di tracciabilità.
- Campo `IsTraceabilityLabel` nella griglia di gestione parametri etichetta.

## 2. Schema dati da aggiungere

```sql
-- Counter persistente per etichetta
CREATE TABLE Traceability_RS.ind.LabelCounters (
    LabelCounterId INT IDENTITY(1,1) PRIMARY KEY,
    MaterialeId INT NOT NULL,
    Prefix NVARCHAR(50) NULL,
    Suffix NVARCHAR(50) NULL,
    LastCounter INT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL,
    CONSTRAINT FK_LabelCounters_Materiali FOREIGN KEY (MaterialeId)
        REFERENCES Traceability_RS.ind.Materiali(MaterialeId)
);

-- Log di ogni stampa
CREATE TABLE Traceability_RS.ind.LabelPrintLog (
    LabelPrintLogId INT IDENTITY(1,1) PRIMARY KEY,
    MaterialeId INT NOT NULL,
    LabelPrinterId INT NOT NULL,
    OrderId INT NULL,
    Quantity INT NOT NULL DEFAULT 1,
    CounterFrom INT NULL,
    CounterTo INT NULL,
    Prefix NVARCHAR(50) NULL,
    Suffix NVARCHAR(50) NULL,
    ScriptSnapshot NVARCHAR(MAX) NULL,
    PrintedAt DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);

-- Flag per etichette di tracciabilità
ALTER TABLE Traceability_RS.ind.LabelTypeParameters
ADD IsTraceabilityLabel BIT NOT NULL DEFAULT 0;
```

## 3. Stampa generica (`/print/generic`)

### Dati in input
1. **Etichetta** (combo con filtro codice/descrizione).
2. **Ribbon** ereditato dall'associazione label ↔ ribbon (read-only).
3. **Counter**:
   - numero corrente (da `LabelCounters.LastCounter`)
   - prefisso alfanumerico opzionale
   - suffisso alfanumerico opzionale
   - incremento automatico +1 dopo ogni stampa
4. **Stampante** (combo con le stampanti configurate; default = stampante associata all'etichetta).
5. **Quantità** da stampare.
6. **Ordini** opzionali (combo/multiselect).

### Comportamento
- Se l'etichetta ha `IsTraceabilityLabel = 1`, la sezione counter viene disabilitata o nascosta.
- Al cambio etichetta si ricaricano ribbon, stampante default, script e counter.
- Al click "Stampa" il backend:
  1. genera i valori seriali (prefisso + counter + suffisso) per la quantità richiesta
  2. invia lo script compilato alla stampante selezionata (socket / driver / file)
  3. incrementa e salva `LastCounter`
  4. scrive il log in `LabelPrintLog`
  5. opzionalmente registra l'associazione agli ordini selezionati

### API
- `GET /api/print/generic/data` — etichette, stampanti, associazioni label↔ribbon↔stampante, script, counter.
- `POST /api/print/generic/print` — payload: `label_id`, `printer_id`, `quantity`, `prefix`, `suffix`, `counter`, `optional_order_ids`.

## 4. Stampa per ordini (`/print/orders`)

### Dati in input
1. **Ordine** (combo con ricerca numero ordine / prodotto).
2. Al selezionare l'ordine si caricano:
   - codice prodotto
   - etichette associate al prodotto (da `BomIndirectMaterials`)
   - ribbon per ogni etichetta
   - script per ogni etichetta
   - stampante default per ogni etichetta
3. **Quantità da stampare** per ogni etichetta — default = qta ordine × qty per pezzo + scarto tecnico.
4. **Flag "stampa tutte insieme"** vs **"stampa una per volta"**.
5. **Stampante** per ogni etichetta.

### Comportamento base
- Selezionato l'ordine, la pagina mostra le righe etichetta con ribbon, script e stampante.
- L'utente può confermare/modificare le quantità e le stampanti.
- Al click "Stampa" il backend invia gli script compilati alle stampanti selezionate e registra il log.

> **Nota:** non viene fatta integrazione con il modulo FAI. Il riferimento alla scansione dell'etichetta di tracciabilità nel FAI è stato usato solo come esempio di logica per risalire da un `labelcod` al numero ordine; se necessario, questa logica potrà essere replicata in modo indipendente nella pagina `/print/orders` senza toccare il modulo FAI.
- Quando ci sono più etichette per prodotto, si usa più stampanti (una per etichetta) oppure si richiede all'operatore di confermare l'ordine in `/print/orders`.

### API
- `GET /api/print/orders/search?q=...` — ricerca ordini.
- `GET /api/print/orders/labels?order_id=...` — etichette, ribbon, script, stampanti per il prodotto dell'ordine.
- `POST /api/print/orders/print` — payload: `order_id`, `print_all_together`, `rows[{label_id, printer_id, quantity, script_data}]`.

## 5. Stampa fisica (backend)

### Implementazione
- **Stampante di rete (Zebra/simili)**: invio via socket TCP all'IP e porta configurati; timeout 5s; retry 1 volta.
- **Stampante USB/Windows**: generazione di un file `.prn` e invio tramite `win32print` o `os.startfile` con il driver selezionato.
- **Stampante "esotica" / driver specifico**: campo `PrinterType` esteso per identificare il driver; il backend carica il driver indicato dalla configurazione.
- **Fallback**: salvare il file `.prn` in una cartella condivisa e loggare il percorso.

### Funzione helper
```python
def send_script_to_printer(script: str, printer: dict) -> dict:
    # PrinterType in ('NETWORK', 'USB', 'FILE', 'DRIVER_XYZ')
    # Se NETWORK -> socket.connect(ip, port); socket.sendall(script.encode())
    # Se USB -> win32print o file .prn
    # Se driver esotico -> delega a funzione specifica
    # Ritorna {ok: bool, message: str, file_path: str?}
```

## 6. Tracciabilità

- Tabella `LabelPrintLog` con tutti i dati di ogni stampa.
- Permette di ricostruire quali seriali/counter sono stati stampati, per quale ordine, su quale stampante, da quale utente.

## 7. File da toccare nel prossimo passo

- `print_label_for_production/routes_print.py` — API e logica di stampa.
- `print_label_for_production/templates/print_generic.html` — form completo.
- `print_label_for_production/templates/print_orders.html` — form completo.
- `print_label_for_production/i18n.py` — nuove chiavi UI.
- `print_label_for_production/db.py` — query helper per counter, log, ordini.
- SQL: `add_label_counters_and_print_log.sql` e `add_is_traceability_label.sql`.
- `main.py` — integrazione FAI (facoltativa, secondo passo).
