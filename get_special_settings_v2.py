import pyodbc
from database_config import DatabaseConfig

def get_special_settings():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    with open("special_settings.txt", "w", encoding="utf-8") as f:
        cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute IN ('Sys_eastern_data', 'Sys_Religione', 'Sys_Pasqua')")
        for r in cursor.fetchall():
            f.write(f"[{r.atribute}] = {r.value}\n")
    conn.close()

if __name__ == "__main__":
    get_special_settings()
