"""
indirect_materials_stock_data.py
Layer dati per giacenze Materiali Indiretti basato sul libro movimenti
(ind.MaterialiMovimenti) e sulla vista ind.vw_GiacenzaCorrente.

Contiene:
  - lettura giacenze / movimenti
  - registrazione movimenti (carico/scarico/rettifica/inventario)
  - registra_scarico_richiesta(): transizione richiesta -> PRELEVATA + scarico
  - configurazione scorta minima (ind.MaterialiRiordino)
  - motore di riordino con invio email (dedup giornaliero su ind.RiordineEmailLog)

Nessuna dipendenza da tkinter: utilizzabile anche dallo scheduler di background.
"""

import logging
import socket
from datetime import datetime

logger = logging.getLogger(__name__)

# Attributo Settings con i destinatari email per gli acquisti indiretti
REORDER_EMAIL_ATTRIBUTE = 'sys_email_acquista_indiretti'


# ----------------------------------------------------------------------------
#  Lettura giacenze e movimenti
# ----------------------------------------------------------------------------
def get_giacenze(db, only_below=False):
    """Ritorna la giacenza corrente di tutti i materiali attivi.

    Ogni elemento e' un dict:
        materiale_id, codice, descrizione, tipo, giacenza, ultimo_movimento,
        livello_minimo, lotto_riordino, is_riordino_attivo, sotto_soglia
    Se only_below=True ritorna solo i materiali sotto la scorta minima
    (con riordino attivo e soglia configurata).
    """
    query = """
        SELECT g.MaterialeId, g.CodiceMateriale, g.DescrizioneMateriale,
               ISNULL(t.Tipo, 'Generico') AS Tipo,
               g.Giacenza, g.UltimoMovimento,
               r.LivelloMinimo, r.LottoRiordino, r.IsAttivo
        FROM ind.vw_GiacenzaCorrente g
        LEFT JOIN ind.TipoMateriali t ON t.TipoMaterialeId = g.TipoMaterialeId
        LEFT JOIN ind.MaterialiRiordino r ON r.MaterialeId = g.MaterialeId
        ORDER BY g.CodiceMateriale
    """
    rows = db.fetch_all(query)
    result = []
    for row in (rows or []):
        livello_min = float(row[6]) if row[6] is not None else None
        is_attivo = bool(row[8]) if row[8] is not None else False
        giacenza = float(row[4] or 0)
        sotto_soglia = (is_attivo and livello_min is not None and giacenza < livello_min)
        item = {
            'materiale_id': row[0],
            'codice': row[1] or '',
            'descrizione': row[2] or '',
            'tipo': row[3] or 'Generico',
            'giacenza': giacenza,
            'ultimo_movimento': row[5],
            'livello_minimo': livello_min,
            'lotto_riordino': float(row[7]) if row[7] is not None else None,
            'is_riordino_attivo': is_attivo,
            'sotto_soglia': sotto_soglia,
        }
        if only_below and not sotto_soglia:
            continue
        result.append(item)
    return result


def get_movimenti(db, materiale_id, limit=200):
    """Ritorna gli ultimi movimenti di un materiale (piu' recenti per primi)."""
    query = """
        SELECT TOP (?) mv.MovimentoId, mv.DataMovimento, mv.TipoMovimento,
               mv.Qty, mv.RichiestaId, mv.EseguitoDa, mv.ComputerSrc, mv.Note
        FROM ind.MaterialiMovimenti mv
        WHERE mv.MaterialeId = ?
        ORDER BY mv.DataMovimento DESC, mv.MovimentoId DESC
    """
    rows = db.fetch_all(query, (limit, materiale_id))
    return [{
        'movimento_id': r[0],
        'data': r[1],
        'tipo': r[2],
        'qty': float(r[3] or 0),
        'richiesta_id': r[4],
        'eseguito_da': r[5] or '',
        'computer': r[6] or '',
        'note': r[7] or '',
    } for r in (rows or [])]


