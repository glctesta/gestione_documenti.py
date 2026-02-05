"""
Script per verificare schema tabella FaiLogs
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

def check_table_schema():
    """Verifica schema tabella FaiLogs"""
    try:
        logger.info("Connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        
        # Cerca la tabella FaiLogs
        logger.info("Ricerca tabella FaiLogs...")
        cursor.execute("""
            SELECT 
                SCHEMA_NAME(schema_id) as SchemaName,
                name as TableName
            FROM sys.tables
            WHERE name LIKE '%FaiLog%'
        """)
        
        tables = cursor.fetchall()
        if tables:
            logger.info("Tabelle trovate:")
            for table in tables:
                logger.info(f"  - [{table.SchemaName}].[{table.TableName}]")
                
                # Mostra colonne
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = '{table.SchemaName}'
                    AND TABLE_NAME = '{table.TableName}'
                    ORDER BY ORDINAL_POSITION
                """)
                
                columns = cursor.fetchall()
                logger.info(f"    Colonne ({len(columns)}):")
                for col in columns[:10]:  # Mostra prime 10
                    logger.info(f"      - {col.column_name} ({col.data_type})")
                
                if len(columns) > 10:
                    logger.info(f"      ... e altre {len(columns) - 10} colonne")
        else:
            logger.warning("Nessuna tabella FaiLogs trovata!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Errore: {e}", exc_info=True)

if __name__ == "__main__":
    check_table_schema()
