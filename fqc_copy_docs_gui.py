# -*- coding: utf-8 -*-
"""
fqc_copy_docs_gui.py
Copy documentation (active checklist items) between products of the same client.

Entry point (called from FqcMasterForm):
    open_fqc_copy_docs(parent, db, lang, user_name)

DB schema: Traceability_RS / chk
    chk.ProductCheckLists          - checklist header
    chk.ProductCheckListDatas      - checklist items (varbinary PictureToCheck)
    chk.ProductCheckListCopyLogs   - copy audit log (created if missing)
"""
from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from fqc_products_gui import (
    _C_ACCENT, _C_BG, _C_BORDER, _C_CARD, _C_ERROR, _C_HEADER,
    _C_SUBTEXT, _C_SUCCESS, _C_TEXT, _C_WARNING,
    _ClientProductMixin,
    _Q_ACTIVE_CHECKLIST,
    _Q_CHECKLIST_ITEMS,
    _Q_CLIENTS,
    _Q_CREATE_CHECKLIST,
    _Q_INSERT_ITEM,
    _Q_PRODUCTS_FOR_CLIENT,
    _btn, _card, _combo, _logo_label,
)

logger = logging.getLogger("TraceabilityRS")

# ── SQL Queries ───────────────────────────────────────────────────────────────

# Products of a client that have an ACTIVE checklist (DateOut IS NULL)
_Q_SRC_PRODUCTS = """
SELECT p.IDProduct, p.ProductCode, cl.ProductCheckListId, cl.CheckListName
FROM   Products p
INNER JOIN [Traceability_RS].[chk].[ProductCheckLists] cl
       ON  cl.IdProduct = p.IDProduct
WHERE  p.IDClient = ?
  AND  cl.DateOut IS NULL
ORDER BY p.ProductCode
"""

# Does the destination product already have a checklist with this name?
_Q_CHECKLIST_NAME_EXISTS = """
SELECT COUNT(*)
FROM   [Traceability_RS].[chk].[ProductCheckLists]
WHERE  IdProduct = ? AND CheckListName = ?
"""

# Next ItemToCheckNumber for appending items (contiguous from MAX+1)
_Q_NEXT_COPY_NUM = """
SELECT ISNULL(MAX(ItemToCheckNumber), 0) + 1
FROM   [Traceability_RS].[chk].[ProductCheckListDatas]
WHERE  ProductCheckListId = ? AND DateOut IS NULL
"""

_Q_INSERT_COPY_LOG = """
INSERT INTO [Traceability_RS].[chk].[ProductCheckListCopyLogs]
    (IdProductSource, IdProductDest, CheckListSourceId, CheckListDestId,
     ItemsCopied, CopiedBy)
VALUES (?, ?, ?, ?, ?, ?)
"""

# Copy history for a destination product (source product code resolved via join)
_Q_COPY_HISTORY = """
SELECT l.CopyLogId, l.CopiedWhen, ps.ProductCode, l.CopiedBy, l.ItemsCopied
FROM   [Traceability_RS].[chk].[ProductCheckListCopyLogs] l
LEFT JOIN Products ps ON ps.IDProduct = l.IdProductSource
WHERE  l.IdProductDest = ?
ORDER BY l.CopiedWhen DESC
"""

_DDL_ENSURE_COPY_LOG_TABLE = """
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'chk')
BEGIN
    EXEC('CREATE SCHEMA chk')
END

IF OBJECT_ID(N'[Traceability_RS].[chk].[ProductCheckListCopyLogs]', N'U') IS NULL
BEGIN
    CREATE TABLE [Traceability_RS].[chk].[ProductCheckListCopyLogs]
    (
        CopyLogId INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_ProductCheckListCopyLogs PRIMARY KEY,
        IdProductSource INT NOT NULL,
        IdProductDest   INT NOT NULL,
        CheckListSourceId INT NOT NULL,
        CheckListDestId   INT NOT NULL,
        ItemsCopied   INT NOT NULL,
        CopiedBy      NVARCHAR(100) NOT NULL,
        CopiedWhen    DATETIME NOT NULL
            CONSTRAINT DF_ProductCheckListCopyLogs_CopiedWhen DEFAULT (GETDATE())
    );

    CREATE INDEX IX_ProductCheckListCopyLogs_Dest
        ON [Traceability_RS].[chk].[ProductCheckListCopyLogs](IdProductDest, CopiedWhen DESC);
END
"""


