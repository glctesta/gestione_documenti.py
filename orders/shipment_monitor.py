"""
orders/shipment_monitor.py

Monitor background per i PC configurati come postazione spedizioni urgenti.
- Polling ogni 15 s
- Mostra popup di avviso quando ci sono regole di spedizione non ancora confermate
- Il popup ricompare ogni N minuti (configurabile via shipment_monitor_config.json
  nella directory di lavoro dell'eseguibile)
- Si attiva solo sui PC con shipment_host.json in %LOCALAPPDATA%

Stesso pattern di indirect_materials_wh_monitor.py / shift_handover_monitor.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import sys
import json
import time
import winsound
import threading
from datetime import datetime

from orders.shipment_workstation_config import is_shipment_workstation

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 15_000           # polling DB ogni 15 secondi
DEFAULT_RE_NOTIFY_MINUTES = 10      # default: il popup ricompare ogni N minuti

# File di configurazione salvato nella directory di lavoro dell'eseguibile.
CONFIG_FILENAME = "shipment_monitor_config.json"


def _executable_dir() -> str:
    """Directory dell'eseguibile (o di lavoro corrente in sviluppo)."""
    if getattr(sys, "frozen", False):
        # App impacchettata con PyInstaller: cartella che contiene il .exe
        return os.path.dirname(sys.executable)
    # In sviluppo: directory di lavoro corrente
    return os.getcwd()


def _config_path() -> str:
    return os.path.join(_executable_dir(), CONFIG_FILENAME)


def _write_default_config(path: str) -> None:
    """Crea il file di config con i valori di default (best-effort)."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"reappear_interval_minutes": DEFAULT_RE_NOTIFY_MINUTES},
                f, indent=4, ensure_ascii=False,
            )
        logger.info(f"ShipmentMonitor: creato file di configurazione {path}")
    except Exception as e:
        logger.warning(f"ShipmentMonitor: impossibile creare config {path}: {e}")


def get_reappear_interval_minutes() -> int:
    """Legge dal JSON l'intervallo (minuti) di ricomparsa del popup.

    Se il file non esiste lo crea con il default. In caso di errore o valore
    non valido restituisce il default.
    """
    path = _config_path()
    try:
        if not os.path.isfile(path):
            _write_default_config(path)
            return DEFAULT_RE_NOTIFY_MINUTES
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        val = int(data.get("reappear_interval_minutes", DEFAULT_RE_NOTIFY_MINUTES))
        return val if val >= 1 else DEFAULT_RE_NOTIFY_MINUTES
    except Exception as e:
        logger.warning(
            f"ShipmentMonitor: config non leggibile ({e}); uso default "
            f"{DEFAULT_RE_NOTIFY_MINUTES} min"
        )
        return DEFAULT_RE_NOTIFY_MINUTES


_QUERY_PENDING_DETAIL = """
SELECT
    R.DybamicShippingRuleId,
    PO.ordernumber   AS ProductionOrder,
    D.CustomerName,
    D.SONumber,
    D.ItemCode,
    D.ItemName,
    FORMAT(R.DateToship, 'dd/MM/yyyy HH:mm') AS DateToShipFmt,
    R.QtyToShip,
    R.ShipTo,
    R.AddBayUser
FROM [Traceability_RS].[dyn].[DynamicShippingRules] R
INNER JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] O
       ON  O.DynamicProductionOrderID = R.DynamicProductionOrderID
INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] D
       ON  D.DynamicSaleOrderId = O.DynamicSaleOrderId
INNER JOIN traceability_rs.dbo.Orders PO
       ON  PO.IDOrder = O.IdOrder
WHERE R.ConfirmedAt IS NULL
  -- Mostra solo gli ordini con residuo da spedire > 0: domanda (regole non
  -- confermate) meno quanto gia' confermato su pallet (dyn.ShipmentPallets).
  -- Gli ordini interamente spediti spariscono; i parziali restano.
  AND (
        (SELECT SUM(r3.QtyToShip)
         FROM [Traceability_RS].[dyn].[DynamicShippingRules] r3
         WHERE r3.DynamicProductionOrderID = R.DynamicProductionOrderID
           AND r3.ConfirmedAt IS NULL)
        -
        ISNULL((SELECT SUM(sp.ConfirmedQty)
                FROM [Traceability_RS].[dyn].[ShipmentPallets] sp
                WHERE sp.DynamicProductionOrderID = R.DynamicProductionOrderID), 0)
      ) > 0
