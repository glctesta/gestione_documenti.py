import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import os
from .project_window import ProjectWindow
from .gantt_window import NpiGanttWindow
from .analysis_window import ProjectAnalysisWindow

# Import per PDF
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)


class NpiDashboardWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.master_app = master

        self.title(self.lang.get('npi_dashboard_title', "Dashboard Progetti NPI"))
        self.geometry("1200x600")  # Finestra più larga per nuove colonne
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self.load_npi_projects()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('active_npi_projects', "Progetti NPI Attivi"),
                                    padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # --- COLONNE AGGIORNATE ---
        cols = ('project_name', 'product_code', 'customer', 'milestone_due_date')
        self.project_tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        self.project_tree.heading('project_name', text=self.lang.get('col_project_name', 'Nome Progetto'))
        self.project_tree.column('project_name', width=300)
        self.project_tree.heading('product_code', text=self.lang.get('col_product_code', 'Codice Prodotto'))
        self.project_tree.column('product_code', width=150)
        self.project_tree.heading('customer', text=self.lang.get('col_customer', 'Cliente'))
        self.project_tree.column('customer', width=180)
        self.project_tree.heading('milestone_due_date',
                                  text=self.lang.get('col_milestone_due_date', 'Scadenza Milestone Finale'))
        self.project_tree.column('milestone_due_date', width=200, anchor=tk.CENTER)

        self.project_tree.pack(fill=tk.BOTH, expand=True)

        # Bind per doppio click -> ora apre la finestra di analisi
        self.project_tree.bind('<Double-1>', self._on_double_click)
        # Il menu contestuale rimane per le altre azioni
        self.project_tree.bind("<Button-3>", self._show_project_context_menu)

        button_frame = ttk.Frame(main_frame, padding=(0, 10, 0, 0))
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text=self.lang.get('btn_refresh', 'Aggiorna'), command=self.load_npi_projects).pack(
            side=tk.LEFT, padx=5)
        # --- NUOVO BOTTONE "ANALISI" ---
        ttk.Button(button_frame, text=self.lang.get('btn_analyze', 'Analisi'),
                   command=self._launch_analysis_window).pack(side=tk.LEFT, padx=5)

        # --- NUOVO BOTTONE EXPORT PDF ---
        self.export_pdf_button = ttk.Button(button_frame, text=self.lang.get('btn_export_pdf', 'Export PDF a C:\\Temp'),
                                            command=self._export_summary_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=5)
        if not REPORTLAB_AVAILABLE:
            self.export_pdf_button.config(state=tk.DISABLED)

        ttk.Button(button_frame, text=self.lang.get('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    def load_npi_projects(self):
        for i in self.project_tree.get_children():
            self.project_tree.delete(i)

        try:
            # --- USA IL NUOVO METODO DEL MANAGER ---
            progetti = self.npi_manager.get_dashboard_projects()

            if not progetti:
                self.project_tree.insert('', tk.END, text="-1",
                                         values=(self.lang.get('no_active_projects', "Nessun progetto attivo trovato."),
                                                 "", "", ""))
                return

            for proj in progetti:
                due_date = proj.ScadenzaMilestoneFinale
                display_date = due_date.strftime('%d/%m/%Y') if due_date else "N/D"

                # Aggiungi simbolo di warning se scaduto
                if due_date and due_date.date() < datetime.now().date():
                    display_date += ' ❗'  # Simbolo di warning

                # L'ID progetto è salvato nel campo 'text' nascosto
                self.project_tree.insert(
                    '', tk.END,
                    text=str(proj.ProgettoId),
                    values=(
                        proj.NomeProgetto,
                        proj.CodiceProdotto or "",
                        proj.Cliente or "",
                        display_date
                    )
                )
        except Exception as e:
            logger.error(f"Errore nel caricamento progetti dashboard: {e}", exc_info=True)
            self.project_tree.insert('', tk.END, text="-1",
                                     values=("Errore", "Impossibile caricare i dati.", str(e), ""))

    def _on_double_click(self, event):
        """Il doppio click ora lancia la finestra di analisi."""
        self._launch_analysis_window()

    def _get_selected_project_info(self):
        """Helper per recuperare ID e nome del progetto selezionato."""
        selection = self.project_tree.selection()
        if not selection:
            messagebox.showwarning("Selezione", "Seleziona un progetto dalla lista.", parent=self)
            return None, None

        item_iid = selection[0]
        project_id = self.project_tree.item(item_iid, 'text')
        values = self.project_tree.item(item_iid, 'values')

        try:
            project_id = int(project_id)
            project_name = values[0]  # Il nome progetto è il primo valore della riga
            return project_id, project_name
        except (ValueError, IndexError):
            messagebox.showwarning("Selezione", "Seleziona un progetto valido dalla lista.", parent=self)
            return None, None

    def _launch_analysis_window(self):
        """Lancia la nuova finestra di analisi."""
        project_id, project_name = self._get_selected_project_info()
        if project_id is None:
            return

        ProjectAnalysisWindow(self, self.npi_manager, self.lang, project_id, project_name)

    # Il menu contestuale rimane per le azioni "vecchie"
    def _show_project_context_menu(self, event):
        iid = self.project_tree.identify_row(event.y)
        if not iid: return

        # Seleziona la riga cliccata
        self.project_tree.selection_set(iid)

        project_id, _ = self._get_selected_project_info()
        if project_id is None: return

        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label=self.lang.get('manage_project', "Gestisci Dettagli Task..."),
                                 command=self._launch_project_window)
        context_menu.add_command(label=self.lang.get('npi_view_gantt', "Visualizza Gantt..."),
                                 command=self._launch_gantt_window)
        context_menu.post(event.x_root, event.y_root)

    def _launch_project_window(self):
        """Apre la finestra di gestione dettaglio task."""
        project_id, _ = self._get_selected_project_info()
        if project_id is None: return

        # Usa l'helper di autorizzazione del master se esiste
        if hasattr(self.master_app, '_execute_authorized_action'):
            self.master_app._execute_authorized_action(
                menu_translation_key='project_window',
                action_callback=lambda: ProjectWindow(self, self.npi_manager, self.lang, project_id)
            )
        else:  # Fallback per test
            ProjectWindow(self, self.npi_manager, self.lang, project_id)

    def _launch_gantt_window(self):
        """Apre la finestra Gantt per il progetto selezionato."""
        project_id, _ = self._get_selected_project_info()
        if project_id is None: return

        NpiGanttWindow(self, self.npi_manager, self.lang, project_id)

    def _export_summary_pdf(self):
        """Genera un report PDF professionale con tutti i progetti e le loro analisi."""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Libreria Mancante",
                                 "La libreria 'reportlab' è necessaria per l'export PDF.\nInstallala con: pip install reportlab",
                                 parent=self)
            return

        self.export_pdf_button.config(state=tk.DISABLED)
        self.update_idletasks()

        try:
            full_report_data = self.npi_manager.get_full_projects_report_data()
            if not full_report_data:
                messagebox.showinfo("Info", "Nessun progetto da includere nel report.", parent=self)
                return

            # Prepara percorso e file
            temp_dir = "C:\\Temp"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, f"NPI_Projects_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

            # Crea il documento
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4

            # Funzione helper per disegnare sezioni
            def draw_project_section(y_start, project_data):
                y = y_start
                # Titolo progetto
                c.setFont("Helvetica-Bold", 12)
                c.drawString(inch, y, f"Project: {project_data['info'].NomeProgetto}")
                y -= 20

                # Dettagli progetto
                c.setFont("Helvetica", 9)
                c.drawString(inch, y, f"Product Code: {project_data['info'].CodiceProdotto or 'N/A'}  |  "
                                      f"Customer: {project_data['info'].Cliente or 'N/A'}")
                y -= 15
                due_date_str = project_data['info'].ScadenzaMilestoneFinale.strftime('%Y-%m-%d') if project_data[
                    'info'].ScadenzaMilestoneFinale else "Not Set"
                c.drawString(inch, y, f"Final Milestone Due Date: {due_date_str}")
                y -= 25

                # Analisi ritardi
                c.setFont("Helvetica-Bold", 10)
                c.drawString(inch, y, "Overdue Task Analysis:")
                y -= 20

                analysis = project_data['analysis']
                if not analysis:
                    c.setFont("Helvetica-Oblique", 9)
                    c.setFillColor(colors.green)
                    c.drawString(inch, y, "No overdue tasks found.")
                    c.setFillColor(colors.black)
                    y -= 20
                else:
                    table_data = [['Owner', '# Late Tasks']]
                    for item in analysis:
                        table_data.append([item['owner_name'], item['late_count']])

                    # Crea la tabella
                    table = Table(table_data, colWidths=[3 * inch, 1.5 * inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))

                    table.wrapOn(c, width, height)
                    table.drawOn(c, inch, y - table._height)
                    y -= (table._height + 20)

                # Linea separatrice
                c.line(inch, y, width - inch, y)
                y -= 15
                return y

            # === Costruzione del PDF ===
            y_pos = height - inch
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2.0, y_pos, "NPI Projects Summary Report")
            y_pos -= 20
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2.0, y_pos, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            y_pos -= 40

            for project in full_report_data:
                # Controlla se c'è abbastanza spazio per la prossima sezione
                # (Stima approssimativa dell'altezza, meglio essere conservativi)
                estimated_height = 120 + (len(project['analysis']) * 20 if project['analysis'] else 0)
                if y_pos < estimated_height:
                    c.showPage()  # Nuova pagina
                    y_pos = height - inch  # Reset Y

                y_pos = draw_project_section(y_pos, project)

            c.save()

            if messagebox.askyesno("Successo", f"Report PDF salvato con successo in:\n{file_path}\n\nVuoi aprirlo ora?",
                                   parent=self):
                os.startfile(file_path)

        except Exception as e:
            logger.error(f"Errore durante l'export PDF: {e}", exc_info=True)
            messagebox.showerror("Errore Export", f"Impossibile generare il PDF:\n{e}", parent=self)
        finally:
            self.export_pdf_button.config(state=tk.NORMAL)