"""
indirect_materials_wh_monitor.py
Monitor background per WH WorkStation: polling nuove richieste + popup + conferma.
Gira su PC con wh_host.json presente.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import socket
import os
import json
import winsound
import time
import threading
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 10_000         # Polling ogni 10s
RE_NOTIFY_MINUTES = 5             # Ri-notifica se non azionato dopo 5 min

# Path wh_host.json
WH_HOST_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
WH_HOST_FILE = os.path.join(WH_HOST_DIR, "wh_host.json")


def is_wh_workstation():
    """Controlla se questo PC è un WH WorkStation."""
    return os.path.isfile(WH_HOST_FILE)


class WHMonitor:
    """Monitor background che controlla nuove richieste materiali."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info(f"WHMonitor avviato su {self.hostname}")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            self._check_new_requests()
        except Exception as e:
            logger.error(f"WHMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check_new_requests(self):
        """Controlla richieste con stato RICHIESTA da notificare.
        Raccoglie TUTTE le richieste pendenti in un batch e mostra un unico popup
        con un unico PDF — evita N documenti separati per N materiali.
        """
        if self._popup_open:
            return

        # Recupera TUTTE le richieste pendenti (non solo una)
        query = """
            SELECT r.RichiestaId, m.CodiceMateriale, m.DescrizioneMateriale,
                   r.QtaRichiesta, r.RichiestoDa, r.DataRichiesta,
                   r.ComputerRichiedente
            FROM ind.MaterialiRichieste r
            JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            WHERE r.Stato = 'RICHIESTA'
              AND (r.DataUltimaNotificaWH IS NULL
                   OR DATEDIFF(MINUTE, r.DataUltimaNotificaWH, GETDATE()) >= ?)
            ORDER BY r.DataRichiesta ASC
        """
        if hasattr(self.db, 'fetch_all'):
            rows = self.db.fetch_all(query, (RE_NOTIFY_MINUTES,))
        else:
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(query, (RE_NOTIFY_MINUTES,))
                rows = self.db.cursor.fetchall()

        if rows:
            # Aggiorna timestamp notifica per tutti i record del batch
            for row in rows:
                self.db.execute_query(
                    "UPDATE ind.MaterialiRichieste SET DataUltimaNotificaWH = GETDATE() WHERE RichiestaId = ?",
                    (row[0],)
                )
            # Mostra un unico popup per l'intero batch
            self._show_request_popup(rows)

    def _show_request_popup(self, requests):
        """Mostra popup con TUTTE le richieste del batch + beep.

        Args:
            requests: list of rows — tutti i materiali in attesa.
        """
        self._popup_open = True
        rids = [r[0] for r in requests]
        richiedente = requests[0][4] or ''
        data_richiesta = requests[0][5]
        computer_rich = requests[0][6] or ''

        # Beep di avviso (3 volte suono di sistema Windows)
        self._play_alert_sound()

        # Popup
        popup = tk.Toplevel(self.master)
        popup.title(f"\u26a0\ufe0f CERERE DE MATERIAL ({len(rids)} materiale)")
        popup.geometry("560x420")
        popup.attributes('-topmost', True)
        popup.configure(bg='#e74c3c')
        popup.grab_set()

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill="both")

        data_str = data_richiesta.strftime('%d/%m/%Y %H:%M') if data_richiesta else ''
        ttk.Label(
            main,
            text=f"\u26a0\ufe0f NOU\u0102 CERERE DE MATERIAL! ({len(rids)} materiale)",
            font=("Segoe UI", 13, "bold"),
            foreground="#e74c3c"
        ).pack(pady=(0, 5))

        ttk.Label(
            main,
            text=f"Solicitant: {richiedente}   |   Data: {data_str}   |   PC: {computer_rich}",
            font=("Segoe UI", 9)
        ).pack(pady=(0, 8))

        # Lista materiali
        cols = ('codice', 'descrizione', 'qty')
        tree = ttk.Treeview(main, columns=cols, show='headings', height=min(len(requests), 8))
        tree.heading('codice', text='Cod')
        tree.heading('descrizione', text='Descriere')
        tree.heading('qty', text='Cantitate')
        tree.column('codice', width=100)
        tree.column('descrizione', width=280)
        tree.column('qty', width=80, anchor='e')
        for r in requests:
            tree.insert('', 'end', values=(r[1] or '', r[2] or '', f"{r[3]:.2f}" if r[3] else '-'))
        tree.pack(fill='both', expand=True, pady=(0, 10))

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=5)

        def on_prepare():
            self._prepare_request(rids, popup)

        def on_dismiss():
            self._popup_open = False
            popup.destroy()

        ttk.Button(
            btn_frame,
            text=self.lang.get('ind_wh_btn_prepare', '\u2705 Preg\u0103te\u0219te \u0219i Confirm\u0103'),
            command=on_prepare
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('ind_wh_btn_print_only', '\U0001f5a8\ufe0f Stampea\u017b\u0103'),
            command=lambda: self._print_request(rids)
        ).pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(
            btn_frame,
            text=self.lang.get('ind_wh_btn_dismiss', '\xcenchide'),
            command=on_dismiss
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        popup.protocol("WM_DELETE_WINDOW", on_dismiss)

    def _prepare_request(self, richiesta_ids, popup):
        """Conferma preparazione per tutti gli ID del batch, stampa un unico PDF.

        Args:
            richiesta_ids: list[int] — tutti gli ID del batch da confermare
        """
        try:
            prepared = []
            for rid in richiesta_ids:
                success = self.db.execute_query(
                    """UPDATE ind.MaterialiRichieste
                       SET Stato = 'PRONTA',
                           DataPreparazione = GETDATE(),
                           PreparatoDa = ?,
                           ComputerPreparatore = ?
                       WHERE RichiestaId = ? AND Stato = 'RICHIESTA'""",
                    (self.lang.get('current_user', 'WH'), self.hostname, rid)
                )
                if success:
                    prepared.append(rid)

            if prepared:
                # Genera e stampa un UNICO PDF per tutti i materiali confermati
                self._print_request(prepared)
                logger.info(f"Batch {prepared} confermato e stampato in un unico PDF")

        except Exception as e:
            logger.error(f"Errore conferma batch richieste: {e}", exc_info=True)

        self._popup_open = False
        popup.destroy()

    def _print_request(self, richiesta_ids):
        """Stampa un UNICO PDF per tutti gli ID del batch.

        Args:
            richiesta_ids: int o list[int]
        """
        try:
            from indirect_materials_pdf import generate_and_print_batch_pdf
            if isinstance(richiesta_ids, int):
                richiesta_ids = [richiesta_ids]
            generate_and_print_batch_pdf(self.db, richiesta_ids, print_now=True)
        except Exception as e:
            logger.error(f"Errore stampa batch richieste {richiesta_ids}: {e}", exc_info=True)

    @staticmethod
    def _play_alert_sound():
        """Suona il suono di sistema Windows 3 volte in un thread separato."""
        def _beep():
            try:
                for _ in range(3):
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    time.sleep(0.4)
            except Exception:
                pass
        threading.Thread(target=_beep, daemon=True).start()


class RequesterMonitor:
    """Monitor background per il PC richiedente: notifica quando il materiale è pronto."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info(f"RequesterMonitor avviato su {self.hostname}")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            self._check_ready_requests()
        except Exception as e:
            logger.error(f"RequesterMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check_ready_requests(self):
        """Controlla se ci sono richieste PRONTA da questo computer."""
        if self._popup_open:
            return

        query = """
            SELECT r.RichiestaId, m.CodiceMateriale, m.DescrizioneMateriale,
                   r.QtaRichiesta, r.PreparatoDa, r.DataPreparazione
            FROM ind.MaterialiRichieste r
            JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            WHERE r.Stato = 'PRONTA'
              AND r.ComputerRichiedente = ?
              AND (r.DataUltimaNotificaRichiedente IS NULL
                   OR DATEDIFF(MINUTE, r.DataUltimaNotificaRichiedente, GETDATE()) >= ?)
            ORDER BY r.DataPreparazione ASC
        """
        row = self.db.fetch_one(query, (self.hostname, RE_NOTIFY_MINUTES))

        if row:
            # Aggiorna timestamp
            self.db.execute_query(
                "UPDATE ind.MaterialiRichieste SET DataUltimaNotificaRichiedente = GETDATE() WHERE RichiestaId = ?",
                (row[0],)
            )
            self._show_ready_popup(row)

    def _show_ready_popup(self, data):
        """Popup: materiale pronto per il prelievo."""
        self._popup_open = True
        rid = data[0]
        codice = data[1] or ''
        descrizione = data[2] or ''
        qty = data[3]
        preparatore = data[4] or ''
        data_prep = data[5]

        # Beep (3 volte suono di sistema Windows)
        self._play_alert_sound()

        popup = tk.Toplevel(self.master)
        popup.title("📦 MATERIAL PREGĂTIT")
        popup.geometry("450x280")
        popup.attributes('-topmost', True)
        popup.configure(bg='#27ae60')
        popup.grab_set()

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get('ind_req_ready_title', '📦 Materialul este pregătit!'),
            font=("Segoe UI", 14, "bold"),
            foreground="#27ae60"
        ).pack(pady=(0, 10))

        prep_str = data_prep.strftime('%H:%M') if data_prep else ''
        info_text = (
            f"Cod: {codice}\n"
            f"Descriere: {descrizione}\n"
            f"Cantitate: {qty:.2f}\n"
            f"Pregătit de: {preparatore} la {prep_str}"
        )
        ttk.Label(main, text=info_text, font=("Segoe UI", 11), justify="left").pack(pady=10)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=10)

        def on_pickup():
            try:
                self.db.execute_query(
                    "UPDATE ind.MaterialiRichieste SET Stato = 'PRELEVATA', DataPrelievo = GETDATE() WHERE RichiestaId = ?",
                    (rid,)
                )
                logger.info(f"Richiesta {rid} marcata come PRELEVATA")
            except Exception as e:
                logger.error(f"Errore aggiornamento prelievo: {e}")
            self._popup_open = False
            popup.destroy()

        def on_later():
            self._popup_open = False
            popup.destroy()

        ttk.Button(
            btn_frame,
            text=self.lang.get('ind_req_btn_pickup', '✅ Ritirato'),
            command=on_pickup
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('ind_req_btn_later', '⏳ Dopo'),
            command=on_later
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        popup.protocol("WM_DELETE_WINDOW", on_later)

    @staticmethod
    def _play_alert_sound():
        """Suona il suono di sistema Windows 3 volte in un thread separato."""
        def _beep():
            try:
                for _ in range(3):
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    time.sleep(0.4)
            except Exception:
                pass
        threading.Thread(target=_beep, daemon=True).start()
