# -*- coding: utf-8 -*-
"""
incoming/incoming_setup_gui.py

Finestra di setup del modulo "Ricezione" (Incoming):

  - Destinatari email e numero di reminder/giorno per ogni tipo di richiesta
    (MPN Mancante, MPN Sbagliato, Mancanza P.O., P.O. Quantità)
    -> incoming_db.get_email_config / save_email_config
  - Destinatari del report mensile (settings atribute
    'Incoming_soluzione_problemi') -> incoming_db.get_monthly_recipients
  - Collegamento alla configurazione della postazione (ruoli receiver/sender)

Accesso DB uniforme: le funzioni di incoming_db accettano sia la classe
Database di main.py sia BackgroundDatabase del servizio background. Per il
salvataggio dei destinatari mensile (funzione non prevista dal contratto di
incoming_db) si usa il pattern condiviso `_cursor(db)` + `db._lock`.
"""

import logging
import re
import tkinter as tk
from tkinter import ttk, messagebox

try:  # importazione come package (from incoming.incoming_setup_gui import ...)
    from . import incoming_db
    from . import incoming_workstation_config
except ImportError:  # fallback: modulo flat o eseguito dalla root del progetto
    try:
        from incoming import incoming_db
        from incoming import incoming_workstation_config
    except ImportError:
        import incoming_db  # type: ignore
        import incoming_workstation_config  # type: ignore

logger = logging.getLogger(__name__)

_EMAIL_SPLIT_RE = re.compile(r'[;,\s]+')
_MAX_REMINDERS_PER_DAY = 24


def _cursor(db):
    """Cursore DB robusto: riallaccia la connessione se il backend lo supporta."""
    if hasattr(db, '_ensure_connection'):
        try:
            db._ensure_connection()
        except Exception:
            pass
    return db.cursor


def _parse_emails(text: str) -> tuple:
    """Split della textarea email in (email_valide, token_scartati)."""
    valid, rejected = [], []
    for token in _EMAIL_SPLIT_RE.split(text or ""):
        token = token.strip()
        if not token:
            continue
        if '@' in token and '.' in token.split('@')[-1]:
            valid.append(token)
        else:
            rejected.append(token)
    return valid, rejected


def _format_emails(emails) -> str:
    return "; ".join(e for e in (emails or []) if e)


def _load_email_config(db, request_type: str) -> dict:
    try:
        cfg = incoming_db.get_email_config(db, request_type)
        if isinstance(cfg, dict):
            return cfg
    except Exception as e:
        logger.error("get_email_config(%s) fallita: %s", request_type, e, exc_info=True)
    return {'emails': [], 'reminders_per_day': 0}


def _load_monthly_recipients(db) -> list:
    try:
        rec = incoming_db.get_monthly_recipients(db)
        return list(rec or [])
    except Exception as e:
        logger.error("get_monthly_recipients fallita: %s", e, exc_info=True)
        return []


def _save_monthly_recipients(db, emails: list) -> None:
    """Salva i destinatari mensili. Preferisce incoming_db.save_monthly_recipients
    se il modulo DB la espone; altrimenti scrive direttamente su
    traceability_rs.dbo.Settings (una riga per email), come da pattern
    di get_email_recipients."""
    save_fn = getattr(incoming_db, 'save_monthly_recipients', None)
    if callable(save_fn):
        save_fn(db, emails)
        return
    attribute = getattr(incoming_db, 'MONTHLY_RECIPIENTS_ATTRIBUTE',
                        'Incoming_soluzione_problemi')
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            "DELETE FROM traceability_rs.dbo.Settings WHERE atribute = ?", attribute)
        for email in emails:
            cur.execute(
                "INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) "
                "VALUES (?, ?)", (attribute, email))
        db.conn.commit()


