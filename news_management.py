# -*- coding: utf-8 -*-
"""
Modulo per la gestione dei messaggi aziendali (News).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from tkcalendar import DateEntry
import logging

logger = logging.getLogger("TraceabilityRS")


class NewsManagementWindow(tk.Toplevel):
    """
    Finestra per la gestione dei messaggi aziendali.
    Permette di visualizzare, creare, modificare e cancellare messaggi.
    """
    
    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.parent = parent
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        
        logger.info(f"=== Inizializzazione NewsManagementWindow ===")
        logger.info(f"Utente: {self.user_name}")
        
        self.title(self.lang.get('news_management_title', 'Gestione Messaggi'))
        self.geometry("1400x800")
        self.transient(parent)
        self.grab_set()
        
        # Variabili
        self.selected_news = None
        self.news_list = []
        
        self._create_widgets()
        self._load_news()
        
    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame filtri
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Data inizio
        ttk.Label(filter_frame, text=self.lang.get('start_date', 'Data Inizio:')).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.start_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/MM/yyyy',
            locale='it_IT'
        )
        self.start_date.set_date(datetime.now() - timedelta(days=30))  # Ultimi 30 giorni
        self.start_date.grid(row=0, column=1, padx=5)
        
        # Data fine
        ttk.Label(filter_frame, text=self.lang.get('end_date', 'Data Fine:')).grid(row=0, column=2, sticky=tk.W, padx=5)
        self.end_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/MM/yyyy',
            locale='it_IT'
        )
        self.end_date.set_date(datetime.now() + timedelta(days=30))  # Prossimi 30 giorni
        self.end_date.grid(row=0, column=3, padx=5)
        
        # Pulsante filtra
        ttk.Button(
            filter_frame,
            text=self.lang.get('apply_filter', 'Applica Filtro'),
            command=self._load_news
        ).grid(row=0, column=4, padx=10)
        
        # Frame lista messaggi
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('news_list', 'Lista Messaggi'), padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('id', 'employer', 'start', 'end', 'publisher', 'mandatory')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('employer', text=self.lang.get('employer', 'Azienda'))
        self.tree.heading('start', text=self.lang.get('start_news', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end_news', 'Fine'))
        self.tree.heading('publisher', text=self.lang.get('publisher', 'Pubblicato da'))
        self.tree.heading('mandatory', text=self.lang.get('mandatory', 'Obbligatorio'))
        
        self.tree.column('id', width=50)
        self.tree.column('employer', width=100)
        self.tree.column('start', width=100)
        self.tree.column('end', width=100)
        self.tree.column('publisher', width=150)
        self.tree.column('mandatory', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        # Frame dettagli
        details_frame = ttk.LabelFrame(main_frame, text=self.lang.get('message_details', 'Dettagli Messaggio'), padding="10")
        details_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))
        
        # Text widget per il messaggio
        self.message_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame pulsanti
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            buttons_frame,
            text=self.lang.get('new_message', 'Nuovo Messaggio'),
            command=self._new_message
        ).pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ttk.Button(
            buttons_frame,
            text=self.lang.get('edit_message', 'Modifica'),
            command=self._edit_message,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(
            buttons_frame,
            text=self.lang.get('delete_message', 'Elimina'),
            command=self._delete_message,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _load_news(self):
        """Carica i messaggi dal database"""
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            
            logger.info(f"Caricamento messaggi dal {start_date} al {end_date}")
            
            query = """
                SELECT 
                    NewId,
                    EmployeerId,
                    StartNews,
                    EndNews,
                    News,
                    Publisher,
                    IsMandatory
                FROM [Employee].[dbo].[News]
                WHERE (StartNews >= ? OR EndNews >= ?)
                  AND (StartNews <= ? OR EndNews <= ?)
                ORDER BY StartNews DESC
            """
            
            with self.db._lock:
                self.db.cursor.execute(query, start_date, start_date, end_date, end_date)
                self.news_list = self.db.cursor.fetchall()
            
            logger.info(f"Caricati {len(self.news_list) if self.news_list else 0} messaggi")
            
            # Popola tree
            self.tree.delete(*self.tree.get_children())
            
            if self.news_list:
                for news in self.news_list:
                    self.tree.insert('', tk.END, values=(
                        news.NewId,
                        news.EmployeerId,
                        news.StartNews.strftime('%d/%m/%Y') if news.StartNews else '',
                        news.EndNews.strftime('%d/%m/%Y') if news.EndNews else '',
                        news.Publisher if news.Publisher else '',
                        'Sì' if news.IsMandatory else 'No'
                    ))
            
        except Exception as e:
            logger.error(f"Errore nel caricamento messaggi: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i messaggi: {str(e)}",
                parent=self
            )
    
    def _on_select(self, event):
        """Gestisce la selezione di un messaggio"""
        selection = self.tree.selection()
        if not selection:
            self.selected_news = None
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            self.message_text.delete(1.0, tk.END)
            return
        
        item = self.tree.item(selection[0])
        news_id = item['values'][0]
        
        # Trova il messaggio completo
        for news in self.news_list:
            if news.NewId == news_id:
                self.selected_news = news
                break
        
        if self.selected_news:
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Mostra il messaggio
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(1.0, self.selected_news.News if self.selected_news.News else '')
    
    def _new_message(self):
        """Apre dialog per nuovo messaggio"""
        dialog = NewsEditDialog(self, self.db, self.lang, self.user_name)
        self.wait_window(dialog)
        if dialog.saved:
            self._load_news()
    
    def _edit_message(self):
        """Apre dialog per modifica messaggio"""
        if not self.selected_news:
            return
        
        dialog = NewsEditDialog(self, self.db, self.lang, self.user_name, self.selected_news)
        self.wait_window(dialog)
        if dialog.saved:
            self._load_news()
    
    def _delete_message(self):
        """Elimina il messaggio selezionato"""
        if not self.selected_news:
            return
        
        response = messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_message', 'Confermare l\'eliminazione del messaggio?'),
            parent=self
        )
        
        if not response:
            return
        
        try:
            logger.info(f"Eliminazione messaggio ID: {self.selected_news.NewId}")
            
            delete_query = """
                DELETE FROM [Employee].[dbo].[News]
                WHERE NewId = ?
            """
            
            with self.db._lock:
                self.db.cursor.execute(delete_query, self.selected_news.NewId)
                try:
                    self.db.cursor.connection.commit()
                except:
                    pass  # Autocommit
            
            logger.info(f"✓ Messaggio {self.selected_news.NewId} eliminato")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('message_deleted', 'Messaggio eliminato con successo'),
                parent=self
            )
            
            self._load_news()
            
        except Exception as e:
            logger.error(f"Errore nell'eliminazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile eliminare il messaggio: {str(e)}",
                parent=self
            )


class NewsEditDialog(tk.Toplevel):
    """Dialog per creare/modificare un messaggio"""
    
    def __init__(self, parent, db_handler, lang_manager, user_name, news=None):
        super().__init__(parent)
        self.parent = parent
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        self.news = news  # None = nuovo, altrimenti modifica
        self.saved = False
        
        title = self.lang.get('edit_message', 'Modifica Messaggio') if news else self.lang.get('new_message', 'Nuovo Messaggio')
        self.title(title)
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if news:
            self._load_data()
    
    def _create_widgets(self):
        """Crea i widget del dialog"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # EmployerID
        ttk.Label(main_frame, text=self.lang.get('employer_id', 'ID Azienda:')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.employer_id = ttk.Spinbox(main_frame, from_=1, to=10, width=10)
        self.employer_id.set(2)  # Default
        self.employer_id.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Data inizio
        ttk.Label(main_frame, text=self.lang.get('start_news', 'Data Inizio:')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_news = DateEntry(
            main_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/MM/yyyy',
            locale='it_IT'
        )
        self.start_news.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Data fine
        ttk.Label(main_frame, text=self.lang.get('end_news', 'Data Fine:')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.end_news = DateEntry(
            main_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/MM/yyyy',
            locale='it_IT'
        )
        self.end_news.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Obbligatorio
        self.is_mandatory = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            main_frame,
            text=self.lang.get('mandatory_message', 'Messaggio Obbligatorio'),
            variable=self.is_mandatory
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Messaggio
        ttk.Label(main_frame, text=self.lang.get('message', 'Messaggio:')).grid(row=4, column=0, sticky=tk.NW, pady=5)
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.message_text = tk.Text(text_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.message_text.yview)
        self.message_text.configure(yscrollcommand=scrollbar.set)
        
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Pulsanti
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            buttons_frame,
            text=self.lang.get('save', 'Salva'),
            command=self._save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def _load_data(self):
        """Carica i dati del messaggio da modificare"""
        if self.news:
            self.employer_id.set(self.news.EmployeerId)
            if self.news.StartNews:
                self.start_news.set_date(self.news.StartNews)
            if self.news.EndNews:
                self.end_news.set_date(self.news.EndNews)
            self.is_mandatory.set(bool(self.news.IsMandatory))
            if self.news.News:
                self.message_text.insert(1.0, self.news.News)
    
    def _save(self):
        """Salva il messaggio"""
        # Validazione
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('message_required', 'Il messaggio è obbligatorio'),
                parent=self
            )
            return
        
        try:
            employer_id = int(self.employer_id.get())
            start_date = self.start_news.get_date()
            end_date = self.end_news.get_date()
            is_mandatory = 1 if self.is_mandatory.get() else 0
            
            if self.news:
                # UPDATE
                logger.info(f"Aggiornamento messaggio ID: {self.news.NewId}")
                
                update_query = """
                    UPDATE [Employee].[dbo].[News]
                    SET EmployeerId = ?,
                        StartNews = ?,
                        EndNews = ?,
                        News = ?,
                        Publisher = ?,
                        IsMandatory = ?
                    WHERE NewId = ?
                """
                
                with self.db._lock:
                    self.db.cursor.execute(
                        update_query,
                        employer_id,
                        start_date,
                        end_date,
                        message,
                        self.user_name,
                        is_mandatory,
                        self.news.NewId
                    )
                    try:
                        self.db.cursor.connection.commit()
                    except:
                        pass  # Autocommit
                
                logger.info(f"✓ Messaggio {self.news.NewId} aggiornato")
            else:
                # INSERT
                logger.info("Creazione nuovo messaggio")
                
                insert_query = """
                    INSERT INTO [Employee].[dbo].[News]
                    (EmployeerId, StartNews, EndNews, News, Publisher, IsMandatory)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                
                with self.db._lock:
                    self.db.cursor.execute(
                        insert_query,
                        employer_id,
                        start_date,
                        end_date,
                        message,
                        self.user_name,
                        is_mandatory
                    )
                    try:
                        self.db.cursor.connection.commit()
                    except:
                        pass  # Autocommit
                
                logger.info("✓ Nuovo messaggio creato")
            
            self.saved = True
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare il messaggio: {str(e)}",
                parent=self
            )
