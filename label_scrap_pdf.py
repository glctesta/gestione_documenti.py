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


# Famiglia materiali indiretti che raccoglie le etichette (ind.FamigliaMateriali).
# Stesso valore usato dalla dichiarazione scarti in label_scrap_gui.py.
LABEL_FAMILY_ID = 1


def fetch_labels_vs_withdrawn(conn, date_from, date_to, family_id=LABEL_FAMILY_ID):
    """Etichette prelevate dal magazzino nel periodo, per materiale, con la quota
    finita a scarto.

    Il totale degli scarti da solo non dice se sono tanti o pochi: serve il
    confronto con quanto e' stato ritirato dal magazzino nello stesso periodo.

    Prelevato = richieste materiali indiretti in stato PRELEVATA con DataPrelievo
    nel periodo. Si usano le richieste e non i movimenti di SCARICO perche' il
    ledger dei movimenti e' partito dopo ed e' vuoto per i mesi precedenti,
    mentre le richieste coprono tutto lo storico.

    Il dato NON e' per operatore (i prelievi non sono attribuiti a chi scarta):
    va sempre letto sul totale del periodo.

    Ritorna (rows, totals):
      rows   = [(codice, descrizione, prelevate, scartate, perc), ...]
      totals = (prelevate, scartate, perc)
    """
    sql = """
        WITH prelievi AS (
            SELECT r.MaterialeId, SUM(r.QtaRichiesta) AS Qta
            FROM ind.MaterialiRichieste r
            WHERE r.Stato = 'PRELEVATA'
              AND r.DataPrelievo >= ? AND r.DataPrelievo < DATEADD(day, 1, ?)
            GROUP BY r.MaterialeId
        ), scarti AS (
            SELECT ls.MaterialeId, SUM(ISNULL(ls.Qty, 1)) AS Qta
            FROM traceability_rs.dbo.labelscrap ls
            WHERE ls.ScrapDate BETWEEN ? AND ? AND ls.MaterialeId IS NOT NULL
            GROUP BY ls.MaterialeId
        )
        SELECT M.CodiceMateriale, ISNULL(M.DescrizioneMateriale, '') AS Descr,
               ISNULL(p.Qta, 0) AS Prelevate, ISNULL(s.Qta, 0) AS Scartate
        FROM ind.Materiali M
        LEFT JOIN prelievi p ON p.MaterialeId = M.MaterialeId
        LEFT JOIN scarti   s ON s.MaterialeId = M.MaterialeId
        WHERE M.FamigliaMaterialiId = ?
          AND (p.Qta IS NOT NULL OR s.Qta IS NOT NULL)
        ORDER BY ISNULL(s.Qta, 0) DESC, M.CodiceMateriale
    """
    rows = []
    try:
        cur = conn.cursor()
        cur.execute(sql, (date_from, date_to, date_from, date_to, family_id))
        for r in cur.fetchall():
            taken = int(r.Prelevate or 0)
            scrapped = int(r.Scartate or 0)
            rows.append((r.CodiceMateriale, r.Descr, taken, scrapped,
                         (scrapped / taken * 100.0) if taken else 0.0))
        cur.close()
    except Exception as e:
        logger.error(f"fetch_labels_vs_withdrawn: {e}", exc_info=True)
        raise
    tot_taken = sum(v[2] for v in rows)
    tot_scrap = sum(v[3] for v in rows)
    return rows, (tot_taken, tot_scrap,
                  (tot_scrap / tot_taken * 100.0) if tot_taken else 0.0)


def _draw_signatures(c, f, width, operator, warehouse_responsible, y=None):
    """Due riquadri firma (in rumeno): operatore dichiarante e responsabile magazzino."""
    from reportlab.lib.units import cm
    if y is None:
        y = 3.6 * cm
    col_w = (width - 4 * cm) / 2
    for i, (title, name) in enumerate((
            ("Operator (declarant)", operator or ''),
            ("Responsabil depozit", warehouse_responsible or ''))):
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
        c.drawString(x, y - 1.9 * cm, "Semnătura")


