# -*- coding: utf-8 -*-
"""
fqc_products_gui.py
FQC (Final Quality Control) Products module.

Entry points (called from main.py):
    open_fqc_execution(parent, db, lang, user_name)
    open_fqc_master(parent, db, lang, user_name)
    open_fqc_feedback(parent, db, lang, user_name)

DB schema: Traceability_RS / chk
    chk.ProductCheckLists          - checklist header
    chk.ProductCheckListDatas      - checklist items  (varbinary PictureToCheck)
    chk.ProductCheckListDataLogs   - execution log
    chk.ProductCheckListDataLogFeedBacks - customer feedback
"""
from __future__ import annotations

import datetime
import io
import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional

logger = logging.getLogger("TraceabilityRS")

try:
    from PIL import Image, ImageTk
    _PIL_OK = True
except ImportError:
    _PIL_OK = False
    logger.warning("PIL not available — FQC images will not be displayed")

# ── Colour tokens (consistent with project style) ─────────────────────────────
_C_HEADER  = '#1f3864'
_C_ACCENT  = '#2e86de'
_C_SUCCESS = '#27ae60'
_C_ERROR   = '#e74c3c'
_C_WARNING = '#f39c12'
_C_BG      = '#f4f6f8'
_C_CARD    = '#ffffff'
_C_BORDER  = '#dde1e7'
_C_TEXT    = '#2c3e50'
_C_SUBTEXT = '#7f8c8d'
_C_OK_ROW  = '#eafaf1'
_C_NOK_ROW = '#fdf2f8'

# ── SQL Queries ───────────────────────────────────────────────────────────────

_Q_CLIENTS = """
SELECT IDClient, ClientName
FROM   Clients
WHERE  isClient = 1
ORDER  BY ClientName
"""

_Q_PRODUCTS_FOR_CLIENT = """
SELECT IDProduct, ProductCode
FROM   Products
WHERE  IDClient = ?
ORDER  BY ProductCode
"""

_Q_LABELCODE_INFO = """
SELECT TOP 1
    l.IDLabelCode,
    l.LabelCod,
    o.IDOrder,
    o.OrderNumber,
    p.IDProduct,
    p.ProductCode,
    c.IDClient,
    c.ClientName
FROM Traceability_RS.dbo.LabelCodes l
INNER JOIN Traceability_RS.dbo.Boards   b ON b.IDBoard   = l.IDBoard
INNER JOIN Traceability_RS.dbo.Orders   o ON o.IDOrder   = b.IDOrder
INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
LEFT JOIN  Traceability_RS.dbo.Clients  c ON c.IDClient  = p.IDClient
WHERE l.LabelCod = ?
ORDER BY l.IDLabelCode DESC
"""

# Products processed in PTHM (IDPhase=107) in the current production day
# (window 07:30 today → 07:30 tomorrow).  Used to highlight / pre-filter.
_Q_PTHM_TODAY = """
SELECT DISTINCT
    p.IDProduct,
    p.ProductCode
FROM Traceability_rs.dbo.Scannings                sc
INNER JOIN Traceability_rs.dbo.OrderPhases         op  ON sc.IDOrderPhase = op.IDOrderPhase
INNER JOIN Traceability_rs.dbo.Orders              o   ON op.IDOrder      = o.IDOrder
INNER JOIN Traceability_rs.dbo.Phases              ph  ON op.IDPhase      = ph.IDPhase
INNER JOIN Traceability_rs.dbo.Products            p   ON o.IDProduct     = p.IDProduct
INNER JOIN Traceability_rs.dbo.Boards              b   ON b.IDBoard       = sc.IDBoard
WHERE
    ph.IDPhase IN (107)
    AND sc.ScanTimeFinish BETWEEN
        CAST(CAST(GETDATE() AS DATE) AS DATETIME) + CAST('07:30:00' AS DATETIME)
        AND
        CAST(CAST(GETDATE() + 1 AS DATE) AS DATETIME) + CAST('07:30:00' AS DATETIME)
GROUP BY p.IDProduct, p.ProductCode
ORDER BY p.ProductCode
"""

_Q_ACTIVE_CHECKLIST = """
SELECT TOP 1
    ProductCheckListId, CheckListName, DateIn
FROM [Traceability_RS].[chk].[ProductCheckLists]
WHERE IdProduct = ? AND DateOut IS NULL
ORDER BY DateIn DESC
"""

_Q_CHECKLIST_ITEMS = """
SELECT ProductCheckListDataId, ItemToCheck, ItemToCheckNumber, PictureToCheck
FROM   [Traceability_RS].[chk].[ProductCheckListDatas]
WHERE  ProductCheckListId = ? AND DateOut IS NULL
ORDER  BY ItemToCheckNumber
"""

_Q_INSERT_LOG = """
INSERT INTO [Traceability_RS].[chk].[ProductCheckListDataLogs]
    (ProductCheckListDataId, IsOK, DateCheckList, [User], NotOkNote)
VALUES (?, ?, GETDATE(), ?, ?)
"""

_Q_UPSERT_LABEL_LOG = """
IF EXISTS (
    SELECT 1
    FROM [Traceability_RS].[chk].[ProductCheckListDataLabelLogs]
    WHERE IDLabelCode = ? AND ProductCheckListDataId = ?
)
BEGIN
    UPDATE [Traceability_RS].[chk].[ProductCheckListDataLabelLogs]
    SET IsOK = ?,
        DateCheckList = GETDATE(),
        [User] = ?,
        NotOkNote = ?,
        DateSys = GETDATE()
    WHERE IDLabelCode = ?
      AND ProductCheckListDataId = ?
END
ELSE
BEGIN
    INSERT INTO [Traceability_RS].[chk].[ProductCheckListDataLabelLogs]
        (ProductCheckListDataId, IDLabelCode, IsOK, DateCheckList, [User], NotOkNote, DateSys)
    VALUES (?, ?, ?, GETDATE(), ?, ?, GETDATE())
END
"""

_Q_LABEL_LOGS = """
SELECT ProductCheckListDataId, IsOK, NotOkNote
FROM [Traceability_RS].[chk].[ProductCheckListDataLabelLogs]
WHERE IDLabelCode = ?
"""

_Q_CREATE_CHECKLIST = """
INSERT INTO [Traceability_RS].[chk].[ProductCheckLists]
    (CheckListName, IdProduct, DateIn)
VALUES (?, ?, GETDATE())
"""

_Q_RENAME_CHECKLIST = """
UPDATE [Traceability_RS].[chk].[ProductCheckLists]
SET    CheckListName = ?
WHERE  ProductCheckListId = ?
"""

_Q_NEXT_ITEM_NUM = """
SELECT ISNULL(MAX(ItemToCheckNumber), 0) + 10
FROM   [Traceability_RS].[chk].[ProductCheckListDatas]
WHERE  ProductCheckListId = ? AND DateOut IS NULL
"""

_Q_INSERT_ITEM = """
INSERT INTO [Traceability_RS].[chk].[ProductCheckListDatas]
    (ProductCheckListId, ItemToCheck, ItemToCheckNumber, PictureToCheck, DateSys)
VALUES (?, ?, ?, ?, GETDATE())
"""

_Q_UPDATE_ITEM = """
UPDATE [Traceability_RS].[chk].[ProductCheckListDatas]
SET    ItemToCheck = ?, PictureToCheck = ?
WHERE  ProductCheckListDataId = ?
"""

