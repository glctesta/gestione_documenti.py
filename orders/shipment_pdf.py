"""
orders/shipment_pdf.py

Generazione documenti PDF per la conferma spedizioni v2 (reportlab).
Due documenti, entrambi con Logo.png, data spedizione, operatore e
data/ora di generazione:

  - generate_pallet_list_pdf  -> "Lista Spedizione per Pallet" (ordinata per pallet)
  - generate_summary_pdf      -> "Riepilogo Spedizione" (tutti i pallet, totali)

I dati vengono letti dagli snapshot salvati in dyn.ShipmentPallets, cosi' le
ristampe restano stabili nel tempo. Stesso pattern di indirect_materials_pdf.py.
"""

import os
import logging
import tempfile
from datetime import datetime, date

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
#  Helper comuni
# ─────────────────────────────────────────────────────────────────────────────
def _get_logo_path():
    """Trova il percorso Logo.png (root progetto o docs/)."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cartella padre di orders/
    candidates = [
        os.path.join(base, "Logo.png"),
        os.path.join(base, "docs", "Logo.png"),
        os.path.join(base, "logo.png"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


def _register_font():
    """Registra Arial (caratteri estesi). Ritorna il nome font o Helvetica."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    try:
        if 'ArialUnicode' not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont('ArialUnicode', 'C:/Windows/Fonts/arial.ttf'))
        return 'ArialUnicode'
    except Exception:
        return 'Helvetica'


def _output_dir():
    """Cartella di archivio dei PDF spedizione."""
    d = os.path.join(tempfile.gettempdir(), "shipments")
    os.makedirs(d, exist_ok=True)
    return d


def _fmt_ship_date(ship_date):
    """Formatta la data spedizione (date/datetime/str) in gg/mm/aaaa."""
    if ship_date is None:
        return ""
    if isinstance(ship_date, (datetime, date)):
        return ship_date.strftime('%d/%m/%Y')
    return str(ship_date)


