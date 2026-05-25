"""
orders/shipment_monitor.py

Monitor background per i PC configurati come postazione spedizioni urgenti.
- Polling ogni 15 s
- Mostra popup di avviso quando ci sono regole di spedizione non ancora confermate
- Si attiva solo sui PC con shipment_host.json in %LOCALAPPDATA%

Stesso pattern di indirect_materials_wh_monitor.py / shift_handover_monitor.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import winsound
import threading
from datetime import datetime

from orders.shipment_workstation_config import is_shipment_workstation

logger = logging.getLogger(__name__)

POLL_INTERVAL_MS = 15_000        # polling ogni 15 secondi
RE_NOTIFY_MINUTES = 10           # ri-notifica se non gestita entro N minuti


_QUERY_PENDING_COUNT = """
SELECT COUNT(*) AS PendingCount
FROM [Traceability_RS].[dyn].[DynamicShippingRules]
WHERE ConfirmedAt IS NULL
"""

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
  AND (R.LastShipmentNotify IS NULL
       OR DATEDIFF(MINUTE, R.LastShipmentNotify, GETDATE()) >= ?)
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
        try:
            # Usa LastShipmentNotify per evitare flood (colonna opzionale — gestisce l'assenza)
            try:
                self.db.cursor.execute(_QUERY_PENDING_DETAIL, (RE_NOTIFY_MINUTES,))
            except Exception:
                # Colonna LastShipmentNotify potrebbe non esistere: usa query semplice
                self.db.cursor.execute(
                    """
                    SELECT R.DybamicShippingRuleId,
                           PO.ordernumber   AS ProductionOrder,
                           D.CustomerName, D.SONumber, D.ItemCode, D.ItemName,
                           FORMAT(R.DateToship,'dd/MM/yyyy HH:mm') AS DateToShipFmt,
                           R.QtyToShip, R.ShipTo, R.AddBayUser
                    FROM [Traceability_RS].[dyn].[DynamicShippingRules] R
                    INNER JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] O
                           ON  O.DynamicProductionOrderID = R.DynamicProductionOrderID
                    INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] D
                           ON  D.DynamicSaleOrderId = O.DynamicSaleOrderId
                    INNER JOIN traceability_rs.dbo.Orders PO ON PO.IDOrder = O.IdOrder
                    WHERE R.ConfirmedAt IS NULL
                    ORDER BY R.DateToship ASC
                    """
                )
            rows = self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"ShipmentMonitor query error: {e}", exc_info=True)
            return

        if not rows:
            return

        # Aggiorna LastShipmentNotify (best-effort)
        for row in rows:
            try:
                self.db.cursor.execute(
                    """
                    UPDATE [Traceability_RS].[dyn].[DynamicShippingRules]
                    SET LastShipmentNotify = GETDATE()
                    WHERE DybamicShippingRuleId = ?
                    """,
                    (row.DybamicShippingRuleId,),
                )
                self.db.conn.commit()
            except Exception:
                pass

        # Mostra popup nel thread UI
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
        popup.geometry("760x420")
        popup.attributes("-topmost", True)
        popup.configure(bg="#c0392b")
        popup.grab_set()

        def _on_close():
            self._popup_open = False
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", _on_close)

        # Header
        tk.Label(
            popup,
            text=self.lang.get(
                "shipment_popup_header",
                f"📦  {len(rows)} SPEDIZIONE/I URGENTE/I NON CONFERMATA/E",
            ),
            bg="#c0392b",
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(12, 4))

        tk.Label(
            popup,
            text=self.lang.get(
                "shipment_popup_subheader",
                "Aprire la finestra 'Conferma Shipping' per registrare la conferma.",
            ),
            bg="#c0392b",
            fg="white",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 10))

        # Treeview
        cols = ("ProductionOrder", "Customer", "SONumber", "ItemCode", "DateToShip", "QtyRequested", "ShipTo", "AddedBy")
        tree = ttk.Treeview(popup, columns=cols, show="headings", height=8)
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

        fr = ttk.Frame(popup)
        fr.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        vsb = ttk.Scrollbar(fr, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottoni
        btn_frame = tk.Frame(popup, bg="#c0392b")
        btn_frame.pack(fill=tk.X, pady=8)

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

    def _open_confirmation(self):
        """Apre la finestra di conferma (senza login — già verificato dal menu)."""
        try:
            from orders.shipment_confirmation_window import open_shipment_confirmation_window

            # Recupera un user_name generico di sistema per apertura da popup
            user_name = getattr(self.master, "last_authenticated_user_name", "Unknown")
            open_shipment_confirmation_window(self.master, self.db, self.lang, user_name)
        except Exception as e:
            logger.error(f"Errore apertura conferma da popup: {e}", exc_info=True)
