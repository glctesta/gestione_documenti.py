# -*- coding: utf-8 -*-
"""
overtime/overtime_economics.py

Analisi di convenienza economica degli straordinari.
Correla la produzione (finalizzata + WIP valorizzato per fase) con il personale
presente in straordinario, usando i prezzi unitari dal file D365.

Vedi docs/Overtime_ConvenienzaEconomica_Spec_v1.0.md
"""
from __future__ import annotations

import os
import glob
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ── Configurazione ─────────────────────────────────────────────────────────────
D365_DIR = r"T:\D365 data"
D365_SHEET = "PR Master data From D365"
D365_HEADER_ROW = 3          # 0-based: intestazioni sulla riga 4 del foglio

# Mappatura fasi per la valorizzazione del WIP (vedi spec §4)
PHASES_TEST = (102, 103)     # ICT, FCT  -> 90%
PHASE_PTHM = 4               # PTHM      -> 60%
PHASES_SMT_AOI = (1, 2)      # SMT, AOI  -> 30%

WIP_PCT_TEST = 0.90
WIP_PCT_PTHM = 0.60
WIP_PCT_SMT = 0.30

WEEKDAY_OT_MULTIPLIER = 1.5  # straordinario feriale = Daily_Cost x 1.5


# ════════════════════════════════════════════════════════════════════════════════
#  Prezzi D365
# ════════════════════════════════════════════════════════════════════════════════
def latest_d365_file(directory: str = D365_DIR):
    """Restituisce il path del file .xlsx più recente (per data modifica),
    ignorando i file temporanei di Excel (~$...). None se assente."""
    try:
        files = [f for f in glob.glob(os.path.join(directory, "*.xlsx"))
                 if not os.path.basename(f).startswith("~$")]
        if not files:
            return None
        return max(files, key=os.path.getmtime)
    except Exception as e:
        logger.error(f"latest_d365_file: {e}", exc_info=True)
        return None


def load_d365_prices():
    """Carica i prezzi unitari dal file D365 più recente.

    Returns: (by_order, by_product, file_path)
      by_order   = {OrderNumber: unit_price}
      by_product = {ProductCode: unit_price}
      file_path  = percorso del file usato (None se non trovato)
    """
    path = latest_d365_file()
    if not path:
        logger.warning("load_d365_prices: nessun file .xlsx in %s", D365_DIR)
        return {}, {}, None

    try:
        import pandas as pd
        df = pd.read_excel(path, sheet_name=D365_SHEET,
                           header=D365_HEADER_ROW, usecols="A,B,K")
        df.columns = ["OrderNumber", "ProductCode", "UnitPrice"]

        by_order, by_product = {}, {}
        for _, r in df.iterrows():
            order = str(r["OrderNumber"]).strip() if r["OrderNumber"] is not None else ""
            prod = str(r["ProductCode"]).strip() if r["ProductCode"] is not None else ""
            price = r["UnitPrice"]
            try:
                price = float(price)
            except (TypeError, ValueError):
                continue
            if order and order.lower() != "nan":
                by_order[order] = price
            if prod and prod.lower() != "nan":
                # non sovrascrivere un prezzo valido con uno 0
                if prod not in by_product or (by_product[prod] in (0, None) and price):
                    by_product[prod] = price
        logger.info("load_d365_prices: %d ordini, %d prodotti da %s",
                    len(by_order), len(by_product), path)
        return by_order, by_product, path
    except Exception as e:
        logger.error(f"load_d365_prices: {e}", exc_info=True)
        return {}, {}, path


def _price_for(order_number, product_code, by_order, by_product):
    """Prezzo unitario: prima per ordine (col A), fallback per prodotto (col B)."""
    if order_number and order_number in by_order and by_order[order_number]:
        return by_order[order_number]
    if product_code and product_code in by_product and by_product[product_code]:
        return by_product[product_code]
    # se l'ordine ha prezzo 0 esplicito, restituiscilo comunque
    if order_number in by_order:
        return by_order[order_number]
    if product_code in by_product:
        return by_product[product_code]
    return None


