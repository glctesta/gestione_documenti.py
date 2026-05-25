"""Patches fails_analysis_gui.py with the new repair query and scrap tab support."""
import re

with open('fails_analysis_gui.py', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add new SQL constants after UPD_RESOLVED ──────────────────────────────
MARKER = 'UPD_RESOLVED = "UPDATE [Traceability_RS].[fls].[FailsAnalysisCache] SET ResolvedAt=? WHERE IDBoard=? AND QueryFrom=? AND QueryTo=? AND ResolvedAt IS NULL"'
ADDITION = r'''
DEL_REPAIRS = "DELETE FROM [Traceability_RS].[fls].[RepairsAnalysisCache] WHERE QueryFrom=? AND QueryTo=?"
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
    "    INNER JOIN DefectsRiferimenti ON DefectsRiferimenti.IDScanDefectDet=ScanDefectDetails.IDScanDefectDet"
    "    INNER JOIN Riferiments ON Riferiments.IDDibaRiferimento=DefectsRiferimenti.IDDibaRiferimento"
    "    INNER JOIN Defects ON ScanDefectDetails.IDDefect=Defects.IDDefect"
    "    INNER JOIN Scannings ON Scannings.IDScan=ScanDefects.IDScan"
    "    INNER JOIN OrderPhases ON OrderPhases.IDOrderPhase=Scannings.IDOrderPhase"
    "    INNER JOIN Orders ON OrderPhases.IDOrder=Orders.IDOrder"
    "    INNER JOIN Products ON Products.IDProduct=Orders.IDProduct"
    "    INNER JOIN Phases ON OrderPhases.IDPhase=Phases.IDPhase"
    "    INNER JOIN Boards ON Scannings.IDBoard=Boards.IDBoard"
    "    WHERE ScanDefects.StopTime BETWEEN @from AND @to"
    ") D"
)'''

if MARKER in content:
    content = content.replace(MARKER, MARKER + ADDITION)
    print("Step 1 OK — new SQL constants added")
else:
    print("Step 1 SKIPPED — marker not found (already done?)")

# ── 2. Add _scrap to __init__ ─────────────────────────────────────────────────
old2 = '        self._data = []\n        self._repaired = []'
new2 = '        self._data = []\n        self._repaired = []\n        self._scrap = []'
if old2 in content:
    content = content.replace(old2, new2)
    print("Step 2 OK — _scrap added to __init__")
else:
    print("Step 2 SKIPPED")

# ── 3. Replace SEL_CACHE with SEL_CACHE_FULL in _load_from_cache ──────────────
old3 = 'cur.execute(SEL_CACHE, (dt_from, dt_to))'
new3 = 'cur.execute(SEL_CACHE_FULL, (dt_from, dt_to))'
if old3 in content:
    content = content.replace(old3, new3)
    print("Step 3 OK — SEL_CACHE -> SEL_CACHE_FULL")
else:
    print("Step 3 SKIPPED")

# ── 4. Update _load_from_cache to populate _scrap ────────────────────────────
old4 = ('            self._data = cur.fetchall()\n'
        '            self._repaired = [r for r in self._data if r[12] is not None]\n'
        '            self.after(0, self._populate_ui)')
new4 = ('            self._data = cur.fetchall()\n'
        '            # r[13] = ResolvedAs: \'REPAIRED\' or \'SCRAP\'\n'
        '            self._repaired = [r for r in self._data if r[12] is not None and r[13] != \'SCRAP\']\n'
        '            self._scrap    = [r for r in self._data if r[12] is not None and r[13] == \'SCRAP\']\n'
        '            self.after(0, self._populate_ui)')
if old4 in content:
    content = content.replace(old4, new4)
    print("Step 4 OK — _scrap populated in _load_from_cache")
else:
    print("Step 4 SKIPPED")

# ── 5. Add SCRAP tab in _build_ui (after tab_rep) ────────────────────────────
old5 = ("        tab_st = tk.Frame(self.nb)\n"
        "        self.nb.add(tab_st, text=self.lang.get('fa_tab_stats', 'Statistiche'))\n"
        "        self._build_stats(tab_st)")
new5 = ("        tab_scrap = tk.Frame(self.nb)\n"
        "        self.nb.add(tab_scrap, text=self.lang.get('fa_tab_scrap', 'Scrap'))\n"
        "        self._build_scrap(tab_scrap)\n"
        "\n"
        "        tab_st = tk.Frame(self.nb)\n"
        "        self.nb.add(tab_st, text=self.lang.get('fa_tab_stats', 'Statistiche'))\n"
        "        self._build_stats(tab_st)")
if old5 in content:
    content = content.replace(old5, new5)
    print("Step 5 OK — Scrap tab added in _build_ui")
else:
    print("Step 5 SKIPPED")

# ── 6. Add _build_scrap after _build_repaired ─────────────────────────────────
SCRAP_BUILD = '''
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

'''

AFTER_BUILD_REP = "    def _build_stats(self, parent):"
if AFTER_BUILD_REP in content:
    content = content.replace(AFTER_BUILD_REP, SCRAP_BUILD + "    def _build_stats(self, parent):")
    print("Step 6 OK — _build_scrap added")
else:
    print("Step 6 SKIPPED")

# ── 7. Add _populate_scrap and update _populate_ui ────────────────────────────
old7 = "        self.export_btn.config(state=tk.NORMAL if self._data else tk.DISABLED)"
new7 = ("        self._populate_scrap()\n"
        "        self.export_btn.config(state=tk.NORMAL if self._data else tk.DISABLED)")
if old7 in content:
    content = content.replace(old7, new7)
    print("Step 7 OK — _populate_scrap called in _populate_ui")
else:
    print("Step 7 SKIPPED")

POPULATE_SCRAP = '''
    def _populate_scrap(self):
        for i in self.tree_scrap.get_children():
            self.tree_scrap.delete(i)
        seen = set()
        for r in self._scrap:
            if r[0] in seen:
                continue
            seen.add(r[0])
            resolved_at = r[12]
            scan_time = r[8]
            self.tree_scrap.insert('', 'end', tags=('scrap',), values=(
                r[2], r[3], r[5], r[0], r[6],
                str(scan_time)[:19] if scan_time else '',
                str(resolved_at)[:19] if resolved_at else '',
            ))

'''
BEFORE_POPULATE_RAW = "    def _populate_raw(self):"
if BEFORE_POPULATE_RAW in content:
    content = content.replace(BEFORE_POPULATE_RAW, POPULATE_SCRAP + "    def _populate_raw(self):")
    print("Step 8 OK — _populate_scrap method added")
else:
    print("Step 8 SKIPPED")

# ── 8. Update _bg_load to also run QUERY_REPAIRS ─────────────────────────────
old8 = ("            self._update_resolved_bg(conn, dt_from, dt_to)\n"
        "            conn.close()\n"
        "            self.after(0, lambda: self._load_from_cache(dt_from, dt_to))")
new8 = ("            # Also load and cache repair data\n"
        "            self._load_repairs_bg(conn, dt_from, dt_to)\n"
        "            # Mark resolved based on actual repair data\n"
        "            self._update_resolved_from_repairs(conn, dt_from, dt_to)\n"
        "            conn.close()\n"
        "            self.after(0, lambda: self._load_from_cache(dt_from, dt_to))")
if old8 in content:
    content = content.replace(old8, new8)
    print("Step 9 OK — _bg_load updated for repairs")
else:
    print("Step 9 SKIPPED")

# ── 9. Replace _update_resolved_bg with new methods ──────────────────────────
old9 = "    def _update_resolved_bg(self, conn, dt_from, dt_to):"
new9 = '''    def _load_repairs_bg(self, conn, dt_from, dt_to):
        """Esegue QUERY_REPAIRS e salva in RepairsAnalysisCache."""
        try:
            cur = conn.cursor()
            cur.execute(DEL_REPAIRS, (dt_from, dt_to))
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

    def _update_resolved_bg(self, conn, dt_from, dt_to):'''

if old9 in content:
    content = content.replace(old9, new9)
    print("Step 10 OK — new repair methods added")
else:
    print("Step 10 SKIPPED")

with open('fails_analysis_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written OK")
