# File: npi/windows/config_window.py (VERSIONE DEFINITIVA E CORRETTA)

import tkinter as tk
from tkinter import ttk, messagebox


# --- Frame per la gestione dei Soggetti (Persone, Clienti, Fornitori) ---
class SubjectManagementFrame(ttk.Frame):

    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_subject_id = None
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = (self.lang.get('col_id'), self.lang.get('col_name_generic'), self.lang.get('col_type'))
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=50)
        self.tree.column(cols[1], width=200)
        self.tree.column(cols[2], width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_subject_select)

        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('subject_details_title'), padding=10)
        paned_window.add(form_frame, weight=2)

        self.fields = {}
        labels = {'NomeSoggetto': 'label_subject_name', 'Tipo': 'label_type', 'Email': 'label_email',
                  'MSTeamsUserID': 'label_msteams_id'}
        for i, (field, key) in enumerate(labels.items()):
            ttk.Label(form_frame, text=self.lang.get(key)).grid(row=i, column=0, sticky=tk.W, pady=2)
            if field == 'Tipo':
                self.fields[field] = ttk.Combobox(form_frame, state='readonly')
                self.fields[field]['values'] = (self.lang.get('subject_type_internal'),
                                                self.lang.get('subject_type_customer'),
                                                self.lang.get('subject_type_supplier'))
            else:
                self.fields[field] = ttk.Entry(form_frame, width=40)
            self.fields[field].grid(row=i, column=1, sticky=tk.EW, padx=5)
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_subject).pack(side=tk.LEFT,
                                                                                                      padx=5)

        self._load_subjects()

    def _load_subjects(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        soggetti = self.npi_manager.get_soggetti()
        if soggetti:
            for s in soggetti:
                tipo_display = s.Tipo
                if tipo_display == 'Interno':
                    tipo_display = self.lang.get('subject_type_internal')
                elif tipo_display == 'Cliente':
                    tipo_display = self.lang.get('subject_type_customer')
                elif tipo_display == 'Fornitore':
                    tipo_display = self.lang.get('subject_type_supplier')
                self.tree.insert('', tk.END, values=(s.SoggettoId, s.Nome, tipo_display))

    def _on_subject_select(self, event=None):
        if not self.tree.selection(): return
        item = self.tree.item(self.tree.selection()[0])
        self.selected_subject_id = item['values'][0]
        soggetto = self.npi_manager.get_soggetto_by_id(self.selected_subject_id)
        if isinstance(soggetto, list) and len(soggetto) > 0:
            soggetto = soggetto[0]  # Get first item from list

        if soggetto:
            self._populate_form(soggetto)

    def _populate_form(self, soggetto):
        self._clear_form(clear_selection=False)
        self.selected_subject_id = soggetto.SoggettoId
        self.fields['NomeSoggetto'].insert(0, soggetto.Nome or "")
        self.fields['Email'].insert(0, soggetto.Email or "")
        self.fields['MSTeamsUserID'].insert(0, soggetto.MSTeamsUserID or "")

        tipo_display = soggetto.Tipo
        if tipo_display == 'Interno':
            tipo_display = self.lang.get('subject_type_internal')
        elif tipo_display == 'Cliente':
            tipo_display = self.lang.get('subject_type_customer')
        elif tipo_display == 'Fornitore':
            tipo_display = self.lang.get('subject_type_supplier')
        self.fields['Tipo'].set(tipo_display or "")

    def _clear_form(self, clear_selection=True):
        self.selected_subject_id = None
        if clear_selection and self.tree.selection(): self.tree.selection_remove(self.tree.selection())
        for widget in self.fields.values():
            if isinstance(widget, ttk.Combobox):
                widget.set('')
            else:
                widget.delete(0, tk.END)

    def _save_subject(self):
        nome = self.fields['NomeSoggetto'].get()
        tipo_display = self.fields['Tipo'].get()
        if not nome or not tipo_display:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('validation_error_subject_required'),
                                 parent=self)
            return

        tipo_db = 'Interno'
        if tipo_display == self.lang.get('subject_type_customer'):
            tipo_db = 'Cliente'
        elif tipo_display == self.lang.get('subject_type_supplier'):
            tipo_db = 'Fornitore'

        data = {'NomeSoggetto': nome, 'Tipo': tipo_db, 'Email': self.fields['Email'].get(),
                'MSTeamsUserID': self.fields['MSTeamsUserID'].get()}
        try:
            if self.selected_subject_id is None:
                self.npi_manager.create_soggetto(data)
            else:
                self.npi_manager.update_soggetto(self.selected_subject_id, data)
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_subject_saved'), parent=self)
            self._load_subjects()
            self._clear_form()
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'),
                                 self.lang.get('db_error_generic_save').format(error=e), parent=self)

    def _delete_subject(self):
        if self.selected_subject_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_subject_to_delete'), parent=self)
            return
        if messagebox.askyesno(self.lang.get('confirm_delete_title'), self.lang.get('confirm_delete_subject_text'),
                               parent=self):
            try:
                self.npi_manager.delete_soggetto(self.selected_subject_id)
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_subject_deleted'),
                                    parent=self)
                self._load_subjects()
                self._clear_form()
            except Exception as e:
                messagebox.showerror(self.lang.get('db_error_title'),
                                     self.lang.get('db_error_delete_subject').format(error=e), parent=self)


