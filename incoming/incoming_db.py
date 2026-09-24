# File: incoming/incoming_db.py
"""Accesso dati per il modulo Ricezione (incoming).

Tabelle (schema [Traceability_RS].[dyn], vedi incoming/incoming_setup.sql):
  - IncomingRequest     : richieste incoming tra PC
  - IncomingReminderLog : log dei reminder inviati (popup/email)

Settings (traceability_rs.dbo.settings, colonna 'atribute' VARCHAR(30)):
  - Incoming_email_<TIPO>        : destinatari email per tipo richiesta (una riga per email)
  - Incoming_rem_<TIPO>          : reminder/giorno per tipo richiesta
  - Incoming_soluzione_problemi  : destinatari report mensile

Funziona sia con la classe Database di main.py sia con BackgroundDatabase
del servizio background: helper `_cursor` + pattern `with db._lock`.
"""
import logging
from datetime import date, datetime

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Costanti di dominio (contratto condiviso)
# ---------------------------------------------------------------------------
REQUEST_TYPES = {
    'MPN_MANCANTE': 'MPN Mancante',
    'MPN_SBAGLIATO': 'MPN Sbagliato',
    'PO_MANCANTE': 'Mancanza P.O.',
    'PO_QUANTITA': 'P.O. Quantità',
}

STATUS_PENDING = 'PENDING'
STATUS_ANSWERED = 'ANSWERED'
STATUS_CONFIRMED_OK = 'CONFIRMED_OK'
STATUS_CONFIRMED_KO = 'CONFIRMED_KO'

MONTHLY_RECIPIENTS_ATTRIBUTE = 'Incoming_soluzione_problemi'

# Email (una per riga settings) di Ingegneria: destinatari in TO
# dell'email preconfezionata di richiesta soluzione.
ENGINEERING_ATTRIBUTE = 'Incoming_email_ingegneria'

# Email (una per riga settings) degli utenti "master": vedono TUTTI i ticket
# aperti, indipendentemente dai destinatari configurati per tipo.
MASTER_ATTRIBUTE = 'Sys_master_for_tikets'

DEFAULT_REMINDERS_PER_DAY = 2

# Età (minuti) oltre la quale una richiesta PENDING va in escalation, e minuti
# minimi fra due popup di escalation consecutivi per la stessa richiesta.
ESCALATION_AGE_MINUTES = 120
ESCALATION_REPEAT_MINUTES = 30

_TABLE = 'Traceability_RS.dyn.IncomingRequest'
_LOG_TABLE = 'Traceability_RS.dyn.IncomingReminderLog'
_SETTINGS_TABLE = 'traceability_rs.dbo.settings'

# Nomi attributo settings: settings.atribute e' VARCHAR(30), nessuno supera il limite.
def _email_attribute(request_type):
    return 'Incoming_email_%s' % request_type


def _reminders_attribute(request_type):
    return 'Incoming_rem_%s' % request_type


_COLUMNS = [
    'Id', 'RequestNumber', 'RequestType', 'SupplierId', 'SupplierName',
    'DdtNumber', 'DdtDate', 'PurOrderNumber', 'MpnCode', 'WrongMpn',
    'ComponentCode', 'QtyToReceive', 'QtyExpectedPerPo', 'RequestedBy', 'RequestedOn',
    'RequesterHost', 'Status', 'AnswerMpnCode', 'AnswerText',
    'AnsweredBy', 'AnsweredOn', 'ConfirmedOk', 'ConfirmedBy', 'ConfirmedOn',
    'LastEscalationPopup',
]

_COLUMNS_SQL = ', '.join('[%s]' % c for c in _COLUMNS)


# ---------------------------------------------------------------------------
# Accesso DB uniforme
# ---------------------------------------------------------------------------
def _cursor(db):
    if hasattr(db, '_ensure_connection'):
        try:
            db._ensure_connection()
        except Exception:
            pass
    return db.cursor


def _fetch_dicts(cur):
    """Converte il result set corrente in lista di dict con chiavi PascalCase."""
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _row_to_dict(cur, row):
    if row is None:
        return None
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))


def _read_setting_values(db, attribute):
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            "SELECT [VALUE] FROM %s WHERE atribute = ?" % _SETTINGS_TABLE,
            (attribute,))
        return [r[0] for r in cur.fetchall() if r[0]]


