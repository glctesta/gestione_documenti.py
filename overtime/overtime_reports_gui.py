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
        SELECT DISTINCT
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
        """Esporta i risultati in PDF con calcolo costi."""
        if not self.tree.get_children():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_data_to_export', 'Nessun dato da esportare'),
                parent=self
            )
            return
        
        try:
            import os
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import cm
            from reportlab.platypus import Table, TableStyle, Image as ReportLabImage
            from reportlab.lib import colors
            from collections import defaultdict
            from datetime import datetime
            
            # Recupera prezzi straordinari
            pricing_query = """
            SELECT t.[Description], d.ValueITem [Value], v.[DESC] Currency,
                  case
                    when t.[Description] = 'WeekendCost' then
                        1
                    else
                        0
                end
                as IsWeekend            
              FROM 
              ResetServices.dbo.OverTimeDefaults D inner join 
              [ResetServices].[dbo].[OverTimeDescriptions] T on t.DescpriptionId=d.DescriptionId inner join 
              ResetServices.dbo.TbValute v on v.IdValuta =d.CurrencyId
              where t.DateOut is null and d.DateOut is null
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(pricing_query)
            pricing_results = cursor.fetchall()
            
            # Estrai prezzi
            weekday_cost = 0
            weekend_cost = 0
            currency = "EUR"
            
            for row in pricing_results:
                if row[3] == 1:  # IsWeekend
                    weekend_cost = float(row[1])
                else:
                    weekday_cost = float(row[1])
                currency = row[2] if row[2] else "EUR"
            
            # Recupera dati straordinari con date complete
            overtime_query = """
            SELECT 
                e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName,
                s.Descriptionreasons,
                s.DateStart,
                s.DateEnd,
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
            
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            
            cursor.execute(overtime_query, (start_date, end_date))
            overtime_results = cursor.fetchall()
            cursor.close()
            
            # Calcola costi per mese e anno
            monthly_costs = defaultdict(lambda: {'hours': 0, 'cost': 0})
            yearly_costs = defaultdict(lambda: {'hours': 0, 'cost': 0})
            total_cost = 0
            total_hours = 0
            
            overtime_data = []
            
            for row in overtime_results:
                employee = row[0]
                reason = row[1]
                date_start = row[2]
                date_end = row[3]
                hours = row[4] if row[4] else 0
                status = row[5]
                
                # Determina se è weekend (sabato=5, domenica=6)
                is_weekend = date_start.weekday() >= 5
                cost_per_hour = weekend_cost if is_weekend else weekday_cost
                cost = hours * cost_per_hour
                
                # Aggrega per mese e anno
                month_key = date_start.strftime('%Y-%m')
                year_key = date_start.strftime('%Y')
                
                monthly_costs[month_key]['hours'] += hours
                monthly_costs[month_key]['cost'] += cost
                yearly_costs[year_key]['hours'] += hours
                yearly_costs[year_key]['cost'] += cost
                
                total_hours += hours
                total_cost += cost
                
                overtime_data.append({
                    'employee': employee,
                    'reason': reason,
                    'date': date_start.strftime('%d/%m/%Y %H:%M'),
                    'date_obj': date_start,  # Per ordinamento
                    'month_key': month_key,
                    'hours': hours,
                    'status': status,
                    'is_weekend': is_weekend,
                    'cost': cost
                })
            
            # Ordina per data
            overtime_data.sort(key=lambda x: x['date_obj'])
            
            # Crea directory C:\Temp se non esiste
            output_dir = r"C:\Temp"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Genera nome file automatico basato sulle date
            filename = f"report_overtime_from_{start_date.strftime('%d-%m-%Y')}_to_{end_date.strftime('%d-%m-%Y')}.pdf"
            file_path = os.path.join(output_dir, filename)
            
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)
            
            # Logo aziendale (in alto a destra)
            logo_path = "Logo.png"
            if os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.5 * cm, height=1.5 * cm)
                    logo.drawOn(c, width - 2.5 * cm, height - 2.5 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Titolo
            c.setFont("Helvetica-Bold", 18)
            c.drawString(2 * cm, height - 2 * cm, "RAPPORTO STRAORDINARI")
            
            c.setFont("Helvetica", 10)
            c.drawString(2 * cm, height - 2.5 * cm, 
                f"Periodo: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
            c.drawString(2 * cm, height - 3 * cm, 
                f"Data generazione: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            y_pos = height - 4 * cm
            
            # === TABELLA RIEPILOGO COSTI PER MESE ===
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y_pos, "RIEPILOGO COSTI PER MESE")
            y_pos -= 0.5 * cm
            
            monthly_table_data = [['Mese', 'Ore', f'Costo ({currency})']]
            for month in sorted(monthly_costs.keys()):
                month_name = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
                monthly_table_data.append([
                    month_name,
                    f"{monthly_costs[month]['hours']:.1f}",
                    f"{monthly_costs[month]['cost']:.2f}"
                ])
            
            monthly_table = Table(monthly_table_data, colWidths=[4*cm, 2*cm, 3*cm])
            monthly_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E5090")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            monthly_table.wrapOn(c, width, height)
            monthly_table_height = monthly_table._height
            monthly_table.drawOn(c, 2 * cm, y_pos - monthly_table_height)
            y_pos -= (monthly_table_height + 0.8 * cm)
            
            # === TABELLA RIEPILOGO COSTI PER ANNO ===
            c.setFont("Helvetica-Bold", 12)
            c.drawString(11 * cm, height - 4 * cm, "RIEPILOGO COSTI PER ANNO")
            
            yearly_table_data = [['Anno', 'Ore', f'Costo ({currency})']]
            for year in sorted(yearly_costs.keys()):
                yearly_table_data.append([
                    year,
                    f"{yearly_costs[year]['hours']:.1f}",
                    f"{yearly_costs[year]['cost']:.2f}"
                ])
            
            # Aggiungi riga totale
            yearly_table_data.append([
                'TOTALE',
                f"{total_hours:.1f}",
                f"{total_cost:.2f}"
            ])
            
            yearly_table = Table(yearly_table_data, colWidths=[3*cm, 2*cm, 3*cm])
            yearly_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E5090")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                # Evidenzia riga totale
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#FFD700")),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            
            yearly_table.wrapOn(c, width, height)
            yearly_table.drawOn(c, 11 * cm, height - 4 * cm - 0.5 * cm - yearly_table._height)
            
            # === TABELLA DETTAGLIO STRAORDINARI ===
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y_pos, "DETTAGLIO STRAORDINARI")
            y_pos -= 0.5 * cm
            
            detail_table_data = [['Dipendente', 'Motivo', 'Data', 'Ore', 'Tipo', 'Stato', f'Costo ({currency})']]
            
            # Raggruppa per mese e aggiungi subtotali
            current_month = None
            month_hours = 0
            month_cost = 0
            subtotal_rows = []  # Traccia le righe di subtotale per lo styling
            month_header_rows = []  # Traccia le righe di intestazione mese
            
            for item in overtime_data:
                item_month = item['month_key']
                
                # Se cambia il mese, aggiungi subtotale del mese precedente
                if current_month is not None and item_month != current_month:
                    month_name = datetime.strptime(current_month, '%Y-%m').strftime('%B %Y')
                    subtotal_rows.append(len(detail_table_data))
                    detail_table_data.append([
                        f'Subtotale {month_name}', '', '', 
                        f'{month_hours:.1f}', '', '', 
                        f'{month_cost:.2f}'
                    ])
                    month_hours = 0
                    month_cost = 0
                
                # Se è un nuovo mese, aggiungi intestazione mese
                if item_month != current_month:
                    month_name = datetime.strptime(item_month, '%Y-%m').strftime('%B %Y')
                    month_header_rows.append(len(detail_table_data))
                    detail_table_data.append([
                        month_name.upper(), '', '', '', '', '', ''
                    ])
                    current_month = item_month
                
                # Aggiungi riga dettaglio
                detail_table_data.append([
                    item['employee'],
                    item['reason'],
                    item['date'],
                    f"{item['hours']:.1f}",
                    'Weekend' if item['is_weekend'] else 'Weekday',
                    item['status'],
                    f"{item['cost']:.2f}"
                ])
                
                month_hours += item['hours']
                month_cost += item['cost']
            
            # Aggiungi subtotale dell'ultimo mese
            if current_month is not None:
                month_name = datetime.strptime(current_month, '%Y-%m').strftime('%B %Y')
                subtotal_rows.append(len(detail_table_data))
                detail_table_data.append([
                    f'Subtotale {month_name}', '', '', 
                    f'{month_hours:.1f}', '', '', 
                    f'{month_cost:.2f}'
                ])
            
            # Aggiungi riga GRAN TOTALE
            grand_total_row = len(detail_table_data)
            detail_table_data.append([
                'GRAN TOTALE', '', '', 
                f'{total_hours:.1f}', '', '', 
                f'{total_cost:.2f}'
            ])
            
            detail_table = Table(detail_table_data, colWidths=[4*cm, 3.5*cm, 3*cm, 1.5*cm, 2*cm, 2*cm, 2.5*cm])
            
            # Stile base
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
            ]
            
            # Stile per intestazioni mese
            for row_idx in month_header_rows:
                table_style.extend([
                    ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#2E5090")),
                    ('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.whitesmoke),
                    ('FONTNAME', (0, row_idx), (-1, row_idx), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, row_idx), (-1, row_idx), 9),
                    ('SPAN', (0, row_idx), (-1, row_idx)),  # Unisci tutte le colonne
                ])
            
            # Stile per subtotali mensili
            for row_idx in subtotal_rows:
                table_style.extend([
                    ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#E0E0E0")),
                    ('FONTNAME', (0, row_idx), (-1, row_idx), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, row_idx), (-1, row_idx), 8),
                ])
            
            # Stile per gran totale
            table_style.extend([
                ('BACKGROUND', (0, grand_total_row), (-1, grand_total_row), colors.HexColor("#FFD700")),
                ('FONTNAME', (0, grand_total_row), (-1, grand_total_row), 'Helvetica-Bold'),
                ('FONTSIZE', (0, grand_total_row), (-1, grand_total_row), 9),
            ])
            
            detail_table.setStyle(TableStyle(table_style))

            
            detail_table.wrapOn(c, width, height)
            detail_table_height = detail_table._height
            detail_table.drawOn(c, 2 * cm, y_pos - detail_table_height)
            
            # Footer
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.5 * cm, 
                "Document automatically generated by TraceabilityRS system")
            c.setFont("Helvetica", 7)
            c.drawString(2 * cm, 1 * cm, 
                f"Tariffe applicate: Weekday={weekday_cost:.2f} {currency}/h | Weekend={weekend_cost:.2f} {currency}/h")
            
            c.save()
            
            # Chiedi se aprire il file
            open_file = messagebox.askyesno(
                self.lang.get('success', 'Successo'),
                f"File PDF salvato con successo:\n{file_path}\n\nVuoi aprire il file?",
                parent=self
            )
            
            if open_file:
                os.startfile(file_path)
            
        except Exception as e:
            logger.error(f"Errore export PDF: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore export PDF:\n{str(e)}",
                parent=self
            )

