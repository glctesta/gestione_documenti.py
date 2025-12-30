"""
Modulo per la gestione delle Paste.
Gestisce:
- Configurazione paste (produttori, codici, datasheet)
- Upload e visualizzazione documenti
- CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
import os
import subprocess
from datetime import datetime
import logging

logger = logging.getLogger("TraceabilityRS")

class PasteConfigurationWindow(tk.Toplevel):
    """Finestra per la configurazione delle paste"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_id = user_id

        self.title(self.lang.get('paste_config_title', 'Configurazione Paste'))
        self.geometry('1000x850')
        self.transient(parent)

        self._current_pasta_id = None
        self._doc_data = None
        self._doc_filename = None
        
        self._build_ui()
        self._load_producers()
        self._load_pastas()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_id}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale diviso in due colonne
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form inserimento
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('paste_form', 'Dati Pasta'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Produttore
        ttk.Label(left_frame, text=self.lang.get('producer', 'Produttore') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.producer_var = tk.StringVar()
        self.producer_combo = ttk.Combobox(left_frame, textvariable=self.producer_var, 
                                          state='readonly', width=40)
        self.producer_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Codice Pasta
        ttk.Label(left_frame, text=self.lang.get('pasta_code', 'Codice Pasta') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.pasta_code_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.pasta_code_var, width=40).grid(
            row=1, column=1, padx=5, pady=5, sticky='ew')

        # Validità (mesi)
        ttk.Label(left_frame, text=self.lang.get('valability_months', 'Validità (mesi)') + ' *').grid(
            row=2, column=0, sticky='w', padx=5, pady=5)
        self.valability_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.valability_var, width=40).grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')

        # Temperatura Minima
        ttk.Label(left_frame, text=self.lang.get('low_temperature', 'Temperatura Minima (°C)') + ' *').grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.low_temp_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.low_temp_var, width=40).grid(
            row=3, column=1, padx=5, pady=5, sticky='ew')

        # Temperatura Massima
        ttk.Label(left_frame, text=self.lang.get('high_temperature', 'Temperatura Massima (°C)') + ' *').grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        self.high_temp_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.high_temp_var, width=40).grid(
            row=4, column=1, padx=5, pady=5, sticky='ew')

        # Documento allegato
        doc_frame = ttk.Frame(left_frame)
        doc_frame.grid(row=5, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        ttk.Label(doc_frame, text=self.lang.get('datasheet', 'Scheda Tecnica')).pack(side='left')
        ttk.Button(doc_frame, text=self.lang.get('btn_upload', 'Carica'), 
                  command=self._upload_doc).pack(side='left', padx=5)
        ttk.Button(doc_frame, text=self.lang.get('btn_view', 'Visualizza'), 
                  command=self._view_doc).pack(side='left', padx=5)
        self.doc_label = ttk.Label(doc_frame, text='', foreground='blue')
        self.doc_label.pack(side='left', padx=5)

        # Pulsanti azione
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'), 
                  command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'), 
                  command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'), 
                  command=self._on_delete).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista paste configurate
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('configured_pastas', 'Paste Configurate'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Treeview
        columns = ('id', 'pasta_code', 'producer', 'created_by', 'created_at', 'has_doc')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        self.tree.heading('id', text='ID')
        self.tree.heading('pasta_code', text=self.lang.get('pasta_code', 'Codice'))
        self.tree.heading('producer', text=self.lang.get('producer', 'Produttore'))
        self.tree.heading('created_by', text=self.lang.get('created_by', 'Creato da'))
        self.tree.heading('created_at', text=self.lang.get('created_at', 'Data Creazione'))
        self.tree.heading('has_doc', text=self.lang.get('doc', 'Doc'))

        self.tree.column('id', width=50)
        self.tree.column('pasta_code', width=120)
        self.tree.column('producer', width=150)
        self.tree.column('created_by', width=100)
        self.tree.column('created_at', width=120)
        self.tree.column('has_doc', width=50)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-Button-1>', self._on_double_click)

    def _load_producers(self):
        """Carica la lista produttori nel combo"""
        producers = self.db.fetch_paste_producers()
        self.producers_dict = {p.SiteName: p.IDSite for p in producers}
        self.producer_combo['values'] = list(self.producers_dict.keys())

    def _load_pastas(self):
        """Carica le paste configurate"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        pastas = self.db.fetch_all_pastas()
        for pasta in pastas:
            created_at = pasta.CreatedAt.strftime('%d/%m/%Y %H:%M') if pasta.CreatedAt else ''
            self.tree.insert('', 'end', values=(
                pasta.Pastaid,
                pasta.PastaCode,
                pasta.SiteName or '',
                pasta.CreatedBy or '',
                created_at,
                '✓' if pasta.PastaDataSheet else ''
            ))

    def _upload_doc(self):
        """Carica un documento"""
        file_path = filedialog.askopenfilename(
            title=self.lang.get('select_document', 'Seleziona Documento'),
            filetypes=[
                ('PDF', '*.pdf'),
                ('Word', '*.doc;*.docx'),
                ('Excel', '*.xls;*.xlsx'),
                ('Images', '*.jpg;*.jpeg;*.png'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self._doc_data = f.read()
                self._doc_filename = os.path.basename(file_path)
                self.doc_label.config(text=self._doc_filename)
                logger.info(f"Documento caricato: {self._doc_filename}")
            except Exception as e:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                   f"{self.lang.get('upload_error', 'Errore caricamento')}: {str(e)}")
                logger.error(f"Errore upload documento: {e}")

    def _view_doc(self):
        """Visualizza il documento corrente"""
        if self._doc_data:
            self._open_document(self._doc_data, self._doc_filename)
        else:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('no_doc', 'Nessun documento caricato'))

    def _open_document(self, doc_data, filename=None):
        """Apre un documento binario"""
        try:
            # Determina l'estensione dal filename se disponibile
            if filename:
                _, ext = os.path.splitext(filename)
            else:
                ext = '.pdf'  # Default

            # Crea un file temporaneo
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(doc_data)
                tmp_path = tmp_file.name

            # Apre il file con l'applicazione predefinita
            if os.name == 'nt':  # Windows
                os.startfile(tmp_path)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.call(['xdg-open', tmp_path])
            
            logger.info(f"Documento aperto: {tmp_path}")
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                               f"{self.lang.get('open_error', 'Errore apertura documento')}: {str(e)}")
            logger.error(f"Errore apertura documento: {e}")

    def _on_select(self, event):
        """Gestisce la selezione di una riga"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_pasta_id = values[0]

        # Carica i dettagli della pasta
        pasta = self.db.fetch_pasta_by_id(self._current_pasta_id)
        if pasta:
            # Trova il produttore nel combo
            if pasta.SiteName in self.producers_dict:
                self.producer_var.set(pasta.SiteName)
            
            self.pasta_code_var.set(pasta.PastaCode or '')
            
            # Carica la configurazione temperatura
            config = self.db.fetch_pasta_config(self._current_pasta_id)
            if config:
                self.valability_var.set(str(config.Valability) if config.Valability else '')
                self.low_temp_var.set(str(config.LowTemperature) if config.LowTemperature else '')
                self.high_temp_var.set(str(config.HighTemperature) if config.HighTemperature else '')
            else:
                self.valability_var.set('')
                self.low_temp_var.set('')
                self.high_temp_var.set('')
            
            # Carica il documento se presente
            self._doc_data = pasta.PastaDataSheet
            if pasta.PastaDataSheet:
                self.doc_label.config(text=self.lang.get('doc_present', 'Documento presente'))
                self._doc_filename = f"{pasta.PastaCode}_datasheet.pdf"
            else:
                self.doc_label.config(text='')
                self._doc_filename = None

    def _on_double_click(self, event):
        """Apre il documento se presente"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        pasta_id = item['values'][0]

        pasta = self.db.fetch_pasta_by_id(pasta_id)
        if pasta and pasta.PastaDataSheet:
            self._open_document(pasta.PastaDataSheet, f"{pasta.PastaCode}_datasheet.pdf")

    def _on_new(self):
        """Pulisce il form per nuovo inserimento"""
        self._current_pasta_id = None
        self.producer_var.set('')
        self.pasta_code_var.set('')
        self.valability_var.set('')
        self.low_temp_var.set('')
        self.high_temp_var.set('')
        self._doc_data = None
        self._doc_filename = None
        self.doc_label.config(text='')

    def _on_save(self):
        """Salva o aggiorna una pasta"""
        # Validazione
        if not self.producer_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_producer', 'Selezionare un produttore'))
            return

        if not self.pasta_code_var.get().strip():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_pasta_code', 'Inserire il codice pasta'))
            return

        # Validazione campi temperatura
        try:
            valability = int(self.valability_var.get().strip()) if self.valability_var.get().strip() else None
            if valability is None or valability <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_valid_valability', 'Inserire una validità valida (mesi)'))
            return

        try:
            low_temp = float(self.low_temp_var.get().strip()) if self.low_temp_var.get().strip() else None
            if low_temp is None:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_valid_low_temp', 'Inserire una temperatura minima valida'))
            return

        try:
            high_temp = float(self.high_temp_var.get().strip()) if self.high_temp_var.get().strip() else None
            if high_temp is None:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_valid_high_temp', 'Inserire una temperatura massima valida'))
            return

        if low_temp >= high_temp:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('temp_range_error', 'La temperatura minima deve essere inferiore alla massima'))
            return

        producer_id = self.producers_dict[self.producer_var.get()]
        pasta_code = self.pasta_code_var.get().strip()

        if self._current_pasta_id:
            # Update pasta
            success, message = self.db.update_pasta(
                self._current_pasta_id,
                producer_id,
                pasta_code,
                self._doc_data
            )
            if success:
                # Update configurazione
                config_success, config_message = self.db.update_pasta_config(
                    self._current_pasta_id, valability, low_temp, high_temp)
                if not config_success:
                    messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                         f"Pasta aggiornata ma errore configurazione: {config_message}")
        else:
            # Insert pasta
            if not self._doc_data:
                if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                                          self.lang.get('no_doc_confirm', 
                                                       'Nessun documento caricato. Continuare?')):
                    return
            
            success, message = self.db.insert_pasta(
                producer_id,
                pasta_code,
                self._doc_data,
                self.user_id
            )
            
            if success:
                # Recupera l'ID della pasta appena inserita
                pastas = self.db.fetch_all_pastas()
                new_pasta = None
                for p in pastas:
                    if p.PastaCode == pasta_code and p.ProducerId == producer_id:
                        new_pasta = p
                        break
                
                if new_pasta:
                    # Insert configurazione
                    config_success, config_message = self.db.insert_pasta_config(
                        new_pasta.Pastaid, valability, low_temp, high_temp)
                    if not config_success:
                        messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                             f"Pasta creata ma errore configurazione: {config_message}")

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_pastas()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'), message)

    def _on_delete(self):
        """Elimina una pasta (soft delete)"""
        if not self._current_pasta_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_pasta', 'Selezionare una pasta da eliminare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_delete_pasta', 'Eliminare la pasta selezionata?')):
            success, message = self.db.delete_pasta(self._current_pasta_id)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'), message)
                self._load_pastas()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'), message)


def open_paste_configuration(parent, db_handler, lang_manager, user_id):
    """Funzione helper per aprire la finestra di configurazione paste"""
    PasteConfigurationWindow(parent, db_handler, lang_manager, user_id)


class PasteLocationsWindow(tk.Toplevel):
    """Finestra per la gestione delle locazioni frigoriferi paste"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_id = user_id

        self.title(self.lang.get('paste_locations_title', 'Gestione Locazioni Frigoriferi'))
        self.geometry('800x500')
        self.transient(parent)

        self._current_location_id = None
        self._build_ui()
        self._load_locations()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_id}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('location_form', 'Dati Locazione'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Nome Locazione
        ttk.Label(left_frame, text=self.lang.get('location_name', 'Nome Locazione') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.name_var, width=40).grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')

        # Pulsanti
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                   command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                   command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                   command=self._on_delete).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista locazioni
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('locations_list', 'Locazioni'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # TreeView
        columns = ('id', 'name')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=18)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('location_name', 'Nome Locazione'))

        self.tree.column('id', width=50)
        self.tree.column('name', width=400)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_locations(self):
        """Carica le locazioni"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = """
                SELECT PastaStoreFrigiderLocationId, PastaStoreFrigiderLocationName
                FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                ORDER BY PastaStoreFrigiderLocationName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=(
                    row.PastaStoreFrigiderLocationId,
                    row.PastaStoreFrigiderLocationName
                ))
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento locazioni: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento locazioni: {str(e)}"
            )

    def _on_select(self, event):
        """Gestisce la selezione"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_location_id = values[0]
        self.name_var.set(values[1])

    def _on_new(self):
        """Pulisce il form"""
        self._current_location_id = None
        self.name_var.set('')

    def _on_save(self):
        """Salva o aggiorna"""
        # Validazione
        if not self.name_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_location_name', 'Inserire il nome della locazione')
            )
            return

        name = self.name_var.get().strip()

        try:
            if self._current_location_id:
                # Update
                query = """
                    UPDATE [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                    SET PastaStoreFrigiderLocationName = ?
                    WHERE PastaStoreFrigiderLocationId = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (name, self._current_location_id))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('location_updated', 'Locazione aggiornata con successo')
            else:
                # Insert
                query = """
                    INSERT INTO [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                    (PastaStoreFrigiderLocationName)
                    VALUES (?)
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (name,))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('location_saved', 'Locazione salvata con successo')

            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_locations()
            self._on_new()

        except Exception as e:
            logger.error(f"Errore salvataggio locazione: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il salvataggio: {str(e)}"
            )

    def _on_delete(self):
        """Elimina"""
        if not self._current_location_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_location', 'Selezionare una locazione da eliminare')
            )
            return

        if messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_location', 'Eliminare la locazione selezionata?')
        ):
            try:
                query = """
                    DELETE FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                    WHERE PastaStoreFrigiderLocationId = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (self._current_location_id,))
                self.db.conn.commit()
                cursor.close()

                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('location_deleted', 'Locazione eliminata con successo')
                )
                self._load_locations()
                self._on_new()

            except Exception as e:
                logger.error(f"Errore eliminazione locazione: {e}")
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"Errore durante l'eliminazione: {str(e)}"
                )


