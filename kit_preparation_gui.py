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
import os
import socket
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import kit_essegi_parser as kep
import kit_notifications as notif
import kit_wh_logic
from print_label_for_production import label_needs

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

        self.requests_authorized = False
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

        if tab == 'priority':
            self.notebook.select(self.priority_frame)
        else:
            self.notebook.select(self.picking_frame)

        self._refresh_priority_list()
        self._refresh_picking_lists()
        self._refresh_requests()
        logger.info("KitPreparationWindow aperta da %s (tab=%s)", self.user_name, tab)

    def _on_tab_changed(self, event=None):
        """Il tab Richieste Materiale richiede un login autorizzato separato."""
        selected = self.notebook.select()
        if selected != str(self.requests_frame):
            return
        if self.requests_authorized:
            return
        # Torna al tab prelievo prima di chiedere il login
        self.notebook.select(self.picking_frame)

        def _authorize():
            self.requests_authorized = True
            self.notebook.select(self.requests_frame)

        try:
            self.app._execute_authorized_action('richiesta_materiali_produzione', _authorize)
        except Exception as e:
            logger.error("Errore login tab Richieste Materiale: %s", e)

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

        filter_frame = ttk.Frame(f)
        filter_frame.pack(fill='x', pady=(0, 8))
        self.only_open_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            filter_frame,
            text=self.lang.get('kit_show_only_open', 'Solo non completati'),
            variable=self.only_open_var,
            command=self._refresh_picking_lists
        ).pack(side='left', padx=(0, 12))
        ttk.Label(filter_frame,
                  text=self.lang.get('kit_search_order_product', 'Cerca ordine/prodotto:')
                  ).pack(side='left')
        self.search_list_var = tk.StringVar()
        entry = ttk.Entry(filter_frame, textvariable=self.search_list_var, width=28)
        entry.pack(side='left', padx=6)
        entry.bind('<Return>', lambda e: self._refresh_picking_lists())
        ttk.Button(filter_frame, text=self.lang.get('kit_btn_search', 'Cerca'),
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
        """Lista WH con filtro 'solo non completati' e ricerca ordine/prodotto."""
        only_open = 1 if getattr(self, 'only_open_var', None) and self.only_open_var.get() else 0
        search = self.search_list_var.get().strip() if hasattr(self, 'search_list_var') else ''
        search_active = 'Y' if search else ''
        like = f'%{search}%' if search else '%'

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
                WHERE (? = 0 OR pl.status IN ('OPEN', 'PARTIAL', 'REOPENED'))
                  AND (? = '' OR EXISTS (
                      SELECT 1
                      FROM Traceability_RS.dbo.picking_list_orders plo3
                      INNER JOIN Traceability_RS.dbo.Orders o ON o.OrderNumber = plo3.order_number
                      INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
                      WHERE plo3.picking_list_id = pl.id
                        AND (o.OrderNumber LIKE ? OR p.ProductCode LIKE ? OR p.ProductName LIKE ?)
                  ))
                GROUP BY pl.id, pl.source_file_name, pl.status, pl.upload_date
                ORDER BY MIN(CASE WHEN ISNULL(op.priority,0) = 0 THEN 4 ELSE op.priority END) ASC,
                         pl.upload_date ASC
            """, (only_open, search_active, like, like, like))
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
        """Apre il selettore file per importare una o piu' liste da T:\\KITTING."""
        self._open_file_chooser()

    def _open_file_chooser(self, include_loaded_default=False):
        """Scelta multipla di file .xlsx in T:\\KITTING con filtro e ordinamento.
        I file gia' caricati (nome con _gia_caricato_) sono nascosti di default;
        si possono mostrare con il checkbox apposito."""
        L = self.lang.get
        try:
            files = kep.list_kitting_files(include_loaded=include_loaded_default)
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

        dlg = tk.Toplevel(self)
        dlg.title(L('kit_choose_file_title', 'Scegli la lista di prelievo'))
        dlg.geometry("720x420")
        dlg.transient(self)
        dlg.grab_set()

        ttk.Label(dlg, text=L(
            'kit_choose_file_msg',
            "Seleziona uno o piu' file da importare:"),
            padding=(8, 8, 8, 0)).pack(anchor='w')

        # ── Filtro e checkbox ─────────────────────────────────────────────
        top = ttk.Frame(dlg, padding=(8, 4, 8, 0))
        top.pack(fill='x')
        ttk.Label(top, text=L('kit_filter_file', 'Filtro nome file:')).pack(side='left')
        filter_var = tk.StringVar()
        filter_entry = ttk.Entry(top, textvariable=filter_var, width=32)
        filter_entry.pack(side='left', padx=6)

        include_loaded_var = tk.BooleanVar(value=include_loaded_default)
        ttk.Checkbutton(
            top,
            text=L('kit_show_loaded_files', 'Visualizza gia'' caricati'),
            variable=include_loaded_var,
            command=lambda: refresh_files()
        ).pack(side='left', padx=(12, 0))

        self._count_var = tk.StringVar(value='')
        ttk.Label(top, textvariable=self._count_var, foreground='#666').pack(side='left', padx=6)

        cols = ('file', 'date', 'orders')
        headers = {
            'file':   L('kit_col_file', 'File'),
            'date':   L('kit_col_file_date', 'Modificato il'),
            'orders': L('kit_col_orders', 'Ordini'),
        }
        widths = {'file': 260, 'date': 150, 'orders': 240}
        tree = ttk.Treeview(dlg, columns=cols, show='headings', selectmode='extended')

        # Stato ordinamento (default: data decrescente, come l'elenco originale)
        sort_state = {'col': 'date', 'reverse': True}
        key_funcs = {
            'file':   lambda f: (f.get('name') or '').lower(),
            'date':   lambda f: f.get('date'),
            'orders': lambda f: str(f.get('orders_compact') or '').lower(),
        }

        def refresh_files():
            nonlocal files
            files = kep.list_kitting_files(include_loaded=include_loaded_var.get())
            render()

        def render(*_a):
            txt = filter_var.get().strip().lower()
            subset = [f for f in files if txt in (f.get('name') or '').lower()]
            subset.sort(key=key_funcs[sort_state['col']], reverse=sort_state['reverse'])
            tree.delete(*tree.get_children())
            for f in subset:
                tree.insert('', 'end', iid=f['path'], values=(
                    f['name'],
                    f['date'].strftime('%d/%m/%Y %H:%M') if f.get('date') else '',
                    f.get('orders_compact') or '?'))
            # Frecce di ordinamento nelle intestazioni
            for c in cols:
                arrow = (' ▼' if sort_state['reverse'] else ' ▲') if c == sort_state['col'] else ''
                tree.heading(c, text=headers[c] + arrow)
            self._count_var.set(L('kit_file_count', '{n} file').format(n=len(subset)))

        def sort_by(c):
            if sort_state['col'] == c:
                sort_state['reverse'] = not sort_state['reverse']
            else:
                sort_state['col'] = c
                sort_state['reverse'] = (c == 'date')  # data: default desc; testo: asc
            render()

        for c in cols:
            tree.heading(c, text=headers[c], command=lambda cc=c: sort_by(cc))
            tree.column(c, width=widths[c], anchor='center' if c == 'date' else 'w')

        def confirm():
            sel = tree.selection()
            if not sel:
                return
            paths = list(sel)
            dlg.destroy()
            self._import_selected_files(paths)

        # Barra pulsanti in basso
        btns = ttk.Frame(dlg, padding=8)
        btns.pack(side='bottom', fill='x')
        ttk.Button(btns, text=L('kit_btn_confirm', 'Conferma'),
                   command=confirm).pack(side='right')
        ttk.Button(btns, text=L('kit_btn_cancel', 'Annulla'),
                   command=dlg.destroy).pack(side='right', padx=6)

        vsb = ttk.Scrollbar(dlg, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y', pady=(6, 0))
        tree.pack(side='left', expand=True, fill='both', padx=(8, 0), pady=(6, 0))

        tree.bind('<Double-1>', lambda e: confirm())
        filter_var.trace_add('write', render)
        render()
        filter_entry.focus_set()

    def _import_selected_files(self, paths):
        """Importa in sequenza i file selezionati e li rinomina dopo il successo."""
        if not paths:
            return
        imported = 0
        for path in paths:
            if self._import_file(path):
                imported += 1
                self._rename_loaded_file(path)
        if imported:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_msg_imported_n', 'Importati {n} file.')
                .replace('{n}', str(imported)),
                parent=self)
        self._refresh_picking_lists()

    def _rename_loaded_file(self, path):
        """Rinomina il file aggiungendo _gia_caricato_gg_mm_YYYY prima dell'estensione."""
        directory, filename = os.path.split(path)
        name, ext = os.path.splitext(filename)
        suffix = datetime.now().strftime('%d_%m_%Y')
        new_name = f"{name}_gia_caricato_{suffix}{ext}"
        new_path = os.path.join(directory, new_name)
        try:
            os.rename(path, new_path)
            logger.info('File rinominato dopo import: %s -> %s', path, new_path)
            return new_path
        except Exception as e:
            logger.error('Errore rinomina file %s: %s', path, e)
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_warn_rename_failed',
                              'Import completato ma impossibile rinominare il file:\\n{path}\\n{e}')
                .replace('{path}', path).replace('{e}', str(e)),
                parent=self)
            return None

    def _parse_with_mapping(self, path):
        """Parsa il file usando il dizionario colonne (dbo.KitColumnAliases).
        Se una colonna non è mappata, apre la maschera di mappatura (stesso login
        della pagina); se l'operatore salva la mappatura, riprova. Ritorna
        l'oggetto EssegiFile oppure None (errore/annullo)."""
        import kit_column_dict
        L = self.lang.get
        try:
            column_dict = kit_column_dict.load_aliases(self.db.conn)
        except Exception as e:
            logger.warning("Kit: dizionario colonne non caricato dal DB (%s), uso i default", e)
            column_dict = None

        for _attempt in range(4):   # max 4 passaggi (un campo mancante per volta)
            try:
                return kep.parse_essegi_file(path, column_dict)
            except kep.UnmappedColumnsError as e:
                import kit_column_mapping_gui
                try:
                    self.grab_release()
                except Exception:
                    pass
                try:
                    saved = kit_column_mapping_gui.open_column_mapping(
                        self, self.db, self.lang, e,
                        __import__('os').path.basename(path), self.user_name)
                finally:
                    try:
                        self.grab_set()
                    except Exception:
                        pass
                if not saved:
                    return None  # operatore ha annullato la mappatura
                # ricarica il dizionario aggiornato e riprova
                try:
                    column_dict = kit_column_dict.load_aliases(self.db.conn)
                except Exception:
                    pass
            except kep.EssegiParseError as e:
                messagebox.showerror(
                    L('error_title', 'Errore'),
                    L('kit_err_parse', 'File non conforme al tracciato di kitting')
                    + f"\n\n{e}", parent=self)
                return None

        messagebox.showerror(
            L('error_title', 'Errore'),
            L('kit_err_map_giveup', 'Impossibile mappare tutte le colonne del file.'),
            parent=self)
        return None

    def _exclude_smt_and_empty(self, parsed):
        """Esclude dalle righe da importare:
          - le righe SENZA reel code (codice unico) — belt-and-suspenders, il
            parser le salta già;
          - i codici SMT, cioè quelli la cui descrizione in dbo.Components contiene
            'SMT' (componenti SMT, non pertinenti ai kit PTH).
        Aggiunge un riepilogo agli avvisi mostrati in anteprima."""
        rows = parsed.rows
        n_empty = sum(1 for r in rows if not (r.unique_number or '').strip())
        rows = [r for r in rows if (r.unique_number or '').strip()]

        smt_codes = set()
        codes = sorted({r.material_code for r in rows if r.material_code})
        if codes:
            try:
                cur = self.db.conn.cursor()
                CHUNK = 1000  # limite parametri per IN (max 2100 in SQL Server)
                for i in range(0, len(codes), CHUNK):
                    chunk = codes[i:i + CHUNK]
                    ph = ','.join('?' * len(chunk))
                    cur.execute(
                        "SELECT ComponentCode FROM Traceability_RS.dbo.Components "
                        f"WHERE ComponentDescription LIKE '%SMT%' AND ComponentCode IN ({ph})",
                        chunk)
                    smt_codes.update(r[0] for r in cur.fetchall())
                cur.close()
            except Exception as e:
                logger.warning("Kit import: filtro SMT non applicato (%s)", e)

        n_smt = sum(1 for r in rows if r.material_code in smt_codes)
        rows = [r for r in rows if r.material_code not in smt_codes]
        parsed.rows = rows
        if n_smt or n_empty:
            parsed.warnings.append(
                self.lang.get('kit_excluded_summary',
                              'Escluse {smt} righe SMT e {empty} righe senza reel code.')
                .replace('{smt}', str(n_smt)).replace('{empty}', str(n_empty)))
        logger.info("Kit import: escluse %d SMT + %d senza reel (rimaste %d righe)",
                    n_smt, n_empty, len(rows))

    def _import_file(self, path):
        """Importa un singolo file .xlsx. Ritorna True se ha successo, False altrimenti."""
        parsed = self._parse_with_mapping(path)
        if parsed is None:
            return False

        # Escludi righe SMT (descrizione Components contiene 'SMT') e senza reel code
        self._exclude_smt_and_empty(parsed)
        if not parsed.rows:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_all_excluded',
                              'Nessuna riga valida da importare dopo l\'esclusione dei codici '
                              'SMT e delle righe senza reel code.'),
                parent=self)
            return False

        # Guardia duplicati: stesso file (hash) gia' importato, QUALSIASI stato
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "SELECT TOP 1 id, status FROM Traceability_RS.dbo.picking_lists "
                "WHERE source_file_hash = ? ORDER BY id DESC",
                (parsed.file_hash,))
            dup = cursor.fetchone()
            cursor.close()
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return False
        if dup:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_duplicate_file',
                              'Questo file è già stato caricato ed elaborato (lista #{id}, stato {status}).\n'
                              'Per non sovrascrivere il lavoro di verifica già fatto, '
                              'il ri-caricamento è bloccato.')
                .replace('{id}', str(dup[0])).replace('{status}', str(dup[1])),
                parent=self)
            return False

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
            return False

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

            # --- righe etichetta automatiche (non bloccanti) ---
            try:
                self._add_label_rows_to_list(list_id, parsed.orders)
            except Exception as e:
                logger.error("Errore righe etichetta per lista %s: %s", list_id, e)
        except Exception as e:
            self.db.conn.rollback()
            logger.error("Errore import lista prelievo: %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return False

        return True

    def _add_label_rows_to_list(self, list_id, order_numbers):
        """Calcola e inserisce righe etichetta automatiche per gli ordini della lista."""
        if not order_numbers:
            return
        import json
        cursor = self.db.conn.cursor()
        try:
            kit_wh_logic.ensure_label_columns(self.db.conn)
            placeholders = ','.join('?' * len(order_numbers))
            cursor.execute(f"""
                SELECT o.OrderNumber, o.IDOrder, o.OrderQuantity, p.IDProduct, p.ProductCode, p.ProductName
                FROM Traceability_RS.dbo.Orders o
                JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
                WHERE o.OrderNumber IN ({placeholders})
            """, list(order_numbers))
            orders = []
            for r in cursor.fetchall():
                orders.append({
                    'IDOrder': r[1],
                    'OrderNumber': r[0],
                    'OrderQuantity': r[2],
                    'IDProduct': r[3],
                    'ProductCode': r[4],
                    'ProductName': r[5],
                })
            product_ids = [o['IDProduct'] for o in orders if o['IDProduct']]
            if not product_ids:
                return
            product_labels = label_needs.fetch_product_labels(cursor, product_ids)
            if not product_labels:
                return
            label_ids = [pl['LabelId'] for pl in product_labels]
            params = label_needs.fetch_label_parameters(cursor, label_ids)
            needs = label_needs.calculate_label_needs(orders, product_labels, params)
            aggregated = label_needs.aggregate_by_label(needs)
            for agg in aggregated:
                request_data = {
                    'orders': agg['Orders'],
                    'qty_net': agg['QtyNet'],
                    'qty_scarto': agg['QtyScarto'],
                    'qty_total': agg['QtyTotal'],
                }
                notes = f"Etichetta automatica per {len(agg['Orders'])} ordini"
                cursor.execute("""
                    INSERT INTO Traceability_RS.dbo.picking_list_items
                        (picking_list_id, material_code, qty_required, pick_status, notes, Source, LabelRequestData)
                    VALUES (?, ?, ?, 'PENDING', ?, 'LABEL', ?)
                """, (list_id, agg['MaterialCode'], agg['QtyTotal'], notes, json.dumps(request_data, default=str)))
            self.db.conn.commit()
        except Exception:
            self.db.conn.rollback()
            raise
        finally:
            cursor.close()

    # ────────────────────── TAB RICHIESTE MATERIALE ────────────────────── #

    def _build_requests_tab(self):
        f = self.requests_frame
        top = ttk.Frame(f)
        top.pack(fill='x', pady=(0, 8))
        ttk.Button(top, text=self.lang.get('kit_req_btn_new', 'Nuova richiesta'),
                   command=self._new_request).pack(side='left')
        ttk.Button(top, text=self.lang.get('kit_req_btn_confirm', 'Conferma disponibilità'),
                   command=self._confirm_request).pack(side='left', padx=(6, 0))
        ttk.Button(top, text=self.lang.get('kit_req_btn_cancel', 'Annulla richiesta'),
                   command=self._cancel_request).pack(side='left', padx=6)
        ttk.Button(top, text=self.lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh_requests).pack(side='left')

        cols = ('id', 'order', 'phase', 'material', 'qty', 'reason', 'requester',
                'date', 'status', 'note')
        self.req_tree = ttk.Treeview(f, columns=cols, show='headings', selectmode='browse')
        headings = {
            'id': 'ID',
            'order': self.lang.get('kit_col_order', 'Ordine'),
            'phase': self.lang.get('kit_req_col_phase', 'Fase'),
            'material': self.lang.get('kit_col_material', 'Codice Materiale'),
            'qty': self.lang.get('kit_col_qty', 'Qtà'),
            'reason': self.lang.get('kit_req_col_reason', 'Motivo'),
            'requester': self.lang.get('kit_req_col_requester', 'Richiedente'),
            'date': self.lang.get('kit_col_set_date', 'Data'),
            'status': self.lang.get('kit_col_status', 'Stato'),
            'note': self.lang.get('kit_req_note', 'Motivazione'),
        }
        widths = {'id': 45, 'order': 95, 'phase': 100, 'material': 180, 'qty': 60,
                  'reason': 130, 'requester': 150, 'date': 110, 'status': 95, 'note': 160}
        for c in cols:
            self.req_tree.heading(c, text=headings[c])
            self.req_tree.column(c, width=widths[c],
                                 anchor='w' if c in ('material', 'requester', 'note', 'reason') else 'center')
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
                self._reason_label(r.get('reason')),
                r['requester'], date, r['wh_status'], r['note'] or ''), tags=(tag,))

    def _reason_label(self, code):
        """Etichetta tradotta di una motivazione (codice REQUEST_REASONS)."""
        if not code:
            return ''
        return self.lang.get('kit_req_reason_' + str(code).lower(), str(code))

    # ─────────────── Nuova richiesta materiale (produzione) ─────────────── #

    def _new_request(self):
        """Gate di autorizzazione: la richiesta materiale richiede un login
        autorizzato (chiave 'richiedi_materiale_kit'). Chi autorizza e' il
        richiedente registrato sulla richiesta."""
        app = self.app

        def run():
            # Richiedente = utente che ha appena autorizzato
            uid = getattr(app, '_temp_authorized_user_id', None)
            name = getattr(app, 'last_authenticated_user_name', None) or self.user_name
            hhid = self.operator_id
            if uid is not None:
                try:
                    hhid = self.db.get_employee_hire_history_id(uid) or self.operator_id
                except Exception as e:
                    logger.warning("Nuova richiesta: hire history id non risolto: %s", e)
            self._new_request_dialog(hhid, name)

        if hasattr(app, '_execute_authorized_action'):
            # grab_release/set intorno al login modale, come per gli altri
            # login in-form (l'app apre la propria LoginWindow).
            try:
                self.grab_release()
            except Exception:
                pass
            try:
                app._execute_authorized_action(
                    menu_translation_key='richiedi_materiale_kit',
                    action_callback=run)
            finally:
                try:
                    self.grab_set()
                except Exception:
                    pass
        else:
            # Fallback (es. test / apertura senza app autorizzante)
            run()

    def _new_request_dialog(self, requested_by, requester_name):
        """Dialog per creare una richiesta materiale per ordine + materiale
        verificato nelle liste di prelievo, con motivazione strutturata.
        requested_by/requester_name = utente autorizzato (vedi _new_request)."""
        import kit_pf_logic as pfl
        L = self.lang.get

        cursor = self.db.conn.cursor()
        try:
            orders = pfl.get_verified_orders(cursor)
        except Exception as e:
            logger.error("Nuova richiesta: caricamento ordini fallito: %s", e)
            messagebox.showerror(L('error_title', 'Errore'),
                                 f"{L('kit_req_orders_err', 'Impossibile caricare gli ordini')}: {e}",
                                 parent=self)
            return
        finally:
            cursor.close()

        if not orders:
            messagebox.showinfo(
                L('info_title', 'Informazione'),
                L('kit_req_no_orders',
                  'Nessun ordine verificato nelle liste di prelievo: non ci sono '
                  'ordini su cui richiedere materiale.'), parent=self)
            return

        dlg = tk.Toplevel(self)
        dlg.title(L('kit_req_btn_new', 'Nuova richiesta'))
        dlg.geometry('480x360')
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()
        fr = ttk.Frame(dlg, padding=14)
        fr.pack(fill='both', expand=True)

        # Ordine (dagli ordini verificati)
        ttk.Label(fr, text=L('kit_col_order', 'Ordine') + ':').grid(row=0, column=0, sticky='w', pady=5)
        order_cb = ttk.Combobox(fr, state='readonly', width=28, values=orders)
        order_cb.current(0)
        order_cb.grid(row=0, column=1, sticky='w', pady=5)

        # Materiale (componenti verificati dell'ordine scelto)
        ttk.Label(fr, text=L('kit_col_material', 'Codice Materiale') + ':').grid(row=1, column=0, sticky='w', pady=5)
        mat_cb = ttk.Combobox(fr, width=28)
        mat_cb.grid(row=1, column=1, sticky='w', pady=5)
        mat_hint = ttk.Label(fr, text='', foreground='gray')
        mat_hint.grid(row=2, column=1, sticky='w')

        self._req_materials = []   # dict material_code/qty_required/qty_picked

        def load_materials(_e=None):
            cur = self.db.conn.cursor()
            try:
                self._req_materials = pfl.get_order_materials(cur, order_cb.get())
            except Exception as ex:
                logger.error("Nuova richiesta: materiali fallito: %s", ex)
                self._req_materials = []
            finally:
                cur.close()
            codes = [m['material_code'] for m in self._req_materials]
            mat_cb['values'] = codes
            mat_cb.set('')
            mat_hint.config(text=L('kit_req_mat_count', '{n} materiali').format(n=len(codes)))

        def on_mat_typed(_e=None):
            txt = mat_cb.get().strip().lower()
            allc = [m['material_code'] for m in self._req_materials]
            mat_cb['values'] = [c for c in allc if txt in c.lower()] if txt else allc

        order_cb.bind('<<ComboboxSelected>>', load_materials)
        mat_cb.bind('<KeyRelease>', on_mat_typed)
        load_materials()

        # Quantità
        ttk.Label(fr, text=L('kit_req_qty', 'Quantità') + ':').grid(row=3, column=0, sticky='w', pady=5)
        qty_var = tk.StringVar()
        ttk.Entry(fr, textvariable=qty_var, width=12).grid(row=3, column=1, sticky='w', pady=5)

        # Fase richiedente
        ttk.Label(fr, text=L('kit_req_col_phase', 'Fase') + ':').grid(row=4, column=0, sticky='w', pady=5)
        phase_map = {'PREFORMING': L('kit_phase_preforming', 'Preforming'),
                     'PRODUCTION': L('kit_phase_production', 'Produzione')}
        phase_cb = ttk.Combobox(fr, state='readonly', width=20,
                                values=list(phase_map.values()))
        phase_cb.current(1)   # default Produzione
        phase_cb.grid(row=4, column=1, sticky='w', pady=5)

        # Motivazione (categorie fisse)
        ttk.Label(fr, text=L('kit_req_col_reason', 'Motivo') + ':').grid(row=5, column=0, sticky='w', pady=5)
        reason_map = {code: self._reason_label(code) for code in pfl.REQUEST_REASONS}
        reason_cb = ttk.Combobox(fr, state='readonly', width=28,
                                 values=list(reason_map.values()))
        reason_cb.current(0)
        reason_cb.grid(row=5, column=1, sticky='w', pady=5)

        # Nota libera (facoltativa)
        ttk.Label(fr, text=L('kit_req_note', 'Motivazione') + ':').grid(row=6, column=0, sticky='nw', pady=5)
        note_txt = tk.Text(fr, width=30, height=3)
        note_txt.grid(row=6, column=1, sticky='w', pady=5)

        def submit():
            order = order_cb.get().strip()
            material = mat_cb.get().strip()
            if not order or not material:
                messagebox.showwarning(L('warning_title', 'Attenzione'),
                                       L('kit_req_msg_required',
                                         'Ordine e codice materiale sono obbligatori'), parent=dlg)
                return
            try:
                qty = float(qty_var.get().strip().replace(',', '.'))
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(L('warning_title', 'Attenzione'),
                                       L('kit_err_qty', 'Quantità non valida'), parent=dlg)
                return
            # Risolve fase e motivo dai rispettivi combo
            phase = next((k for k, v in phase_map.items() if v == phase_cb.get()), 'PRODUCTION')
            reason = next((k for k, v in reason_map.items() if v == reason_cb.get()), None)
            note = note_txt.get('1.0', 'end').strip()

            cur = self.db.conn.cursor()
            try:
                result = pfl.create_material_request(
                    cur, order, phase, material, qty, requested_by,
                    requester_name, note, socket.gethostname(), reason=reason)
                self.db.conn.commit()
            except Exception as ex:
                self.db.conn.rollback()
                messagebox.showerror(L('error_title', 'Errore'), str(ex), parent=dlg)
                return
            finally:
                cur.close()
            try:
                msgs = result['messages']
                notif.send_kit_email_async(self.db.conn, msgs['subject'], msgs['body'])
            except Exception as ex:
                logger.warning("Nuova richiesta #%s: email non inviata: %s",
                               result.get('request_id'), ex)
            logger.info("Richiesta materiale #%s creata da %s (%s x %s, motivo %s)",
                        result.get('request_id'), requester_name, qty, material, reason)
            dlg.destroy()
            self._refresh_requests()

        bar = ttk.Frame(fr)
        bar.grid(row=7, column=0, columnspan=2, sticky='e', pady=(12, 0))
        ttk.Button(bar, text=L('button_cancel', 'Annulla'), command=dlg.destroy).pack(side='right')
        ttk.Button(bar, text=L('kit_req_btn_send', 'Invia richiesta'),
                   command=submit).pack(side='right', padx=(0, 8))
        fr.columnconfigure(1, weight=1)

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