_Q_DELETE_ITEM = """
UPDATE [Traceability_RS].[chk].[ProductCheckListDatas]
SET    DateOut = GETDATE()
WHERE  ProductCheckListDataId = ?
"""

_Q_LOAD_ITEM = """
SELECT ItemToCheck, PictureToCheck
FROM   [Traceability_RS].[chk].[ProductCheckListDatas]
WHERE  ProductCheckListDataId = ?
"""

_Q_NOK_LOGS = """
SELECT
    l.ProductCheckListDataLogId,
    d.ItemToCheckNumber,
    d.ItemToCheck,
    l.[User],
    l.DateCheckList,
    l.NotOkNote
FROM [Traceability_RS].[chk].[ProductCheckListDataLogs]   l
INNER JOIN [Traceability_RS].[chk].[ProductCheckListDatas] d
       ON  l.ProductCheckListDataId = d.ProductCheckListDataId
INNER JOIN [Traceability_RS].[chk].[ProductCheckLists]     cl
       ON  d.ProductCheckListId = cl.ProductCheckListId
WHERE cl.IdProduct = ? AND l.IsOK = 0
ORDER BY l.DateCheckList DESC
"""

_Q_INSERT_FEEDBACK = """
INSERT INTO [Traceability_RS].[chk].[ProductCheckListDataLogFeedBacks]
    (ProductCheckListDataLogId, FeedBack, FeedBackPicture,
     FeedBackDate, FeedBackFrom, DateSys)
VALUES (?, ?, ?, ?, ?, GETDATE())
"""

_DDL_ENSURE_LABEL_LOG_TABLE = """
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'chk')
BEGIN
    EXEC('CREATE SCHEMA chk')
END

IF OBJECT_ID(N'[Traceability_RS].[chk].[ProductCheckListDataLabelLogs]', N'U') IS NULL
BEGIN
    CREATE TABLE [Traceability_RS].[chk].[ProductCheckListDataLabelLogs]
    (
        ProductCheckListDataLabelLogId BIGINT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_ProductCheckListDataLabelLogs PRIMARY KEY,
        ProductCheckListDataId INT NOT NULL,
        IDLabelCode INT NOT NULL,
        IsOK BIT NOT NULL,
        DateCheckList DATETIME NOT NULL
            CONSTRAINT DF_ProductCheckListDataLabelLogs_DateCheckList DEFAULT (GETDATE()),
        [User] NVARCHAR(100) NOT NULL,
        NotOkNote NVARCHAR(1000) NULL,
        DateSys DATETIME NOT NULL
            CONSTRAINT DF_ProductCheckListDataLabelLogs_DateSys DEFAULT (GETDATE())
    );

    CREATE UNIQUE INDEX UX_ProductCheckListDataLabelLogs_Label_Item
        ON [Traceability_RS].[chk].[ProductCheckListDataLabelLogs](IDLabelCode, ProductCheckListDataId);

    CREATE INDEX IX_ProductCheckListDataLabelLogs_Label
        ON [Traceability_RS].[chk].[ProductCheckListDataLabelLogs](IDLabelCode, DateCheckList DESC);
END
"""

# ── Image utilities ───────────────────────────────────────────────────────────

