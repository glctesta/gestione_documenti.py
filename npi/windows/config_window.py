# File: npi/windows/config_window.py (VERSIONE DEFINITIVA E CORRETTA)

import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


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
        labels = {'Nome': 'label_subject_name', 'Tipo': 'label_type', 'Email': 'label_email',
                  'TeamsAddress': 'label_msteams_id'}
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
        self.fields['Nome'].insert(0, soggetto.Nome or "")
        self.fields['Email'].insert(0, soggetto.Email or "")
        self.fields['TeamsAddress'].insert(0, soggetto.TeamsAddress or "")

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
        nome = self.fields['Nome'].get()
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

        data = {'Nome': nome, 'Tipo': tipo_db, 'Email': self.fields['Email'].get(),
                'TeamsAddress': self.fields['TeamsAddress'].get()}
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
        
        # Stato ordinamento: {col_index: 'asc'/'desc'}
        self.sort_state = {}
        self.current_data = []  # Cache dei dati per ordinamento
        self.column_names = []  # Nomi delle colonne
        
        self.pack(fill=tk.BOTH, expand=True)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=1)

        cols = (self.lang.get('col_id'), self.lang.get('col_product_code'), self.lang.get('col_product_name'),
                self.lang.get('col_customer'), self.lang.get('label_version', 'Versione'))
        self.column_names = cols
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        
        # Aggiungi binding per ordinamento cliccabile
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col, command=lambda c=i: self._sort_by_column(c))
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

        # Checkbox "aggiungi defaults" (default True)
        self.add_defaults_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            button_frame,
            text=self.lang.get('add_defaults', 'Aggiungi defaults'),
            variable=self.add_defaults_var
        ).pack(side=tk.LEFT, padx=8)
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
        
        # Campo Owner del progetto NPI
        owner_frame = ttk.Frame(project_frame)
        owner_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(owner_frame, text=self.lang.get('project_owner', 'Owner Progetto:')).pack(side=tk.LEFT, padx=(0, 5))
        self.project_owner_combo = ttk.Combobox(owner_frame, state='readonly', width=30)
        self.project_owner_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo Descrizione del progetto NPI
        desc_label_frame = ttk.Frame(project_frame)
        desc_label_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(desc_label_frame, text=self.lang.get('project_description', 'Descrizione Progetto:')).pack(side=tk.LEFT)
        
        self.project_description_text = tk.Text(project_frame, height=4, wrap=tk.WORD, width=40)
        self.project_description_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Sezione Documenti Progetto
        docs_label_frame = ttk.Frame(project_frame)
        docs_label_frame.pack(fill=tk.X, pady=(5, 5))
        ttk.Label(docs_label_frame, text=self.lang.get('project_documents', 'Documenti Progetto:')).pack(side=tk.LEFT)
        
        # Lista documenti
        docs_list_frame = ttk.Frame(project_frame)
        docs_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        cols = (self.lang.get('col_filename', 'Nome File'), 
                self.lang.get('col_filesize', 'Dimensione'))
        self.docs_tree = ttk.Treeview(docs_list_frame, columns=cols, show='headings', height=4)
        self.docs_tree.heading(cols[0], text=cols[0])
        self.docs_tree.heading(cols[1], text=cols[1])
        self.docs_tree.column(cols[0], width=200)
        self.docs_tree.column(cols[1], width=80)
        self.docs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(docs_list_frame, orient=tk.VERTICAL, command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottoni gestione documenti
        docs_buttons = ttk.Frame(project_frame)
        docs_buttons.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(docs_buttons, text=self.lang.get('btn_add_document', 'Aggiungi'), 
                  command=self._add_project_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(docs_buttons, text=self.lang.get('btn_delete', 'Elimina'), 
                  command=self._remove_project_document).pack(side=tk.LEFT, padx=5)
        
        # Inizializza lista documenti temporanea
        self.project_documents = []
        
        self.create_project_button = ttk.Button(project_frame, text=self.lang.get('btn_create_npi_project'),
                                                command=self._create_npi_project, state=tk.DISABLED)
        self.create_project_button.pack(pady=10)

        self._load_products()

    def _load_products(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        products = self.npi_manager.get_prodotti()
        
        # Carica i soggetti per il combobox owner
        soggetti = self.npi_manager.get_soggetti()
        self.soggetti_map = {s.Nome: s.SoggettoId for s in soggetti}
        self.project_owner_combo['values'] = [''] + list(self.soggetti_map.keys())
        
        # Reset cache dati e stato ordinamento
        self.current_data = []
        self.sort_state = {}
        
        if products:
            # Recupera i progetti NPI per ottenere le versioni
            progetti = self.npi_manager.get_progetti_attivi()
            # Crea una mappa prodotto_id -> versione (progetti ora sono dizionari)
            version_map = {p['ProdottoID']: p['Version'] for p in progetti if p.get('Version')}
            
            for p in products:
                version = version_map.get(p.ProdottoID, "")
                row_data = (p.ProdottoID, p.CodiceProdotto or "", p.NomeProdotto, p.Cliente or "", version)
                self.current_data.append(row_data)
                self.tree.insert('', tk.END, values=row_data)
        
        # Reset indicatori ordinamento nelle intestazioni
        self._update_column_headers()

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

    def _sort_by_column(self, col_index):
        """Ordina il treeview per la colonna specificata."""
        if not self.current_data:
            return
        
        # Toggle direzione ordinamento
        if col_index in self.sort_state:
            self.sort_state[col_index] = 'desc' if self.sort_state[col_index] == 'asc' else 'asc'
        else:
            self.sort_state = {col_index: 'asc'}  # Reset altri ordinamenti
        
        # Ordina i dati (gestisci valori None/vuoti)
        reverse = self.sort_state[col_index] == 'desc'
        
        def sort_key(row):
            val = row[col_index]
            # Converti a stringa per ordinamento, gestisci None
            if val is None:
                return ""
            # Per colonna ID (indice 0), ordina numericamente
            if col_index == 0:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    return 0
            return str(val).lower()
        
        sorted_data = sorted(self.current_data, key=sort_key, reverse=reverse)
        
        # Ricarica treeview con dati ordinati
        self._populate_tree(sorted_data)
        
        # Aggiorna indicatore visivo nell'header
        self._update_column_headers()
    
    def _populate_tree(self, data):
        """Popola il treeview con i dati forniti."""
        # Salva selezione corrente
        current_selection = self.tree.selection()
        selected_id = None
        if current_selection:
            try:
                selected_id = self.tree.item(current_selection[0])['values'][0]
            except (IndexError, KeyError):
                pass
        
        # Pulisci e ripopola
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in data:
            self.tree.insert('', tk.END, values=row)
        
        # Ripristina selezione
        if selected_id is not None:
            for item in self.tree.get_children():
                try:
                    if self.tree.item(item)['values'][0] == selected_id:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
                except (IndexError, KeyError):
                    pass
    
    def _update_column_headers(self):
        """Aggiorna le intestazioni delle colonne con indicatori di ordinamento."""
        for i, col_name in enumerate(self.column_names):
            # Rimuovi eventuali frecce esistenti
            base_text = col_name.replace(' ▲', '').replace(' ▼', '')
            
            if i in self.sort_state:
                arrow = ' ▲' if self.sort_state[i] == 'asc' else ' ▼'
                self.tree.heading(self.column_names[i], text=base_text + arrow)
            else:
                self.tree.heading(self.column_names[i], text=base_text)

    def _create_npi_project(self):
        if self.selected_product_id is None:
            messagebox.showwarning(self.lang.get('warning_no_selection_title'),
                                   self.lang.get('warning_select_product_to_create_project'), parent=self)
            return
        
        # Ottieni i dati dal form
        version = self.version_entry.get().strip() or None
        owner_name = self.project_owner_combo.get().strip()
        owner_id = self.soggetti_map.get(owner_name) if owner_name else None
        descrizione = self.project_description_text.get('1.0', tk.END).strip() or None
        
        try:
            add_defaults = bool(getattr(self, 'add_defaults_var', tk.BooleanVar(value=True)).get())
            progetto = self.npi_manager.create_progetto_npi_for_prodotto(
                self.selected_product_id,
                version,
                owner_id=owner_id,
                descrizione=descrizione,
                add_defaults=add_defaults
            )
            if progetto:
                # Salva i documenti allegati
                if self.project_documents:
                    for doc_data in self.project_documents:
                        self.npi_manager.add_progetto_documento(
                            progetto_id=progetto.ProgettoId,
                            nome_file=doc_data['nome'],
                            tipo_file=doc_data['tipo'],
                            dimensione=doc_data['dimensione'],
                            contenuto=doc_data['contenuto'],
                            descrizione=None,
                            caricato_da=None  # TODO: passare utente loggato
                        )
                
                messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_project_created').format(
                    product_name=progetto.prodotto.NomeProdotto), parent=self)
                # Info defaults aggiunti (se richiesto)
                if add_defaults:
                    has_defaults = self.npi_manager.has_default_categories_and_tasks()
                    if not has_defaults:
                        messagebox.showinfo(
                            self.lang.get('info_title', 'Informazione'),
                            self.lang.get('msg_no_default_tasks', 'Nessuna categoria/task default configurata. Progetto creato senza task di default.'),
                            parent=self
                        )

                # Pulisci i campi dopo la creazione
                self.version_entry.delete(0, tk.END)
                self.project_owner_combo.set('')
                self.project_description_text.delete('1.0', tk.END)
                self._clear_project_documents()
                # Ricarica la lista prodotti per mostrare la versione
                self._load_products()
            else:
                # Progetto già esistente - chiedi se aggiornare
                if messagebox.askyesno(
                    self.lang.get('info_title', 'Informazione'),
                    self.lang.get('msg_project_exists_update', 
                                 'Il progetto esiste già. Vuoi aggiornare i dati (owner, descrizione) e aggiungere documenti?'),
                    parent=self
                ):
                    # Recupera il progetto esistente
                    existing_project = self.npi_manager.get_progetto_by_prodotto(self.selected_product_id)
                    if existing_project:
                        # Aggiorna i dati del progetto
                        update_data = {}
                        if version:
                            update_data['Version'] = version
                        if owner_id:
                            update_data['OwnerID'] = owner_id
                        if descrizione:
                            update_data['Descrizione'] = descrizione
                        
                        if update_data:
                            self.npi_manager.update_progetto_npi(existing_project.ProgettoId, update_data)

                        # Se checkbox attivo, aggiungi i default mancanti
                        add_defaults = bool(getattr(self, 'add_defaults_var', tk.BooleanVar(value=True)).get())
                        if add_defaults:
                            added = self.npi_manager.add_default_tasks_to_project(existing_project.ProgettoId)
                            if added == 0:
                                messagebox.showinfo(
                                    self.lang.get('info_title', 'Informazione'),
                                    self.lang.get('msg_no_default_tasks', 'Nessuna categoria/task default configurata. Progetto creato senza task di default.'),
                                    parent=self
                                )
                        
                        # Aggiungi i documenti
                        if self.project_documents:
                            for doc_data in self.project_documents:
                                self.npi_manager.add_progetto_documento(
                                    progetto_id=existing_project.ProgettoId,
                                    nome_file=doc_data['nome'],
                                    tipo_file=doc_data['tipo'],
                                    dimensione=doc_data['dimensione'],
                                    contenuto=doc_data['contenuto'],
                                    descrizione=None,
                                    caricato_da=None
                                )
                        
                        messagebox.showinfo(
                            self.lang.get('success_title', 'Successo'),
                            self.lang.get('msg_project_updated', 'Progetto aggiornato con successo'),
                            parent=self
                        )
                        
                        # Pulisci i campi
                        self.version_entry.delete(0, tk.END)
                        self.project_owner_combo.set('')
                        self.project_description_text.delete('1.0', tk.END)
                        self._clear_project_documents()
                        self._load_products()
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_create_project').format(error=e),
                                 parent=self)
    
    def _add_project_document(self):
        """Aggiunge un documento alla lista temporanea."""
        file_path = filedialog.askopenfilename(
            title=self.lang.get('select_document', 'Seleziona Documento'),
            filetypes=[
                ('Tutti i file', '*.*'),
                ('Immagini', '*.png;*.jpg;*.jpeg;*.gif;*.bmp'),
                ('PDF', '*.pdf'),
                ('Word', '*.doc;*.docx'),
                ('Excel', '*.xls;*.xlsx')
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Leggi il file
            with open(file_path, 'rb') as f:
                contenuto = f.read()
            
            nome_file = os.path.basename(file_path)
            tipo_file = self._get_mime_type(nome_file)
            dimensione = len(contenuto)
            
            # Aggiungi alla lista temporanea
            doc_data = {
                'nome': nome_file,
                'tipo': tipo_file,
                'dimensione': dimensione,
                'contenuto': contenuto
            }
            self.project_documents.append(doc_data)
            
            # Aggiorna la lista visuale
            size_kb = dimensione / 1024
            size_str = f"{size_kb:.1f} KB"
            self.docs_tree.insert('', tk.END, values=(nome_file, size_str))
            
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Impossibile caricare il file:\n{e}",
                parent=self
            )
    
    def _remove_project_document(self):
        """Rimuove un documento dalla lista temporanea."""
        selection = self.docs_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('msg_select_document', 'Seleziona un documento'),
                parent=self
            )
            return
        
        # Ottieni l'indice del documento selezionato
        item = selection[0]
        index = self.docs_tree.index(item)
        
        # Rimuovi dalla lista e dalla treeview
        del self.project_documents[index]
        self.docs_tree.delete(item)
    
    def _clear_project_documents(self):
        """Pulisce la lista documenti."""
        self.project_documents = []
        for item in self.docs_tree.get_children():
            self.docs_tree.delete(item)
    
    def _get_mime_type(self, filename):
        """Determina il MIME type dal nome file."""
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        return mime_types.get(ext, 'application/octet-stream')


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
            ('CategoryId', 'label_category', 'combo'),  # Categoria come primo campo
            ('ItemID', 'label_item_id', 'entry'),
            ('NomeTask', 'label_task_name', 'entry'),
            ('NrOrdin', 'label_order_number', 'entry'),  # Campo per NrOrdin
            ('Descrizione', 'label_description', 'text'),
            ('IsTitle', 'label_is_title', 'check')
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
        
        # Aggiungi evento al combobox della categoria (gestisce sia filtro che suggerimento)
        self.fields['CategoryId'].bind('<<ComboboxSelected>>', self._on_category_changed)

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row_idx, column=0, columnspan=2, pady=20, sticky=tk.E)
        ttk.Button(button_frame, text=self.lang.get('btn_new'), command=self._new_task).pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(button_frame, text=self.lang.get('btn_save'), command=self._save_task)
        self.save_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_delete'), command=self._delete_task).pack(side=tk.LEFT, padx=5)

        try:
            self.refresh_data()
        except Exception as e:
            # Evita che l'intera finestra fallisca se il caricamento task ha errori di schema
            logger = logging.getLogger(__name__)
            logger.error(f"Errore refresh dati TaskManagementFrame: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('db_error_title', 'Errore Database'),
                self.lang.get('db_error_generic_save', '{error}').format(error=e),
                parent=self
            )

    def refresh_data(self):
        # Salva la categoria attualmente selezionata prima del refresh
        current_category = self.fields['CategoryId'].get() if 'CategoryId' in self.fields else None
        self._load_categories_for_combobox(current_category)
        self._load_tasks()

    def _load_categories_for_combobox(self, selected_category=None):
        """Carica le categorie nella combobox con opzione per mostrare tutti i task
        
        Args:
            selected_category: La categoria da mantenere selezionata dopo il caricamento
        """
        categories = self.npi_manager.get_categories()
        self.category_map = {cat.Category: cat.CategoryId for cat in categories}
        
        # Aggiungi "Tutte le categorie" come prima opzione
        all_categories_label = self.lang.get('all_categories', 'Tutte le categorie')
        
        # Ordina alfabeticamente le categorie
        sorted_categories = sorted(self.category_map.keys())
        
        # Costruisci la lista con "Tutte" all'inizio, poi le categorie ordinate
        category_values = [all_categories_label, ""] + sorted_categories
        self.fields['CategoryId']['values'] = category_values
        
        # Ripristina la categoria precedentemente selezionata, se fornita
        if selected_category and selected_category in category_values:
            self.fields['CategoryId'].set(selected_category)
        else:
            self.fields['CategoryId'].current(0)  # Seleziona "Tutte" di default
        
        # NON sovrascrivere l'evento qui - è già collegato nell'__init__

    def _load_tasks(self):
        selected_iid_before = self.tree.selection()

        for i in self.tree.get_children(): 
            self.tree.delete(i)

        # Ottieni la categoria selezionata per il filtro
        selected_category = self.fields['CategoryId'].get() if hasattr(self, 'fields') and 'CategoryId' in self.fields else None
        filter_category_id = None
        
        all_categories_label = self.lang.get('all_categories', 'Tutte le categorie')
        if selected_category and selected_category != all_categories_label and selected_category != '':
            # Se è selezionata una categoria specifica, ottieni il suo ID
            filter_category_id = self.category_map.get(selected_category)

        # Carica i task (filtrati o tutti)
        if filter_category_id is not None:
            # Usa il metodo che filtra per categoria
            tasks = self.npi_manager.get_tasks_by_category(filter_category_id)
        else:
            # Carica tutti i task
            tasks = self.npi_manager.get_catalogo_task()
        
        # Ordina i task per ItemID prima di visualizzarli
        if tasks:
            tasks = sorted(tasks, key=lambda t: t.ItemID or "")
            
            for t in tasks:
                category_name = t.categoria.Category if t.categoria else ""
                tags_to_apply = ()
                if t.IsTitle:
                    tags_to_apply = ('title_row',)

                self.tree.insert(
                    '', tk.END, text=str(t.TaskID),
                    values=(t.ItemID, t.NomeTask, category_name),
                    tags=tags_to_apply
                )

            # Prova a ri-selezionare l'elemento precedente se ancora esiste
            if selected_iid_before:
                if self.tree.exists(selected_iid_before[0]):
                    self.tree.selection_set(selected_iid_before[0])

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
    
    def _on_category_selected(self, event=None):
        """Genera automaticamente un suggerimento per ItemID quando si seleziona una categoria."""
        # Solo per nuovi task (non in modifica)
        if self.selected_task_id is not None:
            return
        
        # Solo se ItemID è vuoto
        if self.fields['ItemID'].get().strip():
            return
        
        category_name = self.fields['CategoryId'].get()
        if not category_name or category_name == self.lang.get('all_categories', 'Tutte le categorie') or category_name == '':
            return
        
        # Ottieni l'ID della categoria
        category_id = self.category_map.get(category_name)
        if not category_id:
            return
        
        try:
            # Ottieni tutti i task di questa categoria
            tasks = self.npi_manager.get_tasks_by_category(category_id)
            
            if not tasks:
                # Nessun task esistente, suggerisci il primo
                # Usa le prime 3 lettere della categoria + "-005"
                prefix = category_name[:3].upper()
                suggested_id = f"{prefix}-005"
            else:
                # Analizza gli ItemID esistenti per trovare il pattern
                item_ids = [t.ItemID for t in tasks if t.ItemID]
                
                if not item_ids:
                    # Nessun ItemID valido, usa default
                    prefix = category_name[:3].upper()
                    suggested_id = f"{prefix}-005"
                else:
                    # Ordina gli ItemID
                    item_ids.sort()
                    last_id = item_ids[-1]
                    
                    # Prova a estrarre il pattern PREFIX-NUMERO
                    import re
                    match = re.match(r'^([A-Za-z]+)-?(\d+)$', last_id)
                    
                    if match:
                        prefix = match.group(1)
                        last_number = int(match.group(2))
                        # Incrementa di 5 (arrotondato al multiplo di 5 superiore)
                        next_number = ((last_number // 5) + 1) * 5
                        suggested_id = f"{prefix}-{next_number:03d}"
                    else:
                        # Pattern non riconosciuto, usa default
                        prefix = category_name[:3].upper()
                        suggested_id = f"{prefix}-005"
            
            # Popola il campo ItemID con il suggerimento
            self.fields['ItemID'].delete(0, tk.END)
            self.fields['ItemID'].insert(0, suggested_id)
            
        except Exception as e:
            # In caso di errore, non fare nulla (l'utente può inserire manualmente)
            import logging
            logging.warning(f"Errore nella generazione del suggerimento ItemID: {e}")

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
        # Disabilita il campo NrOrdin per i nuovi task (verrà calcolato automaticamente)
        self.fields['NrOrdin'].config(state='disabled')
        self.fields['CategoryId'].focus()  # Focus sulla categoria per iniziare
    
    def _new_task(self):
        """Prepara il form per creare un nuovo task."""
        self._clear_form()
        # Aggiorna il testo del bottone per chiarezza
        self.save_button.config(text=self.lang.get('btn_create', 'Crea Nuovo'))
    
    def _on_category_changed(self, event=None):
        """Gestisce il cambio della categoria: filtra i task E suggerisce ItemID."""
        # 1. Filtra i task visualizzati
        self._load_tasks()
        
        # 2. Chiama il metodo esistente per suggerire ItemID
        self._on_category_selected(event)
    
    def _populate_form(self, task):
        """Popola il form con i dati di un task esistente."""
        self._clear_form(clear_selection=False)
        self.selected_task_id = task.TaskID
        self.fields['CategoryId'].set(task.categoria.Category if task.categoria else '')
        self.fields['ItemID'].insert(0, task.ItemID or "")
        self.fields['NomeTask'].insert(0, task.NomeTask or "")
        self.fields['Descrizione'].delete('1.0', tk.END)
        self.fields['Descrizione'].insert('1.0', task.Descrizione or "")
        # Mostra il NrOrdin e rendilo modificabile
        self.fields['NrOrdin'].config(state='normal')
        self.fields['NrOrdin'].delete(0, tk.END)
        self.fields['NrOrdin'].insert(0, str(task.NrOrdin) if task.NrOrdin else "")
        self.is_title_var.set(bool(task.IsTitle))
        # Aggiorna il testo del bottone
        self.save_button.config(text=self.lang.get('btn_save', 'Salva Modifiche'))

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
        """Salva un nuovo task o modifica uno esistente (con conferma)."""
        item_id_str = self.fields['ItemID'].get().strip()
        nome_task_str = self.fields['NomeTask'].get().strip()
        if not item_id_str or not nome_task_str:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('validation_error_task_required'),
                                 parent=self)
            return

        is_new_task = self.selected_task_id is None
        
        # Chiedi conferma
        if is_new_task:
            confirm_msg = f"Confermi la creazione del nuovo task '{item_id_str} - {nome_task_str}'?"
            confirm_title = "Conferma Creazione"
        else:
            confirm_msg = f"Confermi la modifica del task '{item_id_str} - {nome_task_str}'?"
            confirm_title = "Conferma Modifica"
        
        if not messagebox.askyesno(confirm_title, confirm_msg, parent=self):
            return

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
        
        # Se stiamo modificando un task esistente, includi NrOrdin se modificato
        if not is_new_task:
            nr_ordin_str = self.fields['NrOrdin'].get().strip()
            if nr_ordin_str:
                try:
                    data['NrOrdin'] = int(nr_ordin_str)
                except ValueError:
                    messagebox.showerror(self.lang.get('error_title'), 
                                       "Il Numero d'Ordine deve essere un numero intero.",
                                       parent=self)
                    return

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

        # Listbox per i task della categoria
        tasks_label_frame = ttk.LabelFrame(
            form_frame, 
            text=self.lang.get('category_tasks_label', 'Task in questa categoria:'),
            padding=10
        )
        tasks_label_frame.grid(row=len(labels) + 1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        tasks_label_frame.columnconfigure(0, weight=1)
        tasks_label_frame.rowconfigure(0, weight=1)
        
        # Listbox con scrollbar
        tasks_list_frame = ttk.Frame(tasks_label_frame)
        tasks_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tasks_listbox = tk.Listbox(tasks_list_frame, height=10)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tasks_scrollbar = ttk.Scrollbar(tasks_list_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
        
        # Permetti al form di espandersi verticalmente
        form_frame.rowconfigure(len(labels) + 1, weight=1)

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
                    # Verifica se la categoria è usata in progetti
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
                # Carica i task della categoria
                self._load_category_tasks(self.selected_category_id)
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
        
        # Pulisci anche la listbox dei task
        if hasattr(self, 'tasks_listbox'):
            self.tasks_listbox.delete(0, tk.END)

    def _load_category_tasks(self, category_id):
        """Carica i task della categoria selezionata nella listbox."""
        import logging
        logger = logging.getLogger(__name__)
        
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
class DefaultCatalogFrame(ttk.Frame):
    def __init__(self, master, npi_manager, lang, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.selected_category_id = None
        self.selected_task_id = None
        self.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text=self.lang.get('filter_category', 'Filtro categoria')).pack(side=tk.LEFT)
        self.category_filter = ttk.Combobox(top_frame, width=40)
        self.category_filter.pack(side=tk.LEFT, padx=5)
        self.category_filter.bind('<<ComboboxSelected>>', self._on_category_filter_change)
        self.category_filter.bind('<KeyRelease>', self._on_category_filter_change)

        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Categories
        cat_frame = ttk.LabelFrame(paned, text=self.lang.get('tab_categories_title', 'Categorie'), padding=10)
        paned.add(cat_frame, weight=1)

        cat_cols = (self.lang.get('col_category', 'Categoria'),
                    self.lang.get('col_default_category', 'DefaultCategory'))
        self.cat_tree = ttk.Treeview(cat_frame, columns=cat_cols, show='headings', selectmode='browse')
        for col in cat_cols:
            self.cat_tree.heading(col, text=col)
        self.cat_tree.column(cat_cols[0], width=200)
        self.cat_tree.column(cat_cols[1], width=120, anchor=tk.CENTER)
        self.cat_tree.pack(fill=tk.BOTH, expand=True)
        self.cat_tree.bind('<<TreeviewSelect>>', self._on_category_select)
        self.cat_tree.bind('<Double-1>', self._toggle_category_default)

        # Right: Tasks
        task_frame = ttk.LabelFrame(paned, text=self.lang.get('tab_task_catalog_title', 'Catalogo Task'), padding=10)
        paned.add(task_frame, weight=1)

        filter_row = ttk.Frame(task_frame)
        filter_row.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(filter_row, text=self.lang.get('filter_task', 'Filtro task')).pack(side=tk.LEFT)
        self.task_filter = ttk.Entry(filter_row, width=30)
        self.task_filter.pack(side=tk.LEFT, padx=5)
        self.task_filter.bind('<KeyRelease>', self._on_task_filter_change)

        task_cols = (self.lang.get('col_task_name', 'Nome Task'),
                     self.lang.get('col_default_task', 'DefaultTask'))
        self.task_tree = ttk.Treeview(task_frame, columns=task_cols, show='headings', selectmode='browse')
        for col in task_cols:
            self.task_tree.heading(col, text=col)
        self.task_tree.column(task_cols[0], width=250)
        self.task_tree.column(task_cols[1], width=120, anchor=tk.CENTER)
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        self.task_tree.bind('<<TreeviewSelect>>', self._on_task_select)
        self.task_tree.bind('<Double-1>', self._toggle_task_default)

        self._load_categories()

    def _load_categories(self):
        self.categories = self.npi_manager.get_categories() or []
        self.categories = sorted(self.categories, key=lambda c: (c.Category or '').lower())
        names = [c.Category for c in self.categories if c.Category]
        self.category_filter['values'] = names
        self._apply_category_filter()

    def _apply_category_filter(self):
        filter_text = (self.category_filter.get() or '').strip().lower()
        for i in self.cat_tree.get_children():
            self.cat_tree.delete(i)
        for cat in self.categories:
            if filter_text and filter_text not in (cat.Category or '').lower():
                continue
            default_val = 1 if getattr(cat, 'DefaultCategory', False) else 0
            self.cat_tree.insert('', tk.END, iid=str(cat.CategoryId), values=(cat.Category, default_val))
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)

    def _on_category_filter_change(self, event=None):
        self._apply_category_filter()

    def _on_category_select(self, event=None):
        selection = self.cat_tree.selection()
        if not selection:
            return
        self.selected_category_id = int(selection[0])
        self._load_tasks_for_category(self.selected_category_id)

    def _load_tasks_for_category(self, category_id):
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)
        tasks = self.npi_manager.get_catalogo_task_by_category(category_id) or []
        tasks = sorted(tasks, key=lambda t: (t.NomeTask or '').lower())
        filter_text = (self.task_filter.get() or '').strip().lower() if hasattr(self, 'task_filter') else ''
        for task in tasks:
            if filter_text and filter_text not in (task.NomeTask or '').lower():
                continue
            default_val = 1 if getattr(task, 'DefaultTask', False) else 0
            self.task_tree.insert('', tk.END, iid=str(task.TaskID), values=(task.NomeTask, default_val))

    def _on_task_select(self, event=None):
        selection = self.task_tree.selection()
        if selection:
            self.selected_task_id = int(selection[0])

    def _on_task_filter_change(self, event=None):
        if self.selected_category_id:
            self._load_tasks_for_category(self.selected_category_id)

    def _toggle_category_default(self, event=None):
        selection = self.cat_tree.selection()
        if not selection:
            return
        category_id = int(selection[0])
        current_val = int(self.cat_tree.item(selection[0], 'values')[1])
        new_val = 0 if current_val == 1 else 1
        try:
            if new_val == 0:
                if not messagebox.askyesno(
                        self.lang.get('confirm_title', 'Conferma'),
                        self.lang.get(
                            'confirm_unset_default_category',
                            'Disattivare la categoria di default? Tutti i task di questa categoria verranno azzerati.'
                        ),
                        parent=self
                ):
                    # Non cambiare valore se l'utente annulla
                    return
                # Azzerare i task default della categoria
                self.npi_manager.set_default_tasks_for_category(category_id, False)
            self.npi_manager.update_category_default_flag(category_id, new_val == 1)
            self.cat_tree.set(selection[0], column=1, value=new_val)
            # Se disattivata, aggiorna la lista task per riflettere lo zeroing
            if new_val == 0 and self.selected_category_id == category_id:
                self._load_tasks_for_category(category_id)
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title', 'Errore Database'),
                                 self.lang.get('db_error_generic_save', '{error}').format(error=e), parent=self)

    def _toggle_task_default(self, event=None):
        selection = self.task_tree.selection()
        if not selection:
            return
        task_id = int(selection[0])
        current_val = int(self.task_tree.item(selection[0], 'values')[1])
        new_val = 0 if current_val == 1 else 1
        try:
            self.npi_manager.update_task_default_flag(task_id, new_val == 1)
            self.task_tree.set(selection[0], column=1, value=new_val)
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title', 'Errore Database'),
                                 self.lang.get('db_error_generic_save', '{error}').format(error=e), parent=self)


class NpiConfigWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, authorized_user, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.authorized_user = authorized_user
        self.app_master = master  # Salviamo un riferimento alla finestra principale App

        self.title(self.lang.get('config_window_title'))
        self.geometry("1200x900")
        self.transient(master)
        self.grab_set()

        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.subj_frame = SubjectManagementFrame(notebook, self.npi_manager, self.lang)
        self.prod_frame = ProductManagementFrame(notebook, self.npi_manager, self.lang)
        self.cat_frame = CategoryManagementFrame(notebook, self.npi_manager, self.lang)
        self.task_frame = TaskManagementFrame(notebook, self.npi_manager, self.lang)
        self.defaults_frame = DefaultCatalogFrame(notebook, self.npi_manager, self.lang)

        notebook.add(self.subj_frame, text=self.lang.get('tab_subjects_title'))
        notebook.add(self.prod_frame, text=self.lang.get('tab_products_title'))
        notebook.add(self.cat_frame, text=self.lang.get('tab_categories_title'))
        notebook.add(self.task_frame, text=self.lang.get('tab_task_catalog_title'))
        notebook.add(self.defaults_frame, text=self.lang.get('tab_defaults_title', 'Defaults'))

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
        # Aggiungi evento per filtrare i task quando cambia la categoria
        self.fields['CategoryId'].bind('<<ComboboxSelected>>', self._on_category_filter_change)

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
        """Carica le categorie nella combobox con opzione per mostrare tutti i task"""
        import logging
        logger = logging.getLogger(__name__)
        
        categories = self.npi_manager.get_categories()
        if categories:
            self.category_map = {cat.Category: cat.CategoryId for cat in categories}
            self.category_map_rev = {cat.CategoryId: cat.Category for cat in categories}
            
            # Aggiungi "Tutte le categorie" come prima opzione per il filtro
            all_categories_label = self.lang.get('all_categories', 'Tutte le categorie')
            category_values = [all_categories_label] + list(self.category_map.keys())
            self.fields['CategoryId']['values'] = tuple(category_values)
            self.fields['CategoryId'].current(0)  # Seleziona "Tutte" di default
            
            logger.info(f"📋 Combobox categorie popolata con {len(category_values)} voci (incluso '{all_categories_label}')")
            print(f"📋 DEBUG: Combobox categorie popolata con {len(category_values)} voci")
            print(f"   Prima voce: '{category_values[0]}'")

    def _load_tasks(self):
        """Carica i task nella lista, applicando il filtro per categoria se selezionato"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Ottieni la categoria selezionata dalla combobox
        selected_category = self.fields['CategoryId'].get() if hasattr(self, 'fields') and 'CategoryId' in self.fields else None
        filter_category_id = None
        
        all_categories_label = self.lang.get('all_categories', 'Tutte le categorie')
        if selected_category and selected_category != all_categories_label and selected_category != '':
            # Se è selezionata una categoria specifica, ottieni il suo ID
            filter_category_id = self.category_map.get(selected_category)

        session = self.npi_manager.Session()
        try:
            from ..data_models import TaskCatalogo
            from sqlalchemy.orm import joinedload

            query = session.query(TaskCatalogo).options(
                joinedload(TaskCatalogo.categoria)
            )
            
            # Applica il filtro se una categoria è selezionata
            if filter_category_id is not None:
                query = query.filter(TaskCatalogo.CategoryId == filter_category_id)
            
            tasks = query.all()

            for task in tasks:
                category_name = task.categoria.Category if task.categoria else ""
                self.tree.insert('', tk.END, values=(
                    task.ItemID,
                    task.NomeTask,
                    category_name
                ))
        finally:
            session.close()

    def _on_category_filter_change(self, event=None):
        """Gestisce il cambio della categoria nella combobox per filtrare i task"""
        import logging
        logger = logging.getLogger(__name__)
        selected = self.fields['CategoryId'].get()
        logger.info(f"🔍 Filtro categoria cambiato: '{selected}'")
        print(f"🔍 DEBUG: Filtro categoria cambiato: '{selected}'")
        self._load_tasks()

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
