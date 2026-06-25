# -*- coding: utf-8 -*-
"""
touchup_operator_gui.py  (menu 1 - Problemi rivelati)
L'operatore Touch-Up inserisce uno o piu' LabelCode (verificati) e seleziona
uno o piu' problemi; al salvataggio si crea la segnalazione (che attivera' i
popup sulle postazioni dei reparti instradati).
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox

import touchup_logic as tl

logger = logging.getLogger(__name__)


def open_touchup_operator(master, db, lang, user_name="Unknown"):
    TouchUpOperatorWindow(master, db, lang, user_name)


class TouchUpOperatorWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self._labels = []   # list[dict] verificati

        self.title(lang.get("tuop_title", "Touch-Up - Problemi rivelati"))
        self.geometry("860x620")
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_problems()

    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)
        ttk.Label(main, text=self.lang.get("tuop_header", "Segnalazione problemi schede"),
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 8))

        # LabelCode
        lc = ttk.LabelFrame(main, text=self.lang.get("tuop_labels", "Schede (LabelCode)"), padding=8)
        lc.pack(fill="x")
        row = ttk.Frame(lc)
        row.pack(fill="x")
        ttk.Label(row, text=self.lang.get("tuop_labelcode", "LabelCode:")).pack(side="left")
        self.lc_var = tk.StringVar()
        e = ttk.Entry(row, textvariable=self.lc_var, width=28)
        e.pack(side="left", padx=(4, 6))
        e.bind("<Return>", lambda ev: self._add_label())
        ttk.Button(row, text=self.lang.get("tuop_add_label", "➕ Verifica e aggiungi"),
                   command=self._add_label).pack(side="left", padx=4)
        ttk.Button(row, text=self.lang.get("tuop_remove_label", "Rimuovi selezionata"),
                   command=self._remove_label).pack(side="left", padx=4)

        cols = ("label", "order", "product")
        self.lbl_tree = ttk.Treeview(lc, columns=cols, show="headings", height=6, selectmode="browse")
        for c, t, w in (("label", "LabelCode", 200), ("order", "Ordine", 140), ("product", "Prodotto", 320)):
            self.lbl_tree.heading(c, text=t)
            self.lbl_tree.column(c, width=w, anchor="w")
        self.lbl_tree.pack(fill="x", pady=(6, 0))

        # Problemi
        pf = ttk.LabelFrame(main, text=self.lang.get("tuop_problems", "Problemi rilevati (selezione multipla)"), padding=8)
        pf.pack(fill="both", expand=True, pady=(10, 0))
        self.pb = tk.Listbox(pf, selectmode=tk.MULTIPLE, height=10)
        psb = ttk.Scrollbar(pf, orient="vertical", command=self.pb.yview)
        self.pb.configure(yscrollcommand=psb.set)
        self.pb.pack(side="left", fill="both", expand=True)
        psb.pack(side="right", fill="y")
        self._problems = []

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(10, 0))
        self.status_var = tk.StringVar(value="")
        ttk.Label(bottom, textvariable=self.status_var, foreground="gray").pack(side="left")
        ttk.Button(bottom, text=self.lang.get("tuop_save", "💾 Salva segnalazione"),
                   command=self._save).pack(side="right", padx=4)
        ttk.Button(bottom, text=self.lang.get("close_button", "Chiudi"),
                   command=self.destroy).pack(side="right", padx=4)

    def _load_problems(self):
        self.pb.delete(0, tk.END)
        self._problems = tl.get_active_problems(self.db)
        for p in self._problems:
            self.pb.insert(tk.END, p['ProblemDescription'])

    def _add_label(self):
        code = self.lc_var.get().strip()
        if not code:
            return
        if any(l['LabelCod'] == code for l in self._labels):
            messagebox.showinfo(self.lang.get("info", "Info"),
                                self.lang.get("tuop_dup", "LabelCode già aggiunto."), parent=self)
            return
        info = tl.verify_labelcode(self.db, code)
        if not info:
            messagebox.showerror(self.lang.get("error", "Errore"),
                                 self.lang.get("tuop_lc_notfound", "LabelCode non trovato nel sistema."), parent=self)
            return
        self._labels.append(info)
        self.lbl_tree.insert("", tk.END, iid=code,
                             values=(info['LabelCod'], info['OrderNumber'], info['ProductCode']))
        self.lc_var.set("")

    def _remove_label(self):
        sel = self.lbl_tree.selection()
        if not sel:
            return
        code = sel[0]
        self._labels = [l for l in self._labels if l['LabelCod'] != code]
        self.lbl_tree.delete(code)

    def _save(self):
        if not self._labels:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuop_need_label", "Aggiungi almeno una scheda."), parent=self)
            return
        sel = self.pb.curselection()
        if not sel:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuop_need_problem", "Seleziona almeno un problema."), parent=self)
            return
        problem_ids = [self._problems[i]['TouchUpProblemId'] for i in sel]
        try:
            res = tl.save_report(self.db, self.user_name, self._labels, problem_ids, lang=self.lang)
        except Exception as e:
            logger.error(f"TouchUp save_report: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)
            return
        msg = self.lang.get("tuop_saved", "Segnalazione salvata (N. {0}).").format(res['report_id'])
        if res['status'] == 'REOPENED':
            msg += "\n" + self.lang.get("tuop_reopened", "⚠️ RIAPERTURA: problema già chiuso ripresentato ({0}x).").format(res['reopen_count'])
        elif res['recurrence']:
            msg += "\n" + self.lang.get("tuop_recurrent", "⚠️ Segnalazione RICORRENTE per lo stesso ordine.")
        if res['email_sent']:
            msg += "\n" + self.lang.get("tuop_email", "Email di avviso inviata.")
        messagebox.showinfo(self.lang.get("success", "Successo"), msg, parent=self)
        # reset per una nuova segnalazione
        self._labels = []
        self.lbl_tree.delete(*self.lbl_tree.get_children())
        self.pb.selection_clear(0, tk.END)
        self.status_var.set(self.lang.get("tuop_done", "Pronto per una nuova segnalazione."))