def _bytes_to_photo(data, max_size=(80, 80)) -> Optional[object]:
    """Convert varbinary bytes → Tkinter PhotoImage. Returns None on failure."""
    if not data or not _PIL_OK:
        return None
    try:
        img = Image.open(io.BytesIO(bytes(data)))
        img.thumbnail(max_size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as exc:
        logger.debug(f"_bytes_to_photo: {exc}")
        return None


def _file_to_bytes(path: str) -> Optional[bytes]:
    """Read image file → bytes."""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as exc:
        logger.error(f"_file_to_bytes {path}: {exc}")
        return None


def _logo_label(parent, bg: str) -> Optional[tk.Label]:
    logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    if not os.path.isfile(logo_path) or not _PIL_OK:
        return None
    try:
        img = Image.open(logo_path)
        img.thumbnail((110, 44), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(parent, image=photo, bg=bg)
        lbl._photo = photo          # keep reference
        return lbl
    except Exception:
        return None

# ── Shared UI helpers ─────────────────────────────────────────────────────────

def _card(parent, title: str):
    """Returns inner_frame of a white card with section header."""
    outer = tk.Frame(parent, bg=_C_BORDER)
    outer.pack(fill=tk.X, pady=4)
    inner = tk.Frame(outer, bg=_C_CARD, padx=12, pady=8)
    inner.pack(fill=tk.X, padx=1, pady=1)
    tk.Label(inner, text=title, bg=_C_CARD, fg=_C_HEADER,
             font=('Segoe UI', 8, 'bold')).pack(anchor=tk.W)
    tk.Frame(inner, bg=_C_BORDER, height=1).pack(fill=tk.X, pady=(2, 6))
    return outer, inner


def _btn(parent, text, cmd, bg=_C_ACCENT, fg='#ffffff', width=None):
    kwargs = dict(text=text, bg=bg, fg=fg, activebackground=bg,
                  font=('Segoe UI', 9, 'bold'), relief=tk.FLAT,
                  padx=10, pady=4, cursor='hand2', command=cmd)
    if width:
        kwargs['width'] = width
    return tk.Button(parent, **kwargs)


def _combo(parent, width=38):
    cb = ttk.Combobox(parent, width=width, font=('Segoe UI', 10))
    cb['state'] = 'normal'
    return cb


def _entry(parent, textvariable, width=36):
    return tk.Entry(parent, textvariable=textvariable, font=('Segoe UI', 10),
                    width=width, relief=tk.FLAT,
                    highlightbackground=_C_BORDER,
                    highlightcolor=_C_ACCENT,
                    highlightthickness=1)


def _ensure_fqc_labelcode_schema(db) -> None:
    """Ensure the labelcode-specific FQC persistence table exists."""
    try:
        cur = db.conn.cursor()
        cur.execute(_DDL_ENSURE_LABEL_LOG_TABLE)
        db.conn.commit()
    except Exception as exc:
        logger.error(f"_ensure_fqc_labelcode_schema: {exc}", exc_info=True)
        raise
    finally:
        try:
            cur.close()
        except Exception:
            pass

# ── Client/Product selection mixin ────────────────────────────────────────────

class _ClientProductMixin:
    """Reusable client+product combo logic shared by all three forms."""

    def _init_cp_state(self):
        self._client_map:   dict[str, int] = {}
        self._product_map:  dict[str, int] = {}
        self._all_clients:  list[str]      = []
        self._all_products: list[str]      = []

    def _load_clients(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_CLIENTS)
            rows = cur.fetchall()
            self._client_map  = {r[1]: r[0] for r in rows}
            self._all_clients = [r[1] for r in rows]
            self._client_combo['values'] = self._all_clients
        except Exception as exc:
            logger.error(f"{type(self).__name__} _load_clients: {exc}")

    def _on_client_filter(self, event=None):
        typed = self._client_combo.get().upper()
        self._client_combo['values'] = (
            [c for c in self._all_clients if typed in c.upper()] or self._all_clients
        )

    def _on_client_selected(self, event=None):
        name      = self._client_combo.get()
        id_client = self._client_map.get(name)
        if id_client:
            self._load_products(id_client)

    def _load_products(self, id_client: int):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_PRODUCTS_FOR_CLIENT, (id_client,))
            rows = cur.fetchall()
            self._product_map  = {r[1]: r[0] for r in rows}
            self._all_products = [r[1] for r in rows]
            self._product_combo['values'] = self._all_products
            self._product_combo['state']  = 'normal'
            self._product_combo.set('')
        except Exception as exc:
            logger.error(f"{type(self).__name__} _load_products: {exc}")

    def _on_product_filter(self, event=None):
        typed = self._product_combo.get().upper()
        self._product_combo['values'] = (
            [p for p in self._all_products if typed in p.upper()] or self._all_products
        )

    def _build_cp_grid(self, parent):
        """Build client + product combo rows inside `parent`."""
        g = tk.Frame(parent, bg=_C_CARD)
        g.pack(fill=tk.X)

        tk.Label(g, text=self.lang.get('fqc_client', 'Client:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=10, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
        self._client_combo = _combo(g, 42)
        self._client_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        self._client_combo.bind('<<ComboboxSelected>>', self._on_client_selected)
        self._client_combo.bind('<KeyRelease>',         self._on_client_filter)

        tk.Label(g, text=self.lang.get('fqc_product', 'Product:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=10, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, pady=2)
        self._product_combo = _combo(g, 42)
        self._product_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        self._product_combo['state'] = 'disabled'
        self._product_combo.bind('<<ComboboxSelected>>', self._on_product_selected)
        self._product_combo.bind('<KeyRelease>',         self._on_product_filter)

    def _center(self, min_w=820, min_h=600):
        self.update_idletasks()
        w  = max(self.winfo_width(),  min_w)
        h  = max(self.winfo_height(), min_h)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f'{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}')


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  FqcExecutionForm  —  operator checklist execution                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class FqcExecutionForm(_ClientProductMixin, tk.Toplevel):
    """Operator fills OK/NOK for each checklist item and saves the log."""

    def __init__(self, parent, db, lang, user_name: str):
        tk.Toplevel.__init__(self, parent)
        self.db        = db
        self.lang      = lang
        self.user_name = user_name
        self._init_cp_state()
        self._checklist_id: Optional[int] = None
        self._items:        list[dict]    = []
        self._photo_refs:   list          = []   # keep PhotoImage refs alive
        self._pthm_ids:     set           = set()  # IDProduct processed in PTHM today
        self._selected_product_id: Optional[int] = None
        self._current_label_info: Optional[dict] = None
        self._labelcode_var = tk.StringVar()
        self._labelcode_validated = False

        self.title(self.lang.get('fqc_exec_title', 'FQC Products — Checklist Execution'))
        self.configure(bg=_C_BG)
        self.resizable(True, True)
        self.grab_set()
        self._build_ui()
        self._load_pthm_today()       # load PTHM products before clients
        self._load_clients()
        self.after(120, lambda: self._center(850, 640))

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=_C_HEADER)
        hdr.pack(fill=tk.X)
        logo = _logo_label(hdr, _C_HEADER)
        if logo:
            logo.pack(side=tk.LEFT, padx=12, pady=8)
        ttl = tk.Frame(hdr, bg=_C_HEADER)
        ttl.pack(side=tk.LEFT, pady=8)
        tk.Label(ttl,
                 text=self.lang.get('fqc_exec_title', 'FQC Products — Checklist Execution'),
                 bg=_C_HEADER, fg='#fff', font=('Segoe UI', 13, 'bold')).pack(anchor=tk.W)
        tk.Label(ttl,
                 text=f"{self.lang.get('fqc_operator', 'Operator')}: {self.user_name}",
                 bg=_C_HEADER, fg='#a8c4e0', font=('Segoe UI', 9)).pack(anchor=tk.W)

        # Body
        body = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        body.pack(fill=tk.BOTH, expand=True)

        # Selection card
        _, sel = _card(body, self.lang.get('fqc_selection', 'PRODUCT SELECTION'))
        self._build_cp_grid(sel)

        label_row = tk.Frame(sel, bg=_C_CARD)
        label_row.pack(fill=tk.X, pady=(8, 0))
        tk.Label(
            label_row,
            text=self.lang.get('fqc_labelcode', 'LabelCode:'),
            bg=_C_CARD,
            fg=_C_TEXT,
            font=('Segoe UI', 9),
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        self._labelcode_entry = _entry(label_row, self._labelcode_var, 30)
        self._labelcode_entry.pack(side=tk.LEFT, padx=(0, 6))
        self._labelcode_entry.bind('<Return>', self._validate_labelcode)
        _btn(
            label_row,
            self.lang.get('fqc_verify_labelcode', 'Verify'),
            self._validate_labelcode,
            bg=_C_HEADER,
            width=10
        ).pack(side=tk.LEFT)

        # PTHM badge
        self._pthm_badge = tk.Label(
            sel,
            text='',
            bg=_C_CARD, fg=_C_ACCENT,
            font=('Segoe UI', 8, 'italic')
        )
        self._pthm_badge.pack(anchor=tk.W, pady=(0, 2))

        self._labelcode_status = tk.Label(
            sel,
            text='',
            bg=_C_CARD,
            fg=_C_SUBTEXT,
            font=('Segoe UI', 9, 'italic'),
            justify=tk.LEFT,
            wraplength=760
        )
        self._labelcode_status.pack(anchor=tk.W, pady=(4, 0))

        self._cl_status = tk.Label(sel, text='', bg=_C_CARD, fg=_C_SUBTEXT,
                                   font=('Segoe UI', 9, 'italic'))
        self._cl_status.pack(anchor=tk.W, pady=(4, 0))

        # Checklist card
        _, cl_card = _card(body, self.lang.get('fqc_checklist', 'CHECKLIST'))

        # Scrollable canvas
        self._canvas = tk.Canvas(cl_card, bg=_C_BG, highlightthickness=0, height=370)
        vsb = ttk.Scrollbar(cl_card, orient='vertical', command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._scroll_frame = tk.Frame(self._canvas, bg=_C_BG)
        self._win_id = self._canvas.create_window((0, 0), window=self._scroll_frame,
                                                  anchor='nw')
        self._scroll_frame.bind('<Configure>',
                                lambda e: self._canvas.configure(
                                    scrollregion=self._canvas.bbox('all')))
        self._canvas.bind('<Configure>',
                          lambda e: self._canvas.itemconfig(self._win_id, width=e.width))
        self._canvas.bind('<MouseWheel>',
                          lambda e: self._canvas.yview_scroll(
                              int(-1 * (e.delta / 120)), 'units'))

        self._no_items_lbl = tk.Label(self._scroll_frame,
                                      text=self.lang.get('fqc_select_product',
                                                         'Select a client and product to load the checklist.'),
                                      bg=_C_BG, fg=_C_SUBTEXT,
                                      font=('Segoe UI', 10, 'italic'))
        self._no_items_lbl.pack(pady=30)

        # Footer buttons
        foot = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        foot.pack(fill=tk.X)
        self._save_btn = _btn(foot,
                              self.lang.get('fqc_save_checklist', '✔ Save Results'),
                              self._on_save, _C_SUCCESS)
        self._save_btn.pack(side=tk.LEFT)
        self._save_btn.config(state='disabled')

        close = _btn(foot, self.lang.get('close', 'Close'), self.destroy,
                     bg=_C_BORDER, fg=_C_TEXT)
        close.pack(side=tk.RIGHT)

    # ── PTHM products ─────────────────────────────────────────────────────────

    def _load_pthm_today(self):
        """Load products processed in PTHM (IDPhase=107) during the current production day."""
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_PTHM_TODAY)
            rows = cur.fetchall()
            self._pthm_ids = {r[0] for r in rows}
        except Exception as exc:
            logger.warning(f"FqcExecutionForm _load_pthm_today: {exc}")
            self._pthm_ids = set()

    # ── Product selection callback ─────────────────────────────────────────────

    def _load_products(self, id_client: int):
        """Override: build product list, PTHM products first (prefixed with ★)."""
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_PRODUCTS_FOR_CLIENT, (id_client,))
            rows = cur.fetchall()   # (IDProduct, ProductCode)

            self._product_map  = {}
            self._all_products = []

            pthm_items  = []
            other_items = []
            for pid, code in rows:
                if pid in self._pthm_ids:
                    pthm_items.append((pid, code))
                else:
                    other_items.append((pid, code))

            # ★ PTHM items at the top, then the rest alphabetically
            for pid, code in sorted(pthm_items, key=lambda x: x[1]):
                label = f'\u2605 {code}'   # ★ prefix
                self._product_map[label] = pid
                self._product_map[code]  = pid   # also accessible without prefix
                self._all_products.append(label)

            for pid, code in sorted(other_items, key=lambda x: x[1]):
                self._product_map[code] = pid
                self._all_products.append(code)

            self._product_combo['values'] = self._all_products
            self._product_combo['state']  = 'normal'
            self._product_combo.set('')

            n_pthm = len(pthm_items)
            if n_pthm > 0:
                self._pthm_badge.config(
                    text=self.lang.get('fqc_pthm_hint',
                                       f'\u2605 = {n_pthm} product(s) processed in PTHM today').replace(
                        '{n}', str(n_pthm))
                )
            else:
                self._pthm_badge.config(text='')
        except Exception as exc:
            logger.error(f"FqcExecutionForm _load_products: {exc}")

    def _on_product_filter(self, event=None):
        """Override: search ignores ★ prefix."""
        typed = self._product_combo.get().upper().lstrip('\u2605').strip()
        self._product_combo['values'] = (
            [p for p in self._all_products if typed in p.upper()] or self._all_products
        )

    def _on_product_selected(self, event=None):
        raw = self._product_combo.get()
        # Strip ★ prefix before map lookup
        code       = raw.lstrip('\u2605').strip()
        id_product = self._product_map.get(raw) or self._product_map.get(code)
        if id_product:
            self._selected_product_id = id_product
            self._invalidate_labelcode_if_mismatch()
            self._load_checklist(id_product)

    def _on_client_selected(self, event=None):
        super()._on_client_selected(event)
        self._selected_product_id = None
        self._reset_labelcode_validation(clear_entry=False)

    def _reset_labelcode_validation(self, clear_entry: bool = False):
        self._labelcode_validated = False
        self._current_label_info = None
        if clear_entry:
            self._labelcode_var.set('')
        self._labelcode_status.config(text='', fg=_C_SUBTEXT)

    def _invalidate_labelcode_if_mismatch(self):
        if not self._labelcode_validated or not self._current_label_info:
            return
        current_product = self._current_label_info.get('IDProduct')
        if current_product and self._selected_product_id and current_product != self._selected_product_id:
            self._labelcode_validated = False
            self._labelcode_status.config(
                text=self.lang.get(
                    'fqc_labelcode_product_mismatch',
                    'LabelCode no longer matches the selected product. Verify again.'
                ),
                fg=_C_WARNING
            )

    def _find_product_display_value(self, product_id: int, product_code: str) -> str:
        for value in self._all_products:
            code = value.lstrip('\u2605').strip()
            if self._product_map.get(value) == product_id or code == product_code:
                return value
        return product_code

    def _apply_label_selection(self, label_info: dict):
        client_name = label_info.get('ClientName') or ''
        product_code = label_info.get('ProductCode') or ''
        id_client = label_info.get('IDClient')
        id_product = label_info.get('IDProduct')

        if id_client and client_name:
            self._client_combo.set(client_name)
            self._load_products(id_client)

        if id_product:
            display_value = self._find_product_display_value(id_product, product_code)
            self._product_combo.set(display_value)
            self._selected_product_id = id_product
            self._load_checklist(id_product)

    def _fetch_saved_label_results(self, id_labelcode: int) -> dict[int, dict]:
        saved: dict[int, dict] = {}
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_LABEL_LOGS, (id_labelcode,))
            for row in cur.fetchall():
                saved[int(row[0])] = {
                    'is_ok': int(row[1]),
                    'note': row[2] or ''
                }
        except Exception as exc:
            logger.error(f"_fetch_saved_label_results: {exc}", exc_info=True)
        finally:
            try:
                cur.close()
            except Exception:
                pass
        return saved

    def _validate_labelcode(self, event=None):
        labelcode_value = self._labelcode_var.get().strip()
        if not labelcode_value:
            self._labelcode_status.config(
                text=self.lang.get('fqc_labelcode_required', 'Enter a LabelCode.'),
                fg=_C_WARNING
            )
            self._labelcode_validated = False
            return

        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_LABELCODE_INFO, (labelcode_value,))
            row = cur.fetchone()
        except Exception as exc:
            logger.error(f"_validate_labelcode: {exc}", exc_info=True)
            self._labelcode_status.config(text=str(exc), fg=_C_ERROR)
            self._labelcode_validated = False
            return
        finally:
            try:
                cur.close()
            except Exception:
                pass

        if not row:
            self._labelcode_status.config(
                text=self.lang.get('fqc_labelcode_not_found', 'LabelCode not found in database.'),
                fg=_C_ERROR
            )
            self._labelcode_validated = False
            self._current_label_info = None
            return

        label_info = {
            'IDLabelCode': row[0],
            'LabelCod': row[1],
            'IDOrder': row[2],
            'OrderNumber': row[3],
            'IDProduct': row[4],
            'ProductCode': row[5],
            'IDClient': row[6],
            'ClientName': row[7],
        }

        selected_raw = self._product_combo.get().strip()
        if selected_raw:
            selected_code = selected_raw.lstrip('\u2605').strip()
            selected_product_id = self._product_map.get(selected_raw) or self._product_map.get(selected_code)
            if selected_product_id and selected_product_id != label_info['IDProduct']:
                self._labelcode_status.config(
                    text=(
                        f"{self.lang.get('fqc_labelcode_mismatch', 'LabelCode belongs to a different product.')}: "
                        f"{label_info['OrderNumber']} / {label_info['ProductCode']}"
                    ),
                    fg=_C_ERROR
                )
                self._labelcode_validated = False
                self._current_label_info = label_info
                return

        self._current_label_info = label_info
        self._labelcode_validated = True
        self._apply_label_selection(label_info)
        self._labelcode_status.config(
            text=(
                f"✅ {label_info['OrderNumber']} / {label_info['ProductCode']}"
                + (f" / {label_info['ClientName']}" if label_info.get('ClientName') else '')
            ),
            fg=_C_SUCCESS
        )

    def _load_checklist(self, id_product: int):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_ACTIVE_CHECKLIST, (id_product,))
            cl = cur.fetchone()
            if not cl:
                self._checklist_id = None
                self._cl_status.config(
                    text=self.lang.get('fqc_no_checklist',
                                       '⚠ No active checklist for this product.'),
                    fg=_C_ERROR)
                self._clear_items()
                return
            self._checklist_id = cl[0]
            date_str = cl[2].strftime('%d/%m/%Y') if cl[2] else ''
            self._cl_status.config(text=f'✅  {cl[1]}  ({date_str})', fg=_C_SUCCESS)

            cur.execute(_Q_CHECKLIST_ITEMS, (self._checklist_id,))
            raw = [{'id': r[0], 'desc': r[1], 'num': r[2], 'photo': r[3]}
                   for r in cur.fetchall()]
            saved_results = {}
            if self._labelcode_validated and self._current_label_info:
                saved_results = self._fetch_saved_label_results(self._current_label_info['IDLabelCode'])
            self._render_items(raw, saved_results)
        except Exception as exc:
            logger.error(f"FqcExecutionForm _load_checklist: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)

    # ── Item rendering ────────────────────────────────────────────────────────

    def _clear_items(self):
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        self._items     = []
        self._photo_refs = []
        self._save_btn.config(state='disabled')
        self._no_items_lbl = tk.Label(self._scroll_frame,
                                      text=self.lang.get('fqc_no_checklist',
                                                         '⚠ No active checklist for this product.'),
                                      bg=_C_BG, fg=_C_ERROR,
                                      font=('Segoe UI', 10, 'italic'))
        self._no_items_lbl.pack(pady=30)

    def _render_items(self, raw: list[dict], saved_results: Optional[dict[int, dict]] = None):
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        self._items      = []
        self._photo_refs = []
        saved_results = saved_results or {}

        # Column header bar
        hbar = tk.Frame(self._scroll_frame, bg=_C_HEADER)
        hbar.pack(fill=tk.X)
        for txt, w in [('#', 4), (self.lang.get('fqc_col_desc', 'Description'), 34),
                       (self.lang.get('fqc_col_photo', 'Photo'), 12),
                       ('OK', 6), ('NOK', 6),
                       (self.lang.get('fqc_col_note', 'Note (required if NOK)'), 30)]:
            tk.Label(hbar, text=txt, bg=_C_HEADER, fg='#fff',
                     font=('Segoe UI', 8, 'bold'), width=w,
                     anchor=tk.W).pack(side=tk.LEFT, padx=4, pady=4)

        for i, rd in enumerate(raw):
            item = {
                'data_id':  rd['id'],
                'number':   rd['num'],
                'ok_var':   tk.IntVar(value=-1),
                'note_var': tk.StringVar(),
            }
            row_bg = _C_CARD if i % 2 == 0 else '#f0f4f8'
            row = tk.Frame(self._scroll_frame, bg=row_bg,
                           highlightbackground=_C_BORDER, highlightthickness=1)
            row.pack(fill=tk.X, pady=1)

            # Number
            tk.Label(row, text=str(rd['num']), bg=row_bg, fg=_C_TEXT,
                     font=('Segoe UI', 9, 'bold'), width=4,
                     anchor=tk.CENTER).pack(side=tk.LEFT, padx=4, pady=6)

            # Description
            tk.Label(row, text=rd['desc'], bg=row_bg, fg=_C_TEXT,
                     font=('Segoe UI', 9), wraplength=240, justify=tk.LEFT,
                     width=34, anchor=tk.W).pack(side=tk.LEFT, padx=4)

            # Thumbnail
            photo = _bytes_to_photo(rd['photo'], (80, 64))
            if photo:
                self._photo_refs.append(photo)
                img_lbl = tk.Label(row, image=photo, bg=row_bg, cursor='hand2')
                img_lbl.bind('<Button-1>',
                             lambda e, d=rd['photo']: self._show_full_image(d))
            else:
                img_lbl = tk.Label(row, text='—', bg=row_bg, fg=_C_SUBTEXT,
                                   font=('Segoe UI', 8), width=10)
            img_lbl.pack(side=tk.LEFT, padx=4)

            # Note entry (always present; disabled until NOK selected)
            note_entry = _entry(row, item['note_var'], 28)
            note_entry.config(state='disabled', bg='#eeeeee')
            item['note_entry'] = note_entry
            item['row_frame']  = row

            # OK / NOK radio buttons
            tk.Radiobutton(
                row, text='OK', variable=item['ok_var'], value=1,
                bg=row_bg, fg=_C_SUCCESS, font=('Segoe UI', 9, 'bold'),
                activebackground=row_bg, selectcolor=row_bg,
                command=lambda it=item: self._on_ok(it)
            ).pack(side=tk.LEFT, padx=6)

            tk.Radiobutton(
                row, text='NOK', variable=item['ok_var'], value=0,
                bg=row_bg, fg=_C_ERROR, font=('Segoe UI', 9, 'bold'),
                activebackground=row_bg, selectcolor=row_bg,
                command=lambda it=item: self._on_nok(it)
            ).pack(side=tk.LEFT, padx=2)

            note_entry.pack(side=tk.LEFT, padx=8)
            self._items.append(item)

            saved_item = saved_results.get(rd['id'])
            if saved_item is not None:
                item['ok_var'].set(1 if saved_item.get('is_ok') else 0)
                item['note_var'].set(saved_item.get('note', ''))
                if saved_item.get('is_ok'):
                    self._on_ok(item)
                else:
                    self._on_nok(item)

        if self._items:
            self._save_btn.config(state='normal')

    def _on_ok(self, item: dict):
        item['row_frame'].config(bg=_C_OK_ROW)
        item['note_entry'].config(state='disabled', bg='#eeeeee')
        item['note_var'].set('')

    def _on_nok(self, item: dict):
        item['row_frame'].config(bg=_C_NOK_ROW)
        item['note_entry'].config(state='normal',
                                  bg=_C_CARD,
                                  highlightbackground=_C_ERROR,
                                  highlightthickness=1)
        item['note_entry'].focus_set()

    def _show_full_image(self, data):
        if not data or not _PIL_OK:
            return
        try:
            img   = Image.open(io.BytesIO(bytes(data)))
            img.thumbnail((640, 640), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            pop   = tk.Toplevel(self)
            pop.title(self.lang.get('fqc_photo_preview', 'Photo Preview'))
            pop.configure(bg='#000')
            lbl = tk.Label(pop, image=photo, bg='#000')
            lbl.image = photo
            lbl.pack()
            pop.bind('<Escape>',    lambda e: pop.destroy())
            pop.bind('<Button-1>',  lambda e: pop.destroy())
        except Exception as exc:
            logger.error(f"_show_full_image: {exc}")

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        labelcode_value = self._labelcode_var.get().strip()
        if not labelcode_value:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_labelcode_required', 'Enter a LabelCode.'),
                parent=self
            )
            return

        if not self._labelcode_validated or not self._current_label_info:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get(
                    'fqc_verify_labelcode_first',
                    'Verify the LabelCode before saving the checklist.'
                ),
                parent=self
            )
            return

        unanswered = [it for it in self._items if it['ok_var'].get() == -1]
        if unanswered:
            nums = ', '.join(str(it['number']) for it in unanswered)
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_unanswered',
                              'Please answer all items before saving.') + f'\n\nItems: {nums}',
                parent=self)
            return

        nok_no_note = [it for it in self._items
                       if it['ok_var'].get() == 0 and not it['note_var'].get().strip()]
        if nok_no_note:
            nums = ', '.join(str(it['number']) for it in nok_no_note)
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_note_required',
                              'A note is required for all NOK items.') + f'\n\nItems: {nums}',
                parent=self)
            return

        try:
            cur = self.db.conn.cursor()
            id_labelcode = self._current_label_info['IDLabelCode']
            for it in self._items:
                is_ok = 1 if it['ok_var'].get() == 1 else 0
                note  = it['note_var'].get().strip() if is_ok == 0 else None
                cur.execute(_Q_INSERT_LOG,
                            (it['data_id'], is_ok, self.user_name, note))
                cur.execute(
                    _Q_UPSERT_LABEL_LOG,
                    (
                        id_labelcode, it['data_id'],
                        is_ok, self.user_name, note,
                        id_labelcode, it['data_id'],
                        it['data_id'], id_labelcode, is_ok, self.user_name, note,
                    )
                )
            self.db.conn.commit()
            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('fqc_saved', 'Checklist results saved successfully.'),
                parent=self)
            self.destroy()
        except Exception as exc:
            logger.error(f"FqcExecutionForm _on_save: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  FqcMasterForm  —  checklist creation and management (authorized)         ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class FqcMasterForm(_ClientProductMixin, tk.Toplevel):
    """Admin form for creating and managing FQC checklists and their items."""

    def __init__(self, parent, db, lang, user_name: str):
        tk.Toplevel.__init__(self, parent)
        self.db        = db
        self.lang      = lang
        self.user_name = user_name
        self._init_cp_state()
        self._checklist_id:  Optional[int]   = None
        self._id_product:    Optional[int]   = None
        self._edit_item_id:  Optional[int]   = None   # None = add mode
        self._edit_photo:    Optional[bytes] = None
        self._preview_photo                  = None   # PhotoImage ref

        self.title(self.lang.get('fqc_master_title', 'FQC Products — Checklist Management'))
        self.configure(bg=_C_BG)
        self.resizable(True, True)
        self.grab_set()
        self._build_ui()
        self._load_clients()
        self.after(120, lambda: self._center(860, 660))

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        hdr = tk.Frame(self, bg=_C_HEADER)
        hdr.pack(fill=tk.X)
        logo = _logo_label(hdr, _C_HEADER)
        if logo:
            logo.pack(side=tk.LEFT, padx=12, pady=8)
        tk.Label(hdr,
                 text=self.lang.get('fqc_master_title', 'FQC Products — Checklist Management'),
                 bg=_C_HEADER, fg='#fff',
                 font=('Segoe UI', 13, 'bold')).pack(side=tk.LEFT, pady=8, padx=8)

        body = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        body.pack(fill=tk.BOTH, expand=True)

        # Selection
        _, sel = _card(body, self.lang.get('fqc_selection', 'PRODUCT SELECTION'))
        self._build_cp_grid(sel)

        # Checklist header
        _, hdr_card = _card(body, self.lang.get('fqc_cl_header_section', 'CHECKLIST HEADER'))
        h = tk.Frame(hdr_card, bg=_C_CARD)
        h.pack(fill=tk.X)
        tk.Label(h, text=self.lang.get('fqc_cl_name', 'Checklist Name:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=16, anchor=tk.W).pack(side=tk.LEFT)
        self._cl_name_var = tk.StringVar()
        _entry(h, self._cl_name_var, 38).pack(side=tk.LEFT, padx=4)
        _btn(h, self.lang.get('fqc_save_header', '💾 Save Header'),
             self._save_header, _C_ACCENT).pack(side=tk.LEFT, padx=4)
        self._hdr_status = tk.Label(hdr_card, text='', bg=_C_CARD, fg=_C_SUBTEXT,
                                    font=('Segoe UI', 9, 'italic'))
        self._hdr_status.pack(anchor=tk.W, pady=2)

        # Items
        _, items_card = _card(body, self.lang.get('fqc_items_list', 'CHECKLIST ITEMS'))
        tv_wrap = tk.Frame(items_card, bg=_C_CARD)
        tv_wrap.pack(fill=tk.X)
        cols = ('num', 'desc', 'photo')
        self._tv = ttk.Treeview(tv_wrap, columns=cols, show='headings',
                                height=7, selectmode='browse')
        for col, lbl, w in [('num', '#', 50),
                             ('desc', self.lang.get('fqc_col_desc', 'Description'), 380),
                             ('photo', self.lang.get('fqc_col_photo', 'Photo'), 60)]:
            self._tv.heading(col, text=lbl)
            self._tv.column(col, width=w)
        vsb = ttk.Scrollbar(tv_wrap, orient='vertical', command=self._tv.yview)
        self._tv.configure(yscrollcommand=vsb.set)
        self._tv.pack(side=tk.LEFT, fill=tk.X, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        btns = tk.Frame(items_card, bg=_C_CARD)
        btns.pack(fill=tk.X, pady=4)
        _btn(btns, self.lang.get('fqc_add_item', '+ Add Item'),
             self._start_add, _C_ACCENT).pack(side=tk.LEFT, padx=2)
        _btn(btns, self.lang.get('fqc_edit_item', '✏ Edit'),
             self._start_edit, _C_WARNING).pack(side=tk.LEFT, padx=2)
        _btn(btns, self.lang.get('fqc_delete_item', '🗑 Delete (logical)'),
             self._delete_item, _C_ERROR).pack(side=tk.LEFT, padx=2)

        # Item editor panel (initially hidden)
        self._edit_outer, ep = _card(body, self.lang.get('fqc_item_editor', 'ITEM EDITOR'))
        self._edit_outer.pack_forget()

        tk.Label(ep, text=self.lang.get('fqc_item_desc', 'Description:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9)).pack(anchor=tk.W)
        self._item_desc_var = tk.StringVar()
        _entry(ep, self._item_desc_var, 64).pack(fill=tk.X, pady=2)

        photo_row = tk.Frame(ep, bg=_C_CARD)
        photo_row.pack(fill=tk.X, pady=6)
        self._preview_lbl = tk.Label(photo_row, bg='#e0e4e8', width=18, height=7,
                                     text=self.lang.get('fqc_no_photo', 'No photo'),
                                     fg=_C_SUBTEXT, font=('Segoe UI', 9))
        self._preview_lbl.pack(side=tk.LEFT, padx=(0, 10))
        pc = tk.Frame(photo_row, bg=_C_CARD)
        pc.pack(side=tk.LEFT)
        _btn(pc, self.lang.get('fqc_browse_photo', '📷 Browse photo...'),
             self._browse_photo, _C_HEADER).pack(anchor=tk.W, pady=2)
        self._photo_info = tk.Label(pc, text='', bg=_C_CARD, fg=_C_SUBTEXT,
                                    font=('Segoe UI', 8))
        self._photo_info.pack(anchor=tk.W)

        eb = tk.Frame(ep, bg=_C_CARD)
        eb.pack(fill=tk.X, pady=4)
        _btn(eb, self.lang.get('fqc_save_item', '💾 Save Item'),
             self._save_item, _C_SUCCESS).pack(side=tk.LEFT, padx=2)
        _btn(eb, self.lang.get('cancel', 'Cancel'),
             self._cancel_edit, _C_BORDER, fg=_C_TEXT).pack(side=tk.LEFT, padx=2)

        foot = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        foot.pack(fill=tk.X)
        _btn(foot, self.lang.get('close', 'Close'), self.destroy,
             bg=_C_BORDER, fg=_C_TEXT).pack(side=tk.RIGHT)

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _on_product_selected(self, event=None):
        code = self._product_combo.get()
        self._id_product = self._product_map.get(code)
        if self._id_product:
            self._load_checklist()

    def _load_checklist(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_ACTIVE_CHECKLIST, (self._id_product,))
            cl = cur.fetchone()
            if cl:
                self._checklist_id = cl[0]
                self._cl_name_var.set(cl[1])
                d = cl[2].strftime('%d/%m/%Y') if cl[2] else ''
                self._hdr_status.config(text=f'ID {cl[0]} — {d}', fg=_C_SUCCESS)
            else:
                self._checklist_id = None
                self._cl_name_var.set('')
                self._hdr_status.config(
                    text=self.lang.get('fqc_no_checklist_admin',
                                       '⚠ No checklist — enter name and click Save Header to create.'),
                    fg=_C_WARNING)
            self._refresh_tree()
        except Exception as exc:
            logger.error(f"FqcMasterForm _load_checklist: {exc}")

    def _refresh_tree(self):
        for row in self._tv.get_children():
            self._tv.delete(row)
        if not self._checklist_id:
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_CHECKLIST_ITEMS, (self._checklist_id,))
            for r in cur.fetchall():
                has_photo = '✓' if r[3] else '—'
                self._tv.insert('', 'end', iid=str(r[0]),
                                values=(r[2], r[1][:70], has_photo))
        except Exception as exc:
            logger.error(f"_refresh_tree: {exc}")

    # ── Header ────────────────────────────────────────────────────────────────

    def _save_header(self):
        if not self._id_product:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_select_product_first', 'Please select a product first.'),
                parent=self)
            return
        name = self._cl_name_var.get().strip()
        if not name:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_cl_name_required', 'Checklist name is required.'),
                parent=self)
            return
        try:
            cur = self.db.conn.cursor()
            if self._checklist_id:
                cur.execute(_Q_RENAME_CHECKLIST, (name, self._checklist_id))
            else:
                cur.execute(_Q_CREATE_CHECKLIST, (name, self._id_product))
                cur.execute('SELECT @@IDENTITY')
                self._checklist_id = int(cur.fetchone()[0])
            self.db.conn.commit()
            self._hdr_status.config(text=f'✅ ID {self._checklist_id} — saved', fg=_C_SUCCESS)
            self._refresh_tree()
        except Exception as exc:
            logger.error(f"_save_header: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)

    # ── Item CRUD ─────────────────────────────────────────────────────────────

    def _start_add(self):
        if not self._checklist_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_save_header_first', 'Save the checklist header first.'),
                parent=self)
            return
        self._edit_item_id  = None
        self._edit_photo    = None
        self._preview_photo = None
        self._item_desc_var.set('')
        self._preview_lbl.config(image='', text=self.lang.get('fqc_no_photo', 'No photo'))
        self._photo_info.config(text='')
        self._edit_outer.pack(fill=tk.X, pady=4)

    def _start_edit(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_select_item', 'Select an item first.'), parent=self)
            return
        data_id = int(sel[0])
        self._edit_item_id = data_id
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_LOAD_ITEM, (data_id,))
            row = cur.fetchone()
            if row:
                self._item_desc_var.set(row[0])
                self._edit_photo = bytes(row[1]) if row[1] else None
                self._update_preview(self._edit_photo)
        except Exception as exc:
            logger.error(f"_start_edit: {exc}")
        self._edit_outer.pack(fill=tk.X, pady=4)

    def _delete_item(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_select_item', 'Select an item first.'), parent=self)
            return
        if not messagebox.askyesno(
                self.lang.get('confirm', 'Confirm'),
                self.lang.get('fqc_confirm_delete',
                              'Mark this item as deleted? (soft delete)'),
                parent=self):
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_DELETE_ITEM, (int(sel[0]),))
            self.db.conn.commit()
            self._refresh_tree()
            self._cancel_edit()
        except Exception as exc:
            logger.error(f"_delete_item: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)

    def _browse_photo(self):
        path = filedialog.askopenfilename(
            parent=self,
            title=self.lang.get('fqc_select_photo', 'Select photo'),
            filetypes=[('Images', '*.jpg *.jpeg *.png *.bmp *.gif'), ('All', '*.*')]
        )
        if not path:
            return
        data = _file_to_bytes(path)
        if not data:
            messagebox.showerror('Error', f'Cannot read: {path}', parent=self)
            return
        self._edit_photo = data
        sz = len(data) // 1024
        self._photo_info.config(text=f'{os.path.basename(path)}  ({sz} KB)')
        self._update_preview(data)

    def _update_preview(self, data):
        if not data or not _PIL_OK:
            self._preview_lbl.config(image='', text=self.lang.get('fqc_no_photo', 'No photo'))
            return
        photo = _bytes_to_photo(data, (130, 104))
        if photo:
            self._preview_photo = photo
            self._preview_lbl.config(image=photo, text='')
        else:
            self._preview_lbl.config(image='', text='Preview error')

    def _save_item(self):
        desc = self._item_desc_var.get().strip()
        if not desc:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_desc_required', 'Description is required.'), parent=self)
            return
        if not self._edit_photo:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_photo_required',
                              'A photo is required for each checklist item.'), parent=self)
            return
        try:
            cur = self.db.conn.cursor()
            if self._edit_item_id is None:
                cur.execute(_Q_NEXT_ITEM_NUM, (self._checklist_id,))
                next_n = cur.fetchone()[0]
                cur.execute(_Q_INSERT_ITEM,
                            (self._checklist_id, desc, next_n, self._edit_photo))
            else:
                cur.execute(_Q_UPDATE_ITEM, (desc, self._edit_photo, self._edit_item_id))
            self.db.conn.commit()
            self._refresh_tree()
            self._cancel_edit()
        except Exception as exc:
            logger.error(f"_save_item: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)

    def _cancel_edit(self):
        self._edit_outer.pack_forget()
        self._edit_item_id = None
        self._edit_photo   = None


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  FqcFeedbackForm  —  customer feedback recording                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class FqcFeedbackForm(_ClientProductMixin, tk.Toplevel):
    """Form for recording customer feedback linked to NOK checklist results."""

    def __init__(self, parent, db, lang, user_name: str):
        tk.Toplevel.__init__(self, parent)
        self.db        = db
        self.lang      = lang
        self.user_name = user_name
        self._init_cp_state()
        self._selected_log_id: Optional[int]   = None
        self._fb_photo:        Optional[bytes] = None
        self._fb_preview_photo                 = None

        self.title(self.lang.get('fqc_feedback_title', 'FQC Products — Customer Feedback'))
        self.configure(bg=_C_BG)
        self.resizable(True, True)
        self.grab_set()
        self._build_ui()
        self._load_clients()
        self.after(120, lambda: self._center(840, 620))

    def _build_ui(self):
        hdr = tk.Frame(self, bg=_C_HEADER)
        hdr.pack(fill=tk.X)
        logo = _logo_label(hdr, _C_HEADER)
        if logo:
            logo.pack(side=tk.LEFT, padx=12, pady=8)
        tk.Label(hdr,
                 text=self.lang.get('fqc_feedback_title', 'FQC Products — Customer Feedback'),
                 bg=_C_HEADER, fg='#fff',
                 font=('Segoe UI', 13, 'bold')).pack(side=tk.LEFT, pady=8, padx=8)

        body = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        body.pack(fill=tk.BOTH, expand=True)

        _, sel = _card(body, self.lang.get('fqc_selection', 'PRODUCT SELECTION'))
        self._build_cp_grid(sel)

        # NOK logs treeview
        _, logs_card = _card(body, self.lang.get('fqc_nok_logs', 'NOK CHECKLIST RESULTS'))
        cols = ('date', 'item', 'user', 'note')
        self._logs_tv = ttk.Treeview(logs_card, columns=cols, show='headings',
                                     height=7, selectmode='browse')
        for col, lbl, w in [
            ('date', self.lang.get('fqc_date', 'Date'), 130),
            ('item', self.lang.get('fqc_item', 'Item'),  220),
            ('user', self.lang.get('fqc_user', 'User'),  100),
            ('note', self.lang.get('fqc_note_fb', 'NOK Note'), 260),
        ]:
            self._logs_tv.heading(col, text=lbl)
            self._logs_tv.column(col, width=w)
        vsb = ttk.Scrollbar(logs_card, orient='vertical', command=self._logs_tv.yview)
        self._logs_tv.configure(yscrollcommand=vsb.set)
        self._logs_tv.pack(side=tk.LEFT, fill=tk.X, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._logs_tv.bind('<<TreeviewSelect>>', self._on_log_selected)

        # Feedback form
        _, fb_card = _card(body, self.lang.get('fqc_feedback_form', 'CUSTOMER FEEDBACK'))

        tk.Label(fb_card, text=self.lang.get('fqc_feedback_text', 'Feedback:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9)).pack(anchor=tk.W)
        self._fb_text = tk.Text(fb_card, height=3, font=('Segoe UI', 10),
                                relief=tk.FLAT,
                                highlightbackground=_C_BORDER,
                                highlightcolor=_C_ACCENT, highlightthickness=1)
        self._fb_text.pack(fill=tk.X, pady=2)

        row2 = tk.Frame(fb_card, bg=_C_CARD)
        row2.pack(fill=tk.X, pady=4)
        tk.Label(row2, text=self.lang.get('fqc_fb_from', 'From:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=8, anchor=tk.W).pack(side=tk.LEFT)
        self._fb_from_var = tk.StringVar()
        _entry(row2, self._fb_from_var, 22).pack(side=tk.LEFT, padx=4)
        tk.Label(row2, text=self.lang.get('fqc_fb_date', 'Date:'),
                 bg=_C_CARD, fg=_C_TEXT, font=('Segoe UI', 9),
                 width=6, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        self._fb_date_var = tk.StringVar(
            value=datetime.date.today().strftime('%Y-%m-%d'))
        _entry(row2, self._fb_date_var, 12).pack(side=tk.LEFT, padx=4)

        row3 = tk.Frame(fb_card, bg=_C_CARD)
        row3.pack(fill=tk.X, pady=4)
        self._fb_preview_lbl = tk.Label(row3, bg='#e0e4e8', width=14, height=6,
                                        text=self.lang.get('fqc_no_photo', 'No photo'),
                                        fg=_C_SUBTEXT, font=('Segoe UI', 9))
        self._fb_preview_lbl.pack(side=tk.LEFT, padx=(0, 10))
        _btn(row3, self.lang.get('fqc_browse_photo', '📷 Browse photo...'),
             self._browse_fb_photo, _C_HEADER).pack(side=tk.LEFT)

        foot = tk.Frame(self, bg=_C_BG, padx=12, pady=8)
        foot.pack(fill=tk.X)
        self._save_btn = _btn(foot,
                              self.lang.get('fqc_save_feedback', '💾 Save Feedback'),
                              self._save_feedback, _C_SUCCESS)
        self._save_btn.pack(side=tk.LEFT)
        self._save_btn.config(state='disabled')
        _btn(foot, self.lang.get('close', 'Close'), self.destroy,
             bg=_C_BORDER, fg=_C_TEXT).pack(side=tk.RIGHT)

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _on_product_selected(self, event=None):
        code       = self._product_combo.get()
        id_product = self._product_map.get(code)
        if id_product:
            self._load_nok_logs(id_product)

    def _load_nok_logs(self, id_product: int):
        for row in self._logs_tv.get_children():
            self._logs_tv.delete(row)
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_NOK_LOGS, (id_product,))
            for r in cur.fetchall():
                dt = r[4].strftime('%d/%m/%Y %H:%M') if r[4] else ''
                self._logs_tv.insert('', 'end', iid=str(r[0]),
                                     values=(dt, f'#{r[1]} {r[2][:40]}', r[3], r[5] or ''))
        except Exception as exc:
            logger.error(f"_load_nok_logs: {exc}")

    def _on_log_selected(self, event=None):
        sel = self._logs_tv.selection()
        if sel:
            self._selected_log_id = int(sel[0])
            self._save_btn.config(state='normal')
        else:
            self._selected_log_id = None
            self._save_btn.config(state='disabled')

    def _browse_fb_photo(self):
        path = filedialog.askopenfilename(
            parent=self,
            title=self.lang.get('fqc_select_photo', 'Select photo'),
            filetypes=[('Images', '*.jpg *.jpeg *.png *.bmp *.gif'), ('All', '*.*')]
        )
        if not path:
            return
        data = _file_to_bytes(path)
        if data:
            self._fb_photo = data
            photo = _bytes_to_photo(data, (100, 80))
            if photo:
                self._fb_preview_photo = photo
                self._fb_preview_lbl.config(image=photo, text='')

    def _save_feedback(self):
        if not self._selected_log_id:
            return
        fb_text = self._fb_text.get('1.0', 'end-1c').strip()
        if not fb_text:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_fb_text_required', 'Feedback text is required.'),
                parent=self)
            return
        fb_from = self._fb_from_var.get().strip()
        try:
            fb_date = datetime.datetime.strptime(
                self._fb_date_var.get().strip(), '%Y-%m-%d').date()
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('fqc_date_format', 'Date must be YYYY-MM-DD.'), parent=self)
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_INSERT_FEEDBACK,
                        (self._selected_log_id, fb_text, self._fb_photo,
                         fb_date, fb_from or self.user_name))
            self.db.conn.commit()
            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('fqc_feedback_saved', 'Feedback saved successfully.'),
                parent=self)
            # Reset
            self._fb_text.delete('1.0', tk.END)
            self._fb_from_var.set('')
            self._fb_photo = None
            self._fb_preview_lbl.config(image='', text=self.lang.get('fqc_no_photo', 'No photo'))
            self._fb_preview_photo = None
            self._save_btn.config(state='disabled')
            self._logs_tv.selection_remove(self._logs_tv.selection())
            self._selected_log_id = None
        except Exception as exc:
            logger.error(f"_save_feedback: {exc}", exc_info=True)
            messagebox.showerror('Error', str(exc), parent=self)


# ── Public API ────────────────────────────────────────────────────────────────

def open_fqc_execution(parent, db, lang, user_name: str):
    """Opens the FQC checklist execution form (simple login)."""
    _ensure_fqc_labelcode_schema(db)
    form = FqcExecutionForm(parent, db, lang, user_name)
    parent.wait_window(form)


def open_fqc_master(parent, db, lang, user_name: str):
    """Opens the FQC checklist management form (authorized action)."""
    form = FqcMasterForm(parent, db, lang, user_name)
    parent.wait_window(form)


def open_fqc_feedback(parent, db, lang, user_name: str):
    """Opens the customer feedback form (simple login)."""
    form = FqcFeedbackForm(parent, db, lang, user_name)
    parent.wait_window(form)
