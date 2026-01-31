
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger("TraceabilityRS")

class LabelConfigWindow(tk.Toplevel):
    """Finestra per la configurazione delle etichette."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"LabelConfigWindow: Apertura finestra configurazione (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('label_config_window_title', 'Configurazione Etichetta'))
        self.geometry('700x600')
        self.transient(parent)
        self.grab_set()
        
        self.config_id = None
        
        self._create_widgets()
        self._load_configuration()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')
        
        # Frame principale con scrollbar
        main_canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # === SEZIONE DIMENSIONI ETICHETTA ===
        dimensions_frame = ttk.LabelFrame(scrollable_frame, 
                                         text=self.lang.get('label_dimensions_section', 'Dimensioni Etichetta'),
                                         padding="15")
        dimensions_frame.pack(fill='x', padx=10, pady=10)
        
        # Larghezza
        ttk.Label(dimensions_frame, text=self.lang.get('label_width', 'Larghezza (cm)') + ':').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.width_var = tk.DoubleVar(value=10.0)
        width_spinbox = ttk.Spinbox(dimensions_frame, from_=1.0, to=50.0, increment=0.5,
                                    textvariable=self.width_var, width=10)
        width_spinbox.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # Altezza
        ttk.Label(dimensions_frame, text=self.lang.get('label_height', 'Altezza (cm)') + ':').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        
        self.height_var = tk.DoubleVar(value=5.0)
        height_spinbox = ttk.Spinbox(dimensions_frame, from_=1.0, to=50.0, increment=0.5,
                                     textvariable=self.height_var, width=10)
        height_spinbox.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # === SEZIONE CAMPI DA STAMPARE ===
        fields_frame = ttk.LabelFrame(scrollable_frame,
                                     text=self.lang.get('fields_to_print_section', 'Campi da Stampare'),
                                     padding="15")
        fields_frame.pack(fill='x', padx=10, pady=10)
        
        # Header
        ttk.Label(fields_frame, text=self.lang.get('field_name', 'Campo'), 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Label(fields_frame, text=self.lang.get('print_field', 'Stampa'), 
                 font=('Arial', 9, 'bold')).grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Label(fields_frame, text=self.lang.get('field_position', 'Posizione'), 
                 font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        
        # Numero Ordine
        ttk.Label(fields_frame, text=self.lang.get('print_order_number', 'Numero Ordine')).grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        
        self.print_order_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(fields_frame, variable=self.print_order_var,
                       command=self._on_field_toggle).grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        self.order_position_var = tk.IntVar(value=1)
        self.order_position_spin = ttk.Spinbox(fields_frame, from_=1, to=4, increment=1,
                                               textvariable=self.order_position_var, width=5)
        self.order_position_spin.grid(row=1, column=2, sticky='w', padx=5, pady=5)
        
        # Codice Materiale
        ttk.Label(fields_frame, text=self.lang.get('print_material_code', 'Codice Materiale')).grid(
            row=2, column=0, sticky='w', padx=5, pady=5)
        
        self.print_material_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(fields_frame, variable=self.print_material_var,
                       command=self._on_field_toggle).grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        self.material_position_var = tk.IntVar(value=2)
        self.material_position_spin = ttk.Spinbox(fields_frame, from_=1, to=4, increment=1,
                                                 textvariable=self.material_position_var, width=5)
        self.material_position_spin.grid(row=2, column=2, sticky='w', padx=5, pady=5)
        
        # Quantità Componenti
        ttk.Label(fields_frame, text=self.lang.get('print_component_qty', 'Quantità Componenti')).grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        
        self.print_qty_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(fields_frame, variable=self.print_qty_var,
                       command=self._on_field_toggle).grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        self.qty_position_var = tk.IntVar(value=3)
        self.qty_position_spin = ttk.Spinbox(fields_frame, from_=1, to=4, increment=1,
                                            textvariable=self.qty_position_var, width=5)
        self.qty_position_spin.grid(row=3, column=2, sticky='w', padx=5, pady=5)
        
        # Riferimenti Scheda
        ttk.Label(fields_frame, text=self.lang.get('print_references', 'Riferimenti Scheda')).grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        
        self.print_refs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(fields_frame, variable=self.print_refs_var,
                       command=self._on_field_toggle).grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        self.refs_position_var = tk.IntVar(value=4)
        self.refs_position_spin = ttk.Spinbox(fields_frame, from_=1, to=4, increment=1,
                                             textvariable=self.refs_position_var, width=5)
        self.refs_position_spin.grid(row=4, column=2, sticky='w', padx=5, pady=5)
        
        # Info
        ttk.Label(fields_frame, 
                 text=self.lang.get('position_info', 'La posizione determina l\'ordine di stampa (1=primo, 4=ultimo)'),
                 font=('Arial', 8), foreground='gray').grid(row=5, column=0, columnspan=3, sticky='w', pady=10)
        
        # Frame pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text='💾 ' + self.lang.get('save_button', 'Salva'),
                  command=self._save_configuration).pack(side='right', padx=5)
        ttk.Button(button_frame, text='❌ ' + self.lang.get('cancel_button', 'Annulla'),
                  command=self.destroy).pack(side='right', padx=5)
    
    def _on_field_toggle(self):
        """Gestisce l'abilitazione/disabilitazione dei controlli posizione."""
        self.order_position_spin.config(state='normal' if self.print_order_var.get() else 'disabled')
        self.material_position_spin.config(state='normal' if self.print_material_var.get() else 'disabled')
        self.qty_position_spin.config(state='normal' if self.print_qty_var.get() else 'disabled')
        self.refs_position_spin.config(state='normal' if self.print_refs_var.get() else 'disabled')
    
    def _load_configuration(self):
        """Carica la configurazione corrente dal database."""
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT TOP 1 
                ConfigID, LabelWidth, LabelHeight,
                PrintOrderNumber, PrintMaterialCode, PrintComponentQuantity, PrintReferences,
                OrderNumberPosition, MaterialCodePosition, ComponentQuantityPosition, ReferencesPosition
            FROM [Traceability_RS].[dbo].[LabelConfiguration]
            WHERE IsActive = 1
            ORDER BY ConfigID DESC
            """
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                (self.config_id, width, height,
                 print_order, print_material, print_qty, print_refs,
                 order_pos, material_pos, qty_pos, refs_pos) = row
                
                # Imposta i valori
                self.width_var.set(float(width) if width else 10.0)
                self.height_var.set(float(height) if height else 5.0)
                
                self.print_order_var.set(bool(print_order))
                self.print_material_var.set(bool(print_material))
                self.print_qty_var.set(bool(print_qty))
                self.print_refs_var.set(bool(print_refs))
                
                self.order_position_var.set(order_pos if order_pos else 1)
                self.material_position_var.set(material_pos if material_pos else 2)
                self.qty_position_var.set(qty_pos if qty_pos else 3)
                self.refs_position_var.set(refs_pos if refs_pos else 4)
                
                self._on_field_toggle()
                
                logger.info(f"Configurazione caricata: ID={self.config_id}")
            else:
                logger.warning("Nessuna configurazione trovata, uso valori di default")
                self._on_field_toggle()
        
        except Exception as e:
            logger.error(f"Errore caricamento configurazione: {e}")
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Errore caricamento configurazione:\n{e}",
                parent=self
            )
    
    def _save_configuration(self):
        """Salva la configurazione nel database."""
        try:
            # Validazione
            width = self.width_var.get()
            height = self.height_var.get()
            
            if width <= 0 or height <= 0:
                messagebox.showwarning(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('invalid_dimensions', 'Le dimensioni devono essere maggiori di zero'),
                    parent=self
                )
                return
            
            # Verifica che almeno un campo sia selezionato
            if not any([self.print_order_var.get(), self.print_material_var.get(),
                       self.print_qty_var.get(), self.print_refs_var.get()]):
                messagebox.showwarning(
                    self.lang.get('warning_title', 'Attenzione'),
                    self.lang.get('select_at_least_one_field', 'Seleziona almeno un campo da stampare'),
                    parent=self
                )
                return
            
            cursor = self.db.conn.cursor()
            
            if self.config_id:
                # Update esistente
                query = """
                UPDATE [Traceability_RS].[dbo].[LabelConfiguration]
                SET LabelWidth = ?,
                    LabelHeight = ?,
                    PrintOrderNumber = ?,
                    PrintMaterialCode = ?,
                    PrintComponentQuantity = ?,
                    PrintReferences = ?,
                    OrderNumberPosition = ?,
                    MaterialCodePosition = ?,
                    ComponentQuantityPosition = ?,
                    ReferencesPosition = ?,
                    ModifiedDate = GETDATE(),
                    ModifiedBy = ?
                WHERE ConfigID = ?
                """
                cursor.execute(query,
                             width, height,
                             self.print_order_var.get(), self.print_material_var.get(),
                             self.print_qty_var.get(), self.print_refs_var.get(),
                             self.order_position_var.get() if self.print_order_var.get() else None,
                             self.material_position_var.get() if self.print_material_var.get() else None,
                             self.qty_position_var.get() if self.print_qty_var.get() else None,
                             self.refs_position_var.get() if self.print_refs_var.get() else None,
                             self.user_name,
                             self.config_id)
            else:
                # Nuovo insert
                query = """
                INSERT INTO [Traceability_RS].[dbo].[LabelConfiguration]
                    (LabelWidth, LabelHeight, PrintOrderNumber, PrintMaterialCode,
                     PrintComponentQuantity, PrintReferences,
                     OrderNumberPosition, MaterialCodePosition,
                     ComponentQuantityPosition, ReferencesPosition,
                     CreatedBy, ModifiedBy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query,
                             width, height,
                             self.print_order_var.get(), self.print_material_var.get(),
                             self.print_qty_var.get(), self.print_refs_var.get(),
                             self.order_position_var.get() if self.print_order_var.get() else None,
                             self.material_position_var.get() if self.print_material_var.get() else None,
                             self.qty_position_var.get() if self.print_qty_var.get() else None,
                             self.refs_position_var.get() if self.print_refs_var.get() else None,
                             self.user_name, self.user_name)
            
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('config_saved', 'Configurazione salvata con successo!'),
                parent=self
            )
            logger.info(f"Configurazione etichetta salvata da {self.user_name}")
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio configurazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Errore salvataggio configurazione:\n{e}",
                parent=self
            )
