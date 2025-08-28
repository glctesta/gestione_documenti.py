# operations_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Importa il nuovo widget calendario
from datetime import datetime


class AddInterruptionWindow(tk.Toplevel):
    """Finestra per l'inserimento di un fermo di produzione."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('submenu_interruptions', "Registra Interruzione di Produzione"))
        self.geometry("600x450")
        self.transient(parent)
        self.grab_set()

        # Dati per i combobox
        self.areas_data = {}
        self.problems_data = {}
        self.equipments_data = {}
        self.orders_data = {}
        self.all_order_names = []

        # Variabili Tkinter
        self.date_var = tk.StringVar()
        self.from_hour_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        self.duration_var = tk.StringVar()
        self.po_number_var = tk.StringVar()
        self.area_var = tk.StringVar()
        self.problem_var = tk.StringVar()
        self.equipment_var = tk.StringVar()

        self._create_widgets()
        self._load_combobox_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)  # Permette al campo note di espandersi

        ttk.Label(main_frame, text="Data Interruzione (*):").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.date_entry = DateEntry(main_frame, date_pattern='dd/MM/yyyy', textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, sticky="w", pady=3)

        ttk.Label(main_frame, text="Ora Inizio (HH:MM) (*):").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(main_frame, textvariable=self.from_hour_var, width=10).grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(main_frame, text="Durata (minuti) (*):").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(main_frame, textvariable=self.duration_var, width=10).grid(row=2, column=1, sticky="w", pady=3)

        ttk.Label(main_frame, text="Ordine di Produzione:").grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.order_combo = ttk.Combobox(main_frame, textvariable=self.po_number_var, state="normal")
        self.order_combo.grid(row=3, column=1, sticky="ew", pady=3)
        self.order_combo.bind('<KeyRelease>', self._filter_order_combo)

        ttk.Label(main_frame, text="Area (*):").grid(row=4, column=0, sticky="w", padx=5, pady=3)
        self.area_combo = ttk.Combobox(main_frame, textvariable=self.area_var, state="readonly")
        self.area_combo.grid(row=4, column=1, sticky="ew", pady=3)

        ttk.Label(main_frame, text="Causa (*):").grid(row=5, column=0, sticky="w", padx=5, pady=3)
        self.problem_combo = ttk.Combobox(main_frame, textvariable=self.problem_var, state="readonly")
        self.problem_combo.grid(row=5, column=1, sticky="ew", pady=3)
        self.problem_combo.bind("<<ComboboxSelected>>", self._on_problem_select)

        ttk.Label(main_frame, text="Macchinario Coinvolto:").grid(row=6, column=0, sticky="w", padx=5, pady=3)
        self.equipment_combo = ttk.Combobox(main_frame, textvariable=self.equipment_var, state="disabled")
        self.equipment_combo.grid(row=6, column=1, sticky="ew", pady=3)

        ttk.Label(main_frame, text="Note:").grid(row=7, column=0, sticky="nw", padx=5, pady=3)
        self.notes_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.notes_text.grid(row=7, column=1, sticky="nsew", pady=3)

        ttk.Button(main_frame, text="Salva Dichiarazione", command=self._save_interruption).grid(row=8, column=1,
                                                                                                 sticky="e", pady=15)

    def _load_combobox_data(self):
        # Aree
        areas = self.db.fetch_issue_areas()
        if areas:
            self.areas_data = {a.IssueArea: a.IssueAreaId for a in areas}
            self.area_combo['values'] = sorted(list(self.areas_data.keys()))

        # Carica Ordini di Produzione
        orders = self.db.fetch_open_production_orders()
        if orders:
            self.orders_data = {o.OrderNumber: o.idordine for o in orders}
            self.all_order_names = sorted(list(self.orders_data.keys()))
            self.order_combo['values'] = self.all_order_names

        # Cause/Problemi
        problems = self.db.fetch_issue_problems()
        if problems:
            # Assumiamo che la query restituisca colonne 'IssueProblemId' e 'DescriptionEN' o simile
            self.problems_data = {p.DescriptionEN: p.IssueProblemId for p in problems}
            self.problem_combo['values'] = sorted(list(self.problems_data.keys()))

        # Macchinari
        equipments = self.db.fetch_all_equipments()
        if equipments:
            self.equipments_data = {f"{eq.InternalName or ''} [{eq.SerialNumber}]": eq.EquipmentId for eq in equipments}
            self.equipment_combo['values'] = sorted(list(self.equipments_data.keys()))

    def _on_problem_select(self, event=None):
        """Abilita la scelta della macchina solo se la causa è relativa a un guasto."""
        problem_text = self.problem_var.get().lower()
        if "machine" in problem_text or "equipment" in problem_text or "macchina" in problem_text:
            self.equipment_combo.config(state="readonly")
        else:
            self.equipment_combo.config(state="disabled")
            self.equipment_var.set("")

    def _filter_order_combo(self, event):
        """Filtra la lista degli ordini di produzione in base al testo digitato."""
        typed_text = self.po_number_var.get().lower()
        if not typed_text:
            self.order_combo['values'] = self.all_order_names
            return

        filtered_list = [name for name in self.all_order_names if typed_text in name.lower()]
        self.order_combo['values'] = filtered_list

    def _save_interruption(self):
        # ... (Logica di salvataggio)
        try:
            # Recupera e valida i dati
            report_date = self.date_entry.get_date()
            from_hour = self.from_hour_var.get()
            duration_min = int(self.duration_var.get())
            area_id = self.areas_data[self.area_var.get()]
            problem_id = self.problems_data[self.problem_var.get()]
        except (ValueError, KeyError):
            messagebox.showerror("Dati non validi",
                                 "Assicurati che Data, Ora, Durata, Area e Causa siano compilati correttamente.",
                                 parent=self)
            return

        equipment_id = self.equipments_data.get(self.equipment_var.get())  # Può essere None
        po_number = self.po_number_var.get() or None
        notes = self.notes_text.get("1.0", tk.END).strip() or None

        success, msg = self.db.add_production_interruption(
            report_date, self.user_name, from_hour, duration_min,
            area_id, equipment_id, problem_id, po_number, notes
        )

        if success:
            messagebox.showinfo("Successo", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Errore", msg, parent=self)


def open_add_interruption_window(parent, db, lang, user_name):
    AddInterruptionWindow(parent, db, lang, user_name)