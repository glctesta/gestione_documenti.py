# maintenance_gui.py
# Da aggiungere in cima a maintenance_gui.py
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import tkinter as tk
from tkinter import ttk, messagebox


# --- Finestre Segnaposto per la Gestione Macchine ---

# Da sostituire/incollare in maintenance_gui.py

# Sostituisci questa classe in maintenance_gui.py

# Sostituisci questa classe in maintenance_gui.py

# Sostituisci questa classe in maintenance_gui.py

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


class ViewMachineWindow(tk.Toplevel):
    """Finestra per visualizzare le macchine (precedentemente MachineManagementWindow)."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.title(lang.get('submenu_view_machines'))
        self.geometry("600x400")
        ttk.Label(self, text="Finestra Visualizza Macchine - In Sviluppo", font=("Helvetica", 16)).pack(pady=50,
                                                                                                        padx=20)
        self.transient(parent)
        self.grab_set()


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
    """Finestra per la compilazione dei template di manutenzione."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.title(lang.get('submenu_fill_templates'))
        self.geometry("800x600")
        ttk.Label(self, text="Finestra Compilazione Manutenzione - In Sviluppo", font=("Helvetica", 16)).pack(pady=50,
                                                                                                              padx=20)
        self.transient(parent)
        self.grab_set()


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


def open_fill_templates(parent, db, lang):
    FillTemplateWindow(parent, db, lang)


def open_reports(parent, db, lang):
    ReportsWindow(parent, db, lang)