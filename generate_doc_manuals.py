# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Documenti di Produzione' in 5 lingue.
Produce: manuals/{lang}/documenti_inserisci.pdf
         manuals/{lang}/documenti_visualizza.pdf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Logo.png")
BASE_DIR = os.path.join(os.path.dirname(__file__), "manuals")

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

title_style = ParagraphStyle("T", fontName="Arial-Bold", fontSize=22, textColor=BLUE_DARK,
    spaceAfter=4*mm, alignment=TA_CENTER)
sub_style = ParagraphStyle("S", fontName="Arial-Bold", fontSize=14, textColor=BLUE_MED,
    spaceAfter=8*mm, alignment=TA_CENTER)
h1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, textColor=white,
    spaceAfter=4*mm, spaceBefore=6*mm, leftIndent=4*mm, leading=20,
    backColor=BLUE_DARK, borderPadding=(3*mm, 3*mm, 2*mm, 3*mm))
h2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=12, textColor=BLUE_MED,
    spaceAfter=2*mm, spaceBefore=5*mm, leading=16)
h3 = ParagraphStyle("H3", fontName="Arial-Bold", fontSize=10, textColor=ACCENT,
    spaceAfter=2*mm, spaceBefore=3*mm, leading=13)
body = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black,
    spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
blt = ParagraphStyle("BL", parent=body, leftIndent=10*mm,
    bulletIndent=5*mm, spaceBefore=1*mm, spaceAfter=1*mm)
note = ParagraphStyle("N", fontName="Arial-Italic", fontSize=9,
    textColor=HexColor("#1565c0"), spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=BLUE_LIGHT,
    borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))
warn = ParagraphStyle("W", fontName="Arial-Bold", fontSize=9,
    textColor=ORANGE, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#fff3e0"),
    borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))

def sp(v=3): return Spacer(1, v*mm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=GRAY_MED, spaceBefore=3*mm, spaceAfter=3*mm)

def make_table(headers, rows, W):
    data = [headers] + rows
    t = Table(data, colWidths=[42*mm, W-42*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), BLUE_DARK),
        ("TEXTCOLOR",     (0,0),(-1,0), white),
        ("FONTNAME",      (0,0),(-1,0), "Arial-Bold"),
        ("FONTSIZE",      (0,0),(-1,0), 10),
        ("FONTNAME",      (0,1),(-1,-1), "Arial"),
        ("FONTSIZE",      (0,1),(-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [white, GRAY_LIGHT]),
        ("GRID",          (0,0),(-1,-1), 0.5, GRAY_MED),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
    ]))
    return t

def on_page(canvas_obj, doc, footer_text):
    canvas_obj.saveState()
    canvas_obj.setFont("Arial", 8)
    canvas_obj.setFillColor(HexColor("#9e9e9e"))
    canvas_obj.drawCentredString(A4[0]/2, 12*mm,
        "%s - Pagina %d" % (footer_text, doc.page))
    canvas_obj.setStrokeColor(BLUE_LIGHT)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(15*mm, A4[1]-12*mm, A4[0]-15*mm, A4[1]-12*mm)
    canvas_obj.restoreState()

