import pyodbc
from database_config import DatabaseConfig

def list_seasonal_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    keys_to_search = ['natale', 'year', 'pasqua', 'easter', 'religione', 'religion']
    
    try:
        print("Searching seasonal settings:")
        for key in keys_to_search:
            cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE ?", f"%{key}%")
            for r in cursor.fetchall():
                print(f"Key: {r.atribute}, Value: {r.value}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_seasonal_settings()
