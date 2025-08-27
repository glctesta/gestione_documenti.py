# richieste_intervento.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import simpledialog
from datetime import datetime
# Importa il nuovo file utils.py
import utils
import tempfile
import os
import sys
import subprocess

# In richieste_intervento.py

# In richieste_intervento.py

# In richieste_intervento.py

class AddNewSparePartWindow(tk.Toplevel):
    """Finestra per aggiungere un nuovo materiale di ricambio al catalogo."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.new_part_id = None

        # Usa il gestore della lingua per il titolo
        self.title(self.lang.get('add_new_material_title', "Aggiungi Nuovo Materiale"))
        self.geometry("500x300")
        self.transient(parent)
        self.grab_set()

        self.part_number_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        # Usa il gestore della lingua per tutte le etichette
        ttk.Label(frame, text=self.lang.get('material_part_number_label', "Codice Materiale (*):")).grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky=tk.W,
                                                                                                         pady=5)
        self.part_number_entry = ttk.Entry(frame, textvariable=self.part_number_var)
        self.part_number_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('material_code_label', "Nome Materiale:")).grid(row=1, column=0,
                                                                                            sticky=tk.W, pady=5)
        self.code_entry = ttk.Entry(frame, textvariable=self.code_var)
        self.code_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text=self.lang.get('material_description_label', "Descrizione:")).grid(row=2, column=0,
                                                                                                sticky=tk.NW, pady=5)
        self.description_text = tk.Text(frame, height=5, wrap=tk.WORD)
        self.description_text.grid(row=2, column=1, sticky=tk.EW, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=1, sticky=tk.E, pady=(20, 0))

        # Usa il gestore della lingua per i pulsanti
        ttk.Button(button_frame, text=self.lang.get('save_button', "Salva"), command=self._save_new_part).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', "Annulla"), command=self.destroy).pack(
            side=tk.LEFT)

        self.part_number_entry.focus_set()

    def _save_new_part(self):
        # ... (questo metodo rimane invariato)
        part_number = self.part_number_var.get().strip()
        code = self.code_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()

        if not part_number:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('error_part_number_required', "Il Codice Materiale è obbligatorio."),
                                 parent=self)
            return

        new_id = self.db.add_new_spare_part(part_number, code, description)

        if new_id:
            messagebox.showinfo(self.lang.get('success_title', "Successo"),
                                self.lang.get('info_new_part_saved', "Nuovo materiale salvato con successo."),
                                parent=self)
            self.new_part_id = new_id
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('error_saving_part',
                                               "Impossibile salvare il nuovo materiale.") + f"\n\n{self.db.last_error_details}",
                                 parent=self)

# In richiese_intervento.py

# In richieste_intervento.py

# In richieste_intervento.py

class RequestWindow(tk.Toplevel):
    """Finestra per richiedere parti di ricambio o interventi."""

    def __init__(self, parent, db, lang, user_name, equipment_id, equipment_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name

        self.spare_parts_data = {}
        self.all_spare_parts_names = []
        self.spare_part_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")

        self.title(self.lang.get('request_window_title', "Crea Richiesta Parti/Intervento"))
        self.geometry("650x450")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_spare_parts()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        ttk.Label(main_frame,
                  text=f"{self.lang.get('request_for_machine', 'Richiesta per la macchina:')} {self.equipment_name}",
                  font=("Helvetica", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        ttk.Label(main_frame, text=self.lang.get('spare_part_label', "Parte di Ricambio:")).grid(row=1, column=0,
                                                                                                 sticky=tk.W, padx=5,
                                                                                                 pady=5)

        part_frame = ttk.Frame(main_frame)
        part_frame.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)
        part_frame.columnconfigure(0, weight=1)

        self.spare_parts_combo = ttk.Combobox(part_frame, textvariable=self.spare_part_var, state='normal', height=10)
        self.spare_parts_combo.grid(row=0, column=0, sticky="ew")
        self.spare_parts_combo.bind('<KeyRelease>', self._filter_spare_parts_combo)
        self.spare_parts_combo.bind("<<ComboboxSelected>>", self._on_part_selected)

        new_part_button = ttk.Button(part_frame, text=self.lang.get('new_material_button', "Nuovo..."),
                                     command=self._open_add_new_part_window)
        new_part_button.grid(row=0, column=1, padx=5)

        self.view_doc_button = ttk.Button(part_frame, text="Visualizza Doc.", command=self._open_material_document,
                                          state="disabled")
        self.view_doc_button.grid(row=0, column=2, padx=5)

        ttk.Label(main_frame, text=self.lang.get('quantity_label', "Quantità:")).grid(row=2, column=0, sticky=tk.W,
                                                                                      padx=5, pady=5)
        self.quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text=self.lang.get('notes_label', "Note:")).grid(row=3, column=0, sticky=tk.NW, padx=5,
                                                                               pady=5)
        notes_frame = ttk.Frame(main_frame)
        notes_frame.grid(row=3, column=1, columnspan=2, sticky="nsew", pady=5)
        notes_frame.rowconfigure(0, weight=1)
        notes_frame.columnconfigure(0, weight=1)
        self.notes_text = tk.Text(notes_frame, height=6, wrap=tk.WORD)
        self.notes_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.notes_text.config(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, sticky=tk.E, pady=(15, 0))
        self.save_button = ttk.Button(button_frame, text=self.lang.get('save_request_button', "Invia Richiesta"),
                                      command=self._save_request)
        self.save_button.pack()

    def _load_spare_parts(self, select_id=None):
        self.spare_parts_data = {}
        self.all_spare_parts_names = []
        spare_parts = self.db.fetch_spare_parts()

        print(f"DEBUG: Trovati {len(spare_parts)} materiali di ricambio nel database.")

        if not spare_parts:
            self.spare_parts_combo['values'] = []
            return

        value_to_select = ""
        for part in spare_parts:
            part_number = part.MaterialPartNumber or "N/A"
            part_code = part.MaterialCode or ""
            display_text = f"{part_number} - {part_code}"
            self.spare_parts_data[display_text] = part.SparePartMaterialId
            self.all_spare_parts_names.append(display_text)
            if select_id and part.SparePartMaterialId == select_id:
                value_to_select = display_text

        self.spare_parts_combo['values'] = sorted(self.all_spare_parts_names)
        if value_to_select:
            self.spare_part_var.set(value_to_select)
            self._on_part_selected()

    def _filter_spare_parts_combo(self, event):
        typed_text = self.spare_part_var.get().lower()
        if not typed_text:
            self.spare_parts_combo['values'] = sorted(self.all_spare_parts_names)
        else:
            filtered_list = [name for name in self.all_spare_parts_names if typed_text in name.lower()]
            self.spare_parts_combo['values'] = filtered_list
        self.view_doc_button.config(state="disabled")

    def _on_part_selected(self, event=None):
        material_name = self.spare_part_var.get()
        material_id = self.spare_parts_data.get(material_name)
        if not material_id:
            self.view_doc_button.config(state="disabled")
            return
        doc_data = self.db.fetch_material_document(material_id)
        if doc_data and doc_data.CatalogDetail:
            self.view_doc_button.config(state="normal")
        else:
            self.view_doc_button.config(state="disabled")

    def _open_material_document(self):
        material_name = self.spare_part_var.get()
        material_id = self.spare_parts_data.get(material_name)
        if not material_id: return
        doc_row = self.db.fetch_material_document(material_id)
        if not doc_row or not doc_row.CatalogDetail:
            messagebox.showwarning("Nessun Documento", "Nessun documento trovato per questo materiale.", parent=self)
            return
        binary_data = doc_row.CatalogDetail
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, prefix="material_doc_", suffix=".pdf")
            temp_file.write(binary_data)
            temp_file.close()
            if sys.platform == "win32":
                os.startfile(temp_file.name)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, temp_file.name])
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il documento: {e}", parent=self)

    def _open_add_new_part_window(self):
        add_window = AddNewSparePartWindow(self, self.db, self.lang)
        self.wait_window(add_window)
        newly_created_id = add_window.new_part_id
        if newly_created_id:
            self._load_spare_parts(select_id=newly_created_id)

    def _save_request(self):
        """Valida i dati del form e li salva nel database."""
        part_selection = self.spare_part_var.get()
        quantity_str = self.quantity_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not part_selection or part_selection not in self.spare_parts_data:
            messagebox.showwarning(self.lang.get('warning_title', "Attenzione"), self.lang.get('warning_select_part',
                                                                                               "Selezionare una parte di ricambio valida dalla lista."),
                                   parent=self)
            return
        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning(self.lang.get('warning_title', "Attenzione"),
                                   self.lang.get('warning_invalid_quantity',
                                                 "La quantità deve essere un numero intero positivo."), parent=self)
            return
        spare_part_id = self.spare_parts_data.get(part_selection)
        success = self.db.insert_spare_part_request(
            equipment_id=self.equipment_id,
            spare_part_id=spare_part_id,
            quantity=quantity,
            notes=notes,
            requested_by=self.user_name
        )
        if success:
            messagebox.showinfo(self.lang.get('success_title', "Successo"),
                                self.lang.get('info_request_sent', "Richiesta inviata con successo."), parent=self)
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 f"{self.lang.get('error_sending_request', 'Impossibile inviare la richiesta.')}\n\n{self.db.last_error_details}",
                                 parent=self)


# Funzione Launcher (Invariata)
def open_request_window(parent, db, lang, user_name, equipment_id, equipment_name):
    RequestWindow(parent, db, lang, user_name, equipment_id, equipment_name)