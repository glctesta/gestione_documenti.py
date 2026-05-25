# -*- coding: utf-8 -*-
"""
fqc_email.py
FQC (Final Quality Control) shift-end email report.

Sent twice per working day (Mon–Sat):
    15:30 → covers shift 07:30 – 15:30
    23:30 → covers shift 15:30 – 23:30

Recipients: settings.atribute = 'Sys_check_final_product'
Anti-duplication key: FqcShiftEmail_YYYYMMDD_HHMM  (e.g. 20260520_1530)
"""
from __future__ import annotations

import datetime
import logging
import os
from typing import Optional

logger = logging.getLogger("TraceabilityRS")

# ── SQL ───────────────────────────────────────────────────────────────────────

# Products processed in PTHM phase (IDPhase=107) within the shift window.
# Parameters: (shift_start, shift_end)
_Q_PRODUCTS_IN_SHIFT = """
SELECT DISTINCT
    p.IDProduct,
    p.ProductCode
FROM Traceability_rs.dbo.Scannings                sc
INNER JOIN Traceability_rs.dbo.OrderPhases         op  ON sc.IDOrderPhase = op.IDOrderPhase
INNER JOIN Traceability_rs.dbo.Orders              o   ON op.IDOrder      = o.IDOrder
INNER JOIN Traceability_rs.dbo.Phases              ph  ON op.IDPhase      = ph.IDPhase
INNER JOIN Traceability_rs.dbo.Products            p   ON o.IDProduct     = p.IDProduct
INNER JOIN Traceability_rs.dbo.Boards              b   ON b.IDBoard       = sc.IDBoard
WHERE
    ph.IDPhase IN (107)
    AND sc.ScanTimeFinish BETWEEN ? AND ?
GROUP BY
    p.IDProduct, p.ProductCode
ORDER BY
    p.ProductCode
"""

# Products that have been verified within the shift window
_Q_VERIFIED_IN_SHIFT = """
SELECT DISTINCT p.IDProduct, p.ProductCode
FROM   [Traceability_RS].[chk].[ProductCheckListDataLogs]   l
INNER JOIN [Traceability_RS].[chk].[ProductCheckListDatas]   d
       ON  l.ProductCheckListDataId = d.ProductCheckListDataId
INNER JOIN [Traceability_RS].[chk].[ProductCheckLists]       cl
       ON  d.ProductCheckListId = cl.ProductCheckListId
INNER JOIN [Traceability_RS].[dbo].[Products]                p
       ON  cl.IdProduct = p.IDProduct
WHERE  l.DateCheckList >= ? AND l.DateCheckList < ?
ORDER  BY p.ProductCode
"""

# NOK items within the shift window
_Q_NOK_IN_SHIFT = """
SELECT
    p.ProductCode,
    d.ItemToCheckNumber,
    d.ItemToCheck,
    l.NotOkNote,
    l.[User],
    l.DateCheckList
FROM   [Traceability_RS].[chk].[ProductCheckListDataLogs]   l
INNER JOIN [Traceability_RS].[chk].[ProductCheckListDatas]   d
       ON  l.ProductCheckListDataId = d.ProductCheckListDataId
INNER JOIN [Traceability_RS].[chk].[ProductCheckLists]       cl
       ON  d.ProductCheckListId = cl.ProductCheckListId
INNER JOIN [Traceability_RS].[dbo].[Products]                p
       ON  cl.IdProduct = p.IDProduct
WHERE  l.IsOK = 0
  AND  l.DateCheckList >= ?
  AND  l.DateCheckList < ?
ORDER  BY p.ProductCode, d.ItemToCheckNumber
"""

# Recipient addresses
_Q_RECIPIENTS = """
SELECT [VALUE]
FROM   traceability_rs.dbo.settings
WHERE  atribute = 'Sys_check_final_product'
  AND  ISNULL(DateOut, '9999-01-01') > GETDATE()
"""

# Anti-duplication
_Q_ALREADY_SENT = """
SELECT COUNT(*)
FROM   traceability_rs.dbo.settings
WHERE  atribute = ?
"""

_Q_MARK_SENT = """
INSERT INTO traceability_rs.dbo.settings (atribute, [VALUE])
VALUES (?, ?)
"""

# ── Logo helper ───────────────────────────────────────────────────────────────

