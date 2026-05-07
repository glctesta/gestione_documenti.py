"""
Genera il PDF del manuale Materiale Indirecte in rumeno.
Usa ReportLab con font Arial per supporto caratteri rumeni.
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Font Registration ──
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
    FONT = 'Arial'
    FONT_BOLD = 'Arial-Bold'
except Exception:
    FONT = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

# ── Styles ──
styles = getSampleStyleSheet()

S_TITLE = ParagraphStyle('ManTitle', fontName=FONT_BOLD, fontSize=20, leading=26,
                          alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor('#1a237e'))
S_SUBTITLE = ParagraphStyle('ManSub', fontName=FONT, fontSize=10, alignment=TA_CENTER,
                             spaceAfter=20, textColor=colors.HexColor('#555555'))
S_H1 = ParagraphStyle('H1', fontName=FONT_BOLD, fontSize=15, leading=20,
                       spaceBefore=18, spaceAfter=8, textColor=colors.HexColor('#1565c0'))
S_H2 = ParagraphStyle('H2', fontName=FONT_BOLD, fontSize=12, leading=16,
                       spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#2e7d32'))
S_H3 = ParagraphStyle('H3', fontName=FONT_BOLD, fontSize=10, leading=14,
                       spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#37474f'))
S_BODY = ParagraphStyle('Body', fontName=FONT, fontSize=9.5, leading=13,
                         spaceAfter=4, alignment=TA_JUSTIFY)
S_BULLET = ParagraphStyle('Bullet', fontName=FONT, fontSize=9.5, leading=13,
                           leftIndent=20, spaceAfter=3, bulletIndent=8)
S_NOTE = ParagraphStyle('Note', fontName='Arial-Italic' if FONT == 'Arial' else 'Helvetica-Oblique',
                         fontSize=9, leading=12, leftIndent=15, textColor=colors.HexColor('#666666'),
                         spaceBefore=4, spaceAfter=6)
S_CODE = ParagraphStyle('Code', fontName='Courier', fontSize=8, leading=11,
                         leftIndent=15, spaceAfter=6, backColor=colors.HexColor('#f5f5f5'))

TBL_STYLE = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
    ('FONTNAME', (0, 1), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#bdbdbd')),
    ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#e0e0e0')),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
])

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    w = col_widths or [None] * len(headers)
    t = Table(data, colWidths=w, repeatRows=1)
    t.setStyle(TBL_STYLE)
    return t

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e0e0e0'),
                      spaceBefore=6, spaceAfter=6)

def build_pdf():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(out_dir, "Manual_Materiale_Indirecte_RO.pdf")

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []
    W = doc.width

    # ══════════════════════════════════════════════════════════════
    # COVER
    # ══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("MANUAL DE UTILIZARE", S_TITLE))
    story.append(Paragraph("Materiale Indirecte (Materiale de Consum)", S_TITLE))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Aplicație: TraceabilityRS — DocumentManagement<br/>"
                            "Versiune document: 1.0 — 22/04/2026", S_SUBTITLE))
    story.append(Spacer(1, 2*cm))

    # TOC
    toc_items = [
        "1. Prezentare generală",
        "2. Structura meniului",
        "3. Solicitare Materiale Indirecte",
        "4. Confirmare Materiale (Istoric Cereri)",
        "5. Import Coduri Materiale (Aliniere Coduri)",
        "6. Configurare Coduri Materiale",
        "7. Tipuri Materiale",
        "8. Confirmare WH WorkStation",
        "9. Monitorizare Automată (WH Monitor &amp; Requester Monitor)",
        "10. Generare PDF — Cerere de Material de Consum",
        "11. Schema Bazei de Date",
        "12. Fluxul Complet de Lucru",
    ]
    story.append(Paragraph("Cuprins", S_H2))
    for item in toc_items:
        story.append(Paragraph(f"• {item}", S_BULLET))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 1. PREZENTARE GENERALĂ
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Prezentare Generală", S_H1))
    story.append(Paragraph(
        "Modulul <b>Materiale Indirecte</b> permite gestionarea completă a materialelor de consum "
        "(consumabile de producție) prin intermediul aplicației TraceabilityRS.", S_BODY))
    funcs = [
        "<b>Importul</b> codurilor de materiale din fișiere Excel exportate din Dynamics",
        "<b>Configurarea</b> regulilor de fracționare și cantitate standard per cod material",
        "<b>Solicitarea</b> materialelor de către operatori/departamente",
        "<b>Notificarea automată</b> a depozitului (WH) prin popup-uri cu semnale sonore",
        "<b>Confirmarea</b> și <b>pregătirea</b> cererilor de către personalul de depozit",
        "<b>Notificarea automată</b> a solicitantului când materialul este pregătit",
        "<b>Generarea PDF</b> oficial - Cerere de Material de Consum - cu posibilitate de tip\u0103rire",
    ]
    for f in funcs:
        story.append(Paragraph(f"• {f}", S_BULLET))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 2. STRUCTURA MENIULUI
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Structura Meniului", S_H1))
    story.append(Paragraph("Meniu principal: <b>Materiale → Materiale Indirecte</b>", S_BODY))
    menu_data = [
        ["Materiale Indirecte", "Solicitare Materiale", "Cerere nouă (necesită autorizare)"],
        ["", "Confirmare Materiale", "Istoric cereri + ristampare PDF"],
        ["Configurații", "Confirmare WH WorkStation", "Activare/dezactivare stație WH"],
        ["", "Aliniere Coduri", "Import coduri din Excel (necesită autorizare)"],
        ["", "Configurare Coduri", "Reguli per-cod (necesită autorizare)"],
        ["", "Tipuri Materiale", "CRUD tipuri materiale"],
    ]
    story.append(make_table(["Submeniu", "Funcție", "Descriere"],
                             menu_data, [3.5*cm, 4.5*cm, W-8*cm]))
    story.append(Paragraph('<i>Not\u0103: Func\u021biile cu "necesit\u0103 autorizare" solicit\u0103 autentificarea \u00eenainte de deschidere.</i>', S_NOTE))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 3. SOLICITARE MATERIALE
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Solicitare Materiale Indirecte", S_H1))
    story.append(Paragraph("Acces: Materiale → Materiale Indirecte → <b>Solicitare Materiale</b>", S_BODY))
    story.append(Paragraph("Protecție: Necesită autorizare (login cu rol autorizat)", S_BODY))

    story.append(Paragraph("3.1 Descriere", S_H2))
    story.append(Paragraph(
        "Permite operatorilor să solicite materiale de consum din depozit. Interfața afișează lista "
        "completă a materialelor active cu stocul disponibil în timp real.", S_BODY))

    story.append(Paragraph("3.2 Pași de utilizare", S_H2))
    steps = [
        "<b>Deschideți</b> fereastra din meniu → se solicită autentificarea",
        "<b>Filtrați</b> materialele folosind câmpurile Cod și Descriere (butonul Curăță resetează filtrele)",
        "<b>Selectați</b> materialul dorit din tabel (Cod, Descriere, Tip, Stoc, Ambalaj, Fracționabil)",
        "<b>Introduceți cantitatea</b> — Material fracționabil: cantitate liberă, max = stoc; "
        "Material non-fracționabil: multiplu al ambalajului standard",
        "<b>Trimiteți cererea</b> cu butonul Trimite Cerere",
    ]
    for i, s in enumerate(steps, 1):
        story.append(Paragraph(f"{i}. {s}", S_BULLET))

    story.append(Paragraph("3.3 Reguli de Validare", S_H2))
    val_data = [
        ["Stoc insuficient", "Cantitatea solicitată nu poate depăși stocul disponibil"],
        ["Non-fracționabil", "Cantitatea trebuie să fie multiplu exact al cantității standard"],
        ["Cantitate pozitivă", "Cantitatea trebuie să fie > 0"],
    ]
    story.append(make_table(["Regulă", "Descriere"], val_data, [4*cm, W-4*cm]))

    story.append(Paragraph("3.4 Ce se întâmplă la trimitere", S_H2))
    story.append(Paragraph(
        "Se creează o înregistrare în tabela <b>ind.MaterialiRichieste</b> cu starea RICHIESTA. "
        "Se înregistrează: MaterialeId, cantitatea, stocul la momentul cererii, numele solicitantului, "
        "hostname-ul computerului. Monitorul WH detectează automat cererea.", S_BODY))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 4. CONFIRMARE MATERIALE
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Confirmare Materiale (Istoric Cereri)", S_H1))
    story.append(Paragraph("Acces: Materiale → Materiale Indirecte → <b>Confirmare Materiale</b>", S_BODY))
    story.append(Paragraph("Protecție: Fără autorizare — acces liber", S_BODY))
    story.append(Paragraph(
        "Afișează tabelul complet al tuturor cererilor de materiale indirecte (ID, Data, Cod, Descriere, "
        "Cantitate, Stare, Solicitant, Pregătitor). Permite ristamparea PDF-ului pentru orice cerere selectată.", S_BODY))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 5. IMPORT CODURI
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("5. Import Coduri Materiale (Aliniere Coduri)", S_H1))
    story.append(Paragraph("Acces: Materiale → Configurații → <b>Aliniere Coduri</b>", S_BODY))
    story.append(Paragraph("Protecție: Necesită autorizare", S_BODY))

    story.append(Paragraph("5.1 Format Excel așteptat", S_H2))
    story.append(Paragraph("Fișierul Excel trebuie să respecte formatul export Dynamics:", S_BODY))
    excel_data = [
        ["A (Coloana 1)", "Cod Material"],
        ["B (Coloana 2)", "Descriere"],
        ["H (Coloana 8)", "Cantitate Stoc"],
        ["Q (Coloana 17)", "Tip Material"],
    ]
    story.append(make_table(["Coloană Excel", "Conținut"], excel_data, [4*cm, W-4*cm]))
    story.append(Paragraph("<i>Prima linie (antet) este ignorată automat. Liniile fără cod material sunt omise.</i>", S_NOTE))

    story.append(Paragraph("5.2 Pași de utilizare", S_H2))
    imp_steps = [
        "Deschideți fereastra din meniu → se solicită autentificarea",
        "Apăsați <b>Selectează Excel</b> și alegeți fișierul .xlsx",
        "Datele sunt afișate în tabelul de previzualizare",
        "Verificați datele, apoi apăsați butonul <b>Importă</b>",
        'Confirma\u021bi dialogul: "Importare N coduri materiale?"',
        "Se execută importul cu bara de progres",
    ]
    for i, s in enumerate(imp_steps, 1):
        story.append(Paragraph(f"{i}. {s}", S_BULLET))

    story.append(Paragraph("5.3 Logica de Import (Tranzacție Atomică)", S_H2))
    story.append(Paragraph(
        "Întregul proces este executat într-o <b>singură tranzacție</b> de bază de date. "
        "Dacă apare o eroare, toate modificările sunt anulate (ROLLBACK).", S_BODY))

    phases = [
        ["Faza 0", "Tip Generico", 'Caut\u0103/creeaz\u0103 tipul "Generico" ca default'],
        ["Faza 1", "Upsert Anagrafica", "Dacă codul există → UPDATE; dacă nu → INSERT în ind.Materiali"],
        ["Faza 2", "Soft-Close Stocuri", "DateOut = GETDATE() DOAR pe materialele importate"],
        ["Faza 3", "Insert Stocuri Noi", "INSERT în ind.MaterialiStock cu DateOut = NULL"],
        ["Final", "COMMIT / ROLLBACK", "Succes → COMMIT unic; Eroare → ROLLBACK complet"],
    ]
    story.append(make_table(["Fază", "Operație", "Descriere"], phases, [2*cm, 3.5*cm, W-5.5*cm]))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 6. CONFIGURARE CODURI
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Configurare Coduri Materiale", S_H1))
    story.append(Paragraph("Acces: Materiale → Configurații → <b>Configurare Coduri</b>", S_BODY))
    story.append(Paragraph(
        "Permite configurarea regulilor specifice per cod material: dacă este fracționabil și care "
        "este cantitatea standard. Aceste configurări suprascriu regulile implicite ale tipului.", S_BODY))

    story.append(Paragraph("6.1 Ierarhia Regulilor", S_H2))
    story.append(Paragraph(
        "<b>MaterialConfigurations (per-cod)</b> → prioritate MAXIMĂ. Dacă nu există, se folosesc "
        "valorile din <b>TipoMateriali (per-tip)</b> → valori implicite.", S_BODY))

    story.append(Paragraph("6.2 Operațiuni", S_H2))
    ops = [
        ["💾 Salvează", "Creează sau actualizează configurația per-cod"],
        ["🗑️ Dezactivează", "Soft-delete (setează DateOut = GETDATE())"],
        ["♻️ Reactivează", "Restaurează o configurare dezactivată (DateOut = NULL)"],
    ]
    story.append(make_table(["Acțiune", "Descriere"], ops, [3.5*cm, W-3.5*cm]))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 7. TIPURI MATERIALE
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("7. Tipuri Materiale", S_H1))
    story.append(Paragraph("Acces: Materiale → Configurații → <b>Tipuri Materiale</b>", S_BODY))
    story.append(Paragraph(
        "Gestionarea categoriilor de materiale indirecte. Fiecare tip definește regulile implicite "
        "de fracționare și dimensiunea ambalajului.", S_BODY))
    tipo_ops = [
        ["➕ Adaugă", "Creează un tip nou"],
        ["💾 Salvează", "Actualizează tipul selectat"],
        ["🗑️ Elimină", "Șterge tipul (doar dacă nu are materiale asociate)"],
        ["🔄 Actualizează", "Reîncarcă lista din baza de date"],
    ]
    story.append(make_table(["Buton", "Acțiune"], tipo_ops, [3.5*cm, W-3.5*cm]))
    story.append(Paragraph("<i>Un tip nu poate fi eliminat dacă are materiale asociate.</i>", S_NOTE))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 8. WH WORKSTATION
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("8. Confirmare WH WorkStation", S_H1))
    story.append(Paragraph("Acces: Materiale → Configurații → <b>Confirmare WH WorkStation</b>", S_BODY))
    story.append(Paragraph(
        "Identifică computerul curent ca stație de depozit (Warehouse). Când este activată, pe "
        "acest computer vor apărea automat popup-urile de notificare pentru cereri noi.", S_BODY))
    story.append(Paragraph(
        "<b>Activare:</b> se creează fișierul wh_host.json în %LOCALAPPDATA% cu hostname, "
        "utilizator și data activării.<br/>"
        "<b>Dezactivare:</b> se șterge fișierul wh_host.json.", S_BODY))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 9. MONITORIZARE
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("9. Monitorizare Automată", S_H1))

    story.append(Paragraph("9.1 WH Monitor (Depozit)", S_H2))
    story.append(Paragraph(
        "Activ pe computerele cu WH WorkStation activată. Polling la fiecare 10 secunde. "
        "Verifică cererile cu starea RICHIESTA nenotificate sau notificate cu &gt; 5 min în urmă.", S_BODY))
    story.append(Paragraph(
        "Afișează un <b>popup roșu</b> cu 3 semnale sonore conținând: cod, descriere, cantitate, "
        "solicitant, data cererii, computer solicitant.", S_BODY))
    wh_btns = [
        ["✅ Pregătește și Confirmă", "Stare → PRONTA, generează și tipărește PDF"],
        ["🖨️ Tipărește", "Generează PDF fără schimbare de stare"],
        ["Închide", "Închide popup (se va renotifica după 5 min)"],
    ]
    story.append(make_table(["Buton", "Acțiune"], wh_btns, [4.5*cm, W-4.5*cm]))

    story.append(Paragraph("9.2 Requester Monitor (Solicitant)", S_H2))
    story.append(Paragraph(
        "Activ pe toate computerele. Polling la fiecare 10 secunde. Verifică cereri cu starea PRONTA "
        "al căror ComputerRichiedente corespunde hostname-ului curent.", S_BODY))
    story.append(Paragraph(
        "Afișează un <b>popup verde</b> cu 3 semnale sonore conținând: cod, descriere, cantitate, "
        "pregătit de, ora pregătirii.", S_BODY))
    req_btns = [
        ["✅ Ridicat", "Stare → PRELEVATA, înregistrează data ridicării"],
        ["⏳ Mai târziu", "Închide popup (se va renotifica după 5 min)"],
    ]
    story.append(make_table(["Buton", "Acțiune"], req_btns, [4.5*cm, W-4.5*cm]))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 10. PDF
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("10. Generare PDF — Cerere de Material de Consum", S_H1))
    story.append(Paragraph(
        'Documentul generat se intituleaz\u0103 <b>CERERE DE MATERIAL DE CONSUM</b> \u0219i con\u021bine: '
        "logo Vandewiele, număr cerere, data și ora, tabel material (cod, descriere, cantitate, stoc), "
        "solicitant, pregătitor, note, spații pentru semnături.", S_BODY))
    story.append(Paragraph(
        "PDF-ul este generat în directorul temporar (%TEMP%\\ind_materials\\) și poate fi tipărit automat "
        "pe imprimanta implicită Windows sau deschis în vizualizatorul PDF implicit.", S_BODY))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 11. SCHEMA DB
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("11. Schema Bazei de Date", S_H1))

    story.append(Paragraph("11.1 Tabele Principale", S_H2))
    db_tables = [
        ["ind.TipoMateriali", "TipoMaterialeId, Tipo, IsFrazionabile, QtaConfezione"],
        ["ind.Materiali", "MaterialeId, CodiceMateriale, DescrizioneMateriale, TipoMaterialeId, IsActive"],
        ["ind.MaterialiStock", "MaterialeId, Qty, DateIn, DateOut (NULL=activ), CaricatoDa"],
        ["ind.MaterialiRichieste", "RichiestaId, MaterialeId, QtaRichiesta, Stato, DataRichiesta, "
         "RichiestoDa, ComputerRichiedente, PreparatoDa, DataPreparazione, DataPrelievo, ..."],
        ["dbo.MaterialConfigurations", "MaterialConfigurationId, MaterialId, IsFractionabil, "
         "QuantityStandard, DateOut (NULL=activ)"],
    ]
    story.append(make_table(["Tabel", "Câmpuri principale"], db_tables, [4*cm, W-4*cm]))

    story.append(Paragraph("11.2 Stări Cereri (ind.MaterialiRichieste.Stato)", S_H2))
    stati = [
        ["RICHIESTA", "Cerere trimisă, în așteptare la depozit"],
        ["PRONTA", "Material pregătit de depozit, în așteptare ridicare"],
        ["PRELEVATA", "Material ridicat de solicitant"],
    ]
    story.append(make_table(["Valoare", "Semnificație"], stati, [3*cm, W-3*cm]))
    story.append(hr())

    # ══════════════════════════════════════════════════════════════
    # 12. FLUX COMPLET
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("12. Fluxul Complet de Lucru", S_H1))

    story.append(Paragraph("12.1 Configurare (o singură dată)", S_H2))
    config_steps = [
        "Configurare WH WorkStation → Activare pe PC-ul depozitului",
        "Import Coduri (Aliniere) → Import Excel din Dynamics",
        "Tipuri Materiale → Definire categorii + reguli implicite",
        "Configurare Coduri → Override per-cod (opțional)",
    ]
    for i, s in enumerate(config_steps, 1):
        story.append(Paragraph(f"{i}. {s}", S_BULLET))

    story.append(Paragraph("12.2 Flux operațional zilnic", S_H2))
    flow_data = [
        ["Pasul 1", "SOLICITANT", "Deschide Solicitare Materiale → selectează → introduce cantitatea → "
         "trimite cererea. Stare: RICHIESTA"],
        ["Pasul 2", "DEPOZIT (auto)", "Pe PC-ul WH apare popup roșu cu sunet de alarmă. "
         "Personalul pregătește materialul, apasă Pregătește și Confirmă → tipărire PDF. "
         "Stare: PRONTA"],
        ["Pasul 3", "SOLICITANT (auto)", "Pe PC-ul solicitantului apare popup verde cu sunet. "
         "Solicitantul ridică materialul, apasă Ridicat. Stare: PRELEVATA"],
    ]
    story.append(make_table(["Pas", "Actor", "Descriere"], flow_data, [2*cm, 3.5*cm, W-5.5*cm]))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Document generat pentru uzul intern Vandewiele România. "
                            "Toate drepturile rezervate.", S_NOTE))

    # ── Build ──
    doc.build(story)
    print(f"PDF generat cu succes: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
