"""
diagnose_kit_prod_eligibility.py
Script di supporto per verificare perche' la form Produzione — Ricevimento Kit
(kit_prod_gui.py) non mostra kit da confermare.

Uso:
    python diagnose_kit_prod_eligibility.py

Richiede che il progetto sia nel PYTHONPATH o eseguito dalla root del progetto.
"""
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    try:
        from db import Database
        from kit_prod_logic import eligible_lists, PHASE_PROD
    except ImportError as e:
        logger.error("Import fallito: %s. Eseguire dalla root del progetto.", e)
        sys.exit(1)

    db = Database()
    try:
        db._ensure_connection()
        cur = db.conn.cursor()

        logger.info("=" * 70)
        logger.info("DIAGNOSTICA Ricevimento Kit Produzione (fase %s)", PHASE_PROD)
        logger.info("=" * 70)

        # 1. Conteggio kit_status per stato
        logger.info("\n1. Stati in kit_status:")
        cur.execute("""
            SELECT status, COUNT(*) AS cnt
            FROM Traceability_RS.dbo.kit_status
            GROUP BY status
            ORDER BY cnt DESC
        """)
        rows = cur.fetchall()
        if not rows:
            logger.info("   kit_status e' VUOTA.")
        for r in rows:
            logger.info("   %-30s : %d", r[0], r[1])

        # 2. Ordini eleggibili per la produzione (stati inclusi)
        logger.info("\n2. Ordini nello stato eleggibile per la produzione:")
        cur.execute("""
            SELECT order_number, status, updated_by, updated_date
            FROM Traceability_RS.dbo.kit_status
            WHERE status IN ('WH_CLOSED', 'WH_PARTIAL', 'IN_PREFORMING', 'BLOCKED_MISSING_MATERIAL')
            ORDER BY updated_date DESC
        """)
        rows = cur.fetchall()
        if not rows:
            logger.info("   Nessun ordine in WH_CLOSED/WH_PARTIAL/IN_PREFORMING/BLOCKED_MISSING_MATERIAL.")
        else:
            for r in rows:
                logger.info("   %-15s %-25s by=%-6s %s", r[0], r[1], r[2], r[3])

        # 3. Picking lists che contengono ordini eleggibili
        logger.info("\n3. Picking lists che contengono ordini eleggibili:")
        cur.execute("""
            SELECT DISTINCT pl.id, pl.source_file_name, pl.status, pl.closed_date,
                   plo.order_number, ks.status
            FROM Traceability_RS.dbo.picking_lists pl
            INNER JOIN Traceability_RS.dbo.picking_list_orders plo
                    ON plo.picking_list_id = pl.id
            INNER JOIN Traceability_RS.dbo.kit_status ks
                    ON ks.order_number = plo.order_number
            WHERE ks.status IN ('WH_CLOSED', 'WH_PARTIAL', 'IN_PREFORMING', 'BLOCKED_MISSING_MATERIAL')
            ORDER BY pl.id
        """)
        rows = cur.fetchall()
        if not rows:
            logger.info("   Nessuna picking list trovata con ordini eleggibili.")
        else:
            for r in rows:
                logger.info("   pl.id=%-5d file=%-30s pl.status=%-12s order=%-15s ks.status=%s",
                            r[0], r[1] or '', r[2] or '', r[4], r[5])

        # 4. Risultato della funzione eligible_lists (come la form)
        logger.info("\n4. Risultato della funzione eligible_lists() (quello che vede la form):")
        eligible = eligible_lists(cur)
        if not eligible:
            logger.info("   eligible_lists() ha restituito 0 righe -> la form sara' vuota.")
        else:
            for it in eligible:
                logger.info("   pl.id=%-5d prio=%s blocked=%s orders=%s file=%s",
                            it['id'], it['prio_rank'], it['blocked'], it['orders'], it['file_name'])

        # 5. Picking lists chiuse di recente (controllo flusso)
        logger.info("\n5. Ultime 10 picking_lists chiuse (verificare se sono passate dalla PF):")
        cur.execute("""
            SELECT TOP 10 id, source_file_name, status, closed_date
            FROM Traceability_RS.dbo.picking_lists
            WHERE status = 'CLOSED'
            ORDER BY closed_date DESC
        """)
        for r in cur.fetchall():
            logger.info("   id=%-5d status=%-10s closed=%s file=%s",
                        r[0], r[1] or '', r[3], r[2] or '')

        logger.info("\n" + "=" * 70)
        logger.info("Fine diagnostica.")
        logger.info("=" * 70)
    except Exception as e:
        logger.error("Errore durante la diagnostica: %s", e, exc_info=True)
    finally:
        try:
            db.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
