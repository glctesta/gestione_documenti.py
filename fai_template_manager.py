# File: fai_template_manager.py
"""
Gestione Template FAI (First Article Inspection)
Form con 4 tab: Template, Steps, Step Details, Equipments
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import logging

logger = logging.getLogger(__name__)


class FaiTemplateManagerWindow(tk.Toplevel):
    """Finestra di gestione template FAI con 4 tab."""
    
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.current_template_id = None
        self.all_templates = []  # Cache per il filtro
        
        self.title(self.lang.get('gestione_template_fai', 'Gestione Template FAI'))
        self.geometry("1200x750")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_templates()
        
    def _create_widgets(self):
        """Crea la struttura con tab."""
        # Frame principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook (tab container)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Template
        self.template_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.template_frame, 
                         text=self.lang.get('tab_template', 'Template'))
        self._create_template_tab()
        
        # Tab 2: Steps
        self.steps_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.steps_frame, 
                         text=self.lang.get('tab_steps', 'Steps'))
        self._create_steps_tab()
        
        # Tab 3: Equipments
        self.equipments_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.equipments_frame, 
                         text=self.lang.get('tab_equipments', 'Equipments'))
        self._create_equipments_tab()
        
        # Tab 4: Step Details
        self.step_details_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.step_details_frame, 
                         text=self.lang.get('tab_step_details', 'Step Details'))
        self._create_step_details_tab()
        
        # Bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, 
                  text=self.lang.get('btn_close', 'Chiudi'),
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _create_template_tab(self):
        """Crea il tab Template con filtro e CRUD completo."""
        # Header con filtro
        header_frame = ttk.Frame(self.template_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, 
                 text=self.lang.get('template_list_title', 'Elenco Template'),
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        
        # Filtro template
        filter_frame = ttk.Frame(header_frame)
        filter_frame.pack(side=tk.RIGHT)
        
        ttk.Label(filter_frame, 
                 text=self.lang.get('filter_template', 'Filtra:')).pack(side=tk.LEFT, padx=(0, 5))
        
        self.template_filter_var = tk.StringVar()
        self.template_filter_combo = ttk.Combobox(filter_frame, 
                                                  textvariable=self.template_filter_var,
                                                  width=40,
                                                  state='readonly')
        self.template_filter_combo.pack(side=tk.LEFT, padx=5)
        self.template_filter_combo.bind('<<ComboboxSelected>>', self._on_filter_template)
        
        ttk.Button(filter_frame, 
                  text=self.lang.get('btn_clear_filter', 'Pulisci'),
                  command=self._clear_filter).pack(side=tk.LEFT, padx=5)
        
        # Treeview per lista template
        tree_frame = ttk.Frame(self.template_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'nr_document', 'revision', 'title', 'revision_date')
        self.template_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.template_tree.heading('id', text='ID')
        self.template_tree.heading('nr_document', text=self.lang.get('col_nr_document', 'Nr. Documento'))
        self.template_tree.heading('revision', text=self.lang.get('col_revision', 'Revisione'))
        self.template_tree.heading('title', text=self.lang.get('col_title', 'Titolo'))
        self.template_tree.heading('revision_date', text=self.lang.get('col_revision_date', 'Data Revisione'))
        
        self.template_tree.column('id', width=60)
        self.template_tree.column('nr_document', width=150)
        self.template_tree.column('revision', width=100)
        self.template_tree.column('title', width=350)
        self.template_tree.column('revision_date', width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.template_tree.yview)
        self.template_tree.configure(yscroll=scrollbar.set)
        
        self.template_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind doppio click e selezione
        self.template_tree.bind('<<TreeviewSelect>>', self._on_template_select)
        self.template_tree.bind('<Double-1>', lambda e: self._edit_template())
        
        # Bottoni azioni
        btn_frame = ttk.Frame(self.template_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._new_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_edit', 'Modifica'),
                  command=self._edit_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._delete_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_refresh', 'Aggiorna'),
                  command=self._load_templates).pack(side=tk.LEFT, padx=5)
    
    def _load_templates(self):
        """Carica i template dalla tabella FaiTemplates."""
        try:
            # 💾 Salva il filtro corrente prima di ricaricare
            current_filter = self.template_filter_var.get() if hasattr(self, 'template_filter_var') else None
            
            # Pulisci treeview
            for item in self.template_tree.get_children():
                self.template_tree.delete(item)
            
            # Query al database
            query = """
            SELECT 
                FaiTemplateId,
                NrDocument,
                Revision,
                FaiTitle,
                RevisionDate
            FROM [Traceability_RS].[fai].[FaiTemplates]
            ORDER BY FaiTemplateId DESC
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.all_templates = []
            filter_values = [self.lang.get('all_templates', 'Tutti i template')]
            
            for row in rows:
                template_id = row.FaiTemplateId
                nr_document = row.NrDocument or ''
                revision = row.Revision or ''
                title = row.FaiTitle or ''
                revision_date = row.RevisionDate.strftime('%d/%m/%Y') if row.RevisionDate else ''
                
                # Aggiungi alla treeview
                self.template_tree.insert('', tk.END, iid=str(template_id),
                                         values=(template_id, nr_document, revision, title, revision_date))
                
                # Salva per filtro
                template_data = {
                    'id': template_id,
                    'nr_document': nr_document,
                    'revision': revision,
                    'title': title,
                    'revision_date': revision_date
                }
                self.all_templates.append(template_data)
                
                # Aggiungi al filtro
                filter_label = f"{template_id} - {title}" if title else f"{template_id} - {nr_document}"
                filter_values.append(filter_label)
            
            # Aggiorna combo del filtro
            self.template_filter_combo['values'] = filter_values
            
            # 🔄 Ripristina il filtro precedente se esiste, altrimenti usa default
            if current_filter and current_filter in filter_values:
                self.template_filter_var.set(current_filter)
                # Riapplica il filtro
                self._on_filter_template()
            else:
                self.template_filter_var.set(filter_values[0])
            
            logger.info(f"Caricati {len(rows)} template FAI")
            
        except Exception as e:
            logger.error(f"Errore caricamento template FAI: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i template:\n{e}",
                parent=self
            )
    
    def _on_filter_template(self, event=None):
        """Filtra i template nel treeview."""
        selected = self.template_filter_var.get()
        all_label = self.lang.get('all_templates', 'Tutti i template')
        
        # Pulisci treeview
        for item in self.template_tree.get_children():
            self.template_tree.delete(item)
        
        if selected == all_label:
            # Mostra tutti
            for template in self.all_templates:
                self.template_tree.insert('', tk.END, iid=str(template['id']),
                                         values=(template['id'], template['nr_document'], 
                                               template['revision'], template['title'], 
                                               template['revision_date']))
        else:
            # Mostra solo quello selezionato
            template_id = int(selected.split(' - ')[0])
            template = next((t for t in self.all_templates if t['id'] == template_id), None)
            if template:
                self.template_tree.insert('', tk.END, iid=str(template['id']),
                                         values=(template['id'], template['nr_document'], 
                                               template['revision'], template['title'], 
                                               template['revision_date']))
    
    def _clear_filter(self):
        """Pulisce il filtro e mostra tutti i template."""
        all_label = self.lang.get('all_templates', 'Tutti i template')
        self.template_filter_var.set(all_label)
        self._on_filter_template()
    
    def _on_template_select(self, event=None):
        """Gestisce la selezione di un template."""
        selection = self.template_tree.selection()
        if selection:
            self.current_template_id = int(selection[0])
        else:
            self.current_template_id = None
    
    def _new_template(self):
        """Apre dialog per nuovo template."""
        TemplateEditorDialog(self, self.db, self.lang, None, self._load_templates)
    
    def _edit_template(self):
        """Apre dialog per modifica template."""
        if not self.current_template_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_template_first', 'Seleziona un template da modificare.'),
                parent=self
            )
            return
        
        TemplateEditorDialog(self, self.db, self.lang, self.current_template_id, self._load_templates)
    
    def _delete_template(self):
        """Elimina il template selezionato."""
        if not self.current_template_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_template_first', 'Seleziona un template da eliminare.'),
                parent=self
            )
            return
        
        # Conferma eliminazione
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_template', 'Sei sicuro di voler eliminare questo template?'),
            parent=self
        ):
            return
        
        try:
            query = "DELETE FROM [Traceability_RS].[fai].[FaiTemplates] WHERE FaiTemplateId = ?"
            cursor = self.db.cursor
            cursor.execute(query, (self.current_template_id,))
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('template_deleted', 'Template eliminato con successo.'),
                parent=self
            )
            
            self.current_template_id = None
            self._load_templates()
            
        except Exception as e:
            logger.error(f"Errore eliminazione template: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile eliminare il template:\n{e}",
                parent=self
            )
    
    def _create_steps_tab(self):
        """Crea il tab Steps con filtri e CRUD completo."""
        # Header con filtri
        header_frame = ttk.Frame(self.steps_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, 
                 text=self.lang.get('steps_list_title', 'Gestione Steps'),
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        
        # Frame filtri
        filter_frame = ttk.Frame(self.steps_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primo combo: Template
        ttk.Label(filter_frame, 
                 text=self.lang.get('select_template', 'Seleziona Template:')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.steps_template_var = tk.StringVar()
        self.steps_template_combo = ttk.Combobox(filter_frame, 
                                                 textvariable=self.steps_template_var,
                                                 width=60,
                                                 state='readonly')
        self.steps_template_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.steps_template_combo.bind('<<ComboboxSelected>>', self._on_steps_template_select)
        
        # Secondo combo: Steps filtrati
        ttk.Label(filter_frame, 
                 text=self.lang.get('filter_step', 'Filtra Step:')).grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.steps_filter_var = tk.StringVar()
        self.steps_filter_combo = ttk.Combobox(filter_frame, 
                                               textvariable=self.steps_filter_var,
                                               width=60,
                                               state='readonly')
        self.steps_filter_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.steps_filter_combo.bind('<<ComboboxSelected>>', self._on_steps_filter_select)
        
        ttk.Button(filter_frame, 
                  text=self.lang.get('btn_clear_filter', 'Pulisci'),
                  command=self._clear_steps_filter).grid(row=1, column=2, padx=5, pady=5)
        
        # Treeview per lista steps
        tree_frame = ttk.Frame(self.steps_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('step_id', 'step_name', 'order', 'template_id', 'template_title')
        self.steps_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.steps_tree.heading('step_id', text='Step ID')
        self.steps_tree.heading('step_name', text=self.lang.get('col_step_name', 'Nome Step'))
        self.steps_tree.heading('order', text=self.lang.get('col_order', 'Ordine'))
        self.steps_tree.heading('template_id', text='Template ID')
        self.steps_tree.heading('template_title', text=self.lang.get('col_template_title', 'Titolo Template'))
        
        self.steps_tree.column('step_id', width=80)
        self.steps_tree.column('step_name', width=250)
        self.steps_tree.column('order', width=80)
        self.steps_tree.column('template_id', width=100)
        self.steps_tree.column('template_title', width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.steps_tree.yview)
        self.steps_tree.configure(yscroll=scrollbar.set)
        
        self.steps_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.steps_tree.bind('<<TreeviewSelect>>', self._on_step_select)
        self.steps_tree.bind('<Double-1>', lambda e: self._edit_step())
        
        # Bottoni azioni
        btn_frame = ttk.Frame(self.steps_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._new_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_edit', 'Modifica'),
                  command=self._edit_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._delete_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_refresh', 'Aggiorna'),
                  command=self._load_steps).pack(side=tk.LEFT, padx=5)
        
        # Inizializza variabili
        self.current_step_id = None
        self.selected_template_id_for_steps = None
        self.all_steps = []
        
        # Carica dati iniziali
        self._load_steps_templates()
        self._load_steps()
    
    def _load_steps_templates(self):
        """Carica i template per il combo del tab Steps."""
        try:
            query = """
            SELECT 
                FaiTemplateId,
                NrDocument,
                Revision,
                FaiTitle,
                RevisionDate
            FROM [Traceability_RS].[fai].[FaiTemplates]
            ORDER BY FaiTemplateId DESC
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            template_values = [self.lang.get('all_templates', 'Tutti i template')]
            self.steps_templates_data = {}
            
            for row in rows:
                template_id = row.FaiTemplateId
                title = row.FaiTitle or row.NrDocument or f"Template {template_id}"
                label = f"{template_id} - {title}"
                template_values.append(label)
                self.steps_templates_data[label] = template_id
            
            self.steps_template_combo['values'] = template_values
            if template_values:
                self.steps_template_var.set(template_values[0])
            
            # Aggiorna il combo filtro steps dopo aver caricato i template
            self._update_steps_filter_combo()
            
        except Exception as e:
            logger.error(f"Errore caricamento template per steps: {e}", exc_info=True)
    
    def _load_steps(self):
        """Carica gli step dalla tabella FaiSteps."""
        try:
            # 💾 Salva i filtri correnti prima di ricaricare
            current_template_filter = self.steps_template_var.get() if hasattr(self, 'steps_template_var') else None
            current_step_filter = self.steps_filter_var.get() if hasattr(self, 'steps_filter_var') else None
            
            # Pulisci treeview
            for item in self.steps_tree.get_children():
                self.steps_tree.delete(item)
            
            # Query per caricare tutti gli step attivi con info template
            query = """
            SELECT 
                s.FatStepId,
                s.StepName,
                s.OrderInList,
                s.FaiTemplateId,
                t.FaiTitle
            FROM [Traceability_RS].[fai].[FaiSteps] s
            LEFT JOIN [Traceability_RS].[fai].[FaiTemplates] t ON s.FaiTemplateId = t.FaiTemplateId
            WHERE s.DateOut IS NULL
            ORDER BY s.FaiTemplateId DESC, s.OrderInList, s.StepName
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.all_steps = []
            
            for row in rows:
                step_id = row.FatStepId
                step_name = row.StepName or ''
                order_in_list = row.OrderInList if row.OrderInList is not None else 0
                template_id = row.FaiTemplateId or ''
                template_title = row.FaiTitle or ''
                
                # Aggiungi alla treeview
                self.steps_tree.insert('', tk.END, iid=str(step_id),
                                      values=(step_id, step_name, order_in_list, template_id, template_title))
                
                # Salva per filtro
                step_data = {
                    'step_id': step_id,
                    'step_name': step_name,
                    'order_in_list': order_in_list,
                    'template_id': template_id,
                    'template_title': template_title
                }
                self.all_steps.append(step_data)
            
            # Aggiorna combo filtro steps
            self._update_steps_filter_combo()
            
            # 🔄 Ripristina i filtri precedenti se esistono
            if current_template_filter:
                self.steps_template_var.set(current_template_filter)
                self._on_steps_template_select()
                
                if current_step_filter:
                    # Ripristina anche il filtro step se esiste
                    step_filter_values = self.steps_filter_combo['values']
                    if current_step_filter in step_filter_values:
                        self.steps_filter_var.set(current_step_filter)
                        self._on_steps_filter_select()
            
            logger.info(f"Caricati {len(rows)} steps FAI")
            
        except Exception as e:
            logger.error(f"Errore caricamento steps: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare gli steps:\n{e}",
                parent=self
            )
    
    def _update_steps_filter_combo(self):
        """Aggiorna il combo filtro steps in base al template selezionato."""
        try:
            selected_template = self.steps_template_var.get()
            all_label = self.lang.get('all_templates', 'Tutti i template')
            all_steps_label = self.lang.get('all_steps', 'Tutti gli steps')
            
            filter_values = [all_steps_label]
            
            if selected_template != all_label and selected_template in self.steps_templates_data:
                # Filtra per template selezionato e DateOut is null
                template_id = self.steps_templates_data[selected_template]
                
                query = """
                SELECT FatStepId, StepName, OrderInList
                FROM [Traceability_RS].[fai].[FaiSteps]
                WHERE FaiTemplateId = ? AND DateOut IS NULL
                ORDER BY OrderInList, StepName
                """
                
                cursor = self.db.cursor
                cursor.execute(query, (template_id,))
                rows = cursor.fetchall()
                
                for row in rows:
                    step_id = row.FatStepId
                    step_name = row.StepName or f"Step {step_id}"
                    label = f"{step_id} - {step_name}"
                    filter_values.append(label)
            
            self.steps_filter_combo['values'] = filter_values
            if filter_values:
                self.steps_filter_var.set(filter_values[0])
                
        except Exception as e:
            logger.error(f"Errore aggiornamento filtro steps: {e}", exc_info=True)
    
    def _on_steps_template_select(self, event=None):
        """Gestisce la selezione del template nel tab Steps."""
        selected = self.steps_template_var.get()
        all_label = self.lang.get('all_templates', 'Tutti i template')
        
        # Pulisci treeview
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
        
        if selected == all_label:
            # Mostra tutti gli steps
            self.selected_template_id_for_steps = None
            for step in self.all_steps:
                self.steps_tree.insert('', tk.END, iid=str(step['step_id']),
                                      values=(step['step_id'], step['step_name'], 
                                            step['order_in_list'], step['template_id'], 
                                            step['template_title']))
        else:
            # Mostra solo steps del template selezionato
            template_id = self.steps_templates_data.get(selected)
            self.selected_template_id_for_steps = template_id
            
            for step in self.all_steps:
                if step['template_id'] == template_id:
                    self.steps_tree.insert('', tk.END, iid=str(step['step_id']),
                                          values=(step['step_id'], step['step_name'], 
                                                step['order_in_list'], step['template_id'], 
                                                step['template_title']))
        
        # Aggiorna combo filtro steps
        self._update_steps_filter_combo()
    
    def _on_steps_filter_select(self, event=None):
        """Gestisce la selezione del filtro steps."""
        selected = self.steps_filter_var.get()
        all_steps_label = self.lang.get('all_steps', 'Tutti gli steps')
        
        if selected == all_steps_label:
            # Risincronizza con il filtro template
            self._on_steps_template_select()
            return
        
        # Estrai step_id dal label
        try:
            step_id = int(selected.split(' - ')[0])
            
            # Pulisci treeview
            for item in self.steps_tree.get_children():
                self.steps_tree.delete(item)
            
            # Mostra solo lo step selezionato
            step = next((s for s in self.all_steps if s['step_id'] == step_id), None)
            if step:
                self.steps_tree.insert('', tk.END, iid=str(step['step_id']),
                                      values=(step['step_id'], step['step_name'], 
                                            step['order_in_list'], step['template_id'], 
                                            step['template_title']))
        except (ValueError, IndexError):
            pass
    
    def _clear_steps_filter(self):
        """Pulisce i filtri del tab Steps."""
        all_label = self.lang.get('all_templates', 'Tutti i template')
        self.steps_template_var.set(all_label)
        self._on_steps_template_select()
    
    def _on_step_select(self, event=None):
        """Gestisce la selezione di uno step."""
        selection = self.steps_tree.selection()
        if selection:
            self.current_step_id = int(selection[0])
        else:
            self.current_step_id = None
    
    def _new_step(self):
        """Apre dialog per nuovo step."""
        StepEditorDialog(self, self.db, self.lang, None, self._load_steps, 
                        self.selected_template_id_for_steps)
    
    def _edit_step(self):
        """Apre dialog per modifica step."""
        if not self.current_step_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_step_first', 'Seleziona uno step da modificare.'),
                parent=self
            )
            return
        
        StepEditorDialog(self, self.db, self.lang, self.current_step_id, self._load_steps, None)
    
    def _delete_step(self):
        """Elimina logicamente lo step (imposta DateOut)."""
        if not self.current_step_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_step_first', 'Seleziona uno step da eliminare.'),
                parent=self
            )
            return
        
        # Conferma eliminazione
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_step', 'Sei sicuro di voler eliminare questo step?'),
            parent=self
        ):
            return
        
        try:
            # Cancellazione logica: imposta DateOut invece di DELETE fisico
            query = "UPDATE [Traceability_RS].[fai].[FaiSteps] SET DateOut = GETDATE() WHERE FatStepId = ?"
            cursor = self.db.cursor
            cursor.execute(query, (self.current_step_id,))
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('step_deleted', 'Step eliminato con successo.'),
                parent=self
            )
            
            self.current_step_id = None
            self._load_steps()
            
        except Exception as e:
            logger.error(f"Errore eliminazione step: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile eliminare lo step:\n{e}",
                parent=self
            )
    
    def _create_step_details_tab(self):
        """Crea il tab Step Details con tre filtri a cascata e CRUD completo."""
        # Header
        header_frame = ttk.Frame(self.step_details_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, 
                 text=self.lang.get('step_details_list_title', 'Gestione Step Details'),
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        
        # Filtri a cascata
        filter_frame = ttk.Frame(self.step_details_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro 1: Template
        ttk.Label(filter_frame, 
                 text=self.lang.get('select_template', 'Seleziona Template:')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.sd_template_var = tk.StringVar()
        self.sd_template_combo = ttk.Combobox(filter_frame, 
                                              textvariable=self.sd_template_var,
                                              width=40,
                                              state='readonly')
        self.sd_template_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.sd_template_combo.bind('<<ComboboxSelected>>', self._on_sd_template_select)
        
        # Filtro 2: Step
        ttk.Label(filter_frame, 
                 text=self.lang.get('select_step', 'Seleziona Step:')).grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.sd_step_var = tk.StringVar()
        self.sd_step_combo = ttk.Combobox(filter_frame, 
                                         textvariable=self.sd_step_var,
                                         width=40,
                                         state='readonly')
        self.sd_step_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.sd_step_combo.bind('<<ComboboxSelected>>', self._on_sd_step_select)
        
        # Filtro 3: Step Detail
        ttk.Label(filter_frame, 
                 text=self.lang.get('filter_step_detail', 'Filtra Step Detail:')).grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.sd_detail_filter_var = tk.StringVar()
        self.sd_detail_filter_combo = ttk.Combobox(filter_frame, 
                                                   textvariable=self.sd_detail_filter_var,
                                                   width=60,
                                                   state='readonly')
        self.sd_detail_filter_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.sd_detail_filter_combo.bind('<<ComboboxSelected>>', self._on_sd_detail_filter_select)
        
        ttk.Button(filter_frame, 
                  text=self.lang.get('btn_clear_filter', 'Pulisci'),
                  command=self._clear_step_details_filter).grid(row=2, column=2, padx=5, pady=5)
        
        # Treeview per lista step details
        tree_frame = ttk.Frame(self.step_details_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('detail_id', 'ordine', 'step', 'step_detail', 'equipment')
        self.step_details_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configura stile per righe più alte (permette testo su più righe)
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # Altezza riga aumentata a 40px
        
        self.step_details_tree.heading('detail_id', text='Detail ID')
        self.step_details_tree.heading('ordine', text=self.lang.get('col_ordine', 'Ordine'))
        self.step_details_tree.heading('step', text=self.lang.get('col_step', 'Step'))
        self.step_details_tree.heading('step_detail', text=self.lang.get('col_step_detail', 'Dettaglio'))
        self.step_details_tree.heading('equipment', text=self.lang.get('col_equipment', 'Equipment'))
        
        self.step_details_tree.column('detail_id', width=80)
        self.step_details_tree.column('ordine', width=70)
        self.step_details_tree.column('step', width=280)
        self.step_details_tree.column('step_detail', width=380)
        self.step_details_tree.column('equipment', width=230)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.step_details_tree.yview)
        self.step_details_tree.configure(yscroll=scrollbar.set)
        
        self.step_details_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.step_details_tree.bind('<<TreeviewSelect>>', self._on_step_detail_select)
        self.step_details_tree.bind('<Double-1>', lambda e: self._edit_step_detail())
        
        # Tooltip per mostrare testo completo su hover
        self._create_step_detail_tooltip()
        
        # Bottoni azioni
        btn_frame = ttk.Frame(self.step_details_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._new_step_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_edit', 'Modifica'),
                  command=self._edit_step_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._delete_step_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_refresh', 'Aggiorna'),
                  command=self._load_step_details).pack(side=tk.LEFT, padx=5)
        
        # Inizializza variabili
        self.current_step_detail_id = None
        self.all_step_details = []
        self.sd_templates_data = {}
        self.sd_steps_data = {}
        
        # Carica dati iniziali
        self._load_sd_templates()
        self._load_step_details()
    
    def _create_equipments_tab(self):
        """Crea il tab Equipments con filtro e CRUD completo."""
        # Header
        header_frame = ttk.Frame(self.equipments_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, 
                 text=self.lang.get('equipments_list_title', 'Gestione Equipments'),
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        
        # Filtro equipment
        filter_frame = ttk.Frame(self.equipments_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, 
                 text=self.lang.get('filter_equipment', 'Filtra Equipment:')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        
        self.equipment_filter_var = tk.StringVar()
        self.equipment_filter_combo = ttk.Combobox(filter_frame, 
                                                   textvariable=self.equipment_filter_var,
                                                   width=60,
                                                   state='readonly')
        self.equipment_filter_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.equipment_filter_combo.bind('<<ComboboxSelected>>', self._on_equipment_filter_select)
        
        ttk.Button(filter_frame, 
                  text=self.lang.get('btn_clear_filter', 'Pulisci'),
                  command=self._clear_equipment_filter).grid(row=0, column=2, padx=5, pady=5)
        
        # Treeview per lista equipments
        tree_frame = ttk.Frame(self.equipments_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('equipment_id', 'description', 'serial_number')
        self.equipments_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.equipments_tree.heading('equipment_id', text='Equipment ID')
        self.equipments_tree.heading('description', text=self.lang.get('col_description', 'Descrizione'))
        self.equipments_tree.heading('serial_number', text=self.lang.get('col_serial_number', 'Numero Seriale'))
        
        self.equipments_tree.column('equipment_id', width=120)
        self.equipments_tree.column('description', width=400)
        self.equipments_tree.column('serial_number', width=250)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.equipments_tree.yview)
        self.equipments_tree.configure(yscroll=scrollbar.set)
        
        self.equipments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.equipments_tree.bind('<<TreeviewSelect>>', self._on_equipment_select)
        self.equipments_tree.bind('<Double-1>', lambda e: self._edit_equipment())
        
        # Bottoni azioni
        btn_frame = ttk.Frame(self.equipments_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._new_equipment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_edit', 'Modifica'),
                  command=self._edit_equipment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._delete_equipment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_refresh', 'Aggiorna'),
                  command=self._load_equipments).pack(side=tk.LEFT, padx=5)
        
        # Inizializza variabili
        self.current_equipment_id = None
        self.all_equipments = []
        
        # Carica dati iniziali
        self._load_equipments()
    
    # ========== STEP DETAILS METHODS ==========
    
    def _load_sd_templates(self):
        """Carica i template per il filtro Step Details."""
        try:
            query = """
            SELECT FaiTemplateId, FaiTitle, NrDocument
            FROM [Traceability_RS].[fai].[FaiTemplates]
            ORDER BY FaiTemplateId DESC
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            template_values = [self.lang.get('all_templates', 'Tutti i template')]
            self.sd_templates_data = {}
            
            for row in rows:
                template_id = row.FaiTemplateId
                title = row.FaiTitle or row.NrDocument or f"Template {template_id}"
                label = f"{template_id} - {title}"
                template_values.append(label)
                self.sd_templates_data[label] = template_id
            
            self.sd_template_combo['values'] = template_values
            if template_values:
                self.sd_template_var.set(template_values[0])
            
        except Exception as e:
            logger.error(f"Errore caricamento template per step details: {e}", exc_info=True)
    
    def _load_step_details(self):
        """Carica i step details con join dalla query fornita."""
        try:
            # Pulisci treeview
            for item in self.step_details_tree.get_children():
                self.step_details_tree.delete(item)
            
            # Query con JOIN includendo OrdineList e KeepOnsameLine
            query = """
            SELECT [FaiStepDetailId]
                  ,D.[OrdineList]
                  ,s.StepName + ' -> ' + t.NrDocument as Step
                  ,[StepDetail]
                  ,ISNULL(e.[Description] + ' ' + e.SerialNumber, '') as Equipment
                  ,D.FatStepId
                  ,D.FaiEquipmentid
                  ,D.[KeepOnsameLine]
            FROM [Traceability_RS].[fai].[FaiStepDetails] D
            INNER JOIN [Traceability_RS].[fai].FaiSteps S on D.FatStepId=S.FatStepId and S.DateOut is null
            LEFT JOIN [Traceability_RS].[fai].FaiEquipments E on d.FaiEquipmentId = e.FaiEquipmentid
            INNER JOIN [Traceability_RS].[fai].FaiTemplates T on t.FaiTemplateId=s.FaiTemplateId
            WHERE D.DateOut is null
            ORDER BY s.OrderInList, D.OrdineList
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.all_step_details = []
            
            for row in rows:
                detail_id = row.FaiStepDetailId
                ordine_list = row.OrdineList or 0
                step = row.Step or ''
                step_detail = row.StepDetail or ''
                equipment = row.Equipment or ''
                fat_step_id = row.FatStepId
                equipment_id = row.FaiEquipmentid
                keep_on_same_line = row.KeepOnsameLine or False
                
                # Aggiungi alla treeview
                self.step_details_tree.insert('', tk.END, iid=str(detail_id),
                                             values=(detail_id, ordine_list, step, step_detail, equipment))
                
                # Salva per filtro
                detail_data = {
                    'detail_id': detail_id,
                    'ordine_list': ordine_list,
                    'step': step,
                    'step_detail': step_detail,
                    'equipment': equipment,
                    'fat_step_id': fat_step_id,
                    'equipment_id': equipment_id,
                    'keep_on_same_line': keep_on_same_line
                }
                self.all_step_details.append(detail_data)
            
            # Aggiorna combo filtro details
            self._update_sd_detail_filter_combo()
            
            logger.info(f"Caricati {len(rows)} step details FAI")
            
        except Exception as e:
            logger.error(f"Errore caricamento step details: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare gli step details:\n{e}",
                parent=self
            )
    
    def _on_sd_template_select(self, event=None):
        """Gestisce la selezione del template e carica gli steps."""
        selected = self.sd_template_var.get()
        all_label = self.lang.get('all_templates', 'Tutti i template')
        
        # Reset step combo
        self.sd_step_combo['values'] = []
        self.sd_step_var.set('')
        
        if selected != all_label and selected in self.sd_templates_data:
            template_id = self.sd_templates_data[selected]
            
            # Carica steps per questo template
            try:
                query = """
                SELECT FatStepId, StepName
                FROM [Traceability_RS].[fai].[FaiSteps]
                WHERE FaiTemplateId = ? AND DateOut IS NULL
                ORDER BY OrderInList, StepName
                """
                
                cursor = self.db.cursor
                cursor.execute(query, (template_id,))
                rows = cursor.fetchall()
                
                step_values = [self.lang.get('all_steps', 'Tutti gli step')]
                self.sd_steps_data = {}
                
                for row in rows:
                    step_id = row.FatStepId
                    step_name = row.StepName or f"Step {step_id}"
                    label = f"{step_id} - {step_name}"
                    step_values.append(label)
                    self.sd_steps_data[label] = step_id
                
                self.sd_step_combo['values'] = step_values
                if step_values:
                    self.sd_step_var.set(step_values[0])
                
            except Exception as e:
                logger.error(f"Errore caricamento steps per template: {e}", exc_info=True)
        
        # Filtra treeview
        self._filter_step_details_tree()
    
    def _on_sd_step_select(self, event=None):
        """Gestis ce la selezione dello step e filtra i details."""
        self._filter_step_details_tree()
    
    def _filter_step_details_tree(self):
        """Filtra il treeview in base a template e step selezionati."""
        # Pulisci treeview
        for item in self.step_details_tree.get_children():
            self.step_details_tree.delete(item)
        
        template_selected = self.sd_template_var.get()
        step_selected = self.sd_step_var.get()
        
        all_templates = self.lang.get('all_templates', 'Tutti i template')
        all_steps = self.lang.get('all_steps', 'Tutti gli steps')
        
        for detail in self.all_step_details:
            # Controlli filtri
            if template_selected != all_templates:
                if template_selected not in self.sd_templates_data:
                    continue
                template_id = self.sd_templates_data[template_selected]
                # Verifica se il detail appartiene a uno step di questo template
                # (già filtrato dalla query principale per ora mostriamo tutti)
            
            if step_selected and step_selected != all_steps:
                if step_selected in self.sd_steps_data:
                    step_id = self.sd_steps_data[step_selected]
                    if detail['fat_step_id'] != step_id:
                        continue
            
            self.step_details_tree.insert('', tk.END, iid=str(detail['detail_id']),
                                         values=(detail['detail_id'], detail['ordine_list'], detail['step'], 
                                               detail['step_detail'], detail['equipment']))
        
        # Aggiorna combo filtro details
        self._update_sd_detail_filter_combo()
    
    def _update_sd_detail_filter_combo(self):
        """Aggiorna il combo filtro step details."""
        try:
            filter_values = [self.lang.get('all_details', 'Tutti i dettagli')]
            
            # Prendi solo i detail visibili nel treeview
            for item_id in self.step_details_tree.get_children():
                values = self.step_details_tree.item(item_id, 'values')
                if values:
                    detail_id = values[0]
                    step_detail = values[2]
                    label = f"{detail_id} - {step_detail[:50]}" if len(step_detail) > 50 else f"{detail_id} - {step_detail}"
                    filter_values.append(label)
            
            self.sd_detail_filter_combo['values'] = filter_values
            self.sd_detail_filter_var.set(filter_values[0])
            
        except Exception as e:
            logger.error(f"Errore aggiornamento filtro detail: {e}", exc_info=True)
    
    def _on_sd_detail_filter_select(self, event=None):
        """Filtra mostrando solo il detail selezionato."""
        selected = self.sd_detail_filter_var.get()
        all_label = self.lang.get('all_details', 'Tutti i dettagli')
        
        if selected == all_label:
            self._filter_step_details_tree()
        else:
            # Mostra solo il detail selezionato
            try:
                detail_id = int(selected.split(' - ')[0])
                
                # Pulisci treeview
                for item in self.step_details_tree.get_children():
                    self.step_details_tree.delete(item)
                
                # Mostra solo quello selezionato
                detail = next((d for d in self.all_step_details if d['detail_id'] == detail_id), None)
                if detail:
                    self.step_details_tree.insert('', tk.END, iid=str(detail['detail_id']),
                                                 values=(detail['detail_id'], detail['ordine_list'], detail['step'],
                                                       detail['step_detail'], detail['equipment']))
            except (ValueError, IndexError):
                pass
    
    def _clear_step_details_filter(self):
        """Pulisce tutti i filtri e ricarica."""
        all_templates = self.lang.get('all_templates', 'Tutti i template')
        self.sd_template_var.set(all_templates)
        self.sd_step_var.set('')
        self.sd_detail_filter_var.set('')
        self.sd_step_combo['values'] = []
        self._load_step_details()
    
    def _on_step_detail_select(self, event=None):
        """Gestisce la selezione di un step detail."""
        selection = self.step_details_tree.selection()
        if selection:
            self.current_step_detail_id = int(selection[0])
        else:
            self.current_step_detail_id = None
    
    def _new_step_detail(self):
        """Apre dialog per nuovo step detail."""
        # Se c'è uno step filtrato, passalo come default
        default_step_id = None
        step_selected = self.sd_step_var.get()
        all_steps = self.lang.get('all_steps', 'Tutti gli steps')
        
        if step_selected and step_selected != all_steps and step_selected in self.sd_steps_data:
            default_step_id = self.sd_steps_data[step_selected]
        
        StepDetailEditorDialog(self, self.db, self.lang, None, self._load_step_details, default_step_id)
    
    def _edit_step_detail(self):
        """Apre dialog per modifica step detail."""
        if not self.current_step_detail_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_step_detail_first', 'Seleziona uno step detail da modificare.'),
                parent=self
            )
            return
        
        StepDetailEditorDialog(self, self.db, self.lang, self.current_step_detail_id, self._load_step_details, None)
    
    def _delete_step_detail(self):
        """Elimina logicamente lo step detail (imposta DateOut)."""
        if not self.current_step_detail_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_step_detail_first', 'Seleziona uno step detail da eliminare.'),
                parent=self
            )
            return
        
        # Conferma eliminazione
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_step_detail', 'Sei sicuro di voler eliminare questo step detail?'),
            parent=self
        ):
            return
        
        try:
            # Cancellazione logica: imposta DateOut
            query = "UPDATE [Traceability_RS].[fai].[FaiStepDetails] SET DateOut = GETDATE() WHERE FaiStepDetailId = ?"
            cursor = self.db.cursor
            cursor.execute(query, (self.current_step_detail_id,))
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('step_detail_deleted', 'Step Detail eliminato con successo.'),
                parent=self
            )
            
            self.current_step_detail_id = None
            self._load_step_details()
            
        except Exception as e:
            logger.error(f"Errore eliminazione step detail: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile eliminare lo step detail:\n{e}",
                parent=self
            )
    
    def _create_step_detail_tooltip(self):
        """Crea tooltip che mostra il testo completo quando passi sopra una riga."""
        # Widget tooltip
        self.step_detail_tooltip = None
        
        def show_tooltip(event):
            """Mostra il tooltip con il testo completo."""
            # Identifica la riga sotto il mouse
            item = self.step_details_tree.identify('item', event.x, event.y)
            if not item:
                hide_tooltip()
                return
            
            # Ottieni i valori della riga
            values = self.step_details_tree.item(item, 'values')
            if not values or len(values) < 4:
                hide_tooltip()
                return
            
            # Crea il testo del tooltip con tutte le info
            detail_id, ordine, step, step_detail, equipment = values[:5] if len(values) >= 5 else (*values, '')
            
            tooltip_text = f"ID: {detail_id} | Ordine: {ordine}\n"
            tooltip_text += f"Step: {step}\n"
            tooltip_text += f"Dettaglio: {step_detail}\n"
            if equipment:
                tooltip_text += f"Equipment: {equipment}"
            
            # Crea o aggiorna il tooltip
            if self.step_detail_tooltip:
                self.step_detail_tooltip.destroy()
            
            self.step_detail_tooltip = tk.Toplevel(self)
            self.step_detail_tooltip.wm_overrideredirect(True)
            self.step_detail_tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            
            label = tk.Label(
                self.step_detail_tooltip,
                text=tooltip_text,
                justify=tk.LEFT,
                background="#ffffe0",
                relief=tk.SOLID,
                borderwidth=1,
                font=("TkDefaultFont", 9),
                wraplength=400  # Word wrap a 400px
            )
            label.pack()
        
        def hide_tooltip(event=None):
            """Nascondi il tooltip."""
            if self.step_detail_tooltip:
                self.step_detail_tooltip.destroy()
                self.step_detail_tooltip = None
        
        # Bind eventi mouse
        self.step_details_tree.bind('<Motion>', show_tooltip)
        self.step_details_tree.bind('<Leave>', hide_tooltip)
    
    # ========== EQUIPMENTS METHODS ==========
    
    def _load_equipments(self):
        """Carica gli equipments dalla tabella FaiEquipments."""
        try:
            # Pulisci treeview
            for item in self.equipments_tree.get_children():
                self.equipments_tree.delete(item)
            
            # Query al database
            query = """
            SELECT 
                FaiEquipmentid,
                Description,
                SerialNumber
            FROM [Traceability_RS].[fai].[FaiEquipments]
            ORDER BY Description, SerialNumber
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.all_equipments = []
            filter_values = [self.lang.get('all_equipments', 'Tutti gli equipments')]
            
            for row in rows:
                equipment_id = row.FaiEquipmentid
                description = row.Description or ''
                serial_number = row.SerialNumber or ''
                
                # Aggiungi alla treeview
                self.equipments_tree.insert('', tk.END, iid=str(equipment_id),
                                           values=(equipment_id, description, serial_number))
                
                # Salva per filtro
                equipment_data = {
                    'equipment_id': equipment_id,
                    'description': description,
                    'serial_number': serial_number
                }
                self.all_equipments.append(equipment_data)
                
                # Aggiungi al filtro
                filter_label = f"{equipment_id} - {description}" if description else f"{equipment_id} - {serial_number}"
                filter_values.append(filter_label)
            
            # Aggiorna combo del filtro
            self.equipment_filter_combo['values'] = filter_values
            self.equipment_filter_var.set(filter_values[0])
            
            logger.info(f"Caricati {len(rows)} equipments FAI")
            
        except Exception as e:
            logger.error(f"Errore caricamento equipments: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare gli equipments:\n{e}",
                parent=self
            )
    
    def _on_equipment_filter_select(self, event=None):
        """Filtra gli equipments nel treeview."""
        selected = self.equipment_filter_var.get()
        all_label = self.lang.get('all_equipments', 'Tutti gli equipments')
        
        # Pulisci treeview
        for item in self.equipments_tree.get_children():
            self.equipments_tree.delete(item)
        
        if selected == all_label:
            # Mostra tutti
            for equipment in self.all_equipments:
                self.equipments_tree.insert('', tk.END, iid=str(equipment['equipment_id']),
                                           values=(equipment['equipment_id'], equipment['description'], 
                                                 equipment['serial_number']))
        else:
            # Mostra solo quello selezionato
            try:
                equipment_id = int(selected.split(' - ')[0])
                equipment = next((e for e in self.all_equipments if e['equipment_id'] == equipment_id), None)
                if equipment:
                    self.equipments_tree.insert('', tk.END, iid=str(equipment['equipment_id']),
                                               values=(equipment['equipment_id'], equipment['description'], 
                                                     equipment['serial_number']))
            except (ValueError, IndexError):
                pass
    
    def _clear_equipment_filter(self):
        """Pulisce il filtro e mostra tutti gli equipments."""
        all_label = self.lang.get('all_equipments', 'Tutti gli equipments')
        self.equipment_filter_var.set(all_label)
        self._on_equipment_filter_select()
    
    def _on_equipment_select(self, event=None):
        """Gestisce la selezione di un equipment."""
        selection = self.equipments_tree.selection()
        if selection:
            self.current_equipment_id = int(selection[0])
        else:
            self.current_equipment_id = None
    
    def _new_equipment(self):
        """Apre dialog per nuovo equipment."""
        EquipmentEditorDialog(self, self.db, self.lang, None, self._load_equipments)
    
    def _edit_equipment(self):
        """Apre dialog per modifica equipment."""
        if not self.current_equipment_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_equipment_first', 'Seleziona un equipment da modificare.'),
                parent=self
            )
            return
        
        EquipmentEditorDialog(self, self.db, self.lang, self.current_equipment_id, self._load_equipments)
    
    def _delete_equipment(self):
        """Elimina l'equipment selezionato."""
        if not self.current_equipment_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_equipment_first', 'Seleziona un equipment da eliminare.'),
                parent=self
            )
            return
        
        # Conferma eliminazione
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_equipment', 'Sei sicuro di voler eliminare questo equipment?'),
            parent=self
        ):
            return
        
        try:
            query = "DELETE FROM [Traceability_RS].[fai].[FaiEquipments] WHERE FaiEquipmentid = ?"
            cursor = self.db.cursor
            cursor.execute(query, (self.current_equipment_id,))
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('equipment_deleted', 'Equipment eliminato con successo.'),
                parent=self
            )
            
            self.current_equipment_id = None
            self._load_equipments()
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Errore eliminazione equipment: {e}", exc_info=True)
            
            # Verifica se è un errore di constraint (equipment in uso)
            if 'REFERENCE constraint' in error_msg or 'FOREIGN KEY' in error_msg:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('equipment_in_use', 
                                 'Impossibile eliminare questo equipment perché è attualmente in uso.\n'
                                 'Rimuovere prima tutti i riferimenti a questo equipment.'),
                    parent=self
                )
            else:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"Impossibile eliminare l'equipment:\n{e}",
                    parent=self
                )



