# settings_gui.py
"""
Modulo per la gestione delle impostazioni email.
Gestisce la tabella dbo.Settings con operazioni CRUD.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def open_settings_email(parent, db, lang, user_name):
    """Apre la finestra di gestione impostazioni email."""
    SettingsEmailWindow(parent, db, lang, user_name)


class SettingsEmailWindow(tk.Toplevel):
    """Finestra per gestire le impostazioni email (tabella dbo.Settings)."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"SettingsEmailWindow: Apertura finestra gestione impostazioni (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('settings_email_window_title', 'Gestione Impostazioni Email'))
        self.geometry("1000x600")
        self.transient(parent)
        self.grab_set()
        
        self.search_var = tk.StringVar()
        
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # Frame ricerca
        search_frame = ttk.LabelFrame(self, text=self.lang.get('search_label', 'Cerca'), padding="10")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text=self.lang.get('search_label', 'Cerca:')).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self._on_search())
        
        ttk.Button(search_frame, text=self.lang.get('search_button', 'Cerca'),
                  command=self._on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text=self.lang.get('clear_button', 'Pulisci'),
                  command=self._clear_search).pack(side=tk.LEFT, padx=5)
        
        # Frame treeview
        tree_frame = ttk.Frame(self, padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('id', 'attribute', 'value', 'last_check', 'name')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('attribute', text=self.lang.get('attribute_label', 'Attributo'))
        self.tree.heading('value', text=self.lang.get('value_label', 'Valore'))
        self.tree.heading('last_check', text=self.lang.get('last_check_label', 'Ultimo Controllo'))
        self.tree.heading('name', text=self.lang.get('name_label', 'Nome'))
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('attribute', width=200)
        self.tree.column('value', width=250)
        self.tree.column('last_check', width=150, anchor='center')
        self.tree.column('name', width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click
        self.tree.bind('<Double-1>', lambda e: self._on_edit_setting())
        
        # Frame pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text=self.lang.get('add_button', 'Aggiungi'),
                  command=self._on_add_setting).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('edit_button', 'Modifica'),
                  command=self._on_edit_setting).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('delete_button', 'Elimina'),
                  command=self._on_delete_setting).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text=self.lang.get('refresh_button', 'Aggiorna'),
                  command=self._load_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('close_button', 'Chiudi'),
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_settings(self):
        """Carica tutte le impostazioni."""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT IDSettings, Atribute, Value, LastCheck, Name
            FROM [Traceability_RS].[dbo].[Settings]
            ORDER BY Atribute
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                setting_id, attribute, value, last_check, name = row
                last_check_str = last_check.strftime('%Y-%m-%d %H:%M:%S') if last_check else ''
                name_str = name if name else ''
                
                self.tree.insert('', tk.END, iid=setting_id,
                               values=(setting_id, attribute, value, last_check_str, name_str))
        
        except Exception as e:
            logger.error(f"Errore caricamento impostazioni: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento impostazioni:\n{e}")
    
    def _on_search(self):
        """Cerca impostazioni per Attribute o Value."""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self._load_settings()
            return
        
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT IDSettings, Atribute, Value, LastCheck, Name
            FROM [Traceability_RS].[dbo].[Settings]
            WHERE Atribute LIKE ? OR Value LIKE ?
            ORDER BY Atribute
            """
            params = [f'%{search_term}%', f'%{search_term}%']
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                setting_id, attribute, value, last_check, name = row
                last_check_str = last_check.strftime('%Y-%m-%d %H:%M:%S') if last_check else ''
                name_str = name if name else ''
                
                self.tree.insert('', tk.END, iid=setting_id,
                               values=(setting_id, attribute, value, last_check_str, name_str))
        
        except Exception as e:
            logger.error(f"Errore ricerca impostazioni: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore ricerca:\n{e}")
    
    def _clear_search(self):
        """Pulisce la ricerca e ricarica tutte le impostazioni."""
        self.search_var.set('')
        self._load_settings()
    
    def _on_add_setting(self):
        """Apre il dialog per aggiungere una nuova impostazione."""
        AddEditSettingDialog(self, self.db, self.lang, callback=self._load_settings)
    
    def _on_edit_setting(self):
        """Apre il dialog per modificare l'impostazione selezionata."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('warning_no_selection', 'Seleziona un\'impostazione'))
            return
        
        setting_id = int(selected)
        AddEditSettingDialog(self, self.db, self.lang, setting_id=setting_id,
                           callback=self._load_settings)
    
    def _on_delete_setting(self):
        """Elimina l'impostazione selezionata."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('warning_no_selection', 'Seleziona un\'impostazione'))
            return
        
        if not messagebox.askyesno(self.lang.get('confirm_title', 'Conferma'),
                                  self.lang.get('confirm_delete_setting', 'Confermi eliminazione dell\'impostazione?')):
            return
        
        setting_id = int(selected)
        
        try:
            cursor = self.db.conn.cursor()
            query = "DELETE FROM [Traceability_RS].[dbo].[Settings] WHERE IDSettings = ?"
            cursor.execute(query, setting_id)
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('setting_deleted_success', 'Impostazione eliminata con successo'))
            self._load_settings()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore eliminazione impostazione: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore eliminazione:\n{e}")


class AddEditSettingDialog(tk.Toplevel):
    """Dialog per aggiungere o modificare un'impostazione."""
    
    def __init__(self, parent, db, lang, setting_id=None, callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.setting_id = setting_id
        self.callback = callback
        
        self.is_edit = setting_id is not None
        title = self.lang.get('edit_setting_title', 'Modifica Impostazione') if self.is_edit else \
                self.lang.get('add_setting_title', 'Aggiungi Impostazione')
        self.title(title)
        self.geometry("500x300")
        self.transient(parent)
        self.grab_set()
        
        self.attribute_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.last_check_var = tk.StringVar()
        
        self._create_widgets()
        
        if self.is_edit:
            self._load_setting_data()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        
        # Attribute
        ttk.Label(frame, text=self.lang.get('attribute_label', 'Attributo:') + ' *').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        attribute_entry = ttk.Entry(frame, textvariable=self.attribute_var)
        attribute_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        attribute_entry.focus()
        
        # Value
        ttk.Label(frame, text=self.lang.get('value_label', 'Valore:') + ' *').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        value_entry = ttk.Entry(frame, textvariable=self.value_var)
        value_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Name
        ttk.Label(frame, text=self.lang.get('name_label', 'Nome:')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, textvariable=self.name_var)
        name_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # LastCheck (display only)
        ttk.Label(frame, text=self.lang.get('last_check_label', 'Ultimo Controllo:')).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        last_check_label = ttk.Label(frame, textvariable=self.last_check_var, foreground='gray')
        last_check_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Note
        ttk.Label(frame, text='* ' + self.lang.get('required_fields', 'Campi obbligatori')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Info LastCheck
        info_text = self.lang.get('last_check_auto_update', 'Il campo "Ultimo Controllo" verrà aggiornato automaticamente al salvataggio')
        ttk.Label(frame, text=info_text, foreground='blue', font=('TkDefaultFont', 8)).grid(
            row=5, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Pulsanti
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=1, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(button_frame, text=self.lang.get('save_button', 'Salva'),
                  command=self._validate_and_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', 'Annulla'),
                  command=self.destroy).pack(side=tk.LEFT)
    
    def _load_setting_data(self):
        """Carica i dati dell'impostazione esistente."""
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT Atribute, Value, Name, LastCheck
            FROM [Traceability_RS].[dbo].[Settings]
            WHERE IDSettings = ?
            """
            cursor.execute(query, self.setting_id)
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                attribute, value, name, last_check = row
                self.attribute_var.set(attribute if attribute else '')
                self.value_var.set(value if value else '')
                self.name_var.set(name if name else '')
                if last_check:
                    self.last_check_var.set(last_check.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    self.last_check_var.set('N/D')
        
        except Exception as e:
            logger.error(f"Errore caricamento dati impostazione: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento dati:\n{e}")
            self.destroy()
    
    def _validate_and_save(self):
        """Valida i dati e salva l'impostazione."""
        # Validazione Attribute
        attribute = self.attribute_var.get().strip()
        if not attribute:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               self.lang.get('error_no_attribute', 'Inserisci un attributo'))
            return
        
        # Validazione Value
        value = self.value_var.get().strip()
        if not value:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               self.lang.get('error_no_value', 'Inserisci un valore'))
            return
        
        # Name opzionale
        name = self.name_var.get().strip()
        name = name if name else None
        
        # Salva nel database
        try:
            cursor = self.db.conn.cursor()
            
            if self.is_edit:
                query = """
                UPDATE [Traceability_RS].[dbo].[Settings]
                SET Atribute = ?,
                    Value = ?,
                    Name = ?,
                    LastCheck = GETDATE()
                WHERE IDSettings = ?
                """
                cursor.execute(query, attribute, value, name, self.setting_id)
            else:
                query = """
                INSERT INTO [Traceability_RS].[dbo].[Settings]
                (Atribute, Value, Name, LastCheck)
                VALUES (?, ?, ?, GETDATE())
                """
                cursor.execute(query, attribute, value, name)
            
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('setting_saved_success', 'Impostazione salvata con successo'))
            
            if self.callback:
                self.callback()
            
            self.destroy()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore salvataggio impostazione: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore salvataggio:\n{e}")
