"""
indirect_materials_stats.py  –  Statistiche e rilevamento anomalie materiali indiretti
4 tab: Trend Mensile | YTD per Richiedente | Per Richiedente | Anomalie
"""
import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime, date, timedelta
import statistics

logger = logging.getLogger(__name__)

MONTHS_IT = ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic']

# ─────────────────────────────────────────────────────────────────────────────
class IndirectMaterialsStatsWindow(tk.Toplevel):

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db   = db
        self.lang = lang
        self.title(lang.get('ind_stats_title', 'Statistiche Materiali Indiretti'))
        self.geometry('1200x720')
        self.resizable(True, True)
        self.transient(master)
        self._build_ui()
        self._load_all()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    # ── helpers ──────────────────────────────────────────────────────────────
    def _fetch(self, sql, params=None):
        try:
            if hasattr(self.db, 'fetch_all'):
                return self.db.fetch_all(sql, params) or []
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(sql, params or [])
                return self.db.cursor.fetchall() or []
        except Exception as e:
            logger.error(f'[Stats] {e}', exc_info=True)
            return []

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        top = ttk.Frame(self, padding=6)
        top.pack(fill='x')

        ttk.Label(top, text=self.lang.get('ind_stats_year', 'Anno:'), font=('Segoe UI',9)).pack(side='left')
        self.year_var = tk.StringVar()
        self.year_cb  = ttk.Combobox(top, textvariable=self.year_var, width=8, state='readonly')
        self.year_cb.pack(side='left', padx=(2,12))
        self.year_cb.bind('<<ComboboxSelected>>', lambda e: self._load_all())

        ttk.Button(top, text=self.lang.get('btn_refresh','Aggiorna'), command=self._load_all).pack(side='left')

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both', expand=True, padx=6, pady=6)

        self._build_tab_trend()
        self._build_tab_ytd()
        self._build_tab_requester()
        self._build_tab_anomaly()

    def _tree(self, parent, cols, widths, anchors=None):
        f = ttk.Frame(parent)
        f.pack(fill='both', expand=True)
        tv = ttk.Treeview(f, columns=cols, show='headings')
        for i, c in enumerate(cols):
            tv.heading(c, text=c, command=lambda col=c, t=tv: self._sort(t, col))
            tv.column(c, width=widths[i], anchor=('e' if anchors and anchors[i]=='r' else 'w'))
        sb = ttk.Scrollbar(f, orient='vertical', command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        tv.pack(fill='both', expand=True)
        return tv

    def _sort(self, tv, col):
        data = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            data.sort(key=lambda x: float(x[0].replace('%','').replace(',','.')), reverse=True)
        except ValueError:
            data.sort()
        for i, (_, k) in enumerate(data):
            tv.move(k, '', i)

    # ── Tab 1 – Trend Mensile ─────────────────────────────────────────────
    def _build_tab_trend(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=self.lang.get('ind_stats_tab_trend','📈 Trend Mensile'))

        cols    = ('Tipo', 'Materiale') + tuple(MONTHS_IT) + ('Totale',)
        widths  = [110, 240] + [55]*12 + [70]
        anchors = ['w','w'] + ['r']*12 + ['r']
        self.trend_tree = self._tree(f, cols, widths, anchors)
        self.trend_tree.tag_configure('spike', background='#fff3cd')

        self.trend_lbl = tk.StringVar()
        ttk.Label(f, textvariable=self.trend_lbl, font=('Segoe UI',9,'italic')).pack(anchor='e', padx=6)

    def _load_trend(self, year):
        sql = """
            SELECT ISNULL(t.Tipo,'Generico') AS Tipo,
                   m.CodiceMateriale + ' - ' + m.DescrizioneMateriale AS Mat,
                   MONTH(r.DataRichiesta) AS Mese,
                   SUM(r.QtaRichiesta) AS Qty
            FROM ind.MaterialiRichieste r
            JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
            WHERE YEAR(r.DataRichiesta) = ?
            GROUP BY ISNULL(t.Tipo,'Generico'), m.CodiceMateriale, m.DescrizioneMateriale, MONTH(r.DataRichiesta)
            ORDER BY Tipo, Mat, Mese
        """
        rows = self._fetch(sql, [year])
        # pivot
        pivot = {}  # (tipo, mat) -> [0]*12
        for tipo, mat, mese, qty in rows:
            key = (tipo, mat)
            if key not in pivot:
                pivot[key] = [0.0]*12
            pivot[key][mese-1] += float(qty or 0)

        self.trend_tree.delete(*self.trend_tree.get_children())
        cur_month = date.today().month
        for (tipo, mat), vals in sorted(pivot.items()):
            tot  = sum(vals)
            avg  = statistics.mean(v for v in vals[:cur_month] if v > 0) if any(v>0 for v in vals[:cur_month]) else 0
            # spike = current month > 1.5x average of previous months
            spike = cur_month > 1 and avg > 0 and vals[cur_month-1] > avg * 1.5
            tag   = ('spike',) if spike else ()
            fmts  = [f'{v:.0f}' if v else '' for v in vals]
            self.trend_tree.insert('', 'end',
                values=(tipo, mat) + tuple(fmts) + (f'{tot:.0f}',), tags=tag)
        self.trend_lbl.set(f'{len(pivot)} materiali • Anno {year} • Giallo = spike >150% media')

    # ── Tab 2 – YTD per Richiedente ───────────────────────────────────────
    def _build_tab_ytd(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=self.lang.get('ind_stats_tab_ytd','📊 YTD Richiedenti'))

        cols    = ('Richiedente','# Richieste','Qty Totale','Qty Media/Rich.','# Materiali Diversi','% Consegnato')
        widths  = [160, 100, 100, 120, 140, 110]
        anchors = ['w','r','r','r','r','r']
        self.ytd_tree = self._tree(f, cols, widths, anchors)
        self.ytd_tree.tag_configure('top', background='#d4edda')

        self.ytd_lbl = tk.StringVar()
        ttk.Label(f, textvariable=self.ytd_lbl, font=('Segoe UI',9,'italic')).pack(anchor='e', padx=6)

    def _load_ytd(self, year):
        sql = """
            SELECT r.RichiestoDa,
                   COUNT(*) AS NReq,
                   SUM(r.QtaRichiesta) AS QtyTot,
                   COUNT(DISTINCT r.MaterialeId) AS NMat,
                   SUM(CASE WHEN r.Stato='CONSEGNATA' THEN 1 ELSE 0 END) AS NDel
            FROM ind.MaterialiRichieste r
            WHERE YEAR(r.DataRichiesta) = ?
            GROUP BY r.RichiestoDa
            ORDER BY QtyTot DESC
        """
        rows = self._fetch(sql, [year])
        self.ytd_tree.delete(*self.ytd_tree.get_children())
        if not rows:
            return
        max_qty = float(rows[0][2] or 0)
        for i, (req, n, qty, nmat, ndel) in enumerate(rows):
            qty   = float(qty or 0)
            pct   = f'{ndel/n*100:.0f}%' if n else '0%'
            avg   = f'{qty/n:.1f}' if n else '0'
            tag   = ('top',) if i < 3 else ()
            self.ytd_tree.insert('', 'end',
                values=(req or '?', n, f'{qty:.0f}', avg, nmat, pct), tags=tag)
        self.ytd_lbl.set(f'{len(rows)} richiedenti • YTD {year} • Verde = Top 3 per volume')

    # ── Tab 3 – Per Richiedente (drill-down) ─────────────────────────────
    def _build_tab_requester(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=self.lang.get('ind_stats_tab_req','👤 Dettaglio Richiedente'))

        top = ttk.Frame(f)
        top.pack(fill='x', pady=4, padx=6)
        ttk.Label(top, text=self.lang.get('ind_stats_select_req','Richiedente:')).pack(side='left')
        self.req_var = tk.StringVar()
        self.req_cb  = ttk.Combobox(top, textvariable=self.req_var, width=30, state='readonly')
        self.req_cb.pack(side='left', padx=4)
        self.req_cb.bind('<<ComboboxSelected>>', lambda e: self._load_requester_detail())

        cols    = ('Materiale','Tipo','# Richieste','Qty Totale','Qty Media','Gg Medi tra Req.','Prima','Ultima')
        widths  = [240, 100, 90, 90, 90, 120, 100, 100]
        anchors = ['w','w','r','r','r','r','w','w']
        self.req_tree = self._tree(f, cols, widths, anchors)
        self.req_lbl  = tk.StringVar()
        ttk.Label(f, textvariable=self.req_lbl, font=('Segoe UI',9,'italic')).pack(anchor='e', padx=6)

    def _load_requester_detail(self):
        req  = self.req_var.get()
        year = self.year_var.get() or str(date.today().year)
        if not req:
            return
        sql = """
            SELECT m.CodiceMateriale + ' - ' + m.DescrizioneMateriale AS Mat,
                   ISNULL(t.Tipo,'Generico') AS Tipo,
                   COUNT(*) AS NReq,
                   SUM(r.QtaRichiesta) AS QtyTot,
                   AVG(r.QtaRichiesta) AS QtyAvg,
                   MIN(r.DataRichiesta) AS Prima,
                   MAX(r.DataRichiesta) AS Ultima
            FROM ind.MaterialiRichieste r
            JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
            WHERE r.RichiestoDa = ? AND YEAR(r.DataRichiesta) = ?
            GROUP BY m.CodiceMateriale, m.DescrizioneMateriale, t.Tipo
            ORDER BY QtyTot DESC
        """
        rows = self._fetch(sql, [req, int(year)])
        self.req_tree.delete(*self.req_tree.get_children())
        for mat, tipo, n, qtot, qavg, prima, ultima in rows:
            if prima and ultima and n > 1:
                span = (ultima - prima).days
                avg_days = f'{span/(n-1):.0f}' if n > 1 else '—'
            else:
                avg_days = '—'
            self.req_tree.insert('', 'end', values=(
                mat, tipo, n,
                f'{float(qtot or 0):.0f}',
                f'{float(qavg or 0):.1f}',
                avg_days,
                prima.strftime('%d/%m/%Y') if prima else '',
                ultima.strftime('%d/%m/%Y') if ultima else ''
            ))
        self.req_lbl.set(f'{req} • {len(rows)} materiali diversi • Anno {year}')

    # ── Tab 4 – Anomalie ─────────────────────────────────────────────────
    def _build_tab_anomaly(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=self.lang.get('ind_stats_tab_anomaly','⚠️ Anomalie'))

        info = ttk.Label(f, text=(
            '4 regole: [QTY] qty > media+2σ  |  [FREQ] stesso mat. >1 volta in 7gg  |  '
            '[SPIKE] mese corrente >150% media ultimi 6 mesi  |  [NEW] prima richiesta per quel materiale'
        ), font=('Segoe UI', 8), foreground='#555', wraplength=1100, justify='left')
        info.pack(fill='x', padx=8, pady=(6,2))

        cols   = ('Severità','Regola','Richiedente','Materiale','Data','Qty','Nota')
        widths = [80, 70, 140, 260, 110, 70, 300]
        self.anom_tree = self._tree(f, cols, widths)
        self.anom_tree.tag_configure('HIGH', background='#f8d7da')
        self.anom_tree.tag_configure('MED',  background='#fff3cd')
        self.anom_tree.tag_configure('INFO', background='#d1ecf1')

        self.anom_lbl = tk.StringVar()
        ttk.Label(f, textvariable=self.anom_lbl, font=('Segoe UI',9,'italic')).pack(anchor='e', padx=6)

    def _load_anomaly(self, year):
        anomalies = []

        # ── Regola 1 & 4: stats per materiale ────────────────────────────
        sql_hist = """
            SELECT r.MaterialeId,
                   m.CodiceMateriale + ' - ' + m.DescrizioneMateriale AS Mat,
                   r.RichiestoDa, r.DataRichiesta, r.QtaRichiesta
            FROM ind.MaterialiRichieste r
            JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            WHERE YEAR(r.DataRichiesta) = ?
            ORDER BY r.MaterialeId, r.DataRichiesta
        """
        rows = self._fetch(sql_hist, [year])

        # group by material
        from collections import defaultdict
        mat_rows   = defaultdict(list)   # mid -> [(req, date, qty)]
        mat_labels = {}
        for mid, mat, req, dt, qty in rows:
            mat_rows[mid].append((req, dt, float(qty or 0)))
            mat_labels[mid] = mat

        for mid, recs in mat_rows.items():
            qtys = [r[2] for r in recs]
            mean = statistics.mean(qtys) if qtys else 0
            std  = statistics.stdev(qtys) if len(qtys) > 1 else 0
            seen_requesters = set()
            for i, (req, dt, qty) in enumerate(recs):
                # Regola 1 – qty outlier
                if std > 0 and qty > mean + 2*std:
                    anomalies.append(('HIGH','QTY', req, mat_labels[mid], dt, qty,
                        f'Qty {qty:.0f} > media {mean:.0f} + 2σ ({std:.0f})'))
                # Regola 4 – first request
                if req not in seen_requesters:
                    seen_requesters.add(req)
                    if i > 0:  # not the very first ever
                        anomalies.append(('INFO','NEW', req, mat_labels[mid], dt, qty,
                            'Prima richiesta per questo materiale da questo richiedente'))

        # ── Regola 2 – frequenza: stesso mat stesso richiedente entro 7gg ─
        for mid, recs in mat_rows.items():
            req_dates = defaultdict(list)
            for req, dt, qty in recs:
                req_dates[req].append(dt)
            for req, dates in req_dates.items():
                sdates = sorted(d for d in dates if d)
                for j in range(1, len(sdates)):
                    gap = (sdates[j] - sdates[j-1]).days if sdates[j] and sdates[j-1] else 999
                    if gap <= 7:
                        anomalies.append(('MED','FREQ', req, mat_labels[mid], sdates[j], 0,
                            f'Richiesta ripetuta dopo soli {gap} giorni'))

        # ── Regola 3 – spike mensile (ultimi 6 mesi vs mese corrente) ────
        sql_monthly = """
            SELECT ISNULL(t.Tipo,'Generico') AS Tipo,
                   MONTH(r.DataRichiesta) AS M,
                   SUM(r.QtaRichiesta) AS Qty
            FROM ind.MaterialiRichieste r
            LEFT JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
            LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
            WHERE YEAR(r.DataRichiesta) = ?
            GROUP BY ISNULL(t.Tipo,'Generico'), MONTH(r.DataRichiesta)
        """
        mrows = self._fetch(sql_monthly, [year])
        tipo_monthly = defaultdict(lambda: [0.0]*12)
        for tipo, m, qty in mrows:
            tipo_monthly[tipo][m-1] = float(qty or 0)
        cur_m = date.today().month
        for tipo, vals in tipo_monthly.items():
            hist = [vals[i] for i in range(max(0, cur_m-7), cur_m-1) if vals[i] > 0]
            if hist and cur_m >= 2:
                avg6 = statistics.mean(hist)
                if avg6 > 0 and vals[cur_m-1] > avg6 * 1.5:
                    anomalies.append(('MED','SPIKE', '—', f'Tipo: {tipo}',
                        date(year, cur_m, 1), vals[cur_m-1],
                        f'Qty {vals[cur_m-1]:.0f} vs media6m {avg6:.0f} (+{(vals[cur_m-1]/avg6-1)*100:.0f}%)'))

        # populate treeview
        self.anom_tree.delete(*self.anom_tree.get_children())
        order = {'HIGH': 0, 'MED': 1, 'INFO': 2}
        anomalies.sort(key=lambda x: order.get(x[0], 9))
        for sev, rule, req, mat, dt, qty, note in anomalies:
            dt_str = dt.strftime('%d/%m/%Y') if hasattr(dt, 'strftime') else str(dt)
            self.anom_tree.insert('', 'end',
                values=(sev, rule, req, mat, dt_str, f'{qty:.0f}' if qty else '—', note),
                tags=(sev,))
        high = sum(1 for a in anomalies if a[0]=='HIGH')
        med  = sum(1 for a in anomalies if a[0]=='MED')
        info = sum(1 for a in anomalies if a[0]=='INFO')
        self.anom_lbl.set(
            f'{len(anomalies)} anomalie: {high} critiche (rosso) | {med} medie (giallo) | {info} informative (azzurro)')

    # ── Load all ──────────────────────────────────────────────────────────
    def _load_all(self):
        # populate years on first call
        if not self.year_cb['values']:
            rows = self._fetch("SELECT DISTINCT YEAR(DataRichiesta) FROM ind.MaterialiRichieste ORDER BY 1 DESC")
            years = [str(r[0]) for r in rows] or [str(date.today().year)]
            self.year_cb['values'] = years
            self.year_var.set(years[0])

        # populate requesters for tab 3
        year = int(self.year_var.get() or date.today().year)
        rows = self._fetch(
            "SELECT DISTINCT RichiestoDa FROM ind.MaterialiRichieste WHERE YEAR(DataRichiesta)=? ORDER BY 1",
            [year])
        self.req_cb['values'] = [r[0] for r in rows if r[0]]

        self._load_trend(year)
        self._load_ytd(year)
        self._load_anomaly(year)
        if self.req_var.get():
            self._load_requester_detail()


# ── entry-point ───────────────────────────────────────────────────────────────
def open_indirect_materials_stats(master, db, lang):
    IndirectMaterialsStatsWindow(master, db, lang)
