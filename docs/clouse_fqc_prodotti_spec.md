# Specifica funzionale e tecnica — Nuovo menu **FQC prodotti** per Document Management

## Obiettivo
Lo scopo dell’intervento è aggiungere al programma **Document Management** un nuovo menu denominato **FQC prodotti**, dedicato alla gestione delle checklist di controllo sui prodotti finiti per specifici clienti e prodotti.[cite:1]

Il nuovo menu dovrà essere inserito nel file `main.py`, subito dopo il blocco che richiama `self._update_line_validation_submenu()` e dopo la voce opzionale **Piano produzione**, in prossimità della riga 15958 indicata nella richiesta.[cite:1]

## Posizionamento del menu
Il nuovo comando dovrà essere aggiunto nel menu `self.declarations_submenu` con etichetta visualizzata **FQC prodotti** e con apertura della relativa form dedicata.[cite:1]

Esempio di riferimento nel contesto attuale:

```python
self._update_line_validation_submenu()
# Piano produzione — sotto Validazione linea, solo se abilitato
if getattr(self, '_plan_check_mode', 'False') != 'False':
    self.declarations_submenu.add_command(
        label=self.lang.get('piano_produzione', "Piano produzione"),
        command=self.open_plan_discrepancy_with_login
    )
```

Subito dopo tale sezione dovrà essere introdotta una nuova voce menu per l’apertura della maschera **FQC prodotti**.[cite:1]

## Flusso operativo utente
La nuova funzione dovrà essere molto semplice da usare, con aspetto professionale, integrazione grafica del file `logo.png` e percorso guidato per l’utente.[cite:1]

Il flusso minimo previsto è il seguente:[cite:1]

1. Apertura menu **FQC prodotti**.[cite:1]
2. Selezione del cliente tramite combo editabile.[cite:1]
3. Popolamento del combo prodotti in base al cliente selezionato.[cite:1]
4. Visualizzazione delle checklist associate al prodotto.[cite:1]
5. Esecuzione e registrazione dei controlli item per item.[cite:1]
6. Memorizzazione dell’esito con utente, data, eventuale nota e successiva gestione feedback cliente.[cite:1]

## Selezione clienti e prodotti
Alla prima apertura della form, l’utente dovrà selezionare il cliente; inizialmente i casi previsti sono **AROS** ed **EI**, ma il sistema dovrà essere predisposto per clienti futuri utilizzando il database come fonte dati del combo.[cite:1]

Query per il caricamento clienti:[cite:1]

```sql
select IDClient, ClientName
from Clients
where isClient = 1
order by ClientName;
```

Dopo la selezione del cliente, il combo prodotti dovrà essere popolato tramite la seguente query parametrica:[cite:1]

```sql
select IDProduct, ProductCode
from Products
where IDClient = ?
order by ProductCode;
```

Per l’alimentazione definitiva del combo prodotti, il sistema dovrà inoltre verificare in tracciabilità quali siano i prodotti effettivamente soggetti a controllo; la query specifica sarà fornita successivamente.[cite:1]

## Struttura dati
La gestione della funzione si basa sulle tabelle del database `Traceability_RS` nello schema `chk`, con distinzione tra testata checklist, righe checklist, log esecuzione e feedback successivi.[cite:1]

### Testata checklist
La tabella di definizione delle checklist è:

```sql
SELECT [ProductCheckListId],
       [CheckListName],
       [IdProduct],
       [DateIn],
       [DateOut]
FROM [Traceability_RS].[chk].[ProductCheckLists];
```

Regole applicative:[cite:1]
- `IdProduct` è la chiave verso `Traceability_RS.dbo.Products.IdProduct`.[cite:1]
- `DateOut` gestisce il **soft delete** della checklist.[cite:1]
- `CheckListName` contiene il nome funzionale della checklist associata al prodotto.[cite:1]

### Righe checklist
La tabella di dettaglio degli elementi da controllare è:

```sql
SELECT [ProductCheckListDataId],
       [ProductCheckListId],
       [ItemToCheck],
       [ItemToCheckNumber],
       [PictureToCheck],
       [DateOut],
       [DateSys]
FROM [Traceability_RS].[chk].[ProductCheckListDatas];
```

Regole applicative:[cite:1]
- `ProductCheckListId` è la chiave verso `[chk].[ProductCheckLists]`.[cite:1]
- `ItemToCheck` descrive il componente o l’area da verificare.[cite:1]
- `ItemToCheckNumber` è progressivo in base 10 ed è usato per ordinare gli item.[cite:1]
- `PictureToCheck` memorizza il riferimento alla fotografia esplicativa dell’item.[cite:1]
- Ogni riga checklist deve avere obbligatoriamente testo descrittivo e fotografia associata.[cite:1]
- `DateOut` abilita il soft delete delle singole righe.[cite:1]

