# -*- coding: utf-8 -*-
"""
incoming_monitor.py
Monitor in-app dei popup del modulo "Ricezione" (Incoming).

Riusa il meccanismo condiviso dei popup (Traceability_RS.dbo.kit_popup_queue,
categorie 'INCOMING' e 'INCOMING_ANSWER') gia' usato dal Kit Preparation
(vedi kit_popup_monitor.py). Polling ogni 10 secondi:

  - target 'INCOMING_RECEIVER' -> mostrato solo sui PC con ruolo "receiver"
    (incoming_workstation_config.is_incoming_receiver): nuove richieste,
    reminder ed escalation.
  - target 'INCOMING_SENDER'   -> mostrato solo sui PC con ruolo "sender".
  - target <hostname>          -> mostrato solo su quel PC (es. risposta
    pronta per il richiedente, category='INCOMING_ANSWER').

Il claim e' atomico (UPDATE ... WHERE displayed_date IS NULL): un popup
viene mostrato una sola volta anche con piu' postazioni dello stesso ruolo
attive. Le richieste in escalation (PENDING da >= 120 min senza popup di
escalation da >= 30 min) vengono rilevate dal monitor stesso sulle
postazioni receiver e notificate con popup + email (incoming_email).
"""
import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk

try:
    from .incoming_workstation_config import is_incoming_receiver, is_incoming_sender
except ImportError:  # esecuzione come script standalone
    from incoming_workstation_config import is_incoming_receiver, is_incoming_sender

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 10_000
CATEGORIES = ('INCOMING', 'INCOMING_ANSWER')


def _cursor(db):
    """Cursor uniforme: funziona con la classe Database di main.py e con
    BackgroundDatabase del servizio background."""
    if hasattr(db, '_ensure_connection'):
        try:
            db._ensure_connection()
        except Exception:
            pass
    return db.cursor


