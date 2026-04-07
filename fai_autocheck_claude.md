# Specifica funzionale e tecnica — Autocheck FAI da PlanningMachine

## Obiettivo
Implementare una funzione automatica collegata al comando di menu `open_line_validations_with_login` per identificare con anticipo i controlli FAI obbligatori sui template con `Autocheck = true`, avvisare i responsabili di linea presenti in turno e registrare le mancate verifiche.

## Contesto applicativo
Nel programma, gli operatori compilano le risposte delle form FAI predefinite dai template presenti in:

```sql
SELECT TOP (1000)
      [FaiTemplateId],
      [NrDocument],
      [Revision],
      [FaiTitle],
      [RevisionDate],
      [Autocheck],
      p.phasename,
      p.idphase
FROM [Traceability_RS].[fai].[FaiTemplates] f
INNER JOIN Traceability_RS.dbo.Phases p
    ON p.idphase = f.idphase;
```

Alcuni template hanno `Autocheck = true`. Per questi template il sistema deve individuare in modo automatico le produzioni pianificate e notificare i responsabili di linea con anticipo operativo sufficiente.

## Regola di business principale
Il sistema deve:

1. verificare ogni 30 minuti il file Excel più recente presente in `T:\\Planning\\`;
2. usare esclusivamente il tab `PlanningMachine`;
3. considerare solo le righe la cui data/ora in colonna `O` (`Order Phase Plan Start`) rientra nel range delle prossime 4 ore;
4. considerare solo le righe la cui `PHASE` in colonna `E` corrisponde a una fase associata a un template FAI con `Autocheck = true`;
5. verificare se per quella combinazione ordine/fase la produzione non è ancora stata iniziata;
6. se la quantità prodotta è `0` oppure `NULL`, inviare una email professionale e perentoria ai responsabili di linea, con invio anticipato di 3 ore rispetto all'inizio produzione;
7. registrare l'evento in una tabella dedicata per successive verifiche di conformità.

## Origine dati pianificazione
### Cartella da monitorare
Percorso:

```text
T:\Planning\
```

### Regola di scelta file
Deve essere sempre utilizzato il file Excel più recente disponibile nella cartella, indipendentemente dal nome del file.

La selezione deve quindi avvenire per data di ultima modifica file, non per naming convention.

### Tab da utilizzare
Tab obbligatorio:

```text
PlanningMachine
```

### Colonne rilevanti
- Colonna `E` → `PHASE`
- Colonna `K` → `Order Number`
- Colonna `O` → `Order Phase Plan Start`

## Individuazione delle fasi soggette ad autocheck
L'elenco delle fasi da monitorare deriva dai template FAI con `Autocheck = true`.

Query di riferimento:

```sql
SELECT
      f.[FaiTemplateId],
      f.[NrDocument],
      f.[Revision],
      f.[FaiTitle],
      f.[RevisionDate],
      f.[Autocheck],
      p.phasename,
      p.idphase
FROM [Traceability_RS].[fai].[FaiTemplates] f
INNER JOIN Traceability_RS.dbo.Phases p
    ON p.idphase = f.idphase
WHERE f.Autocheck = 1;
```

La colonna `PHASE` del file Excel deve essere confrontata con `p.phasename`.

Il match richiesto è di uguaglianza esatta.

## Risoluzione della fase tecnica
Per ottenere `IdPhase` a partire dal valore testuale della colonna `E` del file Excel:

```sql
SELECT IdPhase
FROM Traceability_RS.dbo.Phases
WHERE PhaseName = @PhaseName;
```

Dove `@PhaseName` è il valore della colonna `E` del foglio `PlanningMachine`.

## Verifica avvio produzione
Per verificare che la produzione della fase non sia ancora stata avviata, usare la query seguente:

```sql
SELECT COUNT(DISTINCT Traceability_RS.dbo.BoardLabels(Scannings.IDBoard)) AS Qty
FROM Traceability_RS.dbo.Scannings
INNER JOIN Traceability_RS.dbo.OrderPhases
    ON Scannings.IDOrderPhase = OrderPhases.IDOrderPhase
INNER JOIN Traceability_RS.dbo.Orders
    ON OrderPhases.IDOrder = Orders.IDOrder
INNER JOIN Traceability_RS.dbo.Phases
    ON OrderPhases.IDPhase = Phases.IDPhase
INNER JOIN Traceability_RS.dbo.Boards
    ON Boards.IDBoard = Scannings.IDBoard
WHERE Scannings.ScanTimeFinish BETWEEN GETDATE() - 500
    AND CAST(CAST(CAST(GETDATE() AS date) AS nvarchar(10)) + ' 07:30:00' AS smalldatetime)
    AND Orders.OrderNumber = @OrderNumber
    AND Phases.IdPhase = @IdPhase;
```

