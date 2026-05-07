"""
indirect_materials_pdf.py
Genera il PDF "CERERE DE MATERIAL DE CONSUM" in rumeno.
Supporta sia singola richiesta che batch multi-materiale in un unico documento.
"""

import os
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


def _register_font():
    """Registra font Arial con supporto caratteri rumeni. Ritorna il nome font."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    try:
        if 'ArialUnicode' not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont('ArialUnicode', 'C:/Windows/Fonts/arial.ttf'))
        return 'ArialUnicode'
    except Exception:
        return 'Helvetica'


def generate_batch_pdf(db, richiesta_ids):
    """
    Genera un unico PDF per una lista di RichiestaId.
    Tutti i materiali compaiono nella stessa tabella in un documento solo.

    Args:
        db: database handler con fetch_all o cursor
        richiesta_ids: list[int] — uno o più ID richiesta da includere

    Returns:
        str: percorso del file PDF generato
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    if not richiesta_ids:
        raise ValueError("Lista richieste vuota")

    font_name = _register_font()

    # Carica tutti i record in una sola query
    placeholders = ', '.join(['?'] * len(richiesta_ids))
    query = f"""
        SELECT r.RichiestaId, r.DataRichiesta, r.QtaRichiesta,
               r.Stato, r.RichiestoDa, r.PreparatoDa,
               m.CodiceMateriale, m.DescrizioneMateriale,
               r.QtaStockAlMomento, r.Note
        FROM ind.MaterialiRichieste r
        JOIN ind.Materiali m ON r.MaterialeId = m.MaterialeId
        WHERE r.RichiestaId IN ({placeholders})
        ORDER BY r.RichiestaId
    """
    if hasattr(db, 'fetch_all'):
        rows = db.fetch_all(query, tuple(richiesta_ids))
    else:
        db._ensure_connection()
        with db._lock:
            db.cursor.execute(query, tuple(richiesta_ids))
            rows = db.cursor.fetchall()

    if not rows:
        raise ValueError(f"Nessuna richiesta trovata per IDs: {richiesta_ids}")

    # Metadati intestazione dal primo record
    first = rows[0]
    data_richiesta = first[1]
    richiedente = first[4] or ''
    data_str = data_richiesta.strftime('%d/%m/%Y %H:%M') if data_richiesta else ''

    # Path output
    pdf_dir = os.path.join(tempfile.gettempdir(), "ind_materials")
    os.makedirs(pdf_dir, exist_ok=True)
    ids_label = '_'.join(str(r[0]) for r in rows)
    if len(ids_label) > 40:
        ids_label = ids_label[:40]
    pdf_path = os.path.join(
        pdf_dir,
        f"cerere_material_{ids_label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # ── Logo ──────────────────────────────────────────────────────────────
    logo_path = _get_logo_path()
    if logo_path:
        try:
            c.drawImage(logo_path, 2 * cm, height - 3.5 * cm,
                        width=4 * cm, preserveAspectRatio=True)
        except Exception as e:
            logger.warning(f"Impossibile caricare logo: {e}")

    # ── Titolo ────────────────────────────────────────────────────────────
    c.setFont(font_name, 18)
    c.drawCentredString(width / 2, height - 4.5 * cm, "CERERE DE MATERIAL DE CONSUM")

    nr_str = ', '.join(str(r[0]) for r in rows)
    c.setFont(font_name, 10)
    c.drawCentredString(width / 2, height - 5.2 * cm, f"Nr. {nr_str}")

    # ── Data e richiedente ────────────────────────────────────────────────
    y = height - 6.5 * cm
    c.setFont(font_name, 11)
    c.drawString(2 * cm, y, f"Data și ora cererii: {data_str}")
    y -= 0.7 * cm
    c.drawString(2 * cm, y, f"Solicitant: {richiedente}")

    # ── Tabella materiali ─────────────────────────────────────────────────
    y -= 1.2 * cm

    desc_style = ParagraphStyle(
        'DescCell', fontName=font_name, fontSize=10,
        leading=13, wordWrap='CJK', spaceAfter=0, spaceBefore=0,
    )
    hdr_style = ParagraphStyle(
        'HdrCell', fontName=font_name, fontSize=10, leading=12,
        textColor=colors.white, wordWrap='CJK',
    )

    col_widths = [3.5 * cm, 7.5 * cm, 3 * cm, 3.5 * cm]

    # Header row
    table_data = [[
        Paragraph('Cod Material', hdr_style),
        Paragraph('Descriere', hdr_style),
        Paragraph('Cantitate\nsolicitată', hdr_style),
        Paragraph('Stoc la\nmomentul cererii', hdr_style),
    ]]

    # Una riga per ogni materiale nel batch
    for row in rows:
        qty = row[2]
        stock = row[8]
        descrizione = row[7] or ''
        codice = row[6] or ''
        note = row[9] or ''
        desc_text = descrizione + (f"\n[{note}]" if note else '')
        table_data.append([
            codice,
            Paragraph(desc_text, desc_style),
            f"{qty:.2f}" if qty is not None else '-',
            f"{stock:.2f}" if stock is not None else '-',
        ])

    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 1), (3, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    t_width, t_height = t.wrap(width - 4 * cm, height)
    t.drawOn(c, 2 * cm, y - t_height)

    # ── Firme ─────────────────────────────────────────────────────────────
    y = y - t_height - 2 * cm
    c.setFont(font_name, 10)
    c.drawString(2 * cm, y, "Semnătura solicitant:")
    c.drawString(11 * cm, y, "Semnătura predare:")
    y -= 0.5 * cm
    c.drawString(2 * cm, y, "___________________")
    c.drawString(11 * cm, y, "___________________")

    # ── Footer ────────────────────────────────────────────────────────────
    c.setFont(font_name, 8)
    c.drawCentredString(
        width / 2, 1.5 * cm,
        f"Generat automat - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    c.save()
    logger.info(f"PDF generato ({len(rows)} materiali): {pdf_path}")
    return pdf_path


# ── Alias e funzioni pubbliche ─────────────────────────────────────────────

def generate_request_pdf(db, richiesta_id):
    """
    Genera PDF per una singola richiesta.
    Alias mantenuto per compatibilità con la ristampa da storico.
    """
    return generate_batch_pdf(db, [richiesta_id])


def generate_and_print_request_pdf(db, richiesta_id, print_now=True):
    """
    Genera PDF per una singola richiesta e lo stampa.
    Compatibilità: chiamato da storico (reprint singolo) e WH monitor (ristampa singola).
    """
    pdf_path = generate_batch_pdf(db, [richiesta_id])
    if print_now:
        try:
            os.startfile(pdf_path, 'print')
            logger.info(f"PDF inviato in stampa: {pdf_path}")
        except Exception as e:
            logger.error(f"Errore stampa PDF: {e}", exc_info=True)
            os.startfile(pdf_path)
    return pdf_path


def generate_and_print_batch_pdf(db, richiesta_ids, print_now=True):
    """
    Genera un unico PDF per N richieste e lo stampa una volta sola.
    Entry-point principale per il WHMonitor quando processa un batch.
    """
    if not richiesta_ids:
        return None
    pdf_path = generate_batch_pdf(db, richiesta_ids)
    if print_now:
        try:
            os.startfile(pdf_path, 'print')
            logger.info(f"PDF batch inviato in stampa ({len(richiesta_ids)} materiali): {pdf_path}")
        except Exception as e:
            logger.error(f"Errore stampa PDF batch: {e}", exc_info=True)
            os.startfile(pdf_path)
    return pdf_path
