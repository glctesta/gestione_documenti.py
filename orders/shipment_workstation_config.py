"""
orders/shipment_workstation_config.py

Finestra per configurare il computer corrente come postazione ricevente
popup di spedizioni urgenti.  Crea / elimina shipment_host.json in %LOCALAPPDATA%.

Stesso pattern di wh_workstation_config.py e shift_handover_monitor.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_LOCALAPPDATA = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
SHIPMENT_HOST_FILE = os.path.join(_LOCALAPPDATA, "shipment_host.json")


def is_shipment_workstation() -> bool:
    """Restituisce True se questo PC è configurato per ricevere popup spedizioni urgenti."""
    return os.path.isfile(SHIPMENT_HOST_FILE)


class ShipmentWorkstationConfigWindow(tk.Toplevel):
    """Finestra per attivare / disattivare il PC come postazione spedizioni urgenti."""

    def __init__(self, master, lang, user_name: str = "Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get("shipment_ws_title", "Configurazione Postazione Spedizioni"))
        self.geometry("500x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_status()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get("shipment_ws_header", "Configurazione Postazione Spedizioni Urgenti"),
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(0, 8))

        ttk.Label(
            main,
            text=self.lang.get(
                "shipment_ws_desc",
                "Attivando questa funzione, il computer riceverà i popup\n"
                "di notifica per le spedizioni urgenti inserite nel sistema.",
            ),
            justify="center",
        ).pack(pady=(0, 15))

        status_frame = ttk.LabelFrame(
            main, text=self.lang.get("status", "Stato"), padding=10
        )
        status_frame.pack(fill="x", pady=(0, 15))

        self.status_var = tk.StringVar(value="...")
        ttk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 10)).pack()

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        self.btn_activate = ttk.Button(
            btn_frame,
            text=self.lang.get("shipment_ws_activate", "✅ Attiva Postazione"),
            command=self._activate,
        )
        self.btn_activate.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_deactivate = ttk.Button(
            btn_frame,
            text=self.lang.get("shipment_ws_deactivate", "❌ Disattiva Postazione"),
            command=self._deactivate,
        )
        self.btn_deactivate.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _refresh_status(self):
        if os.path.isfile(SHIPMENT_HOST_FILE):
            try:
                with open(SHIPMENT_HOST_FILE, encoding="utf-8") as f:
                    data = json.load(f)
                host = data.get("hostname", "?")
                activated = data.get("activated_at", "?")
                by = data.get("activated_by", "?")
                self.status_var.set(
                    self.lang.get(
                        "shipment_ws_active",
                        "✅ Postazione ATTIVA\nHost: {0}\nAttivata da: {1}  —  {2}",
                    ).format(host, by, activated)
                )
            except Exception:
                self.status_var.set(
                    self.lang.get("shipment_ws_file_error", "⚠️ File presente ma non leggibile")
                )
            self.btn_activate.state(["disabled"])
            self.btn_deactivate.state(["!disabled"])
        else:
            self.status_var.set(
                self.lang.get("shipment_ws_inactive", "❌ Postazione NON attiva")
            )
            self.btn_activate.state(["!disabled"])
            self.btn_deactivate.state(["disabled"])

    def _activate(self):
        try:
            os.makedirs(_LOCALAPPDATA, exist_ok=True)
            data = {
                "shipment_host": True,
                "hostname": socket.gethostname(),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            with open(SHIPMENT_HOST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Shipment workstation attivata: {SHIPMENT_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get("info", "Info"),
                self.lang.get("shipment_ws_activated", "Postazione spedizioni attivata."),
                parent=self,
            )
            self._refresh_status()
        except PermissionError:
            messagebox.showerror(
                self.lang.get("error", "Errore"),
                self.lang.get(
                    "shipment_ws_perm_error",
                    "Permessi insufficienti.\nEseguire come Amministratore.",
                ),
                parent=self,
            )
        except Exception as e:
            logger.error(f"Errore attivazione shipment workstation: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)

    def _deactivate(self):
        if not messagebox.askyesno(
            self.lang.get("confirm", "Conferma"),
            self.lang.get(
                "shipment_ws_confirm_deactivate",
                "Disattivare questa postazione spedizioni?",
            ),
            parent=self,
        ):
            return
        try:
            os.remove(SHIPMENT_HOST_FILE)
            logger.info(f"Shipment workstation disattivata: {SHIPMENT_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get("info", "Info"),
                self.lang.get("shipment_ws_deactivated", "Postazione spedizioni disattivata."),
                parent=self,
            )
            self._refresh_status()
        except PermissionError:
            messagebox.showerror(
                self.lang.get("error", "Errore"),
                self.lang.get(
                    "shipment_ws_perm_error",
                    "Permessi insufficienti.\nEseguire come Amministratore.",
                ),
                parent=self,
            )
        except Exception as e:
            logger.error(f"Errore disattivazione shipment workstation: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)
