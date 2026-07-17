# Analisi — Ordini finiti a magazzino nella lista spedizioni

**Stato:** proposta di progetto, nessuna modifica ancora effettuata.
**Form interessata:** `_orders_reports_placeholder` in `main.py` → `orders/orders_reports_window.py`, classe `DynamicShippingWindow` (menu *Ordini → Urgenze*).

---

## 1. Obiettivo

La lista superiore della form mostra **solo** gli ordini che i planner hanno già
abbinato manualmente (sales order ↔ production order). Vogliamo aggiungere alla
stessa lista, **senza duplicare**, tutti gli ordini che **hanno finito la
produzione e sono stati caricati a magazzino ma non ancora spediti**, presi dalla
query su `LogApiDynamics` + `WarehouseFinish.dbo.Packing` fornita dal committente.

Questi ordini **non hanno un sales order collegato**. **L'abbinamento è manuale**:
lo fa l'addetto alla spedizione **prima di spedire** — non è automatizzabile,
perché l'unico dato in comune con i sales order è il **codice prodotto**. Si usa la
stessa logica dei planner (candidati per prodotto + logica di quantità residua).
La destinazione (spedizione diretta al cliente finale / spedizione normale) e la
logica di email/salvataggio devono restare coerenti con il flusso esistente.

Inoltre: un ordine **già introdotto come urgente** (con una `DynamicShippingRules`)
la cui merce **risulta effettivamente versata a magazzino** — anche con quantità
diversa da quella richiesta — deve comparire **colorato di rosso**, come segnale
"pronto da spedire" (vedi §4bis).

---

## 2. Come funziona oggi (flusso completo)

### 2.1 Tabelle in gioco (schema reale, verificato sul DB)

| Tabella | Ruolo | Colonne chiave |
|---|---|---|
| `dyn.DynamicSaleOrders` | Sales order (import **solo da Excel**) | `DynamicSaleOrderId` PK, `SONumber`, `CustomerName`, `ItemCode`, `ItemName`, `ShipDateRequest`, `QtyOrder`, `QtyToShip`, `QtyStock`, `UnitPrice` |
| `dyn.DynamicProductionOrders` | Abbinamento SO↔PO (creato dai planner) | `DynamicProductionOrderID` PK, `DynamicSaleOrderId`, `IdOrder`, `Qty`, `DateIn` |
| `dyn.DynamicShippingRules` | Richiesta di spedizione (qtà + data + destinazione) | `DybamicShippingRuleId` PK *(refuso, load-bearing)*, `DynamicProductionOrderID`, `QtyToShip`, `DateToship`, `ShipTo`, `AddBayUser`, `DateOut`, `DateSys`, + colonne legacy inutilizzate `Done`/`ConfirmedQty`/`ConfirmedAt`/`ConfirmedByUser` |
| `dyn.Shipments` | Testata spedizione confermata (v2) | `ShipmentId` PK, `ShipmentDate`, `Status` (OPEN/CLOSED/CORRECTED), `ClosedByUser`, `ClosedAt`, `PdfPalletPath`, `PdfSummaryPath` |
| `dyn.ShipmentPallets` | Righe spedizione = **quantità realmente spedita** | `ShipmentPalletId` PK, `ShipmentId`, `PalletCode`, `DynamicProductionOrderID`, `ConfirmedQty`, `ConfirmedByUser`, `ConfirmedAt`, snapshot `ProductionOrderNumber/SONumber/CustomerName/ItemCode/ItemName/ShipTo` |
| `dbo.orders` / `dbo.Products` | Production order e prodotto | `IDOrder`, `OrderNumber` (PO = `LEFT(OrderNumber,2)='PR'`), `OrderQuantity`, `IDProduct` → `ProductCode`, `ProductName` |

### 2.2 Lista superiore (ordini da spedire)

`_load_order_data_with_filters` esegue una CTE che parte da
`dyn.DynamicSaleOrders` **INNER JOIN** `dyn.DynamicProductionOrders` **INNER JOIN**
`dbo.orders`. Conseguenza diretta: **compaiono solo gli ordini già abbinati da un
planner**. Un ordine finito a magazzino ma senza abbinamento oggi non appare da
nessuna parte in questa form.

