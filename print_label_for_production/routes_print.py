# -*- coding: utf-8 -*-
"""
routes_print.py — Route per le pagine di stampa etichette.

Pagine:
  /print/generic  -> Stampa generica di etichette
  /print/orders   -> Stampa etichette legata agli ordini
"""
import logging
import socket
import tempfile
import os
from flask import Blueprint, render_template, request, jsonify

from . import db, auth, i18n, label_needs

logger = logging.getLogger("PrintLabelProduction")

print_bp = Blueprint("print", __name__, url_prefix="/print")


# ---------------------------------------------------------------------------
# Query riutilizzabili
# ---------------------------------------------------------------------------

LABELS_QUERY = """
SELECT
    m.materialeid,
    UPPER(m.CodiceMateriale) AS MaterialCode,
    UPPER(m.DescrizioneMateriale) AS MaterialDescription
FROM traceability_rs.ind.Materiali AS m
LEFT JOIN traceability_rs.ind.FamigliaMateriali AS fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE fm.Famiglia = 'Labels'
ORDER BY m.CodiceMateriale;
"""

PRINTERS_QUERY = """
SELECT LabelPrinterId, PrinterName, PrinterType, ConnectionString,
       PrinterIP, PrinterPort, PrinterLocation, PrinterModel, IsDefault
FROM Traceability_RS.ind.LabelPrinters
WHERE DateOut IS NULL
ORDER BY PrinterName;
"""

LABEL_TYPE_PARAMS_QUERY = """
SELECT ltp.MaterialeId, ltp.ScartoType, ltp.ScartoValue, ltp.ScartoMinimo,
       ltp.Arrotondamento, ltp.IsTraceabilityLabel
FROM Traceability_RS.ind.LabelTypeParameters ltp
WHERE ltp.DateOut IS NULL;
"""

CURRENT_RIBBON_QUERY = """
SELECT TOP 1 lm.RibbonId, r.DescrizioneMateriale AS RibbonDescription
FROM Traceability_RS.dbo.LinkedMaterials lm
LEFT JOIN Traceability_RS.ind.Materiali r ON r.MaterialeId = lm.RibbonId
WHERE lm.LabelId = ? AND lm.dateout IS NULL
ORDER BY lm.dateIn DESC;
"""

CURRENT_PRINTER_QUERY = """
SELECT TOP 1 lpa.LabelPrinterId, p.PrinterName, p.PrinterType, p.ConnectionString,
       p.PrinterIP, p.PrinterPort, p.PrinterLocation, p.PrinterModel
FROM Traceability_RS.dbo.LabelPrinterAssociations lpa
LEFT JOIN Traceability_RS.ind.LabelPrinters p ON p.LabelPrinterId = lpa.LabelPrinterId AND p.DateOut IS NULL
WHERE lpa.LabelId = ? AND lpa.dateout IS NULL
ORDER BY lpa.dateIn DESC;
"""

CURRENT_SCRIPT_QUERY = """
SELECT TOP 1 ls.ScriptToPrint
FROM Traceability_RS.ind.LabelScripts ls
JOIN Traceability_RS.ind.BomIndirectMaterials bm ON bm.BomIndirectMaterialId = ls.BomIndirectMaterialId
WHERE bm.MaterialeID = ? AND ls.DateOut IS NULL AND bm.DateOut IS NULL
ORDER BY ls.DateIn DESC;
"""

