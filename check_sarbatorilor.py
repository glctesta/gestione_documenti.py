import pyodbc
from database_config import DatabaseConfig

def check_sarbatorilor():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("Schema for Employee.dbo.Sarbatorilor:")
        cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM Employee.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Sarbatorilor'")
        for r in cursor.fetchall():
            print(f"Col: {r.COLUMN_NAME}, Type: {r.DATA_TYPE}")
            
        print("\nData for year 2025:")
        cursor.execute("SELECT * FROM Employee.dbo.Sarbatorilor WHERE Year(SarbatoareDate) = 2025")
        for r in cursor.fetchall():
            print(r)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_sarbatorilor()
