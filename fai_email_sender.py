"""
Modulo per l'invio di email di notifica per validazioni FAI
"""

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime

logger = logging.getLogger("TraceabilityRS")


def send_fai_notification_email(db, fai_log_id, pdf_path, product_name, order_number, operator_name, final_result):
    """
    Invia email di notifica per validazione FAI
    
    Args:
        db: Connessione database
        fai_log_id: ID del log FAI
        pdf_path: Percorso del PDF allegato
        product_name: Nome prodotto
        order_number: Numero ordine
        operator_name: Nome operatore
        final_result: True se ultimo step OK, False altrimenti
    """
    try:
        # Recupera indirizzi email da Settings
        email_query = """
        SELECT [Value]
        FROM [Traceability_RS].[dbo].[Settings]
        WHERE [Atribute] = 'Sys_verifica_linea'
        """
        
        db.cursor.execute(email_query)
        result = db.cursor.fetchone()
        
        if not result or not result.Value:
            logger.warning("Nessun indirizzo email configurato per Sys_verifica_linea")
            return False
        
        # Gli indirizzi potrebbero essere separati da virgola/punto e virgola
        recipients = [email.strip() for email in result.Value.replace(';', ',').split(',')]
        
        # Carica configurazione SMTP
        try:
            from smtp_config import SMTP_CONFIG
            smtp_server = SMTP_CONFIG.get('server', 'smtp.office365.com')
            smtp_port = SMTP_CONFIG.get('port', 587)
            smtp_user = SMTP_CONFIG.get('user', 'noreply@tuodominio.com')
            smtp_password = SMTP_CONFIG.get('password', 'password')
        except ImportError:
            logger.warning("smtp_config.py non trovato, uso valori di default")
            smtp_server = "smtp.office365.com"
            smtp_port = 587
            smtp_user = "noreply@tuodominio.com"
            smtp_password = "password"
        
        # Crea messaggio email
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = f"FAI Validation Report - {product_name} - Order {order_number} - {'PASSED ✓' if final_result else 'FAILED ✗'}"
        
        # Corpo email HTML
        result_color = "green" if final_result else "red"
        result_text = "PASSED" if final_result else "FAILED"
        result_icon = "✓" if final_result else "✗"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #003366; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .result {{ 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: {result_color}; 
                    padding: 10px;
                    border: 2px solid {result_color};
                    display: inline-block;
                    margin: 10px 0;
                }}
                .info-table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0;
                }}
                .info-table td {{ 
                    padding: 8px; 
                    border: 1px solid #ddd; 
                }}
                .info-table td:first-child {{ 
                    font-weight: bold; 
                    background-color: #f0f0f0;
                    width: 30%;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>FAI (First Article Inspection) Validation Report</h2>
            </div>
            <div class="content">
                <div class="result">
                    Risultato Finale: {result_text} {result_icon}
                </div>
                
                <table class="info-table">
                    <tr>
                        <td>Product:</td>
                        <td><strong>{product_name}</strong></td>
                    </tr>
                    <tr>
                        <td>Order Number:</td>
                        <td><strong>{order_number}</strong></td>
                    </tr>
                    <tr>
                        <td>Validation Date:</td>
                        <td>{datetime.now().strftime('%d/%m/%Y %H:%M')}</td>
                    </tr>
                    <tr>
                        <td>Operator:</td>
                        <td>{operator_name}</td>
                    </tr>
                    <tr>
                        <td>FAI Log ID:</td>
                        <td>{fai_log_id}</td>
                    </tr>
                </table>
                
                <p>
                    Il report FAI completo è allegato a questa email in formato PDF.
                </p>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    Questa è una email automatica generata dal sistema di tracciabilità.
                    <br>Per qualsiasi domanda, contattare il reparto qualità.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Allega PDF se esiste
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
                pdf_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f'FAI_Report_{order_number}_{datetime.now().strftime("%Y%m%d")}.pdf'
                )
                msg.attach(pdf_attachment)
        
        # Invia email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email FAI inviata a: {', '.join(recipients)}")
        return True
        
    except Exception as e:
        logger.error(f"Errore invio email FAI: {e}", exc_info=True)
        return False
