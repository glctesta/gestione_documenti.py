"""
Modulo per la gestione dei programmi esterni (External IPs).
- ExternalIpsManagerWindow: finestra CRUD sulla tabella Employee.dbo.ExternalIps
- BrowserLauncherWindow:    scelta programma e apertura nel browser
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import logging

logger = logging.getLogger(__name__)


class ExternalIpsManagerWindow(tk.Toplevel):
    """Finestra CRUD per gestire IP/Programmi esterni (Employee.dbo.ExternalIps)."""

    QUERY_ACTIVE = """
        SELECT [ExternalIpID], [ExternalIP], [Port], [ProgramName]
        FROM [Employee].[dbo].[ExternalIps]
        WHERE [DateOut] IS NULL
        ORDER BY [ProgramName]
    """

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(self.lang.get('ext_programs_setup_title', 'SetUp IP - Programmi Esterni'))
        self.geometry('750x500')
        self.resizable(True, True)

        self._create_widgets()
        self._load_data()

        self.transient(parent)
        self.grab_set()

    # ── Widget ──────────────────────────────────────────────────────────
    def _create_widgets(self):
        # Bottoni azione
        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Button(actions, text=self.lang.get('add', 'Aggiungi'),
                   command=self._add).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('edit', 'Modifica'),
                   command=self._edit).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('delete', 'Elimina'),
                   command=self._soft_delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('refresh', 'Aggiorna'),
                   command=self._load_data).pack(side=tk.LEFT, padx=4)

        # Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'IP', 'Port', 'Program'),
            show='headings',
            yscrollcommand=vsb.set
        )
        vsb.config(command=self.tree.yview)

        self.tree.heading('ID', text='ID')
        self.tree.heading('IP', text='IP')
        self.tree.heading('Port', text='Port')
        self.tree.heading('Program', text=self.lang.get('ext_program_name', 'Programma'))

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('IP', width=200)
        self.tree.column('Port', width=80, anchor=tk.CENTER)
        self.tree.column('Program', width=250)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    # ── Dati ────────────────────────────────────────────────────────────
    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.db.cursor.execute(self.QUERY_ACTIVE)
            for row in self.db.cursor.fetchall():
                self.tree.insert('', tk.END, values=(
                    row.ExternalIpID, row.ExternalIP, row.Port, row.ProgramName
                ))
        except Exception as e:
            logger.error(f"Errore caricamento ExternalIps: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_error', 'Errore caricamento')}: {e}",
                parent=self
            )

    # ── CRUD ────────────────────────────────────────────────────────────
    def _add(self):
        dialog = _ExternalIpDialog(self, self.db, self.lang, mode='add')
        self.wait_window(dialog)
        if dialog.result:
            self._load_data()

    def _edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_row', 'Seleziona un record da modificare'),
                parent=self
            )
            return
        vals = self.tree.item(sel[0])['values']
        data = {'ID': vals[0], 'IP': vals[1], 'Port': vals[2], 'Program': vals[3]}
        dialog = _ExternalIpDialog(self, self.db, self.lang, mode='edit', data=data)
        self.wait_window(dialog)
        if dialog.result:
            self._load_data()

    def _soft_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_row', 'Seleziona un record da eliminare'),
                parent=self
            )
            return
        vals = self.tree.item(sel[0])['values']
        rec_id = vals[0]
        program = vals[3]

        if not messagebox.askyesno(
            self.lang.get('confirm_delete', 'Conferma Eliminazione'),
            f"{self.lang.get('ext_confirm_delete', 'Disattivare il programma')} '{program}'?",
            parent=self
        ):
            return

        try:
            self.db.cursor.execute(
                "UPDATE [Employee].[dbo].[ExternalIps] SET [DateOut] = GETDATE() WHERE [ExternalIpID] = ?",
                (rec_id,)
            )
            self.db.conn.commit()
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('ext_deleted_ok', 'Programma disattivato'),
                parent=self
            )
            self._load_data()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


# ═══════════════════════════════════════════════════════════════════════
class _ExternalIpDialog(tk.Toplevel):
    """Dialog per aggiungere / modificare un ExternalIp."""

    def __init__(self, parent, db, lang, mode='add', data=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.mode = mode
        self.data = data
        self.result = False

        title = (self.lang.get('ext_add_title', 'Aggiungi Programma Esterno')
                 if mode == 'add'
                 else self.lang.get('ext_edit_title', 'Modifica Programma Esterno'))
        self.title(title)
        self.geometry('400x220')
        self.resizable(False, False)

        self._create_widgets()
        if mode == 'edit' and data:
            self._populate()

        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        f = ttk.Frame(self, padding=16)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text='IP:').grid(row=0, column=0, sticky=tk.W, pady=4)
        self.ip_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.ip_var, width=30).grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)

        ttk.Label(f, text='Port:').grid(row=1, column=0, sticky=tk.W, pady=4)
        self.port_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.port_var, width=30).grid(row=1, column=1, sticky=tk.EW, padx=6, pady=4)

        ttk.Label(f, text=self.lang.get('ext_program_name', 'Programma:')).grid(row=2, column=0, sticky=tk.W, pady=4)
        self.prog_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.prog_var, width=30).grid(row=2, column=1, sticky=tk.EW, padx=6, pady=4)

        btn = ttk.Frame(f)
        btn.grid(row=3, column=0, columnspan=2, pady=16)
        ttk.Button(btn, text=self.lang.get('save', 'Salva'), command=self._save).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn, text=self.lang.get('cancel', 'Annulla'), command=self.destroy).pack(side=tk.LEFT, padx=6)

        f.columnconfigure(1, weight=1)

    def _populate(self):
        self.ip_var.set(self.data['IP'])
        self.port_var.set(self.data['Port'])
        self.prog_var.set(self.data['Program'])

    def _save(self):
        ip = self.ip_var.get().strip()
        port = self.port_var.get().strip()
        prog = self.prog_var.get().strip()

        if not ip or not port or not prog:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_all_fields_required', 'Tutti i campi sono obbligatori'),
                parent=self
            )
            return

        try:
            if self.mode == 'add':
                self.db.cursor.execute(
                    "INSERT INTO [Employee].[dbo].[ExternalIps] ([ExternalIP], [Port], [ProgramName]) VALUES (?, ?, ?)",
                    (ip, port, prog)
                )
            else:
                self.db.cursor.execute(
                    "UPDATE [Employee].[dbo].[ExternalIps] SET [ExternalIP]=?, [Port]=?, [ProgramName]=? WHERE [ExternalIpID]=?",
                    (ip, port, prog, self.data['ID'])
                )
            self.db.conn.commit()
            self.result = True
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('ext_saved_ok', 'Salvato con successo'),
                parent=self
            )
            self.destroy()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


# ═══════════════════════════════════════════════════════════════════════
class BrowserLauncherWindow(tk.Toplevel):
    """Finestra per selezionare un programma esterno e aprirlo nel browser."""

    QUERY_ACTIVE = """
        SELECT [ExternalIpID], [ExternalIP], [Port], [ProgramName]
        FROM [Employee].[dbo].[ExternalIps]
        WHERE [DateOut] IS NULL
        ORDER BY [ProgramName]
    """

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.programs = []  # lista di dict

        self.title(self.lang.get('ext_browser_title', 'Apri Programma Esterno'))
        self.geometry('450x180')
        self.resizable(False, False)

        self._create_widgets()
        self._load_programs()

        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        f = ttk.Frame(self, padding=20)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            f,
            text=self.lang.get('ext_select_program', 'Seleziona un programma:'),
            font=('Helvetica', 10)
        ).pack(anchor=tk.W, pady=(0, 8))

        self.combo_var = tk.StringVar()
        self.combo = ttk.Combobox(f, textvariable=self.combo_var, state='readonly', width=50)
        self.combo.pack(fill=tk.X, pady=(0, 16))

        btn_frame = ttk.Frame(f)
        btn_frame.pack()

        ttk.Button(
            btn_frame,
            text=self.lang.get('ext_open_browser_btn', '🌐 Apri nel Browser'),
            command=self._open_browser
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            btn_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.LEFT, padx=6)

    def _load_programs(self):
        try:
            self.db.cursor.execute(self.QUERY_ACTIVE)
            self.programs = []
            display_values = []
            for row in self.db.cursor.fetchall():
                entry = {
                    'id': row.ExternalIpID,
                    'ip': row.ExternalIP,
                    'port': row.Port,
                    'name': row.ProgramName
                }
                self.programs.append(entry)
                display_values.append(row.ProgramName)
            self.combo['values'] = display_values
            if display_values:
                self.combo.current(0)
        except Exception as e:
            logger.error(f"Errore caricamento programmi: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _open_browser(self):
        idx = self.combo.current()
        if idx < 0 or not self.programs:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_program', 'Seleziona un programma'),
                parent=self
            )
            return

        prog = self.programs[idx]
        url = f"http://{prog['ip']}:{prog['port']}"
        logger.info(f"Apertura browser: {url} ({prog['name']})")
        webbrowser.open(url)


# ═══════════════════════════════════════════════════════════════════════
# Entry-point richiamati da main.py
# ═══════════════════════════════════════════════════════════════════════
def open_external_ips_manager(parent, db, lang):
    """Apre la finestra di gestione IP esterni (SetUp IP)."""
    ExternalIpsManagerWindow(parent, db, lang)


def open_browser_launcher(parent, db, lang):
    """Apre la finestra per selezionare e aprire un programma nel browser."""
    BrowserLauncherWindow(parent, db, lang)