class IncomingSetupWindow(tk.Toplevel):
    """Setup del modulo Ricezione: email per tipo richiesta, report mensile,
    collegamento alla configurazione postazione."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('incoming_setup_title',
                                 'Setup — Ricezione (Incoming)'))
        self.geometry("680x860")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # (request_type, type_label, emails_var, reminders_var)
        self._type_rows = []
        self._monthly_text = None
        self._engineering_text = None
        self._master_text = None

        self._build_ui()
        self._load_all()

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        logger.info("IncomingSetupWindow aperta (user=%s)", user_name)

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        L = self.lang.get
        main = ttk.Frame(self, padding=15)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=L('incoming_setup_header', 'Configurazione modulo Ricezione (Incoming)'),
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(0, 10))

        # --- Email per tipo richiesta ---------------------------------- #
        email_frame = ttk.LabelFrame(
            main,
            text=L('incoming_setup_email_frame',
                   'Destinatari email e reminder per tipo di richiesta'),
            padding=10,
        )
        email_frame.pack(fill="x", pady=(0, 10))

        head = ttk.Frame(email_frame)
        head.pack(fill="x", pady=(0, 6))
        ttk.Label(head, text=L('incoming_setup_col_type', 'Tipo richiesta'),
                  font=("Segoe UI", 9, "bold"), width=22).pack(side="left")
        ttk.Label(head, text=L('incoming_setup_col_emails', 'Email destinatari (separate da ; o ,)'),
                  font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 0), expand=True, fill="x")
        ttk.Label(head, text=L('incoming_setup_col_reminders', 'Reminder/giorno'),
                  font=("Segoe UI", 9, "bold"), width=14).pack(side="right")

        for request_type in incoming_db.REQUEST_TYPES:
            row = ttk.Frame(email_frame)
            row.pack(fill="x", pady=3)

            type_label = incoming_db.type_label(L, request_type)
            ttk.Label(row, text=type_label, width=22).pack(side="left")

            emails_var = tk.StringVar()
            ttk.Entry(row, textvariable=emails_var).pack(
                side="left", padx=(10, 10), expand=True, fill="x")

            reminders_var = tk.IntVar(value=0)
            ttk.Spinbox(
                row, from_=0, to=_MAX_REMINDERS_PER_DAY, width=6,
                textvariable=reminders_var,
            ).pack(side="right")

            self._type_rows.append((request_type, type_label, emails_var, reminders_var))

        ttk.Label(
            email_frame,
            text=L('incoming_setup_reminders_hint',
                   'I reminder sono popup/email ripetuti giornalmente per ogni richiesta ancora in sospeso.'),
            font=("Segoe UI", 8),
            foreground="#555555",
        ).pack(anchor="w", pady=(6, 0))

        # --- Report mensile -------------------------------------------- #
        monthly_frame = ttk.LabelFrame(
            main,
            text=L('incoming_setup_monthly_frame',
                   'Destinatari report mensile (soluzione problemi)'),
            padding=10,
        )
        monthly_frame.pack(fill="x", pady=(0, 10))

        self._monthly_text = tk.Text(monthly_frame, height=4, wrap="word")
        self._monthly_text.pack(fill="both", expand=True)

        # --- Ingegneria (TO email soluzione) ------------------------------ #
        engineering_frame = ttk.LabelFrame(
            main,
            text=L('incoming_setup_engineering_frame',
                   'Indirizzi email Ingegneria (destinatari in TO della email soluzione)'),
            padding=10,
        )
        engineering_frame.pack(fill="x", pady=(0, 10))

        self._engineering_text = tk.Text(engineering_frame, height=3, wrap="word")
        self._engineering_text.pack(fill="x")
        ttk.Label(
            engineering_frame,
            text=L('incoming_setup_engineering_hint',
                   'Indirizzi Ingegneria inseriti come destinatari principali (A) '
                   'dell\'email preconfezionata di richiesta soluzione.'),
            font=("Segoe UI", 8),
            foreground="#555555",
        ).pack(anchor="w", pady=(4, 0))

        # --- Master ticket ---------------------------------------------- #
        master_frame = ttk.LabelFrame(
            main,
            text=L('incoming_setup_master_frame',
                   'Master ticket (vede tutti i ticket aperti)'),
            padding=10,
        )
        master_frame.pack(fill="x", pady=(0, 10))

        self._master_text = tk.Text(master_frame, height=2, wrap="word")
        self._master_text.pack(fill="x")
        ttk.Label(
            master_frame,
            text=L('incoming_setup_master_hint',
                   'Email degli utenti abilitati a vedere tutti i ticket, '
                   'indipendentemente dai destinatari configurati per tipo.'),
            font=("Segoe UI", 8),
            foreground="#555555",
        ).pack(anchor="w", pady=(4, 0))

        # --- Postazione ------------------------------------------------- #
        ws_frame = ttk.LabelFrame(
            main,
            text=L('incoming_setup_workstation_frame', 'Postazione (questo PC)'),
            padding=10,
        )
        ws_frame.pack(fill="x", pady=(0, 10))

        ws_row = ttk.Frame(ws_frame)
        ws_row.pack(fill="x")

        roles = sorted(incoming_workstation_config.get_roles())
        ws_status = (L('incoming_setup_ws_roles', 'Ruoli attivi: {0}')
                     .format(", ".join(roles) if roles
                             else L('incoming_setup_ws_none', 'nessuno')))
        ttk.Label(ws_row, text=ws_status).pack(side="left")

        ttk.Button(
            ws_row,
            text=L('incoming_setup_ws_open', 'Configura postazione…'),
            command=self._open_workstation_config,
        ).pack(side="right")

        # --- Pulsanti in basso ------------------------------------------ #
        bottom = ttk.Frame(main)
        bottom.pack(fill="x")

        ttk.Button(
            bottom,
            text=L('save', 'Salva'),
            command=self._save_all,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            bottom,
            text=L('close', 'Chiudi'),
            command=self.destroy,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    # ------------------------------------------------------------------ #
    #  Caricamento                                                         #
    # ------------------------------------------------------------------ #
    def _load_all(self):
        for request_type, _label, emails_var, reminders_var in self._type_rows:
            cfg = _load_email_config(self.db, request_type)
            emails_var.set(_format_emails(cfg.get('emails')))
            try:
                reminders_var.set(int(cfg.get('reminders_per_day') or 0))
            except (TypeError, ValueError):
                reminders_var.set(0)

        self._monthly_text.delete("1.0", "end")
        self._monthly_text.insert("1.0", "\n".join(_load_monthly_recipients(self.db)))

        self._engineering_text.delete("1.0", "end")
        try:
            engineering_emails = incoming_db.get_engineering_recipients(self.db)
        except Exception as e:
            logger.error("get_engineering_recipients fallita: %s", e, exc_info=True)
            engineering_emails = []
        self._engineering_text.insert("1.0", "\n".join(engineering_emails))

        self._master_text.delete("1.0", "end")
        try:
            master_emails = incoming_db.get_master_emails(self.db)
        except Exception as e:
            logger.error("get_master_emails fallita: %s", e, exc_info=True)
            master_emails = []
        self._master_text.insert("1.0", "\n".join(master_emails))

    # ------------------------------------------------------------------ #
    #  Salvataggio                                                         #
    # ------------------------------------------------------------------ #
    def _save_all(self):
        L = self.lang.get

        # Validazione email per tipo
        parsed_by_type = {}
        rejected_all = []
        for request_type, _label, emails_var, _rem in self._type_rows:
            valid, rejected = _parse_emails(emails_var.get())
            parsed_by_type[request_type] = valid
            rejected_all.extend(rejected)

        valid_monthly, rejected_monthly = _parse_emails(self._monthly_text.get("1.0", "end"))
        rejected_all.extend(rejected_monthly)

        valid_engineering, rejected_engineering = _parse_emails(
            self._engineering_text.get("1.0", "end"))
        rejected_all.extend(rejected_engineering)

        valid_master, rejected_master = _parse_emails(self._master_text.get("1.0", "end"))
        rejected_all.extend(rejected_master)

        if rejected_all:
            messagebox.showerror(
                L('error', 'Errore'),
                L('incoming_setup_invalid_emails',
                  'I seguenti indirizzi non sono validi e non verranno salvati:\n{0}'
                  ).format("\n".join(rejected_all)),
                parent=self,
            )
            return

        try:
            for request_type, _label, _emails_var, reminders_var in self._type_rows:
                try:
                    reminders = int(reminders_var.get())
                except (TypeError, ValueError):
                    reminders = 0
                reminders = max(0, min(_MAX_REMINDERS_PER_DAY, reminders))
                incoming_db.save_email_config(
                    self.db, request_type, parsed_by_type[request_type], reminders)

            _save_monthly_recipients(self.db, valid_monthly)
            incoming_db.save_engineering_recipients(self.db, valid_engineering)
            incoming_db.save_master_emails(self.db, valid_master)

            logger.info("Setup Incoming salvato da %s: tipi=%s, destinatari mensili=%d, ingegneria=%d, master=%d",
                        self.user_name,
                        {k: len(v) for k, v in parsed_by_type.items()},
                        len(valid_monthly), len(valid_engineering), len(valid_master))
            messagebox.showinfo(
                L('info', 'Info'),
                L('incoming_setup_saved', 'Configurazione salvata con successo.'),
                parent=self,
            )
        except Exception as e:
            logger.error("Errore salvataggio setup Incoming: %s", e, exc_info=True)
            messagebox.showerror(
                L('error', 'Errore'),
                f"{L('incoming_setup_save_error', 'Errore durante il salvataggio')}: {e}",
                parent=self,
            )

    # ------------------------------------------------------------------ #
    #  Altro                                                               #
    # ------------------------------------------------------------------ #
    def _open_workstation_config(self):
        incoming_workstation_config.open_workstation_config(
            self, self.lang, self.user_name)


def open_incoming_setup(master, db, lang, user_name="Unknown"):
    """Apre la finestra di setup del modulo Ricezione."""
    IncomingSetupWindow(master, db, lang, user_name)
