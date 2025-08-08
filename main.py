import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pyodbc
import os
import subprocess
from collections import defaultdict
import sys
import maintenance_gui


# Import per gestire le immagini PNG
try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.4.0"  # Versione aggiornata
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
        translated_text = self.translations[self.current_language].get(key, key)
        if args:
            try:
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
    # Da aggiungere alla classe Database in main.py

    def fetch_all_equipments(self):
        """Recupera ID, Nome Interno e Seriale di tutte le macchine per la selezione."""
        query = "SELECT EquipmentId, InternalName, SerialNumber FROM eqp.Equipments ORDER BY InternalName, SerialNumber;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle macchine: {e}")
            return []

    def fetch_equipment_details(self, equipment_id):
        """Recupera i dettagli di una singola macchina per la modifica."""
        query = "SELECT ParentPhaseId, InternalName, SerialNumber FROM eqp.Equipments WHERE EquipmentId = ?;"
        try:
            self.cursor.execute(query, equipment_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei dettagli macchina: {e}")
            return None

    def update_and_log_equipment_changes(self, equipment_id, new_phase_id, new_internal_name, new_serial,
                                         change_log_string, user_name):
        """Aggiorna la macchina e registra la modifica in una transazione."""
        try:
            # 1. Aggiorna la tabella principale
            update_query = """
                           UPDATE eqp.Equipments
                           SET ParentPhaseId = ?, \
                               InternalName  = ?, \
                               SerialNumber  = ?
                           WHERE EquipmentId = ?; \
                           """
            self.cursor.execute(update_query, new_phase_id, new_internal_name, new_serial, equipment_id)

            # 2. Inserisce il log delle modifiche
            log_query = """
                        INSERT INTO eqp.EquipmentChanges (EquipmentId, Changed, WhoChange, DateChange)
                        VALUES (?, ?, ?, GETDATE()); \
                        """
            self.cursor.execute(log_query, equipment_id, change_log_string, user_name)

            # 3. Se entrambe le operazioni vanno a buon fine, conferma la transazione
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            # Se una delle due query fallisce, annulla tutto
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'aggiornamento della macchina: {e}")
            return False

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None
        self.cursor = None
        self.last_error_details = ""

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str, autocommit=False)
            self.cursor = self.conn.cursor()
            return True
        except pyodbc.Error as ex:
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
        # --- CORREZIONE: Rimossi i backslash '\' non necessari per una migliore leggibilità ---
        query = """
                SELECT p.IDProduct, \
                       p.ProductCode + ' [' + CAST(doc_counts.DocCount AS NVARCHAR(10)) + ' docs]' AS ProductCode
                FROM Traceability_RS.dbo.Products AS p
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

    # Dentro la classe Database

    def fetch_existing_documents(self, product_id, parent_phase_id):
        """
        CORRETTO: Recupera i metadati dei documenti (inclusa la chiave primaria ID)
        per una data fase, senza fare affidamento sulla vecchia colonna DocumentPath.
        """
        # La query ora non seleziona più DocumentPath, che è obsoleto.
        # Selezioniamo l'ID, che è fondamentale per recuperare i dati binari in un secondo momento.
        query = """
                SELECT DocumentProductionID, documentName, DocumentRevisionNumber, CONVERT(bit, Validated) as IsValid
                FROM Traceability_RS.dbo.ProductDocuments
                WHERE Productid = ?
                  AND ParentPhaseId = ?
                  AND DateOutOfValidation IS NULL; \
                """
        try:
            self.cursor.execute(query, product_id, parent_phase_id)
            # Il risultato ora sarà una lista di righe, ciascuna contenente (DocumentProductionID, nome, revisione, è_valido)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore critico in fetch_existing_documents: {e}")
            # In caso di errore, restituisce una lista vuota così l'interfaccia utente non si blocca.
            self.last_error_details = str(e)
            return []

    def authenticate_user(self, user_id, password):
        query = "SELECT u.NomeUser, ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') as EmployeeName, u.pass FROM resetservices.dbo.tbuserkey as U INNER JOIN employee.dbo.employees as e ON e.EmployeeId = u.idanga INNER JOIN employee.dbo.EmployeeHireHistory as h ON e.EmployeeId = h.EmployeeId WHERE h.EndWorkDate IS NULL AND h.employeerid = 2 AND u.Nomeuser = ? AND Pass = ?;"
        try:
            self.cursor.execute(query, user_id, password)
            row = self.cursor.fetchone()
            return row.EmployeeName if row else None
        except pyodbc.Error:
            return None

    # Da aggiungere all'interno della classe Database in main.py

    def fetch_brands(self):
        """Recupera tutti i brand delle macchine."""
        query = "SELECT EquipmentBrandId, Brand FROM eqp.EquipmentBrands ORDER BY Brand;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei brand: {e}")
            return []

    def fetch_equipment_types(self):
        """Recupera tutti i tipi di macchine."""
        query = "SELECT EquipmentTypeId, EquipmentType FROM eqp.EquipmentTypes ORDER BY EquipmentType;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei tipi di macchine: {e}")
            return []

    def fetch_parent_phases_for_maintenance(self):
        """Recupera tutte le fasi di produzione."""
        query = "SELECT IDParentPhase, ParentPhaseName FROM dbo.ParentPhases ORDER BY ParentPhaseName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle fasi di produzione: {e}")
            return []

    def add_new_equipment(self, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number):
        """Salva una nuova macchina nel database."""
        query = """
                INSERT INTO eqp.Equipments
                (BrandId, EquipmentTypeId, ParentPhaseId, SerialNumber, InternalName, ProductionYear, InventoryNumber, \
                 DateSys)
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE()) \
                """
        try:
            self.cursor.execute(query, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'inserimento della macchina: {e}")
            return False

    def fetch_and_open_document(self, document_id):
        """Recupera i dati binari di un PDF dal DB, li salva in un file temporaneo e lo apre."""
        try:
            # Assumendo che la colonna con i dati binari si chiami DocumentData
            sql_select = "SELECT DocumentData FROM Traceability_RS.dbo.ProductDocuments WHERE DocumentProductionID = ?"
            self.cursor.execute(sql_select, document_id)
            row = self.cursor.fetchone()

            if row and row.DocumentData:
                pdf_binary_data = row.DocumentData

                import tempfile
                # os è già importato globalmente

                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_file.write(pdf_binary_data)
                temp_file.close()

                print(f"Apertura del file temporaneo: {temp_file.name}")
                os.startfile(temp_file.name)
                return True
            else:
                print("Nessun dato binario trovato per questo ID documento.")
                return False

        except pyodbc.Error as e:
            print(f"Errore durante il recupero del documento dal DB: {e}")
            return False

    # --- CORREZIONE: Corretta la struttura del blocco try...except che causava un errore di sintassi ---
    def save_document_to_db(self, product_id, parent_phase_id, doc_name, local_file_path, revision, user_name,
                            validated_int):
        """Legge un file PDF e lo salva come VARBINARY(MAX) nel database."""
        try:
            # 1. Leggi il file dal tuo computer in modalità binaria ('rb')
            with open(local_file_path, 'rb') as f:
                pdf_binary_data = f.read()

            # 2. Prepara la query di INSERT con un parametro (?) per i dati binari
            sql_insert = """
                         INSERT INTO Traceability_RS.dbo.ProductDocuments
                         (ProductId, ParentPhaseId, documentName, DocumentRevisionNumber, DocumentData, InsertedBy, \
                          InsertionDate, Validated)
                         VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?) \
                         """

            # 3. Esegui la query passando i dati binari come parametro.
            self.cursor.execute(sql_insert,
                                product_id,
                                parent_phase_id,
                                doc_name,
                                revision,
                                pdf_binary_data,  # Dati del file
                                user_name,
                                validated_int)
            self.conn.commit()
            return True

        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante il salvataggio del documento nel DB: {e}")
            return False
        except FileNotFoundError:
            self.last_error_details = f"File non trovato al percorso: {local_file_path}"
            print(self.last_error_details)
            return False

    # Da aggiungere all'interno della classe Database

    def fetch_latest_version(self, software_name):
        """
        Recupera la stringa della versione più recente per un dato software.
        La versione più recente è indicata da dateout IS NULL.
        """
        query = "SELECT Version FROM traceability_rs.dbo.SwVersions WHERE NameProgram = ? AND dateout IS NULL"
        try:
            self.cursor.execute(query, software_name)
            row = self.cursor.fetchone()
            # Se trova una riga, restituisce la versione, altrimenti None
            return row.Version if row else None
        except pyodbc.Error as e:
            print(f"Errore durante il recupero della versione del software: {e}")
            # In caso di errore, è più sicuro non bloccare l'utente.
            # Potresti voler gestire questo caso in modo diverso.
            return None


# Sostituisci questa intera classe in main.py

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

        # --- CORREZIONE: Assicura che il tasto Invio attivi sempre il login ---
        # "Lega" l'evento <Return> (Invio) all'intera finestra.
        # In questo modo, funzionerà indipendentemente da quale widget ha il focus.
        self.bind('<Return>', self._attempt_login_event)
        # --- FINE CORREZIONE ---

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
        self.login_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(button_frame, command=self._on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        self.user_id_entry.focus_set()

    def update_texts(self):
        """Aggiorna i testi della UI in base alla lingua corrente."""
        self.title(self.lang.get('login_title'))
        self.user_id_label.config(text=self.lang.get('login_user_id'))
        self.password_label.config(text=self.lang.get('login_password'))
        self.login_button.config(text=self.lang.get('login_button'))
        self.cancel_button.config(text=self.lang.get('login_cancel_button'))

    # --- CORREZIONE: Aggiunto un metodo "wrapper" per gestire l'evento ---
    def _attempt_login_event(self, event=None):
        """Funzione chiamata dall'evento 'bind' per poi chiamare la logica di login."""
        self._attempt_login()

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
    # ... (Modificato _save_document per usare la nuova logica) ...
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
        file_path = filedialog.askopenfilename(title=self.lang.get('insert_doc_title'),
                                               filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            self.file_name_var.set(file_path)

    def _save_document(self):
        # Validazione input
        if not all([self.product_var.get(), self.parent_phase_var.get(), self.file_name_var.get(),
                    self.revision_var.get()]):
            messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_input_all_fields'))
            return

        # ... altre validazioni
        revision = self.revision_var.get()
        if len(revision) > 10:
            msg = self.lang.get_raw('error_input_revision_length').replace('{revision}', revision).replace('{length}',
                                                                                                           str(len(
                                                                                                               revision)))
            messagebox.showerror(self.lang.get('app_title'), msg)
            return

        # Recupero dati per il salvataggio
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())
        local_file_path = self.file_name_var.get()
        doc_name = os.path.basename(local_file_path)
        is_validated_bool = self.validated_var.get()
        validated_as_int = 1 if is_validated_bool else 0

        # --- CORREZIONE: Chiamata al nuovo metodo per salvare i dati binari ---
        success = self.db.save_document_to_db(
            product_id,
            parent_phase_id,
            doc_name,
            local_file_path,
            revision,
            self.user_name,
            validated_as_int
        )

        if success:
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
            display_text = f"File: {doc.documentName} | Rev: {doc.DocumentRevisionNumber} | Validato: {is_valid_text}"
            self.docs_listbox.insert(tk.END, display_text)
            if doc.IsValid:
                self.docs_listbox.itemconfig(i, {'bg': '#c8e6c9'})

    def _reset_phase_section(self):
        self.parent_phase_var.set("")
        self.parent_phase_combo.config(state="disabled", values=[])

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
        # --- CORREZIONE: Aggiunto per tenere traccia dei documenti della fase selezionata ---
        self.documents_in_phase = []

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()

        self._create_widgets()
        self.update_texts()
        self._load_products()

    def _create_widgets(self):
        # --- CORREZIONE: Aumentata l'altezza per far spazio alla lista dei documenti ---
        self.geometry("600x350")
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

        # --- CORREZIONE: Aggiunta una Listbox per selezionare quale documento aprire ---
        self.docs_listbox = tk.Listbox(frame, height=5)
        self.docs_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.docs_listbox.bind("<Double-1>", self._on_doc_double_click)  # Evento doppio click

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
        # --- CORREZIONE: Pulisce la lista dei documenti quando cambia il prodotto ---
        self.docs_listbox.delete(0, tk.END)
        self.documents_in_phase = []

        product_id = self.products_data.get(self.product_var.get())
        if product_id:
            parent_phases = self.db.fetch_parent_phases(product_id)
            if parent_phases:
                self.parent_phases_data = {p.Phase: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo.config(state="readonly", values=list(self.parent_phases_data.keys()))
            else:
                messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_no_phases_found'), parent=self)

    def _on_phase_select(self, event=None):
        """
        --- CORREZIONE: Questa funzione ora popola la lista dei documenti invece di tentare di aprirne uno. ---
        """
        self.docs_listbox.delete(0, tk.END)
        self.documents_in_phase = []

        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        # 1. Recupera la lista di tutti i documenti per la fase scelta
        self.documents_in_phase = self.db.fetch_existing_documents(product_id, parent_phase_id)

        if not self.documents_in_phase:
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_document_found'), parent=self)
        else:
            # 2. Popola la Listbox con i nomi dei documenti trovati
            for doc in self.documents_in_phase:
                self.docs_listbox.insert(tk.END, f"{doc.documentName} (Rev: {doc.DocumentRevisionNumber})")

    def _on_doc_double_click(self, event=None):
        """
        --- CORREZIONE: Nuovo metodo che gestisce il doppio click su un documento nella lista. ---
        """
        selected_indices = self.docs_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        # Recupera il documento corrispondente dalla lista che abbiamo salvato
        selected_doc = self.documents_in_phase[selected_index]

        # Chiama il metodo corretto per recuperare e aprire il file binario usando il suo ID
        print(f"Richiesta apertura documento con ID: {selected_doc.DocumentProductionID}")
        self.db.fetch_and_open_document(selected_doc.DocumentProductionID)


class App(tk.Tk):
    # ... (Nessuna modifica in questa classe) ...
    """Classe principale dell'applicazione."""

    def open_add_machine_with_login(self):
        """Apre la finestra di login e, se l'autenticazione ha successo, apre la finestra per aggiungere una macchina."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # Passiamo 'self', 'db', e 'lang' come argomenti
            maintenance_gui.open_add_machine(self, self.db, self.lang)

    # Modifica questo metodo nella classe App in main.py

    def open_edit_machine_with_login(self):
        """Apre la finestra di login e, se l'autenticazione ha successo, apre la finestra per modificare una macchina."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # Salva temporaneamente l'utente per passarlo alla finestra di modifica
            self.authenticated_user_for_maintenance = authenticated_user
            maintenance_gui.open_edit_machine(self, self.db, self.lang)

    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.db = Database(DB_CONN_STR)
        if not self.db.connect():
            self.destroy()
            return

        self.lang = LanguageManager(self.db)

        # --- INIZIO MODIFICA: LOGICA DI CONTROLLO VERSIONE ---
        # 1. Controlla la versione del software
        if self.check_version() is False:
            # Se il controllo fallisce, la finestra di errore è già stata mostrata.
            # Disconnetti e distruggi la finestra prima di uscire.
            self.db.disconnect()
            self.destroy()
            return  # Interrompe l'inizializzazione
        # --- FINE MODIFICA ---

        self.logo_label = None
        self._create_widgets()
        self._create_menu()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.update_texts()

    # Aggiungi questo nuovo metodo di supporto alla classe App
    def check_version(self):
        """
        Controlla la versione dell'applicazione contro il database.
        Restituisce False se l'aggiornamento è obbligatorio, altrimenti True.
        """
        try:
            # Usa sys.executable, che punta sempre al file .exe in un'app compilata.
            # È il metodo più robusto.
            app_name = os.path.basename(sys.executable)
            # --- FINE MODIFICA ---

            print(f"Nome eseguibile rilevato: {app_name}")  # Aggiunto per debugging
            latest_version = self.db.fetch_latest_version(app_name)

            # Se non troviamo una versione nel DB, procediamo per non bloccare l'utente
            if latest_version is None:
                print(f"Nessuna versione trovata nel database per '{app_name}'. Controllo saltato.")
                return True

            # Confronta la versione attuale con quella del DB
            if latest_version != APP_VERSION:
                # Le versioni non corrispondono, mostra un errore e blocca l'app
                title = self.lang.get("upgrade_required_title")
                message = self.lang.get("force_upgrade_message", APP_VERSION, latest_version)

                messagebox.showerror(title, message)
                return False  # Indica che l'app deve chiudersi

            # Le versioni corrispondono, tutto ok
            print(f"Versione applicazione ({APP_VERSION}) aggiornata.")
            return True

        except Exception as e:
            # In caso di qualsiasi errore, non blocchiamo l'utente
            print(f"Errore imprevisto durante il controllo versione: {e}")
            return True

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

    # All'interno della classe App in main.py

    def _create_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Menu Documenti
        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.document_menu)

        # --- NUOVO: Menu Manutenzione ---
        self.maintenance_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.maintenance_menu)
        # --- FINE NUOVO ---

        # Menu Help
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.help_menu)

        # Sottomenu Lingua (rimane dentro Help)
        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))

    # Sostituisci questo metodo nella classe App in main.py

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale."""
        self.title(self.lang.get('app_title'))

        # Menu Documenti (invariato)
        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)
        self.menubar.entryconfig(1, label=self.lang.get('menu_documents'))

        # Menu Manutenzione
        self.maintenance_menu.delete(0, 'end')

        machine_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        # --- INIZIO MODIFICA: I comandi ora puntano ai metodi con login ---
        machine_submenu.add_command(label=self.lang.get('submenu_add_machine'),
                                    command=self.open_add_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_edit_machine'),
                                    command=self.open_edit_machine_with_login)
        # --- FINE MODIFICA ---
        machine_submenu.add_command(label=self.lang.get('submenu_view_machines'),
                                    command=lambda: maintenance_gui.open_view_machines(self, self.db, self.lang))

        self.maintenance_menu.add_cascade(label=self.lang.get('submenu_machines'), menu=machine_submenu)
        self.maintenance_menu.add_command(label=self.lang.get('submenu_maintenance_docs'),
                                          command=lambda: maintenance_gui.open_maintenance_docs(self, self.db,
                                                                                                self.lang))
        self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
                                          command=lambda: maintenance_gui.open_fill_templates(self, self.db, self.lang))
        self.maintenance_menu.add_command(label=self.lang.get('submenu_reports'),
                                          command=lambda: maintenance_gui.open_reports(self, self.db, self.lang))

        self.menubar.entryconfig(2, label=self.lang.get('menu_maintenance'))

        # Menu Help (invariato)
        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        about_menu_label = f"{self.lang.get('menu_about')} {APP_VERSION}"
        self.help_menu.add_command(label=about_menu_label, command=self._show_about)
        self.menubar.entryconfig(3, label=self.lang.get('menu_help'))
    def _change_language(self, lang_code):
        """Cambia la lingua e aggiorna la UI."""
        self.lang.set_language(lang_code)
        self.update_texts()

    def _show_about(self):
        """Mostra la finestra di dialogo 'About' con le informazioni del software."""
        about_title = f"{self.lang.get('about_title')} - v{APP_VERSION}"
        about_template = self.lang.get_raw('about_message')
        about_message = about_template.replace('{version}', APP_VERSION).replace('{developer}', APP_DEVELOPER)

        messagebox.showinfo(
            about_title,  # Titolo aggiornato
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