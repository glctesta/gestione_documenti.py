"""
Overtime Reports GUI
Form per la generazione di rapporti e statistiche straordinari
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from tkcalendar import DateEntry
import logging

logger = logging.getLogger(__name__)


def open_overtime_reports_window(parent, db_handler, lang_manager, user_name):
    """
    Apre la finestra per generare rapporti straordinari.
    
    Args:
        parent: Finestra parent
        db_handler: DatabaseHandler instance
        lang_manager: LanguageManager instance
        user_name: Nome utente loggato
    """
    OvertimeReportsWindow(parent, db_handler, lang_manager, user_name)


class OvertimeReportsWindow(tk.Toplevel):
    """
    Finestra per generare rapporti e statistiche straordinari.
    """
    
    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        
        # Setup finestra
        self.title(self.lang.get('overtime_reports_title', 'Rapporti Straordinari'))
        self.geometry("1200x700")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea i widget dell'interfaccia."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === FILTRI ===
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding="10")
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Periodo
        ttk.Label(filter_frame, text=self.lang.get('period', 'Periodo:')).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filter_frame, text=self.lang.get('from', 'Da:')).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.start_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.start_date.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filter_frame, text=self.lang.get('to', 'A:')).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.end_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.end_date.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        # Tipo rapporto
        ttk.Label(filter_frame, text=self.lang.get('report_type', 'Tipo Rapporto:')).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.report_type_var = tk.StringVar(value='summary')
        report_types = [
            ('summary', self.lang.get('summary_report', 'Riepilogo Generale')),
            ('by_employee', self.lang.get('by_employee', 'Per Dipendente')),
            ('by_reason', self.lang.get('by_reason', 'Per Motivo')),
            ('by_department', self.lang.get('by_department', 'Per Reparto'))
        ]
        
        report_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.report_type_var,
            values=[r[1] for r in report_types],
            state='readonly',
            width=25
        )
        report_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Pulsanti
        ttk.Button(
            filter_frame,
            text=self.lang.get('generate_report', 'Genera Rapporto'),
            command=self._generate_report
        ).grid(row=1, column=3, columnspan=2, padx=5, pady=5)
        
        # === RISULTATI ===
        results_frame = ttk.LabelFrame(main_frame, text=self.lang.get('results', 'Risultati'), padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Notebook per diverse viste
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab Tabella
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text=self.lang.get('table_view', 'Vista Tabella'))
        
        columns = ('employee', 'reason', 'date', 'hours', 'status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        self.tree.heading('employee', text=self.lang.get('employee', 'Dipendente'))
        self.tree.heading('reason', text=self.lang.get('reason', 'Motivo'))
        self.tree.heading('date', text=self.lang.get('date', 'Data'))
        self.tree.heading('hours', text=self.lang.get('hours', 'Ore'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab Statistiche
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text=self.lang.get('statistics', 'Statistiche'))
        
        self.stats_text = tk.Text(stats_frame, wrap=tk.WORD, height=20)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === PULSANTI EXPORT ===
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            export_frame,
            text=self.lang.get('export_excel', 'Esporta Excel'),
            command=self._export_to_excel
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            export_frame,
            text=self.lang.get('export_pdf', 'Esporta PDF'),
            command=self._export_to_pdf
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            export_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _generate_report(self):
        """Genera il rapporto in base ai filtri selezionati."""
        # Pulisci risultati precedenti
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.stats_text.delete('1.0', tk.END)
        
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        
        # Query base
        query = """
        SELECT 
            e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName,
            s.Descriptionreasons,
            s.DateStart,
            DATEDIFF(HOUR, s.DateStart, s.DateEnd) AS Hours,
            CASE 
                WHEN s.SuperVisorId IS NULL THEN 'Pending'
                WHEN s.SuperVisorId > 0 THEN 'Approved'
                ELSE 'Rejected'
            END AS Status
        FROM ResetServices.dbo.ExtraTimeApprovalStory s
        INNER JOIN Employee.dbo.EmployeeHireHistory h ON s.IdEmployee = h.EmployeeHireHistoryId
        INNER JOIN Employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
        WHERE s.DateStart >= ? AND s.DateStart <= ?
        ORDER BY s.DateStart DESC
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            cursor.close()
            
            # Popola tabella
            total_hours = 0
            approved_hours = 0
            pending_hours = 0
            rejected_hours = 0
            
            for row in results:
                date_str = row[2].strftime('%d/%m/%Y %H:%M') if row[2] else 'N/D'
                hours = row[3] if row[3] else 0
                status = row[4]
                
                self.tree.insert('', tk.END, values=(
                    row[0],  # Employee
                    row[1],  # Reason
                    date_str,  # Date
                    hours,  # Hours
                    status  # Status
                ))
                
                total_hours += hours
                if status == 'Approved':
                    approved_hours += hours
                elif status == 'Pending':
                    pending_hours += hours
                elif status == 'Rejected':
                    rejected_hours += hours
            
            # Genera statistiche
            stats = f"""
STATISTICHE STRAORDINARI
Periodo: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}

RIEPILOGO GENERALE:
- Totale richieste: {len(results)}
- Ore totali richieste: {total_hours}

PER STATO:
- Ore approvate: {approved_hours}
- Ore in attesa: {pending_hours}
- Ore rifiutate: {rejected_hours}

PERCENTUALI:
- Approvate: {(approved_hours/total_hours*100) if total_hours > 0 else 0:.1f}%
- In attesa: {(pending_hours/total_hours*100) if total_hours > 0 else 0:.1f}%
- Rifiutate: {(rejected_hours/total_hours*100) if total_hours > 0 else 0:.1f}%
            """
            
            self.stats_text.insert('1.0', stats)
            
        except Exception as e:
            logger.error(f"Errore generazione rapporto: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore generazione rapporto:\n{str(e)}",
                parent=self
            )
    
    def _export_to_excel(self):
        """Esporta i risultati in Excel."""
        if not self.tree.get_children():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_data_to_export', 'Nessun dato da esportare'),
                parent=self
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=self.lang.get('save_excel', 'Salva Excel')
        )
        
        if not file_path:
            return
        
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Straordinari"
            
            # Header
            headers = ['Dipendente', 'Motivo', 'Data', 'Ore', 'Stato']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
            
            # Dati
            for row_idx, item in enumerate(self.tree.get_children(), 2):
                values = self.tree.item(item)['values']
                for col_idx, value in enumerate(values, 1):
                    ws.cell(row=row_idx, column=col_idx, value=value)
            
            wb.save(file_path)
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('excel_exported', 'File Excel esportato con successo'),
                parent=self
            )
            
        except ImportError:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                "Libreria openpyxl non installata.\nInstallare con: pip install openpyxl",
                parent=self
            )
        except Exception as e:
            logger.error(f"Errore export Excel: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore export Excel:\n{str(e)}",
                parent=self
            )
    
    def _export_to_pdf(self):
        """Esporta i risultati in PDF."""
        if not self.tree.get_children():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_data_to_export', 'Nessun dato da esportare'),
                parent=self
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title=self.lang.get('save_pdf', 'Salva PDF')
        )
        
        if not file_path:
            return
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import cm
            from reportlab.platypus import Table, TableStyle
            from reportlab.lib import colors
            
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)
            
            # Titolo
            c.setFont("Helvetica-Bold", 16)
            c.drawString(2 * cm, height - 2 * cm, "RAPPORTO STRAORDINARI")
            
            c.setFont("Helvetica", 10)
            c.drawString(2 * cm, height - 2.5 * cm, 
                f"Periodo: {self.start_date.get_date().strftime('%d/%m/%Y')} - {self.end_date.get_date().strftime('%d/%m/%Y')}")
            
            # Tabella
            table_data = [['Dipendente', 'Motivo', 'Data', 'Ore', 'Stato']]
            
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                table_data.append(values)
            
            table = Table(table_data, colWidths=[5*cm, 5*cm, 4*cm, 2*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            table.wrapOn(c, width, height)
            table.drawOn(c, 2 * cm, height - 8 * cm)
            
            c.save()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('pdf_exported', 'File PDF esportato con successo'),
                parent=self
            )
            
        except Exception as e:
            logger.error(f"Errore export PDF: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore export PDF:\n{str(e)}",
                parent=self
            )
