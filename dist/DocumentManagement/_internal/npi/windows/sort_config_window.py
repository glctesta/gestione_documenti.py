# File: npi/windows/sort_config_window.py
import tkinter as tk
from tkinter import ttk, messagebox

class SortConfigWindow(tk.Toplevel):
    """Finestra di configurazione per l'ordinamento di default del treeview."""
    
    def __init__(self, master, lang, current_config, callback):
        """
        Args:
            master: Finestra parent
            lang: Dizionario traduzioni
            current_config: Lista di tuple (campo, reverse) es: [('Name', False), ('DueDate', False)]
            callback: Funzione da chiamare quando si salva: callback(new_config)
        """
        super().__init__(master)
        self.lang = lang
        self.current_config = current_config.copy() if current_config else []
        self.callback = callback
        
        # Mappa campi -> etichette tradotte
        self.field_labels = {
            'Category': self.lang.get('col_category', 'Categoria'),
            'Name': self.lang.get('col_task', 'Task'),
            'Owner': self.lang.get('col_owner', 'Assegnato a'),
            'Status': self.lang.get('col_status', 'Stato'),
            'StartDate': self.lang.get('col_start_date', 'Inizio'),
            'DueDate': self.lang.get('col_due_date', 'Scadenza')
        }
        
        self.title(self.lang.get('sort_config_title', 'Configurazione Ordinamento'))
        self.geometry("700x500")
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._load_current_config()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        ttk.Label(main_frame, text=self.lang.get('sort_config_description', 
                  'Configura l\'ordinamento di default per i task del progetto:'),
                  font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Frame principale con due colonne
        columns_frame = ttk.Frame(main_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # COLONNA SINISTRA: Campi disponibili
        left_frame = ttk.LabelFrame(columns_frame, text=self.lang.get('available_fields', 'Campi Disponibili'), padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.available_listbox = tk.Listbox(left_frame, height=10)
        self.available_listbox.pack(fill=tk.BOTH, expand=True)
        
        # COLONNA CENTRO: Pulsanti di controllo
        buttons_frame = ttk.Frame(columns_frame)
        buttons_frame.pack(side=tk.LEFT, padx=10, pady=50)
        
        ttk.Button(buttons_frame, text="Aggiungi →", command=self._add_field, width=12).pack(pady=5)
        ttk.Button(buttons_frame, text="← Rimuovi", command=self._remove_field, width=12).pack(pady=5)
        
        # COLONNA DESTRA: Ordinamento corrente
        right_frame = ttk.LabelFrame(columns_frame, text=self.lang.get('current_sort', 'Ordinamento Corrente'), padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Listbox con scrollbar
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.sort_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sort_listbox.yview)
        
        self.sort_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pulsanti per cambiare ordine
        order_buttons = ttk.Frame(right_frame)
        order_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(order_buttons, text="↑ Su", command=self._move_up, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(order_buttons, text="↓ Giù", command=self._move_down, width=10).pack(side=tk.LEFT, padx=2)
        
        # Checkbox per direzione
        direction_frame = ttk.Frame(right_frame)
        direction_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.reverse_var = tk.BooleanVar()
        ttk.Checkbutton(direction_frame, text=self.lang.get('descending', 'Discendente'), 
                       variable=self.reverse_var, command=self._toggle_direction).pack(side=tk.LEFT)
        
        # Pulsanti azione
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text=self.lang.get('btn_save', 'Salva'), 
                  command=self._save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self.lang.get('reset_default', 'Reset Default'), 
                  command=self._reset_to_default).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self.lang.get('btn_cancel', 'Annulla'), 
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_current_config(self):
        """Carica la configurazione corrente nelle listbox."""
        # Popola campi disponibili
        all_fields = list(self.field_labels.keys())
        used_fields = [field for field, _ in self.current_config]
        
        for field in all_fields:
            if field not in used_fields:
                self.available_listbox.insert(tk.END, self.field_labels[field])
        
        # Popola ordinamento corrente
        self._refresh_sort_listbox()
    
    def _refresh_sort_listbox(self):
        """Aggiorna la listbox dell'ordinamento corrente."""
        self.sort_listbox.delete(0, tk.END)
        for field, reverse in self.current_config:
            direction = " ▼" if reverse else " ▲"
            display = f"{self.field_labels[field]}{direction}"
            self.sort_listbox.insert(tk.END, display)
    
    def _add_field(self):
        """Aggiunge un campo dall'elenco disponibili all'ordinamento."""
        selection = self.available_listbox.curselection()
        if not selection:
            return
        
        selected_label = self.available_listbox.get(selection[0])
        # Trova il campo corrispondente
        field = next(k for k, v in self.field_labels.items() if v == selected_label)
        
        # Aggiungi all'ordinamento (default ascendente)
        self.current_config.append((field, False))
        
        # Rimuovi dai disponibili
        self.available_listbox.delete(selection[0])
        
        # Aggiorna ordinamento
        self._refresh_sort_listbox()
    
    def _remove_field(self):
        """Rimuove un campo dall'ordinamento."""
        selection = self.sort_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        field, _ = self.current_config[idx]
        
        # Rimuovi dall'ordinamento
        del self.current_config[idx]
        
        # Aggiungi ai disponibili
        self.available_listbox.insert(tk.END, self.field_labels[field])
        
        # Aggiorna ordinamento
        self._refresh_sort_listbox()
    
    def _move_up(self):
        """Sposta il campo selezionato in alto nella priorità."""
        selection = self.sort_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        idx = selection[0]
        # Scambia con il precedente
        self.current_config[idx], self.current_config[idx-1] = \
            self.current_config[idx-1], self.current_config[idx]
        
        self._refresh_sort_listbox()
        self.sort_listbox.selection_set(idx-1)
    
    def _move_down(self):
        """Sposta il campo selezionato in basso nella priorità."""
        selection = self.sort_listbox.curselection()
        if not selection or selection[0] >= len(self.current_config) - 1:
            return
        
        idx = selection[0]
        # Scambia con il successivo
        self.current_config[idx], self.current_config[idx+1] = \
            self.current_config[idx+1], self.current_config[idx]
        
        self._refresh_sort_listbox()
        self.sort_listbox.selection_set(idx+1)
    
    def _toggle_direction(self):
        """Cambia la direzione del campo selezionato."""
        selection = self.sort_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        field, reverse = self.current_config[idx]
        self.current_config[idx] = (field, self.reverse_var.get())
        
        self._refresh_sort_listbox()
        self.sort_listbox.selection_set(idx)
    
    def _reset_to_default(self):
        """Ripristina l'ordinamento di default: Task, DataScadenza."""
        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_reset_sort', 
                                          'Ripristinare l\'ordinamento di default (Task, Scadenza)?'),
                              parent=self):
            self.current_config = [('Name', False), ('DueDate', False)]
            
            # Ripopola le listbox
            self.available_listbox.delete(0, tk.END)
            all_fields = list(self.field_labels.keys())
            used_fields = [field for field, _ in self.current_config]
            
            for field in all_fields:
                if field not in used_fields:
                    self.available_listbox.insert(tk.END, self.field_labels[field])
            
            self._refresh_sort_listbox()
    
    def _save_config(self):
        """Salva la configurazione e chiude la finestra."""
        if not self.current_config:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('warning_no_sort_fields', 
                                             'Seleziona almeno un campo per l\'ordinamento.'),
                                 parent=self)
            return
        
        # Chiama il callback con la nuova configurazione
        self.callback(self.current_config)
        self.destroy()
