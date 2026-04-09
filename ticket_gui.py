"""
ticket_gui.py – Sistema di Ticketing per TraceabilityRS
Gestisce la creazione, cattura log/screenshot e invio email dei ticket.
Include: TicketWindow, TicketHistoryWindow, TicketManagementWindow.
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

# Stati ticket
STATUS_OPEN = 'open'
STATUS_ON_WORKING = 'on_working'
STATUS_CLOSED = 'closed'

STATUS_LABELS = {
    STATUS_OPEN: {'it': 'Aperto', 'en': 'Open', 'ro': 'Deschis', 'de': 'Offen', 'sv': 'Öppen'},
    STATUS_ON_WORKING: {'it': 'In Lavorazione', 'en': 'On Working', 'ro': 'În Lucru', 'de': 'In Bearbeitung', 'sv': 'Under Arbete'},
    STATUS_CLOSED: {'it': 'Chiuso', 'en': 'Closed', 'ro': 'Închis', 'de': 'Geschlossen', 'sv': 'Stängd'},
}

STATUS_COLORS = {
    STATUS_OPEN: '#E65100',        # Arancione
    STATUS_ON_WORKING: '#1565C0',  # Blu
    STATUS_CLOSED: '#2E7D32',      # Verde
}


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


def _get_employee_work_email(db, employee_hire_history_id: int) -> str:
    """Recupera la WorkEmail di un dipendente dal DB Employee."""
    query = """
        SELECT ea.WorkEmail
        FROM Employee.dbo.EmployeeHireHistory h
        INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
        LEFT JOIN Employee.dbo.EmployeeAddress ea ON ea.EmployeeId = e.EmployeeId
                                                  AND ea.DateOut IS NULL
        WHERE h.EmployeeHireHistoryId = ?
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query, (employee_hire_history_id,))
            row = db.cursor.fetchone()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"[TICKET] Impossibile recuperare WorkEmail per employee {employee_hire_history_id}: {e}")
    return ""


def _get_employee_name(db, employee_hire_history_id: int) -> str:
    """Recupera il nome completo di un dipendente dal DB Employee."""
    query = """
        SELECT UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS EmployeeName
        FROM Employee.dbo.EmployeeHireHistory h
        INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
        WHERE h.EmployeeHireHistoryId = ?
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query, (employee_hire_history_id,))
            row = db.cursor.fetchone()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"[TICKET] Impossibile recuperare nome per employee {employee_hire_history_id}: {e}")
    return ""


def _save_ticket_to_db(db, user_name: str, title: str, description: str,
                        error_type: str, error_message: str,
                        log_snippet: str, screenshot_path: str,
                        employee_id: int = None, work_email: str = None) -> int | None:
    """
    Inserisce il ticket in tck.Tickets e restituisce il TicketID oppure None.
    """
    query = """
        INSERT INTO tck.Tickets
            (UserName, Title, Description, ErrorType, ErrorMessage, LogSnippet, ScreenshotPath,
             OpenedByEmployeeId, OpenedByName, OpenedByEmail, Status)
        OUTPUT INSERTED.TicketID
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                screenshot_path or "",
                employee_id,
                user_name or "unknown",
                work_email or "",
                STATUS_OPEN
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
                        screenshot_path: str, user_name: str,
                        work_email: str = None):
    """Invia la notifica email del ticket (sincrona). Rilancia l'eccezione in caso di errore."""
    from email_connector import EmailSender
    sender = EmailSender()
    subject = f"[Ticket #{ticket_id}] {title}"

    body_html = f"""
<html><body style="font-family:Arial,sans-serif;font-size:13px;color:#333;">
<h2 style="color:#1565C0;">&#128279; Nuovo Ticket #{ticket_id}</h2>
<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;max-width:700px;">
  <tr><td style="font-weight:bold;width:140px;">Utente</td><td>{user_name or 'N/A'}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Email</td><td>{work_email or 'N/A'}</td></tr>
  <tr><td style="font-weight:bold;">Titolo</td><td>{title}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Tipo</td>
      <td><span style="color:{'#C62828' if error_type=='exception' else '#1565C0'}">
          {'&#9888; Eccezione automatica' if error_type=='exception' else '&#9989; Manuale'}
      </span></td></tr>
  <tr><td style="font-weight:bold;">Data/Ora</td>
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


def _send_closure_email(db, ticket_id: int, recipient_email: str,
                        ticket_title: str, closure_note: str,
                        closed_by_name: str):
    """Invia email di notifica chiusura ticket all'utente che lo ha aperto."""
    from email_connector import EmailSender
    sender = EmailSender()
    subject = f"[Ticket #{ticket_id}] Risolto – {ticket_title}"

    body_html = f"""
<html><body style="font-family:Arial,sans-serif;font-size:13px;color:#333;">
<h2 style="color:#2E7D32;">&#9989; Ticket #{ticket_id} – Risolto</h2>
<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;max-width:700px;">
  <tr><td style="font-weight:bold;width:140px;">Ticket</td><td>#{ticket_id}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Titolo</td><td>{ticket_title}</td></tr>
  <tr><td style="font-weight:bold;">Chiuso da</td><td>{closed_by_name}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Data Chiusura</td>
      <td>{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td></tr>
</table>

<h3 style="margin-top:20px;color:#2E7D32;">Nota di Risoluzione</h3>
<div style="background:#E8F5E9;padding:10px;border-left:4px solid #2E7D32;
            white-space:pre-wrap;font-size:12px;">{closure_note or '(nessuna nota)'}</div>

<p style="margin-top:20px;color:#757575;font-size:11px;">
Questo messaggio è stato generato automaticamente dal sistema TraceabilityRS.</p>
</body></html>
"""

    sender.send_email(
        to_email=recipient_email,
        subject=subject,
        body=body_html,
        is_html=True
    )
    logger.info(f"[TICKET] Email chiusura inviata – ticket #{ticket_id} → {recipient_email}")


