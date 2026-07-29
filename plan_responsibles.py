# -*- coding: utf-8 -*-
"""
plan_responsibles.py — Responsabili del rispetto del piano di produzione.

Individua i responsabili diretti (middle + management) che devono fornire
spiegazioni per il non rispetto del piano di produzione e per le richieste
urgenti di spedizione, e invia loro una email giornaliera (in rumeno).

Regola destinatari (CDC produzione, CdcId = 1):
  - TO (responsabili diretti):  FunctionCode > 60 e < 90  (61..89)
  - CC (management):            FunctionCode 90 e 100
I FunctionCode <= 60 (shift/line leader) sono i subalterni: NON destinatari.

La regola e' sempre applicata, ma puo' essere corretta manualmente dalla
maschera di gestione (dbo.PlanResponsibleOverrides): si possono ESCLUDERE
persone calcolate dalla regola o INCLUDERE indirizzi aggiuntivi.

Trigger email: tutte le discrepanze di piano ancora NON giustificate
(dbo.PlanAlerts) a partire da una data configurabile (Sys_plan_responsibles_start_date,
default 27/07/2026), con le piu' recenti evidenziate, piu' le richieste urgenti
di spedizione ancora pendenti (dyn.DynamicShippingRules).

Invio: worker in-app giornaliero (vedi main.py), 1 volta al giorno, giorni
lavorativi RO, con dedup atomico su dbo.settings e rispetto della modalita'
Sys_enable_control_plan_check (True/Test/False, come l'escalation piano).
"""

import os
import logging
from datetime import date, datetime, timedelta

import plan_alert_escalation as pae  # riuso mode Test + summary discrepanze

logger = logging.getLogger("TraceabilityRS")

# Data di partenza di default per le discrepanze aperte (decisione utente).
# NB: settings.Atribute è nvarchar(30) -> tutte le chiavi devono stare in 30 char.
DEFAULT_START_DATE = date(2026, 7, 27)
START_DATE_SETTING = 'Sys_plan_resp_start_date'  # 24 char

# Le discrepanze con ultima alert negli ultimi N giorni vengono evidenziate.
RECENT_HIGHLIGHT_DAYS = 2

# Chiave settings per il dedup "gia' inviata oggi" (claim atomico cross-PC).
# Prefisso <= 22 char: + 'YYYYMMDD' (8) resta entro i 30 di settings.Atribute.
SEND_SLOT_PREFIX = 'SentPlanRespEmail_'  # 18 char + data

# Modalita' DEDICATA di questa email, indipendente da Sys_enable_control_plan_check
# (che governa l'escalation piano ed e' gia' 'True'/live). Default 'Test' cosi'
# la nuova email non parte verso i manager reali finche' non viene messa live.
#   'True'  -> invio reale ai responsabili
#   'Test'  -> invio solo a TEST_EMAIL (gianluca.testa)
#   'False' -> non invia
EMAIL_MODE_SETTING = 'Sys_plan_resp_email_mode'  # 24 char
DEFAULT_EMAIL_MODE = 'Test'

CDC_PRODUZIONE = 1


def get_email_mode(conn) -> str:
    """Modalita' dedicata dell'email responsabili (default 'Test')."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT TOP 1 [value] FROM traceability_rs.dbo.settings "
                        "WHERE atribute = ?", (EMAIL_MODE_SETTING,))
            row = cur.fetchone()
            if row and row[0]:
                val = str(row[0]).strip()
                if val in ('True', 'Test', 'False'):
                    return val
    except Exception as e:
        logger.warning(f"get_email_mode: {e}")
    return DEFAULT_EMAIL_MODE


def set_email_mode(conn, mode: str) -> bool:
    """Imposta la modalita' dedicata ('True' | 'Test' | 'False')."""
    if mode not in ('True', 'Test', 'False'):
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                MERGE traceability_rs.dbo.settings AS t
                USING (SELECT ? AS atribute) AS s ON t.atribute = s.atribute
                WHEN MATCHED THEN UPDATE SET [value] = ?
                WHEN NOT MATCHED THEN INSERT (atribute, [value]) VALUES (s.atribute, ?);
            """, (EMAIL_MODE_SETTING, mode, mode))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"set_email_mode: {e}", exc_info=True)
        return False


# ============================================================
# TABELLA OVERRIDE
# ============================================================
def ensure_overrides_table(conn) -> None:
    """Crea dbo.PlanResponsibleOverrides se non esiste (idempotente)."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                IF OBJECT_ID('traceability_rs.dbo.PlanResponsibleOverrides', 'U') IS NULL
                CREATE TABLE traceability_rs.dbo.PlanResponsibleOverrides (
                    OverrideId  INT IDENTITY(1,1) PRIMARY KEY,
                    WorkEmail   NVARCHAR(255) NOT NULL,
                    DisplayName NVARCHAR(255) NULL,
                    RoleTarget  NVARCHAR(4)   NOT NULL,   -- 'TO' | 'CC'
                    ActionKind  NVARCHAR(10)  NOT NULL,   -- 'EXCLUDE' | 'INCLUDE'
                    CreatedBy   NVARCHAR(255) NULL,
                    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
                    DateOut     DATETIME NULL
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"ensure_overrides_table: {e}", exc_info=True)


