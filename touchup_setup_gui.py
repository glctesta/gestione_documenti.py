# -*- coding: utf-8 -*-
"""
touchup_setup_gui.py  (menu 5 - Gestione)
- Anagrafica problemi (combo del menu 1): nuovo/modifica/disattiva.
- Instradamento problema -> CdcId/SubCdcId (a chi inviare).
- Parametri escalation (minuti no-risposta, soglia giornaliera).
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox

import touchup_logic as tl

logger = logging.getLogger(__name__)


def open_touchup_setup(master, db, lang, user_name="Unknown"):
    TouchUpSetupWindow(master, db, lang, user_name)


class TouchUpSetupWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self._cdc = []
        self._sub = []

        self.title(lang.get("tuset_title", "Touch-Up - Gestione"))
        self.geometry("1040x640")
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_problems()
        self._load_config()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        # ── Problemi (sinistra) ──
        left = ttk.LabelFrame(main, text=self.lang.get("tuset_problems", "Problemi (combo segnalazioni)"), padding=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.pb_tree = ttk.Treeview(left, columns=("id", "code", "desc"), show="headings",
                                    height=16, selectmode="browse")
        self.pb_tree.heading("id", text="ID"); self.pb_tree.column("id", width=0, stretch=False)
        self.pb_tree.heading("code", text=self.lang.get("tuset_code", "Codice")); self.pb_tree.column("code", width=90)
        self.pb_tree.heading("desc", text=self.lang.get("tuset_desc", "Descrizione")); self.pb_tree.column("desc", width=260, anchor="w")
        self.pb_tree.pack(fill="both", expand=True)
        self.pb_tree.bind("<<TreeviewSelect>>", lambda e: self._load_routing())
        pbtn = ttk.Frame(left); pbtn.pack(fill="x", pady=(6, 0))
        ttk.Button(pbtn, text=self.lang.get("tuset_new", "Nuovo"), command=self._new_problem).pack(side="left", padx=3)
        ttk.Button(pbtn, text=self.lang.get("tuset_edit", "Modifica"), command=self._edit_problem).pack(side="left", padx=3)
        ttk.Button(pbtn, text=self.lang.get("tuset_deact", "Disattiva"), command=self._deact_problem).pack(side="left", padx=3)

        # ── Instradamento (destra) ──
        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)
        rt = ttk.LabelFrame(right, text=self.lang.get("tuset_routing", "Instradamento del problema selezionato"), padding=8)
        rt.pack(fill="both", expand=True)
        self.rt_tree = ttk.Treeview(rt, columns=("id", "cdc", "sub"), show="headings", height=8, selectmode="browse")
        self.rt_tree.heading("id", text="ID"); self.rt_tree.column("id", width=0, stretch=False)
        self.rt_tree.heading("cdc", text="CdC"); self.rt_tree.column("cdc", width=200, anchor="w")
        self.rt_tree.heading("sub", text="SubCdC"); self.rt_tree.column("sub", width=220, anchor="w")
        self.rt_tree.pack(fill="both", expand=True)

        addf = ttk.Frame(rt); addf.pack(fill="x", pady=(6, 0))
        ttk.Label(addf, text="CdC:").pack(side="left")
        self.cdc_var = tk.StringVar()
        self.cdc_combo = ttk.Combobox(addf, textvariable=self.cdc_var, state="readonly", width=24)
        self.cdc_combo.pack(side="left", padx=(2, 8))
        self.cdc_combo.bind("<<ComboboxSelected>>", lambda e: self._load_sub())
        ttk.Label(addf, text="SubCdC:").pack(side="left")
        self.sub_var = tk.StringVar()
        self.sub_combo = ttk.Combobox(addf, textvariable=self.sub_var, state="readonly", width=24)
        self.sub_combo.pack(side="left", padx=(2, 8))
        ttk.Button(addf, text=self.lang.get("tuset_add_route", "➕ Aggiungi"), command=self._add_route).pack(side="left", padx=3)
        ttk.Button(addf, text=self.lang.get("tuset_del_route", "Rimuovi"), command=self._del_route).pack(side="left", padx=3)

        # ── Config escalation ──
        cfg = ttk.LabelFrame(right, text=self.lang.get("tuset_cfg", "Parametri escalation"), padding=8)
        cfg.pack(fill="x", pady=(8, 0))
        ttk.Label(cfg, text=self.lang.get("tuset_noresp", "Min. no-risposta → capo:")).grid(row=0, column=0, sticky="w", pady=3)
        self.noresp_var = tk.StringVar()
        ttk.Entry(cfg, textvariable=self.noresp_var, width=8).grid(row=0, column=1, sticky="w", padx=(6, 16))
        ttk.Label(cfg, text=self.lang.get("tuset_daythr", "Soglia ricorrenze/giorno:")).grid(row=0, column=2, sticky="w", pady=3)
        self.daythr_var = tk.StringVar()
        ttk.Entry(cfg, textvariable=self.daythr_var, width=8).grid(row=0, column=3, sticky="w", padx=(6, 16))
        ttk.Button(cfg, text=self.lang.get("save_button", "Salva"), command=self._save_config).grid(row=0, column=4, padx=4)

        self.cdc_combo['values'] = []
        self._cdc = tl.get_cost_centers(self.db)
        self.cdc_combo['values'] = [f"{c['CdcDescription']} ({c['Cdc']})" for c in self._cdc]

        ttk.Button(main, text=self.lang.get("close_button", "Chiudi"), command=self.destroy).pack(side="bottom")

    # ── Problemi ──
    def _load_problems(self):
        self.pb_tree.delete(*self.pb_tree.get_children())
        for p in tl.get_active_problems(self.db):
            self.pb_tree.insert("", tk.END, iid=str(p['TouchUpProblemId']),
                                values=(p['TouchUpProblemId'], p.get('ProblemCode') or '', p['ProblemDescription']))
        self.rt_tree.delete(*self.rt_tree.get_children())

    def _selected_problem_id(self):
        sel = self.pb_tree.selection()
        return int(sel[0]) if sel else None

    def _new_problem(self):
        dlg = _ProblemDialog(self, self.lang)
        self.wait_window(dlg)
        if dlg.result:
            tl.add_problem(self.db, dlg.result[0], dlg.result[1], dlg.result[2])
            self._load_problems()

    def _edit_problem(self):
        pid = self._selected_problem_id()
        if not pid:
            return
        vals = self.pb_tree.item(str(pid))['values']
        dlg = _ProblemDialog(self, self.lang, initial=(vals[1], vals[2]))
        self.wait_window(dlg)
        if dlg.result:
            tl.update_problem(self.db, pid, dlg.result[0], dlg.result[1], dlg.result[2])
            self._load_problems()

    def _deact_problem(self):
        pid = self._selected_problem_id()
        if not pid:
            return
        if messagebox.askyesno(self.lang.get("confirm", "Conferma"),
                               self.lang.get("tuset_confirm_deact", "Disattivare questo problema?"), parent=self):
            tl.deactivate_problem(self.db, pid)
            self._load_problems()

    # ── Instradamento ──
    def _load_routing(self):
        self.rt_tree.delete(*self.rt_tree.get_children())
        pid = self._selected_problem_id()
        if not pid:
            return
        for r in tl.get_routing(self.db, pid):
            self.rt_tree.insert("", tk.END, iid=str(r['TouchUpRoutingId']),
                                values=(r['TouchUpRoutingId'], r.get('CdcDescription') or r['CdcId'],
                                        r.get('SubCdcDescription') or (r['SubCdcId'] if r['SubCdcId'] else '(tutto il CdC)')))

    def _load_sub(self):
        idx = self.cdc_combo.current()
        self.sub_combo.set('')
        self._sub = []
        if idx < 0:
            self.sub_combo['values'] = []
            return
        cdc_id = self._cdc[idx]['CdcId']
        self._sub = tl.get_sub_cost_centers(self.db, cdc_id)
        self.sub_combo['values'] = [self.lang.get("tuset_all_cdc", "(tutto il CdC)")] + \
                                   [f"{s['SubCdcDescription']} ({s['SubCdc']})" for s in self._sub]

    def _add_route(self):
        pid = self._selected_problem_id()
        if not pid:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuset_sel_problem", "Seleziona un problema."), parent=self)
            return
        cidx = self.cdc_combo.current()
        if cidx < 0:
            return
        cdc_id = self._cdc[cidx]['CdcId']
        sidx = self.sub_combo.current()
        sub_id = None
        if sidx > 0:  # 0 = "(tutto il CdC)"
            sub_id = self._sub[sidx - 1]['SubCdcId']
        tl.add_routing(self.db, pid, cdc_id, sub_id)
        self._load_routing()

    def _del_route(self):
        sel = self.rt_tree.selection()
        if not sel:
            return
        tl.remove_routing(self.db, int(sel[0]))
        self._load_routing()

    # ── Config ──
    def _load_config(self):
        cfg = tl.get_config(self.db)
        self.noresp_var.set(str(cfg.get('NoResponseEscalationMinutes', 30)))
        self.daythr_var.set(str(cfg.get('DayRecurrenceThreshold', 3)))

    def _save_config(self):
        try:
            nr = int(self.noresp_var.get().strip())
            dt = int(self.daythr_var.get().strip())
        except ValueError:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuset_cfg_invalid", "Valori non validi."), parent=self)
            return
        tl.set_config(self.db, nr, dt)
        messagebox.showinfo(self.lang.get("info", "Info"),
                            self.lang.get("tuset_cfg_saved", "Parametri salvati."), parent=self)


class _ProblemDialog(tk.Toplevel):
    def __init__(self, parent, lang, initial=None):
        super().__init__(parent)
        self.lang = lang
        self.result = None
        self.title(lang.get("tuset_problem_dlg", "Problema Touch-Up"))
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        frm = ttk.Frame(self, padding=14)
        frm.pack(fill="both", expand=True)
        frm.columnconfigure(1, weight=1)
        ttk.Label(frm, text=self.lang.get("tuset_code", "Codice") + ":").grid(row=0, column=0, sticky="w", pady=5)
        self.code_var = tk.StringVar(value=initial[0] if initial else "")
        ttk.Entry(frm, textvariable=self.code_var, width=20).grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(frm, text=self.lang.get("tuset_desc", "Descrizione") + " *:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_var = tk.StringVar(value=initial[1] if initial else "")
        e = ttk.Entry(frm, textvariable=self.desc_var, width=40)
        e.grid(row=1, column=1, sticky="ew", pady=5)
        e.focus_set()
        btns = ttk.Frame(frm)
        btns.grid(row=2, column=0, columnspan=2, pady=(12, 0), sticky="e")
        ttk.Button(btns, text=lang.get("save_button", "Salva"), command=self._ok).pack(side="left", padx=4)
        ttk.Button(btns, text=lang.get("cancel_button", "Annulla"), command=self.destroy).pack(side="left")

    def _ok(self):
        desc = self.desc_var.get().strip()
        if not desc:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuset_need_desc", "Inserire la descrizione."), parent=self)
            return
        self.result = (self.code_var.get().strip() or None, desc, None)
        self.destroy()
