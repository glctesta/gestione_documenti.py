"""
wh_workstation_config.py
Finestra per configurare il computer come WH WorkStation (ricevente ordini).
Crea o elimina il file wh_host.json in C:\\Users\\Default\\AppData\\Local\\
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

WH_HOST_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
WH_HOST_FILE = os.path.join(WH_HOST_DIR, "wh_host.json")


class WHWorkstationConfigWindow(tk.Toplevel):
    """Finestra per creare o eliminare la configurazione WH WorkStation."""

    def __init__(self, master, lang, user_name="Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get('wh_workstation_title', 'Conferma WH WorkStation'))
        self.geometry("480x320")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_status()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        # Titolo
        ttk.Label(
            main,
            text=self.lang.get('wh_workstation_header',
                               'Configurazione WH WorkStation'),
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(0, 10))

        # Descrizione
        ttk.Label(
            main,
            text=self.lang.get('wh_workstation_desc',
                               'Questa funzione identifica il computer corrente\n'
                               'come postazione ricevente ordini (WH Host).'),
            justify="center"
        ).pack(pady=(0, 15))

        # Frame stato
        status_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('wh_workstation_status_label', 'Stato'),
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
            text=self.lang.get('wh_workstation_create', 'Attiva WH WorkStation'),
            command=self._create_config
        )
        self.btn_create.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get('wh_workstation_delete', 'Disattiva WH WorkStation'),
            command=self._delete_config
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=(5, 0))

    # ------------------------------------------------------------------ #
    #  Logica                                                              #
    # ------------------------------------------------------------------ #
    def _refresh_status(self):
        """Aggiorna lo stato mostrato nella UI."""
        if os.path.isfile(WH_HOST_FILE):
            try:
                with open(WH_HOST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                host = data.get("hostname", "?")
                activated = data.get("activated_at", "?")
                self.status_var.set(
                    self.lang.get('wh_workstation_active',
                                  '✅ WH WorkStation ATTIVA\nHost: {0}\nAttivata: {1}').format(host, activated)
                )
            except Exception:
                self.status_var.set(
                    self.lang.get('wh_workstation_file_error',
                                  '⚠️ File presente ma non leggibile')
                )
            self.btn_create.state(["disabled"])
            self.btn_delete.state(["!disabled"])
        else:
            self.status_var.set(
                self.lang.get('wh_workstation_inactive',
                              '❌ WH WorkStation NON attiva')
            )
            self.btn_create.state(["!disabled"])
            self.btn_delete.state(["disabled"])

    def _create_config(self):
        """Crea il file wh_host.json."""
        try:
            os.makedirs(WH_HOST_DIR, exist_ok=True)

            data = {
                "wh_host": True,
                "hostname": socket.gethostname(),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(WH_HOST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logger.info(f"WH WorkStation config creata: {WH_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('wh_workstation_created',
                              'WH WorkStation attivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per creare {WH_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore creazione WH config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )

    def _delete_config(self):
        """Elimina il file wh_host.json."""
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('wh_workstation_confirm_delete',
                          'Sei sicuro di voler disattivare la WH WorkStation?'),
            parent=self
        ):
            return

        try:
            os.remove(WH_HOST_FILE)
            logger.info(f"WH WorkStation config eliminata: {WH_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('wh_workstation_deleted',
                              'WH WorkStation disattivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per eliminare {WH_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore eliminazione WH config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )


def open_wh_workstation_config(master, lang, user_name="Unknown"):
    """Entry-point richiamabile da main.py."""
    WHWorkstationConfigWindow(master, lang, user_name)
