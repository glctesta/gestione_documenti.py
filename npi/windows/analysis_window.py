import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ProjectAnalysisWindow(tk.Toplevel):
    """
    Finestra per analizzare lo stato dei task di un progetto e inviare solleciti.
    """

    def __init__(self, master, npi_manager, lang, project_id, project_name):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.project_name = project_name
        self.analysis_data = None
        self.final_milestone = None

        # Caratteri unicode per le checkbox
        self.CHAR_CHECKED = '✔'
        self.CHAR_UNCHECKED = ''  # o '☐' se preferisci

        self.title(f"{self.lang.get('analysis_window_title', 'Analisi Progetto')}: {self.project_name}")
        self.geometry("800x700")
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self._load_analysis()

    def _normalize_date(self, value):
        if not value:
            return None
        return value.date() if hasattr(value, 'date') else value

    def _split_late_tasks(self, tasks):
        """Restituisce (open_overdue, completed_late) per la lista task dell'owner."""
        today = datetime.now().date()
        open_overdue = 0
        completed_late = 0

        for task in tasks:
            due_date = self._normalize_date(getattr(task, 'DataScadenza', None))
            status_norm = (getattr(task, 'Stato', '') or '').strip().lower()

            if not due_date:
                continue

            if status_norm == 'completato':
                completion_date = self._normalize_date(getattr(task, 'DataCompletamento', None))
                if completion_date and completion_date > due_date:
                    completed_late += 1
            elif status_norm != 'cancellato' and due_date < today:
                open_overdue += 1

        return open_overdue, completed_late

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(main_frame, text=self.lang.get('late_tasks_summary', "Riepilogo Task in Ritardo"),
                           font=('Helvetica', 14, 'bold'))
        header.pack(pady=(0, 10))

        legend_frame = ttk.Frame(main_frame)
        legend_frame.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(
            legend_frame,
            text=self.lang.get('legend_open_overdue', 'Rosso = Aperti in ritardo'),
            foreground='#C62828',
            font=('Helvetica', 9, 'bold')
        ).pack(side=tk.LEFT, padx=(0, 16))

        ttk.Label(
            legend_frame,
            text=self.lang.get('legend_completed_late', 'Arancione = Completati in ritardo'),
            foreground='#EF6C00',
            font=('Helvetica', 9, 'bold')
        ).pack(side=tk.LEFT)

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # ---** CORREZIONE: DEFINIZIONE PULITA DELLA TREEVIEW CON COLONNA CHECKBOX **---
        cols = ('select', 'owner', 'open_overdue', 'completed_late', 'late_count')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings')

        # Configurazione colonna Checkbox ('select')
        self.tree.heading('select', text=self.CHAR_CHECKED)
        self.tree.column('select', width=40, anchor=tk.CENTER, stretch=tk.NO)

        # Configurazione altre colonne
        self.tree.heading('owner', text=self.lang.get('col_owner', "Responsabile"))
        self.tree.heading('open_overdue', text=self.lang.get('col_open_overdue', "Aperti in Ritardo"))
        self.tree.column('open_overdue', width=140, anchor=tk.CENTER)
        self.tree.heading('completed_late', text=self.lang.get('col_completed_late', "Completati in Ritardo"))
        self.tree.column('completed_late', width=170, anchor=tk.CENTER)
        self.tree.heading('late_count', text=self.lang.get('col_late_tasks_count', "Totale Ritardo"))
        self.tree.column('late_count', width=120, anchor=tk.CENTER)

        # Tag colore per lettura immediata della severita'.
        self.tree.tag_configure('has_open_overdue', foreground='#C62828')
        self.tree.tag_configure('only_completed_late', foreground='#EF6C00')

        # Associa l'evento click alla funzione di toggle
        self.tree.bind('<Button-1>', self._toggle_check)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # ---** FINE CORREZIONE **---

        # Log (invariato)
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding=5)
        log_frame.pack(fill=tk.X, pady=10)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Pulsanti (invariato)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        self.send_button = ttk.Button(button_frame, text=self.lang.get('btn_send_reminders', 'Invia Solleciti'),
                                      command=self._send_reminders, state=tk.DISABLED)
        self.send_button.pack(side=tk.LEFT)
        ttk.Button(button_frame, text=self.lang.get('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    def _toggle_check(self, event):
        """Inverte lo stato di selezione di una riga quando si clicca sulla colonna checkbox."""
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        # Esegui l'azione solo se si clicca sulla prima colonna ('select', che è #1)
        if not row_id or column_id != '#1':
            return

        current_value = self.tree.set(row_id, 'select')
        new_value = self.CHAR_UNCHECKED if current_value == self.CHAR_CHECKED else self.CHAR_CHECKED
        self.tree.set(row_id, 'select', new_value)

    def _load_analysis(self):
        self._log_message("Avvio analisi progetto...")
        try:
            self.analysis_data, self.final_milestone = self.npi_manager.get_project_analysis(self.project_id)
            for item in self.tree.get_children(): self.tree.delete(item)

            if not self.analysis_data:
                self._log_message("Nessun task in ritardo trovato. Ottimo lavoro!")
                return

            owners_with_open_overdue = 0
            owners_with_any_late = 0
            for owner, tasks in self.analysis_data.items():
                open_overdue, completed_late = self._split_late_tasks(tasks)
                total_late = open_overdue + completed_late
                if total_late == 0:
                    continue

                owners_with_any_late += 1
                if open_overdue > 0:
                    owners_with_open_overdue += 1

                row_tag = 'has_open_overdue' if open_overdue > 0 else 'only_completed_late'

                # Il valore della riga ora include il carattere per la checkbox
                values = (self.CHAR_CHECKED, owner.Nome, open_overdue, completed_late, total_late)
                # 'text' non è più usato per dati, ma l'ID della riga è univoco
                self.tree.insert('', tk.END, values=values, text=owner.Nome, tags=(row_tag,))

            if owners_with_any_late == 0:
                self._log_message("Nessun task in ritardo trovato. Ottimo lavoro!")
                self.send_button.config(state=tk.DISABLED)
                return

            self.send_button.config(state=tk.NORMAL)
            self._log_message(
                f"Analisi completata. Responsabili con ritardi: {owners_with_any_late} "
                f"(con task aperti scaduti: {owners_with_open_overdue})."
            )
        except Exception as e:
            logger.error(f"Errore durante l'analisi del progetto {self.project_id}: {e}", exc_info=True)
            self._log_message(f"ERRORE: Impossibile completare l'analisi. Dettagli: {e}")
            messagebox.showerror(self.lang.get('error_title', "Errore"), f"Impossibile analizzare il progetto:\n{e}",
                                 parent=self)

    def _send_reminders(self):
        reminders_to_send = {}
        for row_id in self.tree.get_children():
            # Controlla se la colonna 'select' ha il carattere di spunta
            if self.tree.set(row_id, 'select') == self.CHAR_CHECKED:
                # Recupera il nome dell'owner dal suo ID nascosto nel campo 'text'
                owner_name = self.tree.item(row_id, 'text')
                for owner, tasks in self.analysis_data.items():
                    if owner.Nome == owner_name:
                        reminders_to_send[owner] = tasks
                        break

        if not reminders_to_send:
            messagebox.showinfo("Info", "Nessun responsabile selezionato per l'invio.", parent=self)
            return

        if not messagebox.askyesno("Conferma invio",
                                   f"Sei sicuro di voler inviare solleciti a {len(reminders_to_send)} persone?",
                                   parent=self):
            return

        self.send_button.config(state=tk.DISABLED)
        # ... resto del metodo invariato
        self._log_message(f"Invio solleciti a {len(reminders_to_send)} responsabili...")
        self.update_idletasks()
        try:
            sent, failed = self.npi_manager.send_project_reminders(reminders_to_send, self.final_milestone)
            success_msg = f"Processo completato. Email inviate: {sent}. Fallite: {failed}."
            self._log_message(success_msg)
            messagebox.showinfo("Successo", success_msg, parent=self)
        except Exception as e:
            error_msg = f"ERRORE CRITICO durante l'invio: {e}"
            self._log_message(error_msg)
            logger.critical(f"Errore invio solleciti per progetto {self.project_id}: {e}", exc_info=True)
            messagebox.showerror("Errore Invio", error_msg, parent=self)
        finally:
            self.send_button.config(state=tk.NORMAL)

    def _log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)