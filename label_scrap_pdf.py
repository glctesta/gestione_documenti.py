# -*- coding: utf-8 -*-
"""
label_scrap_pdf.py — generazione PDF per gli scarti etichette.

- generate_declaration_pdf: riepilogo della dichiarazione di un operatore
  (usato alla chiusura della form e dalla stampa forzata di fine turno).
- generate_report_pdf: report professionale con logo per la voce "Report".
- print_pdf: invia un PDF alla stampante predefinita del PC.

Riusa il pattern logo/reportlab di orders/shipment_pdf.py.
"""
import os
import sys
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_logo_path():
    """Trova Logo.png sia da sorgente sia dall'eseguibile compilato (PyInstaller
    onedir: accanto all'exe o in _internal; onefile: _MEIPASS)."""
    bases = [os.path.dirname(os.path.abspath(__file__))]
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        bases += [exe_dir, os.path.join(exe_dir, '_internal')]
    mei = getattr(sys, '_MEIPASS', None)
    if mei:
        bases.append(mei)
    names = ["Logo.png", "logo.png", os.path.join("docs", "Logo.png")]
    for b in bases:
        for n in names:
            p = os.path.join(b, n)
            if os.path.isfile(p):
                return p
    logger.warning("Logo.png non trovato (percorsi controllati: %s)", bases)
    return None


