# fixture_gui.py
"""
Modulo per la gestione delle fixture (IC e FCT).
Contiene finestre per:
- Gestione regole fixture
- Gestione documenti fixture
- Assegnazione prodotti a fixture
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


def open_fixture_rules(parent, db, lang, user_name):
    """Apre la finestra di gestione regole fixture."""
    FixtureRulesWindow(parent, db, lang, user_name)


def open_assign_products_to_fixtures(parent, db, lang, user_name):
    """Apre la finestra di assegnazione prodotti a fixture."""
    AssignProductsToFixturesWindow(parent, db, lang, user_name)


class FixtureRulesWindow(tk.Toplevel):
    """Finestra per gestire le regole di manutenzione delle fixture."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"FixtureRulesWindow: Apertura finestra gestione regole fixture (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('fixture_rules_window_title', 'Gestione Regole Fixture'))
        self.geometry("900x600")
        self.transient(parent)
        self.grab_set()
        
        self.equipment_types_data = {}  # ID -> Name mapping
        self.selected_type_var = tk.StringVar()
        
        self._create_widgets()
        self._load_equipment_types()
        self._load_rules()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # Frame filtro
        filter_frame = ttk.LabelFrame(self, text=self.lang.get('filter_label', 'Filtro'), padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text=self.lang.get('equipment_type_label', 'Tipo Equipaggiamento:')).pack(side=tk.LEFT, padx=5)
        self.type_combo = ttk.Combobox(filter_frame, textvariable=self.selected_type_var, state='readonly', width=30)
        self.type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text=self.lang.get('filter_button', 'Filtra'), 
                  command=self._load_rules).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text=self.lang.get('clear_filter_button', 'Pulisci'), 
                  command=self._clear_filter).pack(side=tk.LEFT, padx=5)
        
        # Frame treeview
        tree_frame = ttk.Frame(self, padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('id', 'type', 'cycles', 'date_out', 'docs_count')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('type', text=self.lang.get('equipment_type_label', 'Tipo'))
        self.tree.heading('cycles', text=self.lang.get('number_of_cycles_label', 'Cicli'))
        self.tree.heading('date_out', text=self.lang.get('date_out_label', 'Data Scadenza'))
        self.tree.heading('docs_count', text=self.lang.get('documents_count_label', 'N° Documenti'))
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('type', width=200)
        self.tree.column('cycles', width=100, anchor='center')
        self.tree.column('date_out', width=120, anchor='center')
        self.tree.column('docs_count', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click
        self.tree.bind('<Double-1>', self._on_row_double_click)
        
        # Frame pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text=self.lang.get('add_button', 'Aggiungi'), 
                  command=self._on_add_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('edit_button', 'Modifica'), 
                  command=self._on_edit_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('delete_button', 'Elimina'), 
                  command=self._on_delete_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('manage_docs_button', 'Gestisci Documenti'), 
                  command=self._on_manage_documents).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text=self.lang.get('refresh_button', 'Aggiorna'), 
                  command=self._load_rules).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('close_button', 'Chiudi'), 
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_equipment_types(self):
        """Carica i tipi di equipaggiamento di test."""
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT EquipmentTypeId, EquipmentType 
            FROM [Traceability_RS].[eqp].[EquipmentTypes] 
            WHERE IsTest = 1
            ORDER BY EquipmentType
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            self.equipment_types_data = {row[0]: row[1] for row in rows}
            self.type_combo['values'] = [''] + list(self.equipment_types_data.values())
        except Exception as e:
            logger.error(f"Errore caricamento tipi equipaggiamento: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'), 
                               f"Errore caricamento tipi equipaggiamento:\n{e}")
    
    def _clear_filter(self):
        """Pulisce il filtro e ricarica tutte le regole."""
        self.selected_type_var.set('')
        self._load_rules()
    
    def _load_rules(self):
        """Carica le regole fixture con filtro opzionale."""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ottieni filtro
        selected_type_name = self.selected_type_var.get()
        type_id = None
        if selected_type_name:
            type_id = [k for k, v in self.equipment_types_data.items() if v == selected_type_name][0]
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT 
                fr.EquipmentFixtureRuleId,
                fr.EquipmentTypeId,
                et.EquipmentType,
                fr.NumberOfCycles,
                fr.DateOut,
                COUNT(fd.FixtureDocumentId) AS DocsCount
            FROM [Traceability_RS].[eqp].[EquipmentFixtureRules] fr
            INNER JOIN [Traceability_RS].[eqp].[EquipmentTypes] et 
                ON fr.EquipmentTypeId = et.EquipmentTypeId
            LEFT JOIN [Traceability_RS].[eqp].[EquipmentFixtureDocuments] fd
                ON fr.EquipmentFixtureRuleId = fd.EquipmentFixtureRuleId
            WHERE et.IsTest = 1
            """
            
            params = []
            if type_id:
                query += " AND fr.EquipmentTypeId = ?"
                params.append(type_id)
            
            query += """
            GROUP BY fr.EquipmentFixtureRuleId, fr.EquipmentTypeId, et.EquipmentType, 
                     fr.NumberOfCycles, fr.DateOut
            ORDER BY et.EquipmentType, fr.NumberOfCycles
            """
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                rule_id, type_id, type_name, cycles, date_out, docs_count = row
                date_out_str = date_out.strftime('%Y-%m-%d') if date_out else 'N/D'
                
                self.tree.insert('', tk.END, iid=rule_id, 
                               values=(rule_id, type_name, cycles, date_out_str, docs_count))
        
        except Exception as e:
            logger.error(f"Errore caricamento regole fixture: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'), 
                               f"Errore caricamento regole:\n{e}")
    
    def _on_add_rule(self):
        """Apre il dialog per aggiungere una nuova regola."""
        AddEditFixtureRuleDialog(self, self.db, self.lang, self.user_name, 
                                callback=self._load_rules)
    
    def _on_edit_rule(self):
        """Apre il dialog per modificare la regola selezionata."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('warning_no_selection', 'Seleziona una regola'))
            return
        
        rule_id = int(selected)
        AddEditFixtureRuleDialog(self, self.db, self.lang, self.user_name, 
                                rule_id=rule_id, callback=self._load_rules)
    
    def _on_delete_rule(self):
        """Elimina la regola selezionata."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('warning_no_selection', 'Seleziona una regola'))
            return
        
        if not messagebox.askyesno(self.lang.get('confirm_title', 'Conferma'),
                                  self.lang.get('confirm_delete_rule', 'Confermi eliminazione della regola?')):
            return
        
        rule_id = int(selected)
        
        try:
            cursor = self.db.conn.cursor()
            query = "DELETE FROM [Traceability_RS].[eqp].[EquipmentFixtureRules] WHERE EquipmentFixtureRuleId = ?"
            cursor.execute(query, rule_id)
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('rule_deleted_success', 'Regola eliminata con successo'))
            self._load_rules()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore eliminazione regola: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore eliminazione regola:\n{e}")
    
    def _on_row_double_click(self, event):
        """Gestisce il doppio click su una riga."""
        self._on_edit_rule()
    
    def _on_manage_documents(self):
        """Apre la finestra di gestione documenti per la regola selezionata."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('warning_no_selection', 'Seleziona una regola'))
            return
        
        rule_id = int(selected)
        # TODO: Implementare FixtureDocumentsWindow
        messagebox.showinfo("Documenti", f"Gestione documenti per regola ID={rule_id}\n(In sviluppo)")


