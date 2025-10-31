# tools_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import io
import os

from pefile import lang

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class MaintCyclesManagerWindow(tk.Toplevel):
    """Finestra per la gestione dei Cicli di Manutenzione (CRUD)."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('maint_cycles_title', "Gestione Cicli Manutenzione"))
        self.geometry("700x400")

        self.current_cycle_id = None

        self.description_var = tk.StringVar()
        self.value_var = tk.StringVar()

        self._create_widgets()
        self._load_cycles()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Lista Cicli (Sinistra)
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('cycles_list_label', "Lista Cicli"))
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ('desc', 'value')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('desc', text=self.lang.get('description_label', "Descrizione"))
        self.tree.heading('value', text=self.lang.get('value_label', "Valore (giorni/frazione)"))
        self.tree.column('value', width=120, anchor='center')
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_cycle_select)

        # Form (Destra)
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('details_label', "Dettagli"))
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text=self.lang.get('description_label', "Descrizione (*):")).grid(row=0, column=0,
                                                                                                sticky="w", padx=5,
                                                                                                pady=5)
        self.desc_entry = ttk.Entry(form_frame, textvariable=self.description_var)
        self.desc_entry.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('value_label_form', "Valore (*):")).grid(row=1, column=0, sticky="w",
                                                                                          padx=5, pady=5)
        self.value_entry = ttk.Entry(form_frame, textvariable=self.value_var)
        self.value_entry.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('value_info_label', "Es: 1 (giorno), 7 (settimana), 0.33 (turno 8h)"),
                  font=("Helvetica", 8)).grid(row=2, column=1, sticky="w", padx=5)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('new_button', "Nuovo"), command=self._clear_form).pack(side="left",
                                                                                                        padx=5)
        ttk.Button(btn_frame, text=self.lang.get('save_button', "Salva"), command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('delete_button', "Cancella"), command=self._delete).pack(side="left",
                                                                                                          padx=5)

    def _load_cycles(self):
        self.tree.delete(*self.tree.get_children())
        self.cycles_list = self.db.fetch_maintenance_cycles()
        for cycle in self.cycles_list:
            self.tree.insert("", "end", iid=cycle.ProgrammedInterventionId,
                             values=(cycle.TimingDescriprion, cycle.TimingValue))

    def _on_cycle_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item: return

        self.current_cycle_id = int(selected_item)
        selected_cycle = next((c for c in self.cycles_list if c.ProgrammedInterventionId == self.current_cycle_id),
                              None)
        if not selected_cycle: return

        self.description_var.set(selected_cycle.TimingDescriprion)
        self.value_var.set(selected_cycle.TimingValue)

    def _clear_form(self):
        self.tree.selection_set([])
        self.current_cycle_id = None
        self.description_var.set("")
        self.value_var.set("")
        self.desc_entry.focus_set()

    def _save(self):
        desc = self.description_var.get().strip()
        val_str = self.value_var.get().strip()
        if not desc or not val_str:
            messagebox.showerror("Dati Mancanti", "Descrizione e Valore sono obbligatori.", parent=self)
            return

        try:
            val = float(val_str)
        except ValueError:
            messagebox.showerror("Valore Non Valido", "Il valore deve essere un numero (es. 7 o 0.5).", parent=self)
            return

        if self.current_cycle_id:  # UPDATE
            if self.db.check_if_cycle_is_used(self.current_cycle_id):
                messagebox.showerror("Operazione non permessa",
                                     "Impossibile modificare un ciclo già in uso nei log di manutenzione.", parent=self)
                return
            success, message = self.db.update_maintenance_cycle(self.current_cycle_id, desc, val)
        else:  # INSERT
            success, message = self.db.add_new_maintenance_cycle(desc, val)

        if success:
            messagebox.showinfo("Successo", message, parent=self)
            self._load_cycles()
            self._clear_form()
        else:
            messagebox.showerror("Errore", message, parent=self)

    def _delete(self):
        if not self.current_cycle_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare un ciclo da cancellare.", parent=self)
            return

        if self.db.check_if_cycle_is_used(self.current_cycle_id):
            messagebox.showerror("Operazione non permessa",
                                 "Impossibile cancellare un ciclo già in uso nei log di manutenzione.", parent=self)
            return

        if messagebox.askyesno("Conferma Cancellazione", "Sei sicuro di voler cancellare questo ciclo?"):
            success, message = self.db.delete_maintenance_cycle(self.current_cycle_id)
            if success:
                messagebox.showinfo("Successo", message, parent=self)
                self._load_cycles()
                self._clear_form()
            else:
                messagebox.showerror("Errore", message, parent=self)


def open_maint_cycles_manager(parent, db, lang, user_id=None):
    MaintCyclesManagerWindow(parent, db, lang)


class DocTypesManagerWindow(tk.Toplevel):
    """Finestra per la gestione dei Tipi di Documento Generale."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('doc_types_title', "Gestione Tipi Documento"))
        self.geometry("800x400")

        self.current_type_id = None
        self.doc_types_list = []

        self.name_var = tk.StringVar()
        self.key_var = tk.StringVar()

        self._create_widgets()
        self._load_types()

    # In tools_gui.py, inside the DocTypesManagerWindow class

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Lista Tipi (Sinistra)
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('doc_types_list_label', "Lista Tipi Documento"))
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ('name', 'key')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('name', text=self.lang.get('type_name_label', "Nome Tipo"))
        self.tree.heading('key', text=self.lang.get('translation_key_label', "Chiave Traduzione"))
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_type_select)

        # Form (Destra)
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('details_label', "Dettagli"))
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text=self.lang.get('type_name_label', "Nome Tipo (*):")).grid(row=0, column=0, sticky="w",
                                                                                            padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('translation_key_label', "Chiave Traduzione (*):")).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          padx=5,
                                                                                                          pady=5)
        self.key_entry = ttk.Entry(form_frame, textvariable=self.key_var)
        self.key_entry.grid(row=1, column=1, sticky="ew", padx=5)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('new_button', "Nuovo"), command=self._clear_form).pack(side="left",
                                                                                                        padx=5)
        ttk.Button(btn_frame, text=self.lang.get('save_button', "Salva"), command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('delete_button', "Cancella"), command=self._delete).pack(side="left",
                                                                                                          padx=5)

    def _load_types(self):
        self.tree.delete(*self.tree.get_children())
        # fetch_doc_categories esiste già e fa quello che ci serve
        self.doc_types_list = self.db.fetch_doc_categories()
        for doc_type in self.doc_types_list:
            self.tree.insert("", "end", iid=doc_type.CategoriaId,
                             values=(doc_type.NomeCategoria, doc_type.TranslationKey))

    def _on_type_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item: return

        self.current_type_id = int(selected_item)
        selected_type = next((t for t in self.doc_types_list if t.CategoriaId == self.current_type_id), None)
        if not selected_type: return

        self.name_var.set(selected_type.NomeCategoria)
        self.key_var.set(selected_type.TranslationKey)

    def _clear_form(self):
        self.tree.selection_set([])
        self.current_type_id = None
        self.name_var.set("")
        self.key_var.set("")
        self.name_entry.focus_set()

    def _save(self):
        name = self.name_var.get().strip()
        key = self.key_var.get().strip()
        if not name or not key:
            messagebox.showerror("Dati Mancanti", "Nome Tipo e Chiave Traduzione sono obbligatori.", parent=self)
            return

        if self.current_type_id:  # UPDATE
            if self.db.check_if_doc_type_is_used(self.current_type_id):
                messagebox.showerror("Operazione non permessa",
                                     "Impossibile modificare un tipo di documento già in uso.", parent=self)
                return
            success, message = self.db.update_doc_type(self.current_type_id, name, key)
        else:  # INSERT
            success, message = self.db.add_new_doc_type(name, key)

        if success:
            messagebox.showinfo("Successo", message, parent=self)
            self._load_types()
            self._clear_form()
        else:
            messagebox.showerror("Errore", message, parent=self)

    def _delete(self):
        if not self.current_type_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare un tipo da cancellare.", parent=self)
            return

        if self.db.check_if_doc_type_is_used(self.current_type_id):
            messagebox.showerror("Operazione non permessa", "Impossibile cancellare un tipo di documento già in uso.",
                                 parent=self)
            return

        if messagebox.askyesno("Conferma Cancellazione", "Sei sicuro di voler cancellare questo tipo di documento?"):
            success, message = self.db.delete_doc_type(self.current_type_id)
            if success:
                messagebox.showinfo("Successo", message, parent=self)
                self._load_types()
                self._clear_form()
            else:
                messagebox.showerror("Errore", message, parent=self)


