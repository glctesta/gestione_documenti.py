# -*- coding: utf-8 -*-
"""
test_smtp_diretto.py
====================
Test SMTP diretto con output verboso (smtplib.set_debuglevel(1)).
Mostra ogni risposta del server SMTP cosi' vediamo esattamente cosa succede.

Esegui con:
    .venv\\Scripts\\python.exe test_smtp_diretto.py
"""
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Configurazione ────────────────────────────────────────────────────────────
SMTP_HOST    = "vandewiele-com.mail.protection.outlook.com"
SMTP_PORT    = 25
FROM_EMAIL   = "Accounting@Eutron.it"

# Legge i destinatari da Sys_verifica_linea per il test reale
import pyodbc
from config_manager import ConfigManager
from utils import get_email_recipients

try:
    config_mgr = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc")
    creds = config_mgr.load_config()
    conn_str = (
        f"DRIVER={creds['driver']};SERVER={creds['server']};"
        f"DATABASE={creds['database']};UID={creds['username']};PWD={creds['password']};"
        "MARS_Connection=Yes;TrustServerCertificate=Yes"
    )
    conn = pyodbc.connect(conn_str)
    recipients_list = get_email_recipients(conn, "Sys_verifica_linea")
    conn.close()
    print(f"Destinatari da Sys_verifica_linea: {recipients_list}")
except Exception as e:
    print(f"ATTENZIONE: impossibile leggere destinatari dal DB: {e}")
    print("Inserisci manualmente un indirizzo email di test:")
    recipients_list = ["gianluca.testa@vandewiele.com"]

TO_EMAIL = ", ".join(recipients_list)
print(f"TO_EMAIL = '{TO_EMAIL}'\n")

# ── Costruisce il messaggio ───────────────────────────────────────────────────
msg = MIMEMultipart()
msg["From"]    = FROM_EMAIL
msg["To"]      = TO_EMAIL
msg["Subject"] = f"[SMTP TEST DIRETTO] {datetime.now().strftime('%H:%M:%S')}"
msg.attach(MIMEText(
    "<html><body><p>Test SMTP diretto - se ricevi questa email il relay funziona!</p>"
    f"<p>Inviata alle {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p></body></html>",
    "html"
))

# ── Invio con debug SMTP verboso ──────────────────────────────────────────────
print("=" * 70)
print(f"Connessione a {SMTP_HOST}:{SMTP_PORT} ...")
print("(Il debug verboso mostra ogni risposta del server)")
print("=" * 70 + "\n")

try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
    server.set_debuglevel(2)   # <-- verboso: stampa ogni riga scambiata

    print("\n--- EHLO ---")
    code, msg_ehlo = server.ehlo()
    print(f"    Risposta EHLO: {code} {msg_ehlo.decode()}\n")

    # Tenta STARTTLS se disponibile
    if server.has_extn("starttls"):
        print("--- STARTTLS disponibile, avvio TLS ---")
        server.starttls()
        server.ehlo()

    print(f"--- MAIL FROM: {FROM_EMAIL} ---")
    print(f"--- RCPT TO: {recipients_list} ---")

    result = server.sendmail(FROM_EMAIL, recipients_list, msg.as_string())

    print(f"\n--- RISULTATO sendmail ---")
    if result:
        print(f"ATTENZIONE: alcuni destinatari rifiutati: {result}")
    else:
        print("OK - nessun destinatario rifiutato (result={{}})  -> email accettata dal relay")

    server.quit()
    print("\nSMTP: connessione chiusa correttamente")
    print("\nRISULTATO FINALE: il relay ha accettato il messaggio.")
    print("Se l'email non arriva, il problema e' sul relay/spam/filtri del destinatario,")
    print("NON nel codice Python.")

except smtplib.SMTPConnectError as e:
    print(f"\nERRORE: impossibile connettersi a {SMTP_HOST}:{SMTP_PORT}")
    print(f"        {e}")
    print("        -> Verifica firewall / VPN / accesso di rete al server SMTP")

except smtplib.SMTPSenderRefused as e:
    print(f"\nERRORE: mittente rifiutato: {e}")
    print(f"        Il relay non accetta email da '{FROM_EMAIL}' da questo host.")

except smtplib.SMTPRecipientsRefused as e:
    print(f"\nERRORE: destinatari rifiutati: {e}")

except smtplib.SMTPException as e:
    print(f"\nERRORE SMTP generico: {e}")
    import traceback; traceback.print_exc()

except OSError as e:
    print(f"\nERRORE rete/timeout: {e}")
    print("        -> Verifica che la porta 25 sia aperta verso il relay")
    import traceback; traceback.print_exc()
