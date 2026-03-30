"""
indirect_materials_types.py
CRUD per la gestione dei TipoMateriali (ind.TipoMateriali).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class TipoMaterialiWindow(tk.Toplevel):
    """Finestra CRUD per gestire i tipi di materiale indiretto."""

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang

        self.title(lang.get('ind_types_title', 'Gestione Tipi Materiale'))
        self.geometry("700x450")
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_types()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(expand=True, fill="both")

        # Header
        ttk.Label(
            main,
            text=self.lang.get('ind_types_header', 'Tipi Materiale Indiretto'),
            font=("Segoe UI", 13, "bold")
        ).pack(fill="x", pady=(0, 10))

        # Treeview
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ('id', 'tipo', 'frazionabile', 'confezione')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('tipo', text=self.lang.get('ind_types_col_name', 'Tipo'))
        self.tree.heading('frazionabile', text=self.lang.get('ind_req_col_fractional', 'Frazionabile'))
        self.tree.heading('confezione', text=self.lang.get('ind_req_col_package', 'Confezione'))

        self.tree.column('id', width=50)
        self.tree.column('tipo', width=250)
        self.tree.column('frazionabile', width=100, anchor="center")
        self.tree.column('confezione', width=100, anchor="e")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Form
        form = ttk.LabelFrame(main, text=self.lang.get('ind_types_detail', 'Dettaglio'), padding=10)
        form.pack(fill="x")

        ttk.Label(form, text=self.lang.get('ind_types_col_name', 'Tipo:')).grid(row=0, column=0, sticky="w", padx=5)
        self.tipo_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.tipo_var, width=30).grid(row=0, column=1, padx=5)

        self.fraz_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form,
            text=self.lang.get('ind_req_col_fractional', 'Frazionabile'),
            variable=self.fraz_var
        ).grid(row=0, column=2, padx=10)

        ttk.Label(form, text=self.lang.get('ind_req_col_package', 'Confezione:')).grid(row=0, column=3, sticky="w", padx=5)
        self.confezione_var = tk.StringVar(value="1")
        ttk.Entry(form, textvariable=self.confezione_var, width=8).grid(row=0, column=4, padx=5)

        # Bottoni
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=0, columnspan=5, pady=(10, 0))

        ttk.Button(btn_frame, text=self.lang.get('ind_types_btn_add', '➕ Aggiungi'), command=self._add).pack(side="left", padx=3)
        ttk.Button(btn_frame, text=self.lang.get('ind_types_btn_save', '💾 Salva'), command=self._save).pack(side="left", padx=3)
        ttk.Button(btn_frame, text=self.lang.get('ind_types_btn_delete', '🗑️ Elimina'), command=self._delete).pack(side="left", padx=3)
        ttk.Button(btn_frame, text=self.lang.get('btn_refresh', '🔄 Aggiorna'), command=self._load_types).pack(side="left", padx=3)

        self._selected_id = None

    def _load_types(self):
        self.tree.delete(*self.tree.get_children())
        self._selected_id = None
        self._clear_form()
        try:
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(
                    "SELECT TipoMaterialeId, Tipo, IsFrazionabile, QtaConfezione FROM ind.TipoMateriali ORDER BY Tipo"
                )
                rows = self.db.cursor.fetchall()
            for row in (rows or []):
                fraz = "Sì" if row[2] else "No"
                self.tree.insert('', 'end', iid=str(row[0]), values=(
                    row[0], row[1] or '', fraz, f"{row[3]:.2f}" if row[3] else '1.00'
                ))
        except Exception as e:
            logger.error(f"Errore caricamento tipi: {e}", exc_info=True)

    def _on_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        self._selected_id = int(selection[0])
        values = self.tree.item(selection[0], 'values')
        self.tipo_var.set(values[1])
        self.fraz_var.set(values[2] == "Sì")
        self.confezione_var.set(values[3])

    def _clear_form(self):
        self.tipo_var.set("")
        self.fraz_var.set(False)
        self.confezione_var.set("1")
        self._selected_id = None

    def _add(self):
        tipo = self.tipo_var.get().strip()
        if not tipo:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'), 'Inserire il nome del tipo.', parent=self)
            return
        try:
            confezione = float(self.confezione_var.get().replace(',', '.'))
        except ValueError:
            confezione = 1.0

        try:
            self.db.execute_query(
                "INSERT INTO ind.TipoMateriali (Tipo, IsFrazionabile, QtaConfezione) VALUES (?, ?, ?)",
                (tipo, 1 if self.fraz_var.get() else 0, confezione)
            )
            self._load_types()
            self._clear_form()
            logger.info(f"Tipo materiale aggiunto: {tipo}")
        except Exception as e:
            logger.error(f"Errore aggiunta tipo: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _save(self):
        if self._selected_id is None:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'), 'Selezionare un tipo da modificare.', parent=self)
            return
        tipo = self.tipo_var.get().strip()
        if not tipo:
            return
        try:
            confezione = float(self.confezione_var.get().replace(',', '.'))
        except ValueError:
            confezione = 1.0

        try:
            self.db.execute_query(
                "UPDATE ind.TipoMateriali SET Tipo = ?, IsFrazionabile = ?, QtaConfezione = ? WHERE TipoMaterialeId = ?",
                (tipo, 1 if self.fraz_var.get() else 0, confezione, self._selected_id)
            )
            self._load_types()
            logger.info(f"Tipo materiale aggiornato: {self._selected_id} → {tipo}")
        except Exception as e:
            logger.error(f"Errore aggiornamento tipo: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _delete(self):
        if self._selected_id is None:
            return
        # Controlla se in uso
        used = self.db.fetch_one(
            "SELECT COUNT(*) FROM ind.Materiali WHERE TipoMaterialeId = ?", (self._selected_id,)
        )
        if used and used[0] > 0:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('ind_types_in_use', 'Tipo in uso da {0} materiali. Non eliminabile.').format(used[0]),
                parent=self
            )
            return

        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'), 'Eliminare il tipo selezionato?', parent=self):
            return
        try:
            self.db.execute_query(
                "DELETE FROM ind.TipoMateriali WHERE TipoMaterialeId = ?", (self._selected_id,)
            )
            self._load_types()
            self._clear_form()
            logger.info(f"Tipo materiale eliminato: {self._selected_id}")
        except Exception as e:
            logger.error(f"Errore eliminazione tipo: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


def open_tipo_materiali(master, db, lang):
    """Entry-point richiamabile da main.py."""
    TipoMaterialiWindow(master, db, lang)