def open_doc_types_manager(parent, db, lang):
    DocTypesManagerWindow(parent, db, lang)

class BrandsManagerWindow(tk.Toplevel):
    """Finestra per la gestione dei Brand (CRUD)."""

    def _display_logo(self):
        if self.logo_binary_data and PIL_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(self.logo_binary_data))
                image.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(image)
                self.logo_label.config(image=self.logo_photo, text="")
            except Exception:
                # CORREZIONE: Aggiunto self.
                self.logo_label.config(image="", text=self.lang.get('logo_error_text', "Errore logo"))
        else:
            # CORREZIONE: Aggiunto self.
            self.logo_label.config(image="", text=self.lang.get('no_logo_text', "Nessun logo"))

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('brands_title', "Gestione Brand"))
        self.geometry("800x500")

        self.suppliers_data = {}
        self.current_brand_id = None
        self.logo_binary_data = None

        self.brand_name_var = tk.StringVar()
        self.supplier_var = tk.StringVar()

        self._create_widgets()
        self._load_suppliers()
        self._load_brands()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)  # Lista a sx
        main_frame.columnconfigure(1, weight=2)  # Form a dx

        # --- Lista Brand (Sinistra) ---
        list_frame = ttk.LabelFrame(main_frame, text=lang.get('brands_list_label', "Lista Brand"))
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ('brand', 'company')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('brand', text=lang.get('header_brand_name', "Nome Brand"))
        self.tree.heading('company', text=lang.get('header_supplier_name', "Produttore"))
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_brand_select)

        # --- Form Inserimento/Modifica (Destra) ---
        form_frame = ttk.LabelFrame(main_frame, text=lang.get('details_label', "Dettagli"))
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text=lang.get('supplier_label', "Produttore (*):")).grid(row=0, column=0, sticky="w",
                                                                                       padx=5, pady=5)
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, state="readonly")
        self.supplier_combo.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=lang.get('brand_name_label', "Nome Brand (*):")).grid(row=1, column=0, sticky="w",
                                                                                         padx=5, pady=5)
        self.brand_entry = ttk.Entry(form_frame, textvariable=self.brand_name_var)
        self.brand_entry.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=lang.get('logo_label', "Logo:")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Button(form_frame, text=lang.get('load_logo_button', "Carica..."), command=self._load_logo).grid(row=2,
                                                                                                             column=1,
                                                                                                             sticky="w",
                                                                                                             padx=5)

        self.logo_label = ttk.Label(form_frame, background="lightgrey", text=lang.get('no_logo_text', "Nessun logo"))
        self.logo_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew", ipady=20)

        # Pulsanti Azione
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=lang.get('new_brand_button', "Nuovo"), command=self._clear_form).pack(side="left",
                                                                                                         padx=5)
        ttk.Button(btn_frame, text=lang.get('save_button', "Salva"), command=self._save).pack(side="left", padx=5)

    def _load_suppliers(self):
        suppliers = self.db.fetch_suppliers()
        if suppliers:
            self.suppliers_data = {f"{s.acronimo} ({s.nazione})": s.idsoc for s in suppliers}
            self.supplier_combo['values'] = sorted(list(self.suppliers_data.keys()))

    def _load_brands(self):
        self.tree.delete(*self.tree.get_children())
        self.brands_list = self.db.fetch_brands_with_company_name()
        for brand in self.brands_list:
            self.tree.insert("", "end", iid=brand.EquipmentBrandId, values=(brand.Brand, brand.CompanyName))

    def _on_brand_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item: return

        self.current_brand_id = int(selected_item)

        # Trova il brand nella lista caricata
        selected_brand = next((b for b in self.brands_list if b.EquipmentBrandId == self.current_brand_id), None)
        if not selected_brand: return

        self.brand_name_var.set(selected_brand.Brand)

        # Trova il nome del produttore da selezionare nel combobox
        supplier_name = next((name for name, id in self.suppliers_data.items() if id == selected_brand.CompanyId), "")
        self.supplier_var.set(supplier_name)

        self.logo_binary_data = selected_brand.BrandLogo
        self._display_logo()

    def _clear_form(self):
        self.tree.selection_set([])  # Deseleziona la lista
        self.current_brand_id = None
        self.brand_name_var.set("")
        self.supplier_var.set("")
        self.logo_binary_data = None
        self._display_logo()
        self.brand_entry.focus_set()

    def _load_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.logo_binary_data = f.read()
                self._display_logo()
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare il logo: {e}")

    def _display_logo(self):
        if self.logo_binary_data and PIL_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(self.logo_binary_data))
                image.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(image)
                self.logo_label.config(image=self.logo_photo, text="")
            except Exception:
                self.logo_label.config(image="", text=lang.get('logo_error_text', "Errore logo"))
        else:
            self.logo_label.config(image="", text=lang.get('no_logo_text', "Nessun logo"))

    def _save(self):
        brand_name = self.brand_name_var.get().strip()
        supplier_name = self.supplier_var.get()

        if not brand_name or not supplier_name:
            messagebox.showerror("Dati Mancanti", "Produttore e Nome Brand sono obbligatori.", parent=self)
            return

        company_id = self.suppliers_data.get(supplier_name)

        if self.current_brand_id:  # Modalità UPDATE
            success, message = self.db.update_brand(self.current_brand_id, company_id, brand_name,
                                                    self.logo_binary_data)
        else:  # Modalità INSERT
            success, message = self.db.add_new_brand(company_id, brand_name, self.logo_binary_data)

        if success:
            messagebox.showinfo("Successo", message, parent=self)
            self._load_brands()
            self._clear_form()
        else:
            messagebox.showerror("Errore", message, parent=self)


