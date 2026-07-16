# -*- coding: utf-8 -*-
"""
scrap_validation_reminder.py
Sollecito validazione scorie/rientri (dbo.ReturnMaterials) ancora PENDENTI
(IsOk IS NULL) da oltre N ore, per i soli MustCode legati a una regola attiva
(dbo.MaterialRules) — cioe' quelli che bloccano il rilascio dello stesso codice
finche' non sono validati.

Invia UNA email riepilogativa (tabella HTML di cio' che resta da validare) agli
indirizzi con attributo 'Sys_email_valida_restituzioni', ricordando che senza
validazione la richiesta collegata non e' rilasciabile.

Soglia ore + intervallo di ri-sollecito configurabili dalla setting
'Sys_valida_restituzioni_hours' (default 8). Il claim e' atomico su ReminderSentAt
(UPDATE condizionato + rowcount): con piu' istanze concorrenti ogni riga genera UN
solo sollecito per finestra (stesso pattern di kit_requests_reminder.py).

Pensato per essere schedulato (Task Scheduler / cron) ogni ~30 minuti, o eseguito
a mano.

Uso:
  .venv\\Scripts\\python.exe scrap_validation_reminder.py [--dry-run]
"""
import sys, io, os, argparse, html

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager
import utils

DEFAULT_HOURS = 8
EMAIL_SETTING = 'Sys_email_valida_restituzioni'
HOURS_SETTING = 'Sys_valida_restituzioni_hours'


def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
    )


def get_hours(cursor) -> int:
    try:
        cursor.execute("SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute=?",
                       (HOURS_SETTING,))
        r = cursor.fetchone()
        if r and str(r[0]).strip().isdigit():
            return max(1, int(str(r[0]).strip()))
    except Exception:
        pass
    return DEFAULT_HOURS


# Righe pendenti (IsOk IS NULL) di MustCode con regola attiva, oltre soglia, da
# risollecitare. COALESCE(DateCreated, DateReturn) copre le righe pre-migrazione.
CANDIDATE_SQL = """
    SELECT rm.ReturnMaterialId,
           mmust.CodiceMateriale        AS MustCode,
           mmust.DescrizioneMateriale   AS MustDesc,
           rm.ReturWeight,
           rm.UserRetur,
           COALESCE(rm.DateCreated, CAST(rm.DateReturn AS DATETIME)) AS Created,
           DATEDIFF(HOUR, COALESCE(rm.DateCreated, CAST(rm.DateReturn AS DATETIME)), GETDATE()) AS HoursPending,
           STUFF((SELECT DISTINCT ', ' + mi.CodiceMateriale
                  FROM dbo.MaterialRules mr2
                    INNER JOIN ind.Materiali mi ON mi.MaterialeId = mr2.MaterialeId
                  WHERE mr2.MustCodeId = rm.MateriaId AND mr2.DateOut IS NULL
                  FOR XML PATH('')), 1, 2, '') AS BlockedCodes
    FROM dbo.ReturnMaterials rm
      INNER JOIN ind.Materiali mmust ON mmust.MaterialeId = rm.MateriaId
    WHERE rm.DateOut IS NULL
      AND rm.IsOk IS NULL
      AND EXISTS (SELECT 1 FROM dbo.MaterialRules mr
                  WHERE mr.MustCodeId = rm.MateriaId AND mr.DateOut IS NULL)
      AND DATEDIFF(HOUR, COALESCE(rm.DateCreated, CAST(rm.DateReturn AS DATETIME)), GETDATE()) >= ?
      AND (rm.ReminderSentAt IS NULL
           OR DATEDIFF(HOUR, rm.ReminderSentAt, GETDATE()) >= ?)
    ORDER BY Created ASC
"""

CLAIM_SQL = """
    UPDATE dbo.ReturnMaterials
    SET ReminderSentAt = GETDATE()
    WHERE ReturnMaterialId = ? AND IsOk IS NULL AND DateOut IS NULL
      AND (ReminderSentAt IS NULL
           OR DATEDIFF(HOUR, ReminderSentAt, GETDATE()) >= ?)
"""