# --- Frame per la gestione dei Prodotti e la creazione di progetti NPI (RIPRISTINATO) ---
class ProductManagementFrame(ttk.Frame):
    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_product_id = None
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = (self.lang.get('col_id'), self.lang.get('col_product_code'), self.lang.get('col_product_name'),
                self.lang.get('col_customer'), self.lang.get('label_version', 'Versione'))
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=50)
        self.tree.column(cols[1], width=100)
        self.tree.column(cols[2], width=200)
        self.tree.column(cols[3], width=150)
        self.tree.column(cols[4], width=80)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_product_select)

        form_panel = ttk.Frame(paned_window)
        paned_window.add(form_panel, weight=2)

        form_frame = ttk.LabelFrame(form_panel, text=self.lang.get('product_details_title'), padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.fields = {}
        labels = {'CodiceProdotto': 'label_product_code', 'NomeProdotto': 'label_product_name',
                  'Cliente': 'label_customer'}
        for i, (field, key) in enumerate(labels.items()):
            ttk.Label(form_frame, text=self.lang.get(key)).grid(row=i, column=0, sticky=tk.W, pady=2)
            self.fields[field] = ttk.Entry(form_frame, width=40)
            self.fields[field].grid(row=i, column=1, sticky=tk.EW, padx=5)
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_product).pack(side=tk.LEFT,
                                                                                                      padx=5)

        # --- FUNZIONALITA' DI GESTIONE PROGETTO CON VERSIONE ---
        project_frame = ttk.LabelFrame(form_panel, text=self.lang.get('project_npi_management_title'), padding=10)
        project_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Campo Versione per il progetto NPI
        version_frame = ttk.Frame(project_frame)
        version_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(version_frame, text=self.lang.get('label_version', 'Versione:')).pack(side=tk.LEFT, padx=(0, 5))
        self.version_entry = ttk.Entry(version_frame, width=20)
        self.version_entry.pack(side=tk.LEFT)
        
        self.create_project_button = ttk.Button(project_frame, text=self.lang.get('btn_create_npi_project'),
                                                command=self._create_npi_project, state=tk.DISABLED)
        self.create_project_button.pack(pady=10)

        self._load_products()

    def _load_products(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        products = self.npi_manager.get_prodotti()
        if products:
            # Recupera i progetti NPI per ottenere le versioni
            progetti = self.npi_manager.get_progetti_attivi()
            # Crea una mappa prodotto_id -> versione
            version_map = {p.ProdottoID: p.Version for p in progetti if p.Version}
            
            for p in products:
                version = version_map.get(p.ProdottoID, "")
                self.tree.insert('', tk.END,
                                 values=(p.ProdottoID, p.CodiceProdotto or "", p.NomeProdotto, p.Cliente or "", version))

    def _on_product_select(self, event=None):
        if not self.tree.selection(): return
        item = self.tree.item(self.tree.selection()[0])
        self.selected_product_id = item['values'][0]
        prodotto = self.npi_manager.get_prodotto_by_id(self.selected_product_id)
        if prodotto:
            self._populate_form(prodotto)
            self.create_project_button.config(state=tk.NORMAL)

    def _populate_form(self, prodotto):
        self._clear_form(clear_selection=False)
        self.selected_product_id = prodotto.ProdottoID
        self.fields['CodiceProdotto'].insert(0, prodotto.CodiceProdotto or "")
        self.fields['NomeProdotto'].insert(0, prodotto.NomeProdotto or "")
        self.fields['Cliente'].insert(0, prodotto.Cliente or "")

    def _clear_form(self, clear_selection=True):
        self.selected_product_id = None
        if clear_selection and self.tree.selection(): self.tree.selection_remove(self.tree.selection())
        self.create_project_button.config(state=tk.DISABLED)
        for field in self.fields.values(): field.delete(0, tk.END)

    def _save_product(self):
        data = {key: widget.get() for key, widget in self.fields.items()}
        if not data['NomeProdotto']:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('validation_error_product_name_required'),
                                 parent=self)
            return
        try:
            if self.selected_product_id is None:
                prodotto_creato = self.npi_manager.create_prodotto(data)
                self.selected_product_id = prodotto_creato.ProdottoID
            else:
                self.npi_manager.update_prodotto(self.selected_product_id, data)
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_product_saved'), parent=self)
            self._load_products()
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'),
                                 self.lang.get('db_error_generic_save').format(error=e), parent=self)

    def _delete_product(self):
        if self.selected_product_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_product_to_delete'), parent=self)
            return
        if messagebox.askyesno(self.lang.get('confirm_delete_title'), self.lang.get('confirm_delete_product_text'),
                               parent=self):
            try:
                self.npi_manager.delete_prodotto(self.selected_product_id)
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_product_deleted'),
                                    parent=self)
                self._load_products()
                self._clear_form()
            except Exception as e:
                messagebox.showerror(self.lang.get('db_error_title'),
                                     self.lang.get('db_error_delete_product').format(error=e), parent=self)

    def _create_npi_project(self):
        if self.selected_product_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_product_to_create_project'), parent=self)
            return
        
        # Ottieni la versione dal campo di input
        version = self.version_entry.get().strip() or None
        
        try:
            progetto = self.npi_manager.create_progetto_npi_for_prodotto(self.selected_product_id, version)
            if progetto:
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_project_created').format(
                    product_name=progetto.prodotto.NomeProdotto), parent=self)
                # Pulisci il campo versione dopo la creazione
                self.version_entry.delete(0, tk.END)
                # Ricarica la lista prodotti per mostrare la versione
                self._load_products()
            else:
                messagebox.showinfo(self.lang.get('info_title'), self.lang.get('info_project_already_exists'),
                                    parent=self)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_create_project').format(error=e),
                                 parent=self)


