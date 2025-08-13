# maintenance_gui.py
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import os
import reportlab
import richieste_intervento

# Import per ReportLab (necessari per MachineDetailsWindow)
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import Image as ReportLabImage
except ImportError:
    print("Warning: reportlab not installed. PDF generation might be affected.")

try:
    from PIL import Image, ImageTk
    # Necessario per MachineDetailsWindow se reportlab è installato
    from reportlab.platypus import Image as ReportLabImage
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ResolveDuplicateDocsWindow(tk.Toplevel):
    """Finestra per permettere all'utente di scegliere tra documenti esistenti e nuovi."""

    def __init__(self, parent, lang, existing_docs, new_doc_details):
        super().__init__(parent)
        self.lang = lang
        # Risultato della scelta: "KEEP_NEW", "KEEP_EXISTING", or None (se chiuso)
        self.result = None

        # Aggiungi queste chiavi di traduzione al tuo DB se non esistono
        self.title(self.lang.get('resolve_duplicates_title', "Risoluzione Conflitto Documenti"))
        self.geometry("850x400")
        self.transient(parent)
        self.grab_set()

        self._create_widgets(existing_docs, new_doc_details)

    def _create_widgets(self, existing_docs, new_doc_details):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # Messaggio informativo
        message = self.lang.get('resolve_duplicates_message',
                                "Esistono già documenti validi per questa combinazione. Cosa vuoi fare?")
        ttk.Label(frame, text=message, wraplength=820, font=("Helvetica", 10, "bold")).pack(pady=10)

        # Contenitore per le due sezioni (Sinistra e Destra)
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True, pady=10)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # --- SINISTRA: Documenti Esistenti (Treeview) ---
        existing_frame = ttk.LabelFrame(container,
                                        text=self.lang.get('existing_documents_label', "Documenti Esistenti Validi"),
                                        padding="10")
        existing_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Usiamo una Treeview perché potrebbero esserci più documenti attivi trovati dalla query
        cols = ('filename', 'date', 'user', 'description')
        self.tree = ttk.Treeview(existing_frame, columns=cols, show='headings', selectmode='none')
        self.tree.heading('filename', text=self.lang.get('header_filename', 'Nome File'))
        self.tree.heading('date', text=self.lang.get('header_date_upload', 'Data Caricamento'))
        self.tree.heading('user', text=self.lang.get('header_user', 'Utente'))
        self.tree.heading('description', text=self.lang.get('header_description', 'Descrizione'))

        self.tree.column('date', width=120)
        self.tree.column('user', width=80)
        self.tree.column('description', width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Popola la Treeview
        for doc in existing_docs:
            # Formatta la data per la visualizzazione (gestione robusta del tipo di dato)
            date_str = doc.DateUpload.strftime('%Y-%m-%d %H:%M') if hasattr(doc.DateUpload, 'strftime') else str(
                doc.DateUpload)
            # Mostra la descrizione recuperata dal DB
            self.tree.insert('', tk.END, values=(doc.Filename, date_str, doc.Uploadedby, doc.DocDescription or 'N/D'))

        # --- DESTRA: Nuovo Documento (Dettagli) ---
        new_frame = ttk.LabelFrame(container, text=self.lang.get('new_document_label', "Nuovo Documento"), padding="10")
        new_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        new_frame.columnconfigure(1, weight=1)

        # Mostra i dettagli del nuovo file
        ttk.Label(new_frame, text=self.lang.get('header_filename', 'Nome File:')).grid(row=0, column=0, sticky="w",
                                                                                       pady=5)
        ttk.Label(new_frame, text=new_doc_details['file_name'], wraplength=300, anchor="w", justify=tk.LEFT).grid(row=0,
                                                                                                                  column=1,
                                                                                                                  sticky="w",
                                                                                                                  pady=5)

        ttk.Label(new_frame, text=self.lang.get('header_user', 'Utente:')).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(new_frame, text=new_doc_details['user_name']).grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(new_frame, text=self.lang.get('description_label', 'Descrizione:')).grid(row=2, column=0, sticky="nw",
                                                                                           pady=5)
        ttk.Label(new_frame, text=new_doc_details['description'], wraplength=300, anchor="w", justify=tk.LEFT).grid(
            row=2, column=1, sticky="w", pady=5)

        # --- Pulsanti di Azione ---
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        # Pulsante per invalidare i vecchi e salvare il nuovo
        keep_new_text = self.lang.get('keep_new_button', "Invalida i vecchi e salva il nuovo")
        ttk.Button(button_frame, text=keep_new_text, command=self._keep_new).pack(side=tk.LEFT, padx=10)

        # Pulsante per mantenere i vecchi e annullare l'inserimento
        keep_existing_text = self.lang.get('keep_existing_button', "Mantieni i vecchi e annulla inserimento")
        ttk.Button(button_frame, text=keep_existing_text, command=self._keep_existing).pack(side=tk.LEFT, padx=10)

    def _keep_new(self):
        self.result = "KEEP_NEW"
        self.destroy()

    def _keep_existing(self):
        self.result = "KEEP_EXISTING"
        self.destroy()

class AddMachineWindow(tk.Toplevel):
    """Finestra per aggiungere una nuova macchina."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(self.lang.get('submenu_add_machine'))
        self.geometry("550x450")  # Aumentata leggermente l'altezza per il logo
        self.transient(parent)
        self.grab_set()

        # Dati per i combobox
        self.brands_data = {}
        self.types_data = {}
        self.phases_data = {}

        # Variabili di controllo
        self.brand_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.phase_var = tk.StringVar()
        self.serial_var = tk.StringVar()
        self.internal_name_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.inventory_var = tk.StringVar()

        self._create_widgets()
        self._load_combobox_data()

    def _create_widgets(self):
        """Crea e posiziona i widget nella finestra."""
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        frame.columnconfigure(1, weight=1)

        # --- Campi del form ---
        ttk.Label(frame, text=self.lang.get('brand_label')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.brand_combo = ttk.Combobox(frame, textvariable=self.brand_var, state='readonly')
        self.brand_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('type_label')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_combo = ttk.Combobox(frame, textvariable=self.type_var, state='readonly')
        self.type_combo.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('phase_label')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phase_combo = ttk.Combobox(frame, textvariable=self.phase_var, state='readonly')
        self.phase_combo.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('serial_number_label')).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.serial_entry = ttk.Entry(frame, textvariable=self.serial_var)
        self.serial_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('internal_name_label')).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.internal_name_entry = ttk.Entry(frame, textvariable=self.internal_name_var)
        self.internal_name_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('production_year_label')).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.year_entry = ttk.Entry(frame, textvariable=self.year_var)
        self.year_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('inventory_number_label')).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.inventory_entry = ttk.Entry(frame, textvariable=self.inventory_var)
        self.inventory_entry.grid(row=6, column=1, sticky=tk.EW, pady=5)

        # --- Pulsanti ---
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=1, sticky=tk.E, pady=(20, 0))

        self.save_button = ttk.Button(button_frame, text=self.lang.get('save_button'), command=self._save_machine)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text=self.lang.get('cancel_button'), command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT)

        # --- NUOVO: Aggiunta logo in basso a destra ---
        if PIL_AVAILABLE:
            try:
                # Carica l'immagine
                image = Image.open("logo.png")
                image.thumbnail((100, 100))  # Rimpicciolisce l'immagine se necessario
                # IMPORTANTE: conservare un riferimento all'immagine per evitare che venga eliminata
                self.logo_image = ImageTk.PhotoImage(image)

                # Crea e posiziona la label con il logo
                logo_label = ttk.Label(frame, image=self.logo_image)
                logo_label.grid(row=8, column=1, sticky=tk.SE, pady=(10, 0), padx=5)
            except FileNotFoundError:
                print("logo.png non trovato per la finestra di inserimento.")
            except Exception as e:
                print(f"Errore caricamento logo: {e}")

        # Rende l'ultima riga (quella del logo) espandibile per spingerlo in basso
        frame.rowconfigure(8, weight=1)

    def _load_combobox_data(self):
        # ... (questo metodo rimane invariato) ...
        """Carica i dati per i menu a tendina dal database."""
        # Carica Brand
        brands = self.db.fetch_brands()
        if brands:
            self.brands_data = {row.Brand: row.EquipmentBrandId for row in brands}
            self.brand_combo['values'] = list(self.brands_data.keys())

        # Carica Tipi Macchina
        types = self.db.fetch_equipment_types()
        if types:
            self.types_data = {row.EquipmentType: row.EquipmentTypeId for row in types}
            self.type_combo['values'] = list(self.types_data.keys())

        # Carica Fasi
        phases = self.db.fetch_parent_phases_for_maintenance()
        if phases:
            self.phases_data = {row.ParentPhaseName: row.IDParentPhase for row in phases}
            self.phase_combo['values'] = list(self.phases_data.keys())

    def _save_machine(self):
        # ... (questo metodo rimane invariato) ...
        """Valida i dati e li salva nel database."""
        # Validazione input
        if not all([self.brand_var.get(), self.type_var.get(), self.phase_var.get(), self.serial_var.get()]):
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_required_fields'), parent=self)
            return

        try:
            # Converte l'anno in numero, se inserito
            prod_year = int(self.year_var.get()) if self.year_var.get() else None
        except ValueError:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_invalid_year'), parent=self)
            return

        # Recupera gli ID dai valori selezionati nei combobox
        brand_id = self.brands_data.get(self.brand_var.get())
        type_id = self.types_data.get(self.type_var.get())
        phase_id = self.phases_data.get(self.phase_var.get())

        success = self.db.add_new_equipment(
            brand_id=brand_id,
            type_id=type_id,
            phase_id=phase_id,
            serial_number=self.serial_var.get(),
            internal_name=self.internal_name_var.get(),
            prod_year=prod_year,
            inv_number=self.inventory_var.get()
        )

        if success:
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('info_machine_saved'), parent=self)
            self.destroy()
        else:
            error_msg = self.lang.get('error_saving_machine') + f"\n\n{self.db.last_error_details}"
            messagebox.showerror(self.lang.get('error_title'), error_msg, parent=self)


# Sostituisci la vecchia EditMachineWindow con queste due classi in maintenance_gui.py

class SelectMachineToEditWindow(tk.Toplevel):
    """Finestra per selezionare quale macchina modificare."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.parent_app = parent
        self.user_name = user_name

        self.title(self.lang.get('select_machine_to_edit_title'))
        self.geometry("500x150")
        self.transient(parent)
        self.grab_set()

        self.equipments_data = {}
        self.selected_machine_var = tk.StringVar()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text=self.lang.get('select_machine_label')).pack(fill=tk.X)
        self.equipment_combo = ttk.Combobox(frame, textvariable=self.selected_machine_var, state='readonly', height=10)
        self.equipment_combo.pack(fill=tk.X, pady=5)

        ttk.Button(frame, text=self.lang.get('edit_button'), command=self._open_edit_window).pack(pady=10)

        self._load_equipments()

    def _load_equipments(self):
        """Carica la lista di tutte le macchine."""
        equipments = self.db.fetch_all_equipments()
        if equipments:
            # Crea un dizionario che mappa il testo visualizzato all'ID
            self.equipments_data = {f"{row.InternalName or 'N/D'} [{row.SerialNumber}]": row.EquipmentId for row in
                                    equipments}
            self.equipment_combo['values'] = list(self.equipments_data.keys())

    def _open_edit_window(self):
        """Apre la finestra di modifica per la macchina selezionata."""
        selection = self.selected_machine_var.get()
        if not selection:
            messagebox.showwarning(self.lang.get('warning_title'), self.lang.get('warning_no_machine_selected'),
                                   parent=self)
            return

        equipment_id = self.equipments_data.get(selection)

        # Apre la finestra di modifica passando tutti i parametri necessari
        EditMachineWindow(self.parent_app, self.db, self.lang, equipment_id, self.user_name)
        self.destroy()


