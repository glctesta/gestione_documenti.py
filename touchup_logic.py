# -*- coding: utf-8 -*-
"""
touchup_logic.py
Layer dati/logica per il modulo Touch-Up (nessuna dipendenza da tkinter).
Vedi docs/TouchUp_Spec_v1.0.md

- verifica LabelCode (riuso query FAI/FQC)
- catalogo problemi + instradamento (problema -> CdcId/SubCdcId)
- salvataggio segnalazione con ricorrenza / riapertura / escalation / email
- destinatari (tecnici + capo functioncode=70) per problema
- risposte del tecnico (chiusura + tempo di reazione)
- report pendenti per le postazioni (monitor popup)
"""
import logging
import socket
from datetime import datetime, time, timedelta

logger = logging.getLogger(__name__)

WARNING_EMAIL_ATTRIBUTE = 'Sys_email_TouchUp_warning'
BOSS_FUNCTION_CODE = 70

# --- verifica LabelCode (come FAI/FQC) ---
_Q_LABELCODE_INFO = """
SELECT TOP 1 l.IDLabelCode, l.LabelCod, o.IDOrder, o.OrderNumber,
       p.IDProduct, p.ProductCode
FROM Traceability_RS.dbo.LabelCodes l
INNER JOIN Traceability_RS.dbo.Boards   b ON b.IDBoard   = l.IDBoard
INNER JOIN Traceability_RS.dbo.Orders   o ON o.IDOrder   = b.IDOrder
INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
WHERE l.LabelCod = ?
ORDER BY l.IDLabelCode DESC
"""

# --- destinatari per CdcId + lista SubCdcId (query fornita dall'utente) ---
_Q_RECIPIENTS = """
SELECT c.CdcId, c.CdcDescription, cs.SubCdcId, cs.SubCdcDescription,
       e.EmployeeName + ' ' + e.EmployeeSurname AS Employee,
       f.functioncode, a.WorkEmail
FROM employee.dbo.costcenters c
  INNER JOIN employee.dbo.cdcsub cs ON c.cdcid = cs.cdcid
  INNER JOIN employee.dbo.EmployeeCdcStories ch ON ch.SubCdcId = cs.SubCdcId AND ch.dateout IS NULL
  INNER JOIN employee.dbo.functions f ON f.functionid = ch.FunctionId
  INNER JOIN employee.dbo.employeehirehistory h ON ch.EmployeeHireHistoryId = h.EmployeeHireHistoryId
       AND h.employeerid = 2 AND h.EndWorkDate IS NULL
  INNER JOIN employee.dbo.employees e ON e.employeeid = h.employeeid
  INNER JOIN employee.dbo.EmployeeAddress a ON a.EmployeeId = e.employeeid AND a.dateout IS NULL
WHERE c.cdcid = ? AND cs.subcdcid IN ({subcdc_ph})
"""


# ─────────────────────────────────────────────────────────────────────────────
#  Accesso DB (usa il wrapper dell'app: _lock, cursor, conn)
# ─────────────────────────────────────────────────────────────────────────────
def _query(db, sql, params=None):
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
    return [dict(zip(cols, r)) for r in rows]


def _scalar(db, sql, params=None):
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(sql, params or ())
        row = cur.fetchone()
    return row[0] if row else None


def _production_day_start(now=None):
    """Inizio del giorno di produzione (07:30) che contiene 'now'."""
    now = now or datetime.now()
    today_730 = datetime.combine(now.date(), time(7, 30))
    return today_730 if now >= today_730 else today_730 - timedelta(days=1)


# ─────────────────────────────────────────────────────────────────────────────
#  Verifica LabelCode
# ─────────────────────────────────────────────────────────────────────────────
def verify_labelcode(db, labelcod):
    """Ritorna dict(IDLabelCode, LabelCod, IDOrder, OrderNumber, IDProduct, ProductCode) o None."""
    rows = _query(db, _Q_LABELCODE_INFO, (labelcod,))
    return rows[0] if rows else None


# ─────────────────────────────────────────────────────────────────────────────
#  Catalogo problemi
# ─────────────────────────────────────────────────────────────────────────────
def get_active_problems(db):
    return _query(db,
                  "SELECT TouchUpProblemId, ProblemCode, ProblemDescription, Severity "
                  "FROM dbo.TouchUpProblems WHERE DateOut IS NULL ORDER BY ProblemDescription")


