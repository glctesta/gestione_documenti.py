# npi/notification_scheduler.py

import logging
import time
import schedule
from datetime import datetime
from typing import Callable
from sqlalchemy.orm import Session

from .notification_manager_v2 import NotificationManagerV2
from email_connector import EmailSender

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    Scheduler per esecuzione automatica controlli e notifiche
    """

    def __init__(self, session_factory: Callable[[], Session],
                 email_sender: EmailSender,
                 teams_webhook_url: str = None):
        """
        Args:
            session_factory: Factory per creare sessioni SQLAlchemy
            email_sender: Istanza EmailSender configurata
            teams_webhook_url: URL webhook Teams (opzionale)
        """
        self.session_factory = session_factory
        self.email_sender = email_sender
        self.teams_webhook_url = teams_webhook_url
        self.is_running = False

    def setup_schedules(self):
        """Configura gli schedule predefiniti"""

        # Controllo task scaduti - ogni giorno alle 9:00
        schedule.every().day.at("09:00").do(self._check_overdue_tasks)

        # Reminder 3 giorni prima - ogni giorno alle 9:00
        schedule.every().day.at("09:00").do(self._check_upcoming_deadlines_3days)

        # Reminder 1 giorno prima - ogni giorno alle 9:00
        schedule.every().day.at("09:00").do(self._check_upcoming_deadlines_1day)

        # Controllo task scaduti - anche alle 14:00
        schedule.every().day.at("14:00").do(self._check_overdue_tasks)

        # Report settimanale - ogni lunedì alle 8:00
        schedule.every().monday.at("08:00").do(self._send_weekly_report)

        logger.info("✅ Schedule notifiche configurati")
        logger.info("📅 Prossime esecuzioni:")
        for job in schedule.get_jobs():
            logger.info(f"   - {job}")

    def start(self):
        """Avvia lo scheduler (blocking)"""
        self.is_running = True
        logger.info("🚀 Scheduler notifiche avviato")

        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check ogni minuto
        except KeyboardInterrupt:
            logger.info("⏹️ Scheduler interrotto da utente")
        finally:
            self.stop()

    def stop(self):
        """Ferma lo scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("⏹️ Scheduler notifiche fermato")

    # ========================================
    # JOB SCHEDULATI
    # ========================================

    def _check_overdue_tasks(self):
        """Job: Controlla task scaduti"""
        logger.info("🔍 Avvio controllo task scaduti...")

        session = None
        try:
            session = self.session_factory()
            manager = NotificationManagerV2(
                session=session,
                email_sender=self.email_sender,
                teams_webhook_url=self.teams_webhook_url
            )

            stats = manager.check_and_notify_overdue_tasks()

            logger.info(f"✅ Controllo task scaduti completato: {stats}")

        except Exception as e:
            logger.error(f"❌ Errore controllo task scaduti: {e}", exc_info=True)
        finally:
            if session:
                session.close()

    def _check_upcoming_deadlines_3days(self):
        """Job: Reminder 3 giorni prima scadenza"""
        logger.info("🔍 Avvio reminder 3 giorni...")

        session = None
        try:
            session = self.session_factory()
            manager = NotificationManagerV2(
                session=session,
                email_sender=self.email_sender,
                teams_webhook_url=self.teams_webhook_url
            )

            stats = manager.check_and_notify_upcoming_deadlines(days_before=3)

            logger.info(f"✅ Reminder 3 giorni completato: {stats}")

        except Exception as e:
            logger.error(f"❌ Errore reminder 3 giorni: {e}", exc_info=True)
        finally:
            if session:
                session.close()

    def _check_upcoming_deadlines_1day(self):
        """Job: Reminder 1 giorno prima scadenza"""
        logger.info("🔍 Avvio reminder 1 giorno...")

        session = None
        try:
            session = self.session_factory()
            manager = NotificationManagerV2(
                session=session,
                email_sender=self.email_sender,
                teams_webhook_url=self.teams_webhook_url
            )

            stats = manager.check_and_notify_upcoming_deadlines(days_before=1)

            logger.info(f"✅ Reminder 1 giorno completato: {stats}")

        except Exception as e:
            logger.error(f"❌ Errore reminder 1 giorno: {e}", exc_info=True)
        finally:
            if session:
                session.close()

    def _send_weekly_report(self):
        """Job: Report settimanale notifiche"""
        logger.info("📊 Generazione report settimanale...")

        session = None
        try:
            session = self.session_factory()
            manager = NotificationManagerV2(
                session=session,
                email_sender=self.email_sender,
                teams_webhook_url=self.teams_webhook_url
            )

            stats = manager.get_notification_stats(days=7)

            # TODO: Invia report via email agli admin
            logger.info(f"📊 Statistiche settimanali: {stats}")

        except Exception as e:
            logger.error(f"❌ Errore report settimanale: {e}", exc_info=True)
        finally:
            if session:
                session.close()
