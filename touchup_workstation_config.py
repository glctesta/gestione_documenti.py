# -*- coding: utf-8 -*-
"""
touchup_workstation_config.py  (menu 4 - Setup workstation)
Configura il PC corrente come postazione che riceve i popup Touch-Up, e per
quali REPARTI (CdC/SubCdC). Crea/elimina touchup_host.json in %LOCALAPPDATA%.
Stesso pattern di shipment_workstation_config.py / shift handover.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

import touchup_logic as tl

logger = logging.getLogger(__name__)

_LOCALAPPDATA = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
TOUCHUP_HOST_FILE = os.path.join(_LOCALAPPDATA, "touchup_host.json")


def is_touchup_workstation() -> bool:
    return os.path.isfile(TOUCHUP_HOST_FILE)


def get_touchup_departments():
    """Ritorna (cdc_ids, subcdc_ids) della postazione (liste, eventualmente vuote)."""
    if not os.path.isfile(TOUCHUP_HOST_FILE):
        return [], []
    try:
        with open(TOUCHUP_HOST_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return list(data.get("cdc_ids", [])), list(data.get("subcdc_ids", []))
    except Exception:
        return [], []


def open_touchup_workstation_config(master, db, lang, user_name="Unknown"):
    TouchUpWorkstationConfigWindow(master, db, lang, user_name)


class TouchUpWorkstationConfigWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self._rows = []   # [(cdc_id, subcdc_id, label)]

        self.title(lang.get("tuws_title", "Postazione Touch-Up - Setup"))
        self.geometry("620x520")
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_departments()
        self._refresh_status()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=14)
        main.pack(expand=True, fill="both")
        ttk.Label(main, text=self.lang.get("tuws_header", "Reparti che ricevono i popup Touch-Up su questo PC"),
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

        self.status_var = tk.StringVar(value="...")
        ttk.Label(main, textvariable=self.status_var, foreground="#1a5276").pack(anchor="w", pady=(0, 8))

        box = ttk.LabelFrame(main, text=self.lang.get("tuws_select", "Seleziona i reparti (CdC / SubCdC)"), padding=8)
        box.pack(fill="both", expand=True)
        self.lb = tk.Listbox(box, selectmode=tk.MULTIPLE, height=14, activestyle="dotbox")
        sb = ttk.Scrollbar(box, orient="vertical", command=self.lb.yview)
        self.lb.configure(yscrollcommand=sb.set)
        self.lb.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        btns = ttk.Frame(main)
        btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text=self.lang.get("tuws_activate", "✅ Attiva su questo PC"),
                   command=self._activate).pack(side="left", padx=4)
        ttk.Button(btns, text=self.lang.get("tuws_deactivate", "❌ Disattiva"),
                   command=self._deactivate).pack(side="left", padx=4)
        ttk.Button(btns, text=self.lang.get("close_button", "Chiudi"),
                   command=self.destroy).pack(side="right", padx=4)

    def _load_departments(self):
        self.lb.delete(0, tk.END)
        self._rows = []
        try:
            for c in tl.get_cost_centers(self.db):
                for s in tl.get_sub_cost_centers(self.db, c['CdcId']):
                    label = f"{c['CdcDescription']}  ›  {s['SubCdcDescription']}"
                    self._rows.append((c['CdcId'], s['SubCdcId'], label))
                    self.lb.insert(tk.END, label)
        except Exception as e:
            logger.error(f"TouchUp WS load departments: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)
        # preselezione da file
        _, sub_ids = get_touchup_departments()
        if sub_ids:
            for i, (cdc, sub, _l) in enumerate(self._rows):
                if sub in sub_ids:
                    self.lb.selection_set(i)

    def _refresh_status(self):
        if is_touchup_workstation():
            cdc_ids, sub_ids = get_touchup_departments()
            self.status_var.set(self.lang.get("tuws_active", "✅ ATTIVA - reparti: {0}").format(len(sub_ids)))
        else:
            self.status_var.set(self.lang.get("tuws_inactive", "❌ Postazione NON attiva"))

    def _activate(self):
        sel = self.lb.curselection()
        if not sel:
            messagebox.showwarning(self.lang.get("warning", "Attenzione"),
                                   self.lang.get("tuws_no_sel", "Seleziona almeno un reparto."), parent=self)
            return
        cdc_ids, sub_ids = set(), set()
        for i in sel:
            cdc, sub, _l = self._rows[i]
            cdc_ids.add(cdc)
            sub_ids.add(sub)
        try:
            os.makedirs(_LOCALAPPDATA, exist_ok=True)
            data = {
                "touchup_host": True,
                "hostname": socket.gethostname(),
                "cdc_ids": sorted(cdc_ids),
                "subcdc_ids": sorted(sub_ids),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            with open(TOUCHUP_HOST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Touch-Up workstation attivata: {TOUCHUP_HOST_FILE} reparti={sorted(sub_ids)}")
            messagebox.showinfo(self.lang.get("info", "Info"),
                                self.lang.get("tuws_activated", "Postazione Touch-Up attivata."), parent=self)
            self._refresh_status()
        except PermissionError:
            messagebox.showerror(self.lang.get("error", "Errore"),
                                 self.lang.get("tuws_perm", "Permessi insufficienti (esegui come Amministratore)."),
                                 parent=self)
        except Exception as e:
            logger.error(f"Errore attivazione Touch-Up WS: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)

    def _deactivate(self):
        if not is_touchup_workstation():
            return
        if not messagebox.askyesno(self.lang.get("confirm", "Conferma"),
                                   self.lang.get("tuws_confirm_off", "Disattivare i popup Touch-Up su questo PC?"),
                                   parent=self):
            return
        try:
            os.remove(TOUCHUP_HOST_FILE)
            self._refresh_status()
            messagebox.showinfo(self.lang.get("info", "Info"),
                                self.lang.get("tuws_deactivated", "Postazione disattivata."), parent=self)
        except Exception as e:
            logger.error(f"Errore disattivazione Touch-Up WS: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)
