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

        ttk.Button(button_frame,
                  text=self.lang.get('manage_email_addresses_button', '📧 Gestione Indirizzi Email'),
                  command=self._on_manage_addresses).pack(side=tk.LEFT, padx=15)

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
    
    def _on_manage_addresses(self):
        """Apre il gestore avanzato degli indirizzi email (correggi/elimina su piu' chiavi)."""
        EmailAddressManagerDialog(self, self.db, self.lang, callback=self._load_settings)

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


# ─────────────────────────────────────────────────────────────────────────────
#  Helper parsing indirizzi
# ─────────────────────────────────────────────────────────────────────────────
def _parse_addresses(value):
    """Spezza un Value in indirizzi (separatori ';' o ','), trim, scartando i vuoti."""
    if not value:
        return []
    raw = str(value).replace(',', ';')
    return [tok.strip() for tok in raw.split(';') if tok.strip()]


def _join_addresses(addrs):
    """Riunisce gli indirizzi con '; ', rimuovendo i duplicati (case-insensitive) e i vuoti."""
    seen, out = set(), []
    for a in addrs:
        a = (a or '').strip()
        if not a:
            continue
        k = a.lower()
        if k not in seen:
            seen.add(k)
            out.append(a)
    return '; '.join(out)


class EmailAddressManagerDialog(tk.Toplevel):
    """Gestione avanzata degli indirizzi email su piu' chiavi (atribute).

    Si filtra per chiave (es. 'Sys_email'): vengono caricate tutte le righe di
    Settings corrispondenti, ne vengono estratti gli indirizzi distinti (separati
    da ';'/','), e si puo' CORREGGERE o ELIMINARE un indirizzo su TUTTE le righe
    che lo contengono in un colpo solo.
    """

    def __init__(self, parent, db, lang, callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.callback = callback
        self._rows = []          # [(id, atribute, value)] caricate dal filtro
        self._addr_map = {}      # email_lower -> {'display':..., 'ids':set, 'attrs':[...]}
        self._id_attr = {}       # IDSettings -> atribute

        self.title(self.lang.get('email_addr_mgr_title', 'Gestione Indirizzi Email'))
        self.geometry('960x720')
        self.transient(parent)
        self.grab_set()

        self.filter_var = tk.StringVar(value='Sys_email')
        self.addr_filter_var = tk.StringVar(value='')
        self.new_addr_var = tk.StringVar()
        self.status_var = tk.StringVar(value='')

        self._create_widgets()
        self._load()

    def _create_widgets(self):
        # Filtro
        flt = ttk.LabelFrame(self, text=self.lang.get('email_addr_mgr_filter',
                                                      'Filtro chiave (atribute)'), padding=10)
        flt.pack(fill=tk.X, padx=10, pady=(10, 5))
        ttk.Label(flt, text=self.lang.get('email_addr_mgr_key', 'Chiave contiene:')).pack(side=tk.LEFT, padx=(0, 6))
        e = ttk.Entry(flt, textvariable=self.filter_var, width=24)
        e.pack(side=tk.LEFT, padx=(0, 6))
        e.bind('<Return>', lambda ev: self._load())
        ttk.Button(flt, text=self.lang.get('email_addr_mgr_load', 'Carica'),
                   command=self._load).pack(side=tk.LEFT, padx=4)
        # Filtro per indirizzo (in memoria, sulla lista gia' caricata)
        ttk.Label(flt, text=self.lang.get('email_addr_mgr_addr_filter', 'Indirizzo contiene:')).pack(
            side=tk.LEFT, padx=(16, 6))
        ae = ttk.Entry(flt, textvariable=self.addr_filter_var, width=26)
        ae.pack(side=tk.LEFT, padx=(0, 6))
        ae.bind('<KeyRelease>', lambda ev: self._refresh_address_list())

        # Lista indirizzi distinti
        body = ttk.LabelFrame(self, text=self.lang.get('email_addr_mgr_addresses',
                                                       'Indirizzi trovati'), padding=8)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        cols = ('email', 'count', 'attrs')
        self.tree = ttk.Treeview(body, columns=cols, show='headings', selectmode='browse', height=9)
        self.tree.heading('email', text=self.lang.get('email_addr_mgr_col_email', 'Indirizzo email'))
        self.tree.heading('count', text=self.lang.get('email_addr_mgr_col_count', 'N. righe'))
        self.tree.heading('attrs', text=self.lang.get('email_addr_mgr_col_keys', 'Chiavi (atribute)'))
        self.tree.column('email', width=280, anchor='w')
        self.tree.column('count', width=70, anchor='center')
        self.tree.column('attrs', width=520, anchor='w')
        vsb = ttk.Scrollbar(body, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Co-occorrenze: altri indirizzi presenti nelle stesse chiavi dell'indirizzo selezionato
        co = ttk.LabelFrame(self, text=self.lang.get('email_addr_mgr_cooccur',
                                                     'Altri indirizzi nelle stesse chiavi'), padding=8)
        co.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        co_cols = ('email', 'shared', 'keys')
        self.co_tree = ttk.Treeview(co, columns=co_cols, show='headings', selectmode='browse', height=7)
        self.co_tree.heading('email', text=self.lang.get('email_addr_mgr_col_email', 'Indirizzo email'))
        self.co_tree.heading('shared', text=self.lang.get('email_addr_mgr_col_shared', 'Chiavi in comune'))
        self.co_tree.heading('keys', text=self.lang.get('email_addr_mgr_col_keys', 'Chiavi (atribute)'))
        self.co_tree.column('email', width=280, anchor='w')
        self.co_tree.column('shared', width=110, anchor='center')
        self.co_tree.column('keys', width=480, anchor='w')
        co_vsb = ttk.Scrollbar(co, orient=tk.VERTICAL, command=self.co_tree.yview)
        self.co_tree.configure(yscroll=co_vsb.set)
        self.co_tree.grid(row=0, column=0, sticky='nsew')
        co_vsb.grid(row=0, column=1, sticky='ns')
        co.grid_rowconfigure(0, weight=1)
        co.grid_columnconfigure(0, weight=1)
        # doppio clic su una co-occorrenza: la seleziona nella lista principale
        self.co_tree.bind('<Double-1>', self._on_cooccur_activate)

        # Azioni
        act = ttk.LabelFrame(self, text=self.lang.get('email_addr_mgr_actions',
                                                      'Azioni sull\'indirizzo selezionato'), padding=8)
        act.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(act, text=self.lang.get('email_addr_mgr_new', 'Nuovo indirizzo:')).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Entry(act, textvariable=self.new_addr_var, width=34).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(act, text=self.lang.get('email_addr_mgr_correct', '✏ Correggi su tutte'),
                   command=self._correct).pack(side=tk.LEFT, padx=4)
        ttk.Button(act, text=self.lang.get('email_addr_mgr_delete', '🗑 Elimina da tutte'),
                   command=self._delete).pack(side=tk.LEFT, padx=4)

        # Status + chiudi
        bottom = ttk.Frame(self, padding=(10, 4))
        bottom.pack(fill=tk.X)
        ttk.Label(bottom, textvariable=self.status_var, foreground='gray').pack(side=tk.LEFT)
        ttk.Button(bottom, text=self.lang.get('close_button', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------ #
    def _load(self):
        key = self.filter_var.get().strip()
        for it in self.tree.get_children():
            self.tree.delete(it)
        self._rows = []
        self._addr_map = {}
        try:
            cursor = self.db.conn.cursor()
            if key:
                cursor.execute(
                    "SELECT IDSettings, Atribute, Value FROM [Traceability_RS].[dbo].[Settings] "
                    "WHERE Atribute LIKE ? ORDER BY Atribute", (f'%{key}%',))
            else:
                cursor.execute(
                    "SELECT IDSettings, Atribute, Value FROM [Traceability_RS].[dbo].[Settings] "
                    "ORDER BY Atribute")
            self._rows = [(r[0], r[1], r[2]) for r in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            logger.error(f"EmailAddressManager _load: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 f"Errore caricamento:\n{e}", parent=self)
            return

        self._id_attr = {}
        for sid, attr, value in self._rows:
            self._id_attr[sid] = attr
            for addr in _parse_addresses(value):
                k = addr.lower()
                entry = self._addr_map.get(k)
                if entry is None:
                    self._addr_map[k] = {'display': addr, 'ids': {sid}, 'attrs': [attr]}
                else:
                    entry['ids'].add(sid)
                    if attr not in entry['attrs']:
                        entry['attrs'].append(attr)

        self.new_addr_var.set('')
        self._refresh_address_list()

    def _refresh_address_list(self):
        """Popola la lista indirizzi applicando il filtro per indirizzo (in memoria)."""
        for it in self.tree.get_children():
            self.tree.delete(it)
        for it in self.co_tree.get_children():
            self.co_tree.delete(it)
        needle = self.addr_filter_var.get().strip().lower()
        shown = 0
        for k in sorted(self._addr_map.keys()):
            if needle and needle not in k:
                continue
            entry = self._addr_map[k]
            attrs_txt = ', '.join(entry['attrs'])
            if len(attrs_txt) > 100:
                attrs_txt = attrs_txt[:100] + '...'
            self.tree.insert('', tk.END, iid=k,
                             values=(entry['display'], len(entry['ids']), attrs_txt))
            shown += 1
        self.status_var.set(
            self.lang.get('email_addr_mgr_loaded',
                          '{0} righe, {1} indirizzi distinti').format(
                len(self._rows), len(self._addr_map))
            + (f"  |  {self.lang.get('email_addr_mgr_shown', 'mostrati')}: {shown}" if needle else ''))

    def _populate_cooccurrences(self, addr_key):
        """Mostra gli altri indirizzi che condividono almeno una chiave con addr_key."""
        for it in self.co_tree.get_children():
            self.co_tree.delete(it)
        entry = self._addr_map.get(addr_key)
        if not entry:
            return
        a_ids = entry['ids']
        results = []
        for k2, e2 in self._addr_map.items():
            if k2 == addr_key:
                continue
            shared_ids = a_ids & e2['ids']
            if shared_ids:
                shared_keys = sorted({self._id_attr.get(i, '') for i in shared_ids})
                results.append((e2['display'], len(shared_ids), shared_keys))
        # ordina per numero di chiavi in comune (desc), poi alfabetico
        results.sort(key=lambda r: (-r[1], r[0].lower()))
        for display, n_shared, shared_keys in results:
            keys_txt = ', '.join(shared_keys)
            if len(keys_txt) > 100:
                keys_txt = keys_txt[:100] + '...'
            self.co_tree.insert('', tk.END, iid=display.lower(),
                                values=(display, n_shared, keys_txt))

    def _on_cooccur_activate(self, _event=None):
        """Doppio clic su una co-occorrenza: la seleziona nella lista principale."""
        sel = self.co_tree.selection()
        if not sel:
            return
        target = sel[0]
        # azzera il filtro indirizzo se nasconde il target, poi seleziona
        if self.addr_filter_var.get().strip() and self.addr_filter_var.get().strip().lower() not in target:
            self.addr_filter_var.set('')
            self._refresh_address_list()
        if self.tree.exists(target):
            self.tree.selection_set(target)
            self.tree.focus(target)
            self.tree.see(target)

    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if sel:
            self.new_addr_var.set(self._addr_map.get(sel[0], {}).get('display', ''))
            self._populate_cooccurrences(sel[0])

    def _selected_key(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(self.lang.get('info_title', 'Info'),
                                self.lang.get('email_addr_mgr_select', 'Seleziona un indirizzo dalla lista.'),
                                parent=self)
            return None
        return sel[0]

    def _apply(self, old_key, new_addr):
        """Applica la sostituzione/eliminazione su tutte le righe che contengono old_key.
        new_addr=None -> eliminazione. Ritorna il numero di righe modificate."""
        changed = 0
        try:
            cursor = self.db.conn.cursor()
            for sid, attr, value in self._rows:
                addrs = _parse_addresses(value)
                if not any(a.lower() == old_key for a in addrs):
                    continue
                new_list = []
                for a in addrs:
                    if a.lower() == old_key:
                        if new_addr is not None:
                            new_list.append(new_addr)
                        # eliminazione: salta
                    else:
                        new_list.append(a)
                new_value = _join_addresses(new_list)
                cursor.execute(
                    "UPDATE [Traceability_RS].[dbo].[Settings] "
                    "SET Value = ?, LastCheck = GETDATE() WHERE IDSettings = ?",
                    (new_value, sid))
                changed += 1
            self.db.conn.commit()
            cursor.close()
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"EmailAddressManager _apply: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 f"Errore aggiornamento:\n{e}", parent=self)
            return -1
        return changed

    def _correct(self):
        key = self._selected_key()
        if key is None:
            return
        old_display = self._addr_map[key]['display']
        new_addr = self.new_addr_var.get().strip()
        if not new_addr or '@' not in new_addr:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('email_addr_mgr_invalid', 'Inserire un indirizzo email valido.'),
                                   parent=self)
            return
        if new_addr.lower() == key:
            return
        n_rows = len(self._addr_map[key]['ids'])
        if not messagebox.askyesno(
            self.lang.get('confirm_title', 'Conferma'),
            self.lang.get('email_addr_mgr_confirm_correct',
                          'Sostituire "{0}" con "{1}" in {2} righe?').format(old_display, new_addr, n_rows),
            parent=self):
            return
        changed = self._apply(key, new_addr)
        if changed >= 0:
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                                self.lang.get('email_addr_mgr_corrected',
                                              'Indirizzo aggiornato in {0} righe.').format(changed),
                                parent=self)
            self._load()
            if self.callback:
                self.callback()

    def _delete(self):
        key = self._selected_key()
        if key is None:
            return
        old_display = self._addr_map[key]['display']
        n_rows = len(self._addr_map[key]['ids'])
        if not messagebox.askyesno(
            self.lang.get('confirm_title', 'Conferma'),
            self.lang.get('email_addr_mgr_confirm_delete',
                          'Eliminare "{0}" da {1} righe?').format(old_display, n_rows),
            parent=self):
            return
        changed = self._apply(key, None)
        if changed >= 0:
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                                self.lang.get('email_addr_mgr_deleted',
                                              'Indirizzo eliminato da {0} righe.').format(changed),
                                parent=self)
            self._load()
            if self.callback:
                self.callback()
