# -*- coding: utf-8 -*-
"""
sct_workstation_config.py
Finestra per configurare il computer come SCT WorkStation (Capo Turno).
Crea o elimina il file sct_host.json in %LOCALAPPDATA%.
Permette di scegliere il reparto e i turni abilitati.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SCT_HOST_DIR  = os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
SCT_HOST_FILE = os.path.join(SCT_HOST_DIR, 'sct_host.json')

# Turni disponibili
SHIFT_OPTIONS = [
    (1, 'Turno 1  (fine 15:30)'),
    (2, 'Turno 2  (fine 23:30)'),
    (3, 'Turno 3  (fine 07:30) — opzionale'),
]


def _fetch_departments(db):
    """Carica reparti da employee.dbo.CdcSub."""
    try:
        sql = "SELECT SubCdcId, SubCdcDescription FROM Employee.dbo.CdcSub WHERE SubCdcId in (1,9,17) ORDER BY SubCdcDescription"
        if hasattr(db, 'fetch_all'):
            rows = db.fetch_all(sql) or []
        else:
            with db._lock:
                db.cursor.execute(sql)
                rows = db.cursor.fetchall() or []
        return [r[1] for r in rows]
    except Exception as e:
        logger.warning(f"Impossibile caricare reparti dal DB: {e}")
        return ['SMT', 'PTHH', 'WAREHOUSE']


class SCTWorkstationConfigWindow(tk.Toplevel):
    """
    Finestra stile WH WorkStation per configurare questo PC come Capo Turno.
    Permette di:
      - Vedere lo stato attuale (ATTIVA / INATTIVA)
      - Scegliere reparto e turni abilitati
      - Attivare (crea sct_host.json) o Disattivare (elimina il file)
    """

    def __init__(self, master, lang, user_name='Unknown', db=None):
        super().__init__(master)
        self.lang      = lang
        self.user_name = user_name
        self.db        = db

        self.title(lang.get('sct_config_title', 'Configurazione SCT WorkStation — Capo Turno'))
        self.geometry('520x420')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._dept_names = _fetch_departments(db) if db else ['SMT', 'PTHH', 'WAREHOUSE']

        self._build_ui()
        self._refresh_status()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        main = ttk.Frame(self, padding=20)
        main.pack(expand=True, fill='both')

        # Titolo
        ttk.Label(
            main,
            text=self.lang.get('sct_config_header', 'Configurazione SCT WorkStation'),
            font=('Segoe UI', 13, 'bold')
        ).pack(pady=(0, 6))

        # Descrizione
        ttk.Label(
            main,
            text=self.lang.get(
                'sct_config_desc',
                'Questa funzione identifica il computer corrente\n'
                'come postazione Capo Turno (SCT Host).\n'
                'I popup di fine turno appariranno solo su questo PC.'
            ),
            justify='center',
            foreground='#555'
        ).pack(pady=(0, 12))

        # ── Stato ─────────────────────────────────────────────────────────────
        status_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('wh_workstation_status_label', 'Stato'),
            padding=10
        )
        status_frame.pack(fill='x', pady=(0, 12))

        self.status_var = tk.StringVar(value='...')
        self.status_lbl = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            justify='center'
        )
        self.status_lbl.pack()

        # ── Configurazione reparto / turni ────────────────────────────────────
        cfg_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('sct_config_params', 'Parametri workstation'),
            padding=10
        )
        cfg_frame.pack(fill='x', pady=(0, 12))

        # Reparto
        row_dept = ttk.Frame(cfg_frame)
        row_dept.pack(fill='x', pady=(0, 8))
        ttk.Label(row_dept, text=self.lang.get('sh_dept', 'Reparto:'), width=12).pack(side='left')
        self.dept_var = tk.StringVar()
        self.dept_cb  = ttk.Combobox(row_dept, textvariable=self.dept_var,
                                     values=self._dept_names, width=25, state='readonly')
        self.dept_cb.pack(side='left', padx=4)
        if self._dept_names:
            self.dept_var.set(self._dept_names[0])

        # Turni (checkbutton)
        row_shifts = ttk.Frame(cfg_frame)
        row_shifts.pack(fill='x')
        ttk.Label(row_shifts, text=self.lang.get('sh_shift', 'Turni:'), width=12).pack(side='left')
        self._shift_vars = {}
        for snum, slabel in SHIFT_OPTIONS:
            var = tk.BooleanVar(value=(snum in (1, 2)))
            self._shift_vars[snum] = var
            ttk.Checkbutton(row_shifts, text=slabel, variable=var).pack(side='left', padx=6)

        # ── Pulsanti ──────────────────────────────────────────────────────────
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill='x')

        self.btn_create = ttk.Button(
            btn_frame,
            text=self.lang.get('sct_config_activate', 'Attiva SCT WorkStation'),
            command=self._create_config
        )
        self.btn_create.pack(side='left', expand=True, fill='x', padx=(0, 5))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get('sct_config_deactivate', 'Disattiva SCT WorkStation'),
            command=self._delete_config
        )
        self.btn_delete.pack(side='left', expand=True, fill='x', padx=(5, 0))

    # ── Logica ────────────────────────────────────────────────────────────────
    def _refresh_status(self):
        """Aggiorna stato UI leggendo sct_host.json."""
        if os.path.isfile(SCT_HOST_FILE):
            try:
                with open(SCT_HOST_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                dept     = data.get('department', '?')
                shifts   = data.get('shifts', [])
                host     = data.get('hostname', '?')
                activated = data.get('activated_at', '?')
                shifts_str = ', '.join(f"T{s}" for s in shifts) if shifts else '—'

                self.status_var.set(
                    f"✅  SCT WorkStation ATTIVA\n"
                    f"Reparto: {dept}   |   Turni: {shifts_str}\n"
                    f"Host: {host}   |   Attivata: {activated}"
                )
                # Pre-seleziona i valori correnti nei widget
                if dept in self._dept_names:
                    self.dept_var.set(dept)
                for snum, var in self._shift_vars.items():
                    var.set(snum in shifts)

                self.btn_create.state(['disabled'])
                self.btn_delete.state(['!disabled'])
            except Exception:
                self.status_var.set('⚠️  File presente ma non leggibile')
                self.btn_create.state(['!disabled'])
                self.btn_delete.state(['!disabled'])
        else:
            self.status_var.set(
                self.lang.get('sct_config_inactive', '❌  SCT WorkStation INATTIVA')
            )
            self.btn_create.state(['!disabled'])
            self.btn_delete.state(['disabled'])

    def _create_config(self):
        """Crea sct_host.json con i parametri selezionati."""
        dept   = self.dept_var.get().strip()
        shifts = [snum for snum, var in self._shift_vars.items() if var.get()]

        if not dept:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('sct_config_err_dept', 'Selezionare un reparto.'),
                parent=self
            )
            return
        if not shifts:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('sct_config_err_shifts', 'Selezionare almeno un turno.'),
                parent=self
            )
            return

        try:
            os.makedirs(SCT_HOST_DIR, exist_ok=True)

            data = {
                'role':         'shift_leader',
                'department':   dept,
                'shifts':       sorted(shifts),
                'hostname':     socket.gethostname(),
                'activated_by': self.user_name,
                'activated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            with open(SCT_HOST_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logger.info(f"SCT WorkStation config creata: {SCT_HOST_FILE} — {data}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get(
                    'sct_config_created',
                    f'SCT WorkStation attivata con successo.\n\n'
                    f'Reparto: {dept}\nTurni: {", ".join(f"T{s}" for s in sorted(shifts))}'
                ),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per creare {SCT_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore creazione SCT config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error', 'Errore')}: {e}",
                parent=self
            )

    def _delete_config(self):
        """Elimina sct_host.json disattivando la workstation."""
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('sct_config_confirm_delete',
                          'Sei sicuro di voler disattivare la SCT WorkStation?\n'
                          'I popup di fine turno non appariranno più su questo PC.'),
            parent=self
        ):
            return

        try:
            os.remove(SCT_HOST_FILE)
            logger.info(f"SCT WorkStation config eliminata: {SCT_HOST_FILE}")
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('sct_config_deleted', 'SCT WorkStation disattivata con successo.'),
                parent=self
            )
            self._refresh_status()

        except PermissionError:
            logger.error(f"Permessi insufficienti per eliminare {SCT_HOST_FILE}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('wh_workstation_permission_error',
                              'Permessi insufficienti.\nEseguire il programma come Amministratore.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore eliminazione SCT config: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error', 'Errore')}: {e}",
                parent=self
            )


def open_sct_workstation_config(master, lang, user_name='Unknown', db=None):
    """Entry-point richiamabile da main.py."""
    SCTWorkstationConfigWindow(master, lang, user_name, db)
