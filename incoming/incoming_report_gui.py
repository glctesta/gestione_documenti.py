# -*- coding: utf-8 -*-
"""
incoming/incoming_report_gui.py

Finestra "Report — Ricezione": report di periodo della situazione MPN.

Filtri combinabili: periodo (da/a su data richiesta), tipo richiesta,
fornitore, codice prodotto (MPN richiesto), MPN errato, MPN soluzione,
stato (tutte / evase / non evase). La griglia si ordina per qualsiasi
colonna (click sull'intestazione), inclusa la data di evasione e il
tempo trascorso tra richiesta ed evasione.

Esportazione Excel: file con blocco filtri applicati + riga intestazioni
formattata (grassetto, riempimento, freeze pani).

Entry point: open_incoming_report_window(master, db, lang)
Nessun login richiesto.
"""
from datetime import datetime, date
import logging
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from tkcalendar import DateEntry
except ImportError:  # tkcalendar e' una dipendenza del progetto, fallback di sicurezza
    DateEntry = None

try:
    from . import incoming_db
except ImportError:  # esecuzione come script standalone
    import incoming_db

logger = logging.getLogger(__name__)


def open_incoming_report_window(master, db, lang):
    """Apre la finestra di report Ricezione."""
    IncomingReportWindow(master, db, lang)


