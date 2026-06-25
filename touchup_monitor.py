# -*- coding: utf-8 -*-
"""
touchup_monitor.py
Monitor background per le postazioni Touch-Up (marker touchup_host.json).
Mostra un popup quando ci sono segnalazioni NEW/REOPENED instradate ai reparti
della postazione. Ricompare ogni N minuti (configurabile). Popup piu' marcato
sulle riaperture/escalation. Stesso pattern di orders/shipment_monitor.py.
"""
import tkinter as tk
from tkinter import ttk
import logging
import os
import sys
import json
import time
import winsound
import threading

import touchup_logic as tl
from touchup_workstation_config import is_touchup_workstation, get_touchup_departments

logger = logging.getLogger(__name__)

DEFAULT_POLL_SECONDS = 60
DEFAULT_REAPPEAR_MIN = 5
CONFIG_FILENAME = "touchup_monitor_config.json"


def _executable_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def _config_path():
    return os.path.join(_executable_dir(), CONFIG_FILENAME)


def _read_config():
    path = _config_path()
    poll, reappear = DEFAULT_POLL_SECONDS, DEFAULT_REAPPEAR_MIN
    try:
        if not os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"polling_seconds": poll, "reappear_minutes": reappear}, f, indent=4)
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            poll = int(data.get("polling_seconds", poll)) or poll
            reappear = int(data.get("reappear_minutes", reappear)) or reappear
    except Exception as e:
        logger.warning(f"TouchUpMonitor config non leggibile ({e}); default")
    return max(15, poll), max(1, reappear)


class TouchUpMonitor:
    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self._running = True
        self._popup_open = False
        self._last_popup_shown = 0.0
        logger.info("TouchUpMonitor avviato")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            if not is_touchup_workstation():
                # postazione non attiva: ricontrolla periodicamente
                self.master.after(60_000, self._poll)
                return
            self._check_pending()
        except Exception as e:
            logger.error(f"TouchUpMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                poll_s, _ = _read_config()
                self.master.after(poll_s * 1000, self._poll)

    def _check_pending(self):
        if self._popup_open:
            return
        _, reappear_min = _read_config()
        if self._last_popup_shown and (time.monotonic() - self._last_popup_shown) < reappear_min * 60:
            return
        cdc_ids, sub_ids = get_touchup_departments()
        try:
            rows = tl.get_pending_reports(self.db, cdc_ids, sub_ids)
        except Exception as e:
            logger.error(f"TouchUpMonitor query error: {e}", exc_info=True)
            return
        if not rows:
            return
        self._last_popup_shown = time.monotonic()
        self.master.after(0, lambda r=rows: self._show_popup(r))

    def _show_popup(self, rows):
        self._popup_open = True
        has_strong = any((r.get('Status') == 'REOPENED' or (r.get('EscalationLevel') or 0) >= 1) for r in rows)
        beeps = 5 if has_strong else 3
        threading.Thread(target=lambda: [winsound.Beep(1000, 350) for _ in range(beeps)], daemon=True).start()

        popup = tk.Toplevel(self.master)
        popup.title(self.lang.get("tu_popup_title", "⚠️ TOUCH-UP - Segnalazioni da gestire"))
        popup.geometry("760x440")
        popup.attributes("-topmost", True)
        popup.configure(bg="#922b21" if has_strong else "#c0392b")
        popup.grab_set()

        def _close():
            self._popup_open = False
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", _close)

        tk.Label(popup, text=self.lang.get("tu_popup_header", "{0} segnalazione/i da prendere in carico").format(len(rows)),
                 bg=popup["bg"], fg="white", font=("Segoe UI", 14, "bold")).pack(pady=(12, 4))
        if has_strong:
            tk.Label(popup, text=self.lang.get("tu_popup_strong", "Sono presenti RIAPERTURE / ricorrenze: priorità ALTA"),
                     bg=popup["bg"], fg="#f9e79f", font=("Segoe UI", 10, "bold")).pack()

        btnf = tk.Frame(popup, bg=popup["bg"])
        btnf.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        ttk.Button(btnf, text=self.lang.get("tu_popup_open", "📋 Apri Soluzioni adottate"),
                   command=lambda: [_close(), self._open_response()]).pack(side=tk.LEFT, padx=20)
        ttk.Button(btnf, text=self.lang.get("btn_close", "Chiudi"), command=_close).pack(side=tk.RIGHT, padx=20)

        fr = ttk.Frame(popup)
        fr.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        cols = ("id", "stato", "data", "esc", "riap")
        tree = ttk.Treeview(fr, columns=cols, show="headings", height=10)
        for c, t, w in (("id", "N.", 60), ("stato", "Stato", 110), ("data", "Creata", 150),
                        ("esc", "Escalation", 90), ("riap", "Riaperture", 90)):
            tree.heading(c, text=t)
            tree.column(c, width=w, anchor="center")
        for r in rows:
            d = r['CreatedAt'].strftime('%d/%m/%Y %H:%M') if r.get('CreatedAt') else ''
            tree.insert("", tk.END, values=(r['TouchUpReportId'], r.get('Status'), d,
                                            r.get('EscalationLevel'), r.get('ReopenCount')))
        tree.pack(fill=tk.BOTH, expand=True)

    def _open_response(self):
        try:
            opener = getattr(self.master, "_open_touchup_response", None)
            if callable(opener):
                opener()
                return
            import touchup_response_gui
            user_name = getattr(self.master, "last_authenticated_user_name", "Unknown")
            touchup_response_gui.open_touchup_response(self.master, self.db, self.lang, user_name)
        except Exception as e:
            logger.error(f"TouchUpMonitor apertura risposte: {e}", exc_info=True)
