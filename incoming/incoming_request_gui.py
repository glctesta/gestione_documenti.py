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
    from . import incoming_email
except ImportError:  # esecuzione come script standalone
    import incoming_email

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
        self._cb_supplier.grid(row=1, column=1, sticky='w', padx=4, pady=6)
        self._cb_supplier.bind('<KeyRelease>', self._on_supplier_key)
        ttk.Button(form, text=L('inc_req_new_supplier', 'Nuovo fornitore…'),
                   command=self._open_new_supplier).grid(
            row=1, column=2, sticky='w', padx=4, pady=6)
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

        # Codice interno (componente) da abbinare all'MPN
        ttk.Label(form, text=L('inc_req_component_code', 'Codice interno (componente):')).grid(
            row=9, column=0, sticky='w', padx=6, pady=6)
        self._add_entry(form, 'component_code', row=9, col=1)

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

    def _open_new_supplier(self, initial=None):
        """Apre il dialog di inserimento rapido fornitore e seleziona il risultato.

        Il dialog verifica univocita' del codice IVA e propone i fornitori con
        nome simile prima di inserire. Se l'utente sceglie un esistente dalla
        lista delle similitudini, viene selezionato quello.
        """
        typed = (initial if initial is not None else self._v_supplier.get()).strip()
        dlg = NewSupplierDialog(self, self.db, self.lang, initial_name=typed)
        if not dlg.result:
            return
        sup = dlg.result
        if not any(s['IDSite'] == sup['id'] for s in self._suppliers):
            self._suppliers.append({'IDSite': sup['id'], 'SiteName': sup['name']})
        self._refresh_supplier_values('')
        self._v_supplier.set(f"{sup['name']} ({sup['id']})")

    # ── Dinamica campi per tipo ───────────────────────────────────────────────
    def _current_type_key(self):
        return self._type_key_by_label.get(self._v_type.get()) or 'MPN_MANCANTE'

    def _on_type_change(self):
        key = self._current_type_key()
        visible = set(_FIELDS_BY_TYPE.get(key, ())) | {'ddt_number', 'ddt_date'}
        # Il codice interno si abbina all'MPN: visibile solo per i tipi MPN.
        if key in ('MPN_MANCANTE', 'MPN_SBAGLIATO'):
            visible.add('component_code')
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
        if not sup and disp:
            # Non in elenco: offri l'inserimento rapido (con codice IVA obbligatorio)
            if messagebox.askyesno(L('inc_req_new_supplier_title', 'Inserimento nuovo fornitore'),
                                   L('inc_req_offer_new_supplier',
                                     'Il fornitore "{0}" non e'' in elenco.\nInserirlo ora?').format(disp),
                                   parent=self):
                self._open_new_supplier(initial=disp)
                sup = self._supplier_by_display.get(self._v_supplier.get().strip())
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

        # Codice interno (componente): opzionale; se mancante in
        # dbo.Components (IDCOMPONENTTYPE = 1) viene inserito silente.
        component_code = self._vars['component_code'].get().strip().upper() or None
        if component_code and key in ('MPN_MANCANTE', 'MPN_SBAGLIATO'):
            try:
                incoming_db.ensure_component(self.db, component_code)
            except Exception as e:
                logger.error(f"Incoming request: verifica componente fallita: {e}", exc_info=True)
        data['component_code'] = component_code

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
            popup_msg = L('inc_req_popup_msg',
                          '{0} — Fornitore: {1} — DDT: {2} — Da: {3}').format(
                incoming_db.type_label(L, key), data['supplier_name'],
                data.get('ddt_number') or '-', self.user_name)
            if data.get('component_code'):
                popup_msg += ' — ' + L('inc_req_popup_code', 'Codice: {0}').format(
                    data['component_code'])
            with self.db._lock:
                cur = _cursor(self.db)
                queue_popup(
                    cur,
                    target='INCOMING_RECEIVER',
                    title=L('inc_req_popup_title', 'Nuova richiesta Ricezione — {0}').format(request_number),
                    message=popup_msg,
                    order_number=request_number,
                    category='INCOMING')
                self.db.conn.commit()
        except Exception as e:
            logger.error(f"Incoming request: popup non accodato per {request_number}: {e}", exc_info=True)

        # Email di notifica ai destinatari configurati per il tipo
        try:
            req = incoming_db.get_request(self.db, request_id) or {}
            incoming_email.send_new_request_email(self.db, req)
        except Exception as e:
            logger.error(f"Incoming request: email non inviata per {request_number}: {e}", exc_info=True)

        messagebox.showinfo(L('info', 'Info'),
                            L('inc_req_sent', 'Richiesta {0} inviata.').format(request_number),
                            parent=self)
        logger.info(f"Incoming request creata: {request_number} (id={request_id}) tipo={key}")
        self._reset()


