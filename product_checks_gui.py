"""
Modulo per la gestione delle verifiche periodiche sui prodotti.
Gestisce:
- Configurazione periodicità verifiche per prodotto
- Gestione task di verifica (generici e specifici)
- Esecuzione verifiche con checklist
- Report verifiche (da completare)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
import os
import subprocess
from datetime import datetime


class ProductChecksManagementWindow(tk.Toplevel):
    """Finestra per la gestione della periodicità delle verifiche prodotti"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_id

        self.title(self.lang.get('product_checks_mgmt_title', 'Gestione Verifiche Prodotti'))
        self.geometry('900x600')
        self.transient(parent)

        self._current_check_id = None
        self._build_ui()
        self._load_products()
        self._load_checks()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale diviso in due colonne
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form inserimento
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('product_check_form', 'Configurazione Verifica'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Combo prodotti
        ttk.Label(left_frame, text=self.lang.get('product', 'Prodotto') + ' *').grid(row=0, column=0, sticky='w',
                                                                                     padx=5, pady=5)
        self.product_combo = ttk.Combobox(left_frame, state='readonly', width=40)
        self.product_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Periodicità in quantità
        ttk.Label(left_frame, text=self.lang.get('periodicity_qty', 'Periodicità (Quantità)') + ' *').grid(row=1,
                                                                                                           column=0,
                                                                                                           sticky='w',
                                                                                                           padx=5,
                                                                                                           pady=5)
        self.periodicity_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.periodicity_var, width=20).grid(row=1, column=1, sticky='w', padx=5,
                                                                                pady=5)

        # Pulsanti azione
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'), command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'), command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'), command=self._on_delete).pack(side='left',
                                                                                                         padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista verifiche configurate
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('configured_checks', 'Verifiche Configurate'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Treeview
        columns = ('id', 'product_code', 'product_name', 'periodicity')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        self.tree.heading('id', text='ID')
        self.tree.heading('product_code', text=self.lang.get('product_code', 'Codice'))
        self.tree.heading('product_name', text=self.lang.get('product_name', 'Nome Prodotto'))
        self.tree.heading('periodicity', text=self.lang.get('periodicity', 'Periodicità'))

        self.tree.column('id', width=50)
        self.tree.column('product_code', width=120)
        self.tree.column('product_name', width=250)
        self.tree.column('periodicity', width=100)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_products(self):
        """Carica la lista prodotti nel combo"""
        products = self.db.fetch_products_for_checks()
        self.products_dict = {f"{p.ProductCode} - {p.ProductName}": p.IDProduct for p in products}
        self.product_combo['values'] = list(self.products_dict.keys())

    def _load_checks(self):
        """Carica le verifiche configurate"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        checks = self.db.fetch_all_product_checks()
        for check in checks:
            self.tree.insert('', 'end', values=(
                check.PeriodicalProductCheckId,
                check.ProductCode,
                check.ProductName,
                check.PeriodicityInQty
            ))

    def _on_select(self, event):
        """Gestisce la selezione di una riga"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_check_id = values[0]
        # Trova il prodotto nel combo
        product_key = f"{values[1]} - {values[2]}"
        if product_key in self.products_dict:
            self.product_combo.set(product_key)
        self.periodicity_var.set(str(values[3]))

    def _on_new(self):
        """Pulisce il form per nuovo inserimento"""
        self._current_check_id = None
        self.product_combo.set('')
        self.periodicity_var.set('')

    def _on_save(self):
        """Salva o aggiorna una verifica"""
        # Validazione
        if not self.product_combo.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('select_product', 'Selezionare un prodotto'))
            return

        try:
            periodicity = int(self.periodicity_var.get())
            if periodicity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('invalid_periodicity', 'Inserire una periodicità valida (numero > 0)'))
            return

        product_id = self.products_dict[self.product_combo.get()]

        if self._current_check_id:
            # Update
            success = self.db.update_product_check(self._current_check_id, product_id, periodicity)
        else:
            # Insert
            success = self.db.insert_product_check(product_id, periodicity)

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                                self.lang.get('check_saved', 'Verifica salvata con successo'))
            self._load_checks()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('save_error', 'Errore durante il salvataggio'))

    def _on_delete(self):
        """Elimina una verifica"""
        if not self._current_check_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('select_check', 'Selezionare una verifica da eliminare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                               self.lang.get('confirm_delete_check', 'Eliminare la verifica selezionata?')):
            if self.db.delete_product_check(self._current_check_id):
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                                    self.lang.get('check_deleted', 'Verifica eliminata'))
                self._load_checks()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                     self.lang.get('delete_error', 'Errore durante l\'eliminazione'))


