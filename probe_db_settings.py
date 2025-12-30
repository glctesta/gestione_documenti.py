import pyodbc
from database_config import DatabaseConfig

def probe_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    queries = [
        "SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Sys_Pasqua%'",
        "SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Sys_Easter%'",
        "SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Sys_Religion%'",
        "SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Sys_Religione%'",
        "SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE 'Sys_%'"
    ]
    
    try:
        for q in queries:
            print(f"\nExecuting: {q}")
            cursor.execute(q)
            rows = cursor.fetchall()
            if not rows:
                print("No results.")
            for r in rows:
                print(f"[{r.atribute}] = {r.value}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    probe_settings()