def _parse_emails(values):
    """Splitta valori settings multi-email (';' o ',') come in utils.get_email_recipients."""
    emails = []
    for value in values:
        value = str(value)
        if ';' in value:
            chunks = [e.strip() for e in value.split(';')]
        elif ',' in value:
            chunks = [e.strip() for e in value.split(',')]
        else:
            chunks = [value.strip()]
        emails.extend(e for e in chunks if e and '@' in e)
    return emails


# ---------------------------------------------------------------------------
# DDL idempotente (equivalente Python di incoming_setup.sql)
# ---------------------------------------------------------------------------
_DDL_REQUEST = """
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[IncomingRequest]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[IncomingRequest] (
        Id                   INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_IncomingRequest PRIMARY KEY,
        RequestNumber        NVARCHAR(20)  NOT NULL
            CONSTRAINT UQ_dyn_IncomingRequest_Number UNIQUE,
        RequestType          NVARCHAR(30)  NOT NULL,
        SupplierId           INT           NULL,
        SupplierName         NVARCHAR(200) NULL,
        DdtNumber            NVARCHAR(50)  NULL,
        DdtDate              DATE          NULL,
        PurOrderNumber       NVARCHAR(50)  NULL,
        MpnCode              NVARCHAR(100) NULL,
        WrongMpn             NVARCHAR(100) NULL,
        ComponentCode        NVARCHAR(100) NULL,              -- codice interno (dbo.Components, IDCOMPONENTTYPE = 1)
        QtyToReceive         DECIMAL(18,3) NULL,
        QtyExpectedPerPo     DECIMAL(18,3) NULL,
        RequestedBy          NVARCHAR(100) NULL,
        RequestedOn          DATETIME      NOT NULL
            CONSTRAINT DF_dyn_IncomingRequest_RequestedOn DEFAULT (GETDATE()),
        RequesterHost        NVARCHAR(100) NULL,
        Status               NVARCHAR(20)  NOT NULL
            CONSTRAINT DF_dyn_IncomingRequest_Status DEFAULT ('PENDING'),
        AnswerMpnCode        NVARCHAR(100) NULL,
        AnswerText           NVARCHAR(1000) NULL,
        AnsweredBy           NVARCHAR(100) NULL,
        AnsweredOn           DATETIME      NULL,
        ConfirmedOk          BIT           NULL,
        ConfirmedBy          NVARCHAR(100) NULL,
        ConfirmedOn          DATETIME      NULL,
        LastEscalationPopup  DATETIME      NULL
    );
    CREATE NONCLUSTERED INDEX IX_dyn_IncomingRequest_Status
        ON [Traceability_RS].[dyn].[IncomingRequest] (Status, RequestedOn);
    CREATE NONCLUSTERED INDEX IX_dyn_IncomingRequest_RequestedOn
        ON [Traceability_RS].[dyn].[IncomingRequest] (RequestedOn);
END
"""

_DDL_REMINDER_LOG = """
IF NOT EXISTS (
    SELECT 1 FROM sys.tables
    WHERE object_id = OBJECT_ID('[Traceability_RS].[dyn].[IncomingReminderLog]')
)
BEGIN
    CREATE TABLE [Traceability_RS].[dyn].[IncomingReminderLog] (
        Id          INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dyn_IncomingReminderLog PRIMARY KEY,
        RequestId   INT      NOT NULL,
        SentAt      DATETIME NOT NULL
            CONSTRAINT DF_dyn_IncomingReminderLog_SentAt DEFAULT (GETDATE()),
        Channel     NVARCHAR(20) NULL,
        CONSTRAINT FK_dyn_IncomingReminderLog_Request
            FOREIGN KEY (RequestId) REFERENCES [Traceability_RS].[dyn].[IncomingRequest] (Id)
    );
    CREATE NONCLUSTERED INDEX IX_dyn_IncomingReminderLog_Request_SentAt
        ON [Traceability_RS].[dyn].[IncomingReminderLog] (RequestId, SentAt);
END
"""

# ALTER idempotente per installazioni gia' esistenti (tabella creata prima
# dell'introduzione della colonna ComponentCode).
_DDL_ALTER_COMPONENT_CODE = """
IF COL_LENGTH('[Traceability_RS].[dyn].[IncomingRequest]', 'ComponentCode') IS NULL
BEGIN
    ALTER TABLE [Traceability_RS].[dyn].[IncomingRequest]
        ADD ComponentCode NVARCHAR(100) NULL;
END
"""