Le colonne per fase (`Associate`, `SMT`, `PTHM`, `ICT`, `FCT`, `Coating`,
`OutOfBox`…) arrivano da `dbo.QuantitaProdottaPerFase(IDOrder, faseId)`. Il
"Rimanente" è `QtyOrder - ISNULL(OutOfBox,0)`.

### 2.3 Regola di spedizione + destinazione

Selezionando un ordine, la lista inferiore mostra le `DynamicShippingRules`.
`ShippingRuleDialog` permette di inserire **quantità, data/ora, e destinazione**
(`ShipTo`, combo a due valori: `Normal Shipment` / `Direct to final Customer`).
**La destinazione vive già in questa form**, in `DynamicShippingRules.ShipTo` —
non esiste una form separata di "ordini urgenti": è questa.

### 2.4 Abbinamento dei planner (la "stessa logica" da riusare)

In `orders/match_production_orders_window.py` + `orders_manager.py`:

- L'unico INSERT è su `dyn.DynamicProductionOrders (DynamicSaleOrderId, IdOrder,
  Qty, DateIn)`.
- **Non esiste alcun vincolo DB "stesso prodotto".** Il legame è solo un filtro
  UI: la combo dei PO candidati è popolata con
  `p.ProductCode LIKE :ItemCode + '%'` (prefisso, non uguaglianza).
- Gli unici controlli forti all'inserimento sono sulle quantità: `qty ≤ residuo SO`
  e `qty ≤ residuo PO` (dove residuo PO = `OrderQuantity − SUM(Qty già abbinata)`).

### 2.5 Conferma spedizione, email, salvataggio (v2)

`orders/shipment_confirmation_window.py`:

- Lo stato **"già spedito" NON è un flag su `DynamicShippingRules`**. È calcolato:
  una `DynamicShippingRules` è una *domanda*; è coperta dall'esistenza di righe
  `dyn.ShipmentPallets` collegate (via `DynamicProductionOrderID`) la cui
  `ConfirmedQty` somma a copertura.
  ```
  Residuo(PO) = SUM(DynamicShippingRules.QtyToShip) − ISNULL(SUM(ShipmentPallets.ConfirmedQty), 0)
  ```
  L'ordine sparisce dalle liste "da spedire" quando Residuo ≤ 0.
- Confermando: si apre/riusa una `dyn.Shipments` (Status OPEN), si aggiungono righe
  `dyn.ShipmentPallets` (qtà per pallet × PO), poi *Finalize* porta la testata a
  `Status='CLOSED'` con `ClosedByUser/ClosedAt`. `ShipmentDate` è la data di
  spedizione.
- **Email** (`_send_shipment_email`, thread in background): TO =
  `Sys_shipment_email` (settings) + account manager per cliente finale; CC =
  `Sys_email_<FinalClientName>`; toggle per cliente in `dbo.ClientShipmentEmailPrefs`.
  Allega i due PDF (`shipment_pdf.generate_shipment_documents`). Corpo: numero
  spedizione, data, operatore, tabella Pallet/Ordine/Codice/Prodotto/Qtà. *Nota:
  il corpo email e i PDF **non** riportano oggi il `ShipTo` direct/normal.*
- **Monitor** (`orders/shipment_monitor.py`): polling ogni 15 s sulle regole con
  residuo > 0; **popup** (3 beep), nessuna email; attivo solo sui PC marcati come
  workstation spedizioni (`shipment_host.json`).

---

## 3. La nuova sorgente: ordini finiti a magazzino

La query fornita restituisce, per un intervallo `@from..@to`, gli ordini caricati
a magazzino: `IDOrder`, `ProductCode`, `OrderNumber`, `WarehouseInsertBox` (data),
`WarehouseTotQtyBox` (qtà). Verificato sul DB: **`LogApiDynamics` e
`WarehouseFinish.dbo.Packing` esistono**, e nessun modulo del repo le usa oggi.

Non hanno `SONumber` né `DynamicProductionOrderID`.

---

## 4. Anti-duplicazione e riconciliazione (misurate sui dati reali)

La finestra effettiva è `MAX(data_inizio_spedizioni, @from) .. @to`. Ciò che è
versato a magazzino **prima del floor** non conta (assunto già spedito).

**Regola (decisa):** per **ogni** ordine a magazzino si inietta la **quota residua
non abbinata**, riconciliando col magazzino sulla chiave **ordine di produzione
(`IDOrder`) + codice prodotto (`ProductCode`)**. `IDOrder` è deterministico (un
ordine → un solo prodotto: verificato, 0 eccezioni), quindi la coppia coincide con
`IDOrder`. Per ogni `IDOrder`, **entro la finestra** `MAX(data_inizio_spedizioni, @from) .. @to`:
```
QtaResidua = DisponibileMagazzino(IDOrder)         -- versato a magazzino nella finestra
           − SUM(DynamicProductionOrders.Qty)      -- già abbinato dai planner (all-time)
           − QtàGiàSpedita(IDOrder)                 -- ShipmentPallets, spedito nella finestra
