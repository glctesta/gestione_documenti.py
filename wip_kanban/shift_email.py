# -*- coding: utf-8 -*-
"""
shift_email.py — Email riepilogativa movimenti kanban ai cambi turno (15:30, 23:30).

Gira come thread daemon dentro il server web (web_server.py): il server e'
sempre attivo, a differenza dell'app desktop. Pattern: fqc_email.py.

Destinatari: righe in Traceability_RS.dbo.settings con atribute='sys_mail_wip_kanban'.
Invio: utils.send_email (SMTP relay interno). Anti-duplicazione: claim atomico
su settings (chiave WipKanbanEmail_YYYYMMDD_HHMM).
"""
import os
import sys
import time
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("WipKanban")

EMAIL_ATTRIBUTE = "sys_mail_wip_kanban"
TRIGGERS = [(15, 30, "1530"), (23, 30, "2330")]  # (ora, minuto, label)
MORNING_START_HOUR = 6  # la mail delle 15:30 copre 06:00 -> 15:30

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


def _logo_path():
    base = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(base, "static", "Logo.png"),
              os.path.join(_project_root, "Logo.png"),
              os.path.join(_project_root, "logo.png")):
        if os.path.isfile(p):
            return p
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Invio
# ─────────────────────────────────────────────────────────────────────────────

def get_recipients(conn):
    cur = conn.cursor()
    cur.execute(
        """SELECT [VALUE] FROM Traceability_RS.dbo.settings
           WHERE atribute = ? AND ISNULL(DateOut, '9999-01-01') > GETDATE()""",
        (EMAIL_ATTRIBUTE,),
    )
    out = []
    for (value,) in cur.fetchall():
        for addr in str(value or "").replace(";", ",").split(","):
            addr = addr.strip()
            if "@" in addr:
                out.append(addr)
    return out


def _claim_slot(conn, slot_key):
    """True se il claim e' riuscito (nessun altro PC/processo ha inviato)."""
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Traceability_RS.dbo.settings (atribute, [VALUE])
           SELECT ?, ?
           WHERE NOT EXISTS (
               SELECT 1 FROM Traceability_RS.dbo.settings WITH (UPDLOCK, HOLDLOCK)
               WHERE atribute = ?)""",
        (slot_key, datetime.now().isoformat(), slot_key),
    )
    return cur.rowcount == 1


def _release_slot(conn, slot_key):
    conn.cursor().execute(
        "DELETE FROM Traceability_RS.dbo.settings WHERE atribute = ?", (slot_key,)
    )


def _section_html(title, rows):
    if not rows:
        return f"<h3>{title}</h3><p><em>Nessun movimento.</em></p>"
    body = "".join(
        "<tr>"
        f"<td>{r['DateIn']:%d/%m/%Y %H:%M}</td>"
        f"<td>{r['PositionCode'] or '-'}</td>"
        f"<td>{r['LabelCode'] or '-'}</td>"
        f"<td>{r['OrderNumber'] or '-'}</td>"
        f"<td>{r['ProductCode'] or '-'}</td>"
        f"<td>{r['User'] or '-'}</td>"
        "</tr>"
        for r in rows
    )
    return (
        f"<h3>{title} ({len(rows)})</h3>"
        "<table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse'>"
        "<tr style='background:#2c5f2e;color:#fff'>"
        "<th>Data</th><th>Posizione</th><th>LabelCode</th><th>Ordine</th><th>Prodotto</th><th>Utente</th>"
        "</tr>" + body + "</table>"
    )


def send_shift_email(conn, start, end, label):
    """Invia la mail del turno. Restituisce True se inviata (o gia' inviata)."""
    slot_key = f"WipKanbanEmail_{datetime.now():%Y%m%d}_{label}"
    if not _claim_slot(conn, slot_key):
        logger.info("Email turno %s già inviata (slot %s)", label, slot_key)
        return True
    conn.commit()

    try:
        recipients = get_recipients(conn)
        if not recipients:
            logger.warning("Nessun destinatario per atribute='%s': email saltata", EMAIL_ATTRIBUTE)
            _release_slot(conn, slot_key)
            conn.commit()
            return False

        from wip_kanban import kanban_logic
        movements = kanban_logic.movements_between(conn, start, end)
        ins = [m for m in movements if m["Action"] == "IN"]
        outs = [m for m in movements if m["Action"] == "OUT"]

        if not movements:
            logger.info("Nessun movimento nel turno %s: nessuna email", label)
            _release_slot(conn, slot_key)
            conn.commit()
            return False

        logo = _logo_path()
        logo_tag = "<img src='cid:kanbanlogo' style='max-width:180px'>" if logo else ""
        html = f"""<html><body>
{logo_tag}
<h2>Kanban produzione — movimenti turno {start:%d/%m/%Y %H:%M} → {end:%H:%M}</h2>
{_section_html('Inserimenti (carico schede)', ins)}
<br/>
{_section_html('Prelievi', outs)}
</body></html>"""

        import utils
        attachments = [("inline", logo, "kanbanlogo")] if logo else None
        utils.send_email(
            recipients=recipients,
            subject=f"Kanban produzione — riepilogo turno {end:%d/%m/%Y %H:%M}",
            body=html,
            is_html=True,
            attachments=attachments,
        )
        logger.info("Email turno %s inviata a %s", label, recipients)
        return True
    except Exception as e:
        logger.error("Errore invio email turno %s: %s", label, e, exc_info=True)
        _release_slot(conn, slot_key)
        conn.commit()
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────────────────────────────────────

def _shift_window(now, label):
    """Finestra del turno che si chiude al trigger `label`."""
    end = now.replace(hour=15 if label == "1530" else 23,
                      minute=30 if label == "1530" else 30, second=0, microsecond=0)
    if label == "1530":
        start = now.replace(hour=MORNING_START_HOUR, minute=0, second=0, microsecond=0)
    else:
        start = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return start, end


def scheduler_loop():
    """Loop infinito: attende i trigger 15:30 / 23:30 (domenica esclusa) e invia."""
    from wip_kanban import db
    logger.info("Scheduler email kanban attivo (trigger 15:30 / 23:30)")
    while True:
        try:
            now = datetime.now()
            if now.weekday() == 6:  # domenica: attendi mezzanotte
                time.sleep(300)
                continue
            nxt = None
            for hh, mm, label in TRIGGERS:
                cand = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
                if cand > now:
                    nxt = (cand, label)
                    break
            if nxt is None:
                nxt = ((now + timedelta(days=1)).replace(hour=TRIGGERS[0][0],
                        minute=TRIGGERS[0][1], second=0, microsecond=0), TRIGGERS[0][2])
            # dormi a fette di 60s per restare reattivo agli shutdown
            while datetime.now() < nxt[0]:
                time.sleep(60)
            conn = db.get_conn()
            try:
                start, end = _shift_window(datetime.now(), nxt[1])
                send_shift_email(conn, start, end, nxt[1])
            finally:
                conn.close()
        except Exception as e:
            logger.error("Errore scheduler email kanban: %s", e, exc_info=True)
            time.sleep(300)


if __name__ == "__main__":
    # Invio manuale di prova (ultima finestra di turno disponibile)
    logging.basicConfig(level=logging.INFO)
    from wip_kanban import db
    now = datetime.now()
    label = "1530" if now.hour < 15 or (now.hour == 15 and now.minute < 30) else "2330"
    start, end = _shift_window(now, label)
    c = db.get_conn()
    try:
        send_shift_email(c, start, end, label)
    finally:
        c.close()
