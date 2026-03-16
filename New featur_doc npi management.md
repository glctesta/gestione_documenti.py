<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Voglio creare un breakdown document per cloud sonet in antropic per sviluppare una nuova funzione nella sezione del NPI project management che si attiva con :

open_npi_project_management
in Document managemet program .
Nella form di gestione dei progetti npi c'e' la possibilita' di aggiungere diversi tipi di documenti, ma non c'e' la loro gestione.
Dobbiamo aggiungere un bottone , in basso alla form di gestione dei progetti NPI, per aprire na form per listare tutti i documenti caricati, con la possibilita' di ordinarli per data, tipo, appartenenza a quale task, data inserimento con la possibilita' di cericarne di nuovo (sempre legati al progetto NPI a cui si fa riferimento) modificarli, con softdelete usando un campo DateOut (datetime) per matenere sempre la cronologia, e cancellazione (softdelete)
Se i documento dono marcati per avere un valore, in fondo alla pagina un riepilogativo con il numero dei documenti e (per quelli che hanno un valore) il totale.

Prima di effettuare qualunque scrittura o modifica di codice bisogna assolutamente considerare:

1. Nessun parametro che attualmente funziona deve essere modificato
2. Per le connessioni al db si usano le cn attuali, non ne vanno scritte altre
3. Prima di completare il lavoro, tutte le funzioni devono essere verificate e testate.
4. le nuove label devono essere tradotte in in.ro.it.sv.de e salvate in traceability_rs.dbo.apptranslations(LanguageCode,TranslationKey,TranslationValue) e davanti alla traduzione in Rumeno va anteposto N per garantire il salvataggio dei caratteri diacrilici.

Ho una visione chiara della struttura del progetto. Ora ho abbastanza contesto per creare il breakdown document completo per Claude Sonnet. Lo genero in formato Markdown professionale, pronto per essere incollato direttamente nel prompt di Claude.

***

# Breakdown Document — NPI Document List Manager

Ecco il documento di breakdown completo, pronto da usare come prompt per **Claude Sonnet (Anthropic)**:

***

```markdown
# BREAKDOWN DOCUMENT — NPI Document List Manager
## Feature: `open_npi_project_management` → Gestione Documenti Progetto NPI
**Repository:** glctesta/gestione_documenti.py (branch: master)
**Data:** 2026-03-16
**Priorità:** Alta
**Autore:** glctesta

---

## 1. CONTESTO E OBIETTIVO

Nel Document Management Program esiste la sezione NPI Project Management,
attivata dal comando `open_npi_project_management`.
La form di gestione progetti NPI permette già di aggiungere diversi tipi di documenti
ai progetti/task, ma non esiste una vista di gestione e consultazione di tali documenti.

L'obiettivo è aggiungere, in fondo alla form NPI esistente, un pulsante che apre una
nuova form dedicata alla **gestione completa dei documenti** associati al progetto NPI
correntemente selezionato.

---

## 2. VINCOLI ASSOLUTI (NON NEGOZIABILI)

1. **NESSUN parametro attualmente funzionante deve essere modificato.**
2. **Per le connessioni al DB si usano le connessioni esistenti nel progetto** (vedere
   `db_connection.py` e `database_config.py`). Non creare nuove stringhe di connessione.
3. **Tutte le funzioni devono essere verificate e testate prima del completamento.**
4. **Le nuove label devono essere tradotte in IT, RO, SV, DE, EN** e salvate in:
   ```sql
   traceability_rs.dbo.apptranslations (LanguageCode, TranslationKey, TranslationValue)
