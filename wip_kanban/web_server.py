# -*- coding: utf-8 -*-
"""
web_server.py — Web server Kanban produzione (porta 6500).

Avvio manuale:  python wip_kanban/web_server.py
Su server:     task scheduler con pythonw.exe (stesso pattern del server
               etichette :5015, vedi docs/PrintLabelForProduction_Spec_v2.0.md §13).

Configurazione: kanban_server_config.json (nella directory dell'eseguibile).
"""
import sys
import io
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

from datetime import timedelta
from flask import Flask, jsonify, request

from wip_kanban import server_config
from wip_kanban.routes_kanban import kanban_bp

logger = logging.getLogger("WipKanban")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )


def create_app():
    setup_logging()
    cfg = server_config.load_config()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )
    app.secret_key = cfg.get("session_secret") or os.urandom(32)
    app.permanent_session_lifetime = timedelta(minutes=int(cfg.get("session_lifetime_minutes", 480)))

    app.register_blueprint(kanban_bp)

    @app.before_request
    def log_request():
        logger.info("Request %s %s from %s", request.method, request.path, request.remote_addr)

    @app.after_request
    def log_response(response):
        logger.info("Response %s %s -> %s", request.method, request.path, response.status_code)
        return response

    def _is_api_request():
        return request.path.startswith('/kanban/api/')

    @app.errorhandler(403)
    def handle_403(e):
        if _is_api_request():
            return jsonify({"error": "forbidden", "message": "Token mancante, scaduto o non valido. Ricaricare la pagina da DocumentManagement."}), 403
        return e

    @app.errorhandler(404)
    def handle_404(e):
        if _is_api_request():
            return jsonify({"error": "not_found", "message": "Endpoint non trovato."}), 404
        return e

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Errore non gestito: %s", e)
        if _is_api_request():
            return jsonify({"error": "internal_error", "message": str(e)}), 500
        return e

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "wip_kanban"})

    @app.route("/")
    def index():
        return "Kanban produzione - server attivo", 200

    return app


def _start_shift_email_scheduler():
    """Thread daemon: email riepilogativa ai cambi turno 15:30 / 23:30.

    L'import di shift_email (utils, email connector) avviene DENTRO il thread:
    non rallenta l'avvio del server (il check porta del dashboard attende ~5s)."""
    import threading

    def _run():
        from wip_kanban import shift_email
        shift_email.scheduler_loop()

    t = threading.Thread(target=_run, daemon=True,
                         name="wip_kanban_shift_email")
    t.start()
    logger.info("Scheduler email kanban avviato")


def _is_bindable(host: str, port: int) -> bool:
    """True se l'indirizzo è locale e la porta è libera su questo PC."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def main():
    app = create_app()
    _start_shift_email_scheduler()
    cfg = server_config.load_config()
    # Bind di default su TUTTE le interfacce: il check del dashboard (localhost)
    # e i client (server_host_ip) devono entrambi raggiungere il server.
    # server_host_ip resta l'indirizzo "pubblicizzato" per URL/browser.
    host = cfg.get("server_bind_host") or "0.0.0.0"
    port = int(cfg.get("server_port", 6500))
    if host not in ("0.0.0.0", "127.0.0.1", "localhost") and not _is_bindable(host, port):
        logger.warning(
            "Indirizzo %s:%s non disponibile su questo PC: avvio su 0.0.0.0.",
            host, port,
        )
        host = "0.0.0.0"
    logger.info("Avvio server kanban su %s:%s", host, port)
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
