"""
scrap_validation_gui.py
Modulo per la validazione delle dichiarazioni di scrap.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ScrapValidationWindow(tk.Toplevel):
    """Finestra per la validazione delle dichiarazioni di scrap."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.parent = parent

        self.title(self.lang.get('scrap_validation_title', 'Validazione Scarti'))
        self.geometry('1200x700')
        self.resizable(True, True)

        # Variabili di stato
        self.selected_declaration = None
        self.scrap_declarations = []  # Memorizza i dati completi delle dichiarazioni
        self.labelcod_map = {}  # Mappa labelcod -> dichiarazione completa

        # ⚠️ IMPORTANTE: Prima crea i widget, POI carica i dati
        self._create_widgets()
        self._load_scrap_declarations()  # ✅ Chiamato DOPO _create_widgets()

        # Centra la finestra
        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        """Crea l'interfaccia grafica"""
        # Frame principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ========== SEZIONE SUPERIORE: LISTA DICHIARAZIONI ==========
        list_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('pending_declarations', 'Dichiarazioni in Attesa'),
            padding=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview con scrollbar
        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            'id', 'date', 'order', 'product_code', #'product_name',
            'area', 'quantity', 'reason', 'declared_by', 'status'
        )

        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll.set,
            selectmode='browse'
        )
        tree_scroll.config(command=self.tree.yview)

        # Configurazione colonne
        self.tree.heading('id', text='ID')
        self.tree.heading('date', text=self.lang.get('date', 'Data'))
        self.tree.heading('order', text=self.lang.get('order', 'Ordine'))
        self.tree.heading('product_code', text=self.lang.get('product_code', 'Codice Prodotto'))
        self.tree.heading('area', text=self.lang.get('area', 'Area'))
        self.tree.heading('quantity', text=self.lang.get('quantity', 'Quantità'))
        self.tree.heading('reason', text=self.lang.get('reason', 'Causale'))
        self.tree.heading('declared_by', text=self.lang.get('declared_by', 'Dichiarato da'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))

        # Larghezze colonne
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('date', width=120, anchor='center')
        self.tree.column('order', width=100)
        self.tree.column('product_code', width=120)
        self.tree.column('area', width=150)
        self.tree.column('quantity', width=80, anchor='center')
        self.tree.column('reason', width=150)
        self.tree.column('declared_by', width=150)
        self.tree.column('status', width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self._on_tree_double_click)

        # ========== SEZIONE CENTRALE: INSERIMENTO LABELCODE ==========
        input_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('enter_labelcode', 'Inserisci Label Code per Validazione'),
            padding=10
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Frame per input labelcode
        labelcode_frame = ttk.Frame(input_frame)
        labelcode_frame.pack(fill=tk.X)

        ttk.Label(
            labelcode_frame,
            text=self.lang.get('label_code', 'Label Code:'),
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.labelcode_var = tk.StringVar()
        self.labelcode_entry = ttk.Entry(
            labelcode_frame,
            textvariable=self.labelcode_var,
            font=('Arial', 12),
            width=20
        )
        self.labelcode_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.labelcode_entry.bind('<Return>', self._on_labelcode_entered)

        ttk.Button(
            labelcode_frame,
            text=self.lang.get('validate_code', 'Valida Code'),
            command=self._on_labelcode_entered
        ).pack(side=tk.LEFT, padx=(0, 10))

        # Label per messaggi di stato
        self.validation_status_label = ttk.Label(
            labelcode_frame,
            text='',
            font=('Arial', 10)
        )
        self.validation_status_label.pack(side=tk.LEFT, padx=(10, 0))

        # ========== SEZIONE INFERIORE: DETTAGLI E AZIONI ==========
        details_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('declaration_details', 'Dettagli Dichiarazione'),
            padding=10
        )
        details_frame.pack(fill=tk.BOTH, expand=False)

        # Frame info (sinistra)
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Labels per i dettagli
        self.detail_labels = {}
        details = [
            ('order', 'Ordine'),
            ('product_code', 'Codice Prodotto'),
            ('area', 'Area'),
            ('quantity', 'Quantità Scartata'),
            ('reason', 'Causale'),
            ('declared_by', 'Dichiarato da'),
            ('date', 'Data Dichiarazione')
        ]

        for i, (key, label) in enumerate(details):
            ttk.Label(
                info_frame,
                text=f"{self.lang.get(key, label)}:",
                font=('Arial', 9, 'bold')
            ).grid(row=i, column=0, sticky='w', pady=2)

            self.detail_labels[key] = ttk.Label(
                info_frame,
                text='-',
                font=('Arial', 9)
            )
            self.detail_labels[key].grid(row=i, column=1, sticky='w', padx=(10, 0), pady=2)

        # ========== PULSANTI AZIONE ==========
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        self.approve_button = ttk.Button(
            buttons_frame,
            text=self.lang.get('approve', '✓ Approva'),
            command=lambda: self._validate_declaration('Approved'),
            style='Success.TButton',
            state='disabled'  # Disabilitato inizialmente
        )
        self.approve_button.pack(side=tk.LEFT, padx=5)

        self.reject_button = ttk.Button(
            buttons_frame,
            text=self.lang.get('reject', '✗ Rifiuta'),
            command=lambda: self._validate_declaration('Rejected'),
            style='Danger.TButton',
            state='disabled'  # Disabilitato inizialmente
        )
        self.reject_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text=self.lang.get('refresh', '↻ Aggiorna'),
            command=self._load_scrap_declarations
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _load_scrap_declarations(self):
        """Carica le dichiarazioni di scrap in attesa di validazione"""
        try:
            # Pulisci la treeview e le mappe
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.scrap_declarations = []
            self.labelcod_map = {}

            # Usa il metodo della classe Database
            declarations = self.db.fetch_scrap_declarations_pending()

            if not declarations:
                logger.info("Nessuna dichiarazione di scrap in attesa di validazione")
                return

            # Popola la treeview e crea la mappa labelcod
            for decl in declarations:
                # Memorizza la dichiarazione completa
                self.scrap_declarations.append(decl)

                # Crea mappa labelcod -> dichiarazione
                if hasattr(decl, 'labelcod') and decl.labelcod:
                    self.labelcod_map[decl.labelcod] = decl

                # Inserisci nella treeview (NASCONDI il labelcod reale)
                masked_code = '*' * len(decl.labelcod) if decl.labelcod else '***'

                self.tree.insert('', 'end', values=(
                    decl.ScrapDeclarationId,  # ID
                    getattr(decl, 'Date', '-'),  # Data
                    getattr(decl, 'OrderNumber', '-'),  # Order
                    getattr(decl, 'Produc', '-'),  # Product Code (nuovo campo)
                    getattr(decl, 'AreaName', '-'),  # Area
                    getattr(decl, 'Qty', 1),  # Quantity
                    getattr(decl, 'Defect', '-'),  # Reason
                    getattr(decl, 'DECLAREDBY', '-'),  # Declared By
                    'Pending'  # Status
                ))

            logger.info(f"Caricate {len(declarations)} dichiarazioni di scrap")

        except Exception as e:
            logger.error(f"Errore caricamento dichiarazioni scrap: {e}")
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                self.lang.get('error_loading_data', f'Errore caricamento dati: {e}'),
                parent=self
            )

    def _on_labelcode_entered(self, event=None):
        """Gestisce l'inserimento del labelcode e cerca la dichiarazione corrispondente"""
        entered_code = self.labelcode_var.get().strip()

        if not entered_code:
            self.validation_status_label.config(text='Inserire un label code', foreground='red')
            return

        try:
            # Cerca il labelcode nella mappa
            if entered_code in self.labelcod_map:
                declaration = self.labelcod_map[entered_code]
                self.selected_declaration = declaration.ScrapDeclarationId

                # Trova e seleziona la riga corrispondente nella treeview
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    if values and values[0] == declaration.ScrapDeclarationId:
                        self.tree.selection_set(item)
                        self.tree.focus(item)
                        break

                # Aggiorna i dettagli con tutti i campi disponibili
                self.detail_labels['order'].config(text=getattr(declaration, 'OrderNumber', '-'))
                self.detail_labels['product_code'].config(text=getattr(declaration, 'Produc', '-'))
                #self.detail_labels['product_name'].config(text=getattr(declaration, 'AreaName', '-'))
                self.detail_labels['area'].config(text=getattr(declaration, 'AreaName', '-'))
                self.detail_labels['quantity'].config(text=str(getattr(declaration, 'Qty', 1)))
                self.detail_labels['reason'].config(text=getattr(declaration, 'Defect', '-'))
                self.detail_labels['declared_by'].config(text=getattr(declaration, 'DECLAREDBY', '-'))
                self.detail_labels['date'].config(text=getattr(declaration, 'Date', '-'))

                # Abilita i pulsanti di azione
                self.approve_button.config(state='normal')
                self.reject_button.config(state='normal')

                self.validation_status_label.config(
                    text='Label code trovato - Validazione abilitata',
                    foreground='green'
                )

            else:
                self._clear_selection()
                self.validation_status_label.config(
                    text='Label code non trovato nelle dichiarazioni pendenti',
                    foreground='red'
                )

        except Exception as e:
            logger.error(f"Errore durante la validazione del label code: {e}")
            self.validation_status_label.config(text=f'Errore: {str(e)}', foreground='red')

    def _clear_selection(self):
        """Pulisce la selezione e i dettagli"""
        self.selected_declaration = None
        for label in self.detail_labels.values():
            label.config(text='-')

        # Disabilita i pulsanti di azione
        self.approve_button.config(state='disabled')
        self.reject_button.config(state='disabled')

        # Pulisce la selezione nella treeview
        self.tree.selection_remove(self.tree.selection())
        self.validation_status_label.config(text='')
        self.labelcode_var.set('')  # Pulisce anche il campo di input

    def _validate_declaration(self, status):
        """Valida o rifiuta la dichiarazione selezionata"""
        if not self.selected_declaration:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('select_declaration', 'Seleziona una dichiarazione'),
                parent=self
            )
            return

        # Conferma azione
        action_text = 'approvare' if status == 'Approved' else 'rifiutare'
        if not messagebox.askyesno(
                self.lang.get('confirm_title', 'Conferma'),
                self.lang.get('confirm_validation', f'Confermi di voler {action_text} questa dichiarazione?'),
                parent=self
        ):
            return

        # Esegui validazione
        success, error = self.db.validate_scrap_declaration(
            self.selected_declaration,
            status,
            None,
            self.user_name
        )

        if success:
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('validation_success', 'Dichiarazione validata con successo'),
                parent=self
            )
            self._load_scrap_declarations()  # Ricarica la lista
            self._clear_selection()
        else:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                self.lang.get('validation_error', f'Errore durante la validazione: {error}'),
                parent=self
            )

    def _on_tree_double_click(self, event):
        """Gestisce il doppio click su una riga per visualizzare l'immagine"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        item_values = item['values']

        if not item_values:
            return

        # Recupera l'ID della dichiarazione
        declaration_id = item_values[0]  # Prima colonna è l'ID

        try:
            # Cerca la dichiarazione completa
            selected_declaration = None
            for decl in self.scrap_declarations:
                if decl.ScrapDeclarationId == declaration_id:
                    selected_declaration = decl
                    break

            if not selected_declaration:
                messagebox.showinfo("Info", "Dichiarazione non trovata.", parent=self)
                return

            # Controlla se c'è un'immagine
            if not hasattr(selected_declaration, 'Picture') or not selected_declaration.Picture:
                messagebox.showinfo("Info", "Nessuna immagine disponibile per questa dichiarazione.", parent=self)
                return

            # Visualizza l'immagine
            self._show_image(selected_declaration.Picture, declaration_id)

        except Exception as e:
            logger.error(f"Errore visualizzazione immagine: {e}")
            messagebox.showerror("Errore", f"Impossibile visualizzare l'immagine: {e}", parent=self)

    def _show_image(self, image_data, declaration_id):
        """Visualizza l'immagine in una nuova finestra"""
        try:
            # Crea una nuova finestra
            image_window = tk.Toplevel(self)
            image_window.title(f"Immagine Dichiarazione #{declaration_id}")
            image_window.geometry("800x600")
            image_window.transient(self)
            image_window.grab_set()

            # Frame principale
            main_frame = ttk.Frame(image_window, padding=10)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Converti i dati binari in immagine
            from PIL import Image, ImageTk
            import io

            # Leggi i dati binari
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)

            # Ridimensiona se troppo grande
            max_size = (700, 500)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Converti per Tkinter
            photo = ImageTk.PhotoImage(image)

            # Label per l'immagine
            image_label = ttk.Label(main_frame, image=photo)
            image_label.image = photo  # Mantieni riferimento per evitare garbage collection
            image_label.pack(expand=True)

            # Pulsante chiudi
            ttk.Button(
                main_frame,
                text="Chiudi",
                command=image_window.destroy
            ).pack(pady=10)

        except Exception as e:
            logger.error(f"Errore elaborazione immagine: {e}")
            messagebox.showerror("Errore", f"Impossibile elaborare l'immagine: {e}", parent=self)


def open_scrap_validation(parent, db, lang, user_name):
    """Apre la finestra di validazione scarti."""
    window = ScrapValidationWindow(parent, db, lang, user_name)
    window.grab_set()