# ----------------------------------------------------------------------------
#  Registrazione movimenti
# ----------------------------------------------------------------------------
def registra_movimento(db, materiale_id, qty, tipo, user_name,
                       hostname=None, richiesta_id=None, note=None):
    """Inserisce un singolo movimento. qty con segno (+carico / -scarico).
    tipo in CARICO / SCARICO / RETTIFICA / INVENTARIO. Ritorna (ok, msg)."""
    if tipo not in ('CARICO', 'SCARICO', 'RETTIFICA', 'INVENTARIO'):
        return False, f"Tipo movimento non valido: {tipo}"
    hostname = hostname or socket.gethostname()
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute(
                "INSERT INTO ind.MaterialiMovimenti "
                "(MaterialeId, Qty, TipoMovimento, RichiestaId, EseguitoDa, ComputerSrc, Note) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (materiale_id, qty, tipo, richiesta_id, user_name, hostname, note)
            )
            db.conn.commit()
            return True, "ok"
        except Exception as e:
            db.conn.rollback()
            logger.error(f"registra_movimento errore: {e}", exc_info=True)
            return False, str(e)


def registra_scarico_richiesta(db, richiesta_id, user_name, hostname=None):
    """Porta una richiesta a stato PRELEVATA e genera il movimento di SCARICO
    (Qty negativa = -QtaRichiesta) collegato, in un'unica transazione.

    Idempotente: se la richiesta e' gia' PRELEVATA o lo scarico esiste gia',
    non duplica. Ritorna (ok, code) dove code in:
        'ok', 'not_found', 'already', 'annullata', 'error'
    """
    hostname = hostname or socket.gethostname()
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute(
                "SELECT Stato, MaterialeId, QtaRichiesta "
                "FROM ind.MaterialiRichieste WHERE RichiestaId = ?",
                (richiesta_id,)
            )
            row = cur.fetchone()
            if not row:
                return False, 'not_found'
            stato, materiale_id, qta = row[0], row[1], float(row[2] or 0)
            if stato == 'PRELEVATA':
                return False, 'already'
            if stato == 'ANNULLATA':
                return False, 'annullata'

            # Transizione di stato
            cur.execute(
                "UPDATE ind.MaterialiRichieste "
                "SET Stato = 'PRELEVATA', DataPrelievo = GETDATE() "
                "WHERE RichiestaId = ? AND Stato <> 'PRELEVATA'",
                (richiesta_id,)
            )
            # Movimento di scarico, solo se non gia' presente per la richiesta
            cur.execute(
                "INSERT INTO ind.MaterialiMovimenti "
                "(MaterialeId, Qty, TipoMovimento, RichiestaId, EseguitoDa, ComputerSrc, Note) "
                "SELECT ?, ?, 'SCARICO', ?, ?, ?, ? "
                "WHERE NOT EXISTS (SELECT 1 FROM ind.MaterialiMovimenti "
                "                  WHERE RichiestaId = ? AND TipoMovimento = 'SCARICO')",
                (materiale_id, -abs(qta), richiesta_id, user_name, hostname,
                 'Scarico da richiesta PRELEVATA', richiesta_id)
            )
            db.conn.commit()
            logger.info(f"Scarico registrato per richiesta {richiesta_id} "
                        f"(materiale {materiale_id}, qty -{abs(qta)})")
            return True, 'ok'
        except Exception as e:
            db.conn.rollback()
            logger.error(f"registra_scarico_richiesta errore: {e}", exc_info=True)
            return False, 'error'


