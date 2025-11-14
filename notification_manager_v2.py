# npi/notification_manager_v2.py

import logging
import requests
import json
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import tempfile
import os
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from email_connector import EmailSender
from npi.data_models import (
    TaskProdotto, Soggetto, NotificationLog,
    NotificationSchedule, NotificationRecipients,
    ProgettoNPI, TaskCatalogo
)

logger = logging.getLogger(__name__)


class NotificationManagerV2:
    """
    Gestione completa notifiche NPI con:
    - Invio email/Teams
    - Controllo scadenze automatico
    - Logging completo
    - Retry mechanism
    """

    def __init__(self, session: Session, email_sender: EmailSender,
                 teams_webhook_url: Optional[str] = None):
        """
        Args:
            session: SQLAlchemy session
            email_sender: Istanza EmailSender configurata
            teams_webhook_url: URL webhook Microsoft Teams (opzionale)
        """
        self.session = session
        self.email_sender = email_sender
        self.teams_webhook_url = teams_webhook_url

    # ========================================
    # METODI PRINCIPALI DI NOTIFICA
    # ========================================

    def notify_task_assignment(self, task_prodotto_id: int,
                               assigned_by: Optional[str] = None) -> bool:
        """
        Notifica assegnazione task a responsabile

        Args:
            task_prodotto_id: ID del task assegnato
            assigned_by: Username di chi ha assegnato il task

        Returns:
            True se notifica inviata con successo
        """
        try:
            # Recupera task con relazioni
            task = self.session.query(TaskProdotto).filter(
                TaskProdotto.TaskProdottoId == task_prodotto_id
            ).first()

            if not task:
                logger.error(f"Task {task_prodotto_id} non trovato")
                return False

            if not task.soggetto:
                logger.warning(f"Task {task_prodotto_id} non ha responsabile assegnato")
                return False

            # Prepara messaggio
            subject = f"🎯 Nuovo Task Assegnato: {task.task_catalogo.NomeTask}"

            body = f"""
            <html>
            <body>
                <h2>Nuovo Task Assegnato</h2>
                <p>Gentile {task.soggetto.Nome},</p>
                <p>Ti è stato assegnato un nuovo task nel progetto NPI:</p>

                <table border="1" cellpadding="10" style="border-collapse: collapse;margin: 20px 0;">
                    <tr><td><strong>Progetto:</strong></td><td>{task.wave.progetto.NomeProgetto}</td></tr>
                    <tr><td><strong>Task:</strong></td><td>{task.task_catalogo.NomeTask}</td></tr>
                    <tr><td><strong>Descrizione:</strong></td><td>{task.task_catalogo.Descrizione or 'N/A'}</td></tr>
                    <tr><td><strong>Data Inizio:</strong></td><td>{task.DataInizio.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td><strong>Data Scadenza:</strong></td><td>{task.DataFine.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td><strong>Durata:</strong></td><td>{task.Durata} giorni</td></tr>
                </table>

                <p><strong>Note:</strong> {task.Note or 'Nessuna nota'}</p>

                <p>Accedi al sistema per visualizzare i dettagli completi.</p>

                <hr>
                <p style="font-size: 0.9em; color: #666;">
                    Assegnato da: {assigned_by or 'Sistema'}<br>
                    Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </body>
            </html>
            """

            # Invia email
            email_sent = self._send_email_notification(
                recipient_email=task.soggetto.Email,
                subject=subject,
                body=body,
                task_prodotto_id=task_prodotto_id,
                soggetto_id=task.soggetto.SoggettoId,
                reason='ASSIGNMENT'
            )

            # Invia Teams se configurato
            teams_sent = False
            if self.teams_webhook_url:
                teams_sent = self._send_teams_notification(
                    task=task,
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

        Returns:
            Dict con statistiche: {'notified': X, 'failed': Y}
        """
        stats = {'notified': 0, 'failed': 0, 'skipped': 0}

        try:
            # Query task scaduti
            overdue_tasks = self.session.query(TaskProdotto).filter(
                and_(
                    TaskProdotto.DataFine < datetime.now(),
                    TaskProdotto.Stato.notin_(['Completato', 'Cancellato']),
                    TaskProdotto.PercentualeCompletamento < 100
                )
            ).all()

            logger.info(f"🔍 Trovati {len(overdue_tasks)} task scaduti")

            for task in overdue_tasks:
                # Controlla se già notificato oggi
                if self._was_notified_today(task.TaskProdottoId, 'OVERDUE'):
                    stats['skipped'] += 1
                    continue

                if self._notify_overdue_task(task):
                    stats['notified'] += 1
                else:
                    stats['failed'] += 1

            logger.info(f"📊 Notifiche ritardi: {stats['notified']} inviate, "
                        f"{stats['failed']} fallite, {stats['skipped']} saltate")

            return stats

        except Exception as e:
            logger.error(f"Errore controllo task scaduti: {e}", exc_info=True)
            return stats

    def check_and_notify_upcoming_deadlines(self, days_before: int = 3) -> Dict[str, int]:
        """
        Notifica task in scadenza nei prossimi N giorni

        Args:
            days_before: Giorni prima della scadenza per notifica

        Returns:
            Dict con statistiche
        """
        stats = {'notified': 0, 'failed': 0}

        try:
            target_date = datetime.now() + timedelta(days=days_before)

            # Query task in scadenza
            upcoming_tasks = self.session.query(TaskProdotto).filter(
                and_(
                    TaskProdotto.DataFine.between(
                        datetime.now(),
                        target_date
                    ),
                    TaskProdotto.Stato.notin_(['Completato', 'Cancellato']),
                    TaskProdotto.PercentualeCompletamento < 100
                )
            ).all()

            logger.info(f"🔍 Trovati {len(upcoming_tasks)} task in scadenza tra {days_before} giorni")

            for task in upcoming_tasks:
                if self._notify_upcoming_deadline(task, days_before):
                    stats['notified'] += 1
                else:
                    stats['failed'] += 1

            return stats

        except Exception as e:
            logger.error(f"Errore controllo scadenze imminenti: {e}", exc_info=True)
            return stats

    # ========================================
    # METODI PRIVATI DI SUPPORTO
    # ========================================

    def _notify_overdue_task(self, task: TaskProdotto) -> bool:
        """Notifica task scaduto"""
        try:
            if not task.soggetto:
                return False

            days_overdue = (datetime.now() - task.DataFine).days

            subject = f"⚠️ TASK IN RITARDO: {task.task_catalogo.NomeTask} ({days_overdue} giorni)"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107;">
                    <h2 style="color: #856404;">⚠️ Task in Ritardo</h2>
                </div>

                <p>Gentile {task.soggetto.Nome},</p>
                <p><strong>Il seguente task è scaduto da {days_overdue} giorni:</strong></p>

                <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
                    <tr style="background-color: #f8d7da;">
                        <td><strong>Progetto:</strong></td>
                        <td>{task.progetto_npi.NomeProgetto}</td>
                    </tr>
                    <tr>
                        <td><strong>Task:</strong></td>
                        <td>{task.task_catalogo.NomeTask}</td>
                    </tr>
                    <tr>
                        <td><strong>Data Scadenza:</strong></td>
                        <td>{task.DataFine.strftime('%d/%m/%Y')}</td>
                    </tr>
                    <tr>
                        <td><strong>Giorni di Ritardo:</strong></td>
                        <td style="color: red; font-weight: bold;">{days_overdue}</td>
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
                    <strong>Azione richiesta:</strong> Si prega di aggiornare lo stato del task 
                    o contattare il project manager per una ripianificazione.
                </p>

                <hr>
                <p style="font-size: 0.9em; color: #666;">
                    Notifica automatica - {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </body>
            </html>
            """

            return self._send_email_notification(
                recipient_email=task.soggetto.Email,
                subject=subject,
                body=body,
                task_prodotto_id=task.TaskProdottoId,
                soggetto_id=task.soggetto.SoggettoId,
                reason='OVERDUE'
            )

        except Exception as e:
            logger.error(f"Errore notifica ritardo task {task.TaskProdottoId}: {e}")
            return False

    def _notify_upcoming_deadline(self, task: TaskProdotto, days_before: int) -> bool:
        """Notifica scadenza imminente"""
        try:
            if not task.soggetto:
                return False

            subject = f"⏰ Reminder: Task in scadenza tra {days_before} giorni"

            body = f"""
            <html>
            <body>
                <h2>⏰ Reminder Scadenza Task</h2>
                <p>Gentile {task.soggetto.Nome},</p>
                <p>Il seguente task scadrà tra <strong>{days_before} giorni</strong>:</p>

                <table border="1" cellpadding="10" style="border-collapse: collapse;">
                    <tr><td><strong>Progetto:</strong></td><td>{task.progetto_npi.NomeProgetto}</td></tr>
                    <tr><td><strong>Task:</strong></td><td>{task.task_catalogo.NomeTask}</td></tr>
                    <tr><td><strong>Data Scadenza:</strong></td><td>{task.DataFine.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td><strong>Completamento:</strong></td><td>{task.PercentualeCompletamento}%</td></tr>
                </table>

                <p>Assicurati di completare il task entro la scadenza.</p>
            </body>
            </html>
            """

            return self._send_email_notification(
                recipient_email=task.soggetto.Email,
                subject=subject,
                body=body,
                task_prodotto_id=task.TaskProdottoId,
                soggetto_id=task.soggetto.SoggettoId,
                reason=f'REMINDER_{days_before}DAYS'
            )

        except Exception as e:
            logger.error(f"Errore notifica reminder task {task.TaskProdottoId}: {e}")
            return False

    def _send_email_notification(self, recipient_email: str, subject: str,
                                 body: str, task_prodotto_id: int,
                                 soggetto_id: Optional[int], reason: str) -> bool:
        """Invia email e logga risultato"""
        try:
            # Invia email
            success = self.email_sender.send_email(
                to_address=recipient_email,
                subject=subject,
                body=body,
                is_html=True
            )

            # Logga risultato
            log_entry = NotificationLog(
                TaskProdottoId=task_prodotto_id,
                SoggettoId=soggetto_id,
                NotificationType='EMAIL',
                NotificationReason=reason,
                RecipientEmail=recipient_email,
                Subject=subject,
                MessageBody=body,
                SentDate=datetime.now(),
                DeliveryStatus='SENT' if success else 'FAILED',
                ErrorMessage=None if success else 'Email send failed'
            )

            self.session.add(log_entry)
            self.session.commit()

            if success:
                logger.info(f"✅ Email inviata a {recipient_email} per task {task_prodotto_id}")
            else:
                logger.error(f"❌ Invio email fallito a {recipient_email}")

            return success

        except Exception as e:
            logger.error(f"Errore invio email: {e}", exc_info=True)

            # Logga errore
            try:
                log_entry = NotificationLog(
                    TaskProdottoId=task_prodotto_id,
                    SoggettoId=soggetto_id,
                    NotificationType='EMAIL',
                    NotificationReason=reason,
                    RecipientEmail=recipient_email,
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

    def _send_teams_notification(self, task: TaskProdotto, reason: str,
                                 assigned_by: Optional[str] = None) -> bool:
        """Invia notifica Microsoft Teams"""
        if not self.teams_webhook_url:
            return False

        try:
            # Prepara messaggio Teams (Adaptive Card)
            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": f"Task NPI: {task.task_catalogo.NomeTask}",
                "themeColor": "0078D7",
                "title": f"🎯 {task.task_catalogo.NomeTask}",
                "sections": [{
                    "activityTitle": f"Progetto: {task.progetto_npi.NomeProgetto}",
                    "activitySubtitle": f"Assegnato a: {task.soggetto.Nome if task.soggetto else 'N/A'}",
                    "facts": [
                        {"name": "Data Inizio:", "value": task.DataInizio.strftime('%d/%m/%Y')},
                        {"name": "Data Scadenza:", "value": task.DataFine.strftime('%d/%m/%Y')},
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
                logger.info(f"✅ Notifica Teams inviata per task {task.TaskProdottoId}")
            else:
                logger.error(f"❌ Invio Teams fallito: {response.status_code} - {response.text}")

            # Logga risultato
            log_entry = NotificationLog(
                TaskProdottoId=task.TaskProdottoId,
                SoggettoId=task.SoggettoId,
                NotificationType='TEAMS',
                NotificationReason=reason,
                RecipientTeamsId=self.teams_webhook_url,
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
