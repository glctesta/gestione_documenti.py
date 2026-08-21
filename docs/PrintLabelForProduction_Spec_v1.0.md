# Etichette Produzione — Specifica di progettazione v1.0

> **⚠️ Documento obsoleto:** vedere `PrintLabelForProduction_Spec_v2.0.md` per la documentazione aggiornata del modulo Etichette Produzione.

> **Stato:** bozza di progetto / pre-implementazione.  
> **Scopo:** definire dove e come aggiungere in `main.py` il sotto-menu *Etichette Produzione*, le pagine web intranet sul server `192.168.10.72:5015` e il codice sorgente in `print_label_for_production/`.

---

## 1. Riepilogo della richiesta

| Elemento | Valore |
|---|---|
| Posizione menu | `Materiali` → sotto-voce di `materials_menu` a fianco della voce attuale `Etichette` (riga ~17838 di `main.py`) |
| Nuova voce | `Etichette Produzione` (cascade) |
| Sotto-voci | 1. `Gestione BOM`<br>2. `Gestione stampanti`<br>3. `Stampa` |
| Tecnologia pagine 1-2 | Browser di default → web server intranet `http://192.168.10.72:5015` |
| Tecnologia pagina 3 | Riuso del form esistente `open_printer_settings_with_login` (finestra Tk) |
| Autorizzazione voci 1-2 | `_execute_authorized_action('gestione_stampa_etichette_produzione', ...)` |
| Autorizzazione voce 3 | `_execute_simple_login(...)` |
| Codice sorgente | Nuova sotto-directory `print_label_for_production/` |

**Conferme ricevute:**
- Voce 3 *Stampa* → apre la **finestra di impostazione stampante** (`open_printer_settings_with_login`).
- La configurazione stampante viene salvata in un **file JSON locale** (`printer_config.json`); se mancante deve essere ricreato; l'utente deve poter inserire/scrivere il nome della stampante in modo che sia riconoscibile in fase di stampa.
- Strategia di accesso web tramite **token monouso** confermata.

---

## 2. Modifiche a `main.py`

### 2.1 Inserimento del sotto-menu

Dopo la riga 17841 (dopo `materials_menu.add_command(label='Etichette', ...)`), aggiungere:

```python
# Sottomenu Etichette Produzione
production_labels_menu = tk.Menu(materials_menu, tearoff=0)
materials_menu.add_cascade(
    label=self.lang.get('submenu_production_labels', 'Etichette Produzione'),
    menu=production_labels_menu
)

production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_bom', '1. Gestione BOM'),
    command=self._open_production_labels_bom_with_auth
)
production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_printers', '2. Gestione stampanti'),
    command=self._open_production_labels_printers_with_auth
)
production_labels_menu.add_command(
    label=self.lang.get('submenu_production_labels_print', '3. Stampa'),
    command=self._open_production_labels_print_with_simple_login
)
```

### 2.2 Handler da aggiungere nella classe principale

```python
def _open_production_labels_bom_with_auth(self):
    """Apre Gestione BOM sul web server (autorizzato)."""
    def _open():
        from print_label_for_production import launcher
        launcher.open_bom_page(
            self, self.db,
            self.last_authorized_user_id,
            self.last_authenticated_user_name
        )
    self._execute_authorized_action('gestione_stampa_etichette_produzione', _open)


def _open_production_labels_printers_with_auth(self):
    """Apre Gestione stampanti sul web server (autorizzato)."""
    def _open():
        from print_label_for_production import launcher
        launcher.open_printers_page(
            self, self.db,
            self.last_authorized_user_id,
            self.last_authenticated_user_name
        )
    self._execute_authorized_action('gestione_stampa_etichette_produzione', _open)


def _open_production_labels_print_with_simple_login(self):
    """Apre la finestra impostazioni stampanti (login semplice)."""
    import label_printing_gui
    self._execute_simple_login(
        action_callback=lambda user_id: label_printing_gui.open_printer_settings_window(
            self, self.db, self.lang,
            self.last_authenticated_user_name
        )
    )
```

---

## 3. Autorizzazioni e traduzioni

La chiave `gestione_stampa_etichette_produzione` deve esistere in `dbo.AppTranslations` con `MenuValue IS NOT NULL`, altrimenti `_execute_authorized_action` (e `grant_permission`) la rifiutano.

