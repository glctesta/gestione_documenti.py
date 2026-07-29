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


# Codice usato in LabelCode per le etichette bianche, che non hanno nulla da
# scansionare. Marcatore fisso invece di NULL: LabelCode e' NOT NULL e cosi'
# le righe manuali restano riconoscibili nei report gia' esistenti.
BLANK_LABEL_CODE = 'BIANCA'


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
        self.geometry('920x760')
        self.minsize(720, 500)
        self.transient(parent)
        self._reason_map = {}
        self._build_ui()
        self._load_reasons()
        self._load_materials()   # materiali indiretti pertinenti alle etichette
        self._load_unprinted()   # dichiarazioni non ancora stampate (anche giorni precedenti)
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

        # Materiale indiretto, ristretto a quelli pertinenti alle etichette
        # (vedi _load_materials). Editabile per poter filtrare digitando,
        # senza staccarsi dallo scanner.
        ttk.Label(form, text=L('lsc_material', 'Materiale') + ':').grid(
            row=2, column=0, sticky='w', pady=4)
        self.material_combo = ttk.Combobox(form, width=48)
        self.material_combo.grid(row=2, column=1, columnspan=2, sticky='w', padx=4, pady=4)
        self.material_combo.bind('<KeyRelease>', self._on_material_typed)
        self.material_hint = ttk.Label(form, text='', foreground='gray')
        self.material_hint.grid(row=2, column=3, sticky='w', padx=4)

        ttk.Label(form, text=L('lsc_scan', 'Scansiona etichetta') + ':').grid(
            row=3, column=0, sticky='w', pady=(10, 4))
        self.scan_entry = ttk.Entry(form, width=40, font=('Consolas', 11))
        self.scan_entry.grid(row=3, column=1, columnspan=2, sticky='w', pady=(10, 4))
        self.scan_entry.bind('<Return>', self._on_scan)
        ttk.Button(form, text=L('lsc_add', 'Aggiungi'), command=self._on_scan).grid(
            row=3, column=3, sticky='w', padx=4, pady=(10, 4))

        # Etichette bianche: non hanno codice da scansionare, si dichiara la
        # sola quantita'. Pulsante separato dalla scansione di proposito, cosi'
        # un Invio a vuoto sullo scanner non puo' inserire righe per sbaglio.
        ttk.Label(form, text=L('lsc_blank', 'Etichette bianche') + ':').grid(
            row=4, column=0, sticky='w', pady=4)
        self.qty_var = tk.StringVar(value='1')
        self.qty_spin = ttk.Spinbox(form, from_=1, to=9999, width=6,
                                    textvariable=self.qty_var, justify='center')
        self.qty_spin.grid(row=4, column=1, sticky='w', padx=4, pady=4)
        ttk.Button(form, text=L('lsc_add_blank', 'Aggiungi senza scansione'),
                   command=self._on_add_blank).grid(row=4, column=2, sticky='w', padx=4, pady=4)

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
        cols = ('n', 'label', 'qty', 'material', 'reason', 'cat', 'time')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, txt, w, a in (('n', '#', 40, 'center'), ('label', L('lsc_scan', 'Etichetta'), 180, 'w'),
                             ('qty', L('lsc_qty', 'Qta'), 50, 'center'),
                             ('material', L('lsc_material', 'Materiale'), 190, 'w'),
                             ('reason', L('lsc_reason', 'Motivo'), 190, 'w'),
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
        ttk.Button(bar, text=L('lsc_manage_families', '🔗 Famiglie materiali'),
                   command=self._open_material_family_manager).pack(side=tk.LEFT, padx=4)
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

    def _load_materials(self):
        """Materiali indiretti pertinenti alle etichette.

        Filtro sulla famiglia materiali 'Labels' (ind.FamigliaMateriali.FamigliaMaterialiId = 1):
        i codici che compaiono qui sono quelli accoppiati a quella famiglia. Nuovi
        accoppiamenti si fanno dal pulsante 'Famiglie materiali' e questa query viene
        rieseguita alla chiusura di quella maschera per riflettere i cambiamenti.
        """
        L = self.lang.get
        self._materials = []      # (MaterialeId, Codice, Descrizione)
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT M.MaterialeId, M.CodiceMateriale, M.DescrizioneMateriale
                FROM ind.Materiali M
                WHERE M.IsActive = 1 AND M.FamigliaMaterialiId = 1
                ORDER BY M.DescrizioneMateriale
            """)
            self._materials = [(r.MaterialeId, r.CodiceMateriale, r.DescrizioneMateriale or '')
                               for r in cur.fetchall()]
            cur.close()
        except Exception as e:
            logger.error(f"Load materiali indiretti: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"{L('lsc_mat_load_err', 'Impossibile caricare i materiali')}: {e}",
                                 parent=self)

        self._material_display = [f"{c} - {d}" for _i, c, d in self._materials]
        self.material_combo['values'] = self._material_display
        if len(self._materials) == 1:
            self.material_combo.current(0)   # una sola scelta: la preseleziono
        self.material_hint.config(
            text=L('lsc_mat_count', '{n} materiali').format(n=len(self._materials)))
        if not self._materials:
            self.material_hint.config(
                text=L('lsc_mat_none', 'Nessun materiale accoppiato alla famiglia etichette'),
                foreground='#B00020')

    def _on_material_typed(self, event=None):
        """Filtro incrementale sulla tendina, per codice o descrizione."""
        if event is not None and event.keysym in ('Up', 'Down', 'Return', 'Escape', 'Tab'):
            return
        txt = self.material_combo.get().strip().lower()
        if not txt:
            self.material_combo['values'] = self._material_display
            return
        self.material_combo['values'] = [d for d in self._material_display
                                         if txt in d.lower()]

    def _current_material(self):
        """Materiale selezionato come (MaterialeId, Codice, Descrizione), o None.

        Non uso combo.current(): con la tendina filtrata l'indice si riferisce
        alla lista ridotta, non a self._materials. Risolvo sul testo.
        """
        txt = self.material_combo.get().strip()
        if not txt:
            return None
        for i, (mid, code, descr) in enumerate(self._materials):
            if self._material_display[i] == txt or code.lower() == txt.lower():
                return mid, code, descr
        return None

    def _load_unprinted(self):
        """Precarica nella lista le dichiarazioni dell'operatore non ancora stampate
        (Printed IS NULL), anche di giorni precedenti: così vengono incluse nel
        riepilogo e nella stampa e nulla resta in sospeso."""
        L = self.lang.get
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT ls.LabelScrapId, ls.LabelCode, r.Reason, ls.Category, ls.DateIn,
                       ls.CodiceMateriale, ls.Qty
                FROM traceability_rs.dbo.labelscrap ls
                INNER JOIN traceability_rs.dbo.LabelScrapReasons r
                    ON r.LabelScrapReasonId = ls.LabelScrapReasonId
                WHERE ls.Operator = ? AND ls.Printed IS NULL
                ORDER BY ls.DateIn
            """, (self.operator,))
            rows = cur.fetchall()
            cur.close()
        except Exception as e:
            logger.error(f"Load dichiarazioni non stampate: {e}", exc_info=True)
            return
        for r in rows:
            t = r.DateIn.strftime('%d/%m %H:%M') if r.DateIn else ''
            # Righe registrate prima dell'introduzione di materiale e quantita'
            qty = int(r.Qty or 1)
            mat = r.CodiceMateriale or ''
            self._session_rows.append({'id': r.LabelScrapId, 'label': r.LabelCode,
                                       'qty': qty, 'material': mat, 'material_descr': '',
                                       'reason': r.Reason, 'category': r.Category, 'time': t})
            self.tree.insert('', 'end', values=(
                len(self._session_rows), r.LabelCode, qty, mat, r.Reason,
                L('lsc_cat_' + (r.Category or '').lower(), r.Category), t))
        if rows:
            self.tree.yview_moveto(1.0)

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
        """Etichetta scansionata: sempre una unita'."""
        code = self.scan_entry.get().strip()
        if not code:
            return
        if self._save_scrap(code, 1):
            self.scan_entry.delete(0, tk.END)
        self.scan_entry.focus_set()

    def _on_add_blank(self):
        """Etichette bianche: nessun codice da scansionare, solo la quantita'."""
        L = self.lang.get
        try:
            qty = int(self.qty_var.get().strip())
        except ValueError:
            qty = 0
        if qty <= 0:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('lsc_qty_invalid', 'Indicare una quantita maggiore di zero.'),
                                   parent=self)
            self.qty_spin.focus_set()
            return
        if self._save_scrap(BLANK_LABEL_CODE, qty):
            self.qty_var.set('1')
        self.scan_entry.focus_set()

    def _save_scrap(self, code, qty):
        """Registra una riga di scarto. Ritorna True se salvata.

        Unico punto di INSERT: scansione e riga manuale differiscono solo per
        il codice e la quantita', quindi i controlli stanno tutti qui e non
        possono divergere fra i due percorsi.
        """
        L = self.lang.get
        reason_txt = self.reason_combo.get()
        reason_id = self._reason_map.get(reason_txt)
        if not reason_id:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('lsc_pick_reason', 'Selezionare un motivo.'), parent=self)
            return False

        mat = self._current_material()
        if not mat:
            messagebox.showwarning(
                L('warning', 'Attenzione'),
                L('lsc_pick_material', 'Selezionare il materiale indiretto.'), parent=self)
            self.material_combo.focus_set()
            return False
        mat_id, mat_code, mat_descr = mat

        category = self.category_var.get()
        scrap_date = self._get_date()
        # Le righe bianche non hanno un'etichetta da risolvere in anagrafica
        id_label = None if code == BLANK_LABEL_CODE else self._resolve_label_id(code)
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                INSERT INTO traceability_rs.dbo.labelscrap
                    (LabelCode, IDLabelCode, ScrapDate, LabelScrapReasonId, Category,
                     Operator, Shift, Hostname, MaterialeId, CodiceMateriale, Qty)
                OUTPUT INSERTED.LabelScrapId
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, id_label, scrap_date, reason_id, category,
                  self.operator, current_shift(), socket.gethostname(),
                  mat_id, mat_code, qty))
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
            return False

        now_s = datetime.now().strftime('%H:%M:%S')
        self._session_rows.append({'id': new_id, 'label': code, 'qty': qty,
                                   'material': mat_code, 'material_descr': mat_descr,
                                   'reason': reason_txt, 'category': category, 'time': now_s})
        self.tree.insert('', 'end', values=(
            len(self._session_rows), code, qty, mat_code, reason_txt,
            L('lsc_cat_' + category.lower(), category), now_s))
        self.tree.yview_moveto(1.0)
        self._refresh_counters()
        return True

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
        # I contatori sono etichette, non righe: da quando esiste Qty una riga
        # puo' valerne molte. ISNULL copre le righe storiche prima della
        # migrazione, che valgono 1 ciascuna.
        self._cnt_vars['session'].set(str(sum(r.get('qty', 1) for r in self._session_rows)))
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT
                  (SELECT ISNULL(SUM(ISNULL(Qty,1)),0) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())
                     AND DATEPART(ISO_WEEK, ScrapDate)=DATEPART(ISO_WEEK, GETDATE())) AS wk,
                  (SELECT ISNULL(SUM(ISNULL(Qty,1)),0) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())
                     AND MONTH(ScrapDate)=MONTH(GETDATE())) AS mo,
                  (SELECT ISNULL(SUM(ISNULL(Qty,1)),0) FROM traceability_rs.dbo.labelscrap
                   WHERE Operator=? AND YEAR(ScrapDate)=YEAR(GETDATE())) AS yr,
                  (SELECT ISNULL(SUM(ISNULL(Qty,1)),0) FROM traceability_rs.dbo.labelscrap) AS gen
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
            wr = label_scrap_pdf.get_warehouse_responsible(self.db.conn)
            label_scrap_pdf.generate_declaration_pdf(
                path, self.operator, self._get_date(), self._session_rows,
                warehouse_responsible=wr)
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

    def _open_material_family_manager(self):
        """Accoppiamento materiali indiretti <-> famiglie materiali.
        Stessa autorizzazione della gestione motivi (chiave 'aggiungi_motivo_label_scrap').
        Alla chiusura, se sono stati fatti accoppiamenti, ricarica i materiali della
        form cosi' i nuovi codici della famiglia etichette compaiono nella tendina."""
        app = self.master

        def cb():
            w = LabelScrapMaterialFamilyManager(self, self.db, self.lang,
                                                on_done=self._load_materials)
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


