# Analisi di Convenienza Economica degli Straordinari — Specifica di Valutazione

**Versione:** 1.0 (bozza per valutazione)
**Data:** 2026-06-19
**Modulo interessato:** `overtime/overtime_analysis_gui.py` (form aperta da `open_overtime_analysis_with_auth`)
**Stato:** da approvare — contiene punti da confermare (vedi §10)

---

## 1. Obiettivo

Estendere la form di analisi straordinari per **correlare la produzione realizzata al personale presente in straordinario**, producendo una *analisi di convenienza economica*:

- quantità di prodotti **finalizzati** (completati) nel periodo;
- quantità di prodotti **lavorati ma ancora in WIP** (non completati), valorizzati in base alla fase raggiunta;
- in rapporto al **numero di persone presenti** prese dalla lista degli autorizzati allo straordinario;
- espressa **in pezzi** e **in valore economico** (€), con il **costo** dello straordinario per ricavare un indice di convenienza.

Lo stesso contenuto va riportato nei **file generati** (Excel/PDF) dalla form.

---

## 2. Stato attuale della form

`OvertimeAnalysisWindow` (`overtime/overtime_analysis_gui.py`) oggi:

- filtra per **intervallo date** e tipo (`ALL`, `OVER APPROVED`, `Time approved = time presence`);
- esegue una query che restituisce, **per dipendente e per giorno**: `Name`, `OvertimeDate`, `MinSuplimentarDone` (minuti straordinario svolti), `MinExtraTimeApproved` (minuti approvati), `Notes`;
- considera "autorizzati" i dipendenti con `Functions.FunctionCode <= 60` e rapporto attivo (`employeerid = 2`, `EndWorkDate IS NULL`);
- esporta in **Excel** (`openpyxl`) e **PDF**.

> La nuova analisi **aggiunge** una sezione/scheda dedicata alla convenienza economica; la tabella per-dipendente esistente resta invariata.

---

## 3. Fonti dati

### 3.1 Persone presenti in straordinario (dalla lista autorizzati)
Derivata dalla query già esistente: dipendenti autorizzati (`FunctionCode <= 60`) con `MinSuplimentarDone > 0` nel periodo.
Metriche aggregate sul periodo:
- **N. persone distinte** in straordinario;
- **Ore straordinario svolte** = `SUM(MinSuplimentarDone)/60`;
- **Ore straordinario approvate** = `SUM(MinExtraTimeApproved)/60`.

### 3.2 Produzione (DB `Traceability_RS`)
Tabelle chiave (verificate):
- `dbo.Orders` — ordine di produzione: `OrderNumber` (es. `PR0000705`), `IDProduct`, `OrderQuantity`, `IsFinished`, `DateFirstBoardFinished`, `QtyDeclareCloseOrder`.
- `dbo.Boards` — singola scheda (PCB): `IDBoard`, `IDOrder`, `BoardFinish`, `FirstTimeFinishGood`, `BoardState`.
- `dbo.Scannings` — passaggi di fase: `IDBoard`, `IDOrderPhase`, `ScanTimeFinish`, `IsPass`.
- `dbo.OrderPhases` — fasi dell'ordine: `IDOrderPhase`, `IDPhase`, `PhasePosition`.
- `dbo.Phases` — anagrafica fasi.
- `dbo.Products` — `IDProduct`, `ProductCode`.