class EditMachineWindow(tk.Toplevel):
    """Finestra per modificare i dati di una macchina specifica."""

    def __init__(self, parent, db, lang, equipment_id, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.equipment_id = equipment_id
        self.user_name = user_name

        # Per confrontare i valori prima/dopo
        self.original_data = {}
        self.phases_data = {}

        # Variabili di controllo
        self.phase_var = tk.StringVar()
        self.serial_var = tk.StringVar()
        self.internal_name_var = tk.StringVar()

        self.title(self.lang.get('submenu_edit_machine'))
        self.geometry("550x300")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text=self.lang.get('phase_label')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.phase_combo = ttk.Combobox(frame, textvariable=self.phase_var, state='readonly')
        self.phase_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('internal_name_label')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.internal_name_entry = ttk.Entry(frame, textvariable=self.internal_name_var)
        self.internal_name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('serial_number_label')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.serial_entry = ttk.Entry(frame, textvariable=self.serial_var)
        self.serial_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=1, sticky=tk.E, pady=(20, 0))
        ttk.Button(button_frame, text=self.lang.get('save_button'), command=self._save_changes).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button'), command=self.destroy).pack(side=tk.LEFT)

    def _load_data(self):
        """Carica i dati della macchina selezionata e li inserisce nei campi."""
        # Carica le fasi di produzione per il combobox
        phases = self.db.fetch_parent_phases_for_maintenance()
        if phases:
            self.phases_data = {row.IDParentPhase: row.ParentPhaseName for row in phases}
            self.phase_combo['values'] = list(self.phases_data.values())

        # Carica i dettagli della macchina specifica
        details = self.db.fetch_equipment_details(self.equipment_id)
        if details:
            self.original_data = details

            # Imposta i valori nei widget
            self.phase_var.set(self.phases_data.get(details.ParentPhaseId, ""))
            self.internal_name_var.set(details.InternalName or "")
            self.serial_var.set(details.SerialNumber or "")
        else:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_loading_machine_details'),
                                 parent=self)
            self.destroy()

    def _save_changes(self):
        """Costruisce il log delle modifiche e salva nel database."""
        # Recupera i nuovi valori
        new_phase_name = self.phase_var.get()
        new_phase_id = [k for k, v in self.phases_data.items() if v == new_phase_name][0]
        new_name = self.internal_name_var.get()
        new_serial = self.serial_var.get()

        # Costruisce la stringa di log confrontando i valori vecchi e nuovi
        change_log = []
        if new_phase_id != self.original_data.ParentPhaseId:
            original_phase_name = self.phases_data.get(self.original_data.ParentPhaseId, 'N/D')
            change_log.append(f"Fase cambiata da '{original_phase_name}' a '{new_phase_name}'.")

        if new_name != self.original_data.InternalName:
            change_log.append(f"Nome Interno cambiato da '{self.original_data.InternalName}' a '{new_name}'.")

        if new_serial != self.original_data.SerialNumber:
            change_log.append(f"Numero di Serie cambiato da '{self.original_data.SerialNumber}' a '{new_serial}'.")

        if not change_log:
            messagebox.showinfo(self.lang.get('info_title'), self.lang.get('info_no_changes'), parent=self)
            return

        # Unisce le modifiche in un'unica stringa
        change_log_string = " ".join(change_log)

        success = self.db.update_and_log_equipment_changes(
            self.equipment_id,
            new_phase_id,
            new_name,
            new_serial,
            change_log_string,
            self.user_name
        )

        if success:
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('info_machine_updated'), parent=self)
            self.destroy()
        else:
            error_msg = self.lang.get('error_updating_machine') + f"\n\n{self.db.last_error_details}"
            messagebox.showerror(self.lang.get('error_title'), error_msg, parent=self)


# In maintenance_gui.py, sostituisci la vecchia ViewMachineWindow con queste due classi

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Image as ReportLabImage


