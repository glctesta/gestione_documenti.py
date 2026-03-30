"""
npi_budget_approval_monitor.py
Monitor background per PC Approvatore Budget NPI: polling nuove richieste + popup + conferma/rifiuto.
Gira su PC con npi_budget_approver.json presente in %LOCALAPPDATA%.
Pattern: identico a indirect_materials_wh_monitor.py (WHMonitor).
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
from datetime import datetime

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 10_000         # Polling ogni 10s
RE_NOTIFY_MINUTES = 5             # Ri-notifica se non azionato dopo 5 min

# Path file marker per identificare il PC approvatore budget
APPROVER_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
APPROVER_FILE = os.path.join(APPROVER_DIR, "npi_budget_approver.json")


def is_budget_approver():
    """Controlla se questo PC è configurato come approvatore budget NPI."""
    return os.path.isfile(APPROVER_FILE)


def set_budget_approver(enable=True):
    """Marca/rimuove questo PC come approvatore budget NPI."""
    if enable:
        data = {
            "hostname": socket.gethostname(),
            "enabled": True,
            "date": datetime.now().isoformat()
        }
        with open(APPROVER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.info(f"PC '{socket.gethostname()}' configurato come approvatore budget NPI")
    else:
        if os.path.isfile(APPROVER_FILE):
            os.remove(APPROVER_FILE)
            logger.info("Configurazione approvatore budget NPI rimossa")


class BudgetApprovalMonitor:
    """Monitor background che controlla nuove richieste approvazione budget NPI."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        logger.info(f"BudgetApprovalMonitor avviato su {self.hostname}")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            self._check_new_requests()
        except Exception as e:
            logger.error(f"BudgetApprovalMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check_new_requests(self):
        """Controlla richieste di approvazione budget Pending da notificare."""
        if self._popup_open:
            return

        query = """
            SELECT r.RequestId, r.BudgetId, r.ItemIds, r.RequestType,
                   r.RequestedBy, r.RequestedDate, r.ComputerRichiedente,
                   b.BudgetName, p.NomeProgetto,
                   COALESCE(prod.CodiceProdotto, '') + ' ' + COALESCE(prod.NomeProdotto, '') AS ProdottoInfo
            FROM dbo.NpiBudgetApprovalRequests r
            JOIN dbo.NpiBudgets b ON r.BudgetId = b.BudgetId
            JOIN dbo.ProgettiNPI p ON b.ProgettoID = p.ProgettoID
            LEFT JOIN dbo.Prodotti prod ON p.ProdottoID = prod.ProdottoID
            WHERE r.Status = 'Pending'
              AND (r.DataUltimaNotifica IS NULL
                   OR DATEDIFF(MINUTE, r.DataUltimaNotifica, GETDATE()) >= ?)
            ORDER BY r.RequestedDate ASC
        """
        row = self.db.fetch_one(query, (RE_NOTIFY_MINUTES,))

        if row:
            # Aggiorna timestamp notifica
            self.db.execute_query(
                "UPDATE dbo.NpiBudgetApprovalRequests SET DataUltimaNotifica = GETDATE() WHERE RequestId = ?",
                (row[0],)
            )
            self._show_approval_popup(row)

    def _show_approval_popup(self, request_data):
        """Mostra popup con richiesta approvazione budget + beep."""
        self._popup_open = True
        req_id = request_data[0]
        budget_id = request_data[1]
        item_ids = request_data[2] or ''
        req_type = request_data[3] or ''
        req_by = request_data[4] or ''
        req_date = request_data[5]
        computer = request_data[6] or ''
        budget_name = request_data[7] or ''
        progetto_nome = request_data[8] or ''
        prodotto_info = request_data[9] or ''

        # Beep di avviso
        self._play_alert_sound()

        popup = tk.Toplevel(self.master)
        popup.title("💰 APPROVAZIONE BUDGET NPI")
        popup.geometry("600x450")
        popup.attributes('-topmost', True)
        popup.configure(bg='#e67e22')
        popup.grab_set()

        main = ttk.Frame(popup, padding=15)
        main.pack(expand=True, fill="both")

        ttk.Label(
            main,
            text=self.lang.get('budget_approval_title', '💰 Nuova Richiesta Approvazione Budget!'),
            font=("Segoe UI", 14, "bold"),
            foreground="#e67e22"
        ).pack(pady=(0, 10))

        date_str = req_date.strftime('%d/%m/%Y %H:%M') if req_date else ''
        tipo = self.lang.get('budget_approval_type_rows', 'Righe') if req_type == 'Righe' else self.lang.get('budget_approval_type_budget', 'Intero Budget')

        # Conta righe coinvolte
        num_items = len(item_ids.split(',')) if item_ids else 0

        info_text = (
            f"Progetto: {progetto_nome} {prodotto_info}\n"
            f"Budget: {budget_name}\n"
            f"Tipo: {tipo}\n"
            f"Righe coinvolte: {num_items}\n"
            f"Richiesto da: {req_by}\n"
            f"Data: {date_str}\n"
            f"Computer: {computer}"
        )
        ttk.Label(main, text=info_text, font=("Segoe UI", 11), justify="left").pack(pady=10)

        # Nota rifiuto (visibile solo se serve)
        note_frame = ttk.LabelFrame(main, text=self.lang.get('budget_approval_rejection_note', 'Nota rifiuto (opzionale)'), padding=5)
        note_frame.pack(fill="x", pady=5)
        self._reject_note_var = tk.StringVar()
        ttk.Entry(note_frame, textvariable=self._reject_note_var, width=60).pack(fill="x")

        # Bottoni
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=10)

        def on_approve():
            self._process_request(req_id, budget_id, item_ids, 'Approved', popup)

        def on_reject():
            self._process_request(req_id, budget_id, item_ids, 'Rejected', popup)

        def on_dismiss():
            self._popup_open = False
            popup.destroy()

        ttk.Button(
            btn_frame,
            text=self.lang.get('budget_approval_btn_approve', '✅ Approva'),
            command=on_approve
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('budget_approval_btn_reject', '❌ Rifiuta'),
            command=on_reject
        ).pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(
            btn_frame,
            text=self.lang.get('budget_approval_btn_later', '⏳ Dopo'),
            command=on_dismiss
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        popup.protocol("WM_DELETE_WINDOW", on_dismiss)

    def _process_request(self, request_id, budget_id, item_ids_str, decision, popup):
        """Processa approvazione/rifiuto e aggiorna DB."""
        try:
            rejection_note = self._reject_note_var.get().strip() if decision == 'Rejected' else ''
            approval_status = 'Approvato' if decision == 'Approved' else 'Rifiutato'

            # Aggiorna la richiesta
            self.db.execute_query(
                """UPDATE dbo.NpiBudgetApprovalRequests
                   SET Status = ?, ProcessedBy = ?, ProcessedDate = GETDATE(),
                       RejectionNote = ?
                   WHERE RequestId = ?""",
                (decision, self.lang.get('current_user', 'Approver'), rejection_note, request_id)
            )

            # Aggiorna gli item coinvolti
            if item_ids_str:
                for item_id_str in item_ids_str.split(','):
                    item_id = item_id_str.strip()
                    if item_id:
                        self.db.execute_query(
                            "UPDATE dbo.NpiBudgetItems SET ItemApproval = ? WHERE BudgetItemId = ?",
                            (approval_status, int(item_id))
                        )

            # Se tutte le righe sono approvate, aggiorna anche il budget
            check_query = """
                SELECT COUNT(*) FROM dbo.NpiBudgetItems
                WHERE BudgetId = ? AND DateOut IS NULL AND ItemApproval != 'Approvato'
            """
            remaining = self.db.fetch_one(check_query, (budget_id,))
            if remaining and remaining[0] == 0:
                self.db.execute_query(
                    "UPDATE dbo.NpiBudgets SET ApprovalStatus = 'Approvato' WHERE BudgetId = ?",
                    (budget_id,)
                )
                logger.info(f"Budget {budget_id} completamente approvato")

            # Se decisione è rifiuto, aggiorna il budget a Rifiutato
            if decision == 'Rejected':
                self.db.execute_query(
                    "UPDATE dbo.NpiBudgets SET ApprovalStatus = 'Rifiutato', RejectionNote = ? WHERE BudgetId = ?",
                    (rejection_note, budget_id)
                )

            logger.info(f"Richiesta {request_id} processata: {decision}")

        except Exception as e:
            logger.error(f"Errore processamento approvazione {request_id}: {e}", exc_info=True)
            messagebox.showerror("Errore", str(e))

        self._popup_open = False
        popup.destroy()

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
