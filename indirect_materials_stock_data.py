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

_reorder_cols_ensured = False


def _ensure_reorder_columns(db):
    """Aggiunge la colonna LivelloRaccomandato a ind.MaterialiRiordino se manca
    (idempotente, una sola volta per processo). Il minimo resta la soglia critica;
    il raccomandato è il livello-obiettivo fino a cui riordinare."""
    global _reorder_cols_ensured
    if _reorder_cols_ensured:
        return
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                "IF NOT EXISTS (SELECT 1 FROM sys.columns "
                "  WHERE object_id = OBJECT_ID('ind.MaterialiRiordino') "
                "    AND name = 'LivelloRaccomandato') "
                "ALTER TABLE ind.MaterialiRiordino ADD LivelloRaccomandato DECIMAL(18,3) NULL"
            )
            db.conn.commit()
        _reorder_cols_ensured = True
    except Exception as e:
        logger.warning(f"_ensure_reorder_columns: {e}")


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
    _ensure_reorder_columns(db)
    query = """
        SELECT g.MaterialeId, g.CodiceMateriale, g.DescrizioneMateriale,
               ISNULL(t.Tipo, 'Generico') AS Tipo,
               g.Giacenza, g.UltimoMovimento,
               r.LivelloMinimo, r.LottoRiordino, r.IsAttivo, r.LivelloRaccomandato
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
        raccomandato = float(row[9]) if row[9] is not None else None
        lotto = float(row[7]) if row[7] is not None else None
        giacenza = float(row[4] or 0)
        sotto_soglia = (is_attivo and livello_min is not None and giacenza <= livello_min)
        # Quantità suggerita da riordinare: fino al raccomandato se impostato,
        # altrimenti il lotto di riordino.
        if raccomandato is not None and raccomandato > giacenza:
            qta_riordino = raccomandato - giacenza
        else:
            qta_riordino = lotto
        item = {
            'materiale_id': row[0],
            'codice': row[1] or '',
            'descrizione': row[2] or '',
            'tipo': row[3] or 'Generico',
            'giacenza': giacenza,
            'ultimo_movimento': row[5],
            'livello_minimo': livello_min,
            'lotto_riordino': lotto,
            'livello_raccomandato': raccomandato,
            'qta_da_riordinare': qta_riordino,
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


def scorie_confermate_per_richiesta(db, richiesta_id):
    """Verifica il gate scorie/rientri per una richiesta.

    Una richiesta il cui materiale ha una regola attiva in dbo.MaterialRules
    (cioe' e' legato al ritorno di un altro materiale o dello stesso codice)
    puo' essere preparata/rilasciata SOLO se:
      1) esiste almeno una scoria collegata alla richiesta
         (dbo.ReturnMaterials.RichiestaId = richiesta), e
      2) NON esiste ALCUNA scoria PENDENTE del MustCode collegato al materiale,
         cioe' nessuna riga dbo.ReturnMaterials del MustCode con IsOk NULL/0 e
         DateOut IS NULL (a prescindere dall'aggancio alla richiesta).
    Il punto 2 e' globale sul codice: le quantita' restituite in eccesso (non
    agganciate per il cap D7) o dichiarate dopo l'invio devono comunque essere
    validate dal magazzino prima di poter rilasciare lo stesso codice.

    Ritorna (allowed: bool, code: str) con code in:
        'ok' | 'scrap_not_confirmed' | 'not_found' | 'error'
    """
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM dbo.MaterialRules mr
                       WHERE mr.MaterialeId = r.MaterialeId AND mr.DateOut IS NULL) AS HasRule,
                    (SELECT COUNT(*) FROM dbo.ReturnMaterials rm
                       WHERE rm.RichiestaId = ? AND rm.DateOut IS NULL) AS LinkedCount,
                    (SELECT COUNT(*) FROM dbo.ReturnMaterials rm
                       INNER JOIN dbo.MaterialRules mr2 ON mr2.MustCodeId = rm.MateriaId
                       WHERE mr2.MaterialeId = r.MaterialeId AND mr2.DateOut IS NULL
                         AND rm.DateOut IS NULL AND ISNULL(rm.IsOk, 0) = 0) AS PendingCount
                FROM ind.MaterialiRichieste r
                WHERE r.RichiestaId = ?
                """,
                (richiesta_id, richiesta_id)
            )
            row = cur.fetchone()
        if not row:
            return False, 'not_found'
        has_rule = int(row[0] or 0)
        linked = int(row[1] or 0)
        pending = int(row[2] or 0)               # scorie pendenti del MustCode (globale sul codice)
        if has_rule == 0:
            return True, 'ok'                      # materiale non legato a ritorni
        if linked > 0 and pending == 0:
            return True, 'ok'                      # scoria agganciata e nessuna pendente sul codice
        logger.info(
            f"[ScrapGate] Richiesta {richiesta_id} BLOCCATA: has_rule={has_rule}, "
            f"linked={linked}, pendenti_codice={pending}"
        )
        return False, 'scrap_not_confirmed'
    except Exception as e:
        logger.error(f"scorie_confermate_per_richiesta errore: {e}", exc_info=True)
        return False, 'error'


