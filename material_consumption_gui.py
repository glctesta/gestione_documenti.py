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

_Q_PRODUCTS_WITH_CONSUMPTION = """
SELECT DISTINCT
        p.IDProduct,
        p.ProductCode
FROM Traceability_RS.dbo.Products p
INNER JOIN Traceability_RS.dbo.ProductConsumptions pc
                ON pc.IdProduct = p.IDProduct
WHERE pc.MaterialConsumption = ?
    AND pc.DateOut IS NULL
ORDER BY p.ProductCode
"""

_Q_CHECK_EXISTING = """
SELECT TOP 1
    ProductConsumptionId,
    MaterialConsumptionGR,
    MaterialeId,
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
    (IdProduct, MaterialConsumptionGR, MaterialConsumption, MaterialeId, [User], DateSys)
VALUES (?, ?, ?, ?, ?, GETDATE())
"""

# Materiali indiretti delle famiglie Alloy / Flux, usati come link per i consumi
_Q_CONSUMPTION_MATERIALS = """
SELECT M.MaterialeId, M.CodiceMateriale, M.DescrizioneMateriale, F.Famiglia
FROM ind.Materiali M
INNER JOIN ind.FamigliaMateriali F ON F.FamigliaMaterialiId = M.FamigliaMaterialiId
WHERE M.IsActive = 1
  AND F.Famiglia IN ('Alloy', 'Flux')
ORDER BY M.CodiceMateriale
"""

# Tipo consumo → famiglia materiali
_MAT_TYPE_FAMILY = {'Alloy_GR': 'Alloy', 'Flux_GR': 'Flux'}

_Q_COUNT_PRODUCTS = """
SELECT COUNT(DISTINCT IdProduct)
FROM   [Traceability_RS].[dbo].[ProductConsumptions]
WHERE  DateOut IS NULL
"""


