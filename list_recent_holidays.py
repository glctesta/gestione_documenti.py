import pyodbc
from database_config import DatabaseConfig

def list_recent_holidays():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("Holidays for 2024-2026:")
        cursor.execute("SELECT * FROM Employee.dbo.Sarbatorilor WHERE Year(SarbatoareDate) IN (2024, 2025, 2026)")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_recent_holidays()
