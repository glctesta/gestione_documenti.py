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
            # r: accesso per attributo o indice (pyodbc)
            seg_id = getattr(r, 'SegnalazioneId', r[0])
            data = getattr(r, 'DataSegnalazione', r[1])
            from_ = getattr(r, 'InputFrom', r[2])
            title = getattr(r, 'Titolo', r[3])
            display = f"[{seg_id}] {data} - {from_} - {title}"
            self.submissions_map[display] = r
            display_values.append(display)
        self.submission_combo['values'] = display_values

    def _on_submission_selected(self, event=None):
        disp = self.submission_var.get()
        row = self.submissions_map.get(disp)
        if not row:
            return
        # Popola dettagli
        get = lambda name, idx: getattr(row, name, row[idx]) if row is not None else ''
        self.lbl_id.config(text=str(get('SegnalazioneId', 0)))
        self.lbl_date.config(text=str(get('DataSegnalazione', 1)))
        self.lbl_from.config(text=str(get('InputFrom', 2)))
        self.lbl_title.config(text=str(get('Titolo', 3)))

        self.txt_desc.config(state='normal'); self.txt_desc.delete('1.0', tk.END)
        self.txt_desc.insert('1.0', str(get('Descrizione', 4) or ''))
        self.txt_desc.config(state='disabled')

        self.lbl_doc.config(text=str(get('Documents', 5)))
        stato = str(get('TipoStato', 6)) + " / " + str(get('StatoType', 7))
        self.lbl_state.config(text=stato)

        # Carica e abilita combo dipendenti
        employees = self.db.fetch_assignable_employees() or []
        self.employees_map.clear()
        self.employee_combo['values'] = [f"{getattr(e, 'Employee', e[1])}" for e in employees]
        for e in employees:
            eid = getattr(e, 'EmployeeHireHistoryId', e[0])
            name = getattr(e, 'Employee', e[1])
            email = getattr(e, 'WorkEmail', e[2])
            self.employees_map[name] = (eid, email)
        self.employee_combo.config(state='readonly')
        self.employee_var.set('')

    def _confirm(self):
        disp = self.submission_var.get().strip()
        emp = self.employee_var.get().strip()
        if not disp:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'), self.lang.get('warning_select_submission', 'Seleziona una segnalazione.'), parent=self)
            return
        if not emp:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'), self.lang.get('warning_select_employee', 'Seleziona un assegnatario.'), parent=self)
            return

        row = self.submissions_map[disp]
        seg_id = getattr(row, 'SegnalazioneId', row[0])
        emp_id, work_email = self.employees_map.get(emp, (None, None))
        if not emp_id:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), self.lang.get('error_invalid_employee', 'Assegnatario non valido.'), parent=self)
            return

        note = self.note_text.get('1.0', tk.END).strip()
        ok = self.db.insert_submission_assignment(segnalazione_id=seg_id, employee_hire_history_id=emp_id, note=note)
        if not ok:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), self.db.last_error_details or 'Errore salvataggio.', parent=self)
            return

        # Invia mail all'assegnatario (usa WorkEmail)
        try:
            recipients = [work_email] if work_email else []
            if recipients:
                subject = f"New assignment - Submission [{seg_id}]"
                title = getattr(row, 'Titolo', row[3])
                who = getattr(row, 'InputFrom', row[2])
                body = (
                    f"Hello,\n\n"
                    f"You have been assigned a new submission.\n\n"
                    f"Submission ID: {seg_id}\n"
                    f"Title: {title}\n"
                    f"Input from: {who}\n"
                    f"Note: {note or '-'}\n\n"
                    f"Regards,\nSystem"
                )
                utils.send_email(recipients=recipients, subject=subject, body=body)
        except Exception as e:
            # Non bloccare l'utente se fallisce la mail: segnala e prosegui
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   f"Operazione registrata ma invio email fallito:\n{e}", parent=self)

        messagebox.showinfo(self.lang.get('success_title', 'Successo'), self.lang.get('info_assignment_saved', 'Assegnazione registrata.'), parent=self)
        self.destroy()