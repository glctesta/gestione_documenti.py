import pyodbc
from database_config import DatabaseConfig

def find_relig_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%relig%'")
    rows = cursor.fetchall()
    
    if not rows:
        print("No 'relig' settings found.")
    else:
        for r in rows:
            print(f"[{r[0]}] = {r[1]}")
    conn.close()

if __name__ == "__main__":
    find_relig_settings()
