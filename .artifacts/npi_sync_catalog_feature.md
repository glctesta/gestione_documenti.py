# Sincronizzazione Catalogo Task NPI

## Problema Risolto

**Problema**: Quando si crea un progetto NPI, vengono copiati tutti i task del catalogo esistenti in quel momento. Se successivamente si creano nuovi task nel catalogo (es. categoria "PROVA"), questi non appaiono nel progetto esistente, anche filtrando per quella categoria.

**Soluzione**: Aggiunto un bottone "Sincronizza Catalogo" che permette di aggiungere al progetto tutti i task del catalogo creati dopo la creazione del progetto.

## File Modificati

1. **`npi/windows/project_window.py`**
   - Aggiunto bottone "Sincronizza Catalogo"
   - Aggiunto metodo `_sync_catalog_tasks()`

2. **`npi/npi_manager.py`**
   - Aggiunto metodo `get_all_catalog_tasks()`
   - Aggiunto metodo `add_catalog_tasks_to_project()`

## Funzionalità

### Bottone "Sincronizza Catalogo"

Posizionato nell'header della finestra progetto NPI, accanto al bottone "Importa Task".

```
[Importa Task] [Sincronizza Catalogo] [Export Excel]
```

### Workflow

```
1. Utente apre progetto NPI esistente
   ↓
2. Crea nuovi task nel catalogo (es. categoria "PROVA")
   ↓
3. Torna al progetto NPI
   ↓
4. I nuovi task NON appaiono (anche filtrando per "PROVA")
   ↓
5. Click "Sincronizza Catalogo"
   ↓
6. Messaggio di conferma:
   ┌─────────────────────────────────────────┐
   │ Questa operazione aggiungerà al        │
   │ progetto tutti i task del catalogo che │
   │ non sono ancora presenti.              │
   │                                         │
   │ I task già esistenti non verranno      │
   │ modificati.                             │
   │                                         │
   │ Vuoi continuare?                        │
   │                                         │
   │              [Sì]  [No]                 │
   └─────────────────────────────────────────┘
   ↓
7. [Sì] → Aggiunge task mancanti
   ↓
8. Messaggio: "Aggiunti X task dal catalogo"
   ↓
9. UI ricaricata → Nuovi task visibili ✅
```

## Logica Implementata

### Metodo `_sync_catalog_tasks()`

```python
def _sync_catalog_tasks(self):
    # 1. Chiedi conferma all'utente
    response = messagebox.askyesno(...)
    
    # 2. Ottieni tutti i task del catalogo
    all_catalog_tasks = self.npi_manager.get_all_catalog_tasks()
    
    # 3. Ottieni i task già presenti nel progetto
    wave = self.progetto.waves[0]
    existing_task_ids = {t.TaskID for t in wave.tasks}
    
    # 4. Trova i task mancanti
    missing_tasks = [t for t in all_catalog_tasks 
                     if t.TaskID not in existing_task_ids]
    
    # 5. Se nessun task mancante
    if not missing_tasks:
        messagebox.showinfo("Tutti i task già presenti")
        return
    
    # 6. Aggiungi i task mancanti
    added_count = self.npi_manager.add_catalog_tasks_to_project(
        wave.WaveID, missing_tasks
    )
    
    # 7. Ricarica UI
    self._load_data_and_populate_ui()
```

### Metodo `get_all_catalog_tasks()`

```python
def get_all_catalog_tasks(self):
    """Ottiene tutti i task del catalogo."""
    tasks = session.scalars(
        select(TaskCatalogo)
        .options(joinedload(TaskCatalogo.categoria))
        .order_by(TaskCatalogo.NrOrdin)
    ).all()
    return [self._detach_object(session, t) for t in tasks]
```

### Metodo `add_catalog_tasks_to_project()`

```python
def add_catalog_tasks_to_project(self, wave_id, catalog_tasks):
    """Aggiunge i task del catalogo mancanti a una wave."""
    added_count = 0
    for catalog_task in catalog_tasks:
        new_task = TaskProdotto(
            WaveID=wave_id,
            TaskID=catalog_task.TaskID
        )
        session.add(new_task)
        added_count += 1
    
    session.commit()
    return added_count
```