# ════════════════════════════════════════════════════════════════════════════════
#  Costo orario straordinario
# ════════════════════════════════════════════════════════════════════════════════
def get_overtime_rates(conn):
    """Legge Daily_Cost e WeekEndCost da OverTimeDefaults.
    Returns dict: {'daily': x, 'weekend': y, 'weekday_ot': x*1.5, 'currency': 'EUR'}."""
    rates = {"daily": 0.0, "weekend": 0.0, "weekday_ot": 0.0, "currency": ""}
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.Description, d.ValueITem, v.[desc] AS Currency
            FROM [ResetServices].[dbo].[OverTimeDefaults] d
            JOIN [ResetServices].[dbo].[OverTimeDescriptions] o ON d.DescriptionId = o.DescpriptionId
            JOIN [ResetServices].[dbo].[TbValute] v            ON d.CurrencyId    = v.IdValuta
        """)
        for desc, value, currency in cur.fetchall():
            d = (desc or "").strip().lower()
            if d == "daily_cost":
                rates["daily"] = float(value or 0)
                rates["currency"] = currency
            elif d == "weekendcost":
                rates["weekend"] = float(value or 0)
        rates["weekday_ot"] = rates["daily"] * WEEKDAY_OT_MULTIPLIER
        cur.close()
    except Exception as e:
        logger.error(f"get_overtime_rates: {e}", exc_info=True)
    return rates


def _hourly_rate_for_day(d, rates):
    """Tariffa oraria: weekend = WeekEndCost (invariato); feriale = Daily_Cost x 1.5."""
    if d.weekday() >= 5:   # 5=sab, 6=dom
        return rates["weekend"]
    return rates["weekday_ot"]


# ════════════════════════════════════════════════════════════════════════════════
#  Straordinari (presenza/ore per dipendente e giorno)
# ════════════════════════════════════════════════════════════════════════════════
_OVERTIME_DETAIL_SQL = """
DECLARE @dateStart DATE = ?;
DECLARE @dateStop  DATE = ?;

WITH
CTE_DailyState_Employee AS (
    SELECT ds.IDDailyState, ds.DailyStateDate, e.IDEmployee,
           UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Name, e.UniqueID
    FROM Timeclocking.dbo.DailyState ds
    INNER JOIN Timeclocking.dbo.Employee e
        ON e.IDEmployee = ds.IDEmployee
       AND ds.DailyStateDate BETWEEN @dateStart AND @dateStop
),
CTE_Done AS (
    SELECT fd.IDDailyState, fd.NoMin AS MinSuplimentarDone
    FROM Timeclocking.dbo.EmployeeRequestFractionalDay fd
    INNER JOIN Timeclocking.dbo.RequestType r ON r.IDRequestType = fd.IDRequestType
    WHERE r.IDRequestType = 8
),
CTE_HireHistory AS (
    SELECT h.EmployeeHireHistoryId AS EmployeeHireId,
           ee.EmployeeNID COLLATE DATABASE_DEFAULT AS UniqueID
    FROM employee.dbo.employees ee
    INNER JOIN employee.dbo.employeehirehistory h
        ON ee.EmployeeId = h.EmployeeId AND h.employeerid = 2 AND h.EndWorkDate IS NULL
    LEFT JOIN Employee.dbo.EmployeeCdcStories cs
        ON cs.EmployeeHireHistoryId = h.EmployeeHireHistoryId AND cs.DateOut IS NULL
    LEFT JOIN Employee.dbo.Functions f ON cs.FunctionId = f.FunctionId
    WHERE ISNULL(f.FunctionCode, 0) <= 60
),
CTE_ExtraTimeApprovalStory AS (
    SELECT es.IdEmployee AS EmployeeHireHistoryId,
           CAST(es.DateStart AS DATE) AS DateStart,
           ISNULL(DATEDIFF(MINUTE, es.DateStart, es.DateEnd), 0) AS MinExtraTimeApproved
    FROM [ResetServices].[dbo].ExtraTimeApprovalStory es
    WHERE CAST(es.DateStart AS DATE) BETWEEN @dateStart AND @dateStop
),
CTE_Combined AS (
    SELECT dse.Name,
           dse.DailyStateDate AS OvertimeDate,
           req.MinSuplimentarDone,
           ISNULL(eta.MinExtraTimeApproved, 0) AS MinExtraTimeApproved
    FROM CTE_DailyState_Employee dse
    INNER JOIN CTE_Done req ON dse.IDDailyState = req.IDDailyState
    INNER JOIN CTE_HireHistory hh ON dse.UniqueID COLLATE DATABASE_DEFAULT = hh.UniqueID
    LEFT JOIN CTE_ExtraTimeApprovalStory eta
        ON hh.EmployeeHireId = eta.EmployeeHireHistoryId AND eta.DateStart = dse.DailyStateDate
)
SELECT DISTINCT Name, OvertimeDate, MinSuplimentarDone, MinExtraTimeApproved
FROM CTE_Combined
ORDER BY OvertimeDate, Name;
"""


def get_overtime_detail(conn, start_date, end_date):
    """Returns list of dict: name, day(date), min_done, min_approved (autorizzati, periodo)."""
    out = []
    try:
        cur = conn.cursor()
        cur.execute(_OVERTIME_DETAIL_SQL, (start_date, end_date))
        for name, odate, min_done, min_appr in cur.fetchall():
            d = odate.date() if hasattr(odate, "date") else odate
            out.append({
                "name": name,
                "day": d,
                "min_done": int(min_done or 0),
                "min_approved": int(min_appr or 0),
            })
        cur.close()
    except Exception as e:
        logger.error(f"get_overtime_detail: {e}", exc_info=True)
    return out


# ════════════════════════════════════════════════════════════════════════════════
#  Produzione: finalizzati + WIP
# ════════════════════════════════════════════════════════════════════════════════
_FINALIZED_SQL = """
WITH LastPhase AS (
    SELECT op.IDOrder, op.IDOrderPhase,
           ROW_NUMBER() OVER (PARTITION BY op.IDOrder ORDER BY op.PhasePosition DESC) AS rn
    FROM dbo.OrderPhases op
)
SELECT CAST(s.ScanTimeFinish AS DATE) AS d,
       o.OrderNumber, p.ProductCode,
       COUNT(DISTINCT s.IDBoard) AS Qty
