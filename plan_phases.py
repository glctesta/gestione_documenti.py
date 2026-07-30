# -*- coding: utf-8 -*-
"""
plan_phases.py — Fasi del piano da tenere in osservazione / da giustificare.

Consente di selezionare da una lista SOLO le fasi importanti (su cui c'e'
tensione) per cui il non rispetto del piano deve essere osservato e giustificato,
invece di monitorare tutte le fasi.

Fasi FINALI, sempre presenti e forzate (non deselezionabili):
  - FCT (ultima fase di test)
  - FQC (Final Quality Control)
Sono le uniche fasi che contano per la giustificazione delle mancate produzioni
e per l'email giornaliera ai responsabili: le fasi intermedie (ICT, PTHM,
PALETIZARE, ...) NON vanno riportate.
(Il "versamento a magazzino" NON e' una fase di PlanAlerts: la quantita'
effettivamente prodotta e versata a magazzino si ricava dalla query D365
get_warehouse_finished_goods — integrazione a parte.)

Storage: tabella dbo.PlanMonitoredPhases (una riga per fase monitorata) +
flag settings Sys_plan_phases_configured. Finche' non e' configurato,
get_monitored_phases() ritorna le sole fasi finali (FCT, FQC).

La selezione e' modificabile dalla maschera plan_phases_gui (login autorizzato,
chiave 'fasi_da_giustificare_mancata_produzione').
"""

import logging

logger = logging.getLogger("TraceabilityRS")

# Fasi FINALI forzate, non deselezionabili (fasi reali di dbo.Phases).
# Sono anche il default quando la selezione non e' mai stata configurata:
# solo queste finiscono nell'email responsabili e nella maschera di
# giustificazione delle mancate produzioni.
FORCED_PHASES = ['FCT', 'FQC']

# NB: settings.Atribute è nvarchar(30) -> chiave <= 30 caratteri.
CONFIG_FLAG_SETTING = 'Sys_plan_phases_configured'  # 26 char


def ensure_table(conn) -> None:
    """Crea dbo.PlanMonitoredPhases se non esiste (idempotente)."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                IF OBJECT_ID('traceability_rs.dbo.PlanMonitoredPhases', 'U') IS NULL
                CREATE TABLE traceability_rs.dbo.PlanMonitoredPhases (
                    PhaseName NVARCHAR(100) NOT NULL PRIMARY KEY,
                    AddedBy   NVARCHAR(255) NULL,
                    AddedDate DATETIME NOT NULL DEFAULT GETDATE()
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"plan_phases.ensure_table: {e}", exc_info=True)


def get_final_phases() -> list:
    """Fasi finali (FCT, FQC): le uniche da riportare/giustificare per default."""
    return list(FORCED_PHASES)


def get_all_plan_phases(conn) -> list:
    """Elenco fasi selezionabili: quelle che compaiono in PlanAlerts (che possono
    generare discrepanze) unite alle fasi forzate. Ordinate alfabeticamente."""
    phases = set(FORCED_PHASES)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT PhaseName FROM traceability_rs.dbo.PlanAlerts "
                        "WHERE PhaseName IS NOT NULL AND LTRIM(RTRIM(PhaseName)) <> ''")
            phases.update(r[0].strip() for r in cur.fetchall() if r[0])
    except Exception as e:
        logger.error(f"get_all_plan_phases: {e}", exc_info=True)
    return sorted(phases)


def get_selected_phases(conn) -> set:
    """Fasi salvate in tabella (senza applicare i forzati)."""
    ensure_table(conn)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT PhaseName FROM traceability_rs.dbo.PlanMonitoredPhases")
            return {r[0].strip() for r in cur.fetchall() if r[0]}
    except Exception as e:
        logger.error(f"get_selected_phases: {e}", exc_info=True)
        return set()


def is_configured(conn) -> bool:
    """True se l'utente ha salvato almeno una volta la configurazione."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT TOP 1 [value] FROM traceability_rs.dbo.settings "
                        "WHERE atribute = ?", (CONFIG_FLAG_SETTING,))
            row = cur.fetchone()
            return bool(row and str(row[0]).strip() in ('1', 'True', 'true'))
    except Exception as e:
        logger.warning(f"is_configured: {e}")
        return False


def get_monitored_phases(conn):
    """Fasi effettivamente monitorate. Ritorna SEMPRE una lista (mai None):

      - non configurato -> solo le fasi finali forzate (FCT, FQC)
      - configurato     -> fasi selezionate UNITE ai forzati

    Il default e' volutamente restrittivo: nell'email ai responsabili e nella
    maschera di giustificazione devono comparire solo le fasi finali.
    """
    if not is_configured(conn):
        return get_final_phases()
    phases = get_selected_phases(conn) | set(FORCED_PHASES)
    return sorted(phases)