def open_paste_locations(parent, db_handler, lang_manager, user_id):
    """Funzione helper per aprire la finestra gestione locazioni"""
    PasteLocationsWindow(parent, db_handler, lang_manager, user_id)



class PasteRefrigeratorsWindow(tk.Toplevel):
    """Finestra per la gestione dei frigoriferi paste"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_id = user_id

        self.title(self.lang.get('refrigerators_title', 'Gestione Frigoriferi Paste'))
        self.geometry('900x550')
        self.transient(parent)

        self._current_refrigerator_id = None
        self._build_ui()
        self._load_refrigerators()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_id}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('refrigerator_form', 'Dati Frigorifero'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Nome Frigorifero
        ttk.Label(left_frame, text=self.lang.get('refrigerator_name', 'Nome Frigorifero') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.name_var, width=40).grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')

        # Ubicazione
        ttk.Label(left_frame, text=self.lang.get('location', 'Ubicazione') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(left_frame, textvariable=self.location_var,
                                          state='readonly', width=37)
        self.location_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Carica le locazioni dal database
        self._load_locations_combo()

        # Connesso
        self.is_connected_var = tk.BooleanVar()
        ttk.Checkbutton(left_frame, text=self.lang.get('is_connected', 'Connesso'),
                       variable=self.is_connected_var).grid(
            row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        # Pulsanti
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._on_delete).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista frigoriferi
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('refrigerators_list', 'Frigoriferi'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # TreeView
        columns = ('id', 'name', 'location', 'connected')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=18)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('refrigerator_name', 'Nome'))
        self.tree.heading('location', text=self.lang.get('location', 'Ubicazione'))
        self.tree.heading('connected', text=self.lang.get('connected', 'Connesso'))

        self.tree.column('id', width=50)
        self.tree.column('name', width=200)
        self.tree.column('location', width=120)
        self.tree.column('connected', width=80)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_locations_combo(self):
        """Carica le locazioni nel combo"""
        try:
            query = """
                SELECT PastaStoreFrigiderLocationName
                FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                ORDER BY PastaStoreFrigiderLocationName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            locations = [row.PastaStoreFrigiderLocationName for row in cursor.fetchall()]
            self.location_combo['values'] = locations
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento locazioni: {e}")

    def _load_refrigerators(self):
        """Carica i frigoriferi"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        refrigerators = self.db.fetch_all_refrigerators()
        for ref in refrigerators:
            connected_text = '✓' if ref.IsConnected else ''
            self.tree.insert('', 'end', values=(
                ref.PastaStoreFrigiderId,
                ref.PastaStoreFrigiderName,
                ref.PastaStoreFrigiderLocation,
                connected_text
            ))

    def _on_select(self, event):
        """Gestisce la selezione"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_refrigerator_id = values[0]
        self.name_var.set(values[1])
        self.location_var.set(values[2])
        self.is_connected_var.set(values[3] == '✓')

    def _on_new(self):
        """Pulisce il form"""
        self._current_refrigerator_id = None
        self.name_var.set('')
        self.location_var.set('')
        self.is_connected_var.set(False)

    def _on_save(self):
        """Salva o aggiorna"""
        # Validazione
        if not self.name_var.get().strip():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_refrigerator_name', 'Inserire il nome del frigorifero'))
            return

        if not self.location_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_location', 'Selezionare l\'ubicazione'))
            return

        name = self.name_var.get().strip()
        location = self.location_var.get()
        is_connected = self.is_connected_var.get()

        if self._current_refrigerator_id:
            # Update
            success, message = self.db.update_refrigerator(
                self._current_refrigerator_id, name, location, is_connected)
        else:
            # Insert
            success, message = self.db.insert_refrigerator(name, location, is_connected)

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_refrigerators()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'), message)

    def _on_delete(self):
        """Elimina"""
        if not self._current_refrigerator_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_refrigerator', 'Selezionare un frigorifero da eliminare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_delete_refrigerator', 'Eliminare il frigorifero selezionato?')):
            success, message = self.db.delete_refrigerator(self._current_refrigerator_id)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'), message)
                self._load_refrigerators()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'), message)


