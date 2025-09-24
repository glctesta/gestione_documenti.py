# richieste_intervento.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import simpledialog
from datetime import datetime

import logger

# Importa il nuovo file utils.py
import utils
import logging
import tempfile
import os
import sys
import subprocess
import utils
class RequestWindow(tk.Toplevel):
    logging.basicConfig(
        filename='ManageDocs.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)

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

        # new_part_button = ttk.Button(part_frame, text=self.lang.get('new_material_button', "Nuovo..."),
        #                              command=self._open_add_new_part_window)
        # new_part_button.grid(row=0, column=1, padx=5)

        self.view_doc_button = ttk.Button(part_frame, text="Visualizza Doc.", command=self._open_material_document,
                                          state="disabled")
        self.view_doc_button.grid(row=0, column=1, padx=5)

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

    def _save_request(self):
        """Valida i dati del form e li salva nel database, poi invia una email di notifica."""
        part_selection = self.spare_part_var.get()
        quantity_str = self.quantity_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Validazione della selezione parte
        if not part_selection or part_selection not in self.spare_parts_data:
            messagebox.showwarning(
                self.lang.get('warning_title', "Attenzione"),
                self.lang.get('warning_select_part', "Selezionare una parte di ricambio valida dalla lista."),
                parent=self
            )
            return

        # Validazione della quantità
        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning_title', "Attenzione"),
                self.lang.get('warning_invalid_quantity', "La quantità deve essere un numero intero positivo."),
                parent=self
            )
            return

        spare_part_id = self.spare_parts_data.get(part_selection)

        # Salvataggio nel database
        success = self.db.insert_spare_part_request(
            equipment_id=self.equipment_id,
            spare_part_id=spare_part_id,
            quantity=quantity,
            notes=notes,
            requested_by=self.user_name
        )

        if success:
            try:
                # Recupera i dettagli del macchinario dal database
                equipment_query = """
                            SELECT eb.Brand + ' ' + 
                            [InternalName] + '(' + [SerialNumber] + ')' as InternalName,[InventoryNumber] as SerialNumber
                            FROM [Traceability_RS].[eqp].[Equipments] e inner join [eqp].[EquipmentBrands] eb on e.BrandId=eb.EquipmentBrandId 
                            where e.equipmentid= ?
                        """
                with self.db.conn.cursor() as cursor:
                    cursor.execute(equipment_query, (self.equipment_id,))
                    equipment_row = cursor.fetchone()

                # Formatta il nome del macchinario
                if equipment_row and (equipment_row.InternalName or equipment_row.SerialNumber):
                    equipment_name = f"{equipment_row.InternalName or ''} [{equipment_row.SerialNumber}]".strip()
                else:
                    equipment_name = f"ID: {self.equipment_id}"

                # Preparazione del contenuto dell'email
                subject = f"Richiesta ricambi - {equipment_name}"

                # Creazione del corpo dell'email
                body = f"""
    Nuova richiesta ricambi:

    Richiedente: {self.user_name}
    Macchinario: {equipment_name}
    Parte richiesta: {part_selection}
    Quantità: {quantity}
    Note: {notes}

    Questa è una email automatica, si prega di non rispondere.
    """
                # Recupero dei destinatari dal database
                recipients = utils.get_email_recipients(self.db.conn)

                # Invio dell'email
                utils.send_email(
                    recipients=recipients,
                    subject=subject,
                    body=body
                )

                messagebox.showinfo(
                    self.lang.get('success_title', "Successo"),
                    self.lang.get('info_request_sent', "Richiesta inviata con successo."),
                    parent=self
                )
                self.destroy()

            except Exception as e:
                logging.error(f"Errore nell'invio dell'email: {str(e)}")
                messagebox.showwarning(
                    self.lang.get('warning_title', "Attenzione"),
                    self.lang.get('warning_email_failed',
                                  "La richiesta è stata salvata ma l'invio dell'email è fallito."),
                    parent=self
                )
                self.destroy()
        else:
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                f"{self.lang.get('error_sending_request', 'Impossibile inviare la richiesta.')}\n\n{self.db.last_error_details}",
                parent=self
            )


def open_request_window(parent, db, lang, user_name, equipment_id, equipment_name):
    RequestWindow(parent, db, lang, user_name, equipment_id, equipment_name)