def avanza_stato_richiesta(db, richiesta_id, nuovo_stato, user_name):
    """Avanza lo stato di una richiesta verso PREPARATA / PRONTA / ANNULLATA.
    Per PRELEVATA usare registra_scarico_richiesta(). Ritorna (ok, msg)."""
    if nuovo_stato not in ('PREPARATA', 'PRONTA', 'ANNULLATA'):
        return False, f"Stato non gestito qui: {nuovo_stato}"
    set_parts = ["Stato = ?"]
    params = [nuovo_stato]
    if nuovo_stato == 'PREPARATA':
        set_parts.append("DataPreparazione = GETDATE()")
        set_parts.append("PreparatoDa = ?")
        params.append(user_name)
    params.append(richiesta_id)
    sql = (f"UPDATE ind.MaterialiRichieste SET {', '.join(set_parts)} "
           f"WHERE RichiestaId = ? AND Stato NOT IN ('PRELEVATA','ANNULLATA')")
    ok = db.execute_query(sql, tuple(params))
    return ok, ('ok' if ok else 'error')


# ----------------------------------------------------------------------------
#  Configurazione scorta minima
# ----------------------------------------------------------------------------
def get_min_config(db, materiale_id):
    """Ritorna la config riordino di un materiale o None."""
    row = db.fetch_one(
        "SELECT LivelloMinimo, LottoRiordino, IsAttivo "
        "FROM ind.MaterialiRiordino WHERE MaterialeId = ?",
        (materiale_id,)
    )
    if not row:
        return None
    return {
        'livello_minimo': float(row[0]) if row[0] is not None else None,
        'lotto_riordino': float(row[1]) if row[1] is not None else None,
        'is_attivo': bool(row[2]),
    }


def upsert_min_config(db, materiale_id, livello_minimo, lotto_riordino,
                      is_attivo, user_name):
    """Crea o aggiorna la configurazione scorta minima di un materiale.
    Ritorna (ok, msg)."""
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute(
                "UPDATE ind.MaterialiRiordino "
                "SET LivelloMinimo = ?, LottoRiordino = ?, IsAttivo = ?, "
                "    DataModifica = GETDATE(), ModificatoDa = ? "
                "WHERE MaterialeId = ?",
                (livello_minimo, lotto_riordino, 1 if is_attivo else 0,
                 user_name, materiale_id)
            )
            if cur.rowcount == 0:
                cur.execute(
                    "INSERT INTO ind.MaterialiRiordino "
                    "(MaterialeId, LivelloMinimo, LottoRiordino, IsAttivo, ModificatoDa) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (materiale_id, livello_minimo, lotto_riordino,
                     1 if is_attivo else 0, user_name)
                )
            db.conn.commit()
            return True, "ok"
        except Exception as e:
            db.conn.rollback()
            logger.error(f"upsert_min_config errore: {e}", exc_info=True)
            return False, str(e)


# ----------------------------------------------------------------------------
#  Motore di riordino
# ----------------------------------------------------------------------------
def _get_reorder_recipients(db):
    """Ritorna la lista di email destinatari del riordino (da Settings)."""
    try:
        from utils import get_email_recipients
        return get_email_recipients(db.conn, attribute=REORDER_EMAIL_ATTRIBUTE)
    except Exception as e:
        logger.error(f"Errore lettura destinatari riordino: {e}", exc_info=True)
        # Fallback: lettura diretta del setting
        raw = db.fetch_setting(REORDER_EMAIL_ATTRIBUTE) if hasattr(db, 'fetch_setting') else None
        if not raw:
            return []
        parts = [p.strip() for p in raw.replace(',', ';').split(';')]
        return [p for p in parts if p and '@' in p]


def _filter_not_sent_today(db, items):
    """Esclude i materiali per cui e' gia' stata inviata una email riordino oggi
    (dedup giornaliero su ind.RiordineEmailLog)."""
    fresh = []
    for it in items:
        row = db.fetch_one(
            "SELECT 1 FROM ind.RiordineEmailLog "
            "WHERE MaterialeId = ? AND CAST(DataInvio AS DATE) = CAST(GETDATE() AS DATE)",
            (it['materiale_id'],)
        )
        if not row:
            fresh.append(it)
    return fresh


