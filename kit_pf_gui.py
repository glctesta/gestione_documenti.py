"""
kit_pf_gui.py
GUI Fase 2 — Presa in Carico Preformatura — Sprint 3
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.2).

Apertura da menu con login 'verifica_kit_materiale' (_execute_authorized_action).
- Elenco kit chiusi dal WH da prendere in carico (per priorita')
- Verifica ingresso: scansione unique number + quantita' ricevuta,
  confronto con quanto chiuso dal WH (kit_item_checks)
- Esito OK -> kit IN_PREFORMING; discrepanze -> lista WH RIAPERTA +
  Email/Popup alla postazione magazzino
- Richiesta materiale aggiuntivo (scrap eccedente BOM, §5.2.3)
"""
import logging
import socket
import tkinter as tk
from tkinter import ttk, messagebox

import kit_wh_logic as whl
import kit_pf_logic as pfl
import kit_notifications as notif

logger = logging.getLogger("PlanMonitor")

PRIORITY_BADGE = {1: '🔴 P1', 2: '🟠 P2', 3: '🟡 P3', 4: '⬜ P0'}
CHECK_EMOJI = {None: '⬜', 'OK': '🟢', 'MISMATCH': '❌'}
CHECK_TAG = {None: '', 'OK': 'ok', 'MISMATCH': 'mismatch'}


def _fmt_qty(v):
    f = float(v or 0)
    return str(int(f)) if f == int(f) else f"{f:g}"


def open_kit_pf_window(parent, db, lang, user_name, operator_id):
    return KitPFWindow(parent, db, lang, user_name, operator_id)


class KitPFWindow(tk.Toplevel):
    """Elenco kit in attesa di presa in carico preformatura."""

    def __init__(self, parent, db, lang, user_name, operator_id):
        super().__init__(parent)
        self.app = parent
        self.db = db
        self.lang = lang
        self.user_name = user_name or '?'
        self.operator_id = operator_id

        self.title(lang.get('kit_pf_title', 'Preformatura — Ingresso Kit'))
        self.geometry("950x520")
        self.transient(parent)

        header = ttk.Frame(self, padding=(10, 6))
        header.pack(fill='x')
        ttk.Label(header, text=lang.get('kit_pf_header',
                                        'Kit chiusi dal magazzino in attesa di presa in carico'),
                  font=("Segoe UI", 11, "bold")).pack(side='left')
        ttk.Label(header, text=f"{lang.get('kit_operator', 'Operatore')}: {self.user_name}",
                  font=("Segoe UI", 9, "italic")).pack(side='right')

        cols = ('id', 'priority', 'orders', 'file', 'status', 'closed')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        headings = {
            'id': 'ID',
            'priority': lang.get('kit_col_priority', 'Priorità'),
            'orders': lang.get('kit_col_orders', 'Ordini'),
            'file': lang.get('kit_col_file', 'File'),
            'status': lang.get('kit_col_status', 'Stato WH'),
            'closed': lang.get('kit_col_closed_date', 'Chiusa il'),
        }
        widths = {'id': 50, 'priority': 80, 'orders': 300, 'file': 200,
                  'status': 90, 'closed': 130}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c],
                             anchor='w' if c in ('orders', 'file') else 'center')
        self.tree.pack(expand=True, fill='both', padx=10)
        self.tree.tag_configure('p1', background='#ffd6d6')
        self.tree.tag_configure('p2', background='#ffe8cc')
        self.tree.tag_configure('p3', background='#fff7cc')
        self.tree.bind('<Double-1>', lambda e: self._open_selected())

        footer = ttk.Frame(self, padding=10)
        footer.pack(fill='x')
        ttk.Button(footer, text=lang.get('kit_btn_open_verify', 'Apri verifica ingresso'),
                   command=self._open_selected).pack(side='left')
        ttk.Button(footer, text=lang.get('kit_btn_refresh', 'Aggiorna'),
                   command=self._refresh).pack(side='left', padx=6)

        self._refresh()
        logger.info("KitPFWindow aperta da %s", self.user_name)

    def _refresh(self):
        cursor = self.db.conn.cursor()
        try:
            rows = pfl.eligible_lists(cursor)
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            prio = int(r['prio_rank'] or 4)
            tag = f'p{prio}' if prio in (1, 2, 3) else ''
            closed = r['closed_date'].strftime('%d/%m/%Y %H:%M') if r['closed_date'] else ''
            self.tree.insert('', 'end', values=(
                r['id'], PRIORITY_BADGE.get(prio, prio), r['orders'],
                r['file_name'], r['status'], closed), tags=(tag,))

    def _open_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('kit_msg_select_list', 'Seleziona una lista di prelievo'),
                parent=self)
            return
        list_id = int(self.tree.item(sel[0])['values'][0])
        KitPFVerifyWindow(self, self.db, self.lang, self.user_name,
                          self.operator_id, list_id)


