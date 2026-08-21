"""
indirect_materials_order_confirmation.py
Form per la conferma degli ordini di acquisto di materiali indiretti.
Legge i solleciti inviati (ind.RiordineEmailLog Stato='INVIATO') e permette di
inserire: quantità ordinata, numero PO, data prevista arrivo.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime, timedelta

from tkcalendar import DateEntry

logger = logging.getLogger(__name__)


# Configurazione colonne:
# (key, testo header, width minima dati, sticky dati, anchor header, espandibile)
COLS = [
    ('select', 'Anulează', 3, '', 'center', False),
    ('code', 'Cod Material', 14, 'w', 'center', True),
    ('desc', 'Descriere', 34, 'w', 'center', True),
    ('qta_sugg', 'Qta suggerita', 12, 'e', 'center', False),
    ('stock', 'Stoc', 10, 'e', 'center', False),
    ('ordered', 'Cantitate comandată', 12, 'w', 'center', False),
    ('po', 'Număr PO', 14, 'w', 'center', False),
    ('eta', 'Data sosire', 12, '', 'center', False),
    ('days', 'Zile', 6, '', 'center', False),
]

PAD_X = 4
PAD_Y = 1
HEADER_BG = '#d9d9d9'
ROW_BG_EVEN = '#f7f7f7'
ROW_BG_ODD = '#ffffff'
SCROLLBAR_WIDTH = 22
EXTRA_WIDTH = 70
EXTRA_HEIGHT = 160
MAX_CANVAS_HEIGHT = 520


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

        self.title(lang.get('purchasing_confirmation_title', 'Conferma ordini materiali indiretti'))
        self.geometry("1000x700")
        self.resizable(True, True)
        self.minsize(900, 500)
        self.transient(master)
        self.grab_set()
        self._initial_layout_done = False
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Header informativo
        top_frame = ttk.Frame(self, padding=(10, 10, 10, 6))
        top_frame.pack(fill="x")
        ttk.Label(
            top_frame,
            text=self.lang.get('purchasing_confirmation_header',
                              'Introduceți pentru fiecare material cantitatea comandată, numărul PO și data estimată de sosire.'),
            font=("Segoe UI", 10)
        ).pack(anchor="w")

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

        for cidx, (key, text, dw, dsticky, hanchor, expand) in enumerate(COLS):
            lbl = tk.Label(
                self.header_frame,
                text=self.lang.get(f'purchasing_confirm_col_{key}', text),
                font=("Segoe UI", 9, "bold"),
                bg=HEADER_BG,
                anchor=hanchor
            )
            lbl.grid(row=0, column=cidx, padx=PAD_X, pady=PAD_Y, sticky="ew")

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
    def _clear_rows(self):
        """Pulisce le righe esistenti e i widget memorizzati."""
        for row in self.row_widgets:
            for w in row['widgets']:
                w.destroy()
        self.row_widgets = []
        for w in self.rows_frame.winfo_children():
            w.destroy()

    def _load_data(self):
        """Carica i solleciti non confermati dal DB."""
        self._clear_rows()

        query = """
            SELECT l.RiordineLogId, m.CodiceMateriale, m.DescrizioneMateriale
            , isnull(l.QtaSuggerita,0) as QtaSuggerita, isnull(l.GiacenzaRilevata, 0) as GiacenzaRilevata, l.DataInvio,  l.DataInvio,
                   DATEDIFF(DAY, l.DataInvio, GETDATE()) AS GiorniTrascorsi
            FROM Traceability_RS.ind.RiordineEmailLog l
            JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = l.MaterialeId
            WHERE l.Stato = 'INVIATO'
              AND l.DataInvio >= DATEADD(DAY, -30, GETDATE())
              AND l.DataInvio >= '2026-08-14'
            ORDER BY l.DataInvio ASC
        """
        try:
            if hasattr(self.db, 'fetch_all'):
                rows = self.db.fetch_all(query)
            else:
                self.db._ensure_connection()
                with self.db._lock:
                    self.db.cursor.execute(query)
                    rows = self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Errore caricamento conferme: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('purchasing_confirm_load_error', 'Errore caricamento dati')}:\n{e}",
                parent=self
            )
            return

        if not rows:
            ttk.Label(
                self.rows_frame,
                text=self.lang.get('purchasing_confirm_none', 'Nessun ordine da confermare.')
            ).grid(row=0, column=0, columnspan=9, pady=20)
            self._layout_table()
            return

        default_eta = datetime.now() + timedelta(days=1)

        for ridx, row in enumerate(rows):
            log_id = row[0]
            codice = row[1] or ''
            descrizione = row[2] or ''
            qta_sugg = row[3] if row[3] is not None else ''
            giacenza = row[4] if row[4] is not None else ''
            data_invio = row[5].strftime('%d/%m/%Y') if row[5] else ''
            giorni = row[6] if row[6] is not None else ''

            created_widgets = []
            bg = ROW_BG_EVEN if ridx % 2 == 0 else ROW_BG_ODD

            var_cancel = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(self.rows_frame, variable=var_cancel)
            chk.grid(row=ridx, column=0, padx=PAD_X, pady=PAD_Y, sticky=COLS[0][3])
            created_widgets.append(chk)

            lbl_code = tk.Label(self.rows_frame, text=codice, width=COLS[1][2], anchor='w', bg=bg, font=("Segoe UI", 9))
            lbl_code.grid(row=ridx, column=1, padx=PAD_X, pady=PAD_Y, sticky=COLS[1][3])
            created_widgets.append(lbl_code)

            lbl_desc = tk.Label(self.rows_frame, text=descrizione, width=COLS[2][2], anchor='w', bg=bg, font=("Segoe UI", 9))
            lbl_desc.grid(row=ridx, column=2, padx=PAD_X, pady=PAD_Y, sticky=COLS[2][3])
            created_widgets.append(lbl_desc)

            lbl_qta = tk.Label(
                self.rows_frame,
                text=f"{qta_sugg:.4f}" if isinstance(qta_sugg, (int, float)) else qta_sugg,
                width=COLS[3][2],
                anchor='e',
                bg=bg,
                font=("Segoe UI", 9)
            )
            lbl_qta.grid(row=ridx, column=3, padx=PAD_X, pady=PAD_Y, sticky=COLS[3][3])
            created_widgets.append(lbl_qta)

            lbl_stock = tk.Label(
                self.rows_frame,
                text=f"{giacenza:.4f}" if isinstance(giacenza, (int, float)) else giacenza,
                width=COLS[4][2],
                anchor='e',
                bg=bg,
                font=("Segoe UI", 9)
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
            eta_widget.set_date(default_eta)
            eta_widget.grid(row=ridx, column=7, padx=PAD_X, pady=PAD_Y, sticky=COLS[7][3])
            created_widgets.append(eta_widget)

            lbl_days = tk.Label(self.rows_frame, text=str(giorni), width=COLS[8][2], anchor='center', bg=bg, font=("Segoe UI", 9))
            lbl_days.grid(row=ridx, column=8, padx=PAD_X, pady=PAD_Y, sticky=COLS[8][3])
            created_widgets.append(lbl_days)

            self.row_widgets.append({
                'log_id': log_id,
                'cancel_var': var_cancel,
                'qty_var': qty_var,
                'po_var': po_var,
                'eta_widget': eta_widget,
                'widgets': created_widgets
            })

        self._layout_table()

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
        window_height = top_height + header_height + canvas_height + btn_height + EXTRA_HEIGHT

        window_width = max(window_width, 820)
        window_height = max(window_height, 400)

        self.geometry(f"{window_width}x{window_height}")
        self.update_idletasks()

    def _save(self):
        """Salva le conferme/annullamenti nel DB."""
        updates = []
        for row in self.row_widgets:
            log_id = row['log_id']
            cancel = row['cancel_var'].get()
            if cancel:
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

            updates.append((log_id, qty, po, eta, 'CONFERMATO'))

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