_SEED_SETTINGS = [
    (_reminders_attribute(t), str(DEFAULT_REMINDERS_PER_DAY)) for t in REQUEST_TYPES
] + [
    # Valore vuoto: nessun master finche' non viene configurato (Setup o SQL).
    (MASTER_ATTRIBUTE, ''),
]


def _exec_ddl(db, sql):
    with db._lock:
        cur = _cursor(db)
        cur.execute(sql)
        db.conn.commit()


def _seed_settings(db):
    with db._lock:
        cur = _cursor(db)
        for attribute, value in _SEED_SETTINGS:
            cur.execute(
                """
                INSERT INTO %s (atribute, [value])
                SELECT ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM %s WHERE atribute = ?
                )
                """ % (_SETTINGS_TABLE, _SETTINGS_TABLE),
                (attribute, value, attribute))
        db.conn.commit()


def create_tables(db):
    """Crea (se mancanti) IncomingRequest + IncomingReminderLog e fa il seed
    dei settings di default (reminder/giorno per tipo richiesta). Idempotente."""
    try:
        _exec_ddl(db, _DDL_REQUEST)
        _exec_ddl(db, _DDL_REMINDER_LOG)
        _exec_ddl(db, _DDL_ALTER_COMPONENT_CODE)
        _seed_settings(db)
        logger.info("incoming: tabelle e seed settings verificati")
    except Exception:
        try:
            db.conn.rollback()
        except Exception:
            pass
        logger.exception("incoming: creazione tabelle/seed fallita")
        raise


# ---------------------------------------------------------------------------
# Creazione / lettura richieste
# ---------------------------------------------------------------------------
def next_request_number(cursor) -> str:
    """'INC-YYYYMMDD-####' con contatore giornaliero.

    Deve essere chiamato DENTRO la transazione di inserimento (stesso lock),
    cosi' la riga committata rende il numero univoco anche fra piu' PC.
    """
    prefix = 'INC-%s-' % date.today().strftime('%Y%m%d')
    cursor.execute(
        "SELECT COUNT(*) FROM %s WHERE RequestNumber LIKE ?" % _TABLE,
        (prefix + '%',))
    count = cursor.fetchone()[0] or 0
    return '%s%04d' % (prefix, count + 1)


def create_request(db, data: dict) -> tuple:
    """Inserisce una nuova richiesta. Ritorna (request_id, request_number).

    data keys: request_type, supplier_id, supplier_name, ddt_number, ddt_date,
    pur_order_number, mpn_code, wrong_mpn, component_code, qty_to_receive,
    qty_expected_per_po, requested_by, requester_host
    """
    with db._lock:
        cur = _cursor(db)
        try:
            request_number = next_request_number(cur)
            cur.execute(
                """
                INSERT INTO %s
                    (RequestNumber, RequestType, SupplierId, SupplierName,
                     DdtNumber, DdtDate, PurOrderNumber, MpnCode, WrongMpn,
                     ComponentCode, QtyToReceive, QtyExpectedPerPo,
                     RequestedBy, RequesterHost, Status)
                OUTPUT INSERTED.Id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """ % _TABLE,
                (request_number,
                 data.get('request_type'),
                 data.get('supplier_id'),
                 data.get('supplier_name'),
                 data.get('ddt_number'),
                 data.get('ddt_date'),
                 data.get('pur_order_number'),
                 data.get('mpn_code'),
                 data.get('wrong_mpn'),
                 data.get('component_code'),
                 data.get('qty_to_receive'),
                 data.get('qty_expected_per_po'),
                 data.get('requested_by'),
                 data.get('requester_host'),
                 STATUS_PENDING))
            row = cur.fetchone()
            request_id = int(row[0]) if row else None
            if request_id is None:
                raise RuntimeError("INSERT IncomingRequest: Id non restituito")
            db.conn.commit()
            logger.info("incoming: creata richiesta %s (id=%s) tipo=%s da %s",
                        request_number, request_id,
                        data.get('request_type'), data.get('requested_by'))
            return request_id, request_number
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: creazione richiesta fallita")
            raise


def get_request(db, request_id) -> dict | None:
    """Riga completa come dict con chiavi PascalCase, o None se non esiste."""
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            "SELECT %s FROM %s WHERE Id = ?" % (_COLUMNS_SQL, _TABLE),
            (request_id,))
        return _row_to_dict(cur, cur.fetchone())