class KitPFVerifyWindow(tk.Toplevel):
    """Verifica di ingresso preformatura per una lista (§5.2.1/5.2.2)."""

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

        self.title(lang.get('kit_pf_verify_title', 'Verifica Ingresso Preformatura')
                   + f" — #{list_id}")
        self.geometry("1000x640")
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

        scan_frame = ttk.LabelFrame(self, text=lang.get('kit_pf_scan_frame',
                                                        'Scansione ingresso'), padding=10)
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

        cols = ('status', 'material', 'unique', 'picked', 'received')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        headings = {
            'status': lang.get('kit_col_state', 'Stato'),
            'material': lang.get('kit_col_material', 'Codice Materiale'),
            'unique': 'Unique Nr',
            'picked': lang.get('kit_pf_col_picked', 'Consegnata WH'),
            'received': lang.get('kit_pf_col_received', 'Ricevuta'),
        }
        widths = {'status': 60, 'material': 280, 'unique': 160,
                  'picked': 110, 'received': 110}
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
            footer, text=lang.get('kit_pf_btn_fail', 'Segnala Discrepanze'),
            command=self._finalize_fail)
        self.btn_fail.pack(side='right', padx=4)
        self.btn_ok = ttk.Button(
            footer, text=lang.get('kit_pf_btn_ok', 'Conferma Verifica OK'),
            command=self._finalize_ok)
        self.btn_ok.pack(side='right', padx=4)
        ttk.Button(footer, text=lang.get('kit_btn_suspend', 'Sospendi Sessione'),
                   command=self._suspend).pack(side='right', padx=4)
        ttk.Button(footer, text=lang.get('kit_pf_btn_request', 'Richiedi Materiale'),
                   command=self._request_material).pack(side='right', padx=12)

    # ─────────────────────── Sessione (fase PF) ──────────────────────── #

    def _start_session(self):
        cursor = self.db.conn.cursor()
        lbl = whl.orders_label(self.info['orders'])
        session = whl.find_open_session(cursor, self.list_id, phase=pfl.PHASE_PF)
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
                    self.info['file_hash'], phase=pfl.PHASE_PF)
        else:
            self.session_id = whl.create_session(
                cursor, self.list_id, self.operator_id,
                self.info['file_hash'], phase=pfl.PHASE_PF)
        self.db.conn.commit()
        cursor.close()

    # ─────────────────────── Scansione ingresso ──────────────────────── #

    def _on_scan(self, event=None):
        unique = self.scan_var.get().strip()
        self.alert_var.set('')
        if not unique:
            return
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT qty_picked FROM Traceability_RS.dbo.picking_list_items
            WHERE picking_list_id=? AND unique_number=? AND qty_picked > 0
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
            outcome, item = pfl.apply_pf_check(cursor, self.list_id, unique, qty,
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
                .replace('{exp}', _fmt_qty(item['qty_picked']))
                .replace('{got}', _fmt_qty(item['qty_received'])))
        self.scan_var.set('')
        self.qty_var.set('')
        self.scan_entry.focus_set()
        self._refresh(keep_alert=True)

    def _register_unknown(self, unique):
        cursor = self.db.conn.cursor()
        try:
            whl.log_event(cursor, whl.orders_label(self.info['orders']),
                          'UNKNOWN_UNIQUE_NUMBER', phase=pfl.PHASE_PF,
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
        items = pfl.get_pf_items(cursor, self.list_id)
        state = pfl.pf_state(cursor, self.list_id)
        cursor.close()

        self.tree.delete(*self.tree.get_children())
        for it in items:
            emoji = CHECK_EMOJI.get(it['check_status'], '⬜')
            tag = CHECK_TAG.get(it['check_status'], '')
            self.tree.insert('', 'end', values=(
                emoji, it['material_code'], it['unique_number'] or '',
                _fmt_qty(it['qty_picked']),
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
                self.lang.get('kit_pf_btn_ok', 'Conferma Verifica OK'),
                self.lang.get('kit_pf_msg_confirm_ok',
                              'Tutte le quantità corrispondono. Confermare la presa in carico?'),
                parent=self):
            return
        cursor = self.db.conn.cursor()
        try:
            pfl.finalize_pf_ok(cursor, self.list_id, self.operator_id)
            self.db.conn.commit()
            logger.info("Lista #%d IN_PREFORMING (verifica OK da %s)",
                        self.list_id, self.user_name)
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_pf_msg_ok_done',
                          'Kit preso in carico: stato IN_PREFORMING.'), parent=self)
        self.finished = True
        self._refresh_parent()
        self.destroy()

    def _finalize_fail(self):
        if not messagebox.askyesno(
                self.lang.get('kit_pf_btn_fail', 'Segnala Discrepanze'),
                self.lang.get('kit_pf_msg_confirm_fail',
                              'Le righe non conformi verranno restituite al magazzino e la '
                              'lista di prelievo sarà RIAPERTA.\nLa postazione WH riceverà '
                              'Email + Popup. Procedere?'),
                parent=self):
            return
        cursor = self.db.conn.cursor()
        try:
            result = pfl.finalize_pf_fail(cursor, self.list_id, self.operator_id)
            self.db.conn.commit()
            logger.info("Lista #%d RIAPERTA da verifica PF (%s): %s",
                        self.list_id, self.user_name, result['bad_codes'])
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        # Email dopo il commit (popup gia' accodato in transazione)
        msgs = result['messages']
        notif.send_kit_email_async(self.db.conn, msgs['subject'], msgs['body'])
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_pf_msg_fail_done',
                          'Lista riaperta e magazzino avvisato (Email + Popup).'),
            parent=self)
        self.finished = True
        self._refresh_parent()
        self.destroy()

    # ─────────────── Richiesta materiale aggiuntivo (§5.2.3) ─────────── #

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
                    cursor, order_cb.get(), pfl.PHASE_PF, material, qty,
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
            logger.info("Richiesta materiale #%d creata da %s (%s x %s)",
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
