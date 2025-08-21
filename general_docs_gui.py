import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import tempfile
import sys
import subprocess


class AddEditDocDialog(tk.Toplevel):
    """Dialogo per aggiungere o modificare un documento generale."""

    def __init__(self, parent, db, lang, user_name, existing_doc=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.existing_doc = existing_doc
        self.transient(parent)
        self.grab_set()

        self.title("Aggiungi Nuovo Documento" if not existing_doc else "Modifica Documento")

        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.version_var = tk.StringVar()
        self.file_path_var = tk.StringVar()
        self.binary_data = None
        self.file_name = ""
        self.result = None

        if existing_doc:
            self.title_var.set(existing_doc.Titolo)
            self.desc_var.set(existing_doc.Descrizione or "")
            self.version_var.set(existing_doc.Versione or "")
            self.file_path_var.set(existing_doc.NomeFile)
            self.binary_data = existing_doc.DatiFile
            self.file_name = existing_doc.NomeFile

        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Titolo (*):").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Descrizione:").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.desc_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Versione:").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.version_var).grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="File (*):").grid(row=3, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.file_path_var, state="readonly").grid(row=3, column=1, sticky="ew")
        ttk.Button(frame, text="Sfoglia...", command=self._browse).grid(row=3, column=2, padx=5)

        ttk.Button(frame, text="Salva", command=self._save).grid(row=4, column=1, columnspan=2, sticky="e", pady=15)

    def _browse(self):
        path = filedialog.askopenfilename(parent=self)
        if path:
            self.file_name = os.path.basename(path)
            self.file_path_var.set(self.file_name)
            with open(path, 'rb') as f:
                self.binary_data = f.read()

    def _save(self):
        if not all([self.title_var.get(), self.file_name, self.binary_data]):
            messagebox.showerror("Dati Mancanti", "Titolo e File sono obbligatori.", parent=self)
            return

        self.result = {
            "title": self.title_var.get(), "desc": self.desc_var.get(),
            "version": self.version_var.get(), "file_name": self.file_name,
            "data": self.binary_data, "user": self.user_name
        }
        self.destroy()


class GeneralDocsViewerWindow(tk.Toplevel):
    """Finestra per visualizzare e gestire i documenti di una specifica categoria."""

    def __init__(self, parent, db, lang, category_id, category_name, user_name, view_only=False):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.category_id = category_id
        self.user_name = user_name
        self.view_only = view_only  # Salva la modalità (sola lettura o completa)

        title_prefix = lang.get('view_mode_title', "Visualizzazione") if view_only else lang.get('manage_mode_title',
                                                                                                 "Gestione")
        self.title(f"{title_prefix} Documenti: {category_name}")
        self.geometry("900x500")

        self._create_widgets()
        self._load_documents()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # La lista è sempre visibile
        cols = ('title', 'version', 'user', 'date')
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading('title', text="Titolo")
        self.tree.heading('version', text="Versione")
        self.tree.heading('user', text="Caricato Da")
        self.tree.heading('date', text="Data Caricamento")
        self.tree.column('version', width=100, anchor='center')
        self.tree.column('user', width=150)
        self.tree.column('date', width=150)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self._open_document)

        # --- LOGICA CONDIZIONALE PER I PULSANTI ---
        # Mostra i pulsanti di gestione solo se NON siamo in modalità "sola lettura"
        if not self.view_only:
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=1, column=0, sticky="e", pady=10)
            ttk.Button(btn_frame, text="Aggiungi Nuovo", command=self._add_doc).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Modifica Selezionato", command=self._edit_doc).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Cancella Selezionato", command=self._delete_doc).pack(side="left", padx=5)

    def _load_documents(self):
        self.tree.delete(*self.tree.get_children())
        docs = self.db.fetch_general_documents(self.category_id)
        for doc in docs:
            self.tree.insert("", "end", iid=doc.DocumentoId, values=(
                doc.Titolo, doc.Versione, doc.CaricatoDa,
                doc.DataCaricamento.strftime('%Y-%m-%d %H:%M')
            ))

    def _open_document(self, event=None):
        selected_id = self.tree.focus()
        if not selected_id: return
        doc = self.db.fetch_single_general_document(selected_id)
        if not doc or not doc.DatiFile:
            messagebox.showwarning("Attenzione", "Documento non trovato o corrotto.")
            return

        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, prefix=doc.Titolo[:20] + "_",
                                                    suffix=os.path.splitext(doc.NomeFile)[1])
            temp_file.write(doc.DatiFile)
            temp_file.close()
            if sys.platform == "win32":
                os.startfile(temp_file.name)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, temp_file.name])
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il file: {e}")

    def _add_doc(self):
        dialog = AddEditDocDialog(self, self.db, self.lang, self.user_name)
        self.wait_window(dialog)
        if dialog.result:
            success = self.db.add_general_document(self.category_id, **dialog.result)
            if success:
                self._load_documents()
            else:
                messagebox.showerror("Errore", f"Salvataggio fallito:\n{self.db.last_error_details}")

    def _edit_doc(self):
        selected_id = self.tree.focus()
        if not selected_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare un documento da modificare.")
            return

        doc_data = self.db.fetch_single_general_document(selected_id)
        dialog = AddEditDocDialog(self, self.db, self.lang, self.user_name, existing_doc=doc_data)
        self.wait_window(dialog)

        if dialog.result:
            success = self.db.update_general_document(selected_id, **dialog.result)
            if success:
                self._load_documents()
            else:
                messagebox.showerror("Errore", f"Aggiornamento fallito:\n{self.db.last_error_details}")

    def _delete_doc(self):
        selected_id = self.tree.focus()
        if not selected_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare un documento da cancellare.")
            return

        if messagebox.askyesno("Conferma Cancellazione",
                               "Sei sicuro di voler cancellare questo documento? L'operazione è irreversibile."):
            success = self.db.delete_general_document(selected_id)
            if success:
                self._load_documents()
            else:
                messagebox.showerror("Errore", f"Cancellazione fallita:\n{self.db.last_error_details}")


def open_general_docs_viewer(parent, db, lang, category_id, category_name, user_name, view_only=False):
    GeneralDocsViewerWindow(parent, db, lang, category_id, category_name, user_name, view_only)