# -*- coding: utf-8 -*-
"""
incoming/incoming_confirm_gui.py

Finestra "Conferma soluzioni — Ricezione" (PC mittente): elenca le richieste
con risposta pronta (Status='ANSWERED') create dallo stesso utente o dallo
stesso PC (RequestedBy = user_name OR RequesterHost = hostname) e permette di
confermare la soluzione (CONFIRMED_OK) o segnalarla come non risolutiva
(CONFIRMED_KO) tramite incoming_db.confirm_request.

Il contratto incoming_db non espone un getter per le richieste ANSWERED
(filtro per utente): qui si legge direttamente Traceability_RS.dyn.IncomingRequest
con il pattern DB uniforme (funziona sia con Database di main.py sia con
BackgroundDatabase del servizio background).

Entry point: open_incoming_confirm(master, db, lang, user_name="Unknown")
"""
import socket
import tkinter as tk
from tkinter import ttk, messagebox
import logging

try:
    from . import incoming_db
except ImportError:  # esecuzione come script standalone
    import incoming_db

logger = logging.getLogger(__name__)

_REFRESH_MS = 30_000  # polling automatico lista

# Stati selezionabili nel filtro (valori Status della tabella IncomingRequest).
_STATUS_FILTERS = (
    incoming_db.STATUS_ANSWERED,
    incoming_db.STATUS_CONFIRMED_OK,
    incoming_db.STATUS_CONFIRMED_KO,
)

_Q_MY_REQUESTS = """
SELECT Id, RequestNumber, RequestType, SupplierName, DdtNumber, DdtDate, PurOrderNumber,
       MpnCode, WrongMpn, QtyToReceive, QtyExpectedPerPo, Status, RequestedBy, RequestedOn,
       RequesterHost, AnswerMpnCode, AnswerText, AnsweredBy, AnsweredOn, ConfirmedOk, ConfirmedOn
FROM Traceability_RS.dyn.IncomingRequest
WHERE Status = ? AND (RequestedBy = ? OR RequesterHost = ?)
ORDER BY AnsweredOn DESC
"""


def open_incoming_confirm(master, db, lang, user_name="Unknown"):
    """Apre la finestra di conferma delle soluzioni."""
    IncomingConfirmWindow(master, db, lang, user_name)


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