```
- Ordine **non abbinato**: residua = disponibile → riga "da abbinare" intera (gialla).
- Ordine **parzialmente abbinato** con magazzino > abbinato: riga planner esistente
  **più** riga "da abbinare" per il residuo.
- Ordine **completamente abbinato** (residua ≤ 0): **nessuna iniezione** — resta solo
  la riga planner esistente (rossa se a magazzino, §4bis). Il residuo negativo
  significa "già interamente reclamato dai planner".

**Numeri reali (oggi, floor `data_inizio_spedizioni = 2026-07-15`):** 24 IDOrder a
magazzino nella finestra → **19 da iniettare** (residua > 0, non abbinati) + **4
urgenti già abbinati** (residua ≤ 0 → non iniettati, solo rossi). I numeri crescono
via via che il magazzino accumula versamenti dopo il floor. *(Con floor più basso i
volumi salgono: su 01/06→17/07 sarebbero 255 nuovi — dipende dal valore del floor.)*

---

## 4bis. Colorazione ROSSO — urgente già a magazzino

Un ordine **urgente** (che ha almeno una `DynamicShippingRules`) la cui merce è
**effettivamente a magazzino** (compare nella query magazzino) va evidenziato in
**rosso** nella lista, *anche se la quantità a magazzino è diversa da quella
richiesta*. È il segnale "la merce c'è, si può spedire".

**Riconciliazione (requisito committente):** gli ordini urgenti dei planner devono
**combinarsi** con i dati versati a magazzino sulla chiave **ordine di produzione +
codice prodotto**. Il confronto è **per `IDOrder`, non per quantità** (la merce a
magazzino può essere maggiore o minore della richiesta):
```sql
-- riga rossa se: esiste una shipping rule per l'ordine  AND  l'ordine è a magazzino
EXISTS (SELECT 1 FROM dyn.DynamicShippingRules r
        JOIN dyn.DynamicProductionOrders po ON po.DynamicProductionOrderID = r.DynamicProductionOrderID
        WHERE po.IdOrder = <IDOrder>)