def _ensure_copy_log_schema(db) -> None:
    """Ensure the copy-log table exists (idempotent DDL)."""
    cur = None
    try:
        cur = db.conn.cursor()
        cur.execute(_DDL_ENSURE_COPY_LOG_TABLE)
        db.conn.commit()
    except Exception as exc:
        logger.error(f"_ensure_copy_log_schema: {exc}", exc_info=True)
        raise
    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  FqcCopyDocsForm                                                           ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class FqcCopyDocsForm(_ClientProductMixin, tk.Toplevel):
    """Copy selected checklist items (documentation) from a source product to a
    destination product of the same client, logging each copy."""

    def __init__(self, parent, db, lang, user_name: str):
        tk.Toplevel.__init__(self, parent)
        self.db        = db
        self.lang      = lang
        self.user_name = user_name
        self._master   = parent
        self._init_cp_state()
        self._src_map:        dict[str, dict] = {}   # display -> {id_product, checklist_id, checklist_name}
        self._all_sources:    list[str]      = []
        self._src_items:      list[dict]     = []    # {'checked', 'num', 'desc', 'photo'}
        self._id_dest:        Optional[int]  = None

        self.title(self.lang.get('fqc_copy_docs_title', 'FQC — Copy Documentation'))
        self.configure(bg=_C_BG)
        self.resizable(True, True)
        self.grab_set()
        self._build_ui()
        self._load_clients()
        self.after(120, lambda: self._center(880, 680))

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        hdr = tk.Frame(self, bg=_C_HEADER)
        hdr.pack(fill=tk.X)
        logo = _logo_label(hdr, _C_HEADER)
        if logo:
            logo.pack(side=tk.LEFT, padx=12, pady=8)
        tk.Label(hdr,
                 text=self.lang.get('fqc_copy_docs_title', 'FQC — Copy Documentation'),
                 bg=_C_HEADER, fg='#fff',
                 font=('Segoe UI', 13, 'bold')).pack(side=tk.LEFT, pady=8, padx=8)

        body = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        body.pack(fill=tk.BOTH, expand=True)

        # ── Selection card ────────────────────────────────────────────────────
        _, sel = _card(body, self.lang.get('fqc_selection', 'PRODUCT SELECTION'))
        g = tk.Frame(sel, bg=_C_CARD)
        g.pack(fill=tk.X)

        tk.Label(g, text=self.lang.get('fqc_client', 'Client:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=18, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
        self._client_combo = _combo(g, 44)
        self._client_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        self._client_combo.bind('<<ComboboxSelected>>', self._on_client_selected)
        self._client_combo.bind('<KeyRelease>',         self._on_client_filter)

        tk.Label(g, text=self.lang.get('fqc_copy_source', 'Source product (with checklist):'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=18, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, pady=2)
        self._src_combo = _combo(g, 44)
        self._src_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        self._src_combo['state'] = 'disabled'
        self._src_combo.bind('<<ComboboxSelected>>', self._on_source_selected)
        self._src_combo.bind('<KeyRelease>',         self._on_source_filter)

        tk.Label(g, text=self.lang.get('fqc_copy_dest', 'Destination product:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=18, anchor=tk.W).grid(row=2, column=0, sticky=tk.W, pady=2)
        self._dest_combo = _combo(g, 44)
        self._dest_combo.grid(row=2, column=1, sticky=tk.W, pady=2)
        self._dest_combo['state'] = 'disabled'
        self._dest_combo.bind('<<ComboboxSelected>>', self._on_dest_selected)
        self._dest_combo.bind('<KeyRelease>',         self._on_dest_filter)

        # ── Items card ────────────────────────────────────────────────────────
        _, items_card = _card(body,
                              self.lang.get('fqc_copy_items_section', 'DOCUMENTATION TO COPY'))
        tv_wrap = tk.Frame(items_card, bg=_C_CARD)
        tv_wrap.pack(fill=tk.BOTH, expand=True)
        cols = ('chk', 'num', 'desc')
        self._tv = ttk.Treeview(tv_wrap, columns=cols, show='headings',
                                height=8, selectmode='browse')
        for col, lbl, w in [
            ('chk',  self.lang.get('fqc_copy_col_sel', '✓'), 36),
            ('num',  self.lang.get('fqc_copy_col_num', '#'),  56),
            ('desc', self.lang.get('fqc_col_desc', 'Description'), 560),
        ]:
            self._tv.heading(col, text=lbl)
            self._tv.column(col, width=w, anchor=tk.W)
        vsb = ttk.Scrollbar(tv_wrap, orient='vertical', command=self._tv.yview)
        self._tv.configure(yscrollcommand=vsb.set)
        self._tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.bind('<ButtonRelease-1>', self._on_item_click)

        item_btns = tk.Frame(items_card, bg=_C_CARD)
        item_btns.pack(fill=tk.X, pady=(4, 0))
        _btn(item_btns, self.lang.get('fqc_copy_select_all', 'Select all'),
             self._select_all, _C_HEADER).pack(side=tk.LEFT, padx=2)
        _btn(item_btns, self.lang.get('fqc_copy_select_none', 'Deselect all'),
             self._select_none, _C_BORDER, fg=_C_TEXT).pack(side=tk.LEFT, padx=2)

        # ── History card ──────────────────────────────────────────────────────
        _, hist_card = _card(body, self.lang.get('fqc_copy_history',
                                                 'COPY HISTORY ON DESTINATION PRODUCT'))
        cols_h = ('when', 'from', 'user', 'items')
        self._hist_tv = ttk.Treeview(hist_card, columns=cols_h, show='headings',
                                     height=4, selectmode='browse')
        for col, lbl, w in [
            ('when',  self.lang.get('fqc_copy_hist_when',  'When'),     140),
            ('from',  self.lang.get('fqc_copy_hist_from',  'From'),     180),
            ('user',  self.lang.get('fqc_copy_hist_user',  'User'),     120),
            ('items', self.lang.get('fqc_copy_hist_items', 'N° items'), 80),
        ]:
            self._hist_tv.heading(col, text=lbl)
            self._hist_tv.column(col, width=w, anchor=tk.W)
        hsb = ttk.Scrollbar(hist_card, orient='vertical', command=self._hist_tv.yview)
        self._hist_tv.configure(yscrollcommand=hsb.set)
        self._hist_tv.pack(side=tk.LEFT, fill=tk.X, expand=True)
        hsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._hist_empty = tk.Label(hist_card, text='', bg=_C_CARD, fg=_C_SUBTEXT,
                                    font=('Segoe UI', 9, 'italic'))
        self._hist_empty.pack(anchor=tk.W, pady=2)

        # ── Footer ────────────────────────────────────────────────────────────
        foot = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        foot.pack(fill=tk.X)
        _btn(foot, self.lang.get('fqc_copy_do_copy', '📋 Copy selected documentation'),
             self._do_copy, _C_SUCCESS).pack(side=tk.LEFT)
        _btn(foot, self.lang.get('close', 'Close'), self.destroy,
             bg=_C_BORDER, fg=_C_TEXT).pack(side=tk.RIGHT)

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_products(self, id_client: int):
        """Loads source products (with active checklist) and destination products
        (all products of the client). Overrides the mixin method."""
        cur = None
        try:
            cur = self.db.conn.cursor()
            # Destination: all products of the client
            cur.execute(_Q_PRODUCTS_FOR_CLIENT, (id_client,))
            rows = cur.fetchall()
            self._product_map  = {r[1]: r[0] for r in rows}
            self._all_products = [r[1] for r in rows]
            self._dest_combo['values'] = self._all_products
            self._dest_combo['state']  = 'normal'
            self._dest_combo.set('')
            self._id_dest = None
            # Source: products with an active checklist
            cur.execute(_Q_SRC_PRODUCTS, (id_client,))
            self._src_map     = {}
            self._all_sources = []
            for r in cur.fetchall():
                disp = f'{r[1]} — {r[3]}'
                self._src_map[disp] = {
                    'id_product':     r[0],
                    'checklist_id':   r[2],
                    'checklist_name': r[3],
                }
                self._all_sources.append(disp)
            self._src_combo['values'] = self._all_sources
            self._src_combo['state']  = 'normal'
            self._src_combo.set('')
            self._clear_items()
            self._clear_history()
        except Exception as exc:
            logger.error(f"FqcCopyDocsForm _load_products: {exc}", exc_info=True)
        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass

    def _on_source_selected(self, event=None):
        disp = self._src_combo.get()
        src = self._src_map.get(disp)
        self._clear_items()
        if not src:
            return
        cur = None
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_CHECKLIST_ITEMS, (src['checklist_id'],))
            self._src_items = [
                {'checked': True, 'num': r[2], 'desc': r[1], 'photo': bytes(r[3]) if r[3] else b''}
                for r in cur.fetchall()
            ]
            for i, it in enumerate(self._src_items):
                self._tv.insert('', 'end', iid=str(i),
                                values=('☑', it['num'], it['desc'][:90]))
        except Exception as exc:
            logger.error(f"FqcCopyDocsForm _on_source_selected: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)
        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass

    def _on_dest_selected(self, event=None):
        code = self._dest_combo.get()
        self._id_dest = self._product_map.get(code)
        self._load_history()

    def _load_history(self):
        self._clear_history()
        if not self._id_dest:
            return
        cur = None
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_COPY_HISTORY, (self._id_dest,))
            rows = cur.fetchall()
            if not rows:
                self._hist_empty.config(
                    text=self.lang.get('fqc_copy_no_history', 'No previous copies on this product.'))
                return
            self._hist_empty.config(text='')
            for r in rows:
                dt = r[1].strftime('%d/%m/%Y %H:%M') if r[1] else ''
                self._hist_tv.insert('', 'end', iid=str(r[0]),
                                     values=(dt, r[2] or '?', r[3] or '', r[4]))
        except Exception as exc:
            logger.error(f"FqcCopyDocsForm _load_history: {exc}", exc_info=True)
        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass

    def _clear_items(self):
        self._src_items = []
        if hasattr(self, '_tv'):
            for row in self._tv.get_children():
                self._tv.delete(row)

    def _clear_history(self):
        if hasattr(self, '_hist_tv'):
            for row in self._hist_tv.get_children():
                self._hist_tv.delete(row)
        if hasattr(self, '_hist_empty'):
            self._hist_empty.config(text='')

    # ── Filtering (source / destination combos) ───────────────────────────────

    def _on_source_filter(self, event=None):
        typed = self._src_combo.get().upper()
        self._src_combo['values'] = (
            [s for s in self._all_sources if typed in s.upper()] or self._all_sources
        )

    def _on_dest_filter(self, event=None):
        typed = self._dest_combo.get().upper()
        self._dest_combo['values'] = (
            [p for p in self._all_products if typed in p.upper()] or self._all_products
        )

    # ── Checkbox toggling ─────────────────────────────────────────────────────

    def _on_item_click(self, event=None):
        row = self._tv.identify_row(event.y)
        if not row:
            return
        idx = int(row)
        if 0 <= idx < len(self._src_items):
            self._src_items[idx]['checked'] = not self._src_items[idx]['checked']
            self._update_item_row(idx)

    def _update_item_row(self, idx: int):
        it = self._src_items[idx]
        self._tv.item(str(idx),
                      values=('☑' if it['checked'] else '☐', it['num'], it['desc'][:90]))

    def _select_all(self):
        for i, it in enumerate(self._src_items):
            if not it['checked']:
                it['checked'] = True
                self._update_item_row(i)

    def _select_none(self):
        for i, it in enumerate(self._src_items):
            if it['checked']:
                it['checked'] = False
                self._update_item_row(i)

    # ── Copy execution ────────────────────────────────────────────────────────

    def _do_copy(self):
        disp = self._src_combo.get()
        src = self._src_map.get(disp)
        if not src:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_copy_err_select_source',
                              'Select a source product with an active checklist.'),
                parent=self)
            return
        dest_code = self._dest_combo.get()
        id_dest = self._product_map.get(dest_code)
        if not id_dest:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_copy_err_select_dest', 'Select a destination product.'),
                parent=self)
            return
        if src['id_product'] == id_dest:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_copy_err_same_product',
                              'Source and destination products must be different.'),
                parent=self)
            return
        selected = [it for it in self._src_items if it['checked']]
        if not selected:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_copy_err_no_items', 'Select at least one item to copy.'),
                parent=self)
            return

        # Peek destination active checklist + new checklist name for the confirm dialog
        cur = None
        dest_cl_id = None
        new_cl_name = None
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_ACTIVE_CHECKLIST, (id_dest,))
            row = cur.fetchone()
            if row:
                dest_cl_id = row[0]
            else:
                name = src['checklist_name']
                cur.execute(_Q_CHECKLIST_NAME_EXISTS, (id_dest, name))
                if cur.fetchone()[0] > 0:
                    name = f'{name} (copia)'
                new_cl_name = name
        except Exception as exc:
            logger.error(f"FqcCopyDocsForm _do_copy (preflight): {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)
            return
        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass

        msg = self.lang.get(
            'fqc_copy_confirm_msg',
            'Copy {n} item(s) from "{src}" to "{dst}"?').format(
                n=len(selected), src=disp, dst=dest_code)
        if new_cl_name:
            msg += '\n' + self.lang.get(
                'fqc_copy_new_cl_msg', 'A new checklist will be created: {name}').format(
                    name=new_cl_name)
        if not messagebox.askyesno(self.lang.get('confirm', 'Confirm'), msg, parent=self):
            return

        cur = None
        try:
            cur = self.db.conn.cursor()
            # Destination checklist: reuse active or create new
            if dest_cl_id:
                cl_dest = dest_cl_id
            else:
                cur.execute(_Q_CREATE_CHECKLIST, (new_cl_name, id_dest))
                cur.execute('SELECT @@IDENTITY')
                cl_dest = int(cur.fetchone()[0])
            # Append items: ItemToCheckNumber continues from MAX(active)+1
            cur.execute(_Q_NEXT_COPY_NUM, (cl_dest,))
            next_n = cur.fetchone()[0]
            for it in selected:
                cur.execute(_Q_INSERT_ITEM,
                            (cl_dest, it['desc'], next_n, it['photo']))
                next_n += 1
            # Audit log in the same transaction
            cur.execute(_Q_INSERT_COPY_LOG,
                        (src['id_product'], id_dest, src['checklist_id'], cl_dest,
                         len(selected), self.user_name))
            self.db.conn.commit()
        except Exception as exc:
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            logger.error(f"FqcCopyDocsForm _do_copy: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)
            return
        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass

        messagebox.showinfo(
            self.lang.get('success', 'Success'),
            self.lang.get('fqc_copy_success', 'Documentation copied successfully.'),
            parent=self)
        self._load_history()
        # Refresh the master form if it is showing the destination product
        try:
            if getattr(self._master, '_id_product', None) == id_dest:
                self._master._load_checklist()
        except Exception as exc:
            logger.debug(f"FqcCopyDocsForm parent refresh: {exc}")


# ── Public API ────────────────────────────────────────────────────────────────

def open_fqc_copy_docs(parent, db, lang, user_name: str):
    """Opens the copy-documentation form."""
    _ensure_copy_log_schema(db)
    form = FqcCopyDocsForm(parent, db, lang, user_name)
    parent.wait_window(form)
    try:
        if parent.winfo_exists():
            parent.grab_set()
    except Exception:
        pass