# --- Frame per la gestione del Catalogo Task ---
class TaskManagementFrame(ttk.Frame):
    # ... il codice di questa classe è corretto e rimane invariato ...
    # def __init__(self, master, npi_manager, lang, **kwargs):
    #     super().__init__(master, **kwargs)
    #     self.npi_manager = npi_manager
    #     self.lang = lang
    #     self.selected_task_id = None
    #     self.pack(fill=tk.BOTH, expand=True)
    #
    #     paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
    #     paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    #
    #     list_frame = ttk.Frame(paned_window, padding=10)
    #     paned_window.add(list_frame, weight=2)
    #
    #     cols = (self.lang.get('col_id'), self.lang.get('col_item_id'), self.lang.get('col_task_name'),
    #             self.lang.get('col_category'))
    #     self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
    #     for col in cols: self.tree.heading(col, text=col)
    #     self.tree.column(cols[0], width=50)
    #     self.tree.column(cols[1], width=100)
    #     self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #     self.tree.bind('<<TreeviewSelect>>', self._on_task_select)
    #
    #     form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('task_catalog_details_title'), padding=10)
    #     paned_window.add(form_frame, weight=3)
    #
    #     self.fields = {}
    #     self.category_map = {}
    #     labels = {'ItemID': 'label_item_id', 'NomeTask': 'label_task_name', 'CategoryId': 'label_category',
    #               'Descrizione': 'label_description'}
    #     for i, (field, key) in enumerate(labels.items()):
    #         ttk.Label(form_frame, text=self.lang.get(key)).grid(row=i, column=0, sticky=tk.NW, pady=2, padx=5)
    #         if field == 'CategoryId':
    #             self.fields[field] = ttk.Combobox(form_frame, state='readonly', width=38)
    #         elif field == 'Descrizione':
    #             self.fields[field] = tk.Text(form_frame, height=5, width=40)
    #         else:
    #             self.fields[field] = ttk.Entry(form_frame, width=40)
    #         self.fields[field].grid(row=i, column=1, sticky=tk.NSEW, pady=2, padx=5)
    #     form_frame.columnconfigure(1, weight=1)
    #     form_frame.rowconfigure(list(labels.keys()).index('Descrizione'), weight=1)
    #
    #     button_frame = ttk.Frame(form_frame)
    #     button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky=tk.E)
    #     ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
    #     ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_task).pack(side=tk.LEFT, padx=5)
    #     ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_task).pack(side=tk.LEFT, padx=5)
    #
    #     self.refresh_data()

    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_task_id = None
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=2)

        # Colonne visibili + colonne nascoste per i dati
        cols = ('ItemID', 'NomeTask', 'Category')
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        # Definisci le intestazioni e le larghezze
        self.tree.heading('ItemID', text=self.lang.get('col_item_id'))
        self.tree.column('ItemID', width=100)
        self.tree.heading('NomeTask', text=self.lang.get('col_task_name'))
        self.tree.column('NomeTask', width=250)
        self.tree.heading('Category', text=self.lang.get('col_category'))
        self.tree.column('Category', width=150)

        # Configura il tag per la formattazione dei titoli
        self.tree.tag_configure('title_row', font='Helvetica 10 bold', background='#eeeeee')

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)

        # FORM DI DETTAGLIO
        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('task_catalog_details_title'), padding=10)
        paned_window.add(form_frame, weight=3)

        self.fields = {}
        self.category_map = {}
        self.is_title_var = tk.BooleanVar()  # Variabile per il checkbox

        # Layout del form aggiornato
        labels_config = [
            ('ItemID', 'label_item_id', 'entry'),
            ('NomeTask', 'label_task_name', 'entry'),
            ('CategoryId', 'label_category', 'combo'),
            ('Descrizione', 'label_description', 'text'),
            ('IsTitle', 'label_is_title', 'check')  # NUOVO CAMPO
        ]

        row_idx = 0
        for field, key, widget_type in labels_config:
            label = ttk.Label(form_frame, text=self.lang.get(key))
            label.grid(row=row_idx, column=0, sticky=tk.NW, pady=2, padx=5)

            if widget_type == 'entry':
                self.fields[field] = ttk.Entry(form_frame, width=40)
            elif widget_type == 'combo':
                self.fields[field] = ttk.Combobox(form_frame, state='readonly', width=38)
            elif widget_type == 'text':
                self.fields[field] = tk.Text(form_frame, height=5, width=40)
            elif widget_type == 'check':
                self.fields[field] = ttk.Checkbutton(form_frame, variable=self.is_title_var)

            self.fields[field].grid(row=row_idx, column=1, sticky=tk.NSEW, pady=2, padx=5)

            if widget_type == 'text':
                form_frame.rowconfigure(row_idx, weight=1)

            row_idx += 1

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row_idx, column=0, columnspan=2, pady=20, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_task).pack(side=tk.LEFT, padx=5)

        self.refresh_data()

    def refresh_data(self):
        self._load_categories_for_combobox()
        self._load_tasks()

    def _load_categories_for_combobox(self):
        categories = self.npi_manager.get_categories()
        self.category_map = {cat.Category: cat.CategoryId for cat in categories}
        self.fields['CategoryId']['values'] = [""] + list(self.category_map.keys())

    def _load_tasks(self):
        selected_iid_before = self.tree.selection()
        #selected_id = self.tree.item(selected_iid_before[0])['values'][0] if selected_iid_before else None

        for i in self.tree.get_children(): self.tree.delete(i)

        #item_to_reselect = None
        tasks = self.npi_manager.get_catalogo_task()
        if tasks:
            for t in tasks:
                category_name = t.categoria.Category if t.categoria else ""
                tags_to_apply = ()
                if t.IsTitle:
                    tags_to_apply = ('title_row',)

                    # Inseriamo i dati
                    # 'text' contiene il TaskID (PK), che non è visibile all'utente.
                self.tree.insert(
                    '', tk.END, text=str(t.TaskID),
                    values=(t.ItemID, t.NomeTask, category_name),
                    tags=tags_to_apply
                )

                # Prova a ri-selezionare l'elemento precedente se ancora esiste
                if selected_iid_before:
                    if self.tree.exists(selected_iid_before[0]):
                        self.tree.selection_set(selected_iid_before[0])

        #         iid = self.tree.insert('', tk.END, values=(t.TaskID, t.ItemID, t.NomeTask, category_name))
        #         if t.TaskID == selected_id:
        #             item_to_reselect = iid
        # if item_to_reselect:
        #     self.tree.selection_set(item_to_reselect)

    def _on_task_select(self, event=None):
        if not self.tree.selection(): return
        # item = self.tree.item(self.tree.selection()[0])
        # self.selected_task_id = item['values'][0]
        # task = self.npi_manager.get_catalogo_task_by_id(self.selected_task_id)
        # if task: self._populate_form(task)
        iid = self.tree.selection()[0]
        self.selected_task_id = int(self.tree.item(iid, 'text'))

        task = self.npi_manager.get_catalogo_task_by_id(self.selected_task_id)
        if task: self._populate_form(task)

    def _populate_form(self, task):
        self._clear_form(clear_selection=False)
        self.selected_task_id = task.TaskID
        self.fields['ItemID'].insert(0, task.ItemID or "")
        self.fields['NomeTask'].insert(0, task.NomeTask or "")
        self.fields['Descrizione'].delete('1.0', tk.END)
        self.fields['Descrizione'].insert('1.0', task.Descrizione or "")
        self.fields['CategoryId'].set(task.categoria.CategoryId if task.categoria else '')
        self.is_title_var.set(bool(task.IsTitle))

    def _clear_form(self, clear_selection=True):
        self.selected_task_id = None
        if clear_selection and self.tree.selection(): self.tree.selection_remove(self.tree.selection())
        for widget in self.fields.values():
            if isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            elif isinstance(widget, ttk.Checkbutton):
                self.is_title_var.set(False)
            else:
                widget.delete(0, tk.END)
        self.fields['ItemID'].focus()

    # def _save_task(self):
    #     item_id_str = self.fields['ItemID'].get().strip()
    #     nome_task_str = self.fields['NomeTask'].get().strip()
    #     if not item_id_str or not nome_task_str:
    #         messagebox.showerror(self.lang.get('error_title'), self.lang.get('validation_error_task_required'),
    #                              parent=self)
    #         return
    #
    #     existing_task = self.npi_manager.get_catalogo_task_by_itemid(item_id_str)
    #     is_new_task = self.selected_task_id is None
    #     is_updating_different_task = existing_task and existing_task.TaskID != self.selected_task_id
    #
    #     if (is_new_task and existing_task) or is_updating_different_task:
    #         messagebox.showerror(self.lang.get('error_duplicate_title'),
    #                              self.lang.get('validation_error_duplicate_itemid').format(itemid=item_id_str),
    #                              parent=self)
    #         return
    #
    #     data = {'ItemID': item_id_str, 'NomeTask': nome_task_str,
    #             'Descrizione': self.fields['Descrizione'].get('1.0', tk.END).strip(),
    #             'CategoryId': self.category_map.get(self.fields['CategoryId'].get())}
    #     try:
    #         if is_new_task:
    #             new_task = self.npi_manager.create_catalogo_task(data)
    #             self.selected_task_id = new_task.TaskID
    #         else:
    #             self.npi_manager.update_catalogo_task(self.selected_task_id, data)
    #         messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_task_saved'), parent=self)
    #         self.refresh_data()
    #     except Exception as e:
    #         messagebox.showerror(self.lang.get('db_error_title'), self.lang.get('db_error_save_task').format(error=e),
    #                              parent=self)

    def _save_task(self):
        """METODO MODIFICATO per gestire la logica di ordinamento e IsTitle."""
        item_id_str = self.fields['ItemID'].get().strip()
        nome_task_str = self.fields['NomeTask'].get().strip()
        if not item_id_str or not nome_task_str:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('validation_error_task_required'),
                                 parent=self)
            return

        is_new_task = self.selected_task_id is None

        # Controllo duplicati
        existing_task = self.npi_manager.get_catalogo_task_by_itemid(item_id_str)
        if (is_new_task and existing_task) or (existing_task and existing_task.TaskID != self.selected_task_id):
            messagebox.showerror(self.lang.get('error_duplicate_title'),
                                 self.lang.get('validation_error_duplicate_itemid').format(itemid=item_id_str),
                                 parent=self)
            return

        # Prepara i dati
        data = {
            'ItemID': item_id_str,
            'NomeTask': nome_task_str,
            'Descrizione': self.fields['Descrizione'].get('1.0', tk.END).strip(),
            'CategoryId': self.category_map.get(self.fields['CategoryId'].get()),
            'IsTitle': self.is_title_var.get()
        }

        try:
            if is_new_task:
                # --- NUOVA LOGICA PER GESTIRE L'ANCORA ---
                # 1. Recupera l'elemento selezionato nella Treeview.
                selection = self.tree.selection()
                anchor_task_id = None

                # 2. Se qualcosa è selezionato, prendi il suo TaskID (che abbiamo memorizzato nella proprietà 'text').
                if selection:
                    try:
                        anchor_task_id = int(self.tree.item(selection[0], 'text'))
                    except (ValueError, IndexError):
                        anchor_task_id = None  # Fallback di sicurezza

                # 3. Chiama il manager passando l'ID dell'ancora.
                #    Se nulla è selezionato, passerà None e il manager inserirà in fondo.
                new_task = self.npi_manager.create_catalogo_task(
                    data,
                    anchor_task_id=anchor_task_id
                )
                self.selected_task_id = new_task.TaskID

            else:  # L'aggiornamento rimane invariato
                self.npi_manager.update_catalogo_task(self.selected_task_id, data)

            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_task_saved'), parent=self)

            # Salviamo la selezione attuale per ripristinarla dopo l'aggiornamento
            current_selection = self.tree.selection()
            self.refresh_data()  # Aggiorna la lista

            # Ri-seleziona l'elemento appena salvato o modificato
            if is_new_task and self.selected_task_id:
                # Cerca il nuovo iid basato sul TaskID
                for iid in self.tree.get_children():
                    if int(self.tree.item(iid, 'text')) == self.selected_task_id:
                        self.tree.selection_set(iid)
                        self.tree.focus(iid)
                        break
            elif current_selection:
                # Ripristina la selezione precedente se era un update
                if self.tree.exists(current_selection[0]):
                    self.tree.selection_set(current_selection[0])
                    self.tree.focus(current_selection[0])

        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'), self.lang.get('db_error_save_task').format(error=e),
                                 parent=self)


    def _delete_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_task_to_delete'), parent=self)
            return
        if messagebox.askyesno(self.lang.get('confirm_delete_title'), self.lang.get('confirm_delete_task_text'),
                               parent=self):
            try:
                self.npi_manager.delete_catalogo_task(self.selected_task_id)
                self.refresh_data()
                self._clear_form()
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_task_deleted'), parent=self)
            except Exception as e:
                messagebox.showerror(self.lang.get('db_error_title'),
                                     self.lang.get('db_error_delete_task').format(error=e), parent=self)


