# -*- coding: utf-8 -*-
"""
kit_web_server.py — Web server intranet della Kit Dashboard (Flask).

Serve due pagine (Depozit / Producție) + drill-down ordine, leggendo lo
SNAPSHOT scritto ogni 5 min dal sync. Endpoint /refresh forza un ricalcolo
immediato (D5). Endpoint /health per il watcher.

Avvio manuale (installazione sul PC 192.168.10.72):
    .venv\\Scripts\\python.exe kit_web_server.py

Configurazione: kit_server_config.json (dir dell'eseguibile).
Spec: docs/KitDashboard_WebServer_Spec_v1.0.md
"""
import sys, io, os, logging, socket, threading, time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

import pyodbc
from flask import Flask, request, redirect, jsonify, abort
from jinja2 import Environment, DictLoader

from config_manager import ConfigManager
from kit_dashboard import server_config, web_data
from kit_dashboard.web_templates import TEMPLATES, STATUS_LABELS
from kit_dashboard.sync_service import KitDashboardSync

logger = logging.getLogger("KitDashboard")

CFG = server_config.load_config()

# ── Jinja env + filtri ──────────────────────────────────────────────────
_env = Environment(loader=DictLoader(TEMPLATES), autoescape=True)


def _f_qty(v):
    if v is None:
        return "—"
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else f"{f:g}"
    except Exception:
        return str(v)


def _f_hm(v):
    return v.strftime("%H:%M") if isinstance(v, datetime) else "—"


def _f_dt(v):
    return v.strftime("%d/%m %H:%M") if isinstance(v, datetime) else "—"


def _f_status(v):
    return STATUS_LABELS.get(v, v or "—")


def _f_yesno(v):
    if v is None:
        return "—"
    return '<span class="ico yes">✔</span>' if v else '<span class="ico no">✗</span>'


_env.filters.update(qty=_f_qty, hm=_f_hm, dt=_f_dt, status=_f_status, yesno=_f_yesno)

# autoescape disattivato solo per yesno (HTML): usiamo Markup
from markupsafe import Markup
_env.filters['yesno'] = lambda v: Markup(_f_yesno(v))

app = Flask(__name__)


# ── DB helpers ──────────────────────────────────────────────────────────
def _conn_str():
    c = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
    return (f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
            f"UID={c['username']};PWD={c['password']};MARS_Connection=Yes;TrustServerCertificate=Yes")


def get_conn():
    return pyodbc.connect(_conn_str(), autocommit=True)


def _authenticate_and_authorize(cur, user_id: str, password: str, key: str):
    """Replica la logica di main.py authenticate_and_authorize per il web server."""
    cur.execute("""
        SELECT u.NomeUser,
               ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') AS EmployeeName,
               h.EmployeeHireHistoryId AS AuthorizedEmployeeHireHistoryId,
               a.AuthorizedUsedId
        FROM resetservices.dbo.tbuserkey AS U
        INNER JOIN employee.dbo.employees AS e ON e.EmployeeId = u.idanga
        INNER JOIN employee.dbo.EmployeeHireHistory AS h ON e.EmployeeId = h.EmployeeId
        LEFT JOIN dbo.AutorizedUsers AS a
               ON a.Employeehirehistoryid = h.EmployeeHireHistoryId
              AND a.TranslationKey = ?
        WHERE h.EndWorkDate IS NULL
          AND h.employeerid = 2
          AND u.Nomeuser = ?
          AND u.Pass = ?
          AND a.DateOut IS NULL
    """, (key, user_id, password))
    return cur.fetchone()


# ── Sync autonomo + heartbeat (server indipendente dall'app) ────────────
_sync_lock = threading.Lock()


def _server_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return CFG.get("server_host_ip", "")


def _write_heartbeat(conn):
    """Il web server registra in DB di essere vivo (visibile a tutti)."""
    try:
        conn.cursor().execute("""
            UPDATE Traceability_RS.dbo.kit_dashboard_controller
            SET controller_host = ?, controller_ip = ?, heartbeat_date = GETDATE(),
                server_state = 'RUNNING', server_pid = ?, last_check_date = GETDATE()
            WHERE lock_name = 'KIT_DASHBOARD'
        """, (socket.gethostname(), _server_ip(), os.getpid()))
        conn.commit()
    except Exception as e:
        logger.warning("Heartbeat fallito: %s", e)


