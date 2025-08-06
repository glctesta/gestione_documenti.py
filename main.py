import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pyodbc
import os
import subprocess  # Importato per lanciare processi esterni come Adobe Reader

# Import per gestire le immagini PNG
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.1.02"
APP_DEVELOPER = "Gianluca Testa"

# --- CONFIGURAZIONE DATABASE ---
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = 'emsreset'
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_UID};PWD={DB_PWD};'


class Database:
    """Classe completa per gestire tutte le operazioni del database."""

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str, autocommit=False)
            self.cursor = self.conn.cursor()
            return True
        except pyodbc.Error as ex:
            messagebox.showerror("Errore Database", f"Impossibile connettersi al database.\n\nDettagli: {ex}")
            return False

    def disconnect(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()

    def fetch_products(self):
        query = "SELECT DISTINCT p.IDProduct, p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']' AS ProductCode FROM Traceability_RS.dbo.Products AS P INNER JOIN [Traceability_RS].[dbo].[ProductParentPhases] AS PP ON pp.IDProduct = p.IDProduct INNER JOIN Traceability_RS.dbo.ParentPhases AS PF ON pf.IDParentPhase = pp.IDParentPhase ORDER BY p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']';"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Errore Query", f"Errore nel recupero dei prodotti: {e}")
            return []

    def fetch_parent_phases(self, id_product):
        query = "SELECT distinct pf.IDParentPhase, pf.ParentPhaseName + IIF(pp.IDProduct IS NULL, '*', '') AS Phase FROM Traceability_RS.dbo.ParentPhases AS pf LEFT JOIN Traceability_RS.dbo.ProductParentPhases AS pp ON pf.IDParentPhase = pp.IDParentPhase AND pp.IDProduct = ? ORDER BY Phase;"
        try:
            self.cursor.execute(query, id_product)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Errore Query", f"Errore nel recupero delle fasi: {e}")
            return []

    def fetch_existing_documents(self, product_id, parent_phase_id):
        query = "SELECT documentName, DocumentRevisionNumber, DocumentPath, CONVERT(bit, Validated) as IsValid FROM Traceability_RS.dbo.ProductDocuments WHERE Productid = ? AND ParentPhaseId = ? AND DateOutOfValidation IS NULL;"
        try:
            self.cursor.execute(query, product_id, parent_phase_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Errore Query", f"Errore nel recupero documenti esistenti: {e}")
            return []

    def authenticate_user(self, user_id, password):
        query = "SELECT u.NomeUser, ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') as EmployeeName, u.pass FROM resetservices.dbo.tbuserkey as U INNER JOIN employee.dbo.employees as e ON e.EmployeeId = u.idanga INNER JOIN employee.dbo.EmployeeHireHistory as h ON e.EmployeeId = h.EmployeeId WHERE h.EndWorkDate IS NULL AND h.employeerid = 2 AND u.Nomeuser = ? AND Pass = ?;"
        try:
            self.cursor.execute(query, user_id, password)
            row = self.cursor.fetchone()
            return row.EmployeeName if row else None
        except pyodbc.Error as e:
            messagebox.showerror("Errore Query Autenticazione", f"Errore durante la verifica delle credenziali: {e}")
            return None

    def save_document(self, product_id, parent_phase_id, doc_name, doc_path, revision, validated_int, user_name):
        sp_call = "{CALL dbo.InsertDoc(?, ?, ?, ?, ?, ?, ?, ?)}"
        update_query = "UPDATE [dbo].[ProductDocuments] SET [Validated] = '0', [DateOutOfValidation] = GETDATE() WHERE Productid = ? AND ParentPhaseId = ? AND DateOutOfValidation IS NULL AND Validated = '1';"
        try:
            if validated_int == 1:
                self.cursor.execute(update_query, product_id, parent_phase_id)

            self.cursor.execute(sp_call, product_id, parent_phase_id, doc_name, revision, doc_path, bool(validated_int),
                                user_name, datetime.now())
            self.conn.commit()
            messagebox.showinfo("Successo", "Documento salvato correttamente.")
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            messagebox.showerror("Errore di Salvataggio",
                                 f"Impossibile salvare il documento tramite Stored Procedure: {e}")
            print(f"ERRORE PYODBC: {e}")
            return False


class LoginWindow(tk.Toplevel):
    """Finestra di autenticazione per l'utente."""

    def __init__(self, master, db_handler):
        super().__init__(master)
        self.title("Autenticazione Utente")
        self.geometry("350x200")
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.db = db_handler
        self.authenticated_user_name = None

        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="User ID:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.user_id_entry = ttk.Entry(frame, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(button_frame, text="Login", command=self._attempt_login).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Annulla", command=self._on_cancel).pack(side="left", padx=10)
        self.user_id_entry.focus_set()

    def _attempt_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if not user_id or not password:
            messagebox.showerror("Errore", "Per favore, inserisci User ID e Password.", parent=self)
            return

        employee_name = self.db.authenticate_user(user_id, password)
        if employee_name:
            self.authenticated_user_name = employee_name
            self.destroy()
        else:
            messagebox.showerror("Autenticazione Fallita", "User ID o Password non corretti.", parent=self)
            self.password_entry.delete(0, tk.END)

    def _on_cancel(self):
        self.authenticated_user_name = None
        self.destroy()


class InsertDocumentForm(tk.Toplevel):
    """Finestra di inserimento documenti."""

    def __init__(self, master, db_handler, user_name):
        super().__init__(master)
        self.title("Inserisci Nuovo Documento")
        self.geometry("650x650")
        self.db = db_handler
        self.user_name = user_name

        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()
        self.file_name_var = tk.StringVar()
        self.revision_var = tk.StringVar()
        self.validated_var = tk.BooleanVar()

        self._create_widgets()
        self._load_products()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="1. Digita per cercare e seleziona un Prodotto:", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var)
        self.product_combo.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))

        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        ttk.Label(frame, text="2. Seleziona Fase:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=2,
                                                                                         sticky=tk.W, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled")
        self.parent_phase_combo.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        details_frame = ttk.LabelFrame(frame, text="3. Dettagli Nuovo Documento", padding="10")
        details_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        details_frame.columnconfigure(1, weight=1)

        ttk.Label(details_frame, text="File Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_entry = ttk.Entry(details_frame, textvariable=self.file_name_var, state="disabled")
        self.file_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.browse_button = ttk.Button(details_frame, text="Sfoglia...", command=self._browse_file, state="disabled")
        self.browse_button.grid(row=0, column=2, padx=(0, 5), pady=5)

        ttk.Label(details_frame, text="Revisione:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.revision_entry = ttk.Entry(details_frame, textvariable=self.revision_var, state="disabled")
        self.revision_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)

        self.validated_check = ttk.Checkbutton(details_frame, text="Validato", variable=self.validated_var,
                                               state="disabled")
        self.validated_check.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

        docs_frame = ttk.LabelFrame(frame, text="Documenti Attivi per questa Fase", padding="10")
        docs_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.docs_listbox = tk.Listbox(docs_frame, height=6, selectbackground="#a6a6a6")
        self.docs_listbox.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(frame, text="Salva", command=self._save_document, state="disabled")
        self.save_button.grid(row=6, column=1, sticky=tk.E, pady=10)

    def _load_products(self):
        products = self.db.fetch_products()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            messagebox.showwarning("Dati Mancanti", "Nessun prodotto trovato nel database.")

    def _on_product_keyrelease(self, event):
        typed_text = self.product_var.get()
        if not typed_text:
            self.product_combo['values'] = self.all_product_names
        else:
            filtered_list = [name for name in self.all_product_names if typed_text.lower() in name.lower()]
            self.product_combo['values'] = filtered_list

    def _on_product_select(self, event=None):
        self._reset_phase_section()
        self._reset_details_section()
        product_id = self.products_data.get(self.product_var.get())

        if product_id:
            parent_phases = self.db.fetch_parent_phases(product_id)
            if parent_phases:
                self.parent_phases_data = {p.Phase: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo['values'] = list(self.parent_phases_data.keys())
                self.parent_phase_combo.config(state="readonly")
            else:
                messagebox.showerror("Dati non trovati", "Nessuna fase trovata per il prodotto selezionato.")
                self.product_combo.focus()

    def _on_phase_select(self, event=None):
        self._reset_details_section()
        self.file_entry.config(state="readonly")
        self.browse_button.config(state="normal")
        self.revision_entry.config(state="normal")
        self.validated_check.config(state="normal")
        self.save_button.config(state="normal")
        self._refresh_document_list()

    def _browse_file(self, event=None):
        file_path = filedialog.askopenfilename(title="Seleziona un documento PDF",
                                               filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            self.file_name_var.set(file_path)

    def _save_document(self):
        if not all([self.product_var.get(), self.parent_phase_var.get(), self.file_name_var.get(),
                    self.revision_var.get()]):
            messagebox.showerror("Errore di input",
                                 "Tutti i campi (Prodotto, Fase, File, Revisione) devono essere compilati.")
            return

        selected_product_display = self.product_var.get()
        if selected_product_display not in self.products_data:
            messagebox.showerror("Errore di input",
                                 "Prodotto non valido. Per favore, seleziona un prodotto dalla lista.")
            return

        revision = self.revision_var.get()
        if len(revision) > 10:
            messagebox.showerror(
                "Errore di Input",
                f"Il numero di revisione ('{revision}') ha {len(revision)} caratteri.\n\n"
                f"La lunghezza massima consentita è 10 caratteri."
            )
            return

        is_validated_bool = self.validated_var.get()
        validated_as_int = 1 if is_validated_bool else 0

        product_id = self.products_data.get(selected_product_display)
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())
        doc_path = self.file_name_var.get()
        doc_name = os.path.basename(doc_path)

        if self.db.save_document(product_id, parent_phase_id, doc_name, doc_path, revision, validated_as_int,
                                 self.user_name):
            self._reset_input_fields()
            self._refresh_document_list()

    def _refresh_document_list(self):
        self.docs_listbox.delete(0, tk.END)
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        existing_docs = self.db.fetch_existing_documents(product_id, parent_phase_id)
        for i, doc in enumerate(existing_docs):
            display_text = f"File: {doc.documentName} | Rev: {doc.DocumentRevisionNumber} | Validato: {'Sì' if doc.IsValid else 'No'}"
            self.docs_listbox.insert(tk.END, display_text)
            if doc.IsValid:
                self.docs_listbox.itemconfig(i, {'bg': '#c8e6c9'})

    def _reset_phase_section(self):
        self.parent_phase_var.set("")
        self.parent_phase_combo.config(state="disabled")
        self.parent_phase_combo['values'] = []

    def _reset_details_section(self):
        self._reset_input_fields()
        self.file_entry.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.revision_entry.config(state="disabled")
        self.validated_check.config(state="disabled")
        self.save_button.config(state="disabled")
        self.docs_listbox.delete(0, tk.END)

    def _reset_input_fields(self):
        self.file_name_var.set("")
        self.revision_var.set("")
        self.validated_var.set(False)
        self.file_entry.config(state="readonly")


class ViewDocumentForm(tk.Toplevel):
    """Finestra per visualizzare un documento."""

    def __init__(self, master, db_handler):
        super().__init__(master)
        self.title("Visualizza Documento")
        self.geometry("600x250")
        self.transient(master)
        self.grab_set()

        self.db = db_handler
        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()

        self._create_widgets()
        self._load_products()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="1. Digita per cercare e seleziona un Prodotto:", font=("Helvetica", 10, "bold")).pack(
            fill=tk.X, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var, width=50)
        self.product_combo.pack(fill=tk.X, pady=(0, 15))
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        ttk.Label(frame, text="2. Seleziona Fase:", font=("Helvetica", 10, "bold")).pack(fill=tk.X, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled", width=50)
        self.parent_phase_combo.pack(fill=tk.X, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        ttk.Button(frame, text="Chiudi", command=self.destroy).pack(side="bottom", pady=10)

    def _load_products(self):
        products = self.db.fetch_products()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            messagebox.showwarning("Dati Mancanti", "Nessun prodotto trovato nel database.", parent=self)

    def _on_product_keyrelease(self, event):
        typed_text = self.product_var.get()
        if not typed_text:
            self.product_combo['values'] = self.all_product_names
        else:
            filtered_list = [name for name in self.all_product_names if typed_text.lower() in name.lower()]
            self.product_combo['values'] = filtered_list

    def _on_product_select(self, event=None):
        self.parent_phase_var.set("")
        self.parent_phase_combo.config(state="disabled", values=[])

        product_id = self.products_data.get(self.product_var.get())
        if product_id:
            parent_phases = self.db.fetch_parent_phases(product_id)
            if parent_phases:
                self.parent_phases_data = {p.Phase: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo.config(state="readonly", values=list(self.parent_phases_data.keys()))
            else:
                messagebox.showerror("Dati non trovati", "Nessuna fase trovata per il prodotto selezionato.",
                                     parent=self)

    def _on_phase_select(self, event=None):
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        documents = self.db.fetch_existing_documents(product_id, parent_phase_id)
        validated_doc_path = None
        for doc in documents:
            if doc.IsValid:
                validated_doc_path = doc.DocumentPath
                break

        if validated_doc_path:
            self._open_with_adobe(validated_doc_path)
        else:
            messagebox.showwarning("Nessun Documento", "Nessun documento valido trovato per la fase selezionata.",
                                   parent=self)

    def _open_with_adobe(self, pdf_path):
        adobe_paths = [
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRd32.exe"
        ]
        adobe_exe = next((path for path in adobe_paths if os.path.exists(path)), None)

        try:
            if adobe_exe:
                print(f"Tentativo di apertura con Adobe Reader: {adobe_exe}")
                subprocess.Popen([adobe_exe, pdf_path])
            else:
                print("Adobe Reader non trovato, tento con il visualizzatore predefinito.")
                messagebox.showinfo("Adobe non trovato",
                                    "Adobe Reader non trovato. Il documento sarà aperto con il visualizzatore predefinito.",
                                    parent=self)
                os.startfile(pdf_path)
        except Exception as e:
            messagebox.showerror("Errore Apertura File", f"Impossibile aprire il file PDF.\n\nDettagli: {e}",
                                 parent=self)
            print(f"ERRORE APERTURA FILE: {e}")


class App(tk.Tk):
    """Classe principale dell'applicazione."""

    def __init__(self):
        super().__init__()
        self.title("Traceability document manager")
        self.geometry("800x600")

        self.db = Database(DB_CONN_STR)
        if not self.db.connect():
            self.destroy()
            return

        self._create_menu()
        self._add_logo()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _add_logo(self):
        if not PIL_AVAILABLE:
            print("Pillow non è installato. Impossibile visualizzare il logo.")
            return

        try:
            image = Image.open("logo.png")
            image.thumbnail((250, 250))
            self.logo_image = ImageTk.PhotoImage(image)

            logo_label = ttk.Label(self, image=self.logo_image)
            logo_label.pack(pady=20, expand=True)
        except FileNotFoundError:
            print("Errore: logo.png non trovato nella cartella dell'applicazione.")
        except Exception as e:
            print(f"Errore durante il caricamento del logo: {e}")

    def _create_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Menu Documenti
        document_menu = tk.Menu(self.menubar, tearoff=0)
        document_menu.add_command(label="Insert document", command=self.open_insert_form)
        document_menu.add_command(label="View document", command=self.open_view_form)
        document_menu.add_separator()
        document_menu.add_command(label="Quit", command=self._on_closing)
        self.menubar.add_cascade(label="Documents", menu=document_menu)

        # --- NUOVO MENU ---
        # Menu Help con la voce About
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        self.menubar.add_cascade(label="Help", menu=help_menu)

    def _show_about(self):
        # --- NUOVA FUNZIONE ---
        """Mostra la finestra di dialogo 'About' con le informazioni del software."""
        about_message = (
            f"Software Version: {APP_VERSION}\n"
            f"Software Developer: {APP_DEVELOPER}"
        )
        messagebox.showinfo(
            "About Traceability Document Manager",
            about_message,
            parent=self
        )

    def open_insert_form(self):
        login_form = LoginWindow(self, self.db)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            insert_form = InsertDocumentForm(self, self.db, authenticated_user)
            insert_form.transient(self)
            insert_form.grab_set()
            self.wait_window(insert_form)

    def open_view_form(self):
        view_form = ViewDocumentForm(self, self.db)
        view_form.transient(self)
        view_form.grab_set()
        self.wait_window(view_form)

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.db.disconnect()
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()