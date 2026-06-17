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
from datetime import datetime

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
    conn = get_conn()
    try:
        cur = conn.cursor()
        ctx = _common(cur)
        ready = web_data.production_ready(cur)
        next_rows = web_data.production_next(cur)
        history = web_data.history_rows(cur, days=days, search=search)
    finally:
        conn.close()
    return _render("produzione", page="prod", ready=ready, next_rows=next_rows,
                   history=history, search=search, days=days, **ctx)


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
