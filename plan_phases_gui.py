# -*- coding: utf-8 -*-
"""
plan_phases_gui.py — Selezione delle fasi del piano da osservare/giustificare.

Maschera (login autorizzato, chiave 'fasi_da_giustificare_mancata_produzione')
per scegliere SOLO le fasi importanti su cui monitorare il non rispetto del piano.
FCT e PALETIZARE sono forzate (sempre monitorate, non deselezionabili).
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

import plan_phases as pp

logger = logging.getLogger("TraceabilityRS")


def open_plan_phases(parent, db, lang, user_name):
    """Entry-point richiamato da main.py."""
    PlanPhasesWindow(parent, db, lang, user_name)


class PlanPhasesWindow(tk.Toplevel):
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        L = self.lang.get

        self.title(L('plan_phases_title', 'Fasi da giustificare — Piano produzione'))
        self.geometry('640x560')
        self.minsize(520, 440)
        self.transient(parent)
        self.grab_set()

        self._vars = {}   # phase -> BooleanVar
        self._build_ui()
        self._load()

    def _build_ui(self):
        L = self.lang.get

        intro = ttk.Label(self, padding=10, justify='left', foreground='#333',
            text=L('plan_phases_intro',
                   'Seleziona SOLO le fasi importanti su cui osservare e giustificare il\n'
                   'non rispetto del piano. FCT e PALETIZARE sono sempre attive (non\n'
                   'deselezionabili). Le fasi non selezionate non vengono più monitorate.'))
        intro.pack(fill='x')

        # Contenitore scrollabile per le checkbox
        outer = ttk.LabelFrame(self, text=L('plan_phases_list', 'Fasi disponibili'), padding=6)
        outer.pack(fill='both', expand=True, padx=10, pady=(0, 6))
        canvas = tk.Canvas(outer, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient='vertical', command=canvas.yview)
        self.checks_frame = ttk.Frame(canvas)
        self.checks_frame.bind(
            '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.checks_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        # Nota su "versamento a magazzino"
        note = ttk.Label(self, padding=(10, 0), justify='left', foreground='#7A1F1F',
            font=('Arial', 8),
            text=L('plan_phases_note_warehouse',
                   'Nota: il "versamento a magazzino" non è una fase del piano; la quantità\n'
                   'versata si ricava dalla query D365 dedicata (integrazione a parte).'))
        note.pack(fill='x')

        # Footer
        footer = ttk.Frame(self, padding=8)
        footer.pack(fill='x')
        ttk.Button(footer, text=L('plan_phases_all', 'Seleziona tutte'),
                   command=lambda: self._set_all(True)).pack(side='left', padx=3)
        ttk.Button(footer, text=L('plan_phases_none', 'Deseleziona tutte'),
                   command=lambda: self._set_all(False)).pack(side='left', padx=3)
        ttk.Button(footer, text=L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side='right', padx=3)
        ttk.Button(footer, text=L('plan_phases_save', '💾 Salva'),
                   command=self._save).pack(side='right', padx=3)

    def _load(self):
        L = self.lang.get
        for w in self.checks_frame.winfo_children():
            w.destroy()
        self._vars = {}

        all_phases = pp.get_all_plan_phases(self.db.conn)
        configured = pp.is_configured(self.db.conn)
        # Non configurato -> default restrittivo: solo le fasi finali (FCT, FQC)
        selected = (pp.get_selected_phases(self.db.conn) if configured
                    else set(pp.get_final_phases()))
        forced = set(pp.FORCED_PHASES)

        # 2 colonne
        for i, ph in enumerate(all_phases):
            is_forced = ph in forced
            var = tk.BooleanVar(value=(True if is_forced else (ph in selected)))
            self._vars[ph] = var
            label = ph + ('  ★' if is_forced else '')
            cb = ttk.Checkbutton(self.checks_frame, text=label, variable=var)
            if is_forced:
                cb.state(['disabled', 'selected'])
            cb.grid(row=i // 2, column=i % 2, sticky='w', padx=8, pady=2)

    def _set_all(self, value: bool):
        for ph, var in self._vars.items():
            if ph in pp.FORCED_PHASES:
                continue  # i forzati restano attivi
            var.set(value)

    def _save(self):
        L = self.lang.get
        chosen = [ph for ph, var in self._vars.items() if var.get()]
        # i forzati sono comunque aggiunti da save_selection
        if pp.save_selection(self.db.conn, chosen, self.user_name):
            monitored = pp.get_monitored_phases(self.db.conn) or []
            messagebox.showinfo(
                L('success', 'OK'),
                L('plan_phases_saved',
                  'Salvato. Fasi monitorate ({n}):\n{lst}').format(
                    n=len(monitored), lst=', '.join(monitored)),
                parent=self)
        else:
            messagebox.showerror(L('error', 'Errore'),
                                 L('plan_phases_save_err', 'Impossibile salvare la selezione.'),
                                 parent=self)