def _ensure_materialeid_column(db):
    """Aggiunge la colonna MaterialeId a ProductConsumptions se manca (idempotente)."""
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                "SELECT COUNT(*) FROM sys.columns "
                "WHERE object_id = OBJECT_ID('Traceability_RS.dbo.ProductConsumptions') "
                "  AND name = 'MaterialeId'"
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "ALTER TABLE Traceability_RS.dbo.ProductConsumptions "
                    "ADD MaterialeId INT NULL"
                )
                db.conn.commit()
                logger.info("Colonna MaterialeId aggiunta a ProductConsumptions")
    except Exception as e:
        logger.warning("Impossibile assicurare colonna MaterialeId: %s", e)


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
        self._existing_consumption: dict | None = None
        self._combo_display_map: dict[str, str] = {}
        self._materials_map:   dict[str, dict] = {}  # mat_type → {display: MaterialeId}
        self._materials_by_id: dict[str, dict] = {}  # mat_type → {MaterialeId: display}
        self._materials_display: dict[str, list] = {}  # mat_type → [display]

        self.title(self.lang.get('mat_cons_title', 'Material Consumption Management'))
        self.resizable(False, False)
        self.configure(bg=_C_BG)
        self.grab_set()

        _ensure_materialeid_column(self.db)
        self._load_consumption_materials()
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

        self._existing_lbl = tk.Label(
            grid,
            text='',
            bg=_C_CARD,
            fg=_C_SUBTEXT,
            font=('Segoe UI', 9, 'italic'),
            justify=tk.LEFT
        )
        self._existing_lbl.grid(row=2, column=0, columnspan=4, sticky=tk.W, padx=4, pady=(6, 0))

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
                       selectcolor=_C_CARD,
                       command=self._on_type_changed).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(row, text=self.lang.get('mat_cons_flux', 'Flux_GR'),
                       variable=self._type_var, value='Flux_GR',
                       bg=_C_CARD, fg=_C_TEXT,
                       font=('Segoe UI', 10),
                       activebackground=_C_CARD,
                       selectcolor=_C_CARD,
                       command=self._on_type_changed).pack(side=tk.LEFT, padx=(0, 24))

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

        # Material combo (ind.Materiali, famiglia del tipo selezionato: Alloy/Flux)
        row2 = tk.Frame(parent, bg=_C_CARD)
        row2.pack(fill=tk.X, pady=(10, 0))
        self._material_lbl = tk.Label(row2,
                 text=self.lang.get('mat_cons_material', 'Materiale:'),
                 bg=_C_CARD, fg=_C_TEXT,
                 font=('Segoe UI', 9), width=14, anchor=tk.W)
        self._material_lbl.pack(side=tk.LEFT)
        self._material_var = tk.StringVar()
        self._material_combo = ttk.Combobox(
            row2, textvariable=self._material_var,
            values=self._materials_display.get('Alloy_GR', []),
            width=70, font=('Segoe UI', 10), state='readonly'
        )
        self._material_combo.pack(side=tk.LEFT)

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_consumption_materials(self):
        """Carica i materiali indiretti delle famiglie Alloy e Flux, indicizzati per tipo consumo."""
        by_family: dict[str, list] = {}
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_CONSUMPTION_MATERIALS)
            for r in cur.fetchall():
                display = f"{r.CodiceMateriale} — {r.DescrizioneMateriale or ''}".strip(' —')
                by_family.setdefault(r.Famiglia, []).append((r.MaterialeId, display))
            cur.close()
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_consumption_materials: {e}', exc_info=True)

        for mat_type, family in _MAT_TYPE_FAMILY.items():
            entries = by_family.get(family, [])
            self._materials_map[mat_type] = {display: mid for mid, display in entries}
            self._materials_by_id[mat_type] = {mid: display for mid, display in entries}
            self._materials_display[mat_type] = [display for _, display in entries]
            if not entries:
                logger.warning(f"Nessun materiale della famiglia '{family}' trovato in ind.Materiali")

    def _on_type_changed(self):
        """Aggiorna la combo materiali quando cambia il tipo Alloy/Flux."""
        mat_type = self._type_var.get()
        if not hasattr(self, '_material_combo'):
            return
        self._material_combo['values'] = self._materials_display.get(mat_type, [])
        self._material_var.set('')
        if self._id_product is not None:
            self._load_existing_consumption_state()

    def _load_products(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_ALL_PRODUCTS)
            self._all_products = [(r.IDProduct, r.ProductCode) for r in cur.fetchall()]
            self._refresh_products_combo()
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_products: {e}')

    def _load_products_with_consumption(self, material_type: str) -> set[int]:
        """Return product IDs that already have a saved consumption for the selected material type."""
        existing_ids: set[int] = set()
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_PRODUCTS_WITH_CONSUMPTION, (material_type,))
            existing_ids = {r.IDProduct for r in cur.fetchall()}
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_products_with_consumption: {e}')
        return existing_ids

    def _refresh_products_combo(self):
        """Refresh combo values and mark products that already have a saved value."""
        material_type = self._type_var.get() if hasattr(self, '_type_var') else 'Alloy_GR'
        existing_ids = self._load_products_with_consumption(material_type)

        self._products_map = {}
        self._combo_display_map = {}
        display_values: list[str] = []

        for id_product, product_code in self._all_products:
            display_code = f'★ {product_code}' if id_product in existing_ids else product_code
            self._products_map[product_code] = id_product
            self._products_map[display_code] = id_product
            self._combo_display_map[product_code] = display_code
            display_values.append(display_code)

        self._combo['values'] = display_values

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
                self._load_existing_consumption_state()
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
        plain_code = code.lstrip('★').strip()
        if code in self._products_map or plain_code in self._products_map:
            id_product = self._products_map.get(code) or self._products_map.get(plain_code)
            self._set_product(id_product, plain_code)
            # Clear label status since user used combo
            self._lc_status.config(text='', fg=_C_SUBTEXT)
            self._load_existing_consumption_state()

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
        display_value = self._combo_display_map.get(product_code, product_code)
        self._combo_var.set(display_value)

    def _load_existing_consumption_state(self):
        """Highlight the product when a saved consumption already exists for the selected type."""
        if self._id_product is None:
            self._existing_consumption = None
            self._existing_lbl.config(text='', fg=_C_SUBTEXT)
            return

        mat_type = self._type_var.get()
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_CHECK_EXISTING, (self._id_product, mat_type))
            existing = cur.fetchone()
        except Exception as e:
            logger.error(f'MaterialConsumptionForm _load_existing_consumption_state: {e}')
            existing = None

        if existing:
            self._existing_consumption = {
                'id': existing.ProductConsumptionId,
                'gr': existing.MaterialConsumptionGR,
                'materiale_id': existing.MaterialeId,
                'date': existing.DateSys,
                'user': existing.User,
                'type': mat_type,
            }
            mat_display = self._materials_by_id.get(mat_type, {}).get(existing.MaterialeId, '')
            if mat_display:
                self._material_var.set(mat_display)
            else:
                self._material_var.set('')
            self._existing_lbl.config(
                text=(
                    f"✅ {mat_type} already set: {existing.MaterialConsumptionGR} gr"
                    f"  |  {self.lang.get('mat_cons_user', 'User')}: {existing.User or '—'}"
                    f"  |  {self.lang.get('mat_cons_date', 'Date')}: {str(existing.DateSys)[:19]}"
                ),
                fg=_C_SUCCESS
            )
            self._info_code_var.set(self._product_code)
            self._info_id_var.set(str(self._id_product))
        else:
            self._existing_consumption = None
            self._material_var.set('')
            self._existing_lbl.config(
                text=self.lang.get(
                    'mat_cons_no_existing',
                    'No saved consumption for this product and type.'
                ),
                fg=_C_SUBTEXT
            )

        # Make the selected product stand out when an existing value is present.
        if existing:
            self._info_code_var.set(f'● {self._product_code}')
            self._info_id_var.set(f'● {self._id_product}')
        else:
            self._info_code_var.set(self._product_code)
            self._info_id_var.set(str(self._id_product))

        # Rebuild combo labels when the selected type changes so markers stay accurate.
        if hasattr(self, '_combo') and self._all_products:
            self._refresh_products_combo()
            if self._product_code:
                self._combo_var.set(self._combo_display_map.get(self._product_code, self._product_code))

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

        # Materiale: obbligatorio se esistono materiali della famiglia del tipo selezionato
        materials_map = self._materials_map.get(mat_type, {})
        material_id = materials_map.get(self._material_var.get().strip())
        if self._materials_display.get(mat_type) and material_id is None:
            messagebox.showwarning(
                self.lang.get('warning', 'Warning'),
                self.lang.get('mat_cons_no_material', 'Selezionare un materiale dalla lista.'),
                parent=self
            )
            return

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
                        f"  Materiale: {self._materials_by_id.get(mat_type, {}).get(existing.MaterialeId, '—')}\n"
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
                material_id,
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
            self._load_existing_consumption_state()

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
