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
        self.scrap_declarations = []

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
            'id', 'date', 'order', 'product_code', 'product_name',
            'quantity', 'reason', 'declared_by', 'status'
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
        self.tree.heading('product_code', text=self.lang.get('product_code', 'Codice'))
        self.tree.heading('product_name', text=self.lang.get('product_name', 'Prodotto'))
        self.tree.heading('quantity', text=self.lang.get('quantity', 'Quantità'))
        self.tree.heading('reason', text=self.lang.get('reason', 'Causale'))
        self.tree.heading('declared_by', text=self.lang.get('declared_by', 'Dichiarato da'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))

        # Larghezze colonne
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('date', width=120, anchor='center')
        self.tree.column('order', width=100)
        self.tree.column('product_code', width=100)
        self.tree.column('product_name', width=200)
        self.tree.column('quantity', width=80, anchor='center')
        self.tree.column('reason', width=150)
        self.tree.column('declared_by', width=150)
        self.tree.column('status', width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_select_declaration)

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
            ('product', 'Prodotto'),
            ('quantity', 'Quantità Scartata'),
            ('reason', 'Causale'),
            ('declared_by', 'Dichiarato da'),
            ('date', 'Data Dichiarazione')#,
            #('notes', 'Note Operatore')
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

        # Frame note validatore (destra)
        #notes_frame = ttk.Frame(details_frame)
        #notes_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ttk.Label(
        #     notes_frame,
        #     text=self.lang.get('validator_notes', 'Note Validatore:'),
        #     font=('Arial', 9, 'bold')
        # ).pack(anchor='w')

        #self.notes_text = tk.Text(notes_frame, height=6, width=40, wrap=tk.WORD)
        #self.notes_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # ========== PULSANTI AZIONE ==========
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            buttons_frame,
            text=self.lang.get('approve', '✓ Approva'),
            command=lambda: self._validate_declaration('Approved'),
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text=self.lang.get('reject', '✗ Rifiuta'),
            command=lambda: self._validate_declaration('Rejected'),
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=5)

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

    def _setup_footer(self):
        """Configura logo e orologio nel footer."""
        footer_frame = ttk.Frame(self)
        footer_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        footer_frame.columnconfigure(1, weight=1)

        # Logo (se disponibile)
        try:
            from PIL import Image, ImageTk
            import os
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((80, 40), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(footer_frame, image=self.logo_photo)
                logo_label.grid(row=0, column=0, sticky=tk.W)
        except Exception as e:
            logger.warning(f"Impossibile caricare logo: {e}")

        # Orologio
        self.clock_label = ttk.Label(footer_frame, text='', font=('Arial', 10))
        self.clock_label.grid(row=0, column=2, sticky=tk.E)
        self._update_clock()

    def _update_clock(self):
        """Aggiorna l'orologio."""
        now = datetime.now().strftime('%H:%M:%S')
        self.clock_label.config(text=now)
        self.after(1000, self._update_clock)

    def _load_scrap_declarations(self):
        """Carica le dichiarazioni di scrap in attesa di validazione"""
        try:
            # Pulisci la treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Usa il metodo della classe Database
            declarations = self.db.fetch_scrap_declarations_pending()

            if not declarations:
                logger.info("Nessuna dichiarazione di scrap in attesa di validazione")
                return

            # Popola la treeview
            for decl in declarations:
                self.tree.insert('', 'end', values=(
                    decl.ScrapDeclarationId,  # ID
                    '',  # Data (non presente nella query)
                    '',  # Order (non presente)
                    decl.labelcod,  # Product Code (uso labelcod)
                    decl.AreaName,  # Product Name (uso AreaName)
                    '',  # Quantity (non presente)
                    decl.Defect,  # Reason
                    decl.DECLAREDBY,  # Declared By
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

    def _on_select_declaration(self, event):
        """Gestisce la selezione di una dichiarazione"""
        selection = self.tree.selection()
        if not selection:
            self._clear_selection()
            return

        item = self.tree.item(selection[0])
        values = item['values']

        if not values:
            return

        # Salva l'ID della dichiarazione selezionata
        self.selected_declaration = values[0]

        # Aggiorna i dettagli con i campi disponibili dalla query
        self.detail_labels['order'].config(text=values[2] if values[2] else '-')
        self.detail_labels['product'].config(text=f"{values[3]} - {values[4]}")  # labelcod - AreaName
        self.detail_labels['quantity'].config(text=values[5] if values[5] else '-')
        self.detail_labels['reason'].config(text=values[6])  # Defect
        self.detail_labels['declared_by'].config(text=values[7])  # DECLAREDBY
        self.detail_labels['date'].config(text=values[1] if values[1] else '-')

    def _clear_selection(self):
        """Pulisce la selezione e i dettagli"""
        self.selected_declaration = None
        for label in self.detail_labels.values():
            label.config(text='-')
        #self.notes_text.delete('1.0', tk.END)

    def _validate_declaration(self, status):
        """Valida o rifiuta la dichiarazione selezionata"""
        if not self.selected_declaration:
            messagebox.showwarning(
                self.lang.get('warning_title', 'Attenzione'),
                self.lang.get('select_declaration', 'Seleziona una dichiarazione'),
                parent=self
            )
            return

        # Ottieni le note del validatore (se necessario)
        #notes = self.notes_text.get('1.0', 'end-1c').strip()

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
            None,#notes,
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

    def _populate_listbox(self):
        """Popola la listbox con le dichiarazioni."""
        self.declarations_listbox.delete(0, tk.END)

        for decl in self.scrap_declarations:
            # Maschera il labelcode con asterischi
            masked_label = '*' * len(decl.labelcod) if decl.labelcod else '***'

            display_text = f"{decl.DECLAREDBY:15} | {masked_label:12} | {decl.AreaName:20} | {decl.DefectNameRO}"
            self.declarations_listbox.insert(tk.END, display_text)

    def _on_declaration_selected(self, event):
        """Gestisce la selezione di una dichiarazione dalla lista."""
        selection = self.declarations_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_declaration = self.scrap_declarations[index]

        # Pulisce il form
        self.labelcode_var.set('')
        self.validation_var.set('')
        self.save_button.config(state='disabled')

        # Aggiorna le info (senza mostrare il labelcode reale)
        self.declared_by_label.config(text=self.selected_declaration.DECLAREDBY)
        self.area_label.config(text=self.selected_declaration.AreaName)
        self.defect_label.config(text=self.selected_declaration.DefectNameRO)
        self.references_label.config(text=self.selected_declaration.Riferiments or '')

        # Focus sull'entry del labelcode
        self.labelcode_entry.focus()

    def _on_labelcode_entered(self, event=None):
        """Gestisce l'inserimento del labelcode."""
        entered_code = self.labelcode_var.get().strip()

        if not self.selected_declaration:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_declaration_first', 'Selezionare prima una dichiarazione dalla lista'),
                parent=self
            )
            return

        if entered_code != self.selected_declaration.labelcod:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('labelcode_mismatch',
                              'Il Label Code inserito non corrisponde alla dichiarazione selezionata'),
                parent=self
            )
            self.labelcode_var.set('')
            return

        # Label code corretto, abilita il salvataggio
        self.save_button.config(state='normal')

    def _save_validation(self):
        """Salva la validazione."""
        if not self.selected_declaration:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_declaration_selected', 'Nessuna dichiarazione selezionata'),
                parent=self
            )
            return

        validation_choice = self.validation_var.get()
        if not validation_choice:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_validation_choice', 'Selezionare una decisione di validazione'),
                parent=self
            )
            return

        try:
            if validation_choice == 'confirm':
                # Conferma scrap - esegui SP
                self.db.execute_stored_procedure(
                    '[Traceability_RS].dbo.[DeclareSCRAP]',
                    LabelCode=self.selected_declaration.labelcod,
                    IdDefect=self.selected_declaration.IDDefect,
                    riferiments=self.selected_declaration.Riferiments,
                    idAreaDefect=self.selected_declaration.IDArea
                )
                message = self.lang.get('scrap_confirmed', 'Scrap confermato con successo')

            else:  # reject
                # Non conferma scrap - aggiorna record
                update_query = """
                               UPDATE [Traceability_RS].[dbo].[ScarpDeclarations]
                               SET Refuzed = 1, RefuzedBy = ?
                               WHERE ScrapDeclarationId = ? \
                               """
                self.db.execute_update(
                    update_query,
                    self.user_name,
                    self.selected_declaration.ScrapDeclarationId
                )
                message = self.lang.get('scrap_rejected', 'Scrap rifiutato con successo')

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                message,
                parent=self
            )

            # Refresh della lista
            self._load_scrap_declarations()

            # Reset form
            self.selected_declaration = None
            self.labelcode_var.set('')
            self.validation_var.set('')
            self.save_button.config(state='disabled')
            self.declared_by_label.config(text='')
            self.area_label.config(text='')
            self.defect_label.config(text='')
            self.references_label.config(text='')

        except Exception as e:
            logger.error(f"Errore nel salvataggio della validazione: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error_saving_validation', 'Errore nel salvataggio')}: {str(e)}",
                parent=self
            )


def open_scrap_validation(parent, db, lang, user_name):
    """Apre la finestra di validazione scarti."""
    window = ScrapValidationWindow(parent, db, lang, user_name)
    window.grab_set()