class AddEditFixtureRuleDialog(tk.Toplevel):
    """Dialog per aggiungere o modificare una regola fixture."""
    
    def __init__(self, parent, db, lang, user_name, rule_id=None, callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.rule_id = rule_id
        self.callback = callback
        
        self.is_edit = rule_id is not None
        title = self.lang.get('edit_fixture_rule_title', 'Modifica Regola Fixture') if self.is_edit else \
                self.lang.get('add_fixture_rule_title', 'Aggiungi Regola Fixture')
        self.title(title)
        self.geometry("450x250")
        self.transient(parent)
        self.grab_set()
        
        self.equipment_types_data = {}
        self.type_var = tk.StringVar()
        self.cycles_var = tk.StringVar()
        self.date_out_var = tk.StringVar()
        
        self._create_widgets()
        self._load_equipment_types()
        
        if self.is_edit:
            self._load_rule_data()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        
        # Tipo equipaggiamento
        ttk.Label(frame, text=self.lang.get('equipment_type_label', 'Tipo Equipaggiamento:') + ' *').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.type_combo = ttk.Combobox(frame, textvariable=self.type_var, state='readonly')
        self.type_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Numero cicli
        ttk.Label(frame, text=self.lang.get('number_of_cycles_label', 'Numero di Cicli:') + ' *').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.cycles_entry = ttk.Entry(frame, textvariable=self.cycles_var)
        self.cycles_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Data scadenza
        ttk.Label(frame, text=self.lang.get('date_out_label', 'Data Scadenza:') + ' (YYYY-MM-DD)').grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(frame, textvariable=self.date_out_var)
        self.date_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Note
        ttk.Label(frame, text='* ' + self.lang.get('required_fields', 'Campi obbligatori')).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Pulsanti
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=1, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(button_frame, text=self.lang.get('save_button', 'Salva'), 
                  command=self._validate_and_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', 'Annulla'), 
                  command=self.destroy).pack(side=tk.LEFT)
    
    def _load_equipment_types(self):
        """Carica i tipi di equipaggiamento di test."""
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT EquipmentTypeId, EquipmentType 
            FROM [Traceability_RS].[eqp].[EquipmentTypes] 
            WHERE IsTest = 1
            ORDER BY EquipmentType
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            self.equipment_types_data = {row[0]: row[1] for row in rows}
            self.type_combo['values'] = list(self.equipment_types_data.values())
        except Exception as e:
            logger.error(f"Errore caricamento tipi equipaggiamento: {e}")
    
    def _load_rule_data(self):
        """Carica i dati della regola esistente."""
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT EquipmentTypeId, NumberOfCycles, DateOut
            FROM [Traceability_RS].[eqp].[EquipmentFixtureRules]
            WHERE EquipmentFixtureRuleId = ?
            """
            cursor.execute(query, self.rule_id)
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                type_id, cycles, date_out = row
                self.type_var.set(self.equipment_types_data.get(type_id, ''))
                self.cycles_var.set(str(cycles))
                if date_out:
                    self.date_out_var.set(date_out.strftime('%Y-%m-%d'))
        
        except Exception as e:
            logger.error(f"Errore caricamento dati regola: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento dati:\n{e}")
            self.destroy()
    
    def _validate_and_save(self):
        """Valida i dati e salva la regola."""
        # Validazione tipo equipaggiamento
        type_name = self.type_var.get()
        if not type_name:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               self.lang.get('error_no_equipment_type', 'Seleziona un tipo di equipaggiamento'))
            return
        
        type_id = [k for k, v in self.equipment_types_data.items() if v == type_name][0]
        
        # Validazione numero cicli
        try:
            cycles = int(self.cycles_var.get())
            if cycles <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               self.lang.get('error_invalid_cycles', 'Numero di cicli non valido'))
            return
        
        # Validazione data (opzionale)
        date_out = None
        if self.date_out_var.get():
            try:
                date_out = datetime.strptime(self.date_out_var.get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                   'Data non valida. Formato: YYYY-MM-DD')
                return
        
        # Salva nel database
        try:
            cursor = self.db.conn.cursor()
            
            if self.is_edit:
                query = """
                UPDATE [Traceability_RS].[eqp].[EquipmentFixtureRules]
                SET EquipmentTypeId = ?,
                    NumberOfCycles = ?,
                    DateOut = ?
                WHERE EquipmentFixtureRuleId = ?
                """
                cursor.execute(query, type_id, cycles, date_out, self.rule_id)
            else:
                query = """
                INSERT INTO [Traceability_RS].[eqp].[EquipmentFixtureRules]
                (EquipmentTypeId, NumberOfCycles, DateOut)
                VALUES (?, ?, ?)
                """
                cursor.execute(query, type_id, cycles, date_out)
            
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('rule_saved_success', 'Regola salvata con successo'))
            
            if self.callback:
                self.callback()
            
            self.destroy()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore salvataggio regola: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore salvataggio regola:\n{e}")


# ========================================
# ASSEGNAZIONE PRODOTTI A FIXTURE
# ========================================

class AssignProductsToFixturesWindow(tk.Toplevel):
    """Finestra per assegnare prodotti alle fixture ICT/FCT."""
    
    def __init__(self, parent, db, lang, user_name):
        logger.info(f"AssignProductsToFixturesWindow: Apertura finestra assegnazione prodotti (user: {user_name})")
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(self.lang.get('assign_products_window_title', 'Assegnazione Prodotti a Fixture'))
        self.geometry("1200x700")
        self.transient(parent)
        self.grab_set()
        
        self.selected_equipment_id = None
        
        self._create_widgets()
        self._load_fixtures()
    
    def _create_widgets(self):
        """Crea i widget della finestra."""
        # PanedWindow per dividere in due pannelli
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pannello sinistro: Fixture
        left_frame = ttk.LabelFrame(paned, text=self.lang.get('fixtures_label', 'Fixture (ICT/FCT)'), padding="10")
        paned.add(left_frame, weight=1)
        
        # Treeview fixture
        fixture_tree_frame = ttk.Frame(left_frame)
        fixture_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'fixture')
        self.fixture_tree = ttk.Treeview(fixture_tree_frame, columns=columns, show='headings', selectmode='browse')
        self.fixture_tree.heading('id', text='ID')
        self.fixture_tree.heading('fixture', text='Fixture')
        self.fixture_tree.column('id', width=50, anchor='center')
        self.fixture_tree.column('fixture', width=350)
        
        fixture_scrollbar = ttk.Scrollbar(fixture_tree_frame, orient=tk.VERTICAL, command=self.fixture_tree.yview)
        self.fixture_tree.configure(yscroll=fixture_scrollbar.set)
        
        self.fixture_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        fixture_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.fixture_tree.bind('<<TreeviewSelect>>', self._on_fixture_selected)
        
        # Pannello destro: Prodotti assegnati
        right_frame = ttk.LabelFrame(paned, text=self.lang.get('assigned_products_label', 'Prodotti Assegnati'), padding="10")
        paned.add(right_frame, weight=2)
        
        # Treeview prodotti
        product_tree_frame = ttk.Frame(right_frame)
        product_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('assignment_id', 'product_code', 'product_name', 'fixture_code', 'date', 'user')
        self.product_tree = ttk.Treeview(product_tree_frame, columns=columns, show='headings', selectmode='browse')
        self.product_tree.heading('assignment_id', text='ID')
        self.product_tree.heading('product_code', text=self.lang.get('product_code_label', 'Codice Prodotto'))
        self.product_tree.heading('product_name', text=self.lang.get('product_name_label', 'Nome Prodotto'))
        self.product_tree.heading('fixture_code', text=self.lang.get('fixture_code_label', 'Codice Fixture'))
        self.product_tree.heading('date', text=self.lang.get('date_label', 'Data'))
        self.product_tree.heading('user', text=self.lang.get('user_label', 'Utente'))
        
        self.product_tree.column('assignment_id', width=50, anchor='center')
        self.product_tree.column('product_code', width=120)
        self.product_tree.column('product_name', width=200)
        self.product_tree.column('fixture_code', width=120)
        self.product_tree.column('date', width=100, anchor='center')
        self.product_tree.column('user', width=100)
        
        product_scrollbar = ttk.Scrollbar(product_tree_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=product_scrollbar.set)
        
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        product_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pulsanti prodotti
        product_button_frame = ttk.Frame(right_frame)
        product_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(product_button_frame, text=self.lang.get('add_product_button', 'Aggiungi Prodotto'),
                  command=self._on_add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(product_button_frame, text=self.lang.get('remove_product_button', 'Rimuovi'),
                  command=self._on_remove_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(product_button_frame, text=self.lang.get('edit_fixture_code_button', 'Modifica Codice'),
                  command=self._on_edit_fixture_code).pack(side=tk.LEFT, padx=5)
        
        # Frame pulsanti principali
        main_button_frame = ttk.Frame(self, padding="10")
        main_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(main_button_frame, text=self.lang.get('refresh_button', 'Aggiorna'),
                  command=self._load_fixtures).pack(side=tk.RIGHT, padx=5)
        ttk.Button(main_button_frame, text=self.lang.get('close_button', 'Chiudi'),
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_fixtures(self):
        """Carica tutte le fixture ICT/FCT."""
        for item in self.fixture_tree.get_children():
            self.fixture_tree.delete(item)
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT 
                e.EquipmentId,
                UPPER(b.Brand) + ' -> ' + e.InternalName + ' ' + 
                ISNULL(e.InventoryNumber, '') + ' ' + ISNULL(e.SerialNumber, '') + 
                ' [' + t.EquipmentType + ']' AS FixtureDisplay
            FROM [Traceability_RS].[eqp].[Equipments] e
            INNER JOIN [Traceability_RS].[eqp].[EquipmentTypes] t 
                ON e.EquipmentTypeId = t.EquipmentTypeId
            INNER JOIN [Traceability_RS].[eqp].[EquipmentBrands] b 
                ON b.EquipmentBrandId = e.BrandId
            WHERE t.EquipmentType LIKE 'ICT%' OR t.EquipmentType LIKE 'FC%'
            ORDER BY FixtureDisplay
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                equipment_id, fixture_display = row
                self.fixture_tree.insert('', tk.END, iid=equipment_id, values=(equipment_id, fixture_display))
        
        except Exception as e:
            logger.error(f"Errore caricamento fixture: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento fixture:\n{e}")
    
    def _on_fixture_selected(self, event):
        """Gestisce la selezione di una fixture."""
        selected = self.fixture_tree.focus()
        if selected:
            self.selected_equipment_id = int(selected)
            self._load_assigned_products()
    
    def _load_assigned_products(self):
        """Carica i prodotti assegnati alla fixture selezionata."""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        if not self.selected_equipment_id:
            return
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT 
                f.EquipmentFixtureID,
                p.productcode,
                p.productname,
                f.FixtureCode,
                f.FixtureDateCreation,
                f.AddByUser
            FROM [Traceability_RS].[eqp].[EquipmentFixtures] f
            INNER JOIN [Traceability_RS].[dbo].[Products] p 
                ON p.IDProduct = f.IdProduct
            WHERE f.EquipmentId = ?
            ORDER BY f.FixtureDateCreation DESC
            """
            cursor.execute(query, self.selected_equipment_id)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                assignment_id, product_code, product_name, fixture_code, date_creation, user = row
                date_str = date_creation.strftime('%Y-%m-%d') if date_creation else ''
                fixture_code_str = fixture_code if fixture_code else ''
                
                self.product_tree.insert('', tk.END, iid=assignment_id,
                                       values=(assignment_id, product_code, product_name, 
                                             fixture_code_str, date_str, user))
        
        except Exception as e:
            logger.error(f"Errore caricamento prodotti assegnati: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento prodotti:\n{e}")
    
    def _on_add_product(self):
        """Apre il dialog per aggiungere un prodotto."""
        if not self.selected_equipment_id:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('error_no_fixture_selected', 'Seleziona una fixture'))
            return
        
        SelectProductDialog(self, self.db, self.lang, self.selected_equipment_id, 
                          self.user_name, callback=self._load_assigned_products)
    
    def _on_remove_product(self):
        """Rimuove il prodotto selezionato dalla fixture."""
        selected = self.product_tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('error_no_product_selected', 'Seleziona un prodotto'))
            return
        
        if not messagebox.askyesno(self.lang.get('confirm_title', 'Conferma'),
                                  self.lang.get('confirm_remove_product', 'Confermi rimozione del prodotto dalla fixture?')):
            return
        
        assignment_id = int(selected)
        
        try:
            cursor = self.db.conn.cursor()
            query = "DELETE FROM [Traceability_RS].[eqp].[EquipmentFixtures] WHERE EquipmentFixtureID = ?"
            cursor.execute(query, assignment_id)
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('product_removed_success', 'Prodotto rimosso con successo'))
            self._load_assigned_products()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore rimozione prodotto: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore rimozione prodotto:\n{e}")
    
    def _on_edit_fixture_code(self):
        """Modifica il codice fixture per l'assegnazione selezionata."""
        selected = self.product_tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('error_no_product_selected', 'Seleziona un prodotto'))
            return
        
        assignment_id = int(selected)
        values = self.product_tree.item(selected, 'values')
        current_code = values[3] if len(values) > 3 else ''
        
        EditFixtureCodeDialog(self, self.db, self.lang, assignment_id, current_code,
                            callback=self._load_assigned_products)


