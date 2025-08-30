# maintenance_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import openpyxl
from tkcalendar import DateEntry
from datetime import datetime, date
from collections import Counter
import tempfile
import os
import sys
import subprocess
import io
import richieste_intervento

# Import per le immagini
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import per i grafici
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import per il PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Image as ReportLabImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ManageMaterialsWindow(tk.Toplevel):
    """Finestra per la gestione completa dei materiali e dei loro collegamenti alle macchine."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('manage_materials_title', "Gestione Materiali di Ricambio"))
        self.geometry("1000x600")

        self.current_material_id = None
        self.all_equipment = []
        self.catalog_binary_data = None
        self.catalog_file_name = None

        self.part_number_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.catalog_name_var = tk.StringVar()
        self.search_code_var = tk.StringVar()
        self.search_desc_var = tk.StringVar()
        self.material_count_var = tk.StringVar()

        self._create_widgets()
        self._load_all_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)

        # --- Pannello Sinistro: Lista e Filtri ---
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('materials_list_label', "Materiali"))
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)

        filter_area = ttk.Frame(list_frame, padding=5)
        filter_area.grid(row=0, column=0, sticky="ew")
        filter_area.columnconfigure(1, weight=1)

        ttk.Label(filter_area, text=self.lang.get('code_name_filter_label', "Codice/Nome:")).grid(row=0, column=0,
                                                                                                  padx=(0, 5))
        search_code_entry = ttk.Entry(filter_area, textvariable=self.search_code_var)
        search_code_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(filter_area, text=self.lang.get('description_filter_label', "Descrizione:")).grid(row=1, column=0,
                                                                                                    padx=(0, 5))
        search_desc_entry = ttk.Entry(filter_area, textvariable=self.search_desc_var)
        search_desc_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))

        search_button = ttk.Button(filter_area, text=self.lang.get('search_button', "Cerca"),
                                   command=self._load_materials)
        search_button.grid(row=0, column=2, rowspan=2, padx=5)

        # --- NUOVO: Associa il tasto Invio alla ricerca ---
        search_code_entry.bind('<Return>', lambda e: self._load_materials())
        search_desc_entry.bind('<Return>', lambda e: self._load_materials())

        cols = ('part_number', 'code')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('part_number', text=self.lang.get('header_part_number', "Codice Articolo"))
        self.tree.heading('code', text=self.lang.get('header_material_name', "Nome Materiale"))
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_material_select)

        count_label = ttk.Label(list_frame, textvariable=self.material_count_var, anchor="e")
        count_label.grid(row=2, column=0, sticky="ew", padx=5)

        # --- Pannello Destro: Form Unica (RIPRISTINATO) ---
        form_frame = ttk.LabelFrame(main_frame,
                                    text=self.lang.get('details_and_links_label', "Dettagli e Collegamenti"))
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(4, weight=1)

        ttk.Label(form_frame, text=self.lang.get('part_number_label', "Codice Articolo (*):")).grid(row=0, column=0,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=3)
        self.part_number_entry = ttk.Entry(form_frame, textvariable=self.part_number_var)
        self.part_number_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        self.part_number_entry.bind('<FocusOut>', self._validate_part_number)
        self.validation_label = ttk.Label(form_frame, text="", foreground="red", font=("Helvetica", 8))
        self.validation_label.grid(row=0, column=2, sticky="w", padx=5)

        ttk.Label(form_frame, text=self.lang.get('material_name_label', "Nome Materiale:")).grid(row=1, column=0,
                                                                                                 sticky="w", padx=5,
                                                                                                 pady=3)
        ttk.Entry(form_frame, textvariable=self.code_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=5,
                                                               pady=3)

        ttk.Label(form_frame, text=self.lang.get('description_label_generic', "Descrizione:")).grid(row=2, column=0,
                                                                                                    sticky="nw", padx=5,
                                                                                                    pady=3)
        self.desc_text = tk.Text(form_frame, height=4, wrap=tk.WORD)
        self.desc_text.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=3)

        ttk.Label(form_frame, text=self.lang.get('catalog_doc_label', "Documento Catalogo:")).grid(row=3, column=0,
                                                                                                   sticky="w", padx=5,
                                                                                                   pady=5)
        doc_frame = ttk.Frame(form_frame)
        doc_frame.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5)
        ttk.Button(doc_frame, text=self.lang.get('attach_button', "Allega..."), command=self._attach_file).pack(
            side="left")
        ttk.Label(doc_frame, textvariable=self.catalog_name_var).pack(side="left", padx=5)

        link_frame = ttk.LabelFrame(form_frame, text=self.lang.get('linked_equipment_label', "Macchinari Collegati"))
        link_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=10)
        link_frame.rowconfigure(0, weight=1)
        link_frame.columnconfigure(0, weight=1)
        self.equipment_listbox = tk.Listbox(link_frame, selectmode="extended")
        self.equipment_listbox.grid(row=0, column=0, sticky="nsew")

        # Pulsanti Azione
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(5, 10), anchor="e")
        ttk.Button(btn_frame, text=self.lang.get('new_button', "Nuovo"), command=self._clear_form).pack(side="right",
                                                                                                        padx=5)
        ttk.Button(btn_frame, text=self.lang.get('save_button', "Salva"), command=self._save).pack(side="right", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('delete_button', "Cancella"), command=self._delete).pack(side="right")

    def _load_all_data(self):
        """Carica tutti i dati necessari all'avvio della finestra."""
        self._load_materials()
        self._load_equipment_listbox()

    def _load_materials(self):
        """Carica i materiali nella lista usando i filtri."""
        self.tree.delete(*self.tree.get_children())

        # Legge i valori dai campi di ricerca
        code_filter = self.search_code_var.get()
        desc_filter = self.search_desc_var.get()

        # Chiama il nuovo metodo del database con i filtri
        self.materials_list = self.db.search_materials(code_filter, desc_filter)

        for mat in self.materials_list:
            self.tree.insert("", "end", iid=mat.SparePartMaterialId, values=(mat.MaterialPartNumber, mat.MaterialCode))
        total_count = len(self.materials_list)
        count_text = f"Totale Materiali: {total_count}"
        self.material_count_var.set(count_text)


    def _load_equipment_listbox(self):
        # ... (Questo metodo rimane invariato)
        self.equipment_listbox.delete(0, tk.END)
        all_equipment_raw = self.db.fetch_all_equipments()
        self.all_equipment = [(eq.EquipmentId, f"{eq.InternalName or ''} [{eq.SerialNumber}]") for eq in
                              all_equipment_raw]
        for _, name in self.all_equipment:
            self.equipment_listbox.insert(tk.END, name)

    def _validate_part_number(self, event=None):
        """Controlla se il Codice Articolo inserito esiste già nel database."""
        # Esegui il controllo solo se stiamo creando un NUOVO materiale
        if self.current_material_id is not None:
            self.validation_label.config(text="")  # Pulisce il messaggio se siamo in modifica
            return

        part_number = self.part_number_var.get().strip()
        if not part_number:
            self.validation_label.config(text="")  # Pulisce se il campo è vuoto
            return

        # Chiama il nuovo metodo del DB
        is_duplicate = self.db.check_if_material_exists(part_number)

        if is_duplicate:
            self.validation_label.config(text="Codice già esistente!")
        else:
            self.validation_label.config(text="")

    def _on_material_select(self, event=None):
        self.validation_label.config(text="")
        selected_item = self.tree.focus()
        if not selected_item: return
        self.current_material_id = int(selected_item)

        mat_data = self.db.fetch_single_material(self.current_material_id)
        if not mat_data: return

        self.part_number_var.set(mat_data.MaterialPartNumber or "")
        self.code_var.set(mat_data.MaterialCode or "")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", mat_data.MaterialDescription or "")

        self.catalog_binary_data = mat_data.CatalogDetail

        # --- CORREZIONE QUI ---
        # Non chiamiamo più una funzione inesistente. Mostriamo un testo generico.
        doc_display_name = "Documento presente" if self.catalog_binary_data else "Nessun documento"
        self.catalog_name_var.set(doc_display_name)

        # Seleziona le macchine collegate nella listbox
        self.equipment_listbox.selection_clear(0, tk.END)
        linked_ids = self.db.fetch_linked_equipment(self.current_material_id)
        for i, (eq_id, _) in enumerate(self.all_equipment):
            if eq_id in linked_ids:
                self.equipment_listbox.selection_set(i)

    def _clear_form(self):
        self.validation_label.config(text="")
        self.tree.selection_set([])
        self.current_material_id = None
        self.part_number_var.set("")
        self.code_var.set("")
        self.desc_text.delete("1.0", tk.END)
        self.catalog_binary_data = None
        self.catalog_file_name = ""
        self.catalog_name_var.set("")
        self.equipment_listbox.selection_clear(0, tk.END)
        self.part_number_entry.focus_set()

    def _attach_file(self):
        path = filedialog.askopenfilename(parent=self)
        if not path: return
        self.catalog_file_name = os.path.basename(path)
        self.catalog_name_var.set(self.catalog_file_name)
        with open(path, 'rb') as f:
            self.catalog_binary_data = f.read()

    def _save(self):
        part_number = self.part_number_var.get().strip().replace(',', ' ')
        code = self.code_var.get().strip().replace(',', ' ')
        desc = self.desc_text.get("1.0", tk.END).strip().replace(',', ' ')

        if not part_number:
            messagebox.showerror("Dati Mancanti", "Il Codice Articolo è obbligatorio.", parent=self)
            return

        selected_indices = self.equipment_listbox.curselection()
        selected_equipment_ids = [self.all_equipment[i][0] for i in selected_indices]

        doc_name_to_save = self.catalog_file_name if self.catalog_binary_data else None

        if self.current_material_id:  # UPDATE
            success, msg_or_id = self.db.update_material(
                self.current_material_id, part_number, code, desc,
                self.catalog_binary_data, doc_name_to_save, self.user_name
            )
            if success:
                self.db.update_material_links(self.current_material_id, selected_equipment_ids, self.user_name)
        else:  # INSERT
            success, msg_or_id = self.db.add_material(
                part_number, code, desc, self.catalog_binary_data, doc_name_to_save, self.user_name
            )
            if success:
                new_id = msg_or_id
                self.db.update_material_links(new_id, selected_equipment_ids, self.user_name)

        if success:
            messagebox.showinfo("Successo", "Dati salvati con successo.", parent=self)
            self._load_all_data()
            self._clear_form()
        else:
            # Se il messaggio è una chiave di traduzione, la traduciamo
            if msg_or_id == "error_duplicate_material":
                error_message = self.lang.get(msg_or_id, "Errore: duplicato.")
            else:
                error_message = f"Salvataggio fallito: {msg_or_id}"
            messagebox.showerror("Errore", error_message, parent=self)

    def _delete(self):
        if not self.current_material_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare un materiale da cancellare.")
            return
        if messagebox.askyesno("Conferma Cancellazione",
                               "Sei sicuro di voler cancellare questo materiale e tutti i suoi collegamenti?"):
            success, msg = self.db.delete_material(self.current_material_id)
            if success:
                messagebox.showinfo("Successo", msg, parent=self)
                self._load_all_data()
                self._clear_form()
            else:
                messagebox.showerror("Errore", msg, parent=self)


