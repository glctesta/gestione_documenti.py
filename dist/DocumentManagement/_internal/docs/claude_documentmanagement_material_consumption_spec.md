# Specifica funzione controllo consumi materiale per `DocumentManagement`

## Contesto
Nel file `main.py`, alla riga 15726, è presente la seguente voce di menu non ancora implementata:

```python
consumption_submenu.add_command(
    label=self.lang.get('menu_consumption_reports', 'Rapporti'),
    command=self._open_material_consumption_reports
)
```

Occorre implementare la logica completa associata al comando `self._open_material_consumption_reports`, includendo:

1. controllo schedulato giornaliero dei codici prodotti in fase `PTHM`;
2. verifica presenza dei dati di consumo alloy in tabella `ProductConsumptions`;
3. invio email professionale per i codici mancanti;
4. comportamento del bottone **Rapporti** nel menu;
5. generazione report in **PDF** ed **Excel** quando i dati esistono.

## Obiettivo funzionale
Il sistema deve poter calcolare e presentare i consumi di alloy relativi ai codici prodotti il giorno precedente nella fase `PTHM` (fase `IDPhase = 107`).

Per poter eseguire il calcolo è necessario che, per ogni `IdProduct` prodotto, esista una riga attiva in `Traceability_RS.dbo.ProductConsumptions` con:

- `IdProduct = <codice prodotto>`
- `MaterialConsumption = 'Alloy'`
- `DateOut IS NULL`

Se tali dati mancano, il sistema deve:

- segnalarlo via email una sola volta al giorno secondo la logica anti-duplicazione già esistente nel progetto;
- impedire la generazione del report dal menu, mostrando un messaggio esplicito all'utente.

## Finestra temporale da usare
La verifica deve considerare il giorno produttivo precedente nel range:

- inizio: `07:30:00` del giorno precedente
- fine: `07:30:00` del giorno corrente

La schedulazione del controllo deve avvenire **una volta al giorno alle 08:05 del mattino**, riutilizzando la logica già implementata nel progetto per evitare invii multipli da PC differenti.

## Query unica richiesta
Creare **una sola query SQL** che:

- estragga i codici prodotti in fase `PTHM` nel giorno precedente;
- aggreghi le quantità processate (`IsPass = 1`);
- recuperi il nome prodotto (`Products.ProductCode`);
- verifichi la presenza del record di consumo alloy attivo in `ProductConsumptions`;
- evidenzi i codici mancanti.

### Query proposta
```sql
DECLARE @DateStart  AS SMALLDATETIME = DATEADD(DAY, -1, CAST(CAST(GETDATE() AS DATE) AS DATETIME)) + CAST('07:30:00' AS DATETIME);
DECLARE @DateFinish AS SMALLDATETIME = CAST(CAST(GETDATE() AS DATE) AS DATETIME) + CAST('07:30:00' AS DATETIME);

SELECT
    o.IDProduct,
    p.ProductCode,
    ISNULL(SUM(CASE WHEN s.IsPass = 1 THEN 1 ELSE 0 END), 0) AS QtyProcessed,
    pc.ProductConsumptionId,
    pc.MaterialConsumption,
    pc.MaterialConsumptionGR,
    CASE
        WHEN pc.ProductConsumptionId IS NULL THEN 1
        ELSE 0
    END AS MissingAlloyConsumption
FROM Traceability_RS.dbo.Scannings s
INNER JOIN Traceability_RS.dbo.OrderPhases op
    ON s.IDOrderPhase = op.IDOrderPhase
INNER JOIN Traceability_RS.dbo.Orders o
    ON op.IDOrder = o.IDOrder
INNER JOIN Traceability_RS.dbo.Phases ph
    ON op.IDPhase = ph.IDPhase
INNER JOIN Traceability_RS.dbo.Products p
    ON o.IDProduct = p.IDProduct
LEFT JOIN Traceability_RS.dbo.ProductConsumptions pc
    ON pc.IdProduct = o.IDProduct
   AND pc.MaterialConsumption = 'Alloy'
   AND pc.DateOut IS NULL
WHERE
    ph.IDPhase = 107
    AND s.ScanTimeFinish >= @DateStart
    AND s.ScanTimeFinish < @DateFinish
GROUP BY
    o.IDProduct,
    p.ProductCode,
    pc.ProductConsumptionId,
    pc.MaterialConsumption,
    pc.MaterialConsumptionGR
ORDER BY
    p.ProductCode;
```

