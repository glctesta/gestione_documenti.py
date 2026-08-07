# -*- coding: utf-8 -*-
"""
routes_bom.py — Route per la pagina Gestione BOM.
"""
import logging
from flask import Blueprint, render_template, request, jsonify

from . import db, auth, i18n

logger = logging.getLogger("PrintLabelProduction")

bom_bp = Blueprint("bom", __name__, url_prefix="")


@bom_bp.route("/bom")
@auth.require_page_token_or_session("bom")
def bom_page():
    user = auth.get_session_user()
    lang = request.args.get("lang", "it")[:10]
    ui = i18n.get_bom_ui(lang)
    return render_template("bom.html", user=user["user_name"], lang=lang, ui=ui)


PRODUCTS_QUERY = """
SELECT
    p.idproduct,
    UPPER(p.productcode) AS ProductCode,
    UPPER(p.productname) AS ProductName,
    ISNULL(m.materialeid, 0) AS LabelId,
    ISNULL(bm.BomIndirectMaterialId, 0) AS BomIndirectMaterialId,
    IIF(ISNULL(m.materialeid, 0) = 0, 'Not Linked At Label',
        m.CodiceMateriale + ' ' + RTRIM(m.DescrizioneMateriale)) AS LinkedAtLabel
FROM traceability_rs.dbo.products p
OUTER APPLY (
    SELECT TOP 1 bm.BomIndirectMaterialId, bm.materialeid
    FROM traceability_rs.ind.BomIndirectMaterials bm
    JOIN traceability_rs.ind.Materiali m0 ON m0.MaterialeId = bm.materialeid
    JOIN traceability_rs.ind.FamigliaMateriali fm ON fm.FamigliaMaterialiId = m0.FamigliaMaterialiId
    WHERE bm.IDProduct = p.IDProduct
      AND bm.DateOut IS NULL
      AND fm.Famiglia = 'Labels'
    ORDER BY bm.DateIn DESC
) bm
LEFT JOIN traceability_rs.ind.Materiali m ON m.MaterialeId = bm.materialeid
WHERE CHARINDEX('CIPR', p.productcode, 1) = 0
ORDER BY UPPER(p.productcode);
"""

LABELS_QUERY = """
SELECT
    m.materialeid,
    UPPER(m.CodiceMateriale) AS MaterialCode,
    UPPER(m.DescrizioneMateriale) AS MaterialDescription,
    fm.FamigliaMaterialiId
FROM traceability_rs.ind.Materiali AS m
LEFT JOIN traceability_rs.ind.FamigliaMateriali AS fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE fm.Famiglia = 'Labels'
ORDER BY m.CodiceMateriale;
"""

RIBBONS_QUERY = """
SELECT
    m.materialeid,
    UPPER(m.CodiceMateriale) AS MaterialCode,
    UPPER(m.DescrizioneMateriale) AS MaterialDescription,
    fm.FamigliaMaterialiId
FROM traceability_rs.ind.Materiali AS m
LEFT JOIN traceability_rs.ind.FamigliaMateriali AS fm ON fm.FamigliaMaterialiId = m.FamigliaMaterialiId
WHERE fm.Famiglia = 'Ribbons'
ORDER BY m.CodiceMateriale;
"""


