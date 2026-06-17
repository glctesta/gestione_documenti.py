"""
kit_scan_gui.py
Interfaccia di scansione del Prelievo Magazzino (Fase 1) — Sprint 2
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §5.1.3, §5.1.4, §5.4, §9.2).

- Campo scansione sempre in focus (scanner USB HID = tastiera, §11.3)
- Semaforo: 🟢 completo, 🟠 parziale, 🔴 non prelevato
- Sospensione e Ripresa Lavoro con confronto hash del file sorgente
- Chiusura lista (solo tutto verde) e Chiusura con Deroga (secondo login
  del responsabile WH via _execute_authorized_action)
- Ogni scansione confermata e' una transazione autonoma (commit immediato)
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import kit_wh_logic as whl

logger = logging.getLogger("PlanMonitor")

STATUS_EMOJI = {
    whl.ST_COMPLETE: '🟢',
    whl.ST_PARTIAL: '🟠',
    whl.ST_PENDING: '🔴',
    whl.ST_PENDING_COMPLETION: '🔴',
    whl.ST_MISSING_FROM_LIST: '🔴',
    whl.ST_NOT_IN_BOM: '⚪',
    whl.ST_REMOVED: '⬛',
}
STATUS_TAG = {
    whl.ST_COMPLETE: 'ok',
    whl.ST_PARTIAL: 'partial',
    whl.ST_PENDING: 'missing',
    whl.ST_PENDING_COMPLETION: 'missing',
    whl.ST_MISSING_FROM_LIST: 'missing',
    whl.ST_NOT_IN_BOM: 'info',
    whl.ST_REMOVED: 'removed',
}


def _fmt_qty(v) -> str:
    f = float(v or 0)
    return str(int(f)) if f == int(f) else f"{f:g}"


def open_kit_scan_window(parent, app, db, lang, user_name, operator_id, list_id):
    """Apre la finestra di scansione per la picking list indicata.

    parent: finestra chiamante (KitPreparationWindow)
    app:    main app (per _execute_authorized_action nella deroga)
    """
    win = KitScanWindow(parent, app, db, lang, user_name, operator_id, list_id)
    return win


class KitScanWindow(tk.Toplevel):

    def __init__(self, parent, app, db, lang, user_name, operator_id, list_id):
        super().__init__(parent)
        self.app = app
        self.db = db
        self.lang = lang
        self.user_name = user_name or '?'
        self.operator_id = operator_id
        self.list_id = list_id
        self.session_id = None
        self.closed = False

        cursor = self.db.conn.cursor()
        self.info = whl.get_list_info(cursor, list_id)
        cursor.close()
        if not self.info:
            messagebox.showerror(lang.get('error_title', 'Errore'),
                                 f'Picking list #{list_id} non trovata', parent=parent)
            self.destroy()
            return

        self.title(lang.get('kit_scan_title', 'Prelievo Kit') +
                   f" — #{list_id}  {self.info['file_name']}")
        self.geometry("1050x680")
        self.transient(parent)

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Avvio sessione (con eventuale ripresa) e matching BOM
        try:
            self._start_session()
            self._run_bom_check()
        except Exception as e:
            self.db.conn.rollback()
            logger.error("KitScanWindow avvio fallito: %s", e)
            messagebox.showerror(lang.get('error_title', 'Errore'), str(e), parent=self)
            self.destroy()
            return

        self._refresh_items()
        self.scan_entry.focus_set()
        logger.info("KitScanWindow lista #%d aperta da %s (sessione %s)",
                    list_id, self.user_name, self.session_id)

    # ─────────────────────────── UI ──────────────────────────────────── #

    def _build_ui(self):
        lang = self.lang

        header = ttk.Frame(self, padding=(10, 6))
        header.pack(fill='x')
        orders_txt = ' / '.join(self.info['orders'])
        ttk.Label(header, text=f"{lang.get('kit_col_orders', 'Ordini')}: {orders_txt}",
                  font=("Segoe UI", 11, "bold")).pack(side='left')
        ttk.Label(header,
                  text=f"{lang.get('kit_operator', 'Operatore')}: {self.user_name}",
                  font=("Segoe UI", 9, "italic")).pack(side='right')

        scan_frame = ttk.LabelFrame(
            self, text=lang.get('kit_scan_frame', 'Scansione'), padding=10)
        scan_frame.pack(fill='x', padx=10, pady=(0, 6))

        ttk.Label(scan_frame,
                  text=lang.get('kit_scan_unique', 'Unique Number (Reel Code):')
                  ).grid(row=0, column=0, sticky='w')
        self.scan_var = tk.StringVar()
        self.scan_entry = ttk.Entry(scan_frame, textvariable=self.scan_var,
                                    width=28, font=("Consolas", 12))
        self.scan_entry.grid(row=0, column=1, padx=8)
        self.scan_entry.bind('<Return>', self._on_scan)

        ttk.Label(scan_frame,
                  text=lang.get('kit_scan_qty', 'Quantità prelevata:')
                  ).grid(row=0, column=2, sticky='w', padx=(16, 0))
        self.qty_var = tk.StringVar()
        self.qty_entry = ttk.Entry(scan_frame, textvariable=self.qty_var,
                                   width=10, font=("Consolas", 12))
        self.qty_entry.grid(row=0, column=3, padx=8)
        self.qty_entry.bind('<Return>', self._on_confirm)

        ttk.Button(scan_frame, text=lang.get('kit_btn_confirm', 'Conferma'),
                   command=self._on_confirm).grid(row=0, column=4, padx=8)

        self.alert_var = tk.StringVar()
        self.alert_lbl = ttk.Label(scan_frame, textvariable=self.alert_var,
                                   foreground='red', font=("Segoe UI", 10, "bold"))
        self.alert_lbl.grid(row=1, column=0, columnspan=5, sticky='w', pady=(6, 0))

        cols = ('status', 'material', 'unique', 'req', 'picked')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        headings = {
            'status': lang.get('kit_col_state', 'Stato'),
            'material': lang.get('kit_col_material', 'Codice Materiale'),
            'unique': 'Unique Nr',
            'req': lang.get('kit_col_required', 'Richiesta'),
            'picked': lang.get('kit_col_picked', 'Prelevata'),
        }
        widths = {'status': 60, 'material': 280, 'unique': 160, 'req': 100, 'picked': 100}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c],
                             anchor='w' if c == 'material' else 'center')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='top', expand=True, fill='both', padx=(10, 0))
        vsb.place(relx=1.0, rely=0.5, relheight=0.6, anchor='e')

        self.tree.tag_configure('ok', background='#d8f5d8')
        self.tree.tag_configure('partial', background='#ffe8cc')
        self.tree.tag_configure('missing', background='#ffd6d6')
        self.tree.tag_configure('info', background='#f0f0f0')
        self.tree.tag_configure('removed', background='#e0e0e0', foreground='#888888')

        footer = ttk.Frame(self, padding=10)
        footer.pack(fill='x')
        self.summary_var = tk.StringVar()
        ttk.Label(footer, textvariable=self.summary_var).pack(side='left')

        self.btn_derog = ttk.Button(
            footer, text=lang.get('kit_btn_close_derog', 'Chiudi con Deroga'),
            command=self._close_with_derogation)
        self.btn_derog.pack(side='right', padx=4)
        self.btn_close = ttk.Button(
            footer, text=lang.get('kit_btn_close_list', 'Chiudi Lista'),
            command=self._close_list)
        self.btn_close.pack(side='right', padx=4)
        ttk.Button(footer, text=lang.get('kit_btn_suspend', 'Sospendi Sessione'),
                   command=self._suspend).pack(side='right', padx=4)

    # ───────────────────── Sessione / Ripresa (§5.4) ─────────────────── #

    def _start_session(self):
        cursor = self.db.conn.cursor()
        lbl = whl.orders_label(self.info['orders'])
        session = whl.find_open_session(cursor, self.list_id)

        if session:
            started = session['started_date'].strftime('%d/%m/%Y %H:%M') \
                if session['started_date'] else '?'
            msg = (self.lang.get(
                'kit_msg_resume',
                'Sessione interrotta il {date} (stato {status}).\nRiprendere dal punto in cui era rimasta?')
                .replace('{date}', started)
                .replace('{status}', session['status']))
            if messagebox.askyesno(self.lang.get('kit_resume_title', 'Ripresa Lavoro'),
                                   msg, parent=self):
                whl.resume_session(cursor, session['id'], self.operator_id, lbl)
                self.session_id = session['id']
            else:
                whl.set_session_status(cursor, session['id'], 'ABORTED')
                self.session_id = whl.create_session(
                    cursor, self.list_id, self.operator_id, self.info['file_hash'])
        else:
            self.session_id = whl.create_session(
                cursor, self.list_id, self.operator_id, self.info['file_hash'])

        # Confronto file sorgente (sempre, §5.4.2 / §9.4)
        check = whl.check_source_file(cursor, self.list_id)
        if check['state'] != 'SAME':
            self._handle_file_change(cursor, check)

        self.db.conn.commit()
        cursor.close()

    def _handle_file_change(self, cursor, check):
        lang = self.lang
        if check['state'] == 'MISSING':
            messagebox.showwarning(
                lang.get('kit_file_changed_title', 'File sorgente cambiato'),
                lang.get('kit_msg_file_missing',
                         'Il file usato per questa lista non è più presente:\n{path}\n'
                         'Si continua con i dati salvati.')
                .replace('{path}', check['path']),
                parent=self)
            whl.keep_old_file(cursor, self.list_id, self.operator_id, None)
            whl.set_resume_decision(cursor, self.session_id, 'KEEP_OLD_FILE',
                                    'File sorgente assente')
            return

        adopt = messagebox.askyesno(
            lang.get('kit_file_changed_title', 'File sorgente cambiato'),
            lang.get('kit_msg_file_changed',
                     'Il file in T:\\KITTING differisce da quello usato in precedenza '
                     'per questa lista.\n\nSÌ = adotta il NUOVO file (le righe verranno '
                     'riallineate)\nNO = continua con i dati salvati')
            , parent=self)
        if adopt:
            result = whl.adopt_new_file(cursor, self.list_id, self.operator_id)
            whl.set_resume_decision(cursor, self.session_id, 'ADOPT_NEW_FILE',
                                    f"added={result['added']} updated={result['updated']} "
                                    f"removed={result['removed']}")
            self.info = whl.get_list_info(cursor, self.list_id)
            messagebox.showinfo(
                lang.get('kit_file_changed_title', 'File sorgente cambiato'),
                lang.get('kit_msg_file_adopted',
                         'Nuovo file adottato: {added} righe aggiunte, '
                         '{updated} aggiornate, {removed} rimosse.')
                .replace('{added}', str(result['added']))
                .replace('{updated}', str(result['updated']))
                .replace('{removed}', str(result['removed'])),
                parent=self)
        else:
            whl.keep_old_file(cursor, self.list_id, self.operator_id,
                              check['current_hash'])
            whl.set_resume_decision(cursor, self.session_id, 'KEEP_OLD_FILE',
                                    'Scelta operatore alla ripresa')

    def _run_bom_check(self):
        cursor = self.db.conn.cursor()
        result = whl.classify_items(cursor, self.list_id, self.operator_id)
        self.db.conn.commit()
        cursor.close()
        if result['not_in_bom'] or result['missing']:
            parts = []
            if result['not_in_bom']:
                parts.append(self.lang.get('kit_msg_not_in_bom',
                                           'Codici nel file ma non in BOM (informativi):')
                             + '\n' + ', '.join(result['not_in_bom'][:15]))
            for order, codes in result['missing'].items():
                parts.append(self.lang.get('kit_msg_missing_bom',
                                           'In BOM di {order} ma assenti dalla lista:')
                             .replace('{order}', order)
                             + '\n' + ', '.join(codes[:15]))
            messagebox.showwarning(
                self.lang.get('kit_bom_check_title', 'Verifica BOM'),
                '\n\n'.join(parts), parent=self)

    # ───────────────────────── Scansione ─────────────────────────────── #

    def _on_scan(self, event=None):
        unique = self.scan_var.get().strip()
        self.alert_var.set('')
        if not unique:
            return
        cursor = self.db.conn.cursor()
        item = whl.find_item_by_unique(cursor, self.list_id, unique)
        cursor.close()
        if item is None:
            self._register_unknown(unique)
            return
        if item['pick_status'] == whl.ST_COMPLETE:
            if not messagebox.askyesno(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('kit_msg_duplicate_scan',
                                  'Riga già completata ({code}). Sovrascrivere la quantità?')
                    .replace('{code}', item['material_code']),
                    parent=self):
                self._reset_scan()
                return
        remaining = item['qty_required']
        self.qty_var.set(_fmt_qty(remaining))
        self._select_row_by_unique(unique)
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
            self.qty_entry.focus_set()
            return

        cursor = self.db.conn.cursor()
        try:
            outcome, item = whl.apply_scan(cursor, self.list_id, unique, qty,
                                           self.operator_id, self.session_id)
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            logger.error("apply_scan fallita: %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()

        if outcome == 'not_found':
            self._alert_unknown(unique)
        self._reset_scan()
        self._refresh_items(keep_alert=True)

    def _register_unknown(self, unique):
        """Scansione di un codice assente dalla lista (§9.2): log + alert."""
        cursor = self.db.conn.cursor()
        try:
            whl.log_event(cursor, whl.orders_label(self.info['orders']),
                          'UNKNOWN_UNIQUE_NUMBER', unique_number=unique,
                          operator_id=self.operator_id, notes=f"list={self.list_id}")
            whl.touch_session(cursor, self.session_id)
            self.db.conn.commit()
        except Exception:
            self.db.conn.rollback()
        finally:
            cursor.close()
        self._alert_unknown(unique)
        self._reset_scan()
        self._refresh_items(keep_alert=True)

    def _alert_unknown(self, unique):
        self.bell()
        self.alert_var.set(
            self.lang.get('kit_msg_unknown_unique',
                          '⚠ Unique number NON presente nella lista: {un} (registrato)')
            .replace('{un}', unique))

    def _reset_scan(self):
        self.scan_var.set('')
        self.qty_var.set('')
        self.scan_entry.focus_set()

    def _select_row_by_unique(self, unique):
        for iid in self.tree.get_children():
            if str(self.tree.set(iid, 'unique')) == unique:
                self.tree.selection_set(iid)
                self.tree.see(iid)
                break

    # ───────────────────────── Refresh / stato ───────────────────────── #

    def _refresh_items(self, keep_alert=False):
        if not keep_alert:
            self.alert_var.set('')
        cursor = self.db.conn.cursor()
        items = whl.get_items(cursor, self.list_id)
        state = whl.closure_state(cursor, self.list_id)
        cursor.close()

        self.tree.delete(*self.tree.get_children())
        for it in items:
            emoji = STATUS_EMOJI.get(it['pick_status'], '❔')
            tag = STATUS_TAG.get(it['pick_status'], '')
            self.tree.insert('', 'end', values=(
                emoji, it['material_code'], it['unique_number'] or '',
                _fmt_qty(it['qty_required']), _fmt_qty(it['qty_picked']),
            ), tags=(tag,))

        c = state['counts']
        summary = (f"🟢 {c.get(whl.ST_COMPLETE, 0)}   "
                   f"🟠 {c.get(whl.ST_PARTIAL, 0)}   "
                   f"🔴 {c.get(whl.ST_PENDING, 0) + c.get(whl.ST_PENDING_COMPLETION, 0) + c.get(whl.ST_MISSING_FROM_LIST, 0)}")
        if c.get(whl.ST_NOT_IN_BOM):
            summary += f"   ⚪ {c[whl.ST_NOT_IN_BOM]}"
        if state['unknown_scans']:
            summary += ('   ' + self.lang.get('kit_lbl_unknown', '⚠ sconosciuti:')
                        + f" {state['unknown_scans']}")
        self.summary_var.set(summary)

        self.btn_close.configure(state='normal' if state['can_close'] else 'disabled')
        self.btn_derog.configure(state='disabled' if state['can_close'] else 'normal')

    # ───────────────────────── Chiusure (§5.1.4) ─────────────────────── #

    def _close_list(self):
        cursor = self.db.conn.cursor()
        state = whl.closure_state(cursor, self.list_id)
        if not state['can_close']:
            cursor.close()
            return
        if state['unknown_scans']:
            if not messagebox.askyesno(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('kit_msg_unknown_on_close',
                                  'Sono registrate {n} scansioni con unique number sconosciuto. '
                                  'Confermare comunque la chiusura?')
                    .replace('{n}', str(state['unknown_scans'])),
                    parent=self):
                cursor.close()
                return
        if not messagebox.askyesno(
                self.lang.get('kit_btn_close_list', 'Chiudi Lista'),
                self.lang.get('kit_msg_confirm_close',
                              'Tutte le righe sono complete. Chiudere la lista?'),
                parent=self):
            cursor.close()
            return
        try:
            whl.close_list(cursor, self.list_id, self.operator_id)
            self.db.conn.commit()
            logger.info("Lista #%d CHIUSA da %s", self.list_id, self.user_name)
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            self.lang.get('kit_msg_closed', 'Lista chiusa: kit completo.'), parent=self)
        self.closed = True
        self._notify_parent_refresh()
        self.destroy()

    def _close_with_derogation(self):
        """Richiede il login del responsabile WH (stessa chiave) + nota obbligatoria."""
        def after_auth():
            manager_id = self.app.last_authorized_user_id
            manager_name = self.app.last_authenticated_user_name or '?'
            note = simpledialog.askstring(
                self.lang.get('kit_btn_close_derog', 'Chiudi con Deroga'),
                self.lang.get('kit_msg_derog_note',
                              'Nota di deroga (obbligatoria) — responsabile: {mgr}')
                .replace('{mgr}', manager_name),
                parent=self)
            if note is None:
                return
            note = note.strip()
            if not note:
                messagebox.showwarning(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('kit_msg_derog_note_required',
                                  'La nota di deroga è obbligatoria'),
                    parent=self)
                return
            cursor = self.db.conn.cursor()
            try:
                missing = whl.close_with_derogation(cursor, self.list_id,
                                                    manager_id, note)
                self.db.conn.commit()
                logger.info("Lista #%d chiusa con DEROGA da %s; mancanti=%s",
                            self.list_id, manager_name, missing)
            except Exception as e:
                self.db.conn.rollback()
                messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                     str(e), parent=self)
                return
            finally:
                cursor.close()
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('kit_msg_derog_done',
                              'Lista chiusa con deroga. Codici mancanti: {codes}')
                .replace('{codes}', ', '.join(missing) or '—'),
                parent=self)
            self.closed = True
            self._notify_parent_refresh()
            self.destroy()

        self.app._execute_authorized_action('conferma_kit_completamento', after_auth)

    # ───────────────────────── Sospensione ───────────────────────────── #

    def _suspend(self):
        self._suspend_session()
        self._notify_parent_refresh()
        self.destroy()

    def _on_close(self):
        if not self.closed:
            self._suspend_session()
        self._notify_parent_refresh()
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
            logger.info("Sessione %s sospesa (lista #%d)", self.session_id, self.list_id)
        except Exception as e:
            self.db.conn.rollback()
            logger.error("Sospensione sessione fallita: %s", e)
        finally:
            cursor.close()

    def _notify_parent_refresh(self):
        try:
            parent = self.master
            if hasattr(parent, '_refresh_picking_lists'):
                parent._refresh_picking_lists()
        except Exception:
            pass
