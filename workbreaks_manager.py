# -*- coding: utf-8 -*-
"""
workbreaks_manager.py
Form per gestire le regole di pausa/orario della tabella Employee.dbo.WorkBreaks.
Ogni pausa può essere associata a più CDC / Sub CDC / Funzioni tramite Employee.dbo.WorkBreakData.

Menu: Operazioni → Personale → Gestione Orari
Autorizzazione: gestisci_orari
"""

import datetime
import itertools
import logging
import os
import time
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

logger = logging.getLogger('TraceabilityRS')

QUERY_WORKBREAKS = """
SELECT wb.WorkBreakId,
       wb.IsForChangeShift,
       wb.Shift,
       wb.FromTime,
       wb.ToTime,
       CASE WHEN wb.Sound IS NOT NULL AND DATALENGTH(wb.Sound) > 0 THEN 1 ELSE 0 END AS SoundLoaded,
       CASE WHEN wb.TextToshow IS NOT NULL AND DATALENGTH(wb.TextToshow) > 0 THEN 1 ELSE 0 END AS TextLoaded,
       wb.EmployeerId,
       er.EmployeerName,
       wb.WorkBreakReasonId,
       wbr.ReasonDescription
FROM Employee.dbo.WorkBreaks wb
LEFT JOIN Employee.dbo.Employeers er ON er.EmployeerId = wb.EmployeerId
LEFT JOIN Employee.dbo.WorkBreakReasons wbr ON wbr.WorkBreakReasonId = wb.WorkBreakReasonId
WHERE wb.DateOut IS NULL
ORDER BY wb.FromTime, wb.Shift
"""

QUERY_WORKBREAKS_FALLBACK = """
SELECT wb.WorkBreakId,
       wb.IsForChangeShift,
       wb.Shift,
       wb.FromTime,
       wb.ToTime,
       CASE WHEN wb.Sound IS NOT NULL AND DATALENGTH(wb.Sound) > 0 THEN 1 ELSE 0 END AS SoundLoaded,
       CASE WHEN wb.TextToshow IS NOT NULL AND DATALENGTH(wb.TextToshow) > 0 THEN 1 ELSE 0 END AS TextLoaded,
       wb.EmployeerId,
       er.EmployeerName,
       NULL AS WorkBreakReasonId,
       NULL AS ReasonDescription
FROM Employee.dbo.WorkBreaks wb
LEFT JOIN Employee.dbo.Employeers er ON er.EmployeerId = wb.EmployeerId
WHERE wb.DateOut IS NULL
ORDER BY wb.FromTime, wb.Shift
"""

QUERY_WORKBREAK_BLOB = """
SELECT Sound, TextToshow
FROM Employee.dbo.WorkBreaks
WHERE WorkBreakId = ?
"""

QUERY_CDC_CHILDREN = """
SELECT wd.WorkBreakId,
       wd.CdcId,
       cc.CdcDescription
FROM Employee.dbo.WorkBreakData wd
INNER JOIN Employee.dbo.CostCenters cc ON cc.CdcId = wd.CdcId
WHERE wd.DateOut IS NULL
  AND wd.CdcId IS NOT NULL
  AND wd.WorkBreakId IN ({placeholders})
"""

QUERY_SUBCDC_CHILDREN = """
SELECT wd.WorkBreakId,
       wd.SubCdcId,
       sc.SubCdcDescription
FROM Employee.dbo.WorkBreakData wd
INNER JOIN Employee.dbo.CdcSub sc ON sc.SubCdcId = wd.SubCdcId
WHERE wd.DateOut IS NULL
  AND wd.SubCdcId IS NOT NULL
  AND wd.WorkBreakId IN ({placeholders})
"""

QUERY_FUNCTION_CHILDREN = """
SELECT wd.WorkBreakId,
       wd.FunctionId,
       f.FunctionDescription
FROM Employee.dbo.WorkBreakData wd
INNER JOIN Employee.dbo.Functions f ON f.FunctionId = wd.FunctionId
WHERE wd.DateOut IS NULL
  AND wd.FunctionId IS NOT NULL
  AND wd.WorkBreakId IN ({placeholders})
"""

QUERY_CENTERS = """
SELECT CdcId, Cdc, CdcDescription
FROM Employee.dbo.CostCenters
ORDER BY CdcDescription
"""

QUERY_SUB_CENTERS = """
SELECT SubCdcId, CdcId, SubCdc, SubCdcDescription
FROM Employee.dbo.CdcSub
ORDER BY SubCdcDescription
"""

QUERY_FUNCTIONS = """
SELECT FunctionId, FunctionCode, FunctionDescription
FROM Employee.dbo.Functions
ORDER BY FunctionDescription
"""

QUERY_EMPLOYERS = """
SELECT EmployeerId, EmployeerName
FROM Employee.dbo.Employeers
ORDER BY EmployeerName
"""

QUERY_REASONS = """
SELECT WorkBreakReasonId, ReasonDescription
FROM Employee.dbo.WorkBreakReasons
WHERE DateOut IS NULL
ORDER BY ReasonDescription
"""

DEFAULT_EMPLOYER_NAME = 'Vandewiele Romania Srl'


def open_workbreaks_manager(master, db, lang):
    WorkBreaksManager(master, db, lang)


