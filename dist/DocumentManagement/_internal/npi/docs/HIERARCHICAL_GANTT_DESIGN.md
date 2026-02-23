# 📊 Gantt Gerarchico per Progetti NPI - Proposta Design

## 🎯 Obiettivo

Creare un sistema di visualizzazione Gantt per progetti NPI con gerarchia padre-figli che supporti:
1. **Gantt individuali** per ogni progetto (padre e figli)
2. **Gantt complessivo consolidato** che mostra l'intera gerarchia
3. **Espansione/collasso** dei task per progetto

---

## 📐 Design Proposto

### Opzione 1: Tabs Multiple ⭐ (Raccomandato)

**UI:** Aggiungere un `ttk.Notebook` sopra il Gantt con tabs:
- **Tab "Progetto Corrente"** - Gantt del solo progetto aperto
- **Tab "Vista Gerarchica"** - Gantt consolidato con tutti i progetti della gerarchia (se esistono figli/padre)
- **Tab per ogni progetto figlio** - Gantt dedicato a ciascun figlio

**Vantaggi:**
- ✅ Visualizzazione chiara e separata
- ✅ Facile navigazione tra progetti
- ✅ Ogni tab ha il suo Gantt indipendente

**Svantaggi:**
- ❌ Più complesso da implementare
- ❌ Occupa più spazio

---

### Opzione 2: Dropdown Selector (Più Semplice)

**UI:** Un dropdown sopra il Gantt con opzioni:
- "Solo Progetto Corrente"
- "Vista Consolidata (Tutto)"
- "Solo Progetto Figlio X"
- "Solo Progetto Figlio Y"

**Vantaggi:**
- ✅ Implementazione più semplice
- ✅ Meno spazio occupato

**Svantaggi:**
- ❌ Un solo Gantt alla volta
- ❌ Navigazione meno intuitiva

---

## 🗂️ Vista Consolidata - Design Dettagliato

### Struttura Gerarchica nel Gantt

```
📦 Progetto Padre: Macchina Completa
  ├─ 📄 Task 1 - Design generale
  ├─ 📄 Task 2 - Approvazione finale
  └─ 📄 Task 3 - Test sistema
  
  📦 Progetto Figlio: PCB Macchina
    ├─ 📄 Task 1.1 - Design PCB
    ├─ 📄 Task 1.2 - Prototipo PCB
    └─ 📄 Task 1.3 - Test PCB
    
  📦 Progetto Figlio: Firmware Macchina
    ├─ 📄 Task 2.1 - Sviluppo firmware
    ├─ 📄 Task 2.2 - Debug firmware
    └─ 📄 Task 2.3 - Release firmware
```

### Funzionalità Espansione/Collasso

**Comportamento:**
1. **Default**: Progetti espansi, task collassati
2. **Click sul progetto**: Espande/collassa i task di quel progetto
3. **Indicatori visuali**:
   - `▼ Progetto X` = Task visibili
   - `▶ Progetto X` = Task nascosti
   - `📦` = Progetto padre
   - `📄` = Progetto figlio

---

## 🎨 Codifica Colori Avanzata

### Livello Progetto
- **Progetto Padre**: Barra più spessa, colore blu scuro `#1565C0`
- **Progetti Figli**: Barra media, colore blu `#42A5F5`

### Livello Task (come ora)
- **In Ritardo**: Rosso `#e74c3c`
- **Target NPI**: Blu Microsoft `#0078d4`
- **Completato**: Verde `#2ecc71`
- **In Lavorazione**: Giallo `#f1c40f`
- **Default**: Blu chiaro `#3498db`

---

## 💾 Dati Necessari

### Nuova Funzione in `npi_manager.py`

```python
def get_gantt_hierarchy_data(self, root_project_id):
    """
    Recupera dati Gantt per un progetto e tutti i suoi discendenti.
    
    Returns:
        {
            'root_project': {...},
            'projects': [
                {
                    'project': ProgettoNPI,
                    'tasks': [...],
                    'is_parent': bool,
                    'level': int
                },
                ...
            ]
        }
    """
```

---

## 🛠️ Implementazione - Step by Step

### Step 1: Modifica `gantt_window.py` - Aggiungere UI Selector ✅