Parametri:
- `@OrderNumber` = valore della colonna `K` del file Excel
- `@IdPhase` = valore ricavato dalla query su `Traceability_RS.dbo.Phases`

### Interpretazione del risultato
- Se `Qty > 0`, la produzione risulta già avviata e non deve partire la notifica FAI preventiva.
- Se `Qty = 0` oppure `Qty IS NULL`, il sistema deve generare la notifica email, purché la riga rientri nella finestra temporale utile e la fase sia soggetta ad autocheck.

## Finestra temporale di controllo
Il job deve essere eseguito ogni 30 minuti.

Ad ogni esecuzione deve:
- leggere il file Excel più recente;
- filtrare le righe con `Order Phase Plan Start` compreso tra `NOW` e `NOW + 4 ore`;
- per ciascuna riga valida valutare se l'invio email deve essere effettuato in modo da avvisare i responsabili circa 3 ore prima dell'inizio produzione.

### Nota operativa
Poiché il controllo è schedulato ogni 30 minuti e la finestra di osservazione è di 4 ore, il sistema deve gestire una logica anti-duplicazione delle notifiche, così da evitare invii ripetuti per lo stesso ordine/fase/template.

## Ricerca destinatari email
Gli indirizzi email dei dipendenti devono essere ricavati con la query seguente:

```sql
SELECT DISTINCT
       e.EmployeeSurname + ' ' + e.EmployeeName AS Employee,
       a.WorkEmail,
       f.FunctionCode
FROM Employee.dbo.EmployeeHireHistory h
LEFT JOIN Employee.dbo.Employees e
    ON e.EmployeeId = h.EmployeeId
   AND h.EmployerId = 2
   AND h.EndWorkDate IS NULL
INNER JOIN Employee.dbo.EmployeeCdcStories ec
    ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
   AND ec.DateOut IS NULL
INNER JOIN Employee.dbo.Functions f
    ON ec.FunctionId = f.FunctionId
INNER JOIN Employee.dbo.CdcSub cs
    ON ec.SubCdcId = cs.SubCdcId
INNER JOIN Employee.dbo.EmployeeAddress a
    ON e.EmployeeId = a.EmployeeId
   AND a.DateOut IS NULL
WHERE cs.SubCdcDescription = 'pthm'
  AND f.FunctionCode BETWEEN 21 AND 80
ORDER BY f.FunctionCode;
```

### Regola di composizione destinatari
- Tutti i record con `FunctionCode < 60` devono essere inseriti in `TO`, ma solo se presenti in turno.
- Tutti i record con `FunctionCode >= 60` devono essere inseriti sempre in `CC`.

## Verifica presenza in turno
Prima di inserire un destinatario in `TO`, il sistema deve verificare che il dipendente sia effettivamente presente al lavoro al momento dell'invio.

Per ottenere anche `IDEmployee`, usare questa query:

```sql
SELECT
    e.EmployeeSurname + ' ' + e.EmployeeName AS Employee,
    a.WorkEmail,
    f.FunctionCode,
    ee.IDEmployee,
    cs.SubCdcDescription
FROM Employee.dbo.EmployeeHireHistory h
LEFT JOIN Employee.dbo.Employees e
    ON e.EmployeeId = h.EmployeeId
   AND h.EmployerId = 2
   AND h.EndWorkDate IS NULL
INNER JOIN Employee.dbo.EmployeeCdcStories ec
    ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
   AND ec.DateOut IS NULL
INNER JOIN Employee.dbo.Functions f
    ON ec.FunctionId = f.FunctionId
INNER JOIN Employee.dbo.CdcSub cs
    ON ec.SubCdcId = cs.SubCdcId
INNER JOIN Employee.dbo.EmployeeAddress a
    ON e.EmployeeId = a.EmployeeId
   AND a.DateOut IS NULL
INNER JOIN Timeclocking.dbo.Employee ee
    ON ee.UniqueID COLLATE database_default = e.EmployeeNID
   AND ee.DataStop IS NULL
WHERE cs.SubCdcDescription = 'pthm'
  AND f.FunctionCode BETWEEN 21 AND 80
ORDER BY f.FunctionCode;
```

### SP per controllo presenza
Per ogni dipendente con `FunctionCode > 20 AND FunctionCode < 60` deve essere eseguita la stored procedure:

```sql
EXEC [dbo].[GetEmployeesTimeclockReal] @from, @to, @IDEmployee;
```

