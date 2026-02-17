"""
Script di test per inviare email FAI usando l'ultima validazione
Destinatario: gianluca.testa@vandewiele.com
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from email_connector import EmailSender
from datetime import datetime
import logging
from config_manager import ConfigManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Carica credenziali criptate
config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
db_credentials = config_mgr.load_config()

DB_DRIVER = db_credentials['driver']
DB_SERVER = db_credentials['server']
DB_DATABASE = db_credentials['database']
DB_UID = db_credentials['username']
DB_PWD = db_credentials['password']
DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
               f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')

def test_fai_email():
    """Invia email di test usando l'ultima validazione FAI"""
    try:
        logger.info("Connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        
        # Recupera l'ultima validazione FAI
        logger.info("Recupero ultima validazione FAI...")
        query = """
        SELECT TOP 1 
            l.FaiLogId,
            l.OrderId,
            l.Operator,
            l.IsOk,
            l.DateIn,
            o.OrderNumber,
            o.ProductCode,
            o.ProductName
        FROM [Traceability_RS].[fai].[FaiLogs] l
        INNER JOIN Orders o ON o.IDOrder = l.OrderId
        ORDER BY l.DateIn DESC
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if not result:
            logger.error("❌ Nessuna validazione FAI trovata nel database")
            return
        
        fai_log_id = result.FaiLogId
        order_id = result.OrderId
        operator = result.Operator
        is_ok = result.IsOk
        date_in = result.DateIn
        order_number = result.OrderNumber
        product_code = result.ProductCode
        product_name = result.ProductName or product_code
        
        logger.info(f"✅ Trovata validazione FAI:")
        logger.info(f"   - FaiLogId: {fai_log_id}")
        logger.info(f"   - Order: {order_number} ({product_name})")
        logger.info(f"   - Operator: {operator}")
        logger.info(f"   - Result: {'PASSED ✓' if is_ok else 'FAILED ✗'}")
        logger.info(f"   - Date: {date_in}")
        
        # Determina risultato finale (controlla l'ultimo step)
        cursor.execute("""
            SELECT TOP 1 IsOk
            FROM [Traceability_RS].[fai].[FaiLogs]
            WHERE FaiLogId = ?
            ORDER BY DateIn DESC
        """, (fai_log_id,))
        
        last_step = cursor.fetchone()
        final_result = bool(last_step.IsOk) if last_step else True
        
        # Genera PDF report (se esiste la funzione)
        pdf_path = None
        try:
            from fai_report_generator import generate_fai_report
            import tempfile
            
            pdf_path = os.path.join(tempfile.gettempdir(), f"FAI_Report_{fai_log_id}_TEST.pdf")
            if generate_fai_report(fai_log_id, type('obj', (object,), {'cursor': cursor, 'conn': conn}), pdf_path):
                logger.info(f"✅ PDF generato: {pdf_path}")
            else:
                logger.warning("⚠️ Impossibile generare PDF")
                pdf_path = None
        except Exception as pdf_error:
            logger.warning(f"⚠️ Errore generazione PDF: {pdf_error}")
            pdf_path = None
        
        # Crea email HTML
        result_text = 'PASSED ✓' if final_result else 'FAILED ✗'
        result_color = "green" if final_result else "red"
        result_label = "PASSED" if final_result else "FAILED"
        result_icon = "✓" if final_result else "✗"
        
        subject = f"[TEST] FAI Validation Report - {product_name} - Order {order_number} - {result_text}"
        
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
                .test-banner {{
                    background-color: #fff3cd;
                    border: 2px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    text-align: center;
                    font-weight: bold;
                    color: #856404;
                }}
            </style>
        </head>
        <body>
            <div class="test-banner">
                ⚠️ QUESTA È UNA EMAIL DI TEST ⚠️
            </div>
            
            <div class="header">
                <h2>FAI (First Article Inspection) Validation Report</h2>
            </div>
            <div class="content">
                <div class="result">
                    Risultato Finale: {result_label} {result_icon}
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
                        <td>{date_in.strftime('%d/%m/%Y %H:%M') if date_in else 'N/A'}</td>
                    </tr>
                    <tr>
                        <td>Operator:</td>
                        <td>{operator}</td>
                    </tr>
                    <tr>
                        <td>FAI Log ID:</td>
                        <td>{fai_log_id}</td>
                    </tr>
                </table>
                
                <p>
                    {"Il report FAI completo è allegato a questa email in formato PDF." if pdf_path else "Report PDF non disponibile per questo test."}
                </p>
                
                <div class="test-banner">
                    📧 Email di test inviata a: gianluca.testa@vandewiele.com
                </div>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    Questa è una email automatica generata dal sistema di tracciabilità.
                    <br>Per qualsiasi domanda, contattare il reparto qualità.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Invia email
        logger.info("📧 Invio email di test...")
        sender = EmailSender("vandewiele-com.mail.protection.outlook.com", 25)
        sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")
        
        attachments = []
        if pdf_path and os.path.exists(pdf_path):
            attachments.append(pdf_path)
            logger.info(f"   📎 Allegato PDF: {pdf_path}")
        
        sender.send_email(
            to_email='gianluca.testa@vandewiele.com',
            subject=subject,
            body=html_body,
            is_html=True,
            attachments=attachments if attachments else None
        )
        
        logger.info("✅ Email inviata con successo!")
        logger.info(f"📧 Destinatario: gianluca.testa@vandewiele.com")
        logger.info(f"📊 Dati validazione: FaiLogId={fai_log_id}, Order={order_number}, Result={result_text}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Errore: {e}", exc_info=True)

if __name__ == "__main__":
    print("=" * 70)
    print("TEST INVIO EMAIL FAI - ULTIMA VALIDAZIONE")
    print("Destinatario: gianluca.testa@vandewiele.com")
    print("=" * 70)
    print()
    
    test_fai_email()
    
    print()
    print("=" * 70)
    print("Controlla la tua casella email!")
    print("=" * 70)
