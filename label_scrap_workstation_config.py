# -*- coding: utf-8 -*-
"""
label_scrap_workstation_config.py

Designa il PC corrente come postazione di STAMPA scarti etichette di fine turno.
Crea/elimina labelscrap_print_host.json in %LOCALAPPDATA%. Solo il PC designato
esegue la stampa forzata (e l'invio email) a fine turno. Stesso pattern di
orders/shipment_workstation_config.py.
"""
import os
import json
import socket
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

logger = logging.getLogger(__name__)

_LOCALAPPDATA = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
LABELSCRAP_PRINT_HOST_FILE = os.path.join(_LOCALAPPDATA, "labelscrap_print_host.json")


def is_labelscrap_print_workstation() -> bool:
    """True se questo PC è la postazione di stampa/email scarti etichette."""
    return os.path.isfile(LABELSCRAP_PRINT_HOST_FILE)


def open_labelscrap_workstation_config(master, lang, user_name="Unknown"):
    LabelScrapWorkstationConfigWindow(master, lang, user_name)


class LabelScrapWorkstationConfigWindow(tk.Toplevel):
    def __init__(self, master, lang, user_name="Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get("lsw_title", "Postazione Stampa Scarti Etichette"))
        self.geometry("520x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._build_ui()
        self._refresh_status()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        L = self.lang.get
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")
        ttk.Label(main, text=L("lsw_header", "Postazione Stampa Scarti Etichette"),
                  font=("Segoe UI", 13, "bold")).pack(pady=(0, 8))
        ttk.Label(main, justify="center", text=L(
            "lsw_desc",
            "Attivando questa funzione, a fine turno (15:15 / 23:15) questo PC\n"
            "stamperà i riepiloghi scarti etichette non stampati e invierà l'email.\n"
            "Designare un solo PC per evitare stampe/invii duplicati.")).pack(pady=(0, 15))
        sf = ttk.LabelFrame(main, text=L("status", "Stato"), padding=10)
        sf.pack(fill="x", pady=(0, 15))
        self.status_var = tk.StringVar(value="...")
        ttk.Label(sf, textvariable=self.status_var, font=("Segoe UI", 10)).pack()
        bf = ttk.Frame(main)
        bf.pack(fill="x")
        self.btn_activate = ttk.Button(bf, text=L("lsw_activate", "✅ Attiva"), command=self._activate)
        self.btn_activate.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.btn_deactivate = ttk.Button(bf, text=L("lsw_deactivate", "❌ Disattiva"), command=self._deactivate)
        self.btn_deactivate.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _refresh_status(self):
        L = self.lang.get
        if os.path.isfile(LABELSCRAP_PRINT_HOST_FILE):
            try:
                with open(LABELSCRAP_PRINT_HOST_FILE, encoding="utf-8") as f:
                    d = json.load(f)
                self.status_var.set(L("lsw_active", "✅ ATTIVA\nHost: {0}\nAttivata da: {1}  —  {2}").format(
                    d.get("hostname", "?"), d.get("activated_by", "?"), d.get("activated_at", "?")))
            except Exception:
                self.status_var.set(L("lsw_file_error", "⚠️ File presente ma non leggibile"))
            self.btn_activate.state(["disabled"])
            self.btn_deactivate.state(["!disabled"])
        else:
            self.status_var.set(L("lsw_inactive", "❌ NON attiva"))
            self.btn_activate.state(["!disabled"])
            self.btn_deactivate.state(["disabled"])

    def _activate(self):
        L = self.lang.get
        try:
            os.makedirs(_LOCALAPPDATA, exist_ok=True)
            with open(LABELSCRAP_PRINT_HOST_FILE, "w", encoding="utf-8") as f:
                json.dump({"labelscrap_print_host": True, "hostname": socket.gethostname(),
                           "activated_by": self.user_name,
                           "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                          f, indent=4, ensure_ascii=False)
            logger.info(f"Label scrap print workstation attivata: {LABELSCRAP_PRINT_HOST_FILE}")
            messagebox.showinfo(L("info", "Info"), L("lsw_activated", "Postazione attivata."), parent=self)
            self._refresh_status()
        except Exception as e:
            logger.error(f"Errore attivazione: {e}", exc_info=True)
            messagebox.showerror(L("error", "Errore"), str(e), parent=self)

    def _deactivate(self):
        L = self.lang.get
        if not messagebox.askyesno(L("confirm", "Conferma"),
                                   L("lsw_confirm_deactivate", "Disattivare questa postazione?"), parent=self):
            return
        try:
            os.remove(LABELSCRAP_PRINT_HOST_FILE)
            logger.info("Label scrap print workstation disattivata")
            messagebox.showinfo(L("info", "Info"), L("lsw_deactivated", "Postazione disattivata."), parent=self)
            self._refresh_status()
        except Exception as e:
            logger.error(f"Errore disattivazione: {e}", exc_info=True)
            messagebox.showerror(L("error", "Errore"), str(e), parent=self)