```

⚠️ Per il **Rumeno (RO)**: anteporre la lettera **N** al valore della traduzione
per garantire il salvataggio corretto dei caratteri diacritici.

Esempio corretto:

```sql
('ro', 'NPI_DOCS_BTN_OPEN', N'Gestionare Documente')
('it', 'NPI_DOCS_BTN_OPEN', 'Gestione Documenti')
('en', 'NPI_DOCS_BTN_OPEN', 'Document Management')
('sv', 'NPI_DOCS_BTN_OPEN', 'Dokumenthantering')
('de', 'NPI_DOCS_BTN_OPEN', 'Dokumentenverwaltung')
```


---

## 3. FILE DA MODIFICARE / CREARE

### 3.1 File esistente da modificare

- **`npi_project_management.py`** (o file equivalente che gestisce la form NPI —
verificare il nome esatto cercando la funzione `open_npi_project_management`)
    - Aggiungere il pulsante in fondo alla form
    - Collegare il pulsante alla nuova form


### 3.2 Nuovo file da creare

- **`npi_document_list.py`** — nuova form di gestione documenti NPI

---

## 4. MODIFICHE ALLA FORM ESISTENTE (npi_project_management.py)

### 4.1 Aggiunta pulsante

Aggiungere, in fondo alla form di gestione progetti NPI (dopo gli altri controlli esistenti),
un pulsante:

```python
btn_gestione_documenti = tk.Button(
    frame_bottom,
    text=get_translation('NPI_DOCS_BTN_OPEN'),  # usa sistema traduzioni esistente
    command=lambda: open_npi_document_list(current_npi_project_id),
    bg="#1E5FA3",
    fg="white",
    font=("Arial", 10, "bold"),
    width=25
)
btn_gestione_documenti.pack(side=tk.RIGHT, padx=10, pady=5)
```

⚠️ **Non modificare nessun altro elemento della form esistente.**
Il `current_npi_project_id` deve essere il parametro già presente nella form
che identifica il progetto NPI corrente.

---

## 5. NUOVA FORM: npi_document_list.py

### 5.1 Classe principale

```
class NPIDocumentListForm(tk.Toplevel)
```

Si apre come `Toplevel` (finestra figlia) passando `npi_project_id` come parametro obbligatorio.

### 5.2 Struttura UI della form

```
┌─────────────────────────────────────────────────────────────────┐
│  [Titolo: Documenti Progetto NPI - {NPI_CODE}]                  │
├──────────────────────────────────┬──────────────────────────────┤
│ Filtri/Ricerca                   │ Ordinamento                  │
│ [Campo testo ricerca] [🔍 Cerca] │ Ordina per: [ComboBox ▼]    │
│                                  │ [ASC] [DESC]                 │
├──────────────────────────────────┴──────────────────────────────┤
│                                                                  │
│  TreeView / Lista documenti                                     │
│  Colonne: #  | Tipo | Descrizione | Task | Data Doc | Inserito │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ [➕ Nuovo] [✏️ Modifica] [🗑️ Elimina]       [🔄 Aggiorna]      │
├─────────────────────────────────────────────────────────────────┤
│ RIEPILOGO (visibile solo se esistono documenti con valore):     │
│  Totale documenti: XX  |  Documenti con valore: XX  | Tot: €XX │
└─────────────────────────────────────────────────────────────────┘
```


### 5.3 Colonne della TreeView

| Colonna | Sorgente DB | Ordinabile | Note |
| :-- | :-- | :-- | :-- |
| \# | ID/RowNumber | No | Progressivo |
| Tipo documento | DocumentType | Sì | Es: PDF, Drawing, BOM... |
| Descrizione | DocumentDescription | Sì |  |
| Task | TaskName/TaskID | Sì | Task NPI di appartenenza |
| Data documento | DocumentDate | Sì | Data del documento |
| Data inserimento | InsertDate | Sì | Data caricamento |
| Valore | Value | Sì | Solo se != NULL e > 0 |
| Stato | DateOut IS NULL → Attivo | No | Mostra icona/colore |

**⚠️ I documenti con `DateOut IS NOT NULL` (soft-deleted) NON vengono mostrati
di default.** Aggiungere opzione checkbox "Mostra eliminati" per vederli (in grigio).

### 5.4 Filtri e ricerca

- **Campo testo libero**: cerca in Descrizione, Tipo, Task (LIKE '%...%')
- **ComboBox Tipo**: filtra per tipo documento (valori da DB)
- **ComboBox Task**: filtra per task NPI (valori legati al progetto)
- **ComboBox Ordinamento**: Data documento, Data inserimento, Tipo, Task, Valore
- **Radio/Toggle**: ASC / DESC
- **Checkbox**: Mostra documenti eliminati (DateOut IS NOT NULL)


### 5.5 Query base di caricamento

```sql
SELECT
    d.DocumentID,
    d.DocumentType,
    d.DocumentDescription,
    t.TaskName,
    d.DocumentDate,
    d.InsertDate,
    d.Value,
    d.DateOut,
    d.FilePath