class ViewMachineWindow(tk.Toplevel):
    """Finestra di ricerca macchine con filtri."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.parent_app = parent

        self.title(self.lang.get('submenu_view_machines'))
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()

        self._create_filter_widgets()
        self._create_results_view()
        self._load_filter_data()

    def _create_filter_widgets(self):
        """Crea la sezione superiore con i filtri di ricerca."""
        filter_frame = ttk.LabelFrame(self, text=self.lang.get('search_filters_label'), padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # Inizializzazione dati
        self.brands_data, self.types_data, self.phases_data = {}, {}, {}
        self.brand_var, self.type_var, self.phase_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.search_text_var = tk.StringVar()

        # Creazione widget
        ttk.Label(filter_frame, text=self.lang.get('brand_label')).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.brand_combo = ttk.Combobox(filter_frame, textvariable=self.brand_var, state='readonly', width=20)
        self.brand_combo.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text=self.lang.get('type_label')).grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.type_combo = ttk.Combobox(filter_frame, textvariable=self.type_var, state='readonly', width=20)
        self.type_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(filter_frame, text=self.lang.get('phase_label')).grid(row=0, column=4, padx=5, pady=2, sticky=tk.W)
        self.phase_combo = ttk.Combobox(filter_frame, textvariable=self.phase_var, state='readonly', width=20)
        self.phase_combo.grid(row=0, column=5, padx=5, pady=2)

        ttk.Label(filter_frame, text=self.lang.get('search_text_label')).grid(row=1, column=0, padx=5, pady=2,
                                                                              sticky=tk.W)
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_text_var, width=50)
        self.search_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W)

        search_button = ttk.Button(filter_frame, text=self.lang.get('search_button'), command=self._perform_search)
        search_button.grid(row=1, column=4, padx=5, pady=5)

        clear_button = ttk.Button(filter_frame, text=self.lang.get('clear_filters_button'), command=self._clear_filters)
        clear_button.grid(row=1, column=5, padx=5, pady=5)

    def _create_results_view(self):
        """Crea la Treeview per mostrare i risultati della ricerca."""
        results_frame = ttk.Frame(self, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ('name', 'serial', 'brand', 'type', 'phase')
        self.tree = ttk.Treeview(results_frame, columns=cols, show='headings', selectmode='browse')

        # Definisci le intestazioni
        self.tree.heading('name', text=self.lang.get('header_internal_name'))
        self.tree.heading('serial', text=self.lang.get('header_serial_number'))
        self.tree.heading('brand', text=self.lang.get('header_brand'))
        self.tree.heading('type', text=self.lang.get('header_type'))
        self.tree.heading('phase', text=self.lang.get('header_phase'))

        self.tree.column('name', width=150)
        self.tree.column('serial', width=150)
        self.tree.column('brand', width=100)
        self.tree.column('type', width=120)
        self.tree.column('phase', width=120)

        # Aggiungi scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        # Evento doppio click per aprire i dettagli
        self.tree.bind('<Double-1>', self._open_details_window)

    def _load_filter_data(self):
        """Carica i dati per i combobox dei filtri."""
        brands = self.db.fetch_brands()
        self.brands_data = {row.Brand: row.EquipmentBrandId for row in brands}
        self.brand_combo['values'] = [''] + list(self.brands_data.keys())

        types = self.db.fetch_equipment_types()
        self.types_data = {row.EquipmentType: row.EquipmentTypeId for row in types}
        self.type_combo['values'] = [''] + list(self.types_data.keys())

        phases = self.db.fetch_parent_phases_for_maintenance()
        self.phases_data = {row.ParentPhaseName: row.IDParentPhase for row in phases}
        self.phase_combo['values'] = [''] + list(self.phases_data.keys())

    def _clear_filters(self):
        """Pulisce tutti i filtri di ricerca."""
        self.brand_var.set('')
        self.type_var.set('')
        self.phase_var.set('')
        self.search_text_var.set('')
        self._perform_search()

    def _perform_search(self):
        """Raccoglie i filtri, esegue la ricerca e popola la Treeview."""
        # Pulisci risultati precedenti
        for i in self.tree.get_children():
            self.tree.delete(i)

        filters = {
            'brand_id': self.brands_data.get(self.brand_var.get()),
            'type_id': self.types_data.get(self.type_var.get()),
            'phase_id': self.phases_data.get(self.phase_var.get()),
            'search_text': self.search_text_var.get()
        }

        results = self.db.search_equipments(filters)

        for row in results:
            # L'ID viene salvato come primo elemento della riga nella treeview
            self.tree.insert('', tk.END, iid=row.EquipmentId,
                             values=(row.InternalName, row.SerialNumber, row.Brand, row.EquipmentType,
                                     row.ParentPhaseName))

    def _open_details_window(self, event=None):
        """Apre la finestra di dettaglio per la macchina selezionata."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        equipment_id = int(selected_item)
        MachineDetailsWindow(self.parent_app, self.db, self.lang, equipment_id)


class MachineDetailsWindow(tk.Toplevel):
    """Finestra che mostra tutte le informazioni di una singola macchina."""

    def __init__(self, parent, db, lang, equipment_id):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.equipment_id = equipment_id
        self.details = None

        self.title(self.lang.get('machine_details_title'))
        self.geometry("900x700")
        self.transient(parent)
        self.grab_set()

        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_widgets()
        self._load_and_display_data()

    def _create_widgets(self):
        """Crea i widget per visualizzare i dettagli."""
        # Frame Anagrafica
        self.master_frame = ttk.LabelFrame(self.main_frame, text=self.lang.get('master_data_label'), padding="10")
        self.master_frame.pack(fill=tk.X, pady=5)

        # Frame Modifiche
        changes_frame = ttk.LabelFrame(self.main_frame, text=self.lang.get('changes_log_label'), padding="10")
        changes_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.changes_tree = ttk.Treeview(changes_frame, columns=('date', 'user', 'change'), show='headings')
        self.changes_tree.heading('date', text=self.lang.get('header_date'))
        self.changes_tree.heading('user', text=self.lang.get('header_user'))
        self.changes_tree.heading('change', text=self.lang.get('header_change'))
        self.changes_tree.pack(fill=tk.BOTH, expand=True)

        # Frame Documenti e Log (usiamo un Notebook)
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        docs_frame = ttk.Frame(notebook, padding="10")
        logs_frame = ttk.Frame(notebook, padding="10")
        notebook.add(docs_frame, text=self.lang.get('maintenance_docs_label'))
        notebook.add(logs_frame, text=self.lang.get('maintenance_logs_label'))

        self.docs_tree = ttk.Treeview(docs_frame, columns=('doc', 'user', 'date'), show='headings')
        self.docs_tree.heading('doc', text=self.lang.get('header_document'))
        self.docs_tree.heading('user', text=self.lang.get('header_user'))
        self.docs_tree.heading('date', text=self.lang.get('header_date'))
        self.docs_tree.pack(fill=tk.BOTH, expand=True)

        self.logs_tree = ttk.Treeview(logs_frame, columns=('date', 'user', 'notes'), show='headings')
        self.logs_tree.heading('date', text=self.lang.get('header_date'))
        self.logs_tree.heading('user', text=self.lang.get('header_user'))
        self.logs_tree.heading('notes', text=self.lang.get('header_notes'))
        self.logs_tree.pack(fill=tk.BOTH, expand=True)

        # Pulsante PDF
        pdf_button = ttk.Button(self.main_frame, text=self.lang.get('generate_pdf_button'), command=self._generate_pdf)
        pdf_button.pack(pady=10)

    def _load_and_display_data(self):
        """Carica tutti i dati e li visualizza nei widget appropriati."""
        self.details = self.db.fetch_full_equipment_details(self.equipment_id)
        if not self.details or not self.details.get('master'):
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_loading_machine_details'),
                                 parent=self)
            self.destroy()
            return

        # Popola anagrafica
        master = self.details['master']
        for i, (key, value) in enumerate(master.items()):
            ttk.Label(self.master_frame, text=f"{key}:", font="Helvetica 9 bold").grid(row=i, column=0, sticky=tk.W,
                                                                                       padx=5)
            ttk.Label(self.master_frame, text=value or "N/D").grid(row=i, column=1, sticky=tk.W, padx=5)

        # Popola log modifiche
        for item in self.details.get('changes', []):
            self.changes_tree.insert('', tk.END, values=(item.DateChange, item.WhoChange, item.Changed))

        # Popola documenti
        for item in self.details.get('docs', []):
            self.docs_tree.insert('', tk.END, values=(item.DocumentSource, item.UploadedBy, item.DateSys))

        # Popola log manutenzioni
        for item in self.details.get('logs', []):
            self.logs_tree.insert('', tk.END, values=(item.DataEsecuzione, item.IdManutentore, item.NoteGenerali))

    def _generate_pdf(self):
        """Genera un report PDF con i dettagli della macchina."""
        if not self.details: return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")],
            title=self.lang.get('save_pdf_title')
        )
        if not file_path: return

        master = self.details['master']
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Funzione ausiliaria per scrivere testo
        def draw_text(y, text, size=10, bold=False):
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, size)
            c.drawString(2 * cm, y, text)

        try:
            # Logo e Titolo
            if os.path.exists("logo.png"):
                logo = ReportLabImage("logo.png", width=3 * cm, height=3 * cm)
                logo.drawOn(c, width - 4.5 * cm, height - 3.5 * cm)

            draw_text(height - 2 * cm, self.lang.get('pdf_report_title'), 18, True)
            draw_text(height - 2.5 * cm,
                      f"{self.lang.get('pdf_print_date')}: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8)

            y_pos = height - 4 * cm
            # Dati Anagrafici
            draw_text(y_pos, self.lang.get('master_data_label'), 14, True)
            y_pos -= cm
            for key, value in master.items():
                draw_text(y_pos, f"{key}: {value or 'N/D'}")
                y_pos -= 0.5 * cm
                if y_pos < 3 * cm:  # Vai a pagina nuova
                    c.showPage()
                    y_pos = height - 3 * cm

            # Qui si potrebbero aggiungere le altre sezioni (modifiche, log, etc.)
            # con logica simile per gestire il cambio pagina.

            c.save()
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('pdf_generated_success'), parent=self)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title'), f"{self.lang.get('pdf_generated_error')}\n\n{e}",
                                 parent=self)


