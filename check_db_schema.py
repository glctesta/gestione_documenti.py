import pyodbc
from database_config import DatabaseConfig

def check_schema():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    with open("schema_results.txt", "w") as f:
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        f.write(f"Current DB: {db_name}\n\n")
        
        f.write("Tables in ResetServices.dbo schema:\n")
        cursor.execute("SELECT TABLE_NAME FROM ResetServices.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")
        for r in cursor.fetchall():
            f.write(f"- {r.TABLE_NAME}\n")
        f.write("\n")

        # Try looking into ResetServices database
        dbs_to_check = ['ResetServices']
        tables_to_check = ['TbUserKey', 'TbUserKeyLogs', 'TbUserKaylogs', 'tbuserkey']
        
        for db in dbs_to_check:
            f.write(f"--- Checking DB: {db} ---\n")
            for table in tables_to_check:
                f.write(f"Checking columns for {db}.dbo.{table}:\n")
                try:
                    cursor.execute(f"""
                        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
                        FROM {db}.INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = '{table}'
                    """)
                    results = cursor.fetchall()
                    if not results:
                        f.write(f"  No columns found for {table} in {db}\n")
                    for r in results:
                        f.write(f"  Col: {r.COLUMN_NAME}, Type: {r.DATA_TYPE}, MaxLen: {r.CHARACTER_MAXIMUM_LENGTH}\n")
                except Exception as e:
                    f.write(f"  Error checking {db}: {e}\n")
                f.write("\n")
    
    conn.close()

if __name__ == "__main__":
    check_schema()