def save_selection(conn, phases, user: str = None) -> bool:
    """Salva la selezione: sostituisce il contenuto della tabella con
    (phases UNITE ai forzati) e imposta il flag di configurazione."""
    ensure_table(conn)
    final = sorted(set(p.strip() for p in phases if p and p.strip()) | set(FORCED_PHASES))
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM traceability_rs.dbo.PlanMonitoredPhases")
            for ph in final:
                cur.execute("INSERT INTO traceability_rs.dbo.PlanMonitoredPhases "
                            "(PhaseName, AddedBy) VALUES (?, ?)", (ph, user or None))
            cur.execute("""
                MERGE traceability_rs.dbo.settings AS t
                USING (SELECT ? AS atribute) AS s ON t.atribute = s.atribute
                WHEN MATCHED THEN UPDATE SET [value] = '1'
                WHEN NOT MATCHED THEN INSERT (atribute, [value]) VALUES (s.atribute, '1');
            """, (CONFIG_FLAG_SETTING,))
        conn.commit()
        logger.info("Fasi monitorate salvate (%d): %s", len(final), final)
        return True
    except Exception as e:
        logger.error(f"save_selection: {e}", exc_info=True)
        try:
            conn.rollback()
        except Exception:
            pass
        return False


# ============================================================
# Quantita' versata a magazzino (D365 ProdFinishedGoods) — helper
# ============================================================
_WAREHOUSE_FINISHED_GOODS_QUERY = """
select
    A.OrderNumber, A.ProductCode, A.QtySend,
    iif(A.ResponseApiDynamics = 1, 'Received by D365', 'NOT received by D365') AS ResponseByD365,
    B.CurrentDate AS DateTransfer, A.FinalClientName
from (
    select Products.ProductCode, D365.OrderNumber, Orders.IDOrder, D365.SendDynamicsDate,
           D365.QtySend, D365.ResponseApiDynamics, D365.MessageSend, fc.FinalClientName,
           (SELECT STUFF((
                SELECT DISTINCT ',' + CAST(Boxes.IDBox AS varchar(20))
                FROM QualityVerifyBoxes
                INNER JOIN Boxes ON Boxes.IDBox = QualityVerifyBoxes.IDBox
                INNER JOIN BoxDetails ON BoxDetails.IDBox = Boxes.IDBox
                INNER JOIN Boards ON Boards.IDBoard = BoxDetails.IDBoard
                INNER JOIN Orders ON Orders.IDOrder = Boards.IDOrder
                WHERE DeclaredDateERP = D365.SendDynamicsDate
                  AND Orders.OrderNumber = D365.OrderNumber
                FOR XML PATH(''), TYPE
           ).value('.', 'nvarchar(max)'), 1, 1, '')) AS IdBoxTrasb
    from (
        select (SELECT JSON_VALUE(LogApiDynamics.MessageSend, '$.Message.Reference')) AS OrderNumber,
               CurrentDate AS SendDynamicsDate,
               (SELECT JSON_VALUE(j.value, '$.RealValue') AS GoodQty
                FROM OPENJSON(LogApiDynamics.MessageSend, '$.Message.KeyValue.ListValue[0].ListValue[0].ListValue') j
                WHERE JSON_VALUE(j.value, '$.Key') = 'GoodQty') AS QtySend,
               ResponseAPI AS ResponseApiDynamics,
               iif(ResponseMessage = 'Response Body: ', 'OK', ResponseMessage) AS ResponseMessage,
               MessageSend
        from LogApiDynamics
        where CurrentDate between ? and ? and EndPointName = 'ProdFinishedGoods'
    ) D365
    inner join Orders   on Orders.OrderNumber = D365.OrderNumber
    inner join Products on Products.IDProduct = Orders.IDProduct
    left  join FinalClients fc on Products.IdFinalClient = fc.IDFinalClient
) A
cross apply (
    select * from [WarehouseFinish].dbo.Packing
    where IdBoxTrac in (SELECT value FROM STRING_SPLIT(A.IdBoxTrasb, ','))
) B
order by B.Code, A.SendDynamicsDate
"""


def get_warehouse_finished_goods(conn, date_from, date_to) -> list:
    """Quantita' di prodotto finito effettivamente versata a magazzino (via D365
    ProdFinishedGoods) nell'intervallo. Ritorna lista di dict per ordine/box."""
    out = []
    try:
        with conn.cursor() as cur:
            cur.execute(_WAREHOUSE_FINISHED_GOODS_QUERY, (date_from, date_to))
            for r in cur.fetchall():
                out.append({
                    'order': r.OrderNumber,
                    'product': r.ProductCode,
                    'qty_sent': r.QtySend,
                    'received_by_d365': r.ResponseByD365,
                    'date_transfer': r.DateTransfer,
                    'final_client': r.FinalClientName,
                })
    except Exception as e:
        logger.error(f"get_warehouse_finished_goods: {e}", exc_info=True)
    return out
