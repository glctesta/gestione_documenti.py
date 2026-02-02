# File: npi/windows/task_dependencies_window.py
import tkinter as tk
from tkinter import ttk, messagebox

class TaskDependenciesWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, task_id, project_id, wave_id, task_name):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.task_id = task_id
        self.project_id = project_id
        self.wave_id = wave_id
        self.task_name = task_name

        self.title(f"{self.lang.get('manage_dependencies_title', 'Gestione Dipendenze')} - {self.task_name}")
        self.geometry("800x600")
        self.transient(master)
        self.grab_set()

        self.all_available_tasks = []
        self.available_predecessors = {}
        self.current_dependencies = {}
        self.dep_category_var = tk.StringVar()

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, text=f"Task: {self.task_name}", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)

        # Content - Split in two: Current Dependencies and Add New
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # TOP: Current Dependencies
        current_frame = ttk.LabelFrame(paned, text=self.lang.get('current_dependencies', 'Dipendenze Attuali'))
        paned.add(current_frame, weight=1)

        cols = ('ID', 'Task', 'Category', 'Type')
        self.tree = ttk.Treeview(current_frame, columns=cols, show='headings')
        self.tree.heading('ID', text="ID")
        self.tree.heading('Task', text=self.lang.get('col_task', 'Task'))
        self.tree.heading('Category', text=self.lang.get('col_category', 'Categoria'))
        self.tree.heading('Type', text=self.lang.get('col_type', 'Tipo'))

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Task', width=300)
        self.tree.column('Category', width=150)
        self.tree.column('Type', width=150)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        sb = ttk.Scrollbar(current_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        btn_remove = ttk.Button(main_frame, text=self.lang.get('btn_remove', 'Elimină Dipendenza'), command=self._remove_selected)
        btn_remove.pack(pady=5)

        # BOTTOM: Add New Dependency
        add_frame = ttk.LabelFrame(paned, text=self.lang.get('add_dependency_title', 'Aggiungi Nuova Dipendenza'))
        paned.add(add_frame, weight=0)

        grid_add = ttk.Frame(add_frame)
        grid_add.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(grid_add, text=self.lang.get('filter_category', 'Filtra per Categoria:')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_cat = ttk.Combobox(grid_add, textvariable=self.dep_category_var, state='readonly', width=30)
        self.combo_cat.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.combo_cat.bind('<<ComboboxSelected>>', self._filter_tasks)

        ttk.Label(grid_add, text=self.lang.get('select_task', 'Seleziona Task Prerequisito:')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_task = ttk.Combobox(grid_add, state='readonly', width=60)
        self.combo_task.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.combo_task.config(postcommand=self._adjust_combo_width)

        ttk.Button(grid_add, text=self.lang.get('btn_add', 'Adaugă'), command=self._add_dependency).grid(row=1, column=2, padx=10)

        # Status Bar
        self.status_bar = ttk.Label(self, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_data(self):
        self._refresh_dependencies()
        self._load_available_predecessors()

    def _refresh_dependencies(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        dependencies = self.npi_manager.get_task_dependencies(self.task_id)
        self.current_dependencies = {}

        for dep in dependencies:
            pred = dep.depends_on_task
            if pred and pred.task_catalogo:
                task_name = pred.task_catalogo.NomeTask
                cat_name = pred.task_catalogo.categoria.Category if pred.task_catalogo.categoria else "N/A"
                dep_type = dep.DependencyType or "FinishToStart"
                
                item_id = self.tree.insert('', tk.END, values=(dep.DependencyID, task_name, cat_name, dep_type))
                self.current_dependencies[item_id] = dep.DependencyID

    def _load_available_predecessors(self):
        self.all_available_tasks = self.npi_manager.get_available_predecessor_tasks(self.task_id, self.wave_id)
        
        categories = set()
        for t in self.all_available_tasks:
            if t.task_catalogo and t.task_catalogo.categoria:
                categories.add(t.task_catalogo.categoria.Category.strip())
            else:
                categories.add("Nessuna Categoria")
        
        all_cat_label = self.lang.get('all_categories', 'Tutte le categorie')
        self.combo_cat['values'] = [all_cat_label] + sorted(list(categories))
        self.dep_category_var.set(all_cat_label)
        self._filter_tasks()

    def _filter_tasks(self, event=None):
        selected_cat = self.dep_category_var.get().strip()
        all_cat_label = self.lang.get('all_categories', 'Tutte le categorie').strip()
        
        self.available_predecessors = {}
        task_names = []
        is_all = (selected_cat == all_cat_label or not selected_cat)

        for t in self.all_available_tasks:
            if not t.task_catalogo: continue
            
            task_cat = t.task_catalogo.categoria.Category.strip() if t.task_catalogo.categoria else "Nessuna Categoria"
            
            if is_all or task_cat.lower() == selected_cat.lower():
                name = t.task_catalogo.NomeTask
                display_name = f"[{task_cat}] {name}" if is_all else name
                
                if display_name in self.available_predecessors:
                    display_name = f"{display_name} (ID:{t.TaskProdottoID})"
                
                task_names.append(display_name)
                self.available_predecessors[display_name] = t.TaskProdottoID
        
        prompt = self.lang.get('select_predecessor', 'Selectea sau cauta sarcina...')
        self.combo_task['values'] = [prompt] + sorted(task_names)
        self.combo_task.current(0)
        self._adjust_combo_width()

    def _adjust_combo_width(self):
        values = self.combo_task['values']
        if not values: return
        max_len = max(len(str(v)) for v in values)
        self.combo_task.config(width=min(max_len + 5, 80))

    def _add_dependency(self):
        selected = self.combo_task.get()
        prompt = self.lang.get('select_predecessor', 'Selectea sau cauta sarcina...')
        if not selected or selected == prompt:
            messagebox.showwarning("Attenzione", "Seleziona un task.")
            return

        pred_id = self.available_predecessors.get(selected)
        if not pred_id: return

        success, msg = self.npi_manager.add_task_dependency(self.task_id, pred_id)
        if success:
            self._refresh_dependencies()
            self._load_available_predecessors() # Re-load to avoid duplicates/circulars
        else:
            messagebox.showerror("Errore", msg)

    def _remove_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona una dipendenza da eliminare.")
            return
        
        dep_id = self.current_dependencies.get(sel[0])
        if not dep_id: return

        if messagebox.askyesno("Conferma", "Eliminare la dipendenza selezionata?"):
            success, msg = self.npi_manager.remove_task_dependency(dep_id)
            if success:
                self._refresh_dependencies()
                self._load_available_predecessors()
            else:
                messagebox.showerror("Errore", msg)