def _esegui_scarico(db, richiesta_id, user_name, hostname):
    """Nucleo: transizione a PRELEVATA + movimento di SCARICO in un'unica
    transazione. NON applica il gate scorie/rientri, perche' dipende dal punto
    del flusso (vedi registra_scarico_richiesta e conferma_ritiro_richiesta).

    Idempotente: se la richiesta e' gia' PRELEVATA o lo scarico esiste gia',
    non duplica. Ritorna (ok, code) con code in:
        'ok', 'not_found', 'already', 'annullata', 'error'
    """
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute(
                "SELECT Stato, MaterialeId, QtaRichiesta, RichiestoDa "
                "FROM ind.MaterialiRichieste WHERE RichiestaId = ?",
                (richiesta_id,)
            )
            row = cur.fetchone()
            if not row:
                return False, 'not_found'
            stato, materiale_id, qta = row[0], row[1], float(row[2] or 0)
            user_name = user_name or row[3] or hostname
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
                        f"(materiale {materiale_id}, qty -{abs(qta)}, da {user_name})")
            return True, 'ok'
        except Exception as e:
            db.conn.rollback()
            logger.error(f"_esegui_scarico errore: {e}", exc_info=True)
            return False, 'error'


def registra_scarico_richiesta(db, richiesta_id, user_name, hostname=None):
    """Rilascio dal magazzino: porta la richiesta a PRELEVATA e genera lo scarico.

    Passa dal gate scorie/rientri: qui il materiale sta per uscire, quindi se le
    scorie collegate non sono confermate il rilascio va bloccato.

    Ritorna (ok, code) con code in:
        'ok', 'not_found', 'already', 'annullata', 'scrap_not_confirmed', 'error'
    """
    allowed, gate_code = scorie_confermate_per_richiesta(db, richiesta_id)
    if not allowed and gate_code == 'scrap_not_confirmed':
        return False, 'scrap_not_confirmed'
    return _esegui_scarico(db, richiesta_id, user_name,
                           hostname or socket.gethostname())


def conferma_ritiro_richiesta(db, richiesta_id, user_name=None, hostname=None):
    """Conferma del RITIRO da parte del richiedente (popup "Ritirato").

    Stessa transizione di registra_scarico_richiesta ma SENZA il gate scorie: a
    questo punto il materiale e' gia' fisicamente in mano all'operatore e
    bloccare la conferma lascerebbe la richiesta aperta.

    Serve perche' questo percorso faceva una UPDATE secca sullo stato senza
    scrivere nulla nel libro movimenti: e' li' che il consumo spariva (1008
    prelievi, 247.362 pezzi, mai contabilizzati) e per cui la giacenza scendeva
    solo al successivo import del file Excel, ritardando le soglie di riordino.

    Se user_name non e' noto (il monitor identifica il PC, non la persona) usa
    il richiedente registrato sulla richiesta.
    """
    return _esegui_scarico(db, richiesta_id, user_name,
                           hostname or socket.gethostname())


