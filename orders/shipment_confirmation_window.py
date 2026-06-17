"""
orders/shipment_confirmation_window.py

Finestra "Conferma Shipping": mostra tutte le regole di spedizione urgenti
ancora non confermate (ConfirmedAt IS NULL).
L'operatore (login semplice) le visualizza, inserisce la quantità confermata
e salva.  Al termine viene inviata un'email professionale agli indirizzi
presenti in traceability_rs.dbo.settings con atribute = 'Sys_shipment_email'.
"""

import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import utils

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
#  Query helper
# ─────────────────────────────────────────────────────────────────────────────

_QUERY_PENDING = """
SELECT
    R.DybamicShippingRuleId,
    PO.ordernumber        AS ProductionOrder,
    D.CustomerName,
    D.SONumber,
    D.ItemCode,
    D.ItemName,
    FORMAT(R.DateToship, 'dd/MM/yyyy HH:mm')  AS DateToShipFmt,
    R.QtyToShip,
    R.ShipTo,
    R.AddBayUser,
    R.datesys             AS RequestedOn,
    -- Quantità già prodotta (OutOfBox)
    K.Packet              AS ProducedQty,
    -- Rimanenti su PO
    D.QtyOrder - ISNULL(K.Packet, 0) AS RemainOverPO,
    -- Quantità totale dell'ordine di produzione (dbo.Orders)
    PO.OrderQuantity      AS OrderQty,
    -- Già spedito (confermato) per lo stesso ordine di produzione
    (SELECT ISNULL(SUM(r2.ConfirmedQty), 0)
     FROM [Traceability_RS].[dyn].[DynamicShippingRules] r2
     WHERE r2.DynamicProductionOrderID = R.DynamicProductionOrderID
       AND r2.ConfirmedAt IS NOT NULL) AS AlreadyShipped
FROM [Traceability_RS].[dyn].[DynamicShippingRules] R
INNER JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] O
       ON  O.DynamicProductionOrderID = R.DynamicProductionOrderID
INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] D
       ON  D.DynamicSaleOrderId = O.DynamicSaleOrderId
INNER JOIN traceability_rs.dbo.Orders PO
       ON  PO.IDOrder = O.IdOrder
OUTER APPLY
    (SELECT NoBoards AS Packet
     FROM traceability_rs.[dbo].[GetOrderPhaseStatus](O.idorder, 9)) AS K
WHERE R.ConfirmedAt IS NULL
ORDER BY R.DateToship ASC
"""

_COLS = (
    "RuleId",          # hidden
    "ProductionOrder",
    "Customer",
    "SONumber",
    "ItemCode",
    "ItemName",
    "DateToShip",
    "QtyRequested",
    "ProducedQty",
    "RemainOverPO",
    "ShipTo",
    "AddedBy",
)

_COL_LABELS = {
    "ProductionOrder": ("Ordine Prod.",    110),
    "Customer":        ("Cliente",         130),
    "SONumber":        ("Ord. Vendita",    100),
    "ItemCode":        ("Codice",           90),
    "ItemName":        ("Prodotto",        150),
    "DateToShip":      ("Data Spedizione", 120),
    "QtyRequested":    ("Qtà Rich.",        80),
    "ProducedQty":     ("Qtà Prodotta",     90),
    "RemainOverPO":    ("Rimanenti PO",     90),
    "ShipTo":          ("Destinazione",    140),
    "AddedBy":         ("Inserito Da",     110),
}


