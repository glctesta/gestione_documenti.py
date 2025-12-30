# Filtri Area e Piano Attivo - Maintenance Fill Template

## ✅ Implementato

Aggiunti filtri avanzati alla finestra `FillTemplateWindow` per la compilazione schede di manutenzione.

## 🎯 Nuove Funzionalità

### 1. **Filtro per Area (ParentPhase)**

Un nuovo combobox permette di filtrare le macchine per area di produzione.

**Query utilizzata**:
```sql
SELECT DISTINCT p.parentphasename, p.IDParentPhase
FROM ParentPhases p
INNER JOIN [Traceability_RS].[eqp].[Equipments] e ON e.parentphaseid = p.IDParentPhase
ORDER BY p.parentphasename
```

**Posizione UI**: Prima del combobox macchine

**Comportamento**:
- Opzione vuota = "Tutte le aree"
- Quando selezionata, filtra automaticamente le macchine

### 2. **Filtro Piano Attivo** ✅ (Già Esistente)

Il checkbox "Solo con piano attivo" era già presente e funzionante.

**Comportamento**:
- Mostra solo macchine con `CompitoId IS NOT NULL`
- Indica le macchine con piano attivo con `(*)`

### 3. **Filtri Combinati**

I due filtri lavorano insieme:
- **Area + Piano Attivo**: Mostra solo macchine dell'area selezionata con piano attivo
- **Solo Area**: Mostra tutte le macchine dell'area (con e senza piano)
- **Solo Piano Attivo**: Mostra tutte le macchine con piano attivo (tutte le aree)
- **Nessun Filtro**: Mostra tutte le macchine

## 🔧 Modifiche Tecniche

### `FillTemplateWindow` (`maintenance_gui.py`)

#### 1. Variabili Aggiunte (`__init__`)

```python
self.phases_data = {}  # Mappa nome area -> ID
self.phase_var = tk.StringVar()  # Area selezionata
```

#### 2. UI Modificata (`_create_widgets`)

```python
# NUOVO: Filtro per Area
ttk.Label(selection_frame, text='Area:').pack(side=tk.LEFT, padx=5)
self.phase_combo = ttk.Combobox(
    selection_frame, 
    textvariable=self.phase_var, 
    state='readonly', 
    width=25
)
self.phase_combo.pack(side=tk.LEFT, padx=5)
self.phase_combo.bind("<<ComboboxSelected>>", lambda e: self._load_equipments())
```

#### 3. Nuovo Metodo `_load_phases`

```python
def _load_phases(self):
    """Carica le aree (ParentPhases) per il filtro."""
    cursor = self.db.conn.cursor()
    query = """
        SELECT DISTINCT p.parentphasename, p.IDParentPhase
        FROM ParentPhases p
        INNER JOIN [Traceability_RS].[eqp].[Equipments] e 
            ON e.parentphaseid = p.IDParentPhase
        ORDER BY p.parentphasename
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    self.phases_data = {row[0]: row[1] for row in rows}
    phase_names = [''] + list(self.phases_data.keys())
    self.phase_combo['values'] = phase_names
    self.phase_var.set('')  # Default: "Tutte"
```

#### 4. Metodo `_load_equipments` Modificato

```python
def _load_equipments(self):
    """Carica le attrezzature filtrate per area e piano attivo."""
    # Ottieni filtri
    selected_phase_name = self.phase_var.get()
    phase_id = self.phases_data.get(selected_phase_name) if selected_phase_name else None
    only_with_plan = self.only_with_plan_var.get()
    
    # Carica con entrambi i filtri
    equipments = self.db.fetch_all_equipments(
        only_with_plan=only_with_plan,
        phase_id=phase_id
    )
    
    # Popola combobox
    if equipments:
        self.equipments_data = {
            f"{row.InternalName or 'N/D'} [{row.SerialNumber}]": row.EquipmentId 
            for row in equipments
        }
        self.all_equipment_names = sorted(list(self.equipments_data.keys()))
        self.equipment_combo['values'] = self.all_equipment_names
    else:
        # Nessuna macchina trovata
        self.equipments_data = {}
        self.all_equipment_names = []
        self.equipment_combo['values'] = []
    
    # Reset selezione se non più valida
    if self.equipment_var.get() not in self.all_equipment_names:
        self.equipment_var.set('')
        self._reset_plan_and_tasks()
```

### Database (`main.py`)

#### Metodo `fetch_all_equipments` Modificato

**Prima** ❌:
```python
def fetch_all_equipments(self, only_with_plan=False):
    query = "SELECT ... WHERE cm.CompitoId IS NOT NULL"
```

**Dopo** ✅:
```python
def fetch_all_equipments(self, only_with_plan=False, phase_id=None):
    query = """
        SELECT DISTINCT e.EquipmentId, 
               InternalName + IIF(cm.CompitoId IS NULL, '', ' (*) ') AS InternalName, 
               SerialNumber 
        FROM eqp.Equipments E 
        LEFT JOIN [eqp].[CompitiManutenzione] CM ON e.EquipmentId = cm.EquipmentId
    """
    
    where_clauses = []
    params = []
    
    if only_with_plan:
        where_clauses.append("cm.CompitoId IS NOT NULL")
    
    if phase_id is not None:
        where_clauses.append("e.ParentPhaseId = ?")
        params.append(phase_id)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY InternalName, SerialNumber;"
    
    self.cursor.execute(query, params)
    return self.cursor.fetchall()
```

## 📊 Flusso Utente

1. **Apri Fill Template Window**
2. **Seleziona Area** (opzionale)
   - Combobox si popola con aree disponibili
   - Vuoto = "Tutte le aree"
3. **Attiva "Solo con piano attivo"** (opzionale)
   - Checkbox filtra macchine con `(*)`
4. **Seleziona Macchina**
   - Lista filtrata in base ai criteri
   - Auto-complete disponibile
5. **Seleziona Piano di Manutenzione**
6. **Compila Task**

## 🎨 Layout UI

```
┌─────────────────────────────────────────────────────────────┐
│ Area: [Combobox ▼]  Macchina: [Combobox ▼]  ☑ Solo piano  │
│                      Piano: [Combobox ▼]                    │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Vantaggi

1. **Navigazione Rapida**: Filtra per area riduce la lista macchine
2. **Focus Specifico**: Lavora su una sola area alla volta
3. **Piano Attivo**: Vedi solo macchine che richiedono manutenzione
4. **Filtri Combinati**: Massima flessibilità
5. **Reset Automatico**: Cambio area resetta selezione macchina

## 🚀 Test

1. Apri "Fill Template"
2. Seleziona un'area dal nuovo combobox
3. Verifica che le macchine siano filtrate
4. Attiva "Solo con piano attivo"
5. Verifica che la lista si riduca ulteriormente

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.2  
**Stato**: ✅ Implementato - Pronto per Test