def get_all_problems(db):
    return _query(db,
                  "SELECT TouchUpProblemId, ProblemCode, ProblemDescription, Severity, DateOut "
                  "FROM dbo.TouchUpProblems ORDER BY ProblemDescription")


def add_problem(db, code, description, severity=None):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute(
            "INSERT INTO dbo.TouchUpProblems (ProblemCode, ProblemDescription, Severity) VALUES (?, ?, ?)",
            (code or None, description, severity))
        db.conn.commit()


def update_problem(db, problem_id, code, description, severity=None):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute(
            "UPDATE dbo.TouchUpProblems SET ProblemCode=?, ProblemDescription=?, Severity=? "
            "WHERE TouchUpProblemId=?", (code or None, description, severity, problem_id))
        db.conn.commit()


def deactivate_problem(db, problem_id):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute("UPDATE dbo.TouchUpProblems SET DateOut=GETDATE() WHERE TouchUpProblemId=?",
                          (problem_id,))
        db.conn.commit()


# ─────────────────────────────────────────────────────────────────────────────
#  Instradamento problema -> reparto
# ─────────────────────────────────────────────────────────────────────────────
def get_routing(db, problem_id):
    return _query(db,
                  "SELECT rt.TouchUpRoutingId, rt.CdcId, c.CdcDescription, rt.SubCdcId, cs.SubCdcDescription "
                  "FROM dbo.TouchUpProblemRouting rt "
                  "LEFT JOIN employee.dbo.costcenters c ON c.CdcId = rt.CdcId "
                  "LEFT JOIN employee.dbo.CdcSub cs ON cs.SubCdcId = rt.SubCdcId "
                  "WHERE rt.TouchUpProblemId = ? AND rt.DateOut IS NULL "
                  "ORDER BY c.CdcDescription, cs.SubCdcDescription", (problem_id,))


def add_routing(db, problem_id, cdc_id, sub_cdc_id):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute(
            "INSERT INTO dbo.TouchUpProblemRouting (TouchUpProblemId, CdcId, SubCdcId) VALUES (?, ?, ?)",
            (problem_id, cdc_id, sub_cdc_id))
        db.conn.commit()


def remove_routing(db, routing_id):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute("UPDATE dbo.TouchUpProblemRouting SET DateOut=GETDATE() WHERE TouchUpRoutingId=?",
                          (routing_id,))
        db.conn.commit()


def get_cost_centers(db):
    return _query(db, "SELECT CdcId, Cdc, CdcDescription FROM employee.dbo.costcenters ORDER BY CdcDescription")


def get_sub_cost_centers(db, cdc_id):
    return _query(db, "SELECT SubCdcId, SubCdc, SubCdcDescription FROM employee.dbo.CdcSub "
                      "WHERE CdcId = ? ORDER BY SubCdcDescription", (cdc_id,))


# ─────────────────────────────────────────────────────────────────────────────
#  Destinatari (tecnici + capo) per un problema
# ─────────────────────────────────────────────────────────────────────────────
def get_recipients_for_problems(db, problem_ids):
    """Ritorna (tecnici:set[email], capi:set[email]) per i reparti instradati dei problemi."""
    tech, boss = set(), set()
    if not problem_ids:
        return tech, boss
    ph = ','.join(['?'] * len(problem_ids))
    routes = _query(db, f"SELECT DISTINCT CdcId, SubCdcId FROM dbo.TouchUpProblemRouting "
                        f"WHERE TouchUpProblemId IN ({ph}) AND DateOut IS NULL", tuple(problem_ids))
    # raggruppa SubCdcId per CdcId (SubCdcId NULL -> tutti i sub del CdC)
    by_cdc = {}
    for r in routes:
        by_cdc.setdefault(r['CdcId'], set())
        if r['SubCdcId'] is not None:
            by_cdc[r['CdcId']].add(r['SubCdcId'])
    for cdc_id, subs in by_cdc.items():
        if not subs:  # routing a livello CdC: prendi tutti i SubCdc del CdC
            subs = {s['SubCdcId'] for s in get_sub_cost_centers(db, cdc_id)}
        if not subs:
            continue
        sub_list = list(subs)
        sub_ph = ','.join(['?'] * len(sub_list))
        sql = _Q_RECIPIENTS.format(subcdc_ph=sub_ph)
        for row in _query(db, sql, tuple([cdc_id] + sub_list)):
            email = (row.get('WorkEmail') or '').strip()
            if not email:
                continue
            if row.get('functioncode') == BOSS_FUNCTION_CODE:
                boss.add(email)
            else:
                tech.add(email)
    return tech, boss


