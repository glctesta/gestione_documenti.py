# -*- coding: utf-8 -*-
"""
automatic_email_manager_gui.py
Form per la gestione degli invii email automatici centralizzati.

Autorizzazione: gestione_invii_automatici
"""
import importlib
import logging
import tkinter as tk
from tkinter import ttk, messagebox

from email_job_coordinator import (
    load_jobs,
    update_job,
    force_claim_job,
    log_job_run,
    release_job_lock,
)

logger = logging.getLogger(__name__)


def open_automatic_email_manager(master, db, lang):
    AutomaticEmailManagerWindow(master, db, lang)


class AutomaticEmailManagerWindow(tk.Toplevel):
    """Gestione centralizzata degli invii email automatici."""

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.L = self.lang.get
        self.title(self.L('auto_email_manager_title', 'Gestione Invii Automatici'))
        self.geometry("1100x620")
        self.minsize(900, 480)
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._rows = []
        self._build_ui()
        self._load_jobs()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill='both', expand=True)
        main.rowconfigure(2, weight=1)
        main.columnconfigure(0, weight=1)

        ttk.Label(
            main,
            text=self.L('auto_email_manager_header', 'Configurazione invii email/report automatici'),
            font=('Segoe UI', 12, 'bold')
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))

        # Filtro
        filter_frame = ttk.Frame(main)
        filter_frame.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(filter_frame, text=self.L('auto_email_filter', 'Filtra:')).pack(side='left')
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=40)
        filter_entry.pack(side='left', padx=(6, 0))
        self.filter_var.trace_add('write', lambda *_a: self._apply_filter())

        # Treeview
        tree_frame = ttk.Frame(main)
        tree_frame.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        cols = ('job_name', 'display_name', 'timing', 'recipients_key', 'enabled',
                'last_run', 'status')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            selectmode='browse'
        )
        self.tree.heading('job_name', text=self.L('auto_email_col_job', 'Job'))
        self.tree.heading('display_name', text=self.L('auto_email_col_name', 'Nome'))
        self.tree.heading('timing', text=self.L('auto_email_col_timing', 'Timing'))
        self.tree.heading('recipients_key', text=self.L('auto_email_col_recipients', 'Chiave destinatari'))
        self.tree.heading('enabled', text=self.L('auto_email_col_enabled', 'Abilitato'))
        self.tree.heading('last_run', text=self.L('auto_email_col_last_run', 'Ultimo run'))
        self.tree.heading('status', text=self.L('auto_email_col_status', 'Stato'))

        self.tree.column('job_name', width=160, anchor='w')
        self.tree.column('display_name', width=240, anchor='w')
        self.tree.column('timing', width=160, anchor='w')
        self.tree.column('recipients_key', width=150, anchor='w')
        self.tree.column('enabled', width=70, anchor='center')
        self.tree.column('last_run', width=130, anchor='center')
        self.tree.column('status', width=90, anchor='center')

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Bottoni
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=3, column=0, sticky='ew')
        ttk.Button(
            btn_frame,
            text=self.L('btn_edit', 'Modifica'),
            command=self._on_edit
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_force_run', 'Forza esecuzione'),
            command=self._on_force_run
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_refresh', 'Aggiorna'),
            command=self._load_jobs
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_close', 'Chiudi'),
            command=self.destroy
        ).pack(side='right')

        self.status_var = tk.StringVar()
        ttk.Label(main, textvariable=self.status_var, foreground='#555').grid(
            row=4, column=0, sticky='w', pady=(5, 0)
        )

    def _load_jobs(self):
        self.status_var.set(self.L('loading', 'Caricamento in corso...'))
        self.update_idletasks()
        self._rows = load_jobs(self.db)
        self._apply_filter()
        self.status_var.set(
            f"{len(self._rows)} {self.L('auto_email_jobs_loaded', 'job configurati')}"
        )

    def _apply_filter(self):
        text = self.filter_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for rec in self._rows:
            search = ' '.join(str(rec.get(k, '')) for k in (
                'JobName', 'DisplayName', 'Timing', 'RecipientsSettingKey',
                'LastRunStatus', 'Description'
            )).lower()
            if text and text not in search:
                continue
            last_run = ''
            if rec.get('LastRunAt'):
                try:
                    last_run = rec['LastRunAt'].strftime('%d/%m/%Y %H:%M')
                except Exception:
                    last_run = str(rec['LastRunAt'])
            enabled = 'Sì' if rec.get('IsEnabled') else 'No'
            iid = rec['JobName']
            self.tree.insert('', 'end', iid=iid, values=(
                rec.get('JobName', ''),
                rec.get('DisplayName', ''),
                rec.get('Timing', ''),
                rec.get('RecipientsSettingKey', ''),
                enabled,
                last_run,
                rec.get('LastRunStatus', ''),
            ))

    def _selected_job(self):
        sel = self.tree.selection()
        if not sel:
            return None
        job_name = sel[0]
        for rec in self._rows:
            if rec['JobName'] == job_name:
                return rec
        return None

    def _on_edit(self):
        rec = self._selected_job()
        if not rec:
            messagebox.showwarning(
                self.L('warning', 'Attenzione'),
                self.L('auto_email_select_job', 'Seleziona un job da modificare.'),
                parent=self
            )
            return
        EditJobDialog(self, self.db, self.lang, rec, self._load_jobs)

    def _on_force_run(self):
        rec = self._selected_job()
        if not rec:
            messagebox.showwarning(
                self.L('warning', 'Attenzione'),
                self.L('auto_email_select_job', 'Seleziona un job da eseguire.'),
                parent=self
            )
            return
        job_name = rec['JobName']
        display = rec.get('DisplayName', job_name)
        if not messagebox.askyesno(
            self.L('confirm', 'Conferma'),
            self.L('auto_email_force_confirm', "Forzare l'esecuzione di {name}?").replace('{name}', display),
            parent=self
        ):
            return

        if not force_claim_job(self.db, job_name, lock_minutes=10):
            messagebox.showwarning(
                self.L('warning', 'Attenzione'),
                self.L('auto_email_force_disabled', 'Job disabilitato o impossibile acquisire il lock.'),
                parent=self
            )
            return

        try:
            self._execute_job(rec)
        except Exception as e:
            logger.error("Force run fallito per %s: %s", job_name, e, exc_info=True)
            release_job_lock(self.db, job_name)
            log_job_run(self.db, job_name, 'ERROR', f"force run error: {e}")
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('auto_email_force_error', 'Errore esecuzione forzata')}:\n{e}",
                parent=self
            )
        finally:
            self._load_jobs()

    def _execute_job(self, rec):
        """Tenta di eseguire il job importando modulo e funzione configurati."""
        job_name = rec['JobName']
        module_path = rec.get('ModulePath') or ''
        func_name = rec.get('FunctionName') or ''
        module_name = module_path.replace('.py', '') if module_path.endswith('.py') else module_path

        if not module_name or not func_name:
            log_job_run(
                self.db, job_name, 'OK',
                'force run: nessuna funzione automatica configurata'
            )
            messagebox.showinfo(
                self.L('info_title', 'Informazione'),
                self.L('auto_email_force_no_func', 'Lock acquisito. Nessuna funzione automatica configurata per questo job.'),
                parent=self
            )
            return

        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            raise RuntimeError(f"Impossibile importare {module_name}: {e}")

        # Se FunctionName contiene piu' funzioni separate da '/', prova la prima
        first_func = func_name.split('/')[0].strip()
        if not hasattr(mod, first_func):
            raise RuntimeError(f"Funzione {first_func} non trovata in {module_name}")

        func = getattr(mod, first_func)
        result = func(self.db, self.lang)
        msg = f"force run OK: {result}"
        log_job_run(self.db, job_name, 'OK', msg)
        messagebox.showinfo(
            self.L('info_title', 'Informazione'),
            self.L('auto_email_force_ok', 'Esecuzione forzata completata.').replace('{result}', str(result)),
            parent=self
        )