class ShipmentConfirmationWindow(tk.Toplevel):
    """Finestra per confermare le spedizioni urgenti pendenti."""

    def __init__(self, master, db, lang, user_name: str):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        # rule_id -> {order_qty, already_shipped, max_confirmable, produced, requested}
        self._rule_info = {}

        self.title(self.lang.get("shipment_confirm_title", "Conferma Spedizioni Urgenti"))
        self.geometry("1300x650")
        self.transient(master)

        self._build_ui()
        self._load_data()

    # ------------------------------------------------------------------ #
    #  UI
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # --- Header ---
        hdr = ttk.Frame(main)
        hdr.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(
            hdr,
            text=self.lang.get(
                "shipment_confirm_header",
                "⚠️  Spedizioni Urgenti — Conferma Ricezione",
            ),
            font=("Segoe UI", 13, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Button(
            hdr,
            text=self.lang.get("btn_refresh", "🔄 Aggiorna"),
            command=self._load_data,
        ).pack(side=tk.RIGHT, padx=5)

        # --- Treeview ---
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.tree = ttk.Treeview(
            tree_frame, columns=_COLS, show="headings", selectmode="browse"
        )

        # Hidden column
        self.tree.column("RuleId", width=0, stretch=False)
        self.tree.heading("RuleId", text="")

        for col in _COLS[1:]:
            label, width = _COL_LABELS[col]
            self.tree.heading(col, text=self.lang.get(f"col_{col.lower()}", label))
            anchor = tk.W if col in ("Customer", "ItemName", "ShipTo") else tk.CENTER
            self.tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Tag colore riga selezionata
        self.tree.tag_configure("urgente", background="#fff3cd")

        # --- Pannello Conferma ---
        confirm_frame = ttk.LabelFrame(
            main,
            text=self.lang.get("shipment_confirm_panel", "Conferma Spedizione Selezionata"),
            padding=10,
        )
        confirm_frame.pack(fill=tk.X)

        ttk.Label(
            confirm_frame,
            text=self.lang.get("shipment_confirm_qty_label", "Quantità confermata:"),
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 8))

        self.qty_var = tk.StringVar()
        self.qty_entry = ttk.Entry(confirm_frame, textvariable=self.qty_var, width=12)
        self.qty_entry.grid(row=0, column=1, sticky=tk.W)

        self.qty_hint = ttk.Label(confirm_frame, text="", foreground="gray")
        self.qty_hint.grid(row=0, column=2, sticky=tk.W, padx=(8, 20))

        self.btn_confirm = ttk.Button(
            confirm_frame,
            text=self.lang.get("btn_confirm_shipping", "✅ Conferma Spedizione"),
            command=self._confirm_selected,
            state=tk.DISABLED,
        )
        self.btn_confirm.grid(row=0, column=3, padx=5)

        # Status bar
        self.status_var = tk.StringVar(
            value=self.lang.get("select_row_first", "Seleziona una riga per confermare")
        )
        ttk.Label(main, textvariable=self.status_var, foreground="gray").pack(
            fill=tk.X, pady=(4, 0)
        )

        # Bind selezione
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    # ------------------------------------------------------------------ #
    #  Data
    # ------------------------------------------------------------------ #
    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._rule_info = {}
        try:
            self.db.cursor.execute(_QUERY_PENDING)
            rows = self.db.cursor.fetchall()
            for row in rows:
                order_qty = int(row.OrderQty or 0)
                already_shipped = int(row.AlreadyShipped or 0)
                self._rule_info[str(row.DybamicShippingRuleId)] = {
                    "order_qty": order_qty,
                    "already_shipped": already_shipped,
                    "max_confirmable": max(0, order_qty - already_shipped),
                    "produced": int(row.ProducedQty or 0),
                    "requested": int(row.QtyToShip or 0),
                }
                requested_on = (
                    row.RequestedOn.strftime("%d/%m/%Y %H:%M")
                    if row.RequestedOn
                    else ""
                )
                self.tree.insert(
                    "",
                    tk.END,
                    tags=("urgente",),
                    values=(
                        row.DybamicShippingRuleId,
                        row.ProductionOrder or "",
                        row.CustomerName or "",
                        row.SONumber or "",
                        row.ItemCode or "",
                        row.ItemName or "",
                        row.DateToShipFmt or "",
                        row.QtyToShip or 0,
                        row.ProducedQty or 0,
                        row.RemainOverPO or 0,
                        row.ShipTo or "",
                        row.AddBayUser or "",
                    ),
                )
            count = len(rows)
            self.status_var.set(
                self.lang.get(
                    "shipment_pending_count",
                    "{0} spedizione/i urgente/i in attesa di conferma",
                ).format(count)
            )
        except Exception as e:
            logger.error(f"Errore caricamento spedizioni urgenti: {e}", exc_info=True)
            messagebox.showerror(self.lang.get("error", "Errore"), str(e), parent=self)

    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            self.btn_confirm.config(state=tk.DISABLED)
            return
        values = self.tree.item(sel[0], "values")
        rule_id = str(values[0])
        requested_qty = int(values[7]) if values[7] else 0
        produced_qty = int(values[8]) if values[8] else 0
        info = self._rule_info.get(rule_id, {})
        max_conf = info.get("max_confirmable", 0)

        # Valore predefinito: quantità prodotta (non quantità richiesta)
        self.qty_var.set(str(produced_qty))
        self.qty_hint.config(
            text=self.lang.get(
                "shipment_qty_hint",
                "(prodotta: {0} | richiesta: {1} | max ordine: {2})",
            ).format(produced_qty, requested_qty, max_conf)
        )
        self.btn_confirm.config(state=tk.NORMAL)

    # ------------------------------------------------------------------ #
    #  Conferma
    # ------------------------------------------------------------------ #
    def _confirm_selected(self):
        sel = self.tree.selection()
        if not sel:
            return

        values = self.tree.item(sel[0], "values")
        rule_id      = values[0]
        prod_order   = values[1]
        customer     = values[2]
        so_number    = values[3]
        item_code    = values[4]
        item_name    = values[5]
        date_to_ship = values[6]
        requested_qty = int(values[7]) if values[7] else 0
        produced_qty  = int(values[8]) if values[8] else 0
        remain_po     = int(values[9]) if values[9] else 0
        ship_to       = values[10]

        # --- Validazione quantità ---
        qty_str = self.qty_var.get().strip()
        if not qty_str:
            messagebox.showwarning(
                self.lang.get("warning", "Attenzione"),
                self.lang.get("qty_required", "Inserire la quantità confermata."),
                parent=self,
            )
            return
        try:
            confirmed_qty = int(qty_str)
        except ValueError:
            messagebox.showwarning(
                self.lang.get("warning", "Attenzione"),
                self.lang.get("qty_invalid", "Quantità non valida."),
                parent=self,
            )
            return
        if confirmed_qty <= 0:
            messagebox.showwarning(
                self.lang.get("warning", "Attenzione"),
                self.lang.get("qty_positive", "La quantità deve essere maggiore di zero."),
                parent=self,
            )
            return

        # La quantità confermata può superare la quantità richiesta, ma NON la
        # quantità residua dell'ordine di produzione (Orders.OrderQuantity meno
        # quanto già spedito/confermato per lo stesso ordine).
        info = self._rule_info.get(str(rule_id), {})
        order_qty = info.get("order_qty", 0)
        already_shipped = info.get("already_shipped", 0)
        max_confirmable = info.get("max_confirmable", max(0, order_qty - already_shipped))
        if confirmed_qty > max_confirmable:
            messagebox.showwarning(
                self.lang.get("warning", "Attenzione"),
                self.lang.get(
                    "shipment_qty_over_order",
                    "La quantità confermata ({0}) non può superare la quantità residua "
                    "dell'ordine ({1}) = quantità ordine ({2}) − già spedito ({3}).",
                ).format(confirmed_qty, max_confirmable, order_qty, already_shipped),
                parent=self,
            )
            return

        # --- Avviso discrepanza ---
        discrepancy = confirmed_qty != requested_qty
        if discrepancy:
            diff = confirmed_qty - requested_qty
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            msg = self.lang.get(
                "shipment_qty_discrepancy",
                "⚠️  Attenzione: la quantità confermata ({0}) differisce\n"
                "dalla quantità richiesta ({1})  →  differenza: {2}.\n\n"
                "Continuare con la conferma?",
            ).format(confirmed_qty, requested_qty, diff_str)
            if not messagebox.askyesno(
                self.lang.get("confirm", "Conferma"), msg, parent=self
            ):
                return

        # --- Salvataggio ---
        confirmed_at = datetime.now()
        try:
            self.db.cursor.execute(
                """
                UPDATE [Traceability_RS].[dyn].[DynamicShippingRules]
                SET ConfirmedByUser = ?,
                    ConfirmedQty   = ?,
                    ConfirmedAt    = ?
                WHERE DybamicShippingRuleId = ?
                """,
                (self.user_name, confirmed_qty, confirmed_at, rule_id),
            )
            self.db.conn.commit()
            logger.info(
                f"Spedizione {rule_id} confermata da {self.user_name} - qty {confirmed_qty}"
            )
        except Exception as e:
            logger.error(f"Errore salvataggio conferma: {e}", exc_info=True)
            self.db.conn.rollback()
            messagebox.showerror(
                self.lang.get("error", "Errore"), str(e), parent=self
            )
            return

        # --- Email ---
        threading.Thread(
            target=self._send_confirmation_email,
            args=(
                prod_order,
                customer,
                so_number,
                item_code,
                item_name,
                date_to_ship,
                requested_qty,
                confirmed_qty,
                produced_qty,
                remain_po,
                ship_to,
                confirmed_at,
                discrepancy,
            ),
            daemon=True,
        ).start()

        messagebox.showinfo(
            self.lang.get("success", "Successo"),
            self.lang.get(
                "shipment_confirmed_ok",
                "Spedizione confermata con successo.",
            ),
            parent=self,
        )
        self._load_data()

    # ------------------------------------------------------------------ #
    #  Email
    # ------------------------------------------------------------------ #
    def _send_confirmation_email(
        self,
        prod_order,
        customer,
        so_number,
        item_code,
        item_name,
        date_to_ship,
        requested_qty,
        confirmed_qty,
        produced_qty,
        remain_po,
        ship_to,
        confirmed_at: datetime,
        discrepancy: bool,
    ):
        try:
            recipients = utils.get_email_recipients(
                self.db.conn, "Sys_shipment_email"
            )
            if not recipients:
                logger.warning("Nessun destinatario per Sys_shipment_email — email non inviata")
                return

            diff_row = ""
            if discrepancy:
                diff = confirmed_qty - requested_qty
                diff_str = f"+{diff}" if diff > 0 else str(diff)
                diff_color = "#c0392b" if diff < 0 else "#e67e22"
                diff_row = f"""
                <tr style="background:#fdecea;">
                  <td style="padding:6px 10px;font-weight:bold;color:{diff_color};">
                    ⚠️ DISCREPANZA QUANTITÀ
                  </td>
                  <td style="padding:6px 10px;color:{diff_color};font-weight:bold;">
                    Confermata: <strong>{confirmed_qty}</strong> vs Richiesta: <strong>{requested_qty}</strong>
                    &nbsp;(differenza: {diff_str})
                  </td>
                </tr>"""

            subject_prefix = "⚠️ DISCREPANZA — " if discrepancy else ""
            subject = (
                f"{subject_prefix}Conferma Spedizione Urgente: {so_number} / {prod_order}"
            )

            body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body {{font-family:'Segoe UI',Arial,sans-serif;font-size:13px;color:#333;}}
    table {{border-collapse:collapse;width:100%;max-width:700px;}}
    th {{background:#1a5276;color:#fff;padding:8px 10px;text-align:left;}}
    td {{padding:6px 10px;border-bottom:1px solid #ddd;}}
    tr:nth-child(even){{background:#f8f8f8;}}
    .header-box {{background:#1a5276;color:#fff;padding:16px;border-radius:4px;margin-bottom:18px;}}
    .footer {{font-size:11px;color:#888;margin-top:20px;}}
  </style>
</head>
<body>
  <div class="header-box">
    <h2 style="margin:0;">📦 Conferma Spedizione Urgente</h2>
    <p style="margin:4px 0 0;">Registrata il {confirmed_at.strftime('%d/%m/%Y alle %H:%M:%S')}
       da <strong>{self.user_name}</strong></p>
  </div>

  <table>
    <tr><th colspan="2">Dettaglio Ordine</th></tr>
    <tr><td>Cliente</td><td><strong>{customer}</strong></td></tr>
    <tr><td>Ordine di Vendita</td><td>{so_number}</td></tr>
    <tr><td>Ordine di Produzione</td><td>{prod_order}</td></tr>
    <tr><td>Codice Prodotto</td><td>{item_code}</td></tr>
    <tr><td>Descrizione Prodotto</td><td>{item_name}</td></tr>
    <tr><td>Data Spedizione Richiesta</td><td>{date_to_ship}</td></tr>
    <tr><td>Destinazione</td><td>{ship_to}</td></tr>
    <tr><th colspan="2" style="padding-top:12px;">Quantità</th></tr>
    <tr><td>Quantità Richiesta</td><td>{requested_qty}</td></tr>
    <tr><td>Quantità Prodotta (OutOfBox)</td><td>{produced_qty}</td></tr>
    <tr><td>Rimanenti su PO</td><td>{remain_po}</td></tr>
    <tr><td>Quantità <strong>Confermata</strong> per Spedizione</td>
        <td><strong>{confirmed_qty}</strong></td></tr>
    {diff_row}
    <tr><th colspan="2" style="padding-top:12px;">Conferma</th></tr>
    <tr><td>Confermato Da</td><td><strong>{self.user_name}</strong></td></tr>
    <tr><td>Data / Ora Conferma</td><td>{confirmed_at.strftime('%d/%m/%Y %H:%M:%S')}</td></tr>
  </table>

  <p class="footer">Email generata automaticamente da TraceabilityRS — non rispondere a questo messaggio.</p>
</body>
</html>"""

            utils.send_email(recipients, subject, body, is_html=True)
            logger.info(f"Email conferma spedizione inviata a {recipients}")
        except Exception as e:
            logger.error(f"Errore invio email conferma spedizione: {e}", exc_info=True)


def open_shipment_confirmation_window(master, db, lang, user_name: str):
    """Punto di ingresso pubblico."""
    ShipmentConfirmationWindow(master, db, lang, user_name)