class CheckTasksManagementWindow(tk.Toplevel):
    """Finestra per la gestione dei task di verifica (generici e specifici)"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_id

        self.title(self.lang.get('check_tasks_mgmt_title', 'Gestione Task di Verifica'))
        self.geometry('1000x700')
        self.transient(parent)

        self._current_task_id = None
        self._doc_data = None
        self._build_ui()
        self._load_products()
        self._load_tasks()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('task_form', 'Task di Verifica'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Azione da eseguire
        ttk.Label(left_frame, text=self.lang.get('item_to_check', 'Azione da Eseguire') + ' *').grid(row=0, column=0,
                                                                                                     sticky='w', padx=5,
                                                                                                     pady=5)
        self.item_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Checkbox IsGeneric
        self.is_generic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_frame, text=self.lang.get('is_generic', 'Task Generico'),
                        variable=self.is_generic_var, command=self._on_generic_changed).grid(row=1, column=0,
                                                                                             columnspan=2, sticky='w',
                                                                                             padx=5, pady=5)

        # Combo prodotti (disabilitato se generico)
        ttk.Label(left_frame, text=self.lang.get('specific_product', 'Prodotto Specifico')).grid(row=2, column=0,
                                                                                                 sticky='w', padx=5,
                                                                                                 pady=5)
        self.product_combo = ttk.Combobox(left_frame, state='disabled', width=47)
        self.product_combo.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # Documento allegato
        doc_frame = ttk.Frame(left_frame)
        doc_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        ttk.Label(doc_frame, text=self.lang.get('document', 'Documento')).pack(side='left')
        ttk.Button(doc_frame, text=self.lang.get('btn_upload', 'Carica'), command=self._upload_doc).pack(side='left',
                                                                                                         padx=5)
        self.doc_label = ttk.Label(doc_frame, text='', foreground='blue')
        self.doc_label.pack(side='left', padx=5)

        # Pulsanti azione
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'), command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'), command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'), command=self._on_delete).pack(side='left',
                                                                                                         padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista task
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('configured_tasks', 'Task Configurati'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        columns = ('id', 'item', 'is_generic', 'product', 'has_doc', 'user', 'date')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=25)
        self.tree.heading('id', text='ID')
        self.tree.heading('item', text=self.lang.get('item', 'Azione'))
        self.tree.heading('is_generic', text=self.lang.get('type', 'Tipo'))
        self.tree.heading('product', text=self.lang.get('product', 'Prodotto'))
        self.tree.heading('has_doc', text=self.lang.get('doc', 'Doc'))
        self.tree.heading('user', text=self.lang.get('user', 'Utente'))
        self.tree.heading('date', text=self.lang.get('date', 'Data'))

        self.tree.column('id', width=50)
        self.tree.column('item', width=250)
        self.tree.column('is_generic', width=80)
        self.tree.column('product', width=150)
        self.tree.column('has_doc', width=50)
        self.tree.column('user', width=100)
        self.tree.column('date', width=100)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-Button-1>', self._on_double_click)

    def _on_generic_changed(self):
        """Gestisce il cambio dello stato del checkbox IsGeneric"""
        if self.is_generic_var.get():
            self.product_combo.set('')
            self.product_combo.config(state='disabled')
        else:
            self.product_combo.config(state='readonly')

    def _load_products(self):
        """Carica i prodotti con verifiche configurate"""
        products = self.db.fetch_products_with_checks()
        self.products_dict = {f"{p.ProductCode} - {p.ProductName}": p.PeriodicalProductCheckId for p in products}
        self.product_combo['values'] = list(self.products_dict.keys())

    def _load_tasks(self):
        """Carica i task configurati"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        tasks = self.db.fetch_all_check_tasks()
        for task in tasks:
            self.tree.insert('', 'end', values=(
                task.PriodicalProductCheckListId,
                task.ItemToCheck,
                self.lang.get('generic', 'Generico') if task.IsGeneric else self.lang.get('specific', 'Specifico'),
                task.ProductCode or '',
                '✓' if task.Doc else '',
                task.UserType,
                task.DateIn.strftime('%d/%m/%Y') if task.DateIn else ''
            ))

    def _upload_doc(self):
        """Carica un documento"""
        file_path = filedialog.askopenfilename(
            title=self.lang.get('select_document', 'Seleziona Documento'),
            filetypes=[
                ('PDF', '*.pdf'),
                ('Word', '*.doc;*.docx'),
                ('Excel', '*.xls;*.xlsx'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self._doc_data = f.read()
                self.doc_label.config(text=os.path.basename(file_path))
            except Exception as e:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                     f"{self.lang.get('upload_error', 'Errore caricamento')}: {str(e)}")

    def _on_select(self, event):
        """Gestisce la selezione di una riga"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_task_id = values[0]

        # Carica i dettagli del task
        task = self.db.fetch_check_task_by_id(self._current_task_id)
        if task:
            self.item_var.set(task.ItemToCheck)
            self.is_generic_var.set(task.IsGeneric)
            self._on_generic_changed()

            if not task.IsGeneric and task.ProductCode:
                product_key = f"{task.ProductCode} - {task.ProductName}"
                if product_key in self.products_dict:
                    self.product_combo.set(product_key)

            self._doc_data = task.Doc
            if task.Doc:
                self.doc_label.config(text=self.lang.get('doc_present', 'Documento presente'))
            else:
                self.doc_label.config(text='')

    def _on_double_click(self, event):
        """Apre il documento se presente"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        task_id = item['values'][0]

        task = self.db.fetch_check_task_by_id(task_id)
        if task and task.Doc:
            self._open_document(task.Doc)

    def _open_document(self, doc_data):
        """Apre un documento binario"""
        try:
            # Crea un file temporaneo
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(doc_data)
                tmp_path = tmp_file.name

            # Apre il file con l'applicazione predefinita
            if os.name == 'nt':  # Windows
                os.startfile(tmp_path)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.call(['xdg-open', tmp_path])
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 f"{self.lang.get('open_error', 'Errore apertura documento')}: {str(e)}")

    def _on_new(self):
        """Pulisce il form"""
        self._current_task_id = None
        self.item_var.set('')
        self.is_generic_var.set(True)
        self.product_combo.set('')
        self._doc_data = None
        self.doc_label.config(text='')
        self._on_generic_changed()

    def _on_save(self):
        """Salva o aggiorna un task"""
        # Validazione
        if not self.item_var.get().strip():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('enter_item', 'Inserire l\'azione da eseguire'))
            return

        is_generic = self.is_generic_var.get()
        product_check_id = None

        if not is_generic:
            if not self.product_combo.get():
                messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                       self.lang.get('select_product', 'Selezionare un prodotto'))
                return
            product_check_id = self.products_dict[self.product_combo.get()]

        if self._current_task_id:
            # Update
            success = self.db.update_check_task(
                self._current_task_id,
                self.item_var.get().strip(),
                is_generic,
                self.user_name,
                self._doc_data,
                product_check_id
            )
        else:
            # Insert
            success = self.db.insert_check_task(
                self.item_var.get().strip(),
                is_generic,
                self.user_name,
                self._doc_data,
                product_check_id
            )

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                                self.lang.get('task_saved', 'Task salvato con successo'))
            self._load_tasks()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('save_error', 'Errore durante il salvataggio'))

    def _on_delete(self):
        """Elimina un task (soft delete)"""
        if not self._current_task_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('select_task', 'Selezionare un task da eliminare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                               self.lang.get('confirm_delete_task', 'Eliminare il task selezionato?')):
            if self.db.delete_check_task(self._current_task_id):
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                                    self.lang.get('task_deleted', 'Task eliminato'))
                self._load_tasks()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                     self.lang.get('delete_error', 'Errore durante l\'eliminazione'))