def list_overrides(conn) -> list:
    """Override attivi (DateOut IS NULL). Ritorna lista di dict."""
    ensure_overrides_table(conn)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT OverrideId, WorkEmail, DisplayName, RoleTarget, ActionKind
                FROM traceability_rs.dbo.PlanResponsibleOverrides
                WHERE DateOut IS NULL
            """)
            return [{'id': r.OverrideId, 'email': r.WorkEmail, 'name': r.DisplayName,
                     'role': r.RoleTarget, 'action': r.ActionKind}
                    for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"list_overrides: {e}", exc_info=True)
        return []


def add_override(conn, email: str, name: str, role: str, action: str, user: str) -> bool:
    """Aggiunge un override (EXCLUDE regola / INCLUDE manuale). Evita duplicati
    attivi per la stessa (email, role, action)."""
    ensure_overrides_table(conn)
    email = (email or '').strip()
    role = (role or '').strip().upper()
    action = (action or '').strip().upper()
    if not email or role not in ('TO', 'CC') or action not in ('EXCLUDE', 'INCLUDE'):
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO traceability_rs.dbo.PlanResponsibleOverrides
                    (WorkEmail, DisplayName, RoleTarget, ActionKind, CreatedBy)
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM traceability_rs.dbo.PlanResponsibleOverrides
                    WHERE DateOut IS NULL AND LOWER(WorkEmail) = LOWER(?)
                      AND RoleTarget = ? AND ActionKind = ?
                )
            """, (email, name or None, role, action, user or None,
                  email, role, action))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"add_override: {e}", exc_info=True)
        return False


def remove_override(conn, override_id: int, user: str = None) -> bool:
    """Soft-delete di un override (DateOut = GETDATE())."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE traceability_rs.dbo.PlanResponsibleOverrides
                SET DateOut = GETDATE()
                WHERE OverrideId = ? AND DateOut IS NULL
            """, (int(override_id),))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"remove_override: {e}", exc_info=True)
        return False


