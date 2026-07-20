# -*- coding: utf-8 -*-
"""
ei_aros_label_gui.py — Stampa etichette EI → Aros.

L'operatore digita/seleziona un codice Eutron (colonna ``EutronCode``, la "chiave
CodiceEutron") dalla tabella ``traceability_rs.dbo.ConversionTables``; il sistema
stampa un'etichetta ZEBRA (ZPL) con ``ArosCode`` e ``ArosDescription``
corrispondenti, la quantità inserita dall'operatore e il nome dell'operatore che
ha stampato (in caratteri piccoli).

Configurazione stampante (di norma ZEBRA) + template dello script di stampa in
``ei_aros_label_config.json`` (bottone "Configura stampante"): connessione
DEFAULT/USB/IP e template ZPL editabile con segnaposto.

Nota: le font residenti Zebra non supportano il vero corsivo; il nome operatore è
reso nella font più piccola. Per un corsivo reale servirebbe un rendering a
immagine (non incluso).
"""
import json
import logging
import os
import tkinter as tk
from tkinter import messagebox, ttk

logger = logging.getLogger("TraceabilityRS")

CONFIG_FILENAME = "ei_aros_label_config.json"

# Segnaposto disponibili nel template: {aros_code} {aros_description} {eutron_code}
# {quantity} {operator} {date}
DEFAULT_ZPL = r"""^XA
^CI28
^PW780
^LL400
^LH0,0

^FO20,20^A0N,64,64^FD{aros_code}^FS
^FO560,18^GB200,72,3^FS
^FO585,38^A0N,34,34^FDEI AROS^FS

^FO20,115^A0N,30,30^FB740,3,4,L^FD{aros_description}^FS

^FO20,235^A0N,28,28^FDEI: {eutron_code}^FS
^FO20,278^A0N,28,28^FDAROS: {aros_code}^FS

^FO500,205^A0N,40,40^FDQ.ta^FS
^FO500,250^A0N,90,90^FD{quantity}^FS

^FO560,110^BQN,2,5^FDLA,{aros_code}^FS

^FO20,362^A0N,18,18^FDOp.: {operator}   {date}^FS
^XZ
"""


# ─── Config (stampante + template) ───────────────────────────────────────────

def _config_path() -> str:
    try:
        from config_manager import get_base_path
        base = get_base_path()
    except Exception:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, CONFIG_FILENAME)


def default_config() -> dict:
    return {
        "connection_type": "DEFAULT",   # DEFAULT | USB | IP
        "ip": "",
        "port": 9100,
        "usb_printer_name": "",
        "printer_model": "ZEBRA",
        "zpl_template": DEFAULT_ZPL,
        "last_updated": "",
    }


def load_config() -> dict:
    path = _config_path()
    cfg = default_config()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            cfg.update({k: saved[k] for k in cfg if k in saved})
        except Exception as e:
            logger.error(f"EI→Aros: errore lettura config {path}: {e}")
    if not (cfg.get('zpl_template') or '').strip():
        cfg['zpl_template'] = DEFAULT_ZPL
    return cfg


