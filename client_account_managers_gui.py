# -*- coding: utf-8 -*-
"""
client_account_managers_gui.py

Gestione Account Manager dei clienti finali e preferenze di comunicazione per le
conferme di spedizione.

Per ogni cliente finale (dbo.FinalClients) si gestiscono:
  - gli Account Manager associati (dbo.ClientAccountManagers <-> dbo.ClientAccountLists)
    che riceveranno le email in TO;
  - i destinatari in CC, salvati in dbo.Settings con atribute = 'Sys_email_<FinalClientName>';
  - due interruttori (invio agli Account Manager / invio ai CC), salvati per cliente
    finale in dbo.ClientShipmentEmailPrefs.

Solo la form di gestione: l'aggancio all'email di conferma spedizioni e' separato.
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger(__name__)

# riuso parsing indirizzi dalla gestione settings
try:
    from settings_gui import _parse_addresses, _join_addresses
except Exception:  # fallback difensivo
    def _parse_addresses(value):
        if not value:
            return []
        return [t.strip() for t in str(value).replace(',', ';').split(';') if t.strip()]

    def _join_addresses(addrs):
        seen, out = set(), []
        for a in addrs:
            a = (a or '').strip()
            if a and a.lower() not in seen:
                seen.add(a.lower())
                out.append(a)
        return '; '.join(out)


def open_client_account_managers(parent, db, lang, user_name):
    """Punto di ingresso pubblico."""
    ClientAccountManagersWindow(parent, db, lang, user_name)


class ClientAccountManagersWindow(tk.Toplevel):
    """Gestione account manager + preferenze email per cliente finale."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        self._current_idfc = None
        self._current_name = None

        self.title(self.lang.get('cam_title', 'Gestione Account Manager Clienti'))
        self.geometry('1080x640')
        self.transient(parent)
        self.grab_set()

        self.send_am_var = tk.BooleanVar(value=True)
        self.send_cc_var = tk.BooleanVar(value=True)

        self._build_ui()
        self._load_final_clients()

    # ------------------------------------------------------------------ #
    def _cursor(self):
        return self.db.conn.cursor()

    def _build_ui(self):
        main = ttk.Frame(self, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        # ── Sinistra: clienti finali ──
        left = ttk.LabelFrame(main, text=self.lang.get('cam_final_clients', 'Clienti finali'), padding=6)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        self.fc_tree = ttk.Treeview(left, columns=('id', 'name', 'acr'), show='headings',
                                    selectmode='browse', height=24)
        self.fc_tree.heading('id', text='ID')
        self.fc_tree.heading('name', text=self.lang.get('cam_col_client', 'Cliente finale'))
        self.fc_tree.heading('acr', text=self.lang.get('cam_col_acronym', 'Acronimo'))
        self.fc_tree.column('id', width=0, stretch=False)
        self.fc_tree.column('name', width=180, anchor='w')
        self.fc_tree.column('acr', width=80, anchor='center')
        self.fc_tree.pack(fill=tk.Y, expand=True)
        self.fc_tree.bind('<<TreeviewSelect>>', self._on_client_select)

        # ── Destra ──
        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sel_label = ttk.Label(right, text=self.lang.get('cam_select_client', 'Seleziona un cliente finale'),
                                   font=('Segoe UI', 11, 'bold'))
        self.sel_label.pack(anchor='w', pady=(0, 6))

        # Account managers
        am_frame = ttk.LabelFrame(right, text=self.lang.get('cam_managers', 'Account Manager (destinatari TO)'),
                                  padding=6)
        am_frame.pack(fill=tk.BOTH, expand=True)
        cols = ('listid', 'mgrid', 'name', 'surname', 'email', 'phone')
        self.am_tree = ttk.Treeview(am_frame, columns=cols, show='headings', selectmode='browse', height=8)
        for hidden in ('listid', 'mgrid'):
            self.am_tree.column(hidden, width=0, stretch=False)
            self.am_tree.heading(hidden, text='')
        self.am_tree.heading('name', text=self.lang.get('cam_col_name', 'Nome'))
        self.am_tree.heading('surname', text=self.lang.get('cam_col_surname', 'Cognome'))
        self.am_tree.heading('email', text=self.lang.get('cam_col_email', 'Email'))
        self.am_tree.heading('phone', text=self.lang.get('cam_col_phone', 'Telefono'))
        self.am_tree.column('name', width=140, anchor='w')
        self.am_tree.column('surname', width=140, anchor='w')
        self.am_tree.column('email', width=240, anchor='w')
        self.am_tree.column('phone', width=120, anchor='w')
        avsb = ttk.Scrollbar(am_frame, orient=tk.VERTICAL, command=self.am_tree.yview)
        self.am_tree.configure(yscroll=avsb.set)
        self.am_tree.grid(row=0, column=0, sticky='nsew')
        avsb.grid(row=0, column=1, sticky='ns')
        am_frame.grid_rowconfigure(0, weight=1)
        am_frame.grid_columnconfigure(0, weight=1)

        am_btns = ttk.Frame(am_frame)
        am_btns.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(6, 0))
        ttk.Button(am_btns, text=self.lang.get('cam_new', 'Nuovo + associa'),
                   command=self._new_manager).pack(side=tk.LEFT, padx=3)
        ttk.Button(am_btns, text=self.lang.get('cam_associate', 'Associa esistente'),
                   command=self._associate_existing).pack(side=tk.LEFT, padx=3)
        ttk.Button(am_btns, text=self.lang.get('cam_edit', 'Modifica'),
                   command=self._edit_manager).pack(side=tk.LEFT, padx=3)
        ttk.Button(am_btns, text=self.lang.get('cam_remove', 'Rimuovi associazione'),
                   command=self._remove_association).pack(side=tk.LEFT, padx=3)

        # CC settings
        cc_frame = ttk.LabelFrame(right, text=self.lang.get('cam_cc', 'Destinatari in CC (Sys_email_<cliente>)'),
                                  padding=6)
        cc_frame.pack(fill=tk.X, pady=(8, 0))
        self.cc_key_label = ttk.Label(cc_frame, text='', foreground='gray', font=('Segoe UI', 8))
        self.cc_key_label.pack(anchor='w')
        self.cc_text = tk.Text(cc_frame, height=3, wrap='word')
        self.cc_text.pack(fill=tk.X, pady=(2, 4))
        ttk.Button(cc_frame, text=self.lang.get('cam_save_cc', 'Salva CC'),
                   command=self._save_cc).pack(anchor='e')

        # Toggle invio
        tg_frame = ttk.LabelFrame(right, text=self.lang.get('cam_send_prefs', 'Invio automatico email'), padding=6)
        tg_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Checkbutton(tg_frame, text=self.lang.get('cam_send_am', 'Invia agli Account Manager (TO)'),
                        variable=self.send_am_var, command=self._save_prefs).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Checkbutton(tg_frame, text=self.lang.get('cam_send_cc', 'Invia ai destinatari CC'),
                        variable=self.send_cc_var, command=self._save_prefs).pack(side=tk.LEFT)

        # Status + chiudi
        bottom = ttk.Frame(self, padding=(8, 4))
        bottom.pack(fill=tk.X)
        self.status_var = tk.StringVar(value='')
        ttk.Label(bottom, textvariable=self.status_var, foreground='gray').pack(side=tk.LEFT)
        ttk.Button(bottom, text=self.lang.get('close_button', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT)

        self._set_right_enabled(False)

    def _set_right_enabled(self, enabled):
        state = 'normal' if enabled else 'disabled'
        try:
            self.cc_text.config(state=state)
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    def _load_final_clients(self):
        for it in self.fc_tree.get_children():
            self.fc_tree.delete(it)
        try:
            cur = self._cursor()
            cur.execute("SELECT IDFinalClient, FinalClientName, ISNULL(AcronimForCode,'') "
                        "FROM [Traceability_RS].[dbo].[FinalClients] ORDER BY FinalClientName")
            for r in cur.fetchall():
                self.fc_tree.insert('', tk.END, iid=str(r[0]), values=(r[0], r[1] or '', r[2] or ''))
            cur.close()
        except Exception as e:
            logger.error(f"CAM _load_final_clients: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    def _on_client_select(self, _event=None):
        sel = self.fc_tree.selection()
        if not sel:
            return
        self._current_idfc = int(sel[0])
        self._current_name = self.fc_tree.set(sel[0], 'name')
        self.sel_label.config(text=f"{self._current_name}  (ID {self._current_idfc})")
        self.cc_key_label.config(text=f"settings.atribute = Sys_email_{self._current_name}")
        self._set_right_enabled(True)
        self._load_managers()
        self._load_cc()
        self._load_prefs()

    # ---- Account managers ----
    def _load_managers(self):
        for it in self.am_tree.get_children():
            self.am_tree.delete(it)
        if self._current_idfc is None:
            return
        try:
            cur = self._cursor()
            cur.execute(
                "SELECT cal.ClientAccountListId, cam.ClientAccountManagerId, cam.Name, cam.Surname, "
                "       cam.WorkEmail, cam.Telephon "
                "FROM [Traceability_RS].[dbo].[ClientAccountLists] cal "
                "JOIN [Traceability_RS].[dbo].[ClientAccountManagers] cam "
                "  ON cam.ClientAccountManagerId = cal.ClientAccountManagerId "
                "WHERE cal.IDFinalClient = ? AND cal.Dateout IS NULL AND cam.Dateout IS NULL "
                "ORDER BY cam.Surname, cam.Name", (self._current_idfc,))
            for r in cur.fetchall():
                self.am_tree.insert('', tk.END, iid=str(r[0]),
                                    values=(r[0], r[1], r[2] or '', r[3] or '', r[4] or '', r[5] or ''))
            cur.close()
        except Exception as e:
            logger.error(f"CAM _load_managers: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    def _new_manager(self):
        if self._current_idfc is None:
            return
        dlg = _ManagerDialog(self, self.lang)
        self.wait_window(dlg)
        if dlg.result is None:
            return
        name, surname, email, phone = dlg.result
        try:
            cur = self._cursor()
            cur.execute(
                "INSERT INTO [Traceability_RS].[dbo].[ClientAccountManagers] (Name, Surname, WorkEmail, Telephon) "
                "OUTPUT INSERTED.ClientAccountManagerId VALUES (?, ?, ?, ?)",
                (name, surname, email, phone))
            mgr_id = int(cur.fetchone()[0])
            cur.execute(
                "INSERT INTO [Traceability_RS].[dbo].[ClientAccountLists] (ClientAccountManagerId, IDFinalClient) "
                "VALUES (?, ?)", (mgr_id, self._current_idfc))
            self.db.conn.commit()
            cur.close()
            self._load_managers()
            self.status_var.set(self.lang.get('cam_saved', 'Salvato.'))
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _new_manager: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    def _associate_existing(self):
        if self._current_idfc is None:
            return
        try:
            cur = self._cursor()
            # manager attivi non gia' associati a questo cliente finale
            cur.execute(
                "SELECT cam.ClientAccountManagerId, cam.Name, cam.Surname, cam.WorkEmail "
                "FROM [Traceability_RS].[dbo].[ClientAccountManagers] cam "
                "WHERE cam.Dateout IS NULL AND cam.ClientAccountManagerId NOT IN ("
                "  SELECT ClientAccountManagerId FROM [Traceability_RS].[dbo].[ClientAccountLists] "
                "  WHERE IDFinalClient = ? AND Dateout IS NULL) "
                "ORDER BY cam.Surname, cam.Name", (self._current_idfc,))
            rows = [(r[0], f"{r[2]} {r[1]}".strip(), r[3] or '') for r in cur.fetchall()]
            cur.close()
        except Exception as e:
            logger.error(f"CAM _associate list: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        if not rows:
            messagebox.showinfo(self.lang.get('info_title', 'Info'),
                                self.lang.get('cam_no_unassociated', 'Nessun account manager disponibile da associare.'),
                                parent=self)
            return
        dlg = _PickManagerDialog(self, self.lang, rows)
        self.wait_window(dlg)
        if dlg.result is None:
            return
        try:
            cur = self._cursor()
            cur.execute(
                "INSERT INTO [Traceability_RS].[dbo].[ClientAccountLists] (ClientAccountManagerId, IDFinalClient) "
                "VALUES (?, ?)", (dlg.result, self._current_idfc))
            self.db.conn.commit()
            cur.close()
            self._load_managers()
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _associate insert: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    def _edit_manager(self):
        sel = self.am_tree.selection()
        if not sel:
            messagebox.showinfo(self.lang.get('info_title', 'Info'),
                                self.lang.get('cam_select_mgr', 'Seleziona un account manager.'), parent=self)
            return
        mgr_id = int(self.am_tree.set(sel[0], 'mgrid'))
        cur_vals = (self.am_tree.set(sel[0], 'name'), self.am_tree.set(sel[0], 'surname'),
                    self.am_tree.set(sel[0], 'email'), self.am_tree.set(sel[0], 'phone'))
        dlg = _ManagerDialog(self, self.lang, initial=cur_vals)
        self.wait_window(dlg)
        if dlg.result is None:
            return
        name, surname, email, phone = dlg.result
        try:
            cur = self._cursor()
            cur.execute(
                "UPDATE [Traceability_RS].[dbo].[ClientAccountManagers] "
                "SET Name=?, Surname=?, WorkEmail=?, Telephon=? WHERE ClientAccountManagerId=?",
                (name, surname, email, phone, mgr_id))
            self.db.conn.commit()
            cur.close()
            self._load_managers()
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _edit_manager: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    def _remove_association(self):
        sel = self.am_tree.selection()
        if not sel:
            messagebox.showinfo(self.lang.get('info_title', 'Info'),
                                self.lang.get('cam_select_mgr', 'Seleziona un account manager.'), parent=self)
            return
        list_id = int(self.am_tree.set(sel[0], 'listid'))
        who = f"{self.am_tree.set(sel[0], 'surname')} {self.am_tree.set(sel[0], 'name')}".strip()
        if not messagebox.askyesno(
            self.lang.get('confirm_title', 'Conferma'),
            self.lang.get('cam_confirm_remove', 'Rimuovere "{0}" da questo cliente?').format(who),
            parent=self):
            return
        try:
            cur = self._cursor()
            cur.execute("DELETE FROM [Traceability_RS].[dbo].[ClientAccountLists] WHERE ClientAccountListId=?",
                        (list_id,))
            self.db.conn.commit()
            cur.close()
            self._load_managers()
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _remove_association: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    # ---- CC (settings) ----
    def _cc_key(self):
        return f"Sys_email_{self._current_name}"

    def _load_cc(self):
        self.cc_text.config(state='normal')
        self.cc_text.delete('1.0', tk.END)
        try:
            cur = self._cursor()
            cur.execute("SELECT Value FROM [Traceability_RS].[dbo].[Settings] WHERE Atribute=?", (self._cc_key(),))
            row = cur.fetchone()
            cur.close()
            if row and row[0]:
                self.cc_text.insert('1.0', '; '.join(_parse_addresses(row[0])))
        except Exception as e:
            logger.error(f"CAM _load_cc: {e}", exc_info=True)

    def _save_cc(self):
        if self._current_idfc is None:
            return
        raw = self.cc_text.get('1.0', tk.END)
        value = _join_addresses(_parse_addresses(raw.replace('\n', ';')))
        try:
            cur = self._cursor()
            cur.execute("SELECT COUNT(*) FROM [Traceability_RS].[dbo].[Settings] WHERE Atribute=?", (self._cc_key(),))
            exists = cur.fetchone()[0] > 0
            if exists:
                cur.execute("UPDATE [Traceability_RS].[dbo].[Settings] SET Value=?, LastCheck=GETDATE() "
                            "WHERE Atribute=?", (value, self._cc_key()))
            else:
                cur.execute("INSERT INTO [Traceability_RS].[dbo].[Settings] (Atribute, Value, Name, LastCheck) "
                            "VALUES (?, ?, ?, GETDATE())",
                            (self._cc_key(), value, f"CC spedizioni {self._current_name}"))
            self.db.conn.commit()
            cur.close()
            self.cc_text.delete('1.0', tk.END)
            self.cc_text.insert('1.0', value)
            self.status_var.set(self.lang.get('cam_cc_saved', 'CC salvati per {0}.').format(self._current_name))
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _save_cc: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)

    # ---- Preferenze invio ----
    def _load_prefs(self):
        try:
            cur = self._cursor()
            cur.execute("SELECT SendToAccountManager, SendToCc FROM [Traceability_RS].[dbo].[ClientShipmentEmailPrefs] "
                        "WHERE IDFinalClient=?", (self._current_idfc,))
            row = cur.fetchone()
            cur.close()
            if row is None:
                self.send_am_var.set(True)
                self.send_cc_var.set(True)
            else:
                self.send_am_var.set(bool(row[0]))
                self.send_cc_var.set(bool(row[1]))
        except Exception as e:
            logger.error(f"CAM _load_prefs: {e}", exc_info=True)

    def _save_prefs(self):
        if self._current_idfc is None:
            return
        am = 1 if self.send_am_var.get() else 0
        cc = 1 if self.send_cc_var.get() else 0
        try:
            cur = self._cursor()
            cur.execute("SELECT COUNT(*) FROM [Traceability_RS].[dbo].[ClientShipmentEmailPrefs] WHERE IDFinalClient=?",
                        (self._current_idfc,))
            if cur.fetchone()[0] > 0:
                cur.execute("UPDATE [Traceability_RS].[dbo].[ClientShipmentEmailPrefs] "
                            "SET SendToAccountManager=?, SendToCc=?, LastUpdate=GETDATE(), UpdatedBy=? "
                            "WHERE IDFinalClient=?", (am, cc, self.user_name, self._current_idfc))
            else:
                cur.execute("INSERT INTO [Traceability_RS].[dbo].[ClientShipmentEmailPrefs] "
                            "(IDFinalClient, SendToAccountManager, SendToCc, LastUpdate, UpdatedBy) "
                            "VALUES (?, ?, ?, GETDATE(), ?)", (self._current_idfc, am, cc, self.user_name))
            self.db.conn.commit()
            cur.close()
            self.status_var.set(self.lang.get('cam_prefs_saved', 'Preferenze invio salvate.'))
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"CAM _save_prefs: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)


class _ManagerDialog(tk.Toplevel):
    """Dialog nuovo/modifica account manager."""

    def __init__(self, parent, lang, initial=None):
        super().__init__(parent)
        self.lang = lang
        self.result = None
        self.title(lang.get('cam_mgr_dialog', 'Account Manager'))
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill=tk.BOTH, expand=True)
        frm.columnconfigure(1, weight=1)

        self.name_var = tk.StringVar(value=initial[0] if initial else '')
        self.surname_var = tk.StringVar(value=initial[1] if initial else '')
        self.email_var = tk.StringVar(value=initial[2] if initial else '')
        self.phone_var = tk.StringVar(value=initial[3] if initial else '')

        rows = [
            (lang.get('cam_col_name', 'Nome') + ' *', self.name_var),
            (lang.get('cam_col_surname', 'Cognome') + ' *', self.surname_var),
            (lang.get('cam_col_email', 'Email') + ' *', self.email_var),
            (lang.get('cam_col_phone', 'Telefono'), self.phone_var),
        ]
        for i, (lbl, var) in enumerate(rows):
            ttk.Label(frm, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 8))
            ent = ttk.Entry(frm, textvariable=var, width=36)
            ent.grid(row=i, column=1, sticky=tk.EW, pady=5)
            if i == 0:
                ent.focus_set()

        btns = ttk.Frame(frm)
        btns.grid(row=len(rows), column=0, columnspan=2, pady=(12, 0), sticky=tk.E)
        ttk.Button(btns, text=lang.get('save_button', 'Salva'), command=self._ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text=lang.get('cancel_button', 'Annulla'), command=self.destroy).pack(side=tk.LEFT)

    def _ok(self):
        name = self.name_var.get().strip()
        surname = self.surname_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        if not name or not surname or not email or '@' not in email:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('cam_mgr_invalid', 'Inserire nome, cognome ed email valida.'),
                                   parent=self)
            return
        self.result = (name, surname, email, phone or None)
        self.destroy()


