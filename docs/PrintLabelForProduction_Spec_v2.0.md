# Etichette Produzione — Specifica e Manuale Operativo v2.0

> **Stato:** implementato e in uso.  
> **Scopo:** documentare il sotto-menu `Materiali → Etichette Produzione`, le pagine web intranet sul server `192.168.10.72:5015` e il codice sorgente in `print_label_for_production/`.

---

## Indice

1. [Riepilogo](#1-riepilogo)
2. [Menu in `main.py`](#2-menu-in-mainpy)
3. [Autorizzazioni e traduzioni](#3-autorizzazioni-e-traduzioni)
4. [Architettura token e sessione](#4-architettura-token-e-sessione)
5. [Struttura file](#5-struttura-file)
6. [Server web Flask](#6-server-web-flask)
7. [Pagina Gestione etichette (`/bom`)](#7-pagina-gestione-etichette-bom)
8. [Pagina Gestione stampanti (`/printers`)](#8-pagina-gestione-stampanti-printers)
9. [Pagina Stampa generica (`/print/generic`)](#9-pagina-stampa-generica-printgeneric)
10. [Pagina Stampa per ordini (`/print/orders`)](#10-pagina-stampa-per-ordini-printorders)
11. [Stampa fisica (backend)](#11-stampa-fisica-backend)
12. [Schema database](#12-schema-database)
13. [Deployment sul server](#13-deployment-sul-server)
14. [Note e problemi noti](#14-note-e-problemi-noti)

---

## 1. Riepilogo

| Elemento | Valore |
|---|---|
| Posizione menu | `Materiali` → sotto-voce cascade `Etichette Produzione` |
| Voci attuali | 1. Stampa generica<br>2. Stampa per ordini<br>3. Gestione etichette |
| Tecnologia | Browser di default → web server intranet `http://192.168.10.72:5015` |
| Autorizzazione voci 1-2 | `_execute_simple_login(...)` |
| Autorizzazione voce 3 | `_execute_authorized_action('gestione_stampa_etichette_produzione', ...)` |
| Codice sorgente | `print_label_for_production/` |

**Note rispetto alla versione precedente (v1.0):**
- La vecchia voce `3. Stampa` che apriva la finestra Tk di impostazione stampante è stata rimossa.
- Le impostazioni stampanti sono ora gestite dalla pagina web `/printers`, raggiungibile dal pulsante **Gestisci stampanti** nella pagina `/bom`.
- Sono state aggiunte le pagine `/print/generic` (stampa generica) e `/print/orders` (stampa per ordini).
- Sono state introdotte tabelle per counter, log di stampa, parametri di scarto e flag `IsTraceabilityLabel`.

---

## 2. Menu in `main.py`

Il sotto-menu è definito in `main.py` (intorno alla riga 17826) con le seguenti voci:

```python
production_labels_menu = tk.Menu(materials_menu, tearoff=0)
materials_menu.add_cascade(
    label=self.lang.get('submenu_production_labels', 'Etichette Produzione'),
    menu=production_labels_menu
)

production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_generic_print', '1. Stampa generica'),
    command=self._open_production_labels_generic_print_with_simple_login
)
production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_order_print', '2. Stampa per ordini'),
    command=self._open_production_labels_order_print_with_simple_login
)
production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_bom', '3. Gestione etichette'),
    command=self._open_production_labels_bom_with_auth
)
```

Gli handler corrispondenti caricano `print_label_for_production.launcher` e aprono le pagine web:

| Handler | Pagina | Permesso/Login |
|---|---|---|
| `_open_production_labels_generic_print_with_simple_login` | `/print/generic` | login semplice |
| `_open_production_labels_order_print_with_simple_login` | `/print/orders` | login semplice |
| `_open_production_labels_bom_with_auth` | `/bom` | `gestione_stampa_etichette_produzione` |

---

## 3. Autorizzazioni e traduzioni

### 3.1 Chiave autorizzazione

La chiave `gestione_stampa_etichette_produzione` deve esistere in `dbo.AppTranslations` con `MenuValue IS NOT NULL`, altrimenti `_execute_authorized_action` (e `grant_permission`) la rifiutano.

Traduzione italiano esempio:

```sql
INSERT INTO Traceability_RS.dbo.AppTranslations
    (LanguageCode, TranslationKey, TranslationValue, MenuValue)
VALUES
    ('it', 'gestione_stampa_etichette_produzione', 'Etichette Produzione', 'Etichette Produzione');
```

### 3.2 Chiavi traduzione menu

| Chiave | Testo italiano default |
|---|---|
| `submenu_production_labels` | `Etichette Produzione` |
| `submenu_production_labels_generic_print` | `1. Stampa generica` |
| `submenu_production_labels_order_print` | `2. Stampa per ordini` |
| `submenu_production_labels_bom` | `3. Gestione etichette` |

Le traduzioni complete sono inserite da `setup_print_label_production.py` per tutte le lingue (`it`, `en`, `ro`, `de`, `sv`).

---

## 4. Architettura token e sessione

Le pagine web sono pubblicate su intranet (`192.168.10.72:5015`). Per evitare l'accesso diretto da browser, viene usato un **token monouso a vita breve**, condiviso tramite il database già usato sia da DocumentManagement che dal web server.

### 4.1 Flusso

1. L'utente clicca su una voce del menu in `main.py`.
2. `launcher.py` genera un token UUIDv4 e lo inserisce in `Traceability_RS.ind.PrintLabelWebSessions` con:
   - `UserId`, `UserName`
   - `Permission`
   - `Page` (`print_generic`, `print_orders`, `bom`, `printers`)
   - `IssuedAt`, `ExpiresAt` (es. `GETDATE() + 5 minuti`)
   - `UsedAt = NULL`
3. Viene aperto il browser all'URL: `http://192.168.10.72:5015/<page>?token=<uuid>`.
4. Il web server, alla prima richiesta:
   - verifica che il token esista, non scaduto e non già usato;
   - verifica che la pagina richiesta corrisponda a `Page`;
   - segna `UsedAt = GETDATE()`;
   - crea una sessione Flask con `user_id`, `user_name`, `permission` e durata (es. 30 min).
5. Le richieste successive usano il cookie di sessione.  
   Accesso diretto a una pagina **senza token e senza sessione valida** → `403 Forbidden`.

### 4.2 Tabella sessioni

```sql
CREATE TABLE Traceability_RS.ind.PrintLabelWebSessions (
    Token NVARCHAR(64) NOT NULL PRIMARY KEY,
    UserId INT NOT NULL,
    UserName NVARCHAR(255) NOT NULL,
    Permission NVARCHAR(255) NOT NULL,
    Page NVARCHAR(50) NOT NULL,
    IssuedAt DATETIME NOT NULL DEFAULT GETDATE(),
    ExpiresAt DATETIME NOT NULL,
    UsedAt DATETIME NULL,
    ClientIP NVARCHAR(50) NULL
);
```

---

## 5. Struttura file

```
print_label_for_production/
├── __init__.py
├── server_config.py          # Configurazione host/porta/TTL (print_label_server_config.json)
├── launcher.py               # Genera token e apre browser da main.py
├── db.py                     # Connessione DB e helper query
├── web_server.py             # Entry-point Flask
├── auth.py                   # Validazione token + sessione Flask
├── i18n.py                   # Traduzioni UI in 5 lingue
├── label_needs.py            # Calcolo fabbisogno etichette per ordini
├── routes_bom.py             # Route /bom e API BOM
├── routes_printers.py        # Route /printers e API stampanti
├── routes_print.py           # Route /print/generic e /print/orders + API stampa
├── templates/
│   ├── bom.html
│   ├── printers.html
│   ├── print_generic.html
│   └── print_orders.html
└── static/
    ├── style.css
    └── app.js
```

---

## 6. Server web Flask

### 6.1 Configurazione

`server_config.py` carica/salva `print_label_server_config.json`:

```json
{
    "server_host_ip": "192.168.10.72",
    "server_port": 5015,
    "token_ttl_minutes": 5,
    "session_lifetime_minutes": 30,
    "session_secret": "<generato casualmente>"
}
```

### 6.2 Avvio

Scheduled task sul server `192.168.10.72`:

```
pythonw.exe C:\<percorso>\print_label_for_production\web_server.py
```

con working directory = cartella contenente `db_config.enc` e `encryption_key.key`.

Requisiti: Python 3.11, `Flask`, `pyodbc`, `markupsafe`, driver ODBC, porta `5015` aperta nel firewall, configurazione cifrata DB.

### 6.3 Endpoint di health check

`GET /health` — restituisce lo stato del server e della connessione DB.

---

## 7. Pagina Gestione etichette (`/bom`)

### 7.1 URL

`/bom?token=<uuid>`

### 7.2 Layout

La pagina è organizzata in pannelli:

1. **Produs** — selezione prodotto con filtro su codice/descrizione.
2. **Etichette asociate produsului** — lista etichette già associate al prodotto, con `QuantityPerPiece` (etichette per pezzo).
3. **Parametri scarto tehnic** — configurazione scarto per tipo etichetta (`FIXED`/`PERC`, minimo, arrotondamento, flag `IsTraceabilityLabel`).
4. **Labels / Ribbons / Stampanti** — tre liste affiancate per selezionare label, ribbon e stampante; è presente un campo di ricerca per codice/descrizione della label.
5. **Associazione** — pulsante per salvare l'associazione label ↔ ribbon e label ↔ stampante.
6. **Script imprimantă** — editor dello script di stampa (ZPL/TSPL/EPL) per l'accoppiamento BOM-label selezionato.
7. **Fabbisogno etichette** — tabella con il calcolo del fabbisogno per ordini in produzione (da `label_needs.py`).

### 7.3 Query principali

#### Prodotti

```sql
SELECT 
    p.idproduct,
    UPPER(p.productcode) AS ProductCode,
    UPPER(p.productname) AS ProductName,
    IIF(ISNULL(m.materialeid,0) = 0, 'Not Linked At Label',
        m.CodiceMateriale + ' ' + RTRIM(m.DescrizioneMateriale)) AS LinkedAtLabel
FROM 
    traceability_rs.dbo.products p
    LEFT JOIN traceability_rs.ind.BomIndirectMaterials AS BM ON bm.IDProduct = p.IDProduct
    LEFT JOIN traceability_rs.ind.Materiali AS M ON m.MaterialeId = bm.materialeid AND bm.dateout IS NULL
    LEFT JOIN traceability_rs.ind.FamigliaMateriali AS FM ON FM.FamigliaMaterialiId = m.FamigliaMaterialiId AND fm.Famiglia = 'Labels'
WHERE CHARINDEX('CIPR', p.productcode, 1) = 0
ORDER BY UPPER(p.productcode);
```

#### Labels

```sql
SELECT 
    m.materialeid,
    UPPER(m.CodiceMateriale) AS MaterialCode,
    UPPER(m.DescrizioneMateriale) AS MaterialDescription,
    fm.FamigliaMaterialiId
FROM
    traceability_rs.ind.Materiali AS M
    LEFT JOIN traceability_rs.ind.FamigliaMateriali AS FM ON FM.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE fm.Famiglia = 'Labels'
ORDER BY m.CodiceMateriale;
```

#### Ribbons

```sql
SELECT 
    m.materialeid,
    UPPER(m.CodiceMateriale) AS MaterialCode,
    UPPER(m.DescrizioneMateriale) AS MaterialDescription
FROM
    traceability_rs.ind.Materiali AS M
    LEFT JOIN traceability_rs.ind.FamigliaMateriali AS FM ON FM.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE fm.Famiglia = 'Ribbons'
ORDER BY m.CodiceMateriale;
```

### 7.4 Salvataggio associazioni

`POST /api/bom/link`

Body JSON:

```json
{
  "idproduct": 123,
  "label_material_id": 456,
  "ribbon_material_id": 789,
  "printer_id": 5
}
```

Algoritmo:
1. Chiude (`DateOut = GETDATE()`) tutti i materiali attivi per quel prodotto in `BomIndirectMaterials`.
2. Inserisce i nuovi materiali (label e ribbon) con `QuantityPerPiece = 1` (default).
3. Salva l'associazione label ↔ stampante in `LabelPrinterAssociations`.
4. Registra utente nelle colonne `[User]`.

### 7.5 Gestione etichette per prodotto

Per ogni prodotto è possibile avere **una o più etichette** (anche dello stesso tipo o tipi diversi). Per ciascuna etichetta si configura:

- `QuantityPerPiece` — quante etichette di quel tipo servono per pezzo prodotto.
- Ribbon associato (da `LinkedMaterials`).
- Stampante associata (da `LabelPrinterAssociations`).
- Script di stampa (da `LabelScripts`).
- Parametri di scarto (da `LabelTypeParameters`).

### 7.6 Parametri di scarto tecnico

Tabella `Traceability_RS.ind.LabelTypeParameters`:

| Colonna | Descrizione |
|---|---|
| `MaterialeId` | Codice etichetta (FK a `ind.Materiali`) |
| `ScartoType` | `FIXED` o `PERC` |
| `ScartoValue` | Valore fisso o percentuale di scarto |
| `ScartoMinimo` | Scarto minimo garantito |
| `Arrotondamento` | Multiplo di arrotondamento (es. 500) |
| `IsTraceabilityLabel` | `1` = etichetta di tracciabilità; non usa `LabelCounters` |

### 7.7 Editor script

`GET /api/bom/script?label_bom_id=<id>`  
`POST /api/bom/script`

Body JSON:

```json
{
  "bom_id": 123,
  "script": "^XA..."
}
```

Lo script viene salvato in `Traceability_RS.ind.LabelScripts`, collegato a una riga `BomIndirectMaterialId`. È possibile avere uno script attivo per accoppiamento; al salvataggio di uno nuovo viene chiuso (`DateOut`) il precedente.

### 7.8 Pulsante Gestisci stampanti

Dalla pagina `/bom` è possibile aprire la pagina `/printers` in una nuova tab per configurare le stampanti. Se la sessione Flask è già attiva sullo stesso browser, l'accesso è consentito; altrimenti è necessario un nuovo token dalla pagina o da `main.py`.

---

## 8. Pagina Gestione stampanti (`/printers`)

### 8.1 URL

`/printers?token=<uuid>`

### 8.2 Funzionalità

- Elenco stampanti attive (`DateOut IS NULL`) in `Traceability_RS.ind.LabelPrinters`.
- Form per aggiungere/modificare: nome, tipo (`DEFAULT`/`USB`/`NETWORK`), connessione, IP, portă, locație, modello, default.
- Al salvataggio di una nuova stampante default, la precedente default viene chiusa (`DateOut = GETDATE()`).
- Log utente nella colonna `[User]`.

### 8.3 Tabelle

```sql
CREATE TABLE Traceability_RS.ind.LabelPrinters (
    LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
    PrinterName NVARCHAR(255) NOT NULL,
    PrinterType NVARCHAR(50) NOT NULL,        -- DEFAULT / USB / NETWORK
    ConnectionString NVARCHAR(500),
    PrinterIP NVARCHAR(50),
    PrinterPort INT,
    PrinterLocation NVARCHAR(255),
    PrinterModel NVARCHAR(100),
    LastRevisionDate DATETIME NULL,
    IsDefault BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL
);
```

### 8.4 API

- `GET /api/printers` — lista stampanti.
- `POST /api/printers` — crea/modifica stampante.
- `DELETE /api/printers/<id>` — soft-delete (`DateOut = GETDATE()`).

---

## 9. Pagina Stampa generica (`/print/generic`)

### 9.1 URL

`/print/generic?token=<uuid>`

### 9.2 Dati in input

1. **Etichetta** — combo con filtro codice/descrizione.
2. **Ribbon** — ereditato dall'associazione label ↔ ribbon (read-only).
3. **Counter**:
   - numero corrente da `LabelCounters.LastCounter`;
   - prefisso alfanumerico opzionale;
   - suffisso alfanumerico opzionale;
   - incremento automatico +1 dopo ogni stampa.
4. **Stampante** — combo con le stampanti configurate; default = stampante associata all'etichetta.
5. **Quantità** — da stampare.
6. **Ordini** — opzionali (multi-select).

### 9.3 Comportamento

- Se l'etichetta ha `IsTraceabilityLabel = 1`, la sezione counter è disabilitata o nascosta.
- Al cambio etichetta si ricaricano ribbon, stampante default, script e counter.
- Al click **Stampa** il backend:
  1. genera i valori seriali (`prefisso + counter + suffisso`) per la quantità richiesta;
  2. invia lo script compilato alla stampante selezionata (socket / driver / file);
  3. incrementa e salva `LastCounter`;
  4. scrive il log in `LabelPrintLog`;
  5. opzionalmente registra l'associazione agli ordini selezionati.

### 9.4 API

- `GET /api/print/generic/data` — etichette, stampanti, associazioni label↔ribbon↔stampante, script, counter.
- `POST /api/print/generic/print` — payload: `label_id`, `printer_id`, `quantity`, `prefix`, `suffix`, `counter`, `optional_order_ids`.

---

## 10. Pagina Stampa per ordini (`/print/orders`)

### 10.1 URL

`/print/orders?token=<uuid>`

### 10.2 Dati in input

1. **Ordine** — combo con ricerca per numero ordine / prodotto.
2. Al selezionare l'ordine si caricano:
   - codice prodotto;
   - etichette associate al prodotto (da `BomIndirectMaterials`);
   - ribbon per ogni etichetta;
   - script per ogni etichetta;
   - stampante default per ogni etichetta.
3. **Quantità da stampare** per ogni etichetta — default = qta ordine × qty per pezzo + scarto tecnico.
4. **Flag "stampa tutte insieme"** vs **"stampa una per volta"**.
5. **Stampante** per ogni etichetta.

### 10.3 Comportamento

- Selezionato l'ordine, la pagina mostra le righe etichetta con ribbon, script e stampante.
- L'utente può confermare/modificare le quantità e le stampanti.
- Al click **Stampa** il backend invia gli script compilati alle stampanti selezionate e registra il log.
- **Non** è integrato con il modulo FAI; il riferimento alla scansione dell'etichetta di tracciabilità era solo un esempio di logica per risalire da un `labelcod` al numero ordine.

### 10.4 API

- `GET /api/print/orders/search?q=...` — ricerca ordini.
- `GET /api/print/orders/labels?order_id=...` — etichette, ribbon, script, stampanti per il prodotto dell'ordine.
- `POST /api/print/orders/print` — payload: `order_id`, `print_all_together`, `rows[{label_id, printer_id, quantity, script_data}]`.

### 10.5 Nome tabella ordini

La tabella degli ordini è `Traceability_RS.dbo.Orders` (come usato in `label_needs.py`).

---

## 11. Stampa fisica (backend)

### 11.1 Protocolli supportati

| Tipo stampante | Implementazione |
|---|---|
| **NETWORK** | Socket TCP all'IP e porta configurati (`PrinterIP`, `PrinterPort`); timeout 5s; retry 1 volta. |
| **USB** | Generazione di un file `.prn` e invio tramite `win32print` / `os.startfile` con il driver selezionato. |
| **FILE** | Salvataggio del file `.prn` in una cartela condivisă; loggare il percorso. |
| **DEFAULT** | Comportamento di fallback. |

Le stampanti possono essere sia in rete (IP:portă) sia USB.

### 11.2 Funzione helper

`routes_print.py` contiene una funzione helper del tipo:

```python
def send_script_to_printer(script: str, printer: dict) -> dict:
    # PrinterType in ('NETWORK', 'USB', 'FILE', 'DEFAULT')
    # NETWORK -> socket.connect(ip, port); socket.sendall(script.encode())
    # USB -> win32print o file .prn
    # FILE -> salva .prn e logga percorso
    # Ritorna {ok: bool, message: str, file_path: str?}
```

### 11.3 Log di stampa

Ogni stampa viene registrata in `Traceability_RS.ind.LabelPrintLog`.

---

## 12. Schema database

### 12.1 Tabelle principali

```sql
-- Sessioni web
CREATE TABLE Traceability_RS.ind.PrintLabelWebSessions (
    Token NVARCHAR(64) NOT NULL PRIMARY KEY,
    UserId INT NOT NULL,
    UserName NVARCHAR(255) NOT NULL,
    Permission NVARCHAR(255) NOT NULL,
    Page NVARCHAR(50) NOT NULL,
    IssuedAt DATETIME NOT NULL DEFAULT GETDATE(),
    ExpiresAt DATETIME NOT NULL,
    UsedAt DATETIME NULL,
    ClientIP NVARCHAR(50) NULL
);

-- Stampanti
CREATE TABLE Traceability_RS.ind.LabelPrinters (
    LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
    PrinterName NVARCHAR(255) NOT NULL,
    PrinterType NVARCHAR(50) NOT NULL,
    ConnectionString NVARCHAR(500),
    PrinterIP NVARCHAR(50),
    PrinterPort INT,
    PrinterLocation NVARCHAR(255),
    PrinterModel NVARCHAR(100),
    LastRevisionDate DATETIME NULL,
    IsDefault BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL
);

-- Associazione Label <-> Ribbon
CREATE TABLE Traceability_RS.dbo.LinkedMaterials (
    LinkedMaterialId INT IDENTITY(1,1) PRIMARY KEY,
    LabelId INT NOT NULL,
    RibbonId INT NOT NULL,
    dateout DATETIME NULL,
    dateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);

-- Associazione Label <-> Stampante
CREATE TABLE Traceability_RS.dbo.LabelPrinterAssociations (
    LabelPrinterAssociationId INT IDENTITY(1,1) PRIMARY KEY,
    LabelId INT NOT NULL,
    LabelPrinterId INT NOT NULL,
    dateout DATETIME NULL,
    dateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);

-- Script di stampa per BOM-label
CREATE TABLE Traceability_RS.ind.LabelScripts (
    LabelScriptId INT IDENTITY(1,1) PRIMARY KEY,
    BomIndirectMaterialId INT NOT NULL,
    ScriptToPrint NVARCHAR(MAX) NULL,
    DateOut DATETIME NULL,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    [User] NVARCHAR(255) NULL
);

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

-- Parametri di scarto per tipo etichetta
CREATE TABLE Traceability_RS.ind.LabelTypeParameters (
    LabelTypeParameterId INT IDENTITY(1,1) PRIMARY KEY,
    MaterialeId INT NOT NULL,
    ScartoType NVARCHAR(10) NOT NULL CONSTRAINT CK_LabelTypeParam_ScartoType
        CHECK (ScartoType IN ('FIXED', 'PERC')),
    ScartoValue DECIMAL(10,4) NOT NULL DEFAULT 0,
    ScartoMinimo DECIMAL(10,4) NOT NULL DEFAULT 0,
    Arrotondamento DECIMAL(10,4) NOT NULL DEFAULT 1,
    IsTraceabilityLabel BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL,
    CONSTRAINT FK_LabelTypeParameters_Materiali FOREIGN KEY (MaterialeId)
        REFERENCES Traceability_RS.ind.Materiali(MaterialeId)
);
```

### 12.2 Altre colonne coinvolte

```sql
-- Quantità etichette per pezzo nella BOM indiretta
ALTER TABLE Traceability_RS.ind.BomIndirectMaterials
    ADD QuantityPerPiece DECIMAL(10,4) NOT NULL DEFAULT 1;

-- Tracciamento righe etichetta inserite automaticamente in picking list
ALTER TABLE Traceability_RS.dbo.picking_list_items
    ADD Source NVARCHAR(20) NULL DEFAULT 'FILE',
        LabelRequestData NVARCHAR(MAX) NULL;
```

---

## 13. Deployment sul server

1. Copiare il progetto (o almeno `print_label_for_production/`, `config_manager.py`, `db_config.enc`, `encryption_key.key`) sul server `192.168.10.72`.
2. Creare venv:
   ```
   py -3.11 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   Assicurarsi che siano installati `Flask`, `pyodbc`, `markupsafe`.
3. Aprire porta `5015` TCP inbound sul firewall di Windows del server.
4. Creare Scheduled Task che avvia:
   ```
   .venv\Scripts\pythonw.exe C:\<path>\print_label_for_production\web_server.py
   ```
   con Working Directory = cartella contenente `db_config.enc`.
5. Verificare: `http://192.168.10.72:5015/health` deve rispondere; `http://192.168.10.72:5015/bom` deve restituire `403` se chiamato senza token.
6. Client DocumentManagement: nessuna installazione, richiede solo browser e connessione al DB per generare il token.

---

## 14. Note e problemi noti

1. **Pulsante “Gestisci stampanti" dalla `/bom`**: apre `/printers` in una nuova tab. Se la sessione Flask è già attiva sullo stesso dominio funziona; altrimenti la pagina richiede un nuovo token.
2. **Picking list**: le colonne `Source` e `LabelRequestData` su `dbo.picking_list_items` sono create ma non sono ancora utilizzate dal codice attuale (riservate a sviluppi futuri).
3. **`label_needs.py`**: la query di calcolo fabbisogno si appoggia a `LogApiDynamics` con endpoint `ProdFinishedGoods` e a dati warehouse; va verificata sui dati reali.
4. **Template `/print/orders.html`**: contiene testo hardcoded e alcuni mismatch nei nomi campo API (`OrderID` vs `IDOrder`, `OrderCode` vs `OrderNumber`, `Quantity` vs `OrderQuantity`). La pagina potrebbe non funzionare correttamente fino a correzione.
5. **Template `/print/generic.html`**: la chiave di traduzione `script` non è presente nella sezione italiana di `PRINT_UI`; l'etichetta del campo script risulta vuota in italiano. Inoltre il titolo del pannello settings è hardcoded `<h2>Settings</h2>`.
6. **Counter**: per le etichette con `IsTraceabilityLabel = 1` il counter non viene gestito tramite `LabelCounters`, per evitare sovrapposizioni con la numerazione di tracciabilità principale (`traceability_rs.dbo.labels.labelcod`).
7. **Stampanti**: supportate sia rete (IP:portă) sia USB. Il tipo `DEFAULT` è un fallback.
8. **Pulizia token**: i record di `PrintLabelWebSessions` scaduti possono essere rimossi con un job SQL semplice (`DELETE WHERE ExpiresAt < DATEADD(DAY, -1, GETDATE())`) o gestiti nel web server.

---

> **Documento generato per uso interno Vandewiele Romania.**  
> **Tutti i diritti riservati.**
