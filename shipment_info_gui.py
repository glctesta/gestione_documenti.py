# -*- coding: utf-8 -*-
"""
shipment_info_gui.py
Form "Info Spedizioni": accoppia 1-1 ogni sito (dbo.Sites) alla sua directory
sotto \\192.168.10.110\Shipping e gestisce i destinatari TO / CC delle email
automatiche di spedizione (tabella dbo.ShipmentEmailConfig).
Modifica = soft-delete del record attivo + inserimento nuovo (storia conservata).
"""
from __future__ import annotations
import logging
import re
import tkinter as tk
from tkinter import ttk, messagebox

from shipment_info_service import ensure_config_table

logger = logging.getLogger("TraceabilityRS")

_Q_SITES = """
SELECT IDSite, SiteName
FROM Traceability_RS.dbo.Sites
ORDER BY SiteName
"""

_Q_LIST = """
SELECT c.ConfigId, c.IDSite, s.SiteName, c.DirectoryName,
       c.ToEmails, c.CcEmails, c.IsActive, c.DateIn, c.[User]
FROM Traceability_RS.dbo.ShipmentEmailConfig c
INNER JOIN Traceability_RS.dbo.Sites s ON s.IDSite = c.IDSite
WHERE c.DateOut IS NULL
ORDER BY s.SiteName
"""

_Q_INSERT = """
INSERT INTO Traceability_RS.dbo.ShipmentEmailConfig
    (IDSite, DirectoryName, ToEmails, CcEmails, IsActive, [User])
VALUES (?, ?, ?, ?, ?, ?)
"""

_Q_SOFT_DELETE = """
UPDATE Traceability_RS.dbo.ShipmentEmailConfig
SET DateOut = GETDATE()
WHERE IDSite = ? AND DateOut IS NULL
"""

_EMAIL_RE = re.compile(r'^[^@\s;]+@[^@\s;]+\.[^@\s;]+$')


def open_shipment_info_form(master, db, lang, user_name: str):
    return ShipmentInfoForm(master, db, lang, user_name)


