# -*- coding: utf-8 -*-
"""
web_server.py — Web server intranet per Etichette Produzione (Flask).

Avvio sul server 192.168.10.72:
    .venv\Scripts\python.exe print_label_for_production\web_server.py

Configurazione: print_label_server_config.json (nella directory dell'eseguibile).
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

from print_label_for_production import server_config
from print_label_for_production.routes_bom import bom_bp
from print_label_for_production.routes_printers import printers_bp

logger = logging.getLogger("PrintLabelProduction")


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
    app.permanent_session_lifetime = timedelta(minutes=int(cfg.get("session_lifetime_minutes", 30)))

    app.register_blueprint(bom_bp)
    app.register_blueprint(printers_bp)

    @app.before_request
    def log_request():
        logger.info("Request %s %s from %s", request.method, request.path, request.remote_addr)

    @app.after_request
    def log_response(response):
        logger.info("Response %s %s -> %s", request.method, request.path, response.status_code)
        return response

    def _is_api_request():
        return request.path.startswith('/api/')

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

    @app.errorhandler(500)
    def handle_500(e):
        logger.exception("Errore interno server: %s", e)
        if _is_api_request():
            return jsonify({"error": "internal_error", "message": str(e.original_exception) if getattr(e, 'original_exception', None) else "Errore interno del server."}), 500
        return e

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Errore non gestito: %s", e)
        if _is_api_request():
            return jsonify({"error": "internal_error", "message": str(e)}), 500
        return e

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/")
    def index():
        return "Etichette Produzione - server attivo", 200

    return app


def main():
    cfg = server_config.load_config()
    app = create_app()
    host = cfg.get("server_host_ip", "0.0.0.0")
    port = int(cfg.get("server_port", 5015))
    logger.info("Avvio PrintLabelProduction server su %s:%s", host, port)
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