# --- Frame per la gestione delle Categorie ---
# --- Frame per la gestione delle Categorie ---
class CategoryManagementFrame(ttk.Frame):
    """Frame per la gestione delle categorie dei task NPI."""

    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_category_id = None

        # ⭐ IMPORTANTE: Inizializza fields subito
        self.fields = {}

        self.pack(fill=tk.BOTH, expand=True)

        # Layout principale con PanedWindow
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- PANNELLO SINISTRO: Lista Categorie ---
        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = (
            self.lang.get('col_id'),
            self.lang.get('col_category'),
            self.lang.get('col_order')
        )
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        # Configura colonne
        self.tree.heading(cols[0], text=cols[0])
        self.tree.column(cols[0], width=50)
        self.tree.heading(cols[1], text=cols[1])
        self.tree.column(cols[1], width=200)
        self.tree.heading(cols[2], text=cols[2])
        self.tree.column(cols[2], width=80)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_category_select)

        # --- PANNELLO DESTRO: Form Dettagli ---
        form_frame = ttk.LabelFrame(
            paned_window,
            text=self.lang.get('category_details_title'),
            padding=10
        )
        paned_window.add(form_frame, weight=2)

        # Campi del form
        labels = {
            'Category': 'label_category_name',
            'NrOrdin': 'label_order_number'
        }

        for i, (field, key) in enumerate(labels.items()):
            ttk.Label(form_frame, text=self.lang.get(key)).grid(
                row=i, column=0, sticky=tk.W, pady=2
            )
            self.fields[field] = ttk.Entry(form_frame, width=40)
            self.fields[field].grid(row=i, column=1, sticky=tk.EW, padx=5)

        form_frame.columnconfigure(1, weight=1)

        # Bottoni
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky=tk.E)

        ttk.Button(
            button_frame,
            text=self.lang.get('btn_new'),
            command=self._clear_form
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text=self.lang.get('btn_save'),
            command=self._save_category
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text=self.lang.get('btn_delete'),
            command=self._delete_category
        ).pack(side=tk.LEFT, padx=5)

        # Carica i dati iniziali
        self._load_categories()

    def _load_categories(self):
        """Carica le categorie nel treeview."""
        # Pulisci il treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Carica le categorie dal database
        try:
            categories = self.npi_manager.get_categories()
            if categories:
                for cat in categories:
                    self.tree.insert('', tk.END, values=(
                        cat.CategoryId,
                        cat.Category,
                        cat.NrOrdin or ""
                    ))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('db_error_title'),
                self.lang.get('db_error_load_categories').format(error=e),
                parent=self
            )

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
        except Exception as e:
            messagebox.showerror(
                self.lang.get('db_error_title'),
                f"Errore nel caricamento della categoria: {str(e)}",
                parent=self
            )

    def _populate_form(self, category):
        """Popola il form con i dati della categoria selezionata."""
        self._clear_form(clear_selection=False)
        self.selected_category_id = category.CategoryId
        self.fields['Category'].insert(0, category.Category or "")
        self.fields['NrOrdin'].insert(0, str(category.NrOrdin or ""))

    def _clear_form(self, clear_selection=True):
        """Pulisce il form."""
        self.selected_category_id = None

        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

        # ⭐ Verifica sicurezza
        if not hasattr(self, 'fields'):
            return

        for widget in self.fields.values():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)

    def _save_category(self):
        """Salva la categoria (nuova o aggiornamento)."""
        category_name = self.fields['Category'].get().strip()
        order_str = self.fields['NrOrdin'].get().strip()

        # Validazione
        if not category_name:
            messagebox.showerror(
                self.lang.get('error_title'),
                self.lang.get('validation_error_category_name_required'),
                parent=self
            )
            return

        # Converti l'ordine in intero
        try:
            order_number = int(order_str) if order_str else 0
        except ValueError:
            messagebox.showerror(
                self.lang.get('error_title'),
                self.lang.get('validation_error_order_must_be_number'),
                parent=self
            )
            return

        data = {
            'Category': category_name,
            'NrOrdin': order_number
        }

        try:
            if self.selected_category_id is None:
                # Crea nuova categoria
                self.npi_manager.create_category(data)
                messagebox.showinfo(
                    self.lang.get('success_title'),
                    self.lang.get('success_category_saved'),
                    parent=self
                )
            else:
                # Aggiorna categoria esistente
                self.npi_manager.update_category(self.selected_category_id, data)
                messagebox.showinfo(
                    self.lang.get('success_title'),
                    self.lang.get('success_category_updated'),
                    parent=self
                )

            self._load_categories()
            self._clear_form()

        except Exception as e:
            messagebox.showerror(
                self.lang.get('db_error_title'),
                self.lang.get('db_error_generic_save').format(error=e),
                parent=self
            )

    def _delete_category(self):
        """Elimina la categoria selezionata."""
        if self.selected_category_id is None:
            messagebox.showwarning(
                self.lang.get('warning_no_selection_title'),
                self.lang.get('warning_select_category_to_delete'),
                parent=self
            )
            return

        # Conferma eliminazione
        if not messagebox.askyesno(
                self.lang.get('confirm_delete_title'),
                self.lang.get('confirm_delete_category_text'),
                parent=self
        ):
            return

        try:
            self.npi_manager.delete_category(self.selected_category_id)
            messagebox.showinfo(
                self.lang.get('success_title'),
                self.lang.get('success_category_deleted'),
                parent=self
            )
            self._load_categories()
            self._clear_form()

        except Exception as e:
            messagebox.showerror(
                self.lang.get('db_error_title'),
                self.lang.get('db_error_delete_category').format(error=e),
                parent=self
            )