# ─────────────────────────────────────────────────────────────────────────────
#  Salvataggio segnalazione + ricorrenza / riapertura / escalation / email
# ─────────────────────────────────────────────────────────────────────────────
def save_report(db, user_name, labels, problem_ids, lang=None, notes=None):
    """Salva una segnalazione Touch-Up.
       labels: list[dict] con IDLabelCode, LabelCod, IDOrder, OrderNumber, IDProduct, ProductCode
       problem_ids: list[int]
    Ritorna dict(report_id, status, recurrence, reopen_count, email_sent, boss_escalated).
    """
    if not labels or not problem_ids:
        raise ValueError("Servono almeno una scheda e un problema")
    host = socket.gethostname()
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(
            "INSERT INTO dbo.TouchUpReports (CreatedByUser, ComputerSrc, Notes) "
            "OUTPUT INSERTED.TouchUpReportId VALUES (?, ?, ?)", (user_name, host, notes))
        report_id = int(cur.fetchone()[0])
        for lb in labels:
            cur.execute(
                "INSERT INTO dbo.TouchUpReportLabels "
                "(TouchUpReportId, IDLabelCode, LabelCod, IDOrder, OrderNumber, IDProduct, ProductCode) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (report_id, lb.get('IDLabelCode'), lb.get('LabelCod'), lb.get('IDOrder'),
                 lb.get('OrderNumber'), lb.get('IDProduct'), lb.get('ProductCode')))
        for pid in problem_ids:
            cur.execute("INSERT INTO dbo.TouchUpReportProblems (TouchUpReportId, TouchUpProblemId) "
                        "VALUES (?, ?)", (report_id, pid))
        db.conn.commit()

    orders = [o for o in {lb.get('OrderNumber') for lb in labels} if o]
    products = [p for p in {lb.get('ProductCode') for lb in labels} if p]
    day_start = _production_day_start()

    recurrence = False
    reopen_count = 0
    boss_escalate = False

    for pid in problem_ids:
        # ricorrenza stesso ordine+problema (report precedenti diversi da questo)
        if orders:
            oph = ','.join(['?'] * len(orders))
            cnt = _scalar(db,
                          f"SELECT COUNT(DISTINCT rp.TouchUpReportId) "
                          f"FROM dbo.TouchUpReportProblems rp "
                          f"JOIN dbo.TouchUpReportLabels rl ON rl.TouchUpReportId = rp.TouchUpReportId "
                          f"WHERE rp.TouchUpProblemId = ? AND rl.OrderNumber IN ({oph}) "
                          f"AND rp.TouchUpReportId <> ?", tuple([pid] + orders + [report_id])) or 0
            if cnt >= 1:
                recurrence = True
        # riapertura: report CHIUSI con stesso prodotto+problema
        if products:
            pph = ','.join(['?'] * len(products))
            rc = _scalar(db,
                         f"SELECT COUNT(DISTINCT r.TouchUpReportId) "
                         f"FROM dbo.TouchUpReports r "
                         f"JOIN dbo.TouchUpReportProblems rp ON rp.TouchUpReportId = r.TouchUpReportId "
                         f"JOIN dbo.TouchUpReportLabels rl ON rl.TouchUpReportId = r.TouchUpReportId "
                         f"WHERE r.Status = 'CLOSED' AND rp.TouchUpProblemId = ? AND rl.ProductCode IN ({pph}) "
                         f"AND r.TouchUpReportId <> ?", tuple([pid] + products + [report_id])) or 0
            reopen_count = max(reopen_count, rc)
        # soglia giornaliera stesso problema (qualsiasi ordine/prodotto)
        day_cnt = _scalar(db,
                          "SELECT COUNT(DISTINCT rp.TouchUpReportId) "
                          "FROM dbo.TouchUpReportProblems rp "
                          "JOIN dbo.TouchUpReports r ON r.TouchUpReportId = rp.TouchUpReportId "
                          "WHERE rp.TouchUpProblemId = ? AND r.CreatedAt >= ?",
                          (pid, day_start)) or 0
        threshold = _scalar(db, "SELECT DayRecurrenceThreshold FROM dbo.TouchUpConfig WHERE Id=1") or 3
        if day_cnt >= threshold:
            boss_escalate = True

    is_reopen = reopen_count > 0
    status = 'REOPENED' if is_reopen else 'NEW'
    esc_level = 2 if boss_escalate else (1 if (recurrence or is_reopen) else 0)

    db._ensure_connection()
    with db._lock:
        db.cursor.execute(
            "UPDATE dbo.TouchUpReports SET Status=?, ReopenCount=?, EscalationLevel=?, BossEscalated=? "
            "WHERE TouchUpReportId=?",
            (status, reopen_count, esc_level, 1 if boss_escalate else 0, report_id))
        db.conn.commit()

    email_sent = False
    # email ad ogni ricorrenza (>=2ª) o riapertura o escalation al capo
    if recurrence or is_reopen or boss_escalate:
        email_sent = _send_warning_email(db, report_id, problem_ids, recurrence, is_reopen,
                                         reopen_count, boss_escalate, lang)

    return {'report_id': report_id, 'status': status, 'recurrence': recurrence,
            'reopen_count': reopen_count, 'email_sent': email_sent, 'boss_escalated': boss_escalate}


