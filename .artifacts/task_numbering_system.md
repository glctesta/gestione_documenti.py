# Sistema di Numerazione Gerarchica per Task NPI

## Panoramica

È stato implementato un nuovo sistema di numerazione gerarchica per i task del catalogo NPI. Questo sistema garantisce che ogni task abbia un numero d'ordine (`NrOrdin`) unico all'interno della propria categoria, seguendo uno schema prevedibile e scalabile.

## Schema di Numerazione

### Formula
```
NrOrdin = (NrOrdin_Categoria × 100) + numero_progressivo_task
```

### Incremento
- **Nuovi task**: incremento automatico di **5** rispetto all'ultimo task della categoria
- **Primo task di una categoria**: `(NrOrdin_Categoria × 100) + 5`

### Esempi

#### Categoria "Design" (NrOrdin = 10)
- Task 1: `1005` (10 × 100 + 5)
- Task 2: `1010` (10 × 100 + 10)
- Task 3: `1015` (10 × 100 + 15)
- Task 4: `1020` (10 × 100 + 20)

#### Categoria "Materials procurement" (NrOrdin = 20)
- Task 1: `2005` (20 × 100 + 5)
- Task 2: `2010` (20 × 100 + 10)
- Task 3: `2015` (20 × 100 + 15)

#### Categoria "Pilot run preparation" (NrOrdin = 30)
- Task 1: `3005` (30 × 100 + 5)
- Task 2: `3010` (30 × 100 + 10)

## Regole di Validazione

### 1. Creazione Nuovi Task
- ✅ Il `NrOrdin` viene **calcolato automaticamente**
- ✅ Non è necessario specificarlo manualmente
- ✅ Il campo `NrOrdin` è **disabilitato** nel form per i nuovi task

### 2. Modifica Task Esistenti
- ✅ Il `NrOrdin` può essere **modificato manualmente**
- ✅ Il campo `NrOrdin` è **abilitato** nel form per task esistenti
- ⚠️ **Validazione**: non può essere uguale a quello di un altro task nella **stessa categoria**
- ✅ Può essere uguale a quello di un task in una **categoria diversa**

### 3. Unicità
- ❌ **NON permesso**: Due task con stesso `NrOrdin` nella stessa categoria
- ✅ **Permesso**: Due task con stesso `NrOrdin` in categorie diverse

## Esempi di Validazione

### ✅ Scenario Valido
```
Design Task 1      → NrOrdin = 1005 ✓
Design Task 2      → NrOrdin = 1010 ✓
Materials Task 1   → NrOrdin = 2005 ✓
Materials Task 2   → NrOrdin = 1005 ✓ (categoria diversa da Design)
```

### ❌ Scenario Non Valido
```
Design Task 1      → NrOrdin = 1005 ✓
Design Task 2      → NrOrdin = 1010 ✓
Design Task 3      → NrOrdin = 1005 ✗ ERRORE: duplicato nella categoria Design!
```

## Modifiche al Codice

### File: `npi/npi_manager.py`

#### 1. Metodo `create_catalogo_task()`
- **Rimosso**: logica complessa di anchor e gap
- **Aggiunto**: calcolo automatico basato su categoria
- **Comportamento**: 
  - Ottiene il `NrOrdin` della categoria
  - Calcola la base: `categoria_nr_ordin × 100`
  - Trova il massimo `NrOrdin` esistente nella categoria
  - Aggiunge 5 al massimo (o usa base + 5 se è il primo)

#### 2. Metodo `update_catalogo_task()`
- **Aggiunto**: validazione per duplicati nella stessa categoria
- **Comportamento**:
  - Se `NrOrdin` viene modificato, verifica che non esista già
  - Controlla solo nella stessa categoria
  - Solleva `ValueError` se trova un duplicato

### File: `npi/windows/config_window.py`

#### 1. Form Task (`TaskManagementFrame`)
- **Aggiunto**: campo `NrOrdin` nel form
- **Comportamento**:
  - **Nuovo task**: campo disabilitato (valore calcolato automaticamente)
  - **Modifica task**: campo abilitato (valore modificabile manualmente)

#### 2. Metodo `_populate_form()`
- **Aggiunto**: popolamento del campo `NrOrdin`
- **Aggiunto**: abilitazione del campo per task esistenti

#### 3. Metodo `_clear_form()`
- **Aggiunto**: disabilitazione del campo `NrOrdin` per nuovi task

#### 4. Metodo `_save_task()`
- **Aggiunto**: validazione del valore `NrOrdin` se modificato
- **Aggiunto**: inclusione di `NrOrdin` nei dati solo per task esistenti

## Vantaggi del Nuovo Sistema

1. **Prevedibilità**: È facile capire a quale categoria appartiene un task dal suo `NrOrdin`
2. **Scalabilità**: Ogni categoria può avere fino a 99 task (da X05 a X99 con incrementi di 5)
3. **Flessibilità**: I task possono essere rinumerati manualmente se necessario
4. **Sicurezza**: Validazione automatica previene duplicati nella stessa categoria
5. **Semplicità**: Non serve più gestire gap e rinumerazioni complesse

## Migrazione dei Dati Esistenti

⚠️ **ATTENZIONE**: I task esistenti potrebbero avere `NrOrdin` che non seguono questo schema.

### Opzioni:
1. **Mantenere i valori esistenti**: I task vecchi mantengono i loro numeri, solo i nuovi seguono lo schema
2. **Rinumerare tutto**: Creare uno script di migrazione per rinumerare tutti i task esistenti

### Script di Migrazione (opzionale)
```python
# Esempio di script per rinumerare tutti i task esistenti
def migrate_task_numbering(npi_manager):
    categories = npi_manager.get_categories()
    
    for category in categories:
        tasks = npi_manager.get_tasks_by_category(category.CategoryId)
        base = category.NrOrdin * 100
        
        for i, task in enumerate(tasks, start=1):
            new_ordin = base + (i * 5)
            npi_manager.update_catalogo_task(task.TaskID, {'NrOrdin': new_ordin})
            print(f"Task {task.NomeTask}: {task.NrOrdin} → {new_ordin}")
```

## Test

Per testare il sistema:
1. Aprire la finestra di configurazione NPI
2. Andare al tab "Catalogo Task"
3. Creare un nuovo task → verificare che `NrOrdin` sia disabilitato
4. Salvare il task → verificare che il numero sia calcolato correttamente
5. Selezionare il task salvato → verificare che `NrOrdin` sia ora abilitato
6. Modificare `NrOrdin` manualmente → salvare
7. Tentare di creare un duplicato → verificare che venga bloccato

## Note Tecniche

- Il campo `NrOrdin` nel database rimane di tipo `Integer`
- Non è necessario modificare lo schema del database
- La validazione avviene a livello applicativo
- I messaggi di errore sono localizzati (supporto multilingua)
