# -*- coding: utf-8 -*-
"""
touchup_response_gui.py  (menu 2 - Soluzioni adottate)
Il tecnico vede le segnalazioni aperte (NEW/REOPENED), legge il dettaglio e
conferma le azioni intraprese; alla conferma la segnalazione si chiude e viene
registrato il tempo di reazione.
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox

import touchup_logic as tl

logger = logging.getLogger(__name__)


def open_touchup_response(master, db, lang, user_name="Unknown"):
    TouchUpResponseWindow(master, db, lang, user_name)


class TouchUpResponseWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get("ture_title", "Touch-Up - Soluzioni adottate"))
        self.geometry("980x640")
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        top = ttk.Frame(main)
        top.pack(fill="x")
        ttk.Label(top, text=self.lang.get("ture_header", "Segnalazioni aperte"),
                  font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Button(top, text=self.lang.get("btn_refresh", "Aggiorna"), command=self._load).pack(side="right")

        cols = ("id", "stato", "data", "createdby", "esc", "riap")
        self.tree = ttk.Treeview(main, columns=cols, show="headings", height=9, selectmode="browse")
        for c, t, w in (("id", "N.", 60), ("stato", "Stato", 100), ("data", "Creata", 150),
                        ("createdby", "Da", 160), ("esc", "Escalation", 90), ("riap", "Riaperture", 90)):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(fill="x", pady=(6, 8))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.tag_configure("strong", foreground="#c0392b")

        # Dettaglio
        det = ttk.LabelFrame(main, text=self.lang.get("ture_detail", "Dettaglio segnalazione"), padding=8)
        det.pack(fill="both", expand=True)
        self.detail = tk.Text(det, height=10, wrap="word", state="disabled")
        self.detail.pack(fill="both", expand=True)

        # Azioni
        act = ttk.LabelFrame(main, text=self.lang.get("ture_actions", "Azioni intraprese / da intraprendere"), padding=8)
        act.pack(fill="x", pady=(8, 0))
        self.actions_txt = tk.Text(act, height=3, wrap="word")
        self.actions_txt.pack(fill="x")
        bf = ttk.Frame(act)
        bf.pack(fill="x", pady=(6, 0))
        ttk.Button(bf, text=self.lang.get("ture_confirm", "✅ Conferma e chiudi"),
                   command=self._confirm).pack(side="right", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        try:
            for r in tl.list_open_reports(self.db):
                d = r['CreatedAt'].strftime('%d/%m/%Y %H:%M') if r.get('CreatedAt') else ''
                tag = "strong" if (r.get('Status') == 'REOPENED' or (r.get('EscalationLevel') or 0) >= 1) else ""
                self.tree.insert("", tk.END, iid=str(r['TouchUpReportId']),
                                 values=(r['TouchUpReportId'], r.get('Status'), d, r.get('CreatedByUser') or '',
                                         r.get('EscalationLevel'), r.get('ReopenCount')),
                                 tags=(tag,) if tag else ())
        except Exception as e:
            logger.error(f"TouchUp response load: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)

    def _on_select(self, _e=None):
        sel = self.tree.selection()
        self.detail.config(state="normal")
        self.detail.delete("1.0", tk.END)
        if sel:
            try:
                det = tl.get_report_detail(self.db, int(sel[0]))
                rep = det['report']
                lines = [
                    f"Segnalazione N. {rep.get('TouchUpReportId')}  -  Stato: {rep.get('Status')}",
                    f"Creata: {rep.get('CreatedAt')}  da {rep.get('CreatedByUser') or ''}",
                    f"Escalation: {rep.get('EscalationLevel')}   Riaperture: {rep.get('ReopenCount')}",
                    "",
                    "PROBLEMI: " + ", ".join(p['ProblemDescription'] for p in det['problems']),
                    "",
                    "SCHEDE:",
                ]
                for l in det['labels']:
                    lines.append(f"   • {l['LabelCod']}  |  ordine {l['OrderNumber']}  |  {l['ProductCode']}")
                self.detail.insert("1.0", "\n".join(lines))
            except Exception as e:
                self.detail.insert("1.0", f"Errore: {e}")
        self.detail.config(state="disabled")

    def _confirm(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("ture_select", "Seleziona una segnalazione."), parent=self)
            return
        actions = self.actions_txt.get("1.0", tk.END).strip()
        if not actions:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("ture_need_actions", "Inserire le azioni intraprese."), parent=self)
            return
        try:
            ok = tl.mark_response(self.db, int(sel[0]), self.user_name, actions)
        except Exception as e:
            logger.error(f"TouchUp mark_response: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)
            return
        if ok:
            messagebox.showinfo(self.lang.get("success", "Successo"),
                                self.lang.get("ture_closed", "Segnalazione chiusa e tempo di reazione registrato."),
                                parent=self)
            self.actions_txt.delete("1.0", tk.END)
            self._load()
            self.detail.config(state="normal"); self.detail.delete("1.0", tk.END); self.detail.config(state="disabled")