class IncomingMonitor:
    """Monitor background popup del modulo Ricezione (tutti i PC)."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info("IncomingMonitor avviato su %s (receiver=%s, sender=%s)",
                    self.hostname, is_incoming_receiver(), is_incoming_sender())
        self._poll()

    def stop(self):
        self._running = False

    # ------------------------------------------------------------------ #
    #  Polling                                                             #
    # ------------------------------------------------------------------ #
    def _poll(self):
        if not self._running:
            return
        try:
            self._check_escalations()
            if not self._popup_open:
                self._check_queue()
        except Exception as e:
            logger.error("IncomingMonitor polling error: %s", e, exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _targets(self):
        targets = [self.hostname]
        if is_incoming_receiver():
            targets.append('INCOMING_RECEIVER')
        if is_incoming_sender():
            targets.append('INCOMING_SENDER')
        return targets

    def _check_queue(self):
        targets = self._targets()
        placeholders = ','.join('?' * len(targets))
        cat_ph = ','.join('?' * len(CATEGORIES))
        query = (f"SELECT TOP 10 id, title, message, order_number, created_date, category "
                 f"FROM Traceability_RS.dbo.kit_popup_queue "
                 f"WHERE displayed_date IS NULL AND target IN ({placeholders}) "
                 f"AND category IN ({cat_ph}) "
                 f"ORDER BY created_date ASC")
        params = tuple(targets) + CATEGORIES
        if hasattr(self.db, 'fetch_all'):
            rows = self.db.fetch_all(query, params)
        else:
            with self.db._lock:
                cur = _cursor(self.db)
                cur.execute(query, params)
                rows = cur.fetchall()
        if not rows:
            return

        # Claim atomico riga per riga: vince una sola postazione
        claimed = []
        with self.db._lock:
            cur = _cursor(self.db)
            for row in rows:
                cur.execute(
                    "UPDATE Traceability_RS.dbo.kit_popup_queue "
                    "SET displayed_date = GETDATE(), displayed_on = ? "
                    "WHERE id = ? AND displayed_date IS NULL",
                    (self.hostname, row[0])
                )
                if cur.rowcount > 0:
                    claimed.append(row)
            self.db.conn.commit()
        if claimed:
            self._show_popup(claimed)

    # ------------------------------------------------------------------ #
    #  Escalation (solo postazioni receiver)                               #
    # ------------------------------------------------------------------ #
    def _check_escalations(self):
        """Rileva richieste PENDENTI da troppo tempo e notifica popup + email.
        Delegato a incoming_email.process_escalations (claim atomico via
        LastEscalationPopup): sicuro anche se eseguito su piu' PC receiver."""
        if not is_incoming_receiver():
            return
        try:
            try:
                from .incoming_email import process_escalations
            except ImportError:  # esecuzione come script standalone
                from incoming_email import process_escalations
            process_escalations(self.db)
        except Exception as e:
            logger.error("IncomingMonitor escalation check error: %s", e, exc_info=True)

    # ------------------------------------------------------------------ #
    #  Popup                                                               #
    # ------------------------------------------------------------------ #
    def _show_popup(self, rows):
        self._popup_open = True
        self._play_alert_sound()

        popup = tk.Toplevel(self.master)
        popup.title(self.lang.get('incoming_popup_title', '🔔 Ricezione — Richieste Incoming'))
        popup.geometry("580x380")
        popup.attributes('-topmost', True)
        popup.configure(bg='#2c3e50')

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill='both')

        for row in rows:
            _, title, message, order_number, created = row[0], row[1], row[2], row[3], row[4]
            created_str = created.strftime('%d/%m/%Y %H:%M') if created else ''
            ttk.Label(main, text=title, font=("Segoe UI", 11, "bold"),
                      foreground="#c0392b").pack(anchor='w', pady=(4, 0))
            ttk.Label(main, text=message, font=("Segoe UI", 10),
                      wraplength=520, justify='left').pack(anchor='w')
            ttk.Label(main, text=created_str, font=("Segoe UI", 8, "italic"),
                      foreground='#777').pack(anchor='w', pady=(0, 6))

        has_answer = any(len(row) > 5 and row[5] == 'INCOMING_ANSWER' for row in rows)
        has_request = any(len(row) > 5 and row[5] == 'INCOMING' for row in rows)

        def on_close():
            self._popup_open = False
            popup.destroy()

        if has_request:
            def _open_solutions():
                on_close()
                try:
                    opener = getattr(self.master, 'open_incoming_soluzioni_with_login', None)
                    if callable(opener):
                        # Via menu principale: login/autorizzazione 'incoming_soluzioni'
                        opener()
                        return
                except Exception as e:
                    logger.error("Apertura Soluzioni con login fallita: %s", e,
                                 exc_info=True)
                try:
                    from .incoming_solutions_gui import open_incoming_solutions
                except ImportError:  # esecuzione come script standalone
                    from incoming_solutions_gui import open_incoming_solutions
                try:
                    open_incoming_solutions(self.master, self.db, self.lang)
                except Exception as e:
                    logger.error("Apertura finestra soluzioni incoming fallita: %s", e,
                                 exc_info=True)

            ttk.Button(main,
                       text=self.lang.get('incoming_popup_open_solutions',
                                          'Apri Soluzioni (leggi note / rispondi)'),
                       command=_open_solutions).pack(pady=(8, 0))

        if has_answer:
            def _open_confirm():
                on_close()
                try:
                    from .incoming_confirm_gui import open_incoming_confirm
                except ImportError:  # esecuzione come script standalone
                    from incoming_confirm_gui import open_incoming_confirm
                try:
                    open_incoming_confirm(self.master, self.db, self.lang)
                except Exception as e:
                    logger.error("Apertura finestra conferma incoming fallita: %s", e,
                                 exc_info=True)

            ttk.Button(main,
                       text=self.lang.get('incoming_popup_open_confirm',
                                          'Apri finestra conferma soluzione'),
                       command=_open_confirm).pack(pady=(8, 0))

        ttk.Button(main, text=self.lang.get('incoming_popup_ack', 'OK — Presa visione'),
                   command=on_close).pack(pady=8)
        popup.protocol('WM_DELETE_WINDOW', on_close)

    @staticmethod
    def _play_alert_sound():
        def _beep():
            try:
                import winsound
                for _ in range(3):
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    time.sleep(0.4)
            except Exception:
                pass
        threading.Thread(target=_beep, daemon=True).start()