def get_warehouse_responsible(conn):
    """Nome del responsabile magazzino (Logistica, CdcId=3, FunctionCode>61).
    Ritorna la stringa nome o '' se non trovato. Richiede una connessione pyodbc."""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT TOP 1 Employees.EmployeeSurname + ' ' + Employees.EmployeeName AS Employee
            FROM Employee.dbo.EmployeeHireHistory
            INNER JOIN Employee.dbo.Employees
                ON EmployeeHireHistory.EmployeeId = Employees.EmployeeId
            INNER JOIN Employee.dbo.EmployeeCdcStories
                ON EmployeeCdcStories.EmployeeHireHistoryId = EmployeeHireHistory.EmployeeHireHistoryId
            INNER JOIN Employee.dbo.CdcSub ON EmployeeCdcStories.SubCdcId = CdcSub.SubCdcId
            INNER JOIN Employee.dbo.CostCenters ON CdcSub.CdcId = CostCenters.CdcId
            INNER JOIN Employee.dbo.Functions ON EmployeeCdcStories.FunctionId = Functions.FunctionId
            INNER JOIN resetservices.dbo.tbuserkey k ON Employees.employeeid = k.idanga
            INNER JOIN Employee.dbo.EmployeeAddress A
                ON A.EmployeeId = Employees.EmployeeId AND A.DateOut IS NULL
            WHERE EmployeeHireHistory.EmployeerId = 2
              AND EmployeeHireHistory.EndWorkDate IS NULL
              AND EmployeeCdcStories.DateOut IS NULL
              AND CostCenters.cdcid = 3 AND Functions.FunctionCode > 61
        """)
        row = cur.fetchone()
        cur.close()
        return (row[0] or '') if row else ''
    except Exception as e:
        logger.error(f"get_warehouse_responsible: {e}", exc_info=True)
        return ''


def _draw_signatures(c, f, width, operator, warehouse_responsible, y=None):
    """Disegna due riquadri firma: operatore dichiarante e responsabile magazzino."""
    from reportlab.lib.units import cm
    if y is None:
        y = 3.6 * cm
    col_w = (width - 4 * cm) / 2
    for i, (title, name) in enumerate((
            ("Operatore (dichiarante)", operator or ''),
            ("Responsabile magazzino", warehouse_responsible or ''))):
        x = 2 * cm + i * col_w
        c.setFont(f["b"], 9)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawString(x, y, title)
        c.setFont(f["n"], 10)
        c.drawString(x, y - 0.55 * cm, name)
        # linea per la firma
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.6)
        c.line(x, y - 1.5 * cm, x + col_w - 1 * cm, y - 1.5 * cm)
        c.setFont(f["n"], 8)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(x, y - 1.9 * cm, "Firma")


def _register_font():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    out = {"n": "Helvetica", "b": "Helvetica-Bold"}
    try:
        if "LSArial" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("LSArial", "C:/Windows/Fonts/arial.ttf"))
        out["n"] = "LSArial"
    except Exception:
        pass
    try:
        if "LSArialB" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("LSArialB", "C:/Windows/Fonts/arialbd.ttf"))
        out["b"] = "LSArialB"
    except Exception:
        pass
    return out


def print_pdf(pdf_path):
    """Invia un PDF alla stampante predefinita (best-effort)."""
    try:
        os.startfile(pdf_path, 'print')
        logger.info(f"Label scrap PDF inviato in stampa: {pdf_path}")
        return True
    except Exception as e:
        logger.error(f"Errore stampa PDF {pdf_path}: {e}", exc_info=True)
        try:
            os.startfile(pdf_path)
        except Exception:
            pass
        return False


def _draw_header(c, f, width, height, title, subtitle):
    from reportlab.lib.units import cm
    logo = _get_logo_path()
    if logo:
        try:
            c.drawImage(logo, 2 * cm, height - 3.0 * cm, width=4 * cm,
                        preserveAspectRatio=True, mask='auto')
        except Exception as e:
            logger.warning(f"Logo non caricato: {e}")
    c.setFont(f["b"], 16)
    c.drawCentredString(width / 2, height - 2.1 * cm, title)
    if subtitle:
        c.setFont(f["n"], 10)
        c.drawCentredString(width / 2, height - 2.8 * cm, subtitle)
    c.setStrokeColorRGB(0.1, 0.32, 0.55)
    c.setLineWidth(1)
    c.line(2 * cm, height - 3.4 * cm, width - 2 * cm, height - 3.4 * cm)
    return height - 4.0 * cm


def _table(c, f, x, y, headers, rows, col_w, width, height, row_h=0.62):
    """Disegna una tabella semplice con intestazione colorata; ritorna la Y finale.
    Gestisce il salto pagina."""
    from reportlab.lib.units import cm

    def head():
        c.setFillColorRGB(0.1, 0.32, 0.55)
        c.rect(x, cy - row_h * cm, sum(col_w) * cm, row_h * cm, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont(f["b"], 9)
        cx = x
        for h, w in zip(headers, col_w):
            c.drawString(cx + 0.15 * cm, cy - row_h * cm + 0.18 * cm, str(h))
            cx += w * cm

    cy = y
    head()
    cy -= row_h * cm
    c.setFont(f["n"], 9)
    for i, r in enumerate(rows):
        if cy < 2.5 * cm:  # nuova pagina
            c.showPage()
            cy = height - 2 * cm
            head()
            cy -= row_h * cm
            c.setFont(f["n"], 9)
        if i % 2 == 0:
            c.setFillColorRGB(0.95, 0.96, 0.98)
            c.rect(x, cy - row_h * cm, sum(col_w) * cm, row_h * cm, fill=1, stroke=0)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        cx = x
        for val, w in zip(r, col_w):
            c.drawString(cx + 0.15 * cm, cy - row_h * cm + 0.18 * cm, str(val)[:int(w * 2.0)])
            cx += w * cm
        cy -= row_h * cm
    return cy


def generate_declaration_pdf(pdf_path, operator, scrap_date, rows, warehouse_responsible=''):
    """Riepilogo dichiarazione scarti etichette di un operatore, con riquadri firma
    (operatore dichiarante + responsabile magazzino).
    rows: lista di dict con keys: label, reason, category, time.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm

    f = _register_font()
    width, height = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)
    date_str = scrap_date.strftime('%d/%m/%Y') if hasattr(scrap_date, 'strftime') else str(scrap_date)
    y = _draw_header(c, f, width, height, "Declarare rebuturi etichete",
                     "Scarti etichette — riepilogo dichiarazione")

    c.setFont(f["n"], 10)
    c.drawString(2 * cm, y, f"Operatore: {operator}")
    c.drawRightString(width - 2 * cm, y, f"Data: {date_str}")
    y -= 0.5 * cm
    c.drawString(2 * cm, y, f"Totale etichette dichiarate: {len(rows)}")
    c.drawRightString(width - 2 * cm, y,
                      f"Generato: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 0.8 * cm

    data = [(i + 1, r.get('label', ''), r.get('reason', ''),
             r.get('category', ''), r.get('time', '')) for i, r in enumerate(rows)]
    y = _table(c, f, 2 * cm, y, ["#", "Etichetta", "Motivo", "Categoria", "Ora"],
               data, [1.0, 6.5, 5.0, 2.5, 2.0], width, height)

    # Riquadri firma in fondo alla pagina (se lo spazio è poco, nuova pagina).
    if y < 5.5 * cm:
        c.showPage()
    _draw_signatures(c, f, width, operator, warehouse_responsible)

    c.setFont(f["n"], 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(2 * cm, 1.2 * cm, "TraceabilityRS — documento generato automaticamente")
    c.save()
    return pdf_path


def generate_report_pdf(pdf_path, date_from, date_to, operator_filter, detail_rows,
                        by_reason, by_category, by_operator, warehouse_responsible=''):
    """Report scarti etichette con logo, dettaglio + riepiloghi.
    detail_rows: (date, operator, label, reason, category, shift)
    by_reason/by_category/by_operator: liste di (label, count).
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm

    f = _register_font()
    width, height = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)
    df = date_from.strftime('%d/%m/%Y') if hasattr(date_from, 'strftime') else str(date_from)
    dt = date_to.strftime('%d/%m/%Y') if hasattr(date_to, 'strftime') else str(date_to)
    y = _draw_header(c, f, width, height, "Report rebuturi etichete",
                     f"Scarti etichette — {df} → {dt}")

    c.setFont(f["n"], 10)
    c.drawString(2 * cm, y, f"Operatore: {operator_filter or 'Tutti'}")
    c.drawRightString(width - 2 * cm, y, f"Totale: {len(detail_rows)}")
    y -= 0.7 * cm

    # riepiloghi
    def summary(title, items, x):
        yy = y
        c.setFont(f["b"], 10)
        c.setFillColorRGB(0.1, 0.32, 0.55)
        c.drawString(x, yy, title)
        yy -= 0.45 * cm
        c.setFont(f["n"], 9)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        for lbl, cnt in items[:12]:
            c.drawString(x, yy, f"{str(lbl)[:28]}: {cnt}")
            yy -= 0.4 * cm
        return yy

    y1 = summary("Per motivo", by_reason, 2 * cm)
    y2 = summary("Per categoria", by_category, 8 * cm)
    y3 = summary("Per operatore", by_operator, 13.5 * cm)
    y = min(y1, y2, y3) - 0.3 * cm

    data = [(d[0].strftime('%d/%m/%Y') if hasattr(d[0], 'strftime') else str(d[0]),
             str(d[1])[:18], str(d[2])[:20], str(d[3])[:22], d[4], d[5] or '')
            for d in detail_rows]
    y = _table(c, f, 2 * cm, y,
               ["Data", "Operatore", "Etichetta", "Motivo", "Cat.", "Turno"],
               data, [2.2, 3.0, 3.4, 3.8, 2.0, 1.6], width, height)

    # Riquadri firma (operatore filtrato + responsabile magazzino)
    if y < 5.5 * cm:
        c.showPage()
    _draw_signatures(c, f, width, operator_filter or '', warehouse_responsible)

    c.setFont(f["n"], 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(2 * cm, 1.2 * cm,
                 f"TraceabilityRS — generato il {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.save()
    return pdf_path

