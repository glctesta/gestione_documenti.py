# -*- coding: utf-8 -*-
"""
fai_code_delay.py — Codici con delay dedicato per la verifica oraria FAI.

Alcuni codici non possono essere verificati (FAI) nel tempo standard stabilito
dal programma perché richiedono modifiche tecniche alle temperature del forno
wave. Per questi codici si applica un ritardo aggiuntivo (in minuti) prima che
la verifica FAI venga considerata scaduta / segnalata.

Questa è la sola persistenza (tabella fai.FaiCodeDelay). La maschera di gestione
è in fai_code_delay_gui.py (bottone dalla gestione template FAI, login autorizzato
chiave 'aggiungi_codici_per_delay_fai'). L'applicazione del delay nel ciclo di
autocheck (fai_autocheck) è un passo separato.
"""

import logging

logger = logging.getLogger("PlanMonitor")


def ensure_table(conn) -> None:
    """Crea fai.FaiCodeDelay se non esiste (idempotente)."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                IF OBJECT_ID('fai.FaiCodeDelay', 'U') IS NULL
                CREATE TABLE fai.FaiCodeDelay (
                    Code         NVARCHAR(100) NOT NULL PRIMARY KEY,
                    DelayMinutes INT NOT NULL,
                    AddedBy      NVARCHAR(255) NULL,
                    AddedDate    DATETIME NOT NULL DEFAULT GETDATE()
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"fai_code_delay.ensure_table: {e}", exc_info=True)


def list_codes(conn) -> list:
    """Elenco codici con delay. Ritorna lista di dict."""
    ensure_table(conn)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT Code, DelayMinutes, AddedBy, AddedDate "
                        "FROM fai.FaiCodeDelay ORDER BY Code")
            return [{'code': r.Code, 'minutes': r.DelayMinutes,
                     'added_by': r.AddedBy, 'added_date': r.AddedDate}
                    for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"fai_code_delay.list_codes: {e}", exc_info=True)
        return []


def upsert_code(conn, code: str, minutes: int, user: str = None) -> bool:
    """Aggiunge o aggiorna un codice con i minuti di delay."""
    code = (code or '').strip()
    if not code:
        return False
    try:
        minutes = int(minutes)
    except (TypeError, ValueError):
        return False
    if minutes < 0:
        return False
    ensure_table(conn)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                MERGE fai.FaiCodeDelay AS t
                USING (SELECT ? AS Code) AS s ON UPPER(t.Code) = UPPER(s.Code)
                WHEN MATCHED THEN UPDATE SET DelayMinutes = ?, AddedBy = ?, AddedDate = GETDATE()
                WHEN NOT MATCHED THEN
                    INSERT (Code, DelayMinutes, AddedBy) VALUES (?, ?, ?);
            """, (code, minutes, user or None, code, minutes, user or None))
        conn.commit()
        logger.info("FaiCodeDelay: %r -> %d min (da %s)", code, minutes, user)
        return True
    except Exception as e:
        logger.error(f"fai_code_delay.upsert_code: {e}", exc_info=True)
        return False


def remove_code(conn, code: str) -> bool:
    """Rimuove un codice dalla lista."""
    code = (code or '').strip()
    if not code:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fai.FaiCodeDelay WHERE UPPER(Code) = UPPER(?)", (code,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"fai_code_delay.remove_code: {e}", exc_info=True)
        return False


def get_delay_minutes(conn, code: str) -> int:
    """Minuti di delay per un codice (0 se non presente). Pronto per l'uso nel
    ciclo di autocheck quando verrà deciso il criterio di applicazione."""
    code = (code or '').strip()
    if not code:
        return 0
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DelayMinutes FROM fai.FaiCodeDelay WHERE UPPER(Code) = UPPER(?)",
                        (code,))
            row = cur.fetchone()
            return int(row[0]) if row and row[0] is not None else 0
    except Exception as e:
        logger.warning(f"fai_code_delay.get_delay_minutes: {e}")
        return 0


def get_delay_map(conn) -> dict:
    """Mappa {CODE_UPPER: minuti} per lookup veloce nel ciclo di autocheck."""
    out = {}
    try:
        ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT Code, DelayMinutes FROM fai.FaiCodeDelay")
            for r in cur.fetchall():
                if r.Code:
                    out[r.Code.strip().upper()] = int(r.DelayMinutes or 0)
    except Exception as e:
        logger.warning(f"fai_code_delay.get_delay_map: {e}")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  Grazia "N minuti a prescindere" per la verifica oraria FAI
#  Traccia quando un ordine/fase è stato visto per la PRIMA volta dal ciclo, così
#  la segnalazione FAI viene rimandata sempre di N minuti da quel momento — a
#  prescindere da quanto l'ordine sia vicino/lontano dall'inizio pianificato.
# ─────────────────────────────────────────────────────────────────────────────
def ensure_pending_table(conn) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute("""
                IF OBJECT_ID('fai.FaiDelayPending', 'U') IS NULL
                CREATE TABLE fai.FaiDelayPending (
                    OrderNumber  NVARCHAR(50) NOT NULL,
                    IdPhase      INT NOT NULL,
                    PlannedStart DATETIME NOT NULL,
                    FirstSeen    DATETIME NOT NULL,
                    CONSTRAINT PK_FaiDelayPending PRIMARY KEY (OrderNumber, IdPhase, PlannedStart)
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"fai_code_delay.ensure_pending_table: {e}", exc_info=True)


def check_delay_grace(conn, order_number: str, id_phase: int,
                      planned_start, delay_min: int) -> bool:
    """Gestisce la grazia di `delay_min` minuti PRIMA di segnalare il FAI per un
    codice in ritardo (forno wave).

    Ritorna:
        True  -> segnalazione da RIMANDARE (grazia non ancora trascorsa)
        False -> si può PROCEDERE (grazia trascorsa)

    Alla prima comparsa dell'ordine/fase registra l'istante (FirstSeen) e rimanda;
    ai cicli successivi lascia procedere solo quando sono trascorsi delay_min
    minuti da FirstSeen. Il confronto temporale è fatto lato DB (GETDATE) per
    evitare disallineamenti di orologio tra i PC. In caso di errore NON blocca la
    segnalazione (fail-open)."""
    ensure_pending_table(conn)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT CASE WHEN DATEADD(MINUTE, ?, FirstSeen) <= GETDATE() "
                        "THEN 0 ELSE 1 END AS StillWaiting "
                        "FROM fai.FaiDelayPending "
                        "WHERE OrderNumber = ? AND IdPhase = ? AND PlannedStart = ?",
                        (int(delay_min), order_number, id_phase, planned_start))
            row = cur.fetchone()
            if row is None:
                # Prima comparsa: registra e rimanda.
                cur.execute("INSERT INTO fai.FaiDelayPending "
                            "(OrderNumber, IdPhase, PlannedStart, FirstSeen) "
                            "VALUES (?, ?, ?, GETDATE())",
                            (order_number, id_phase, planned_start))
                conn.commit()
                return True
            return bool(row[0])
    except Exception as e:
        logger.warning(f"fai_code_delay.check_delay_grace: {e}")
        return False


def cleanup_pending(conn, older_than_days: int = 2) -> None:
    """Elimina le righe di grazia vecchie (PlannedStart passato da giorni)."""
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fai.FaiDelayPending "
                        "WHERE PlannedStart < DATEADD(DAY, ?, GETDATE())",
                        (-abs(int(older_than_days)),))
        conn.commit()
    except Exception as e:
        logger.warning(f"fai_code_delay.cleanup_pending: {e}")
