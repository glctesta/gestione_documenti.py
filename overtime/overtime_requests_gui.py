"""
Overtime Requests GUI
Form per la creazione di richieste di straordinario
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import logging

from .overtime_manager import OvertimeManager

logger = logging.getLogger(__name__)


def open_overtime_request_window(parent, db_handler, lang_manager, user_name, user_id=0):
    """
    Apre la finestra per creare richieste di straordinario.
    
    Args:
        parent: Finestra parent
        db_handler: DatabaseHandler instance
        lang_manager: LanguageManager instance
        user_name: Nome utente loggato
        user_id: ID utente (idanga da tbuserkey)
    """
    OvertimeRequestWindow(parent, db_handler, lang_manager, user_name, user_id)


class OvertimeRequestWindow(tk.Toplevel):
    """
    Finestra per creare richieste di straordinario.
    """
    
    def __init__(self, parent, db_handler, lang_manager, user_name, user_id=0):
        super().__init__(parent)
        
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        self.user_id = user_id  # ID utente (idanga)
        self.manager = OvertimeManager(db_handler)
        
        # Dati
        self.employees_data = {}  # {display_name: employee_id}
        self.reasons_data = {}    # {reason_text: (reason_id, requires_order, requires_justify)}
        self.orders_data = {}     # {display_text: order_id}
        self.selected_employees = []  # Lista di dict con dati dipendenti selezionati
        self.all_employee_values = []
        
        # Setup finestra
        self.title(self.lang.get('overtime_request_title', 'Richiesta Straordinario'))
        self.geometry("1200x800")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_initial_data()
    
    def _create_widgets(self):
        """Crea i widget dell'interfaccia."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === SEZIONE SELEZIONE DIPENDENTE ===
        selection_frame = ttk.LabelFrame(
            main_frame, 
            text=self.lang.get('employee_selection', 'Selezione Dipendente'),
            padding="10"
        )
        selection_frame.pack(fill=tk.X, pady=5)
        
        # Riga 1: Dipendente
        ttk.Label(selection_frame, text=self.lang.get('employee', 'Dipendente:')).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.employee_var = tk.StringVar()
        self.employee_combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.employee_var,
            state='normal',
            width=40
        )
        self.employee_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.employee_combo.bind('<Return>', self._filter_employee_combo)
        self.employee_combo.bind('<FocusOut>', self._filter_employee_combo)
        self.employee_combo.bind('<FocusIn>', self._reset_employee_filter)
        self.employee_combo.bind('<<ComboboxSelected>>', self._sync_employee_display_name)
        
        # Riga 2: Motivo
        ttk.Label(selection_frame, text=self.lang.get('reason', 'Motivo:')).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.reason_var = tk.StringVar()
        self.reason_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.reason_var,
            state='readonly',
            width=40
        )
        self.reason_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.reason_combo.bind('<<ComboboxSelected>>', self._on_reason_changed)
        
        # Riga 3: Data e Ora Inizio
        ttk.Label(selection_frame, text=self.lang.get('start_datetime', 'Data/Ora Inizio:')).grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        
        datetime_start_frame = ttk.Frame(selection_frame)
        datetime_start_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.start_date = DateEntry(
            datetime_start_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.start_date.pack(side=tk.LEFT, padx=2)
        
        self.start_hour_var = tk.StringVar(value="18")
        self.start_minute_var = tk.StringVar(value="00")
        
        ttk.Spinbox(datetime_start_frame, from_=0, to=23, textvariable=self.start_hour_var, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(datetime_start_frame, text=":").pack(side=tk.LEFT)
        ttk.Spinbox(datetime_start_frame, from_=0, to=59, textvariable=self.start_minute_var, width=5).pack(side=tk.LEFT, padx=2)
        
        # Riga 4: Data e Ora Fine
        ttk.Label(selection_frame, text=self.lang.get('end_datetime', 'Data/Ora Fine:')).grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5
        )
        
        datetime_end_frame = ttk.Frame(selection_frame)
        datetime_end_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.end_date = DateEntry(
            datetime_end_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.end_date.pack(side=tk.LEFT, padx=2)
        
        self.end_hour_var = tk.StringVar(value="21")
        self.end_minute_var = tk.StringVar(value="00")
        
        ttk.Spinbox(datetime_end_frame, from_=0, to=23, textvariable=self.end_hour_var, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(datetime_end_frame, text=":").pack(side=tk.LEFT)
        ttk.Spinbox(datetime_end_frame, from_=0, to=59, textvariable=self.end_minute_var, width=5).pack(side=tk.LEFT, padx=2)
        
        # Riga 5: Giustificazione (opzionale, visibile solo se richiesta)
        ttk.Label(selection_frame, text=self.lang.get('justification', 'Giustificazione:')).grid(
            row=4, column=0, sticky=tk.NW, padx=5, pady=5
        )
        self.justify_text = tk.Text(selection_frame, height=3, width=40, wrap=tk.WORD)
        self.justify_text.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.justify_text.config(state='disabled')
        
        # === SEZIONE ORDINI (opzionale) ===
        self.orders_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('order_association', 'Associazione Ordini (opzionale)'),
            padding="10"
        )
        self.orders_frame.pack(fill=tk.X, pady=5)
        self.orders_frame.pack_forget()  # Nascosto di default
        
        ttk.Label(self.orders_frame, text=self.lang.get('order', 'Ordine:')).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.order_var = tk.StringVar()
        self.order_combo = ttk.Combobox(
            self.orders_frame,
            textvariable=self.order_var,
            state='readonly',
            width=30
        )
        self.order_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.orders_frame, text=self.lang.get('target_quantity', 'Quantità Target:')).grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.qty_var = tk.StringVar(value="0")
        ttk.Entry(self.orders_frame, textvariable=self.qty_var, width=10).grid(
            row=0, column=3, sticky=tk.W, padx=5, pady=5
        )
        
        # Pulsante Aggiungi Dipendente
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text=self.lang.get('add_employee', 'Aggiungi Dipendente'),
            command=self._add_employee_to_list
        ).pack(side=tk.LEFT, padx=5)
        
        # === LISTA DIPENDENTI AGGIUNTI ===
        list_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('employees_list', 'Dipendenti Aggiunti'),
            padding="10"
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview
        columns = ('employee', 'reason', 'start', 'end', 'hours', 'justify')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        self.tree.heading('employee', text=self.lang.get('employee', 'Dipendente'))
        self.tree.heading('reason', text=self.lang.get('reason', 'Motivo'))
        self.tree.heading('start', text=self.lang.get('start', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end', 'Fine'))
        self.tree.heading('hours', text=self.lang.get('hours', 'Ore'))
        self.tree.heading('justify', text=self.lang.get('justify', 'Giustificazione'))
        
        self.tree.column('employee', width=200)
        self.tree.column('reason', width=200)
        self.tree.column('start', width=130)
        self.tree.column('end', width=130)
        self.tree.column('hours', width=60)
        self.tree.column('justify', width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pulsante rimuovi
        ttk.Button(
            list_frame,
            text=self.lang.get('remove_selected', 'Rimuovi Selezionato'),
            command=self._remove_selected_employee
        ).pack(pady=5)
        
        # === PULSANTI AZIONE ===
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('submit_request', 'Invia Richiesta'),
            command=self._submit_request
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _load_initial_data(self):
        """Carica dati iniziali (dipendenti, motivi, ordini)."""
        # Carica dipendenti
        logger.info("Caricamento dipendenti eligibili...")
        employees = self.manager.fetch_eligible_employees()
        logger.info(f"Dipendenti trovati: {len(employees) if employees else 0}")
        if employees:
            self.employees_data = {
                f"{row[1]} {row[2]}": row[0] for row in employees
            }
            self.all_employee_values = sorted(list(self.employees_data.keys()))
            self.employee_combo['values'] = self.all_employee_values
            logger.info(f"Combobox popolata con {len(self.employees_data)} dipendenti")
        else:
            logger.warning("Nessun dipendente eligibile trovato")
        
        # Carica motivi
        logger.info("Caricamento motivi straordinario...")
        reasons = self.manager.fetch_overtime_reasons()
        logger.info(f"Motivi trovati: {len(reasons) if reasons else 0}")
        if reasons:
            self.reasons_data = {
                row[1]: (row[0], row[2], row[3]) for row in reasons
            }
            self.reason_combo['values'] = list(self.reasons_data.keys())
            logger.info(f"Combobox motivi popolata con {len(self.reasons_data)} motivi")
        else:
            logger.warning("Nessun motivo straordinario trovato")
        
        # Carica ordini
        logger.info("Caricamento ordini recenti...")
        orders = self.manager.fetch_recent_orders()
        logger.info(f"Ordini trovati: {len(orders) if orders else 0}")
        if orders:
            self.orders_data = {
                f"{row[1]} (Qty: {row[2]})": row[0] for row in orders
            }
            self.order_combo['values'] = list(self.orders_data.keys())
            logger.info(f"Combobox ordini popolata con {len(self.orders_data)} ordini")
        else:
            logger.warning("Nessun ordine recente trovato")
    
    def _on_reason_changed(self, event=None):
        """Gestisce cambio motivo per mostrare/nascondere campi opzionali."""
        reason_text = self.reason_var.get()
        if not reason_text or reason_text not in self.reasons_data:
            return
        
        reason_id, requires_order, requires_justify = self.reasons_data[reason_text]
        
        # Mostra/nascondi sezione ordini
        if requires_order == 'Yes':
            self.orders_frame.pack(fill=tk.X, pady=5, before=self.tree.master)
        else:
            self.orders_frame.pack_forget()
        
        # Abilita/disabilita giustificazione
        if requires_justify == 'Yes':
            self.justify_text.config(state='normal')
        else:
            self.justify_text.config(state='disabled')
            self.justify_text.delete('1.0', tk.END)

    def _filter_employee_combo(self, event=None):
        """Filtra dinamicamente i dipendenti nel combobox in base al testo digitato."""
        query = self.employee_var.get().strip().lower()
        all_values = self.all_employee_values or sorted(list(self.employees_data.keys()))

        if not query:
            filtered_values = all_values
        else:
            starts_with = [name for name in all_values if name.lower().startswith(query)]
            contains = [name for name in all_values if query in name.lower() and name not in starts_with]
            filtered_values = starts_with + contains

        self.employee_combo['values'] = filtered_values

        if event and event.keysym in ('Up', 'Down', 'Escape', 'Tab'):
            return
        if event and event.keysym == 'Return' and filtered_values and query:
            self.employee_combo.event_generate('<Down>')

    def _reset_employee_filter(self, event=None):
        """Ripristina elenco completo nel combobox dipendenti."""
        if self.all_employee_values:
            self.employee_combo['values'] = self.all_employee_values

    def _sync_employee_display_name(self, event=None):
        """Normalizza il nome selezionato nel formato esatto presente in lista."""
        employee_name = self.employee_var.get().strip()
        if not employee_name:
            return
        for name in self.employees_data.keys():
            if name.lower() == employee_name.lower():
                self.employee_var.set(name)
                return

    def _resolve_employee_name(self):
        """Risolvi il nome dipendente digitato/selecionato contro la lista valida."""
        employee_name = self.employee_var.get().strip()
        if not employee_name:
            return None
        if employee_name in self.employees_data:
            return employee_name

        matches = [name for name in self.employees_data.keys() if name.lower() == employee_name.lower()]
        if len(matches) == 1:
            self.employee_var.set(matches[0])
            return matches[0]
        return None
    
    def _add_employee_to_list(self):
        """Aggiunge dipendente selezionato alla lista."""
        # Validazioni
        if not self.employee_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_employee_warning', 'Selezionare un dipendente'),
                parent=self
            )
            return
        
        if not self.reason_var.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_reason_warning', 'Selezionare un motivo'),
                parent=self
            )
            return
        
        # Costruisci datetime
        try:
            start_dt = datetime.combine(
                self.start_date.get_date(),
                datetime.strptime(f"{self.start_hour_var.get()}:{self.start_minute_var.get()}", "%H:%M").time()
            )
            end_dt = datetime.combine(
                self.end_date.get_date(),
                datetime.strptime(f"{self.end_hour_var.get()}:{self.end_minute_var.get()}", "%H:%M").time()
            )
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore formato data/ora: {e}",
                parent=self
            )
            return
        
        # VALIDAZIONE: La richiesta non può essere retroattiva
        now = datetime.now()
        if start_dt < now:
            messagebox.showerror(
                self.lang.get('validation_error', 'Errore Validazione'),
                self.lang.get('no_retroactive_requests', 
                    'Le richieste di straordinario non possono essere retroattive.\n'
                    'La data/ora di inizio deve essere nel futuro.'),
                parent=self
            )
            return
        
        # Valida che fine sia dopo inizio
        if end_dt <= start_dt:
            messagebox.showerror(
                self.lang.get('validation_error', 'Errore Validazione'),
                self.lang.get('end_before_start', 
                    'La data/ora di fine deve essere successiva alla data/ora di inizio.'),
                parent=self
            )
            return
        
        employee_name = self._resolve_employee_name()
        if not employee_name:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_employee_warning', 'Selezionare un dipendente valido dalla lista'),
                parent=self
            )
            return

        employee_id = self.employees_data[employee_name]
        reason_text = self.reason_var.get()
        reason_id, requires_order, requires_justify = self.reasons_data[reason_text]
        
        # Valida richiesta
        is_valid, error_msg = self.manager.validate_overtime_request(
            employee_id, start_dt, end_dt, reason_id
        )
        
        if not is_valid:
            messagebox.showerror(
                self.lang.get('validation_error', 'Errore Validazione'),
                error_msg,
                parent=self
            )
            return
        
        # Verifica giustificazione se richiesta
        justify = self.justify_text.get('1.0', tk.END).strip()
        if requires_justify == 'Yes' and not justify:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('justify_required', 'Giustificazione obbligatoria per questo motivo'),
                parent=self
            )
            return
        
        # Calcola ore
        hours = (end_dt - start_dt).total_seconds() / 3600
        
        # Aggiungi a lista
        employee_data = {
            'employee_id': employee_id,
            'employee_name': employee_name,
            'reason_id': reason_id,
            'reason_text': reason_text,
            'start': start_dt,
            'end': end_dt,
            'hours': hours,
            'justify': justify if justify else 'N/A',
            'order_id': None,
            'qty_target': None
        }
        
        # Aggiungi ordine se presente
        if requires_order == 'Yes':
            if not self.order_var.get():
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('order_required', 'Ordine obbligatorio per questo motivo'),
                    parent=self
                )
                return
            
            order_display = self.order_var.get()
            employee_data['order_id'] = self.orders_data[order_display]
            
            # Estrai numero ordine dal display (formato: "PO_NUMBER (Qty: XXX)")
            try:
                order_number = order_display.split(' (Qty:')[0]
                employee_data['order_number'] = order_number
                
                order_qty_str = order_display.split('Qty: ')[1].rstrip(')')
                order_qty = float(order_qty_str)
                target_qty = float(self.qty_var.get()) if self.qty_var.get() else 0
                
                # Valida che quantità target non superi quantità ordine
                if target_qty > order_qty:
                    messagebox.showerror(
                        self.lang.get('validation_error', 'Errore Validazione'),
                        self.lang.get('qty_exceeds_order', f'Quantità target ({target_qty}) non può superare quantità ordine ({order_qty})'),
                        parent=self
                    )
                    return
                
                employee_data['qty_target'] = int(target_qty)
            except (ValueError, IndexError) as e:
                logger.error(f"Errore parsing quantità ordine: {e}")
                employee_data['order_number'] = 'N/A'
                employee_data['qty_target'] = 0
        
        self.selected_employees.append(employee_data)
        
        # Aggiungi a treeview
        self.tree.insert('', tk.END, values=(
            employee_name,
            reason_text,
            start_dt.strftime('%d/%m/%Y %H:%M'),
            end_dt.strftime('%d/%m/%Y %H:%M'),
            f"{hours:.1f}",
            justify
        ))
        
        # Reset campi
        self.employee_var.set('')
        self.reason_var.set('')
        self.justify_text.delete('1.0', tk.END)
        self.order_var.set('')
        self.qty_var.set('0')
    
    def _remove_selected_employee(self):
        """Rimuove dipendente selezionato dalla lista."""
        selected = self.tree.selection()
        if not selected:
            return
        
        # Trova indice
        index = self.tree.index(selected[0])
        
        # Rimuovi da lista e treeview
        del self.selected_employees[index]
        self.tree.delete(selected[0])
    
    def _submit_request(self):
        """Invia la richiesta di straordinario."""
        if not self.selected_employees:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_employees_selected', 'Aggiungere almeno un dipendente'),
                parent=self
            )
            return
        
        # Conferma
        confirm = messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_submit', f'Confermare invio richiesta per {len(self.selected_employees)} dipendente/i?'),
            parent=self
        )
        
        if not confirm:
            return
        
        # Crea richiesta
        success, request_id, request_number, error_msg = self.manager.create_overtime_request(
            supervisor_id=self.user_id,  # Usa l'ID utente reale invece di 0
            supervisor_name=self.user_name,
            employees_data=self.selected_employees,
            orders_data=None  # TODO: Gestire ordini se necessario
        )
        
        if not success:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore creazione richiesta:\n{error_msg}",
                parent=self
            )
            return
        
        # Genera PDF con dati completi
        pdf_employees = [
            {
                'employee_id': emp['employee_id'],
                'name': emp['employee_name'],
                'start': emp['start'],
                'end': emp['end'],
                'reason': emp['reason_text'],
                'order_id': emp.get('order_id'),
                'order_number': emp.get('order_number'),  # Aggiungi numero ordine
                'qty_target': emp.get('qty_target')
            }
            for emp in self.selected_employees
        ]
        
        pdf_path = self.manager.generate_overtime_pdf(
            request_id,
            request_number,
            self.user_name,
            pdf_employees
        )
        
        # Invia email
        if pdf_path:
            self.manager.send_overtime_notification(
                request_number,
                self.user_name,
                len(self.selected_employees),
                pdf_path
            )
        
        # Successo
        messagebox.showinfo(
            self.lang.get('success', 'Successo'),
            self.lang.get('request_created', f'Richiesta creata con successo!\nNumero: {request_number}'),
            parent=self
        )
        
        self.destroy()