class ProductVerificationWindow(tk.Toplevel):
    """Finestra per l'esecuzione delle verifiche sui prodotti"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_id

        self.title(self.lang.get('product_verification_title', 'Esecuzione Verifiche Prodotti'))
        self.geometry('1200x750')
        self.transient(parent)

        self._current_must_check_id = None
        self._current_label_code_id = None  # Nuovo campo per memorizzare l'IDLabelCode
        self._check_items = []
        self._build_ui()
        self._load_products_to_check()
        # FORZA IL CARICAMENTO DEI TASK GENERICI ALL'APERTURA
        self.after(100, self._load_generic_tasks_only)

    def _load_generic_tasks_only(self):
        """Carica solo i task generici all'apertura della finestra"""
        self._load_checklist()

    def _on_label_code_changed(self, *args):
        """Verifica il label code quando viene modificato"""
        label_code = self.label_code_var.get().strip()

        if not label_code or not self._current_must_check_id:
            self.label_code_status_label.config(text='')
            self._current_label_code_id = None  # Reset IDLabelCode
            return

        # Esegui verifica dopo un breve delay per evitare troppe query
        self.after(500, self._perform_label_code_check, label_code)

    def _perform_label_code_check(self, label_code):
        """Esegue la verifica effettiva del label code"""
        if label_code != self.label_code_var.get().strip():
            return  # Il testo è cambiato durante il delay

        try:
            label_code_id = self.db.check_label_code_exists(label_code, self._current_must_check_id)

            if label_code_id:
                self.label_code_status_label.config(text='✓', foreground='green')
                self._current_label_code_id = label_code_id  # Memorizza l'IDLabelCode
            else:
                self.label_code_status_label.config(text='✗', foreground='red')
                self._current_label_code_id = None  # Reset IDLabelCode
                # Mostra messaggio di avviso
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('Label_Not_Found', 'Etichetta non trovata o non relativa al prodotto selezionato'),
                    parent=self
                )

        except Exception as e:
            self.label_code_status_label.config(text='', foreground='black')
            self._current_label_code_id = None  # Reset IDLabelCode
            #logger.error(f"Error during label code verification: {e}")

    def _on_result_changed(self, event=None):
        """Gestisce il cambio del risultato (mostra/nasconde campo commento)"""
        if self.result_var.get() == 'FAIL':
            self.comment_label.grid()
            self.comment_text.grid()
            self.comment_label.configure(text=self.lang.get('Comments', 'Commenti') + ' *')
        else:
            self.comment_label.grid_remove()
            self.comment_text.grid_remove()

    def _load_products_to_check(self):
        """Carica i prodotti che necessitano verifica"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        products = self.db.fetch_products_must_check()
        for product in products:
            self.products_tree.insert('', 'end', values=(
                product.PeriodicalProductCheckMustListId,
                product.ordernumber,
                product.productcode,
                product.PhaseName,
                product.Date,
                product.Ora
            ))

    def _build_ui(self):

        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale con due listbox affiancate
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Listbox sinistra: Prodotti da verificare
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('products_to_check', 'Prodotti da Verificare'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        columns_left = ('id', 'order', 'product', 'phase', 'date', 'time')
        self.products_tree = ttk.Treeview(left_frame, columns=columns_left, show='headings', height=25)
        self.products_tree.heading('id', text='ID')
        self.products_tree.heading('order', text=self.lang.get('order', 'Ordine'))
        self.products_tree.heading('product', text=self.lang.get('product', 'Prodotto'))
        self.products_tree.heading('phase', text=self.lang.get('phase', 'Fase'))
        self.products_tree.heading('date', text=self.lang.get('date', 'Data'))
        self.products_tree.heading('time', text=self.lang.get('time', 'Ora'))

        self.products_tree.column('id', width=50)
        self.products_tree.column('order', width=120)
        self.products_tree.column('product', width=120)
        self.products_tree.column('phase', width=150)
        self.products_tree.column('date', width=100)
        self.products_tree.column('time', width=80)

        scroll_left = ttk.Scrollbar(left_frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scroll_left.set)

        self.products_tree.pack(side='left', fill='both', expand=True)
        scroll_left.pack(side='right', fill='y')

        self.products_tree.bind('<<TreeviewSelect>>', self._on_product_select)

        # Listbox destra: Checklist
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('checklist', 'Checklist Verifica'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Frame per input dati verifica
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill='x', padx=5, pady=5)

        # Frame per label code con verifica
        label_frame = ttk.Frame(input_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=2)

        ttk.Label(label_frame, text=self.lang.get('label_code', 'Codice Label') + ' *').pack(side='left')

        # Frame per entry e icona verifica
        entry_frame = ttk.Frame(label_frame)
        entry_frame.pack(side='left', fill='x', expand=True, padx=(10, 5))

        self.label_code_var = tk.StringVar()
        self.label_code_entry = ttk.Entry(entry_frame, textvariable=self.label_code_var, width=20)
        self.label_code_entry.pack(side='left', fill='x', expand=True)

        # Icona verifica label code
        self.label_code_status_label = ttk.Label(entry_frame, text='', font=('Arial', 12))
        self.label_code_status_label.pack(side='left', padx=5)

        # Bind per verifica in tempo reale
        self.label_code_var.trace('w', self._on_label_code_changed)

        ttk.Label(input_frame, text=self.lang.get('result', 'Risultato') + ' *').grid(row=1, column=0, sticky='w',
                                                                                      padx=5, pady=2)
        self.result_var = tk.StringVar()
        self.result_combo = ttk.Combobox(input_frame, textvariable=self.result_var, state='readonly', width=18)
        self.result_combo['values'] = ['PASS', 'FAIL']
        self.result_combo.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.result_combo.bind('<<ComboboxSelected>>', self._on_result_changed)

        # Campo commento (visibile solo quando risultato è FAIL)
        self.comment_label = ttk.Label(input_frame, text=self.lang.get('Comments', 'Commenti'))
        self.comment_label.grid(row=2, column=0, sticky='nw', padx=5, pady=2)

        self.comment_text = tk.Text(input_frame, width=40, height=4)
        self.comment_text.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        # Nascondi inizialmente il campo commento
        self.comment_label.grid_remove()
        self.comment_text.grid_remove()

        input_frame.columnconfigure(1, weight=1)

        # Treeview per checklist con checkbox
        columns_right = ('check', 'id', 'item', 'doc')
        self.checklist_tree = ttk.Treeview(right_frame, columns=columns_right, show='tree headings', height=15)
        self.checklist_tree.heading('#0', text='✓')
        self.checklist_tree.heading('check', text='')
        self.checklist_tree.heading('id', text='ID')
        self.checklist_tree.heading('item', text=self.lang.get('item', 'Azione'))
        self.checklist_tree.heading('doc', text=self.lang.get('doc', 'Doc'))

        self.checklist_tree.column('#0', width=30)
        self.checklist_tree.column('check', width=0, stretch=False)
        self.checklist_tree.column('id', width=50)
        self.checklist_tree.column('item', width=350)
        self.checklist_tree.column('doc', width=50)

        scroll_right = ttk.Scrollbar(right_frame, orient='vertical', command=self.checklist_tree.yview)
        self.checklist_tree.configure(yscrollcommand=scroll_right.set)

        self.checklist_tree.pack(side='top', fill='both', expand=True, padx=5)

        # Frame per i pulsanti
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', padx=5, pady=10)

        ttk.Button(btn_frame, text=self.lang.get('Save_Verification', 'Salva Verifica'),
                   command=self._on_save_verification, style='Accent.TButton').pack(side='left', padx=5)

        ttk.Button(btn_frame, text=self.lang.get('Clear', 'Pulisci'),
                   command=self._clear_verification_form).pack(side='left', padx=5)

        scroll_right.pack(side='right', fill='y')

        self.checklist_tree.bind('<Button-1>', self._on_checklist_click)
        self.checklist_tree.bind('<Double-Button-1>', self._on_checklist_double_click)

    def _on_product_select(self, event):
        """Gestisce la selezione di un prodotto da verificare"""
        selection = self.products_tree.selection()
        if not selection:
            return

        item = self.products_tree.item(selection[0])
        self._current_must_check_id = item['values'][0]

        # Reset status label code quando cambia prodotto
        self.label_code_status_label.config(text='')
        self._current_label_code_id = None  # Reset IDLabelCode

        # Carica la checklist per questo prodotto
        self._load_checklist()

    def _load_checklist(self):
        """Carica la checklist per il prodotto selezionato"""
        for item in self.checklist_tree.get_children():
            self.checklist_tree.delete(item)

        self._check_items = []

        print(f"=== DEBUG CHECKLIST LOADING ===")
        print(f"Current must check ID: {self._current_must_check_id}")

        # CARICA SEMPRE I TASK GENERICI (anche senza prodotto selezionato)
        generic_tasks = self.db.fetch_generic_check_tasks()
        print(f"Generic tasks type: {type(generic_tasks)}")
        print(f"Generic tasks length: {len(generic_tasks)}")

        for task in generic_tasks:
            print(f"Generic task: {task.ItemToCheck}")
            item_id = self.checklist_tree.insert('', 'end', text='☐', values=(
                False,
                task.PriodicalProductCheckListId,
                task.ItemToCheck,
                '✓' if task.Doc else ''
            ))
            self._check_items.append({
                'tree_id': item_id,
                'task_id': task.PriodicalProductCheckListId,
                'checked': False,
                'doc': task.Doc
            })

        # CARICA TASK SPECIFICI solo se c'è un prodotto selezionato
        if self._current_must_check_id:
            specific_tasks = self.db.fetch_specific_check_tasks(self._current_must_check_id)
            print(f"Found {len(specific_tasks)} specific tasks")
            print(f"Specific tasks length: {len(specific_tasks)}")

            for task in specific_tasks:
                print(f"Specific task: {task.ItemToCheck}")
                item_id = self.checklist_tree.insert('', 'end', text='☐', values=(
                    False,
                    task.PriodicalProductCheckListId,
                    task.ItemToCheck,
                    '✓' if task.Doc else ''
                ))
                self._check_items.append({
                    'tree_id': item_id,
                    'task_id': task.PriodicalProductCheckListId,
                    'checked': False,
                    'doc': task.Doc
                })

        print(f"Total checklist items: {len(self._check_items)}")
        print(f"Tree children count: {len(self.checklist_tree.get_children())}")

    def _on_checklist_click(self, event):
        """Gestisce il click sulla checklist (toggle checkbox)"""
        region = self.checklist_tree.identify('region', event.x, event.y)
        if region == 'tree':
            item_id = self.checklist_tree.identify_row(event.y)
            if item_id:
                # Toggle checkbox
                for check_item in self._check_items:
                    if check_item['tree_id'] == item_id:
                        check_item['checked'] = not check_item['checked']
                        new_symbol = '☑' if check_item['checked'] else '☐'
                        self.checklist_tree.item(item_id, text=new_symbol)
                        break

    def _on_checklist_double_click(self, event):
        """Apre il documento se presente"""
        item_id = self.checklist_tree.identify_row(event.y)
        if item_id:
            for check_item in self._check_items:
                if check_item['tree_id'] == item_id and check_item['doc']:
                    task = self.db.fetch_check_task_by_id(check_item['task_id'])
                    if task and task.Doc:
                        self._open_document(task.Doc)
                    break

    def _open_document(self, doc_data):
        """Apre un documento binario"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(doc_data)
                tmp_path = tmp_file.name

            if os.name == 'nt':
                os.startfile(tmp_path)
            elif os.name == 'posix':
                subprocess.call(['xdg-open', tmp_path])
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 f"{self.lang.get('open_error', 'Errore apertura')}: {str(e)}")

    def _on_save_verification(self):
        """Salva la verifica completata"""
        # Validazione
        if not self._current_must_check_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_product_to_check', 'Selezionare un prodotto da verificare'),
                parent=self
            )
            return

        if not self.label_code_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_label_code', 'Inserire il codice label'),
                parent=self
            )
            return

        if not self._current_label_code_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('Label_Not_Found', 'Etichetta non trovata o non relativa al prodotto selezionato'),
                parent=self
            )
            return

        if not self.result_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_result', 'Selezionare il risultato (PASS/FAIL)'),
                parent=self
            )
            return

        # Validazione commento obbligatorio per FAIL
        comments = self.comment_text.get('1.0', 'end-1c').strip()
        if self.result_var.get() == 'FAIL' and not comments:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('Comments_Required_For_Fail', 'Il campo commenti è obbligatorio per risultato FAIL'),
                parent=self
            )
            return

        # Verifica che tutti i checkbox siano spuntati
        all_checked = all(item['checked'] for item in self._check_items)
        if not all_checked:
            if not messagebox.askyesno(
                    self.lang.get('confirm', 'Conferma'),
                    self.lang.get('not_all_checked', 'Non tutti gli item sono stati verificati. Continuare?'),
                    parent=self
            ):
                return

        # Salva nel database usando l'IDLabelCode
        success = self.db.save_product_verification(
            must_check_id=self._current_must_check_id,
            user_name=self.user_name,
            label_code_id=self._current_label_code_id,  # Usa l'IDLabelCode invece del codice testo
            status=self.result_var.get(),
            comments=comments if self.result_var.get() == 'FAIL' else None
        )

        if success:
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('verification_saved', 'Verifica salvata con successo'),
                parent=self
            )
            # Ricarica la lista prodotti
            self._load_products_to_check()
            # Pulisci il form
            self._clear_verification_form()
        else:
            # Gestione errori specifici
            error_msg = self.lang.get('save_error', 'Errore durante il salvataggio')
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{error_msg}: {self.db.last_error_details}",
                parent=self
            )

    def _clear_verification_form(self):
        """Pulisce il form di verifica"""
        self._current_must_check_id = None
        self._current_label_code_id = None
        self.label_code_var.set('')
        self.label_code_status_label.config(text='')
        self.result_var.set('')
        self.comment_text.delete('1.0', 'end')
        self._on_result_changed()
        self._check_items = []
        for item in self.checklist_tree.get_children():
            self.checklist_tree.delete(item)