# 🚧 Gantt Gerarchico - Implementazione in Corso

## ✅ Completato

### Backend (npi_manager.py)
- ✅ Funzione `get_gantt_hierarchy_data(root_project_id)`
  - Recupera gerarchia completa progetti
  - Processa ricorsivamente padre e figli
  - Aggrega dati Gantt per ogni progetto
  - Restituisce struttura dati con livelli e relazioni

**Commit:** `99b1437c`

---

## 🔨 In Sviluppo

### Frontend (gantt_window.py)

#### Modifiche Necessarie:

1. **Aggiungere ttk.Notebook per Tabs** ✋
   - Tab "Progetto Corrente" - Gantt come ora
   - Tab "Vista Consolidata" - Gantt gerarchico (se ha figli/padre)
   - Tab per ogni progetto figlio

2. **Modificare __init__** ✋
   - Controllare se progetto ha gerarchia
   - Se sì, creare tabs
   - Se no, Gantt normale (retro

compatibile)

3. **Creare Funzione `create_hierarchical_chart()`** ✋
   - Processa dati da `get_gantt_hierarchy_data()`
   - Crea righe Gantt per:
     - Progetto (barra più spessa)
     - Task (se espansi)
   - Implementa logica espansione/collasso

4. **Gestire Click su Progetti** ✋
   - Espandere/collassare task
   - Aggiornare indicatore ▼/▶

---

## 📋 Piano Implementazione

### Fase 1: UI Tabs (Prossimo Step)
```python
# In gantt_window.py __init__
self.notebook = ttk.Notebook(chart_frame)
self.notebook.pack(fill=tk.BOTH, expand=True)

# Tab progetto corrente
tab_current = ttk.Frame(self.notebook)
self.notebook.add(tab_current, text="Progetto Corrente")

# Se ha gerarchia...
if hierarchy_data['has_hierarchy']:
    # Tab vista consolidata
    tab_consolidated = ttk.Frame(self.notebook)
    self.notebook.add(tab_consolidated, text="Vista Consolidata")
    
    # Tab per ogni figlio
    for child in children:
        tab_child = ttk.Frame(self.notebook)
        self.notebook.add(tab_child, text=child_name)
```

### Fase 2: Gantt Gerarchico
```python
def create_hierarchical_chart(self):
    """Crea Gantt con gerarchia progetti espandibile."""
    
    # Stato espansione (dict project_id -> bool)
    self.expanded = {}
    
    # Per ogni progetto nella gerarchia
    for proj_data in hierarchy['projects']:
        # Aggiungi barra progetto
        self._add_project_bar(proj_data)
        
        # Se espanso, aggiungi task
        if self.expanded.get(proj_data['project_id'], True):
            for task in proj_data['tasks']:
                self._add_task_bar(task, proj_data['level'])
```

### Fase 3: Interattività
- Click su progetto → toggle espansione
- Refresh Gantt
- Animazioni (opzionale)

---

## 🎯 Prossimo Step

**Modifica `gantt_window.py` per aggiungere sistema tabs.**

Vuoi che proceda con l'implementazione completa ora, oppure preferisci:
1. **Implementazione completa in una volta** (più tempo, tutto funzionante)
2. **Implementazione incrementale** (prima tabs base, poi gerarchia)

**Dimmi come preferisci procedere!** 🚀
