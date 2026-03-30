"""
indirect_materials_request.py
Form per richiedere materiali indiretti con filtri, validazione quantità
e invio richiesta al WH tramite DB.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import socket
from datetime import datetime

logger = logging.getLogger(__name__)

NOTIFY_INTERVAL_MS = 10_000       # Polling ogni 10s
RE_NOTIFY_MINUTES = 5             # Ri-notifica ogni 5 minuti se non azionato


class RequestIndirectMaterialsWindow(tk.Toplevel):
    """Form per richiedere materiali indiretti."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.hostname = socket.gethostname()

        self.title(lang.get('ind_req_title', 'Richiesta Materiali Indiretti'))
        self.geometry("900x600")
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._selected_material = None

        self._build_ui()
        self._load_materials()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(expand=True, fill="both")

        # Header
        ttk.Label(
            main,
            text=self.lang.get('ind_req_header', 'Richiesta Materiali Indiretti'),
            font=("Segoe UI", 13, "bold")
        ).pack(fill="x", pady=(0, 10))

        # --- Filtri ---
        filter_frame = ttk.LabelFrame(main, text=self.lang.get('ind_req_filters', 'Filtri'), padding=5)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text=self.lang.get('ind_req_filter_code', 'Codice:')).grid(row=0, column=0, padx=5)
        self.filter_code_var = tk.StringVar()
        code_entry = ttk.Entry(filter_frame, textvariable=self.filter_code_var, width=20)
        code_entry.grid(row=0, column=1, padx=5)
        code_entry.bind('<KeyRelease>', lambda e: self._filter_materials())

        ttk.Label(filter_frame, text=self.lang.get('ind_req_filter_desc', 'Descrizione:')).grid(row=0, column=2, padx=5)
        self.filter_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(filter_frame, textvariable=self.filter_desc_var, width=30)
        desc_entry.grid(row=0, column=3, padx=5)
        desc_entry.bind('<KeyRelease>', lambda e: self._filter_materials())

        ttk.Button(
            filter_frame,
            text=self.lang.get('ind_req_btn_clear', 'Pulisci'),
            command=self._clear_filters
        ).grid(row=0, column=4, padx=10)

        # --- Treeview materiali ---
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ('codice', 'descrizione', 'tipo', 'stock', 'confezione', 'frazionabile')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('codice', text=self.lang.get('ind_import_col_code', 'Codice'))
        self.tree.heading('descrizione', text=self.lang.get('ind_import_col_desc', 'Descrizione'))
        self.tree.heading('tipo', text=self.lang.get('ind_req_col_type', 'Tipo'))
        self.tree.heading('stock', text=self.lang.get('ind_req_col_stock', 'Stock'))
        self.tree.heading('confezione', text=self.lang.get('ind_req_col_package', 'Confezione'))
        self.tree.heading('frazionabile', text=self.lang.get('ind_req_col_fractional', 'Frazionabile'))

        self.tree.column('codice', width=120)
        self.tree.column('descrizione', width=300)
        self.tree.column('tipo', width=100)
        self.tree.column('stock', width=80, anchor="e")
        self.tree.column('confezione', width=80, anchor="e")
        self.tree.column('frazionabile', width=80, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind('<<TreeviewSelect>>', self._on_material_selected)

        # --- Quantità e invio ---
        req_frame = ttk.LabelFrame(main, text=self.lang.get('ind_req_request', 'Richiesta'), padding=10)
        req_frame.pack(fill="x")

        self.selected_label_var = tk.StringVar(value=self.lang.get('ind_req_no_selection', 'Seleziona un materiale dalla lista'))
        ttk.Label(req_frame, textvariable=self.selected_label_var, font=("Segoe UI", 10)).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        ttk.Label(req_frame, text=self.lang.get('ind_req_qty', 'Quantità:')).grid(row=1, column=0, padx=5, sticky="w")
        self.qty_var = tk.StringVar(value="1")
        self.qty_entry = ttk.Entry(req_frame, textvariable=self.qty_var, width=10)
        self.qty_entry.grid(row=1, column=1, padx=5)

        self.btn_send = ttk.Button(
            req_frame,
            text=self.lang.get('ind_req_btn_send', 'Invia Richiesta'),
            command=self._send_request,
            state="disabled"
        )
        self.btn_send.grid(row=1, column=2, padx=20)

        # Storico
        ttk.Button(
            req_frame,
            text=self.lang.get('ind_req_btn_history', 'Storico Richieste'),
            command=self._open_history
        ).grid(row=1, column=3, padx=5)

        # Info validazione
        self.validation_var = tk.StringVar(value="")
        ttk.Label(req_frame, textvariable=self.validation_var, foreground="gray").grid(row=2, column=0, columnspan=4, sticky="w", pady=(5, 0))

    # ------------------------------------------------------------------ #
    #  Caricamento e filtro materiali                                       #
    # ------------------------------------------------------------------ #
    def _load_materials(self):
        """Carica materiali attivi con stock attivo dal DB.
        Se esiste una MaterialConfiguration per il materiale, usa i valori
        IsFractionabil e QuantityStandard da lì (override per-codice).
        Altrimenti usa i valori da TipoMateriali (default per-tipo)."""
        try:
            query = """
                SELECT m.MaterialeId, m.CodiceMateriale, m.DescrizioneMateriale,
                       ISNULL(t.Tipo, 'Generico') AS Tipo,
                       ISNULL(s.Qty, 0) AS QtaStock,
                       ISNULL(t.QtaConfezione, 1) AS QtaConfezione,
                       ISNULL(t.IsFrazionabile, 0) AS IsFrazionabile,
                       t.TipoMaterialeId,
                       mc.IsFractionabil,
                       mc.QuantityStandard
                FROM ind.Materiali m
                LEFT JOIN ind.TipoMateriali t ON m.TipoMaterialeId = t.TipoMaterialeId
                LEFT JOIN ind.MaterialiStock s ON m.MaterialeId = s.MaterialeId AND s.DateOut IS NULL
                LEFT JOIN dbo.MaterialConfigurations mc
                    ON mc.MaterialId = m.MaterialeId AND mc.DateOut IS NULL
                WHERE m.IsActive = 1
                ORDER BY m.CodiceMateriale
            """
            result = self.db.fetch_all(query) if hasattr(self.db, 'fetch_all') else self._fetch_all(query)
            self._all_materials = []
            for row in (result or []):
                # MaterialConfigurations override (per-codice) se presente
                mc_is_fract = row[8]    # mc.IsFractionabil (None se non configurato)
                mc_qty_std = row[9]     # mc.QuantityStandard (None se non configurato)
                has_config = mc_is_fract is not None

                if has_config:
                    frazionabile = bool(mc_is_fract)
                    confezione = float(mc_qty_std) if mc_qty_std else 1.0
                else:
                    frazionabile = bool(row[6])
                    confezione = float(row[5] or 1)

                self._all_materials.append({
                    'id': row[0],
                    'codice': row[1] or '',
                    'descrizione': row[2] or '',
                    'tipo': row[3] or 'Generico',
                    'stock': float(row[4] or 0),
                    'confezione': confezione,
                    'frazionabile': frazionabile,
                    'has_config': has_config,
                })
            self._filter_materials()
        except Exception as e:
            logger.error(f"Errore caricamento materiali: {e}", exc_info=True)
            self._all_materials = []

    def _fetch_all(self, query, params=None):
        """Fallback se db non ha fetch_all."""
        self.db._ensure_connection()
        with self.db._lock:
            if params:
                self.db.cursor.execute(query, params)
            else:
                self.db.cursor.execute(query)
            return self.db.cursor.fetchall()

    def _filter_materials(self):
        """Filtra materiali in base ai campi filtro."""
        self.tree.delete(*self.tree.get_children())
        code_filter = self.filter_code_var.get().strip().lower()
        desc_filter = self.filter_desc_var.get().strip().lower()

        self._filtered_materials = []
        for m in self._all_materials:
            if code_filter and code_filter not in m['codice'].lower():
                continue
            if desc_filter and desc_filter not in m['descrizione'].lower():
                continue
            fraz_text = "Sì" if m['frazionabile'] else "No"
            idx = len(self._filtered_materials)
            self.tree.insert('', 'end', iid=str(idx), values=(
                m['codice'], m['descrizione'], m['tipo'],
                f"{m['stock']:.2f}", f"{m['confezione']:.0f}", fraz_text
            ))
            self._filtered_materials.append(m)

    def _clear_filters(self):
        self.filter_code_var.set("")
        self.filter_desc_var.set("")
        self._filter_materials()

    # ------------------------------------------------------------------ #
    #  Selezione e validazione                                              #
    # ------------------------------------------------------------------ #
    def _on_material_selected(self, event=None):
        selection = self.tree.selection()
        if not selection:
            self._selected_material = None
            self.btn_send.state(["disabled"])
            self.qty_entry.config(state='normal')
            return

        idx = int(selection[0])
        self._selected_material = self._filtered_materials[idx] if idx < len(self._filtered_materials) else None

        if self._selected_material:
            m = self._selected_material
            self.selected_label_var.set(f"📦 {m['codice']} - {m['descrizione']}  |  Stock: {m['stock']:.2f}")

            qty_std = m['confezione']

            stock = m['stock']
            self.qty_entry.config(state='normal')

            if m['frazionabile']:
                # Frazionabile: qty editabile, massimo = stock
                self.qty_var.set(str(int(qty_std)))
                self.validation_var.set(
                    self.lang.get('ind_req_fraz_rule_config',
                                  'Quantità editabile, massimo {0} (stock disponibile).').format(int(stock))
                )
            else:
                # Non frazionabile: qty editabile, multiplo di confezione, massimo = stock
                self.qty_var.set(str(int(qty_std)))
                max_packs = int(stock // qty_std) if qty_std > 0 else 0
                max_qty = max_packs * int(qty_std)
                self.validation_var.set(
                    self.lang.get('ind_req_nonfraz_rule_config',
                                  'Quantità deve essere multiplo di {0}. Massimo: {1} (stock disponibile).').format(int(qty_std), int(max_qty))
                )

            self.btn_send.state(["!disabled"])

    def _validate_qty(self):
        """Valida la quantità rispetto a MaterialConfigurations.
        Regole:
        - IsFractionabil=0: qty deve essere esattamente = QuantityStandard
        - IsFractionabil=1: qty deve essere multiplo di QuantityStandard e <= QuantityStandard
        - Stock deve essere >= qty richiesta
        - Qty rappresenta sempre un multiplo di QuantityStandard
        """
        if not self._selected_material:
            return False, "Nessun materiale selezionato"

        try:
            qty = float(self.qty_var.get().replace(',', '.'))
        except ValueError:
            return False, self.lang.get('ind_req_invalid_qty', 'Quantità non valida')

        if qty <= 0:
            return False, self.lang.get('ind_req_qty_positive', 'La quantità deve essere maggiore di 0')

        m = self._selected_material
        qty_standard = m['confezione']
        stock = m['stock']

        # Stock deve essere >= quantità richiesta
        if stock < qty:
            return False, self.lang.get(
                'ind_req_stock_insufficient',
                'Stock insufficiente. Disponibile: {0}, richiesto: {1}.'
            ).format(f"{stock:.2f}", f"{qty:.2f}")

        if not m['frazionabile']:
            # Non frazionabile: qty deve essere multiplo della confezione
            if qty_standard > 0 and qty % qty_standard != 0:
                return False, self.lang.get(
                    'ind_req_nonfraz_error_config',
                    'Materiale non frazionabile. La quantità deve essere un multiplo di {0}.'
                ).format(int(qty_standard))

        return True, qty

    # ------------------------------------------------------------------ #
    #  Invio richiesta                                                      #
    # ------------------------------------------------------------------ #
    def _send_request(self):
        valid, result = self._validate_qty()
        if not valid:
            messagebox.showerror(self.lang.get('error', 'Errore'), result, parent=self)
            return

        qty = result
        m = self._selected_material

        # Conferma
        confirm_msg = self.lang.get(
            'ind_req_confirm_send',
            'Inviare richiesta per:\n\n{0} - {1}\nQuantità: {2}'
        ).format(m['codice'], m['descrizione'], qty)

        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'), confirm_msg, parent=self):
            return

        try:
            # INSERT richiesta
            query = """
                INSERT INTO ind.MaterialiRichieste
                    (MaterialeId, QtaRichiesta, QtaStockAlMomento, Stato,
                     DataRichiesta, RichiestoDa, ComputerRichiedente)
                VALUES (?, ?, ?, 'RICHIESTA', GETDATE(), ?, ?)
            """
            success = self.db.execute_query(query, (
                m['id'], qty, m['stock'], self.user_name, self.hostname
            ))

            if success:
                messagebox.showinfo(
                    self.lang.get('info', 'Info'),
                    self.lang.get('ind_req_sent_ok', 'Richiesta inviata con successo!\nIl magazzino verrà notificato.'),
                    parent=self
                )
                logger.info(f"Richiesta materiale inviata: {m['codice']} x {qty} da {self.user_name}@{self.hostname}")
            else:
                raise Exception(self.db.last_error_details)

        except Exception as e:
            logger.error(f"Errore invio richiesta: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('ind_req_send_error', 'Errore invio richiesta')}:\n{e}",
                parent=self
            )

    # ------------------------------------------------------------------ #
    #  Storico                                                              #
    # ------------------------------------------------------------------ #
    def _open_history(self):
        RequestHistoryWindow(self, self.db, self.lang, self.user_name)


class RequestHistoryWindow(tk.Toplevel):
    """Finestra storico richieste materiali."""

    def __init__(self, master, db, lang, user_name):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get('ind_req_history_title', 'Storico Richieste Materiali'))
        self.geometry("1000x500")
        self.resizable(True, True)
        self.transient(master)

        self._build_ui()
        self._load_history()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(expand=True, fill="both")

        # Header
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 10))

        ttk.Label(
            header,
            text=self.lang.get('ind_req_history_header', 'Storico Richieste'),
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        ttk.Button(
            header,
            text=self.lang.get('btn_refresh', 'Aggiorna'),
            command=self._load_history
        ).pack(side="right", padx=5)

        ttk.Button(
            header,
            text=self.lang.get('ind_req_btn_reprint', 'Ristampa PDF'),
            command=self._reprint_selected
        ).pack(side="right", padx=5)

        # Treeview
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill="both", expand=True)

        columns = ('id', 'data', 'codice', 'descrizione', 'qty', 'stato', 'richiedente', 'preparatore')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('data', text=self.lang.get('ind_req_col_date', 'Data'))
        self.tree.heading('codice', text=self.lang.get('ind_import_col_code', 'Codice'))
        self.tree.heading('descrizione', text=self.lang.get('ind_import_col_desc', 'Descrizione'))
        self.tree.heading('qty', text=self.lang.get('ind_req_qty', 'Quantità'))
        self.tree.heading('stato', text=self.lang.get('ind_req_col_status', 'Stato'))
        self.tree.heading('richiedente', text=self.lang.get('ind_req_col_requester', 'Richiedente'))
        self.tree.heading('preparatore', text=self.lang.get('ind_req_col_preparer', 'Preparatore'))

        self.tree.column('id', width=50)
        self.tree.column('data', width=130)
        self.tree.column('codice', width=100)
        self.tree.column('descrizione', width=250)
        self.tree.column('qty', width=70, anchor="e")
        self.tree.column('stato', width=100)
        self.tree.column('richiedente', width=100)
        self.tree.column('preparatore', width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_history(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = """
                SELECT r.RichiestaId, r.DataRichiesta,
                       m.CodiceMateriale, m.DescrizioneMateriale,
                       r.QtaRichiesta, r.Stato, r.RichiestoDa, r.PreparatoDa
                FROM ind.MaterialiRichieste r
                JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
                ORDER BY r.DataRichiesta DESC
            """
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(query)
                rows = self.db.cursor.fetchall()

            for row in (rows or []):
                data_str = row[1].strftime('%d/%m/%Y %H:%M') if row[1] else ''
                self.tree.insert('', 'end', iid=str(row[0]), values=(
                    row[0], data_str, row[2] or '', row[3] or '',
                    f"{row[4]:.2f}" if row[4] else '0', row[5] or '',
                    row[6] or '', row[7] or ''
                ))
        except Exception as e:
            logger.error(f"Errore caricamento storico: {e}", exc_info=True)

    def _reprint_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ind_req_select_to_reprint', 'Seleziona una richiesta da ristampare'),
                parent=self
            )
            return

        richiesta_id = int(selection[0])
        try:
            from indirect_materials_pdf import generate_and_print_request_pdf
            generate_and_print_request_pdf(self.db, richiesta_id, print_now=True)
            messagebox.showinfo(
                self.lang.get('info', 'Info'),
                self.lang.get('ind_req_reprint_ok', 'PDF generato e inviato in stampa.'),
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore ristampa: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('ind_req_reprint_error', 'Errore ristampa')}:\n{e}",
                parent=self
            )


def open_request_indirect_materials(master, db, lang, user_name="Unknown"):
    """Entry-point richiamabile da main.py."""
    RequestIndirectMaterialsWindow(master, db, lang, user_name)
