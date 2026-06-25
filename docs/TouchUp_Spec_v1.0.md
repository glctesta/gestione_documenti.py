# Touch-Up — Segnalazione problemi schede & instradamento ai tecnici (Spec v1.1)

> Documento di **revisione** (v1.1: integrate le tue decisioni — marker locale, query destinatari, chiusura/riapertura, escalation, intervalli). Nessun codice verrà scritto finché non approvi e non confermi i 3 residui minori in §10.
> Riuso pattern esistenti: verifica LabelCode dei FAI/FQC, monitor popup per-postazione (cambio turno / spedizioni / materiali indiretti), destinatari email da `dbo.Settings`.

## 1. Obiettivo
Dare all'area **Touch-Up** uno strumento per **registrare e segnalare tempestivamente** le problematiche riscontrate sulle schede elettroniche visionate. Le segnalazioni vengono **instradate automaticamente** ai reparti competenti (principalmente i tecnici del **wave soldering**, ma anche altri) in base al **tipo di problema**. I tecnici ricevono un **popup** sulle postazioni configurate e devono **leggere e confermare le azioni** intraprese. Il sistema misura il **tempo di reazione** e, in caso di **ricorrenza** dello stesso problema sullo stesso ordine, **rinforza** l'avviso e invia un'**email** ai responsabili.

