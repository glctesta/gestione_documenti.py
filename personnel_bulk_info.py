"""
personnel_bulk_info.py
Form per inviare email di informazione bulk al personale.

Carica i dipendenti attivi con credenziali ERP dalla query condivisa e permette
di selezionare i destinatari, modificare oggetto e corpo dell'email e inviarla.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)

QUERY_EMPLOYEES = """
SELECT 
    UPPER(e.EmployeeName + ' ' + e.employeesurname) AS [NAME],
    k.nomeuser AS userid,
    k.Pass AS PasswordERP,
    IIF(LEN(ISNULL(a.workemail, '')) = 0, a.email, a.workemail) AS Email,
    co.CdcDescription AS CdcDescription
FROM Employee.dbo.employees e
INNER JOIN Employee.dbo.employeehirehistory h
    ON e.employeeid = h.employeeid
    AND h.employeerid = 2
    AND h.EndWorkDate IS NULL
INNER JOIN Employee.dbo.EmployeeCdcStories ec
    ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
    AND ec.dateout IS NULL
INNER JOIN Employee.dbo.functions f
    ON ec.FunctionId = f.FunctionId
INNER JOIN Employee.dbo.CodeCores AS cc
    ON cc.CodeCoresId = h.CodeCoresId
INNER JOIN Employee.dbo.employeers er
    ON er.EmployeerId = h.EmployeerId
INNER JOIN Employee.dbo.CdcSub sc
    ON ec.SubCdcId = sc.SubCdcId
INNER JOIN Employee.dbo.CostCenters co
    ON co.CdcId = sc.CdcId
LEFT JOIN ResetServices.dbo.tbuserkey k
    ON h.EmployeeId = k.IdAnga
LEFT JOIN Employee.dbo.employeeaddress A
    ON a.EmployeeId = e.EmployeeId
    AND a.dateout IS NULL
