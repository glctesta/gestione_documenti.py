"""
Script di debug per verificare invio email FAI fails
Con logging dettagliato
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from email_connector import EmailSender
import logging

# Logging molto dettagliato
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

DB_CONN_STR = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=SRV-SQL2014;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

def debug_email():
    """Debug invio email"""
    try:
        print("\n" + "="*70)
        print("DEBUG EMAIL FAI FAILS")
        print("="*70 + "\n")
        
        # 1. Test connessione database
        print("1️⃣ Test connessione database...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        print("   ✅ Connesso al database\n")
        
        # 2. Verifica fails non analizzati
        print("2️⃣ Verifica fails non analizzati...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM [Traceability_RS].[fai].[FaiLogs]
            WHERE IsOk = 0 AND ISNULL(IsAnalized, 0) = 0
        """)
        count = cursor.fetchone()[0]
        print(f"   📊 Trovati {count} fails non analizzati\n")
        
        if count == 0:
            print("   ⚠️ PROBLEMA: Nessun fail non analizzato!")
            print("   💡 Soluzione: Imposta IsAnalized=0 su almeno un record con IsOk=0\n")
            
            # Mostra alcuni fails esistenti
            cursor.execute("""
                SELECT TOP 5 FaiLogId, Operator, IsOk, ISNULL(IsAnalized, 0) as IsAnalized
                FROM [Traceability_RS].[fai].[FaiLogs]
                WHERE IsOk = 0
                ORDER BY DateIn DESC
            """)
            fails = cursor.fetchall()
            if fails:
                print("   📋 Ultimi 5 fails (IsOk=0):")
                for f in fails:
                    print(f"      - FaiLogId: {f.FaiLogId}, Operator: {f.Operator}, IsAnalized: {f.IsAnalized}")
                print()
            
            return
        
        # 3. Test configurazione email
        print("3️⃣ Test configurazione email...")
        sender = EmailSender()
        print("   ✅ EmailSender creato")
        
        sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")
        print("   ✅ Credenziali salvate")
        
        from_email = sender.load_credentials()
        print(f"   📧 Email mittente: {from_email}\n")
        
        # 4. Test invio email semplice (senza HTML)
        print("4️⃣ Test invio email semplice...")
        
        try:
            sender.send_email(
                to_email='gianluca.testa@vandewiele.com',
                subject='[TEST DEBUG] Email semplice FAI fails',
                body=f'Questo è un test di debug.\n\nTrovati {count} fails non analizzati.\n\nSe ricevi questa email, il sistema funziona!',
                is_html=False
            )
            print("   ✅ Email semplice inviata!\n")
        except Exception as e:
            print(f"   ❌ ERRORE invio email: {e}\n")
            logger.error("Errore invio email", exc_info=True)
            return
        
        # 5. Test invio email HTML con logo
        print("5️⃣ Test invio email HTML con logo...")
        
        html_body = """
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #366092;">Test Email HTML</h2>
            <p>Questa è una email di test in formato HTML.</p>
            <p>Se vedi questo messaggio formattato, l'HTML funziona!</p>
        </body>
        </html>
        """
        
        attachments = []
        if os.path.exists("logo.png"):
            attachments.append(('inline', 'logo.png', 'company_logo'))
            print("   📎 Logo trovato e allegato")
        else:
            print("   ⚠️ Logo non trovato (logo.png)")
        
        try:
            sender.send_email(
                to_email='gianluca.testa@vandewiele.com',
                subject='[TEST DEBUG] Email HTML FAI fails',
                body=html_body,
                is_html=True,
                attachments=attachments
            )
            print("   ✅ Email HTML inviata!\n")
        except Exception as e:
            print(f"   ❌ ERRORE invio email HTML: {e}\n")
            logger.error("Errore invio email HTML", exc_info=True)
            return
        
        cursor.close()
        conn.close()
        
        print("="*70)
        print("✅ DEBUG COMPLETATO")
        print("="*70)
        print("\n📧 Controlla la tua email: gianluca.testa@vandewiele.com")
        print("   Dovresti aver ricevuto 2 email:")
        print("   1. [TEST DEBUG] Email semplice FAI fails")
        print("   2. [TEST DEBUG] Email HTML FAI fails\n")
        
    except Exception as e:
        print(f"\n❌ ERRORE CRITICO: {e}\n")
        logger.error("Errore critico", exc_info=True)

if __name__ == "__main__":
    debug_email()
