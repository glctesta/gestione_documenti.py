# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Segnalazioni' in 5 lingue.
Produce: manuals/{lang}/segnalazioni_nuova.pdf
         manuals/{lang}/segnalazioni_assegna.pdf
         manuals/{lang}/segnalazioni_gestione.pdf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Logo.png")
BASE_DIR = os.path.join(os.path.dirname(__file__), "manuals")
BLUE_DARK = HexColor("#1a237e"); BLUE_MED = HexColor("#283593"); BLUE_LIGHT = HexColor("#e8eaf6")
GRAY_LIGHT = HexColor("#f5f5f5"); GRAY_MED = HexColor("#e0e0e0"); ACCENT = HexColor("#0d47a1")
ORANGE = HexColor("#e65100")
WINFONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial", os.path.join(WINFONTS, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(WINFONTS, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(WINFONTS, "ariali.ttf")))

title_style = ParagraphStyle("T", fontName="Arial-Bold", fontSize=22, textColor=BLUE_DARK, spaceAfter=4*mm, alignment=TA_CENTER)
sub_style = ParagraphStyle("S", fontName="Arial-Bold", fontSize=14, textColor=BLUE_MED, spaceAfter=8*mm, alignment=TA_CENTER)
h1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, textColor=white, spaceAfter=4*mm, spaceBefore=6*mm, leftIndent=4*mm, leading=20, backColor=BLUE_DARK, borderPadding=(3*mm,3*mm,2*mm,3*mm))
h2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=12, textColor=BLUE_MED, spaceAfter=2*mm, spaceBefore=5*mm, leading=16)
body = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black, spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
note_s = ParagraphStyle("N", fontName="Arial-Italic", fontSize=9, textColor=HexColor("#1565c0"), spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12, backColor=BLUE_LIGHT, borderPadding=(2*mm,2*mm,2*mm,2*mm))
warn_s = ParagraphStyle("W", fontName="Arial-Bold", fontSize=9, textColor=ORANGE, spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12, backColor=HexColor("#fff3e0"), borderPadding=(2*mm,2*mm,2*mm,2*mm))

