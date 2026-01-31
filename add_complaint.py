"""
Modulo per l'aggiunta di nuovi reclami
Interfaccia grafica e logica di inserimento dati
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import json
import os
from pathlib import Path
from tkcalendar import DateEntry

logger = logging.getLogger(__name__)


@dataclass
class ClaimHeader:
    """Dati della testata del reclamo"""
    ClaimTypeId: int
    IdProduct: int
    DateClaim: str
    AWB: str
    TransportDocument: str
    CustomerClaimNumber: str = ""
    InternalClaimNumber: str = ""
    ShortClaimDescription: str = ""
    TargetDate: str = ""
    Quantity: int = 1
    IDFinalClient: int = 0
    ClaimDecisionId: Optional[int] = None
    USERName: str = ""
    DateSys: str = ""


@dataclass
class ClaimDetail:
    """Dati di ogni riga di reclamo"""
    FirstInspectionResultId: int
    LabelCod: str
    RootCause: str
    SummaryCorrectiveAction: str
    SummaryPreventiveAction: str
    ClaimStatusId: int
    ClaimDefectId: Optional[int] = None


class ComplaintsNumerationManager:
    """Gestisce la numerazione dei reclami"""

    CONFIG_FILE = 'Complains_numeration.json'

    @staticmethod
    def load_config() -> Dict:
        """Carica la configurazione da file JSON"""
        if os.path.exists(ComplaintsNumerationManager.CONFIG_FILE):
            try:
                with open(ComplaintsNumerationManager.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Errore caricamento config reclami: {e}")

        # Config di default
        current_year = datetime.now().year
        current_month = datetime.now().month
        return {
            'anno_corrente': current_year,
            'numero_reclami_anno': 0,
            'numero_reclami_mese': 0,
            'mese_corrente': current_month
        }

    @staticmethod
    def save_config(config: Dict):
        """Salva la configurazione su file JSON"""
        try:
            with open(ComplaintsNumerationManager.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Errore salvataggio config reclami: {e}")

    @staticmethod
    def generate_internal_claim_number() -> str:
        """Genera il numero interno del reclamo nel formato: anno/mese/numero_anno"""
        config = ComplaintsNumerationManager.load_config()
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Reset se cambio anno
        if config['anno_corrente'] != current_year:
            config['anno_corrente'] = current_year
            config['numero_reclami_anno'] = 0
            config['numero_reclami_mese'] = 0
            config['mese_corrente'] = current_month

        # Reset se cambio mese
        if config['mese_corrente'] != current_month:
            config['mese_corrente'] = current_month
            config['numero_reclami_mese'] = 0

        # Incrementa contatori
        config['numero_reclami_anno'] += 1
        config['numero_reclami_mese'] += 1

        # Salva aggiornamenti
        ComplaintsNumerationManager.save_config(config)

        # Genera numero
        num_anno = config['numero_reclami_anno']
        num_mese = config['numero_reclami_mese']

        return f"{num_anno}/{num_mese}/{current_year}"


class AddComplaintWindow(tk.Toplevel):
    """Finestra principale per l'aggiunta di un nuovo reclamo"""

    def __init__(self, parent, db, lang, authenticated_user):
        super().__init__(parent)

        self.parent = parent
        self.db = db
        self.lang = lang
        self.authenticated_user = authenticated_user

        self.title(lang.get('title_add_complaint', 'Aggiungi Reclamo'))
        self.geometry('1400x900')
        self.resizable(True, True)

        # Dati interni
        self.claim_header: Optional[ClaimHeader] = None
        self.claim_log_id: Optional[int] = None
        self.claim_details: List[ClaimDetail] = []
        self.combo_data: Dict = {}  # Cache per i dati dei combo

        # Stato della form
        self.header_saved = False
        self.rows_to_add = 0

        # Carica dati combo
        self._load_combo_data()

        # UI
        self._create_widgets()

        # Centra la finestra
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    # =========================================================================
    # CARICAMENTO DATI
    # =========================================================================

    def _load_combo_data(self):
        """Carica tutti i dati per i combobox"""
        try:
            logger.debug("[ADD_COMPLAINT] === INIZIO _load_combo_data ===")

            # Final Clients
            query_clients = """
                            SELECT IDFinalClient, FinalClientName, AcronimForCode
                            FROM FinalClients
                            ORDER BY FinalClientName
                            """
            clients = self.db.fetch_all(query_clients)
            self.combo_data['clients'] = clients
            self.combo_data['clients_map'] = {f"{c[1]} ({c[2]})": c[0] for c in clients}
            logger.debug(f"[ADD_COMPLAINT] Clienti caricati: {len(clients)}")

            # Products (con IDFinalClient per filtro)
            query_products = """
                             SELECT idproduct, productcode, productname, IDFinalClient
                             FROM products
                             WHERE CHARINDEX('cipr', productcode, 1) = 0
                               AND CHARINDEX('RMA', productcode, 1) = 0
                             ORDER BY productcode
                             """
            products = self.db.fetch_all(query_products)
            self.combo_data['products'] = products
            self.combo_data['products_map'] = {f"{p[1]} - {p[2]}": p[0] for p in products}
            logger.debug(f"[ADD_COMPLAINT] Prodotti caricati: {len(products)}")

            # Claim Types
            query_types = """
                          SELECT ClaimTypeId, ClaimType
                          FROM [Traceability_RS].[clm].[ClaimTypes]
                          ORDER BY ClaimType
                          """
            types = self.db.fetch_all(query_types)
            self.combo_data['claim_types'] = types
            self.combo_data['claim_types_map'] = {ct[1]: ct[0] for ct in types}
            logger.debug(f"[ADD_COMPLAINT] Claim Types caricati: {len(types)}")

            # First Inspection Results
            query_inspection = """
                               SELECT FirstInspectionResultId, FirstInspectionResult
                               FROM [Traceability_RS].[clm].[FirstInspectionResults]
                               ORDER BY FirstInspectionResult
                               """
            inspection = self.db.fetch_all(query_inspection)
            self.combo_data['inspection_results'] = inspection
            self.combo_data['inspection_map'] = {i[1]: i[0] for i in inspection}
            logger.debug(f"[ADD_COMPLAINT] Inspection Results caricati: {len(inspection)}")

            # Claim Status
            query_status = """
                           SELECT ClaimStatusId, ClaimStatus, IsEnd
                           FROM [Traceability_RS].[clm].[ClaimStatus]
                           """
            status = self.db.fetch_all(query_status)
            self.combo_data['claim_status'] = status
            self.combo_data['status_map'] = {s[1]: s[0] for s in status}
            logger.debug(f"[ADD_COMPLAINT] Claim Status caricati: {len(status)}")

            # Claim Defects
            query_defects = """
                            SELECT ClaimDefectId,
                                   ISNULL(CONCAT(p.ProcessStep, ' - '), '') + c.ClaimDefect as ClaimDefect
                            FROM [Traceability_RS].[clm].[ClaimDefects] c
                                LEFT JOIN [Traceability_RS].[clm].[ProcessSteps] p
                            ON c.ProcessStepId = p.ProcessStepId
                            ORDER BY ISNULL(CONCAT(p.ProcessStep, ' - '), '') + c.ClaimDefect
                            """
            defects = self.db.fetch_all(query_defects)
            self.combo_data['defects'] = defects
            self.combo_data['defects_map'] = {d[1]: d[0] for d in defects}
            logger.debug(f"[ADD_COMPLAINT] Defects caricati: {len(defects)}")

            # Document Types (NEW)
            doc_types = self.db.fetch_claim_doc_types()
            self.combo_data['doc_types'] = doc_types
            self.combo_data['doc_types_map'] = {dt[1]: dt[0] for dt in doc_types}
            logger.debug(f"[ADD_COMPLAINT] Document Types caricati: {len(doc_types)}")

            logger.info("[ADD_COMPLAINT] ✅ Tutti i dati combo caricati con successo")

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] ❌ Errore caricamento dati combo: {e}")
            messagebox.showerror(
                "Errore",
                f"Errore nel caricamento dei dati: {str(e)}",
                parent=self
            )

    # =========================================================================
    # CREAZIONE INTERFACCIA
    # =========================================================================

    def _create_widgets(self):
        """Crea l'interfaccia utente"""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_header(main_frame)
        self._create_claim_header_frame(main_frame)
        self._create_claim_details_frame(main_frame)

    def _create_header(self, parent):
        """Crea l'header con logo e orologio"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        try:
            if os.path.exists('Logo.png'):
                from PIL import Image, ImageTk
                logo_img = Image.open('Logo.png')
                logo_img.thumbnail((100, 50))
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(header_frame, image=self.logo_photo)
                logo_label.pack(side=tk.LEFT)
        except Exception as e:
            logger.warning(f"[ADD_COMPLAINT] Errore caricamento logo: {e}")

        ttk.Frame(header_frame).pack(side=tk.LEFT, expand=True)

        self.clock_label = ttk.Label(header_frame, text="", font=("Arial", 12, "bold"))
        self.clock_label.pack(side=tk.RIGHT)
        self._update_clock()

    def _update_clock(self):
        """Aggiorna l'orologio"""
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self._update_clock)

    def _create_claim_header_frame(self, parent):
        """Crea il frame per la testata del reclamo"""
        header_frame = ttk.LabelFrame(
            parent,
            text=self.lang.get('lbl_claim_header', 'Testata Reclamo'),
            padding=10
        )
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # ===== COLONNA SINISTRA: CLIENTE =====
        left_col = ttk.Frame(header_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Client
        ttk.Label(left_col, text=self.lang.get('lbl_client', 'Cliente') + " *:").pack(anchor=tk.W)
        self.var_client = tk.StringVar()
        self.combo_client = ttk.Combobox(
            left_col,
            textvariable=self.var_client,
            state='readonly',
            width=30
        )
        client_values = [f"{c[1]} ({c[2]})" for c in self.combo_data.get('clients', [])]
        self.combo_client['values'] = client_values
        self.combo_client.bind('<<ComboboxSelected>>', self._on_client_selected)
        self.combo_client.pack(fill=tk.X, pady=(0, 10))

        # Customer Claim Number
        ttk.Label(left_col, text=self.lang.get('lbl_customer_claim_num', 'N° Reclamo Cliente') + " *:").pack(anchor=tk.W)
        self.var_customer_claim = tk.StringVar()
        ttk.Entry(left_col, textvariable=self.var_customer_claim, width=30).pack(fill=tk.X, pady=(0, 10))

        # Short Description
        ttk.Label(left_col, text=self.lang.get('lbl_description', 'Descrizione Breve') + " *:").pack(anchor=tk.W)
        self.var_description = tk.StringVar()
        ttk.Entry(left_col, textvariable=self.var_description, width=30).pack(fill=tk.X, pady=(0, 10))

        # Quantity
        ttk.Label(left_col, text=self.lang.get('lbl_quantity', 'Quantità') + " *:").pack(anchor=tk.W)
        self.var_quantity = tk.StringVar(value="1")
        ttk.Spinbox(
            left_col,
            from_=1,
            to=9999,
            textvariable=self.var_quantity,
            width=30
        ).pack(fill=tk.X, pady=(0, 10))

        # ===== COLONNA CENTRALE: DETTAGLI TECNICI =====
        center_col = ttk.Frame(header_frame)
        center_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Claim Type
        ttk.Label(center_col, text=self.lang.get('lbl_claim_type', 'Tipo Reclamo') + " *:").pack(anchor=tk.W)
        self.var_claim_type = tk.StringVar()
        self.combo_claim_type = ttk.Combobox(
            center_col,
            textvariable=self.var_claim_type,
            state='readonly',
            width=30
        )
        claim_type_values = [ct[1] for ct in self.combo_data.get('claim_types', [])]
        self.combo_claim_type['values'] = claim_type_values
        self.combo_claim_type.pack(fill=tk.X, pady=(0, 10))

        # Product
        ttk.Label(center_col, text=self.lang.get('lbl_product', 'Prodotto') + " *:").pack(anchor=tk.W)
        self.var_product = tk.StringVar()
        self.combo_product = ttk.Combobox(
            center_col,
            textvariable=self.var_product,
            state='normal',  # Cambiato da readonly a normal per permettere editing
            width=30
        )
        # Salva la lista completa dei prodotti per il filtro
        self.all_products = [f"{p[1]} - {p[2]}" for p in self.combo_data.get('products', [])]
        product_values = self.all_products
        self.combo_product['values'] = product_values
        # Aggiungi binding per filtrare mentre l'utente digita
        self.combo_product.bind('<KeyRelease>', self._filter_products)
        self.combo_product.pack(fill=tk.X, pady=(0, 10))

        # Date Claim
        ttk.Label(center_col, text=self.lang.get('lbl_date_claim', 'Data Reclamo') + " *:").pack(anchor=tk.W)
        self.date_claim_picker = DateEntry(
            center_col,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.date_claim_picker.pack(fill=tk.X, pady=(0, 10))

        # Target Date
        ttk.Label(center_col, text=self.lang.get('lbl_target_date', 'Data Target') + " *:").pack(anchor=tk.W)
        self.date_target_picker = DateEntry(
            center_col,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.date_target_picker.pack(fill=tk.X, pady=(0, 10))

        # ===== COLONNA DESTRA: TRASPORTO E DOCUMENTI =====
        right_col = ttk.Frame(header_frame)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # AWB
        ttk.Label(right_col, text=self.lang.get('lbl_awb', 'AWB') + ":").pack(anchor=tk.W)
        self.var_awb = tk.StringVar()
        ttk.Entry(right_col, textvariable=self.var_awb, width=30).pack(fill=tk.X, pady=(0, 10))

        # Transport Document
        ttk.Label(right_col, text=self.lang.get('lbl_transport_doc', 'Documento Trasporto') + ":").pack(anchor=tk.W)
        self.var_transport_doc = tk.StringVar()
        ttk.Entry(right_col, textvariable=self.var_transport_doc, width=30).pack(fill=tk.X, pady=(0, 10))

        # Document Type (NEW - DISABLED initially)
        ttk.Label(right_col, text=self.lang.get('lbl_doc_type', 'Tipo Documento') + ":").pack(anchor=tk.W)
        self.var_doc_type = tk.StringVar()
        self.combo_doc_type = ttk.Combobox(
            right_col,
            textvariable=self.var_doc_type,
            state='disabled',
            width=30
        )
        doc_type_values = [dt[1] for dt in self.combo_data.get('doc_types', [])]
        self.combo_doc_type['values'] = doc_type_values
        self.combo_doc_type.pack(fill=tk.X, pady=(0, 10))

        # Document Upload Button (NEW)
        self.btn_upload_doc = ttk.Button(
            right_col,
            text=self.lang.get('btn_upload_doc', 'Carica Documento'),
            command=self._upload_claim_document,
            state=tk.DISABLED
        )
        self.btn_upload_doc.pack(fill=tk.X, pady=(0, 10))

        # Document Count Label (NEW)
        self.lbl_doc_count = ttk.Label(
            right_col,
            text=self.lang.get('lbl_doc_count', 'Documenti caricati: 0'),
            foreground='gray'
        )
        self.lbl_doc_count.pack(anchor=tk.W, pady=(0, 10))

        # Internal Claim Number
        ttk.Label(right_col, text=self.lang.get('lbl_internal_claim_num', 'N° Reclamo Interno') + ":").pack(anchor=tk.W)
        self.var_internal_claim = tk.StringVar(
            value=ComplaintsNumerationManager.generate_internal_claim_number()
        )
        ttk.Entry(
            right_col,
            textvariable=self.var_internal_claim,
            state='readonly',
            width=30
        ).pack(fill=tk.X, pady=(0, 10))

        # ===== PULSANTI NELLA TESTATA =====
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        # Bottone per gestione prodotti (a sinistra)
        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_manage_products', 'Gestione Prodotti'),
            command=self._open_products_management
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Bottone per refresh manuale prodotti
        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_refresh_products', '🔄 Refresh Prodotti'),
            command=self._manual_refresh_products
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Frame(buttons_frame).pack(side=tk.LEFT, expand=True)

        # Bottone Annulla (prima a destra, meno prominente)
        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Pulsante per modificare la testata (inizialmente nascosto)
        self.btn_edit_header = ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_edit_header', 'Modifica Testata'),
            command=self._edit_header
        )
        # Il pulsante viene mostrato solo dopo il salvataggio
        # Non fare pack qui, lo faremo in _enable_details_section
        
        # Bottone Salva Testata (più a destra, più prominente)
        self.btn_save_header = ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_save', 'Salva Testata'),
            command=self._save_header
        )
        self.btn_save_header.pack(side=tk.RIGHT, padx=(5, 0))

    def _create_claim_details_frame(self, parent):
        """Crea il frame per le righe di dettaglio del reclamo"""
        self.details_frame = ttk.LabelFrame(
            parent,
            text=self.lang.get('lbl_claim_details', 'Dettagli Reclamo'),
            padding=10
        )
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.info_label = ttk.Label(
            self.details_frame,
            text=self.lang.get('msg_enter_quantity', 'Salvare la testata per aggiungere le righe'),
            foreground='gray'
        )
        self.info_label.pack(pady=20)

        # Frame per il filtro LabelCode
        filter_frame = ttk.Frame(self.details_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(
            filter_frame, 
            text=self.lang.get('lbl_filter_labelcode', 'Filtra per Label Code:')
        ).pack(side=tk.LEFT, padx=5)
        
        self.var_labelcode_filter = tk.StringVar()
        self.entry_labelcode_filter = ttk.Entry(
            filter_frame,
            textvariable=self.var_labelcode_filter,
            width=30
        )
        self.entry_labelcode_filter.pack(side=tk.LEFT, padx=5)
        self.entry_labelcode_filter.bind('<KeyRelease>', self._filter_label_codes)
        
        # Bottone per pulire il filtro
        ttk.Button(
            filter_frame,
            text=self.lang.get('btn_clear_filter', 'X'),
            command=self._clear_labelcode_filter,
            width=3
        ).pack(side=tk.LEFT, padx=2)

        self.tree_details = None
        self._create_details_treeview()

        self.details_buttons_frame = ttk.Frame(self.details_frame)
        self.details_buttons_frame.pack(fill=tk.X, pady=(10, 0))

        # Bottoni azioni righe in ordine logico: Aggiungi → Modifica → Rimuovi
        self.btn_add_row = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_add_detail_row', 'Aggiungi Riga'),
            command=self._add_detail_row,
            state=tk.DISABLED
        )
        self.btn_add_row.pack(side=tk.LEFT, padx=5)
        
        self.btn_edit_row = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_edit_detail_row', 'Modifica Riga'),
            command=self._edit_detail_row,
            state=tk.DISABLED
        )
        self.btn_edit_row.pack(side=tk.LEFT, padx=5)

        self.btn_remove_row = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_remove_detail_row', 'Rimuovi Riga'),
            command=self._remove_detail_row,
            state=tk.DISABLED
        )
        self.btn_remove_row.pack(side=tk.LEFT, padx=5)

        ttk.Frame(self.details_buttons_frame).pack(side=tk.LEFT, expand=True)

        self.btn_save_final = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_save', 'Salva Reclamo'),
            command=self._save_complaint,
            state=tk.DISABLED
        )
        self.btn_save_final.pack(side=tk.RIGHT, padx=(0, 5))

    def _create_details_treeview(self):
        """Crea la Treeview per i dettagli"""
        if self.tree_details:
            self.tree_details.destroy()

        columns = ('Num', 'Label', 'Defect', 'Inspection', 'RootCause', 'Corrective', 'Preventive', 'Status')
        self.tree_details = ttk.Treeview(
            self.details_frame,
            columns=columns,
            height=10,
            show='headings'
        )

        self.tree_details.column('Num', width=50)
        self.tree_details.column('Label', width=100)
        self.tree_details.column('Defect', width=150)
        self.tree_details.column('Inspection', width=120)
        self.tree_details.column('RootCause', width=150)
        self.tree_details.column('Corrective', width=150)
        self.tree_details.column('Preventive', width=150)
        self.tree_details.column('Status', width=100)

        self.tree_details.heading('Num', text=self.lang.get('col_num', 'N°'))
        self.tree_details.heading('Label', text=self.lang.get('col_label', 'Label Cod'))
        self.tree_details.heading('Defect', text=self.lang.get('col_defect', 'Difetto'))
        self.tree_details.heading('Inspection', text=self.lang.get('col_inspection', 'Ispez. Iniziale'))
        self.tree_details.heading('RootCause', text=self.lang.get('col_root_cause', 'Causa Radice'))
        self.tree_details.heading('Corrective', text=self.lang.get('col_corrective', 'Az. Correttiva'))
        self.tree_details.heading('Preventive', text=self.lang.get('col_preventive', 'Az. Preventiva'))
        self.tree_details.heading('Status', text=self.lang.get('col_status', 'Stato'))

        scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, command=self.tree_details.yview)
        self.tree_details['yscroll'] = scrollbar.set

        self.tree_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding doppio-click per modificare riga
        self.tree_details.bind('<Double-1>', self._on_detail_double_click)

    # =========================================================================
    # FILTRI E HELPER UI
    # =========================================================================

    def _filter_products(self, event=None):
        """Filtra i prodotti in base al testo digitato nel combo."""
        typed_text = self.var_product.get().lower()
        
        if not typed_text:
            # Se il campo è vuoto, mostra tutti i prodotti
            self.combo_product['values'] = self.all_products
        else:
            # Filtra i prodotti che contengono il testo digitato
            filtered = [p for p in self.all_products if typed_text in p.lower()]
            self.combo_product['values'] = filtered

    def _on_client_selected(self, event=None):
        """Gestisce la selezione del cliente (placeholder per future implementazioni)."""
        pass

    def _filter_label_codes(self, event=None):
        """Filtra le righe dei dettagli in base al LabelCode digitato."""
        if not self.tree_details:
            return
            
        filter_text = self.var_labelcode_filter.get().lower().strip()
        
        # Ottieni tutte le righe
        all_items = self.tree_details.get_children()
        
        if not filter_text:
            # Se il filtro è vuoto, mostra tutte le righe
            for item in all_items:
                self.tree_details.reattach(item, '', 'end')
        else:
            # Nascondi le righe che non corrispondono al filtro
            for item in all_items:
                values = self.tree_details.item(item, 'values')
                # values[1] è il LabelCode (seconda colonna dopo Num)
                if len(values) > 1:
                    label_code = str(values[1]).lower()
                    if filter_text in label_code:
                        # Mostra la riga
                        self.tree_details.reattach(item, '', 'end')
                    else:
                        # Nascondi la riga
                        self.tree_details.detach(item)

    def _clear_labelcode_filter(self):
        """Pulisce il filtro LabelCode e mostra tutte le righe."""
        self.var_labelcode_filter.set('')
        self._filter_label_codes()

    def _edit_header(self):
        """Permette la modifica della testata già salvata."""
        # Riabilita i campi della testata
        self.combo_client.config(state='readonly')
        self.combo_claim_type.config(state='readonly')
        self.combo_product.config(state='normal')
        
        # Cambia il pulsante in "Aggiorna Testata"
        self.btn_save_header.config(text=self.lang.get('btn_update_header', 'Aggiorna Testata'))
        
        # Nascondi "Modifica Testata" e mostra "Aggiorna Testata"
        self.btn_edit_header.pack_forget()
        self.btn_save_header.pack(side=tk.RIGHT, padx=(0, 5))

    def _update_header(self):
        """Aggiorna la testata del reclamo già salvata."""
        if not self.claim_log_id:
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                'Nessuna testata da aggiornare',
                parent=self
            )
            return
            
        is_valid, error_msg = self._validate_header()
        if not is_valid:
            messagebox.showerror(
                self.lang.get('err_validation', 'Errore Validazione'),
                error_msg,
                parent=self
            )
            return

        try:
            claim_header = self._prepare_header_data()
            if claim_header is None:
                return

            # Aggiorna la testata nel database
            success = self.db.update_claim_header(self.claim_log_id, claim_header)
            
            if success:
                self.claim_header = claim_header
                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('msg_header_updated', 'Testata aggiornata con successo'),
                    parent=self
                )
                
                # Ritorna alla modalità visualizzazione
                self._enable_details_section()
            else:
                error_msg = self.lang.get('err_update_failed', "Errore nell'aggiornamento della testata")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    error_msg,
                    parent=self
                )
                
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore aggiornamento testata: {e}")
            error_msg = self.lang.get('err_update_error', "Errore durante l'aggiornamento")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{error_msg}: {str(e)}",
                parent=self
            )




    # =========================================================================
    # LOGICA DI VALIDAZIONE E SALVATAGGIO
    # =========================================================================

    def _validate_header(self) -> Tuple[bool, str]:
        """Valida i dati della testata"""
        if not self.var_client.get():
            return False, self.lang.get('err_client_required', 'Cliente obbligatorio')

        if not self.var_customer_claim.get().strip():
            return False, self.lang.get('err_customer_claim_required', 'N° Reclamo Cliente obbligatorio')

        if not self.var_description.get().strip():
            return False, self.lang.get('err_description_required', 'Descrizione obbligatoria')

        if not self.var_claim_type.get():
            return False, self.lang.get('err_claim_type_required', 'Tipo Reclamo obbligatorio')

        if not self.var_product.get():
            return False, self.lang.get('err_product_required', 'Prodotto obbligatorio')

        try:
            qty = int(self.var_quantity.get())
            if qty <= 0:
                return False, self.lang.get('err_quantity_required', 'Quantità deve essere > 0')
        except ValueError:
            return False, self.lang.get('err_invalid_quantity', 'Quantità non valida')

        return True, ""

    def _prepare_header_data(self) -> Optional[ClaimHeader]:
        """Prepara i dati della testata dal form"""
        try:
            client_text = self.var_client.get()
            client_id = self.combo_data['clients_map'].get(client_text, 0)

            if client_id == 0:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_client_id_not_found', 'Cliente non trovato'),
                    parent=self
                )
                return None

            product_text = self.var_product.get()
            product_id = self.combo_data['products_map'].get(product_text, 0)

            if product_id == 0:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_product_id_not_found', 'Prodotto non trovato'),
                    parent=self
                )
                return None

            claim_type_text = self.var_claim_type.get()
            claim_type_id = self.combo_data['claim_types_map'].get(claim_type_text, 0)

            if claim_type_id == 0:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_claim_type_id_not_found', 'Tipo reclamo non trovato'),
                    parent=self
                )
                return None

            header = ClaimHeader(
                ClaimTypeId=claim_type_id,
                IdProduct=product_id,
                DateClaim=self.date_claim_picker.get_date().strftime('%Y-%m-%d'),
                AWB=self.var_awb.get() if self.var_awb.get() else "",
                TransportDocument=self.var_transport_doc.get() if self.var_transport_doc.get() else "",
                CustomerClaimNumber=self.var_customer_claim.get(),
                InternalClaimNumber=self.var_internal_claim.get(),
                ShortClaimDescription=self.var_description.get(),
                TargetDate=self.date_target_picker.get_date().strftime('%Y-%m-%d'),
                Quantity=int(self.var_quantity.get()),
                IDFinalClient=client_id,
                ClaimDecisionId=None,
                USERName=self.authenticated_user,
                DateSys=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            logger.debug(f"[ADD_COMPLAINT] ClaimHeader preparato correttamente")
            return header

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore preparazione dati: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_prepare_header', 'Errore nella preparazione dei dati')}: {str(e)}",
                parent=self
            )
            return None

    def _save_header(self):
        """Salva la testata del reclamo"""
        logger.info("[ADD_COMPLAINT] === INIZIO _save_header ===")

        # Se la testata è già stata salvata, chiama _update_header
        if self.header_saved:
            self._update_header()
            return

        is_valid, error_msg = self._validate_header()
        if not is_valid:
            logger.error(f"[ADD_COMPLAINT] Validazione fallita: {error_msg}")
            messagebox.showerror(
                self.lang.get('err_validation', 'Errore Validazione'),
                error_msg,
                parent=self
            )
            return

        try:
            claim_header = self._prepare_header_data()

            if claim_header is None:
                logger.error("[ADD_COMPLAINT] ❌ Errore: claim_header è None")
                return

            logger.info(f"[ADD_COMPLAINT] Salvataggio testata reclamo: {claim_header.InternalClaimNumber}")

            self.claim_log_id = self.db.insert_claim_header(claim_header)

            if not self.claim_log_id:
                logger.error("[ADD_COMPLAINT] ❌ insert_claim_header ha restituito None/0")
                messagebox.showerror(
                    self.lang.get('err_save_failed', 'Salvataggio Fallito'),
                    self.lang.get('msg_error_saving_complaint', 'Errore durante il salvataggio della testata'),
                    parent=self
                )
                return

            logger.info(f"[ADD_COMPLAINT] ✅ Testata salvata con ID: {self.claim_log_id}")

            self.claim_header = claim_header
            self.header_saved = True
            self.rows_to_add = int(self.var_quantity.get())

            self._enable_details_section()

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                f"{self.lang.get('msg_complaint_added', 'Testata salvata con successo')}\n\n" +
                f"{self.lang.get('msg_rows_to_add', 'Righe da aggiungere: ')}{self.rows_to_add}",
                parent=self
            )

            logger.info("[ADD_COMPLAINT] === FINE _save_header (SUCCESSO) ===")

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] ❌ Exception in _save_header: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_save_error', 'Errore nel salvataggio')}: {str(e)}",
                parent=self
            )

    def _enable_details_section(self):
        """Abilita la sezione dettagli dopo il salvataggio della testata"""
        self.info_label.config(
            text=f"{self.lang.get('msg_rows_to_add', 'Righe da aggiungere: ')}{self.rows_to_add}",
            foreground='black'
        )

        self.btn_add_row.config(state=tk.NORMAL)
        self.btn_remove_row.config(state=tk.NORMAL)
        self.btn_edit_row.config(state=tk.NORMAL)  # Abilita anche Edit
        self.btn_save_final.config(state=tk.NORMAL)
        self.btn_upload_doc.config(state=tk.NORMAL)  # Enable document upload
        self.combo_doc_type.config(state='readonly')  # Enable document type selection

        # Nascondi "Salva Testata" e mostra "Modifica Testata"
        self.btn_save_header.pack_forget()
        self.btn_edit_header.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Disabilita i campi della testata
        self.combo_client.config(state='disabled')
        self.combo_claim_type.config(state='disabled')
        self.combo_product.config(state='disabled')

    def _upload_claim_document(self):
        """Carica un documento per il reclamo (NEW)"""
        if not self.claim_log_id:
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                'Salvare prima la testata del reclamo',
                parent=self
            )
            return

        if not self.var_doc_type.get():
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                'Selezionare un tipo di documento',
                parent=self
            )
            return

        filetypes = [
            (self.lang.get('file_all', 'Tutti i file'), "*.*"),
            (self.lang.get('file_pdf', 'File PDF'), "*.pdf"),
            (self.lang.get('file_images', 'Immagini'), "*.png *.jpg *.jpeg *.gif *.bmp"),
            (self.lang.get('file_excel', 'File Excel'), "*.xlsx *.xls"),
            (self.lang.get('file_word', 'File Word'), "*.docx *.doc"),
        ]

        try:
            filepath = filedialog.askopenfilename(
                parent=self,
                title=self.lang.get('title_select_file', 'Seleziona file documento'),
                filetypes=filetypes
            )

            if filepath:
                file_size = os.path.getsize(filepath)
                max_size = 10 * 1024 * 1024  # 10 MB

                if file_size > max_size:
                    messagebox.showerror(
                        self.lang.get('err_file_too_large', 'File Troppo Grande'),
                        f"Dimensione massima: 10 MB\nDimensione file: {file_size / (1024 * 1024):.2f} MB",
                        parent=self
                    )
                    return

                with open(filepath, 'rb') as f:
                    file_binary = f.read()
                file_name = os.path.basename(filepath)

                doc_type_text = self.var_doc_type.get()
                doc_type_id = self.combo_data['doc_types_map'].get(doc_type_text, 0)

                if doc_type_id == 0:
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        'Tipo documento non valido',
                        parent=self
                    )
                    return

                success = self.db.save_claim_document(
                    self.claim_log_id,
                    doc_type_id,
                    file_binary,
                    file_name
                )

                if success:
                    self._update_document_count_label()
                    messagebox.showinfo(
                        self.lang.get('success', 'Successo'),
                        f'Documento "{file_name}" caricato con successo',
                        parent=self
                    )
                else:
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        'Errore nel salvataggio del documento',
                        parent=self
                    )

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore upload documento: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"Errore nel caricamento del file: {str(e)}",
                parent=self
            )

    def _update_document_count_label(self):
        """Aggiorna il label con il conteggio documenti (NEW)"""
        if self.claim_log_id:
            count = self.db.get_claim_documents_count(self.claim_log_id)
            self.lbl_doc_count.config(
                text=f"{self.lang.get('lbl_doc_count', 'Documenti caricati')}: {count}",
                foreground='black' if count > 0 else 'gray'
            )

    def _add_detail_row(self):
        """Aggiunge una nuova riga di dettaglio"""
        if len(self.tree_details.get_children()) >= self.rows_to_add:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                f"Non puoi aggiungere più di {self.rows_to_add} righe",
                parent=self
            )
            return

        self._open_detail_editor()

    def _remove_detail_row(self):
        """Rimuove la riga di dettaglio selezionata"""
        selection = self.tree_details.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('msg_select_row', 'Selezionare una riga'),
                parent=self
            )
            return

        if messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('msg_confirm_delete', "Confermare l'eliminazione della riga?"),
            parent=self
        ):
            for item in selection:
                self.tree_details.delete(item)

    def _edit_detail_row(self):
        """Modifica la riga di dettaglio selezionata"""
        selection = self.tree_details.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('msg_select_row', 'Selezionare una riga'),
                parent=self
            )
            return
        
        # Prendi il primo elemento selezionato
        selected_item = selection[0]
        item_values = self.tree_details.item(selected_item, 'values')
        
        # Recupera i dati dal tree (row_idx è il numero progressivo - 1)
        row_idx = int(item_values[0]) - 1
        
        # Crea un dict con i dati attuali per popolare l'editor
        detail_data = {
            'LabelCod': item_values[1],
            'ClaimDefectId': self.combo_data['defects_map'].get(item_values[2]),
            'FirstInspectionResultId': self.combo_data['inspection_map'].get(item_values[3]),
            'RootCause': item_values[4],
            'SummaryCorrectiveAction': item_values[5],
            'SummaryPreventiveAction': item_values[6],
            'ClaimStatusId': self.combo_data['status_map'].get(item_values[7])
        }
        
        logger.info(f"[EDIT_ROW] Dati TreeView: {item_values}")
        logger.info(f"[EDIT_ROW] Detail_data: {detail_data}")
        
        # Se è già stato salvato nel DB, passa anche il detail_id
        # Per ora assumiamo che i dettagli salvati abbbiado un tag 'detail_id'
        detail_id = None
        tags = self.tree_details.item(selected_item, 'tags')
        if tags and len(tags) > 0:
            try:
                detail_id = int(tags[0])
            except:
                pass
        
        # Apri l'editor con i dati esistenti
        DetailEditorWindow(
            self, self.db, self.lang, self.combo_data, row_idx,
            lambda data: self._update_row_in_tree(selected_item, data),
            detail_id=detail_id,
            detail_data=detail_data
        )
    
    def _on_detail_double_click(self, event):
        """Gestisce il doppio click su una riga per modificarla"""
        # Simula il click sul pulsante Edit
        self._edit_detail_row()

    def _open_detail_editor(self, row_idx: Optional[int] = None):
        """Apre la finestra di editing per una riga di dettaglio"""
        DetailEditorWindow(self, self.db, self.lang, self.combo_data, row_idx, self._add_row_to_tree)

    def _update_row_in_tree(self, item_id, row_data: Dict):
        """Aggiorna una riga esistente nella treeview"""
        # Mantieni il numero progressivo esistente
        current_values = self.tree_details.item(item_id, 'values')
        num = current_values[0]  # Numero progressivo
        
        values = (
            num,
            row_data.get('label', ''),
            row_data.get('defect', ''),
            row_data.get('inspection', ''),
            row_data.get('root_cause', ''),
            row_data.get('corrective', ''),
            row_data.get('preventive', ''),
            row_data.get('status', '')
        )
        
        # Aggiorna i valori
        self.tree_details.item(item_id, values=values)
        
        # Se c'è un detail_id (UPDATE su DB), mantieni il tag
        if 'detail_id' in row_data:
            self.tree_details.item(item_id, tags=(str(row_data['detail_id']),))

    def _add_row_to_tree(self, row_data: Dict):
        """Aggiunge una riga alla treeview"""
        num = len(self.tree_details.get_children()) + 1
        values = (
            num,
            row_data.get('label', ''),
            row_data.get('defect', ''),
            row_data.get('inspection', ''),
            row_data.get('root_cause', ''),
            row_data.get('corrective', ''),
            row_data.get('preventive', ''),
            row_data.get('status', '')
        )

        self.tree_details.insert('', 'end', values=values)

    def _save_complaint(self):
        """Salva il reclamo completo con tutti i dettagli"""
        if not self.header_saved:
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                self.lang.get('msg_save_header_first', 'Salvare prima la testata'),
                parent=self
            )
            return

        try:
            rows_inserted = len(self.tree_details.get_children())

            # STRICT VALIDATION: Require exact match (NEW)
            if rows_inserted != self.rows_to_add:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    f"Devi inserire esattamente {self.rows_to_add} righe di dettaglio.\n" +
                    f"Attualmente inserite: {rows_inserted}",
                    parent=self
                )
                return

            # Prepara i dettagli dalla treeview
            claim_details = []
            for item in self.tree_details.get_children():
                values = self.tree_details.item(item)['values']

                defect_text = values[2]
                defect_id = self.combo_data['defects_map'].get(defect_text)

                inspection_text = values[3]
                inspection_id = self.combo_data['inspection_map'].get(inspection_text)

                status_text = values[7]
                status_id = self.combo_data['status_map'].get(status_text)

                detail = {
                    'FirstInspectionResultId': inspection_id,
                    'LabelCod': values[1],
                    'RootCause': values[4],
                    'SummaryCorrectiveAction': values[5],
                    'SummaryPreventiveAction': values[6],
                    'ClaimStatusId': status_id,
                    'ClaimDefectId': defect_id
                }
                claim_details.append(detail)

            # Salva i dettagli
            if claim_details:
                success = self.db.insert_claim_details(self.claim_log_id, claim_details)

                if not success:
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        self.lang.get('msg_error_saving_details', 'Errore nel salvataggio dei dettagli'),
                        parent=self
                    )
                    return

            logger.info(f"[ADD_COMPLAINT] Reclamo completo salvato: {self.claim_header.InternalClaimNumber}")

            # Send email notification (NEW)
            try:
                self.db.send_claim_notification_email(self.claim_log_id, self.claim_header)
                logger.info("[ADD_COMPLAINT] Email notifica inviata")
            except Exception as email_error:
                logger.warning(f"[ADD_COMPLAINT] Errore invio email: {email_error}")
                # Don't fail the save if email fails

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('msg_complaint_added', 'Reclamo salvato con successo'),
                parent=self
            )

            self.destroy()

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore salvataggio reclamo: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_save_error', 'Errore nel salvataggio')}: {str(e)}",
                parent=self
            )

    def _on_client_selected(self, event=None):
        """Filtra i prodotti in base al cliente selezionato."""
        client_text = self.var_client.get()
        if not client_text:
            # Nessun cliente selezionato, mostra tutti i prodotti
            product_values = [f"{p[1]} - {p[2]}" for p in self.combo_data.get('products', [])]
            self.combo_product['values'] = product_values
            return
        
        # Ottieni l'ID del cliente selezionato
        client_id = self.combo_data['clients_map'].get(client_text)
        
        if not client_id:
            logger.warning(f"[ADD_COMPLAINT] Cliente non trovato: {client_text}")
            return
        
        # Filtra i prodotti per questo cliente
        all_products = self.combo_data.get('products', [])
        filtered_products = [p for p in all_products if p[3] == client_id]  # p[3] è IDFinalClient
        
        if not filtered_products:
            logger.warning(f"[ADD_COMPLAINT] Nessun prodotto trovato per cliente ID {client_id}")
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                f"Nessun prodotto associato al cliente selezionato.\n\n"
                f"Usa il bottone 'Gestione Prodotti' per associare prodotti al cliente.",
                parent=self
            )
            self.combo_product['values'] = []
            self.var_product.set('')
        else:
            product_values = [f"{p[1]} - {p[2]}" for p in filtered_products]
            self.combo_product['values'] = product_values
            # Aggiorna la mappa dei prodotti filtrati
            self.combo_data['products_map'] = {f"{p[1]} - {p[2]}": p[0] for p in filtered_products}
            logger.debug(f"[ADD_COMPLAINT] Prodotti filtrati per cliente {client_id}: {len(filtered_products)}")
    
    def _open_products_management(self):
        """Apre la gestione prodotti senza login aggiuntivo."""
        try:
            # Usa l'utente già autenticato per aprire la gestione prodotti
            if hasattr(self.parent, 'traceability_manager'):
                # Rilascia il grab PERMANENTEMENTE
                # La finestra prodotti deve poter essere usata liberamente
                self.grab_release()
                logger.info("[ADD_COMPLAINT] Grab rilasciato per apertura gestione prodotti")
                
                # Apri la gestione prodotti
                self.parent.traceability_manager.open_define_products(self.authenticated_user)
                
                # NON riprendere il grab qui!
                # La finestra prodotti è ora aperta e deve rimanere interattiva
                # Il grab verrà ripreso solo quando l'utente chiude questa form complaints
                
                logger.info("[ADD_COMPLAINT] Gestione prodotti aperta - grab NON ripreso")
                
            else:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_cannot_open_products', 'Impossibile aprire la gestione prodotti'),
                    parent=self
                )
                logger.error("[ADD_COMPLAINT] parent.traceability_manager non trovato")
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore apertura gestione prodotti: {e}")
            err_msg = self.lang.get('err_opening_products', 'Errore nell\'apertura della gestione prodotti')
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{err_msg}: {str(e)}",
                parent=self
            )
    
    def _reload_products_data(self):
        """Ricarica i dati dei prodotti dal database."""
        try:
            query_products = """
                             SELECT idproduct, ProductCode, ProductName, IDFinalClient
                             FROM products
                             WHERE CHARINDEX('cipr', ProductCode, 1) = 0
                               AND CHARINDEX('RMA', ProductCode, 1) = 0
                             ORDER BY ProductCode
                             """
            products = self.db.fetch_all(query_products)
            self.combo_data['products'] = products
            self.combo_data['products_map'] = {f"{p[1]} - {p[2]}": p[0] for p in products}
            logger.info(f"[ADD_COMPLAINT] Prodotti ricaricati: {len(products)}")
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore ricaricamento prodotti: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"Errore nel ricaricamento dei prodotti: {str(e)}",
                parent=self
            )
    
    def _manual_refresh_products(self):
        """Ricarica manualmente i dati dei prodotti su richiesta dell'utente."""
        try:
            logger.info("[ADD_COMPLAINT] Refresh manuale prodotti richiesto dall'utente")
            self._reload_products_data()
            
            # Riapplica il filtro se c'è un cliente selezionato
            if self.var_client.get():
                self._on_client_selected()
            
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('msg_products_updated', 'Dati prodotti aggiornati!'),
                parent=self
            )
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore refresh manuale: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_refresh_failed', 'Errore durante il refresh')}: {str(e)}",
                parent=self
            )


