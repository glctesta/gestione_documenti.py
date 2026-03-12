# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Dichiarazioni' (sotto Operativita' > Produzione)
in 5 lingue.

Produce per ogni lingua:
  - operazioni_interruzioni.pdf         (Interruzioni di produzione)
  - operazioni_dichiarazione_scarti.pdf  (Dichiarazione scarti)
  - operazioni_validazione_scarti.pdf    (Validazione scarti)
  - operazioni_validazione_linea.pdf     (FAI: Template, Validazioni, Storico, Fails)
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO = os.path.join(os.path.dirname(__file__), "Logo.png")
BASE = os.path.join(os.path.dirname(__file__), "manuals")

BD = HexColor("#1a237e"); BM = HexColor("#283593"); BL = HexColor("#e8eaf6")
GL = HexColor("#f5f5f5"); GM = HexColor("#e0e0e0"); AC = HexColor("#0d47a1")
OR = HexColor("#e65100"); GR = HexColor("#2e7d32")

WF = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial",        os.path.join(WF, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold",   os.path.join(WF, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(WF, "ariali.ttf")))

TS = ParagraphStyle("T", fontName="Arial-Bold", fontSize=22, textColor=BD, spaceAfter=4*mm, alignment=TA_CENTER)
SS = ParagraphStyle("S", fontName="Arial-Bold", fontSize=14, textColor=BM, spaceAfter=8*mm, alignment=TA_CENTER)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, textColor=white, spaceAfter=4*mm,
    spaceBefore=6*mm, leftIndent=4*mm, leading=20, backColor=BD, borderPadding=(3*mm,3*mm,2*mm,3*mm))
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=12, textColor=BM, spaceAfter=2*mm, spaceBefore=5*mm, leading=16)
B  = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black, spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
BL_S = ParagraphStyle("BL", parent=B, leftIndent=10*mm, bulletIndent=5*mm, spaceBefore=1*mm, spaceAfter=1*mm)
N  = ParagraphStyle("N", fontName="Arial-Italic", fontSize=9, textColor=HexColor("#1565c0"), spaceAfter=3*mm,
    spaceBefore=2*mm, leftIndent=6*mm, leading=12, backColor=BL, borderPadding=(2*mm,2*mm,2*mm,2*mm))
W  = ParagraphStyle("W", fontName="Arial-Bold", fontSize=9, textColor=OR, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#fff3e0"), borderPadding=(2*mm,2*mm,2*mm,2*mm))
TI = ParagraphStyle("TI", fontName="Arial-Italic", fontSize=9, textColor=GR, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#e8f5e9"), borderPadding=(2*mm,2*mm,2*mm,2*mm))

def sp(v=3): return Spacer(1, v*mm)
def hrl(): return HRFlowable(width="100%", thickness=0.5, color=GM, spaceBefore=3*mm, spaceAfter=3*mm)
def bul(t): return Paragraph("<bullet>&bull;</bullet> " + t, BL_S)

def tbl(headers, rows, wid):
    data = [headers] + rows
    t = Table(data, colWidths=[42*mm, wid-42*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BD),("TEXTCOLOR",(0,0),(-1,0),white),
        ("FONTNAME",(0,0),(-1,0),"Arial-Bold"),("FONTSIZE",(0,0),(-1,0),10),
        ("FONTNAME",(0,1),(-1,-1),"Arial"),("FONTSIZE",(0,1),(-1,-1),9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[white,GL]),
        ("GRID",(0,0),(-1,-1),0.5,GM),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),4),
    ]))
    return t

def on_pg(c, d, ft):
    c.saveState(); c.setFont("Arial", 8); c.setFillColor(HexColor("#9e9e9e"))
    c.drawCentredString(A4[0]/2, 12*mm, "%s - Pag. %d" % (ft, d.page))
    c.setStrokeColor(BL); c.setLineWidth(0.5)
    c.line(15*mm, A4[1]-12*mm, A4[0]-15*mm, A4[1]-12*mm); c.restoreState()

def cover(s, title, subtitle, app, ver):
    s.append(sp(15))
    if os.path.exists(LOGO):
        s.append(Image(LOGO, width=50*mm, height=25*mm, hAlign="CENTER"))
    s.append(sp(8))
    s.append(Paragraph(title, TS))
    s.append(Paragraph(subtitle, SS))
    s.append(Paragraph("%s - %s" % (app, ver),
        ParagraphStyle("V", fontName="Arial", fontSize=10, textColor=HexColor("#616161"), alignment=TA_CENTER)))
    s.append(sp(5)); s.append(hrl())

