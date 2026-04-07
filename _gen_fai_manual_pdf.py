# -*- coding: utf-8 -*-
"""Genera FAI_Autocheck_Manual_RO.pdf dal contenuto del manuale."""
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Output ──
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'docs')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PDF = os.path.join(OUTPUT_DIR, 'FAI_Autocheck_Manual_RO.pdf')

# ── Font Registration ──
try:
    pdfmetrics.registerFont(TTFont('ArialUni', 'C:/Windows/Fonts/ARIALUNI.TTF'))
    BASE_FONT = 'ArialUni'
except:
    BASE_FONT = 'Helvetica'

# ── Colors ──
CLR_DARK = HexColor('#1a1a2e')
CLR_PRIMARY = HexColor('#003366')
CLR_ACCENT = HexColor('#B71C1C')
CLR_GREEN = HexColor('#2E7D32')
CLR_ORANGE = HexColor('#E65100')
CLR_LIGHT_BG = HexColor('#f5f7fa')
CLR_TABLE_HEADER = HexColor('#003366')
CLR_TABLE_ALT = HexColor('#e8edf2')
CLR_WARNING_BG = HexColor('#fff3cd')

# ── Styles ──
styles = getSampleStyleSheet()

st_title = ParagraphStyle('FAITitle', parent=styles['Title'],
    fontName=BASE_FONT, fontSize=22, textColor=CLR_PRIMARY,
    spaceAfter=6*mm, alignment=TA_CENTER)

st_h1 = ParagraphStyle('FAIH1', parent=styles['Heading1'],
    fontName=BASE_FONT, fontSize=16, textColor=CLR_PRIMARY,
    spaceBefore=8*mm, spaceAfter=4*mm)

st_h2 = ParagraphStyle('FAIH2', parent=styles['Heading2'],
    fontName=BASE_FONT, fontSize=13, textColor=CLR_DARK,
    spaceBefore=6*mm, spaceAfter=3*mm)

st_h3 = ParagraphStyle('FAIH3', parent=styles['Heading3'],
    fontName=BASE_FONT, fontSize=11, textColor=CLR_DARK,
    spaceBefore=4*mm, spaceAfter=2*mm)

st_body = ParagraphStyle('FAIBody', parent=styles['Normal'],
    fontName=BASE_FONT, fontSize=10, leading=14,
    alignment=TA_JUSTIFY, spaceAfter=2*mm)

st_bullet = ParagraphStyle('FAIBullet', parent=st_body,
    leftIndent=8*mm, bulletIndent=3*mm, spaceAfter=1.5*mm)

st_note = ParagraphStyle('FAINote', parent=st_body,
    fontSize=9, leftIndent=5*mm, textColor=HexColor('#555555'))

st_table_h = ParagraphStyle('FAITableH', parent=st_body,
    fontSize=9, textColor=HexColor('#ffffff'), fontName=BASE_FONT)

st_table_c = ParagraphStyle('FAITableC', parent=st_body,
    fontSize=9, fontName=BASE_FONT, spaceAfter=0)

st_warning = ParagraphStyle('FAIWarning', parent=st_body,
    fontSize=10, textColor=CLR_ACCENT, fontName=BASE_FONT)


