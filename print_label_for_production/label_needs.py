# -*- coding: utf-8 -*-
"""
label_needs.py — Calcolo fabbisogno etichette per ordini in ingresso in produzione.
"""
import logging
import math
from typing import List, Dict, Optional

logger = logging.getLogger("PrintLabelProduction")

# Fasi standard (da fai_autocheck.py)
PHASE_AOI = 2
PHASE_PTHM = 4


ORDERS_FOR_LABEL_NEEDS_QUERY = """
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
WITH WH AS (
    SELECT JSON_VALUE(L.MessageSend,'$.Message.Reference') AS OrderNumber,
           SUM(TRY_CAST(JSON_VALUE(j.value,'$.RealValue') AS int)) AS QtyWarehouse
    FROM Traceability_RS.dbo.LogApiDynamics L
    CROSS APPLY OPENJSON(L.MessageSend,
        '$.Message.KeyValue.ListValue[0].ListValue[0].ListValue') j
    WHERE L.EndPointName = 'ProdFinishedGoods'
      AND JSON_VALUE(j.value,'$.Key') = 'GoodQty'
    GROUP BY JSON_VALUE(L.MessageSend,'$.Message.Reference')
)
SELECT o.IDOrder, o.OrderNumber, p.IDProduct, p.ProductCode, p.ProductName,
       o.OrderQuantity
FROM Traceability_RS.dbo.Orders o
INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
CROSS APPLY (
    SELECT COUNT(DISTINCT s.IDBoard) AS BoardsAoi
    FROM Traceability_RS.dbo.Scannings s
    INNER JOIN Traceability_RS.dbo.OrderPhases op ON op.IDOrderPhase = s.IDOrderPhase
    WHERE op.IDOrder = o.IDOrder
      AND op.IDPhase = ?
      AND s.ScanTimeFinish IS NOT NULL
) aoi
LEFT JOIN WH wh ON wh.OrderNumber = o.OrderNumber
WHERE aoi.BoardsAoi = 0
  AND ISNULL(wh.QtyWarehouse, 0) < o.OrderQuantity
  {date_filter}
ORDER BY o.OrderNumber;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
"""


PRODUCT_LABELS_QUERY = """
SELECT
    bm.IDProduct,
    bm.MaterialeID AS LabelId,
    bm.QuantityPerPiece,
    m.CodiceMateriale AS MaterialCode,
    m.DescrizioneMateriale AS MaterialDescription
FROM Traceability_RS.ind.BomIndirectMaterials bm
JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = bm.MaterialeID
JOIN Traceability_RS.ind.FamigliaMateriali fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE bm.IDProduct IN ({placeholders})
  AND bm.DateOut IS NULL
  AND fm.Famiglia = 'Labels'
ORDER BY bm.IDProduct, m.CodiceMateriale;
"""


LABEL_PARAMS_QUERY = """
SELECT
    ltp.MaterialeId,
    ltp.ScartoType,
    ltp.ScartoValue,
    ltp.ScartoMinimo,
    ltp.Arrotondamento
FROM Traceability_RS.ind.LabelTypeParameters ltp
WHERE ltp.MaterialeId IN ({placeholders})
  AND ltp.DateOut IS NULL;
"""


def _rows_to_dicts(cursor) -> List[dict]:
    columns = [desc[0] for desc in cursor.description]
    rows = []
    for r in cursor.fetchall():
        rows.append(dict(zip(columns, r)))
    return rows


def fetch_orders_for_label_needs(cursor, phase_aoi: int, lookback_days: Optional[int] = None) -> List[dict]:
    date_filter = ""
    params = [phase_aoi]
    if lookback_days:
        date_filter = "AND o.OrderDate >= DATEADD(day, -?, GETDATE())"
        params.append(lookback_days)
    query = ORDERS_FOR_LABEL_NEEDS_QUERY.format(date_filter=date_filter)
    cursor.execute(query, params)
    return _rows_to_dicts(cursor)


