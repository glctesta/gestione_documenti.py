# -*- coding: utf-8 -*-
"""
routes_printers.py — Route per la pagina Gestione stampanti.

Nota: lo schema della tabella ind.LabelPrinters è proposto; adattare se già esiste.
"""
import logging
from flask import Blueprint, render_template, request, jsonify

from . import db, auth, i18n

logger = logging.getLogger("PrintLabelProduction")

printers_bp = Blueprint("printers", __name__, url_prefix="")


@printers_bp.route("/printers")
@auth.require_page_token_or_session("printers")
def printers_page():
    user = auth.get_session_user()
    lang = request.args.get("lang", "it")[:10]
    ui = i18n.get_printers_ui(lang)
    return render_template("printers.html", user=user["user_name"], lang=lang, ui=ui)


@printers_bp.route("/api/printers")
@auth.require_page_token_or_session("printers")
def api_printers_list():
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT LabelPrinterId, PrinterName, PrinterType, ConnectionString,
                          PrinterIP, PrinterPort, PrinterLocation, PrinterModel,
                          LastRevisionDate, IsDefault, DateIn
                   FROM Traceability_RS.ind.LabelPrinters
                   WHERE DateOut IS NULL
                   ORDER BY PrinterName"""
            )
            return jsonify(db.fetch_all_dict(cur))
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/printers: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@printers_bp.route("/api/printers", methods=["POST"])
@auth.require_page_token_or_session("printers")
def api_printers_save():
    data = request.get_json(silent=True) or {}
    name = data.get("printer_name", "").strip()
    ptype = data.get("printer_type", "USB")
    conn_str = data.get("connection_string", "").strip()
    printer_ip = data.get("printer_ip", "").strip()
    printer_port = data.get("printer_port")
    printer_location = data.get("printer_location", "").strip()
    model = data.get("printer_model", "").strip()
    last_revision = data.get("last_revision_date") or None
    is_default = bool(data.get("is_default", False))

    if not name:
        return jsonify({"error": "missing_name"}), 400

    try:
        printer_port = int(printer_port) if printer_port else None
    except (ValueError, TypeError):
        printer_port = None

    user = auth.get_session_user()["user_name"]
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        if is_default:
            cur.execute(
                """UPDATE Traceability_RS.ind.LabelPrinters
                   SET DateOut = GETDATE()
                   WHERE IsDefault = 1 AND DateOut IS NULL"""
            )
        cur.execute(
            """INSERT INTO Traceability_RS.ind.LabelPrinters
               (PrinterName, PrinterType, ConnectionString, PrinterIP, PrinterPort,
                PrinterLocation, PrinterModel, LastRevisionDate, IsDefault, DateIn, [User])
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)""",
            (name, ptype, conn_str, printer_ip, printer_port, printer_location,
             model, last_revision, int(is_default), user),
        )
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        logger.exception("Errore salvataggio stampante: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()