# ==============================================================================
#  TRANSLATIONS
# ==============================================================================
TEXTS = {
    "it": {
        "app": "TraceabilityRS",
        "ver": "Versione 2.3.6",
        # INSERT
        "ins_title": "Inserimento Documenti di Produzione",
        "ins_subtitle": "Guida all'inserimento dei documenti",
        "ins_access": "Necessita autenticazione (login)",
        "ins_desc": "Questa funzione permette di caricare nuovi documenti di produzione nel sistema, "
                    "associandoli a un prodotto e a una fase del processo produttivo.",
        "ins_steps_title": "Procedura passo per passo",
        "ins_step1_title": "1. Selezionare il Prodotto",
        "ins_step1": "Dal menu a tendina, selezionare il prodotto a cui associare il documento. "
                     "E' possibile digitare nel campo per filtrare la lista.",
        "ins_step2_title": "2. Selezionare la Fase",
        "ins_step2": "Dopo aver selezionato il prodotto, si attiva il menu delle fasi. "
                     "Selezionare la fase di produzione pertinente.",
        "ins_step3_title": "3. Documenti Esistenti",
        "ins_step3": "Dopo aver selezionato la fase, il sistema mostra i documenti gia' presenti. "
                     "I documenti validati sono evidenziati in verde.",
        "ins_step4_title": "4. Inserire il Nuovo Documento",
        "ins_file": "Fare clic su 'Sfoglia' per selezionare il file PDF da caricare.",
        "ins_rev": "Inserire il numero di revisione (max 10 caratteri).",
        "ins_date": "Inserire la data del documento in formato GG/MM/AAAA.",
        "ins_valid": "Selezionare la casella 'Validato' solo se si dispone dell'autorizzazione necessaria.",
        "ins_step5_title": "5. Salvare",
        "ins_step5": "Fare clic su 'Salva' per caricare il documento nel database. "
                     "Se esiste gia' un documento per la stessa fase, il sistema chiedera' conferma per la sostituzione.",
        "ins_fields_title": "Campi del Modulo",
        "fld_product": "Prodotto *",
        "fld_product_d": "Lista prodotti disponibili nel sistema",
        "fld_phase": "Fase *",
        "fld_phase_d": "Fase del processo produttivo",
        "fld_file": "Nome File *",
        "fld_file_d": "File PDF da caricare (tramite 'Sfoglia')",
        "fld_rev": "Revisione *",
        "fld_rev_d": "Numero revisione del documento (max 10 caratteri)",
        "fld_date": "Data Documento *",
        "fld_date_d": "Data del documento (formato: GG/MM/AAAA)",
        "fld_validated": "Validato",
        "fld_validated_d": "Conferma che il documento e' approvato (richiede autorizzazione speciale)",
        "ins_note": "NOTA: La validazione di un documento richiede un permesso speciale "
                    "(ruolo 'validatore_documenti'). Senza tale permesso non sara' possibile "
                    "spuntare la casella 'Validato'.",
        "ins_warn": "ATTENZIONE: Se si sostituisce un documento esistente, quello precedente "
                    "viene marcato come 'fuori validazione' ma resta nel database per lo storico.",
        # VIEW
        "view_title": "Visualizzazione Documenti di Produzione",
        "view_subtitle": "Guida alla consultazione dei documenti",
        "view_access": "Accesso diretto (senza login)",
        "view_desc": "Questa funzione permette di consultare e aprire i documenti di produzione "
                     "associati ai prodotti e alle fasi del processo produttivo.",
        "view_steps_title": "Procedura passo per passo",
        "view_step1_title": "1. Selezionare il Prodotto",
        "view_step1": "Selezionare il prodotto dal menu a tendina. Vengono mostrati solo "
                      "i prodotti che hanno almeno un documento associato.",
        "view_step2_title": "2. Selezionare la Fase",
        "view_step2": "Selezionare la fase per visualizzare la lista dei documenti disponibili.",
        "view_step3_title": "3. Visualizzare i Documenti",
        "view_step3": "La lista mostra tutti i documenti con il loro stato:",
        "view_valid": "VALIDO - Documento approvato e utilizzabile",
        "view_invalid": "Non valido - Documento non ancora approvato o sostituito",
        "view_open_title": "Aprire un Documento",
        "view_open": "Fare doppio clic sul documento nella lista oppure selezionarlo e "
                     "premere il pulsante 'Apri'. Solo i documenti validati possono essere aperti.",
        "view_validate_title": "Validare un Documento",
        "view_validate": "Selezionare un documento non validato e premere 'Valida'. "
                        "E' necessario disporre del permesso 'validatore_documenti'.",
        "view_buttons_title": "Pulsanti disponibili",
        "btn_open": "Apri",
        "btn_open_d": "Apre il documento selezionato (solo se validato)",
        "btn_validate": "Valida",
        "btn_validate_d": "Valida il documento selezionato (richiede autorizzazione)",
        "btn_close": "Chiudi",
        "btn_close_d": "Chiude la finestra",
        "view_note": "NOTA: La lista mostra tutti i documenti, incluse le revisioni precedenti. "
                     "I documenti sostituiti sono marcati come non validi.",
        "field": "Campo",
        "description": "Descrizione",
        "button": "Pulsante",
        "footer": "TraceabilityRS - Documenti di Produzione",
    },
    "ro": {
        "app": "TraceabilityRS",
        "ver": "Versiunea 2.3.6",
        "ins_title": "Inserarea Documentelor de Productie",
        "ins_subtitle": "Ghid de inserare a documentelor",
        "ins_access": "Necesita autentificare (login)",
        "ins_desc": "Aceasta functie permite incarcarea documentelor noi de productie in sistem, "
                    "asociindu-le unui produs si unei faze a procesului de productie.",
        "ins_steps_title": "Procedura pas cu pas",
        "ins_step1_title": "1. Selectati Produsul",
        "ins_step1": "Din meniul derulant, selectati produsul caruia doriti sa-i asociati documentul. "
                     "Puteti tasta in camp pentru a filtra lista.",
        "ins_step2_title": "2. Selectati Faza",
        "ins_step2": "Dupa selectarea produsului, se activeaza meniul fazelor. "
                     "Selectati faza de productie relevanta.",
        "ins_step3_title": "3. Documente existente",
        "ins_step3": "Dupa selectarea fazei, sistemul afiseaza documentele deja prezente. "
                     "Documentele validate sunt evidentiate in verde.",
        "ins_step4_title": "4. Inserati Noul Document",
        "ins_file": "Faceti clic pe 'Rasfoieste' pentru a selecta fisierul PDF de incarcat.",
        "ins_rev": "Introduceti numarul de revizie (max 10 caractere).",
        "ins_date": "Introduceti data documentului in format ZZ/LL/AAAA.",
        "ins_valid": "Bifati caseta 'Validat' doar daca aveti autorizarea necesara.",
        "ins_step5_title": "5. Salvati",
        "ins_step5": "Faceti clic pe 'Salveaza' pentru a incarca documentul in baza de date. "
                     "Daca exista deja un document pentru aceeasi faza, sistemul va solicita confirmarea inlocuirii.",
        "ins_fields_title": "Campuri Formular",
        "fld_product": "Produs *",
        "fld_product_d": "Lista produselor disponibile in sistem",
        "fld_phase": "Faza *",
        "fld_phase_d": "Faza procesului de productie",
        "fld_file": "Nume Fisier *",
        "fld_file_d": "Fisier PDF de incarcat (prin 'Rasfoieste')",
        "fld_rev": "Revizie *",
        "fld_rev_d": "Numarul de revizie al documentului (max 10 caractere)",
        "fld_date": "Data Document *",
        "fld_date_d": "Data documentului (format: ZZ/LL/AAAA)",
        "fld_validated": "Validat",
        "fld_validated_d": "Confirma ca documentul este aprobat (necesita autorizare speciala)",
        "ins_note": "NOTA: Validarea unui document necesita un permis special "
                    "(rolul 'validatore_documenti'). Fara acest permis nu veti putea "
                    "bifa caseta 'Validat'.",
        "ins_warn": "ATENTIE: Daca inlocuiti un document existent, cel anterior "
                    "va fi marcat 'in afara validarii' dar ramane in baza de date pentru istoric.",
        "view_title": "Vizualizarea Documentelor de Productie",
        "view_subtitle": "Ghid de consultare a documentelor",
        "view_access": "Acces direct (fara login)",
        "view_desc": "Aceasta functie permite consultarea si deschiderea documentelor de productie "
                     "asociate produselor si fazelor procesului de productie.",
        "view_steps_title": "Procedura pas cu pas",
        "view_step1_title": "1. Selectati Produsul",
        "view_step1": "Selectati produsul din meniul derulant. Sunt afisate doar "
                      "produsele care au cel putin un document asociat.",
        "view_step2_title": "2. Selectati Faza",
        "view_step2": "Selectati faza pentru a vizualiza lista documentelor disponibile.",
        "view_step3_title": "3. Vizualizati Documentele",
        "view_step3": "Lista afiseaza toate documentele cu statusul lor:",
        "view_valid": "VALID - Document aprobat si utilizabil",
        "view_invalid": "Invalid - Document neaprobat sau inlocuit",
        "view_open_title": "Deschiderea unui Document",
        "view_open": "Faceti dublu clic pe document in lista sau selectati-l si "
                     "apasati butonul 'Deschide'. Doar documentele validate pot fi deschise.",
        "view_validate_title": "Validarea unui Document",
        "view_validate": "Selectati un document nevalidat si apasati 'Valideaza'. "
                        "Este necesar permisul 'validatore_documenti'.",
        "view_buttons_title": "Butoane disponibile",
        "btn_open": "Deschide",
        "btn_open_d": "Deschide documentul selectat (doar daca este validat)",
        "btn_validate": "Valideaza",
        "btn_validate_d": "Valideaza documentul selectat (necesita autorizare)",
        "btn_close": "Inchide",
        "btn_close_d": "Inchide fereastra",
        "view_note": "NOTA: Lista afiseaza toate documentele, inclusiv reviziile anterioare. "
                     "Documentele inlocuite sunt marcate ca invalide.",
        "field": "Camp",
        "description": "Descriere",
        "button": "Buton",
        "footer": "TraceabilityRS - Documente de Productie",
    },
    "en": {
        "app": "TraceabilityRS",
        "ver": "Version 2.3.6",
        "ins_title": "Insert Production Documents",
        "ins_subtitle": "Document Insertion Guide",
        "ins_access": "Requires authentication (login)",
        "ins_desc": "This function allows uploading new production documents to the system, "
                    "associating them with a product and a production process phase.",
        "ins_steps_title": "Step-by-Step Procedure",
        "ins_step1_title": "1. Select the Product",
        "ins_step1": "From the dropdown menu, select the product to associate the document with. "
                     "You can type in the field to filter the list.",
        "ins_step2_title": "2. Select the Phase",
        "ins_step2": "After selecting the product, the phase menu becomes active. "
                     "Select the relevant production phase.",
        "ins_step3_title": "3. Existing Documents",
        "ins_step3": "After selecting the phase, the system displays already existing documents. "
                     "Validated documents are highlighted in green.",
        "ins_step4_title": "4. Enter the New Document",
        "ins_file": "Click 'Browse' to select the PDF file to upload.",
        "ins_rev": "Enter the revision number (max 10 characters).",
        "ins_date": "Enter the document date in DD/MM/YYYY format.",
        "ins_valid": "Check the 'Validated' box only if you have the required authorization.",
        "ins_step5_title": "5. Save",
        "ins_step5": "Click 'Save' to upload the document to the database. "
                     "If a document already exists for the same phase, the system will ask for replacement confirmation.",
        "ins_fields_title": "Form Fields",
        "fld_product": "Product *",
        "fld_product_d": "List of products available in the system",
        "fld_phase": "Phase *",
        "fld_phase_d": "Production process phase",
        "fld_file": "File Name *",
        "fld_file_d": "PDF file to upload (via 'Browse')",
        "fld_rev": "Revision *",
        "fld_rev_d": "Document revision number (max 10 characters)",
        "fld_date": "Document Date *",
        "fld_date_d": "Document date (format: DD/MM/YYYY)",
        "fld_validated": "Validated",
        "fld_validated_d": "Confirms document is approved (requires special authorization)",
        "ins_note": "NOTE: Document validation requires a special permission "
                    "('validatore_documenti' role). Without it, you cannot check "
                    "the 'Validated' box.",
        "ins_warn": "WARNING: If you replace an existing document, the previous one "
                    "is marked as 'out of validation' but remains in the database for history.",
        "view_title": "View Production Documents",
        "view_subtitle": "Document Consultation Guide",
        "view_access": "Direct access (no login required)",
        "view_desc": "This function allows you to view and open production documents "
                     "associated with products and production process phases.",
        "view_steps_title": "Step-by-Step Procedure",
        "view_step1_title": "1. Select the Product",
        "view_step1": "Select the product from the dropdown menu. Only products "
                      "with at least one associated document are shown.",
        "view_step2_title": "2. Select the Phase",
        "view_step2": "Select the phase to view the list of available documents.",
        "view_step3_title": "3. View Documents",
        "view_step3": "The list displays all documents with their status:",
        "view_valid": "VALID - Approved and usable document",
        "view_invalid": "Invalid - Not yet approved or replaced document",
        "view_open_title": "Open a Document",
        "view_open": "Double-click the document in the list or select it and "
                     "press the 'Open' button. Only validated documents can be opened.",
        "view_validate_title": "Validate a Document",
        "view_validate": "Select an unvalidated document and press 'Validate'. "
                        "The 'validatore_documenti' permission is required.",
        "view_buttons_title": "Available Buttons",
        "btn_open": "Open",
        "btn_open_d": "Opens the selected document (only if validated)",
        "btn_validate": "Validate",
        "btn_validate_d": "Validates the selected document (requires authorization)",
        "btn_close": "Close",
        "btn_close_d": "Closes the window",
        "view_note": "NOTE: The list shows all documents, including previous revisions. "
                     "Replaced documents are marked as invalid.",
        "field": "Field",
        "description": "Description",
        "button": "Button",
        "footer": "TraceabilityRS - Production Documents",
    },
    "de": {
        "app": "TraceabilityRS",
        "ver": "Version 2.3.6",
        "ins_title": "Produktionsdokumente Einfuegen",
        "ins_subtitle": "Anleitung zum Einfuegen von Dokumenten",
        "ins_access": "Erfordert Authentifizierung (Login)",
        "ins_desc": "Diese Funktion ermoeglicht das Hochladen neuer Produktionsdokumente "
                    "in das System und deren Zuordnung zu einem Produkt und einer Produktionsphase.",
        "ins_steps_title": "Schritt-fuer-Schritt-Anleitung",
        "ins_step1_title": "1. Produkt auswaehlen",
        "ins_step1": "Waehlen Sie das Produkt aus dem Dropdown-Menue. "
                     "Sie koennen im Feld tippen, um die Liste zu filtern.",
        "ins_step2_title": "2. Phase auswaehlen",
        "ins_step2": "Nach der Produktauswahl wird das Phasenmenue aktiv. "
                     "Waehlen Sie die entsprechende Produktionsphase.",
        "ins_step3_title": "3. Vorhandene Dokumente",
        "ins_step3": "Nach der Phasenauswahl zeigt das System bereits vorhandene Dokumente an. "
                     "Validierte Dokumente sind gruen hervorgehoben.",
        "ins_step4_title": "4. Neues Dokument eingeben",
        "ins_file": "Klicken Sie auf 'Durchsuchen', um die hochzuladende PDF-Datei auszuwaehlen.",
        "ins_rev": "Geben Sie die Revisionsnummer ein (max. 10 Zeichen).",
        "ins_date": "Geben Sie das Dokumentdatum im Format TT/MM/JJJJ ein.",
        "ins_valid": "Aktivieren Sie 'Validiert' nur bei entsprechender Berechtigung.",
        "ins_step5_title": "5. Speichern",
        "ins_step5": "Klicken Sie auf 'Speichern'. Bei vorhandenem Dokument wird die Ersetzung bestaetigt.",
        "ins_fields_title": "Formularfelder",
        "fld_product": "Produkt *", "fld_product_d": "Liste der verfuegbaren Produkte",
        "fld_phase": "Phase *", "fld_phase_d": "Produktionsprozessphase",
        "fld_file": "Dateiname *", "fld_file_d": "PDF-Datei zum Hochladen (ueber 'Durchsuchen')",
        "fld_rev": "Revision *", "fld_rev_d": "Revisionsnummer (max. 10 Zeichen)",
        "fld_date": "Dokumentdatum *", "fld_date_d": "Datum des Dokuments (Format: TT/MM/JJJJ)",
        "fld_validated": "Validiert", "fld_validated_d": "Bestaetigt das Dokument (erfordert Sonderberechtigung)",
        "ins_note": "HINWEIS: Die Dokumentvalidierung erfordert eine Sonderberechtigung "
                    "('validatore_documenti'). Ohne diese kann 'Validiert' nicht aktiviert werden.",
        "ins_warn": "ACHTUNG: Bei Ersetzung wird das vorherige Dokument als "
                    "'ausser Validierung' markiert, bleibt aber im System fuer die Historie.",
        "view_title": "Produktionsdokumente Anzeigen",
        "view_subtitle": "Anleitung zur Dokumenteinsicht",
        "view_access": "Direkter Zugriff (kein Login erforderlich)",
        "view_desc": "Diese Funktion ermoeglicht die Ansicht und das Oeffnen der Produktionsdokumente.",
        "view_steps_title": "Schritt-fuer-Schritt-Anleitung",
        "view_step1_title": "1. Produkt auswaehlen",
        "view_step1": "Waehlen Sie das Produkt. Es werden nur Produkte mit Dokumenten angezeigt.",
        "view_step2_title": "2. Phase auswaehlen",
        "view_step2": "Waehlen Sie die Phase, um die Dokumentliste anzuzeigen.",
        "view_step3_title": "3. Dokumente anzeigen",
        "view_step3": "Die Liste zeigt alle Dokumente mit Status:",
        "view_valid": "GUELTIG - Genehmigtes und verwendbares Dokument",
        "view_invalid": "Ungueltig - Nicht genehmigt oder ersetztes Dokument",
        "view_open_title": "Dokument oeffnen",
        "view_open": "Doppelklick auf das Dokument oder 'Oeffnen' klicken. "
                     "Nur validierte Dokumente koennen geoeffnet werden.",
        "view_validate_title": "Dokument validieren",
        "view_validate": "Waehlen Sie ein unvalidiertes Dokument und klicken Sie 'Validieren'.",
        "view_buttons_title": "Verfuegbare Schaltflaechen",
        "btn_open": "Oeffnen", "btn_open_d": "Oeffnet das ausgewaehlte Dokument (nur wenn validiert)",
        "btn_validate": "Validieren", "btn_validate_d": "Validiert das Dokument (Berechtigung erforderlich)",
        "btn_close": "Schliessen", "btn_close_d": "Schliesst das Fenster",
        "view_note": "HINWEIS: Die Liste zeigt alle Revisionen. Ersetzte Dokumente sind als ungueltig markiert.",
        "field": "Feld", "description": "Beschreibung", "button": "Schaltflaeche",
        "footer": "TraceabilityRS - Produktionsdokumente",
    },
    "sv": {
        "app": "TraceabilityRS",
        "ver": "Version 2.3.6",
        "ins_title": "Infoga Produktionsdokument",
        "ins_subtitle": "Guide foer dokumentinsaettning",
        "ins_access": "Kraever autentisering (inloggning)",
        "ins_desc": "Denna funktion goer det moejligt att ladda upp nya produktionsdokument "
                    "i systemet och koppla dem till en produkt och en produktionsfas.",
        "ins_steps_title": "Steg-foer-steg-procedur",
        "ins_step1_title": "1. Vaelj Produkt",
        "ins_step1": "Vaelj produkt fraan rullgardinsmenyn. Skriv i faeltet foer att filtrera listan.",
        "ins_step2_title": "2. Vaelj Fas",
        "ins_step2": "Efter produktval aktiveras fasmenyn. Vaelj relevant produktionsfas.",
        "ins_step3_title": "3. Befintliga dokument",
        "ins_step3": "Systemet visar befintliga dokument. Validerade dokument markeras i groent.",
        "ins_step4_title": "4. Ange nytt dokument",
        "ins_file": "Klicka 'Blaeddra' foer att vaelja PDF-filen att ladda upp.",
        "ins_rev": "Ange revisionsnummer (max 10 tecken).",
        "ins_date": "Ange dokumentdatum i formatet DD/MM/AAAA.",
        "ins_valid": "Kryssa 'Validerad' endast vid raeekt behoeorighet.",
        "ins_step5_title": "5. Spara",
        "ins_step5": "Klicka 'Spara'. Om ett dokument redan finns bekraeftas ersaettningen.",
        "ins_fields_title": "Formulaerfaelt",
        "fld_product": "Produkt *", "fld_product_d": "Lista oever tillgaengliga produkter",
        "fld_phase": "Fas *", "fld_phase_d": "Produktionsfas",
        "fld_file": "Filnamn *", "fld_file_d": "PDF-fil att ladda upp (via 'Blaeddra')",
        "fld_rev": "Revision *", "fld_rev_d": "Revisionsnummer (max 10 tecken)",
        "fld_date": "Dokumentdatum *", "fld_date_d": "Dokumentets datum (format: DD/MM/AAAA)",
        "fld_validated": "Validerad", "fld_validated_d": "Bekraeftar att dokumentet aer godkaent",
        "ins_note": "OBS: Dokumentvalidering kraever saerskild behoeorighet ('validatore_documenti').",
        "ins_warn": "VARNING: Vid ersaettning markeras det tidigare dokumentet som ogiltigt men behaalles.",
        "view_title": "Visa Produktionsdokument",
        "view_subtitle": "Guide foer dokumentvisning",
        "view_access": "Direkt aatkomst (ingen inloggning)",
        "view_desc": "Denna funktion goer det moejligt att visa och oeppna produktionsdokument.",
        "view_steps_title": "Steg-foer-steg-procedur",
        "view_step1_title": "1. Vaelj Produkt",
        "view_step1": "Vaelj produkt. Endast produkter med dokument visas.",
        "view_step2_title": "2. Vaelj Fas",
        "view_step2": "Vaelj fas foer att visa dokumentlistan.",
        "view_step3_title": "3. Visa Dokument",
        "view_step3": "Listan visar alla dokument med status:",
        "view_valid": "GILTIG - Godkaent och anvaendbart dokument",
        "view_invalid": "Ogiltig - Ej godkaent eller ersatt dokument",
        "view_open_title": "Oeppna ett Dokument",
        "view_open": "Dubbelklicka eller vaelj och klicka 'Oeppna'. Endast validerade dokument kan oeppnas.",
        "view_validate_title": "Validera ett Dokument",
        "view_validate": "Vaelj ett ej validerat dokument och klicka 'Validera'.",
        "view_buttons_title": "Tillgaengliga knappar",
        "btn_open": "Oeppna", "btn_open_d": "Oeppnar valt dokument (om validerat)",
        "btn_validate": "Validera", "btn_validate_d": "Validerar valt dokument (kraever behoeorighet)",
        "btn_close": "Staeng", "btn_close_d": "Staenger foenestret",
        "view_note": "OBS: Listan visar alla revisioner. Ersatta dokument aer markerade som ogiltiga.",
        "field": "Faelt", "description": "Beskrivning", "button": "Knapp",
        "footer": "TraceabilityRS - Produktionsdokument",
    },
}


