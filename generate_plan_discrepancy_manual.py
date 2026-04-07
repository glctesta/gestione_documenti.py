# -*- coding: utf-8 -*-
"""
Genera il manuale PDF per la procedura 'Discrepanțe Plan de Producție'
in lingua Romena, con logo Vandewiele in alto a destra.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, ListFlowable, ListItem, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# Percorsi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "manuals", "ro")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "produzione_discrepanze_piano.pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Stili
# ============================================================
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'ManualTitle', parent=styles['Title'],
    fontSize=22, textColor=colors.HexColor('#0078D4'),
    spaceAfter=20, alignment=TA_CENTER
)
subtitle_style = ParagraphStyle(
    'ManualSubtitle', parent=styles['Normal'],
    fontSize=11, textColor=colors.HexColor('#555555'),
    spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Oblique'
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=16, textColor=colors.HexColor('#0078D4'),
    spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold'
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=13, textColor=colors.HexColor('#2C3E50'),
    spaceBefore=15, spaceAfter=8, fontName='Helvetica-Bold'
)
h3_style = ParagraphStyle(
    'H3', parent=styles['Heading3'],
    fontSize=11, textColor=colors.HexColor('#34495E'),
    spaceBefore=10, spaceAfter=5, fontName='Helvetica-Bold'
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_JUSTIFY,
    spaceAfter=8
)
note_style = ParagraphStyle(
    'Note', parent=body_style,
    fontSize=9, textColor=colors.HexColor('#E67E22'),
    fontName='Helvetica-BoldOblique', spaceBefore=5, spaceAfter=10,
    leftIndent=20, borderPadding=5
)
important_style = ParagraphStyle(
    'Important', parent=body_style,
    fontSize=10, textColor=colors.HexColor('#C0392B'),
    fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=8,
    leftIndent=20, borderPadding=5
)
bullet_style = ParagraphStyle(
    'Bullet', parent=body_style,
    fontSize=10, leftIndent=25, bulletIndent=12,
    spaceAfter=4
)

# ============================================================
# Header/Footer con logo
# ============================================================
def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Logo in alto a destra
    if os.path.exists(LOGO_PATH):
        try:
            canvas_obj.drawImage(LOGO_PATH,
                                 A4[0] - inch - 100, A4[1] - 45,
                                 width=100, height=35,
                                 preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    # Footer
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(colors.HexColor('#999999'))
    canvas_obj.drawString(inch, 30,
                          f"Vandewiele Romania — Manual: Discrepanțe Plan de Producție")
    canvas_obj.drawRightString(A4[0] - inch, 30,
                               f"Pagina {doc.page}")
    canvas_obj.restoreState()


# ============================================================
# Contenuto del manuale
# ============================================================
def build_manual():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch + 10,
        bottomMargin=60
    )
    story = []

    # ── Titolo ──
    story.append(Spacer(1, 30))
    story.append(Paragraph("Manual Discrepanțe Plan de Producție", title_style))
    story.append(Paragraph(
        "Procedura de justificare a neconcordanțelor din planul de producție",
        subtitle_style
    ))
    story.append(Paragraph(
        "Versiunea 2.0 — Aprilie 2026",
        ParagraphStyle('ver', parent=subtitle_style, fontSize=9)
    ))
    story.append(Spacer(1, 30))

    # ── 1. Prezentare generală ──
    story.append(Paragraph("1. Prezentare generală", h1_style))
    story.append(Paragraph(
        "Modulul <b>Discrepanțe Plan de Producție</b> monitorizează automat conformitatea "
        "producției cu planul zilnic. Când o comandă nu respectă cantitățile sau termenele planificate, "
        "sistemul generează <b>alerte automate</b> care necesită justificare din partea personalului responsabil.",
        body_style
    ))
    story.append(Paragraph(
        "Sistemul funcționează pe două niveluri:",
        body_style
    ))
    bullets = ListFlowable([
        ListItem(Paragraph(
            "<b>Alerte roșii (Red)</b> — Producția este în întârziere față de plan (deficit cantitativ)", bullet_style)),
        ListItem(Paragraph(
            "<b>Alerte portocalii (Out of Plan)</b> — Producția nu corespunde cu planificarea curentă", bullet_style)),
    ], bulletType='bullet', start='•')
    story.append(bullets)

    # ── 2. Acces ──
    story.append(Paragraph("2. Accesarea modulului", h1_style))
    story.append(Paragraph(
        "Din meniul principal: <b>Operații → Justifică Discrepanțe Plan</b>",
        body_style
    ))
    story.append(Paragraph(
        "Este necesară autentificarea cu credențiale valide. Sesiunea este limitată la <b>60 de minute</b>, "
        "afișate de cronometrul din colțul din dreapta sus.",
        body_style
    ))
    story.append(Paragraph(
        "⚠ Dacă funcționalitatea este dezactivată, contactați departamentul IT "
        "pentru a activa parametrul <i>Sys_enable_control_plan_check</i>.",
        note_style
    ))

    # ── 3. Fereastra principală ──
    story.append(Paragraph("3. Fereastra principală (Master)", h1_style))
    story.append(Paragraph(
        "După autentificare se deschide fereastra de riepilogo cu toate comenzile ce prezintă discrepanțe "
        "nejustificate. Informațiile sunt afișate într-un tabel cu următoarele coloane:",
        body_style
    ))

    col_data = [
        ['Coloană', 'Descriere'],
        ['Order', 'Numărul comenzii de producție'],
        ['Product', 'Denumirea produsului'],
        ['Nr. Discrepancies', 'Numărul total de alerte distincte (fază + dată)'],
        ['🔴 Delay', 'Numărul de alerte roșii (întârzieri)'],
        ['🟠 Out of Plan', 'Numărul de alerte portocalii'],
        ['Total Deficit', 'Deficitul cantitativ total'],
        ['Phases', 'Fazele de producție afectate'],
        ['First Alert / Last Alert', 'Data primei și ultimei alerte'],
    ]
    col_table = Table(col_data, colWidths=[2.5*cm, 12*cm])
    col_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(col_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Rândurile cu fond <font color='#E53935'>roșu deschis</font> conțin alerte de tip <b>Delay</b>. "
        "Rândurile cu fond <font color='#FB8C00'>portocaliu</font> conțin doar alerte <b>Out of Plan</b>.",
        body_style
    ))

    # ── 4. Justificare la nivel de comandă ──
    story.append(Paragraph("4. Justificare la nivel de comandă (Group)", h1_style))
    story.append(Paragraph(
        "Pentru a justifica toate alertele unei comenzi în bloc:",
        body_style
    ))
    steps = ListFlowable([
        ListItem(Paragraph("Selectați una sau mai multe comenzi din tabel (Ctrl+Click pentru selecție multiplă)", bullet_style)),
        ListItem(Paragraph("Alegeți o <b>motivație</b> din lista derulantă (preîncărcată din baza de date)", bullet_style)),
        ListItem(Paragraph("Opțional, adăugați <b>note</b> descriptive", bullet_style)),
        ListItem(Paragraph("Apăsați <b>✅ Salvează pt. comandă selectată</b>", bullet_style)),
        ListItem(Paragraph("Confirmați operațiunea în fereastra de dialog", bullet_style)),
    ], bulletType='1')
    story.append(steps)
    story.append(Paragraph(
        "Toate alertele asociate comenzilor selectate vor fi marcate ca justificate.",
        body_style
    ))

    # ── 5. Fereastra de detaliu ──
    story.append(Paragraph("5. Fereastra de detaliu (Detail)", h1_style))
    story.append(Paragraph(
        "Faceți dublu-click pe o comandă sau selectați-o și apăsați <b>🔍 Deschide detalii</b> "
        "pentru a vedea toate alertele analitice ale acelei comenzi.",
        body_style
    ))
    story.append(Paragraph(
        "Fereastra de detaliu afișează fiecare alertă individual, cu informații despre:",
        body_style
    ))
    detail_bullets = ListFlowable([
        ListItem(Paragraph("<b>Phase</b> — Faza de producție (SMT, ICT, PTHM, etc.)", bullet_style)),
        ListItem(Paragraph("<b>Qty Plan / Produced / Expected</b> — Cantități planificate/produse/așteptate", bullet_style)),
        ListItem(Paragraph("<b>Deficit</b> — Diferența cantitativă", bullet_style)),
        ListItem(Paragraph("<b>Status</b> — Tipul alertei (red / out_of_plan)", bullet_style)),
        ListItem(Paragraph("<b>Alert Date</b> — Data la care s-a generat alerta", bullet_style)),
        ListItem(Paragraph("<b>Future</b> — ✓ dacă comanda apare pe o dată viitoare", bullet_style)),
    ], bulletType='bullet', start='•')
    story.append(detail_bullets)

    story.append(Paragraph("5.1 Justificare la nivel de rând", h2_style))
    story.append(Paragraph(
        "Selectați rândurile dorite (sau folosiți <b>☑ Selectează tot</b>), alegeți motivația, "
        "adăugați note opționale, apoi apăsați <b>✅ Salvează pt. rândurile selectate</b>.",
        body_style
    ))

    # ── 6. REGULA IMPORTANTĂ ──
    story.append(PageBreak())
    story.append(Paragraph("6. Regula de excludere pe dată", h1_style))
    story.append(Paragraph(
        "⚠ REGULĂ IMPORTANTĂ — Justificarea este legată de data alertei:",
        important_style
    ))
    story.append(Paragraph(
        "Odată ce un operator a validat și justificat o discrepanță pentru o anumită "
        "<b>comandă + produs + fază + dată</b>, acea combinație <b>NU va mai apărea</b> în lista "
        "de warning-uri pentru aceeași dată, chiar dacă sistemul generează noi alerte cu "
        "identificatori diferiți.",
        body_style
    ))
    story.append(Spacer(1, 5))

    rule_data = [
        ['Scenariu', 'Comportament'],
        ['Comandă justificată pe 07/04/2026',
         'NU apare în warning-uri pentru 07/04/2026'],
        ['Aceeași comandă pe o dată diferită\n(ex: 09/04/2026)',
         'APARE în warning-uri — necesită justificare separată'],
        ['Comandă justificată + fază diferită\npe aceeași dată',
         'Faza nejustificată APARE, cea justificată NU'],
    ]
    rule_table = Table(rule_data, colWidths=[7*cm, 8*cm])
    rule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C0392B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FEF9E7'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(rule_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Această regulă se aplică atât la nivelul ferestrei de justificare (GUI), cât și "
        "la nivelul escalării automate prin email. Verificarea se bazează pe combinația unică: "
        "<b>idorder + ProductName + PhaseName + AlertDate (ca dată, fără oră)</b>.",
        body_style
    ))

    # ── 7. Escalare automată ──
    story.append(Paragraph("7. Sistemul de escalare automată", h1_style))
    story.append(Paragraph(
        "Alertele nejustificate sunt monitorizate automat de un proces periodic care trimite "
        "email-uri de escalare în funcție de nivelul de urgență:",
        body_style
    ))

    esc_data = [
        ['Nivel', 'Timp', 'Destinatari TO', 'Destinatari CC'],
        ['1-3', 'La fiecare 60 min', 'Leader fază', 'Manager fază'],
        ['4+', 'La fiecare 60 min', 'Management\n(Sys_Alert_not_responce_plan)',
         'Leader + Manager fază'],
    ]
    esc_table = Table(esc_data, colWidths=[1.5*cm, 3.5*cm, 5*cm, 5*cm])
    esc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F8FF')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ]))
    story.append(esc_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Escalarea se oprește automat după justificarea alertelor. "
        "Conform regulii de excludere pe dată, alertele justificate pentru o dată specifică "
        "nu generează mai escalări pe aceeași dată.",
        body_style
    ))

    # ── 8. Rezumat rapoarte ──
    story.append(Paragraph("8. Rapoarte periodice", h1_style))
    story.append(Paragraph(
        "Sistemul generează automat două tipuri de rapoarte:",
        body_style
    ))
    report_bullets = ListFlowable([
        ListItem(Paragraph(
            "<b>Raport lunar</b> — Rezumat complet cu statistici pe faze, tipări de alertă, "
            "și rate de justificare. Trimis automat pe primul ziua lucrătoare a lunii.", bullet_style)),
        ListItem(Paragraph(
            "<b>Verificare săptămânală</b> — Analiză a tendințelor recurente per comandă/fază. "
            "Trimisă automat în fiecare vineri.", bullet_style)),
    ], bulletType='bullet', start='•')
    story.append(report_bullets)

    # ── 9. Note ──
    story.append(Paragraph("9. Note finale", h1_style))
    story.append(Paragraph(
        "• Sesiunea de justificare expiră după <b>60 de minute</b> — re-autentificarea este necesară.<br/>"
        "• Motivațiile disponibile sunt configurate în baza de date (tabelul <i>PlanRespect</i>).<br/>"
        "• Duplicatele sunt eliminate automat la deschiderea ferestrei.<br/>"
        "• Pentru probleme tehnice, contactați departamentul IT.",
        body_style
    ))

    # Build
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✅ Manuale generato: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == '__main__':
    build_manual()
