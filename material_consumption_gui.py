# -*- coding: utf-8 -*-
"""
material_consumption_gui.py
Form for managing product material consumption data (Alloy_GR / Flux_GR).
"""
from __future__ import annotations
import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger("TraceabilityRS")

# ── SQL ────────────────────────────────────────────────────────────────────────

_Q_LABEL_TO_PRODUCT = """
SELECT TOP 1
    b.IDBoard,
    o.IDOrder,
    o.OrderNumber,
    p.IDProduct,
    p.ProductCode
FROM LabelCodes lc
INNER JOIN Boards   b ON b.IDBoard   = lc.IDBoard
INNER JOIN Orders   o ON o.IDOrder   = b.IDOrder
INNER JOIN Products p ON p.IDProduct = o.IDProduct
WHERE lc.labelcod = ?
"""

_Q_ALL_PRODUCTS = """
SELECT IDProduct, ProductCode
FROM   Products
WHERE (charindex('CIP', ProductCode) = 0) AND (charindex('RMA', ProductCode) = 0)
ORDER  BY ProductCode
"""

_Q_CHECK_EXISTING = """
SELECT TOP 1
    ProductConsumptionId,
    MaterialConsumptionGR,
    DateSys,
    [User]
FROM [Traceability_RS].[dbo].[ProductConsumptions]
WHERE IdProduct           = ?
  AND MaterialConsumption = ?
  AND DateOut             IS NULL
"""

_Q_SOFT_DELETE = """
UPDATE [Traceability_RS].[dbo].[ProductConsumptions]
SET    DateOut = GETDATE()
WHERE  ProductConsumptionId = ?
"""

_Q_INSERT = """
INSERT INTO [Traceability_RS].[dbo].[ProductConsumptions]
    (IdProduct, MaterialConsumptionGR, MaterialConsumption, [User], DateSys)
VALUES (?, ?, ?, ?, GETDATE())
"""

_Q_COUNT_PRODUCTS = """
SELECT COUNT(DISTINCT IdProduct)
FROM   [Traceability_RS].[dbo].[ProductConsumptions]
WHERE  DateOut IS NULL
"""


# ── Colours / style tokens ─────────────────────────────────────────────────────

_C_HEADER   = '#1f3864'
_C_ACCENT   = '#2e86de'
_C_SUCCESS  = '#27ae60'
_C_ERROR    = '#e74c3c'
_C_WARNING  = '#f39c12'
_C_BG       = '#f4f6f8'
_C_CARD     = '#ffffff'
_C_BORDER   = '#dde1e7'
_C_TEXT     = '#2c3e50'
_C_SUBTEXT  = '#7f8c8d'