# ── Dialog inserimento rapido fornitore ───────────────────────────────────────
class NewSupplierDialog(tk.Toplevel):
    """Inserimento rapido di un fornitore non presente in anagrafica.

    Flusso: validazione campi -> verifica codice IVA gia' esistente (rifiuto)
    -> eventuale proposta di nomi simili (dialog dedicato) -> INSERT in
    dbo.Sites. Il risultato e' in self.result: {'id': IDSite, 'name': nome}
    oppure None se annullato / scelto un esistente gia' noto al chiamante
    (in quel caso result punta all'esistente, cosi' viene selezionato).
    """

    def __init__(self, master, db, lang, initial_name=""):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.result = None
        L = self.lang.get

        self.title(L('inc_req_new_supplier_title', 'Inserimento nuovo fornitore'))
        self.geometry('460x230')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        frm = ttk.Frame(self, padding=16)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text=L('inc_req_supplier_name', 'Ragione sociale:')).grid(
            row=0, column=0, sticky='w', pady=6)
        self._v_name = tk.StringVar(value=initial_name)
        ttk.Entry(frm, textvariable=self._v_name, width=40).grid(
            row=0, column=1, sticky='w', padx=6, pady=6)

        ttk.Label(frm, text=L('inc_req_supplier_vat', 'Codice IVA / P.IVA (*):')).grid(
            row=1, column=0, sticky='w', pady=6)
        self._v_vat = tk.StringVar()
        vat_entry = ttk.Entry(frm, textvariable=self._v_vat, width=25)
        vat_entry.grid(row=1, column=1, sticky='w', padx=6, pady=6)

        ttk.Label(frm, text=L('inc_req_vat_mandatory',
                              '(*) Il codice IVA e'' obbligatorio: viene verificato che non esista gia''.'),
                  font=('Segoe UI', 8), foreground='#555555', wraplength=420,
                  justify='left').grid(row=2, column=0, columnspan=2, sticky='w', pady=(2, 8))

        bar = ttk.Frame(frm)
        bar.grid(row=3, column=0, columnspan=2, sticky='e', pady=(10, 0))
        ttk.Button(bar, text=L('inc_req_save_supplier', 'Salva fornitore'),
                   command=self._on_ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Annulla'),
                   command=self.destroy).pack(side=tk.LEFT, padx=4)

        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.update_idletasks()
        vat_entry.focus_set()

    def _on_ok(self):
        L = self.lang.get
        name = self._v_name.get().strip()
        vat = self._v_vat.get().strip()
        if not name:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_name_required', 'Inserire la ragione sociale del fornitore.'),
                                parent=self)
            return
        if not vat:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_vat_required', 'Inserire il codice IVA del fornitore (obbligatorio).'),
                                parent=self)
            return
        if len(name) > 250:
            messagebox.showinfo(L('info', 'Info'),
                                L('inc_req_name_too_long', 'Ragione sociale troppo lunga (max 250 caratteri).'),
                                parent=self)
            return

        # 1. Codice IVA gia' presente -> rifiuto, mostrando i fornitori esistenti
        try:
            existing = incoming_db.find_suppliers_by_vat(self.db, vat)
        except Exception as e:
            logger.error(f"Verifica IVA fornitore fallita: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 L('inc_req_vat_check_error', 'Impossibile verificare il codice IVA:\n{0}').format(e),
                                 parent=self)
            return
        if existing:
            names = '\n'.join(f"• {r['SiteName']} (ID {r['IDSite']})" for r in existing[:10])
            messagebox.showwarning(
                L('warning', 'Attenzione'),
                L('inc_req_vat_exists',
                  'Esiste gia'' una societa'' con questo codice IVA:\n{0}\n\n'
                  'Inserimento rifiutato: selezionare la societa'' esistente.').format(names),
                parent=self)
            return

        # 2. Verifica similitudine nomi: propone eventuali fornitori esistenti
        try:
            matches = incoming_db.supplier_name_suggestions(self.db, name)
        except Exception as e:
            logger.error(f"Verifica similitudine nomi fallita: {e}", exc_info=True)
            matches = []
        if matches:
            sim = SimilarSuppliersDialog(self, self.lang, matches)
            if sim.cancelled:
                return  # l'utente chiude: resta nel dialog per correggere
            if sim.selected:
                # Usa il fornitore esistente selezionato: nessun INSERT
                self.result = {'id': sim.selected['IDSite'],
                               'name': str(sim.selected['SiteName']).strip()}
                self.destroy()
                return
            # sim.selected None + non annullato -> l'utente conferma "Inserisci nuovo"

        # 3. Inserimento
        try:
            new_id = incoming_db.create_supplier(self.db, name, vat)
        except Exception as e:
            logger.error(f"Inserimento fornitore '{name}' fallito: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 L('inc_req_supplier_save_error',
                                   'Errore durante l''inserimento del fornitore:\n{0}').format(e),
                                 parent=self)
            return
        self.result = {'id': new_id, 'name': name}
        messagebox.showinfo(L('info', 'Info'),
                            L('inc_req_supplier_created', 'Fornitore "{0}" inserito correttamente.').format(name),
                            parent=self)
        self.destroy()