AND <IDOrder> ∈ (ordini della query magazzino nel periodo)
```
Riguarda le righe **già presenti** in lista (urgenti abbinati), non gli iniettati.
Le righe **iniettate "da abbinare"** (SO vuoto) hanno invece colore **giallo**,
distinto dal rosso.

---

## 5. Abbinamento manuale dell'addetto — chiave prodotto

L'abbinamento **non è automatico**: lo fa l'addetto **prima di spedire**, come i
planner. L'unico dato in comune tra ordine di magazzino e sales order è il codice
prodotto. Verifica sui 256 ordini nuovi:

| Criterio | Ordini con ≥1 SO candidato |
|---|---|
| `ItemCode = ProductCode` (uguaglianza) | **0 su 256** |
| `ProductCode` **senza suffisso `\|N`** = `ItemCode` | **202 su 256** |
| Nessun SO con quel prodotto | **54 su 256 (21%)** |

**Chiave di abbinamento accertata:** l'`ItemCode` del sales order corrisponde al
`ProductCode` **privato del suffisso `|N`** (versione/revisione). Esempio reale:
`ProductCode = 'SLSV+CPU-3MOT-E_C|1'` → `'SLSV+CPU-3MOT-E_C'` = `ItemCode`.
```sql
LEFT(ProductCode, CHARINDEX('|', ProductCode + '|') - 1) = ItemCode
```
È più preciso del `LIKE ItemCode%` della UI planner (che darebbe falsi positivi su
codici più lunghi) e sui dati reali produce lo stesso insieme (202). Sui candidati
si applica poi la **logica di quantità dei planner**: SO con residuo
`QtyOrder − SUM(Qty già abbinata) > 0`, e la qtà abbinata non supera né il residuo
del SO né la disponibilità a magazzino.

**Il 21% senza SO** (54/256): questi prodotti **non hanno oggi alcun sales order in
`dyn.DynamicSaleOrders`**. Poiché i SO entrano solo via import Excel, diventano
abbinabili appena il SO di quel prodotto viene importato. Fino ad allora la cella SO
resta vuota e la riga **non è spedibile** — l'addetto non può scegliere un SO che non
esiste. Non serve un percorso "senza SO": si abbina appena il SO compare.

---

## 6. Interazione sulle righe di magazzino (abbinamento + destinazione inline)

Modello confermato dal committente: l'addetto alla spedizione lavora **direttamente
sulla riga dell'ordine di magazzino**, prima di spedire.

- **Colonna Sales Order**: sulle righe iniettate è **vuota ma editabile**. Cliccandola
  si apre il picker dei SO **candidati per lo stesso prodotto** (`ProductCode` senza
  `|N` = `ItemCode`) con **residuo > 0**, tenendo conto delle quantità (come i planner).
  Scegliendo un SO si crea l'abbinamento (`dyn.DynamicProductionOrders`) esattamente
  come fa oggi il planner.
- **Colonna Destinazione (`ShipTo`)**: l'addetto può **impostare, modificare o
  confermare** direttamente sulla riga se è `Direct to final Customer` o
  `Normal Shipment` — anche per una segnalazione già esistente.
- Completati SO + destinazione, la riga prosegue nel flusso esistente
  (`ShippingRuleDialog` → conferma v2 → email/PDF), senza nuove form.

Non serve una form separata di "ordini urgenti": abbinamento e destinazione si fanno
in linea, sulla stessa lista.

---

## 7. Date e quantità già spedite

**Requisito:** se l'utente sceglie un intervallo diverso da oggi, le quantità già
spedite non devono risultare disponibili. Poiché non c'è storico dedicato, si usa
come data di partenza la setting **`data_inizio_spedizioni`** in
`traceability_rs.dbo.Settings` (verificato: **esiste, valore `2026-07-15`**).

**Formula di disponibilità per un ordine di magazzino:**
```
Disponibile(IDOrder) =
      WarehouseTotQty(IDOrder, da = MAX(data_inizio_spedizioni, @from) .. @to)
    − Abbinato(IDOrder)              -- SUM(DynamicProductionOrders.Qty)
    − QtàGiàSpedita(IDOrder)         -- ShipmentPallets nella finestra
    − CorrezioneManuale(IDOrder)     -- ledger di allineamento (sotto)
