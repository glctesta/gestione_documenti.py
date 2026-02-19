"""
Overtime Manager - Business Logic
Gestione logica business per straordinari
"""

import logging
from datetime import datetime, date
from typing import List, Dict, Tuple, Optional
import os
import tempfile

logger = logging.getLogger(__name__)


class OvertimeManager:
    """
    Gestisce la logica business per le richieste di straordinario.
    """
    
    def __init__(self, db_handler):
        """
        Inizializza il manager.
        
        Args:
            db_handler: Istanza di DatabaseHandler
        """
        self.db = db_handler
    
    # ==================== METODI DIPENDENTI ====================
    
    def fetch_eligible_employees(self, month=None, year=None):
        """
        Recupera dipendenti eligibili per straordinario (non hanno superato ore massime).
        
        Args:
            month: Mese di riferimento (default: mese corrente)
            year: Anno di riferimento (default: anno corrente)
            
        Returns:
            List di dipendenti con (EmployeeHireHistoryId, Nome, Cognome, OreMensili)
        """
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year
        
        # Calcola primo e ultimo giorno del mese
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)
        
        query = """
        SELECT 
            h.EmployeeHireHistoryId,
            e.EmployeeSurname,
            e.EmployeeName,
            ISNULL(SUM(DATEDIFF(HOUR, s.DateStart, s.DateEnd)), 0) AS MonthlyHours
        FROM Employee.dbo.Employees e
        INNER JOIN Employee.dbo.EmployeeHireHistory h 
            ON e.EmployeeId = h.EmployeeId
        LEFT JOIN ResetServices.dbo.ExtraTimeApprovalStory s 
            ON h.EmployeeHireHistoryId = s.IdEmployee
            AND s.DateStart >= ? 
            AND s.DateStart < ?
        WHERE h.EndWorkDate IS NULL
            AND h.EmployeerId = 2
            AND NOT e.employeeName ='ANONYMOUS'
        GROUP BY h.EmployeeHireHistoryId, e.EmployeeSurname, e.EmployeeName
        HAVING ISNULL(SUM(DATEDIFF(HOUR, s.DateStart, s.DateEnd)), 0) < 
            (SELECT MaxHourPerMonth FROM Employee.dbo.OverTimeRules WHERE DateOut IS NULL)
        ORDER BY e.EmployeeSurname, e.EmployeeName
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query, (first_day, last_day))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Errore recupero dipendenti eligibili: {e}", exc_info=True)
            return []
    
    def get_employee_monthly_hours(self, employee_id, month=None, year=None):
        """
        Calcola le ore di straordinario già effettuate da un dipendente nel mese.
        
        Args:
            employee_id: ID dipendente (EmployeeHireHistoryId)
            month: Mese di riferimento
            year: Anno di riferimento
            
        Returns:
            int: Ore totali nel mese
        """
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year
        
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)
        
        query = """
        SELECT ISNULL(SUM(DATEDIFF(HOUR, DateStart, DateEnd)), 0) AS TotalHours
        FROM ResetServices.dbo.ExtraTimeApprovalStory
        WHERE IdEmployee = ?
            AND DateStart >= ?
            AND DateStart < ?
        """
        
        try:
            result = self.db.fetch_one(query, (employee_id, first_day, last_day))
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Errore calcolo ore mensili: {e}", exc_info=True)
            return 0
    
    # ==================== METODI MOTIVI ====================
    
    def fetch_overtime_reasons(self):
        """
        Recupera tutti i motivi di straordinario ordinati.
        
        Returns:
            List di motivi con (IdMotivo, OverTime_Reason, ObbgligoOrdine, Justify)
        """
        query = """
        SELECT IdMotivo, OverTime_Reason, ObbgligoOrdine, Justify, MaxIterazioniMese
        FROM ResetServices.dbo.OverTime_Reason
        ORDER BY Ordine
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Errore recupero motivi straordinario: {e}", exc_info=True)
            return []
    
    # ==================== METODI ORDINI ====================
    
    def fetch_recent_orders(self):
        """
        Recupera ordini recenti per associazione a straordinario.
        
        Returns:
            List di ordini con (IdOrdine, PO, QtaStory)
        """
        query = """
        SELECT o.IDOrder as IdOrdine, o.OrderNumber as PO, o.OrderQuantity as QtaStory
        FROM traceability_rs.dbo.orders o
        inner join traceability_rs.dbo.products p on o.idproduct=p.IDProduct
        WHERE 
            o.OrderDate > DATEADD(DAY, -100, GETDATE())  -- Ultimi 100 giorni        
        ORDER BY o.OrderDate DESC
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Errore recupero ordini recenti: {e}", exc_info=True)
            return []
    
    # ==================== VALIDAZIONI ====================
    
    def validate_overtime_request(self, employee_id, start_datetime, end_datetime, reason_id):
        """
        Valida una richiesta di straordinario.
        
        Args:
            employee_id: ID dipendente
            start_datetime: Data/ora inizio
            end_datetime: Data/ora fine
            reason_id: ID motivo
            
        Returns:
            Tuple (is_valid: bool, error_message: str)
        """
        # Validazione 1: Data fine >= Data inizio
        if end_datetime <= start_datetime:
            return False, "Data/ora fine deve essere successiva a data/ora inizio"
        
        # Validazione 2: Ore massime mensili
        hours_requested = (end_datetime - start_datetime).total_seconds() / 3600
        current_hours = self.get_employee_monthly_hours(
            employee_id, 
            start_datetime.month, 
            start_datetime.year
        )
        
        max_hours_query = "SELECT MaxHoursPerMonth FROM ResetServices.dbo.OvertimeRules WHERE DateOut IS NULL"
        max_hours_result = self.db.fetch_one(max_hours_query)
        max_hours = max_hours_result[0] if max_hours_result else 32
        
        if current_hours + hours_requested > max_hours:
            return False, f"Superamento ore massime mensili ({max_hours}h). Ore attuali: {current_hours}h, richieste: {hours_requested}h"
        
        # Validazione 3: Verifica sovrapposizioni
        overlap_query = """
        SELECT COUNT(*) 
        FROM ResetServices.dbo.ExtraTimeApprovalStory
        WHERE IdEmployee = ?
            AND (
                (DateStart <= ? AND DateEnd > ?)
                OR (DateStart < ? AND DateEnd >= ?)
                OR (DateStart >= ? AND DateEnd <= ?)
            )
        """
        overlap_result = self.db.fetch_one(
            overlap_query, 
            (employee_id, start_datetime, start_datetime, end_datetime, end_datetime, start_datetime, end_datetime)
        )
        
        if overlap_result and overlap_result[0] > 0:
            return False, "Esiste già una richiesta di straordinario per questo dipendente in questo periodo"
        
        return True, ""
    
    # ==================== CREAZIONE RICHIESTE ====================
    
    def create_overtime_request(self, supervisor_id, supervisor_name, employees_data, orders_data=None):
        """
        Crea una nuova richiesta di straordinario.
        
        Args:
            supervisor_id: ID supervisore richiedente
            supervisor_name: Nome supervisore
            employees_data: Lista di dict con dati dipendenti
                [{
                    'employee_id': int,
                    'reason_id': int,
                    'reason_text': str,
                    'start': datetime,
                    'end': datetime,
                    'justify': str,
                    'order_id': int (optional),
                    'qty_target': int (optional)
                }]
            orders_data: Lista di dict con ordini associati (optional)
                [{'order_id': int, 'quantity': int}]
                
        Returns:
            Tuple (success: bool, request_id: int, request_number: str, error_msg: str)
        """
        try:
            # 1. Chiama SP Registro per ottenere numero richiesta
            registro_query = """
            EXEC ResetServices.dbo.Registro 
                @tipo=190, 
                @anno=?, 
                @data=?, 
                @operatore=?, 
                @obj=?, 
                @chichiama=0
            """
            
            first_order_id = orders_data[0]['order_id'] if orders_data and len(orders_data) > 0 else 0
            
            cursor = self.db.conn.cursor()
            cursor.execute(
                registro_query,
                (datetime.now().year, datetime.now().strftime('%Y-%m-%d'), supervisor_id, first_order_id)
            )
            registro_result = cursor.fetchone()
            registro_id = registro_result[0]
            request_number = registro_result[1]
            
            # 2. Inserisci in ExtraTimeApproval (usa OUTPUT per recuperare ID)
            approval_query = """
            SET NOCOUNT ON;
            DECLARE @InsertedId TABLE (Id INT);
            INSERT INTO ResetServices.dbo.ExtraTimeApproval (IdChief, IdRegistro, DateSys)
            OUTPUT INSERTED.ExtraHourApprovalId INTO @InsertedId
            VALUES (?, ?, GETDATE());
            SELECT Id FROM @InsertedId;
            """
            cursor.execute(approval_query, (supervisor_id, registro_id))
            
            # Recupera ID generato
            result = cursor.fetchone()
            
            if result is None or result[0] is None:
                raise Exception("Impossibile recuperare ID della richiesta creata. Verifica la struttura della tabella ExtraTimeApproval.")
            
            approval_id = int(result[0])
            logger.info(f"ExtraTimeApproval creato con ID: {approval_id}")
            
            # 3. Inserisci dipendenti in ExtraTimeApprovalStory (usa struttura esistente)
            story_query = """
            INSERT INTO ResetServices.dbo.ExtraTimeApprovalStory 
            (ExtraHourApprovalId, IdEmployee, Descriptionreasons, DateStart, DateEnd, 
             SuperVisorId, Justify, IdOrder, QtyTarget, DateSys)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
            """
            
            for emp in employees_data:
                cursor.execute(story_query, (
                    approval_id,
                    emp['employee_id'],
                    emp['reason_text'],
                    emp['start'],
                    emp['end'],
                    supervisor_id,
                    emp.get('justify', 'N/A'),
                    emp.get('order_id'),
                    emp.get('qty_target')
                ))
            
            # 4. Inserisci ordini associati (se presenti) - usa struttura esistente
            if orders_data and len(orders_data) > 0:
                orders_query = """
                INSERT INTO ResetServices.dbo.ExtraTimeOrders 
                (IdOrder, NoQuantityToAchieve, ExtraHourApprovalId, DateSys)
                VALUES (?, ?, ?, GETDATE())
                """
                for order in orders_data:
                    cursor.execute(orders_query, (
                        order['order_id'],
                        order['quantity'],
                        approval_id
                    ))
            
            self.db.conn.commit()
            cursor.close()
            
            logger.info(f"Richiesta straordinario creata: ID={approval_id}, Numero={request_number}")
            return True, approval_id, request_number, ""
            
        except Exception as e:
            self.db.conn.rollback()
            error_msg = f"Errore creazione richiesta: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, None, None, error_msg
    
    # ==================== GENERAZIONE PDF ====================
    
    def generate_overtime_pdf(self, request_id, request_number, supervisor_name, employees_data, orders_data=None):
        """
        Genera PDF accordo straordinari in inglese.
        
        Args:
            request_id: ID richiesta
            request_number: Numero richiesta
            supervisor_name: Nome supervisore
            employees_data: Dati dipendenti (deve includere 'employee_id' per calcolare ore)
            orders_data: Dati ordini (optional)
            
        Returns:
            str: Path del PDF generato, None se errore
        """
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.platypus import Image as ReportLabImage, Table, TableStyle, Paragraph
            from reportlab.lib import colors
            from reportlab.lib.styles import ParagraphStyle
            
            # Recupera numero richiesta formattato da TbRegistro
            request_number_query = """
            SELECT r.NumRegistro + ' on ' + FORMAT(r.datareg, 'd', 'ro-ro') AS RequestNumber
            FROM ResetServices.dbo.TbRegistro r 
            INNER JOIN ResetServices.dbo.ExtraTimeApproval e ON r.Contatore = e.IdRegistro
            WHERE e.ExtraHourApprovalId = ?
            """
            
            result = self.db.fetch_one(request_number_query, (request_id,))
            formatted_request_number = result[0] if result else request_number
            
            # Crea file temporaneo
            temp_file = tempfile.NamedTemporaryFile(
                prefix=f"OverTimeRequest_{formatted_request_number.replace(' ', '_').replace('/', '-')}_",
                suffix=".pdf",
                delete=False,
                dir="C:\\Temp"
            )
            file_path = temp_file.name
            temp_file.close()
            
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            
            # Helper per testo
            def draw_text(y, text, size=10, bold=False):
                font = "Helvetica-Bold" if bold else "Helvetica"
                c.setFont(font, size)
                c.drawString(2 * cm, y, text)
            
            def resolve_logo_path():
                base_dir = os.path.dirname(os.path.dirname(__file__))
                for candidate in (
                    os.path.join(base_dir, "Logo.png"),
                    os.path.join(base_dir, "logo.png"),
                    "Logo.png",
                    "logo.png",
                ):
                    if os.path.exists(candidate):
                        return candidate
                return None

            # Logo aziendale
            logo_path = resolve_logo_path()
            if logo_path and os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.8 * cm, height=1.8 * cm)
                    logo.drawOn(c, width - 3.0 * cm, height - 2.4 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Header professionale
            c.setFillColor(colors.HexColor("#1F3A5F"))
            c.rect(0, height - 3 * cm, width, 3 * cm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(2 * cm, height - 1.8 * cm, "OVERTIME AGREEMENT")
            c.setFont("Helvetica", 8.5)
            c.drawString(2 * cm, height - 2.35 * cm, f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.setFillColor(colors.black)
            
            y_pos = height - 4.0 * cm
            
            # Dettagli richiesta in riquadro con wrapping
            c.setFillColor(colors.HexColor("#F3F6FB"))
            c.setStrokeColor(colors.HexColor("#C5D1E0"))
            c.roundRect(1.8 * cm, y_pos - 2.2 * cm, width - 3.6 * cm, 2.0 * cm, 6, stroke=1, fill=1)
            c.setFillColor(colors.HexColor("#1F3A5F"))
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2.2 * cm, y_pos - 0.65 * cm, "REQUEST DETAILS")
            detail_style = ParagraphStyle(
                name='overtime_detail_style',
                fontName='Helvetica',
                fontSize=9,
                leading=10.8,
                wordWrap='CJK'
            )
            req_line = Paragraph(f"<b>Request Number:</b> {formatted_request_number}", detail_style)
            req_line.wrapOn(c, width - 4.4 * cm, 0.5 * cm)
            req_line.drawOn(c, 2.2 * cm, y_pos - 1.3 * cm)
            by_line = Paragraph(f"<b>Requested by:</b> {supervisor_name}", detail_style)
            by_line.wrapOn(c, width - 4.4 * cm, 0.5 * cm)
            by_line.drawOn(c, 2.2 * cm, y_pos - 1.8 * cm)
            y_pos -= 2.8 * cm
            
            # Disclaimer box
            c.setStrokeColor(colors.red)
            c.setLineWidth(2)
            c.rect(2 * cm, y_pos - 1.5 * cm, width - 4 * cm, 1.2 * cm)
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.red)
            c.drawCentredString(width / 2, y_pos - 0.6 * cm, "IMPORTANT NOTICE")
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.black)
            notice_style = ParagraphStyle(
                name='overtime_notice_style',
                fontName='Helvetica',
                fontSize=8,
                leading=9.2,
                alignment=1,
                wordWrap='CJK'
            )
            notice = Paragraph(
                "This is a REQUEST. Overtime work cannot be performed until explicitly approved.",
                notice_style
            )
            notice_width = width - 4.6 * cm
            _, notice_height = notice.wrap(notice_width, 0.8 * cm)
            notice.drawOn(c, 2.3 * cm, y_pos - 0.8 * cm - notice_height)
            y_pos -= 2 * cm
            
            # Tabella dipendenti con ore già effettuate
            draw_text(y_pos, "EMPLOYEES INVOLVED", 14, True)
            y_pos -= 0.8 * cm
            
            # Header con word-wrap reale tramite Paragraph
            cell_style = ParagraphStyle(
                name='overtime_cell_style',
                fontName='Helvetica',
                fontSize=7,
                leading=8.2,
                alignment=1,
                wordWrap='CJK'
            )
            table_data = [[
                Paragraph('Employee', cell_style),
                Paragraph('Start Date/Time', cell_style),
                Paragraph('End Date/Time', cell_style),
                Paragraph('Hours', cell_style),
                Paragraph('Current Month Hrs', cell_style),
                Paragraph('Reason', cell_style),
                Paragraph('Order (Target Qty)', cell_style)
            ]]

            for emp in employees_data:
                hours = (emp['end'] - emp['start']).total_seconds() / 3600
                
                # Recupera ore già effettuate nel mese
                employee_id = emp.get('employee_id')
                current_hours = 0
                if employee_id:
                    current_hours = self.get_employee_monthly_hours(
                        employee_id,
                        emp['start'].month,
                        emp['start'].year
                    )
                
                # Formatta ordine se presente
                order_info = 'N/A'
                if emp.get('order_id') and emp.get('order_number'):
                    qty = emp.get('qty_target', 0)
                    order_info = f"{emp['order_number']} ({qty} pcs)"
                
                table_data.append([
                    Paragraph(str(emp.get('name', '')), cell_style),
                    Paragraph(emp['start'].strftime('%d/%m/%Y %H:%M'), cell_style),
                    Paragraph(emp['end'].strftime('%d/%m/%Y %H:%M'), cell_style),
                    Paragraph(f"{hours:.1f}", cell_style),
                    Paragraph(f"{current_hours:.1f}", cell_style),
                    Paragraph(str(emp.get('reason', '')), cell_style),
                    Paragraph(order_info, cell_style)
                ])
            
            # Tabella con larghezze adattate
            table = Table(table_data, colWidths=[3.0*cm, 2.4*cm, 2.4*cm, 1.3*cm, 1.8*cm, 3.8*cm, 2.6*cm], repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.6, colors.HexColor("#A9B9CF")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBFD")]),
            ]))
            
            table.wrapOn(c, width, height)
            table_height = table._height
            table.drawOn(c, 1.4 * cm, y_pos - table_height)
            y_pos -= (table_height + 1 * cm)
            
            # Footer in inglese
            c.setStrokeColor(colors.HexColor("#D7DFEB"))
            c.line(1.5 * cm, 2.1 * cm, width - 1.5 * cm, 2.1 * cm)
            c.setFillColor(colors.HexColor("#4D5E73"))
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.6 * cm, 
                "Document automatically generated by TraceabilityRS system")
            
            c.save()
            logger.info(f"PDF generated: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            return None
    
    def generate_approval_confirmation_pdf(self, request_id, approver_name):
        """
        Genera PDF di conferma approvazione con RequestNumber e ApprovalNumber.
        
        Args:
            request_id: ID richiesta
            approver_name: Nome di chi ha approvato
            
        Returns:
            str: Path del PDF generato, None se errore
        """
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.platypus import Image as ReportLabImage, Table, TableStyle, Paragraph
            from reportlab.lib import colors
            from reportlab.lib.styles import ParagraphStyle
            
            # Recupera numeri richiesta e approvazione da TbRegistro
            numbers_query = """
            SELECT DISTINCT r.NumRegistro + ' on ' + FORMAT(r.datareg, 'd', 'ro-ro') AS RequestNumber,
                   r1.NumRegistro + ' on ' + FORMAT(r1.datareg, 'd', 'ro-ro') AS ApprovalNumber
            FROM ResetServices.dbo.TbRegistro r 
            INNER JOIN ResetServices.dbo.ExtraTimeApproval e ON r.Contatore = e.IdRegistro
            INNER JOIN ResetServices.dbo.ExtraTimeApprovalStory es ON es.ExtraHourApprovalId = e.ExtraHourApprovalId
            INNER JOIN ResetServices.dbo.TbRegistro r1 ON r1.Contatore = es.ApprovedId
            WHERE e.ExtraHourApprovalId = ?
            """
            
            result = self.db.fetch_one(numbers_query, (request_id,))
            if not result:
                logger.error(f"Could not retrieve numbers for request_id: {request_id}")
                return None
            
            request_number, approval_number = result[0], result[1]

            # Recupera dettaglio dipendenti/ore autorizzate e ordini collegati
            employees_query = """
            SELECT
                e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName,
                s.DateStart,
                s.DateEnd,
                CAST(DATEDIFF(MINUTE, s.DateStart, s.DateEnd) / 60.0 AS DECIMAL(10,2)) AS AuthorizedHours,
                s.IdOrder,
                o.OrderNumber,
                s.QtyTarget
            FROM ResetServices.dbo.ExtraTimeApprovalStory s
            INNER JOIN Employee.dbo.EmployeeHireHistory h
                ON s.IdEmployee = h.EmployeeHireHistoryId
            INNER JOIN Employee.dbo.Employees e
                ON h.EmployeeId = e.EmployeeId
            LEFT JOIN traceability_rs.dbo.orders o
                ON o.IDOrder = s.IdOrder
            WHERE s.ExtraHourApprovalId = ?
            ORDER BY e.EmployeeSurname, e.EmployeeName, s.DateStart
            """
            cursor = self.db.conn.cursor()
            cursor.execute(employees_query, (request_id,))
            employee_rows = cursor.fetchall()
            cursor.close()
            
            # Crea file temporaneo
            temp_file = tempfile.NamedTemporaryFile(
                prefix=f"ApprovalConfirmation_{approval_number.replace(' ', '_').replace('/', '-')}_",
                suffix=".pdf",
                delete=False,
                dir="C:\\Temp"
            )
            file_path = temp_file.name
            temp_file.close()
            
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            
            # Helper per testo
            def draw_text(y, text, size=10, bold=False):
                font = "Helvetica-Bold" if bold else "Helvetica"
                c.setFont(font, size)
                c.drawString(2 * cm, y, text)
            
            def resolve_logo_path():
                base_dir = os.path.dirname(os.path.dirname(__file__))
                for candidate in (
                    os.path.join(base_dir, "Logo.png"),
                    os.path.join(base_dir, "logo.png"),
                    "Logo.png",
                    "logo.png",
                ):
                    if os.path.exists(candidate):
                        return candidate
                return None

            # Logo aziendale
            logo_path = resolve_logo_path()
            if logo_path and os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.8 * cm, height=1.8 * cm)
                    logo.drawOn(c, width - 3.0 * cm, height - 2.4 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Header
            c.setFillColor(colors.HexColor("#1F3A5F"))
            c.rect(0, height - 3 * cm, width, 3 * cm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(2 * cm, height - 1.8 * cm, "OVERTIME APPROVAL CONFIRMATION")
            c.setFont("Helvetica", 8.5)
            c.drawString(2 * cm, height - 2.35 * cm, f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.setFillColor(colors.black)
            
            y_pos = height - 4.0 * cm
            
            # Box di conferma verde
            c.setFillColor(colors.HexColor("#28A745"))
            c.setStrokeColor(colors.HexColor("#28A745"))
            c.setLineWidth(2)
            c.rect(2 * cm, y_pos - 2 * cm, width - 4 * cm, 1.5 * cm, fill=0)
            
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, y_pos - 0.8 * cm, "APPROVED")
            c.setFont("Helvetica", 10)
            
            y_pos -= 2.5 * cm
            
            # Dettagli con tabella (word-wrap sicuro)
            draw_text(y_pos, "APPROVAL DETAILS", 14, True)
            y_pos -= 0.8 * cm

            details_style = ParagraphStyle(
                name='approval_details_style',
                fontName='Helvetica',
                fontSize=9,
                leading=11,
                wordWrap='CJK'
            )

            details_data = [
                [Paragraph('<b>Request Number</b>', details_style), Paragraph(str(request_number), details_style)],
                [Paragraph('<b>Approval Number</b>', details_style), Paragraph(str(approval_number), details_style)],
                [Paragraph('<b>Approved by</b>', details_style), Paragraph(str(approver_name), details_style)],
                [Paragraph('<b>Approval Date</b>', details_style), Paragraph(datetime.now().strftime('%d/%m/%Y %H:%M'), details_style)],
            ]

            details_table = Table(details_data, colWidths=[5.0 * cm, width - 9.0 * cm])
            details_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#A9B9CF')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9FBFD')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            details_table.wrapOn(c, width, height)
            details_table.drawOn(c, 2 * cm, y_pos - details_table._height)

            y_pos = y_pos - details_table._height - 0.9 * cm

            # Sezione dipendenti/ore autorizzate + ordini (se presenti)
            c.setFillColor(colors.HexColor("#1F3A5F"))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y_pos, "AUTHORIZED EMPLOYEES")
            y_pos -= 0.6 * cm

            employee_cell_style = ParagraphStyle(
                name='approval_employee_cell_style',
                fontName='Helvetica',
                fontSize=8,
                leading=9.4,
                alignment=1,
                wordWrap='CJK'
            )

            has_orders = any((row[4] is not None) or (row[5] is not None) for row in employee_rows)

            if has_orders:
                employee_table_data = [[
                    Paragraph("Employee", employee_cell_style),
                    Paragraph("Time Window", employee_cell_style),
                    Paragraph("Authorized Hours", employee_cell_style),
                    Paragraph("Order / Target Qty", employee_cell_style),
                ]]
            else:
                employee_table_data = [[
                    Paragraph("Employee", employee_cell_style),
                    Paragraph("Time Window", employee_cell_style),
                    Paragraph("Authorized Hours", employee_cell_style),
                ]]

            for row in employee_rows:
                employee_name = row[0] or "N/A"
                date_start = row[1]
                date_end = row[2]
                authorized_hours = row[3] if row[3] is not None else 0
                order_number = row[5]
                qty_target = row[6]

                time_window = "N/A"
                if date_start and date_end:
                    time_window = f"{date_start.strftime('%d/%m/%Y %H:%M')} - {date_end.strftime('%d/%m/%Y %H:%M')}"

                if has_orders:
                    if order_number:
                        order_info = f"{order_number} / {int(qty_target) if qty_target is not None else 0}"
                    else:
                        order_info = "N/A"
                    employee_table_data.append([
                        Paragraph(str(employee_name), employee_cell_style),
                        Paragraph(time_window, employee_cell_style),
                        Paragraph(f"{float(authorized_hours):.2f}", employee_cell_style),
                        Paragraph(order_info, employee_cell_style),
                    ])
                else:
                    employee_table_data.append([
                        Paragraph(str(employee_name), employee_cell_style),
                        Paragraph(time_window, employee_cell_style),
                        Paragraph(f"{float(authorized_hours):.2f}", employee_cell_style),
                    ])

            if has_orders:
                employee_col_widths = [5.0 * cm, 4.0 * cm, 2.8 * cm, width - 2 * cm - 2 * cm - 5.0 * cm - 4.0 * cm - 2.8 * cm]
            else:
                employee_col_widths = [5.5 * cm, 5.0 * cm, width - 2 * cm - 2 * cm - 5.5 * cm - 5.0 * cm]

            employee_table = Table(employee_table_data, colWidths=employee_col_widths, repeatRows=1)
            employee_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#A9B9CF')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FBFD')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            employee_table.wrapOn(c, width, height)

            # Evita overflow verticale
            if y_pos - employee_table._height < 2.5 * cm:
                c.showPage()
                c.setFillColor(colors.HexColor("#1F3A5F"))
                c.rect(0, height - 2.5 * cm, width, 2.5 * cm, stroke=0, fill=1)
                c.setFillColor(colors.white)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(2 * cm, height - 1.6 * cm, "OVERTIME APPROVAL CONFIRMATION - DETAILS")
                c.setFillColor(colors.black)
                y_pos = height - 3.2 * cm

            employee_table.drawOn(c, 2 * cm, y_pos - employee_table._height)
            
            # Footer uniforme al report richiesta
            c.setStrokeColor(colors.HexColor("#D7DFEB"))
            c.line(1.5 * cm, 2.1 * cm, width - 1.5 * cm, 2.1 * cm)
            c.setFillColor(colors.HexColor("#4D5E73"))
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.6 * cm, 
                "Document automatically generated by TraceabilityRS system")
            
            c.save()
            logger.info(f"Approval confirmation PDF generated: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating approval PDF: {e}", exc_info=True)
            return None

    def generate_approval_excel(self, request_id):
        """
        Genera un file Excel con il dettaglio dei dipendenti autorizzati allo
        straordinario: nome, data, ore autorizzate e totale ore già effettuate
        nel mese corrente da ciascun dipendente.

        Args:
            request_id: ID richiesta (ExtraHourApprovalId)

        Returns:
            str: Path del file Excel generato, None in caso di errore
        """
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter

            # ── Query dati dipendenti della richiesta ──────────────────────
            query = """
            SELECT
                h.EmployeeHireHistoryId,
                e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName,
                s.DateStart,
                s.DateEnd,
                CAST(DATEDIFF(MINUTE, s.DateStart, s.DateEnd) / 60.0 AS DECIMAL(10,2)) AS AuthorizedHours
            FROM ResetServices.dbo.ExtraTimeApprovalStory s
            INNER JOIN Employee.dbo.EmployeeHireHistory h
                ON s.IdEmployee = h.EmployeeHireHistoryId
            INNER JOIN Employee.dbo.Employees e
                ON h.EmployeeId = e.EmployeeId
            WHERE s.ExtraHourApprovalId = ?
            ORDER BY e.EmployeeSurname, e.EmployeeName, s.DateStart
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (request_id,))
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                logger.warning(f"generate_approval_excel: no employees found for request_id={request_id}")
                return None

            # ── Stili ─────────────────────────────────────────────────────
            header_fill   = PatternFill(start_color="1F3A5F", end_color="1F3A5F", fill_type="solid")
            header_font   = Font(bold=True, color="FFFFFF", size=10)
            alt_fill      = PatternFill(start_color="F0F4FA", end_color="F0F4FA", fill_type="solid")
            center_align  = Alignment(horizontal="center", vertical="center")
            left_align    = Alignment(horizontal="left",   vertical="center")
            thin_border   = Border(
                left=Side(style="thin", color="A9B9CF"),
                right=Side(style="thin", color="A9B9CF"),
                top=Side(style="thin", color="A9B9CF"),
                bottom=Side(style="thin", color="A9B9CF")
            )

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Overtime Approved"

            # ── Intestazione colonne ──────────────────────────────────────
            headers = [
                "Employee",
                "Date",
                "Start Time",
                "End Time",
                "Authorized Hours",
                "Monthly Hours (already done)",
            ]
            col_widths = [32, 14, 12, 12, 18, 28]

            for col_idx, (header, width) in enumerate(zip(headers, col_widths), start=1):
                cell = ws.cell(row=1, column=col_idx, value=header)
                cell.font      = header_font
                cell.fill      = header_fill
                cell.alignment = center_align
                cell.border    = thin_border
                ws.column_dimensions[get_column_letter(col_idx)].width = width

            ws.row_dimensions[1].height = 20

            # ── Righe dati ────────────────────────────────────────────────
            for row_idx, row in enumerate(rows, start=2):
                hire_id        = row[0]
                emp_name       = row[1]
                date_start     = row[2]   # datetime
                date_end       = row[3]   # datetime
                auth_hours     = float(row[4]) if row[4] is not None else 0.0

                # Ore mensili già effettuate (mese del giorno di straordinario)
                ref_month = date_start.month if date_start else datetime.now().month
                ref_year  = date_start.year  if date_start else datetime.now().year
                monthly_hours = self.get_employee_monthly_hours(hire_id, ref_month, ref_year)

                fill = alt_fill if row_idx % 2 == 0 else None

                def _cell(col, value, align=center_align):
                    c = ws.cell(row=row_idx, column=col, value=value)
                    c.border    = thin_border
                    c.alignment = align
                    if fill:
                        c.fill = fill
                    return c

                _cell(1, emp_name,    align=left_align)
                _cell(2, date_start.strftime("%d/%m/%Y")    if date_start else "N/A")
                _cell(3, date_start.strftime("%H:%M")       if date_start else "N/A")
                _cell(4, date_end.strftime("%H:%M")         if date_end   else "N/A")
                _cell(5, round(auth_hours, 2))
                _cell(6, round(float(monthly_hours), 2))

            # ── Totale ────────────────────────────────────────────────────
            total_row = len(rows) + 2
            total_font = Font(bold=True, size=10)
            for col in range(1, 7):
                c = ws.cell(row=total_row, column=col)
                c.border    = thin_border
                c.font      = total_font
                c.fill      = PatternFill(start_color="D7DFEB", end_color="D7DFEB", fill_type="solid")
                c.alignment = center_align
            ws.cell(row=total_row, column=1, value="TOTAL").alignment = left_align
            ws.cell(row=total_row, column=5,
                    value=f"=SUM(E2:E{total_row - 1})")
            ws.cell(row=total_row, column=6).value = ""

            # ── Salva file temporaneo ─────────────────────────────────────
            temp_file = tempfile.NamedTemporaryFile(
                prefix=f"OvertimeApproval_{request_id}_",
                suffix=".xlsx",
                delete=False,
                dir="C:\\Temp"
            )
            file_path = temp_file.name
            temp_file.close()
            wb.save(file_path)

            logger.info(f"Approval Excel generated: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Error generating approval Excel: {e}", exc_info=True)
            return None

    # ==================== EMAIL ====================

    
    def send_overtime_notification(self, request_number, supervisor_name, employees_count, pdf_path):
        """
        Invia email di notifica ai responsabili.
        
        Args:
            request_number: Numero richiesta
            supervisor_name: Nome supervisore
            employees_count: Numero dipendenti coinvolti
            pdf_path: Path del PDF da allegare
            
        Returns:
            bool: True se invio riuscito
        """
        try:
            # Recupera destinatari da Settings
            recipients_str = self.db.fetch_setting('overtime_request')
            if not recipients_str:
                logger.error("No recipients configured for overtime_request in Settings")
                return False
            
            # Converti stringa in lista (separati da virgola o punto e virgola)
            recipients = [r.strip() for r in recipients_str.replace(';', ',').split(',') if r.strip()]
            
            if not recipients:
                logger.error("No valid recipients found in overtime_request setting")
                return False
            
            # Prepara email in inglese con HTML
            subject = f"Overtime Request Pending Approval - {request_number}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #2E5090;">Overtime Request Notification</h2>
                <p>Dear Manager,</p>
                <p>A new overtime request has been submitted and requires your approval.</p>
                <table style="border-collapse: collapse; margin: 20px 0;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold; width: 180px;">Request Number:</td>
                        <td style="padding: 8px;">{request_number}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Requested by:</td>
                        <td style="padding: 8px;">{supervisor_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Employees Involved:</td>
                        <td style="padding: 8px;">{employees_count}</td>
                    </tr>
                </table>
                <p style="background-color: #FFF3CD; border-left: 4px solid #FFC107; padding: 12px; margin: 20px 0;">
                    <strong>⚠️ Action Required:</strong> Please review and approve/reject this request via:<br>
                    <strong>ERP → Operations → Personnel → Overtime → Authorization</strong>
                </p>
                <p>The overtime agreement document signed by the employees is attached to this email.</p>
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>TraceabilityRS System</strong>
                </p>
            </body>
            </html>
            """
            
            # Importa funzione send_email da utils
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from utils import send_email
            
            # Invia email con allegato
            send_email(
                recipients=recipients,
                subject=subject,
                body=body,
                is_html=True,
                attachments=[pdf_path] if pdf_path and os.path.exists(pdf_path) else None
            )
            
            logger.info(f"Email sent successfully to: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}", exc_info=True)
            return False
    
    def send_approval_notification(self, request_id, request_number, requester_id, approved, approver_name, extra_attachments=None, attachment_path=None):
        """
        Invia email di notifica approvazione/rifiuto al richiedente.

        Args:
            request_id: ID richiesta
            request_number: Numero richiesta (non usato, recuperato da DB)
            requester_id: ID richiedente (EmployeeHireHistoryId)
            approved: True se approvata, False se rifiutata
            approver_name: Nome di chi ha approvato/rifiutato
            extra_attachments: Lista di path file da allegare (PDF + Excel, opzionale)
            attachment_path: (deprecato) singolo path allegato per compatibilità

        Returns:
            bool: True se invio riuscito
        """
        try:
            # Recupera email richiedente
            email_query = """
            SELECT DISTINCT e.employeename + ' '+ e.employeesurname as Employee,  
                    ea.WorkEmail AS Email
            FROM  Employee.dbo.EmployeeHireHistory h
            LEFT JOIN Employee.dbo.Employees e 
                ON e.EmployeeId = h.EmployeeId and h.employeerid =2 and h.EndWorkDate is null
            LEFT JOIN Employee.dbo.EmployeeAddress ea
                ON ea.EmployeeId = e.EmployeeId
               AND ea.DateOut IS NULL
            WHERE h.EmployeeHireHistoryId = ?
            """
            
            result = self.db.fetch_one(email_query, (requester_id,))
            
            if not result or not result[1]:
                logger.error(f"No email found for requester ID: {requester_id}")
                return False
            
            requester_name = result[0]
            requester_email = result[1]
            
            # Recupera numeri formattati da TbRegistro
            if approved:
                # Se approvato, recupera sia RequestNumber che ApprovalNumber
                numbers_query = """
                SELECT DISTINCT r.NumRegistro + ' on ' + FORMAT(r.datareg, 'd', 'ro-ro') AS RequestNumber,
                       r1.NumRegistro + ' on ' + FORMAT(r1.datareg, 'd', 'ro-ro') AS ApprovalNumber
                FROM ResetServices.dbo.TbRegistro r 
                INNER JOIN ResetServices.dbo.ExtraTimeApproval e ON r.Contatore = e.IdRegistro
                INNER JOIN ResetServices.dbo.ExtraTimeApprovalStory es ON es.ExtraHourApprovalId = e.ExtraHourApprovalId
                INNER JOIN ResetServices.dbo.TbRegistro r1 ON r1.Contatore = es.ApprovedId
                WHERE e.ExtraHourApprovalId = ?
                """
                numbers_result = self.db.fetch_one(numbers_query, (request_id,))
                formatted_request_number = numbers_result[0] if numbers_result else request_number
                formatted_approval_number = numbers_result[1] if numbers_result else "N/A"
            else:
                # Se rifiutato, recupera solo RequestNumber
                request_query = """
                SELECT r.NumRegistro + ' on ' + FORMAT(r.datareg, 'd', 'ro-ro') AS RequestNumber
                FROM ResetServices.dbo.TbRegistro r 
                INNER JOIN ResetServices.dbo.ExtraTimeApproval e ON r.Contatore = e.IdRegistro
                WHERE e.ExtraHourApprovalId = ?
                """
                request_result = self.db.fetch_one(request_query, (request_id,))
                formatted_request_number = request_result[0] if request_result else request_number
                formatted_approval_number = None
            
            # Prepara email
            status = "APPROVED" if approved else "REJECTED"
            status_color = "#28A745" if approved else "#DC3545"
            
            subject = f"Overtime Request {status} - {formatted_request_number}"
            
            # Costruisci tabella dettagli
            details_rows = f"""
                <tr>
                    <td style="padding: 8px; font-weight: bold; width: 180px;">Request Number:</td>
                    <td style="padding: 8px;">{formatted_request_number}</td>
                </tr>
            """
            
            if approved and formatted_approval_number:
                details_rows += f"""
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Approval Number:</td>
                    <td style="padding: 8px;">{formatted_approval_number}</td>
                </tr>
                """
            
            details_rows += f"""
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                    <td style="padding: 8px; color: {status_color}; font-weight: bold;">{status}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Reviewed by:</td>
                    <td style="padding: 8px;">{approver_name}</td>
                </tr>
            """
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: {status_color};">Overtime Request {status}</h2>
                <p>Dear {requester_name},</p>
                <p>Your overtime request has been <strong style="color: {status_color};">{status}</strong>.</p>
                <table style="border-collapse: collapse; margin: 20px 0;">
                    {details_rows}
                </table>
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>TraceabilityRS System</strong>
                </p>
            </body>
            </html>
            """
            
            # Importa funzione send_email da utils
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from utils import send_email
            
            attachments = []
            # Supporto per extra_attachments (nuovo) e attachment_path (legacy)
            if extra_attachments:
                attachments.extend([p for p in extra_attachments if p and os.path.exists(p)])
            elif attachment_path and os.path.exists(attachment_path):
                attachments.append(attachment_path)
            if not attachments:
                attachments = None

            # Recupera indirizzi CC da Settings
            cc_emails = None
            try:
                cc_result = self.db.fetch_one(
                    "SELECT [Value] FROM traceability_rs.dbo.Settings WHERE Atribute = 'Sys_email_Overtami_responce'"
                )
                if cc_result and cc_result[0]:
                    cc_emails = [e.strip() for e in cc_result[0].replace(';', ',').split(',') if e.strip()]
                    logger.info(f"Approval notification CC: {cc_emails}")
                else:
                    logger.warning("Sys_email_Overtami_responce not configured in Settings – sending without CC")
            except Exception as _cc_exc:
                logger.warning(f"Could not read CC setting: {_cc_exc}")

            # Invia email: TO = richiedente, CC = indirizzi da Settings
            send_email(
                recipients=[requester_email],
                subject=subject,
                body=body,
                is_html=True,
                attachments=attachments,
                cc_emails=cc_emails
            )

            logger.info(f"Approval notification sent to: {requester_email} | CC: {cc_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending approval notification: {e}", exc_info=True)
            return False
    
    def send_weekly_overtime_analysis_email(self):
        """
        Invia email settimanale con analisi straordinari non autorizzati.
        Da chiamare ogni lunedì per il periodo della settimana precedente.
        
        Returns:
            bool: True se email inviata con successo
        """
        try:
            from datetime import timedelta
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment
            
            # Calcola date settimana precedente (lunedì-domenica)
            today = date.today()
            days_since_monday = today.weekday()  # 0 = Monday
            last_monday = today - timedelta(days=days_since_monday + 7)
            last_sunday = last_monday + timedelta(days=6)
            
            logger.info(f"Generating weekly overtime analysis for period: {last_monday} to {last_sunday}")
            
            # Query analisi con filtro OVER APPROVED
            query = """
            DECLARE @dateStart DATE = ?;
            DECLARE @DateStop DATE = ?;
            DECLARE @Filter AS NVARCHAR(30) = 'OVER APPROVED';

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
            WHERE Notes LIKE @Filter
            ORDER BY OvertimeDate, Name;
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(query, (last_monday, last_sunday))
            results = cursor.fetchall()
            cursor.close()
            
            if not results:
                logger.info("No unauthorized overtime found for last week. Email not sent.")
                return True
            
            # Crea Excel
            output_dir = tempfile.gettempdir()
            filename = f"Unauthorized_Overtime_{last_monday.strftime('%Y%m%d')}_{last_sunday.strftime('%Y%m%d')}.xlsx"
            file_path = os.path.join(output_dir, filename)
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Unauthorized Overtime"
            
            # Header
            headers = ['Nr', 'Employee', 'Date', 'Min Presence', 'Min Approved', 'Notes']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Dati
            for row_idx, row in enumerate(results, 2):
                ws.cell(row=row_idx, column=1, value=row[0]).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=2, value=row[1])
                ws.cell(row=row_idx, column=3, value=row[2].strftime('%d/%m/%Y') if row[2] else 'N/D').alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=4, value=row[3]).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=5, value=row[5]).alignment = Alignment(horizontal='center')
                ws.cell(row=row_idx, column=6, value=row[6])
                
                # Evidenzia in rosso
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
            
            # Recupera destinatari
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT AttributeValue 
                FROM Traceability_RS.dbo.Settings 
                WHERE AttributeName = 'Sys_email_overtime_issues'
            """)
            result = cursor.fetchone()
            cursor.close()
            
            if not result or not result[0]:
                logger.warning("No email recipients configured in Settings.Sys_email_overtime_issues")
                return False
            
            recipients = [email.strip() for email in result[0].split(',')]
            
            # Prepara email
            subject = f"⚠️ Unauthorized Overtime Report - Week {last_monday.strftime('%d/%m/%Y')} to {last_sunday.strftime('%d/%m/%Y')}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #C00000;">⚠️ Unauthorized Overtime Alert</h2>
                <p>Dear Team,</p>
                <p>The attached report summarizes <strong style="color: #C00000;">{len(results)} unauthorized overtime entries</strong> 
                for the period <strong>{last_monday.strftime('%d/%m/%Y')} to {last_sunday.strftime('%d/%m/%Y')}</strong>.</p>
                
                <p>These entries indicate cases where the actual overtime presence exceeded the approved overtime hours.</p>
                
                <p style="margin-top: 20px;">
                    <strong>Action Required:</strong><br>
                    Please review the attached Excel file and take appropriate action.
                </p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>TraceabilityRS System</strong>
                </p>
            </body>
            </html>
            """
            
            # Importa funzione send_email
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from utils import send_email
            
            # Invia email con allegato
            send_email(
                recipients=recipients,
                subject=subject,
                body=body,
                is_html=True,
                attachments=[file_path]
            )
            
            logger.info(f"Weekly overtime analysis email sent to: {recipients}")
            
            # Rimuovi file temporaneo
            try:
                os.remove(file_path)
            except:
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending weekly overtime analysis email: {e}", exc_info=True)
            return False