def sp(v=3): return Spacer(1, v*mm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=GRAY_MED, spaceBefore=3*mm, spaceAfter=3*mm)
def make_table(headers, rows, W):
    data = [headers] + rows
    t = Table(data, colWidths=[42*mm, W-42*mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE_DARK),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Arial-Bold"),("FONTSIZE",(0,0),(-1,0),10),("FONTNAME",(0,1),(-1,-1),"Arial"),("FONTSIZE",(0,1),(-1,-1),9),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,GRAY_LIGHT]),("GRID",(0,0),(-1,-1),0.5,GRAY_MED),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),4)]))
    return t
def on_page(c, d, ft):
    c.saveState(); c.setFont("Arial",8); c.setFillColor(HexColor("#9e9e9e"))
    c.drawCentredString(A4[0]/2,12*mm,"%s - Pagina %d"%(ft,d.page))
    c.setStrokeColor(BLUE_LIGHT); c.setLineWidth(0.5); c.line(15*mm,A4[1]-12*mm,A4[0]-15*mm,A4[1]-12*mm); c.restoreState()

MANUALS = [
    ("segnalazioni_nuova", "new"),
    ("segnalazioni_assegna", "assign"),
    ("segnalazioni_gestione", "manage"),
]

TEXTS = {}
for lang, (footer, field_l, desc_l, titles, subtitles, descs, steps, fields, notes, warns) in {
    "it": ("TraceabilityRS - Segnalazioni", "Campo", "Descrizione",
        {"new":"Nuova Segnalazione","assign":"Assegna Segnalazione","manage":"Gestione Segnalazioni"},
        {"new":"Guida alla creazione di una nuova segnalazione","assign":"Guida all'assegnazione delle segnalazioni","manage":"Guida alla gestione delle segnalazioni"},
        {"new":"Questa funzione consente di creare una nuova segnalazione per problemi, anomalie o suggerimenti. "
               "La segnalazione viene registrata nel sistema e assegnata al reparto competente per la risoluzione.",
         "assign":"Questa funzione consente ai responsabili di assegnare le segnalazioni ricevute ai tecnici o reparti competenti. "
                  "L'assegnazione include la definizione della priorita' e della scadenza prevista.",
         "manage":"Questa funzione consente di gestire il ciclo completo delle segnalazioni: dalla ricezione alla chiusura. "
                  "Include il monitoraggio dello stato, l'aggiornamento delle azioni correttive e la generazione dei report."},
        {"new":["1. Tipo Segnalazione / Selezionare il tipo: problema di qualita', sicurezza, suggerimento, altro.",
                "2. Descrizione / Inserire una descrizione dettagliata del problema o suggerimento.",
                "3. Allegati / Allegare eventuali foto, documenti o evidenze.",
                "4. Invio / Fare clic su 'Invia' per registrare la segnalazione."],
         "assign":["1. Lista Segnalazioni / Visualizzare le segnalazioni in attesa di assegnazione.",
                   "2. Seleziona Responsabile / Selezionare il tecnico o reparto responsabile.",
                   "3. Priorita' e Scadenza / Definire la priorita' (Alta, Media, Bassa) e la data di scadenza.",
                   "4. Conferma / Confermare l'assegnazione. Il responsabile ricevera' una notifica email."],
         "manage":["1. Dashboard / Visualizzare la dashboard con lo stato di tutte le segnalazioni.",
                   "2. Filtri / Filtrare per stato, priorita', reparto o periodo.",
                   "3. Aggiornamenti / Aggiornare lo stato e le azioni intraprese per ogni segnalazione.",
                   "4. Chiusura / Chiudere la segnalazione dopo la verifica della risoluzione."]},
        {"new":[("Tipo *","Tipo di segnalazione (Qualita', Sicurezza, Suggerimento, Altro)"),
                ("Reparto *","Reparto di appartenenza del segnalante"),
                ("Descrizione *","Descrizione dettagliata del problema"),
                ("Ubicazione","Ubicazione/area dove e' stato riscontrato il problema"),
                ("Allegati","File allegati (foto, documenti)")],
         "assign":[("Segnalazione *","Segnalazione da assegnare"),
                   ("Responsabile *","Tecnico o reparto responsabile della risoluzione"),
                   ("Priorita' *","Livello di priorita' (Alta, Media, Bassa)"),
                   ("Scadenza *","Data di scadenza prevista per la risoluzione"),
                   ("Note","Note aggiuntive per il responsabile")],
         "manage":[("Stato *","Stato attuale (Nuova, Assegnata, In Lavorazione, Risolta, Chiusa)"),
                   ("Azione Correttiva","Descrizione dell'azione intrapresa"),
                   ("Data Risoluzione","Data in cui il problema e' stato risolto"),
                   ("Verifica","Verifica dell'efficacia della soluzione"),
                   ("Report","Generazione del report riepilogativo")]},
        {"new":"NOTA: Le segnalazioni vengono automaticamente numerate e tracciate nel sistema.","assign":"NOTA: Le segnalazioni ad alta priorita' inviano una notifica immediata al responsabile.","manage":"NOTA: Le segnalazioni scadute vengono automaticamente evidenziate in rosso nella dashboard."},
        {"new":"ATTENZIONE: Le segnalazioni relative alla sicurezza vengono automaticamente classificate come alta priorita'.","assign":"ATTENZIONE: La riassegnazione di una segnalazione gia' in lavorazione richiede la conferma del responsabile corrente.","manage":"ATTENZIONE: Una segnalazione chiusa non puo' essere riaperta senza l'autorizzazione del responsabile qualita'."}),
    "ro": ("TraceabilityRS - Semnalari", "Camp", "Descriere",
        {"new":"Semnalare Noua","assign":"Atribuire Semnalare","manage":"Gestionare Semnalari"},
        {"new":"Ghid pentru crearea unei semnalari noi","assign":"Ghid pentru atribuirea semnalarilor","manage":"Ghid pentru gestionarea semnalarilor"},
        {"new":"Aceasta functie permite crearea unei noi semnalari pentru probleme, anomalii sau sugestii.",
         "assign":"Aceasta functie permite responsabililor sa atribuie semnalarile primite tehnicienilor sau departamentelor competente.",
         "manage":"Aceasta functie permit gestionarea ciclului complet al semnalarilor."},
        {"new":["1. Tip Semnalare / Selectati tipul.","2. Descriere / Inserati descrierea detaliata.","3. Atasamente / Atasati fotografii sau documente.","4. Trimitere / Faceti clic pe 'Trimite'."],
         "assign":["1. Lista Semnalari / Vizualizati semnalarile in asteptare.","2. Selectati Responsabilul / Selectati tehnicianul.","3. Prioritate si Termen / Definiti prioritatea si termenul.","4. Confirmare / Confirmati atribuirea."],
         "manage":["1. Dashboard / Vizualizati starea tuturor semnalarilor.","2. Filtre / Filtrati dupa stare, prioritate.","3. Actualizari / Actualizati starea.","4. Inchidere / Inchideti semnalarea."]},
        {"new":[("Tip *","Tipul semnalarii"),("Departament *","Departamentul"),("Descriere *","Descrierea detaliata"),("Locatie","Locatia problemei"),("Atasamente","Fisiere atasate")],
         "assign":[("Semnalare *","Semnalarea de atribuit"),("Responsabil *","Tehnicianul responsabil"),("Prioritate *","Nivelul de prioritate"),("Termen *","Termenul de rezolvare"),("Note","Note suplimentare")],
         "manage":[("Stare *","Starea actuala"),("Actiune Corectiva","Actiunea intreprinsa"),("Data Rezolvare","Data rezolvarii"),("Verificare","Verificarea eficacitatii"),("Raport","Generarea raportului")]},
        {"new":"NOTA: Semnalarile sunt numerotate si urmarite automat.","assign":"NOTA: Semnalarile cu prioritate mare trimit notificare imediata.","manage":"NOTA: Semnalarile expirate sunt evidentiate in rosu."},
        {"new":"ATENTIE: Semnalarile de securitate sunt clasificate automat ca prioritate mare.","assign":"ATENTIE: Reatribuirea necesita confirmarea responsabilului actual.","manage":"ATENTIE: O semnalare inchisa nu poate fi redeschisa fara autorizare."}),
    "en": ("TraceabilityRS - Submissions", "Field", "Description",
        {"new":"New Submission","assign":"Assign Submission","manage":"Submissions Management"},
        {"new":"Guide to creating a new submission","assign":"Guide to assigning submissions","manage":"Guide to managing submissions"},
        {"new":"This function allows creating a new submission for problems, anomalies or suggestions.",
         "assign":"This function allows managers to assign received submissions to technicians or departments.",
         "manage":"This function manages the complete submission lifecycle."},
        {"new":["1. Submission Type / Select the type.","2. Description / Enter a detailed description.","3. Attachments / Attach photos or documents.","4. Submit / Click 'Submit'."],
         "assign":["1. Submission List / View pending submissions.","2. Select Responsible / Select the technician.","3. Priority and Deadline / Set priority and deadline.","4. Confirm / Confirm the assignment."],
         "manage":["1. Dashboard / View the status of all submissions.","2. Filters / Filter by status, priority.","3. Updates / Update status and actions.","4. Close / Close the submission."]},
        {"new":[("Type *","Submission type"),("Department *","Department"),("Description *","Detailed description"),("Location","Problem location"),("Attachments","Attached files")],
         "assign":[("Submission *","Submission to assign"),("Responsible *","Responsible technician"),("Priority *","Priority level"),("Deadline *","Resolution deadline"),("Notes","Additional notes")],
         "manage":[("Status *","Current status"),("Corrective Action","Action taken"),("Resolution Date","Resolution date"),("Verification","Solution verification"),("Report","Summary report")]},
        {"new":"NOTE: Submissions are automatically numbered and tracked.","assign":"NOTE: High-priority submissions send immediate notification.","manage":"NOTE: Overdue submissions are highlighted in red."},
        {"new":"WARNING: Safety submissions are automatically classified as high priority.","assign":"WARNING: Reassignment requires current responsible's confirmation.","manage":"WARNING: A closed submission cannot be reopened without authorization."}),
    "de": ("TraceabilityRS - Meldungen", "Feld", "Beschreibung",
        {"new":"Neue Meldung","assign":"Meldung zuweisen","manage":"Meldungsverwaltung"},
        {"new":"Anleitung zur Erstellung einer neuen Meldung","assign":"Anleitung zur Zuweisung von Meldungen","manage":"Anleitung zur Verwaltung von Meldungen"},
        {"new":"Diese Funktion ermoeglicht die Erstellung einer neuen Meldung.",
         "assign":"Diese Funktion ermoeglicht es, Meldungen zuzuweisen.",
         "manage":"Diese Funktion verwaltet den vollstaendigen Meldungslebenszyklus."},
        {"new":["1. Meldungstyp / Typ auswaehlen.","2. Beschreibung / Detaillierte Beschreibung eingeben.","3. Anhaenge / Fotos oder Dokumente anhaengen.","4. Einreichen / Auf 'Einreichen' klicken."],
         "assign":["1. Meldungsliste / Ausstehende Meldungen anzeigen.","2. Verantwortlichen waehlen / Techniker auswaehlen.","3. Prioritaet und Frist / Prioritaet und Frist festlegen.","4. Bestaetigen / Zuweisung bestaetigen."],
         "manage":["1. Dashboard / Status aller Meldungen anzeigen.","2. Filter / Nach Status, Prioritaet filtern.","3. Aktualisierungen / Status aktualisieren.","4. Schliessen / Meldung schliessen."]},
        {"new":[("Typ *","Meldungstyp"),("Abteilung *","Abteilung"),("Beschreibung *","Detaillierte Beschreibung"),("Ort","Problemort"),("Anhaenge","Angehaengte Dateien")],
         "assign":[("Meldung *","Zuzuweisende Meldung"),("Verantwortlicher *","Verantwortlicher Techniker"),("Prioritaet *","Prioritaetsstufe"),("Frist *","Loesungsfrist"),("Notizen","Zusaetzliche Notizen")],
         "manage":[("Status *","Aktueller Status"),("Korrekturmassnahme","Ergriffene Massnahme"),("Loesungsdatum","Loesungsdatum"),("Verifizierung","Loesungsverifizierung"),("Bericht","Zusammenfassungsbericht")]},
        {"new":"HINWEIS: Meldungen werden automatisch nummeriert.","assign":"HINWEIS: Hochprioritaere Meldungen senden sofortige Benachrichtigung.","manage":"HINWEIS: Ueberfaellige Meldungen werden rot hervorgehoben."},
        {"new":"ACHTUNG: Sicherheitsmeldungen werden automatisch als hoch eingestuft.","assign":"ACHTUNG: Neuzuweisung erfordert Bestaetigung des aktuellen Verantwortlichen.","manage":"ACHTUNG: Geschlossene Meldungen koennen nicht ohne Genehmigung wieder geoeffnet werden."}),
    "sv": ("TraceabilityRS - Anmaelningar", "Faelt", "Beskrivning",
        {"new":"Ny Anmaelning","assign":"Tilldela Anmaelning","manage":"Hantering av Anmaelningar"},
        {"new":"Guide foer att skapa en ny anmaelning","assign":"Guide foer tilldelning av anmaelningar","manage":"Guide foer hantering av anmaelningar"},
        {"new":"Denna funktion goer det moejligt att skapa en ny anmaelning.",
         "assign":"Denna funktion goer det moejligt att tilldela anmaelningar.",
         "manage":"Denna funktion hanterar hela anmaelningslivscykeln."},
        {"new":["1. Anmaelningstyp / Vaelj typ.","2. Beskrivning / Ange detaljerad beskrivning.","3. Bilagor / Bifoga foton eller dokument.","4. Skicka / Klicka poe 'Skicka'."],
         "assign":["1. Anmaelningslista / Visa vaentande anmaelningar.","2. Vaelj ansvarig / Vaelj tekniker.","3. Prioritet och tidsfrist / Ange prioritet och tidsfrist.","4. Bekraefta / Bekraefta tilldelningen."],
         "manage":["1. Dashboard / Visa status foer alla anmaelningar.","2. Filter / Filtrera efter status, prioritet.","3. Uppdateringar / Uppdatera status.","4. Staeng / Staeng anmaelningen."]},
        {"new":[("Typ *","Anmaelningstyp"),("Avdelning *","Avdelning"),("Beskrivning *","Detaljerad beskrivning"),("Plats","Problemets plats"),("Bilagor","Bifogade filer")],
         "assign":[("Anmaelning *","Anmaelning att tilldela"),("Ansvarig *","Ansvarig tekniker"),("Prioritet *","Prioritetsnivoe"),("Tidsfrist *","Loesningsfrist"),("Anteckningar","Ytterligare anteckningar")],
         "manage":[("Status *","Aktuell status"),("Korrigerande oetgaerd","Vidtagen oetgaerd"),("Loesningsdatum","Loesningsdatum"),("Verifiering","Loesningsverifiering"),("Rapport","Sammanfattningsrapport")]},
        {"new":"NOTERA: Anmaelningar numreras och spoeras automatiskt.","assign":"NOTERA: Hoegprioriterade anmaelningar skickar omedelbar notifiering.","manage":"NOTERA: Foerfallna anmaelningar markeras i roett."},
        {"new":"VARNING: Saekerhetanmaelningar klassificeras automatiskt som hoeg prioritet.","assign":"VARNING: Omtilldelning kraever bekraeftelse froen nuvarande ansvarig.","manage":"VARNING: En staengd anmaelning kan inte oeppnas igen utan godkaennande."}),
}.items():
    T = {"app":"TraceabilityRS","ver":"Versione 2.3.6" if lang=="it" else ("Versiunea 2.3.6" if lang=="ro" else "Version 2.3.6"),
         "footer":footer,"field":field_l,"description":desc_l}
    for key in ("new","assign","manage"):
        T[f"{key}_title"] = titles[key]
        T[f"{key}_subtitle"] = subtitles[key]
        T[f"{key}_desc"] = descs[key]
        T[f"{key}_steps"] = steps[key]
        T[f"{key}_fields"] = fields[key]
        T[f"{key}_note"] = notes[key]
        T[f"{key}_warn"] = warns[key]
    TEXTS[lang] = T


def _cover(story, T):
    story.append(sp(20))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=50*mm, height=50*mm)); story.append(sp(6))
    story.append(Paragraph(T["app"], title_style))
    story.append(Paragraph(T["ver"], sub_style))


