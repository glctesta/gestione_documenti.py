# -*- coding: utf-8 -*-
"""
stale_clients_report.py — segnalazione dei PC fermi a una versione obsoleta.

Perche' esiste: quando l'aggiornamento automatico fallisce su un PC (percorso
sorgente non raggiungibile, dialogo di update morto, istanza mai riavviata) il
fallimento e' SILENZIOSO: il client ritenta ogni 15 minuti, non avvisa nessuno e
resta indietro per settimane. Il 31/07/2026 ne sono stati trovati 21, alcuni con
oltre 30 riavvii senza mai avanzare di versione, che continuavano a eseguire
logiche gia' disattivate (referat FAI).

I dati ci sono gia': sta.ProgramUsageSessions registra ad ogni avvio versione,
hostname, IP e istante. Qui si confrontano con la versione corrente pubblicata
in dbo.SWVersions e si manda un riepilogo a chi gestisce l'installato.

Uso:
    import stale_clients_report as scr
    sent, msg = scr.send_stale_clients_email(conn, mode=None, logo_path='logo.png')

Test manuale (nessun invio, stampa a video):
    python stale_clients_report.py
"""

import logging
import os
import sys
from datetime import datetime

logger = logging.getLogger("TraceabilityRS")

# Modalita' dedicata (settings.Atribute max 30 char)
EMAIL_MODE_SETTING = 'Sys_stale_clients_mode'      # 22 char
DEFAULT_EMAIL_MODE = 'Test'
RECIPIENTS_SETTING = 'Sys_stale_clients_email'     # 23 char
TEST_EMAIL = 'gianluca.testa@vandewiele.com'

# Dedup giornaliero cross-PC: prefisso + YYYYMMDD entro i 30 char di Atribute
SEND_SLOT_PREFIX = 'SentStaleClients_'             # 17 char + 8

# Non si giudica un PC sull'ULTIMA versione pubblicata: se e' uscita mezz'ora fa
# nessuno l'ha ancora presa. Il riferimento e' la versione piu' recente
# pubblicata da almeno GRACE_HOURS: chi non e' arrivato nemmeno a quella e'
# davvero indietro. Senza questa grazia il report griderebbe "al lupo" a ogni
# rilascio (il 31/07/2026: 40 falsi allarmi su 48 PC).
GRACE_HOURS = 24
# Finestra di analisi: oltre, il PC e' semplicemente spento da tempo.
LOOKBACK_DAYS = 14


def get_email_mode(conn) -> str:
    """'True' invio reale, 'Test' solo a TEST_EMAIL, 'False' disattivato."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT TOP 1 [value] FROM traceability_rs.dbo.settings "
                        "WHERE atribute = ?", (EMAIL_MODE_SETTING,))
            row = cur.fetchone()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"stale_clients: errore lettura {EMAIL_MODE_SETTING}: {e}")
    return DEFAULT_EMAIL_MODE


def get_current_version(conn) -> str:
    """Versione attualmente pubblicata per DocumentManagement.exe."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT TOP 1 Version FROM Traceability_RS.dbo.SWVersions
                WHERE NameProgram = 'DocumentManagement.exe' AND DateOut IS NULL
                ORDER BY Datesys DESC
            """)
            row = cur.fetchone()
        return str(row[0]).strip() if row and row[0] else ''
    except Exception as e:
        logger.error(f"stale_clients: errore lettura versione corrente: {e}")
        return ''


def get_reference_version(conn, grace_hours: int = GRACE_HOURS) -> tuple:
    """Versione di riferimento per il giudizio + istante di pubblicazione.

    E' la piu' alta fra quelle pubblicate da almeno `grace_hours` E non
    superiore a quella attualmente in distribuzione: lo storico di SWVersions
    contiene anche righe spurie (es. una '9.3.0.0' di gennaio 2026) che
    altrimenti diventerebbero il riferimento e farebbero risultare obsoleto
    l'intero parco macchine.
    Ritorna (versione, pubblicata_il); ('', None) se non determinabile.
    """
    current = get_current_version(conn)
    if not current:
        return '', None
    cur_key = _version_key(current)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT Version, MIN(Datesys) AS Pubblicata
                FROM Traceability_RS.dbo.SWVersions
                WHERE NameProgram = 'DocumentManagement.exe'
                  AND Datesys <= DATEADD(hour, -?, GETDATE())
                GROUP BY Version
            """, (grace_hours,))
            rows = [(str(r[0]).strip(), r[1]) for r in cur.fetchall()
                    if r[0] and _version_key(str(r[0]).strip()) <= cur_key]
        if not rows:
            return '', None
        return max(rows, key=lambda r: _version_key(r[0]))
    except Exception as e:
        logger.error(f"stale_clients: errore versione di riferimento: {e}")
        return '', None