class TemplateEditorDialog(tk.Toplevel):
    """Dialog per inserimento/modifica template."""
    
    def __init__(self, parent, db, lang, template_id, callback):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.template_id = template_id
        self.callback = callback
        
        # Configura finestra
        title = lang.get('edit_template', 'Modifica Template') if template_id else lang.get('new_template', 'Nuovo Template')
        self.title(title)
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if template_id:
            self._load_template_data()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form campi
        row = 0
        
        # Nr. Documento
        ttk.Label(main_frame, text=self.lang.get('nr_document', 'Nr. Documento:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.nr_document_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nr_document_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Revisione
        ttk.Label(main_frame, text=self.lang.get('revision', 'Revisione:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.revision_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.revision_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Titolo
        ttk.Label(main_frame, text=self.lang.get('title', 'Titolo:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.title_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Data Revisione
        ttk.Label(main_frame, text=self.lang.get('revision_date', 'Data Revisione:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.revision_date_entry = DateEntry(main_frame, width=37, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.revision_date_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Configura grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def _load_template_data(self):
        """Carica i dati del template esistente."""
        try:
            query = """
            SELECT NrDocument, Revision, FaiTitle, RevisionDate
            FROM [Traceability_RS].[fai].[FaiTemplates]
            WHERE FaiTemplateId = ?
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (self.template_id,))
            row = cursor.fetchone()
            
            if row:
                self.nr_document_var.set(row.NrDocument or '')
                self.revision_var.set(row.Revision or '')
                self.title_var.set(row.FaiTitle or '')
                if row.RevisionDate:
                    self.revision_date_entry.set_date(row.RevisionDate)
                    
        except Exception as e:
            logger.error(f"Errore caricamento template {self.template_id}: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i dati del template:\n{e}",
                parent=self
            )
            self.destroy()
    
    def _save(self):
        """Salva il template."""
        # Validazione
        nr_document = self.nr_document_var.get().strip()
        revision = self.revision_var.get().strip()
        title = self.title_var.get().strip()
        
        if not title:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('title_required', 'Il titolo è obbligatorio.'),
                parent=self
            )
            return
        
        try:
            revision_date = self.revision_date_entry.get_date()
            
            if self.template_id:
                # Update
                query = """
                UPDATE [Traceability_RS].[fai].[FaiTemplates]
                SET NrDocument = ?,
                    Revision = ?,
                    FaiTitle = ?,
                    RevisionDate = ?
                WHERE FaiTemplateId = ?
                """
                params = (nr_document, revision, title, revision_date, self.template_id)
            else:
                # Insert
                query = """
                INSERT INTO [Traceability_RS].[fai].[FaiTemplates]
                (NrDocument, Revision, FaiTitle, RevisionDate)
                VALUES (?, ?, ?, ?)
                """
                params = (nr_document, revision, title, revision_date)
            
            cursor = self.db.cursor
            cursor.execute(query, params)
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('template_saved', 'Template salvato con successo.'),
                parent=self
            )
            
            # Callback per ricaricare lista
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio template: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare il template:\n{e}",
                parent=self
            )


class StepEditorDialog(tk.Toplevel):
    """Dialog per inserimento/modifica step."""
    
    def __init__(self, parent, db, lang, step_id, callback, default_template_id=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.step_id = step_id
        self.callback = callback
        self.default_template_id = default_template_id
        
        # Configura finestra
        title = lang.get('edit_step', 'Modifica Step') if step_id else lang.get('new_step', 'Nuovo Step')
        self.title(title)
        self.geometry("500x300")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if step_id:
            self._load_step_data()
        elif default_template_id:
            # Preseleziona il template se fornito
            self._preselect_template(default_template_id)
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form campi
        row = 0
        
        # Inizializza order_var prima di caricare i template (necessario per _update_suggested_order)
        self.order_var = tk.IntVar(value=1)
        
        # Template
        ttk.Label(main_frame, text=self.lang.get('template', 'Template:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(main_frame, 
                                           textvariable=self.template_var,
                                           width=37,
                                           state='readonly')
        self.template_combo.grid(row=row, column=1, sticky=tk.EW, pady=5)
        # Bind per aggiornare OrderInList quando cambia il template
        self.template_combo.bind('<<ComboboxSelected>>', self._on_template_change)
        self._load_templates()
        row += 1
        
        # Nome Step
        ttk.Label(main_frame, text=self.lang.get('step_name', 'Nome Step:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.step_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.step_name_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Ordine di visualizzazione (widget UI)
        ttk.Label(main_frame, text=self.lang.get('order_in_list', 'Ordine:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(main_frame, from_=1, to=255, textvariable=self.order_var, width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Configura grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def _load_templates(self):
        """Carica i template disponibili nel combo."""
        try:
            query = """
            SELECT FaiTemplateId, FaiTitle, NrDocument
            FROM [Traceability_RS].[fai].[FaiTemplates]
            ORDER BY FaiTemplateId DESC
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.templates_data = {}
            template_values = []
            
            for row in rows:
                template_id = row.FaiTemplateId
                title = row.FaiTitle or row.NrDocument or f"Template {template_id}"
                label = f"{template_id} - {title}"
                template_values.append(label)
                self.templates_data[label] = template_id
            
            self.template_combo['values'] = template_values
            if template_values:
                self.template_var.set(template_values[0])
                # Se stiamo creando un nuovo step, aggiorna l'OrderInList suggerito
                if not self.step_id:
                    self._update_suggested_order()
                
        except Exception as e:
            logger.error(f"Errore caricamento template: {e}", exc_info=True)
    
    def _preselect_template(self, template_id):
        """Preseleziona un template nel combo."""
        for label, tid in self.templates_data.items():
            if tid == template_id:
                self.template_var.set(label)
                # Aggiorna l'OrderInList suggerito per questo template
                if not self.step_id:  # Solo per nuovi step
                    self._update_suggested_order()
                break
    
    def _on_template_change(self, event=None):
        """Gestisce il cambio di template e aggiorna OrderInList suggerito."""
        if not self.step_id:  # Solo per nuovi step, non in modifica
            self._update_suggested_order()
    
    def _update_suggested_order(self):
        """Calcola e imposta il prossimo OrderInList disponibile per il template selezionato."""
        template_label = self.template_var.get()
        if not template_label or template_label not in self.templates_data:
            return
        
        try:
            template_id = self.templates_data[template_label]
            
            # Query per trovare il massimo OrderInList per questo template (solo record attivi)
            query = """
            SELECT ISNULL(MAX(OrderInList), 0) as MaxOrder
            FROM [Traceability_RS].[fai].[FaiSteps]
            WHERE FaiTemplateId = ? AND DateOut IS NULL
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (template_id,))
            result = cursor.fetchone()
            
            if result:
                max_order = result.MaxOrder if result.MaxOrder is not None else 0
                # Suggerisci il prossimo numero (max + 1), ma non superare 255
                next_order = min(max_order + 1, 255)
                self.order_var.set(next_order)
                logger.info(f"OrderInList suggerito per template {template_id}: {next_order}")
                
        except Exception as e:
            logger.error(f"Errore calcolo OrderInList suggerito: {e}", exc_info=True)
            # In caso di errore, mantieni il valore predefinito (1)
    
    def _load_step_data(self):
        """Carica i dati dello step esistente."""
        try:
            query = """
            SELECT StepName, FaiTemplateId, OrderInList
            FROM [Traceability_RS].[fai].[FaiSteps]
            WHERE FatStepId = ?
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (self.step_id,))
            row = cursor.fetchone()
            
            if row:
                self.step_name_var.set(row.StepName or '')
                
                # Seleziona template
                for label, tid in self.templates_data.items():
                    if tid == row.FaiTemplateId:
                        self.template_var.set(label)
                        break
                
                # Imposta ordine
                if row.OrderInList is not None:
                    self.order_var.set(row.OrderInList)
                    
        except Exception as e:
            logger.error(f"Errore caricamento step {self.step_id}: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i dati dello step:\n{e}",
                parent=self
            )
            self.destroy()
    
    def _save(self):
        """Salva lo step."""
        # Validazione
        step_name = self.step_name_var.get().strip()
        template_label = self.template_var.get()
        
        if not step_name:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('step_name_required', 'Il nome dello step è obbligatorio.'),
                parent=self
            )
            return
        
        if not template_label or template_label not in self.templates_data:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('template_required', 'Seleziona un template.'),
                parent=self
            )
            return
        
        try:
            template_id = self.templates_data[template_label]
            order_in_list = self.order_var.get()
            
            # Validazione: verifica che OrderInList sia unico per questo template (escludendo record cancellati)
            check_query = """
            SELECT COUNT(*) as Count
            FROM [Traceability_RS].[fai].[FaiSteps]
            WHERE FaiTemplateId = ? 
            AND OrderInList = ? 
            AND DateOut IS NULL
            AND FatStepId != ?
            """
            
            cursor = self.db.cursor
            # Se stiamo creando un nuovo step, usa 0 come ID (non esisterà mai)
            check_step_id = self.step_id if self.step_id else 0
            cursor.execute(check_query, (template_id, order_in_list, check_step_id))
            result = cursor.fetchone()
            
            if result and result.Count > 0:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('order_already_exists', 
                                 f'Esiste già uno step attivo con ordine {order_in_list} per questo template.\n'
                                 f'Scegli un numero di ordine diverso.'),
                    parent=self
                )
                return
            
            if self.step_id:
                # Update
                query = """
                UPDATE [Traceability_RS].[fai].[FaiSteps]
                SET StepName = ?,
                    FaiTemplateId = ?,
                    OrderInList = ?
                WHERE FatStepId = ?
                """
                params = (step_name, template_id, order_in_list, self.step_id)
            else:
                # Insert
                query = """
                INSERT INTO [Traceability_RS].[fai].[FaiSteps]
                (StepName, FaiTemplateId, OrderInList)
                VALUES (?, ?, ?)
                """
                params = (step_name, template_id, order_in_list)
            
            cursor = self.db.cursor
            cursor.execute(query, params)
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('step_saved', 'Step salvato con successo.'),
                parent=self
            )
            
            # Callback per ricaricare lista
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio step: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare lo step:\n{e}",
                parent=self
            )


class StepDetailEditorDialog(tk.Toplevel):
    """Dialog per inserimento/modifica step detail."""
    
    def __init__(self, parent, db, lang, detail_id, callback, default_step_id=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.detail_id = detail_id
        self.callback = callback
        self.default_step_id = default_step_id
        
        # Configura finestra
        title = lang.get('edit_step_detail', 'Modifica Step Detail') if detail_id else lang.get('new_step_detail', 'Nuovo Step Detail')
        self.title(title)
        self.geometry("600x350")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if detail_id:
            self._load_detail_data()
        elif default_step_id:
            self._preselect_step(default_step_id)
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form campi
        row = 0
        
        # Step (obbligatorio)
        ttk.Label(main_frame, text=self.lang.get('step', 'Step:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.step_var = tk.StringVar()
        self.step_combo = ttk.Combobox(main_frame, 
                                       textvariable=self.step_var,
                                       width=50,
                                       state='readonly')
        self.step_combo.grid(row=row, column=1, sticky=tk.EW, pady=5)
        self.step_combo.bind('<<ComboboxSelected>>', self._on_step_change)
        self._load_steps()
        row += 1
        
        # OrdineList (numero d'ordine, obbligatorio)
        ttk.Label(main_frame, text=self.lang.get('ordine_in_list', 'Ordine:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ordine_var = tk.IntVar(value=1)
        ordine_spinbox = ttk.Spinbox(main_frame, 
                                     from_=1, to=255, 
                                     textvariable=self.ordine_var,
                                     width=10)
        ordine_spinbox.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Step Detail (obbligatorio)
        ttk.Label(main_frame, text=self.lang.get('step_detail', 'Dettaglio:')).grid(row=row, column=0, sticky=tk.NW, pady=5)
        self.step_detail_text = tk.Text(main_frame, width=50, height=8, wrap=tk.WORD)
        self.step_detail_text.grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Equipment (opzionale)
        ttk.Label(main_frame, text=self.lang.get('equipment', 'Equipment:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.equipment_var = tk.StringVar()
        self.equipment_combo = ttk.Combobox(main_frame, 
                                            textvariable=self.equipment_var,
                                            width=50,
                                            state='readonly')
        self.equipment_combo.grid(row=row, column=1, sticky=tk.EW, pady=5)
        self._load_equipments()
        row += 1
        
        # KeepOnsameLine (checkbox)
        self.keep_on_same_line_var = tk.BooleanVar(value=False)
        chk_keep_same_line = ttk.Checkbutton(
            main_frame, 
            text=self.lang.get('keep_on_same_line', 'Mantieni sulla stessa riga'),
            variable=self.keep_on_same_line_var
        )
        chk_keep_same_line.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Configura grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def _load_steps(self):
        """Carica gli steps disponibili (solo attivi)."""
        try:
            query = """
            SELECT s.FatStepId, s.StepName, t.NrDocument
            FROM [Traceability_RS].[fai].[FaiSteps] s
            INNER JOIN [Traceability_RS].[fai].[FaiTemplates] t ON s.FaiTemplateId = t.FaiTemplateId
            WHERE s.DateOut IS NULL
            ORDER BY s.OrderInList, s.StepName
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.steps_data = {}
            step_values = []
            
            for row in rows:
                step_id = row.FatStepId
                step_name = row.StepName or f"Step {step_id}"
                nr_document = row.NrDocument or ''
                label = f"{step_id} - {step_name} -> {nr_document}"
                step_values.append(label)
                self.steps_data[label] = step_id
            
            self.step_combo['values'] = step_values
            
        except Exception as e:
            logger.error(f"Errore caricamento steps: {e}", exc_info=True)
    
    def _load_equipments(self):
        """Carica gli equipments disponibili."""
        try:
            query = """
            SELECT FaiEquipmentid, Description, SerialNumber
            FROM [Traceability_RS].[fai].[FaiEquipments]
            ORDER BY Description, SerialNumber
            """
            
            cursor = self.db.cursor
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.equipments_data = {}
            equipment_values = [self.lang.get('no_equipment', 'Nessun Equipment')]
            self.equipments_data[equipment_values[0]] = None
            
            for row in rows:
                equipment_id = row.FaiEquipmentid
                description = row.Description or ''
                serial_number = row.SerialNumber or ''
                label = f"{equipment_id} - {description} {serial_number}".strip()
                equipment_values.append(label)
                self.equipments_data[label] = equipment_id
            
            self.equipment_combo['values'] = equipment_values
            self.equipment_var.set(equipment_values[0])
            
        except Exception as e:
            logger.error(f"Errore caricamento equipments: {e}", exc_info=True)
    
    def _on_step_change(self, event=None):
        """Quando si cambia step, aggiorna il suggerimento di OrdineList."""
        self._update_suggested_ordine()
    
    def _update_suggested_ordine(self):
        """Suggerisce il prossimo OrdineList disponibile per lo step selezionato."""
        step_label = self.step_var.get()
        if not step_label or step_label not in self.steps_data:
            return
        
        try:
            step_id = self.steps_data[step_label]
            
            # Query per trovare il massimo OrdineList per questo step
            query = """
            SELECT ISNULL(MAX(OrdineList), 0) AS MaxOrdine
            FROM [Traceability_RS].[fai].[FaiStepDetails]
            WHERE FatStepId = ? AND DateOut IS NULL
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (step_id,))
            row = cursor.fetchone()
            
            max_ordine = row.MaxOrdine if row else 0
            suggested_ordine = min(max_ordine + 1, 255)
            
            # Imposta il valore suggerito
            self.ordine_var.set(suggested_ordine)
            
        except Exception as e:
            logger.error(f"Errore aggiornamento suggerimento OrdineList: {e}", exc_info=True)
    
    def _preselect_step(self, step_id):
        """Preseleziona uno step nel combo e aggiorna OrdineList suggerito."""
        for label, sid in self.steps_data.items():
            if sid == step_id:
                self.step_var.set(label)
                self._update_suggested_ordine()
                break
    
    def _load_detail_data(self):
        """Carica i dati del detail esistente."""
        try:
            query = """
            SELECT FatStepId, OrdineList, StepDetail, FaiEquipmentid, KeepOnsameLine
            FROM [Traceability_RS].[fai].[FaiStepDetails]
            WHERE FaiStepDetailId = ?
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (self.detail_id,))
            row = cursor.fetchone()
            
            if row:
                # Preseleziona step (aggiorna anche il suggerimento ordine)
                self._preselect_step(row.FatStepId)
                
                # OrdineList
                self.ordine_var.set(row.OrdineList or 1)
                
                # Step Detail
                self.step_detail_text.delete('1.0', tk.END)
                self.step_detail_text.insert('1.0', row.StepDetail or '')
                
                # Equipment
                if row.FaiEquipmentid:
                    for label, eq_id in self.equipments_data.items():
                        if eq_id == row.FaiEquipmentid:
                            self.equipment_var.set(label)
                            break
                
                # KeepOnsameLine
                self.keep_on_same_line_var.set(bool(row.KeepOnsameLine))
                    
        except Exception as e:
            logger.error(f"Errore caricamento step detail {self.detail_id}: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i dati dello step detail:\n{e}",
                parent=self
            )
            self.destroy()
    
    def _save(self):
        """Salva lo step detail."""
        # Validazione
        step_label = self.step_var.get()
        ordine_list = self.ordine_var.get()
        step_detail = self.step_detail_text.get('1.0', tk.END).strip()
        equipment_label = self.equipment_var.get()
        
        if not step_label or step_label not in self.steps_data:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('step_required', 'Seleziona uno step.'),
                parent=self
            )
            return
        
        if not step_detail:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('step_detail_required', 'Il campo Dettaglio è obbligatorio.'),
                parent=self
            )
            return
        
        try:
            step_id = self.steps_data[step_label]
            equipment_id = self.equipments_data.get(equipment_label, None)
            
            # Validazione unicità OrdineList per questo step (solo attivi)
            check_query = """
            SELECT COUNT(*) AS cnt
            FROM [Traceability_RS].[fai].[FaiStepDetails]
            WHERE FatStepId = ? AND OrdineList = ? AND DateOut IS NULL AND FaiStepDetailId != ?
            """
            cursor = self.db.cursor
            cursor.execute(check_query, (step_id, ordine_list, self.detail_id or 0))
            result = cursor.fetchone()
            
            if result and result.cnt > 0:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('ordine_already_exists', 
                                 f'Esiste già un detail con ordine {ordine_list} per questo step.'),
                    parent=self
                )
                return
            
            if self.detail_id:
                # Update
                query = """
                UPDATE [Traceability_RS].[fai].[FaiStepDetails]
                SET FatStepId = ?,
                    OrdineList = ?,
                    StepDetail = ?,
                    FaiEquipmentid = ?,
                    KeepOnsameLine = ?
                WHERE FaiStepDetailId = ?
                """
                params = (step_id, ordine_list, step_detail, equipment_id, 
                         self.keep_on_same_line_var.get(), self.detail_id)
            else:
                # Insert
                query = """
                INSERT INTO [Traceability_RS].[fai].[FaiStepDetails]
                (FatStepId, OrdineList, StepDetail, FaiEquipmentid, KeepOnsameLine)
                VALUES (?, ?, ?, ?, ?)
                """
                params = (step_id, ordine_list, step_detail, equipment_id, 
                         self.keep_on_same_line_var.get())
            
            cursor.execute(query, params)
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('step_detail_saved', 'Step Detail salvato con successo.'),
                parent=self
            )
            
            # Callback per ricaricare lista
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio step detail: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare lo step detail:\n{e}",
                parent=self
            )


class EquipmentEditorDialog(tk.Toplevel):
    """Dialog per inserimento/modifica equipment."""
    
    def __init__(self, parent, db, lang, equipment_id, callback):
        super().__init__(parent)
        self.db = db
        self.lang = lang  
        self.equipment_id = equipment_id
        self.callback = callback
        
        # Configura finestra
        title = lang.get('edit_equipment', 'Modifica Equipment') if equipment_id else lang.get('new_equipment', 'Nuovo Equipment')
        self.title(title)
        self.geometry("500x250")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if equipment_id:
            self._load_equipment_data()
    
    def _create_widgets(self):
        """Crea i widget del dialog."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form campi
        row = 0
        
        # Descrizione
        ttk.Label(main_frame, text=self.lang.get('description', 'Descrizione:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.description_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Numero Seriale
        ttk.Label(main_frame, text=self.lang.get('serial_number', 'Numero Seriale:')).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.serial_number_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.serial_number_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        row += 1
        
        # Configura grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel', 'Annulla'),
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def _load_equipment_data(self):
        """Carica i dati dell'equipment esistente."""
        try:
            query = """
            SELECT Description, SerialNumber
            FROM [Traceability_RS].[fai].[FaiEquipments]
            WHERE FaiEquipmentid = ?
            """
            
            cursor = self.db.cursor
            cursor.execute(query, (self.equipment_id,))
            row = cursor.fetchone()
            
            if row:
                self.description_var.set(row.Description or '')
                self.serial_number_var.set(row.SerialNumber or '')
                    
        except Exception as e:
            logger.error(f"Errore caricamento equipment {self.equipment_id}: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare i dati dell'equipment:\n{e}",
                parent=self
            )
            self.destroy()
    
    def _save(self):
        """Salva l'equipment."""
        # Validazione
        description = self.description_var.get().strip()
        serial_number = self.serial_number_var.get().strip()
        
        if not description and not serial_number:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('equipment_fields_required', 'Compilare almeno uno tra Descrizione e Numero Seriale.'),
                parent=self
            )
            return
        
        try:
            if self.equipment_id:
                # Update
                query = """
                UPDATE [Traceability_RS].[fai].[FaiEquipments]
                SET Description = ?,
                    SerialNumber = ?
                WHERE FaiEquipmentid = ?
                """
                params = (description, serial_number, self.equipment_id)
            else:
                # Insert
                query = """
                INSERT INTO [Traceability_RS].[fai].[FaiEquipments]
                (Description, SerialNumber)
                VALUES (?, ?)
                """
                params = (description, serial_number)
            
            cursor = self.db.cursor
            cursor.execute(query, params)
            self.db.conn.commit()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('equipment_saved', 'Equipment salvato con successo.'),
                parent=self
            )
            
            # Callback per ricaricare lista
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            logger.error(f"Errore salvataggio equipment: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile salvare l'equipment:\n{e}",
                parent=self
            )



def open_fai_template_manager(parent, db, lang, user_name):
    """Apre la finestra di gestione template FAI."""
    FaiTemplateManagerWindow(parent, db, lang, user_name)
