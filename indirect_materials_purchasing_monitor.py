"""
indirect_materials_purchasing_monitor.py
Monitor background per la WorkStation Acquisti materiali indiretti.
Mostra un popup giornaliero (una sola volta al giorno, dopo le 10:00) con i
materiali per cui è stato inviato un sollecito di riordino e non sono ancora
stati confermati. Il popup consente di scaricare un file Excel e ricorda il
numero di richieste in attesa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import socket
import os
import json
import winsound
import threading
from datetime import datetime, timedelta

from openpyxl import Workbook

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 60_000       # Polling ogni 60s
POPUP_HOUR = 10                 # Popup attivo dalle 10:00
POPUP_MINUTE = 0

HOST_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
PURCHASING_HOST_FILE = os.path.join(HOST_DIR, "purchasing_host.json")
POPUP_LAST_FILE = os.path.join(HOST_DIR, "purchasing_popup_last.json")


def is_purchasing_workstation():
    """Controlla se questo PC è una WorkStation acquisti materiali."""
    return os.path.isfile(PURCHASING_HOST_FILE)


def _read_popup_last_date():
    """Legge l'ultima data in cui il popup è stato mostrato."""
    if not os.path.isfile(POPUP_LAST_FILE):
        return None
    try:
        with open(POPUP_LAST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("last_popup_date")
    except Exception as e:
        logger.warning(f"Errore lettura {POPUP_LAST_FILE}: {e}")
        return None


def _write_popup_last_date(date_str):
    """Salva l'ultima data in cui il popup è stato mostrato."""
    try:
        os.makedirs(HOST_DIR, exist_ok=True)
        with open(POPUP_LAST_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_popup_date": date_str}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Errore scrittura {POPUP_LAST_FILE}: {e}")


class PurchasingMonitor:
    """Monitor background che controlla i solleciti di riordino non confermati."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info(f"PurchasingMonitor avviato su {self.hostname}")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            self._check_and_notify()
        except Exception as e:
            logger.error(f"PurchasingMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check_and_notify(self):
        """Verifica orario e presenza di solleciti non confermati; mostra popup se necessario."""
        if self._popup_open:
            return

        now = datetime.now()
        if now.hour < POPUP_HOUR or (now.hour == POPUP_HOUR and now.minute < POPUP_MINUTE):
            return

        today_str = now.strftime("%Y-%m-%d")
        if _read_popup_last_date() == today_str:
            return

        rows = self._fetch_pending_reorders()
        if not rows:
            # Nessun sollecito pendente: registriamo comunque che il check è stato fatto
            # così non si ripete finché non c'è qualcosa di nuovo
            _write_popup_last_date(today_str)
            return

        self._show_popup(rows)

    def _fetch_pending_reorders(self):
        """Recupera i materiali con sollecito inviato e non ancora confermati."""
        query = """
            SELECT l.RiordineLogId, m.CodiceMateriale, m.DescrizioneMateriale,
                   l.GiacenzaRilevata, l.LivelloMinimo, l.QtaSuggerita,
                   l.DataInvio, DATEDIFF(DAY, l.DataInvio, GETDATE()) AS GiorniTrascorsi
            FROM Traceability_RS.ind.RiordineEmailLog l
            JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = l.MaterialeId
            WHERE l.Stato = 'INVIATO'
              AND l.DataInvio >= DATEADD(DAY, -60, GETDATE())
            ORDER BY l.DataInvio ASC
        """
        try:
            if hasattr(self.db, 'fetch_all'):
                return self.db.fetch_all(query)
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(query)
                return self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Errore fetch pending reorders: {e}", exc_info=True)
            return []

    def _show_popup(self, rows):
        """Mostra il popup con l'elenco dei materiali in attesa."""
        self._popup_open = True
        self._play_alert_sound()

        popup = tk.Toplevel(self.master)
        popup.title(self.lang.get('purchasing_popup_title', 'Reminder acquisti materiali indiretti'))
        popup.geometry("720x520")
        popup.attributes('-topmost', True)
        popup.configure(bg='#f39c12')
        popup.grab_set()

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get('purchasing_popup_header',
                              f"⚠️ Richieste di acquisto in attesa ({len(rows)} materiali)"),
            font=("Segoe UI", 13, "bold"),
            foreground="#d35400"
        ).pack(pady=(0, 10))

        ttk.Label(
            main,
            text=self.lang.get('purchasing_popup_intro',
                              'I seguenti materiali indiretti sono sotto scorta e richiedono un ordine di acquisto.'),
            wraplength=680
        ).pack(pady=(0, 10))

        cols = ('codice', 'descrizione', 'giacenza', 'minimo', 'qty', 'data', 'giorni')
        tree = ttk.Treeview(main, columns=cols, show='headings', height=min(len(rows), 10))
        tree.heading('codice', text=self.lang.get('ind_import_col_code', 'Codice'))
        tree.heading('descrizione', text=self.lang.get('ind_import_col_desc', 'Descrizione'))
        tree.heading('giacenza', text=self.lang.get('ind_stock_col_stock', 'Giacenza'))
        tree.heading('minimo', text=self.lang.get('ind_min_col_min', 'Scorta minima'))
        tree.heading('qty', text=self.lang.get('ind_reorder_col_qty', 'Qta da ordinare'))
        tree.heading('data', text=self.lang.get('purchasing_popup_date', 'Data invio'))
        tree.heading('giorni', text=self.lang.get('purchasing_popup_days', 'Giorni'))
        tree.column('codice', width=100)
        tree.column('descrizione', width=220)
        tree.column('giacenza', width=70, anchor='e')
        tree.column('minimo', width=70, anchor='e')
        tree.column('qty', width=80, anchor='e')
        tree.column('data', width=100)
        tree.column('giorni', width=60, anchor='center')

        for r in rows:
            data_invio = r[6].strftime('%d/%m/%Y') if r[6] else ''
            tree.insert('', 'end', values=(
                r[1] or '', r[2] or '',
                f"{r[3]:.2f}" if r[3] is not None else '-',
                f"{r[4]:.2f}" if r[4] is not None else '-',
                f"{r[5]:.2f}" if r[5] is not None else '-',
                data_invio,
                r[7] or 0
            ))
        tree.pack(fill='both', expand=True, pady=(0, 10))

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame,
            text=self.lang.get('purchasing_popup_excel', 'Scarica Excel'),
            command=lambda: self._export_excel(rows)
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('purchasing_popup_close', 'Chiudi'),
            command=lambda: self._close_popup(popup)
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        popup.protocol("WM_DELETE_WINDOW", lambda: self._close_popup(popup))

    def _close_popup(self, popup):
        today_str = datetime.now().strftime("%Y-%m-%d")
        _write_popup_last_date(today_str)
        popup.destroy()
        self._popup_open = False

    def _export_excel(self, rows):
        """Genera e apre un file Excel con l'elenco dei materiali in attesa."""
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Acquisti materiali"

            headers = [
                self.lang.get('ind_import_col_code', 'Codice'),
                self.lang.get('ind_import_col_desc', 'Descrizione'),
                self.lang.get('ind_stock_col_stock', 'Giacenza'),
                self.lang.get('ind_min_col_min', 'Scorta minima'),
                self.lang.get('ind_reorder_col_qty', 'Qta da ordinare'),
                self.lang.get('purchasing_popup_date', 'Data invio'),
                self.lang.get('purchasing_popup_days', 'Giorni trascorsi'),
            ]
            ws.append(headers)

            for r in rows:
                data_invio = r[6].strftime('%d/%m/%Y') if r[6] else ''
                ws.append([
                    r[1] or '',
                    r[2] or '',
                    float(r[3]) if r[3] is not None else 0,
                    float(r[4]) if r[4] is not None else 0,
                    float(r[5]) if r[5] is not None else 0,
                    data_invio,
                    r[7] or 0,
                ])

            # Auto-width colonne
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except Exception:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column].width = adjusted_width

            file_path = os.path.join(
                HOST_DIR,
                f"purchasing_reorders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            wb.save(file_path)
            logger.info(f"Excel acquisti materiali salvato: {file_path}")
            os.startfile(file_path)
        except Exception as e:
            logger.error(f"Errore esportazione Excel: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('purchasing_excel_error', 'Errore esportazione Excel')}:\n{e}",
                parent=self.master
            )

    def _play_alert_sound(self):
        """Beep di avviso (3 volte suono di sistema Windows)."""
        def _beep():
            for _ in range(3):
                try:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                except Exception:
                    pass
                import time
                time.sleep(0.3)
        threading.Thread(target=_beep, daemon=True).start()
