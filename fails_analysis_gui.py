import tkinter as tk
from tkinter import ttk, messagebox
import threading, datetime, os, logging
import pyodbc
from collections import Counter

logger = logging.getLogger("TraceabilityRS")

QUERY_MAIN = """
declare @from datetime=?
declare @to datetime=?
select distinct Orders.OrderNumber,Products.ProductCode,Orders.OrderQuantity,Phases.PhaseName,
Boards.IDBoard,dbo.BoardLabels(Boards.IDBoard) as Labels,
iif(LastScan.IsPass=0,'FAIL','PASS') as ScanResult,LastScan.ScanTimeFinish as ScanTime,
iif(ScanDefects.IsPass is null,null,iif(ScanDefects.IsPass=0,'SCRAP','REPAIRED')) as RepairResult,
Defects.DefectNameRO,Riferiments.CodRiferimento as CodRiferimentoDefect
from (select Scannings.* from Scannings inner join boards on Boards.IDBoard=Scannings.IDBoard
where ScanTimeFinish between @from and @to) A
cross apply (select top 1 * from Scannings s where s.IDBoard=A.IDBoard order by s.IDScan desc) LastScan
inner join boards on Boards.IDBoard=LastScan.IDBoard
inner join Orders on Orders.IDOrder=boards.IDOrder
inner join Products on products.IDProduct=Orders.IDProduct
inner join OrderPhases on LastScan.IDOrderPhase=OrderPhases.IDOrderPhase
inner join Phases on Phases.IDPhase=OrderPhases.IDPhase
left join ScanDefects on ScanDefects.IDScan=LastScan.IDScan
left join ScanDefectDetails on ScanDefectDetails.IDScanDefect=ScanDefects.IDScanDefect
left join Defects on Defects.IDDefect=ScanDefectDetails.IDDefect
left join DefectsRiferiments on DefectsRiferiments.IDScanDefectDet=ScanDefectDetails.IDScanDefectDet
left join Riferiments on Riferiments.IDDibaRiferimento=DefectsRiferiments.IDDibaRiferimento
where LastScan.IsPass=0 and ScanDefects.IsPass is null
order by Orders.OrderNumber,Products.ProductCode,Boards.IDBoard
"""

QUERY_TODAY = """
select distinct Boards.IDBoard
from (select Scannings.* from Scannings inner join boards on Boards.IDBoard=Scannings.IDBoard
where ScanTimeFinish between ? and ?) A
cross apply (select top 1 * from Scannings s where s.IDBoard=A.IDBoard order by s.IDScan desc) LastScan
inner join boards on Boards.IDBoard=LastScan.IDBoard
left join ScanDefects on ScanDefects.IDScan=LastScan.IDScan
where LastScan.IsPass=0 and ScanDefects.IsPass is null
"""