### 3.1 Script di setup proposto

File: `setup_print_label_production_auth.py` (stile `setup_kit_preparation_sprint0.py`):

```python
LANGS = ['it', 'en', 'ro', 'de', 'sv']
AUTH_KEY = (
    'gestione_stampa_etichette_produzione',
    'Etichette Produzione',
    'Etichette Produzione',
    'Production Labels',
    'Etichete Producție',
    'Produktionsetiketten',
    'Produktionsetiketter'
)

# Inserimento con MenuValue valorizzato per tutte le lingue
```

### 3.2 Traduzioni per le voci di menu (senza MenuValue)

Aggiungere in `AppTranslations` le chiavi:

- `submenu_production_labels` → `Etichette Produzione`
- `submenu_production_labels_bom` → `1. Gestione BOM`
- `submenu_production_labels_printers` → `2. Gestione stampanti`
- `submenu_production_labels_print` → `3. Stampa`

---

## 4. Strategia: pagine accessibili solo da DocumentManagement

**Problema:** le pagine web sono su intranet (`192.168.10.72:5015`). Chiunque connettendosi direttamente al browser potrebbe aprirle.

**Soluzione proposta:** token monouso a vita breve, condiviso tramite il database già usato sia da DocumentManagement che dal web server.

### 4.1 Flusso

1. L'utente clicca su *Gestione BOM* o *Gestione stampanti* in `main.py`.
2. `_execute_authorized_action` autentica l'utente e verifica il permesso `gestione_stampa_etichette_produzione`.
3. `print_label_for_production/launcher.py` genera un token UUIDv4 e lo inserisce in `Traceability_RS.ind.PrintLabelWebSessions` con:
   - `UserId`, `UserName`
   - `Permission`
   - `Page` (`bom` oppure `printers`)
   - `IssuedAt`, `ExpiresAt` (es. `GETDATE() + 5 minuti`)
   - `UsedAt = NULL`
4. Viene aperto il browser all'URL:  
   `http://192.168.10.72:5015/bom?token=<uuid>`
5. Il web server, alla prima richiesta:
   - verifica che il token esista, non scaduto e non già usato;
   - verifichi che la pagina richiesta corrisponda a `Page`;
   - segni `UsedAt = GETDATE()`;
   - crei una sessione firmata (Flask `session`) con `user_id`, `user_name`, `permission` e durata (es. 30 min).
6. Le richieste successive usano il cookie di sessione.  
   Accesso diretto a `/bom` o `/printers` **senza token e senza sessione valida** → `403 Forbidden`.

### 4.2 Vantaggi

- Non serve un segreto condiviso tra app e web server: si usa il DB.
- Il token è monouso e scade rapidamente; anche se l'URL viene copiato subito non funziona.
- Ogni azione di salvataggio sul web server conosce l'utente reale e può loggarlo nelle colonne `[User]`.

### 4.3 Tabella token

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

## 5. Struttura file proposta

```
print_label_for_production/
├── __init__.py
├── server_config.py       # Config JSON con host/porta/segreto
├── launcher.py            # Genera token e apre browser da main.py
├── db.py                  # Helper connessione DB per il web server
├── web_server.py          # Entry-point Flask (scheduled task sul .72)
├── routes_bom.py          # Route /bom e API BOM
├── routes_printers.py     # Route /printers e API stampanti
├── auth.py                # Validazione token + sessione
├── templates/
│   ├── bom.html
│   └── printers.html
└── static/
    ├── style.css
    └── app.js
```

---

## 6. Server web Flask

### 6.1 Configurazione

`server_config.py` (analogo a `kit_dashboard/server_config.py`):

```python
DEFAULT_CONFIG = {
    "server_host_ip": "192.168.10.72",
    "server_port": 5015,
    "token_ttl_minutes": 5,
    "session_lifetime_minutes": 30,
    "session_secret": None,  # generato casualmente al primo avvio se None
}
```

### 6.2 Avvio

Scheduled task su `192.168.10.72`:

```
pythonw.exe C:\<percorso>\print_label_for_production\web_server.py
```