def make_table(headers, data_rows, col_widths=None):
    """Create a styled table."""
    h_cells = [Paragraph(f'<b>{h}</b>', st_table_h) for h in headers]
    d_cells = [[Paragraph(str(c), st_table_c) for c in row] for row in data_rows]
    all_rows = [h_cells] + d_cells

    tbl = Table(all_rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), CLR_TABLE_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]
    for i in range(1, len(all_rows)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), CLR_TABLE_ALT))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="FAI Autocheck — Manuale Operativo",
        author="Vandewiele — TraceabilityRS"
    )
    story = []
    W = doc.width

    # ══════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("FAI AUTOCHECK", st_title))
    story.append(Paragraph("Manuale Operativo", ParagraphStyle(
        'Subtitle', parent=st_title, fontSize=14, textColor=CLR_DARK)))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="60%", thickness=2, color=CLR_PRIMARY))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Vandewiele — TraceabilityRS", ParagraphStyle(
        'Company', parent=st_body, alignment=TA_CENTER, fontSize=11, textColor=CLR_PRIMARY)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Versiune: 1.0 — Aprilie 2026", ParagraphStyle(
        'Ver', parent=st_body, alignment=TA_CENTER, fontSize=9, textColor=HexColor('#888888'))))
    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 1. CE ESTE FAI AUTOCHECK
    # ══════════════════════════════════════════
    story.append(Paragraph("1. Ce este FAI Autocheck", st_h1))
    story.append(Paragraph(
        "Sistemul <b>FAI Autocheck</b> este un modul automatizat care garanteaza executarea controalelor FAI "
        "(First Article Inspection) <b>inainte</b> de inceperea productiei pentru fazele critice.", st_body))
    story.append(Paragraph("Sistemul opereaza pe <b>doua niveluri</b>:", st_body))
    story.append(Spacer(1, 3*mm))

    story.append(make_table(
        ['Nivel', 'Ce face', 'Cine este implicat'],
        [
            ['Email Preventiv', 'La fiecare 30 de minute verifica planificarea si trimite email daca un ordin cu FAI obligatoriu urmeaza sa inceapa', 'Responsabili linie PTHM'],
            ['Validare Ghidata', 'Cand operatorul deschide formularul FAI, comenzile sunt pre-incarcate din fisierul Excel de planificare', 'Operatori de linie'],
        ],
        col_widths=[3*cm, 8*cm, 5*cm]
    ))
    story.append(Spacer(1, 5*mm))

    # ══════════════════════════════════════════
    # 2. EMAIL-URI PREVENTIVE AUTOMATE
    # ══════════════════════════════════════════
    story.append(Paragraph("2. Email-uri Preventive Automate", st_h1))

    story.append(Paragraph("2.1 Cum functioneaza", st_h2))
    story.append(Paragraph("Sistemul in <b>fundal</b> (fara interventia operatorului):", st_body))
    steps = [
        "La fiecare <b>30 de minute</b> citeste cel mai recent fisier Excel din folderul <font color='#003366'><b>T:\\Planning\\</b></font>",
        "Deschide tab-ul <b>PlanningMachine</b> si cauta toate comenzile cu incepere planificata in urmatoarele <b>4 ore</b>",
        "Pentru fiecare comanda gasita, verifica daca <b>faza</b> corespunde unui template FAI cu <b>Autocheck = 1</b>",
        "Daca da, verifica daca <b>productia a inceput deja</b> (cantitate > 0)",
        "Daca productia <b>NU a inceput</b>, trimite un <b>email urgent</b> responsabililor de linie",
    ]
    for i, s in enumerate(steps, 1):
        story.append(Paragraph(f"{i}. {s}", st_bullet))

    story.append(Paragraph("2.2 Cine primeste email-ul", st_h2))
    story.append(make_table(
        ['Rol', 'Conditie', 'Camp email'],
        [
            ['Responsabili linie (FunctionCode 21-59)', 'Doar daca sunt PREZENTI in tura (verificat prin pontaj)', 'TO (destinatar principal)'],
            ['Manageri (FunctionCode 60-80)', 'INTOTDEAUNA', 'CC (copie)'],
        ],
        col_widths=[5*cm, 6.5*cm, 4.5*cm]
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<font color='#B71C1C'><b>Atentie:</b></font> Daca niciun responsabil de linie nu este in tura, "
        "email-ul <b>nu este trimis</b> dar evenimentul este inregistrat in baza de date.", st_warning))

    story.append(Paragraph("2.3 Continutul email-ului", st_h2))
    items = [
        "Avertisment urgent cu solicitare de actiune",
        "Numarul comenzii si numele fazei",
        "Ora planificata de incepere a productiei",
        "Template-ul FAI aplicabil (titlu, document, revizie)",
        "Nota privind inregistrarea in scopuri de conformitate",
    ]
    for item in items:
        story.append(Paragraph(f"• {item}", st_bullet))

    story.append(Paragraph("2.4 Anti-duplicare", st_h2))
    story.append(Paragraph(
        "Sistemul <b>nu trimite acelasi email de doua ori</b>. Pentru fiecare combinatie unica de: "
        "numar comanda + faza + template FAI + ora planificata — se trimite <b>o singura notificare</b>.", st_body))

    story.append(Paragraph("2.5 Ore de functionare", st_h2))
    story.append(make_table(
        ['Parametru', 'Valoare'],
        [
            ['Interval de verificare', 'La fiecare 30 de minute'],
            ['Fereastra de anticipare', '4 ore inainte de incepere'],
            ['Ore active', '06:00 — 22:00'],
            ['Zile active', 'Doar zile lucratoare (calendar Romania)'],
        ],
        col_widths=[5*cm, 11*cm]
    ))

    # ══════════════════════════════════════════
    # 3. VALIDARE FAI CU COMENZI DIN PLANNING
    # ══════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("3. Validare FAI cu Comenzi din Planning", st_h1))

    story.append(Paragraph("3.1 Cand se activeaza", st_h2))
    story.append(Paragraph(
        "Cand un operator deschide formularul <b>FAI — Validare Linie</b> si selecteaza "
        "un template cu <b>Autocheck = 1</b>, sistemul schimba automat comportamentul "
        "selectorului de comenzi:", st_body))
    story.append(make_table(
        ['Template', 'Comportament comenzi'],
        [
            ['Autocheck = 0 (implicit)', 'Operatorul tasteaza si cauta printre TOATE comenzile din baza de date'],
            ['Autocheck = 1', 'Sistemul incarca DOAR comenzile planificate din fisierul Excel, filtrate dupa faza template-ului'],
        ],
        col_widths=[4*cm, 12*cm]
    ))

    story.append(Paragraph("3.2 Pasi operativi", st_h2))

    story.append(Paragraph("<b>Pas 1: Accesare Validare Linie</b>", st_h3))
    story.append(Paragraph(
        "Din meniul principal: <font color='#003366'><b>Meniu → FAI → Validare Linie → [Login cu credentiale]</b></font>", st_body))

    story.append(Paragraph("<b>Pas 2: Selectare Template FAI</b>", st_h3))
    story.append(Paragraph(
        "Din meniul derulant <b>\"Template FAI\"</b>, selectati template-ul dorit. "
        "Daca template-ul are <b>Autocheck activ</b>, sistemul va afisa automat comenzile din planificare. "
        "In bara de stare va aparea mesajul:", st_body))
    story.append(Paragraph(
        "<i>«X comenzi din planning (Y intarziate &lt;3h)»</i>", st_note))

    story.append(Paragraph("<b>Pas 3: Intelegerea indicatorilor</b>", st_h3))
    story.append(Paragraph(
        "Fiecare comanda din lista afiseaza un <b>indicator de timp</b>:", st_body))
    story.append(make_table(
        ['Pictograma', 'Semnificatie', 'Exemplu'],
        [
            ['✅', 'Comanda incepe peste 3 ore sau mai mult — timp suficient', '✅ PR0000345 - PROD001 [Start 07:30 (in 13h)]'],
            ['⏰', 'Comanda incepe in mai putin de 3 ore — control FAI INTARZIAT', '⏰ PR0000348 - PROD002 [Start 17:53 (in 0h — LATE!)]'],
        ],
        col_widths=[2*cm, 6*cm, 8*cm]
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<font color='#B71C1C'><b>Important:</b></font> Comenzile cu ⏰ pot fi in continuare selectate si validate, "
        "dar sistemul <b>inregistreaza automat</b> ca controlul FAI a fost efectuat cu intarziere.", st_warning))

    story.append(Paragraph("<b>Pas 4: Selectare comanda</b>", st_h3))
    story.append(Paragraph(
        "Faceti clic pe comanda dorita. Campurile se vor completa automat: "
        "<b>Cod</b> (cod produs), <b>Cantitate</b>, <b>Comanda SL</b> (ID comanda).", st_body))

    story.append(Paragraph("<b>Pas 5: Completare checklist</b>", st_h3))
    story.append(Paragraph("Procedati normal cu completarea checklist-ului FAI:", st_body))
    story.append(Paragraph("• <b>OK</b> — controlul este trecut", st_bullet))
    story.append(Paragraph("• <b>Not OK</b> — controlul NU este trecut (se va solicita descriere problema, cauza radacina si actiune corectiva)", st_bullet))
    story.append(Paragraph("• <b>N/A</b> — controlul nu este aplicabil", st_bullet))

    story.append(Paragraph("<b>Pas 6: Salvare validare</b>", st_h3))
    story.append(Paragraph("Apasati <b>\"Salveaza Validarea\"</b>. Sistemul:", st_body))
    story.append(Paragraph("1. Salveaza toate rezultatele in baza de date", st_bullet))
    story.append(Paragraph("2. Genereaza PDF-ul raportului FAI", st_bullet))
    story.append(Paragraph("3. Trimite email-ul de notificare", st_bullet))
    story.append(Paragraph(
        "4. <b>Daca Autocheck:</b> inregistreaza evenimentul cu starea <b>VERIFIED_ON_TIME</b> "
        "(daca ≥ 3h inainte) sau <b>VERIFIED_LATE</b> (daca &lt; 3h inainte)", st_bullet))

    # ══════════════════════════════════════════
    # 4. STARI POSIBILE
    # ══════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4. Stari posibile in Tabelul de Urmarire", st_h1))
    story.append(Paragraph(
        "Toate evenimentele sunt inregistrate in tabela "
        "<font color='#003366'><b>FaiAutocheckNotifications</b></font>:", st_body))
    story.append(make_table(
        ['Stare', 'Semnificatie'],
        [
            ['SENT', 'Email preventiv trimis catre responsabili'],
            ['SKIPPED_ALREADY_STARTED', 'Productia deja inceputa, email nenecesar'],
            ['SKIPPED_NO_RECIPIENT', 'Niciun responsabil prezent in tura'],
            ['VERIFIED_ON_TIME', 'FAI executat cu cel putin 3h inainte ✅'],
            ['VERIFIED_LATE', 'FAI executat cu mai putin de 3h inainte ⏰'],
        ],
        col_widths=[5*cm, 11*cm]
    ))

    # ══════════════════════════════════════════
    # 5. FAQ
    # ══════════════════════════════════════════
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("5. Intrebari Frecvente", st_h1))

    faqs = [
        ("De ce nu vad comenzi cand selectez template-ul Autocheck?",
         "Cauze posibile:<br/>1. <b>Nicio comanda PTHM in urmatoarele 4 ore</b><br/>"
         "2. <b>Fisierul Excel neactualizat</b> — sistemul citeste cel mai recent fisier din T:\\Planning\\<br/>"
         "3. <b>Faza nu corespunde</b> — faza comenzii din Excel trebuie sa corespunda exact fazei template-ului FAI"),
        ("Pot valida o comanda care nu este in lista din planning?",
         "Nu, daca template-ul are Autocheck activ. Pentru a valida o comanda neplanificata, "
         "utilizati un template FAI fara Autocheck."),
        ("Ce se intampla daca nu execut controlul FAI inainte de incepere?",
         "1. Sistemul va trimite email-uri preventive responsabililor<br/>"
         "2. Evenimentul va fi inregistrat in baza de date<br/>"
         "3. Daca controlul este efectuat dupa incepere, va fi marcat ca <b>VERIFIED_LATE</b>"),
        ("Email-ul mai ajunge daca FAI a fost deja completat?",
         "Nu. Daca productia a inceput deja (cantitate > 0), sistemul inregistreaza "
         "SKIPPED_ALREADY_STARTED si <b>nu trimite email-ul</b>."),
        ("Sistemul functioneaza si in zilele libere?",
         "Nu. Sistemul respecta <b>calendarul lucrator romanesc</b> si se dezactiveaza "
         "automat in weekend si sarbatori legale."),
    ]

    for q, a in faqs:
        story.append(Paragraph(f"<b>Q: {q}</b>", st_h3))
        story.append(Paragraph(a, st_body))
        story.append(Spacer(1, 2*mm))

    # ── Build ──
    doc.build(story)
    print(f"PDF generato: {OUTPUT_PDF}")
    return OUTPUT_PDF


if __name__ == '__main__':
    build_pdf()