def _fetch_tickets_for_user(db, employee_id: int) -> list:
    """Recupera tutti i ticket aperti dall'utente, ordinati per data decrescente."""
    query = """
        SELECT TicketID, CreatedAt, Title, Status, ErrorType,
               ClosedAt, ClosedByName, ClosureNote, ClosureNotified
        FROM tck.Tickets
        WHERE OpenedByEmployeeId = ?
        ORDER BY CreatedAt DESC
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query, (employee_id,))
            cols = [d[0] for d in db.cursor.description]
            rows = db.cursor.fetchall()
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        logger.error(f"[TICKET] Errore fetch ticket utente: {e}", exc_info=True)
        return []


def _fetch_all_tickets(db) -> list:
    """Recupera tutti i ticket (per gestione admin), ordinati per data decrescente."""
    query = """
        SELECT TicketID, CreatedAt, Title, Status, ErrorType,
               OpenedByName, OpenedByEmail, OpenedByEmployeeId,
               ClosedAt, ClosedByName, ClosureNote, ClosureNotified,
               Description
        FROM tck.Tickets
        ORDER BY 
            CASE Status 
                WHEN 'open' THEN 1 
                WHEN 'on_working' THEN 2 
                WHEN 'closed' THEN 3 
            END,
            CreatedAt DESC
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query)
            cols = [d[0] for d in db.cursor.description]
            rows = db.cursor.fetchall()
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        logger.error(f"[TICKET] Errore fetch tutti i ticket: {e}", exc_info=True)
        return []


def _update_ticket_status(db, ticket_id: int, new_status: str,
                          closed_by_id: int = None, closed_by_name: str = None,
                          closure_note: str = None) -> bool:
    """Aggiorna lo stato di un ticket. Per chiusura, popola anche i campi closure."""
    try:
        with db._lock:
            db._clear_cursor_state()
            if new_status == STATUS_CLOSED:
                db.cursor.execute("""
                    UPDATE tck.Tickets 
                    SET Status = ?, ClosedAt = GETDATE(), ClosedBy = ?,
                        ClosedByName = ?, ClosureNote = ?
                    WHERE TicketID = ?
                """, (new_status, closed_by_id, closed_by_name, closure_note or '', ticket_id))
            else:
                db.cursor.execute("""
                    UPDATE tck.Tickets SET Status = ? WHERE TicketID = ?
                """, (new_status, ticket_id))
            db.conn.commit()
        logger.info(f"[TICKET] Ticket #{ticket_id} aggiornato a '{new_status}'")
        return True
    except Exception as e:
        logger.error(f"[TICKET] Errore aggiornamento stato ticket #{ticket_id}: {e}", exc_info=True)
        return False