def _send_warning_email(db, report_id, problem_ids, recurrence, is_reopen, reopen_count, boss_escalate, lang):
    try:
        import utils
        recipients = utils.get_email_recipients(db.conn, WARNING_EMAIL_ATTRIBUTE) or []
        tech, boss = get_recipients_for_problems(db, problem_ids)
        cc = sorted((set(boss) | (set(tech) if False else set())))  # capo in CC; tecnici opzionali
        if not recipients and not boss:
            logger.warning("Touch-Up: nessun destinatario email warning")
            return False
        if not recipients:
            recipients = sorted(boss)
            cc = []
        detail = get_report_detail(db, report_id)
        reasons = []
        if recurrence:
            reasons.append("segnalazione RICORRENTE (stesso ordine+problema)")
        if is_reopen:
            reasons.append(f"RIAPERTURA (stesso prodotto+problema, {reopen_count}x)")
        if boss_escalate:
            reasons.append("SOGLIA GIORNALIERA superata (escalation responsabile)")
        labels_html = "".join(
            f"<tr><td>{l['LabelCod']}</td><td>{l['OrderNumber']}</td><td>{l['ProductCode']}</td></tr>"
            for l in detail['labels'])
        probs_html = ", ".join(p['ProblemDescription'] for p in detail['problems'])
        subject = f"[Touch-Up] Avviso #{report_id} - {'; '.join(reasons)}"
        body = f"""<html><body style="font-family:'Segoe UI',Arial,sans-serif;font-size:13px;color:#333;">
<div style="background:#c0392b;color:#fff;padding:14px;border-radius:4px;">
  <h2 style="margin:0;">Touch-Up - Avviso problema schede #{report_id}</h2>
  <p style="margin:4px 0 0;">{'; '.join(reasons)}</p>
</div>
<p>Segnalato da <strong>{detail['report'].get('CreatedByUser','')}</strong> il
   {detail['report'].get('CreatedAt')}.</p>
<p><strong>Problemi:</strong> {probs_html}</p>
<table style="border-collapse:collapse;"><tr style="background:#34495e;color:#fff;">
  <th style="padding:6px 10px;">LabelCode</th><th style="padding:6px 10px;">Ordine</th>
  <th style="padding:6px 10px;">Prodotto</th></tr>{labels_html}</table>
<p style="color:#888;font-size:11px;">Email automatica TraceabilityRS - non rispondere.</p>
</body></html>"""
        utils.send_email(recipients, subject, body, is_html=True, cc_emails=cc or None)
        db._ensure_connection()
        with db._lock:
            db.cursor.execute("UPDATE dbo.TouchUpReports SET EmailSentCount = EmailSentCount + 1 "
                              "WHERE TouchUpReportId=?", (report_id,))
            db.conn.commit()
        logger.info(f"Touch-Up: email warning #{report_id} a {recipients} CC {cc}")
        return True
    except Exception as e:
        logger.error(f"Touch-Up: errore invio email warning #{report_id}: {e}", exc_info=True)
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  Dettaglio report
# ─────────────────────────────────────────────────────────────────────────────
def get_report_detail(db, report_id):
    rep = _query(db, "SELECT * FROM dbo.TouchUpReports WHERE TouchUpReportId=?", (report_id,))
    labels = _query(db, "SELECT LabelCod, OrderNumber, ProductCode FROM dbo.TouchUpReportLabels "
                        "WHERE TouchUpReportId=? ORDER BY OrderNumber, LabelCod", (report_id,))
    problems = _query(db, "SELECT p.TouchUpProblemId, p.ProblemDescription "
                          "FROM dbo.TouchUpReportProblems rp "
                          "JOIN dbo.TouchUpProblems p ON p.TouchUpProblemId=rp.TouchUpProblemId "
                          "WHERE rp.TouchUpReportId=?", (report_id,))
    responses = _query(db, "SELECT RespondedByUser, RespondedAt, ReactionSeconds, ActionsTaken "
                           "FROM dbo.TouchUpResponses WHERE TouchUpReportId=? ORDER BY RespondedAt", (report_id,))
    return {'report': rep[0] if rep else {}, 'labels': labels, 'problems': problems, 'responses': responses}