def _as_datetime(value):
    """Normalizza pyodbc datetime / date / stringa in datetime, oppure None."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(value[:19], fmt)
            except ValueError:
                continue
    return None


def _fmt_dt(value):
    """Formatta un datetime/pyodbc date in 'DD/MM/YYYY HH:MM'."""
    dt = _as_datetime(value)
    return dt.strftime('%d/%m/%Y %H:%M') if dt else ''


def _fmt_elapsed_minutes(minutes):
    """Minuti -> '3g 5h', '2h 14m', '45m'."""
    if minutes is None:
        return ''
    minutes = max(0, int(minutes))
    days, rem = divmod(minutes, 1440)
    hours, mins = divmod(rem, 60)
    if days:
        return f"{days}g {hours}h"
    if hours:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"


def elapsed_minutes(row):
    """Minuti tra richiesta ed evasione; None se non evasa o dati mancanti."""
    requested = _as_datetime(row.get('RequestedOn'))
    answered = _as_datetime(row.get('AnsweredOn'))
    if not requested or not answered:
        return None
    return int((answered - requested).total_seconds() // 60)


class IncomingReportWindow(tk.Toplevel):
    """Report di periodo delle richieste Ricezione con filtri, ordinamento ed export."""

    # (col_id, sort_key, width, anchor) — sort_key: nome chiave nella riga dict
    # oppure callable(riga) -> valore di ordinamento
    _COLUMNS = (
        ('number', 'RequestNumber', 150, 'w'),
        ('type', '_type_sort', 130, 'w'),
        ('supplier', 'SupplierName', 190, 'w'),
        ('ddt', 'DdtNumber', 100, 'w'),
        ('ddt_date', 'DdtDate', 90, 'w'),
        ('po', 'PurOrderNumber', 100, 'w'),
        ('mpn', 'MpnCode', 110, 'w'),
        ('wrong_mpn', 'WrongMpn', 110, 'w'),
        ('qty_receive', 'QtyToReceive', 80, 'e'),
        ('qty_expected', 'QtyExpectedPerPo', 80, 'e'),
        ('requested_by', 'RequestedBy', 120, 'w'),
        ('requested_on', 'RequestedOn', 130, 'w'),
        ('host', 'RequesterHost', 110, 'w'),
        ('status', '_status_sort', 110, 'w'),
        ('answer_mpn', 'AnswerMpnCode', 110, 'w'),
        ('answered_by', 'AnsweredBy', 110, 'w'),
        ('answered_on', 'AnsweredOn', 130, 'w'),
        ('elapsed', '_elapsed_sort', 100, 'e'),
    )

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang
        L = self.lang.get

        self.title(L('inc_rep_title', 'Report Ricezione — situazione MPN'))
        self.geometry('1240x680')
        self.minsize(1000, 560)
        self.transient(master)

        self._rows = []            # righe correnti (dict) gia' filtrate
        self._sort_col = 'requested_on'
        self._sort_desc = True
        self._type_key_by_label = {
            incoming_db.type_label(L, k): k for k in incoming_db.REQUEST_TYPES}

        self._build_ui()
        self.grab_set()
        self._search()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        L = self.lang.get

        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('inc_rep_title', 'Report Ricezione — situazione MPN'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)

        # ── Filtri ──
        filt = ttk.LabelFrame(self, text=L('inc_rep_filters', 'Filtri'), padding=8)
        filt.pack(fill=tk.X, padx=10, pady=6)

        # Riga 1: periodo + stato
        r1 = ttk.Frame(filt)
        r1.pack(fill=tk.X, pady=2)
        ttk.Label(r1, text=L('inc_rep_filter_from', 'Da:'), width=16).pack(side=tk.LEFT)
        self._v_from = tk.StringVar()
        if DateEntry:
            de_from = DateEntry(r1, textvariable=self._v_from, width=12,
                                background='darkblue', foreground='white',
                                borderwidth=2, date_pattern='dd/mm/yyyy')
        else:
            de_from = ttk.Entry(r1, textvariable=self._v_from, width=12)
        de_from.pack(side=tk.LEFT, padx=4)
        ttk.Label(r1, text=L('inc_rep_filter_to', 'A:'), width=4).pack(side=tk.LEFT)
        self._v_to = tk.StringVar()
        if DateEntry:
            de_to = DateEntry(r1, textvariable=self._v_to, width=12,
                              background='darkblue', foreground='white',
                              borderwidth=2, date_pattern='dd/mm/yyyy')
        else:
            de_to = ttk.Entry(r1, textvariable=self._v_to, width=12)
        de_to.pack(side=tk.LEFT, padx=4)
        ttk.Label(r1, text=L('inc_rep_filter_status', 'Stato:'), width=8).pack(side=tk.LEFT, padx=(16, 0))
        self._v_status = tk.StringVar()
        self._status_labels = {
            L('inc_rep_status_all', '(tutte)'): '',
            L('inc_rep_status_answered', 'Evase'): 'EVASE',
            L('inc_rep_status_pending', 'Non evase'): 'NON_EVASE',
        }
        cb_status = ttk.Combobox(r1, textvariable=self._v_status, state='readonly', width=14,
                                 values=list(self._status_labels.keys()))
        cb_status.current(0)
        cb_status.pack(side=tk.LEFT, padx=4)

        # Riga 2: tipo + fornitore
        r2f = ttk.Frame(filt)
        r2f.pack(fill=tk.X, pady=2)
        ttk.Label(r2f, text=L('inc_rep_filter_type', 'Tipo:'), width=16).pack(side=tk.LEFT)
        self._v_type = tk.StringVar()
        cb_type = ttk.Combobox(r2f, textvariable=self._v_type, state='readonly', width=28,
                               values=[L('inc_sol_all_types', '(tutti)')] +
                               list(self._type_key_by_label.keys()))
        cb_type.current(0)
        cb_type.pack(side=tk.LEFT, padx=4)
        ttk.Label(r2f, text=L('inc_rep_filter_supplier', 'Fornitore:'), width=10).pack(side=tk.LEFT, padx=(16, 0))
        self._v_supplier = tk.StringVar()
        ttk.Entry(r2f, textvariable=self._v_supplier, width=28).pack(side=tk.LEFT, padx=4)

        # Riga 3: MPN richiesto / errato / soluzione
        r3 = ttk.Frame(filt)
        r3.pack(fill=tk.X, pady=2)
        ttk.Label(r3, text=L('inc_rep_filter_product', 'Codice prodotto (MPN):'), width=16).pack(side=tk.LEFT)
        self._v_mpn = tk.StringVar()
        ttk.Entry(r3, textvariable=self._v_mpn, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Label(r3, text=L('inc_rep_filter_wrong', 'MPN errato:'), width=12).pack(side=tk.LEFT, padx=(10, 0))
        self._v_wrong = tk.StringVar()
        ttk.Entry(r3, textvariable=self._v_wrong, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Label(r3, text=L('inc_rep_filter_answer', 'MPN soluzione:'), width=14).pack(side=tk.LEFT, padx=(10, 0))
        self._v_answer = tk.StringVar()
        ttk.Entry(r3, textvariable=self._v_answer, width=20).pack(side=tk.LEFT, padx=4)

        # Riga 4: pulsanti
        r4 = ttk.Frame(filt)
        r4.pack(fill=tk.X, pady=(6, 0))
        ttk.Button(r4, text=L('inc_rep_search', '🔍 Cerca'), command=self._search).pack(side=tk.LEFT, padx=4)
        self._btn_export = ttk.Button(r4, text=L('inc_rep_export', '⬇ Esporta Excel'),
                                      command=self._export_excel, state='disabled')
        self._btn_export.pack(side=tk.LEFT, padx=4)
        self._lbl_count = ttk.Label(r4, text='')
        self._lbl_count.pack(side=tk.RIGHT, padx=4)

        # ── Griglia risultati ──
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = [c[0] for c in self._COLUMNS]
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        headings = {
            'number': L('inc_col_number', 'Numero'),
            'type': L('inc_col_type', 'Tipo'),
            'supplier': L('inc_col_supplier', 'Fornitore'),
            'ddt': L('inc_col_ddt', 'DDT'),
            'ddt_date': L('inc_rep_col_ddt_date', 'Data DDT'),
            'po': L('inc_col_po', 'P.O.'),
            'mpn': L('inc_col_mpn', 'MPN'),
            'wrong_mpn': L('inc_rep_col_wrong_mpn', 'MPN errato'),
            'qty_receive': L('inc_rep_col_qty_receive', 'Q.tà da ricevere'),
            'qty_expected': L('inc_rep_col_qty_expected', 'Q.tà attesa P.O.'),
            'requested_by': L('inc_col_by', 'Richiesto da'),
            'requested_on': L('inc_rep_col_requested_on', 'Data richiesta'),
            'host': L('inc_rep_col_host', 'PC'),
            'status': L('inc_rep_col_status', 'Stato'),
            'answer_mpn': L('inc_rep_col_answer_mpn', 'MPN soluzione'),
            'answered_by': L('inc_rep_col_answered_by', 'Evasa da'),
            'answered_on': L('inc_rep_col_answered_on', 'Data evasione'),
            'elapsed': L('inc_rep_col_elapsed', 'Tempo trascorso'),
        }
        widths = {c[0]: (c[2], c[3]) for c in self._COLUMNS}
        for c in cols:
            self.tree.heading(c, text=headings[c], command=lambda col=c: self._sort_by(col))
            w, anc = widths[c]
            self.tree.column(c, width=w, anchor=anc)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(wrap, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        ttk.Button(self, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(
            side=tk.RIGHT, padx=10, pady=6)

    # ── Ricerca ───────────────────────────────────────────────────────────────
    def _parse_date(self, text):
        text = (text or '').strip()
        if not text:
            return None
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        return None

    def _current_filters(self):
        return {
            'date_from': self._parse_date(self._v_from.get()),
            'date_to': self._parse_date(self._v_to.get()),
            'request_type': self._type_key_by_label.get(self._v_type.get()),
            'supplier': self._v_supplier.get().strip() or None,
            'mpn_code': self._v_mpn.get().strip() or None,
            'wrong_mpn': self._v_wrong.get().strip() or None,
            'answer_mpn': self._v_answer.get().strip() or None,
            'status': self._status_labels.get(self._v_status.get(), ''),
        }

    def _search(self):
        L = self.lang.get
        try:
            self._rows = incoming_db.get_requests_report(self.db, self._current_filters()) or []
        except Exception as e:
            logger.error("Incoming report: ricerca fallita: %s", e, exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        # ripristina ordinamento corrente sul nuovo result set
        self._sort_rows()
        self._reload_tree()
        self._lbl_count.config(text=f"{len(self._rows)} {L('inc_sol_pending', 'richieste')}")
        self._btn_export.config(state='normal' if self._rows else 'disabled')

    # ── Ordinamento ───────────────────────────────────────────────────────────
    def _sort_key_for(self, col_id):
        for c in self._COLUMNS:
            if c[0] == col_id:
                return c[1]
        return col_id

    def _sort_value(self, row, key):
        if key == '_type_sort':
            return (row.get('RequestType') or '')
        if key == '_status_sort':
            return (row.get('Status') or '')
        if key == '_elapsed_sort':
            return elapsed_minutes(row)
        value = row.get(key)
        if value is None:
            return ''
        if key in ('DdtDate', 'RequestedOn', 'AnsweredOn'):
            dt = _as_datetime(value)
            return dt or ''
        if isinstance(value, str):
            return value.lower()
        return value

    def _sort_rows(self):
        key = self._sort_key_for(self._sort_col)

        def value(r):
            return self._sort_value(r, key)

        def is_empty(r):
            v = value(r)
            return v is None or v == ''

        # I valori vuoti (es. non evase senza data evasione/tempo) restano
        # sempre in fondo, in entrambe le direzioni di ordinamento.
        try:
            non_empty = sorted((r for r in self._rows if not is_empty(r)),
                               key=value, reverse=self._sort_desc)
        except TypeError:
            # valori eterogenei: ordina come stringa
            non_empty = sorted((r for r in self._rows if not is_empty(r)),
                               key=lambda r: str(value(r)),
                               reverse=self._sort_desc)
        self._rows = non_empty + [r for r in self._rows if is_empty(r)]

    def _sort_by(self, col_id):
        if self._sort_col == col_id:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col = col_id
            self._sort_desc = False
        self._sort_rows()
        self._reload_tree()

    def _reload_tree(self):
        L = self.lang.get
        self.tree.delete(*self.tree.get_children())
        for r in self._rows:
            self.tree.insert('', 'end', values=(
                r.get('RequestNumber') or '',
                incoming_db.type_label(L, r.get('RequestType')),
                r.get('SupplierName') or '',
                r.get('DdtNumber') or '',
                _fmt_dt(r.get('DdtDate'))[:10],
                r.get('PurOrderNumber') or '',
                r.get('MpnCode') or '',
                r.get('WrongMpn') or '',
                r.get('QtyToReceive') if r.get('QtyToReceive') is not None else '',
                r.get('QtyExpectedPerPo') if r.get('QtyExpectedPerPo') is not None else '',
                r.get('RequestedBy') or '',
                _fmt_dt(r.get('RequestedOn')),
                r.get('RequesterHost') or '',
                self._status_text(r.get('Status')),
                r.get('AnswerMpnCode') or '',
                r.get('AnsweredBy') or '',
                _fmt_dt(r.get('AnsweredOn')),
                _fmt_elapsed_minutes(elapsed_minutes(r)),
            ))

    def _status_text(self, status):
        L = self.lang.get
        return {
            incoming_db.STATUS_PENDING: L('inc_rep_status_pending', 'Non evase'),
            incoming_db.STATUS_ANSWERED: L('inc_rep_status_answered', 'Evase'),
            incoming_db.STATUS_CONFIRMED_OK: L('inc_rep_confirmed_ok', 'Confermata OK'),
            incoming_db.STATUS_CONFIRMED_KO: L('inc_rep_confirmed_ko', 'Confermata KO'),
        }.get(status, status or '')

    # ── Export Excel ──────────────────────────────────────────────────────────
    def _export_excel(self):
        L = self.lang.get
        if not self._rows:
            return
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment

            wb = Workbook()
            ws = wb.active
            ws.title = "Report Ricezione"

            headers = [self.tree.heading(c)['text'] for c in self.tree['columns']]

            # Titolo
            title_cell = ws.cell(row=1, column=1, value=L('inc_rep_title', 'Report Ricezione — situazione MPN'))
            title_cell.font = Font(bold=True, size=13)

            # Blocco filtri applicati
            filters = self._current_filters()
            filter_lines = [
                f"{L('inc_rep_filter_from', 'Da:')} {self._v_from.get() or '-'}   "
                f"{L('inc_rep_filter_to', 'A:')} {self._v_to.get() or '-'}",
                f"{L('inc_rep_filter_type', 'Tipo:')} {self._v_type.get()}   "
                f"{L('inc_rep_filter_supplier', 'Fornitore:')} {filters['supplier'] or '-'}   "
                f"{L('inc_rep_filter_status', 'Stato:')} {self._v_status.get()}",
                f"{L('inc_rep_filter_product', 'Codice prodotto (MPN):')} {filters['mpn_code'] or '-'}   "
                f"{L('inc_rep_filter_wrong', 'MPN errato:')} {filters['wrong_mpn'] or '-'}   "
                f"{L('inc_rep_filter_answer', 'MPN soluzione:')} {filters['answer_mpn'] or '-'}",
            ]
            for i, line in enumerate(filter_lines, start=2):
                ws.cell(row=i, column=1, value=line)

            header_row = 2 + len(filter_lines) + 1  # riga intestazioni dopo titolo+filtri+vuota

            # Riga intestazioni formattata
            header_fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=header_row, column=col_num, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Dati (stesso ordine visibile nella griglia)
            for row_num, r in enumerate(self._rows, header_row + 1):
                values = (
                    r.get('RequestNumber') or '',
                    incoming_db.type_label(L, r.get('RequestType')),
                    r.get('SupplierName') or '',
                    r.get('DdtNumber') or '',
                    _fmt_dt(r.get('DdtDate'))[:10],
                    r.get('PurOrderNumber') or '',
                    r.get('MpnCode') or '',
                    r.get('WrongMpn') or '',
                    r.get('QtyToReceive') if r.get('QtyToReceive') is not None else '',
                    r.get('QtyExpectedPerPo') if r.get('QtyExpectedPerPo') is not None else '',
                    r.get('RequestedBy') or '',
                    _fmt_dt(r.get('RequestedOn')),
                    r.get('RequesterHost') or '',
                    self._status_text(r.get('Status')),
                    r.get('AnswerMpnCode') or '',
                    r.get('AnsweredBy') or '',
                    _fmt_dt(r.get('AnsweredOn')),
                    _fmt_elapsed_minutes(elapsed_minutes(r)),
                )
                for col_num, value in enumerate(values, 1):
                    ws.cell(row=row_num, column=col_num, value=value)

            # Freeze pani sotto la riga intestazioni + auto larghezze
            ws.freeze_panes = ws.cell(row=header_row + 1, column=1)
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if cell.value is not None and len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except Exception:
                        pass
                ws.column_dimensions[column_letter].width = min(max(max_length + 2, 10), 55)

            # Salva ed apri
            temp_dir = r"C:\Temp"
            os.makedirs(temp_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(temp_dir, f"ReportRicezione_{timestamp}.xlsx")
            wb.save(filepath)

            if hasattr(os, "startfile"):
                os.startfile(filepath)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])

            messagebox.showinfo(
                L('success', 'Successo'),
                L('inc_rep_export_done', 'Report esportato con successo:\n{0}').format(filepath),
                parent=self)
        except Exception as e:
            logger.error("Incoming report: export Excel fallito: %s", e, exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"{L('inc_rep_export_error', 'Errore durante l''esportazione')}:\n{e}",
                                 parent=self)
