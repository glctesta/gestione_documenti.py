"""Quick test: invia solo la email Global NPI a gtesta@gmail.com con il nuovo layout."""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=roghipsql01.vandewiele.local\\emsreset;"
    "DATABASE=Traceability_rs;"
    "UID=emsreset;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya"
)
TEST_EMAIL = "gtesta@gmail.com"

params = urllib.parse.quote_plus(conn_str)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}",
    poolclass=QueuePool, pool_size=5, max_overflow=10,
    pool_recycle=3600, pool_pre_ping=True, pool_timeout=30, echo=False)
with engine.connect() as c: c.execute(text("SELECT 1"))
print("DB OK")

from npi.npi_manager import GestoreNPI
from npi.npi_auto_notifications import NpiAutoNotificationService
from utils import send_email

svc = NpiAutoNotificationService(GestoreNPI(engine=engine))
stats = svc._collect_global_npi_stats()
logo_path = svc._resolve_logo_path()
logo_html = '<img src="cid:company_logo" style="max-width:150px;height:auto;" alt="Logo">' if logo_path else ""
html = svc._build_global_view_email_html(stats, logo_html)
subject = f"[TEST GLOBAL v2] NPI Weekly Overview - {stats.get('total', 0)} Projects, {len(stats.get('clients',{}))} Customers"
attachments = [('inline', logo_path, 'company_logo')] if logo_path else None
send_email(recipients=[TEST_EMAIL], subject=subject, body=html, is_html=True, attachments=attachments)
print(f"OK - Email Global inviata con {len(stats.get('clients',{}))} clienti, {stats['total']} progetti")
engine.dispose()
