"""
Script per eseguire setup database FAI fails email
"""

import pyodbc
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

DB_CONN_STR = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=SRV-SQL2014;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

def setup_database():
    """Esegue setup database per FAI fails email"""
    try:
        logger.info("Connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        
        # 1. Verifica/Aggiungi campo IsAnalized
        logger.info("Verifica campo IsAnalized...")
        cursor.execute("""
            SELECT 1 
            FROM sys.columns 
            WHERE object_id = OBJECT_ID(N'[fai].[FaiLogs]') 
            AND name = 'IsAnalized'
        """)
        
        if cursor.fetchone() is None:
            logger.info("Aggiunta campo IsAnalized...")
            cursor.execute("""
                ALTER TABLE [fai].[FaiLogs]
                ADD IsAnalized BIT DEFAULT 0
            """)
            conn.commit()
            logger.info("✅ Campo IsAnalized aggiunto")
        else:
            logger.info("✅ Campo IsAnalized già esistente")
        
        # 2. Verifica/Aggiungi setting Sys_email_fai_fails
        logger.info("Verifica setting Sys_email_fai_fails...")
        cursor.execute("""
            SELECT 1 
            FROM [dbo].[Settings] 
            WHERE atribute = 'Sys_email_fai_fails'
        """)
        
        if cursor.fetchone() is None:
            logger.info("Aggiunta setting Sys_email_fai_fails...")
            cursor.execute("""
                INSERT INTO [dbo].[Settings] (atribute, [VALUE])
                VALUES ('Sys_email_fai_fails', 'gianluca.testa@vandewiele.com')
            """)
            conn.commit()
            logger.info("✅ Setting Sys_email_fai_fails aggiunto")
        else:
            logger.info("✅ Setting Sys_email_fai_fails già esistente")
        
        cursor.close()
        conn.close()
        
        logger.info("=" * 60)
        logger.info("✅ Setup database completato con successo!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Errore durante setup: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    setup_database()