Richiede: Python 3.11, `Flask`, `pyodbc`, `markupsafe`, driver ODBC, porta `5015` aperta in firewall, `db_config.enc` e `encryption_key.key` nella working directory.

### 6.3 Validazione token (auth.py)

```python
def validate_token(token: str, expected_page: str):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT UserId, UserName, Permission, UsedAt, ExpiresAt
               FROM Traceability_RS.ind.PrintLabelWebSessions
               WHERE Token = ?""", (token,))
        row = cur.fetchone()
        if not row:
            return None
        if row.UsedAt is not None or row.ExpiresAt < datetime.now():
            return None
        if row.Permission != 'gestione_stampa_etichette_produzione':
            return None
        cur.execute(
            "UPDATE Traceability_RS.ind.PrintLabelWebSessions SET UsedAt = GETDATE() WHERE Token = ?",
            (token,))
        return {'user_id': row.UserId, 'user_name': row.UserName, 'permission': row.Permission}
    finally:
        conn.close()
```

---

## 7. Pagina *Gestione BOM*

### 7.1 URL

`/bom?token=<uuid>`

### 7.2 Layout proposto

- **Colonna sinistra:** selezione prodotto.
  - Combo con `ProductCode — ProductName — LinkedAtLabel`.
- **Colonna destra:** due liste affiancate.
  - Lista *Labels*.
  - Lista *Ribbons*.
- **Basso:** editor dello script (textarea) + pulsante *Salva script*.
  - Abilitato solo dopo aver salvato un accoppiamento.

### 7.3 Query dati

#### Prodotti

```sql
select 
    p.idproduct,
    upper(p.productcode) as ProductCode,
    upper(p.productname) as ProductName,
    iif(isnull(m.materialeid,0) = 0, 'Not Linked At Label',
        m.CodiceMateriale + ' ' + rtrim(m.DescrizioneMateriale)) as LinkedAtLabel
from 
    traceability_rs.dbo.products p
    left join traceability_rs.ind.BomIndirectMaterials as BM on bm.IDProduct = p.IDProduct
    left join traceability_rs.ind.Materiali as M on m.MaterialeId = bm.materialeid and bm.dateout is null
    left join traceability_rs.ind.FamigliaMateriali as FM on FM.FamigliaMaterialiId = m.FamigliaMaterialiId and fm.Famiglia = 'Labels'
where charindex('CIPR', p.productcode, 1) = 0
order by upper(p.productcode);
```

#### Labels

```sql
select 
    m.materialeid,
    upper(m.CodiceMateriale) as MaterialCode,
    upper(m.DescrizioneMateriale) as MaterialDescription,
    fm.FamigliaMaterialiId
from
    traceability_rs.ind.Materiali as M
    left join traceability_rs.ind.FamigliaMateriali as FM on FM.FamigliaMaterialiId = m.FamigliaMaterialiId
where fm.Famiglia = 'Labels'
order by m.CodiceMateriale;
```

#### Ribbons

```sql
select 
    m.materialeid,
    upper(m.CodiceMateriale) as MaterialCode,
    upper(m.DescrizioneMateriale) as MaterialDescription,
    fm.FamigliaMaterialiId
from
    traceability_rs.ind.Materiali as M
    left join traceability_rs.ind.FamigliaMateriali as FM on FM.FamigliaMaterialiId = m.FamigliaMaterialiId
where fm.Famiglia = 'Ribbons'
order by m.CodiceMateriale;
```

### 7.4 Logica di salvataggio accoppiamento

`POST /api/bom/link`

Body JSON:

```json
{
  "idproduct": 123,
  "label_material_id": 456,
  "ribbon_material_id": 789
}
```

Algoritmo:

1. Verificare duplicati attivi:

```sql
SELECT MaterialeID
FROM Traceability_RS.ind.BomIndirectMaterials
WHERE IDProduct = ? AND DateOut IS NULL;
```

Se uno dei `materialeid` selezionati è già presente, restituire errore `409` con messaggio: *Accoppiamento già esistente*.

2. Chiudere tutti i materiali attivi per quel prodotto:

```sql
UPDATE Traceability_RS.ind.BomIndirectMaterials
SET DateOut = GETDATE()
WHERE IDProduct = ? AND DateOut IS NULL;
```

3. Inserire i nuovi materiali (label e ribbon) con utente loggato:

