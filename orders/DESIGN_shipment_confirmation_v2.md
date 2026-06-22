# Design — Conferma Spedizioni v2 (per Ordine + Pallet + Documenti)

> Documento di verifica della logica. **Nessun codice scritto finché non approvi.**
> Stato attuale di riferimento: [shipment_confirmation_window.py](shipment_confirmation_window.py),
> [shipment_monitor.py](shipment_monitor.py), [add_shipment_confirmation_columns.sql](add_shipment_confirmation_columns.sql).

## 1. Decisioni approvate (input utente)

| # | Scelta | Valore |
|---|--------|--------|
| 1 | Raggruppamento lista e filtri | **Ordine di Produzione** (`dbo.Orders.ordernumber`) |
| 2 | Ambito "spedizione" | **Più ordini insieme** → serve un'entità Spedizione (header) con sotto i pallet |
| 3 | Codice PALLET | **Inserito dall'operatore** (es. etichetta fisica / SSCC) |
| 4 | Documenti | **PDF reportlab + Logo.png**, archiviati su disco + path in SQL; ristampabili |

## 2. Come funziona oggi (sintesi)

- La form conferma **una regola alla volta**: `UPDATE dyn.DynamicShippingRules SET ConfirmedQty, ConfirmedAt, ConfirmedByUser WHERE DybamicShippingRuleId = ?`.
- "Pending" = `R.ConfirmedAt IS NULL` (usato sia dalla form sia dal monitor popup).
- Una sola email di conferma per riga; nessun concetto di pallet, nessun documento, nessuna spedizione.
- Catena tabelle: `DynamicShippingRules (R)` → `DynamicProductionOrders (O)` → `DynamicSaleOrders (D)`; `O.IdOrder` → `dbo.Orders (PO)`.

**Limite:** il modello è 1 conferma = 1 regola. Le nuove richieste (più pallet per ordine, una spedizione su più ordini, residuo da scalare, documenti, correzione) richiedono un modello a 2 livelli.

## 3. Nuovo modello dati (SQL)

Due nuove tabelle nello schema `dyn`. Le colonne di conferma inline esistenti su `DynamicShippingRules` restano (storico + roll-up), ma il flusso nuovo è guidato dalle nuove tabelle.

### 3.1 `dyn.Shipments` — testata spedizione (raggruppa più ordini/pallet)

| Colonna | Tipo | Note |
|---------|------|------|
| ShipmentId | INT IDENTITY PK | |
| ShipmentDate | DATE | **Data della spedizione**, default oggi, editabile |
| Status | NVARCHAR(20) | `OPEN` → `CLOSED` → (`CORRECTED`) |
| CreatedByUser | NVARCHAR(100) | operatore che crea |
| CreatedAt | DATETIME | timestamp creazione |
| ClosedByUser | NVARCHAR(100) NULL | chi ha finalizzato |
| ClosedAt | DATETIME NULL | quando finalizzata |
| LastModifiedByUser | NVARCHAR(100) NULL | per correzioni |
| LastModifiedAt | DATETIME NULL | per correzioni |
| Notes | NVARCHAR(MAX) NULL | |
| PdfPalletPath | NVARCHAR(400) NULL | ultimo PDF "lista per pallet" archiviato |
| PdfSummaryPath | NVARCHAR(400) NULL | ultimo PDF "riepilogo spedizione" archiviato |

### 3.2 `dyn.ShipmentPallets` — righe: quantità confermata per (pallet × ordine)

| Colonna | Tipo | Note |
|---------|------|------|
| ShipmentPalletId | INT IDENTITY PK | |
| ShipmentId | INT FK → Shipments | |
| PalletCode | NVARCHAR(50) | inserito dall'operatore — **univoco solo entro la spedizione** |
| DynamicProductionOrderID | INT FK → DynamicProductionOrders | l'ordine spedito su questo pallet |
| ConfirmedQty | INT | quantità dichiarata spedita su questo pallet per questo ordine |
| ConfirmedByUser | NVARCHAR(100) | |
| ConfirmedAt | DATETIME | |
| — snapshot per documenti stabili — | | (congelati al salvataggio, così le ristampe non cambiano se cambiano i dati sorgente) |
| ProductionOrderNumber | NVARCHAR(50) | |
| SONumber | NVARCHAR(50) | |
| CustomerName | NVARCHAR(200) | |
| ItemCode | NVARCHAR(50) | |
| ItemName | NVARCHAR(200) | |
| ShipTo | NVARCHAR(200) | |