FROM [traceability_rs].[dbo].[NPIDocuments] d  -- verifica nome tabella reale
LEFT JOIN [traceability_rs].[dbo].[NPITasks] t  -- verifica nome tabella reale
    ON d.TaskID = t.TaskID
WHERE d.NPIProjectID = @npi_project_id
  AND d.DateOut IS NULL  -- default: solo attivi
ORDER BY d.InsertDate DESC
```

⚠️ **Verificare i nomi esatti delle tabelle e colonne** consultando il DB
prima di scrivere qualsiasi query.

---

## 6. OPERAZIONI CRUD

### 6.1 NUOVO DOCUMENTO

- Apre una sotto-form (dialog `Toplevel`) con i campi:
    - Tipo documento (ComboBox, valori da DB)
    - Descrizione (Entry obbligatorio)
    - Task di appartenenza (ComboBox)
    - Data documento (DatePicker o Entry con validazione)
    - Valore (Entry numerico, opzionale)
    - File path / allegato (opzionale, con pulsante Sfoglia)
- Al salvataggio: INSERT con `InsertDate = GETDATE()`, `DateOut = NULL`


### 6.2 MODIFICA DOCUMENTO

- Doppio click sulla riga O pulsante Modifica
- Apre la stessa sotto-form pre-compilata
- Al salvataggio: UPDATE del record esistente
- ⚠️ Non modificare mai `InsertDate` originale
- ⚠️ Non modificare mai `DateOut` se già valorizzato


### 6.3 ELIMINAZIONE (SOFT DELETE)

- Pulsante Elimina con conferma messagebox
- Esegue:

```sql
UPDATE [NPIDocuments]
SET DateOut = GETDATE()
WHERE DocumentID = @doc_id
  AND NPIProjectID = @npi_project_id
```

- NON esegue DELETE fisico
- Il record rimane nella cronologia e visibile attivando "Mostra eliminati"


### 6.4 RIPRISTINO (solo se "Mostra eliminati" attivo)

- Pulsante Ripristina (visibile solo per record con DateOut valorizzato)
- Esegue:

```sql
UPDATE [NPIDocuments]
SET DateOut = NULL
WHERE DocumentID = @doc_id
```


---

## 7. RIEPILOGO IN FONDO ALLA FORM

Visibile solo se esistono documenti con campo `Value` valorizzato (non NULL, > 0):

```
┌─────────────────────────────────────────────────────┐
│  Totale documenti attivi: 15                        │
│  Documenti con valore:     8                        │
│  Valore totale:        € 12.450,00                  │
└─────────────────────────────────────────────────────┘
```

Il riepilogo si aggiorna ad ogni operazione (nuovo/modifica/elimina/ricerca).

```sql
SELECT
    COUNT(*) AS TotaleDocumenti,
    COUNT(CASE WHEN Value IS NOT NULL AND Value > 0 THEN 1 END) AS DocConValore,
    SUM(CASE WHEN Value IS NOT NULL THEN Value ELSE 0 END) AS ValoreTotale
FROM [traceability_rs].[dbo].[NPIDocuments]
WHERE NPIProjectID = @npi_project_id
  AND DateOut IS NULL
