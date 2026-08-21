"""
wh_workstation_config.py
Finestra per configurare il computer come WorkStation (WH o Acquisti materiali).
Crea o elimina il file corrispondente in %LOCALAPPDATA%:
  - wh_host.json        -> postazione ricevente ordini (WH)
  - purchasing_host.json -> postazione ufficio acquisti materiali indiretti
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

HOST_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
WH_HOST_FILE = os.path.join(HOST_DIR, "wh_host.json")
PURCHASING_HOST_FILE = os.path.join(HOST_DIR, "purchasing_host.json")


class WHWorkstationConfigWindow(tk.Toplevel):
    """Finestra per creare o eliminare la configurazione di una WorkStation."""

    def __init__(self, master, lang, user_name="Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get('workstation_config_title', 'Configura WorkStation'))
        self.geometry("520x420")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_status()

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        logger.info("Workstation Config Window aperta")

    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get('workstation_config_header', 'Configurazione WorkStation'),
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            main,
            text=self.lang.get('workstation_config_desc',
                               'Identifica questo computer come postazione ricevente ordini (WH) '
                               'o come postazione acquisti materiali indiretti.'),
            justify="center"
        ).pack(pady=(0, 15))

        # Selettore tipo workstation
        type_frame = ttk.Frame(main)
        type_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(type_frame, text=self.lang.get('workstation_type', 'Tipo WorkStation:')).pack(side="left", padx=(0, 8))
        self.type_var = tk.StringVar(value="WH")
        self.type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            values=["WH", "Acquisti materiali"],
            state="readonly",
            width=30
        )
        self.type_combo.pack(side="left")
        self.type_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_status())

        # Frame stato
        status_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('workstation_status_label', 'Stato'),
            padding=10
        )
        status_frame.pack(fill="x", pady=(0, 15))

        self.status_var = tk.StringVar(value="...")
        self.status_lbl = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10)
        )
        self.status_lbl.pack()

        # Pulsanti
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        self.btn_create = ttk.Button(
            btn_frame,
            text=self.lang.get('workstation_create', 'Attiva WorkStation'),
            command=self._create_config
        )
        self.btn_create.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get('workstation_delete', 'Disattiva WorkStation'),
            command=self._delete_config
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _get_file_for_type(self, wstype):
        return PURCHASING_HOST_FILE if wstype == "Acquisti materiali" else WH_HOST_FILE

    def _refresh_status(self):
        wstype = self.type_var.get()
        cfg_file = self._get_file_for_type(wstype)
        label_active = self.lang.get('workstation_active', '✅ WorkStation ATTIVA\nHost: {0}\nAttivata: {1}')
        label_inactive = self.lang.get('workstation_inactive', '❌ WorkStation NON attiva')
        label_file_error = self.lang.get('workstation_file_error', '⚠️ File presente ma non leggibile')

        if os.path.isfile(cfg_file):
            try:
                with open(cfg_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                host = data.get("hostname", "?")
                activated = data.get("activated_at", "?")
                self.status_var.set(label_active.format(host, activated))
            except Exception:
                self.status_var.set(label_file_error)
            self.btn_create.state(["disabled"])
            self.btn_delete.state(["!disabled"])
        else:
            self.status_var.set(label_inactive)
            self.btn_create.state(["!disabled"])
            self.btn_delete.state(["disabled"])

    def _create_config(self):
        wstype = self.type_var.get()
        cfg_file = self._get_file_for_type(wstype)
        try:
            os.makedirs(HOST_DIR, exist_ok=True)

            data = {
                "workstation_type": wstype,
                "hostname": socket.gethostname(),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(cfg_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logger.info(f"Workstation config creata: {cfg_file}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('workstation_created', 'WorkStation attivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per creare {cfg_file}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore creazione workstation config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )

    def _delete_config(self):
        wstype = self.type_var.get()
        cfg_file = self._get_file_for_type(wstype)
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('workstation_confirm_delete',
                          'Sei sicuro di voler disattivare la WorkStation?'),
            parent=self
        ):
            return

        try:
            os.remove(cfg_file)
            logger.info(f"Workstation config eliminata: {cfg_file}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('workstation_deleted', 'WorkStation disattivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per eliminare {cfg_file}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore eliminazione workstation config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )


def is_wh_workstation():
    """Controlla se questo PC è un WH WorkStation."""
    return os.path.isfile(WH_HOST_FILE)


def is_purchasing_workstation():
    """Controlla se questo PC è una WorkStation acquisti materiali."""
    return os.path.isfile(PURCHASING_HOST_FILE)


def open_wh_workstation_config(master, lang, user_name="Unknown"):
    """Entry-point richiamabile da main.py."""
    WHWorkstationConfigWindow(master, lang, user_name)