def _version_key(v: str) -> tuple:
    """Versione come tupla di interi, per confronti corretti (2.4.2.10 > 2.4.2.9)."""
    out = []
    for part in str(v or '').split('.'):
        try:
            out.append(int(part))
        except ValueError:
            out.append(0)
    return tuple(out)


def get_client_versions(conn, lookback_days: int = LOOKBACK_DAYS) -> list:
    """Ultimo avvio per PC con versione, IP e numero di avvii nel periodo."""
    query = """
        WITH S AS (
            SELECT HostName, IpAddress, AppVersion, StartDateTime,
                   ROW_NUMBER() OVER (PARTITION BY HostName
                                      ORDER BY StartDateTime DESC) AS rn,
                   COUNT(*)    OVER (PARTITION BY HostName) AS Avvii,
                   MAX(AppVersion) OVER (PARTITION BY HostName) AS VerMax
            FROM sta.ProgramUsageSessions
            WHERE StartDateTime >= DATEADD(day, -?, GETDATE())
              AND ProgramName = 'DocumentManagement.exe'
        )
        SELECT HostName, IpAddress, AppVersion, StartDateTime, Avvii, VerMax
        FROM S WHERE rn = 1
    """
    rows = []
    try:
        with conn.cursor() as cur:
            cur.execute(query, (lookback_days,))
            for r in cur.fetchall():
                rows.append({
                    'host': r.HostName,
                    'ip': r.IpAddress,
                    'version': (r.AppVersion or '').strip(),
                    'last_start': r.StartDateTime,
                    'starts': r.Avvii,
                    'max_version': (r.VerMax or '').strip(),
                })
    except Exception as e:
        logger.error(f"stale_clients: errore lettura sessioni: {e}", exc_info=True)
    return rows


def analyze(conn, lookback_days: int = LOOKBACK_DAYS) -> dict:
    """Classifica i client rispetto alla versione di riferimento.

    'critici'  = il programma e' stato AVVIATO dopo la pubblicazione e gira
                 ancora vecchio: ha avuto l'occasione e non si e' aggiornato,
                 quindi l'update sta fallendo (sorgente irraggiungibile,
                 processo bloccato...).
    'indietro' = non riavviato dalla pubblicazione: PC spento o poco usato,
                 si allineera' alla prossima apertura.
    """
    current = get_current_version(conn)
    reference, published_at = get_reference_version(conn)
    clients = get_client_versions(conn, lookback_days)

    critici, indietro, aggiornati = [], [], []
    ref_key = _version_key(reference) if reference else None
    for c in clients:
        if not ref_key or _version_key(c['version']) >= ref_key:
            aggiornati.append(c)
            continue
        c['giorni_fermo'] = ((datetime.now() - c['last_start']).total_seconds() / 86400.0
                             if c['last_start'] else 999)
        ha_avuto_occasione = (published_at is not None and c['last_start'] is not None
                              and c['last_start'] >= published_at)
        (critici if ha_avuto_occasione else indietro).append(c)

    critici.sort(key=lambda c: (_version_key(c['version']), c['host']))
    indietro.sort(key=lambda c: c['host'])
    return {'current': current, 'reference': reference,
            'published_at': published_at, 'critici': critici,
            'indietro': indietro, 'aggiornati': aggiornati}


