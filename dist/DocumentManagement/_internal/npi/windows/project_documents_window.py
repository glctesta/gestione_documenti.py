# npi/windows/project_documents_window.py
"""
Finestra per visualizzare e filtrare tutti i documenti caricati nel progetto NPI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


class ProjectDocumentsWindow(tk.Toplevel):
    """Finestra per visualizzare, filtrare e aprire documenti del progetto."""
    
    def __init__(self, master, npi_manager, lang, project_id, project_name):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.project_name = project_name
        
        self.title(f"{self.lang.get('project_documents_title', 'Documenti Progetto')}: {self.project_name}")
        self.geometry("1200x700")
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._load_documents()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(
            main_frame,
            text=self.lang.get('all_project_documents', 'Tutti i Documenti del Progetto'),
            font=('Helvetica', 14, 'bold')
        )
        header.pack(pady=(0, 10))
        
        # Filtri
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prima riga filtri
        filter_row1 = ttk.Frame(filter_frame)
        filter_row1.pack(fill=tk.X, pady=2)
        
        # Filtro Tipo Documento
        ttk.Label(filter_row1, text=self.lang.get('document_type', 'Tipo Documento:')).pack(side=tk.LEFT, padx=5)
        self.doc_type_var = tk.StringVar()
        self.doc_type_combo = ttk.Combobox(filter_row1, textvariable=self.doc_type_var, state='readonly', width=30)
        self.doc_type_combo.pack(side=tk.LEFT, padx=5)
        self.doc_type_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Filtro Task
        ttk.Label(filter_row1, text=self.lang.get('task', 'Task:')).pack(side=tk.LEFT, padx=(20, 5))
        self.task_var = tk.StringVar()
        self.task_combo = ttk.Combobox(filter_row1, textvariable=self.task_var, state='readonly', width=40)
        self.task_combo.pack(side=tk.LEFT, padx=5)
        self.task_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Seconda riga filtri
        filter_row2 = ttk.Frame(filter_frame)
        filter_row2.pack(fill=tk.X, pady=2)
        
        # Filtro Data Da
        ttk.Label(filter_row2, text=self.lang.get('from_date', 'Da Data:')).pack(side=tk.LEFT, padx=5)
        self.from_date_var = tk.StringVar()
        self.from_date_entry = ttk.Entry(filter_row2, textvariable=self.from_date_var, width=12)
        self.from_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Filtro Data A
        ttk.Label(filter_row2, text=self.lang.get('to_date', 'A Data:')).pack(side=tk.LEFT, padx=(20, 5))
        self.to_date_var = tk.StringVar()
        self.to_date_entry = ttk.Entry(filter_row2, textvariable=self.to_date_var, width=12)
        self.to_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Bottoni filtro
        ttk.Button(filter_row2, text=self.lang.get('apply_filters', 'Applica Filtri'), 
                  command=self._apply_filters).pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(filter_row2, text=self.lang.get('clear_filters', 'Pulisci Filtri'), 
                  command=self._clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Treeview documenti
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('task', 'doc_type', 'doc_title', 'date_in', 'user', 'version', 'value')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('task', text=self.lang.get('col_task', 'Task'))
        self.tree.heading('doc_type', text=self.lang.get('col_doc_type', 'Tipo Documento'))
        self.tree.heading('doc_title', text=self.lang.get('col_doc_title', 'Titolo Documento'))
        self.tree.heading('date_in', text=self.lang.get('col_date_uploaded', 'Data Caricamento'))
        self.tree.heading('user', text=self.lang.get('col_user', 'Utente'))
        self.tree.heading('version', text=self.lang.get('col_version', 'Versione'))
        self.tree.heading('value', text=self.lang.get('col_value', 'Valore (€)'))
        
        self.tree.column('task', width=200)
        self.tree.column('doc_type', width=150)
        self.tree.column('doc_title', width=250)
        self.tree.column('date_in', width=120, anchor=tk.CENTER)
        self.tree.column('user', width=120)
        self.tree.column('version', width=80, anchor=tk.CENTER)
        self.tree.column('value', width=100, anchor=tk.E)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double click per aprire documento
        self.tree.bind('<Double-1>', self._open_document)
        
        # Info label
        self.info_label = ttk.Label(main_frame, text="", foreground="blue")
        self.info_label.pack(pady=5)
        
        # Bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text=self.lang.get('btn_open_document', 'Apri Documento'), 
                  command=self._open_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_refresh', 'Aggiorna'), 
                  command=self._load_documents).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('btn_close', 'Chiudi'), 
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_documents(self):
        """Carica tutti i documenti del progetto."""
        try:
            # Ottieni tutti i documenti del progetto
            documents = self.npi_manager.get_all_project_documents(self.project_id)
            
            if not documents:
                self.info_label.config(text=self.lang.get('no_documents_found', 'Nessun documento trovato per questo progetto.'))
                return
            
            # Salva tutti i documenti per filtraggio
            self.all_documents = documents
            
            # Popola combo tipi documento
            doc_types = set()
            tasks = set()
            
            for doc in documents:
                if doc.get('doc_type'):
                    doc_types.add(doc['doc_type'])
                if doc.get('task_name'):
                    tasks.add(doc['task_name'])
            
            all_types_label = self.lang.get('all_types', 'Tutti i tipi')
            all_tasks_label = self.lang.get('all_tasks', 'Tutti i task')
            
            self.doc_type_combo['values'] = [all_types_label] + sorted(list(doc_types))
            self.doc_type_combo.set(all_types_label)
            
            self.task_combo['values'] = [all_tasks_label] + sorted(list(tasks))
            self.task_combo.set(all_tasks_label)
            
            # Mostra tutti i documenti
            self._apply_filters()
            
        except Exception as e:
            logger.error(f"Errore caricamento documenti progetto: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile caricare i documenti:\n{e}", parent=self)
    
    def _apply_filters(self):
        """Applica i filtri e aggiorna la treeview."""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self, 'all_documents'):
            return
        
        # Ottieni valori filtri
        selected_type = self.doc_type_var.get()
        selected_task = self.task_var.get()
        from_date_str = self.from_date_var.get().strip()
        to_date_str = self.to_date_var.get().strip()
        
        all_types_label = self.lang.get('all_types', 'Tutti i tipi')
        all_tasks_label = self.lang.get('all_tasks', 'Tutti i task')
        
        # Parse date
        from_date = None
        to_date = None
        
        try:
            if from_date_str:
                from_date = datetime.strptime(from_date_str, '%d/%m/%Y').date()
        except ValueError:
            pass
        
        try:
            if to_date_str:
                to_date = datetime.strptime(to_date_str, '%d/%m/%Y').date()
        except ValueError:
            pass
        
        # Filtra documenti
        filtered_count = 0
        for doc in self.all_documents:
            # Filtro tipo documento
            if selected_type != all_types_label and doc.get('doc_type') != selected_type:
                continue
            
            # Filtro task
            if selected_task != all_tasks_label and doc.get('task_name') != selected_task:
                continue
            
            # Filtro data
            doc_date = doc.get('date_in')
            if doc_date:
                if isinstance(doc_date, str):
                    try:
                        doc_date = datetime.strptime(doc_date, '%d/%m/%Y').date()
                    except:
                        pass
                elif hasattr(doc_date, 'date'):
                    doc_date = doc_date.date()
                
                if from_date and doc_date < from_date:
                    continue
                if to_date and doc_date > to_date:
                    continue
            
            # Aggiungi a treeview
            task_name = doc.get('task_name', 'N/A')
            doc_type = doc.get('doc_type', 'N/A')
            doc_title = doc.get('doc_title', 'N/A')
            date_in = doc.get('date_in_formatted', 'N/A')
            user = doc.get('user', 'N/A')
            version = str(doc.get('version', '0'))
            value = f"{doc.get('value', 0):.2f}" if doc.get('value') else ""
            
            self.tree.insert('', tk.END, text=str(doc['doc_id']), 
                           values=(task_name, doc_type, doc_title, date_in, user, version, value))
            filtered_count += 1
        
        # Aggiorna label info
        total = len(self.all_documents)
        self.info_label.config(
            text=f"{self.lang.get('showing', 'Visualizzati')}: {filtered_count} / {total} {self.lang.get('documents', 'documenti')}"
        )
    
    def _clear_filters(self):
        """Pulisce tutti i filtri."""
        all_types_label = self.lang.get('all_types', 'Tutti i tipi')
        all_tasks_label = self.lang.get('all_tasks', 'Tutti i task')
        
        self.doc_type_combo.set(all_types_label)
        self.task_combo.set(all_tasks_label)
        self.from_date_var.set('')
        self.to_date_var.set('')
        
        self._apply_filters()
    
    def _open_document(self, event=None):
        """Apre il documento selezionato."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_document', 'Seleziona un documento da aprire.'),
                parent=self
            )
            return
        
        item = selection[0]
        doc_id = int(self.tree.item(item, 'text'))
        
        try:
            # Recupera il documento completo
            documento = self.npi_manager.get_npi_document(doc_id)
            
            if not documento or not documento.DocumentBody:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('document_not_found', 'Documento non trovato o vuoto.'),
                    parent=self
                )
                return
            
            # Salva in file temporaneo e apri
            suffix = os.path.splitext(documento.DocumentTitle)[1] or '.bin'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(documento.DocumentBody)
                tmp_path = tmp.name
            
            os.startfile(tmp_path)
            logger.info(f"Documento aperto: {documento.DocumentTitle}")
            
        except Exception as e:
            logger.error(f"Errore apertura documento: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('cannot_open_document', 'Impossibile aprire il documento')}:\n{e}",
                parent=self
            )
