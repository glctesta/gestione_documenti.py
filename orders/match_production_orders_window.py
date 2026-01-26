# File: orders/match_production_orders_window.py
"""
Finestra per accoppiare gli ordini di vendita agli ordini di produzione
"""
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

logger = logging.getLogger(__name__)


class MatchProductionOrdersWindow(tk.Toplevel):
    """Finestra per associare ordini di produzione agli ordini di vendita"""
    
    def __init__(self, master, db, lang, orders_manager, user_name):
        """
        Inizializza la finestra di accoppiamento ordini
        
        Args:
            master: Finestra padre
            db: Connessione database
            lang: Gestore traduzioni
            orders_manager: Manager degli ordini
            user_name: Nome dell'utente loggato
        """
        logger.info("Inizializzazione finestra di accoppiamento ordini Class->MatchProductionOrdersWindow")
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.orders_manager = orders_manager
        self.user_name = user_name
        
        self.title(self.lang.get('match_production_orders_title', 'Accoppia Ordini di Produzione'))
        self.geometry('1600x800')
        self.transient(master)
        
        self.selected_sale_order = None
        self.production_orders_cache = []
        self.sale_orders_data = {}  # Dizionario per salvare ItemCode/ItemName per ogni ordine
        
        self._create_widgets()
        self._load_sale_orders()
        self._load_production_orders()
    
    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale con paned window
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ==================== PANNELLO SINISTRA: ORDINI DI VENDITA ====================
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)
        
        # Header
        ttk.Label(
            left_frame,
            text=self.lang.get('sale_orders', 'Ordini di Vendita'),
            font=('Helvetica', 12, 'bold')
        ).pack(pady=(0, 10))
        
        # Filtri
        filters_frame = ttk.LabelFrame(left_frame, text=self.lang.get('filters', 'Filtri'), padding=10)
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Riga 1: SO Number e Cliente
        row1 = ttk.Frame(filters_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text=self.lang.get('so_number', 'N. Ordine:')).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_so_number = ttk.Entry(row1, width=15)
        self.filter_so_number.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row1, text=self.lang.get('customer', 'Cliente:')).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_customer = ttk.Entry(row1, width=20)
        self.filter_customer.pack(side=tk.LEFT)
        
        # Riga 2: Prodotto
        row2 = ttk.Frame(filters_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text=self.lang.get('product', 'Prodotto:')).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_product = ttk.Entry(row2, width=30)
        self.filter_product.pack(side=tk.LEFT)
        
        # Riga 3: Range Date
        row3 = ttk.Frame(filters_frame)
        row3.pack(fill=tk.X, pady=2)
        
        ttk.Label(row3, text=self.lang.get('date_from', 'Data Da:')).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_date_from = DateEntry(
            row3,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            locale='it_IT'
        )
        self.filter_date_from.set_date(datetime.now() - timedelta(days=90))
        self.filter_date_from.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row3, text=self.lang.get('date_to', 'Data A:')).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_date_to = DateEntry(
            row3,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            locale='it_IT'
        )
        self.filter_date_to.set_date(datetime.now() + timedelta(days=180))
        self.filter_date_to.pack(side=tk.LEFT)
        
        # Bottoni filtro
        btn_row = ttk.Frame(filters_frame)
        btn_row.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            btn_row,
            text=self.lang.get('btn_apply_filter', 'Applica Filtri'),
            command=self._apply_filters
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_row,
            text=self.lang.get('btn_reset_filter', 'Resetta Filtri'),
            command=self._reset_filters
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview ordini di vendita
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('SONumber', 'Customer', 'Product', 'ShipDate', 'QtyOrder', 'QtyAssigned', 'QtyRemaining')
        
        self.sale_orders_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.sale_orders_tree.heading('SONumber', text=self.lang.get('col_so_number', 'N. Ordine'))
        self.sale_orders_tree.heading('Customer', text=self.lang.get('col_customer', 'Cliente'))
        self.sale_orders_tree.heading('Product', text=self.lang.get('col_product', 'Prodotto'))
        self.sale_orders_tree.heading('ShipDate', text=self.lang.get('col_ship_date', 'Data Spedizione'))
        self.sale_orders_tree.heading('QtyOrder', text=self.lang.get('col_qty_order', 'Qtà Ordine'))
        self.sale_orders_tree.heading('QtyAssigned', text=self.lang.get('col_qty_assigned', 'Qtà Assegnata'))
        self.sale_orders_tree.heading('QtyRemaining', text=self.lang.get('col_qty_remaining', 'Qtà Rimanente'))
        
        self.sale_orders_tree.column('SONumber', width=100)
        self.sale_orders_tree.column('Customer', width=150)
        self.sale_orders_tree.column('Product', width=200)
        self.sale_orders_tree.column('ShipDate', width=100)
        self.sale_orders_tree.column('QtyOrder', width=80, anchor=tk.E)
        self.sale_orders_tree.column('QtyAssigned', width=80, anchor=tk.E)
        self.sale_orders_tree.column('QtyRemaining', width=80, anchor=tk.E)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.sale_orders_tree.yview)
        self.sale_orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sale_orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.sale_orders_tree.bind('<<TreeviewSelect>>', self._on_sale_order_select)
        
        # ==================== PANNELLO DESTRA: ASSOCIAZIONE ====================
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # Header
        ttk.Label(
            right_frame,
            text=self.lang.get('association', 'Associazione Ordini'),
            font=('Helvetica', 12, 'bold')
        ).pack(pady=(0, 10))
        
        # Info ordine selezionato
        info_frame = ttk.LabelFrame(right_frame, text=self.lang.get('selected_sale_order', 'Ordine di Vendita Selezionato'), padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(info_frame, text=self.lang.get('no_selection', 'Nessun ordine selezionato'), foreground='gray')
        self.info_label.pack()
        
        # Frame associazione
        assoc_frame = ttk.LabelFrame(right_frame, text=self.lang.get('add_production_order', 'Aggiungi Ordine di Produzione'), padding=10)
        assoc_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Combo ordini di produzione (editabile per filtro)
        ttk.Label(assoc_frame, text=self.lang.get('production_order', 'Ordine di Produzione:')).pack(anchor=tk.W)
        self.production_order_combo = ttk.Combobox(assoc_frame, width=50)
        self.production_order_combo.pack(fill=tk.X, pady=(5, 10))
        
        # Quantità
        qty_frame = ttk.Frame(assoc_frame)
        qty_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(qty_frame, text=self.lang.get('quantity', 'Quantità:')).pack(side=tk.LEFT, padx=(0, 5))
        self.qty_entry = ttk.Entry(qty_frame, width=15)
        self.qty_entry.pack(side=tk.LEFT)
        self.qty_entry.insert(0, '0')
        
        # Bottone aggiungi
        ttk.Button(
            assoc_frame,
            text=self.lang.get('btn_add_association', 'Aggiungi Associazione'),
            command=self._add_association
        ).pack()
        
        # Lista associazioni esistenti
        existing_frame = ttk.LabelFrame(right_frame, text=self.lang.get('existing_associations', 'Associazioni Esistenti'), padding=10)
        existing_frame.pack(fill=tk.BOTH, expand=True)
        
        list_frame = ttk.Frame(existing_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        assoc_columns = ('ProductionOrder', 'Product', 'Qty', 'DateIn')
        
        self.associations_tree = ttk.Treeview(list_frame, columns=assoc_columns, show='headings', selectmode='browse')
        
        self.associations_tree.heading('ProductionOrder', text=self.lang.get('col_production_order', 'Ordine Produzione'))
        self.associations_tree.heading('Product', text=self.lang.get('col_product', 'Prodotto'))
        self.associations_tree.heading('Qty', text=self.lang.get('col_quantity', 'Quantità'))
        self.associations_tree.heading('DateIn', text=self.lang.get('col_date_in', 'Data Ins.'))
        
        self.associations_tree.column('ProductionOrder', width=120)
        self.associations_tree.column('Product', width=150)
        self.associations_tree.column('Qty', width=80, anchor=tk.E)
        self.associations_tree.column('DateIn', width=100)
        
        assoc_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.associations_tree.yview)
        self.associations_tree.configure(yscrollcommand=assoc_scrollbar.set)
        
        self.associations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        assoc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottone elimina associazione
        ttk.Button(
            existing_frame,
            text=self.lang.get('btn_delete_association', 'Elimina Associazione'),
            command=self._delete_association
        ).pack(pady=(10, 0))
    
    def _load_sale_orders(self, filters=None):
        """Carica gli ordini di vendita con filtri opzionali"""
        try:
            # Pulisci treeview
            for item in self.sale_orders_tree.get_children():
                self.sale_orders_tree.delete(item)
            
            # Carica ordini - salviamo ItemCode separatamente per il filtro
            self.sale_orders_data = {}  # Dizionario per salvare ItemCode per ogni ordine
            orders = self.orders_manager.get_sale_orders_for_matching(filters)
            
            for order in orders:
                ship_date = order['ShipDateRequest'].strftime('%d/%m/%Y') if order['ShipDateRequest'] else ''
                product_display = f"{order['ItemCode'] or ''} [{order['ItemName'] or ''}]"
                
                qty_assigned = order['QtyAssigned'] or 0
                qty_remaining = (order['QtyOrder'] or 0) - qty_assigned
                
                # Salva ItemCode nel dizionario
                order_id = order['DynamicSaleOrderId']
                self.sale_orders_data[order_id] = {
                    'ItemCode': order['ItemCode'],
                    'ItemName': order['ItemName']
                }
                
                # Colora in verde se completamente assegnato
                tags = ()
                if qty_remaining <= 0:
                    tags = ('completed',)
                
                self.sale_orders_tree.insert('', tk.END, values=(
                    order['SONumber'] or '',
                    order['CustomerName'] or '',
                    product_display,
                    ship_date,
                    order['QtyOrder'] or 0,
                    qty_assigned,
                    qty_remaining
                ), tags=tags, iid=order_id)
            
            # Configura tag per ordini completati
            self.sale_orders_tree.tag_configure('completed', background='#90EE90')
            
        except Exception as e:
            logger.error(f"Errore nel caricamento ordini di vendita: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento ordini: {e}",
                parent=self
            )
    
    def _load_production_orders(self, product_code=None):
        """Carica gli ordini di produzione disponibili
        
        Args:
            product_code: Filtro opzionale per ProductCode
        """
        try:
            logger.info(f"_load_production_orders chiamato con ProductCode: {product_code}")
            self.production_orders_cache = self.orders_manager.get_available_production_orders(product_code)
            
            logger.info(f"Trovati {len(self.production_orders_cache)} ordini di produzione")
            
            # Popola combo
            display_values = [
                f"{po['OrderNumber']} - {po['Product']}" 
                for po in self.production_orders_cache
            ]
            self.production_order_combo['values'] = display_values
            
            logger.info(f"Combo popolato con {len(display_values)} valori")
            
            # Reset selezione combo
            if display_values:
                self.production_order_combo.current(0)
                logger.info(f"Selezionato primo elemento: {display_values[0]}")
            else:
                self.production_order_combo.set('')
                logger.warning("Nessun ordine di produzione trovato!")
            
        except Exception as e:
            logger.error(f"Errore nel caricamento ordini produzione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento ordini produzione: {e}",
                parent=self
            )
    
    def _apply_filters(self):
        """Applica i filtri alla lista ordini"""
        filters = {
            'so_number': self.filter_so_number.get().strip(),
            'customer': self.filter_customer.get().strip(),
            'product': self.filter_product.get().strip(),
            'date_from': self.filter_date_from.get_date(),
            'date_to': self.filter_date_to.get_date()
        }
        self._load_sale_orders(filters)
    
    def _reset_filters(self):
        """Resetta i filtri"""
        self.filter_so_number.delete(0, tk.END)
        self.filter_customer.delete(0, tk.END)
        self.filter_product.delete(0, tk.END)
        self.filter_date_from.set_date(datetime.now() - timedelta(days=90))
        self.filter_date_to.set_date(datetime.now() + timedelta(days=180))
        self._load_sale_orders()
    
    def _on_sale_order_select(self, event):
        """Gestisce la selezione di un ordine di vendita"""
        selection = self.sale_orders_tree.selection()
        if not selection:
            self.selected_sale_order = None
            self.info_label.config(text=self.lang.get('no_selection', 'Nessun ordine selezionato'), foreground='gray')
            # Ricarica tutti gli ordini produzione (nessun filtro)
            self._load_production_orders()
            return
        
        item_id = int(selection[0])
        
        # Recupera ItemCode dal dizionario che abbiamo salvato in _load_sale_orders
        item_code = self.sale_orders_data.get(item_id, {}).get('ItemCode')
        
        self.selected_sale_order = {
            'DynamicSaleOrderId': item_id,
            'values': self.sale_orders_tree.item(selection[0], 'values'),
            'ItemCode': item_code
        }
        
        # Aggiorna info
        so_number = self.selected_sale_order['values'][0]
        customer = self.selected_sale_order['values'][1]
        product_str = self.selected_sale_order['values'][2]
        qty_remaining = self.selected_sale_order['values'][6]
        
        logger.info(f"Ordine selezionato: {so_number}, ItemCode: {item_code}, Product: {product_str}")
        
        info_text = f"Ordine: {so_number} | Cliente: {customer} | Qtà Rimanente: {qty_remaining}"
        self.info_label.config(text=info_text, foreground='black')
        
        # Imposta quantità suggerita
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, str(qty_remaining))
        
        # Carica associazioni esistenti
        self._load_existing_associations()
        
        # Ricarica ordini produzione FILTRATI per lo stesso ProductCode
        logger.info(f"Caricamento ordini produzione filtrati per ProductCode: {item_code}")
        self._load_production_orders(item_code)
    
    def _load_existing_associations(self):
        """Carica le associazioni esistenti per l'ordine selezionato"""
        try:
            # Pulisci treeview
            for item in self.associations_tree.get_children():
                self.associations_tree.delete(item)
            
            if not self.selected_sale_order:
                return
            
            associations = self.orders_manager.get_production_associations(
                self.selected_sale_order['DynamicSaleOrderId']
            )
            
            for assoc in associations:
                date_in = assoc['DateIn'].strftime('%d/%m/%Y %H:%M') if assoc['DateIn'] else ''
                
                self.associations_tree.insert('', tk.END, values=(
                    assoc['OrderNumber'] or '',
                    assoc['Product'] or '',
                    assoc['Qty'] or 0,
                    date_in
                ), iid=assoc['DynamicProductionOrderID'])
            
        except Exception as e:
            logger.error(f"Errore nel caricamento associazioni: {e}", exc_info=True)
    
    def _add_association(self):
        """Aggiunge una nuova associazione"""
        try:
            if not self.selected_sale_order:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('select_sale_order_first', 'Seleziona prima un ordine di vendita'),
                    parent=self
                )
                return
            
            # Verifica combo produzione
            po_index = self.production_order_combo.current()
            if po_index < 0:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('select_production_order', 'Seleziona un ordine di produzione'),
                    parent=self
                )
                return
            
            # Verifica quantità
            try:
                qty = float(self.qty_entry.get())
                if qty <= 0:
                    raise ValueError("Quantità deve essere maggiore di zero")
            except ValueError as e:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('invalid_quantity', 'Quantità non valida'),
                    parent=self
                )
                return
            
            # Verifica quantità rimanente
            qty_remaining = float(self.selected_sale_order['values'][6])
            if qty > qty_remaining:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"{self.lang.get('qty_exceeds_remaining', 'La quantità eccede quella rimanente')}: {qty_remaining}",
                    parent=self
                )
                return
            
            # Crea associazione
            po_data = self.production_orders_cache[po_index]
            
            association_data = {
                'DynamicSaleOrderId': self.selected_sale_order['DynamicSaleOrderId'],
                'IdOrder': po_data['IdOrder'],
                'Qty': qty
            }
            
            self.orders_manager.create_production_association(association_data)
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('association_created', 'Associazione creata con successo'),
                parent=self
            )
            
            # Ricarica
            self._load_sale_orders()
            self._load_production_orders()  # Ricarica perché un ordine è stato assegnato
            self._load_existing_associations()
            
        except Exception as e:
            logger.error(f"Errore creazione associazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore creazione associazione: {e}",
                parent=self
            )
    
    def _delete_association(self):
        """Elimina un'associazione esistente"""
        try:
            selection = self.associations_tree.selection()
            if not selection:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('select_association', 'Seleziona un\'associazione da eliminare'),
                    parent=self
                )
                return
            
            if not messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('confirm_delete_association', 'Confermare eliminazione associazione?'),
                parent=self
            ):
                return
            
            item_id = int(selection[0])
            self.orders_manager.delete_production_association(item_id)
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('association_deleted', 'Associazione eliminata'),
                parent=self
            )
            
            # Ricarica
            self._load_sale_orders()
            self._load_production_orders()
            self._load_existing_associations()
            
        except Exception as e:
            logger.error(f"Errore eliminazione associazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore eliminazione associazione: {e}",
                parent=self
            )


def open_match_production_orders_window(master, db, lang, user_name):
    """
    Apre la finestra di accoppiamento ordini di produzione
    
    Args:
        master: Finestra padre
        db: Connessione database
        lang: Gestore traduzioni
        user_name: Nome utente loggato
    """
    from orders.orders_manager import OrdersManager
    
    orders_manager = OrdersManager(db)
    MatchProductionOrdersWindow(master, db, lang, orders_manager, user_name)
