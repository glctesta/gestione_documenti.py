"""
Modulo per l'aggiunta di nuovi reclami
Interfaccia grafica e logica di inserimento dati
"""

import tkinter as tk
from tkinter import ttk, messagebox
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
    TransportDocumentData: Optional[bytes] = None  # Cambiato da str a bytes
    CustomerClaimNumber: str = ""
    InternalClaimNumber: str = ""
    ShortClaimDescription: str = ""
    TargetDate: str = ""
    Quantity: int = 1
    IDFinalClient: int = 0
    ClaimDecisionId: Optional[int] = None
    USERName: str = ""
    TransportDocumentFileName: Optional[str] = None
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
                            ORDER BY FinalClientName \
                            """
            clients = self.db.fetch_all(query_clients)
            self.combo_data['clients'] = clients
            self.combo_data['clients_map'] = {f"{c[1]} ({c[2]})": c[0] for c in clients}
            logger.debug(f"[ADD_COMPLAINT] Clienti caricati: {len(clients)}")
            logger.debug(f"[ADD_COMPLAINT] clients_map: {self.combo_data['clients_map']}")

            # Products
            query_products = """
                             SELECT idproduct, ProductCode, ProductName
                             FROM products
                             WHERE CHARINDEX('cipr', ProductCode, 1) = 0
                               AND CHARINDEX('RMA', ProductCode, 1) = 0
                             ORDER BY ProductCode \
                             """
            products = self.db.fetch_all(query_products)
            self.combo_data['products'] = products
            self.combo_data['products_map'] = {f"{p[1]} - {p[2]}": p[0] for p in products}
            logger.debug(f"[ADD_COMPLAINT] Prodotti caricati: {len(products)}")
            logger.debug(f"[ADD_COMPLAINT] products_map: {list(self.combo_data['products_map'].keys())}")

            # Claim Types
            query_types = """
                          SELECT ClaimTypeId, ClaimType
                          FROM [Traceability_RS].[clm].[ClaimTypes]
                          ORDER BY ClaimType \
                          """
            types = self.db.fetch_all(query_types)
            self.combo_data['claim_types'] = types
            self.combo_data['claim_types_map'] = {ct[1]: ct[0] for ct in types}
            logger.debug(f"[ADD_COMPLAINT] Claim Types caricati: {len(types)}")
            logger.debug(f"[ADD_COMPLAINT] claim_types_map: {self.combo_data['claim_types_map']}")

            # First Inspection Results
            query_inspection = """
                               SELECT FirstInspectionResultId, FirstInspectionResult
                               FROM [Traceability_RS].[clm].[FirstInspectionResults]
                               ORDER BY FirstInspectionResult \
                               """
            inspection = self.db.fetch_all(query_inspection)
            self.combo_data['inspection_results'] = inspection
            self.combo_data['inspection_map'] = {i[1]: i[0] for i in inspection}
            logger.debug(f"[ADD_COMPLAINT] Inspection Results caricati: {len(inspection)}")

            # Claim Status
            query_status = """
                           SELECT ClaimStatusId, ClaimStatus, IsEnd
                           FROM [Traceability_RS].[clm].[ClaimStatus] \
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
                            ORDER BY ISNULL(CONCAT(p.ProcessStep, ' - '), '') + c.ClaimDefect \
                            """
            defects = self.db.fetch_all(query_defects)
            self.combo_data['defects'] = defects
            self.combo_data['defects_map'] = {d[1]: d[0] for d in defects}
            logger.debug(f"[ADD_COMPLAINT] Defects caricati: {len(defects)}")

            logger.info("[ADD_COMPLAINT] ✅ Tutti i dati combo caricati con successo")
            logger.debug("[ADD_COMPLAINT] === FINE _load_combo_data ===")

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] ❌ Errore caricamento dati combo: {e}")
            import traceback
            traceback.print_exc()
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

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === HEADER CON LOGO E OROLOGIO ===
        self._create_header(main_frame)

        # === FRAME TESTATA RECLAMO ===
        self._create_claim_header_frame(main_frame)

        # === FRAME RIGHE RECLAMO ===
        self._create_claim_details_frame(main_frame)

    def _create_header(self, parent):
        """Crea l'header con logo e orologio"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Logo a sinistra
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

        # Spazio elastico
        ttk.Frame(header_frame).pack(side=tk.LEFT, expand=True)

        # Orologio a destra
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

        # Frame esterno con bordo
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
        self.combo_client.pack(fill=tk.X, pady=(0, 10))

        # Customer Claim Number
        ttk.Label(left_col, text=self.lang.get('lbl_customer_claim_num', 'N° Reclamo Cliente') + " *:").pack(
            anchor=tk.W)
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
            state='readonly',
            width=30
        )
        product_values = [f"{p[1]} - {p[2]}" for p in self.combo_data.get('products', [])]
        self.combo_product['values'] = product_values
        self.combo_product.pack(fill=tk.X, pady=(0, 10))

        # === Date Claim con Calendario ===
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

        # === Target Date con Calendario ===
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

        # ===== COLONNA DESTRA: TRASPORTO =====
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

        # === Transport Document Date con Calendario ===
        ttk.Label(right_col, text=self.lang.get('lbl_transport_date', 'Data Doc. Trasporto') + ":").pack(anchor=tk.W)
        self.date_transport_picker = DateEntry(
            right_col,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.date_transport_picker.pack(fill=tk.X, pady=(0, 10))

        # === Transport Document File ===
        ttk.Label(right_col, text=self.lang.get('lbl_transport_file', 'File Documento') + ":").pack(anchor=tk.W)

        file_frame = ttk.Frame(right_col)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.var_transport_file = tk.StringVar()
        self.label_file = ttk.Label(file_frame, text=self.lang.get('msg_no_file', 'Nessun file'), foreground='gray')
        self.label_file.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            file_frame,
            text=self.lang.get('btn_browse', 'Sfoglia...'),
            command=self._select_transport_file,
            width=12
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Internal Claim Number (ReadOnly)
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

        ttk.Frame(buttons_frame).pack(side=tk.LEFT, expand=True)

        # Pulsante Salva Testata
        self.btn_save_header = ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_save', 'Salva Testata'),
            command=self._save_header
        )
        self.btn_save_header.pack(side=tk.RIGHT, padx=(0, 5))

        # Pulsante Annulla
        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=(0, 5))

    def _prepare_header_data(self) -> Optional[ClaimHeader]:
        """
        Prepara i dati della testata dal form

        Returns:
            ClaimHeader: Oggetto con i dati, None se errore
        """
        try:
            logger.debug("[ADD_COMPLAINT] === INIZIO _prepare_header_data ===")

            # Ottieni IDs dai valori dei combobox (stringhe)
            logger.debug(f"[ADD_COMPLAINT] combo_data keys: {list(self.combo_data.keys())}")

            client_text = self.var_client.get()
            logger.debug(f"[ADD_COMPLAINT] client_text: '{client_text}'")
            logger.debug(f"[ADD_COMPLAINT] clients_map: {self.combo_data.get('clients_map', {})}")

            client_id = self.combo_data['clients_map'].get(client_text, 0)
            logger.debug(f"[ADD_COMPLAINT] client_id: {client_id}")

            if client_id == 0:
                logger.error(f"[ADD_COMPLAINT] Client ID non trovato per: '{client_text}'")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_client_id_not_found', 'Cliente non trovato nella mappa'),
                    parent=self
                )
                return None

            product_text = self.var_product.get()
            logger.debug(f"[ADD_COMPLAINT] product_text: '{product_text}'")
            logger.debug(f"[ADD_COMPLAINT] products_map: {self.combo_data.get('products_map', {})}")

            product_id = self.combo_data['products_map'].get(product_text, 0)
            logger.debug(f"[ADD_COMPLAINT] product_id: {product_id}")

            if product_id == 0:
                logger.error(f"[ADD_COMPLAINT] Product ID non trovato per: '{product_text}'")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_product_id_not_found', 'Prodotto non trovato nella mappa'),
                    parent=self
                )
                return None

            claim_type_text = self.var_claim_type.get()
            logger.debug(f"[ADD_COMPLAINT] claim_type_text: '{claim_type_text}'")
            logger.debug(f"[ADD_COMPLAINT] claim_types_map: {self.combo_data.get('claim_types_map', {})}")

            claim_type_id = self.combo_data['claim_types_map'].get(claim_type_text, 0)
            logger.debug(f"[ADD_COMPLAINT] claim_type_id: {claim_type_id}")

            if claim_type_id == 0:
                logger.error(f"[ADD_COMPLAINT] Claim Type ID non trovato per: '{claim_type_text}'")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_claim_type_id_not_found', 'Tipo reclamo non trovato nella mappa'),
                    parent=self
                )
                return None

            # Leggi il file se selezionato
            file_binary = None
            file_name = None
            filepath = self.var_transport_file.get()
            logger.debug(f"[ADD_COMPLAINT] filepath: '{filepath}'")

            if filepath and os.path.exists(filepath):
                try:
                    # Verifica la dimensione del file
                    file_size = os.path.getsize(filepath)
                    max_size = 10 * 1024 * 1024  # 10 MB

                    logger.debug(f"[ADD_COMPLAINT] file_size: {file_size} bytes")

                    if file_size > max_size:
                        logger.error(f"[ADD_COMPLAINT] File troppo grande: {file_size / (1024 * 1024):.2f} MB")
                        messagebox.showerror(
                            self.lang.get('err_file_too_large', 'File Troppo Grande'),
                            f"{self.lang.get('msg_max_file_size', 'Dimensione massima')}: 10 MB\n" +
                            f"{self.lang.get('msg_file_size', 'Dimensione file')}: {file_size / (1024 * 1024):.2f} MB",
                            parent=self
                        )
                        return None

                    with open(filepath, 'rb') as f:
                        file_binary = f.read()
                    file_name = os.path.basename(filepath)
                    logger.debug(f"[ADD_COMPLAINT] File letto: {file_name} ({len(file_binary)} bytes)")

                except IOError as io_error:
                    logger.exception(f"[ADD_COMPLAINT] IOError lettura file: {io_error}")
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        f"{self.lang.get('err_read_file', 'Errore nella lettura del file')}: {str(io_error)}",
                        parent=self
                    )
                    return None
                except Exception as file_error:
                    logger.exception(f"[ADD_COMPLAINT] Exception lettura file: {file_error}")
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        f"{self.lang.get('err_read_file', 'Errore nella lettura del file')}: {str(file_error)}",
                        parent=self
                    )
                    return None
            else:
                logger.debug(f"[ADD_COMPLAINT] Nessun file da caricare")

            # Estrai le date dai widget calendario
            try:
                logger.debug(f"[ADD_COMPLAINT] Estrazione date dal calendario...")

                # CORRETTO: Usa date_claim_picker (DateEntry widget) non var_date_claim
                date_claim_obj = self.date_claim_picker.get_date()
                date_claim = date_claim_obj.strftime('%Y-%m-%d')
                logger.debug(f"[ADD_COMPLAINT] date_claim: {date_claim}")

                # CORRETTO: Usa date_target_picker (DateEntry widget)
                date_target_obj = self.date_target_picker.get_date()
                date_target = date_target_obj.strftime('%Y-%m-%d')
                logger.debug(f"[ADD_COMPLAINT] date_target: {date_target}")

                # CORRETTO: Usa date_transport_picker (DateEntry widget)
                date_transport = None
                if self.var_transport_doc.get():
                    date_transport_obj = self.date_transport_picker.get_date()
                    date_transport = date_transport_obj.strftime('%Y-%m-%d')
                    logger.debug(f"[ADD_COMPLAINT] date_transport: {date_transport}")

            except AttributeError as attr_error:
                logger.exception(f"[ADD_COMPLAINT] AttributeError: widget calendario non trovato: {attr_error}")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    f"Errore widget calendario: {str(attr_error)}",
                    parent=self
                )
                return None
            except Exception as date_error:
                logger.exception(f"[ADD_COMPLAINT] Exception conversione data: {date_error}")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    f"{self.lang.get('err_invalid_data', 'Dati non validi')}: {str(date_error)}",
                    parent=self
                )
                return None

            # Crea e restituisci l'oggetto ClaimHeader
            logger.debug(f"[ADD_COMPLAINT] Creazione oggetto ClaimHeader...")

            header = ClaimHeader(
                ClaimTypeId=claim_type_id,
                IdProduct=product_id,
                DateClaim=date_claim,  # Data dal calendario
                AWB=self.var_awb.get() if self.var_awb.get() else None,
                TransportDocument=self.var_transport_doc.get() if self.var_transport_doc.get() else None,
                TransportDocumentData=file_binary,
                TransportDocumentFileName=file_name,
                CustomerClaimNumber=self.var_customer_claim.get(),
                InternalClaimNumber=self.var_internal_claim.get(),
                ShortClaimDescription=self.var_description.get(),
                TargetDate=date_target,  # Data dal calendario
                Quantity=int(self.var_quantity.get()),
                IDFinalClient=client_id,
                ClaimDecisionId=None,
                USERName=self.authenticated_user
            )

            logger.info(f"[ADD_COMPLAINT] ✅ ClaimHeader preparato correttamente")
            logger.info(f"[ADD_COMPLAINT]    - ClaimTypeId: {header.ClaimTypeId}")
            logger.info(f"[ADD_COMPLAINT]    - IdProduct: {header.IdProduct}")
            logger.info(f"[ADD_COMPLAINT]    - DateClaim: {header.DateClaim}")
            logger.info(f"[ADD_COMPLAINT]    - TargetDate: {header.TargetDate}")
            logger.info(f"[ADD_COMPLAINT]    - Quantity: {header.Quantity}")
            logger.info(f"[ADD_COMPLAINT]    - File: {header.TransportDocumentFileName}")
            logger.debug(f"[ADD_COMPLAINT] === FINE _prepare_header_data ===")
            return header

        except ValueError as val_error:
            logger.exception(f"[ADD_COMPLAINT] ValueError conversione dati: {val_error}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_invalid_data', 'Dati non validi')}: {str(val_error)}",
                parent=self
            )
            return None
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] ❌ Exception inaspettata in _prepare_header_data: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_prepare_header', 'Errore nella preparazione dei dati')}: {str(e)}",
                parent=self
            )
            return None

    def _select_transport_file(self):
        """Apre un dialog per selezionare il file di trasporto"""
        from tkinter import filedialog

        # Estensioni supportate
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
                # Verifica la dimensione del file (max 10 MB)
                file_size = os.path.getsize(filepath)
                max_size = 10 * 1024 * 1024  # 10 MB

                if file_size > max_size:
                    messagebox.showerror(
                        self.lang.get('err_file_too_large', 'File Troppo Grande'),
                        f"{self.lang.get('msg_max_file_size', 'Dimensione massima')}: 10 MB\n" +
                        f"{self.lang.get('msg_file_size', 'Dimensione file')}: {file_size / (1024 * 1024):.2f} MB",
                        parent=self
                    )
                    return

                self.var_transport_file.set(filepath)
                filename = os.path.basename(filepath)
                self.label_file.config(text=filename, foreground='black')

                logger.info(f"[ADD_COMPLAINT] File selezionato: {filename} ({file_size / 1024:.2f} KB)")

        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore selezione file: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_select_file', 'Errore nella selezione del file')}: {str(e)}",
                parent=self)

    def _create_claim_details_frame(self, parent):
        """Crea il frame per le righe di dettaglio del reclamo"""

        self.details_frame = ttk.LabelFrame(
            parent,
            text=self.lang.get('lbl_claim_details', 'Dettagli Reclamo'),
            padding=10
        )
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Informazione iniziale
        self.info_label = ttk.Label(
            self.details_frame,
            text=self.lang.get('msg_enter_quantity', 'Salvare la testata per aggiungere le righe'),
            foreground='gray'
        )
        self.info_label.pack(pady=20)

        # Treeview per le righe
        self.tree_details = None
        self._create_details_treeview()

        # Frame pulsanti dettagli (disabilitato finché la testata non è salvata)
        self.details_buttons_frame = ttk.Frame(self.details_frame)
        self.details_buttons_frame.pack(fill=tk.X, pady=(10, 0))

        self.btn_add_row = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_add_detail_row', 'Aggiungi Riga'),
            command=self._add_detail_row,
            state=tk.DISABLED
        )
        self.btn_add_row.pack(side=tk.LEFT, padx=5)

        self.btn_remove_row = ttk.Button(
            self.details_buttons_frame,
            text=self.lang.get('btn_remove_detail_row', 'Rimuovi Riga'),
            command=self._remove_detail_row,
            state=tk.DISABLED
        )
        self.btn_remove_row.pack(side=tk.LEFT, padx=5)

        # Spazio elastico
        ttk.Frame(self.details_buttons_frame).pack(side=tk.LEFT, expand=True)

        # Pulsanti finali (salva/chiudi)
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

        # Definisci colonne
        self.tree_details.column('Num', width=50)
        self.tree_details.column('Label', width=100)
        self.tree_details.column('Defect', width=150)
        self.tree_details.column('Inspection', width=120)
        self.tree_details.column('RootCause', width=150)
        self.tree_details.column('Corrective', width=150)
        self.tree_details.column('Preventive', width=150)
        self.tree_details.column('Status', width=100)

        # Intestazioni
        self.tree_details.heading('Num', text=self.lang.get('col_num', 'N°'))
        self.tree_details.heading('Label', text=self.lang.get('col_label', 'Label Cod'))
        self.tree_details.heading('Defect', text=self.lang.get('col_defect', 'Difetto'))
        self.tree_details.heading('Inspection', text=self.lang.get('col_inspection', 'Ispez. Iniziale'))
        self.tree_details.heading('RootCause', text=self.lang.get('col_root_cause', 'Causa Radice'))
        self.tree_details.heading('Corrective', text=self.lang.get('col_corrective', 'Az. Correttiva'))
        self.tree_details.heading('Preventive', text=self.lang.get('col_preventive', 'Az. Preventiva'))
        self.tree_details.heading('Status', text=self.lang.get('col_status', 'Stato'))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, command=self.tree_details.yview)
        self.tree_details['yscroll'] = scrollbar.set

        self.tree_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

    def _save_header(self):
        """Salva la testata del reclamo"""

        logger.info("[ADD_COMPLAINT] === INIZIO _save_header ===")

        # Valida testata
        is_valid, error_msg = self._validate_header()
        if not is_valid:
            logger.error(f"[ADD_COMPLAINT] Validazione fallita: {error_msg}")
            messagebox.showerror(
                self.lang.get('err_validation', 'Errore Validazione'),
                error_msg,
                parent=self
            )
            return

        logger.debug("[ADD_COMPLAINT] Validazione header OK")

        try:
            # Prepara dati testata
            logger.debug("[ADD_COMPLAINT] Chiamata _prepare_header_data()...")
            claim_header = self._prepare_header_data()

            logger.debug(f"[ADD_COMPLAINT] claim_header type: {type(claim_header)}")
            logger.debug(f"[ADD_COMPLAINT] claim_header value: {claim_header}")

            # IMPORTANTE: Verifica che claim_header non sia None
            if claim_header is None:
                logger.error("[ADD_COMPLAINT] ❌ Errore: claim_header è None")
                messagebox.showerror(
                    self.lang.get('err_error', 'Errore'),
                    self.lang.get('err_prepare_header', 'Errore nella preparazione dei dati'),
                    parent=self
                )
                return

            logger.info(f"[ADD_COMPLAINT] Salvataggio testata reclamo: {claim_header.InternalClaimNumber}")

            # Salva testata
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

            # Abilita i dettagli
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
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_save_error', 'Errore nel salvataggio')}: {str(e)}",
                parent=self
            )
            logger.info("[ADD_COMPLAINT] === FINE _save_header (ERRORE) ===")

    def _enable_details_section(self):
        """Abilita la sezione dettagli dopo il salvataggio della testata"""

        # Aggiorna l'etichetta informativa
        self.info_label.config(
            text=f"{self.lang.get('msg_rows_to_add', 'Righe da aggiungere: ')}{self.rows_to_add}",
            foreground='black'
        )

        # Abilita pulsanti
        self.btn_add_row.config(state=tk.NORMAL)
        self.btn_remove_row.config(state=tk.NORMAL)
        self.btn_save_final.config(state=tk.NORMAL)

        # Disabilita la modifica della testata
        self.btn_save_header.config(state=tk.DISABLED)
        self.combo_client.config(state='disabled')
        self.combo_claim_type.config(state='disabled')
        self.combo_product.config(state='disabled')

    def _add_detail_row(self):
        """Aggiunge una nuova riga di dettaglio"""

        if len(self.tree_details.get_children()) >= self.rows_to_add:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                f"Non puoi aggiungere più di {self.rows_to_add} righe",
                parent=self
            )
            return

        # Apri finestra di editing
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
            self.lang.get('msg_confirm_delete', 'Confermare l\'eliminazione della riga?'),
            parent=self
        ):
            for item in selection:
                self.tree_details.delete(item)

    def _open_detail_editor(self, row_idx: Optional[int] = None):
        """Apre la finestra di editing per una riga di dettaglio"""

        DetailEditorWindow(self, self.db, self.lang, self.combo_data, row_idx, self._add_row_to_tree)

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

    def _prepare_header_data(self) -> Optional[ClaimHeader]:
        """
        Prepara i dati della testata dal form

        Returns:
            ClaimHeader: Oggetto con i dati, None se errore
        """
        try:
            # Ottieni IDs dai valori dei combobox (stringhe)
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

            # Leggi il file se selezionato
            file_binary = None
            file_name = None
            filepath = self.var_transport_file.get()

            if filepath and os.path.exists(filepath):
                try:
                    # Verifica la dimensione del file
                    file_size = os.path.getsize(filepath)
                    max_size = 10 * 1024 * 1024  # 10 MB

                    if file_size > max_size:
                        messagebox.showerror(
                            self.lang.get('err_file_too_large', 'File Troppo Grande'),
                            f"{self.lang.get('msg_max_file_size', 'Dimensione massima')}: 10 MB\n" +
                            f"{self.lang.get('msg_file_size', 'Dimensione file')}: {file_size / (1024 * 1024):.2f} MB",
                            parent=self
                        )
                        return None

                    with open(filepath, 'rb') as f:
                        file_binary = f.read()
                    file_name = os.path.basename(filepath)
                    logger.debug(f"[ADD_COMPLAINT] File letto: {file_name} ({len(file_binary)} bytes)")

                except IOError as io_error:
                    logger.exception(f"[ADD_COMPLAINT] Errore lettura file: {io_error}")
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        f"{self.lang.get('err_read_file', 'Errore nella lettura del file')}: {str(io_error)}",
                        parent=self
                    )
                    return None
                except Exception as file_error:
                    logger.exception(f"[ADD_COMPLAINT] Errore inaspettato lettura file: {file_error}")
                    messagebox.showerror(
                        self.lang.get('err_error', 'Errore'),
                        f"{self.lang.get('err_read_file', 'Errore nella lettura del file')}: {str(file_error)}",
                        parent=self
                    )
                    return None

            # Crea e restituisci l'oggetto ClaimHeader
            header = ClaimHeader(
                ClaimTypeId=claim_type_id,
                IdProduct=product_id,
                DateClaim=self.date_claim_picker.get_date().strftime('%Y-%m-%d'),
                AWB=self.var_awb.get() if self.var_awb.get() else None,
                TransportDocument=self.var_transport_doc.get() if self.var_transport_doc.get() else None,
                TransportDocumentData=file_binary,  # Dati binari del file (può essere None)
                TransportDocumentFileName=file_name,  # Nome del file (può essere None)
                CustomerClaimNumber=self.var_customer_claim.get(),
                InternalClaimNumber=self.var_internal_claim.get(),
                ShortClaimDescription=self.var_description.get(),
                TargetDate=self.date_target_picker.get_date().strftime('%Y-%m-%d')if self.date_target_picker.get_date().strftime('%Y-%m-%d') else None,
                Quantity=int(self.var_quantity.get()),
                IDFinalClient=client_id,
                ClaimDecisionId=None,
                USERName=self.authenticated_user
            )

            logger.debug(f"[ADD_COMPLAINT] ClaimHeader preparato correttamente")
            return header

        except ValueError as val_error:
            logger.exception(f"[ADD_COMPLAINT] Errore conversione dati: {val_error}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_invalid_data', 'Dati non validi')}: {str(val_error)}",
                parent=self
            )
            return None
        except Exception as e:
            logger.exception(f"[ADD_COMPLAINT] Errore inaspettato preparazione dati: {e}")
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                f"{self.lang.get('err_prepare_header', 'Errore nella preparazione dei dati')}: {str(e)}",
                parent=self
            )
            return None

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

            if rows_inserted < self.rows_to_add:
                if not messagebox.askyesno(
                        self.lang.get('warning', 'Attenzione'),
                        f"Hai inserito {rows_inserted} su {self.rows_to_add} righe.\nContinuare comunque?",
                        parent=self
                ):
                    return

            # Prepara i dettagli dalla treeview
            claim_details = []
            for item in self.tree_details.get_children():
                values = self.tree_details.item(item)['values']

                # Mappa i valori ai campi
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


