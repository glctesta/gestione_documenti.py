import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import collections.abc


class CalibrationsWindow(tk.Toplevel):
    def __init__(self, parent, db_object, language_manager):
        super().__init__(parent)
        self.parent = parent
        self.db = db_object
        self.lang = language_manager

        self.equipment_map = {}
        self.supplier_map = {}
        self.all_supplier_names = []

        self.title(self.lang.get('calibrations_title', "Gestione Calibrazioni"))
        self.geometry("650x550")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_initial_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        select_frame = ttk.LabelFrame(main_frame, text=self.lang.get('select_equipment', "Seleziona Attrezzatura"),
                                      padding="10")
        select_frame.pack(fill=tk.X, expand=True, pady=(0, 10))
        self.combo_equipment = ttk.Combobox(select_frame, state="readonly", font=('Segoe UI', 10))
        self.combo_equipment.pack(fill=tk.X, expand=True)
        self.combo_equipment.bind("<<ComboboxSelected>>", self._on_equipment_select)

        self.details_frame = ttk.LabelFrame(main_frame,
                                            text=self.lang.get('calibration_details', "Dettagli Ultima Calibrazione"),
                                            padding="10")
        ttk.Label(self.details_frame, text=self.lang.get('last_calibration_date', "Data ultima calibrazione:")).grid(
            row=0, column=0, sticky="w", pady=2, padx=5)
        self.lbl_last_date = ttk.Label(self.details_frame, text="N/D", font=('Segoe UI', 10, 'bold'))
        self.lbl_last_date.grid(row=0, column=1, sticky="w", pady=2, padx=5)
        ttk.Label(self.details_frame, text=self.lang.get('expiry_date', "Data di scadenza:")).grid(row=1, column=0,
                                                                                                   sticky="w", pady=2,
                                                                                                   padx=5)
        self.lbl_expiry_date = ttk.Label(self.details_frame, text="N/D", font=('Segoe UI', 10, 'bold'))
        self.lbl_expiry_date.grid(row=1, column=1, sticky="w", pady=2, padx=5)

        self.insert_frame = ttk.LabelFrame(main_frame,
                                           text=self.lang.get('new_calibration_data', "Inserisci Nuova Calibrazione"),
                                           padding="10")
        ttk.Label(self.insert_frame, text=self.lang.get('new_expiry_date', "Nuova data di scadenza:")).grid(row=0,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=5,
                                                                                                            padx=5)
        self.entry_new_expiry_date = DateEntry(self.insert_frame, width=18, background='darkblue', foreground='white',
                                               borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_new_expiry_date.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        ttk.Label(self.insert_frame, text=self.lang.get('certifying_body', "Ente certificatore:")).grid(row=1, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=5, padx=5)
        self.combo_cert_body = ttk.Combobox(self.insert_frame, width=35)
        self.combo_cert_body.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.combo_cert_body.bind('<KeyRelease>', self._on_supplier_search)
        self.combo_cert_body.bind('<<ComboboxSelected>>', lambda e: self.focus())
        ttk.Label(self.insert_frame, text=self.lang.get('certificate_number', "Numero certificato:")).grid(row=2,
                                                                                                           column=0,
                                                                                                           sticky="w",
                                                                                                           pady=5,
                                                                                                           padx=5)
        self.entry_cert_number = ttk.Entry(self.insert_frame, width=38)
        self.entry_cert_number.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.btn_save = ttk.Button(self.insert_frame, text=self.lang.get('save_button', "Salva"),
                                   command=self._save_calibration)
        self.btn_save.grid(row=3, column=1, sticky="e", pady=10, padx=5)

    def _load_initial_data(self):
        self._load_equipment_list()
        self._load_suppliers()

    def _load_equipment_list(self):
        try:
            rows = self.db.get_calibratable_equipment()
            if not rows:
                self.combo_equipment['values'] = [
                    self.lang.get('no_equipment_found', "Nessuna attrezzatura da calibrare trovata.")]
                return
            equipment_display_list = [f"{row.InternalName} (Mat: {row.InventoryNumber}) - {row.Brand}" for row in rows]
            self.equipment_map = {f"{row.InternalName} (Mat: {row.InventoryNumber}) - {row.Brand}": row.EquipmentId for
                                  row in rows}
            self.combo_equipment['values'] = equipment_display_list
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare la lista attrezzature:\n{e}",
                                 parent=self)

    def _load_suppliers(self):
        try:
            rows = self.db.get_suppliers()
            if not rows: return
            self.all_supplier_names = sorted([row.SiteName for row in rows])
            self.supplier_map = {row.SiteName: row.IDSite for row in rows}
            self.combo_cert_body['values'] = self.all_supplier_names
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare la lista fornitori:\n{e}",
                                 parent=self)

    def _on_supplier_search(self, event=None):
        value = self.combo_cert_body.get().lower()
        if value == '':
            self.combo_cert_body['values'] = self.all_supplier_names
        else:
            filtered_data = [name for name in self.all_supplier_names if value in name.lower()]
            self.combo_cert_body['values'] = filtered_data

    def _on_equipment_select(self, event=None):
        selected_display_name = self.combo_equipment.get()
        if not selected_display_name: return
        equipment_id = self.equipment_map.get(selected_display_name)
        if equipment_id:
            self._load_calibration_data(equipment_id)

    # --- FUNZIONE MODIFICATA ---
    def _load_calibration_data(self, equipment_id):
        """Carica e visualizza i dati dell'ultima calibrazione per l'attrezzatura selezionata."""
        try:
            # MODIFICA: Nasconde entrambi i frame per iniziare da una situazione pulita
            self.insert_frame.pack_forget()
            self.details_frame.pack_forget()

            row = self.db.get_last_calibration(equipment_id)

            # Popola le etichette con i dati
            if row:
                self.lbl_last_date.config(text=str(row.CalibratedOn) if row.CalibratedOn else "N/D")
                self.lbl_expiry_date.config(text=str(row.ExpireOn) if row.ExpireOn else "NESSUNA")
            else:
                self.lbl_last_date.config(text="Nessuna calibrazione registrata")
                self.lbl_expiry_date.config(text="N/D")

            # --- NUOVA LOGICA DI VISUALIZZAZIONE ---
            # 1. Mostra SEMPRE il frame dei dettagli dopo una selezione
            self.details_frame.pack(fill=tk.X, expand=True, pady=10)

            # 2. Mostra il frame di inserimento SOLO se non c'è una riga
            #    o se la data di scadenza è assente (None)
            show_insert_frame = (not row) or (row and row.ExpireOn is None)
            if show_insert_frame:
                self.insert_frame.pack(fill=tk.X, expand=True, pady=10)

        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare i dati di calibrazione:\n{e}",
                                 parent=self)

    def _save_calibration(self):
        selected_equipment_name = self.combo_equipment.get()
        equipment_id = self.equipment_map.get(selected_equipment_name)
        selected_supplier_name = self.combo_cert_body.get().strip()
        supplier_id = self.supplier_map.get(selected_supplier_name)
        new_expiry_date = self.entry_new_expiry_date.get_date().strftime('%Y-%m-%d')
        cert_number = self.entry_cert_number.get().strip()

        if not supplier_id:
            messagebox.showwarning(self.lang.get('missing_data', "Dati Mancanti"), self.lang.get('supplier_not_valid',
                                                                                                 "Selezionare un ente certificatore valido dalla lista."),
                                   parent=self)
            return

        try:
            self.db.add_new_calibration(equipment_id, new_expiry_date, supplier_id, cert_number)
            messagebox.showinfo(self.lang.get('success', "Successo"),
                                self.lang.get('save_success_message', "Dati di calibrazione salvati correttamente."),
                                parent=self)
            self.combo_cert_body.set('')
            self.entry_cert_number.delete(0, tk.END)
            self._load_calibration_data(equipment_id)
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore di Salvataggio"), f"Impossibile salvare i dati:\n{e}",
                                 parent=self)

