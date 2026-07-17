# -*- coding: utf-8 -*-
"""
label_scrap_gui.py — Dichiarazione scarti etichette.

Form (login operatore) dove l'operatore scansiona le etichette scartate con data,
motivo (dedicati, in rumeno) e categoria Produzione/Stampa. Ad ogni scansione i
contatori mostrano: sessione, settimana/mese/anno dell'operatore, e totale generale.
Alla chiusura offre la stampa del riepilogo (PDF con logo).

Tabelle: traceability_rs.dbo.labelscrap, dbo.LabelScrapReasons.
Il codice etichetta si accetta come testo; se noto in LabelCodes si salva l'IDLabelCode.
"""
import os
import socket
import logging
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

logger = logging.getLogger(__name__)

CATEGORIES = (('Production', 'Produzione'), ('Print', 'Stampa'))


def current_shift(now=None):
    """Turno corrente come etichetta di fine: 07:30 / 15:30 / 23:30."""
    now = now or datetime.now()
    t = now.hour * 60 + now.minute
    if 7 * 60 + 30 <= t < 15 * 60 + 30:
        return '07:30'
    if 15 * 60 + 30 <= t < 23 * 60 + 30:
        return '15:30'
    return '23:30'


def open_label_scrap_declaration(parent, db, lang):
    """Entry point: apre la form di dichiarazione scarti etichette."""
    operator = getattr(parent, 'last_authenticated_user_name', '') or 'Unknown'
    LabelScrapDeclarationWindow(parent, db, lang, operator)