## Esempio Pratico

### Scenario: Aggiunta Task Categoria "PROVA"

```
Situazione Iniziale:
- Progetto NPI creato il 01/01/2024
- Catalogo aveva 50 task
- Progetto ha 50 task

Azioni:
1. 15/01/2024: Crei 5 nuovi task categoria "PROVA" nel catalogo
2. Apri progetto NPI
3. Filtri per categoria "PROVA"
4. ❌ Nessun task visibile (i 5 nuovi non ci sono)

Soluzione:
5. Click "Sincronizza Catalogo"
6. Conferma operazione
7. ✅ Aggiunti 5 task dal catalogo
8. Filtri per "PROVA"
9. ✅ Ora vedi tutti i 5 task!
```

## Chiavi di Traduzione

### Nuove Chiavi da Aggiungere

```
btn_sync_catalog        → "Sincronizza Catalogo"
msg_sync_catalog        → Messaggio di conferma
msg_no_missing_tasks    → "Tutti i task già presenti"
msg_tasks_synced        → "Aggiunti X task dal catalogo"
```

### Script SQL

Vedi file: `.artifacts/sql_translations_npi_sync_catalog.sql`

## Vantaggi

1. ✅ **Flessibilità**: Puoi aggiungere task al catalogo in qualsiasi momento
2. ✅ **Controllo**: L'utente decide quando sincronizzare
3. ✅ **Sicurezza**: Conferma prima di modificare il progetto
4. ✅ **Non distruttivo**: I task esistenti non vengono modificati
5. ✅ **Feedback chiaro**: Messaggi informativi su cosa è stato fatto

## Note Tecniche

### Confronto Task

Il confronto tra task esistenti e task del catalogo avviene tramite `TaskID`:

```python
existing_task_ids = {t.TaskID for t in wave.tasks}
missing_tasks = [t for t in all_catalog_tasks 
                 if t.TaskID not in existing_task_ids]
```

### Creazione TaskProdotto

Per ogni task mancante, viene creato un nuovo `TaskProdotto`:

```python
new_task = TaskProdotto(
    WaveID=wave_id,      # ID della wave del progetto
    TaskID=catalog_task.TaskID  # ID del task dal catalogo
)
```

### Ricaricamento UI

Dopo la sincronizzazione, la UI viene ricaricata per mostrare i nuovi task:

```python
self._load_data_and_populate_ui()
self.log_status(f"Sincronizzati {added_count} task dal catalogo")
```

## Test

### Test 1: Sincronizzazione con Task Mancanti
1. Crea progetto NPI
2. Aggiungi nuovi task al catalogo
3. Apri progetto NPI
4. Click "Sincronizza Catalogo"
5. ✅ Verifica task aggiunti
6. ✅ Verifica messaggio corretto

### Test 2: Sincronizzazione senza Task Mancanti
1. Apri progetto NPI già sincronizzato
2. Click "Sincronizza Catalogo"
3. ✅ Verifica messaggio "Tutti i task già presenti"

### Test 3: Filtro Categoria dopo Sincronizzazione
1. Sincronizza task categoria "PROVA"
2. Filtra per categoria "PROVA"
3. ✅ Verifica nuovi task visibili

### Test 4: Task Esistenti Non Modificati
1. Assegna alcuni task prima della sincronizzazione
2. Sincronizza catalogo
3. ✅ Verifica task assegnati rimasti invariati

## Limitazioni

- La sincronizzazione aggiunge solo task **nuovi** (non presenti nel progetto)
- I task già presenti nel progetto **non vengono aggiornati** anche se modificati nel catalogo
- Se vuoi aggiornare task esistenti, devi farlo manualmente

## Possibili Miglioramenti Futuri

1. **Sincronizzazione Selettiva**: Permettere di scegliere quali task aggiungere
2. **Filtro per Categoria**: Sincronizzare solo task di una categoria specifica
3. **Aggiornamento Task Esistenti**: Opzione per aggiornare anche i task già presenti
4. **Sincronizzazione Automatica**: Opzione per sincronizzare automaticamente all'apertura del progetto

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Completato e Testato
