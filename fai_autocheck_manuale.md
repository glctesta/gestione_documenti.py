# FAI Autocheck — Manuale Operativo

## 📋 Cos'è il FAI Autocheck

Il sistema **FAI Autocheck** è un modulo automatizzato che garantisce l'esecuzione dei controlli FAI (First Article Inspection) **prima** dell'avvio della produzione per le fasi critiche. 

Il sistema opera su **due livelli**:

| Livello | Cosa fa | Chi coinvolge |
|---------|---------|---------------|
| **Email Preventiva** | Ogni 30 minuti controlla il planning e invia email se un ordine con FAI obbligatorio sta per iniziare | Responsabili di linea PTHM |
| **Validazione Guidata** | Quando l'operatore apre la form FAI, gli ordini vengono pre-caricati dal planning Excel | Operatori di linea |

---

## 🔔 Parte 1: Email Preventive Automatiche

### Come funziona

Il sistema **in background** (senza intervento dell'operatore):

1. **Ogni 30 minuti** legge il file Excel più recente dalla cartella `T:\Planning\`
2. Apre il tab **PlanningMachine** e cerca tutti gli ordini con avvio pianificato nelle **prossime 4 ore**
3. Per ogni ordine trovato, verifica se la **fase** corrisponde a un template FAI con **Autocheck = 1**
4. Se sì, controlla se la **produzione è già iniziata** (quantità > 0)
5. Se la produzione **NON è iniziata**, invia un'**email urgente** ai responsabili di linea

### Chi riceve l'email

| Ruolo | Condizione | Campo email |
|-------|-----------|-------------|
| **Responsabili linea** (FunctionCode 21-59) | Solo se **presenti in turno** (verificato via timbratrice) | **TO** (destinatario principale) |
| **Manager** (FunctionCode 60-80) | **Sempre** | **CC** (copia conoscenza) |

> ⚠️ Se nessun responsabile di linea è in turno, l'email **non viene inviata** ma l'evento viene comunque registrato nel database.

### Contenuto dell'email

L'email contiene:
- ⚠️ **Avviso urgente** con richiesta di azione
- **Numero ordine** e **nome fase**
- **Orario pianificato** di avvio produzione
- **Template FAI** applicabile (titolo, documento, revisione)
- Nota sulla registrazione ai fini di compliance

### Anti-duplicazione

Il sistema **non invia la stessa email due volte**. Per ogni combinazione univoca di:
- Numero ordine
- Fase
- Template FAI
- Orario pianificato

viene inviata **una sola notifica**. Se il planning cambia e l'orario viene spostato, viene considerata come una nuova combinazione.

### Orari di funzionamento

| Parametro | Valore |
|-----------|--------|
| Intervallo di controllo | Ogni 30 minuti |
| Finestra di anticipo | 4 ore prima dell'avvio |
| Orario attivo | 06:00 — 22:00 |
| Giorni attivi | Solo giorni lavorativi (calendario Romania) |

---

## 🖥️ Parte 2: Validazione FAI con Ordini dal Planning

### Quando si attiva

Quando un operatore apre la form **FAI — Validazione Linea** e seleziona un template con **Autocheck = 1**, il sistema cambia automaticamente il comportamento del selettore ordini:

| Template | Comportamento ordini |
|----------|---------------------|
| **Autocheck = 0** (default) | L'operatore digita e cerca tra **tutti gli ordini** nel database |
| **Autocheck = 1** | Il sistema carica **solo gli ordini pianificati** dal file Excel, filtrati per la fase del template |

### Passi operativi

#### 1. Accedere alla Validazione Linea

```
Menu → FAI → Validazione Linea → [Login con credenziali]
```

#### 2. Selezionare il Template FAI

Dal menu a tendina **"Template FAI"**, selezionare il template desiderato.

- Se il template ha **Autocheck attivo**, il sistema mostrerà automaticamente gli ordini dal planning
- Nella barra di stato in basso apparirà il messaggio:  
  `📋 X ordini da planning (Y in ritardo <3h)`

#### 3. Comprendere gli Indicatori degli Ordini

Ogni ordine nella lista mostra un **indicatore di tempo**:

| Icona | Significato | Esempio |
|-------|-------------|---------|
| ✅ | L'ordine inizia tra **3 ore o più** — tempo sufficiente per il controllo FAI | `✅ PR0000345 - PROD001 - Nome [Start 07:30 (in 13h)]` |
| ⏰ | L'ordine inizia tra **meno di 3 ore** — controllo FAI in **ritardo** | `⏰ PR0000348 - PROD002 - Nome [Start 17:53 (in 0h — LATE!)]` |

> **Importante:** Gli ordini con ⏰ possono comunque essere selezionati e validati, ma il sistema **registra automaticamente** che il controllo FAI è stato eseguito in ritardo rispetto alla pianificazione.

#### 4. Selezionare l'Ordine

Cliccare sull'ordine desiderato dalla lista. I campi verranno compilati automaticamente:
- **Cod** (codice prodotto)
- **Cantitate** (quantità ordine)
- **Comanda SL** (ID ordine nel sistema)

#### 5. Compilare la Checklist

Procedere normalmente con la compilazione della checklist FAI:
- ✅ **OK** — il controllo è superato
- ❌ **Not OK** — il controllo NON è superato (verrà richiesto di inserire descrizione problema, causa radice e azione correttiva)
- **N/A** — il controllo non è applicabile

#### 6. Salvare la Validazione

Premere **"Salva Validazione"**. Il sistema:
1. Salva tutti i risultati nel database (come per i template normali)
2. Genera il PDF del report FAI
3. Invia l'email di notifica ai destinatari configurati
4. **Se Autocheck**: registra l'evento con lo stato:
   - `VERIFIED_ON_TIME` — se il controllo è stato fatto **≥ 3 ore prima** dell'avvio
   - `VERIFIED_LATE` — se il controllo è stato fatto **< 3 ore prima** dell'avvio

---

## 📊 Tabella Tracciamento (per Amministratori)

Tutti gli eventi vengono registrati nella tabella `Traceability_RS.fai.FaiAutocheckNotifications`:

| Campo | Descrizione |
|-------|-------------|
| `OrderNumber` | Numero ordine |
| `PhaseName` | Nome della fase |
| `FaiTemplateId` | Template FAI applicato |
| `PlannedStart` | Data/ora pianificata dal file Excel (colonna O) |
| `DetectionTime` | Quando il sistema ha rilevato l'evento |
| `EmailSentTime` | Quando l'email è stata inviata (NULL se non inviata) |
| `NotificationStatus` | Stato: `SENT`, `SKIPPED_ALREADY_STARTED`, `SKIPPED_NO_RECIPIENT`, `VERIFIED_ON_TIME`, `VERIFIED_LATE` |
| `VerificationCompleted` | Se il controllo FAI è stato eseguito |

### Stati possibili

| Stato | Significato |
|-------|-------------|
| `SENT` | Email preventiva inviata ai responsabili |
| `SKIPPED_ALREADY_STARTED` | Produzione già avviata, email non necessaria |
| `SKIPPED_NO_RECIPIENT` | Nessun responsabile presente in turno |
| `VERIFIED_ON_TIME` | FAI eseguito con almeno 3h di anticipo ✅ |
| `VERIFIED_LATE` | FAI eseguito con meno di 3h di anticipo ⏰ |

---

## ❓ Domande Frequenti

### Perché non vedo ordini quando seleziono il template Autocheck?

Possibili cause:
1. **Nessun ordine PTHM nelle prossime 4 ore** — il sistema mostra solo ordini con avvio pianificato entro 4 ore
2. **File Excel non aggiornato** — il sistema legge il file più recente in `T:\Planning\`. Verificare che il planning sia stato aggiornato
3. **Fase non corrispondente** — la fase dell'ordine nell'Excel deve corrispondere esattamente alla fase del template FAI

### Posso validare un ordine che non è nella lista del planning?

No, se il template ha Autocheck attivo. Per validare un ordine non pianificato, utilizzare un template FAI senza Autocheck.

### Cosa succede se non eseguo il controllo FAI prima dell'avvio?

1. Il sistema invierà email preventive ai responsabili di linea
2. L'evento sarà registrato nel database per revisione compliance
3. Se il controllo viene eseguito dopo l'avvio, verrà marcato come `VERIFIED_LATE`

### L'email arriva anche se il FAI è stato già completato?

No. Se la produzione risulta già avviata al momento del controllo (quantità > 0), il sistema registra `SKIPPED_ALREADY_STARTED` e **non invia l'email**.

### Il sistema funziona anche nei giorni festivi?

No. Il sistema rispetta il **calendario lavorativo rumeno** e si disattiva automaticamente nei weekend e festivi.
