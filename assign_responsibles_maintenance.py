import tkinter as tk
from tkinter import ttk, messagebox


class AssignResponsiblesWindow(tk.Toplevel):
    """Finestra per assegnare responsabili ai programmi di manutenzione."""
    
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('assign_responsibles_title', "Assegna Responsabili ai Programmi di Manutenzione"))
        self.geometry("1000x600")
        
        # Dizionario per memorizzare le funzioni disponibili
        self.functions_data = {}
        
        # ID del programma selezionato
        self.selected_program_id = None
        
        self._create_widgets()
        self._load_functions()
        self._load_programs()
    
    def _create_widgets(self):
        """Crea i componenti grafici della finestra."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Frame sinistro - Lista programmi
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('programs_list_label', "Programmi di Manutenzione"), padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        
        # Treeview per i programmi
        cols = ('id', 'timing', 'value', 'order', 'responsible')
        self.programs_tree = ttk.Treeview(left_frame, columns=cols, show="headings")
        self.programs_tree.heading('id', text='ID')
        self.programs_tree.heading('timing', text=self.lang.get('timing_description', 'Descrizione Timing'))
        self.programs_tree.heading('value', text=self.lang.get('timing_value', 'Valore'))
        self.programs_tree.heading('order', text=self.lang.get('order', 'Ordine'))
        self.programs_tree.heading('responsible', text=self.lang.get('responsible', 'Responsabile'))
        
        self.programs_tree.column('id', width=50)
        self.programs_tree.column('timing', width=200)
        self.programs_tree.column('value', width=80)
        self.programs_tree.column('order', width=60)
        self.programs_tree.column('responsible', width=200)
        
        self.programs_tree.grid(row=0, column=0, sticky="nsew")
        self.programs_tree.bind("<<TreeviewSelect>>", self._on_program_select)
        
        # Scrollbar per programmi
        programs_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.programs_tree.yview)
        self.programs_tree.configure(yscrollcommand=programs_scrollbar.set)
        programs_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame destro - Gestione responsabile
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('assign_responsible_label', "Assegna/Modifica Responsabile"), padding="10")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.columnconfigure(1, weight=1)
        
        # Combo per selezionare il responsabile
        ttk.Label(right_frame, text=self.lang.get('select_responsible_label', "Seleziona Responsabile:")).grid(row=0, column=0, sticky="w", padx=5, pady=10)
        self.responsible_var = tk.StringVar()
        self.responsible_combo = ttk.Combobox(right_frame, textvariable=self.responsible_var, state="readonly", width=40)
        self.responsible_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        
        # Info programma selezionato
        info_frame = ttk.LabelFrame(right_frame, text=self.lang.get('selected_program_info', "Informazioni Programma Selezionato"), padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        info_frame.columnconfigure(1, weight=1)
        
        self.info_timing = ttk.Label(info_frame, text="", font=("Helvetica", 10))
        self.info_timing.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        
        self.info_value = ttk.Label(info_frame, text="", font=("Helvetica", 10))
        self.info_value.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        
        self.info_current_resp = ttk.Label(info_frame, text="", font=("Helvetica", 10, "bold"))
        self.info_current_resp.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        
        # Pulsanti azione
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text=self.lang.get('assign_button', "Assegna"), command=self._assign_responsible).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('remove_assignment_button', "Rimuovi Assegnazione"), command=self._remove_assignment).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.lang.get('refresh_button', "Aggiorna"), command=self._load_programs).pack(side="left", padx=5)
    
    def _load_functions(self):
        """Carica le funzioni disponibili dal database."""
        query = """
        SELECT FunctionDescription, FunctionCode
        FROM [Employee].[dbo].[Functions]
        WHERE FunctionCode IN (20, 30, 40, 50, 60, 80, 61)
        ORDER BY FunctionDescription
        """
        try:
            results = self.db.fetch_all(query)
            if results:
                self.functions_data = {row[0]: row[0] for row in results}
                self.responsible_combo['values'] = sorted(list(self.functions_data.keys()))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                f"{self.lang.get('error_loading_functions', 'Errore nel caricamento delle funzioni:')} {e}",
                parent=self
            )
    
    def _load_programs(self):
        """Carica i programmi di manutenzione dal database."""
        query = """
        SELECT TOP (1000) 
            [ProgrammedInterventionId],
            [TimingDescriprion],
            [TimingValue],
            [OrdinePrn],
            [BelongTo]
        FROM [Traceability_RS].[eqp].[ProgrammedInterventions]
        ORDER BY [TimingDescriprion]
        """
        try:
            self.programs_tree.delete(*self.programs_tree.get_children())
            results = self.db.fetch_all(query)
            
            if results:
                for row in results:
                    prog_id, timing, value, order, belong_to = row
                    self.programs_tree.insert("", "end", values=(
                        prog_id,
                        timing or '',
                        value or '',
                        order or '',
                        belong_to or ''
                    ))
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                f"{self.lang.get('error_loading_programs', 'Errore nel caricamento dei programmi:')} {e}",
                parent=self
            )
    
    def _on_program_select(self, event=None):
        """Gestisce la selezione di un programma dalla lista."""
        selected_item = self.programs_tree.focus()
        if not selected_item:
            return
        
        values = self.programs_tree.item(selected_item, 'values')
        self.selected_program_id = values[0]
        
        # Aggiorna le informazioni del programma selezionato
        self.info_timing.config(text=f"{self.lang.get('timing_label', 'Timing')}: {values[1]}")
        self.info_value.config(text=f"{self.lang.get('value_label', 'Valore')}: {values[2]}")
        
        current_resp = values[4] if values[4] else self.lang.get('not_assigned', 'Non assegnato')
        self.info_current_resp.config(text=f"{self.lang.get('current_responsible_label', 'Responsabile Attuale')}: {current_resp}")
        
        # Preseleziona il responsabile attuale nel combo se esiste
        if values[4] and values[4] in self.functions_data:
            self.responsible_var.set(values[4])
        else:
            self.responsible_var.set('')
    
    def _assign_responsible(self):
        """Assegna o modifica il responsabile per il programma selezionato."""
        if not self.selected_program_id:
            messagebox.showwarning(
                self.lang.get('warning_title', "Attenzione"),
                self.lang.get('select_program_warning', "Selezionare un programma dalla lista."),
                parent=self
            )
            return
        
        responsible = self.responsible_var.get()
        if not responsible:
            messagebox.showwarning(
                self.lang.get('warning_title', "Attenzione"),
                self.lang.get('select_responsible_warning', "Selezionare un responsabile."),
                parent=self
            )
            return
        
        # Conferma l'operazione
        if not messagebox.askyesno(
            self.lang.get('confirm_title', "Conferma"),
            f"{self.lang.get('confirm_assign_message', 'Assegnare')} '{responsible}' {self.lang.get('to_program', 'al programma')} ID {self.selected_program_id}?",
            parent=self
        ):
            return
        
        # Esegui l'UPDATE
        query = """
        UPDATE [Traceability_RS].[eqp].[ProgrammedInterventions]
        SET BelongTo = ?
        WHERE ProgrammedInterventionId = ?
        """
        try:
            self.db.execute_query(query, (responsible, self.selected_program_id))
            messagebox.showinfo(
                self.lang.get('success_title', "Successo"),
                self.lang.get('assignment_success', "Assegnazione completata con successo."),
                parent=self
            )
            self._load_programs()  # Ricarica la lista per mostrare le modifiche
        except Exception as e:
            error_msg = self.lang.get('error_assigning', "Errore durante l'assegnazione:")
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                f"{error_msg} {e}",
                parent=self
            )
    
    def _remove_assignment(self):
        """Rimuove l'assegnazione del responsabile per il programma selezionato."""
        if not self.selected_program_id:
            messagebox.showwarning(
                self.lang.get('warning_title', "Attenzione"),
                self.lang.get('select_program_warning', "Selezionare un programma dalla lista."),
                parent=self
            )
            return
        
        # Conferma l'operazione
        confirm_msg = self.lang.get('confirm_remove_message', "Rimuovere l'assegnazione dal programma")
        if not messagebox.askyesno(
            self.lang.get('confirm_title', "Conferma"),
            f"{confirm_msg} ID {self.selected_program_id}?",
            parent=self
        ):
            return
        
        # Esegui l'UPDATE per impostare BelongTo a NULL
        query = """
        UPDATE [Traceability_RS].[eqp].[ProgrammedInterventions]
        SET BelongTo = NULL
        WHERE ProgrammedInterventionId = ?
        """
        try:
            self.db.execute_query(query, (self.selected_program_id,))
            messagebox.showinfo(
                self.lang.get('success_title', "Successo"),
                self.lang.get('removal_success', "Assegnazione rimossa con successo."),
                parent=self
            )
            self.responsible_var.set('')  # Pulisce il combo
            self._load_programs()  # Ricarica la lista per mostrare le modifiche
        except Exception as e:
            error_msg = self.lang.get('error_removing', "Errore durante la rimozione:")
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                f"{error_msg} {e}",
                parent=self
            )


def open_assign_responsibles(parent, db, lang):
    """Launcher function to create and show the AssignResponsiblesWindow."""
    AssignResponsiblesWindow(parent, db, lang)