def build_pdf(path, story_fn, ft):
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    s = []; story_fn(s, A4[0]-36*mm)
    doc.build(s, onFirstPage=lambda c,d: on_pg(c,d,ft), onLaterPages=lambda c,d: on_pg(c,d,ft))

# ==============================================================================
T = {
  "it": {
    "a":"TraceabilityRS","v":"Versione 2.3.7","ft":"TraceabilityRS - Dichiarazioni",
    "login":"Necessita autenticazione (login)",
    # --- INTERRUZIONI ---
    "int_t":"Interruzioni di Produzione",
    "int_s":"Registrazione dei fermi produttivi",
    "int_intro":"Questa funzione permette di registrare i fermi e le interruzioni di produzione. "
                "Ogni interruzione viene classificata per tipo, area e problema riscontrato.",
    "int_proc":"Procedura di inserimento",
    "int_f":[("Area di Lavoro (WA) *","Selezionare l'area di lavoro dalla lista"),
             ("Sotto-Area (SA)","Selezionare la sotto-area (filtrata automaticamente per WA)"),
             ("Tipo Problema *","Selezionare il tipo di problema dalla lista"),
             ("Ordine","Selezionare l'ordine di produzione coinvolto (filtro digitando)"),
             ("Data","Data dell'interruzione"),
             ("Ora Inizio / Ora Fine","Orario di inizio e fine del fermo"),
             ("Durata (min)","Calcolata automaticamente oppure inserita manualmente"),
             ("Commenti","Descrizione dettagliata del problema"),
             ("Piano d'Azione","Azioni correttive intraprese o da intraprendere"),
             ("Documenti","Allegare documenti di supporto (foto, report, ecc.)")],
    "int_save":"Premere 'Salva' per registrare l'interruzione nel database.",
    "int_note":"NOTA: E' possibile allegare piu' documenti all'interruzione. "
               "Il sistema calcola automaticamente la durata dal tempo di inizio e fine.",
    "int_warn":"ATTENZIONE: Compilare almeno Area di Lavoro e Tipo Problema prima di salvare.",
    # --- DICHIARAZIONE SCARTI ---
    "scrap_t":"Dichiarazione Scarti",
    "scrap_s":"Registrazione degli scarti di produzione",
    "scrap_intro":"Questa funzione permette di dichiarare gli scarti di produzione. "
                  "L'operatore identifica il pezzo tramite scansione del codice etichetta, "
                  "seleziona la causale e completa la dichiarazione.",
    "scrap_proc":"Procedura",
    "scrap_step1":"1. Scansionare o digitare il <b>codice etichetta</b> (LabelCode) del pezzo",
    "scrap_step2":"2. Premere <b>Verifica</b> - il sistema carica i dati del prodotto (ordine, fase, prodotto)",
    "scrap_step3":"3. Selezionare la <b>causale di scarto</b> dalla lista",
    "scrap_step4":"4. Aggiungere <b>riferimenti</b> se richiesti dalla causale (da DB o manuali)",
    "scrap_step5":"5. Opzionale: allegare una <b>foto</b> del difetto",
    "scrap_step6":"6. Premere <b>Salva</b> per registrare la dichiarazione",
    "scrap_note":"NOTA: La dichiarazione verra' sottoposta a validazione prima di essere confermata. "
                 "Un supervisore dovra' approvare o rifiutare lo scarto.",
    "scrap_warn":"ATTENZIONE: Alcune causali richiedono obbligatoriamente l'inserimento di riferimenti.",
    # --- VALIDAZIONE SCARTI ---
    "val_t":"Validazione Scarti",
    "val_s":"Approvazione o rifiuto delle dichiarazioni",
    "val_intro":"Questa funzione permette ai supervisori di validare le dichiarazioni di scarto "
                "pending. Il validatore puo' approvare, rifiutare e aggiungere note.",
    "val_proc":"Procedura",
    "val_list":"La finestra mostra la lista delle dichiarazioni in attesa di validazione con le colonne:",
    "val_cols":[("Prodotto","Nome del prodotto"),
               ("Ordine","Numero ordine di produzione"),
               ("LabelCode","Codice etichetta del pezzo scartato"),
               ("Causale","Motivo dello scarto"),
               ("Dichiarante","Operatore che ha creato la dichiarazione"),
               ("Data","Data della dichiarazione")],
    "val_step1":"1. Selezionare una dichiarazione dalla lista, oppure scansionare un LabelCode",
    "val_step2":"2. Verificare i dettagli mostrati (prodotto, causale, riferimenti, foto)",
    "val_step3":"3. Aggiungere <b>note del validatore</b> se necessario",
    "val_step4":"4. Premere <b>Approva</b> o <b>Rifiuta</b>",
    "val_note":"NOTA: Doppio clic sulla riga per visualizzare la foto allegata alla dichiarazione. "
               "Una dichiarazione approvata attiva automaticamente la stored procedure di elaborazione scarto.",
    # --- VALIDAZIONE LINEA (FAI) ---
    "fai_t":"Validazione Linea (FAI)",
    "fai_s":"First Article Inspection - Controllo iniziale produzione",
    "fai_intro":"La Validazione Linea (FAI - First Article Inspection) gestisce il controllo "
                "qualita' del primo pezzo prodotto su ogni linea/ordine. Include la gestione "
                "dei template, l'esecuzione delle validazioni e la reportistica.",
    "fai_tmpl_t":"Gestione Template FAI",
    "fai_tmpl":"Creare e configurare i template di validazione: definire gli step, i punti di "
               "controllo, i valori attesi e le tolleranze per ogni tipo di prodotto/processo.",
    "fai_val_t":"Validazioni FAI",
    "fai_val_intro":"Esecuzione della validazione primo pezzo:",
    "fai_val_step1":"1. Selezionare il <b>template FAI</b> appropriato",
    "fai_val_step2":"2. Selezionare l'<b>ordine di produzione</b>",
    "fai_val_step3":"3. Scansionare il <b>LabelCode</b> del primo pezzo",
    "fai_val_step4":"4. Compilare la <b>checklist</b> (OK/Non OK per ogni step)",
    "fai_val_step5":"5. Per step 'Non OK': inserire dettagli del problema e azione correttiva",
    "fai_val_step6":"6. Spuntare le <b>dichiarazioni operatore</b> richieste",
    "fai_val_step7":"7. <b>Salvare</b> e opzionalmente <b>stampare</b> il report PDF",
    "fai_hist_t":"Storico Validazioni FAI",
    "fai_hist":"Consultare lo storico di tutte le validazioni eseguite: filtrare per data, "
               "prodotto, ordine. Rivedere i risultati e ristampare report.",
    "fai_fails_t":"Rapporto FAI Fails",
    "fai_fails":"Report specifico dei soli step falliti (Non OK) nelle validazioni FAI. "
                "Utile per analisi trend difetti e miglioramento continuo.",
    "fai_note":"NOTA: I template FAI possono avere regole speciali (es. KeepOnSameLine) "
               "che mantengono step correlati sulla stessa riga della checklist.",
    "field":"Campo","desc":"Descrizione","col":"Colonna",
  },
  "ro": {
    "a":"TraceabilityRS","v":"Versiunea 2.3.7","ft":"TraceabilityRS - Declaratii",
    "login":"Necesita autentificare (login)",
    "int_t":"Intreruperi de Productie",
    "int_s":"Inregistrarea opririi productiei",
    "int_intro":"Aceasta functie permite inregistrarea opririlor si intreruperilor de productie. "
                "Fiecare intrerupere este clasificata dupa tip, zona si problema intalnita.",
    "int_proc":"Procedura de inserare",
    "int_f":[("Zona de Lucru (WA) *","Selectati zona de lucru din lista"),
             ("Sub-Zona (SA)","Selectati sub-zona (filtrata automat dupa WA)"),
             ("Tip Problema *","Selectati tipul de problema din lista"),
             ("Comanda","Selectati comanda de productie implicata"),
             ("Data","Data intreruperii"),
             ("Ora Inceput / Ora Sfarsit","Orele de inceput si sfarsit ale opririi"),
             ("Durata (min)","Calculata automat sau introdusa manual"),
             ("Comentarii","Descrierea detaliata a problemei"),
             ("Plan de Actiune","Actiuni corective luate sau de intreprins"),
             ("Documente","Atasati documente suport (fotografii, rapoarte etc.)")],
    "int_save":"Apasati 'Salveaza' pentru a inregistra intreruperea in baza de date.",
    "int_note":"NOTA: Puteti atasa mai multe documente. Sistemul calculeaza automat durata.",
    "int_warn":"ATENTIE: Completati cel putin Zona de Lucru si Tipul Problemei inainte de salvare.",
    "scrap_t":"Declaratie Rebuturi",
    "scrap_s":"Inregistrarea rebuturilor de productie",
    "scrap_intro":"Aceasta functie permite declararea rebuturilor de productie. "
                  "Operatorul identifica piesa prin scanarea codului de eticheta.",
    "scrap_proc":"Procedura",
    "scrap_step1":"1. Scanati sau tastati <b>codul de eticheta</b> (LabelCode) al piesei",
    "scrap_step2":"2. Apasati <b>Verifica</b> - sistemul incarca datele produsului",
    "scrap_step3":"3. Selectati <b>cauza rebutului</b> din lista",
    "scrap_step4":"4. Adaugati <b>referinte</b> daca sunt cerute de cauza",
    "scrap_step5":"5. Optional: atasati o <b>fotografie</b> a defectului",
    "scrap_step6":"6. Apasati <b>Salveaza</b> pentru a inregistra declaratia",
    "scrap_note":"NOTA: Declaratia va fi supusa validarii inainte de confirmare.",
    "scrap_warn":"ATENTIE: Unele cauze necesita obligatoriu introducerea de referinte.",
    "val_t":"Validare Rebuturi",
    "val_s":"Aprobarea sau respingerea declaratiilor",
    "val_intro":"Aceasta functie permite supervizorilor sa valideze declaratiile de rebut in asteptare.",
    "val_proc":"Procedura",
    "val_list":"Fereastra afiseaza lista declaratiilor in asteptare cu coloanele:",
    "val_cols":[("Produs","Numele produsului"),
               ("Comanda","Numarul comenzii de productie"),
               ("LabelCode","Codul de eticheta al piesei rebutate"),
               ("Cauza","Motivul rebutului"),
               ("Declarant","Operatorul care a creat declaratia"),
               ("Data","Data declaratiei")],
    "val_step1":"1. Selectati o declaratie din lista sau scanati un LabelCode",
    "val_step2":"2. Verificati detaliile afisate",
    "val_step3":"3. Adaugati <b>note ale validatorului</b> daca este necesar",
    "val_step4":"4. Apasati <b>Aproba</b> sau <b>Respinge</b>",
    "val_note":"NOTA: Dublu clic pe rand pentru a vizualiza fotografia atasata. "
               "O declaratie aprobata activeaza automat procedura stocata de procesare.",
    "fai_t":"Validare Linie (FAI)",
    "fai_s":"First Article Inspection - Controlul initial al productiei",
    "fai_intro":"Validarea Liniei (FAI) gestioneaza controlul calitatii primei piese produse.",
    "fai_tmpl_t":"Gestionare Template FAI",
    "fai_tmpl":"Creati si configurati template-urile de validare: definiti pasii, punctele de control.",
    "fai_val_t":"Validari FAI",
    "fai_val_intro":"Executarea validarii primei piese:",
    "fai_val_step1":"1. Selectati <b>template-ul FAI</b> potrivit",
    "fai_val_step2":"2. Selectati <b>comanda de productie</b>",
    "fai_val_step3":"3. Scanati <b>LabelCode</b>-ul primei piese",
    "fai_val_step4":"4. Completati <b>checklist-ul</b> (OK/Non OK pentru fiecare pas)",
    "fai_val_step5":"5. Pentru pasi 'Non OK': introduceti detalii si actiuni corective",
    "fai_val_step6":"6. Bifati <b>declaratiile operatorului</b> necesare",
    "fai_val_step7":"7. <b>Salvati</b> si optional <b>tipariti</b> raportul PDF",
    "fai_hist_t":"Istoric Validari FAI",
    "fai_hist":"Consultati istoricul tuturor validarilor efectuate.",
    "fai_fails_t":"Raport FAI Esecuri",
    "fai_fails":"Raport specific al pasilor esuati in validarile FAI.",
    "fai_note":"NOTA: Template-urile FAI pot avea reguli speciale (ex: KeepOnSameLine).",
    "field":"Camp","desc":"Descriere","col":"Coloana",
  },
  "en": {
    "a":"TraceabilityRS","v":"Version 2.3.7","ft":"TraceabilityRS - Declarations",
    "login":"Requires authentication (login)",
    "int_t":"Production Interruptions",
    "int_s":"Recording production stoppages",
    "int_intro":"This function records production stoppages and interruptions. "
                "Each interruption is classified by type, area, and problem encountered.",
    "int_proc":"Entry Procedure",
    "int_f":[("Work Area (WA) *","Select the work area from the list"),
             ("Sub-Area (SA)","Select the sub-area (auto-filtered by WA)"),
             ("Problem Type *","Select the problem type from the list"),
             ("Order","Select the production order involved"),
             ("Date","Date of the interruption"),
             ("Start Time / End Time","Start and end times of the stoppage"),
             ("Duration (min)","Calculated automatically or entered manually"),
             ("Comments","Detailed description of the problem"),
             ("Action Plan","Corrective actions taken or to be taken"),
             ("Documents","Attach supporting documents (photos, reports, etc.)")],
    "int_save":"Press 'Save' to record the interruption in the database.",
    "int_note":"NOTE: Multiple documents can be attached. Duration is auto-calculated.",
    "int_warn":"WARNING: Fill in at least Work Area and Problem Type before saving.",
    "scrap_t":"Scrap Declaration",
    "scrap_s":"Recording production scrap",
    "scrap_intro":"This function allows declaring production scrap. "
                  "The operator identifies the piece by scanning the label code.",
    "scrap_proc":"Procedure",
    "scrap_step1":"1. Scan or type the <b>label code</b> (LabelCode) of the piece",
    "scrap_step2":"2. Press <b>Verify</b> - the system loads product data",
    "scrap_step3":"3. Select the <b>scrap reason</b> from the list",
    "scrap_step4":"4. Add <b>references</b> if required by the reason",
    "scrap_step5":"5. Optional: attach a <b>photo</b> of the defect",
    "scrap_step6":"6. Press <b>Save</b> to record the declaration",
    "scrap_note":"NOTE: The declaration will be submitted for validation before confirmation.",
    "scrap_warn":"WARNING: Some reasons require mandatory reference entry.",
    "val_t":"Scrap Validation",
    "val_s":"Approving or rejecting declarations",
    "val_intro":"This function allows supervisors to validate pending scrap declarations.",
    "val_proc":"Procedure",
    "val_list":"The window shows pending declarations with the columns:",
    "val_cols":[("Product","Product name"),
               ("Order","Production order number"),
               ("LabelCode","Label code of the scrapped piece"),
               ("Reason","Scrap reason"),
               ("Declarant","Operator who created the declaration"),
               ("Date","Declaration date")],
    "val_step1":"1. Select a declaration from the list, or scan a LabelCode",
    "val_step2":"2. Verify the displayed details",
    "val_step3":"3. Add <b>validator notes</b> if needed",
    "val_step4":"4. Press <b>Approve</b> or <b>Reject</b>",
    "val_note":"NOTE: Double-click a row to view the attached photo. "
               "An approved declaration automatically triggers the scrap processing procedure.",
    "fai_t":"Line Validation (FAI)",
    "fai_s":"First Article Inspection",
    "fai_intro":"Line Validation (FAI) manages the quality inspection of the first piece produced.",
    "fai_tmpl_t":"FAI Template Management",
    "fai_tmpl":"Create and configure validation templates: define steps, check points, and tolerances.",
    "fai_val_t":"FAI Validations",
    "fai_val_intro":"Executing first article validation:",
    "fai_val_step1":"1. Select the appropriate <b>FAI template</b>",
    "fai_val_step2":"2. Select the <b>production order</b>",
    "fai_val_step3":"3. Scan the <b>LabelCode</b> of the first piece",
    "fai_val_step4":"4. Complete the <b>checklist</b> (OK/Not OK for each step)",
    "fai_val_step5":"5. For 'Not OK' steps: enter problem details and corrective action",
    "fai_val_step6":"6. Check the required <b>operator declarations</b>",
    "fai_val_step7":"7. <b>Save</b> and optionally <b>print</b> the PDF report",
    "fai_hist_t":"FAI Validation History",
    "fai_hist":"Browse the history of all validations performed.",
    "fai_fails_t":"FAI Fails Report",
    "fai_fails":"Specific report of only failed steps in FAI validations.",
    "fai_note":"NOTE: FAI templates may have special rules (e.g., KeepOnSameLine).",
    "field":"Field","desc":"Description","col":"Column",
  },
  "de": {
    "a":"TraceabilityRS","v":"Version 2.3.7","ft":"TraceabilityRS - Erklaerungen",
    "login":"Erfordert Authentifizierung (Login)",
    "int_t":"Produktionsunterbrechungen",
    "int_s":"Erfassung von Produktionsstillstaenden",
    "int_intro":"Diese Funktion erfasst Produktionsstillstaende und Unterbrechungen.",
    "int_proc":"Eingabeverfahren",
    "int_f":[("Arbeitsbereich (WA) *","Arbeitsbereich aus der Liste waehlen"),
             ("Unterbereich (SA)","Unterbereich waehlen (automatisch nach WA gefiltert)"),
             ("Problemtyp *","Problemtyp aus der Liste waehlen"),
             ("Auftrag","Betroffenen Produktionsauftrag waehlen"),
             ("Datum","Datum der Unterbrechung"),
             ("Startzeit / Endzeit","Start- und Endzeit des Stillstands"),
             ("Dauer (Min)","Automatisch berechnet oder manuell eingegeben"),
             ("Kommentare","Detaillierte Problembeschreibung"),
             ("Aktionsplan","Ergriffene oder geplante Korrekturmassnahmen"),
             ("Dokumente","Begleitdokumente anhaengen")],
    "int_save":"'Speichern' druecken, um die Unterbrechung zu erfassen.",
    "int_note":"HINWEIS: Mehrere Dokumente koennen angehaengt werden.",
    "int_warn":"ACHTUNG: Mindestens Arbeitsbereich und Problemtyp vor dem Speichern ausfuellen.",
    "scrap_t":"Ausschusserklaerung",
    "scrap_s":"Erfassung von Produktionsausschuss",
    "scrap_intro":"Diese Funktion ermoeglicht die Erklaerung von Produktionsausschuss.",
    "scrap_proc":"Verfahren",
    "scrap_step1":"1. <b>Etikettencode</b> (LabelCode) scannen oder eingeben",
    "scrap_step2":"2. <b>Pruefen</b> druecken - Produktdaten werden geladen",
    "scrap_step3":"3. <b>Ausschussgrund</b> aus der Liste waehlen",
    "scrap_step4":"4. <b>Referenzen</b> hinzufuegen falls erforderlich",
    "scrap_step5":"5. Optional: <b>Foto</b> des Defekts anhaengen",
    "scrap_step6":"6. <b>Speichern</b> druecken",
    "scrap_note":"HINWEIS: Die Erklaerung wird vor der Bestaetigung zur Validierung eingereicht.",
    "scrap_warn":"ACHTUNG: Einige Gruende erfordern zwingend Referenzeingabe.",
    "val_t":"Ausschussvalidierung",
    "val_s":"Genehmigung oder Ablehnung von Erklaerungen",
    "val_intro":"Diese Funktion ermoeglicht Vorgesetzten die Validierung ausstehender Erklaerungen.",
    "val_proc":"Verfahren",
    "val_list":"Das Fenster zeigt ausstehende Erklaerungen mit den Spalten:",
    "val_cols":[("Produkt","Produktname"),
               ("Auftrag","Produktionsauftragsnummer"),
               ("LabelCode","Etikettencode"),("Grund","Ausschussgrund"),
               ("Erklaerer","Bediener"),("Datum","Erklaerungsdatum")],
    "val_step1":"1. Erklaerung aus der Liste waehlen oder LabelCode scannen",
    "val_step2":"2. Angezeigte Details pruefen",
    "val_step3":"3. <b>Validierungsnotizen</b> hinzufuegen",
    "val_step4":"4. <b>Genehmigen</b> oder <b>Ablehnen</b> druecken",
    "val_note":"HINWEIS: Doppelklick auf eine Zeile zeigt das angehaengte Foto.",
    "fai_t":"Linienvalidierung (FAI)",
    "fai_s":"Erststueck-Pruefung",
    "fai_intro":"Die Linienvalidierung (FAI) verwaltet die Qualitaetspruefung des ersten Stuecks.",
    "fai_tmpl_t":"FAI-Vorlagenverwaltung",
    "fai_tmpl":"Validierungsvorlagen erstellen und konfigurieren.",
    "fai_val_t":"FAI-Validierungen",
    "fai_val_intro":"Durchfuehrung der Erststueck-Pruefung:",
    "fai_val_step1":"1. Passende <b>FAI-Vorlage</b> waehlen",
    "fai_val_step2":"2. <b>Produktionsauftrag</b> waehlen",
    "fai_val_step3":"3. <b>LabelCode</b> scannen",
    "fai_val_step4":"4. <b>Checkliste</b> ausfuellen (OK/Nicht OK)",
    "fai_val_step5":"5. Bei 'Nicht OK': Problemdetails eingeben",
    "fai_val_step6":"6. <b>Bedienererklaerungen</b> ankreuzen",
    "fai_val_step7":"7. <b>Speichern</b> und optional <b>drucken</b>",
    "fai_hist_t":"FAI-Validierungsverlauf",
    "fai_hist":"Verlauf aller durchgefuehrten Validierungen einsehen.",
    "fai_fails_t":"FAI-Fehlerbericht",
    "fai_fails":"Spezifischer Bericht ueber fehlgeschlagene Schritte.",
    "fai_note":"HINWEIS: FAI-Vorlagen koennen Sonderregeln haben (z.B. KeepOnSameLine).",
    "field":"Feld","desc":"Beschreibung","col":"Spalte",
  },
  "sv": {
    "a":"TraceabilityRS","v":"Version 2.3.7","ft":"TraceabilityRS - Deklarationer",
    "login":"Kraever autentisering (inloggning)",
    "int_t":"Produktionsavbrott",
    "int_s":"Registrering av produktionsstopp",
    "int_intro":"Denna funktion registrerar produktionsstopp och avbrott.",
    "int_proc":"Inmatningsfoerfarande",
    "int_f":[("Arbetsomraade (WA) *","Vaelj arbetsomraade fraan listan"),
             ("Underomraade (SA)","Vaelj underomraade (filtrerat efter WA)"),
             ("Problemtyp *","Vaelj problemtyp fraan listan"),
             ("Order","Vaelj betraeffad produktionsorder"),
             ("Datum","Datum foer avbrottet"),
             ("Starttid / Sluttid","Start- och sluttid foer stoppet"),
             ("Varaktighet (min)","Beraeknas automatiskt eller anges manuellt"),
             ("Kommentarer","Detaljerad problembeskrivning"),
             ("Aatgaerdsplan","Korrigerande aatgaerder"),
             ("Dokument","Bifoga stoeddokument")],
    "int_save":"Tryck 'Spara' foer att registrera avbrottet.",
    "int_note":"OBS: Flera dokument kan bifogas. Varaktigheten beraeknas automatiskt.",
    "int_warn":"VARNING: Fyll i minst Arbetsomraade och Problemtyp foere sparande.",
    "scrap_t":"Kassationsdeklaration",
    "scrap_s":"Registrering av produktionskassation",
    "scrap_intro":"Denna funktion goer det moejligt att deklarera produktionskassation.",
    "scrap_proc":"Foerfarande",
    "scrap_step1":"1. Skanna eller skriv in <b>etikettkoden</b> (LabelCode)",
    "scrap_step2":"2. Tryck <b>Verifiera</b> - systemet laddar produktdata",
    "scrap_step3":"3. Vaelj <b>kassationsorsak</b> fraan listan",
    "scrap_step4":"4. Laegga till <b>referenser</b> om det kraevs",
    "scrap_step5":"5. Valfritt: bifoga ett <b>foto</b> av defekten",
    "scrap_step6":"6. Tryck <b>Spara</b> foer att registrera deklarationen",
    "scrap_note":"OBS: Deklarationen skickas foer validering foere bekraeftelse.",
    "scrap_warn":"VARNING: Vissa orsaker kraever obligatorisk referensinmatning.",
    "val_t":"Kassationsvalidering",
    "val_s":"Godkaennande eller avvisande av deklarationer",
    "val_intro":"Denna funktion laater chefer validera vaentande kassationsdeklarationer.",
    "val_proc":"Foerfarande",
    "val_list":"Foenestret visar vaentande deklarationer med kolumnerna:",
    "val_cols":[("Produkt","Produktnamn"),("Order","Produktionsordernummer"),
               ("LabelCode","Etikettkod"),("Orsak","Kassationsorsak"),
               ("Deklarant","Operatoer"),("Datum","Deklarationsdatum")],
    "val_step1":"1. Vaelj en deklaration fraan listan, eller skanna en LabelCode",
    "val_step2":"2. Verifiera visade detaljer",
    "val_step3":"3. Laegga till <b>validatoranteckningar</b>",
    "val_step4":"4. Tryck <b>Godkaenn</b> eller <b>Avvisa</b>",
    "val_note":"OBS: Dubbelklicka foer att visa bifogat foto. "
               "En godkaend deklaration utloeser automatiskt kassationsbearbetningen.",
    "fai_t":"Linjevalidering (FAI)",
    "fai_s":"Foersta Artikelinspektion",
    "fai_intro":"Linjevalidering (FAI) hanterar kvalitetsinspektionen av den foersta producerade detaljen.",
    "fai_tmpl_t":"FAI-mallhantering",
    "fai_tmpl":"Skapa och konfigurera valideringsmallar.",
    "fai_val_t":"FAI-valideringar",
    "fai_val_intro":"Genomfoerande av foersta artikelvalidering:",
    "fai_val_step1":"1. Vaelj laemplig <b>FAI-mall</b>",
    "fai_val_step2":"2. Vaelj <b>produktionsorder</b>",
    "fai_val_step3":"3. Skanna <b>LabelCode</b>",
    "fai_val_step4":"4. Fyll i <b>checklistan</b> (OK/Ej OK)",
    "fai_val_step5":"5. Foer 'Ej OK': ange problemdetaljer",
    "fai_val_step6":"6. Kryssa i <b>operatoersdeklarationer</b>",
    "fai_val_step7":"7. <b>Spara</b> och valfritt <b>skriva ut</b>",
    "fai_hist_t":"FAI-valideringshistorik",
    "fai_hist":"Graanska historik oever alla genomfoerda valideringar.",
    "fai_fails_t":"FAI-felrapport",
    "fai_fails":"Specifik rapport oever misslyckade steg.",
    "fai_note":"OBS: FAI-mallar kan ha specialregler (t.ex. KeepOnSameLine).",
    "field":"Faelt","desc":"Beskrivning","col":"Kolumn",
  },
}