### Log delle verifiche eseguite
La tabella di registrazione dei controlli effettuati è:

```sql
SELECT [ProductCheckListDataLogId],
       [ProductCheckListDataId],
       [IsOK],
       [DateCheckList],
       [User],
       [NotOkNote]
FROM [Traceability_RS].[chk].[ProductCheckListDataLogs];
```

Regole applicative:[cite:1]
- `ProductCheckListDataId` è la chiave verso `[Traceability_RS].[chk].[ProductCheckListDatas]`.[cite:1]
- `IsOK` è un bit che rappresenta l’esito del controllo.[cite:1]
- Se `IsOK = 0`, la nota `NotOkNote` è obbligatoria.[cite:1]
- `User` deve riportare il nome dell’utente autenticato al login.[cite:1]
- `DateCheckList` registra data e ora del controllo eseguito.[cite:1]

### Feedback cliente
La tabella dei feedback successivi è:

```sql
SELECT [ProductCheckListDataLogFeedBackId],
       [ProductCheckListDataLogId],
       [FeedBack],
       [FeedBackPicture],
       [FeedBackDate],
       [FeedBackFrom],
       [DateSys]
FROM [Traceability_RS].[chk].[ProductCheckListDataLogFeedBacks];
```

Regole applicative:[cite:1]
- La compilazione avviene separatamente, sotto login `_execute_authenticated_login`, in caso di feedback negativo da parte del cliente.[cite:1]
- `ProductCheckListDataLogId` è la chiave verso `[Traceability_RS].[chk].[ProductCheckListDataLogs]`.[cite:1]
- Il feedback potrà comprendere testo, immagine, data e soggetto che lo ha emesso.[cite:1]

## Funzioni richieste
Il modulo dovrà prevedere almeno tre aree funzionali.[cite:1]

### 1. Esecuzione checklist FQC prodotti
La form principale dovrà consentire all’operatore di selezionare cliente e prodotto, caricare la checklist attiva del prodotto e registrare l’esito di ogni item.[cite:1]

Per ogni riga dovranno essere visibili almeno:[cite:1]
- Numero progressivo item.[cite:1]
- Descrizione `ItemToCheck`.[cite:1]
- Immagine esplicativa `PictureToCheck`.[cite:1]
- Selettore esito **OK / Not OK**.[cite:1]
- Campo nota obbligatorio in caso di **Not OK**.[cite:1]

Al salvataggio, il sistema dovrà generare una riga nella tabella `[chk].[ProductCheckListDataLogs]` per ogni item verificato.[cite:1]

### 2. Manutenzione anagrafica checklist
Dovrà esistere una form dedicata alla creazione e manutenzione delle checklist, accessibile solo sotto `_execute_authorized_login`.[cite:1]

La form dovrà permettere di:[cite:1]
- Selezionare un prodotto (`IDProduct`).[cite:1]
- Inserire il nome della checklist in `CheckListName`.[cite:1]
- Creare la testata in `[Traceability_RS].[chk].[ProductCheckLists]`.[cite:1]
- Inserire le righe in `[Traceability_RS].[chk].[ProductCheckListDatas]`.[cite:1]
- Associare obbligatoriamente una foto a ciascuna descrizione.[cite:1]
- Modificare righe esistenti.[cite:1]
- Aggiungere nuovi item.[cite:1]
- Eseguire cancellazione logica tramite `DateOut` sia in testata sia nelle righe.[cite:1]

La stessa maschera dovrà quindi gestire creazione, modifica e soft delete in modo integrato e intuitivo.[cite:1]

### 3. Gestione feedback cliente
Dovrà essere disponibile una form separata, protetta da `_execute_authenticated_login`, per registrare i feedback negativi del cliente sulle verifiche eseguite.[cite:1]

Questa funzione dovrà consentire di associare il feedback al log originario, registrando testo, eventuale immagine, data del feedback e origine del feedback stesso.[cite:1]

## Regole di business
Il sistema dovrà applicare le seguenti regole:[cite:1]

