"""
Test script: invia TUTTE le email NPI a gtesta@gmail.com
  1) Tutte le Email Project Owner consolidate
  2) Tutte le Email Task Owner consolidate
  3) Panoramica globale NPI
"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import urllib
from datetime import datetime, date, timedelta
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


def create_npi_engine():
    params = urllib.parse.quote_plus(conn_str)
    connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
    engine = create_engine(
        connection_url, poolclass=QueuePool, pool_size=5, max_overflow=10,
        pool_recycle=3600, pool_pre_ping=True, pool_timeout=30, echo=False
    )
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
    print("  Engine DB connesso OK")
    return engine


def main():
    from utils import send_email

    print("=" * 60)
    print("TEST EMAIL NPI - Invio COMPLETO a", TEST_EMAIL)
    print("=" * 60)

    engine = create_npi_engine()
    from npi.npi_manager import GestoreNPI
    from npi.npi_auto_notifications import NpiAutoNotificationService

    npi_mgr = GestoreNPI(engine=engine)
    svc = NpiAutoNotificationService(npi_mgr)
    po_sent = 0
    to_sent = 0

    # 1) TUTTE LE EMAIL PROJECT OWNER
    print("\n[1/3] Raccolta dati per TUTTI i Project Owner...")
    project_owner_map = svc._collect_all_task_notifications()
    print(f"      Trovati {len(project_owner_map)} Project Owner con task")

    for po_email, po_data in project_owner_map.items():
        all_tasks = []
        for tasks in po_data['tasks_by_task_owner'].values():
            all_tasks.extend(tasks)
        overdue_count = sum(1 for t in all_tasks if t['notification_type'] == 'TaskOverdue')
        tomorrow_count = sum(1 for t in all_tasks if t['notification_type'] == 'TaskDueTomorrow')
        excel_path = svc._build_project_owner_excel(po_data['owner_name'], po_data['tasks_by_task_owner'])
        html_body = svc._build_project_owner_email_html(
            po_data['owner_name'], po_data['tasks_by_task_owner'], overdue_count, tomorrow_count)
        subject = (f"[TEST PO] NPI Alert - {overdue_count} overdue, "
                   f"{tomorrow_count} due tomorrow ({len(all_tasks)} tasks) - "
                   f"{po_data['owner_name']} [orig: {po_email}]")
        logo_path = svc._resolve_logo_path()
        attachments = []
        if logo_path: attachments.append(('inline', logo_path, 'company_logo'))
        if excel_path: attachments.append(excel_path)
        try:
            send_email(recipients=[TEST_EMAIL], subject=subject, body=html_body,
                       is_html=True, attachments=attachments if attachments else None)
            po_sent += 1
            print(f"      OK PO #{po_sent}: {po_data['owner_name']} ({po_email}) -> {len(all_tasks)} task")
        except Exception as e:
            print(f"      ERRORE PO {po_data['owner_name']}: {e}")
        try:
            if excel_path and os.path.exists(excel_path): os.remove(excel_path)
        except: pass

    if not project_owner_map:
        print("      SKIP - Nessun dato Project Owner")

    # 2) TUTTE LE EMAIL TASK OWNER
    print(f"\n[2/3] Raccolta dati per TUTTI i Task Owner...")
    task_owner_map = svc._collect_task_owner_notifications()
    print(f"      Trovati {len(task_owner_map)} Task Owner con task")

    for to_email, to_data in task_owner_map.items():
        tasks = to_data['tasks']
        overdue_count = sum(1 for t in tasks if t['notification_type'] == 'TaskOverdue')
        tomorrow_count = sum(1 for t in tasks if t['notification_type'] == 'TaskDueTomorrow')
        html_body = svc._build_task_owner_email_html(
            to_data['task_owner_name'], tasks, overdue_count, tomorrow_count)
        subject = (f"[TEST TO] NPI Alert - {overdue_count} overdue, "
                   f"{tomorrow_count} due tomorrow ({len(tasks)} tasks) - "
                   f"{to_data['task_owner_name']} [orig: {to_email}]")
        logo_path = svc._resolve_logo_path()
        attachments = [('inline', logo_path, 'company_logo')] if logo_path else None
        try:
            send_email(recipients=[TEST_EMAIL], subject=subject, body=html_body,
                       is_html=True, attachments=attachments)
            to_sent += 1
            print(f"      OK TO #{to_sent}: {to_data['task_owner_name']} ({to_email}) -> {len(tasks)} task")
        except Exception as e:
            print(f"      ERRORE TO {to_data['task_owner_name']}: {e}")

    if not task_owner_map:
        print("      SKIP - Nessun dato Task Owner")

    # 3) PANORAMICA GLOBALE NPI
    print(f"\n[3/3] Raccolta statistiche globali NPI...")
    try:
        stats = svc._collect_global_npi_stats()
        logo_path = svc._resolve_logo_path()
        logo_html = '<img src="cid:company_logo" style="max-width:150px;height:auto;" alt="Logo">' if logo_path else ""
        html_body = svc._build_global_view_email_html(stats, logo_html)
        subject = f"[TEST GLOBAL] NPI Weekly Overview - {stats.get('total_active', 0)} Active Projects"
        attachments = [('inline', logo_path, 'company_logo')] if logo_path else None
        send_email(recipients=[TEST_EMAIL], subject=subject, body=html_body,
                   is_html=True, attachments=attachments)
        print(f"      OK Panoramica Globale ({stats.get('total_active', 0)} progetti)")
    except Exception as e:
        print(f"      ERRORE panoramica globale: {e}")

    engine.dispose()
    print("\n" + "=" * 60)
    print(f"COMPLETATO - {po_sent} PO + {to_sent} TO + 1 Global = {po_sent+to_sent+1} emails")
    print(f"Controlla {TEST_EMAIL}")
    print("=" * 60)


if __name__ == "__main__":
    main()