### Regola per `@from` e `@to`
- Se l'ora di esecuzione del processo è precedente alle `15:30`, `@from` deve essere impostato alla data del giorno con orario `06:40` (cioè 50 minuti prima delle 07:30).
- Se l'ora di esecuzione del processo è uguale o successiva alle `15:30`, `@from` deve essere impostato alla data del giorno con orario `16:20` (cioè 50 minuti dopo le 15:30).
- `@to` deve essere valorizzato con il timestamp corrente di esecuzione, oppure con un estremo superiore coerente con la logica già adottata nel sistema di timbratura.

### Interpretazione presenza
- Se il risultato della stored procedure non è `NULL`, il dipendente è considerato presente e può essere inserito nei destinatari `TO`.
- Se il risultato è `NULL`, il dipendente non deve essere inserito nei destinatari `TO`.
- I dipendenti con `FunctionCode >= 60` devono essere inseriti sempre in `CC`, indipendentemente dalla presenza.

## Regole finali di invio email
Una email deve essere inviata quando tutte le condizioni seguenti sono vere:

- esiste una riga nel tab `PlanningMachine` con `Order Phase Plan Start` nelle prossime 4 ore;
- la `PHASE` della riga coincide esattamente con una fase associata a un template con `Autocheck = true`;
- la query di verifica produzione per quell'`Order Number` e quell'`IdPhase` restituisce `0` oppure `NULL`;
- non è già stata inviata una notifica valida per la stessa combinazione ordine/fase/template nella stessa finestra di controllo.

## Contenuto email richiesto
La email deve avere tono molto professionale e perentorio.

### Oggetto proposto
```text
Azione richiesta — Esecuzione controllo FAI prima dell'avvio produzione ordine {OrderNumber}
```

### Corpo proposto
```text
Gentili Responsabili di Linea,

si comunica che per l'ordine {OrderNumber}, fase {PhaseName}, è previsto a breve l'avvio della produzione secondo pianificazione.

Dalle verifiche automatiche effettuate, il controllo FAI associato al template obbligatorio con gestione Autocheck non risulta ancora eseguito.

Si richiede pertanto di provvedere con la massima urgenza all'esecuzione e registrazione del controllo FAI prima dell'inizio della produzione.

Orario pianificato di avvio fase: {PlannedStart}
Template FAI applicabile: {FaiTitle}
Documento / Revisione: {NrDocument} / {Revision}

La presente comunicazione costituisce avviso operativo preventivo. L'eventuale mancata esecuzione del controllo sarà registrata ai fini di verifica del rispetto della procedura.

Cordiali saluti,
Sistema automatico di controllo FAI
```

## Tabella di tracciatura da creare
È richiesta una tabella in `Traceability_TS.dbo` per registrare gli eventi di controllo e le eventuali mancate verifiche.

### Obiettivi della tabella
La tabella deve permettere di:
- evitare duplicazione degli invii;
- tracciare quando una notifica è stata inviata;
- registrare ordine, fase, template e orario pianificato;
- registrare i destinatari coinvolti;
- evidenziare i casi in cui il controllo non è stato effettuato.

### Proposta struttura tabella
```sql
CREATE TABLE Traceability_TS.dbo.FaiAutocheckNotifications (
    IdNotification            BIGINT IDENTITY(1,1) PRIMARY KEY,
    OrderNumber               NVARCHAR(50)      NOT NULL,
    IdPhase                   INT               NOT NULL,
    PhaseName                 NVARCHAR(100)     NOT NULL,
    FaiTemplateId             INT               NOT NULL,
    FaiTitle                  NVARCHAR(255)     NULL,
    NrDocument                NVARCHAR(100)     NULL,
    Revision                  NVARCHAR(50)      NULL,
    PlannedStart              DATETIME          NOT NULL,
    DetectionTime             DATETIME          NOT NULL DEFAULT GETDATE(),
    EmailSentTime             DATETIME          NULL,
    EmailTo                   NVARCHAR(MAX)     NULL,
    EmailCc                   NVARCHAR(MAX)     NULL,
    ProductionQtyAtCheck      INT               NULL,
    PresenceChecked           BIT               NOT NULL DEFAULT 0,
    NotificationStatus        NVARCHAR(30)      NOT NULL,
    VerificationCompleted     BIT               NOT NULL DEFAULT 0,
    VerificationCompletedTime DATETIME          NULL,
    NonComplianceFlag         BIT               NOT NULL DEFAULT 0,
    Notes                     NVARCHAR(1000)    NULL
);
```