class LabelScrapMaterialFamilyManager(tk.Toplevel):
    """Accoppiamento materiali indiretti (ind.Materiali) alle famiglie materiali
    (ind.FamigliaMateriali).

    L'operatore filtra i materiali per codice o descrizione, sceglie una famiglia
    dalla tendina e accoppia i materiali selezionati (selezione multipla). Il
    campo aggiornato e' ind.Materiali.FamigliaMaterialiId. Alla chiusura, se e'
    stato fatto almeno un accoppiamento, il chiamante ricarica i materiali della
    dichiarazione scarti (on_done -> _load_materials)."""

    def __init__(self, master, db, lang, on_done=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.on_done = on_done
        self._changed = False
        self._families = {}    # nome -> id
        self._materials = []   # (id, codice, descrizione, fam_id, fam_nome)
        L = self.lang.get
        self.title(L('lsc_fam_title', 'Accoppia materiali a famiglie'))
        self.geometry('780x560')
        self.minsize(640, 440)
        self.transient(master)
        self.grab_set()
        self._build()
        self._load_families()
        self._load_materials()
        self.filter_entry.focus_set()

    def _build(self):
        L = self.lang.get
        top = ttk.Frame(self, padding=8)
        top.pack(fill=tk.X)
        ttk.Label(top, text=L('lsc_fam_filter', 'Filtro (codice o descrizione)') + ':').pack(side=tk.LEFT)
        self.filter_entry = ttk.Entry(top, width=28)
        self.filter_entry.pack(side=tk.LEFT, padx=4)
        self.filter_entry.bind('<KeyRelease>', lambda _e: self._apply_filter())

        ttk.Label(top, text=L('lsc_fam_family', 'Famiglia') + ':').pack(side=tk.LEFT, padx=(12, 2))
        self.family_combo = ttk.Combobox(top, width=22, state='readonly')
        self.family_combo.pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text=L('lsc_fam_assign', '🔗 Accoppia selezionati'),
                   command=self._assign).pack(side=tk.LEFT, padx=8)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        cols = ('code', 'descr', 'family')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='extended')
        for c, t, w, a in (('code', L('lsc_fam_code', 'Codice'), 140, 'w'),
                           ('descr', L('lsc_fam_descr', 'Descrizione'), 380, 'w'),
                           ('family', L('lsc_fam_family', 'Famiglia'), 150, 'w')):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor=a)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=8, pady=6)
        self.count_lbl = ttk.Label(bar, text='', foreground='#555')
        self.count_lbl.pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'),
                   command=self._done).pack(side=tk.RIGHT, padx=4)

    def _load_families(self):
        self._families = {}
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT FamigliaMaterialiId, Famiglia FROM ind.FamigliaMateriali ORDER BY Famiglia")
            rows = cur.fetchall()
            cur.close()
        except Exception as e:
            logger.error(f"Load famiglie materiali: {e}", exc_info=True)
            rows = []
        names = []
        for r in rows:
            self._families[r.Famiglia] = r.FamigliaMaterialiId
            names.append(r.Famiglia)
        self.family_combo['values'] = names
        if names:
            self.family_combo.current(0)

    def _load_materials(self):
        self._materials = []
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT M.MaterialeId, M.CodiceMateriale, M.DescrizioneMateriale,
                       M.FamigliaMaterialiId, F.Famiglia
                FROM ind.Materiali M
                LEFT JOIN ind.FamigliaMateriali F ON F.FamigliaMaterialiId = M.FamigliaMaterialiId
                WHERE M.IsActive = 1
                ORDER BY M.CodiceMateriale
            """)
            self._materials = [(r.MaterialeId, r.CodiceMateriale, r.DescrizioneMateriale or '',
                                r.FamigliaMaterialiId, r.Famiglia or '')
                               for r in cur.fetchall()]
            cur.close()
        except Exception as e:
            logger.error(f"Load materiali per accoppiamento: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
        self._apply_filter()

    def _apply_filter(self):
        txt = self.filter_entry.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for mid, code, descr, _fam_id, fam_name in self._materials:
            if txt and txt not in code.lower() and txt not in descr.lower():
                continue
            self.tree.insert('', 'end', iid=str(mid), values=(code, descr, fam_name))
            shown += 1
        self.count_lbl.config(
            text=self.lang.get('lsc_fam_count', '{n} materiali').format(n=shown))

    def _assign(self):
        L = self.lang.get
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(L('info', 'Info'),
                                L('lsc_fam_pick_mat', 'Selezionare almeno un materiale.'),
                                parent=self)
            return
        fam_name = self.family_combo.get()
        fam_id = self._families.get(fam_name)
        if not fam_id:
            messagebox.showinfo(L('info', 'Info'),
                                L('lsc_fam_pick_fam', 'Selezionare una famiglia.'),
                                parent=self)
            return
        try:
            cur = self.db.conn.cursor()
            for iid in sel:
                cur.execute("UPDATE ind.Materiali SET FamigliaMaterialiId = ? WHERE MaterialeId = ?",
                            (fam_id, int(iid)))
            self.db.conn.commit()
            cur.close()
        except Exception as e:
            logger.error(f"Accoppiamento materiale-famiglia: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self._changed = True
        self._load_materials()

    def _done(self):
        # on_done (ricarica materiali della form scarti) solo se qualcosa e' cambiato
        if self._changed and self.on_done:
            self.on_done()
        self.destroy()
