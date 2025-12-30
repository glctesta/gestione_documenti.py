"""
Modulo per la gestione del cambio password utente.
Permette agli utenti di cambiare la propria password con verifica della password corrente.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
import logging

logger = logging.getLogger("TraceabilityRS")


class ChangePasswordWindow(tk.Toplevel):
    """Finestra per il cambio password utente"""
    
    def __init__(self, parent, db, lang, user_id=None, force_change=False):
        """
        Inizializza la finestra di cambio password.
        
        Args:
            parent: Finestra padre
            db: Oggetto database
            lang: Gestore traduzioni
            user_id: ID utente (opzionale, se None chiede all'utente)
            force_change: Se True, la finestra è modale e obbligatoria
        """
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_id = user_id
        self.force_change = force_change
        self.password_changed = False
        
        self.title(self.lang.get('change_password_title', 'Cambio Password'))
        self.geometry("450x450")
        self.resizable(False, False)
        
        if force_change:
            # Finestra modale obbligatoria
            self.transient(parent)
            self.grab_set()
            self.protocol("WM_DELETE_WINDOW", self._on_cancel_forced)
        else:
            self.transient(parent)
        
        self._build_ui()
        self._center_window()
        
    def _center_window(self):
        """Centra la finestra sullo schermo"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _build_ui(self):
        """Costruisce l'interfaccia utente"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        if self.force_change:
            title_text = self.lang.get('password_expired_title', 
                                      '⚠️ Password Scaduta - Cambio Obbligatorio')
            title_color = 'red'
        else:
            title_text = self.lang.get('change_password_title', 'Cambio Password')
            title_color = 'black'
            
        title_label = ttk.Label(main_frame, text=title_text, 
                               font=('Arial', 12, 'bold'),
                               foreground=title_color)
        title_label.pack(pady=(0, 20))
        
        # Frame campi
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # User ID (se non fornito)
        if self.user_id is None:
            ttk.Label(fields_frame, text=self.lang.get('user_id_label', 'User ID:')).grid(
                row=0, column=0, sticky=tk.W, pady=5)
            self.userid_entry = ttk.Entry(fields_frame, width=30)
            self.userid_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
            start_row = 1
        else:
            # Mostra user ID (read-only)
            ttk.Label(fields_frame, text=self.lang.get('user_id_label', 'User ID:')).grid(
                row=0, column=0, sticky=tk.W, pady=5)
            ttk.Label(fields_frame, text=str(self.user_id), 
                     font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            start_row = 1
        
        # Password corrente
        ttk.Label(fields_frame, text=self.lang.get('current_password_label', 
                                                   'Password Corrente:')).grid(
            row=start_row, column=0, sticky=tk.W, pady=5)
        self.current_password_entry = ttk.Entry(fields_frame, width=30, show='*')
        self.current_password_entry.grid(row=start_row, column=1, pady=5, padx=(10, 0))
        
        # Nuova password
        ttk.Label(fields_frame, text=self.lang.get('new_password_label', 
                                                   'Nuova Password:')).grid(
            row=start_row+1, column=0, sticky=tk.W, pady=5)
        self.new_password_entry = ttk.Entry(fields_frame, width=30, show='*')
        self.new_password_entry.grid(row=start_row+1, column=1, pady=5, padx=(10, 0))
        
        # Conferma nuova password
        ttk.Label(fields_frame, text=self.lang.get('confirm_password_label', 
                                                   'Conferma Password:')).grid(
            row=start_row+2, column=0, sticky=tk.W, pady=5)
        self.confirm_password_entry = ttk.Entry(fields_frame, width=30, show='*')
        self.confirm_password_entry.grid(row=start_row+2, column=1, pady=5, padx=(10, 0))
        
        # Requisiti password
        requirements_text = self.lang.get('password_requirements',
            'Requisiti password:\n'
            '• Minimo 6 caratteri\n'
            '• Almeno una lettera maiuscola\n'
            '• Almeno un numero'
        )
        req_label = ttk.Label(fields_frame, text=requirements_text, 
                             font=('Arial', 8), foreground='gray')
        req_label.grid(row=start_row+3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Pulsanti
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('button_change_password', 'Cambia Password'),
                  command=self._on_change_password).pack(side=tk.LEFT, padx=5)
        
        if not self.force_change:
            ttk.Button(btn_frame, text=self.lang.get('button_cancel', 'Annulla'),
                      command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def _on_cancel_forced(self):
        """Gestisce il tentativo di chiusura quando il cambio è obbligatorio"""
        messagebox.showwarning(
            self.lang.get('warning_title', 'Attenzione'),
            self.lang.get('password_change_required', 
                         'Il cambio password è obbligatorio. Non puoi annullare.'),
            parent=self
        )
    
    def _validate_password(self, password):
        """
        Valida i requisiti della password.
        
        Returns:
            tuple: (bool, str) - (valido, messaggio_errore)
        """
        if len(password) < 6:
            return False, self.lang.get('password_too_short', 
                                       'La password deve essere di almeno 6 caratteri')
        
        if not any(c.isupper() for c in password):
            return False, self.lang.get('password_no_uppercase', 
                                       'La password deve contenere almeno una lettera maiuscola')
        
        if not any(c.isdigit() for c in password):
            return False, self.lang.get('password_no_number', 
                                       'La password deve contenere almeno un numero')
        
        return True, ""
    
    def _on_change_password(self):
        """Gestisce il cambio password"""
        try:
            # Recupera i valori
            if self.user_id is None:
                user_id = self.userid_entry.get().strip()
                if not user_id:
                    messagebox.showerror(
                        self.lang.get('error_title', 'Errore'),
                        self.lang.get('userid_required', 'Inserire User ID'),
                        parent=self
                    )
                    return
            else:
                user_id = self.user_id
            
            current_password = self.current_password_entry.get()
            new_password = self.new_password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            
            # Validazioni
            if not current_password:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    self.lang.get('current_password_required', 'Inserire la password corrente'),
                    parent=self
                )
                return
            
            if not new_password:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    self.lang.get('new_password_required', 'Inserire la nuova password'),
                    parent=self
                )
                return
            
            if new_password != confirm_password:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    self.lang.get('passwords_dont_match', 'Le password non coincidono'),
                    parent=self
                )
                return
            
            # Valida requisiti password
            valid, error_msg = self._validate_password(new_password)
            if not valid:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    error_msg,
                    parent=self
                )
                return
            
            # Verifica password corrente e cambia
            success, message = self._change_password_in_db(user_id, current_password, new_password)
            
            if success:
                self.password_changed = True
                messagebox.showinfo(
                    self.lang.get('success_title', 'Successo'),
                    self.lang.get('password_changed_successfully', 
                                 'Password cambiata con successo!'),
                    parent=self
                )
                self.destroy()
            else:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    message,
                    parent=self
                )
                
        except Exception as e:
            logger.error(f"Errore durante il cambio password: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"{self.lang.get('unexpected_error', 'Errore imprevisto')}: {str(e)}",
                parent=self
            )
    
    def _change_password_in_db(self, user_id, current_password, new_password):
        """
        Cambia la password nel database.
        
        Returns:
            tuple: (bool, str) - (successo, messaggio)
        """
        try:
            # Verifica password corrente
            query_check = """
                SELECT IdUserKey, Pass 
                FROM ResetServices.dbo.TbUserKey 
                WHERE NomeUser = ?
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(query_check, user_id)
            row = cursor.fetchone()
            
            if not row:
                return False, self.lang.get('user_not_found', 'Utente non trovato')
            
            if row.Pass != current_password:
                # Gestione caso in cui Pass sia in formato binario (bytes)
                db_pass = row.Pass
                if isinstance(db_pass, bytes):
                    try:
                        db_pass = db_pass.decode('utf-8').rstrip('\x00')
                    except:
                        pass
                
                if db_pass != current_password:
                    return False, self.lang.get('wrong_current_password', 
                                               'Password corrente errata')
                                           
            if new_password == current_password:
                return False, self.lang.get('new_password_same_as_current', 
                                           'La nuova password non può essere uguale a quella attuale')

            # --- NUOVA LOGICA: Controllo storico password (ultimi 6 mesi) ---
            query_history_check = """
                SELECT TOP 1 UserKeyPassLogId
                FROM ResetServices.dbo.TbUserKeyLogs
                WHERE IduserKey = ? AND Password = CONVERT(VARBINARY(MAX), ?) 
                  AND DateChange >= DATEADD(month, -6, GETDATE())
            """
            cursor.execute(query_history_check, row.IdUserKey, new_password)
            if cursor.fetchone():
                return False, self.lang.get('password_already_used_recently', 
                                           'Questa password è già stata utilizzata negli ultimi 6 mesi. Sceglierne una diversa.')

            # Aggiorna password principale
            query_update = """
                UPDATE ResetServices.dbo.TbUserKey
                SET Pass = CONVERT(VARBINARY(MAX), ?),
                    Cambia = 1,
                    Scadenza = 90,
                    Scade = 1,
                    DataChangePass = GETDATE()
                WHERE IdUserKey = ?
            """
            cursor.execute(query_update, new_password, row.IdUserKey)

            # --- NUOVA LOGICA: Registrazione nello storico ---
            query_log = """
                INSERT INTO ResetServices.dbo.TbUserKeyLogs (IduserKey, Password, DateChange)
                VALUES (?, CONVERT(VARBINARY(MAX), ?), GETDATE())
            """
            cursor.execute(query_log, row.IdUserKey, new_password)
            
            self.db.conn.commit()
            
            logger.info(f"Password cambiata per utente: {user_id}")
            return True, "Password cambiata con successo"
            
        except pyodbc.Error as e:
            self.db.conn.rollback()
            logger.error(f"Errore database durante cambio password: {e}")
            return False, f"Errore database: {str(e)}"
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore imprevisto durante cambio password: {e}")
            return False, f"Errore imprevisto: {str(e)}"
        finally:
            try:
                cursor.close()
            except:
                pass


def check_password_expiration(db, user_id):
    """
    Verifica se la password dell'utente è scaduta.
    
    Args:
        db: Oggetto database
        user_id: ID utente
        
    Returns:
        tuple: (bool, str) - (scaduta, messaggio)
    """
    try:
        query = """
            SELECT Cambia, Scadenza, Scade, DataChangePass
            FROM ResetServices.dbo.TbUserKey
            WHERE NomeUser = ?
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, user_id)
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return False, "Utente non trovato"
        
        # Se i campi sono NULL, non forza il cambio
        cambia = getattr(row, 'Cambia', None)
        scadenza = getattr(row, 'Scadenza', None)
        scade = getattr(row, 'Scade', None)
        data_change = getattr(row, 'DataChangePass', None)
        
        # Se tutti NULL o Scade è False, non scade
        if scade is None or scade == 0:
            return False, "Password non scade"
        
        # Se Cambia è True, forza cambio
        if cambia == 1:
            # Se non c'è data cambio, forza cambio
            if data_change is None:
                return True, "Prima configurazione password"
            
            # Calcola giorni dalla data cambio
            if scadenza is not None and scadenza > 0:
                from datetime import datetime, timedelta
                giorni_passati = (datetime.now() - data_change).days
                
                if giorni_passati >= scadenza:
                    return True, f"Password scaduta ({giorni_passati} giorni)"
        
        return False, "Password valida"
        
    except Exception as e:
        logger.error(f"Errore verifica scadenza password: {e}")
        return False, f"Errore: {str(e)}"


def open_change_password_window(parent, db, lang, user_id=None, force_change=False):
    """
    Apre la finestra di cambio password.
    
    Args:
        parent: Finestra padre
        db: Oggetto database
        lang: Gestore traduzioni
        user_id: ID utente (opzionale)
        force_change: Se True, cambio obbligatorio
        
    Returns:
        bool: True se la password è stata cambiata
    """
    window = ChangePasswordWindow(parent, db, lang, user_id, force_change)
    parent.wait_window(window)
    return window.password_changed