ORDER BY R.DateToship ASC
"""


class ShipmentMonitor:
    """Monitor background per le spedizioni urgenti non confermate."""

    def __init__(self, master, db, lang):
        self.master = master
        self.db = db
        self.lang = lang
        self._running = True
        self._popup_open = False
        # Momento (monotonic) in cui il popup è stato mostrato l'ultima volta.
        # Usato per il throttle in memoria basato sul JSON (reappear_interval_minutes).
        self._last_popup_shown = 0.0
        logger.info("ShipmentMonitor avviato")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            # Se il file marker è stato rimosso interrompi silenziosamente
            if not is_shipment_workstation():
                logger.info("ShipmentMonitor: shipment_host.json rimosso — monitor fermato")
                return
            self._check_pending()
        except Exception as e:
            logger.error(f"ShipmentMonitor polling error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check_pending(self):
        if self._popup_open:
            return

        # Throttle in memoria: non riproporre il popup prima dell'intervallo
        # configurato nel JSON (reappear_interval_minutes, in MINUTI).
        interval_minutes = get_reappear_interval_minutes()
        interval_seconds = interval_minutes * 60
        if self._last_popup_shown and \
                (time.monotonic() - self._last_popup_shown) < interval_seconds:
            return

        try:
            self.db.cursor.execute(_QUERY_PENDING_DETAIL)
            rows = self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"ShipmentMonitor query error: {e}", exc_info=True)
            return

        if not rows:
            return

        # Registra il momento della notifica e mostra il popup nel thread UI
        self._last_popup_shown = time.monotonic()
        logger.info(
            f"ShipmentMonitor: {len(rows)} spedizioni non confermate — popup "
            f"(prossima ricomparsa tra {interval_minutes} min)"
        )
        self.master.after(0, lambda r=rows: self._show_popup(r))

    def _show_popup(self, rows):
        self._popup_open = True

        # Beep
        threading.Thread(
            target=lambda: [winsound.Beep(880, 300) for _ in range(3)],
            daemon=True,
        ).start()

        popup = tk.Toplevel(self.master)
        popup.title(
            self.lang.get(
                "shipment_popup_title",
                f"⚠️ SPEDIZIONI URGENTI — {len(rows)} in attesa di conferma",
            )
        )
        popup.geometry("820x480")
        popup.minsize(700, 380)
        popup.attributes("-topmost", True)
        popup.configure(bg="#c0392b")
        popup.grab_set()

        def _on_close():
            self._popup_open = False
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", _on_close)

        # ── Header (in alto) ──
        header_frame = tk.Frame(popup, bg="#c0392b")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(
            header_frame,
            text=self.lang.get(
                "shipment_popup_header",
                f"📦  {len(rows)} SPEDIZIONE/I URGENTE/I NON CONFERMATA/E",
            ),
            bg="#c0392b",
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(12, 4))
        tk.Label(
            header_frame,
            text=self.lang.get(
                "shipment_popup_subheader",
                "Aprire la finestra 'Conferma Shipping' per registrare la conferma.",
            ),
            bg="#c0392b",
            fg="white",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 10))

        # ── Bottoni (ancorati in basso: packati PRIMA della lista così
        #    restano sempre visibili anche se la finestra si rimpicciolisce) ──
        btn_frame = tk.Frame(popup, bg="#c0392b")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text=self.lang.get("shipment_popup_btn_open", "📋 Apri Conferma Shipping"),
            command=lambda: [_on_close(), self._open_confirmation()],
        ).pack(side=tk.LEFT, padx=20)

        ttk.Button(
            btn_frame,
            text=self.lang.get("btn_close", "Chiudi"),
            command=_on_close,
        ).pack(side=tk.RIGHT, padx=20)

        # ── Lista (riempie lo spazio centrale rimanente) ──
        fr = ttk.Frame(popup)
        fr.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))

        cols = ("ProductionOrder", "Customer", "SONumber", "ItemCode", "DateToShip", "QtyRequested", "ShipTo", "AddedBy")
        tree = ttk.Treeview(fr, columns=cols, show="headings", height=8)
        tree.heading("ProductionOrder", text="Ord. Prod.")
        tree.heading("Customer",        text="Cliente")
        tree.heading("SONumber",        text="Ord. Vendita")
        tree.heading("ItemCode",        text="Codice")
        tree.heading("DateToShip",      text="Data Sped.")
        tree.heading("QtyRequested",    text="Qtà Rich.")
        tree.heading("ShipTo",          text="Destinazione")
        tree.heading("AddedBy",         text="Inserito Da")

        tree.column("ProductionOrder", width=110, anchor=tk.CENTER)
        tree.column("Customer",        width=120, anchor=tk.W)
        tree.column("SONumber",        width=90,  anchor=tk.CENTER)
        tree.column("ItemCode",        width=85,  anchor=tk.CENTER)
        tree.column("DateToShip",      width=110, anchor=tk.CENTER)
        tree.column("QtyRequested",    width=65,  anchor=tk.CENTER)
        tree.column("ShipTo",          width=130, anchor=tk.W)
        tree.column("AddedBy",         width=100, anchor=tk.CENTER)

        for row in rows:
            tree.insert(
                "",
                tk.END,
                values=(
                    row.ProductionOrder or "",
                    row.CustomerName or "",
                    row.SONumber or "",
                    row.ItemCode or "",
                    row.DateToShipFmt or "",
                    row.QtyToShip or 0,
                    row.ShipTo or "",
                    row.AddBayUser or "",
                ),
            )

        vsb = ttk.Scrollbar(fr, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _open_confirmation(self):
        """Apre la finestra di conferma passando per il login previsto dal menu."""
        try:
            # Usa lo stesso flusso del menu: login semplice + apertura finestra
            menu_handler = getattr(self.master, "_open_shipment_confirmation", None)
            if callable(menu_handler):
                menu_handler()
                return

            # Fallback: apertura diretta se il metodo del menu non è disponibile
            from orders.shipment_confirmation_window import open_shipment_confirmation_window
            user_name = getattr(self.master, "last_authenticated_user_name", "Unknown")
            open_shipment_confirmation_window(self.master, self.db, self.lang, user_name)
        except Exception as e:
            logger.error(f"Errore apertura conferma da popup: {e}", exc_info=True)
