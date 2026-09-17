# -*- coding: utf-8 -*-
"""
incoming/incoming_request_gui.py

Form "Nuova richiesta Ricezione" (PC mittente / WH incoming).

Permette di creare una richiesta di tipo:
  - MPN_MANCANTE   : MPN presente sul DDT ma non a sistema
  - MPN_SBAGLIATO  : MPN errato rilevato in ricezione
  - PO_MANCANTE    : numero P.O. mancante / non a sistema
  - PO_QUANTITA    : quantità in arrivo diversa da quella attesa sul P.O.

Il salvataggio avviene tramite incoming_db.create_request (numero INC-YYYYMMDD-####
transazionale); dopo il commit viene accodato un popup per i PC con ruolo
'receiver' (target='INCOMING_RECEIVER', category='INCOMING').

Entry point: open_incoming_request(master, db, lang, user_name="Unknown")
"""
import socket
import tkinter as tk
from tkinter import ttk, messagebox
import logging

from kit_notifications import queue_popup

try:
    from . import incoming_db
except ImportError:  # esecuzione come script standalone
    import incoming_db

try:
    from calendar_widget import DatePickerEntry
except ImportError:
    DatePickerEntry = None

logger = logging.getLogger(__name__)

# Campi obbligatori per ogni tipo di richiesta (fornitore e DDT sono sempre richiesti).
_FIELDS_BY_TYPE = {
    'MPN_MANCANTE': ('ddt_number', 'ddt_date', 'mpn_code'),
    'MPN_SBAGLIATO': ('ddt_number', 'ddt_date', 'wrong_mpn'),
    'PO_MANCANTE': ('ddt_number', 'ddt_date', 'pur_order_number'),
    'PO_QUANTITA': ('ddt_number', 'ddt_date', 'pur_order_number',
                    'qty_to_receive', 'qty_expected_per_po'),
}

_Q_SUPPLIERS = ("SELECT IDSite, SiteName FROM Traceability_RS.dbo.Sites "
                "WHERE IsSupplier = 1 ORDER BY SiteName")


def open_incoming_request(master, db, lang, user_name="Unknown", request_type=None):
    """Apre la finestra di creazione richiesta (tipo preselezionabile)."""
    IncomingRequestWindow(master, db, lang, user_name, request_type)


# ── DB helpers ──────────────────────────────────────────────────────────────
def _cursor(db):
    """Cursore uniforme: funziona con Database di main.py e BackgroundDatabase."""
    if hasattr(db, '_ensure_connection'):
        try:
            db._ensure_connection()
        except Exception:
            pass
    return db.cursor


def _fetch(db, sql, params=None):
    with db._lock:
        cur = _cursor(db)
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    return [dict(zip(cols, r)) for r in rows]


