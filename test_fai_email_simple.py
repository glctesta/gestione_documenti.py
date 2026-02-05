"""
Script semplificato per test email FAI fails
Invia a: gianluca.testa@vandewiele.com
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from email_connector import EmailSender
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

DB_CONN_STR = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=SRV-SQL2014;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

def send_test_email():
    """Invia email di test"""
    try:
        logger.info("Connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        
        # Query statistiche FAI fails
        logger.info("Recupero statistiche FAI fails...")
        query_stats = """
        SELECT 
            l.Operator,
            COUNT(DISTINCT l.FaiLogId) as TotalFAI,
            SUM(CASE WHEN l.IsOk = 0 THEN 1 ELSE 0 END) as TotalFails,
            CAST(SUM(CASE WHEN l.IsOk = 0 THEN 1 ELSE 0 END) * 100.0 / 
                 NULLIF(COUNT(DISTINCT l.FaiLogId), 0) AS DECIMAL(5,2)) as FailureRate
        FROM [Traceability_RS].[fai].[FaiLogs] l
        WHERE ISNULL(l.IsAnalized, 0) = 0 AND l.IsOk = 0
        GROUP BY l.Operator
        ORDER BY FailureRate DESC
        """
        
        cursor.execute(query_stats)
        statistics = cursor.fetchall()
        
        if not statistics:
            logger.warning("⚠️ Nessun FAI fail non analizzato trovato")
            logger.info("Per testare, crea almeno un record con IsOk=0 e IsAnalized=0")
            return
        
        logger.info(f"✅ Trovati {len(statistics)} operatori con fails")
        
        # Conta totale fails
        cursor.execute("""
            SELECT COUNT(*) 
            FROM [Traceability_RS].[fai].[FaiLogs]
            WHERE IsOk = 0 AND ISNULL(IsAnalized, 0) = 0
        """)
        num_fails = cursor.fetchone()[0]
        
        logger.info(f"✅ Totale fails non analizzati: {num_fails}")
        
        # Genera tabella HTML
        table_rows = ""
        for stat in statistics:
            operator = stat.Operator or 'N/A'
            total_fai = stat.TotalFAI or 0
            total_fails = stat.TotalFails or 0
            failure_rate = stat.FailureRate or 0.0
            
            if failure_rate < 5.0:
                row_color = "#d4edda"
            elif failure_rate < 15.0:
                row_color = "#fff3cd"
            else:
                row_color = "#f8d7da"
            
            table_rows += f"""
            <tr style="background-color: {row_color};">
                <td style="padding: 10px; border: 1px solid #ddd;">{operator}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{total_fai}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{total_fails}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{failure_rate:.2f}%</td>
            </tr>
            """
        
        # Email HTML
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="margin-bottom: 20px;">
                <img src="cid:company_logo" alt="Company Logo" width="120"/>
            </div>
            
            <h2 style="color: #366092;">Raport Automat - Defecte FAI Nevalidate (TEST)</h2>
            
            <p>Bună ziua,</p>
            
            <p>Aceasta este o <strong>EMAIL DE TEST</strong> pentru sistemul automat de notificare FAI fails.</p>
            
            <p>În legătură cu declarațiile FAI obligatorii, după un control automat asupra calității 
            fișelor declarate Valide pentru confirmarea începerii producției, a rezultat că 
            <strong>{num_fails} fișe</strong> au fost marcate ca <strong>FAIL</strong> după 
            declarația de validare.</p>
            
            <h3 style="color: #366092;">Statistici pe Operator:</h3>
            
            <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                <thead>
                    <tr style="background-color: #366092; color: white;">
                        <th style="padding: 10px; border: 1px solid #ddd;">Operator</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Total FAI</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Total Defecte</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Procent Defecte (%)</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;"/>
            
            <p style="font-weight: bold; color: #d9534f;">Vă recomandăm să acordați atenție maximă 
            în faza de validare a liniilor.</p>
            
            <p>Acest control este fundamental pentru a evita reparații inutile și, în consecință, 
            risipa de resurse și, evident, de bani.</p>
            
            <p>Responsabilitatea revine șefilor de linie și, în consecință, șefilor de tură.</p>
            
            <p style="font-style: italic;">În fiecare lună va fi întocmit un raport rezumativ cu 
            defectele de acest tip care vor influența evaluarea celor responsabili.</p>
            
            <br/>
            <p>Mulțumim,<br/>
            <strong>Sistem de Trasabilitate</strong></p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;"/>
            <p style="color: #999; font-size: 12px;">
            <strong>NOTA:</strong> Aceasta este o email de test. În producție, emailul va fi trimis automat 
            în fiecare zi la ora 07:00 către șefii de linie și tură.
            </p>
        </body>
        </html>
        """
        
        # Invia email
        logger.info("Invio email di test...")
        sender = EmailSender()
        sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")
        
        attachments = []
        if os.path.exists("logo.png"):
            attachments.append(('inline', 'logo.png', 'company_logo'))
        
        sender.send_email(
            to_email='gianluca.testa@vandewiele.com',
            subject="[TEST] Raport Automat - Defecte FAI Nevalidate",
            body=html_body,
            is_html=True,
            attachments=attachments,
            cc_emails=None
        )
        
        logger.info("✅ Email di test inviata con successo!")
        logger.info("📧 Destinatario: gianluca.testa@vandewiele.com")
        logger.info("📊 Statistiche incluse: {} operatori, {} fails totali".format(len(statistics), num_fails))
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Errore: {e}", exc_info=True)

if __name__ == "__main__":
    print("=" * 70)
    print("TEST INVIO EMAIL FAI FAILS")
    print("Destinatario: gianluca.testa@vandewiele.com")
    print("=" * 70)
    print()
    
    send_test_email()
    
    print()
    print("=" * 70)
    print("Controlla la tua casella email!")
    print("=" * 70)
