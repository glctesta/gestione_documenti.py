# start_notification_service.py

import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from npi.notification_scheduler import NotificationScheduler
from email_connector import EmailSender
from config import (
    DATABASE_CONNECTION_STRING,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    TEAMS_WEBHOOK_URL
)

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('notification_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Avvia il servizio di notifiche NPI"""

    logger.info("=" * 60)
    logger.info("🚀 AVVIO SERVIZIO NOTIFICHE NPI")
    logger.info("=" * 60)

    try:
        # Crea engine database
        engine = create_engine(
            DATABASE_CONNECTION_STRING,
            pool_pre_ping=True,
            pool_recycle=3600
        )

        # Crea session factory
        Session = sessionmaker(bind=engine)

        # Configura EmailSender
        email_sender = EmailSender(
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD
        )

        # Crea scheduler
        scheduler = NotificationScheduler(
            session_factory=Session,
            email_sender=email_sender,
            teams_webhook_url=TEAMS_WEBHOOK_URL
        )

        # Configura schedule
        scheduler.setup_schedules()

        # Avvia (blocking)
        logger.info("✅ Servizio pronto - In attesa di schedule...")
        scheduler.start()

    except KeyboardInterrupt:
        logger.info("⏹️ Servizio interrotto da utente")
    except Exception as e:
        logger.error(f"❌ Errore fatale: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("👋 Servizio terminato")


if __name__ == "__main__":
    main()
