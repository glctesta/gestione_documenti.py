# -*- coding: utf-8 -*-
"""
material_rules_gui.py
Form per gestire le regole di prerequisito tra materiali indiretti.

Tabella: dbo.MaterialRules
- MaterialeId   = materiale richiesto
- MustCodeId    = materiale-scoria che deve essere stato consegnato/dichiarato
- DateOut IS NULL -> regola attiva
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)

QUERY_RULES = """
SELECT mr.MaterilRuleId,
       m.MaterialeId          AS MaterialeId,
       m.CodiceMateriale      AS CodiceRichiesto,
       m.DescrizioneMateriale AS DescRichiesto,
       mc.MaterialeId         AS MustCodeId,
       mc.CodiceMateriale     AS CodiceScoria,
       mc.DescrizioneMateriale AS DescScoria
FROM dbo.MaterialRules mr
INNER JOIN ind.Materiali m  ON m.MaterialeId = mr.MaterialeId
INNER JOIN ind.Materiali mc ON mc.MaterialeId = mr.MustCodeId
WHERE mr.DateOut IS NULL
ORDER BY m.CodiceMateriale, mc.CodiceMateriale
"""

QUERY_MATERIALS = """
SELECT MaterialeId, CodiceMateriale, DescrizioneMateriale
FROM ind.Materiali
WHERE IsActive = 1
ORDER BY CodiceMateriale
"""


def open_material_rules_manager(master, db, lang):
    MaterialRulesManager(master, db, lang)


class MaterialRulesManager(tk.Toplevel):
    """Gestione regole scorie/rientri materiali indiretti."""

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.L = self.lang.get

        self.title(self.L('material_rules_title', 'Gestione Regole Materiali'))
        self.geometry("850x620")
        self.resizable(True, True)
        self.minsize(700, 480)
        self.transient(master)
        self.grab_set()

        self._materials = []     # [(MaterialeId, Codice, Descrizione)]
        self._rules = []         # righe caricate
        self._build_ui()
        self._load_materials()
        self._load_rules()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        ttk.Label(main,
                  text=self.L('material_rules_header', 'Definisci quali materiali richiedono una consegna/scoria'),
                  font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Editor nuova regola
        editor = ttk.LabelFrame(main,
                                text=self.L('material_rules_new', 'Nuova regola'),
                                padding=10)
        editor.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        editor.columnconfigure(1, weight=1)
        editor.columnconfigure(3, weight=1)

        ttk.Label(editor, text=self.L('material_rules_requested', 'Materiale richiesto:')).grid(
            row=0, column=0, sticky="w", padx=(0, 6), pady=4)
        self.requested_var = tk.StringVar()
        self.requested_combo = ttk.Combobox(editor, textvariable=self.requested_var, state="normal", width=45)
        self.requested_combo.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=4)
        self.requested_combo.bind('<KeyRelease>', self._on_requested_key)
        self.requested_combo.bind('<<ComboboxSelected>>', self._on_requested_select)

        ttk.Label(editor, text=self.L('material_rules_scrap', 'Materiale scoria richiesto:')).grid(
            row=0, column=2, sticky="w", padx=(0, 6), pady=4)
        self.scrap_var = tk.StringVar()
        self.scrap_combo = ttk.Combobox(editor, textvariable=self.scrap_var, state="normal", width=45)
        self.scrap_combo.grid(row=0, column=3, sticky="ew", pady=4)
        self.scrap_combo.bind('<KeyRelease>', self._on_scrap_key)
        self.scrap_combo.bind('<<ComboboxSelected>>', self._on_scrap_select)

        ttk.Button(editor, text=self.L('material_rules_add', 'Aggiungi regola'),
                   command=self._add_rule).grid(row=1, column=0, columnspan=4, pady=(10, 0))

        # Tabella regole attive
        tree_frame = ttk.Frame(main)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        cols = ('requested_code', 'requested_desc', 'scrap_code', 'scrap_desc')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('requested_code', text=self.L('material_rules_col_req_code', 'Cod. richiesto'))
        self.tree.heading('requested_desc', text=self.L('material_rules_col_req_desc', 'Descrizione'))
        self.tree.heading('scrap_code', text=self.L('material_rules_col_scrap_code', 'Cod. scoria'))
        self.tree.heading('scrap_desc', text=self.L('material_rules_col_scrap_desc', 'Descrizione'))

        self.tree.column('requested_code', width=120)
        self.tree.column('requested_desc', width=220)
        self.tree.column('scrap_code', width=120)
        self.tree.column('scrap_desc', width=220)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Bottoni
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=3, column=0, sticky="ew")
        ttk.Button(btn_frame, text=self.L('material_rules_delete', 'Elimina regola selezionata'),
                   command=self._delete_rule).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text=self.L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side="right")

        self.status_var = tk.StringVar()
        ttk.Label(main, textvariable=self.status_var, foreground="#555").grid(
            row=4, column=0, sticky="w", pady=(5, 0)
        )

    def _load_materials(self):
        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                cur.execute(QUERY_MATERIALS)
                rows = cur.fetchall()
        except Exception as e:
            logger.error(f"Errore caricamento materiali: {e}", exc_info=True)
            messagebox.showerror(self.L('error', 'Errore'),
                                 f"{self.L('material_rules_load_err', 'Errore caricamento materiali')}:\n{e}",
                                 parent=self)
            rows = []

        self._materials = []
        display = []
        for r in rows:
            mid = r[0]
            code = r[1] or ''
            desc = r[2] or ''
            text = f"{code} - {desc}"
            self._materials.append((mid, code, desc, text))
            display.append(text)

        self.requested_combo['values'] = display
        self.scrap_combo['values'] = display

    def _on_requested_key(self, event=None):
        self._filter_combo(self.requested_combo, self.requested_var)

    def _on_scrap_key(self, event=None):
        self._filter_combo(self.scrap_combo, self.scrap_var)

    def _filter_combo(self, combo, var):
        """Filtra i materiali del combobox per codice o descrizione parziali."""
        text = var.get().strip().lower()
        if not text:
            combo['values'] = [m[3] for m in self._materials]
            return
        filtered = [
            m[3] for m in self._materials
            if text in m[1].lower() or text in m[2].lower()
        ]
        combo['values'] = filtered

    def _on_requested_select(self, event=None):
        self.requested_var.set(self.requested_combo.get())

    def _on_scrap_select(self, event=None):
        self.scrap_var.set(self.scrap_combo.get())

    def _load_rules(self):
        self.status_var.set(self.L('loading', 'Caricamento in corso...'))
        self.update_idletasks()

        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                cur.execute(QUERY_RULES)
                rows = cur.fetchall()
        except Exception as e:
            logger.error(f"Errore caricamento regole: {e}", exc_info=True)
            messagebox.showerror(self.L('error', 'Errore'),
                                 f"{self.L('material_rules_load_err', 'Errore caricamento regole')}:\n{e}",
                                 parent=self)
            rows = []

        self._rules = []
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            rule = {
                'rule_id': r[0],
                'materiale_id': r[1],
                'codice_richiesto': r[2] or '',
                'desc_richiesto': r[3] or '',
                'must_code_id': r[4],
                'codice_scoria': r[5] or '',
                'desc_scoria': r[6] or '',
            }
            self._rules.append(rule)
            self.tree.insert('', 'end', iid=str(rule['rule_id']), values=(
                rule['codice_richiesto'], rule['desc_richiesto'],
                rule['codice_scoria'], rule['desc_scoria']
            ))

        self.status_var.set(
            f"{len(self._rules)} {self.L('material_rules_loaded', 'regole attive')}"
        )

    def _get_selected_material(self, combo_var):
        text = combo_var.get()
        if not text:
            return None
        for item in self._materials:
            if item[3] == text:
                return item[0]
        return None

    def _add_rule(self):
        requested_id = self._get_selected_material(self.requested_var)
        scrap_id = self._get_selected_material(self.scrap_var)

        if not requested_id:
            messagebox.showwarning(self.L('warning', 'Attenzione'),
                                    self.L('material_rules_select_requested', 'Seleziona il materiale richiesto.'),
                                    parent=self)
            return
        if not scrap_id:
            messagebox.showwarning(self.L('warning', 'Attenzione'),
                                    self.L('material_rules_select_scrap', 'Seleziona il materiale scoria richiesto.'),
                                    parent=self)
            return
        # Verifica regola già attiva per lo stesso MaterialeId
        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                cur.execute(
                    "SELECT COUNT(*) FROM dbo.MaterialRules "
                    "WHERE MaterialeId = ? AND DateOut IS NULL",
                    (requested_id,)
                )
                existing = cur.fetchone()[0]
                if existing:
                    messagebox.showwarning(
                        self.L('warning', 'Attenzione'),
                        self.L('material_rules_exists', 'Esiste già una regola attiva per questo materiale.'),
                        parent=self
                    )
                    return

                cur.execute(
                    "INSERT INTO dbo.MaterialRules (MaterialeId, MustCodeId, DateIn) VALUES (?, ?, GETDATE())",
                    (requested_id, scrap_id)
                )
                self.db.conn.commit()
        except Exception as e:
            logger.error(f"Errore inserimento regola: {e}", exc_info=True)
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            messagebox.showerror(self.L('error', 'Errore'),
                                 f"{self.L('material_rules_add_err', 'Errore inserimento regola')}:\n{e}",
                                 parent=self)
            return

        self.requested_var.set('')
        self.scrap_var.set('')
        self._load_rules()

    def _delete_rule(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.L('warning', 'Attenzione'),
                                    self.L('material_rules_select_delete', 'Seleziona una regola da eliminare.'),
                                    parent=self)
            return

        rule_id = int(sel[0])
        if not messagebox.askyesno(
            self.L('confirm', 'Conferma'),
            self.L('material_rules_confirm_delete', 'Confermi l\'eliminazione della regola selezionata?'),
            parent=self
        ):
            return

        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                cur.execute(
                    "UPDATE dbo.MaterialRules SET DateOut = GETDATE() WHERE MaterilRuleId = ?",
                    (rule_id,)
                )
                self.db.conn.commit()
        except Exception as e:
            logger.error(f"Errore eliminazione regola: {e}", exc_info=True)
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            messagebox.showerror(self.L('error', 'Errore'),
                                 f"{self.L('material_rules_delete_err', 'Errore eliminazione regola')}:\n{e}",
                                 parent=self)
            return

        self._load_rules()
