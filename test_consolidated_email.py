"""
Script di test: invia 1 email consolidata task owner con dati fittizi.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta, datetime

# --- Dati fittizi per il test ---
recipient_email = "gianluca.testa@vandewiele.com"
recipient_name = "Gianluca Testa"

projects_grouped = {
    101: {
        'project_name': 'NPI Motor Assembly X200',
        'project_code': 'MA-X200',
        'project_owner': 'Marco Rossi',
        'tasks': [
            {
                'task_name': 'Validazione componenti meccanici',
                'task_owner_name': 'Gianluca Testa',
                'due_date': date.today() - timedelta(days=7),
                'delay_days': 7,
                'task_status': 'In Progress',
                'notification_type': 'TaskOverdue',
            },
            {
                'task_name': 'Test resistenza termica',
                'task_owner_name': 'Gianluca Testa',
                'due_date': date.today() - timedelta(days=3),
                'delay_days': 3,
                'task_status': 'In Progress',
                'notification_type': 'TaskOverdue',
            },
            {
                'task_name': 'Aggiornamento documentazione tecnica',
                'task_owner_name': 'Gianluca Testa',
                'due_date': date.today() + timedelta(days=1),
                'delay_days': 0,
                'task_status': 'Not Started',
                'notification_type': 'TaskDueTomorrow',
            },
        ]
    },
    205: {
        'project_name': 'NPI Sensor Board V3',
        'project_code': 'SB-V3',
        'project_owner': 'Elena Bianchi',
        'tasks': [
            {
                'task_name': 'Verifica compatibilità firmware',
                'task_owner_name': 'Gianluca Testa',
                'due_date': date.today() - timedelta(days=12),
                'delay_days': 12,
                'task_status': 'In Progress',
                'notification_type': 'TaskOverdue',
            },
        ]
    },
}

overdue_count = 3
tomorrow_count = 1

# --- Genera HTML con lo stesso template ---
logo_html = ""
logo_path = os.path.join(os.getcwd(), "Logo.png")
if os.path.exists(logo_path):
    logo_html = '<img src="cid:company_logo" style="max-width:150px;height:auto;" alt="Company Logo">'

total_tasks = overdue_count + tomorrow_count

summary_html = f"""
<div style="display:flex;gap:12px;margin:14px 0;">
    <div style="flex:1;background:#FDECEA;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:bold;color:#B30000;">{overdue_count}</div>
        <div style="font-size:12px;color:#B30000;">OVERDUE</div>
    </div>
    <div style="flex:1;background:#FFF3E0;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:bold;color:#E65100;">{tomorrow_count}</div>
        <div style="font-size:12px;color:#E65100;">DUE TOMORROW</div>
    </div>
    <div style="flex:1;background:#E8F5E9;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:bold;color:#1B5E20;">{len(projects_grouped)}</div>
        <div style="font-size:12px;color:#1B5E20;">PROJECTS</div>
    </div>
</div>
"""

projects_html = ""
for pid, pdata in projects_grouped.items():
    rows_html = ""
    for t in sorted(pdata['tasks'], key=lambda x: x['due_date']):
        if t['notification_type'] == 'TaskOverdue':
            icon = "🚨"
            badge = f'<span style="background:#B30000;color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;">OVERDUE ({t["delay_days"]}d)</span>'
        else:
            icon = "⚠️"
            badge = '<span style="background:#E65100;color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;">DUE TOMORROW</span>'

        rows_html += f"""
        <tr>
            <td style="padding:8px;border:1px solid #e5e7eb;">{icon} {t['task_name']}</td>
            <td style="padding:8px;border:1px solid #e5e7eb;">{t['task_owner_name']}</td>
            <td style="padding:8px;border:1px solid #e5e7eb;text-align:center;">{t['due_date'].strftime('%d/%m/%Y')}</td>
            <td style="padding:8px;border:1px solid #e5e7eb;text-align:center;">{t['task_status']}</td>
            <td style="padding:8px;border:1px solid #e5e7eb;text-align:center;">{badge}</td>
        </tr>
        """

    projects_html += f"""
    <div style="margin:16px 0;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;">
        <div style="background:#1F4E78;color:#fff;padding:10px 14px;">
            <strong>{pdata['project_name']}</strong>
            <span style="opacity:0.8;margin-left:10px;">({pdata['project_code']})</span>
            <span style="float:right;font-size:12px;">Owner: {pdata['project_owner']}</span>
        </div>
        <table style="border-collapse:collapse;width:100%;">
            <thead>
                <tr style="background:#f1f5f9;">
                    <th style="padding:8px;border:1px solid #e5e7eb;text-align:left;">Task</th>
                    <th style="padding:8px;border:1px solid #e5e7eb;text-align:left;">Task Owner</th>
                    <th style="padding:8px;border:1px solid #e5e7eb;text-align:center;">Due Date</th>
                    <th style="padding:8px;border:1px solid #e5e7eb;text-align:center;">Status</th>
                    <th style="padding:8px;border:1px solid #e5e7eb;text-align:center;">Alert</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """

html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:'Segoe UI',Arial,sans-serif;color:#1f2937;background:#f5f7fb;padding:20px;">
    <div style="max-width:980px;margin:0 auto;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;">
        <div style="background:#FFFFFF;color:#0B3A66;padding:20px 24px;border-bottom:3px solid #0B3A66;">
            {logo_html}
            <h2 style="margin:12px 0 4px 0;">NPI Task Notification — Task Owner</h2>
            <p style="margin:0;opacity:0.92;">Consolidated alert for {total_tasks} task(s) requiring attention.</p>
        </div>
        <div style="padding:22px 24px;">
            <p>Dear <strong>{recipient_name}</strong>,</p>
            <p>The NPI monitoring system detected the following tasks that need your attention:</p>

            {summary_html}

            {projects_html}

            <div style="background:#e7f3ff;border-left:4px solid #0078d4;padding:15px;margin:20px 0;border-radius:4px;">
                <h4 style="color:#0078d4;margin:0 0 10px 0;">📌 ACTION REQUIRED</h4>
                <ul style="margin:0;padding-left:20px;color:#333;">
                    <li>Please review and update the task status in the NPI system</li>
                    <li>Coordinate with team members if dependencies exist</li>
                    <li>Contact the relevant project owner if you need assistance</li>
                </ul>
            </div>

            <p style="color:#6b7280;font-size:12px;margin-top:24px;">
                This is an automated notification from the NPI Project Management System.
                Please do not reply to this email.
                Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </div>
</body>
</html>
"""

subject = f"[TEST] NPI Task Alert - {overdue_count} overdue, {tomorrow_count} due tomorrow ({total_tasks} tasks)"

# --- Invio email ---
try:
    from utils import send_email

    attachments = None
    if os.path.exists(logo_path):
        attachments = [('inline', logo_path, 'company_logo')]

    send_email(
        recipients=[recipient_email],
        subject=subject,
        body=html_body,
        is_html=True,
        cc_emails=[],
        attachments=attachments
    )
    print(f"✅ Email di test inviata con successo a {recipient_email}")
except Exception as e:
    print(f"❌ Errore invio: {e}")
    import traceback
    traceback.print_exc()