class IncomingConfirmWindow(tk.Toplevel):
    """Elenco richieste con risposta + conferma OK/KO."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        self.hostname = socket.gethostname()
        L = self.lang.get

        self.title(L('inc_conf_title', 'Conferma soluzioni — Ricezione'))
        self.geometry('1080x660')
        self.minsize(900, 560)
        self.transient(master)

        self._rows_by_iid = {}
        self._selected = None
        self._refresh_job = None

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
        tk.Label(header, text=L('inc_conf_title', 'Conferma soluzioni — Ricezione'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)
        tk.Label(header, text=f"{self.user_name} @ {self.hostname}",
                 bg='#1F3864', fg='#B4C7E7', font=('Helvetica', 9)).pack(
            side=tk.RIGHT, padx=12)

        # Filtro stato
        f = ttk.Frame(self)
        f.pack(fill=tk.X, padx=10, pady=6)
        ttk.Label(f, text=L('inc_conf_filter_status', 'Stato:')).pack(side=tk.LEFT, padx=4)
        self._v_filter = tk.StringVar()
        cb = ttk.Combobox(f, textvariable=self._v_filter, state='readonly', width=22,
                          values=_STATUS_FILTERS)
        cb.current(0)  # ANSWERED
        cb.pack(side=tk.LEFT, padx=4)
        cb.bind('<<ComboboxSelected>>', lambda ev: self._refresh())
        ttk.Button(f, text=L('inc_sol_refresh', '🔄 Aggiorna'), command=self._refresh).pack(
            side=tk.LEFT, padx=10)

        # Lista richieste
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('number', 'type', 'supplier', 'mpn', 'status', 'answered_by', 'answered_on')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, h, w, anc in (
                ('number', L('inc_col_number', 'Numero'), 150, 'w'),
                ('type', L('inc_col_type', 'Tipo'), 140, 'w'),
                ('supplier', L('inc_col_supplier', 'Fornitore'), 220, 'w'),
                ('mpn', L('inc_col_mpn', 'MPN'), 120, 'w'),
                ('status', L('inc_col_status', 'Stato'), 120, 'w'),
                ('answered_by', L('inc_col_answered_by', 'Risposta di'), 130, 'w'),
                ('answered_on', L('inc_col_answered_on', 'Risposto il'), 110, 'center')):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor=anc)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Dettaglio richiesta + risposta
        det = ttk.LabelFrame(self, text=L('inc_conf_detail', 'Dettaglio richiesta e risposta'), padding=8)
        det.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        self._v_request = tk.StringVar()
        tk.Label(det, textvariable=self._v_request, justify='left', anchor='nw',
                 font=('Courier', 9)).pack(fill=tk.X, pady=2)
        ttk.Label(det, text=L('inc_conf_answer', 'Risposta ricevuta:'),
                  font=('Helvetica', 9, 'bold')).pack(anchor='w', pady=(6, 0))
        self._txt_answer = tk.Text(det, height=5, wrap='word', state='disabled',
                                   bg='#F2F2F2', font=('Segoe UI', 9))
        self._txt_answer.pack(fill=tk.BOTH, expand=True, pady=2)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        self._btn_ok = ttk.Button(bar, text=L('inc_conf_ok', '✔ Conferma soluzione'),
                                  command=lambda: self._confirm(True), state='disabled')
        self._btn_ok.pack(side=tk.LEFT, padx=4)
        self._btn_ko = ttk.Button(bar, text=L('inc_conf_ko', '✘ Soluzione non risolutiva'),
                                  command=lambda: self._confirm(False), state='disabled')
        self._btn_ko.pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self._on_close).pack(
            side=tk.RIGHT, padx=4)

    # ── Lista ─────────────────────────────────────────────────────────────────
    def _refresh(self):
        L = self.lang.get
        if not self.winfo_exists():
            return
        status = self._v_filter.get() or incoming_db.STATUS_ANSWERED
        try:
            with self.db._lock:
                cur = _cursor(self.db)
                cur.execute(_Q_MY_REQUESTS, (status, self.user_name, self.hostname))
                cols = [d[0] for d in cur.description]
                rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Incoming confirm: lettura richieste fallita: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        self.tree.delete(*self.tree.get_children())
        self._rows_by_iid = {}
        self._selected = None
        self._btn_ok.config(state='disabled')
        self._btn_ko.config(state='disabled')
        self._v_request.set('')
        self._set_answer_text('')
        for r in rows:
            iid = str(r.get('Id'))
            self._rows_by_iid[iid] = r
            mpn = r.get('AnswerMpnCode') or r.get('WrongMpn') or r.get('MpnCode') or ''
            self.tree.insert('', 'end', iid=iid, values=(
                r.get('RequestNumber') or '',
                incoming_db.type_label(self.lang.get, r.get('RequestType')),
                r.get('SupplierName') or '',
                mpn,
                r.get('Status') or '',
                r.get('AnsweredBy') or '',
                _fmt_dt(r.get('AnsweredOn'))))

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
    def _set_answer_text(self, text):
        self._txt_answer.config(state='normal')
        self._txt_answer.delete('1.0', 'end')
        if text:
            self._txt_answer.insert('1.0', text)
        self._txt_answer.config(state='disabled')

    def _on_select(self, _ev=None):
        L = self.lang.get
        sel = self.tree.selection()
        if not sel:
            return
        r = self._rows_by_iid.get(sel[0])
        if not r:
            return
        self._selected = r
        lines = [
            f"{L('inc_col_number', 'Numero')}: {r.get('RequestNumber') or ''}   "
            f"{L('inc_col_status', 'Stato')}: {r.get('Status') or ''}",
            f"{L('inc_col_type', 'Tipo')}: {incoming_db.type_label(L, r.get('RequestType'))}",
            f"{L('inc_col_supplier', 'Fornitore')}: {r.get('SupplierName') or ''}",
            f"{L('inc_col_ddt', 'DDT')}: {r.get('DdtNumber') or ''}  {_fmt_dt(r.get('DdtDate'))}",
            f"{L('inc_req_mpn', 'Codice MPN')}: {r.get('MpnCode') or '-'}   "
            f"{L('inc_req_wrong_mpn', 'MPN errato')}: {r.get('WrongMpn') or '-'}   "
            f"{L('inc_sol_answer_mpn', 'MPN corretto')}: {r.get('AnswerMpnCode') or '-'}",
            f"{L('inc_req_po', 'P.O.')}: {r.get('PurOrderNumber') or '-'}   "
            f"{L('inc_req_qty_receive', 'Q.tà da ricevere')}: {r.get('QtyToReceive') if r.get('QtyToReceive') is not None else '-'}   "
            f"{L('inc_req_qty_expected', 'Q.tà attesa P.O.')}: {r.get('QtyExpectedPerPo') if r.get('QtyExpectedPerPo') is not None else '-'}",
            f"{L('inc_col_by', 'Richiesto da')}: {r.get('RequestedBy') or ''}  ({_fmt_dt(r.get('RequestedOn'))})   "
            f"{L('inc_col_answered_by', 'Risposta di')}: {r.get('AnsweredBy') or ''}  ({_fmt_dt(r.get('AnsweredOn'))})",
        ]
        if r.get('Status') in (incoming_db.STATUS_CONFIRMED_OK, incoming_db.STATUS_CONFIRMED_KO):
            lines.append(f"{L('inc_conf_confirmed_on', 'Confermato il')}: {_fmt_dt(r.get('ConfirmedOn'))}")
        self._v_request.set('\n'.join(lines))
        answer = r.get('AnswerText') or ''
        if r.get('AnswerMpnCode'):
            answer = f"{L('inc_sol_answer_mpn', 'MPN corretto')}: {r['AnswerMpnCode']}\n\n{answer}"
        self._set_answer_text(answer.strip())
        answered = (r.get('Status') == incoming_db.STATUS_ANSWERED)
        self._btn_ok.config(state='normal' if answered else 'disabled')
        self._btn_ko.config(state='normal' if answered else 'disabled')

    # ── Conferma ──────────────────────────────────────────────────────────────
    def _confirm(self, ok):
        L = self.lang.get
        r = self._selected
        if not r:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_sol_select', 'Seleziona una richiesta.'), parent=self)
            return
        if ok:
            msg = L('inc_conf_confirm_ok',
                    'Confermare la soluzione per {0}?').format(r.get('RequestNumber') or r.get('Id'))
        else:
            msg = L('inc_conf_confirm_ko',
                    'Segnalare la soluzione di {0} come NON risolutiva?\nLa richiesta tornerà in stato KO.')
            msg = msg.format(r.get('RequestNumber') or r.get('Id'))
        if not messagebox.askyesno(L('confirm', 'Conferma'), msg, parent=self):
            return
        try:
            done = incoming_db.confirm_request(self.db, r.get('Id'), ok, self.user_name)
        except Exception as e:
            logger.error(f"Incoming confirm: conferma fallita per {r.get('Id')}: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'), str(e), parent=self)
            return
        if not done:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('inc_conf_already_confirmed',
                                     'Richiesta già confermata da un altro operatore.'), parent=self)
        logger.info(f"Incoming request {r.get('RequestNumber')} (id={r.get('Id')}) "
                    f"confermata {'OK' if ok else 'KO'} da {self.user_name}")
        self._refresh()
