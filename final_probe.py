import pyodbc
from database_config import DatabaseConfig

def probe():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    keys = [
        'Sys_natale', 'Sys_natale_preallert', 'Sys_natale_postallert',
        'Sys_HappyNewYear', 'Sys_HappyNewYear_Preallert', 'Sys_HappyNewYear_PostAllert',
        'Sys_Pasqua', 'Sys_Pasqua_preallert', 'Sys_Pasqua_postallert',
        'Sys_Easter', 'Sys_Easter_preallert', 'Sys_Easter_postallert',
        'Sys_Religion', 'Sys_Religione',
        'Sys_eastern_data'
    ]
    
    print("PROBE RESULTS:")
    for key in keys:
        cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = ?", key)
        row = cursor.fetchone()
        if row:
            print(f"{key} = {row[0]}")
        else:
            print(f"{key} = NOT FOUND")
    conn.close()

if __name__ == "__main__":
    probe()