WHERE NOT k.NomeUser IS NULL
ORDER BY co.CdcDescription, UPPER(e.EmployeeName + ' ' + e.employeesurname)
"""


class PersonnelBulkInfoWindow(tk.Toplevel):
    """Finestra per invio email bulk al personale."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.employees = []
        self.selected = set()

        self.title(lang.get('personnel_bulk_info_title', 'Informazioni BULK'))
        self.geometry("950x700")
        self.resizable(True, True)
        self.minsize(800, 550)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_employees()

    # ═══════════════════════════════════════════════════════════════════════
    #  UI
    # ═══════════════════════════════════════════════════════════════════════
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)
        main.rowconfigure(1, weight=1)
        main.columnconfigure(0, weight=1)

        ttk.Label(
            main,
            text=self.lang.get('personnel_bulk_info_header', 'Invio informazioni al personale'),
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Selezione rapida
        sel_frame = ttk.Frame(main)
        sel_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(
            sel_frame,
            text=self.lang.get('select_all', 'Seleziona tutti'),
            command=self._select_all
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            sel_frame,
            text=self.lang.get('deselect_all', 'Deseleziona tutti'),
            command=self._deselect_all
        ).pack(side="left", padx=(0, 5))
        self.count_var = tk.StringVar(value="0 / 0 selezionati")
        ttk.Label(sel_frame, textvariable=self.count_var).pack(side="right")

        # Tabella dipendenti
        tree_frame = ttk.Frame(main)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        cols = ('select', 'name', 'cdc', 'userid', 'password', 'email')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            selectmode='browse'
        )
        self.tree.heading('select', text='')
        self.tree.heading('name', text=self.lang.get('personnel_bulk_info_name', 'Nome'))
        self.tree.heading('cdc', text=self.lang.get('personnel_bulk_info_cdc', 'Centro di costo'))
        self.tree.heading('userid', text=self.lang.get('personnel_bulk_info_userid', 'User ID'))
        self.tree.heading('password', text=self.lang.get('personnel_bulk_info_password', 'Password ERP'))
        self.tree.heading('email', text=self.lang.get('personnel_bulk_info_email', 'Email'))

        self.tree.column('select', width=40, anchor='center')
        self.tree.column('name', width=220)
        self.tree.column('cdc', width=180)
        self.tree.column('userid', width=100)
        self.tree.column('password', width=120)
        self.tree.column('email', width=220)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind('<ButtonRelease-1>', self._on_tree_click)
        self.tree.bind('<space>', self._toggle_selected_key)

        # Email
        email_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('personnel_bulk_info_email', 'Email'),
            padding=10
        )
        email_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        email_frame.columnconfigure(1, weight=1)

        ttk.Label(
            email_frame,
            text=self.lang.get('personnel_bulk_info_subject', 'Oggetto:')
        ).grid(row=0, column=0, sticky="w")
        self.subject_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.subject_var).grid(
            row=0, column=1, sticky="ew", padx=(5, 0)
        )

        ttk.Label(
            email_frame,
            text=self.lang.get('personnel_bulk_info_body', 'Testo:')
        ).grid(row=1, column=0, sticky="nw", pady=(5, 0))
        self.body_text = tk.Text(email_frame, height=8, wrap="word", font=("Segoe UI", 9))
        self.body_text.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(5, 0))

        # Bottoni e stato
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=4, column=0, sticky="ew")
        ttk.Button(
            btn_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side="right", padx=(5, 0))
        ttk.Button(
            btn_frame,
            text=self.lang.get('send', 'Invia'),
            command=self._send
        ).pack(side="right", padx=(5, 0))

        self.status_var = tk.StringVar()
        ttk.Label(main, textvariable=self.status_var, foreground="#555").grid(
            row=5, column=0, sticky="w", pady=(5, 0)
        )

    # ═══════════════════════════════════════════════════════════════════════
    #  Dati
    # ═══════════════════════════════════════════════════════════════════════
    def _load_employees(self):
        self.status_var.set(self.lang.get('loading', 'Caricamento in corso...'))
        self.update_idletasks()

        try:
            if hasattr(self.db, 'fetch_all'):
                rows = self.db.fetch_all(QUERY_EMPLOYEES)
            else:
                self.db._ensure_connection()
                with self.db._lock:
                    self.db.cursor.execute(QUERY_EMPLOYEES)
                    rows = self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Errore caricamento personale: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('personnel_bulk_info_load_error', 'Errore caricamento dipendenti')}:\n{e}",
                parent=self
            )
            self.status_var.set("")
            return

        self.employees = []
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            emp = {
                'name': row[0] or '',
                'userid': row[1] or '',
                'password': row[2] or '',
                'email': row[3] or '',
                'cdc': row[4] if len(row) > 4 else '',
            }
            self.employees.append(emp)
            self.tree.insert('', 'end', values=(
                '☐', emp['name'], emp['cdc'], emp['userid'], emp['password'], emp['email']
            ))

        self.selected = set()
        self._update_count()
        self.status_var.set(
            f"{len(self.employees)} {self.lang.get('personnel_bulk_info_loaded', 'dipendenti caricati')}"
        )

    # ═══════════════════════════════════════════════════════════════════════
    #  Selezione
    # ═══════════════════════════════════════════════════════════════════════
    def _on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != 'cell':
            return
        col = self.tree.identify_column(event.x)
        if col == '#1':  # colonna select
            item = self.tree.identify_row(event.y)
            if item:
                self._toggle_item(item)

    def _toggle_selected_key(self, event=None):
        sel = self.tree.selection()
        if sel:
            self._toggle_item(sel[0])

    def _toggle_item(self, item):
        idx = self.tree.index(item)
        values = list(self.tree.item(item, 'values'))
        if idx in self.selected:
            self.selected.remove(idx)
            values[0] = '☐'
        else:
            self.selected.add(idx)
            values[0] = '☑'
        self.tree.item(item, values=values)
        self._update_count()

    def _select_all(self):
        self.selected = set(range(len(self.employees)))
        for item in self.tree.get_children():
            values = list(self.tree.item(item, 'values'))
            values[0] = '☑'
            self.tree.item(item, values=values)
        self._update_count()

    def _deselect_all(self):
        self.selected = set()
        for item in self.tree.get_children():
            values = list(self.tree.item(item, 'values'))
            values[0] = '☐'
            self.tree.item(item, values=values)
        self._update_count()

    def _update_count(self):
        total = len(self.employees)
        selected = len(self.selected)
        self.count_var.set(
            f"{selected} / {total} {self.lang.get('personnel_bulk_info_selected', 'selezionati')}"
        )

    # ═══════════════════════════════════════════════════════════════════════
    #  Invio email
    # ═══════════════════════════════════════════════════════════════════════
    def _send(self):
        if not self.selected:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('personnel_bulk_info_no_selection', 'Seleziona almeno un destinatario.'),
                parent=self
            )
            return

        subject = self.subject_var.get().strip()
        body = self.body_text.get('1.0', 'end').strip()

        if not subject:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('personnel_bulk_info_no_subject', "Inserisci l'oggetto dell'email."),
                parent=self
            )
            return
        if not body:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('personnel_bulk_info_no_body', "Inserisci il testo dell'email."),
                parent=self
            )
            return

        recipients = [
            self.employees[i]['email']
            for i in self.selected
            if self.employees[i].get('email')
        ]
        if not recipients:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('personnel_bulk_info_no_emails',
                              "Nessun indirizzo email valido tra i selezionati."),
                parent=self
            )
            return

        self.status_var.set(self.lang.get('sending', 'Invio in corso...'))
        self.update_idletasks()

        try:
            from email_connector import EmailSender
            sender = EmailSender()
            sender.send_email(
                to_email='; '.join(recipients),
                subject=subject,
                body=body,
                is_html=False
            )
            logger.info(
                f"Email bulk inviata da {self.user_name} a {len(recipients)} destinatari"
            )
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('personnel_bulk_info_sent',
                              'Email inviata a {0} destinatari.').format(len(recipients)),
                parent=self
            )
            self.status_var.set("")
        except Exception as e:
            logger.error(f"Errore invio email bulk: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('personnel_bulk_info_send_error', 'Errore invio email')}:\n{e}",
                parent=self
            )
            self.status_var.set("")


def open_personnel_bulk_info(master, db, lang, user_name):
    """Entry-point richiamabile da main.py."""
    PersonnelBulkInfoWindow(master, db, lang, user_name)
