# -*- coding: utf-8 -*-
"""
Modulo GUI per la giustificazione delle discrepanze del piano di produzione.

Architettura Master-Detail:
- Form principale (PlanDiscrepancyWindow): mostra DISTINCT ordini+prodotti 
  con conteggio discrepanze per categoria (red / out_of_plan).
- Form dettaglio (PlanDetailWindow): mostra tutte le righe analitiche 
  per un ordine+prodotto selezionato.

Giustificazione a due livelli:
  1) A livello di Ordine+Prodotto (master): influenza TUTTE le righe del gruppo
  2) A livello di riga analitica (detail): influenza solo quella riga
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger("TraceabilityRS")


# ================================================================
# FORM MASTER — Riepilogo per Ordine + Prodotto
# ================================================================

class PlanDiscrepancyWindow(tk.Toplevel):
    """Finestra principale: riepilogo discrepanze raggruppate per ordine+prodotto."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('piano_produzione',
                                  'Piano Produzione — Discrepanze'))
        self.geometry('1100x650')
        self.transient(parent)
        self.grab_set()

        # Dati interni
        self._tree_data = {}   # {iid: {order_number, product_name, ...}}
        self._reasons = []     # [(PlanResponseId, Description)]
        self._timer_seconds = 3600
        self._timer_id = None

        # Pulizia duplicati
        self._cleanup_duplicates()

        # Build UI
        self._build_ui()

        # Carica dati
        self._load_reasons()
        self._load_summary()

        # Avvia timer
        self._start_timer()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ================================================================
    # CLEANUP
    # ================================================================
    def _cleanup_duplicates(self):
        try:
            import plan_alert_escalation as pae
            deleted = pae.cleanup_duplicate_alerts(self.db.conn)
            if deleted > 0:
                logger.info(f"Pulizia pre-apertura: eliminati {deleted} duplicati")
        except Exception as e:
            logger.error(f"Errore pulizia duplicati: {e}")

    # ================================================================
    # UI
    # ================================================================
    def _build_ui(self):
        # --- Header ---
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)

        ttk.Label(header,
            text=f"{self.lang.get('logged_user', 'Operator')}: {self.user_name}",
            font=('Arial', 10, 'bold')).pack(side='left')

        self.timer_label = ttk.Label(header,
            text="⏱ 60:00", font=('Arial', 12, 'bold'),
            foreground='#1565C0')
        self.timer_label.pack(side='right', padx=10)

        ttk.Label(header,
            text=self.lang.get('time_remaining', 'Timp rămas:'),
            font=('Arial', 10)).pack(side='right')

        # --- Toolbar ---
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=(0, 5))

        ttk.Button(toolbar,
            text=self.lang.get('btn_refresh', '🔄 Actualizare'),
            command=self._load_summary).pack(side='left', padx=3)

        # Info
        self.info_label = ttk.Label(toolbar,
            text=self.lang.get('plan_dblclick_hint',
                               'Double-click on a row to see details'),
            font=('Arial', 9, 'italic'), foreground='#666')
        self.info_label.pack(side='left', padx=15)

        self.count_label = ttk.Label(toolbar, text="", font=('Arial', 9))
        self.count_label.pack(side='right', padx=5)

        # --- TreeView MASTER ---
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('order', 'product', 'total', 'red', 'out_of_plan',
                    'deficit', 'phases', 'first_date', 'last_date')
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                  show='headings', selectmode='extended',
                                  height=15)

        col_config = {
            'order':       (self.lang.get('col_order', 'Order'),                100, 'center'),
            'product':     (self.lang.get('col_product', 'Product'),            220, 'w'),
            'total':       (self.lang.get('col_total_disc', 'Nr. Discrepancies'), 100, 'center'),
            'red':         (self.lang.get('col_red', '🔴 Delay'),                90, 'center'),
            'out_of_plan': (self.lang.get('col_out_of_plan', '🟠 Out of Plan'),  90, 'center'),
            'deficit':     (self.lang.get('col_deficit_total', 'Total Deficit'), 90, 'center'),
            'phases':      (self.lang.get('col_phases', 'Phases'),              180, 'w'),
            'first_date':  (self.lang.get('col_first_alert', 'First Alert'),    90, 'center'),
            'last_date':   (self.lang.get('col_last_alert', 'Last Alert'),      90, 'center'),
        }
        for col, (label, width, anchor) in col_config.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure('has_red', background='#FFCDD2')
        self.tree.tag_configure('only_out', background='#FFF3E0')

        vsb = ttk.Scrollbar(tree_frame, orient='vertical',
                              command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal',
                              command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Double-click per aprire dettaglio
        self.tree.bind('<Double-1>', self._on_double_click)

        # --- Pannello giustificazione GROUP-LEVEL ---
        justify_frame = ttk.LabelFrame(self,
            text=self.lang.get('justify_group',
                               '📝 Justificare la nivel de comandă (se aplică tuturor alertelor)'),
            padding=10)
        justify_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(justify_frame,
            text=self.lang.get('reason_label', 'Motivație:'),
            font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5)

        self.reason_var = tk.StringVar()
        self.reason_combo = ttk.Combobox(justify_frame,
            textvariable=self.reason_var, state='readonly', width=50)
        self.reason_combo.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(justify_frame,
            text=self.lang.get('notes_label', 'Note:'),
            font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=5)

        self.notes_var = tk.StringVar()
        ttk.Entry(justify_frame, textvariable=self.notes_var,
                  width=25).grid(row=0, column=3, sticky='ew', padx=5)

        self.btn_save_group = ttk.Button(justify_frame,
            text=self.lang.get('btn_save_group',
                               '✅ Salvează pt. comandă selectată'),
            command=self._save_group_justification)
        self.btn_save_group.grid(row=0, column=4, padx=10)

        justify_frame.columnconfigure(1, weight=2)
        justify_frame.columnconfigure(3, weight=1)

        # --- Footer ---
        footer = ttk.Frame(self, padding=5)
        footer.pack(fill='x', padx=10)

        ttk.Button(footer,
            text=self.lang.get('btn_close', 'Închide'),
            command=self._on_close).pack(side='right', padx=5)

        ttk.Button(footer,
            text=self.lang.get('btn_open_detail', '🔍 Deschide detalii'),
            command=self._open_selected_detail).pack(side='right', padx=5)

    # ================================================================
    # DATI
    # ================================================================
    def _load_reasons(self):
        try:
            import plan_alert_escalation as pae
            rows = pae.get_response_reasons(self.db.conn)
            self._reasons = [(r.PlanResponseId, r.ResponseDescription)
                             for r in rows]
            self.reason_combo['values'] = [desc for _, desc in self._reasons]
            if self._reasons:
                self.reason_combo.current(0)
        except Exception as e:
            logger.error(f"Errore caricamento motivazioni: {e}")

    def _load_summary(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self._tree_data = {}

            import plan_alert_escalation as pae
            rows = pae.get_unresponded_alerts_summary(self.db.conn)

            count = 0
            for row in rows:
                red = row.RedCount or 0
                out = row.OutOfPlanCount or 0
                tag = 'has_red' if red > 0 else 'only_out'

                iid = self.tree.insert('', 'end', values=(
                    row.OrderNumber,
                    row.ProductName,
                    row.TotalAlerts or 0,
                    red,
                    out,
                    row.TotalDeficit or 0,
                    row.Phases or '',
                    str(row.FirstAlertDate) if row.FirstAlertDate else '',
                    str(row.LastAlertDate) if row.LastAlertDate else ''
                ), tags=(tag,))

                self._tree_data[iid] = {
                    'order_number': row.OrderNumber,
                    'product_name': row.ProductName,
                    'total': row.TotalAlerts or 0,
                }
                count += 1

            self.count_label.config(
                text=f"{count} {self.lang.get('orders_with_discrepancies', 'orders with discrepancies')}")
            logger.info(f"Riepilogo: {count} ordini con discrepanze")

        except Exception as e:
            logger.error(f"Errore caricamento riepilogo: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Eroare'), f"Eroare: {e}")

    # ================================================================
    # DETTAGLIO
    # ================================================================
    def _on_double_click(self, event):
        self._open_selected_detail()

    def _open_selected_detail(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Atenție'),
                self.lang.get('select_order',
                              'Selectați o comandă din listă.'))
            return
        iid = selection[0]
        data = self._tree_data.get(iid)
        if data:
            PlanDetailWindow(
                self, self.db, self.lang, self.user_name,
                data['order_number'], data['product_name'],
                self._reasons, self._on_detail_closed
            )

    def _on_detail_closed(self):
        """Callback quando la finestra dettaglio viene chiusa — ricarica."""
        self._load_summary()

    # ================================================================
    # SALVA GROUP
    # ================================================================
    def _save_group_justification(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Atenție'),
                self.lang.get('select_order',
                              'Selectați cel puțin o comandă din listă.'))
            return

        reason_text = self.reason_var.get().strip()
        if not reason_text:
            messagebox.showwarning(
                self.lang.get('warning', 'Atenție'),
                self.lang.get('select_reason', 'Selectați o motivație.'))
            return

        plan_response_id = None
        for rid, desc in self._reasons:
            if desc == reason_text:
                plan_response_id = rid
                break
        if plan_response_id is None:
            return

        notes = self.notes_var.get().strip()

        # Mostra riepilogo
        total_orders = len(selection)
        total_alerts = sum(
            self._tree_data[iid]['total'] for iid in selection
            if iid in self._tree_data)

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Confirm'),
            self.lang.get('confirm_save_group',
                          'Save justification for {orders} orders ({alerts} total alerts)?').format(
                              orders=total_orders, alerts=total_alerts)
            + f"\n\n{self.lang.get('reason_label', 'Reason:')} {reason_text}"
            + f"\n{self.lang.get('notes_label', 'Notes:')} {notes if notes else '—'}"):
            return

        import plan_alert_escalation as pae
        saved = 0
        for iid in selection:
            data = self._tree_data.get(iid)
            if not data:
                continue
            alert_ids = pae.get_all_alert_ids_for_order_product(
                self.db.conn, data['order_number'], data['product_name'])
            if alert_ids:
                ok = pae.save_response(
                    self.db.conn, alert_ids, plan_response_id,
                    self.user_name, notes)
                if ok:
                    saved += len(alert_ids)

        if saved > 0:
            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('saved_justifications',
                              '{count} justifications saved successfully.').format(count=saved))
            self._load_summary()
            self.notes_var.set('')

    # ================================================================
    # TIMER
    # ================================================================
    def _start_timer(self):
        self._update_timer()

    def _update_timer(self):
        if self._timer_seconds <= 0:
            expired = self.lang.get('timer_expired', 'EXPIRED')
            self.timer_label.config(
                text=f"⏱ 00:00 — {expired}!", foreground='#B71C1C')
            return
        minutes = self._timer_seconds // 60
        seconds = self._timer_seconds % 60
        self.timer_label.config(text=f"⏱ {minutes:02d}:{seconds:02d}")
        if self._timer_seconds <= 300:
            self.timer_label.config(foreground='#B71C1C')
        elif self._timer_seconds <= 900:
            self.timer_label.config(foreground='#E65100')
        else:
            self.timer_label.config(foreground='#1565C0')
        self._timer_seconds -= 1
        self._timer_id = self.after(1000, self._update_timer)

    # ================================================================
    # CHIUSURA
    # ================================================================
    def _on_close(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
        remaining = len(self.tree.get_children())
        if remaining > 0:
            if not messagebox.askyesno(
                self.lang.get('confirm', 'Confirm'),
                self.lang.get('close_with_pending',
                              'There are still {count} orders with unjustified discrepancies.\nClose?').format(
                                  count=remaining)):
                return
        self.destroy()


# ================================================================
# FORM DETAIL — Righe analitiche per un Ordine+Prodotto
# ================================================================

class PlanDetailWindow(tk.Toplevel):
    """Finestra dettaglio: tutte le righe analitiche per un ordine+prodotto."""

    def __init__(self, parent, db, lang, user_name,
                 order_number, product_name, reasons, on_close_callback):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.order_number = order_number
        self.product_name = product_name
        self._reasons = reasons   # [(id, desc)] dalla master
        self._on_close_callback = on_close_callback
        self._tree_data = {}

        self.title(f"Detalii — {order_number} / {product_name}")
        self.geometry('1200x550')
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_details()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # --- Header ---
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)

        ttk.Label(header,
            text=f"{self.lang.get('col_order', 'Order')}: {self.order_number}",
            font=('Arial', 11, 'bold')).pack(side='left')
        ttk.Label(header,
            text=f"  |  {self.lang.get('col_product', 'Product')}: {self.product_name}",
            font=('Arial', 11)).pack(side='left')

        self.count_label = ttk.Label(header, text="", font=('Arial', 9))
        self.count_label.pack(side='right')

        # --- Toolbar ---
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=(0, 5))

        ttk.Button(toolbar,
            text=self.lang.get('btn_select_all', '☑ Selectează tot'),
            command=self._select_all).pack(side='left', padx=3)
        ttk.Button(toolbar,
            text=self.lang.get('btn_deselect_all', '☐ Deselectează tot'),
            command=self._deselect_all).pack(side='left', padx=3)

        # --- TreeView DETAIL ---
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('phase', 'qty_xls', 'qty_produced', 'qty_expected',
                    'deficit', 'status', 'alert_date', 'projected_end',
                    'on_future')
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                  show='headings', selectmode='extended',
                                  height=14)

        col_config = {
            'phase':        (self.lang.get('col_phase', 'Phase'),                130, 'w'),
            'qty_xls':      (self.lang.get('col_qty_plan', 'Qty Plan'),          80, 'center'),
            'qty_produced': (self.lang.get('col_qty_produced', 'Qty Produced'),   80, 'center'),
            'qty_expected': (self.lang.get('col_qty_expected', 'Qty Expected'),   80, 'center'),
            'deficit':      (self.lang.get('col_deficit', 'Deficit'),             70, 'center'),
            'status':       (self.lang.get('col_status', 'Status'),              90, 'center'),
            'alert_date':   (self.lang.get('col_alert_date', 'Alert Date'),     100, 'center'),
            'projected_end':(self.lang.get('col_projected_end', 'Projected End'), 100, 'center'),
            'on_future':    (self.lang.get('col_future', 'Future'),              60, 'center'),
        }
        for col, (label, width, anchor) in col_config.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure('red', background='#FFCDD2')
        self.tree.tag_configure('out_of_plan', background='#FFF3E0')

        vsb = ttk.Scrollbar(tree_frame, orient='vertical',
                              command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # --- Pannello giustificazione ROW-LEVEL ---
        justify_frame = ttk.LabelFrame(self,
            text=self.lang.get('justify_row',
                               '📝 Justificare la nivel de rând (se aplică doar rândurilor selectate)'),
            padding=10)
        justify_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(justify_frame,
            text=self.lang.get('reason_label', 'Motivație:'),
            font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5)

        self.reason_var = tk.StringVar()
        self.reason_combo = ttk.Combobox(justify_frame,
            textvariable=self.reason_var, state='readonly', width=50)
        self.reason_combo['values'] = [desc for _, desc in self._reasons]
        if self._reasons:
            self.reason_combo.current(0)
        self.reason_combo.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(justify_frame,
            text=self.lang.get('notes_label', 'Note:'),
            font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=5)

        self.notes_var = tk.StringVar()
        ttk.Entry(justify_frame, textvariable=self.notes_var,
                  width=25).grid(row=0, column=3, sticky='ew', padx=5)

        ttk.Button(justify_frame,
            text=self.lang.get('btn_save_rows',
                               '✅ Salvează pt. rândurile selectate'),
            command=self._save_row_justification
        ).grid(row=0, column=4, padx=10)

        justify_frame.columnconfigure(1, weight=2)
        justify_frame.columnconfigure(3, weight=1)

        # --- Footer ---
        footer = ttk.Frame(self, padding=5)
        footer.pack(fill='x', padx=10)

        ttk.Button(footer,
            text=self.lang.get('btn_close', 'Închide'),
            command=self._on_close).pack(side='right', padx=5)

    # ================================================================
    # DATI
    # ================================================================
    def _load_details(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self._tree_data = {}

            import plan_alert_escalation as pae
            rows = pae.get_alerts_for_order_product(
                self.db.conn, self.order_number, self.product_name)

            count = 0
            for row in rows:
                tag = row.StatusColor if row.StatusColor in (
                    'red', 'out_of_plan') else ''
                future_label = '✓' if row.OnFuture else ''
                projected = str(row.ProjectedEnd) if row.ProjectedEnd else ''

                iid = self.tree.insert('', 'end', values=(
                    row.PhaseName,
                    row.QtyInXls or 0,
                    row.QtyProduced or 0,
                    row.QtyExpected or 0,
                    row.Deficit or 0,
                    row.StatusColor,
                    str(row.AlertDate),
                    projected,
                    future_label
                ), tags=(tag,))

                self._tree_data[iid] = {
                    'alert_id': row.AlertId,
                    'phase_name': row.PhaseName,
                    'alert_date': row.AlertDate,
                }
                count += 1

            self.count_label.config(
                text=f"{count} {self.lang.get('analytical_alerts', 'analytical alerts')}")

        except Exception as e:
            logger.error(f"Errore caricamento dettagli: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Eroare'), f"Eroare: {e}")

    # ================================================================
    # SELEZIONE
    # ================================================================
    def _select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def _deselect_all(self):
        self.tree.selection_remove(*self.tree.get_children())

    # ================================================================
    # SALVA ROW
    # ================================================================
    def _save_row_justification(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Atenție'),
                self.lang.get('select_rows',
                              'Selectați cel puțin o alertă din listă.'))
            return

        reason_text = self.reason_var.get().strip()
        if not reason_text:
            messagebox.showwarning(
                self.lang.get('warning', 'Atenție'),
                self.lang.get('select_reason', 'Selectați o motivație.'))
            return

        plan_response_id = None
        for rid, desc in self._reasons:
            if desc == reason_text:
                plan_response_id = rid
                break
        if plan_response_id is None:
            return

        notes = self.notes_var.get().strip()

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Confirm'),
            self.lang.get('confirm_save_rows',
                          'Save justification for {count} rows?').format(
                              count=len(selection))
            + f"\n\n{self.lang.get('reason_label', 'Reason:')} {reason_text}"
            + f"\n{self.lang.get('notes_label', 'Notes:')} {notes if notes else '—'}"):
            return

        import plan_alert_escalation as pae
        saved = 0
        for iid in selection:
            data = self._tree_data.get(iid)
            if not data:
                continue
            # Per ogni riga selezionata, recupera tutti gli AlertId
            # con stessa fase e data (possono esserci duplicati orari)
            alert_ids = pae.get_alert_ids_for_row(
                self.db.conn, self.order_number, self.product_name,
                data['phase_name'], data['alert_date'])
            if alert_ids:
                ok = pae.save_response(
                    self.db.conn, alert_ids, plan_response_id,
                    self.user_name, notes)
                if ok:
                    saved += len(alert_ids)

        if saved > 0:
            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('saved_justifications',
                              '{count} justifications saved successfully.').format(count=saved))
            self._load_details()
            self.notes_var.set('')

    # ================================================================
    # CHIUSURA
    # ================================================================
    def _on_close(self):
        if self._on_close_callback:
            self._on_close_callback()
        self.destroy()


def open_plan_discrepancy(parent, db, lang, user_name):
    """Funzione di apertura chiamata da main.py."""
    PlanDiscrepancyWindow(parent, db, lang, user_name)
