from email_connector import EmailSender
import logging
import re
from typing import List, Optional
import os


logger = logging.getLogger("TraceabilityRS")  # usa la config fatta in main.py

def get_email_recipients(conn, attribute: str = 'Sys_Email_Purchase') -> List[str]:
    """
    Recupera gli indirizzi email dei destinatari dal database per lo specifico attributo.
    Esempi di attributo: 'Sys_Email_Purchase', 'Sys_email_submission'
    """
    try:
        query = """
        SELECT [VALUE]
        FROM traceability_rs.dbo.settings
        WHERE atribute = ?
        """
        with conn.cursor() as cursor:
            cursor.execute(query, attribute)
            results = cursor.fetchall()

        email_list = [row[0] for row in results if row[0]]

        valid_emails = []
        for email in email_list:
            chunks = []
            if ';' in email:
                chunks = [e.strip() for e in email.split(';')]
            elif ',' in email:
                chunks = [e.strip() for e in email.split(',')]
            else:
                chunks = [email.strip()]
            valid_emails.extend([e for e in chunks if e and '@' in e])

        logger.info(f"Indirizzi email trovati per {attribute}: {valid_emails}")
        return valid_emails

    except Exception as e:
        logger.error(f"Errore nel recupero degli indirizzi email ({attribute}): {str(e)}")
        raise





def send_email(
    recipients: List[str],
    subject: str,
    body: str,
    smtp_host: str = "vandewiele-com.mail.protection.outlook.com",
    smtp_port: int = 25,
    is_html: bool = False,  # <-- nuovo parametro opzionale, default False: compatibile
    timeout: int= 15
) -> None:
    """
    Invia l'email ai destinatari specificati.

    Args:
        recipients: Lista di indirizzi email destinatari
        subject: Oggetto dell'email
        body: Corpo dell'email (testo o HTML se is_html=True)
        smtp_host: Host SMTP
        smtp_port: Porta SMTP
        is_html: Se True invia il corpo come HTML (default: False)

    Note: Usa EmailSender già presente nel progetto.
    :param timeout:
    """
    if not recipients:
        logger.error("Nessun destinatario specificato per l'email")
        return

    try:
        sender = EmailSender(smtp_host, smtp_port)

        # ATTENZIONE: credenziali hardcoded – idealmente spostarle in config sicura
        sender.save_credentials(
            "Accounting@Eutron.it",
            "9jHgFhSs7Vf+"
        )

        sender.send_email(
            to_email=', '.join(recipients),
            subject=subject,
            body=body,
            is_html=is_html  # <-- passa il flag
        )
        logger.info("Email inviata con successo a %d destinatari", len(recipients))
        print("email inviata")
    except Exception as e:
        logger.error("Errore nell'invio dell'email: %s", str(e))
        raise


def send_monthly_report_email(
    recipients: List[str],
    attachment_path: str,
    logo_path: str = "logo.png",
    smtp_host: str = "vandewiele-com.mail.protection.outlook.com",
    smtp_port: int = 25
) -> None:
    """
    Invia l'email mensile con il report Excel allegato e il logo aziendale.

    Args:
        recipients: Lista di indirizzi email destinatari
        attachment_path: Percorso completo del file Excel da allegare
        logo_path: Percorso del logo aziendale (default: logo.png nella directory corrente)
        smtp_host: Host SMTP
        smtp_port: Porta SMTP
    """
    if not recipients:
        logger.error("Nessun destinatario specificato per l'email mensile")
        return

    if not os.path.exists(attachment_path):
        logger.error(f"File allegato non trovato: {attachment_path}")
        raise FileNotFoundError(f"File allegato non trovato: {attachment_path}")

    try:
        sender = EmailSender(smtp_host, smtp_port)

        # Salva credenziali
        sender.save_credentials(
            "Accounting@Eutron.it",
            "9jHgFhSs7Vf+"
        )

        # Crea corpo HTML con logo embedded
        html_body = f"""
        <html>
        <body>
        <div style="font-family: Arial, sans-serif;">
            <div style="margin-bottom: 20px;">
                <img src="cid:company_logo" alt="Company Logo" width="200"/>
            </div>
            <h2 style="color: #366092;">Monthly Review - Fail after Board Validation</h2>
            <p>Questa email riepiloga la situazione afferente alle schede che sono state validate PASS per i processi di <strong>PTH</strong>, <strong>COATING</strong> e <strong>SMT</strong>.</p>
            <p>In allegato trovate il report dettagliato con le statistiche <strong>PPM</strong> (Parts Per Million) per utente.</p>
            <br/>
            <p style="color: #666;">
                Cordiali saluti,<br/>
                <strong>Sistema di Tracciabilità</strong>
            </p>
        </body>
        </html>
        """

        # Invia email con allegato
        sender.send_email(
            to_email=', '.join(recipients),
            subject="Monthly review - Fail after board validation",
            body=html_body,
            is_html=True,
            attachments=[attachment_path]
        )
        
        logger.info(f"Email mensile inviata con successo a {len(recipients)} destinatari")
        logger.info(f"Allegato: {os.path.basename(attachment_path)}")
        
    except Exception as e:
        logger.error(f"Errore nell'invio dell'email mensile: {str(e)}")
        raise


def get_employee_work_email(conn, employee_name: str) -> Optional[str]:
    """
    Recupera l'indirizzo email lavorativo (WorkEmail) di un dipendente in base al nome completo.

    Args:
        conn: Connessione al database
        employee_name: Nome completo del dipendente (es. "TESTA GIANLUCA")

    Returns:
        L'indirizzo email lavorativo come stringa se trovato, altrimenti None
    """
    try:
        # Dividi il nome in cognome e nome
        # Assumendo formato "COGNOME NOME"
        parts = employee_name.strip().split()
        if len(parts) < 2:
            logger.warning(f"Formato nome non valido: {employee_name}")
            return None
        
        surname = parts[0]
        name = ' '.join(parts[1:])  # In caso di nomi composti
        
        query = """
        SELECT a.WorkEmail 
        FROM employee.dbo.employees e 
        INNER JOIN employee.dbo.EmployeeAddress a 
            ON a.EmployeeId = e.EmployeeId 
            AND a.DateOut IS NULL 
        INNER JOIN employee.dbo.employeehirehistory h 
            ON e.employeeid = h.employeeid 
            AND h.EndWorkDate IS NULL 
            AND h.employeerid = 2
        WHERE e.EmployeeSurname = ? AND e.EmployeeName = ?
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (surname, name))
            row = cursor.fetchone()

        if row and row[0]:
            work_email = row[0].strip()
            logger.info(f"WorkEmail trovata per {employee_name}: {work_email}")
            return work_email

        logger.warning(f"Nessun risultato trovato per: {employee_name}")
        return None

    except Exception as e:
        logger.error(f"Errore nel recupero della WorkEmail per {employee_name}: {e}")
        raise