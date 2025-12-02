# File: npi/windows/project_window.py (VERSIONE COMPLETA E CORRETTA)

import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import openpyxl
from openpyxl.styles import Alignment
from tkcalendar import DateEntry
from datetime import datetime

try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
except ImportError:
    openpyxl = None

# Assicurati che i percorsi di importazione siano corretti per la tua struttura
from .import_tasks_window import ImportTasksWindow
from .task_documents_window import TaskDocumentsWindow

logger = logging.getLogger(__name__)


class ProjectWindow(tk.Toplevel):

    def __init__(self, master, npi_manager, lang, project_id, master_app, logged_in_user: str,
                 final_customers: list = None):
        super().__init__(master)
        if project_id is None:
            self.destroy()
            return

        if openpyxl is None:
            messagebox.showerror("Libreria Mancante",
                                 "La libreria 'openpyxl' è necessaria per l'esportazione Excel.\n"
                                 "Installala con: pip install openpyxl", parent=self)
            # Non blocchiamo la finestra, ma l'esportazione non funzionerà

        # 1. Imposta gli attributi di base
        self.npi_manager = npi_manager
        self.lang = lang
        self.project_id = project_id
        self.master_app = master_app
        self.logged_in_user = logged_in_user

        if not self.logged_in_user:
            logger.error("ProjectWindow aperta senza un nome utente valido.")
            messagebox.showerror("Errore Critico", "Utente non valido.", parent=master)
            self.destroy()
            return

        # 2. Inizializza le variabili e i dizionari di stato
        self.progetto = None
        self.current_task_id = None
        self.soggetti_map = {}
        self.soggetti_map_rev = {}
        self.doc_types_map = {}
        self.doc_types_map_rev = {}
        self.selected_file_path = None
        self.selected_file_data = None
        self.active_docs_for_task = {}
        self.doc_types_properties = {}
        

        # Mappe per clienti finali
        self.final_customers = final_customers if final_customers else []

        try:
            self.final_clients_map = {fc[1]: fc[0] for fc in self.final_customers}
            self.final_clients_map_rev = {v: k for k, v in self.final_clients_map.items()}
        except AttributeError as e:
            messagebox.showerror("Errore di Configurazione",
                                 f"Impossibile mappare i clienti finali. Attributo non trovato: {e}\nControlla i nomi delle colonne nel modello dati.",
                                 parent=self)
            self.final_clients_map = {}
            self.final_clients_map_rev = {}

        self.fields = {}
        self.doc_widgets = {}

        self.status_map_display = {
            'Da Fare': self.lang.get('status_todo', 'Da Fare'),
            'In Lavorazione': self.lang.get('status_wip', 'In Lavorazione'),
            'Completato': self.lang.get('status_done', 'Completato'),
            'Bloccato': self.lang.get('status_blocked', 'Bloccato'),
        }
        self.status_map_db = {v: k for k, v in self.status_map_display.items()}

        self.geometry("1400x900")
        self.title(self.lang.get('project_window_title', 'Gestione Progetto NPI'))
        self.transient(master)
        self.grab_set()

        self.show_assigned_var = tk.BooleanVar(value=True)
        self._create_widgets()

    def _create_widgets(self):
        # Main Layout
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.header_label = ttk.Label(header_frame, text="", font=('Segoe UI', 16, 'bold'))
        self.header_label.pack(side=tk.LEFT)

        # Buttons in Header (Moved here as requested)
        self.import_button = ttk.Button(header_frame, text=self.lang.get('btn_import_tasks', 'Importa Task'), command=self._launch_import_tasks_window)
        self.import_button.pack(side=tk.LEFT, padx=10)
        
        self.export_button = ttk.Button(header_frame, text=self.lang.get('btn_export_excel', 'Export Excel'), command=self._export_cost_report, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(header_frame, text=self.lang.get('show_assigned', 'Mostra Assegnati'), variable=self.show_assigned_var, command=self._populate_treeview).pack(side=tk.LEFT, padx=5)

        # Project Dates
        dates_frame = ttk.LabelFrame(header_frame, text=self.lang.get('project_dates_title', 'Date Progetto'))
        dates_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(dates_frame, text=self.lang.get('start_date', 'Inizio:')).pack(side=tk.LEFT, padx=5)
        self.project_start_date_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.project_start_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dates_frame, text=self.lang.get('due_date', 'Scadenza:')).pack(side=tk.LEFT, padx=5)
        self.project_due_date_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.project_due_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(dates_frame, text=self.lang.get('save_dates', 'Salva Date'), command=self._save_project_dates).pack(side=tk.LEFT, padx=5)

        # Content Split
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left Panel: Treeview
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        columns = ('Name', 'Category', 'Owner', 'Status', 'DueDate')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings')
        self.tree.heading('Name', text=self.lang.get('col_task', 'Task'))
        self.tree.heading('Category', text=self.lang.get('col_category', 'Categoria'))
        self.tree.heading('Owner', text=self.lang.get('col_owner', 'Assegnato a'))
        self.tree.heading('Status', text=self.lang.get('col_status', 'Stato'))
        self.tree.heading('DueDate', text=self.lang.get('col_due_date', 'Scadenza'))
        
        self.tree.column('Name', width=200)
        self.tree.column('Category', width=100)
        self.tree.column('Owner', width=100)
        self.tree.column('Status', width=100)
        self.tree.column('DueDate', width=80)
        
        self.tree.tag_configure('special_task', foreground='red')
        self.tree.tag_configure('bold_task', font=('Segoe UI', 9, 'bold'))
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right Panel: Details
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        # Task Details Form
        details_frame = ttk.LabelFrame(right_frame, text=self.lang.get('task_details', 'Dettagli Task'))
        details_frame.pack(fill=tk.X, padx=5, pady=5)

        # Fields
        grid_frame = ttk.Frame(details_frame)
        grid_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Name & Category (Read-only)
        ttk.Label(grid_frame, text=self.lang.get('label_task', 'Task:')).grid(row=0, column=0, sticky=tk.W)
        self.fields['task_name'] = ttk.Label(grid_frame, text="", font=('Segoe UI', 10, 'bold'))
        self.fields['task_name'].grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(grid_frame, text=self.lang.get('label_category', 'Categoria:')).grid(row=1, column=0, sticky=tk.W)
        self.fields['task_category'] = ttk.Label(grid_frame, text="")
        self.fields['task_category'].grid(row=1, column=1, sticky=tk.W)

        # Editable Fields
        labels_config = [
            ('OwnerID', self.lang.get('label_owner', 'Assegnato a'), 'combo'),
            ('Stato', self.lang.get('label_status', 'Stato'), 'combo'),
            ('DataInizio', self.lang.get('label_start_date', 'Data Inizio'), 'date'),
            ('DataScadenza', self.lang.get('label_due_date', 'Data Scadenza'), 'date'),
            ('DataCompletamento', self.lang.get('label_completion_date', 'Data Completamento'), 'date'),
        ]

        r = 2
        for field_name, label_text, widget_type in labels_config:
            ttk.Label(grid_frame, text=label_text).grid(row=r, column=0, sticky=tk.W, pady=2)
            if widget_type == 'combo':
                w = ttk.Combobox(grid_frame, state='readonly')
            elif widget_type == 'date':
                w = DateEntry(grid_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            self.fields[field_name] = w
            w.grid(row=r, column=1, sticky=tk.EW, pady=2)
            r += 1

        # Checkbox IsPostFinalMilestone
        self.fields['IsPostFinalMilestone'] = ttk.Checkbutton(grid_frame, text="Target NPI", command=self._on_target_npi_change)
        self.fields['IsPostFinalMilestone'].var = tk.BooleanVar()
        self.fields['IsPostFinalMilestone'].config(variable=self.fields['IsPostFinalMilestone'].var)
        self.fields['IsPostFinalMilestone'].grid(row=r, column=1, sticky=tk.W, pady=2)
        r += 1

        # Notes
        ttk.Label(grid_frame, text=self.lang.get('label_notes', 'Note')).grid(row=r, column=0, sticky=tk.NW, pady=2)
        self.fields['Note'] = tk.Text(grid_frame, height=4, width=40)
        self.fields['Note'].grid(row=r, column=1, sticky=tk.EW, pady=2)
        r += 1

        ttk.Button(details_frame, text=self.lang.get('btn_save', 'Salva Modifiche'), command=self._save_task_details).pack(pady=5)

        # Documents Section
        doc_frame = ttk.LabelFrame(right_frame, text=self.lang.get('documents_title', 'Documenti'))
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Doc Form
        df = ttk.Frame(doc_frame)
        df.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(df, text=self.lang.get('doc_type', 'Tipo:')).grid(row=0, column=0, sticky=tk.W)
        self.doc_widgets['type'] = ttk.Combobox(df, state='readonly')
        self.doc_widgets['type'].grid(row=0, column=1, columnspan=2, sticky=tk.EW)
        self.doc_widgets['type'].bind('<<ComboboxSelected>>', self._on_doc_type_selected)

        ttk.Label(df, text=self.lang.get('doc_title', 'Titolo:')).grid(row=1, column=0, sticky=tk.W)
        self.doc_widgets['title'] = ttk.Entry(df)
        self.doc_widgets['title'].grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        ttk.Label(df, text=self.lang.get('final_client', 'Cliente Finale:')).grid(row=2, column=0, sticky=tk.W)
        self.doc_widgets['final_client'] = ttk.Combobox(df, values=[fc[0] for fc in self.final_customers])
        self.doc_widgets['final_client'].grid(row=2, column=1, columnspan=2, sticky=tk.EW)

        # Dynamic fields
        self.doc_widgets['value_label'] = ttk.Label(df, text=self.lang.get('doc_value', 'Valore (€):'))
        self.doc_widgets['value_entry'] = ttk.Entry(df)
        
        self.doc_widgets['due_date_label'] = ttk.Label(df, text=self.lang.get('doc_due_date', 'Scadenza Doc:'))
        self.doc_widgets['due_date_entry'] = DateEntry(df, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')

        # Replacement logic
        self.doc_widgets['is_replacement_var'] = tk.BooleanVar()
        cb = ttk.Checkbutton(df, text=self.lang.get('is_replacement', 'Sostituisce doc esistente'), variable=self.doc_widgets['is_replacement_var'], command=self._toggle_replacement_combo)
        cb.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        self.doc_widgets['replaces_combo'] = ttk.Combobox(df, state='disabled')
        self.doc_widgets['replaces_combo'].grid(row=6, column=0, columnspan=3, sticky=tk.EW)

        # File selection
        ttk.Button(df, text=self.lang.get('select_file', 'Seleziona File...'), command=self._select_file).grid(row=7, column=0, sticky=tk.W)
        self.doc_widgets['file_label'] = ttk.Label(df, text=self.lang.get('no_file_selected', 'Nessun file'))
        self.doc_widgets['file_label'].grid(row=7, column=1, columnspan=2, sticky=tk.W)

        # Note Doc
        ttk.Label(df, text=self.lang.get('notes', 'Note:')).grid(row=8, column=0, sticky=tk.NW)
        self.doc_widgets['note_text'] = tk.Text(df, height=3, width=30)
        self.doc_widgets['note_text'].grid(row=8, column=1, columnspan=2, sticky=tk.EW)

        ttk.Button(df, text=self.lang.get('save_doc', 'Carica Documento'), command=self._save_document).grid(row=9, column=1, pady=5)
        
        self.view_docs_button = ttk.Button(doc_frame, text=self.lang.get('view_docs', 'Vedi Documenti Caricati'), command=self._launch_view_documents_window, state=tk.DISABLED)
        self.view_docs_button.pack(pady=5)

        # Initial call to load data
        self.after(100, self._load_data_and_populate_ui)

    def _on_doc_type_selected(self, event=None):
        doc_type_desc = self.doc_widgets['type'].get()
        if not doc_type_desc: return
        doc_type_id = self.doc_types_map[doc_type_desc]
        props = self.doc_types_properties[doc_type_id]
        if props['has_value']:
            self.doc_widgets['value_label'].grid(row=3, column=0, sticky=tk.W, pady=2)
            self.doc_widgets['value_entry'].grid(row=3, column=1, columnspan=2, sticky=tk.EW, pady=2)
        else:
            self.doc_widgets['value_label'].grid_remove()
            self.doc_widgets['value_entry'].grid_remove()
        if props['check_date']:
            self.doc_widgets['due_date_label'].grid(row=4, column=0, sticky=tk.W, pady=2)
            self.doc_widgets['due_date_entry'].grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=2)
        else:
            self.doc_widgets['due_date_label'].grid_remove()
            self.doc_widgets['due_date_entry'].grid_remove()

    def _load_data_and_populate_ui(self):
        try:
            soggetti = self.npi_manager.get_soggetti()
            self.soggetti_map = {s.Nome: s.SoggettoId for s in soggetti}
            self.soggetti_map_rev = {v: k for k, v in self.soggetti_map.items()}
            self.fields['OwnerID']['values'] = [''] + list(self.soggetti_map.keys())
            self.fields['Stato']['values'] = list(self.status_map_display.values())

            doc_types = self.npi_manager.get_npi_document_types()
            self.doc_types_map = {dt.NpiDocumentDescription: dt.NpiDocumentTypeId for dt in doc_types}
            self.doc_types_map_rev = {v: k for k, v in self.doc_types_map.items()}
            self.doc_types_properties = {dt.NpiDocumentTypeId: {'has_value': dt.HasValue, 'check_date': dt.CheckDate}
                                         for dt in doc_types}
            self.doc_widgets['type']['values'] = list(self.doc_types_map.keys())

            self.progetto = self.npi_manager.get_dettagli_progetto(self.project_id)
            if not self.progetto: raise ValueError("Progetto non trovato.")

            title = f"{self.progetto.prodotto.CodiceProdotto or 'N/A'} - {self.progetto.prodotto.NomeProdotto}"
            self.header_label.config(text=title)
            self.project_start_date_entry.set_date(self.progetto.DataInizio)
            self.project_due_date_entry.set_date(self.progetto.ScadenzaProgetto)

            self._populate_treeview()

            if openpyxl: self.export_button.config(state=tk.NORMAL)

        except Exception as e:
            logger.error(f"Errore caricamento dati: {e}", exc_info=True)
            messagebox.showerror("Errore Caricamento", f"Impossibile caricare i dati:\n{e}", parent=self)
            self.destroy()

        self._disable_form()
        self._disable_doc_form()

    def _export_cost_report(self):
        if not self.progetto:
            messagebox.showwarning("Warning", "No project loaded.", parent=self)
            return

        temp_dir = "C:\\temp"
        try:
            os.makedirs(temp_dir, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Folder Creation Error", f"Could not create folder {temp_dir}:\n{e}", parent=self)
            return

        product_code_file = self.progetto.prodotto.CodiceProdotto.replace(" ",
                                                                          "_") if self.progetto.prodotto.CodiceProdotto else "NO_CODE"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(temp_dir, f"Cost_Report_{product_code_file}_{timestamp}.xlsx")

        messagebox.showinfo("Exporting", f"Creating the report...\nThe file will be saved in:\n{file_path}",
                            parent=self)
        self.update_idletasks()

        report_rows = []
        grand_total = 0.0

        for task in self.progetto.waves[0].tasks:
            if task.documents:
                task_total = 0.0
                task_docs_data = []
                for doc in task.documents:
                    if doc.ValueInEur and doc.ValueInEur > 0:
                        doc_value = doc.ValueInEur
                        task_docs_data.append([
                            doc.document_type.NpiDocumentDescription if doc.document_type else "N/A",
                            doc.DocumentTitle,
                            doc_value
                        ])
                        task_total += doc_value

                if task_docs_data:
                    task_name = task.task_catalogo.NomeTask if task.task_catalogo else "Unknown Task"
                    report_rows.append({'type': 'task', 'data': [task_name]})
                    for doc_data in task_docs_data:
                        report_rows.append({'type': 'doc', 'data': doc_data})
                    report_rows.append({'type': 'subtotal', 'data': ["Task Subtotal", "", task_total]})
                    grand_total += task_total

        if not report_rows:
            messagebox.showinfo("No Data", "No documents with costs found for this project.", parent=self)
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Cost Report"

            bold_font = Font(bold=True)
            header_font = Font(bold=True, size=14)
            currency_format = '#,##0.00 "€"'  # Formato valuta

            ws.merge_cells('A1:C1');
            cell = ws['A1']
            cell.value = f"Project Cost Report: {self.progetto.prodotto.NomeProdotto}"
            cell.font = header_font;
            cell.alignment = Alignment(horizontal='center')
            ws.merge_cells('A2:C2');
            cell = ws['A2']
            cell.value = f"Product Code: {self.progetto.prodotto.CodiceProdotto or 'N/A'}"
            cell.font = bold_font

            headers = ["Task / Document Type", "Document Title", "Cost (€)"]
            ws.append([])
            ws.append(headers)
            for col_letter in ['A', 'B', 'C']: ws[f'{col_letter}4'].font = bold_font

            for row_info in report_rows:
                row_num = ws.max_row + 1
                if row_info['type'] == 'task':
                    ws.cell(row_num, 1).value = row_info['data'][0]
                    ws.cell(row_num, 1).font = bold_font
                elif row_info['type'] == 'doc':
                    ws.cell(row_num, 1).value = f"  {row_info['data'][0]}"
                    ws.cell(row_num, 2).value = row_info['data'][1]
                    cell = ws.cell(row_num, 3)
                    cell.value = row_info['data'][2]
                    cell.number_format = currency_format
                elif row_info['type'] == 'subtotal':
                    ws.cell(row_num, 1).value = row_info['data'][0]
                    ws.cell(row_num, 1).font = bold_font
                    ws.cell(row_num, 1).alignment = Alignment(horizontal='right')
                    cell = ws.cell(row_num, 3)
                    cell.value = row_info['data'][2]
                    cell.font = bold_font
                    cell.number_format = currency_format
                    ws.append([])

            ws.append([])
            total_row = ws.max_row + 1
            ws.cell(total_row, 1).value = "PROJECT GRAND TOTAL"
            ws.cell(total_row, 1).font = header_font
            cell = ws.cell(total_row, 3)
            cell.value = grand_total
            cell.font = header_font
            cell.number_format = currency_format

            for col in ['A', 'B']: ws.column_dimensions[col].width = 50
            ws.column_dimensions['C'].width = 20

            wb.save(file_path)

            if messagebox.askyesno("Export Complete",
                                   f"Cost report saved successfully to:\n{file_path}\n\nDo you want to open the file now?",
                                   parent=self):
                try:
                    os.startfile(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open the file:\n{e}", parent=self)

        except Exception as e:
            logger.error(f"Error creating the Excel file: {e}", exc_info=True)
            messagebox.showerror("Export Error", f"Could not create the Excel file:\n{e}", parent=self)

    def _populate_treeview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        if not self.progetto or not self.progetto.waves: return
        wave = self.progetto.waves[0]
        self.import_button.config(state=tk.DISABLED if any(t.OwnerID is not None for t in wave.tasks) else tk.NORMAL)

        for task in sorted(wave.tasks, key=lambda t: t.task_catalogo.ItemID if t.task_catalogo else ''):

            if self.show_assigned_var.get() != (task.OwnerID is not None): continue

            owner = task.owner.Nome if task.owner else ""
            due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else ""

            # Se la lista dei documenti del task non è vuota, aggiungi un asterisco.
            if task.documents:
                due_date+= " *"

            status = self.status_map_display.get(task.Stato, task.Stato)
            tags = []
            if task.IsPostFinalMilestone:
                tags.append('special_task')
                tags.append('bold_task')
            
            cat = task.task_catalogo.categoria.Category if task.task_catalogo and task.task_catalogo.categoria else ""
            name = task.task_catalogo.NomeTask if task.task_catalogo else "Catalogo non trovato"
            self.tree.insert('', tk.END, text=task.TaskProdottoID, values=(name, cat, owner, status, due_date),
                             tags=tuple(tags))

    def _on_target_npi_change(self):
        """Gestisce il cambio immediato del flag Target NPI."""
        if not self.current_task_id: return
        
        is_target = self.fields['IsPostFinalMilestone'].var.get()
        
        # Se l'utente ha deselezionato, permettiamo (nessun target)
        # Se ha selezionato, chiamiamo il manager per l'esclusività
        
        if is_target:
            try:
                self.npi_manager.set_target_npi_task(self.current_task_id, self.project_id)
                # Aggiorna il modello locale (opzionale se ricarichiamo tutto)
                # Ricarica tutto per aggiornare la treeview e gli altri task
                self._load_data_and_populate_ui()
                # Ripristina la selezione
                # (omesso per semplicità, l'utente vedrà il refresh)
            except Exception as e:
                logger.error(f"Errore impostazione Target NPI: {e}")
                messagebox.showerror("Errore", f"Impossibile impostare il Target NPI:\n{e}", parent=self)
                # Revert checkbox
                self.fields['IsPostFinalMilestone'].var.set(False)
        else:
             # Se deseleziona, dobbiamo aggiornare solo questo task nel DB?
             # La richiesta dice "solo 1 task... deve essere marchato". 
             # Se deseleziono, nessuno è target.
             # Implementiamo un update semplice per questo caso o usiamo set_target_npi_task?
             # set_target_npi_task imposta a True.
             # Per impostare a False, usiamo update_task_prodotto standard o una nuova chiamata.
             # Usiamo update standard per semplicità.
             try:
                 self.npi_manager.update_task_prodotto(self.current_task_id, {'IsPostFinalMilestone': False})
                 self._load_data_and_populate_ui()
             except Exception as e:
                 logger.error(f"Errore rimozione Target NPI: {e}")
                 messagebox.showerror("Errore", f"Impossibile rimuovere il Target NPI:\n{e}", parent=self)
                 self.fields['IsPostFinalMilestone'].var.set(True)

    def _on_task_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            self._disable_form();
            self._disable_doc_form()
            self.view_docs_button.config(state=tk.DISABLED);
            return
        self.current_task_id = int(self.tree.item(sel[0], 'text'))
        task = self._get_task_by_id(self.current_task_id)
        if task:
            self._populate_form(task);
            self._enable_form();
            self._enable_doc_form()
            docs = self.npi_manager.get_documents_for_task(self.current_task_id)
            self.active_docs_for_task = {doc.NpiDocumentId: doc.DocumentTitle for doc in docs if not doc.DateOut}
            self.doc_widgets['replaces_combo']['values'] = list(self.active_docs_for_task.values())
            self.view_docs_button.config(state=tk.NORMAL if docs else tk.DISABLED)
            self._reset_doc_form()
        else:
            self._disable_form();
            self._disable_doc_form()

    def _reset_doc_form(self):
        self.doc_widgets['type'].set('')
        self.doc_widgets['title'].delete(0, tk.END)
        self.doc_widgets['final_client'].set('')
        self.doc_widgets['value_entry'].delete(0, tk.END)
        self.doc_widgets['due_date_entry'].set_date(None)
        self.doc_widgets['replaces_combo'].set('')
        self.doc_widgets['is_replacement_var'].set(False)
        self.doc_widgets['note_text'].delete('1.0', tk.END)
        self.selected_file_path = None
        self.selected_file_data = None
        self.doc_widgets['file_label'].config(text=self.lang.get('no_file_selected'))
        self._toggle_replacement_combo()

    def _populate_form(self, task):
        name = task.task_catalogo.NomeTask if task.task_catalogo else "Task non definito"
        cat = task.task_catalogo.categoria.Category if task.task_catalogo and task.task_catalogo.categoria else ""
        self.fields['task_name'].config(text=name);
        self.fields['task_category'].config(text=cat)
        self.fields['OwnerID'].set(self.soggetti_map_rev.get(task.OwnerID, ""));
        self.fields['Stato'].set(self.status_map_display.get(task.Stato, task.Stato))
        self.fields['Note'].delete('1.0', tk.END);
        self.fields['Note'].insert('1.0', task.Note or "")
        self.fields['DataScadenza'].set_date(task.DataScadenza);
        self.fields['DataInizio'].set_date(task.DataInizio)
        self.fields['DataCompletamento'].set_date(task.DataCompletamento)
        if 'IsPostFinalMilestone' in self.fields:
             self.fields['IsPostFinalMilestone'].var.set(task.IsPostFinalMilestone or False)

    def _disable_form(self):
        self.current_task_id = None
        for child in self.fields.values(): child.config(state='disabled')

    def _enable_form(self):
        for name, child in self.fields.items():
            if name in ['task_name', 'task_category']: continue
            state = 'readonly' if isinstance(child, (DateEntry, ttk.Combobox)) else 'normal'
            child.config(state=state)

    def _disable_doc_form(self):
        for name, widget in self.doc_widgets.items():
            if isinstance(widget, tk.BooleanVar): continue
            widget.config(state=tk.DISABLED)
        self._reset_doc_form()

    def _enable_doc_form(self):
        for name, widget in self.doc_widgets.items():
            if isinstance(widget, tk.BooleanVar): continue
            if name == 'replaces_combo': continue  # Gestito dal toggle
            state = 'readonly' if isinstance(widget, ttk.Combobox) else 'normal'
            widget.config(state=state)

    def _toggle_replacement_combo(self):
        is_replacement = self.doc_widgets['is_replacement_var'].get()
        self.doc_widgets['replaces_combo'].config(state='readonly' if is_replacement else 'disabled')
        if not is_replacement: self.doc_widgets['replaces_combo'].set('')

    def _select_file(self):
        path = filedialog.askopenfilename(title=self.lang.get('select_file_title'), filetypes=[('All', '*.*')])
        if not path: return
        try:
            with open(path, 'rb') as f:
                self.selected_file_data = f.read()
            self.selected_file_path = path
            self.doc_widgets['file_label'].config(text=os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Errore Lettura", f"Impossibile leggere il file:\n{e}", parent=self)
            self.selected_file_path = None;
            self.selected_file_data = None
            self.doc_widgets['file_label'].config(text=self.lang.get('no_file_selected'))

    def _save_document(self):
        if not self.current_task_id: return

        doc_type_desc = self.doc_widgets['type'].get()
        title = self.doc_widgets['title'].get().strip()
        final_client_name = self.doc_widgets['final_client'].get()

        if not all([doc_type_desc, title]):
            messagebox.showwarning("Dati Mancanti", "Tipo Documento e Titolo sono obbligatori.", parent=self)
            return
        if not self.selected_file_data:
            messagebox.showwarning("Dati Mancanti", "Selezionare un file da allegare.", parent=self)
            return

        doc_type_id = self.doc_types_map[doc_type_desc]
        props = self.doc_types_properties[doc_type_id]

        doc_value = float(self.doc_widgets['value_entry'].get() or 0) if props['has_value'] else None
        due_date_str = self.doc_widgets['due_date_entry'].get()
        due_date = datetime.strptime(due_date_str, '%d/%m/%Y') if props['check_date'] and due_date_str else None

        if props['has_value'] and (doc_value is None or doc_value <= 0):
            messagebox.showwarning("Dati non validi", "Il Valore deve essere maggiore di zero.", parent=self)
            return
        if props['check_date'] and (not due_date or due_date.date() <= datetime.now().date()):
            messagebox.showwarning("Data non valida", "La Scadenza deve essere una data futura.", parent=self)
            return

        replaces_doc_id = None
        if self.doc_widgets['is_replacement_var'].get():
            doc_to_replace_title = self.doc_widgets['replaces_combo'].get()
            if not doc_to_replace_title:
                messagebox.showwarning("Dati Mancanti", "Selezionare un documento da sostituire.", parent=self)
                return
            rev_map = {title: doc_id for doc_id, title in self.active_docs_for_task.items()}
            replaces_doc_id = rev_map.get(doc_to_replace_title)

        try:
            self.npi_manager.add_npi_document(
                task_prodotto_id=self.current_task_id,
                doc_type_id=doc_type_id,
                title=title,
                body=self.selected_file_data,
                user=self.logged_in_user,
                note=self.doc_widgets['note_text'].get('1.0', tk.END).strip(),
                replaces_doc_id=replaces_doc_id,
                doc_value=doc_value,
                due_date=due_date,
                # --- CORREZIONE QUI ---
                # Il nome del parametro deve corrispondere a quello atteso dalla funzione del gestore,
                # che è molto probabilmente lo stesso della colonna nel DB.
                #IdFinalClient=self.final_clients_map.get(final_client_name)
                IDSite=self.final_clients_map.get(final_client_name)
            )
            messagebox.showinfo("Successo", "Documento salvato.", parent=self)
            self._on_task_select()  # Ricarica i dati del task
        except Exception as e:
            logger.error(f"Errore salvataggio documento: {e}", exc_info=True)
            messagebox.showerror("Errore Database", f"Impossibile salvare il documento:\n{e}", parent=self)

    def _launch_view_documents_window(self):
        if not self.current_task_id: return
        task = self._get_task_by_id(self.current_task_id)
        name = task.task_catalogo.NomeTask if task and task.task_catalogo else "Task"
        # Passa la mappa INVERSA alla finestra dei documenti
        TaskDocumentsWindow(
            self, self.npi_manager, self.lang, self.current_task_id,
            self.master_app, name, self.final_clients_map_rev
        )

    def _get_task_by_id(self, task_id):
        return next((t for t in self.progetto.waves[0].tasks if t.TaskProdottoID == task_id),
                    None) if self.progetto and self.progetto.waves else None

    def _launch_import_tasks_window(self):
        win = ImportTasksWindow(self, self.npi_manager, self.lang, self.project_id)
        self.wait_window(win)
        self._load_data_and_populate_ui()

    def _save_project_dates(self):
        try:
            start = datetime.strptime(self.project_start_date_entry.get(), '%d/%m/%Y')
            due = datetime.strptime(self.project_due_date_entry.get(), '%d/%m/%Y')
            updated, msg = self.npi_manager.update_project_dates(self.project_id, start, due, self.lang)
            messagebox.showinfo("Successo", "Date aggiornate.", parent=self)
            if msg: messagebox.showinfo('Informazione', msg, parent=self)
            self._load_data_and_populate_ui()
        except Exception as e:
            logger.error(f"Errore salvataggio date progetto: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile salvare le date:\n{e}", parent=self)

    def _save_task_details(self):
        """Salva i dettagli del task con validazione per milestone finale."""
        if not self.current_task_id:
            return

        # Recupera il nuovo stato
        nuovo_stato_display = self.fields['Stato'].get()
        nuovo_stato_db = self.status_map_db.get(nuovo_stato_display, 'Da Fare')

        # ===== VALIDAZIONE MILESTONE FINALE =====
        # Se il nuovo stato è 'Completato', verifica le dipendenze
        if nuovo_stato_db == 'Completato':
            is_valid, error_msg = self.npi_manager.validate_final_milestone_completion(
                self.current_task_id
            )

            if not is_valid:
                messagebox.showwarning(
                    self.lang.get('validation_error_title', 'Errore Validazione'),
                    error_msg,
                    parent=self
                )
                # Non procede con il salvataggio
                return

        # ===== SALVATAGGIO =====
        data = {
            'OwnerID': self.soggetti_map.get(self.fields['OwnerID'].get()),
            'Stato': nuovo_stato_db,
            'Note': self.fields['Note'].get('1.0', tk.END).strip(),
            'DataScadenza': self.fields['DataScadenza'].get(),
            'DataInizio': self.fields['DataInizio'].get(),
            'DataCompletamento': self.fields['DataCompletamento'].get(),
            'IsPostFinalMilestone': self.fields['IsPostFinalMilestone'].var.get()
        }

        try:
            task = self.npi_manager.update_task_prodotto(self.current_task_id, data)
            if messagebox.askyesno(
                    self.lang.get('notification_send_title', 'Conferma Notifiche'),
                    self.lang.get('notification_send_prompt', 'Inviare notifiche per questo task?'),
                    parent=self
            ):
                self.npi_manager.invia_notifiche_task(
                    task,
                    conferma_utente=False,
                    lang=self.lang
                )

            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('success_task_updated', 'Task aggiornato con successo.'),
                parent=self
            )

            # Ricarica la UI
            self._load_data_and_populate_ui()

        except Exception as e:
            logger.error(f"Errore salvataggio task: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                f"Impossibile aggiornare il task:\n{e}",
                parent=self
            )