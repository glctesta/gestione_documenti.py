# -*- coding: utf-8 -*-
"""
routes_kanban.py — Route web del kanban WIP/REPAIR.

Pagine:
  /kanban/load  -> Carica schede (permesso 'crea_kanBan_produzione')
  /kanban/pick  -> Preleva schede (login semplice, tutto auditato)

NOTA: le route /kanban/report* (pagina report + API filtri + export Excel)
sono VOLONTARIAMENTE PUBBLICHE (nessun token/auth): il report riguarda solo
le schede attualmente presenti in kanban ed e' destinato alla rete interna.
"""
import logging
from datetime import datetime

import pyodbc
from flask import Blueprint, render_template, request, jsonify, send_file, session

from . import db, auth, i18n, kanban_logic, pdf_gen, excel_gen

logger = logging.getLogger("WipKanban")

kanban_bp = Blueprint("kanban", __name__, url_prefix="/kanban")


def _user_name():
    user = auth.get_session_user() or {}
    return user.get("user_name") or "Unknown"


def _ui():
    lang = request.args.get("lang") or "it"
    return i18n.get_ui(lang), lang


def _conn():
    conn = db.get_conn()
    conn.timeout = 60
    return conn


@kanban_bp.route("/load")
@auth.require_page_token_or_session("kanban_load")
def page_load():
    ui, lang = _ui()
    return render_template("kanban_load.html", ui=ui, lang=lang, user=_user_name())


@kanban_bp.route("/pick")
@auth.require_page_token_or_session("kanban_pick")
def page_pick():
    ui, lang = _ui()
    return render_template("kanban_pick.html", ui=ui, lang=lang, user=_user_name(),
                           warning_ro=i18n.PICK_WARNING_RO)


# ── API comuni ────────────────────────────────────────────────────────────────

@kanban_bp.route("/api/masters")
@auth.require_page_token_or_session("kanban_load")
def api_masters():
    conn = _conn()
    try:
        cur = conn.cursor()
        return jsonify({
            "masters": kanban_logic.list_masters(cur),
            "counts": kanban_logic.counts(cur),
        })
    finally:
        conn.close()


