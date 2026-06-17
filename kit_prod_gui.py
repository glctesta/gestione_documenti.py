"""
kit_prod_gui.py
GUI Fase 3 — Ricezione e Verifica in Produzione — Sprint 4
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.3, §9.3).

Apertura da menu con login 'verifica_kit_materiale' (la stessa chiave copre
tutte le operazioni della sezione produzione, §2.3).
- Elenco kit presi in carico dalla preformatura (e bloccati, per ri-verifica)
- Verifica ricevimento: scansione vs quantita' presa in carico PF
- Esito OK -> RECEIVED_IN_PRODUCTION; mancanze -> BLOCKED_MISSING_MATERIAL
  + Email/Popup alla preformatura
- Richiesta materiale aggiuntivo (deteriorato/perso, §5.3.3)
- Materiale ritrovato (§5.3.4): annulla la richiesta pendente verso il WH
"""
import logging
import socket
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import kit_wh_logic as whl
import kit_pf_logic as pfl
import kit_prod_logic as prl
import kit_notifications as notif

logger = logging.getLogger("PlanMonitor")

PRIORITY_BADGE = {1: '🔴 P1', 2: '🟠 P2', 3: '🟡 P3', 4: '⬜ P0'}
CHECK_EMOJI = {None: '⬜', 'OK': '🟢', 'MISMATCH': '❌'}
CHECK_TAG = {None: '', 'OK': 'ok', 'MISMATCH': 'mismatch'}


def _fmt_qty(v):
    f = float(v or 0)
    return str(int(f)) if f == int(f) else f"{f:g}"


def open_kit_prod_window(parent, db, lang, user_name, operator_id):
    return KitProdWindow(parent, db, lang, user_name, operator_id)


class KitProdWindow(tk.Toplevel):
    """Elenco kit in attesa di ricevimento in linea."""

    def __init__(self, parent, db, lang, user_name, operator_id):
        super().__init__(parent)
        self.app = parent
        self.db = db
        self.lang = lang
        self.user_name = user_name or '?'
        self.operator_id = operator_id

        self.title(lang.get('kit_prod_title', 'Produzione — Ricevimento Kit'))
        self.geometry("950x520")
        self.transient(parent)

        header = ttk.Frame(self, padding=(10, 6))
        header.pack(fill='x')
        ttk.Label(header, text=lang.get('kit_prod_header',
                                        'Kit dalla preformatura in attesa di ricevimento in linea'),
                  font=("Segoe UI", 11, "bold")).pack(side='left')
        ttk.Label(header, text=f"{lang.get('kit_operator', 'Operatore')}: {self.user_name}",
                  font=("Segoe UI", 9, "italic")).pack(side='right')

        cols = ('id', 'priority', 'orders', 'file', 'state', 'closed')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        headings = {
            'id': 'ID',
            'priority': lang.get('kit_col_priority', 'Priorità'),
            'orders': lang.get('kit_col_orders', 'Ordini'),
            'file': lang.get('kit_col_file', 'File'),
            'state': lang.get('kit_col_status', 'Stato'),
            'closed': lang.get('kit_col_closed_date', 'Chiusa il'),
        }
        widths = {'id': 50, 'priority': 80, 'orders': 290, 'file': 190,
                  'state': 110, 'closed': 130}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c],
                             anchor='w' if c in ('orders', 'file') else 'center')
        self.tree.pack(expand=True, fill='both', padx=10)
        self.tree.tag_configure('p1', background='#ffd6d6')
        self.tree.tag_configure('p2', background='#ffe8cc')
        self.tree.tag_configure('p3', background='#fff7cc')
        self.tree.tag_configure('blocked', background='#f5c6cb')
        self.tree.bind('<Double-1>', lambda e: self._open_selected())

        footer = ttk.Frame(self, padding=10)
        footer.pack(fill='x')
        ttk.Button(footer, text=lang.get('kit_prod_btn_open', 'Apri ricevimento'),
                   command=self._open_selected).pack(side='left')
        ttk.Button(footer, text=lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh).pack(side='left', padx=6)

        self._refresh()
        logger.info("KitProdWindow aperta da %s", self.user_name)

    def _refresh(self):
        cursor = self.db.conn.cursor()
        try:
            rows = prl.eligible_lists(cursor)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            prio = int(r['prio_rank'] or 4)
            blocked = bool(r['blocked'])
            tag = 'blocked' if blocked else (f'p{prio}' if prio in (1, 2, 3) else '')
            state = ('⛔ ' + self.lang.get('kit_prod_state_blocked', 'BLOCCATO')) if blocked \
                else self.lang.get('kit_prod_state_ready', 'IN PREFORMATURA')
            closed = r['closed_date'].strftime('%d/%m/%Y %H:%M') if r['closed_date'] else ''
            self.tree.insert('', 'end', values=(
                r['id'], PRIORITY_BADGE.get(prio, prio), r['orders'],
                r['file_name'], state, closed), tags=(tag,))

    def _open_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_select_list', 'Seleziona una lista di prelievo'),
                parent=self)
            return
        list_id = int(self.tree.item(sel[0])['values'][0])
        KitProdVerifyWindow(self, self.db, self.lang, self.user_name,
                            self.operator_id, list_id)