### 3.3 Prezzi unitari (file D365)
File Excel in **`T:\D365 data\`**. Si prende **sempre il più recente per data di modifica**, qualunque sia il nome (ignorando i file temporanei `~$*.xlsx`).
- **Foglio:** `PR Master data From D365`
- **Intestazioni alla riga 4**, dati **dalla riga 5**:
  - **Colonna A** = `Production` → numero ordine di produzione (es. `PR0000705`) → join con `Orders.OrderNumber`
  - **Colonna B** = `Item number` → codice prodotto (es. `PFVO+VOR-792`) → fallback su `Products.ProductCode`
  - **Colonna K** = `Unit Price` → prezzo unitario (€)
- Note: alcuni prezzi risultano **0** → vedi gestione in §10 (prezzi mancanti).

---

## 4. Mappatura fasi (CONFERMATA)

| Bucket valorizzazione | Fasi (`IDPhase`) | Nome |
|---|---|---|
| Fino ad **AOI/SMT** | `1` (SMT), `2` (AOI) | SMT, AOI |
| Fino a **PTHM** | `4` (PTHM) | PTHM |
| Dopo i **Test** | `102` (ICT), `103` (FCT) | ICT, FCT |

> **Nota:** Touch-Up = `107` è una fase **successiva** a PTHM; come indicato, **non** viene usata come riferimento: per il WIP teniamo **PTHM = 4**.
> Il vecchio commento `IDPhase=107 = PTHM` presente in `material_consumption_report_gui.py` è errato (107 = TOUCH-UP) ma non impatta questa analisi.

---

## 5. Modello di valorizzazione

### 5.1 Prodotto finalizzato
**Definizione (recepita):** una scheda è *finalizzata* quando ha **superato la fase finale** del proprio ordine, cioè la fase con la **massima `PhasePosition`** nelle `OrderPhases` dell'ordine, con `IsPass = 1`.
Questo gestisce automaticamente i diversi instradamenti per prodotto (chi termina in PALETIZARE, chi in PACKING, chi in OUTGOING, ecc.) senza fissare un `IDPhase` specifico.
Valore pieno: **100% × prezzo unitario**.

### 5.2 WIP (lavorato ma non completato)
Percentuale del prezzo unitario in base alla **fase più avanzata superata** (`IsPass = 1`):

| Condizione (fase superata) | % valore |
|---|---|
| Ha superato **ICT (102)** o **FCT (103)** | **90%** |
| altrimenti ha superato **PTHM (4)** | **60%** |
| altrimenti ha superato **SMT (1)** o **AOI (2)** | **30%** |
| nessuna delle precedenti | 0% (non valorizzato come WIP) |

La % più alta raggiunta prevale. Valore WIP scheda = `% × prezzo_unitario_prodotto`.

---

## 6. Metriche di convenienza economica (output)

Aggregate sul periodo selezionato:

**Quantità (pezzi)**
- Pezzi finalizzati
- Pezzi in WIP (conteggio schede) e **pezzi-equivalenti** WIP (somma delle percentuali, es. 10 schede al 60% = 6 pezzi-equivalenti)

**Valore (€)**
- Valore finalizzato = Σ (pezzi finalizzati × prezzo)
- Valore WIP = Σ (% fase × prezzo)
- **Valore prodotto totale** = finalizzato + WIP

**Personale straordinario**
- N. persone presenti, ore svolte, ore approvate

**Costi (€)** — modello recepito (vedi §7.3)
- Costo straordinario = Σ, per ogni record di straordinario, `ore × tariffa_oraria`
  - feriale: `Daily_Cost × 1,5`
  - weekend (sab/dom): `WeekEndCost` (invariato)

**Indici di convenienza**
- Valore prodotto / persona in straordinario
- Valore prodotto / ora di straordinario
- **Margine** = Valore prodotto − Costo straordinario
- **Indice convenienza** = Valore prodotto / Costo straordinario (>1 = conveniente)

> Granularità proposta: riepilogo complessivo + dettaglio **per giorno** (e opzionalmente per ordine/prodotto), così da affiancare le ore di straordinario del giorno al valore prodotto dello stesso giorno.

---

## 7. Query proposte (produzione)

> Le seguenti sono **bozze** da confermare insieme alla definizione di "finalizzato" (§10).
> `@dateStart` / `@dateStop` = stesso intervallo della form.

### 7.1 Schede finalizzate nel periodo — ultima fase superata (bozza)
"Finalizzata" = la scheda ha un passaggio con `IsPass=1` sulla fase con **massima `PhasePosition`** dell'ordine.
```sql
WITH LastPhase AS (   -- fase finale (max position) per ogni ordine
    SELECT op.IDOrder, op.IDOrderPhase, op.IDPhase,
           ROW_NUMBER() OVER (PARTITION BY op.IDOrder ORDER BY op.PhasePosition DESC) AS rn
    FROM dbo.OrderPhases op
)
SELECT o.OrderNumber, o.IDProduct, p.ProductCode,
       COUNT(DISTINCT s.IDBoard) AS PezziFinalizzati
