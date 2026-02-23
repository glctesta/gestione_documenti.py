"""
test_fai_validation_email.py
============================
Script di test end-to-end del flusso email FAI di validazione linea.

Replica esattamente la logica di LineValidationWindow._save_validation:
  1. Legge l'ultimo record da fai.FaiLogs
  2. Genera il PDF con generate_fai_report
  3. Recupera i destinatari da Settings (Sys_verifica_linea)
  4. Invia l'email con utils.send_email

Esegui con:
    .venv\\Scripts\\python.exe test_fai_validation_email.py
"""

import sys
import os
import logging
import tempfile

# Forza UTF-8 per evitare UnicodeEncodeError su Windows
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Aggiunge la directory del progetto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("test_fai_email")

# ── Intestazione ──────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  TEST FAI VALIDATION EMAIL")
print("=" * 70 + "\n")

# ── 1. Credenziali DB ─────────────────────────────────────────────────────────
try:
    print("1. Carico credenziali da db_config.enc ...")
    from config_manager import ConfigManager
    config_mgr = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc")
    creds = config_mgr.load_config()

    DB_CONN_STR = (
        f"DRIVER={creds['driver']};"
        f"SERVER={creds['server']};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']};"
        "MARS_Connection=Yes;TrustServerCertificate=Yes"
    )
    print(f"   OK - server: {creds['server']}, db: {creds['database']}\n")
except Exception as e:
    print(f"   ATTENZIONE - impossibile caricare db_config.enc: {e}")
    print("   Uso Trusted_Connection di fallback (da debug_fai_email.py)\n")
    DB_CONN_STR = (
        "DRIVER={SQL Server Native Client 11.0};"
        "SERVER=SRV-SQL2014;"
        "DATABASE=Traceability_RS;"
        "Trusted_Connection=yes;"
    )

# ── 2. Connessione ────────────────────────────────────────────────────────────
try:
    import pyodbc
    print("2. Connessione al database ...")
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    print("   OK - connesso!\n")
except Exception as e:
    print(f"   ERRORE connessione: {e}")
    sys.exit(1)

# ── 3. Ultimo record FaiLogs ──────────────────────────────────────────────────
try:
    print("3. Recupero ultimo record da fai.FaiLogs ...")
    cursor.execute("""
        SELECT TOP 1
            l.FaiLogId,
            l.OrderId,
            l.IsOk,
            l.Operator,
            l.DateIn,
            o.OrderNumber,
            p.ProductCode,
            p.ProductName
        FROM Traceability_RS.fai.FaiLogs l
        LEFT JOIN Traceability_RS.dbo.orders o ON l.OrderId = o.IDOrder
        LEFT JOIN Traceability_RS.dbo.Products p ON o.IDProduct = p.IDProduct
        WHERE l.DateOut IS NULL
        ORDER BY l.FaiLogId DESC
    """)
    row = cursor.fetchone()

    if not row:
        print("   ERRORE: nessun record in fai.FaiLogs!")
        sys.exit(1)

    fai_log_id   = row.FaiLogId
    is_ok        = row.IsOk
    operator     = row.Operator or "N/A"
    date_in      = row.DateIn
    order_number = row.OrderNumber or "N/A"
    product_code = row.ProductCode or "N/A"
    product_name = (row.ProductName or row.ProductCode or "N/A")

    print(f"   FaiLogId   : {fai_log_id}")
    print(f"   Operator   : {operator}")
    print(f"   DateIn     : {date_in}")
    print(f"   OrderNumber: {order_number}")
    print(f"   ProductCode: {product_code}")
    print(f"   IsOk       : {is_ok}\n")

