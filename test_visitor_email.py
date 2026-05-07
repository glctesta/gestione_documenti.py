# -*- coding: utf-8 -*-
"""Test invio email management visitatori a gianluca.testa@vandewiele.com"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config_manager import ConfigManager
from email_connector import EmailSender
from datetime import datetime
from collections import OrderedDict
import pyodbc

# Connessione DB con credenziali criptate (stesso pattern di main.py)
config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
db_credentials = config_mgr.load_config()
conn_str = (f"DRIVER={db_credentials['driver']};SERVER={db_credentials['server']};"
            f"DATABASE={db_credentials['database']};UID={db_credentials['username']};"
            f"PWD={db_credentials['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")

conn = pyodbc.connect(conn_str)
print("✅ Connesso al database")

# Query visitatori da oggi in poi
query = """
    SELECT 
        v.VisitorId,
        CAST(v.StartVisit AS DATE) AS VisitDate,
        v.CompanyName,
        v.GuestName,
        v.Pourpose,
        v.SponsorGuy,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM Employee.dbo.VisitorArrivalDetails vad 
                WHERE vad.VisitorId = v.VisitorId
            ) THEN 1 ELSE 0 
        END AS HasPickup,
        (
            SELECT TOP 1 vsd.Name 
            FROM Employee.dbo.VisitorArrivalDetails vad
            INNER JOIN Employee.dbo.VisitorSupportersData vsd 
                ON vsd.SupporterDataId = vad.HotelId
            WHERE vad.VisitorId = v.VisitorId
        ) AS HotelName,
        v.StartVisit,
        v.EndVisit
    FROM Employee.dbo.Visitors v
    WHERE v.EndVisit >= CAST(GETDATE() AS DATE)
    ORDER BY CAST(v.StartVisit AS DATE), v.CompanyName, v.GuestName
"""

cursor = conn.cursor()
cursor.execute(query)
visitors = cursor.fetchall()
cursor.close()

print(f"📋 Trovati {len(visitors)} visitatori futuri")
for v in visitors:
    print(f"   • {v.GuestName} ({v.CompanyName}) — {v.VisitDate} — Hotel: {v.HotelName or 'N/A'} — Pickup: {'Sì' if v.HasPickup else 'No'}")

if not visitors:
    print("Nessun visitatore — esco")
    conn.close()
    sys.exit(0)

# Raggruppamento per giorno
days = OrderedDict()
for v in visitors:
    day_key = v.VisitDate
    if day_key not in days:
        days[day_key] = []
    days[day_key].append(v)

table_rows = ''
for day, day_visitors in days.items():
    day_str = day.strftime('%A %d/%m/%Y') if hasattr(day, 'strftime') else str(day)
    table_rows += f'''
    <tr style="background-color: #0078D4; color: white;">
        <td colspan="6" style="padding: 8px 12px; font-weight: bold; font-size: 13px;">
            📅 {day_str} — {len(day_visitors)} vizitator(i)
        </td>
    </tr>
    '''
    for i, v in enumerate(day_visitors):
        bg = ' style="background-color: #F8F9FA;"' if i % 2 == 0 else ''
        pickup_icon = '✅' if v.HasPickup else '❌'
        hotel = v.HotelName or '—'
        start_str = v.StartVisit.strftime('%d/%m') if v.StartVisit else ''
        end_str = v.EndVisit.strftime('%d/%m') if v.EndVisit else ''
        table_rows += f'''
        <tr{bg}>
            <td style="padding: 6px 10px;">{v.CompanyName or '—'}</td>
            <td style="padding: 6px 10px;">{v.GuestName or '—'}</td>
            <td style="padding: 6px 10px;">{v.Pourpose or '—'}</td>
            <td style="padding: 6px 10px; text-align: center;">{start_str} — {end_str}</td>
            <td style="padding: 6px 10px; text-align: center;">{pickup_icon}</td>
            <td style="padding: 6px 10px;">{hotel}</td>
        </tr>
        '''

today_str = datetime.now().strftime('%d/%m/%Y')
logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; font-size: 12px; color: #333;">
    <img src="cid:company_logo" alt="Vandewiele" style="width: 150px; margin-bottom: 10px;" /><br/>
    <h2 style="color: #0078D4;">Listă Vizitatori Programați / Scheduled Visitors List</h2>
    <p>Data raport: <strong>{today_str}</strong></p>
    <p>Mai jos este lista actualizată a vizitatorilor programați de astăzi în continuare:</p>

    <table style="border-collapse: collapse; margin: 15px 0; font-size: 12px; width: 100%; border: 1px solid #ddd;">
        <tr style="background-color: #2C3E50; color: white;">
            <th style="padding: 8px 10px; text-align: left;">Companie</th>
            <th style="padding: 8px 10px; text-align: left;">Persoană</th>
            <th style="padding: 8px 10px; text-align: left;">Scop vizită</th>
            <th style="padding: 8px 10px; text-align: center;">Perioadă</th>
            <th style="padding: 8px 10px; text-align: center;">Pickup</th>
            <th style="padding: 8px 10px; text-align: left;">Hotel</th>
        </tr>
        {table_rows}
    </table>

    <p style="color: #888; font-size: 10px; margin-top: 20px;">
        Total vizitatori: {len(visitors)}<br/>
        Email generată automat de TraceabilityRS — TEST
    </p>
</body>
</html>
"""

# Invio email
sender = EmailSender()
attachments = []
if os.path.exists(logo_path):
    attachments.append(('inline', logo_path, 'company_logo'))
    print(f"📎 Logo allegato: {logo_path}")

print(f"\n📧 Invio email a gianluca.testa@vandewiele.com con {len(visitors)} visitatori...")
sender.send_email(
    to_email='gianluca.testa@vandewiele.com',
    subject=f"[TEST] Vizitatori Programați — {today_str} — {len(visitors)} persoane",
    body=body_html,
    is_html=True,
    attachments=attachments if attachments else None
)
print("✅ Email inviata con successo!")
conn.close()