```


---

## 8. SCHEMA DB — COLONNA DateOut (se non esiste)

Se la tabella NPIDocuments non ha già la colonna `DateOut`, aggiungere:

```sql
-- Eseguire SOLO se la colonna non esiste
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'NPIDocuments'
      AND COLUMN_NAME = 'DateOut'
)
BEGIN
    ALTER TABLE [traceability_rs].[dbo].[NPIDocuments]
    ADD DateOut DATETIME NULL;
END
```


---

## 9. TRADUZIONI DA INSERIRE

File SQL da generare: `NPI_DOCUMENT_LIST_TRANSLATIONS.sql`

### Label necessarie (TranslationKey → testo base IT):

| TranslationKey | IT | EN | RO | SV | DE |
| :-- | :-- | :-- | :-- | :-- | :-- |
| NPI_DOCS_BTN_OPEN | Gestione Documenti | Document Management | N'Gestionare Documente' | Dokumenthantering | Dokumentenverwaltung |
| NPI_DOCS_TITLE | Documenti Progetto NPI | NPI Project Documents | N'Documente Proiect NPI' | NPI Projektdokument | NPI-Projektdokumente |
| NPI_DOCS_COL_TYPE | Tipo | Type | N'Tip' | Typ | Typ |
| NPI_DOCS_COL_DESC | Descrizione | Description | N'Descriere' | Beskrivning | Beschreibung |
| NPI_DOCS_COL_TASK | Task | Task | N'Activitate' | Uppgift | Aufgabe |
| NPI_DOCS_COL_DOCDATE | Data Documento | Document Date | N'Data Document' | Dokumentdatum | Dokumentdatum |
| NPI_DOCS_COL_INSDATE | Data Inserimento | Insert Date | N'Data Inserare' | Infogningsdatum | Eingabedatum |
| NPI_DOCS_COL_VALUE | Valore | Value | N'Valoare' | Värde | Wert |
| NPI_DOCS_BTN_NEW | Nuovo | New | N'Nou' | Ny | Neu |
| NPI_DOCS_BTN_EDIT | Modifica | Edit | N'Modifică' | Redigera | Bearbeiten |
| NPI_DOCS_BTN_DELETE | Elimina | Delete | N'Șterge' | Ta bort | Löschen |
| NPI_DOCS_BTN_REFRESH | Aggiorna | Refresh | N'Actualizează' | Uppdatera | Aktualisieren |
| NPI_DOCS_BTN_RESTORE | Ripristina | Restore | N'Restaurează' | Återställ | Wiederherstellen |
| NPI_DOCS_SEARCH | Cerca... | Search... | N'Caută...' | Sök... | Suchen... |
| NPI_DOCS_SORT_BY | Ordina per | Sort by | N'Sortează după' | Sortera efter | Sortieren nach |
| NPI_DOCS_SHOW_DELETED | Mostra eliminati | Show deleted | N'Afișează șterse' | Visa borttagna | Gelöschte anzeigen |
| NPI_DOCS_SUMMARY_TOTAL | Totale documenti | Total documents | N'Total documente' | Totala dokument | Dokumente gesamt |
| NPI_DOCS_SUMMARY_WITH_VAL | Documenti con valore | Documents with value | N'Documente cu valoare' | Dokument med värde | Dokumente mit Wert |
| NPI_DOCS_SUMMARY_TOT_VAL | Valore totale | Total value | N'Valoare totală' | Totalvärde | Gesamtwert |
| NPI_DOCS_CONFIRM_DELETE | Confermare eliminazione? | Confirm deletion? | N'Confirmați ștergerea?' | Bekräfta borttagning? | Löschen bestätigen? |
| NPI_DOCS_DIALOG_NEW | Nuovo Documento | New Document | N'Document Nou' | Nytt dokument | Neues Dokument |
| NPI_DOCS_DIALOG_EDIT | Modifica Documento | Edit Document | N'Modificare Document' | Redigera dokument | Dokument bearbeiten |
| NPI_DOCS_STATUS_ACTIVE | Attivo | Active | N'Activ' | Aktiv | Aktiv |
| NPI_DOCS_STATUS_DELETED | Eliminato | Deleted | N'Șters' | Borttagen | Gelöscht |

### Formato INSERT SQL (da usare per ogni riga):

```sql
-- Sostituire N'...' per il rumeno come da convenzione del progetto
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.apptranslations
               WHERE LanguageCode = 'it' AND TranslationKey = 'NPI_DOCS_BTN_OPEN')
    INSERT INTO traceability_rs.dbo.apptranslations (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'NPI_DOCS_BTN_OPEN', 'Gestione Documenti');