class ShipmentInfoForm(tk.Toplevel):
    """Gestione sito → directory spedizioni + destinatari email."""

    def __init__(self, parent, db, lang, logged_user: str):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.logged_user = logged_user or 'system'

        self._sites: dict[str, int] = {}          # "SiteName (ID)" → IDSite
        self._selected_config_id = None

        L = lambda k, d: self.lang.get(k, d)  # noqa: E731
        self._L = L

        self.title(L('ship_info_title', 'Info Spedizioni'))
        self.geometry('860x560')
        self.minsize(760, 480)
        self.configure(bg='#f4f6f8')
        self.grab_set()

        ensure_config_table(self.db)
        self._build_ui()
        self._load_sites()
        self._reload()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        L = self._L
        pad = {'padx': 8, 'pady': 4}

        top = tk.Frame(self, bg='#f4f6f8')
        top.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ── Griglia configurazione ────────────────────────────────────────────
        frm = tk.LabelFrame(top, text=L('ship_info_config', 'Configurazione sito'),
                            bg='#ffffff', padx=10, pady=10)
        frm.pack(fill=tk.X)

        tk.Label(frm, text=L('ship_info_site', 'Sito:'), bg='#ffffff',
                 font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, **pad)
        self._site_var = tk.StringVar()
        self._site_combo = ttk.Combobox(frm, textvariable=self._site_var, state='readonly',
                                        width=45, font=('Segoe UI', 10))
        self._site_combo.grid(row=0, column=1, sticky=tk.W, **pad)

        tk.Label(frm, text=L('ship_info_dir', 'Directory:'), bg='#ffffff',
                 font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, **pad)
        dir_row = tk.Frame(frm, bg='#ffffff')
        dir_row.grid(row=1, column=1, sticky=tk.W, **pad)
        tk.Label(dir_row, text=r'\\192.168.10.110\InternalApplications\Shipping\ ', bg='#ffffff',
                 fg='#7f8c8d', font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self._dir_var = tk.StringVar()
        tk.Entry(dir_row, textvariable=self._dir_var, width=30,
                 font=('Segoe UI', 10)).pack(side=tk.LEFT)

        tk.Label(frm, text=L('ship_info_to', 'Email TO:'), bg='#ffffff',
                 font=('Segoe UI', 10)).grid(row=2, column=0, sticky=tk.W, **pad)
        self._to_var = tk.StringVar()
        tk.Entry(frm, textvariable=self._to_var, width=60,
                 font=('Segoe UI', 10)).grid(row=2, column=1, sticky=tk.W, **pad)
        tk.Label(frm, text=L('ship_info_sep_hint', '(separate da ; o ,)'),
                 bg='#ffffff', fg='#7f8c8d', font=('Segoe UI', 8)).grid(
            row=2, column=2, sticky=tk.W, **pad)

        tk.Label(frm, text=L('ship_info_cc', 'Email CC:'), bg='#ffffff',
                 font=('Segoe UI', 10)).grid(row=3, column=0, sticky=tk.W, **pad)
        self._cc_var = tk.StringVar()
        tk.Entry(frm, textvariable=self._cc_var, width=60,
                 font=('Segoe UI', 10)).grid(row=3, column=1, sticky=tk.W, **pad)

        self._active_var = tk.IntVar(value=1)
        tk.Checkbutton(frm, text=L('ship_info_active', 'Servizio attivo'),
                       variable=self._active_var, bg='#ffffff',
                       font=('Segoe UI', 10)).grid(row=4, column=1, sticky=tk.W, **pad)

        # ── Tabella configurazioni ────────────────────────────────────────────
        tbl_frm = tk.LabelFrame(top, text=L('ship_info_list', 'Configurazioni attive'),
                                bg='#ffffff', padx=10, pady=10)
        tbl_frm.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        cols = ('site', 'dir', 'to', 'cc', 'active')
        self._tree = ttk.Treeview(tbl_frm, columns=cols, show='headings', height=10)
        self._tree.heading('site', text=L('ship_info_site', 'Sito'))
        self._tree.heading('dir', text=L('ship_info_dir', 'Directory'))
        self._tree.heading('to', text='TO')
        self._tree.heading('cc', text='CC')
        self._tree.heading('active', text=L('ship_info_active_col', 'Attivo'))
        self._tree.column('site', width=200)
        self._tree.column('dir', width=140)
        self._tree.column('to', width=220)
        self._tree.column('cc', width=180)
        self._tree.column('active', width=60, anchor=tk.CENTER)
        vsb = ttk.Scrollbar(tbl_frm, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tree.bind('<<TreeviewSelect>>', self._on_select)

        # ── Bottoni ───────────────────────────────────────────────────────────
        btn = tk.Frame(self, bg='#f4f6f8')
        btn.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(btn, text=self._L('new', 'Nuovo'), width=10,
                  command=self._clear_form).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text=self._L('save', 'Salva'), width=10,
                  bg='#2e86de', fg='#ffffff', relief=tk.FLAT,
                  command=self._on_save).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text=self._L('delete', 'Elimina'), width=10,
                  command=self._on_delete).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text=self._L('close', 'Chiudi'), width=10,
                  command=self.destroy).pack(side=tk.RIGHT, padx=4)

    # ── Caricamento ───────────────────────────────────────────────────────────

    def _load_sites(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_SITES)
            values = []
            for r in cur.fetchall():
                display = f"{r.SiteName} ({r.IDSite})"
                self._sites[display] = r.IDSite
                values.append(display)
            cur.close()
            self._site_combo['values'] = values
        except Exception as e:
            logger.error(f"ShipmentInfoForm _load_sites: {e}", exc_info=True)

    def _reload(self):
        self._tree.delete(*self._tree.get_children())
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_LIST)
            self._rows = {}
            for r in cur.fetchall():
                self._tree.insert('', tk.END, iid=str(r.ConfigId), values=(
                    r.SiteName,
                    r.DirectoryName,
                    (r.ToEmails or '')[:60],
                    (r.CcEmails or '')[:50],
                    '✔' if r.IsActive else '—',
                ))
                self._rows[r.ConfigId] = r
            cur.close()
        except Exception as e:
            logger.error(f"ShipmentInfoForm _reload: {e}", exc_info=True)
            messagebox.showerror(self._L('error', 'Errore'), str(e), parent=self)

    # ── Eventi ────────────────────────────────────────────────────────────────

    def _on_select(self, event=None):
        sel = self._tree.selection()
        if not sel:
            return
        row = self._rows.get(int(sel[0]))
        if not row:
            return
        self._selected_config_id = row.ConfigId
        self._site_var.set(f"{row.SiteName} ({row.IDSite})")
        self._dir_var.set(row.DirectoryName or '')
        self._to_var.set(row.ToEmails or '')
        self._cc_var.set(row.CcEmails or '')
        self._active_var.set(1 if row.IsActive else 0)

    def _clear_form(self):
        self._selected_config_id = None
        self._site_var.set('')
        self._dir_var.set('')
        self._to_var.set('')
        self._cc_var.set('')
        self._active_var.set(1)
        self._tree.selection_remove(self._tree.selection())

    # ── Validazione ───────────────────────────────────────────────────────────

    @staticmethod
    def _parse_emails(raw: str):
        return [a.strip() for a in raw.replace(',', ';').split(';') if a.strip()]

    def _validate(self):
        L = self._L
        site_display = self._site_var.get().strip()
        id_site = self._sites.get(site_display)
        if id_site is None:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('ship_info_no_site', 'Selezionare un sito.'), parent=self)
            return None

        directory = self._dir_var.get().strip()
        if not directory:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('ship_info_no_dir', 'Inserire la directory.'), parent=self)
            return None

        to_list = self._parse_emails(self._to_var.get())
        if not to_list:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('ship_info_no_to', 'Inserire almeno un indirizzo TO.'), parent=self)
            return None
        cc_list = self._parse_emails(self._cc_var.get())
        bad = [a for a in to_list + cc_list if not _EMAIL_RE.match(a)]
        if bad:
            messagebox.showwarning(
                L('warning', 'Attenzione'),
                L('ship_info_bad_email', 'Indirizzi non validi:') + '\n' + '\n'.join(bad),
                parent=self)
            return None

        return id_site, directory, ';'.join(to_list), ';'.join(cc_list)

    # ── Salvataggio / eliminazione ────────────────────────────────────────────

    def _on_save(self):
        L = self._L
        data = self._validate()
        if not data:
            return
        id_site, directory, to_emails, cc_emails = data
        is_active = 1 if self._active_var.get() else 0

        try:
            cur = self.db.conn.cursor()
            # Modifica: chiude il record attivo del sito e ne inserisce uno nuovo
            cur.execute(_Q_SOFT_DELETE, (id_site,))
            cur.execute(_Q_INSERT, (id_site, directory, to_emails, cc_emails,
                                    is_active, self.logged_user))
            self.db.conn.commit()
            cur.close()
            logger.info(
                "ShipmentEmailConfig salvata: IDSite=%s dir=%s TO=%s CC=%s active=%s user=%s",
                id_site, directory, to_emails, cc_emails, is_active, self.logged_user)
        except Exception as e:
            logger.error(f"ShipmentInfoForm _on_save: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return

        messagebox.showinfo(L('success', 'Successo'),
                            L('ship_info_saved', 'Configurazione salvata.'), parent=self)
        self._clear_form()
        self._reload()

    def _on_delete(self):
        L = self._L
        site_display = self._site_var.get().strip()
        id_site = self._sites.get(site_display)
        if id_site is None:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('ship_info_no_site', 'Selezionare un sito.'), parent=self)
            return
        if not messagebox.askyesno(
                L('ship_info_del_title', 'Elimina configurazione'),
                L('ship_info_del_msg', "Eliminare la configurazione del sito selezionato?"),
                parent=self):
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(_Q_SOFT_DELETE, (id_site,))
            self.db.conn.commit()
            cur.close()
            logger.info("ShipmentEmailConfig eliminata (soft): IDSite=%s user=%s",
                        id_site, self.logged_user)
        except Exception as e:
            logger.error(f"ShipmentInfoForm _on_delete: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self._clear_form()
        self._reload()
