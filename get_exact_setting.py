import pyodbc
from database_config import DatabaseConfig

def get_exact_setting():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = 'Sys_eastern_data'")
    row = cursor.fetchone()
    if row:
        print("--- Sys_eastern_data ---")
        print(row[0])
        print("------------------------")
    else:
        print("Sys_eastern_data not found")
        
    cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = 'Sys_Religion'")
    row = cursor.fetchone()
    if row:
        print("--- Sys_Religion ---")
        print(row[0])
        print("------------------------")
    else:
        print("Sys_Religion not found")

    conn.close()

if __name__ == "__main__":
    get_exact_setting()
