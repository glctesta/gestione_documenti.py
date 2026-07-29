# -*- coding: utf-8 -*-
"""
kit_column_mapping_gui.py — Maschera di mappatura colonne per i file di kitting.

Si apre quando `parse_essegi_file` solleva UnmappedColumnsError (un file con
intestazioni non ancora nel dizionario). Propone, per ogni campo mancante,
l'intestazione più simile trovata nel file e permette di confermarla/correggerla;
la scelta viene salvata come alias in dbo.KitColumnAliases, così il sistema
riconoscerà quel formato anche in futuro.

Gira con lo stesso livello di login di chi ha aperto la pagina di kitting
(nessun login aggiuntivo: è una finestra modale della pagina già autorizzata).
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

import kit_column_dict as kcd

logger = logging.getLogger("PlanMonitor")


def open_column_mapping(parent, db, lang, error, file_name, user_name) -> bool:
    """Apre la maschera modale. Ritorna True se l'operatore ha salvato la mappatura."""
    dlg = ColumnMappingDialog(parent, db, lang, error, file_name, user_name)
    parent.wait_window(dlg)
    return bool(getattr(dlg, 'saved', False))


class ColumnMappingDialog(tk.Toplevel):
    def __init__(self, parent, db, lang, error, file_name, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.error = error
        self.file_name = file_name
        self.user_name = user_name or 'Unknown'
        self.saved = False
        L = self.lang.get

        self.title(L('kcm_title', 'Mappatura colonne kitting'))
        self.geometry('660x460')
        self.transient(parent)
        self.grab_set()

        # Valori di intestazione disponibili nel file (col, valore)
        self._header_values = [v for _c, v in (error.header or [])]
        self._combos = {}   # field -> combobox

        self._build_ui()

    def _build_ui(self):
        L = self.lang.get
        pad = ttk.Frame(self, padding=12)
        pad.pack(fill='both', expand=True)

        ttk.Label(pad, justify='left', foreground='#333',
            text=L('kcm_intro',
                   'Il file «{f}» contiene colonne non ancora riconosciute.\n'
                   'Associa i campi mancanti all\'intestazione corretta presente nel file.\n'
                   'Le scelte vengono aggiunte al dizionario e riusate per i prossimi file.')
                   .format(f=self.file_name)).pack(anchor='w', pady=(0, 10))

        # Campi già riconosciuti (contesto)
        if self.error.found:
            found_txt = ', '.join(kcd.FIELD_LABELS.get(f, f) for f in self.error.found)
            ttk.Label(pad, foreground='#0a7d28',
                text=L('kcm_found', 'Già riconosciuti: {x}').format(x=found_txt)).pack(anchor='w', pady=(0, 8))

        box = ttk.LabelFrame(pad, text=L('kcm_missing', 'Campi da associare'), padding=10)
        box.pack(fill='x')

        for i, field in enumerate(self.error.missing):
            label = kcd.FIELD_LABELS.get(field, field)
            sug = (self.error.suggestions or {}).get(field, {})
            suggestion = sug.get('suggestion')
            ratio = sug.get('ratio')

            ttk.Label(box, text=label + ':', font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky='w', padx=(0, 8), pady=6)
            var = tk.StringVar()
            combo = ttk.Combobox(box, textvariable=var, width=34, values=self._header_values)
            if suggestion:
                combo.set(suggestion)
            combo.grid(row=i, column=1, sticky='w', pady=6)
            self._combos[field] = combo

            hint = ''
            if suggestion:
                hint = L('kcm_suggestion', '(proposto: «{s}», somiglianza {r})').format(
                    s=suggestion, r=ratio)
            ttk.Label(box, text=hint, foreground='#888', font=('Arial', 8)).grid(
                row=i, column=2, sticky='w', padx=8)

        ttk.Label(pad, foreground='#7A1F1F', font=('Arial', 8), justify='left',
            text=L('kcm_note',
                   'Nota: scegli l\'intestazione ESATTA come appare nel file. Se nessuna è '
                   'corretta, annulla e verifica il file.')).pack(anchor='w', pady=(10, 0))

        bar = ttk.Frame(pad)
        bar.pack(fill='x', pady=(12, 0))
        ttk.Button(bar, text=L('kcm_save', '💾 Salva mappatura e riprova'),
                   command=self._save).pack(side='right', padx=3)
        ttk.Button(bar, text=L('btn_cancel', 'Annulla'),
                   command=self._cancel).pack(side='right', padx=3)

    def _save(self):
        L = self.lang.get
        chosen = {}
        for field, combo in self._combos.items():
            val = combo.get().strip()
            if not val:
                messagebox.showwarning(L('warning', 'Attenzione'),
                    L('kcm_pick_all', 'Associa un\'intestazione a tutti i campi mancanti.'),
                    parent=self)
                return
            chosen[field] = val
        # Salva gli alias
        ok = True
        for field, val in chosen.items():
            if not kcd.add_alias(self.db.conn, field, val, self.user_name):
                ok = False
        if not ok:
            messagebox.showerror(L('error', 'Errore'),
                L('kcm_save_err', 'Impossibile salvare uno o più alias.'), parent=self)
            return
        self.saved = True
        self.destroy()

    def _cancel(self):
        self.saved = False
        self.destroy()
