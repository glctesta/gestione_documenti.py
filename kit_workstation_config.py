"""
kit_workstation_config.py
Configurazione esplicita delle postazioni del flusso Kit Preparation.

Due ruoli indipendenti, ciascuno identificato da un file-flag locale in
%LOCALAPPDATA% (stesso meccanismo di wh_host.json usato per i materiali
indiretti / richieste materiale):

  - Formazione Kit            -> kit_prep_host.json  (target popup 'KIT_PREP')
  - Ricezione Kit Produzione  -> kit_prod_host.json  (target popup 'KIT_PROD')

I popup vengono indirizzati al target di ruolo e mostrati SOLO sulle
postazioni che hanno il flag corrispondente (vedi kit_popup_monitor.py).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_FLAG_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))

KIT_PREP_FLAG_FILE = os.path.join(_FLAG_DIR, "kit_prep_host.json")
KIT_PROD_FLAG_FILE = os.path.join(_FLAG_DIR, "kit_prod_host.json")

TARGET_KIT_PREP = "KIT_PREP"
TARGET_KIT_PROD = "KIT_PROD"


def is_kit_prep_workstation() -> bool:
    """True se questo PC è una postazione di Formazione Kit."""
    return os.path.isfile(KIT_PREP_FLAG_FILE)


def is_kit_prod_workstation() -> bool:
    """True se questo PC è una postazione di Ricezione Kit Produzione."""
    return os.path.isfile(KIT_PROD_FLAG_FILE)


class _KitWorkstationConfigWindow(tk.Toplevel):
    """Finestra generica per attivare/disattivare una postazione kit.

    Parametrizzata dal ruolo: file-flag, target popup e prefisso delle
    chiavi di traduzione. Le chiavi generiche (stato, errori) sono
    condivise con wh_workstation_* per non ritradurre testi identici.
    """

    def __init__(self, master, lang, user_name, flag_file, target,
                 key_prefix, default_role_label):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name
        self.flag_file = flag_file
        self.target = target
        self.kp = key_prefix
        self.default_role_label = default_role_label

        self.title(self.lang.get(f'{self.kp}_title',
                                 f'Conferma Postazione {default_role_label}'))
        self.geometry("520x340")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_status()

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        logger.info("Kit WorkStation Config Window aperta (ruolo=%s)", self.target)

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get(f'{self.kp}_header',
                               f'Configurazione Postazione {self.default_role_label}'),
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            main,
            text=self.lang.get(f'{self.kp}_desc',
                               'Questa funzione identifica il computer corrente\n'
                               f'come postazione "{self.default_role_label}".'),
            justify="center"
        ).pack(pady=(0, 15))

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

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        self.btn_create = ttk.Button(
            btn_frame,
            text=self.lang.get(f'{self.kp}_create',
                               f'Attiva Postazione {self.default_role_label}'),
            command=self._create_config
        )
        self.btn_create.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get(f'{self.kp}_delete',
                               f'Disattiva Postazione {self.default_role_label}'),
            command=self._delete_config
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=(5, 0))

    # ------------------------------------------------------------------ #
    #  Logica                                                              #
    # ------------------------------------------------------------------ #
    def _refresh_status(self):
        if os.path.isfile(self.flag_file):
            try:
                with open(self.flag_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                host = data.get("hostname", "?")
                activated = data.get("activated_at", "?")
                self.status_var.set(
                    self.lang.get(f'{self.kp}_active',
                                  '✅ Postazione ATTIVA\nHost: {0}\nAttivata: {1}').format(host, activated)
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
                self.lang.get(f'{self.kp}_inactive',
                              '❌ Postazione NON attiva')
            )
            self.btn_create.state(["!disabled"])
            self.btn_delete.state(["disabled"])

    def _create_config(self):
        try:
            os.makedirs(os.path.dirname(self.flag_file), exist_ok=True)

            data = {
                "role": self.target,
                "hostname": socket.gethostname(),
                "activated_by": self.user_name,
                "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(self.flag_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logger.info("Kit WorkStation config creata (%s): %s", self.target, self.flag_file)
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get(f'{self.kp}_created',
                              'Postazione attivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error("Permessi insufficienti per creare %s", self.flag_file)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error("Errore creazione kit config: %s", e, exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )

    def _delete_config(self):
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get(f'{self.kp}_confirm_delete',
                          'Sei sicuro di voler disattivare questa postazione?'),
            parent=self
        ):
            return

        try:
            os.remove(self.flag_file)
            logger.info("Kit WorkStation config eliminata (%s): %s", self.target, self.flag_file)
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get(f'{self.kp}_deleted',
                              'Postazione disattivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error("Permessi insufficienti per eliminare %s", self.flag_file)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error("Errore eliminazione kit config: %s", e, exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=self
            )


def open_kit_prep_workstation_config(master, lang, user_name="Unknown"):
    """Entry-point: postazione Formazione Kit (target KIT_PREP)."""
    _KitWorkstationConfigWindow(
        master, lang, user_name,
        flag_file=KIT_PREP_FLAG_FILE,
        target=TARGET_KIT_PREP,
        key_prefix='kit_prep_ws',
        default_role_label='Formazione Kit'
    )


def open_kit_prod_workstation_config(master, lang, user_name="Unknown"):
    """Entry-point: postazione Ricezione Kit Produzione (target KIT_PROD)."""
    _KitWorkstationConfigWindow(
        master, lang, user_name,
        flag_file=KIT_PROD_FLAG_FILE,
        target=TARGET_KIT_PROD,
        key_prefix='kit_prod_ws',
        default_role_label='Ricezione Kit Produzione'
    )
