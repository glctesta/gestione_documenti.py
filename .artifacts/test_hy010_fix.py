# -*- coding: utf-8 -*-
"""Test HY010: riproduce l'errore con la query vecchia e verifica il fix."""
import sys, time
import pyodbc
from config_manager import ConfigManager

creds = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
conn_str = (f"DRIVER={creds['driver']};SERVER={creds['server']};DATABASE={creds['database']};"
            f"UID={creds['username']};PWD={creds['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")
print("Driver:", creds['driver'])

QUERY_OLD = """
            WITH OrderData AS (
                SELECT o.IDOrder,
                    d.[SONumber],
                    o.ordernumber,
                    d.[CustomerName],
                    d.[ItemCode],
                    d.[ItemName],
                    d.[ShipDateRequest],
                    d.[QtyOrder],
                    po.Qty AS QtyAssigned,
                    sub.NoBoards AS Associate,
                    sub2.NoBoards AS SMT,
                    sub3.NoBoards AS PTHM,
                    sub4.NoBoards AS ICT,
                    sub5.NoBoards AS FCT,
                    sub6.NoBoards AS Coating,
                    sub7.NoBoards AS [Coating Bottom],
                    sub8.NoBoards AS OutOfBox,
                    po.DynamicProductionOrderID
                FROM
                    [Traceability_RS].[dyn].[DynamicSaleOrders] d
                INNER JOIN
                    [Traceability_RS].[dyn].[DynamicProductionOrders] po ON d.DynamicSaleOrderId = po.DynamicSaleOrderId
                INNER JOIN
                    traceability_rs.dbo.orders o ON po.IdOrder = o.IDOrder
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 0)) sub
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 1)) sub2
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 4)) sub3
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 102)) sub4
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 103)) sub5
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 132)) sub6
                OUTER APPLY
                    (SELECT NoBoards FROM traceability_rs.[dbo].[QuantitaProdottaPerFase](o.IDOrder, 135)) sub7
                OUTER APPLY
                    (select NoBoards from traceability_rs.[dbo].[GetOrderPhaseStatus](o.IDOrder,9)) as sub8
            )

            SELECT
                IDOrder,
                [CustomerName],
                [SONumber] as SaleOrder,
                ordernumber As ProductionOrder,
                [ItemCode],
                [ItemName],
                [ShipDateRequest],
                [QtyOrder],
                QtyAssigned,
                Associate,
                SMT,
                PTHM,
                ICT,
                FCT,
                Coating,
                [Coating Bottom],
                OutOfBox,
                [QtyOrder] - ISNULL(OutOfBox, 0) AS Remain,
                DynamicProductionOrderID
            FROM
                OrderData
            ORDER BY
                SONumber
            """

QUERY_NEW = "SET NOCOUNT ON;\n" + QUERY_OLD


def run(label, query, dedicated):
    cnxn = pyodbc.connect(conn_str, autocommit=False)
    cnxn.timeout = 300
    t0 = time.time()
    try:
        if dedicated:
            cur = cnxn.cursor()
            try:
                cur.execute(query, [])
                rows = cur.fetchall()
            finally:
                cur.close()
        else:
            cur = cnxn.cursor()
            cur.execute(query, [])
            rows = cur.fetchall()
        print(f"{label}: OK - {len(rows)} righe in {time.time()-t0:.1f}s")
        return True
    except Exception as e:
        print(f"{label}: ERRORE dopo {time.time()-t0:.1f}s -> {type(e).__name__}: {e}")
        return False
    finally:
        cnxn.close()


ok_old = run("VECCHIA (cursore condiviso, senza NOCOUNT)", QUERY_OLD, dedicated=False)
ok_new = run("FIXATA (cursore dedicato + SET NOCOUNT ON)", QUERY_NEW, dedicated=True)
sys.exit(0 if ok_new else 1)