def _mark_closure_notified(db, ticket_id: int):
    """Segna il ticket come notificato all'utente."""
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(
                "UPDATE tck.Tickets SET ClosureNotified = 1 WHERE TicketID = ?", (ticket_id,)
            )
            db.conn.commit()
    except Exception as e:
        logger.warning(f"[TICKET] Impossibile aggiornare ClosureNotified: {e}")


def check_and_notify_closed_tickets(master, db, lang, employee_id: int, user_name: str):
    """
    Controlla se ci sono ticket chiusi non ancora notificati per l'utente.
    Se sì, mostra un popup per ciascuno.
    Chiamato da _execute_simple_login dopo un login riuscito.
    """
    query = """
        SELECT TicketID, Title, ClosureNote, ClosedByName, ClosedAt
        FROM tck.Tickets
        WHERE OpenedByEmployeeId = ? AND Status = ? AND ClosureNotified = 0
    """
    try:
        with db._lock:
            db._clear_cursor_state()
            db.cursor.execute(query, (employee_id, STATUS_CLOSED))
            cols = [d[0] for d in db.cursor.description]
            rows = db.cursor.fetchall()
        tickets = [dict(zip(cols, row)) for row in rows]

        for t in tickets:
            closed_at_str = ""
            if t.get('ClosedAt'):
                closed_at_str = t['ClosedAt'].strftime('%d/%m/%Y %H:%M') if hasattr(t['ClosedAt'], 'strftime') else str(t['ClosedAt'])

            msg = (
                f"{lang.get('ticket_closed_popup_header', 'Il tuo ticket è stato risolto!')}\n\n"
                f"Ticket: #{t['TicketID']}\n"
                f"{lang.get('ticket_title_label', 'Titolo')}: {t['Title']}\n"
                f"{lang.get('ticket_closed_by', 'Chiuso da')}: {t.get('ClosedByName', 'N/A')}\n"
                f"{lang.get('ticket_closed_at', 'Data chiusura')}: {closed_at_str}\n\n"
                f"{lang.get('ticket_closure_note_label', 'Nota')}: {t.get('ClosureNote', '(nessuna nota)')}"
            )
            messagebox.showinfo(
                lang.get('ticket_closed_popup_title', 'Ticket Risolto'),
                msg,
                parent=master
            )
            _mark_closure_notified(db, t['TicketID'])
            logger.info(f"[TICKET] Notifica popup mostrata per ticket #{t['TicketID']} all'utente {user_name}")

    except Exception as e:
        logger.warning(f"[TICKET] Errore controllo ticket chiusi per utente {employee_id}: {e}")


# --------------------------------------------------------------------------- #
#  Finestra apertura ticket                                                     #
# --------------------------------------------------------------------------- #