def open_brands_manager(parent, db, lang):
    BrandsManagerWindow(parent, db, lang)

class AddSupplierDialog(tk.Toplevel):
    """Dialogo per inserire un nuovo fornitore."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.transient(parent)
        self.grab_set()
        self.title(lang.get('add_supplier_title', "Nuovo Fornitore"))
        self.geometry("450x250")

        self.new_supplier_added = False
        self.currencies_data = {}

        self.name_var = tk.StringVar()
        self.nation_var = tk.StringVar()
        self.vat_var = tk.StringVar()
        self.currency_var = tk.StringVar()

        self._create_widgets()
        self._load_currencies()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text=self.lang.get('supplier_name_label', "Nome Fornitore (*):")).grid(row=0, column=0,
                                                                                                sticky="w", pady=5)
        self.name_entry = ttk.Entry(frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text=self.lang.get('nation_label', "Nazione:")).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.nation_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text=self.lang.get('vat_number_label', "Partita IVA (*):")).grid(row=2, column=0, sticky="w",
                                                                                          pady=5)
        ttk.Entry(frame, textvariable=self.vat_var).grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text=self.lang.get('currency_label', "Valuta (*):")).grid(row=3, column=0, sticky="w", pady=5)
        self.currency_combo = ttk.Combobox(frame, textvariable=self.currency_var, state="readonly")
        self.currency_combo.grid(row=3, column=1, sticky="ew")

        ttk.Button(frame, text=self.lang.get('save_button', "Salva"), command=self._save_supplier).grid(row=4, column=1,
                                                                                                        sticky="e",
                                                                                                        pady=15)
        self.name_entry.focus_set()

    def _load_currencies(self):
        currencies = self.db.fetch_currencies()
        if currencies:
            self.currencies_data = {c.desc: c.IdValuta for c in currencies}
            self.currency_combo['values'] = sorted(list(self.currencies_data.keys()))

    def _save_supplier(self):
        name = self.name_var.get().strip()
        nation = self.nation_var.get().strip()
        vat = self.vat_var.get().strip()
        currency_name = self.currency_var.get()

        if not all([name, vat, currency_name]):
            messagebox.showerror("Dati Mancanti", "Nome Fornitore, Partita IVA e Valuta sono obbligatori.", parent=self)
            return

        currency_id = self.currencies_data.get(currency_name)

        success, message = self.db.add_new_supplier(name, nation, vat, currency_id)

        if success:
            messagebox.showinfo("Successo", message, parent=self)
            self.new_supplier_added = True
            self.destroy()
        else:
            messagebox.showerror("Errore", message, parent=self)


class SuppliersManagerWindow(tk.Toplevel):
    """Finestra per la gestione dei fornitori."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('suppliers_title', "Gestione Produttori"))
        self.geometry("600x200")

        self.suppliers_data = {}
        self.supplier_var = tk.StringVar()

        self._create_widgets()
        self._load_suppliers()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)

        lbl = ttk.Label(frame, text=self.lang.get('select_supplier_label',
                                                  "Seleziona un produttore esistente o creane uno nuovo:"))
        lbl.pack(fill="x", pady=5)

        combo_frame = ttk.Frame(frame)
        combo_frame.pack(fill="x", expand=True, pady=5)
        combo_frame.columnconfigure(0, weight=1)

        self.supplier_combo = ttk.Combobox(combo_frame, textvariable=self.supplier_var, state="readonly", height=15)
        self.supplier_combo.grid(row=0, column=0, sticky="ew")

        new_button = ttk.Button(combo_frame, text=self.lang.get('new_button', "Nuovo..."),
                                command=self._open_add_dialog)
        new_button.grid(row=0, column=1, padx=(10, 0))

    def _load_suppliers(self):
        suppliers = self.db.fetch_suppliers()
        if suppliers:
            self.suppliers_data = {f"{s.acronimo} ({s.nazione})": s.idsoc for s in suppliers}
            self.supplier_combo['values'] = sorted(list(self.suppliers_data.keys()))

    def _open_add_dialog(self):
        dialog = AddSupplierDialog(self, self.db, self.lang)
        self.wait_window(dialog)
        if dialog.new_supplier_added:
            self._load_suppliers()  # Ricarica la lista se un nuovo fornitore è stato aggiunto


