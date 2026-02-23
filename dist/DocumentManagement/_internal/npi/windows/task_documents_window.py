import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskDocumentsWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, task_prodotto_id, master_app, task_name,
                 final_clients_map_rev: dict):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.task_prodotto_id = task_prodotto_id
        self.master_app = master_app
        self.task_name = task_name
        self.documents = []
        # Questa mappa è ricevuta da ProjectWindow, deve essere {id: nome}
        self.final_clients_map_rev = final_clients_map_rev

        self.title(f"{self.lang.get('task_documents_list', 'Documenti Task')}: {self.task_name}")
        self.geometry("1000x600")
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self._load_documents()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        self.open_button = ttk.Button(action_frame, text=self.lang.get('btn_open_doc', 'Apri'),
                                      command=self._open_document, state=tk.DISABLED)
        self.open_button.pack(side=tk.LEFT, padx=5)
        self.auth_button = ttk.Button(action_frame, text=self.lang.get('btn_authorize_doc', 'Autorizza...'),
                                      command=self._authorize_document, state=tk.DISABLED)
        self.auth_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self.lang.get('btn_refresh', 'Aggiorna'), command=self._load_documents).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self.lang.get('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

        cols = ('title', 'type', 'final_client', 'value', 'due_date', 'user', 'date_in', 'version', 'authorized',
                'note')
        self.tree = ttk.Treeview(main_frame, columns=cols, show='headings', selectmode='browse')

        self.tree.heading('title', text=self.lang.get('col_doc_title', 'Titolo'))
        self.tree.heading('type', text=self.lang.get('col_doc_type', 'Tipo'))
        self.tree.heading('final_client', text=self.lang.get('col_final_client', 'Cliente Finale'))
        self.tree.heading('value', text=self.lang.get('col_doc_value', 'Valore'))
        self.tree.heading('due_date', text=self.lang.get('col_doc_due_date', 'Scadenza'))
        self.tree.heading('user', text=self.lang.get('col_doc_user', 'Utente'))
        self.tree.heading('date_in', text=self.lang.get('col_doc_date_in', 'Data Inserimento'))
        self.tree.heading('version', text=self.lang.get('col_doc_version', 'Vers.'))
        self.tree.heading('authorized', text=self.lang.get('col_authorized', 'Autorizzato Da'))
        self.tree.heading('note', text=self.lang.get('col_note', 'Note'))

        self.tree.column('version', width=40, anchor=tk.CENTER)
        self.tree.column('value', width=80, anchor=tk.E)
        self.tree.column('due_date', width=100, anchor=tk.CENTER)
        self.tree.column('note', width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-1>', self._open_document)

        self.tree.tag_configure('inactive', font=('Helvetica', 9, 'italic'), foreground='gray')
        self.tree.tag_configure('overdue', foreground='red')

    def _load_documents(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            self.documents = self.npi_manager.get_documents_for_task(self.task_prodotto_id)
            for doc in self.documents:
                tags = []
                if doc.DateOut:
                    tags.append('inactive')

                # --- CORREZIONE: USARE I NOMI DEGLI ATTRIBUTI DEL MODELLO DATI REALE ---
                if hasattr(doc, 'DueDate') and doc.DueDate and doc.DueDate < datetime.now():
                    tags.append('overdue')

                # Usa la mappa inversa per trovare il nome del cliente a partire dal suo ID (doc.IDSite)
                client_name = self.final_clients_map_rev.get(doc.IDSite, "")

                doc_type_desc = doc.document_type.NpiDocumentDescription if doc.document_type else "N/A"
                date_in_str = doc.DateIn.strftime('%Y-%m-%d %H:%M') if doc.DateIn else ''
                due_date_str = doc.DueDate.strftime('%Y-%m-%d') if hasattr(doc, 'DueDate') and doc.DueDate else ''
                value_str = f"{doc.ValueInEur:.2f} €" if hasattr(doc,
                                                                 'ValueInEur') and doc.ValueInEur is not None else ''

                self.tree.insert('', tk.END, text=str(doc.NpiDocumentId), values=(
                    doc.DocumentTitle,
                    doc_type_desc,
                    client_name,
                    value_str,
                    due_date_str,
                    doc.User or '',
                    date_in_str,
                    doc.VersionNumber,
                    doc.AutorizedBy or 'NON AUTORIZZATO',
                    doc.Note or ''
                ), tags=tuple(tags))  # Converti la lista di tag in una tupla
        except Exception as e:
            logger.error(f"Errore caricamento documenti: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title'), f"Impossibile caricare i documenti:\n{e}", parent=self)

    def _on_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            self.open_button.config(state=tk.DISABLED);
            self.auth_button.config(state=tk.DISABLED)
            return
        doc_id = int(self.tree.item(selection[0], 'text'))
        selected_doc = next((d for d in self.documents if d.NpiDocumentId == doc_id), None)
        if not selected_doc: return
        self.open_button.config(state=tk.NORMAL)
        if not selected_doc.AutorizedBy and not selected_doc.DateOut:
            self.auth_button.config(state=tk.NORMAL)
        else:
            self.auth_button.config(state=tk.DISABLED)

    def _open_document(self, event=None):
        selection = self.tree.selection()
        if not selection: return
        doc_id = int(self.tree.item(selection[0], 'text'))
        try:
            body = self.npi_manager.get_document_body(doc_id)
            if not body:
                messagebox.showwarning("Attenzione", "Documento non trovato o corpo vuoto.", parent=self);
                return
            title = self.tree.item(selection[0], 'values')[0]
            suffix = os.path.splitext(title)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix or '.tmp') as tmp_file:
                tmp_file.write(body);
                tmp_path = tmp_file.name
            logger.info(f"Apertura file temporaneo: {tmp_path}")
            os.startfile(tmp_path)
        except Exception as e:
            logger.error(f"Errore apertura documento {doc_id}: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile aprire il documento:\n{e}", parent=self)

    def _authorize_document(self):
        selection = self.tree.selection()
        if not selection: return
        doc_id = int(self.tree.item(selection[0], 'text'))
        self.master_app._execute_authorized_action('autorizzatore_npi', lambda: self._perform_auth_callback(doc_id))

    def _perform_auth_callback(self, doc_id):
        try:
            authorizer_name = self.master_app.last_authenticated_user_name
            if not authorizer_name: raise ValueError("Nome utente autorizzatore non disponibile.")
            self.npi_manager.authorize_document(doc_id, authorizer_name)
            messagebox.showinfo("Successo", "Documento autorizzato con successo.", parent=self)
            self._load_documents()
        except Exception as e:
            logger.error(f"Callback autorizzazione fallito: {e}", exc_info=True)
            messagebox.showerror("Errore Autorizzazione", f"Impossibile completare l'autorizzazione:\n{e}", parent=self)