# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Manutenzione' in 5 lingue.
Produce i seguenti file per ogni lingua:
  - manutenzione_aggiungi_macchina.pdf  (anche per modifica/visualizza/tipi)
  - manutenzione_fixture_regole.pdf     (anche per assegnazione)
  - manutenzione_gestione_task.pdf      (anche per voci task/responsabili)
  - manutenzione_compila_schede.pdf
  - manutenzione_report_panoramica.pdf  (anche per rapporti fixtures)
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
H3 = ParagraphStyle("H3", fontName="Arial-Bold", fontSize=10, textColor=AC, spaceAfter=2*mm, spaceBefore=3*mm, leading=13)
B  = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black, spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
BI = ParagraphStyle("BI", parent=B, leftIndent=8*mm)
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
    "a":"TraceabilityRS","v":"Versione 2.3.6","ft":"TraceabilityRS - Manutenzione",
    "login":"Necessita autenticazione (login)",
    # --- MACHINES ---
    "m_t":"Gestione Macchine","m_s":"Guida completa alla gestione delle macchine",
    "m_intro":"Questa sezione copre tutte le operazioni relative alle macchine: aggiunta, modifica, "
              "visualizzazione e gestione dei tipi di equipaggiamento.",
    "m_add_t":"Aggiungere una Nuova Macchina",
    "m_add":"Il modulo di inserimento richiede i seguenti campi:",
    "m_f":[("Nome Macchina *","Nome identificativo dell'equipaggiamento"),
           ("Tipo Equipaggiamento *","Selezionare dalla lista (es: Loom, Tufting, Finishing)"),
           ("Linea","Linea di produzione assegnata"),
           ("Brand *","Marca del produttore"),
           ("Compagnia","Si compila automaticamente in base al Brand"),
           ("Numero Seriale","Numero di serie della macchina"),
           ("Anno Produzione","Anno di fabbricazione"),
           ("Note","Note aggiuntive")],
    "m_edit_t":"Modificare una Macchina",
    "m_edit":"Selezionare prima il tipo di equipaggiamento per filtrare la lista, "
             "poi selezionare la macchina da modificare. Tutte le modifiche vengono registrate "
             "in un log automatico con data, utente e dettaglio del cambio.",
    "m_view_t":"Visualizzare le Macchine",
    "m_view":"La finestra di ricerca offre filtri per Tipo, Brand, Linea, Nome e Data. "
             "I risultati appaiono in una tabella con doppio clic per i dettagli. "
             "La scheda dettagli puo' generare un PDF con tutte le informazioni della macchina.",
    "m_types_t":"Gestione Tipi Macchine",
    "m_types":"Permette di definire e modificare le categorie di equipaggiamento utilizzate nei menu a tendina.",
    "m_note":"NOTA: Ogni modifica viene tracciata con utente, data e valore precedente/nuovo.",
    # --- FIXTURE ---
    "f_t":"Gestione Fixture","f_s":"Regole e assegnazione prodotti",
    "f_intro":"I Fixture sono attrezzature speciali associate alle macchine. "
              "Questa sezione copre sia le regole di gestione che l'assegnazione ai prodotti.",
    "f_rules_t":"Regole Fixture",
    "f_rules":"Definisce le regole di utilizzo e manutenzione per i fixture: "
              "intervalli di controllo, soglie di usura, criteri di sostituzione.",
    "f_assign_t":"Assegnazione Prodotti ai Fixture",
    "f_assign":"Permette di associare specifici prodotti ai fixture disponibili, "
               "definendo quali fixture sono compatibili con quali prodotti.",
    # --- TASKS ---
    "t_t":"Task di Manutenzione","t_s":"Gestione dei piani e delle attivita'",
    "t_intro":"Questa sezione gestisce i piani di manutenzione: definizione dei task, "
              "configurazione delle voci e assegnazione dei responsabili.",
    "t_manage_t":"Gestione Task",
    "t_manage":"Creare e configurare i task di manutenzione: nome, descrizione, frequenza, "
               "tipo (preventiva, correttiva, predittiva), priorita'.",
    "t_cycles_t":"Gestione Voci Task",
    "t_cycles":"Definisce le singole voci (checklist) che compongono ogni task: "
               "punti di controllo, valori attesi, unita' di misura.",
    "t_assign_t":"Assegna Responsabili",
    "t_assign":"Associa i task ai responsabili dell'esecuzione. "
               "Un task puo' avere piu' responsabili e un responsabile puo' gestire piu' task.",
    # --- FILL TEMPLATES ---
    "c_t":"Compila Schede","c_s":"Esecuzione delle schede di manutenzione",
    "c_intro":"Questa funzione e' il cuore operativo della manutenzione. "
              "Permette agli operatori di compilare le schede di controllo durante l'esecuzione dei task.",
    "c_step1":"1. Selezionare l'area/fase dal menu a tendina",
    "c_step2":"2. Selezionare l'equipaggiamento da manutenere",
    "c_step3":"3. Selezionare il piano di manutenzione attivo",
    "c_step4":"4. Compilare le voci del task (OK/KO/Valore)",
    "c_step5":"5. Salvare il registro completato",
    "c_note":"NOTA: Per equipaggiamenti con conteggio cicli, il sistema mostra automaticamente "
             "le statistiche e avvisa quando si raggiungono soglie critiche.",
    "c_request":"Se durante la compilazione si riscontra un problema, e' possibile generare "
                "direttamente una richiesta di intervento dal pulsante dedicato.",
    # --- REPORTS ---
    "r_t":"Rapporti Manutenzione","r_s":"Report e analisi",
    "r_intro":"La sezione rapporti offre una panoramica dello stato della manutenzione:",
    "r_overview_t":"Report Panoramica",
    "r_overview":"Visualizzazione d'insieme di tutti i task, scadenze, completamenti. "
                 "Utile per il controllo manageriale e l'analisi dei trend.",
    "r_fixtures_t":"Rapporti Fixtures",
    "r_fixtures":"Report specializzati sull'utilizzo e lo stato dei fixture: "
                 "cicli effettuati, usura, prossime sostituzioni.",
    "r_missing_t":"Missing Action Report",
    "r_missing":"Report dei task in ritardo o non completati entro la scadenza prevista.",
    "field":"Campo","desc":"Descrizione",
  },
  "ro": {
    "a":"TraceabilityRS","v":"Versiunea 2.3.6","ft":"TraceabilityRS - Mentenanta",
    "login":"Necesita autentificare (login)",
    "m_t":"Gestionare Masini","m_s":"Ghid complet de gestionare a masinilor",
    "m_intro":"Aceasta sectiune acopera operatiunile legate de masini: adaugare, modificare, "
              "vizualizare si gestionarea tipurilor de echipamente.",
    "m_add_t":"Adaugarea unei Masini Noi",
    "m_add":"Formularul de inserare necesita urmatoarele campuri:",
    "m_f":[("Nume Masina *","Numele identificativ al echipamentului"),
           ("Tip Echipament *","Selectati din lista (ex: Loom, Tufting, Finishing)"),
           ("Linie","Linia de productie atribuita"),
           ("Brand *","Marca producatorului"),
           ("Companie","Se completeaza automat in functie de Brand"),
           ("Numar Serie","Numarul de serie al masinii"),
           ("An Productie","Anul de fabricatie"),
           ("Note","Note suplimentare")],
    "m_edit_t":"Modificarea unei Masini",
    "m_edit":"Selectati intai tipul de echipament pentru filtrare, apoi masina de modificat. "
             "Toate modificarile sunt inregistrate intr-un log automat.",
    "m_view_t":"Vizualizarea Masinilor",
    "m_view":"Fereastra de cautare ofera filtre pentru Tip, Brand, Linie, Nume si Data. "
             "Dublu clic pentru detalii. Fisa de detalii poate genera un PDF.",
    "m_types_t":"Gestionare Tipuri Masini",
    "m_types":"Permite definirea categoriilor de echipamente utilizate in meniurile derulante.",
    "m_note":"NOTA: Fiecare modificare e trasata cu utilizator, data si valoarea anterioara/noua.",
    "f_t":"Gestionare Fixture","f_s":"Reguli si atribuire produse",
    "f_intro":"Fixture sunt echipamente speciale asociate masinilor.",
    "f_rules_t":"Reguli Fixture",
    "f_rules":"Defineste regulile de utilizare si mentenanta pentru fixture.",
    "f_assign_t":"Atribuire Produse la Fixture",
    "f_assign":"Permite asocierea produselor la fixture disponibile.",
    "t_t":"Taskuri de Mentenanta","t_s":"Gestionarea planurilor si activitatilor",
    "t_intro":"Aceasta sectiune gestioneaza planurile de mentenanta.",
    "t_manage_t":"Gestionare Taskuri",
    "t_manage":"Creati si configurati taskuri: nume, descriere, frecventa, tip, prioritate.",
    "t_cycles_t":"Gestionare Voci Task",
    "t_cycles":"Defineste elementele checklist ale fiecarui task.",
    "t_assign_t":"Atribuire Responsabili",
    "t_assign":"Asociaza taskurile cu responsabilii executiei.",
    "c_t":"Completare Fise","c_s":"Executarea fiselor de mentenanta",
    "c_intro":"Functia principala operationala de mentenanta.",
    "c_step1":"1. Selectati zona/faza din meniul derulant",
    "c_step2":"2. Selectati echipamentul de intretinut",
    "c_step3":"3. Selectati planul de mentenanta activ",
    "c_step4":"4. Completati elementele taskului (OK/KO/Valoare)",
    "c_step5":"5. Salvati registrul completat",
    "c_note":"NOTA: Pentru echipamente cu contor cicluri, sistemul afiseaza statistici si avertizeaza la praguri critice.",
    "c_request":"Daca gasiti o problema, puteti genera o cerere de interventie direct din butonul dedicat.",
    "r_t":"Rapoarte Mentenanta","r_s":"Rapoarte si analize",
    "r_intro":"Sectiunea de rapoarte ofera o vedere de ansamblu:",
    "r_overview_t":"Raport General",
    "r_overview":"Vizualizare de ansamblu a taskurilor, termenelor si completarilor.",
    "r_fixtures_t":"Rapoarte Fixture",
    "r_fixtures":"Rapoarte specializate privind utilizarea si starea fixture.",
    "r_missing_t":"Raport Actiuni Lipsa",
    "r_missing":"Raport al taskurilor intarziate sau necompletate.",
    "field":"Camp","desc":"Descriere",
  },
  "en": {
    "a":"TraceabilityRS","v":"Version 2.3.6","ft":"TraceabilityRS - Maintenance",
    "login":"Requires authentication (login)",
    "m_t":"Machine Management","m_s":"Complete machine management guide",
    "m_intro":"This section covers all machine-related operations: adding, editing, "
              "viewing, and managing equipment types.",
    "m_add_t":"Adding a New Machine",
    "m_add":"The insertion form requires the following fields:",
    "m_f":[("Machine Name *","Equipment identifier name"),
           ("Equipment Type *","Select from list (e.g., Loom, Tufting, Finishing)"),
           ("Line","Assigned production line"),
           ("Brand *","Manufacturer brand"),
           ("Company","Auto-filled based on Brand"),
           ("Serial Number","Machine serial number"),
           ("Production Year","Year of manufacture"),
           ("Notes","Additional notes")],
    "m_edit_t":"Editing a Machine",
    "m_edit":"First select the equipment type to filter, then select the machine to edit. "
             "All changes are recorded in an automatic log with date, user, and change details.",
    "m_view_t":"Viewing Machines",
    "m_view":"The search window offers filters for Type, Brand, Line, Name, and Date. "
             "Double-click for details. The detail card can generate a PDF.",
    "m_types_t":"Equipment Types Management",
    "m_types":"Define and modify equipment categories used in dropdown menus.",
    "m_note":"NOTE: Every change is tracked with user, date, and previous/new values.",
    "f_t":"Fixture Management","f_s":"Rules and product assignment",
    "f_intro":"Fixtures are special equipment associated with machines.",
    "f_rules_t":"Fixture Rules",
    "f_rules":"Defines usage and maintenance rules for fixtures.",
    "f_assign_t":"Product Assignment to Fixtures",
    "f_assign":"Associates specific products with available fixtures.",
    "t_t":"Maintenance Tasks","t_s":"Plan and activity management",
    "t_intro":"This section manages maintenance plans.",
    "t_manage_t":"Task Management",
    "t_manage":"Create and configure tasks: name, description, frequency, type, priority.",
    "t_cycles_t":"Task Items Management",
    "t_cycles":"Defines the checklist items composing each task.",
    "t_assign_t":"Assign Responsibles",
    "t_assign":"Associates tasks with execution responsibles.",
    "c_t":"Fill Templates","c_s":"Executing maintenance checklists",
    "c_intro":"The operational core of maintenance.",
    "c_step1":"1. Select the area/phase from the dropdown",
    "c_step2":"2. Select the equipment to maintain",
    "c_step3":"3. Select the active maintenance plan",
    "c_step4":"4. Fill in task items (OK/KO/Value)",
    "c_step5":"5. Save the completed log",
    "c_note":"NOTE: For equipment with cycle counting, the system shows statistics and warns at critical thresholds.",
    "c_request":"If an issue is found, you can generate an intervention request directly from the dedicated button.",
    "r_t":"Maintenance Reports","r_s":"Reports and analysis",
    "r_intro":"The reports section provides an overview:",
    "r_overview_t":"Overview Report",
    "r_overview":"Overview of all tasks, deadlines, and completions.",
    "r_fixtures_t":"Fixtures Reports",
    "r_fixtures":"Specialized reports on fixture usage and status.",
    "r_missing_t":"Missing Action Report",
    "r_missing":"Report of overdue or incomplete tasks.",
    "field":"Field","desc":"Description",
  },
  "de": {
    "a":"TraceabilityRS","v":"Version 2.3.6","ft":"TraceabilityRS - Wartung",
    "login":"Erfordert Authentifizierung (Login)",
    "m_t":"Maschinenverwaltung","m_s":"Vollstaendige Anleitung",
    "m_intro":"Dieser Bereich umfasst alle maschinenbezogenen Operationen.",
    "m_add_t":"Neue Maschine hinzufuegen",
    "m_add":"Das Formular erfordert folgende Felder:",
    "m_f":[("Maschinenname *","Bezeichnung des Equipments"),
           ("Equipmenttyp *","Aus Liste waehlen"),
           ("Linie","Zugewiesene Produktionslinie"),
           ("Marke *","Herstellermarke"),
           ("Unternehmen","Automatisch basierend auf Marke"),
           ("Seriennummer","Seriennummer der Maschine"),
           ("Produktionsjahr","Herstellungsjahr"),
           ("Notizen","Zusaetzliche Notizen")],
    "m_edit_t":"Maschine bearbeiten",
    "m_edit":"Equipmenttyp zur Filterung waehlen, dann Maschine auswaehlen. "
             "Alle Aenderungen werden protokolliert.",
    "m_view_t":"Maschinen anzeigen",
    "m_view":"Suchfenster mit Filtern. Doppelklick fuer Details. PDF-Generierung moeglich.",
    "m_types_t":"Equipmenttypen verwalten",
    "m_types":"Kategorien fuer Dropdown-Menues definieren und bearbeiten.",
    "m_note":"HINWEIS: Jede Aenderung wird mit Benutzer, Datum und Werten protokolliert.",
    "f_t":"Fixture-Verwaltung","f_s":"Regeln und Produktzuweisung",
    "f_intro":"Fixtures sind spezielle Ausruestungen fuer Maschinen.",
    "f_rules_t":"Fixture-Regeln","f_rules":"Nutzungs- und Wartungsregeln fuer Fixtures.",
    "f_assign_t":"Produktzuweisung","f_assign":"Produkte den verfuegbaren Fixtures zuordnen.",
    "t_t":"Wartungsaufgaben","t_s":"Plan- und Aktivitaetenverwaltung",
    "t_intro":"Dieser Bereich verwaltet Wartungsplaene.",
    "t_manage_t":"Aufgabenverwaltung","t_manage":"Aufgaben erstellen und konfigurieren.",
    "t_cycles_t":"Aufgabenelemente","t_cycles":"Checklisten-Elemente je Aufgabe definieren.",
    "t_assign_t":"Verantwortliche zuweisen","t_assign":"Aufgaben Verantwortlichen zuordnen.",
    "c_t":"Formulare ausfuellen","c_s":"Wartungschecklisten ausfuehren",
    "c_intro":"Das operative Herzstuck der Wartung.",
    "c_step1":"1. Bereich/Phase waehlen","c_step2":"2. Equipment waehlen",
    "c_step3":"3. Aktiven Wartungsplan waehlen","c_step4":"4. Aufgabenelemente ausfuellen (OK/KO/Wert)",
    "c_step5":"5. Abgeschlossenes Protokoll speichern",
    "c_note":"HINWEIS: Bei Equipment mit Zyklusdaten zeigt das System Statistiken und warnt bei kritischen Schwellen.",
    "c_request":"Bei Problemen kann direkt eine Interventionsanfrage erstellt werden.",
    "r_t":"Wartungsberichte","r_s":"Berichte und Analysen",
    "r_intro":"Die Berichtssektion bietet eine Uebersicht:",
    "r_overview_t":"Uebersichtsbericht","r_overview":"Uebersicht aller Aufgaben und Fristen.",
    "r_fixtures_t":"Fixture-Berichte","r_fixtures":"Spezialberichte zu Fixture-Nutzung.",
    "r_missing_t":"Fehlende Aktionen","r_missing":"Bericht ueberfaelliger Aufgaben.",
    "field":"Feld","desc":"Beschreibung",
  },
  "sv": {
    "a":"TraceabilityRS","v":"Version 2.3.6","ft":"TraceabilityRS - Underhaall",
    "login":"Kraever autentisering (inloggning)",
    "m_t":"Maskinhantering","m_s":"Komplett guide",
    "m_intro":"Denna sektion taecker alla maskinrelaterade operationer.",
    "m_add_t":"Laegga till ny maskin",
    "m_add":"Formulaeret kraever foeljande faelt:",
    "m_f":[("Maskinnamn *","Utrustningsidentifierare"),
           ("Utrustningstyp *","Vaelj fraan lista"),
           ("Linje","Tilldelad produktionslinje"),
           ("Maerke *","Tillverkarens maerke"),
           ("Foeretag","Fylls i automatiskt baserat paa maerke"),
           ("Serienummer","Maskinens serienummer"),
           ("Produktionsaar","Tillverkningsaar"),
           ("Anteckningar","Ytterligare anteckningar")],
    "m_edit_t":"Redigera maskin",
    "m_edit":"Vaelj utrustningstyp foer filtrering, sedan maskin. Alla aendringar loggas.",
    "m_view_t":"Visa maskiner",
    "m_view":"Soekfoenster med filter. Dubbelklicka foer detaljer. PDF-generering moeejlig.",
    "m_types_t":"Hantera utrustningstyper","m_types":"Definiera kategorier foer rullgardinsmenyer.",
    "m_note":"OBS: Varje aendring loggas med anvaendare, datum och vaerden.",
    "f_t":"Fixture-hantering","f_s":"Regler och produkttilldelning",
    "f_intro":"Fixtures aer specialutrustning foer maskiner.",
    "f_rules_t":"Fixture-regler","f_rules":"Anvaendnings- och underhaallsregler.",
    "f_assign_t":"Produkttilldelning","f_assign":"Koppla produkter till tillgaengliga fixtures.",
    "t_t":"Underhaallsuppgifter","t_s":"Plan- och aktivitetshantering",
    "t_intro":"Denna sektion hanterar underhaallsplaner.",
    "t_manage_t":"Uppgiftshantering","t_manage":"Skapa och konfigurera uppgifter.",
    "t_cycles_t":"Uppgiftselement","t_cycles":"Definiera checklista-element per uppgift.",
    "t_assign_t":"Tilldela ansvariga","t_assign":"Koppla uppgifter till ansvariga.",
    "c_t":"Fyll i formulaer","c_s":"Utfoera underhaallschecklistor",
    "c_intro":"Det operativa hjaertat av underhaall.",
    "c_step1":"1. Vaelj omraade/fas","c_step2":"2. Vaelj utrustning",
    "c_step3":"3. Vaelj aktiv underhaallsplan","c_step4":"4. Fyll i uppgiftselement (OK/KO/Vaerde)",
    "c_step5":"5. Spara slutfoert protokoll",
    "c_note":"OBS: Foer utrustning med cykelddata visar systemet statistik och varnar vid kritiska troesklar.",
    "c_request":"Vid problem kan en interventionsbegaeran skapas direkt.",
    "r_t":"Underhaallsrapporter","r_s":"Rapporter och analyser",
    "r_intro":"Rapportsektionen ger en oeversikt:",
    "r_overview_t":"Oeversiktsrapport","r_overview":"Oeversikt oever uppgifter och tidsfrister.",
    "r_fixtures_t":"Fixture-rapporter","r_fixtures":"Specialrapporter om fixture-anvaendning.",
    "r_missing_t":"Saknade aatgaerder","r_missing":"Rapport oever foersenade uppgifter.",
    "field":"Faelt","desc":"Beskrivning",
  },
}


