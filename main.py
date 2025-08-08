import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pyodbc
import os
import subprocess
from collections import defaultdict

# Import per gestire le immagini PNG
try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.2.01"  # Versione aggiornata
APP_DEVELOPER = "Gianluca Testa"

# --- CONFIGURAZIONE DATABASE ---
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = 'emsreset'
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_UID};PWD={DB_PWD};'


class LanguageManager:
    """Gestisce le traduzioni e la lingua corrente dell'applicazione."""

    def __init__(self, db_handler):
        self.db = db_handler
        self.translations = defaultdict(dict)
        self.current_language = 'it'  # Lingua predefinita
        self.load_translations()

    def load_translations(self):
        """Carica le traduzioni dal database."""
        records = self.db.fetch_translations()
        if not records:
            messagebox.showwarning("Traduzioni Mancanti",
                                   "Nessuna traduzione trovata nel database. Verrà usato il testo di default.")
            return
        for lang_code, key, value in records:
            self.translations[lang_code.lower()][key] = value

    def get(self, key, *args):
        """Restituisce la traduzione per una data chiave nella lingua corrente."""
        # Se la chiave non viene trovata, restituisce la chiave stessa per debugging
        translated_text = self.translations[self.current_language].get(key, key)
        if args:
            try:
                # Usa la sintassi .format() per i placeholder come {e}
                return translated_text.format(*args)
            except (IndexError, KeyError):
                return translated_text
        return translated_text

    def get_raw(self, key):
        """Restituisce il template di traduzione senza formattazione."""
        return self.translations[self.current_language].get(key, key)

    def set_language(self, lang_code):
        """Imposta la lingua corrente."""
        self.current_language = lang_code.lower()


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
            # A questo punto il LanguageManager non è ancora disponibile
            messagebox.showerror("Database Error", f"Cannot connect to the database.\n\nDetails: {ex}")
            return False

    def disconnect(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()

    def fetch_translations(self):
        query = "SELECT LanguageCode, TranslationKey, TranslationValue FROM Traceability_rs.dbo.AppTranslations;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Query Error", f"Error fetching translations: {e}")
            return []

    def fetch_products(self):
        query = "SELECT DISTINCT p.IDProduct, p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']' AS ProductCode FROM Traceability_RS.dbo.Products AS P INNER JOIN [Traceability_RS].[dbo].[ProductParentPhases] AS PP ON pp.IDProduct = p.IDProduct INNER JOIN Traceability_RS.dbo.ParentPhases AS PF ON pf.IDParentPhase = pp.IDParentPhase ORDER BY p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']';"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_products_with_documents(self):
        query = """
                SELECT p.IDProduct, \
                       p.ProductCode + ' [' + CAST(doc_counts.DocCount AS NVARCHAR(10)) + ' docs]' AS ProductCode
                FROM Traceability_RS.dbo.Products AS p \
                         INNER JOIN (SELECT ProductId, COUNT(*) AS DocCount \
                                     FROM Traceability_RS.dbo.ProductDocuments \
                                     WHERE DateOutOfValidation IS NULL \
                                     GROUP BY ProductId) AS doc_counts ON p.IDProduct = doc_counts.ProductId
                ORDER BY ProductCode; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_parent_phases(self, id_product):
        query = "SELECT distinct pf.IDParentPhase, pf.ParentPhaseName + IIF(pp.IDProduct IS NULL, '*', '') AS Phase FROM Traceability_RS.dbo.ParentPhases AS pf LEFT JOIN Traceability_RS.dbo.ProductParentPhases AS pp ON pf.IDParentPhase = pp.IDParentPhase AND pp.IDProduct = ? ORDER BY Phase;"
        try:
            self.cursor.execute(query, id_product)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_existing_documents(self, product_id, parent_phase_id):
        query = "SELECT documentName, DocumentRevisionNumber, DocumentPath, CONVERT(bit, Validated) as IsValid FROM Traceability_RS.dbo.ProductDocuments WHERE Productid = ? AND ParentPhaseId = ? AND DateOutOfValidation IS NULL;"
        try:
            self.cursor.execute(query, product_id, parent_phase_id)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def authenticate_user(self, user_id, password):
        query = "SELECT u.NomeUser, ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') as EmployeeName, u.pass FROM resetservices.dbo.tbuserkey as U INNER JOIN employee.dbo.employees as e ON e.EmployeeId = u.idanga INNER JOIN employee.dbo.EmployeeHireHistory as h ON e.EmployeeId = h.EmployeeId WHERE h.EndWorkDate IS NULL AND h.employeerid = 2 AND u.Nomeuser = ? AND Pass = ?;"
        try:
            self.cursor.execute(query, user_id, password)
            row = self.cursor.fetchone()
            return row.EmployeeName if row else None
        except pyodbc.Error:
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
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False


class LoginWindow(tk.Toplevel):
    """Finestra di autenticazione per l'utente."""

    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager
        self.authenticated_user_name = None

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self.update_texts()

    def _create_widgets(self):
        self.geometry("350x200")
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.user_id_label = ttk.Label(frame)
        self.user_id_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.user_id_entry = ttk.Entry(frame, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=10)

        self.password_label = ttk.Label(frame)
        self.password_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        self.login_button = ttk.Button(button_frame, command=self._attempt_login)
        self.login_button.pack(side="left", padx=10)
        self.cancel_button = ttk.Button(button_frame, command=self._on_cancel)
        self.cancel_button.pack(side="left", padx=10)

        self.user_id_entry.focus_set()

    def update_texts(self):
        """Aggiorna i testi della UI in base alla lingua corrente."""
        self.title(self.lang.get('login_title'))
        self.user_id_label.config(text=self.lang.get('login_user_id'))
        self.password_label.config(text=self.lang.get('login_password'))
        self.login_button.config(text=self.lang.get('login_button'))
        self.cancel_button.config(text=self.lang.get('login_cancel_button'))

    def _attempt_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if not user_id or not password:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_error_credentials'), parent=self)
            return

        employee_name = self.db.authenticate_user(user_id, password)
        if employee_name:
            self.authenticated_user_name = employee_name
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)
            self.password_entry.delete(0, tk.END)

    def _on_cancel(self):
        self.authenticated_user_name = None
        self.destroy()