def save_config(cfg: dict) -> bool:
    path = _config_path()
    try:
        from datetime import datetime
        cfg['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
        logger.info(f"EI→Aros: config stampante salvata in {path}")
        return True
    except Exception as e:
        logger.error(f"EI→Aros: errore salvataggio config: {e}")
        return False


def _zpl_escape(value) -> str:
    """Neutralizza i caratteri di controllo ZPL nei dati variabili."""
    s = '' if value is None else str(value)
    return s.replace('^', ' ').replace('~', ' ').replace('\\', ' ').strip()


def build_zpl(template: str, mapping: dict) -> str:
    zpl = template or DEFAULT_ZPL
    for key, val in mapping.items():
        zpl = zpl.replace('{' + key + '}', _zpl_escape(val))
    return zpl


def print_zpl(cfg: dict, zpl: str) -> None:
    """Invia lo ZPL alla stampante secondo la connessione configurata.
    Solleva un'eccezione in caso di errore."""
    from printer_connection_manager import get_printer_connection
    printer_config = {
        'connection_type': cfg.get('connection_type', 'DEFAULT'),
        'ip': cfg.get('ip', ''),
        'port': int(cfg.get('port', 9100) or 9100),
        'usb_printer_name': cfg.get('usb_printer_name', ''),
        'printer_model': cfg.get('printer_model', 'ZEBRA'),
    }
    conn = get_printer_connection(printer_config)
    conn.print_label(zpl)


# ─── Finestra principale: selezione codice + stampa ──────────────────────────

class EiArosLabelWindow(tk.Toplevel):
    def __init__(self, master, db, lang, operator_name=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.operator_name = operator_name or 'N/A'
        self._rows = []          # tutti i record
        self._by_code = {}       # EutronCode -> [record, ...]
        self._all_codes = []     # elenco EutronCode ordinato (per il combo)
        self._current = None     # record selezionato

        L = self.lang.get
        self.title(L('ei_aros_title', 'Etichette EI → Aros'))
        self.geometry('640x430')
        self.minsize(560, 400)
        self.resizable(True, True)
        self._build_ui()
        self._load_data()
        self.grab_set()

    # ── UI ──
    def _build_ui(self):
        L = self.lang.get
        header = tk.Frame(self, bg='#1F3864')
        header.pack(fill=tk.X)
        tk.Label(header, text=L('ei_aros_title', 'Etichette EI → Aros'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)
        tk.Label(header, text=f"{L('ei_aros_operator', 'Operatore')}: {self.operator_name}",
                 bg='#1F3864', fg='#c9d4ea', font=('Helvetica', 9, 'italic')).pack(
            side=tk.RIGHT, padx=12)

        body = ttk.Frame(self, padding=14)
        body.pack(fill=tk.BOTH, expand=True)
        body.columnconfigure(1, weight=1)

        ttk.Label(body, text=L('ei_aros_eutron', 'Codice Eutron:')).grid(
            row=0, column=0, sticky='w', pady=6)
        self._v_code = tk.StringVar()
        self._cb_code = ttk.Combobox(body, textvariable=self._v_code)
        self._cb_code.grid(row=0, column=1, sticky='ew', padx=6, pady=6)
        self._cb_code.bind('<KeyRelease>', self._on_code_keyrelease)
        self._cb_code.bind('<<ComboboxSelected>>', lambda e: self._lookup())
        self._cb_code.bind('<Return>', lambda e: self._lookup())
        ttk.Button(body, text=L('ei_aros_verify', 'Verifica'),
                   command=self._lookup).grid(row=0, column=2, padx=4, pady=6)

        # Risultati (sola lettura)
        res = ttk.LabelFrame(body, text=L('ei_aros_result', 'Corrispondenza Aros'), padding=10)
        res.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(10, 6))
        res.columnconfigure(1, weight=1)
        ttk.Label(res, text=L('ei_aros_code', 'Codice Aros:')).grid(row=0, column=0, sticky='w', pady=3)
        self._l_aros = ttk.Label(res, text='—', font=('Segoe UI', 11, 'bold'), foreground='#1F3864')
        self._l_aros.grid(row=0, column=1, sticky='w', padx=8, pady=3)
        ttk.Label(res, text=L('ei_aros_desc', 'Descrizione:')).grid(row=1, column=0, sticky='nw', pady=3)
        self._l_desc = ttk.Label(res, text='—', wraplength=420, justify='left')
        self._l_desc.grid(row=1, column=1, sticky='w', padx=8, pady=3)

        # Quantità
        ttk.Label(body, text=L('ei_aros_qty', 'Quantità:')).grid(row=2, column=0, sticky='w', pady=6)
        self._v_qty = tk.StringVar()
        vcmd = (self.register(self._validate_qty), '%P')
        ttk.Entry(body, textvariable=self._v_qty, width=16, validate='key',
                  validatecommand=vcmd).grid(row=2, column=1, sticky='w', padx=6, pady=6)

        # Stato
        self._status = tk.Label(body, text='', anchor='w', fg='#555')
        self._status.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(6, 0))

        # Bottoni
        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=14, pady=10)
        self._btn_print = ttk.Button(bar, text=L('ei_aros_print', '🖨 Stampa etichetta'),
                                     command=self._print, state='disabled')
        self._btn_print.pack(side=tk.LEFT)
        ttk.Button(bar, text=L('ei_aros_config', '⚙ Configura stampante'),
                   command=self._open_config).pack(side=tk.LEFT, padx=8)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    # ── Dati ──
    def _load_data(self):
        L = self.lang.get
        try:
            cur = self.db.conn.cursor()
            cur.execute(
                "SELECT ConversionTableId, EutronCode, ArosCode, ArosDescription "
                "FROM traceability_rs.dbo.ConversionTables "
                "WHERE EutronCode IS NOT NULL AND LTRIM(RTRIM(EutronCode)) <> '' "
                "ORDER BY EutronCode")
            for r in cur.fetchall():
                rec = {
                    'id': r.ConversionTableId,
                    'eutron': (r.EutronCode or '').strip(),
                    'aros': (r.ArosCode or '').strip(),
                    'desc': (r.ArosDescription or '').strip(),
                }
                self._rows.append(rec)
                bucket = self._by_code.setdefault(rec['eutron'], [])
                # Evita duplicati identici (stesso Aros+descrizione): non è una
                # vera ambiguità e non deve far comparire il chooser.
                if not any(x['aros'] == rec['aros'] and x['desc'] == rec['desc'] for x in bucket):
                    bucket.append(rec)
            cur.close()
            self._all_codes = sorted(self._by_code.keys(), key=str.lower)
            self._cb_code['values'] = self._all_codes
            self._set_status(L('ei_aros_loaded', '{0} codici caricati.').format(len(self._all_codes)))
        except Exception as e:
            logger.error(f"EI→Aros: errore caricamento ConversionTables: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"{L('ei_aros_load_err', 'Impossibile caricare i codici')}:\n{e}",
                                 parent=self)

    def _on_code_keyrelease(self, event):
        # Non filtrare sui tasti di navigazione/selezione
        if event.keysym in ('Up', 'Down', 'Return', 'Escape', 'Left', 'Right', 'Tab'):
            return
        typed = self._v_code.get().strip().lower()
        if not typed:
            self._cb_code['values'] = self._all_codes
            return
        matches = [c for c in self._all_codes if typed in c.lower()]
        self._cb_code['values'] = matches or self._all_codes

    def _lookup(self):
        L = self.lang.get
        code = self._v_code.get().strip()
        self._current = None
        self._l_aros.config(text='—')
        self._l_desc.config(text='—')
        self._btn_print.config(state='disabled')
        if not code:
            return
        # match esatto (case-insensitive)
        rows = self._by_code.get(code)
        if rows is None:
            key = next((k for k in self._by_code if k.lower() == code.lower()), None)
            rows = self._by_code.get(key) if key else None
        if not rows:
            self._set_status(L('ei_aros_not_found', "Codice Eutron '{0}' non trovato.").format(code),
                             error=True)
            return
        rec = rows[0] if len(rows) == 1 else self._choose_row(rows)
        if not rec:
            return
        self._current = rec
        self._v_code.set(rec['eutron'])
        self._l_aros.config(text=rec['aros'] or '—')
        self._l_desc.config(text=rec['desc'] or '—')
        self._btn_print.config(state='normal')
        self._set_status(L('ei_aros_ready', 'Codice trovato. Inserire la quantità e stampare.'))

    def _choose_row(self, rows):
        """Disambigua un EutronCode con più corrispondenze Aros."""
        L = self.lang.get
        dlg = tk.Toplevel(self)
        dlg.title(L('ei_aros_choose', 'Seleziona corrispondenza'))
        dlg.geometry('460x240')
        dlg.transient(self)
        dlg.grab_set()
        ttk.Label(dlg, text=L('ei_aros_choose_msg',
                              'Più corrispondenze per questo codice Eutron. Selezionare:'),
                  wraplength=430).pack(padx=10, pady=8, anchor='w')
        lb = tk.Listbox(dlg, height=6)
        for rec in rows:
            lb.insert('end', f"{rec['aros']} — {rec['desc']}")
        lb.pack(fill=tk.BOTH, expand=True, padx=10)
        lb.selection_set(0)
        chosen = {'rec': None}

        def _ok():
            sel = lb.curselection()
            if sel:
                chosen['rec'] = rows[sel[0]]
            dlg.destroy()

        bar = ttk.Frame(dlg)
        bar.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(bar, text=L('btn_ok', 'OK'), command=_ok).pack(side=tk.RIGHT)
        ttk.Button(bar, text=L('btn_cancel', 'Annulla'), command=dlg.destroy).pack(side=tk.RIGHT, padx=6)
        lb.bind('<Double-Button-1>', lambda e: _ok())
        self.wait_window(dlg)
        return chosen['rec']

    def _validate_qty(self, proposed):
        return proposed == '' or proposed.isdigit()

    def _set_status(self, text, error=False):
        self._status.config(text=text, fg='#B71C1C' if error else '#2E7D32')

    # ── Stampa ──
    def _print(self):
        L = self.lang.get
        if not self._current:
            return
        qty = self._v_qty.get().strip()
        if not qty or not qty.isdigit() or int(qty) <= 0:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('ei_aros_qty_req', 'Inserire una quantità valida (numero > 0).'),
                                   parent=self)
            return
        from datetime import datetime
        cfg = load_config()
        mapping = {
            'aros_code': self._current['aros'],
            'aros_description': self._current['desc'],
            'eutron_code': self._current['eutron'],
            'quantity': qty,
            'operator': self.operator_name,
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        }
        zpl = build_zpl(cfg.get('zpl_template', DEFAULT_ZPL), mapping)
        try:
            self.config(cursor='watch')
            self.update_idletasks()
            print_zpl(cfg, zpl)
            self._set_status(L('ei_aros_printed', 'Etichetta inviata alla stampante: {0} (q.tà {1}).')
                             .format(self._current['aros'], qty))
            logger.info("EI→Aros etichetta stampata: Aros=%s Eutron=%s qty=%s op=%s",
                        self._current['aros'], self._current['eutron'], qty, self.operator_name)
        except Exception as e:
            logger.error(f"EI→Aros: errore stampa: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"{L('ei_aros_print_err', 'Errore durante la stampa')}:\n{e}",
                                 parent=self)
        finally:
            self.config(cursor='')

    def _open_config(self):
        EiArosPrinterConfigDialog(self, self.lang)


