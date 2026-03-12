# label_printing_gui.py
"""
Modulo per la gestione della stampa etichette.
Gestisce:
- Selezione ordini per stampa etichette
- Impostazioni stampante (da implementare)
- Configurazione etichette (dimensioni e campi)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import qrcode
from io import BytesIO

logger = logging.getLogger("TraceabilityRS")


def open_label_print_window(parent, db, lang, user_name):
    """Apre la finestra di stampa etichette."""
    LabelPrintWindow(parent, db, lang, user_name)


def open_printer_settings_window(parent, db, lang, user_name):
    """Apre la finestra impostazioni stampante."""
    PrinterSettingsWindow(parent, db, lang, user_name)


def open_label_config_window(parent, db, lang, user_name):
    """Apre la finestra di configurazione etichetta."""
    from label_config_window import LabelConfigWindow
    LabelConfigWindow(parent, db, lang, user_name)



class LabelPrintWindow(tk.Toplevel):
    """Finestra per la stampa etichette."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"LabelPrintWindow: Apertura finestra stampa etichette (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('label_print_window_title', 'Stampa Etichette'))
        self.geometry('1000x650')
        self.transient(parent)
        self.grab_set()
        
        self.selected_order_id = None
        self.selected_order_number = None
        self.orders_dict = {}
        self.label_data = []
        self.phases_list = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')
        
        # Frame principale
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Ricerca ordine con text box
        ttk.Label(main_frame, text=self.lang.get('order_label', 'Ordine') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.order_search_var = tk.StringVar()
        self.order_search_entry = ttk.Entry(search_frame, textvariable=self.order_search_var, width=30)
        self.order_search_entry.pack(side='left', fill='x', expand=True)
        self.order_search_entry.bind('<Return>', lambda e: self._search_orders())
        
        ttk.Button(search_frame, text=self.lang.get('search_button', '🔍 Cerca'),
                   command=self._search_orders).pack(side='left', padx=(5, 0))
        
        # Treeview per i risultati della ricerca
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        
        self.orders_tree = ttk.Treeview(results_frame, columns=('OrderNumber',), show='headings', height=5)
        self.orders_tree.heading('OrderNumber', text=self.lang.get('order_number', 'Numero Ordine'))
        self.orders_tree.column('OrderNumber', width=300)
        self.orders_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.orders_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.bind('<<TreeviewSelect>>', self._on_order_selected)
        self.orders_tree.bind('<Double-1>', self._on_order_selected)
        
        # Frame per informazioni ordine
        info_frame = ttk.LabelFrame(main_frame, text=self.lang.get('order_info', 'Informazioni Ordine'), 
                                     padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=10)
        
        # Numero ordine
        ttk.Label(info_frame, text=self.lang.get('order_number', 'Numero Ordine') + ':').grid(
            row=0, column=0, sticky='w', padx=5, pady=2)
        self.order_number_label = ttk.Label(info_frame, text='-', font=('Arial', 9, 'bold'))
        self.order_number_label.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Codice prodotto
        ttk.Label(info_frame, text=self.lang.get('product_code', 'Codice Prodotto') + ':').grid(
            row=1, column=0, sticky='w', padx=5, pady=2)
        self.product_code_label = ttk.Label(info_frame, text='-', font=('Arial', 9, 'bold'))
        self.product_code_label.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        # Quantità
        ttk.Label(info_frame, text=self.lang.get('quantity', 'Quantità') + ':').grid(
            row=2, column=0, sticky='w', padx=5, pady=2)
        self.quantity_label = ttk.Label(info_frame, text='-', font=('Arial', 9, 'bold'))
        self.quantity_label.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        # Selezione fase
        ttk.Label(main_frame, text=self.lang.get('phase_label', 'Fase') + ' *').grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        
        self.phase_combo = ttk.Combobox(main_frame, state='disabled', width=40)
        self.phase_combo.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.phase_combo.bind('<<ComboboxSelected>>', self._on_phase_selected)
        
        # Label per conteggio componenti
        ttk.Label(main_frame, text=self.lang.get('components_count_label', 'Componenti disponibili') + ':').grid(
            row=3, column=2, sticky='w', padx=5, pady=5)
        self.components_count_label = ttk.Label(main_frame, text='-', font=('Arial', 9, 'bold'))
        self.components_count_label.grid(row=3, column=3, sticky='w', padx=5, pady=2)
        
        # Codice componente
        ttk.Label(main_frame, text=self.lang.get('component_code', 'Codice Componente') + ' *').grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        
        self.component_code_var = tk.StringVar()
        self.component_code_entry = ttk.Entry(main_frame, textvariable=self.component_code_var, width=40)
        self.component_code_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        # Premendo Invio nel campo Codice Componente si avvia la stampa
        self.component_code_entry.bind('<Return>', lambda e: self._on_print())
        
        main_frame.columnconfigure(1, weight=1)
        
        # Spacer
        ttk.Label(main_frame, text='').grid(row=5, column=0, columnspan=2, pady=10)
        
        main_frame.rowconfigure(1, weight=1)
        
        # Frame pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text=self.lang.get('print_button', 'Stampa'),
                  command=self._on_print).pack(side='right', padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', 'Annulla'),
                  command=self._on_cancel).pack(side='right', padx=5)
    
    def _search_orders(self):
        """Cerca gli ordini nel database usando LIKE senza limiti di data."""
        search_text = self.order_search_var.get().strip()
        if not search_text:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('enter_order_search', 'Inserisci un numero ordine o parte di esso'),
                parent=self
            )
            return
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT TOP 100 IDOrder, OrderNumber
            FROM [Traceability_RS].[dbo].[Orders]
            WHERE OrderNumber LIKE ?
            ORDER BY OrderNumber DESC
            """
            cursor.execute(query, f'%{search_text}%')
            rows = cursor.fetchall()
            cursor.close()
            
            # Pulisci risultati precedenti
            self.orders_dict = {}
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)
            self._reset_order_info()
            
            for row in rows:
                order_id, order_number = row
                self.orders_dict[order_number] = order_id
                self.orders_tree.insert('', 'end', values=(order_number,))
            
            if rows:
                logger.info(f"Trovati {len(rows)} ordini per ricerca '{search_text}'")
            else:
                logger.warning(f"Nessun ordine trovato per ricerca '{search_text}'")
                messagebox.showinfo(
                    self.lang.get('info_title', 'Informazione'),
                    self.lang.get('no_orders_found_search', search_text),
                    parent=self
                )
        
        except Exception as e:
            logger.error(f"Errore ricerca ordini: {e}")
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Errore ricerca ordini:\n{e}",
                parent=self
            )
    
    def _on_order_selected(self, event=None):
        """Gestisce la selezione di un ordine dalla Treeview."""
        selection = self.orders_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        order_number = self.orders_tree.item(item, 'values')[0]
        
        if order_number and order_number in self.orders_dict:
            self.selected_order_id = self.orders_dict[order_number]
            self.selected_order_number = order_number
            logger.info(f"Ordine selezionato: {order_number} (ID: {self.selected_order_id})")
            self._load_order_data()
    
    def _on_phase_selected(self, event=None):
        """Gestisce la selezione di una fase."""
        selected_phase = self.phase_combo.get()
        if selected_phase:
            logger.info(f"Fase selezionata: {selected_phase}")
            self._update_components_count()
    
    def _update_components_count(self):
        """Aggiorna il conteggio dei componenti per la fase selezionata."""
        selected_phase = self.phase_combo.get()
        
        if not selected_phase or not self.label_data:
            self.components_count_label.config(text='-')
            return
        
        # Filtra i componenti per la fase selezionata
        filtered_components = [
            d for d in self.label_data 
            if d['ParentPhaseName'] == selected_phase
        ]
        
        # Conta i componenti unici
        unique_components = set(d['ComponentCode'] for d in filtered_components)
        count = len(unique_components)
        
        # Aggiorna il label
        self.components_count_label.config(text=str(count))
        logger.info(f"Componenti per fase '{selected_phase}': {count}")
    
    def _load_order_data(self):
        """Carica i dati dell'ordine selezionato."""
        try:
            cursor = self.db.conn.cursor()
            
            # Query con i dettagli componenti e riferimenti
            query = """
            DECLARE @Ordernumber VARCHAR(250) = ?;

            WITH AggregatedRiferimenti AS (
                SELECT
                    PCE.IDProduct,
                    PCE.IDComponent,
                    STUFF(
                        (SELECT DISTINCT ', ' + PR.CodRiferimento
                         FROM ProductRiferiments PR
                         INNER JOIN ProductComponentsErp PCE_inner ON PR.IDProductCompErp = PCE_inner.IDProductCompErp
                         WHERE PCE_inner.IDProduct = PCE.IDProduct
                           AND PCE_inner.IDComponent = PCE.IDComponent
                         FOR XML PATH(''), TYPE
                        ).value('.', 'NVARCHAR(MAX)')
                    , 1, 2, '') AS CodRiferimentiConcatenati
                FROM ProductComponentsErp PCE
                GROUP BY
                    PCE.IDProduct,
                    PCE.IDComponent
            )
            SELECT
                P.ProductCode,
                O.OrderNumber,
                O.OrderQuantity,
                C.ComponentCode,
                C.ComponentDescription,
                AR.CodRiferimentiConcatenati,
                pp.ParentPhaseName
            FROM Orders O
            INNER JOIN Products P ON P.IDProduct = O.IDProduct
            INNER JOIN ProductComponentsErp PCE ON PCE.IDProduct = P.IDProduct
            INNER JOIN ProductRiferiments PR ON PR.IDProductCompErp = PCE.IDProductCompErp
            INNER JOIN Components C ON PCE.IDComponent = C.IDComponent
            INNER JOIN ParentPhases pp ON pp.IDParentPhase = PR.IDParentPhase
            LEFT JOIN AggregatedRiferimenti AR ON AR.IDProduct = PCE.IDProduct AND AR.IDComponent = PCE.IDComponent
            WHERE O.OrderNumber = @Ordernumber
            GROUP BY
                O.IDProduct,
                P.ProductCode,
                O.IDOrder,
                O.OrderNumber,
                O.OrderQuantity,
                C.ComponentCode,
                C.ComponentDescription,
                AR.CodRiferimentiConcatenati,
                pp.ParentPhaseName
            """
            
            cursor.execute(query, self.selected_order_number)
            rows = cursor.fetchall()
            cursor.close()
            
            if rows:
                # Salva i dati
                self.label_data = []
                phases_set = set()
                
                product_code = None
                order_number = None
                order_quantity = None
                
                for row in rows:
                    product_code, order_number, order_quantity, component_code, component_desc, cod_riferimenti, parent_phase = row
                    
                    self.label_data.append({
                        'ProductCode': product_code,
                        'OrderNumber': order_number,
                        'OrderQuantity': order_quantity,
                        'ComponentCode': component_code,
                        'ComponentDescription': component_desc,
                        'CodRiferimenti': cod_riferimenti,
                        'ParentPhaseName': parent_phase
                    })
                    
                    if parent_phase:
                        phases_set.add(parent_phase)
                
                # Aggiorna le label con le informazioni ordine
                self.order_number_label.config(text=order_number or '-')
                self.product_code_label.config(text=product_code or '-')
                self.quantity_label.config(text=str(order_quantity) if order_quantity else '-')
                
                # Popola il combo delle fasi
                self.phases_list = sorted(list(phases_set))
                self.phase_combo['values'] = self.phases_list
                
                # Imposta PTHM come default se presente, altrimenti la prima fase
                if 'PTHM' in self.phases_list:
                    self.phase_combo.set('PTHM')
                elif self.phases_list:
                    self.phase_combo.set(self.phases_list[0])
                
                self.phase_combo.config(state='readonly')
                
                # Aggiorna il conteggio dei componenti per la fase selezionata
                self._update_components_count()
                
                # Posiziona il focus sul campo component code
                self.component_code_entry.focus_set()
                
                logger.info(f"Caricati {len(self.label_data)} record per ordine {order_number}")
                logger.info(f"Fasi trovate: {len(phases_set)}")
            else:
                logger.warning(f"Nessun dato trovato per ordine {self.selected_order_number}")
                messagebox.showwarning(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('no_data_for_order', 'Nessun dato trovato per questo ordine'),
                    parent=self
                )
                # Reset
                self._reset_order_info()
        
        except Exception as e:
            logger.error(f"Errore caricamento dati ordine: {e}")
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Errore caricamento dati ordine:\n{e}",
                parent=self
            )
            self._reset_order_info()
    
    def _reset_order_info(self):
        """Reset delle informazioni ordine."""
        self.order_number_label.config(text='-')
        self.product_code_label.config(text='-')
        self.quantity_label.config(text='-')
        self.phase_combo.set('')
        self.phase_combo['values'] = []
        self.phase_combo.config(state='disabled')
        self.components_count_label.config(text='-')
        self.label_data = []
        self.phases_list = []
    
    def _on_print(self):
        """Gestisce il click sul pulsante Stampa."""
        logger.info("🖱️ GUI: Utente ha cliccato sul pulsante Stampa")
        
        # Validazione
        if not self.selected_order_number:
            logger.warning("🖱️ GUI: Validazione fallita - Nessun ordine selezionato")
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('select_order', 'Seleziona un ordine'),
                parent=self
            )
            return
        
        if not self.phase_combo.get():
            logger.warning("🖱️ GUI: Validazione fallita - Nessuna fase selezionata")
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('select_phase', 'Seleziona una fase'),
                parent=self
            )
            return
        
        # Validazione codice componente
        component_code = self.component_code_var.get().strip()
        if not component_code:
            logger.warning("🖱️ GUI: Validazione fallita - Nessun codice componente inserito")
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('enter_component_code', 'Inserisci il codice componente'),
                parent=self
            )
            return
        
        logger.info(f"🖱️ GUI: Validazione completata - Ordine: {self.order_combo.get()}, Fase: {self.phase_combo.get()}, Componente: {component_code}")
        
        # Filtra i dati in base alla fase selezionata
        selected_phase = self.phase_combo.get()
        filtered_data = [d for d in self.label_data if d['ParentPhaseName'] == selected_phase]
        
        # Filtra per codice componente
        component_data = [d for d in filtered_data if d['ComponentCode'] == component_code]
        
        if not component_data:
            logger.warning(f"🖱️ GUI: Componente '{component_code}' non trovato per la fase '{selected_phase}'")
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('component_not_found', f'Componente "{component_code}" non trovato per la fase selezionata'),
                parent=self
            )
            return
        
        # Prendi il primo record (dovrebbe essere unico per componente+fase)
        label_to_print = component_data[0]
        
        # Prepara i dati completi per l'etichetta
        label_print_data = {
            'OrderNumber': label_to_print['OrderNumber'],
            'ComponentCode': label_to_print['ComponentCode'],
            'ComponentDescription': label_to_print.get('ComponentDescription', ''),
            'OrderQuantity': label_to_print['OrderQuantity'],
            'References': label_to_print['CodRiferimenti'] or 'N/A',
            'Phase': label_to_print['ParentPhaseName'],
            'ProductCode': label_to_print['ProductCode']
        }
        
        logger.info(f"🖱️ GUI: Dati etichetta preparati - {label_print_data}")
        
        # Genera QR code per il component code
        try:
            logger.info(f"🖱️ GUI: Generazione QR code per componente '{component_code}'...")
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(component_code)
            qr.make(fit=True)
            
            # Crea l'immagine QR code
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Salva in BytesIO per uso futuro
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            
            label_print_data['QRCodeImage'] = qr_buffer
            
            logger.info(f"🖱️ GUI: ✓ QR code generato con successo per componente: {component_code}")
        except Exception as e:
            logger.error(f"🖱️ GUI: ❌ Errore generazione QR code: {e}")
            label_print_data['QRCodeImage'] = None
        
        # Stampa l'etichetta usando il modulo label_printer
        logger.info("🖱️ GUI: Chiamata al modulo label_printer per stampare l'etichetta...")
        from label_printer import print_label
        
        success, error_msg = print_label(label_print_data, self.db)
        
        if success:
            logger.info(f"🖱️ GUI: ✅ Stampa completata con successo!")
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('label_printed', 'Etichetta stampata con successo!'),
                parent=self
            )
            logger.info(f"🖱️ GUI: Etichetta stampata - Ordine: {self.selected_order_number}, "
                       f"Componente: {component_code}, Fase: {selected_phase}")
            # Reset campo e torna al Codice Componente per il prossimo inserimento
            self.component_code_var.set('')
            self.component_code_entry.focus_set()
        else:
            logger.error(f"🖱️ GUI: ❌ Errore durante la stampa: {error_msg}")
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"{self.lang.get('print_error', 'Errore durante la stampa')}:\n{error_msg}",
                parent=self
            )
            logger.error(f"🖱️ GUI: Errore stampa etichetta: {error_msg}")

    
    def _on_cancel(self):
        """Chiude la finestra."""
        logger.info("LabelPrintWindow: Chiusura finestra")
        self.destroy()


