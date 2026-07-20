"""
NPI Upcoming Tasks Window — Elenco di TUTTI i task NPI in scadenza nei prossimi
N giorni (0-5), per tutti i prodotti. Selezionando una riga si apre la gestione
del progetto/prodotto corrispondente, previo login NPI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NpiUpcomingTasksWindow(tk.Toplevel):
    """Task NPI in scadenza entro N giorni (tutti i prodotti)."""

    COLUMNS = (
        'project_name', 'customer', 'product_code', 'category',
        'task_name', 'owner_name', 'due_date', 'days_left', 'status'
    )
    HEADER_KEYS = {
        'project_name': ('npi_upcoming_col_project', 'Progetto NPI'),
        'customer': ('npi_upcoming_col_customer', 'Cliente'),
        'product_code': ('npi_upcoming_col_product', 'Prodotto'),
        'category': ('npi_upcoming_col_family', 'Famiglia'),
        'task_name': ('npi_upcoming_col_task', 'Task'),
        'owner_name': ('npi_upcoming_col_owner', 'Responsabile'),
        'due_date': ('npi_upcoming_col_due_date', 'Scadenza'),
        'days_left': ('npi_upcoming_col_days_left', 'Giorni'),
        'status': ('npi_upcoming_col_status', 'Stato'),
    }
    COL_WIDTHS = {
        'project_name': 190, 'customer': 130, 'product_code': 110,
        'category': 110, 'task_name': 210, 'owner_name': 140,
        'due_date': 90, 'days_left': 70, 'status': 90,
    }

    def __init__(self, master, npi_manager, lang, on_open_project=None, default_days=5):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self._on_open_project = on_open_project  # callback(project_id, project_name)

        self.HEADERS = {col: self.lang.get(key, default)
                        for col, (key, default) in self.HEADER_KEYS.items()}

        self.title(self.lang.get('npi_upcoming_title', 'NPI — Task in scadenza'))
        self.geometry('1300x660')
        self.transient(master)
        self.grab_set()

        self._all_data = []
        self._sort_col = 'days_left'
        self._sort_reverse = False

        self._days_var = tk.IntVar(value=max(0, min(5, int(default_days))))

        self._build_ui()
        self._load_data()

    # ── UI ──
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        top = ttk.LabelFrame(main, text=self.lang.get('npi_upcoming_filters', 'Filtro scadenze'), padding=8)
        top.pack(fill=tk.X, pady=(0, 6))
        ttk.Label(top, text=self.lang.get('npi_upcoming_days_label',
                                          'Giorni di anticipo (0-5):')).pack(side=tk.LEFT)
        self._spin = ttk.Spinbox(top, from_=0, to=5, width=5, textvariable=self._days_var,
                                 command=self._load_data, state='readonly')
        self._spin.pack(side=tk.LEFT, padx=(6, 12))
        ttk.Button(top, text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
                   command=self._load_data).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, foreground='#555',
                  text=self.lang.get('npi_upcoming_hint',
                                     'Doppio click su una riga per aprire il progetto (con login NPI).')
                  ).pack(side=tk.LEFT, padx=(16, 0))

        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(tree_frame, columns=self.COLUMNS, show='headings',
                                 selectmode='browse', height=22)
        for col in self.COLUMNS:
            self.tree.heading(col, text=self.HEADERS[col], command=lambda c=col: self._on_sort(c))
            anchor = tk.CENTER if col in ('days_left', 'due_date', 'status') else tk.W
            self.tree.column(col, width=self.COL_WIDTHS.get(col, 100), anchor=anchor)
        self.tree.tag_configure('today', foreground='#C0392B', font=('Segoe UI', 9, 'bold'))
        self.tree.tag_configure('soon', foreground='#E67E22')
        self.tree.tag_configure('normal', foreground='#2C3E50')

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.tree.bind('<Double-1>', lambda e: self._open_selected())

        btn = ttk.Frame(main)
        btn.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btn, text=self.lang.get('npi_upcoming_open', '📂 Apri progetto selezionato'),
                   command=self._open_selected).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

        self.status_var = tk.StringVar(value='')
        ttk.Label(main, textvariable=self.status_var, relief='sunken', anchor='w').pack(fill=tk.X, pady=(6, 0))

    # ── Dati ──
    def _load_data(self):
        self.config(cursor='watch')
        self.update_idletasks()
        try:
            days = max(0, min(5, int(self._days_var.get())))
            self._all_data = self.npi_manager.get_all_upcoming_tasks(days_ahead=days)
            self._sort_data()
            self._refresh_tree()
        except Exception as e:
            logger.error(f"Errore caricamento task in scadenza: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('npi_upcoming_load_error', 'Impossibile caricare i task')}:\n{e}",
                parent=self)
        finally:
            self.config(cursor='')

    def _on_sort(self, col):
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        self._sort_data()
        self._refresh_tree()

    def _sort_data(self):
        col = self._sort_col

        def key(item):
            val = item.get(col, '')
            if col == 'days_left':
                return val if isinstance(val, int) else 0
            if col == 'due_date':
                return val or datetime.min
            return str(val).lower()

        self._all_data.sort(key=key, reverse=self._sort_reverse)

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for d in self._all_data:
            due_str = d['due_date'].strftime('%d/%m/%Y') if d['due_date'] else ''
            dl = d.get('days_left', 0)
            tag = 'today' if dl <= 0 else ('soon' if dl <= 2 else 'normal')
            self.tree.insert('', tk.END, values=(
                d['project_name'], d['customer'], d['product_code'], d['category'],
                d['task_name'], d['owner_name'], due_str, dl, d['status']
            ), tags=(tag,))

        for col in self.COLUMNS:
            arrow = ''
            if col == self._sort_col:
                arrow = ' ▼' if self._sort_reverse else ' ▲'
            self.tree.heading(col, text=self.HEADERS[col] + arrow)

        n = len(self._all_data)
        days = self._days_var.get()
        self.status_var.set(
            self.lang.get('npi_upcoming_status', '{0} task in scadenza entro {1} giorni').format(n, days))

    # ── Apertura progetto (con login NPI) ──
    def _open_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('npi_upcoming_select', 'Selezionare un task dalla lista.'), parent=self)
            return
        idx = self.tree.index(sel[0])
        if idx >= len(self._all_data):
            return
        row = self._all_data[idx]
        project_id = row.get('project_id')
        project_name = row.get('project_name', '')
        if not project_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('npi_upcoming_no_project', 'Progetto non individuato per il task selezionato.'),
                parent=self)
            return
        if not callable(self._on_open_project):
            logger.warning("NpiUpcomingTasksWindow: nessun callback on_open_project")
            return
        # Il callback esegue il login NPI e apre la gestione del progetto/prodotto
        self._on_open_project(project_id, project_name)
