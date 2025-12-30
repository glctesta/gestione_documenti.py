# Miglioramenti UX: Bottoni e Suggerimenti

## Problemi Risolti

### 1. ❌ Suggerimento ItemID Non Funzionava
**Causa**: L'evento del combobox categoria veniva sovrascritto durante il refresh
**Soluzione**: Creato metodo unificato `_on_category_changed()` che gestisce sia il filtro che il suggerimento

### 2. ❌ Logica Bottoni Confusa
**Causa**: Non era chiaro se "Salva" creava o modificava
**Soluzione**: 
- Bottone "Nuovo" ora chiama `_new_task()` e cambia il testo del bottone Salva in "Crea Nuovo"
- Quando selezioni un task, il bottone diventa "Salva Modifiche"
- Aggiunta conferma prima di salvare/modificare

## Modifiche Implementate

### File: `npi/windows/config_window.py`

#### 1. Nuovo Metodo `_new_task()`
```python
def _new_task(self):
    """Prepara il form per creare un nuovo task."""
    self._clear_form()
    # Aggiorna il testo del bottone per chiarezza
    self.save_button.config(text='Crea Nuovo')
```

#### 2. Metodo Unificato `_on_category_changed()`
```python
def _on_category_changed(self, event=None):
    """Gestisce il cambio della categoria: filtra i task E suggerisce ItemID."""
    # 1. Filtra i task visualizzati
    self._load_tasks()
    
    # 2. Suggerisce ItemID per nuovi task
    self._on_category_selected(event)
```

#### 3. Metodo `_populate_form()` Migliorato
```python
def _populate_form(self, task):
    """Popola il form con i dati di un task esistente."""
    # ... popola i campi ...
    
    # Aggiorna il testo del bottone
    self.save_button.config(text='Salva Modifiche')
```

#### 4. Conferma Prima del Salvataggio
```python
def _save_task(self):
    # ... validazione ...
    
    # Chiedi conferma
    if is_new_task:
        confirm_msg = f"Confermi la creazione del nuovo task '{item_id} - {nome}'?"
    else:
        confirm_msg = f"Confermi la modifica del task '{item_id} - {nome}'?"
    
    if not messagebox.askyesno("Conferma", confirm_msg):
        return
    
    # ... salva ...
```

## Workflow Migliorato

### Creazione Nuovo Task

```
1. Clicca "Nuovo"
   ├─ Form viene pulito
   ├─ Focus su "Categoria"
   └─ Bottone diventa: [Crea Nuovo]

2. Seleziona Categoria (es: "Design")
   ├─ Lista task viene filtrata
   └─ ItemID suggerito: "DES-005" ✨

3. Compila i campi
   ├─ ItemID: DES-005 (o modifica)
   ├─ Nome: Initial sketches
   └─ Descrizione: ...

4. Clicca "Crea Nuovo"
   ├─ Mostra: "Confermi la creazione del nuovo task 'DES-005 - Initial sketches'?"
   ├─ [Sì] → Task creato
   └─ [No] → Annulla
```

### Modifica Task Esistente

```
1. Seleziona task dalla lista
   ├─ Form viene popolato
   └─ Bottone diventa: [Salva Modifiche]

2. Modifica i campi
   ├─ ItemID: DES-005 → DES-010
   ├─ Nome: ...
   └─ ...

3. Clicca "Salva Modifiche"
   ├─ Mostra: "Confermi la modifica del task 'DES-010 - ...'?"
   ├─ [Sì] → Task aggiornato
   └─ [No] → Annulla
```

## Indicatori Visivi

### Stato del Form

| Situazione | Bottone Salva | Focus Iniziale | NrOrdin |
|------------|---------------|----------------|---------|
| Nuovo task | "Crea Nuovo" | Categoria | Disabilitato |
| Modifica task | "Salva Modifiche" | - | Abilitato |

### Esempio Visivo

