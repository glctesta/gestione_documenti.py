"""
Fix 1: Remove _update_resolved (QUERY_TODAY) from _load_from_cache — it overwrites real repair dates with 'now'
Fix 2: Load _scrap and _repaired directly from RepairsAnalysisCache, not from FailsAnalysisCache matching
"""

with open('fails_analysis_gui.py', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add SEL_SCRAP / SEL_REPAIRED_FROM_REPAIRS constants ───────────────────
OLD1 = 'UPD_REPAIRS_QUERY_TO = (\n    "UPDATE [Traceability_RS].[fls].[RepairsAnalysisCache] "\n    "SET QueryTo=? WHERE QueryFrom=? AND QueryTo=?"\n)'
NEW1 = (OLD1 + '\n\n'
        'SEL_SCRAP_FROM_REPAIRS = (\n'
        '    "SELECT IDBoard,Labels,ProductCode,OrderNumber,PhaseName,ResultRepair,DateRepair,Defect,CodRiferimento "\n'
        '    "FROM [Traceability_RS].[fls].[RepairsAnalysisCache] "\n'
        '    "WHERE QueryFrom=? AND QueryTo=? AND ResultRepair=\'SCRAP\' ORDER BY DateRepair"\n'
        ')\n'
        'SEL_REPAIRED_FROM_REPAIRS = (\n'
        '    "SELECT IDBoard,Labels,ProductCode,OrderNumber,PhaseName,ResultRepair,DateRepair,Defect,CodRiferimento "\n'
        '    "FROM [Traceability_RS].[fls].[RepairsAnalysisCache] "\n'
        '    "WHERE QueryFrom=? AND QueryTo=? AND ResultRepair=\'REPAIRED\' ORDER BY DateRepair"\n'
        ')')
if OLD1 in content:
    content = content.replace(OLD1, NEW1)
    print("Step 1 OK - SEL_SCRAP/SEL_REPAIRED constants added")
else:
    print("Step 1 SKIPPED")

# ── 2. Remove _update_resolved from _load_from_cache ─────────────────────────
OLD2 = ('        try:\n'
        '            # Garantisce che ResolvedAs e RepairsAnalysisCache esistano\n'
        '            # anche quando si carica dalla cache senza passare per _bg_load\n'
        '            self._ensure_schema_main()\n'
        '            self._update_resolved(dt_from, dt_to)\n'
        '            cur = self.db.cursor\n'
        '            cur.execute(SEL_CACHE_FULL, (dt_from, dt_to))')
NEW2 = ('        try:\n'
        '            # Garantisce che ResolvedAs e RepairsAnalysisCache esistano\n'
        '            # anche quando si carica dalla cache senza passare per _bg_load\n'
        '            self._ensure_schema_main()\n'
        '            cur = self.db.cursor\n'
        '            cur.execute(SEL_CACHE_FULL, (dt_from, dt_to))')
if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("Step 2 OK - _update_resolved removed from _load_from_cache")
else:
    print("Step 2 SKIPPED")

# ── 3. Load _scrap and _repaired from RepairsAnalysisCache directly ───────────
OLD3 = ('            self._data = cur.fetchall()\n'
        '            # r[13] = ResolvedAs: \'REPAIRED\' or \'SCRAP\'\n'
        '            self._repaired = [r for r in self._data if r[12] is not None and r[13] != \'SCRAP\']\n'
        '            self._scrap    = [r for r in self._data if r[12] is not None and r[13] == \'SCRAP\']\n'
        '            self.after(0, self._populate_ui)')
NEW3 = ('            self._data = cur.fetchall()\n'
        '            # Load repaired and scrap directly from RepairsAnalysisCache\n'
        '            # to get the real DateRepair, independent of FailsAnalysisCache matching\n'
        '            cur.execute(SEL_REPAIRED_FROM_REPAIRS, (dt_from, dt_to))\n'
        '            self._repaired = cur.fetchall()\n'
        '            cur.execute(SEL_SCRAP_FROM_REPAIRS, (dt_from, dt_to))\n'
        '            self._scrap = cur.fetchall()\n'
        '            self.after(0, self._populate_ui)')
if OLD3 in content:
    content = content.replace(OLD3, NEW3)
    print("Step 3 OK - _repaired/_scrap from RepairsAnalysisCache")
else:
    print("Step 3 SKIPPED")

# ── 4. Update _populate_repaired to use new RepairsAnalysisCache format ───────
# RepairsAnalysisCache columns: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,
#   4=PhaseName,5=ResultRepair,6=DateRepair,7=Defect,8=CodRiferimento
# Old FailsAnalysisCache format used: r[0]=IDBoard,r[2]=OrderNumber,r[3]=ProductCode,
#   r[5]=PhaseName,r[6]=Labels,r[8]=ScanTime,r[12]=ResolvedAt
OLD4 = ('    def _populate_repaired(self):\n'
        '        for i in self.tree_rep.get_children():\n'
        '            self.tree_rep.delete(i)\n'
        '        seen = set()\n'
        '        for r in self._repaired:\n'
        '            if r[0] in seen:\n'
        '                continue\n'
        '            seen.add(r[0])\n'
        '            resolved_at = r[12]\n'
        '            scan_time = r[8]\n'
        '            giorni = \'\'\n'
        '            tag = \'medium\'\n'
        '            if resolved_at and scan_time:\n'
        '                delta = (resolved_at - scan_time).days\n'
        '                giorni = delta\n'
        '                tag = \'fast\' if delta <= 1 else (\'medium\' if delta <= 7 else \'slow\')\n'
        '            self.tree_rep.insert(\'\', tk.END, tags=(tag,), values=(\n'
        '                r[2], r[3], r[5], r[0], r[6],\n'
        '                str(scan_time)[:19] if scan_time else \'\',\n'
        '                str(resolved_at)[:19] if resolved_at else \'\',\n'
        '                giorni\n'
        '            ))')
NEW4 = ('    def _populate_repaired(self):\n'
        '        # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,\n'
        '        #   4=PhaseName,5=ResultRepair,6=DateRepair,7=Defect,8=CodRiferimento\n'
        '        for i in self.tree_rep.get_children():\n'
        '            self.tree_rep.delete(i)\n'
        '        seen = set()\n'
        '        for r in self._repaired:\n'
        '            board_id = r[0]\n'
        '            if board_id in seen:\n'
        '                continue\n'
        '            seen.add(board_id)\n'
        '            date_repair = r[6]\n'
        '            # Find scan time from _data (FailsAnalysisCache) by IDBoard\n'
        '            scan_time = next((d[8] for d in self._data if d[0] == board_id), None)\n'
        '            giorni = \'\'\n'
        '            tag = \'medium\'\n'
        '            if date_repair and scan_time:\n'
        '                delta = (date_repair - scan_time).days\n'
        '                giorni = delta\n'
        '                tag = \'fast\' if delta <= 1 else (\'medium\' if delta <= 7 else \'slow\')\n'
        '            self.tree_rep.insert(\'\', tk.END, tags=(tag,), values=(\n'
        '                r[3], r[2], r[4], board_id, r[1],\n'
        '                str(scan_time)[:19] if scan_time else \'\',\n'
        '                str(date_repair)[:19] if date_repair else \'\',\n'
        '                giorni\n'
        '            ))')
if OLD4 in content:
    content = content.replace(OLD4, NEW4)
    print("Step 4 OK - _populate_repaired updated for new format")
else:
    print("Step 4 SKIPPED")

# ── 5. Update _populate_scrap to use RepairsAnalysisCache format ──────────────
OLD5 = ('    def _populate_scrap(self):\n'
        '        for i in self.tree_scrap.get_children():\n'
        '            self.tree_scrap.delete(i)\n'
        '        seen = set()\n'
        '        for r in self._scrap:\n'
        '            if r[0] in seen:\n'
        '                continue\n'
        '            seen.add(r[0])\n'
        '            resolved_at = r[12]\n'
        '            scan_time = r[8]\n'
        '            self.tree_scrap.insert(\'\', \'end\', tags=(\'scrap\',), values=(\n'
        '                r[2], r[3], r[5], r[0], r[6],\n'
        '                str(scan_time)[:19] if scan_time else \'\',\n'
        '                str(resolved_at)[:19] if resolved_at else \'\',\n'
        '            ))')
NEW5 = ('    def _populate_scrap(self):\n'
        '        # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,\n'
        '        #   4=PhaseName,5=ResultRepair,6=DateRepair,7=Defect,8=CodRiferimento\n'
        '        for i in self.tree_scrap.get_children():\n'
        '            self.tree_scrap.delete(i)\n'
        '        seen = set()\n'
        '        for r in self._scrap:\n'
        '            board_id = r[0]\n'
        '            if board_id in seen:\n'
        '                continue\n'
        '            seen.add(board_id)\n'
        '            date_scrap = r[6]\n'
        '            scan_time = next((d[8] for d in self._data if d[0] == board_id), None)\n'
        '            self.tree_scrap.insert(\'\', \'end\', tags=(\'scrap\',), values=(\n'
        '                r[3], r[2], r[4], board_id, r[1],\n'
        '                str(scan_time)[:19] if scan_time else \'\',\n'
        '                str(date_scrap)[:19] if date_scrap else \'\',\n'
        '            ))')
if OLD5 in content:
    content = content.replace(OLD5, NEW5)
    print("Step 5 OK - _populate_scrap updated for new format")
else:
    print("Step 5 SKIPPED")

# ── 6. Update stats scrap count (now from self._scrap directly) ───────────────
# The stats already use len({r[0] for r in self._scrap}) which works for both formats
# But r[0] is IDBoard in both old and new format, so it's still OK

# ── 7. Update Excel scrap sheet (same format change) ─────────────────────────
OLD7 = ('            seen_sc, ri = set(), 2\n'
        '            for r in self._scrap:\n'
        '                if r[0] in seen_sc:\n'
        '                    continue\n'
        '                seen_sc.add(r[0])\n'
        '                for c, v in enumerate([r[2],r[3],r[5],r[0],r[6],\n'
        '                                        str(r[8])[:19] if r[8] else \'\',\n'
        '                                        str(r[12])[:19] if r[12] else \'\'], 1):\n'
        '                    ce = ws_scrap.cell(ri, c, v)\n'
        '                    ce.fill = SCRAP_FILL\n'
        '                    ce.border = THIN\n'
        '                ri += 1')
NEW7 = ('            seen_sc, ri = set(), 2\n'
        '            for r in self._scrap:\n'
        '                if r[0] in seen_sc:\n'
        '                    continue\n'
        '                seen_sc.add(r[0])\n'
        '                # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,\n'
        '                #   4=PhaseName,6=DateRepair\n'
        '                scan_time_s = next((d[8] for d in self._data if d[0] == r[0]), None)\n'
        '                for c, v in enumerate([r[3],r[2],r[4],r[0],r[1],\n'
        '                                        str(scan_time_s)[:19] if scan_time_s else \'\',\n'
        '                                        str(r[6])[:19] if r[6] else \'\'], 1):\n'
        '                    ce = ws_scrap.cell(ri, c, v)\n'
        '                    ce.fill = SCRAP_FILL\n'
        '                    ce.border = THIN\n'
        '                ri += 1')
if OLD7 in content:
    content = content.replace(OLD7, NEW7)
    print("Step 7 OK - Excel scrap sheet updated for new format")
else:
    print("Step 7 SKIPPED")

# ── 8. Update Excel repaired sheet to use new format ─────────────────────────
OLD8 = ('            seen2, ri = set(), 2\n'
        '            for r in self._repaired:\n'
        '                if r[0] in seen2:\n'
        '                    continue\n'
        '                seen2.add(r[0])\n'
        '                ra, st = r[12], r[8]\n'
        '                giorni = \'\'\n'
        '                fl = ALT\n'
        '                if ra and st:\n'
        '                    delta = (ra - st).days\n'
        '                    giorni = delta\n'
        '                    fl = (PatternFill(\'solid\', fgColor=\'D4EDDA\') if delta <= 1 else\n'
        '                          PatternFill(\'solid\', fgColor=\'FFF3CD\') if delta <= 7 else\n'
        '                          PatternFill(\'solid\', fgColor=\'FFE5B4\'))\n'
        '                for c, v in enumerate([r[2], r[3], r[5], r[0], r[6],\n'
        '                                        str(st)[:19] if st else \'\',\n'
        '                                        str(ra)[:19] if ra else \'\', giorni], 1):\n'
        '                    ce = ws2.cell(ri, c, v)\n'
        '                    ce.fill = fl\n'
        '                    ce.border = THIN\n'
        '                ri += 1')
NEW8 = ('            seen2, ri = set(), 2\n'
        '            for r in self._repaired:\n'
        '                # RepairsAnalysisCache: 0=IDBoard,1=Labels,2=ProductCode,3=OrderNumber,\n'
        '                #   4=PhaseName,5=ResultRepair,6=DateRepair\n'
        '                if r[0] in seen2:\n'
        '                    continue\n'
        '                seen2.add(r[0])\n'
        '                ra = r[6]  # DateRepair\n'
        '                st = next((d[8] for d in self._data if d[0] == r[0]), None)\n'
        '                giorni = \'\'\n'
        '                fl = ALT\n'
        '                if ra and st:\n'
        '                    delta = (ra - st).days\n'
        '                    giorni = delta\n'
        '                    fl = (PatternFill(\'solid\', fgColor=\'D4EDDA\') if delta <= 1 else\n'
        '                          PatternFill(\'solid\', fgColor=\'FFF3CD\') if delta <= 7 else\n'
        '                          PatternFill(\'solid\', fgColor=\'FFE5B4\'))\n'
        '                for c, v in enumerate([r[3], r[2], r[4], r[0], r[1],\n'
        '                                        str(st)[:19] if st else \'\',\n'
        '                                        str(ra)[:19] if ra else \'\', giorni], 1):\n'
        '                    ce = ws2.cell(ri, c, v)\n'
        '                    ce.fill = fl\n'
        '                    ce.border = THIN\n'
        '                ri += 1')
if OLD8 in content:
    content = content.replace(OLD8, NEW8)
    print("Step 8 OK - Excel repaired sheet updated for new format")
else:
    print("Step 8 SKIPPED")

with open('fails_analysis_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written OK")
