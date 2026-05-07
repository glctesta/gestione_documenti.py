"""
Gestione Check Errati — Permette la cancellazione di verifiche prodotto
inserite erroneamente nella coda PeriodicalProductCheckMustLists.

Mostra solo le verifiche ancora da eseguire (senza record in PeriodicalProductCheckLogs)
e consente la rimozione con autorizzazione.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger("TraceabilityRS")


class ManageWrongChecksWindow(tk.Toplevel):
    """Finestra per la gestione e cancellazione di verifiche prodotto errate."""

    def __init__(self, parent, db_handler, lang_manager, user_name="Unknown"):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name

        self.title(self.lang.get('wrong_checks_title', 'Gestione Check Errati'))
        self.geometry('950x550')
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_pending_checks()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(expand=True, fill="both")

        # Header
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 8))

        ttk.Label(
            header,
            text=self.lang.get('wrong_checks_header',
                               'Verifiche in attesa — selezionare e cancellare quelle errate'),
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        ttk.Label(
            header,
            text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
            font=("Segoe UI", 10)
        ).pack(side="right")

        # Treeview
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill="both", expand=True)

        columns = ('id', 'order', 'product', 'phase', 'date', 'time')
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show='headings',
            selectmode='extended', height=20
        )

        self.tree.heading('id', text='ID')
        self.tree.heading('order', text=self.lang.get('order', 'Ordine'))
        self.tree.heading('product', text=self.lang.get('product', 'Prodotto'))
        self.tree.heading('phase', text=self.lang.get('phase', 'Fase'))
        self.tree.heading('date', text=self.lang.get('date', 'Data'))
        self.tree.heading('time', text=self.lang.get('time', 'Ora'))

        self.tree.column('id', width=60, anchor='center')
        self.tree.column('order', width=140)
        self.tree.column('product', width=160)
        self.tree.column('phase', width=200)
        self.tree.column('date', width=110, anchor='center')
        self.tree.column('time', width=80, anchor='center')

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Bottoni
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_delete = ttk.Button(
            btn_frame,
            text=self.lang.get('wrong_checks_btn_delete', '🗑️ Cancella selezionati'),
            command=self._delete_selected,
            state='disabled'
        )
        self.btn_delete.pack(side="left", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
            command=self._load_pending_checks
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            btn_frame,
            text=self.lang.get('btn_close', 'Chiudi'),
            command=self.destroy
        ).pack(side="right")

        # Status bar
        self.status_var = tk.StringVar(value="")
        ttk.Label(main, textvariable=self.status_var, relief="sunken", anchor="w").pack(
            fill="x", pady=(5, 0))

        # Abilita bottone cancella quando c'è una selezione
        self.tree.bind('<<TreeviewSelect>>', self._on_selection_changed)

    # ------------------------------------------------------------------ #
    #  Caricamento dati                                                    #
    # ------------------------------------------------------------------ #
    def _load_pending_checks(self):
        """Carica le verifiche in attesa (senza log associato)."""
        self.tree.delete(*self.tree.get_children())
        self.btn_delete.state(['disabled'])

        try:
            pending = self.db.fetch_products_must_check()
            for p in pending:
                self.tree.insert('', 'end', values=(
                    p.PeriodicalProductCheckMustListId,
                    p.ordernumber,
                    p.productcode,
                    p.PhaseName,
                    p.Date,
                    p.Ora
                ))

            count = len(pending)
            self.status_var.set(
                f"{count} {self.lang.get('wrong_checks_pending', 'verifiche in attesa')}"
            )
            logger.info(f"ManageWrongChecks: caricate {count} verifiche in attesa")

        except Exception as e:
            logger.error(f"ManageWrongChecks: errore caricamento: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wrong_checks_load_error', 'Errore caricamento verifiche')}:\n{e}",
                parent=self
            )

    # ------------------------------------------------------------------ #
    #  Cancellazione                                                       #
    # ------------------------------------------------------------------ #
    def _on_selection_changed(self, event=None):
        sel = self.tree.selection()
        if sel:
            self.btn_delete.state(['!disabled'])
        else:
            self.btn_delete.state(['disabled'])

    def _delete_selected(self):
        """Cancella le verifiche selezionate da PeriodicalProductCheckMustLists."""
        selection = self.tree.selection()
        if not selection:
            return

        count = len(selection)
        # Raccogli info per il messaggio di conferma
        details = []
        ids_to_delete = []
        for sel_item in selection:
            vals = self.tree.item(sel_item, 'values')
            ids_to_delete.append(int(vals[0]))
            details.append(f"  • {vals[1]} / {vals[2]} — {vals[3]}")

        confirm_msg = self.lang.get(
            'wrong_checks_confirm_delete',
            'Cancellare {0} verifiche selezionate?\n\n{1}\n\nQuesta operazione è irreversibile.'
        ).format(count, '\n'.join(details[:10]))  # max 10 dettagli

        if count > 10:
            confirm_msg += f"\n  ... e altre {count - 10}"

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            confirm_msg,
            icon='warning',
            parent=self
        ):
            return

        # Esegui cancellazione
        deleted = 0
        errors = 0
        try:
            self.db._ensure_connection()
            with self.db._lock:
                cursor = self.db.cursor
                self.db.conn.autocommit = False
                try:
                    for must_id in ids_to_delete:
                        try:
                            # Verifica che non ci siano log associati (sicurezza)
                            cursor.execute(
                                "SELECT COUNT(*) FROM [dbo].[PeriodicalProductCheckLogs] "
                                "WHERE PeriodicalProductCheckMustListId = ?",
                                (must_id,)
                            )
                            log_count = cursor.fetchone()[0]
                            if log_count > 0:
                                logger.warning(
                                    f"ManageWrongChecks: skip ID {must_id} — ha {log_count} log associati"
                                )
                                errors += 1
                                continue

                            cursor.execute(
                                "DELETE FROM [dbo].[PeriodicalProductCheckMustLists] "
                                "WHERE PeriodicalProductCheckMustListId = ?",
                                (must_id,)
                            )
                            deleted += 1
                        except Exception as e:
                            logger.error(f"ManageWrongChecks: errore DELETE ID {must_id}: {e}")
                            errors += 1

                    self.db.conn.commit()
                    logger.info(
                        f"ManageWrongChecks: cancellate {deleted} verifiche "
                        f"(errori: {errors}) da utente {self.user_name}"
                    )
                except Exception as e:
                    self.db.conn.rollback()
                    raise
                finally:
                    self.db.conn.autocommit = True

        except Exception as e:
            logger.error(f"ManageWrongChecks: errore transazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('wrong_checks_delete_error', 'Errore durante la cancellazione')}:\n{e}",
                parent=self
            )
            return

        # Feedback
        msg = self.lang.get(
            'wrong_checks_deleted_ok',
            '{0} verifiche cancellate con successo.'
        ).format(deleted)
        if errors > 0:
            msg += f"\n{errors} {self.lang.get('wrong_checks_skipped', 'saltate (hanno log associati)')}"

        messagebox.showinfo(
            self.lang.get('success', 'Successo'),
            msg,
            parent=self
        )
        self._load_pending_checks()


def open_manage_wrong_checks(master, db, lang, user_name="Unknown"):
    """Entry-point richiamabile da main.py."""
    ManageWrongChecksWindow(master, db, lang, user_name)