def get_pending_requests(db, request_type=None, allowed_types=None) -> list:
    """Richieste con Status='PENDING', per RequestedOn crescente.

    allowed_types=None -> nessun filtro aggiuntivo (vista master).
    allowed_types=set/list -> solo i tipi indicati; lista vuota -> nessun risultato.
    """
    with db._lock:
        cur = _cursor(db)
        sql = "SELECT %s FROM %s WHERE Status = ?" % (_COLUMNS_SQL, _TABLE)
        params = [STATUS_PENDING]
        if request_type:
            sql += " AND RequestType = ?"
            params.append(request_type)
        if allowed_types is not None:
            if not allowed_types:
                return []
            placeholders = ', '.join('?' * len(allowed_types))
            sql += " AND RequestType IN (%s)" % placeholders
            params.extend(sorted(allowed_types))
        sql += " ORDER BY RequestedOn"
        cur.execute(sql, params)
        return _fetch_dicts(cur)


def get_requests_report(db, filters: dict | None = None) -> list:
    """Report richieste incoming con filtri combinabili (periodo, MPN, stato...).

    filters (tutti opzionali):
      date_from, date_to  -> su CAST(RequestedOn AS DATE), estremi inclusi
      request_type        -> RequestType esatto
      supplier            -> LIKE '%v%' su SupplierName
      mpn_code            -> LIKE '%v%' su MpnCode (codice prodotto richiesto)
      wrong_mpn           -> LIKE '%v%' su WrongMpn
      answer_mpn          -> LIKE '%v%' su AnswerMpnCode
      status              -> 'EVASE' (ANSWERED + CONFIRMED_*), 'NON_EVASE' (PENDING),
                             None/'' per tutte
    """
    filters = filters or {}
    sql = "SELECT %s FROM %s WHERE 1=1" % (_COLUMNS_SQL, _TABLE)
    params = []
    if filters.get('date_from'):
        sql += " AND CAST(RequestedOn AS DATE) >= ?"
        params.append(filters['date_from'])
    if filters.get('date_to'):
        sql += " AND CAST(RequestedOn AS DATE) <= ?"
        params.append(filters['date_to'])
    if filters.get('request_type'):
        sql += " AND RequestType = ?"
        params.append(filters['request_type'])
    if filters.get('supplier'):
        sql += " AND SupplierName LIKE ?"
        params.append('%%%s%%' % filters['supplier'])
    if filters.get('mpn_code'):
        sql += " AND MpnCode LIKE ?"
        params.append('%%%s%%' % filters['mpn_code'])
    if filters.get('wrong_mpn'):
        sql += " AND WrongMpn LIKE ?"
        params.append('%%%s%%' % filters['wrong_mpn'])
    if filters.get('answer_mpn'):
        sql += " AND AnswerMpnCode LIKE ?"
        params.append('%%%s%%' % filters['answer_mpn'])
    status = filters.get('status')
    if status == 'EVASE':
        sql += " AND Status IN (?, ?, ?)"
        params.extend([STATUS_ANSWERED, STATUS_CONFIRMED_OK, STATUS_CONFIRMED_KO])
    elif status == 'NON_EVASE':
        sql += " AND Status = ?"
        params.append(STATUS_PENDING)
    sql += " ORDER BY RequestedOn DESC"
    with db._lock:
        cur = _cursor(db)
        cur.execute(sql, params)
        return _fetch_dicts(cur)


# ---------------------------------------------------------------------------
# Componenti (dbo.Components): codice interno abbinato all'MPN
# ---------------------------------------------------------------------------
def component_exists(db, code) -> bool:
    """True se il codice esiste in Traceability_RS.dbo.Components con
    IDCOMPONENTTYPE = 1 (componenti standard)."""
    code = (code or '').strip().upper()
    if not code:
        return False
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            "SELECT 1 FROM Traceability_RS.dbo.Components "
            "WHERE ComponentCode = ? AND IDCOMPONENTTYPE = 1",
            (code,))
        return cur.fetchone() is not None


def ensure_component(db, code) -> bool:
    """Inserisce il codice in dbo.Components (IDCOMPONENTTYPE = 1) se assente.

    Inserimento silente: nessuna segnalazione all'utente, solo log.
    Ritorna True se il codice esiste (gia' presente o appena inserito)."""
    code = (code or '').strip().upper()
    if not code:
        return False
    if component_exists(db, code):
        return True
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "INSERT INTO Traceability_RS.dbo.Components "
                "(ComponentCode, ComponentDescription, IDCOMPONENTTYPE) "
                "VALUES (?, '', 1)",
                (code,))
            db.conn.commit()
            logger.info("incoming: creato componente '%s' (IDCOMPONENTTYPE=1)", code)
            return True
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: inserimento componente '%s' fallito", code)
            return False