def _row_html(c, evidenzia=False):
    stile = ' style="background:#FFEBEE;"' if evidenzia else ''
    ultimo = c['last_start'].strftime('%d/%m/%Y %H:%M') if c['last_start'] else '—'
    return (f"<tr{stile}>"
            f"<td>{c['host']}</td><td>{c['ip'] or '—'}</td>"
            f"<td align='center'><b>{c['version']}</b></td>"
            f"<td align='center'>{c['starts']}</td>"
            f"<td>{ultimo}</td></tr>")


def build_html(data: dict) -> str:
    current = data['current']
    critici, indietro = data['critici'], data['indietro']
    head = ("<th>PC</th><th>IP</th><th>Versione</th>"
            "<th>Avvii (14gg)</th><th>Ultimo avvio</th>")
    riferimento = data.get('reference') or 'n/d'
    pubblicata = data.get('published_at')
    pub_str = pubblicata.strftime('%d/%m/%Y %H:%M') if pubblicata else 'n/d'
    parti = [
        "<div style=\"font-family:Segoe UI,Arial,sans-serif;font-size:13px;\">",
        f"<h2 style='color:#1F3864;'>Client con versione obsoleta</h2>",
        f"<p>Versione pubblicata: <b>{current or 'n/d'}</b>. "
        f"Riferimento del controllo: <b>{riferimento}</b> (in distribuzione dal "
        f"{pub_str}, oltre {GRACE_HOURS}h fa).<br>"
        f"Allineati {len(data['aggiornati'])} PC, "
        f"da verificare {len(critici) + len(indietro)}.</p>",
    ]
    if critici:
        parti.append(
            "<h3 style='color:#B71C1C;'>Aggiornamento che non riesce "
            f"({len(critici)})</h3>"
            "<p>Su questi PC il programma <b>e' stato avviato dopo</b> la "
            "pubblicazione e gira ancora una versione vecchia: ha avuto "
            "l'occasione di aggiornarsi e non l'ha fatto. Cause tipiche: "
            "percorso sorgente non raggiungibile dall'utente che esegue il "
            "programma (unita' di rete mappata assente), oppure processo di "
            "update bloccato.</p>"
            f"<table border='1' cellpadding='5' cellspacing='0' "
            f"style='border-collapse:collapse;'><tr style='background:#1F3864;"
            f"color:#fff;'>{head}</tr>"
            + "".join(_row_html(c, True) for c in critici) + "</table>")
    if indietro:
        parti.append(
            f"<h3 style='color:#E65100;'>Indietro di versione ({len(indietro)})</h3>"
            "<p>Non riavviati dalla pubblicazione: PC spenti o usati di rado, "
            "si allineeranno alla prossima apertura del programma.</p>"
            f"<table border='1' cellpadding='5' cellspacing='0' "
            f"style='border-collapse:collapse;'><tr style='background:#455A64;"
            f"color:#fff;'>{head}</tr>"
            + "".join(_row_html(c) for c in indietro) + "</table>")
    if not critici and not indietro:
        parti.append("<p style='color:#2E7D32;'><b>Tutti i PC sono allineati "
                     "alla versione pubblicata.</b></p>")
    parti.append(f"<p style='color:#888;font-size:11px;'>Generato il "
                 f"{datetime.now():%d/%m/%Y %H:%M} — dati da "
                 f"sta.ProgramUsageSessions (ultimi {LOOKBACK_DAYS} giorni).</p>")
    parti.append("</div>")
    return "".join(parti)


