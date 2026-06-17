# -*- coding: utf-8 -*-
"""
eta.py — Stima dei minuti al completamento del kit (fase magazzino).

Modello semplice e robusto:
  eta_minutes = items_rimanenti * avg_min_per_item + buffer_richieste

- avg_min_per_item: media storica da liste WH chiuse di recente
  ((closed_date - upload_date) / items_total), con fallback configurabile.
- buffer_richieste: tempo medio storico richiesta->conferma materiale, sommato
  se l'ordine ha richieste aperte.

È una stima statistica ricalcolata ad ogni sync (5 min): robustezza > precisione.
"""
import logging

logger = logging.getLogger("KitDashboard")


def avg_minutes_per_item(cursor, sample: int = 20, fallback: float = 1.5) -> float:
    """Minuti medi per item da liste WH chiuse di recente."""
    try:
        cursor.execute(f"""
            SELECT AVG(per_item) FROM (
                SELECT TOP {int(sample)}
                    CAST(DATEDIFF(SECOND, pl.upload_date, pl.closed_date) AS FLOAT)
                        / 60.0 / NULLIF(cnt.n, 0) AS per_item
                FROM Traceability_RS.dbo.picking_lists pl
                CROSS APPLY (
                    SELECT COUNT(*) AS n
                    FROM Traceability_RS.dbo.picking_list_items i
                    WHERE i.picking_list_id = pl.id
                ) cnt
                WHERE pl.closed_date IS NOT NULL
                  AND pl.upload_date IS NOT NULL
                  AND pl.closed_date > pl.upload_date
                  AND cnt.n > 0
                ORDER BY pl.closed_date DESC
            ) t
        """)
        r = cursor.fetchone()
        if r and r[0] and r[0] > 0:
            return float(r[0])
    except Exception as e:
        logger.warning("avg_minutes_per_item fallback (%s)", e)
    return float(fallback)


def avg_request_confirm_minutes(cursor, sample: int = 30) -> float:
    """Minuti medi richiesta materiale -> conferma WH (per il buffer)."""
    try:
        cursor.execute(f"""
            SELECT AVG(CAST(DATEDIFF(SECOND, request_date, confirmed_date) AS FLOAT)/60.0)
            FROM (
                SELECT TOP {int(sample)} request_date, confirmed_date
                FROM Traceability_RS.dbo.material_requests
                WHERE confirmed_date IS NOT NULL AND confirmed_date > request_date
                ORDER BY confirmed_date DESC
            ) t
        """)
        r = cursor.fetchone()
        if r and r[0] and r[0] > 0:
            return float(r[0])
    except Exception as e:
        logger.warning("avg_request_confirm_minutes fallback (%s)", e)
    return 0.0


def estimate_minutes(items_remaining: int, avg_item_min: float,
                     open_requests: int, avg_req_min: float) -> int:
    """ETA in minuti (intero). 0 item rimanenti -> 0."""
    if items_remaining <= 0:
        base = 0.0
    else:
        base = items_remaining * max(0.1, avg_item_min)
    if open_requests > 0:
        base += avg_req_min  # un solo buffer: le richieste sono parallele
    return int(round(base))