# ---------------------------------------------------------------------------
# Risposta e conferma
# ---------------------------------------------------------------------------
def answer_request(db, request_id, answer_mpn_code, answer_text, answered_by) -> bool:
    """Registra la risposta: Status='ANSWERED', AnsweredOn=GETDATE().
    Ritorna True solo se la richiesta era PENDING."""
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                """
                UPDATE %s
                SET AnswerMpnCode = ?, AnswerText = ?, AnsweredBy = ?,
                    AnsweredOn = GETDATE(), Status = ?
                WHERE Id = ? AND Status = ?
                """ % _TABLE,
                (answer_mpn_code, answer_text, answered_by,
                 STATUS_ANSWERED, request_id, STATUS_PENDING))
            ok = cur.rowcount == 1
            db.conn.commit()
            if ok:
                logger.info("incoming: risposta registrata per richiesta id=%s da %s",
                            request_id, answered_by)
            else:
                logger.warning("incoming: answer_request id=%s ignorato (non PENDING o inesistente)",
                               request_id)
            return ok
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: answer_request id=%s fallita", request_id)
            raise


def confirm_request(db, request_id, ok: bool, confirmed_by) -> bool:
    """Conferma l'esito: Status CONFIRMED_OK/CONFIRMED_KO + ConfirmedOn.
    Ritorna True solo se la richiesta era in uno stato confermabile."""
    status = STATUS_CONFIRMED_OK if ok else STATUS_CONFIRMED_KO
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                """
                UPDATE %s
                SET ConfirmedOk = ?, ConfirmedBy = ?, ConfirmedOn = GETDATE(),
                    Status = ?
                WHERE Id = ? AND Status IN (?, ?)
                """ % _TABLE,
                (1 if ok else 0, confirmed_by, status,
                 request_id, STATUS_PENDING, STATUS_ANSWERED))
            done = cur.rowcount == 1
            db.conn.commit()
            if done:
                logger.info("incoming: richiesta id=%s confermata %s da %s",
                            request_id, status, confirmed_by)
            else:
                logger.warning("incoming: confirm_request id=%s ignorato (stato non confermabile)",
                               request_id)
            return done
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: confirm_request id=%s fallita", request_id)
            raise


# ---------------------------------------------------------------------------
# Configurazione email / reminder (settings)
# ---------------------------------------------------------------------------
def get_email_config(db, request_type) -> dict:
    """{'emails': [str], 'reminders_per_day': int} per il tipo richiesta."""
    emails = _parse_emails(_read_setting_values(db, _email_attribute(request_type)))
    reminder_values = _read_setting_values(db, _reminders_attribute(request_type))
    try:
        reminders_per_day = int(str(reminder_values[0]).strip())
    except (IndexError, ValueError):
        reminders_per_day = DEFAULT_REMINDERS_PER_DAY
    return {'emails': emails, 'reminders_per_day': reminders_per_day}


def save_email_config(db, request_type, emails: list, reminders_per_day: int):
    """Sostituisce destinatari e reminder/giorno per il tipo richiesta."""
    emails = [e.strip() for e in (emails or []) if e and e.strip()]
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "DELETE FROM %s WHERE atribute IN (?, ?)" % _SETTINGS_TABLE,
                (_email_attribute(request_type), _reminders_attribute(request_type)))
            for email in emails:
                cur.execute(
                    "INSERT INTO %s (atribute, [value]) VALUES (?, ?)" % _SETTINGS_TABLE,
                    (_email_attribute(request_type), email))
            cur.execute(
                "INSERT INTO %s (atribute, [value]) VALUES (?, ?)" % _SETTINGS_TABLE,
                (_reminders_attribute(request_type), str(int(reminders_per_day))))
            db.conn.commit()
            logger.info("incoming: config email salvata per %s (%d destinatari, %d reminder/giorno)",
                        request_type, len(emails), int(reminders_per_day))
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: save_email_config %s fallita", request_type)
            raise


def get_monthly_recipients(db) -> list:
    """Destinatari report mensile dal settings atribute='Incoming_soluzione_problemi'."""
    return _parse_emails(_read_setting_values(db, MONTHLY_RECIPIENTS_ATTRIBUTE))