> Un ordine su più pallet = più righe `ShipmentPallets` con stesso `DynamicProductionOrderID` e `PalletCode` diversi.
> Un pallet con più ordini = più righe con stesso `PalletCode` e `DynamicProductionOrderID` diversi.

**Unicità del codice pallet (richiesta utente):** il `PalletCode` deve essere univoco **solo all'interno della stessa spedizione**. In spedizioni diverse o in giorni diversi può ripetersi liberamente. Quindi NON un vincolo globale, ma:
- Constraint a livello tabella: `UNIQUE (ShipmentId, PalletCode)` → impedisce due pallet con lo stesso codice nella stessa spedizione, ma li consente tra spedizioni diverse.
- Nota: lo stesso `PalletCode` può comparire più volte nella **stessa** spedizione se associato a **ordini diversi** (un pallet misto). In tal caso la chiave logica del pallet è `(ShipmentId, PalletCode)` e le righe sono `(ShipmentId, PalletCode, DynamicProductionOrderID)`. → Il constraint UNIQUE corretto è quindi `UNIQUE (ShipmentId, PalletCode, DynamicProductionOrderID)` (un ordine non può comparire due volte sullo stesso pallet della stessa spedizione; lo si aggiorna sommando). *Confermare in §9.*

Migration: stesso pattern `IF NOT EXISTS … CREATE TABLE` del file SQL esistente, idempotente.

## 4. Logica dei totali e del residuo (il cuore)

Raggruppamento per **Ordine di Produzione** (`DynamicProductionOrderID`, mostrato come `ordernumber`).

Per ogni ordine con regole ancora aperte:

```
QtyToShipTotal   = SUM(R.QtyToShip)           -- regole con ConfirmedAt IS NULL (la "domanda")
QtyConfirmedTot  = SUM(SP.ConfirmedQty)        -- da ShipmentPallets per quel DynamicProductionOrderID
Residuo          = QtyToShipTotal - QtyConfirmedTot
```

- L'ordine compare nella lista "da spedire" finché **Residuo > 0**.
- Quando l'operatore dichiara una quantità su un pallet → si crea/aggiorna una riga `ShipmentPallets` → il **Residuo mostrato si scala** in tempo reale.
- **Eccesso consentito (decisione §9.2 = NO blocco):** la somma confermata per un ordine **può superare** `QtyToShipTotal`. In caso di eccesso si mostra un **avviso non bloccante** e si chiede conferma esplicita, ma il salvataggio procede. Di conseguenza il `Residuo` può diventare ≤ 0.

> **Scelta architetturale (aggiornata): niente roll-up di `ConfirmedAt`.**
> Il residuo è calcolato ovunque come `SUM(QtyToShip) − SUM(ShipmentPallets.ConfirmedQty)`. Non si scrive mai `ConfirmedAt` sulle regole dal flusso v2.
> - **Perché:** così le **correzioni** (modifica/elimina pallet) ricalcolano il residuo automaticamente, senza dover "riaprire" regole né distinguere quelle chiuse dal vecchio flusso da quelle chiuse da v2 (operazione ambigua e rischiosa sui dati legacy).
> - **Conseguenza:** la query "pending" del **monitor** ([shipment_monitor.py](shipment_monitor.py)) va aggiornata per sottrarre `ShipmentPallets` (fatto). Gli ordini interamente spediti spariscono dal popup; i parziali restano (decisione §9.3).
> - Le colonne inline `DynamicShippingRules.ConfirmedQty/ConfirmedAt/ConfirmedByUser` restano per i dati **storici** del vecchio flusso; non sono più scritte da v2.
> - Gli ordini già confermati col vecchio flusso (`ConfirmedAt` valorizzato) sono esclusi dalla domanda → nessun doppio conteggio, nessuna migrazione storica.

## 5. Flusso operativo (UI)

Form rielaborata `ShipmentConfirmationWindow`:

1. **Barra filtri** (in alto): casella "Ordine" (cerca su `ordernumber`) + casella "Prodotto" (cerca su `ItemCode`/`ItemName`) + campo **Data spedizione** (default oggi).
2. **Lista ordini da spedire** (griglia 1): una riga per Ordine di Produzione, colonne:
   `Ordine Prod. | Cliente | Ord. Vendita | Codice | Prodotto | Data Sped. | Qtà da Spedire (tot) | Confermato | Residuo`.
3. L'operatore **seleziona un ordine**, inserisce **Codice Pallet** + **Qtà spedita** → bottone **"Aggiungi a spedizione"**:
   - crea la riga in `ShipmentPallets` sotto la **Spedizione corrente** (header `OPEN`, creata alla prima aggiunta),
   - scala il Residuo nella griglia 1.