# ============================================================
# REGOLA + DESTINATARI EFFETTIVI
# ============================================================
def get_rule_responsibles(conn) -> dict:
    """Calcola i responsabili dalla regola (CdcId=1). Ritorna:
        {'to': [ {name, email, functioncode, function} ... ],
         'cc': [ ... ]}
    TO = FunctionCode 61..89 ; CC = FunctionCode 90/100. Deduplicati per email."""
    query = """
    SELECT DISTINCT
        UPPER(e.EmployeeName + ' ' + e.EmployeeSurname) AS Employee,
        f.FunctionCode, f.FunctionDescription, a.WorkEmail
    FROM employee.dbo.EmployeeHireHistory h
    INNER JOIN employee.dbo.EmployeeCdcStories css
        ON h.EmployeeHireHistoryId = css.EmployeeHireHistoryId AND css.DateOut IS NULL
    INNER JOIN employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
    INNER JOIN employee.dbo.CdcSub s ON s.SubCdcId = css.SubCdcId
    INNER JOIN employee.dbo.Functions f ON f.FunctionId = css.FunctionId
    INNER JOIN employee.dbo.CostCenters c ON c.CdcId = s.CdcId
    INNER JOIN employee.dbo.EmployeeAddress a
        ON a.EmployeeId = h.EmployeeId AND a.DateOut IS NULL
    WHERE h.EndWorkDate IS NULL AND h.employeerid = 2
      AND c.CdcId = ?
      AND ((f.FunctionCode > 60 AND f.FunctionCode < 90) OR f.FunctionCode IN (90, 100))
      AND a.WorkEmail IS NOT NULL AND LTRIM(RTRIM(a.WorkEmail)) <> ''
    ORDER BY f.FunctionCode
    """
    to_map, cc_map = {}, {}
    try:
        with conn.cursor() as cur:
            cur.execute(query, (CDC_PRODUZIONE,))
            for r in cur.fetchall():
                email = (r.WorkEmail or '').strip()
                if not email:
                    continue
                person = {'name': r.Employee, 'email': email,
                          'functioncode': r.FunctionCode,
                          'function': r.FunctionDescription}
                key = email.lower()
                if 60 < r.FunctionCode < 90:
                    to_map.setdefault(key, person)
                elif r.FunctionCode in (90, 100):
                    cc_map.setdefault(key, person)
    except Exception as e:
        logger.error(f"get_rule_responsibles: {e}", exc_info=True)
    return {'to': list(to_map.values()), 'cc': list(cc_map.values())}


def get_effective_recipients(conn) -> tuple:
    """Applica gli override alla regola. Ritorna
        (to_emails, cc_emails, to_people, cc_people)
    dove *_people sono liste di dict {name, email, functioncode?, origin}."""
    rule = get_rule_responsibles(conn)
    overrides = list_overrides(conn)

    excl = {'TO': set(), 'CC': set()}
    incl = {'TO': [], 'CC': []}
    for o in overrides:
        role = o['role']
        if role not in ('TO', 'CC'):
            continue
        if o['action'] == 'EXCLUDE':
            excl[role].add(o['email'].lower())
        elif o['action'] == 'INCLUDE':
            incl[role].append({'name': o['name'] or o['email'], 'email': o['email'],
                               'origin': 'manuale'})

    def build(role_key, rule_people):
        people, seen = [], set()
        for p in rule_people:
            k = p['email'].lower()
            if k in excl[role_key] or k in seen:
                continue
            seen.add(k)
            people.append({**p, 'origin': 'regola'})
        for p in incl[role_key]:
            k = p['email'].lower()
            if k in seen:
                continue
            seen.add(k)
            people.append(p)
        return people

    to_people = build('TO', rule['to'])
    cc_people = build('CC', rule['cc'])
    return ([p['email'] for p in to_people], [p['email'] for p in cc_people],
            to_people, cc_people)


# ============================================================
# DATA DI PARTENZA (settings)
# ============================================================
def get_start_date(conn) -> date:
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT TOP 1 [value] FROM traceability_rs.dbo.settings "
                        "WHERE atribute = ?", (START_DATE_SETTING,))
            row = cur.fetchone()
            if row and row[0]:
                txt = str(row[0]).strip()
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d.%m.%Y'):
                    try:
                        return datetime.strptime(txt, fmt).date()
                    except ValueError:
                        continue
    except Exception as e:
        logger.warning(f"get_start_date: {e}")
    return DEFAULT_START_DATE


def set_start_date(conn, d: date) -> bool:
    """Upsert della data di partenza (formato ISO)."""
    val = d.strftime('%Y-%m-%d')
    try:
        with conn.cursor() as cur:
            cur.execute("""
                MERGE traceability_rs.dbo.settings AS t
                USING (SELECT ? AS atribute) AS s ON t.atribute = s.atribute
                WHEN MATCHED THEN UPDATE SET [value] = ?
                WHEN NOT MATCHED THEN INSERT (atribute, [value]) VALUES (s.atribute, ?);
            """, (START_DATE_SETTING, val, val))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"set_start_date: {e}", exc_info=True)
        return False