class DetailEditorWindow(tk.Toplevel):
    """Finestra per editing dettagli reclamo"""

    def __init__(self, parent, db, lang, combo_data, row_idx, callback, detail_id=None, detail_data=None):
        super().__init__(parent)

        self.parent = parent
        self.db = db
        self.lang = lang
        self.combo_data = combo_data
        self.row_idx = row_idx
        self.callback = callback
        self.labelcode_verified = False
        self.query_results = None
        
        # Modalità modifica o creazione
        self.detail_id = detail_id  # Se valorizzato, la riga è già nel DB
        self.detail_data = detail_data  # Dati esistenti da modificare
        # Modalità modifica se ci sono dati da popolare (anche se non ancora salvati nel DB)
        self.is_edit_mode = detail_data is not None

        title = lang.get('title_edit_detail', 'Modifica Dettaglio') if self.is_edit_mode else lang.get('title_add_detail', 'Aggiungi Dettaglio')
        self.title(title)
        self.geometry('600x500')
        self.resizable(False, False)

        self._create_widgets()
        
        # Se siamo in modalità modifica, popola i campi
        if self.is_edit_mode:
            logger.info(f"[DETAIL_EDITOR] Chiamando _populate_fields() - is_edit_mode: {self.is_edit_mode}")
            self._populate_fields()

        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        """Crea l'interfaccia"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Label Code with confirmation button
        label_frame = ttk.Frame(main_frame)
        label_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(label_frame, text=self.lang.get('lbl_label_cod', 'Label Cod') + " *:").pack(anchor=tk.W)
        
        entry_frame = ttk.Frame(label_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.var_label = tk.StringVar()
        self.entry_label = ttk.Entry(entry_frame, textvariable=self.var_label)
        self.entry_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_confirm_label = ttk.Button(
            entry_frame, 
            text=self.lang.get('btn_confirm', 'Conferma'),
            command=self._verify_labelcode
        )
        self.btn_confirm_label.pack(side=tk.LEFT)

        # Defect
        ttk.Label(main_frame, text=self.lang.get('lbl_defect', 'Difetto') + " *:").pack(anchor=tk.W)
        self.var_defect = tk.StringVar()
        self.combo_defect = ttk.Combobox(main_frame, textvariable=self.var_defect, state='readonly')
        defect_values = [d[1] for d in self.combo_data.get('defects', [])]
        self.combo_defect['values'] = defect_values
        self.combo_defect.pack(fill=tk.X, pady=(0, 10))

        # Inspection
        ttk.Label(main_frame, text=self.lang.get('lbl_inspection', 'Ispezione Iniziale') + " *:").pack(anchor=tk.W)
        self.var_inspection = tk.StringVar()
        self.combo_inspection = ttk.Combobox(main_frame, textvariable=self.var_inspection, state='readonly')
        inspection_values = [i[1] for i in self.combo_data.get('inspection_results', [])]
        self.combo_inspection['values'] = inspection_values
        self.combo_inspection.pack(fill=tk.X, pady=(0, 10))

        # Root Cause
        ttk.Label(main_frame, text=self.lang.get('lbl_root_cause', 'Causa Radice') + ":").pack(anchor=tk.W)
        self.var_root_cause = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.var_root_cause).pack(fill=tk.X, pady=(0, 10))

        # Corrective Action
        ttk.Label(main_frame, text=self.lang.get('lbl_corrective', 'Azione Correttiva') + ":").pack(anchor=tk.W)
        self.var_corrective = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.var_corrective).pack(fill=tk.X, pady=(0, 10))

        # Preventive Action
        ttk.Label(main_frame, text=self.lang.get('lbl_preventive', 'Azione Preventiva') + ":").pack(anchor=tk.W)
        self.var_preventive = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.var_preventive).pack(fill=tk.X, pady=(0, 10))

        # Status
        ttk.Label(main_frame, text=self.lang.get('lbl_status', 'Stato') + " *:").pack(anchor=tk.W)
        self.var_status = tk.StringVar()
        self.combo_status = ttk.Combobox(main_frame, textvariable=self.var_status, state='readonly')
        status_values = [s[1] for s in self.combo_data.get('claim_status', [])]
        self.combo_status['values'] = status_values
        self.combo_status.pack(fill=tk.X, pady=(0, 10))
        
        # Frame for query results (initially hidden)
        self.results_container = ttk.Frame(main_frame)
        # Don't pack it yet - it will be packed when labelcode is verified
        
        # Phases results
        self.phases_frame = ttk.LabelFrame(
            self.results_container, 
            text=self.lang.get('lbl_phases', 'Fasi'), 
            padding=5
        )
        self.phases_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Create Treeview for phases
        phases_cols = ('OrderNumber', 'PhasePosition', 'PhaseName', 'BoardState', 'ScanResult', 'ScanTimeFinish')
        self.tree_phases = ttk.Treeview(
            self.phases_frame,
            columns=phases_cols,
            height=5,
            show='headings'
        )
        
        self.tree_phases.heading('OrderNumber', text=self.lang.get('col_order', 'Ordine'))
        self.tree_phases.heading('PhasePosition', text=self.lang.get('col_phase_pos', 'Pos'))
        self.tree_phases.heading('PhaseName', text=self.lang.get('col_phase', 'Fase'))
        self.tree_phases.heading('BoardState', text=self.lang.get('col_board_state', 'Stato Board'))
        self.tree_phases.heading('ScanResult', text=self.lang.get('col_scan_result', 'Risultato'))
        self.tree_phases.heading('ScanTimeFinish', text=self.lang.get('col_scan_time', 'Data'))
        
        self.tree_phases.column('OrderNumber', width=100)
        self.tree_phases.column('PhasePosition', width=50)
        self.tree_phases.column('PhaseName', width=150)
        self.tree_phases.column('BoardState', width=100)
        self.tree_phases.column('ScanResult', width=80)
        self.tree_phases.column('ScanTimeFinish', width=150)
        
        phases_scrollbar = ttk.Scrollbar(self.phases_frame, orient=tk.VERTICAL, command=self.tree_phases.yview)
        self.tree_phases['yscroll'] = phases_scrollbar.set
        self.tree_phases.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        phases_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Repairs results
        self.repairs_frame = ttk.LabelFrame(
            self.results_container, 
            text=self.lang.get('lbl_repairs', 'Riparazioni'), 
            padding=5
        )
        self.repairs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for repairs
        repairs_cols = ('RepairDate', 'DefectName', 'DefectArea')
        self.tree_repairs = ttk.Treeview(
            self.repairs_frame,
            columns=repairs_cols,
            height=3,
            show='headings'
        )
        
        self.tree_repairs.heading('RepairDate', text=self.lang.get('col_repair_date', 'Data Riparazione'))
        self.tree_repairs.heading('DefectName', text=self.lang.get('col_defect', 'Difetto'))
        self.tree_repairs.heading('DefectArea', text=self.lang.get('col_area', 'Area'))
        
        self.tree_repairs.column('RepairDate', width=150)
        self.tree_repairs.column('DefectName', width=200)
        self.tree_repairs.column('DefectArea', width=150)
        
        repairs_scrollbar = ttk.Scrollbar(self.repairs_frame, orient=tk.VERTICAL, command=self.tree_repairs.yview)
        self.tree_repairs['yscroll'] = repairs_scrollbar.set
        self.tree_repairs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        repairs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'), command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'), command=self.destroy).pack(side=tk.RIGHT)

    def _populate_fields(self):
        """Popola i campi con i dati esistenti (modalità modifica)"""
        if not self.detail_data:
            logger.warning("[DETAIL_EDITOR] detail_data è None o vuoto")
            return
        
        logger.info(f"[DETAIL_EDITOR] Inizio popolamento con: {self.detail_data}")
        
        # Popola i campi
        label_cod = self.detail_data.get('LabelCod', '')
        self.var_label.set(label_cod)
        logger.info(f"[DETAIL_EDITOR] Label impostato: '{label_cod}'")
        
        # Defect
        defect_id = self.detail_data.get('ClaimDefectId')
        if defect_id:
            for defect in self.combo_data.get('defects', []):
                if defect[0] == defect_id:
                    self.var_defect.set(defect[1])
                    break
        
        # Inspection
        inspection_id = self.detail_data.get('FirstInspectionResultId')
        if inspection_id:
            for inspection in self.combo_data.get('inspection_results', []):
                if inspection[0] == inspection_id:
                    self.var_inspection.set(inspection[1])
                    break
        
        # Status
        status_id = self.detail_data.get('ClaimStatusId')
        if status_id:
            for status in self.combo_data.get('claim_status', []):
                if status[0] == status_id:
                    self.var_status.set(status[1])
                    break
        
        self.var_root_cause.set(self.detail_data.get('RootCause', ''))
        self.var_corrective.set(self.detail_data.get('SummaryCorrectiveAction', ''))
        self.var_preventive.set(self.detail_data.get('SummaryPreventiveAction', ''))
        
        # In modalità modifica, il label code è già verificato
        self.labelcode_verified = True
        self.entry_label.config(state='readonly')
        self.btn_confirm_label.config(state=tk.DISABLED)

    def _verify_labelcode(self):
        """Verifica il labelcode eseguendo la query e confrontando l'IDProduct"""
        labelcode = self.var_label.get().strip()
        
        if not labelcode:
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                self.lang.get('err_labelcode_required', 'Inserire un codice label'),
                parent=self
            )
            self.entry_label.focus()
            return
        
        try:
            # Query SQL fornita dall'utente
            query = """
            select distinct pr.IDProduct,
            pr.ProductCode,
            o.OrderNumber, l.LabelCod, dbo.BoardState(b.BoardState) as BoardState,
            p.IDPhase, p.PhaseName, op.PhasePosition,
            iif (s.IsPass=0,'FAIL', 'PASS') as ScanResult, s.ScanTimeFinish,  
            iif (sd.IsPass=0,'FAIL', 'PASS') as RepairResult, sd.StopTime as RepairDate,  
            d.DefectNameRO, a.AreaName as DefectArea
            from Scannings s
            inner join LabelCodes l on s.IDBoard = l.IDBoard
            inner join Boards b on b.IDBoard = s.IDBoard
            inner join OrderPhases op on s.IDOrderPhase =op.IDOrderPhase
            inner join Orders o on o.IDOrder = op.IDOrder
            inner join Phases p on p.IDPhase = op.IDPhase
            left join ScanDefects sd on  sd.IDScan = s.IDScan
            left join ScanDefectDetails sdd on sd.IDScanDefect = sdd.IDScanDefect
            left join Defects d on d.IDDefect = sdd.IDDefect
            left join Areas a on a.IDArea = sdd.IDArea
            inner join Products Pr on pr.IDProduct=o.IDProduct
            cross apply 
            (select top 1 PhasePosition from 
            OrderPhases 
            where OrderPhases.IDOrder= o.IDOrder 
            and OrderPhases.IDPhase= op.IDPhase
            order by OrderPhases.PhasePosition ) pp
            where l.LabelCod = ?
            and op.PhasePosition>= pp.PhasePosition
            order by op.PhasePosition, s.ScanTimeFinish
            """
            
            logger.info(f"[LABELCODE_VERIFY] Verifica labelcode: {labelcode}")
            results = self.db.fetch_all(query, (labelcode,))
            
            if not results or len(results) == 0:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_labelcode_not_found', 'LabelCode non trovato nel database'),
                    parent=self
                )
                self.entry_label.focus()
                return
            
            # Verifica IDProduct - prende il primo risultato per il confronto
            found_product_id = results[0][0]  # IDProduct è la prima colonna
            
            # Ottieni l'IDProduct dalla testata del reclamo (parent window)
            if hasattr(self.parent, 'claim_header') and self.parent.claim_header:
                expected_product_id = self.parent.claim_header.IdProduct
            else:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    'Impossibile recuperare il prodotto dalla testata del reclamo',
                    parent=self
                )
                return
            
            logger.info(f"[LABELCODE_VERIFY] IDProduct trovato: {found_product_id}, atteso: {expected_product_id}")
            
            # Confronta gli IDProduct
            if found_product_id != expected_product_id:
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_labelcode_wrong_product', 
                                  'ATTENZIONE!\n\n'
                                  'Il LabelCode inserito NON appartiene al prodotto\n'
                                  'per cui si sta inserendo il reclamo.\n\n'
                                  'Verificare il codice e riprovare.'),
                    parent=self
                )
                self.entry_label.focus()
                self.entry_label.selection_range(0, tk.END)
                return
            
            # IDProduct corretto - salva i risultati e mostra la form allargata
            self.query_results = results
            self.labelcode_verified = True
            
            # Disabilita il campo label e il bottone conferma
            self.entry_label.config(state='disabled')
            self.btn_confirm_label.config(state=tk.DISABLED)
            
            # Allarga la finestra
            self.geometry('1200x700')
            
            # Mostra il container dei risultati
            self.results_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            
            # Popola le treeview con i dati
            self._populate_results(results)
            
            logger.info("[LABELCODE_VERIFY] Labelcode verificato con successo")
            
        except Exception as e:
            logger.exception(f"[LABELCODE_VERIFY] Errore durante la verifica: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"Errore durante la verifica del labelcode:\n{str(e)}",
                parent=self
            )
    
    def _populate_results(self, results):
        """Popola le treeview con i risultati della query"""
        # Pulisci le treeview
        for item in self.tree_phases.get_children():
            self.tree_phases.delete(item)
        for item in self.tree_repairs.get_children():
            self.tree_repairs.delete(item)
        
        # Separa i dati delle fasi e delle riparazioni
        phases_data = []
        repairs_data = []
        
        for row in results:
            # row structure:
            # 0: IDProduct, 1: ProductCode, 2: OrderNumber, 3: LabelCod, 4: BoardState,
            # 5: IDPhase, 6: PhaseName, 7: PhasePosition, 8: ScanResult, 9: ScanTimeFinish,
            # 10: RepairResult, 11: RepairDate, 12: DefectNameRO, 13: DefectArea
            
            # Dati delle fasi (sempre presenti)
            phase_data = {
                'OrderNumber': row[2],
                'PhasePosition': row[7],
                'PhaseName': row[6],
                'BoardState': row[4],
                'ScanResult': row[8],
                'ScanTimeFinish': row[9]
            }
            
            # Evita duplicati nelle fasi
            if phase_data not in phases_data:
                phases_data.append(phase_data)
            
            # Dati delle riparazioni (solo se presenti)
            # RepairResult (row[10]) è 'PASS' se non ci sono riparazioni effettive
            # Controlliamo se ci sono dati di riparazione (DefectNameRO, DefectArea, RepairDate)
            if row[12] or row[13] or row[11]:  # Se c'è almeno un dato di riparazione
                repair_data = {
                    'RepairDate': row[11] if row[11] else '',
                    'DefectName': row[12] if row[12] else '',
                    'DefectArea': row[13] if row[13] else ''
                }
                # Evita duplicati nelle riparazioni
                if repair_data not in repairs_data:
                    repairs_data.append(repair_data)
        
        # Popola la treeview delle fasi
        for phase in phases_data:
            self.tree_phases.insert('', 'end', values=(
                phase['OrderNumber'],
                phase['PhasePosition'],
                phase['PhaseName'],
                phase['BoardState'],
                phase['ScanResult'],
                phase['ScanTimeFinish']
            ))
        
        # Popola la treeview delle riparazioni (se presenti)
        if repairs_data:
            for repair in repairs_data:
                self.tree_repairs.insert('', 'end', values=(
                    repair['RepairDate'],
                    repair['DefectName'],
                    repair['DefectArea']
                ))
        else:
            # Se non ci sono riparazioni, aggiungi una riga che dice "Nessuna riparazione"
            self.tree_repairs.insert('', 'end', values=(
                self.lang.get('no_repairs', 'Nessuna riparazione'),
                '',
                ''
            ))

    def _save(self):
        """Salva i dati del dettaglio"""
        if not self.var_label.get().strip():
            messagebox.showerror('Errore', 'Label Cod obbligatorio', parent=self)
            return

        if not self.var_defect.get():
            messagebox.showerror('Errore', 'Difetto obbligatorio', parent=self)
            return

        if not self.var_inspection.get():
            messagebox.showerror('Errore', 'Ispezione Iniziale obbligatoria', parent=self)
            return

        if not self.var_status.get():
            messagebox.showerror('Errore', 'Stato obbligatorio', parent=self)
            return

        row_data = {
            'label': self.var_label.get(),
            'defect': self.var_defect.get(),
            'inspection': self.var_inspection.get(),
            'root_cause': self.var_root_cause.get(),
            'corrective': self.var_corrective.get(),
            'preventive': self.var_preventive.get(),
            'status': self.var_status.get()
        }
        
        # Se siamo in modalità modifica, aggiungi l'ID del dettaglio
        if self.is_edit_mode:
            row_data['detail_id'] = self.detail_id

        self.callback(row_data)
        self.destroy()