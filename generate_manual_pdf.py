# -*- coding: utf-8 -*-
"""
Genera il manuale PDF del menu Personal in rumeno.
Usa ReportLab con font Arial per supporto diacritici rumeni.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Logo.png")
OUTPUT_DIR = r"C:\Temp"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Manual_Personal_RO.pdf")

BLUE_DARK  = HexColor("#1a237e")
BLUE_MED   = HexColor("#283593")
BLUE_LIGHT = HexColor("#e8eaf6")
GRAY_LIGHT = HexColor("#f5f5f5")
GRAY_MED   = HexColor("#e0e0e0")
ACCENT     = HexColor("#0d47a1")
ORANGE     = HexColor("#e65100")
GREEN_D    = HexColor("#2e7d32")

WINFONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial",        os.path.join(WINFONTS, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold",   os.path.join(WINFONTS, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(WINFONTS, "ariali.ttf")))

styles = getSampleStyleSheet()

title_style = ParagraphStyle("ManualTitle", parent=styles["Title"],
    fontName="Arial-Bold", fontSize=26, textColor=BLUE_DARK,
    spaceAfter=6*mm, alignment=TA_CENTER)

subtitle_style = ParagraphStyle("ManualSubtitle", parent=styles["Normal"],
    fontName="Arial", fontSize=12, textColor=HexColor("#616161"),
    spaceAfter=10*mm, alignment=TA_CENTER)

h1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=18,
    textColor=white, spaceAfter=4*mm, spaceBefore=8*mm,
    leftIndent=4*mm, leading=22, backColor=BLUE_DARK,
    borderPadding=(3*mm, 3*mm, 2*mm, 3*mm))

h2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=14,
    textColor=BLUE_MED, spaceAfter=3*mm, spaceBefore=6*mm,
    borderWidth=0, borderColor=BLUE_MED, borderPadding=(0, 0, 1, 0), leading=18)

h3 = ParagraphStyle("H3", fontName="Arial-Bold", fontSize=11,
    textColor=ACCENT, spaceAfter=2*mm, spaceBefore=4*mm, leading=14)

body = ParagraphStyle("Body", fontName="Arial", fontSize=10,
    textColor=black, spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)

body_indent = ParagraphStyle("BodyIndent", parent=body, leftIndent=8*mm)

bullet = ParagraphStyle("Bullet", parent=body, leftIndent=10*mm,
    bulletIndent=5*mm, spaceBefore=1*mm, spaceAfter=1*mm)

note_style = ParagraphStyle("Note", fontName="Arial-Italic", fontSize=9,
    textColor=HexColor("#1565c0"), spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=BLUE_LIGHT,
    borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))

important_style = ParagraphStyle("Important", fontName="Arial-Bold", fontSize=9,
    textColor=ORANGE, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#fff3e0"),
    borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))

tip_style = ParagraphStyle("Tip", fontName="Arial-Italic", fontSize=9,
    textColor=GREEN_D, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#e8f5e9"),
    borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))


def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if not col_widths:
        col_widths = [None] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), BLUE_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), white),
        ("FONTNAME",      (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Arial"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, GRAY_LIGHT]),
        ("GRID",          (0, 0), (-1, -1), 0.5, GRAY_MED),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ]))
    return t

def menu_path(path):
    return Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Meniu: </font>'
        '<font name="Arial" size="9" color="#0d47a1">%s</font>' % path, body)

def access_line(text):
    return Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
        '<font name="Arial-Italic" size="9">%s</font>' % text, body)

def sp(v=3):
    return Spacer(1, v * mm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GRAY_MED,
                      spaceBefore=3*mm, spaceAfter=3*mm)


def on_page(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Arial", 8)
    canvas_obj.setFillColor(HexColor("#9e9e9e"))
    txt = "Manual de Utilizare - Meniul Personal - TraceabilityRS v2.3.6 - Pagina %d" % doc.page
    canvas_obj.drawCentredString(A4[0] / 2, 12 * mm, txt)
    canvas_obj.setStrokeColor(BLUE_LIGHT)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(15*mm, A4[1] - 12*mm, A4[0] - 15*mm, A4[1] - 12*mm)
    canvas_obj.restoreState()


def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    story = []
    W = A4[0] - 36*mm

    # ===== COVER PAGE =====
    story.append(sp(25))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=60*mm, height=30*mm, hAlign="CENTER"))
    story.append(sp(15))
    story.append(Paragraph("Manual de Utilizare", title_style))
    story.append(Paragraph('Meniul "Personal"', ParagraphStyle("Sub",
        fontName="Arial-Bold", fontSize=18, textColor=BLUE_MED,
        alignment=TA_CENTER, spaceAfter=8*mm)))
    story.append(Paragraph("TraceabilityRS - Versiune 2.3.6", subtitle_style))
    story.append(sp(10))
    story.append(hr())
    story.append(sp(5))

    story.append(Paragraph("Structura Meniului", h2))
    overview = [
        ["Nr.", "Sectiune", "Sub-meniuri"],
        ["1", "Oaspeti", "Inregistrare, Raport PDF, Setari (Hotels, Companii Aeriene, Shuttle, Reguli, Gestiune)"],
        ["2", "Absente", "Autorizare Absente, Reguli Absente"],
        ["3", "Note Disciplinare", "Creare, PDF, Email automat"],
        ["4", "Comisie Disciplinara", "(dezactivat)"],
        ["5", "Mesaje", "Gestionare mesaje Kiosk"],
        ["6", "Ore Suplimentare", "Cereri, Autorizare, Rapoarte, Analiza, Raspunsuri"],
        ["7", "Programe Externe", "SetUp IP, Deschide Program"],
    ]
    t = Table(overview, colWidths=[12*mm, 42*mm, W - 54*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), BLUE_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), white),
        ("FONTNAME",      (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Arial"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, GRAY_LIGHT]),
        ("GRID",          (0, 0), (-1, -1), 0.5, GRAY_MED),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ===== 1. OASPETI =====
    story.append(Paragraph("1. Oaspeti", h1))

    story.append(Paragraph("1.1 Inregistrare Oaspeti", h2))
    story.append(menu_path("Personal > Oaspeti > Inregistrare Oaspeti"))
    story.append(access_line("Necesita autentificare (login)"))
    story.append(sp(2))
    story.append(Paragraph(
        "Permite inregistrarea vizitatorilor care vin in fabrica. "
        "Formularul ofera campuri pentru compania vizitatorului, numele, "
        "datele vizitei, motivul si persoana de referinta.", body))

    story.append(sp(2))
    story.append(Paragraph("Campuri obligatorii:", h3))
    story.append(make_table(
        ["Camp", "Descriere"],
        [
            ["Companie *", "Selectati din lista existenta sau introduceti o companie noua"],
            ["Nume Oaspete *", "Selectati din lista sau introduceti un nume nou (salvat in MAJUSCULE)"],
            ["Data Inceput *", "Data de sosire a vizitatorului"],
            ["Data Sfarsit *", "Data de plecare a vizitatorului"],
            ["Motiv *", "Scopul vizitei (ex: Quality Assurance, Audit)"],
            ["Mesaj de Bun Venit", 'Text afisat pe ecranul de bun venit (implicit: "Welcome in our factory")'],
            ["Persoana de Referinta *", "Angajatul responsabil, selectat din lista angajatilor activi"],
        ],
        col_widths=[40*mm, W - 40*mm]
    ))

    story.append(sp(3))
    story.append(Paragraph("Butoane disponibile:", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Nou</b> - curata formularul pentru o noua inregistrare", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Salveaza</b> - salveaza vizita in baza de date", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Modifica</b> - actualizeaza datele vizitei selectate din tabel", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Sterge</b> - elimina vizita selectata", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Inchide</b> - daca au fost inregistrati oaspeti noi, deschide automat Booking (hotel/shuttle)", bullet))

    story.append(sp(2))
    story.append(Paragraph(
        "NOTA: Daca compania nu exista, sistemul propune crearea automata. "
        "Daca oaspetele exista deja in baza de date (cu alta companie), va fi reutilizat automat. "
        "La inchidere, oaspetii sunt grupati pe data de sosire pentru booking-ul serviciilor.", note_style))

    story.append(sp(3))
    story.append(Paragraph("Lista vizitatorilor (panoul inferior):", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Filtreaza</b> - filtreaza lista dupa data selectata din calendar", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Arata Tot</b> - afiseaza ultimii 50 de vizitatori (30 zile)", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Tipareste Lista</b> - genereaza si tipareste raportul PDF pentru data filtrata", bullet))

    story.append(sp(4))
    story.append(Paragraph("1.2 Raport Oaspeti (PDF)", h2))
    story.append(menu_path("Personal > Oaspeti > Raport Oaspeti"))
    story.append(access_line("Necesita autentificare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Genereaza un raport PDF in format A4 cu toti vizitatorii prezenti in fabrica "
        "in ziua curenta. Raportul include:", body))
    story.append(Paragraph("<bullet>&bull;</bullet> Antet cu logo-ul companiei", bullet))
    story.append(Paragraph('<bullet>&bull;</bullet> Titlu: "LISTA VIZITATORI PREZENTI"', bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Tabel: Nume Vizitator, Companie, Ora Sosire, Ora Plecare", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Nota legala in limba romana pentru departamentul de personal", bullet))
    story.append(sp(2))
    story.append(Paragraph(
        "La generare, se salveaza in C:\\Temp, se deschide automat si se actualizeaza "
        "campul PrintedOn in baza de date.", body))

    story.append(sp(4))
    story.append(Paragraph("1.3 Setari Oaspeti", h2))
    settings_items = [
        ("1.3.1 Hoteluri", "Personal > Oaspeti > Setari > Hoteluri",
         "Gestioneaza lista hotelurilor disponibile pentru cazarea vizitatorilor: "
         "adaugare, modificare, stergere (nume, adresa, telefon, email, tarif)."),
        ("1.3.2 Companii Aeriene", "Personal > Oaspeti > Setari > Companii Aeriene",
         "Gestioneaza lista companiilor aeriene pentru aranjamentele de zbor: "
         "adaugare, modificare, stergere (nume, cod IATA)."),
        ("1.3.3 Shuttle", "Personal > Oaspeti > Setari > Shuttle",
         "Gestioneaza serviciile de transport (shuttle): furnizor, contact, tarif."),
        ("1.3.4 Reguli", "Personal > Oaspeti > Setari > Reguli",
         "Configureaza regulile pentru gestionarea vizitatorilor: "
         "notificari automate, restrictii de acces, parametri de validare."),
        ("1.3.5 Gestiune Oaspeti", "Personal > Oaspeti > Setari > Gestiune Oaspeti",
         "Administrare centralizata a datelor oaspetilor: cautare, filtrare, "
         "modificare date personale (email, companie), vizualizare istoricul vizitelor."),
    ]
    for title, path, desc in settings_items:
        story.append(Paragraph(title, h3))
        story.append(menu_path(path))
        story.append(Paragraph(desc, body_indent))
        story.append(sp(1))
    story.append(PageBreak())

    # ===== 2. ABSENTE =====
    story.append(Paragraph("2. Absente", h1))

    story.append(Paragraph("2.1 Autorizare Absente", h2))
    story.append(menu_path("Personal > Absente > Autorizare Absente"))
    story.append(access_line("Necesita autentificare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Permite managerilor sa vizualizeze, aprobe sau respinga cererile de absenta "
        "ale angajatilor din echipa lor.", body))

    story.append(sp(2))
    story.append(Paragraph("Tipuri de cereri gestionate:", h3))
    story.append(make_table(
        ["Tip", "Descriere"],
        [
            ["Concediu de odihna", "Zile de concediu anual (zilele disponibile se calculeaza automat)"],
            ["Bilet de voie", "Permis temporar de iesire din fabrica"],
            ["Invoire", "Absenta pe fractiune de zi"],
            ["Concediu medical", "Zile de boala"],
            ["Alte tipuri", "Conform codurilor din sistemul de pontaj"],
        ],
        col_widths=[40*mm, W - 40*mm]
    ))

    story.append(sp(3))
    story.append(Paragraph("Flux de aprobare:", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> 1. Angajatul depune cererea (din sistemul Kiosk sau alta interfata)", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> 2. Managerul deschide <b>Autorizare Absente</b>", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> 3. Se afiseaza cererile in asteptare pentru echipa managerului", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> 4. Managerul aproba sau respinge fiecare cerere", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> 5. La aprobare, absenta se sincronizeaza cu sistemul de pontaj", bullet))

    story.append(sp(2))
    story.append(Paragraph(
        "IMPORTANT: Pentru concediul de odihna, sistemul calculeaza automat zilele "
        "disponibile (GiorniDisponibili), tinand cont de: vechime, bonusuri, sarbatori "
        "legale si zile deja utilizate in anul curent.", important_style))

    story.append(sp(3))
    story.append(Paragraph("2.2 Reguli Absente", h2))
    story.append(menu_path("Personal > Absente > Reguli Absente"))
    story.append(access_line("Necesita autentificare"))
    story.append(sp(2))
    story.append(Paragraph("Configureaza regulile si parametrii pentru diferitele tipuri de absenta:", body))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>DayNoZone</b> - nr. zile inainte de data necesare pentru depunerea cererii "
                           "(0 = se permite selectarea zilei curente)", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Restrictii pe tipuri de absenta", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Limite maxime per perioada", bullet))
    story.append(PageBreak())

    # ===== 3. NOTE DISCIPLINARE =====
    story.append(Paragraph("3. Note Disciplinare (Referat)", h1))
    story.append(menu_path("Personal > Note Disciplinare"))
    story.append(access_line("Necesita autorizare (permisii bazate pe rol)"))
    story.append(sp(2))
    story.append(Paragraph(
        "Modul specializat pentru emiterea si gestionarea referatelor disciplinare, "
        "inlocuind functionalitatea din vechiul sistem Access.", body))

    story.append(sp(2))
    story.append(Paragraph("Creare referat nou:", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> Selectare angajat din lista activa", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Completare motiv / descriere a abaterii", bullet))
    story.append(Paragraph('<bullet>&bull;</bullet> Selectare articol legal (din baza de date, tip "DISCIPLINA")', bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Generare automata a numarului de registru (DocName)", bullet))

    story.append(sp(2))
    story.append(Paragraph("Generare PDF:", h3))
    story.append(Paragraph(
        "PDF format A4 Portrait cu font Arial, suport complet caractere romanesti. "
        "Include preambul generat automat adaptat la gen si departament, "
        "plus contextul legal al articolului selectat.", body_indent))

    story.append(sp(2))
    story.append(Paragraph("Notificare automata (email):", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Destinatari:</b> autorul referatului + angajatul vizat", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>CC:</b> lista din setarea Sys_email_referat", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Continut:</b> tabel rezumat HTML + logo + PDF atasat", bullet))

    story.append(sp(2))
    story.append(Paragraph(
        "NOTA: Stergerea nu este fizica - se marcheaza cu IsDeleted = 1, "
        "pastrand istoricul complet de audit.", note_style))

    # ===== 4. COMISIE DISCIPLINARA =====
    story.append(sp(4))
    story.append(Paragraph("4. Comisie Disciplinara", h1))
    story.append(sp(2))
    story.append(Paragraph(
        "Aceasta functie <b>nu este inca disponibila</b> (este dezactivata in meniu). "
        "Va permite gestionarea sedintelor comisiei disciplinare intr-o versiune viitoare.", body))

    # ===== 5. MESAJE =====
    story.append(sp(4))
    story.append(Paragraph("5. Mesaje", h1))
    story.append(menu_path("Personal > Mesaje"))
    story.append(access_line("Necesita autentificare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Gestioneaza mesajele si comunicarile interne afisate pe sistemul Kiosk "
        "si/sau aplicatia de bun venit.", body))
    story.append(sp(2))
    story.append(Paragraph("<bullet>&bull;</bullet> Creare mesaj nou (titlu, continut, perioada de afisare)", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Modificare mesaje existente", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Stergere mesaje expirate", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Mesajele active se afiseaza automat pe ecranele Kiosk", bullet))
    story.append(PageBreak())

    # ===== 6. ORE SUPLIMENTARE =====
    story.append(Paragraph("6. Ore Suplimentare", h1))

    story.append(Paragraph("6.1 Cereri", h2))
    story.append(menu_path("Personal > Ore Suplimentare > Cereri"))
    story.append(access_line("Necesita autorizare"))
    story.append(sp(2))
    story.append(Paragraph("Permite depunerea cererilor de ore suplimentare:", body))
    story.append(Paragraph("<bullet>&bull;</bullet> Selectare angajat sau echipa", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Definire perioada: data, ora de inceput, ora de sfarsit", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Introducere motivul orelor suplimentare", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Trimitere spre aprobare", bullet))

    story.append(sp(3))
    story.append(Paragraph("6.2 Autorizare", h2))
    story.append(menu_path("Personal > Ore Suplimentare > Autorizare"))
    story.append(access_line("Necesita autorizare (manager/responsabil)"))
    story.append(sp(2))
    story.append(Paragraph(
        "Procesul de aprobare sau respingere a cererilor de ore suplimentare. "
        "La aprobare se genereaza automat PDF-ul de autorizare.", body))
    story.append(sp(2))
    story.append(Paragraph("PDF-ul de autorizare contine:", h3))
    story.append(Paragraph("<bullet>&bull;</bullet> Logo companie", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Tabel cu: Angajat, Data, Ora de la, Ora la, Motiv", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Suma totala ore suplimentare", bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> Text in limba romana: predarea documentului la departamentul HR", bullet))

    story.append(sp(3))
    story.append(Paragraph("6.3 Rapoarte", h2))
    story.append(menu_path("Personal > Ore Suplimentare > Rapoarte"))
    story.append(access_line("Necesita autorizare"))
    story.append(sp(2))
    story.append(Paragraph("Genereaza rapoarte detaliate ale orelor suplimentare:", body))
    story.append(Paragraph('<bullet>&bull;</bullet> <b>PDF:</b> format A4 Portrait, cu coloane "Ora da"/"Ora a", '
                           'bloc rezumativ cu ipoteze de calcul', bullet))
    story.append(Paragraph("<bullet>&bull;</bullet> <b>Excel:</b> cu formule native =SUM(), filtrare automata pe antet", bullet))
    story.append(sp(2))
    story.append(Paragraph(
        "TIP: Daca fisierul Excel este deschis/blocat de alt utilizator, sistemul salveaza "
        "automat cu un nume alternativ cu timestamp in C:\\Temp.", tip_style))

    story.append(sp(3))
    story.append(Paragraph("6.4 Analiza", h2))
    story.append(menu_path("Personal > Ore Suplimentare > Analiza"))
    story.append(access_line("Necesita autorizare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Ofera o vizualizare analitica a orelor suplimentare: "
        "statistici per departament, tendinte lunare, comparatii pe perioade.", body))

    story.append(sp(3))
    story.append(Paragraph("6.5 Raspunsuri", h2))
    story.append(menu_path("Personal > Ore Suplimentare > Raspunsuri"))
    story.append(access_line("Necesita autorizare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Gestioneaza raspunsurile si feedback-ul privind cererile de ore suplimentare.", body))
    story.append(PageBreak())

    # ===== 7. PROGRAME EXTERNE =====
    story.append(Paragraph("7. Programe Externe", h1))

    story.append(Paragraph("7.1 SetUp IP", h2))
    story.append(menu_path("Personal > Programe Externe > SetUp IP"))
    story.append(access_line("Necesita autentificare"))
    story.append(sp(2))
    story.append(Paragraph(
        "Lanseaza utilitarul de configurare a adresei IP pentru echipamentele de retea.", body))

    story.append(sp(3))
    story.append(Paragraph("7.2 Deschide Program", h2))
    story.append(menu_path("Personal > Programe Externe > Deschide Program"))
    story.append(access_line("Acces direct"))
    story.append(sp(2))
    story.append(Paragraph(
        "Deschide aplicatia externa configurata in browser (aplicatie web asociata).", body))

    # ===== REFERINTE TEHNICE =====
    story.append(sp(6))
    story.append(hr())
    story.append(Paragraph("Referinte Tehnice", h2))
    story.append(make_table(
        ["Element", "Descriere"],
        [
            ["Baza de date principala", "Employee.dbo.*"],
            ["Tabel vizitatori", "Employee.dbo.Visitors"],
            ["Tabel date oaspeti", "Employee.dbo.VisitorData"],
            ["Tabel companii", "Employee.dbo.VisitorPlanToCharges"],
            ["Tabel furnizori transport", "Employee.dbo.VisitorSupportersData"],
            ["Tabel cereri absente", "Employee.dbo.AbsenceRequestes"],
            ["Tabel istoric disciplinar", "Employee.dbo.EmployeeDisciplinaryHistory"],
            ["Setari sistem", "Traceability_RS.dbo.Settings"],
            ["Traduceri", "Traceability_RS.dbo.AppTranslations"],
        ],
        col_widths=[50*mm, W - 50*mm]
    ))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("PDF generato: %s" % OUTPUT_FILE)
    return OUTPUT_FILE


if __name__ == "__main__":
    pdf = build()
    if os.name == "nt":
        os.startfile(pdf)
