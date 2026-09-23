# -*- coding: utf-8 -*-
"""
picks_tasks.py — Sweep PTHM + email giornaliera prelievo-per-ordine WIP.

Gira come thread daemon dentro web_server.py (porta 6500), accanto allo
scheduler email di shift_email.py:

  * ogni POLL_INTERVAL_SEC secondi esegue kanban_logic.pthm_sweep: scarica dal
    kanban le schede "cercate per ordine" la cui ultima scansione e' nella
    fase PTHM (match esatto, vedi PTHM_PHASE_NAMES);
  * una volta al giorno alle EMAIL_HOUR:EMAIL_MINUTE invia la mail
    "schede cercate non passate PTHM" con allegato Excel delle schede pending.

Anti-duplicazione della mail: claim atomico su dbo.settings (stesso pattern di
shift_email._claim_slot), chiave WipKanbanPicksEmail_YYYYMMDD.

Destinatari: dbo.settings Atribute='Sys_email_kanban_irregular', Value con
email separate da ';'.
"""
import time
import logging
from datetime import datetime

logger = logging.getLogger("WipKanban")

POLL_INTERVAL_SEC = 60
EMAIL_HOUR = 7
EMAIL_MINUTE = 0

RECIPIENTS_ATTRIBUTE = "Sys_email_kanban_irregular"
EMAIL_SUBJECT = "Kanban WIP — schede cercate non passate PTHM"


# ─────────────────────────────────────────────────────────────────────────────
# Sweep PTHM
# ─────────────────────────────────────────────────────────────────────────────

def run_pthm_sweep():
    """Esegue lo sweep su una connessione propria; commit solo se tutto ok."""
    from wip_kanban import db, kanban_logic
    conn = db.get_conn()
    try:
        conn.timeout = 120
        cur = conn.cursor()
        swept = kanban_logic.pthm_sweep(cur)
        if swept:
            conn.commit()
            logger.info("PTHM sweep: %d schede scaricate (%s)",
                        len(swept), ", ".join(s["LabelCode"] for s in swept[:10]))
        else:
            conn.rollback()  # nessuna modifica attesa, ma scarico eventuali lock
        return swept
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Email giornaliera
# ─────────────────────────────────────────────────────────────────────────────

def get_recipients(conn):
    """Destinatari da settings (Value: email separate da ';')."""
    cur = conn.cursor()
    cur.execute(
        """SELECT [VALUE] FROM Traceability_RS.dbo.Settings
           WHERE Atribute = ?""",
        (RECIPIENTS_ATTRIBUTE,),
    )
    out = []
    for (value,) in cur.fetchall():
        for addr in str(value or "").split(";"):
            addr = addr.strip().replace(",", "")
            if "@" in addr:
                out.append(addr)
    return out


def _claim_slot(conn, slot_key):
    """True se il claim e' riuscito (nessun altro processo ha inviato oggi)."""
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Traceability_RS.dbo.Settings (Atribute, [VALUE])
           SELECT ?, ?
           WHERE NOT EXISTS (
               SELECT 1 FROM Traceability_RS.dbo.Settings WITH (UPDLOCK, HOLDLOCK)
               WHERE Atribute = ?)""",
        (slot_key, datetime.now().isoformat(), slot_key),
    )
    return cur.rowcount == 1


def _release_slot(conn, slot_key):
    conn.cursor().execute(
        "DELETE FROM Traceability_RS.dbo.Settings WHERE Atribute = ?", (slot_key,)
    )


def _section_html(title, stats):
    return (f"<h3>{title}</h3>"
            f"<p>Ordini: <b>{stats['orders']}</b> · "
            f"Schede: <b>{stats['boards']}</b> · "
            f"Prodotti: <b>{stats['products']}</b></p>")


def send_daily_email(conn):
    """Invia la mail del mattino. Restituisce True se inviata (o gia' inviata)."""
    from wip_kanban import i18n, kanban_logic, excel_gen

    slot_key = f"WipKanbanPicksEmail_{datetime.now():%Y%m%d}"
    if not _claim_slot(conn, slot_key):
        logger.info("Email picks PTHM già inviata oggi (slot %s)", slot_key)
        return True
    conn.commit()

    try:
        recipients = get_recipients(conn)
        if not recipients:
            logger.warning("Nessun destinatario per Atribute='%s': email saltata",
                           RECIPIENTS_ATTRIBUTE)
            _release_slot(conn, slot_key)
            conn.commit()
            return False

        cur = conn.cursor()
        stats = kanban_logic.order_picks_stats(cur)
        rows = kanban_logic.order_picks_open(cur)

        ui = i18n.get_ui("it")
        path = excel_gen.order_picks_workbook(rows, ui)
        attachment_name = f"kanban_wip_picks_{datetime.now():%Y%m%d_%H%M}.xlsx"

        html = f"""<html><body>
<h2>{EMAIL_SUBJECT}</h2>
<p>Schede cercate per ordine (prelievo WIP) non ancora passate PTHM.</p>
{_section_html('Aperte (in attesa di PTHM)', stats['open'])}
<br/>
{_section_html('Passate PTHM (scaricate)', stats['passed'])}
<br/>
<p>Allegato: {attachment_name} ({len(rows)} schede pending).</p>
</body></html>"""

        import utils
        utils.send_email(
            recipients=recipients,
            subject=EMAIL_SUBJECT,
            body=html,
            is_html=True,
            attachments=[path],
        )
        logger.info("Email picks PTHM inviata a %s (%d schede pending)",
                    recipients, len(rows))
        return True
    except Exception as e:
        logger.error("Errore invio email picks PTHM: %s", e, exc_info=True)
        _release_slot(conn, slot_key)
        conn.commit()
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────────────────────────────────────

def scheduler_loop():
    """Loop daemon: sweep PTHM ogni 60s + email giornaliera alle 7:00."""
    logger.info("Scheduler picks WIP attivo (sweep ogni %ds, email %02d:%02d)",
                POLL_INTERVAL_SEC, EMAIL_HOUR, EMAIL_MINUTE)
    while True:
        try:
            run_pthm_sweep()
        except Exception as e:
            logger.error("Errore sweep PTHM: %s", e, exc_info=True)

        # Email giornaliera: una tantum nella finestra EMAIL_HOUR:EMAIL_MINUTE
        try:
            now = datetime.now()
            if now.hour == EMAIL_HOUR and now.minute >= EMAIL_MINUTE:
                from wip_kanban import db
                conn = db.get_conn()
                try:
                    send_daily_email(conn)
                finally:
                    conn.close()
        except Exception as e:
            logger.error("Errore gestione email picks: %s", e, exc_info=True)

        time.sleep(POLL_INTERVAL_SEC)
