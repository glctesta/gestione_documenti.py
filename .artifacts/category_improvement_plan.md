# Implementazione: Miglioramento Gestione Categorie NPI

## Obiettivo
Migliorare il tab "Categorie" in `config_window.py` per:
1. Mostrare una listbox con tutti i task della categoria selezionata
2. Aggiungere un indicatore `***` per le categorie già utilizzate in progetti

## Modifiche necessarie

### 1. npi_manager.py - Aggiungere nuovi metodi

```python
def get_tasks_by_category(self, category_id):
    """
    Recupera tutti i task del catalogo per una specifica categoria.
    
    Args:
        category_id: ID della categoria
        
    Returns:
        Lista di TaskCatalogo ordinati per Nrordin
    """
    session = self._get_session()
    try:
        tasks = session.query(TaskCatalogo).filter(
            TaskCatalogo.CategoryId == category_id
        ).order_by(TaskCatalogo.Nrordin).all()
        
        return self._detach_list(session, tasks)
    finally:
        session.close()


def is_category_used_in_projects(self, category_id):
    """
    Verifica se una categoria è stata utilizzata in almeno un progetto.
    
    Args:
        category_id: ID della categoria
        
    Returns:
        True se la categoria è usata, False altrimenti
    """
    session = self._get_session()
    try:
        # Query per verificare se esistono TaskProdotto con task di questa categoria
        count = session.query(TaskProdotto).join(
            TaskCatalogo, TaskProdotto.TaskID == TaskCatalogo.TaskID
        ).filter(
            TaskCatalogo.CategoryId == category_id
        ).count()
        
        return count > 0
    finally:
        session.close()
```

### 2. config_window.py - Modificare CategoryManagementFrame

#### Modifiche al __init__:
- Aggiungere una Listbox per i task sotto il form
- Aggiungere un label "Task in questa categoria:"

#### Modifiche a _load_categories:
- Aggiungere `***` alle categorie usate

#### Modifiche a _on_category_select:
- Caricare i task della categoria nella listbox

#### Nuovo metodo _load_category_tasks:
- Popolare la listbox con i task

## Codice da aggiungere

### In __init__ dopo i campi del form:

```python
# Listbox per i task della categoria
tasks_label_frame = ttk.LabelFrame(
    form_frame, 
    text=self.lang.get('category_tasks_label', 'Task in questa categoria:')
)
tasks_label_frame.grid(row=len(labels), column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
tasks_label_frame.columnconfigure(0, weight=1)
tasks_label_frame.rowconfigure(0, weight=1)

# Listbox con scrollbar
tasks_list_frame = ttk.Frame(tasks_label_frame)
tasks_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

self.tasks_listbox = tk.Listbox(tasks_list_frame, height=10)
self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tasks_scrollbar = ttk.Scrollbar(tasks_list_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
self.tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
```

### Modificare _load_categories:

```python
def _load_categories(self):
    """Carica le categorie nel treeview con indicatore *** per quelle usate."""
    # Pulisci il treeview
    for item in self.tree.get_children():
        self.tree.delete(item)

    # Carica le categorie dal database
    try:
        categories = self.npi_manager.get_categories()
        if categories:
            for cat in categories:
                # Verifica se la categoria è usata
                is_used = self.npi_manager.is_category_used_in_projects(cat.CategoryId)
                category_name = cat.Category
                if is_used:
                    category_name += " ***"
                
                self.tree.insert('', tk.END, values=(
                    cat.CategoryId,
                    category_name,
                    cat.NrOrdin or ""
                ))
    except Exception as e:
        messagebox.showerror(
            self.lang.get('db_error_title'),
            self.lang.get('db_error_load_categories').format(error=e),
            parent=self
        )
```

### Aggiungere nuovo metodo _load_category_tasks:

```python
def _load_category_tasks(self, category_id):
    """Carica i task della categoria selezionata nella listbox."""
    # Pulisci la listbox
    self.tasks_listbox.delete(0, tk.END)
    
    if category_id is None:
        return
    
    try:
        tasks = self.npi_manager.get_tasks_by_category(category_id)
        
        if not tasks:
            self.tasks_listbox.insert(tk.END, self.lang.get('no_tasks_in_category', 'Nessun task in questa categoria'))
        else:
            for task in tasks:
                # Formato: ItemID - NomeTask
                display_text = f"{task.ItemID} - {task.NomeTask}"
                if task.IsTitle:
                    display_text = f"[TITOLO] {display_text}"
                self.tasks_listbox.insert(tk.END, display_text)
    except Exception as e:
        logger.error(f"Errore caricamento task categoria: {e}")
        self.tasks_listbox.insert(tk.END, f"Errore: {e}")
```

### Modificare _on_category_select:

```python
def _on_category_select(self, event=None):
    """Gestisce la selezione di una categoria dalla lista."""
    if not self.tree.selection():
        return

    try:
        item = self.tree.item(self.tree.selection()[0])
        self.selected_category_id = item['values'][0]

        # Ottieni la categoria dal manager
        category = self.npi_manager.get_category_by_id(self.selected_category_id)

        if category:
            self._populate_form(category)
            # NUOVO: Carica i task della categoria
            self._load_category_tasks(self.selected_category_id)
    except Exception as e:
        messagebox.showerror(
            self.lang.get('db_error_title'),
            f"Errore nel caricamento della categoria: {str(e)}",
            parent=self
        )
```

### Modificare _clear_form:

```python
def _clear_form(self, clear_selection=True):
    """Pulisce il form."""
    self.selected_category_id = None

    if clear_selection and self.tree.selection():
        self.tree.selection_remove(self.tree.selection())

    # Verifica sicurezza
    if not hasattr(self, 'fields'):
        return

    for widget in self.fields.values():
        if isinstance(widget, ttk.Entry):
            widget.delete(0, tk.END)
    
    # NUOVO: Pulisci anche la listbox dei task
    if hasattr(self, 'tasks_listbox'):
        self.tasks_listbox.delete(0, tk.END)
```

## Traduzioni necessarie

Aggiungere queste chiavi:
- `category_tasks_label`: "Task in questa categoria:"
- `no_tasks_in_category`: "Nessun task in questa categoria"

## Test
1. Aprire la finestra di configurazione NPI
2. Andare al tab "Categorie"
3. Selezionare una categoria
4. Verificare che:
   - Appaia la lista dei task
   - Le categorie usate abbiano `***`