def avanza_stato_richiesta(db, richiesta_id, nuovo_stato, user_name):
    """Avanza lo stato di una richiesta verso PREPARATA / PRONTA / ANNULLATA.
    Per PRELEVATA usare registra_scarico_richiesta(). Ritorna (ok, msg)."""
    if nuovo_stato not in ('PREPARATA', 'PRONTA', 'ANNULLATA'):
        return False, f"Stato non gestito qui: {nuovo_stato}"
    # Gate scorie/rientri: blocca la preparazione se le scorie collegate non sono confermate
    if nuovo_stato == 'PREPARATA':
        allowed, gate_code = scorie_confermate_per_richiesta(db, richiesta_id)
        if not allowed and gate_code == 'scrap_not_confirmed':
            return False, 'scrap_not_confirmed'
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
    _ensure_reorder_columns(db)
    row = db.fetch_one(
        "SELECT LivelloMinimo, LottoRiordino, IsAttivo, LivelloRaccomandato "
        "FROM ind.MaterialiRiordino WHERE MaterialeId = ?",
        (materiale_id,)
    )
    if not row:
        return None
    return {
        'livello_minimo': float(row[0]) if row[0] is not None else None,
        'lotto_riordino': float(row[1]) if row[1] is not None else None,
        'is_attivo': bool(row[2]),
        'livello_raccomandato': float(row[3]) if row[3] is not None else None,
    }


def upsert_min_config(db, materiale_id, livello_minimo, lotto_riordino,
                      is_attivo, user_name, livello_raccomandato=None):
    """Crea o aggiorna la configurazione scorta minima/raccomandata di un materiale.
    Ritorna (ok, msg)."""
    _ensure_reorder_columns(db)
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute(
                "UPDATE ind.MaterialiRiordino "
                "SET LivelloMinimo = ?, LottoRiordino = ?, IsAttivo = ?, "
                "    LivelloRaccomandato = ?, DataModifica = GETDATE(), ModificatoDa = ? "
                "WHERE MaterialeId = ?",
                (livello_minimo, lotto_riordino, 1 if is_attivo else 0,
                 livello_raccomandato, user_name, materiale_id)
            )
            if cur.rowcount == 0:
                cur.execute(
                    "INSERT INTO ind.MaterialiRiordino "
                    "(MaterialeId, LivelloMinimo, LottoRiordino, IsAttivo, "
                    " LivelloRaccomandato, ModificatoDa) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (materiale_id, livello_minimo, lotto_riordino,
                     1 if is_attivo else 0, livello_raccomandato, user_name)
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


def _claim_materials_today(db, items, recipients):
    """Prenota ATOMICAMENTE l'invio odierno per ciascun materiale (INSERT ...
    WHERE NOT EXISTS per la data di oggi in ind.RiordineEmailLog) e ritorna solo
    i materiali effettivamente prenotati da QUESTO processo (cur.rowcount > 0).

    Sostituisce il vecchio check-then-act: con il recupero all'avvio più PC
    possono partire in contemporanea la mattina — la prenotazione atomica
    garantisce che ogni materiale finisca in UNA sola email (niente doppioni)."""
    inviato_a = '; '.join(recipients)[:255]
    claimed = []
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        for it in items:
            try:
                cur.execute(
                    "INSERT INTO ind.RiordineEmailLog "
                    "(MaterialeId, GiacenzaRilevata, LivelloMinimo, QtaSuggerita, Stato, InviatoA) "
                    "SELECT ?, ?, ?, ?, 'INVIATO', ? "
                    "WHERE NOT EXISTS (SELECT 1 FROM ind.RiordineEmailLog WITH (UPDLOCK, HOLDLOCK) "
                    "  WHERE MaterialeId = ? AND Stato = 'INVIATO' "
                    "    AND CAST(DataInvio AS DATE) = CAST(GETDATE() AS DATE))",
                    (it['materiale_id'], it['giacenza'], it['livello_minimo'],
                     it.get('qta_da_riordinare'), inviato_a, it['materiale_id'])
                )
                if cur.rowcount and cur.rowcount > 0:
                    claimed.append(it)
            except Exception as e:
                logger.error(f"_claim_materials_today {it.get('materiale_id')}: {e}")
        db.conn.commit()
    return claimed


def _unclaim_materials_today(db, items):
    """Rilascia le prenotazioni odierne dei materiali indicati (usato se l'invio
    email fallisce, così il controllo successivo può ritentare)."""
    if not items:
        return
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            for it in items:
                cur.execute(
                    "DELETE FROM ind.RiordineEmailLog "
                    "WHERE MaterialeId = ? AND CAST(DataInvio AS DATE) = CAST(GETDATE() AS DATE)",
                    (it['materiale_id'],)
                )
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            logger.error(f"_unclaim_materials_today errore: {e}", exc_info=True)


