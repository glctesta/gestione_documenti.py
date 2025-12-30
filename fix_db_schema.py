import pyodbc
from database_config import DatabaseConfig

def fix_schema():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("Altering ResetServices.dbo.TbUserKeyLogs.Password to VARBINARY(MAX)...")
        cursor.execute("ALTER TABLE ResetServices.dbo.TbUserKeyLogs ALTER COLUMN Password VARBINARY(MAX)")
        
        print("Altering ResetServices.dbo.TbUserKey.Pass to VARBINARY(MAX)...")
        cursor.execute("ALTER TABLE ResetServices.dbo.TbUserKey ALTER COLUMN Pass VARBINARY(MAX)")
        
        conn.commit()
        print("Schema fix successful!")
    except Exception as e:
        conn.rollback()
        print(f"Error fixing schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_schema()