#### Nuovo Task
```
┌─────────────────────────────────────┐
│ Dettagli Task                       │
├─────────────────────────────────────┤
│ Categoria:  [Design      ▼] ← focus │
│ ItemID:     DES-005      ← suggerito│
│ Nome:       [____________]          │
│ Nr. Ordine: [disabilitato]          │
│                                     │
│ [Nuovo] [Crea Nuovo] [Elimina]      │
│          ^^^^^^^^^^^                │
└─────────────────────────────────────┘
```

#### Modifica Task
```
┌─────────────────────────────────────┐
│ Dettagli Task                       │
├─────────────────────────────────────┤
│ Categoria:  [Design      ▼]         │
│ ItemID:     DES-005                 │
│ Nome:       Initial sketches        │
│ Nr. Ordine: 1005         ← editabile│
│                                     │
│ [Nuovo] [Salva Modifiche] [Elimina] │
│          ^^^^^^^^^^^^^^^            │
└─────────────────────────────────────┘
```

## Messaggi di Conferma

### Creazione
```
┌─────────────────────────────────────┐
│ Conferma Creazione                  │
├─────────────────────────────────────┤
│ Confermi la creazione del nuovo     │
│ task 'DES-005 - Initial sketches'?  │
│                                     │
│              [Sì]  [No]             │
└─────────────────────────────────────┘
```

### Modifica
```
┌─────────────────────────────────────┐
│ Conferma Modifica                   │
├─────────────────────────────────────┤
│ Confermi la modifica del task       │
│ 'DES-010 - 3D Modeling'?            │
│                                     │
│              [Sì]  [No]             │
└─────────────────────────────────────┘
```

### Eliminazione
```
┌─────────────────────────────────────┐
│ Conferma Eliminazione               │
├─────────────────────────────────────┤
│ Sei sicuro di voler eliminare il    │
│ task 'DES-005 - Initial sketches'?  │
│                                     │
│ Questa azione non può essere        │
│ annullata.                          │
│                                     │
│              [Sì]  [No]             │
└─────────────────────────────────────┘
```

## Vantaggi

### 1. ✅ Chiarezza
- Il testo del bottone indica chiaramente l'azione
- "Crea Nuovo" vs "Salva Modifiche"

### 2. ✅ Sicurezza
- Conferma prima di ogni operazione
- Previene modifiche accidentali

### 3. ✅ Suggerimento Funzionante
- ItemID viene suggerito automaticamente
- Basato sui task esistenti nella categoria

### 4. ✅ Workflow Intuitivo
- Focus automatico sulla categoria
- Bottoni che cambiano in base al contesto

## Test

### Test 1: Suggerimento ItemID
1. Clicca "Nuovo"
2. Seleziona categoria "Design"
3. ✅ Verifica che ItemID sia popolato (es: DES-005)

### Test 2: Creazione con Conferma
1. Compila il form
2. Clicca "Crea Nuovo"
3. ✅ Verifica che appaia la conferma
4. Clicca "Sì"
5. ✅ Verifica che il task sia creato

### Test 3: Modifica con Conferma
1. Seleziona un task esistente
2. ✅ Verifica che il bottone dica "Salva Modifiche"
3. Modifica un campo
4. Clicca "Salva Modifiche"
5. ✅ Verifica che appaia la conferma
6. Clicca "Sì"
7. ✅ Verifica che il task sia aggiornato

### Test 4: Annullamento
1. Inizia a creare/modificare un task
2. Clicca "Salva" o "Crea Nuovo"
3. Clicca "No" nella conferma
4. ✅ Verifica che nulla sia salvato

## Note Tecniche

- Il riferimento a `self.save_button` viene salvato per poter cambiare il testo dinamicamente
- Il focus iniziale è sulla Categoria per facilitare il suggerimento ItemID
- Le conferme usano `messagebox.askyesno()` che restituisce `True`/`False`
- Il metodo `_on_category_changed()` unifica filtro e suggerimento in un unico evento
