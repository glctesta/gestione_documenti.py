# npi/windows/project_documents_window.py
"""
Finestra per visualizzare, filtrare, ordinare e gestire (CRUD) 
tutti i documenti caricati nel progetto NPI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


class ProjectDocumentsWindow(tk.Toplevel):
    """Finestra per visualizzare, filtrare, ordinare e gestire documenti del progetto."""
    
    def __init__(self, master, npi_manager, lang, project_id, project_name):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.project_name = project_name
        self.all_documents = []
        self.show_deleted_var = tk.BooleanVar(value=False)
        self.sort_field = 'date_in'
        self.sort_ascending = False
        
        self.title(f"{self.lang.get('NPI_DOCS_TITLE', 'Documenti Progetto NPI')}: {self.project_name}")
        self.geometry("1200x750")
        self.minsize(900, 600)
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
            text=self.lang.get('NPI_DOCS_TITLE', 'Documenti Progetto NPI'),
            font=('Helvetica', 14, 'bold')
        )
        header.pack(pady=(0, 10))
        
        # ════════════════════════════════════════
        # FILTRI E RICERCA
        # ════════════════════════════════════════
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prima riga: Ricerca + Tipo + Task
        filter_row1 = ttk.Frame(filter_frame)
        filter_row1.pack(fill=tk.X, pady=2)
        
        # Ricerca libera
        ttk.Label(filter_row1, text=self.lang.get('NPI_DOCS_SEARCH', 'Cerca...')).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_row1, textvariable=self.search_var, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_var.trace_add('write', lambda *a: self._apply_filters())
        
        # Filtro Tipo Documento
        ttk.Label(filter_row1, text=self.lang.get('NPI_DOCS_COL_TYPE', 'Tipo:')).pack(side=tk.LEFT, padx=(20, 5))
        self.doc_type_var = tk.StringVar()
        self.doc_type_combo = ttk.Combobox(filter_row1, textvariable=self.doc_type_var, state='readonly', width=25)
        self.doc_type_combo.pack(side=tk.LEFT, padx=5)
        self.doc_type_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Filtro Task
        ttk.Label(filter_row1, text=self.lang.get('NPI_DOCS_COL_TASK', 'Task:')).pack(side=tk.LEFT, padx=(20, 5))
        self.task_var = tk.StringVar()
        self.task_combo = ttk.Combobox(filter_row1, textvariable=self.task_var, state='readonly', width=30)
        self.task_combo.pack(side=tk.LEFT, padx=5)
        self.task_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        
        # Seconda riga: Date + Ordinamento + Mostra eliminati
        filter_row2 = ttk.Frame(filter_frame)
        filter_row2.pack(fill=tk.X, pady=2)
        
        # Filtro Data Da/A
        ttk.Label(filter_row2, text=self.lang.get('from_date', 'Da Data:')).pack(side=tk.LEFT, padx=5)
        self.from_date_var = tk.StringVar()
        ttk.Entry(filter_row2, textvariable=self.from_date_var, width=12).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_row2, text=self.lang.get('to_date', 'A Data:')).pack(side=tk.LEFT, padx=(10, 5))
        self.to_date_var = tk.StringVar()
        ttk.Entry(filter_row2, textvariable=self.to_date_var, width=12).pack(side=tk.LEFT, padx=5)
        
        # Ordinamento
        ttk.Label(filter_row2, text=self.lang.get('NPI_DOCS_SORT_BY', 'Ordina per:')).pack(side=tk.LEFT, padx=(20, 5))
        self.sort_var = tk.StringVar(value='date_in')
        sort_options = [
            (self.lang.get('NPI_DOCS_COL_INSDATE', 'Data Inserimento'), 'date_in'),
            (self.lang.get('NPI_DOCS_COL_TYPE', 'Tipo'), 'doc_type'),
            (self.lang.get('NPI_DOCS_COL_TASK', 'Task'), 'task_name'),
            (self.lang.get('NPI_DOCS_COL_VALUE', 'Valore'), 'value'),
            (self.lang.get('NPI_DOCS_COL_DESC', 'Titolo'), 'doc_title'),
        ]
        self.sort_display_map = {label: key for label, key in sort_options}
        sort_combo = ttk.Combobox(filter_row2, textvariable=self.sort_var, state='readonly', width=18,
                                  values=[label for label, _ in sort_options])
        sort_combo.current(0)
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self._on_sort_changed())
        
        # ASC/DESC Toggle
        self.sort_dir_var = tk.StringVar(value='DESC')
        ttk.Radiobutton(filter_row2, text='▲ ASC', variable=self.sort_dir_var, value='ASC',
                        command=self._on_sort_changed).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(filter_row2, text='▼ DESC', variable=self.sort_dir_var, value='DESC',
                        command=self._on_sort_changed).pack(side=tk.LEFT, padx=2)
        
        # Mostra eliminati
        ttk.Checkbutton(filter_row2, text=self.lang.get('NPI_DOCS_SHOW_DELETED', 'Mostra eliminati'),
                        variable=self.show_deleted_var,
                        command=self._load_documents).pack(side=tk.LEFT, padx=(20, 5))
        
        # Bottoni filtro
        ttk.Button(filter_row2, text=self.lang.get('apply_filters', 'Applica'),
                   command=self._apply_filters).pack(side=tk.RIGHT, padx=5)
        ttk.Button(filter_row2, text=self.lang.get('clear_filters', 'Pulisci'),
                   command=self._clear_filters).pack(side=tk.RIGHT, padx=5)
        
        # ════════════════════════════════════════
        # TREEVIEW DOCUMENTI
        # ════════════════════════════════════════
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('task', 'doc_type', 'doc_title', 'date_in', 'user', 'version', 'value', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('task', text=self.lang.get('NPI_DOCS_COL_TASK', 'Task'))
        self.tree.heading('doc_type', text=self.lang.get('NPI_DOCS_COL_TYPE', 'Tipo Documento'))
        self.tree.heading('doc_title', text=self.lang.get('NPI_DOCS_COL_DESC', 'Titolo Documento'))
        self.tree.heading('date_in', text=self.lang.get('NPI_DOCS_COL_INSDATE', 'Data Inserimento'))
        self.tree.heading('user', text=self.lang.get('col_user', 'Utente'))
        self.tree.heading('version', text=self.lang.get('col_version', 'Versione'))
        self.tree.heading('value', text=self.lang.get('NPI_DOCS_COL_VALUE', 'Valore (€)'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))
        
        self.tree.column('task', width=180)
        self.tree.column('doc_type', width=140)
        self.tree.column('doc_title', width=220)
        self.tree.column('date_in', width=130, anchor=tk.CENTER)
        self.tree.column('user', width=110)
        self.tree.column('version', width=70, anchor=tk.CENTER)
        self.tree.column('value', width=100, anchor=tk.E)
        self.tree.column('status', width=80, anchor=tk.CENTER)
        
        # Tag per documenti eliminati
        self.tree.tag_configure('deleted', foreground='gray')
        self.tree.tag_configure('active', foreground='black')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double click per aprire documento
        self.tree.bind('<Double-1>', self._open_document)
        
        # ════════════════════════════════════════
        # PULSANTI CRUD
        # ════════════════════════════════════════
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 5))
        
        # Pulsanti a sinistra
        left_btns = ttk.Frame(button_frame)
        left_btns.pack(side=tk.LEFT)
        
        ttk.Button(left_btns, text=f"➕ {self.lang.get('NPI_DOCS_BTN_NEW', 'Nuovo')}",
                   command=self._new_document).pack(side=tk.LEFT, padx=3)
        ttk.Button(left_btns, text=f"✏️ {self.lang.get('NPI_DOCS_BTN_EDIT', 'Modifica')}",
                   command=self._edit_document).pack(side=tk.LEFT, padx=3)
        ttk.Button(left_btns, text=f"🗑️ {self.lang.get('NPI_DOCS_BTN_DELETE', 'Elimina')}",
                   command=self._delete_document).pack(side=tk.LEFT, padx=3)
        self.btn_restore = ttk.Button(left_btns, text=f"🔄 {self.lang.get('NPI_DOCS_BTN_RESTORE', 'Ripristina')}",
                                      command=self._restore_document)
        self.btn_restore.pack(side=tk.LEFT, padx=3)
        
        # Pulsanti a destra
        right_btns = ttk.Frame(button_frame)
        right_btns.pack(side=tk.RIGHT)
        
        ttk.Button(right_btns, text=self.lang.get('btn_open_document', 'Apri Documento'),
                   command=self._open_document).pack(side=tk.LEFT, padx=3)
        ttk.Button(right_btns, text=f"🔄 {self.lang.get('NPI_DOCS_BTN_REFRESH', 'Aggiorna')}",
                   command=self._load_documents).pack(side=tk.LEFT, padx=3)
        ttk.Button(right_btns, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.LEFT, padx=3)
        
        # ════════════════════════════════════════
        # INFO + RIEPILOGO
        # ════════════════════════════════════════
        self.info_label = ttk.Label(main_frame, text="", foreground="blue")
        self.info_label.pack(pady=2)
        
        # Summary panel (visibile solo se ci sono documenti con valore)
        self.summary_frame = ttk.LabelFrame(main_frame,
                                            text=self.lang.get('NPI_DOCS_SUMMARY_TOTAL', 'Riepilogo'),
                                            padding=8)
        self.summary_frame.pack(fill=tk.X, pady=(5, 0))
        
        summary_row = ttk.Frame(self.summary_frame)
        summary_row.pack(fill=tk.X)
        
        self.lbl_total_docs = ttk.Label(summary_row,
                                        text=f"{self.lang.get('NPI_DOCS_SUMMARY_TOTAL', 'Totale documenti')}: 0",
                                        font=('Helvetica', 10, 'bold'))
        self.lbl_total_docs.pack(side=tk.LEFT, padx=20)
        
        self.lbl_docs_value = ttk.Label(summary_row,
                                        text=f"{self.lang.get('NPI_DOCS_SUMMARY_WITH_VAL', 'Documenti con valore')}: 0",
                                        font=('Helvetica', 10))
        self.lbl_docs_value.pack(side=tk.LEFT, padx=20)
        
        self.lbl_total_value = ttk.Label(summary_row,
                                         text=f"{self.lang.get('NPI_DOCS_SUMMARY_TOT_VAL', 'Valore totale')}: € 0,00",
                                         font=('Helvetica', 10, 'bold'), foreground='#1E5FA3')
        self.lbl_total_value.pack(side=tk.LEFT, padx=20)
        
        # Nascondi inizialmente il summary
        self.summary_frame.pack_forget()
    
    # ════════════════════════════════════════
    # CARICAMENTO DATI
    # ════════════════════════════════════════
    
    def _load_documents(self):
        """Carica tutti i documenti del progetto."""
        try:
            include_deleted = self.show_deleted_var.get()
            documents = self.npi_manager.get_all_project_documents(
                self.project_id, include_deleted=include_deleted
            )
            
            self.all_documents = documents if documents else []
            
            if not self.all_documents:
                self.info_label.config(
                    text=self.lang.get('no_documents_found', 'Nessun documento trovato per questo progetto.')
                )
            
            # Popola combo filtri
            doc_types = set()
            tasks = set()
            for doc in self.all_documents:
                if doc.get('doc_type'):
                    doc_types.add(doc['doc_type'])
                if doc.get('task_name'):
                    tasks.add(doc['task_name'])
            
            all_types_label = self.lang.get('all_types', 'Tutti i tipi')
            all_tasks_label = self.lang.get('all_tasks', 'Tutti i task')
            
            self.doc_type_combo['values'] = [all_types_label] + sorted(list(doc_types))
            if not self.doc_type_var.get():
                self.doc_type_combo.set(all_types_label)
            
            self.task_combo['values'] = [all_tasks_label] + sorted(list(tasks))
            if not self.task_var.get():
                self.task_combo.set(all_tasks_label)
            
            self._apply_filters()
            self._update_summary()
            
        except Exception as e:
            logger.error(f"Errore caricamento documenti progetto: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile caricare i documenti:\n{e}", parent=self)
    
    # ════════════════════════════════════════
    # FILTRI E ORDINAMENTO
    # ════════════════════════════════════════
    
    def _on_sort_changed(self):
        """Gestisce il cambio di campo/direzione ordinamento."""
        sort_label = self.sort_var.get()
        self.sort_field = self.sort_display_map.get(sort_label, 'date_in')
        self.sort_ascending = (self.sort_dir_var.get() == 'ASC')
        self._apply_filters()
    
    def _apply_filters(self):
        """Applica filtri, ricerca e ordinamento, poi aggiorna la treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.all_documents:
            return
        
        # Valori filtri
        selected_type = self.doc_type_var.get()
        selected_task = self.task_var.get()
        search_text = self.search_var.get().strip().lower()
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
        filtered = []
        for doc in self.all_documents:
            # Filtro tipo
            if selected_type != all_types_label and doc.get('doc_type') != selected_type:
                continue
            # Filtro task
            if selected_task != all_tasks_label and doc.get('task_name') != selected_task:
                continue
            # Filtro ricerca libera
            if search_text:
                searchable = f"{doc.get('doc_title', '')} {doc.get('doc_type', '')} {doc.get('task_name', '')} {doc.get('note', '')}".lower()
                if search_text not in searchable:
                    continue
            # Filtro data
            doc_date = doc.get('date_in')
            if doc_date:
                if isinstance(doc_date, str):
                    try:
                        doc_date = datetime.strptime(doc_date, '%d/%m/%Y').date()
                    except Exception:
                        doc_date = None
                elif hasattr(doc_date, 'date'):
                    doc_date = doc_date.date()
                
                if doc_date:
                    if from_date and doc_date < from_date:
                        continue
                    if to_date and doc_date > to_date:
                        continue
            
            filtered.append(doc)
        
        # Ordina
        def get_sort_key(doc):
            val = doc.get(self.sort_field)
            if val is None:
                return '' if isinstance(doc.get(self.sort_field), str) else 0
            if isinstance(val, str):
                return val.lower()
            return val
        
        try:
            filtered.sort(key=get_sort_key, reverse=not self.sort_ascending)
        except TypeError:
            pass  # In caso di tipi misti
        
        # Popola treeview
        active_label = self.lang.get('NPI_DOCS_STATUS_ACTIVE', 'Attivo')
        deleted_label = self.lang.get('NPI_DOCS_STATUS_DELETED', 'Eliminato')
        
        filtered_count = 0
        for doc in filtered:
            task_name = doc.get('task_name', 'N/A')
            doc_type = doc.get('doc_type', 'N/A')
            doc_title = doc.get('doc_title', 'N/A')
            date_in = doc.get('date_in_formatted', 'N/A')
            user = doc.get('user', 'N/A')
            version = str(doc.get('version', '0'))
            value = f"{doc.get('value', 0):.2f}" if doc.get('value') else ""
            is_deleted = doc.get('is_deleted', False)
            status = deleted_label if is_deleted else active_label
            tag = 'deleted' if is_deleted else 'active'
            
            self.tree.insert('', tk.END, text=str(doc['doc_id']),
                             values=(task_name, doc_type, doc_title, date_in, user, version, value, status),
                             tags=(tag,))
            filtered_count += 1
        
        # Aggiorna label info
        total = len(self.all_documents)
        self.info_label.config(
            text=f"{self.lang.get('showing', 'Visualizzati')}: {filtered_count} / {total} {self.lang.get('documents', 'documenti')}"
        )
    
    def _clear_filters(self):
        """Pulisce tutti i filtri."""
        self.doc_type_combo.set(self.lang.get('all_types', 'Tutti i tipi'))
        self.task_combo.set(self.lang.get('all_tasks', 'Tutti i task'))
        self.from_date_var.set('')
        self.to_date_var.set('')
        self.search_var.set('')
        self._apply_filters()
    
    # ════════════════════════════════════════
    # RIEPILOGO
    # ════════════════════════════════════════
    
    def _update_summary(self):
        """Aggiorna il pannello riepilogativo."""
        try:
            summary = self.npi_manager.get_project_document_summary(self.project_id)
            total = summary.get('total_docs', 0)
            with_val = summary.get('docs_with_value', 0)
            total_val = summary.get('total_value', 0.0)
            
            self.lbl_total_docs.config(
                text=f"{self.lang.get('NPI_DOCS_SUMMARY_TOTAL', 'Totale documenti')}: {total}"
            )
            self.lbl_docs_value.config(
                text=f"{self.lang.get('NPI_DOCS_SUMMARY_WITH_VAL', 'Documenti con valore')}: {with_val}"
            )
            self.lbl_total_value.config(
                text=f"{self.lang.get('NPI_DOCS_SUMMARY_TOT_VAL', 'Valore totale')}: € {total_val:,.2f}"
            )
            
            # Mostra/nascondi pannello
            if with_val > 0:
                self.summary_frame.pack(fill=tk.X, pady=(5, 0))
            else:
                self.summary_frame.pack_forget()
                
        except Exception as e:
            logger.error(f"Errore aggiornamento riepilogo: {e}", exc_info=True)
    
    # ════════════════════════════════════════
    # APERTURA DOCUMENTO
    # ════════════════════════════════════════
    
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
            documento = self.npi_manager.get_npi_document(doc_id)
            
            if not documento or not documento.DocumentBody:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('document_not_found', 'Documento non trovato o vuoto.'),
                    parent=self
                )
                return
            
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
    
    # ════════════════════════════════════════
    # CRUD: NUOVO
    # ════════════════════════════════════════
    
    def _new_document(self):
        """Apre dialog per creare un nuovo documento."""
        DocumentDialog(
            parent=self,
            npi_manager=self.npi_manager,
            lang=self.lang,
            project_id=self.project_id,
            on_save_callback=self._on_crud_complete,
            mode='new'
        )
    
    # ════════════════════════════════════════
    # CRUD: MODIFICA
    # ════════════════════════════════════════
    
    def _edit_document(self):
        """Apre dialog per modificare il documento selezionato."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_document', 'Seleziona un documento da modificare.'),
                parent=self
            )
            return
        
        item = selection[0]
        doc_id = int(self.tree.item(item, 'text'))
        
        # Trova il doc nei dati caricati
        doc_data = next((d for d in self.all_documents if d['doc_id'] == doc_id), None)
        if not doc_data:
            return
        
        # Non permettere modifica di documenti eliminati
        if doc_data.get('is_deleted'):
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('cannot_edit_deleted', 'Non è possibile modificare un documento eliminato. Ripristinalo prima.'),
                parent=self
            )
            return
        
        DocumentDialog(
            parent=self,
            npi_manager=self.npi_manager,
            lang=self.lang,
            project_id=self.project_id,
            on_save_callback=self._on_crud_complete,
            mode='edit',
            doc_data=doc_data
        )
    
    # ════════════════════════════════════════
    # CRUD: ELIMINA (SOFT DELETE)
    # ════════════════════════════════════════
    
    def _delete_document(self):
        """Soft-delete del documento selezionato."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_document', 'Seleziona un documento da eliminare.'),
                parent=self
            )
            return
        
        item = selection[0]
        doc_id = int(self.tree.item(item, 'text'))
        
        # Trova il doc
        doc_data = next((d for d in self.all_documents if d['doc_id'] == doc_id), None)
        if doc_data and doc_data.get('is_deleted'):
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('already_deleted', 'Questo documento è già stato eliminato.'),
                parent=self
            )
            return
        
        if not messagebox.askyesno(
            self.lang.get('confirm_delete_title', 'Conferma'),
            self.lang.get('NPI_DOCS_CONFIRM_DELETE', 'Confermare eliminazione?'),
            parent=self
        ):
            return
        
        try:
            self.npi_manager.soft_delete_npi_document(doc_id)
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('document_deleted', 'Documento eliminato con successo.'),
                parent=self
            )
            self._on_crud_complete()
        except Exception as e:
            logger.error(f"Errore eliminazione documento: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore eliminazione:\n{e}",
                parent=self
            )
    
    # ════════════════════════════════════════
    # CRUD: RIPRISTINO
    # ════════════════════════════════════════
    
    def _restore_document(self):
        """Ripristina un documento soft-deleted."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_document', 'Seleziona un documento da ripristinare.'),
                parent=self
            )
            return
        
        item = selection[0]
        doc_id = int(self.tree.item(item, 'text'))
        
        # Verifica che sia effettivamente eliminato
        doc_data = next((d for d in self.all_documents if d['doc_id'] == doc_id), None)
        if not doc_data or not doc_data.get('is_deleted'):
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('not_deleted', 'Questo documento non è eliminato.'),
                parent=self
            )
            return
        
        try:
            self.npi_manager.restore_npi_document(doc_id)
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('document_restored', 'Documento ripristinato con successo.'),
                parent=self
            )
            self._on_crud_complete()
        except Exception as e:
            logger.error(f"Errore ripristino documento: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore ripristino:\n{e}",
                parent=self
            )
    
    def _on_crud_complete(self):
        """Callback dopo ogni operazione CRUD: ricarica dati e riepilogo."""
        self._load_documents()


# ════════════════════════════════════════════════════════
# DIALOG NUOVO / MODIFICA DOCUMENTO
# ════════════════════════════════════════════════════════

class DocumentDialog(tk.Toplevel):
    """Dialog per creare o modificare un documento NPI."""
    
    def __init__(self, parent, npi_manager, lang, project_id, on_save_callback,
                 mode='new', doc_data=None):
        super().__init__(parent)
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.on_save_callback = on_save_callback
        self.mode = mode
        self.doc_data = doc_data
        self.selected_file_data = None
        
        title = self.lang.get('NPI_DOCS_DIALOG_NEW', 'Nuovo Documento') if mode == 'new' \
            else self.lang.get('NPI_DOCS_DIALOG_EDIT', 'Modifica Documento')
        self.title(title)
        self.geometry("550x450")
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)
        
        self._create_widgets()
        
        if mode == 'edit' and doc_data:
            self._populate_from_data(doc_data)
    
    def _create_widgets(self):
        main = ttk.Frame(self, padding=15)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Tipo documento
        ttk.Label(main, text=self.lang.get('NPI_DOCS_COL_TYPE', 'Tipo Documento:')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(main, textvariable=self.type_var, state='readonly', width=40)
        self.type_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # Carica tipi
        try:
            doc_types = self.npi_manager.get_npi_document_types()
            self.doc_types_map = {dt.NpiDocumentDescription: dt.NpiDocumentTypeId for dt in doc_types}
            self.doc_types_map_rev = {dt.NpiDocumentTypeId: dt.NpiDocumentDescription for dt in doc_types}
            self.type_combo['values'] = list(self.doc_types_map.keys())
        except Exception as e:
            logger.error(f"Errore caricamento tipi documento: {e}")
            self.doc_types_map = {}
            self.doc_types_map_rev = {}
        
        # Titolo / Descrizione
        ttk.Label(main, text=self.lang.get('NPI_DOCS_COL_DESC', 'Titolo / Descrizione:')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.title_var, width=42).grid(
            row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # Valore (€)
        ttk.Label(main, text=self.lang.get('NPI_DOCS_COL_VALUE', 'Valore (€):')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.value_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.value_var, width=20).grid(
            row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Note
        ttk.Label(main, text=self.lang.get('notes', 'Note:')).grid(
            row=3, column=0, sticky=tk.NW, pady=5)
        self.note_text = tk.Text(main, height=4, width=42)
        self.note_text.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # File (solo per nuovo documento)
        if self.mode == 'new':
            ttk.Label(main, text=self.lang.get('select_file', 'File:')).grid(
                row=4, column=0, sticky=tk.W, pady=5)
            file_frame = ttk.Frame(main)
            file_frame.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
            
            ttk.Button(file_frame, text=self.lang.get('browse', 'Sfoglia...'),
                       command=self._select_file).pack(side=tk.LEFT)
            self.file_label = ttk.Label(file_frame,
                                        text=self.lang.get('no_file_selected', 'Nessun file'))
            self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Espandi colonna 1
        main.columnconfigure(1, weight=1)
        
        # Pulsanti
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                   command=self._save, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                   command=self.destroy, width=15).pack(side=tk.LEFT, padx=10)
    
    def _select_file(self):
        """Apre dialogo per selezionare un file da allegare."""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(parent=self)
        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    self.selected_file_data = f.read()
                filename = os.path.basename(filepath)
                self.file_label.config(text=filename)
                # Auto-fill titolo se vuoto
                if not self.title_var.get():
                    self.title_var.set(filename)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile leggere il file:\n{e}", parent=self)
    
    def _populate_from_data(self, data):
        """Pre-popola i campi per la modalità modifica."""
        # Tipo
        type_id = data.get('doc_type_id')
        if type_id and type_id in self.doc_types_map_rev:
            self.type_var.set(self.doc_types_map_rev[type_id])
        
        # Titolo
        self.title_var.set(data.get('doc_title', ''))
        
        # Valore
        val = data.get('value')
        if val is not None and val > 0:
            self.value_var.set(str(val))
        
        # Note
        note = data.get('note', '')
        if note:
            self.note_text.insert('1.0', note)
    
    def _save(self):
        """Salva il documento (nuovo o modificato)."""
        # Validazione
        doc_type_text = self.type_var.get()
        title = self.title_var.get().strip()
        
        if not doc_type_text:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('doc_type_required', 'Seleziona un tipo documento.'),
                parent=self
            )
            return
        
        if not title:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('doc_title_required', 'Inserisci un titolo per il documento.'),
                parent=self
            )
            return
        
        doc_type_id = self.doc_types_map.get(doc_type_text)
        
        # Parse valore
        value = None
        value_str = self.value_var.get().strip()
        if value_str:
            try:
                value = float(value_str.replace(',', '.'))
            except ValueError:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('invalid_value', 'Il valore inserito non è valido.'),
                    parent=self
                )
                return
        
        note = self.note_text.get('1.0', tk.END).strip() or None
        
        try:
            if self.mode == 'new':
                if not self.selected_file_data:
                    messagebox.showwarning(
                        self.lang.get('warning', 'Attenzione'),
                        self.lang.get('no_file_selected', 'Seleziona un file da caricare.'),
                        parent=self
                    )
                    return
                
                # Per il nuovo documento, usa il primo task del progetto come default
                # (il task specifico verrà gestito in una versione futura)
                self.npi_manager.add_npi_document(
                    task_prodotto_id=self._get_first_task_id(),
                    doc_type_id=doc_type_id,
                    title=title,
                    body=self.selected_file_data,
                    user=os.getenv('USERNAME', 'system'),
                    note=note,
                    doc_value=value
                )
            else:
                # Modifica
                doc_id = self.doc_data['doc_id']
                update_data = {
                    'DocumentTitle': title,
                    'NpiDocumentTypeId': doc_type_id,
                    'ValueInEur': value,
                    'Note': note
                }
                self.npi_manager.update_npi_document(doc_id, update_data)
            
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('document_saved', 'Documento salvato con successo.'),
                parent=self
            )
            self.destroy()
            if self.on_save_callback:
                self.on_save_callback()
                
        except Exception as e:
            logger.error(f"Errore salvataggio documento: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore salvataggio:\n{e}",
                parent=self
            )
    
    def _get_first_task_id(self):
        """Recupera il primo TaskProdottoID del progetto per associare il documento."""
        try:
            docs = self.npi_manager.get_all_project_documents(self.project_id)
            if docs:
                # Usa lo stesso task del primo documento esistente
                return docs[0].get('task_prodotto_id')
            
            # Altrimenti cerca il primo task del progetto via la wave
            from sqlalchemy import select
            from ..data_models import TaskProdotto, WaveNPI
            session = self.npi_manager._get_session()
            try:
                task_id = session.scalar(
                    select(TaskProdotto.TaskProdottoID)
                    .join(WaveNPI, TaskProdotto.WaveID == WaveNPI.WaveID)
                    .where(WaveNPI.ProgettoID == self.project_id)
                    .limit(1)
                )
                return task_id
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Errore recupero task ID: {e}")
            return None