```
`QtàGiàSpedita` dalle spedizioni v2:
```sql
SUM(sp.ConfirmedQty)
FROM dyn.ShipmentPallets sp
JOIN dyn.DynamicProductionOrders dpo ON dpo.DynamicProductionOrderID = sp.DynamicProductionOrderID
JOIN dyn.Shipments s ON s.ShipmentId = sp.ShipmentId
WHERE dpo.IdOrder = @IDOrder AND s.ShipmentDate >= <data_inizio_spedizioni>
```
Interpretazione: `data_inizio_spedizioni` è il "punto zero". Tutto ciò che è a
magazzino da quella data conta come potenzialmente disponibile; lo spedito v2 da
quella data si sottrae. Prima di quella data si assume tutto già gestito.

### 7bis. Correzione manuale "già spedito" (allineamento transitorio)

Il floor per data è grossolano: merce versata **dopo** il floor ma già spedita
fuori dal sistema (durante la transizione) resterebbe erroneamente disponibile.
Finché non tutte le spedizioni passano dal sistema, l'operatore deve poter
**dichiarare quanto di un ordine è già stato spedito**, per allineare i dati.

**Meccanismo:** nuovo ledger `dyn.WarehouseShippedAdjustments`, append-only con
audit, sottratto nella formula (`CorrezioneManuale` sopra):

| Colonna | Tipo | Note |
|---|---|---|
| `AdjustmentId` | INT IDENTITY PK | |
| `IDOrder` | INT NOT NULL | ordine di produzione (`dbo.Orders`) |
| `ProductCode` | NVARCHAR(100) | snapshot per audit |
| `Qty` | INT NOT NULL | quantità dichiarata già spedita fuori sistema |
| `Note` | NVARCHAR(400) | motivo/riferimento |
| `AdjustedByUser` | NVARCHAR(200) NOT NULL | chi |
| `AdjustedAt` | DATETIME NOT NULL DEFAULT GETDATE() | quando |

`CorrezioneManuale(IDOrder) = ISNULL(SUM(Qty), 0)` per quell'ordine. Sulla riga,
l'operatore apre "Già spedito", inserisce la quantità (≤ disponibile) e una nota;
la quota esce dalla disponibilità. È append-only: più correzioni si sommano, con
traccia completa. Non tocca il floor né i dati esistenti — è puramente additivo e
transitorio (si smette di usarlo quando tutte le spedizioni passano dal sistema).

> Nota: finché un ordine di magazzino non è abbinato non ha `DynamicProductionOrderID`,
> quindi non ha `ShipmentPallets` e `QtàGiàSpedita = 0`: appare interamente
> disponibile. Diventa scalabile solo dopo il primo abbinamento+spedizione. È
> coerente col fatto che senza abbinamento non può esserci spedizione tracciata.

---

## 8. Impatto su email e salvataggio

Se gli ordini iniettati passano per l'abbinamento e poi per il `ShippingRuleDialog`
e la conferma v2 esistenti, **email e salvataggio non richiedono modifiche**: la
spedizione finisce in `dyn.Shipments`/`dyn.ShipmentPallets`, l'email parte con
`Sys_shipment_email` + account manager, i PDF si generano come oggi.

Punti di attenzione:
- **Modifica decisa:** l'email di conferma oggi **non riporta il `ShipTo`**. Va
  aggiunta la destinazione **direct/normal nel corpo email** (colonna/nota per riga,
  in `_send_shipment_email` / `_collect_pallets_for_email`). Il dato è già in
  `ShipmentPallets.ShipTo`, va solo reso nel template HTML.
- Gli ordini iniettati senza SO non hanno cliente finale → il ramo
  account-manager/CC per cliente (`Sys_email_<cliente>`) non si attiva finché non
  sono abbinati.

---

## 9. Punti — decisi e ancora aperti

**Decisi dal committente:**
- ✅ **Abbinamento manuale inline** dall'addetto prima di spedire: colonna SO vuota
  ma editabile sulla riga di magazzino, picker di SO con stesso prodotto + qtà residua.
- ✅ **Chiave prodotto** = `ProductCode` senza suffisso `|N` uguale a `ItemCode`.
- ✅ **Destinazione editabile inline**: l'addetto imposta/modifica/conferma
  `ShipTo` (direct/normal) sulla riga.
- ✅ **Rosso**: ordine urgente con merce già a magazzino → riga rossa, anche a
  quantità diversa (confronto per `IDOrder`).
- ✅ **Senza SO** (54/256): non spedibili finché il SO di quel prodotto non è
  importato; nessun percorso senza SO.
- ✅ **Parziali**: si inietta la **quota residua** (magazzino − già abbinato); la
  riga abbinata dei planner resta, più una riga "da abbinare" per il residuo.
- ✅ **Data**: da `traceability_rs.dbo.Settings`, attribute **`data_inizio_spedizioni`**
  — esiste, valore **`2026-07-15`**.
- ✅ **Colore iniettati**: righe "da abbinare" in **giallo**, distinto dal rosso
  "urgente-a-magazzino".
- ✅ **Email**: aggiungere la destinazione **direct/normal nel corpo** dell'email
  di conferma.

**Tutte le decisioni sono chiuse** — nessun punto aperto residuo.

---

## 10. Proposta di implementazione (a valle delle decisioni)

**Fase 0 — dato:** nessuno script setting necessario — `data_inizio_spedizioni`
(`2026-07-15`) è già in `Settings`. Si legge col pattern standard del repo
(`SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = ?`).

**Fase 1 — lettura:** nuovo metodo che, per l'intervallo scelto ma non prima di
`data_inizio_spedizioni`, calcola per ogni `IDOrder` a magazzino la **quota residua**:
```
Residua = DisponibileMagazzino(IDOrder, da data_inizio_spedizioni .. @to)
        − SUM(DynamicProductionOrders.Qty per IdOrder)     -- già abbinato
        − QtàGiàSpedita(IDOrder, da data_inizio_spedizioni) -- via ShipmentPallets (§7)
