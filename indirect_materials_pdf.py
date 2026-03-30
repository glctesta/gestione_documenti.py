"""
indirect_materials_pdf.py
Genera il PDF "CERERE DE MATERIAL DE CONSUM" in rumeno.
"""

import os
import sys
import logging
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_logo_path():
    """Trova il percorso Logo.png."""
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, "Logo.png"),
        os.path.join(base, "docs", "Logo.png"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


def generate_request_pdf(db, richiesta_id):
    """
    Genera il PDF per una richiesta e restituisce il percorso del file.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import Table, TableStyle, Paragraph, Image as RLImage
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # Registra font con supporto caratteri rumeni
    try:
        pdfmetrics.registerFont(TTFont('ArialUnicode', 'C:/Windows/Fonts/arial.ttf'))
        font_name = 'ArialUnicode'
    except Exception:
        font_name = 'Helvetica'

    # Carica dati richiesta
    query = """
        SELECT r.RichiestaId, r.DataRichiesta, r.QtaRichiesta,
               r.Stato, r.RichiestoDa, r.PreparatoDa,
               m.CodiceMateriale, m.DescrizioneMateriale,
               r.QtaStockAlMomento, r.Note
        FROM ind.MaterialiRichieste r
        JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
        WHERE r.RichiestaId = ?
    """
    row = db.fetch_one(query, (richiesta_id,))
    if not row:
        raise ValueError(f"Richiesta {richiesta_id} non trovata")

    rid = row[0]
    data_richiesta = row[1]
    qty = row[2]
    stato = row[3]
    richiedente = row[4] or ''
    preparatore = row[5] or ''
    codice = row[6] or ''
    descrizione = row[7] or ''
    stock = row[8]
    note = row[9] or ''

    # Genera PDF in temp
    pdf_dir = os.path.join(tempfile.gettempdir(), "ind_materials")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"cerere_material_{rid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Logo
    logo_path = _get_logo_path()
    if logo_path:
        try:
            c.drawImage(logo_path, 2 * cm, height - 3.5 * cm, width=4 * cm, preserveAspectRatio=True)
        except Exception as e:
            logger.warning(f"Impossibile caricare logo: {e}")

    # Titolo
    c.setFont(font_name, 18)
    c.drawCentredString(width / 2, height - 4.5 * cm, "CERERE DE MATERIAL DE CONSUM")

    c.setFont(font_name, 10)
    c.drawCentredString(width / 2, height - 5.2 * cm, f"Nr. {rid}")

    # Data e ora
    y = height - 6.5 * cm
    c.setFont(font_name, 11)
    data_str = data_richiesta.strftime('%d/%m/%Y %H:%M') if data_richiesta else ''
    c.drawString(2 * cm, y, f"Data și ora cererii: {data_str}")

    # Tabella materiale
    y -= 1.5 * cm
    table_data = [
        ['Cod Material', 'Descriere', 'Cantitate solicitată', 'Stoc la momentul cererii'],
        [codice, descrizione, f"{qty:.2f}", f"{stock:.2f}" if stock else '-']
    ]

    t = Table(table_data, colWidths=[3.5 * cm, 7 * cm, 3.5 * cm, 4 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    t_width, t_height = t.wrap(width, height)
    t.drawOn(c, 2 * cm, y - t_height)

    # Info sotto tabella
    y = y - t_height - 1.5 * cm
    c.setFont(font_name, 11)
    c.drawString(2 * cm, y, f"Solicitant: {richiedente}")

    y -= 0.8 * cm
    c.drawString(2 * cm, y, f"Pregătit de: {preparatore if preparatore else '___________________'}")

    if note:
        y -= 0.8 * cm
        c.drawString(2 * cm, y, f"Note: {note}")

    # Firme
    y -= 2.5 * cm
    c.setFont(font_name, 10)
    c.drawString(2 * cm, y, "Semnătura solicitant:")
    c.drawString(11 * cm, y, "Semnătura predare:")

    y -= 0.5 * cm
    c.drawString(2 * cm, y, "___________________")
    c.drawString(11 * cm, y, "___________________")

    # Footer
    c.setFont(font_name, 8)
    c.drawCentredString(width / 2, 1.5 * cm, f"Generat automat - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    c.save()
    logger.info(f"PDF generato: {pdf_path}")
    return pdf_path


def generate_and_print_request_pdf(db, richiesta_id, print_now=True):
    """Genera PDF e lo stampa sulla stampante di default."""
    pdf_path = generate_request_pdf(db, richiesta_id)

    if print_now:
        try:
            os.startfile(pdf_path, 'print')
            logger.info(f"PDF inviato in stampa: {pdf_path}")
        except Exception as e:
            logger.error(f"Errore stampa PDF: {e}", exc_info=True)
            # Apri comunque il file
            os.startfile(pdf_path)

    return pdf_path
