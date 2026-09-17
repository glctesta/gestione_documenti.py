# -*- coding: utf-8 -*-
"""
incoming/incoming_workstation_config.py

Configurazione delle postazioni del modulo "Ricezione" (Incoming).

Due ruoli indipendenti, attivi per singolo PC (file-flag locale in
%LOCALAPPDATA%, stesso meccanismo di kit_workstation_config.py):

  - receiver  -> PC che RICEVE le richieste (popup nuove richieste +
                 escalation, target popup 'INCOMING_RECEIVER')
  - sender    -> PC che INVIA le richieste (WH incoming; riceve il popup
                 di risposta sul proprio host, target = RequesterHost)

I due ruoli convivono in UN solo file marcatore (incoming_workstation.json)
con una mappa "roles": se nessun ruolo resta attivo il file viene cancellato.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import tempfile
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

ROLE_RECEIVER = 'receiver'   # PC che RICEVE le richieste (popup nuove richieste + escalation)
ROLE_SENDER = 'sender'       # PC che INVIA le richieste (WH incoming; riceve popup risposta)

VALID_ROLES = (ROLE_RECEIVER, ROLE_SENDER)

_FLAG_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
MARKER_FILE = os.path.join(_FLAG_DIR, "incoming_workstation.json")

# Target popup usati sulla coda condivisa kit_popup_queue
TARGET_INCOMING_RECEIVER = "INCOMING_RECEIVER"


def _read_marker() -> dict:
    """Legge il file marcatore; restituisce {'hostname':..., 'roles': {...}} o
    una struttura vuota se assente/illeggibile."""
    if not os.path.isfile(MARKER_FILE):
        return {"hostname": socket.gethostname(), "roles": {}}
    try:
        with open(MARKER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"hostname": socket.gethostname(), "roles": {}}
        roles = data.get("roles")
        if not isinstance(roles, dict):
            roles = {}
        return {"hostname": data.get("hostname", socket.gethostname()), "roles": roles}
    except Exception as e:
        logger.error("incoming_workstation.json non leggibile (%s): tratto come assente", e)
        return {"hostname": socket.gethostname(), "roles": {}}


def _write_marker(data: dict) -> None:
    """Scrittura atomica (tmp -> replace) del file marcatore."""
    os.makedirs(_FLAG_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=_FLAG_DIR,
                                     encoding="utf-8") as tf:
        json.dump(data, tf, ensure_ascii=False, indent=2)
        tmp = tf.name
    os.replace(tmp, MARKER_FILE)


def get_roles() -> set:
    """Insieme dei ruoli Incoming attivi su questo PC (sottoinsieme di
    {'receiver','sender'})."""
    data = _read_marker()
    return {r for r in data["roles"] if r in VALID_ROLES and data["roles"][r]}


def is_incoming_receiver() -> bool:
    """True se questo PC riceve le richieste Incoming (popup nuove richieste
    ed escalation, target 'INCOMING_RECEIVER')."""
    return ROLE_RECEIVER in get_roles()


def is_incoming_sender() -> bool:
    """True se questo PC invia le richieste Incoming (WH incoming; riceve il
    popup di risposta sul proprio host)."""
    return ROLE_SENDER in get_roles()


def activate_role(role: str, user_name: str) -> None:
    """Attiva un ruolo su questo PC. Solleva ValueError per ruoli non validi."""
    if role not in VALID_ROLES:
        raise ValueError(f"Ruolo Incoming non valido: {role!r}")
    data = _read_marker()
    data["hostname"] = socket.gethostname()
    data["roles"][role] = {
        "activated_by": user_name,
        "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _write_marker(data)
    logger.info("Ruolo Incoming '%s' attivato su %s da %s (file=%s)",
                role, socket.gethostname(), user_name, MARKER_FILE)


def deactivate_role(role: str) -> None:
    """Disattiva un ruolo su questo PC; se non resta nessun ruolo attivo
    cancella il file marcatore."""
    data = _read_marker()
    if role not in data["roles"]:
        return
    del data["roles"][role]
    if not data["roles"]:
        deactivate_all()
    else:
        _write_marker(data)
    logger.info("Ruolo Incoming '%s' disattivato su %s (file=%s)",
                role, socket.gethostname(), MARKER_FILE)


def deactivate_all() -> None:
    """Disattiva tutti i ruoli Incoming su questo PC (cancella il marcatore)."""
    try:
        if os.path.isfile(MARKER_FILE):
            os.remove(MARKER_FILE)
            logger.info("File marcatore Incoming rimosso: %s", MARKER_FILE)
    except Exception as e:
        logger.error("Errore rimozione %s: %s", MARKER_FILE, e)


class _RoleSection(ttk.LabelFrame):
    """Sezione Attiva/Disattiva per un singolo ruolo."""

    def __init__(self, master, lang, user_name, role, role_label):
        super().__init__(master, text=role_label, padding=10)
        self.lang = lang
        self.user_name = user_name
        self.role = role

        self.status_var = tk.StringVar(value="...")
        ttk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")

        self.btn_activate = ttk.Button(
            btn_frame,
            text=self.lang.get('incoming_ws_activate', '✅ Attiva'),
            command=self._activate,
        )
        self.btn_activate.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_deactivate = ttk.Button(
            btn_frame,
            text=self.lang.get('incoming_ws_deactivate', '❌ Disattiva'),
            command=self._deactivate,
        )
        self.btn_deactivate.pack(side="left", expand=True, fill="x", padx=(5, 0))

        self._refresh_status()

    def _refresh_status(self):
        info = _read_marker()["roles"].get(self.role)
        if info:
            self.status_var.set(
                self.lang.get(
                    'incoming_ws_active',
                    '✅ Ruolo ATTIVO\nHost: {0}\nAttivato da: {1}  —  {2}',
                ).format(
                    socket.gethostname(),
                    info.get("activated_by", "?"),
                    info.get("activated_at", "?"),
                )
            )
            self.btn_activate.state(["disabled"])
            self.btn_deactivate.state(["!disabled"])
        else:
            self.status_var.set(
                self.lang.get('incoming_ws_inactive', '❌ Ruolo NON attivo')
            )
            self.btn_activate.state(["!disabled"])
            self.btn_deactivate.state(["disabled"])

    def _activate(self):
        top = self.winfo_toplevel()
        try:
            activate_role(self.role, self.user_name)
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('incoming_ws_activated', 'Ruolo attivato con successo.'),
                parent=top,
            )
        except PermissionError:
            logger.error("Permessi insufficienti per creare %s", MARKER_FILE)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=top,
            )
        except Exception as e:
            logger.error("Errore attivazione ruolo Incoming %s: %s", self.role, e,
                         exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=top,
            )
        self._refresh_status()

    def _deactivate(self):
        top = self.winfo_toplevel()
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('incoming_ws_confirm_deactivate',
                          'Sei sicuro di voler disattivare questo ruolo?'),
            parent=top,
        ):
            return
        try:
            deactivate_role(self.role)
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('incoming_ws_deactivated', 'Ruolo disattivato con successo.'),
                parent=top,
            )
        except PermissionError:
            logger.error("Permessi insufficienti per modificare %s", MARKER_FILE)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=top,
            )
        except Exception as e:
            logger.error("Errore disattivazione ruolo Incoming %s: %s", self.role, e,
                         exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wh_workstation_generic_error', 'Errore')}: {e}",
                parent=top,
            )
        self._refresh_status()


class IncomingWorkstationConfigWindow(tk.Toplevel):
    """Finestra standalone per attivare/disattivare i ruoli Incoming del PC."""

    def __init__(self, master, lang, user_name="Unknown"):
        super().__init__(master)
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('incoming_ws_title',
                                 'Configurazione Postazione — Ricezione (Incoming)'))
        self.geometry("560x430")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._role_sections = []
        self._build_ui()

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        logger.info("IncomingWorkstationConfigWindow aperta su %s (ruoli=%s)",
                    socket.gethostname(), sorted(get_roles()))

    def _build_ui(self):
        L = self.lang.get
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=L('incoming_ws_header', 'Configurazione Postazione Ricezione'),
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(0, 8))

        ttk.Label(
            main,
            text=L('incoming_ws_desc',
                   'Identifica questo computer come postazione del modulo Ricezione.\n'
                   '"Ricevitore" mostra i popup delle nuove richieste ed escalation;\n'
                   '"Mittente" invia le richieste dal magazzino incoming.'),
            justify="center",
        ).pack(pady=(0, 12))

        self._role_sections.append(_RoleSection(
            main, self.lang, self.user_name, ROLE_RECEIVER,
            L('incoming_ws_receiver_label', 'Ricevitore richieste (popup nuove richieste + escalation)'),
        ))
        self._role_sections[-1].pack(fill="x", pady=(0, 10))

        self._role_sections.append(_RoleSection(
            main, self.lang, self.user_name, ROLE_SENDER,
            L('incoming_ws_sender_label', 'Mittente richieste (WH incoming; popup di risposta)'),
        ))
        self._role_sections[-1].pack(fill="x", pady=(0, 10))

        bottom = ttk.Frame(main)
        bottom.pack(fill="x")

        ttk.Button(
            bottom,
            text=L('incoming_ws_deactivate_all', 'Disattiva tutto'),
            command=self._deactivate_all,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            bottom,
            text=L('close', 'Chiudi'),
            command=self.destroy,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _deactivate_all(self):
        L = self.lang.get
        if not messagebox.askyesno(
            L('confirm', 'Conferma'),
            L('incoming_ws_confirm_deactivate_all',
              'Disattivare TUTTI i ruoli Incoming su questo PC?'),
            parent=self,
        ):
            return
        try:
            deactivate_all()
            messagebox.showinfo(
                L('info', 'Info'),
                L('incoming_ws_deactivated', 'Ruolo disattivato con successo.'),
                parent=self,
            )
        except Exception as e:
            logger.error("Errore disattivazione totale Incoming: %s", e, exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
        for section in self._role_sections:
            section._refresh_status()


def open_workstation_config(master, lang, user_name="Unknown"):
    """Apre la finestra standalone Attiva/Disattiva per i ruoli Incoming."""
    IncomingWorkstationConfigWindow(master, lang, user_name)


if __name__ == "__main__":
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("Marker file:", MARKER_FILE)
    print("Ruoli attivi:", sorted(get_roles()))
    print("receiver:", is_incoming_receiver(), " sender:", is_incoming_sender())