def _get_recipients(conn) -> list:
    """Destinatari da settings; se non configurati ripiega su TEST_EMAIL."""
    try:
        from utils import get_email_recipients
        dest = get_email_recipients(conn, attribute=RECIPIENTS_SETTING)
        if dest:
            return dest
    except Exception as e:
        logger.warning(f"stale_clients: destinatari non letti ({e})")
    return [TEST_EMAIL]


def _claim_send_slot(conn, setting_key: str) -> bool:
    """True se questo PC vince la corsa all'invio odierno (INSERT WHERE NOT EXISTS)."""
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO traceability_rs.dbo.settings (atribute, [value])
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM traceability_rs.dbo.settings
                WITH (UPDLOCK, HOLDLOCK) WHERE atribute = ?
            )
        """, (setting_key, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), setting_key))
        claimed = cur.rowcount > 0
        conn.commit()
        cur.close()
        return claimed
    except Exception as e:
        logger.error(f"stale_clients: _claim_send_slot: {e}", exc_info=True)
        return False


def send_stale_clients_email(conn, mode: str = None, logo_path: str = 'logo.png',
                             force: bool = False) -> tuple:
    """Invia il riepilogo dei client obsoleti. Ritorna (inviata, messaggio).

    Non invia nulla se tutti i PC sono allineati: l'email deve comparire solo
    quando c'e' qualcosa da fare.
    """
    if mode is None:
        mode = get_email_mode(conn)
    if str(mode).strip().lower() == 'false':
        return False, "modalita' 'False': invio disattivato"

    data = analyze(conn)
    if not data['critici'] and not data['indietro']:
        return False, "nessun client obsoleto: niente da segnalare"

    if not force:
        slot = SEND_SLOT_PREFIX + datetime.now().strftime('%Y%m%d')
        if not _claim_send_slot(conn, slot):
            return False, "gia' inviata oggi (o vinta da un altro PC)"

    to_emails = _get_recipients(conn)
    subj = (f"[Client obsoleti] {len(data['critici'])} PC non si aggiornano, "
            f"{len(data['indietro'])} indietro — versione {data['current']}")
    if str(mode).strip().lower() == 'test':
        subj = "[TEST] " + subj
        to_emails = [TEST_EMAIL]

    try:
        from email_connector import EmailSender
        sender = EmailSender()
        attachments = []
        if logo_path and os.path.exists(logo_path):
            attachments.append(('inline', logo_path, 'company_logo'))
        sender.send_email(
            to_email=to_emails[0],
            subject=subj,
            body=build_html(data),
            is_html=True,
            attachments=attachments or None,
            cc_emails=to_emails[1:] or None,
        )
        logger.info(f"stale_clients: report inviato a {to_emails} "
                    f"({len(data['critici'])} critici, {len(data['indietro'])} indietro)")
        return True, f"inviata a {', '.join(to_emails)}"
    except Exception as e:
        logger.error(f"stale_clients: errore invio: {e}", exc_info=True)
        return False, f"errore invio: {e}"


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pyodbc
    from database_config import DatabaseConfig
    _cn = pyodbc.connect(DatabaseConfig().get_connection_string(), timeout=60)
    _data = analyze(_cn)
    print(f"Versione pubblicata: {_data['current']}")
    print(f"Riferimento (>{GRACE_HOURS}h): {_data['reference']} "
          f"pubblicata il {_data['published_at']}")
    print(f"Allineati: {len(_data['aggiornati'])}")
    print(f"\nAGGIORNAMENTO CHE NON RIESCE ({len(_data['critici'])}):")
    for _c in _data['critici']:
        print(f"   {_c['host']:18} {str(_c['ip']):16} v{_c['version']:10} "
              f"{_c['starts']:3} avvii  ultimo {_c['last_start']:%d/%m %H:%M}")
    print(f"\nINDIETRO ({len(_data['indietro'])}):")
    for _c in _data['indietro']:
        print(f"   {_c['host']:18} v{_c['version']:10} {_c['starts']:3} avvii  "
              f"ultimo {_c['last_start']:%d/%m %H:%M}")
    _cn.close()