## 2. Menu (nuovo gruppo "Touch-up")
Nuova voce **"Touch-up"** (cascade) inserita **subito dopo il gruppo FQC Prodotti**, nello stesso menu `declarations_submenu` ([main.py:16594-16620](../main.py#L16594)). Sottovoci:

| # | Voce | Apre | Autorizzazione (`_execute_authorized_action`) |
|---|------|------|----------------------------------------------|
| 1 | **Problemi rivelati** | form operatore Touch-Up: inserisce LabelCode + problemi | chiave **`operatore_touchup`** |
| 2 | **Soluzioni adottate** | form tecnico: legge segnalazione e conferma azioni | chiave **`tecnico_risponde_touchup`** |
| 3 | **Rapporti** | report (da definire più avanti) | **nessun login** |
| 4 | **Setup workstation** | abilita i popup su una postazione | chiave **`attiva_workstation_tecnici`** |
| 5 | **Gestione** | anagrafica problemi + instradamento problema→reparto | chiave **`set_up_touchup`** |

> Le chiavi vanno abilitate in `dbo.AutorizedUsers` (via permissions_gui) per gli utenti competenti.

## 3. Modello dati (nuove tabelle — bozza, da approvare)

### 3.1 `dbo.TouchUpProblems` — catalogo problemi (combo del menu 1)
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpProblemId | INT IDENTITY PK | |
| ProblemCode | NVARCHAR(30) NULL | codice breve opzionale |
| ProblemDescription | NVARCHAR(200) NOT NULL | testo mostrato nel combo |
| Severity | TINYINT NULL | opzionale (priorità base) |
| DateOut | DATETIME NULL | soft-delete (attivo = NULL) |

CRUD in **menu 5** (introdurre/modificare/cancellare le voci del combo del menu 1).

### 3.2 `dbo.TouchUpProblemRouting` — instradamento problema → reparto
Realizza **issue → CdcId → SubCdcId** (uno o molti reparti per problema).
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpRoutingId | INT IDENTITY PK | |
| TouchUpProblemId | INT FK → TouchUpProblems | |
| CdcId | INT | FK logica → employee.dbo.costcenters |
| SubCdcId | INT NULL | FK logica → employee.dbo.CdcSub (NULL = tutto il CdC) |
| DateOut | DATETIME NULL | soft-delete |

I **destinatari** (tecnici/persone) si ricavano dai dipendenti collegati a `CdcId`/`SubCdcId` con la **query fornita** (parametrizzata su `@CdcId` e lista `@SubCdcIds`):

```sql
SELECT c.CdcId, c.CdcDescription, cs.SubCdcId, cs.SubCdcDescription,
       e.EmployeeName + ' ' + e.EmployeeSurname AS Employee,
       f.functioncode, a.WorkEmail
FROM employee.dbo.costcenters c
  INNER JOIN employee.dbo.cdcsub cs ON c.cdcid = cs.cdcid
  INNER JOIN employee.dbo.EmployeeCdcStories ch ON ch.SubCdcId = cs.SubCdcId AND ch.dateout IS NULL
  INNER JOIN employee.dbo.functions f ON f.functionid = ch.FunctionId
  INNER JOIN employee.dbo.employeehirehistory h ON ch.EmployeeHireHistoryId = h.EmployeeHireHistoryId
       AND h.employeerid = 2 AND h.EndWorkDate IS NULL
  INNER JOIN employee.dbo.employees e ON e.employeeid = h.employeeid
  INNER JOIN employee.dbo.EmployeeAddress a ON a.EmployeeId = e.employeeid AND a.dateout IS NULL
WHERE c.cdcid = ? AND cs.subcdcid IN (...);
```

- **Destinatari "tecnici"** = tutte le righe del CdC/SubCdC instradato (WorkEmail).
- **`functioncode = 70` = il CAPO** a cui **escalare**: in caso di **mancata risposta entro XX minuti** (XX da setup), oppure **invii ripetuti** dello stesso problema sullo stesso ordine, oppure **nella giornata/periodo** lo stesso tipo di problema anche per ordini/prodotti diversi (soglia da setup).

### 3.3 `dbo.TouchUpReports` — testata segnalazione
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpReportId | INT IDENTITY PK | |
| CreatedAt | DATETIME NOT NULL (GETDATE) | inizio conteggio tempo di reazione |
| CreatedByUser | NVARCHAR(100) | operatore Touch-Up |
| ComputerSrc | NVARCHAR(100) | host |
| Status | NVARCHAR(20) | `NEW` → `ACK`/`CLOSED` (risposta) → eventuale `REOPENED` |
| EscalationLevel | INT DEFAULT 0 | aumenta sulle ricorrenze/escalation al capo |
| FirstResponseAt | DATETIME NULL | prima risposta tecnico (per tempo di reazione) |
| ClosedAt | DATETIME NULL | chiusura |
| ReopenCount | INT DEFAULT 0 | quante volte riaperta (stesso prodotto+problema) |
| Notes | NVARCHAR(MAX) NULL | |

### 3.4 `dbo.TouchUpReportLabels` — schede segnalate (1..N per report)
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpReportLabelId | INT IDENTITY PK | |
| TouchUpReportId | INT FK | |
| IDLabelCode | INT | da verifica LabelCode |
| LabelCod | NVARCHAR(50) | snapshot |
| IDOrder | INT | snapshot |
| OrderNumber | NVARCHAR(50) | snapshot (chiave per ricorrenza) |
| IDProduct | INT | snapshot |
| ProductCode | NVARCHAR(50) | snapshot |

### 3.5 `dbo.TouchUpReportProblems` — problemi del report (1..N per report)
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpReportProblemId | INT IDENTITY PK | |
| TouchUpReportId | INT FK | |
| TouchUpProblemId | INT FK → TouchUpProblems | |

> Una segnalazione = N schede × M problemi. L'instradamento avviene **per problema** (ogni problema → suoi reparti).

### 3.6 `dbo.TouchUpResponses` — risposta del tecnico (menu 2)
| Colonna | Tipo | Note |
|---|---|---|
| TouchUpResponseId | INT IDENTITY PK | |
| TouchUpReportId | INT FK | |
| RespondedByUser | NVARCHAR(100) | tecnico |
| RespondedAt | DATETIME (GETDATE) | |
| ReactionSeconds | INT | = DATEDIFF(s, Report.CreatedAt, RespondedAt) |
| ActionsTaken | NVARCHAR(MAX) | azioni intraprese / da intraprendere |

### 3.7 Workstation popup (menu 4) — DECISO: marker locale
Come **materiali indiretti / cambio turni**: il menu 4, eseguito **sulla postazione**, crea il marker `touchup_host.json` in `%LOCALAPPDATA%` con il/i reparto/i (CdcId/SubCdcId) della postazione. Un `touchup_monitor.py` (polling **60s**, configurabile) mostra il popup quando arrivano report **instradati al suo reparto** non ancora gestiti; il popup **ricompare ogni 5 min** (configurabile) finché non viene gestito. Config in `touchup_monitor_config.json` (intervallo polling + ricomparsa).

Marker/chiavi **dedicati** (`touchup_host.json`) così i popup **non** si attivano per spedizioni/materiali/turni.

## 4. Verifica LabelCode (riuso FAI/FQC)
Nel menu 1 i LabelCode inseriti vengono verificati con la query già usata (`_Q_LABELCODE_INFO`, [fqc_products_gui.py:66](../fqc_products_gui.py#L66)): `LabelCod` → `IDLabelCode, IDOrder, OrderNumber, IDProduct, ProductCode`. LabelCode non trovato → errore (non salvabile).

## 5. Flusso operativo

### Menu 1 — Problemi rivelati (operatore Touch-Up)
1. Inserisce **uno o più LabelCode** (verificati uno a uno → mostra ProductCode/OrderNumber).
2. Seleziona dal combo **uno o più problemi** (`TouchUpProblems` attivi) legati a quella scheda/gruppo.
3. **Conferma e salva** → crea `TouchUpReports` + `TouchUpReportLabels` + `TouchUpReportProblems`.
4. Il salvataggio **attiva i popup** sulle postazioni dei reparti instradati (per ciascun problema → routing → reparti).

### Menu 2 — Soluzioni adottate (tecnico)
1. Popup invita il tecnico ad aprire la form.
2. Il tecnico **legge** il contenuto della segnalazione.
3. **Conferma le azioni** che intende svolgere / ha svolto → crea `TouchUpResponses` con **tempo di reazione** (`ReactionSeconds`). Report passa a `ACK`/`CLOSED`. Il popup smette.

### Menu 4 — Setup workstation
Abilita/disabilita i popup Touch-Up sulla postazione (vedi §3.7) e ne imposta il reparto.

### Menu 5 — Gestione
- CRUD **anagrafica problemi** (`TouchUpProblems`) → popola il combo del menu 1.
- **Instradamento** problema → CdcId → SubCdcId (`TouchUpProblemRouting`), con selezione da `employee.dbo.costcenters` / `employee.dbo.CdcSub`.

### Menu 3 — Rapporti
Da definire più avanti (placeholder).

## 6. Ricorrenza, chiusura/riapertura, escalation e tempo di reazione
- **Tempo di reazione** = `TouchUpReports.CreatedAt` → `FirstResponseAt` (prima risposta del tecnico in menu 2).
- **Chiusura**: la conferma azioni in menu 2 **chiude** la segnalazione (`CLOSED`, `ClosedAt`).
- **Riapertura**: se **per lo stesso PRODOTTO** si ripresenta **lo stesso PROBLEMA** dopo la chiusura, la segnalazione si **riapre** (`REOPENED`), `ReopenCount++`, popup riattivato. (Match per `ProductCode` + `TouchUpProblemId`.)
- **Ricorrenza per escalation**: chiave **(OrderNumber + TouchUpProblemId)**. Lo stesso **problema** può inoltre ricorrere su **più ordini/prodotti** nella **giornata/periodo** (per l'escalation al capo).
- **Popup più forte/insistente** su ricorrenze/riaperture (ricomparsa ridotta, colore/suono marcati, `EscalationLevel++`).
- **Escalation al CAPO** (`functioncode = 70` del reparto instradato) quando:
  1. **mancata risposta** entro **XX minuti** dalla creazione (XX = `NoResponseEscalationMinutes`, setup), oppure
  2. **2ª+ segnalazione ricorrente** stesso (OrderNumber+Problema), oppure
  3. **stesso tipo di problema** ≥ **N volte** nella giornata/periodo anche su ordini/prodotti diversi (N = `DayRecurrenceThreshold`, setup).

## 7. Email & destinatari
- **Trigger email** (warning con dati sintetici: cosa, ordine/prodotto, quante volte, tempi, persone implicate):
  1. dalla **2ª segnalazione ricorrente** dello stesso problema (stesso OrderNumber+Problema), **oppure**
  2. quando una segnalazione **chiusa viene riaperta** da un'ulteriore segnalazione (stesso prodotto+problema).
  *(da confermare se inviare anche alle ricorrenze 3ª/4ª — §10.5)*
- **Destinatari**: `Settings.Sys_email_TouchUp_warning` (via `utils.get_email_recipients`), in **CC il capo** (`functioncode=70`) del/i reparto/i instradato/i; opzionale in CC i tecnici del reparto.

## 7-bis. Parametri di setup (configurabili)
- **Locali** (`touchup_monitor_config.json`, come gli altri monitor): `polling_seconds` (default **60**), `reappear_minutes` (default **5**).
- **Globali** (in `dbo.Settings` o tabella `dbo.TouchUpConfig`): `NoResponseEscalationMinutes` (XX), `DayRecurrenceThreshold` (N), definizione di "giornata/periodo" (default **giorno di produzione 07:30→07:30**, come PTHM).

## 8. Pattern riusati (riferimenti)
- Verifica LabelCode: `_Q_LABELCODE_INFO`.
- Monitor popup per-postazione: `shift_handover_monitor.py`, `orders/shipment_monitor.py`, `indirect_materials_wh_monitor.py` (marker host JSON + polling + intervallo ricomparsa configurabile).
- Email: `utils.get_email_recipients` + `utils.send_email`.
- Traduzioni: `dbo.AppTranslations` (5 lingue) per tutte le nuove stringhe.

## 9. Cosa verrà creato (se approvi)
1. SQL migration: 6 tabelle (§3.1–3.6) [+ eventuale §3.7 opzione B], idempotente.
2. Moduli GUI: `touchup_operator_gui.py` (m.1), `touchup_response_gui.py` (m.2), `touchup_setup_gui.py` (m.5), `touchup_workstation_config.py` (m.4), `touchup_monitor.py` (popup).
3. Voci di menu + handler in `main.py` (con le 4 chiavi di autorizzazione).
4. Logica escalation/email + chiave `Sys_email_TouchUp_warning`.
5. Traduzioni 5 lingue.

## 10. Decisioni (confermate) e residui
1. ✅ **Workstation**: marker **locale** per-postazione (come materiali indiretti / cambio turni); ogni PC è legato al/i **reparto/i** e filtra i popup.
2. ✅ **Query destinatari**: fornita (vedi §3.2); `functioncode=70` = capo per escalation.
3. ✅ **Chiusura/riapertura**: la risposta **chiude**; si **riapre** se lo stesso problema si ripresenta per lo **stesso prodotto** (`ReopenCount`).
4. ✅ **Ricorrenza**: **(OrderNumber + Problema)**; il problema può ricorrere su più ordini (per soglia giornaliera).
5. ⏳ **Email**: alla **2ª ricorrente** e su **riapertura** (confermato). Da confermare: inviare **anche** alle ricorrenze successive (3ª, 4ª…)? *(default proposto: sì, ad ogni nuova ricorrenza/riapertura)*
6. ✅ **Più problemi → reparti diversi**: percorsi/popup/email **separati per reparto**.
7. ✅ **Intervalli**: polling **60s**, ricomparsa **5 min**, entrambi **settabili** (setup).

### Residui — CONFERMATI
- ✅ Email **ad ogni** ricorrenza oltre la 2ª (e ad ogni riapertura).
- ✅ Default: `NoResponseEscalationMinutes = 30`, `DayRecurrenceThreshold = 3`.
- ✅ "Giornata/periodo" = giorno di produzione **07:30→07:30** (come PTHM).

---
**Prossimo passo**: confermi i 3 residui sopra e procedo con: (a) SQL tabelle, (b) moduli GUI (operatore/risposta/setup/gestione), (c) monitor popup, (d) escalation+email, (e) traduzioni.
