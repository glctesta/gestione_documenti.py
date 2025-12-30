import pyodbc
from database_config import DatabaseConfig

def probe_easter():
    config = DatabaseConfig()
    conn_str = config.get_connection_string()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # 1. Get Sys_eastern_data query
    cursor.execute("SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = 'Sys_eastern_data'")
    query = cursor.fetchone()
    if query:
        print(f"Query found: {query[0]}")
    else:
        print("Query Sys_eastern_data NOT found.")

    # 2. Look for religion and holiday type settings
    # Search for anything that could be religion or holiday type
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Religion%' OR atribute LIKE '%Sarbatoare%'")
    rows = cursor.fetchall()
    print("\nReligion/Sarbatoare Settings:")
    for r in rows:
        print(f"[{r.atribute}] = {r.value}")

    # 3. Look for Easter images
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%Pasqua%' OR atribute LIKE '%Easter%'")
    rows = cursor.fetchall()
    print("\nEaster Images Settings:")
    for r in rows:
        print(f"[{r.atribute}] = {r.value}")

    # 4. Look for all seasonal pre/post values
    cursor.execute("SELECT atribute, [value] FROM traceability_rs.dbo.Settings WHERE atribute LIKE '%preallert%' OR atribute LIKE '%postallert%'")
    rows = cursor.fetchall()
    print("\nAlert Window Settings:")
    for r in rows:
        print(f"[{r.atribute}] = {r.value}")

    conn.close()

if __name__ == "__main__":
    probe_easter()