def build_html(rows, hours) -> str:
    head = (
        f"<p>Le seguenti dichiarazioni di scorie/rientri sono in attesa di validazione "
        f"da oltre <b>{hours} ore</b>.</p>"
        f"<p><b>Finche' non vengono validate, non sara' possibile rilasciare lo stesso codice</b> "
        f"(preparazione e prelievo restano bloccati).</p>"
    )
    th = ("<tr style='background:#2c3e50;color:#fff'>"
          "<th style='padding:6px 10px;text-align:left'>Codice scoria</th>"
          "<th style='padding:6px 10px;text-align:left'>Descrizione</th>"
          "<th style='padding:6px 10px;text-align:right'>Peso dich. (kg)</th>"
          "<th style='padding:6px 10px;text-align:left'>Dichiarato da</th>"
          "<th style='padding:6px 10px;text-align:left'>Data/ora</th>"
          "<th style='padding:6px 10px;text-align:right'>Ore attesa</th>"
          "<th style='padding:6px 10px;text-align:left'>Codici bloccati</th></tr>")
    trs = []
    for i, r in enumerate(rows):
        bg = '#f5f6fa' if i % 2 else '#ffffff'
        trs.append(
            f"<tr style='background:{bg}'>"
            f"<td style='padding:6px 10px'>{html.escape(str(r.MustCode or ''))}</td>"
            f"<td style='padding:6px 10px'>{html.escape(str(r.MustDesc or ''))}</td>"
            f"<td style='padding:6px 10px;text-align:right'>{float(r.ReturWeight or 0):.1f}</td>"
            f"<td style='padding:6px 10px'>{html.escape(str(r.UserRetur or ''))}</td>"
            f"<td style='padding:6px 10px'>{r.Created:%d/%m/%Y %H:%M}</td>"
            f"<td style='padding:6px 10px;text-align:right'>{int(r.HoursPending or 0)}</td>"
            f"<td style='padding:6px 10px'>{html.escape(str(r.BlockedCodes or '-'))}</td></tr>"
        )
    table = ("<table style='border-collapse:collapse;font-family:Segoe UI,Arial,sans-serif;"
             "font-size:13px;border:1px solid #ddd'>" + th + ''.join(trs) + "</table>")
    foot = ("<p style='font-size:12px;color:#666'>Usare la voce di menu "
            "\"Convalida Quantita' Dichiarate\" per registrare il peso rilevato e validare.</p>")
    return f"<div>{head}{table}{foot}</div>"


def main():
    parser = argparse.ArgumentParser(description='Sollecito validazione scorie/rientri pendenti')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    conn = get_conn()
    cursor = conn.cursor()
    hours = get_hours(cursor)
    print(f"Soglia/intervallo sollecito: {hours} ore{' (DRY-RUN)' if args.dry_run else ''}")

    cursor.execute(CANDIDATE_SQL, (hours, hours))
    candidates = cursor.fetchall()
    if not candidates:
        print("Nessuna validazione pendente da sollecitare.")
        conn.close()
        return

    # Claim atomico per riga: vince una sola istanza concorrente
    claimed = []
    for r in candidates:
        if args.dry_run:
            claimed.append(r)
            continue
        cursor.execute(CLAIM_SQL, (r.ReturnMaterialId, hours))
        if cursor.rowcount > 0:
            claimed.append(r)
    if not args.dry_run:
        conn.commit()

    if not claimed:
        print("Validazioni gia' sollecitate da un'altra istanza.")
        conn.close()
        return

    print(f"Da sollecitare: {len(claimed)} dichiarazioni")
    for r in claimed:
        print(f"  - #{r.ReturnMaterialId} | {r.MustCode} | {float(r.ReturWeight or 0):.1f} kg "
              f"| {r.UserRetur} | {r.Created:%d/%m/%Y %H:%M} | {int(r.HoursPending or 0)}h "
              f"| blocca: {r.BlockedCodes or '-'}")

    if args.dry_run:
        print("DRY-RUN: nessuna email inviata, nessun claim scritto.")
        conn.close()
        return

    try:
        recipients = utils.get_email_recipients(conn, EMAIL_SETTING)
        if recipients:
            utils.send_email(
                recipients,
                f"[SOLLECITO] {len(claimed)} validazioni scorie/rientri in attesa da oltre {hours}h",
                build_html(claimed, hours),
                is_html=True)
            print(f"Email inviata a {len(recipients)} destinatari.")
        else:
            print(f"ATTENZIONE: nessun destinatario in {EMAIL_SETTING}, email non inviata.")
    except Exception as e:
        print(f"ERRORE invio email: {e}")

    conn.close()
    print("Sollecito completato.")


if __name__ == '__main__':
    main()