@bom_bp.route("/api/products")
@auth.require_page_token_or_session("bom")
def api_products():
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(PRODUCTS_QUERY)
            rows = db.fetch_all_dict(cur)
            logger.info("/api/products restituisce %s righe", len(rows))
            return jsonify(rows)
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/products: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/labels")
@auth.require_page_token_or_session("bom")
def api_labels():
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(LABELS_QUERY)
            rows = db.fetch_all_dict(cur)
            logger.info("/api/labels restituisce %s righe", len(rows))
            return jsonify(rows)
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/labels: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/ribbons")
@auth.require_page_token_or_session("bom")
def api_ribbons():
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(RIBBONS_QUERY)
            rows = db.fetch_all_dict(cur)
            logger.info("/api/ribbons restituisce %s righe", len(rows))
            return jsonify(rows)
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/ribbons: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/printer/default")
@auth.require_page_token_or_session("bom")
def api_default_printer():
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT TOP 1 LabelPrinterId, PrinterName, PrinterType, ConnectionString,
                          PrinterIP, PrinterPort, PrinterLocation, PrinterModel, IsDefault
                   FROM Traceability_RS.ind.LabelPrinters
                   WHERE DateOut IS NULL AND IsDefault = 1
                   ORDER BY DateIn DESC"""
            )
            row = db.row_to_dict(cur.fetchone(), cur)
            return jsonify(row or {"printer": None})
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/printer/default: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/printers/list")
@auth.require_page_token_or_session("bom")
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
            rows = db.fetch_all_dict(cur)
            logger.info("/api/printers/list restituisce %s righe", len(rows))
            return jsonify(rows)
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/printers/list: %s", e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/linked_materials/current")
@auth.require_page_token_or_session("bom")
def api_current_linked_material():
    label_id = request.args.get("label_id", type=int)
    if not label_id:
        return jsonify({"error": "missing_label_id"}), 400
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT TOP 1 lm.LinkedMaterialId, lm.RibbonId,
                          r.DescrizioneMateriale AS RibbonDescription
                   FROM Traceability_RS.dbo.LinkedMaterials lm
                   LEFT JOIN Traceability_RS.ind.Materiali r ON r.MaterialeId = lm.RibbonId
                   WHERE lm.LabelId = ? AND lm.dateout IS NULL
                   ORDER BY lm.dateIn DESC""",
                (label_id,),
            )
            row = db.row_to_dict(cur.fetchone(), cur)
            return jsonify(row or {})
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/linked_materials/current label_id=%s: %s", label_id, e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/label_printer_association/current")
@auth.require_page_token_or_session("bom")
def api_current_label_printer_association():
    label_id = request.args.get("label_id", type=int)
    if not label_id:
        return jsonify({"error": "missing_label_id"}), 400
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT TOP 1 lpa.LabelPrinterAssociationId, lpa.LabelPrinterId,
                          p.PrinterName, p.PrinterType, p.ConnectionString,
                          p.PrinterIP, p.PrinterPort, p.PrinterLocation, p.PrinterModel,
                          p.LastRevisionDate
                   FROM Traceability_RS.dbo.LabelPrinterAssociations lpa
                   LEFT JOIN Traceability_RS.ind.LabelPrinters p ON p.LabelPrinterId = lpa.LabelPrinterId AND p.DateOut IS NULL
                   WHERE lpa.LabelId = ? AND lpa.dateout IS NULL
                   ORDER BY lpa.dateIn DESC""",
                (label_id,),
            )
            row = db.row_to_dict(cur.fetchone(), cur)
            return jsonify(row or {})
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/label_printer_association/current label_id=%s: %s", label_id, e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/linked_materials", methods=["POST"])
@auth.require_page_token_or_session("bom")
def api_save_linked_material():
    data = request.get_json(silent=True) or {}
    label_id = data.get("label_id")
    ribbon_id = data.get("ribbon_id")
    if not label_id or not ribbon_id:
        return jsonify({"error": "missing_parameters"}), 400

    user = auth.get_session_user()["user_name"]
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE Traceability_RS.dbo.LinkedMaterials
               SET dateout = GETDATE()
               WHERE LabelId = ? AND dateout IS NULL""",
            (label_id,),
        )
        cur.execute(
            """INSERT INTO Traceability_RS.dbo.LinkedMaterials
               (LabelId, RibbonId, dateIn, [User])
               VALUES (?, ?, GETDATE(), ?)""",
            (label_id, ribbon_id, user),
        )
        cur.execute(
            """SELECT LinkedMaterialId
               FROM Traceability_RS.dbo.LinkedMaterials
               WHERE LabelId = ? AND RibbonId = ? AND dateout IS NULL""",
            (label_id, ribbon_id),
        )
        linked_id = cur.fetchone()
        conn.commit()
        return jsonify({"ok": True, "linked_material_id": linked_id[0] if linked_id else None})
    except Exception as e:
        logger.exception("Errore salvataggio associazione: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


@bom_bp.route("/api/label_printer_association", methods=["POST"])
@auth.require_page_token_or_session("bom")
def api_save_label_printer_association():
    data = request.get_json(silent=True) or {}
    label_id = data.get("label_id")
    printer_id = data.get("printer_id")
    if not label_id or not printer_id:
        return jsonify({"error": "missing_parameters"}), 400

    user = auth.get_session_user()["user_name"]
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE Traceability_RS.dbo.LabelPrinterAssociations
               SET dateout = GETDATE()
               WHERE LabelId = ? AND dateout IS NULL""",
            (label_id,),
        )
        cur.execute(
            """INSERT INTO Traceability_RS.dbo.LabelPrinterAssociations
               (LabelId, LabelPrinterId, dateIn, [User])
               VALUES (?, ?, GETDATE(), ?)""",
            (label_id, printer_id, user),
        )
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        logger.exception("Errore salvataggio associazione label-stampante: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()


@bom_bp.route("/api/label_bom")
@auth.require_page_token_or_session("bom")
def api_label_bom():
    label_id = request.args.get("label_id", type=int)
    if not label_id:
        return jsonify({"error": "missing_label_id"}), 400
    try:
        conn = db.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT TOP 1 BomIndirectMaterialId
                   FROM Traceability_RS.ind.BomIndirectMaterials
                   WHERE MaterialeID = ? AND DateOut IS NULL
                   ORDER BY DateIn DESC""",
                (label_id,),
            )
            row = cur.fetchone()
            return jsonify({"bom_id": row[0] if row else None})
        finally:
            conn.close()
    except Exception as e:
        logger.exception("Errore /api/label_bom label_id=%s: %s", label_id, e)
        return jsonify({"error": "db_error", "message": str(e)}), 500