def sync_now():
    """Esegue il sync (con lock per evitare sovrapposizioni) + heartbeat."""
    if not _sync_lock.acquire(blocking=False):
        logger.info("Sync già in corso: salto")
        return False
    conn = None
    try:
        conn = get_conn()
        KitDashboardSync(CFG).run_once(conn)
        _write_heartbeat(conn)
        return True
    except Exception as e:
        logger.error("Sync autonomo fallito: %s", e, exc_info=True)
        return False
    finally:
        if conn:
            conn.close()
        _sync_lock.release()


def _sync_loop():
    interval = int(CFG.get("sync_interval_minutes", 5)) * 60
    sync_now()  # primo sync immediato all'avvio
    while True:
        time.sleep(interval)
        sync_now()


def _common(cur):
    sd = web_data.snapshot_date(cur)
    return {
        'snapshot_time': sd.strftime("%d/%m %H:%M") if sd else None,
        'request_path': request.path,
    }


def _render(name, **ctx):
    return _env.get_template(name).render(**ctx)


# ── Route ───────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return redirect("/produzione")


@app.route("/magazzino")
def magazzino():
    conn = get_conn()
    try:
        cur = conn.cursor()
        ctx = _common(cur)
        rows = web_data.warehouse_rows(cur)
    finally:
        conn.close()
    return _render("magazzino", page="mag", rows=rows, **ctx)


@app.route("/produzione")
def produzione():
    search = (request.args.get("q") or "").strip()
    days = int(CFG.get("history_default_days", 3))
    error = request.args.get("error")
    saved = request.args.get("saved")
    conn = get_conn()
    try:
        cur = conn.cursor()
        ctx = _common(cur)
        ready = web_data.production_ready(cur)
        next_rows = web_data.production_next(cur)
        received = web_data.production_received(cur)
        history = web_data.history_rows(cur, days=days, search=search)
    finally:
        conn.close()
    return _render("produzione", page="prod", ready=ready, next_rows=next_rows,
                   received=received, history=history, search=search, days=days,
                   error=error, saved=saved, **ctx)


@app.route("/posticipi")
def posticipi():
    """Pagina con l'elenco degli ordini attualmente posticipati."""
    error = request.args.get("error")
    saved = request.args.get("saved")
    conn = get_conn()
    try:
        cur = conn.cursor()
        ctx = _common(cur)
        rows = web_data.postponed_orders(cur)
    finally:
        conn.close()
    return _render("posticipi", page="prod", rows=rows, error=error, saved=saved, **ctx)


@app.route("/gestione_posticipi", methods=["POST"])
def gestione_posticipi():
    """Riattiva o modifica i giorni di posticipo per gli ordini selezionati."""
    orders_raw = (request.form.get("orders") or "").strip()
    orders = [o.strip() for o in orders_raw.split(",") if o.strip()]
    azione = (request.form.get("azione") or "").strip()
    days = request.form.get("days", type=int)
    user_id = (request.form.get("user_id") or "").strip()
    password = (request.form.get("password") or "").strip()

    if not orders or azione not in ('riattiva', 'modifica') or not user_id or not password:
        return redirect("/posticipi?error=missing")
    if azione == 'modifica' and (not days or days < 1):
        return redirect("/posticipi?error=missing")

    conn = get_conn()
    try:
        cur = conn.cursor()
        auth = _authenticate_and_authorize(cur, user_id, password, 'posponi_produzione')
        if not auth or auth.AuthorizedUsedId is None:
            return redirect("/posticipi?error=auth")

        placeholders = ','.join('?' * len(orders))
        if azione == 'riattiva':
            cur.execute(f"""
                UPDATE Traceability_RS.dbo.kit_order_postponements
                SET expires_at = DATEADD(SECOND, -1, GETDATE())
                WHERE order_number IN ({placeholders})
                  AND expires_at > GETDATE()
            """, orders)
        else:
            cur.execute(f"""
                UPDATE Traceability_RS.dbo.kit_order_postponements
                SET days = ?,
                    expires_at = DATEADD(DAY, ?, postponed_at)
                WHERE order_number IN ({placeholders})
                  AND expires_at > GETDATE()
            """, (days, days) + tuple(orders))
        conn.commit()
        affected = cur.rowcount
    finally:
        conn.close()

    sync_now()
    return redirect(f"/posticipi?saved={affected}")


