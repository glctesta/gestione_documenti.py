# -*- coding: utf-8 -*-
"""
fai_autocheck.py — FAI Autocheck da PlanningMachine

Background worker che:
1. Ogni 30 minuti legge il file Excel più recente in T:\Planning\
2. Analizza tab PlanningMachine per produzioni nelle prossime 4 ore
3. Verifica corrispondenza con template FAI Autocheck=true
4. Se produzione non avviata → email preventiva ai responsabili in turno
5. Registra eventi in FaiAutocheckNotifications per anti-duplicazione
"""

import os
import glob
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger("TraceabilityRS")

# ================================================================
# COSTANTI
# ================================================================

PLANNING_PATH = r"T:\Planning"
PLANNING_TAB = "PlanningMachine"
COL_PHASE = 4          # colonna E (0-based)
COL_ORDER_NUMBER = 10  # colonna K (0-based)
COL_PLANNED_START = 14 # colonna O (0-based)

LOOKAHEAD_HOURS = 4    # finestra di controllo
INTERVAL_MINUTES = 30  # intervallo tra i cicli


# ================================================================
# 1. TEMPLATE AUTOCHECK
# ================================================================

SQL_AUTOCHECK_TEMPLATES = """
    SELECT f.[FaiTemplateId], f.[NrDocument], f.[Revision],
           f.[FaiTitle], p.[PhaseName], p.[IdPhase]
    FROM [Traceability_RS].[fai].[FaiTemplates] f
    INNER JOIN [Traceability_RS].[dbo].[Phases] p
        ON p.[IdPhase] = f.[IdPhase]
    WHERE f.[Autocheck] = 1
"""


def get_autocheck_templates(conn) -> Dict[str, dict]:
    """
    Restituisce dict {PhaseName_upper: template_info}
    per match rapido con il file Excel.
    """
    templates = {}
    with conn.cursor() as cur:
        cur.execute(SQL_AUTOCHECK_TEMPLATES)
        for r in cur.fetchall():
            key = (r.PhaseName or '').strip().upper()
            templates[key] = {
                'FaiTemplateId': r.FaiTemplateId,
                'NrDocument': r.NrDocument,
                'Revision': r.Revision,
                'FaiTitle': r.FaiTitle,
                'PhaseName': r.PhaseName,
                'IdPhase': r.IdPhase
            }
    logger.info(f"FAI Autocheck: {len(templates)} template con Autocheck=1")
    return templates


# ================================================================
# 2. LETTURA FILE EXCEL
# ================================================================

def _find_latest_excel(folder: str) -> Optional[str]:
    """Trova il file Excel più recente nella cartella per data modifica.

    Esclude i file lock di Office (basename che inizia con '~$'): questi
    vengono creati quando un utente apre il file in Excel e causano
    PermissionError se aperti con openpyxl.
    """
    patterns = [os.path.join(folder, '*.xlsx'), os.path.join(folder, '*.xls')]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    # Escludi file lock di Office (~$filename.xlsx)
    files = [f for f in files if not os.path.basename(f).startswith('~$')]

    if not files:
        logger.warning(f"FAI Autocheck: nessun file Excel in {folder}")
        return None

    latest = max(files, key=os.path.getmtime)
    logger.info(f"FAI Autocheck: file selezionato: {os.path.basename(latest)}")
    return latest


