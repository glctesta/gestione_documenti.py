"""
ticket_gui.py – Sistema di Ticketing per TraceabilityRS
Gestisce la creazione, cattura log/screenshot e invio email dei ticket.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import datetime
import traceback
import logging

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  Costanti                                                                     #
# --------------------------------------------------------------------------- #
_TICKET_DIR = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "tickets")
_LOG_FILE = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "logs", "traceability_rs.log")


# --------------------------------------------------------------------------- #
#  Funzioni di supporto                                                         #
# --------------------------------------------------------------------------- #

def _get_ticket_email(db) -> str:
    """Legge l'email destinataria da dbo.settings."""
    query = "SELECT [value] FROM dbo.settings WHERE Atribute = 'SysEmail_service_tickets'"
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query)
            row = db.cursor.fetchone()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"[TICKET] Impossibile leggere email destinataria: {e}")
    return ""


def _get_log_tail(n: int = 50) -> str:
    """Restituisce le ultime n righe del log attivo."""
    try:
        if not os.path.exists(_LOG_FILE):
            return "(file log non trovato)"
        with open(_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return "".join(lines[-n:])
    except Exception as e:
        logger.warning(f"[TICKET] Errore lettura log: {e}")
        return f"(errore lettura log: {e})"


def _capture_screenshot(widget) -> str | None:
    """
    Cattura uno screenshot dell'intero schermo e lo salva in _TICKET_DIR.
    Restituisce il percorso del file PNG oppure None in caso di errore.
    """
    try:
        from PIL import ImageGrab
        os.makedirs(_TICKET_DIR, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(_TICKET_DIR, f"ticket_{ts}.png")

        # Cattura l'intero schermo
        img = ImageGrab.grab()
        img.save(path, "PNG")
        return path
    except ImportError:
        logger.warning("[TICKET] PIL non disponibile: screenshot non catturato")
        return None
    except Exception as e:
        logger.warning(f"[TICKET] Errore screenshot: {e}")
        return None


def _save_ticket_to_db(db, user_name: str, title: str, description: str,
                        error_type: str, error_message: str,
                        log_snippet: str, screenshot_path: str) -> int | None:
    """
    Inserisce il ticket in tck.Tickets e restituisce il TicketID oppure None.
    """
    query = """
        INSERT INTO tck.Tickets
            (UserName, Title, Description, ErrorType, ErrorMessage, LogSnippet, ScreenshotPath)
        OUTPUT INSERTED.TicketID
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query, (
                user_name or "unknown",
                title,
                description,
                error_type,
                error_message or "",
                log_snippet or "",
                screenshot_path or ""
            ))
            row = db.cursor.fetchone()
            db.conn.commit()
        if row:
            return int(row[0])
    except Exception as e:
        logger.error(f"[TICKET] Errore salvataggio DB: {e}", exc_info=True)
    return None


def _mark_ticket_email_sent(db, ticket_id: int):
    """Aggiorna EmailSent=1 per il ticket indicato."""
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(
                "UPDATE tck.Tickets SET EmailSent = 1 WHERE TicketID = ?", (ticket_id,)
            )
            db.conn.commit()
    except Exception as e:
        logger.warning(f"[TICKET] Impossibile aggiornare EmailSent: {e}")


def _send_ticket_email(db, ticket_id: int, recipient: str, title: str,
                        description: str, error_type: str,
                        error_message: str, log_snippet: str,
                        screenshot_path: str, user_name: str):
    """Invia la notifica email del ticket (sincrona). Rilancia l'eccezione in caso di errore."""
    from email_connector import EmailSender
    sender = EmailSender()
    subject = f"[Ticket #{ticket_id}] {title}"

    body_html = f"""
<html><body style="font-family:Arial,sans-serif;font-size:13px;color:#333;">
<h2 style="color:#1565C0;">&#128279; Nuovo Ticket #{ticket_id}</h2>
<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;max-width:700px;">
  <tr><td style="font-weight:bold;width:140px;">Utente</td><td>{user_name or 'N/A'}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Titolo</td><td>{title}</td></tr>
  <tr><td style="font-weight:bold;">Tipo</td>
      <td><span style="color:{'#C62828' if error_type=='exception' else '#1565C0'}">
          {'&#9888; Eccezione automatica' if error_type=='exception' else '&#9989; Manuale'}
      </span></td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Data/Ora</td>
      <td>{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td></tr>
</table>

<h3 style="margin-top:20px;color:#1565C0;">Descrizione</h3>
<div style="background:#F5F5F5;padding:10px;border-left:4px solid #1565C0;
            white-space:pre-wrap;font-size:12px;">{description}</div>
"""
    if error_message:
        body_html += f"""
<h3 style="color:#C62828;">Dettaglio Errore / Stacktrace</h3>
<pre style="background:#FFF3E0;padding:10px;border-left:4px solid #C62828;
            font-size:11px;overflow-x:auto;">{error_message}</pre>
"""
    if log_snippet:
        body_html += f"""
<h3 style="color:#2E7D32;">Log recente (ultime righe)</h3>
<pre style="background:#E8F5E9;padding:10px;border-left:4px solid #2E7D32;
            font-size:10px;overflow-x:auto;">{log_snippet}</pre>
"""
    body_html += "</body></html>"

    attachments = []
    if screenshot_path and os.path.exists(screenshot_path):
        attachments.append(screenshot_path)
    if os.path.exists(_LOG_FILE):
        attachments.append(_LOG_FILE)

    sender.send_email(
        to_email=recipient,
        subject=subject,
        body=body_html,
        is_html=True,
        attachments=attachments if attachments else None
    )
    _mark_ticket_email_sent(db, ticket_id)
    logger.info(f"[TICKET] Email inviata – ticket #{ticket_id} → {recipient}")


# --------------------------------------------------------------------------- #
#  Finestra principale                                                           #
# --------------------------------------------------------------------------- #

class TicketWindow(tk.Toplevel):
    """
    Finestra di ticketing. Può essere aperta manualmente (Help → Tickets)
    o automaticamente in caso di eccezione non gestita.

    Parametri:
        master     – finestra padre (MainApplication)
        db         – DatabaseHandler
        lang       – LanguageManager
        user_name  – nome utente corrente (str | None)
        error_info – dict con chiavi 'type', 'message', 'traceback'
                     se apertura automatica da eccezione
    """

    def __init__(self, master, db, lang, user_name=None, error_info=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or ""
        self.error_info = error_info or {}
        self._screenshot_path: str | None = None

        # Configurazione finestra
        title_key = "ticket_window_title" if not self.error_info else "ticket_window_title_error"
        self.title(self.lang.get(title_key, "Nuovo Ticket" if not self.error_info else "Errore – Apri Ticket"))
        self.geometry("820x680")
        self.minsize(700, 580)
        self.transient(master)
        self.grab_set()

        self._is_auto = bool(self.error_info)
        self._build_ui()
        self._populate_auto(self.error_info)

        # Centra sulla finestra padre
        self.update_idletasks()
        px = master.winfo_x() + (master.winfo_width() - self.winfo_width()) // 2
        py = master.winfo_y() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")

    # ------------------------------------------------------------------ build

    def _build_ui(self):
        # --- Banner errore automatico ---
        if self._is_auto:
            banner = tk.Frame(self, bg="#B71C1C", padx=10, pady=6)
            banner.pack(fill=tk.X)
            tk.Label(
                banner,
                text=f"⚠  {self.lang.get('ticket_auto_error_banner', 'Errore rilevato automaticamente – compila il ticket per segnalarlo.')}",
                bg="#B71C1C", fg="white", font=("Helvetica", 10, "bold")
            ).pack(side=tk.LEFT)

        # --- Frame principale con padding ---
        main = ttk.Frame(self, padding=12)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(1, weight=1)

        row = 0

        # Titolo
        ttk.Label(main, text=self.lang.get('ticket_title_label', 'Titolo (*)'),
                  font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
        self.title_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.title_var, width=70).grid(
            row=row, column=1, sticky="ew", pady=(0, 8))
        row += 1

        # Tipo
        ttk.Label(main, text=self.lang.get('ticket_type_label', 'Tipo'),
                  font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
        type_val = "exception" if self._is_auto else "manual"
        type_display = (self.lang.get('ticket_type_exception', '⚠ Eccezione automatica')
                        if self._is_auto else
                        self.lang.get('ticket_type_manual', '✅ Manuale'))
        ttk.Label(main, text=type_display,
                  foreground="#C62828" if self._is_auto else "#1565C0").grid(
            row=row, column=1, sticky="w", pady=(0, 8))
        self._error_type = type_val
        row += 1

        # Descrizione
        ttk.Label(main, text=self.lang.get('ticket_description_label', 'Descrizione (*)'),
                  font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
        desc_frame = ttk.Frame(main)
        desc_frame.grid(row=row, column=1, sticky="nsew", pady=(0, 8))
        desc_frame.columnconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)
        self.desc_text = tk.Text(desc_frame, height=5, wrap=tk.WORD, font=("Helvetica", 9))
        desc_sb = ttk.Scrollbar(desc_frame, orient=tk.VERTICAL, command=self.desc_text.yview)
        self.desc_text.configure(yscrollcommand=desc_sb.set)
        self.desc_text.grid(row=0, column=0, sticky="nsew")
        desc_sb.grid(row=0, column=1, sticky="ns")
        main.rowconfigure(row, weight=1)
        row += 1

        # Dettaglio errore (solo se automatico)
        if self._is_auto:
            ttk.Label(main, text=self.lang.get('ticket_error_detail_label', 'Dettaglio errore'),
                      font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
            err_frame = ttk.Frame(main)
            err_frame.grid(row=row, column=1, sticky="nsew", pady=(0, 8))
            err_frame.columnconfigure(0, weight=1)
            err_frame.rowconfigure(0, weight=1)
            self.error_text = tk.Text(err_frame, height=5, wrap=tk.WORD, font=("Courier", 8),
                                      state=tk.DISABLED, bg="#FFF8E1")
            err_sb = ttk.Scrollbar(err_frame, orient=tk.VERTICAL, command=self.error_text.yview)
            self.error_text.configure(yscrollcommand=err_sb.set)
            self.error_text.grid(row=0, column=0, sticky="nsew")
            err_sb.grid(row=0, column=1, sticky="ns")
            main.rowconfigure(row, weight=1)
            row += 1

        # Log recente
        ttk.Label(main, text=self.lang.get('ticket_log_label', 'Log recente (ultime 50 righe)'),
                  font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
        log_frame = ttk.Frame(main)
        log_frame.grid(row=row, column=1, sticky="nsew", pady=(0, 8))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, height=5, wrap=tk.NONE, font=("Courier", 7),
                                state=tk.DISABLED, bg="#F1F8E9")
        log_sb_v = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_sb_h = ttk.Scrollbar(log_frame, orient=tk.HORIZONTAL, command=self.log_text.xview)
        self.log_text.configure(yscrollcommand=log_sb_v.set, xscrollcommand=log_sb_h.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_sb_v.grid(row=0, column=1, sticky="ns")
        log_sb_h.grid(row=1, column=0, sticky="ew")
        main.rowconfigure(row, weight=1)
        row += 1

        # Screenshot
        scr_frame = ttk.Frame(main)
        scr_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.scr_capture_btn = ttk.Button(
            scr_frame,
            text=self.lang.get('ticket_capture_btn', '📷 Cattura Screenshot'),
            command=self._on_capture_screenshot
        )
        self.scr_capture_btn.pack(side=tk.LEFT)
        self.scr_status_label = ttk.Label(scr_frame, text=self.lang.get('ticket_no_screenshot', '(nessuno screenshot)'),
                                          foreground="#757575")
        self.scr_status_label.pack(side=tk.LEFT, padx=(10, 0))
        row += 1

        # Pulsanti azione
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky="e", pady=(4, 0))
        self.send_btn = ttk.Button(
            btn_frame,
            text=self.lang.get('ticket_send_btn', '📨 Invia Ticket'),
            command=self._on_send
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(6, 0))
        ttk.Button(
            btn_frame,
            text=self.lang.get('button_close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT)

        # Carica log subito
        self._load_log()

    # ------------------------------------------------------------------ populate

    def _populate_auto(self, error_info: dict):
        """Pre-compila i campi se apertura da eccezione."""
        if not error_info:
            return

        # Titolo automatico
        err_type = error_info.get('type', 'Exception')
        self.title_var.set(f"[Auto] {err_type}")

        # Testo errore
        if hasattr(self, 'error_text'):
            full = ""
            if error_info.get('message'):
                full += f"Messaggio:\n{error_info['message']}\n\n"
            if error_info.get('traceback'):
                full += f"Traceback:\n{error_info['traceback']}"
            self.error_text.config(state=tk.NORMAL)
            self.error_text.insert("1.0", full)
            self.error_text.config(state=tk.DISABLED)

    def _load_log(self):
        log_content = _get_log_tail(50)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert("1.0", log_content)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------ callbacks

    def _on_capture_screenshot(self):
        """Cattura screenshot e aggiorna lo stato."""
        # Minimizza la finestra brevemente per includere lo sfondo
        self.withdraw()
        self.master.update_idletasks()
        path = _capture_screenshot(self.master)
        self.deiconify()

        if path:
            self._screenshot_path = path
            fname = os.path.basename(path)
            self.scr_status_label.config(
                text=f"✓ {fname}",
                foreground="#2E7D32"
            )
            logger.info(f"[TICKET] Screenshot salvato: {path}")
        else:
            self.scr_status_label.config(
                text=self.lang.get('ticket_screenshot_failed', '⚠ Screenshot non riuscito'),
                foreground="#C62828"
            )

    def _on_send(self):
        """Valida, salva su DB e invia email."""
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning(
                self.lang.get('warn_title', 'Attenzione'),
                self.lang.get('ticket_title_required', "Inserire un titolo per il ticket."),
                parent=self
            )
            return

        if not description:
            messagebox.showwarning(
                self.lang.get('warn_title', 'Attenzione'),
                self.lang.get('ticket_description_required', "Inserire una descrizione del problema."),
                parent=self
            )
            return

        # Componi error_message
        error_msg = ""
        if self.error_info:
            error_msg = ""
            if self.error_info.get('message'):
                error_msg += f"Messaggio: {self.error_info['message']}\n"
            if self.error_info.get('traceback'):
                error_msg += f"\nTraceback:\n{self.error_info['traceback']}"

        log_snippet = _get_log_tail(50)

        # Disabilita il pulsante durante il salvataggio
        self.send_btn.config(state=tk.DISABLED,
                             text=self.lang.get('ticket_sending', '⏳ Invio in corso...'))
        self.update_idletasks()

        try:
            ticket_id = _save_ticket_to_db(
                db=self.db,
                user_name=self.user_name,
                title=title,
                description=description,
                error_type=self._error_type,
                error_message=error_msg,
                log_snippet=log_snippet,
                screenshot_path=self._screenshot_path or ""
            )

            if ticket_id is None:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('ticket_save_error', 'Errore durante il salvataggio del ticket nel database.'),
                    parent=self
                )
                self.send_btn.config(state=tk.NORMAL,
                                     text=self.lang.get('ticket_send_btn', '📨 Invia Ticket'))
                return

            # Recupera destinatario email e invia
            recipient = _get_ticket_email(self.db)
            email_sent = False
            if recipient:
                try:
                    _send_ticket_email(
                        db=self.db,
                        ticket_id=ticket_id,
                        recipient=recipient,
                        title=title,
                        description=description,
                        error_type=self._error_type,
                        error_message=error_msg,
                        log_snippet=log_snippet,
                        screenshot_path=self._screenshot_path or "",
                        user_name=self.user_name
                    )
                    email_sent = True
                    logger.info(f"[TICKET] Ticket #{ticket_id} creato, email inviata → {recipient}")
                except Exception as mail_err:
                    logger.error(f"[TICKET] Ticket #{ticket_id} creato ma email fallita: {mail_err}", exc_info=True)
                    messagebox.showwarning(
                        self.lang.get('warn_title', 'Attenzione'),
                        f"Ticket #{ticket_id} salvato, ma l'invio email è fallito:\n{mail_err}",
                        parent=self
                    )
            else:
                logger.warning(f"[TICKET] Ticket #{ticket_id} creato, nessuna email destinataria trovata (SysEmail_service_tickets).")
                messagebox.showwarning(
                    self.lang.get('warn_title', 'Attenzione'),
                    f"Ticket #{ticket_id} salvato, ma nessun indirizzo email configurato in settings (SysEmail_service_tickets).",
                    parent=self
                )

            if email_sent:
                messagebox.showinfo(
                    self.lang.get('info_title', 'Informazione'),
                    self.lang.get(
                        'ticket_sent_ok',
                        f"Ticket #{ticket_id} registrato con successo."
                    ).replace('{id}', str(ticket_id)),
                    parent=self
                )
            self.destroy()

        except Exception as e:
            logger.error(f"[TICKET] Errore durante invio ticket: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('ticket_send_error', 'Errore durante invio ticket')}: {e}",
                parent=self
            )
            self.send_btn.config(state=tk.NORMAL,
                                 text=self.lang.get('ticket_send_btn', '📨 Invia Ticket'))


# --------------------------------------------------------------------------- #
#  Entry point pubblico                                                         #
# --------------------------------------------------------------------------- #

def open_ticket_window(master, db, lang, user_name=None, error_info=None):
    """
    Apre la finestra ticket.
    Chiamata da menu (error_info=None) o da sys.excepthook (error_info=dict).
    """
    try:
        TicketWindow(master, db, lang, user_name, error_info)
    except Exception as e:
        logger.error(f"[TICKET] Impossibile aprire TicketWindow: {e}", exc_info=True)
        # Fallback minimal: almeno logga
        messagebox.showerror(
            "Errore Ticketing",
            f"Impossibile aprire la finestra ticket: {e}",
            parent=master
        )
