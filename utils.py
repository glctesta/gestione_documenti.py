# utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
from datetime import datetime

# Email Configuration (Assuming Office 365)
SMTP_SERVER = "vandewiele-com.mail.protection.outlook.com"
SMTP_PORT = 25
SMTP_USER = "Accounting@Eutron.it"
SMTP_PASSWORD = "9jHgFhSs7Vf+"  # Password fornita dall'utente


def send_email(recipients, subject, body):
    """Sends an email using the configured SMTP settings."""

    # Recipients deve essere una lista di stringhe
    if not recipients:
        print("Email sending skipped: No recipients provided.")
        return True

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    # Unisce la lista dei destinatari in una stringa separata da virgole per l'header
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connessione al server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # Identificazione al server SMTP

        # Avvio crittografia TLS
        server.starttls()
        server.ehlo()  # Re-identificazione dopo connessione TLS

        # Login
        server.login(SMTP_USER, SMTP_PASSWORD)

        # Invio email
        # Il secondo argomento deve essere la lista degli indirizzi
        server.sendmail(SMTP_USER, recipients, msg.as_string())

        # Disconnessione
        server.quit()
        print(f"Email successfully sent to {msg['To']}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Failed to send email: SMTP Authentication Error. Check username/password.")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"Failed to send email: {e}")
        traceback.print_exc()
        return False
