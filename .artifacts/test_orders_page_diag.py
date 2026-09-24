# -*- coding: utf-8 -*-
"""Diagnostica pagina /print/orders sul server deployato:
emette un token nel DB, carica la pagina (consumando il token e creando la
sessione), poi chiama la search API con la sessione."""
import json
import urllib.request
import http.cookiejar
import pyodbc
from config_manager import ConfigManager

BASE = "http://192.168.10.72:5015"
TOKEN = "diagtest00000000000000000000001"

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
conn_str = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
            f"UID={creds['username']};PWD={creds['password']};TrustServerCertificate=Yes")
cnxn = pyodbc.connect(conn_str, autocommit=True)
cur = cnxn.cursor()
cur.execute(
    """INSERT INTO Traceability_RS.ind.PrintLabelWebSessions
       (Token, UserId, UserName, Permission, Page, IssuedAt, ExpiresAt)
       VALUES (?, 1, 'DIAG', 'gestione_stampa_etichette_produzione', 'print_orders',
               GETDATE(), DATEADD(MINUTE, 5, GETDATE()))""", (TOKEN,))
cnxn.close()
print("Token inserito")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Carica la pagina (consuma il token, crea la sessione)
try:
    r = opener.open(f"{BASE}/print/orders?token={TOKEN}&lang=it", timeout=30)
    html = r.read().decode('utf-8', 'replace')
    print(f"PAGE: HTTP {r.status}, {len(html)} bytes")
    print("  contiene fix 'o.IDOrder'?:", "o.IDOrder" in html)
    print("  contiene BUG  'o.OrderID'?:", "o.OrderID" in html)
    print("  contiene 'OrderNumber'?:", "OrderNumber" in html)
except Exception as e:
    print("PAGE ERRORE:", e)

# 2. Search API con la sessione
try:
    r = opener.open(f"{BASE}/print/api/orders/search?q=999", timeout=60)
    body = r.read().decode('utf-8', 'replace')
    print(f"SEARCH: HTTP {r.status}")
    data = json.loads(body)
    print(f"  righe: {len(data)}")
    for row in data[:3]:
        print("  ", row)
except urllib.error.HTTPError as e:
    print(f"SEARCH HTTP {e.code}:", e.read().decode('utf-8', 'replace')[:300])
except Exception as e:
    print("SEARCH ERRORE:", e)