4. **Pallet della spedizione corrente** (griglia 2): `Pallet | Ordine | Codice | Prodotto | Qtà`, con possibilità di **modificare/eliminare** una riga prima della finalizzazione.
5. **Finalizza spedizione**:
   - imposta `Shipments.Status='CLOSED'`, `ClosedBy/At`,
   - roll-up `ConfirmedAt` sugli ordini completati (§4),
   - genera i **2 PDF** (§6), li archivia e salva i path,
   - invia email di conferma spedizione *(assunzione — §9)*.
6. **Recupera spedizione** (per data): carica una spedizione passata, mostra pallet, consente **correzione** → ricalcola residui/roll-up, **prepara email di correzione**, **ristampa** i PDF (aggiorna `LastModified*`, `Status='CORRECTED'`).

## 6. Documenti (PDF reportlab, pattern di [indirect_materials_pdf.py](indirect_materials_pdf.py))

Intestazione comune a entrambi: **Logo.png**, titolo, **Data spedizione**, **Operatore**, **data/ora generazione** (footer "Generato automaticamente — gg/mm/aaaa hh:mm:ss").

- **Doc A — "Lista Spedizione per Pallet"**: ordinata per `PalletCode`. Per ogni pallet: blocco/tabella con righe `Ordine | Cliente | Codice | Prodotto | Qtà` e subtotale pallet.
- **Doc B — "Riepilogo Spedizione"**: tutti i pallet della spedizione in un'unica vista, con subtotali per ordine e **totale generale** (numero pallet, numero ordini, qtà totale).

Archiviazione: cartella dedicata (es. `…/shipments/SHIP_<ShipmentId>_<timestamp>.pdf`), path salvato su `dyn.Shipments`. Ristampa = rigenerazione dagli snapshot SQL (documenti stabili).

## 7. Email

- **Conferma spedizione** (alla finalizzazione, *assunzione*): riepilogo HTML della spedizione (riusa `utils.get_email_recipients(conn,'Sys_shipment_email')` + `utils.send_email`), allegando o referenziando i PDF.
- **Correzione**: email evidenziata "CORREZIONE" con il delta rispetto alla versione precedente (cosa è cambiato), agli stessi destinatari.

## 8. Impatti sul codice esistente

- [shipment_confirmation_window.py](shipment_confirmation_window.py): riscrittura sostanziale (query raggruppata, 2 griglie, filtri, pallet, finalizza/recupera).
- Nuovo modulo `orders/shipment_pdf.py` per i 2 PDF.
- Nuovo SQL `orders/add_shipments_tables.sql` (le 2 tabelle).
- [shipment_monitor.py](shipment_monitor.py): **query pending aggiornata** per sottrarre `ShipmentPallets` (residuo > 0). Nessun'altra modifica.
- `main.py` / entry-point: invariato (`open_shipment_confirmation_window`).

## 9. Decisioni (confermate dall'utente)

1. **Email su finalizzazione normale**: ✅ **SÌ** — sempre (riepilogo spedizione), oltre a quella di correzione.
2. **Discrepanza qtà**: ❌ **NO blocco** — l'eccesso oltre la qtà da spedire è **consentito** con avviso non bloccante (come oggi). Vedi §4.
3. **Ordini parzialmente spediti**: ✅ **SÌ** — restano nel popup del monitor finché Residuo > 0.
4. **Una spedizione per sessione**: ✅ **SÌ** — una sola `OPEN` per volta, ripresa consentita se non finalizzata.
5. **Permessi**: ✅ **SÌ** — correzione/ristampa con la stessa autorizzazione `conferma_spedizioni`.
6. **Allegato PDF in email**: ✅ **SÌ** — i 2 PDF (lista per-pallet + riepilogo) vengono **allegati** all'email.
7. **Numerazione pallet**: ✅ **SÌ** — campo manuale con **suggerimento automatico progressivo** entro la spedizione (1, 2, 3…), pre-compilato ma sovrascrivibile col codice reale; controllo anti-duplicato live entro la spedizione.
8. **Pallet misto** (stesso codice pallet, ordini diversi nella stessa spedizione): ✅ **SÌ** — chiave riga = `ShipmentId + PalletCode + DynamicProductionOrderID` (vedi §3.2).

---
**Prossimo passo:** confermi (o correggi i punti §9) e procedo con: (a) SQL tabelle, (b) modulo PDF, (c) riscrittura form. Aspetto il tuo OK.
