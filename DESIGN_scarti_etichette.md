# Analisi — Scarti etichette (dichiarazione, stampa/email fine turno, report)

**Stato:** proposta di progetto, nessuna modifica ancora effettuata.
**Menu:** Operazioni → Materiali, due nuove voci dopo "Etichette" (main.py ~16491).

---

## 1. Obiettivo

Tracciare gli scarti di etichette di produzione. Due voci di menu:

1. **Dichiarazione scarti** — form (login operatore) dove si scansionano le etichette
   scartate, con data, motivo scarto e categoria Produzione/Stampa; contatori live;
   stampa/email di riepilogo a fine turno.
2. **Report scarti etichette** — form che genera Excel e PDF (con logo) filtrando per
   data da/a e operatore.

I dati vanno in una nuova tabella `traceability_rs.dbo.labelscrap`.

---

## 2. Pattern riusabili accertati (dal codice)

| Serve | Riuso |
|---|---|
| Login operatore | `self._execute_simple_login(action_callback=...)` — il callback riceve lo *user_id*; il nome operatore si legge da `parent.last_authenticated_user_name` |
| Validazione etichetta | `dbo.LabelCodes.LabelCod` (varchar 150) via `get_scrap_label_info` |
| Motivi scarto | **NUOVA** tabella dedicata `dbo.LabelScrapReasons` (separata da `ScrapResons`, che è per difetti schede) |
| Email destinatari | `utils.get_email_recipients(conn, 'sys_email_labelScrap')` (settings, da creare) |
| Scheduler fine turno | poll `after()` in stile `ShiftHandoverMonitor`, finestra 15:15/23:15 (`if h==15 and 13<=m<=17`) |
| PC designato per stampa | marker file `%LOCALAPPDATA%\labelscrap_print_host.json` (come `shipment_host.json`) |
| Dedup email cross-PC | `_claim_send_slot(conn, key)` — INSERT WHERE NOT EXISTS su settings, chiavi `SentLabelScrap_YYYYMMDD_turno` e `SentLabelScrapWeek_YYYYWW` |
| Stampa su default printer | `os.startfile(path, 'print')` |
| PDF con logo | pattern `orders/shipment_pdf.py` (`_get_logo_path`, `_draw_header`, tabella reportlab) |
| Excel professionale | pattern `openpyxl` (header fill, bordi, autofit, freeze) |
| Invio email | `utils.send_email(recipients, subject, body, is_html=True, attachments=...)` |
| Email venerdì | worker con guard `today.weekday()==4` + claim settimanale |

---

## 3. Tabella `traceability_rs.dbo.labelscrap`

Una riga per etichetta scartata (una per scansione).

| Colonna | Tipo | Note |
|---|---|---|
| `LabelScrapId` | INT IDENTITY PK | |
| `LabelCode` | NVARCHAR(150) | codice scansionato (testo grezzo) |
| `IDLabelCode` | INT NULL | FK LabelCodes se il codice è noto (altrimenti NULL) |
| `ScrapDate` | DATE NOT NULL | data dichiarata dall'operatore |
| `LabelScrapReasonId` | INT NOT NULL | FK LabelScrapReasons |
| `Category` | NVARCHAR(20) NOT NULL | 'Production' / 'Print' |
| `Operator` | NVARCHAR(200) NOT NULL | nome operatore (last_authenticated_user_name) |
| `Shift` | NVARCHAR(10) NULL | turno al momento (07:30/15:30/23:30) |
| `Hostname` | NVARCHAR(100) NULL | PC di dichiarazione |
| `Printed` | DATETIME NULL | quando il riepilogo è stato stampato (NULL = da stampare) |
| `DateIn` | DATETIME NOT NULL DEFAULT GETDATE() | timestamp inserimento |

`dbo.LabelScrapReasons`: `LabelScrapReasonId` INT IDENTITY PK, `Reason` NVARCHAR(150),
`IsActive` BIT DEFAULT 1.

---

## 4. Form "Dichiarazione scarti"

- Apertura: `_execute_simple_login`; operatore in sola lettura da `last_authenticated_user_name`.
- Campi: **data** (default oggi), **motivo** (combo da LabelScrapReasons attivi),
  **categoria** Produzione/Stampa (radio/toggle), campo **scansione etichetta** (Enter).
- Ad ogni scansione: INSERT in `labelscrap` e aggiornamento **contatori live**:
  - scansionate in **questa sessione**;
  - dall'operatore nella **settimana** corrente, nel **mese**, nell'**anno**;
  - **contatore generale** (tutti gli operatori) — totale complessivo.
- Alla chiusura: chiede se stampare il **riepilogo dichiarazione** (PDF con logo). Se sì,
  stampa su default printer e segna `Printed=GETDATE()` sulle righe della sessione.
- Se l'operatore non stampa, le righe restano `Printed=NULL`.

---

## 5. Fine turno (15:15 e 23:15) — solo sul PC designato

Monitor in stile `ShiftHandoverMonitor`, attivo solo se esiste
`labelscrap_print_host.json`. Nella finestra 15:15±2 e 23:15±2 (15 min prima di
15:30/23:30):

1. **Stampa** il riepilogo delle righe del turno non ancora stampate
   (`Printed IS NULL`), poi le segna `Printed=GETDATE()` — così non si ristampa.
2. **Email** (dedup cross-PC via claim `SentLabelScrap_YYYYMMDD_turno`) ai destinatari
   `sys_email_labelScrap`, con allegato PDF/Excel del turno.

## 6. Email settimanale (venerdì pomeriggio)

Worker con guard `weekday()==4`, claim `SentLabelScrapWeek_YYYYWW`: invia il resoconto
della settimana con rolling **dall'inizio del mese** e **YTD**, Excel + PDF.

---

## 7. Report scarti etichette (seconda voce)

Form con filtri **data da/a** e **operatore** (combo dagli operatori presenti in
labelscrap). Genera **Excel** e **PDF professionale con logo** del dettaglio +
riepiloghi (per operatore, per motivo, per categoria).

---

## 8. Decisioni (prese)

1. ✅ **Validazione etichetta**: accetta qualunque codice come testo; se noto in
   `LabelCodes` salva anche `IDLabelCode`, altrimenti NULL. Non blocca i misprint.
2. ✅ **PC di stampa fine turno**: un solo PC designato via marker
   `labelscrap_print_host.json` (con voce di attivazione/disattivazione).
3. ✅ **Riepilogo fine turno**: un documento **separato per ogni operatore** che ha
   dichiarato nel turno e non ha stampato.
4. ✅ **Motivi scarto**: set di **default** in `LabelScrapReasons` + piccola **UI di
   gestione** per correggerli. Default proposti: inceppamento stampante, dati errati,
   etichetta danneggiata, codice illeggibile, ristampa, nastro/toner esaurito, altro.

---

*Analisi redatta prima di qualsiasi modifica. Pattern verificati sul codice reale.*
