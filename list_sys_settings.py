import pyodbc
from database_config import DatabaseConfig

def list_all_sys_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("All Sys_ settings in traceability_rs.dbo.Settings:")
        cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE 'Sys_%' ORDER BY atribute")
        rows = cursor.fetchall()
        for r in rows:
            print(f"[{r.atribute}] = {r.value}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_all_sys_settings()