```


---

## 10. CHECKLIST DI VERIFICA PRE-CONSEGNA

- [ ] Verificato nome esatto della form `open_npi_project_management` nel codice
- [ ] Verificato nome esatto tabella NPIDocuments (o equivalente) nel DB
- [ ] Verificato nome esatto tabella NPITasks (o equivalente) nel DB
- [ ] Verificata struttura colonne tabella NPIDocuments
- [ ] Colonna `DateOut` presente o aggiunta con ALTER TABLE idempotente
- [ ] Connessioni DB usano **solo** `db_connection.py` / `database_config.py` esistenti
- [ ] Nessun parametro esistente modificato nella form originale
- [ ] Pulsante aggiunto in fondo senza alterare layout esistente
- [ ] Form `NPIDocumentListForm` apre correttamente con `npi_project_id`
- [ ] Caricamento lista documenti filtra per `NPIProjectID` e `DateOut IS NULL`
- [ ] Ordinamento funzionante per tutte le colonne previste
- [ ] Ricerca/filtro funzionante
- [ ] Nuovo documento: INSERT corretto con tutti i campi obbligatori
- [ ] Modifica documento: UPDATE corretto, InsertDate non toccato
- [ ] Soft delete: UPDATE DateOut = GETDATE(), NO DELETE fisico
- [ ] Ripristino: UPDATE DateOut = NULL funzionante
- [ ] Riepilogo visibile solo se esistono documenti con valore
- [ ] Riepilogo si aggiorna dinamicamente ad ogni operazione
- [ ] Tutte le label usano il sistema traduzioni esistente
- [ ] File SQL traduzioni generato con tutte le 5 lingue (it/ro/en/sv/de)
- [ ] Prefisso N'...' per tutte le traduzioni in Rumeno
- [ ] Testato con dati reali (almeno creazione, modifica, eliminazione, ripristino)
- [ ] Testato con progetto NPI senza documenti (lista vuota, nessun riepilogo)
- [ ] Testato con progetto NPI con documenti senza valore (nessun riepilogo)

---

## 11. NOTE TECNICHE AGGIUNTIVE

- Usare **`messagebox.askyesno()`** per conferme eliminate
- Il widget lista principale deve essere **`ttk.Treeview`** con scrollbar verticale
- La form si apre con **`grab_set()`** (modale) per evitare operazioni parallele
sulla form NPI principale durante la gestione documenti
- Gestire eccezioni DB con **try/except** e messagebox di errore all'utente
- Tutti i log di errore seguono il pattern del progetto esistente
- La form deve essere **ridimensionabile** con comportamento responsive della TreeView
- Dimensione minima consigliata: 900x600 px

```

***

Questo breakdown document è strutturato per dare a Claude Sonnet tutte le informazioni necessarie per implementare la funzionalità senza ambiguità . I punti chiave incorporati:

- **Vincoli DB**: nessuna nuova connessione, uso esclusivo di `db_connection.py` e `database_config.py` già presenti nel repository 
- **Soft delete**: campo `DateOut DATETIME NULL` con ALTER TABLE idempotente (verifica esistenza prima di aggiungere)
- **Traduzioni**: tabella completa con 5 lingue (IT/EN/RO/SV/DE) e prefisso `N'...'` per il rumeno
- **Checklist**: 20 verifiche da completare prima della consegna per garantire che tutto funzioni```

