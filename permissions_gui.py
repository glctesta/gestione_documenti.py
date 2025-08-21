# permissions_gui.py
import tkinter as tk
from tkinter import ttk, messagebox


class ViewPermissionsWindow(tk.Toplevel):
    """Finestra per la SOLA VISUALIZZAZIONE dei permessi di un utente."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('view_permissions_title', "Visualizza Autorizzazioni"))
        self.geometry("700x400")
        self.transient(parent)
        self.grab_set()

        self.employees_data = {}
        self.employee_var = tk.StringVar()

        self._create_widgets()
        self._load_employees()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Filtro per dipendente
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(filter_frame, text=self.lang.get('select_employee_label', "Seleziona Dipendente:")).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=(0, 5))
        self.employee_combo = ttk.Combobox(filter_frame, textvariable=self.employee_var, state="readonly", height=10)
        self.employee_combo.grid(row=0, column=1, sticky="ew")
        self.employee_combo.bind("<<ComboboxSelected>>", self._load_permissions)

        # Lista permessi
        cols = ('permission',)
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading('permission', text=self.lang.get('permission_header', "Menu Autorizzato"))
        self.tree.grid(row=1, column=0, sticky="nsew")

    def _load_employees(self):
        # Riusiamo la funzione esistente per caricare i dipendenti
        employees = self.db.fetch_authorized_employees()
        if employees:
            self.employees_data = {e.Employ: e.EmployeeHireHistoryId for e in employees}
            self.employee_combo['values'] = sorted(list(self.employees_data.keys()))

    def _load_permissions(self, event=None):
        self.tree.delete(*self.tree.get_children())
        employee_name = self.employee_var.get()
        if not employee_name: return

        employee_id = self.employees_data.get(employee_name)
        permissions = self.db.fetch_user_permissions(employee_id)

        if permissions:
            for perm in permissions:
                if perm.MenuKey:  # Mostra solo se esiste una chiave menu
                    self.tree.insert("", "end", values=(perm.MenuKey,))


class ManagePermissionsWindow(tk.Toplevel):
    """Finestra per AGGIUNGERE o RIMUOVERE permessi a un utente."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('manage_permissions_title', "Gestione Autorizzazioni Speciali"))
        self.geometry("900x500")
        self.transient(parent)
        self.grab_set()

        self.employees_data = {}
        self.available_perms_data = {}
        self.assigned_perms_data = {}
        self.employee_var = tk.StringVar()

        # --- NUOVO: Lista per conservare tutti i nomi dei dipendenti per la ricerca ---
        self.all_employee_names = []

        self._create_widgets()
        self._load_employees()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_frame.columnconfigure(1, weight=1)
        ttk.Label(top_frame, text=self.lang.get('select_employee_label', "Seleziona o Cerca Dipendente:")).grid(row=0,
                                                                                                                column=0)

        # --- MODIFICATO: state='normal' per permettere la scrittura ---
        self.employee_combo = ttk.Combobox(top_frame, textvariable=self.employee_var, state="normal", height=10)
        self.employee_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.employee_combo.bind("<<ComboboxSelected>>", self._populate_lists)
        # --- NUOVO: Associa la pressione dei tasti alla funzione di filtro ---
        self.employee_combo.bind('<KeyRelease>', self._filter_employee_combo)

        lists_frame = ttk.Frame(main_frame)
        lists_frame.grid(row=1, column=0, sticky="nsew")
        lists_frame.rowconfigure(0, weight=1)
        lists_frame.columnconfigure(0, weight=1)
        lists_frame.columnconfigure(2, weight=1)

        # Lista Sinistra: Permessi Disponibili
        available_frame = ttk.LabelFrame(lists_frame,
                                         text=self.lang.get('available_perms_label', "Permessi Disponibili"))
        available_frame.grid(row=0, column=0, sticky="nsew")
        self.available_list = tk.Listbox(available_frame, selectmode="extended")
        self.available_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Pulsanti Centrali
        btn_frame = ttk.Frame(lists_frame)
        btn_frame.grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text=">>", command=self._grant_permission).pack(pady=5)
        ttk.Button(btn_frame, text="<<", command=self._revoke_permission).pack(pady=5)

        # Lista Destra: Permessi Assegnati
        assigned_frame = ttk.LabelFrame(lists_frame, text=self.lang.get('assigned_perms_label', "Permessi Assegnati"))
        assigned_frame.grid(row=0, column=2, sticky="nsew")
        self.assigned_list = tk.Listbox(assigned_frame, selectmode="extended")
        self.assigned_list.pack(fill="both", expand=True, padx=5, pady=5)

    def _load_employees(self):
        employees = self.db.fetch_authorized_employees()
        if employees:
            self.employees_data = {e.Employ: e.EmployeeHireHistoryId for e in employees}
            # --- NUOVO: Salva la lista completa per la ricerca ---
            self.all_employee_names = sorted(list(self.employees_data.keys()))
            self.employee_combo['values'] = self.all_employee_names

    # --- NUOVO: Metodo per filtrare la lista dei dipendenti ---
    def _filter_employee_combo(self, event):
        typed_text = self.employee_var.get().lower()

        if not typed_text:
            self.employee_combo['values'] = self.all_employee_names
            # Se l'utente cancella il testo, pulisce anche le liste dei permessi
            self.available_list.delete(0, tk.END)
            self.assigned_list.delete(0, tk.END)
            return

        filtered_list = [name for name in self.all_employee_names if typed_text in name.lower()]
        self.employee_combo['values'] = filtered_list

    def _populate_lists(self, event=None):
        # ... questo metodo rimane invariato ...
        self.available_list.delete(0, tk.END)
        self.assigned_list.delete(0, tk.END)
        self.available_perms_data.clear()
        self.assigned_perms_data.clear()

        employee_name = self.employee_var.get()
        if not employee_name or employee_name not in self.employees_data:
            return  # Non fare nulla se il nome non è valido
        employee_id = self.employees_data[employee_name]

        available = self.db.fetch_available_permissions(employee_id)
        for perm in available:
            self.available_list.insert(tk.END, perm.translationvalue)
            self.available_perms_data[perm.translationvalue] = perm.Translationkey

        assigned = self.db.fetch_user_permissions(employee_id)
        for perm in assigned:
            if perm.MenuKey:
                self.assigned_list.insert(tk.END, perm.MenuKey)
                self.assigned_perms_data[perm.MenuKey] = perm.AuthorizedUsedId

    def _grant_permission(self):
        # ... questo metodo rimane invariato ...
        selections = self.available_list.curselection()
        if not selections: return
        employee_id = self.employees_data[self.employee_var.get()]

        for i in selections:
            display_name = self.available_list.get(i)
            translation_key = self.available_perms_data[display_name]
            self.db.grant_permission(employee_id, translation_key)

        self._populate_lists()

    def _revoke_permission(self):
        # ... questo metodo rimane invariato ...
        selections = self.assigned_list.curselection()
        if not selections: return

        for i in selections:
            display_name = self.assigned_list.get(i)
            authorized_user_id = self.assigned_perms_data[display_name]
            self.db.revoke_permission(authorized_user_id)

        self._populate_lists()


# Funzioni Launcher
def open_view_permissions_window(parent, db, lang):
    ViewPermissionsWindow(parent, db, lang)


def open_manage_permissions_window(parent, db, lang):
    ManagePermissionsWindow(parent, db, lang)