FROM LastPhase lp
JOIN dbo.Scannings s ON s.IDOrderPhase = lp.IDOrderPhase AND s.IsPass = 1
JOIN dbo.Orders    o ON o.IDOrder    = lp.IDOrder
JOIN dbo.Products  p ON p.IDProduct  = o.IDProduct
WHERE lp.rn = 1
  AND CAST(s.ScanTimeFinish AS DATE) BETWEEN @dateStart AND @dateStop
GROUP BY o.OrderNumber, o.IDProduct, p.ProductCode;
```
> Nella query §7.2 (WIP), una scheda è "non finalizzata" se **non** compare tra quelle finalizzate (nessun `IsPass=1` sull'ultima fase dell'ordine).

### 7.2 Schede in WIP con fase più avanzata (bozza)
```sql
WITH BoardPhase AS (
    SELECT b.IDBoard, o.OrderNumber, o.IDProduct,
           MAX(CASE WHEN op.IDPhase IN (102,103) AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassTest,
           MAX(CASE WHEN op.IDPhase = 4          AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassPTHM,
           MAX(CASE WHEN op.IDPhase IN (1,2)     AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassSMTAOI
    FROM dbo.Boards b
    JOIN dbo.Orders     o  ON o.IDOrder = b.IDOrder
    JOIN dbo.Scannings  s  ON s.IDBoard = b.IDBoard
    JOIN dbo.OrderPhases op ON op.IDOrderPhase = s.IDOrderPhase
    WHERE b.FirstTimeFinishGood IS NULL          -- non finalizzata — DA CONFERMARE
      AND s.ScanTimeFinish BETWEEN @dateStart AND @dateStop
    GROUP BY b.IDBoard, o.OrderNumber, o.IDProduct
)
SELECT OrderNumber, IDProduct,
       CASE WHEN PassTest=1 THEN 0.90
            WHEN PassPTHM=1 THEN 0.60
            WHEN PassSMTAOI=1 THEN 0.30
            ELSE 0 END AS WipPct
FROM BoardPhase
WHERE PassTest=1 OR PassPTHM=1 OR PassSMTAOI=1;
```

Il prezzo unitario per `OrderNumber`/`ProductCode` viene poi applicato lato Python dai dati del file D365.

### 7.3 Costo orario straordinario (recepito)
Valori da `ResetServices.dbo.OverTimeDefaults` / `OverTimeDescriptions` (verificati): `Daily_Cost = 15 €`, `WeekEndCost = 30 €` (EUR).
```sql
SELECT o.Description, d.ValueITem, v.[desc] AS Currency
FROM [ResetServices].[dbo].[OverTimeDefaults] d
JOIN [ResetServices].[dbo].[OverTimeDescriptions] o ON d.DescriptionId = o.DescpriptionId
JOIN [ResetServices].[dbo].[TbValute] v            ON d.CurrencyId    = v.IdValuta;
```
**Regole tariffa oraria:**
- `Daily_Cost` = costo orario reale di base.
- **Straordinario feriale (lun–ven):** `Daily_Cost × 1,5` → 15 × 1,5 = **22,5 €/h**.
- **Weekend (sab–dom):** `WeekEndCost` → **30 €/h**, **già** pari al doppio del giornaliero, quindi **non** si applica il +50%.

Determinazione feriale/weekend dal giorno di `OvertimeDate` di ciascun record.
`Costo straordinario = Σ (ore_record × tariffa_record)`.

---

## 8. Lettura del file D365 (lato Python)

```python
import os, glob
import pandas as pd

D365_DIR = r"T:\D365 data"

def latest_d365_file():
    files = [f for f in glob.glob(os.path.join(D365_DIR, "*.xlsx"))
             if not os.path.basename(f).startswith("~$")]
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def load_prices():
    path = latest_d365_file()
    df = pd.read_excel(path, sheet_name="PR Master data From D365",
                       header=3, usecols="A,B,K")      # header su riga 4
    df.columns = ["OrderNumber", "ProductCode", "UnitPrice"]
    by_order   = dict(zip(df["OrderNumber"], df["UnitPrice"]))
    by_product = dict(zip(df["ProductCode"], df["UnitPrice"]))
    return by_order, by_product, path
```
Lookup prezzo: prima per `OrderNumber` (col A), fallback per `ProductCode` (col B).

---

## 9. Modifiche alla UI e ai file generati

### 9.1 Form
- Nuova area/scheda **"Convenienza Economica"** sotto i filtri esistenti, con i KPI di §6 (riquadri di riepilogo) e una tabella di dettaglio per giorno (e/o per ordine).
- Indicazione del **file D365 usato** (nome + data) e avviso se non trovato/illeggibile.

### 9.2 Export Excel
- Nuovo foglio **"Convenienza Economica"**: riepilogo KPI + dettaglio; evidenziazione `Indice convenienza` (verde ≥ 1, rosso < 1).

### 9.3 Export PDF
- Nuova sezione con tabella KPI di riepilogo.

---

## 10. Decisioni recepite e punti minori

**Recepite:**
1. ✅ **"Prodotto finalizzato"** = scheda che ha **superato la fase finale** dell'ordine (max `PhasePosition`, `IsPass=1`). Conteggio a livello **scheda**. (§5.1, §7.1)
2. ✅ **Costo orario** = da `OverTimeDefaults`: feriale `Daily_Cost ×1,5` (22,5 €/h), weekend `WeekEndCost` (30 €/h, invariato). (§7.3)

**Punti minori da decidere in fase di implementazione (con default proposto):**
- **Prezzi mancanti/0 nel file D365** → *default:* valorizzare a 0 ed elencare in coda gli ordini/prodotti senza prezzo (segnalazione), senza bloccare il report.
- **Periodo del WIP** → *default:* schede con attività (scansioni) nel periodo selezionato (come §7.2).
- **Correlazione temporale** → *default:* riepilogo di periodo **+** dettaglio **per giorno** (affianca ore straordinario e valore prodotto dello stesso giorno).
- **Righe non-ordine nel tab D365** → scartare righe con `OrderNumber` vuoto / non in formato `PR…`.

---

## 11. Cosa ho già verificato

- ✅ Fasi reali e mappatura buckets (SMT=1, AOI=2, PTHM=4, ICT=102, FCT=103).
- ✅ Tabelle produzione (`Orders`, `Boards`, `Scannings`, `OrderPhases`) e relativi campi.
- ✅ File D365 accessibile da `T:\D365 data`, foglio `PR Master data From D365`, header riga 4, colonne A/B/K con prezzi reali.
- ✅ `pandas` e `openpyxl` disponibili.
- ✅ Modello costo straordinario verificato su `OverTimeDefaults` (Daily_Cost 15 €, WeekEndCost 30 €).
- ✅ Definizione di "finalizzato" e costo orario **recepiti** (§10): nessun blocco residuo per l'implementazione.

---

## 12. Stima di massima

| Attività | Stima |
|---|---|
| Lettura prezzi D365 + cache più-recente | 0,5 g |
| Query finalizzati + WIP (dopo conferma §10) | 1 g |
| Calcolo KPI convenienza + correlazione overtime | 1 g |
| UI form (sezione KPI + dettaglio) | 1 g |
| Export Excel/PDF | 0,5–1 g |
| Test su dati reali | 0,5 g |

---

*Prossimo passo:* decisioni chiave recepite (§10). Si può procedere con l'implementazione; i punti minori usano i default proposti salvo diversa indicazione.