TB = "SELECT COUNT(*) FROM [Traceability_RS].[fls].[FailsAnalysisCache] WHERE QueryFrom=? AND QueryTo=?"
DEL_CACHE = "DELETE FROM [Traceability_RS].[fls].[FailsAnalysisCache] WHERE QueryFrom=? AND QueryTo=?"
INS_CACHE = """INSERT INTO [Traceability_RS].[fls].[FailsAnalysisCache]
(IDBoard,LabelCode,OrderNumber,ProductCode,OrderQuantity,PhaseName,Labels,ScanResult,ScanTime,
RepairResult,DefectNameRO,CodRiferimento,QueryFrom,QueryTo)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
SEL_CACHE = """SELECT IDBoard,LabelCode,OrderNumber,ProductCode,OrderQuantity,PhaseName,Labels,
ScanResult,ScanTime,RepairResult,DefectNameRO,CodRiferimento,ResolvedAt
FROM [Traceability_RS].[fls].[FailsAnalysisCache]
WHERE QueryFrom=? AND QueryTo=? ORDER BY OrderNumber,ProductCode,IDBoard"""
SEL_UNRESOLVED = "SELECT DISTINCT IDBoard FROM [Traceability_RS].[fls].[FailsAnalysisCache] WHERE QueryFrom=? AND QueryTo=? AND ResolvedAt IS NULL"
UPD_RESOLVED = "UPDATE [Traceability_RS].[fls].[FailsAnalysisCache] SET ResolvedAt=? WHERE IDBoard=? AND QueryFrom=? AND QueryTo=? AND ResolvedAt IS NULL"
DEL_REPAIRS = "DELETE FROM [Traceability_RS].[fls].[RepairsAnalysisCache]"
INS_REPAIRS = (
    "INSERT INTO [Traceability_RS].[fls].[RepairsAnalysisCache] "
    "(IDBoard,Labels,ProductCode,OrderNumber,PhaseName,ResultRepair,DateRepair,"
    "CodRiferimento,Defect,QueryFrom,QueryTo) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
)
SEL_REPAIRS = (
    "SELECT Labels,ResultRepair,DateRepair "
    "FROM [Traceability_RS].[fls].[RepairsAnalysisCache] "
    "WHERE QueryFrom=? AND QueryTo=? ORDER BY Labels,DateRepair"
)
UPD_RESOLVED_AS = (
    "UPDATE [Traceability_RS].[fls].[FailsAnalysisCache] "
    "SET ResolvedAt=?, ResolvedAs=? "
    "WHERE LabelCode=? AND QueryFrom=? AND QueryTo=? AND ResolvedAt IS NULL"
)
SEL_CACHE_FULL = (
    "SELECT IDBoard,LabelCode,OrderNumber,ProductCode,OrderQuantity,PhaseName,Labels,"
    "ScanResult,ScanTime,RepairResult,DefectNameRO,CodRiferimento,ResolvedAt,ResolvedAs "
    "FROM [Traceability_RS].[fls].[FailsAnalysisCache] "
    "WHERE QueryFrom=? AND QueryTo=? ORDER BY OrderNumber,ProductCode,IDBoard"
)

SEL_CACHE_DATES = (
    "SELECT MIN(QueryFrom), MAX(QueryTo), COUNT(*) "
    "FROM [Traceability_RS].[fls].[FailsAnalysisCache]"
)
UPD_CACHE_QUERY_TO = (
    "UPDATE [Traceability_RS].[fls].[FailsAnalysisCache] "
    "SET QueryTo=? WHERE QueryFrom=? AND QueryTo=?"
)
UPD_REPAIRS_QUERY_TO = (
    "UPDATE [Traceability_RS].[fls].[RepairsAnalysisCache] "
    "SET QueryTo=? WHERE QueryFrom=? AND QueryTo=?"
)

SEL_SCRAP_FROM_REPAIRS = (
    "SELECT IDBoard,Labels,ProductCode,OrderNumber,PhaseName,ResultRepair,DateRepair,Defect,CodRiferimento "
    "FROM [Traceability_RS].[fls].[RepairsAnalysisCache] "
    "WHERE ResultRepair='SCRAP' ORDER BY DateRepair"
)
SEL_REPAIRED_FROM_REPAIRS = (
    "SELECT IDBoard,Labels,ProductCode,OrderNumber,PhaseName,ResultRepair,DateRepair,Defect,CodRiferimento "
    "FROM [Traceability_RS].[fls].[RepairsAnalysisCache] "
    "WHERE ResultRepair='REPAIRED' ORDER BY DateRepair"
)

QUERY_REPAIRS = (
    "DECLARE @from datetime=? "
    "DECLARE @to   datetime=? "
    "SELECT D.IDBoard,D.Labels,D.ProductCode,D.OrderProduction,D.PhaseName,"
    "       D.ResultRepair,D.DateRepair,D.CodRiferimento,D.Defect "
    "FROM ("
    "    SELECT Products.ProductCode,Orders.OrderProduction,Phases.PhaseName,"
    "        dbo.Boards.IDBoard,"
    "        dbo.BoardLabels(Boards.IDBoard) AS Labels,"
    "        CASE WHEN ScanDefects.IsPass=1 THEN 'REPAIRED' ELSE 'SCRAP' END AS ResultRepair,"
    "        ScanDefects.StopTime AS DateRepair,"
    "        Riferiments.CodRiferimento,"
    "        Defects.DefectNameRO AS Defect"
    "    FROM ScanDefects"
    "    INNER JOIN ScanDefectDetails ON ScanDefects.IDScanDefect=ScanDefectDetails.IDScanDefect"
    "    INNER JOIN DefectsRiferiments ON DefectsRiferiments.IDScanDefectDet=ScanDefectDetails.IDScanDefectDet"
    "    INNER JOIN Riferiments ON Riferiments.IDDibaRiferimento=DefectsRiferiments.IDDibaRiferimento"
    "    INNER JOIN Defects ON ScanDefectDetails.IDDefect=Defects.IDDefect"
    "    INNER JOIN Scannings ON Scannings.IDScan=ScanDefects.IDScan"
    "    INNER JOIN OrderPhases ON OrderPhases.IDOrderPhase=Scannings.IDOrderPhase"
    "    INNER JOIN Orders ON OrderPhases.IDOrder=Orders.IDOrder"
    "    INNER JOIN Products ON Products.IDProduct=Orders.IDProduct"
    "    INNER JOIN Phases ON OrderPhases.IDPhase=Phases.IDPhase"
    "    INNER JOIN Boards ON Scannings.IDBoard=Boards.IDBoard"
    "    WHERE ScanDefects.StopTime BETWEEN @from AND @to"
    ") D"
)

# ALTER TABLE statements — eseguiti automaticamente se le colonne sono ancora piccole
ALTER_STMTS = [
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [LabelCode]      NVARCHAR(1000) NOT NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [OrderNumber]    NVARCHAR(200)  NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [ProductCode]    NVARCHAR(200)  NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [PhaseName]      NVARCHAR(400)  NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [Labels]         NVARCHAR(2000) NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [ScanResult]     NVARCHAR(20)   NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [RepairResult]   NVARCHAR(40)   NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [DefectNameRO]   NVARCHAR(1000) NULL",
    "ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] ALTER COLUMN [CodRiferimento] NVARCHAR(500)  NULL",
    # Aggiunge ResolvedAs se mancante
    ("IF NOT EXISTS(SELECT 1 FROM sys.columns c "
     "INNER JOIN sys.tables t ON t.object_id=c.object_id "
     "INNER JOIN sys.schemas s ON s.schema_id=t.schema_id "
     "WHERE s.name='fls' AND t.name='FailsAnalysisCache' AND c.name='ResolvedAs') "
     "BEGIN ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] "
     "ADD [ResolvedAs] NVARCHAR(20) NULL END"),
    # Crea RepairsAnalysisCache se mancante
    ("IF NOT EXISTS(SELECT 1 FROM sys.tables t "
     "INNER JOIN sys.schemas s ON s.schema_id=t.schema_id "
     "WHERE t.name='RepairsAnalysisCache' AND s.name='fls') "
     "BEGIN CREATE TABLE [Traceability_RS].[fls].[RepairsAnalysisCache]("
     "[ID] INT IDENTITY PRIMARY KEY,"
     "[IDBoard] INT NULL,[Labels] NVARCHAR(2000) NOT NULL,"
     "[ProductCode] NVARCHAR(200) NULL,[OrderNumber] NVARCHAR(200) NULL,"
     "[PhaseName] NVARCHAR(400) NULL,[ResultRepair] NVARCHAR(20) NULL,"
     "[DateRepair] DATETIME NULL,[CodRiferimento] NVARCHAR(500) NULL,"
     "[Defect] NVARCHAR(1000) NULL,[QueryFrom] DATETIME NOT NULL,"
     "[QueryTo] DATETIME NOT NULL,[CachedAt] DATETIME DEFAULT GETDATE()) END"),
]


def _trunc(val, max_len):
    """Tronca una stringa a max_len caratteri per evitare 22001 truncation errors."""
    if val is None:
        return None
    s = str(val)
    return s[:max_len] if len(s) > max_len else s

class FailsAnalysisWindow(tk.Toplevel):
    def __init__(self, parent, db, lang, user_name=''):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.title(lang.get('fa_title', 'Analisi Schede FAIL'))
        self.geometry('1280x760')
        self.minsize(900, 600)
        self._data = []
        self._repaired = []
        self._scrap = []
        self._loading = False
        self.filter_active_var = tk.BooleanVar(value=True)  # Filtro FAIL attivi
        self._dt_from = None
        self._dt_to = None
        self._build_ui()
        self.grab_set()
        # Avvia auto-refresh in background se la cache ha dati precedenti
        self.after(200, self._auto_refresh_if_needed)

    # ------------------------------------------------------------------
    def _build_ui(self):
        hdr = tk.Frame(self, bg='#1F3864', padx=10, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=self.lang.get('fa_title', 'Analisi Schede FAIL'),
                 bg='#1F3864', fg='white', font=('Segoe UI', 13, 'bold')).pack(side=tk.LEFT)

        bar = tk.Frame(self, padx=8, pady=6, bg='#F0F0F0')
        bar.pack(fill=tk.X)
        tk.Label(bar, text=self.lang.get('fa_date_from', 'Da:'), bg='#F0F0F0').pack(side=tk.LEFT)
        self.from_var = tk.StringVar(value='2026-01-01')
        tk.Entry(bar, textvariable=self.from_var, width=12).pack(side=tk.LEFT, padx=4)
        tk.Label(bar, text=self.lang.get('fa_date_to', 'A:'), bg='#F0F0F0').pack(side=tk.LEFT)
        self.to_var = tk.StringVar(value=datetime.date.today().strftime('%Y-%m-%d'))
        tk.Entry(bar, textvariable=self.to_var, width=12).pack(side=tk.LEFT, padx=4)

        btn_style = dict(font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        self.load_btn = tk.Button(bar, text=self.lang.get('fa_load_btn', '🔄 Carica / Aggiorna'),
                                  command=self._on_load, bg='#2E75B6', fg='white', **btn_style)
        self.load_btn.pack(side=tk.LEFT, padx=10)
        self.export_btn = tk.Button(bar, text=self.lang.get('fa_export_btn', '📊 Esporta Excel'),
                                    command=self._export_excel, bg='#217346', fg='white',
                                    state=tk.DISABLED, **btn_style)
        self.export_btn.pack(side=tk.LEFT)
        self.status_var = tk.StringVar()
        tk.Label(bar, textvariable=self.status_var, bg='#F0F0F0', fg='#444',
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=14)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        tab_raw = tk.Frame(self.nb)
        self.nb.add(tab_raw, text=self.lang.get('fa_tab_raw', 'Dati Grezzi'))
        self._build_raw(tab_raw)

        tab_rep = tk.Frame(self.nb)
        self.nb.add(tab_rep, text=self.lang.get('fa_tab_repaired', 'Schede Riparate'))
        self._build_repaired(tab_rep)

        tab_scrap = tk.Frame(self.nb)
        self.nb.add(tab_scrap, text=self.lang.get('fa_tab_scrap', 'Scrap'))
        self._build_scrap(tab_scrap)

        tab_st = tk.Frame(self.nb)
        self.nb.add(tab_st, text=self.lang.get('fa_tab_stats', 'Statistiche'))
        self._build_stats(tab_st)

    def _make_tree(self, parent, cols, widths, labels=None):
        f = tk.Frame(parent)
        f.pack(fill=tk.BOTH, expand=True)
        vb = ttk.Scrollbar(f, orient=tk.VERTICAL)
        hb = ttk.Scrollbar(f, orient=tk.HORIZONTAL)
        tree = ttk.Treeview(f, columns=cols, show='headings',
                            yscrollcommand=vb.set, xscrollcommand=hb.set)
        vb.config(command=tree.yview)
        hb.config(command=tree.xview)
        for i, (c, w) in enumerate(zip(cols, widths)):
            lbl = labels[i] if labels else c
            tree.heading(c, text=lbl)
            tree.column(c, width=w, minwidth=40, anchor=tk.CENTER if w <= 80 else tk.W)
        vb.pack(side=tk.RIGHT, fill=tk.Y)
        hb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def _build_raw(self, parent):
        # Barra filtri sopra la griglia
        fbar = tk.Frame(parent, bg='#F8F8F8', padx=6, pady=4)
        fbar.pack(fill=tk.X)
        chk = tk.Checkbutton(
            fbar,
            text=self.lang.get('fa_filter_active', 'Solo FAIL ancora aperti'),
            variable=self.filter_active_var,
            command=self._populate_raw,
            bg='#F8F8F8', font=('Segoe UI', 9)
        )
        chk.pack(side=tk.LEFT)
        self.raw_count_lbl = tk.Label(fbar, text='', bg='#F8F8F8',
                                      font=('Segoe UI', 9), fg='#555')
        self.raw_count_lbl.pack(side=tk.LEFT, padx=12)

        col_keys = [
            ('fa_col_order',    'N. Ordine',     110),
            ('fa_col_product',  'Prodotto',      110),
            ('fa_col_qty',      'Qty',            55),
            ('fa_col_phase',    'Fase',          110),
            ('fa_col_idboard',  'IDBoard',        65),
            ('fa_col_labels',   'Label',         160),
            ('fa_col_scanres',  'Risultato',      65),
            ('fa_col_scantime', 'Data Scan',     140),
            ('fa_col_repair',   'Riparazione',    85),
            ('fa_col_defect',   'Difetto',       160),
            ('fa_col_codref',   'Cod.Rif.',      110),
        ]
        cols   = tuple(k for k, _, _ in col_keys)
        widths = tuple(w for _, _, w in col_keys)
        labels = tuple(self.lang.get(k, d) for k, d, _ in col_keys)
        self.tree_raw = self._make_tree(parent, cols, widths, labels)
        self.tree_raw.tag_configure('fail',     background='#FADADD')
        self.tree_raw.tag_configure('repaired', background='#D4EDDA')
        self.tree_raw.tag_configure('scrap',    background='#FFE5B4')

    def _build_repaired(self, parent):
        col_keys = [
            ('fa_col_order',     'N. Ordine',     110),
            ('fa_col_product',   'Prodotto',      110),
            ('fa_col_phase',     'Fase',          110),
            ('fa_col_idboard',   'IDBoard',        65),
            ('fa_col_labels',    'Label',         160),
            ('fa_col_scantime',  'Data Scan',     140),
            ('fa_col_resolved',  'Data Risoluz.', 140),
            ('fa_col_days',      'Giorni',         70),
        ]
        cols   = tuple(k for k, _, _ in col_keys)
        widths = tuple(w for _, _, w in col_keys)
        labels = tuple(self.lang.get(k, d) for k, d, _ in col_keys)
        self.tree_rep = self._make_tree(parent, cols, widths, labels)
        self.tree_rep.tag_configure('fast',   background='#D4EDDA')
        self.tree_rep.tag_configure('medium', background='#FFF3CD')
        self.tree_rep.tag_configure('slow',   background='#FFE5B4')


    def _build_scrap(self, parent):
        col_keys = [
            ('fa_col_order',    'N. Ordine',     110),
            ('fa_col_product',  'Prodotto',      110),
            ('fa_col_phase',    'Fase',          110),
            ('fa_col_idboard',  'IDBoard',        65),
            ('fa_col_labels',   'Label',         160),
            ('fa_col_scantime', 'Data Scan',     140),
            ('fa_col_resolved', 'Data Scrap',    140),
        ]
        cols   = tuple(k for k, _, _ in col_keys)
        widths = tuple(w for _, _, w in col_keys)
        labels = tuple(self.lang.get(k, d) for k, d, _ in col_keys)
        self.tree_scrap = self._make_tree(parent, cols, widths, labels)
        self.tree_scrap.tag_configure('scrap', background='#FADADD')

    def _build_stats(self, parent):
        self.stats_text = tk.Text(parent, wrap=tk.WORD, state=tk.DISABLED,
                                  font=('Courier New', 9), bg='#F8F9FA', padx=8, pady=6)
        sb = ttk.Scrollbar(parent, command=self.stats_text.yview)
        self.stats_text.config(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    def _parse_dates(self):
        dt_from = datetime.datetime.strptime(self.from_var.get().strip(), '%Y-%m-%d')
        dt_to = datetime.datetime.strptime(self.to_var.get().strip(), '%Y-%m-%d')
        return dt_from, dt_to.replace(hour=23, minute=59, second=59)


    def _auto_refresh_if_needed(self):
        """All'apertura controlla se la cache ha giorni mancanti e li aggiorna automaticamente."""
        try:
            self._ensure_schema_main()
            self.db.cursor.execute(SEL_CACHE_DATES)
            row = self.db.cursor.fetchone()
            if not row or row[2] == 0:
                return  # Cache vuota, aspetta che l'utente prema Carica
            min_from, max_to = row[0], row[1]
            today = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
            today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            # Aggiorna i campi data nella UI
            self.from_var.set(min_from.strftime('%Y-%m-%d') if min_from else '')
            self.to_var.set(today.strftime('%Y-%m-%d'))
            if max_to >= today_start:
                # Dati già aggiornati a oggi: carica dalla cache
                self._load_from_cache(min_from, max_to)
                # Se repaired/scrap sono vuoti, la RepairsAnalysisCache è vuota
                # (es. prima apertura dopo migrazione schema) → carica in background
                if not self._repaired and not self._scrap:
                    self._loading = True
                    self.load_btn.config(state=tk.DISABLED)
                    self.status_var.set(
                        self.lang.get('fa_loading_repairs', 'Caricamento dati riparazione...')
                    )
                    threading.Thread(
                        target=self._bg_load_repairs_for_range,
                        args=(min_from, max_to),
                        daemon=True
                    ).start()
                return
            # Giorni mancanti: avvio refresh automatico in background
            self._loading = True
            self.load_btn.config(state=tk.DISABLED)
            gap_days = (today_start - max_to).days
            msg = self.lang.get('fa_auto_refreshing', 'Aggiornamento automatico: {0} giorni mancanti...')
            try:
                msg = msg.format(gap_days)
            except Exception:
                msg = f'Aggiornamento automatico: {gap_days} giorni mancanti...'
            self.status_var.set(msg)
            threading.Thread(
                target=self._bg_auto_refresh,
                args=(min_from, max_to, today),
                daemon=True
            ).start()
        except Exception as e:
            logger.warning(f"AnalisiFailsRS _auto_refresh_if_needed: {e}")

    def _bg_load_repairs_for_range(self, dt_from, dt_to):
        """Carica le riparazioni in background per il range indicato (quando RepairsAnalysisCache è vuota)."""
        try:
            conn = pyodbc.connect(self.db.conn_str, autocommit=False)
            self._ensure_cache_schema(conn)
            self._load_repairs_bg(conn, dt_from, dt_to)
            self._update_resolved_from_repairs(conn, dt_from, dt_to)
            conn.close()
            logger.info(f"AnalisiFailsRS _bg_load_repairs_for_range: completato ({dt_from} → {dt_to})")
            self.after(0, lambda: self._load_from_cache(dt_from, dt_to))
        except Exception as e:
            logger.error(f"AnalisiFailsRS _bg_load_repairs_for_range: {e}", exc_info=True)
            err_msg = str(e)
            self.after(0, lambda msg=err_msg: (
                self.status_var.set(f'Errore caricamento riparazioni: {msg}'),
                self.load_btn.config(state=tk.NORMAL),
                setattr(self, '_loading', False)
            ))

    def _bg_auto_refresh(self, min_from, old_to, new_to):
        """Aggiunge in background solo il periodo mancante (old_to → new_to) alla cache esistente."""
        try:
            conn = pyodbc.connect(self.db.conn_str, autocommit=False)
            cur = conn.cursor()
            self._ensure_cache_schema(conn)

            # 1. Carica FAIL per il solo periodo mancante
            cur.execute(QUERY_MAIN, (old_to, new_to))
            rows = cur.fetchall()
            cols_desc = [d[0] for d in cur.description]
            inserted = 0
            for r in rows:
                rd = dict(zip(cols_desc, r))
                cur.execute(INS_CACHE, (
                    rd.get('IDBoard'),
                    _trunc(rd.get('Labels', '') or '', 1000),
                    _trunc(rd.get('OrderNumber'), 200),
                    _trunc(rd.get('ProductCode'), 200),
                    rd.get('OrderQuantity'),
                    _trunc(rd.get('PhaseName'), 400),
                    _trunc(rd.get('Labels'), 2000),
                    _trunc(rd.get('ScanResult'), 20),
                    rd.get('ScanTime'),
                    _trunc(rd.get('RepairResult'), 40),
                    _trunc(rd.get('DefectNameRO'), 1000),
                    _trunc(rd.get('CodRiferimentoDefect'), 500),
                    min_from, new_to   # Nuovo range esteso
                ))
                inserted += 1
            conn.commit()

            # 2. Aggiorna QueryTo di tutti i record esistenti al nuovo range
            cur.execute(UPD_CACHE_QUERY_TO, (new_to, min_from, old_to))
            conn.commit()

            # 3. Aggiorna anche RepairsAnalysisCache (range esteso)
            cur.execute(UPD_REPAIRS_QUERY_TO, (new_to, min_from, old_to))
            conn.commit()

            # 4. Carica riparazioni per il solo periodo mancante e aggiorna
            self._load_repairs_bg(conn, min_from, new_to)
            self._update_resolved_from_repairs(conn, min_from, new_to)
            conn.close()

            logger.info(f"AnalisiFailsRS auto-refresh: {inserted} nuovi FAIL aggiunti ({old_to} -> {new_to})")
            self.after(0, lambda: self._load_from_cache(min_from, new_to))
        except Exception as e:
            logger.error(f"AnalisiFailsRS _bg_auto_refresh: {e}", exc_info=True)
            err_msg = str(e)
            self.after(0, lambda msg=err_msg: (
                self.status_var.set(f'Errore auto-refresh: {msg}'),
                self.load_btn.config(state=tk.NORMAL),
                setattr(self, '_loading', False)
            ))

    def _on_load(self):
        if self._loading:
            return
        try:
            dt_from, dt_to = self._parse_dates()
        except ValueError:
            messagebox.showerror('Errore', 'Formato data non valido (YYYY-MM-DD)', parent=self)
            return

        try:
            self.db.cursor.execute(TB, (dt_from, dt_to))
            count = self.db.cursor.fetchone()[0]
        except Exception:
            count = 0

        if count > 0:
            if not messagebox.askyesno(
                self.lang.get('fa_confirm_reload', 'Cache esistente'),
                self.lang.get('fa_confirm_reload_msg',
                              'Trovati {} record in cache.\nRicaricare dal database?').format(count),
                parent=self
            ):
                self._dt_from, self._dt_to = dt_from, dt_to
                self._load_from_cache(dt_from, dt_to)
                return

        self._loading = True
        self._dt_from, self._dt_to = dt_from, dt_to
        self.load_btn.config(state=tk.DISABLED)
        self.status_var.set(self.lang.get('fa_status_loading', 'Caricamento in corso...'))
        threading.Thread(target=self._bg_load, args=(dt_from, dt_to), daemon=True).start()

    def _bg_load(self, dt_from, dt_to):
        """Eseguito in background thread — usa connessione pyodbc dedicata."""
        try:
            conn = pyodbc.connect(self.db.conn_str, autocommit=False)
            cur = conn.cursor()
            # Allarga le colonne se necessario (operazione idempotente)
            self._ensure_cache_schema(conn)
            cur.execute(DEL_CACHE, (dt_from, dt_to))
            conn.commit()
            cur.execute(QUERY_MAIN, (dt_from, dt_to))
            rows = cur.fetchall()
            cols_desc = [d[0] for d in cur.description]
            for r in rows:
                rd = dict(zip(cols_desc, r))
                cur.execute(INS_CACHE, (
                    rd.get('IDBoard'),
                    _trunc(rd.get('Labels', '') or '', 1000),
                    _trunc(rd.get('OrderNumber'), 200),
                    _trunc(rd.get('ProductCode'), 200),
                    rd.get('OrderQuantity'),
                    _trunc(rd.get('PhaseName'), 400),
                    _trunc(rd.get('Labels'), 2000),
                    _trunc(rd.get('ScanResult'), 20),
                    rd.get('ScanTime'),
                    _trunc(rd.get('RepairResult'), 40),
                    _trunc(rd.get('DefectNameRO'), 1000),
                    _trunc(rd.get('CodRiferimentoDefect'), 500),
                    dt_from, dt_to
                ))
            conn.commit()
            # Also load and cache repair data
            self._load_repairs_bg(conn, dt_from, dt_to)
            # Mark resolved based on actual repair data
            self._update_resolved_from_repairs(conn, dt_from, dt_to)
            conn.close()
            self.after(0, lambda: self._load_from_cache(dt_from, dt_to))
        except Exception as e:
            logger.error(f"Errore BG load AnalisiFailsRS: {e}", exc_info=True)
            err_msg = str(e)
            self.after(0, lambda msg=err_msg: (
                self.status_var.set(f'Errore: {msg}'),
                self.load_btn.config(state=tk.NORMAL),
                setattr(self, '_loading', False)
            ))

    @staticmethod
    def _ensure_cache_schema(conn):
        """Allarga le colonne di FailsAnalysisCache se ancora dimensionate troppo piccole."""
        cur = conn.cursor()
        for stmt in ALTER_STMTS:
            try:
                cur.execute(stmt)
                conn.commit()
            except Exception as ex:
                # Ignora errori (es. colonna già della dimensione giusta)
                logger.debug(f"_ensure_cache_schema skip: {ex}")
                try:
                    conn.rollback()
                except Exception:
                    pass

    # Costanti SQL per migrazioni inline (usate da _ensure_schema_main)
    _SCHEMA_MIGRATIONS = [
        # Aggiunge ResolvedAs se mancante
        ("IF NOT EXISTS(SELECT 1 FROM sys.columns c "
         "INNER JOIN sys.tables t ON t.object_id=c.object_id "
         "INNER JOIN sys.schemas s ON s.schema_id=t.schema_id "
         "WHERE s.name='fls' AND t.name='FailsAnalysisCache' AND c.name='ResolvedAs') "
         "BEGIN ALTER TABLE [Traceability_RS].[fls].[FailsAnalysisCache] "
         "ADD [ResolvedAs] NVARCHAR(20) NULL END"),
        # Crea RepairsAnalysisCache se mancante
        ("IF NOT EXISTS(SELECT 1 FROM sys.tables t "
         "INNER JOIN sys.schemas s ON s.schema_id=t.schema_id "
         "WHERE t.name='RepairsAnalysisCache' AND s.name='fls') "
         "BEGIN CREATE TABLE [Traceability_RS].[fls].[RepairsAnalysisCache]("
         "[ID] INT IDENTITY PRIMARY KEY,"
         "[IDBoard] INT NULL,[Labels] NVARCHAR(2000) NOT NULL,"
         "[ProductCode] NVARCHAR(200) NULL,[OrderNumber] NVARCHAR(200) NULL,"
         "[PhaseName] NVARCHAR(400) NULL,[ResultRepair] NVARCHAR(20) NULL,"
         "[DateRepair] DATETIME NULL,[CodRiferimento] NVARCHAR(500) NULL,"
         "[Defect] NVARCHAR(1000) NULL,[QueryFrom] DATETIME NOT NULL,"
         "[QueryTo] DATETIME NOT NULL,[CachedAt] DATETIME DEFAULT GETDATE()) END"),
    ]

    def _ensure_schema_main(self):
        """Esegue le migrazioni schema usando db.cursor del thread principale."""
        for stmt in self._SCHEMA_MIGRATIONS:
            try:
                self.db.cursor.execute(stmt)
                self.db.conn.commit()
            except Exception as ex:
                logger.debug(f"_ensure_schema_main skip: {ex}")
                try:
                    self.db.conn.rollback()
                except Exception:
                    pass

    def _load_repairs_bg(self, conn, dt_from, dt_to):
        """Esegue QUERY_REPAIRS e salva in RepairsAnalysisCache."""
        try:
            cur = conn.cursor()
            cur.execute(DEL_REPAIRS)
            conn.commit()
            cur.execute(QUERY_REPAIRS, (dt_from, dt_to))
            rows = cur.fetchall()
            cols_desc = [d[0] for d in cur.description]
            for r in rows:
                rd = dict(zip(cols_desc, r))
                cur.execute(INS_REPAIRS, (
                    rd.get('IDBoard'),
                    _trunc(rd.get('Labels') or '', 2000),
                    _trunc(rd.get('ProductCode'), 200),
                    _trunc(rd.get('OrderProduction'), 200),
                    _trunc(rd.get('PhaseName'), 400),
                    _trunc(rd.get('ResultRepair'), 20),
                    rd.get('DateRepair'),
                    _trunc(rd.get('CodRiferimento'), 500),
                    _trunc(rd.get('Defect'), 1000),
                    dt_from, dt_to
                ))
            conn.commit()
            logger.info(f"AnalisiFailsRS: {len(rows)} righe riparazione caricate in cache")
        except Exception as e:
            logger.warning(f"AnalisiFailsRS _load_repairs_bg: {e}")

    def _update_resolved_from_repairs(self, conn, dt_from, dt_to):
        """Aggiorna ResolvedAt/ResolvedAs in FailsAnalysisCache basandosi sui dati reali di riparazione."""
        try:
            cur = conn.cursor()
            cur.execute(SEL_REPAIRS, (dt_from, dt_to))
            repair_rows = cur.fetchall()
            # Build dict: label -> (result, date)  — keep first REPAIRED, else SCRAP
            repair_map = {}
            for r in repair_rows:
                label, result, date_r = r[0], r[1], r[2]
                if label not in repair_map or result == 'REPAIRED':
                    repair_map[label] = (result, date_r)
            resolved = 0
            for label, (result, date_r) in repair_map.items():
                cur.execute(UPD_RESOLVED_AS, (date_r, result, label, dt_from, dt_to))
                resolved += cur.rowcount
            if resolved:
                conn.commit()
                logger.info(f"AnalisiFailsRS: {resolved} schede marcate {result}")
        except Exception as e:
            logger.warning(f"AnalisiFailsRS _update_resolved_from_repairs: {e}")

    def _update_resolved_bg(self, conn, dt_from, dt_to):
        """Aggiorna ResolvedAt usando una connessione dedicata (chiamata da bg thread)."""
        try:
            now = datetime.datetime.now()
            t0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
            t1 = now.replace(hour=23, minute=59, second=59, microsecond=0)
            cur = conn.cursor()
            cur.execute(QUERY_TODAY, (t0, t1))
            active = {r[0] for r in cur.fetchall()}
            cur.execute(SEL_UNRESOLVED, (dt_from, dt_to))
            cached = {r[0] for r in cur.fetchall()}
            resolved = cached - active
            for board_id in resolved:
                cur.execute(UPD_RESOLVED, (now, board_id, dt_from, dt_to))
            if resolved:
                conn.commit()
                logger.info(f"AnalisiFailsRS: {len(resolved)} schede marcate risolte")
        except Exception as e:
            logger.warning(f"AnalisiFailsRS _update_resolved_bg: {e}")

    def _update_resolved(self, dt_from, dt_to):
        """Aggiorna ResolvedAt usando db.cursor (thread principale)."""
        try:
            now = datetime.datetime.now()
            t0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
            t1 = now.replace(hour=23, minute=59, second=59, microsecond=0)
            cur = self.db.cursor
            cur.execute(QUERY_TODAY, (t0, t1))
            active = {r[0] for r in cur.fetchall()}
            cur.execute(SEL_UNRESOLVED, (dt_from, dt_to))
            cached = {r[0] for r in cur.fetchall()}
            resolved = cached - active
            for board_id in resolved:
                cur.execute(UPD_RESOLVED, (now, board_id, dt_from, dt_to))
            if resolved:
                self.db.conn.commit()
                logger.info(f"AnalisiFailsRS: {len(resolved)} schede marcate risolte")
        except Exception as e:
            logger.warning(f"AnalisiFailsRS _update_resolved: {e}")

    def _load_from_cache(self, dt_from, dt_to):
        try:
            # Garantisce che ResolvedAs e RepairsAnalysisCache esistano
            # anche quando si carica dalla cache senza passare per _bg_load
            self._ensure_schema_main()
            cur = self.db.cursor
            cur.execute(SEL_CACHE_FULL, (dt_from, dt_to))
            self._data = cur.fetchall()
            # Load repaired and scrap directly from RepairsAnalysisCache
            # to get the real DateRepair, independent of FailsAnalysisCache matching
            cur.execute(SEL_REPAIRED_FROM_REPAIRS)
            self._repaired = cur.fetchall()
            cur.execute(SEL_SCRAP_FROM_REPAIRS)
            self._scrap = cur.fetchall()
            self.after(0, self._populate_ui)
        except Exception as e:
            logger.error(f"AnalisiFailsRS _load_from_cache: {e}", exc_info=True)
            self.status_var.set(f'Errore: {e}')
        finally:
            self._loading = False
            self.load_btn.config(state=tk.NORMAL)

    # ------------------------------------------------------------------
    def _populate_ui(self):
        self._populate_raw()
        self._populate_repaired()
        self._populate_scrap()
        self._populate_stats()
        fail_ids  = {r[0] for r in self._data}
        rep_ids   = {r[0] for r in self._repaired}
        scrap_ids = {r[0] for r in self._scrap}
        total = len(fail_ids)
        rep   = len(fail_ids & rep_ids)                     # FAIL riparati
        scrap = len(fail_ids & scrap_ids)                   # FAIL scrappati
        open_ = total - rep - scrap                         # FAIL ancora aperti
        pct   = (rep / total * 100) if total else 0
        self.status_var.set(
            self.lang.get('fa_status_ready',
                          '{0} schede FAIL \u2014 {1} riparate ({2:.1f}%)').format(total, rep, pct)
        )
        self.export_btn.config(state=tk.NORMAL if self._data else tk.DISABLED)


    def _populate_scrap(self):
        # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,
        #   4=PhaseName,5=ResultRepair,6=DateRepair,7=Defect,8=CodRiferimento
        for i in self.tree_scrap.get_children():
            self.tree_scrap.delete(i)
        seen = set()
        for r in self._scrap:
            board_id = r[0]
            if board_id in seen:
                continue
            seen.add(board_id)
            date_scrap = r[6]
            scan_time = next((d[8] for d in self._data if d[0] == board_id), None)
            self.tree_scrap.insert('', 'end', tags=('scrap',), values=(
                r[3], r[2], r[4], board_id, r[1],
                str(scan_time)[:19] if scan_time else '',
                str(date_scrap)[:19] if date_scrap else '',
            ))

    def _populate_raw(self):
        for i in self.tree_raw.get_children():
            self.tree_raw.delete(i)
        only_active = self.filter_active_var.get()
        seen = set()
        shown = 0
        for r in self._data:
            # r[12]=ResolvedAt: None = ancora FAIL, not None = riparata/scrap
            if only_active and r[12] is not None:
                continue
            key = (r[0], r[10], r[11])
            if key in seen:
                continue
            seen.add(key)
            shown += 1
            repair = r[9] or ''
            tag = 'repaired' if repair == 'REPAIRED' else ('scrap' if repair == 'SCRAP' else 'fail')
            self.tree_raw.insert('', tk.END, tags=(tag,), values=(
                r[2], r[3], r[4], r[5], r[0], r[6],
                r[7] or '', str(r[8])[:19] if r[8] else '',
                repair, r[10] or '', r[11] or ''
            ))
        # Aggiorna etichetta contatore
        total = len({r[0] for r in self._data})
        lbl_key = 'fa_raw_count'
        lbl_def = '{0} di {1} schede' if not only_active else '{0} schede FAIL aperte'
        lbl_text = self.lang.get(lbl_key, lbl_def)
        try:
            lbl_text = lbl_text.format(shown, total)
        except Exception:
            lbl_text = f'{shown} / {total}'
        if hasattr(self, 'raw_count_lbl'):
            self.raw_count_lbl.config(text=lbl_text)

    def _populate_repaired(self):
        # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,
        #   4=PhaseName,5=ResultRepair,6=DateRepair,7=Defect,8=CodRiferimento
        for i in self.tree_rep.get_children():
            self.tree_rep.delete(i)
        seen = set()
        for r in self._repaired:
            board_id = r[0]
            if board_id in seen:
                continue
            seen.add(board_id)
            date_repair = r[6]
            # Find scan time from _data (FailsAnalysisCache) by IDBoard
            scan_time = next((d[8] for d in self._data if d[0] == board_id), None)
            giorni = ''
            tag = 'medium'
            if date_repair and scan_time:
                delta = (date_repair - scan_time).days
                giorni = delta
                tag = 'fast' if delta <= 1 else ('medium' if delta <= 7 else 'slow')
            self.tree_rep.insert('', tk.END, tags=(tag,), values=(
                r[3], r[2], r[4], board_id, r[1],
                str(scan_time)[:19] if scan_time else '',
                str(date_repair)[:19] if date_repair else '',
                giorni
            ))

    def _populate_stats(self):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete('1.0', tk.END)

        # ── Set di IDBoard per ogni categoria ────────────────────────────────
        fail_ids    = {r[0] for r in self._data}          # FAIL nel periodo
        rep_ids     = {r[0] for r in self._repaired}      # Riparazioni nel periodo
        scrap_ids   = {r[0] for r in self._scrap}         # Scrap nel periodo

        # FAIL riparati = intersezione tra FAIL e riparazioni
        rep_of_fail   = fail_ids & rep_ids
        scrap_of_fail = fail_ids & scrap_ids
        open_of_fail  = fail_ids - rep_of_fail - scrap_of_fail

        total   = len(fail_ids)
        rep     = len(rep_of_fail)
        scrap_n = len(scrap_of_fail)
        open_n  = len(open_of_fail)
        pct     = (rep / total * 100) if total else 0

        T = self.lang.get
        lines = [
            '=' * 58,
            '  ' + T('fa_stats_title',    'FAIL BOARDS — RIEPILOGO STATISTICO'),
            '=' * 58,
            '  ' + T('fa_stats_total',    'Totale schede FAIL :') + f' {total}',
            '  ' + T('fa_stats_repaired', 'Schede riparate    :') + f' {rep}',
            '  ' + T('fa_stats_open',     'Schede aperte      :') + f' {open_n}',
            '  ' + T('fa_stats_scrap',    'Schede scrap       :') + f' {scrap_n}',
            '  ' + T('fa_stats_pct',      '% riparate         :') + f' {pct:.1f}%',
            '',
            '  ' + T('fa_stats_by_phase', 'Distribuzione per Fase:'),
            '-' * 42,
        ]

        # ── Distribuzione per fase (da FAIL) ─────────────────────────────────
        phases = Counter(r[5] for r in self._data if r[5])
        for ph, cnt in sorted(phases.items(), key=lambda x: -x[1]):
            lines.append(f'    {ph:<32} {cnt:>5}')

        # ── Riparazioni per periodo (tutte, non solo FAIL del range) ─────────
        now         = datetime.datetime.now()
        start_year  = datetime.datetime(now.year, 1, 1)
        start_month = datetime.datetime(now.year, now.month, 1)
        start_day   = datetime.datetime(now.year, now.month, now.day)
        # r[6] = DateRepair in RepairsAnalysisCache
        rep_year  = len({r[0] for r in self._repaired if r[6] and r[6] >= start_year})
        rep_month = len({r[0] for r in self._repaired if r[6] and r[6] >= start_month})
        rep_day   = len({r[0] for r in self._repaired if r[6] and r[6] >= start_day})
        lines += [
            '',
            '  ' + T('fa_stats_period_title', 'Schede riparate per periodo:'),
            '-' * 42,
            '  ' + T('fa_stats_rep_year',  'Da inizio anno    :') + f' {rep_year}',
            '  ' + T('fa_stats_rep_month', 'Da inizio mese    :') + f' {rep_month}',
            '  ' + T('fa_stats_rep_day',   "Nell'ultimo giorno:") + f' {rep_day}',
        ]

        # ── Top prodotti e label ──────────────────────────────────────────────
        lines += ['', '  ' + T('fa_stats_top_products', 'Top 15 Prodotti con piu FAIL:'), '-' * 42]
        prods = Counter(r[3] for r in self._data if r[3])
        for pr, cnt in prods.most_common(15):
            lines.append(f'    {pr:<32} {cnt:>5}')
        lines += ['', '  ' + T('fa_stats_top_labels', 'Top 10 Labels con piu FAIL:'), '-' * 42]
        lbs = Counter(r[6] for r in self._data if r[6])
        for lb, cnt in lbs.most_common(10):
            lines.append(f'    {lb:<32} {cnt:>5}')

        self.stats_text.insert(tk.END, '\n'.join(lines))
        self.stats_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------
    def _export_excel(self):
        if not self._data:
            messagebox.showwarning('', self.lang.get('fa_no_data', 'Nessun dato'), parent=self)
            return
        try:
            import openpyxl
            from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
            from openpyxl.utils import get_column_letter

            HDR_FILL = PatternFill('solid', fgColor='1F3864')
            HDR_FONT = Font(bold=True, color='FFFFFF')
            THIN = Border(left=Side(style='thin'), right=Side(style='thin'),
                          top=Side(style='thin'), bottom=Side(style='thin'))
            ALT = PatternFill('solid', fgColor='EBF3FB')

            def hdr(ws, headers):
                for c, h in enumerate(headers, 1):
                    cell = ws.cell(1, c, h)
                    cell.fill = HDR_FILL
                    cell.font = HDR_FONT
                    cell.alignment = Alignment(horizontal='center')
                    cell.border = THIN

            def autofit(ws):
                for col in ws.columns:
                    mx = max((len(str(ce.value or '')) for ce in col), default=8)
                    ws.column_dimensions[get_column_letter(col[0].column)].width = min(mx + 3, 50)

            wb = openpyxl.Workbook()

            # Sheet 1 — Raw
            ws1 = wb.active
            ws1.title = self.lang.get('fa_tab_raw', 'Dati Grezzi')
            hdr(ws1, ['OrderNumber', 'ProductCode', 'Qty', 'PhaseName', 'IDBoard', 'Labels',
                       'ScanResult', 'ScanTime', 'RepairResult', 'DefectNameRO', 'CodRiferimento'])
            FILLS = {
                'FAIL': PatternFill('solid', fgColor='FADADD'),
                'REPAIRED': PatternFill('solid', fgColor='D4EDDA'),
                'SCRAP': PatternFill('solid', fgColor='FFE5B4'),
            }
            seen, ri = set(), 2
            for r in self._data:
                key = (r[0], r[10], r[11])
                if key in seen:
                    continue
                seen.add(key)
                fl = FILLS.get(r[7] or '', ALT if ri % 2 == 0 else PatternFill())
                for c, v in enumerate([r[2], r[3], r[4], r[5], r[0], r[6], r[7],
                                        str(r[8])[:19] if r[8] else '', r[9], r[10], r[11]], 1):
                    ce = ws1.cell(ri, c, v)
                    ce.fill = fl
                    ce.border = THIN
                ri += 1
            ws1.freeze_panes = 'A2'
            autofit(ws1)

            # Sheet 2 — Repaired
            ws2 = wb.create_sheet(self.lang.get('fa_tab_repaired', 'Riparate'))
            hdr(ws2, ['OrderNumber', 'ProductCode', 'PhaseName', 'IDBoard', 'Labels',
                       'ScanTime', 'ResolvedAt', 'Giorni Riparazione'])
            seen2, ri = set(), 2
            for r in self._repaired:
                # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,
                #   4=PhaseName,5=ResultRepair,6=DateRepair
                if r[0] in seen2:
                    continue
                seen2.add(r[0])
                ra = r[6]  # DateRepair
                st = next((d[8] for d in self._data if d[0] == r[0]), None)
                giorni = ''
                fl = ALT
                if ra and st:
                    delta = (ra - st).days
                    giorni = delta
                    fl = (PatternFill('solid', fgColor='D4EDDA') if delta <= 1 else
                          PatternFill('solid', fgColor='FFF3CD') if delta <= 7 else
                          PatternFill('solid', fgColor='FFE5B4'))
                for c, v in enumerate([r[3], r[2], r[4], r[0], r[1],
                                        str(st)[:19] if st else '',
                                        str(ra)[:19] if ra else '', giorni], 1):
                    ce = ws2.cell(ri, c, v)
                    ce.fill = fl
                    ce.border = THIN
                ri += 1
            ws2.freeze_panes = 'A2'
            autofit(ws2)

            # Sheet 3 — Scrap
            ws_scrap = wb.create_sheet(self.lang.get('fa_tab_scrap', 'Scrap'))
            hdr(ws_scrap, [
                self.lang.get('fa_col_order',    'N. Ordine'),
                self.lang.get('fa_col_product',  'Prodotto'),
                self.lang.get('fa_col_phase',    'Fase'),
                self.lang.get('fa_col_idboard',  'IDBoard'),
                self.lang.get('fa_col_labels',   'Label'),
                self.lang.get('fa_col_scantime', 'Data Scan'),
                self.lang.get('fa_col_resolved', 'Data Scrap'),
            ])
            SCRAP_FILL = PatternFill('solid', fgColor='FADADD')
            seen_sc, ri = set(), 2
            for r in self._scrap:
                if r[0] in seen_sc:
                    continue
                seen_sc.add(r[0])
                # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,4=PhaseName,6=DateRepair
                scan_time_s = next((d[8] for d in self._data if d[0] == r[0]), None)
                for c, v in enumerate([r[3], r[2], r[4], r[0], r[1],
                                        str(scan_time_s)[:19] if scan_time_s else '',
                                        str(r[6])[:19] if r[6] else ''], 1):
                    ce = ws_scrap.cell(ri, c, v)
                    ce.fill = SCRAP_FILL
                    ce.border = THIN
                ri += 1
            ws_scrap.freeze_panes = 'A2'
            autofit(ws_scrap)

            # Sheet 4 — Stats
            ws3 = wb.create_sheet(self.lang.get('fa_tab_stats', 'Statistiche'))
            T3 = self.lang.get
            total = len({r[0] for r in self._data})
            rep   = len({r[0] for r in self._repaired})
            pct   = (rep / total * 100) if total else 0
            now3         = datetime.datetime.now()
            start_year3  = datetime.datetime(now3.year, 1, 1)
            start_month3 = datetime.datetime(now3.year, now3.month, 1)
            start_day3   = datetime.datetime(now3.year, now3.month, now3.day)
            rep_year3    = len({r[0] for r in self._repaired if r[12] and r[12] >= start_year3})
            rep_month3   = len({r[0] for r in self._repaired if r[12] and r[12] >= start_month3})
            rep_day3     = len({r[0] for r in self._repaired if r[12] and r[12] >= start_day3})
            # Riepilogo globale
            summary_rows = [
                [T3('fa_stats_total',    'Totale schede FAIL'),  total],
                [T3('fa_stats_repaired', 'Schede riparate'),     rep],
                [T3('fa_stats_scrap',    'Schede scrap'),        len({r[0] for r in self._scrap})],
                [T3('fa_stats_open',     'Schede aperte (non risolte)'), total - rep - len({r[0] for r in self._scrap})],
                [T3('fa_stats_pct',      '% Riparate'),          f'{pct:.1f}%'],
                [],
                [T3('fa_stats_period_title', 'Schede riparate per periodo'), ''],
                [T3('fa_stats_rep_year',  'Da inizio anno'),     rep_year3],
                [T3('fa_stats_rep_month', 'Da inizio mese'),     rep_month3],
                [T3('fa_stats_rep_day',   'Nell''ultimo giorno'), rep_day3],
                [],
            ]
            for row in summary_rows:
                ws3.append(row)
            # Header periodo
            r_per = 6
            for col in [1, 2]:
                ws3.cell(r_per, col).fill = PatternFill('solid', fgColor='2E75B6')
                ws3.cell(r_per, col).font = HDR_FONT
            # Distribuzione per Fase
            ws3.append([T3('fa_col_phase', 'Fase'), T3('fa_col_qty', 'N. schede')])
            r_h = ws3.max_row
            ws3.cell(r_h, 1).fill = HDR_FILL; ws3.cell(r_h, 1).font = HDR_FONT
            ws3.cell(r_h, 2).fill = HDR_FILL; ws3.cell(r_h, 2).font = HDR_FONT
            for ph, cnt in sorted(Counter(r[5] for r in self._data if r[5]).items(), key=lambda x: -x[1]):
                ws3.append([ph, cnt])
            ws3.append([])
            ws3.append([T3('fa_col_product', 'Prodotto'), T3('fa_col_qty', 'N. schede')])
            r_h2 = ws3.max_row
            ws3.cell(r_h2, 1).fill = HDR_FILL; ws3.cell(r_h2, 1).font = HDR_FONT
            ws3.cell(r_h2, 2).fill = HDR_FILL; ws3.cell(r_h2, 2).font = HDR_FONT
            for pr, cnt in Counter(r[3] for r in self._data if r[3]).most_common(20):
                ws3.append([pr, cnt])
            ws3.column_dimensions['A'].width = 40
            ws3.column_dimensions['B'].width = 18

            os.makedirs(r'C:\Temp', exist_ok=True)
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            fp = rf'C:\Temp\AnalisiFailsRS_{ts}.xlsx'
            wb.save(fp)
            logger.info(f"AnalisiFailsRS: Excel salvato {fp}")
            os.startfile(fp)
        except Exception as e:
            logger.error(f"AnalisiFailsRS export Excel: {e}", exc_info=True)
            messagebox.showerror('Errore', f'Impossibile generare Excel:\n{e}', parent=self)


def open_fails_analysis(parent, db, lang, user_name=''):
    FailsAnalysisWindow(parent, db, lang, user_name)