### Stati suggeriti
Valori suggeriti per `NotificationStatus`:
- `PENDING`
- `SENT`
- `SKIPPED_ALREADY_STARTED`
- `SKIPPED_ALREADY_SENT`
- `SKIPPED_NO_RECIPIENT`
- `VERIFIED`
- `NON_COMPLIANT`

## Logica di conformità successiva
Oltre all'invio iniziale, il sistema deve consentire una verifica successiva dell'effettiva esecuzione del controllo FAI.

Per questo motivo è necessario collegare la tabella di tracking con un successivo riscontro applicativo, in modo da sapere:
- se il template FAI atteso è stato effettivamente compilato;
- quando è stato compilato;
- chi non ha effettuato la verifica nei tempi richiesti.

La logica puntuale di chiusura del controllo potrà essere completata quando sarà disponibile la query o la regola definitiva per identificare l'avvenuta compilazione della FAI.

## Flusso logico proposto
1. Scheduler ogni 30 minuti.
2. Individuazione del file più recente in `T:\Planning\`.
3. Apertura del file Excel e lettura del tab `PlanningMachine`.
4. Filtro righe con `Order Phase Plan Start` nelle prossime 4 ore.
5. Match esatto della `PHASE` con l'elenco fasi dei template `Autocheck = true`.
6. Recupero di `IdPhase` e metadati template.
7. Verifica produzione tramite query `Qty`.
8. Se `Qty > 0`, nessuna email; registrazione eventuale stato di skip.
9. Se `Qty = 0` o `NULL`, recupero destinatari e verifica presenza per i ruoli in `TO`.
10. Composizione lista `TO` e `CC`.
11. Verifica anti-duplicazione su tabella tracking.
12. Invio email.
13. Registrazione evento nella tabella `Traceability_TS.dbo.FaiAutocheckNotifications`.
14. Successiva verifica del rispetto della procedura FAI.

## Logica anti-duplicazione consigliata
Per evitare invii multipli della stessa segnalazione, considerare chiave logica composta da:
- `OrderNumber`
- `IdPhase`
- `FaiTemplateId`
- `PlannedStart`

È consigliato creare anche un indice univoco filtrato o una regola applicativa equivalente.

Esempio:

```sql
CREATE UNIQUE INDEX UX_FaiAutocheckNotifications_Unique
ON Traceability_TS.dbo.FaiAutocheckNotifications (
    OrderNumber,
    IdPhase,
    FaiTemplateId,
    PlannedStart
);
```

## Pseudocodice operativo
```text
Ogni 30 minuti:
    file = file più recente in T:\Planning\
    righe = leggi tab PlanningMachine
    righe_valide = righe con PlannedStart tra now e now + 4 ore

    templates_autocheck = query FaiTemplates con Autocheck = true

    per ogni riga in righe_valide:
        se PHASE non corrisponde esattamente a templates_autocheck.phasename:
            continua

        idPhase = query phases by phasename
        orderNumber = colonna K
        plannedStart = colonna O

        qty = query produzione(orderNumber, idPhase)

        se qty > 0:
            registra skip se necessario
            continua

        se esiste già notifica inviata per stessa chiave logica:
            continua

        destinatari = query dipendenti
        to = []
        cc = []

        per ogni destinatario:
            se functioncode < 60:
                presenza = execute GetEmployeesTimeclockReal(@from, @to, IDEmployee)
                se presenza non null:
                    aggiungi a TO
            altrimenti:
                aggiungi a CC

        invia email se TO non vuoto
        registra evento su tabella tracking
```

## Punti da confermare
Per completare la specifica esecutiva restano da confermare i seguenti elementi:

- query definitiva per individuare i responsabili di linea da associare a ciascuna fase, se diversa dalla selezione generale `pthm`;
- regola finale per determinare l'avvenuta esecuzione del controllo FAI e valorizzare `VerificationCompleted`;
- definizione precisa del parametro `@to` nella stored procedure `GetEmployeesTimeclockReal`;
- tecnologia di invio email da usare nel programma applicativo;
- eventuale testo email bilingue o solo italiano;
- gestione festività / turni speciali / notturni se richiesti.

## Nota implementativa importante
Nel testo ricevuto è presente un passaggio ambiguo relativo alla frase “la PHASE (CHE DEVE ESSERE SOLO UGUALE al valore autocheck = …)”.

La lettura più coerente è che la `PHASE` del file Excel debba coincidere esattamente con la fase associata al template FAI che ha `Autocheck = true`, non con il valore booleano del campo `Autocheck`.

In implementazione conviene quindi formalizzare esplicitamente questa regola come:

```text
PHASE Excel = PhaseName del template FAI con Autocheck = true
```