def _draw_header(c, font_name, width, height, title, shipment_id,
                 ship_date, operator):
    """Disegna logo + titolo + riga spedizione. Ritorna la Y sotto l'header."""
    from reportlab.lib.units import cm

    logo_path = _get_logo_path()
    if logo_path:
        try:
            c.drawImage(logo_path, 2 * cm, height - 3.2 * cm,
                        width=4 * cm, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            logger.warning(f"Impossibile caricare logo: {e}")

    c.setFont(font_name, 17)
    c.drawCentredString(width / 2, height - 2.2 * cm, title)

    c.setFont(font_name, 10)
    c.drawCentredString(
        width / 2, height - 3.0 * cm,
        f"Spedizione N. {shipment_id}  -  Data spedizione: {_fmt_ship_date(ship_date)}"
    )

    y = height - 4.2 * cm
    c.setFont(font_name, 10)
    c.drawString(2 * cm, y, f"Operatore: {operator or '-'}")
    c.drawRightString(
        width - 2 * cm, y,
        f"Generato il: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )
    y -= 0.3 * cm
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.line(2 * cm, y, width - 2 * cm, y)
    return y - 0.6 * cm


def _draw_footer(c, font_name, width):
    from reportlab.lib.units import cm
    c.setFont(font_name, 8)
    c.drawCentredString(
        width / 2, 1.2 * cm,
        f"Documento generato automaticamente da TraceabilityRS - "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Caricamento dati
# ─────────────────────────────────────────────────────────────────────────────
def _load_shipment(db, shipment_id):
    """Ritorna (header_row, pallet_rows) per la spedizione indicata."""
    cur = db.cursor
    cur.execute(
        """
        SELECT ShipmentId, ShipmentDate, Status, CreatedByUser, CreatedAt,
               ClosedByUser, ClosedAt, LastModifiedByUser, LastModifiedAt
        FROM [Traceability_RS].[dyn].[Shipments]
        WHERE ShipmentId = ?
        """,
        (shipment_id,),
    )
    header = cur.fetchone()
    if header is None:
        raise ValueError(f"Spedizione {shipment_id} non trovata")

    cur.execute(
        """
        SELECT PalletCode, ProductionOrderNumber, SONumber, CustomerName,
               ItemCode, ItemName, ShipTo, ConfirmedQty
        FROM [Traceability_RS].[dyn].[ShipmentPallets]
        WHERE ShipmentId = ?
        ORDER BY PalletCode, ProductionOrderNumber
        """,
        (shipment_id,),
    )
    pallets = cur.fetchall()
    return header, pallets


# ─────────────────────────────────────────────────────────────────────────────
#  Documento A — Lista per Pallet
# ─────────────────────────────────────────────────────────────────────────────
def generate_pallet_list_pdf(db, shipment_id, operator=None):
    """Genera il PDF 'Lista Spedizione per Pallet'. Ritorna il path."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    font_name = _register_font()
    header, pallets = _load_shipment(db, shipment_id)
    ship_date = header.ShipmentDate
    operator = operator or header.CreatedByUser

    pdf_path = os.path.join(
        _output_dir(),
        f"SHIP_{shipment_id}_pallet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = _draw_header(c, font_name, width, height,
                     "LISTA SPEDIZIONE PER PALLET", shipment_id, ship_date, operator)

    cell = ParagraphStyle('cell', fontName=font_name, fontSize=9, leading=11, wordWrap='CJK')
    hdr = ParagraphStyle('hdr', fontName=font_name, fontSize=9, leading=11,
                         textColor=colors.white, wordWrap='CJK')

    # Raggruppa per pallet
    from collections import OrderedDict
    by_pallet = OrderedDict()
    for r in pallets:
        by_pallet.setdefault(r.PalletCode, []).append(r)

    col_widths = [3.2 * cm, 3.2 * cm, 2.6 * cm, 4.8 * cm, 2.6 * cm]
    bottom_margin = 2.2 * cm

    grand_qty = 0
    for pallet_code, rows in by_pallet.items():
        pallet_qty = sum(int(x.ConfirmedQty or 0) for x in rows)
        grand_qty += pallet_qty

        # Titolo pallet
        if y < bottom_margin + 3 * cm:
            _draw_footer(c, font_name, width)
            c.showPage()
            y = _draw_header(c, font_name, width, height,
                             "LISTA SPEDIZIONE PER PALLET", shipment_id, ship_date, operator)
        c.setFont(font_name, 11)
        c.drawString(2 * cm, y, f"PALLET: {pallet_code}    (pezzi: {pallet_qty})")
        y -= 0.5 * cm

        data = [[Paragraph('Ordine Prod.', hdr), Paragraph('Ord. Vendita', hdr),
                 Paragraph('Codice', hdr), Paragraph('Prodotto', hdr),
                 Paragraph('Qta', hdr)]]
        for x in rows:
            data.append([
                Paragraph(str(x.ProductionOrderNumber or ''), cell),
                Paragraph(str(x.SONumber or ''), cell),
                Paragraph(str(x.ItemCode or ''), cell),
                Paragraph(str(x.ItemName or ''), cell),
                Paragraph(str(int(x.ConfirmedQty or 0)), cell),
            ])

        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (4, 0), (4, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        _tw, th = t.wrap(width - 4 * cm, height)
        if y - th < bottom_margin:
            _draw_footer(c, font_name, width)
            c.showPage()
            y = _draw_header(c, font_name, width, height,
                             "LISTA SPEDIZIONE PER PALLET", shipment_id, ship_date, operator)
            c.setFont(font_name, 11)
            c.drawString(2 * cm, y, f"PALLET: {pallet_code}    (pezzi: {pallet_qty})")
            y -= 0.5 * cm
        t.drawOn(c, 2 * cm, y - th)
        y = y - th - 0.8 * cm

    # Totale generale
    if y < bottom_margin + 1.5 * cm:
        _draw_footer(c, font_name, width)
        c.showPage()
        y = _draw_header(c, font_name, width, height,
                         "LISTA SPEDIZIONE PER PALLET", shipment_id, ship_date, operator)
    c.setFont(font_name, 12)
    c.drawString(2 * cm, y,
                 f"TOTALE: {len(by_pallet)} pallet  -  {grand_qty} pezzi")

    _draw_footer(c, font_name, width)
    c.save()
    logger.info(f"PDF lista pallet generato: {pdf_path}")
    return pdf_path


# ─────────────────────────────────────────────────────────────────────────────
#  Documento B — Riepilogo Spedizione
# ─────────────────────────────────────────────────────────────────────────────
def generate_summary_pdf(db, shipment_id, operator=None):
    """Genera il PDF 'Riepilogo Spedizione'. Ritorna il path."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    font_name = _register_font()
    header, pallets = _load_shipment(db, shipment_id)
    ship_date = header.ShipmentDate
    operator = operator or header.CreatedByUser

    pdf_path = os.path.join(
        _output_dir(),
        f"SHIP_{shipment_id}_riepilogo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = _draw_header(c, font_name, width, height,
                     "RIEPILOGO SPEDIZIONE", shipment_id, ship_date, operator)

    cell = ParagraphStyle('cell', fontName=font_name, fontSize=9, leading=11, wordWrap='CJK')
    hdr = ParagraphStyle('hdr', fontName=font_name, fontSize=9, leading=11,
                         textColor=colors.white, wordWrap='CJK')

    col_widths = [2.4 * cm, 3.0 * cm, 3.4 * cm, 2.4 * cm, 4.0 * cm, 1.8 * cm]
    data = [[Paragraph('Pallet', hdr), Paragraph('Ordine Prod.', hdr),
             Paragraph('Cliente', hdr), Paragraph('Codice', hdr),
             Paragraph('Prodotto', hdr), Paragraph('Qta', hdr)]]

    grand_qty = 0
    orders_seen = set()
    pallets_seen = set()
    for x in pallets:
        grand_qty += int(x.ConfirmedQty or 0)
        orders_seen.add(x.ProductionOrderNumber)
        pallets_seen.add(x.PalletCode)
        data.append([
            Paragraph(str(x.PalletCode or ''), cell),
            Paragraph(str(x.ProductionOrderNumber or ''), cell),
            Paragraph(str(x.CustomerName or ''), cell),
            Paragraph(str(x.ItemCode or ''), cell),
            Paragraph(str(x.ItemName or ''), cell),
            Paragraph(str(int(x.ConfirmedQty or 0)), cell),
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (5, 0), (5, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    # La tabella puo' eccedere la pagina: usa splitting di platypus
    avail_w = width - 4 * cm
    parts = t.split(avail_w, y - 2.2 * cm)
    if not parts:
        parts = [t]
    for idx, part in enumerate(parts):
        if idx > 0:
            _draw_footer(c, font_name, width)
            c.showPage()
            y = _draw_header(c, font_name, width, height,
                             "RIEPILOGO SPEDIZIONE", shipment_id, ship_date, operator)
        _pw, ph = part.wrap(avail_w, height)
        part.drawOn(c, 2 * cm, y - ph)
        y = y - ph - 0.6 * cm

    # Totali
    if y < 2.2 * cm + 1.5 * cm:
        _draw_footer(c, font_name, width)
        c.showPage()
        y = _draw_header(c, font_name, width, height,
                         "RIEPILOGO SPEDIZIONE", shipment_id, ship_date, operator)
    c.setFont(font_name, 12)
    c.drawString(2 * cm, y,
                 f"TOTALE GENERALE:  {len(pallets_seen)} pallet  -  "
                 f"{len(orders_seen)} ordini  -  {grand_qty} pezzi")

    _draw_footer(c, font_name, width)
    c.save()
    logger.info(f"PDF riepilogo generato: {pdf_path}")
    return pdf_path


# ─────────────────────────────────────────────────────────────────────────────
#  Entry-point combinato
# ─────────────────────────────────────────────────────────────────────────────
def generate_shipment_documents(db, shipment_id, operator=None):
    """Genera entrambi i PDF. Ritorna (pallet_pdf_path, summary_pdf_path)."""
    pallet_pdf = generate_pallet_list_pdf(db, shipment_id, operator)
    summary_pdf = generate_summary_pdf(db, shipment_id, operator)
    return pallet_pdf, summary_pdf


def print_pdf(pdf_path):
    """Invia un PDF alla stampante predefinita (best-effort)."""
    try:
        os.startfile(pdf_path, 'print')
        logger.info(f"PDF inviato in stampa: {pdf_path}")
    except Exception as e:
        logger.error(f"Errore stampa PDF {pdf_path}: {e}", exc_info=True)
        try:
            os.startfile(pdf_path)
        except Exception:
            pass
