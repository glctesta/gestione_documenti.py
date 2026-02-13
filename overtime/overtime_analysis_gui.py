"""
Overtime Analysis GUI
Form per analisi straordinari con confronto presenza/approvazione
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from tkcalendar import DateEntry
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def open_overtime_analysis_window(parent, db_handler, lang_manager, user_name):
    """
    Apre la finestra per analisi straordinari.
    
    Args:
        parent: Finestra parent
        db_handler: DatabaseHandler instance
        lang_manager: LanguageManager instance
        user_name: Nome utente loggato
    """
    OvertimeAnalysisWindow(parent, db_handler, lang_manager, user_name)


class OvertimeAnalysisWindow(tk.Toplevel):
    """
    Finestra per analisi straordinari con export PDF/Excel.
    """
    
    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        self.analysis_data = []
        self.sort_column = None
        self.sort_reverse = False
        
        # Setup finestra
        self.title(self.lang.get('overtime_analysis_title', 'Analisi Straordinari'))
        self.geometry("1400x700")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        # Imposta date default (mese corrente)
        today = date.today()
        first_day = date(today.year, today.month, 1)
        self.start_date.set_date(first_day)
        self.end_date.set_date(today)
    
    def _create_widgets(self):
        """Crea i widget dell'interfaccia."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === FILTRI ===
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding="10")
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Date
        ttk.Label(filter_frame, text=self.lang.get('from', 'Da:')).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.start_date.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filter_frame, text=self.lang.get('to', 'A:')).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.end_date = DateEntry(
            filter_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.end_date.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Filtro tipo
        ttk.Label(filter_frame, text=self.lang.get('filter_type', 'Tipo Filtro:')).grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.filter_type_var = tk.StringVar(value='ALL')
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type_var,
            values=['ALL', 'OVER APPROVED', 'Time approved = time presence'],
            state='readonly',
            width=30
        )
        filter_combo.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Pulsante genera
        ttk.Button(
            filter_frame,
            text=self.lang.get('generate_analysis', 'Genera Analisi'),
            command=self._generate_analysis
        ).grid(row=0, column=6, padx=5, pady=5)
        
        # === RISULTATI ===
        results_frame = ttk.LabelFrame(main_frame, text=self.lang.get('results', 'Risultati'), padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview
        columns = ('nr', 'name', 'date', 'min_done', 'min_approved', 'notes')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=20)
        
        # Intestazioni cliccabili per ordinamento
        self.tree.heading('nr', text='Nr', command=lambda: self._sort_by_column('nr'))
        self.tree.heading('name', text=self.lang.get('employee', 'Dipendente'), command=lambda: self._sort_by_column('name'))
        self.tree.heading('date', text=self.lang.get('date', 'Data'), command=lambda: self._sort_by_column('date'))
        self.tree.heading('min_done', text=self.lang.get('min_done', 'Min Presenza'), command=lambda: self._sort_by_column('min_done'))
        self.tree.heading('min_approved', text=self.lang.get('min_approved', 'Min Approvati'), command=lambda: self._sort_by_column('min_approved'))
        self.tree.heading('notes', text=self.lang.get('notes', 'Note'), command=lambda: self._sort_by_column('notes'))
        
        self.tree.column('nr', width=50, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.W)
        self.tree.column('date', width=100, anchor=tk.CENTER)
        self.tree.column('min_done', width=120, anchor=tk.CENTER)
        self.tree.column('min_approved', width=120, anchor=tk.CENTER)
        self.tree.column('notes', width=250, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
    
    def _generate_analysis(self):
        """Genera l'analisi in base ai filtri selezionati."""
        # Pulisci risultati precedenti
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.analysis_data = []
        
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        filter_type = self.filter_type_var.get()
        
        # Converti filtro per query
        filter_param = None if filter_type == 'ALL' else filter_type
        
        # Query di analisi
        query = """
        DECLARE @dateStart DATE = ?;
        DECLARE @DateStop DATE = ?;
        DECLARE @Filter AS NVARCHAR(30) = ?;

        WITH
        CTE_DailyState_Employee AS (
            SELECT 
                ds.IDDailyState,
                ds.DailyStateDate,
                e.IDEmployee,
                UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Name, 
                e.UniqueID
            FROM Timeclocking.dbo.DailyState ds
            INNER JOIN Timeclocking.dbo.Employee e
                ON e.IDEmployee = ds.IDEmployee AND ds.DailyStateDate BETWEEN @dateStart AND @DateStop
        ),
        CTE_Done AS (
            SELECT
                fd.IDDailyState,
                fd.NoMin AS MinSuplimentarDone,
                r.RequestName
            FROM Timeclocking.dbo.EmployeeRequestFractionalDay fd
            INNER JOIN Timeclocking.dbo.RequestType r
                ON r.IDRequestType = fd.IDRequestType
            WHERE r.IDRequestType = 8
        ),
        CTE_HireHistory AS (
            SELECT
                h.EmployeeHireHistoryId AS EmployeeHireId,
                ee.EmployeeNID COLLATE DATABASE_DEFAULT AS UniqueID
            FROM employee.dbo.employees ee
            INNER JOIN employee.dbo.employeehirehistory h
                ON ee.EmployeeId = h.EmployeeId
                AND h.employeerid = 2
                AND h.EndWorkDate IS NULL
        ),
        CTE_ExtraTimeApprovalStory AS (
            SELECT
                es.IdEmployee AS EmployeeHireHistoryId,
                CAST(es.DateStart AS DATE) AS DateStart,
                ISNULL(DATEDIFF(MINUTE, es.DateStart, es.DateEnd), 0) AS MinExtraTimeApproved
            FROM [ResetServices].[dbo].ExtraTimeApprovalStory es
            WHERE CAST(es.DateStart AS DATE) BETWEEN @dateStart AND @dateStop
        ),
        CTE_Combined AS (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY dse.DailyStateDate, dse.Name) AS Nr,
                dse.Name,
                dse.DailyStateDate AS OvertimeDate,
                req.MinSuplimentarDone,
                req.RequestName,
                ISNULL(eta.MinExtraTimeApproved, 0) AS MinExtraTimeApproved,
                CASE
                    WHEN ISNULL(req.MinSuplimentarDone, 0) > ISNULL(eta.MinExtraTimeApproved, 0) THEN
                        'OVER APPROVED'
                    ELSE
                        'Time approved = time presence'
                END AS Notes
            FROM CTE_DailyState_Employee dse
            INNER JOIN CTE_Done req ON dse.IDDailyState = req.IDDailyState
            INNER JOIN CTE_HireHistory hh ON dse.UniqueID COLLATE DATABASE_DEFAULT = hh.UniqueID
            LEFT JOIN CTE_ExtraTimeApprovalStory eta ON hh.EmployeeHireId = eta.EmployeeHireHistoryId
                AND eta.DateStart = dse.DailyStateDate
        )
        SELECT DISTINCT *
        FROM CTE_Combined
        WHERE Notes LIKE ISNULL(@Filter, Notes)
        ORDER BY OvertimeDate, Name;
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query, (start_date, end_date, filter_param))
            results = cursor.fetchall()
            cursor.close()
            
            # Popola tabella e salva dati
            for row in results:
                nr = row[0]
                name = row[1]
                overtime_date = row[2].strftime('%d/%m/%Y') if row[2] else 'N/D'
                min_done = row[3] if row[3] else 0
                min_approved = row[5] if row[5] else 0
                notes = row[6]
                
                # Colora righe OVER APPROVED in rosso
                tag = 'over_approved' if notes == 'OVER APPROVED' else ''
                
                self.tree.insert('', tk.END, values=(
                    nr, name, overtime_date, min_done, min_approved, notes
                ), tags=(tag,))
                
                self.analysis_data.append({
                    'nr': nr,
                    'name': name,
                    'date': overtime_date,
                    'min_done': min_done,
                    'min_approved': min_approved,
                    'notes': notes
                })
            
            # Configura tag per evidenziare
            self.tree.tag_configure('over_approved', background='#FFE0E0')
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                f"Analisi completata: {len(results)} record trovati",
                parent=self
            )
            
        except Exception as e:
            logger.error(f"Errore generazione analisi: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore generazione analisi:\n{str(e)}",
                parent=self
            )
    
    def _sort_by_column(self, col):
        """
        Ordina i dati della tabella in base alla colonna selezionata.
        
        Args:
            col: Nome della colonna da ordinare
        """
        if not self.analysis_data:
            return
        
        # Determina direzione ordinamento
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # Mappa colonne ai campi dati
        col_map = {
            'nr': 'nr',
            'name': 'name',
            'date': 'date',
            'min_done': 'min_done',
            'min_approved': 'min_approved',
            'notes': 'notes'
        }
        
        sort_key = col_map.get(col, 'nr')
        
        # Funzione di ordinamento personalizzata per gestire date
        def sort_func(item):
            value = item[sort_key]
            # Converti date in formato ordinabile
            if sort_key == 'date' and isinstance(value, str):
                try:
                    # Formato: DD/MM/YYYY
                    parts = value.split('/')
                    if len(parts) == 3:
                        return f"{parts[2]}{parts[1]}{parts[0]}"  # YYYYMMDD
                except:
                    pass
            # Gestisci valori numerici
            if sort_key in ['nr', 'min_done', 'min_approved']:
                try:
                    return int(value) if value else 0
                except:
                    return 0
            # Default: ordinamento stringa
            return str(value).lower() if value else ''
        
        # Ordina i dati
        self.analysis_data.sort(key=sort_func, reverse=self.sort_reverse)
        
        # Ricarica la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for item_data in self.analysis_data:
            tag = 'over_approved' if item_data['notes'] == 'OVER APPROVED' else ''
            self.tree.insert('', tk.END, values=(
                item_data['nr'],
                item_data['name'],
                item_data['date'],
                item_data['min_done'],
                item_data['min_approved'],
                item_data['notes']
            ), tags=(tag,))
        
        # Configura tag
        self.tree.tag_configure('over_approved', background='#FFE0E0')
        
        # Aggiorna intestazioni con indicatore ordinamento
        self._update_column_headers()
    
    def _update_column_headers(self):
        """Aggiorna le intestazioni delle colonne con indicatori di ordinamento."""
        headers = {
            'nr': 'Nr',
            'name': self.lang.get('employee', 'Dipendente'),
            'date': self.lang.get('date', 'Data'),
            'min_done': self.lang.get('min_done', 'Min Presenza'),
            'min_approved': self.lang.get('min_approved', 'Min Approvati'),
            'notes': self.lang.get('notes', 'Note')
        }
        
        for col, header_text in headers.items():
            if col == self.sort_column:
                # Aggiungi indicatore direzione
                indicator = ' ▼' if self.sort_reverse else ' ▲'
                self.tree.heading(col, text=header_text + indicator)
            else:
                self.tree.heading(col, text=header_text)
    
    def _export_to_excel(self):
        """Esporta i risultati in Excel."""
        if not self.analysis_data:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_data_to_export', 'Nessun dato da esportare'),
                parent=self
            )
            return
        
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment
            
            # Crea directory C:\Temp se non esiste
            output_dir = r"C:\Temp"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Nome file
            filter_type = self.filter_type_var.get().replace(' ', '_')
            filename = f"ReportAnalysis_Overtime_{filter_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = os.path.join(output_dir, filename)
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Overtime Analysis"
            
            # Header
            headers = ['Nr', 'Employee', 'Date', 'Min Presence', 'Min Approved', 'Notes']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="2E5090", end_color="2E5090", fill_type="solid")
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Dati
            for row_idx, item in enumerate(self.analysis_data, 2):
                ws.cell(row=row_idx, column=1, value=item['nr']).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=2, value=item['name'])
                ws.cell(row=row_idx, column=3, value=item['date']).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=4, value=item['min_done']).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=5, value=item['min_approved']).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=6, value=item['notes'])
                
                # Evidenzia OVER APPROVED in rosso
                if item['notes'] == 'OVER APPROVED':
                    for col in range(1, 7):
                        ws.cell(row=row_idx, column=col).fill = PatternFill(
                            start_color="FFE0E0", end_color="FFE0E0", fill_type="solid"
                        )
            
            # Adatta larghezza colonne
            ws.column_dimensions['A'].width = 8
            ws.column_dimensions['B'].width = 35
            ws.column_dimensions['C'].width = 12
            ws.column_dimensions['D'].width = 15
            ws.column_dimensions['E'].width = 15
            ws.column_dimensions['F'].width = 30
            
            wb.save(file_path)
            
            # Chiedi se aprire
            open_file = messagebox.askyesno(
                self.lang.get('success', 'Successo'),
                f"File Excel salvato:\n{file_path}\n\nVuoi aprire il file?",
                parent=self
            )
            
            if open_file:
                os.startfile(file_path)
            
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
        if not self.analysis_data:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_data_to_export', 'Nessun dato da esportare'),
                parent=self
            )
            return
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import cm
            from reportlab.platypus import Table, TableStyle, Image as ReportLabImage
            from reportlab.lib import colors
            
            # Crea directory C:\Temp se non esiste
            output_dir = r"C:\Temp"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Nome file
            filter_type = self.filter_type_var.get().replace(' ', '_')
            filename = f"ReportAnalysis_Overtime_{filter_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            file_path = os.path.join(output_dir, filename)
            
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)
            
            # Logo
            logo_path = "Logo.png"
            if os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.5 * cm, height=1.5 * cm)
                    logo.drawOn(c, width - 2.5 * cm, height - 2.5 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Titolo
            c.setFont("Helvetica-Bold", 18)
            c.drawString(2 * cm, height - 2 * cm, "OVERTIME ANALYSIS REPORT")
            
            c.setFont("Helvetica", 10)
            c.drawString(2 * cm, height - 2.5 * cm, 
                f"Period: {self.start_date.get_date().strftime('%d/%m/%Y')} - {self.end_date.get_date().strftime('%d/%m/%Y')}")
            c.drawString(2 * cm, height - 3 * cm, 
                f"Filter: {self.filter_type_var.get()}")
            c.drawString(2 * cm, height - 3.5 * cm, 
                f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            # Tabella
            table_data = [['Nr', 'Employee', 'Date', 'Min Presence', 'Min Approved', 'Notes']]
            over_approved_rows = []
            
            for idx, item in enumerate(self.analysis_data, 1):
                table_data.append([
                    item['nr'],
                    item['name'],
                    item['date'],
                    item['min_done'],
                    item['min_approved'],
                    item['notes']
                ])
                if item['notes'] == 'OVER APPROVED':
                    over_approved_rows.append(idx)
            
            table = Table(table_data, colWidths=[1.5*cm, 5*cm, 2.5*cm, 3*cm, 3*cm, 5*cm])
            
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E5090")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
            ]
            
            # Evidenzia righe OVER APPROVED
            for row_idx in over_approved_rows:
                table_style.append(
                    ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#FFE0E0"))
                )
            
            table.setStyle(TableStyle(table_style))
            
            table.wrapOn(c, width, height)
            table_height = table._height
            table.drawOn(c, 2 * cm, height - 5 * cm - table_height)
            
            # Footer
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.5 * cm, 
                "Document automatically generated by TraceabilityRS system")
            
            c.save()
            
            # Chiedi se aprire
            open_file = messagebox.askyesno(
                self.lang.get('success', 'Successo'),
                f"File PDF salvato:\n{file_path}\n\nVuoi aprire il file?",
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