class KitProdVerifyWindow(tk.Toplevel):
    """Verifica ricevimento kit in linea (§5.3.1/5.3.2)."""

    def __init__(self, parent, db, lang, user_name, operator_id, list_id):
        super().__init__(parent)
        self.parent_win = parent
        self.db = db
        self.lang = lang
        self.user_name = user_name or '?'
        self.operator_id = operator_id
        self.list_id = list_id
        self.session_id = None
        self.finished = False

        cursor = self.db.conn.cursor()
        self.info = whl.get_list_info(cursor, list_id)
        cursor.close()

        self.title(lang.get('kit_prod_verify_title', 'Verifica Ricevimento Produzione')
                   + f" — #{list_id}")
        self.geometry("1000x660")
        self.transient(parent)

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        try:
            self._start_session()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(lang.get('error_title', 'Errore'), str(e), parent=self)
            self.destroy()
            return

        self._refresh()
        self.scan_entry.focus_set()

    # ─────────────────────────── UI ──────────────────────────────────── #

    def _build_ui(self):
        lang = self.lang
        header = ttk.Frame(self, padding=(10, 6))
        header.pack(fill='x')
        ttk.Label(header,
                  text=f"{lang.get('kit_col_orders', 'Ordini')}: {' / '.join(self.info['orders'])}",
                  font=("Segoe UI", 11, "bold")).pack(side='left')
        ttk.Label(header, text=f"{lang.get('kit_operator', 'Operatore')}: {self.user_name}",
                  font=("Segoe UI", 9, "italic")).pack(side='right')

        scan_frame = ttk.LabelFrame(self, text=lang.get('kit_prod_scan_frame',
                                                        'Scansione ricevimento'), padding=10)
        scan_frame.pack(fill='x', padx=10, pady=(0, 6))
        ttk.Label(scan_frame, text=lang.get('kit_scan_unique', 'Unique Number (Reel Code):')
                  ).grid(row=0, column=0, sticky='w')
        self.scan_var = tk.StringVar()
        self.scan_entry = ttk.Entry(scan_frame, textvariable=self.scan_var,
                                    width=28, font=("Consolas", 12))
        self.scan_entry.grid(row=0, column=1, padx=8)
        self.scan_entry.bind('<Return>', self._on_scan)

        ttk.Label(scan_frame, text=lang.get('kit_pf_qty_received', 'Quantità ricevuta:')
                  ).grid(row=0, column=2, sticky='w', padx=(16, 0))
        self.qty_var = tk.StringVar()
        self.qty_entry = ttk.Entry(scan_frame, textvariable=self.qty_var,
                                   width=10, font=("Consolas", 12))
        self.qty_entry.grid(row=0, column=3, padx=8)
        self.qty_entry.bind('<Return>', self._on_confirm)
        ttk.Button(scan_frame, text=lang.get('kit_btn_confirm', 'Conferma'),
                   command=self._on_confirm).grid(row=0, column=4, padx=8)

        self.alert_var = tk.StringVar()
        ttk.Label(scan_frame, textvariable=self.alert_var, foreground='red',
                  font=("Segoe UI", 10, "bold")).grid(row=1, column=0, columnspan=5,
                                                      sticky='w', pady=(6, 0))

        cols = ('status', 'material', 'unique', 'expected', 'received')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        headings = {
            'status': lang.get('kit_col_state', 'Stato'),
            'material': lang.get('kit_col_material', 'Codice Materiale'),
            'unique': 'Unique Nr',
            'expected': lang.get('kit_prod_col_expected', 'Da preformatura'),
            'received': lang.get('kit_pf_col_received', 'Ricevuta'),
        }
        widths = {'status': 60, 'material': 280, 'unique': 160,
                  'expected': 120, 'received': 110}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c],
                             anchor='w' if c == 'material' else 'center')
        self.tree.pack(expand=True, fill='both', padx=10)
        self.tree.tag_configure('ok', background='#d8f5d8')
        self.tree.tag_configure('mismatch', background='#ffd6d6')

        footer = ttk.Frame(self, padding=10)
        footer.pack(fill='x')
        self.summary_var = tk.StringVar()
        ttk.Label(footer, textvariable=self.summary_var).pack(side='left')

        self.btn_fail = ttk.Button(
            footer, text=lang.get('kit_prod_btn_fail', 'Segnala Mancanze (Blocca)'),
            command=self._finalize_fail)
        self.btn_fail.pack(side='right', padx=4)
        self.btn_ok = ttk.Button(
            footer, text=lang.get('kit_prod_btn_ok', 'Conferma Ricevimento OK'),
            command=self._finalize_ok)
        self.btn_ok.pack(side='right', padx=4)
        ttk.Button(footer, text=lang.get('kit_btn_suspend', 'Sospendi Sessione'),
                   command=self._suspend).pack(side='right', padx=4)
        ttk.Button(footer, text=lang.get('kit_prod_btn_found', 'Materiale Ritrovato'),
                   command=self._material_found).pack(side='right', padx=12)
        ttk.Button(footer, text=lang.get('kit_pf_btn_request', 'Richiedi Materiale'),
                   command=self._request_material).pack(side='right')

    # ─────────────────────── Sessione (fase PROD) ────────────────────── #

    def _start_session(self):
        cursor = self.db.conn.cursor()
        lbl = whl.orders_label(self.info['orders'])
        session = whl.find_open_session(cursor, self.list_id, phase=prl.PHASE_PROD)
        if session:
            started = session['started_date'].strftime('%d/%m/%Y %H:%M') \
                if session['started_date'] else '?'
            if messagebox.askyesno(
                    self.lang.get('kit_resume_title', 'Ripresa Lavoro'),
                    self.lang.get('kit_msg_resume',
                                  'Sessione interrotta il {date} (stato {status}).\n'
                                  'Riprendere dal punto in cui era rimasta?')
                    .replace('{date}', started).replace('{status}', session['status']),
                    parent=self):
                whl.resume_session(cursor, session['id'], self.operator_id, lbl)
                self.session_id = session['id']
            else:
                whl.set_session_status(cursor, session['id'], 'ABORTED')
                self.session_id = whl.create_session(
                    cursor, self.list_id, self.operator_id,
                    self.info['file_hash'], phase=prl.PHASE_PROD)
        else:
            self.session_id = whl.create_session(
                cursor, self.list_id, self.operator_id,
                self.info['file_hash'], phase=prl.PHASE_PROD)
        self.db.conn.commit()
        cursor.close()

    # ─────────────────────── Scansione ricevimento ───────────────────── #

    def _on_scan(self, event=None):
        unique = self.scan_var.get().strip()
        self.alert_var.set('')
        if not unique:
            return
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT ISNULL(cpf.qty_actual, i.qty_picked)
            FROM Traceability_RS.dbo.picking_list_items i
            LEFT JOIN Traceability_RS.dbo.kit_item_checks cpf
                   ON cpf.item_id = i.id AND cpf.phase = 'PREFORMING'
            WHERE i.picking_list_id=? AND i.unique_number=? AND i.qty_picked > 0
        """, (self.list_id, unique))
        r = cursor.fetchone()
        cursor.close()
        if r is None:
            self._register_unknown(unique)
            return
        self.qty_var.set(_fmt_qty(r[0]))
        self.qty_entry.focus_set()
        self.qty_entry.selection_range(0, 'end')

    def _on_confirm(self, event=None):
        unique = self.scan_var.get().strip()
        qty_txt = self.qty_var.get().strip().replace(',', '.')
        self.alert_var.set('')
        if not unique:
            self.scan_entry.focus_set()
            return
        try:
            qty = float(qty_txt)
            if qty < 0:
                raise ValueError
        except ValueError:
            self.alert_var.set(self.lang.get('kit_err_qty', 'Quantità non valida'))
            return

        cursor = self.db.conn.cursor()
        try:
            outcome, item = prl.apply_prod_check(cursor, self.list_id, unique, qty,
                                                 self.operator_id, self.session_id)
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()

        if outcome == 'not_found':
            self._alert_unknown(unique)
        elif outcome == 'mismatch':
            self.bell()
            self.alert_var.set(
                self.lang.get('kit_pf_msg_mismatch',
                              '❌ Discrepanza: {code} — consegnata {exp}, ricevuta {got}')
                .replace('{code}', item['material_code'])
                .replace('{exp}', _fmt_qty(item['qty_expected']))
                .replace('{got}', _fmt_qty(item['qty_received'])))
        self.scan_var.set('')
        self.qty_var.set('')
        self.scan_entry.focus_set()
        self._refresh(keep_alert=True)

    def _register_unknown(self, unique):
        cursor = self.db.conn.cursor()
        try:
            whl.log_event(cursor, whl.orders_label(self.info['orders']),
                          'UNKNOWN_UNIQUE_NUMBER', phase=prl.PHASE_PROD,
                          unique_number=unique, operator_id=self.operator_id,
                          notes=f"list={self.list_id}")
            whl.touch_session(cursor, self.session_id)
            self.db.conn.commit()
        except Exception:
            self.db.conn.rollback()
        finally:
            cursor.close()
        self._alert_unknown(unique)
        self.scan_var.set('')
        self.qty_var.set('')
        self.scan_entry.focus_set()

    def _alert_unknown(self, unique):
        self.bell()
        self.alert_var.set(
            self.lang.get('kit_msg_unknown_unique',
                          '⚠ Unique number NON presente nella lista: {un} (registrato)')
            .replace('{un}', unique))

    # ─────────────────────────── Refresh ─────────────────────────────── #

    def _refresh(self, keep_alert=False):
        if not keep_alert:
            self.alert_var.set('')
        cursor = self.db.conn.cursor()
        items = prl.get_prod_items(cursor, self.list_id)
        state = prl.prod_state(cursor, self.list_id)
        cursor.close()

        self.tree.delete(*self.tree.get_children())
        for it in items:
            emoji = CHECK_EMOJI.get(it['check_status'], '⬜')
            tag = CHECK_TAG.get(it['check_status'], '')
            self.tree.insert('', 'end', values=(
                emoji, it['material_code'], it['unique_number'] or '',
                _fmt_qty(it['qty_expected']),
                _fmt_qty(it['qty_received']) if it['qty_received'] is not None else '',
            ), tags=(tag,))

        self.summary_var.set(
            f"🟢 {state['ok']}   ❌ {state['mismatch']}   ⬜ {state['unchecked']}"
            f"   /   {state['total']}")
        self.btn_ok.configure(state='normal' if state['all_ok'] else 'disabled')
        self.btn_fail.configure(state='normal' if state['has_mismatch'] else 'disabled')

    # ─────────────────────────── Esiti ───────────────────────────────── #

    def _finalize_ok(self):
        if not messagebox.askyesno(
                self.lang.get('kit_prod_btn_ok', 'Conferma Ricevimento OK'),
                self.lang.get('kit_prod_msg_confirm_ok',
                              'Tutte le quantità corrispondono. Confermare il ricevimento in linea?'),
                parent=self):
            return
        cursor = self.db.conn.cursor()
        try:
            prl.finalize_prod_ok(cursor, self.list_id, self.operator_id)
            self.db.conn.commit()
            logger.info("Lista #%d RECEIVED_IN_PRODUCTION (da %s)",
                        self.list_id, self.user_name)
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_prod_msg_ok_done',
                          'Kit ricevuto in linea: la produzione può procedere.'),
            parent=self)
        self.finished = True
        self._refresh_parent()
        self.destroy()

    def _finalize_fail(self):
        if not messagebox.askyesno(
                self.lang.get('kit_prod_btn_fail', 'Segnala Mancanze (Blocca)'),
                self.lang.get('kit_prod_msg_confirm_fail',
                              'L\'ordine verrà BLOCCATO (kit incompleto) e la preformatura '
                              'riceverà Email + Popup. Procedere?'),
                parent=self):
            return
        cursor = self.db.conn.cursor()
        try:
            result = prl.finalize_prod_fail(cursor, self.list_id, self.operator_id)
            self.db.conn.commit()
            logger.info("Lista #%d BLOCCATA in ricevimento linea (%s): %s",
                        self.list_id, self.user_name, result['bad_codes'])
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        msgs = result['messages']
        notif.send_kit_email_async(self.db.conn, msgs['subject'], msgs['body'])
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_prod_msg_fail_done',
                          'Ordine bloccato e preformatura avvisata (Email + Popup).'),
            parent=self)
        self.finished = True
        self._refresh_parent()
        self.destroy()

    # ─────────── Richiesta materiale aggiuntivo (§5.3.3) ─────────────── #

    def _request_material(self):
        dlg = tk.Toplevel(self)
        dlg.title(self.lang.get('kit_pf_btn_request', 'Richiedi Materiale'))
        dlg.geometry("420x260")
        dlg.transient(self)
        dlg.grab_set()
        f = ttk.Frame(dlg, padding=12)
        f.pack(expand=True, fill='both')

        ttk.Label(f, text=self.lang.get('kit_col_order', 'Ordine')).grid(row=0, column=0, sticky='w')
        order_cb = ttk.Combobox(f, state='readonly', values=self.info['orders'], width=20)
        order_cb.current(0)
        order_cb.grid(row=0, column=1, sticky='w', pady=3)

        ttk.Label(f, text=self.lang.get('kit_col_material', 'Codice Materiale')).grid(row=1, column=0, sticky='w')
        mat_var = tk.StringVar()
        sel = self.tree.selection()
        if sel:
            mat_var.set(self.tree.item(sel[0])['values'][1])
        ttk.Entry(f, textvariable=mat_var, width=28).grid(row=1, column=1, sticky='w', pady=3)

        ttk.Label(f, text=self.lang.get('kit_req_qty', 'Quantità aggiuntiva')).grid(row=2, column=0, sticky='w')
        qty_var = tk.StringVar()
        ttk.Entry(f, textvariable=qty_var, width=12).grid(row=2, column=1, sticky='w', pady=3)

        ttk.Label(f, text=self.lang.get('kit_req_note', 'Motivazione (obbligatoria)')).grid(row=3, column=0, sticky='nw')
        note_txt = tk.Text(f, width=32, height=4)
        note_txt.grid(row=3, column=1, sticky='w', pady=3)

        def submit():
            material = mat_var.get().strip()
            note = note_txt.get('1.0', 'end').strip()
            try:
                qty = float(qty_var.get().strip().replace(',', '.'))
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                       self.lang.get('kit_err_qty', 'Quantità non valida'),
                                       parent=dlg)
                return
            if not material or not note:
                messagebox.showwarning(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('kit_req_msg_required',
                                  'Codice materiale e motivazione sono obbligatori'),
                    parent=dlg)
                return
            cursor = self.db.conn.cursor()
            try:
                result = pfl.create_material_request(
                    cursor, order_cb.get(), prl.PHASE_PROD, material, qty,
                    self.operator_id, self.user_name, note, socket.gethostname())
                self.db.conn.commit()
            except Exception as e:
                self.db.conn.rollback()
                messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                     str(e), parent=dlg)
                return
            finally:
                cursor.close()
            msgs = result['messages']
            notif.send_kit_email_async(self.db.conn, msgs['subject'], msgs['body'])
            logger.info("Richiesta materiale #%d (PRODUZIONE) da %s (%s x %s)",
                        result['request_id'], self.user_name, qty, material)
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_req_msg_sent',
                              'Richiesta inviata al magazzino (Email + Popup).'),
                parent=dlg)
            dlg.destroy()

        btns = ttk.Frame(f)
        btns.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btns, text=self.lang.get('kit_btn_confirm', 'Conferma'),
                   command=submit).pack(side='left', padx=4)
        ttk.Button(btns, text=self.lang.get('kit_btn_cancel', 'Annulla'),
                   command=dlg.destroy).pack(side='left', padx=4)

    # ─────────────── Materiale ritrovato (§5.3.4 / §9.3) ─────────────── #

    def _material_found(self):
        cursor = self.db.conn.cursor()
        try:
            requests = prl.open_requests_for_orders(cursor, self.info['orders'])
        finally:
            cursor.close()
        if not requests:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_found_msg_none',
                              'Nessuna richiesta aperta per gli ordini di questo kit.'),
                parent=self)
            return

        dlg = tk.Toplevel(self)
        dlg.title(self.lang.get('kit_prod_btn_found', 'Materiale Ritrovato'))
        dlg.geometry("640x320")
        dlg.transient(self)
        dlg.grab_set()
        ttk.Label(dlg, text=self.lang.get(
            'kit_found_msg_pick', 'Seleziona la richiesta del materiale ritrovato:'),
            padding=8).pack(anchor='w')

        cols = ('id', 'order', 'material', 'qty', 'status', 'date')
        tree = ttk.Treeview(dlg, columns=cols, show='headings', selectmode='browse')
        for c, (txt, w) in {
            'id': ('ID', 45),
            'order': (self.lang.get('kit_col_order', 'Ordine'), 95),
            'material': (self.lang.get('kit_col_material', 'Codice Materiale'), 180),
            'qty': (self.lang.get('kit_col_qty', 'Qtà'), 60),
            'status': (self.lang.get('kit_col_status', 'Stato'), 100),
            'date': (self.lang.get('kit_col_set_date', 'Data'), 110),
        }.items():
            tree.heading(c, text=txt)
            tree.column(c, width=w, anchor='w' if c == 'material' else 'center')
        for r in requests:
            date = r['request_date'].strftime('%d/%m %H:%M') if r['request_date'] else ''
            qty = float(r['qty'] or 0)
            tree.insert('', 'end', values=(
                r['id'], r['order_number'], r['material_code'],
                str(int(qty)) if qty == int(qty) else f"{qty:g}",
                r['wh_status'], date))
        tree.pack(expand=True, fill='both', padx=8)

        def confirm():
            sel = tree.selection()
            if not sel:
                return
            req_id = int(tree.item(sel[0])['values'][0])
            note = simpledialog.askstring(
                self.lang.get('kit_prod_btn_found', 'Materiale Ritrovato'),
                self.lang.get('kit_found_msg_note',
                              'Nota sul ritrovamento (obbligatoria):'),
                parent=dlg)
            if not note or not note.strip():
                return
            cursor = self.db.conn.cursor()
            try:
                result = prl.mark_material_found(cursor, req_id,
                                                 self.operator_id, note.strip())
                self.db.conn.commit()
            except Exception as e:
                self.db.conn.rollback()
                messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                     str(e), parent=dlg)
                return
            finally:
                cursor.close()
            if not result['done']:
                messagebox.showinfo(
                    self.lang.get('info_title', 'Informazione'),
                    self.lang.get('kit_req_msg_not_pending',
                                  'La richiesta non è più in stato PENDING'),
                    parent=dlg)
            else:
                logger.info("Materiale ritrovato: richiesta #%d risolta da %s",
                            req_id, self.user_name)
                msg = self.lang.get('kit_found_msg_done',
                                    'Richiesta risolta: FOUND_IN_PRODUCTION. '
                                    'Il magazzino è stato avvisato (Popup).')
                if result['was_confirmed']:
                    msg += '\n' + self.lang.get(
                        'kit_found_msg_was_confirmed',
                        '⚠ Il WH aveva già confermato il prelievo: il responsabile '
                        'WH deve chiudere manualmente il ciclo (§9.3).')
                messagebox.showinfo(self.lang.get('info_title', 'Informazione'),
                                    msg, parent=dlg)
            dlg.destroy()

        btns = ttk.Frame(dlg, padding=8)
        btns.pack(fill='x')
        ttk.Button(btns, text=self.lang.get('kit_btn_confirm', 'Conferma'),
                   command=confirm).pack(side='right')
        ttk.Button(btns, text=self.lang.get('kit_btn_cancel', 'Annulla'),
                   command=dlg.destroy).pack(side='right', padx=6)

    # ─────────────────────────── Chiusura ────────────────────────────── #

    def _suspend(self):
        self._suspend_session()
        self.destroy()

    def _on_close(self):
        if not self.finished:
            self._suspend_session()
        self.destroy()

    def _suspend_session(self):
        if self.session_id is None:
            return
        cursor = self.db.conn.cursor()
        try:
            whl.set_session_status(cursor, self.session_id, 'SUSPENDED',
                                   operator_id=self.operator_id,
                                   orders_lbl=whl.orders_label(self.info['orders']))
            self.db.conn.commit()
        except Exception:
            self.db.conn.rollback()
        finally:
            cursor.close()

    def _refresh_parent(self):
        try:
            if hasattr(self.parent_win, '_refresh'):
                self.parent_win._refresh()
        except Exception:
            pass