def read_planning_excel(lookback_hours: int = 0) -> List[dict]:
    """
    Legge il tab PlanningMachine dal file Excel più recente.
    Filtra righe con PlannedStart tra (now - lookback_hours) e (now + LOOKAHEAD_HOURS).
    Restituisce lista di dict con phase, order_number, planned_start.
    
    Args:
        lookback_hours: ore nel passato da includere (default 0 = solo futuro).
                        Usato dall'enforcement per catturare ordini il cui 
                        PlannedStart è appena passato (es. per L3 escalation).
    """
    filepath = _find_latest_excel(PLANNING_PATH)
    if not filepath:
        return []

    now = datetime.now()
    earliest = now - timedelta(hours=lookback_hours)
    cutoff = now + timedelta(hours=LOOKAHEAD_HOURS)

    rows = []
    try:
        import openpyxl
        wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)

        if PLANNING_TAB not in wb.sheetnames:
            logger.error(
                f"FAI Autocheck: tab '{PLANNING_TAB}' non trovato in {filepath}")
            wb.close()
            return []

        ws = wb[PLANNING_TAB]

        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            # Salta righe troppo corte
            if not row or len(row) <= COL_PLANNED_START:
                continue

            phase_raw = row[COL_PHASE]
            order_raw = row[COL_ORDER_NUMBER]
            start_raw = row[COL_PLANNED_START]

            if not phase_raw or not order_raw or not start_raw:
                continue

            # Parsing data/ora
            planned_start = None
            if isinstance(start_raw, datetime):
                planned_start = start_raw
            elif isinstance(start_raw, str):
                for fmt in ('%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M',
                            '%Y-%m-%d %H:%M', '%m/%d/%Y %H:%M:%S'):
                    try:
                        planned_start = datetime.strptime(start_raw.strip(), fmt)
                        break
                    except ValueError:
                        continue
            if not planned_start:
                continue

            # Filtra per finestra temporale: earliest ≤ PlannedStart ≤ cutoff
            if not (earliest <= planned_start <= cutoff):
                continue

            rows.append({
                'phase': str(phase_raw).strip(),
                'order_number': str(order_raw).strip(),
                'planned_start': planned_start,
                'row_idx': row_idx
            })

        wb.close()

    except PermissionError as e:
        # Il file e' aperto in Excel da un utente (lock): log senza stacktrace
        # e riprova al prossimo ciclo.
        logger.warning(
            f"FAI Autocheck: file Excel temporaneamente in lock "
            f"(aperto da un utente): {os.path.basename(filepath)} — "
            f"riprovo al prossimo ciclo. Dettaglio: {e}"
        )
        return []
    except Exception as e:
        logger.error(f"FAI Autocheck: errore lettura Excel: {e}", exc_info=True)

    logger.info(f"FAI Autocheck: {len(rows)} righe valide in finestra "
                f"[-{lookback_hours}h, +{LOOKAHEAD_HOURS}h]")
    return rows


# ================================================================
# 3. VERIFICA PRODUZIONE AVVIATA
# ================================================================

SQL_CHECK_PRODUCTION = """
    SELECT COUNT(DISTINCT Traceability_RS.dbo.BoardLabels(Scannings.IDBoard)) AS Qty
    FROM Traceability_RS.dbo.Scannings
    INNER JOIN Traceability_RS.dbo.OrderPhases
        ON Scannings.IDOrderPhase = OrderPhases.IDOrderPhase
    INNER JOIN Traceability_RS.dbo.Orders
        ON OrderPhases.IDOrder = Orders.IDOrder
    INNER JOIN Traceability_RS.dbo.Phases
        ON OrderPhases.IDPhase = Phases.IDPhase
    INNER JOIN Traceability_RS.dbo.Boards
        ON Boards.IDBoard = Scannings.IDBoard
    WHERE Scannings.ScanTimeFinish BETWEEN GETDATE() - 500
        AND CAST(CAST(CAST(GETDATE() AS date) AS nvarchar(10))
            + ' 07:30:00' AS smalldatetime)
        AND Orders.OrderNumber = ?
        AND Phases.IdPhase = ?
"""


def check_production_started(conn, order_number: str, id_phase: int) -> int:
    """Verifica se la produzione è già avviata. Ritorna Qty (0 = non avviata)."""
    with conn.cursor() as cur:
        cur.execute(SQL_CHECK_PRODUCTION, (order_number, id_phase))
        row = cur.fetchone()
    return int(row.Qty or 0) if row else 0


