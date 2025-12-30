import pyodbc
from database_config import DatabaseConfig

def print_holidays():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT TipSarbatoare, Religion, SarbatoareDate FROM Employee.dbo.Sarbatorilor WHERE Year(SarbatoareDate) IN (2024, 2025, 2026)")
    for r in cursor.fetchall():
        print(f"Type: {r[0]}, Religion: {r[1]}, Date: {r[2]}")
    conn.close()

if __name__ == "__main__":
    print_holidays()
