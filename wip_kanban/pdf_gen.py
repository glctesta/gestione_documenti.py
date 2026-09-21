# -*- coding: utf-8 -*-
"""
pdf_gen.py — Generazione PDF per il kanban (pattern orders/shipment_pdf.py).

- labels_pdf: 16 pagine A5 (una per posizione): nome posizione grande + QR sotto.
- list_pdf:   lista schede raggruppata per posizione (alfabetico), con logo.
"""
import os
import io
import tempfile
import logging
from datetime import datetime

import qrcode
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import ParagraphStyle

logger = logging.getLogger("WipKanban")

_FONT = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"


def _register_font():
    """Registra Arial (supporta diacritiche rumene); fallback Helvetica."""
    global _FONT, _FONT_BOLD
    for path, name in (("C:/Windows/Fonts/arial.ttf", "KanbanArial"),
                       ("C:/Windows/Fonts/arialbd.ttf", "KanbanArial-Bold")):
        if os.path.isfile(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
            except Exception:
                return
    _FONT, _FONT_BOLD = "KanbanArial", "KanbanArial-Bold"


def _logo_path():
    base = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(base, "static", "Logo.png"),
              os.path.join(base, "..", "Logo.png"),
              os.path.join(base, "..", "logo.png")):
        if os.path.isfile(p):
            return p
    return None


_register_font()


def _qr_image(code: str, box_px: int = 8) -> ImageReader:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box_px, border=2)
    qr.add_data(code)
    qr.make(fit=True)
    buf = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def labels_pdf(positions, user_note=""):
    """PDF A5 con una pagina per posizione: codice grande + QR sotto.

    positions: lista di codici posizione (es. ['WP1A1', ..., 'WP1D4']).
    Restituisce il path del file temporaneo."""
    path = os.path.join(tempfile.gettempdir(), f"kanban_labels_{datetime.now():%Y%m%d_%H%M%S}.pdf")
    w, h = A5  # 420 x 595 pt (148 x 210 mm)
    c = canvas.Canvas(path, pagesize=A5)

    for pos in positions:
        c.setFont(_FONT_BOLD, 72)
        c.drawCentredString(w / 2, h - 90 * mm, pos)

        c.setFont(_FONT, 14)
        c.drawCentredString(w / 2, h - 100 * mm, "KANBAN")

        qr = _qr_image(pos)
        qr_size = 55 * mm
        c.drawImage(qr, (w - qr_size) / 2, h - 100 * mm - qr_size - 10 * mm,
                    width=qr_size, height=qr_size)

        if user_note:
            c.setFont(_FONT, 10)
            c.drawCentredString(w / 2, 15 * mm, user_note)

        c.showPage()

    c.save()
    return path


def list_pdf(rows, title, subtitle=""):
    """Lista schede attive raggruppata per posizione (ordine alfabetico).

    rows: dict con chiavi PositionCode, LabelCode, OrderNumber, ProductCode,
          ScanResult, PhaseName, ScanTimeFinish, LoadedBy, DateIn.
    Restituisce il path del file temporaneo."""
    path = os.path.join(tempfile.gettempdir(), f"kanban_list_{datetime.now():%Y%m%d_%H%M%S}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm)

    style_title = ParagraphStyle("t", fontName=_FONT_BOLD, fontSize=15)
    style_sub = ParagraphStyle("s", fontName=_FONT, fontSize=9, textColor=colors.HexColor("#555555"))
    style_hdr = ParagraphStyle("h", fontName=_FONT_BOLD, fontSize=11, spaceBefore=8, spaceAfter=3)

    story = []
    logo = _logo_path()
    if logo:
        story.append(RLImage(logo, width=30 * mm, height=12 * mm))
    story.append(Paragraph(title, style_title))
    if subtitle:
        story.append(Paragraph(subtitle, style_sub))
    story.append(Spacer(1, 6 * mm))

    data = [["Posizione", "LabelCode", "Prodotto", "Ordine", "Esito", "Fase", "Ultima scansione"]]
    prev_pos = None
    group_rows = []
    for idx, r in enumerate(rows, start=1):
        pos = r.get("PositionCode") or ""
        if pos != prev_pos:
            data.append([f"Posizione {pos}", "", "", "", "", "", ""])
            group_rows.append(idx)
            prev_pos = pos
        data.append([
            "",
            r.get("LabelCode") or "",
            (r.get("ProductCode") or "")[:28],
            r.get("OrderNumber") or "",
            r.get("ScanResult") or "-",
            r.get("PhaseName") or "-",
            r.get("ScanTimeFinish").strftime("%d/%m/%Y %H:%M") if r.get("ScanTimeFinish") else "-",
        ])

    table = Table(data, colWidths=[22 * mm, 34 * mm, 48 * mm, 26 * mm, 14 * mm, 36 * mm, 32 * mm])
    style = [
        ("FONTNAME", (0, 0), (-1, -1), _FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5f2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), _FONT_BOLD),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbbbbb")),
        ("ROWBACKGROUNDS", (1, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7f4")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    for g in group_rows:
        style += [("SPAN", (0, g), (-1, g)),
                  ("FONTNAME", (0, g), (-1, g), _FONT_BOLD),
                  ("BACKGROUND", (0, g), (-1, g), colors.HexColor("#dce8dc"))]
    table.setStyle(TableStyle(style))
    story.append(table)

    doc.build(story)
    return path