```
Restituisce solo righe con `Residua > 0`, con: `IDOrder, ProductCode, OrderNumber,
WarehouseInsertBox, QtaResidua`.

**Fase 2 — UI:** iniettare quelle righe nella lista superiore con **tag distinto**
"da abbinare" (SO/cliente vuoti). Comportamento:
- riga già abbinata (planner) → come oggi; se urgente-e-a-magazzino → **rossa** (§4bis);
- riga "da abbinare" → **colonna SO editabile inline**: picker dei SO con
  `LEFT(ProductCode,'|') = ItemCode` e residuo > 0 (logica quantità planner);
  **colonna ShipTo editabile inline** (direct/normal). Alla scelta del SO si crea
  l'abbinamento (`orders_manager.create_production_association`), poi si prosegue col
  `ShippingRuleDialog`/conferma v2 esistente.

**Fase 3 — email:** aggiungere la colonna/nota **destinazione (direct/normal)** al
corpo dell'email di conferma (`_send_shipment_email`), dato già disponibile in
`ShipmentPallets.ShipTo`. Salvataggio e PDF invariati.

**Verifica finale (su dati reali, floor 2026-07-15):** che la somma
iniettato + abbinato + già spedito quadri col disponibile a magazzino, che nessun
`IDOrder` compaia due volte con la stessa quota, che gli ordini con residuo ≤ 0
(interamente abbinati) **non** siano iniettati, e che gli urgenti già a magazzino
(oggi 4: IDOrder 11634/11652/11689/11699) risultino rossi. Numeri attuali: **19
iniettati (gialli) + 4 rossi**.

---

## 11. Stato implementazione

- ✅ **Fase 1** — `DynamicShippingWindow._fetch_warehouse_available()` in
  `orders_reports_window.py`: lettura riconciliata (magazzino − abbinato − spedito −
  correzione), floor da `data_inizio_spedizioni`. Verificata: 20 gialle + 4 rosse.
- ✅ **Fase 2** — resa in lista: righe gialle "da abbinare" (`da_abbinare`, giallo
  `#ffe066`) e ordini urgenti-a-magazzino in rosso (`urgent_wh`, `#f5c6cb`). Doppio
  click su riga gialla → `WarehouseMatchDialog`: picker SO (chiave `ItemCode =
  ProductCode` senza `|N`, residuo > 0), quantità, data/ora, destinazione
  direct/normal; crea abbinamento (`DynamicProductionOrders`) + regola
  (`DynamicShippingRules`). Dei 20 gialli, 10 hanno un SO candidato subito.
- ✅ **Correzione "già spedito"** — `WarehouseShippedDialog` +
  `_add_shipped_adjustment()`; tabella `dyn.WarehouseShippedAdjustments`
  (`add_warehouse_shipped_adjustments.sql`, **da applicare**). La lettura è
  resiliente: senza tabella la correzione vale 0.
- ⏳ **Fase 3** — destinazione direct/normal nel corpo email di conferma: da fare.
- ⏳ **Traduzioni** — le nuove chiavi (`wh_*`) hanno default inline; da inserire in
  `AppTranslations` in un secondo passaggio.

---

*Analisi redatta prima delle modifiche; Fasi 1-2 poi implementate. Numeri verificati
sul DB di produzione in sola lettura.*