# ================================================================
# 4. DESTINATARI EMAIL + VERIFICA PRESENZA
# ================================================================

SQL_RECIPIENTS = """
    SELECT e.EmployeeSurname + ' ' + e.EmployeeName AS Employee,
           a.WorkEmail,
           f.FunctionCode,
           ee.IDEmployee,
           cs.SubCdcDescription
    FROM Employee.dbo.EmployeeHireHistory h
    LEFT JOIN Employee.dbo.Employees e
        ON e.EmployeeId = h.EmployeeId
       AND h.EmployerId = 2
       AND h.EndWorkDate IS NULL
    INNER JOIN Employee.dbo.EmployeeCdcStories ec
        ON h.EmployeeHireHistoryId = ec.EmployeeHireHistoryId
       AND ec.DateOut IS NULL
    INNER JOIN Employee.dbo.Functions f
        ON ec.FunctionId = f.FunctionId
    INNER JOIN Employee.dbo.CdcSub cs
        ON ec.SubCdcId = cs.SubCdcId
    INNER JOIN Employee.dbo.EmployeeAddress a
        ON e.EmployeeId = a.EmployeeId
       AND a.DateOut IS NULL
    INNER JOIN Timeclocking.dbo.Employee ee
        ON ee.UniqueID COLLATE database_default = e.EmployeeNID
       AND ee.DataStop IS NULL
    WHERE cs.SubCdcDescription = 'pthm'
      AND f.FunctionCode BETWEEN 21 AND 80
    ORDER BY f.FunctionCode
"""


def _check_presence(conn, id_employee: int) -> bool:
    """
    Verifica presenza in turno via SP GetEmployeesTimeclockReal.
    - Prima delle 15:30 → @from = oggi 06:40
    - Dopo le 15:30 → @from = oggi 16:20
    - @to = GETDATE()
    """
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')

    if now.hour < 15 or (now.hour == 15 and now.minute < 30):
        from_dt = f"{today_str} 06:40:00"
    else:
        from_dt = f"{today_str} 16:20:00"

    to_dt = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with conn.cursor() as cur:
            cur.execute(
                "EXEC [Timeclocking].[dbo].[GetEmployeesTimeclockReal] ?, ?, ?",
                (from_dt, to_dt, id_employee))
            result = cur.fetchone()
        return result is not None
    except Exception as e:
        logger.warning(f"FAI Autocheck: errore verifica presenza ID {id_employee}: {e}")
        return False


def get_recipients_with_presence(conn) -> Tuple[List[str], List[str]]:
    """
    Restituisce (to_list, cc_list) di email.
    - FunctionCode < 60 e presente in turno → TO
    - FunctionCode >= 60 → sempre in CC
    """
    to_list = []
    cc_list = []

    with conn.cursor() as cur:
        cur.execute(SQL_RECIPIENTS)
        rows = cur.fetchall()

    for r in rows:
        email = (r.WorkEmail or '').strip()
        if not email or '@' not in email:
            continue

        fc = r.FunctionCode or 0
        if fc >= 60:
            cc_list.append(email)
        else:
            # Verifica presenza
            if _check_presence(conn, r.IDEmployee):
                to_list.append(email)
            else:
                logger.debug(
                    f"FAI Autocheck: {r.Employee} non in turno, escluso da TO")

    # Deduplica
    to_list = list(dict.fromkeys(to_list))
    cc_list = list(dict.fromkeys(cc_list))

    logger.info(f"FAI Autocheck: destinatari TO={len(to_list)}, CC={len(cc_list)}")
    return to_list, cc_list


# ================================================================
# 5. ANTI-DUPLICAZIONE
# ================================================================

SQL_CHECK_ALREADY_SENT = """
    SELECT 1
    FROM [Traceability_RS].[fai].[FaiAutocheckNotifications]
    WHERE OrderNumber = ?
      AND IdPhase = ?
      AND FaiTemplateId = ?
      AND PlannedStart = ?
      AND NotificationStatus IN ('SENT', 'SKIPPED_ALREADY_STARTED')
"""