@kanban_bp.route("/api/locations/create", methods=["POST"])
@auth.require_page_token_or_session("kanban_load")
def api_create_location():
    body = request.get_json(silent=True) or {}
    area = body.get("area")
    row_index = body.get("row_index")
    deposit = body.get("deposit") or 1
    try:
        row_index = int(row_index) if row_index not in (None, "") else None
        deposit = int(deposit)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_params", "message": "row_index/deposit non numerici"}), 400
    conn = _conn()
    try:
        cur = conn.cursor()
        try:
            code = kanban_logic.create_location(cur, area, _user_name(),
                                                row_index=row_index, deposit=deposit)
        except ValueError as e:
            err = str(e)
            if err == "missing_row_index":
                return jsonify({"error": "missing_row_index"}), 409
            if err == "duplicate_row_index":
                return jsonify({"error": "duplicate_row_index"}), 409
            return jsonify({"error": "invalid_area", "message": str(e)}), 400
        conn.commit()
        return jsonify({"ok": True, "code": code})
    except pyodbc.IntegrityError:
        conn.rollback()
        logger.warning("Tentativo di duplicato su WipKanbanLocations (area=%s)", area)
        return jsonify({"error": "duplicate"}), 409
    except Exception as e:
        conn.rollback()
        logger.exception("Errore creazione locazione: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


@kanban_bp.route("/api/masters/<master>/rowindex", methods=["POST"])
@auth.require_page_token_or_session("kanban_load")
def api_master_rowindex(master):
    body = request.get_json(silent=True) or {}
    row_index = body.get("row_index")
    deposit = body.get("deposit") or 1
    try:
        row_index = int(row_index)
        deposit = int(deposit)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_params", "message": "row_index/deposit non numerici"}), 400
    conn = _conn()
    try:
        cur = conn.cursor()
        try:
            found = kanban_logic.set_master_rowindex(cur, master, row_index, deposit=deposit)
        except ValueError as e:
            err = str(e)
            if err == "duplicate_row_index":
                return jsonify({"error": "duplicate_row_index"}), 409
            return jsonify({"error": "invalid_params", "message": str(e)}), 400
        if not found:
            conn.rollback()
            return jsonify({"error": "unknown_master"}), 404
        conn.commit()
        return jsonify({"ok": True, "code": master, "row_index": row_index})
    except Exception as e:
        conn.rollback()
        logger.exception("Errore aggiornamento RowIndex per %s: %s", master, e)
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


@kanban_bp.route("/api/positions")
@auth.require_page_token_or_session("kanban_load")
def api_positions():
    master = request.args.get("master") or ""
    conn = _conn()
    try:
        cur = conn.cursor()
        return jsonify({"positions": kanban_logic.list_positions(cur, master)})
    finally:
        conn.close()


@kanban_bp.route("/api/positions/<code>/boards")
@auth.require_page_token_or_session("kanban_load")
def api_boards_in_position(code):
    conn = _conn()
    try:
        cur = conn.cursor()
        return jsonify({"boards": kanban_logic.boards_in_position(cur, code)})
    finally:
        conn.close()


@kanban_bp.route("/api/board-info")
@auth.require_page_token_or_session("kanban_load")
def api_board_info():
    labelcode = (request.args.get("labelcode") or "").strip()
    if not labelcode:
        return jsonify({"error": "missing_labelcode"}), 400
    conn = _conn()
    try:
        cur = conn.cursor()
        info = kanban_logic.board_info(cur, labelcode)
        if not info:
            return jsonify({"error": "not_found"}), 404
        return jsonify(info)
    finally:
        conn.close()


@kanban_bp.route("/api/positions/<code>/boards", methods=["POST"])
@auth.require_page_token_or_session("kanban_load")
def api_load_board(code):
    labelcode = (request.get_json(silent=True) or {}).get("labelcode") or ""
    conn = _conn()
    try:
        cur = conn.cursor()
        ok, err, info = kanban_logic.load_board(cur, code, labelcode, _user_name())
        if not ok:
            conn.rollback()
            status = 404 if err in ("invalid_labelcode", "invalid_position") else 409
            return jsonify({"error": err, "info": info}), status
        conn.commit()
        return jsonify({"ok": True, "info": info})
    except Exception as e:
        conn.rollback()
        logger.exception("Errore caricamento scheda: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


# ── PDF ───────────────────────────────────────────────────────────────────────

@kanban_bp.route("/api/masters/<master>/labels.pdf")
@auth.require_page_token_or_session("kanban_load")
def api_labels_pdf(master):
    conn = _conn()
    try:
        cur = conn.cursor()
        positions = kanban_logic.list_positions(cur, master)
        if not positions:
            return jsonify({"error": "unknown_master"}), 404
        path = pdf_gen.labels_pdf(positions)
        return send_file(path, as_attachment=True, download_name=f"kanban_labels_{master}.pdf")
    finally:
        conn.close()


@kanban_bp.route("/api/list.pdf")
@auth.require_page_token_or_session("kanban_load")
def api_list_pdf():
    ui, _ = _ui()
    master = (request.args.get("master") or "").strip()
    conn = _conn()
    try:
        cur = conn.cursor()
        if master:
            if not kanban_logic.parse_master(master):
                return jsonify({"error": "unknown_master"}), 404
            rows = kanban_logic.boards_in_master(cur, master)
            title = ui["boards_in_position"].replace("{code}", master)
        else:
            rows = kanban_logic.list_all_boards(cur)
            title = ui["title_load"]
        path = pdf_gen.list_pdf(rows, title=title,
                                subtitle=f"{len(rows)} schede — {datetime.now():%d/%m/%Y %H:%M}")
        return send_file(path, as_attachment=True, download_name="kanban_lista_schede.pdf")
    finally:
        conn.close()


@kanban_bp.route("/api/export.xlsx")
@auth.require_page_token_or_session("kanban_load")
def api_export_xlsx():
    ui, _ = _ui()
    conn = _conn()
    try:
        cur = conn.cursor()
        rows_by_area = {
            area: kanban_logic.list_all_boards_by_area(cur, area)
            for area in kanban_logic.AREA_LETTERS
        }
        path = excel_gen.kanban_workbook(rows_by_area, ui)
        return send_file(path, as_attachment=True,
                         download_name=f"kanban_export_{datetime.now():%Y%m%d_%H%M}.xlsx")
    finally:
        conn.close()


# ── Report (PUBBLICO: nessun token, rete interna) ────────────────────────────

@kanban_bp.route("/report")
def page_report():
    ui, lang = _ui()
    return render_template("kanban_report.html", ui=ui, lang=lang)


@kanban_bp.route("/api/report/filters")
def api_report_filters():
    conn = _conn()
    try:
        cur = conn.cursor()
        return jsonify(kanban_logic.report_filter_values(cur))
    finally:
        conn.close()


@kanban_bp.route("/api/report.xlsx")
def api_report_xlsx():
    ui, _ = _ui()
    order = request.args.get("order") or ""
    wip_type = request.args.get("type") or "all"
    product = request.args.get("product") or ""
    state = request.args.get("state") or "all"
    conn = _conn()
    try:
        cur = conn.cursor()
        rows = kanban_logic.report_boards(cur, order=order, wip_type=wip_type,
                                          product=product, state=state)
        path = excel_gen.report_workbook(rows, ui)
        return send_file(path, as_attachment=True,
                         download_name=f"kanban_report_{datetime.now():%Y%m%d_%H%M}.xlsx")
    finally:
        conn.close()


# ── Pagina Preleva ────────────────────────────────────────────────────────────

@kanban_bp.route("/api/search")
@auth.require_page_token_or_session("kanban_pick")
def api_search():
    order = request.args.get("order") or ""
    product = request.args.get("product") or ""
    labelcode = request.args.get("labelcode") or ""
    if not order and not product and not labelcode:
        return jsonify({"error": "missing_query"}), 400
    conn = _conn()
    try:
        cur = conn.cursor()
        return jsonify({"locations": kanban_logic.search_locations(
            cur, order=order, product=product, labelcode=labelcode)})
    finally:
        conn.close()


@kanban_bp.route("/api/board-status")
@auth.require_page_token_or_session("kanban_pick")
def api_board_status():
    labelcode = (request.args.get("labelcode") or "").strip()
    if not labelcode:
        return jsonify({"error": "missing_labelcode"}), 400
    conn = _conn()
    try:
        cur = conn.cursor()
        status = kanban_logic.kanban_status(cur, labelcode)
        if not status:
            return jsonify({"error": "not_in_kanban"}), 404
        return jsonify(status)
    finally:
        conn.close()


@kanban_bp.route("/api/withdraw", methods=["POST"])
@auth.require_page_token_or_session("kanban_pick")
def api_withdraw():
    labelcode = (request.get_json(silent=True) or {}).get("labelcode") or ""
    conn = _conn()
    try:
        cur = conn.cursor()
        ok, err, info = kanban_logic.withdraw_board(cur, labelcode, _user_name())
        if not ok:
            conn.rollback()
            return jsonify({"error": err}), 404 if err == "not_in_kanban" else 400
        conn.commit()
        return jsonify({"ok": True, "info": info})
    except Exception as e:
        conn.rollback()
        logger.exception("Errore prelievo scheda: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()
