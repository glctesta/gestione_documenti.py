# -*- coding: utf-8 -*-
"""
attribuisci_cdc_gui.py

Form "Attribuisci cdc" (menu Strumenti). Permette a un capo dipartimento di
riassegnare il sotto-reparto (SubCdc) di un dipendente subordinato, mantenendo
invariati CdcId (dipartimento) e FunctionCode (funzione).

- Dal login si riceve l'EmployeeHireHistoryId del capo; Query A ne ricava CdcId e
  FunctionCode. Query B elenca i subordinati (stesso CdcId, FunctionCode < capo).
- Il salvataggio storicizza in employee.dbo.EmployeeCdcStories: chiude la storia
  attiva (DateOut=GETDATE()) e inserisce una nuova riga col nuovo SubCdc (stesso
  FunctionId, DateIn=GETDATE()).
- Dopo il commit invia una email: TO = WorkEmail del capo, CC = destinatari da
  settings 'cambio_subcdc'.

Spec: docs/AttribuisciCdc_Spec_v1.0.md
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger("TraceabilityRS")

CC_SETTING = 'cambio_subcdc'


def open_attribuisci_cdc(master, db, lang, head_ehh, user_name):
    """Entry point. head_ehh = EmployeeHireHistoryId del capo (dal login)."""
    AttribuisciCdcWindow(master, db, lang, head_ehh, user_name)


# ── DB helpers ──────────────────────────────────────────────────────────────
def _fetch(db, sql, params=None):
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    return [dict(zip(cols, r)) for r in rows]


_Q_HEAD = """
SELECT cs.CdcId, cc.CdcDescription, ec.SubCdcId, cs.SubCdcDescription, f.FunctionCode
FROM employee.dbo.EmployeeHireHistory h
INNER JOIN employee.dbo.EmployeeCdcStories ec ON ec.EmployeeHireHistoryId = h.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
INNER JOIN employee.dbo.CdcSub cs      ON ec.SubCdcId = cs.SubCdcId
INNER JOIN employee.dbo.CostCenters cc ON cs.CdcId    = cc.CdcId
INNER JOIN employee.dbo.Functions f    ON ec.FunctionId = f.FunctionId
WHERE h.EmployeerId = 2 AND h.EndWorkDate IS NULL
  AND h.EmployeeHireHistoryId = ?
"""

_Q_HEAD_EMAIL = """
SELECT a.WorkEmail FROM employee.dbo.EmployeeHireHistory h
INNER JOIN employee.dbo.EmployeeAddress a ON a.EmployeeId = h.EmployeeId AND a.DateOut IS NULL
WHERE h.EmployeeHireHistoryId = ?
"""

# FunctionCode del "super responsabile" che vede TUTTI i dipendenti attivi senza restrizioni.
SUPER_FUNCTION_CODE = 100

_Q_SUBCDC = ("SELECT SubCdcId, SubCdcDescription FROM employee.dbo.CdcSub "
             "WHERE CdcId = ? ORDER BY SubCdcDescription")

_Q_SUBCDC_ALL = ("SELECT SubCdcId, SubCdcDescription FROM employee.dbo.CdcSub "
                 "ORDER BY SubCdcDescription")

# Base senza WHERE: le condizioni sono aggiunte da _search (dipende da is_super).
_Q_SUBORDINATES_BASE = """
SELECT UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Employee,
       h.EmployeeHireHistoryId, ec.EmployeeCdcStoryId,
       c.CdcId, c.CdcDescription, cs.SubCdcId, cs.SubCdcDescription,
       f.FunctionId, f.FunctionCode, f.FunctionDescription
FROM employee.dbo.Employees e
INNER JOIN employee.dbo.EmployeeHireHistory h ON e.EmployeeId = h.EmployeeId
       AND h.EndWorkDate IS NULL AND h.EmployeerId = 2
