# -*- coding: utf-8 -*-
"""
backfill_fai_pdfs.py
====================
Genera e salva il PDF FAI per tutti i record in fai.FaiLogs
che non hanno ancora il campo DocVerification compilato.

Esegui con:
    .venv\\Scripts\\python.exe backfill_fai_pdfs.py

Opzioni:
    --dry-run     Mostra quanti record verrebbero aggiornati senza fare nulla
    --limit N     Elabora al massimo N record
    --log-id ID   Elabora solo il FaiLogId specificato
"""
import sys
import os
import argparse
import logging
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("backfill_fai_pdfs")

# ── Argomenti CLI ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Backfill PDF FAI mancanti in fai.FaiLogs")
parser.add_argument("--dry-run",  action="store_true", help="Mostra i record senza elaborarli")
parser.add_argument("--limit",    type=int, default=None, help="Numero massimo di record da elaborare")
parser.add_argument("--log-id",   type=int, default=None, help="Elabora solo questo FaiLogId")
args = parser.parse_args()

# ── Connessione DB ─────────────────────────────────────────────────────────────
import pyodbc
from config_manager import ConfigManager

try:
    config_mgr = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc")
    creds = config_mgr.load_config()
    DB_CONN_STR = (
        f"DRIVER={creds['driver']};"
        f"SERVER={creds['server']};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']};"
        "MARS_Connection=Yes;TrustServerCertificate=Yes"
    )
    logger.info(f"Credenziali caricate - server: {creds['server']}, db: {creds['database']}")
except Exception as e:
    logger.error(f"Impossibile caricare le credenziali: {e}")
    sys.exit(1)

try:
    conn = pyodbc.connect(DB_CONN_STR)
    cursor = conn.cursor()
    logger.info("Connessione al database stabilita.")
except Exception as e:
    logger.error(f"Errore connessione: {e}")
    sys.exit(1)

# ── Recupera i record senza PDF ────────────────────────────────────────────────
try:
    if args.log_id:
        # Modalita' singolo record (ignora DocVerification: forza rigenerazione)
        query = """
            SELECT FaiLogId
            FROM Traceability_RS.fai.FaiLogs
            WHERE FaiLogId = ?
            ORDER BY FaiLogId ASC
        """
        cursor.execute(query, args.log_id)
    else:
        # Tutti i record senza DocVerification
        query = """
            SELECT FaiLogId
            FROM Traceability_RS.fai.FaiLogs
            WHERE DocVerification IS NULL
            ORDER BY FaiLogId ASC
        """
        cursor.execute(query)

    records = cursor.fetchall()

    if args.limit:
        records = records[:args.limit]

    logger.info(f"Record da elaborare: {len(records)}")

    if not records:
        logger.info("Nessun record da elaborare. Uscita.")
        sys.exit(0)

    if args.dry_run:
        logger.info("[DRY RUN] Nessuna modifica effettuata. Record che verrebbero elaborati:")
        for r in records:
            logger.info(f"  FaiLogId: {r.FaiLogId}")
        sys.exit(0)

except Exception as e:
    logger.error(f"Errore query record: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)

# ── Elaborazione ──────────────────────────────────────────────────────────────
from fai_report_generator import generate_fai_report

class FakeDB:
    """Adattatore che espone conn e cursor come si aspetta generate_fai_report"""
    def __init__(self, connection, cur):
        self.conn   = connection
        self.cursor = cur

fake_db = FakeDB(conn, cursor)

ok_count   = 0
fail_count = 0
skip_count = 0

update_query = """
UPDATE Traceability_RS.fai.FaiLogs
SET DocVerification = ?
WHERE FaiLogId = ?
"""

for record in records:
    fai_log_id = record.FaiLogId
    pdf_path   = os.path.join(tempfile.gettempdir(), f"BACKFILL_FAI_{fai_log_id}.pdf")

    logger.info(f"Elaboro FaiLogId={fai_log_id} ...")

    try:
        ok = generate_fai_report(fai_log_id, fake_db, pdf_path)
        if not ok:
            logger.warning(f"  --> generate_fai_report ha restituito False. Salto.")
            skip_count += 1
            continue

        if not os.path.exists(pdf_path):
            logger.warning(f"  --> PDF non trovato su disco dopo la generazione: {pdf_path}")
            skip_count += 1
            continue

        with open(pdf_path, 'rb') as f:
            pdf_binary = f.read()

        cursor.execute(update_query, (pdf_binary, fai_log_id))
        conn.commit()
        size_kb = len(pdf_binary) / 1024
        logger.info(f"  --> OK: PDF salvato ({size_kb:.1f} KB)")
        ok_count += 1

        # Rimuove il file temporaneo
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    except Exception as err:
        logger.error(f"  --> ERRORE FaiLogId={fai_log_id}: {err}", exc_info=True)
        fail_count += 1
        try:
            conn.rollback()
        except Exception:
            pass

# ── Riepilogo ──────────────────────────────────────────────────────────────────
print()
logger.info("=" * 60)
logger.info(f"COMPLETATO: {ok_count} PDF salvati, {skip_count} saltati, {fail_count} errori")
logger.info("=" * 60)

cursor.close()
conn.close()
