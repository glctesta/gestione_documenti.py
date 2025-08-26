# materials_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import openpyxl
from datetime import datetime
import io

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ManageMaterialsWindow(tk.Toplevel):
    """Finestra per la gestione completa dei materiali e dei loro collegamenti."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('manage_materials_title', "Gestione Materiali di Ricambio"))
        self.geometry("1000x600")

        self.current_material_id = None
        self.all_equipment = []  # Lista di tuple (id, nome)
        self.catalog_binary_data = None
        self.catalog_file_name = None

        self._create_widgets()
        self._load_all_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)

        # Pannello Sinistro: Lista Materiali
        list_frame = ttk.LabelFrame(main_frame, text="Materiali")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ('part_number', 'code')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('part_number', text="Codice Articolo")
        self.tree.heading('code', text="Nome Materiale")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_material_select)

        # Pannello Destro: Dettagli e Collegamenti
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.rowconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Dettagli
        details_frame = ttk.Frame(notebook, padding="10")
        notebook.add(details_frame, text="Dettagli Materiale")
        details_frame.columnconfigure(1, weight=1)

        self.part_number_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.catalog_name_var = tk.StringVar()

        ttk.Label(details_frame, text="Codice Articolo (*):").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.part_number_entry = ttk.Entry(details_frame, textvariable=self.part_number_var)
        self.part_number_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(details_frame, text="Nome Materiale:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(details_frame, textvariable=self.code_var).grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(details_frame, text="Descrizione:").grid(row=2, column=0, sticky="nw", padx=5, pady=3)
        self.desc_text = tk.Text(details_frame, height=5, wrap=tk.WORD)
        self.desc_text.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(details_frame, text="Documento Catalogo:").grid(row=3, column=0, sticky="w", padx=5, pady=10)
        ttk.Button(details_frame, text="Allega/Sostituisci...", command=self._attach_file).grid(row=3, column=1,
                                                                                                sticky="w", padx=5)
        ttk.Label(details_frame, textvariable=self.catalog_name_var).grid(row=4, column=1, sticky="w", padx=5)

        # Tab 2: Macchinari
        links_frame = ttk.Frame(notebook, padding="10")
        notebook.add(links_frame, text="Macchinari Collegati")
        links_frame.rowconfigure(0, weight=1)
        links_frame.columnconfigure(0, weight=1)

        self.equipment_listbox = tk.Listbox(links_frame, selectmode="extended")
        self.equipment_listbox.grid(row=0, column=0, sticky="nsew")

        # Pulsanti Azione
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(5, 10), anchor="e")
        ttk.Button(btn_frame, text="Nuovo", command=self._clear_form).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Salva", command=self._save).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancella", command=self._delete).pack(side="right")

    def _load_all_data(self):
        """Carica tutti i dati necessari all'avvio della finestra."""
        # Carica tutti i materiali per la lista a sinistra
        self.tree.delete(*self.tree.get_children())
        self.materials_list = self.db.fetch_all_materials()
        for mat in self.materials_list:
            self.tree.insert("", "end", iid=mat.SparePartMaterialId, values=(mat.MaterialPartNumber, mat.MaterialCode))

        # Carica tutte le macchine per la lista di selezione
        self.equipment_listbox.delete(0, tk.END)
        all_equipment_raw = self.db.fetch_all_equipments()
        self.all_equipment = [(eq.EquipmentId, f"{eq.InternalName or ''} [{eq.SerialNumber}]") for eq in
                              all_equipment_raw]
        for _, name in self.all_equipment:
            self.equipment_listbox.insert(tk.END, name)

    def _on_material_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item: return
        self.current_material_id = int(selected_item)

        # Carica dettagli del materiale selezionato
        mat_data = self.db.fetch_single_material(self.current_material_id)
        if not mat_data: return

        self.part_number_var.set(mat_data.MaterialPartNumber or "")
        self.code_var.set(mat_data.MaterialCode or "")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", mat_data.MaterialDescription or "")

        self.catalog_binary_data = mat_data.CatalogDetail
        self.catalog_file_name = "Documento presente" if self.catalog_binary_data else "Nessun documento"
        self.catalog_name_var.set(self.catalog_file_name)

        # Seleziona le macchine collegate nella listbox
        self.equipment_listbox.selection_clear(0, tk.END)
        linked_ids = self.db.fetch_linked_equipment(self.current_material_id)
        for i, (eq_id, _) in enumerate(self.all_equipment):
            if eq_id in linked_ids:
                self.equipment_listbox.selection_set(i)

    def _clear_form(self):
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

        code = self.code_var.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()

        # Recupera gli ID delle macchine selezionate
        selected_indices = self.equipment_listbox.curselection()
        selected_equipment_ids = [self.all_equipment[i][0] for i in selected_indices]

        if self.current_material_id:  # UPDATE
            success, msg = self.db.update_material(self.current_material_id, part_number, code, desc,
                                                   self.catalog_binary_data)
            if success:
                self.db.update_material_links(self.current_material_id, selected_equipment_ids)
        else:  # INSERT
            success, new_id = self.db.add_material(part_number, code, desc, self.catalog_binary_data)
            if success:
                self.db.update_material_links(new_id, selected_equipment_ids)

        if success:
            messagebox.showinfo("Successo", "Dati salvati con successo.", parent=self)
            self._load_all_data()
            self._clear_form()
        else:
            messagebox.showerror("Errore", "Salvataggio fallito.", parent=self)

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

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(filter_frame, text="Seleziona Macchinario:").grid(row=0, column=0)
        self.equipment_combo = ttk.Combobox(filter_frame, textvariable=self.equipment_var, state="readonly")
        self.equipment_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.equipment_combo.bind("<<ComboboxSelected>>", self._load_materials_for_equipment)

        cols = ('part_number', 'code', 'desc')
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading('part_number', text="Codice Articolo")
        self.tree.heading('code', text="Nome Materiale")
        self.tree.heading('desc', text="Descrizione")
        self.tree.grid(row=1, column=0, sticky="nsew")

        ttk.Button(main_frame, text="Esporta in Excel", command=self._export_to_excel).grid(row=2, column=0, sticky="e",
                                                                                            pady=10)

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


# Funzioni Launcher
def open_manage_materials(parent, db, lang, user_name):
    ManageMaterialsWindow(parent, db, lang, user_name)


def open_view_materials(parent, db, lang, user_name):
    ViewMaterialsWindow(parent, db, lang, user_name)