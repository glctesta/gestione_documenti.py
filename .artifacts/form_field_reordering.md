# Riordino Campi Form Task

## Modifica Implementata

Il campo **Categoria** è stato spostato come **primo elemento** del form di gestione task, per ottimizzare il workflow di creazione.

## File Modificato

**`npi/windows/config_window.py`** - Classe `TaskManagementFrame`

## Ordine Campi

### Prima
```
┌─────────────────────────────────────┐
│ Dettagli Task                       │
├─────────────────────────────────────┤
│ ItemID:        [____________]       │
│ Nome Task:     [____________]       │
│ Categoria:     [▼___________]       │
│ Nr. Ordine:    [____________]       │
│ Descrizione:   [____________]       │
│ □ Is Title                          │
└─────────────────────────────────────┘
```

### Dopo
```
┌─────────────────────────────────────┐
│ Dettagli Task                       │
├─────────────────────────────────────┤
│ Categoria:     [▼___________]  ← 1° │
│ ItemID:        [____________]  ← 2° │
│ Nome Task:     [____________]       │
│ Nr. Ordine:    [____________]       │
│ Descrizione:   [____________]       │
│ □ Is Title                          │
└─────────────────────────────────────┘
```

## Vantaggi

### 1. Workflow Ottimizzato
```
Workflow PRIMA:
1. Clicca "Nuovo"
2. Inserisci ItemID manualmente (es: DES-005)
3. Inserisci Nome Task
4. Seleziona Categoria
   └─ ItemID già compilato, nessun suggerimento

Workflow DOPO:
1. Clicca "Nuovo"
2. Seleziona Categoria (es: Design)
   └─ ItemID viene suggerito automaticamente: DES-005 ✨
3. Accetta o modifica ItemID
4. Inserisci Nome Task
```

### 2. Suggerimento Automatico Efficace

Con la categoria come primo campo, il **suggerimento automatico di ItemID** funziona al meglio:

```
┌─────────────────────────────────────┐
│ Nuovo Task                          │
├─────────────────────────────────────┤
│ Categoria:  [Design ▼]              │
│             ↓ (seleziona)           │
│ ItemID:     DES-005  ← suggerito!   │
│ Nome:       [____________]          │
└─────────────────────────────────────┘
```

### 3. Logica Naturale

L'ordine rispecchia il **flusso logico** di creazione:
1. **Cosa** stai facendo? → Categoria (Design, Testing, etc.)
2. **Quale** codice? → ItemID (DES-005)
3. **Come** si chiama? → Nome Task (Initial sketches)
4. **Dettagli** → Descrizione, flags, etc.

## Implementazione

```python
labels_config = [
    ('CategoryId', 'label_category', 'combo'),  # ← Spostato qui
    ('ItemID', 'label_item_id', 'entry'),
    ('NomeTask', 'label_task_name', 'entry'),
    ('NrOrdin', 'label_order_number', 'entry'),
    ('Descrizione', 'label_description', 'text'),
    ('IsTitle', 'label_is_title', 'check')
]
```

## Interazione con Altre Funzionalità

Questa modifica si integra perfettamente con:

### ✅ Suggerimento Automatico ItemID
```
1. Seleziona Categoria → Trigger evento
2. Sistema genera suggerimento ItemID
3. Popola campo ItemID automaticamente
```

### ✅ Numerazione Gerarchica NrOrdin
```
1. Seleziona Categoria (es: Design, NrOrdin=10)
2. Sistema calcola NrOrdin = 10 × 100 + 5 = 1005
3. Campo NrOrdin viene popolato al salvataggio
```

### ✅ Filtro Categoria
```
- Il filtro in alto rimane indipendente
- Serve per visualizzare task di una categoria
- Il campo nel form serve per assegnare la categoria al task
```

## Esempio Completo

### Creazione Nuovo Task

```
Passo 1: Clicca "Nuovo"
┌─────────────────────────────────────┐
│ Categoria:  [___________▼]          │
│ ItemID:     [____________]          │
│ Nome:       [____________]          │
└─────────────────────────────────────┘

Passo 2: Seleziona "Design"
┌─────────────────────────────────────┐
│ Categoria:  [Design      ▼]         │
│ ItemID:     DES-005      ← auto!    │
│ Nome:       [____________]          │
└─────────────────────────────────────┘

Passo 3: Compila il resto
┌─────────────────────────────────────┐
│ Categoria:  [Design      ▼]         │
│ ItemID:     DES-005                 │
│ Nome:       Initial sketches        │
│ Nr. Ordine: [disabilitato]          │
│ Descr:      Create first sketches   │
│ □ Is Title                          │
└─────────────────────────────────────┘

Passo 4: Salva
→ NrOrdin viene calcolato: 1005
→ Task creato con successo!
```

## Note

- Il campo **NrOrdin** rimane **disabilitato** per nuovi task (calcolato automaticamente)
- Il campo **NrOrdin** diventa **modificabile** quando si modifica un task esistente
- L'ordine dei campi non influenza la validazione o il salvataggio
- Il focus iniziale rimane sul primo campo (ora Categoria)

## Benefici UX

1. ✅ **Meno errori**: L'utente non dimentica di selezionare la categoria
2. ✅ **Più veloce**: Il suggerimento ItemID fa risparmiare tempo
3. ✅ **Più intuitivo**: Il flusso è naturale (categoria → codice → nome)
4. ✅ **Più consistente**: Incoraggia l'uso di convenzioni di codifica uniformi

## Conclusione

Spostare la **Categoria** come primo campo trasforma il form da:
- ❌ "Inserisci manualmente tutto"

A:
- ✅ "Seleziona la categoria e lascia che il sistema ti aiuti"

Questo piccolo cambiamento migliora significativamente l'esperienza utente! 🎯