class WorkBreaksManager(tk.Toplevel):
    """Gestione pause/orari di lavoro (WorkBreaks + WorkBreakData)."""

    def __init__(self, master, db, lang):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.L = self.lang.get

        self.title(self.L('workbreaks_title', 'Gestione Orari'))
        self.geometry('1200x820')
        self.minsize(1000, 700)
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._cdc_items = []           # [(CdcId, display)]
        self._sub_cdc_items = []       # [(SubCdcId, display)]
        self._functions = []           # [(FunctionId, display)]
        self._employers = {}           # display -> EmployeerId
        self._reasons = {}             # display -> WorkBreakReasonId

        self._rows = {}                # tree iid -> record dict
        self._cdc_by_parent = {}       # WorkBreakId -> {CdcId: desc}
        self._subcdc_by_parent = {}    # WorkBreakId -> {SubCdcId: desc}
        self._functions_by_parent = {} # WorkBreakId -> {FunctionId: desc}

        self._sort_col = None          # colonna attualmente ordinata
        self._sort_dir = 'asc'         # 'asc' o 'desc'
        self._heading_texts = {}       # nome colonna -> testo base heading
        self._sort_keys = {}           # nome colonna -> funzione chiave ordinamento

        self._text_bytes = b''         # contenuto binario documento caricato
        self._sound_bytes = b''        # contenuto binario audio caricato
        self._text_changed = False
        self._sound_changed = False
        self._loading_form = False     # per evitare trace durante caricamento

        start = time.monotonic()
        logger.info('Apertura Gestione Orari (WorkBreaks)')
        self._build_ui()
        logger.info('UI costruita in %.3fs', time.monotonic() - start)

        t0 = time.monotonic()
        self._load_lookups()
        logger.info('Lookup caricati in %.3fs', time.monotonic() - t0)

        t0 = time.monotonic()
        self._load_data()
        logger.info('Dati caricati in %.3fs', time.monotonic() - t0)
        logger.info('Apertura Gestione Orari completata in %.3fs', time.monotonic() - start)

        self.protocol('WM_DELETE_WINDOW', self.destroy)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill='both', expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        # Intestazione
        ttk.Label(
            main,
            text=self.L('workbreaks_header', 'Gestione pause e fasce orarie'),
            font=('Segoe UI', 12, 'bold')
        ).grid(row=0, column=0, sticky='w', pady=(0, 8))

        # Albero
        tree_frame = ttk.Frame(main)
        tree_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        cols = (
            'cdc', 'subcdc', 'functions', 'shift', 'from_time', 'to_time',
            'text', 'sound', 'change_shift', 'employer', 'reason'
        )
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            selectmode='browse'
        )
        heading_map = {
            'cdc': self.L('workbreaks_col_cdc', 'CDC'),
            'subcdc': self.L('workbreaks_col_subcdc', 'Sub CDC'),
            'functions': self.L('workbreaks_col_function', 'Funzioni'),
            'shift': self.L('workbreaks_col_shift', 'Turno'),
            'from_time': self.L('workbreaks_col_from', 'Dalle'),
            'to_time': self.L('workbreaks_col_to', 'Alle'),
            'text': self.L('workbreaks_col_text', 'Documento'),
            'sound': self.L('workbreaks_col_sound', 'Audio'),
            'change_shift': self.L('workbreaks_col_change_shift', 'Cambio turno'),
            'employer': self.L('workbreaks_col_employer', 'Azienda'),
            'reason': self.L('workbreaks_col_reason', 'Motivazione'),
        }
        self._heading_texts = heading_map
        for col, text in heading_map.items():
            self.tree.heading(
                col,
                text=text,
                command=lambda _col=col: self._on_heading_click(_col)
            )

        self._sort_keys = {
            'cdc': lambda rec: self._join_names(self._cdc_by_parent.get(rec['WorkBreakId'], {})),
            'subcdc': lambda rec: self._join_names(self._subcdc_by_parent.get(rec['WorkBreakId'], {})),
            'functions': lambda rec: self._join_names(self._functions_by_parent.get(rec['WorkBreakId'], {})),
            'shift': lambda rec: rec['Shift'],
            'from_time': lambda rec: rec['FromTime'],
            'to_time': lambda rec: rec['ToTime'],
            'text': lambda rec: rec['TextLoaded'],
            'sound': lambda rec: rec['SoundLoaded'],
            'change_shift': lambda rec: rec['IsForChangeShift'],
            'employer': lambda rec: rec['EmployeerName'].lower(),
            'reason': lambda rec: rec['ReasonDescription'].lower(),
        }

        self.tree.column('cdc', width=120)
        self.tree.column('subcdc', width=140)
        self.tree.column('functions', width=140)
        self.tree.column('shift', width=60, anchor='center')
        self.tree.column('from_time', width=70, anchor='center')
        self.tree.column('to_time', width=70, anchor='center')
        self.tree.column('text', width=80, anchor='center')
        self.tree.column('sound', width=80, anchor='center')
        self.tree.column('change_shift', width=90, anchor='center')
        self.tree.column('employer', width=120)
        self.tree.column('reason', width=120)

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Tooltip per colonne con testo troncato
        self._tooltip = None
        self.tree.bind('<Motion>', self._on_tree_motion)
        self.tree.bind('<Leave>', self._on_tree_leave)
        self.tree.bind('<ButtonPress>', lambda _event: self._hide_tooltip())

        # Editor
        editor = ttk.LabelFrame(
            main,
            text=self.L('workbreaks_editor', 'Dettaglio'),
            padding=10
        )
        editor.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        for c in range(6):
            editor.columnconfigure(c, weight=1)
        editor.rowconfigure(0, weight=1)
        editor.rowconfigure(5, weight=1)

        # Riga 0 - CDC (listbox multi) e Turno
        ttk.Label(editor, text=self.L('workbreaks_label_cdcs', 'CDC:')).grid(
            row=0, column=0, sticky='nw', padx=5, pady=3)
        cdc_frame = ttk.Frame(editor)
        cdc_frame.grid(row=0, column=1, columnspan=2, sticky='nsew', padx=5, pady=3)
        cdc_frame.columnconfigure(0, weight=1)
        cdc_frame.rowconfigure(0, weight=1)
        self.cdc_list = tk.Listbox(
            cdc_frame,
            selectmode='multiple',
            exportselection=False,
            height=4
        )
        self.cdc_list.grid(row=0, column=0, sticky='nsew')
        cdc_sb = ttk.Scrollbar(cdc_frame, orient='vertical', command=self.cdc_list.yview)
        self.cdc_list.configure(yscrollcommand=cdc_sb.set)
        cdc_sb.grid(row=0, column=1, sticky='ns')

        ttk.Label(editor, text=self.L('workbreaks_label_shift', 'Turno:')).grid(
            row=0, column=3, sticky='w', padx=5, pady=3)
        self.shift_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.shift_var, width=15).grid(
            row=0, column=4, sticky='ew', padx=5, pady=3)

        # Riga 1 - orari
        self.from_label = ttk.Label(editor, text=self.L('workbreaks_label_from', 'Dalle (HH:MM):'))
        self.from_label.grid(row=1, column=0, sticky='w', padx=5, pady=3)
        self.from_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.from_var, width=15).grid(
            row=1, column=1, sticky='ew', padx=5, pady=3)

        self.to_label = ttk.Label(editor, text=self.L('workbreaks_label_to', 'Alle (HH:MM):'))
        self.to_label.grid(row=1, column=2, sticky='w', padx=5, pady=3)
        self.to_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.to_var, width=15).grid(
            row=1, column=3, sticky='ew', padx=5, pady=3)

        # Riga 2 - Documento
        ttk.Label(editor, text=self.L('workbreaks_label_text', 'Documento:')).grid(
            row=2, column=0, sticky='w', padx=5, pady=3)
        self.text_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.text_var).grid(
            row=2, column=1, columnspan=4, sticky='ew', padx=5, pady=3)
        ttk.Button(
            editor,
            text=self.L('workbreaks_browse', 'Sfoglia...'),
            command=self._browse_document
        ).grid(row=2, column=5, sticky='ew', padx=5, pady=3)

        # Riga 3 - Audio
        ttk.Label(editor, text=self.L('workbreaks_label_sound', 'File audio:')).grid(
            row=3, column=0, sticky='w', padx=5, pady=3)
        self.sound_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.sound_var).grid(
            row=3, column=1, columnspan=4, sticky='ew', padx=5, pady=3)
        ttk.Button(
            editor,
            text=self.L('workbreaks_browse', 'Sfoglia...'),
            command=self._browse_sound
        ).grid(row=3, column=5, sticky='ew', padx=5, pady=3)

        # Tracce per rilevare modifica manuale dei campi file
        self.text_var.trace_add('write', self._on_text_var_changed)
        self.sound_var.trace_add('write', self._on_sound_var_changed)

        # Riga 4 - Cambio turno e Azienda
        self.change_shift_var = tk.IntVar(value=0)
        ttk.Checkbutton(
            editor,
            text=self.L('workbreaks_label_change_shift', 'Cambio turno'),
            variable=self.change_shift_var,
            onvalue=1,
            offvalue=0
        ).grid(row=4, column=0, sticky='w', padx=5, pady=3)
        self.change_shift_var.trace_add('write', self._on_change_shift_toggle)

        ttk.Label(editor, text=self.L('workbreaks_label_employer', 'Azienda:')).grid(
            row=4, column=2, sticky='w', padx=5, pady=3)
        self.employer_var = tk.StringVar()
        self.employer_combo = ttk.Combobox(
            editor,
            textvariable=self.employer_var,
            state='readonly',
            width=30
        )
        self.employer_combo.grid(row=4, column=3, columnspan=3, sticky='ew', padx=5, pady=3)

        # Riga 5 - Motivazione pausa
        ttk.Label(editor, text=self.L('workbreaks_label_reason', 'Motivazione:')).grid(
            row=5, column=0, sticky='w', padx=5, pady=3)
        self.reason_var = tk.StringVar()
        self.reason_combo = ttk.Combobox(
            editor,
            textvariable=self.reason_var,
            state='readonly',
            width=30
        )
        self.reason_combo.grid(row=5, column=1, columnspan=5, sticky='ew', padx=5, pady=3)

        # Riga 6 - Sub CDC e Funzioni (listbox multi-selezione)
        ttk.Label(editor, text=self.L('workbreaks_label_subcdcs', 'Sub CDC:')).grid(
            row=6, column=0, sticky='nw', padx=5, pady=(10, 3))
        ttk.Label(editor, text=self.L('workbreaks_label_functions', 'Funzioni:')).grid(
            row=6, column=3, sticky='nw', padx=5, pady=(10, 3))

        # Sub CDC listbox
        sub_frame = ttk.Frame(editor)
        sub_frame.grid(row=7, column=0, columnspan=3, sticky='nsew', padx=5, pady=3)
        sub_frame.columnconfigure(0, weight=1)
        sub_frame.rowconfigure(0, weight=1)
        self.sub_cdc_list = tk.Listbox(
            sub_frame,
            selectmode='multiple',
            exportselection=False,
            height=6
        )
        self.sub_cdc_list.grid(row=0, column=0, sticky='nsew')
        sub_sb = ttk.Scrollbar(sub_frame, orient='vertical', command=self.sub_cdc_list.yview)
        self.sub_cdc_list.configure(yscrollcommand=sub_sb.set)
        sub_sb.grid(row=0, column=1, sticky='ns')

        # Functions listbox
        func_frame = ttk.Frame(editor)
        func_frame.grid(row=7, column=3, columnspan=3, sticky='nsew', padx=5, pady=3)
        func_frame.columnconfigure(0, weight=1)
        func_frame.rowconfigure(0, weight=1)
        self.function_list = tk.Listbox(
            func_frame,
            selectmode='multiple',
            exportselection=False,
            height=6
        )
        self.function_list.grid(row=0, column=0, sticky='nsew')
        func_sb = ttk.Scrollbar(func_frame, orient='vertical', command=self.function_list.yview)
        self.function_list.configure(yscrollcommand=func_sb.set)
        func_sb.grid(row=0, column=1, sticky='ns')

        editor.rowconfigure(7, weight=1)

        # Pulsanti
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=3, column=0, sticky='ew')

        ttk.Button(
            btn_frame,
            text=self.L('btn_new', 'Nuovo'),
            command=self._on_new
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_save', 'Salva'),
            command=self._on_save
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_delete', 'Elimina'),
            command=self._on_delete
        ).pack(side='left', padx=(0, 8))
        ttk.Button(
            btn_frame,
            text=self.L('btn_close', 'Chiudi'),
            command=self.destroy
        ).pack(side='right')

        self.status_var = tk.StringVar()
        ttk.Label(main, textvariable=self.status_var, foreground='#555').grid(
            row=4, column=0, sticky='w', pady=(5, 0)
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------
    def _load_lookups(self):
        logger.info('Caricamento lookup Gestione Orari (CDC, SubCDC, Funzioni, Aziende)')
        total_start = time.monotonic()
        try:
            # CDC
            t0 = time.monotonic()
            rows = self.db.fetch_all(QUERY_CENTERS)
            logger.debug('Query CDC eseguita in %.3fs: %d righe', time.monotonic() - t0, len(rows))
            self._cdc_items = []
            self.cdc_list.delete(0, 'end')
            for r in rows:
                cdc_id = r[0]
                cdc_code = r[1] or ''
                cdc_desc = r[2] or ''
                display = f'{cdc_desc} ({cdc_code})' if cdc_code else cdc_desc
                self._cdc_items.append((cdc_id, display))
                self.cdc_list.insert('end', display)

            # Sub CDC
            t0 = time.monotonic()
            rows = self.db.fetch_all(QUERY_SUB_CENTERS)
            logger.debug('Query SubCDC eseguita in %.3fs: %d righe', time.monotonic() - t0, len(rows))
            self._sub_cdc_items = []
            self.sub_cdc_list.delete(0, 'end')
            for r in rows:
                sub_id = r[0]
                sub_code = r[2] or ''
                sub_desc = r[3] or ''
                display = f'{sub_desc} ({sub_code})' if sub_code else sub_desc
                self._sub_cdc_items.append((sub_id, display))
                self.sub_cdc_list.insert('end', display)

            # Functions
            t0 = time.monotonic()
            rows = self.db.fetch_all(QUERY_FUNCTIONS)
            logger.debug('Query Functions eseguita in %.3fs: %d righe', time.monotonic() - t0, len(rows))
            self._functions = []
            self.function_list.delete(0, 'end')
            for r in rows:
                fid = r[0]
                fcode = r[1] or ''
                fdesc = r[2] or ''
                display = f'{fdesc} ({fcode})' if fcode else fdesc
                self._functions.append((fid, display))
                self.function_list.insert('end', display)

            # Employers
            t0 = time.monotonic()
            rows = self.db.fetch_all(QUERY_EMPLOYERS)
            logger.debug('Query Employers eseguita in %.3fs: %d righe', time.monotonic() - t0, len(rows))
            emp_displays = []
            self._employers = {}
            for r in rows:
                eid = r[0]
                ename = r[1] or ''
                self._employers[ename] = eid
                emp_displays.append(ename)
            self.employer_combo['values'] = emp_displays

            # Reasons (opzionale: se la tabella non esiste ancora, continuiamo)
            t0 = time.monotonic()
            try:
                rows = self.db.fetch_all(QUERY_REASONS)
                logger.debug('Query Reasons eseguita in %.3fs: %d righe', time.monotonic() - t0, len(rows))
                reason_displays = []
                self._reasons = {}
                for r in rows:
                    rid = r[0]
                    rdesc = r[1] or ''
                    self._reasons[rdesc] = rid
                    reason_displays.append(rdesc)
                self.reason_combo['values'] = reason_displays
            except Exception as reason_err:
                logger.warning(
                    'Tabella WorkBreakReasons non disponibile, motivazioni non caricate: %s',
                    reason_err
                )
                self._reasons = {}
                self.reason_combo['values'] = []

            logger.info(
                'Lookup caricati in %.3fs: %d CDC, %d SubCDC, %d Funzioni, %d Aziende, %d Motivazioni',
                time.monotonic() - total_start,
                len(self._cdc_items), len(self._sub_cdc_items),
                len(self._functions), len(self._employers), len(self._reasons)
            )

        except Exception as e:
            logger.exception('Errore caricamento lookup Gestione Orari')
            self._set_error_status(f'Errore caricamento lookup: {e}')
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('workbreaks_load_err', 'Errore caricamento dati lookup')}:\n{e}",
                parent=self
            )

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------
    def _load_data(self):
        logger.info('Caricamento dati Gestione Orari')
        start_ts = time.monotonic()
        self.status_var.set(self.L('loading', 'Caricamento in corso...'))
        self.update_idletasks()

        self.tree.delete(*self.tree.get_children())
        self._rows = {}
        self._cdc_by_parent = {}
        self._subcdc_by_parent = {}
        self._functions_by_parent = {}
        self._clear_form()

        try:
            t0 = time.monotonic()
            parent_rows = self.db.fetch_all(QUERY_WORKBREAKS)
            logger.info('WorkBreaks padri caricati in %.3fs: %d righe', time.monotonic() - t0, len(parent_rows))
        except Exception as e:
            err_msg = str(e)
            if 'WorkBreakReasons' in err_msg or '42S02' in err_msg:
                logger.warning(
                    'WorkBreakReasons non trovata, uso query fallback senza motivazioni: %s',
                    err_msg
                )
                try:
                    parent_rows = self.db.fetch_all(QUERY_WORKBREAKS_FALLBACK)
                except Exception as e2:
                    logger.exception('Errore caricamento WorkBreaks padri (fallback)')
                    self._set_error_status(f'Errore caricamento WorkBreaks: {e2}')
                    messagebox.showerror(
                        self.L('error', 'Errore'),
                        f"{self.L('workbreaks_load_err', 'Errore caricamento regole')}:\n{e2}",
                        parent=self
                    )
                    parent_rows = []
            else:
                logger.exception('Errore caricamento WorkBreaks padri')
                self._set_error_status(f'Errore caricamento WorkBreaks: {e}')
                messagebox.showerror(
                    self.L('error', 'Errore'),
                    f"{self.L('workbreaks_load_err', 'Errore caricamento regole')}:\n{e}",
                    parent=self
                )
                parent_rows = []

        parent_ids = [r[0] for r in parent_rows]

        # Carica figli CDC filtrati per i padri in memoria
        t0 = time.monotonic()
        cdc_rows = self._fetch_children(QUERY_CDC_CHILDREN, parent_ids)
        for wb_id, cdc_id, desc in cdc_rows:
            self._cdc_by_parent.setdefault(wb_id, {})[cdc_id] = desc or ''
        logger.info('Figli CDC caricati in %.3fs: %d righe', time.monotonic() - t0, len(cdc_rows))

        # Carica figli Sub CDC filtrati per i padri in memoria
        t0 = time.monotonic()
        sub_rows = self._fetch_children(QUERY_SUBCDC_CHILDREN, parent_ids)
        for wb_id, sub_id, desc in sub_rows:
            self._subcdc_by_parent.setdefault(wb_id, {})[sub_id] = desc or ''
        logger.info('Figli SubCDC caricati in %.3fs: %d righe', time.monotonic() - t0, len(sub_rows))

        # Carica figli Funzioni filtrati per i padri in memoria
        t0 = time.monotonic()
        func_rows = self._fetch_children(QUERY_FUNCTION_CHILDREN, parent_ids)
        for wb_id, func_id, desc in func_rows:
            self._functions_by_parent.setdefault(wb_id, {})[func_id] = desc or ''
        logger.info('Figli Funzioni caricati in %.3fs: %d righe', time.monotonic() - t0, len(func_rows))

        records = []
        for r in parent_rows:
            rec = {
                'WorkBreakId': r[0],
                'IsForChangeShift': bool(r[1]),
                'Shift': r[2] or '',
                'FromTime': self._format_time(r[3]),
                'ToTime': self._format_time(r[4]),
                'SoundLoaded': bool(r[5]),
                'TextLoaded': bool(r[6]),
                'EmployeerId': r[7],
                'EmployeerName': r[8] or '',
                'WorkBreakReasonId': r[9],
                'ReasonDescription': r[10] or '',
            }
            iid = str(rec['WorkBreakId'])
            self._rows[iid] = rec
            records.append(rec)

        self._apply_sort(records)

        count = len(self._rows)
        self.status_var.set(
            f"{count} {self.L('workbreaks_loaded', 'regole attive')}"
        )
        logger.info(
            'Caricate %d regole attive in %.3fs',
            count, time.monotonic() - start_ts
        )

    def _format_time(self, value):
        """Formatta un valore orario letto dal DB (stringa HH:MM) per l'UI."""
        if value is None:
            return ''
        if isinstance(value, datetime.datetime):
            return value.strftime('%H:%M')
        if isinstance(value, datetime.time):
            return value.strftime('%H:%M')
        if isinstance(value, str):
            return value[:5]
        return str(value)

    def _format_time_str(self, t):
        """Formatta un oggetto datetime.time in stringa HH:MM per il DB."""
        if t is None:
            return ''
        return t.strftime('%H:%M')

    def _fetch_children(self, base_query, parent_ids):
        """
        Esegue una query figlia filtrando solo per i WorkBreakId dei padri caricati.
        Se parent_ids e' vuoto restituisce una lista vuota senza interrogare il DB.
        """
        if not parent_ids:
            return []
        placeholders = ','.join('?' * len(parent_ids))
        query = base_query.format(placeholders=placeholders)
        try:
            return self.db.fetch_all(query, parent_ids)
        except Exception as e:
            logger.exception('Errore caricamento figli con query filtrata')
            self._set_error_status(f'Errore caricamento figli: {e}')
            return []

    def _on_heading_click(self, col):
        """Gestisce il click sull'intestazione di colonna per ordinare."""
        if self._sort_col == col:
            self._sort_dir = 'desc' if self._sort_dir == 'asc' else 'asc'
        else:
            self._sort_col = col
            self._sort_dir = 'asc'
        logger.info('Ordinamento: col=%s dir=%s', self._sort_col, self._sort_dir)
        self._apply_sort()

    def _apply_sort(self, records=None):
        """Popola l'albero applicando l'ordinamento corrente."""
        if records is None:
            records = list(self._rows.values())
        if self._sort_col:
            reverse = self._sort_dir == 'desc'
            key_func = self._sort_keys.get(self._sort_col)
            if key_func:
                try:
                    records = sorted(records, key=key_func, reverse=reverse)
                except Exception as e:
                    logger.exception('Errore ordinamento colonna %s', self._sort_col)
        self._populate_tree(records)
        self._update_heading_arrows()

    def _populate_tree(self, records):
        """Inserisce i record nell'albero."""
        self.tree.delete(*self.tree.get_children())
        for rec in records:
            cdc_map = self._cdc_by_parent.get(rec['WorkBreakId'], {})
            subcdc_map = self._subcdc_by_parent.get(rec['WorkBreakId'], {})
            func_map = self._functions_by_parent.get(rec['WorkBreakId'], {})
            iid = str(rec['WorkBreakId'])
            self.tree.insert(
                '', 'end',
                iid=iid,
                values=(
                    self._join_names(cdc_map, 25),
                    self._join_names(subcdc_map, 25),
                    self._join_names(func_map, 25),
                    rec['Shift'],
                    rec['FromTime'],
                    rec['ToTime'],
                    self._bool_mark(rec['TextLoaded']),
                    self._bool_mark(rec['SoundLoaded']),
                    self._bool_mark(rec['IsForChangeShift']),
                    rec['EmployeerName'],
                    rec['ReasonDescription'],
                )
            )

    def _update_heading_arrows(self):
        """Aggiorna le frecce nelle intestazioni per indicare la colonna ordinata."""
        arrow = ' ▲' if self._sort_dir == 'asc' else ' ▼'
        for col, base_text in self._heading_texts.items():
            if col == self._sort_col:
                self.tree.heading(col, text=base_text + arrow)
            else:
                self.tree.heading(col, text=base_text)

    def _set_error_status(self, message):
        """Mostra il messaggio di errore nella barra di stato."""
        self.status_var.set(message)
        logger.error(message)

    def _bool_mark(self, value):
        return '✓' if value else ''

    def _join_names(self, name_map, max_len=25):
        if not name_map:
            return ''
        names = list(name_map.values())
        text = ', '.join(names)
        if len(text) > max_len:
            text = text[:max_len - 3] + '...'
        return text

    def _find_employer_display(self, name):
        """Restituisce il display name dell'azienda cercando per nome case-insensitive."""
        name_clean = name.strip().lower()
        for display in self._employers.keys():
            if display.strip().lower() == name_clean:
                return display
        return None

    def _on_tree_motion(self, event):
        """Mostra un tooltip con il testo completo quando il mouse e' su una cella troncata."""
        region = self.tree.identify_region(event.x, event.y)
        if region != 'cell':
            self._hide_tooltip()
            return

        col = self.tree.identify_column(event.x)
        col_id = self.tree.column(col, 'id')
        item = self.tree.identify_row(event.y)
        if not item or col_id not in ('cdc', 'subcdc', 'functions'):
            self._hide_tooltip()
            return

        rec = self._rows.get(item)
        if not rec:
            self._hide_tooltip()
            return

        if col_id == 'subcdc':
            text = self._join_names(self._subcdc_by_parent.get(rec['WorkBreakId'], {}), 9999)
        elif col_id == 'cdc':
            text = self._join_names(self._cdc_by_parent.get(rec['WorkBreakId'], {}), 9999)
        else:
            text = self._join_names(self._functions_by_parent.get(rec['WorkBreakId'], {}), 9999)

        if not text:
            self._hide_tooltip()
            return

        self._show_tooltip(event.x_root + 15, event.y_root + 10, text)

    def _show_tooltip(self, x, y, text):
        """Crea o aggiorna la finestra tooltip."""
        if self._tooltip is not None:
            if getattr(self._tooltip, '_text', None) == text:
                return
            self._tooltip.destroy()
        self._tooltip = tk.Toplevel(self)
        self._tooltip.wm_overrideredirect(True)
        self._tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self._tooltip,
            text=text,
            background='#ffffe0',
            relief='solid',
            borderwidth=1,
            justify='left',
            wraplength=400,
            padx=4,
            pady=2
        )
        label.pack()
        self._tooltip._text = text

    def _hide_tooltip(self):
        """Nasconde il tooltip."""
        if self._tooltip is not None:
            self._tooltip.destroy()
            self._tooltip = None

    def _on_tree_leave(self, event=None):
        """Nasconde il tooltip quando il mouse esce dalla treeview."""
        self._hide_tooltip()

    # ------------------------------------------------------------------
    # Form
    # ------------------------------------------------------------------
    def _on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        rec = self._rows.get(sel[0])
        if not rec:
            return

        self._loading_form = True

        # Seleziona CDC figli
        cdc_ids = set(self._cdc_by_parent.get(rec['WorkBreakId'], {}).keys())
        self.cdc_list.selection_clear(0, 'end')
        for idx, (cid, _) in enumerate(self._cdc_items):
            if cid in cdc_ids:
                self.cdc_list.selection_set(idx)

        self.shift_var.set(rec['Shift'])
        self.from_var.set(rec['FromTime'])
        self.to_var.set(rec['ToTime'])

        # Carica i blob solo quando serve (selezione di una riga)
        try:
            t0 = time.monotonic()
            blob_row = self.db.fetch_one(QUERY_WORKBREAK_BLOB, (rec['WorkBreakId'],))
            if blob_row:
                self._sound_bytes = blob_row[0] if blob_row[0] is not None else b''
                self._text_bytes = blob_row[1] if blob_row[1] is not None else b''
            else:
                self._sound_bytes = b''
                self._text_bytes = b''
            logger.info(
                'Blob WorkBreakId=%s caricati in %.3fs (sound=%d bytes, text=%d bytes)',
                rec['WorkBreakId'], time.monotonic() - t0,
                len(self._sound_bytes), len(self._text_bytes)
            )
        except Exception as e:
            logger.exception('Errore caricamento blob WorkBreakId=%s', rec['WorkBreakId'])
            self._sound_bytes = b''
            self._text_bytes = b''

        self._text_changed = False
        self._sound_changed = False
        loaded_text = self.L('workbreaks_file_loaded', '<file caricato>')
        self.text_var.set(loaded_text if self._text_bytes else '')
        self.sound_var.set(loaded_text if self._sound_bytes else '')
        self.change_shift_var.set(1 if rec['IsForChangeShift'] else 0)
        self._set_combo_by_id(self.employer_var, self._employers, rec['EmployeerId'])
        self._set_combo_by_id(self.reason_var, self._reasons, rec['WorkBreakReasonId'])

        # Seleziona Sub CDC figli
        sub_ids = set(self._subcdc_by_parent.get(rec['WorkBreakId'], {}).keys())
        self.sub_cdc_list.selection_clear(0, 'end')
        for idx, (sid, _) in enumerate(self._sub_cdc_items):
            if sid in sub_ids:
                self.sub_cdc_list.selection_set(idx)

        # Seleziona le Funzioni figlie
        func_ids = set(self._functions_by_parent.get(rec['WorkBreakId'], {}).keys())
        self.function_list.selection_clear(0, 'end')
        for idx, (fid, _) in enumerate(self._functions):
            if fid in func_ids:
                self.function_list.selection_set(idx)

        self._loading_form = False

    def _set_combo_by_id(self, var, mapping, lookup_id):
        var.set('')
        if lookup_id is None:
            return
        for display, pk in mapping.items():
            if pk == lookup_id:
                var.set(display)
                break

    def _on_new(self):
        self.tree.selection_remove(*self.tree.selection())
        self._clear_form()
        default_employer = self._find_employer_display(DEFAULT_EMPLOYER_NAME)
        if default_employer:
            self.employer_var.set(default_employer)
            logger.debug('Azienda di default impostata: %s', default_employer)
        else:
            logger.warning('Azienda di default non trovata: %s', DEFAULT_EMPLOYER_NAME)

    def _clear_form(self):
        self._loading_form = True

        self.cdc_list.selection_clear(0, 'end')
        self.shift_var.set('')
        self.from_var.set('')
        self.to_var.set('')
        self.text_var.set('')
        self.sound_var.set('')
        self.change_shift_var.set(0)
        self.employer_var.set('')
        self.reason_var.set('')
        self.sub_cdc_list.selection_clear(0, 'end')
        self.function_list.selection_clear(0, 'end')
        self._text_bytes = b''
        self._sound_bytes = b''
        self._text_changed = False
        self._sound_changed = False

        self._loading_form = False

    def _on_change_shift_toggle(self, *args):
        """Cambia le etichette orarie per i cambi turno."""
        if self.change_shift_var.get():
            self.from_label.configure(
                text=self.L('workbreaks_label_new_shift_start', 'Inizio nuovo turno (HH:MM):')
            )
            self.to_label.configure(
                text=self.L('workbreaks_label_grace_time', 'Tempo di grazia (HH:MM):')
            )
        else:
            self.from_label.configure(
                text=self.L('workbreaks_label_from', 'Dalle (HH:MM):')
            )
            self.to_label.configure(
                text=self.L('workbreaks_label_to', 'Alle (HH:MM):')
            )



    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------
    def _on_text_var_changed(self, *args):
        if self._loading_form:
            return
        path = self.text_var.get().strip()
        loaded_marker = self.L('workbreaks_file_loaded', '<file caricato>')
        if path == loaded_marker:
            return
        self._text_changed = True
        if not path:
            self._text_bytes = b''
            return
        self._text_bytes = self._read_file_bytes(path)

    def _on_sound_var_changed(self, *args):
        if self._loading_form:
            return
        path = self.sound_var.get().strip()
        loaded_marker = self.L('workbreaks_file_loaded', '<file caricato>')
        if path == loaded_marker:
            return
        self._sound_changed = True
        if not path:
            self._sound_bytes = b''
            return
        self._sound_bytes = self._read_file_bytes(path)

    def _read_file_bytes(self, path):
        if not path:
            return b''
        try:
            with open(path, 'rb') as f:
                data = f.read()
            logger.debug('Letto file %s: %d bytes', path, len(data))
            return data
        except Exception as e:
            logger.exception('Errore lettura file %s', path)
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('workbreaks_file_read_err', 'Errore lettura file')}:\n{e}",
                parent=self
            )
            return b''

    def _browse_document(self):
        path = filedialog.askopenfilename(
            parent=self,
            title=self.L('workbreaks_browse_doc_title', 'Seleziona documento'),
            filetypes=[
                (self.L('workbreaks_pdf_files', 'PDF'), '*.pdf'),
                (self.L('workbreaks_all_files', 'Tutti i file'), '*.*')
            ]
        )
        if path:
            self.text_var.set(path)
            self._text_changed = True
            self._text_bytes = self._read_file_bytes(path)

    def _browse_sound(self):
        path = filedialog.askopenfilename(
            parent=self,
            title=self.L('workbreaks_browse_sound_title', 'Seleziona file audio'),
            filetypes=[
                (self.L('workbreaks_audio_files', 'Audio'), '*.mp3 *.wav *.ogg'),
                (self.L('workbreaks_all_files', 'Tutti i file'), '*.*')
            ]
        )
        if path:
            self.sound_var.set(path)
            self._sound_changed = True
            self._sound_bytes = self._read_file_bytes(path)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_selected_cdc_ids(self):
        indices = self.cdc_list.curselection()
        return [self._cdc_items[i][0] for i in indices]

    def _get_selected_subcdc_ids(self):
        indices = self.sub_cdc_list.curselection()
        return [self._sub_cdc_items[i][0] for i in indices]

    def _get_selected_function_ids(self):
        indices = self.function_list.curselection()
        return [self._functions[i][0] for i in indices]

    def _parse_time(self, value, field_name):
        value = (value or '').strip()
        if not value:
            raise ValueError(f"{field_name} {self.L('workbreaks_required', 'obbligatorio')}")
        parts = value.split(':')
        if len(parts) != 2:
            raise ValueError(f"{field_name}: {self.L('workbreaks_time_format', 'formato HH:MM non valido')}")
        try:
            hour = int(parts[0])
            minute = int(parts[1])
        except ValueError:
            raise ValueError(f"{field_name}: {self.L('workbreaks_time_format', 'formato HH:MM non valido')}")
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            raise ValueError(f"{field_name}: {self.L('workbreaks_time_range', 'ora fuori range')}")
        return f"{hour:02d}:{minute:02d}"

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def _on_save(self):
        logger.info('Salvataggio regola WorkBreaks avviato')
        try:
            cdc_ids = self._get_selected_cdc_ids()
            if not cdc_ids:
                messagebox.showwarning(
                    self.L('warning', 'Attenzione'),
                    self.L('workbreaks_err_cdc_required', 'Selezionare almeno un CDC.'),
                    parent=self
                )
                return

            employer_name = self.employer_var.get().strip()
            employer_id = self._employers.get(employer_name)
            if not employer_id:
                messagebox.showwarning(
                    self.L('warning', 'Attenzione'),
                    self.L('workbreaks_err_employer_required', "Selezionare l'azienda."),
                    parent=self
                )
                return

            reason_name = self.reason_var.get().strip()
            reason_id = self._reasons.get(reason_name)

            shift = self.shift_var.get().strip()
            if not shift:
                messagebox.showwarning(
                    self.L('warning', 'Attenzione'),
                    self.L('workbreaks_err_shift_required', 'Indicare il turno.'),
                    parent=self
                )
                return

            is_change = bool(self.change_shift_var.get())
            from_time = self._parse_time(self.from_var.get(), self.L('workbreaks_label_from', 'Dalle'))
            to_time = self._parse_time(self.to_var.get(), self.L('workbreaks_label_to', 'Alle'))

            subcdc_ids = self._get_selected_subcdc_ids()
            func_ids = self._get_selected_function_ids()

            parent_cdc = cdc_ids[0]
            parent_subcdc = subcdc_ids[0] if subcdc_ids else None
            parent_function = func_ids[0] if func_ids else None

            text_bytes = self._text_bytes
            sound_bytes = self._sound_bytes

            selected_iid = self.tree.selection()
            workbreak_id = int(selected_iid[0]) if selected_iid else None

            if workbreak_id is None:
                params = (
                    1 if is_change else 0,
                    parent_cdc,
                    parent_subcdc,
                    shift,
                    from_time,
                    to_time,
                    parent_function,
                    sound_bytes,
                    text_bytes,
                    employer_id,
                    reason_id
                )
                new_id = self.db.execute_insert_returning(QUERY_INSERT_WORKBREAK, params)
                if new_id is None:
                    err = getattr(self.db, 'last_error_details', 'unknown')
                    logger.error('INSERT WorkBreaks fallito: %s', err)
                    messagebox.showerror(
                        self.L('error', 'Errore'),
                        f"{self.L('workbreaks_save_err', 'Errore durante il salvataggio.')}:\n{err}",
                        parent=self
                    )
                    return
                logger.info('WorkBreaks inserito con ID %s', new_id)
                self._insert_children(new_id, cdc_ids, subcdc_ids, func_ids)
            else:
                params = (
                    1 if is_change else 0,
                    parent_cdc,
                    parent_subcdc,
                    shift,
                    from_time,
                    to_time,
                    parent_function,
                    sound_bytes,
                    text_bytes,
                    employer_id,
                    reason_id,
                    workbreak_id
                )
                if not self.db.execute_query(QUERY_UPDATE_WORKBREAK, params):
                    err = getattr(self.db, 'last_error_details', 'unknown')
                    logger.error('UPDATE WorkBreaks fallito: %s', err)
                    messagebox.showerror(
                        self.L('error', 'Errore'),
                        f"{self.L('workbreaks_save_err', 'Errore durante il salvataggio.')}:\n{err}",
                        parent=self
                    )
                    return
                logger.info('WorkBreaks aggiornato ID %s', workbreak_id)
                if not self.db.execute_query(QUERY_CLOSE_WORKBREAK_DATA, (workbreak_id,)):
                    err = getattr(self.db, 'last_error_details', 'unknown')
                    logger.error('Chiusura figli WorkBreakData fallita: %s', err)
                    messagebox.showerror(
                        self.L('error', 'Errore'),
                        f"{self.L('workbreaks_save_err', 'Errore durante il salvataggio.')}:\n{err}",
                        parent=self
                    )
                    return
                self._insert_children(workbreak_id, cdc_ids, subcdc_ids, func_ids)

            self._load_data()
            self._clear_form()
            self.status_var.set(self.L('workbreaks_saved', 'Regola salvata.'))
            logger.info('Salvataggio WorkBreaks completato')

        except Exception as e:
            logger.exception('Errore salvataggio WorkBreaks')
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('workbreaks_save_err', 'Errore durante il salvataggio.')}:\n{e}",
                parent=self
            )

    def _insert_children(self, workbreak_id, cdc_ids, subcdc_ids, func_ids):
        sub_ids = subcdc_ids or [None]
        f_ids = func_ids or [None]
        combos = list(itertools.product(cdc_ids, sub_ids, f_ids))
        logger.info('Inserimento %d combinazioni CDC/SubCDC/Funzione per WorkBreakId=%s', len(combos), workbreak_id)
        for cdc, sub, func in combos:
            params = (workbreak_id, cdc, sub, func)
            if not self.db.execute_query(QUERY_INSERT_WORKBREAK_DATA, params):
                err = getattr(self.db, 'last_error_details', 'unknown')
                logger.error('INSERT WorkBreakData fallito: %s', err)
                raise RuntimeError(f"Errore inserimento dettaglio WorkBreakData: {err}")

    def _on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.L('warning', 'Attenzione'),
                self.L('workbreaks_err_select_to_delete', 'Selezionare una regola da eliminare.'),
                parent=self
            )
            return
        workbreak_id = int(sel[0])
        rec = self._rows.get(sel[0])
        desc = f"{rec.get('FromTime', '')} - {rec.get('ToTime', '')}" if rec else str(workbreak_id)
        if not messagebox.askyesno(
            self.L('confirm', 'Conferma'),
            self.L('workbreaks_confirm_delete', f'Eliminare la regola {desc}?'),
            parent=self
        ):
            return
        logger.info('Eliminazione WorkBreakId=%s', workbreak_id)
        if not self.db.execute_query(QUERY_DELETE_WORKBREAK_DATA, (workbreak_id,)):
            err = getattr(self.db, 'last_error_details', 'unknown')
            logger.error('Eliminazione figli WorkBreakData fallita: %s', err)
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('workbreaks_delete_err', 'Errore eliminazione.')}:\n{err}",
                parent=self
            )
            return
        if not self.db.execute_query(QUERY_DELETE_WORKBREAK, (workbreak_id,)):
            err = getattr(self.db, 'last_error_details', 'unknown')
            logger.error('Eliminazione WorkBreaks fallita: %s', err)
            messagebox.showerror(
                self.L('error', 'Errore'),
                f"{self.L('workbreaks_delete_err', 'Errore eliminazione.')}:\n{err}",
                parent=self
            )
            return
        self._load_data()
        self._clear_form()
        self.status_var.set(self.L('workbreaks_deleted', 'Regola eliminata.'))
        logger.info('WorkBreakId=%s eliminato', workbreak_id)


