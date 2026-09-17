# -*- coding: utf-8 -*-
"""
incoming/incoming_solutions_gui.py

Finestra "Soluzioni Ricezione" (PC receiver): elenca le richieste PENDING,
permette di inserire la soluzione (MPN corretto + testo) e di inviarla.

Dopo incoming_db.answer_request viene accodato un popup per il PC che ha
generato la richiesta (target=RequesterHost, category='INCOMING_ANSWER',
order_number=str(RequestId)) così il mittente viene avvisato in tempo reale.

Entry point: open_incoming_solutions(master, db, lang, user_name="Unknown")
"""
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import logging

from kit_notifications import queue_popup

try:
    from . import incoming_db
except ImportError:  # esecuzione come script standalone
    import incoming_db

logger = logging.getLogger(__name__)

_REFRESH_MS = 30_000  # polling automatico lista richieste


def open_incoming_solutions(master, db, lang, user_name="Unknown"):
    """Apre la finestra di gestione delle soluzioni."""
    IncomingSolutionsWindow(master, db, lang, user_name)


def _cursor(db):
    """Cursore uniforme: funziona con Database di main.py e BackgroundDatabase."""
    if hasattr(db, '_ensure_connection'):
        try:
            db._ensure_connection()
        except Exception:
            pass
    return db.cursor


def _fmt_dt(value):
    """Formatta un datetime/pyodbc date in 'DD/MM/YYYY HH:MM'."""
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    try:
        return value.strftime('%d/%m/%Y %H:%M')
    except AttributeError:
        return str(value)