class AddMaintenanceDocWindow(tk.Toplevel):
    """Finestra per caricare un nuovo documento di manutenzione (Aggiornata con Tipo Doc e Descrizione)."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('submenu_add_maint_doc'))
        self.geometry("600x350")  # Aumentata l'altezza per i nuovi campi
        self.transient(parent)
        self.grab_set()

        # Dati
        self.equipments_data = {}
        self.interventions_data = {}
        # NUOVO: Per memorizzare i tipi di documento (EquipmentMaintenanceDocTypeId)
        self.doc_types_data = {}

        # Variabili di controllo
        self.equipment_var = tk.StringVar()
        self.intervention_var = tk.StringVar()
        # NUOVO
        self.doc_type_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.file_path_var = tk.StringVar()

        self._create_widgets()
        self._load_data()

    # Helper per la validazione del limite di caratteri (150) in tempo reale
    def _validate_description(self, P):
        # P è il valore potenziale dell'entry se la modifica viene permessa
        if len(P) <= 150:
            return True
        else:
            self.bell()  # Suono di avviso sistema se si supera il limite
            return False

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        # Registra la funzione di validazione per Tkinter
        vcmd = (self.register(self._validate_description), '%P')

        # 1. Selezione Macchina (Row 0)
        ttk.Label(frame, text=self.lang.get('select_machine_label')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.equipment_combo = ttk.Combobox(frame, textvariable=self.equipment_var, state='readonly', height=10)
        self.equipment_combo.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # 2. Selezione Intervento Programmato (Row 1)
        maint_type_label = self.lang.get('maintenance_type_label', 'Tipo Intervento:')
        ttk.Label(frame, text=maint_type_label).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.intervention_combo = ttk.Combobox(frame, textvariable=self.intervention_var, state='readonly', height=10)
        self.intervention_combo.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # 3. NUOVO: Selezione Tipo Documento (Row 2)
        doc_type_label_text = self.lang.get('doc_type_label', 'Tipo Documento:')
        ttk.Label(frame, text=doc_type_label_text).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.doc_type_combo = ttk.Combobox(frame, textvariable=self.doc_type_var, state='readonly', height=5)
        self.doc_type_combo.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # 4. NUOVO: Descrizione (Row 3)
        # Aggiungi questa chiave di traduzione ('description_label') al tuo database se non esiste
        description_label_text = self.lang.get('description_label', 'Descrizione (Max 150 car.):')
        ttk.Label(frame, text=description_label_text).grid(row=3, column=0, sticky=tk.W, pady=5)
        # Usiamo un Entry con validazione in tempo reale (validate="key", validatecommand=vcmd)
        self.description_entry = ttk.Entry(frame, textvariable=self.description_var, validate="key",
                                           validatecommand=vcmd)
        self.description_entry.grid(row=3, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # 5. Selezione File (Row 4)
        ttk.Label(frame, text=self.lang.get('select_document_label')).grid(row=4, column=0, sticky=tk.W, pady=5)
        file_entry = ttk.Entry(frame, textvariable=self.file_path_var, state='readonly')
        file_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)

        browse_button = ttk.Button(frame, text=self.lang.get('button_browse'), command=self._browse_file)
        browse_button.grid(row=4, column=2, padx=5, pady=5)

        # Pulsante Salva (Row 5)
        save_button = ttk.Button(frame, text=self.lang.get('save_button'), command=self._save_document)
        save_button.grid(row=5, column=1, columnspan=2, sticky=tk.E, pady=20)

    def _load_data(self):
        """Carica i dati per i combobox."""

        # 1. Carica macchine (Invariato)
        equipments = self.db.fetch_all_equipments()
        if equipments:
            self.equipments_data = {f"{row.InternalName or 'N/D'} [{row.SerialNumber}]": row.EquipmentId for row in
                                    equipments}
            self.equipment_combo['values'] = list(self.equipments_data.keys())

        # 2. Carica Interventi Programmati (Invariato)
        interventions = self.db.fetch_programmed_interventions()
        if interventions:
            for row in interventions:
                display_text = f"{row.TimingDescriprion} (Valore: {row.TimingValue})"
                self.interventions_data[display_text] = row.ProgrammedInterventionId
            self.intervention_combo['values'] = list(self.interventions_data.keys())

        # 3. NUOVO: Carica Tipi Documento Specifici (usando il nuovo metodo DB)
        doc_types = self.db.fetch_specific_maintenance_doc_types()
        if doc_types:
            for row in doc_types:
                # Mappa il testo (DocumentType) all'ID (EquipmentMaintenanceDocTypeId)
                self.doc_types_data[row.DocumentType] = row.EquipmentMaintenanceDocTypeId
            self.doc_type_combo['values'] = list(self.doc_types_data.keys())

    def _browse_file(self):
        # (Questo metodo rimane invariato)
        """Apre la finestra di dialogo per selezionare il file."""
        filetypes = [
            (self.lang.get('doc_filter_all_supported', "File Supportati"), "*.pdf;*.docx;*.doc;*.xlsx;*.xls"),
            ("PDF", "*.pdf"),
            ("Word", "*.docx;*.doc"),
            ("Excel", "*.xlsx;*.xls"),
            (self.lang.get('all_files_filter', "Tutti i file"), "*.*")
        ]
        file_path = filedialog.askopenfilename(title=self.lang.get('select_file_title'), filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)

    def _save_document(self):
        """Valida i dati, controlla i duplicati e gestisce il salvataggio/aggiornamento."""

        # --- 1. RECUPERO E VALIDAZIONE INPUT (Invariato) ---
        machine_selection = self.equipment_var.get()
        intervention_selection = self.intervention_var.get()
        doc_type_selection = self.doc_type_var.get()
        description = self.description_var.get().strip()
        file_path = self.file_path_var.get()

        # (Validazione campi obbligatori e lunghezza descrizione...)
        if not all([machine_selection, intervention_selection, doc_type_selection, description, file_path]):
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_all_fields_doc_required_extended',
                                                                             'Tutti i campi sono obbligatori.'),
                                 parent=self)
            return

        if len(description) > 150:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_description_too_long',
                                                                             'La descrizione non può superare i 150 caratteri.'),
                                 parent=self)
            return

        # --- 2. MAPPATURA ID (Invariato) ---
        equipment_id = self.equipments_data.get(machine_selection)
        programmed_intervention_id = self.interventions_data.get(intervention_selection)
        doc_type_id = self.doc_types_data.get(doc_type_selection)

        if not all([equipment_id, programmed_intervention_id, doc_type_id]):
            messagebox.showerror(self.lang.get('error_title'), "Errore interno: Impossibile trovare gli ID.",
                                 parent=self)
            return

        # --- 3. CONTROLLO DUPLICATI (NUOVA LOGICA) ---
        # Usa il nuovo metodo del database per trovare documenti attivi
        existing_docs = self.db.fetch_active_existing_maintenance_docs(equipment_id, programmed_intervention_id,
                                                                       doc_type_id)

        ids_to_invalidate = []
        file_name = os.path.basename(file_path)  # Definiamo file_name qui

        if existing_docs:
            # Prepara i dettagli del nuovo file per il confronto
            new_doc_details = {
                'file_name': file_name,
                'user_name': self.user_name,
                'description': description
            }

            # Mostra la finestra di risoluzione conflitti
            resolve_dialog = ResolveDuplicateDocsWindow(self, self.lang, existing_docs, new_doc_details)
            self.wait_window(resolve_dialog)  # Attendi che l'utente faccia la scelta

            decision = resolve_dialog.result

            if decision == "KEEP_EXISTING":
                messagebox.showinfo(self.lang.get('info_title'), self.lang.get('operation_cancelled',
                                                                               "Operazione annullata. Documenti esistenti mantenuti."),
                                    parent=self)
                return  # Interrompi il salvataggio
            elif decision == "KEEP_NEW":
                # L'utente vuole procedere. Prepariamo la lista degli ID da invalidare.
                ids_to_invalidate = [doc.EquipmentDocumentationId for doc in existing_docs]
            else:
                # L'utente ha chiuso la finestra senza scegliere (result è None)
                return  # Interrompi il salvataggio

        # --- 4. PROCESSO DI SALVATAGGIO (Lettura File e Transazione DB) ---
        try:
            # 4.1 Lettura File
            with open(file_path, 'rb') as f:
                binary_data = f.read()

            file_type = os.path.splitext(file_name)[1]

            # 4.2 Transazione DB (INSERT + eventuale UPDATE)
            # Chiama il metodo DB aggiornato (replace_maintenance_document), passando anche gli ID da invalidare
            success = self.db.replace_maintenance_document(
                equipment_id=equipment_id,
                intervention_id=programmed_intervention_id,
                doc_type_id=doc_type_id,
                description=description,
                file_name=file_name,
                file_type=file_type,
                binary_data=binary_data,
                user_name=self.user_name,
                invalidate_ids=ids_to_invalidate  # Passa la lista (può essere vuota)
            )

            # --- 5. GESTIONE RISULTATO E FEEDBACK ---
            if success:
                # Messaggio aggiornato per riflettere il versioning
                success_msg = self.lang.get('info_doc_saved', "Nuovo documento salvato con successo.")
                if ids_to_invalidate:
                    success_msg += "\n" + self.lang.get('info_old_doc_invalidated',
                                                        "Le versioni precedenti sono state invalidate (DateOut impostato).")

                messagebox.showinfo(self.lang.get('success_title'), success_msg, parent=self)
                self.destroy()
            else:
                # Il DB ha già eseguito il rollback. Mostriamo l'errore.
                messagebox.showerror(self.lang.get('error_title'), self.db.last_error_details, parent=self)

        except Exception as e:
            # Errore lettura file o altro errore imprevisto
            messagebox.showerror(self.lang.get('error_title'), f"{self.lang.get('error_reading_file')}\n\n{e}",
                                 parent=self)


class SearchMaintDocsWindow(tk.Toplevel):
    """Finestra per cercare, visualizzare e selezionare i documenti di manutenzione."""

    def __init__(self, parent, db, lang, mode, user_name=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.mode = mode  # 'view' o 'edit'
        self.user_name = user_name

        # Aggiorna il titolo in base alla modalità
        self.title(self.lang.get(f'submenu_{mode}_maint_doc'))
        self.geometry("1100x600")  # Aumentata larghezza per mostrare tutte le colonne
        self.transient(parent)
        self.grab_set()

        # Dati e variabili per i filtri
        self.equipments_data = {}
        self.interventions_data = {}
        self.doc_types_data = {}
        self.equipment_var = tk.StringVar()
        self.intervention_var = tk.StringVar()
        self.doc_type_var = tk.StringVar()
        # NUOVO: Checkbox per mostrare i documenti invalidati
        self.show_inactive_var = tk.BooleanVar(value=False)

        self._create_filter_widgets()
        self._create_results_view()
        self._load_filter_data()
        self._perform_search()  # Esegui una ricerca iniziale

    def _create_filter_widgets(self):
        filter_frame = ttk.LabelFrame(self, text=self.lang.get('search_filters_label'), padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # Filtro Macchina
        ttk.Label(filter_frame, text=self.lang.get('select_machine_label')).grid(row=0, column=0, padx=5, pady=5,
                                                                                 sticky=tk.W)
        self.equipment_combo = ttk.Combobox(filter_frame, textvariable=self.equipment_var, state='readonly', width=35)
        self.equipment_combo.grid(row=0, column=1, padx=5, pady=5)

        # Filtro Intervento
        ttk.Label(filter_frame, text=self.lang.get('maintenance_type_label', 'Intervento:')).grid(row=0, column=2,
                                                                                                  padx=5, pady=5,
                                                                                                  sticky=tk.W)
        self.intervention_combo = ttk.Combobox(filter_frame, textvariable=self.intervention_var, state='readonly',
                                               width=30)
        self.intervention_combo.grid(row=0, column=3, padx=5, pady=5)

        # Filtro Tipo Documento
        ttk.Label(filter_frame, text=self.lang.get('doc_type_label', 'Tipo Doc:')).grid(row=0, column=4, padx=5, pady=5,
                                                                                        sticky=tk.W)
        self.doc_type_combo = ttk.Combobox(filter_frame, textvariable=self.doc_type_var, state='readonly', width=25)
        self.doc_type_combo.grid(row=0, column=5, padx=5, pady=5)

        # Checkbox Mostra Inattivi
        ttk.Checkbutton(filter_frame, text=self.lang.get('show_inactive_check', "Includi versioni vecchie/eliminate"),
                        variable=self.show_inactive_var).grid(row=1, column=1, columnspan=3, padx=5, pady=5,
                                                              sticky=tk.W)

        # Pulsanti
        search_button = ttk.Button(filter_frame, text=self.lang.get('search_button'), command=self._perform_search)
        search_button.grid(row=1, column=5, padx=5, pady=5, sticky=tk.E)
        clear_button = ttk.Button(filter_frame, text=self.lang.get('clear_filters_button'), command=self._clear_filters)
        clear_button.grid(row=1, column=4, padx=5, pady=5, sticky=tk.E)

    def _create_results_view(self):
        results_frame = ttk.Frame(self, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Colonne Treeview (aggiunta 'date_out')
        cols = ('machine', 'intervention', 'doctype', 'filename', 'description', 'date', 'user', 'date_out')
        self.tree = ttk.Treeview(results_frame, columns=cols, show='headings', selectmode='browse')

        # Intestazioni
        self.tree.heading('machine', text=self.lang.get('header_internal_name'))
        self.tree.heading('intervention', text=self.lang.get('header_intervention', 'Intervento'))
        self.tree.heading('doctype', text=self.lang.get('header_doc_type', 'Tipo Doc'))
        self.tree.heading('filename', text=self.lang.get('header_filename', 'File'))
        self.tree.heading('description', text=self.lang.get('header_description', 'Descrizione'))
        self.tree.heading('date', text=self.lang.get('header_date_upload', 'Caricato il'))
        self.tree.heading('user', text=self.lang.get('header_user'))
        self.tree.heading('date_out', text=self.lang.get('header_date_out', 'Invalidato il'))

        # Configurazione larghezza colonne
        self.tree.column('machine', width=150)
        self.tree.column('intervention', width=120)
        self.tree.column('doctype', width=100)
        self.tree.column('filename', width=180)
        self.tree.column('description', width=150)
        self.tree.column('date', width=120)
        self.tree.column('user', width=80)
        self.tree.column('date_out', width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        # Configura il tag per i record invalidati (sfondo grigio)
        self.tree.tag_configure('inactive', background='#f0f0f0', foreground='gray')

        # Pulsante Azione (Modifica o Visualizza)
        action_button_text = self.lang.get('edit_manage_button',
                                           'Modifica/Gestisci') if self.mode == 'edit' else self.lang.get('view_button',
                                                                                                          'Visualizza')
        action_button = ttk.Button(results_frame, text=action_button_text, command=self._open_action_window)
        action_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Collega anche il doppio click
        self.tree.bind('<Double-1>', self._open_action_window)

    def _load_filter_data(self):
        # (Questo metodo rimane invariato rispetto alla versione precedente)
        # Macchine
        equipments = self.db.fetch_all_equipments()
        if equipments:
            self.equipments_data = {f"{row.InternalName or 'N/D'} [{row.SerialNumber}]": row.EquipmentId for row in
                                    equipments}
            self.equipment_combo['values'] = [''] + list(self.equipments_data.keys())

        # Interventi
        interventions = self.db.fetch_programmed_interventions()
        if interventions:
            intervention_map = {}
            for row in interventions:
                display_text = f"{row.TimingDescriprion} (Valore: {row.TimingValue})"
                intervention_map[display_text] = row.ProgrammedInterventionId
            self.interventions_data = intervention_map
            self.intervention_combo['values'] = [''] + list(self.interventions_data.keys())

        # Tipi Documento (Usiamo la lista specifica 1, 2, 5)
        doc_types = self.db.fetch_specific_maintenance_doc_types()
        if doc_types:
            self.doc_types_data = {row.DocumentType: row.EquipmentMaintenanceDocTypeId for row in doc_types}
            self.doc_type_combo['values'] = [''] + list(self.doc_types_data.keys())

    def _clear_filters(self):
        self.equipment_var.set('')
        self.intervention_var.set('')
        self.doc_type_var.set('')
        self.show_inactive_var.set(False)
        self._perform_search()

    def _perform_search(self):
        # Pulisci risultati precedenti
        for i in self.tree.get_children():
            self.tree.delete(i)

        filters = {
            'equipment_id': self.equipments_data.get(self.equipment_var.get()),
            'intervention_id': self.interventions_data.get(self.intervention_var.get()),
            'doc_type_id': self.doc_types_data.get(self.doc_type_var.get()),
        }

        include_inactive = self.show_inactive_var.get()

        # Esegui la ricerca (usando il metodo DB aggiornato in main.py)
        results = self.db.search_maintenance_documents(filters, include_inactive=include_inactive)

        # Popola la Treeview
        for row in results:
            # Formattazione data
            date_str = row.DateSys.strftime('%Y-%m-%d %H:%M') if hasattr(row.DateSys, 'strftime') else str(row.DateSys)
            date_out_str = row.DateOut.strftime('%Y-%m-%d %H:%M') if row.DateOut else ''

            # L'ID (EquipmentDocumentationId) viene usato come 'iid'
            self.tree.insert('', tk.END, iid=row.EquipmentDocumentationId,
                             values=(row.InternalName, row.InterventionName, row.DocumentType, row.FileName,
                                     row.DocDescription, date_str, row.UploadedBy, date_out_str))

            # Applica il tag se il documento è inattivo
            if row.DateOut:
                self.tree.item(row.EquipmentDocumentationId, tags=('inactive',))

    def _open_action_window(self, event=None):
        """Gestisce l'azione (Modifica o Visualizza) per il documento selezionato."""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning(self.lang.get('warning_title'),
                                   self.lang.get('warning_no_document_selected', "Nessun documento selezionato."),
                                   parent=self)
            return

        # L'ID è salvato come stringa (iid) nella treeview, riconvertiamolo in int
        doc_id = int(selected_item_id)

        if self.mode == 'edit':
            # Modalità 'edit' (già implementata nelle richieste precedenti)
            # Assicurati che la classe EditMaintenanceDocWindow sia presente nel file
            edit_window = EditMaintenanceDocWindow(self, self.db, self.lang, doc_id, self.user_name)
            self.wait_window(edit_window)
            # Aggiorna la ricerca dopo che la finestra di modifica si è chiusa
            self._perform_search()

        elif self.mode == 'view':
            # Modalità 'view' (NUOVA IMPLEMENTAZIONE)
            print(f"Richiesta visualizzazione documento ID: {doc_id}")

            # Chiama il nuovo metodo DB per aprire il file
            success = self.db.fetch_and_open_maintenance_document(doc_id)

            if not success:
                # Mostra un errore se il file non può essere aperto
                error_msg = self.lang.get('error_opening_document', "Impossibile aprire il documento.")

                # Aggiungi i dettagli dell'errore se disponibili (es. file non trovato, errore DB)
                # Controlliamo che l'attributo esista prima di accedervi
                if hasattr(self.db, 'last_error_details') and self.db.last_error_details:
                    error_msg += f"\n\nDettagli: {self.db.last_error_details}"

                messagebox.showerror(self.lang.get('error_title'), error_msg, parent=self)