def _log_reorder_sent(db, items, recipients):
    """Registra l'invio email riordino per dedup futuro (modalità force/on-demand)."""
    inviato_a = '; '.join(recipients)[:255]
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            for it in items:
                cur.execute(
                    "INSERT INTO ind.RiordineEmailLog "
                    "(MaterialeId, GiacenzaRilevata, LivelloMinimo, QtaSuggerita, Stato, InviatoA) "
                    "SELECT ?, ?, ?, ?, 'INVIATO', ? "
                    "WHERE NOT EXISTS (SELECT 1 FROM ind.RiordineEmailLog "
                    "  WHERE MaterialeId = ? AND Stato = 'INVIATO' "
                    "    AND CAST(DataInvio AS DATE) = CAST(GETDATE() AS DATE))",
                    (it['materiale_id'], it['giacenza'], it['livello_minimo'],
                     it.get('qta_da_riordinare'), inviato_a, it['materiale_id'])
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
    col_racc = t('ind_min_col_recommended', 'Scorta raccomandata')
    col_qty = t('ind_reorder_col_qty', 'Qta da riordinare')
    footer = t('ind_reorder_email_footer',
               'Email generata automaticamente dal sistema Document Management.')

    rows_html = []
    for it in items:
        racc = it.get('livello_raccomandato')
        racc_str = f"{racc:.2f}" if racc is not None else '-'
        qta = it.get('qta_da_riordinare')
        qta_str = f"{qta:.2f}" if qta is not None else '-'
        rows_html.append(
            "<tr>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['codice']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['descrizione']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{it['giacenza']:.2f}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{it['livello_minimo']:.2f}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{racc_str}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;font-weight:bold;'>{qta_str}</td>"
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
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_racc}</th>"
        f"<th style='border:1px solid #ccc;padding:6px;'>{col_qty}</th>"
        "</tr></thead><tbody>"
        + ''.join(rows_html) +
        "</tbody></table>"
        f"<p style='color:#888;font-size:11px;margin-top:16px;'>{footer}</p>"
    )
    return subject, body


def _build_purchasing_reminder_email(items):
    """Costruisce il corpo HTML dell'email di reminder acquisti in inglese."""
    headers = [
        'Material Code', 'Description', 'Requested Qty', 'Reiterations',
        'Business Days Pending', 'Days Since First Request'
    ]
    rows_html = []
    for it in items:
        qta_str = f"{it['qta']:.2f}" if it['qta'] is not None else '-'
        rows_html.append(
            "<tr>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['codice']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;'>{it['descrizione']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:right;'>{qta_str}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:center;'>{it['reminder_count']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:center;'>{it['business_days']}</td>"
            f"<td style='border:1px solid #ccc;padding:6px;text-align:center;'>{it['calendar_days']}</td>"
            "</tr>"
        )

    body = (
        "<p>Dear Purchasing Team,</p>"
        "<p>The following indirect materials are still pending purchase order confirmation. "
        "Please review and update the order status via the <strong>Conferma ordini</strong> form.</p>"
        "<table style='border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px;'>"
        "<thead><tr style='background:#f0f0f0;'>"
        + ''.join(f"<th style='border:1px solid #ccc;padding:6px;'>{h}</th>" for h in headers) +
        "</tr></thead><tbody>"
        + ''.join(rows_html) +
        "</tbody></table>"
        "<p style='color:#888;font-size:11px;margin-top:16px;'>"
        "This is an automatic reminder sent by the Document Management system.</p>"
    )
    return body