def _logo_base64() -> str:
    """Return base64 of Logo.png if present."""
    logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
    if not os.path.isfile(logo_path):
        return ''
    try:
        import base64
        with open(logo_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    except Exception:
        return ''

# ── Core function ─────────────────────────────────────────────────────────────

def run_fqc_shift_email(db, shift_start: datetime.datetime, shift_end: datetime.datetime,
                        shift_label: str) -> None:
    """
    Build and send the FQC shift-end email.

    Args:
        db:           DB wrapper object (db.conn, db.fetch_setting, db.execute_query)
        shift_start:  datetime — inclusive start of the shift window
        shift_end:    datetime — exclusive end of the shift window
        shift_label:  e.g. '1530' or '2330' (used in the anti-dup key)
    """
    today_str   = datetime.date.today().strftime('%Y%m%d')
    setting_key = f'FqcShiftEmail_{today_str}_{shift_label}'

    conn = db.conn

    # ── Anti-duplication ──────────────────────────────────────────────────────
    try:
        cur = conn.cursor()
        cur.execute(_Q_ALREADY_SENT, (setting_key,))
        count = cur.fetchone()[0]
        if count > 0:
            logger.info(f"fqc_email: {setting_key} already sent — skip")
            return
        # Claim the slot immediately (before any await)
        cur.execute(_Q_MARK_SENT, (setting_key,
                                   datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        cur.close()
    except Exception as exc:
        logger.error(f"fqc_email anti-dup: {exc}")
        return

    # ── Recipients ────────────────────────────────────────────────────────────
    try:
        cur = conn.cursor()
        cur.execute(_Q_RECIPIENTS)
        rows = cur.fetchall()
        cur.close()
        recipients = [r[0].strip() for r in rows if r[0] and r[0].strip()]
    except Exception as exc:
        logger.error(f"fqc_email recipients: {exc}")
        return

    if not recipients:
        logger.warning("fqc_email: no recipients for Sys_check_final_product")
        return

    # ── Data retrieval ────────────────────────────────────────────────────────
    try:
        cur = conn.cursor()

        # "Previsti": products processed in PTHM (IDPhase=107) during the shift
        cur.execute(_Q_PRODUCTS_IN_SHIFT, (shift_start, shift_end))
        all_products = {r[0]: r[1] for r in cur.fetchall()}   # id → code

        # "Verificati": products with at least one FQC log in the same shift window
        cur.execute(_Q_VERIFIED_IN_SHIFT, (shift_start, shift_end))
        verified = {r[0]: r[1] for r in cur.fetchall()}        # id → code

        # NOK items in the same window
        cur.execute(_Q_NOK_IN_SHIFT, (shift_start, shift_end))
        nok_rows = cur.fetchall()

        cur.close()
    except Exception as exc:
        logger.error(f"fqc_email data query: {exc}", exc_info=True)
        return

    missing = {pid: code for pid, code in all_products.items()
               if pid not in verified}

    # ── Build HTML ────────────────────────────────────────────────────────────
    logo_b64 = _logo_base64()
    logo_img  = (f'<img src="data:image/png;base64,{logo_b64}" '
                 f'style="height:44px;margin-right:16px;" alt="Logo"/>'
                 if logo_b64 else '')

    shift_str = f"{shift_start.strftime('%H:%M')} – {shift_end.strftime('%H:%M')}"
    date_str  = datetime.date.today().strftime('%d / %m / %Y')

    # Colour coding
    ok_color      = '#27ae60'
    missing_color = '#e74c3c'
    nok_color     = '#f39c12'
    hdr_color     = '#1f3864'

    def _table_row(bg, *cells):
        tds = ''.join(f'<td style="padding:6px 10px;border-bottom:1px solid #eee;">{c}</td>'
                      for c in cells)
        return f'<tr style="background:{bg};">{tds}</tr>'

    # Verified table
    verified_html = ''
    for pid, code in sorted(verified.items(), key=lambda x: x[1]):
        verified_html += _table_row('#eafaf1', code, '✅ Verified')

    # Missing table
    missing_html = ''
    for pid, code in sorted(missing.items(), key=lambda x: x[1]):
        missing_html += _table_row('#fdf2f8', code, '❌ Missing')

    # NOK table
    nok_html = ''
    for r in nok_rows:
        prod, item_n, item_desc, note, user, dt = r
        dt_str = dt.strftime('%H:%M') if dt else ''
        nok_html += _table_row('#fff8e1',
                                prod,
                                f'#{item_n} — {item_desc[:50]}',
                                note or '',
                                user,
                                dt_str)

    def _section(title, color, table_body, headers):
        if not table_body:
            return ''
        ths = ''.join(f'<th style="padding:6px 10px;text-align:left;">{h}</th>'
                      for h in headers)
        return f"""
        <h3 style="color:{color};margin-top:20px;">{title}</h3>
        <table style="border-collapse:collapse;width:100%;font-size:13px;">
          <thead><tr style="background:{color};color:#fff;">{ths}</tr></thead>
          <tbody>{table_body}</tbody>
        </table>"""

    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"/></head>
    <body style="font-family:Segoe UI,Arial,sans-serif;margin:0;padding:0;background:#f4f6f8;">
      <table width="100%" cellpadding="0" cellspacing="0"
             style="background:{hdr_color};padding:16px 24px;">
        <tr>
          <td>{logo_img}</td>
          <td style="color:#fff;">
            <span style="font-size:18px;font-weight:bold;">
              FQC Products — Shift Report
            </span><br/>
            <span style="font-size:12px;color:#a8c4e0;">
              {date_str} &nbsp;|&nbsp; Shift: {shift_str}
            </span>
          </td>
        </tr>
      </table>
      <div style="padding:20px 24px;background:#fff;">
        <p style="color:#555;font-size:13px;">
          This is the automated FQC shift summary for the period
          <strong>{shift_start.strftime('%d/%m/%Y %H:%M')}</strong>
          –
          <strong>{shift_end.strftime('%H:%M')}</strong>.
        </p>

        <!-- Summary badges -->
        <table style="margin-bottom:20px;">
          <tr>
            <td style="padding:8px 16px;background:{hdr_color};color:#fff;
                       border-radius:4px;font-size:13px;text-align:center;margin-right:8px;">
              📋 Expected<br/><strong style="font-size:22px;">{len(all_products)}</strong>
            </td>
            <td width="8"></td>
            <td style="padding:8px 16px;background:{ok_color};color:#fff;
                       border-radius:4px;font-size:13px;text-align:center;">
              ✅ Verified<br/><strong style="font-size:22px;">{len(verified)}</strong>
            </td>
            <td width="8"></td>
            <td style="padding:8px 16px;background:{missing_color};color:#fff;
                       border-radius:4px;font-size:13px;text-align:center;">
              ❌ Missing<br/><strong style="font-size:22px;">{len(missing)}</strong>
            </td>
            <td width="8"></td>
            <td style="padding:8px 16px;background:{nok_color};color:#fff;
                       border-radius:4px;font-size:13px;text-align:center;">
              ⚠ NOK Items<br/><strong style="font-size:22px;">{len(nok_rows)}</strong>
            </td>
          </tr>
        </table>

        {_section('✅ Verified Products', ok_color, verified_html,
                   ['Product Code', 'Status'])}
        {_section('❌ Missing Verifications', missing_color, missing_html,
                   ['Product Code', 'Status'])}
        {_section('⚠ NOK Items', nok_color, nok_html,
                   ['Product', 'Item', 'Note', 'User', 'Time'])}

        <p style="color:#aaa;font-size:11px;margin-top:30px;border-top:1px solid #eee;
                  padding-top:10px;">
          This email was generated automatically by Document Management —
          FQC Module at {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}.
          Do not reply to this message.
        </p>
      </div>
    </body>
    </html>
    """

    # ── Send ──────────────────────────────────────────────────────────────────
    subject = (f"FQC Shift Report — {date_str} "
               f"[{shift_str}] — "
               f"{len(verified)}/{len(all_products)} verified")
    try:
        import utils
        utils.send_email(
            to_addresses=recipients,
            subject=subject,
            body=body_html,
            is_html=True
        )
        logger.info(f"fqc_email: sent to {recipients} ({shift_label})")
    except Exception as exc:
        logger.error(f"fqc_email send: {exc}", exc_info=True)


# ── Convenience wrappers called by the scheduler ──────────────────────────────

def run_fqc_shift_1530(db) -> None:
    """15:30 email: covers shift 07:30 → 15:30."""
    today = datetime.date.today()
    start = datetime.datetime.combine(today, datetime.time(7, 30))
    end   = datetime.datetime.combine(today, datetime.time(15, 30))
    run_fqc_shift_email(db, start, end, '1530')


def run_fqc_shift_2330(db) -> None:
    """23:30 email: covers shift 15:30 → 23:30."""
    today = datetime.date.today()
    start = datetime.datetime.combine(today, datetime.time(15, 30))
    end   = datetime.datetime.combine(today, datetime.time(23, 30))
    run_fqc_shift_email(db, start, end, '2330')