# ============================================================
# DATI: discrepanze aperte + urgenze spedizione
# ============================================================
def get_open_discrepancies(conn, start_date: date) -> list:
    """Discrepanze di piano non giustificate da start_date a oggi, ordinate per
    ultima alert (piu' recenti prima). Limitate alle fasi monitorate se configurate."""
    try:
        import plan_phases
        monitored = plan_phases.get_monitored_phases(conn)
    except Exception:
        monitored = None
    rows = pae.get_unresponded_alerts_summary(
        conn, date_from=start_date, date_to=date.today(), phases=monitored)
    out = []
    for r in rows:
        out.append({
            'order': r.OrderNumber,
            'product': r.ProductName,
            'total': r.TotalAlerts or 0,
            'red': r.RedCount or 0,
            'out_of_plan': r.OutOfPlanCount or 0,
            'deficit': r.TotalDeficit or 0,
            'phases': r.Phases or '',
            'first_date': r.FirstAlertDate,
            'last_date': r.LastAlertDate,
        })
    out.sort(key=lambda x: (x['last_date'] or date.min), reverse=True)
    return out


_QUERY_PENDING_URGENT = """
SELECT
    PO.ordernumber   AS ProductionOrder,
    D.CustomerName,
    D.SONumber,
    D.ItemCode,
    D.ItemName,
    R.DateToship,
    R.QtyToShip,
    R.ShipTo,
    R.AddBayUser
FROM [Traceability_RS].[dyn].[DynamicShippingRules] R
INNER JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] O
       ON  O.DynamicProductionOrderID = R.DynamicProductionOrderID
INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] D
       ON  D.DynamicSaleOrderId = O.DynamicSaleOrderId
INNER JOIN traceability_rs.dbo.Orders PO
       ON  PO.IDOrder = O.IdOrder
WHERE R.ConfirmedAt IS NULL
  AND (
        (SELECT SUM(r3.QtyToShip)
         FROM [Traceability_RS].[dyn].[DynamicShippingRules] r3
         WHERE r3.DynamicProductionOrderID = R.DynamicProductionOrderID
           AND r3.ConfirmedAt IS NULL)
        -
        ISNULL((SELECT SUM(sp.ConfirmedQty)
                FROM [Traceability_RS].[dyn].[ShipmentPallets] sp
                WHERE sp.DynamicProductionOrderID = R.DynamicProductionOrderID), 0)
      ) > 0
ORDER BY R.DateToship ASC
"""


def get_pending_urgent_shipments(conn) -> list:
    """Richieste urgenti di spedizione ancora pendenti (residuo da spedire > 0)."""
    out = []
    try:
        with conn.cursor() as cur:
            cur.execute(_QUERY_PENDING_URGENT)
            for r in cur.fetchall():
                out.append({
                    'order': r.ProductionOrder,
                    'customer': r.CustomerName,
                    'so': r.SONumber,
                    'item_code': r.ItemCode,
                    'item_name': r.ItemName,
                    'date_to_ship': r.DateToship,
                    'qty': r.QtyToShip,
                    'ship_to': r.ShipTo,
                    'requested_by': r.AddBayUser,
                })
    except Exception as e:
        logger.error(f"get_pending_urgent_shipments: {e}", exc_info=True)
    return out


# Fasi che fanno da precursore del versamento a magazzino (FCT, fallback ICT):
# regola empirica dell'utente. Il versamento e' atteso lo stesso giorno della
# richiesta FCT pianificata; ICT si considera solo se manca FCT.
DEPOSIT_PRECURSOR_PHASES = ('FCT', 'ICT')


def get_deposit_status_map(conn, date_from: date, date_to: date) -> dict:
    """Mappa OrderNumber -> {'last_date': datetime} dei versamenti a magazzino
    effettivi (D365 ProdFinishedGoods) nel periodo. La presenza dell'ordine =
    'versato'. Non aggrego le quantita' (la query ripete la GoodQty per box)."""
    import plan_phases
    d_from = datetime(date_from.year, date_from.month, date_from.day)
    d_to = datetime(date_to.year, date_to.month, date_to.day) + timedelta(days=1)
    rows = plan_phases.get_warehouse_finished_goods(conn, d_from, d_to)
    m = {}
    for r in rows:
        o = r.get('order')
        if not o:
            continue
        dt = r.get('date_transfer')
        cur = m.get(o)
        if cur is None:
            m[o] = {'last_date': dt}
        elif dt and (cur['last_date'] is None or dt > cur['last_date']):
            cur['last_date'] = dt
    return m