# --- Finestra Principale di Configurazione ---
class NpiConfigWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, authorized_user, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.authorized_user = authorized_user
        self.app_master = master  # Salviamo un riferimento alla finestra principale App

        self.title(self.lang.get('config_window_title'))
        self.geometry("1200x700")
        self.transient(master)
        self.grab_set()

        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.subj_frame = SubjectManagementFrame(notebook, self.npi_manager, self.lang)
        self.prod_frame = ProductManagementFrame(notebook, self.npi_manager, self.lang)
        self.cat_frame = CategoryManagementFrame(notebook, self.npi_manager, self.lang)
        self.task_frame = TaskManagementFrame(notebook, self.npi_manager, self.lang)

        notebook.add(self.subj_frame, text=self.lang.get('tab_subjects_title'))
        notebook.add(self.prod_frame, text=self.lang.get('tab_products_title'))
        notebook.add(self.cat_frame, text=self.lang.get('tab_categories_title'))
        notebook.add(self.task_frame, text=self.lang.get('tab_task_catalog_title'))

        def on_tab_changed(event):
            try:
                if notebook.select() == str(self.task_frame):
                    self.task_frame.refresh_data()
            except tk.TclError:
                pass

        notebook.bind("<<NotebookTabChanged>>", on_tab_changed)


