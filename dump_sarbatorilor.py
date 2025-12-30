import pyodbc
from database_config import DatabaseConfig

def dump_sarbatorilor():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        print("Rows from Employee.dbo.Sarbatorilor for 2024-2025:")
        cursor.execute("SELECT * FROM Employee.dbo.Sarbatorilor WHERE Year(SarbatoareDate) IN (2024, 2025)")
        cols = [column[0] for column in cursor.description]
        print(f"Columns: {cols}")
        for r in cursor.fetchall():
            print(dict(zip(cols, r)))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    dump_sarbatorilor()
