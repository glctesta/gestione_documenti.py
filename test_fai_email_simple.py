"""
Script di test semplificato per inviare email FAI
Output salvato in test_fai_output.txt
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from email_connector import EmailSender
from datetime import datetime
from config_manager import ConfigManager

# Redirect output to file
output_file = open('test_fai_output.txt', 'w', encoding='utf-8')

def log(msg):
    print(msg)
    output_file.write(msg + '\n')
    output_file.flush()

try:
    log("=" * 70)
    log("TEST INVIO EMAIL FAI - ULTIMA VALIDAZIONE")
    log("=" * 70)
    log("")
    
    # Carica credenziali
    log("1. Caricamento credenziali database...")
    config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
    db_credentials = config_mgr.load_config()
    
    DB_DRIVER = db_credentials['driver']
    DB_SERVER = db_credentials['server']
    DB_DATABASE = db_credentials['database']
    DB_UID = db_credentials['username']
    DB_PWD = db_credentials['password']
    DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
                   f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')
    
    log(f"   ✅ Server: {DB_SERVER}")
    log(f"   ✅ Database: {DB_DATABASE}")
    log("")
    
    # Connessione database
    log("2. Connessione al database...")
    conn = pyodbc.connect(DB_CONN_STR, timeout=10)
    cursor = conn.cursor()
    log("   ✅ Connesso!")
    log("")
    
    # Recupera ultima validazione
    log("3. Recupero ultima validazione FAI...")
    query = """
    SELECT TOP 1 
        l.FaiLogId,
        l.OrderId,
        l.Operator,
        l.IsOk,
        l.DateIn,
        o.OrderNumber,
        CAST(o.IDOrder AS VARCHAR(50)) as ProductInfo
    FROM [Traceability_RS].[fai].[FaiLogs] l
    INNER JOIN Orders o ON o.IDOrder = l.OrderId
    ORDER BY l.DateIn DESC
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if not result:
        log("   ❌ Nessuna validazione FAI trovata!")
        output_file.close()
        sys.exit(1)
    
    fai_log_id = result.FaiLogId
    order_number = result.OrderNumber
    product_name = f"Order {order_number}"  # Usa OrderNumber come product name
    operator = result.Operator
    is_ok = result.IsOk
    date_in = result.DateIn
    
    log(f"   ✅ FaiLogId: {fai_log_id}")
    log(f"   ✅ Order: {order_number}")
    log(f"   ✅ Product: {product_name}")
    log(f"   ✅ Operator: {operator}")
    log(f"   ✅ Result: {'PASSED ✓' if is_ok else 'FAILED ✗'}")
    log(f"   ✅ Date: {date_in}")
    log("")
    
    # Genera PDF
    log("4. Generazione PDF report...")
    pdf_path = None
    try:
        from fai_report_generator import generate_fai_report
        import tempfile
        
        pdf_path = os.path.join(tempfile.gettempdir(), f"FAI_Report_{fai_log_id}_TEST.pdf")
        
        # Crea oggetto db mock per generate_fai_report
        class DBMock:
            def __init__(self, cursor, conn):
                self.cursor = cursor
                self.conn = conn
        
        db_mock = DBMock(cursor, conn)
        
        if generate_fai_report(fai_log_id, db_mock, pdf_path):
            log(f"   ✅ PDF generato: {pdf_path}")
        else:
            log("   ⚠️ Impossibile generare PDF")
            pdf_path = None
    except Exception as pdf_error:
        log(f"   ⚠️ Errore PDF: {pdf_error}")
        pdf_path = None
    log("")
    
    # Prepara email
    log("5. Preparazione email...")
    final_result = bool(is_ok)
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
    
    log(f"   ✅ Subject: {subject}")
    log("")
    
    # Invia email
    log("6. Invio email...")
    sender = EmailSender("vandewiele-com.mail.protection.outlook.com", 25)
    sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")
    
    attachments = []
    if pdf_path and os.path.exists(pdf_path):
        attachments.append(pdf_path)
        log(f"   📎 Allegato: {os.path.basename(pdf_path)}")
    
    sender.send_email(
        to_email='gianluca.testa@vandewiele.com',
        subject=subject,
        body=html_body,
        is_html=True,
        attachments=attachments if attachments else None
    )
    
    log("   ✅ Email inviata con successo!")
    log("")
    
    cursor.close()
    conn.close()
    
    log("=" * 70)
    log("✅ TEST COMPLETATO CON SUCCESSO!")
    log("=" * 70)
    log("")
    log("📧 Controlla la casella email: gianluca.testa@vandewiele.com")
    log(f"📊 Dati validazione: FaiLogId={fai_log_id}, Order={order_number}")
    
except Exception as e:
    log("")
    log("=" * 70)
    log(f"❌ ERRORE: {e}")
    log("=" * 70)
    import traceback
    log(traceback.format_exc())

finally:
    output_file.close()
    print("\n✅ Output salvato in: test_fai_output.txt")