def open_paste_refrigerators(parent, db_handler, lang_manager, user_id):
    """Funzione helper per aprire la finestra gestione frigoriferi"""
    PasteRefrigeratorsWindow(parent, db_handler, lang_manager, user_id)


class PasteReceptionWindow(tk.Toplevel):
    """Finestra per il ricevimento paste"""

    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name

        self.title(self.lang.get('paste_reception_title', 'Ricevimento Paste'))
        self.geometry('1200x650')
        self.transient(parent)

        self._current_log_id = None
        self._doc_data = None
        self._doc_filename = None
        self._current_label_id = None  # Track generated label ID
        self._label_used = False  # Track if label was used

        # Bind window close event
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_pastas()
        self._load_logs()
        self._load_printer_config()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('reception_form', 'Ricevimento'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Pasta
        ttk.Label(left_frame, text=self.lang.get('pasta', 'Pasta') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.pasta_var = tk.StringVar()
        self.pasta_combo = ttk.Combobox(left_frame, textvariable=self.pasta_var,
                                        state='readonly', width=37)
        self.pasta_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.pasta_combo.bind('<<ComboboxSelected>>', self._on_pasta_selected)

        # Locazione Frigorifero (solo warehouse)
        ttk.Label(left_frame, text=self.lang.get('refrigerator_location', 'Locazione Frigorifero') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(left_frame, textvariable=self.location_var,
                                           state='readonly', width=37)
        self.location_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self._load_warehouse_locations()

        # Codice Etichetta (auto-generato)
        ttk.Label(left_frame, text=self.lang.get('label_code', 'Codice Etichetta')).grid(
            row=2, column=0, sticky='w', padx=5, pady=5)
        self.label_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.label_var, state='readonly', width=40).grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')

        # Documento
        doc_frame = ttk.Frame(left_frame)
        doc_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=10)
        ttk.Label(doc_frame, text=self.lang.get('incoming_document', 'Documento Ricevimento')).pack(side='left')
        ttk.Button(doc_frame, text=self.lang.get('btn_upload', 'Carica'),
                  command=self._upload_doc).pack(side='left', padx=5)
        ttk.Button(doc_frame, text=self.lang.get('btn_view', 'Visualizza'),
                  command=self._view_doc).pack(side='left', padx=5)
        ttk.Button(doc_frame, text=self.lang.get('btn_delete_doc', 'Elimina Doc'),
                  command=self._delete_doc).pack(side='left', padx=5)
        self.doc_label = ttk.Label(doc_frame, text='', foreground='blue')
        self.doc_label.pack(side='left', padx=5)

        # Pulsanti
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_receive', 'Ricevi'),
                  command=self._on_receive).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_print_label', 'Stampa Etichetta'),
                  command=self._on_print_label).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete_reception', 'Elimina Ricevimento'),
                  command=self._on_delete_reception).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Log ricevimenti
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('reception_logs', 'Log Ricevimenti'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # TreeView
        columns = ('id', 'pasta', 'producer', 'label', 'date', 'user', 'doc')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        self.tree.heading('id', text='ID')
        self.tree.heading('pasta', text=self.lang.get('pasta_code', 'Codice'))
        self.tree.heading('producer', text=self.lang.get('producer', 'Produttore'))
        self.tree.heading('label', text=self.lang.get('label', 'Etichetta'))
        self.tree.heading('date', text=self.lang.get('reception_date', 'Data'))
        self.tree.heading('user', text=self.lang.get('user', 'Utente'))
        self.tree.heading('doc', text=self.lang.get('doc', 'Doc'))

        self.tree.column('id', width=40)
        self.tree.column('pasta', width=100)
        self.tree.column('producer', width=120)
        self.tree.column('label', width=130)
        self.tree.column('date', width=130)
        self.tree.column('user', width=80)
        self.tree.column('doc', width=40)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-Button-1>', self._on_double_click)

    def _load_pastas(self):
        """Carica le paste nel combo"""
        pastas = self.db.fetch_all_pastas_for_reception()
        self.pastas_dict = {f"{p.PastaCode} ({p.ProducerName})": p.Pastaid for p in pastas}
        self.pasta_combo['values'] = list(self.pastas_dict.keys())

    def _load_warehouse_locations(self):
        """Carica solo le locazioni warehouse nel combo"""
        try:
            query = """
                SELECT PastaStoreFrigiderLocationId, PastaStoreFrigiderLocationName
                FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                WHERE LOWER(PastaStoreFrigiderLocationName) LIKE '%warehouse%'
                ORDER BY PastaStoreFrigiderLocationName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            self.locations_dict = {}
            for row in cursor.fetchall():
                self.locations_dict[row.PastaStoreFrigiderLocationName] = row.PastaStoreFrigiderLocationId
            
            self.location_combo['values'] = list(self.locations_dict.keys())
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento locazioni warehouse: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento locazioni: {str(e)}"
            )

    def _load_logs(self):
        """Carica i log di ricevimento"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        logs = self.db.fetch_pasta_logs(100)
        for log in logs:
            date_str = log.GetIn.strftime('%Y-%m-%d %H:%M') if log.GetIn else ''
            self.tree.insert('', 'end', values=(
                log.PastaLogId,
                log.PastaCode,
                log.ProducerName or '',
                log.LabelCode,
                date_str,
                log.User,
                '✓' if log.HasDoc else ''
            ))

    def _on_select(self, event):
        """Gestisce la selezione"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_log_id = values[0]
        # Carica il documento se presente
        doc_data = self.db.fetch_pasta_log_document(self._current_log_id)
        if doc_data:
            self._doc_data = doc_data
            self.doc_label.config(text=self.lang.get('doc_present', 'Documento presente'))
            self._doc_filename = f"reception_{values[0]}.pdf"
        else:
            self._doc_data = None
            self.doc_label.config(text='')
            self._doc_filename = None

    def _on_double_click(self, event):
        """Visualizza il documento al doppio click"""
        if self._doc_data:
            self._open_document(self._doc_data, self._doc_filename)

    def _on_pasta_selected(self, event=None):
        """Genera automaticamente un nuovo codice etichetta quando si seleziona una pasta"""
        # Cleanup previous unused label
        self._cleanup_unused_label()
        
        # Reset form
        self._doc_data = None
        self._doc_filename = None
        self.doc_label.config(text='')
        self._label_used = False

        # Genera nuovo codice etichetta
        label_code = self.db.generate_label_code()
        if label_code:
            # Inserisci subito il codice nel DB
            label_id = self.db.insert_label_code(label_code)
            if label_id:
                self._current_label_id = label_id
                self.label_var.set(label_code)
                logger.info(f"Label generato automaticamente: {label_code}, ID: {label_id}")
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                   self.lang.get('label_insert_error', 'Errore inserimento codice etichetta'))
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                               self.lang.get('label_generation_error', 'Errore generazione codice etichetta'))

    def _cleanup_unused_label(self):
        """Elimina il codice etichetta se non è stato utilizzato"""
        if self._current_label_id and not self._label_used:
            self.db.delete_label_code(self._current_label_id)
            logger.info(f"Label non utilizzato eliminato: ID={self._current_label_id}")
            self._current_label_id = None

    def _on_close(self):
        """Gestisce la chiusura della finestra"""
        self._cleanup_unused_label()
        self.destroy()

    def _upload_doc(self):
        """Carica un documento"""
        file_path = filedialog.askopenfilename(
            title=self.lang.get('select_document', 'Seleziona Documento'),
            filetypes=[
                ('PDF', '*.pdf'),
                ('Images', '*.jpg;*.jpeg;*.png'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self._doc_data = f.read()
                self._doc_filename = os.path.basename(file_path)
                self.doc_label.config(text=self._doc_filename)
                logger.info(f"Documento caricato: {self._doc_filename}")

                # Se stiamo modificando un log esistente, aggiorna subito
                if self._current_log_id:
                    success, message = self.db.update_pasta_log_document(self._current_log_id, self._doc_data)
                    if success:
                        messagebox.showinfo(self.lang.get('success', 'Successo'), message)
                        self._load_logs()
                    else:
                        messagebox.showerror(self.lang.get('error', 'Errore'), message)

            except Exception as e:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                   f"{self.lang.get('upload_error', 'Errore caricamento')}: {str(e)}")
                logger.error(f"Errore upload documento: {e}")

    def _view_doc(self):
        """Visualizza il documento"""
        if self._doc_data:
            self._open_document(self._doc_data, self._doc_filename)
        else:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('no_doc', 'Nessun documento caricato'))

    def _delete_doc(self):
        """Elimina il documento"""
        if not self._current_log_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_log', 'Selezionare un log'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_delete_doc', 'Eliminare il documento?')):
            success, message = self.db.update_pasta_log_document(self._current_log_id, None)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'), message)
                self._doc_data = None
                self._doc_filename = None
                self.doc_label.config(text='')
                self._load_logs()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'), message)

    def _open_document(self, doc_data, filename=None):
        """Apre un documento binario"""
        try:
            if filename:
                _, ext = os.path.splitext(filename)
            else:
                ext = '.pdf'

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(doc_data)
                tmp_path = tmp_file.name

            if os.name == 'nt':
                os.startfile(tmp_path)
            elif os.name == 'posix':
                subprocess.call(['xdg-open', tmp_path])

            logger.info(f"Documento aperto: {tmp_path}")
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                               f"{self.lang.get('open_error', 'Errore apertura documento')}: {str(e)}")
            logger.error(f"Errore apertura documento: {e}")

    def _on_delete_reception(self):
        """Elimina un ricevimento (solo se non trasferito)"""
        if not self._current_log_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_reception', 'Selezionare un ricevimento da eliminare')
            )
            return

        try:
            # Verifica se la pasta è stata trasferita
            query = """
                SELECT COUNT(*) as TransferCount
                FROM [Traceability_RS].[pst].[PastaInUseLogs]
                WHERE PastaLogid = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self._current_log_id,))
            row = cursor.fetchone()
            transfer_count = row.TransferCount if row else 0
            cursor.close()

            if transfer_count > 0:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('cannot_delete_transferred', 
                                 'Impossibile eliminare: la pasta è già stata trasferita')
                )
                return

            # Conferma eliminazione
            if not messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('confirm_delete_reception', 'Eliminare il ricevimento selezionato?')
            ):
                return

            # Elimina il ricevimento
            delete_query = """
                DELETE FROM [Traceability_RS].[pst].[PastaLogs]
                WHERE PastaLogId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(delete_query, (self._current_log_id,))
            self.db.conn.commit()
            cursor.close()

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('reception_deleted', 'Ricevimento eliminato con successo')
            )
            
            # Reset e ricarica
            self._current_log_id = None
            self._doc_data = None
            self._doc_filename = None
            self.doc_label.config(text='')
            self._load_logs()

        except Exception as e:
            logger.error(f"Errore eliminazione ricevimento: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'eliminazione: {str(e)}"
            )

    def _load_printer_config(self):
        """Carica la configurazione della stampante"""
        try:
            query = """
                SELECT TOP 1 PrinterIP, PrinterPort
                FROM [Traceability_RS].[pst].[PrinterConfig]
                WHERE IsActive = 1
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                self.printer_ip = row.PrinterIP
                self.printer_port = row.PrinterPort
                logger.info(f"Configurazione stampante caricata: {self.printer_ip}:{self.printer_port}")
            else:
                self.printer_ip = None
                self.printer_port = None
                logger.warning("Nessuna configurazione stampante trovata")
        except Exception as e:
            logger.error(f"Errore caricamento configurazione stampante: {e}")
            self.printer_ip = None
            self.printer_port = None

    def _on_receive(self):
        """Registra il ricevimento della pasta"""
        # Validazione
        if not self.pasta_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_pasta', 'Selezionare una pasta')
            )
            return

        if not self.location_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_location', 'Selezionare una locazione')
            )
            return

        if not self.label_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_label_code', 'Nessun codice etichetta generato')
            )
            return

        try:
            # Ottieni l'ID della pasta selezionata
            pasta_id = self.pastas_dict[self.pasta_var.get()]
            
            # Ottieni l'ID della locazione selezionata
            location_id = self.locations_dict[self.location_var.get()]
            
            # Inserisci il log di ricevimento
            query = """
                INSERT INTO [Traceability_RS].[pst].[PastaLogs]
                (Pastaid, LabelCode, GetIn, [User], PastaStoreFrigiderLocationId, IncomingDocument)
                VALUES (?, ?, GETDATE(), ?, ?, ?)
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (
                pasta_id,
                self.label_var.get(),
                self.user_name,
                location_id,
                self._doc_data if self._doc_data else None
            ))
            self.db.conn.commit()
            
            # Ottieni l'ID del log appena inserito
            cursor.execute("SELECT @@IDENTITY")
            log_id = cursor.fetchone()[0]
            cursor.close()
            
            # Marca l'etichetta come utilizzata
            self._label_used = True
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('reception_saved', 'Ricevimento registrato con successo')
            )
            
            logger.info(f"Ricevimento registrato: PastaLogId={log_id}, Label={self.label_var.get()}")
            
            # Reset form e ricarica
            self.pasta_var.set('')
            self.location_var.set('')
            self.label_var.set('')
            self._doc_data = None
            self._doc_filename = None
            self.doc_label.config(text='')
            self._current_label_id = None
            self._label_used = False
            self._load_logs()
            
        except Exception as e:
            logger.error(f"Errore registrazione ricevimento: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il ricevimento: {str(e)}"
            )

    def _on_print_label(self):
        """Gestisce la stampa dell'etichetta"""
        if not self._current_log_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_log', 'Selezionare un log da stampare')
            )
            return

        try:
            # Recupera i dati del log per la stampa
            query = """
                SELECT pl.LabelCode, p.PastaCode, pr.ProducerName, pl.GetIn
                FROM [Traceability_RS].[pst].[PastaLogs] pl
                INNER JOIN [Traceability_RS].[pst].[Pastas] p ON pl.Pastaid = p.Pastaid
                LEFT JOIN [Traceability_RS].[pst].[Producers] pr ON p.ProducerId = pr.ProducerId
                WHERE pl.PastaLogId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self._current_log_id,))
            row = cursor.fetchone()
            cursor.close()

            if not row:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('log_not_found', 'Log non trovato')
                )
                return

            label_data = {
                'label_code': row.LabelCode,
                'pasta_code': row.PastaCode,
                'producer': row.ProducerName or '',
                'date': row.GetIn.strftime('%Y-%m-%d %H:%M') if row.GetIn else ''
            }

            # Genera ZPL
            zpl_content = self._generate_zpl_label(label_data)
            
            # Stampa
            if self.printer_ip and self.printer_port:
                self._print_to_zebra(zpl_content)
                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('label_sent', 'Etichetta inviata alla stampante')
                )
                logger.info(f"Etichetta stampata: {label_data['label_code']}")
            else:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('printer_not_configured', 'Stampante non configurata')
                )

        except Exception as e:
            logger.error(f"Errore stampa etichetta: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la stampa: {str(e)}"
            )

    def _generate_zpl_label(self, label_data):
        """Genera il contenuto ZPL per l'etichetta"""
        zpl_template = f"""^XA
^FO50,30^A0N,30,30^FDPasta: {label_data['pasta_name']}^FS
^FO50,70^A0N,25,25^FDRicevuto: {label_data['reception_date']}^FS
^FO50,110^A0N,25,25^FDCodice: {label_data['label_code']}^FS
^FO50,150^A0N,25,25^FDDa: {label_data['user_name']}^FS
^FO50,190^A0N,30,30^FDScadenza: {label_data['expiry_date']}^FS
^FO50,230^A0N,25,25^FDTemp: {label_data['low_temp']}C - {label_data['high_temp']}C^FS
^FO50,270^GB700,3,3^FS
^FO50,280^A0N,20,20^FDPASTRATI IN FRIGIDER^FS
^FO600,30^BQN,2,6^FDQA,{label_data['label_code']}^FS
^XZ"""
        return zpl

    def _print_to_zebra(self, zpl_content):
        """Invia il contenuto ZPL alla stampante Zebra via socket"""
        import socket
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.printer_ip, int(self.printer_port)))
            sock.send(zpl_content.encode('utf-8'))
            sock.close()
            logger.info(f"ZPL inviato a {self.printer_ip}:{self.printer_port}")
        except Exception as e:
            logger.error(f"Errore invio ZPL: {e}")
            raise