class MaterialConsumptionForm(tk.Toplevel):
    """Top-level form for entering product material consumption data."""

    def __init__(self, parent, db, lang, logged_user: str):
        super().__init__(parent)
        self.db          = db
        self.lang        = lang
        self.logged_user = logged_user

        # State
        self._id_product:   int | None  = None
        self._product_code: str         = ''
        self._products_map: dict        = {}   # ProductCode → IDProduct
        self._all_products: list        = []   # [(IDProduct, ProductCode), ...]

        self.title(self.lang.get('mat_cons_title', 'Material Consumption Management'))
        self.resizable(False, False)
        self.configure(bg=_C_BG)
        self.grab_set()

        self._build_ui()
        self._load_products()
        self._load_count()
        self.after(100, self._center)

    # ── UI build ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=_C_HEADER)
        hdr.pack(fill=tk.X)

        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
        if os.path.isfile(logo_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                img.thumbnail((120, 48), Image.LANCZOS)
                self._logo_img = ImageTk.PhotoImage(img)
                tk.Label(hdr, image=self._logo_img, bg=_C_HEADER).pack(
                    side=tk.LEFT, padx=14, pady=10
                )
            except Exception:
                pass

        ttl_frame = tk.Frame(hdr, bg=_C_HEADER)
        ttl_frame.pack(side=tk.LEFT, pady=10)
        tk.Label(ttl_frame,
                 text=self.lang.get('mat_cons_title', 'Material Consumption Management'),
                 bg=_C_HEADER, fg='#ffffff',
                 font=('Segoe UI', 14, 'bold')).pack(anchor=tk.W)

        self._count_lbl = tk.Label(
            ttl_frame,
            text='',
            bg=_C_HEADER, fg='#a8c4e0',
            font=('Segoe UI', 10)
        )
        self._count_lbl.pack(anchor=tk.W)

        # ── Main area ────────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=_C_BG, padx=16, pady=14)
        body.pack(fill=tk.BOTH, expand=True)

        # ── Card: Product Search ─────────────────────────────────────────────────
        self._card(body, self.lang.get('mat_cons_search', 'PRODUCT SEARCH'), self._build_search)

        # ── Card: Product Info ───────────────────────────────────────────────────
        self._card(body, self.lang.get('mat_cons_info', 'PRODUCT INFO'), self._build_info)

        # ── Card: Consumption Data ───────────────────────────────────────────────
        self._card(body, self.lang.get('mat_cons_data', 'CONSUMPTION DATA'), self._build_data)

        # ── Buttons ──────────────────────────────────────────────────────────────
        btn_row = tk.Frame(self, bg=_C_BG, padx=16, pady=10)
        btn_row.pack(fill=tk.X)

        self._save_btn = tk.Button(
            btn_row,
            text=self.lang.get('mat_cons_save', 'Save'),
            bg=_C_ACCENT, fg='#ffffff',
            activebackground='#1a6fc4',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT, padx=22, pady=6,
            cursor='hand2',
            command=self._on_save
        )
        self._save_btn.pack(side=tk.LEFT)

        tk.Button(
            btn_row,
            text=self.lang.get('close', 'Close'),
            bg=_C_BORDER, fg=_C_TEXT,
            font=('Segoe UI', 10),
            relief=tk.FLAT, padx=16, pady=6,
            cursor='hand2',
            command=self.destroy
        ).pack(side=tk.RIGHT)

    def _card(self, parent, title: str, builder):
        """Creates a white card with a section title."""
        outer = tk.Frame(parent, bg=_C_BORDER, bd=0)
        outer.pack(fill=tk.X, pady=6)
        inner = tk.Frame(outer, bg=_C_CARD, padx=14, pady=10)
        inner.pack(fill=tk.X, padx=1, pady=1)
        tk.Label(inner,
                 text=title,
                 bg=_C_CARD, fg=_C_HEADER,
                 font=('Segoe UI', 8, 'bold')).pack(anchor=tk.W, pady=(0, 6))
        sep = tk.Frame(inner, bg=_C_BORDER, height=1)
        sep.pack(fill=tk.X, pady=(0, 8))
        builder(inner)

    def _build_search(self, parent):
        # Row 1: LabelCode
        r1 = tk.Frame(parent, bg=_C_CARD)
        r1.pack(fill=tk.X, pady=3)
        tk.Label(r1, text=self.lang.get('mat_cons_labelcode', 'Label Code:'),
                 bg=_C_CARD, fg=_C_TEXT,
                 font=('Segoe UI', 9), width=12, anchor=tk.W).pack(side=tk.LEFT)
        self._lc_var = tk.StringVar()
        lc_entry = tk.Entry(r1, textvariable=self._lc_var,
                            font=('Segoe UI', 10), width=28,
                            relief=tk.FLAT,
                            highlightbackground=_C_BORDER,
                            highlightcolor=_C_ACCENT,
                            highlightthickness=1)
        lc_entry.pack(side=tk.LEFT, padx=(0, 6))
        lc_entry.bind('<Return>', self._on_validate_label)
        lc_entry.bind('<FocusOut>', self._on_validate_label)

        tk.Button(r1,
                  text=self.lang.get('mat_cons_validate', 'Validate'),
                  bg=_C_HEADER, fg='#fff',
                  font=('Segoe UI', 9),
                  relief=tk.FLAT, padx=10, pady=3,
                  cursor='hand2',
                  command=self._on_validate_label).pack(side=tk.LEFT)

        self._lc_status = tk.Label(r1, text='', bg=_C_CARD, fg=_C_SUBTEXT,
                                   font=('Segoe UI', 9))
        self._lc_status.pack(side=tk.LEFT, padx=8)

        # Divider
        tk.Label(parent,
                 text=f'— {self.lang.get("mat_cons_or", "OR")} —',
                 bg=_C_CARD, fg=_C_SUBTEXT,
                 font=('Segoe UI', 9, 'italic')).pack(anchor=tk.W, pady=4)

        # Row 2: Product combo
        r2 = tk.Frame(parent, bg=_C_CARD)
        r2.pack(fill=tk.X, pady=3)
        tk.Label(r2,
                 text=self.lang.get('mat_cons_product', 'Product:'),
                 bg=_C_CARD, fg=_C_TEXT,
                 font=('Segoe UI', 9), width=12, anchor=tk.W).pack(side=tk.LEFT)
        self._combo_var = tk.StringVar()
        self._combo = ttk.Combobox(r2, textvariable=self._combo_var,
                                   width=40, font=('Segoe UI', 10))
        self._combo.pack(side=tk.LEFT)
        self._combo.bind('<<ComboboxSelected>>', self._on_combo_selected)
        self._combo.bind('<KeyRelease>', self._on_combo_filter)

    def _build_info(self, parent):
        grid = tk.Frame(parent, bg=_C_CARD)
        grid.pack(fill=tk.X)

        def _lbl(col, text):
            tk.Label(grid, text=text, bg=_C_CARD, fg=_C_SUBTEXT,
                     font=('Segoe UI', 8)).grid(row=0, column=col*2, sticky=tk.W, padx=4)

        def _val(col, var):
            lbl = tk.Label(grid, textvariable=var, bg=_C_CARD, fg=_C_TEXT,
                           font=('Segoe UI', 10, 'bold'))
            lbl.grid(row=1, column=col*2, sticky=tk.W, padx=4)

        self._info_code_var = tk.StringVar(value='—')
        self._info_id_var   = tk.StringVar(value='—')

        _lbl(0, self.lang.get('mat_cons_pcode', 'Product Code'))
        _lbl(1, 'IDProduct')
        _val(0, self._info_code_var)
        _val(1, self._info_id_var)

    def _build_data(self, parent):
        row = tk.Frame(parent, bg=_C_CARD)
        row.pack(fill=tk.X)

        # Radio buttons for Alloy / Flux
        self._type_var = tk.StringVar(value='Alloy_GR')
        tk.Radiobutton(row, text=self.lang.get('mat_cons_alloy', 'Alloy_GR'),
                       variable=self._type_var, value='Alloy_GR',
                       bg=_C_CARD, fg=_C_TEXT,
                       font=('Segoe UI', 10),
                       activebackground=_C_CARD,
                       selectcolor=_C_CARD).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(row, text=self.lang.get('mat_cons_flux', 'Flux_GR'),
                       variable=self._type_var, value='Flux_GR',
                       bg=_C_CARD, fg=_C_TEXT,
                       font=('Segoe UI', 10),
                       activebackground=_C_CARD,
                       selectcolor=_C_CARD).pack(side=tk.LEFT, padx=(0, 24))

        # Value field
        tk.Label(row,
                 text=self.lang.get('mat_cons_value', 'Value (gr):'),
                 bg=_C_CARD, fg=_C_TEXT,
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 6))

        self._value_var = tk.StringVar()
        vcmd = (self.register(self._validate_numeric), '%P')
        self._value_entry = tk.Entry(
            row, textvariable=self._value_var,
            validate='key', validatecommand=vcmd,
            font=('Segoe UI', 10), width=12,
            relief=tk.FLAT,
            highlightbackground=_C_BORDER,
            highlightcolor=_C_ACCENT,
            highlightthickness=1
        )
        self._value_entry.pack(side=tk.LEFT)
        tk.Label(row, text='gr', bg=_C_CARD, fg=_C_SUBTEXT,
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=4)

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_products(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_ALL_PRODUCTS)
            self._all_products = [(r.IDProduct, r.ProductCode) for r in cur.fetchall()]
            codes = [r[1] for r in self._all_products]
            self._products_map = {r[1]: r[0] for r in self._all_products}
            self._combo['values'] = codes
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_products: {e}')

    def _load_count(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_COUNT_PRODUCTS)
            row = cur.fetchone()
            cnt = row[0] if row else 0
            lbl = self.lang.get('mat_cons_products_count', 'Products configured')
            self._count_lbl.config(text=f'{lbl}: {cnt}')
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_count: {e}')

    # ── Validation ────────────────────────────────────────────────────────────

    @staticmethod
    def _validate_numeric(value: str) -> bool:
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            return '.' in value or value == '-'

    def _on_validate_label(self, event=None):
        lc = self._lc_var.get().strip()
        if not lc:
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_LABEL_TO_PRODUCT, (lc,))
            row = cur.fetchone()
            if row:
                self._set_product(row.IDProduct, row.ProductCode)
                self._lc_status.config(
                    text=f'✅ {row.ProductCode}',
                    fg=_C_SUCCESS
                )
            else:
                self._lc_status.config(
                    text=self.lang.get('mat_cons_lc_not_found', '❌ Label not found'),
                    fg=_C_ERROR
                )
                self._clear_product()
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _on_validate_label: {e}')
            self._lc_status.config(text=f'❌ {str(e)[:40]}', fg=_C_ERROR)

    def _on_combo_selected(self, event=None):
        code = self._combo_var.get()
        if code in self._products_map:
            self._set_product(self._products_map[code], code)
            # Clear label status since user used combo
            self._lc_status.config(text='', fg=_C_SUBTEXT)

    def _on_combo_filter(self, event=None):
        """Filters combo list based on user input."""
        typed = self._combo_var.get().upper()
        if not typed:
            self._combo['values'] = [r[1] for r in self._all_products]
            return
        filtered = [r[1] for r in self._all_products if typed in r[1].upper()]
        self._combo['values'] = filtered

    def _set_product(self, id_product: int, product_code: str):
        self._id_product   = id_product
        self._product_code = product_code
        self._info_code_var.config(value=product_code) if hasattr(self._info_code_var, 'config') else self._info_code_var.set(product_code)
        self._info_id_var.set(str(id_product))
        self._combo_var.set(product_code)

    def _clear_product(self):
        self._id_product   = None
        self._product_code = ''
        self._info_code_var.set('—')
        self._info_id_var.set('—')

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        # Validation
        if self._id_product is None:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('mat_cons_no_product', 'Please select a product first.'),
                parent=self
            )
            return

        value_str = self._value_var.get().strip()
        if not value_str:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('mat_cons_no_value', 'Please enter a consumption value.'),
                parent=self
            )
            return

        try:
            value_gr = float(value_str)
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('mat_cons_invalid_value', 'Value must be a number.'),
                parent=self
            )
            return

        mat_type = self._type_var.get()  # 'Alloy_GR' or 'Flux_GR'

        try:
            cur = self.db.conn.cursor()

            # ── Check existing ────────────────────────────────────────────────
            cur.execute(_Q_CHECK_EXISTING, (self._id_product, mat_type))
            existing = cur.fetchone()

            if existing:
                existing_gr   = existing.MaterialConsumptionGR
                existing_date = str(existing.DateSys)[:19]
                existing_user = existing.User or '—'
                existing_id   = existing.ProductConsumptionId

                answer = messagebox.askyesno(
                    self.lang.get('mat_cons_exists_title', 'Existing Record Found'),
                    (
                        f"{self.lang.get('mat_cons_exists_msg', 'A record already exists for this product')}:\n\n"
                        f"  Product : {self._product_code}\n"
                        f"  Type    : {mat_type}\n"
                        f"  Value   : {existing_gr} gr\n"
                        f"  Date    : {existing_date}\n"
                        f"  User    : {existing_user}\n\n"
                        f"{self.lang.get('mat_cons_overwrite', 'Do you want to replace it with the new value?')}"
                    ),
                    parent=self
                )
                if not answer:
                    return
                # Soft delete
                cur.execute(_Q_SOFT_DELETE, (existing_id,))

            # ── Insert new ────────────────────────────────────────────────────
            cur.execute(_Q_INSERT, (
                self._id_product,
                value_gr,
                mat_type,
                self.logged_user or 'system'
            ))
            self.db.conn.commit()

            messagebox.showinfo(
                self.lang.get('success', 'Success'),
                self.lang.get('mat_cons_saved', 'Data saved successfully.'),
                parent=self
            )

            # Refresh count
            self._load_count()
            # Clear value for next entry
            self._value_var.set('')

        except Exception as e:
            logger.error(f'MaterialConsumptionForm _on_save: {e}', exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Error'),
                f"{self.lang.get('mat_cons_save_error', 'Save error')}:\n{e}",
                parent=self
            )

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = self.winfo_screenwidth()  // 2 - w // 2
        y = self.winfo_screenheight() // 2 - h // 2
        self.geometry(f'+{x}+{y}')
