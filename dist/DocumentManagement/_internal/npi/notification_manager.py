# npi/notification_manager_v2.py - SEZIONI CORRETTE

import logging
import requests
import json
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, text

from email_connector import EmailSender
from .data_models import TaskProdotto, NotificationLog, ProgettoNPI, TaskCatalogo

logger = logging.getLogger(__name__)


class NotificationManagerV2:
    """
    Gestione completa notifiche NPI con supporto Employee database
    """

    def __init__(self, session: Session, email_sender: EmailSender,
                 teams_webhook_url: Optional[str] = None,
                 config_path: str = 'npi_notifications_config.json'):
        self.session = session
        self.email_sender = email_sender
        self.teams_webhook_url = teams_webhook_url
        
        # Carica configurazione
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> dict:
        """Carica configurazione da file JSON"""
        try:
            import json
            import os
            
            # Cerca il file nella directory corrente o nella directory npi
            if os.path.exists(config_path):
                path = config_path
            else:
                path = os.path.join(os.path.dirname(__file__), '..', config_path)
            
            if os.path.exists(path):
                with open(path, 'r') as f:
                    config = json.load(f)
                    logger.info(f"Configurazione caricata da {path}")
                    return config
            else:
                logger.warning(f"File configurazione non trovato: {config_path}, uso default")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Errore caricamento configurazione: {e}", exc_info=True)
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Configurazione di default"""
        return {
            "recipient_types": {
                "Interno": {"send_email": True},
                "Cliente": {"send_email": False},
                "Fornitore": {"send_email": False}
            },
            "notification_settings": {
                "enabled": True
            }
        }

    # ========================================
    # METODI HELPER PER RECUPERO DATI EMPLOYEE
    # ========================================

    def _get_employee_info(self, owner_id: int) -> Optional[Dict]:
        """
        Recupera informazioni employee da OwnerID (EmployeeHireHistoryId)

        Args:
            owner_id: EmployeeHireHistoryId del task owner

        Returns:
            Dict con {employee_hire_history_id, name, email} o None
        """
        try:
            query = text("""
                         SELECT s.EmployeeHireHistoryId,
                                e.EmployeeName + ' ' + e.EmployeeSurname AS FullName,
                                a.WorkEmail                              AS Email
                         FROM Employee.dbo.EmployeeHireHistory s
                                  INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = s.EmployeeId
                                  LEFT JOIN Employee.dbo.EmployeeAddress a ON a.EmployeeId = e.EmployeeId
                         WHERE s.EmployeeHireHistoryId = :owner_id
                         """)

            result = self.session.execute(query, {'owner_id': owner_id}).fetchone()

            if result:
                return {
                    'employee_hire_history_id': result[0],
                    'name': result[1],
                    'email': result[2]
                }

            logger.warning(f"Employee non trovato per OwnerID {owner_id}")
            return None

        except Exception as e:
            logger.error(f"Errore recupero employee info: {e}", exc_info=True)
            return None

    def _get_task_with_employee(self, task_prodotto_id: int) -> Optional[Tuple[TaskProdotto, Dict]]:
        """
        Recupera task con informazioni employee

        Returns:
            Tuple (TaskProdotto, employee_info_dict) o None
        """
        try:
            # Recupera task
            task = self.session.query(TaskProdotto).filter(
                TaskProdotto.TaskId == task_prodotto_id
            ).first()

            if not task:
                logger.error(f"Task {task_prodotto_id} non trovato")
                return None

            # Recupera info employee
            if not task.OwnerID:
                logger.warning(f"Task {task_prodotto_id} non ha OwnerID assegnato")
                return task, None

            employee_info = self._get_employee_info(task.OwnerID)

            return task, employee_info

        except Exception as e:
            logger.error(f"Errore recupero task con employee: {e}", exc_info=True)
            return None

    # ========================================
    # METODI HELPER PER CC E PDF
    # ========================================

    def _get_cc_emails_from_settings(self) -> List[str]:
        """
        Recupera lista email CC da tabella Settings
        
        Returns:
            Lista di indirizzi email da mettere in CC
        """
        try:
            query = text("""
                SELECT [Value]
                FROM [Traceability_RS].[dbo].[Settings]
                WHERE [Attribute] IN ('Sys_Email_late_npi_cc', ' Sys_Email_late_npi_cc')
            """)
            
            result = self.session.execute(query).fetchone()
            
            if result and result[0]:
                # Parse semicolon-separated emails
                emails = [email.strip() for email in result[0].split(';')]
                logger.debug(f"CC emails da settings: {emails}")
                return emails
            
            logger.warning("Nessun CC email trovato in Settings")
            return []
            
        except Exception as e:
            logger.error(f"Errore recupero CC emails: {e}", exc_info=True)
            return []

    def _get_project_owner_email(self, task_id: int) -> Optional[str]:
        """
        Recupera email del project owner per un task
        
        Args:
            task_id: ID del task
            
        Returns:
            Email del project owner o None
        """
        try:
            query = text("""
                SELECT DISTINCT
                    e.EmployeeName + ' ' + e.EmployeeSurname AS FullName,
                    a.WorkEmail AS Email
                FROM [Traceability_RS].[dbo].[TaskProdotto] tp
                INNER JOIN [Traceability_RS].[dbo].[WaveNPI] w ON tp.WaveID = w.WaveID
                INNER JOIN [Traceability_RS].[dbo].[ProgettiNPI] p ON w.ProgettoID = p.ProgettoID
                LEFT JOIN [Employee].[dbo].[EmployeeHireHistory] s ON p.OwnerID = s.EmployeeHireHistoryId
                LEFT JOIN [Employee].[dbo].[Employees] e ON e.EmployeeId = s.EmployeeId
                LEFT JOIN [Employee].[dbo].[EmployeeAddress] a ON a.EmployeeId = e.EmployeeId
                WHERE tp.TaskId = :task_id
            """)
            
            result = self.session.execute(query, {'task_id': task_id}).fetchone()
            
            if result and result[1]:
                logger.debug(f"Project owner per task {task_id}: {result[0]} ({result[1]})")
                return result[1]
            
            logger.warning(f"Project owner non trovato per task {task_id}")
            return None
            
        except Exception as e:
            logger.error(f"Errore recupero project owner: {e}", exc_info=True)
            return None
    
    def _get_notification_cc_emails(self, task_id: int) -> List[str]:
        """
        Recupera lista completa CC per notifiche NPI
        
        Combina:
        - Email da Settings (Sys_Email_late_npi_cc)
        - Email Project Owner (se disponibile)
        
        Args:
            task_id: ID del task
            
        Returns:
            Lista di email per CC (sempre almeno Settings, + Owner se presente)
        """
        cc_emails = []
        
        # 1. Recupera CC da Settings (sempre presenti)
        settings_emails = self._get_cc_emails_from_settings()
        if settings_emails:
            cc_emails.extend(settings_emails)
        
        # 2. Aggiungi Project Owner se disponibile
        project_owner_email = self._get_project_owner_email(task_id)
        if project_owner_email and project_owner_email not in cc_emails:
            cc_emails.append(project_owner_email)
            logger.debug(f"Aggiunto project owner in CC: {project_owner_email}")
        
        return cc_emails

    def _generate_dashboard_pdf(self, project_id: int) -> Optional[str]:
        """
        Genera PDF dashboard per un progetto
        
        Args:
            project_id: ID del progetto
            
        Returns:
            Path del file PDF generato o None
        """
        try:
            import tempfile
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            
            # Recupera dati progetto
            query = text("""
                SELECT 
                    p.NomeProgetto,
                    pr.CodiceProdotto,
                    p.ScadenzaProgetto,
                    e.EmployeeName + ' ' + e.EmployeeSurname AS ProjectOwner,
                    COUNT(DISTINCT tp.TaskProdottoID) AS TotalTasks,
                    SUM(CASE WHEN tp.Stato = 'Completato' THEN 1 ELSE 0 END) AS CompletedTasks,
                    SUM(CASE WHEN tp.DataFine < GETDATE() AND tp.Stato != 'Completato' THEN 1 ELSE 0 END) AS OverdueTasks
                FROM [Traceability_RS].[dbo].[ProgettiNPI] p
                LEFT JOIN [Traceability_RS].[dbo].[Prodotti] pr ON p.ProdottoID = pr.ProdottoID
                LEFT JOIN [Traceability_RS].[dbo].[WaveNPI] w ON p.ProgettoID = w.ProgettoID
                LEFT JOIN [Traceability_RS].[dbo].[TaskProdotto] tp ON w.WaveID = tp.WaveID
                LEFT JOIN [Employee].[dbo].[EmployeeHireHistory] s ON p.OwnerID = s.EmployeeHireHistoryId
                LEFT JOIN [Employee].[dbo].[Employees] e ON e.EmployeeId = s.EmployeeId
                WHERE p.ProgettoID = :project_id
                GROUP BY p.NomeProgetto, pr.CodiceProdotto, p.ScadenzaProgetto, 
                         e.EmployeeName, e.EmployeeSurname
            """)
            
            project_data = self.session.execute(query, {'project_id': project_id}).fetchone()
            
            if not project_data:
                logger.error(f"Progetto {project_id} non trovato")
                return None
            
            # Recupera task in ritardo
            overdue_query = text("""
                SELECT 
                    tc.NomeTask,
                    e.EmployeeName + ' ' + e.EmployeeSurname AS TaskOwner,
                    tp.DataFine,
                    DATEDIFF(DAY, tp.DataFine, GETDATE()) AS DaysOverdue
                FROM [Traceability_RS].[dbo].[TaskProdotto] tp
                INNER JOIN [Traceability_RS].[dbo].[TaskCatalogo] tc ON tp.TaskID = tc.TaskID
                INNER JOIN [Traceability_RS].[dbo].[WaveNPI] w ON tp.WaveID = w.WaveID
                LEFT JOIN [Employee].[dbo].[EmployeeHireHistory] s ON tp.OwnerID = s.EmployeeHireHistoryId
                LEFT JOIN [Employee].[dbo].[Employees] e ON e.EmployeeId = s.EmployeeId
                WHERE w.ProgettoID = :project_id
                  AND tp.DataFine < GETDATE()
                  AND tp.Stato != 'Completato'
                ORDER BY DaysOverdue DESC
            """)
            
            overdue_tasks = self.session.execute(overdue_query, {'project_id': project_id}).fetchall()
            
            # Crea PDF temporaneo
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_path = temp_file.name
            temp_file.close()
            
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Titolo
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#0066cc'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph(f"Dashboard Progetto NPI", title_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Informazioni progetto
            project_info = [
                ['Progetto:', project_data[0] or 'N/A'],
                ['Codice Prodotto:', project_data[1] or 'N/A'],
                ['Scadenza:', project_data[2].strftime('%d/%m/%Y') if project_data[2] else 'N/A'],
                ['Project Owner:', project_data[3] or 'N/A'],
                ['Task Totali:', str(project_data[4] or 0)],
                ['Task Completati:', str(project_data[5] or 0)],
                ['Task in Ritardo:', str(project_data[6] or 0)]
            ]
            
            info_table = Table(project_info, colWidths=[5*cm, 12*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(info_table)
            story.append(Spacer(1, 1*cm))
            
            # Task in ritardo
            if overdue_tasks:
                story.append(Paragraph("Task in Ritardo", styles['Heading2']))
                story.append(Spacer(1, 0.3*cm))
                
                task_data = [['Task', 'Responsabile', 'Scadenza', 'Giorni Ritardo']]
                for task in overdue_tasks:
                    task_data.append([
                        task[0] or 'N/A',
                        task[1] or 'Non assegnato',
                        task[2].strftime('%d/%m/%Y') if task[2] else 'N/A',
                        str(task[3])
                    ])
                
                task_table = Table(task_data, colWidths=[6*cm, 4*cm, 3*cm, 3*cm])
                task_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9534f')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                story.append(task_table)
            else:
                story.append(Paragraph("Nessun task in ritardo", styles['Normal']))
            
            # Genera PDF
            doc.build(story)
            logger.info(f"PDF dashboard generato: {pdf_path}")
            return pdf_path
            
        except ImportError:
            logger.error("reportlab non installato. Installare con: pip install reportlab")
            return None
        except Exception as e:
            logger.error(f"Errore generazione PDF dashboard: {e}", exc_info=True)
            return None

    # ========================================
    # METODI PRINCIPALI DI NOTIFICA - CORRETTI
    # ========================================

    def notify_task_assignment(self, task_prodotto_id: int,
                               assigned_by: Optional[str] = None) -> bool:
        """
        Notifica assegnazione task a responsabile
        """
        try:
            # Recupera task con employee info
            result = self._get_task_with_employee(task_prodotto_id)
            if not result:
                return False

            task, employee_info = result

            if not employee_info or not employee_info.get('email'):
                logger.warning(f"Task {task_prodotto_id}: email destinatario non disponibile")
                return False

            # Prepara messaggio
            subject = f"🎯 Nuovo Task Assegnato: {task.task_catalogo.NomeTask}"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #0066cc;">🎯 Nuovo Task Assegnato</h2>
                <p>Gentile <strong>{employee_info['name']}</strong>,</p>
                <p>Ti è stato assegnato un nuovo task nel progetto NPI:</p>

                <table border="1" cellpadding="10" style="border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #f0f0f0;">
                        <td><strong>Progetto:</strong></td>
                        <td>{task.wave.progetto.NomeProgetto}</td>
                    </tr>
                    <tr>
                        <td><strong>Task:</strong></td>
                        <td>{task.task_catalogo.NomeTask}</td>
                    </tr>
                    <tr>
                        <td><strong>Descrizione:</strong></td>
                        <td>{task.task_catalogo.Descrizione or 'N/A'}</td>
                    </tr>
                    <tr style="background-color: #fff3cd;">
                        <td><strong>Data Inizio:</strong></td>
                        <td>{task.DataInizio.strftime('%d/%m/%Y') if task.DataInizio else 'N/A'}</td>
                    </tr>
                    <tr style="background-color: #fff3cd;">
                        <td><strong>Data Scadenza:</strong></td>
                        <td>{task.DataFine.strftime('%d/%m/%Y') if task.DataFine else 'N/A'}</td>
                    </tr>
                    <tr>
                        <td><strong>Durata:</strong></td>
                        <td>{task.Durata} giorni</td>
                    </tr>
                </table>

                <p><strong>Note:</strong> {task.Note or 'Nessuna nota'}</p>

                <p style="margin-top: 30px;">
                    <em>Accedi al sistema per visualizzare i dettagli completi e aggiornare lo stato del task.</em>
                </p>

                <hr style="margin-top: 40px;">
                <p style="font-size: 0.9em; color: #666;">
                    Assegnato da: {assigned_by or 'Sistema'}<br>
                    Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </body>
            </html>
            """

            # Invia email
            email_sent = self._send_email_notification(
                recipient_email=employee_info['email'],
                recipient_name=employee_info['name'],
                subject=subject,
                body=body,
                task_prodotto_id=task_prodotto_id,
                employee_hire_history_id=employee_info['employee_hire_history_id'],
                reason='ASSIGNMENT'
            )

            # Invia Teams se configurato
            teams_sent = False
            if self.teams_webhook_url:
                teams_sent = self._send_teams_notification(
                    task=task,
                    employee_info=employee_info,
                    reason='ASSIGNMENT',
                    assigned_by=assigned_by
                )

            return email_sent or teams_sent

        except Exception as e:
            logger.error(f"Errore notifica assegnazione task {task_prodotto_id}: {e}", exc_info=True)
            return False

    def check_and_notify_overdue_tasks(self) -> Dict[str, int]:
        """
        Controlla task scaduti e invia notifiche
        """
        stats = {'notified': 0, 'failed': 0, 'skipped': 0}

        try:
            # Query task scaduti con JOIN Employee e Soggetto per tipo
            query = text("""
                         SELECT tp.TaskId,
                                tp.OwnerID,
                                e.EmployeeName + ' ' + e.EmployeeSurname AS FullName,
                                a.WorkEmail                              AS Email,
                                DATEDIFF(DAY, tp.DataFine, GETDATE())    AS GiorniRitardo,
                                ISNULL(sog.Tipo, 'Interno')              AS TipoSoggetto
                         FROM Traceability_rs.dbo.TaskProdotto tp
                                  LEFT JOIN Employee.dbo.EmployeeHireHistory s ON tp.OwnerID = s.EmployeeHireHistoryId
                                  LEFT JOIN Employee.dbo.Employees e ON e.EmployeeId = s.EmployeeId
                                  LEFT JOIN Employee.dbo.EmployeeAddress a ON a.EmployeeId = e.EmployeeId
                                  LEFT JOIN Traceability_rs.dbo.vw_Soggetti sog ON s.EmployeeHireHistoryId = sog.SoggettoId
                         WHERE tp.DataFine < GETDATE()
                           AND tp.Stato NOT IN ('Completato', 'Cancellato')
                           AND tp.PercentualeCompletamento < 100
                           AND tp.OwnerID IS NOT NULL
                         """)

            results = self.session.execute(query).fetchall()

            logger.info(f"🔍 Trovati {len(results)} task scaduti")

            for row in results:
                task_id = row[0]
                owner_id = row[1]
                full_name = row[2]
                email = row[3]
                giorni_ritardo = row[4]
                tipo_soggetto = row[5] if len(row) > 5 else 'Interno'
                
                # Verifica se il tipo di soggetto può ricevere email
                recipient_config = self.config.get('recipient_types', {}).get(tipo_soggetto, {'send_email': False})
                if not recipient_config.get('send_email', False):
                    logger.info(f"Task {task_id}: notifica saltata per tipo soggetto '{tipo_soggetto}' (config: send_email=false)")
                    stats['skipped'] += 1
                    continue

                # Controlla se già notificato oggi
                if self._was_notified_today(task_id, 'OVERDUE'):
                    stats['skipped'] += 1
                    continue

                if not email:
                    logger.warning(f"Task {task_id}: email non disponibile")
                    stats['skipped'] += 1
                    continue

                # Invia notifica
                if self._notify_overdue_task_direct(
                        task_id=task_id,
                        owner_id=owner_id,
                        full_name=full_name,
                        email=email,
                        giorni_ritardo=giorni_ritardo
                ):
                    stats['notified'] += 1
                else:
                    stats['failed'] += 1

            logger.info(f"📊 Notifiche ritardi: {stats['notified']} inviate, "
                        f"{stats['failed']} fallite, {stats['skipped']} saltate")

            return stats

        except Exception as e:
            logger.error(f"Errore controllo task scaduti: {e}", exc_info=True)
            return stats

    def _notify_overdue_task_direct(self, task_id: int, owner_id: int,
                                    full_name: str, email: str,
                                    giorni_ritardo: int) -> bool:
        """
        Notifica task scaduto con dati già recuperati
        """
        pdf_path = None
        try:
            # Recupera task per dettagli
            task = self.session.query(TaskProdotto).filter(
                TaskProdotto.TaskId == task_id
            ).first()

            if not task:
                return False
            
            # Recupera project ID per PDF
            project_id = task.wave.progetto.ProgettoId if task.wave and task.wave.progetto else None

            # Recupera CC emails (Settings + Project Owner)
            cc_emails = self._get_notification_cc_emails(task_id)
            
            # Genera PDF dashboard se abbiamo un project ID
            if project_id:
                pdf_path = self._generate_dashboard_pdf(project_id)
                if pdf_path:
                    logger.info(f"PDF dashboard generato per progetto {project_id}: {pdf_path}")
                else:
                    logger.warning(f"Impossibile generare PDF per progetto {project_id}")

            subject = f"⚠️ TASK IN RITARDO: {task.task_catalogo.NomeTask} ({giorni_ritardo} giorni)"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="cid:logo" alt="Company Logo" style="max-width: 200px; height: auto;">
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
                    <h2 style="color: #856404; margin: 0;">⚠️ Task in Ritardo</h2>
                </div>

                <p>Gentile <strong>{full_name}</strong>,</p>
                <p><strong style="color: #d9534f;">Il seguente task è scaduto da {giorni_ritardo} giorni:</strong></p>

                <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #f8d7da;">
                        <td style="width: 30%;"><strong>Progetto:</strong></td>
                        <td>{task.wave.progetto.NomeProgetto}</td>
                    </tr>
                    <tr>
                        <td><strong>Task:</strong></td>
                        <td>{task.task_catalogo.NomeTask}</td>
                    </tr>
                    <tr>
                        <td><strong>Data Scadenza:</strong></td>
                        <td>{task.DataFine.strftime('%d/%m/%Y') if task.DataFine else 'N/A'}</td>
                    </tr>
                    <tr style="background-color: #f8d7da;">
                        <td><strong>Giorni di Ritardo:</strong></td>
                        <td style="color: red; font-weight: bold; font-size: 1.2em;">{giorni_ritardo}</td>
                    </tr>
                    <tr>
                        <td><strong>Completamento:</strong></td>
                        <td>{task.PercentualeCompletamento}%</td>
                    </tr>
                    <tr>
                        <td><strong>Stato:</strong></td>
                        <td>{task.Stato}</td>
                    </tr>
                </table>

                <div style="background-color: #d1ecf1; padding: 15px; border-left: 5px solid #0c5460; margin: 20px 0;">
                    <p style="margin: 0;"><strong>⚡ Azione richiesta:</strong></p>
                    <ul style="margin: 10px 0;">
                        <li>Aggiorna lo stato del task nel sistema</li>
                        <li>Contatta il project manager se necessario ripianificare</li>
                        <li>Completa il task al più presto</li>
                    </ul>
                </div>

                <hr style="margin-top: 40px;">
                <p style="font-size: 0.9em; color: #666;">
                    Notifica automatica - Sistema NPI<br>
                    {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </body>
            </html>
            """
            
            # Prepara allegati (PDF + Logo)
            attachments = []
            if pdf_path:
                attachments.append(pdf_path)
            
            # Aggiungi logo come inline image
            import os
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Logo.png')
            if os.path.exists(logo_path):
                attachments.append(('inline', logo_path, 'logo'))


            return self._send_email_notification(
                recipient_email=email,
                recipient_name=full_name,
                subject=subject,
                body=body,
                task_prodotto_id=task_id,
                employee_hire_history_id=owner_id,
                reason='OVERDUE',
                cc_emails=cc_emails if cc_emails else None,
                attachments=attachments
            )

        except Exception as e:
            logger.error(f"Errore notifica ritardo task {task_id}: {e}", exc_info=True)
            return False
        finally:
            # Cleanup PDF temporaneo
            if pdf_path:
                try:
                    import os
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                        logger.debug(f"PDF temporaneo rimosso: {pdf_path}")
                except Exception as e:
                    logger.warning(f"Impossibile rimuovere PDF temporaneo {pdf_path}: {e}")

    def check_and_notify_upcoming_deadlines(self, days_before: int = 3) -> Dict[str, int]:
        """
        Notifica task in scadenza nei prossimi N giorni
        """
        stats = {'notified': 0, 'failed': 0}

        try:
            query = text("""
                         SELECT tp.TaskId,
                                tp.OwnerID,
                                e.EmployeeName + ' ' + e.EmployeeSurname AS FullName,
                                a.WorkEmail                              AS Email,
                                DATEDIFF(DAY, GETDATE(), tp.DataFine)    AS GiorniAllaScadenza
                         FROM TaskProdotto tp
                                  LEFT JOIN Employee.dbo.EmployeeHireHistory s ON tp.OwnerID = s.EmployeeHireHistoryId
                                  LEFT JOIN Employee.dbo.Employees e ON e.EmployeeId = s.EmployeeId
                                  LEFT JOIN Employee.dbo.EmployeeAddress a ON a.EmployeeId = e.EmployeeId
                         WHERE tp.DataFine BETWEEN GETDATE() AND DATEADD(DAY, :days_before, GETDATE())
                           AND tp.Stato NOT IN ('Completato', 'Cancellato')
                           AND tp.PercentualeCompletamento < 100
                           AND tp.OwnerID IS NOT NULL
                         """)

            results = self.session.execute(query, {'days_before': days_before}).fetchall()

            logger.info(f"🔍 Trovati {len(results)} task in scadenza tra {days_before} giorni")

            for row in results:
                task_id = row[0]
                owner_id = row[1]
                full_name = row[2]
                email = row[3]

                if not email:
                    continue

                if self._notify_upcoming_deadline_direct(
                        task_id=task_id,
                        owner_id=owner_id,
                        full_name=full_name,
                        email=email,
                        days_before=days_before
                ):
                    stats['notified'] += 1
                else:
                    stats['failed'] += 1

            return stats

        except Exception as e:
            logger.error(f"Errore controllo scadenze imminenti: {e}", exc_info=True)
            return stats

    def _notify_upcoming_deadline_direct(self, task_id: int, owner_id: int,
                                         full_name: str, email: str,
                                         days_before: int) -> bool:
        """Notifica scadenza imminente"""
        try:
            task = self.session.query(TaskProdotto).filter(
                TaskProdotto.TaskId == task_id
            ).first()

            if not task:
                return False

            subject = f"⏰ Reminder: Task in scadenza tra {days_before} giorni"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #d1ecf1; padding: 15px; border-left: 5px solid #0c5460; margin-bottom: 20px;">
                    <h2 style="color: #0c5460; margin: 0;">⏰ Reminder Scadenza Task</h2>
                </div>

                <p>Gentile <strong>{full_name}</strong>,</p>
                <p>Il seguente task scadrà tra <strong style="color: #ff8c00;">{days_before} giorni</strong>:</p>

                <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #f0f0f0;">
                        <td style="width: 30%;"><strong>Progetto:</strong></td>
                        <td>{task.wave.progetto.NomeProgetto}</td>
                    </tr>
                    <tr>
                        <td><strong>Task:</strong></td>
                        <td>{task.task_catalogo.NomeTask}</td>
                    </tr>
                    <tr style="background-color: #fff3cd;">
                        <td><strong>Data Scadenza:</strong></td>
                        <td>{task.DataFine.strftime('%d/%m/%Y') if task.DataFine else 'N/A'}</td>
                    </tr>
                    <tr>
                        <td><strong>Completamento:</strong></td>
                        <td>{task.PercentualeCompletamento}%</td>
                    </tr>
                    <tr>
                        <td><strong>Stato:</strong></td>
                        <td>{task.Stato}</td>
                    </tr>
                </table>

                <p style="margin-top: 20px;">
                    <strong>📌 Promemoria:</strong> Assicurati di completare il task entro la scadenza per evitare ritardi nel progetto.
                </p>

                <hr style="margin-top: 40px;">
                <p style="font-size: 0.9em; color: #666;">
                    Notifica automatica - Sistema NPI<br>
                    {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </body>
            </html>
            """

            return self._send_email_notification(
                recipient_email=email,
                recipient_name=full_name,
                subject=subject,
                body=body,
                task_prodotto_id=task_id,
                employee_hire_history_id=owner_id,
                reason=f'REMINDER_{days_before}DAYS'
            )

        except Exception as e:
            logger.error(f"Errore notifica reminder task {task_id}: {e}", exc_info=True)
            return False

    # ========================================
    # METODI PRIVATI DI SUPPORTO - CORRETTI
    # ========================================

    def _send_email_notification(self, recipient_email: str, recipient_name: str,
                                 subject: str, body: str, task_prodotto_id: int,
                                 employee_hire_history_id: Optional[int],
                                 reason: str, cc_emails: Optional[List[str]] = None,
                                 attachments: Optional[List[str]] = None) -> bool:
        """Invia email e logga risultato"""
        try:
            # Invia email con CC e allegati
            success = self.email_sender.send_email(
                to_email=recipient_email,
                subject=subject,
                body=body,
                is_html=True,
                cc_emails=cc_emails,
                attachments=attachments
            )

            # Logga risultato
            log_entry = NotificationLog(
                TaskProdottoId=task_prodotto_id,
                EmployeeHireHistoryId=employee_hire_history_id,
                NotificationType='EMAIL',
                NotificationReason=reason,
                RecipientEmail=recipient_email,
                RecipientName=recipient_name,
                Subject=subject,
                MessageBody=body,
                SentDate=datetime.now(),
                DeliveryStatus='SENT' if success else 'FAILED',
                ErrorMessage=None if success else 'Email send failed'
            )

            self.session.add(log_entry)
            self.session.commit()

            if success:
                cc_info = f" (CC: {', '.join(cc_emails)})" if cc_emails else ""
                attach_info = f" con {len(attachments)} allegato/i" if attachments else ""
                logger.info(f"✅ Email inviata a {recipient_name} ({recipient_email}){cc_info}{attach_info} per task {task_prodotto_id}")
            else:
                logger.error(f"❌ Invio email fallito a {recipient_email}")

            return success

        except Exception as e:
            logger.error(f"Errore invio email: {e}", exc_info=True)

            # Logga errore
            try:
                log_entry = NotificationLog(
                    TaskProdottoId=task_prodotto_id,
                    EmployeeHireHistoryId=employee_hire_history_id,
                    NotificationType='EMAIL',
                    NotificationReason=reason,
                    RecipientEmail=recipient_email,
                    RecipientName=recipient_name,
                    Subject=subject,
                    MessageBody=body,
                    SentDate=datetime.now(),
                    DeliveryStatus='FAILED',
                    ErrorMessage=str(e)
                )
                self.session.add(log_entry)
                self.session.commit()
            except:
                pass

            return False

    def _send_teams_notification(self, task: TaskProdotto, employee_info: Dict,
                                 reason: str, assigned_by: Optional[str] = None) -> bool:
        """Invia notifica Microsoft Teams"""
        if not self.teams_webhook_url:
            return False

        try:
            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": f"Task NPI: {task.task_catalogo.NomeTask}",
                "themeColor": "0078D7",
                "title": f"🎯 {task.task_catalogo.NomeTask}",
                "sections": [{
                    "activityTitle": f"Progetto: {task.wave.progetto.NomeProgetto}",
                    "activitySubtitle": f"Assegnato a: {employee_info['name']}",
                    "facts": [
                        {"name": "Data Inizio:",
                         "value": task.DataInizio.strftime('%d/%m/%Y') if task.DataInizio else 'N/A'},
                        {"name": "Data Scadenza:",
                         "value": task.DataFine.strftime('%d/%m/%Y') if task.DataFine else 'N/A'},
                        {"name": "Durata:", "value": f"{task.Durata} giorni"},
                        {"name": "Completamento:", "value": f"{task.PercentualeCompletamento}%"}
                    ],
                    "text": task.Note or "Nessuna nota"
                }]
            }

            response = requests.post(
                self.teams_webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(card),
                timeout=10
            )

            success = response.status_code == 200

            if success:
                logger.info(f"✅ Notifica Teams inviata per task {task.TaskId}")
            else:
                logger.error(f"❌ Invio Teams fallito: {response.status_code}")

            # Logga risultato
            log_entry = NotificationLog(
                TaskProdottoId=task.TaskId,
                EmployeeHireHistoryId=employee_info['employee_hire_history_id'],
                NotificationType='TEAMS',
                NotificationReason=reason,
                RecipientTeamsId=self.teams_webhook_url,
                RecipientName=employee_info['name'],
                Subject=f"Task: {task.task_catalogo.NomeTask}",
                MessageBody=json.dumps(card),
                SentDate=datetime.now(),
                DeliveryStatus='SENT' if success else 'FAILED',
                ErrorMessage=None if success else f"HTTP {response.status_code}"
            )

            self.session.add(log_entry)
            self.session.commit()

            return success

        except Exception as e:
            logger.error(f"Errore invio Teams: {e}", exc_info=True)
            return False

    def _was_notified_today(self, task_prodotto_id: int, reason: str) -> bool:
        """Controlla se task già notificato oggi"""
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            exists = self.session.query(NotificationLog).filter(
                and_(
                    NotificationLog.TaskProdottoId == task_prodotto_id,
                    NotificationLog.NotificationReason == reason,
                    NotificationLog.SentDate >= today_start,
                    NotificationLog.DeliveryStatus == 'SENT'
                )
            ).first()

            return exists is not None

        except Exception as e:
            logger.error(f"Errore controllo notifica: {e}")
            return False

    # ========================================
    # METODI DI REPORTING
    # ========================================

    def get_notification_stats(self, days: int = 7) -> Dict:
        """Statistiche notifiche ultimi N giorni"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            logs = self.session.query(NotificationLog).filter(
                NotificationLog.SentDate >= cutoff_date
            ).all()

            stats = {
                'total': len(logs),
                'sent': sum(1 for log in logs if log.DeliveryStatus == 'SENT'),
                'failed': sum(1 for log in logs if log.DeliveryStatus == 'FAILED'),
                'by_reason': {},
                'by_type': {}
            }

            for log in logs:
                # Per motivo
                if log.NotificationReason not in stats['by_reason']:
                    stats['by_reason'][log.NotificationReason] = 0
                stats['by_reason'][log.NotificationReason] += 1

                # Per tipo
                if log.NotificationType not in stats['by_type']:
                    stats['by_type'][log.NotificationType] = 0
                stats['by_type'][log.NotificationType] += 1

            return stats

        except Exception as e:
            logger.error(f"Errore recupero statistiche: {e}")
            return {}

    def get_failed_notifications(self, limit: int = 50) -> List[NotificationLog]:
        """Recupera notifiche fallite per retry"""
        try:
            return self.session.query(NotificationLog).filter(
                and_(
                    NotificationLog.DeliveryStatus == 'FAILED',
                    NotificationLog.RetryCount < 3
                )
            ).order_by(NotificationLog.SentDate.desc()).limit(limit).all()

        except Exception as e:
            logger.error(f"Errore recupero notifiche fallite: {e}")
            return []