class SimilarSuppliersDialog(tk.Toplevel):
    """Mostra i fornitori con nome simile a quello inserito.

    L'utente puo' selezionarne uno (selected valorizzato), confermare
    l'inserimento di un nuovo fornitore (selected=None, cancelled=False)
    oppure annullare tornando al dialog di inserimento (cancelled=True).
    """

    def __init__(self, master, lang, matches):
        super().__init__(master)
        self.lang = lang
        self.selected = None
        self.cancelled = True   # resta True finche' non si preme una delle due azioni
        L = self.lang.get

        self.title(L('inc_req_similar_title', 'Possibili fornitori esistenti'))
        self.geometry('520x300')
        self.transient(master)
        self.grab_set()

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text=L('inc_req_similar_msg',
                              'Esistono fornitori con nome simile. Verificare che non sia lo stesso '
                              'prima di inserirne uno nuovo.'),
                  wraplength=490, justify='left').pack(anchor='w', pady=(0, 8))

        wrap = ttk.Frame(frm)
        wrap.pack(fill=tk.BOTH, expand=True)
        self._list = tk.Listbox(wrap, height=8, font=('Segoe UI', 9))
        sb = ttk.Scrollbar(wrap, orient='vertical', command=self._list.yview)
        self._list.configure(yscrollcommand=sb.set)
        self._list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        for m in matches:
            self._list.insert(tk.END, f"{m['SiteName']}  (ID {m['IDSite']})")
        self._matches = matches
        if matches:
            self._list.selection_set(0)

        bar = ttk.Frame(frm)
        bar.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(bar, text=L('inc_req_similar_use', 'Usa selezionato'),
                   command=self._on_use).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('inc_req_similar_proceed', 'Inserisci nuovo'),
                   command=self._on_proceed).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text=L('btn_close', 'Annulla'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def _on_use(self):
        sel = self._list.curselection()
        if not sel:
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('inc_req_similar_pick',
                                              'Selezionare un fornitore dall''elenco.'), parent=self)
            return
        self.selected = self._matches[sel[0]]
        self.cancelled = False
        self.destroy()

    def _on_proceed(self):
        self.selected = None
        self.cancelled = False
        self.destroy()