- Una checklist è valida se `DateOut` è null sia in testata sia nelle righe.[cite:1]
- Gli item devono essere mostrati in ordine crescente di `ItemToCheckNumber`.[cite:1]
- Ogni item deve avere fotografia obbligatoria in fase di definizione checklist.[cite:1]
- In fase di controllo, se l’esito è **Not OK**, la nota è obbligatoria.[cite:1]
- Il nome utente deve essere sempre salvato nel log dei controlli.[cite:1]
- Le funzioni di manutenzione checklist devono essere disponibili solo a utenti autorizzati.[cite:1]
- Le funzioni di feedback devono essere disponibili solo dopo autenticazione.[cite:1]

## Cross-check con tracciabilità
Per alimentare correttamente il combo dei prodotti e per determinare cosa debba essere controllato, il sistema dovrà eseguire un controllo incrociato con i dati di tracciabilità.[cite:1]

In particolare, il programma dovrà verificare se esistono prodotti presenti in `chk.ProductCheckLists` e confrontarli con i prodotti risultanti dalla tracciabilità; tutti i prodotti previsti nella lista dovranno risultare verificati.[cite:1]

La query esatta per il recupero dei prodotti da controllare lato tracciabilità non è ancora disponibile e sarà fornita in un secondo momento.[cite:1]

## Email di fine turno
Alle ore **15:30** e **23:30** il sistema dovrà inviare un’email automatica utilizzando la chiave `Sys_check_final_product`.[cite:1]

L’email dovrà contenere un resoconto sintetico con:[cite:1]
- Prodotti previsti da verificare.[cite:1]
- Prodotti effettivamente verificati.[cite:1]
- Eventuali prodotti mancanti o ancora da verificare.[cite:1]
- Eventuali anomalie o controlli con esito negativo rilevanti.[cite:1]

## Requisiti UI/UX
L’interfaccia dovrà essere progettata con priorità alla facilità d’uso, velocità operativa e chiarezza visiva.[cite:1]

Requisiti minimi:[cite:1]
- Aspetto professionale coerente con l’applicazione esistente.[cite:1]
- Presenza del `logo.png` nelle form principali.[cite:1]
- Combo editabili per agevolare la ricerca rapida di cliente e prodotto.[cite:1]
- Griglia checklist leggibile con immagini di supporto ben visibili.[cite:1]
- Pulsanti chiari per salvataggio, modifica, aggiunta e cancellazione logica.[cite:1]
- Riduzione al minimo dei passaggi per l’operatore di linea o controllo qualità.[cite:1]

## Proposta tecnica di implementazione
A livello applicativo si suggerisce di introdurre almeno i seguenti metodi o equivalenti:[cite:1]

| Componente | Scopo |
|---|---|
| `open_fqc_products_with_login()` | Apertura menu con autenticazione o controllo accessi.[cite:1] |
| `open_fqc_products_form()` | Form principale di esecuzione checklist.[cite:1] |
| `open_fqc_products_master_with_login()` | Accesso protetto alla manutenzione checklist.[cite:1] |
| `open_fqc_products_master_form()` | Maschera di creazione/modifica testata e righe checklist.[cite:1] |
| `open_fqc_products_feedback_with_login()` | Accesso autenticato alla gestione feedback.[cite:1] |
| `open_fqc_products_feedback_form()` | Maschera per inserimento feedback cliente.[cite:1] |
| `load_clients_for_fqc()` | Caricamento elenco clienti.[cite:1] |
| `load_products_for_fqc(id_client)` | Caricamento prodotti per cliente.[cite:1] |
| `load_checklist_for_product(id_product)` | Caricamento checklist attiva e relative righe.[cite:1] |
| `save_product_checklist_logs()` | Scrittura esiti in `[chk].[ProductCheckListDataLogs]`.[cite:1] |
| `send_final_product_check_email()` | Invio email di riepilogo ai turni previsti.[cite:1] |

## Punti aperti
Restano da definire i seguenti elementi prima dello sviluppo definitivo:[cite:1]

- Query esatta di tracciabilità per identificare i prodotti che richiedono controllo.[cite:1]
- Regole di selezione della checklist nel caso in cui un prodotto abbia più versioni storiche.[cite:1]
- Destinatari email associati alla chiave `Sys_check_final_product`.[cite:1]
- Layout esatto delle form e comportamento atteso in caso di checklist incompleta.[cite:1]
- Eventuale gestione upload fisico delle immagini e percorso di salvataggio di `PictureToCheck` e `FeedBackPicture`.[cite:1]

## Risultato atteso
Al termine dell’intervento, il modulo **Document Management** dovrà consentire di configurare checklist per prodotto finito, eseguirle in modo guidato, tracciare gli esiti per utente e data, raccogliere eventuali feedback cliente e inviare un riepilogo automatico di fine turno sullo stato dei controlli effettuati e mancanti.[cite:1]