# Categorie mostrate in rumeno nel documento
_CATEGORY_RO = {'Production': 'Producție', 'Print': 'Tipărire'}

# Clausola di responsabilità (rumeno). {op} = nome operatore.
_DISCLAIMER_RO = (
    "Subsemnatul {op} declar pe propria răspundere că am depus maximă diligență în "
    "manipularea etichetelor și că sunt conștient că acestea constituie un bun cu un "
    "cost ridicat. Sunt conștient că, în caz de neglijență, gestionare necorespunzătoare "
    "și mai ales ca urmare a nerespectării procedurilor de producție și de utilizare a "
    "imprimantei — pe care declar că le-am însușit și înțeles — pot fi obligat să acopăr, "
    "în solidar, contravaloarea bunurilor deteriorate sau distruse.")


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

    def fit(txt, w_cm, font):
        """Taglia il testo alla larghezza REALE della colonna.

        Prima si tagliava a 2 caratteri per centimetro: una stima grossolana che
        riduceva le date a '23/0' e i nomi a 'ARNOL', ma soprattutto troncava i
        numeri ('117.4' al posto di '117.417'), rendendo il PDF non solo brutto
        ma sbagliato."""
        s = str(txt)
        avail = w_cm * cm - 0.3 * cm
        if avail <= 0:
            return ''
        while s and c.stringWidth(s, font, 9) > avail:
            s = s[:-1]
        return s

    def head():
        c.setFillColorRGB(0.1, 0.32, 0.55)
        c.rect(x, cy - row_h * cm, sum(col_w) * cm, row_h * cm, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont(f["b"], 9)
        cx = x
        for h, w in zip(headers, col_w):
            c.drawString(cx + 0.15 * cm, cy - row_h * cm + 0.18 * cm, fit(h, w, f["b"]))
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
            c.drawString(cx + 0.15 * cm, cy - row_h * cm + 0.18 * cm, fit(val, w, f["n"]))
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

    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle

    f = _register_font()
    width, height = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)
    date_str = scrap_date.strftime('%d/%m/%Y') if hasattr(scrap_date, 'strftime') else str(scrap_date)
    y = _draw_header(c, f, width, height, "Proces verbal predare-primire rebuturi etichete",
                     "Declarare rebuturi etichete")

    c.setFont(f["n"], 10)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(2 * cm, y, f"Operator: {operator}")
    c.drawRightString(width - 2 * cm, y, f"Data: {date_str}")
    y -= 0.5 * cm
    # Somma delle quantita', non conteggio righe: una riga di etichette
    # bianche puo' valerne molte. get('qty', 1) copre le righe storiche.
    total_qty = sum(int(r.get('qty', 1) or 1) for r in rows)
    c.drawString(2 * cm, y, f"Total etichete declarate: {total_qty}")
    c.drawRightString(width - 2 * cm, y,
                      f"Generat: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 0.8 * cm

    data = [(i + 1, r.get('label', ''), int(r.get('qty', 1) or 1), r.get('material', ''),
             r.get('reason', ''),
             _CATEGORY_RO.get(r.get('category', ''), r.get('category', '')),
             r.get('time', '')) for i, r in enumerate(rows)]
    y = _table(c, f, 2 * cm, y,
               ["Nr.", "Etichetă", "Cant.", "Material", "Motiv", "Categorie", "Ora"],
               data, [1.0, 3.8, 1.2, 3.2, 4.0, 2.2, 1.6], width, height)

    # Clausola di responsabilità + firme in fondo. Serve spazio: ~9 cm.
    if y < 9.5 * cm:
        c.showPage()
        y = height - 2 * cm

    style = ParagraphStyle('disc', fontName=f["n"], fontSize=9, leading=13,
                           alignment=4)  # justify
    para = Paragraph(_DISCLAIMER_RO.format(op=operator or '________'), style)
    pw, ph = para.wrap(width - 4 * cm, 6 * cm)
    y -= 0.4 * cm
    para.drawOn(c, 2 * cm, y - ph)
    y -= ph + 1.2 * cm

    if y < 3.5 * cm:
        c.showPage()
        y = height - 3 * cm
    _draw_signatures(c, f, width, operator, warehouse_responsible, y=y)

    c.setFont(f["n"], 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(2 * cm, 1.2 * cm, "TraceabilityRS — document generat automat")
    c.save()
    return pdf_path


def generate_report_pdf(pdf_path, date_from, date_to, operator_filter, detail_rows,
                        by_reason, by_category, by_operator, warehouse_responsible='',
                        vs_rows=None, vs_totals=None):
    """Report scarti etichette con logo, dettaglio + riepiloghi.
    detail_rows: (date, operator, label, reason, category, shift, qty, materiale)
    by_reason/by_category/by_operator: liste di (label, quantita').
    vs_rows: (codice, descrizione, prelevate, scartate, perc) — scarti a fronte
        del prelevato dal magazzino nel periodo; vs_totals: (prelevate, scartate, perc).
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

    total_qty = sum(int(d[6]) for d in detail_rows if len(d) > 6)
    c.setFont(f["n"], 10)
    c.drawString(2 * cm, y, f"Operatore: {operator_filter or 'Tutti'}")
    c.drawRightString(width - 2 * cm, y,
                      f"Righe: {len(detail_rows)}   Etichette scartate: {total_qty}")
    y -= 0.7 * cm

    # Scarti a fronte del prelevato dal magazzino: e' il dato che dice se gli
    # scarti sono tanti o pochi, il totale da solo non lo dice.
    if vs_rows:
        c.setFont(f["b"], 10)
        c.setFillColorRGB(0.1, 0.32, 0.55)
        c.drawString(2 * cm, y, "Scarti a fronte del prelevato dal magazzino")
        c.setFillColorRGB(0.1, 0.1, 0.1)
        y -= 0.45 * cm
        vdata = [(code, descr, f"{taken:,}".replace(',', '.'),
                  f"{scrapped:,}".replace(',', '.'), f"{rate:.2f}%" if taken else '-')
                 for code, descr, taken, scrapped, rate in vs_rows]
        if vs_totals:
            t_taken, t_scrap, t_rate = vs_totals
            vdata.append(("TOTALE", "", f"{t_taken:,}".replace(',', '.'),
                          f"{t_scrap:,}".replace(',', '.'),
                          f"{t_rate:.2f}%" if t_taken else '-'))
        y = _table(c, f, 2 * cm, y,
                   ["Materiale", "Descrizione", "Prelevate", "Scartate", "% scarto"],
                   vdata, [3.4, 6.4, 2.6, 2.6, 2.0], width, height)
        y -= 0.25 * cm
        c.setFont(f["n"], 7.5)
        c.setFillColorRGB(0.45, 0.45, 0.45)
        c.drawString(2 * cm, y, "Prelievi = richieste materiali indiretti in stato "
                                "PRELEVATA nel periodo (tutti gli operatori).")
        c.setFillColorRGB(0.1, 0.1, 0.1)
        y -= 0.6 * cm

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

    # I riepiloghi sono in ETICHETTE (somma delle quantita'), non in righe
    y1 = summary("Per motivo (etichette)", by_reason, 2 * cm)
    y2 = summary("Per categoria (etichette)", by_category, 8 * cm)
    y3 = summary("Per operatore (etichette)", by_operator, 13.5 * cm)
    y = min(y1, y2, y3) - 0.3 * cm

    data = [(d[0].strftime('%d/%m/%Y') if hasattr(d[0], 'strftime') else str(d[0]),
             d[1], d[2], str(d[6]) if len(d) > 6 else '',
             d[7] if len(d) > 7 else '',
             d[3], d[4], d[5] or '')
            for d in detail_rows]
    # Le larghezze sommano a 17 cm = A4 meno i margini di 2 cm per lato
    y = _table(c, f, 2 * cm, y,
               ["Data", "Operatore", "Etichetta", "Q.tà", "Materiale", "Motivo", "Cat.", "Turno"],
               data, [2.0, 2.8, 2.6, 1.2, 2.4, 3.0, 1.6, 1.4], width, height)

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