INNER JOIN employee.dbo.EmployeeCdcStories ec ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
INNER JOIN employee.dbo.CdcSub cs      ON ec.SubCdcId = cs.SubCdcId
INNER JOIN employee.dbo.CostCenters c  ON c.CdcId = cs.CdcId
INNER JOIN employee.dbo.Functions f    ON ec.FunctionId = f.FunctionId
"""

_Q_SUBORDINATES_ORDER = " ORDER BY UPPER(e.EmployeeSurname + ' ' + e.EmployeeName)"


class AttribuisciCdcWindow(tk.Toplevel):
    def __init__(self, master, db, lang, head_ehh, user_name):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.head_ehh = head_ehh
        self.user_name = user_name or 'Unknown'
        L = self.lang.get

        self.title(L('acdc_title', 'Attribuisci CDC'))
        self.geometry('1040x620')
        self.minsize(880, 500)
        self.transient(master)

        # Dati del capo (Query A) — con A2 confermato: una sola storia attiva
        head = _fetch(db, _Q_HEAD, (head_ehh,))
        if not head:
            messagebox.showerror(
                L('error', 'Errore'),
                L('acdc_no_head_story',
                  'Impossibile determinare reparto/funzione del responsabile loggato.'),
                parent=master)
            self.destroy()
            return
        self.head = head[0]
        self.head_cdc_id = self.head['CdcId']
        self.head_fcode = self.head['FunctionCode']
        try:
            em = _fetch(db, _Q_HEAD_EMAIL, (head_ehh,))
            self.head_email = (em[0]['WorkEmail'] or '').strip() if em else None
        except Exception:
            self.head_email = None

        # FunctionCode 100 = vede TUTTI i dipendenti attivi, senza filtro di reparto/subordinazione.
        self.is_super = (self.head_fcode == SUPER_FUNCTION_CODE)
        # Opzioni per il filtro sotto-reparto: tutte se super, altrimenti quelle del reparto del capo.
        self.filter_subcdc_options = _fetch(db, _Q_SUBCDC_ALL) if self.is_super \
            else _fetch(db, _Q_SUBCDC, (self.head_cdc_id,))
        self._subcdc_cache = {}          # CdcId -> [SubCdc...] per la combo "nuovo sotto-reparto"
        self._current_new_options = []   # opzioni combo per il dipendente selezionato

        self._rows_by_id = {}
        self._selected = None
        self._build_ui()
        self.grab_set()
        self._search()

    # ── UI ──
    def _build_ui(self):
        L = self.lang.get
        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('acdc_title', 'Attribuisci CDC'), bg='#1F3864', fg='white',
                 font=('Helvetica', 13, 'bold')).pack(side=tk.LEFT, padx=12, pady=10)
        dept = (L('acdc_all_departments', 'Tutti i reparti') if self.is_super
                else (self.head.get('CdcDescription') or self.head_cdc_id))
        tk.Label(self, anchor='w', fg='#1F3864', font=('Helvetica', 9, 'bold'),
                 text=L('acdc_dept_info', 'Reparto: {0}   —   Responsabile: {1}').format(
                     dept, self.user_name)
                 ).pack(fill=tk.X, padx=12, pady=(6, 0))

        # Filtri
        f = ttk.LabelFrame(self, text=L('acdc_filters', 'Filtri'))
        f.pack(fill=tk.X, padx=10, pady=6)
        ttk.Label(f, text=L('acdc_filter_name', 'Cognome / Nome:')).grid(row=0, column=0, sticky='w', padx=6, pady=6)
        self._v_name = tk.StringVar()
        e = ttk.Entry(f, textvariable=self._v_name, width=28)
        e.grid(row=0, column=1, padx=4, pady=6)
        e.bind('<Return>', lambda ev: self._search())
        ttk.Label(f, text=L('acdc_filter_subcdc', 'Sotto-reparto:')).grid(row=0, column=2, sticky='w', padx=6, pady=6)
        self._v_subf = tk.StringVar()
        self._cb_subf = ttk.Combobox(f, textvariable=self._v_subf, width=30, state='readonly',
                                     values=[''] + [s['SubCdcDescription'] for s in self.filter_subcdc_options])
        self._cb_subf.current(0)
        self._cb_subf.grid(row=0, column=3, padx=4, pady=6)
        ttk.Button(f, text=L('acdc_search', '🔍 Cerca'), command=self._search).grid(
            row=0, column=4, padx=12, pady=6)

        # Lista subordinati
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('emp', 'subcdc', 'func', 'fcode')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, h, w, anc in (
                ('emp', L('acdc_col_employee', 'Dipendente'), 300, 'w'),
                ('subcdc', L('acdc_col_subcdc', 'Sotto-reparto attuale'), 260, 'w'),
                ('func', L('acdc_col_function', 'Funzione'), 240, 'w'),
                ('fcode', L('acdc_col_fcode', 'Cod.Funz.'), 90, 'center')):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor=anc)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Pannello riassegnazione
        ed = ttk.LabelFrame(self, text=L('acdc_reassign', 'Riassegnazione sotto-reparto'))
        ed.pack(fill=tk.X, padx=10, pady=4)
        ttk.Label(ed, text=L('acdc_current_cdc', 'Reparto (non modificabile):')).grid(
            row=0, column=0, sticky='w', padx=6, pady=4)
        self._v_cur_cdc = tk.StringVar()
        ttk.Label(ed, textvariable=self._v_cur_cdc, font=('Helvetica', 9, 'bold')).grid(
            row=0, column=1, sticky='w', padx=4, pady=4)
        ttk.Label(ed, text=L('acdc_current_function', 'Funzione (non modificabile):')).grid(
            row=0, column=2, sticky='w', padx=6, pady=4)
        self._v_cur_fun = tk.StringVar()
        ttk.Label(ed, textvariable=self._v_cur_fun, font=('Helvetica', 9, 'bold')).grid(
            row=0, column=3, sticky='w', padx=4, pady=4)
        ttk.Label(ed, text=L('acdc_new_subcdc', 'Nuovo sotto-reparto:')).grid(
            row=1, column=0, sticky='w', padx=6, pady=6)
        self._v_new_sub = tk.StringVar()
        self._cb_new_sub = ttk.Combobox(ed, textvariable=self._v_new_sub, width=40, state='readonly')
        self._cb_new_sub.grid(row=1, column=1, columnspan=2, sticky='w', padx=4, pady=6)
        self._btn_save = ttk.Button(ed, text=L('acdc_btn_save', '💾 Salva riassegnazione'),
                                    command=self._save, state='disabled')
        self._btn_save.grid(row=1, column=3, padx=12, pady=6)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT, padx=4)

    # ── Ricerca ──
    def _search(self):
        name = self._v_name.get().strip()
        name_like = f"%{name.upper()}%" if name else None
        subf = self._v_subf.get().strip() or None
        conds, params = [], []
        if not self.is_super:
            # restrizione: solo il reparto del capo e i subordinati (FunctionCode < capo)
            conds.append("c.CdcId = ? AND f.FunctionCode < ?")
            params += [self.head_cdc_id, self.head_fcode]
        conds.append("(? IS NULL OR cs.SubCdcDescription = ?)")
        params += [subf, subf]
        conds.append("(? IS NULL OR UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) LIKE ?)")
        params += [name_like, name_like]
        sql = _Q_SUBORDINATES_BASE + " WHERE " + " AND ".join(conds) + _Q_SUBORDINATES_ORDER
        try:
            rows = _fetch(self.db, sql, tuple(params))
        except Exception as e:
            logger.error(f"Attribuisci CDC ricerca: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
            return
        self.tree.delete(*self.tree.get_children())
        self._rows_by_id = {}
        self._selected = None
        self._btn_save.config(state='disabled')
        self._v_cur_cdc.set('')
        self._v_cur_fun.set('')
        for r in rows:
            iid = str(r['EmployeeCdcStoryId'])
            self._rows_by_id[iid] = r
            self.tree.insert('', 'end', iid=iid, values=(
                r['Employee'], r['SubCdcDescription'], r['FunctionDescription'], r['FunctionCode']))

    def _on_select(self, _e=None):
        sel = self.tree.selection()
        if not sel:
            return
        r = self._rows_by_id.get(sel[0])
        if not r:
            return
        self._selected = r
        self._v_cur_cdc.set(f"{r['CdcDescription']} ({r['CdcId']})")
        self._v_cur_fun.set(f"{r['FunctionDescription']} ({r['FunctionCode']})")
        # Combo "nuovo sotto-reparto" ristretta al CdcId DEL DIPENDENTE (CdcId non modificabile).
        self._current_new_options = self._subcdc_options_for(r['CdcId'])
        self._cb_new_sub['values'] = [s['SubCdcDescription'] for s in self._current_new_options]
        self._v_new_sub.set(r['SubCdcDescription'] or '')   # preseleziona l'attuale
        self._btn_save.config(state='normal')

    def _subcdc_options_for(self, cdc_id):
        if cdc_id not in self._subcdc_cache:
            self._subcdc_cache[cdc_id] = _fetch(self.db, _Q_SUBCDC, (cdc_id,))
        return self._subcdc_cache[cdc_id]

    def _subcdc_id_by_desc(self, desc):
        for s in self._current_new_options:
            if s['SubCdcDescription'] == desc:
                return s['SubCdcId']
        return None

    # ── Salvataggio ──
    def _save(self):
        L = self.lang.get
        r = self._selected
        if not r:
            messagebox.showinfo(L('info', 'Info'), L('acdc_select_employee', 'Seleziona un dipendente.'), parent=self)
            return
        new_desc = self._v_new_sub.get().strip()
        new_sub_id = self._subcdc_id_by_desc(new_desc)
        if not new_sub_id:
            messagebox.showinfo(L('info', 'Info'),
                                L('acdc_select_new_subcdc', 'Seleziona il nuovo sotto-reparto.'), parent=self)
            return
        if new_sub_id == r['SubCdcId']:
            messagebox.showinfo(L('info', 'Info'),
                                L('acdc_no_change', 'Il sotto-reparto selezionato è già quello attuale.'), parent=self)
            return
        if not messagebox.askyesno(
                L('confirm', 'Conferma'),
                L('acdc_confirm', 'Spostare {0}\nda "{1}" a "{2}"?').format(
                    r['Employee'], r['SubCdcDescription'], new_desc), parent=self):
            return

        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                cur.execute(
                    "UPDATE employee.dbo.EmployeeCdcStories SET DateOut = GETDATE() "
                    "WHERE EmployeeCdcStoryId = ? AND DateOut IS NULL",
                    (r['EmployeeCdcStoryId'],))
                if cur.rowcount != 1:
                    self.db.conn.rollback()
                    messagebox.showwarning(L('warning', 'Attenzione'),
                                           L('acdc_save_conflict',
                                             'La posizione è cambiata nel frattempo. Aggiorna e riprova.'),
                                           parent=self)
                    self._search()
                    return
                cur.execute(
                    "INSERT INTO employee.dbo.EmployeeCdcStories "
                    "(EmployeeHireHistoryId, SubCdcId, FunctionId, DateIn) VALUES (?, ?, ?, GETDATE())",
                    (r['EmployeeHireHistoryId'], new_sub_id, r['FunctionId']))
                self.db.conn.commit()
            logger.info("Attribuisci CDC: EHH=%s da SubCdc %s a %s (FunctionId=%s) da %s",
                        r['EmployeeHireHistoryId'], r['SubCdcId'], new_sub_id, r['FunctionId'], self.user_name)
        except Exception as e:
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            logger.error(f"Attribuisci CDC salvataggio: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return

        self._send_email(r, new_desc, new_sub_id)
        messagebox.showinfo(L('info', 'Info'), L('acdc_saved', 'Riassegnazione salvata.'), parent=self)
        self._search()

    def _send_email(self, r, new_desc, new_sub_id):
        L = self.lang.get
        try:
            import utils
            cc = []
            try:
                cc = utils.get_email_recipients(self.db.conn, CC_SETTING)
            except Exception as e:
                logger.warning(f"Attribuisci CDC: destinatari CC '{CC_SETTING}' non recuperati: {e}")
            if not self.head_email:
                logger.warning("Attribuisci CDC: WorkEmail del responsabile assente, email non inviata.")
                messagebox.showwarning(L('warning', 'Attenzione'),
                                       L('acdc_email_no_to',
                                         'Modifica salvata, ma manca la tua email aziendale: notifica non inviata.'),
                                       parent=self)
                return
            subject = f"[Attribuisci CDC] {r['Employee']} — cambio sotto-reparto"
            body = f"""
            <div style="font-family:Segoe UI,Arial,sans-serif;font-size:13px;color:#333">
              <p>È stata registrata una riassegnazione di sotto-reparto.</p>
              <table style="border-collapse:collapse">
                <tr><td style="padding:3px 10px;color:#666">Dipendente</td><td style="padding:3px 10px"><b>{r['Employee']}</b></td></tr>
                <tr><td style="padding:3px 10px;color:#666">Reparto</td><td style="padding:3px 10px">{r['CdcDescription']} ({r['CdcId']})</td></tr>
                <tr><td style="padding:3px 10px;color:#666">Funzione</td><td style="padding:3px 10px">{r['FunctionDescription']} ({r['FunctionCode']})</td></tr>
                <tr><td style="padding:3px 10px;color:#666">Da sotto-reparto</td><td style="padding:3px 10px">{r['SubCdcDescription']}</td></tr>
                <tr><td style="padding:3px 10px;color:#666">A sotto-reparto</td><td style="padding:3px 10px"><b>{new_desc}</b></td></tr>
                <tr><td style="padding:3px 10px;color:#666">Eseguito da</td><td style="padding:3px 10px">{self.user_name}</td></tr>
              </table>
              <p style="font-size:11px;color:#888">Email automatica — Traceability RS.</p>
            </div>"""
            utils.send_email([self.head_email], subject, body, is_html=True,
                             cc_emails=cc or None)
            logger.info("Attribuisci CDC: email inviata a %s (CC %d)", self.head_email, len(cc))
        except Exception as e:
            logger.error(f"Attribuisci CDC invio email: {e}", exc_info=True)
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('acdc_email_error',
                                     'Modifica salvata, ma invio email non riuscito:\n{0}').format(e),
                                   parent=self)