def gen_machines(lang, t):
    out = os.path.join(BASE, lang, "manutenzione_aggiungi_macchina.pdf")
    def story(s, wid):
        cover(s, t["m_t"], t["m_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["m_intro"], B))
        # Add
        s.append(Paragraph(t["m_add_t"], H1))
        s.append(Paragraph(t["m_add"], B))
        s.append(tbl([t["field"], t["desc"]], [list(f) for f in t["m_f"]], wid))
        # Edit
        s.append(Paragraph(t["m_edit_t"], H1))
        s.append(Paragraph(t["m_edit"], B))
        # View
        s.append(Paragraph(t["m_view_t"], H1))
        s.append(Paragraph(t["m_view"], B))
        # Types
        s.append(Paragraph(t["m_types_t"], H1))
        s.append(Paragraph(t["m_types"], B))
        s.append(sp(3)); s.append(Paragraph(t["m_note"], N))
    build_pdf(out, story, t["ft"])
    # Copy aliases
    d = os.path.dirname(out)
    for alias in ["manutenzione_tipi_macchine","manutenzione_modifica_macchina","manutenzione_visualizza_macchine"]:
        shutil.copy2(out, os.path.join(d, alias + ".pdf"))
    print("  [%s] machines (4 files)" % lang.upper())

def gen_fixtures(lang, t):
    out = os.path.join(BASE, lang, "manutenzione_fixture_regole.pdf")
    def story(s, wid):
        cover(s, t["f_t"], t["f_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["f_intro"], B))
        s.append(Paragraph(t["f_rules_t"], H1))
        s.append(Paragraph(t["f_rules"], B))
        s.append(Paragraph(t["f_assign_t"], H1))
        s.append(Paragraph(t["f_assign"], B))
    build_pdf(out, story, t["ft"])
    shutil.copy2(out, os.path.join(os.path.dirname(out), "manutenzione_fixture_assegnazione.pdf"))
    print("  [%s] fixtures (2 files)" % lang.upper())

def gen_tasks(lang, t):
    out = os.path.join(BASE, lang, "manutenzione_gestione_task.pdf")
    def story(s, wid):
        cover(s, t["t_t"], t["t_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["t_intro"], B))
        s.append(Paragraph(t["t_manage_t"], H1))
        s.append(Paragraph(t["t_manage"], B))
        s.append(Paragraph(t["t_cycles_t"], H1))
        s.append(Paragraph(t["t_cycles"], B))
        s.append(Paragraph(t["t_assign_t"], H1))
        s.append(Paragraph(t["t_assign"], B))
    build_pdf(out, story, t["ft"])
    d = os.path.dirname(out)
    for alias in ["manutenzione_voci_task", "manutenzione_assegna_responsabili"]:
        shutil.copy2(out, os.path.join(d, alias + ".pdf"))
    print("  [%s] tasks (3 files)" % lang.upper())

def gen_fill(lang, t):
    out = os.path.join(BASE, lang, "manutenzione_compila_schede.pdf")
    def story(s, wid):
        cover(s, t["c_t"], t["c_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["c_intro"], B))
        s.append(Paragraph("Procedura", H1))
        s.append(bul(t["c_step1"])); s.append(bul(t["c_step2"]))
        s.append(bul(t["c_step3"])); s.append(bul(t["c_step4"]))
        s.append(bul(t["c_step5"]))
        s.append(sp(3)); s.append(Paragraph(t["c_note"], N))
        s.append(Paragraph(t["c_request"], TI))
    build_pdf(out, story, t["ft"])
    print("  [%s] fill templates (1 file)" % lang.upper())

def gen_reports(lang, t):
    out = os.path.join(BASE, lang, "manutenzione_report_panoramica.pdf")
    def story(s, wid):
        cover(s, t["r_t"], t["r_s"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["r_intro"], B))
        s.append(Paragraph(t["r_overview_t"], H1))
        s.append(Paragraph(t["r_overview"], B))
        s.append(Paragraph(t["r_fixtures_t"], H1))
        s.append(Paragraph(t["r_fixtures"], B))
        s.append(Paragraph(t["r_missing_t"], H1))
        s.append(Paragraph(t["r_missing"], B))
    build_pdf(out, story, t["ft"])
    shutil.copy2(out, os.path.join(os.path.dirname(out), "manutenzione_rapporti_fixtures.pdf"))
    print("  [%s] reports (2 files)" % lang.upper())


if __name__ == "__main__":
    print("Generazione manuali 'Manutenzione' in 5 lingue...")
    for lc, tx in T.items():
        os.makedirs(os.path.join(BASE, lc), exist_ok=True)
        gen_machines(lc, tx)
        gen_fixtures(lc, tx)
        gen_tasks(lc, tx)
        gen_fill(lc, tx)
        gen_reports(lc, tx)
    print("\nCompletato! 60 PDF generati (12 per lingua x 5 lingue)")