def build_insert_manual(lang, t):
    out_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "documenti_inserisci.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    W = A4[0] - 36*mm
    s = []

    footer_text = t["footer"]

    # Cover
    s.append(sp(15))
    if os.path.exists(LOGO_PATH):
        s.append(Image(LOGO_PATH, width=50*mm, height=25*mm, hAlign="CENTER"))
    s.append(sp(8))
    s.append(Paragraph(t["ins_title"], title_style))
    s.append(Paragraph(t["ins_subtitle"], sub_style))
    s.append(Paragraph("%s - %s" % (t["app"], t["ver"]),
        ParagraphStyle("V", fontName="Arial", fontSize=10, textColor=HexColor("#616161"), alignment=TA_CENTER)))
    s.append(sp(5))
    s.append(hr())

    # Access
    s.append(Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
        '<font name="Arial-Italic" size="9">%s</font>' % t["ins_access"], body))
    s.append(sp(3))
    s.append(Paragraph(t["ins_desc"], body))

    # Steps
    s.append(Paragraph(t["ins_steps_title"], h1))
    s.append(Paragraph(t["ins_step1_title"], h2))
    s.append(Paragraph(t["ins_step1"], body))
    s.append(Paragraph(t["ins_step2_title"], h2))
    s.append(Paragraph(t["ins_step2"], body))
    s.append(Paragraph(t["ins_step3_title"], h2))
    s.append(Paragraph(t["ins_step3"], body))
    s.append(Paragraph(t["ins_step4_title"], h2))
    s.append(Paragraph("<bullet>&bull;</bullet> " + t["ins_file"], blt))
    s.append(Paragraph("<bullet>&bull;</bullet> " + t["ins_rev"], blt))
    s.append(Paragraph("<bullet>&bull;</bullet> " + t["ins_date"], blt))
    s.append(Paragraph("<bullet>&bull;</bullet> " + t["ins_valid"], blt))
    s.append(Paragraph(t["ins_step5_title"], h2))
    s.append(Paragraph(t["ins_step5"], body))

    # Fields table
    s.append(sp(3))
    s.append(Paragraph(t["ins_fields_title"], h1))
    s.append(make_table(
        [t["field"], t["description"]],
        [
            [t["fld_product"], t["fld_product_d"]],
            [t["fld_phase"], t["fld_phase_d"]],
            [t["fld_file"], t["fld_file_d"]],
            [t["fld_rev"], t["fld_rev_d"]],
            [t["fld_date"], t["fld_date_d"]],
            [t["fld_validated"], t["fld_validated_d"]],
        ], W))

    s.append(sp(4))
    s.append(Paragraph(t["ins_note"], note))
    s.append(Paragraph(t["ins_warn"], warn))

    doc.build(s,
        onFirstPage=lambda c, d: on_page(c, d, footer_text),
        onLaterPages=lambda c, d: on_page(c, d, footer_text))
    print("  [%s] %s" % (lang.upper(), out_path))


