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
            from reportlab.platypus import Image as ReportLabImage, Table, TableStyle
            from reportlab.lib import colors
            
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
            
            # Logo aziendale (dimezzato: 1.5cm invece di 3cm)
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.5 * cm, height=1.5 * cm)
                    logo.drawOn(c, width - 2.5 * cm, height - 2.5 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Titolo in inglese
            draw_text(height - 2 * cm, "OVERTIME AGREEMENT", 18, True)
            draw_text(height - 2.5 * cm, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8)
            
            y_pos = height - 4 * cm
            
            # Dettagli richiesta in inglese
            draw_text(y_pos, "REQUEST DETAILS", 14, True)
            y_pos -= 0.8 * cm
            draw_text(y_pos, f"Request Number: {formatted_request_number}")
            y_pos -= 0.5 * cm
            draw_text(y_pos, f"Requested by: {supervisor_name}")
            y_pos -= 1 * cm
            
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
            c.drawCentredString(width / 2, y_pos - 1 * cm, 
                "This is a REQUEST. Overtime work cannot be performed until explicitly approved.")
            y_pos -= 2 * cm
            
            # Tabella dipendenti con ore già effettuate
            draw_text(y_pos, "EMPLOYEES INVOLVED", 14, True)
            y_pos -= 0.8 * cm
            
            # Header con colonna ore già effettuate e ordine
            table_data = [['Employee', 'Start Date/Time', 'End Date/Time', 'Hours', 'Current\nMonth Hrs', 'Reason', 'Order\n(Target Qty)']]
            
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
                    order_info = f"{emp['order_number']}\n({qty} pcs)"
                
                table_data.append([
                    emp['name'],
                    emp['start'].strftime('%d/%m/%Y\n%H:%M'),
                    emp['end'].strftime('%d/%m/%Y\n%H:%M'),
                    f"{hours:.1f}",
                    f"{current_hours:.1f}",
                    emp['reason'],
                    order_info
                ])
            
            # Tabella con larghezze adattate
            table = Table(table_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 1.2*cm, 1.5*cm, 3.5*cm, 2*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('WORDWRAP', (0, 0), (-1, -1), True),  # Abilita word wrap
            ]))
            
            table.wrapOn(c, width, height)
            table_height = table._height
            table.drawOn(c, 1.5 * cm, y_pos - table_height)
            y_pos -= (table_height + 1 * cm)
            
            # Footer in inglese
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.5 * cm, 
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
            from reportlab.platypus import Image as ReportLabImage
            from reportlab.lib import colors
            
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
            
            # Logo aziendale
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                try:
                    logo = ReportLabImage(logo_path, width=1.5 * cm, height=1.5 * cm)
                    logo.drawOn(c, width - 2.5 * cm, height - 2.5 * cm)
                except Exception as e:
                    logger.warning(f"Cannot load logo: {e}")
            
            # Titolo
            draw_text(height - 2 * cm, "OVERTIME APPROVAL CONFIRMATION", 18, True)
            draw_text(height - 2.5 * cm, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8)
            
            y_pos = height - 4 * cm
            
            # Box di conferma verde
            c.setFillColor(colors.HexColor("#28A745"))
            c.setStrokeColor(colors.HexColor("#28A745"))
            c.setLineWidth(2)
            c.rect(2 * cm, y_pos - 2 * cm, width - 4 * cm, 1.5 * cm, fill=0)
            
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, y_pos - 0.8 * cm, "✓ APPROVED")
            c.setFont("Helvetica", 10)
            
            y_pos -= 2.5 * cm
            
            # Dettagli
            draw_text(y_pos, "APPROVAL DETAILS", 14, True)
            y_pos -= 0.8 * cm
            draw_text(y_pos, f"Request Number: {request_number}")
            y_pos -= 0.5 * cm
            draw_text(y_pos, f"Approval Number: {approval_number}")
            y_pos -= 0.5 * cm
            draw_text(y_pos, f"Approved by: {approver_name}")
            y_pos -= 0.5 * cm
            draw_text(y_pos, f"Approval Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            # Footer
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 1.5 * cm, 
                "Document automatically generated by TraceabilityRS system")
            
            c.save()
            logger.info(f"Approval confirmation PDF generated: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating approval PDF: {e}", exc_info=True)
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
    
    def send_approval_notification(self, request_id, request_number, requester_id, approved, approver_name):
        """
        Invia email di notifica approvazione/rifiuto al richiedente.
        
        Args:
            request_id: ID richiesta
            request_number: Numero richiesta (non usato, recuperato da DB)
            requester_id: ID richiedente (EmployeeHireHistoryId)
            approved: True se approvata, False se rifiutata
            approver_name: Nome di chi ha approvato/rifiutato
            
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
            
            # Invia email
            send_email(
                recipients=[requester_email],
                subject=subject,
                body=body,
                is_html=True
            )
            
            logger.info(f"Approval notification sent to: {requester_email}")
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
