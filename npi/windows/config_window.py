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
                self.tree.insert('', tk.END, values=(s.SoggettoID, s.NomeSoggetto, tipo_display))

    def _on_subject_select(self, event=None):
        if not self.tree.selection(): return
        item = self.tree.item(self.tree.selection()[0])
        self.selected_subject_id = item['values'][0]
        soggetto = self.npi_manager.get_soggetto_by_id(self.selected_subject_id)
        if soggetto: self._populate_form(soggetto)

    def _populate_form(self, soggetto):
        self._clear_form(clear_selection=False)
        self.selected_subject_id = soggetto.SoggettoID
        self.fields['NomeSoggetto'].insert(0, soggetto.NomeSoggetto or "")
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
                self.lang.get('col_customer'))
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=50)
        self.tree.column(cols[1], width=100)
        self.tree.column(cols[2], width=200)
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

        # --- FUNZIONALITA' DI GESTIONE PROGETTO RIPRISTINATA QUI ---
        project_frame = ttk.LabelFrame(form_panel, text=self.lang.get('project_npi_management_title'), padding=10)
        project_frame.pack(fill=tk.X, padx=10, pady=10)
        self.create_project_button = ttk.Button(project_frame, text=self.lang.get('btn_create_npi_project'),
                                                command=self._create_npi_project, state=tk.DISABLED)
        self.create_project_button.pack(pady=10)

        self._load_products()

    def _load_products(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        products = self.npi_manager.get_prodotti()
        if products:
            for p in products:
                self.tree.insert('', tk.END,
                                 values=(p.ProdottoID, p.CodiceProdotto or "", p.NomeProdotto, p.Cliente or ""))

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
        try:
            progetto = self.npi_manager.create_progetto_npi_for_prodotto(self.selected_product_id)
            if progetto:
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_project_created').format(
                    product_name=progetto.prodotto.NomeProdotto), parent=self)
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
                category_name = t.category.Category if t.category else ""
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

    # def _populate_form(self, task):
    #     self._clear_form(clear_selection=False)
    #     self.selected_task_id = task.TaskID
    #     self.fields['ItemID'].insert(0, task.ItemID or "")
    #     self.fields['NomeTask'].insert(0, task.NomeTask or "")
    #     self.fields['Descrizione'].insert('1.0', task.Descrizione or "")
    #     self.fields['CategoryId'].set(task.category.Category if task.category else '')

    def _populate_form(self, task):
        self._clear_form(clear_selection=False)
        self.selected_task_id = task.TaskID
        self.fields['ItemID'].insert(0, task.ItemID or "")
        self.fields['NomeTask'].insert(0, task.NomeTask or "")
        self.fields['Descrizione'].delete('1.0', tk.END)
        self.fields['Descrizione'].insert('1.0', task.Descrizione or "")
        self.fields['CategoryId'].set(task.category.Category if task.category else '')
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
class CategoryManagementFrame(ttk.Frame):
    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_category_id = None
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = ('Nr', 'CategoryName')
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        self.tree.heading('Nr', text='Nr.')
        self.tree.column('Nr', width=60, anchor='center')

        self.tree.heading('CategoryName', text=self.lang.get('col_category_name', 'Nome Categoria'))
        self.tree.column('CategoryName', width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_category_select)

        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('category_details_title'), padding=10)
        paned_window.add(form_frame, weight=2)

        # --- CORREZIONE: Assegnazione coerente degli attributi 'self' ---

        # Campo Nome Categoria
        ttk.Label(form_frame, text=self.lang.get('label_category_name')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.field_category = ttk.Entry(form_frame, width=40)
        self.field_category.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Campo Numero Ordine
        ttk.Label(form_frame, text=self.lang.get('label_order_num', 'Numero Ordine:')).grid(row=1, column=0,
                                                                                            sticky=tk.W, pady=5)
        self.field_nr_ordin = ttk.Entry(form_frame, width=40)
        self.field_nr_ordin.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- FINE CORREZIONE ---

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_category).pack(side=tk.LEFT,
                                                                                                       padx=5)

        self._load_categories()

    def _load_categories(self):
        selected_iid_before = self.tree.selection()
        for i in self.tree.get_children(): self.tree.delete(i)

        categories = self.npi_manager.get_categories()
        if categories:
            for cat in categories:
                self.tree.insert('', tk.END, text=str(cat.CategoryId), values=(cat.NrOrdin or '', cat.Category))

        if selected_iid_before and self.tree.exists(selected_iid_before[0]):
            self.tree.selection_set(selected_iid_before[0])

    def _on_category_select(self, event=None):
        if not self.tree.selection(): return

        iid = self.tree.selection()[0]
        self.selected_category_id = int(self.tree.item(iid, 'text'))

        values = self.tree.item(iid, 'values')

        self._clear_form(clear_selection=False)
        # Qui ora i nomi corrispondono a quelli in __init__
        self.field_nr_ordin.insert(0, values[0])
        self.field_category.insert(0, values[1])

    def _clear_form(self, clear_selection=True):
        self.selected_category_id = None
        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

        # Qui ora i nomi corrispondono a quelli in __init__
        self.field_category.delete(0, tk.END)
        self.field_nr_ordin.delete(0, tk.END)

    def _save_category(self):
        # Qui ora i nomi corrispondono a quelli in __init__
        category_name = self.field_category.get().strip()
        nr_ordin_str = self.field_nr_ordin.get().strip()

        if not category_name or not nr_ordin_str:
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('validation_error_category_fields_required'), parent=self)
            return

        try:
            nr_ordin_value = int(nr_ordin_str)
        except ValueError:
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('validation_error_order_num_must_be_integer'), parent=self)
            return

        data = {'Category': category_name, 'NrOrdin': nr_ordin_value}

        try:
            if self.selected_category_id is None:
                self.npi_manager.create_category(data)
            else:
                self.npi_manager.update_category(self.selected_category_id, data)

            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_category_saved'), parent=self)
            self._load_categories()
            self._clear_form()

            try:
                notebook = self.master
                for tab_id in notebook.tabs():
                    widget = notebook.nametowidget(tab_id)
                    # NOTA: Questo modo di trovare il widget è fragile.
                    # Se il nome della classe TaskManagementFrame è in un altro modulo,
                    # è meglio usare isinstance(widget, TaskManagementFrame)
                    if 'TaskManagementFrame' in str(type(widget).__name__):
                        widget.refresh_data()
                        break
            except Exception as e:
                print(f"Avviso: impossibile aggiornare il frame dei task. Errore: {e}")

        except ValueError as ve:
            messagebox.showerror(self.lang.get('error_duplicate_title'), str(ve), parent=self)
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'),
                                 self.lang.get('db_error_generic_save').format(error=e), parent=self)

    def _delete_category(self):
        if self.selected_category_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_category_to_delete'), parent=self)
            return
        if messagebox.askyesno(self.lang.get('confirm_delete_title'), self.lang.get('confirm_delete_category_text'),
                               parent=self):
            try:
                self.npi_manager.delete_category(self.selected_category_id)
                self._load_categories()
                self._clear_form()

                try:
                    notebook = self.master
                    for tab_id in notebook.tabs():
                        widget = notebook.nametowidget(tab_id)
                        if 'TaskManagementFrame' in str(type(widget).__name__):
                            widget.refresh_data()
                            break
                except Exception as e:
                    print(f"Avviso: impossibile aggiornare il frame dei task. Errore: {e}")
            except Exception as e:
                messagebox.showerror(self.lang.get('db_error_title'),
                                     self.lang.get('db_error_delete_category').format(error=e), parent=self)

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