# ─────────────────────────────────────────────────────────────────────────────
#  Risposta del tecnico (chiusura + tempo di reazione)
# ─────────────────────────────────────────────────────────────────────────────
def mark_response(db, report_id, user_name, actions):
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute("SELECT CreatedAt, FirstResponseAt FROM dbo.TouchUpReports WHERE TouchUpReportId=?",
                    (report_id,))
        row = cur.fetchone()
        if not row:
            return False
        created_at, first_resp = row[0], row[1]
        cur.execute("SELECT DATEDIFF(SECOND, ?, GETDATE())", (created_at,))
        reaction = int(cur.fetchone()[0] or 0)
        cur.execute(
            "INSERT INTO dbo.TouchUpResponses (TouchUpReportId, RespondedByUser, ReactionSeconds, ActionsTaken) "
            "VALUES (?, ?, ?, ?)", (report_id, user_name, reaction, actions))
        cur.execute(
            "UPDATE dbo.TouchUpReports "
            "SET Status='CLOSED', ClosedAt=GETDATE(), "
            "    FirstResponseAt = ISNULL(FirstResponseAt, GETDATE()) "
            "WHERE TouchUpReportId=?", (report_id,))
        db.conn.commit()
    return True


# ─────────────────────────────────────────────────────────────────────────────
#  Report pendenti per le postazioni (monitor popup)
# ─────────────────────────────────────────────────────────────────────────────
def get_pending_reports(db, cdc_ids, sub_cdc_ids):
    """Report NEW/REOPENED instradati ai reparti della postazione."""
    if not cdc_ids and not sub_cdc_ids:
        return []
    conds, params = [], []
    if sub_cdc_ids:
        conds.append(f"rt.SubCdcId IN ({','.join(['?'] * len(sub_cdc_ids))})")
        params += list(sub_cdc_ids)
    if cdc_ids:
        conds.append(f"(rt.SubCdcId IS NULL AND rt.CdcId IN ({','.join(['?'] * len(cdc_ids))}))")
        params += list(cdc_ids)
    where_routing = " OR ".join(conds)
    sql = (f"SELECT DISTINCT r.TouchUpReportId, r.Status, r.CreatedAt, r.EscalationLevel, r.ReopenCount "
           f"FROM dbo.TouchUpReports r "
           f"JOIN dbo.TouchUpReportProblems rp ON rp.TouchUpReportId = r.TouchUpReportId "
           f"JOIN dbo.TouchUpProblemRouting rt ON rt.TouchUpProblemId = rp.TouchUpProblemId AND rt.DateOut IS NULL "
           f"WHERE r.Status IN ('NEW','REOPENED') AND ({where_routing}) "
           f"ORDER BY r.EscalationLevel DESC, r.CreatedAt ASC")
    return _query(db, sql, tuple(params))


def list_open_reports(db):
    """Tutte le segnalazioni NEW/REOPENED (per la form 'Soluzioni adottate')."""
    return _query(db,
                  "SELECT TouchUpReportId, Status, CreatedAt, CreatedByUser, EscalationLevel, ReopenCount "
                  "FROM dbo.TouchUpReports WHERE Status IN ('NEW','REOPENED') "
                  "ORDER BY EscalationLevel DESC, CreatedAt ASC")


def get_config(db):
    rows = _query(db, "SELECT NoResponseEscalationMinutes, DayRecurrenceThreshold FROM dbo.TouchUpConfig WHERE Id=1")
    if rows:
        return rows[0]
    return {'NoResponseEscalationMinutes': 30, 'DayRecurrenceThreshold': 3}


