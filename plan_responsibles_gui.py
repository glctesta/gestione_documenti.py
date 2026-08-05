# -*- coding: utf-8 -*-
"""
plan_responsibles_gui.py — Maschera di gestione dei responsabili del piano.

Mostra i responsabili calcolati dalla regola (FunctionCode 61..89 = TO,
90/100 = CC, CdcId=1) e consente di:
  - escludere una persona calcolata dalla regola (es. in ferie);
  - riattivare una persona esclusa;
  - aggiungere un destinatario manuale (TO o CC);
  - rimuovere un destinatario manuale;
  - impostare la data di partenza delle discrepanze aperte;
  - fare l'anteprima dell'email e inviarla subito (rispetta la modalità
    Sys_enable_control_plan_check: in Test l'email va solo a te).

Le modifiche sono persistite in dbo.PlanResponsibleOverrides.
"""

import os
import tempfile
import webbrowser
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

import plan_responsibles as pr

try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

logger = logging.getLogger("TraceabilityRS")


def open_plan_responsibles(parent, db, lang, user_name):
    """Entry-point richiamato da main.py."""
    PlanResponsiblesWindow(parent, db, lang, user_name)


class PlanResponsiblesWindow(tk.Toplevel):
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        L = self.lang.get

        self.title(L('plan_resp_title', 'Responsabili Piano Produzione'))
        self.geometry('900x560')
        self.minsize(760, 460)
        self.transient(parent)
        self.grab_set()

        self._row_data = {}   # iid -> dict
        self._build_ui()
        self._load()

    # ------------------------------------------------------------------ #
    def _build_ui(self):
        L = self.lang.get

        # --- Riga data di partenza ---
        top = ttk.LabelFrame(self, text=L('plan_resp_startdate',
            'Discrepanze aperte a partire dalla data'), padding=8)
        top.pack(fill='x', padx=10, pady=(10, 4))
        cur_start = pr.get_start_date(self.db.conn)
        if DateEntry:
            self.start_entry = DateEntry(top, width=12, date_pattern='dd/mm/yyyy', locale='it_IT')
            self.start_entry.set_date(cur_start)
        else:
            self.start_entry = ttk.Entry(top, width=12)
            self.start_entry.insert(0, cur_start.strftime('%d/%m/%Y'))
        self.start_entry.pack(side='left', padx=(0, 8))
        ttk.Button(top, text=L('plan_resp_save_date', '💾 Salva data'),
                   command=self._save_start_date).pack(side='left')

        # Modalità dedicata dell'email (Test/True/False), indipendente dall'escalation
        ttk.Label(top, text=L('plan_resp_email_mode', 'Modalità email:')).pack(side='left', padx=(24, 4))
        self.mode_var = tk.StringVar(value=pr.get_email_mode(self.db.conn))
        self.mode_combo = ttk.Combobox(top, textvariable=self.mode_var, width=8, state='readonly',
                                       values=['Test', 'True', 'False'])
        self.mode_combo.pack(side='left')
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self._change_mode())
        ttk.Label(top, text=L('plan_resp_mode_hint',
            '(Test = solo a te; True = ai responsabili; False = spento)'),
            font=('Arial', 8), foreground='#888').pack(side='left', padx=(6, 0))

        # --- Toolbar azioni ---
        tb = ttk.Frame(self)
        tb.pack(fill='x', padx=10, pady=(4, 0))
        ttk.Button(tb, text=L('plan_resp_toggle', '⛔ Escludi / ✅ Riattiva'),
                   command=self._toggle_selected).pack(side='left', padx=3)
        ttk.Button(tb, text=L('plan_resp_add', '➕ Aggiungi manuale'),
                   command=self._add_manual).pack(side='left', padx=3)
        ttk.Button(tb, text=L('plan_resp_remove', '🗑 Rimuovi manuale'),
                   command=self._remove_manual).pack(side='left', padx=3)
        ttk.Button(tb, text=L('btn_refresh', '🔄 Aggiorna'),
                   command=self._load).pack(side='left', padx=3)
        ttk.Button(tb, text=L('plan_resp_preview', '👁 Anteprima email'),
                   command=self._preview).pack(side='right', padx=3)
        ttk.Button(tb, text=L('plan_resp_send', '📧 Invia adesso'),
                   command=self._send_now).pack(side='right', padx=3)

        # --- Tabella destinatari ---
        wrap = ttk.Frame(self)
        wrap.pack(fill='both', expand=True, padx=10, pady=8)
        cols = ('name', 'email', 'fc', 'role', 'origin', 'state')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        headers = {
            'name':   L('plan_resp_col_name', 'Nome'),
            'email':  L('plan_resp_col_email', 'Email'),
            'fc':     L('plan_resp_col_fc', 'FC'),
            'role':   L('plan_resp_col_role', 'Ruolo'),
            'origin': L('plan_resp_col_origin', 'Origine'),
            'state':  L('plan_resp_col_state', 'Stato'),
        }
        widths = {'name': 220, 'email': 250, 'fc': 50, 'role': 60, 'origin': 90, 'state': 90}
        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c],
                             anchor='center' if c in ('fc', 'role', 'origin', 'state') else 'w')
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='left', fill='y')
        self.tree.tag_configure('excluded', background='#f8d7da')
        self.tree.tag_configure('manual', background='#d8f5d8')
        self.tree.tag_configure('cc', foreground='#555')

        # --- Footer ---
        footer = ttk.Frame(self, padding=6)
        footer.pack(fill='x', padx=10)
        self.info_label = ttk.Label(footer, text='', font=('Arial', 9), foreground='#555')
        self.info_label.pack(side='left')
        ttk.Button(footer, text=L('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side='right')

    # ------------------------------------------------------------------ #
    def _load(self):
        self.tree.delete(*self.tree.get_children())
        self._row_data = {}
        rule = pr.get_rule_responsibles(self.db.conn)
        overrides = pr.list_overrides(self.db.conn)
        excl = {}   # (role, email_lower) -> override_id
        incl = []
        for o in overrides:
            if o['action'] == 'EXCLUDE':
                excl[(o['role'], o['email'].lower())] = o['id']
            elif o['action'] == 'INCLUDE':
                incl.append(o)

        n_to = n_cc = 0
        for role, people in (('TO', rule['to']), ('CC', rule['cc'])):
            for p in people:
                oid = excl.get((role, p['email'].lower()))
                excluded = oid is not None
                tags = []
                if excluded:
                    tags.append('excluded')
                if role == 'CC':
                    tags.append('cc')
                iid = self.tree.insert('', 'end', values=(
                    p['name'], p['email'], p.get('functioncode', ''),
                    role, self.lang.get('plan_resp_origin_rule', 'Regola'),
                    (self.lang.get('plan_resp_excluded', 'Escluso') if excluded
                     else self.lang.get('plan_resp_active', 'Attivo'))
                ), tags=tuple(tags))
                self._row_data[iid] = {'email': p['email'], 'name': p['name'],
                                       'role': role, 'origin': 'rule',
                                       'excluded': excluded, 'exclude_id': oid}
                if not excluded:
                    n_to += (role == 'TO')
                    n_cc += (role == 'CC')

        for o in incl:
            tags = ['manual'] + (['cc'] if o['role'] == 'CC' else [])
            iid = self.tree.insert('', 'end', values=(
                o['name'] or o['email'], o['email'], '', o['role'],
                self.lang.get('plan_resp_origin_manual', 'Manuale'),
                self.lang.get('plan_resp_active', 'Attivo')
            ), tags=tuple(tags))
            self._row_data[iid] = {'email': o['email'], 'name': o['name'],
                                   'role': o['role'], 'origin': 'manual',
                                   'excluded': False, 'override_id': o['id']}
            n_to += (o['role'] == 'TO')
            n_cc += (o['role'] == 'CC')

        self.info_label.config(text=self.lang.get(
            'plan_resp_counts', 'Destinatari attivi — TO: {to}  |  CC: {cc}').format(
                to=n_to, cc=n_cc))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('plan_resp_select', 'Seleziona una riga.'),
                                parent=self)
            return None, None
        return sel[0], self._row_data.get(sel[0])

    # ------------------------------------------------------------------ #
    def _save_start_date(self):
        L = self.lang.get
        if DateEntry and hasattr(self.start_entry, 'get_date'):
            d = self.start_entry.get_date()
        else:
            try:
                d = datetime.strptime(self.start_entry.get().strip(), '%d/%m/%Y').date()
            except Exception:
                messagebox.showerror(L('error', 'Errore'),
                                     L('plan_resp_bad_date', 'Data non valida (gg/mm/aaaa).'),
                                     parent=self)
                return
        if pr.set_start_date(self.db.conn, d):
            messagebox.showinfo(L('success', 'OK'),
                                L('plan_resp_date_saved', 'Data di partenza salvata: {d}').format(
                                    d=d.strftime('%d/%m/%Y')), parent=self)
        else:
            messagebox.showerror(L('error', 'Errore'),
                                 L('plan_resp_date_err', 'Impossibile salvare la data.'), parent=self)

    def _change_mode(self):
        L = self.lang.get
        new_mode = self.mode_var.get()
        if new_mode == 'True':
            if not messagebox.askyesno(
                    L('warning', 'Attenzione'),
                    L('plan_resp_confirm_live',
                      'Impostando "True" l\'email verrà inviata ai RESPONSABILI REALI '
                      '(e in copia ai manager) ogni mattina. Confermi?'), parent=self):
                self.mode_var.set(pr.get_email_mode(self.db.conn))
                return
        if not pr.set_email_mode(self.db.conn, new_mode):
            messagebox.showerror(L('error', 'Errore'),
                                 L('plan_resp_mode_err', 'Impossibile salvare la modalità.'),
                                 parent=self)
            self.mode_var.set(pr.get_email_mode(self.db.conn))

    def _toggle_selected(self):
        L = self.lang.get
        _iid, data = self._selected()
        if not data:
            return
        if data['origin'] == 'manual':
            messagebox.showinfo(L('info', 'Info'),
                                L('plan_resp_use_remove',
                                  'Per i destinatari manuali usa "Rimuovi manuale".'), parent=self)
            return
        if data['excluded']:
            # riattiva: rimuovi l'override EXCLUDE
            if pr.remove_override(self.db.conn, data['exclude_id'], self.user_name):
                self._load()
        else:
            if pr.add_override(self.db.conn, data['email'], data['name'],
                               data['role'], 'EXCLUDE', self.user_name):
                self._load()

    def _add_manual(self):
        L = self.lang.get
        email = simpledialog.askstring(
            L('plan_resp_add', 'Aggiungi manuale'),
            L('plan_resp_ask_email', 'Indirizzo email:'), parent=self)
        if not email or '@' not in email:
            if email is not None:
                messagebox.showerror(L('error', 'Errore'),
                                     L('plan_resp_bad_email', 'Email non valida.'), parent=self)
            return
        name = simpledialog.askstring(
            L('plan_resp_add', 'Aggiungi manuale'),
            L('plan_resp_ask_name', 'Nome (facoltativo):'), parent=self) or ''
        # Ruolo TO/CC
        role = self._ask_role()
        if not role:
            return
        if pr.add_override(self.db.conn, email.strip(), name.strip(), role, 'INCLUDE', self.user_name):
            self._load()

    def _ask_role(self):
        """Piccola finestra per scegliere TO o CC."""
        L = self.lang.get
        dlg = tk.Toplevel(self)
        dlg.title(L('plan_resp_col_role', 'Ruolo'))
        dlg.transient(self)
        dlg.grab_set()
        ttk.Label(dlg, text=L('plan_resp_ask_role', 'Ruolo del destinatario:'),
                  padding=10).pack()
        choice = {'val': None}
        btns = ttk.Frame(dlg, padding=8)
        btns.pack()
        def pick(v):
            choice['val'] = v
            dlg.destroy()
        ttk.Button(btns, text='TO (responsabile)', command=lambda: pick('TO')).pack(side='left', padx=6)
        ttk.Button(btns, text='CC (management)', command=lambda: pick('CC')).pack(side='left', padx=6)
        self.wait_window(dlg)
        return choice['val']

    def _remove_manual(self):
        L = self.lang.get
        _iid, data = self._selected()
        if not data:
            return
        if data['origin'] != 'manual':
            messagebox.showinfo(L('info', 'Info'),
                                L('plan_resp_only_manual',
                                  'Solo i destinatari manuali possono essere rimossi. '
                                  'Per quelli da regola usa Escludi.'), parent=self)
            return
        if messagebox.askyesno(L('confirm', 'Conferma'),
                               L('plan_resp_confirm_remove',
                                 'Rimuovere {e} dai destinatari?').format(e=data['email']),
                               parent=self):
            if pr.remove_override(self.db.conn, data['override_id'], self.user_name):
                self._load()

    # ------------------------------------------------------------------ #
    def _preview(self):
        try:
            # only_new: l'anteprima deve mostrare cio' che partirebbe davvero,
            # cioe' senza le righe gia' inviate e rimaste uguali.
            data = pr.gather(self.db.conn, only_new=True)
            html = pr.build_email_html(data)
            fd, path = tempfile.mkstemp(suffix='.html', prefix='plan_resp_')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(html)
            webbrowser.open('file://' + path)
        except Exception as e:
            logger.error(f"Anteprima email responsabili: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _send_now(self):
        L = self.lang.get
        mode = pr.get_email_mode(self.db.conn)   # modalità dedicata dell'email
        if mode == 'False':
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('plan_resp_disabled',
                                     'Modalità email = False: invio disattivato. '
                                     'Imposta Test o True per inviare.'),
                                   parent=self)
            return
        to, cc, _tp, _cp = pr.get_effective_recipients(self.db.conn)
        dest = (L('plan_resp_test_dest', 'MODALITÀ TEST: verrà inviata solo a te.')
                if mode == 'Test'
                else L('plan_resp_real_dest', 'TO: {to}\nCC: {cc}').format(
                    to=', '.join(to) or '—', cc=', '.join(cc) or '—'))
        if not messagebox.askyesno(
                L('confirm', 'Conferma'),
                L('plan_resp_confirm_send', 'Inviare adesso l\'email ai responsabili?\n\n{dest}').format(
                    dest=dest), parent=self):
            return
        sent, msg = pr.send_daily_responsibles_email(
            self.db.conn, mode=mode, logo_path='logo.png', force=True)
        if sent:
            messagebox.showinfo(L('success', 'OK'), msg, parent=self)
        else:
            messagebox.showwarning(L('warning', 'Attenzione'), msg, parent=self)
