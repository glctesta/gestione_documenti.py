# Attribuisci CDC — Analisi e progettazione
## v1.0 (BOZZA — in attesa di conferma). **Nessuna modifica al codice effettuata.**

> Riepilogo della logica concordata. Attendo il tuo OK (e le risposte ai *Punti aperti* §9)
> prima di scrivere codice.

---

## 1. Obiettivo

Nuova voce di menu **Strumenti → "Attribuisci cdc"**. Consente a un **capo dipartimento**
di **riassegnare il sotto-reparto (SubCdc)** di un dipendente a lui subordinato, mantenendo
invariati **CdcId** (dipartimento) e **FunctionCode** (livello/funzione). La modifica viene
**storicizzata** nella tabella `employee.dbo.EmployeeCdcStories` (chiusura della riga attiva +
inserimento nuova riga) e notificata via **email**.

---

## 2. Accesso e identità del capo

- Apertura sotto `_execute_authorized_action('gestisci_cdc_operatore', ...)`.
  - ⚠️ Nel messaggio la chiave era scritta `gestisci"cdc_operatore` (con doppio apice):
    presumo un refuso per **`gestisci_cdc_operatore`**. → §9-A1.
- Dal login recupero (già disponibili dopo l'autorizzazione):
  - `self.last_authorized_user_id` = **EmployeeHireHistoryId del capo** (= `auth_result.AuthorizedEmployeeHireHistoryId`).
  - `self.last_authenticated_user_name` = nome del capo.
- L'`EmployeeHireHistoryId` del capo è il parametro della **Query A** (sotto).

---

## 3. Modello dati (verificato sul DB)

```
employee.dbo.EmployeeCdcStories (EmployeeCdcStoryId PK IDENTITY, EmployeeHireHistoryId,
                                 SubCdcId, FunctionId, DateIn NOT NULL, DateOut NULL)
employee.dbo.CdcSub        (SubCdcId PK, CdcId, SubCdc, SubCdcDescription, DirectEmployee,
                            IndirectProduction, ...)
employee.dbo.CostCenters   (CdcId PK, CdcDescription, Cdc, ...)
employee.dbo.Functions     (FunctionId PK, FunctionCode int, FunctionDescription, ...)
employee.dbo.EmployeeHireHistory / Employees / EmployeeAddress (per nome + WorkEmail)
```
- `CdcId` **non** è colonna di `EmployeeCdcStories`: deriva da `SubCdcId` via `CdcSub`.
  → "CdcId non modificabile" si traduce nel vincolo: **il nuovo SubCdc deve appartenere allo
  stesso CdcId** del dipendente.
- "FunctionCode non modificabile" → nell'INSERT si riusa **lo stesso FunctionId**.
- `EmployeeCdcStoryId` è **IDENTITY** → l'INSERT non lo elenca.
- Attributo `settings 'cambio_subcdc'`: **ASSENTE** oggi → da creare (§8).

---

## 4. Query

### 4.1 Query A — dati del capo (dipartimento + soglia), dal suo EmployeeHireHistoryId
Versione corretta e qualificata `employee.dbo` (fix: `f.dunctioncode`→`f.FunctionCode`, tabelle
non qualificate → il DB di default della connessione è `Traceability_rs`, quindi vanno prefissate):
```sql
SELECT cs.CdcId, ec.SubCdcId, cs.SubCdcDescription, f.FunctionCode
FROM employee.dbo.EmployeeHireHistory h
INNER JOIN employee.dbo.EmployeeCdcStories ec ON ec.EmployeeHireHistoryId = h.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
INNER JOIN employee.dbo.CdcSub cs      ON ec.SubCdcId = cs.SubCdcId
INNER JOIN employee.dbo.CostCenters cc ON cs.CdcId   = cc.CdcId
INNER JOIN employee.dbo.Functions f    ON ec.FunctionId = f.FunctionId
WHERE h.EmployeerId = 2 AND h.EndWorkDate IS NULL
  AND h.EmployeeHireHistoryId = ?;   -- EmployeeHireHistoryId del capo (dal login)
```
→ ottengo **CdcId del capo** e **FunctionCode del capo** (soglia). Vedi §9-A2 (capo con più righe attive).

### 4.2 Query B — elenco dipendenti subordinati (query fornita + filtro subordinazione)
La query "grande" fornita, con in più `EmployeeHireHistoryId` e `EmployeeCdcStoryId` (servono al
salvataggio) e il filtro di subordinazione:
```sql
SELECT UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Employee,
       h.EmployeeHireHistoryId, ec.EmployeeCdcStoryId,
       c.CdcId, c.CdcDescription, cs.SubCdcId, cs.SubCdcDescription,
       cs.IndirectProduction, cs.DirectEmployee,
       f.FunctionId, f.FunctionCode, f.FunctionDescription
FROM employee.dbo.Employees e
INNER JOIN employee.dbo.EmployeeHireHistory h ON e.EmployeeId = h.EmployeeId
       AND h.EndWorkDate IS NULL AND h.EmployeerId = 2
INNER JOIN employee.dbo.EmployeeCdcStories ec ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
INNER JOIN employee.dbo.CdcSub cs      ON ec.SubCdcId = cs.SubCdcId
INNER JOIN employee.dbo.CostCenters c  ON c.CdcId = cs.CdcId
INNER JOIN employee.dbo.Functions f    ON ec.FunctionId = f.FunctionId
WHERE c.CdcId = ?                                   -- CdcId del capo (Query A)
  AND f.FunctionCode < ?                            -- SOLO subordinati (soglia capo)
  -- filtri UI opzionali:
  AND (@SubCdc IS NULL OR cs.SubCdcDescription = @SubCdc)
  AND (@Name  IS NULL OR UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) LIKE @Name)
ORDER BY UPPER(e.EmployeeSurname + ' ' + e.EmployeeName);
```

### 4.3 Opzioni "Nuovo SubCdc" (stesso CdcId del dipendente)
```sql
SELECT SubCdcId, SubCdcDescription FROM employee.dbo.CdcSub
WHERE CdcId = ? ORDER BY SubCdcDescription;
```

### 4.4 WorkEmail del capo (TO della mail)
```sql
SELECT a.WorkEmail FROM employee.dbo.EmployeeHireHistory h
INNER JOIN employee.dbo.EmployeeAddress a ON a.EmployeeId = h.EmployeeId AND a.DateOut IS NULL
WHERE h.EmployeeHireHistoryId = ?;
```

---

## 5. Form (nuovo `attribuisci_cdc_gui.py`)

- **Filtri** in alto:
  - Cognome/Nome (entry, LIKE) — la "funzione di filtro cognome nome".
  - **SubCdcDescription** (combo, valori dai SubCdc del dipartimento del capo).
  - Pulsante *Cerca*.
- **Combo/lista dipendenti**: risultati di Query B (subordinati). Colonne: Dipendente, SubCdc
  attuale, Funzione, ecc.
- Alla **selezione** del dipendente:
  - mostro (sola lettura) **CdcId/CdcDescription** e **FunctionCode/FunctionDescription** (NON modificabili);
  - **combo "Nuovo SubCdc"** con i SubCdc dello **stesso CdcId** (Query 4.3).
- Pulsante **Salva**.

---

## 6. Salvataggio (storicizzazione) — in un'unica transazione

Sul record attuale del **dipendente selezionato** (identificato dal suo `EmployeeCdcStoryId`
di Query B):
```sql
-- 1) chiudo la storia attiva selezionata
UPDATE employee.dbo.EmployeeCdcStories
SET DateOut = GETDATE()
WHERE EmployeeCdcStoryId = ? AND DateOut IS NULL;

-- 2) inserisco la nuova storia col nuovo SubCdc (stesso FunctionId, DateIn ora)
INSERT INTO employee.dbo.EmployeeCdcStories (EmployeeHireHistoryId, SubCdcId, FunctionId, DateIn)
VALUES (?, ?, ?, GETDATE());
```
- `EmployeeHireHistoryId` e `FunctionId` invariati (dal record selezionato).
- `SubCdcId` = nuovo scelto; **vincolo applicativo**: il suo `CdcId` deve coincidere con quello
  attuale (garantito perché la combo mostra solo SubCdc dello stesso CdcId).
- Commit unico; in caso di errore rollback.

---

## 7. Email di notifica (dopo il commit)

- **TO**: WorkEmail del **capo** che ha effettuato il login (Query 4.4).
- **CC**: indirizzi da `traceability_rs.dbo.settings` con `Atribute = 'cambio_subcdc'`
  (via `utils.get_email_recipients(conn, 'cambio_subcdc')`).
- **Corpo** (riepilogo): dipendente, **da** SubCdc → **a** SubCdc, dipartimento (CdcDescription),
  funzione, chi ha eseguito la modifica (capo) e data/ora.
- Invio con `utils.send_email(recipients=[to], subject=..., body=..., is_html=True, cc_emails=cc)`.
- Se manca la WorkEmail del capo o l'attributo `cambio_subcdc` è vuoto: la modifica resta
  salvata; si logga un warning e si avvisa che la mail non è stata inviata (§9-A5).

---

## 8. Componenti / file previsti

| File | Intervento |
|---|---|
| `attribuisci_cdc_gui.py` (**nuovo**) | form: filtri, elenco subordinati, combo nuovo SubCdc, salva + email |
| `main.py` | voce menu Strumenti "Attribuisci cdc" + handler `open_attribuisci_cdc_with_login` (chiave `gestisci_cdc_operatore`) |
| `insert_attribuisci_cdc_translations.py` (**nuovo**) | traduzioni menu + form (5 lingue) |
| `settings` (dato) | inserire `Atribute='cambio_subcdc'` con i destinatari CC (Employeerid=2) |
| `dbo.AutorizedUsers` (dato) | concedere la chiave `gestisci_cdc_operatore` ai capi dipartimento |

---

## 9. Punti aperti — da confermare

- **A1 — Chiave permesso**: uso **`gestisci_cdc_operatore`** (il messaggio riportava
  `gestisci"cdc_operatore`, presumo refuso). Confermi?
- **A2 — Capo con più righe attive** in `EmployeeCdcStories` (più CdcId/funzioni): come
  definisco dipartimento e soglia? *Proposta*: considero tutte le sue righe attive →
  dipendenti con `CdcId ∈ {CdcId del capo}` e `FunctionCode < MAX(FunctionCode del capo)`.
  In alternativa, se il capo ha una sola riga attiva (caso tipico) il problema non si pone.
- **A3 — Soglia**: "inferiore" = **strettamente `<`** (escludo pari livello). Confermi (oppure `<=`)?
- **A4 — Spostamento solo entro il proprio CdcId**: il nuovo SubCdc è ristretto allo **stesso
  CdcId** del dipendente (per non modificare il CdcId). Confermi?
- **A5 — Email**: HTML, lingua **italiano** (come le altre notifiche di sistema)? Comportamento
  se `cambio_subcdc` è vuoto o manca la WorkEmail del capo (salvo comunque + warning)?
- **A6 — DateIn nuova riga** = `GETDATE()`. Confermi (nessun altro campo da valorizzare).

---

*Fine documento. In attesa di OK e risposte §9 prima di procedere.*
