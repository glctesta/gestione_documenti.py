"""
Modulo per la presa in carico paste in produzione
Conferma ricevimento paste nel frigorifero di produzione
"""
import tkinter as tk
from tkinter import ttk, messagebox
from loguru import logger


class PasteTakeChargeWindow(tk.Toplevel):
    """Finestra per presa in carico paste in produzione"""
    
    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        
        self.title(self.lang.get('paste_take_charge', 'Presa In Carico Paste'))
        self.geometry("1100x500")
        self.transient(parent)
        
        # Variabili
        self.production_fridges_dict = {}
        
        self._build_ui()
        self._load_production_fridges()
    
    def _build_ui(self):
        """Costruisce l'interfaccia"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Dividi in due colonne: sinistra (form) e destra (immagine)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=False)
        
        # --- Frame Form (sinistro) ---
        form_frame = ttk.LabelFrame(left_frame, text=self.lang.get('paste_take_charge', 'Presa In Carico'), padding="10")
        form_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Label Code
        ttk.Label(form_frame, text=self.lang.get('label_code', 'Codice Label') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.label_var = tk.StringVar()
        self.label_entry = ttk.Entry(form_frame, textvariable=self.label_var, width=30)
        self.label_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Frigorifero Produzione
        ttk.Label(form_frame, text=self.lang.get('production_fridge', 'Frigorifero Produzione') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        
        self.fridge_var = tk.StringVar()
        self.fridge_combo = ttk.Combobox(form_frame, textvariable=self.fridge_var,
                                        state='readonly', width=40)
        self.fridge_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Info Label
        self.info_label = ttk.Label(form_frame, text='', foreground='blue')
        self.info_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Pulsanti
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self.lang.get('btn_confirm', 'Conferma Presa In Carico'),
                  command=self._confirm_take_charge).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self.destroy).pack(side='left', padx=5)
        
        # --- Frame Destro (immagine + messaggio) ---
        # Carica minuti acclimatamento
        acclimate_minutes = self._get_acclimate_minutes()
        
        # Carica immagine
        try:
            from PIL import Image, ImageTk
            import os
            
            img_path = os.path.join(os.path.dirname(__file__), 'Frigo_acclimate.jpg')
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Ridimensiona se necessario
                img = img.resize((400, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                img_label = ttk.Label(right_frame, image=photo)
                img_label.image = photo  # Mantieni riferimento
                img_label.pack(pady=10)
            else:
                logger.warning(f"[PASTE] Immagine non trovata: {img_path}")
        except Exception as e:
            logger.error(f"[PASTE] Errore caricamento immagine: {e}")
        
        # Messaggio acclimatamento in rosso bold
        warning_text = self.lang.get(
            'acclimate_warning',
            f'Attenzione, la pasta appena caricata deve essere posizionata '
            f'nella parte del frigorifero evidenziata nella foto per acclimatamento '
            f'per {acclimate_minutes} minuti.'
        ).format(minutes=acclimate_minutes)
        
        warning_label = ttk.Label(
            right_frame,
            text=warning_text,
            foreground='red',
            font=('Arial', 10, 'bold'),
            wraplength=400,
            justify='center'
        )
        warning_label.pack(pady=10, padx=10)
    
    def _load_production_fridges(self):
        """Carica i frigoriferi di produzione (IsWarehouse=0)"""
        try:
            query = """
                SELECT PastaStoreFrigiderLocationId, PastaStoreFrigiderLocationName, PastaStoreFrigiderId
                FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                WHERE IsWarehouse = 0
                ORDER BY PastaStoreFrigiderLocationName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            self.production_fridges_dict = {}
            for row in cursor.fetchall():
                # Usa PastaStoreFrigiderId come chiave
                self.production_fridges_dict[row.PastaStoreFrigiderLocationName] = row.PastaStoreFrigiderId
            
            self.fridge_combo['values'] = list(self.production_fridges_dict.keys())
            cursor.close()
            
            logger.info(f"[TAKE_CHARGE] Caricati {len(self.production_fridges_dict)} frigoriferi produzione")
        except Exception as e:
            logger.error(f"Errore caricamento frigoriferi: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento frigoriferi: {str(e)}"
            )
    
    def _get_acclimate_minutes(self):
        """Recupera i minuti di acclimatamento dal database"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT TimeInMinute 
                FROM [Traceability_RS].[pst].[PasteAcclimate]
            """)
            
            row = cursor.fetchone()
            cursor.close()
            
            if row and row.TimeInMinute:
                return int(row.TimeInMinute)
            else:
                logger.warning("[TAKE_CHARGE] Minuti acclimatamento non trovati, uso default 30")
                return 30  # Default
        except Exception as e:
            logger.error(f"Errore recupero minuti acclimatamento: {e}")
            return 30  # Default in caso di errore
    
    
    def _confirm_take_charge(self):
        """Conferma la presa in carico della pasta"""
        label_code = self.label_var.get().strip()
        fridge_name = self.fridge_var.get()
        
        # Validazioni
        if not label_code:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_label_code', 'Inserire il codice label')
            )
            return
        
        if not fridge_name:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_fridge', 'Selezionare un frigorifero')
            )
            return
        
        try:
            fridge_id = self.production_fridges_dict[fridge_name]
            cursor = self.db.conn.cursor()
            
            # Query per trovare la pasta in pending
            query = """
                SELECT p.[PastaLogId], pa.PastaCode
                FROM [Traceability_RS].[pst].[PastaLogs] p 
                INNER JOIN [Traceability_RS].[pst].[PastaLabelCodes] l 
                    ON p.LabeCodeId = l.LabelCodeId 
                INNER JOIN [Traceability_RS].[pst].[Pastas] pa
                    ON p.PastaId = pa.Pastaid
                INNER JOIN [Traceability_RS].[pst].[PastaStoreFrigiders] f 
                    ON f.PastaStoreFrigiderId = p.PastaStoreFrigiderId
                WHERE p.Pending = 1 
                  AND p.GetOut IS NULL 
                  AND p.PastaStoreFrigiderId = ?
                  AND l.LabelCode = ?
            """
            
            cursor.execute(query, (fridge_id, label_code))
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('paste_not_found_pending', 
                                 f'Pasta con label {label_code} non trovata in pending per questo frigorifero')
                )
                return
            
            pasta_log_id = result.PastaLogId
            pasta_code = result.PastaCode
            
            # Conferma prima di procedere
            confirm = messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                f"Confermare la presa in carico della pasta:\n\n"
                f"Codice Pasta: {pasta_code}\n"
                f"Label: {label_code}\n"
                f"Frigorifero: {fridge_name}"
            )
            
            if not confirm:
                cursor.close()
                return
            
            # UPDATE: Pending da 1 a 0 e LoadDate = GETDATE()
            update_query = """
                UPDATE [Traceability_RS].[pst].[PastaLogs]
                SET Pending = 0, LoadDate = GETDATE()
                WHERE PastaLogId = ?
            """
            
            cursor.execute(update_query, (pasta_log_id,))
            self.db.conn.commit()
            cursor.close()
            
            logger.info(f"[TAKE_CHARGE] Presa in carico PastaLogId={pasta_log_id}, Label={label_code}, User={self.user_name}")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('take_charge_completed', 
                             f'Presa in carico completata!\n\nPasta: {pasta_code}\nLabel: {label_code}')
            )
            
            # Reset form
            self.label_var.set('')
            self.fridge_var.set('')
            self.info_label.config(text='')
            
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore presa in carico: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la presa in carico: {str(e)}"
            )


def open_paste_take_charge(parent, db_handler, lang_manager, user_name):
    """Funzione helper per aprire la finestra presa in carico"""
    PasteTakeChargeWindow(parent, db_handler, lang_manager, user_name)