# ---------------------------------------------------------------------------
# Destinatari Ingegneria (settings 'Incoming_email_ingegneria'): vanno in TO
# dell'email preconfezionata di richiesta soluzione.
# ---------------------------------------------------------------------------
def get_engineering_recipients(db) -> list:
    return _parse_emails(_read_setting_values(db, ENGINEERING_ATTRIBUTE))


def save_engineering_recipients(db, emails: list):
    """Sostituisce i destinatari Ingegneria (una riga settings per email)."""
    emails = [e.strip() for e in (emails or []) if e and e.strip()]
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "DELETE FROM %s WHERE atribute = ?" % _SETTINGS_TABLE,
                (ENGINEERING_ATTRIBUTE,))
            for email in emails:
                cur.execute(
                    "INSERT INTO %s (atribute, [value]) VALUES (?, ?)" % _SETTINGS_TABLE,
                    (ENGINEERING_ATTRIBUTE, email))
            db.conn.commit()
            logger.info("incoming: destinatari Ingegneria salvati (%d email)", len(emails))
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: save_engineering_recipients fallita")
            raise


# ---------------------------------------------------------------------------
# Master ticket (settings 'Sys_master_for_tikets')
# ---------------------------------------------------------------------------
def get_master_emails(db) -> list:
    """Email degli utenti master: vedono tutti i ticket aperti."""
    return _parse_emails(_read_setting_values(db, MASTER_ATTRIBUTE))


def save_master_emails(db, emails: list):
    """Sostituisce le email master (una riga settings per email)."""
    emails = [e.strip() for e in (emails or []) if e and e.strip()]
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "DELETE FROM %s WHERE atribute = ?" % _SETTINGS_TABLE,
                (MASTER_ATTRIBUTE,))
            for email in emails:
                cur.execute(
                    "INSERT INTO %s (atribute, [value]) VALUES (?, ?)" % _SETTINGS_TABLE,
                    (MASTER_ATTRIBUTE, email))
            db.conn.commit()
            logger.info("incoming: email master ticket salvate (%d)", len(emails))
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: save_master_emails fallita")
            raise


def is_ticket_master(db, user_email) -> bool:
    """True se l'email dell'utente loggato e' tra quelle master (confronto case-insensitive)."""
    if not user_email:
        return False
    low = str(user_email).strip().lower()
    return any(e.lower() == low for e in get_master_emails(db))


def get_visible_types_for_email(db, user_email) -> set:
    """Tipi di richiesta visibili per l'email: quelli in cui figura tra i destinatari."""
    if not user_email:
        return set()
    low = str(user_email).strip().lower()
    visible = set()
    for rt in REQUEST_TYPES:
        emails = get_email_config(db, rt).get('emails') or []
        if any(e.lower() == low for e in emails):
            visible.add(rt)
    return visible


def resolve_user_email(db, user_name):
    """Email aziendale (WorkEmail) dell'utente loggato, dal nome visualizzato.

    Stessa query di auto_email_settings_gui._resolve_user_email: cerca per
    'Nome Cognome' o 'Cognome Nome' fra i dipendenti attivi (EmployeerId = 2).
    """
    if not user_name:
        return None
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            """
            SELECT TOP 1 ea.WorkEmail
            FROM Employee.dbo.EmployeeHireHistory h
            INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
            LEFT JOIN Employee.dbo.EmployeeAddress ea
                ON ea.EmployeeId = e.EmployeeId AND ea.DateOut IS NULL
            WHERE h.EndWorkDate IS NULL AND h.EmployeerId = 2
              AND (e.EmployeeName + ' ' + e.EmployeeSurname = ?
                   OR e.EmployeeSurname + ' ' + e.EmployeeName = ?)
            """,
            (user_name, user_name))
        row = cur.fetchone()
        if row and row[0]:
            email = str(row[0]).strip()
            if email and '@' in email:
                return email
    return None


# ---------------------------------------------------------------------------
# Fornitori (Sites): inserimento rapido dalla form Ricezione
# ---------------------------------------------------------------------------
def normalize_vat(vat):
    """Normalizza un codice IVA per il confronto: maiuscolo, senza spazi."""
    return ''.join(str(vat or '').split()).upper()


