"""
material_configurations.py
CRUD per la gestione delle configurazioni materiali (dbo.MaterialConfigurations).
Permette di assegnare IsFractionabil e QuantityStandard ai codici di ind.Materiali.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class MaterialConfigurationsWindow(tk.Toplevel):
    """Finestra CRUD per gestire le configurazioni materiali."""

    def __init__(self, master, db, lang, user_name='Unknown'):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(lang.get('mat_config_title', 'Configurazione Codici Materiale'))
        self.geometry("950x550")
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._selected_config_id = None
        self._selected_material_id = None

        self._build_ui()
        self._load_data()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(expand=True, fill="both")

        # Header
        ttk.Label(
            main,
            text=self.lang.get('mat_config_header', 'Configurazione Codici Materiale'),
            font=("Segoe UI", 13, "bold")
        ).pack(fill="x", pady=(0, 10))

        # Filtri
        filter_frame = ttk.LabelFrame(main, text=self.lang.get('mat_config_filters', 'Filtri'), padding=5)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text=self.lang.get('mat_config_filter_code', 'Codice:')).pack(side="left", padx=5)
        self.filter_code_var = tk.StringVar()
        self.filter_code_var.trace_add('write', lambda *a: self._apply_filter())
        ttk.Entry(filter_frame, textvariable=self.filter_code_var, width=15).pack(side="left", padx=5)

        ttk.Label(filter_frame, text=self.lang.get('mat_config_filter_desc', 'Descrizione:')).pack(side="left", padx=5)
        self.filter_desc_var = tk.StringVar()
        self.filter_desc_var.trace_add('write', lambda *a: self._apply_filter())
        ttk.Entry(filter_frame, textvariable=self.filter_desc_var, width=25).pack(side="left", padx=5)

        # Checkbox per mostrare solo configurati
        self.show_configured_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filter_frame,
            text=self.lang.get('mat_config_show_configured', 'Solo configurati'),
            variable=self.show_configured_only_var,
            command=self._apply_filter
        ).pack(side="left", padx=10)

        ttk.Button(filter_frame, text='🔄', command=self._load_data, width=3).pack(side="right", padx=5)

        # Treeview
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ('material_id', 'code', 'description', 'fractionable', 'qty_standard', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('material_id', text='ID')
        self.tree.heading('code', text=self.lang.get('mat_config_col_code', 'Codice'))
        self.tree.heading('description', text=self.lang.get('mat_config_col_desc', 'Descrizione'))
        self.tree.heading('fractionable', text=self.lang.get('mat_config_col_fract', 'Frazionabile'))
        self.tree.heading('qty_standard', text=self.lang.get('mat_config_col_qty', 'Qtà Standard'))
        self.tree.heading('status', text=self.lang.get('mat_config_col_status', 'Stato'))

        self.tree.column('material_id', width=50, anchor="center")
        self.tree.column('code', width=150)
        self.tree.column('description', width=300)
        self.tree.column('fractionable', width=100, anchor="center")
        self.tree.column('qty_standard', width=100, anchor="e")
        self.tree.column('status', width=80, anchor="center")

        # Tag per righe disattivate
        self.tree.tag_configure('inactive', foreground='gray')
        self.tree.tag_configure('configured', background='#e8f5e9')

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Form
        form = ttk.LabelFrame(main, text=self.lang.get('mat_config_detail', 'Dettaglio Configurazione'), padding=10)
        form.pack(fill="x")

        # Riga 1: Codice e Descrizione (read-only)
        ttk.Label(form, text=self.lang.get('mat_config_col_code', 'Codice:')).grid(row=0, column=0, sticky="w", padx=5)
        self.code_label = ttk.Label(form, text="", font=("Segoe UI", 10, "bold"))
        self.code_label.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(form, text=self.lang.get('mat_config_col_desc', 'Descrizione:')).grid(row=0, column=2, sticky="w", padx=5)
        self.desc_label = ttk.Label(form, text="", wraplength=300)
        self.desc_label.grid(row=0, column=3, sticky="w", padx=5)

        # Riga 2: IsFractionabil e QuantityStandard
        self.fraz_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form,
            text=self.lang.get('mat_config_col_fract', 'Frazionabile'),
            variable=self.fraz_var
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(form, text=self.lang.get('mat_config_col_qty', 'Qtà Standard:')).grid(row=1, column=2, sticky="w", padx=5)
        self.qty_var = tk.StringVar(value="1")
        ttk.Entry(form, textvariable=self.qty_var, width=10).grid(row=1, column=3, sticky="w", padx=5)

        # Bottoni
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text=self.lang.get('mat_config_btn_save', '💾 Salva Configurazione'),
            command=self._save
        ).pack(side="left", padx=3)
        ttk.Button(
            btn_frame,
            text=self.lang.get('mat_config_btn_delete', '🗑️ Disattiva'),
            command=self._soft_delete
        ).pack(side="left", padx=3)
        ttk.Button(
            btn_frame,
            text=self.lang.get('mat_config_btn_restore', '♻️ Riattiva'),
            command=self._restore
        ).pack(side="left", padx=3)

        # Contatore
        self.count_label = ttk.Label(main, text="", font=("Segoe UI", 8))
        self.count_label.pack(fill="x", pady=(5, 0))

    def _load_data(self):
        """Carica tutti i materiali con le relative configurazioni."""
        self.tree.delete(*self.tree.get_children())
        self._selected_config_id = None
        self._selected_material_id = None
        self._clear_form()
        self._all_rows = []

        try:
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute("""
                    SELECT m.MaterialeId, m.CodiceMateriale, m.DescrizioneMateriale,
                           mc.MaterialConfigurationId, mc.IsFractionabil, mc.QuantityStandard, mc.DateOut
                    FROM ind.Materiali m
                    LEFT JOIN dbo.MaterialConfigurations mc 
                        ON mc.MaterialId = m.MaterialeId AND mc.DateOut IS NULL
                    WHERE m.IsActive = 1
                    ORDER BY m.CodiceMateriale
                """)
                self._all_rows = self.db.cursor.fetchall() or []
        except Exception as e:
            logger.error(f"Errore caricamento configurazioni materiali: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento dati:\n{e}",
                parent=self
            )

        self._apply_filter()

    def _apply_filter(self, *args):
        """Applica i filtri correnti alla treeview."""
        self.tree.delete(*self.tree.get_children())
        code_filter = self.filter_code_var.get().strip().lower()
        desc_filter = self.filter_desc_var.get().strip().lower()
        show_configured = self.show_configured_only_var.get()

        count = 0
        for row in self._all_rows:
            material_id, code, desc, config_id, is_fract, qty_std, date_out = row
            code = code or ''
            desc = desc or ''

            # Filtro testo
            if code_filter and code_filter not in code.lower():
                continue
            if desc_filter and desc_filter not in desc.lower():
                continue

            # Filtro solo configurati
            if show_configured and config_id is None:
                continue

            # Formatta valori
            if config_id is not None:
                fraz_display = "Sì" if is_fract else "No"
                qty_display = f"{qty_std:.2f}" if qty_std is not None else "1.00"
                status = self.lang.get('mat_config_status_active', 'Attivo')
                tags = ('configured',)
            else:
                fraz_display = "-"
                qty_display = "-"
                status = self.lang.get('mat_config_status_none', 'Non config.')
                tags = ()

            self.tree.insert('', 'end', iid=str(material_id), values=(
                material_id, code, desc, fraz_display, qty_display, status
            ), tags=tags)
            count += 1

        self.count_label.config(
            text=self.lang.get('mat_config_count', 'Visualizzati: {count} materiali').format(count=count)
        )

    def _on_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        self._selected_material_id = int(selection[0])
        values = self.tree.item(selection[0], 'values')

        self.code_label.config(text=values[1])
        self.desc_label.config(text=values[2])

        # Cerca la configurazione nella cache
        for row in self._all_rows:
            if row[0] == self._selected_material_id:
                config_id, is_fract, qty_std, date_out = row[3], row[4], row[5], row[6]
                if config_id is not None:
                    self._selected_config_id = config_id
                    self.fraz_var.set(bool(is_fract))
                    self.qty_var.set(f"{qty_std:.2f}" if qty_std is not None else "1")
                else:
                    self._selected_config_id = None
                    self.fraz_var.set(False)
                    self.qty_var.set("1")
                break

    def _clear_form(self):
        self.code_label.config(text="")
        self.desc_label.config(text="")
        self.fraz_var.set(False)
        self.qty_var.set("1")
        self._selected_config_id = None
        self._selected_material_id = None

    def _save(self):
        """Salva o aggiorna la configurazione per il materiale selezionato."""
        if self._selected_material_id is None:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('mat_config_select_material', 'Selezionare un materiale dalla lista.'),
                parent=self
            )
            return

        try:
            qty = float(self.qty_var.get().replace(',', '.'))
            if qty <= 0:
                raise ValueError("Quantità deve essere positiva")
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('mat_config_invalid_qty', 'Inserire una quantità standard valida (numero positivo).'),
                parent=self
            )
            return

        is_fract = 1 if self.fraz_var.get() else 0

        try:
            if self._selected_config_id is not None:
                # UPDATE configurazione esistente
                self.db.execute_query(
                    """UPDATE dbo.MaterialConfigurations 
                       SET IsFractionabil = ?, QuantityStandard = ?
                       WHERE MaterialConfigurationId = ?""",
                    (is_fract, qty, self._selected_config_id)
                )
                logger.info(
                    f"Configurazione materiale aggiornata: ConfigId={self._selected_config_id}, "
                    f"MaterialId={self._selected_material_id}, IsFract={is_fract}, Qty={qty}"
                )
            else:
                # INSERT nuova configurazione
                self.db.execute_query(
                    """INSERT INTO dbo.MaterialConfigurations 
                       (MaterialId, IsFractionabil, QuantityStandard)
                       VALUES (?, ?, ?)""",
                    (self._selected_material_id, is_fract, qty)
                )
                logger.info(
                    f"Configurazione materiale creata: MaterialId={self._selected_material_id}, "
                    f"IsFract={is_fract}, Qty={qty}"
                )

            self._load_data()
            # Riseleziona il materiale appena salvato
            try:
                self.tree.selection_set(str(self._selected_material_id))
                self.tree.see(str(self._selected_material_id))
                self._on_select()
            except tk.TclError:
                pass

        except Exception as e:
            logger.error(f"Errore salvataggio configurazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore salvataggio:\n{e}",
                parent=self
            )

    def _soft_delete(self):
        """Disattiva (soft-delete) la configurazione selezionata."""
        if self._selected_config_id is None:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('mat_config_no_config', 'Nessuna configurazione attiva da disattivare per questo materiale.'),
                parent=self
            )
            return

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('mat_config_confirm_delete', 'Disattivare la configurazione per questo materiale?'),
            parent=self
        ):
            return

        try:
            self.db.execute_query(
                "UPDATE dbo.MaterialConfigurations SET DateOut = GETDATE() WHERE MaterialConfigurationId = ?",
                (self._selected_config_id,)
            )
            logger.info(f"Configurazione materiale disattivata: ConfigId={self._selected_config_id}")
            self._load_data()
        except Exception as e:
            logger.error(f"Errore disattivazione configurazione: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _restore(self):
        """Riattiva una configurazione soft-deleted cercandola per MaterialId."""
        if self._selected_material_id is None:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('mat_config_select_material', 'Selezionare un materiale dalla lista.'),
                parent=self
            )
            return

        try:
            # Cerca configurazione disattivata per questo materiale
            row = self.db.fetch_one(
                """SELECT MaterialConfigurationId FROM dbo.MaterialConfigurations 
                   WHERE MaterialId = ? AND DateOut IS NOT NULL
                   ORDER BY DateOut DESC""",
                (self._selected_material_id,)
            )
            if row:
                self.db.execute_query(
                    "UPDATE dbo.MaterialConfigurations SET DateOut = NULL WHERE MaterialConfigurationId = ?",
                    (row[0],)
                )
                logger.info(f"Configurazione materiale riattivata: ConfigId={row[0]}")
                self._load_data()
                try:
                    self.tree.selection_set(str(self._selected_material_id))
                    self.tree.see(str(self._selected_material_id))
                    self._on_select()
                except tk.TclError:
                    pass
            else:
                messagebox.showinfo(
                    self.lang.get('info', 'Info'),
                    self.lang.get('mat_config_no_inactive', 'Nessuna configurazione disattivata trovata per questo materiale.'),
                    parent=self
                )
        except Exception as e:
            logger.error(f"Errore riattivazione configurazione: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


def open_material_configurations(master, db, lang, user_name='Unknown'):
    """Entry-point richiamabile da main.py."""
    MaterialConfigurationsWindow(master, db, lang, user_name)