class ProducersWindow(tk.Toplevel):
    """Finestra per la gestione dei produttori di paste"""
    
    def __init__(self, parent, db_handler, lang_manager):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        
        self.title(self.lang.get('producers_management', 'Gestione Produttori'))
        self.geometry("800x600")
        self.transient(parent)
        
        self._selected_id = None
        self._build_ui()
        self._load_producers()
    
    def _build_ui(self):
        """Costruisce l'interfaccia"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Frame superiore: Form
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('producer_data', 'Dati Produttore'), padding="10")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Producer Name
        ttk.Label(form_frame, text=self.lang.get('producer_name', 'Nome Produttore') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=40).grid(
            row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Country
        ttk.Label(form_frame, text=self.lang.get('country', 'Paese')).grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.country_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.country_var, width=40).grid(
            row=1, column=1, sticky='ew', padx=5, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Pulsanti azioni
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self.lang.get('btn_add', 'Aggiungi'),
                  command=self._on_add).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_update', 'Modifica'),
                  command=self._on_update).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._on_delete).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_clear', 'Pulisci'),
                  command=self._clear_form).pack(side='left', padx=2)
        
        # Frame inferiore: TreeView
        tree_frame = ttk.LabelFrame(main_frame, text=self.lang.get('producers_list', 'Elenco Produttori'), padding="10")
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # TreeView
        columns = ('id', 'name', 'country')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('producer_name', 'Nome Produttore'))
        self.tree.heading('country', text=self.lang.get('country', 'Paese'))
        
        self.tree.column('id', width=50)
        self.tree.column('name', width=400)
        self.tree.column('country', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selezione
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
    
    def _load_producers(self):
        """Carica i produttori dal database"""
        try:
            self.tree.delete(*self.tree.get_children())
            
            query = """
                SELECT ProducerId, Producers, Country
                FROM [Traceability_RS].[dbo].[Producers]
                ORDER BY Producers
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=(
                    row.ProducerId,
                    row.Producers or '',
                    row.Country or ''
                ))
            
            cursor.close()
            logger.info("Produttori caricati")
            
        except Exception as e:
            logger.error(f"Errore caricamento produttori: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il caricamento: {str(e)}"
            )
    
    def _on_select(self, event):
        """Gestisce la selezione di un produttore"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        self._selected_id = values[0]
        self.name_var.set(values[1])
        self.country_var.set(values[2])
    
    def _clear_form(self):
        """Pulisce il form"""
        self._selected_id = None
        self.name_var.set('')
        self.country_var.set('')
        self.tree.selection_remove(self.tree.selection())
    
    def _validate_form(self):
        """Valida i dati del form"""
        if not self.name_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('producer_name_required', 'Il nome del produttore è obbligatorio')
            )
            return False
        return True
    
    def _on_add(self):
        """Aggiunge un nuovo produttore"""
        if not self._validate_form():
            return
        
        try:
            query = """
                INSERT INTO [Traceability_RS].[dbo].[Producers] (Producers, Country)
                VALUES (?, ?)
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (
                self.name_var.get().strip(),
                self.country_var.get().strip() or None
            ))
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('producer_added', 'Produttore aggiunto con successo')
            )
            
            self._clear_form()
            self._load_producers()
            
        except Exception as e:
            logger.error(f"Errore aggiunta produttore: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'aggiunta: {str(e)}"
            )
    
    def _on_update(self):
        """Modifica un produttore esistente"""
        if not self._selected_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_producer', 'Selezionare un produttore da modificare')
            )
            return
        
        if not self._validate_form():
            return
        
        try:
            query = """
                UPDATE [Traceability_RS].[dbo].[Producers]
                SET Producers = ?, Country = ?
                WHERE ProducerId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (
                self.name_var.get().strip(),
                self.country_var.get().strip() or None,
                self._selected_id
            ))
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('producer_updated', 'Produttore modificato con successo')
            )
            
            self._clear_form()
            self._load_producers()
            
        except Exception as e:
            logger.error(f"Errore modifica produttore: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la modifica: {str(e)}"
            )
    
    def _on_delete(self):
        """Elimina un produttore"""
        if not self._selected_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_producer', 'Selezionare un produttore da eliminare')
            )
            return
        
        # Conferma eliminazione
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_producer', 'Eliminare il produttore selezionato?')
        ):
            return
        
        try:
            query = """
                DELETE FROM [Traceability_RS].[dbo].[Producers]
                WHERE ProducerId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self._selected_id,))
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('producer_deleted', 'Produttore eliminato con successo')
            )
            
            self._clear_form()
            self._load_producers()
            
        except Exception as e:
            logger.error(f"Errore eliminazione produttore: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'eliminazione: {str(e)}"
            )


    def _load_printer_config(self, activity_type='paste_labels'):
        """Carica la configurazione della stampante dal database
        
        Args:
            activity_type: Tipo di attività per cui selezionare la stampante
                          (es. 'paste_labels', 'production', ecc.)
        """
        # Configurazione di default
        default_config = {
            "printer_ip": "192.168.1.100",
            "printer_port": 9100,
            "printer_name": "Zebra ZT230",
            "enabled": False
        }
        
        try:
            # Carica la prima stampante attiva dal database
            # In futuro si può estendere per selezionare in base all'attività
            query = """
                SELECT TOP 1 PrinterIP, PrinterPort, PrinterName, IsActive
                FROM [Traceability_RS].[pst].[PrinterConfigs]
                WHERE IsActive = 1
                ORDER BY PrinterId
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                self.printer_config = {
                    "printer_ip": row.PrinterIP,
                    "printer_port": row.PrinterPort,
                    "printer_name": row.PrinterName,
                    "enabled": row.IsActive
                }
                logger.info(f"Configurazione stampante caricata dal DB: {row.PrinterName}")
            else:
                logger.warning("Nessuna stampante attiva trovata nel database, uso configurazione di default")
                self.printer_config = default_config
                
        except Exception as e:
            logger.error(f"Errore caricamento config stampante dal DB: {e}")
            self.printer_config = default_config

    def _get_pasta_config_data(self, pasta_id):
        """Recupera i dati di configurazione della pasta (validità e temperature)"""
        try:
            query = """
                SELECT 
                    pc.Valability,
                    pc.LowTemperature,
                    pc.HighTemperature
                FROM [Traceability_RS].[pst].[PastaConfigs] pc
                WHERE pc.DateOut IS NULL 
                  AND pc.PastaId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (pasta_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'valability': row.Valability,
                    'low_temp': row.LowTemperature,
                    'high_temp': row.HighTemperature
                }
            else:
                logger.warning(f"Configurazione pasta non trovata per PastaId: {pasta_id}")
                return None
        except Exception as e:
            logger.error(f"Errore recupero configurazione pasta: {e}")
            return None

    def _generate_zpl_label(self, label_data):
        """Genera il template ZPL per l'etichetta con QR code"""
        # Template ZPL con QR code
        zpl_template = f"""^XA
                ^FO50,30^A0N,30,30^FDPasta: {label_data['pasta_name']}^FS
                ^FO50,70^A0N,25,25^FDRicevuto: {label_data['reception_date']}^FS
                ^FO50,110^A0N,25,25^FDCodice: {label_data['label_code']}^FS
                ^FO50,150^A0N,25,25^FDDa: {label_data['user_name']}^FS
                ^FO50,190^A0N,30,30^FDScadenza: {label_data['expiry_date']}^FS
                ^FO50,230^A0N,25,25^FDTemp: {label_data['low_temp']}C - {label_data['high_temp']}C^FS
                ^FO50,270^GB700,3,3^FS
                ^FO50,280^A0N,20,20^FDPASTRATI IN FRIGIDER^FS
                ^FO600,30^BQN,2,6^FDQA,{label_data['label_code']}^FS
                ^XZ"""
        
        return zpl_template

    def _print_to_zebra(self, zpl_content):
        """Invia il contenuto ZPL alla stampante Zebra via socket"""
        import socket
        
        if not self.printer_config.get('enabled', True):
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('printer_disabled', 'Stampante disabilitata nella configurazione')
            )
            return False
        
        try:
            # Connessione alla stampante
            printer_ip = self.printer_config.get('printer_ip')
            printer_port = self.printer_config.get('printer_port', 9100)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Timeout 5 secondi
            
            logger.info(f"Connessione a stampante {printer_ip}:{printer_port}")
            sock.connect((printer_ip, printer_port))
            
            # Invia ZPL
            sock.send(zpl_content.encode('utf-8'))
            sock.close()
            
            logger.info("Etichetta inviata alla stampante con successo")
            return True
            
        except socket.timeout:
            logger.error("Timeout connessione stampante")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('printer_timeout', 'Timeout connessione stampante. Verificare che sia accesa e raggiungibile.')
            )
            return False
        except socket.error as e:
            logger.error(f"Errore connessione stampante: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('printer_connection_error', 'Errore connessione stampante')}: {str(e)}"
            )
            return False
        except Exception as e:
            logger.error(f"Errore stampa etichetta: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('print_error', 'Errore durante la stampa')}: {str(e)}"
            )
            return False

    def _on_print_label(self):
        """Gestisce la stampa dell'etichetta"""
        # Validazione: deve esserci un log selezionato
        if not self._current_log_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_reception_to_print', 'Selezionare un ricevimento dalla lista per stampare l\'etichetta')
            )
            return
        
        try:
            # Recupera i dati del ricevimento
            query = """
                SELECT 
                    pl.PastaLogId,
                    pl.PastaId,
                    pl.LabelCode,
                    pl.GetIn,
                    pl.RegistryId,
                    p.PastaCode,
                    pr.ProducerName
                FROM [Traceability_RS].[pst].[PastaLogs] pl
                INNER JOIN [Traceability_RS].[pst].[Pastas] p ON pl.PastaId = p.PastaId
                INNER JOIN [Traceability_RS].[dbo].[Producers] pr ON p.ProducerId = pr.ProducerId
                WHERE pl.PastaLogId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self._current_log_id,))
            log_row = cursor.fetchone()
            cursor.close()
            
            if not log_row:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('reception_not_found', 'Ricevimento non trovato')
                )
                return
            
            # Recupera configurazione pasta
            pasta_config = self._get_pasta_config_data(log_row.PastaId)
            if not pasta_config:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('pasta_config_not_found', 'Configurazione pasta non trovata. Impossibile stampare etichetta.')
                )
                return
            
            # Calcola data di scadenza
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            
            reception_date = log_row.GetIn
            validity_months = pasta_config['valability']
            expiry_date = reception_date + relativedelta(months=validity_months)
            
            # Prepara i dati per l'etichetta
            label_data = {
                'pasta_name': f"{log_row.PastaCode} - {log_row.ProducerName}",
                'reception_date': reception_date.strftime('%d/%m/%Y %H:%M'),
                'label_code': log_row.LabelCode,
                'user_name': self.user_name,
                'expiry_date': expiry_date.strftime('%d/%m/%Y'),
                'low_temp': pasta_config['low_temp'],
                'high_temp': pasta_config['high_temp']
            }
            
            # Genera ZPL
            zpl_content = self._generate_zpl_label(label_data)
            
            # Debug: mostra ZPL generato
            logger.info(f"ZPL generato:\n{zpl_content}")
            
            # Stampa
            if self._print_to_zebra(zpl_content):
                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('label_printed', 'Etichetta stampata con successo')
                )
            
        except ImportError:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('missing_dateutil', 'Libreria python-dateutil non installata.\nEseguire: pip install python-dateutil')
            )
        except Exception as e:
            logger.error(f"Errore stampa etichetta: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('print_error', 'Errore durante la stampa')}: {str(e)}"
            )

    def _on_receive(self):
        """Registra il ricevimento"""
        # Validazione
        if not self.pasta_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_pasta', 'Selezionare una pasta'))
            return

        if not self.location_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_location', 'Selezionare una locazione'))
            return

        if not self.label_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('no_label_code', 'Codice etichetta mancante'))
            return

        pasta_id = self.pastas_dict[self.pasta_var.get()]
        location_id = self.locations_dict[self.location_var.get()]
        
        # Usa il label_id già generato
        if not self._current_label_id:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                               self.lang.get('no_label_code', 'Codice etichetta mancante'))
            return

        # Inserisci il log di ricevimento
        success, message = self.db.insert_pasta_log(pasta_id, self._current_label_id, self.user_name, self._doc_data)

        if success:
            # Mark label as used
            self._label_used = True
            self._current_label_id = None
            
            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_logs()
            
            # Reset form
            self.pasta_var.set('')
            self.label_var.set('')
            self._doc_data = None
            self._doc_filename = None
            self.doc_label.config(text='')
            self._label_used = False
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'), message)


def open_paste_reception(parent, db_handler, lang_manager, user_name):
    """Funzione helper per aprire la finestra ricevimento paste"""
    PasteReceptionWindow(parent, db_handler, lang_manager, user_name)
