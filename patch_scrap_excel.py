"""Adds Scrap Excel sheet and updates stats scrap count."""

with open('fails_analysis_gui.py', encoding='utf-8') as f:
    content = f.read()

# Add SCRAP sheet in Excel after Sheet 2
old = "            ws2.freeze_panes = 'A2'\n            autofit(ws2)\n\n            # Sheet 3 \u2014 Stats"
new = """            ws2.freeze_panes = 'A2'
            autofit(ws2)

            # Sheet 3 \u2014 Scrap
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
                for c, v in enumerate([r[2], r[3], r[5], r[0], r[6],
                                        str(r[8])[:19] if r[8] else '',
                                        str(r[12])[:19] if r[12] else ''], 1):
                    ce = ws_scrap.cell(ri, c, v)
                    ce.fill = SCRAP_FILL
                    ce.border = THIN
                ri += 1
            ws_scrap.freeze_panes = 'A2'
            autofit(ws_scrap)

            # Sheet 4 \u2014 Stats"""

if old in content:
    content = content.replace(old, new)
    print("Excel Scrap sheet: OK")
else:
    print("Excel Scrap NOT FOUND - searching...")
    idx = content.find("ws2.freeze_panes = 'A2'")
    print(f"  Found at idx: {idx}")
    print(f"  Context: {repr(content[idx:idx+80])}")

# Add scrap count to stats text
old2 = ("            '  ' + T('fa_stats_open',           'Schede aperte      :') + f' {total - rep}',")
new2 = ("            '  ' + T('fa_stats_open',           'Schede aperte      :') + f' {total - rep - len({r[0] for r in self._scrap})}',\n"
        "            '  ' + T('fa_stats_scrap',          'Schede scrap       :') + f' {len({r[0] for r in self._scrap})}',")
if old2 in content:
    content = content.replace(old2, new2)
    print("Stats scrap count: OK")
else:
    print("Stats scrap NOT FOUND")

# Also add scrap in Excel stats sheet summary
old3 = ("                [T3('fa_stats_repaired', 'Schede riparate'),     rep],\n"
        "                [T3('fa_stats_open',     'Schede aperte'),       total - rep],")
new3 = ("                [T3('fa_stats_repaired', 'Schede riparate'),     rep],\n"
        "                [T3('fa_stats_scrap',    'Schede scrap'),        len({r[0] for r in self._scrap})],\n"
        "                [T3('fa_stats_open',     'Schede aperte (non risolte)'), total - rep - len({r[0] for r in self._scrap})],")
if old3 in content:
    content = content.replace(old3, new3)
    print("Excel stats scrap: OK")
else:
    print("Excel stats scrap NOT FOUND")

with open('fails_analysis_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written")