def find_suppliers_by_vat(db, vat):
    """Fornitori con lo stesso codice IVA (normalizzato, con/senza prefisso 'IT').

    Ritorna lista di {'IDSite', 'SiteName'}; vuota se il codice e' libero.
    """
    norm = normalize_vat(vat)
    if not norm:
        return []
    variants = {norm}
    if norm.startswith('IT') and len(norm) > 2:
        variants.add(norm[2:])
    else:
        variants.add('IT' + norm)
    placeholders = ', '.join('?' * len(variants))
    sql = (
        "SELECT IDSite, SiteName FROM Traceability_RS.dbo.Sites "
        "WHERE REPLACE(UPPER(SiteVat), ' ', '') IN (%s)" % placeholders)
    with db._lock:
        cur = _cursor(db)
        cur.execute(sql, tuple(sorted(variants)))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


def supplier_name_suggestions(db, name, limit=5, cutoff=0.6):
    """Nomi fornitore simili a quello proposto (difflib), per evitare duplicati.

    Ritorna lista di {'IDSite', 'SiteName'} ordinata per somiglianza.
    """
    import difflib
    term = (name or '').strip().lower()
    if len(term) < 3:
        return []
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            "SELECT IDSite, SiteName FROM Traceability_RS.dbo.Sites "
            "WHERE IsSupplier = 1 AND SiteName IS NOT NULL AND SiteName <> ''")
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    choices = {str(r['SiteName']).strip().lower(): r for r in rows
               if str(r['SiteName'] or '').strip()}
    matches = difflib.get_close_matches(term, list(choices.keys()), n=limit, cutoff=cutoff)
    return [choices[m] for m in matches]


def create_supplier(db, name, vat):
    """Inserisce un nuovo fornitore in dbo.Sites (stesso pattern di
    Database.add_new_site: IDLastPhase=139, IsSupplier=1).

    Ritorna il nuovo IDSite. Il chiamante deve aver gia' verificato che il
    codice IVA non esista (find_suppliers_by_vat).
    """
    name = (name or '').strip()[:250]
    vat = (vat or '').strip()[:50]
    if not name or not vat:
        raise ValueError("Nome e codice IVA sono obbligatori")
    sql = """
        INSERT INTO Traceability_RS.dbo.Sites
            (SiteName, SiteAddress, SiteVat, SiteCountry, Logo,
             IDLastPhase, IsSupplier, IsTempraryLeasingComp)
        OUTPUT INSERTED.IDSite
        VALUES (?, NULL, ?, NULL, NULL, 139, 1, 0)
    """
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(sql, (name, vat))
            row = cur.fetchone()
            db.conn.commit()
            new_id = int(row[0]) if row else None
            if new_id is None:
                raise RuntimeError("INSERT Sites: IDSite non restituito")
            logger.info("incoming: creato fornitore '%s' (IDSite=%s, VAT=%s)", name, new_id, vat)
            return new_id
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: creazione fornitore '%s' fallita", name)
            raise


def save_monthly_recipients(db, emails: list):
    """Sostituisce i destinatari del report mensile (una riga settings per email)."""
    emails = [e.strip() for e in (emails or []) if e and e.strip()]
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "DELETE FROM %s WHERE atribute = ?" % _SETTINGS_TABLE,
                (MONTHLY_RECIPIENTS_ATTRIBUTE,))
            for email in emails:
                cur.execute(
                    "INSERT INTO %s (atribute, [value]) VALUES (?, ?)" % _SETTINGS_TABLE,
                    (MONTHLY_RECIPIENTS_ATTRIBUTE, email))
            db.conn.commit()
            logger.info("incoming: destinatari report mensile salvati (%d email)",
                        len(emails))
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: save_monthly_recipients fallita")
            raise


# ---------------------------------------------------------------------------
# Escalation
# ---------------------------------------------------------------------------
def get_escalation_candidates(db) -> list:
    """PENDING con eta' >= ESCALATION_AGE_MINUTES e mai escalate o escalate
    almeno ESCALATION_REPEAT_MINUTES fa."""
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            """
            SELECT %s FROM %s
            WHERE Status = ?
              AND DATEDIFF(MINUTE, RequestedOn, GETDATE()) >= %d
              AND (LastEscalationPopup IS NULL
                   OR DATEDIFF(MINUTE, LastEscalationPopup, GETDATE()) >= %d)
            ORDER BY RequestedOn
            """ % (_COLUMNS_SQL, _TABLE,
                   ESCALATION_AGE_MINUTES, ESCALATION_REPEAT_MINUTES),
            (STATUS_PENDING,))
        return _fetch_dicts(cur)