def set_config(db, no_response_minutes, day_threshold):
    db._ensure_connection()
    with db._lock:
        db.cursor.execute(
            "UPDATE dbo.TouchUpConfig SET NoResponseEscalationMinutes=?, DayRecurrenceThreshold=? WHERE Id=1",
            (no_response_minutes, day_threshold))
        db.conn.commit()


# ─────────────────────────────────────────────────────────────────────────────
#  Escalation per NO-RISPOSTA entro XX minuti (job background)
#  Claim atomico (UPDATE ... OUTPUT WHERE NoResponseEscalatedAt IS NULL) cosi'
#  fra piu' client solo uno "vince" ogni report -> niente email duplicate.
# ─────────────────────────────────────────────────────────────────────────────
def escalate_unanswered_reports(db):
    """Trova i report NEW/REOPENED piu' vecchi della soglia e senza risposta,
       li marca (claim) e invia email al responsabile. Ritorna la lista di ID."""
    minutes = (get_config(db) or {}).get('NoResponseEscalationMinutes', 30) or 30
    db._ensure_connection()
    with db._lock:
        cur = db.cursor
        cur.execute(
            "UPDATE dbo.TouchUpReports SET NoResponseEscalatedAt = GETDATE(), "
            "    BossEscalated = 1, "
            "    EscalationLevel = CASE WHEN EscalationLevel < 2 THEN 2 ELSE EscalationLevel END "
            "OUTPUT INSERTED.TouchUpReportId "
            "WHERE Status IN ('NEW','REOPENED') AND NoResponseEscalatedAt IS NULL "
            "  AND DATEDIFF(MINUTE, CreatedAt, GETDATE()) >= ?", (minutes,))
        ids = [r[0] for r in cur.fetchall()]
        db.conn.commit()
    for rid in ids:
        try:
            det = get_report_detail(db, rid)
            problem_ids = [p['TouchUpProblemId'] for p in det['problems']]
            _send_noresponse_email(db, rid, problem_ids, det, minutes)
        except Exception as e:
            logger.error(f"Touch-Up: errore email no-risposta #{rid}: {e}", exc_info=True)
    if ids:
        logger.info(f"Touch-Up: escalation no-risposta su report {ids}")
    return ids


def _send_noresponse_email(db, report_id, problem_ids, detail, minutes):
    import utils
    recipients = utils.get_email_recipients(db.conn, WARNING_EMAIL_ATTRIBUTE) or []
    _tech, boss = get_recipients_for_problems(db, problem_ids)
    cc = sorted(boss)
    if not recipients and boss:
        recipients = sorted(boss)
        cc = []
    if not recipients and not cc:
        logger.warning(f"Touch-Up no-risposta #{report_id}: nessun destinatario")
        return False
    probs_html = ", ".join(p['ProblemDescription'] for p in detail['problems'])
    labels_html = "".join(
        f"<tr><td>{l['LabelCod']}</td><td>{l['OrderNumber']}</td><td>{l['ProductCode']}</td></tr>"
        for l in detail['labels'])
    subject = f"[Touch-Up] ESCALATION #{report_id} - nessuna risposta entro {minutes} min"
    body = f"""<html><body style="font-family:'Segoe UI',Arial,sans-serif;font-size:13px;color:#333;">
<div style="background:#7d3c98;color:#fff;padding:14px;border-radius:4px;">
  <h2 style="margin:0;">Touch-Up - ESCALATION (nessuna risposta) #{report_id}</h2>
  <p style="margin:4px 0 0;">Segnalazione aperta da oltre {minutes} minuti senza presa in carico.</p>
</div>
<p><strong>Problemi:</strong> {probs_html}</p>
<table style="border-collapse:collapse;"><tr style="background:#34495e;color:#fff;">
  <th style="padding:6px 10px;">LabelCode</th><th style="padding:6px 10px;">Ordine</th>
  <th style="padding:6px 10px;">Prodotto</th></tr>{labels_html}</table>
<p style="color:#888;font-size:11px;">Email automatica TraceabilityRS - non rispondere.</p>
</body></html>"""
    utils.send_email(recipients, subject, body, is_html=True, cc_emails=cc or None)
    db._ensure_connection()
    with db._lock:
        db.cursor.execute("UPDATE dbo.TouchUpReports SET EmailSentCount = EmailSentCount + 1 "
                          "WHERE TouchUpReportId=?", (report_id,))
        db.conn.commit()
    logger.info(f"Touch-Up: email no-risposta #{report_id} a {recipients} CC {cc}")
    return True
