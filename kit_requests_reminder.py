"""
kit_requests_reminder.py
Reminder richieste materiale kit ancora PENDING — Sprint 3
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §7.1: reminder ripetuto a
ogni scadenza del timeout — default 10 minuti — finche' la richiesta non
passa a CONFIRMED/CANCELLED).

Pensato per essere schedulato (Task Scheduler / cron) ogni 5 minuti, o
eseguito a mano. Il claim e' atomico su wh_last_notified (UPDATE con
condizione + rowcount): con piu' istanze concorrenti ogni richiesta
genera UNA sola notifica per finestra (stesso pattern del log email).

Timeout configurabile dalla setting 'Sys_kit_reminder_minutes' (se assente: 10).

Uso:
  .venv\\Scripts\\python.exe kit_requests_reminder.py [--dry-run]
"""
import sys, io, os, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager
import utils

DEFAULT_MINUTES = 10
EMAIL_SETTING = 'Sys_email_Kit_materiali'
MINUTES_SETTING = 'Sys_kit_reminder_minutes'


def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
    )


def get_reminder_minutes(cursor) -> int:
    try:
        cursor.execute("SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute=?",
                       (MINUTES_SETTING,))
        r = cursor.fetchone()
        if r and str(r[0]).strip().isdigit():
            return max(1, int(str(r[0]).strip()))
    except Exception:
        pass
    return DEFAULT_MINUTES


def main():
    parser = argparse.ArgumentParser(description='Reminder richieste materiale kit PENDING')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    conn = get_conn()
    cursor = conn.cursor()
    minutes = get_reminder_minutes(cursor)
    print(f"Timeout reminder: {minutes} minuti{' (DRY-RUN)' if args.dry_run else ''}")

    # Candidate: PENDING oltre il timeout, mai notificate o notificate da > timeout
    cursor.execute("""
        SELECT id, order_number, requesting_phase, material_code, qty_requested,
               request_date, note
        FROM Traceability_RS.dbo.material_requests
        WHERE wh_status = 'PENDING' AND resolution IS NULL
          AND DATEDIFF(MINUTE, request_date, GETDATE()) >= ?
          AND (wh_last_notified IS NULL
               OR DATEDIFF(MINUTE, wh_last_notified, GETDATE()) >= ?)
        ORDER BY request_date ASC
    """, (minutes, minutes))
    candidates = cursor.fetchall()
    if not candidates:
        print("Nessuna richiesta da sollecitare.")
        conn.close()
        return

    # Claim atomico per richiesta: vince una sola istanza concorrente
    claimed = []
    for r in candidates:
        if args.dry_run:
            claimed.append(r)
            continue
        cursor.execute("""
            UPDATE Traceability_RS.dbo.material_requests
            SET wh_last_notified = GETDATE()
            WHERE id = ? AND wh_status = 'PENDING'
              AND (wh_last_notified IS NULL
                   OR DATEDIFF(MINUTE, wh_last_notified, GETDATE()) >= ?)
        """, (r[0], minutes))
        if cursor.rowcount > 0:
            claimed.append(r)
    if not args.dry_run:
        conn.commit()

    if not claimed:
        print("Richieste gia' sollecitate da un'altra istanza.")
        conn.close()
        return

    lines = [f"- #{r[0]} | ordine {r[1]} | fase {r[2]} | {r[3]} x {float(r[4]):g} "
             f"| richiesta il {r[5]:%d/%m/%Y %H:%M} | {r[6] or '-'}"
             for r in claimed]
    print(f"Da sollecitare: {len(claimed)} richieste")
    for ln in lines:
        print(' ', ln)

    if args.dry_run:
        print("DRY-RUN: nessuna notifica inviata.")
        conn.close()
        return

    # Popup alla postazione Formazione Kit (consumato dal monitor in-app)
    for r in claimed:
        cursor.execute("""
            INSERT INTO Traceability_RS.dbo.kit_popup_queue
                (category, target, title, message, order_number)
            VALUES ('DIRECT_MATERIAL', 'KIT_PREP', ?, ?, ?)
        """, (f"⏰ REMINDER richiesta materiale — {r[1]}",
              f"Richiesta #{r[0]} ancora in attesa da oltre {minutes} min: "
              f"{r[3]} x {float(r[4]):g} (fase {r[2]}). Motivo: {r[6] or '-'}",
              r[1]))
    conn.commit()

    # Email riepilogativa
    try:
        recipients = utils.get_email_recipients(conn, EMAIL_SETTING)
        if recipients:
            utils.send_email(
                recipients,
                f"[REMINDER] {len(claimed)} richieste materiale kit in attesa",
                "Le seguenti richieste di materiale aggiuntivo sono ancora in attesa "
                f"di conferma da oltre {minutes} minuti:\n\n" + '\n'.join(lines)
                + "\n\nAccedi al sistema (scheda Richieste Materiale) per gestirle.")
            print(f"Email inviata a {len(recipients)} destinatari.")
        else:
            print(f"ATTENZIONE: nessun destinatario in {EMAIL_SETTING}, email non inviata.")
    except Exception as e:
        print(f"ERRORE invio email: {e}")

    conn.close()
    print("Reminder completato.")


if __name__ == '__main__':
    main()
