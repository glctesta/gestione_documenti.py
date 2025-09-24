# utils.py
from email_connector import EmailSender
import logging
from typing import List, Optional

# Configurazione logging
logging.basicConfig(
    filename='ManageDocs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def get_email_recipients(conn) -> List[str]:
    """
    Recupera gli indirizzi email dei destinatari dal database.

    Args:
        conn: Connessione al database

    Returns:
        List[str]: Lista di indirizzi email validi
    """
    try:
        query = """
        SELECT [VALUE] 
        FROM traceability_rs.dbo.settings 
        WHERE atribute = 'Sys_Email_Purchase'
        """

        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        # Estrai gli indirizzi email dalla prima colonna di ogni riga
        email_list = [row[0] for row in results if row[0]]

        # Pulisci e valida gli indirizzi email
        valid_emails = []
        for email in email_list:
            # Gestisce il caso in cui ci siano più email separate da virgola o punto e virgola
            separators = [';', ',']
            emails = [email]

            for separator in separators:
                if separator in email:
                    emails = [e.strip() for e in email.split(separator)]
                    break

            valid_emails.extend([e for e in emails if e and '@' in e])
        print(valid_emails)
        return valid_emails
        logger.info(f"Indirizzi email trovati: {valid_emails}")
        return valid_emails

    except Exception as e:
        logger.error(f"Errore nel recupero degli indirizzi email: {str(e)}")
        raise  # Meglio sollevare l'eccezione invece di usare valori di default


def send_email(recipients: List[str], subject: str, body: str,
               smtp_host: str = "vandewiele-com.mail.protection.outlook.com", smtp_port: int = 25) -> None:
    """
    Invia l'email ai destinatari specificati.

    Args:
        recipients: Lista di indirizzi email destinatari
        subject: Oggetto dell'email
        body: Corpo dell'email
        smtp_host: Host SMTP (default: vandewiele-com.mail.protection.outlook.com)
        smtp_port: Porta SMTP (default: 25)

    Raises:
        ValueError: Se non ci sono destinatari
        Exception: Per altri errori durante l'invio
    """
    if not recipients:
        logger.error("Nessun destinatario specificato per l'email")
        raise ValueError("Nessun destinatario specificato per l'email")

    try:
        sender = EmailSender(smtp_host, smtp_port)
        # Prima volta: salva le credenziali (verranno criptate)
        sender.save_credentials("Accounting@Eutron.it",
                            "9jHgFhSs7Vf+"
                                )
        # Note: Le credenziali non dovrebbero essere nel codice
        # Utilizzare variabili d'ambiente o file di configurazione sicuri
        sender.send_email(
            to_email=', '.join(recipients),
            subject=subject,
            body=body,
            is_html=False
        )
        logger.info(f"Email inviata con successo a {len(recipients)} destinatari")
        print("email inviata")
    except Exception as e:
        logger.error(f"Errore nell'invio dell'email: {str(e)}")
        raise