def fetch_product_labels(cursor, product_ids: List[int]) -> List[dict]:
    if not product_ids:
        return []
    placeholders = ','.join('?' * len(product_ids))
    query = PRODUCT_LABELS_QUERY.format(placeholders=placeholders)
    cursor.execute(query, product_ids)
    return _rows_to_dicts(cursor)


def fetch_label_parameters(cursor, materiale_ids: List[int]) -> Dict[int, dict]:
    if not materiale_ids:
        return {}
    placeholders = ','.join('?' * len(materiale_ids))
    query = LABEL_PARAMS_QUERY.format(placeholders=placeholders)
    cursor.execute(query, materiale_ids)
    result = {}
    for r in cursor.fetchall():
        result[r[0]] = {
            'ScartoType': r[1],
            'ScartoValue': r[2],
            'ScartoMinimo': r[3],
            'Arrotondamento': r[4],
        }
    return result


def compute_scarto(qty_net: float, params: Optional[dict]) -> float:
    if not params:
        return 0.0
    scarto = 0.0
    scarto_type = params.get('ScartoType')
    scarto_value = float(params.get('ScartoValue') or 0)
    if scarto_type == 'FIXED':
        scarto = scarto_value
    elif scarto_type == 'PERC':
        scarto = qty_net * (scarto_value / 100.0)
    minimo = float(params.get('ScartoMinimo') or 0)
    if scarto < minimo:
        scarto = minimo
    return scarto


def round_up(qty: float, arrotondamento: float) -> float:
    if not arrotondamento or arrotondamento <= 0:
        return qty
    return math.ceil(qty / arrotondamento) * arrotondamento


def calculate_label_needs(
    orders: List[dict],
    product_labels: List[dict],
    label_params: Dict[int, dict]
) -> List[dict]:
    needs = []
    for order in orders:
        product_id = order['IDProduct']
        order_qty = order.get('OrderQuantity') or 0
        labels_for_product = [pl for pl in product_labels if pl['IDProduct'] == product_id]
        for pl in labels_for_product:
            qty_per_piece = pl.get('QuantityPerPiece') or 1
            qty_net = order_qty * qty_per_piece
            params = label_params.get(pl['LabelId'])
            scarto = compute_scarto(qty_net, params)
            arrotondamento = float(params['Arrotondamento'] or 1) if params else 1
            qty_total = round_up(qty_net + scarto, arrotondamento)
            needs.append({
                'IDOrder': order['IDOrder'],
                'OrderNumber': order['OrderNumber'],
                'IDProduct': product_id,
                'ProductCode': order['ProductCode'],
                'ProductName': order['ProductName'],
                'LabelId': pl['LabelId'],
                'MaterialCode': pl['MaterialCode'],
                'MaterialDescription': pl['MaterialDescription'],
                'QuantityPerPiece': qty_per_piece,
                'QtyNet': qty_net,
                'QtyScarto': scarto,
                'QtyTotal': qty_total,
            })
    return needs


def aggregate_by_label(needs: List[dict]) -> List[dict]:
    agg: Dict[int, dict] = {}
    for n in needs:
        key = n['LabelId']
        if key not in agg:
            agg[key] = {
                'LabelId': n['LabelId'],
                'MaterialCode': n['MaterialCode'],
                'MaterialDescription': n['MaterialDescription'],
                'Orders': [],
                'QtyNet': 0.0,
                'QtyScarto': 0.0,
                'QtyTotal': 0.0,
            }
        agg[key]['Orders'].append({
            'IDOrder': n['IDOrder'],
            'OrderNumber': n['OrderNumber'],
            'QtyNet': n['QtyNet'],
            'QtyScarto': n['QtyScarto'],
            'QtyTotal': n['QtyTotal'],
        })
        agg[key]['QtyNet'] += n['QtyNet']
        agg[key]['QtyScarto'] += n['QtyScarto']
        agg[key]['QtyTotal'] += n['QtyTotal']
    return list(agg.values())
