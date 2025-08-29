# operations_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta


class AddInterruptionWindow(tk.Toplevel):
    """Finestra per l'inserimento di un fermo di produzione."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('submenu_interruptions', "Registra Interruzione di Produzione"))
        self.geometry("800x650")

        # Dati per i combobox
        self.working_areas_data, self.sub_areas_data, self.lines_data = {}, {}, {}
        self.orders_data, self.issue_areas_data, self.problems_data = {}, {}, {}
        self.all_order_names = []

        # Variabili Tkinter
        self.working_area_var, self.sub_area_var, self.line_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.order_var = tk.StringVar()
        self.time_choice_var = tk.StringVar(value="duration")
        self.from_hour_var, self.to_hour_var, self.duration_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.issue_area_var, self.problem_var = tk.StringVar(), tk.StringVar()
        # Definisce i testi dei placeholder
        self.action_plan_placeholder = self.lang.get('action_plan_placeholder', 'Inserire un piano d''azione...')
        self.comments_placeholder = self.lang.get('comments_placeholder',
                                                  'Digita una nota per spiegare meglio il problema...')

        self.action_plan_placeholder = self.lang.get('action_plan_placeholder', 'Inserire un piano d''azione...')

        self._create_widgets()
        self._load_initial_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)

        loc_frame = ttk.LabelFrame(main_frame, text=self.lang.get('loc_frame_title', "Localizzazione"))
        loc_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)
        loc_frame.columnconfigure(1, weight=1)
        loc_frame.columnconfigure(3, weight=1)

        ttk.Label(loc_frame, text=self.lang.get('working_area_label', "Working Area (*):")).grid(row=0, column=0,
                                                                                                 sticky="w", padx=5,
                                                                                                 pady=3)
        self.wa_combo = ttk.Combobox(loc_frame, textvariable=self.working_area_var, state="readonly")
        self.wa_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.wa_combo.bind("<<ComboboxSelected>>", self._on_wa_select)

        ttk.Label(loc_frame, text=self.lang.get('sub_area_label', "Sub Area (*):")).grid(row=0, column=2, sticky="w",
                                                                                         padx=5, pady=3)
        self.sa_combo = ttk.Combobox(loc_frame, textvariable=self.sub_area_var, state="disabled")
        self.sa_combo.grid(row=0, column=3, sticky="ew", padx=5)
        self.sa_combo.bind("<<ComboboxSelected>>", self._on_sa_select)

        ttk.Label(loc_frame, text=self.lang.get('line_label', "Linea (*):")).grid(row=1, column=0, sticky="w", padx=5,
                                                                                  pady=3)
        self.line_combo = ttk.Combobox(loc_frame, textvariable=self.line_var, state="disabled")
        self.line_combo.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(loc_frame, text=self.lang.get('order_label', "Ordine di Produzione:")).grid(row=1, column=2,
                                                                                              sticky="w", padx=5,
                                                                                              pady=3)
        self.order_combo = ttk.Combobox(loc_frame, textvariable=self.order_var, state="normal")
        self.order_combo.grid(row=1, column=3, sticky="ew", padx=5)
        self.order_combo.bind("<KeyRelease>", self._filter_order_combo)

        time_frame = ttk.LabelFrame(main_frame, text=self.lang.get('time_frame_title', "Tempistiche"))
        time_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        time_frame.columnconfigure(1, weight=1)

        ttk.Label(time_frame, text=self.lang.get('date_label_req', "Data (*):")).grid(row=0, column=0, sticky="w",
                                                                                      padx=5, pady=3)
        self.date_entry = DateEntry(time_frame, date_pattern='dd/MM/yyyy')
        self.date_entry.grid(row=0, column=1, sticky="w")

        ttk.Radiobutton(time_frame, text=self.lang.get('time_radio_duration', "Durata (minuti)"),
                        variable=self.time_choice_var, value="duration", command=self._toggle_time_fields).grid(row=1,
                                                                                                                column=0,
                                                                                                                sticky="w",
                                                                                                                padx=5)
        self.duration_entry = ttk.Entry(time_frame, textvariable=self.duration_var)
        self.duration_entry.grid(row=1, column=1, sticky="w")

        ttk.Radiobutton(time_frame, text=self.lang.get('time_radio_range', "Intervallo Orario"),
                        variable=self.time_choice_var, value="range", command=self._toggle_time_fields).grid(row=2,
                                                                                                             column=0,
                                                                                                             sticky="w",
                                                                                                             padx=5)
        range_frame = ttk.Frame(time_frame)
        range_frame.grid(row=2, column=1, sticky="ew")
        ttk.Label(range_frame, text=self.lang.get('from_label_short', "Da:")).pack(side="left")
        self.from_entry = ttk.Entry(range_frame, textvariable=self.from_hour_var, width=8)
        self.from_entry.pack(side="left", padx=5)
        ttk.Label(range_frame, text=self.lang.get('to_label_short', "A:")).pack(side="left")
        self.to_entry = ttk.Entry(range_frame, textvariable=self.to_hour_var, width=8)
        self.to_entry.pack(side="left", padx=5)
        self.to_entry.bind("<FocusOut>", self._calculate_duration)

        cause_frame = ttk.LabelFrame(main_frame, text=self.lang.get('cause_frame_title', "Causa dell'Interruzione"))
        cause_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5)
        cause_frame.columnconfigure(1, weight=1)
        cause_frame.columnconfigure(3, weight=1)

        ttk.Label(cause_frame, text=self.lang.get('issue_area_label', "Issue Area (*):")).grid(row=0, column=0,
                                                                                               sticky="w", padx=5,
                                                                                               pady=3)
        self.ia_combo = ttk.Combobox(cause_frame, textvariable=self.issue_area_var, state="readonly")
        self.ia_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.ia_combo.bind("<<ComboboxSelected>>", lambda e: self._update_problems_combo())


        ttk.Label(cause_frame, text=self.lang.get('event_label', "Evento/Problema (*):")).grid(row=0, column=2,
                                                                                               sticky="w", padx=5,
                                                                                               pady=3)
        self.problem_combo = ttk.Combobox(cause_frame, textvariable=self.problem_var, state="disabled")
        self.problem_combo.grid(row=0, column=3, sticky="ew", padx=5)

        notes_frame = ttk.LabelFrame(main_frame, text=self.lang.get('notes_frame_title', "Note e Piano d'Azione"))
        notes_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=5)
        main_frame.rowconfigure(3, weight=1)
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(0, weight=1)
        notes_frame.rowconfigure(2, weight=1)
        ttk.Label(notes_frame, text=self.lang.get('comments_label', "Commenti (*):")).pack(anchor="w")
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.insert("1.0", self.comments_placeholder)
        self.notes_text.config(foreground="grey")
        self.notes_text.bind("<FocusIn>", self._on_comments_focus_in)
        self.notes_text.bind("<FocusOut>", self._on_comments_focus_out)
        self.notes_text.pack(fill="x", expand=True, padx=5, pady=2)

        ttk.Label(notes_frame, text=self.lang.get('comments_label', "Commenti (*):")).pack(anchor="w")
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(fill="x", expand=True, padx=5, pady=2)

        ttk.Label(notes_frame, text=self.lang.get('action_plan_label_req', "Piano d'Azione (*):")).pack(anchor="w")
        self.action_text = tk.Text(notes_frame, height=3)
        self.action_text.insert("1.0", self.action_plan_placeholder)
        self.action_text.config(foreground="grey")
        self.action_text.bind("<FocusIn>", self._on_action_plan_focus_in)
        self.action_text.bind("<FocusOut>", self._on_action_plan_focus_out)
        self.action_text.pack(fill="x", expand=True, padx=5, pady=2)

        ttk.Button(main_frame, text=self.lang.get('save_declaration_button', "Salva Dichiarazione"),
                   command=self._save_interruption).grid(row=4, column=3, sticky="e", pady=15)
        self._toggle_time_fields()

    def _load_initial_data(self):
        areas = self.db.fetch_working_areas()
        if areas:
            self.working_areas_data = {a.AreaName: a.WorkingAreaID for a in areas}
            self.wa_combo['values'] = sorted(list(self.working_areas_data.keys()))

        orders = self.db.fetch_production_orders_for_breakdown()
        if orders:
            self.orders_data = {o.OrderNumber: o.IdOrdine for o in orders}
            self.all_order_names = sorted(list(self.orders_data.keys()))
            self.order_combo['values'] = self.all_order_names

        issue_areas = self.db.fetch_issue_areas()
        if issue_areas:
            self.issue_areas_data = {ia.IssueArea: ia.IssueAreaId for ia in issue_areas}
            self.ia_combo['values'] = sorted(list(self.issue_areas_data.keys()))

    def _on_wa_select(self, event=None):
        """Azione eseguita quando si seleziona una Working Area."""
        self.sub_area_var.set('')
        self.sa_combo.config(state="disabled", values=[])
        self._on_sa_select()  # Chiama l'aggiornamento a cascata

        wa_id = self.working_areas_data.get(self.working_area_var.get())
        if not wa_id: return

        sub_areas = self.db.fetch_working_sub_areas(wa_id)
        if sub_areas:
            self.sub_areas_data = {sa.AreaSubName: sa.WorkingSubAreaID for sa in sub_areas}
            self.sa_combo['values'] = sorted(list(self.sub_areas_data.keys()))
            self.sa_combo.config(state="readonly")

    def _on_sa_select(self, event=None):
        """Azione eseguita quando si seleziona una Sub Area."""
        self.line_var.set('')
        self.line_combo.config(state="disabled", values=[])

        wa_id = self.working_areas_data.get(self.working_area_var.get())
        sa_id = self.sub_areas_data.get(self.sub_area_var.get())

        # Aggiorna i problemi PRIMA, perché non dipende dalla linea
        self._update_problems_combo()

        if not wa_id or not sa_id: return

        lines = self.db.fetch_working_lines(wa_id, sa_id)
        if lines:
            self.lines_data = {l.WorkingLineName: l.WorkingLineID for l in lines}
            self.line_combo['values'] = sorted(list(self.lines_data.keys()))
            self.line_combo.config(state="readonly")

    def _filter_order_combo(self, event):
        typed_text = self.order_var.get().lower()
        if not typed_text:
            self.order_combo['values'] = self.all_order_names
            return
        filtered_list = [name for name in self.all_order_names if typed_text in name.lower()]
        self.order_combo['values'] = filtered_list

    def _update_problems_combo(self):
        """Funzione centrale per aggiornare il combobox Evento/Problema."""
        print("\n--- DEBUG: Avvio aggiornamento combo Problemi ---")
        self.problem_var.set('')

        wa_id = self.working_areas_data.get(self.working_area_var.get())
        sa_id = self.sub_areas_data.get(self.sub_area_var.get())
        ia_id = self.issue_areas_data.get(self.issue_area_var.get())

        print(f"--- DEBUG: ID -> WA_ID: {wa_id}, SA_ID: {sa_id}, IA_ID: {ia_id} ---")

        # Attiva il combo IN OGNI CASO, anche se vuoto
        self.problem_combo.config(state="readonly")
        print("--- DEBUG: Combo Problemi ATTIVATO. ---")

        if not all([wa_id, sa_id, ia_id]):
            self.problem_combo['values'] = []
            print("--- DEBUG: ID mancanti, il combo problemi sarà vuoto. ---")
            return

        problems = self.db.fetch_issue_problems(wa_id, ia_id, sa_id)
        print(f"--- DEBUG: Trovati {len(problems)} problemi dal DB. ---")
        if problems:
            self.problems_data = {p.IssueDescription: p.IssueProblemId for p in problems}
            self.problem_combo['values'] = sorted(list(self.problems_data.keys()))
        else:
            self.problem_combo['values'] = [self.lang.get('no_problems_found', "Nessun problema trovato")]

    def _on_comments_focus_in(self, event):
        """Chiamato quando l'utente clicca nel campo Commenti."""
        if self.notes_text.get("1.0", "end-1c") == self.comments_placeholder:
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.config(foreground="black")

    def _on_comments_focus_out(self, event):
        """Chiamato quando l'utente lascia il campo Commenti."""
        if not self.notes_text.get("1.0", "end-1c"):
            self.notes_text.insert("1.0", self.comments_placeholder)
            self.notes_text.config(foreground="grey")

    def _toggle_time_fields(self):
        if self.time_choice_var.get() == "duration":
            self.duration_entry.config(state="normal")
            self.from_entry.config(state="disabled")
            self.to_entry.config(state="disabled")
        else:  # "range"
            self.duration_entry.config(state="disabled")
            self.from_entry.config(state="normal")
            self.to_entry.config(state="normal")

    def _calculate_duration(self, event=None):
        try:
            start = datetime.strptime(self.from_hour_var.get(), "%H:%M")
            end = datetime.strptime(self.to_hour_var.get(), "%H:%M")
            if end < start:
                end += timedelta(days=1)
            duration = end - start
            self.duration_var.set(str(int(duration.total_seconds() / 60)))
        except ValueError:
            self.duration_var.set("")

        # In operations_gui.py, dentro la classe AddInterruptionWindow

        def _update_problems_combo(self):
            print("\n" + "=" * 20)
            print("--- DEBUG: Avvio di _update_problems_combo ---")

            # Pulisce lo stato precedente
            self.problem_var.set('')
            self.problem_combo.config(state="disabled", values=[])

            try:
                wa_id = self.working_areas_data.get(self.working_area_var.get())
                sa_id = self.sub_areas_data.get(self.sub_area_var.get())
                ia_id = self.issue_areas_data.get(self.issue_area_var.get())

                print(f"--- DEBUG: ID per la query -> WA_ID: {wa_id}, SA_ID: {sa_id}, IA_ID: {ia_id} ---")

                if not all([wa_id, sa_id, ia_id]):
                    print("--- DEBUG: Uno o più ID necessari sono mancanti. Interrompo la funzione. ---")
                    return

                # Chiama il database
                problems = self.db.fetch_issue_problems(wa_id, ia_id, sa_id)
                print(f"--- DEBUG: Query eseguita. Numero di problemi restituiti: {len(problems)} ---")

                if problems:
                    self.problems_data = {p.IssueDescription: p.IssueProblemId for p in problems}
                    self.problem_combo['values'] = sorted(list(self.problems_data.keys()))
                else:
                    # Se non ci sono problemi, popola con un messaggio informativo
                    no_problems_msg = self.lang.get('no_problems_found', "Nessun problema trovato nel DB")
                    self.problem_combo['values'] = [no_problems_msg]

            finally:
                # --- ATTIVAZIONE INCONDIZIONATA ---
                # Questo comando viene eseguito SEMPRE, anche se non ci sono dati.
                self.problem_combo.config(state="readonly")
                print("--- DEBUG: COMANDO DI ATTIVAZIONE ESEGUITO per il combo Evento/Problema. ---")
                print("=" * 20 + "\n")

    def _on_action_plan_focus_in(self, event):
        if self.action_text.get("1.0", "end-1c") == self.action_plan_placeholder:
            self.action_text.delete("1.0", tk.END)
            self.action_text.config(foreground="black")

    def _on_action_plan_focus_out(self, event):
        if not self.action_text.get("1.0", "end-1c"):
            self.action_text.insert("1.0", self.action_plan_placeholder)
            self.action_text.config(foreground="grey")

    def _save_interruption(self):
        try:
            params = {}
            note_text = self.notes_text.get("1.0", tk.END).strip()
            action_plan_text = self.action_text.get("1.0", tk.END).strip()

            if not note_text or note_text == self.comments_placeholder:
                messagebox.showerror("Dati Mancanti", "Il campo Commenti è obbligatorio.", parent=self)
                return

            if not action_plan_text or action_plan_text == self.action_plan_placeholder:
                messagebox.showerror("Dati Mancanti", "Il campo Piano d'Azione è obbligatorio.", parent=self)
                return

            params['note'] = note_text
            params['action_plan'] = action_plan_text
            params['note'] = self.notes_text.get("1.0", tk.END).strip()
            action_plan_text = self.action_text.get("1.0", tk.END).strip()

            if not params['note'] or not action_plan_text or action_plan_text == self.action_plan_placeholder:
                messagebox.showerror("Dati Mancanti", "I campi Commenti e Piano d'Azione sono obbligatori.",
                                     parent=self)
                return
            params['action_plan'] = action_plan_text

            params['report_date'] = self.date_entry.get_date()
            params['user_name'] = self.user_name
            params['working_area_id'] = self.working_areas_data[self.working_area_var.get()]
            params['sub_area_id'] = self.sub_areas_data[self.sub_area_var.get()]
            params['line_id'] = self.lines_data[self.line_var.get()]
            params['issue_area_id'] = self.issue_areas_data[self.issue_area_var.get()]
            params['problem_id'] = self.problems_data[self.problem_var.get()]

            if self.time_choice_var.get() == "duration":
                params['lost_gain'] = int(self.duration_var.get())
                params['from_hour'] = None
                params['to_hour'] = None
            else:
                self._calculate_duration(None)
                params['lost_gain'] = int(self.duration_var.get())
                params['from_hour'] = self.from_hour_var.get()
                params['to_hour'] = self.to_hour_var.get()

            order_name = self.order_var.get()
            params['po_number'] = order_name.split(' ')[0] if order_name and ' [' in order_name else order_name
            params['product_code'] = order_name.split('[')[1].replace(']',
                                                                      '') if order_name and '[' in order_name else None
            params['hours'] = round(params['lost_gain'] / 60.0, 2)

            success, msg = self.db.add_production_interruption(params)

            if success:
                messagebox.showinfo("Successo", msg, parent=self)
                self.destroy()
            else:
                messagebox.showerror("Errore", msg, parent=self)

        except (KeyError, ValueError) as e:
            messagebox.showerror("Dati Mancanti o non Validi",
                                 f"Assicurati che tutti i campi obbligatori (*) siano compilati correttamente.\n\nDettaglio: {e}",
                                 parent=self)


def open_add_interruption_window(parent, db, lang, user_name):
    AddInterruptionWindow(parent, db, lang, user_name)