# -*- coding: utf-8 -*-
"""
display_server.py — Server display di reparto per il kanban WIP/REPAIR (porta 6505).

Alimenta i monitor di reparto: dashboard idle (statistiche, ultima operazione)
e modalità evidenziata 3D quando la pagina Preleva (:6500) segnala una scheda
da prelevare (POST /api/highlight, fire-and-forget).

Avvio manuale:  python wip_kanban/display_server.py
Su server:      task scheduler con services/run_display_server.bat (pythonw).

Nessuna autenticazione: rete interna, come il report kanban.
Gli highlight sono in memoria (dict area+deposit -> dati+timestamp) e scadono
dopo HIGHLIGHT_TTL_SEC senza rinnovi.
"""
import sys
import os
import io
import time
import logging

# La root del progetto deve essere importabile (config_manager, database_config...)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

from datetime import timedelta
from threading import Lock

from flask import Flask, jsonify, request, render_template

from wip_kanban import db, i18n, kanban_logic

logger = logging.getLogger("WipKanban")

PORT = 6505
HIGHLIGHT_TTL_SEC = 60


def _setup_file_logging():
    """Aggiunge un handler su file (logs/display_server.log nella root del
    progetto) cosi' gli errori di avvio restano visibili anche con pythonw."""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(project_root, "logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(
            os.path.join(log_dir, "display_server.log"), encoding="utf-8"
        )
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
        logger.addHandler(fh)
        logging.getLogger().addHandler(fh)
    except Exception as e:
        logger.warning("Log su file non disponibile: %s", e)

# Highlight attivi in memoria: {(area, deposit): {position, labelcode,
# order_number, product_code, ts}} — ts = epoch del POST.
_highlights = {}
_highlights_lock = Lock()


def create_app():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )
    app.secret_key = os.urandom(32)
    app.permanent_session_lifetime = timedelta(minutes=480)

    @app.before_request
    def log_request():
        logger.info("Display %s %s from %s", request.method, request.path, request.remote_addr)

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Errore non gestito display: %s", e)
        if request.path.startswith("/api/"):
            return jsonify({"error": "internal_error", "message": str(e)}), 500
        return e

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "wip_kanban_display"})

    @app.route("/display")
    def page_display():
        area = (request.args.get("area") or "WIP").upper().strip()
        if area not in kanban_logic.AREA_LETTERS:
            area = "WIP"
        try:
            deposit = int(request.args.get("deposit") or 1)
        except ValueError:
            deposit = 1
        lang = request.args.get("lang") or "ro"
        ui = i18n.get_ui(lang)
        return render_template("kanban_display.html", ui=ui, lang=lang,
                               area=area, deposit=deposit)

    @app.route("/api/state")
    def api_state():
        area = (request.args.get("area") or "WIP").upper().strip()
        if area not in kanban_logic.AREA_LETTERS:
            return jsonify({"error": "invalid_area"}), 400
        try:
            deposit = int(request.args.get("deposit") or 1)
        except ValueError:
            deposit = 1

        highlight = _active_highlight(area, deposit)
        conn = db.get_conn()
        try:
            conn.timeout = 60
            cur = conn.cursor()
            state = kanban_logic.display_state(cur, area, deposit=deposit)
        finally:
            conn.close()
        state["highlight"] = highlight
        return jsonify(state)

    @app.route("/api/highlight", methods=["POST"])
    def api_highlight():
        body = request.get_json(silent=True) or {}
        area = (body.get("area") or "").upper().strip()
        if area not in kanban_logic.AREA_LETTERS:
            # Prima lettera del PositionCode come fallback (W/R)
            pos = (body.get("position") or "").upper().strip()
            area = kanban_logic.LETTER_AREAS.get(pos[:1], "")
        if area not in kanban_logic.AREA_LETTERS:
            return jsonify({"ok": False, "error": "invalid_area"}), 400
        try:
            deposit = int(body.get("deposit") or 1)
        except (TypeError, ValueError):
            deposit = 1
        with _highlights_lock:
            _highlights[(area, deposit)] = {
                "position": (body.get("position") or "").upper().strip(),
                "labelcode": body.get("labelcode") or "",
                "order_number": body.get("order_number") or "",
                "product_code": body.get("product_code") or "",
                "ts": time.time(),
            }
        logger.info("Highlight %s deposit=%s pos=%s", area, deposit,
                    body.get("position"))
        return jsonify({"ok": True})

    return app


def _active_highlight(area, deposit):
    """Highlight attivo per area+deposit se esiste e ha età < HIGHLIGHT_TTL_SEC."""
    with _highlights_lock:
        h = _highlights.get((area, deposit))
        if not h:
            return None
        age = time.time() - h["ts"]
        if age >= HIGHLIGHT_TTL_SEC:
            del _highlights[(area, deposit)]
            return None
        return {
            "position": h["position"],
            "labelcode": h["labelcode"],
            "order_number": h["order_number"],
            "product_code": h["product_code"],
            "age_sec": round(age, 1),
        }


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    _setup_file_logging()
    try:
        app = create_app()
        logger.info("Avvio display kanban su 0.0.0.0:%s", PORT)
        app.run(host="0.0.0.0", port=PORT, threaded=True)
    except Exception:
        logger.exception("AVVIO FALLITO: display kanban su porta %s", PORT)
        raise


if __name__ == "__main__":
    main()
