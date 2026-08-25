"""
indirect_materials_order_confirmation.py
Form per la conferma degli ordini di acquisto di materiali indiretti.
Legge i solleciti inviati (ind.RiordineEmailLog Stato='INVIATO') e permette di
inserire: quantità ordinata, numero PO, data prevista arrivo.

Novità:
- I materiali ripetuti sono raggruppati per codice/descrizione.
- Le intestazioni di colonna consentono l'ordinamento A-Z / Z-A.
- Campo di filtro per codice o descrizione.
- Le conferme già inserite restano visibili in una tabella separata in fondo,
  in ordine di inserimento.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime, timedelta
from collections import defaultdict

from tkcalendar import DateEntry

logger = logging.getLogger(__name__)


# Configurazione colonne principali:
# (key, testo header, width caratteri, sticky dati, anchor header, ordinabile)
COLS = [
    ('select', 'Anulează', 3, '', 'center', False),
    ('code', 'Cod Material', 14, 'w', 'center', True),
    ('desc', 'Descriere', 34, 'w', 'center', True),
    ('qta_sugg', 'Qta suggerita', 12, 'e', 'center', True),
    ('stock', 'Stoc', 10, 'e', 'center', True),
    ('ordered', 'Cantitate comandată', 12, 'w', 'center', False),
    ('po', 'Număr PO', 14, 'w', 'center', False),
    ('eta', 'Data sosire', 16, '', 'center', True),
    ('days', 'Zile', 8, '', 'center', True),
]

# Colonne tabella inferiore conferme: (key, testo default, width pixel)
BOTTOM_COLS = [
    ('code', 'Cod Material', 120),
    ('desc', 'Descriere', 260),
    ('qty', 'Cantitate comandată', 110),
    ('po', 'Număr PO', 120),
    ('eta', 'Data sosire', 110),
    ('confirmed', 'Data conferma', 130),
]

PAD_X = 4
PAD_Y = 1
HEADER_BG = '#d9d9d9'
ROW_BG_EVEN = '#f7f7f7'
ROW_BG_ODD = '#ffffff'
SCROLLBAR_WIDTH = 22
EXTRA_WIDTH = 160
EXTRA_HEIGHT = 240
MAX_CANVAS_HEIGHT = 360


def _col_text(key):
    """Restituisce il testo di default di una colonna principale."""
    for c in COLS:
        if c[0] == key:
            return c[1]
    return key


class IndirectMaterialsOrderConfirmationWindow(tk.Toplevel):
    """Form di conferma ordini materiali indiretti."""

    def __init__(self, master, db, lang, user_name="Unknown"):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.row_widgets = []
        self.rows_frame_id = None
        self.table_frame = None
        self.header_labels = {}

        self.all_groups = []
        self.filtered_groups = []
        self.bottom_rows = []
        self.sort_col = None
        self.sort_desc = False
        self.filter_var = tk.StringVar()
        self.default_eta = datetime.now() + timedelta(days=1)

        self.title(lang.get('purchasing_confirmation_title', 'Conferma ordini materiali indiretti'))
        self.geometry("1100x750")
        self.resizable(True, True)
        self.minsize(950, 550)
        self.transient(master)
        self.grab_set()
        self._initial_layout_done = False
        self._build_ui()
        self._load_data()

    # ═══════════════════════════════════════════════════════════════════════
    #  UI
    # ═══════════════════════════════════════════════════════════════════════
    def _build_ui(self):
        # Header informativo + filtro
        top_frame = ttk.Frame(self, padding=(10, 10, 10, 6))
        top_frame.pack(fill="x")
        top_frame.columnconfigure(0, weight=1)

        ttk.Label(
            top_frame,
            text=self.lang.get(
                'purchasing_confirmation_header',
                'Introduceți pentru fiecare material cantitatea comandată, numărul PO și data estimată de sosire.'
            ),
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w")

        filter_frame = ttk.Frame(top_frame)
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(
            filter_frame,
            text=self.lang.get('purchasing_confirm_filter', 'Filtrează:'),
            font=("Segoe UI", 9)
        ).grid(row=0, column=0, sticky="w")
        self.filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, font=("Segoe UI", 9))
        self.filter_entry.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.filter_var.trace_add('write', self._on_filter_change)

        # Container per tabella: header fisso + body scrollabile
        container = ttk.Frame(self, padding=(10, 0, 10, 6))
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Wrapper che mantiene header e canvas allineati alla stessa larghezza
        self.table_frame = ttk.Frame(container)
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(1, weight=1)  # body espandibile

        # Header fisso
        self.header_frame = ttk.Frame(self.table_frame, padding=(0, 2, 0, 2))
        self.header_frame.grid(row=0, column=0, sticky="new")

        for cidx, (key, text, dw, dsticky, hanchor, sortable) in enumerate(COLS):
            lbl = tk.Label(
                self.header_frame,
                text=self.lang.get(f'purchasing_confirm_col_{key}', text),
                font=("Segoe UI", 9, "bold"),
                bg=HEADER_BG,
                anchor=hanchor,
                cursor='hand2' if sortable else 'arrow'
            )
            lbl.grid(row=0, column=cidx, padx=PAD_X, pady=PAD_Y, sticky="ew")
            if sortable:
                lbl.bind('<Button-1>', lambda e, k=key: self._on_header_click(k))
            self.header_labels[key] = lbl

        ttk.Separator(self.table_frame, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=(0, 2))

        # Body scrollabile
        self.body_container = ttk.Frame(self.table_frame)
        self.body_container.grid(row=2, column=0, sticky="nsew")
        self.body_container.columnconfigure(0, weight=1)
        self.body_container.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.body_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.body_container, orient="vertical", command=self.canvas.yview)
        self.rows_frame = ttk.Frame(self.canvas)

        self.rows_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.rows_frame_id = self.canvas.create_window(
            (0, 0), window=self.rows_frame, anchor="nw", tags="rows_frame"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Adatta frame interno alla larghezza del canvas quando la finestra viene ridimensionata
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        # Scroll con mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Tabella inferiore: conferme già inserite (ordine di inserimento)
        self.bottom_frame = ttk.LabelFrame(
            self,
            text=self.lang.get('purchasing_confirm_bottom_title', 'Comenzi confirmate'),
            padding=(10, 6, 10, 6)
        )
        self.bottom_frame.pack(fill="x", padx=10, pady=(0, 6))
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.bottom_tree = ttk.Treeview(
            self.bottom_frame,
            columns=[c[0] for c in BOTTOM_COLS],
            show='headings',
            height=5
        )
        for key, text, width in BOTTOM_COLS:
            self.bottom_tree.heading(key, text=self.lang.get(f'purchasing_confirm_bottom_col_{key}', text))
            self.bottom_tree.column(key, width=width, minwidth=width, anchor='center')
        self.bottom_tree.grid(row=0, column=0, sticky="nsew")

        bottom_scroll = ttk.Scrollbar(
            self.bottom_frame, orient="vertical", command=self.bottom_tree.yview
        )
        self.bottom_tree.configure(yscrollcommand=bottom_scroll.set)
        bottom_scroll.grid(row=0, column=1, sticky="ns")

        # Bottoni azione
        btn_frame = ttk.Frame(self, padding=(10, 6, 10, 10))
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame,
            text=self.lang.get('purchasing_confirm_save', 'Salvează confirmări'),
            command=self._save
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            btn_frame,
            text=self.lang.get('purchasing_confirm_reload', 'Actualizează'),
            command=self._load_data
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            btn_frame,
            text=self.lang.get('purchasing_confirm_close', 'Închide'),
            command=self.destroy
        ).pack(side="right")

    # ═══════════════════════════════════════════════════════════════════════
    #  Eventi
    # ═══════════════════════════════════════════════════════════════════════
    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _on_canvas_resize(self, event):
        """Espande il frame interno alla larghezza del canvas quando la finestra viene ridimensionata."""
        try:
            if self.rows_frame_id is not None:
                self.canvas.itemconfig(self.rows_frame_id, width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception:
            pass

    def _on_header_click(self, key):
        """Gestisce l'ordinamento A-Z / Z-A cliccando sull'intestazione."""
        if self.sort_col == key:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_col = key
            self.sort_desc = False
        self._update_header_arrows()
        self._apply_filter()

    def _on_filter_change(self, *args):
        """Applica il filtro in tempo reale."""
        self._apply_filter()

    # ═══════════════════════════════════════════════════════════════════════
    #  Dati
    # ═══════════════════════════════════════════════════════════════════════
    def _fetch(self, query):
        """Esegue una query e restituisce le righe."""
        if hasattr(self.db, 'fetch_all'):
            return self.db.fetch_all(query)
        self.db._ensure_connection()
        with self.db._lock:
            self.db.cursor.execute(query)
            return self.db.cursor.fetchall()

    def _load_data(self):
        """Carica i solleciti non confermati e le conferme già salvate dal DB."""
        self._clear_rows()
        self.all_groups = []
        self.filtered_groups = []
        self.bottom_rows = []

        query_open = """
            SELECT l.RiordineLogId, m.CodiceMateriale, m.DescrizioneMateriale,
                   isnull(l.QtaSuggerita, 0) as QtaSuggerita,
                   isnull(l.GiacenzaRilevata, 0) as GiacenzaRilevata,
                   l.DataInvio,
                   DATEDIFF(DAY, l.DataInvio, GETDATE()) AS GiorniTrascorsi
            FROM Traceability_RS.ind.RiordineEmailLog l
            JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = l.MaterialeId
            WHERE l.Stato = 'INVIATO'
              AND l.DataInvio >= DATEADD(DAY, -30, GETDATE())
              AND l.DataInvio >= '2026-08-14'
        """

        query_confirmed = """
            SELECT l.RiordineLogId, m.CodiceMateriale, m.DescrizioneMateriale,
                   isnull(l.QtaOrdinata, 0) as QtaOrdinata,
                   isnull(l.NumeroPO, '') as NumeroPO,
                   l.DataPrevistaArrivo,
                   l.DataConferma
            FROM Traceability_RS.ind.RiordineEmailLog l
            JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = l.MaterialeId
            WHERE l.Stato = 'CONFERMATO'
              AND l.DataInvio >= DATEADD(DAY, -30, GETDATE())
              AND l.DataInvio >= '2026-08-14'
            ORDER BY l.DataConferma ASC, l.RiordineLogId ASC
        """

        try:
            rows_open = self._fetch(query_open)
            rows_confirmed = self._fetch(query_confirmed)
        except Exception as e:
            logger.error(f"Errore caricamento conferme: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('purchasing_confirm_load_error', 'Errore caricamento dati')}:\n{e}",
                parent=self
            )
            return

        # Raggruppa i solleciti aperti per codice/descrizione
        groups = defaultdict(lambda: {
            'log_ids': [],
            'qta_sugg': 0.0,
            'stock': None,
            'data_invio': None,
            'giorni': 0,
        })

        for row in rows_open:
            log_id = row[0]
            code = row[1] or ''
            desc = row[2] or ''
            qta = row[3] if row[3] is not None else 0.0
            stock = row[4] if row[4] is not None else 0.0
            data_invio = row[5]
            giorni = row[6] if row[6] is not None else 0

            key = (code, desc)
            g = groups[key]
            g['log_ids'].append(log_id)
            g['qta_sugg'] += float(qta)
            if g['stock'] is None:
                g['stock'] = float(stock)
            # Conserva la data di invio più recente del gruppo
            if data_invio is not None:
                if g['data_invio'] is None or data_invio > g['data_invio']:
                    g['data_invio'] = data_invio
            g['giorni'] = max(g['giorni'], giorni)

        for (code, desc), g in groups.items():
            self.all_groups.append({
                'group_key': (code, desc),
                'code': code,
                'desc': desc,
                'log_ids': sorted(g['log_ids']),
                'qta_sugg': g['qta_sugg'],
                'stock': g['stock'] if g['stock'] is not None else 0.0,
                'data_invio': g['data_invio'],
                'giorni': g['giorni'],
            })

        self.bottom_rows = rows_confirmed

        # Renderizza prima la tabella inferiore, poi quella principale
        # (il layout finale dipende dall'altezza della tabella inferiore)
        self._render_bottom_table()
        self._apply_filter()

    def _apply_filter(self, *args):
        """Filtra i gruppi in base al testo del campo filtro."""
        text = self.filter_var.get().strip().lower()
        if text:
            self.filtered_groups = [
                g for g in self.all_groups
                if text in g['code'].lower() or text in g['desc'].lower()
            ]
        else:
            self.filtered_groups = list(self.all_groups)
        self._sort_groups()
        self._render_main_table()

    def _sort_groups(self):
        """Ordina i gruppi filtrati in base alla colonna e direzione scelta."""
        if not self.sort_col:
            return

        def key_fn(g):
            if self.sort_col == 'code':
                return g['code'].lower()
            if self.sort_col == 'desc':
                return g['desc'].lower()
            if self.sort_col == 'qta_sugg':
                return float(g['qta_sugg'])
            if self.sort_col == 'stock':
                return float(g['stock'])
            if self.sort_col == 'eta':
                return g['data_invio'] or datetime.min
            if self.sort_col == 'days':
                try:
                    return int(g['giorni'])
                except Exception:
                    return -1
            return ''

        self.filtered_groups.sort(key=key_fn, reverse=self.sort_desc)

    def _update_header_arrows(self):
        """Aggiorna le intestazioni mostrando la freccia di ordinamento."""
        for key, lbl in self.header_labels.items():
            base = self.lang.get(f'purchasing_confirm_col_{key}', _col_text(key))
            if key == self.sort_col:
                arrow = ' ▼' if self.sort_desc else ' ▲'
                lbl.config(text=f"{base}{arrow}", fg='#004080')
            else:
                lbl.config(text=base, fg='black')

    def _clear_rows(self):
        """Pulisce le righe esistenti e i widget memorizzati."""
        for row in self.row_widgets:
            for w in row['widgets']:
                w.destroy()
        self.row_widgets = []
        for w in self.rows_frame.winfo_children():
            w.destroy()

    def _capture_input_state(self):
        """Cattura i valori attuali inseriti dall'utente per gruppo."""
        state = {}
        for row in self.row_widgets:
            try:
                eta = row['eta_widget'].get_date()
            except Exception:
                eta = None
            state[row['group_key']] = {
                'cancel': row['cancel_var'].get(),
                'qty': row['qty_var'].get(),
                'po': row['po_var'].get(),
                'eta': eta,
            }
        return state

    def _render_main_table(self, restore_state=None):
        """Disegna le righe della tabella principale."""
        if restore_state is None:
            restore_state = self._capture_input_state()

        # Pulisce
        for row in self.row_widgets:
            for w in row['widgets']:
                w.destroy()
        self.row_widgets = []
        for w in self.rows_frame.winfo_children():
            w.destroy()

        if not self.filtered_groups:
            ttk.Label(
                self.rows_frame,
                text=self.lang.get('purchasing_confirm_none', 'Nessun ordine da confermare.')
            ).grid(row=0, column=0, columnspan=len(COLS), pady=20)
            self._layout_table()
            return

        for ridx, g in enumerate(self.filtered_groups):
            bg = ROW_BG_EVEN if ridx % 2 == 0 else ROW_BG_ODD
            created_widgets = []
            code, desc = g['group_key']

            var_cancel = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(self.rows_frame, variable=var_cancel)
            chk.grid(row=ridx, column=0, padx=PAD_X, pady=PAD_Y, sticky=COLS[0][3])
            created_widgets.append(chk)

            lbl_code = tk.Label(
                self.rows_frame, text=code, width=COLS[1][2], anchor='w',
                bg=bg, font=("Segoe UI", 9)
            )
            lbl_code.grid(row=ridx, column=1, padx=PAD_X, pady=PAD_Y, sticky=COLS[1][3])
            created_widgets.append(lbl_code)

            lbl_desc = tk.Label(
                self.rows_frame, text=desc, width=COLS[2][2], anchor='w',
                bg=bg, font=("Segoe UI", 9)
            )
            lbl_desc.grid(row=ridx, column=2, padx=PAD_X, pady=PAD_Y, sticky=COLS[2][3])
            created_widgets.append(lbl_desc)

            lbl_qta = tk.Label(
                self.rows_frame,
                text=f"{g['qta_sugg']:.4f}",
                width=COLS[3][2], anchor='e', bg=bg, font=("Segoe UI", 9)
            )
            lbl_qta.grid(row=ridx, column=3, padx=PAD_X, pady=PAD_Y, sticky=COLS[3][3])
            created_widgets.append(lbl_qta)

            lbl_stock = tk.Label(
                self.rows_frame,
                text=f"{g['stock']:.4f}",
                width=COLS[4][2], anchor='e', bg=bg, font=("Segoe UI", 9)
            )
            lbl_stock.grid(row=ridx, column=4, padx=PAD_X, pady=PAD_Y, sticky=COLS[4][3])
            created_widgets.append(lbl_stock)

            qty_var = tk.StringVar()
            po_var = tk.StringVar()

            entry_qty = ttk.Entry(self.rows_frame, textvariable=qty_var, width=COLS[5][2])
            entry_qty.grid(row=ridx, column=5, padx=PAD_X, pady=PAD_Y, sticky=COLS[5][3])
            created_widgets.append(entry_qty)

            entry_po = ttk.Entry(self.rows_frame, textvariable=po_var, width=COLS[6][2])
            entry_po.grid(row=ridx, column=6, padx=PAD_X, pady=PAD_Y, sticky=COLS[6][3])
            created_widgets.append(entry_po)

            eta_widget = DateEntry(
                self.rows_frame,
                width=COLS[7][2],
                date_pattern='dd/MM/yyyy',
                firstweekday='monday',
                locale='ro_RO'
            )
            eta_widget.set_date(self.default_eta)
            eta_widget.grid(row=ridx, column=7, padx=PAD_X, pady=PAD_Y, sticky=COLS[7][3])
            created_widgets.append(eta_widget)

            lbl_days = tk.Label(
                self.rows_frame, text=str(g['giorni']), width=COLS[8][2],
                anchor='center', bg=bg, font=("Segoe UI", 9)
            )
            lbl_days.grid(row=ridx, column=8, padx=PAD_X, pady=PAD_Y, sticky=COLS[8][3])
            created_widgets.append(lbl_days)

            # Ripristina eventuali valori inseriti prima del filtro/ordinamento
            if g['group_key'] in restore_state:
                st = restore_state[g['group_key']]
                var_cancel.set(st.get('cancel', False))
                qty_var.set(st.get('qty', ''))
                po_var.set(st.get('po', ''))
                eta = st.get('eta')
                if eta:
                    try:
                        eta_widget.set_date(eta)
                    except Exception:
                        pass

            self.row_widgets.append({
                'group_key': g['group_key'],
                'log_ids': g['log_ids'],
                'cancel_var': var_cancel,
                'qty_var': qty_var,
                'po_var': po_var,
                'eta_widget': eta_widget,
                'widgets': created_widgets
            })

        self._layout_table()

    def _render_bottom_table(self):
        """Popola la tabella inferiore con le conferme già salvate."""
        for item in self.bottom_tree.get_children():
            self.bottom_tree.delete(item)

        for row in self.bottom_rows:
            code = row[1] or ''
            desc = row[2] or ''
            qty = row[3] if row[3] is not None else 0.0
            po = row[4] or ''
            eta = row[5].strftime('%d/%m/%Y') if row[5] else ''
            confirmed = row[6].strftime('%d/%m/%Y %H:%M') if row[6] else ''
            self.bottom_tree.insert(
                '', 'end',
                values=(code, desc, f"{qty:.4f}", po, eta, confirmed)
            )

    def _layout_table(self):
        """Allinea header e colonne dati e adatta la finestra al contenuto."""
        self.update_idletasks()

        # Calcola larghezza richiesta per ogni colonna (header + dati)
        col_widths = [0] * len(COLS)

        for w in self.header_frame.winfo_children():
            info = w.grid_info()
            if not info:
                continue
            cidx = int(info.get('column', 0))
            col_widths[cidx] = max(col_widths[cidx], w.winfo_reqwidth())

        for row in self.row_widgets:
            for cidx, w in enumerate(row['widgets']):
                col_widths[cidx] = max(col_widths[cidx], w.winfo_reqwidth())

        # Aggiungi padding (dx + sx)
        for cidx in range(len(col_widths)):
            col_widths[cidx] += PAD_X * 2

        total_content_width = sum(col_widths)

        # Applica minsize a header e dati
        for cidx, width in enumerate(col_widths):
            self.header_frame.grid_columnconfigure(cidx, minsize=width, weight=0)
            self.rows_frame.grid_columnconfigure(cidx, minsize=width, weight=0)

        # Calcola altezza righe
        total_rows_height = 0
        for row in self.row_widgets:
            row_h = max(w.winfo_reqheight() for w in row['widgets']) + PAD_Y * 2
            total_rows_height += row_h

        # Header e bottoni
        header_height = self.header_frame.winfo_reqheight()
        top_height = self.winfo_children()[0].winfo_reqheight()
        btn_height = self.winfo_children()[-1].winfo_reqheight()
        bottom_height = self.bottom_frame.winfo_reqheight()

        # Altezza canvas limitata
        canvas_height = min(total_rows_height, MAX_CANVAS_HEIGHT)
        if canvas_height < 120:
            canvas_height = 120

        # Aggiorna canvas e frame interno
        self.canvas.configure(width=total_content_width, height=canvas_height)
        if self.rows_frame_id is not None:
            self.canvas.itemconfig(self.rows_frame_id, width=total_content_width)

        # Forza il wrapper a non espandersi oltre il contenuto
        self.table_frame.grid(row=0, column=0, sticky="nw")

        # Adatta finestra
        window_width = total_content_width + SCROLLBAR_WIDTH + EXTRA_WIDTH
        window_height = (
            top_height + header_height + canvas_height +
            bottom_height + btn_height + EXTRA_HEIGHT
        )

        window_width = max(window_width, 950)
        window_height = max(window_height, 550)

        self.geometry(f"{window_width}x{window_height}")
        self.update_idletasks()

    # ═══════════════════════════════════════════════════════════════════════
    #  Salvataggio
    # ═══════════════════════════════════════════════════════════════════════
    def _save(self):
        """Salva le conferme/annullamenti nel DB."""
        updates = []
        for row in self.row_widgets:
            log_ids = row['log_ids']
            cancel = row['cancel_var'].get()
            if cancel:
                for log_id in log_ids:
                    updates.append((log_id, None, None, None, 'ANNULLATO'))
                continue

            qty_str = row['qty_var'].get().strip().replace(',', '.')
            po = row['po_var'].get().strip()

            try:
                eta = row['eta_widget'].get_date()
            except Exception:
                eta = None

            if not qty_str and not po:
                continue

            try:
                qty = float(qty_str) if qty_str else 0
            except ValueError:
                messagebox.showwarning(
                    self.lang.get('warn_title', 'Attenzione'),
                    self.lang.get('purchasing_confirm_qty_invalid', 'Quantità non valida'),
                    parent=self
                )
                return

            if po and not qty_str:
                qty = 0

            # Salva la quantità sul log più vecchio e annulla i duplicati raggruppati
            main_log_id = min(log_ids)
            updates.append((main_log_id, qty, po, eta, 'CONFERMATO'))
            for log_id in log_ids:
                if log_id != main_log_id:
                    updates.append((log_id, None, None, None, 'ANNULLATO'))

        if not updates:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('purchasing_confirm_no_changes', 'Nessuna modifica da salvare.'),
                parent=self
            )
            return

        try:
            self.db._ensure_connection()
            with self.db._lock:
                cur = self.db.cursor
                for log_id, qty, po, eta, stato in updates:
                    cur.execute(
                        """UPDATE Traceability_RS.ind.RiordineEmailLog
                           SET QtaOrdinata = ?,
                               NumeroPO = ?,
                               DataPrevistaArrivo = ?,
                               Stato = ?,
                               DataConferma = GETDATE(),
                               ConfermatoDa = ?
                           WHERE RiordineLogId = ?""",
                        (qty, po, eta, stato, self.user_name, log_id)
                    )
                self.db.conn.commit()

            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('purchasing_confirm_saved', 'Conferme salvate.'),
                parent=self
            )
            self._load_data()
        except Exception as e:
            logger.error(f"Errore salvataggio conferme: {e}", exc_info=True)
            self.db.conn.rollback()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('purchasing_confirm_save_error', 'Errore salvataggio')}:\n{e}",
                parent=self
            )

    def destroy(self):
        """Pulisce i binding al destroy."""
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()


def open_indirect_materials_order_confirmation(master, db, lang, user_name):
    """Entry-point richiamabile da main.py."""
    IndirectMaterialsOrderConfirmationWindow(master, db, lang, user_name)