class SelectProductDialog(tk.Toplevel):
    """Dialog per selezionare un prodotto da assegnare."""
    
    def __init__(self, parent, db, lang, equipment_id, user_name, callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.equipment_id = equipment_id
        self.user_name = user_name
        self.callback = callback
        
        self.title(self.lang.get('select_product_title', 'Seleziona Prodotto'))
        self.geometry("700x500")
        self.transient(parent)
        self.grab_set()
        
        self.search_var = tk.StringVar()
        self.fixture_code_var = tk.StringVar()
        
        self._create_widgets()
        self._load_products()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        # Frame ricerca
        search_frame = ttk.Frame(self, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text=self.lang.get('search_label', 'Cerca:')).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text=self.lang.get('search_button', 'Cerca'),
                  command=self._load_products).pack(side=tk.LEFT, padx=5)
        
        # Treeview prodotti
        tree_frame = ttk.Frame(self, padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'code', 'name')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('code', text=self.lang.get('product_code_label', 'Codice'))
        self.tree.heading('name', text=self.lang.get('product_name_label', 'Nome'))
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('code', width=150)
        self.tree.column('name', width=400)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', lambda e: self._select_product())
        
        # Frame codice fixture
        code_frame = ttk.Frame(self, padding="10")
        code_frame.pack(fill=tk.X)
        
        ttk.Label(code_frame, text=self.lang.get('fixture_code_label', 'Codice Fixture:')).pack(side=tk.LEFT, padx=5)
        ttk.Entry(code_frame, textvariable=self.fixture_code_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Pulsanti
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text=self.lang.get('select_button', 'Seleziona'),
                  command=self._select_product).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_products(self):
        """Carica i prodotti con filtro di ricerca."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get().strip()
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            SELECT IDProduct, productcode, productname
            FROM [Traceability_RS].[dbo].[Products]
            """
            
            params = []
            if search_term:
                query += " WHERE productcode LIKE ? OR productname LIKE ?"
                params = [f'%{search_term}%', f'%{search_term}%']
            
            query += " ORDER BY productcode"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                product_id, code, name = row
                self.tree.insert('', tk.END, iid=product_id, values=(product_id, code, name))
        
        except Exception as e:
            logger.error(f"Errore caricamento prodotti: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore caricamento prodotti:\n{e}")
    
    def _select_product(self):
        """Assegna il prodotto selezionato alla fixture."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                 self.lang.get('error_no_product_selected', 'Seleziona un prodotto'))
            return
        
        product_id = int(selected)
        fixture_code = self.fixture_code_var.get().strip()
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            INSERT INTO [Traceability_RS].[eqp].[EquipmentFixtures]
            (EquipmentId, IdProduct, FixtureCode, FixtureDateCreation, AddByUser)
            VALUES (?, ?, ?, GETDATE(), ?)
            """
            cursor.execute(query, self.equipment_id, product_id, fixture_code if fixture_code else None, self.user_name)
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('product_assigned_success', 'Prodotto assegnato con successo'))
            
            if self.callback:
                self.callback()
            
            self.destroy()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore assegnazione prodotto: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore assegnazione prodotto:\n{e}")


