# -*- coding: utf-8 -*-
"""
Modulo GUI per l'inserimento giornaliero dei valori di stock.

Logica:
- Carica tutti gli item da CommunicationItems
- Selettore data per scegliere il giorno (default: oggi)
- Mostra i valori della data selezionata (se già inseriti) altrimenti campi vuoti
- INSERT o UPDATE su Communications
- Modifica consentita SOLO se User == utente loggato
- Alla chiusura invia email con valori inseriti + analisi rolling + YTD
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from tkcalendar import DateEntry
import logging
import threading
import os

logger = logging.getLogger("TraceabilityRS")


# ================================================================
# QUERY
# ================================================================

SQL_ITEMS = """
    SELECT [CommunicationItemId], [CommunitationHeather]
    FROM [Traceability_RS].[dbo].[CommunicationItems]
    ORDER BY [CommunicationItemId]
"""

SQL_DATE_VALUES = """
    SELECT c.[CommunicationId], c.[CommunicationItemId],
           c.[ValueforItem], c.[User]
    FROM [Traceability_RS].[dbo].[Communications] c
    WHERE CAST(c.[DateCommunication] AS DATE) = ?
"""

SQL_INSERT = """
    INSERT INTO [Traceability_RS].[dbo].[Communications]
        ([CommunicationItemId], [ValueforItem], [DateCommunication], [User])
    VALUES (?, ?, ?, ?)
"""

SQL_UPDATE = """
    UPDATE [Traceability_RS].[dbo].[Communications]
    SET [ValueforItem] = ?, [User] = ?
    WHERE [CommunicationId] = ?
"""

SQL_EMAIL_SETTING = """
    SELECT [Value]
    FROM [Traceability_RS].[dbo].[settings]
    WHERE [atribute] = 'Sys_email_stock_value'
