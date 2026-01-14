# Funzionalità Verifica LabelCode nei Reclami

## Data Implementazione
11 Gennaio 2026

## Descrizione
È stata implementata una nuova funzionalità nel modulo `add_complaint.py` che permette di verificare i labelcode inseriti nei dettagli dei reclami, confrontandoli con il prodotto specificato nella testata del reclamo.

## Modifiche Implementate

### 1. File Modificato: `add_complaint.py`

#### Classe `DetailEditorWindow`
La finestra di editing dei dettagli è stata modificata per includere:

##### Nuovi Attributi
- `labelcode_verified`: Booleano che indica se il labelcode è stato verificato
- `query_results`: Memorizza i risultati della query per eventuali usi futuri

##### Modifiche all'Interfaccia
- **Campo LabelCode**: Aggiunto un bottone "Conferma" accanto al campo di input
- **Frame dei Risultati**: Creati due frame collassabili per visualizzare:
  - **Fasi di Produzione**: Mostra ordine, posizione fase, nome fase, stato board, risultato scansione e data
  - **Riparazioni**: Mostra data riparazione, difetto e area (se presenti)

##### Nuovi Metodi

###### `_verify_labelcode()`
Esegue la verifica del labelcode con i seguenti step:
1. Valida che il campo labelcode non sia vuoto
2. Esegue la query SQL fornita dall'utente per recuperare i dati di produzione
3. Verifica che l'IDProduct trovato corrisponda a quello della testata del reclamo
4. Se **non corrisponde**: 
   - Mostra un messaggio di errore multilingua
   - Riporta il focus sul campo labelcode
   - Seleziona tutto il testo per una facile correzione
5. Se **corrisponde**:
   - Disabilita il campo labelcode e il bottone conferma
   - Allarga la finestra da 600x500 a 1200x700
   - Mostra i risultati divisi in fasi e riparazioni
   - Popola le due treeview con i dati

###### `_populate_results(results)`
Popola le due treeview separando i dati:
- **Fasi**: Mostra tutte le fasi attraversate dal board (senza duplicati)
- **Riparazioni**: Mostra solo le riparazioni effettive (verifica che ci siano dati nelle colonne DefectNameRO, DefectArea o RepairDate)
- Se non ci sono riparazioni, mostra "Nessuna riparazione"

### 2. Query SQL Implementata

```sql
select distinct pr.IDProduct,
pr.ProductCode,
o.OrderNumber, l.LabelCod, dbo.BoardState(b.BoardState) as BoardState,
p.IDPhase, p.PhaseName, op.PhasePosition,
iif (s.IsPass=0,'FAIL', 'PASS') as ScanResult, s.ScanTimeFinish,  
iif (sd.IsPass=0,'FAIL', 'PASS') as RepairResult, sd.StopTime as RepairDate,  
d.DefectNameRO, a.AreaName as DefectArea
from Scannings s
inner join LabelCodes l on s.IDBoard = l.IDBoard
inner join Boards b on b.IDBoard = s.IDBoard
inner join OrderPhases op on s.IDOrderPhase =op.IDOrderPhase
inner join Orders o on o.IDOrder = op.IDOrder
inner join Phases p on p.IDPhase = op.IDPhase
left join ScanDefects sd on  sd.IDScan = s.IDScan
left join ScanDefectDetails sdd on sd.IDScanDefect = sdd.IDScanDefect
left join Defects d on d.IDDefect = sdd.IDDefect
left join Areas a on a.IDArea = sdd.IDArea
inner join Products Pr on pr.IDProduct=o.IDProduct
cross apply 
(select top 1 PhasePosition from 
OrderPhases 
where OrderPhases.IDOrder= o.IDOrder 
and OrderPhases.IDPhase= op.IDPhase
order by OrderPhases.PhasePosition ) pp
where l.LabelCod = ?
and op.PhasePosition>= pp.PhasePosition
order by op.PhasePosition, s.ScanTimeFinish
```

**Struttura dei risultati:**
- 0: IDProduct
- 1: ProductCode
- 2: OrderNumber
- 3: LabelCod
- 4: BoardState
- 5: IDPhase
- 6: PhaseName
- 7: PhasePosition
- 8: ScanResult
- 9: ScanTimeFinish
- 10: RepairResult
- 11: RepairDate
- 12: DefectNameRO
- 13: DefectArea

### 3. File SQL Creato: `LABELCODE_VERIFICATION_TRANSLATIONS.sql`

Contiene tutte le traduzioni necessarie in 5 lingue (IT, RO, EN, DE, SV):

#### Chiavi di Traduzione Aggiunte
- `btn_confirm`: Testo del bottone conferma
- `lbl_phases`: Titolo frame fasi
- `lbl_repairs`: Titolo frame riparazioni
- `col_order`: Intestazione colonna ordine
- `col_phase_pos`: Intestazione colonna posizione
- `col_phase`: Intestazione colonna fase
- `col_board_state`: Intestazione colonna stato board
- `col_scan_result`: Intestazione colonna risultato
- `col_scan_time`: Intestazione colonna data
- `col_repair_date`: Intestazione colonna data riparazione
- `col_area`: Intestazione colonna area
- `err_labelcode_required`: Errore campo vuoto
- `err_labelcode_not_found`: Errore labelcode non trovato
- `err_labelcode_wrong_product`: Errore prodotto non corrispondente (con messaggio dettagliato multiriga)
- `no_repairs`: Messaggio per assenza di riparazioni

## Flusso Operativo

1. L'utente clicca su "Aggiungi Riga" nella sezione dettagli
2. Si apre il `DetailEditorWindow` con dimensioni 600x500
3. L'utente inserisce il labelcode nel primo campo
4. L'utente clicca "Conferma"
5. Il sistema esegue la query e verifica l'IDProduct
6. **Scenario A - IDProduct NON corrisponde:**
   - Mostra messaggio di errore multilingua
   - Focus torna al campo labelcode
   - Il testo viene selezionato per facilitare la correzione
   - L'utente può correggere e riprovare
7. **Scenario B - IDProduct corrisponde:**
   - La finestra si allarga a 1200x700
   - Campo labelcode e bottone conferma vengono disabilitati
   - Appare il frame "Fasi" con la treeview popolata
   - Appare il frame "Riparazioni" con la treeview popolata (o "Nessuna riparazione")
   - L'utente può completare gli altri campi del dettaglio

## Note Tecniche

- La finestra si allarga automaticamente solo dopo la verifica positiva
- I risultati vengono deduplucati per evitare righe ripetute
- Il campo RepairResult non viene mostrato nelle riparazioni (come richiesto dall'utente)
- Il logging è stato implementato per tracciare tutte le operazioni di verifica
- La gestione degli errori è robusta con try-catch e messaggi user-friendly

## Installazione

1. Eseguire lo script `LABELCODE_VERIFICATION_TRANSLATIONS.sql` sul database `Traceability_RS`
2. Riavviare l'applicazione per caricare le nuove traduzioni
3. Le modifiche al codice sono già attive nel file `add_complaint.py`

## Test Consigliati

1. Inserire un labelcode valido appartenente al prodotto del reclamo
2. Inserire un labelcode valido ma di un prodotto diverso
3. Inserire un labelcode inesistente
4. Verificare che i dati delle fasi vengano visualizzati correttamente
5. Verificare che le riparazioni vengano visualizzate solo se presenti
6. Testare in tutte le lingue supportate (IT, RO, EN, DE, SV)