def mark_escalation_sent(db, request_id):
    """Marca l'invio del popup di escalation (UPDATE atomico LastEscalationPopup)."""
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "UPDATE %s SET LastEscalationPopup = GETDATE() WHERE Id = ?" % _TABLE,
                (request_id,))
            db.conn.commit()
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: mark_escalation_sent id=%s fallita", request_id)
            raise


# ---------------------------------------------------------------------------
# Reminder
# ---------------------------------------------------------------------------
def get_pending_for_reminders(db) -> list:
    """Tutte le PENDING con dati minimi per il loop dei reminder."""
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            """
            SELECT Id, RequestNumber, RequestType, RequestedOn, RequesterHost
            FROM %s
            WHERE Status = ?
            ORDER BY RequestedOn
            """ % _TABLE,
            (STATUS_PENDING,))
        return _fetch_dicts(cur)


def count_reminders_today(db, request_id) -> int:
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            """
            SELECT COUNT(*) FROM %s
            WHERE RequestId = ? AND SentAt >= CAST(CAST(GETDATE() AS DATE) AS DATETIME)
            """ % _LOG_TABLE,
            (request_id,))
        return int(cur.fetchone()[0] or 0)


def log_reminder_sent(db, request_id, channel: str = None):
    with db._lock:
        cur = _cursor(db)
        try:
            cur.execute(
                "INSERT INTO %s (RequestId, Channel) VALUES (?, ?)" % _LOG_TABLE,
                (request_id, channel))
            db.conn.commit()
        except Exception:
            try:
                db.conn.rollback()
            except Exception:
                pass
            logger.exception("incoming: log_reminder_sent id=%s fallita", request_id)
            raise


# ---------------------------------------------------------------------------
# Statistiche mensili / YTD
# ---------------------------------------------------------------------------
def _stats_for_range(db, start: datetime, end: datetime) -> dict:
    """Aggregato per tipo su [start, end): by_type con total, answered,
    confirmed_ok, confirmed_ko, avg_response_minutes (float|None)."""
    with db._lock:
        cur = _cursor(db)
        cur.execute(
            """
            SELECT RequestType, RequestedOn, AnsweredOn, ConfirmedOk, Status
            FROM %s
            WHERE RequestedOn >= ? AND RequestedOn < ?
            """ % _TABLE,
            (start, end))
        rows = cur.fetchall()

    by_type = {}
    for request_type, requested_on, answered_on, confirmed_ok, _status in rows:
        bucket = by_type.setdefault(request_type, {
            'total': 0, 'answered': 0, 'confirmed_ok': 0, 'confirmed_ko': 0,
            '_response_minutes': [],
        })
        bucket['total'] += 1
        if answered_on is not None:
            bucket['answered'] += 1
            try:
                delta = (answered_on - requested_on).total_seconds() / 60.0
                bucket['_response_minutes'].append(max(delta, 0.0))
            except (TypeError, AttributeError):
                pass
        if confirmed_ok is True:
            bucket['confirmed_ok'] += 1
        elif confirmed_ok is False:
            bucket['confirmed_ko'] += 1

    for bucket in by_type.values():
        minutes = bucket.pop('_response_minutes')
        bucket['avg_response_minutes'] = (
            float(sum(minutes)) / len(minutes)) if minutes else None
    return {'by_type': by_type}


def get_monthly_stats(db, year: int, month: int) -> dict:
    """{'month': {...by_type...}, 'ytd': {...by_type da gennaio a fine mese...}}."""
    month_start = datetime(year, month, 1)
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    ytd_start = datetime(year, 1, 1)
    return {
        'month': _stats_for_range(db, month_start, next_month),
        'ytd': _stats_for_range(db, ytd_start, next_month),
    }


# ---------------------------------------------------------------------------
# Etichette tipo richiesta tradotte
# ---------------------------------------------------------------------------

def type_label(lang, request_type):
    """Etichetta del tipo richiesta tradotta nella lingua corrente (fallback italiano).
    Accetta sia il language manager sia il suo metodo bound .get."""
    default = REQUEST_TYPES.get(request_type, request_type)
    get = lang if callable(lang) else lang.get
    try:
        return get('incoming_type_' + str(request_type).lower(), default)
    except Exception:
        return default


def type_choices(lang):
    """Lista etichette tradotte, nello stesso ordine di REQUEST_TYPES."""
    return [type_label(lang, k) for k in REQUEST_TYPES]