def _apply_deposit_status(discrepancies: list, deposit_map: dict) -> None:
    """Aggiunge a ogni discrepanza lo stato versamento a magazzino.
    Solo per gli ordini la cui discrepanza tocca FCT (o ICT come fallback):
      - 'versato'  se l'ordine risulta versato a magazzino nel periodo
      - 'mancante' altrimenti
    Per le altre fasi lo stato resta None (non pertinente)."""
    for d in discrepancies:
        tokens = [p.strip().upper() for p in (d.get('phases') or '').split(',')]
        relevant = any(ph in tokens for ph in DEPOSIT_PRECURSOR_PHASES)
        if not relevant:
            d['deposit'] = None
            d['deposit_date'] = None
            continue
        info = deposit_map.get(d['order'])
        if info:
            d['deposit'] = 'versato'
            d['deposit_date'] = info.get('last_date')
        else:
            d['deposit'] = 'mancante'
            d['deposit_date'] = None


def gather(conn) -> dict:
    """Raccoglie tutti i dati per l'email/anteprima."""
    ensure_overrides_table(conn)
    start_date = get_start_date(conn)
    discrepancies = get_open_discrepancies(conn, start_date)
    deposit_map = get_deposit_status_map(conn, start_date, date.today())
    _apply_deposit_status(discrepancies, deposit_map)
    return {
        'start_date': start_date,
        'discrepancies': discrepancies,
        'shipments': get_pending_urgent_shipments(conn),
    }


# ============================================================
# EMAIL HTML (in rumeno)
# ============================================================
def _fmt_date(d) -> str:
    if not d:
        return '—'
    try:
        return d.strftime('%d/%m/%Y')
    except Exception:
        return str(d)


def _fmt_datetime(d) -> str:
    if not d:
        return '—'
    try:
        return d.strftime('%d/%m/%Y %H:%M')
    except Exception:
        return str(d)


