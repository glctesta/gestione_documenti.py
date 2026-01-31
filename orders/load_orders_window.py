# File: orders/load_orders_window.py
"""
Finestra per il caricamento ordini da Excel
"""
import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import openpyxl

logger = logging.getLogger(__name__)


class LoadOrdersWindow(tk.Toplevel):
    """Finestra per visualizzare e importare ordini dinamici"""
    
    def __init__(self, master, db, lang, orders_manager, user_name):
        """
        Inizializza la finestra di caricamento ordini
        
        Args:
            master: Finestra padre
            db: Connessione database
            lang: Gestore traduzioni
            orders_manager: Manager degli ordini
            user_name: Nome dell'utente loggato
        """
        super().__init__(master)
        logger.info("Inizializzazione finestra di caricamento ordini Class->LoadOrdersWindow")
        self.db = db
        self.lang = lang
        self.orders_manager = orders_manager
        self.user_name = user_name
        
        self.title(self.lang.get('load_orders_title', 'Carica Ordini'))
        self.geometry('1600x700')
        self.transient(master)
        
        # Variabile per il filtro giorni
        self.days_limit = tk.IntVar(value=100)
        
        # Variabile per il filtro Linked
        self.linked_filter = tk.StringVar(value='All')
        
        # Variabili per l'ordinamento
        self.sort_column = None
        self.sort_reverse = False
        self.orders_data = []  # Cache dei dati per ordinamento locale
        
        self._create_widgets()
        self._load_orders()
    
    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con titolo e bottoni
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text=self.lang.get('dynamic_orders_list', 'Elenco Ordini Dinamici'),
            font=('Helvetica', 14, 'bold')
        ).pack(side=tk.LEFT)
        
        # Frame per filtro giorni
        filter_frame = ttk.Frame(header_frame)
        filter_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(
            filter_frame,
            text=self.lang.get('days_filter', 'Giorni dalla data odierna:'),
            font=('Helvetica', 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        days_spinbox = ttk.Spinbox(
            filter_frame,
            from_=1,
            to=365,
            textvariable=self.days_limit,
            width=10,
            command=self._on_days_filter_change
        )
        days_spinbox.pack(side=tk.LEFT)
        days_spinbox.bind('<Return>', lambda e: self._on_days_filter_change())
        days_spinbox.bind('<FocusOut>', lambda e: self._on_days_filter_change())
        
        # Frame per filtro Linked
        linked_frame = ttk.Frame(header_frame)
        linked_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(
            linked_frame,
            text=self.lang.get('linked_filter', 'Collegato:'),
            font=('Helvetica', 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        linked_combo = ttk.Combobox(
            linked_frame,
            textvariable=self.linked_filter,
            values=['All', 'Yes', 'No'],
            state='readonly',
            width=8
        )
        linked_combo.pack(side=tk.LEFT)
        linked_combo.bind('<<ComboboxSelected>>', lambda e: self._on_filter_change())
        
        # Bottoni azione
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            btn_frame,
            text=self.lang.get('btn_import_excel', 'Importa da Excel'),
            command=self._import_from_excel
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text=self.lang.get('btn_refresh', 'Aggiorna'),
            command=self._load_orders
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text=self.lang.get('btn_match_production_orders', 'Accoppia Ordini Produzione'),
            command=self._match_production_orders
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview per visualizzare gli ordini
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = (
            'SONumber', 'CustomerName', 'ProductCode', 'ProductName',
            'ShipDate', 'QtyOrder', 'QtyToShip', 'QtyStock', 'Currency', 'UnitPrice',
            'LastUpdate', 'Linked'
        )
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        # Configura intestazioni (cliccabili per ordinamento)
        for col in columns:
            self.tree.heading(col, text=self._get_column_header(col), command=lambda c=col: self._sort_by_column(c))
        
        # Imposta testi intestazioni
        self._update_column_headers()
        
        # Larghezza colonne
        self.tree.column('SONumber', width=100)
        self.tree.column('CustomerName', width=150)
        self.tree.column('ProductCode', width=100)
        self.tree.column('ProductName', width=200)
        self.tree.column('ShipDate', width=100)
        self.tree.column('QtyOrder', width=80)
        self.tree.column('QtyToShip', width=80)
        self.tree.column('QtyStock', width=80)
        self.tree.column('Currency', width=60)
        self.tree.column('UnitPrice', width=80)
        self.tree.column('LastUpdate', width=100)
        self.tree.column('Linked', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text='', relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def _get_column_header(self, col):
        """Restituisce il testo dell'intestazione per una colonna"""
        headers = {
            'SONumber': self.lang.get('col_so_number', 'N. Ordine'),
            'CustomerName': self.lang.get('col_customer', 'Cliente'),
            'ProductCode': self.lang.get('col_product_code', 'Cod. Prodotto'),
            'ProductName': self.lang.get('col_product_name', 'Nome Prodotto'),
            'ShipDate': self.lang.get('col_ship_date', 'Data Spedizione'),
            'QtyOrder': self.lang.get('col_qty_order', 'Qtà Ordinata'),
            'QtyToShip': self.lang.get('col_qty_to_ship', 'Qtà da Spedire'),
            'QtyStock': self.lang.get('col_qty_stock', 'Qtà in Stock'),
            'Currency': self.lang.get('col_currency', 'Valuta'),
            'UnitPrice': self.lang.get('col_unit_price', 'Prezzo Unit.'),
            'LastUpdate': self.lang.get('col_last_update', 'Ultimo Agg.'),
            'Linked': self.lang.get('col_linked', 'Collegato')
        }
        return headers.get(col, col)
    
    def _update_column_headers(self):
        """Aggiorna le intestazioni delle colonne con indicatori di ordinamento"""
        columns = (
            'SONumber', 'CustomerName', 'ProductCode', 'ProductName',
            'ShipDate', 'QtyOrder', 'QtyToShip', 'QtyStock', 'Currency', 'UnitPrice',
            'LastUpdate', 'Linked'
        )
        
        for col in columns:
            header_text = self._get_column_header(col)
            if col == self.sort_column:
                # Aggiungi indicatore di ordinamento
                indicator = ' ▼' if self.sort_reverse else ' ▲'
                header_text += indicator
            self.tree.heading(col, text=header_text)
    
    def _sort_by_column(self, col):
        """Ordina i dati per la colonna selezionata"""
        # Se clicchiamo sulla stessa colonna, inverti l'ordine
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # Ordina i dati in memoria
        self._sort_and_display_orders()
    
    def _sort_and_display_orders(self):
        """Ordina e visualizza gli ordini nella treeview"""
        if not self.orders_data:
            return
        
        # Mappa colonne treeview a chiavi dizionario
        column_map = {
            'SONumber': 'SONumber',
            'CustomerName': 'CustomerName',
            'ProductCode': 'ProductCode',
            'ProductName': 'ProductName',
            'ShipDate': 'ShipDateRequest',
            'QtyOrder': 'QtyOrder',
            'QtyToShip': 'QtyToShip',
            'QtyStock': 'QtyStock',
            'Currency': 'Currency',
            'UnitPrice': 'UnitPrice',
            'LastUpdate': 'LastUpdate',
            'Linked': 'Linked'
        }
        
        if self.sort_column:
            data_key = column_map.get(self.sort_column)
            if data_key:
                # Ordina con gestione di valori None
                self.orders_data.sort(
                    key=lambda x: (x.get(data_key) is None, x.get(data_key) or ''),
                    reverse=self.sort_reverse
                )
        
        # Pulisci e ricarica treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for order in self.orders_data:
            ship_date = order['ShipDateRequest'].strftime('%d/%m/%Y') if order['ShipDateRequest'] else ''
            last_update = order['LastUpdate'].strftime('%d/%m/%Y %H:%M') if order.get('LastUpdate') else ''
            
            self.tree.insert('', tk.END, values=(
                order['SONumber'] or '',
                order['CustomerName'] or '',
                order['ProductCode'] or '',
                order['ProductName'] or '',
                ship_date,
                order['QtyOrder'] or 0,
                order['QtyToShip'] or 0,
                order['QtyStock'] or 0,
                order['Currency'] or '',
                f"{order['UnitPrice']:.2f}" if order['UnitPrice'] else '0.00',
                last_update,
                order.get('Linked', 'No')
            ))
        
        # Aggiorna intestazioni con indicatori
        self._update_column_headers()
    
    def _on_filter_change(self):
        """Gestisce il cambio di qualsiasi filtro e ricarica gli ordini"""
        self._load_orders()
    
    def _on_days_filter_change(self):
        """Gestisce il cambio del filtro giorni e ricarica gli ordini"""
        self._load_orders()
    
    def _load_orders(self):
        """Carica gli ordini dal database"""
        try:
            # Carica ordini con filtri
            days_limit = self.days_limit.get()
            linked_filter = self.linked_filter.get()
            self.orders_data = self.orders_manager.get_all_dynamic_orders(
                days_limit=days_limit,
                linked_filter=linked_filter
            )
            
            # Visualizza con ordinamento corrente
            self._sort_and_display_orders()
            
            self.status_label.config(
                text=f"{len(self.orders_data)} {self.lang.get('orders_loaded', 'ordini caricati')} "
                     f"(filtro: {days_limit} giorni, collegato: {linked_filter})"
            )
            
        except Exception as e:
            logger.error(f"Errore nel caricamento ordini: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error_loading_orders', 'Errore caricamento ordini')}:\n{e}",
                parent=self
            )
    
    def _match_production_orders(self):
        """Apre la finestra di accoppiamento ordini di produzione"""
        from orders.match_production_orders_window import open_match_production_orders_window
        open_match_production_orders_window(self, self.db, self.lang, self.user_name)
    
    def _import_from_excel(self):
        """Importa ordini da file Excel"""
        file_path = filedialog.askopenfilename(
            title=self.lang.get('select_excel_file', 'Seleziona file Excel'),
            filetypes=[
                ('Excel files', '*.xlsx *.xls'),
                ('All files', '*.*')
            ],
            parent=self
        )
        
        if not file_path:
            return
        
        try:
            # Leggi il file Excel
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active
            
            # Leggi le intestazioni dalla prima riga
            headers = []
            for cell in sheet[1]:
                headers.append(cell.value)
            logger.info(f"INTESTAZIONI EXCEL: {headers}")
            
            # Crea mappa intestazione -> indice colonna
            # Mappatura secondo l'immagine fornita:
            # SQL Field          -> Excel Header
            column_map = {}
            header_mapping = {
                'so number': 'SONumber',
                'customer name': 'CustomerName',
                'item code': 'ItemCode',
                'item name': 'ItemName',
                'req. shipdate': 'ShipDateRequest',
                'req shipdate': 'ShipDateRequest',  # Variante senza punto
                'order qty': 'QtyOrder',
                'remaining qty': 'QtyToShip',
                'stock qty': 'QtyStock',
                'currency': 'Currency',
                'unit price': 'UnitPrice'
            }
            
            # Trova gli indici delle colonne necessarie (case-insensitive)
            mapping_log = []
            for idx, header in enumerate(headers):
                if header is None:
                    continue
                header_clean = str(header).strip().lower()
                if header_clean in header_mapping:
                    field_name = header_mapping[header_clean]
                    column_map[field_name] = idx
                    mapping_log.append(f"✓ '{header}' (col {idx}) → {field_name}")
                    logger.info(f"Mappato '{header}' (colonna {idx}) → {field_name}")
            
            # Mostra mapping trovato
            mapping_msg = "MAPPING COLONNE TROVATO:\n\n"
            mapping_msg += "\n".join(mapping_log)
            mapping_msg += "\n\n"
            
            # Verifica che tutti i campi necessari siano presenti
            required_fields = ['SONumber', 'CustomerName', 'ItemCode', 'ItemName']
            missing_fields = [f for f in required_fields if f not in column_map]
            
            if missing_fields:
                mapping_msg += f"\n⚠️ CAMPI MANCANTI: {', '.join(missing_fields)}\n"
                mapping_msg += "\nIntestazioni trovate nell'Excel:\n"
                for idx, h in enumerate(headers):
                    mapping_msg += f"  Col {idx}: {h}\n"
            
            messagebox.showinfo(
                "Mapping Colonne Excel",
                mapping_msg,
                parent=self
            )
            
            if missing_fields:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"Campi obbligatori mancanti nell'Excel:\n{', '.join(missing_fields)}\n\nControlla le intestazioni del file Excel.",
                    parent=self
                )
                return
            
            # Helper function per ottenere valore da riga
            def get_value(row, field_name, default=None):
                """Ottiene il valore dalla riga usando la mappa delle colonne"""
                if field_name not in column_map:
                    return default
                idx = column_map[field_name]
                if idx >= len(row):
                    return default
                return row[idx] if row[idx] is not None else default
            
            # Helper function per conversione sicura a float
            def safe_float(value, default=0):
                """Converte un valore in float in modo sicuro"""
                if value is None or value == '':
                    return default
                if isinstance(value, (int, float)):
                    return float(value)
                try:
                    return float(str(value).replace(',', '.'))
                except (ValueError, AttributeError):
                    logger.warning(f"Impossibile convertire '{value}' in float, uso {default}")
                    return default
            
            # Helper function per conversione sicura a string
            def safe_str(value, default=None):
                """Converte un valore in stringa in modo sicuro"""
                if value is None or value == '':
                    return default
                return str(value).strip()
            
            excel_rows = []
            for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                # Skip righe vuote
                so_number = get_value(row, 'SONumber')
                if not so_number:
                    continue
                
                # Skip righe che contengono filtri o intestazioni
                first_cell = safe_str(so_number, '')
                if 'Applied filters' in first_cell or 'Sales Order' in first_cell:
                    logger.info(f"Saltata riga {row_idx}: {first_cell} (filtro/intestazione)")
                    continue
                
                # Parsing della data
                ship_date = None
                date_value = get_value(row, 'ShipDateRequest')
                if date_value:
                    if isinstance(date_value, datetime):
                        ship_date = date_value
                    elif isinstance(date_value, str):
                        try:
                            ship_date = datetime.strptime(date_value, '%d-%m-%Y')
                        except:
                            try:
                                ship_date = datetime.strptime(date_value, '%Y-%m-%d')
                            except:
                                logger.warning(f"Impossibile parsare data '{date_value}' alla riga {row_idx}")
                
                # Validazione: verifica che almeno una quantità sia > 0
                qty_order = safe_float(get_value(row, 'QtyOrder'))
                qty_to_ship = safe_float(get_value(row, 'QtyToShip'))
                qty_stock = safe_float(get_value(row, 'QtyStock'))
                
                if qty_order <= 0 and qty_to_ship <= 0 and qty_stock <= 0:
                    logger.info(f"Saltata riga {row_idx}: nessuna quantità valida")
                    continue
                
                order_data = {
                    'SONumber': safe_str(get_value(row, 'SONumber')),
                    'CustomerName': safe_str(get_value(row, 'CustomerName')),
                    'ItemCode': safe_str(get_value(row, 'ItemCode')),
                    'ItemName': safe_str(get_value(row, 'ItemName')),
                    'ShipDateRequest': ship_date,
                    'QtyOrder': qty_order,
                    'QtyToShip': qty_to_ship,
                    'QtyStock': qty_stock,
                    'Currency': safe_str(get_value(row, 'Currency'), 'EUR'),
                    'UnitPrice': safe_float(get_value(row, 'UnitPrice'))
                }
                excel_rows.append(order_data)

            
            if not excel_rows:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('no_data_in_excel', 'Nessun dato trovato nel file Excel'),
                    parent=self
                )
                return
            
            # Conferma importazione
            if not messagebox.askyesno(
                self.lang.get('confirm_import', 'Conferma Importazione'),
                f"{self.lang.get('confirm_import_rows', 'Importare')} {len(excel_rows)} {self.lang.get('rows', 'righe')}?",
                parent=self
            ):
                return
            
            # Esegui importazione
            self.status_label.config(text=self.lang.get('importing', 'Importazione in corso...'))
            self.update()
            
            stats = self.orders_manager.import_from_excel_data(excel_rows, self.user_name)
            
            # Mostra risultati
            message = f"{self.lang.get('import_completed', 'Importazione completata')}:\n\n"
            message += f"{self.lang.get('inserted', 'Inseriti')}: {stats['inserted']}\n"
            message += f"{self.lang.get('updated', 'Aggiornati')}: {stats['updated']}\n"
            message += f"{self.lang.get('errors', 'Errori')}: {stats['errors']}"
            
            if stats['errors'] > 0:
                message += "\n\n" + self.lang.get('see_log_for_details', 'Vedere il log per i dettagli')
            
            messagebox.showinfo(
                self.lang.get('import_result', 'Risultato Importazione'),
                message,
                parent=self
            )
            
            # Ricarica gli ordini
            self._load_orders()
            
        except Exception as e:
            logger.error(f"Errore importazione Excel: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error_importing_excel', 'Errore importazione Excel')}:\n{e}",
                parent=self
            )


def open_load_orders_window(master, db, lang, user_name):
    """
    Apre la finestra di caricamento ordini
    
    Args:
        master: Finestra padre
        db: Connessione database
        lang: Gestore traduzioni  
        user_name: Nome utente loggato
    """
    from orders.orders_manager import OrdersManager
    
    orders_manager = OrdersManager(db)
    LoadOrdersWindow(master, db, lang, orders_manager, user_name)
