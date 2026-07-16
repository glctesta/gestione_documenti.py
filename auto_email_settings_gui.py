# -*- coding: utf-8 -*-
"""
auto_email_settings_gui.py

Gestione iscrizioni alle email automatiche (tabella traceability_rs.dbo.settings).

Due livelli:
  - VISTA UTENTE (tier1, chiave menu 'modifica_invoi_email_auto'): l'utente loggato
    vede TUTTI i servizi (Employeerid=2) con lo stato della propria iscrizione e puo'
    iscriversi (aggiunta della propria WorkEmail alla colonna Value) o disiscriversi
    (rimozione). Un filtro testuale + stato permette di cercare i servizi.
    I servizi OBBLIGATORI (IsBlocked=1) sono protetti: per rimuoversi serve il secondo
    login super user (chiave 'permetti_modifica_auormail_obbligatorie'); l'iscrizione
    invece e' sempre libera.
  - VISTA ADMIN (tier2, super user): CRUD completo sui servizi Employeerid=2 —
    modifica destinatari/nome, imposta/togli il flag obbligatorio, aggiungi servizi.

L'email dell'utente e' risolta dal nome autenticato via Employee.dbo (EmployeerId=2),
come in disciplinary_gui.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)

EMPLOYERID = 2
KEY_SUPER = 'permetti_modifica_auormail_obbligatorie'


def _split_recipients(value):
    """Spezza la lista destinatari (separatori ';' o ',') in indirizzi puliti."""
    if not value:
        return []
    out = []
    for chunk in value.replace(',', ';').split(';'):
        c = chunk.strip()
        if c:
            out.append(c)
    return out


def open_auto_email_settings(master, db, lang, user_name):
    """Entry point: apre la vista utente delle iscrizioni email automatiche."""
    AutoEmailSubscriptionWindow(master, db, lang, user_name)


# ─────────────────────────────────────────────────────────────────────────────
#  Accesso DB
# ─────────────────────────────────────────────────────────────────────────────
def _fetch(db, sql, params=None):
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    return [dict(zip(cols, r)) for r in rows]


def _exec(db, sql, params):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute(sql, params)
        db.conn.commit()


def _resolve_user_email(db, user_name):
    try:
        rows = _fetch(db, """
            SELECT TOP 1 ea.WorkEmail
            FROM Employee.dbo.EmployeeHireHistory h
            INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
            LEFT JOIN Employee.dbo.EmployeeAddress ea
                ON ea.EmployeeId = e.EmployeeId AND ea.DateOut IS NULL
            WHERE h.EndWorkDate IS NULL AND h.EmployeerId = ?
              AND (e.EmployeeName + ' ' + e.EmployeeSurname = ?
                   OR e.EmployeeSurname + ' ' + e.EmployeeName = ?)
        """, (EMPLOYERID, user_name, user_name))
        if rows and rows[0].get('WorkEmail'):
            return rows[0]['WorkEmail'].strip()
    except Exception as e:
        logger.warning(f"Risoluzione email utente '{user_name}': {e}")
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  Vista utente (tier1)
# ─────────────────────────────────────────────────────────────────────────────
class AutoEmailSubscriptionWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        self._super_ok = False
        L = self.lang.get

        self.title(L('aes_title', 'Iscrizioni Email Automatiche'))
        self.geometry('900x520')
        self.minsize(760, 420)
        self.transient(master)

        self.user_email = _resolve_user_email(db, self.user_name)
        self._all_rows = []
        self._rows_by_id = {}
        self._build_ui()
        self.grab_set()
        self._load()

    def _build_ui(self):
        L = self.lang.get
        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('aes_title', 'Iscrizioni Email Automatiche'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)

        info = L('aes_user_info', 'Utente: {0}   —   Email: {1}').format(
            self.user_name, self.user_email or L('aes_no_email', '(non trovata)'))
        tk.Label(self, text=info, anchor='w', fg='#1F3864',
                 font=('Helvetica', 9, 'bold')).pack(fill=tk.X, padx=12, pady=(6, 0))
        tk.Label(self, anchor='w', fg='#555', font=('Helvetica', 8, 'italic'),
                 text=L('aes_hint', 'Iscriviti ai servizi che ti interessano o disiscriviti '
                        'da quelli che non vuoi più ricevere. Per disiscriversi da un servizio '
                        'obbligatorio serve un super user.')).pack(
            fill=tk.X, padx=12, pady=(0, 4))

        # ── Barra filtri ────────────────────────────────────────────────
        flt = ttk.Frame(self)
        flt.pack(fill=tk.X, padx=10, pady=(2, 0))
        ttk.Label(flt, text=L('aes_search', 'Cerca') + ':').pack(side=tk.LEFT, padx=(0, 4))
        self._v_search = tk.StringVar()
        self._v_search.trace_add('write', lambda *_: self._refresh_tree())
        e_search = ttk.Entry(flt, textvariable=self._v_search, width=32)
        e_search.pack(side=tk.LEFT)
        ttk.Button(flt, text=L('aes_clear_filter', '✖ Azzera'),
                   command=lambda: (self._v_search.set(''),
                                    self._v_status.set(self._status_opts[0]))).pack(side=tk.LEFT, padx=4)
        self._status_opts = (L('aes_f_all', 'Tutti'),
                             L('aes_f_sub', 'Solo iscritti'),
                             L('aes_f_unsub', 'Solo non iscritti'))
        self._v_status = tk.StringVar(value=self._status_opts[0])
        cb = ttk.Combobox(flt, textvariable=self._v_status, values=self._status_opts,
                          state='readonly', width=18)
        cb.pack(side=tk.LEFT, padx=(12, 0))
        cb.bind('<<ComboboxSelected>>', lambda _e: self._refresh_tree())
        self._lbl_count = ttk.Label(flt, text='', foreground='#555')
        self._lbl_count.pack(side=tk.RIGHT)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('attr', 'name', 'sub', 'mand')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('attr', text=L('aes_c_attr', 'Servizio (attributo)'))
        self.tree.heading('name', text=L('aes_c_name', 'Descrizione'))
        self.tree.heading('sub', text=L('aes_c_sub', 'Iscritto'))
        self.tree.heading('mand', text=L('aes_c_mand', 'Obbligatoria'))
        self.tree.column('attr', width=250, anchor='w')
        self.tree.column('name', width=300, anchor='w')
        self.tree.column('sub', width=90, anchor='center')
        self.tree.column('mand', width=100, anchor='center')
        self.tree.tag_configure('mand', foreground='#B71C1C')
        self.tree.tag_configure('unsub', foreground='#888888')
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree.bind('<Double-1>', lambda _e: self._toggle())

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('aes_btn_sub', '✅ Iscriviti'),
                   command=self._subscribe).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('aes_btn_unsub', '🚫 Non ricevere più'),
                   command=self._unsubscribe).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('aes_btn_admin', '🔧 Gestione servizi (super user)'),
                   command=self._open_admin).pack(side=tk.LEFT, padx=16)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _load(self):
        """Rilegge tutti i servizi dal DB e ricalcola lo stato di iscrizione."""
        self._all_rows = []
        self._rows_by_id = {}
        if not self.user_email:
            self._refresh_tree()
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('aes_no_email_msg',
                              'Impossibile determinare la tua email aziendale.\n'
                              'Nessun servizio da mostrare.'),
                parent=self)
            return
        try:
            rows = _fetch(self.db,
                          "SELECT IDSettings, Atribute, Value, Name, ISNULL(IsBlocked,0) AS IsBlocked "
                          "FROM traceability_rs.dbo.settings "
                          "WHERE Employeerid = ? ORDER BY Atribute", (EMPLOYERID,))
        except Exception as e:
            logger.error(f"Load auto-email settings: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
            return
        email_low = self.user_email.lower()
        for r in rows:
            r['_subscribed'] = email_low in [x.lower() for x in _split_recipients(r['Value'])]
            self._all_rows.append(r)
            self._rows_by_id[r['IDSettings']] = r
        self._refresh_tree()

    def _refresh_tree(self):
        """Ripopola la treeview applicando i filtri correnti (nessuna query DB)."""
        L = self.lang.get
        prev = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        needle = self._v_search.get().strip().lower()
        status = self._v_status.get()
        shown = 0
        for r in self._all_rows:
            if status == self._status_opts[1] and not r['_subscribed']:
                continue
            if status == self._status_opts[2] and r['_subscribed']:
                continue
            if needle and needle not in ((r['Atribute'] or '') + ' ' +
                                         (r['Name'] or '')).lower():
                continue
            tags = []
            if r['IsBlocked']:
                tags.append('mand')
            if not r['_subscribed']:
                tags.append('unsub')
            self.tree.insert('', 'end', iid=str(r['IDSettings']),
                             values=(r['Atribute'],
                                     r['Name'] or '',
                                     L('yes', 'Sì') if r['_subscribed'] else L('no', 'No'),
                                     L('yes', 'Sì') if r['IsBlocked'] else L('no', 'No')),
                             tags=tuple(tags))
            shown += 1
        self._lbl_count.config(text=L('aes_count', '{0} di {1} servizi').format(
            shown, len(self._all_rows)))
        for iid in prev:
            if self.tree.exists(iid):
                self.tree.selection_set(iid)
                self.tree.see(iid)
                break

    def _selected_id(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def _selected_row(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('aes_select_row', 'Seleziona un servizio.'),
                                parent=self)
            return None
        return self._rows_by_id.get(sid)

    def _current_recipients(self, sid):
        """Rilegge Value dal DB per non sovrascrivere modifiche concorrenti."""
        rows = _fetch(self.db, "SELECT Value FROM traceability_rs.dbo.settings "
                               "WHERE IDSettings = ?", (sid,))
        return _split_recipients(rows[0]['Value'] if rows else '')

    def _write_recipients(self, sid, recips):
        _exec(self.db,
              "UPDATE traceability_rs.dbo.settings SET Value = ?, LastCheck = GETDATE() "
              "WHERE IDSettings = ?", ('; '.join(recips), sid))

    def _toggle(self):
        """Doppio click: iscrive o disiscrive a seconda dello stato corrente."""
        row = self._selected_row()
        if row:
            self._unsubscribe() if row['_subscribed'] else self._subscribe()

    def _subscribe(self):
        L = self.lang.get
        row = self._selected_row()
        if not row:
            return
        if not self.user_email:
            return
        if row['_subscribed']:
            messagebox.showinfo(L('info', 'Info'),
                                L('aes_already_sub', 'Sei già iscritto a questo servizio.'),
                                parent=self)
            return
        if not messagebox.askyesno(
                L('confirm', 'Conferma'),
                L('aes_sub_confirm', 'Vuoi iscriverti a "{0}"?').format(row['Atribute']),
                parent=self):
            return
        sid = row['IDSettings']
        try:
            recips = self._current_recipients(sid)
            if self.user_email.lower() not in [x.lower() for x in recips]:
                recips.append(self.user_email)
                self._write_recipients(sid, recips)
                logger.info("Subscribe: %s aggiunto a IDSettings=%s (%s)",
                            self.user_email, sid, row['Atribute'])
            messagebox.showinfo(L('info', 'Info'),
                                L('aes_sub_done', 'Riceverai questa email.'), parent=self)
            self._load()
        except Exception as e:
            logger.error(f"Subscribe error: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)

    def _unsubscribe(self):
        L = self.lang.get
        row = self._selected_row()
        if not row:
            return
        if not row['_subscribed']:
            messagebox.showinfo(L('info', 'Info'),
                                L('aes_not_sub', 'Non sei iscritto a questo servizio.'),
                                parent=self)
            return
        sid = row['IDSettings']

        def do_unsub():
            try:
                recips = [x for x in self._current_recipients(sid)
                          if x.lower() != self.user_email.lower()]
                self._write_recipients(sid, recips)
                logger.info("Unsubscribe: %s rimosso da IDSettings=%s (%s)",
                            self.user_email, sid, row['Atribute'])
                messagebox.showinfo(L('info', 'Info'),
                                    L('aes_unsub_done', 'Non riceverai più questa email.'),
                                    parent=self)
                self._load()
            except Exception as e:
                logger.error(f"Unsubscribe error: {e}", exc_info=True)
                messagebox.showerror(L('error', 'Errore'), str(e), parent=self)

        if not messagebox.askyesno(
                L('confirm', 'Conferma'),
                L('aes_unsub_confirm', 'Vuoi smettere di ricevere "{0}"?').format(
                    row['Atribute']), parent=self):
            return
        if row['IsBlocked']:
            # Servizio obbligatorio: richiede super user
            messagebox.showinfo(
                L('info', 'Info'),
                L('aes_mand_needs_super',
                  'Questo servizio è obbligatorio: serve l\'autorizzazione di un super user.'),
                parent=self)
            self._ensure_super(do_unsub)
        else:
            do_unsub()

    def _open_admin(self):
        def after_auth():
            try:
                self.grab_release()
            except Exception:
                pass
            w = AutoEmailAdminWindow(self, self.db, self.lang)
            self.wait_window(w)
            try:
                self.grab_set()
            except Exception:
                pass
            self._load()
        self._ensure_super(after_auth)

    def _ensure_super(self, on_ok):
        """Esegue on_ok solo dopo autorizzazione super user (chiave KEY_SUPER).
        In-sessione l'autorizzazione viene ricordata."""
        if self._super_ok:
            on_ok()
            return
        master = self.master
        if not hasattr(master, '_execute_authorized_action'):
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('aes_no_auth', 'Autorizzazione non disponibile.'),
                                 parent=self)
            return

        def cb():
            self._super_ok = True
            on_ok()

        try:
            self.grab_release()
        except Exception:
            pass
        try:
            master._execute_authorized_action(KEY_SUPER, cb)
        finally:
            try:
                self.grab_set()
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
#  Vista admin (tier2) — aperta solo dopo login super user
# ─────────────────────────────────────────────────────────────────────────────
class AutoEmailAdminWindow(tk.Toplevel):
    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang
        L = self.lang.get
        self.title(L('aes_admin_title', 'Gestione Servizi Email Automatiche (super user)'))
        self.geometry('1000x600')
        self.minsize(820, 480)
        self.transient(master)
        self._build_ui()
        self.grab_set()
        self._load()

    def _build_ui(self):
        L = self.lang.get
        header = tk.Frame(self, bg='#7B1FA2')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('aes_admin_title', 'Gestione Servizi Email Automatiche (super user)'),
                 bg='#7B1FA2', fg='white', font=('Helvetica', 12, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=8)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=(8, 4))
        cols = ('id', 'attr', 'name', 'value', 'mand')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, h, w, anc in (
                ('id', 'ID', 50, 'center'),
                ('attr', L('aes_c_attr', 'Servizio (attributo)'), 220, 'w'),
                ('name', L('aes_c_name', 'Descrizione'), 220, 'w'),
                ('value', L('aes_c_value', 'Destinatari'), 360, 'w'),
                ('mand', L('aes_c_mand', 'Obbligatoria'), 90, 'center')):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor=anc)
        self.tree.tag_configure('mand', foreground='#B71C1C')
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Editor
        ed = ttk.LabelFrame(self, text=L('aes_editor', 'Modifica servizio selezionato'))
        ed.pack(fill=tk.X, padx=10, pady=4)
        ttk.Label(ed, text=L('aes_c_attr', 'Servizio (attributo)') + ':').grid(row=0, column=0, sticky='w', padx=6, pady=4)
        self._v_attr = tk.StringVar()
        self._e_attr = ttk.Entry(ed, textvariable=self._v_attr, width=30, state='readonly')
        self._e_attr.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        ttk.Label(ed, text=L('aes_c_name', 'Descrizione') + ':').grid(row=0, column=2, sticky='w', padx=6, pady=4)
        self._v_name = tk.StringVar()
        ttk.Entry(ed, textvariable=self._v_name, width=34).grid(row=0, column=3, sticky='w', padx=4, pady=4)
        ttk.Label(ed, text=L('aes_c_value', 'Destinatari') + ':').grid(row=1, column=0, sticky='w', padx=6, pady=4)
        self._v_value = tk.StringVar()
        ttk.Entry(ed, textvariable=self._v_value, width=90).grid(
            row=1, column=1, columnspan=3, sticky='we', padx=4, pady=4)
        self._v_mand = tk.BooleanVar(value=False)
        ttk.Checkbutton(ed, text=L('aes_mandatory', 'Obbligatoria (non disattivabile dagli utenti)'),
                        variable=self._v_mand).grid(row=2, column=1, columnspan=3, sticky='w', padx=4, pady=4)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('aes_btn_save', '💾 Salva modifiche'),
                   command=self._save).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('aes_btn_add', '➕ Aggiungi servizio'),
                   command=self._add).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        self._rows_by_id = {}
        try:
            rows = _fetch(self.db,
                          "SELECT IDSettings, Atribute, Value, Name, ISNULL(IsBlocked,0) AS IsBlocked "
                          "FROM traceability_rs.dbo.settings "
                          "WHERE Employeerid = ? ORDER BY Atribute", (EMPLOYERID,))
        except Exception as e:
            logger.error(f"Admin load: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
            return
        for r in rows:
            self._rows_by_id[r['IDSettings']] = r
            mand = self.lang.get('yes', 'Sì') if r['IsBlocked'] else self.lang.get('no', 'No')
            self.tree.insert('', 'end', iid=str(r['IDSettings']),
                             values=(r['IDSettings'], r['Atribute'], r['Name'] or '',
                                     r['Value'] or '', mand),
                             tags=('mand',) if r['IsBlocked'] else ())

    def _on_select(self, _e=None):
        sel = self.tree.selection()
        if not sel:
            return
        r = self._rows_by_id.get(int(sel[0]))
        if not r:
            return
        self._v_attr.set(r['Atribute'] or '')
        self._v_name.set(r['Name'] or '')
        self._v_value.set(r['Value'] or '')
        self._v_mand.set(bool(r['IsBlocked']))

    def _save(self):
        L = self.lang.get
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(L('info', 'Info'), L('aes_select_row', 'Seleziona un servizio.'), parent=self)
            return
        sid = int(sel[0])
        name = self._v_name.get().strip() or None
        value = self._v_value.get().strip()
        is_blocked = 1 if self._v_mand.get() else 0
        try:
            _exec(self.db,
                  "UPDATE traceability_rs.dbo.settings "
                  "SET Name = ?, Value = ?, IsBlocked = ?, LastCheck = GETDATE() "
                  "WHERE IDSettings = ?", (name, value, is_blocked, sid))
            logger.info("Admin update IDSettings=%s IsBlocked=%s", sid, is_blocked)
            messagebox.showinfo(L('info', 'Info'), L('aes_saved', 'Modifiche salvate.'), parent=self)
            self._load()
        except Exception as e:
            logger.error(f"Admin save: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)

    def _add(self):
        AutoEmailAddDialog(self, self.db, self.lang, on_done=self._load)


class AutoEmailAddDialog(tk.Toplevel):
    def __init__(self, master, db, lang, on_done=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.on_done = on_done
        L = self.lang.get
        self.title(L('aes_add_title', 'Nuovo servizio email'))
        self.geometry('560x260')
        self.resizable(False, False)
        self.transient(master)

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text=L('aes_c_attr', 'Servizio (attributo)') + ':').grid(row=0, column=0, sticky='w', pady=5)
        self._v_attr = tk.StringVar()
        ttk.Entry(frm, textvariable=self._v_attr, width=40).grid(row=0, column=1, sticky='w', pady=5)
        ttk.Label(frm, text=L('aes_c_name', 'Descrizione') + ':').grid(row=1, column=0, sticky='w', pady=5)
        self._v_name = tk.StringVar()
        ttk.Entry(frm, textvariable=self._v_name, width=40).grid(row=1, column=1, sticky='w', pady=5)
        ttk.Label(frm, text=L('aes_c_value', 'Destinatari') + ':').grid(row=2, column=0, sticky='w', pady=5)
        self._v_value = tk.StringVar()
        ttk.Entry(frm, textvariable=self._v_value, width=40).grid(row=2, column=1, sticky='w', pady=5)
        self._v_mand = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text=L('aes_mandatory', 'Obbligatoria (non disattivabile dagli utenti)'),
                        variable=self._v_mand).grid(row=3, column=1, sticky='w', pady=6)

        bar = ttk.Frame(frm)
        bar.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(bar, text=L('aes_btn_create', 'Crea'), command=self._create).pack(side=tk.LEFT, padx=6)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.LEFT, padx=6)
        self.grab_set()

    def _create(self):
        L = self.lang.get
        attr = self._v_attr.get().strip()
        if not attr:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('aes_attr_required', 'Il nome attributo è obbligatorio.'), parent=self)
            return
        value = self._v_value.get().strip()
        name = self._v_name.get().strip() or None
        is_blocked = 1 if self._v_mand.get() else 0
        try:
            # unicità attributo per Employeerid=2
            dup = _fetch(self.db,
                         "SELECT COUNT(*) AS n FROM traceability_rs.dbo.settings "
                         "WHERE Atribute = ? AND Employeerid = ?", (attr, EMPLOYERID))
            if dup and dup[0]['n'] > 0:
                messagebox.showwarning(L('warning', 'Attenzione'),
                                       L('aes_attr_dup', 'Esiste già un servizio con questo attributo.'),
                                       parent=self)
                return
            _exec(self.db,
                  "INSERT INTO traceability_rs.dbo.settings "
                  "(Atribute, Value, Name, IsBlocked, Employeerid, LastCheck) "
                  "VALUES (?, ?, ?, ?, ?, GETDATE())",
                  (attr, value, name, is_blocked, EMPLOYERID))
            logger.info("Admin add service Atribute=%s IsBlocked=%s", attr, is_blocked)
            messagebox.showinfo(L('info', 'Info'), L('aes_added', 'Servizio aggiunto.'), parent=self)
            if self.on_done:
                self.on_done()
            self.destroy()
        except Exception as e:
            logger.error(f"Admin add: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