def gen_interruptions(lang, t):
    out = os.path.join(BASE, lang, "operazioni_interruzioni.pdf")
    def story(s, wid):
        cover(s, t["int_t"], t["int_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["int_intro"], B))
        s.append(Paragraph(t["int_proc"], H1))
        s.append(tbl([t["field"], t["desc"]], [list(f) for f in t["int_f"]], wid))
        s.append(sp(2)); s.append(Paragraph(t["int_save"], B))
        s.append(sp(2))
        s.append(Paragraph(t["int_warn"], W))
        s.append(Paragraph(t["int_note"], N))
    build_pdf(out, story, t["ft"])
    print("  [%s] interruptions" % lang.upper())

def gen_scrap_declaration(lang, t):
    out = os.path.join(BASE, lang, "operazioni_dichiarazione_scarti.pdf")
    def story(s, wid):
        cover(s, t["scrap_t"], t["scrap_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["scrap_intro"], B))
        s.append(Paragraph(t["scrap_proc"], H1))
        s.append(bul(t["scrap_step1"])); s.append(bul(t["scrap_step2"]))
        s.append(bul(t["scrap_step3"])); s.append(bul(t["scrap_step4"]))
        s.append(bul(t["scrap_step5"])); s.append(bul(t["scrap_step6"]))
        s.append(sp(2))
        s.append(Paragraph(t["scrap_warn"], W))
        s.append(Paragraph(t["scrap_note"], N))
    build_pdf(out, story, t["ft"])
    print("  [%s] scrap declaration" % lang.upper())

def gen_scrap_validation(lang, t):
    out = os.path.join(BASE, lang, "operazioni_validazione_scarti.pdf")
    def story(s, wid):
        cover(s, t["val_t"], t["val_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["val_intro"], B))
        s.append(Paragraph(t["val_proc"], H1))
        s.append(Paragraph(t["val_list"], B))
        s.append(tbl([t["col"], t["desc"]], [list(c) for c in t["val_cols"]], wid))
        s.append(sp(2))
        s.append(bul(t["val_step1"])); s.append(bul(t["val_step2"]))
        s.append(bul(t["val_step3"])); s.append(bul(t["val_step4"]))
        s.append(sp(2))
        s.append(Paragraph(t["val_note"], N))
    build_pdf(out, story, t["ft"])
    print("  [%s] scrap validation" % lang.upper())

def gen_fai(lang, t):
    out = os.path.join(BASE, lang, "operazioni_validazione_linea.pdf")
    def story(s, wid):
        cover(s, t["fai_t"], t["fai_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["fai_intro"], B))
        # Template
        s.append(Paragraph(t["fai_tmpl_t"], H1))
        s.append(Paragraph(t["fai_tmpl"], B))
        # Validations
        s.append(Paragraph(t["fai_val_t"], H1))
        s.append(Paragraph(t["fai_val_intro"], B))
        s.append(bul(t["fai_val_step1"])); s.append(bul(t["fai_val_step2"]))
        s.append(bul(t["fai_val_step3"])); s.append(bul(t["fai_val_step4"]))
        s.append(bul(t["fai_val_step5"])); s.append(bul(t["fai_val_step6"]))
        s.append(bul(t["fai_val_step7"]))
        # History
        s.append(Paragraph(t["fai_hist_t"], H1))
        s.append(Paragraph(t["fai_hist"], B))
        # Fails
        s.append(Paragraph(t["fai_fails_t"], H1))
        s.append(Paragraph(t["fai_fails"], B))
        s.append(sp(3))
        s.append(Paragraph(t["fai_note"], N))
    build_pdf(out, story, t["ft"])
    # Copy aliases for sub-menu keys
    d = os.path.dirname(out)
    for alias in ["operazioni_gestione_template_fai","operazioni_validazioni_fai",
                   "operazioni_storico_validazioni_fai","operazioni_rapporto_fai_fails"]:
        shutil.copy2(out, os.path.join(d, alias + ".pdf"))
    print("  [%s] FAI line validation (5 files)" % lang.upper())


if __name__ == "__main__":
    print("Generazione manuali 'Dichiarazioni' in 5 lingue...")
    for lc, tx in T.items():
        os.makedirs(os.path.join(BASE, lc), exist_ok=True)
        gen_interruptions(lc, tx)
        gen_scrap_declaration(lc, tx)
        gen_scrap_validation(lc, tx)
        gen_fai(lc, tx)
    print("\nCompletato! 40 PDF generati (8 per lingua x 5 lingue)")
