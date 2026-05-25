"""Adds auto-refresh on form open: checks cache dates and appends missing days in background."""

with open('fails_analysis_gui.py', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add SEL_CACHE_DATES constant after SEL_CACHE_FULL ─────────────────────
OLD1 = ('SEL_CACHE_FULL = (\n'
        '    "SELECT IDBoard,LabelCode,OrderNumber,ProductCode,OrderQuantity,PhaseName,Labels,"\n'
        '    "ScanResult,ScanTime,RepairResult,DefectNameRO,CodRiferimento,ResolvedAt,ResolvedAs "\n'
        '    "FROM [Traceability_RS].[fls].[FailsAnalysisCache] "\n'
        '    "WHERE QueryFrom=? AND QueryTo=? ORDER BY OrderNumber,ProductCode,IDBoard"\n'
        ')')
NEW1 = (OLD1 + '\n\n'
        'SEL_CACHE_DATES = (\n'
        '    "SELECT MIN(QueryFrom), MAX(QueryTo), COUNT(*) "\n'
        '    "FROM [Traceability_RS].[fls].[FailsAnalysisCache]"\n'
        ')\n'
        'UPD_CACHE_QUERY_TO = (\n'
        '    "UPDATE [Traceability_RS].[fls].[FailsAnalysisCache] "\n'
        '    "SET QueryTo=? WHERE QueryFrom=? AND QueryTo=?"\n'
        ')\n'
        'UPD_REPAIRS_QUERY_TO = (\n'
        '    "UPDATE [Traceability_RS].[fls].[RepairsAnalysisCache] "\n'
        '    "SET QueryTo=? WHERE QueryFrom=? AND QueryTo=?"\n'
        ')')
if OLD1 in content:
    content = content.replace(OLD1, NEW1)
    print("Step 1 OK - SEL_CACHE_DATES added")
else:
    print("Step 1 SKIPPED")

# ── 2. Trigger auto-refresh after _build_ui ──────────────────────────────────
OLD2 = '        self._build_ui()\n        self.grab_set()\n'
NEW2 = ('        self._build_ui()\n'
        '        self.grab_set()\n'
        '        # Avvia auto-refresh in background se la cache ha dati precedenti\n'
        '        self.after(200, self._auto_refresh_if_needed)\n')
if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("Step 2 OK - auto_refresh trigger added")
else:
    print("Step 2 SKIPPED")

# ── 3. Add _auto_refresh_if_needed and _bg_auto_refresh before _on_load ──────
AUTO_METHODS = '''
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

'''

# Insert before _on_load
BEFORE = '    def _on_load(self):'
if BEFORE in content:
    content = content.replace(BEFORE, AUTO_METHODS + BEFORE)
    print("Step 3 OK - auto-refresh methods added")
else:
    print("Step 3 SKIPPED")

with open('fails_analysis_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written OK")
