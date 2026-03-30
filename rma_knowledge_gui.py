# File: rma_knowledge_gui.py
# GUI per la RMA Knowledge Base — Ricerca e Inserimento soluzioni

import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

logger = logging.getLogger(__name__)


class RmaKnowledgeBaseWindow(tk.Toplevel):
    """
    Finestra principale RMA Knowledge Base con due Tab:
    - Tab Ricerca: accesso libero per cercare soluzioni storiche
    - Tab Inserimento: protetto con _execute_authorized_action
    """

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.lang = lang
        self._rma_mgr = None

        self.title(self.lang.get('rma_kb_title', '🔧 RMA Knowledge Base'))
        self.geometry("1200x800")
        self.minsize(900, 600)
        self.transient(parent)

        # Manager lazy init
        self._init_manager()

        # Build UI
        self._build_ui()

        # Carica dati iniziali
        self._load_lookups()
        self._update_stats()

    # ══════════════════════════════════════════════════════════════════
    # Init manager
    # ══════════════════════════════════════════════════════════════════
    def _init_manager(self):
        try:
            from rma_manager import RmaManager
            self._rma_mgr = RmaManager(self.db)
            logger.info("RmaKnowledgeBaseWindow: RmaManager inizializzato.")
        except Exception as e:
            logger.error(f"Errore init RmaManager: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile inizializzare RMA Manager: {e}",
                parent=self
            )
            self.destroy()

    # ══════════════════════════════════════════════════════════════════
    # Build UI
    # ══════════════════════════════════════════════════════════════════
    def _build_ui(self):
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=8, pady=8)

        # Tab 1: Ricerca
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text=self.lang.get('rma_tab_search', '🔍 Ricerca Soluzioni'))
        self._build_search_tab()

        # Tab 2: Inserimento
        self.insert_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.insert_frame, text=self.lang.get('rma_tab_insert', '➕ Inserisci Soluzione'))
        self._build_insert_tab()

        # Bind tab change per autorizzazione
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    # ══════════════════════════════════════════════════════════════════
    # Tab RICERCA
    # ══════════════════════════════════════════════════════════════════
    def _build_search_tab(self):
        # --- Barra statistiche ---
        stats_frame = ttk.Frame(self.search_frame)
        stats_frame.pack(fill='x', padx=8, pady=(8, 4))

        self.stats_label = ttk.Label(stats_frame, text="", font=('Segoe UI', 9))
        self.stats_label.pack(side='left')

        # --- Frame filtri ---
        filters_frame = ttk.LabelFrame(
            self.search_frame,
            text=self.lang.get('rma_filters', 'Filtri (combinabili)')
        )
        filters_frame.pack(fill='x', padx=8, pady=4)

        # Riga 1
        r1 = ttk.Frame(filters_frame)
        r1.pack(fill='x', padx=8, pady=4)

        ttk.Label(r1, text=self.lang.get('rma_serial', 'Serial Number:')).pack(side='left', padx=(0, 4))
        self.search_serial_var = tk.StringVar()
        serial_entry = ttk.Entry(r1, textvariable=self.search_serial_var, width=20)
        serial_entry.pack(side='left', padx=(0, 16))

        ttk.Label(r1, text=self.lang.get('rma_part_code', 'Codice Parte:')).pack(side='left', padx=(0, 4))
        self.search_part_var = tk.StringVar()
        self.part_combo = ttk.Combobox(r1, textvariable=self.search_part_var, width=22, state='readonly')
        self.part_combo.pack(side='left', padx=(0, 16))

        ttk.Label(r1, text=self.lang.get('rma_customer', 'Cliente:')).pack(side='left', padx=(0, 4))
        self.search_customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(r1, textvariable=self.search_customer_var, width=22, state='readonly')
        self.customer_combo.pack(side='left')

        # Riga 2
        r2 = ttk.Frame(filters_frame)
        r2.pack(fill='x', padx=8, pady=4)

        ttk.Label(r2, text=self.lang.get('rma_fault_contains', 'Guasto contiene:')).pack(side='left', padx=(0, 4))
        self.search_fault_var = tk.StringVar()
        ttk.Entry(r2, textvariable=self.search_fault_var, width=20).pack(side='left', padx=(0, 16))

        ttk.Label(r2, text=self.lang.get('rma_fault_type', 'Tipo Guasto:')).pack(side='left', padx=(0, 4))
        self.search_ftype_var = tk.StringVar()
        self.ftype_combo = ttk.Combobox(r2, textvariable=self.search_ftype_var, width=22, state='readonly')
        self.ftype_combo.pack(side='left', padx=(0, 16))

        ttk.Label(r2, text=self.lang.get('rma_reference', 'Reference:')).pack(side='left', padx=(0, 4))
        self.search_ref_var = tk.StringVar()
        self.ref_combo = ttk.Combobox(r2, textvariable=self.search_ref_var, width=18, state='readonly')
        self.ref_combo.pack(side='left')

        # Riga 3: Bottoni
        r3 = ttk.Frame(filters_frame)
        r3.pack(fill='x', padx=8, pady=(4, 8))

        search_btn = ttk.Button(
            r3,
            text=self.lang.get('rma_search_btn', '🔎 Cerca'),
            command=self._do_search
        )
        search_btn.pack(side='left', padx=(0, 8))

        reset_btn = ttk.Button(
            r3,
            text=self.lang.get('rma_reset_btn', '🔄 Reset'),
            command=self._reset_filters
        )
        reset_btn.pack(side='left', padx=(0, 16))

        self.results_label = ttk.Label(r3, text="", font=('Segoe UI', 9, 'italic'))
        self.results_label.pack(side='left')

        # Bind Enter per ricerca
        serial_entry.bind('<Return>', lambda e: self._do_search())
        self.ftype_combo.bind('<<ComboboxSelected>>', self._on_ftype_changed)

        # --- TreeView risultati ---
        tree_frame = ttk.Frame(self.search_frame)
        tree_frame.pack(fill='both', expand=True, padx=8, pady=4)

        cols = ('serial', 'part', 'customer', 'fault', 'type', 'reference', 'date')
        self.result_tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=12)
        self.result_tree.heading('serial', text='Serial Number')
        self.result_tree.heading('part', text='Codice Parte')
        self.result_tree.heading('customer', text='Cliente')
        self.result_tree.heading('fault', text='Descrizione Guasto')
        self.result_tree.heading('type', text='Tipo Guasto')
        self.result_tree.heading('reference', text='Reference')
        self.result_tree.heading('date', text='Data Ordine')

        self.result_tree.column('serial', width=140)
        self.result_tree.column('part', width=150)
        self.result_tree.column('customer', width=120)
        self.result_tree.column('fault', width=250)
        self.result_tree.column('type', width=130)
        self.result_tree.column('reference', width=80)
        self.result_tree.column('date', width=90)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient='vertical', command=self.result_tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.result_tree.xview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.result_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.result_tree.bind('<<TreeviewSelect>>', self._on_result_select)

        # Mappa iid → record data
        self._result_data = {}

        # --- Pannello dettaglio ---
        self._build_detail_panel()

    def _build_detail_panel(self):
        """Pannello inferiore con i dettagli del record selezionato."""
        detail_frame = ttk.LabelFrame(
            self.search_frame,
            text=self.lang.get('rma_detail', '📋 Dettaglio Selezionato')
        )
        detail_frame.pack(fill='x', padx=8, pady=(4, 8))

        # Container con due colonne
        left = ttk.Frame(detail_frame)
        left.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        right = ttk.Frame(detail_frame)
        right.pack(side='left', fill='both', expand=True, padx=8, pady=8)

        # --- Colonna sinistra: Informazioni scheda ---
        self._detail_labels = {}

        def add_detail(parent, key, label_text, row, col=0, **kwargs):
            ttk.Label(parent, text=label_text, font=('Segoe UI', 9, 'bold')).grid(
                row=row, column=col, sticky='nw', padx=(0, 8), pady=2
            )
            val_label = ttk.Label(parent, text='', wraplength=400, font=('Segoe UI', 9))
            val_label.grid(row=row, column=col + 1, sticky='nw', pady=2)
            self._detail_labels[key] = val_label

        add_detail(left, 'serial', 'Serial:', 0)
        add_detail(left, 'part', 'Codice Parte:', 1)
        add_detail(left, 'part_desc', 'Descrizione:', 2)
        add_detail(left, 'customer', 'Cliente:', 3)
        add_detail(left, 'rma_num', 'N° RMA:', 4)

        # GUASTO (evidenziato in rosso)
        ttk.Separator(left, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', pady=4)
        fault_label = ttk.Label(left, text='🔴 GUASTO:', font=('Segoe UI', 9, 'bold'), foreground='#CC0000')
        fault_label.grid(row=6, column=0, sticky='nw', padx=(0, 8), pady=2)
        self._detail_labels['fault'] = ttk.Label(left, text='', wraplength=400, foreground='#CC0000',
                                                  font=('Segoe UI', 9))
        self._detail_labels['fault'].grid(row=6, column=1, sticky='nw', pady=2)

        add_detail(left, 'fault_type_detail', 'Tipo/Dettaglio:', 7)
        add_detail(left, 'ref_asm', 'Reference / Assembly:', 8)

        # SOLUZIONE (evidenziata in verde)
        ttk.Separator(left, orient='horizontal').grid(row=9, column=0, columnspan=2, sticky='ew', pady=4)
        sol_label = ttk.Label(left, text='🟢 SOLUZIONE:', font=('Segoe UI', 9, 'bold'), foreground='#008800')
        sol_label.grid(row=10, column=0, sticky='nw', padx=(0, 8), pady=2)
        self._detail_labels['solution'] = ttk.Label(left, text='', wraplength=400, foreground='#008800',
                                                     font=('Segoe UI', 9))
        self._detail_labels['solution'].grid(row=10, column=1, sticky='nw', pady=2)

        add_detail(left, 'corrective', 'Azione correttiva:', 11)
        add_detail(left, 'cause', 'Causa:', 12)

        # --- Colonna destra: Produzione e info ---
        add_detail(right, 'site', 'Sito prod.:', 0)
        add_detail(right, 'responsible', 'Resp. processo:', 1)
        add_detail(right, 'prod_week', 'Sett. produzione:', 2)
        add_detail(right, 'warranty', 'Garanzia:', 3)
        add_detail(right, 'repair_time', 'Tempo riparazione:', 4)
        add_detail(right, 'cost', 'Costo:', 5)
        add_detail(right, 'test', 'Test:', 6)
        add_detail(right, 'operator', 'Operatore:', 7)
        add_detail(right, 'already_rep', 'Già riparata:', 8)
        add_detail(right, 'origin', 'Origine:', 9)
        add_detail(right, 'source', 'Fonte:', 10)
        add_detail(right, 'product_code', 'Prodotto (trac.):', 11)

        # Bottone tracciabilità (visibile solo per SN con "TI")
        self._trace_btn = ttk.Button(
            right,
            text=self.lang.get('rma_open_traceability', '🔗 Apri Tracciabilità'),
            command=self._open_traceability
        )
        self._trace_btn.grid(row=12, column=0, columnspan=2, sticky='w', pady=(8, 0))
        self._trace_btn.grid_remove()  # nascosto di default

        left.grid_columnconfigure(1, weight=1)
        right.grid_columnconfigure(1, weight=1)

    # ══════════════════════════════════════════════════════════════════
    # Tab INSERIMENTO
    # ══════════════════════════════════════════════════════════════════
    def _build_insert_tab(self):
        # Il contenuto viene costruito solo dopo l'autorizzazione
        self._insert_authorized = False
        self._insert_content_built = False

        # Placeholder
        self._auth_placeholder = ttk.Label(
            self.insert_frame,
            text=self.lang.get('rma_auth_required',
                               '🔐 Accesso riservato. Effettuare il login per inserire nuove soluzioni.'),
            font=('Segoe UI', 12),
            anchor='center'
        )
        self._auth_placeholder.pack(fill='both', expand=True, pady=50)

    def _build_insert_form(self):
        """Costruisce il form di inserimento dopo l'autorizzazione."""
        if self._insert_content_built:
            return

        # Rimuovi il placeholder
        self._auth_placeholder.pack_forget()

        # Scrollable frame
        canvas = tk.Canvas(self.insert_frame)
        scrollbar = ttk.Scrollbar(self.insert_frame, orient='vertical', command=canvas.yview)
        form_frame = ttk.Frame(canvas)

        form_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=form_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        scrollbar.pack(side='right', fill='y')

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        row = 0

        # --- Sezione: Verifica etichetta ---
        lf_verify = ttk.LabelFrame(form_frame, text=self.lang.get('rma_verify_label', '📋 Verifica Etichetta'))
        lf_verify.grid(row=row, column=0, columnspan=4, sticky='ew', padx=8, pady=4)
        row += 1

        vr = 0
        ttk.Label(lf_verify, text='Serial Number *').grid(row=vr, column=0, sticky='w', padx=8, pady=4)
        self.ins_serial_var = tk.StringVar()
        serial_entry = ttk.Entry(lf_verify, textvariable=self.ins_serial_var, width=24)
        serial_entry.grid(row=vr, column=1, sticky='w', padx=4, pady=4)

        self.ins_verify_btn = ttk.Button(
            lf_verify,
            text=self.lang.get('rma_verify_btn', '✔ Verifica'),
            command=self._verify_serial
        )
        self.ins_verify_btn.grid(row=vr, column=2, padx=8, pady=4)

        self.ins_verify_status = ttk.Label(lf_verify, text='', font=('Segoe UI', 9))
        self.ins_verify_status.grid(row=vr, column=3, sticky='w', padx=8, pady=4)
        vr += 1

        # Info tracciabilità (readonly)
        ttk.Label(lf_verify, text='Ordine:').grid(row=vr, column=0, sticky='w', padx=8, pady=2)
        self.ins_order_var = tk.StringVar()
        ttk.Entry(lf_verify, textvariable=self.ins_order_var, state='readonly', width=20).grid(
            row=vr, column=1, sticky='w', padx=4, pady=2)
        ttk.Label(lf_verify, text='Prodotto:').grid(row=vr, column=2, sticky='w', padx=8, pady=2)
        self.ins_product_var = tk.StringVar()
        ttk.Entry(lf_verify, textvariable=self.ins_product_var, state='readonly', width=20).grid(
            row=vr, column=3, sticky='w', padx=4, pady=2)

        serial_entry.bind('<Return>', lambda e: self._verify_serial())

        # Variabili di tracciabilità interne
        self._ins_id_label_code = None
        self._ins_id_order = None
        self._ins_product_code = None

        # --- Sezione: Guasto ---
        lf_fault = ttk.LabelFrame(form_frame, text=self.lang.get('rma_fault_section', '🔴 Guasto'))
        lf_fault.grid(row=row, column=0, columnspan=4, sticky='ew', padx=8, pady=4)
        row += 1

        fr = 0
        ttk.Label(lf_fault, text=self.lang.get('rma_part_code', 'Codice Parte:')).grid(
            row=fr, column=0, sticky='w', padx=8, pady=4)
        self.ins_part_var = tk.StringVar()
        self.ins_part_combo = ttk.Combobox(lf_fault, textvariable=self.ins_part_var, width=24)
        self.ins_part_combo.grid(row=fr, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_fault, text=self.lang.get('rma_customer', 'Cliente:')).grid(
            row=fr, column=2, sticky='w', padx=8, pady=4)
        self.ins_customer_var = tk.StringVar()
        self.ins_customer_combo = ttk.Combobox(lf_fault, textvariable=self.ins_customer_var, width=24)
        self.ins_customer_combo.grid(row=fr, column=3, sticky='w', padx=4, pady=4)
        fr += 1

        ttk.Label(lf_fault, text=self.lang.get('rma_fault_desc', 'Descrizione Guasto:')).grid(
            row=fr, column=0, sticky='nw', padx=8, pady=4)
        self.ins_fault_desc = tk.Text(lf_fault, width=60, height=3, wrap='word')
        self.ins_fault_desc.grid(row=fr, column=1, columnspan=3, sticky='ew', padx=4, pady=4)
        fr += 1

        ttk.Label(lf_fault, text=self.lang.get('rma_fault_type', 'Tipo Guasto:')).grid(
            row=fr, column=0, sticky='w', padx=8, pady=4)
        self.ins_ftype_var = tk.StringVar()
        self.ins_ftype_combo = ttk.Combobox(lf_fault, textvariable=self.ins_ftype_var, width=24, state='readonly')
        self.ins_ftype_combo.grid(row=fr, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_fault, text=self.lang.get('rma_fault_detail', 'Dettaglio:')).grid(
            row=fr, column=2, sticky='w', padx=8, pady=4)
        self.ins_fdetail_var = tk.StringVar()
        self.ins_fdetail_combo = ttk.Combobox(lf_fault, textvariable=self.ins_fdetail_var, width=24, state='readonly')
        self.ins_fdetail_combo.grid(row=fr, column=3, sticky='w', padx=4, pady=4)
        fr += 1

        self.ins_ftype_combo.bind('<<ComboboxSelected>>', self._on_ins_ftype_changed)

        ttk.Label(lf_fault, text=self.lang.get('rma_reference', 'Reference:')).grid(
            row=fr, column=0, sticky='w', padx=8, pady=4)
        self.ins_ref_var = tk.StringVar()
        self.ins_ref_combo = ttk.Combobox(lf_fault, textvariable=self.ins_ref_var, width=24)
        self.ins_ref_combo.grid(row=fr, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_fault, text='Assembly:').grid(row=fr, column=2, sticky='w', padx=8, pady=4)
        self.ins_assembly_var = tk.StringVar()
        self.ins_assembly_combo = ttk.Combobox(lf_fault, textvariable=self.ins_assembly_var, width=24)
        self.ins_assembly_combo.grid(row=fr, column=3, sticky='w', padx=4, pady=4)

        # --- Sezione: Soluzione ---
        lf_solution = ttk.LabelFrame(form_frame, text=self.lang.get('rma_solution_section', '🟢 Soluzione'))
        lf_solution.grid(row=row, column=0, columnspan=4, sticky='ew', padx=8, pady=4)
        row += 1

        sr = 0
        ttk.Label(lf_solution, text=self.lang.get('rma_fault_notes', 'Note Guasto / Soluzione *:')).grid(
            row=sr, column=0, sticky='nw', padx=8, pady=4)
        self.ins_fault_notes = tk.Text(lf_solution, width=60, height=4, wrap='word')
        self.ins_fault_notes.grid(row=sr, column=1, columnspan=3, sticky='ew', padx=4, pady=4)
        sr += 1

        ttk.Label(lf_solution, text=self.lang.get('rma_corrective', 'Azione correttiva:')).grid(
            row=sr, column=0, sticky='nw', padx=8, pady=4)
        self.ins_corrective = tk.Text(lf_solution, width=60, height=3, wrap='word')
        self.ins_corrective.grid(row=sr, column=1, columnspan=3, sticky='ew', padx=4, pady=4)
        sr += 1

        ttk.Label(lf_solution, text=self.lang.get('rma_cause_code', 'Codice Causa:')).grid(
            row=sr, column=0, sticky='w', padx=8, pady=4)
        self.ins_cause_code_var = tk.StringVar()
        cause_combo = ttk.Combobox(lf_solution, textvariable=self.ins_cause_code_var, width=14, state='readonly',
                                   values=['', 'FC01', 'FC02', 'FC03', 'FC04'])
        cause_combo.grid(row=sr, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_solution, text=self.lang.get('rma_cause_text', 'Causa (testo):')).grid(
            row=sr, column=2, sticky='w', padx=8, pady=4)
        self.ins_cause_text_var = tk.StringVar()
        ttk.Entry(lf_solution, textvariable=self.ins_cause_text_var, width=24).grid(
            row=sr, column=3, sticky='w', padx=4, pady=4)

        # --- Sezione: Produzione & Extra ---
        lf_extra = ttk.LabelFrame(form_frame, text=self.lang.get('rma_extra_section', '📊 Produzione'))
        lf_extra.grid(row=row, column=0, columnspan=4, sticky='ew', padx=8, pady=4)
        row += 1

        er = 0
        ttk.Label(lf_extra, text=self.lang.get('rma_warranty', 'Garanzia:')).grid(
            row=er, column=0, sticky='w', padx=8, pady=4)
        self.ins_warranty_var = tk.StringVar()
        ttk.Combobox(lf_extra, textvariable=self.ins_warranty_var, width=14, state='readonly',
                     values=['', 'Warranty YES', 'Warranty NO', 'Scrap']).grid(
            row=er, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_extra, text=self.lang.get('rma_site', 'Sito Produzione:')).grid(
            row=er, column=2, sticky='w', padx=8, pady=4)
        self.ins_site_var = tk.StringVar()
        self.ins_site_combo = ttk.Combobox(lf_extra, textvariable=self.ins_site_var, width=20, state='readonly')
        self.ins_site_combo.grid(row=er, column=3, sticky='w', padx=4, pady=4)
        er += 1

        ttk.Label(lf_extra, text=self.lang.get('rma_resp', 'Resp. Processo:')).grid(
            row=er, column=0, sticky='w', padx=8, pady=4)
        self.ins_resp_var = tk.StringVar()
        ttk.Entry(lf_extra, textvariable=self.ins_resp_var, width=24).grid(
            row=er, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(lf_extra, text=self.lang.get('rma_repair_time', 'Tempo (min):')).grid(
            row=er, column=2, sticky='w', padx=8, pady=4)
        self.ins_time_var = tk.StringVar()
        ttk.Spinbox(lf_extra, textvariable=self.ins_time_var, from_=0, to=9999, width=8).grid(
            row=er, column=3, sticky='w', padx=4, pady=4)

        # --- Sezione: Allegati ---
        lf_attach = ttk.LabelFrame(form_frame, text=self.lang.get('rma_attach_section', '📎 Allegati'))
        lf_attach.grid(row=row, column=0, columnspan=4, sticky='ew', padx=8, pady=4)
        row += 1

        ar = 0
        ttk.Label(lf_attach, text=self.lang.get('rma_photo', 'Foto difetto:')).grid(
            row=ar, column=0, sticky='w', padx=8, pady=4)
        self.ins_photo_var = tk.StringVar()
        ttk.Entry(lf_attach, textvariable=self.ins_photo_var, width=40, state='readonly').grid(
            row=ar, column=1, columnspan=2, sticky='w', padx=4, pady=4)
        ttk.Button(lf_attach, text=self.lang.get('rma_browse', '📂 Sfoglia'),
                   command=self._browse_photo).grid(row=ar, column=3, padx=8, pady=4)
        ar += 1

        ttk.Label(lf_attach, text=self.lang.get('rma_doc_links', 'Link documenti:')).grid(
            row=ar, column=0, sticky='nw', padx=8, pady=4)
        self.ins_doc_links = tk.Text(lf_attach, width=60, height=2, wrap='word')
        self.ins_doc_links.grid(row=ar, column=1, columnspan=3, sticky='ew', padx=4, pady=4)

        # --- Bottoni ---
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row, column=0, columnspan=4, sticky='e', padx=8, pady=(12, 8))

        ttk.Button(btn_frame, text=self.lang.get('rma_save', '💾 Salva'),
                   command=self._do_save).pack(side='right', padx=8)
        ttk.Button(btn_frame, text=self.lang.get('rma_clear', '🧹 Pulisci'),
                   command=self._clear_insert_form).pack(side='right', padx=8)

        # Popola combobox inserimento
        self._populate_insert_combos()
        self._insert_content_built = True

    # ══════════════════════════════════════════════════════════════════
    # Caricamento lookup e statistiche
    # ══════════════════════════════════════════════════════════════════
    def _load_lookups(self):
        """Carica i dati per le combobox di ricerca."""
        if not self._rma_mgr:
            return

        # Codici parte
        parts = [''] + self._rma_mgr.get_distinct_part_codes()
        self.part_combo['values'] = parts

        # Clienti
        customers = [''] + self._rma_mgr.get_distinct_customers()
        self.customer_combo['values'] = customers

        # Tipi guasto
        self._fault_types = self._rma_mgr.get_fault_types()
        ftype_names = [''] + [f"{ft.Code} - {ft.Description}" for ft in self._fault_types]
        self.ftype_combo['values'] = ftype_names
        self._ftype_map = {f"{ft.Code} - {ft.Description}": ft.RmaFaultTypeId for ft in self._fault_types}

        # Reference
        refs = [''] + self._rma_mgr.get_distinct_references()
        self.ref_combo['values'] = refs

        # Fault details (tutti)
        self._all_fault_details = self._rma_mgr.get_fault_details()

    def _update_stats(self):
        """Aggiorna le statistiche in alto."""
        if not self._rma_mgr:
            return
        stats = self._rma_mgr.get_statistics()
        text = (
            f"📊 Totale record: {stats['total']:,} | "
            f"Con soluzione: {stats['with_solution']:,} | "
            f"Seriali unici: {stats['unique_serials']:,} | "
            f"Codici parte: {stats['unique_parts']}"
        )
        self.stats_label.config(text=text)

    def _populate_insert_combos(self):
        """Popola le combobox del form di inserimento."""
        if not self._rma_mgr:
            return

        # Codici parte (inserimento libero)
        self.ins_part_combo['values'] = self._rma_mgr.get_distinct_part_codes()

        # Clienti (inserimento libero)
        self.ins_customer_combo['values'] = self._rma_mgr.get_distinct_customers()

        # Tipi guasto
        ftype_names = [''] + [f"{ft.Code} - {ft.Description}" for ft in self._fault_types]
        self.ins_ftype_combo['values'] = ftype_names

        # Reference (autocomplete)
        self.ins_ref_combo['values'] = self._rma_mgr.get_distinct_references()

        # Assembly (autocomplete)
        self.ins_assembly_combo['values'] = self._rma_mgr.get_distinct_assemblies()

        # Siti produzione
        sites = self._rma_mgr.get_production_sites()
        site_names = [''] + [s.Name for s in sites]
        self.ins_site_combo['values'] = site_names
        self._site_map = {s.Name: s.RmaProductionSiteId for s in sites}

    # ══════════════════════════════════════════════════════════════════
    # Eventi tab
    # ══════════════════════════════════════════════════════════════════
    def _on_tab_changed(self, event=None):
        """Quando l'utente clicca sul tab Inserimento, verifica autorizzazione."""
        selected = self.notebook.index(self.notebook.select())
        if selected == 1 and not self._insert_authorized:
            # Tab inserimento - richiedi autorizzazione
            self._request_insert_auth()

    def _request_insert_auth(self):
        """Richiede autorizzazione per il tab inserimento."""
        try:
            app = self.parent
            result = app._execute_authorized_action(
                'aggiungi_rma_soluzioni',
                self._on_insert_authorized
            )
            if not result:
                # Non autorizzato - torna al tab ricerca
                self.notebook.select(0)
        except Exception as e:
            logger.error(f"Errore autorizzazione RMA: {e}", exc_info=True)
            self.notebook.select(0)

    def _on_insert_authorized(self):
        """Callback dopo autorizzazione riuscita."""
        self._insert_authorized = True
        self._build_insert_form()
        logger.info("RMA tab inserimento autorizzato e costruito.")

    # ══════════════════════════════════════════════════════════════════
    # Ricerca
    # ══════════════════════════════════════════════════════════════════
    def _do_search(self):
        """Esegue la ricerca con i filtri impostati."""
        if not self._rma_mgr:
            return

        filters = {}

        sn = self.search_serial_var.get().strip()
        if sn:
            filters['serial_number'] = sn

        pc = self.search_part_var.get().strip()
        if pc:
            filters['part_code'] = pc

        ft = self.search_fault_var.get().strip()
        if ft:
            filters['fault_text'] = ft

        ftype = self.search_ftype_var.get().strip()
        if ftype and ftype in self._ftype_map:
            filters['fault_type_id'] = self._ftype_map[ftype]

        ref = self.search_ref_var.get().strip()
        if ref:
            filters['reference'] = ref

        cust = self.search_customer_var.get().strip()
        if cust:
            filters['customer'] = cust

        results = self._rma_mgr.search_records(filters)

        # Popola TreeView
        self.result_tree.delete(*self.result_tree.get_children())
        self._result_data.clear()

        for r in results:
            iid = str(r.RmaRecordId)
            # Tronca testi lunghi per la colonna TreeView
            fault_short = (r.FaultDescription or '')[:60]
            self.result_tree.insert('', 'end', iid=iid, values=(
                r.SerialNumber or '',
                r.PartCode or '',
                r.CustomerName or '',
                fault_short,
                r.FaultType or '',
                r.Reference or '',
                r.OrderDateFmt or ''
            ))
            self._result_data[iid] = r

        total = self._rma_mgr.get_total_count()
        self.results_label.config(
            text=f"Risultati: {len(results)} su {total:,}"
        )

    def _reset_filters(self):
        """Reset tutti i filtri."""
        self.search_serial_var.set('')
        self.search_part_var.set('')
        self.search_fault_var.set('')
        self.search_ftype_var.set('')
        self.search_ref_var.set('')
        self.search_customer_var.set('')
        self.result_tree.delete(*self.result_tree.get_children())
        self._result_data.clear()
        self.results_label.config(text='')
        self._clear_detail_panel()

    def _on_ftype_changed(self, event=None):
        """Quando cambia il tipo guasto, potrebbe filtrare i dettagli (futuro)."""
        pass

    # ══════════════════════════════════════════════════════════════════
    # Dettaglio
    # ══════════════════════════════════════════════════════════════════
    def _on_result_select(self, event=None):
        """Mostra il dettaglio del record selezionato nel pannello inferiore."""
        sel = self.result_tree.focus()
        if not sel or sel not in self._result_data:
            return

        r = self._result_data[sel]

        self._detail_labels['serial'].config(text=r.SerialNumber or '')
        self._detail_labels['part'].config(text=r.PartCode or '')
        self._detail_labels['part_desc'].config(text=r.PartDescription or '')
        self._detail_labels['customer'].config(text=r.CustomerName or '')
        self._detail_labels['rma_num'].config(text=r.RmaNumber or '')
        self._detail_labels['fault'].config(text=r.FaultDescription or '')

        type_detail = r.FaultType or ''
        if r.FaultDetail:
            type_detail += f" → {r.FaultDetail}"
        self._detail_labels['fault_type_detail'].config(text=type_detail)

        ref_asm = r.Reference or ''
        if r.Assembly:
            ref_asm += f" / {r.Assembly}"
        self._detail_labels['ref_asm'].config(text=ref_asm)

        self._detail_labels['solution'].config(text=r.FaultNotes or '—')
        self._detail_labels['corrective'].config(text=r.CorrectiveAction or '')

        cause = ''
        if r.FaultCause:
            cause = r.FaultCause
        if r.FaultCauseCode:
            cause = f"{cause} ({r.FaultCauseCode})" if cause else r.FaultCauseCode
        self._detail_labels['cause'].config(text=cause)

        self._detail_labels['site'].config(text=r.ProductionSite or '')
        self._detail_labels['responsible'].config(text=r.ProcessResponsible or '')
        self._detail_labels['prod_week'].config(text=r.ProductionWeek or '')
        self._detail_labels['warranty'].config(text=r.WarrantyType or '')

        time_str = f"{r.RepairTimeMinutes} min" if r.RepairTimeMinutes else ''
        self._detail_labels['repair_time'].config(text=time_str)

        cost_str = f"€{r.Cost:.2f}" if r.Cost else ''
        self._detail_labels['cost'].config(text=cost_str)

        self._detail_labels['test'].config(text=r.TestType or '')
        self._detail_labels['operator'].config(text=r.Operator or '')
        self._detail_labels['already_rep'].config(
            text=self.lang.get('yes', 'Sì') if r.AlreadyRepaired else self.lang.get('no', 'No') if r.AlreadyRepaired is not None else ''
        )
        self._detail_labels['origin'].config(text=r.Origin or '')
        self._detail_labels['source'].config(text=r.Source or '')
        self._detail_labels['product_code'].config(text=r.ProductCode or '')

        # Bottone tracciabilità: mostra solo se SN contiene "TI"
        sn = r.SerialNumber or ''
        if 'TI' in sn.upper() and r.IDLabelCode:
            self._trace_btn.grid()
            self._trace_btn._label_code = sn
        else:
            self._trace_btn.grid_remove()

    def _clear_detail_panel(self):
        """Pulisce il pannello dettaglio."""
        for lbl in self._detail_labels.values():
            lbl.config(text='')
        self._trace_btn.grid_remove()

    def _open_traceability(self):
        """Apre la tracciabilità per il serial number selezionato."""
        try:
            label_code = getattr(self._trace_btn, '_label_code', None)
            if label_code:
                info = self.db.get_scrap_label_info(label_code)
                if info:
                    messagebox.showinfo(
                        self.lang.get('rma_traceability', 'Tracciabilità'),
                        f"Ordine: {getattr(info, 'OrderNumber', '')}\n"
                        f"Prodotto: {getattr(info, 'ProductCode', '')}\n"
                        f"Data ordine: {getattr(info, 'OrderDate', '')}",
                        parent=self
                    )
                else:
                    messagebox.showinfo(
                        self.lang.get('rma_traceability', 'Tracciabilità'),
                        self.lang.get('rma_trace_not_found', 'Informazioni di tracciabilità non trovate.'),
                        parent=self
                    )
        except Exception as e:
            logger.error(f"Errore apertura tracciabilità: {e}")

    # ══════════════════════════════════════════════════════════════════
    # Inserimento
    # ══════════════════════════════════════════════════════════════════
    def _verify_serial(self):
        """Verifica il serial number usando la funzione di tracciabilità."""
        sn = self.ins_serial_var.get().strip()
        if not sn:
            return

        # Prova lookup tracciabilità
        trace = self._rma_mgr.lookup_traceability(sn)
        if trace:
            self._ins_id_label_code = trace['id_label_code']
            self._ins_id_order = trace['id_order']
            self._ins_product_code = trace['product_code']
            self.ins_order_var.set(trace['order_number'] or '')
            self.ins_product_var.set(trace['product_code'] or '')
            self.ins_verify_status.config(
                text=f"✅ Trovato — Ordine: {trace['order_number']}",
                foreground='green'
            )
        else:
            self._ins_id_label_code = None
            self._ins_id_order = None
            self._ins_product_code = None
            self.ins_order_var.set('')
            self.ins_product_var.set('')
            self.ins_verify_status.config(
                text='⚠ Non trovato nella tracciabilità (scheda esterna?)',
                foreground='#CC8800'
            )

    def _on_ins_ftype_changed(self, event=None):
        """Quando cambia il tipo guasto nel form inserimento, aggiorna i dettagli."""
        ftype_str = self.ins_ftype_var.get().strip()
        if ftype_str and ftype_str in self._ftype_map:
            ftype_id = self._ftype_map[ftype_str]
            details = self._rma_mgr.get_fault_details(ftype_id)
            detail_names = [''] + [f"{d.Code} - {d.Description}" for d in details]
            self.ins_fdetail_combo['values'] = detail_names
            self._ins_fdetail_map = {f"{d.Code} - {d.Description}": d.RmaFaultDetailId for d in details}
        else:
            self.ins_fdetail_combo['values'] = ['']
            self._ins_fdetail_map = {}
        self.ins_fdetail_var.set('')

    def _browse_photo(self):
        """Seleziona un file immagine."""
        path = filedialog.askopenfilename(
            title=self.lang.get('rma_select_photo', 'Seleziona foto difetto'),
            filetypes=[
                ("Immagini", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("Tutti i file", "*.*")
            ],
            parent=self
        )
        if path:
            self.ins_photo_var.set(path)

    def _do_save(self):
        """Salva un nuovo record RMA."""
        if not self._rma_mgr:
            return

        sn = self.ins_serial_var.get().strip()
        if not sn:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('rma_serial_required', 'Il Serial Number è obbligatorio.'),
                parent=self
            )
            return

        # Raccogli dati dal form
        data = {
            'serial_number': sn,
            'part_code': self.ins_part_var.get().strip() or None,
            'customer_part_code': None,
            'part_description': None,
            'rma_number': None,
            'customer_id': None,
            'customer_name': self.ins_customer_var.get().strip() or None,
            'fault_description': self.ins_fault_desc.get('1.0', 'end').strip() or None,
            'fault_cause_code': self.ins_cause_code_var.get().strip() or None,
            'fault_cause': self.ins_cause_text_var.get().strip() or None,
            'fault_type_id': None,
            'fault_detail_id': None,
            'reference': self.ins_ref_var.get().strip() or None,
            'assembly': self.ins_assembly_var.get().strip() or None,
            'fault_notes': self.ins_fault_notes.get('1.0', 'end').strip() or None,
            'corrective_action': self.ins_corrective.get('1.0', 'end').strip() or None,
            'production_week': None,
            'production_site_id': None,
            'process_responsible': self.ins_resp_var.get().strip() or None,
            'warranty_type': self.ins_warranty_var.get().strip() or None,
            'origin': None,
            'repair_time_minutes': None,
            'cost': None,
            'already_repaired': None,
            'operator': getattr(self.parent, 'last_authenticated_user_name', None),
            'test_type': None,
            'order_date': None,
            'delivery_date': None,
            'close_date': None,
            'test_date': None,
            'photo_path': self.ins_photo_var.get().strip() or None,
            'document_links': self.ins_doc_links.get('1.0', 'end').strip() or None,
            'id_label_code': self._ins_id_label_code,
            'id_order': self._ins_id_order,
            'product_code': self._ins_product_code,
            'inserted_by': getattr(self.parent, 'last_authenticated_user_name', 'UNKNOWN'),
            'source': 'MANUAL'
        }

        # Tipo guasto
        ftype_str = self.ins_ftype_var.get().strip()
        if ftype_str and ftype_str in self._ftype_map:
            data['fault_type_id'] = self._ftype_map[ftype_str]

        # Dettaglio guasto
        fdetail_str = self.ins_fdetail_var.get().strip()
        if fdetail_str and hasattr(self, '_ins_fdetail_map') and fdetail_str in self._ins_fdetail_map:
            data['fault_detail_id'] = self._ins_fdetail_map[fdetail_str]

        # Sito produzione
        site = self.ins_site_var.get().strip()
        if site and site in self._site_map:
            data['production_site_id'] = self._site_map[site]

        # Tempo riparazione
        time_str = self.ins_time_var.get().strip()
        if time_str:
            try:
                data['repair_time_minutes'] = int(time_str)
            except ValueError:
                pass

        # Salva
        new_id = self._rma_mgr.insert_record(data)
        if new_id:
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('rma_saved_ok', f'Soluzione RMA salvata (ID: {new_id})'),
                parent=self
            )
            self._clear_insert_form()
            self._update_stats()
        else:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('rma_save_error', 'Errore nel salvataggio. Controllare i log.'),
                parent=self
            )

    def _clear_insert_form(self):
        """Pulisce il form di inserimento."""
        self.ins_serial_var.set('')
        self.ins_order_var.set('')
        self.ins_product_var.set('')
        self.ins_verify_status.config(text='')
        self._ins_id_label_code = None
        self._ins_id_order = None
        self._ins_product_code = None

        self.ins_part_var.set('')
        self.ins_customer_var.set('')
        self.ins_fault_desc.delete('1.0', 'end')
        self.ins_ftype_var.set('')
        self.ins_fdetail_var.set('')
        self.ins_ref_var.set('')
        self.ins_assembly_var.set('')

        self.ins_fault_notes.delete('1.0', 'end')
        self.ins_corrective.delete('1.0', 'end')
        self.ins_cause_code_var.set('')
        self.ins_cause_text_var.set('')

        self.ins_warranty_var.set('')
        self.ins_site_var.set('')
        self.ins_resp_var.set('')
        self.ins_time_var.set('')

        self.ins_photo_var.set('')
        self.ins_doc_links.delete('1.0', 'end')
