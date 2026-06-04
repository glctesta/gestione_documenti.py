# -*- coding: utf-8 -*-
"""
Gestione badge visitatori / non dipendenti.

Permette di:
- inserire badge dedicati ai non dipendenti in Employee.dbo.Badges
- visualizzare se un badge e' disponibile o assegnato a un visitatore
- modificare il numero badge
- cancellare badge solo se non risultano assegnati attivamente
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger("TraceabilityRS")


class GuestBadgesWindow(tk.Toplevel):
    """Finestra gestione badge per non dipendenti."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self._selected_badge_id = None

        self.title(self.lang.get('guest_badges_title', 'Gestione Badges'))
        self.geometry('1080x620')
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_badges()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill='both', expand=True)

        toolbar = ttk.LabelFrame(
            main,
            text=self.lang.get('guest_badges_editor', 'Inserimento / Modifica Badge'),
            padding=10,
        )
        toolbar.pack(fill='x', pady=(0, 8))

        ttk.Label(toolbar, text=self.lang.get('badge_number', 'Numero Badge:')).grid(
            row=0, column=0, sticky='w', padx=5, pady=4
        )
        self.badge_number_var = tk.StringVar()
        self.badge_entry = ttk.Entry(toolbar, textvariable=self.badge_number_var, width=25)
        self.badge_entry.grid(row=0, column=1, sticky='w', padx=5, pady=4)

        ttk.Button(
            toolbar,
            text=self.lang.get('btn_new', 'Nuovo'),
            command=self._reset_form,
        ).grid(row=0, column=2, padx=5, pady=4)
        ttk.Button(
            toolbar,
            text=self.lang.get('btn_save', 'Salva'),
            command=self._save_badge,
        ).grid(row=0, column=3, padx=5, pady=4)
        ttk.Button(
            toolbar,
            text=self.lang.get('btn_delete', 'Elimina'),
            command=self._delete_badge,
        ).grid(row=0, column=4, padx=5, pady=4)
        ttk.Button(
            toolbar,
            text=self.lang.get('btn_refresh', 'Aggiorna'),
            command=self._load_badges,
        ).grid(row=0, column=5, padx=5, pady=4)

        self.status_var = tk.StringVar(value='')
        ttk.Label(toolbar, textvariable=self.status_var, foreground='gray').grid(
            row=1, column=0, columnspan=6, sticky='w', padx=5, pady=(6, 0)
        )

        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill='both', expand=True)

        columns = (
            'BadgeId', 'NoBadge', 'DateIn', 'Status',
            'GuestName', 'Phone', 'AssignedOn', 'ValidUpTo'
        )
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')

        labels = {
            'BadgeId': 'ID',
            'NoBadge': self.lang.get('badge_number', 'Numero Badge'),
            'DateIn': self.lang.get('date_in', 'Data Inserimento'),
            'Status': self.lang.get('status', 'Stato'),
            'GuestName': self.lang.get('col_guest_name', 'Ospite'),
            'Phone': self.lang.get('col_phone', 'Telefono'),
            'AssignedOn': self.lang.get('assigned_on', 'Assegnato Il'),
            'ValidUpTo': self.lang.get('valid_up_to', 'Valido Fino Al'),
        }
        widths = {
            'BadgeId': 60,
            'NoBadge': 130,
            'DateIn': 130,
            'Status': 110,
            'GuestName': 190,
            'Phone': 130,
            'AssignedOn': 130,
            'ValidUpTo': 130,
        }
        for col in columns:
            anchor = 'w' if col in ('NoBadge', 'GuestName', 'Phone') else 'center'
            self.tree.heading(col, text=labels[col])
            self.tree.column(col, width=widths[col], anchor=anchor)

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure('available', background='#d4edda')
        self.tree.tag_configure('assigned', background='#fff3cd')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_badges(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = """
                SELECT
                    b.BadgeId,
                    b.NoBadge,
                    b.DateIn,
                    vd.GuestName,
                    vd.TelephonNumber,
                    vb.DateIn AS AssignedOn,
                    vb.DateOut AS ValidUpTo
                FROM Employee.dbo.Badges b
                OUTER APPLY (
                    SELECT TOP 1 vbl.VisitorDataID, vbl.DateIn, vbl.DateOut
                    FROM Employee.dbo.VisitorBadgeLogs vbl
                    WHERE vbl.BadgeId = b.BadgeId
                      AND CAST(vbl.DateOut AS DATE) >= CAST(GETDATE() AS DATE)
                    ORDER BY vbl.DateOut DESC, vbl.DateIn DESC
                ) vb
                LEFT JOIN Employee.dbo.VisitorData vd
                    ON vd.VisitorDataID = vb.VisitorDataID
                                WHERE ISNULL(b.ForGuest, 0) = 1
                  AND ISNULL(b.EmployeerId, 2) = 2
                ORDER BY b.NoBadge
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            for row in rows:
                status = self.lang.get('badge_status_assigned', 'Assegnato') if row.GuestName else self.lang.get('badge_status_available', 'Disponibile')
                tag = 'assigned' if row.GuestName else 'available'
                date_in = row.DateIn.strftime('%d/%m/%Y %H:%M') if row.DateIn else ''
                assigned_on = row.AssignedOn.strftime('%d/%m/%Y %H:%M') if row.AssignedOn else ''
                valid_up_to = row.ValidUpTo.strftime('%d/%m/%Y') if row.ValidUpTo else ''
                self.tree.insert('', 'end', values=(
                    row.BadgeId,
                    row.NoBadge or '',
                    date_in,
                    status,
                    row.GuestName or '',
                    row.TelephonNumber or '',
                    assigned_on,
                    valid_up_to,
                ), tags=(tag,))

            self.status_var.set(
                self.lang.get('guest_badges_loaded', 'Badge caricati: {0}').format(len(rows))
            )
            self._reset_form(clear_status=False)
        except Exception as e:
            logger.error(f"Errore caricamento badge visitatori: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}", parent=self)

    def _reset_form(self, clear_status=True):
        self._selected_badge_id = None
        self.badge_number_var.set('')
        if clear_status:
            self.status_var.set('')
        self.tree.selection_remove(*self.tree.selection())
        self.badge_entry.focus_set()

    def _on_select(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], 'values')
        if not values:
            return
        self._selected_badge_id = int(values[0])
        self.badge_number_var.set(values[1])
        self.status_var.set(f"ID {values[0]} - {values[3]}")

    def _badge_exists(self, badge_number, exclude_badge_id=None):
        query = """
            SELECT TOP 1 BadgeId
            FROM Employee.dbo.Badges
            WHERE NoBadge COLLATE Latin1_General_CI_AI = ? COLLATE Latin1_General_CI_AI
        """
        params = [badge_number]
        if exclude_badge_id:
            query += " AND BadgeId <> ?"
            params.append(exclude_badge_id)
        cursor = self.db.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return bool(row)

    def _save_badge(self):
        badge_number = self.badge_number_var.get().strip()
        if not badge_number:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('badge_number_required', 'Inserire il numero badge.'),
                parent=self,
            )
            return

        try:
            if self._badge_exists(badge_number, self._selected_badge_id):
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('badge_number_exists', 'Questo numero badge esiste già.'),
                    parent=self,
                )
                return

            cursor = self.db.conn.cursor()
            if self._selected_badge_id:
                cursor.execute(
                    """
                    UPDATE Employee.dbo.Badges
                    SET NoBadge = ?
                    WHERE BadgeId = ?
                    """,
                    (badge_number, self._selected_badge_id),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO Employee.dbo.Badges (NoBadge, DateIn, EmployeerId, ForGuest)
                    VALUES (?, GETDATE(), 2, 1)
                    """,
                    (badge_number,),
                )
            self.db.conn.commit()
            cursor.close()
            self._load_badges()
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('badge_saved_ok', 'Badge salvato con successo.'),
                parent=self,
            )
        except Exception as e:
            logger.error(f"Errore salvataggio badge visitatore: {e}", exc_info=True)
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}", parent=self)

    def _delete_badge(self):
        if not self._selected_badge_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_badge', 'Selezionare un badge dalla lista.'),
                parent=self,
            )
            return

        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                """
                SELECT TOP 1 vb.VisitorDataID
                FROM Employee.dbo.VisitorBadgeLogs vb
                WHERE vb.BadgeId = ?
                  AND CAST(vb.DateOut AS DATE) >= CAST(GETDATE() AS DATE)
                """,
                (self._selected_badge_id,),
            )
            active_assignment = cursor.fetchone()
            if active_assignment:
                cursor.close()
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get(
                        'badge_delete_blocked',
                        'Il badge è assegnato a un visitatore e non può essere eliminato.',
                    ),
                    parent=self,
                )
                return

            if not messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('confirm_delete_badge', 'Eliminare il badge selezionato?'),
                parent=self,
            ):
                cursor.close()
                return

            cursor.execute(
                "DELETE FROM Employee.dbo.Badges WHERE BadgeId = ?",
                (self._selected_badge_id,),
            )
            self.db.conn.commit()
            cursor.close()
            self._load_badges()
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('badge_deleted_ok', 'Badge eliminato con successo.'),
                parent=self,
            )
        except Exception as e:
            logger.error(f"Errore eliminazione badge visitatore: {e}", exc_info=True)
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}", parent=self)