def check_and_send_purchasing_reminder(db, lang, country_code='RO'):
    """Verifica i solleciti di acquisto non confermati e, ogni 2 giorni lavorativi,
    invia un reminder email in inglese agli acquisti.
    Ritorna dict: {sent, count, recipients, reason}.

    Usa email_job_coordinator per garantire UN SOLO invio cross-PC.
    """
    from business_days import count_business_days_between, is_business_day
    from email_job_coordinator import claim_job_run, release_job_lock, log_job_run

    if not is_business_day(country_code=country_code):
        return {'sent': False, 'count': 0, 'reason': 'not_business_day'}

    job_name = 'purchasing_reminder'
    if not claim_job_run(db, job_name, lock_minutes=120):
        return {'sent': False, 'count': 0, 'reason': 'locked_or_disabled'}

    email_sent = False

    try:
        recipients = _get_reorder_recipients(db)
        if not recipients:
            release_job_lock(db, job_name)
            log_job_run(db, job_name, 'SKIPPED', 'nessun destinatario configurato')
            return {'sent': False, 'count': 0, 'reason': 'no_recipients'}

        rows = db.fetch_all(
            """
            SELECT l.RiordineLogId, m.CodiceMateriale, m.DescrizioneMateriale,
                   l.QtaSuggerita, l.DataInvio, l.ReminderCount
            FROM Traceability_RS.ind.RiordineEmailLog l
            JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = l.MaterialeId
            WHERE l.Stato = 'INVIATO'
              AND l.DataInvio >= DATEADD(DAY, -60, GETDATE())
            ORDER BY l.DataInvio ASC
            """
        )

        today = datetime.now().date()
        items = []
        for row in (rows or []):
            log_id, codice, descrizione, qta, data_invio, reminder_count = row
            business_days = count_business_days_between(data_invio, today, country_code=country_code)
            calendar_days = (today - data_invio.date()).days if data_invio else 0
            # Reminder ogni 2 giorni lavorativi rispetto alla prima richiesta.
            if business_days >= 2 * ((reminder_count or 0) + 1):
                items.append({
                    'log_id': log_id,
                    'codice': codice or '',
                    'descrizione': descrizione or '',
                    'qta': float(qta) if qta is not None else None,
                    'business_days': business_days,
                    'calendar_days': calendar_days,
                    'reminder_count': reminder_count or 0,
                })

        if not items:
            release_job_lock(db, job_name)
            log_job_run(db, job_name, 'SKIPPED', 'nessun reminder dovuto')
            return {'sent': False, 'count': 0, 'reason': 'no_reminders_due'}

        subject = "Indirect Materials Purchase Orders - Pending Confirmation Reminder"
        body = _build_purchasing_reminder_email(items)

        try:
            from email_connector import EmailSender
            sender = EmailSender()
            sender.send_email(to_email='; '.join(recipients), subject=subject,
                              body=body, is_html=True)
            email_sent = True
        except Exception as e:
            logger.error(f"Errore invio reminder acquisti: {e}", exc_info=True)
            release_job_lock(db, job_name)
            log_job_run(db, job_name, 'ERROR', f"errore invio: {e}")
            return {'sent': False, 'count': len(items), 'reason': f'error: {e}'}

        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            try:
                for it in items:
                    cur.execute(
                        "UPDATE ind.RiordineEmailLog "
                        "SET ReminderCount = ReminderCount + 1, DataUltimoReminder = GETDATE() "
                        "WHERE RiordineLogId = ?",
                        (it['log_id'],)
                    )
                db.conn.commit()
                logger.info(f"Reminder acquisti inviato per {len(items)} materiali.")
                log_job_run(
                    db, job_name, 'OK',
                    f"inviati {len(items)} materiali a {len(recipients)} destinatari"
                )
                return {'sent': True, 'count': len(items), 'recipients': recipients, 'reason': 'ok'}
            except Exception as e:
                db.conn.rollback()
                logger.error(f"Errore aggiornamento reminder count: {e}", exc_info=True)
                # L'email e' gia' stata consegnata: non rilasciare il lock per non re-inviare.
                log_job_run(
                    db, job_name, 'OK',
                    f"inviati {len(items)} materiali ma aggiornamento contatori fallito: {e}"
                )
                return {'sent': True, 'count': len(items), 'recipients': recipients,
                        'reason': f'ok (db update error: {e})'}
    except Exception as e:
        logger.error(f"Errore imprevisto purchasing reminder: {e}", exc_info=True)
        if not email_sent:
            release_job_lock(db, job_name)
        log_job_run(db, job_name, 'ERROR', f"errore imprevisto: {e}")
        return {'sent': False, 'count': 0, 'reason': f'error: {e}'}


_daily_email_table_ensured = False


def _ensure_daily_email_table(db):
    """Crea la tabella ind.RiordineEmailDaily se non esiste (lock giornaliero per l'email aggregata)."""
    global _daily_email_table_ensured
    if _daily_email_table_ensured:
        return
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute("""
            IF OBJECT_ID('ind.RiordineEmailDaily','U') IS NULL
            CREATE TABLE ind.RiordineEmailDaily (
                EmailDate DATE NOT NULL PRIMARY KEY,
                CreatedAt DATETIME NOT NULL DEFAULT GETDATE()
            )
        """)
        db.conn.commit()
    _daily_email_table_ensured = True