class InsertDocumentForm(tk.Toplevel):
    """Finestra di inserimento documenti."""

    def __init__(self, master, db_handler, user_name, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.user_name = user_name
        self.lang = lang_manager

        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()
        self.file_name_var = tk.StringVar()
        self.revision_var = tk.StringVar()
        self.validated_var = tk.BooleanVar()

        self._create_widgets()
        self.update_texts()
        self._load_products()

    def _create_widgets(self):
        self.geometry("650x650")
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.product_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.product_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var)
        self.product_combo.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        self.phase_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.phase_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled")
        self.parent_phase_combo.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        self.details_frame = ttk.LabelFrame(frame, padding="10")
        self.details_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.details_frame.columnconfigure(1, weight=1)

        self.file_name_label = ttk.Label(self.details_frame)
        self.file_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_entry = ttk.Entry(self.details_frame, textvariable=self.file_name_var, state="disabled")
        self.file_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.browse_button = ttk.Button(self.details_frame, command=self._browse_file, state="disabled")
        self.browse_button.grid(row=0, column=2, padx=(0, 5), pady=5)

        self.revision_label = ttk.Label(self.details_frame)
        self.revision_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.revision_entry = ttk.Entry(self.details_frame, textvariable=self.revision_var, state="disabled")
        self.revision_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)

        self.validated_check = ttk.Checkbutton(self.details_frame, variable=self.validated_var, state="disabled")
        self.validated_check.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.docs_frame = ttk.LabelFrame(frame, padding="10")
        self.docs_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.docs_listbox = tk.Listbox(self.docs_frame, height=6, selectbackground="#a6a6a6")
        self.docs_listbox.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(frame, command=self._save_document, state="disabled")
        self.save_button.grid(row=6, column=1, sticky=tk.E, pady=10)

    def update_texts(self):
        """Aggiorna i testi della UI."""
        self.title(self.lang.get('insert_doc_title'))
        self.product_label.config(text=self.lang.get('label_select_product'))
        self.phase_label.config(text=self.lang.get('label_select_phase'))
        self.details_frame.config(text=self.lang.get('frame_new_doc_details'))
        self.file_name_label.config(text=self.lang.get('label_file_name'))
        self.browse_button.config(text=self.lang.get('button_browse'))
        self.revision_label.config(text=self.lang.get('label_revision'))
        self.validated_check.config(text=self.lang.get('check_validated'))
        self.docs_frame.config(text=self.lang.get('frame_active_docs'))
        self.save_button.config(text=self.lang.get('button_save'))
        self._refresh_document_list()

    def _load_products(self):
        products = self.db.fetch_products()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_products_found'))

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
                messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_no_phases_found'))
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
        # I filtri non sono nel DB, li lascio hardcoded ma con etichette generiche
        file_path = filedialog.askopenfilename(title=self.lang.get('insert_doc_title'),
                                               filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            self.file_name_var.set(file_path)

    def _save_document(self):
        if not all([self.product_var.get(), self.parent_phase_var.get(), self.file_name_var.get(),
                    self.revision_var.get()]):
            messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_input_all_fields'))
            return

        selected_product_display = self.product_var.get()
        if selected_product_display not in self.products_data:
            messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_input_invalid_product'))
            return

        revision = self.revision_var.get()
        if len(revision) > 10:
            msg = self.lang.get_raw('error_input_revision_length').replace('{revision}', revision).replace('{length}',
                                                                                                           str(len(
                                                                                                               revision)))
            messagebox.showerror(self.lang.get('app_title'), msg)
            return

        is_validated_bool = self.validated_var.get()
        validated_as_int = 1 if is_validated_bool else 0

        product_id = self.products_data.get(selected_product_display)
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())
        doc_path = self.file_name_var.get()
        doc_name = os.path.basename(doc_path)

        if self.db.save_document(product_id, parent_phase_id, doc_name, doc_path, revision, validated_as_int,
                                 self.user_name):
            messagebox.showinfo(self.lang.get('app_title'), self.lang.get('info_save_success'))
            self._reset_input_fields()
            self._refresh_document_list()
        else:
            msg = self.lang.get_raw('error_save_failed').replace('{e}', self.db.last_error_details)
            messagebox.showerror(self.lang.get('app_title'), msg)

    def _refresh_document_list(self):
        self.docs_listbox.delete(0, tk.END)
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        existing_docs = self.db.fetch_existing_documents(product_id, parent_phase_id)
        yes_text = self.lang.get('text_yes')
        no_text = self.lang.get('text_no')
        for i, doc in enumerate(existing_docs):
            is_valid_text = yes_text if doc.IsValid else no_text
            # Manteniamo un formato compatto per la listbox
            display_text = f"File: {doc.documentName} | Rev: {doc.DocumentRevisionNumber} | Validato: {is_valid_text}"
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

    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.transient(master)
        self.grab_set()

        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()

        self._create_widgets()
        self.update_texts()
        self._load_products()

    def _create_widgets(self):
        self.geometry("600x250")
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=1)

        self.product_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.product_label.pack(fill=tk.X, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var, width=50)
        self.product_combo.pack(fill=tk.X, pady=(0, 15))
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        self.phase_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.phase_label.pack(fill=tk.X, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled", width=50)
        self.parent_phase_combo.pack(fill=tk.X, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        self.close_button = ttk.Button(frame, command=self.destroy)
        self.close_button.pack(side="bottom", pady=10)

    def update_texts(self):
        """Aggiorna i testi della UI."""
        self.title(self.lang.get('view_doc_title'))
        self.product_label.config(text=self.lang.get('label_select_product'))
        self.phase_label.config(text=self.lang.get('label_select_phase'))
        self.close_button.config(text=self.lang.get('button_close'))

    def _load_products(self):
        products = self.db.fetch_products_with_documents()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            # Non esiste una chiave specifica per questo messaggio, riutilizzo quella esistente.
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_products_found'), parent=self)

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
                messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_no_phases_found'), parent=self)

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
           messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_document_found'), parent=self)

    def _open_with_adobe(self, pdf_path):
        adobe_paths = [
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRd32.exe"
        ]
        adobe_exe = next((path for path in adobe_paths if os.path.exists(path)), None)

        try:
            if adobe_exe:
                subprocess.Popen([adobe_exe, pdf_path])
            else:
                #messagebox.showinfo(self.lang.get('app_title'), self.lang.get('info_adobe_not_found'), parent=self)
                os.startfile(pdf_path)
        except Exception as e:
            msg = self.lang.get_raw('error_open_file').replace('{e}', str(e))
            messagebox.showerror(self.lang.get('app_title'), msg, parent=self)


class App(tk.Tk):
    """Classe principale dell'applicazione."""

    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.db = Database(DB_CONN_STR)
        if not self.db.connect():
            self.destroy()
            return

        self.lang = LanguageManager(self.db)

        self.logo_label = None  # Inizializza il logo label
        self._create_widgets()
        self._create_menu()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.update_texts()

    def _create_widgets(self):
        if not PIL_AVAILABLE:
            print("Pillow non è installato. Impossibile visualizzare il logo.")
            return
        try:
            image = Image.open("logo.png")
            image.thumbnail((250, 250))
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(self, image=self.logo_image)
            self.logo_label.pack(pady=20, expand=True)
        except FileNotFoundError:
            print("Errore: logo.png non trovato nella cartella dell'applicazione.")
        except Exception as e:
            print(f"Errore durante il caricamento del logo: {e}")

    def _create_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.document_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.help_menu)

        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale."""
        self.title(self.lang.get('app_title'))

        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)
        self.menubar.entryconfig(1, label=self.lang.get('menu_documents'))

        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        self.help_menu.add_command(label=self.lang.get('menu_about'), command=self._show_about)
        self.menubar.entryconfig(2, label=self.lang.get('menu_help'))

    def _change_language(self, lang_code):
        """Cambia la lingua e aggiorna la UI."""
        self.lang.set_language(lang_code)
        self.update_texts()

    def _show_about(self):
        about_template = self.lang.get_raw('about_message')
        about_message = about_template.replace('{version}', APP_VERSION).replace('{developer}', APP_DEVELOPER)
        messagebox.showinfo(
            self.lang.get('about_title'),
            about_message,
            parent=self
        )

    def open_insert_form(self):
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            insert_form = InsertDocumentForm(self, self.db, authenticated_user, self.lang)
            insert_form.transient(self)
            insert_form.grab_set()
            self.wait_window(insert_form)

    def open_view_form(self):
        view_form = ViewDocumentForm(self, self.db, self.lang)
        view_form.transient(self)
        view_form.grab_set()
        self.wait_window(view_form)

    def _on_closing(self):
        if messagebox.askokcancel(self.lang.get('quit_title'), self.lang.get('quit_message')):
            self.db.disconnect()
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()