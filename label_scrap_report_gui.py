# -*- coding: utf-8 -*-
"""
label_scrap_report_gui.py — Report scarti etichette.

Form con filtri data da/a e operatore; genera Excel e PDF (con logo) del dettaglio
e dei riepiloghi (per motivo, categoria, operatore). Legge traceability_rs.dbo.labelscrap.
"""
import os
import logging
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

logger = logging.getLogger(__name__)


def open_label_scrap_report(parent, db, lang):
    LabelScrapReportWindow(parent, db, lang)


class LabelScrapReportWindow(tk.Toplevel):
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        L = self.lang.get
        self.title(L('lsr_title', 'Report Scarti Etichette'))
        self.geometry('960x600')
        self.transient(parent)
        self._rows = []
        self._build()
        self._load_operators()
        self._generate()

    def _build(self):
        L = self.lang.get
        flt = ttk.LabelFrame(self, text=L('filters', 'Filtri'), padding=8)
        flt.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(flt, text=L('lsr_from', 'Da') + ':').pack(side=tk.LEFT, padx=(0, 4))
        if DateEntry:
            self.d_from = DateEntry(flt, width=12, date_pattern='dd/mm/yyyy', locale='it_IT')
            self.d_from.set_date(datetime.now() - timedelta(days=30))
        else:
            self.d_from = ttk.Entry(flt, width=12)
            self.d_from.insert(0, (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y'))
        self.d_from.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Label(flt, text=L('lsr_to', 'A') + ':').pack(side=tk.LEFT, padx=(0, 4))
        if DateEntry:
            self.d_to = DateEntry(flt, width=12, date_pattern='dd/mm/yyyy', locale='it_IT')
        else:
            self.d_to = ttk.Entry(flt, width=12)
            self.d_to.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.d_to.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Label(flt, text=L('lsc_operator', 'Operatore') + ':').pack(side=tk.LEFT, padx=(0, 4))
        self.op_combo = ttk.Combobox(flt, width=24, state='readonly')
        self.op_combo.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(flt, text=L('lsr_generate', 'Genera'), command=self._generate).pack(side=tk.LEFT, padx=4)
        ttk.Button(flt, text=L('lsr_excel', '📊 Excel'), command=self._export_excel).pack(side=tk.LEFT, padx=4)
        ttk.Button(flt, text=L('lsr_pdf', '📄 PDF'), command=self._export_pdf).pack(side=tk.LEFT, padx=4)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('date', 'operator', 'label', 'reason', 'category', 'shift')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, t, w, a in (('date', L('lsc_date', 'Data'), 100, 'center'),
                           ('operator', L('lsc_operator', 'Operatore'), 180, 'w'),
                           ('label', L('lsc_scan', 'Etichetta'), 200, 'w'),
                           ('reason', L('lsc_reason', 'Motivo'), 220, 'w'),
                           ('category', L('lsc_category', 'Categoria'), 100, 'center'),
                           ('shift', L('lsc_shift', 'Turno'), 70, 'center')):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        self.count_lbl = ttk.Label(self, text='', foreground='#555')
        self.count_lbl.pack(anchor='w', padx=12, pady=(0, 8))

    def _load_operators(self):
        vals = [self.lang.get('all_operators', 'Tutti')]
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT DISTINCT Operator FROM traceability_rs.dbo.labelscrap ORDER BY Operator")
            vals.extend([r.Operator for r in cur.fetchall() if r.Operator])
            cur.close()
        except Exception as e:
            logger.error(f"Load operators: {e}")
        self.op_combo['values'] = vals
        self.op_combo.current(0)

    def _dates(self):
        def gd(w):
            if DateEntry and hasattr(w, 'get_date'):
                return w.get_date()
            return datetime.strptime(w.get().strip(), '%d/%m/%Y').date()
        return gd(self.d_from), gd(self.d_to)

    def _operator(self):
        op = self.op_combo.get()
        return None if op == self.lang.get('all_operators', 'Tutti') else op

    def _generate(self):
        L = self.lang.get
        try:
            df, dt = self._dates()
        except Exception:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('lsr_bad_dates', 'Date non valide.'), parent=self)
            return
        op = self._operator()
        sql = """
            SELECT ls.ScrapDate, ls.Operator, ls.LabelCode, r.Reason, ls.Category, ls.Shift
            FROM traceability_rs.dbo.labelscrap ls
            INNER JOIN traceability_rs.dbo.LabelScrapReasons r
                ON r.LabelScrapReasonId = ls.LabelScrapReasonId
            WHERE ls.ScrapDate BETWEEN ? AND ?
        """
        params = [df, dt]
        if op:
            sql += " AND ls.Operator = ?"
            params.append(op)
        sql += " ORDER BY ls.ScrapDate, ls.Operator"
        try:
            cur = self.db.conn.cursor()
            cur.execute(sql, params)
            self._rows = [(r.ScrapDate, r.Operator, r.LabelCode, r.Reason, r.Category, r.Shift)
                          for r in cur.fetchall()]
            cur.close()
        except Exception as e:
            logger.error(f"Genera report: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self.tree.delete(*self.tree.get_children())
        for r in self._rows:
            d = r[0].strftime('%d/%m/%Y') if hasattr(r[0], 'strftime') else str(r[0])
            self.tree.insert('', 'end', values=(d, r[1], r[2], r[3], r[4], r[5] or ''))
        self.count_lbl.config(text=L('lsr_count', '{0} scarti nel periodo').format(len(self._rows)))

    def _aggregates(self):
        from collections import Counter
        by_reason = Counter(r[3] for r in self._rows).most_common()
        by_category = Counter(r[4] for r in self._rows).most_common()
        by_operator = Counter(r[1] for r in self._rows).most_common()
        return by_reason, by_category, by_operator

    def _export_excel(self):
        L = self.lang.get
        if not self._rows:
            messagebox.showinfo(L('info', 'Info'), L('lsr_no_data', 'Nessun dato da esportare.'), parent=self)
            return
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        except ImportError:
            messagebox.showerror(L('error', 'Errore'), 'openpyxl non disponibile', parent=self)
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Scarti Etichette'
        H_FILL = PatternFill('solid', fgColor='1F3864')
        H_FONT = Font(bold=True, color='FFFFFF')
        THIN = Border(*(Side(style='thin'),) * 4)
        headers = ['Data', 'Operatore', 'Etichetta', 'Motivo', 'Categoria', 'Turno']
        for c, h in enumerate(headers, 1):
            cell = ws.cell(1, c, h)
            cell.fill, cell.font, cell.alignment, cell.border = H_FILL, H_FONT, Alignment(horizontal='center'), THIN
        for ri, r in enumerate(self._rows, 2):
            d = r[0].strftime('%d/%m/%Y') if hasattr(r[0], 'strftime') else str(r[0])
            for ci, v in enumerate((d, r[1], r[2], r[3], r[4], r[5] or ''), 1):
                ws.cell(ri, ci, v).border = THIN
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = f'A1:F{len(self._rows) + 1}'
        for col in ws.columns:
            w = max((len(str(c.value or '')) for c in col), default=8)
            ws.column_dimensions[col[0].column_letter].width = min(w + 3, 50)

        # foglio riepiloghi
        by_reason, by_category, by_operator = self._aggregates()
        ws2 = wb.create_sheet('Riepiloghi')
        r0 = 1
        for title, items in (('Per motivo', by_reason), ('Per categoria', by_category),
                             ('Per operatore', by_operator)):
            ws2.cell(r0, 1, title).font = Font(bold=True, size=12, color='1F3864')
            r0 += 1
            for lbl, cnt in items:
                ws2.cell(r0, 1, lbl)
                ws2.cell(r0, 2, cnt)
                r0 += 1
            r0 += 1
        for col in ws2.columns:
            w = max((len(str(c.value or '')) for c in col), default=8)
            ws2.column_dimensions[col[0].column_letter].width = min(w + 3, 50)

        temp_dir = r'c:\Temp'
        os.makedirs(temp_dir, exist_ok=True)
        path = os.path.join(temp_dir, f"ScartiEtichette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        wb.save(path)
        self._offer_open(path)

    def _export_pdf(self):
        L = self.lang.get
        if not self._rows:
            messagebox.showinfo(L('info', 'Info'), L('lsr_no_data', 'Nessun dato da esportare.'), parent=self)
            return
        try:
            import label_scrap_pdf
            df, dt = self._dates()
            by_reason, by_category, by_operator = self._aggregates()
            wr = label_scrap_pdf.get_warehouse_responsible(self.db.conn)
            temp_dir = r'c:\Temp'
            os.makedirs(temp_dir, exist_ok=True)
            path = os.path.join(temp_dir, f"ScartiEtichette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            label_scrap_pdf.generate_report_pdf(path, df, dt, self._operator(), self._rows,
                                                by_reason, by_category, by_operator,
                                                warehouse_responsible=wr)
            self._offer_open(path)
        except Exception as e:
            logger.error(f"Export PDF: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)

    def _offer_open(self, path):
        L = self.lang.get
        if messagebox.askyesno(L('success', 'Successo'),
                               f"{L('file_saved', 'File salvato in')}: {path}\n\n{L('open_file_question', 'Aprire il file?')}",
                               parent=self):
            try:
                os.startfile(path)
            except Exception as e:
                messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
