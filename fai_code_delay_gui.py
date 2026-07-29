# -*- coding: utf-8 -*-
"""
fai_code_delay_gui.py — Maschera gestione codici con delay FAI (forno wave).

Permette di gestire l'elenco dei codici che, per modifiche tecniche alle
temperature del forno wave, hanno bisogno di minuti aggiuntivi prima che la
verifica oraria FAI sia considerata scaduta.

Aperta dal bottone nella gestione template FAI, con login autorizzato
(chiave 'aggiungi_codici_per_delay_fai').
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

import fai_code_delay as fcd

logger = logging.getLogger("PlanMonitor")


def open_fai_code_delay(parent, db, lang, user_name):
    """Entry-point richiamato dalla gestione template FAI."""
    FaiCodeDelayWindow(parent, db, lang, user_name)


class FaiCodeDelayWindow(tk.Toplevel):
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        L = self.lang.get

        self.title(L('fcd_title', 'Codici con delay FAI (forno wave)'))
        self.geometry('640x480')
        self.minsize(520, 380)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load()

    def _build_ui(self):
        L = self.lang.get

        ttk.Label(self, padding=(10, 10, 10, 4), justify='left', foreground='#333',
            text=L('fcd_intro',
                   'Codici che, per modifiche alle temperature del forno wave, hanno bisogno\n'
                   'di minuti aggiuntivi prima che la verifica FAI sia considerata scaduta.')
            ).pack(anchor='w')

        # Riga inserimento
        top = ttk.LabelFrame(self, text=L('fcd_add', 'Aggiungi / aggiorna codice'), padding=8)
        top.pack(fill='x', padx=10, pady=(0, 6))
        ttk.Label(top, text=L('fcd_code', 'Codice') + ':').grid(row=0, column=0, sticky='w')
        self.code_var = tk.StringVar()
        code_entry = ttk.Entry(top, textvariable=self.code_var, width=28)
        code_entry.grid(row=0, column=1, padx=(4, 16), sticky='w')
        ttk.Label(top, text=L('fcd_minutes', 'Minuti di delay') + ':').grid(row=0, column=2, sticky='w')
        self.min_var = tk.StringVar(value='30')
        self.min_spin = ttk.Spinbox(top, from_=0, to=100000, width=8,
                                    textvariable=self.min_var, justify='center')
        self.min_spin.grid(row=0, column=3, padx=4, sticky='w')
        ttk.Button(top, text=L('fcd_btn_add', '➕ Aggiungi / Aggiorna'),
                   command=self._add).grid(row=0, column=4, padx=(12, 0))
        code_entry.bind('<Return>', lambda e: self._add())

        # Tabella
        wrap = ttk.Frame(self)
        wrap.pack(fill='both', expand=True, padx=10, pady=4)
        cols = ('code', 'minutes', 'added_by', 'added_date')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        headers = {
            'code':       L('fcd_code', 'Codice'),
            'minutes':    L('fcd_minutes', 'Minuti di delay'),
            'added_by':   L('fcd_added_by', 'Inserito da'),
            'added_date': L('fcd_added_date', 'Data'),
        }
        widths = {'code': 200, 'minutes': 110, 'added_by': 150, 'added_date': 130}
        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c],
                             anchor='center' if c in ('minutes', 'added_date') else 'w')
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='left', fill='y')
        self.tree.bind('<Double-1>', lambda e: self._edit_selected())

        # Footer
        bar = ttk.Frame(self, padding=8)
        bar.pack(fill='x', padx=10)
        ttk.Button(bar, text=L('fcd_btn_remove', '🗑 Rimuovi'),
                   command=self._remove).pack(side='left')
        self.count_var = tk.StringVar(value='')
        ttk.Label(bar, textvariable=self.count_var, foreground='#666').pack(side='left', padx=10)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side='right')

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        rows = fcd.list_codes(self.db.conn)
        for r in rows:
            d = r['added_date'].strftime('%d/%m/%Y %H:%M') if r.get('added_date') else ''
            self.tree.insert('', 'end', iid=r['code'],
                             values=(r['code'], r['minutes'], r.get('added_by') or '', d))
        self.count_var.set(self.lang.get('fcd_count', '{n} codici').format(n=len(rows)))

    def _add(self):
        L = self.lang.get
        code = self.code_var.get().strip()
        if not code:
            messagebox.showinfo(L('info', 'Info'),
                                L('fcd_need_code', 'Inserisci un codice.'), parent=self)
            return
        try:
            minutes = int(self.min_var.get())
            if minutes < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(L('error', 'Errore'),
                                 L('fcd_bad_minutes', 'Minuti non validi (intero ≥ 0).'), parent=self)
            return
        if fcd.upsert_code(self.db.conn, code, minutes, self.user_name):
            self.code_var.set('')
            self._load()
        else:
            messagebox.showerror(L('error', 'Errore'),
                                 L('fcd_save_err', 'Impossibile salvare il codice.'), parent=self)

    def _edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        self.code_var.set(vals[0])
        self.min_var.set(str(vals[1]))

    def _remove(self):
        L = self.lang.get
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(L('info', 'Info'),
                                L('fcd_select', 'Seleziona un codice da rimuovere.'), parent=self)
            return
        code = sel[0]
        if messagebox.askyesno(L('confirm', 'Conferma'),
                               L('fcd_confirm_remove', 'Rimuovere il codice {c}?').format(c=code),
                               parent=self):
            if fcd.remove_code(self.db.conn, code):
                self._load()