## Regole di business

### 1. Controllo schedulato giornaliero
Implementare un controllo automatico alle **08:05** che:

1. esegue la query unica sopra;
2. filtra i record con `MissingAlloyConsumption = 1`;
3. se esistono righe mancanti, invia una email usando la logica di invio già esistente nel progetto;
4. usa la logica già presente per evitare email duplicate inviate da più computer;
5. recupera i destinatari da `Traceability_RS.dbo.Settings` usando la chiave:
   - `Sys_missing_data_alloy`

### 2. Testo funzionale dell'email
L’email deve essere in formato molto professionale, con utilizzo di `logo.png`, e spiegare chiaramente che:

- per poter calcolare i consumi di alloy è **imperativo** avere i valori di alloy per tutti i codici presenti nell’elenco;
- tali valori devono essere determinati pesando:
  - una scheda non saldata;
  - la stessa scheda immediatamente dopo il processo di saldatura Wave;
- nella mail devono comparire i codici mancanti e le quantità processate nel giorno produttivo considerato.

### 3. Comportamento del menu `Rapporti`
Quando l’utente clicca il bottone associato a:

```python
command=self._open_material_consumption_reports
```

il sistema deve:

1. eseguire la verifica dei dati necessari;
2. se **manca almeno un record** `ProductConsumptions` per `MaterialConsumption = 'Alloy'` e `DateOut IS NULL`, mostrare un messaggio bloccante all’utente.

### Messaggio suggerito all’utente
```text
Non è possibile calcolare il report dei consumi materiale perché non sono stati inseriti tutti i dati di consumo alloy necessari in anagrafica prodotto.
```

È preferibile aggiungere anche il dettaglio dei codici mancanti, se coerente con lo stile UI già presente nell’applicazione.

### 4. Generazione report se i dati esistono
Se tutti i dati richiesti sono presenti, il sistema deve generare:

- un report **PDF**;
- un report **Excel**.

Il report deve contenere, per il giorno produttivo selezionato o per il giorno precedente in caso di esecuzione automatica:

- `ProductCode`
- quantità schede processate (`QtyProcessed`)
- peso unitario della scheda per alloy, preso da `ProductConsumptions.MaterialConsumptionGR`
- totale parziale per codice
- totale complessivo del giorno

### Formula di calcolo
Per ogni codice:

```text
totale_parziale = QtyProcessed * MaterialConsumptionGR
```

Totale giorno:

```text
totale_giorno = somma(totale_parziale di tutti i codici)
```

## Struttura dati del report
Colonne minime richieste:

| Campo | Descrizione |
|---|---|
| ProductCode | Codice prodotto |
| QtyProcessed | Numero schede processate con `IsPass = 1` |
| MaterialConsumptionGR | Peso unitario alloy per scheda |
| PartialTotalGR | Totale parziale per codice |

Nel footer o nella parte finale del report inserire:

- `TotalDayGR`
- data di riferimento del report
- eventuale finestra oraria considerata (`07:30 -> 07:30`)

## Requisiti implementativi

### Metodo suggerito: scheduler
Creare o collegare una routine tipo:

```python
def _check_missing_alloy_consumption_daily(self):
    ...
```

Questa routine deve:

- essere richiamata dal sistema di scheduling già esistente nel progetto;
- usare la medesima logica anti-duplicazione mail già presente;
- usare helper già disponibili per database, log, mail e template HTML.

### Metodo menu
Implementare:

```python
def _open_material_consumption_reports(self):
    ...
```

Responsabilità del metodo:

1. recuperare i dati del giorno produttivo interessato;
2. verificare che nessun prodotto abbia `MissingAlloyConsumption = 1`;
3. in caso di mancanze, mostrare messaggio e interrompere il flusso;
4. in caso positivo, generare PDF ed Excel;
5. eventualmente aprire il PDF oppure mostrare un messaggio di conferma con i path dei file generati, seguendo lo stile già usato nel progetto.