def _claim_daily_email_lock(db):
    """Prenota ATOMICAMENTE l'invio dell'email di riordino aggregata odierna.
    Ritorna True solo se questo processo vince il lock."""
    _ensure_daily_email_table(db)
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute("""
            INSERT INTO ind.RiordineEmailDaily (EmailDate)
            SELECT CAST(GETDATE() AS DATE)
            WHERE NOT EXISTS (
                SELECT 1 FROM ind.RiordineEmailDaily WITH (UPDLOCK, HOLDLOCK)
                WHERE EmailDate = CAST(GETDATE() AS DATE)
            )
        """)
        db.conn.commit()
        return cur.rowcount > 0


def _release_daily_email_lock(db):
    """Rilascia il lock giornaliero (usato in caso di errore di invio)."""
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        try:
            cur.execute("DELETE FROM ind.RiordineEmailDaily WHERE EmailDate = CAST(GETDATE() AS DATE)")
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            logger.error(f"_release_daily_email_lock errore: {e}", exc_info=True)


def check_and_send_reorder(db, lang, force=False):
    """Verifica i materiali sotto scorta minima e invia UN'UNICA email di riordino al giorno.

    Args:
        force: se True ignora il dedup giornaliero (invio manuale on-demand).

    Ritorna dict: {sent: bool, count: int, recipients: list, reason: str}
    """
    below = get_giacenze(db, only_below=True)
    if not below:
        return {'sent': False, 'count': 0, 'recipients': [], 'reason': 'no_items'}

    # Destinatari PRIMA della prenotazione: se non ce ne sono, non consumare il
    # claim (altrimenti i materiali risulterebbero "inviati oggi" senza email).
    recipients = _get_reorder_recipients(db)
    if not recipients:
        logger.warning(f"Riordino: nessun destinatario configurato in Settings.{REORDER_EMAIL_ATTRIBUTE}")
        return {'sent': False, 'count': len(below), 'recipients': [], 'reason': 'no_recipients'}

    # Lock atomico a livello di email aggregata: garantisce UN'UNICA email al giorno
    # in caso di esecuzioni concorrenti (più PC / processi).
    if not force and not _claim_daily_email_lock(db):
        logger.info("Riordino: email giornaliera gia' inviata da un altro processo.")
        return {'sent': False, 'count': 0, 'recipients': recipients, 'reason': 'daily_email_already_sent'}

    # Prenotazione atomica giornaliera per singolo materiale (dedup cross-PC).
    # In modalità force (invio manuale) si invia comunque per tutti i materiali sotto soglia.
    if force:
        to_send = below
    else:
        to_send = _claim_materials_today(db, below, recipients)
        if not to_send:
            _release_daily_email_lock(db)  # nessun materiale da inviare: rilascia il lock
            return {'sent': False, 'count': 0, 'recipients': recipients, 'reason': 'already_sent_today'}

    subject, body = _build_reorder_email(lang, to_send)
    email_sent = False   # dopo la consegna le prenotazioni non si rilasciano piu'
    try:
        from email_connector import EmailSender
        sender = EmailSender()
        # Un'unica email a tutti i destinatari (in TO), invece di una per ciascuno.
        sender.send_email(to_email='; '.join(recipients), subject=subject,
                          body=body, is_html=True)
        email_sent = True
        if force:
            _log_reorder_sent(db, to_send, recipients)  # log per il dedup dei run automatici
        logger.info(f"Riordino: email inviata a {len(recipients)} destinatari per {len(to_send)} materiali.")
        return {'sent': True, 'count': len(to_send), 'recipients': recipients, 'reason': 'ok'}
    except Exception as e:
        if email_sent:
            # Email gia' consegnata: le prenotazioni RESTANO, altrimenti il giro
            # successivo rimanda lo stesso riordino.
            logger.error(f"Riordino: email inviata, errore successivo: {e}; "
                         f"prenotazioni mantenute", exc_info=True)
            return {'sent': True, 'count': len(to_send), 'recipients': recipients, 'reason': 'ok'}
        logger.error(f"Riordino: errore invio email: {e}", exc_info=True)
        if not force:
            _unclaim_materials_today(db, to_send)   # rilascia le prenotazioni: si ritenta al prossimo giro
            _release_daily_email_lock(db)          # permette il ritentativo dell'email aggregata
        return {'sent': False, 'count': len(to_send), 'recipients': recipients, 'reason': f'error: {e}'}