"""


# ================================================================
# FORM PRINCIPALE
# ================================================================

class StockValueWindow(tk.Toplevel):
    """Finestra per l'inserimento giornaliero del valore stock."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('menu_stock_value', 'Stock Value'))
        self.geometry('720x560')
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        # Dati interni
        self._items = []        # [(CommunicationItemId, CommunitationHeather)]
        self._day_data = {}     # {item_id: {comm_id, value, user}}
        self._entry_vars = {}   # {item_id: tk.StringVar}
        self._has_saved = False
        self._saved_date = None # data dell'ultimo salvataggio per l'email

        self._build_ui()
        self._load_data()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ================================================================
    # UI
    # ================================================================
    def _build_ui(self):
        # ── Header ──
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)

        ttk.Label(header,
            text=f"{self.lang.get('logged_user', 'Operator')}: {self.user_name}",
            font=('Arial', 10, 'bold')).pack(side='left')

        # ── Date picker ──
        date_frame = ttk.Frame(self)
        date_frame.pack(fill='x', padx=10, pady=(0, 5))

        ttk.Label(date_frame,
            text=f"📅 {self.lang.get('stock_select_date', 'Date')}:",
            font=('Arial', 10, 'bold'),
            foreground='#1565C0').pack(side='left', padx=(0, 8))

        self.date_entry = DateEntry(date_frame,
            width=14, date_pattern='dd/mm/yyyy',
            maxdate=date.today(),
            font=('Arial', 11, 'bold'),
            foreground='#1565C0',
            state='readonly')
        self.date_entry.pack(side='left')
        self.date_entry.bind('<<DateEntrySelected>>', lambda e: self._load_data())

        ttk.Button(date_frame,
            text=self.lang.get('stock_today', '📌 Today'),
            command=self._go_today).pack(side='left', padx=10)

        # ── Info bar ──
        info_frame = ttk.Frame(self)
        info_frame.pack(fill='x', padx=10)
        self.info_label = ttk.Label(info_frame,
            text=self.lang.get('stock_fill_all',
                               'Fill in all items and save'),
            font=('Arial', 9, 'italic'), foreground='#666')
        self.info_label.pack(side='left')

        self.status_label = ttk.Label(info_frame, text="",
            font=('Arial', 9, 'bold'))
        self.status_label.pack(side='right')

        # ── Scrollable items frame ──
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        vsb = ttk.Scrollbar(canvas_frame, orient='vertical',
                             command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.items_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.items_frame, anchor='nw')
        self.items_frame.bind('<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Header colonne
        ttk.Label(self.items_frame,
            text=self.lang.get('stock_item', 'Item'),
            font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w',
                                               padx=10, pady=5)
        ttk.Label(self.items_frame,
            text=self.lang.get('stock_value_label', 'Value'),
            font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='w',
                                               padx=10, pady=5)
        ttk.Label(self.items_frame,
            text=self.lang.get('col_status', 'Status'),
            font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w',
                                               padx=10, pady=5)

        ttk.Separator(self.items_frame, orient='horizontal').grid(
            row=1, column=0, columnspan=3, sticky='ew', padx=5)

        # ── Footer bottoni ──
        footer = ttk.Frame(self, padding=5)
        footer.pack(fill='x', padx=10)

        self.btn_save = ttk.Button(footer,
            text=self.lang.get('stock_save_all', '✅ Save All'),
            command=self._save_all)
        self.btn_save.pack(side='left', padx=5)

        ttk.Button(footer,
            text=self.lang.get('btn_refresh', '🔄 Refresh'),
            command=self._load_data).pack(side='left', padx=5)

        ttk.Button(footer,
            text=self.lang.get('btn_close', 'Close'),
            command=self._on_close).pack(side='right', padx=5)

    # ================================================================
    # HELPERS
    # ================================================================
    def _get_selected_date(self):
        """Restituisce la data selezionata come date object."""
        return self.date_entry.get_date()

    def _go_today(self):
        """Reimposta il selettore data a oggi e ricarica."""
        self.date_entry.set_date(date.today())
        self._load_data()

    # ================================================================
    # CARICAMENTO DATI
    # ================================================================
    def _load_data(self):
        # Pulisci righe precedenti (tranne header e separator)
        for widget in self.items_frame.winfo_children():
            info = widget.grid_info()
            if info.get('row', 0) > 1:
                widget.destroy()
        self._entry_vars.clear()

        selected_date = self._get_selected_date()
        sel_date_str = selected_date.strftime('%Y-%m-%d')

        try:
            # 1. Carica items
            with self.db.conn.cursor() as cur:
                cur.execute(SQL_ITEMS)
                self._items = [(r.CommunicationItemId, r.CommunitationHeather)
                               for r in cur.fetchall()]

            # 2. Carica valori per la data selezionata
            with self.db.conn.cursor() as cur:
                cur.execute(SQL_DATE_VALUES, (sel_date_str,))
                self._day_data = {}
                for r in cur.fetchall():
                    self._day_data[r.CommunicationItemId] = {
                        'comm_id': r.CommunicationId,
                        'value': r.ValueforItem,
                        'user': r.User
                    }

            # 3. Costruisci righe
            filled = 0
            for idx, (item_id, item_name) in enumerate(self._items):
                row = idx + 2  # dopo header + separator

                ttk.Label(self.items_frame,
                    text=item_name or f'Item #{item_id}',
                    font=('Arial', 10)).grid(
                        row=row, column=0, sticky='w', padx=10, pady=3)

                var = tk.StringVar()
                existing = self._day_data.get(item_id)

                entry = ttk.Entry(self.items_frame, textvariable=var,
                                  width=20, justify='right')

                if existing:
                    var.set(str(existing['value'] or ''))
                    filled += 1
                    is_own = (existing['user'] or '').strip().upper() == \
                             self.user_name.strip().upper()
                    if is_own:
                        status_text = '✅ ' + self.lang.get('stock_editable', 'Editable')
                        status_color = '#2E7D32'
                    else:
                        status_text = '🔒 ' + (existing['user'] or '')
                        status_color = '#B71C1C'
                        entry.config(state='readonly')
                else:
                    status_text = '⬜ ' + self.lang.get('stock_empty', 'Empty')
                    status_color = '#757575'

                entry.grid(row=row, column=1, sticky='ew', padx=10, pady=3)

                ttk.Label(self.items_frame, text=status_text,
                    foreground=status_color,
                    font=('Arial', 9)).grid(
                        row=row, column=2, sticky='w', padx=10, pady=3)

                self._entry_vars[item_id] = var

            self.items_frame.columnconfigure(1, weight=1)

            # Status
            total = len(self._items)
            date_label = selected_date.strftime('%d/%m/%Y')
            self.status_label.config(
                text=f"{date_label}  —  {filled}/{total} {self.lang.get('stock_filled', 'filled')}",
                foreground='#2E7D32' if filled == total else '#E65100')

        except Exception as e:
            logger.error(f"Errore caricamento stock values: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Error'), str(e), parent=self)

    # ================================================================
    # SALVATAGGIO
    # ================================================================
    def _save_all(self):
        selected_date = self._get_selected_date()
        sel_date_sql = selected_date.strftime('%Y-%m-%d')

        # Verifica che tutti i campi siano compilati
        missing = []
        values_to_save = {}
        for item_id, item_name in self._items:
            var = self._entry_vars.get(item_id)
            if not var:
                continue
            val_str = var.get().strip()
            if not val_str:
                missing.append(item_name)
                continue
            try:
                val = float(val_str.replace(',', '.'))
                values_to_save[item_id] = val
            except ValueError:
                messagebox.showwarning(
                    self.lang.get('warning', 'Warning'),
                    self.lang.get('stock_invalid_number',
                                  'Invalid number for item: {item}').format(
                                      item=item_name),
                    parent=self)
                return

        if missing:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('stock_missing_items',
                              'Please fill in all items. Missing: {items}').format(
                                  items=', '.join(missing)),
                parent=self)
            return

        # Conferma
        date_label = selected_date.strftime('%d/%m/%Y')
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Confirm'),
            self.lang.get('stock_confirm_save',
                          'Save values for {count} items?').format(
                              count=len(values_to_save))
            + f"\n\n📅 {date_label}",
            parent=self):
            return

        try:
            saved = 0
            with self.db.conn.cursor() as cur:
                for item_id, val in values_to_save.items():
                    existing = self._day_data.get(item_id)
                    if existing:
                        # UPDATE (solo se stesso user)
                        is_own = (existing['user'] or '').strip().upper() == \
                                 self.user_name.strip().upper()
                        if not is_own:
                            continue  # skip — locked by another user
                        cur.execute(SQL_UPDATE,
                                    (val, self.user_name, existing['comm_id']))
                    else:
                        # INSERT con la data selezionata
                        cur.execute(SQL_INSERT,
                                    (item_id, val, sel_date_sql, self.user_name))
                    saved += 1

            self.db.conn.commit()
            self._has_saved = True
            self._saved_date = selected_date

            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('saved_justifications',
                              '{count} justifications saved successfully.').format(
                                  count=saved),
                parent=self)

            self._load_data()

        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore salvataggio stock values: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Error'), str(e), parent=self)

    # ================================================================
    # CHIUSURA + EMAIL
    # ================================================================
    def _on_close(self):
        if self._has_saved:
            # Invia email in background
            saved_date = self._saved_date or date.today()
            t = threading.Thread(target=self._send_email,
                                 args=(saved_date,), daemon=True)
            t.start()
        self.destroy()

    def _send_email(self, report_date):
        """Invia email con valori della data + analisi rolling + YTD."""
        try:
            # 1. Recupera destinatari
            with self.db.conn.cursor() as cur:
                cur.execute(SQL_EMAIL_SETTING)
                row = cur.fetchone()

            if not row or not row.Value:
                logger.warning("Stock Value: nessun destinatario in Sys_email_stock_value")
                return

            raw_emails = row.Value.strip()
            emails = [e.strip() for e in raw_emails.replace(';', ',').split(',')
                      if e.strip() and '@' in e.strip()]
            if not emails:
                logger.warning("Stock Value: nessun indirizzo email valido")
                return

            report_date_sql = report_date.strftime('%Y-%m-%d')
            report_date_str = report_date.strftime('%d/%m/%Y')

            # 2. Valori della data selezionata
            with self.db.conn.cursor() as cur:
                cur.execute("""
                    SELECT ci.[CommunitationHeather] AS ItemName,
                           c.[ValueforItem], c.[User]
                    FROM [Traceability_RS].[dbo].[Communications] c
                    INNER JOIN [Traceability_RS].[dbo].[CommunicationItems] ci
                        ON c.CommunicationItemId = ci.CommunicationItemId
                    WHERE CAST(c.[DateCommunication] AS DATE) = ?
                    ORDER BY ci.[CommunicationItemId]
                """, (report_date_sql,))
                day_values = cur.fetchall()

            if not day_values:
                logger.info("Stock Value: nessun valore per la data, email non inviata")
                return

            # 3. Storico per analisi rolling
            with self.db.conn.cursor() as cur:
                cur.execute("""
                    SELECT ci.[CommunitationHeather] AS ItemName,
                           SUM(c.[ValueforItem]) AS TotalValue,
                           MONTH(c.[DateCommunication]) AS CommMonth,
                           YEAR(c.[DateCommunication]) AS CommYear,
                           COUNT(*) AS EntryCount
                    FROM [Traceability_RS].[dbo].[Communications] c
                    INNER JOIN [Traceability_RS].[dbo].[CommunicationItems] ci
                        ON c.CommunicationItemId = ci.CommunicationItemId
                    WHERE c.[DateCommunication] >= DATEADD(MONTH, -12, GETDATE())
                    GROUP BY ci.[CommunitationHeather],
                             MONTH(c.[DateCommunication]),
                             YEAR(c.[DateCommunication])
                    ORDER BY ci.[CommunitationHeather],
                             YEAR(c.[DateCommunication]),
                             MONTH(c.[DateCommunication])
                """)
                history = cur.fetchall()

            # 4. YTD
            current_year = date.today().year
            with self.db.conn.cursor() as cur:
                cur.execute("""
                    SELECT ci.[CommunitationHeather] AS ItemName,
                           SUM(c.[ValueforItem]) AS YTDTotal,
                           AVG(c.[ValueforItem]) AS YTDAvg,
                           COUNT(*) AS YTDCount
                    FROM [Traceability_RS].[dbo].[Communications] c
                    INNER JOIN [Traceability_RS].[dbo].[CommunicationItems] ci
                        ON c.CommunicationItemId = ci.CommunicationItemId
                    WHERE YEAR(c.[DateCommunication]) = ?
                    GROUP BY ci.[CommunitationHeather]
                    ORDER BY ci.[CommunitationHeather]
                """, (current_year,))
                ytd_data = cur.fetchall()

            # 5. Costruisci email HTML
            # Tabella valori del giorno
            today_rows = ""
            for tv in day_values:
                val = tv.ValueforItem or 0
                today_rows += f"""
                <tr>
                    <td style="padding:8px 12px; border:1px solid #dee2e6;">{tv.ItemName}</td>
                    <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:right;
                               font-weight:bold;">{val:,.2f}</td>
                    <td style="padding:8px 12px; border:1px solid #dee2e6;">{tv.User or ''}</td>
                </tr>"""

            # Tabella rolling mensile
            rolling_rows = ""
            prev_values = {}
            for h in history:
                item = h.ItemName
                total = float(h.TotalValue or 0)
                month_label = f"{h.CommYear}-{h.CommMonth:02d}"
                prev = prev_values.get(item)
                if prev is not None and prev != 0:
                    change_pct = ((total - prev) / abs(prev)) * 100
                    change_str = f"{change_pct:+.1f}%"
                    change_color = '#2E7D32' if change_pct >= 0 else '#B71C1C'
                else:
                    change_str = "—"
                    change_color = '#666'
                prev_values[item] = total

                rolling_rows += f"""
                <tr>
                    <td style="padding:6px 10px; border:1px solid #dee2e6;">{item}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:center;">{month_label}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:right;">{total:,.2f}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:center;
                               color:{change_color}; font-weight:bold;">{change_str}</td>
                </tr>"""

            # Tabella YTD
            ytd_rows = ""
            for y in ytd_data:
                ytd_total = float(y.YTDTotal or 0)
                ytd_avg = float(y.YTDAvg or 0)
                ytd_rows += f"""
                <tr>
                    <td style="padding:6px 10px; border:1px solid #dee2e6;">{y.ItemName}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:right;">{ytd_total:,.2f}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:right;">{ytd_avg:,.2f}</td>
                    <td style="padding:6px 10px; border:1px solid #dee2e6; text-align:center;">{y.YTDCount}</td>
                </tr>"""

            # ── 5b. ANALISI INTELLIGENTE ──────────────────────────────
            # Confronto valore odierno vs media 30gg + deviazione standard
            analysis_rows = ""
            alerts_html = ""
            try:
                with self.db.conn.cursor() as cur:
                    cur.execute("""
                        SELECT ci.[CommunitationHeather] AS ItemName,
                               AVG(c.[ValueforItem]) AS Avg30,
                               STDEV(c.[ValueforItem]) AS StDev30,
                               MIN(c.[ValueforItem]) AS Min30,
                               MAX(c.[ValueforItem]) AS Max30,
                               COUNT(*) AS Count30
                        FROM [Traceability_RS].[dbo].[Communications] c
                        INNER JOIN [Traceability_RS].[dbo].[CommunicationItems] ci
                            ON c.CommunicationItemId = ci.CommunicationItemId
                        WHERE c.[DateCommunication] >= DATEADD(DAY, -30, GETDATE())
                        GROUP BY ci.[CommunitationHeather]
                        ORDER BY ci.[CommunitationHeather]
                    """)
                    stats_30d = {r.ItemName: r for r in cur.fetchall()}

                # Trend ultimi 7 giorni per ogni item
                with self.db.conn.cursor() as cur:
                    cur.execute("""
                        SELECT ci.[CommunitationHeather] AS ItemName,
                               c.[ValueforItem],
                               CAST(c.[DateCommunication] AS DATE) AS CommDate
                        FROM [Traceability_RS].[dbo].[Communications] c
                        INNER JOIN [Traceability_RS].[dbo].[CommunicationItems] ci
                            ON c.CommunicationItemId = ci.CommunicationItemId
                        WHERE c.[DateCommunication] >= DATEADD(DAY, -7, GETDATE())
                        ORDER BY ci.[CommunitationHeather], c.[DateCommunication]
                    """)
                    trend_raw = cur.fetchall()

                # Gruppo trend per item
                trend_by_item = {}
                for r in trend_raw:
                    trend_by_item.setdefault(r.ItemName, []).append(
                        float(r.ValueforItem or 0))

                alert_items = []  # lista di alert testuali

                for tv in day_values:
                    item_name = tv.ItemName
                    current_val = float(tv.ValueforItem or 0)
                    stat = stats_30d.get(item_name)

                    if not stat or not stat.Count30 or stat.Count30 < 3:
                        # Dati insufficienti
                        analysis_rows += f"""
                        <tr style="background-color:#f8f9fa;">
                            <td style="padding:8px 12px; border:1px solid #dee2e6;">{item_name}</td>
                            <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:right;">{current_val:,.2f}</td>
                            <td colspan="5" style="padding:8px 12px; border:1px solid #dee2e6; text-align:center;
                                       color:#999; font-style:italic;">Insufficient data (&lt;3 entries)</td>
                        </tr>"""
                        continue

                    avg_30 = float(stat.Avg30 or 0)
                    std_30 = float(stat.StDev30 or 0)
                    min_30 = float(stat.Min30 or 0)
                    max_30 = float(stat.Max30 or 0)

                    # % rispetto alla media
                    if avg_30 != 0:
                        delta_pct = ((current_val - avg_30) / abs(avg_30)) * 100
                    else:
                        delta_pct = 0.0

                    # Anomalia: valore fuori 1.5 * σ dalla media
                    is_anomaly = False
                    anomaly_icon = ""
                    if std_30 > 0:
                        z_score = abs(current_val - avg_30) / std_30
                        if z_score > 2.0:
                            is_anomaly = True
                            anomaly_icon = "🔴"
                            alert_items.append(
                                f"<strong>{item_name}</strong>: value {current_val:,.2f} "
                                f"deviates <strong>{z_score:.1f}σ</strong> from mean "
                                f"({avg_30:,.2f}) — <em>Critical anomaly</em>")
                        elif z_score > 1.5:
                            is_anomaly = True
                            anomaly_icon = "🟡"
                            alert_items.append(
                                f"<strong>{item_name}</strong>: value {current_val:,.2f} "
                                f"deviates <strong>{z_score:.1f}σ</strong> from mean "
                                f"({avg_30:,.2f}) — <em>Warning</em>")

                    # Trend 7gg
                    vals_7d = trend_by_item.get(item_name, [])
                    if len(vals_7d) >= 2:
                        trend_diff = vals_7d[-1] - vals_7d[0]
                        if trend_diff > 0:
                            trend_icon = "📈"
                            trend_label = "Rising"
                        elif trend_diff < 0:
                            trend_icon = "📉"
                            trend_label = "Declining"
                        else:
                            trend_icon = "➡️"
                            trend_label = "Stable"
                        # Alerta per trend costantemente in crescita
                        if len(vals_7d) >= 4 and all(
                            vals_7d[i] <= vals_7d[i+1] for i in range(len(vals_7d)-1)):
                            alert_items.append(
                                f"<strong>{item_name}</strong>: "
                                f"stock rising for {len(vals_7d)} consecutive days "
                                f"({vals_7d[0]:,.0f} → {vals_7d[-1]:,.0f})")
                    else:
                        trend_icon = "—"
                        trend_label = "N/A"

                    # Colore riga
                    if is_anomaly:
                        row_bg = "#fff3cd" if anomaly_icon == "🟡" else "#f8d7da"
                    else:
                        row_bg = "#ffffff"

                    delta_color = '#2E7D32' if delta_pct <= 5 else (
                        '#E65100' if delta_pct <= 15 else '#B71C1C')
                    delta_str = f"{delta_pct:+.1f}%"

                    analysis_rows += f"""
                    <tr style="background-color:{row_bg};">
                        <td style="padding:8px 12px; border:1px solid #dee2e6;">{anomaly_icon} {item_name}</td>
                        <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:right;
                                   font-weight:bold;">{current_val:,.2f}</td>
                        <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:right;">{avg_30:,.2f}</td>
                        <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:center;
                                   color:{delta_color}; font-weight:bold;">{delta_str}</td>
                        <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:center;">{min_30:,.2f} — {max_30:,.2f}</td>
                        <td style="padding:8px 12px; border:1px solid #dee2e6; text-align:center;">{trend_icon} {trend_label}</td>
                    </tr>"""

                # Alert box
                if alert_items:
                    alerts_list = "".join(
                        f'<li style="margin:6px 0; font-size:13px;">{a}</li>'
                        for a in alert_items)
                    alerts_html = f"""
                    <div style="background-color:#fff3cd; border-left:4px solid #ffc107;
                                padding:12px 16px; margin:20px 0; border-radius:4px;">
                        <p style="margin:0 0 8px; font-weight:bold; font-size:14px;
                                  color:#856404;">⚠️ Attention Required</p>
                        <ul style="margin:0; padding-left:20px;">{alerts_list}</ul>
                    </div>"""

            except Exception as e:
                logger.warning(f"Stock analysis section failed: {e}")
                analysis_rows = ""
                alerts_html = ""

            # ── Sezione analisi HTML ──
            if analysis_rows:
                analysis_section = f"""
                <!-- ANALISI INTELLIGENTE -->
                <h3 style="color:#0056b3; margin-top:30px;">🔍 Stock Analysis — Anomaly Detection</h3>
                <p style="font-size:12px; color:#666; margin-bottom:8px;">
                    Comparing today's values against the 30-day average. 
                    🟡 = Warning (>1.5σ), 🔴 = Critical (>2σ)
                </p>
                <table style="border-collapse:collapse; width:100%; margin:10px 0;">
                    <thead>
                    <tr style="background-color:#6c3483; color:#fff;">
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:left;">Item</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:right;">Today</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:right;">Avg 30d</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">vs Avg</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">Range 30d</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">Trend 7d</th>
                    </tr>
                    </thead>
                    <tbody>{analysis_rows}</tbody>
                </table>
                {alerts_html}"""
            else:
                analysis_section = ""

            body_html = f"""
            <html>
            <body style="font-family:'Segoe UI',Arial,sans-serif; color:#333; margin:0; padding:0;">
            <div style="max-width:750px; margin:0 auto; padding:20px;">
                <!-- Header -->
                <div style="border-bottom:3px solid #0056b3; padding-bottom:15px; margin-bottom:20px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="font-size:22px; font-weight:bold; color:#0056b3;">
                            Stock Value Report — {report_date_str}
                        </td>
                        <td style="text-align:right;">
                            <img src="cid:company_logo" alt="Vandewiele"
                                 style="width:120px; height:auto;" />
                        </td>
                    </tr>
                    </table>
                </div>

                <p style="font-size:14px;">Dear colleagues,</p>
                <p style="font-size:14px;">
                    Below are the stock values for <strong>{report_date_str}</strong>
                    entered by <strong>{self.user_name}</strong>.
                </p>

                <!-- VALORI DEL GIORNO -->
                <h3 style="color:#0056b3; margin-top:25px;">📊 Values for {report_date_str}</h3>
                <table style="border-collapse:collapse; width:100%; margin:10px 0;">
                    <thead>
                    <tr style="background-color:#0056b3; color:#fff;">
                        <th style="padding:10px 12px; border:1px solid #dee2e6; text-align:left;">Item</th>
                        <th style="padding:10px 12px; border:1px solid #dee2e6; text-align:right;">Value</th>
                        <th style="padding:10px 12px; border:1px solid #dee2e6; text-align:left;">User</th>
                    </tr>
                    </thead>
                    <tbody>{today_rows}</tbody>
                </table>

                {analysis_section}

                <!-- ROLLING MENSILE -->
                <h3 style="color:#0056b3; margin-top:30px;">📈 Monthly Rolling Analysis (Last 12 Months)</h3>
                <table style="border-collapse:collapse; width:100%; margin:10px 0;">
                    <thead>
                    <tr style="background-color:#495057; color:#fff;">
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:left;">Item</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">Month</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:right;">Total</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">Change</th>
                    </tr>
                    </thead>
                    <tbody>{rolling_rows}</tbody>
                </table>

                <!-- YTD -->
                <h3 style="color:#0056b3; margin-top:30px;">📅 Year-To-Date ({current_year})</h3>
                <table style="border-collapse:collapse; width:100%; margin:10px 0;">
                    <thead>
                    <tr style="background-color:#28a745; color:#fff;">
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:left;">Item</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:right;">YTD Total</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:right;">YTD Avg</th>
                        <th style="padding:8px 10px; border:1px solid #dee2e6; text-align:center;">Entries</th>
                    </tr>
                    </thead>
                    <tbody>{ytd_rows}</tbody>
                </table>

                <!-- Footer -->
                <div style="margin-top:30px; padding-top:15px; border-top:1px solid #dee2e6;">
                    <p style="font-size:11px; color:#888; line-height:1.5;">
                        This is an automated notification generated by the TraceabilityRS system.
                        Please do not reply to this email.<br/>
                        &copy; {datetime.now().year} Vandewiele Romania &mdash; All rights reserved.
                    </p>
                </div>
            </div>
            </body>
            </html>
            """

            # 6. Invia
            from email_connector import EmailSender
            sender = EmailSender()
            sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")

            attachments = []
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            if os.path.exists(logo_path):
                attachments.append(('inline', logo_path, 'company_logo'))

            sender.send_email(
                to_email=emails[0],
                subject=f"Stock Value Report — {report_date_str}",
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=emails[1:] if len(emails) > 1 else None
            )

            logger.info(f"Stock Value email inviata a {len(emails)} destinatari "
                        f"per data {report_date_str}")

        except Exception as e:
            logger.error(f"Errore invio email Stock Value: {e}", exc_info=True)


# ================================================================
# ENTRY POINT
# ================================================================

def open_stock_value(parent, db, lang, user_name):
    """Funzione di apertura chiamata da main.py."""
    StockValueWindow(parent, db, lang, user_name)