class IncomingRequestWindow(tk.Toplevel):
    """Form di creazione di una nuova richiesta Ricezione."""

    def __init__(self, master, db, lang, user_name="Unknown", request_type=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'Unknown'
        self.hostname = socket.gethostname()
        L = self.lang.get

        self.title(L('inc_req_title', 'Nuova richiesta — Ricezione'))
        self.geometry('760x640')
        self.minsize(680, 560)
        self.transient(master)

        # Fornitori (tutti, poi filtrati da combo)
        try:
            self._suppliers = _fetch(self.db, _Q_SUPPLIERS)
        except Exception as e:
            logger.error(f"Incoming request: lettura fornitori fallita: {e}", exc_info=True)
            self._suppliers = []
            messagebox.showerror(L('error', 'Errore'),
                                 L('inc_req_suppliers_error', 'Impossibile caricare l\'elenco fornitori.'), parent=self)
        self._supplier_by_display = {}

        self._vars = {}
        self._rows = {}          # field_name -> (label_widget, input_widget)
        self._type_key_by_label = {
            incoming_db.type_label(L, k): k for k in incoming_db.REQUEST_TYPES}
        self._build_ui()
        self.grab_set()
        if request_type in incoming_db.REQUEST_TYPES:
            self._v_type.set(incoming_db.type_label(L, request_type))
        self._on_type_change()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        L = self.lang.get

        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('inc_req_title', 'Nuova richiesta — Ricezione'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)
        tk.Label(header, text=f"{self.user_name} @ {self.hostname}",
                 bg='#1F3864', fg='#B4C7E7', font=('Helvetica', 9)).pack(
            side=tk.RIGHT, padx=12)

        form = ttk.LabelFrame(self, text=L('inc_req_data', 'Dati richiesta'), padding=8)
        form.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Tipo richiesta
        ttk.Label(form, text=L('inc_req_type', 'Tipo richiesta:')).grid(
            row=0, column=0, sticky='w', padx=6, pady=6)
        self._v_type = tk.StringVar()
        self._cb_type = ttk.Combobox(
            form, textvariable=self._v_type, state='readonly', width=40,
            values=list(self._type_key_by_label.keys()))
        self._cb_type.grid(row=0, column=1, columnspan=2, sticky='w', padx=4, pady=6)
        self._cb_type.bind('<<ComboboxSelected>>', lambda ev: self._on_type_change())

        # Fornitore (combo filtrabile)
        ttk.Label(form, text=L('inc_req_supplier', 'Fornitore:')).grid(
            row=1, column=0, sticky='w', padx=6, pady=6)
        self._v_supplier = tk.StringVar()
        self._cb_supplier = ttk.Combobox(form, textvariable=self._v_supplier, width=52)
        self._cb_supplier.grid(row=1, column=1, columnspan=2, sticky='w', padx=4, pady=6)
        self._cb_supplier.bind('<KeyRelease>', self._on_supplier_key)
        self._refresh_supplier_values('')

        # DDT numero
        ttk.Label(form, text=L('inc_req_ddt_number', 'Numero DDT:')).grid(
            row=2, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'ddt_number', row=2, col=1)

        # DDT data
        ttk.Label(form, text=L('inc_req_ddt_date', 'Data DDT:')).grid(
            row=3, column=0, sticky='w', padx=6, pady=6)
        if DatePickerEntry is not None:
            dp = DatePickerEntry(form)
            dp.grid(row=3, column=1, sticky='w', padx=4, pady=6)
            self._rows['ddt_date'] = (None, dp)
        else:
            self._add_entry(form, 'ddt_date', row=3, col=1)

        # P.O.
        ttk.Label(form, text=L('inc_req_po', 'Numero P.O.:')).grid(
            row=4, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'pur_order_number', row=4, col=1)

        # MPN (mancante)
        ttk.Label(form, text=L('inc_req_mpn', 'Codice MPN:')).grid(
            row=5, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'mpn_code', row=5, col=1)

        # MPN errato
        ttk.Label(form, text=L('inc_req_wrong_mpn', 'MPN errato rilevato:')).grid(
            row=6, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'wrong_mpn', row=6, col=1)

        # Quantità
        ttk.Label(form, text=L('inc_req_qty_receive', 'Quantità da ricevere:')).grid(
            row=7, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'qty_to_receive', row=7, col=1, width=12)

        ttk.Label(form, text=L('inc_req_qty_expected', 'Quantità attesa da P.O.:')).grid(
            row=8, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'qty_expected_per_po', row=8, col=1, width=12)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('inc_req_send', '📨 Invia richiesta'),
                   command=self._save).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('inc_req_reset', 'Azzera campi'),
                   command=self._reset).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(
            side=tk.RIGHT, padx=4)

    def _add_entry(self, parent, name, row, col, width=30):
        var = tk.StringVar()
        e = ttk.Entry(parent, textvariable=var, width=width)
        e.grid(row=row, column=col, sticky='w', padx=4, pady=6)
        lbl = parent.grid_slaves(row=row, column=0)
        self._vars[name] = var
        self._rows[name] = (lbl[0] if lbl else None, e)
        return e

    # ── Fornitore filtrabile ──────────────────────────────────────────────────
    def _refresh_supplier_values(self, filter_text):
        ft = filter_text.strip().upper()
        values = []
        self._supplier_by_display = {}
        for s in self._suppliers:
            name = (s['SiteName'] or '').strip()
            if not name:
                continue
            if ft and ft not in name.upper():
                continue
            disp = f"{name} ({s['IDSite']})"
            values.append(disp)
            self._supplier_by_display[disp] = s
        self._cb_supplier['values'] = values

    def _on_supplier_key(self, _ev=None):
        self._refresh_supplier_values(self._v_supplier.get())

    # ── Dinamica campi per tipo ───────────────────────────────────────────────
    def _current_type_key(self):
        return self._type_key_by_label.get(self._v_type.get()) or 'MPN_MANCANTE'

    def _on_type_change(self):
        key = self._current_type_key()
        visible = set(_FIELDS_BY_TYPE.get(key, ())) | {'ddt_number', 'ddt_date'}
        for name, (lbl, widget) in self._rows.items():
            if name in ('ddt_number', 'ddt_date'):
                continue  # sempre visibili
            if lbl is not None:
                if name in visible:
                    lbl.grid()
                else:
                    lbl.grid_remove()
            if name in visible:
                widget.grid()
            else:
                widget.grid_remove()

    def _reset(self):
        self._v_supplier.set('')
        self._refresh_supplier_values('')
        for var in self._vars.values():
            var.set('')

    # ── Validazione e salvataggio ─────────────────────────────────────────────
    def _parse_qty(self, name):
        raw = self._vars[name].get().strip()
        if not raw:
            return None
        try:
            val = float(raw.replace(',', '.'))
        except ValueError:
            raise ValueError(name)
        if val < 0:
            raise ValueError(name)
        return val

    def _save(self):
        L = self.lang.get
        key = self._current_type_key()
        required = _FIELDS_BY_TYPE.get(key, ())

        if not self._v_type.get():
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_select_type', 'Seleziona il tipo di richiesta.'), parent=self)
            return

        # Fornitore
        disp = self._v_supplier.get().strip()
        sup = self._supplier_by_display.get(disp)
        if not sup:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_select_supplier', 'Seleziona un fornitore dall\'elenco.'), parent=self)
            return

        data = {
            'request_type': key,
            'supplier_id': sup['IDSite'],
            'supplier_name': (sup['SiteName'] or '').strip(),
            'requested_by': self.user_name,
            'requester_host': self.hostname,
        }

        # DDT
        if 'ddt_number' in required:
            ddt = self._vars['ddt_number'].get().strip()
            if not ddt:
                messagebox.showinfo(L('info', 'Info'),
                                    L('inc_req_ddt_required', 'Inserire il numero DDT.'), parent=self)
                return
            data['ddt_number'] = ddt
        else:
            data['ddt_number'] = self._vars['ddt_number'].get().strip() or None

        ddt_widget = self._rows['ddt_date'][1]
        if DatePickerEntry is not None and hasattr(ddt_widget, 'get'):
            ddt_date = ddt_widget.get()
        else:
            ddt_date = self._vars['ddt_date'].get().strip() or None
        if 'ddt_date' in required and not ddt_date:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_ddt_date_required', 'Inserire la data DDT.'), parent=self)
            return
        data['ddt_date'] = ddt_date

        # Altri campi condizionali
        for name in ('pur_order_number', 'mpn_code', 'wrong_mpn'):
            val = self._vars[name].get().strip().upper() or None
            if name in required and not val:
                messagebox.showinfo(L('info', 'Info'),
                                    L('inc_req_field_required', 'Compilare il campo richiesto ({0}).')
                                    .format(name), parent=self)
                return
            data[name] = val

        for name in ('qty_to_receive', 'qty_expected_per_po'):
            try:
                val = self._parse_qty(name)
            except ValueError:
                messagebox.showinfo(L('info', 'Info'),
                                    L('inc_req_qty_invalid', 'Quantità non valida in {0}.').format(name),
                                    parent=self)
                return
            if name in required and val is None:
                messagebox.showinfo(L('info', 'Info'),
                                    L('inc_req_field_required', 'Compilare il campo richiesto ({0}).')
                                    .format(name), parent=self)
                return
            data[name] = val

        try:
            request_id, request_number = incoming_db.create_request(self.db, data)
        except Exception as e:
            logger.error(f"Incoming request: creazione fallita: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 L('inc_req_save_error', 'Errore durante il salvataggio della richiesta:\n{0}').format(e),
                                 parent=self)
            return

        # Popup per i PC receiver (transazione separata, dopo il commit di create_request)
        try:
            with self.db._lock:
                cur = _cursor(self.db)
                queue_popup(
                    cur,
                    target='INCOMING_RECEIVER',
                    title=L('inc_req_popup_title', 'Nuova richiesta Ricezione — {0}').format(request_number),
                    message=L('inc_req_popup_msg',
                              '{0} — Fornitore: {1} — DDT: {2} — Da: {3}').format(
                        incoming_db.type_label(L, key), data['supplier_name'],
                        data.get('ddt_number') or '-', self.user_name),
                    order_number=request_number,
                    category='INCOMING')
                self.db.conn.commit()
        except Exception as e:
            logger.error(f"Incoming request: popup non accodato per {request_number}: {e}", exc_info=True)

        messagebox.showinfo(L('info', 'Info'),
                            L('inc_req_sent', 'Richiesta {0} inviata.').format(request_number),
                            parent=self)
        logger.info(f"Incoming request creata: {request_number} (id={request_id}) tipo={key}")
        self._reset()