def build_manual(lang, T, section_key, prefix):
    out = os.path.join(BASE_DIR, lang, f"{section_key}.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=18*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)
    W = A4[0] - 30*mm
    story = []
    _cover(story, T)
    story.append(Paragraph(T[f"{prefix}_title"], title_style))
    story.append(Paragraph(T[f"{prefix}_subtitle"], sub_style))
    story.append(hr())
    story.append(Paragraph(T[f"{prefix}_desc"], body))
    story.append(sp(4))
    story.append(Paragraph(T[f"{prefix}_title"], h1))
    for step_text in T[f"{prefix}_steps"]:
        parts = step_text.split(" / ", 1)
        story.append(Paragraph(parts[0], h2))
        if len(parts) > 1:
            story.append(Paragraph(parts[1], body))
    story.append(hr())
    story.append(Paragraph(T["field"], h1))
    rows = []
    for fname, fdesc in T[f"{prefix}_fields"]:
        rows.append([Paragraph(fname, body), Paragraph(fdesc, body)])
    story.append(make_table([Paragraph(T["field"], body), Paragraph(T["description"], body)], rows, W))
    story.append(sp(4))
    story.append(Paragraph(T[f"{prefix}_note"], note_s))
    story.append(Paragraph(T[f"{prefix}_warn"], warn_s))
    doc.build(story, onFirstPage=lambda c,d: on_page(c,d,T["footer"]), onLaterPages=lambda c,d: on_page(c,d,T["footer"]))
    print(f"  -> {out}")


if __name__ == "__main__":
    for lang in ("it","ro","en","de","sv"):
        os.makedirs(os.path.join(BASE_DIR, lang), exist_ok=True)
        T = TEXTS[lang]
        print(f"[{lang}]")
        for section_key, prefix in MANUALS:
            build_manual(lang, T, section_key, prefix)
    print(f"\nDone! {len(MANUALS)*5} PDF generati.")
