# -*- coding: utf-8 -*-
"""
Generatore manuale FAI in PDF — Documentazione completa in rumeno.
Copre: template FAI, validazione linea, autocheck, enforcement, rapoarte.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# ── Font Registration ──────────────────────────────────────────
FONT_DIR = r'C:\Windows\Fonts'
for name, file in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf'),
                   ('Arial-Italic', 'ariali.ttf'), ('Arial-BoldItalic', 'arialbi.ttf')]:
    if name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, file)))

# ── Color Palette ──────────────────────────────────────────────
C_PRIMARY    = HexColor('#1B3A5C')   # Dark blue
C_SECONDARY  = HexColor('#2E86AB')   # Teal
C_ACCENT     = HexColor('#E8483F')   # Red accent
C_SUCCESS    = HexColor('#27AE60')   # Green
C_WARNING    = HexColor('#F39C12')   # Orange
C_LIGHT_BG   = HexColor('#F4F6F9')   # Light bg
C_TABLE_HDR  = HexColor('#1B3A5C')   # Table header
C_TABLE_ALT  = HexColor('#EBF0F5')   # Alt row

# ── Styles ─────────────────────────────────────────────────────
styles = getSampleStyleSheet()

S_TITLE = ParagraphStyle('DocTitle', fontName='Arial-Bold', fontSize=26,
    leading=32, textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=6)

S_SUBTITLE = ParagraphStyle('DocSubtitle', fontName='Arial-Italic', fontSize=12,
    leading=16, textColor=C_SECONDARY, alignment=TA_CENTER, spaceAfter=20)

S_H1 = ParagraphStyle('H1', fontName='Arial-Bold', fontSize=16,
    leading=22, textColor=C_PRIMARY, spaceBefore=20, spaceAfter=8,
    borderPadding=(0, 0, 4, 0))

S_H2 = ParagraphStyle('H2', fontName='Arial-Bold', fontSize=13,
    leading=18, textColor=C_SECONDARY, spaceBefore=14, spaceAfter=6)

S_H3 = ParagraphStyle('H3', fontName='Arial-Bold', fontSize=11,
    leading=15, textColor=C_PRIMARY, spaceBefore=10, spaceAfter=4)

S_BODY = ParagraphStyle('Body', fontName='Arial', fontSize=10,
    leading=14, textColor=black, alignment=TA_JUSTIFY, spaceAfter=6)

S_BULLET = ParagraphStyle('Bullet', fontName='Arial', fontSize=10,
    leading=14, leftIndent=20, bulletIndent=8, spaceAfter=3,
    bulletFontName='Arial', bulletFontSize=10)

S_NOTE = ParagraphStyle('Note', fontName='Arial-Italic', fontSize=9,
    leading=12, textColor=HexColor('#555555'), leftIndent=15,
    borderColor=C_SECONDARY, borderWidth=2, borderPadding=8,
    backColor=HexColor('#F0F7FA'), spaceAfter=8)

S_WARNING_BOX = ParagraphStyle('Warning', fontName='Arial-Bold', fontSize=10,
    leading=14, textColor=C_ACCENT, leftIndent=15,
    borderColor=C_ACCENT, borderWidth=2, borderPadding=8,
    backColor=HexColor('#FEF0EF'), spaceAfter=8)

S_FOOTER = ParagraphStyle('Footer', fontName='Arial', fontSize=8,
    leading=10, textColor=HexColor('#999999'), alignment=TA_CENTER)

# ── Helpers ────────────────────────────────────────────────────
def section_line():
    return HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY,
                      spaceBefore=4, spaceAfter=8)

def make_table(headers, data, col_widths=None):
    """Creates a styled table."""
    all_data = [headers] + data
    t = Table(all_data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), C_TABLE_HDR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(all_data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), C_TABLE_ALT))
    t.setStyle(TableStyle(style))
    return t

def add_header_footer(canvas_obj, doc):
    """Header with logo + footer with page numbers."""
    canvas_obj.saveState()
    w, h = A4
    # Header line
    canvas_obj.setStrokeColor(C_PRIMARY)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(2*cm, h - 1.8*cm, w - 2*cm, h - 1.8*cm)
    # Logo
    if os.path.exists("Logo.png"):
        try:
            canvas_obj.drawImage("Logo.png", 2*cm, h - 1.6*cm,
                width=2.5*cm, height=1*cm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    # Header text
    canvas_obj.setFont('Arial', 8)
    canvas_obj.setFillColor(HexColor('#999999'))
    canvas_obj.drawRightString(w - 2*cm, h - 1.3*cm,
        "TraceabilityRS — Manual FAI System")
    # Footer
    canvas_obj.setFont('Arial', 8)
    canvas_obj.setFillColor(HexColor('#999999'))
    canvas_obj.drawString(2*cm, 1.2*cm,
        f"Document generat automat — {datetime.now().strftime('%d/%m/%Y')}")
    canvas_obj.drawRightString(w - 2*cm, 1.2*cm,
        f"Pagina {doc.page}")
    canvas_obj.restoreState()


# ── BUILD DOCUMENT ─────────────────────────────────────────────
def build_fai_manual():
    output_dir = r"C:\Temp"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir,
        f"Manual_FAI_System_{datetime.now().strftime('%Y%m%d')}.pdf")

    doc = SimpleDocTemplate(filepath, pagesize=A4,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm)

    story = []
    W = doc.width

    # ══════════════════════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("MANUAL FAI SYSTEM", S_TITLE))
    story.append(Paragraph("First Article Inspection — Sistem Complet", S_SUBTITLE))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="60%", thickness=3, color=C_SECONDARY,
                            spaceBefore=0, spaceAfter=20))

    # Info box
    info_data = [
        ['Versiune:', '2.4'],
        ['Data:', datetime.now().strftime('%d/%m/%Y')],
        ['Departament:', 'Producție / Calitate'],
        ['Companie:', 'Vandewiele Romania S.R.L.'],
        ['Aplicație:', 'TraceabilityRS — Document Management'],
    ]
    info_table = Table(info_data, colWidths=[4*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Arial-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), C_PRIMARY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("CUPRINS", S_H1))
    story.append(section_line())

    toc_items = [
        "1. Prezentare Generală a Sistemului FAI",
        "2. Șabloane FAI (FAI Templates)",
        "3. Validarea Liniei de Producție",
        "4. FAI Autocheck — Monitorizare Automată din Planificare",
        "5. FAI Compliance Enforcement — Sistem de Escaladare",
        "6. Raportarea FAI — Vizualizator și Export",
        "7. Notificări FAI Failures",
        "8. Baza de Date — Structura Tabelelor FAI",
        "9. Roluri și Responsabilități",
        "10. Întrebări Frecvente (FAQ)",
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", ParagraphStyle('TOC',
            fontName='Arial', fontSize=11, leading=18, leftIndent=15,
            textColor=C_PRIMARY)))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 1. OVERVIEW
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("1. Prezentare Generală a Sistemului FAI", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Sistemul FAI (First Article Inspection) este un modul integrat în aplicația "
        "TraceabilityRS care asigură conformitatea calității producției prin verificări "
        "standardizate la începutul fiecărui tur de lucru și la schimbarea ordinelor de "
        "producție. Sistemul acoperă întregul ciclu de viață al verificărilor FAI:",
        S_BODY))

    story.append(Paragraph("• <b>Definirea șabloanelor</b> — Crearea și gestionarea template-urilor FAI cu pași de verificare", S_BULLET))
    story.append(Paragraph("• <b>Validarea pe linie</b> — Completarea verificărilor de către capi tur/capilinea", S_BULLET))
    story.append(Paragraph("• <b>Autocheck din planificare</b> — Notificări preventive bazate pe planul de producție", S_BULLET))
    story.append(Paragraph("• <b>Enforcement cu escaladare</b> — Monitorizarea obligatorie cu 3 nivele de escaladare", S_BULLET))
    story.append(Paragraph("• <b>Raportare și export</b> — Vizualizarea și exportul rezultatelor în Excel", S_BULLET))
    story.append(Paragraph("• <b>Notificări non-conformități</b> — Alerte automate pentru FAI-uri eșuate", S_BULLET))

    # Architecture diagram as table
    story.append(Spacer(1, 10))
    story.append(Paragraph("Arhitectura Sistemului FAI", S_H2))

    arch_data = [
        ['Modul', 'Fișier', 'Funcționalitate'],
        ['Template Manager', 'main.py (UI)', 'Creare/editare șabloane FAI'],
        ['Validare Linie', 'line_validation_gui.py', 'Formular de verificare cu checklist'],
        ['Autocheck', 'fai_autocheck.py', 'Monitorizare din Excel planificare'],
        ['Enforcement', 'fai_enforcement.py', 'Escaladare obligatorie pe 3 nivele'],
        ['Rapoarte', 'fai_reports_viewer.py', 'Vizualizare și export Excel'],
        ['Notif. Eșecuri', 'utils.py', 'Email automate pentru non-conformități'],
    ]
    story.append(make_table(arch_data[0], arch_data[1:],
        col_widths=[3.5*cm, 4.5*cm, 9*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 2. FAI TEMPLATES
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("2. Șabloane FAI (FAI Templates)", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Șabloanele FAI definesc structura verificărilor care trebuie efectuate. "
        "Fiecare template este asociat unei faze de producție (SMT, PTHM, ICT, FCT) "
        "și conține mai mulți pași de verificare organizați în secțiuni.",
        S_BODY))

    story.append(Paragraph("Structura unui Template FAI", S_H2))

    tmpl_data = [
        ['Câmp', 'Descriere', 'Exemplu'],
        ['NrDocument', 'Număr document template', 'FAI-SMT-001'],
        ['Revision', 'Versiunea reviziei', '3'],
        ['FaiTitle', 'Titlul documentului', 'FAI Verificare Linie SMT'],
        ['IdPhase', 'Faza de producție asociată', 'SMT / PTHM / ICT / FCT'],
        ['Autocheck', 'Template folosit în monitorizare automată', 'Da / Nu'],
        ['RevisionDate', 'Data ultimei revizii', '15/03/2026'],
    ]
    story.append(make_table(tmpl_data[0], tmpl_data[1:],
        col_widths=[3*cm, 7*cm, 7*cm]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Fiecare template conține:", S_BODY))
    story.append(Paragraph("• <b>FaiSteps</b> — Sectiuni/grupuri de verificare (ex: Verificare Stencil, Verificare Temperatura)", S_BULLET))
    story.append(Paragraph("• <b>FaiStepDetails</b> — Pași individuali din fiecare secțiune cu descriere detaliată", S_BULLET))
    story.append(Paragraph("• <b>Validation Labels</b> — Etichete pentru tipul de verificare (OK / NOT OK / N/A)", S_BULLET))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>NOTĂ:</b> Template-urile cu câmpul <b>Autocheck = 1</b> sunt utilizate de "
        "modulul de monitorizare automată din planificare. Doar aceste template-uri "
        "declanșează notificări preventive.",
        S_NOTE))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 3. LINE VALIDATION
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("3. Validarea Liniei de Producție", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Validarea liniei este procesul prin care capi de tur și capii de linie "
        "completează verificările FAI obligatorii. Aceasta se realizează prin "
        "formularul <b>LineValidationWindow</b>.",
        S_BODY))

    story.append(Paragraph("Pașii de Completare", S_H2))

    steps_val = [
        "1. Selectarea template-ului FAI corespunzător fazei de producție",
        "2. Selectarea ordinului de producție din lista disponibilă",
        "3. Parcurgerea fiecărui pas de verificare din checklist",
        "4. Marcarea fiecărui pas ca: <b>OK</b>, <b>NOT OK</b> sau <b>N/A</b>",
        "5. Completarea câmpului <b>Dati/Note</b> cu observații (obligatoriu pentru NOT OK)",
        "6. Introducerea <b>LabelCode</b> pentru etichetarea sesiunii",
        "7. Salvarea validării cu generarea automată a documentului PDF",
    ]
    for s in steps_val:
        story.append(Paragraph(f"• {s}", S_BULLET))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Câmpuri Obligatorii în Caz de NOT OK", S_H3))
    story.append(Paragraph(
        "Când un pas este marcat ca <b>NOT OK</b>, sistemul solicită completarea "
        "obligatorie a următoarelor câmpuri:",
        S_BODY))

    nok_data = [
        ['Câmp', 'Descriere'],
        ['ProblemDescription', 'Descrierea detaliată a problemei constatate'],
        ['RoutCauseProblem', 'Cauza identificată a problemei (root cause)'],
        ['CorrectiveAction', 'Acțiunea corectivă întreprinsă sau planificată'],
    ]
    story.append(make_table(nok_data[0], nok_data[1:],
        col_widths=[4.5*cm, 12.5*cm]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Ordinele de Producție", S_H2))
    story.append(Paragraph(
        "Lista ordinelor este populată din două surse:", S_BODY))
    story.append(Paragraph("• <b>Din baza de date</b> — Ordinele active din Traceability_RS", S_BULLET))
    story.append(Paragraph("• <b>Din fișierul de planificare Excel</b> — Ordinele din Planning Machine "
        "(T:\\Planning), filtrate automat pe faza corespunzătoare template-ului FAI selectat. "
        "Ordinele cu start planificat în mai puțin de 3 ore sunt evidențiate cu 🔴.", S_BULLET))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 4. AUTOCHECK
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("4. FAI Autocheck — Monitorizare Automată din Planificare", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Modulul FAI Autocheck funcționează ca un serviciu de fundal care monitorizează "
        "permanent fișierul de planificare Excel (T:\\Planning) pentru a identifica "
        "producțiile programate în următoarele 4 ore și a trimite notificări preventive.",
        S_BODY))

    story.append(Paragraph("Flux de Funcționare", S_H2))

    flow_data = [
        ['Pas', 'Acțiune', 'Interval'],
        ['1', 'Citirea celui mai recent fișier Excel din T:\\Planning', 'La fiecare 30 min'],
        ['2', 'Filtrarea producțiilor din următoarele 4 ore', '-'],
        ['3', 'Verificarea dacă faza are un template FAI cu Autocheck=1', '-'],
        ['4', 'Verificarea dacă producția a fost deja pornită (Scannings)', '-'],
        ['5', 'Verificarea prezenței responsabililor în tur', 'Via Timeclocking SP'],
        ['6', 'Trimiterea notificării email preventive', 'Anti-duplicare activă'],
    ]
    story.append(make_table(flow_data[0], flow_data[1:],
        col_widths=[1.5*cm, 10.5*cm, 5*cm]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Destinatari Email", S_H2))
    story.append(Paragraph(
        "Emailurile sunt trimise în funcție de rolul și prezența angajatului:", S_BODY))
    story.append(Paragraph("• <b>TO</b> — Capi tur/capilinea (FunctionCode 21-59) prezenți în tur", S_BULLET))
    story.append(Paragraph("• <b>CC</b> — Coordonatori (FunctionCode ≥ 60), întotdeauna incluși", S_BULLET))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>NOTĂ:</b> Sistemul verifică prezența prin procedura stocată "
        "<i>Timeclocking.dbo.GetEmployeesTimeclockReal</i>. Angajații care nu sunt "
        "prezenți fizic în fabrică nu primesc notificări.",
        S_NOTE))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 5. ENFORCEMENT
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("5. FAI Compliance Enforcement — Sistem de Escaladare", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Modulul de Enforcement este un sistem automat care <b>obligă</b> completarea "
        "FAI-urilor la fiecare început de tur. Dacă verificarea nu este efectuată în "
        "termenul prevăzut, sistemul declanșează un proces de escaladare pe 3 nivele, "
        "culminând cu emisiunea automată a unui <b>Referat disciplinar</b>.",
        S_BODY))

    story.append(Paragraph(
        "<b>⚠️ ATENȚIE:</b> Necompletarea FAI-ului în termen de 120 de minute de la "
        "începutul turului duce la generarea automată a unui referat disciplinar!",
        S_WARNING_BOX))

    story.append(Paragraph("Tururile Monitorizate", S_H2))

    shift_data = [
        ['Tur', 'Start', 'Verificare la', 'Condiție Activare'],
        ['Dimineață', '07:30', '08:30', 'Întotdeauna activ'],
        ['După-amiază', '15:30', '16:30', 'Întotdeauna activ'],
        ['Noapte', '23:30', '00:30', 'Doar dacă există producție activă'],
    ]
    story.append(make_table(shift_data[0], shift_data[1:],
        col_widths=[3*cm, 3*cm, 3.5*cm, 7.5*cm]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Procesul de Escaladare", S_H2))

    esc_data = [
        ['Nivel', 'Moment', 'Destinatar', 'Acțiune'],
        ['Nivel 1 🟡', '+60 min', 'Șef Secție\n(FunctionCode 60-69)',
         'Notificare email de avertizare'],
        ['Nivel 2 🟠', '+90 min', 'Șef Producție\n(FunctionCode 70-79)',
         'Notificare email urgentă'],
        ['Nivel 3 🔴', '+120 min', 'Resp. Calitate + Administrator\n(FunctionCode ≥80)',
         'Notificare email +\nREFERAT DISCIPLINAR automat'],
    ]
    # Use Paragraph for wrapping in cells
    esc_formatted = []
    for row in esc_data[1:]:
        esc_formatted.append([
            Paragraph(row[0], ParagraphStyle('c', fontName='Arial-Bold', fontSize=9, leading=12)),
            Paragraph(row[1], ParagraphStyle('c', fontName='Arial', fontSize=9, leading=12)),
            Paragraph(row[2], ParagraphStyle('c', fontName='Arial', fontSize=9, leading=12)),
            Paragraph(row[3], ParagraphStyle('c', fontName='Arial', fontSize=9, leading=12)),
        ])
    esc_headers = [
        Paragraph(h, ParagraphStyle('h', fontName='Arial-Bold', fontSize=9, textColor=white))
        for h in esc_data[0]
    ]

    esc_table = Table([esc_headers] + esc_formatted,
        colWidths=[2.5*cm, 2.5*cm, 5*cm, 7*cm])
    esc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_TABLE_HDR),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#FFF9E6')),  # L1 yellow
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#FFF0E0')),  # L2 orange
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#FEF0EF')),  # L3 red
    ]))
    story.append(esc_table)

    story.append(Spacer(1, 12))
    story.append(Paragraph("Referatul Disciplinar Automat", S_H2))
    story.append(Paragraph(
        "La atingerea Nivelului 3 de escaladare, sistemul generează automat:", S_BODY))
    story.append(Paragraph("• Un document <b>REFERAT</b> în format PDF, cu număr de înregistrare generat "
        "din procedura stocată <i>Employee.dbo.Registro</i> (RegistryTypeId=60)", S_BULLET))
    story.append(Paragraph("• Înregistrarea în tabelul <b>EmployeeDisciplinaryHistory</b> "
        "cu ArticoloLegaleId=33 (nerespectarea regulamentului intern)", S_BULLET))
    story.append(Paragraph("• Semnătura digitală a <b>Administratorului</b> este inclusă automat în PDF", S_BULLET))
    story.append(Paragraph("• PDF-ul este atașat la email-ul de notificare Nivel 3", S_BULLET))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Monitorizarea Ordinelor Noi", S_H2))
    story.append(Paragraph(
        "Pe lângă verificarea la începutul turului, sistemul monitorizează în mod "
        "continuu (la fiecare oră) tabelul <b>Scannings</b> pentru a detecta ordine noi "
        "care au intrat în producție. Logica:", S_BODY))
    story.append(Paragraph("• Se compară IDOrder-urile din ultima oră cu cele din ora precedentă", S_BULLET))
    story.append(Paragraph("• Se verifică dacă ordinul nou are un <b>FaiTemplate</b> asociat (prin IdPhase)", S_BULLET))
    story.append(Paragraph("• Dacă FAI-ul nu a fost completat → se declanșează ciclul de escaladare", S_BULLET))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 6. REPORTS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("6. Raportarea FAI — Vizualizator și Export", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Vizualizatorul de rapoarte FAI permite consultarea și exportul tuturor "
        "verificărilor efectuate. Se accesează din meniul aplicației cu autentificare.",
        S_BODY))

    story.append(Paragraph("Funcționalități", S_H2))

    report_data = [
        ['Funcție', 'Descriere'],
        ['Filtrare pe dată', 'Selectarea intervalului De la / Până la'],
        ['Filtrare pe Produs', 'Căutare parțială pe codul produsului'],
        ['Filtrare pe Operator', 'Căutare parțială pe numele operatorului'],
        ['Filtrare pe LabelCode', 'Căutare parțială pe codul etichetei FAI'],
        ['Vizualizare Treeview', 'O singură linie per sesiune (GROUP BY)'],
        ['Export Excel', 'Export detaliat cu toate răspunsurile individuale pe pași'],
        ['Vizualizare PDF', 'Deschiderea documentului PDF din baza de date'],
        ['Eliminare validare', 'Ștergere soft a unei validări (DateOut = acum)'],
    ]
    story.append(make_table(report_data[0], report_data[1:],
        col_widths=[4.5*cm, 12.5*cm]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Diferența Treeview vs. Excel", S_H3))
    story.append(Paragraph(
        "Vizualizarea în Treeview arată câte <b>o singură linie per sesiune de validare</b> "
        "(grupat pe LabelCode, Ordine, Operator și Template). "
        "Exportul Excel conține <b>toate rândurile detaliate</b> cu fiecare pas de verificare, "
        "valorile introduse, descrierile problemelor și acțiunile corective.",
        S_BODY))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Coloane Export Excel", S_H3))
    excel_cols = [
        ['Coloană', 'Descriere'],
        ['FAI Document', 'Număr document + revizie + data emiterii'],
        ['LabelCode', 'Codul etichetei sesiunii de validare'],
        ['Data/Ora', 'Data și ora completării'],
        ['N. Ordine', 'Numărul ordinului de producție'],
        ['Codice Prodotto', 'Codul produsului'],
        ['Operatore', 'Numele operatorului care a completat'],
        ['Step', 'Numele secțiunii de verificare'],
        ['Descrizione Step', 'Descrierea detaliată a pasului'],
        ['Risultato', 'OK / NOT OK / N/A'],
        ['Dati/Note', 'Valorile introduse sau observațiile'],
        ['Descrizione Problema', 'Descrierea problemei (dacă NOT OK)'],
        ['Causa Radice', 'Cauza identificată a problemei'],
        ['Azione Correttiva', 'Acțiunea corectivă întreprinsă'],
    ]
    story.append(make_table(excel_cols[0], excel_cols[1:],
        col_widths=[4*cm, 13*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 7. FAI FAILURES
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("7. Notificări FAI Failures", S_H1))
    story.append(section_line())

    story.append(Paragraph(
        "Sistemul trimite automat notificări email când sunt detectate "
        "non-conformități (FAI-uri marcate ca NOT OK). Email-urile includ "
        "statistici despre performanța operatorilor.", S_BODY))

    story.append(Paragraph("Conținut Email", S_H2))
    story.append(Paragraph("• Lista completă a <b>LabelCode-urilor</b> cu FAI eșuat", S_BULLET))
    story.append(Paragraph("• Statistici pe operator: Total verificări, Total eșecuri, Procentul de eșec", S_BULLET))
    story.append(Paragraph("• După trimitere, înregistrările sunt marcate ca analizate (IsAnalized=1)", S_BULLET))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 8. DATABASE SCHEMA
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("8. Baza de Date — Structura Tabelelor FAI", S_H1))
    story.append(section_line())

    db_data = [
        ['Tabel', 'Schemă', 'Scop'],
        ['FaiTemplates', 'fai', 'Șabloanele de verificare cu metadate'],
        ['FaiSteps', 'fai', 'Secțiunile din fiecare template'],
        ['FaiStepDetails', 'fai', 'Pașii individuali de verificare'],
        ['FaiLogs', 'fai', 'Rezultatele completate (un rând per pas)'],
        ['FaiAutocheckNotifications', 'fai', 'Tracking notificări autocheck (anti-duplicare)'],
        ['FaiEnforcementLog', 'fai', 'Tracking enforcement și escaladări'],
        ['Orders', 'dbo', 'Ordinele de producție'],
        ['OrderPhases', 'dbo', 'Fazele asociate ordinelor'],
        ['Phases', 'dbo', 'Fazele de producție (SMT, PTHM, ICT, FCT)'],
        ['Scannings', 'dbo', 'Scannerile de producție (intrare/ieșire board)'],
        ['Boards', 'dbo', 'Plăcile de circuit (link la ordine)'],
    ]
    story.append(make_table(db_data[0], db_data[1:],
        col_widths=[5*cm, 2*cm, 10*cm]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Tabelul FaiLogs — Câmpuri Principale", S_H2))
    failogs_data = [
        ['Câmp', 'Tip', 'Descriere'],
        ['FaiLogId', 'INT PK', 'Identificator unic'],
        ['FaiStepDetailId', 'INT FK', 'Pasul de verificare'],
        ['OrderId', 'INT FK', 'Ordinul de producție'],
        ['Operator', 'NVARCHAR', 'Numele operatorului'],
        ['LabelCode', 'NVARCHAR', 'Codul etichetei sesiunii'],
        ['IsOk', 'BIT', 'Rezultat: 1=OK, 0=NOT OK'],
        ['IsNA', 'BIT', 'Pas neaplicabil'],
        ['Dati', 'NVARCHAR', 'Valori/observații introduse'],
        ['ProblemDescription', 'NVARCHAR', 'Descrierea problemei'],
        ['RoutCauseProblem', 'NVARCHAR', 'Cauza problemei'],
        ['CorrectiveAction', 'NVARCHAR', 'Acțiune corectivă'],
        ['DocVerification', 'VARBINARY', 'Document PDF atașat'],
        ['DateIn', 'DATETIME', 'Data completării'],
        ['DateOut', 'DATETIME', 'Data anulării (NULL=valid)'],
    ]
    story.append(make_table(failogs_data[0], failogs_data[1:],
        col_widths=[4*cm, 3*cm, 10*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 9. ROLES
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("9. Roluri și Responsabilități", S_H1))
    story.append(section_line())

    roles_data = [
        ['Rol', 'FunctionCode', 'Responsabilitate FAI'],
        ['Cap de linie / Cap de tur', '21 — 59',
         'Completarea FAI la fiecare început de tur și la schimbarea ordinelor'],
        ['Șef Secție', '60 — 69',
         'Primește escaladarea Nivel 1 și asigură completarea FAI'],
        ['Șef Producție', '70 — 79',
         'Primește escaladarea Nivel 2 și intervine în cazuri urgente'],
        ['Responsabil Calitate', '≥ 80',
         'Primește escaladarea Nivel 3, gestionează non-conformitățile'],
        ['Administrator', 'Tabel Administrators',
         'Primește escaladarea Nivel 3, semnatar al referatelor disciplinare'],
    ]
    roles_formatted = []
    for row in roles_data[1:]:
        roles_formatted.append([
            Paragraph(row[0], ParagraphStyle('c', fontName='Arial-Bold', fontSize=9, leading=12)),
            Paragraph(row[1], ParagraphStyle('c', fontName='Arial', fontSize=9, leading=12, alignment=TA_CENTER)),
            Paragraph(row[2], ParagraphStyle('c', fontName='Arial', fontSize=9, leading=12)),
        ])
    roles_headers = [
        Paragraph(h, ParagraphStyle('h', fontName='Arial-Bold', fontSize=9, textColor=white))
        for h in roles_data[0]
    ]
    roles_table = Table([roles_headers] + roles_formatted,
        colWidths=[4*cm, 3*cm, 10*cm])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_TABLE_HDR),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(roles_table)

    story.append(Spacer(1, 12))
    story.append(Paragraph("Regula Minimă de Completare", S_H2))
    story.append(Paragraph(
        "Fiecare linie de producție trebuie să aibă cel puțin <b>2 FAI-uri completate "
        "pe zi</b> (câte unul la fiecare schimb de tur). Dacă în timpul turului se "
        "schimbă ordinul de producție, este necesar un FAI suplimentar pentru noul ordin.",
        S_BODY))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>⚠️ IMPORTANT:</b> Sistemul de enforcement este activ 24/7. Turul de noapte "
        "(23:30) este monitorizat doar dacă există producție activă detectată în tabelul "
        "Scannings.",
        S_WARNING_BOX))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 10. FAQ
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("10. Întrebări Frecvente (FAQ)", S_H1))
    story.append(section_line())

    faqs = [
        ("Ce se întâmplă dacă nu completez FAI-ul la timp?",
         "Sistemul declanșează automat escaladarea: după 60 de minute, șeful de secție "
         "este notificat. După 90 de minute, șeful de producție. După 120 de minute, "
         "responsabilul calitate și administratorul primesc notificarea, iar un "
         "referat disciplinar este generat automat."),
        ("Cum știe sistemul dacă sunt prezent în tur?",
         "Sistemul verifică prezența prin procedura stocată GetEmployeesTimeclockReal "
         "din baza de date Timeclocking. Doar angajații care au pontaj de intrare "
         "în intervalul turului curent sunt monitorizați."),
        ("Ce este LabelCode?",
         "LabelCode este un cod unic atribuit fiecărei sesiuni de validare FAI. "
         "Toate răspunsurile individuale (pe fiecare pas) din aceeași sesiune au "
         "același LabelCode. Este folosit pentru gruparea și filtrarea rezultatelor."),
        ("De câte FAI-uri am nevoie pe zi?",
         "Minim 2 per linie (câte unul per schimb). Dacă în timpul turului se "
         "schimbă ordinul, este necesar un FAI suplimentar."),
        ("Ce se întâmplă când apare un ordin nou?",
         "Sistemul monitorizează la fiecare oră tabelul Scannings pentru a detecta "
         "ordine noi intrate în producție. Dacă ordinul are un template FAI asociat "
         "și FAI-ul nu este completat, se declanșează ciclul de escaladare."),
        ("Cum se generează referatul disciplinar automat?",
         "La Nivelul 3 de escaladare, sistemul: (1) generează un număr de document "
         "prin SP Registro, (2) înregistrează în EmployeeDisciplinaryHistory, "
         "(3) creează un PDF cu semnătura administratorului, (4) trimite email-ul "
         "cu PDF-ul atașat."),
        ("Pot vedea istoricul escaladărilor?",
         "Da, toate evenimentele sunt înregistrate în tabelul fai.FaiEnforcementLog. "
         "Se poate interoga pentru: tipul evenimentului, nivelul de escaladare, "
         "dacă FAI-ul a fost completat ulterior, și dacă a fost generat un referat."),
    ]

    for q, a in faqs:
        story.append(Paragraph(f"<b>Î: {q}</b>", ParagraphStyle('Q',
            fontName='Arial-Bold', fontSize=10, leading=14,
            textColor=C_PRIMARY, spaceBefore=10, spaceAfter=4)))
        story.append(Paragraph(f"R: {a}", ParagraphStyle('A',
            fontName='Arial', fontSize=10, leading=14,
            leftIndent=15, spaceAfter=8)))

    # ── Build ──────────────────────────────────────────────────
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"\n[OK] Manual FAI generat: {filepath}")
    return filepath


if __name__ == "__main__":
    path = build_fai_manual()
    try:
        os.startfile(path)
    except Exception:
        pass