# File: npi/windows/config_window.py
# AGGIUNGERE/MODIFICARE la classe TaskCatalogManagementFrame

class TaskCatalogManagementFrame(ttk.Frame):
    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_task_id = None  # ← AGGIUNGERE questo attributo
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Lista task
        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = (
            self.lang.get('col_item_id'),
            self.lang.get('col_task_name'),
            self.lang.get('col_category')
        )
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=100)
        self.tree.column(cols[1], width=250)
        self.tree.column(cols[2], width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)  # ← AGGIUNGERE binding

        # Form dettagli
        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('task_details_title'), padding=10)
        paned_window.add(form_frame, weight=2)

        self.fields = {}

        # ItemID
        ttk.Label(form_frame, text=self.lang.get('label_item_id')).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.fields['ItemID'] = ttk.Entry(form_frame, width=40)
        self.fields['ItemID'].grid(row=0, column=1, sticky=tk.EW, padx=5)

        # NomeTask
        ttk.Label(form_frame, text=self.lang.get('label_task_name')).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.fields['NomeTask'] = ttk.Entry(form_frame, width=40)
        self.fields['NomeTask'].grid(row=1, column=1, sticky=tk.EW, padx=5)

        # Categoria
        ttk.Label(form_frame, text=self.lang.get('label_category')).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.fields['CategoryId'] = ttk.Combobox(form_frame, state='readonly', width=38)
        self.fields['CategoryId'].grid(row=2, column=1, sticky=tk.EW, padx=5)

        # Descrizione
        ttk.Label(form_frame, text=self.lang.get('label_description')).grid(row=3, column=0, sticky=tk.NW, pady=2)
        desc_frame = ttk.Frame(form_frame)
        desc_frame.grid(row=3, column=1, sticky=tk.EW, padx=5)
        self.fields['Descrizione'] = tk.Text(desc_frame, height=4, width=40, wrap=tk.WORD)
        desc_scrollbar = ttk.Scrollbar(desc_frame, command=self.fields['Descrizione'].yview)
        self.fields['Descrizione'].config(yscrollcommand=desc_scrollbar.set)
        self.fields['Descrizione'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Durata Stimata
        ttk.Label(form_frame, text=self.lang.get('label_estimated_duration')).grid(row=4, column=0, sticky=tk.W, pady=2)
        self.fields['DurataStimata'] = ttk.Spinbox(form_frame, from_=0, to=999, width=38)
        self.fields['DurataStimata'].grid(row=4, column=1, sticky=tk.EW, padx=5)

        # Tipo Soggetto
        ttk.Label(form_frame, text=self.lang.get('label_subject_type')).grid(row=5, column=0, sticky=tk.W, pady=2)
        self.fields['TipoSoggetto'] = ttk.Combobox(form_frame, state='readonly', width=38)
        self.fields['TipoSoggetto']['values'] = (
            self.lang.get('subject_type_internal'),
            self.lang.get('subject_type_customer'),
            self.lang.get('subject_type_supplier')
        )
        self.fields['TipoSoggetto'].grid(row=5, column=1, sticky=tk.EW, padx=5)

        form_frame.columnconfigure(1, weight=1)

        # Pulsanti
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_task).pack(side=tk.LEFT, padx=5)

        self._load_categories_combo()
        self._load_tasks()

    def _load_categories_combo(self):
        """Carica le categorie nella combobox"""
        categories = self.npi_manager.get_categories()
        if categories:
            self.category_map = {cat.Category: cat.CategoryId for cat in categories}
            self.category_map_rev = {cat.CategoryId: cat.Category for cat in categories}
            self.fields['CategoryId']['values'] = tuple(self.category_map.keys())

    def _load_tasks(self):
        """Carica i task nella lista"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        session = self.npi_manager.Session()
        try:
            from ..data_models import TaskCatalogo
            from sqlalchemy.orm import joinedload

            tasks = session.query(TaskCatalogo).options(
                joinedload(TaskCatalogo.categoria)
            ).all()

            for task in tasks:
                category_name = task.categoria.Category if task.categoria else ""
                self.tree.insert('', tk.END, values=(
                    task.ItemID,
                    task.NomeTask,
                    category_name
                ))
        finally:
            session.close()

    def _on_task_select(self, event=None):
        """Gestisce la selezione di un task dalla lista"""
        if not self.tree.selection():
            return
        item = self.tree.item(self.tree.selection()[0])
        item_id = item['values'][0]

        # Recupera i dettagli dal database
        session = self.npi_manager.Session()
        try:
            from ..data_models import TaskCatalogo
            from sqlalchemy.orm import joinedload

            task = session.query(TaskCatalogo).options(
                joinedload(TaskCatalogo.category)
            ).filter(TaskCatalogo.ItemID == item_id).first()

            if task:
                self._populate_form(task)
        finally:
            session.close()

    def _populate_form(self, task):
        """Popola il form con i dati del task selezionato"""
        self._clear_form(clear_selection=False)
        self.selected_task_id = task.TaskID

        self.fields['ItemID'].insert(0, task.ItemID or "")
        self.fields['NomeTask'].insert(0, task.NomeTask or "")

        if task.CategoryId and task.CategoryId in self.category_map_rev:
            self.fields['CategoryId'].set(self.category_map_rev[task.CategoryId])

        if task.Descrizione:
            self.fields['Descrizione'].insert('1.0', task.Descrizione)

        if task.DurataStimata:
            self.fields['DurataStimata'].delete(0, tk.END)
            self.fields['DurataStimata'].insert(0, str(task.DurataStimata))

        # Mappa TipoSoggetto
        tipo_display = task.TipoSoggetto or ""
        if tipo_display == 'Interno':
            tipo_display = self.lang.get('subject_type_internal')
        elif tipo_display == 'Cliente':
            tipo_display = self.lang.get('subject_type_customer')
        elif tipo_display == 'Fornitore':
            tipo_display = self.lang.get('subject_type_supplier')
        self.fields['TipoSoggetto'].set(tipo_display)

    def _clear_form(self, clear_selection=True):
        """Pulisce il form"""
        self.selected_task_id = None
        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

        self.fields['ItemID'].delete(0, tk.END)
        self.fields['NomeTask'].delete(0, tk.END)
        self.fields['CategoryId'].set('')
        self.fields['Descrizione'].delete('1.0', tk.END)
        self.fields['DurataStimata'].delete(0, tk.END)
        self.fields['TipoSoggetto'].set('')

    def _save_task(self):
        """Salva o aggiorna un task"""
        item_id = self.fields['ItemID'].get()
        nome_task = self.fields['NomeTask'].get()
        category_name = self.fields['CategoryId'].get()

        if not item_id or not nome_task or not category_name:
            messagebox.showerror(
                self.lang.get('error_title'),
                self.lang.get('validation_error_task_required'),
                parent=self
            )
            return

        # Mappa categoria
        category_id = self.category_map.get(category_name)

        # Mappa TipoSoggetto
        tipo_display = self.fields['TipoSoggetto'].get()
        tipo_db = 'Interno'
        if tipo_display == self.lang.get('subject_type_customer'):
            tipo_db = 'Cliente'
        elif tipo_display == self.lang.get('subject_type_supplier'):
            tipo_db = 'Fornitore'

        data = {
            'ItemID': item_id,
            'NomeTask': nome_task,
            'CategoryId': category_id,
            'Descrizione': self.fields['Descrizione'].get('1.0', tk.END).strip(),
            'DurataStimata': int(self.fields['DurataStimata'].get() or 0),
            'TipoSoggetto': tipo_db
        }

        try:
            if self.selected_task_id is None:
                # Creazione nuovo task
                session = self.npi_manager.Session()
                try:
                    from ..data_models import TaskCatalogo
                    new_task = TaskCatalogo(**data)
                    session.add(new_task)
                    session.commit()
                    messagebox.showinfo(
                        self.lang.get('success_title'),
                        self.lang.get('success_task_created'),
                        parent=self
                    )
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()
            else:
                # Aggiornamento task esistente
                session = self.npi_manager.Session()
                try:
                    from ..data_models import TaskCatalogo
                    task = session.query(TaskCatalogo).get(self.selected_task_id)
                    if task:
                        for key, value in data.items():
                            setattr(task, key, value)
                        session.commit()
                    messagebox.showinfo(
                        self.lang.get('success_title'),
                        self.lang.get('success_task_updated'),
                        parent=self
                    )
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()

            self._load_tasks()
            self._clear_form()
        except Exception as e:
            messagebox.showerror(
                self.lang.get('db_error_title'),
                self.lang.get('db_error_generic_save').format(error=e),
                parent=self
            )

    def _delete_task(self):
        """Elimina un task"""
        if self.selected_task_id is None:
            messagebox.showwarning(
                self.lang.get('warning_no_selection_title'),
                self.lang.get('warning_select_task_to_delete'),
                parent=self
            )
            return

        if messagebox.askyesno(
                self.lang.get('confirm_delete_title'),
                self.lang.get('confirm_delete_task_text'),
                parent=self
        ):
            try:
                session = self.npi_manager.Session()
                try:
                    from ..data_models import TaskCatalogo
                    task = session.query(TaskCatalogo).get(self.selected_task_id)
                    if task:
                        session.delete(task)
                        session.commit()
                    messagebox.showinfo(
                        self.lang.get('success_title'),
                        self.lang.get('success_task_deleted'),
                        parent=self
                    )
                    self._load_tasks()
                    self._clear_form()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()
            except Exception as e:
                messagebox.showerror(
                    self.lang.get('db_error_title'),
                    self.lang.get('db_error_delete_task').format(error=e),
                    parent=self
                )