class PrinterSettingsWindow(tk.Toplevel):
    """Finestra per le impostazioni della stampante."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"PrinterSettingsWindow: Apertura finestra impostazioni (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('printer_settings_window_title', 'Impostazioni Stampante'))
        self.geometry('700x500')
        self.transient(parent)
        self.grab_set()
        
        # Importa i moduli necessari
        from printer_config import PrinterConfigManager
        from printer_connection_manager import get_available_printers, get_default_printer
        
        self.config_manager = PrinterConfigManager()
        self.get_available_printers = get_available_printers
        self.get_default_printer = get_default_printer
        
        self._create_widgets()
        self._load_current_config()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')
        
        # Frame principale
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Titolo
        ttk.Label(main_frame, text=self.lang.get('select_printer_type', 'Seleziona tipo di connessione stampante:'),
                  font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Radio buttons per tipo connessione
        self.connection_type_var = tk.StringVar(value='DEFAULT')
        
        radio_frame = ttk.Frame(main_frame)
        radio_frame.pack(fill='x', pady=10)
        
        ttk.Radiobutton(radio_frame, text=self.lang.get('default_printer', '🖨️ Stampante di Default Windows'),
                       variable=self.connection_type_var, value='DEFAULT',
                       command=self._on_connection_type_changed).pack(anchor='w', pady=5)
        
        ttk.Radiobutton(radio_frame, text=self.lang.get('usb_printer', '🔌 Stampante USB (Zebra/Brother)'),
                       variable=self.connection_type_var, value='USB',
                       command=self._on_connection_type_changed).pack(anchor='w', pady=5)
        
        ttk.Radiobutton(radio_frame, text=self.lang.get('ip_printer', '🌐 Stampante IP/Network'),
                       variable=self.connection_type_var, value='IP',
                       command=self._on_connection_type_changed).pack(anchor='w', pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Frame per configurazione dinamica
        self.config_frame = ttk.LabelFrame(main_frame, text=self.lang.get('printer_config', 'Configurazione'),
                                           padding="15")
        self.config_frame.pack(fill='both', expand=True, pady=10)
        
        # --- Frame per Default Printer ---
        self.default_frame = ttk.Frame(self.config_frame)
        
        ttk.Label(self.default_frame, text=self.lang.get('current_default_printer', 'Stampante di default corrente:'),
                  font=('Arial', 9)).grid(row=0, column=0, sticky='w', pady=5)
        
        self.default_printer_label = ttk.Label(self.default_frame, text='-', 
                                               font=('Arial', 9, 'bold'), foreground='blue')
        self.default_printer_label.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Button(self.default_frame, text='🔄 ' + self.lang.get('refresh', 'Aggiorna'),
                  command=self._refresh_default_printer).grid(row=0, column=2, padx=5)
        
        ttk.Label(self.default_frame, 
                  text=self.lang.get('default_printer_info', 
                                    'La stampante di default di Windows verrà utilizzata per la stampa.'),
                  wraplength=500, justify='left').grid(row=1, column=0, columnspan=3, sticky='w', pady=10)
        
        # --- Frame per USB Printer ---
        self.usb_frame = ttk.Frame(self.config_frame)
        
        ttk.Label(self.usb_frame, text=self.lang.get('select_usb_printer', 'Seleziona stampante USB:') + ' *').grid(
            row=0, column=0, sticky='w', pady=5)
        
        self.usb_printer_combo = ttk.Combobox(self.usb_frame, state='readonly', width=40)
        self.usb_printer_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Button(self.usb_frame, text='🔍 ' + self.lang.get('detect_printers', 'Rileva Stampanti'),
                  command=self._detect_usb_printers).grid(row=0, column=2, padx=5)
        
        ttk.Label(self.usb_frame, text=self.lang.get('printer_model', 'Modello:') + ' *').grid(
            row=1, column=0, sticky='w', pady=5)
        
        self.printer_model_var = tk.StringVar(value='ZEBRA')
        model_frame = ttk.Frame(self.usb_frame)
        model_frame.grid(row=1, column=1, sticky='w', pady=5)
        ttk.Radiobutton(model_frame, text='Zebra', variable=self.printer_model_var, 
                       value='ZEBRA').pack(side='left', padx=5)
        ttk.Radiobutton(model_frame, text='Brother', variable=self.printer_model_var, 
                       value='BROTHER').pack(side='left', padx=5)
        ttk.Radiobutton(model_frame, text='ZJIANG ZJ-9210', variable=self.printer_model_var, 
                       value='ZJIANG').pack(side='left', padx=5)
        
        self.usb_frame.columnconfigure(1, weight=1)
        
        # --- Frame per IP Printer ---
        self.ip_frame = ttk.Frame(self.config_frame)
        
        ttk.Label(self.ip_frame, text=self.lang.get('printer_ip', 'Indirizzo IP:') + ' *').grid(
            row=0, column=0, sticky='w', pady=5)
        
        self.ip_var = tk.StringVar()
        ttk.Entry(self.ip_frame, textvariable=self.ip_var, width=20).grid(
            row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.ip_frame, text=self.lang.get('printer_port', 'Porta:') + ' *').grid(
            row=1, column=0, sticky='w', pady=5)
        
        self.port_var = tk.StringVar(value='9100')
        ttk.Entry(self.ip_frame, textvariable=self.port_var, width=10).grid(
            row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.ip_frame, text=self.lang.get('ip_printer_info', 
                                                     '(Porta standard: 9100 per Zebra, 9100 per Brother)'),
                  font=('Arial', 8), foreground='gray').grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        # Mostra il frame di default inizialmente
        self.default_frame.pack(fill='both', expand=True)
        
        # Frame pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text='🧪 ' + self.lang.get('test_connection', 'Test Connessione'),
                  command=self._test_connection).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text='💾 ' + self.lang.get('save_button', 'Salva'),
                  command=self._save_config).pack(side='right', padx=5)
        ttk.Button(button_frame, text='❌ ' + self.lang.get('cancel_button', 'Annulla'),
                  command=self.destroy).pack(side='right', padx=5)
    
    def _on_connection_type_changed(self):
        """Gestisce il cambio di tipo connessione"""
        # Nascondi tutti i frame
        self.default_frame.pack_forget()
        self.usb_frame.pack_forget()
        self.ip_frame.pack_forget()
        
        # Mostra il frame appropriato
        conn_type = self.connection_type_var.get()
        if conn_type == 'DEFAULT':
            self.default_frame.pack(fill='both', expand=True)
            self._refresh_default_printer()
        elif conn_type == 'USB':
            self.usb_frame.pack(fill='both', expand=True)
            self._detect_usb_printers()
        elif conn_type == 'IP':
            self.ip_frame.pack(fill='both', expand=True)
    
    def _refresh_default_printer(self):
        """Aggiorna la stampante di default"""
        default_printer = self.get_default_printer()
        if default_printer:
            self.default_printer_label.config(text=default_printer)
            logger.info(f"Stampante di default: {default_printer}")
        else:
            self.default_printer_label.config(text=self.lang.get('no_default_printer', 'Nessuna stampante di default'))
            logger.warning("Nessuna stampante di default trovata")
    
    def _detect_usb_printers(self):
        """Rileva le stampanti USB disponibili"""
        printers = self.get_available_printers()
        if printers:
            self.usb_printer_combo['values'] = printers
            logger.info(f"Rilevate {len(printers)} stampanti")
        else:
            self.usb_printer_combo['values'] = []
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('no_printers_found', 'Nessuna stampante rilevata sul sistema'),
                parent=self
            )
    
    def _load_current_config(self):
        """Carica la configurazione corrente"""
        config = self.config_manager.get_config()
        conn_type = config.get('connection_type', 'DEFAULT')
        
        self.connection_type_var.set(conn_type)
        
        if conn_type == 'USB':
            self.usb_printer_combo.set(config.get('usb_printer_name', ''))
            self.printer_model_var.set(config.get('printer_model', 'ZEBRA'))
        elif conn_type == 'IP':
            self.ip_var.set(config.get('ip', ''))
            self.port_var.set(str(config.get('port', 9100)))
        
        self._on_connection_type_changed()
        logger.info(f"Configurazione caricata: {conn_type}")
    
    def _test_connection(self):
        """Testa la connessione alla stampante"""
        from printer_connection_manager import get_printer_connection, PrinterConnectionError
        
        conn_type = self.connection_type_var.get()
        
        try:
            # Crea la configurazione di test
            if conn_type == 'DEFAULT':
                config = {'connection_type': 'DEFAULT'}
            elif conn_type == 'USB':
                usb_printer = self.usb_printer_combo.get()
                if not usb_printer:
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('select_usb_printer', 'Seleziona una stampante USB'),
                        parent=self
                    )
                    return
                config = {
                    'connection_type': 'USB',
                    'usb_printer_name': usb_printer,
                    'printer_model': self.printer_model_var.get()
                }
            elif conn_type == 'IP':
                if not self.ip_var.get():
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('enter_ip', 'Inserisci l\'indirizzo IP'),
                        parent=self
                    )
                    return
                try:
                    port = int(self.port_var.get())
                except ValueError:
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('invalid_port', 'Porta non valida'),
                        parent=self
                    )
                    return
                config = {
                    'connection_type': 'IP',
                    'ip': self.ip_var.get(),
                    'port': port
                }
            
            # Testa la connessione
            printer_conn = get_printer_connection(config)
            if printer_conn.test_connection():
                messagebox.showinfo(
                    self.lang.get('success_title', 'Successo'),
                    self.lang.get('connection_test_success', 'Test connessione riuscito!\n\n') + 
                    printer_conn.get_status(),
                    parent=self
                )
                logger.info("Test connessione stampante riuscito")
            else:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    self.lang.get('connection_test_failed', 'Test connessione fallito'),
                    parent=self
                )
        except PrinterConnectionError as e:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"{self.lang.get('connection_error', 'Errore di connessione')}:\n{str(e)}",
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore test connessione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"{self.lang.get('test_error', 'Errore durante il test')}:\n{str(e)}",
                parent=self
            )
    
    def _save_config(self):
        """Salva la configurazione"""
        conn_type = self.connection_type_var.get()
        
        try:
            if conn_type == 'DEFAULT':
                self.config_manager.update_default_config()
            elif conn_type == 'USB':
                usb_printer = self.usb_printer_combo.get()
                if not usb_printer:
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('select_usb_printer', 'Seleziona una stampante USB'),
                        parent=self
                    )
                    return
                self.config_manager.update_usb_config(usb_printer, self.printer_model_var.get())
            elif conn_type == 'IP':
                if not self.ip_var.get():
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('enter_ip', 'Inserisci l\'indirizzo IP'),
                        parent=self
                    )
                    return
                try:
                    port = int(self.port_var.get())
                except ValueError:
                    messagebox.showwarning(
                        self.lang.get('warning_title', 'Attenzione'),
                        self.lang.get('invalid_port', 'Porta non valida'),
                        parent=self
                    )
                    return
                self.config_manager.update_ip_config(self.ip_var.get(), port)
            
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('config_saved', 'Configurazione salvata con successo!'),
                parent=self
            )
            logger.info(f"Configurazione stampante salvata: {conn_type}")
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio configurazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"{self.lang.get('save_error', 'Errore durante il salvataggio')}:\n{str(e)}",
                parent=self
            )
