import pyodbc
from database_config import DatabaseConfig

def get_eastern_data():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = 'Sys_eastern_data'")
        val = cursor.fetchone()[0]
        print(f"Sys_eastern_data: {val}")
        
        cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = 'Sys_Religione'")
        val2 = cursor.fetchone()
        print(f"Sys_Religione: {val2[0] if val2 else 'NOT FOUND'}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    get_eastern_data()
