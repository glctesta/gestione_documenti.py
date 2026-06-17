# Gestione Scorie / Rientri Materiali — Analisi e progettazione
## v1.0 (BOZZA — in attesa di conferma). **Nessuna modifica al codice effettuata.**

> Attendo la tua conferma e le risposte alle *Decisioni aperte* (§9) prima di scrivere codice.

---

## 1. Obiettivo

Introdurre la **dichiarazione delle scorie/rientri** di materiale come **prerequisito** per
poter richiedere certi materiali indiretti. In sintesi:

1. Nuova voce di menu **"Gestione scorie"** (Manutenzione → Task) che apre una form per
   registrare i kg di materiale scartato/rientrato nella tabella `dbo.ReturnMaterials`.
2. La richiesta di un materiale indiretto **collegato da una regola** (`dbo.MaterialRules`)
   viene **bloccata** se non esiste almeno una dichiarazione di scoria non ancora consumata.
3. All'invio della richiesta, le dichiarazioni di scoria consumate vengono **agganciate** alla
   richiesta (campo `RichiestaId`).

---

## 2. Modello dati (verificato sul DB)

```
ind.Materiali          (MaterialeId PK, CodiceMateriale, DescrizioneMateriale, IsActive, …)
dbo.MaterialRules      (MaterilRuleId PK, MaterialeId, MustCodeId, DateIn, DateOut)
dbo.ReturnMaterials    (ReturnMaterialId PK IDENTITY, MateriaId, ReturWeight float,
                        DateReturn date, UserRetur nvarchar, RichiestaId int NULL, DateOut datetime)
ind.MaterialiRichieste (RichiestaId PK IDENTITY, MaterialeId, QtaRichiesta, …, DataRichiesta, …)
```

**Relazione `MaterialRules`** (interpretazione, da confermare — §9-D1):
- `MaterialeId` = **materiale richiesto** (lo chiamiamo `m`, "IndirectMaterial").
- `MustCodeId` = **materiale-scoria da dichiarare** (lo chiamiamo `m1`, "LinkedMaterial").
- Entrambi sono righe di `ind.Materiali`.
- Regola: *per richiedere `m` devo prima aver dichiarato la scoria del suo `m1`*.