# ─── Finestra configurazione stampante + script ──────────────────────────────

class EiArosPrinterConfigDialog(tk.Toplevel):
    def __init__(self, master, lang):
        super().__init__(master)
        self.lang = lang
        L = self.lang.get
        self.title(L('ei_aros_cfg_title', 'Configurazione stampante EI → Aros'))
        self.geometry('720x620')
        self.minsize(620, 560)
        self.transient(master)
        self._cfg = load_config()
        self._build_ui()
        self._apply_cfg_to_ui()
        self.grab_set()

    def _build_ui(self):
        L = self.lang.get
        root = ttk.Frame(self, padding=12)
        root.pack(fill=tk.BOTH, expand=True)

        # Connessione
        conn = ttk.LabelFrame(root, text=L('ei_aros_cfg_conn', 'Connessione stampante'), padding=10)
        conn.pack(fill=tk.X)
        self._v_conn = tk.StringVar(value='DEFAULT')
        for val, label in (('DEFAULT', L('ei_aros_cfg_default', 'Stampante di default di Windows')),
                           ('USB', L('ei_aros_cfg_usb', 'Stampante USB / locale')),
                           ('IP', L('ei_aros_cfg_ip', 'Stampante di rete (IP)'))):
            ttk.Radiobutton(conn, text=label, variable=self._v_conn, value=val,
                            command=self._on_conn_changed).pack(anchor='w', pady=2)

        # USB
        self._usb_frame = ttk.Frame(conn)
        ttk.Label(self._usb_frame, text=L('ei_aros_cfg_printer', 'Stampante:')).grid(
            row=0, column=0, sticky='w', padx=(20, 4), pady=4)
        self._v_usb = tk.StringVar()
        self._cb_usb = ttk.Combobox(self._usb_frame, textvariable=self._v_usb, width=44, state='readonly')
        self._cb_usb.grid(row=0, column=1, sticky='w', pady=4)
        try:
            from printer_connection_manager import get_available_printers
            self._cb_usb['values'] = get_available_printers()
        except Exception as e:
            logger.warning(f"EI→Aros: elenco stampanti non disponibile: {e}")

        # IP
        self._ip_frame = ttk.Frame(conn)
        ttk.Label(self._ip_frame, text=L('ei_aros_cfg_ipaddr', 'Indirizzo IP:')).grid(
            row=0, column=0, sticky='w', padx=(20, 4), pady=4)
        self._v_ip = tk.StringVar()
        ttk.Entry(self._ip_frame, textvariable=self._v_ip, width=20).grid(row=0, column=1, sticky='w', pady=4)
        ttk.Label(self._ip_frame, text=L('ei_aros_cfg_port', 'Porta:')).grid(
            row=0, column=2, sticky='w', padx=(12, 4), pady=4)
        self._v_port = tk.StringVar(value='9100')
        ttk.Entry(self._ip_frame, textvariable=self._v_port, width=8).grid(row=0, column=3, sticky='w', pady=4)

        # Modello
        model_fr = ttk.Frame(root)
        model_fr.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(model_fr, text=L('ei_aros_cfg_model', 'Modello (linguaggio):')).pack(side=tk.LEFT)
        self._v_model = tk.StringVar(value='ZEBRA')
        ttk.Combobox(model_fr, textvariable=self._v_model, width=14, state='readonly',
                     values=['ZEBRA']).pack(side=tk.LEFT, padx=6)
        ttk.Label(model_fr, text=L('ei_aros_cfg_model_hint', '(ZPL — stampanti Zebra)'),
                  foreground='#777').pack(side=tk.LEFT)

        # Template ZPL
        tpl = ttk.LabelFrame(root, text=L('ei_aros_cfg_script', 'Script di stampa (ZPL)'), padding=8)
        tpl.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        ttk.Label(tpl, foreground='#777', wraplength=660, justify='left',
                  text=L('ei_aros_cfg_placeholders',
                         'Segnaposto disponibili: {aros_code} {aros_description} {eutron_code} '
                         '{quantity} {operator} {date}')).pack(anchor='w', pady=(0, 4))
        txt_wrap = ttk.Frame(tpl)
        txt_wrap.pack(fill=tk.BOTH, expand=True)
        self._txt = tk.Text(txt_wrap, wrap='none', font=('Consolas', 9), height=12)
        vsb = ttk.Scrollbar(txt_wrap, orient='vertical', command=self._txt.yview)
        hsb = ttk.Scrollbar(txt_wrap, orient='horizontal', command=self._txt.xview)
        self._txt.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self._txt.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        txt_wrap.rowconfigure(0, weight=1)
        txt_wrap.columnconfigure(0, weight=1)
        ttk.Button(tpl, text=L('ei_aros_cfg_reset', '↺ Ripristina script predefinito'),
                   command=self._reset_template).pack(anchor='w', pady=(6, 0))

        # Bottoni
        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=12, pady=10)
        ttk.Button(bar, text=L('ei_aros_cfg_testprint', '🖨 Stampa di prova'),
                   command=self._test_print).pack(side=tk.LEFT)
        ttk.Button(bar, text=L('btn_save', '💾 Salva'), command=self._save).pack(side=tk.RIGHT)
        ttk.Button(bar, text=L('btn_cancel', 'Annulla'), command=self.destroy).pack(side=tk.RIGHT, padx=6)

    def _on_conn_changed(self):
        ct = self._v_conn.get()
        self._usb_frame.pack_forget()
        self._ip_frame.pack_forget()
        if ct == 'USB':
            self._usb_frame.pack(fill=tk.X)
        elif ct == 'IP':
            self._ip_frame.pack(fill=tk.X)

    def _apply_cfg_to_ui(self):
        c = self._cfg
        self._v_conn.set(c.get('connection_type', 'DEFAULT'))
        self._v_usb.set(c.get('usb_printer_name', ''))
        self._v_ip.set(c.get('ip', ''))
        self._v_port.set(str(c.get('port', 9100)))
        self._v_model.set(c.get('printer_model', 'ZEBRA'))
        self._txt.delete('1.0', 'end')
        self._txt.insert('1.0', c.get('zpl_template', DEFAULT_ZPL))
        self._on_conn_changed()

    def _reset_template(self):
        self._txt.delete('1.0', 'end')
        self._txt.insert('1.0', DEFAULT_ZPL)

    def _collect(self) -> dict:
        L = self.lang.get
        ct = self._v_conn.get()
        try:
            port = int(self._v_port.get().strip() or '9100')
        except ValueError:
            port = 9100
        cfg = {
            'connection_type': ct,
            'ip': self._v_ip.get().strip(),
            'port': port,
            'usb_printer_name': self._v_usb.get().strip(),
            'printer_model': self._v_model.get().strip() or 'ZEBRA',
            'zpl_template': self._txt.get('1.0', 'end').strip() + '\n',
        }
        if ct == 'USB' and not cfg['usb_printer_name']:
            raise ValueError(L('ei_aros_cfg_need_usb', 'Selezionare una stampante USB/locale.'))
        if ct == 'IP' and not cfg['ip']:
            raise ValueError(L('ei_aros_cfg_need_ip', 'Inserire l\'indirizzo IP della stampante.'))
        return cfg

    def _save(self):
        L = self.lang.get
        try:
            cfg = self._collect()
        except ValueError as ve:
            messagebox.showwarning(L('warning', 'Attenzione'), str(ve), parent=self)
            return
        if save_config(cfg):
            messagebox.showinfo(L('success', 'Fatto'),
                                L('ei_aros_cfg_saved', 'Configurazione salvata.'), parent=self)
            self.destroy()
        else:
            messagebox.showerror(L('error', 'Errore'),
                                 L('ei_aros_cfg_save_err', 'Salvataggio configurazione fallito.'),
                                 parent=self)

    def _test_print(self):
        L = self.lang.get
        try:
            cfg = self._collect()
        except ValueError as ve:
            messagebox.showwarning(L('warning', 'Attenzione'), str(ve), parent=self)
            return
        from datetime import datetime
        mapping = {
            'aros_code': 'TEST-0001',
            'aros_description': 'ETICHETTA DI PROVA EI → AROS',
            'eutron_code': 'TEST+PROVA',
            'quantity': '1',
            'operator': L('ei_aros_cfg_test', 'PROVA'),
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        }
        zpl = build_zpl(cfg.get('zpl_template', DEFAULT_ZPL), mapping)
        try:
            print_zpl(cfg, zpl)
            messagebox.showinfo(L('success', 'Fatto'),
                                L('ei_aros_cfg_test_ok', 'Etichetta di prova inviata alla stampante.'),
                                parent=self)
        except Exception as e:
            logger.error(f"EI→Aros: errore stampa di prova: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"{L('ei_aros_print_err', 'Errore durante la stampa')}:\n{e}",
                                 parent=self)


def open_ei_aros_label_window(master, db, lang, operator_name=None):
    """Entry point: apre la finestra Etichette EI → Aros."""
    EiArosLabelWindow(master, db, lang, operator_name=operator_name)