class EditMaintenanceDocWindow(tk.Toplevel):
    """Finestra per gestire (Sostituire o Cancellare) un documento esistente."""

    def __init__(self, parent, db, lang, doc_id, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.doc_id = doc_id
        self.user_name = user_name
        self.doc_data = None  # Memorizza i dati del documento corrente

        self.title(self.lang.get('edit_maint_doc_title', "Gestione Documento Manutenzione"))
        self.geometry("600x500")  # Aumentata altezza per la descrizione modificabile
        self.transient(parent)
        self.grab_set()

        self.new_file_path_var = tk.StringVar()
        # NUOVO: Variabile per la descrizione (potenzialmente modificata durante la sostituzione)
        self.description_var = tk.StringVar()

        # Registra la validazione per il limite di 150 caratteri
        self.vcmd = (self.register(self._validate_description), '%P')

        self._create_widgets()
        self._load_document_data()

    def _validate_description(self, P):
        # Helper per limite 150 caratteri (identico a AddMaintenanceDocWindow)
        if len(P) <= 150:
            return True
        else:
            self.bell()
            return False

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Sezione Dettagli Documento Corrente (Read-Only) ---
        details_frame = ttk.LabelFrame(main_frame,
                                       text=self.lang.get('current_document_details', "Dettagli Documento Corrente"),
                                       padding="10")
        details_frame.pack(fill=tk.X, pady=5)
        details_frame.columnconfigure(1, weight=1)

        # Label variabili
        self.lbl_machine = ttk.Label(details_frame, text="N/D")
        self.lbl_intervention = ttk.Label(details_frame, text="N/D")
        self.lbl_doctype = ttk.Label(details_frame, text="N/D")
        self.lbl_filename = ttk.Label(details_frame, text="N/D", wraplength=400, justify=tk.LEFT)
        self.lbl_uploaded = ttk.Label(details_frame, text="N/D")

        # Posizionamento (Descrizione rimossa qui, spostata nella sezione sostituzione)
        ttk.Label(details_frame, text=self.lang.get('select_machine_label')).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lbl_machine.grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=self.lang.get('maintenance_type_label')).grid(row=1, column=0, sticky=tk.W,
                                                                                    pady=2)
        self.lbl_intervention.grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=self.lang.get('doc_type_label')).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.lbl_doctype.grid(row=2, column=1, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=self.lang.get('label_file_name')).grid(row=3, column=0, sticky=tk.NW, pady=2)
        self.lbl_filename.grid(row=3, column=1, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=self.lang.get('header_date_upload')).grid(row=4, column=0, sticky=tk.W, pady=2)
        self.lbl_uploaded.grid(row=4, column=1, sticky=tk.W, pady=2)

        # --- Sezione Azione 1: Sostituzione (Replace) ---
        replace_frame = ttk.LabelFrame(main_frame,
                                       text=self.lang.get('action_replace_document', "Azione 1: Sostituisci Documento"),
                                       padding="10")
        replace_frame.pack(fill=tk.X, pady=10)
        replace_frame.columnconfigure(1, weight=1)

        # NUOVO: Descrizione modificabile (pre-popolata con quella esistente)
        description_label_text = self.lang.get('new_description_label', 'Descrizione (Max 150 car.):')
        ttk.Label(replace_frame, text=description_label_text).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.description_entry = ttk.Entry(replace_frame, textvariable=self.description_var, validate="key",
                                           validatecommand=self.vcmd)
        self.description_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # Selezione nuovo file
        ttk.Label(replace_frame, text=self.lang.get('select_new_file', "Seleziona nuovo file:")).grid(row=1, column=0,
                                                                                                      sticky=tk.W,
                                                                                                      pady=5)
        file_entry = ttk.Entry(replace_frame, textvariable=self.new_file_path_var, state='readonly')
        file_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        browse_button = ttk.Button(replace_frame, text=self.lang.get('button_browse'), command=self._browse_file)
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.replace_button = ttk.Button(replace_frame,
                                         text=self.lang.get('confirm_replace_button', "Conferma Sostituzione"),
                                         command=self._replace_document)
        self.replace_button.grid(row=2, column=2, pady=5)

        # --- Sezione Azione 2: Cancellazione (Delete/Invalidate) ---
        delete_frame = ttk.LabelFrame(main_frame,
                                      text=self.lang.get('action_delete_document', "Azione 2: Cancella Documento"),
                                      padding="10")
        delete_frame.pack(fill=tk.X, pady=5)

        ttk.Label(delete_frame, text=self.lang.get('delete_warning_message',
                                                   "Questa azione imposterà DateOut sul documento corrente.")).pack(
            side=tk.LEFT, padx=5)
        self.delete_button = ttk.Button(delete_frame,
                                        text=self.lang.get('confirm_delete_button', "Conferma Cancellazione"),
                                        command=self._delete_document)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

    def _load_document_data(self):
        """Carica i dati del documento dal DB e aggiorna la UI."""
        self.doc_data = self.db.fetch_maintenance_doc_by_id(self.doc_id)

        if not self.doc_data:
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('error_document_not_found', "Documento non trovato."), parent=self)
            self.destroy()
            return

        # Aggiorna le Label
        self.lbl_machine.config(text=self.doc_data.InternalName)
        self.lbl_intervention.config(text=self.doc_data.TimingDescriprion)
        self.lbl_doctype.config(text=self.doc_data.DocumentType)
        self.lbl_filename.config(text=self.doc_data.FileName)

        # Popola il campo descrizione modificabile
        self.description_var.set(getattr(self.doc_data, 'DocDescription', '') or "")

        date_str = self.doc_data.DateSys.strftime('%Y-%m-%d %H:%M') if hasattr(self.doc_data.DateSys,
                                                                               'strftime') else str(
            self.doc_data.DateSys)
        self.lbl_uploaded.config(text=f"{date_str} da {self.doc_data.UploadedBy}")

        # Controlla se il documento è già invalidato
        if self.doc_data.DateOut is not None:
            messagebox.showwarning(self.lang.get('warning_title'), self.lang.get('warning_doc_already_inactive',
                                                                                 "Questo documento è già stato invalidato. Non sono permesse modifiche."),
                                   parent=self)
            # Disabilita i pulsanti di azione e il campo descrizione
            self.replace_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.description_entry.config(state="disabled")

    def _browse_file(self):
        # (Invariato)
        filetypes = [
            (self.lang.get('doc_filter_all_supported', "File Supportati"), "*.pdf;*.docx;*.doc;*.xlsx;*.xls"),
            ("PDF", "*.pdf"), ("Word", "*.docx;*.doc"), ("Excel", "*.xlsx;*.xls"),
            (self.lang.get('all_files_filter', "Tutti i file"), "*.*")
        ]
        file_path = filedialog.askopenfilename(title=self.lang.get('select_file_title'), filetypes=filetypes,
                                               parent=self)
        if file_path:
            self.new_file_path_var.set(file_path)

    def _replace_document(self):
        """Sostituisce il documento corrente con il nuovo file e la nuova descrizione."""
        file_path = self.new_file_path_var.get()
        description = self.description_var.get().strip()  # Recupera la descrizione (potenzialmente modificata)

        if not file_path or not description:
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_replacement_fields_required',
                                                                             "Selezionare un nuovo file e inserire una descrizione."),
                                 parent=self)
            return

        # Conferma dell'utente
        if not messagebox.askyesno(self.lang.get('confirm_replace_title', "Conferma Sostituzione"),
                                   self.lang.get('confirm_replace_message',
                                                 "Sei sicuro di voler sostituire il documento corrente? Verrà invalidato e il nuovo file verrà caricato."),
                                   parent=self):
            return

        try:
            # 1. Lettura nuovo file
            with open(file_path, 'rb') as f:
                binary_data = f.read()

            file_name = os.path.basename(file_path)
            file_type = os.path.splitext(file_name)[1]

            # 2. Transazione DB (Usiamo la funzione replace_maintenance_document)
            # I parametri EquipmentId, InterventionId, DocTypeId vengono ereditati dal documento originale.
            # La descrizione viene presa dal campo modificabile.
            success = self.db.replace_maintenance_document(
                equipment_id=self.doc_data.EquipmentId,
                intervention_id=self.doc_data.ProgrammedInterventionId,
                doc_type_id=self.doc_data.EquipmentMaintenanceDocTypeId,
                description=description,  # Usa la descrizione aggiornata
                file_name=file_name,
                file_type=file_type,
                binary_data=binary_data,
                user_name=self.user_name,
                invalidate_ids=[self.doc_id]  # Invalida SOLO il documento corrente
            )

            if success:
                messagebox.showinfo(self.lang.get('success_title'),
                                    self.lang.get('info_doc_replaced_success', "Documento sostituito con successo."),
                                    parent=self)
                self.destroy()
            else:
                messagebox.showerror(self.lang.get('error_title'), self.db.last_error_details, parent=self)

        except Exception as e:
            messagebox.showerror(self.lang.get('error_title'), f"{self.lang.get('error_reading_file')}\n\n{e}",
                                 parent=self)

    def _delete_document(self):
        """Invalida il documento corrente senza sostituirlo."""

        # Conferma dell'utente (Azione pericolosa)
        if not messagebox.askyesno(self.lang.get('confirm_delete_title', "Conferma Cancellazione"),
                                   self.lang.get('confirm_delete_message',
                                                 "Sei sicuro di voler cancellare (invalidare) questo documento? L'operazione non è reversibile."),
                                   parent=self, icon='warning'):
            return

        # Chiama la nuova funzione DB per invalidare il singolo documento
        success = self.db.invalidate_single_maintenance_doc(self.doc_id, self.user_name)

        if success:
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('info_doc_deleted_success',
                                                                              "Documento invalidato con successo (DateOut impostato)."),
                                parent=self)
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title'), self.db.last_error_details, parent=self)



