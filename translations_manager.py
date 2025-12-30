"""
Modulo per la gestione delle traduzioni dell'applicazione
Permette di visualizzare, filtrare, aggiungere, modificare ed eliminare traduzioni
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, List, Tuple


class TranslationsManagerWindow(tk.Toplevel):
    """Finestra per la gestione delle traduzioni"""
    
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        
        self.title(self.lang.get('translations_manager_title', 'Gestione Traduzioni'))
        self.geometry('1400x800')
        
        # Variabili per i filtri
        self.filter_language = tk.StringVar()
        self.filter_key = tk.StringVar()
        self.filter_value = tk.StringVar()
        self.filter_menu = tk.StringVar()
        
        self._create_widgets()
        self._load_translations()
        
    def _create_widgets(self):
        """Crea tutti i widget della finestra"""
        
        # Frame principale con PanedWindow per dividere traduzioni e utenti autorizzati
        main_paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== SEZIONE SUPERIORE: TRADUZIONI =====
        translations_frame = ttk.Frame(main_paned)
        main_paned.add(translations_frame, weight=3)
        
        # Frame filtri
        filters_frame = ttk.LabelFrame(translations_frame, text=self.lang.get('filters', 'Filtri'), padding=10)
        filters_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Riga 1: LanguageCode e TranslationKey
        row1 = ttk.Frame(filters_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text=self.lang.get('language_code', 'Lingua:')).pack(side=tk.LEFT, padx=5)
        language_combo = ttk.Combobox(row1, textvariable=self.filter_language, width=10, 
                                      values=['', 'it', 'ro', 'de', 'en', 'sv'], state='readonly')
        language_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text=self.lang.get('translation_key', 'Chiave:')).pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=self.filter_key, width=30).pack(side=tk.LEFT, padx=5)
        
        # Riga 2: TranslationValue e MenuValue
        row2 = ttk.Frame(filters_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text=self.lang.get('translation_value', 'Valore:')).pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=self.filter_value, width=30).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text=self.lang.get('menu_value', 'Menu:')).pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=self.filter_menu, width=30).pack(side=tk.LEFT, padx=5)
        
        # Pulsanti filtri
        buttons_row = ttk.Frame(filters_frame)
        buttons_row.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_row, text=self.lang.get('apply_filters', 'Applica Filtri'), 
                  command=self._apply_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row, text=self.lang.get('reset_filters', 'Reset Filtri'), 
                  command=self._reset_filters).pack(side=tk.LEFT, padx=5)
        
        # Frame Treeview traduzioni
        tree_frame = ttk.Frame(translations_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview traduzioni
        self.translations_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'LanguageCode', 'TranslationKey', 'TranslationValue', 'MenuValue'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.translations_tree.yview)
        hsb.config(command=self.translations_tree.xview)
        
        # Configurazione colonne
        self.translations_tree.heading('ID', text='ID')
        self.translations_tree.heading('LanguageCode', text=self.lang.get('language_code', 'Lingua'))
        self.translations_tree.heading('TranslationKey', text=self.lang.get('translation_key', 'Chiave'))
        self.translations_tree.heading('TranslationValue', text=self.lang.get('translation_value', 'Valore'))
        self.translations_tree.heading('MenuValue', text=self.lang.get('menu_value', 'Menu'))
        
        self.translations_tree.column('ID', width=50, anchor=tk.CENTER)
        self.translations_tree.column('LanguageCode', width=80, anchor=tk.CENTER)
        self.translations_tree.column('TranslationKey', width=250)
        self.translations_tree.column('TranslationValue', width=300)
        self.translations_tree.column('MenuValue', width=200)
        
        # Bind selezione
        self.translations_tree.bind('<<TreeviewSelect>>', self._on_translation_select)
        
        # Layout treeview e scrollbars
        self.translations_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Frame pulsanti azioni
        actions_frame = ttk.Frame(translations_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(actions_frame, text=self.lang.get('add', 'Aggiungi'), 
                  command=self._add_translation).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=self.lang.get('edit', 'Modifica'), 
                  command=self._edit_translation).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=self.lang.get('delete', 'Elimina'), 
                  command=self._delete_translation).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=self.lang.get('refresh', 'Aggiorna'), 
                  command=self._load_translations).pack(side=tk.LEFT, padx=5)
        
        # ===== SEZIONE INFERIORE: UTENTI AUTORIZZATI =====
        authorized_frame = ttk.LabelFrame(main_paned, text=self.lang.get('authorized_users', 'Utenti Autorizzati'), padding=10)
        main_paned.add(authorized_frame, weight=1)
        
        # Frame Treeview utenti autorizzati
        auth_tree_frame = ttk.Frame(authorized_frame)
        auth_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        auth_vsb = ttk.Scrollbar(auth_tree_frame, orient=tk.VERTICAL)
        auth_hsb = ttk.Scrollbar(auth_tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview utenti autorizzati
        self.authorized_tree = ttk.Treeview(
            auth_tree_frame,
            columns=('AuthorizedUsedId', 'Employee', 'DateIn', 'DateOut'),
            show='headings',
            yscrollcommand=auth_vsb.set,
            xscrollcommand=auth_hsb.set
        )
        
        auth_vsb.config(command=self.authorized_tree.yview)
        auth_hsb.config(command=self.authorized_tree.xview)
        
        # Configurazione colonne
        self.authorized_tree.heading('AuthorizedUsedId', text='ID')
        self.authorized_tree.heading('Employee', text=self.lang.get('employee', 'Dipendente'))
        self.authorized_tree.heading('DateIn', text=self.lang.get('date_in', 'Data Inizio'))
        self.authorized_tree.heading('DateOut', text=self.lang.get('date_out', 'Data Fine'))
        
        self.authorized_tree.column('AuthorizedUsedId', width=80, anchor=tk.CENTER)
        self.authorized_tree.column('Employee', width=300)
        self.authorized_tree.column('DateIn', width=150, anchor=tk.CENTER)
        self.authorized_tree.column('DateOut', width=150, anchor=tk.CENTER)
        
        # Layout treeview e scrollbars
        self.authorized_tree.grid(row=0, column=0, sticky='nsew')
        auth_vsb.grid(row=0, column=1, sticky='ns')
        auth_hsb.grid(row=1, column=0, sticky='ew')
        
        auth_tree_frame.grid_rowconfigure(0, weight=1)
        auth_tree_frame.grid_columnconfigure(0, weight=1)
    
    def _load_translations(self):
        """Carica tutte le traduzioni dal database"""
        # Pulisci treeview
        for item in self.translations_tree.get_children():
            self.translations_tree.delete(item)
        
        query = """
        SELECT [ID], [LanguageCode], [TranslationKey], [TranslationValue], [MenuValue]
        FROM [Traceability_RS].[dbo].[AppTranslations]
        ORDER BY [TranslationKey], [LanguageCode]
        """
        
        try:
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()
            
            for row in rows:
                self.translations_tree.insert('', tk.END, values=(
                    row.ID,
                    row.LanguageCode,
                    row.TranslationKey,
                    row.TranslationValue,
                    row.MenuValue if row.MenuValue else ''
                ))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_error', 'Errore caricamento')}: {str(e)}",
                parent=self
            )
    
    def _apply_filters(self):
        """Applica i filtri alle traduzioni"""
        # Pulisci treeview
        for item in self.translations_tree.get_children():
            self.translations_tree.delete(item)
        
        # Costruisci query con filtri
        query = """
        SELECT [ID], [LanguageCode], [TranslationKey], [TranslationValue], [MenuValue]
        FROM [Traceability_RS].[dbo].[AppTranslations]
        WHERE 1=1
        """
        params = []
        
        if self.filter_language.get():
            query += " AND [LanguageCode] = ?"
            params.append(self.filter_language.get())
        
        if self.filter_key.get():
            query += " AND [TranslationKey] LIKE ?"
            params.append(f"%{self.filter_key.get()}%")
        
        if self.filter_value.get():
            query += " AND [TranslationValue] LIKE ?"
            params.append(f"%{self.filter_value.get()}%")
        
        if self.filter_menu.get():
            query += " AND [MenuValue] LIKE ?"
            params.append(f"%{self.filter_menu.get()}%")
        
        query += " ORDER BY [TranslationKey], [LanguageCode]"
        
        try:
            self.db.cursor.execute(query, params)
            rows = self.db.cursor.fetchall()
            
            for row in rows:
                self.translations_tree.insert('', tk.END, values=(
                    row.ID,
                    row.LanguageCode,
                    row.TranslationKey,
                    row.TranslationValue,
                    row.MenuValue if row.MenuValue else ''
                ))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('filter_error', 'Errore applicazione filtri')}: {str(e)}",
                parent=self
            )
    
    def _reset_filters(self):
        """Reset tutti i filtri"""
        self.filter_language.set('')
        self.filter_key.set('')
        self.filter_value.set('')
        self.filter_menu.set('')
        self._load_translations()
    
    def _on_translation_select(self, event):
        """Gestisce la selezione di una traduzione"""
        selection = self.translations_tree.selection()
        if not selection:
            # Pulisci utenti autorizzati
            for item in self.authorized_tree.get_children():
                self.authorized_tree.delete(item)
            return
        
        # Ottieni TranslationKey selezionata
        item = self.translations_tree.item(selection[0])
        values = item['values']
        translation_key = values[2]  # TranslationKey è la terza colonna
        
        # Carica utenti autorizzati
        self._load_authorized_users(translation_key)
    
    def _load_authorized_users(self, translation_key: str):
        """Carica gli utenti autorizzati per una specifica TranslationKey"""
        # Pulisci treeview
        for item in self.authorized_tree.get_children():
            self.authorized_tree.delete(item)
        
        query = """
        SELECT TOP (1000) 
            [AuthorizedUsedId],
            [TranslationKey],
            a.[EmployeeHireHistoryId],
            e.EmployeeName + ' ' + e.EmployeeSurname as [Employee],
            a.[DateIn],
            a.[DateOut]
        FROM [Traceability_RS].[dbo].[AutorizedUsers] a 
        INNER JOIN employee.dbo.EmployeeHireHistory h ON h.EmployeeHireHistoryId = a.EmployeeHireHistoryId 
        INNER JOIN employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
        WHERE a.[TranslationKey] = ?
        ORDER BY a.[TranslationKey]
        """
        
        try:
            self.db.cursor.execute(query, (translation_key,))
            rows = self.db.cursor.fetchall()
            
            for row in rows:
                self.authorized_tree.insert('', tk.END, values=(
                    row.AuthorizedUsedId,
                    row.Employee,
                    row.DateIn.strftime('%Y-%m-%d %H:%M:%S') if row.DateIn else '',
                    row.DateOut.strftime('%Y-%m-%d %H:%M:%S') if row.DateOut else ''
                ))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_authorized_error', 'Errore caricamento utenti autorizzati')}: {str(e)}",
                parent=self
            )
    
    def _add_translation(self):
        """Apre dialog per aggiungere una nuova traduzione"""
        dialog = TranslationDialog(self, self.db, self.lang, mode='add')
        self.wait_window(dialog)
        
        if dialog.result:
            self._load_translations()
    
    def _edit_translation(self):
        """Apre dialog per modificare la traduzione selezionata"""
        selection = self.translations_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_translation', 'Seleziona una traduzione da modificare'),
                parent=self
            )
            return
        
        # Ottieni dati traduzione selezionata
        item = self.translations_tree.item(selection[0])
        values = item['values']
        
        translation_data = {
            'ID': values[0],
            'LanguageCode': values[1],
            'TranslationKey': values[2],
            'TranslationValue': values[3],
            'MenuValue': values[4] if values[4] else None
        }
        
        dialog = TranslationDialog(self, self.db, self.lang, mode='edit', data=translation_data)
        self.wait_window(dialog)
        
        if dialog.result:
            self._load_translations()
    
    def _delete_translation(self):
        """Elimina la traduzione selezionata"""
        selection = self.translations_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_translation', 'Seleziona una traduzione da eliminare'),
                parent=self
            )
            return
        
        # Ottieni ID traduzione
        item = self.translations_tree.item(selection[0])
        translation_id = item['values'][0]
        translation_key = item['values'][2]
        
        # Conferma eliminazione
        confirm = messagebox.askyesno(
            self.lang.get('confirm_delete', 'Conferma Eliminazione'),
            f"{self.lang.get('confirm_delete_translation', 'Eliminare la traduzione')} '{translation_key}'?",
            parent=self
        )
        
        if not confirm:
            return
        
        query = "DELETE FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [ID] = ?"
        
        try:
            self.db.cursor.execute(query, (translation_id,))
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('translation_deleted', 'Traduzione eliminata con successo'),
                parent=self
            )
            
            self._load_translations()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('delete_error', 'Errore eliminazione')}: {str(e)}",
                parent=self
            )


class TranslationDialog(tk.Toplevel):
    """Dialog per aggiungere/modificare una traduzione"""
    
    def __init__(self, parent, db, lang, mode='add', data=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.mode = mode
        self.data = data
        self.result = False
        
        title = self.lang.get('add_translation', 'Aggiungi Traduzione') if mode == 'add' else self.lang.get('edit_translation', 'Modifica Traduzione')
        self.title(title)
        self.geometry('500x300')
        self.resizable(False, False)
        
        self._create_widgets()
        
        # Se mode edit, popola i campi
        if mode == 'edit' and data:
            self._populate_fields()
        
        # Centra la finestra
        self.transient(parent)
        self.grab_set()
    
    def _create_widgets(self):
        """Crea i widget del dialog"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # LanguageCode
        ttk.Label(main_frame, text=self.lang.get('language_code', 'Lingua:')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar()
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var, 
                                      values=['it', 'ro', 'de', 'en', 'sv'], state='readonly', width=30)
        language_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # TranslationKey
        ttk.Label(main_frame, text=self.lang.get('translation_key', 'Chiave:')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.key_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.key_var, width=30).grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # TranslationValue
        ttk.Label(main_frame, text=self.lang.get('translation_value', 'Valore:')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.value_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.value_var, width=30).grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # MenuValue
        ttk.Label(main_frame, text=self.lang.get('menu_value', 'Menu (opzionale):')).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.menu_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.menu_var, width=30).grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Pulsanti
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text=self.lang.get('save', 'Salva'), 
                  command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text=self.lang.get('cancel', 'Annulla'), 
                  command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
    
    def _populate_fields(self):
        """Popola i campi con i dati esistenti (mode edit)"""
        self.language_var.set(self.data['LanguageCode'])
        self.key_var.set(self.data['TranslationKey'])
        self.value_var.set(self.data['TranslationValue'])
        if self.data['MenuValue']:
            self.menu_var.set(self.data['MenuValue'])
    
    def _save(self):
        """Salva la traduzione"""
        # Validazione
        if not self.language_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('language_required', 'Seleziona una lingua'),
                parent=self
            )
            return
        
        if not self.key_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('key_required', 'Inserisci una chiave'),
                parent=self
            )
            return
        
        if not self.value_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('value_required', 'Inserisci un valore'),
                parent=self
            )
            return
        
        try:
            if self.mode == 'add':
                # INSERT
                query = """
                INSERT INTO [Traceability_RS].[dbo].[AppTranslations] 
                ([LanguageCode], [TranslationKey], [TranslationValue], [MenuValue])
                VALUES (?, ?, ?, ?)
                """
                params = (
                    self.language_var.get(),
                    self.key_var.get().strip(),
                    self.value_var.get().strip(),
                    self.menu_var.get().strip() if self.menu_var.get().strip() else None
                )
            else:
                # UPDATE
                query = """
                UPDATE [Traceability_RS].[dbo].[AppTranslations]
                SET [LanguageCode] = ?,
                    [TranslationKey] = ?,
                    [TranslationValue] = ?,
                    [MenuValue] = ?
                WHERE [ID] = ?
                """
                params = (
                    self.language_var.get(),
                    self.key_var.get().strip(),
                    self.value_var.get().strip(),
                    self.menu_var.get().strip() if self.menu_var.get().strip() else None,
                    self.data['ID']
                )
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            
            self.result = True
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('translation_saved', 'Traduzione salvata con successo'),
                parent=self
            )
            self.destroy()
            
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('save_error', 'Errore salvataggio')}: {str(e)}",
                parent=self
            )


def open_translations_manager(parent, db, lang):
    """Apre la finestra di gestione traduzioni"""
    TranslationsManagerWindow(parent, db, lang)
