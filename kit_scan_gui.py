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
import ctypes
import logging
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import winsound

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
        self._sort_col = None
        self._sort_reverse = False
        self._current_items = []

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

        # Attiva la finestra a livello OS PRIMA dei messagebox di avvio.
        # _start_session (ripresa) e _run_bom_check aprono messagebox modali con
        # parent=self mentre la finestra transient non e' ancora attiva: cosi'
        # facendo il focus tastiera restava orfano e le due caselle di scansione
        # risultavano non editabili. Portandola in primo piano e prendendo il
        # focus prima, i messagebox sono figli di una finestra gia' attiva.
        self.update_idletasks()
        self.lift()
        try:
            self.focus_force()
        except Exception:
            pass

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
        # Focus differito sulla casella scansione: dopo i messagebox e dopo che
        # la finestra e' realmente mappata, cosi' il focus attecchisce davvero.
        self.after(50, self._focus_scan)
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

        self.filter_positive_var = tk.BooleanVar(value=True)
        self.filter_positive_cb = ttk.Checkbutton(
            scan_frame,
            text=lang.get('kit_filter_positive', 'Mostra solo quantità necessarie > 0'),
            variable=self.filter_positive_var,
            command=self._refresh_items
        )
        self.filter_positive_cb.grid(row=0, column=5, padx=(16, 0), sticky='w')

        self.alert_var = tk.StringVar()
        self.alert_lbl = ttk.Label(scan_frame, textvariable=self.alert_var,
                                   foreground='red', font=("Segoe UI", 10, "bold"))
        self.alert_lbl.grid(row=1, column=0, columnspan=6, sticky='w', pady=(6, 0))

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
            self.tree.heading(c, text=headings[c], command=lambda c=c: self._sort_items(c))
            self.tree.column(c, width=widths[c],
                             anchor='w' if c == 'material' else 'center')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='top', expand=True, fill='both', padx=(10, 0))
        vsb.place(relx=1.0, rely=0.5, relheight=0.6, anchor='e')

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label=lang.get('kit_pick_label', 'Preleva etichetta'),
            command=self._pick_label_prompt)
        self.tree.bind('<Button-3>', self._on_tree_right_click)

        self.tree.tag_configure('ok', background='#d8f5d8')
        self.tree.tag_configure('partial', background='#ffe8cc')
        self.tree.tag_configure('missing', background='#ffd6d6')
        self.tree.tag_configure('info', background='#f0f0f0')
        self.tree.tag_configure('removed', background='#e0e0e0', foreground='#888888')
        self.tree.tag_configure('label', background='#e6e6fa')

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

    def _focus_scan(self):
        """Porta la finestra in primo piano e mette il focus sulla casella di
        scansione. Idempotente: usata all'avvio (differita) e dopo ogni reset."""
        try:
            self.lift()
            self.focus_force()
        except Exception:
            pass
        try:
            self.scan_entry.focus_set()
            self.scan_entry.selection_range(0, 'end')
        except Exception:
            pass

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
            self._play_error_sound()
            self._show_big_red_x(unique)
            self._register_unknown(unique)
            return
        self._play_success_sound()
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
            self._play_error_sound()
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
        else:
            self._play_success_sound()
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
        self._reset_scan()
        self._refresh_items(keep_alert=True)

    def _alert_unknown(self, unique):
        self._play_error_sound()
        self._show_big_red_x(unique)
        self.alert_var.set(
            self.lang.get('kit_msg_unknown_unique',
                          '⚠ Unique number NON presente nella lista: {un} (registrato)')
            .replace('{un}', unique))

    def _play_success_sound(self):
        """Suono di sistema Windows per scansione HU valida."""
        try:
            winsound.MessageBeep(winsound.MB_OK)
        except Exception:
            pass

    def _error_sound_path(self):
        """Percorso del file MP3 di errore (risolve sia in sviluppo che in exe PyInstaller)."""
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'sounds', 'universfield-error-notification-352286.mp3')

    def _play_error_sound(self):
        """Suono di errore dedicato: file MP3 incluso nel build; fallback su MessageBeep."""
        path = self._error_sound_path()
        if os.path.exists(path):
            try:
                def _play():
                    alias = f"errsnd_{threading.current_thread().ident or 0}"
                    mci = ctypes.windll.winmm.mciSendStringW
                    mci.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
                    mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, None)
                    mci(f'play {alias}', None, 0, None)

                    def _close():
                        try:
                            mci(f'stop {alias}', None, 0, None)
                            mci(f'close {alias}', None, 0, None)
                        except Exception:
                            pass

                    threading.Timer(3.0, _close).start()

                threading.Thread(target=_play, daemon=True).start()
                return
            except Exception:
                logger.exception("Errore riproduzione MP3 di errore")
        try:
            winsound.MessageBeep(winsound.MB_ICONHAND)
        except Exception:
            pass

    def _show_big_red_x(self, unique):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        popup.configure(bg='white', highlightbackground='red', highlightthickness=10)
        popup.geometry("300x300")
        popup.transient(self)
        popup.grab_set()
        lbl_x = tk.Label(popup, text='X', font=('Arial', 140, 'bold'),
                         fg='red', bg='white')
        lbl_x.pack(expand=True, fill='both')
        lbl_msg = tk.Label(
            popup,
            text=self.lang.get('kit_msg_big_x', '{un}\nNON IN LISTA')
                .replace('{un}', unique),
            font=('Arial', 14, 'bold'),
            fg='red',
            bg='white',
            wraplength=260,
            justify='center'
        )
        lbl_msg.pack(side='bottom', pady=10)
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        popup.geometry(f"+{x}+{y}")

        def _release_and_destroy(popup):
            try:
                popup.grab_release()
            except Exception:
                pass
            popup.destroy()

        self.after(2000, lambda: _release_and_destroy(popup))

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

        # Applica filtro "solo quantità necessarie > 0" se checkbox selezionato
        if self.filter_positive_var.get():
            items = [it for it in items if float(it.get('qty_required') or 0) > 0]

        self._current_items = items
        self._render_items()

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

    def _render_items(self):
        """Disegna la treeview usando self._current_items rispettando l'ordinamento corrente."""
        self.tree.delete(*self.tree.get_children())
        for idx, it in enumerate(self._current_items):
            emoji = STATUS_EMOJI.get(it['pick_status'], '❔')
            tag = STATUS_TAG.get(it['pick_status'], '')
            material = it['material_code']
            if it.get('Source') == 'LABEL':
                material = '🏷️ ' + material
                tag = 'label'
            self.tree.insert('', 'end', iid=str(idx), values=(
                emoji, material, it['unique_number'] or '',
                _fmt_qty(it['qty_required']), _fmt_qty(it['qty_picked']),
            ), tags=(tag,))

    def _on_tree_right_click(self, event):
        """Mostra il menu contestuale solo sulle righe etichetta prelevabili."""
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        try:
            item = self._current_items[int(row_id)]
        except (ValueError, IndexError):
            return
        if item.get('Source') != 'LABEL' or item.get('pick_status') == whl.ST_COMPLETE:
            return
        self.tree.selection_set(row_id)
        self.context_menu.post(event.x_root, event.y_root)

    def _pick_label_prompt(self):
        """Chiede la quantità prelevata per la riga etichetta selezionata."""
        sel = self.tree.selection()
        if not sel:
            return
        try:
            item = self._current_items[int(sel[0])]
        except (ValueError, IndexError):
            return
        if item.get('Source') != 'LABEL' or item.get('pick_status') == whl.ST_COMPLETE:
            return
        qty_txt = simpledialog.askstring(
            self.lang.get('kit_pick_label', 'Preleva etichetta'),
            self.lang.get('kit_prompt_label_qty',
                          'Quantità prelevata per {material}:')
            .replace('{material}', str(item.get('material_code', ''))),
            parent=self)
        if qty_txt is None:
            return
        qty_txt = qty_txt.strip().replace(',', '.')
        try:
            qty = float(qty_txt)
        except ValueError:
            self.alert_var.set(self.lang.get('kit_err_qty', 'Quantità non valida'))
            self._play_error_sound()
            return
        self._pick_label_item(item['id'], qty)

    def _pick_label_item(self, item_id, qty):
        """Aggiorna la riga picking_list_items per un prelievo etichetta manuale."""
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(
                "SELECT qty_required FROM Traceability_RS.dbo.picking_list_items WHERE id = ?",
                (item_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Riga picking_list_items id={item_id} non trovata")
            qty_required = float(row[0] or 0)
            if qty <= 0:
                pick_status = whl.ST_PENDING
            elif qty >= qty_required:
                pick_status = whl.ST_COMPLETE
            else:
                pick_status = whl.ST_PARTIAL
            cursor.execute("""
                UPDATE Traceability_RS.dbo.picking_list_items
                SET qty_picked = ?, pick_status = ?, picked_by = ?, picked_date = GETDATE()
                WHERE id = ?
            """, (qty, pick_status, self.operator_id, item_id))
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            logger.error("Prelievo etichetta fallito: %s", e)
            messagebox.showerror(self.lang.get('error_title', 'Errore'), str(e), parent=self)
            return
        finally:
            cursor.close()
        self._refresh_items()

    def _sort_items(self, col):
        """Ordina self._current_items per la colonna cliccata e ridisegna la griglia."""
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False

        reverse = self._sort_reverse

        def sort_key(it):
            if col == 'status':
                return int(it.get('pick_status', 0))
            if col == 'material':
                return str(it.get('material_code') or '').lower()
            if col == 'unique':
                return str(it.get('unique_number') or '').lower()
            if col in ('req', 'picked'):
                return float(it.get('qty_required' if col == 'req' else 'qty_picked') or 0)
            return ''

        self._current_items.sort(key=sort_key, reverse=reverse)
        self._render_items()

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
        label_pending = [it for it in self._current_items
                         if it.get('Source') == 'LABEL'
                         and it.get('pick_status') not in (whl.ST_COMPLETE, whl.ST_REMOVED)]
        if label_pending:
            msg = '\n'.join(
                f"{it['material_code']} (richiesti {_fmt_qty(it['qty_required'])}, prelevati {_fmt_qty(it['qty_picked'])}"
                for it in label_pending
            )
            if not messagebox.askyesno(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('kit_msg_labels_pending',
                                  'Attenzione: le seguenti righe etichetta non sono ancora prelevate:\n{labels}\n\nChiudere comunque la lista?')
                    .replace('{labels}', msg),
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
