"""
kit_popup_monitor.py
Monitor in-app dei popup del modulo Kit Preparation — Sprint 3
(spec §7.2: riusa il meccanismo dei materiali indiretti, categoria DIRECT_MATERIAL).

Polling di kit_popup_queue ogni 10s:
  - target 'KIT_PREP' -> mostrato solo sui PC con kit_prep_host.json (Formazione Kit)
  - target 'KIT_PROD' -> mostrato solo sui PC con kit_prod_host.json (Ricezione Kit Produzione)
  - target <hostname>  -> mostrato solo su quel PC (richiedente)
Il claim e' atomico (UPDATE ... WHERE displayed_date IS NULL): un popup
viene mostrato una sola volta anche con piu' postazioni dello stesso ruolo attive.
"""
import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk

from kit_workstation_config import is_kit_prep_workstation, is_kit_prod_workstation
from kit_dashboard import server_config

logger = logging.getLogger("PlanMonitor")

POLL_INTERVAL_MS = 10_000


class KitPopupMonitor:
    """Monitor background popup Kit Preparation (tutti i PC)."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info("KitPopupMonitor avviato su %s (kit_prep=%s, kit_prod=%s)",
                    self.hostname, is_kit_prep_workstation(), is_kit_prod_workstation())
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            if not self._popup_open:
                self._check_queue()
        except Exception as e:
            logger.error("KitPopupMonitor polling error: %s", e, exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _targets(self):
        targets = [self.hostname]
        if is_kit_prep_workstation():
            targets.append('KIT_PREP')
        if is_kit_prod_workstation():
            targets.append('KIT_PROD')
        return targets

    def _check_queue(self):
        targets = self._targets()
        placeholders = ','.join('?' * len(targets))
        params = list(targets)
        # Se l'avviso "server down" è silenziato su questo PC, NON pescare quelle
        # righe (così le claima un altro PC non silenziato; il claim resta atomico).
        muted_clause = ""
        if server_config.is_alert_muted():
            muted_clause = "AND category <> ? "
            params.append(server_config.CATEGORY_SERVER_DOWN)
        query = (f"SELECT TOP 10 id, title, message, order_number, created_date, category "
                 f"FROM Traceability_RS.dbo.kit_popup_queue "
                 f"WHERE displayed_date IS NULL AND target IN ({placeholders}) "
                 f"{muted_clause}"
                 f"ORDER BY created_date ASC")
        if hasattr(self.db, 'fetch_all'):
            rows = self.db.fetch_all(query, tuple(params))
        else:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
        if not rows:
            return

        # Claim atomico riga per riga: vince una sola postazione
        claimed = []
        for row in rows:
            ok = self.db.execute_query(
                "UPDATE Traceability_RS.dbo.kit_popup_queue "
                "SET displayed_date = GETDATE(), displayed_on = ? "
                "WHERE id = ? AND displayed_date IS NULL",
                (self.hostname, row[0])
            )
            if ok:
                claimed.append(row)
        if claimed:
            self._show_popup(claimed)

    def _show_popup(self, rows):
        self._popup_open = True
        self._play_alert_sound()

        popup = tk.Toplevel(self.master)
        popup.title(self.lang.get('kit_popup_title', '🔔 Kit Preparation'))
        popup.geometry("560x360")
        popup.attributes('-topmost', True)
        popup.configure(bg='#2c3e50')

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill='both')

        has_server_down = False
        for row in rows:
            _, title, message, order_number, created = row[0], row[1], row[2], row[3], row[4]
            category = row[5] if len(row) > 5 else None
            if category == server_config.CATEGORY_SERVER_DOWN:
                has_server_down = True
            created_str = created.strftime('%d/%m/%Y %H:%M') if created else ''
            ttk.Label(main, text=title, font=("Segoe UI", 11, "bold"),
                      foreground="#c0392b").pack(anchor='w', pady=(4, 0))
            ttk.Label(main, text=message, font=("Segoe UI", 10),
                      wraplength=500, justify='left').pack(anchor='w')
            ttk.Label(main, text=created_str, font=("Segoe UI", 8, "italic"),
                      foreground='#777').pack(anchor='w', pady=(0, 6))

        # Checkbox di silenziamento: solo per l'avviso "server non raggiungibile"
        mute_var = tk.BooleanVar(value=False)
        if has_server_down:
            ttk.Checkbutton(
                main,
                text=self.lang.get('kit_alert_mute',
                                   'Non mostrare in seguito questo avviso su questo PC'),
                variable=mute_var
            ).pack(anchor='w', pady=(6, 0))

        def on_close():
            if has_server_down and mute_var.get():
                try:
                    server_config.set_alert_muted(True)
                    logger.info("Avviso Kit Dashboard silenziato su questo PC")
                except Exception as e:
                    logger.warning("Silenziamento avviso fallito: %s", e)
            self._popup_open = False
            popup.destroy()

        ttk.Button(main, text=self.lang.get('kit_popup_ack', 'OK — Presa visione'),
                   command=on_close).pack(pady=8)
        popup.protocol("WM_DELETE_WINDOW", on_close)

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