```sql
INSERT INTO Traceability_RS.ind.BomIndirectMaterials
    (IDProduct, MaterialeID, DateIn, [User])
VALUES
    (?, ?, GETDATE(), ?),
    (?, ?, GETDATE(), ?);
```

4. Restituire il nuovo `BomIndirectMaterialId` relativo alla label (servirà per lo script).

### 7.5 Editor script

`GET /api/bom/script?label_bom_id=<id>`

```sql
SELECT TOP (1) LabelScriptId, ScriptToPrint
FROM Traceability_RS.ind.LabelScripts
WHERE BomIndirectMaterialId = ? AND DateOut IS NULL
ORDER BY DateIn DESC;
```

`POST /api/bom/script`

Body JSON:

```json
{
  "bom_id": 123,
  "script": "^XA..."
}
```

Algoritmo:

1. Verificare duplicato attivo con stesso contenuto:

```sql
SELECT LabelScriptId
FROM Traceability_RS.ind.LabelScripts
WHERE BomIndirectMaterialId = ? AND DateOut IS NULL AND ScriptToPrint = ?;
```

Se esiste, restituire `409` *Script già attivo*.

2. Chiudere lo script attivo:

```sql
UPDATE Traceability_RS.ind.LabelScripts
SET DateOut = GETDATE()
WHERE BomIndirectMaterialId = ? AND DateOut IS NULL;
```

3. Inserire il nuovo script:

```sql
INSERT INTO Traceability_RS.ind.LabelScripts
    (BomIndirectMaterialId, ScriptToPrint, DateIn, [User])
VALUES
    (?, ?, GETDATE(), ?);
```

---

## 8. Pagina *Gestione stampanti*

**Nota:** non sono stati forniti dettagli di schema per la gestione centralizzata delle stampanti. Di seguito una proposta minimale, da confermare.

### 8.1 URL

`/printers?token=<uuid>`

### 8.2 Tabella proposta

```sql
CREATE TABLE Traceability_RS.ind.LabelPrinters (
    LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
    PrinterName NVARCHAR(255) NOT NULL,
    PrinterType NVARCHAR(50) NOT NULL,        -- DEFAULT / USB / NETWORK
    ConnectionString NVARCHAR(500),           -- nome USB, IP:port, o vuoto per default
    PrinterModel NVARCHAR(100),
    IsDefault BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL
);
```

### 8.3 Funzionalità

- Elenco stampanti attive (`DateOut IS NULL`).
- Form per aggiungere/modificare: nome, tipo, connessione, modello, default.
- Al salvataggio di una nuova stampante default, chiudere (`DateOut = GETDATE()`) la precedente stampante default.
- Log utente nella colonna `[User]`.

---

## 9. Voce *Stampa* (menu 3)

Come richiesto, si riusa il form esistente di impostazione stampanti (`open_printer_settings_with_login`).

```python
def _open_production_labels_print_with_simple_login(self):
    import label_printing_gui
    self._execute_simple_login(
        action_callback=lambda user_id: label_printing_gui.open_printer_settings_window(
            self, self.db, self.lang,
            self.last_authenticated_user_name
        )
    )
```

### 9.1 Persistenza su file JSON locale

Il modulo `printer_config.py` già gestisce un file JSON locale (`printer_config.json`) nella directory dell’applicazione. Vanno garantiti i seguenti comportamenti:

- **Se il file non esiste:** `PrinterConfigManager` lo crea automaticamente con la configurazione di default:
  ```json
  {
    "connection_type": "DEFAULT",
    "ip": "",
    "port": 9100,
    "usb_printer_name": "",
    "printer_model": "ZEBRA",
    "last_updated": ""
  }
  ```
- **Inserimento manuale del nome stampante:** nella modalità *USB* la finestra di settings deve permettere di **scrivere/scansionare direttamente il nome della stampante** (oltre al rilevamento automatico), così che:
  - stampanti non rilevabili o condivise in rete possano essere configurate;
  - in fase di stampa il nome salvato in `usb_printer_name` venga riconosciuto da `printer_connection_manager`.
