import pyodbc
from database_config import DatabaseConfig

def check_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Relig%'")
    rows = cursor.fetchall()
    print("Settings with 'Relig':")
    for r in rows:
        print(f"[{r[0]}] = {r[1]}")
    
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Pasqua%'")
    rows = cursor.fetchall()
    print("\nSettings with 'Pasqua':")
    for r in rows:
        print(f"[{r[0]}] = {r[1]}")
    
    conn.close()

if __name__ == "__main__":
    check_settings()