except Exception as e:
    print(f"   ERRORE query FaiLogs: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)

# ── 4. Genera PDF ─────────────────────────────────────────────────────────────
pdf_path = None
try:
    print("4. Generazione PDF con generate_fai_report ...")

    class FakeDB:
        def __init__(self, connection, cur):
            self.conn   = connection
            self.cursor = cur

    fake_db  = FakeDB(conn, cursor)
    tmp_path = os.path.join(tempfile.gettempdir(), f"TEST_FAI_{fai_log_id}.pdf")

    from fai_report_generator import generate_fai_report
    ok = generate_fai_report(fai_log_id, fake_db, tmp_path)

    if ok and os.path.exists(tmp_path):
        size_kb  = os.path.getsize(tmp_path) / 1024
        pdf_path = tmp_path
        print(f"   OK - PDF generato: {pdf_path} ({size_kb:.1f} KB)\n")
    else:
        print("   ATTENZIONE: generate_fai_report ha restituito False.")
        print("   L'email verra' inviata SENZA allegato PDF.\n")

except Exception as e:
    print(f"   ERRORE generazione PDF: {e}")
    import traceback; traceback.print_exc()
    print("   L'email verra' inviata SENZA allegato PDF.\n")

# ── 5. Destinatari ────────────────────────────────────────────────────────────
try:
    print("5. Lettura destinatari da Settings (Sys_verifica_linea) ...")
    from utils import get_email_recipients
    recipients = get_email_recipients(conn, "Sys_verifica_linea")

    if recipients:
        print(f"   OK - destinatari trovati: {recipients}\n")
    else:
        print("   ERRORE: nessun destinatario per 'Sys_verifica_linea'!")
        # Ricerca diagnostica
        cursor.execute("""
            SELECT atribute, [VALUE]
            FROM dbo.settings
            WHERE atribute LIKE '%verifica%'
               OR atribute LIKE '%linea%'
               OR atribute LIKE '%email%'
        """)
        rows = cursor.fetchall()
        if rows:
            print("   Voci trovate con la ricerca LIKE '%verifica%' OR '%linea%' OR '%email%':")
            for r in rows:
                print(f"      atribute='{r[0]}', VALUE='{r[1]}'")
        else:
            print("   Nessuna voce trovata con i pattern di ricerca.")
        sys.exit(1)

except Exception as e:
    print(f"   ERRORE lettura destinatari: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)

# ── 6. Invia email ────────────────────────────────────────────────────────────
try:
    print("6. Invio email ...")
    from utils import send_email
    from datetime import datetime

    final_result  = bool(is_ok)
    result_label  = "PASSED" if final_result else "FAILED"
    result_icon   = "OK"     if final_result else "FAIL"
    result_color  = "green"  if final_result else "red"

    subject = f"[TEST] FAI Validation Report - {product_name} - Order {order_number} - {result_label}"

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ background-color: #003366; color: white; padding: 20px; }}
            .content {{ padding: 20px; }}
            .banner {{ background:#fffbe6; border:1px solid #f59e0b; padding:10px;
                       border-radius:4px; margin-bottom:16px; font-size:13px; color:#92400e; }}
            .result {{
                font-size: 24px; font-weight: bold;
                color: {result_color};
                padding: 10px; border: 2px solid {result_color};
                display: inline-block; margin: 10px 0;
            }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            td {{ padding: 8px; border: 1px solid #ddd; }}
            td:first-child {{ font-weight: bold; background: #f0f0f0; width: 30%; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>FAI (First Article Inspection) Validation Report</h2>
        </div>
        <div class="content">
            <div class="banner">
                ATTENZIONE: Questa e' una email di TEST generata dallo script
                test_fai_validation_email.py - non da una vera validazione.
            </div>
            <div class="result">Risultato Finale: {result_label} {result_icon}</div>
            <table>
                <tr><td>Product:</td>        <td><strong>{product_name}</strong></td></tr>
                <tr><td>Order Number:</td>   <td><strong>{order_number}</strong></td></tr>
                <tr><td>Validation Date:</td><td>{datetime.now().strftime('%d/%m/%Y %H:%M')}</td></tr>
                <tr><td>Operator:</td>       <td>{operator}</td></tr>
                <tr><td>FAI Log ID:</td>     <td>{fai_log_id}</td></tr>
            </table>
            <p>Il report FAI completo e' allegato a questa email in formato PDF.</p>
            <p style="color:#666; font-size:12px; margin-top:30px;">
                Email automatica del sistema di tracciabilita'.<br>
                Per domande contattare il reparto qualita'.
            </p>
        </div>
    </body>
    </html>
    """

    attachments = []
    if pdf_path and os.path.exists(pdf_path):
        attachments.append(pdf_path)
        print(f"   Allegato: {pdf_path}")
    else:
        print("   Nessun allegato PDF disponibile")

    send_email(
        recipients=recipients,
        subject=subject,
        body=html_body,
        is_html=True,
        attachments=attachments if attachments else None
    )

    print(f"\n   OK - email inviata a: {', '.join(recipients)}")

except Exception as e:
    print(f"\n   ERRORE invio email: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)

finally:
    try:
        cursor.close()
        conn.close()
    except Exception:
        pass

print("\n" + "=" * 70)
print("  TEST COMPLETATO - controlla la casella dei destinatari")
print("=" * 70 + "\n")
