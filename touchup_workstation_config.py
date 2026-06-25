# -*- coding: utf-8 -*-
"""
touchup_workstation_config.py  (menu 4 - Setup workstation)
Configura il PC corrente come postazione che riceve i popup Touch-Up.
Crea/elimina touchup_host.json in %LOCALAPPDATA%.
Stessa identica logica di wh_workstation_config.py (materiali indiretti) e
della postazione cambio turno: semplice attiva/disattiva, nessuna altra scelta.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

TOUCHUP_HOST_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
TOUCHUP_HOST_FILE = os.path.join(TOUCHUP_HOST_DIR, "touchup_host.json")


def is_touchup_workstation() -> bool:
    """True se questo PC è configurato per ricevere i popup Touch-Up."""
    return os.path.isfile(TOUCHUP_HOST_FILE)


class TouchUpWorkstationConfigWindow(tk.Toplevel):
    """Finestra per attivare / disattivare il PC come postazione Touch-Up."""

    def __init__(self, master, lang, user_name="Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get('tuws_title', 'Postazione Touch-Up - Setup'))
        self.geometry("480x320")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_status()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        logger.info("Touch-Up WorkStation Config Window aperta")

    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get('tuws_header', 'Configurazione Postazione Touch-Up'),
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            main,
            text=self.lang.get('tuws_desc',
                               'Attivando questa funzione, il computer riceverà i popup\n'
                               'di notifica per le segnalazioni Touch-Up.'),
            justify="center"
        ).pack(pady=(0, 15))

        status_frame = ttk.LabelFrame(
            main, text=self.lang.get('status', 'Stato'), padding=10
        )
        status_frame.pack(fill="x", pady=(0, 15))

        self.status_var = tk.StringVar(value="...")
        ttk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 10)).pack()

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        self.btn_create = ttk.Button(
            btn_frame,
            text=self.lang.get('tuws_activate', '✅ Attiva su questo PC'),
            command=self._create_config
        )
        self.btn_create.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get('tuws_deactivate', '❌ Disattiva'),
            command=self._delete_config
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _refresh_status(self):
        if os.path.isfile(TOUCHUP_HOST_FILE):
            try:
                with open(TOUCHUP_HOST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                host = data.get("hostname", "?")
                activated = data.get("activated_at", "?")
                self.status_var.set(
                    self.lang.get('tuws_active',
                                  '✅ Postazione Touch-Up ATTIVA\nHost: {0}\nAttivata: {1}').format(host, activated)
                )
            except Exception:
                self.status_var.set(self.lang.get('tuws_file_error', '⚠️ File presente ma non leggibile'))
            self.btn_create.state(["disabled"])
            self.btn_delete.state(["!disabled"])
        else:
            self.status_var.set(self.lang.get('tuws_inactive', '❌ Postazione Touch-Up NON attiva'))
            self.btn_create.state(["!disabled"])
            self.btn_delete.state(["disabled"])

    def _create_config(self):
        try:
            os.makedirs(TOUCHUP_HOST_DIR, exist_ok=True)
            data = {
                "touchup_host": True,
                "hostname": socket.gethostname(),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(TOUCHUP_HOST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Touch-Up WorkStation config creata: {TOUCHUP_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('tuws_activated', 'Postazione Touch-Up attivata con successo.'),
                parent=self
            )
            self._refresh_status()
        except PermissionError:
            logger.error(f"Permessi insufficienti per creare {TOUCHUP_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('tuws_perm',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore creazione Touch-Up config: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _delete_config(self):
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('tuws_confirm_off', 'Disattivare i popup Touch-Up su questo PC?'),
            parent=self
        ):
            return
        try:
            os.remove(TOUCHUP_HOST_FILE)
            logger.info(f"Touch-Up WorkStation config eliminata: {TOUCHUP_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('tuws_deactivated', 'Postazione Touch-Up disattivata con successo.'),
                parent=self
            )
            self._refresh_status()
        except PermissionError:
            logger.error(f"Permessi insufficienti per eliminare {TOUCHUP_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('tuws_perm',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore eliminazione Touch-Up config: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


def open_touchup_workstation_config(master, lang, user_name="Unknown"):
    """Entry-point richiamabile da main.py."""
    TouchUpWorkstationConfigWindow(master, lang, user_name)
