# npi/npi_auto_notifications.py
"""
Sistema di notifiche automatiche giornaliere per task NPI in scadenza o scaduti.
Invia email professionali ai responsabili dei task e ai responsabili dei progetti.
"""

import logging
import json
import os
from datetime import datetime, timedelta, date
from pathlib import Path
import threading
import time
from typing import Dict, List, Tuple, Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


class NpiAutoNotificationService:
    """
    Servizio per notifiche automatiche giornaliere per task NPI.
    Controlla task in scadenza (domani) e scaduti, inviando email ai responsabili.
    """
    
    def __init__(self, npi_manager, config_path='npi_notifications_config.json'):
        self.npi_manager = npi_manager
        self.config_path = config_path
        self.config = self._load_config()
        self.running = False
        self.thread = None
        
    def _load_config(self) -> dict:
        """Carica la configurazione dal file JSON."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Configurazione notifiche caricata da {self.config_path}")
                return config
            else:
                logger.warning(f"File configurazione {self.config_path} non trovato. Uso configurazione default.")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Errore caricamento configurazione: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Restituisce configurazione default."""
        return {
            "notification_settings": {
                "enabled": True,
                "check_time": "08:00",
                "email_sender_name": "NPI Project Management System",
                "include_logo": True,
                "logo_path": "logo.png"
            },
            "recipient_types": {
                "Interno": {"send_email": True},
                "Cliente": {"send_email": False},
                "Fornitore": {"send_email": False}
            },
            "notification_types": {
                "task_due_tomorrow": {"enabled": True, "days_before": 1},
                "task_overdue": {"enabled": True}
            }
        }
    
    def start(self):
        """Avvia il servizio di notifiche in background."""
        if self.running:
            logger.warning("Servizio notifiche già in esecuzione")
            return
        
        if not self.config['notification_settings']['enabled']:
            logger.info("Servizio notifiche disabilitato nella configurazione")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_service, daemon=True, name="NPINotificationService")
        self.thread.start()
        logger.info("Servizio notifiche automatiche NPI avviato")
    
    def stop(self):
        """Ferma il servizio di notifiche."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("Servizio notifiche automatiche NPI fermato")
    
    def _run_service(self):
        """Loop principale del servizio (esegue in thread separato)."""
        logger.info("Thread servizio notifiche in esecuzione")
        
        # Esegui immediatamente al primo avvio
        self._check_and_send_notifications()
        
        # Poi controlla ogni ora se è il momento di inviare
        check_time_str = self.config['notification_settings']['check_time']
        target_hour, target_minute = map(int, check_time_str.split(':'))
        
        while self.running:
            try:
                now = datetime.now()
                
                # Controlla se è l'ora configurata
                if now.hour == target_hour and now.minute == target_minute:
                    logger.info(f"Ora configurata raggiunta ({check_time_str}), avvio controllo notifiche")
                    self._check_and_send_notifications()
                    # Dormi un minuto per evitare esecuzioni multiple
                    time.sleep(60)
                else:
                    # Controlla ogni 30 secondi
                    time.sleep(30)
                    
            except Exception as e:
                logger.error(f"Errore nel loop del servizio notifiche: {e}", exc_info=True)
                time.sleep(300)  # Attendi 5 minuti in caso di errore
    
    def _check_and_send_notifications(self):
        """Controlla task e invia notifiche necessarie."""
        logger.info("=== INIZIO CONTROLLO NOTIFICHE NPI ===")
        
        try:
            # Ottieni tutti i progetti attivi
            progetti = self.npi_manager.get_all_npi_projects()
            
            if not progetti:
                logger.info("Nessun progetto NPI trovato")
                return
            
            total_sent = 0
            total_skipped = 0
            total_failed = 0
            
            for progetto in progetti:
                # Salta progetti chiusi
                if progetto.StatoProgetto == 'Chiuso':
                    continue
                
                sent, skipped, failed = self._process_project_notifications(progetto)
                total_sent += sent
                total_skipped += skipped
                total_failed += failed
            
            logger.info(f"=== FINE CONTROLLO NOTIFICHE NPI ===")
            logger.info(f"Totale email inviate: {total_sent}")
            logger.info(f"Totale email saltate: {total_skipped}")
            logger.info(f"Totale email fallite: {total_failed}")
            
        except Exception as e:
            logger.error(f"Errore durante controllo notifiche: {e}", exc_info=True)
    
    def _process_project_notifications(self, progetto) -> Tuple[int, int, int]:
        """Processa notifiche per un singolo progetto."""
        sent = 0
        skipped = 0
        failed = 0
        
        try:
            from ..models import TaskProdotto, WaveNPI
            
            # Ottieni tutti i task del progetto
            with self.npi_manager.session_scope() as session:
                tasks = session.scalars(
                    select(TaskProdotto)
                    .join(WaveNPI)
                    .where(
                        and_(
                            WaveNPI.ProgettoID == progetto.ProgettoId,
                            TaskProdotto.OwnerID.isnot(None),
                            TaskProdotto.Stato != 'Completato'
                        )
                    )
                    .options(
                        joinedload(TaskProdotto.owner),
                        joinedload(TaskProdotto.task_catalogo),
                        joinedload(TaskProdotto.wave).joinedload(WaveNPI.progetto).joinedload(ProgettoNPI.owner),
                        subqueryload(TaskProdotto.dependencies)
                    )
                ).all()
                
                for task in tasks:
                    s, sk, f = self._process_task_notifications(task, progetto, session)
                    sent += s
                    skipped += sk
                    failed += f
                
                # NUOVO: Analisi rischio progetto e notifica Project Owner
                s, sk, f = self._assess_project_risk_and_notify(progetto, tasks, session)
                sent += s
                skipped += sk
                failed += f
                    
        except Exception as e:
            logger.error(f"Errore processamento progetto {progetto.ProgettoId}: {e}", exc_info=True)
            failed += 1
        
        return sent, skipped, failed
    
    def _assess_project_risk_and_notify(self, progetto, tasks, session) -> Tuple[int, int, int]:
        """
        Analizza il rischio del progetto basandosi su task in ritardo.
        Invia email al Project Owner se il progetto è a rischio.
        
        Logica intelligente:
        - Conta task scaduti
        - Verifica task scaduti nel critical path (con dipendenti)
        - Calcola buffer temporale vs giorni necessari
        - Determina livello di rischio (Low/Medium/High/Critical)
        """
        from ..models import NpiTaskNotification, TaskProductDependency
        
        try:
            if not progetto.owner or not progetto.owner.Email:
                return 0, 0, 0
            
            # Verifica tipo soggetto
            recipient_category = progetto.owner.Tipo or 'Interno'
            recipient_config = self.config['recipient_types'].get(recipient_category, {"send_email": False})
            if not recipient_config['send_email']:
                return 0, 1, 0
            
            today = date.today()
            
            # 1. Identifica task in ritardo
            overdue_tasks = []
            for task in tasks:
                if task.DataScadenza:
                    due_date = task.DataScadenza.date() if hasattr(task.DataScadenza, 'date') else task.DataScadenza
                    if due_date < today and task.Stato != 'Completato':
                        overdue_tasks.append(task)
            
            # Se nessun task in ritardo, progetto ok
            if not overdue_tasks:
                return 0, 0, 0
            
            # 2. Analizza impatto task in ritardo
            critical_path_tasks = []  # Task in ritardo che bloccano altri task
            blocking_info = {}  # task_id -> lista di task bloccati
            
            for task in overdue_tasks:
                # Trova task che dipendono da questo task in ritardo
                dependent_tasks = session.scalars(
                    select(TaskProdotto)
                    .join(TaskProductDependency, TaskProductDependency.TaskProdottoID == TaskProdotto.TaskProdottoID)
                    .where(TaskProductDependency.DependsOnTaskProdottoID == task.TaskProdottoID)
                    .options(joinedload(TaskProdotto.task_catalogo), joinedload(TaskProdotto.owner))
                ).all()
                
                if dependent_tasks:
                    critical_path_tasks.append(task)
                    blocking_info[task.TaskProdottoID] = dependent_tasks
            
            # 3. Calcola buffer temporale
            project_end = progetto.ScadenzaProgetto
            if not project_end:
                buffer_days = None
            else:
                end_date = project_end.date() if hasattr(project_end, 'date') else project_end
                buffer_days = (end_date - today).days
            
            # 4. Determina livello di rischio
            risk_level, risk_color, risk_icon = self._calculate_risk_level(
                len(overdue_tasks),
                len(critical_path_tasks),
                buffer_days,
                len(tasks)
            )
            
            # 5. Verifica se già inviata oggi (evita duplicati)
            notification_type = f'ProjectRisk_{risk_level}'
            existing = session.scalars(
                select(NpiTaskNotification).where(
                    and_(
                        NpiTaskNotification.ProgettoID == progetto.ProgettoId,
                        NpiTaskNotification.RecipientSoggettoID == progetto.owner.SoggettoId,
                        NpiTaskNotification.NotificationType == notification_type,
                        NpiTaskNotification.NotificationDate == today
                    )
                )
            ).first()
            
            if existing:
                logger.debug(f"Risk notification già inviata oggi al Project Owner per progetto {progetto.ProgettoId}")
                return 0, 1, 0
            
            # 6. Genera e invia email di rischio progetto
            email_html = self._generate_project_risk_email(
                progetto, overdue_tasks, critical_path_tasks, blocking_info,
                risk_level, risk_color, risk_icon, buffer_days
            )
            
            from utils import send_email
            
            subject = f"🚨 NPI Project Risk Alert: {progetto.prodotto.NomeProdotto if progetto.prodotto else 'Project'} - {risk_level.upper()} RISK"
            
            send_email(
                recipients=[progetto.owner.Email],
                subject=subject,
                body=email_html,
                is_html=True
            )
            
            # 7. Registra notifica
            notification = NpiTaskNotification(
                TaskProdottoID=None,  # Non specifico di un task
                ProgettoID=progetto.ProgettoId,
                RecipientSoggettoID=progetto.owner.SoggettoId,
                NotificationType=notification_type,
                NotificationDate=today,
                RecipientEmail=progetto.owner.Email,
                RecipientName=progetto.owner.Nome,
                RecipientType='ProjectOwner',
                DeliveryStatus='Sent'
            )
            session.add(notification)
            session.commit()
            
            logger.info(f"Project Risk Alert ({risk_level}) inviato a {progetto.owner.Nome} per progetto {progetto.ProgettoId}")
            return 1, 0, 0
            
        except Exception as e:
            logger.error(f"Errore valutazione rischio progetto: {e}", exc_info=True)
            return 0, 0, 1
    
    def _calculate_risk_level(self, overdue_count, critical_path_count, buffer_days, total_tasks) -> Tuple[str, str, str]:
        """
        Calcola il livello di rischio del progetto basandosi su metriche.
        
        Returns:
            (risk_level, risk_color, risk_icon)
        """
        # Fattori di rischio
        overdue_ratio = overdue_count / max(total_tasks, 1)
        
        # CRITICAL: Task nel critical path in ritardo + poco buffer
        if critical_path_count > 0 and (buffer_days is None or buffer_days <= 7):
            return 'Critical', '#8B0000', '🔴'  # Dark Red
        
        # HIGH: Molti task in ritardo o critical path
        if overdue_ratio > 0.3 or critical_path_count >= 3:
            return 'High', '#DC143C', '🚨'  # Crimson
        
        # MEDIUM: Alcuni task in ritardo
        if overdue_ratio > 0.15 or critical_path_count >= 1:
            return 'Medium', '#FFA500', '⚠️'  # Orange
        
        # LOW: Pochi task in ritardo, molto buffer
        return 'Low', '#FFD700', '⚡'  # Gold
    
    def _process_task_notifications(self, task, progetto, session) -> Tuple[int, int, int]:
        """Processa notifiche per un singolo task."""
        sent = 0
        skipped = 0
        failed = 0
        
        if not task.DataScadenza:
            return sent, skipped, failed
        
        today = date.today()
        due_date = task.DataScadenza.date() if hasattr(task.DataScadenza, 'date') else task.DataScadenza
        
        # Determina il tipo di notifica
        notification_type = None
        
        if self.config['notification_types']['task_due_tomorrow']['enabled']:
            days_before = self.config['notification_types']['task_due_tomorrow']['days_before']
            if due_date == today + timedelta(days=days_before):
                notification_type = 'TaskDueTomorrow'
        
        if self.config['notification_types']['task_overdue']['enabled']:
            if due_date < today:
                notification_type = 'TaskOverdue'
        
        if not notification_type:
            return sent, skipped, failed
        
        # Invia email al task owner
        if task.owner:
            s, sk, f = self._send_notification_email(
                task, progetto, task.owner, 'TaskOwner', notification_type, session
            )
            sent += s
            skipped += sk
            failed += f
        
        # Invia email al project owner se diverso dal task owner
        if progetto.owner and progetto.owner.SoggettoId != (task.OwnerID if task.owner else None):
            s, sk, f = self._send_notification_email(
                task, progetto, progetto.owner, 'ProjectOwner', notification_type, session
            )
            sent += s
            skipped += sk
            failed += f
        
        return sent, skipped, failed
    
    def _send_notification_email(
        self, task, progetto, recipient, recipient_type, notification_type, session
    ) -> Tuple[int, int, int]:
        """Invia una email di notifica ed registra nel database."""
        from ..models import NpiTaskNotification
        
        # Verifica se il tipo di soggetto può ricevere email
        recipient_category = recipient.Tipo or 'Interno'
        recipient_config = self.config['recipient_types'].get(recipient_category, {"send_email": False})
        
        if not recipient_config['send_email']:
            logger.debug(f"Email saltata per {recipient.Nome} (tipo: {recipient_category})")
            return 0, 1, 0
        
        if not recipient.Email:
            logger.warning(f"Nessuna email configurata per {recipient.Nome}")
            return 0, 1, 0
        
        # Controllo duplicati
        today = date.today()
        existing = session.scalars(
            select(NpiTaskNotification).where(
                and_(
                    NpiTaskNotification.TaskProdottoID == task.TaskProdottoID,
                    NpiTaskNotification.RecipientSoggettoID == recipient.SoggettoId,
                    NpiTaskNotification.NotificationType == notification_type,
                    NpiTaskNotification.NotificationDate == today
                )
            )
        ).first()
        
        if existing:
            logger.debug(f"Notifica già inviata oggi a {recipient.Nome} per task {task.TaskProdottoID}")
            return 0, 1, 0
        
        # Genera email HTML
        email_html = self._generate_notification_email(task, progetto, recipient, recipient_type, notification_type)
        
        # Invia email
        try:
            from utils import send_email
            
            subject = f"NPI Task Alert: {task.task_catalogo.NomeTask if task.task_catalogo else 'Task'}"
            if notification_type == 'TaskDueTomorrow':
                subject += " - Due Tomorrow"
            else:
                subject += " - OVERDUE"
            
            send_email(
                recipients=[recipient.Email],
                subject=subject,
                body=email_html,
                is_html=True
            )
            
            # Registra notifica
            notification = NpiTaskNotification(
                TaskProdottoID=task.TaskProdottoID,
                ProgettoID=progetto.ProgettoId,
                RecipientSoggettoID=recipient.SoggettoId,
                NotificationType=notification_type,
                NotificationDate=today,
                RecipientEmail=recipient.Email,
                RecipientName=recipient.Nome,
                RecipientType=recipient_type,
                DeliveryStatus='Sent'
            )
            session.add(notification)
            session.commit()
            
            logger.info(f"Notifica {notification_type} inviata a {recipient.Nome} per task {task.TaskProdottoID}")
            return 1, 0, 0
            
        except Exception as e:
            logger.error(f"Errore invio email a {recipient.Nome}: {e}", exc_info=True)
            
            # Registra errore
            try:
                notification = NpiTaskNotification(
                    TaskProdottoID=task.TaskProdottoID,
                    ProgettoID=progetto.ProgettoId,
                    RecipientSoggettoID=recipient.SoggettoId,
                    NotificationType=notification_type,
                    NotificationDate=today,
                    RecipientEmail=recipient.Email,
                    RecipientName=recipient.Nome,
                    RecipientType=recipient_type,
                    DeliveryStatus='Failed',
                    ErrorMessage=str(e)
                )
                session.add(notification)
                session.commit()
            except:
                pass
            
            return 0, 0, 1
    
    def _generate_notification_email(
        self, task, progetto, recipient, recipient_type, notification_type
    ) -> str:
        """Genera HTML email professionale con logo."""
        
        # Determina il titolo e colore in base al tipo
        if notification_type == 'TaskDueTomorrow':
            alert_title = "⚠️ TASK DUE TOMORROW"
            alert_color = "#FFA500"  # Orange
            message = "This task is due tomorrow"
        else:  # TaskOverdue
            alert_title = "🚨 TASK OVERDUE"
            alert_color = "#DC143C"  # Crimson
            message = "This task is overdue and requires immediate attention"
        
        # Dati task
        task_name = task.task_catalogo.NomeTask if task.task_catalogo else "N/A"
        task_owner = task.owner.Nome if task.owner else "Unassigned"
        task_due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else "N/A"
        task_start_date = task.DataInizio.strftime('%d/%m/%Y') if task.DataInizio else "N/A"
        task_status = task.Stato or "Not Started"
        
        # Dati progetto
        project_name = progetto.prodotto.NomeProdotto if progetto.prodotto else "N/A"
        project_code = progetto.prodotto.CodiceProdotto if progetto.prodotto else "N/A"
        project_owner = progetto.owner.Nome if progetto.owner else "N/A"
        
        # Dipendenze bloccate
        blocked_tasks_html = ""
        dependencies = self.npi_manager.get_task_dependencies(task.TaskProdottoID)
        if dependencies:
            blocked_list = []
            with self.npi_manager.session_scope() as session:
                from ..models import TaskProdotto, TaskProductDependency
                
                # Trova task che dipendono da questo
                dependent_tasks = session.scalars(
                    select(TaskProdotto)
                    .join(TaskProductDependency, TaskProductDependency.TaskProdottoID == TaskProdotto.TaskProdottoID)
                    .where(TaskProductDependency.DependsOnTaskProdottoID == task.TaskProdottoID)
                    .options(joinedload(TaskProdotto.task_catalogo), joinedload(TaskProdotto.owner))
                ).all()
                
                for dep_task in dependent_tasks:
                    dep_name = dep_task.task_catalogo.NomeTask if dep_task.task_catalogo else "Task"
                    dep_owner = dep_task.owner.Nome if dep_task.owner else "Unassigned"
                    blocked_list.append(f"<li><strong>{dep_name}</strong> (Owner: {dep_owner})</li>")
            
            if blocked_list:
                blocked_tasks_html = f"""
                <div style="background: #FFF3CD; border-left: 4px solid #FFC107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ BLOCKED TASKS</h4>
                    <p style="margin: 0 0 10px 0; color: #856404;">The following tasks depend on this task and are currently blocked:</p>
                    <ul style="margin: 0; padding-left: 20px; color: #856404;">
                        {''.join(blocked_list)}
                    </ul>
                </div>
                """
        
        # Logo (base64 embedded o path)
        logo_html = ""
        if self.config['notification_settings']['include_logo']:
            logo_path = self.config['notification_settings']['logo_path']
            if os.path.exists(logo_path):
                # Per semplicità, usiamo un path relativo
                # In produzione, considerare di embeddare come base64
                logo_html = f'<img src="cid:logo" style="max-width: 150px; height: auto;" alt="Company Logo">'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
                .header {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 30px 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 10px 0 0 0; font-size: 24px; }}
                .alert-box {{ background: {alert_color}; color: white; padding: 20px; text-align: center; font-size: 20px; font-weight: bold; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .section {{ margin: 25px 0; padding: 20px; background: #f8f9fa; border-left: 4px solid #0078d4; border-radius: 4px; }}
                .section h2 {{ color: #0078d4; margin: 0 0 15px 0; font-size: 18px; border-bottom: 2px solid #0078d4; padding-bottom: 10px; }}
                .info-row {{ margin: 8px 0; }}
                .label {{ font-weight: bold; color: #555; display: inline-block; min-width: 120px; }}
                .value {{ color: #333; }}
                .footer {{ background: #f1f1f1; padding: 20px; margin-top: 20px; border-top: 3px solid #0078d4; border-radius: 4px; text-align: center; }}
                .footer p {{ margin: 5px 0; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    {logo_html}
                    <h1>NPI Project Management System</h1>
                    <p>Automated Task Notification</p>
                </div>
                
                <div class="alert-box">
                    {alert_title}
                </div>
                
                <div class="content">
                    <p style="font-size: 16px; margin-bottom: 20px;">Dear <strong>{recipient.Nome}</strong>,</p>
                    <p>{message}:</p>
                    
                    <div class="section">
                        <h2>📋 PROJECT DETAILS</h2>
                        <div class="info-row"><span class="label">Project Name:</span> <span class="value">{project_name}</span></div>
                        <div class="info-row"><span class="label">Product Code:</span> <span class="value">{project_code}</span></div>
                        <div class="info-row"><span class="label">Project Owner:</span> <span class="value">{project_owner}</span></div>
                    </div>
                    
                    <div class="section">
                        <h2>⚠️ TASK DETAILS</h2>
                        <div class="info-row"><span class="label">Task Name:</span> <span class="value" style="font-weight: bold; color: {alert_color};">{task_name}</span></div>
                        <div class="info-row"><span class="label">Task Owner:</span> <span class="value">{task_owner}</span></div>
                        <div class="info-row"><span class="label">Start Date:</span> <span class="value">{task_start_date}</span></div>
                        <div class="info-row"><span class="label">Due Date:</span> <span class="value" style="font-weight: bold; color: {alert_color};">{task_due_date}</span></div>
                        <div class="info-row"><span class="label">Status:</span> <span class="value">{task_status}</span></div>
                    </div>
                    
                    {blocked_tasks_html}
                    
                    <div style="background: #e7f3ff; border-left: 4px solid #0078d4; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <h4 style="color: #0078d4; margin: 0 0 10px 0;">📌 ACTION REQUIRED</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #333;">
                            <li>Please review and update the task status in the NPI system</li>
                            <li>Coordinate with team members if dependencies exist</li>
                            <li>Contact the project owner if you need assistance</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>This is an automated notification from the NPI Project Management System.</strong></p>
                    <p>Please do not reply to this email.</p>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_project_risk_email(
        self, progetto, overdue_tasks, critical_path_tasks, blocking_info,
        risk_level, risk_color, risk_icon, buffer_days
    ) -> str:
        """Genera email HTML di Project Risk Alert per il Project Owner."""
        
        # Dati progetto
        project_name = progetto.prodotto.NomeProdotto if progetto.prodotto else "N/A"
        project_code = progetto.prodotto.CodiceProdotto if progetto.prodotto else "N/A"
        project_owner = progetto.owner.Nome if progetto.owner else "N/A"
        project_end = progetto.ScadenzaProgetto.strftime('%d/%m/%Y') if progetto.ScadenzaProgetto else "Not Set"
        
        # Buffer info
        buffer_html = ""
        if buffer_days is not None:
            buffer_color = "#DC143C" if buffer_days <= 7 else "#FFA500" if buffer_days <= 14 else "#28a745"
            buffer_html = f'<div class="info-row"><span class="label">Days to Deadline:</span> <span class="value" style="font-weight: bold; color: {buffer_color};">{buffer_days} days</span></div>'
        
        # Lista task in ritardo
        overdue_list_html = ""
        for task in overdue_tasks:
            task_name = task.task_catalogo.NomeTask if task.task_catalogo else "Task"
            task_owner = task.owner.Nome if task.owner else "Unassigned"
            due_date = task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else "N/A"
            days_overdue = (date.today() - (task.DataScadenza.date() if hasattr(task.DataScadenza, 'date') else task.DataScadenza)).days
            
            # Icon se critical path
            critical_icon = " 🔗" if task in critical_path_tasks else ""
            
            overdue_list_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{task_name}{critical_icon}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{task_owner}</td>
                <td style="padding: 8px; border: 1px solid #ddd; color: #DC143C; font-weight: bold;">{due_date}</td>
                <td style="padding: 8px; border: 1px solid #ddd; color: #DC143C;">{days_overdue} days</td>
            </tr>
            """
        
        # Blocchi critici
        critical_path_html = ""
        if critical_path_tasks:
            blocked_sections = []
            for task in critical_path_tasks:
                task_name = task.task_catalogo.NomeTask if task.task_catalogo else "Task"
                blocked_tasks = blocking_info.get(task.TaskProdottoID, [])
                
                blocked_list = []
                for dep_task in blocked_tasks:
                    dep_name = dep_task.task_catalogo.NomeTask if dep_task.task_catalogo else "Task"
                    dep_owner = dep_task.owner.Nome if dep_task.owner else "Unassigned"
                    blocked_list.append(f"<li><strong>{dep_name}</strong> (Owner: {dep_owner})</li>")
                
                if blocked_list:
                    blocked_sections.append(f"""
                    <div style="margin: 10px 0; padding: 10px; background: #fff; border-left: 3px solid #DC143C;">
                        <strong style="color: #DC143C;">🔗 {task_name}</strong> is blocking:
                        <ul style="margin: 5px 0 0 20px; padding: 0;">
                            {''.join(blocked_list)}
                        </ul>
                    </div>
                    """)
            
            if blocked_sections:
                critical_path_html = f"""
                <div style="background: #FFF3CD; border-left: 4px solid #FFC107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h4 style="color: #856404; margin: 0 0 10px 0;">🔗 CRITICAL PATH IMPACT</h4>
                    <p style="margin: 0 0 10px 0; color: #856404;">The following overdue tasks are blocking other tasks, creating a critical path delay:</p>
                    {''.join(blocked_sections)}
                </div>
                """
        
        # Risk summary
        total_overdue = len(overdue_tasks)
        total_critical = len(critical_path_tasks)
        
        # Logo
        logo_html = ""
        if self.config['notification_settings']['include_logo']:
            logo_path = self.config['notification_settings']['logo_path']
            if os.path.exists(logo_path):
                logo_html = f'<img src="cid:logo" style="max-width: 150px; height: auto;" alt="Company Logo">'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
                .header {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 30px 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 10px 0 0 0; font-size: 24px; }}
                .alert-box {{ background: {risk_color}; color: white; padding: 25px; text-align: center; font-size: 24px; font-weight: bold; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .section {{ margin: 25px 0; padding: 20px; background: #f8f9fa; border-left: 4px solid #0078d4; border-radius: 4px; }}
                .section h2 {{ color: #0078d4; margin: 0 0 15px 0; font-size: 18px; border-bottom: 2px solid #0078d4; padding-bottom: 10px; }}
                .info-row {{ margin: 8px 0; }}
                .label {{ font-weight: bold; color: #555; display: inline-block; min-width: 150px; }}
                .value {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background: #0078d4; color: white; padding: 10px; text-align: left; }}
                .footer {{ background: #f1f1f1; padding: 20px; margin-top: 20px; border-top: 3px solid #0078d4; border-radius: 4px; text-align: center; }}
                .footer p {{ margin: 5px 0; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    {logo_html}
                    <h1>NPI Project Management System</h1>
                    <p>Project Risk Alert</p>
                </div>
                
                <div class="alert-box">
                    {risk_icon} {risk_level.upper()} RISK - PROJECT AT RISK
                </div>
                
                <div class="content">
                    <p style="font-size: 16px; margin-bottom: 20px;">Dear <strong>{project_owner}</strong>,</p>
                    <p><strong>This automated alert notifies you that your project is at risk due to overdue tasks.</strong></p>
                    <p>Immediate action is required to prevent project delays and ensure timely completion.</p>
                    
                    <div class="section">
                        <h2>📋 PROJECT DETAILS</h2>
                        <div class="info-row"><span class="label">Project Name:</span> <span class="value">{project_name}</span></div>
                        <div class="info-row"><span class="label">Product Code:</span> <span class="value">{project_code}</span></div>
                        <div class="info-row"><span class="label">Project Owner:</span> <span class="value">{project_owner}</span></div>
                        <div class="info-row"><span class="label">Project End Date:</span> <span class="value">{project_end}</span></div>
                        {buffer_html}
                    </div>
                    
                    <div class="section">
                        <h2>⚠️ RISK ANALYSIS</h2>
                        <div class="info-row"><span class="label">Risk Level:</span> <span class="value" style="font-weight: bold; color: {risk_color};">{risk_icon} {risk_level.upper()}</span></div>
                        <div class="info-row"><span class="label">Total Overdue Tasks:</span> <span class="value" style="font-weight: bold; color: #DC143C;">{total_overdue}</span></div>
                        <div class="info-row"><span class="label">Critical Path Tasks:</span> <span class="value" style="font-weight: bold; color: #DC143C;">{total_critical}</span></div>
                        
                        <div style="background: #f8d7da; border-left: 4px solid #DC143C; padding: 15px; margin: 15px 0; border-radius: 4px;">
                            <h4 style="color: #721c24; margin: 0 0 10px 0;">⚠️ IMPACT ASSESSMENT</h4>
                            <p style="margin: 0; color: #721c24;">
                                Due to the overdue tasks, <strong>it is difficult for this project to be completed on time</strong>.
                                {f'With only {buffer_days} days remaining, ' if buffer_days is not None else ''}
                                {'Critical path tasks are blocking other team members, creating cascading delays.' if total_critical > 0 else 'Immediate corrective action is essential to recover the schedule.'}
                            </p>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>📝 OVERDUE TASKS DETAILS</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Task Name</th>
                                    <th>Owner</th>
                                    <th>Due Date</th>
                                    <th>Days Overdue</th>
                                </tr>
                            </thead>
                            <tbody>
                                {overdue_list_html}
                            </tbody>
                        </table>
                        <p style="font-size: 12px; color: #666; margin-top: 10px;">🔗 = Task on critical path (blocking other tasks)</p>
                    </div>
                    
                    {critical_path_html}
                    
                    <div style="background: #d1ecf1; border-left: 4px solid #0078d4; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <h4 style="color: #0c5460; margin: 0 0 10px 0;">📌 RECOMMENDED ACTIONS</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #0c5460;">
                            <li><strong>Immediate Review:</strong> Contact task owners to understand delays and obstacles</li>
                            <li><strong>Resource Allocation:</strong> Consider reassigning resources to critical path tasks</li>
                            <li><strong>Timeline Adjustment:</strong> Evaluate if project timeline needs revision</li>
                            <li><strong>Stakeholder Communication:</strong> Inform stakeholders about project status and risks</li>
                            <li><strong>Daily Monitoring:</strong> Implement daily standup to track progress on overdue tasks</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>This is an automated risk assessment from the NPI Project Management System.</strong></p>
                    <p>Please do not reply to this email.</p>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html


# Istanza globale del servizio
_notification_service = None


def start_notification_service(npi_manager, config_path='npi_notifications_config.json'):
    """Avvia il servizio di notifiche automatiche."""
    global _notification_service
    
    if _notification_service is None:
        _notification_service = NpiAutoNotificationService(npi_manager, config_path)
        _notification_service.start()
        logger.info("Servizio notifiche automatiche NPI inizializzato")
    else:
        logger.warning("Servizio notifiche già attivo")
    
    return _notification_service


def stop_notification_service():
    """Ferma il servizio di notifiche automatiche."""
    global _notification_service
    
    if _notification_service:
        _notification_service.stop()
        _notification_service = None
        logger.info("Servizio notifiche automatiche NPI terminato")