# --- Funzioni Launcher aggiornate/nuove ---
def open_add_maintenance_doc(parent, db, lang, user_name):
    AddMaintenanceDocWindow(parent, db, lang, user_name)


def open_search_maintenance_doc(parent, db, lang, mode, user_name=None):
    # Questa è una finestra segnaposto per la logica di ricerca
    SearchMaintDocsWindow(parent, db, lang, mode, user_name)


# ... le altre funzioni launcher rimangono invariate ...

# --- Finestre Segnaposto per le Altre Funzionalità di Manutenzione ---

class MaintenanceDocsWindow(tk.Toplevel):
    """Finestra per la gestione dei documenti di manutenzione."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.title(lang.get('submenu_maintenance_docs'))
        self.geometry("600x400")
        ttk.Label(self, text="Finestra Documenti Manutenzione - In Sviluppo", font=("Helvetica", 16)).pack(pady=50,
                                                                                                           padx=20)
        self.transient(parent)
        self.grab_set()


class FillTemplateWindow(tk.Toplevel):
    """Finestra per la compilazione delle schede di manutenzione."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.start_time = None  # Variabile per memorizzare l'ora di inizio (Requisito)

        self.title(lang.get('submenu_fill_templates'))
        self.geometry("950x600")  # Dimensione adeguata per visualizzare i compiti
        self.transient(parent)
        self.grab_set()

        # Dati e variabili
        self.equipments_data = {}
        self.plans_data = {}  # Mappa il testo del piano a (PianoManutenzioneId, ProgrammedInterventionId)
        # Memorizza gli ID (CompitoId) dei compiti spuntati
        self.completed_tasks = set()

        self.equipment_var = tk.StringVar()
        self.plan_var = tk.StringVar()

        # Inizializzazione widget (per sicurezza)
        self.tasks_tree = None
        self.notes_text = None
        self.save_button = None
        self.request_button = None
        self.plan_combo = None

        self._create_widgets()
        self._load_equipments()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Sezione Selezione (Top) ---
        selection_frame = ttk.Frame(frame)
        selection_frame.pack(fill=tk.X, pady=10)

        # 1. Selezione Macchina
        ttk.Label(selection_frame, text=self.lang.get('select_machine_label')).pack(side=tk.LEFT, padx=5)
        self.equipment_combo = ttk.Combobox(selection_frame, textvariable=self.equipment_var, state='readonly',
                                            width=40)
        self.equipment_combo.pack(side=tk.LEFT, padx=5)
        # Il binding che causava l'errore (ora punta al metodo corretto definito sotto)
        self.equipment_combo.bind("<<ComboboxSelected>>", self._on_equipment_select)

        # 2. Selezione Piano Manutenzione
        ttk.Label(selection_frame, text=self.lang.get('select_maintenance_plan', "Seleziona Piano:")).pack(side=tk.LEFT,
                                                                                                           padx=5)
        self.plan_combo = ttk.Combobox(selection_frame, textvariable=self.plan_var, state='disabled', width=40)
        self.plan_combo.pack(side=tk.LEFT, padx=5)
        self.plan_combo.bind("<<ComboboxSelected>>", self._on_plan_select)

        # --- Sezione Compiti (Center) ---
        tasks_frame = ttk.LabelFrame(frame, text=self.lang.get('maintenance_tasks_label', "Compiti da Eseguire"),
                                     padding="10")
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Treeview per i compiti con checkbox simulati
        cols = ('check', 'name', 'category', 'description')
        self.tasks_tree = ttk.Treeview(tasks_frame, columns=cols, show='headings')

        # Configurazione colonne
        self.tasks_tree.heading('check', text='☑')
        self.tasks_tree.heading('name', text=self.lang.get('header_task_name', 'Compito'))
        self.tasks_tree.heading('category', text=self.lang.get('header_category', 'Categoria'))
        self.tasks_tree.heading('description', text=self.lang.get('header_description', 'Descrizione'))

        self.tasks_tree.column('check', width=30, anchor='center', stretch=tk.NO)
        self.tasks_tree.column('name', width=250)
        self.tasks_tree.column('category', width=120)
        self.tasks_tree.column('description', width=450)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscroll=scrollbar.set)

        self.tasks_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Gestione click e doppio click
        self.tasks_tree.bind('<Button-1>', self._on_tree_click)
        self.tasks_tree.bind('<Double-1>', self._on_tree_double_click)

        # --- Sezione Note (Bottom-Center) ---
        notes_frame = ttk.LabelFrame(frame,
                                     text=self.lang.get('maintenance_notes_label', "Note Generali / Osservazioni"),
                                     padding="10")
        notes_frame.pack(fill=tk.X, pady=5)

        self.notes_text = tk.Text(notes_frame, height=4, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X, expand=True, padx=5)
        self.notes_text.config(state='disabled')

        # --- Sezione Azioni (Bottom) ---
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill=tk.X, pady=10)

        # Pulsante Richiesta
        request_button_text = self.lang.get('request_button', "Crea Richiesta (Parti/Intervento)")
        self.request_button = ttk.Button(action_frame, text=request_button_text, command=self._open_request_window,
                                         state='disabled')
        self.request_button.pack(side=tk.LEFT, padx=5)

        # Pulsante Salva
        self.save_button = ttk.Button(action_frame,
                                      text=self.lang.get('save_completed_tasks', "Salva Compiti Eseguiti"),
                                      command=self._save_logs, state='disabled')
        self.save_button.pack(side=tk.RIGHT, padx=5)

    def _load_equipments(self):
        # (Invariato)
        equipments = self.db.fetch_all_equipments()
        if equipments:
            self.equipments_data = {f"{row.InternalName or 'N/D'} [{row.SerialNumber}]": row.EquipmentId for row in
                                    equipments}
            self.equipment_combo['values'] = list(self.equipments_data.keys())

    def _reset_plan_and_tasks(self):
        self.plan_var.set("")
        if self.plan_combo:
            self.plan_combo.config(state='disabled', values=[])
        self.plans_data = {}
        self._reset_tasks()

    def _reset_tasks(self):
        # Controllo difensivo: Assicurati che i widget esistano prima di accedervi
        if self.tasks_tree:
            for i in self.tasks_tree.get_children():
                self.tasks_tree.delete(i)

        self.completed_tasks = set()
        self.start_time = None

        if self.save_button:
            self.save_button.config(state='disabled')

        # Pulisci e disabilita il campo note e il pulsante richiesta
        if self.notes_text:
            self.notes_text.config(state='normal')
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.config(state='disabled')

        if self.request_button:
            self.request_button.config(state='disabled')

    # !!! METODO MANCANTE CHE CAUSAVA L'ERRORE !!!
    def _on_equipment_select(self, event=None):
        self._reset_plan_and_tasks()
        equipment_id = self.equipments_data.get(self.equipment_var.get())

        if equipment_id:
            # Chiama il metodo DB per la Query 1
            plans = self.db.fetch_available_maintenance_plans(equipment_id)
            if plans:
                # Mappiamo il testo descrittivo a una tupla (PianoManutenzioneId, ProgrammedInterventionId)
                self.plans_data = {row.TimingDescriprion: (row.PianoManutenzioneId, row.ProgrammedInterventionId) for
                                   row in plans}
                self.plan_combo['values'] = list(self.plans_data.keys())
                self.plan_combo.config(state='readonly')
            else:
                messagebox.showinfo(self.lang.get('info_title'), self.lang.get('info_no_plans_available',
                                                                               "Nessun piano di manutenzione disponibile o tutti i compiti sono già stati eseguiti per questa macchina."),
                                    parent=self)

    def _on_plan_select(self, event=None):
        self._reset_tasks()
        plan_selection = self.plan_var.get()
        if plan_selection and plan_selection in self.plans_data:
            # Recupera ProgrammedInterventionId dalla tupla memorizzata (indice 1)
            _, programmed_intervention_id = self.plans_data[plan_selection]

            # --- TIME TRACKING: Memorizza l'ora corrente ---
            self.start_time = datetime.now()
            print(f"Inizio compilazione scheda alle: {self.start_time}")

            # Chiama il metodo DB per la Query 2
            tasks = self.db.fetch_maintenance_tasks(programmed_intervention_id)

            if tasks:
                for task in tasks:
                    task_id = task.compitoid
                    # Inserisce nella Treeview, usando task_id come iid
                    self.tasks_tree.insert('', tk.END, iid=task_id,
                                           values=("", task.nomecompito, task.categoria, task.descrizioneCompito))

                # Abilita salvataggio, note e richieste
                self.save_button.config(state='normal')
                self.notes_text.config(state='normal')
                self.request_button.config(state='normal')
            else:
                messagebox.showwarning(self.lang.get('warning_title'),
                                       self.lang.get('warn_no_tasks_found', "Nessun compito trovato per questo piano."),
                                       parent=self)

    def _on_tree_click(self, event):
        # Gestisce il click per simulare un checkbox nella Treeview
        region = self.tasks_tree.identify("region", event.x, event.y)
        column = self.tasks_tree.identify_column(event.x)

        # Controlla se il click è avvenuto su una cella e nella prima colonna (#1, che è 'check')
        if region == "cell" and column == "#1":
            item_iid = self.tasks_tree.identify_row(event.y)
            if item_iid:
                try:
                    task_id = int(item_iid)
                except ValueError:
                    return

                # Inverti lo stato del checkbox
                if task_id in self.completed_tasks:
                    self.completed_tasks.remove(task_id)
                    self.tasks_tree.set(item_iid, 'check', "")
                else:
                    self.completed_tasks.add(task_id)
                    self.tasks_tree.set(item_iid, 'check', "✔")  # Carattere Unicode ✔

    def _on_tree_double_click(self, event):
        """Gestisce il doppio click su un compito per aprire il documento associato."""

        item_iid = self.tasks_tree.focus()

        if not item_iid:
            return

        # Evita l'esecuzione se si fa doppio click sulla colonna checkbox
        column = self.tasks_tree.identify_column(event.x)
        if column == "#1":
            return

        try:
            task_id = int(item_iid)
        except ValueError:
            return

        print(f"Richiesta apertura documento per CompitoId: {task_id}")

        # Chiama il metodo DB (definito in main.py)
        success = self.db.fetch_and_open_document_by_task_id(task_id)

        if not success:
            error_msg = self.lang.get('error_opening_task_document',
                                      "Impossibile aprire il documento associato al compito.")

            if hasattr(self.db, 'last_error_details') and self.db.last_error_details:
                error_msg += f"\n\n{self.db.last_error_details}"

            messagebox.showwarning(self.lang.get('warning_title'), error_msg, parent=self)

    def _open_request_window(self):
        # Recupera le informazioni necessarie sulla macchina corrente
        equipment_name = self.equipment_var.get()
        equipment_id = self.equipments_data.get(equipment_name)

        if not equipment_id:
            # Questo non dovrebbe succedere se il pulsante è abilitato solo dopo la selezione del piano
            messagebox.showerror(self.lang.get('error_title'), "Errore interno: ID macchina non trovato.", parent=self)
            return

        # Chiama il launcher nel nuovo modulo 'richieste_intervento.py'
        richieste_intervento.open_request_window(
            parent=self,
            db=self.db,
            lang=self.lang,
            user_name=self.user_name,
            equipment_id=equipment_id,
            equipment_name=equipment_name
        )

    def _save_logs(self):
        if not self.completed_tasks:
            messagebox.showwarning(self.lang.get('warning_title'), self.lang.get('warn_no_tasks_completed',
                                                                                 "Nessun compito selezionato come completato."),
                                   parent=self)
            return

        equipment_id = self.equipments_data.get(self.equipment_var.get())
        if not equipment_id or not self.start_time:
            messagebox.showerror(self.lang.get('error_title'),
                                 "Errore interno: Dati macchina o ora di inizio mancanti.", parent=self)
            return

        # Recupera le note dal widget Text
        notes_content = self.notes_text.get("1.0", tk.END).strip()

        # Chiedi conferma
        confirm_msg = self.lang.get('confirm_save_logs_message', "Salvare i log per {0} compiti?").format(
            len(self.completed_tasks))

        if messagebox.askyesno(self.lang.get('confirm_save_title', "Conferma Salvataggio"), confirm_msg, parent=self):

            # Chiama il metodo DB per salvare i log in batch
            success = self.db.log_completed_tasks(
                equipment_id=equipment_id,
                user_name=self.user_name,
                completed_task_ids=list(self.completed_tasks),
                start_time=self.start_time,
                notes=notes_content  # Passaggio delle note
            )

            if success:
                messagebox.showinfo(self.lang.get('success_title'),
                                    self.lang.get('info_logs_saved_success', "Log manutenzione salvati con successo."),
                                    parent=self)
                # Resetta la selezione corrente e aggiorna la lista piani disponibili
                self._on_equipment_select()
            else:
                messagebox.showerror(self.lang.get('error_title'), self.db.last_error_details, parent=self)