class LabelScrapDeclarationWindow(tk.Toplevel):
    def __init__(self, parent, db, lang, operator):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.operator = operator
        self._session_rows = []  # dict: label, reason, category, time, id
        L = self.lang.get

        self.title(L('lsc_title', 'Dichiarazione Scarti Etichette'))
        self.geometry('820x560')
        self.minsize(720, 500)
        self.transient(parent)
        self._reason_map = {}
        self._build_ui()
        self._load_reasons()
        self._refresh_counters()
        self.grab_set()
        self.scan_entry.focus_set()

    # ── UI ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        L = self.lang.get
        head = tk.Frame(self, bg='#1F3864')
        head.pack(fill=tk.X)
        tk.Label(head, text=L('lsc_title', 'Dichiarazione Scarti Etichette'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)
        tk.Label(head, text=f"{L('lsc_operator', 'Operatore')}: {self.operator}",
                 bg='#1F3864', fg='#cfe0f5', font=('Helvetica', 10, 'bold')).pack(
            side=tk.RIGHT, padx=12)

        form = ttk.Frame(self, padding=10)
        form.pack(fill=tk.X)

        ttk.Label(form, text=L('lsc_date', 'Data') + ':').grid(row=0, column=0, sticky='w', pady=4)
        if DateEntry:
            self.date_entry = DateEntry(form, width=12, date_pattern='dd/mm/yyyy', locale='it_IT')
            self.date_entry.grid(row=0, column=1, sticky='w', padx=(4, 20))
        else:
            self.date_entry = ttk.Entry(form, width=12)
            self.date_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
            self.date_entry.grid(row=0, column=1, sticky='w', padx=(4, 20))

        ttk.Label(form, text=L('lsc_reason', 'Motivo') + ':').grid(row=0, column=2, sticky='w', pady=4)
        self.reason_combo = ttk.Combobox(form, width=32, state='readonly')
        self.reason_combo.grid(row=0, column=3, sticky='w', padx=4)

        ttk.Label(form, text=L('lsc_category', 'Categoria') + ':').grid(row=1, column=0, sticky='w', pady=4)
        self.category_var = tk.StringVar(value='Production')
        cat_fr = ttk.Frame(form)
        cat_fr.grid(row=1, column=1, columnspan=2, sticky='w')
        for val, _label in CATEGORIES:
            ttk.Radiobutton(cat_fr, text=L('lsc_cat_' + val.lower(), _label),
                            variable=self.category_var, value=val).pack(side=tk.LEFT, padx=(0, 12))

        ttk.Label(form, text=L('lsc_scan', 'Scansiona etichetta') + ':').grid(
            row=2, column=0, sticky='w', pady=(10, 4))
        self.scan_entry = ttk.Entry(form, width=40, font=('Consolas', 11))
        self.scan_entry.grid(row=2, column=1, columnspan=2, sticky='w', pady=(10, 4))
        self.scan_entry.bind('<Return>', self._on_scan)
        ttk.Button(form, text=L('lsc_add', 'Aggiungi'), command=self._on_scan).grid(
            row=2, column=3, sticky='w', padx=4, pady=(10, 4))

        # ── Contatori ────────────────────────────────────────────────────
        cnt = ttk.LabelFrame(self, text=L('lsc_counters', 'Contatori'))
        cnt.pack(fill=tk.X, padx=10, pady=6)
        self._cnt_vars = {k: tk.StringVar(value='0') for k in
                          ('session', 'week', 'month', 'year', 'general')}
        labels = [('session', L('lsc_c_session', 'Sessione')),
                  ('week', L('lsc_c_week', 'Settimana (tu)')),
                  ('month', L('lsc_c_month', 'Mese (tu)')),
                  ('year', L('lsc_c_year', 'Anno (tu)')),
                  ('general', L('lsc_c_general', 'Generale (tutti)'))]
        for i, (k, lbl) in enumerate(labels):
            cell = ttk.Frame(cnt)
            cell.grid(row=0, column=i, padx=12, pady=6, sticky='w')
            tk.Label(cell, textvariable=self._cnt_vars[k], font=('Helvetica', 18, 'bold'),
                     fg='#1F3864').pack()
            tk.Label(cell, text=lbl, font=('Helvetica', 8), fg='#555').pack()

        # ── Lista sessione ───────────────────────────────────────────────
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('n', 'label', 'reason', 'cat', 'time')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, txt, w, a in (('n', '#', 40, 'center'), ('label', L('lsc_scan', 'Etichetta'), 240, 'w'),
                             ('reason', L('lsc_reason', 'Motivo'), 240, 'w'),
                             ('cat', L('lsc_category', 'Categoria'), 100, 'center'),
                             ('time', L('lsc_time', 'Ora'), 80, 'center')):
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('lsc_undo', '↩ Annulla ultima'),
                   command=self._undo_last).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('lsc_manage_reasons', '⚙ Motivi'),
                   command=self._open_reasons_manager).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('lsc_close_print', '🖨 Chiudi e stampa'),
                   command=lambda: self._close(print_it=True)).pack(side=tk.RIGHT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=lambda: self._close(print_it=None)).pack(side=tk.RIGHT, padx=4)
        self.protocol('WM_DELETE_WINDOW', lambda: self._close(print_it=None))

    # ── Dati ──────────────────────────────────────────────────────────────
    def _load_reasons(self):
        self._reason_map = {}
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT LabelScrapReasonId, Reason FROM traceability_rs.dbo.LabelScrapReasons "
                        "WHERE IsActive = 1 ORDER BY Reason")
            rows = cur.fetchall()
            cur.close()
        except Exception as e:
            logger.error(f"Load motivi scarto: {e}", exc_info=True)
            rows = []
        labels = []
        for r in rows:
            self._reason_map[r.Reason] = r.LabelScrapReasonId
            labels.append(r.Reason)
        self.reason_combo['values'] = labels
        if labels:
            self.reason_combo.current(0)

    def _resolve_label_id(self, code):
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT TOP 1 IDLabelCode FROM traceability_rs.dbo.LabelCodes WHERE LabelCod = ?", (code,))
            row = cur.fetchone()
            cur.close()
            return row[0] if row else None
        except Exception:
            return None

    def _get_date(self):
        if DateEntry and hasattr(self.date_entry, 'get_date'):
            return self.date_entry.get_date()
        try:
            return datetime.strptime(self.date_entry.get().strip(), '%d/%m/%Y').date()
        except Exception:
            return datetime.now().date()

    def _on_scan(self, event=None):
        L = self.lang.get
        code = self.scan_entry.get().strip()
        if not code:
            return
        reason_txt = self.reason_combo.get()
        reason_id = self._reason_map.get(reason_txt)
        if not reason_id:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('lsc_pick_reason', 'Selezionare un motivo.'), parent=self)
            return
        category = self.category_var.get()
        scrap_date = self._get_date()
        id_label = self._resolve_label_id(code)
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                INSERT INTO traceability_rs.dbo.labelscrap
                    (LabelCode, IDLabelCode, ScrapDate, LabelScrapReasonId, Category,
                     Operator, Shift, Hostname)
                OUTPUT INSERTED.LabelScrapId
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, id_label, scrap_date, reason_id, category,
                  self.operator, current_shift(), socket.gethostname()))
            new_id = cur.fetchone()[0]
            self.db.conn.commit()
            cur.close()
        except Exception as e:
            logger.error(f"Insert labelscrap: {e}", exc_info=True)
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return

        now_s = datetime.now().strftime('%H:%M:%S')
        self._session_rows.append({'id': new_id, 'label': code, 'reason': reason_txt,
                                   'category': category, 'time': now_s})
        self.tree.insert('', 'end', values=(len(self._session_rows), code, reason_txt,
                                            L('lsc_cat_' + category.lower(), category), now_s))
        self.tree.yview_moveto(1.0)
        self.scan_entry.delete(0, tk.END)
        self.scan_entry.focus_set()
        self._refresh_counters()

    def _undo_last(self):
        if not self._session_rows:
            return
        L = self.lang.get
        row = self._session_rows[-1]
        if not messagebox.askyesno(L('confirm', 'Conferma'),
                                   L('lsc_undo_confirm', 'Annullare l\'ultima scansione ({0})?').format(row['label']),
                                   parent=self):
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute("DELETE FROM traceability_rs.dbo.labelscrap WHERE LabelScrapId = ?", (row['id'],))
            self.db.conn.commit()
            cur.close()
        except Exception as e:
            logger.error(f"Undo labelscrap: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self._session_rows.pop()
        kids = self.tree.get_children()
        if kids:
            self.tree.delete(kids[-1])
        self._refresh_counters()

    def _refresh_counters(self):
        self._cnt_vars['session'].set(str(len(self._session_rows)))
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT
                  (SELECT COUNT(*) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())
                     AND DATEPART(ISO_WEEK, ScrapDate)=DATEPART(ISO_WEEK, GETDATE())) AS wk,
                  (SELECT COUNT(*) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())
                     AND MONTH(ScrapDate)=MONTH(GETDATE())) AS mo,
                  (SELECT COUNT(*) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())) AS yr,
                  (SELECT COUNT(*) FROM traceability_rs.dbo.labelscrap) AS gen
            """, (self.operator, self.operator, self.operator))
            r = cur.fetchone()
            cur.close()
            self._cnt_vars['week'].set(str(r.wk))
            self._cnt_vars['month'].set(str(r.mo))
            self._cnt_vars['year'].set(str(r.yr))
            self._cnt_vars['general'].set(str(r.gen))
        except Exception as e:
            logger.error(f"Refresh counters: {e}", exc_info=True)

    # ── Chiusura + stampa ─────────────────────────────────────────────────
    def _close(self, print_it=None):
        L = self.lang.get
        if self._session_rows and print_it is None:
            ans = messagebox.askyesnocancel(
                L('lsc_print_q_title', 'Stampa riepilogo'),
                L('lsc_print_q', 'Vuoi stampare il riepilogo della dichiarazione?'),
                parent=self)
            if ans is None:
                return  # annulla chiusura
            print_it = bool(ans)
        if print_it and self._session_rows:
            self._print_summary()
        self.destroy()

    def _print_summary(self):
        L = self.lang.get
        try:
            import label_scrap_pdf
            fd, path = tempfile.mkstemp(
                suffix='.pdf', prefix=f'ScartiEtichette_{self.operator[:20]}_')
            os.close(fd)
            label_scrap_pdf.generate_declaration_pdf(
                path, self.operator, self._get_date(), self._session_rows)
            label_scrap_pdf.print_pdf(path)
            # Segna come stampate le righe della sessione
            ids = [r['id'] for r in self._session_rows]
            if ids:
                cur = self.db.conn.cursor()
                ph = ','.join(['?'] * len(ids))
                cur.execute(f"UPDATE traceability_rs.dbo.labelscrap SET Printed=GETDATE() "
                            f"WHERE LabelScrapId IN ({ph})", ids)
                self.db.conn.commit()
                cur.close()
        except Exception as e:
            logger.error(f"Stampa riepilogo: {e}", exc_info=True)
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   f"{L('lsc_print_err', 'Impossibile stampare il riepilogo')}: {e}",
                                   parent=self)

    def _open_reasons_manager(self):
        """Gestione motivi: richiede autorizzazione (chiave 'aggiungi_motivo_label_scrap').
        Il login modale è gestito dall'app padre; rilasciamo/riprendiamo il grab
        come per le altre azioni autorizzate in-form."""
        app = self.master

        def cb():
            w = LabelScrapReasonsManager(self, self.db, self.lang, on_done=self._load_reasons)
            self.wait_window(w)  # modale: il grab torna alla form solo alla chiusura

        if not hasattr(app, '_execute_authorized_action'):
            cb()
            return
        try:
            self.grab_release()
        except Exception:
            pass
        try:
            app._execute_authorized_action('aggiungi_motivo_label_scrap', cb)
        finally:
            try:
                self.grab_set()
            except Exception:
                pass


class LabelScrapReasonsManager(tk.Toplevel):
    """Gestione motivi scarto etichette (dbo.LabelScrapReasons)."""

    def __init__(self, master, db, lang, on_done=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.on_done = on_done
        L = self.lang.get
        self.title(L('lsc_reasons_title', 'Motivi scarto etichette'))
        self.geometry('520x420')
        self.transient(master)
        self.grab_set()
        self._build()
        self._load()

    def _build(self):
        L = self.lang.get
        top = ttk.Frame(self, padding=8)
        top.pack(fill=tk.X)
        self.entry = ttk.Entry(top, width=40)
        self.entry.pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text=L('lsc_add', 'Aggiungi'), command=self._add).pack(side=tk.LEFT, padx=4)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.tree = ttk.Treeview(wrap, columns=('id', 'reason', 'active'), show='headings')
        for c, t, w in (('id', 'ID', 50), ('reason', L('lsc_reason', 'Motivo'), 320),
                        ('active', L('lsc_active', 'Attivo'), 70)):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor='center' if c != 'reason' else 'w')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(bar, text=L('lsc_toggle', 'Attiva/Disattiva'),
                   command=self._toggle).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=self._done).pack(side=tk.RIGHT, padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT LabelScrapReasonId, Reason, IsActive FROM traceability_rs.dbo.LabelScrapReasons "
                        "ORDER BY Reason")
            for r in cur.fetchall():
                self.tree.insert('', 'end', iid=str(r.LabelScrapReasonId),
                                 values=(r.LabelScrapReasonId, r.Reason,
                                         self.lang.get('yes', 'Sì') if r.IsActive else self.lang.get('no', 'No')))
            cur.close()
        except Exception as e:
            logger.error(f"Load reasons manager: {e}", exc_info=True)

    def _add(self):
        L = self.lang.get
        txt = self.entry.get().strip()
        if not txt:
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute("INSERT INTO traceability_rs.dbo.LabelScrapReasons (Reason) VALUES (?)", (txt,))
            self.db.conn.commit()
            cur.close()
        except Exception as e:
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self.entry.delete(0, tk.END)
        self._load()

    def _toggle(self):
        sel = self.tree.selection()
        if not sel:
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE traceability_rs.dbo.LabelScrapReasons SET IsActive = 1 - IsActive "
                        "WHERE LabelScrapReasonId = ?", (int(sel[0]),))
            self.db.conn.commit()
            cur.close()
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
            return
        self._load()

    def _done(self):
        if self.on_done:
            self.on_done()
        self.destroy()
