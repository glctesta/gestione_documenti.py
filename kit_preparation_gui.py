"""
kit_preparation_gui.py
GUI del modulo Kit Preparation — Sprint 1
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §3, §5.1.1, §8).

Due schede:
  - Priorita' Ordini: assegnazione priorita' P0-P3 agli ordini (tabella
    order_priority), per il pianificatore.
  - Liste Prelievo: import dei file Essegi da T:\\KITTING (scelta file se
    piu' di uno, hash SHA-256, anteprima) e lista delle picking list
    ordinata per priorita' poi data — la "lista WH".

Login a monte (gestito da main.py):
  - apertura via _execute_authorized_action('conferma_kit_completamento', ...)
    per il prelievo, o _execute_simple_login per la sola priorita'.
L'operatore (EmployeeHireHistoryId) arriva dal chiamante.
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import kit_essegi_parser as kep

logger = logging.getLogger("PlanMonitor")

PRIORITY_BADGE = {0: '⬜ P0', 1: '🔴 P1', 2: '🟠 P2', 3: '🟡 P3'}


def open_kit_preparation_window(parent, db, lang, user_name, operator_id, tab='picking'):
    """Apre la finestra Kit Preparation sulla scheda indicata ('priority'|'picking')."""
    win = KitPreparationWindow(parent, db, lang, user_name, operator_id, tab)
    return win


class KitPreparationWindow(tk.Toplevel):

    def __init__(self, parent, db, lang, user_name, operator_id, tab='picking'):
        super().__init__(parent)
        self.app = parent          # main app: serve per il login di deroga (Sprint 2)
        self.db = db
        self.lang = lang
        self.user_name = user_name or '?'
        self.operator_id = operator_id

        self.title(lang.get('kit_prep_title', 'Preparazione Kit Produzione'))
        self.geometry("1000x640")
        self.transient(parent)

        header = ttk.Frame(self, padding=(10, 6))
        header.pack(fill='x')
        ttk.Label(header,
                  text=f"{lang.get('kit_operator', 'Operatore')}: {self.user_name}",
                  font=("Segoe UI", 9, "italic")).pack(side='right')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=8, pady=(0, 8))

        self.priority_frame = ttk.Frame(self.notebook, padding=10)
        self.picking_frame = ttk.Frame(self.notebook, padding=10)
        self.requests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.priority_frame,
                          text=lang.get('kit_tab_priority', 'Priorità Ordini'))
        self.notebook.add(self.picking_frame,
                          text=lang.get('kit_tab_picking', 'Liste Prelievo'))
        self.notebook.add(self.requests_frame,
                          text=lang.get('kit_tab_requests', 'Richieste Materiale'))

        self._build_priority_tab()
        self._build_picking_tab()
        self._build_requests_tab()

        if tab == 'priority':
            self.notebook.select(self.priority_frame)
        else:
            self.notebook.select(self.picking_frame)

        self._refresh_priority_list()
        self._refresh_picking_lists()
        self._refresh_requests()
        logger.info("KitPreparationWindow aperta da %s (tab=%s)", self.user_name, tab)

    # ────────────────────────── TAB PRIORITA' ──────────────────────────── #

    def _build_priority_tab(self):
        f = self.priority_frame

        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Label(top, text=self.lang.get('kit_search_order', 'Cerca ordine:')).pack(side='left')
        self.search_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.search_var, width=24)
        entry.pack(side='left', padx=6)
        entry.bind('<Return>', lambda e: self._refresh_priority_list())
        ttk.Button(top, text=self.lang.get('kit_btn_search', 'Cerca'),
                   command=self._refresh_priority_list).pack(side='left')

        ttk.Label(top, text=self.lang.get('kit_priority_label', 'Priorità:')).pack(side='left', padx=(24, 4))
        self.priority_var = tk.StringVar(value='0')
        labels = {
            '0': self.lang.get('kit_priority_0', '[0] Normale'),
            '1': self.lang.get('kit_priority_1', '[1] Urgente'),
            '2': self.lang.get('kit_priority_2', '[2] Alta'),
            '3': self.lang.get('kit_priority_3', '[3] Media'),
        }
        self._priority_labels = labels
        self.priority_combo = ttk.Combobox(top, state='readonly', width=14,
                                           values=list(labels.values()))
        self.priority_combo.current(0)
        self.priority_combo.pack(side='left')
        ttk.Button(top, text=self.lang.get('kit_btn_apply_priority', 'Applica a selezione'),
                   command=self._apply_priority).pack(side='left', padx=6)

        cols = ('order', 'product', 'qty', 'priority', 'set_by', 'set_date')
        self.prio_tree = ttk.Treeview(f, columns=cols, show='headings', selectmode='extended')
        headings = {
            'order': self.lang.get('kit_col_order', 'Ordine'),
            'product': self.lang.get('kit_col_product', 'Prodotto'),
            'qty': self.lang.get('kit_col_qty', 'Qtà ordine'),
            'priority': self.lang.get('kit_col_priority', 'Priorità'),
            'set_by': self.lang.get('kit_col_set_by', 'Impostata da'),
            'set_date': self.lang.get('kit_col_set_date', 'Data'),
        }
        widths = {'order': 110, 'product': 220, 'qty': 80, 'priority': 80,
                  'set_by': 180, 'set_date': 130}
        for c in cols:
            self.prio_tree.heading(c, text=headings[c])
            self.prio_tree.column(c, width=widths[c], anchor='center' if c != 'product' else 'w')
        vsb = ttk.Scrollbar(f, orient='vertical', command=self.prio_tree.yview)
        self.prio_tree.configure(yscrollcommand=vsb.set)
        self.prio_tree.pack(side='left', expand=True, fill='both')
        vsb.pack(side='left', fill='y')

        self.prio_tree.tag_configure('p1', background='#ffd6d6')
        self.prio_tree.tag_configure('p2', background='#ffe8cc')
        self.prio_tree.tag_configure('p3', background='#fff7cc')

    def _refresh_priority_list(self):
        """Ordini con priorita' assegnata + risultato ricerca, ordinati per priorita'."""
        search = self.search_var.get().strip() if hasattr(self, 'search_var') else ''
        try:
            cursor = self.db.conn.cursor()
            if search:
                query = """
                SELECT TOP 200 o.OrderNumber, p.ProductCode, o.OrderQuantity,
                       ISNULL(op.priority, 0) AS priority,
                       ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '') AS set_by,
                       op.set_date
                FROM Traceability_RS.dbo.Orders o
                INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
                LEFT JOIN Traceability_RS.dbo.order_priority op ON op.order_number = o.OrderNumber
                LEFT JOIN employee.dbo.EmployeeHireHistory h ON h.EmployeeHireHistoryId = op.set_by
                LEFT JOIN employee.dbo.employees e ON e.EmployeeId = h.EmployeeId
                WHERE o.OrderNumber LIKE ?
                ORDER BY CASE WHEN ISNULL(op.priority,0)=0 THEN 4 ELSE op.priority END ASC,
                         o.OrderNumber DESC
                """
                cursor.execute(query, f'%{search}%')
            else:
                query = """
                SELECT o.OrderNumber, p.ProductCode, o.OrderQuantity,
                       op.priority,
                       ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '') AS set_by,
                       op.set_date
                FROM Traceability_RS.dbo.order_priority op
                INNER JOIN Traceability_RS.dbo.Orders o ON o.OrderNumber = op.order_number
                INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
                LEFT JOIN employee.dbo.EmployeeHireHistory h ON h.EmployeeHireHistoryId = op.set_by
                LEFT JOIN employee.dbo.employees e ON e.EmployeeId = h.EmployeeId
                ORDER BY CASE WHEN op.priority=0 THEN 4 ELSE op.priority END ASC,
                         o.OrderNumber DESC
                """
                cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            logger.error("Errore caricamento priorita': %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return

        self.prio_tree.delete(*self.prio_tree.get_children())
        for r in rows:
            prio = int(r[3]) if r[3] is not None else 0
            set_date = r[5].strftime('%d/%m/%Y %H:%M') if r[5] else ''
            tag = f'p{prio}' if prio in (1, 2, 3) else ''
            self.prio_tree.insert('', 'end', values=(
                r[0], r[1], r[2], PRIORITY_BADGE.get(prio, prio), r[4], set_date
            ), tags=(tag,))

    def _apply_priority(self):
        sel = self.prio_tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_select_order', 'Seleziona almeno un ordine'),
                parent=self)
            return
        priority = self.priority_combo.current()  # indice = valore 0..3
        try:
            cursor = self.db.conn.cursor()
            for item in sel:
                order_number = self.prio_tree.item(item)['values'][0]
                cursor.execute("""
                    MERGE Traceability_RS.dbo.order_priority AS t
                    USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
                    WHEN MATCHED THEN
                        UPDATE SET priority = ?, set_by = ?, set_date = GETDATE()
                    WHEN NOT MATCHED THEN
                        INSERT (order_number, priority, set_by) VALUES (s.order_number, ?, ?);
                """, (order_number, priority, self.operator_id, priority, self.operator_id))
            self.db.conn.commit()
            logger.info("Priorita' %d applicata a %d ordini da %s",
                        priority, len(sel), self.user_name)
        except Exception as e:
            self.db.conn.rollback()
            logger.error("Errore salvataggio priorita': %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        self._refresh_priority_list()
        self._refresh_picking_lists()

    # ────────────────────────── TAB LISTE PRELIEVO ─────────────────────── #

    def _build_picking_tab(self):
        f = self.picking_frame

        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Button(top, text=self.lang.get('kit_btn_load_list', 'Carica lista da T:\\KITTING'),
                   command=self._load_list_clicked).pack(side='left')
        ttk.Button(top, text=self.lang.get('kit_btn_open_picking', 'Apri prelievo'),
                   command=self._open_scan_selected).pack(side='left', padx=6)
        ttk.Button(top, text=self.lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh_picking_lists).pack(side='left')

        cols = ('id', 'priority', 'orders', 'file', 'rows', 'status', 'upload')
        self.lists_tree = ttk.Treeview(f, columns=cols, show='headings', selectmode='browse')
        headings = {
            'id': 'ID',
            'priority': self.lang.get('kit_col_priority', 'Priorità'),
            'orders': self.lang.get('kit_col_orders', 'Ordini'),
            'file': self.lang.get('kit_col_file', 'File'),
            'rows': self.lang.get('kit_col_rows', 'Righe'),
            'status': self.lang.get('kit_col_status', 'Stato'),
            'upload': self.lang.get('kit_col_upload_date', 'Caricata il'),
        }
        widths = {'id': 50, 'priority': 80, 'orders': 280, 'file': 200,
                  'rows': 60, 'status': 90, 'upload': 130}
        for c in cols:
            self.lists_tree.heading(c, text=headings[c])
            self.lists_tree.column(c, width=widths[c],
                                   anchor='w' if c in ('orders', 'file') else 'center')
        vsb = ttk.Scrollbar(f, orient='vertical', command=self.lists_tree.yview)
        self.lists_tree.configure(yscrollcommand=vsb.set)
        self.lists_tree.pack(side='left', expand=True, fill='both')
        vsb.pack(side='left', fill='y')

        self.lists_tree.tag_configure('p1', background='#ffd6d6')
        self.lists_tree.tag_configure('p2', background='#ffe8cc')
        self.lists_tree.tag_configure('p3', background='#fff7cc')
        self.lists_tree.bind('<Double-1>', lambda e: self._open_scan_selected())

    def _open_scan_selected(self):
        """Apre l'interfaccia di scansione per la lista selezionata (Sprint 2)."""
        sel = self.lists_tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_select_list', 'Seleziona una lista di prelievo'),
                parent=self)
            return
        values = self.lists_tree.item(sel[0])['values']
        list_id, status = values[0], str(values[5])
        if status not in ('OPEN', 'PARTIAL', 'REOPENED'):
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_msg_list_closed',
                              'La lista #{id} è in stato {status}: non è apribile.')
                .replace('{id}', str(list_id)).replace('{status}', status),
                parent=self)
            return
        import kit_scan_gui
        kit_scan_gui.open_kit_scan_window(
            self, self.app, self.db, self.lang,
            self.user_name, self.operator_id, int(list_id))

    def _refresh_picking_lists(self):
        """Lista WH: picking list ordinate per priorita' (P1>P2>P3>P0) poi data."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT pl.id, pl.source_file_name, pl.status, pl.upload_date,
                       STUFF((SELECT '/' + plo.order_number
                              FROM Traceability_RS.dbo.picking_list_orders plo
                              WHERE plo.picking_list_id = pl.id
                              FOR XML PATH('')), 1, 1, '') AS orders,
                       (SELECT COUNT(*) FROM Traceability_RS.dbo.picking_list_items i
                        WHERE i.picking_list_id = pl.id) AS n_rows,
                       MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) AS prio_rank
                FROM Traceability_RS.dbo.picking_lists pl
                LEFT JOIN Traceability_RS.dbo.picking_list_orders plo2
                       ON plo2.picking_list_id = pl.id
                LEFT JOIN Traceability_RS.dbo.order_priority op
                       ON op.order_number = plo2.order_number
                GROUP BY pl.id, pl.source_file_name, pl.status, pl.upload_date
                ORDER BY MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) ASC,
                         pl.upload_date ASC
            """)
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            logger.error("Errore caricamento picking lists: %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return

        self.lists_tree.delete(*self.lists_tree.get_children())
        for r in rows:
            prio_rank = r[6] if r[6] is not None else 4
            prio = 0 if prio_rank == 4 else int(prio_rank)
            tag = f'p{prio}' if prio in (1, 2, 3) else ''
            upload = r[3].strftime('%d/%m/%Y %H:%M') if r[3] else ''
            self.lists_tree.insert('', 'end', values=(
                r[0], PRIORITY_BADGE.get(prio, prio), r[4] or '', r[1], r[5], r[2], upload
            ), tags=(tag,))

    def _load_list_clicked(self):
        """Scelta file da T:\\KITTING (finestra se piu' di uno) e import."""
        try:
            files = kep.list_kitting_files()
        except kep.EssegiParseError as e:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                self.lang.get('kit_err_kitting_dir', 'Directory T:\\KITTING non raggiungibile')
                + f"\n{e}", parent=self)
            return
        if not files:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_msg_no_files', 'Nessun file .xlsx presente in T:\\KITTING'),
                parent=self)
            return

        if len(files) == 1:
            self._import_file(files[0]['path'])
        else:
            self._open_file_chooser(files)

    def _open_file_chooser(self, files):
        """Finestra di scelta quando in T:\\KITTING ci sono piu' file (spec §5.1.1)."""
        dlg = tk.Toplevel(self)
        dlg.title(self.lang.get('kit_choose_file_title', 'Scegli la lista di prelievo'))
        dlg.geometry("640x320")
        dlg.transient(self)
        dlg.grab_set()

        ttk.Label(dlg, text=self.lang.get(
            'kit_choose_file_msg',
            'Più file presenti in T:\\KITTING — seleziona quello corretto:'),
            padding=8).pack(anchor='w')

        cols = ('file', 'date', 'orders')
        tree = ttk.Treeview(dlg, columns=cols, show='headings', selectmode='browse')
        tree.heading('file', text=self.lang.get('kit_col_file', 'File'))
        tree.heading('date', text=self.lang.get('kit_col_file_date', 'Modificato il'))
        tree.heading('orders', text=self.lang.get('kit_col_orders', 'Ordini'))
        tree.column('file', width=220, anchor='w')
        tree.column('date', width=130, anchor='center')
        tree.column('orders', width=240, anchor='w')
        tree.pack(expand=True, fill='both', padx=8)
        for fi in files:
            tree.insert('', 'end', values=(
                fi['name'], fi['date'].strftime('%d/%m/%Y %H:%M'), fi['orders_compact']
            ))

        btns = ttk.Frame(dlg, padding=8)
        btns.pack(fill='x')

        def confirm():
            sel = tree.selection()
            if not sel:
                return
            idx = tree.index(sel[0])
            dlg.destroy()
            self._import_file(files[idx]['path'])

        tree.bind('<Double-1>', lambda e: confirm())
        ttk.Button(btns, text=self.lang.get('kit_btn_confirm', 'Conferma'),
                   command=confirm).pack(side='right')
        ttk.Button(btns, text=self.lang.get('kit_btn_cancel', 'Annulla'),
                   command=dlg.destroy).pack(side='right', padx=6)

    def _import_file(self, path):
        try:
            parsed = kep.parse_essegi_file(path)
        except kep.EssegiParseError as e:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                self.lang.get('kit_err_parse', 'File non conforme al tracciato Essegi')
                + f"\n\n{e}", parent=self)
            return

        # Guardia duplicati: stesso hash con lista non chiusa
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "SELECT id, status FROM Traceability_RS.dbo.picking_lists "
                "WHERE source_file_hash = ? AND status <> 'CLOSED'",
                (parsed.file_hash,))
            dup = cursor.fetchone()
            cursor.close()
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        if dup:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_duplicate_file',
                              'Questo file è già stato importato (lista #{id}, stato {status}).')
                .replace('{id}', str(dup[0])).replace('{status}', str(dup[1])),
                parent=self)
            return

        # Anteprima e conferma
        summary = self.lang.get('kit_import_summary',
                                'File: {file}\nOrdini: {orders}\nRighe materiale: {rows}\n'
                                'Codici distinti: {materials}')
        summary = (summary.replace('{file}', parsed.file_name)
                          .replace('{orders}', ', '.join(parsed.orders))
                          .replace('{rows}', str(len(parsed.rows)))
                          .replace('{materials}', str(len(parsed.distinct_materials))))
        if parsed.warnings:
            summary += ('\n\n' + self.lang.get('kit_import_warnings', 'Avvisi:') + '\n'
                        + '\n'.join(parsed.warnings[:10]))
            if len(parsed.warnings) > 10:
                summary += f"\n(+{len(parsed.warnings) - 10})"
        if not messagebox.askyesno(
                self.lang.get('kit_import_preview_title', 'Conferma import lista'),
                summary + '\n\n' + self.lang.get('kit_msg_proceed', 'Procedere con l\'import?'),
                parent=self):
            return

        # Insert transazionale
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO Traceability_RS.dbo.picking_lists
                    (source_file_name, source_file_path, source_file_hash,
                     source_file_date, uploaded_by, status)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, 'OPEN')
            """, (parsed.file_name, parsed.file_path, parsed.file_hash,
                  parsed.file_date, self.operator_id))
            list_id = cursor.fetchone()[0]

            for order in parsed.orders:
                cursor.execute(
                    "INSERT INTO Traceability_RS.dbo.picking_list_orders "
                    "(picking_list_id, order_number) VALUES (?, ?)",
                    (list_id, order))

            cursor.executemany(
                "INSERT INTO Traceability_RS.dbo.picking_list_items "
                "(picking_list_id, material_code, unique_number, qty_required) "
                "VALUES (?, ?, ?, ?)",
                [(list_id, r.material_code, r.unique_number, r.quantity)
                 for r in parsed.rows])

            for order in parsed.orders:
                cursor.execute("""
                    MERGE Traceability_RS.dbo.kit_status AS t
                    USING (SELECT ? AS order_number) AS s ON t.order_number = s.order_number
                    WHEN MATCHED THEN
                        UPDATE SET status = 'WH_OPEN', updated_by = ?, updated_date = GETDATE()
                    WHEN NOT MATCHED THEN
                        INSERT (order_number, status, updated_by)
                        VALUES (s.order_number, 'WH_OPEN', ?);
                """, (order, self.operator_id, self.operator_id))

            self.db.conn.commit()
            logger.info("Lista prelievo #%d importata da %s: file=%s ordini=%s righe=%d",
                        list_id, self.user_name, parsed.file_name,
                        parsed.orders, len(parsed.rows))
        except Exception as e:
            self.db.conn.rollback()
            logger.error("Errore import lista prelievo: %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return

        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_msg_import_done', 'Lista importata correttamente (#{id})')
            .replace('{id}', str(list_id)),
            parent=self)
        self._refresh_picking_lists()

    # ────────────────────── TAB RICHIESTE MATERIALE ────────────────────── #

    def _build_requests_tab(self):
        f = self.requests_frame
        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Button(top, text=self.lang.get('kit_req_btn_confirm', 'Conferma disponibilità'),
                   command=self._confirm_request).pack(side='left')
        ttk.Button(top, text=self.lang.get('kit_req_btn_cancel', 'Annulla richiesta'),
                   command=self._cancel_request).pack(side='left', padx=6)
        ttk.Button(top, text=self.lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh_requests).pack(side='left')

        cols = ('id', 'order', 'phase', 'material', 'qty', 'requester',
                'date', 'status', 'note')
        self.req_tree = ttk.Treeview(f, columns=cols, show='headings', selectmode='browse')
        headings = {
            'id': 'ID',
            'order': self.lang.get('kit_col_order', 'Ordine'),
            'phase': self.lang.get('kit_req_col_phase', 'Fase'),
            'material': self.lang.get('kit_col_material', 'Codice Materiale'),
            'qty': self.lang.get('kit_col_qty', 'Qtà'),
            'requester': self.lang.get('kit_req_col_requester', 'Richiedente'),
            'date': self.lang.get('kit_col_set_date', 'Data'),
            'status': self.lang.get('kit_col_status', 'Stato'),
            'note': self.lang.get('kit_req_note', 'Motivazione'),
        }
        widths = {'id': 45, 'order': 95, 'phase': 100, 'material': 180, 'qty': 60,
                  'requester': 150, 'date': 110, 'status': 95, 'note': 180}
        for c in cols:
            self.req_tree.heading(c, text=headings[c])
            self.req_tree.column(c, width=widths[c],
                                 anchor='w' if c in ('material', 'requester', 'note') else 'center')
        vsb = ttk.Scrollbar(f, orient='vertical', command=self.req_tree.yview)
        self.req_tree.configure(yscrollcommand=vsb.set)
        self.req_tree.pack(side='left', expand=True, fill='both')
        vsb.pack(side='left', fill='y')
        self.req_tree.tag_configure('pending', background='#fff3cd')
        self.req_tree.tag_configure('confirmed', background='#d8f5d8')

    def _refresh_requests(self):
        import kit_pf_logic as pfl
        cursor = self.db.conn.cursor()
        try:
            rows = pfl.get_requests(cursor, only_open=True)
        except Exception as e:
            logger.error("Errore caricamento richieste: %s", e)
            return
        finally:
            cursor.close()
        self.req_tree.delete(*self.req_tree.get_children())
        for r in rows:
            tag = 'pending' if r['wh_status'] == 'PENDING' else 'confirmed'
            date = r['request_date'].strftime('%d/%m %H:%M') if r['request_date'] else ''
            qty = float(r['qty'] or 0)
            self.req_tree.insert('', 'end', values=(
                r['id'], r['order_number'], r['phase'], r['material_code'],
                str(int(qty)) if qty == int(qty) else f"{qty:g}",
                r['requester'], date, r['wh_status'], r['note'] or ''), tags=(tag,))

    def _selected_request_id(self):
        sel = self.req_tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_req_msg_select', 'Seleziona una richiesta'),
                parent=self)
            return None
        return int(self.req_tree.item(sel[0])['values'][0])

    def _confirm_request(self):
        import kit_pf_logic as pfl
        req_id = self._selected_request_id()
        if req_id is None:
            return
        cursor = self.db.conn.cursor()
        try:
            ok = pfl.confirm_material_request(cursor, req_id, self.operator_id)
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        if not ok:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_req_msg_not_pending',
                              'La richiesta non è più in stato PENDING'),
                parent=self)
        else:
            logger.info("Richiesta materiale #%d confermata da %s", req_id, self.user_name)
        self._refresh_requests()

    def _cancel_request(self):
        import kit_pf_logic as pfl
        req_id = self._selected_request_id()
        if req_id is None:
            return
        reason = simpledialog.askstring(
            self.lang.get('kit_req_btn_cancel', 'Annulla richiesta'),
            self.lang.get('kit_req_msg_cancel_reason', 'Motivo annullamento (obbligatorio):'),
            parent=self)
        if not reason or not reason.strip():
            return
        cursor = self.db.conn.cursor()
        try:
            ok = pfl.cancel_material_request(cursor, req_id, self.operator_id,
                                             reason.strip())
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        if ok:
            logger.info("Richiesta materiale #%d annullata da %s: %s",
                        req_id, self.user_name, reason)
        self._refresh_requests()