FROM LastPhase lp
JOIN dbo.Scannings s ON s.IDOrderPhase = lp.IDOrderPhase AND s.IsPass = 1
JOIN dbo.Orders    o ON o.IDOrder   = lp.IDOrder
JOIN dbo.Products  p ON p.IDProduct = o.IDProduct
WHERE lp.rn = 1
  AND s.ScanTimeFinish >= ? AND s.ScanTimeFinish < ?
GROUP BY CAST(s.ScanTimeFinish AS DATE), o.OrderNumber, p.ProductCode
"""

_WIP_SQL = """
WITH LastPhase AS (
    SELECT IDOrder, IDOrderPhase,
           ROW_NUMBER() OVER (PARTITION BY IDOrder ORDER BY PhasePosition DESC) AS rn
    FROM dbo.OrderPhases
),
FinalizedBoards AS (
    SELECT DISTINCT s.IDBoard
    FROM LastPhase lp
    JOIN dbo.Scannings s ON s.IDOrderPhase = lp.IDOrderPhase AND s.IsPass = 1
    WHERE lp.rn = 1
),
BoardPhase AS (
    SELECT b.IDBoard, o.OrderNumber, p.ProductCode,
           MAX(CASE WHEN op.IDPhase IN (102,103) AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassTest,
           MAX(CASE WHEN op.IDPhase = 4          AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassPTHM,
           MAX(CASE WHEN op.IDPhase IN (1,2)     AND s.IsPass=1 THEN 1 ELSE 0 END) AS PassSMTAOI
    FROM dbo.Boards b
    JOIN dbo.Orders     o  ON o.IDOrder    = b.IDOrder
    JOIN dbo.Products   p  ON p.IDProduct  = o.IDProduct
    JOIN dbo.Scannings  s  ON s.IDBoard    = b.IDBoard
    JOIN dbo.OrderPhases op ON op.IDOrderPhase = s.IDOrderPhase
    WHERE b.IDBoard NOT IN (SELECT IDBoard FROM FinalizedBoards)
      AND EXISTS (SELECT 1 FROM dbo.Scannings sx
                  WHERE sx.IDBoard = b.IDBoard
                    AND sx.ScanTimeFinish >= ? AND sx.ScanTimeFinish < ?)
    GROUP BY b.IDBoard, o.OrderNumber, p.ProductCode
)
SELECT OrderNumber, ProductCode,
       CASE WHEN PassTest=1 THEN 0.90
            WHEN PassPTHM=1 THEN 0.60
            WHEN PassSMTAOI=1 THEN 0.30
            ELSE 0 END AS WipPct
FROM BoardPhase
WHERE PassTest=1 OR PassPTHM=1 OR PassSMTAOI=1
"""


def get_finalized(conn, dt_start, dt_end):
    """Returns list of dict: day(date), order_number, product_code, qty."""
    out = []
    try:
        cur = conn.cursor()
        cur.execute(_FINALIZED_SQL, (dt_start, dt_end))
        for d, order, prod, qty in cur.fetchall():
            dd = d.date() if hasattr(d, "date") else d
            out.append({"day": dd, "order_number": (order or "").strip(),
                        "product_code": (prod or "").strip(), "qty": int(qty or 0)})
        cur.close()
    except Exception as e:
        logger.error(f"get_finalized: {e}", exc_info=True)
    return out


def get_wip(conn, dt_start, dt_end):
    """Returns list of dict: order_number, product_code, wip_pct (una riga per scheda)."""
    out = []
    try:
        cur = conn.cursor()
        cur.execute(_WIP_SQL, (dt_start, dt_end))
        for order, prod, pct in cur.fetchall():
            out.append({"order_number": (order or "").strip(),
                        "product_code": (prod or "").strip(),
                        "wip_pct": float(pct or 0)})
        cur.close()
    except Exception as e:
        logger.error(f"get_wip: {e}", exc_info=True)
    return out


# ════════════════════════════════════════════════════════════════════════════════
#  Calcolo KPI di convenienza
# ════════════════════════════════════════════════════════════════════════════════
def compute_economics(conn, start_date, end_date):
    """Calcola tutti i KPI di convenienza economica per il periodo [start, end].

    Returns un dict con riepilogo, dettaglio per giorno ed elenco prezzi mancanti.
    """
    dt_start = datetime.combine(start_date, datetime.min.time())
    dt_end = datetime.combine(end_date + timedelta(days=1), datetime.min.time())

    by_order, by_product, d365_path = load_d365_prices()
    rates = get_overtime_rates(conn)
    ot_detail = get_overtime_detail(conn, start_date, end_date)
    finalized = get_finalized(conn, dt_start, dt_end)
    wip = get_wip(conn, dt_start, dt_end)

    missing_price = set()

    # ── Straordinari aggregati ──
    people = set()
    ot_min_done = 0
    ot_min_approved = 0
    ot_cost = 0.0
    per_day = {}   # day -> {people:set, min_done, cost, finalized_value}
    for r in ot_detail:
        people.add(r["name"])
        ot_min_done += r["min_done"]
        ot_min_approved += r["min_approved"]
        rate = _hourly_rate_for_day(r["day"], rates)
        cost = (r["min_done"] / 60.0) * rate
        ot_cost += cost
        pd_ = per_day.setdefault(r["day"], {"people": set(), "min_done": 0,
                                            "cost": 0.0, "finalized_value": 0.0})
        pd_["people"].add(r["name"])
        pd_["min_done"] += r["min_done"]
        pd_["cost"] += cost

    # ── Finalizzati ──
    finalized_pieces = 0
    finalized_value = 0.0
    for r in finalized:
        price = _price_for(r["order_number"], r["product_code"], by_order, by_product)
        finalized_pieces += r["qty"]
        if price is None:
            missing_price.add(f"{r['order_number']} / {r['product_code']}")
            price = 0.0
        val = r["qty"] * price
        finalized_value += val
        pd_ = per_day.setdefault(r["day"], {"people": set(), "min_done": 0,
                                            "cost": 0.0, "finalized_value": 0.0})
        pd_["finalized_value"] += val

    # ── WIP ──
    wip_boards = len(wip)
    wip_pieces_equiv = 0.0
    wip_value = 0.0
    for r in wip:
        price = _price_for(r["order_number"], r["product_code"], by_order, by_product)
        wip_pieces_equiv += r["wip_pct"]
        if price is None:
            missing_price.add(f"{r['order_number']} / {r['product_code']}")
            price = 0.0
        wip_value += r["wip_pct"] * price

    total_value = finalized_value + wip_value
    n_people = len(people)
    ot_hours_done = ot_min_done / 60.0
    ot_hours_approved = ot_min_approved / 60.0

    summary = {
        "d365_file": d365_path,
        "rates": rates,
        "people": n_people,
        "ot_hours_done": ot_hours_done,
        "ot_hours_approved": ot_hours_approved,
        "ot_cost": ot_cost,
        "finalized_pieces": finalized_pieces,
        "finalized_value": finalized_value,
        "wip_boards": wip_boards,
        "wip_pieces_equiv": wip_pieces_equiv,
        "wip_value": wip_value,
        "total_value": total_value,
        "margin": total_value - ot_cost,
        "index": (total_value / ot_cost) if ot_cost else None,
        "value_per_person": (total_value / n_people) if n_people else None,
        "value_per_ot_hour": (total_value / ot_hours_done) if ot_hours_done else None,
        "missing_price": sorted(missing_price),
    }

    per_day_list = []
    for d in sorted(per_day.keys()):
        v = per_day[d]
        per_day_list.append({
            "day": d,
            "people": len(v["people"]),
            "hours_done": v["min_done"] / 60.0,
            "cost": v["cost"],
            "finalized_value": v["finalized_value"],
        })

    return {"summary": summary, "per_day": per_day_list}