def _age_minutes(requested_on):
    if requested_on is None:
        return None
    if isinstance(requested_on, str):
        try:
            requested_on = datetime.strptime(requested_on[:19], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    try:
        return int((datetime.now() - requested_on).total_seconds() // 60)
    except TypeError:
        return None


class IncomingSolutionsWindow(tk.Toplevel):
    """Elenco richieste pending + inserimento soluzione."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        L = self.lang.get

        self.title(L('inc_sol_title', 'Soluzioni — Ricezione'))
        self.geometry('1080x640')
        self.minsize(900, 540)
        self.transient(master)

        self._rows_by_iid = {}
        self._selected = None
        self._refresh_job = None
        self._type_key_by_label = {
            incoming_db.type_label(L, k): k for k in incoming_db.REQUEST_TYPES}

        self._build_ui()
        self.grab_set()
        self._refresh()
        self._schedule_refresh()
        self.protocol('WM_DELETE_WINDOW', self._on_close)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        L = self.lang.get

        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('inc_sol_title', 'Soluzioni — Ricezione'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)

        # Filtro tipo
        f = ttk.Frame(self)
        f.pack(fill=tk.X, padx=10, pady=6)
        ttk.Label(f, text=L('inc_sol_filter_type', 'Tipo:')).pack(side=tk.LEFT, padx=4)
        self._v_filter = tk.StringVar()
        cb = ttk.Combobox(f, textvariable=self._v_filter, state='readonly', width=28,
                          values=[L('inc_sol_all_types', '(tutti)')] + list(self._type_key_by_label.keys()))
        cb.current(0)
        cb.pack(side=tk.LEFT, padx=4)
        cb.bind('<<ComboboxSelected>>', lambda ev: self._refresh())
        ttk.Button(f, text=L('inc_sol_refresh', '🔄 Aggiorna'), command=self._refresh).pack(
            side=tk.LEFT, padx=10)

        # Lista richieste
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('number', 'type', 'supplier', 'ddt', 'mpn', 'po', 'qty', 'by', 'age')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, h, w, anc in (
                ('number', L('inc_col_number', 'Numero'), 150, 'w'),
                ('type', L('inc_col_type', 'Tipo'), 130, 'w'),
                ('supplier', L('inc_col_supplier', 'Fornitore'), 200, 'w'),
                ('ddt', L('inc_col_ddt', 'DDT'), 110, 'w'),
                ('mpn', L('inc_col_mpn', 'MPN'), 110, 'w'),
                ('po', L('inc_col_po', 'P.O.'), 110, 'w'),
                ('qty', L('inc_col_qty', 'Q.tà'), 70, 'e'),
                ('by', L('inc_col_by', 'Richiesto da'), 130, 'w'),
                ('age', L('inc_col_age', 'Età (min)'), 80, 'e')):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor=anc)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Dettaglio + risposta
        det = ttk.LabelFrame(self, text=L('inc_sol_detail', 'Dettaglio richiesta e soluzione'), padding=8)
        det.pack(fill=tk.X, padx=10, pady=4)
        self._v_detail = tk.StringVar()
        tk.Label(det, textvariable=self._v_detail, justify='left', anchor='w',
                 font=('Courier', 9)).pack(fill=tk.X, pady=2)

        ans = ttk.Frame(det)
        ans.pack(fill=tk.X, pady=4)
        ttk.Label(ans, text=L('inc_sol_answer_mpn', 'MPN corretto:')).grid(
            row=0, column=0, sticky='w', padx=4, pady=4)
        self._v_answer_mpn = tk.StringVar()
        self._e_answer_mpn = ttk.Entry(ans, textvariable=self._v_answer_mpn, width=25)
        self._e_answer_mpn.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        ttk.Label(ans, text=L('inc_sol_answer_text', 'Soluzione / nota:')).grid(
            row=1, column=0, sticky='nw', padx=4, pady=4)
        self._txt_answer = tk.Text(ans, height=3, width=70, wrap='word')
        self._txt_answer.grid(row=1, column=1, columnspan=2, sticky='we', padx=4, pady=4)
        ans.columnconfigure(2, weight=1)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        self._btn_send = ttk.Button(bar, text=L('inc_sol_send', '✉ Invia risposta'),
                                    command=self._send_answer, state='disabled')
        self._btn_send.pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self._on_close).pack(
            side=tk.RIGHT, padx=4)

    # ── Lista ─────────────────────────────────────────────────────────────────
    def _filter_type_key(self):
        return self._type_key_by_label.get(self._v_filter.get())

    def _refresh(self):
        L = self.lang.get
        if not self.winfo_exists():
            return
        try:
            rows = incoming_db.get_pending_requests(self.db, self._filter_type_key())
        except Exception as e:
            logger.error(f"Incoming solutions: lettura pending fallita: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self.tree.delete(*self.tree.get_children())
        self._rows_by_iid = {}
        self._selected = None
        self._btn_send.config(state='disabled')
        self._v_detail.set('')
        for r in rows:
            iid = str(r.get('Id'))
            self._rows_by_iid[iid] = r
            mpn = r.get('WrongMpn') or r.get('MpnCode') or ''
            age = _age_minutes(r.get('RequestedOn'))
            self.tree.insert('', 'end', iid=iid, values=(
                r.get('RequestNumber') or '',
                incoming_db.type_label(L, r.get('RequestType')),
                r.get('SupplierName') or '',
                r.get('DdtNumber') or '',
                mpn,
                r.get('PurOrderNumber') or '',
                r.get('QtyToReceive') if r.get('QtyToReceive') is not None else '',
                r.get('RequestedBy') or '',
                age if age is not None else ''))
        self.title(L('inc_sol_title', 'Soluzioni — Ricezione') +
                   f"  ({len(rows)} {L('inc_sol_pending', 'in attesa')})")

    def _schedule_refresh(self):
        self._refresh_job = self.after(_REFRESH_MS, self._on_timer)

    def _on_timer(self):
        self._refresh_job = None
        if not self.winfo_exists():
            return
        self._refresh()
        self._schedule_refresh()

    def _on_close(self):
        if self._refresh_job is not None:
            try:
                self.after_cancel(self._refresh_job)
            except Exception:
                pass
            self._refresh_job = None
        self.destroy()

    # ── Selezione / dettaglio ─────────────────────────────────────────────────
    def _on_select(self, _ev=None):
        L = self.lang.get
        sel = self.tree.selection()
        if not sel:
            return
        r = self._rows_by_iid.get(sel[0])
        if not r:
            return
        self._selected = r
        self._btn_send.config(state='normal')
        lines = [
            f"{L('inc_col_number', 'Numero')}: {r.get('RequestNumber') or ''}",
            f"{L('inc_col_type', 'Tipo')}: {incoming_db.type_label(L, r.get('RequestType'))}",
            f"{L('inc_col_supplier', 'Fornitore')}: {r.get('SupplierName') or ''}",
            f"{L('inc_col_ddt', 'DDT')}: {r.get('DdtNumber') or ''}  {_fmt_dt(r.get('DdtDate'))}",
            f"{L('inc_req_mpn', 'Codice MPN')}: {r.get('MpnCode') or '-'}   "
            f"{L('inc_req_wrong_mpn', 'MPN errato')}: {r.get('WrongMpn') or '-'}",
            f"{L('inc_req_po', 'P.O.')}: {r.get('PurOrderNumber') or '-'}   "
            f"{L('inc_req_qty_receive', 'Q.tà da ricevere')}: {r.get('QtyToReceive') if r.get('QtyToReceive') is not None else '-'}   "
            f"{L('inc_req_qty_expected', 'Q.tà attesa P.O.')}: {r.get('QtyExpectedPerPo') if r.get('QtyExpectedPerPo') is not None else '-'}",
            f"{L('inc_col_by', 'Richiesto da')}: {r.get('RequestedBy') or ''} @ {r.get('RequesterHost') or ''}  "
            f"({_fmt_dt(r.get('RequestedOn'))})",
        ]
        self._v_detail.set('\n'.join(lines))
        if r.get('RequestType') in ('MPN_MANCANTE', 'MPN_SBAGLIATO'):
            self._e_answer_mpn.config(state='normal')
        else:
            self._v_answer_mpn.set('')
            self._e_answer_mpn.config(state='disabled')

    # ── Invio risposta ────────────────────────────────────────────────────────
    def _send_answer(self):
        L = self.lang.get
        r = self._selected
        if not r:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_sol_select', 'Seleziona una richiesta.'), parent=self)
            return
        rid = r.get('Id')
        mpn = self._v_answer_mpn.get().strip().upper()
        text = self._txt_answer.get('1.0', 'end').strip()
        if r.get('RequestType') in ('MPN_MANCANTE', 'MPN_SBAGLIATO') and not mpn:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_sol_mpn_required', 'Inserire il codice MPN corretto.'), parent=self)
            return
        if not text:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_sol_text_required', 'Inserire una descrizione della soluzione.'), parent=self)
            return
        if not messagebox.askyesno(L('confirm', 'Conferma'),
                                   L('inc_sol_confirm_send', 'Inviare la risposta a {0}?').format(
                                       r.get('RequestNumber') or rid), parent=self):
            return

        try:
            ok = incoming_db.answer_request(self.db, rid, mpn or None, text, self.user_name)
        except Exception as e:
            logger.error(f"Incoming solutions: risposta fallita per {rid}: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        if not ok:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('inc_sol_already_answered',
                                     'Richiesta già risolta da un altro operatore.'), parent=self)
            self._refresh()
            return

        # Popup per il PC mittente (transazione separata, dopo il commit di answer_request)
        target = (r.get('RequesterHost') or '').strip() or 'INCOMING_RECEIVER'
        try:
            with self.db._lock:
                cur = _cursor(self.db)
                queue_popup(
                    cur,
                    target=target,
                    title=L('inc_sol_popup_title', 'Risposta pronta — {0}').format(
                        r.get('RequestNumber') or rid),
                    message=L('inc_sol_popup_msg',
                              'La richiesta {0} ha una risposta da {1}.\nMPN: {2}\n{3}').format(
                        r.get('RequestNumber') or rid, self.user_name, mpn or '-', text[:300]),
                    order_number=str(rid),
                    category='INCOMING_ANSWER')
                self.db.conn.commit()
        except Exception as e:
            logger.error(f"Incoming solutions: popup risposta non accodato per {rid}: {e}",
                         exc_info=True)

        logger.info(f"Incoming request {r.get('RequestNumber')} (id={rid}) risolta da {self.user_name}")
        self._v_answer_mpn.set('')
        self._txt_answer.delete('1.0', 'end')
        self._refresh()