def build_email_html(data: dict, logo_cid: str = 'company_logo') -> str:
    """Costruisce il corpo HTML dell'email (rumeno, professionale)."""
    start_date = data['start_date']
    discrepancies = data['discrepancies']
    shipments = data['shipments']
    today = date.today()
    recent_threshold = today - timedelta(days=RECENT_HIGHLIGHT_DAYS)

    logo_tag = (f'<img src="cid:{logo_cid}" style="max-height:60px;margin-bottom:10px;" '
                f'alt="Logo">')

    # Tabella discrepanze
    if discrepancies:
        drows = ""
        for d in discrepancies:
            recent = bool(d['last_date'] and d['last_date'] >= recent_threshold)
            bg = '#FFF3CD' if recent else '#ffffff'
            badge = ' <span style="color:#B71C1C;font-weight:bold;">(recent)</span>' if recent else ''
            # Stato versamento a magazzino (solo per ordini con FCT/ICT)
            dep = d.get('deposit')
            if dep == 'versato':
                dep_html = (f'<span style="color:#0a7d28;font-weight:bold;">Predat</span>'
                            f'{" (" + _fmt_date(d.get("deposit_date")) + ")" if d.get("deposit_date") else ""}')
            elif dep == 'mancante':
                dep_html = '<span style="color:#B71C1C;font-weight:bold;">Lipsă</span>'
            else:
                dep_html = '<span style="color:#999;">—</span>'
            drows += f"""
            <tr style="background:{bg};">
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{d['order']}{badge}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{d['product']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{d['phases']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{d['total']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{d['deficit']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{_fmt_date(d['first_date'])}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{_fmt_date(d['last_date'])}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{dep_html}</td>
            </tr>"""
        disc_table = f"""
        <h3 style="color:#1F3864;margin:18px 0 6px;">Discrepanțe de plan nejustificate ({len(discrepancies)})</h3>
        <table style="border-collapse:collapse;width:100%;font-size:13px;">
            <thead>
                <tr style="background:#1F3864;color:#fff;">
                    <th style="padding:8px 10px;text-align:left;">Comandă</th>
                    <th style="padding:8px 10px;text-align:left;">Produs</th>
                    <th style="padding:8px 10px;text-align:left;">Faze</th>
                    <th style="padding:8px 10px;">Nr. alerte</th>
                    <th style="padding:8px 10px;">Deficit</th>
                    <th style="padding:8px 10px;">Prima alertă</th>
                    <th style="padding:8px 10px;">Ultima alertă</th>
                    <th style="padding:8px 10px;">Predare magazie</th>
                </tr>
            </thead>
            <tbody>{drows}</tbody>
        </table>
        <p style="font-size:12px;color:#666;margin:4px 0 0;">
            Rândurile evidențiate cu galben au alerte din ultimele {RECENT_HIGHLIGHT_DAYS} zile.
            Coloana „Predare magazie" (doar pentru comenzile cu FCT/ICT): <b style="color:#0a7d28;">Predat</b>
            = produs deja predat în magazie (D365); <b style="color:#B71C1C;">Lipsă</b> = încă nepredat.</p>
        """
    else:
        disc_table = ('<h3 style="color:#1F3864;margin:18px 0 6px;">Discrepanțe de plan '
                      'nejustificate</h3><p>Nu există discrepanțe deschise în perioada '
                      f'analizată (începând cu {_fmt_date(start_date)}).</p>')

    # Tabella urgenze spedizione
    if shipments:
        srows = ""
        for s in shipments:
            srows += f"""
            <tr>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{s['order']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{s['customer'] or '—'}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{(s['item_code'] or '')} {(s['item_name'] or '')}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{_fmt_datetime(s['date_to_ship'])}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;text-align:center;">{s['qty']}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{s['ship_to'] or '—'}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #dee2e6;">{s['requested_by'] or '—'}</td>
            </tr>"""
        ship_table = f"""
        <h3 style="color:#1F3864;margin:18px 0 6px;">Cereri urgente de livrare în așteptare ({len(shipments)})</h3>
        <table style="border-collapse:collapse;width:100%;font-size:13px;">
            <thead>
                <tr style="background:#7A1F1F;color:#fff;">
                    <th style="padding:8px 10px;text-align:left;">Comandă</th>
                    <th style="padding:8px 10px;text-align:left;">Client</th>
                    <th style="padding:8px 10px;text-align:left;">Articol</th>
                    <th style="padding:8px 10px;">Data livrării</th>
                    <th style="padding:8px 10px;">Cantitate</th>
                    <th style="padding:8px 10px;text-align:left;">Livrare către</th>
                    <th style="padding:8px 10px;text-align:left;">Solicitat de</th>
                </tr>
            </thead>
            <tbody>{srows}</tbody>
        </table>
        """
    else:
        ship_table = ('<h3 style="color:#1F3864;margin:18px 0 6px;">Cereri urgente de '
                      'livrare</h3><p>Nu există cereri urgente de livrare în așteptare.</p>')

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;color:#333;line-height:1.6;margin:0;padding:0;">
  <div style="max-width:960px;margin:0 auto;padding:20px;">
    <div style="text-align:center;border-bottom:3px solid #1F3864;padding-bottom:10px;margin-bottom:16px;">
      {logo_tag}
      <h2 style="color:#1F3864;margin:6px 0;">Raport zilnic — respectarea planului de producție</h2>
    </div>

    <p>Stimați responsabili de producție,</p>

    <p>Vă transmitem situația actualizată a <b>discrepanțelor de plan de producție rămase
    nejustificate</b> (începând cu data de <b>{_fmt_date(start_date)}</b>) și a
    <b>cererilor urgente de livrare</b> aflate în așteptare. Vă rugăm să furnizați
    <b>explicații punctuale și corecte</b> pentru fiecare situație în parte.</p>

    <p>Aceste informații trebuie să fie <b>exacte și complete</b>: numai pe baza unor date
    corecte conducerea poate analiza cauzele reale și îmbunătăți gestionarea producției.</p>

    <p>Facem apel la <b>simțul dumneavoastră de responsabilitate</b> pentru funcția pe care
    compania v-a încredințat-o. Vă reamintim, de asemenea, că aveți deplina libertate de a
    <b>evalua personalul din subordine în funcție de performanțele reale</b> ale fiecăruia și
    că, în cele din urmă, <b>calitatea rezultatelor dumneavoastră depinde în primul rând de
    echipa pe care ați ales-o</b>.</p>

    {disc_table}

    {ship_table}

    <p style="margin-top:18px;">Vă rugăm să accesați formularul <b>„Plan de producție —
    Discrepanțe"</b> din aplicație pentru a justifica fiecare discrepanță în cel mai scurt timp.</p>

    <p>Vă mulțumim pentru colaborare și pentru profesionalismul dumneavoastră.</p>
    <p style="margin-top:10px;color:#1F3864;"><b>Conducerea Producției</b></p>

    <hr style="border:none;border-top:1px solid #ddd;margin:20px 0 8px;">
    <p style="font-size:11px;color:#999;">Mesaj generat automat de sistemul de monitorizare a
    planului de producție. Vă rugăm să nu răspundeți la această adresă.</p>
  </div>