## Pseudocodice richiesto
```python
def _open_material_consumption_reports(self):
    rows = self._get_material_consumption_rows_for_previous_day()

    missing_rows = [r for r in rows if r["MissingAlloyConsumption"] == 1]
    if missing_rows:
        self._show_warning(
            "Non è possibile calcolare il report dei consumi materiale perché non sono stati inseriti tutti i dati di consumo alloy necessari in anagrafica prodotto."
        )
        return

    report_rows = []
    total_day_gr = 0
    for r in rows:
        partial_total = (r["QtyProcessed"] or 0) * (r["MaterialConsumptionGR"] or 0)
        total_day_gr += partial_total
        report_rows.append({
            "ProductCode": r["ProductCode"],
            "QtyProcessed": r["QtyProcessed"],
            "MaterialConsumptionGR": r["MaterialConsumptionGR"],
            "PartialTotalGR": partial_total,
        })

    excel_path = self._export_material_consumption_excel(report_rows, total_day_gr)
    pdf_path = self._export_material_consumption_pdf(report_rows, total_day_gr)
    self._notify_success_report_created(pdf_path, excel_path)
```

## Pseudocodice controllo schedulato
```python
def _check_missing_alloy_consumption_daily(self):
    if not self._should_run_daily_task("missing_alloy_consumption", run_time="08:05"):
        return

    rows = self._get_material_consumption_rows_for_previous_day()
    missing_rows = [r for r in rows if r["MissingAlloyConsumption"] == 1]

    if not missing_rows:
        return

    recipients = self._get_setting_value("Sys_missing_data_alloy")
    if not recipients:
        self.log_warning("Setting Sys_missing_data_alloy non configurata")
        return

    html = self._build_missing_alloy_email_html(missing_rows)
    self._send_email_with_existing_logic(
        to=recipients,
        subject="Missing alloy consumption data for processed products",
        html_body=html,
        inline_images=["logo.png"]
    )
```

## Contenuto HTML professionale dell’email
L’HTML deve seguire il layout professionale già usato nel progetto per le notifiche sistema.

### Requisiti contenuto
- header con `logo.png`
- titolo chiaro
- introduzione formale
- spiegazione del problema
- tabella con:
  - `ProductCode`
  - `QtyProcessed`
- nota operativa su come misurare il consumo alloy
- chiusura formale

### Testo suggerito per l’email
```html
<p>Dear Team,</p>
<p>
The system detected that some products processed in the PTHM phase during the previous production day
have no active alloy consumption data configured in the product consumption master data.
</p>
<p>
In order to calculate alloy consumption correctly, it is imperative that all products in the list below
have a valid alloy consumption value configured.
</p>
<p>
The alloy consumption value must be determined by weighing one unsoldered PCB and then weighing the same PCB
immediately after the Wave soldering process. The weight difference must then be recorded in the system.
</p>
<p>The following product codes are currently missing the required data:</p>
```

## Nota importante sulla finestra temporale
Nel testo SQL fornito inizialmente erano presenti:

```sql
DECLARE @DateStart AS SMALLDATETIME = CAST(CAST(GETDATE() AS DATE) AS DATETIME) + CAST('07:30:00' AS DATETIME);
DECLARE @DateFinish AS SMALLDATETIME = CAST(CAST(GETDATE() + 1 AS DATE) AS DATETIME) + CAST('07:30:00' AS DATETIME);
```

ma, dato che il controllo deve verificare **i codici prodotti nel giorno precedente**, la finestra corretta per il job schedulato delle 08:05 deve essere:

- `GETDATE() - 1` per l’inizio;
- `GETDATE()` per la fine;

sempre con soglia `07:30:00`.

## Cosa deve fare Claude
Produrre il codice necessario integrandosi con l’architettura esistente del progetto `DocumentManagement`, riusando ove possibile:

- scheduler già presente;
- logica già implementata per evitare invii duplicati da computer diversi;
- helper email esistenti;
- stile grafico email esistente;
- helper esportazione PDF/Excel già presenti, se disponibili.

## Output richiesto a Claude
Claude deve restituire:

1. implementazione del metodo `_open_material_consumption_reports`;
2. eventuale metodo SQL helper dedicato;
3. routine schedulata giornaliera delle 08:05;
4. funzione di costruzione email HTML professionale;
5. integrazione nel flusso già esistente dell’applicazione;
6. gestione errori e logging coerente con il progetto.

## Vincoli
- Non introdurre logiche parallele se esiste già un framework interno per scheduler, email, log e lock distribuito.
- Non inviare email multiple lo stesso giorno da postazioni diverse.
- Considerare solo `MaterialConsumption = 'Alloy'`.
- Considerare solo record attivi con `DateOut IS NULL`.
- Usare `Products.ProductCode` come descrizione leggibile del codice.
- Il report va generato solo se tutti i dati richiesti sono presenti.