CURRENT_COUNTER_QUERY = """
SELECT TOP 1 LabelCounterId, Prefix, Suffix, LastCounter
FROM Traceability_RS.ind.LabelCounters
WHERE MaterialeId = ? AND DateOut IS NULL
ORDER BY DateIn DESC;
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_user_name():
    user = auth.get_session_user()
    return user["user_name"] if user else "N/A"


def _fetch_labels(cur):
    cur.execute(LABELS_QUERY)
    return db.fetch_all_dict(cur)


def _fetch_printers(cur):
    cur.execute(PRINTERS_QUERY)
    return db.fetch_all_dict(cur)


def _fetch_label_type_params(cur):
    cur.execute(LABEL_TYPE_PARAMS_QUERY)
    return {row["MaterialeId"]: row for row in db.fetch_all_dict(cur)}


def _fetch_current_ribbon(cur, label_id):
    cur.execute(CURRENT_RIBBON_QUERY, (label_id,))
    return db.row_to_dict(cur.fetchone(), cur)


def _fetch_current_printer(cur, label_id):
    cur.execute(CURRENT_PRINTER_QUERY, (label_id,))
    return db.row_to_dict(cur.fetchone(), cur)


def _fetch_current_script(cur, label_id):
    cur.execute(CURRENT_SCRIPT_QUERY, (label_id,))
    row = cur.fetchone()
    return row[0] if row else ""


def _fetch_current_counter(cur, label_id):
    cur.execute(CURRENT_COUNTER_QUERY, (label_id,))
    row = cur.fetchone()
    if not row:
        return None
    return {
        "LabelCounterId": row[0],
        "Prefix": row[1],
        "Suffix": row[2],
        "LastCounter": row[3],
    }


def _send_network(script, ip, port):
    try:
        port = int(port) if port else 9100
        with socket.create_connection((ip, port), timeout=5) as sock:
            sock.sendall(script.encode("utf-8"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Errore invio socket a %s:%s", ip, port)
        return {"ok": False, "message": f"Errore socket {ip}:{port}: {e}"}


def _send_to_printer(script, printer):
    """Invia lo script alla stampante in base al tipo configurato."""
    ptype = (printer.get("PrinterType") or "NETWORK").upper()
    conn_str = printer.get("ConnectionString") or ""
    ip = printer.get("PrinterIP") or ""
    port = printer.get("PrinterPort")

    if ptype == "NETWORK" or (ip and port):
        return _send_network(script, ip or conn_str, port)

    if ptype == "USB":
        # Fallback: salva file .prn e prova a stampare tramite driver Windows
        try:
            fd, path = tempfile.mkstemp(suffix=".prn", prefix="label_")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(script)
            # Se win32print è disponibile, lo usa
            try:
                import win32print
                import win32api
                printer_name = conn_str or printer.get("PrinterName", "")
                if printer_name:
                    h = win32print.OpenPrinter(printer_name)
                    try:
                        win32print.StartDocPrinter(h, 1, ("Label", None, "RAW"))
                        win32print.StartPagePrinter(h)
                        win32print.WritePrinter(h, script.encode("utf-8"))
                        win32print.EndPagePrinter(h)
                        win32print.EndDocPrinter(h)
                    finally:
                        win32print.ClosePrinter(h)
                    return {"ok": True}
            except Exception as e:
                logger.warning("win32print non disponibile o fallito: %s", e)
            return {"ok": True, "file_path": path, "message": "Script salvato in file .prn"}
        except Exception as e:
            return {"ok": False, "message": f"Errore salvataggio file: {e}"}

    # Fallback generico: salva file .prn
    try:
        fd, path = tempfile.mkstemp(suffix=".prn", prefix="label_")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(script)
        return {"ok": True, "file_path": path, "message": "Tipo stampante non gestito; script salvato in file .prn"}
    except Exception as e:
        return {"ok": False, "message": f"Errore fallback: {e}"}


# ---------------------------------------------------------------------------
# Placeholder pages
# ---------------------------------------------------------------------------

@print_bp.route("/generic")
@auth.require_page_token_or_session("print_generic")
def generic_print_page():
    user = auth.get_session_user()
    lang = request.args.get("lang", "it")[:10]
    ui = i18n.get_print_ui(lang)
    return render_template("print_generic.html", user=user["user_name"], lang=lang, ui=ui)


@print_bp.route("/orders")
@auth.require_page_token_or_session("print_orders")
def orders_print_page():
    user = auth.get_session_user()
    lang = request.args.get("lang", "it")[:10]
    ui = i18n.get_print_ui(lang)
    return render_template("print_orders.html", user=user["user_name"], lang=lang, ui=ui)


# ---------------------------------------------------------------------------
# API Stampa generica
# ---------------------------------------------------------------------------

@print_bp.route("/api/generic/data")
@auth.require_page_token_or_session("print_generic")
def api_generic_data():
    """Restituisce labels, stampanti, parametri, associazioni e counter per la stampa generica."""
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        labels = _fetch_labels(cur)
        printers = _fetch_printers(cur)
        params = _fetch_label_type_params(cur)
        for label in labels:
            lid = label["materialeid"]
            label["ribbon"] = _fetch_current_ribbon(cur, lid) or {}
            label["printer"] = _fetch_current_printer(cur, lid) or {}
            label["script"] = _fetch_current_script(cur, lid) or ""
            label["counter"] = _fetch_current_counter(cur, lid) or {
                "LabelCounterId": None,
                "Prefix": "",
                "Suffix": "",
                "LastCounter": 0,
            }
            label["is_traceability"] = bool(params.get(lid, {}).get("IsTraceabilityLabel", 0))

        default_printer = next((p for p in printers if p.get("IsDefault")), None)
        return jsonify({
            "labels": labels,
            "printers": printers,
            "default_printer": default_printer,
            "params": params,
        })
    except Exception as e:
        logger.exception("Errore /api/generic/data: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


@print_bp.route("/api/generic/print", methods=["POST"])
@auth.require_page_token_or_session("print_generic")
def api_generic_print():
    """Esegue la stampa generica di una o più etichette."""
    data = request.get_json(silent=True) or {}
    label_id = data.get("label_id")
    printer_id = data.get("printer_id")
    quantity = int(data.get("quantity", 1) or 1)
    prefix = (data.get("prefix") or "").strip()
    suffix = (data.get("suffix") or "").strip()
    counter_start = int(data.get("counter") or 0)
    script_template = data.get("script", "")
    order_ids = data.get("order_ids") or []

    if not label_id or not printer_id or quantity <= 0:
        return jsonify({"error": "missing_parameters"}), 400

    conn = db.get_conn()
    try:
        cur = conn.cursor()

        # Parametri etichetta
        cur.execute(
            """SELECT TOP 1 IsTraceabilityLabel
               FROM Traceability_RS.ind.LabelTypeParameters
               WHERE MaterialeId = ? AND DateOut IS NULL
               ORDER BY DateIn DESC""",
            (label_id,),
        )
        row = cur.fetchone()
        is_traceability = bool(row[0]) if row else False

        # Recupera stampante
        cur.execute(
            """SELECT LabelPrinterId, PrinterName, PrinterType, ConnectionString,
                      PrinterIP, PrinterPort
               FROM Traceability_RS.ind.LabelPrinters
               WHERE LabelPrinterId = ? AND DateOut IS NULL""",
            (printer_id,),
        )
        printer = db.row_to_dict(cur.fetchone(), cur)
        if not printer:
            return jsonify({"error": "printer_not_found"}), 404

        user = _get_user_name()
        counter_from = counter_start
        counter_to = counter_start

        if not is_traceability:
            counter_to = counter_from + quantity - 1
            # Compila lo script per ogni pezzo
            scripts = []
            for i in range(quantity):
                serial = f"{prefix}{counter_from + i}{suffix}"
                scripts.append(script_template.replace("{SERIAL}", serial).replace("{COUNTER}", str(counter_from + i)))
            full_script = "\n".join(scripts)
        else:
            # Etichetta tracciabilità: non usa counter, lo script viene usato così come è
            # (eventualmente sostituzioni specifiche possono essere aggiunte in seguito)
            full_script = script_template

        # Invio alla stampante
        result = _send_to_printer(full_script, printer)
        if not result.get("ok"):
            return jsonify({"error": "print_error", "message": result.get("message")}), 500

        # Aggiorna counter persistente
        if not is_traceability:
            cur.execute(
                """SELECT TOP 1 LabelCounterId
                   FROM Traceability_RS.ind.LabelCounters
                   WHERE MaterialeId = ? AND DateOut IS NULL
                   ORDER BY DateIn DESC""",
                (label_id,),
            )
            existing = cur.fetchone()
            new_last = counter_to + 1
            if existing:
                cur.execute(
                    """UPDATE Traceability_RS.ind.LabelCounters
                       SET LastCounter = ?, Prefix = ?, Suffix = ?, DateIn = GETDATE(), [User] = ?
                       WHERE LabelCounterId = ?""",
                    (new_last, prefix, suffix, user, existing[0]),
                )
            else:
                cur.execute(
                    """INSERT INTO Traceability_RS.ind.LabelCounters
                       (MaterialeId, Prefix, Suffix, LastCounter, DateIn, [User])
                       VALUES (?, ?, ?, ?, GETDATE(), ?)""",
                    (label_id, prefix, suffix, new_last, user),
                )

        # Log stampa
        cur.execute(
            """INSERT INTO Traceability_RS.ind.LabelPrintLog
               (MaterialeId, LabelPrinterId, OrderId, Quantity, CounterFrom, CounterTo,
                Prefix, Suffix, ScriptSnapshot, PrintedAt, [User])
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)""",
            (label_id, printer_id, order_ids[0] if order_ids else None, quantity,
             counter_from, counter_to, prefix, suffix, full_script[:4000], user),
        )

        conn.commit()
        return jsonify({
            "ok": True,
            "printed": quantity,
            "counter_from": counter_from,
            "counter_to": counter_to,
            "next_counter": counter_to + 1 if not is_traceability else None,
            "file_path": result.get("file_path"),
            "message": result.get("message"),
        })
    except Exception as e:
        logger.exception("Errore /api/generic/print: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# API Stampa per ordini (placeholder strutturale)
# ---------------------------------------------------------------------------

@print_bp.route("/api/orders/search")
@auth.require_page_token_or_session("print_orders")
def api_orders_search():
    """Ricerca ordini per numero ordine / prodotto."""
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify([])
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        # Cerca ordini attivi (non ancora completati in AOI) per numero ordine o prodotto
        cur.execute(
            """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
               SELECT TOP 50 o.IDOrder, o.OrderNumber, p.IDProduct, p.ProductCode, p.ProductName, o.OrderQuantity
               FROM Traceability_RS.dbo.Orders o
               INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
               WHERE (o.OrderNumber LIKE ? OR p.ProductCode LIKE ? OR p.ProductName LIKE ?)
               ORDER BY o.OrderDate DESC
               SET TRANSACTION ISOLATION LEVEL READ COMMITTED;""",
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
        rows = db.fetch_all_dict(cur)
        conn.close()
        return jsonify(rows)
    except Exception as e:
        logger.exception("Errore /api/orders/search: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@print_bp.route("/api/orders/labels")
@auth.require_page_token_or_session("print_orders")
def api_orders_labels():
    """Restituisce etichette, ribbon, script, stampanti per il prodotto dell'ordine."""
    order_id = request.args.get("order_id", type=int)
    if not order_id:
        return jsonify({"error": "missing_order_id"}), 400
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        # Recupera prodotto e quantità ordine
        cur.execute(
            """SELECT o.IDOrder, o.OrderNumber, o.IDProduct, p.ProductCode, p.ProductName, o.OrderQuantity
               FROM Traceability_RS.dbo.Orders o
               INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
               WHERE o.IDOrder = ?""",
            (order_id,),
        )
        order = db.row_to_dict(cur.fetchone(), cur)
        if not order:
            return jsonify({"error": "order_not_found"}), 404

        # Etichette associate al prodotto
        cur.execute(
            """SELECT bm.MaterialeID AS LabelId, bm.QuantityPerPiece,
                      m.CodiceMateriale AS MaterialCode, m.DescrizioneMateriale AS MaterialDescription
               FROM Traceability_RS.ind.BomIndirectMaterials bm
               JOIN Traceability_RS.ind.Materiali m ON m.MaterialeId = bm.MaterialeID
               JOIN Traceability_RS.ind.FamigliaMateriali fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
               WHERE bm.IDProduct = ? AND bm.DateOut IS NULL AND fm.Famiglia = 'Labels'
               ORDER BY m.CodiceMateriale""",
            (order["IDProduct"],),
        )
        labels = db.fetch_all_dict(cur)

        printers = _fetch_printers(cur)
        label_ids = [l["LabelId"] for l in labels]
        params = label_needs.fetch_label_parameters(cur, label_ids) if label_ids else {}

        order_qty = float(order.get("OrderQuantity") or 0)
        for label in labels:
            lid = label["LabelId"]
            label["ribbon"] = _fetch_current_ribbon(cur, lid) or {}
            label["printer"] = _fetch_current_printer(cur, lid) or {}
            label["script"] = _fetch_current_script(cur, lid) or ""
            label["is_traceability"] = bool(params.get(lid, {}).get("IsTraceabilityLabel", 0))
            label["params"] = params.get(lid)
            qty_per_piece = float(label.get("QuantityPerPiece") or 1)
            qty_net = order_qty * qty_per_piece
            scarto = label_needs.compute_scarto(qty_net, label.get("params"))
            arrotondamento = float((label.get("params") or {}).get("Arrotondamento") or 1)
            label["suggested_qty"] = int(label_needs.round_up(qty_net + scarto, arrotondamento))
            label["qty_net"] = qty_net
            label["qty_scarto"] = scarto

        conn.close()
        return jsonify({
            "order": order,
            "labels": labels,
            "printers": printers,
            "default_printer": next((p for p in printers if p.get("IsDefault")), None),
        })
    except Exception as e:
        logger.exception("Errore /api/orders/labels: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@print_bp.route("/api/orders/print", methods=["POST"])
@auth.require_page_token_or_session("print_orders")
def api_orders_print():
    """Esegue la stampa per ordini."""
    data = request.get_json(silent=True) or {}
    order_id = data.get("order_id")
    rows = data.get("rows") or []
    print_all_together = bool(data.get("print_all_together", False))
    if not order_id or not rows:
        return jsonify({"error": "missing_parameters"}), 400

    conn = db.get_conn()
    try:
        cur = conn.cursor()
        user = _get_user_name()
        printed = 0
        log_ids = []
        scripts_by_printer = {}

        for row in rows:
            label_id = row.get("label_id")
            printer_id = row.get("printer_id")
            quantity = int(row.get("quantity") or 0)
            script_template = row.get("script_data") or ""
            if not label_id or not printer_id or quantity <= 0 or not script_template:
                continue

            cur.execute(
                """SELECT TOP 1 IsTraceabilityLabel
                   FROM Traceability_RS.ind.LabelTypeParameters
                   WHERE MaterialeId = ? AND DateOut IS NULL
                   ORDER BY DateIn DESC""",
                (label_id,),
            )
            r = cur.fetchone()
            is_traceability = bool(r[0]) if r else False

            cur.execute(
                """SELECT LabelPrinterId, PrinterName, PrinterType, ConnectionString,
                          PrinterIP, PrinterPort
                   FROM Traceability_RS.ind.LabelPrinters
                   WHERE LabelPrinterId = ? AND DateOut IS NULL""",
                (printer_id,),
            )
            printer = db.row_to_dict(cur.fetchone(), cur)
            if not printer:
                continue

            counter_from = 0
            counter_to = 0
            prefix = ""
            suffix = ""
            full_script = ""

            if not is_traceability:
                counter_start = 0
                cur.execute(
                    """SELECT TOP 1 LabelCounterId, LastCounter, Prefix, Suffix
                       FROM Traceability_RS.ind.LabelCounters
                       WHERE MaterialeId = ? AND DateOut IS NULL
                       ORDER BY DateIn DESC""",
                    (label_id,),
                )
                cr = cur.fetchone()
                if cr:
                    counter_start = int(cr[1] or 0)
                    prefix = cr[2] or ""
                    suffix = cr[3] or ""
                counter_from = counter_start
                counter_to = counter_start + quantity - 1
                scripts = []
                for i in range(quantity):
                    serial = f"{prefix}{counter_start + i}{suffix}"
                    scripts.append(script_template.replace("{SERIAL}", serial).replace("{COUNTER}", str(counter_start + i)))
                full_script = "\n".join(scripts)
                new_last = counter_to + 1
                if cr:
                    cur.execute(
                        "UPDATE Traceability_RS.ind.LabelCounters SET LastCounter=?, Prefix=?, Suffix=?, DateIn=GETDATE(), [User]=? WHERE LabelCounterId=?",
                        (new_last, prefix, suffix, user, cr[0]),
                    )
                else:
                    cur.execute(
                        "INSERT INTO Traceability_RS.ind.LabelCounters (MaterialeId, LastCounter, DateIn, [User]) VALUES (?, ?, GETDATE(), ?)",
                        (label_id, new_last, user),
                    )
            else:
                full_script = script_template

            if print_all_together:
                key = printer_id
                scripts_by_printer[key] = scripts_by_printer.get(key, {"printer": printer, "scripts": [], "rows": []})
                scripts_by_printer[key]["scripts"].append(full_script)
                scripts_by_printer[key]["rows"].append({
                    "label_id": label_id, "quantity": quantity, "counter_from": counter_from,
                    "counter_to": counter_to, "prefix": prefix, "suffix": suffix,
                    "full_script": full_script,
                })
            else:
                result = _send_to_printer(full_script, printer)
                if not result.get("ok"):
                    return jsonify({"error": "print_error", "message": result.get("message")}), 500
                printed += quantity
                cur.execute(
                    """INSERT INTO Traceability_RS.ind.LabelPrintLog
                       (MaterialeId, LabelPrinterId, OrderId, Quantity, CounterFrom, CounterTo,
                        Prefix, Suffix, ScriptSnapshot, PrintedAt, [User])
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)""",
                    (label_id, printer_id, order_id, quantity, counter_from, counter_to,
                     prefix, suffix, full_script[:4000], user),
                )
                log_ids.append(cur.fetchone())  # non restituisce niente con INSERT

        if print_all_together:
            for key, item in scripts_by_printer.items():
                combined = "\n".join(item["scripts"])
                result = _send_to_printer(combined, item["printer"])
                if not result.get("ok"):
                    return jsonify({"error": "print_error", "message": result.get("message")}), 500
                for r in item["rows"]:
                    printed += r["quantity"]
                    cur.execute(
                        """INSERT INTO Traceability_RS.ind.LabelPrintLog
                           (MaterialeId, LabelPrinterId, OrderId, Quantity, CounterFrom, CounterTo,
                            Prefix, Suffix, ScriptSnapshot, PrintedAt, [User])
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)""",
                        (r["label_id"], key, order_id, r["quantity"], r["counter_from"], r["counter_to"],
                         r["prefix"], r["suffix"], r["full_script"][:4000], user),
                    )

        conn.commit()
        return jsonify({"ok": True, "printed": printed, "print_all_together": print_all_together})
    except Exception as e:
        logger.exception("Errore /api/orders/print: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()