class EditJobDialog(tk.Toplevel):
    """Dialog per modificare un job automatico."""

    def __init__(self, parent, db, lang, rec, on_save_callback):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.L = self.lang.get
        self.rec = rec
        self.on_save_callback = on_save_callback
        self.title(self.L('auto_email_edit_title', 'Modifica job'))
        self.geometry("550x420")
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._populate()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill='both', expand=True)
        main.columnconfigure(1, weight=1)

        r = 0
        ttk.Label(main, text=self.L('auto_email_col_job', 'Job:')).grid(
            row=r, column=0, sticky='w', pady=3)
        ttk.Label(main, text=self.rec.get('JobName', '')).grid(
            row=r, column=1, sticky='w', pady=3)

        r += 1
        ttk.Label(main, text=self.L('auto_email_col_name', 'Nome visualizzato:')).grid(
            row=r, column=0, sticky='w', pady=3)
        self.display_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.display_var).grid(
            row=r, column=1, sticky='ew', pady=3)

        r += 1
        ttk.Label(main, text=self.L('auto_email_col_timing', 'Timing:')).grid(
            row=r, column=0, sticky='w', pady=3)
        self.timing_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.timing_var).grid(
            row=r, column=1, sticky='ew', pady=3)

        r += 1
        ttk.Label(main, text=self.L('auto_email_col_recipients', 'Chiave destinatari (Settings.atribute):')).grid(
            row=r, column=0, sticky='w', pady=3)
        self.recipients_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.recipients_var).grid(
            row=r, column=1, sticky='ew', pady=3)

        r += 1
        ttk.Label(main, text=self.L('auto_email_enabled', 'Abilitato:')).grid(
            row=r, column=0, sticky='w', pady=3)
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main, variable=self.enabled_var, onvalue=True, offvalue=False).grid(
            row=r, column=1, sticky='w', pady=3)

        r += 1
        ttk.Label(main, text=self.L('auto_email_description', 'Descrizione / note:')).grid(
            row=r, column=0, sticky='nw', pady=3)
        self.description_text = tk.Text(main, wrap='word', height=8)
        self.description_text.grid(row=r, column=1, sticky='nsew', pady=3)
        main.rowconfigure(r, weight=1)

        # Bottoni
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=r + 1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        ttk.Button(
            btn_frame,
            text=self.L('btn_save', 'Salva'),
            command=self._on_save
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_cancel', 'Annulla'),
            command=self.destroy
        ).pack(side='right')

    def _populate(self):
        self.display_var.set(self.rec.get('DisplayName', ''))
        self.timing_var.set(self.rec.get('Timing', ''))
        self.recipients_var.set(self.rec.get('RecipientsSettingKey', '') or '')
        self.enabled_var.set(bool(self.rec.get('IsEnabled')))
        self.description_text.delete('1.0', 'end')
        self.description_text.insert('1.0', self.rec.get('Description', '') or '')

    def _on_save(self):
        fields = {
            'DisplayName': self.display_var.get().strip(),
            'Timing': self.timing_var.get().strip(),
            'RecipientsSettingKey': self.recipients_var.get().strip() or None,
            'IsEnabled': 1 if self.enabled_var.get() else 0,
            'Description': self.description_text.get('1.0', 'end').strip(),
        }
        if update_job(self.db, self.rec['JobName'], fields):
            self.destroy()
            self.on_save_callback()
        else:
            messagebox.showerror(
                self.L('error', 'Errore'),
                self.L('auto_email_save_error', 'Errore durante il salvataggio.'),
                parent=self
            )