def check_already_notified(conn, order_number: str, id_phase: int,
                           template_id: int, planned_start: datetime) -> bool:
    """Verifica se esiste già una notifica per questa combinazione."""
    with conn.cursor() as cur:
        cur.execute(SQL_CHECK_ALREADY_SENT,
                    (order_number, id_phase, template_id, planned_start))
        return cur.fetchone() is not None


# ================================================================
# 6. REGISTRAZIONE TRACKING
# ================================================================

SQL_INSERT_NOTIFICATION = """
    INSERT INTO [Traceability_RS].[fai].[FaiAutocheckNotifications]
        (OrderNumber, IdPhase, PhaseName, FaiTemplateId, FaiTitle,
         NrDocument, Revision, PlannedStart, DetectionTime,
         EmailSentTime, EmailTo, EmailCc, ProductionQtyAtCheck,
         PresenceChecked, NotificationStatus)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, 1, ?)
"""


def record_notification(conn, data: dict):
    """Registra l'evento nella tabella tracking.

    Rollback difensivo se l'INSERT fallisce: evita che una transazione
    residua tenga lock esclusivi sulla tabella FaiAutocheckNotifications.
    Con autocommit=True il rollback e' un no-op ma serve da rete di sicurezza
    qualora la connessione venga aperta con autocommit=False.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_INSERT_NOTIFICATION, (
                data['order_number'],
                data['id_phase'],
                data['phase_name'],
                data['template_id'],
                data.get('fai_title'),
                data.get('nr_document'),
                data.get('revision'),
                data['planned_start'],
                data.get('email_sent_time'),      # NULL se non inviata
                data.get('email_to', ''),
                data.get('email_cc', ''),
                data.get('production_qty', 0),
                data['status']
            ))
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise


# ================================================================
# 7. INVIO EMAIL
# ================================================================

def send_fai_autocheck_email(to_emails: List[str], cc_emails: List[str],
                             order_data: dict, template_data: dict,
                             logo_path: str = "Logo.png"):
    """Compone e invia email professionale per FAI autocheck."""
    from email_connector import EmailSender

    order_number = order_data['order_number']
    phase_name = template_data['PhaseName']
    planned_start = order_data['planned_start']
    fai_title = template_data.get('FaiTitle', 'N/A')
    nr_doc = template_data.get('NrDocument', 'N/A')
    revision = template_data.get('Revision', 'N/A')

    planned_str = planned_start.strftime('%d/%m/%Y %H:%M')

    subject = (f"Azione richiesta — Esecuzione controllo FAI prima "
               f"dell'avvio produzione ordine {order_number}")

    html_body = f"""
    <html>
    <body style="font-family:'Segoe UI',Arial,sans-serif; color:#333; margin:0; padding:0;">
    <div style="max-width:700px; margin:0 auto; padding:20px;">

        <!-- Header -->
        <div style="border-bottom:3px solid #B71C1C; padding-bottom:15px; margin-bottom:20px;">
            <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td style="font-size:20px; font-weight:bold; color:#B71C1C;">
                    ⚠️ CONTROLLO FAI RICHIESTO
                </td>
                <td style="text-align:right;">
                    <img src="cid:company_logo" alt="Vandewiele"
                         style="width:120px; height:auto;" />
                </td>
            </tr>
            </table>
        </div>

        <p style="font-size:14px;">Gentili Responsabili di Linea,</p>

        <p style="font-size:14px;">
            si comunica che per l'ordine <strong>{order_number}</strong>,
            fase <strong>{phase_name}</strong>, è previsto a breve l'avvio
            della produzione secondo pianificazione.
        </p>

        <p style="font-size:14px;">
            Dalle verifiche automatiche effettuate, il controllo FAI associato
            al template obbligatorio con gestione Autocheck
            <strong>non risulta ancora eseguito</strong>.
        </p>

        <p style="font-size:14px; font-weight:bold; color:#B71C1C;">
            Si richiede pertanto di provvedere con la massima urgenza
            all'esecuzione e registrazione del controllo FAI prima
            dell'inizio della produzione.
        </p>

        <!-- Dettagli -->
        <table style="border-collapse:collapse; width:100%; margin:20px 0;
                       background-color:#fff3cd; border:1px solid #ffc107;">
            <tr>
                <td style="padding:10px 14px; font-weight:bold; width:250px;
                           border-bottom:1px solid #ffeaa7;">
                    📅 Orario pianificato avvio fase
                </td>
                <td style="padding:10px 14px; border-bottom:1px solid #ffeaa7;
                           font-size:16px; font-weight:bold; color:#B71C1C;">
                    {planned_str}
                </td>
            </tr>
            <tr>
                <td style="padding:10px 14px; font-weight:bold;
                           border-bottom:1px solid #ffeaa7;">
                    📋 Template FAI applicabile
                </td>
                <td style="padding:10px 14px;
                           border-bottom:1px solid #ffeaa7;">{fai_title}</td>
            </tr>
            <tr>
                <td style="padding:10px 14px; font-weight:bold;">
                    📄 Documento / Revisione
                </td>
                <td style="padding:10px 14px;">{nr_doc} / {revision}</td>
            </tr>
        </table>

        <div style="background-color:#f8d7da; border-left:4px solid #B71C1C;
                    padding:12px 16px; margin:20px 0; border-radius:4px;">
            <p style="margin:0; font-size:13px; color:#721c24;">
                La presente comunicazione costituisce avviso operativo preventivo.
                L'eventuale mancata esecuzione del controllo sarà registrata
                ai fini di verifica del rispetto della procedura.
            </p>
        </div>

        <!-- Footer -->
        <div style="margin-top:30px; padding-top:15px; border-top:1px solid #dee2e6;">
            <p style="font-size:12px; color:#666;">
                Cordiali saluti,<br/>
                <strong>Sistema automatico di controllo FAI</strong>
            </p>
            <p style="font-size:10px; color:#aaa;">
                Questo messaggio è stato generato automaticamente dal sistema
                TraceabilityRS. Non rispondere a questa email.
            </p>
        </div>
    </div>
    </body>
    </html>
    """

    sender = EmailSender()
    sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")

    attachments = []
    full_logo = os.path.join(os.path.dirname(__file__), logo_path)
    if os.path.exists(full_logo):
        attachments.append(('inline', full_logo, 'company_logo'))

    sender.send_email(
        to_email=', '.join(to_emails),
        subject=subject,
        body=html_body,
        is_html=True,
        attachments=attachments if attachments else None,
        cc_emails=cc_emails if cc_emails else None
    )

    logger.info(f"FAI Autocheck email inviata per ordine {order_number} "
                f"fase {phase_name} a {len(to_emails)} dest. TO, "
                f"{len(cc_emails)} CC")


# ================================================================
# 8. CICLO PRINCIPALE
# ================================================================

def run_autocheck_cycle(conn, logo_path: str = "Logo.png") -> int:
    """
    Esegue un ciclo completo di autocheck.
    Restituisce il numero di email inviate.
    """
    sent_count = 0

    # 1. Carica template autocheck
    templates = get_autocheck_templates(conn)
    if not templates:
        logger.info("FAI Autocheck: nessun template con Autocheck=1")
        return 0

    # 2. Leggi file Excel
    planning_rows = read_planning_excel()
    if not planning_rows:
        logger.info("FAI Autocheck: nessuna riga valida nel planning")
        return 0

    # 3. Per ogni riga valida
    # Cache destinatari (calcolati una volta sola per ciclo)
    recipients_cache = None

    for pr in planning_rows:
        phase_upper = pr['phase'].upper()

        # 3a. Match fase ← autocheck template
        template = templates.get(phase_upper)
        if not template:
            continue  # fase non soggetta ad autocheck

        order_number = pr['order_number']
        id_phase = template['IdPhase']
        template_id = template['FaiTemplateId']
        planned_start = pr['planned_start']

        # 3b. Verifica anti-duplicazione
        try:
            if check_already_notified(conn, order_number, id_phase,
                                      template_id, planned_start):
                logger.debug(
                    f"FAI Autocheck: skip duplicato {order_number}/{phase_upper}")
                continue
        except Exception as e:
            logger.warning(f"FAI Autocheck: errore anti-dup check: {e}")

        # 3c. Verifica produzione avviata
        try:
            qty = check_production_started(conn, order_number, id_phase)
        except Exception as e:
            logger.error(
                f"FAI Autocheck: errore verifica produzione: {e}", exc_info=True)
            qty = 0

        if qty > 0:
            # Produzione già avviata → registra e skip
            try:
                record_notification(conn, {
                    'order_number': order_number,
                    'id_phase': id_phase,
                    'phase_name': template['PhaseName'],
                    'template_id': template_id,
                    'fai_title': template.get('FaiTitle'),
                    'nr_document': template.get('NrDocument'),
                    'revision': template.get('Revision'),
                    'planned_start': planned_start,
                    'email_sent_time': None,
                    'email_to': '',
                    'email_cc': '',
                    'production_qty': qty,
                    'status': 'SKIPPED_ALREADY_STARTED'
                })
            except Exception as e:
                logger.warning(
                    f"FAI Autocheck: errore registrazione skip: {e}")
            continue

        # 3d. Recupera destinatari (con cache)
        if recipients_cache is None:
            try:
                recipients_cache = get_recipients_with_presence(conn)
            except Exception as e:
                logger.error(
                    f"FAI Autocheck: errore recupero destinatari: {e}",
                    exc_info=True)
                recipients_cache = ([], [])

        to_list, cc_list = recipients_cache

        if not to_list:
            # Nessun destinatario in turno
            try:
                record_notification(conn, {
                    'order_number': order_number,
                    'id_phase': id_phase,
                    'phase_name': template['PhaseName'],
                    'template_id': template_id,
                    'fai_title': template.get('FaiTitle'),
                    'nr_document': template.get('NrDocument'),
                    'revision': template.get('Revision'),
                    'planned_start': planned_start,
                    'email_sent_time': None,
                    'email_to': '',
                    'email_cc': '; '.join(cc_list),
                    'production_qty': 0,
                    'status': 'SKIPPED_NO_RECIPIENT'
                })
            except Exception as e:
                logger.warning(
                    f"FAI Autocheck: errore registrazione no-recipient: {e}")
            logger.warning(
                f"FAI Autocheck: nessun responsabile in turno per "
                f"{order_number}/{phase_upper}")
            continue

        # 3e. Invia email
        try:
            send_fai_autocheck_email(
                to_list, cc_list, pr, template, logo_path)
            email_time = datetime.now()
            sent_count += 1
        except Exception as e:
            logger.error(
                f"FAI Autocheck: errore invio email per "
                f"{order_number}/{phase_upper}: {e}", exc_info=True)
            email_time = None

        # 3f. Registra evento
        try:
            record_notification(conn, {
                'order_number': order_number,
                'id_phase': id_phase,
                'phase_name': template['PhaseName'],
                'template_id': template_id,
                'fai_title': template.get('FaiTitle'),
                'nr_document': template.get('NrDocument'),
                'revision': template.get('Revision'),
                'planned_start': planned_start,
                'email_sent_time': email_time,
                'email_to': '; '.join(to_list),
                'email_cc': '; '.join(cc_list),
                'production_qty': 0,
                'status': 'SENT' if email_time else 'PENDING'
            })
        except Exception as e:
            logger.error(
                f"FAI Autocheck: errore registrazione notifica: {e}",
                exc_info=True)

    logger.info(f"FAI Autocheck: ciclo completato, {sent_count} email inviate")
    return sent_count