class _PickManagerDialog(tk.Toplevel):
    """Dialog per scegliere un account manager esistente da associare."""

    def __init__(self, parent, lang, rows):
        super().__init__(parent)
        self.lang = lang
        self.result = None
        self.title(lang.get('cam_pick', 'Associa Account Manager'))
        self.geometry('480x360')
        self.transient(parent)
        self.grab_set()

        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(frm, columns=('id', 'who', 'email'), show='headings', selectmode='browse')
        self.tree.heading('id', text='')
        self.tree.heading('who', text=lang.get('cam_col_manager', 'Account Manager'))
        self.tree.heading('email', text=lang.get('cam_col_email', 'Email'))
        self.tree.column('id', width=0, stretch=False)
        self.tree.column('who', width=200, anchor='w')
        self.tree.column('email', width=240, anchor='w')
        self.tree.pack(fill=tk.BOTH, expand=True)
        for mid, who, email in rows:
            self.tree.insert('', tk.END, iid=str(mid), values=(mid, who, email))
        self.tree.bind('<Double-1>', lambda e: self._ok())

        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btns, text=lang.get('cam_associate', 'Associa'), command=self._ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text=lang.get('cancel_button', 'Annulla'), command=self.destroy).pack(side=tk.RIGHT)

    def _ok(self):
        sel = self.tree.selection()
        if not sel:
            return
        self.result = int(sel[0])
        self.destroy()
