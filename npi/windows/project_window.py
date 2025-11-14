import logging
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from  .import_tasks_window import ImportTasksWindow
logger = logging.getLogger(__name__)


class ProjectWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, project_id):
        super().__init__(master)
        if project_id is None:
            self.destroy()
            return

        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.progetto = None
        self.soggetti_map = {}
        self.soggetti_map_rev = {}

        self.status_map_display = {
            'Da Fare': self.lang.get('status_todo', 'Da Fare'),
            'In Lavorazione': self.lang.get('status_wip', 'In Lavorazione'),
            'Completato': self.lang.get('status_done', 'Completato'),
            'Bloccato': self.lang.get('status_blocked', 'Bloccato'),
        }
        self.status_map_db = {v: k for k, v in self.status_map_display.items()}

        self.geometry("1400x800")
        self.title(self.lang.get('project_window_title'))
        self.transient(master)
        self.grab_set()

        self.show_assigned_var = tk.BooleanVar(value=True)

        self._create_widgets()
        self._load_project_data()

    def _create_widgets(self):
        # Header Frame
        header_frame = ttk.LabelFrame(self, text=self.lang.get('project_info_title'), padding=10)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.header_label = ttk.Label(header_frame, text="...", font=('Helvetica', 12))
        self.header_label.pack(side=tk.LEFT, padx=(0, 20))

        btn_save_dates = ttk.Button(header_frame, text=self.lang.get('btn_save_dates', "Salva Date"),
                                    command=self._save_project_dates)
        btn_save_dates.pack(side=tk.RIGHT, padx=5)

        ttk.Label(header_frame, text=self.lang.get('label_project_due_date', "Scadenza Progetto:")).pack(side=tk.RIGHT,
                                                                                                         padx=(10, 5))
        self.project_due_date_entry = DateEntry(header_frame, width=12, date_pattern='dd/MM/yyyy', state='readonly')
        self.project_due_date_entry.pack(side=tk.RIGHT)

        ttk.Label(header_frame, text=self.lang.get('label_project_start_date', "Inizio Progetto:")).pack(side=tk.RIGHT,
                                                                                                         padx=(10, 5))
        self.project_start_date_entry = DateEntry(header_frame, width=12, date_pattern='dd/MM/yyyy', state='readonly')
        self.project_start_date_entry.pack(side=tk.RIGHT)

        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview (lista task)
        list_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(list_frame, weight=3)

        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=(0, 5))

        filter_check = ttk.Checkbutton(
            action_frame,
            text=self.lang.get('show_assigned_tasks', 'Mostra assegnati'),
            variable=self.show_assigned_var,
            onvalue=True,
            offvalue=False,
            command=self._populate_treeview  # Richiama il ricaricamento del tree
        )
        filter_check.pack(side=tk.LEFT, padx=(0, 20))

        self.import_button = ttk.Button(
            action_frame,
            text=self.lang.get('btn_import_tasks', 'Importa Assegnamenti...'),
            command=self._launch_import_tasks_window,
            state=tk.DISABLED  # Parte disabilitato
        )
        self.import_button.pack(side=tk.LEFT)

        cols = (self.lang.get('col_task_name'), self.lang.get('col_category'), self.lang.get('col_owner'),
                self.lang.get('col_status'), self.lang.get('col_due_date'))
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column(cols[0], width=250);
        self.tree.column(cols[1], width=150)
        self.tree.column(cols[2], width=120);
        self.tree.column(cols[3], width=100)
        self.tree.column(cols[4], width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)

        self.tree.tag_configure('special_task', foreground='red', font=('Helvetica', 9, 'bold'))

        # Form dettagli task
        form_frame = ttk.LabelFrame(paned_window, text=self.lang.get('task_details_title'), padding=10)
        paned_window.add(form_frame, weight=2)

        self.fields = {}
        labels = [
            ('task_name', self.lang.get('label_task_name'), 'label'),
            ('task_category', self.lang.get('label_category'), 'label'),
            ('OwnerID', self.lang.get('label_owner'), 'combo'),
            ('Stato', self.lang.get('label_status'), 'combo'),
            ('DataScadenza', self.lang.get('label_due_date'), 'date'),
            ('DataInizio', self.lang.get('label_start_date'), 'date'),
            ('DataCompletamento', self.lang.get('label_completion_date'), 'date'),
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
        form_frame.columnconfigure(1, weight=1)
        self.fields['Note'].grid_configure(sticky=tk.NSEW)
        form_frame.rowconfigure(labels.index(('Note', self.lang.get('label_notes'), 'text')), weight=1)
        ttk.Button(form_frame, text=self.lang.get('btn_save_changes'), command=self._save_task_details).grid(
            row=len(labels), column=1, sticky=tk.E, pady=20)
        self._disable_form()

    # def _load_project_data(self):
    #     soggetti = self.npi_manager.get_soggetti()
    #     self.soggetti_map = {s.Nome: s.SoggettoId for s in soggetti}
    #     self.soggetti_map_rev = {v: k for k, v in self.soggetti_map.items()}
    #     self.fields['OwnerID']['values'] = [''] + list(self.soggetti_map.keys())
    #     self.fields['Stato']['values'] = list(self.status_map_display.values())
    #
    #     # Carica il progetto completo con tutti i task
    #     self.progetto = self.npi_manager.get_dettagli_progetto(self.project_id)
    #     if not self.progetto:
    #         logger.error('_load_project_data: Progetto non trovato')
    #         self.destroy();
    #         return
    #
    #     title = f"{self.progetto.prodotto.CodiceProdotto or 'N/A'} - {self.progetto.prodotto.NomeProdotto}"
    #     self.header_label.config(text=title)
    #     self.project_start_date_entry.set_date(self.progetto.DataInizio)
    #     self.project_due_date_entry.set_date(self.progetto.ScadenzaProgetto)
    #
    #     for i in self.tree.get_children(): self.tree.delete(i)
    #
    #     if not self.progetto.waves: return
    #     wave = self.progetto.waves[0]
    #
    #     for task in sorted(wave.tasks, key=lambda t: t.task_catalogo.ItemID if t.task_catalogo else ''):
    #         owner_name = task.owner.Nome if task.owner else ""
    #         due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else ""
    #         status_display = self.status_map_display.get(task.Stato, task.Stato)
    #
    #         # ** LA CORREZIONE È QUI **
    #         tags_to_apply = ()  # Sempre inizializzato a un valore di default
    #
    #         category_name = ""
    #         task_name = "Task di catalogo non trovato"
    #
    #         if task.task_catalogo:
    #             task_name = task.task_catalogo.NomeTask
    #             if task.task_catalogo.categoria:
    #                 category_name = task.task_catalogo.categoria.Category
    #
    #             if task.task_catalogo.IsFinalMilestone:
    #                 tags_to_apply = ('special_task',)
    #
    #         self.tree.insert('', tk.END, text=task.TaskProdottoID, values=(
    #             task_name, category_name, owner_name, status_display, due_date
    #         ), tags=tags_to_apply)
    #
    #     self._disable_form()

    def _load_project_data(self):
        """Carica i dati principali del progetto UNA SOLA VOLTA."""
        soggetti = self.npi_manager.get_soggetti()
        self.soggetti_map = {s.Nome: s.SoggettoId for s in soggetti}
        self.soggetti_map_rev = {v: k for k, v in self.soggetti_map.items()}
        self.fields['OwnerID']['values'] = [''] + list(self.soggetti_map.keys())
        self.fields['Stato']['values'] = list(self.status_map_display.values())

        # Carica il progetto completo con tutti i task
        self.progetto = self.npi_manager.get_dettagli_progetto(self.project_id)
        if not self.progetto:
            logger.error('_load_project_data: Progetto non trovato')
            self.destroy();
            return

        title = f"{self.progetto.prodotto.CodiceProdotto or 'N/A'} - {self.progetto.prodotto.NomeProdotto}"
        self.header_label.config(text=title)
        self.project_start_date_entry.set_date(self.progetto.DataInizio)
        self.project_due_date_entry.set_date(self.progetto.ScadenzaProgetto)

        # Ora popola la vista, che applicherà i filtri
        self._populate_treeview()
        self._disable_form()

    def _populate_treeview(self):
        """Popola o ri-popola la TreeView applicando i filtri correnti."""
        for i in self.tree.get_children(): self.tree.delete(i)

        if not self.progetto or not self.progetto.waves: return

        wave = self.progetto.waves[0]

        # Controlla se ci sono task assegnati
        has_assigned_tasks = any(task.OwnerID is not None for task in wave.tasks)
        self.import_button.config(state=tk.DISABLED if has_assigned_tasks else tk.NORMAL)

        # Applica il filtro
        show_assigned = self.show_assigned_var.get()

        for task in sorted(wave.tasks, key=lambda t: t.task_catalogo.ItemID if t.task_catalogo else ''):
            is_assigned = task.OwnerID is not None

            # Condizione filtro
            if (show_assigned and not is_assigned) or (not show_assigned and is_assigned):
                continue

            owner_name = task.owner.Nome if task.owner else ""
            due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else ""
            status_display = self.status_map_display.get(task.Stato, task.Stato)

            tags_to_apply = ()
            category_name = ""
            task_name = "Task di catalogo non trovato"

            if task.task_catalogo:
                task_name = task.task_catalogo.NomeTask
                if task.task_catalogo.categoria: category_name = task.task_catalogo.categoria.Category
                if task.task_catalogo.IsFinalMilestone: tags_to_apply = ('special_task',)

            self.tree.insert('', tk.END, text=task.TaskProdottoID, values=(
                task_name, category_name, owner_name, status_display, due_date
            ), tags=tags_to_apply)

    def _launch_import_tasks_window(self):
        """Apre la finestra per importare gli assegnamenti."""
        win = ImportTasksWindow(self, self.npi_manager, self.lang, self.project_id)
        self.wait_window(win)  # Aspetta che la finestra di import venga chiusa

        # Ricarica tutto per riflettere le modifiche
        self._load_project_data()

    def _save_project_dates(self):
        try:
            start_date_str = self.project_start_date_entry.get()
            due_date_str = self.project_due_date_entry.get()
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y') if start_date_str else None
            due_date = datetime.strptime(due_date_str, '%d/%m/%Y') if due_date_str else None

            # La logica di business e validazione è nel manager
            updated_project, override_message = self.npi_manager.update_project_dates(
                self.project_id, start_date, due_date
            )

            messagebox.showinfo(
                self.lang.get('success_title'),
                self.lang.get('success_project_dates_updated', "Date del progetto aggiornate con successo."),
                parent=self
            )

            if override_message:
                messagebox.showinfo(self.lang.get('info_title', 'Informazione'), override_message, parent=self)

            self._load_project_data()

        except ValueError as ve:
            messagebox.showerror(self.lang.get('error_title'), str(ve), parent=self)
        except Exception as e:
            logger.error(f"Errore durante il salvataggio date progetto: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('db_error_title'), f"{self.lang.get('db_error_generic_save')}\n{e}",
                                 parent=self)

    def _on_task_select(self, event=None):
        selection = self.tree.selection()
        if not selection: return
        self._enable_form()
        try:
            task_id = int(self.tree.item(selection[0], 'text'))
            selected_task = next((t for t in self.progetto.waves[0].tasks if t.TaskProdottoID == task_id), None)
            if selected_task:
                self._populate_form(selected_task)
            else:
                self._disable_form()
        except (ValueError, TypeError):
            self._disable_form()

    def _populate_form(self, task):
        self.current_task_id = task.TaskProdottoID
        category_name = ""
        task_name = "Task di catalogo non trovato"
        if task.task_catalogo:
            task_name = task.task_catalogo.NomeTask
            if task.task_catalogo.categoria: category_name = task.task_catalogo.categoria.Category
        self.fields['task_name'].config(text=task_name)
        self.fields['task_category'].config(text=category_name)
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
            if messagebox.askyesno(
                    self.lang.get('notification_send_title', 'Conferma Invio Notifiche'),
                    self.lang.get('notification_send_prompt', 'Vuoi inviare le notifiche per questo task?'),
                    parent=self
            ):
                task_aggiornato = self._get_task_by_id(self.current_task_id)
                if task_aggiornato: self.npi_manager.invia_notifiche_task(task_aggiornato, conferma_utente=False,
                                                                          lang=self.lang)
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('success_task_updated'), parent=self)
            self._load_project_data()
        except Exception as e:
            messagebox.showerror(self.lang.get('db_error_title'), f"{self.lang.get('db_error_save_task')}\n{e}",
                                 parent=self)

    def _get_task_by_id(self, task_id):
        if not self.progetto or not self.progetto.waves: return None
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