@app.route("/ordine/<order_number>")
def ordine(order_number):
    conn = get_conn()
    try:
        cur = conn.cursor()
        ctx = _common(cur)
        d = web_data.order_detail(cur, order_number)
    finally:
        conn.close()
    return _render("ordine", page="prod", order_number=order_number, d=d, **ctx)


@app.route("/posponi", methods=["POST"])
def posponi():
    """Registra un posticipo per gli ordini selezionati dopo login autorizzato."""
    orders_raw = (request.form.get("orders") or "").strip()
    orders = [o.strip() for o in orders_raw.split(",") if o.strip()]
    reason_code = (request.form.get("reason_code") or "").strip()
    reason_text = (request.form.get("reason_text") or "").strip()
    days = request.form.get("days", type=int)
    user_id = (request.form.get("user_id") or "").strip()
    password = (request.form.get("password") or "").strip()

    if not orders or not reason_code or not reason_text or not days or days < 1 or not user_id or not password:
        return redirect("/produzione?error=missing")

    reason_labels = {
        'MISSING_COMPONENTS': 'Lipsă componente',
        'DOCUMENTATION_PROBLEMS': 'Probleme documentație',
        'TECHNICAL_PROBLEMS': 'Probleme tehnice',
        'OTHER_URGENT': 'Amânat pentru alte urgențe',
    }
    if reason_code not in reason_labels:
        return redirect("/produzione?error=reason")

    conn = get_conn()
    try:
        cur = conn.cursor()
        auth = _authenticate_and_authorize(cur, user_id, password, 'posponi_produzione')
        if not auth or auth.AuthorizedUsedId is None:
            return redirect("/produzione?error=auth")

        user_name = auth.EmployeeName or user_id
        expires = datetime.now() + timedelta(days=days)

        for order in orders:
            cur.execute("SELECT IDOrder FROM Traceability_RS.dbo.Orders WHERE OrderNumber = ?", (order,))
            row = cur.fetchone()
            idorder = row[0] if row else None
            cur.execute("""
                INSERT INTO Traceability_RS.dbo.kit_order_postponements
                    (order_number, idorder, reason_code, reason_label, reason_text,
                     days, postponed_by, postponed_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
            """, (order, idorder, reason_code, reason_labels[reason_code],
                  reason_text, days, user_name, expires))
        conn.commit()
    finally:
        conn.close()

    sync_now()
    return redirect(f"/produzione?saved={len(orders)}")


@app.route("/refresh", methods=["POST"])
def refresh():
    nxt = request.form.get("next") or "/produzione"
    sync_now()
    return redirect(nxt)


@app.route("/health")
def health():
    try:
        conn = get_conn()
        try:
            cur = conn.cursor()
            sd = web_data.snapshot_date(cur)
        finally:
            conn.close()
        return jsonify(status="ok",
                       snapshot_date=sd.isoformat() if sd else None,
                       server_time=datetime.now().isoformat())
    except Exception as e:
        return jsonify(status="error", error=str(e)), 500


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    port = int(CFG.get("server_port", 8090))
    # Thread di sincronizzazione autonomo (server indipendente dall'app desktop)
    threading.Thread(target=_sync_loop, name="KitDashboardSyncLoop", daemon=True).start()
    logger.info("Kit Dashboard web server in avvio su :%d (sync ogni %s min)",
                port, CFG.get("sync_interval_minutes", 5))
    app.run(host="0.0.0.0", port=port, threaded=True)


if __name__ == "__main__":
    main()