# ------------------------------------------------------------------
# Query per salvataggio / modifica / eliminazione
# ------------------------------------------------------------------
QUERY_INSERT_WORKBREAK = """
INSERT INTO Employee.dbo.WorkBreaks (
    IsForChangeShift, IdCdc, IdSubCdc, Shift, FromTime, ToTime, functionId,
    Sound, TextToshow, DateIn, EmployeerId, WorkBreakReasonId
)
OUTPUT inserted.WorkBreakId
VALUES (
    ?, ?, ?, ?, ?, ?, ?,
    CONVERT(VARBINARY(MAX), ?),
    CONVERT(VARBINARY(MAX), ?),
    GETDATE(), ?, ?
)
"""

QUERY_UPDATE_WORKBREAK = """
UPDATE Employee.dbo.WorkBreaks
SET IsForChangeShift = ?,
    IdCdc = ?,
    IdSubCdc = ?,
    Shift = ?,
    FromTime = ?,
    ToTime = ?,
    functionId = ?,
    Sound = CONVERT(VARBINARY(MAX), ?),
    TextToshow = CONVERT(VARBINARY(MAX), ?),
    EmployeerId = ?,
    WorkBreakReasonId = ?
WHERE WorkBreakId = ?
"""

QUERY_CLOSE_WORKBREAK_DATA = """
UPDATE Employee.dbo.WorkBreakData
SET DateOut = GETDATE()
WHERE WorkBreakId = ? AND DateOut IS NULL
"""

QUERY_INSERT_WORKBREAK_DATA = """
INSERT INTO Employee.dbo.WorkBreakData (WorkBreakId, CdcId, SubCdcId, FunctionId, DateIn)
VALUES (?, ?, ?, ?, GETDATE())
"""

QUERY_DELETE_WORKBREAK = """
UPDATE Employee.dbo.WorkBreaks
SET DateOut = GETDATE()
WHERE WorkBreakId = ?
"""

QUERY_DELETE_WORKBREAK_DATA = """
UPDATE Employee.dbo.WorkBreakData
SET DateOut = GETDATE()
WHERE WorkBreakId = ? AND DateOut IS NULL
"""
