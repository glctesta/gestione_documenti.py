"""
kit_dashboard_gui.py
Dashboard Stato Kit e Reporting — Sprint 5
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §8.2).

Sola lettura, nessun login (§8.1). Tre schede:
  - Dashboard: stato per ordine (WH / Preformatura / Produzione), sessioni
    riprendibili, alert
  - Storico Eccezioni: filtri data/ordine + export Excel
  - Analisi Cause: conteggi mappati sulle 5 cause della §1.1,
    top materiali richiesti, ordini con piu' eccezioni
"""
import logging
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk, messagebox, filedialog

import kit_dashboard_logic as kdl

logger = logging.getLogger("PlanMonitor")

PRIORITY_BADGE = {0: '⬜ P0', 1: '🔴 P1', 2: '🟠 P2', 3: '🟡 P3'}
SYMBOL = {'G': '🟢', 'O': '🟠', 'R': '🔴', '-': '⬜'}


def open_kit_dashboard(parent, db, lang):
    return KitDashboardWindow(parent, db, lang)


class KitDashboardWindow(tk.Toplevel):

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(lang.get('kit_dash_title', 'Dashboard Stato Kit'))
        self.geometry("1100x640")
        self.transient(parent)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=8, pady=8)

        self.dash_frame = ttk.Frame(self.notebook, padding=10)
        self.hist_frame = ttk.Frame(self.notebook, padding=10)
        self.causes_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.dash_frame, text=lang.get('kit_dash_tab', 'Dashboard'))
        self.notebook.add(self.hist_frame, text=lang.get('kit_dash_tab_history',
                                                         'Storico Eccezioni'))
        self.notebook.add(self.causes_frame, text=lang.get('kit_dash_tab_causes',
                                                           'Analisi Cause'))

        self._build_dashboard_tab()
        self._build_history_tab()
        self._build_causes_tab()

        self._refresh_dashboard()
        self._refresh_history()
        self._refresh_causes()
        logger.info("KitDashboardWindow aperta")

    # ─────────────────────────── Dashboard ───────────────────────────── #

    def _build_dashboard_tab(self):
        f = self.dash_frame
        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Button(top, text=self.lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh_dashboard).pack(side='left')
        self.dash_summary = tk.StringVar()
        ttk.Label(top, textvariable=self.dash_summary).pack(side='right')

        cols = ('order', 'priority', 'status', 'wh', 'pf', 'prod',
                'session', 'requests', 'alert', 'updated')
        self.dash_tree = ttk.Treeview(f, columns=cols, show='headings',
                                      selectmode='browse')
        headings = {
            'order': self.lang.get('kit_col_order', 'Ordine'),
            'priority': self.lang.get('kit_col_priority', 'Priorità'),
            'status': self.lang.get('kit_col_status', 'Stato'),
            'wh': 'WH',
            'pf': self.lang.get('kit_dash_col_pf', 'Preform.'),
            'prod': self.lang.get('kit_dash_col_prod', 'Produz.'),
            'session': self.lang.get('kit_dash_col_session', 'Sessione'),
            'requests': self.lang.get('kit_dash_col_requests', 'Rich. aperte'),
            'alert': 'Alert',
            'updated': self.lang.get('kit_dash_col_updated', 'Aggiornato'),
        }
        widths = {'order': 100, 'priority': 75, 'status': 200, 'wh': 55,
                  'pf': 70, 'prod': 70, 'session': 130, 'requests': 90,
                  'alert': 60, 'updated': 120}
        for c in cols:
            self.dash_tree.heading(c, text=headings[c])
            self.dash_tree.column(c, width=widths[c],
                                  anchor='w' if c == 'status' else 'center')
        vsb = ttk.Scrollbar(f, orient='vertical', command=self.dash_tree.yview)
        self.dash_tree.configure(yscrollcommand=vsb.set)
        self.dash_tree.pack(side='left', expand=True, fill='both')
        vsb.pack(side='left', fill='y')
        self.dash_tree.tag_configure('alert', background='#ffd6d6')
        self.dash_tree.tag_configure('session', background='#fff3cd')

    def _refresh_dashboard(self):
        cursor = self.db.conn.cursor()
        try:
            rows = kdl.dashboard_rows(cursor)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self.dash_tree.delete(*self.dash_tree.get_children())
        n_alert = 0
        for r in rows:
            session = ''
            if r['session_phase']:
                session = f"⏸ {r['session_phase']} ({r['session_status']})"
            alert = '⚠️' if r['alert'] else ''
            if r['alert']:
                n_alert += 1
            tag = 'alert' if r['alert'] else ('session' if session else '')
            updated = r['updated_date'].strftime('%d/%m %H:%M') if r['updated_date'] else ''
            self.dash_tree.insert('', 'end', values=(
                r['order_number'], PRIORITY_BADGE.get(r['priority'], r['priority']),
                r['kit_status'],
                SYMBOL.get(r['wh'], '⬜'), SYMBOL.get(r['pf'], '⬜'),
                SYMBOL.get(r['prod'], '⬜'),
                session, r['open_requests'] or '', alert, updated), tags=(tag,))
        self.dash_summary.set(
            self.lang.get('kit_dash_summary', '{n} ordini in lavorazione — {a} con alert')
            .replace('{n}', str(len(rows))).replace('{a}', str(n_alert)))

    # ───────────────────────── Storico Eccezioni ─────────────────────── #

    def _build_history_tab(self):
        f = self.hist_frame
        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Label(top, text=self.lang.get('kit_dash_from', 'Dal (gg/mm/aaaa):')
                  ).pack(side='left')
        self.from_var = tk.StringVar(
            value=(date.today() - timedelta(days=30)).strftime('%d/%m/%Y'))
        ttk.Entry(top, textvariable=self.from_var, width=12).pack(side='left', padx=4)
        ttk.Label(top, text=self.lang.get('kit_dash_to', 'Al:')).pack(side='left')
        self.to_var = tk.StringVar(value=date.today().strftime('%d/%m/%Y'))
        ttk.Entry(top, textvariable=self.to_var, width=12).pack(side='left', padx=4)
        ttk.Label(top, text=self.lang.get('kit_search_order', 'Cerca ordine:')
                  ).pack(side='left', padx=(12, 0))
        self.order_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.order_var, width=14).pack(side='left', padx=4)
        ttk.Button(top, text=self.lang.get('kit_btn_search', 'Cerca'),
                   command=self._refresh_history).pack(side='left', padx=4)
        ttk.Button(top, text=self.lang.get('kit_dash_btn_export', 'Esporta Excel'),
                   command=self._export_history).pack(side='right')

        cols = ('date', 'order', 'phase', 'event', 'material', 'unique',
                'expected', 'actual', 'operator', 'notes')
        self.hist_tree = ttk.Treeview(f, columns=cols, show='headings',
                                      selectmode='browse')
        headings = {
            'date': self.lang.get('kit_col_set_date', 'Data'),
            'order': self.lang.get('kit_col_order', 'Ordine'),
            'phase': self.lang.get('kit_req_col_phase', 'Fase'),
            'event': self.lang.get('kit_dash_col_event', 'Evento'),
            'material': self.lang.get('kit_col_material', 'Codice Materiale'),
            'unique': 'Unique Nr',
            'expected': self.lang.get('kit_dash_col_expected', 'Attesa'),
            'actual': self.lang.get('kit_dash_col_actual', 'Effettiva'),
            'operator': self.lang.get('kit_operator', 'Operatore'),
            'notes': self.lang.get('kit_dash_col_notes', 'Note'),
        }
        widths = {'date': 105, 'order': 110, 'phase': 90, 'event': 150,
                  'material': 140, 'unique': 115, 'expected': 65, 'actual': 65,
                  'operator': 130, 'notes': 220}
        for c in cols:
            self.hist_tree.heading(c, text=headings[c])
            self.hist_tree.column(c, width=widths[c],
                                  anchor='w' if c in ('material', 'operator', 'notes') else 'center')
        vsb = ttk.Scrollbar(f, orient='vertical', command=self.hist_tree.yview)
        self.hist_tree.configure(yscrollcommand=vsb.set)
        self.hist_tree.pack(side='left', expand=True, fill='both')
        vsb.pack(side='left', fill='y')
        self.hist_tree.tag_configure('fail', background='#ffd6d6')
        self.hist_tree.tag_configure('derog', background='#ffe8cc')
        self._hist_rows = []

    def _parse_date(self, txt):
        txt = txt.strip()
        if not txt:
            return None
        try:
            d, m, y = txt.split('/')
            return date(int(y), int(m), int(d))
        except Exception:
            return None

    def _refresh_history(self):
        cursor = self.db.conn.cursor()
        try:
            self._hist_rows = kdl.exceptions_history(
                cursor,
                date_from=self._parse_date(self.from_var.get()),
                date_to=self._parse_date(self.to_var.get()),
                order_filter=self.order_var.get().strip())
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self.hist_tree.delete(*self.hist_tree.get_children())
        for r in self._hist_rows:
            tag = ('fail' if r['event_type'] == 'VERIFY_FAIL'
                   else 'derog' if r['event_type'] == 'CLOSE_DEROGATION' else '')
            self.hist_tree.insert('', 'end', values=(
                r['event_date'].strftime('%d/%m/%y %H:%M') if r['event_date'] else '',
                r['order_number'], r['phase'], r['event_type'],
                r['material_code'] or '', r['unique_number'] or '',
                f"{float(r['qty_expected']):g}" if r['qty_expected'] is not None else '',
                f"{float(r['qty_actual']):g}" if r['qty_actual'] is not None else '',
                r['operator'], r['notes'] or ''), tags=(tag,))

    def _export_history(self):
        if not self._hist_rows:
            messagebox.showinfo(self.lang.get('info_title', 'Informazione'),
                                self.lang.get('kit_dash_msg_no_data', 'Nessun dato da esportare'),
                                parent=self)
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension='.xlsx',
            filetypes=[('Excel', '*.xlsx')],
            initialfile=f"kit_eccezioni_{date.today():%Y%m%d}.xlsx")
        if not path:
            return
        try:
            kdl.export_exceptions_xlsx(self._hist_rows, path)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_dash_msg_exported', 'Esportate {n} righe in:\n{path}')
            .replace('{n}', str(len(self._hist_rows))).replace('{path}', path),
            parent=self)

    # ───────────────────────── Analisi Cause ─────────────────────────── #

    def _build_causes_tab(self):
        f = self.causes_frame
        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Label(top, text=self.lang.get('kit_dash_from', 'Dal (gg/mm/aaaa):')
                  ).pack(side='left')
        self.c_from_var = tk.StringVar(
            value=(date.today() - timedelta(days=90)).strftime('%d/%m/%Y'))
        ttk.Entry(top, textvariable=self.c_from_var, width=12).pack(side='left', padx=4)
        ttk.Label(top, text=self.lang.get('kit_dash_to', 'Al:')).pack(side='left')
        self.c_to_var = tk.StringVar(value=date.today().strftime('%d/%m/%Y'))
        ttk.Entry(top, textvariable=self.c_to_var, width=12).pack(side='left', padx=4)
        ttk.Button(top, text=self.lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh_causes).pack(side='left', padx=6)

        body = ttk.Frame(f)
        body.pack(expand=True, fill='both')

        left = ttk.LabelFrame(body, text=self.lang.get(
            'kit_dash_causes_frame', 'Cause ricorrenti (§1.1)'), padding=6)
        left.pack(side='left', expand=True, fill='both', padx=(0, 6))
        self.causes_tree = ttk.Treeview(left, columns=('cause', 'count'),
                                        show='headings', height=9)
        self.causes_tree.heading('cause', text=self.lang.get('kit_dash_col_cause', 'Causa'))
        self.causes_tree.heading('count', text=self.lang.get('kit_dash_col_count', 'Eventi'))
        self.causes_tree.column('cause', width=380, anchor='w')
        self.causes_tree.column('count', width=70, anchor='center')
        self.causes_tree.pack(expand=True, fill='both')

        right = ttk.Frame(body)
        right.pack(side='left', expand=True, fill='both')

        mat_frame = ttk.LabelFrame(right, text=self.lang.get(
            'kit_dash_top_materials', 'Top materiali richiesti'), padding=6)
        mat_frame.pack(expand=True, fill='both', pady=(0, 6))
        self.mat_tree = ttk.Treeview(mat_frame, columns=('material', 'n', 'qty'),
                                     show='headings', height=6)
        self.mat_tree.heading('material', text=self.lang.get('kit_col_material', 'Codice Materiale'))
        self.mat_tree.heading('n', text=self.lang.get('kit_dash_col_nreq', 'Richieste'))
        self.mat_tree.heading('qty', text=self.lang.get('kit_dash_col_totqty', 'Qtà totale'))
        self.mat_tree.column('material', width=200, anchor='w')
        self.mat_tree.column('n', width=80, anchor='center')
        self.mat_tree.column('qty', width=90, anchor='center')
        self.mat_tree.pack(expand=True, fill='both')

        ord_frame = ttk.LabelFrame(right, text=self.lang.get(
            'kit_dash_top_orders', 'Ordini con più eccezioni'), padding=6)
        ord_frame.pack(expand=True, fill='both')
        self.ord_tree = ttk.Treeview(ord_frame, columns=('order', 'n'),
                                     show='headings', height=6)
        self.ord_tree.heading('order', text=self.lang.get('kit_col_order', 'Ordine'))
        self.ord_tree.heading('n', text=self.lang.get('kit_dash_col_count', 'Eventi'))
        self.ord_tree.column('order', width=160, anchor='w')
        self.ord_tree.column('n', width=80, anchor='center')
        self.ord_tree.pack(expand=True, fill='both')

    def _refresh_causes(self):
        cursor = self.db.conn.cursor()
        try:
            result = kdl.cause_analysis(
                cursor,
                date_from=self._parse_date(self.c_from_var.get()),
                date_to=self._parse_date(self.c_to_var.get()))
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self.causes_tree.delete(*self.causes_tree.get_children())
        for c in result['causes']:
            label = self.lang.get(c['key'], c['cause'])
            self.causes_tree.insert('', 'end', values=(label, c['count']))
        self.mat_tree.delete(*self.mat_tree.get_children())
        for m in result['top_materials']:
            qty = m['total_qty']
            self.mat_tree.insert('', 'end', values=(
                m['material_code'], m['n_requests'],
                str(int(qty)) if qty == int(qty) else f"{qty:g}"))
        self.ord_tree.delete(*self.ord_tree.get_children())
        for o in result['top_orders']:
            self.ord_tree.insert('', 'end', values=(o['order_number'], o['n_exceptions']))