- **Visualizzazione in fase di stampa:** nella finestra di stampa etichette (`LabelPrintWindow`) aggiungere un’etichetta che mostri la stampante configurata (es. *Stampante: Zebra-ET1*). Se il file JSON è assente o il nome stampante è vuoto, aprire automaticamente la finestra di impostazione.

### 9.2 Modifiche proposte a `printer_config.py` e alla finestra di settings

1. Aggiungere un campo testo editabile affianco al combo USB (`usb_printer_entry`), sincronizzato con il combo: quando si seleziona dal combo, il testo si aggiorna; quando si scrive, il combo passa a quel valore (se non presente, viene accettato comunque).
2. Validazione del salvataggio: se `connection_type == 'USB'` e `usb_printer_name` è vuoto, mostrare un avviso *"Inserire il nome della stampante"*.
3. Al salvataggio, `printer_config.json` viene scritto/aggiornato con il nome inserito.

### 9.3 Modifiche proposte a `LabelPrintWindow` (finestra stampa)

- Al caricamento, istanziare `PrinterConfigManager`.
- Mostrare un nuovo campo/header: *Stampante configurata: ...*.
- Se il file JSON manca o `usb_printer_name` / `ip` / default non sono validi, aprire `PrinterSettingsWindow` in modo che l’utente inserisca il nome prima di poter stampare.

---

## 10. SQL di supporto

### 10.1 Tabella sessioni web

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

### 10.2 Tabella stampanti (proposta)

```sql
CREATE TABLE Traceability_RS.ind.LabelPrinters (
    LabelPrinterId INT IDENTITY(1,1) PRIMARY KEY,
    PrinterName NVARCHAR(255) NOT NULL,
    PrinterType NVARCHAR(50) NOT NULL,
    ConnectionString NVARCHAR(500),
    PrinterModel NVARCHAR(100),
    IsDefault BIT NOT NULL DEFAULT 0,
    DateIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateOut DATETIME NULL,
    [User] NVARCHAR(255) NULL
);
```

### 10.3 Inserimento chiave autorizzazione (esempio SQL)

```sql
IF NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='gestione_stampa_etichette_produzione')
    INSERT INTO Traceability_RS.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue, MenuValue)
    VALUES ('it', 'gestione_stampa_etichette_produzione', 'Etichette Produzione', 'Etichette Produzione');
-- ripetere per en, ro, de, sv
```

---

## 11. Deployment sul server 192.168.10.72

1. Copiare il progetto (o almeno `print_label_for_production/`, `config_manager.py`, `db_config.enc`, `encryption_key.key`) sul server.
2. Creare venv:
   ```
   py -3.11 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   Aggiungere/rinforzare `Flask`, `pyodbc`, `markupsafe`.
3. Aprire porta `5015` TCP inbound sul firewall di Windows del server.
4. Creare Scheduled Task che avvia:
   ```
   .venv\Scripts\pythonw.exe C:\<path>\print_label_for_production\web_server.py
   ```
   con Working Directory = cartella contenente `db_config.enc`.
5. Verificare: `http://192.168.10.72:5015/bom` (deve restituire `403` se chiamato senza token).
6. Client DocumentManagement: nessuna installazione, richiede solo browser e connessione al DB per generare il token.

---

## 12. Note / decisioni aperte

1. **Configurazione stampante (confermato):** file JSON locale; se assente viene ricreato; l’utente deve poter scrivere il nome della stampante per riconoscerla in fase di stampa. Vedi §9.
2. **Gestione stampanti (web):** manca lo schema corrente delle stampanti. La tabella `LabelPrinters` è proposta; va confermata o adattata se esiste già un'altra tabella/configurazione.
3. **Script stampante:** si assume che `LabelScripts` abbia un vincolo di unicità su `(BomIndirectMaterialId, DateOut, ScriptToPrint)`. Se lo schema è diverso, la logica di salvataggio va adattata.
4. **Sessioni token:** la pulizia periodica di `PrintLabelWebSessions` può essere fatta con un job SQL semplice (`DELETE WHERE ExpiresAt < DATEADD(DAY, -1, GETDATE())`) o gestita nel web server.
5. **Sicurezza aggiuntiva opzionale:** legare il token anche all'IP del client (`ClientIP`) e rifiutarlo se cambia. Utile ma può creare problemi con proxy/reti aziendali; da valutare.