def _log_reorder_sent(db, items, recipients):
    """Registra l'invio email riordino per dedup futuro."""
    inviato_a = '; '.join(recipients)[:255]
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            for it in items:
                cur.execute(
                    "INSERT INTO ind.RiordineEmailLog "
                    "(MaterialeId, GiacenzaRilevata, LivelloMinimo, InviatoA) "
                    "VALUES (?, ?, ?, ?)",
                    (it['materiale_id'], it['giacenza'], it['livello_minimo'], inviato_a)
                )
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            logger.error(f"_log_reorder_sent errore: {e}", exc_info=True)


def _build_reorder_email(lang, items):
    """Costruisce (subject, html_body) dell'email di riordino, tradotti."""
    def t(key, default):
        try:
            return lang.get(key, default)
        except Exception:
            return default

    subject = t('ind_reorder_email_subject',
                'Richiesta riordino materiali indiretti sotto scorta minima')
    intro = t('ind_reorder_email_intro',
              'I seguenti materiali indiretti sono scesi sotto la scorta minima e necessitano di riordino:')
    col_code = t('ind_import_col_code', 'Codice')
    col_desc = t('ind_import_col_desc', 'Descrizione')
    col_stock = t('ind_stock_col_stock', 'Giacenza')
    col_min = t('ind_min_col_min', 'Scorta minima')
    col_lotto = t('ind_min_col_lot', 'Lotto riordino')
    footer = t('ind_reorder_email_footer',
               'Email generata automaticamente dal sistema Document Management.')

    rows_html = []
    for it in items:
        lotto = it.get('lotto_riordino')
        lotto_str = f"{lotto:.2f}" if lotto is not None else '-'
        rows_html.append(
            "<tr>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['codice']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['descrizione']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{it['giacenza']:.2f}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{it['livello_minimo']:.2f}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{lotto_str}</td>"
            "</tr>"
        )

    body = (
        f"<p>{intro}</p>"
        "<table style='border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px;'>"
        "<thead><tr style='background:#f0f0f0;'>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_code}</th>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_desc}</th>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_stock}</th>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_min}</th>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_lotto}</th>"
        "</tr></thead><tbody>"
        + ''.join(rows_html) +
        "</tbody></table>"
        f"<p style='color:#888;font-size:11px;margin-top:16px;'>{footer}</p>"
    )
    return subject, body


def check_and_send_reorder(db, lang, force=False):
    """Verifica i materiali sotto scorta minima e invia l'email di riordino.

    Args:
        force: se True ignora il dedup giornaliero (invio manuale on-demand).

    Ritorna dict: {sent: bool, count: int, recipients: list, reason: str}
    """
    below = get_giacenze(db, only_below=True)
    if not below:
        return {'sent': False, 'count': 0, 'recipients': [], 'reason': 'no_items'}

    to_send = below if force else _filter_not_sent_today(db, below)
    if not to_send:
        return {'sent': False, 'count': 0, 'recipients': [], 'reason': 'already_sent_today'}

    recipients = _get_reorder_recipients(db)
    if not recipients:
        logger.warning(f"Riordino: nessun destinatario configurato in Settings.{REORDER_EMAIL_ATTRIBUTE}")
        return {'sent': False, 'count': len(to_send), 'recipients': [], 'reason': 'no_recipients'}

    subject, body = _build_reorder_email(lang, to_send)
    try:
        from email_connector import EmailSender
        sender = EmailSender()
        for addr in recipients:
            sender.send_email(to_email=addr, subject=subject, body=body, is_html=True)
        _log_reorder_sent(db, to_send, recipients)
        logger.info(f"Riordino: email inviata a {len(recipients)} destinatari per {len(to_send)} materiali.")
        return {'sent': True, 'count': len(to_send), 'recipients': recipients, 'reason': 'ok'}
    except Exception as e:
        logger.error(f"Riordino: errore invio email: {e}", exc_info=True)
        return {'sent': False, 'count': len(to_send), 'recipients': recipients, 'reason': f'error: {e}'}