def build_view_manual(lang, t):
    out_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "documenti_visualizza.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    W = A4[0] - 36*mm
    s = []

    footer_text = t["footer"]

    # Cover
    s.append(sp(15))
    if os.path.exists(LOGO_PATH):
        s.append(Image(LOGO_PATH, width=50*mm, height=25*mm, hAlign="CENTER"))
    s.append(sp(8))
    s.append(Paragraph(t["view_title"], title_style))
    s.append(Paragraph(t["view_subtitle"], sub_style))
    s.append(Paragraph("%s - %s" % (t["app"], t["ver"]),
        ParagraphStyle("V2", fontName="Arial", fontSize=10, textColor=HexColor("#616161"), alignment=TA_CENTER)))
    s.append(sp(5))
    s.append(hr())

    # Access
    s.append(Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
        '<font name="Arial-Italic" size="9">%s</font>' % t["view_access"], body))
    s.append(sp(3))
    s.append(Paragraph(t["view_desc"], body))

    # Steps
    s.append(Paragraph(t["view_steps_title"], h1))
    s.append(Paragraph(t["view_step1_title"], h2))
    s.append(Paragraph(t["view_step1"], body))
    s.append(Paragraph(t["view_step2_title"], h2))
    s.append(Paragraph(t["view_step2"], body))
    s.append(Paragraph(t["view_step3_title"], h2))
    s.append(Paragraph(t["view_step3"], body))
    s.append(Paragraph("<bullet>&bull;</bullet> <b>%s</b> - %s" % (t["view_valid"].split(" - ")[0], t["view_valid"].split(" - ")[1]), blt))
    s.append(Paragraph("<bullet>&bull;</bullet> <b>%s</b> - %s" % (t["view_invalid"].split(" - ")[0], t["view_invalid"].split(" - ")[1]), blt))

    s.append(Paragraph(t["view_open_title"], h2))
    s.append(Paragraph(t["view_open"], body))
    s.append(Paragraph(t["view_validate_title"], h2))
    s.append(Paragraph(t["view_validate"], body))

    # Buttons table
    s.append(sp(3))
    s.append(Paragraph(t["view_buttons_title"], h1))
    s.append(make_table(
        [t["button"], t["description"]],
        [
            [t["btn_open"], t["btn_open_d"]],
            [t["btn_validate"], t["btn_validate_d"]],
            [t["btn_close"], t["btn_close_d"]],
        ], W))

    s.append(sp(4))
    s.append(Paragraph(t["view_note"], note))

    doc.build(s,
        onFirstPage=lambda c, d: on_page(c, d, footer_text),
        onLaterPages=lambda c, d: on_page(c, d, footer_text))
    print("  [%s] %s" % (lang.upper(), out_path))


if __name__ == "__main__":
    print("Generazione manuali 'Documenti di Produzione'...")
    for lang_code, texts in TEXTS.items():
        build_insert_manual(lang_code, texts)
        build_view_manual(lang_code, texts)
    print("\nCompletato! 10 PDF generati in manuals/")