class TicketWindow(tk.Toplevel):
    """
    Finestra di ticketing. Può essere aperta manualmente (Help → Tickets)
    o automaticamente in caso di eccezione non gestita.

    Parametri:
        master        – finestra padre (MainApplication)
        db            – DatabaseHandler
        lang          – LanguageManager
        user_name     – nome utente corrente (str | None)
        error_info    – dict con chiavi 'type', 'message', 'traceback'
                        se apertura automatica da eccezione
        employee_id   – EmployeeHireHistoryId (int | None)
        work_email    – WorkEmail dell'utente (str | None)
    """

    def __init__(self, master, db, lang, user_name=None, error_info=None,
                 employee_id=None, work_email=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or ""
        self.error_info = error_info or {}
        self.employee_id = employee_id
        self.work_email = work_email or ""
        self._screenshot_path: str | None = None

        # Configurazione finestra
        title_key = "ticket_window_title" if not self.error_info else "ticket_window_title_error"
        self.title(self.lang.get(title_key, "Nuovo Ticket" if not self.error_info else "Errore – Apri Ticket"))
        self.geometry("820x700")
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

        # Utente (nome)
        ttk.Label(main, text=self.lang.get('ticket_user_label', 'Utente'),
                  font=("Helvetica", 9, "bold")).grid(row=row, column=0, sticky="nw", pady=(0, 2))
        user_display = self.user_name or "(non identificato)"
        if self.work_email:
            user_display += f"  ({self.work_email})"
        ttk.Label(main, text=user_display, foreground="#1565C0",
                  font=("Helvetica", 9)).grid(row=row, column=1, sticky="w", pady=(0, 8))
        row += 1

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
                screenshot_path=self._screenshot_path or "",
                employee_id=self.employee_id,
                work_email=self.work_email
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
                        user_name=self.user_name,
                        work_email=self.work_email
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
#  Finestra storico ticket (per l'utente)                                       #
# --------------------------------------------------------------------------- #

class TicketHistoryWindow(tk.Toplevel):
    """
    Mostra lo storico dei ticket aperti dall'utente corrente.
    """

    def __init__(self, master, db, lang, employee_id: int, user_name: str = ""):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.employee_id = employee_id
        self.user_name = user_name

        self.title(self.lang.get('ticket_history_title', 'Storico Ticket'))
        self.geometry("1050x550")
        self.minsize(900, 400)
        self.transient(master)
        self.grab_set()

        self._tickets = []
        self._build_ui()
        self._load_tickets()

        # Centra sulla finestra padre
        self.update_idletasks()
        px = master.winfo_x() + (master.winfo_width() - self.winfo_width()) // 2
        py = master.winfo_y() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")

    def _build_ui(self):
        # Header
        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill=tk.X)
        ttk.Label(header,
                  text=f"{self.lang.get('ticket_history_header', 'I tuoi Ticket')} – {self.user_name}",
                  font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)

        # Treeview
        tree_frame = ttk.Frame(self, padding=(12, 4))
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "date", "title", "type", "status", "closed_at", "closed_by", "note")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=18)

        self.tree.heading("id", text="#")
        self.tree.heading("date", text=self.lang.get('ticket_col_date', 'Data Apertura'))
        self.tree.heading("title", text=self.lang.get('ticket_col_title', 'Titolo'))
        self.tree.heading("type", text=self.lang.get('ticket_col_type', 'Tipo'))
        self.tree.heading("status", text=self.lang.get('ticket_col_status', 'Stato'))
        self.tree.heading("closed_at", text=self.lang.get('ticket_col_closed_at', 'Data Chiusura'))
        self.tree.heading("closed_by", text=self.lang.get('ticket_col_closed_by', 'Chiuso da'))
        self.tree.heading("note", text=self.lang.get('ticket_col_closure_note', 'Nota Chiusura'))

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=130, anchor="center")
        self.tree.column("title", width=250)
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("status", width=110, anchor="center")
        self.tree.column("closed_at", width=130, anchor="center")
        self.tree.column("closed_by", width=130)
        self.tree.column("note", width=200)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Tags per colori stato
        self.tree.tag_configure('open', foreground=STATUS_COLORS[STATUS_OPEN])
        self.tree.tag_configure('on_working', foreground=STATUS_COLORS[STATUS_ON_WORKING])
        self.tree.tag_configure('closed', foreground=STATUS_COLORS[STATUS_CLOSED])

        # Pulsanti
        btn_frame = ttk.Frame(self, padding=(12, 8))
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text=self.lang.get('ticket_btn_refresh', '🔄 Aggiorna'),
                   command=self._load_tickets).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=self.lang.get('button_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _load_tickets(self):
        """Carica e visualizza i ticket dell'utente."""
        self.tree.delete(*self.tree.get_children())
        self._tickets = _fetch_tickets_for_user(self.db, self.employee_id)

        for t in self._tickets:
            created = ""
            if t.get('CreatedAt'):
                created = t['CreatedAt'].strftime('%d/%m/%Y %H:%M') if hasattr(t['CreatedAt'], 'strftime') else str(t['CreatedAt'])

            closed_at = ""
            if t.get('ClosedAt'):
                closed_at = t['ClosedAt'].strftime('%d/%m/%Y %H:%M') if hasattr(t['ClosedAt'], 'strftime') else str(t['ClosedAt'])

            status = t.get('Status', STATUS_OPEN)
            status_display = self.lang.get(f'ticket_status_{status}',
                                           STATUS_LABELS.get(status, {}).get('it', status))

            err_type = t.get('ErrorType', 'manual')
            type_display = '⚠' if err_type == 'exception' else '✅'

            tag = status if status in (STATUS_OPEN, STATUS_ON_WORKING, STATUS_CLOSED) else ''

            self.tree.insert('', tk.END, values=(
                t.get('TicketID', ''),
                created,
                t.get('Title', ''),
                type_display,
                status_display,
                closed_at,
                t.get('ClosedByName', ''),
                t.get('ClosureNote', '')
            ), tags=(tag,))


# --------------------------------------------------------------------------- #
#  Finestra gestione ticket (per admin/programmatore)                           #
# --------------------------------------------------------------------------- #

class TicketManagementWindow(tk.Toplevel):
    """
    Finestra di gestione ticket per il programmatore/admin.
    Permette di visualizzare tutti i ticket, cambiare stato, chiudere con nota.
    Protetta da _execute_authorized_action.
    """

    def __init__(self, master, db, lang, admin_user_id: int = None, admin_user_name: str = ""):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.admin_user_id = admin_user_id
        self.admin_user_name = admin_user_name

        self.title(self.lang.get('ticket_manage_title', 'Gestione Ticket'))
        self.geometry("1200x650")
        self.minsize(1000, 500)
        self.transient(master)
        self.grab_set()

        self._tickets = []
        self._build_ui()
        self._load_tickets()

        # Centra
        self.update_idletasks()
        px = master.winfo_x() + (master.winfo_width() - self.winfo_width()) // 2
        py = master.winfo_y() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")

    def _build_ui(self):
        # Header
        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill=tk.X)
        ttk.Label(header,
                  text=self.lang.get('ticket_manage_header', 'Gestione Ticket – Tutti i ticket'),
                  font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)

        # Filtro stato
        filter_frame = ttk.Frame(header)
        filter_frame.pack(side=tk.RIGHT)
        ttk.Label(filter_frame, text=self.lang.get('ticket_filter_status', 'Stato:')).pack(side=tk.LEFT, padx=(0, 4))
        self.filter_var = tk.StringVar(value='all')
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, state='readonly', width=16)
        filter_values = [
            self.lang.get('ticket_filter_all', 'Tutti'),
            self.lang.get('ticket_status_open', 'Aperto'),
            self.lang.get('ticket_status_on_working', 'In Lavorazione'),
            self.lang.get('ticket_status_closed', 'Chiuso'),
        ]
        filter_combo['values'] = filter_values
        filter_combo.current(0)
        filter_combo.pack(side=tk.LEFT)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filter())
        self._filter_map = {
            filter_values[0]: 'all',
            filter_values[1]: STATUS_OPEN,
            filter_values[2]: STATUS_ON_WORKING,
            filter_values[3]: STATUS_CLOSED,
        }

        # Treeview
        tree_frame = ttk.Frame(self, padding=(12, 4))
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "date", "opened_by", "email", "title", "type", "status",
                    "closed_at", "closed_by", "note")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

        self.tree.heading("id", text="#")
        self.tree.heading("date", text=self.lang.get('ticket_col_date', 'Data Apertura'))
        self.tree.heading("opened_by", text=self.lang.get('ticket_col_opened_by', 'Aperto da'))
        self.tree.heading("email", text=self.lang.get('ticket_col_email', 'Email'))
        self.tree.heading("title", text=self.lang.get('ticket_col_title', 'Titolo'))
        self.tree.heading("type", text=self.lang.get('ticket_col_type', 'Tipo'))
        self.tree.heading("status", text=self.lang.get('ticket_col_status', 'Stato'))
        self.tree.heading("closed_at", text=self.lang.get('ticket_col_closed_at', 'Data Chiusura'))
        self.tree.heading("closed_by", text=self.lang.get('ticket_col_closed_by', 'Chiuso da'))
        self.tree.heading("note", text=self.lang.get('ticket_col_closure_note', 'Nota Chiusura'))

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("opened_by", width=150)
        self.tree.column("email", width=150)
        self.tree.column("title", width=200)
        self.tree.column("type", width=55, anchor="center")
        self.tree.column("status", width=110, anchor="center")
        self.tree.column("closed_at", width=120, anchor="center")
        self.tree.column("closed_by", width=130)
        self.tree.column("note", width=200)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Tags per colori stato
        self.tree.tag_configure('open', foreground=STATUS_COLORS[STATUS_OPEN])
        self.tree.tag_configure('on_working', foreground=STATUS_COLORS[STATUS_ON_WORKING])
        self.tree.tag_configure('closed', foreground=STATUS_COLORS[STATUS_CLOSED])

        # Pulsanti azione
        btn_frame = ttk.Frame(self, padding=(12, 8))
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame,
                   text=self.lang.get('ticket_btn_set_working', '🔧 In Lavorazione'),
                   command=lambda: self._change_status(STATUS_ON_WORKING)).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('ticket_btn_close_ticket', '✅ Chiudi Ticket'),
                   command=self._close_ticket).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('ticket_btn_reopen', '🔄 Riapri'),
                   command=lambda: self._change_status(STATUS_OPEN)).pack(side=tk.LEFT, padx=4)

        ttk.Separator(btn_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Button(btn_frame,
                   text=self.lang.get('ticket_btn_view_detail', '📋 Dettagli'),
                   command=self._view_detail).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('ticket_btn_refresh', '🔄 Aggiorna'),
                   command=self._load_tickets).pack(side=tk.LEFT, padx=4)

        ttk.Button(btn_frame,
                   text=self.lang.get('button_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

        # Doppio clic per dettagli
        self.tree.bind('<Double-Button-1>', lambda e: self._view_detail())

    def _load_tickets(self):
        """Carica tutti i ticket dal DB."""
        self.tree.delete(*self.tree.get_children())
        self._tickets = _fetch_all_tickets(self.db)
        self._display_tickets(self._tickets)

    def _display_tickets(self, tickets):
        """Mostra i ticket nel treeview."""
        self.tree.delete(*self.tree.get_children())
        for t in tickets:
            created = ""
            if t.get('CreatedAt'):
                created = t['CreatedAt'].strftime('%d/%m/%Y %H:%M') if hasattr(t['CreatedAt'], 'strftime') else str(t['CreatedAt'])

            closed_at = ""
            if t.get('ClosedAt'):
                closed_at = t['ClosedAt'].strftime('%d/%m/%Y %H:%M') if hasattr(t['ClosedAt'], 'strftime') else str(t['ClosedAt'])

            status = t.get('Status', STATUS_OPEN)
            status_display = self.lang.get(f'ticket_status_{status}',
                                           STATUS_LABELS.get(status, {}).get('it', status))

            err_type = t.get('ErrorType', 'manual')
            type_display = '⚠' if err_type == 'exception' else '✅'

            tag = status if status in (STATUS_OPEN, STATUS_ON_WORKING, STATUS_CLOSED) else ''

            self.tree.insert('', tk.END, values=(
                t.get('TicketID', ''),
                created,
                t.get('OpenedByName', ''),
                t.get('OpenedByEmail', ''),
                t.get('Title', ''),
                type_display,
                status_display,
                closed_at,
                t.get('ClosedByName', ''),
                t.get('ClosureNote', '')
            ), tags=(tag,))

    def _apply_filter(self):
        """Applica il filtro per stato."""
        selected_label = self.filter_var.get()
        status_filter = None
        for label, status_val in self._filter_map.items():
            if label == selected_label:
                status_filter = status_val
                break

        if status_filter == 'all' or status_filter is None:
            self._display_tickets(self._tickets)
        else:
            filtered = [t for t in self._tickets if t.get('Status') == status_filter]
            self._display_tickets(filtered)

    def _get_selected_ticket(self):
        """Restituisce il dict del ticket selezionato o None."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warn_title', 'Attenzione'),
                self.lang.get('ticket_select_one', 'Selezionare un ticket dalla lista.'),
                parent=self
            )
            return None
        values = self.tree.item(sel[0], 'values')
        ticket_id = int(values[0])
        # Cerca nei dati originali
        for t in self._tickets:
            if t.get('TicketID') == ticket_id:
                return t
        return None

    def _change_status(self, new_status: str):
        """Cambia lo stato del ticket selezionato."""
        ticket = self._get_selected_ticket()
        if not ticket:
            return

        ticket_id = ticket['TicketID']
        current_status = ticket.get('Status', STATUS_OPEN)

        if current_status == new_status:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('ticket_already_status', f"Il ticket è già nello stato '{new_status}'."),
                parent=self
            )
            return

        if current_status == STATUS_CLOSED and new_status != STATUS_OPEN:
            messagebox.showwarning(
                self.lang.get('warn_title', 'Attenzione'),
                self.lang.get('ticket_closed_cannot_change', 'Un ticket chiuso può solo essere riaperto.'),
                parent=self
            )
            return

        success = _update_ticket_status(self.db, ticket_id, new_status)
        if success:
            self._load_tickets()
        else:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('ticket_status_update_error', 'Errore durante il cambio stato del ticket.'),
                parent=self
            )

    def _close_ticket(self):
        """Chiude il ticket selezionato con nota di chiusura e notifica."""
        ticket = self._get_selected_ticket()
        if not ticket:
            return

        ticket_id = ticket['TicketID']
        current_status = ticket.get('Status', STATUS_OPEN)

        if current_status == STATUS_CLOSED:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('ticket_already_closed', 'Il ticket è già chiuso.'),
                parent=self
            )
            return

        # Finestra per nota di chiusura
        close_dialog = tk.Toplevel(self)
        close_dialog.title(self.lang.get('ticket_close_dialog_title', f'Chiudi Ticket #{ticket_id}'))
        close_dialog.geometry("550x320")
        close_dialog.transient(self)
        close_dialog.grab_set()

        # Centra
        close_dialog.update_idletasks()
        px = self.winfo_x() + (self.winfo_width() - close_dialog.winfo_width()) // 2
        py = self.winfo_y() + (self.winfo_height() - close_dialog.winfo_height()) // 2
        close_dialog.geometry(f"+{px}+{py}")

        main_f = ttk.Frame(close_dialog, padding=12)
        main_f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_f,
                  text=f"{self.lang.get('ticket_closing_header', 'Chiusura Ticket')} #{ticket_id}",
                  font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(0, 4))

        ttk.Label(main_f,
                  text=f"{self.lang.get('ticket_col_title', 'Titolo')}: {ticket.get('Title', '')}",
                  font=("Helvetica", 9)).pack(anchor="w", pady=(0, 4))

        ttk.Label(main_f,
                  text=f"{self.lang.get('ticket_col_opened_by', 'Aperto da')}: {ticket.get('OpenedByName', '')}",
                  font=("Helvetica", 9)).pack(anchor="w", pady=(0, 8))

        ttk.Label(main_f,
                  text=self.lang.get('ticket_closure_note_label', 'Nota di risoluzione (*):'),
                  font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(0, 2))

        note_text = tk.Text(main_f, height=6, wrap=tk.WORD, font=("Helvetica", 9))
        note_text.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        def do_close():
            note = note_text.get("1.0", tk.END).strip()
            if not note:
                messagebox.showwarning(
                    self.lang.get('warn_title', 'Attenzione'),
                    self.lang.get('ticket_closure_note_required',
                                  'Inserire una nota di risoluzione per chiudere il ticket.'),
                    parent=close_dialog
                )
                return

            success = _update_ticket_status(
                self.db, ticket_id, STATUS_CLOSED,
                closed_by_id=self.admin_user_id,
                closed_by_name=self.admin_user_name,
                closure_note=note
            )

            if not success:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('ticket_close_error', 'Errore durante la chiusura del ticket.'),
                    parent=close_dialog
                )
                return

            # Notifica email se l'utente ha un indirizzo email
            opener_email = ticket.get('OpenedByEmail', '').strip()
            if opener_email:
                try:
                    _send_closure_email(
                        db=self.db,
                        ticket_id=ticket_id,
                        recipient_email=opener_email,
                        ticket_title=ticket.get('Title', ''),
                        closure_note=note,
                        closed_by_name=self.admin_user_name
                    )
                    _mark_closure_notified(self.db, ticket_id)
                    logger.info(f"[TICKET] Email chiusura inviata per ticket #{ticket_id} → {opener_email}")
                except Exception as mail_err:
                    logger.error(f"[TICKET] Email chiusura fallita per ticket #{ticket_id}: {mail_err}", exc_info=True)
                    # Non bloccare la chiusura se l'email fallisce
                    # La notifica popup avverrà al prossimo login
            else:
                logger.info(f"[TICKET] Ticket #{ticket_id} chiuso. Nessuna email per l'utente – notifica popup al prossimo login.")

            close_dialog.destroy()
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('ticket_closed_ok', f'Ticket #{ticket_id} chiuso con successo.').replace('{id}', str(ticket_id)),
                parent=self
            )
            self._load_tickets()

        btn_f = ttk.Frame(main_f)
        btn_f.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(btn_f,
                   text=self.lang.get('ticket_btn_confirm_close', '✅ Conferma Chiusura'),
                   command=do_close).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_f,
                   text=self.lang.get('button_cancel', 'Annulla'),
                   command=close_dialog.destroy).pack(side=tk.RIGHT, padx=4)

    def _view_detail(self):
        """Mostra la descrizione completa del ticket selezionato."""
        ticket = self._get_selected_ticket()
        if not ticket:
            return

        detail_win = tk.Toplevel(self)
        detail_win.title(f"Ticket #{ticket.get('TicketID', '')}")
        detail_win.geometry("700x500")
        detail_win.transient(self)
        detail_win.grab_set()

        detail_win.update_idletasks()
        px = self.winfo_x() + (self.winfo_width() - detail_win.winfo_width()) // 2
        py = self.winfo_y() + (self.winfo_height() - detail_win.winfo_height()) // 2
        detail_win.geometry(f"+{px}+{py}")

        main_f = ttk.Frame(detail_win, padding=12)
        main_f.pack(fill=tk.BOTH, expand=True)

        # Header info
        info_text = f"#{ticket.get('TicketID', '')}"
        created = ticket.get('CreatedAt', '')
        if created and hasattr(created, 'strftime'):
            created = created.strftime('%d/%m/%Y %H:%M')
        info_text += f"  |  {created}"
        info_text += f"  |  {ticket.get('OpenedByName', '')}"

        ttk.Label(main_f, text=info_text,
                  font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 4))

        ttk.Label(main_f, text=ticket.get('Title', ''),
                  font=("Helvetica", 11)).pack(anchor="w", pady=(0, 8))

        # Stato con colore
        status = ticket.get('Status', STATUS_OPEN)
        status_display = self.lang.get(f'ticket_status_{status}',
                                       STATUS_LABELS.get(status, {}).get('it', status))
        ttk.Label(main_f, text=f"Stato: {status_display}",
                  foreground=STATUS_COLORS.get(status, '#333'),
                  font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 8))

        # Descrizione
        ttk.Label(main_f, text=self.lang.get('ticket_description_label', 'Descrizione:'),
                  font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(0, 2))
        desc_text = tk.Text(main_f, height=10, wrap=tk.WORD, font=("Helvetica", 9),
                           state=tk.NORMAL)
        desc_text.insert("1.0", ticket.get('Description', ''))
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        # Nota chiusura (se presente)
        if ticket.get('ClosureNote'):
            ttk.Label(main_f, text=self.lang.get('ticket_closure_note_label', 'Nota di risoluzione:'),
                      font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(0, 2))
            note_text = tk.Text(main_f, height=4, wrap=tk.WORD, font=("Helvetica", 9),
                               bg="#E8F5E9", state=tk.NORMAL)
            note_text.insert("1.0", ticket.get('ClosureNote', ''))
            note_text.config(state=tk.DISABLED)
            note_text.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(main_f, text=self.lang.get('button_close', 'Chiudi'),
                   command=detail_win.destroy).pack(side=tk.RIGHT)


# --------------------------------------------------------------------------- #
#  Entry point pubblico                                                         #
# --------------------------------------------------------------------------- #

def open_ticket_window(master, db, lang, user_name=None, error_info=None,
                       employee_id=None, work_email=None):
    """
    Apre la finestra ticket.
    Chiamata da menu (error_info=None) o da sys.excepthook (error_info=dict).
    """
    try:
        TicketWindow(master, db, lang, user_name, error_info, employee_id, work_email)
    except Exception as e:
        logger.error(f"[TICKET] Impossibile aprire TicketWindow: {e}", exc_info=True)
        # Fallback minimal: almeno logga
        messagebox.showerror(
            "Errore Ticketing",
            f"Impossibile aprire la finestra ticket: {e}",
            parent=master
        )