</body>
</html>"""
    return html


# ============================================================
# DEDUP + INVIO
# ============================================================
def _claim_send_slot(conn, setting_key: str) -> bool:
    """True se questo PC vince la corsa all'invio odierno (INSERT WHERE NOT EXISTS)."""
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO traceability_rs.dbo.settings (atribute, [value])
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM traceability_rs.dbo.settings
                WITH (UPDLOCK, HOLDLOCK) WHERE atribute = ?
            )
        """, (setting_key, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), setting_key))
        claimed = cur.rowcount > 0
        conn.commit()
        cur.close()
        return claimed
    except Exception as e:
        logger.error(f"_claim_send_slot: {e}", exc_info=True)
        return False


def send_daily_responsibles_email(conn, mode: str = None,
                                  logo_path: str = 'logo.png',
                                  force: bool = False) -> tuple:
    """Invia l'email giornaliera ai responsabili.

    Args:
        mode : 'True' | 'Test' | 'False'. Se None usa la modalita' DEDICATA
               (Sys_plan_responsibles_email_mode, default 'Test'), indipendente
               dall'escalation piano. 'Test' reindirizza a TEST_EMAIL; 'False' non invia.
        force: se True ignora il dedup giornaliero (usato dal pulsante "Invia adesso").

    Returns:
        (sent: bool, message: str)
    """
    if mode is None:
        mode = get_email_mode(conn)
    if mode == 'False':
        return False, "Email responsabili disabilitata (modalità dedicata = False)"

    data = gather(conn)
    if not data['discrepancies'] and not data['shipments'] and not force:
        return False, "Nessuna discrepanza aperta né urgenza: email non inviata"

    to_emails, cc_emails, _to_people, _cc_people = get_effective_recipients(conn)
    if not to_emails:
        return False, "Nessun destinatario (responsabile) trovato"

    # Dedup giornaliero (salvo invio forzato)
    if not force:
        key = SEND_SLOT_PREFIX + date.today().strftime('%Y%m%d')
        if not _claim_send_slot(conn, key):
            return False, "Email già inviata oggi (da questo o altro PC)"

    subject = "Raport zilnic — respectarea planului de producție și livrări urgente"
    body = build_email_html(data)

    # Override modalità Test (riuso della logica dell'escalation piano)
    to_emails, cc_emails, subject = pae._apply_test_mode_override(
        mode, to_emails, cc_emails, subject)

    attachments = None
    if logo_path and os.path.exists(logo_path):
        attachments = [('inline', logo_path, 'company_logo')]

    try:
        from utils import send_email
        send_email(recipients=to_emails, subject=subject, body=body,
                   is_html=True, cc_emails=cc_emails or None, attachments=attachments)
        logger.info("Email responsabili piano inviata: TO=%s CC=%s (discr=%d, urg=%d)",
                    to_emails, cc_emails, len(data['discrepancies']), len(data['shipments']))
        return True, (f"Email inviata a {len(to_emails)} destinatari "
                      f"({len(data['discrepancies'])} discrepanze, {len(data['shipments'])} urgenze)")
    except Exception as e:
        logger.error(f"send_daily_responsibles_email: invio fallito: {e}", exc_info=True)
        return False, f"Errore invio email: {e}"