class MaintenanceTimesManagerWindow(tk.Toplevel):
    """Finestra per gestire i tempi standard di manutenzione."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('maint_times_title', "Gestione Tempi Manutenzione"))
        self.geometry("1000x600")

        self.equipments_data = {}
        self.cycles_data = {}
        self.tasks_data = {}  # Per conservare i dati completi della riga selezionata

        self.equipment_var = tk.StringVar()
        self.cycle_var = tk.StringVar()
        self.pdf_ref_var = tk.StringVar()
        self.timing_var = tk.StringVar()

        self._create_widgets()
        self._load_filters()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Filtri
        filter_frame = ttk.LabelFrame(main_frame, text="Filtri", padding="10")
        filter_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)

        ttk.Label(filter_frame, text="Macchinario:").grid(row=0, column=0, sticky="w", padx=5)
        self.equipment_combo = ttk.Combobox(filter_frame, textvariable=self.equipment_var, state="readonly")
        self.equipment_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.equipment_combo.bind("<<ComboboxSelected>>", self._on_filter_change)

        ttk.Label(filter_frame, text="Ciclo di Manutenzione:").grid(row=0, column=2, sticky="w", padx=5)
        self.cycle_combo = ttk.Combobox(filter_frame, textvariable=self.cycle_var, state="readonly")
        self.cycle_combo.grid(row=0, column=3, sticky="ew", padx=5)
        self.cycle_combo.bind("<<ComboboxSelected>>", self._on_filter_change)

        # Contenuto
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=3)  # Lista
        content_frame.columnconfigure(1, weight=2)  # Dettagli

        # Lista Task (Sinistra)
        cols = ('task', 'desc')
        self.tree = ttk.Treeview(content_frame, columns=cols, show="headings")
        self.tree.heading('task', text="Nome Compito")
        self.tree.heading('desc', text="Descrizione")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_task_select)

        # Form Dettagli (Destra)
        details_frame = ttk.LabelFrame(content_frame, text="Dettagli", padding="15")
        details_frame.pack(side="right", fill="y", padx=(10, 0))
        details_frame.columnconfigure(0, weight=1)

        ttk.Label(details_frame, text="Riferimento PDF:").pack(anchor="w")
        self.pdf_ref_entry = ttk.Entry(details_frame, textvariable=self.pdf_ref_var, state="disabled")
        self.pdf_ref_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(details_frame, text="Tempo Standard (minuti):").pack(anchor="w")
        self.timing_entry = ttk.Entry(details_frame, textvariable=self.timing_var, state="disabled")
        self.timing_entry.pack(fill="x")

        self.save_button = ttk.Button(details_frame, text="Salva Modifiche", command=self._save_changes,
                                      state="disabled")
        self.save_button.pack(pady=20)

    def _load_filters(self):
        equipments = self.db.fetch_equipments_for_timing()
        if equipments:
            self.equipments_data = {eq.EquipmentName: eq.EquipmentId for eq in equipments}
            self.equipment_combo['values'] = sorted(list(self.equipments_data.keys()))

        cycles = self.db.fetch_maintenance_cycles()
        if cycles:
            self.cycles_data = {c.TimingDescriprion: c.ProgrammedInterventionId for c in cycles}
            self.cycle_combo['values'] = sorted(list(self.cycles_data.keys()))

    def _on_filter_change(self, event=None):
        equipment_id = self.equipments_data.get(self.equipment_var.get())
        cycle_id = self.cycles_data.get(self.cycle_var.get())

        self.tree.delete(*self.tree.get_children())
        self._clear_details_form()

        if equipment_id and cycle_id:
            tasks = self.db.fetch_tasks_for_timing(equipment_id, cycle_id)
            self.tasks_data.clear()
            for task in tasks:
                self.tree.insert("", "end", iid=task.CompitoId, values=(task.NomeCompito, task.DescrizioneCompito))
                self.tasks_data[task.CompitoId] = task  # Salva tutti i dati della riga

    def _on_task_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item:
            self._clear_details_form()
            return

        task_id = int(selected_item)
        task_data = self.tasks_data.get(task_id)
        if not task_data: return

        self.pdf_ref_var.set(task_data.PdfRiferiment or "")
        self.timing_var.set(task_data.TimingMinutes or "")

        self.pdf_ref_entry.config(state="normal")
        self.timing_entry.config(state="normal")
        self.save_button.config(state="normal")

    def _clear_details_form(self):
        self.pdf_ref_var.set("")
        self.timing_var.set("")
        self.pdf_ref_entry.config(state="disabled")
        self.timing_entry.config(state="disabled")
        self.save_button.config(state="disabled")

    def _save_changes(self):
        selected_item = self.tree.focus()
        if not selected_item: return

        task_id = int(selected_item)
        task_data = self.tasks_data.get(task_id)

        new_pdf_ref = self.pdf_ref_var.get().strip()
        new_timing_str = self.timing_var.get().strip()

        try:
            # Convalida che il timing sia un numero, se inserito
            if new_timing_str:
                float(new_timing_str)
        except ValueError:
            messagebox.showerror("Errore", "Il tempo standard deve essere un numero.", parent=self)
            return

        # 1. Aggiorna riferimento PDF
        pdf_success = self.db.update_task_pdf_reference(task_id, new_pdf_ref)

        # 2. Aggiorna il timing
        timing_success = self.db.update_task_timing(task_id, new_timing_str, task_data.CompitoManutenzioneTimingId)

        if pdf_success and timing_success:
            messagebox.showinfo("Successo", "Dati aggiornati con successo.", parent=self)
            self._on_filter_change()  # Ricarica la lista per mostrare i dati aggiornati
        else:
            messagebox.showerror("Errore",
                                 f"Si è verificato un errore durante il salvataggio:\n{self.db.last_error_details}",
                                 parent=self)


class CompanyManagerWindow(tk.Toplevel):
    """Finestra per la gestione delle Compagnie/Siti."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('company_management_title', "Gestione Compagnie"))
        self.geometry("900x550")

        self.current_site_id = None
        self.logo_binary_data = None
        self.sites_list = []

        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.vat_var = tk.StringVar()
        self.country_var = tk.StringVar()

        self._create_widgets()
        self._load_sites()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Lista Compagnie (Sinistra)
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('company_list_label', "Lista Compagnie"))
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ('name', 'country', 'vat')
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        self.tree.heading('name', text=self.lang.get('header_company_name', "Nome Compagnia"))
        self.tree.heading('country', text=self.lang.get('header_country', "Nazione"))
        self.tree.heading('vat', text=self.lang.get('header_vat', "Partita IVA"))
        self.tree.column('country', width=80, anchor='center')
        self.tree.column('vat', width=120)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_site_select)

        # Form (Destra)
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('details_label', "Dettagli"))
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text=self.lang.get('company_name_label', "Nome Compagnia (*):")).grid(row=0, column=0,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=3)
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('address_label', "Indirizzo:")).grid(row=1, column=0, sticky="w",
                                                                                      padx=5, pady=3)
        ttk.Entry(form_frame, textvariable=self.address_var).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('vat_label', "Partita IVA:")).grid(row=2, column=0, sticky="w", padx=5,
                                                                                    pady=3)
        ttk.Entry(form_frame, textvariable=self.vat_var).grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('country_label', "Nazione (*):")).grid(row=3, column=0, sticky="w",
                                                                                        padx=5, pady=3)
        ttk.Entry(form_frame, textvariable=self.country_var).grid(row=3, column=1, sticky="ew", padx=5)

        ttk.Label(form_frame, text=self.lang.get('logo_label', "Logo:")).grid(row=4, column=0, sticky="w", padx=5,
                                                                              pady=5)
        ttk.Button(form_frame, text=self.lang.get('load_logo_button', "Carica..."), command=self._load_logo).grid(row=4,
                                                                                                                  column=1,
                                                                                                                  sticky="w",
                                                                                                                  padx=5)

        self.logo_label = ttk.Label(form_frame, background="lightgrey",
                                    text=self.lang.get('no_logo_text', "Nessun logo"))
        self.logo_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", ipady=20)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('new_button_short', "Nuovo"), command=self._clear_form).pack(
            side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('save_button', "Salva"), command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('delete_button', "Cancella"), command=self._delete).pack(side="left",
                                                                                                          padx=5)

    def _load_sites(self):
        self.tree.delete(*self.tree.get_children())
        self.sites_list = self.db.fetch_all_sites()
        for site in self.sites_list:
            self.tree.insert("", "end", iid=site.IDSite, values=(site.SiteName, site.SiteCountry, site.SiteVat))

    def _load_logo(self):
        """Apre una finestra di dialogo per selezionare un file immagine."""
        if not PIL_AVAILABLE:
            messagebox.showwarning("Libreria Mancante",
                                   "La libreria Pillow non è installata. Impossibile caricare immagini.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            with open(file_path, 'rb') as f:
                self.logo_binary_data = f.read()
            self._display_logo()

    def _on_site_select(self, event=None):
        selected_item = self.tree.focus()
        if not selected_item: return
        self.current_site_id = int(selected_item)

        selected_site = next((s for s in self.sites_list if s.IDSite == self.current_site_id), None)
        if not selected_site: return

        self.name_var.set(selected_site.SiteName or "")
        self.address_var.set(selected_site.SiteAddress or "")
        self.vat_var.set(selected_site.SiteVat or "")
        self.country_var.set(selected_site.SiteCountry or "")
        self.logo_binary_data = selected_site.Logo
        self._display_logo()

    def _clear_form(self):
        self.tree.selection_set([])
        self.current_site_id = None
        self.name_var.set("")
        self.address_var.set("")
        self.vat_var.set("")
        self.country_var.set("")
        self.logo_binary_data = None
        self._display_logo()
        self.name_entry.focus_set()

    def _display_logo(self):
        """Mostra un'anteprima del logo caricato."""
        if self.logo_binary_data and PIL_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(self.logo_binary_data))
                image = image.convert("RGB")
                image.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(image)
                self.logo_label.config(image=self.logo_photo, text="")
            except Exception as e:
                print(f"ERRORE caricamento logo: {e}")
                self.logo_label.config(image="", text=self.lang.get('logo_error_text', "Errore logo"))
        else:
            self.logo_label.config(image="", text=self.lang.get('no_logo_text', "Nessun logo"))

    def _save(self):
        name = self.name_var.get().strip()
        country = self.country_var.get().strip()
        if not name or not country:
            messagebox.showerror("Dati Mancanti", "Nome Compagnia e Nazione sono obbligatori.", parent=self)
            return

        address = self.address_var.get().strip()
        vat = self.vat_var.get().strip()

        # --- CONTROLLO AGGIUNTIVO PER SICUREZZA ---
        # Se stiamo modificando, l'ID è già noto. Se è nuovo, non c'è CompanyId da validare qui.
        company_id_to_save = self.current_site_id
        # --- FINE CONTROLLO ---

        if company_id_to_save:  # UPDATE
            success, message = self.db.update_site(company_id_to_save, name, address, vat, country,
                                                   self.logo_binary_data)
        else:  # INSERT
            success, message = self.db.add_new_site(name, address, vat, country, self.logo_binary_data)

        if success:
            messagebox.showinfo("Successo", message, parent=self)
            self._load_sites()
            self._clear_form()
        else:
            messagebox.showerror("Errore", message, parent=self)

    def _delete(self):
        if not self.current_site_id:
            messagebox.showwarning("Nessuna Selezione", "Selezionare una compagnia da cancellare.", parent=self)
            return

        if messagebox.askyesno("Conferma Cancellazione",
                               "Sei sicuro di voler cancellare questa compagnia? L'operazione non è reversibile."):
            # Aggiungere qui un controllo per verificare se la compagnia è in uso prima di cancellare
            success, message = self.db.delete_site(self.current_site_id)
            if success:
                messagebox.showinfo("Successo", message, parent=self)
                self._load_sites()
                self._clear_form()
            else:
                messagebox.showerror("Errore", message, parent=self)

def open_company_manager(parent, db, lang, user_name):
    CompanyManagerWindow(parent, db, lang, user_name)
def open_maintenance_times_manager(parent, db, lang, user_name):
    MaintenanceTimesManagerWindow(parent, db, lang, user_name)

def open_suppliers_manager(parent, db, lang, user_id=None):
    SuppliersManagerWindow(parent, db, lang)