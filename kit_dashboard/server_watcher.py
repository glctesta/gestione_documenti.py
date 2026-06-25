# -*- coding: utf-8 -*-
"""
server_watcher.py — Verifica /health del web server e alert se DOWN.

Usato dalle istanze NON-host (e come ulteriore rete di sicurezza dall'host).
Decisione D2 = solo alert (nessun rilancio remoto). L'alert è:
  - popup ai PC `KIT_PREP` (riga in kit_popup_queue, mostrata da kit_popup_monitor)
  - email ai destinatari `Sys_email_Kit_materiali`
con **dedup atomico** (kit_dashboard_alert_log) per non spammare con più watcher.
"""
import socket
import logging
from datetime import datetime

logger = logging.getLogger("KitDashboard")


def check_health(cfg: dict, timeout: float = 4.0) -> bool:
    """True se il web server risponde 200 su /health.

    Usa urllib (stdlib, nessuna dipendenza da bundlare) e **bypassa il proxy**
    di sistema: gli IP intranet non devono passare per il proxy aziendale,
    altrimenti il controllo fallirebbe pur essendo il server raggiungibile.
    """
    import urllib.request
    url = f"http://{cfg['server_host_ip']}:{cfg['server_port']}{cfg.get('health_path','/health')}"
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url, timeout=timeout) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            return code == 200
    except Exception as e:
        logger.debug("check_health KO: %s", e)
        return False


def server_heartbeat_fresh(conn, cfg: dict) -> bool:
    """True se il server ha scritto un heartbeat recente in DB.

    Il web server aggiorna `kit_dashboard_controller.heartbeat_date` a ogni sync.
    Se è recente, il server è VIVO anche se questo PC non lo raggiunge via HTTP
    (proxy/rete locale) → niente alert.
    """
    try:
        max_min = int(cfg.get("sync_interval_minutes", 5)) * 2 + 3
        cur = conn.cursor()
        cur.execute("""
            SELECT CASE WHEN heartbeat_date IS NOT NULL
                        AND heartbeat_date > DATEADD(MINUTE, -?, GETDATE())
                   THEN 1 ELSE 0 END
            FROM Traceability_RS.dbo.kit_dashboard_controller
            WHERE lock_name = 'KIT_DASHBOARD'
        """, (max_min,))
        r = cur.fetchone()
        return bool(r and r[0])
    except Exception as e:
        logger.warning("server_heartbeat_fresh errore: %s", e)
        return False


ALERT_THROTTLE_DAYS = 5  # un solo warning ogni 5 giorni (richiesta utente)


def _alert_window_key(now: datetime, days: int = ALERT_THROTTLE_DAYS) -> str:
    """Chiave di dedup per finestra di N giorni. Il bucket (ordinale//N) rende
    la PK `alert_key` atomica: un solo alert per finestra fra tutti i watcher."""
    bucket = now.toordinal() // max(1, days)
    return f"SERVER_DOWN|D{bucket}"


def watcher_enabled(conn) -> bool:
    """False se l'alert Kit Dashboard è stato disattivato centralmente
    (Settings.Sys_kit_dashboard_watcher = OFF/0/no/false/disabled).
    Default: abilitato (retro-compatibile)."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT TOP 1 Value FROM Traceability_RS.dbo.Settings "
                    "WHERE Atribute = 'Sys_kit_dashboard_watcher'")
        r = cur.fetchone()
        if r and r[0] is not None:
            val = str(r[0]).strip().lower()
            if val in ('0', 'off', 'no', 'false', 'disabled', 'disattivo', 'spento'):
                return False
        return True
    except Exception as e:
        logger.debug("watcher_enabled check fallito (%s): assumo abilitato", e)
        return True


def claim_alert(conn, key: str, host: str) -> bool:
    """Claim atomico: ritorna True solo a chi vince (un alert per finestra)."""
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Traceability_RS.dbo.kit_dashboard_alert_log (alert_key, created_by)
        SELECT ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM Traceability_RS.dbo.kit_dashboard_alert_log
                          WHERE alert_key = ?)
    """, (key, host, key))
    won = cur.rowcount == 1
    conn.commit()
    return won


def send_alert(conn, cfg: dict):
    """Accoda popup KIT_PREP + invia email (dopo aver vinto il claim)."""
    host = cfg['server_host_ip']
    title = "⚠ Kit Dashboard NON raggiungibile"
    msg = (f"Il server della dashboard kit ({host}:{cfg['server_port']}) non risponde. "
           f"Verificare che il PC {host} e il servizio web siano attivi.")
    # Popup ai target configurati (default KIT_PREP). Categoria dedicata
    # 'KIT_DASHBOARD_DOWN' così il monitor può offrire la checkbox di silenziamento.
    from . import server_config
    cur = conn.cursor()
    for target in cfg.get('alert_targets', ['KIT_PREP']):
        cur.execute("""
            INSERT INTO Traceability_RS.dbo.kit_popup_queue
                (category, target, title, message, order_number)
            VALUES (?, ?, ?, ?, NULL)
        """, (server_config.CATEGORY_SERVER_DOWN, target, title[:200], msg[:1000]))
    conn.commit()
    # Email
    try:
        import utils
        recipients = utils.get_email_recipients(conn, cfg.get('email_setting', 'Sys_email_Kit_materiali'))
        if recipients:
            utils.send_email(recipients, "[ALERT] Kit Dashboard non raggiungibile", msg)
            logger.info("Alert email inviata a %d destinatari", len(recipients))
        else:
            logger.warning("Nessun destinatario per l'alert Kit Dashboard")
    except Exception as e:
        logger.error("Invio email alert fallito: %s", e)


def handle_down(conn, cfg: dict):
    """Gestisce un server DOWN: gate centralizzato + dedup (5 giorni) + alert."""
    if not watcher_enabled(conn):
        logger.info("Kit Dashboard watcher disattivato (Sys_kit_dashboard_watcher): nessun alert.")
        return
    host = socket.gethostname()
    key = _alert_window_key(datetime.now())
    try:
        if claim_alert(conn, key, host):
            logger.warning("Kit Dashboard DOWN: invio alert (%s)", key)
            send_alert(conn, cfg)
        else:
            logger.info("Kit Dashboard DOWN: alert già inviato negli ultimi %d giorni", ALERT_THROTTLE_DAYS)
    except Exception as e:
        logger.error("handle_down errore: %s", e, exc_info=True)