class ViewMaterialsWindow(tk.Toplevel):
    """Finestra per la visualizzazione e l'esportazione dei materiali per macchina."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('view_materials_title', "Visualizza Materiali per Macchinario"))
        self.geometry("800x500")

        self.equipments_data = {}
        self.equipment_var = tk.StringVar()
        self.materials_in_view = []

        self._create_widgets()
        self._load_equipments()

    # In materials_gui.py, dentro la classe ViewMaterialsWindow

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(filter_frame, text=self.lang.get('select_equipment_label', "Seleziona Macchinario:")).grid(row=0,
                                                                                                             column=0)
        self.equipment_combo = ttk.Combobox(filter_frame, textvariable=self.equipment_var, state="readonly")
        self.equipment_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.equipment_combo.bind("<<ComboboxSelected>>", self._load_materials_for_equipment)

        cols = ('part_number', 'code', 'desc')
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading('part_number', text=self.lang.get('header_part_number', "Codice Articolo"))
        self.tree.heading('code', text=self.lang.get('header_material_name', "Nome Materiale"))
        self.tree.heading('desc', text=self.lang.get('description_label_generic', "Descrizione"))
        self.tree.grid(row=1, column=0, sticky="nsew")

        ttk.Button(main_frame, text=self.lang.get('export_excel_button', "Esporta in Excel"),
                   command=self._export_to_excel).grid(row=2, column=0, sticky="e", pady=10)

    def _load_equipments(self):
        equipments = self.db.fetch_all_equipments()
        if equipments:
            self.equipments_data = {f"{r.InternalName or ''} [{r.SerialNumber}]": r.EquipmentId for r in equipments}
            self.equipment_combo['values'] = sorted(list(self.equipments_data.keys()))

    def _load_materials_for_equipment(self, event=None):
        self.tree.delete(*self.tree.get_children())
        equipment_id = self.equipments_data.get(self.equipment_var.get())
        if not equipment_id: return

        self.materials_in_view = self.db.fetch_materials_for_equipment(equipment_id)
        for mat in self.materials_in_view:
            self.tree.insert("", "end", values=(mat.MaterialPartNumber, mat.MaterialCode, mat.MaterialDescription))

    def _export_to_excel(self):
        if not self.materials_in_view:
            messagebox.showwarning("Nessun Dato", "Nessun materiale da esportare per la macchina selezionata.")
            return

        temp_dir = "C:\\temp"
        try:
            os.makedirs(temp_dir, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Errore Directory", f"Impossibile creare la directory {temp_dir}:\n{e}")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        machine_name = self.equipment_var.get().replace(" ", "_").replace("[", "").replace("]", "")
        file_path = os.path.join(temp_dir, f"materiali_{machine_name}_{timestamp}.xlsx")

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Materiali"

            headers = ["Codice Articolo", "Nome Materiale", "Descrizione"]
            sheet.append(headers)

            for mat in self.materials_in_view:
                sheet.append([mat.MaterialPartNumber, mat.MaterialCode, mat.MaterialDescription])

            workbook.save(file_path)
            messagebox.showinfo("Successo", f"File Excel salvato con successo in:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Errore Esportazione", f"Impossibile generare il file Excel:\n{e}")


def open_manage_materials(parent, db, lang, user_name):
    ManageMaterialsWindow(parent, db, lang, user_name)


def open_view_materials(parent, db, lang, user_name):
    ViewMaterialsWindow(parent, db, lang, user_name)