class EditFixtureCodeDialog(tk.Toplevel):
    """Dialog per modificare il codice fixture."""
    
    def __init__(self, parent, db, lang, assignment_id, current_code, callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.assignment_id = assignment_id
        self.callback = callback
        
        self.title(self.lang.get('edit_fixture_code_title', 'Modifica Codice Fixture'))
        self.geometry("400x150")
        self.transient(parent)
        self.grab_set()
        
        self.code_var = tk.StringVar(value=current_code)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=self.lang.get('fixture_code_label', 'Codice Fixture:')).pack(anchor=tk.W, pady=5)
        code_entry = ttk.Entry(frame, textvariable=self.code_var, width=40)
        code_entry.pack(fill=tk.X, pady=5)
        code_entry.focus()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text=self.lang.get('save_button', 'Salva'),
                  command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _save(self):
        """Salva il nuovo codice fixture."""
        new_code = self.code_var.get().strip()
        
        try:
            cursor = self.db.conn.cursor()
            query = """
            UPDATE [Traceability_RS].[eqp].[EquipmentFixtures]
            SET FixtureCode = ?
            WHERE EquipmentFixtureID = ?
            """
            cursor.execute(query, new_code if new_code else None, self.assignment_id)
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                              self.lang.get('fixture_code_updated_success', 'Codice fixture aggiornato'))
            
            if self.callback:
                self.callback()
            
            self.destroy()
        
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore aggiornamento codice fixture: {e}")
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                               f"Errore aggiornamento codice:\n{e}")