```python
# Aggiungi sopra il Gantt
selector_frame = ttk.Frame(self)
selector_frame.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(selector_frame, text="Vista:").pack(side=tk.LEFT, padx=5)
self.view_mode = ttk.Combobox(selector_frame, state='readonly', width=30)
self.view_mode['values'] = ['Progetto Corrente', 'Vista Consolidata']
self.view_mode.current(0)
self.view_mode.bind('<<ComboboxSelected>>', self._on_view_changed)
```

### Step 2: Aggiungere Logica Visualizzazione

```python
def _on_view_changed(self, event=None):
    mode = self.view_mode.get()
    
    if mode == 'Progetto Corrente':
        # Gantt standard attuale
        self._create_standard_gantt()
    elif mode == 'Vista Consolidata':
        # Gantt gerarchico con espansione/collasso
        self._create_hierarchical_gantt()
```

### Step 3: Implementare Gantt Gerarchico

```python
def _create_hierarchical_gantt(self):
    """Crea Gantt con gerarchia progetti espandibile."""
    
    # 1. Recupera gerarchia completa
    hierarchy = self.npi_manager.get_project_hierarchy(self.project_id)
    
    # 2. Costruisci lista progetti piatta con livelli
    projects_flat = self._flatten_hierarchy(hierarchy)
    
    # 3. Per ogni progetto, aggiungi:
    #    - Barra progetto (clickable)
    #    - Task del progetto (se espanso)
    
    # 4. Gestisci click per espandere/collassare
```

### Step 4: Stato Espansione/Collasso

```python
# Dizionario per tracciare stato
self.expanded_projects = {
    project_id: False  # False = collassato (task nascosti)
}

def _toggle_project_expansion(self, project_id):
    """Espande/collassa i task di un progetto."""
    self.expanded_projects[project_id] = not self.expanded_projects.get(project_id, False)
    self._refresh_gantt()
```

---

## 📊 Layout Gantt Gerarchico - Esempio Visivo

```
Timeline →
       Gen    Feb    Mar    Apr    Mag
       |------|------|------|------|
       
📦 Macchina Completa [═══════════════════════════════]
  ▼ Task Macchina
    Task 1          [═══════]
    Task 2                    [══════]
    Task 3                              [═════════]

  📄 PCB Macchina  [═══════════════]
    ▶ Task PCB (collassati)

  📄 Firmware      [════════════════════]
    ▼ Task Firmware
      Task 2.1      [═══════]
      Task 2.2              [═════]
      Task 2.3                    [═══════]
```

---

## 🎯 Milestone Aggregate

**Opzionale ma utile**: Mostrare milestone aggregate:
- **Start Progetto Padre** = MIN(start di tutti i progetti)
- **Fine Progetto Padre** = MAX(fine di tutti i progetti)
- **Completamento Padre** = MEDIA(completamento figli pesata per numero task)

```python
def calculate_aggregate_progress(projects):
    total_tasks = sum(len(p['tasks']) for p in projects)
    completed_tasks = sum(
        len([t for t in p['tasks'] if t['Status'] == 'Completato'])
        for p in projects
    )
    return int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
```

---

## ✅ Vantaggi Soluzione Proposta

1. **Flessibilità**: Vedi solo quello che ti serve
2. **Scalabilità**: Funziona con gerarchie profonde
3. **UX Intuitiva**: Click per espandere/collassare
4. **Performance**: Carica solo i dati necessari
5. **Retrocompatibilità**: Progetti senza figli funzionano come prima

---

## 🚀 Prossimi Passi

1. **Conferma Design** ✋ - Quale opzione preferisci?
   - Opzione 1: Tabs multiple
   - Opzione 2: Dropdown selector

2. **Implementazione Backend** 
   - Funzione `get_gantt_hierarchy_data()`
   - Logica aggregazione dati

3. **Implementazione Frontend**
   - UI selector/tabs
   - Logica espansione/collasso
   - Rendering Gantt gerarchico

4. **Testing**
   - Test con progetti semplici
   - Test con gerarchie profonde
   - Test performance

---

## 💬 Domande da Chiarire

1. **Profondità massima?** - Quanti livelli di gerarchia supportare? (consiglio max 3)
2. **Ordinamento?** - Come ordinare i progetti figli? (per data inizio? alfabetico?)
3. **Filtri?** - Applicare gli stessi filtri (categoria, owner) anche nella vista consolidata?
4. **Link dipendenze?** - Mostrare dipendenze tra task di progetti diversi?

---

**Dimmi cosa ne pensi e quale opzione preferisci, poi procedo con l'implementazione!** 🎯
