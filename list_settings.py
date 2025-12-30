import pyodbc
from database_config import DatabaseConfig

def list_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("Settings in traceability_rs.dbo.Settings:")
        cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings ORDER BY atribute")
        for r in cursor.fetchall():
            print(f"Key: {r.atribute}, Value: {r.value}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_settings()
