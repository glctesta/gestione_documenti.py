"""
Modulo per la gestione delle validazioni di linea (FAI - First Article Inspection)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import logging
import os

logger = logging.getLogger("TraceabilityRS")


class ToolTip:
    """Crea un tooltip per un widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                        relief=tk.SOLID, borderwidth=1, font=('Arial', 9))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class LineValidationWindow(tk.Toplevel):
    """Finestra per l'inserimento e gestione delle validazioni FAI"""
    
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('line_validation_title', 'FAI - Validazione Linea'))
        self.geometry('1400x900')
        self.transient(parent)
        self.grab_set()
        
        # Dati
        self.current_fai_log_id = None
        self.current_order_id = None  # 🆕 Track ordine salvato
        self.current_order_date = None  # 🆕 Track data salvataggio
        self.step_details = []
        self.step_widgets = {}  # Dizionario per memorizzare i widget di ogni step
        self.templates_map = {}  # Dizionario per mappare i template
        self.orders_map = {}  # Dizionario per mappare gli ordini
        self.all_orders = []  # Lista completa ordini per filtro
        self._create_widgets()
        self._load_initial_data()
    
    def _create_widgets(self):
        """Crea la struttura UI principale"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # HEADER - Informazioni template e ordine
        self._create_header_section(main_frame)
        
        # SEPARATOR
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # CHECKLISTK - Dettagli step con checkbox OK/Not OK
        self._create_checklist_section(main_frame)
        
        # FOOTER - Pulsanti azione
        self._create_footer_section(main_frame)
    
    def _create_header_section(self, parent):
        """Crea la sezione header con template info e selezione ordine"""
        header_frame = ttk.LabelFrame(parent, text=self.lang.get('fai_header', 'Informazioni Validazione'), padding="10")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prima riga - Logo e Template Selector
        row1 = ttk.Frame(header_frame)
        row1.pack(fill=tk.X, pady=5)
        
        # Logo/Title
        ttk.Label(row1, text="◊ VANDEWIELE", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(row1, text="FORMULAR", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 20))
        
        # Template Selector
        ttk.Label(row1, text=self.lang.get('select_template', 'Template FAI:'), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(20, 5))
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(row1, textvariable=self.template_var, state='readonly', width=40)
        self.template_combo.pack(side=tk.LEFT, padx=5)
        self.template_combo.bind('<<ComboboxSelected>>', self._on_template_selected)
        
        # Seconda riga - Document info
        row2 = ttk.Frame(header_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Nr. document:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.doc_number_label = ttk.Label(row2, text="", font=('Arial', 9, 'bold'))
        self.doc_number_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(row2, text="Revizia:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.revision_label = ttk.Label(row2, text="", font=('Arial', 9, 'bold'))
        self.revision_label.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(row2, text="Data ultim rev:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.revision_date_label = ttk.Label(row2, text="", font=('Arial', 9, 'bold'))
        self.revision_date_label.grid(row=0, column=5, sticky=tk.W, padx=5)
        
        # Terza riga - Selezione ordine e prodotto
        row3 = ttk.Frame(header_frame)
        row3.pack(fill=tk.X, pady=10)
        
        order_label = ttk.Label(row3, text=self.lang.get('select_order', 'Seleziona Ordine:'), font=('Arial', 10, 'bold'))
        order_label.pack(side=tk.LEFT, padx=5)
        
        # Combobox EDITABILE per ricerca ordine
        self.order_var = tk.StringVar()
        self.order_combo = ttk.Combobox(
            row3, 
            textvariable=self.order_var,
            width=50,
            state='normal'  # ✅ Editabile invece di readonly
        )
        self.order_combo.pack(side=tk.LEFT, padx=5)
        
        # Bind per filtro ricerca live
        self.order_combo.bind('<KeyRelease>', self._filter_orders)
        self.order_combo.bind('<<ComboboxSelected>>', self._on_order_selected)
        
        # Quarta riga - Checkboxes tipo validazione
        row4 = ttk.Frame(header_frame)
        row4.pack(fill=tk.X, pady=10)
        
        self.npi_var = tk.BooleanVar()
        self.test_var = tk.BooleanVar()
        self.production_var = tk.BooleanVar()
        self.std_deviation_var = tk.BooleanVar()
        self.others_var = tk.BooleanVar()
        
        ttk.Checkbutton(row4, text="☐ NPI (PRESERIE)", variable=self.npi_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(row4, text="☐ TEST", variable=self.test_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(row4, text="☐ PRODUCȚIE", variable=self.production_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(row4, text="☐ VARIAȚIA STANDARD A PROCESULUI", variable=self.std_deviation_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(row4, text="☐ Others", variable=self.others_var).pack(side=tk.LEFT, padx=10)
        
        # Quinta riga - Cod prodotto e Quantità e Ordine
        row5 = ttk.Frame(header_frame)
        row5.pack(fill=tk.X, pady=5)
        
        ttk.Label(row5, text="Cod:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.product_code_entry = ttk.Entry(row5, width=20, state='readonly')
        self.product_code_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(row5, text="Cantitate:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.quantity_entry = ttk.Entry(row5, width=10, state='readonly')  # ✅ Readonly
        self.quantity_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(row5, text="Comanda SL:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.order_sl_label = ttk.Label(row5, text="", font=('Arial', 9, 'bold'))
        self.order_sl_label.grid(row=0, column=5, sticky=tk.W, padx=5)
        
        # Sesta riga - LabelCode
        row6 = ttk.Frame(header_frame)
        row6.pack(fill=tk.X, pady=5)
        
        ttk.Label(row6, text="LabelCode:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.labelcode_entry = ttk.Entry(row6, width=30)
        self.labelcode_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.labelcode_entry.bind('<Return>', self._validate_labelcode)  # Validazione con Enter
        
        ttk.Button(row6, text="Verifica", command=self._validate_labelcode).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Label per feedback validazione
        self.labelcode_status_label = ttk.Label(row6, text="", foreground="gray")
        self.labelcode_status_label.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Flag per tracciare validazione
        self.labelcode_validated = False
    
    def _create_checklist_section(self, parent):
        """Crea la sezione con la checklist degli step FAI"""
        checklist_frame = ttk.LabelFrame(parent, text=self.lang.get('fai_checklist', 'Checklist Validazione'), padding="10")
        checklist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame con scrollbar
        canvas_frame = ttk.Frame(checklist_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas e scrollbar
        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, background="#f0f0f0")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel (solo all'interno della finestra)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        # Header della checklist
        header = ttk.Frame(self.scrollable_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Configura le colonne del grid per header
        header.columnconfigure(0, minsize=250)  # Step
        header.columnconfigure(1, minsize=400)  # Descrizione
        header.columnconfigure(2, minsize=200)  # Equipment
        header.columnconfigure(3, minsize=40)   # OK
        header.columnconfigure(4, minsize=60)   # Not OK
        header.columnconfigure(5, minsize=250)  # Note
        
        ttk.Label(header, text="Step", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=2)
        ttk.Label(header, text="Descrizione", font=('Arial', 9, 'bold')).grid(row=0, column=1, sticky='w', padx=2)
        ttk.Label(header, text="Equipment", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky='w', padx=2)
        ttk.Label(header, text="OK", font=('Arial', 9, 'bold')).grid(row=0, column=3, sticky='w', padx=2)
        ttk.Label(header, text="Not OK", font=('Arial', 9, 'bold')).grid(row=0, column=4, sticky='w', padx=2)
        ttk.Label(header, text="Note", font=('Arial', 9, 'bold')).grid(row=0, column=5, sticky='w', padx=2)
        
        # Contenitore per gli step (sarà popolato dinamicamente)
        self.steps_container = ttk.Frame(self.scrollable_frame)
        self.steps_container.pack(fill=tk.BOTH, expand=True)
    
    def _on_mousewheel(self, event):
        """Gestisce lo scroll con la rotella del mouse"""
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            # Ignora errori se il canvas è stato distrutto
            pass
    
    def _create_footer_section(self, parent):
        """Crea la sezione footer con pulsanti"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 🆕 Salva riferimento pulsante Salva
        self.save_button = ttk.Button(footer_frame, text=self.lang.get('btn_save', 'Salva Validazione'), 
                   command=self._save_validation)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(footer_frame, text=self.lang.get('btn_print', 'Stampa'), 
                   command=self._print_validation).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(footer_frame, text=self.lang.get('btn_close', 'Chiudi'), 
                   command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(footer_frame, text="", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def _load_initial_data(self):
        """Carica i dati iniziali (template FAI e ordini)"""
        try:
            # Carica template FAI
            self._load_fai_templates()
            
            # Carica ordini
            self._load_orders()
            
        except Exception as e:
            logger.error(f"Errore caricamento dati iniziali: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i dati: {e}",
                parent=self
            )
    
    def _load_fai_templates(self):
        """Carica tutti i template FAI disponibili"""
        try:
            query = """
            SELECT 
                [FaiTemplateId],
                [NrDocument],
                [Revision],
                [FaiTitle],
                [RevisionDate]
            FROM [Traceability_RS].[fai].[FaiTemplates]
            ORDER BY [FaiTemplateId] DESC
            """
            
            logger.info(f"Esecuzione query template FAI...")
            try:
                self.db.cursor.execute(query)
                result = self.db.cursor.fetchall()
                logger.info(f"Query template FAI completata. Trovati {len(result)} risultati")
            except Exception as e:
                logger.error(f"Errore esecuzione query template: {e}")
                result = []
            
            # Verifica che result abbia elementi
            if result and len(result) > 0:
                logger.info(f"Trovati {len(result)} template FAI")
                self.templates_map = {
                    f"{template.NrDocument} - Rev.{template.Revision} - {template.FaiTitle}": {
                        'FaiTemplateId': template.FaiTemplateId,
                        'NrDocument': template.NrDocument,
                        'Revision': template.Revision,
                        'FaiTitle': template.FaiTitle,
                        'RevisionDate': template.RevisionDate
                    }
                    for template in result
                }
                
                self.template_combo['values'] = list(self.templates_map.keys())
                
                if self.templates_map:
                    self.template_combo.current(0)
                    self._on_template_selected()
            else:
                logger.warning("Nessun template FAI trovato")
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Nessun template FAI trovato nel database. Verificare la tabella FaiTemplates.',
                    parent=self
                )
                
        except Exception as e:
            logger.error(f"Errore caricamento template FAI: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i template FAI: {e}",
                parent=self
            )
    
    def _on_template_selected(self, event=None):
        """Gestisce la selezione di un template"""
        selected = self.template_var.get()
        if selected and selected in self.templates_map:
            template_data = self.templates_map[selected]
            
            # Aggiorna i campi della testata
            self.doc_number_label.config(text=template_data['NrDocument'] or "")
            self.revision_label.config(text=str(template_data['Revision'] or ""))
            
            if template_data['RevisionDate']:
                rev_date = template_data['RevisionDate'].strftime('%d/%m/%Y') if hasattr(template_data['RevisionDate'], 'strftime') else str(template_data['RevisionDate'])
                self.revision_date_label.config(text=rev_date)
            
            # Carica gli step per questo template
            self.current_template_id = template_data['FaiTemplateId']
            self._load_fai_steps()
    
    def _load_orders(self):
        """Carica gli ordini dal database (escludendo CIPR e RMA)"""
        try:
            query = """
            SELECT o.IDOrder, o.OrderNumber, o.orderquantity, p.productcode, p.productname 
            FROM [Traceability_RS].[dbo].[Orders] o
            INNER JOIN [Traceability_RS].[dbo].[Products] p ON o.IDProduct = p.IDProduct
            WHERE o.OrderNumber IS NOT NULL
                AND CHARINDEX('cipr', UPPER(p.productcode), 1) = 0 
                AND CHARINDEX('RMA', UPPER(p.productcode), 1) = 0
            ORDER BY o.OrderDate DESC
            """
            
            logger.info(f"Esecuzione query ordini...")
            try:
                self.db.cursor.execute(query)
                result = self.db.cursor.fetchall()
                logger.info(f"Query ordini completata. Trovati {len(result)} risultati")
            except Exception as e:
                logger.error(f"Errore esecuzione query ordini: {e}")
                result = []
            
            # Verifica che result abbia elementi
            if result and len(result) > 0:
                logger.info(f"Trovati {len(result)} ordini")
                self.orders_map = {
                    f"{row.OrderNumber} - {row.productcode} - {row.productname}": {
                        'IDOrder': row.IDOrder,
                        'OrderNumber': row.OrderNumber,
                        'OrderQuantity': row.orderquantity,
                        'ProductCode': row.productcode,
                        'ProductName': row.productname
                    }
                    for row in result
                }
                
                # Salva lista completa per filtro ricerca
                self.all_orders = list(self.orders_map.keys())
                self.order_combo['values'] = self.all_orders
                
                if self.orders_map:
                    self.order_combo.current(0)
                    self._on_order_selected()
            else:
                logger.warning("Nessun ordine trovato")
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Nessun ordine trovato nel database. Verificare:\n' +
                    '1. Tabella Orders con OrderDate >= 2025-08-01\n' +
                    '2. Prodotti senza CIPR o RMA nel codice',
                    parent=self
                )
                
        except Exception as e:
            logger.error(f"Errore caricamento ordini: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare gli ordini: {e}",
                parent=self
            )
    
    def _load_fai_steps(self):
        """Carica gli step FAI dal database per il template selezionato"""
        try:
            if not hasattr(self, 'current_template_id'):
                return
            
            
            # SELECT 
            #     t.FaiTitle,
            #     t.NrDocument,
            #     t.Revision,
            #     FORMAT(t.RevisionDate, 'd', 'ro-ro') as RevisionDate,
            #     ISNULL(fh.NPI, 0) as NPI,
            #     ISNULL(fh.Test, 0) as Test,
            #     ISNULL(fh.PRODUCTION, 0) as PRODUCTION,
            #     ISNULL(fh.StandardProcessDeviation, 0) as StandardProcessDeviation,
            #     ISNULL(fh.Others, 0) as Others,
            #     d.[FaiStepDetailId],
            #     s.StepName + ' -> ' + t.NrDocument as Step,
            #     d.[StepDetail],
            #     ISNULL(e.[Description], '') + ' ' + ISNULL(e.SerialNumber, '') as Equipment,
            #     s.OrderinList,
            #     d.OrdineList,
            #     l.DateIn,
            #     ISNULL(d.KeepOnsameLine, 0) as KeepOnsameLine
            # FROM [Traceability_RS].[fai].[FaiStepDetails] d
            # INNER JOIN [Traceability_RS].[fai].FaiSteps s ON d.FatStepId = s.FatStepId AND s.DateOut IS NULL
            # LEFT JOIN [Traceability_RS].[fai].FaiEquipments e ON d.FaiEquipmentId = e.FaiEquipmentid
            # INNER JOIN [Traceability_RS].[fai].FaiTemplates t ON t.FaiTemplateId = s.FaiTemplateId
            # LEFT JOIN Traceability_RS.fai.FaiLogs l ON l.FaiStepDetailId = d.FaiStepDetailId
            # LEFT JOIN traceability_rs.fai.FaiLogHeathers fh ON fh.[FaiLogId] = l.FaiLogId
            # WHERE d.DateOut IS NULL AND t.FaiTemplateId = ?
            # ORDER BY s.OrderinList, d.OrdineList
            query = """
            SELECT 
                t.FaiTitle,
                t.NrDocument,
                t.Revision,
                FORMAT(t.RevisionDate, 'd', 'ro-ro') as RevisionDate,
                0 as NPI,
                0 as Test,
                0 as PRODUCTION,
                0 as StandardProcessDeviation,
                '' as Others,
                d.[FaiStepDetailId],
                s.StepName + ' -> ' + t.NrDocument as Step,
                d.[StepDetail],
                ISNULL(e.[Description], '') + ' ' + ISNULL(e.SerialNumber, '') as Equipment,
                s.OrderinList,
                d.OrdineList,
                ''DateIn,
                ISNULL(d.KeepOnsameLine, 0) as KeepOnsameLine,
                ISNULL(d.NoteMandatory, 0) as NoteMandatory
            FROM [Traceability_RS].[fai].[FaiStepDetails] d
            INNER JOIN [Traceability_RS].[fai].FaiSteps s ON d.FatStepId = s.FatStepId AND s.DateOut IS NULL
            LEFT JOIN [Traceability_RS].[fai].FaiEquipments e ON d.FaiEquipmentId = e.FaiEquipmentid
            INNER JOIN [Traceability_RS].[fai].FaiTemplates t ON t.FaiTemplateId = s.FaiTemplateId
            WHERE d.DateOut IS NULL AND t.FaiTemplateId = ?
            ORDER BY s.OrderinList, d.OrdineList
            """
            
            try:
                self.db.cursor.execute(query, (self.current_template_id,))
                result = self.db.cursor.fetchall()
            except Exception as e:
                logger.error(f"Errore caricamento step FAI: {e}")
                result = []
            
            # Verifica che result abbia elementi
            if result and len(result) > 0:
                self.step_details = list(result)
                self._populate_checklist()
            else:
                logger.warning("Nessuno step FAI trovato")
                # Pulisce la checklist
                for widget in self.steps_container.winfo_children():
                    widget.destroy()
                
        except Exception as e:
            logger.error(f"Errore caricamento step FAI: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare gli step: {e}",
                parent=self
            )
    
    def _filter_orders(self, event=None):
        """Filtra gli ordini nel combobox mentre l'utente digita"""
        try:
            # Ottieni il testo corrente
            search_text = self.order_var.get().lower()
            
            # Filtra gli ordini che contengono il testo
            if search_text:
                filtered = [order for order in self.all_orders if search_text in order.lower()]
            else:
                filtered = self.all_orders
            
            # Aggiorna i valori del combobox
            self.order_combo['values'] = filtered
            
        except Exception as e:
            logger.error(f"Errore filtro ordini: {e}")
    
    def _populate_checklist(self):
        """Popola la checklist con gli step FAI"""
        # Pulisci container esistente
        for widget in self.steps_container.winfo_children():
            widget.destroy()
        
        # Resetta il dizionario dei widget
        self.step_widgets = {}
        
        # Configura le colonne del grid
        self.steps_container.columnconfigure(0, minsize=250)  # Step
        self.steps_container.columnconfigure(1, minsize=400)  # Descrizione
        self.steps_container.columnconfigure(2, minsize=200)  # Equipment
        self.steps_container.columnconfigure(3, minsize=40)   # OK
        self.steps_container.columnconfigure(4, minsize=60)   # Not OK
        self.steps_container.columnconfigure(5, minsize=250)  # Note
        
        # Crea una riga per ogni step
        for idx, step in enumerate(self.step_details):
            # Alterna colore sfondo
            bg_color = '#ffffff' if idx % 2 == 0 else '#f5f5f5'
            
            # Step name
            step_label = tk.Label(self.steps_container, text=step.Step, width=35, 
                                 background=bg_color, anchor='w', font=('Arial', 9))
            step_label.grid(row=idx, column=0, sticky='ew', padx=2, pady=1)
            
            # Description con tooltip
            desc_text = step.StepDetail[:50] + '...' if len(step.StepDetail) > 50 else step.StepDetail
            desc_label = tk.Label(self.steps_container, text=desc_text, width=55,
                                 background=bg_color, anchor='w', font=('Arial', 9))
            desc_label.grid(row=idx, column=1, sticky='ew', padx=2, pady=1)
            
            # Aggiungi tooltip se la descrizione è lunga
            if len(step.StepDetail) > 50:
                ToolTip(desc_label, step.StepDetail)
            
            # Equipment
            eq_label = tk.Label(self.steps_container, text=step.Equipment.strip(), width=28,
                               background=bg_color, anchor='w', font=('Arial', 9))
            eq_label.grid(row=idx, column=2, sticky='ew', padx=2, pady=1)
            
            # OK checkbox
            ok_var = tk.BooleanVar()
            ok_check = ttk.Checkbutton(self.steps_container, variable=ok_var)
            ok_check.grid(row=idx, column=3, padx=2, pady=1)
            
            # Not OK checkbox
            not_ok_var = tk.BooleanVar()
            not_ok_check = ttk.Checkbutton(self.steps_container, variable=not_ok_var)
            not_ok_check.grid(row=idx, column=4, padx=2, pady=1)
            
            # Configura i command ora che entrambe le variabili esistono
            ok_check.configure(command=lambda ok=ok_var, nok=not_ok_var, st=step: self._on_ok_check(ok, nok, st))
            not_ok_check.configure(command=lambda ok=ok_var, nok=not_ok_var, st=step: self._on_not_ok_check(ok, nok, st))
            
            # Note entry
            note_entry = ttk.Entry(self.steps_container, width=35, font=('Arial', 9))
            note_entry.grid(row=idx, column=5, sticky='ew', padx=2, pady=1)
            
            # Salva riferimenti nel dizionario usando FaiStepDetailId come chiave
            self.step_widgets[step.FaiStepDetailId] = {
                'ok_var': ok_var,
                'not_ok_var': not_ok_var,
                'note_entry': note_entry
            }
    
    def _on_ok_check(self, ok_var, not_ok_var, step_detail):
        """Gestisce il check di OK (deseleziona Not OK e gestisce KeepOnsameLine)"""
        if ok_var.get():
            not_ok_var.set(False)
            
            # Se KeepOnsameLine=true, deseleziona gli altri OK dello stesso gruppo
            if step_detail.KeepOnsameLine:
                # Trova tutti gli step con lo stesso FaiStepId ma diverso FaiStepDetailId
                for other_step in self.step_details:
                    if (other_step.FaiStepDetailId != step_detail.FaiStepDetailId and
                        hasattr(other_step, 'OrderinList') and hasattr(step_detail, 'OrderinList') and
                        other_step.OrderinList == step_detail.OrderinList and
                        other_step.KeepOnsameLine):
                        # Deseleziona OK per gli altri step dello stesso gruppo
                        other_step_id = other_step.FaiStepDetailId
                        if other_step_id in self.step_widgets:
                            self.step_widgets[other_step_id]['ok_var'].set(False)
    
    def _on_not_ok_check(self, ok_var, not_ok_var, step_detail):
        """Gestisce il check di Not OK (deseleziona OK e richiede dettagli problema)"""
        if not_ok_var.get():
            ok_var.set(False)
            
            # Apri dialog per raccogliere dettagli del problema
            step_id = step_detail.FaiStepDetailId
            if step_id in self.step_widgets:
                result = self._show_problem_dialog(step_detail)
                
                if result:
                    # Salva i dettagli nel dizionario
                    self.step_widgets[step_id]['problem_description'] = result['problem']
                    self.step_widgets[step_id]['root_cause'] = result['root_cause']
                    self.step_widgets[step_id]['corrective_action'] = result['corrective_action']
                else:
                    # Se l'utente annulla, deseleziona NOT OK
                    not_ok_var.set(False)
    
    def _show_problem_dialog(self, step_detail):
        """Mostra dialog per inserire dettagli del problema"""
        dialog = tk.Toplevel(self)
        dialog.title("Dettagli Problema - NOT OK")
        dialog.geometry("600x400")
        dialog.transient(self)
        dialog.grab_set()
        
        result = {}
        
        # Titolo
        title_label = ttk.Label(dialog, text=f"Step: {step_detail.Step}", 
                               font=('Arial', 10, 'bold'))
        title_label.pack(pady=10, padx=10)
        
        # Frame principale
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Problem Description
        ttk.Label(main_frame, text="Descriere problemă *:", 
                 font=('Arial', 9, 'bold')).pack(anchor='w', pady=(5, 2))
        problem_text = tk.Text(main_frame, height=4, width=60, font=('Arial', 9))
        problem_text.pack(fill=tk.X, pady=(0, 10))
        
        # Root Cause
        ttk.Label(main_frame, text="Cauza (Root Cause) *:", 
                 font=('Arial', 9, 'bold')).pack(anchor='w', pady=(5, 2))
        root_cause_text = tk.Text(main_frame, height=4, width=60, font=('Arial', 9))
        root_cause_text.pack(fill=tk.X, pady=(0, 10))
        
        # Corrective Action
        ttk.Label(main_frame, text="Acțiuni corective *:", 
                 font=('Arial', 9, 'bold')).pack(anchor='w', pady=(5, 2))
        corrective_text = tk.Text(main_frame, height=4, width=60, font=('Arial', 9))
        corrective_text.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def on_save():
            problem = problem_text.get("1.0", tk.END).strip()
            root_cause = root_cause_text.get("1.0", tk.END).strip()
            corrective = corrective_text.get("1.0", tk.END).strip()
            
            if not problem or not root_cause or not corrective:
                messagebox.showwarning(
                    "Attenzione",
                    "Tutti i campi sono obbligatori",
                    parent=dialog
                )
                return
            
            result['problem'] = problem
            result['root_cause'] = root_cause
            result['corrective_action'] = corrective
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Salva", command=on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annulla", command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Centra il dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        dialog.wait_window()
        return result if result else None
    
    def _on_order_selected(self, event=None):
        """Gestisce la selezione di un ordine"""
        selected = self.order_var.get()
        if selected and selected in self.orders_map:
            order_data = self.orders_map[selected]
            
            # Popola il codice prodotto
            self.product_code_entry.config(state='normal')
            self.product_code_entry.delete(0, tk.END)
            self.product_code_entry.insert(0, order_data['ProductCode'])
            self.product_code_entry.config(state='readonly')
            
            # Popola la quantità ordine
            self.quantity_entry.config(state='normal')
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, str(order_data.get('OrderQuantity', '')))
            self.quantity_entry.config(state='readonly')
            
            # Popola il numero ordine (IDOrder)
            self.order_sl_label.config(text=str(order_data['IDOrder']))
            
            # Reset validazione LabelCode
            self.labelcode_validated = False
            self.labelcode_entry.delete(0, tk.END)
            self.labelcode_status_label.config(text="", foreground="gray")
            
            # 🆕 Riabilita pulsante Salva se ordine diverso o giorno diverso
            self._check_enable_save_button(order_data['IDOrder'])
    
    def _check_enable_save_button(self, new_order_id):
        """Riabilita pulsante Salva solo se ordine diverso o giorno diverso"""
        from datetime import date
        today = date.today()
        
        # Abilita se: ordine diverso OPPURE stesso ordine ma giorno diverso
        if self.current_order_id != new_order_id or self.current_order_date != today:
            self.save_button.config(state='normal')
            logger.info(f"Pulsante Salva riabilitato (ordine={new_order_id}, data={today})")
        else:
            logger.info(f"Pulsante Salva resta disabilitato (stesso ordine={new_order_id}, stesso giorno={today})")
    
    def _validate_labelcode(self, event=None):
        """Valida il LabelCode inserito verificando che appartenga all'ordine selezionato"""
        labelcode_value = self.labelcode_entry.get().strip()
        
        if not labelcode_value:
            self.labelcode_status_label.config(text="Inserire un LabelCode", foreground="orange")
            self.labelcode_validated = False
            return
        
        # Verifica che un ordine sia selezionato
        selected_order = self.order_var.get()
        if not selected_order or selected_order not in self.orders_map:
            self.labelcode_status_label.config(text="Selezionare prima un ordine", foreground="red")
            self.labelcode_validated = False
            return
        
        order_data = self.orders_map[selected_order]
        current_order_id = order_data['IDOrder']
        
        try:
            # Query per verificare il LabelCode
            validation_query = """
            SELECT o.IDOrder, o.OrderNumber 
            FROM LabelCodes L 
            INNER JOIN Boards B ON b.IDBoard = l.IDBoard
            INNER JOIN orders o ON o.IDOrder = b.IDOrder
            WHERE l.labelcod = ?
            """
            
            logger.info(f"Validazione LabelCode: {labelcode_value} per ordine {current_order_id}")
            self.db.cursor.execute(validation_query, (labelcode_value,))
            result = self.db.cursor.fetchone()
            
            if result:
                # LabelCode trovato, verifica se corrisponde all'ordine selezionato
                if result.IDOrder == current_order_id:
                    self.labelcode_status_label.config(
                        text=f"✅ Validato (Ordine: {result.OrderNumber})", 
                        foreground="green"
                    )
                    self.labelcode_validated = True
                    logger.info(f"✅ LabelCode validato correttamente per ordine {current_order_id}")
                else:
                    self.labelcode_status_label.config(
                        text=f"❌ Codice appartiene a ordine {result.OrderNumber} (IDOrder: {result.IDOrder})", 
                        foreground="red"
                    )
                    self.labelcode_validated = False
                    logger.warning(f"❌ LabelCode {labelcode_value} appartiene a ordine diverso: {result.IDOrder} anziché {current_order_id}")
            else:
                self.labelcode_status_label.config(
                    text="❌ LabelCode non trovato nel database", 
                    foreground="red"
                )
                self.labelcode_validated = False
                logger.warning(f"❌ LabelCode {labelcode_value} non trovato nel database")
                
        except Exception as e:
            logger.error(f"Errore validazione LabelCode: {e}", exc_info=True)
            self.labelcode_status_label.config(
                text=f"❌ Errore validazione: {str(e)[:50]}", 
                foreground="red"
            )
            self.labelcode_validated = False
    
    def _validate_all_steps_filled(self):
        """Valida step considerando regola KeepOnsameLine"""
        missing_steps = []
        keep_on_same_line_groups = {}
        
        logger.info(f"Validazione step: totale step da controllare: {len(self.step_details)}")
        
        # Raggruppa step per FatStepId se hanno KeepOnsameLine=true
        for step in self.step_details:
            step_id = step.FaiStepDetailId
            if step_id in self.step_widgets:
                widgets = self.step_widgets[step_id]
                is_ok = widgets['ok_var'].get()
                is_not_ok = widgets['not_ok_var'].get()
                notes = widgets['note_entry'].get().strip()
                
                has_answer = (is_ok == True) or (is_not_ok == True)
                
                # 🆕 Validazione NoteMandatory
                if has_answer and hasattr(step, 'NoteMandatory') and step.NoteMandatory:
                    if not notes:
                        missing_steps.append(step.Step + " - ⚠️ Codice Stencil obbligatorio")
                        logger.warning(f"⚠️ Step {step.Step}: NoteMandatory=true ma note vuote")
                
                if step.KeepOnsameLine:
                    # Raggruppa per FatStepId (step principale)
                    group_key = step.OrderinList  # Usato come gruppo
                    if group_key not in keep_on_same_line_groups:
                        keep_on_same_line_groups[group_key] = []
                    keep_on_same_line_groups[group_key].append({
                        'step': step,
                        'has_answer': has_answer
                    })
                else:
                    # Step normale: DEVE avere risposta
                    if not has_answer:
                        missing_steps.append(f"{step.Step}")
                        logger.warning(f"⚠️ Step mancante: {step.Step}")
        
        # Verifica gruppi KeepOnsameLine: almeno UNO deve avere risposta
        for group_key, group_steps in keep_on_same_line_groups.items():
            has_any_answer = any(s['has_answer'] for s in group_steps)
            if not has_any_answer:
                # Nessuno step del gruppo ha risposta
                group_name = group_steps[0]['step'].Step
                missing_steps.append(f"Gruppo '{group_name}' (almeno uno dei {len(group_steps)})")
                logger.warning(f"⚠️ Gruppo mancante: {group_name}")
        
        logger.info(f"✅ Validazione completata: {len(missing_steps)} step mancanti")
        if missing_steps:
            logger.warning(f"Step mancanti: {', '.join(missing_steps[:5])}")
        
        return missing_steps
    
    def _save_validation(self):
        """Salva la validazione nel database"""
        logger.info("=" * 80)
        logger.info("🔵 PULSANTE SALVA CLICCATO - Inizio _save_validation")
        logger.info("=" * 80)
        
        try:
            # Validazione
            selected_order = self.order_var.get()
            logger.info(f"Ordine selezionato: {selected_order}")
            
            if not selected_order:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('select_order_first', 'Seleziona prima un ordine'),
                    parent=self
                )
                return
            
            order_data = self.orders_map[selected_order]
            logger.info(f"📊 Order data recuperato: IDOrder={order_data['IDOrder']}")
            
            # Verifica se esiste già una validazione per questo ordine oggi
            check_query = """
            SELECT TOP 1 l.FaiLogId, h.FaiLogHeatherId
            FROM [Traceability_RS].[fai].[FaiLogs] l
            LEFT JOIN [Traceability_RS].[fai].[FaiLogHeathers] h ON l.FaiLogId = h.FaiLogId
            WHERE l.OrderId = ? 
                AND CAST(l.DateIn AS DATE) = CAST(GETDATE() AS DATE)
            ORDER BY l.DateIn DESC
            """
            
            logger.info(f"🔍 Controllo duplicati per ordine {order_data['IDOrder']}...")
            self.db.cursor.execute(check_query, (order_data['IDOrder'],))
            existing = self.db.cursor.fetchone()
            
            if existing:
                logger.info(f"⚠️ Trovata validazione esistente: FaiLogId={existing.FaiLogId}")
                # Esiste già una validazione per questo ordine oggi
                response = messagebox.askyesno(
                    self.lang.get('warning', 'Attenzione'),
                    f"Esiste già una validazione FAI per questo ordine datata oggi.\n\n"
                    f"Vuoi ANNULLARE la precedente e crearne una nuova?\n\n"
                    f"(DateOut verrà impostato sulla validazione precedente)",
                    parent=self
                )
                
                if response:
                    # Elimina i record esistenti
                    try:
                        logger.info(f"Annullamento validazione precedente per ordine {order_data['IDOrder']}")
                        
                        # UPDATE DateOut sui record vecchi per annullarli (NO DELETE)
                        update_dateout_query = """
                        UPDATE [Traceability_RS].[fai].[FaiLogs]
                        SET DateOut = GETDATE()
                        WHERE OrderId = ? AND CAST(DateIn AS DATE) = CAST(GETDATE() AS DATE) AND DateOut IS NULL
                        """
                        self.db.cursor.execute(update_dateout_query, (order_data['IDOrder'],))
                        rows_updated = self.db.cursor.rowcount
                        
                        # UPDATE anche header
                        if existing.FaiLogId:
                            update_header_query = """
                            UPDATE [Traceability_RS].[fai].[FaiLogHeathers]
                            SET DateOut = GETDATE()
                            WHERE FaiLogId = ? AND DateOut IS NULL
                            """
                            self.db.cursor.execute(update_header_query, (existing.FaiLogId,))
                        
                        # Commit
                        self.db.conn.commit()
                        logger.info("Commit completato - validazione precedente eliminata")
                        
                    except Exception as del_error:
                        logger.error(f"Errore eliminazione validazione precedente: {del_error}", exc_info=True)
                        self.db.conn.rollback()
                        messagebox.showerror(
                            self.lang.get('error', 'Errore'),
                            f"Impossibile eliminare la validazione precedente: {del_error}",
                            parent=self
                        )
                        return
                else:
                    # L'utente ha scelto di non sovrascrivere
                    logger.info("❌ Utente ha scelto di non sovrascrivere - annullo salvataggio")
                    return
            else:
                logger.info("✅ Nessun duplicato trovato, procedo con validazione")
            
            # Verifica che tutti gli step abbiano risposta
            logger.info("🔎 Inizio validazione completezza step...")
            missing_steps = self._validate_all_steps_filled()
            
            logger.info(f"✅ Validazione completata: {len(missing_steps)} step mancanti")
            
            if missing_steps:
                logger.warning(f"⚠️ Blocco salvataggio: ci sono {len(missing_steps)} step mancanti")
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    f"Compila tutti gli step prima di salvare.\n\nStep mancanti:\n" + 
                    "\n".join(f"- {step}" for step in missing_steps[:10]) +
                    (f"\n... e altri {len(missing_steps) - 10}" if len(missing_steps) > 10 else ""),
                    parent=self
                )
                return
            
            # 🆕 Validazione LabelCode
            labelcode_value = self.labelcode_entry.get().strip()
            if not labelcode_value:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Inserire un LabelCode prima di salvare',
                    parent=self
                )
                return
            
            if not self.labelcode_validated:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Verificare il LabelCode prima di salvare (premere il pulsante Verifica)',
                    parent=self
                )
                return
            
            # Verifica almeno un tipo di validazione selezionato
            if not any([self.npi_var.get(), self.test_var.get(), self.production_var.get(), 
                       self.std_deviation_var.get(), self.others_var.get()]):
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('select_validation_type', 'Seleziona almeno un tipo di validazione'),
                    parent=self
                )
                return
            
            # Trova il primo step con risposta per creare il log master
            first_step_with_answer = None
            for step in self.step_details:
                step_id = step.FaiStepDetailId
                if step_id in self.step_widgets:
                    widgets = self.step_widgets[step_id]
                    if widgets['ok_var'].get() or widgets['not_ok_var'].get():
                        first_step_with_answer = step
                        break
            
            if not first_step_with_answer:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Seleziona almeno uno step (OK o NOT OK) prima di salvare',
                    parent=self
                )
                return
            
            # Inserisci il PRIMO record in FaiLogs per ottenere il FaiLogId auto-generato
            first_widgets = self.step_widgets[first_step_with_answer.FaiStepDetailId]
            is_ok = first_widgets['ok_var'].get()
            is_not_ok = first_widgets['not_ok_var'].get()
            notes = first_widgets['note_entry'].get().strip()
            problem_desc = notes if is_not_ok else None
            
            # Usa OUTPUT per recuperare l'ID generato direttamente
            first_log_query = """
            INSERT INTO Traceability_RS.fai.FaiLogs 
            (FaiStepDetailId, Operator, IsOk, ProblemDescription, RoutCauseProblem, CorrectiveAction, Dati, OrderId, DateIn, LabelCode)
            OUTPUT INSERTED.FaiLogId
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
            """
            
            # Recupera dettagli problema se NOT OK
            root_cause = first_widgets.get('root_cause', None) if is_not_ok else None
            corrective = first_widgets.get('corrective_action', None) if is_not_ok else None
            
            first_log_params = (
                first_step_with_answer.FaiStepDetailId,
                self.user_name,
                1 if is_ok else 0,
                problem_desc,
                root_cause,
                corrective,
                notes,  # 🆕 Salva note/codice stencil in Dati
                order_data['IDOrder'],
                labelcode_value  # 🆕 LabelCode validato
            )
            
            # Usa cursor direttamente 
            try:
                logger.info(f"Inserimento primo record FaiLogs per step {first_step_with_answer.FaiStepDetailId}")
                self.db.cursor.execute(first_log_query, first_log_params)
                
                # OUTPUT restituisce il valore direttamente
                result = self.db.cursor.fetchone()
                fai_log_id = int(result[0]) if result and result[0] else None
                
                if not fai_log_id:
                    raise Exception("OUTPUT INSERTED.FaiLogId non ha ritornato un valore")
                
                logger.info(f"FaiLogId generato: {fai_log_id}")
                
            except Exception as insert_error:
                logger.error(f"Errore inserimento primo record: {insert_error}", exc_info=True)
                self.db.conn.rollback()
                raise Exception(f"Errore inserimento primo record FaiLogs: {insert_error}")
            
            # Inserisci gli ALTRI dettagli in FaiLogs con lo stesso FaiLogId
            for step in self.step_details:
                if step.FaiStepDetailId == first_step_with_answer.FaiStepDetailId:
                    continue  # Già inserito
                
                step_id = step.FaiStepDetailId
                if step_id in self.step_widgets:
                    widgets = self.step_widgets[step_id]
                    is_ok = widgets['ok_var'].get()
                    is_not_ok = widgets['not_ok_var'].get()
                    notes = widgets['note_entry'].get().strip()
                    
                    # Inserisci nel log solo se è stato checkato qualcosa
                    if is_ok or is_not_ok:
                        log_query = """
                        INSERT INTO Traceability_RS.fai.FaiLogs 
                        (FaiStepDetailId, Operator, IsOk, ProblemDescription, RoutCauseProblem, CorrectiveAction, Dati, OrderId, DateIn, LabelCode)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
                        """
                        
                        problem_desc = notes if is_not_ok else None
                        root_cause = widgets.get('root_cause', None) if is_not_ok else None
                        corrective = widgets.get('corrective_action', None) if is_not_ok else None
                        
                        log_params = (
                            step_id,
                            self.user_name,
                            1 if is_ok else 0,
                            problem_desc,
                            root_cause,
                            corrective,
                            notes,  # 🆕 Salva note/codice stencil in Dati
                            order_data['IDOrder'],
                            labelcode_value  # 🆕 LabelCode validato
                        )
                        
                        self.db.execute_query(log_query, log_params)
            
            # ORA inserisci l'header in FaiLogHeathers usando il FaiLogId valido
            header_query = """
            INSERT INTO Traceability_RS.fai.FaiLogHeathers 
            (FaiLogId, NPI, Test, PRODUCTION, StandardProcessDeviation, Others, SerialNumberInterval)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            header_params = (
                fai_log_id,
                1 if self.npi_var.get() else 0,
                1 if self.test_var.get() else 0,
                1 if self.production_var.get() else 0,
                1 if self.std_deviation_var.get() else 0,
                1 if self.others_var.get() else 0,
                labelcode_value  # 🆕 Salva LabelCode validato in SerialNumberInterval
            )
            
            # Esegui insert header
            result = self.db.execute_query(header_query, header_params)
            
            if not result:
                logger.error("Errore inserimento header FAI")
                self.db.conn.rollback()
                raise Exception("Errore inserimento header FAI")
            
            # Commit finale di tutta la transazione
            self.db.conn.commit()
            logger.info(f"Validazione FAI salvata con successo - FaiLogId: {fai_log_id}")
            
            self.current_fai_log_id = fai_log_id
            
            # Calcola risultato finale (basato sull'ultimo step)
            final_result = True
            last_step_ok = None
            for step in reversed(self.step_details):
                step_id = step.FaiStepDetailId
                if step_id in self.step_widgets:
                    widgets = self.step_widgets[step_id]
                    if widgets['ok_var'].get() or widgets['not_ok_var'].get():
                        last_step_ok = widgets['ok_var'].get()
                        break
            
            final_result = last_step_ok if last_step_ok is not None else True
            
            # Invia email di notifica
            try:
                from fai_report_generator import generate_fai_report
                from utils import get_email_recipients, send_email
                from email_connector import EmailSender
                import tempfile
                import os # Aggiunto per os.path.join
                from datetime import datetime # Aggiunto per datetime.now()
                
                # Genera PDF report
                pdf_path = os.path.join(tempfile.gettempdir(), f"FAI_Report_{fai_log_id}.pdf")
                if generate_fai_report(fai_log_id, self.db, pdf_path):
                    logger.info(f"Report FAI generato: {pdf_path}")
                    
                    # Salva PDF nel database come binary
                    try:
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_binary = pdf_file.read()
                        
                        # UPDATE primo record FaiLogs con il PDF
                        update_pdf_query = """
                        UPDATE Traceability_RS.fai.FaiLogs
                        SET DocVerification = ?
                        WHERE FaiLogId = ?
                        """
                        self.db.cursor.execute(update_pdf_query, (pdf_binary, fai_log_id))
                        self.db.conn.commit()
                        logger.info(f"PDF salvato nel database: {len(pdf_binary)} bytes")
                    
                    except Exception as pdf_error:
                        logger.error(f"Errore salvataggio PDF nel database: {pdf_error}", exc_info=True)
                
                # Recupera destinatari email
                recipients = get_email_recipients(self.db.conn, 'Sys_verifica_linea')
                
                if recipients:
                    product_name = order_data.get('ProductName', order_data.get('ProductCode', 'Unknown'))
                    order_num = order_data.get('OrderNumber', order_data.get('IDOrder', 'Unknown'))
                    
                    # Crea subject
                    result_text = 'PASSED ✓' if final_result else 'FAILED ✗'
                    subject = f"FAI Validation Report - {product_name} - Order {order_num} - {result_text}"
                    
                    # Crea corpo HTML
                    result_color = "green" if final_result else "red"
                    result_label = "PASSED" if final_result else "FAILED"
                    result_icon = "✓" if final_result else "✗"
                    
                    html_body = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; }}
                            .header {{ background-color: #003366; color: white; padding: 20px; }}
                            .content {{ padding: 20px; }}
                            .result {{ 
                                font-size: 24px; 
                                font-weight: bold; 
                                color: {result_color}; 
                                padding: 10px;
                                border: 2px solid {result_color};
                                display: inline-block;
                                margin: 10px 0;
                            }}
                            .info-table {{ 
                                border-collapse: collapse; 
                                width: 100%; 
                                margin: 20px 0;
                            }}
                            .info-table td {{ 
                                padding: 8px; 
                                border: 1px solid #ddd; 
                            }}
                            .info-table td:first-child {{ 
                                font-weight: bold; 
                                background-color: #f0f0f0;
                                width: 30%;
                            }}
                        </style>
                    </head>  
                    <body>
                        <div class="header">
                            <h2>FAI (First Article Inspection) Validation Report</h2>
                        </div>
                        <div class="content">
                            <div class="result">
                                Risultato Finale: {result_label} {result_icon}
                            </div>
                            
                            <table class="info-table">
                                <tr>
                                    <td>Product:</td>
                                    <td><strong>{product_name}</strong></td>
                                </tr>
                                <tr>
                                    <td>Order Number:</td>
                                    <td><strong>{order_num}</strong></td>
                                </tr>
                                <tr>
                                    <td>Validation Date:</td>
                                    <td>{datetime.now().strftime('%d/%m/%Y %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td>Operator:</td>
                                    <td>{self.user_name}</td>
                                </tr>
                                <tr>
                                    <td>FAI Log ID:</td>
                                    <td>{fai_log_id}</td>
                                </tr>
                            </table>
                            
                            <p>
                                Il report FAI completo è allegato a questa email in formato PDF.
                            </p>
                            
                            <p style="color: #666; font-size: 12px; margin-top: 30px;">
                                Questa è una email automatica generata dal sistema di tracciabilità.
                                <br>Per qualsiasi domanda, contattare il reparto qualità.
                            </p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # Usa EmailSender direttamente per gestire allegati
                    sender = EmailSender("vandewiele-com.mail.protection.outlook.com", 25)
                    sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")
                    
                    # Invia con allegato PDF
                    sender.send_email(
                        to_email=', '.join(recipients),
                        subject=subject,
                        body=html_body,
                        is_html=True,
                        attachments=[pdf_path]  # ✅ Lista di allegati
                    )
                    
                    logger.info(f"Email FAI inviata a: {', '.join(recipients)}")
                else:
                    logger.warning("Nessun destinatario configurato per Sys_verifica_linea")
                    messagebox.showinfo(
                        self.lang.get('info', 'Info'),
                        'Validazione salvata ma email non inviata:\n'
                        'Nessun destinatario configurato in Settings (Sys_verifica_linea)',
                        parent=self
                    )
                        
            except Exception as email_error:
                logger.error(f"Errore invio email FAI: {email_error}", exc_info=True)
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    f'Validazione salvata ma email non inviata:\n{str(email_error)}',
                    parent=self
                )
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('validation_saved', 'Validazione salvata con successo'),
                parent=self
            )
            
            self.status_label.config(text=f"Validazione salvata - ID: {fai_log_id}", foreground="green")
            
            # 🆕 Disabilita pulsante Salva e traccia ordine/data
            from datetime import date
            self.current_order_id = order_data['IDOrder']
            self.current_order_date = date.today()
            self.save_button.config(state='disabled')
            logger.info(f"Pulsante Salva disabilitato (ordine={self.current_order_id}, data={self.current_order_date})")
            
        except Exception as e:
            logger.error(f"Errore salvataggio validazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare la validazione: {e}",
                parent=self
            )
    
    def _print_validation(self):
        """Genera e stampa il report PDF della validazione"""
        try:
            if not self.current_fai_log_id:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    'Salva prima la validazione per poterla stampare',
                    parent=self
                )
                return
            
            # Importa il generatore di report
            from fai_report_generator import generate_fai_report
            import tempfile
            import os
            import subprocess
            
            # Genera PDF in temp
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, f'FAI_Report_{self.current_fai_log_id}.pdf')
            
            # Genera il report
            success = generate_fai_report(self.current_fai_log_id, self.db, pdf_path)
            
            if success and os.path.exists(pdf_path):
                # Apri il PDF con il viewer predefinito
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path)
                else:  # Linux/Mac
                    subprocess.call(['xdg-open', pdf_path])
                
                logger.info(f"Report FAI aperto: {pdf_path}")
                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    f'Report generato:\n{pdf_path}',
                    parent=self
                )
            else:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    'Errore durante la generazione del report PDF',
                    parent=self
                )
                
        except Exception as e:
            logger.error(f"Errore stampa validazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile stampare: {e}",
                parent=self
            )


def open_line_validation_window(parent, db, lang, user_name):
    """Apre la finestra di validazione linea"""
    LineValidationWindow(parent, db, lang, user_name)