# AGGIORNA la funzione launcher in maintenance_gui.py per accettare user_name
# Sostituisci la vecchia definizione di open_fill_templates con questa:
def open_fill_templates(parent, db, lang, user_name=None):
    # Controlla se user_name è stato fornito (dovrebbe esserlo se chiamato tramite login da App)
    if user_name:
        FillTemplateWindow(parent, db, lang, user_name)  # Passa user_name alla classe
    else:
        # Fallback di sicurezza nel caso venga chiamata erroneamente senza utente
        print("Errore: Tentativo di aprire Compilazione Schede senza autenticazione.")


class ReportsWindow(tk.Toplevel):
    """Finestra per la generazione di report."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.title(lang.get('submenu_reports'))
        self.geometry("700x500")
        ttk.Label(self, text="Finestra Generazione Report - In Sviluppo", font=("Helvetica", 16)).pack(pady=50, padx=20)
        self.transient(parent)
        self.grab_set()


# --- Funzioni "Launcher" per aprire le finestre dal menu principale ---

def open_add_machine(parent, db, lang):
    AddMachineWindow(parent, db, lang)


# Modifica questa funzione in maintenance_gui.py

def open_edit_machine(parent, db, lang):
    # L'utente autenticato viene passato qui
    user_name = parent.authenticated_user_for_maintenance # Dovremo aggiungere questa variabile
    SelectMachineToEditWindow(parent, db, lang, user_name)


def open_view_machines(parent, db, lang):
    ViewMachineWindow(parent, db, lang)


def open_maintenance_docs(parent, db, lang):
    MaintenanceDocsWindow(parent, db, lang)


def open_fill_templates(parent, db, lang, user_name=None):
    # Controlla se user_name è stato fornito (dovrebbe esserlo se chiamato tramite login da App)
    if user_name:
        FillTemplateWindow(parent, db, lang, user_name) # Passa user_name alla classe
    else:
        # Fallback di sicurezza nel caso venga chiamata erroneamente senza utente
        print("Errore: Tentativo di aprire Compilazione Schede senza autenticazione.")



def open_reports(parent, db, lang):
    ReportsWindow(parent, db, lang)