class DetailEditorWindow(tk.Toplevel):
    """Finestra per editare i dettagli di una riga"""

    def __init__(self, parent, db, lang, combo_data, row_idx, callback):
        super().__init__(parent)

        self.parent = parent
        self.db = db
        self.lang = lang
        self.combo_data = combo_data
        self.row_idx = row_idx
        self.callback = callback

        self.title(lang.get('title_edit_detail', 'Aggiungi Dettaglio Reclamo'))
        self.geometry('600x500')
        self.resizable(False, False)

        self._create_widgets()

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def _create_widgets(self):
        """Crea i widget della finestra"""

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Label Code
        ttk.Label(frame, text=self.lang.get('lbl_label_cod', 'Label Cod') + " *:").pack(anchor=tk.W)
        self.var_label = tk.StringVar()
        ttk.Entry(frame, textvariable=self.var_label, width=50).pack(fill=tk.X, pady=(0, 10))

        # Defect
        ttk.Label(frame, text=self.lang.get('lbl_defect', 'Difetto') + ":").pack(anchor=tk.W)
        self.var_defect = tk.StringVar()
        combo_defect = ttk.Combobox(
            frame,
            textvariable=self.var_defect,
            state='readonly',
            width=48
        )
        combo_defect['values'] = [d[1] for d in self.combo_data.get('defects', [])]
        combo_defect.pack(fill=tk.X, pady=(0, 10))

        # First Inspection Result
        ttk.Label(frame, text=self.lang.get('lbl_inspection', 'Ispez. Iniziale') + ":").pack(anchor=tk.W)
        self.var_inspection = tk.StringVar(value='Pending Analysis')
        combo_inspection = ttk.Combobox(
            frame,
            textvariable=self.var_inspection,
            state='readonly',
            width=48
        )
        combo_inspection['values'] = [i[1] for i in self.combo_data.get('inspection_results', [])]
        combo_inspection.pack(fill=tk.X, pady=(0, 10))

        # Root Cause
        ttk.Label(frame, text=self.lang.get('lbl_root_cause', 'Causa Radice') + ":").pack(anchor=tk.W)
        self.var_root_cause = tk.StringVar()
        ttk.Entry(frame, textvariable=self.var_root_cause, width=50).pack(fill=tk.X, pady=(0, 10))

        # Corrective Action
        ttk.Label(frame, text=self.lang.get('lbl_corrective_action', 'Az. Correttiva') + ":").pack(anchor=tk.W)
        self.var_corrective = tk.StringVar()
        ttk.Entry(frame, textvariable=self.var_corrective, width=50).pack(fill=tk.X, pady=(0, 10))

        # Preventive Action
        ttk.Label(frame, text=self.lang.get('lbl_preventive_action', 'Az. Preventiva') + ":").pack(anchor=tk.W)
        self.var_preventive = tk.StringVar()
        ttk.Entry(frame, textvariable=self.var_preventive, width=50).pack(fill=tk.X, pady=(0, 10))

        # Claim Status
        ttk.Label(frame, text=self.lang.get('lbl_status', 'Stato') + ":").pack(anchor=tk.W)
        self.var_status = tk.StringVar(value='Open')
        combo_status = ttk.Combobox(
            frame,
            textvariable=self.var_status,
            state='readonly',
            width=48
        )
        combo_status['values'] = [s[1] for s in self.combo_data.get('claim_status', [])]
        combo_status.pack(fill=tk.X, pady=(0, 20))

        # Pulsanti
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X)

        ttk.Frame(buttons_frame).pack(side=tk.LEFT, expand=True)

        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_save', 'Salva'),
            command=self._save_row
        ).pack(side=tk.RIGHT, padx=(0, 5))

        ttk.Button(
            buttons_frame,
            text=self.lang.get('btn_cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=(0, 5))

    def _save_row(self):
        """Salva la riga e chiama la callback"""

        if not self.var_label.get().strip():
            messagebox.showerror(
                self.lang.get('err_error', 'Errore'),
                self.lang.get('err_label_required', 'Label Cod obbligatorio'),
                parent=self
            )
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

        self.callback(row_data)
        self.destroy()


# Test standalone
if __name__ == '__main__':
    print("[ADD_COMPLAINT] Modulo importabile correttamente")