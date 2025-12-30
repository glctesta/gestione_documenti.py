import pyodbc
from database_config import DatabaseConfig

def check_userkey_columns():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Try different schemas/databases just in case
    queries = [
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TbUserKey'",
        "SELECT COLUMN_NAME FROM ResetServices.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TbUserKey'",
        "SELECT COLUMN_NAME FROM Traceability_RS.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TbUserKey'"
    ]
    
    for q in queries:
        try:
            print(f"Querying: {q}")
            cursor.execute(q)
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r[0]}")
            else:
                print("  No columns found for this query.")
        except Exception as e:
            print(f"  Error: {e}")
    conn.close()

if __name__ == "__main__":
    check_userkey_columns()
