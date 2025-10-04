# assign_submissions_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import utils

def open_assign_submissions(parent, db, lang):
    AssignSubmissionWindow(parent, db, lang)

class AssignSubmissionWindow(tk.Toplevel):
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(lang.get('assign_submission_title', 'Assegna Segnalazione'))
        self.geometry("820x520")
        self.transient(parent)
        self.grab_set()

        # Dati
        self.unassigned_rows = []
        self.submissions_map = {}  # display -> row
        self.employees_map = {}    # display -> (hire_history_id, email)

        # Var
        self.submission_var = tk.StringVar()
        self.employee_var = tk.StringVar()

        self._build_ui()
        self._load_unassigned()

    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(3, weight=1)

        # Combo segnalazioni
        ttk.Label(main, text=self.lang.get('select_submission_label', 'Segnalazione da assegnare:')).grid(row=0, column=0, sticky='w')
        self.submission_combo = ttk.Combobox(main, textvariable=self.submission_var, state='readonly', height=10)
        self.submission_combo.grid(row=0, column=1, sticky='ew', padx=6, pady=4)
        self.submission_combo.bind("<<ComboboxSelected>>", self._on_submission_selected)

        # Dettagli (readonly)
        details_frame = ttk.LabelFrame(main, text=self.lang.get('details_label', 'Dettagli'))
        details_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(8, 6))
        details_frame.columnconfigure(1, weight=1)
        for r in range(4): details_frame.rowconfigure(r, weight=0)
        details_frame.rowconfigure(4, weight=1)

        ttk.Label(details_frame, text="ID:").grid(row=0, column=0, sticky='e', padx=5, pady=3)
        self.lbl_id = ttk.Label(details_frame, text="-"); self.lbl_id.grid(row=0, column=1, sticky='w')

        ttk.Label(details_frame, text=self.lang.get('header_date', 'Data:')).grid(row=0, column=2, sticky='e', padx=5)
        self.lbl_date = ttk.Label(details_frame, text="-"); self.lbl_date.grid(row=0, column=3, sticky='w')

        ttk.Label(details_frame, text=self.lang.get('header_user', 'Segnalato da:')).grid(row=1, column=0, sticky='e', padx=5)
        self.lbl_from = ttk.Label(details_frame, text="-"); self.lbl_from.grid(row=1, column=1, columnspan=3, sticky='w')

        ttk.Label(details_frame, text=self.lang.get('title_label', 'Titolo:')).grid(row=2, column=0, sticky='e', padx=5)
        self.lbl_title = ttk.Label(details_frame, text="-"); self.lbl_title.grid(row=2, column=1, columnspan=3, sticky='w')

        ttk.Label(details_frame, text=self.lang.get('description_label', 'Descrizione:')).grid(row=3, column=0, sticky='ne', padx=5, pady=3)
        self.txt_desc = tk.Text(details_frame, height=5, wrap=tk.WORD)
        self.txt_desc.grid(row=3, column=1, columnspan=3, sticky='nsew', pady=3)
        self.txt_desc.config(state='disabled')

        ttk.Label(details_frame, text="Doc:").grid(row=4, column=0, sticky='e', padx=5)
        self.lbl_doc = ttk.Label(details_frame, text="-"); self.lbl_doc.grid(row=4, column=1, sticky='w')
        ttk.Label(details_frame, text="Stato:").grid(row=4, column=2, sticky='e', padx=5)
        self.lbl_state = ttk.Label(details_frame, text="-"); self.lbl_state.grid(row=4, column=3, sticky='w')

        # Combo assegnatario
        ttk.Label(main, text=self.lang.get('assign_to_label', 'Assegna a:')).grid(row=2, column=0, sticky='w', pady=(10, 0))
        self.employee_combo = ttk.Combobox(main, textvariable=self.employee_var, state='disabled')
        self.employee_combo.grid(row=2, column=1, sticky='ew', padx=6, pady=(10, 0))

        # Nota
        ttk.Label(main, text=self.lang.get('notes_label', 'Nota (opzionale):')).grid(row=3, column=0, sticky='nw', pady=(10, 0))
        self.note_text = tk.Text(main, height=4, wrap=tk.WORD)
        self.note_text.grid(row=3, column=1, sticky='nsew', padx=6, pady=(10, 0))

        # Bottoni
        btns = ttk.Frame(main)
        btns.grid(row=4, column=1, sticky='e', pady=10)
        ttk.Button(btns, text=self.lang.get('save_button', 'Salva'), command=self._confirm).pack(side='left', padx=5)
        ttk.Button(btns, text=self.lang.get('cancel_button', 'Annulla'), command=self.destroy).pack(side='left')

    def _load_unassigned(self):
        self.unassigned_rows = self.db.fetch_unassigned_submissions() or []
        self.submissions_map.clear()
        display_values = []

        for r in self.unassigned_rows:
            # r è un dict grazie al metodo sopra
            seg_id = r.get('SegID')
            if seg_id is None:
                continue
            data = r.get('DataSegnalazione', '')
            from_ = r.get('InputFrom', '')
            title = r.get('Titolo', '')
            display = f"[{seg_id}] {data} - {from_} - {title}"
            self.submissions_map[display] = r
            display_values.append(display)

        self.submission_combo['values'] = display_values

    def _on_submission_selected(self, event=None):
        disp = self.submission_var.get()
        r = self.submissions_map.get(disp)
        if not r:
            return

        self.lbl_id.config(text=str(r.get('SegID', '-')))
        self.lbl_date.config(text=str(r.get('DataSegnalazione', '-')))
        self.lbl_from.config(text=str(r.get('InputFrom', '-')))
        self.lbl_title.config(text=str(r.get('Titolo', '-')))

        self.txt_desc.config(state='normal')
        self.txt_desc.delete('1.0', tk.END)
        self.txt_desc.insert('1.0', str(r.get('Descrizione', '') or ''))
        self.txt_desc.config(state='disabled')

        self.lbl_doc.config(text=str(r.get('Documents', '-')))
        self.lbl_state.config(text=f"{r.get('TipoStato', '-')} / {r.get('StatoType', '-')}")

        # Carica e abilita combo dipendenti
        employees = self.db.fetch_assignable_employees() or []
        self.employees_map.clear()
        display_values = []
        for e in employees:
            # pyodbc row: 0=id, 1=nome, 2=email (come da query fornita)
            try:
                eid = getattr(e, 'EmployeeHireHistoryId', e[0])
                name = getattr(e, 'Employee', e[1])
                email = getattr(e, 'WorkEmail', e[2])
                eid = int(eid)
            except Exception:
                continue
            display_values.append(name)
            self.employees_map[name] = {'id': eid, 'email': email}

        self.employee_combo['values'] = display_values
        self.employee_combo.config(state='readonly')
        self.employee_var.set('')

    def _confirm(self):
        disp = (self.submission_var.get() or '').strip()
        emp_display = (self.employee_var.get() or '').strip()
        if not disp:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('warning_select_submission', 'Seleziona una segnalazione.'),
                                   parent=self)
            return
        if not emp_display:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('warning_select_employee', 'Seleziona un assegnatario.'), parent=self)
            return

        r = self.submissions_map.get(disp)
        if not r:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 'Impossibile recuperare i dati della segnalazione.', parent=self)
            return

        seg_id = int(r['SegID'])  # è sicuramente numerico
        seg_date = r.get('DataSegnalazione')
        title = r.get('Titolo', '')
        who = r.get('InputFrom', '')
        reporter_email = r.get('Email')  # email del segnalante

        emp_info = self.employees_map.get(emp_display)
        if not emp_info:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 self.lang.get('error_invalid_employee', 'Assegnatario non valido.'), parent=self)
            return

        emp_id = emp_info['id']
        assignee_email = emp_info['email']
        note = (self.note_text.get('1.0', tk.END) or '').strip()

        ok = self.db.assign_submission(segnalazione_id=seg_id, employee_hire_history_id=emp_id, note=note)
        if not ok:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 self.db.last_error_details or 'Errore salvataggio.', parent=self)
            return

        # Date in dd.mm.yyyy
        from datetime import datetime, date as dtdate
        def fmt_dt(d):
            try:
                if isinstance(d, (datetime, dtdate)):
                    return d.strftime('%d.%m.%Y')
                return str(d)
            except Exception:
                return str(d)

        today_s = fmt_dt(datetime.now())
        seg_date_s = fmt_dt(seg_date)

        # Email all’assegnatario
        try:
            if assignee_email:
                subject = f"New assignment - Submission [{seg_id}]"
                body = (
                    "Hello,\n\n"
                    "You have been assigned a new submission.\n\n"
                    f"Submission ID: {seg_id}\n"
                    f"Title: {title}\n"
                    f"Input from: {who}\n"
                    f"Note: {note or '-'}\n\n"
                    "Regards,\nSystem"
                )
                utils.send_email(recipients=[assignee_email], subject=subject, body=body)
        except Exception as e:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   f"Operazione registrata ma invio email all'assegnatario fallito:\n{e}", parent=self)

        # Email al segnalante (testo richiesto)
        try:
            if reporter_email:
                subject2 = f"Conferma presa in carico segnalazione [{seg_id}]"
                body2 = (
                    "Gentile utente,\n\n"
                    f"La sua segnalazione del {seg_date_s} con titolo \"{title}\" "
                    f"è stata presa in carico in data {today_s} dalla persona a cui è stata assegnata "
                    f"({emp_display}).\n"
                    "Sarà informato sulle decisioni che saranno prese.\n\n"
                    "Cordiali saluti,\nSistema"
                )
                utils.send_email(recipients=[reporter_email], subject=subject2, body=body2)
        except Exception as e:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   f"Operazione registrata ma invio email al segnalante fallito:\n{e}", parent=self)

        messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                            self.lang.get('info_assignment_saved', 'Assegnazione registrata.'), parent=self)
        self.destroy()