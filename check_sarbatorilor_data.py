import pyodbc
from database_config import DatabaseConfig

def check_table_content():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT TOP 50 * FROM Employee.dbo.Sarbatorilor")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows.")
        for r in rows:
            print(r)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_table_content()
