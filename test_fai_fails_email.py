"""
Script di test per verificare l'invio email FAI fails.
Invia email di test a gianluca.testa@vandewiele.com
"""

import sys
import os

# Aggiungi il percorso del progetto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from utils import send_fai_fails_notification
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Connection string
DB_CONN_STR = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=SRV-SQL2014;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

def test_fai_fails_email():
    """Test invio email FAI fails"""
    try:
        logger.info("Connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR)
        logger.info("✅ Connesso al database")
        
        # Temporaneamente modifica i destinatari per il test
        logger.info("Configurazione destinatari di test...")
        
        # Salva i destinatari originali
        cursor = conn.cursor()
        cursor.execute("""
            SELECT [VALUE] 
            FROM [Traceability_RS].[dbo].[Settings] 
            WHERE atribute = 'Sys_email_fai_fails'
        """)
        row = cursor.fetchone()
        original_cc = row[0] if row else None
        
        # Imposta destinatario di test (solo per CC, i TO vengono dalla query)
        cursor.execute("""
            UPDATE [Traceability_RS].[dbo].[Settings]
            SET [VALUE] = 'gianluca.testa@vandewiele.com'
            WHERE atribute = 'Sys_email_fai_fails'
        """)
        
        if cursor.rowcount == 0:
            # Setting non esiste, crealo
            cursor.execute("""
                INSERT INTO [Traceability_RS].[dbo].[Settings] (atribute, [VALUE])
                VALUES ('Sys_email_fai_fails', 'gianluca.testa@vandewiele.com')
            """)
        
        conn.commit()
        logger.info("✅ Destinatari configurati per test")
        
        # Invia email
        logger.info("Invio email di test...")
        success = send_fai_fails_notification(conn, logo_path="logo.png")
        
        if success:
            logger.info("✅ Email inviata con successo!")
        else:
            logger.warning("⚠️ Nessun FAI fail non analizzato trovato")
            logger.info("Creazione dati di test...")
            
            # Verifica se ci sono fails
            cursor.execute("""
                SELECT COUNT(*) 
                FROM [Traceability_RS].[fai].[FaiLogs]
                WHERE IsOk = 0 AND ISNULL(IsAnalized, 0) = 0
            """)
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info(f"Trovati {count} fails non analizzati")
                logger.info("Per testare l'email, è necessario avere almeno un record con:")
                logger.info("  - IsOk = 0")
                logger.info("  - IsAnalized = 0 (o NULL)")
            else:
                logger.info(f"Trovati {count} fails non analizzati, ma l'invio è fallito")
        
        # Ripristina destinatari originali se esistevano
        if original_cc:
            cursor.execute("""
                UPDATE [Traceability_RS].[dbo].[Settings]
                SET [VALUE] = ?
                WHERE atribute = 'Sys_email_fai_fails'
            """, original_cc)
            conn.commit()
            logger.info("✅ Destinatari originali ripristinati")
        
        cursor.close()
        conn.close()
        logger.info("✅ Test completato")
        
    except Exception as e:
        logger.error(f"❌ Errore durante il test: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("TEST INVIO EMAIL FAI FAILS")
    print("Destinatario: gianluca.testa@vandewiele.com")
    print("=" * 60)
    print()
    
    test_fai_fails_email()
    
    print()
    print("=" * 60)
    print("Test terminato. Controlla la tua casella email!")
    print("=" * 60)