**Query di collegamento** (fornita dall'utente):
```sql
SELECT m1.MaterialeId,                                   -- m1 = MustCode (scoria) -> selezionabile
       m.CodiceMateriale        AS IndirectMaterial,     -- m  = materiale richiesto (contesto)
       m.DescrizioneMateriale   AS IndirectDescription,
       m1.CodiceMateriale       AS LinkedMaterial,
       m1.DescrizioneMateriale  AS LinkedMaterialDescription
FROM ind.Materiali m
  INNER JOIN dbo.MaterialRules mr ON m.MaterialeId = mr.MaterialeId
  INNER JOIN ind.Materiali  m1   ON m1.MaterialeId = mr.MustCodeId
-- proposta: AND mr.DateOut IS NULL  (solo regole attive — §9-D3)
ORDER BY m1.CodiceMateriale;
```
> In `dbo.ReturnMaterials.MateriaId` viene salvato l'**`m1` selezionato** (il MustCode/scoria).

---

## 3. Parte A — Aggiornamento query `_load_materials` (indirect_materials_request.py:197)

**Scopo:** sapere, per ciascun materiale, se ha un **materiale collegato** (`LinkedMaterial` via
`MaterialRules`) → è il flag che attiva il *gating* della scoria al momento della richiesta.

Equivalente pulito della query fornita (stesso risultato, più leggibile dei `RIGHT OUTER JOIN`):
```sql
SELECT m.MaterialeId, m.CodiceMateriale, m.DescrizioneMateriale,
       ISNULL(t.Tipo, 'Generico') AS Tipo,
       ISNULL(s.Qty, 0) AS QtaStock,
       ISNULL(t.QtaConfezione, 1) AS QtaConfezione,
       ISNULL(t.IsFrazionabile, 0) AS IsFrazionabile,
       t.TipoMaterialeId,
       mc.IsFractionabil, mc.QuantityStandard,
       link.CodiceMateriale AS LinkedMaterial,           -- NUOVO
       mr.MustCodeId         AS MustCodeId               -- NUOVO (utile per il gating)
FROM ind.Materiali m
  LEFT JOIN ind.TipoMateriali t        ON m.TipoMaterialeId = t.TipoMaterialeId
  LEFT JOIN ind.MaterialiStock s       ON m.MaterialeId = s.MaterialeId AND s.DateOut IS NULL
  LEFT JOIN dbo.MaterialConfigurations mc ON mc.MaterialId = m.MaterialeId AND mc.DateOut IS NULL
  LEFT JOIN dbo.MaterialRules mr       ON mr.MaterialeId = m.MaterialeId AND mr.DateOut IS NULL
  LEFT JOIN ind.Materiali link         ON link.MaterialeId = mr.MustCodeId
WHERE m.IsActive = 1
ORDER BY m.CodiceMateriale;
```
Nel parsing si aggiungono al dict materiale: `linked_material` (codice) e `must_code_id`
(per il controllo). I materiali con `must_code_id` valorizzato sono soggetti al gating (§6).

> ✅ D2: un materiale ha **al più una** regola attiva (`MaterialRules.DateOut IS NULL`), quindi
> la LEFT JOIN non duplica le righe. Nessuna aggregazione necessaria.

---

## 4. Parte B — Voce di menu "Gestione scorie"

In `main.py` (~riga 16924), **prima** di "Assegna Responsabili":
```python
tasks_submenu.add_command(
    label=self.lang.get('submenu_manage_scrap_returns', 'Gestione scorie'),
    command=self.open_scrap_returns_with_login)
tasks_submenu.add_command(label=self.lang.get('submenu_assign_responsibles', "Assegna Responsabili"),
                          command=self.open_assign_responsibles_with_login)
```
Nuovo handler `open_scrap_returns_with_login` che usa `_execute_authorized_action` con chiave
`'dichiara_scarti-rientri'` e apre la nuova finestra (modulo `scrap_returns_gui.py`).

**Autorizzazione:** la chiave `'dichiara_scarti-rientri'` deve essere **concessa agli utenti**
nella tabella `dbo.AutorizedUsers` (`TranslationKey='dichiara_scarti-rientri'`, `DateOut IS NULL`),
come per le altre voci protette. (Da fare tramite lo strumento di gestione autorizzazioni.)

---

## 5. Parte C — Finestra "Gestione scorie" (nuovo `scrap_returns_gui.py`)

**Selezione materiale (scoria `m1`):** combobox/lista popolata dalla query di collegamento (§2),
mostrando `LinkedMaterial` (codice+descrizione `m1`) come elemento selezionabile e, per contesto,
il materiale richiesto correlato `m` (IndirectDescription). L'utente seleziona **solo `m1`**.

**Campi di registrazione:**
| Campo UI | → ReturnMaterials | Note |
|---|---|---|
| Materiale scoria (`m1`) | `MateriaId` = m1.MaterialeId | da selezione |
| Data | `DateReturn` | **preimpostata a oggi**, modificabile |
| Peso (kg) | `ReturWeight` | numerico, **1 decimale**, > 0 |
| (utente) | `UserRetur` | nome utente autenticato |
| (auto) | `RichiestaId` = NULL | si valorizza solo al consumo (§6) |

**Inserimento:**
```sql
INSERT INTO dbo.ReturnMaterials (MateriaId, ReturWeight, DateReturn, UserRetur, RichiestaId)
VALUES (?, ?, ?, ?, NULL);
```

**Più registrazioni nello stesso giorno:** consentite. Ma prima di inserire, se esiste già una
riga con **stesso `MateriaId` + stessa `DateReturn` + stesso `ReturWeight`** (arrotondato a 1
decimale), mostrare un **warning**: *"Stessa quantità già registrata per questo giorno. Confermi?"*
→ se l'utente conferma, si inserisce comunque.
```sql
SELECT COUNT(*) FROM dbo.ReturnMaterials
WHERE MateriaId = ? AND DateReturn = ? AND ROUND(ReturWeight,1) = ? AND DateOut IS NULL;
```

**Elenco/storico** nella stessa finestra (opzionale ma utile): righe `ReturnMaterials` del
materiale selezionato (data, kg, utente, stato = consumata se `RichiestaId` valorizzato).

---

## 6. Parte D — Gating alla richiesta (indirect_materials_request.py)

Quando si richiede un materiale `m` che **ha una regola** (`must_code_id` valorizzato, §3):

**Prima di permettere la richiesta** (proposta: al momento dell'**aggiunta al carrello** *e*
ri-controllo all'**invio** — §9-D4):
```sql
-- esistono scorie del MustCode (m1) non ancora consumate?
SELECT COUNT(*) FROM dbo.ReturnMaterials
WHERE MateriaId = ?  -- m.must_code_id  (= m1)
  AND RichiestaId IS NULL
  AND DateOut IS NULL;
```
- Se `0` → **avviso** ("Per richiedere questo materiale occorre prima dichiarare la scoria del
  materiale collegato.") e **apertura della form "Gestione scorie"** con login
  `dichiara_scarti-rientri` (vedi §10). La richiesta NON viene aggiunta finché non c'è scoria.
- Se `> 0` → richiesta permessa.

**All'invio della richiesta** (in `_send_all_requests`), modificare l'INSERT per **catturare il
nuovo `RichiestaId`** e poi agganciare le scorie consumate:
```sql
INSERT INTO ind.MaterialiRichieste (MaterialeId, QtaRichiesta, QtaStockAlMomento, Stato,
                                    DataRichiesta, RichiestoDa, ComputerRichiedente)
OUTPUT INSERTED.RichiestaId
VALUES (?, ?, ?, 'RICHIESTA', GETDATE(), ?, ?);

-- subito dopo, per i materiali con regola: aggancia le scorie consumate al RichiestaId.
-- NB: NON tutte indiscriminatamente — entro il limite della quantità richiesta (D7, §9).
-- La logica esatta dipende dalla risposta su D7 (unità di confronto):
--   (c) proposta: aggancia le righe RichiestaId IS NULL in ordine di DateReturn fino a coprire QtaRichiesta.
UPDATE dbo.ReturnMaterials
SET RichiestaId = ?            -- nuovo RichiestaId
WHERE MateriaId = ?           -- m.must_code_id (= m1)
  AND RichiestaId IS NULL
  AND DateOut IS NULL;        -- (filtro/cap da rifinire secondo D7)
```
Tutto nella **stessa transazione** già presente (commit/rollback unico).

> Nota terminologica: nel testo della richiesta era citato *"registrare in `dbo.materialrules`"*;
> l'interpretazione è che la registrazione vada in **`dbo.ReturnMaterials`** (le scorie), non in
> `MaterialRules` (che contiene le regole, gestite altrove). Da confermare (§9-D5).

---

## 7. Componenti / file

| File | Intervento |
|---|---|
| `indirect_materials_request.py` | query `_load_materials` (+LinkedMaterial/MustCodeId); gating in `_add_to_cart`/`_send_all_requests`; OUTPUT RichiestaId + UPDATE ReturnMaterials |
| `main.py` | voce menu "Gestione scorie" + handler `open_scrap_returns_with_login` (auth key) |
| `scrap_returns_gui.py` (**nuovo**) | finestra di registrazione scorie (`ReturnMaterials`) |
| `*_translations.sql` (+DB) | chiavi: `submenu_manage_scrap_returns`, titoli/etichette form, messaggi gating/warning (5 lingue) |
| `dbo.AutorizedUsers` (dati) | concessione chiave `dichiara_scarti-rientri` agli utenti abilitati |

---

## 8. Fasi

| Fase | Contenuto |
|---|---|
| 0 | Aggiornare query `_load_materials` + parsing (LinkedMaterial/MustCodeId) |
| 1 | `scrap_returns_gui.py` + voce menu + handler autorizzato + traduzioni |
| 2 | Gating richiesta (blocco) + cattura RichiestaId + UPDATE ReturnMaterials |
| 3 | Warning duplicato stesso giorno/quantità; storico in form; verifica end-to-end |

---

## 9. Decisioni — RISOLTE (risposte utente)

- **D1 — ✅ confermato:** `MaterialRules.MaterialeId = m` (richiesto), `MustCodeId = m1`
  (scoria da dichiarare, salvato in `ReturnMaterials.MateriaId`).
- **D2 — ✅ regola singola:** un materiale ha **al più UNA** regola **attiva** (`DateOut IS NULL`).
  → niente gestione N-linked; `_load_materials` prende l'unica regola con `DateOut IS NULL`.
- **D3 — ✅ sì:** filtrare solo regole attive (`MaterialRules.DateOut IS NULL`).
- **D4 — ✅ al momento dell'aggiunta della richiesta:** se il materiale è "gated" e non ci sono
  scorie disponibili (`RichiestaId IS NULL`), mostrare **avviso** e poi **aprire la form scorie**
  (con login `dichiara_scarti-rientri`). Vedi §6.
- **D5 — ✅ confermato:** la registrazione scorie va in **`dbo.ReturnMaterials`**.
- **D6 — ✅ sì:** filtrare `ReturnMaterials.DateOut IS NULL` (soft-delete).
- **D7 — ✅ opzione (c):** nessun cap rigido per ora. All'invio si agganciano le scorie
  `RichiestaId IS NULL` del `MustCode` in **ordine di `DateReturn`** accumulando `ReturWeight`
  **fino a coprire `QtaRichiesta`** (l'ultima riga può superare di poco; se il totale disponibile
  è inferiore, si agganciano tutte). Si raccolgono i dati per la futura media scorie/quantità.
- **D8 — ✅ multilingua:** la finestra segue la regola standard (chiavi in `AppTranslations`, 5 lingue).

### Unico punto ancora da chiarire — D7 (unità di confronto)
`ReturnMaterials.ReturWeight` è in **kg**; `ind.MaterialiRichieste.QtaRichiesta` è la quantità
richiesta del materiale indiretto (pezzi/confezioni). Per applicare *"scorie ≤ quantità richiesta"*
serve sapere **come confrontarle**:
- (a) per questi materiali kg e quantità richiesta sono **omogenei** (es. entrambi kg) → confronto diretto;
- (b) servono un fattore di conversione / unità dedicata;
- (c) per ora **nessun blocco rigido**: aggancio le scorie `RichiestaId IS NULL` **fino a coprire**
  `QtaRichiesta` (somma `ReturWeight`), lasciando il resto per richieste future, e raccolgo i dati
  per la media (proposta operativa).

→ **Conferma quale tra (a)/(b)/(c)** prima di implementare l'aggancio scorie↔richiesta (§6).

---

## 10. Integrazione nella form di Richiesta Materiali (requisito aggiuntivo)

- **Segnalazione visiva:** se il codice materiale **appartiene alla categoria** (ha una regola
  attiva in `MaterialRules`), va **evidenziato** nella lista/selezione della form di richiesta
  (es. icona/colore/colonna "Scoria richiesta").
- **Flusso al momento dell'aggiunta della richiesta** per un materiale gated:
  1. verifica scorie disponibili (`ReturnMaterials` del `MustCode`, `RichiestaId IS NULL`, `DateOut IS NULL`);
  2. se **assenti** → **avviso** ("Per richiedere questo materiale occorre prima dichiarare la
     scoria del materiale collegato.") e subito dopo **apertura della form "Gestione scorie"**
     (passando per il login `dichiara_scarti-rientri`);
  3. dopo aver registrato la scoria, l'utente può ri-aggiungere la richiesta (ora consentita).
- All'**invio** della richiesta si aggancia il nuovo `RichiestaId` alle scorie consumate
  (entro il limite di D7).

---

*Fine documento. Manca solo la conferma su D7 (unità di confronto) prima di procedere.*
