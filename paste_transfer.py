"""
Modulo per il trasferimento paste da warehouse a produzione
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from loguru import logger


class PastaTransferToProductionWindow(tk.Toplevel):
    """Finestra per trasferimento paste da warehouse a produzione"""
    
    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        
        self.title(self.lang.get('paste_transfer_to_production', 'Trasferimento Paste a Produzione'))
        self.geometry("900x700")
        self.transient(parent)
        
        # Variabili
        self._current_pasta_log = None
        self._current_pasta_info = None
        self.production_locations_dict = {}
        
        self._build_ui()
        self._load_production_locations()
    
    def _build_ui(self):
        """Costruisce l'interfaccia"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # --- SEZIONE 1: Ricerca Label ---
        search_frame = ttk.LabelFrame(main_frame, text=self.lang.get('search_label', 'Ricerca Label'), padding="10")
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text=self.lang.get('label_code', 'Codice Label') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.label_var = tk.StringVar()
        self.label_entry = ttk.Entry(search_frame, textvariable=self.label_var, width=30)
        self.label_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Button(search_frame, text=self.lang.get('btn_verify', 'Verifica'),
                  command=self._verify_label).grid(row=0, column=2, padx=5, pady=5)
        
        # --- SEZIONE 2: Info Pasta (nascosta inizialmente) ---
        self.info_frame = ttk.LabelFrame(main_frame, text=self.lang.get('paste_info', 'Informazioni Pasta'), padding="10")
        self.info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.info_frame.pack_forget()  # Nascosto inizialmente
        
        # Info Labels
        info_grid = ttk.Frame(self.info_frame)
        info_grid.pack(fill='x', padx=5, pady=5)
        
        row = 0
        ttk.Label(info_grid, text=self.lang.get('pasta_code', 'Codice Pasta') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.pasta_code_label = ttk.Label(info_grid, text='', font=('', 10, 'bold'))
        self.pasta_code_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        row += 1
        ttk.Label(info_grid, text=self.lang.get('producer', 'Produttore') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.producer_label = ttk.Label(info_grid, text='')
        self.producer_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        row += 1
        ttk.Label(info_grid, text=self.lang.get('current_location', 'Posizione Attuale') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.location_label = ttk.Label(info_grid, text='')
        self.location_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        row += 1
        ttk.Label(info_grid, text=self.lang.get('reception_date', 'Data Ricevimento') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.reception_date_label = ttk.Label(info_grid, text='')
        self.reception_date_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        row += 1
        ttk.Label(info_grid, text=self.lang.get('expiration_date', 'Data Scadenza') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.expiration_label = ttk.Label(info_grid, text='', font=('', 10, 'bold'))
        self.expiration_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        row += 1
        ttk.Label(info_grid, text=self.lang.get('status', 'Stato') + ':').grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        self.status_label = ttk.Label(info_grid, text='', font=('', 10, 'bold'))
        self.status_label.grid(row=row, column=1, sticky='w', padx=5, pady=3)
        
        # --- SEZIONE 3: Selezione Destinazione ---
        dest_frame = ttk.LabelFrame(self.info_frame, text=self.lang.get('destination', 'Destinazione'), padding="10")
        dest_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Label(dest_frame, text=self.lang.get('production_location', 'Frigorifero Produzione') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.dest_location_var = tk.StringVar()
        self.dest_location_combo = ttk.Combobox(dest_frame, textvariable=self.dest_location_var,
                                                state='readonly', width=40)
        self.dest_location_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        dest_frame.columnconfigure(1, weight=1)
        
        # --- SEZIONE 4: Pulsanti Azione ---
        btn_frame = ttk.Frame(self.info_frame)
        btn_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(btn_frame, text=self.lang.get('btn_transfer', 'Trasferisci'),
                  command=self._transfer).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self._reset_form).pack(side='left', padx=5)
    
    def _load_production_locations(self):
        """Carica le location di produzione (IsWarehouse=0)"""
        try:
            query = """
                SELECT PastaStoreFrigiderLocationId, PastaStoreFrigiderLocationName, PastaStoreFrigiderId
                FROM [Traceability_RS].[pst].[PastaStoreFrigiderLocations]
                WHERE IsWarehouse = 0
                ORDER BY PastaStoreFrigiderLocationName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            self.production_locations_dict = {}
            for row in cursor.fetchall():
                self.production_locations_dict[row.PastaStoreFrigiderLocationName] = {
                    'location_id': row.PastaStoreFrigiderLocationId,
                    'fridge_id': row.PastaStoreFrigiderId
                }
            
            self.dest_location_combo['values'] = list(self.production_locations_dict.keys())
            cursor.close()
            
            logger.info(f"[TRANSFER] Caricate {len(self.production_locations_dict)} locations produzione")
        except Exception as e:
            logger.error(f"Errore caricamento location produzione: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento frigoriferi: {str(e)}"
            )
    
    def _verify_label(self):
        """Verifica il label code e mostra le info se valido"""
        label_code = self.label_var.get().strip()
        
        if not label_code:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_label_code', 'Inserire il codice label')
            )
            return
        
        try:
            cursor = self.db.conn.cursor()
            
            # 1. Trova LabeCodeId
            cursor.execute("""
                SELECT LabelCodeId 
                FROM [Traceability_RS].[pst].[PastaLabelCodes]
                WHERE LabelCode = ?
            """, (label_code,))
            
            label_row = cursor.fetchone()
            if not label_row:
                cursor.close()
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('label_not_found', f'Label {label_code} non trovato')
                )
                return
            
            label_code_id = label_row.LabelCodeId
            
            # 2. Cerca in PastaLogs (warehouse, GetOut NULL)
            cursor.execute("""
                SELECT pl.PastaLogId, pl.PastaId, pl.GetIn, pl.PastaStoreFrigiderId,
                       p.PastaCode, pr.Producers as ProducerName,
                       psl.PastaStoreFrigiderLocationName
                FROM [Traceability_RS].[pst].[PastaLogs] pl
                INNER JOIN [Traceability_RS].[pst].[Pastas] p ON pl.PastaId = p.Pastaid
                INNER JOIN [Traceability_RS].[dbo].[Producers] pr ON p.ProducerId = pr.ProducerId
                INNER JOIN [Traceability_RS].[pst].[PastaStoreFrigiders] psf 
                    ON pl.PastaStoreFrigiderId = psf.PastaStoreFrigiderId
                INNER JOIN [Traceability_RS].[pst].[PastaStoreFrigiderLocations] psl 
                    ON psf.PastaStoreFrigiderId = psl.PastaStoreFrigiderId
                WHERE pl.LabeCodeId = ?
                  AND psl.IsWarehouse = 1
                  AND pl.GetOut IS NULL
            """, (label_code_id,))
            
            pasta_log = cursor.fetchone()
            if not pasta_log:
                cursor.close()
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('pasta_not_in_warehouse', 
                                 'Pasta non trovata in warehouse o già trasferita')
                )
                return
            
            # 3. Verifica validità tramite DateIn da PastaInUseLogs e Valability da PastaConfigs
            cursor.execute("""
                SELECT c.Valability, piul.DateIn
                FROM [Traceability_RS].[pst].[PastaConfigs] c
                INNER JOIN [Traceability_RS].[pst].[PastaInUseLogs] piul 
                    ON piul.PastaLogid = ?
                WHERE c.PastaId = ?
            """, (pasta_log.PastaLogId, pasta_log.PastaId))
            
            validity_row = cursor.fetchone()
            cursor.close()
            
            if not validity_row or not validity_row.Valability or not validity_row.DateIn:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('no_validity_config', 'Configurazione validità non trovata')
                )
                return
            
            # Calcola data scadenza
            date_in = validity_row.DateIn
            valability_months = validity_row.Valability
            expiration_date = date_in + timedelta(days=30 * valability_months)
            
            is_valid = datetime.now() < expiration_date
            days_remaining = (expiration_date - datetime.now()).days
            
            # Salva le info
            self._current_pasta_log = pasta_log
            self._current_pasta_info = {
                'label_code_id': label_code_id,
                'expiration_date': expiration_date,
                'is_valid': is_valid,
                'days_remaining': days_remaining
            }
            
            # 4. Mostra info_frame
            self.pasta_code_label.config(text=pasta_log.PastaCode)
            self.producer_label.config(text=pasta_log.ProducerName)
            self.location_label.config(text=pasta_log.PastaStoreFrigiderLocationName)
            self.reception_date_label.config(text=date_in.strftime('%d/%m/%Y %H:%M'))
            self.expiration_label.config(text=expiration_date.strftime('%d/%m/%Y'))
            
            if is_valid:
                status_text = f"✓ VALIDA ({days_remaining} giorni rimanenti)"
                self.status_label.config(text=status_text, foreground='green')
                self.info_frame.pack(fill='both', expand=True, padx=5, pady=5)
            else:
                status_text = f"✗ SCADUTA ({abs(days_remaining)} giorni fa)"
                self.status_label.config(text=status_text, foreground='red')
                self.info_frame.pack(fill='both', expand=True, padx=5, pady=5)
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('paste_expired', 'ATTENZIONE: La pasta è scaduta!')
                )
            
            logger.info(f"[TRANSFER] Verificato label {label_code}: PastaLogId={pasta_log.PastaLogId}, Valido={is_valid}")
            
        except Exception as e:
            logger.error(f"Errore verifica label: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la verifica: {str(e)}"
            )
    
    def _transfer(self):
        """Esegue il trasferimento"""
        if not self.dest_location_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_destination', 'Selezionare frigorifero di destinazione')
            )
            return
        
        if not self._current_pasta_log or not self._current_pasta_info:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('verify_label_first', 'Verificare prima il label')
            )
            return
        
        try:
            dest_location_name = self.dest_location_var.get()
            dest_info = self.production_locations_dict[dest_location_name]
            dest_location_id = dest_info['location_id']
            dest_fridge_id = dest_info['fridge_id']
            
            cursor = self.db.conn.cursor()
            
            # 1. UPDATE PastaLogs: SET GetOut = GETDATE() WHERE PastaLogId
            cursor.execute("""
                UPDATE [Traceability_RS].[pst].[PastaLogs]
                SET GetOut = GETDATE()
                WHERE PastaLogId = ?
            """, (self._current_pasta_log.PastaLogId,))
            
            # 2. UPDATE PastaInUseLogs: SET DateOut = GETDATE()
            cursor.execute("""
                UPDATE [Traceability_RS].[pst].[PastaInUseLogs]
                SET DateOut = GETDATE()
                WHERE PastaLogid = ?
            """, (self._current_pasta_log.PastaLogId,))
            
            self.db.conn.commit()
            
            # 3. INSERT nuovo PastaLogs (Pending=1)
            cursor.execute("""
                INSERT INTO [Traceability_RS].[pst].[PastaLogs]
                (PastaId, LabeCodeId, GetIn, [User], PastaStoreFrigiderId, Pending)
                VALUES (?, ?, GETDATE(), ?, ?, 1)
            """, (
                self._current_pasta_log.PastaId,
                self._current_pasta_info['label_code_id'],
                self.user_name,
                dest_fridge_id
            ))
            
            # Ottieni l'ID del nuovo log
            cursor.execute("SELECT @@IDENTITY")
            new_log_id = int(cursor.fetchone()[0])
            
            # 4. INSERT nuovo PastaInUseLogs (IsNew=1)
            cursor.execute("""
                INSERT INTO [Traceability_RS].[pst].[PastaInUseLogs]
                (PastaLogid, PastaStoreFrigiderLocationId, IsNew, DateIn)
                VALUES (?, ?, 1, GETDATE())
            """, (new_log_id, dest_location_id))
            
            self.db.conn.commit()
            cursor.close()
            
            logger.info(f"[TRANSFER] Trasferito PastaLogId={self._current_pasta_log.PastaLogId} "
                       f"→ Nuovo PastaLogId={new_log_id}, Location={dest_location_name}")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('transfer_completed', 
                             f'Pasta trasferita con successo in {dest_location_name}')
            )
            
            # Reset form
            self._reset_form()
            
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore trasferimento: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il trasferimento: {str(e)}"
            )
    
    def _reset_form(self):
        """Reset del form"""
        self.label_var.set('')
        self.dest_location_var.set('')
        self.info_frame.pack_forget()
        self._current_pasta_log = None
        self._current_pasta_info = None


def open_paste_to_production(parent, db_handler, lang_manager, user_name):
    """Funzione helper per aprire la finestra trasferimento"""
    PastaTransferToProductionWindow(parent, db_handler, lang_manager, user_name)
