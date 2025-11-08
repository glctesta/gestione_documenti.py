# File: npi/windows/project_window.py (VERSIONE CORRETTA SECONDO IL MODELLO DATI)
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

logger = logging.getLogger(__name__)

class ProjectWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, project_id):
        super().__init__(master)
        if project_id is None:
            print("ERRORE CRITICO: ProjectWindow chiamato con project_id=None!")
            import traceback
            print("Stack trace:")
            for line in traceback.format_stack()[-3:]:
                print(line.strip())
            self.destroy()
            return
        # DEBUG - verifica i parametri ricevuti
        print(f"DEBUG ProjectWindow: project_id ricevuto = {project_id}")
        print(f"DEBUG ProjectWindow: tipo project_id = {type(project_id)}")
        print(f"DEBUG ProjectWindow: npi_manager = {npi_manager}")
        print(f"DEBUG ProjectWindow: lang = {lang}")
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.progetto = None
        self.soggetti_map = {}
        self.soggetti_map_rev = {}

        self.status_map_display = {
            'Da Fare': self.lang.get('status_todo'),
            'In Lavorazione': self.lang.get('status_wip'),
            'Completato': self.lang.get('status_done'),
            'Bloccato': self.lang.get('status_blocked'),
        }
        self.status_map_db = {v: k for k, v in self.status_map_display.items()}

        self.geometry("1400x800")
        self.title(self.lang.get('project_window_title'))
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self._load_project_data()

    def _create_widgets(self):
        header_frame = ttk.LabelFrame(self, text=self.lang.get('project_info_title'), padding=10)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.header_label = ttk.Label(header_frame, text="...", font=('Helvetica', 12))
        self.header_label.pack(side=tk.LEFT)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=3)

        cols = (self.lang.get('col_task_name'), self.lang.get('col_category'), self.lang.get('col_owner'),
                self.lang.get('col_status'), self.lang.get('col_due_date'))
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=250);
        self.tree.column(cols[1], width=150);
        self.tree.column(cols[2], width=120)
        self.tree.column(cols[3], width=100);
        self.tree.column(cols[4], width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)

        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('task_details_title'), padding=10)
        paned_window.add(form_frame, weight=2)

        self.fields = {}
        labels = [
            ('task_name', self.lang.get('label_task_name'), 'label'),
            ('task_category', self.lang.get('label_category'), 'label'),
            ('OwnerID', self.lang.get('label_owner'), 'combo'),
            ('Stato', self.lang.get('label_status'), 'combo'),
            ('DataScadenza', self.lang.get('label_due_date'), 'date'),  # CAMPO CAMBIATO
            ('DataInizio', self.lang.get('label_start_date'), 'date'),  # CAMPO CAMBIATO
            ('DataCompletamento', self.lang.get('label_completion_date'), 'date'),  # CAMPO CAMBIATO
            ('Note', self.lang.get('label_notes'), 'text')
        ]

        for i, (field_name, label_text, widget_type) in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=tk.NW, pady=5, padx=5)
            if widget_type == 'label':
                self.fields[field_name] = ttk.Label(form_frame, text="", wraplength=300)
            elif widget_type == 'combo':
                self.fields[field_name] = ttk.Combobox(form_frame, state='readonly')
            elif widget_type == 'date':
                self.fields[field_name] = DateEntry(form_frame, width=12, date_pattern='dd/MM/yyyy', state='readonly')
            elif widget_type == 'text':
                self.fields[field_name] = tk.Text(form_frame, height=8, width=40)
            self.fields[field_name].grid(row=i, column=1, sticky=tk.EW, pady=5, padx=5)

        form_frame.columnconfigure(1, weight=1);
        self.fields['Note'].grid_configure(sticky=tk.NSEW)
        form_frame.rowconfigure(labels.index(('Note', self.lang.get('label_notes'), 'text')), weight=1)

        ttk.Button(form_frame, text=self.lang.get('btn_save_changes'), command=self._save_task_details).grid(
            row=len(labels), column=1, sticky=tk.E, pady=20)
        self._disable_form()

    def _load_project_data(self):
        soggetti = self.npi_manager.get_soggetti()
        self.soggetti_map = {s.NomeSoggetto: s.SoggettoID for s in soggetti}
        self.soggetti_map_rev = {v: k for k, v in self.soggetti_map.items()}
        self.fields['OwnerID']['values'] = [''] + list(self.soggetti_map.keys())
        self.fields['Stato']['values'] = list(self.status_map_display.values())

        self.progetto = self.npi_manager.get_dettagli_progetto(self.project_id)
        if not self.progetto:
            logger.error('_load_project_data:Progetto non trovato')
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_project_not_found'), parent=self)
            self.destroy()
            return

        title = f"{self.progetto.prodotto.CodiceProdotto or 'N/A'} - {self.progetto.prodotto.NomeProdotto}"
        self.header_label.config(text=title)
        for i in self.tree.get_children(): self.tree.delete(i)

        # Gestiamo il caso (improbabile) di zero waves
        if not self.progetto.waves: return
        wave = self.progetto.waves[0]  # Assumiamo di lavorare sulla prima wave per ora

        for task in sorted(wave.tasks, key=lambda t: t.task_template.ItemID):
            owner_name = task.owner.NomeSoggetto if task.owner else ""
            due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else ""
            status_display = self.status_map_display.get(task.Stato, task.Stato)

            self.tree.insert('', tk.END, text=task.TaskProdottoID, values=(  # text ora ha ID corretto
                task.task_template.NomeTask,
                task.task_template.category.Category if task.task_template.category else "",
                owner_name,
                status_display,
                due_date
            ))
        self._disable_form()


    def _on_task_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        self._enable_form()

        try:
            # --- MODIFICA CHIAVE QUI ---
            # Convertiamo in intero l'ID del task recuperato dalla Treeview.
            task_id_str = self.tree.item(selection[0], 'text')
            task_id = int(task_id_str)
            # --- FINE MODIFICA ---

            # Trova il task nella prima wave (ora il confronto funzionerà)
            selected_task = next((t for t in self.progetto.waves[0].tasks if t.TaskProdottoID == task_id), None)

            if selected_task:
                self._populate_form(selected_task)
            else:
                # Se il task non viene trovato per qualche motivo, disabilita il form per sicurezza
                self._disable_form()

        except (ValueError, TypeError):
            # Se 'text' non è un numero valido, disabilitiamo il form per evitare errori
            self._disable_form()

    def _populate_form(self, task):
        self.current_task_id = task.TaskProdottoID
        self.fields['task_name'].config(text=task.task_template.NomeTask)
        self.fields['task_category'].config(
            text=task.task_template.category.Category if task.task_template.category else "")

        self.fields['OwnerID'].set(self.soggetti_map_rev.get(task.OwnerID, ""))
        self.fields['Stato'].set(self.status_map_display.get(task.Stato, task.Stato))

        self.fields['Note'].delete('1.0', tk.END)
        if task.Note: self.fields['Note'].insert('1.0', task.Note)

        self.fields['DataScadenza'].set_date(task.DataScadenza)
        self.fields['DataInizio'].set_date(task.DataInizio)
        self.fields['DataCompletamento'].set_date(task.DataCompletamento)

    def _save_task_details(self):
        if not hasattr(self, 'current_task_id') or self.current_task_id is None: return

        data = {
            'OwnerID': self.soggetti_map.get(self.fields['OwnerID'].get()),
            'Stato': self.status_map_db.get(self.fields['Stato'].get(), 'Da Fare'),
            'Note': self.fields['Note'].get('1.0', tk.END).strip(),
            'DataScadenza': self.fields['DataScadenza'].get(),
            'DataInizio': self.fields['DataInizio'].get(),
            'DataCompletamento': self.fields['DataCompletamento'].get()
        }

        try:
            self.npi_manager.update_task_prodotto(self.current_task_id, data)

            # AGGIUNTA: Chiedi conferma per inviare notifiche
            if messagebox.askyesno(
                    self.lang.get('notification_send_title', 'Conferma Invio Notifiche'),
                    self.lang.get('notification_send_prompt', 'Vuoi inviare le notifiche per questo task?'),
                    parent=self
            ):
                # Recupera il task aggiornato
                task_aggiornato = self._get_task_by_id(self.current_task_id)
                if task_aggiornato:
                    # Invia notifiche
                    success = self.npi_manager.invia_notifiche_task(
                        task_aggiornato,
                        conferma_utente=False,  # Già confermato
                        lang=self.lang
                    )
                    if success:
                        messagebox.showinfo(
                            self.lang.get('success_title'),
                            self.lang.get('notification_sent_success', 'Notifiche inviate con successo'),
                            parent=self
                        )

            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_task_updated'), parent=self)
            self._load_project_data()

        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'), f"{self.lang.get('db_error_save_task')}\n{e}",
                                 parent=self)

    def _get_task_by_id(self, task_id):
        """Helper method per recuperare un task dal progetto corrente."""
        if not self.progetto or not self.progetto.waves:
            return None
        return next((t for t in self.progetto.waves[0].tasks if t.TaskProdottoID == task_id), None)

    def _disable_form(self):
        self.current_task_id = None
        for child in self.fields.values():
            if isinstance(child, tk.Text):
                child.config(state='disabled')
            else:
                child.config(state='disabled')

    def _enable_form(self):
        for name, child in self.fields.items():
            if name in ['task_name', 'task_category']: continue
            if isinstance(child, (DateEntry, ttk.Combobox)):
                child.config(state='readonly')
            elif isinstance(child, tk.Text):
                child.config(state='normal')