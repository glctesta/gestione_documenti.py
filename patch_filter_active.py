"""Adds 'Solo FAIL attivi' filter checkbox to the raw data tab."""

with open('fails_analysis_gui.py', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add self.filter_active_var in __init__ ─────────────────────────────────
OLD1 = ('        self._data = []\n'
        '        self._repaired = []\n'
        '        self._scrap = []\n'
        '        self._loading = False')
NEW1 = ('        self._data = []\n'
        '        self._repaired = []\n'
        '        self._scrap = []\n'
        '        self._loading = False\n'
        '        self.filter_active_var = tk.BooleanVar(value=True)  # Filtro FAIL attivi')
if OLD1 in content:
    content = content.replace(OLD1, NEW1)
    print("Step 1 OK - filter_active_var added to __init__")
else:
    print("Step 1 SKIPPED")

# ── 2. Add filter checkbox row at top of _build_raw ──────────────────────────
OLD2 = ('    def _build_raw(self, parent):\n'
        '        col_keys = [')
NEW2 = ('    def _build_raw(self, parent):\n'
        '        # Barra filtri sopra la griglia\n'
        '        fbar = tk.Frame(parent, bg=\'#F8F8F8\', padx=6, pady=4)\n'
        '        fbar.pack(fill=tk.X)\n'
        '        chk = tk.Checkbutton(\n'
        '            fbar,\n'
        '            text=self.lang.get(\'fa_filter_active\', \'Solo FAIL ancora aperti\'),\n'
        '            variable=self.filter_active_var,\n'
        '            command=self._populate_raw,\n'
        '            bg=\'#F8F8F8\', font=(\'Segoe UI\', 9)\n'
        '        )\n'
        '        chk.pack(side=tk.LEFT)\n'
        '        self.raw_count_lbl = tk.Label(fbar, text=\'\', bg=\'#F8F8F8\',\n'
        '                                      font=(\'Segoe UI\', 9), fg=\'#555\')\n'
        '        self.raw_count_lbl.pack(side=tk.LEFT, padx=12)\n'
        '\n'
        '        col_keys = [')
if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("Step 2 OK - filter checkbox added in _build_raw")
else:
    print("Step 2 SKIPPED")

# ── 3. Update _populate_raw to apply filter and update count label ────────────
OLD3 = ('    def _populate_raw(self):\n'
        '        for i in self.tree_raw.get_children():\n'
        '            self.tree_raw.delete(i)\n'
        '        seen = set()\n'
        '        for r in self._data:\n'
        '            key = (r[0], r[10], r[11])\n'
        '            if key in seen:\n'
        '                continue\n'
        '            seen.add(key)\n'
        '            repair = r[9] or \'\'\n'
        '            tag = \'repaired\' if repair == \'REPAIRED\' else (\'scrap\' if repair == \'SCRAP\' else \'fail\')\n'
        '            self.tree_raw.insert(\'\', tk.END, tags=(tag,), values=(\n'
        '                r[2], r[3], r[4], r[5], r[0], r[6],\n'
        '                r[7] or \'\', str(r[8])[:19] if r[8] else \'\',\n'
        '                repair, r[10] or \'\', r[11] or \'\'\n'
        '            ))')
NEW3 = ('    def _populate_raw(self):\n'
        '        for i in self.tree_raw.get_children():\n'
        '            self.tree_raw.delete(i)\n'
        '        only_active = self.filter_active_var.get()\n'
        '        seen = set()\n'
        '        shown = 0\n'
        '        for r in self._data:\n'
        '            # r[12]=ResolvedAt: None = ancora FAIL, not None = riparata/scrap\n'
        '            if only_active and r[12] is not None:\n'
        '                continue\n'
        '            key = (r[0], r[10], r[11])\n'
        '            if key in seen:\n'
        '                continue\n'
        '            seen.add(key)\n'
        '            shown += 1\n'
        '            repair = r[9] or \'\'\n'
        '            tag = \'repaired\' if repair == \'REPAIRED\' else (\'scrap\' if repair == \'SCRAP\' else \'fail\')\n'
        '            self.tree_raw.insert(\'\', tk.END, tags=(tag,), values=(\n'
        '                r[2], r[3], r[4], r[5], r[0], r[6],\n'
        '                r[7] or \'\', str(r[8])[:19] if r[8] else \'\',\n'
        '                repair, r[10] or \'\', r[11] or \'\'\n'
        '            ))\n'
        '        # Aggiorna etichetta contatore\n'
        '        total = len({r[0] for r in self._data})\n'
        '        lbl_key = \'fa_raw_count\'\n'
        '        lbl_def = \'{0} di {1} schede\' if not only_active else \'{0} schede FAIL aperte\'\n'
        '        lbl_text = self.lang.get(lbl_key, lbl_def)\n'
        '        try:\n'
        '            lbl_text = lbl_text.format(shown, total)\n'
        '        except Exception:\n'
        '            lbl_text = f\'{shown} / {total}\'\n'
        '        if hasattr(self, \'raw_count_lbl\'):\n'
        '            self.raw_count_lbl.config(text=lbl_text)')
if OLD3 in content:
    content = content.replace(OLD3, NEW3)
    print("Step 3 OK - _populate_raw updated with filter logic")
else:
    print("Step 3 SKIPPED")

with open('fails_analysis_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written OK")