@bom_bp.route("/api/bom/script", methods=["GET", "POST"])
@auth.require_page_token_or_session("bom")
def api_bom_script():
    if request.method == "GET":
        bom_id = request.args.get("bom_id", type=int)
        if not bom_id:
            return jsonify({"error": "missing_bom_id"}), 400
        try:
            conn = db.get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """SELECT TOP (1) LabelScriptId, ScriptToPrint
                       FROM Traceability_RS.ind.LabelScripts
                       WHERE BomIndirectMaterialId = ? AND DateOut IS NULL
                       ORDER BY DateIn DESC""",
                    (bom_id,),
                )
                row = db.row_to_dict(cur.fetchone(), cur)
                return jsonify({"script": row["ScriptToPrint"] if row else ""})
            finally:
                conn.close()
        except Exception as e:
            logger.exception("Errore lettura script bom_id=%s: %s", bom_id, e)
            return jsonify({"error": "db_error", "message": str(e)}), 500

    data = request.get_json(silent=True) or {}
    bom_id = data.get("bom_id")
    script = data.get("script", "")
    if not bom_id:
        return jsonify({"error": "missing_bom_id"}), 400

    user = auth.get_session_user()["user_name"]
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT LabelScriptId
               FROM Traceability_RS.ind.LabelScripts
               WHERE BomIndirectMaterialId = ? AND DateOut IS NULL AND ScriptToPrint = ?""",
            (bom_id, script),
        )
        if cur.fetchone():
            return jsonify({"error": "duplicate_script", "message": "Script già attivo con lo stesso contenuto."}), 409

        cur.execute(
            """UPDATE Traceability_RS.ind.LabelScripts
               SET DateOut = GETDATE()
               WHERE BomIndirectMaterialId = ? AND DateOut IS NULL""",
            (bom_id,),
        )
        cur.execute(
            """INSERT INTO Traceability_RS.ind.LabelScripts
               (BomIndirectMaterialId, ScriptToPrint, DateIn, [User])
               VALUES (?, ?, GETDATE(), ?)""",
            (bom_id, script, user),
        )
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        logger.exception("Errore salvataggio script: %s", e)
        conn.rollback()
        return jsonify({"error": "db_error", "message": str(e)}), 500
    finally:
        conn.close()
