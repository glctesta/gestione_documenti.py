# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per le sezioni Operazioni mancanti in 5 lingue.
Produce: manuals/{lang}/operazioni_gestione_reclami.pdf
         manuals/{lang}/operazioni_ordini.pdf
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
        "app": "TraceabilityRS", "ver": "Versione 2.3.6",
        "field": "Campo", "description": "Descrizione", "button": "Pulsante",
        # -- Gestione Reclami --
        "reclami_title": "Gestione Reclami",
        "reclami_subtitle": "Guida alla gestione dei reclami cliente",
        "reclami_desc": "Questo modulo consente di registrare, tracciare e gestire i reclami provenienti dai clienti. "
                        "Ogni reclamo viene associato a un prodotto, un cliente e una causa principale, permettendo "
                        "l'analisi statistica e il miglioramento continuo del processo produttivo.",
        "reclami_steps_title": "Procedura passo per passo",
        "reclami_step1_t": "1. Nuovo Reclamo",
        "reclami_step1": "Fare clic su 'Nuovo Reclamo' per aprire il modulo di inserimento. "
                         "Compilare tutti i campi obbligatori: cliente, prodotto, data, descrizione del problema.",
        "reclami_step2_t": "2. Assegnazione e Analisi",
        "reclami_step2": "Il reclamo viene assegnato automaticamente al responsabile qualita'. "
                         "E' possibile aggiungere note, allegare documenti e definire le azioni correttive.",
        "reclami_step3_t": "3. Azioni Correttive",
        "reclami_step3": "Definire le azioni correttive necessarie con scadenze e responsabili. "
                         "Il sistema traccia automaticamente lo stato di avanzamento.",
        "reclami_step4_t": "4. Chiusura Reclamo",
        "reclami_step4": "Una volta completate tutte le azioni correttive, il reclamo puo' essere chiuso. "
                         "La chiusura richiede la verifica dell'efficacia delle azioni intraprese.",
        "reclami_fields_title": "Campi principali",
        "fld_cliente": "Cliente *", "fld_cliente_d": "Nome del cliente che ha inoltrato il reclamo",
        "fld_prodotto": "Prodotto *", "fld_prodotto_d": "Prodotto oggetto del reclamo",
        "fld_data": "Data Reclamo *", "fld_data_d": "Data in cui il reclamo e' stato ricevuto",
        "fld_desc": "Descrizione *", "fld_desc_d": "Descrizione dettagliata del problema riscontrato",
        "fld_causa": "Causa Principale", "fld_causa_d": "Categoria della causa radice del difetto",
        "fld_azione": "Azione Correttiva", "fld_azione_d": "Descrizione dell'azione correttiva pianificata",
        "fld_stato": "Stato", "fld_stato_d": "Stato attuale del reclamo (Aperto, In Lavorazione, Chiuso)",
        "reclami_note": "NOTA: I reclami sono visibili a tutti gli utenti, ma solo il responsabile qualita' "
                        "puo' modificarne lo stato e chiuderli.",
        "reclami_warn": "ATTENZIONE: Un reclamo chiuso non puo' essere riaperto. Assicurarsi che tutte le "
                        "azioni correttive siano state completate prima della chiusura.",
        # -- Ordini --
        "ordini_title": "Gestione Ordini",
        "ordini_subtitle": "Guida alla gestione degli ordini di produzione",
        "ordini_desc": "Il modulo Ordini permette di gestire gli ordini di produzione, dalla creazione al completamento. "
                       "Ogni ordine e' associato a un prodotto, una quantita' e una data di consegna prevista.",
        "ordini_steps_title": "Procedura passo per passo",
        "ordini_step1_t": "1. Visualizzare gli Ordini",
        "ordini_step1": "La schermata principale mostra la lista degli ordini attivi. "
                        "E' possibile filtrare per stato, prodotto o data di consegna.",
        "ordini_step2_t": "2. Dettaglio Ordine",
        "ordini_step2": "Fare doppio clic sull'ordine per visualizzarne i dettagli completi: "
                        "quantita' ordinata, quantita' prodotta, stato di avanzamento.",
        "ordini_step3_t": "3. Aggiornare lo Stato",
        "ordini_step3": "Lo stato dell'ordine viene aggiornato automaticamente in base alla produzione registrata. "
                        "E' possibile anche modificarlo manualmente se necessario.",
        "ordini_step4_t": "4. Report Ordini",
        "ordini_step4": "Generare report sullo stato degli ordini con filtri per periodo, cliente o prodotto.",
        "ordini_fields_title": "Campi principali",
        "fld_codice": "Codice Ordine *", "fld_codice_d": "Codice univoco dell'ordine",
        "fld_prod_ord": "Prodotto *", "fld_prod_ord_d": "Prodotto associato all'ordine",
        "fld_qty": "Quantita' *", "fld_qty_d": "Quantita' totale ordinata",
        "fld_data_cons": "Data Consegna *", "fld_data_cons_d": "Data di consegna prevista",
        "fld_cliente_ord": "Cliente", "fld_cliente_ord_d": "Cliente che ha emesso l'ordine",
        "fld_stato_ord": "Stato", "fld_stato_ord_d": "Stato dell'ordine (Nuovo, In Produzione, Completato, Spedito)",
        "ordini_note": "NOTA: Gli ordini completati restano visibili nello storico per consultazione.",
        "ordini_warn": "ATTENZIONE: La modifica della quantita' di un ordine in produzione richiede l'approvazione del responsabile.",
        "footer": "TraceabilityRS - Operazioni",
    },
    "ro": {
        "app": "TraceabilityRS", "ver": "Versiunea 2.3.6",
        "field": "Camp", "description": "Descriere", "button": "Buton",
        "reclami_title": "Gestionare Reclamatii",
        "reclami_subtitle": "Ghid pentru gestionarea reclamatiilor clientilor",
        "reclami_desc": "Acest modul permite inregistrarea, urmarirea si gestionarea reclamatiilor de la clienti. "
                        "Fiecare reclamatie este asociata unui produs, unui client si unei cauze principale.",
        "reclami_steps_title": "Procedura pas cu pas",
        "reclami_step1_t": "1. Reclamatie Noua",
        "reclami_step1": "Faceti clic pe 'Reclamatie Noua' pentru a deschide formularul. Completati toate campurile obligatorii.",
        "reclami_step2_t": "2. Atribuire si Analiza",
        "reclami_step2": "Reclamatia este atribuita automat responsabilului de calitate. Puteti adauga note si documente.",
        "reclami_step3_t": "3. Actiuni Corective",
        "reclami_step3": "Definiti actiunile corective necesare cu termene si responsabili.",
        "reclami_step4_t": "4. Inchidere Reclamatie",
        "reclami_step4": "Dupa completarea actiunilor corective, reclamatia poate fi inchisa.",
        "reclami_fields_title": "Campuri principale",
        "fld_cliente": "Client *", "fld_cliente_d": "Numele clientului care a depus reclamatia",
        "fld_prodotto": "Produs *", "fld_prodotto_d": "Produsul care face obiectul reclamatiei",
        "fld_data": "Data Reclamatie *", "fld_data_d": "Data primirii reclamatiei",
        "fld_desc": "Descriere *", "fld_desc_d": "Descrierea detaliata a problemei",
        "fld_causa": "Cauza Principala", "fld_causa_d": "Categoria cauzei principale a defectului",
        "fld_azione": "Actiune Corectiva", "fld_azione_d": "Descrierea actiunii corective planificate",
        "fld_stato": "Stare", "fld_stato_d": "Starea actuala (Deschis, In Lucru, Inchis)",
        "reclami_note": "NOTA: Reclamatiile sunt vizibile tuturor utilizatorilor, dar numai responsabilul de calitate le poate modifica.",
        "reclami_warn": "ATENTIE: O reclamatie inchisa nu poate fi redeschisa.",
        "ordini_title": "Gestionare Comenzi",
        "ordini_subtitle": "Ghid pentru gestionarea comenzilor de productie",
        "ordini_desc": "Modulul Comenzi permite gestionarea comenzilor de productie, de la creare pana la finalizare.",
        "ordini_steps_title": "Procedura pas cu pas",
        "ordini_step1_t": "1. Vizualizare Comenzi", "ordini_step1": "Ecranul principal arata lista comenzilor active.",
        "ordini_step2_t": "2. Detalii Comanda", "ordini_step2": "Dublu clic pe comanda pentru detalii complete.",
        "ordini_step3_t": "3. Actualizare Stare", "ordini_step3": "Starea comenzii se actualizeaza automat pe baza productiei.",
        "ordini_step4_t": "4. Rapoarte Comenzi", "ordini_step4": "Generati rapoarte cu filtre pe perioada, client sau produs.",
        "ordini_fields_title": "Campuri principale",
        "fld_codice": "Cod Comanda *", "fld_codice_d": "Codul unic al comenzii",
        "fld_prod_ord": "Produs *", "fld_prod_ord_d": "Produsul asociat comenzii",
        "fld_qty": "Cantitate *", "fld_qty_d": "Cantitatea totala comandata",
        "fld_data_cons": "Data Livrare *", "fld_data_cons_d": "Data de livrare prevazuta",
        "fld_cliente_ord": "Client", "fld_cliente_ord_d": "Clientul care a emis comanda",
        "fld_stato_ord": "Stare", "fld_stato_ord_d": "Starea comenzii (Nou, In Productie, Finalizat, Expediat)",
        "ordini_note": "NOTA: Comenzile finalizate raman vizibile in istoric.",
        "ordini_warn": "ATENTIE: Modificarea cantitatii unei comenzi in productie necesita aprobare.",
        "footer": "TraceabilityRS - Operatiuni",
    },
    "en": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "field": "Field", "description": "Description", "button": "Button",
        "reclami_title": "Complaints Management",
        "reclami_subtitle": "Guide to customer complaints management",
        "reclami_desc": "This module allows you to register, track and manage customer complaints. "
                        "Each complaint is associated with a product, customer and root cause.",
        "reclami_steps_title": "Step-by-step procedure",
        "reclami_step1_t": "1. New Complaint", "reclami_step1": "Click 'New Complaint' to open the input form. Fill in all required fields.",
        "reclami_step2_t": "2. Assignment and Analysis", "reclami_step2": "The complaint is automatically assigned to the quality manager.",
        "reclami_step3_t": "3. Corrective Actions", "reclami_step3": "Define the necessary corrective actions with deadlines and responsible persons.",
        "reclami_step4_t": "4. Close Complaint", "reclami_step4": "Once all corrective actions are completed, the complaint can be closed.",
        "reclami_fields_title": "Main Fields",
        "fld_cliente": "Customer *", "fld_cliente_d": "Name of the customer who filed the complaint",
        "fld_prodotto": "Product *", "fld_prodotto_d": "Product subject to the complaint",
        "fld_data": "Complaint Date *", "fld_data_d": "Date the complaint was received",
        "fld_desc": "Description *", "fld_desc_d": "Detailed description of the problem",
        "fld_causa": "Root Cause", "fld_causa_d": "Category of the root cause of the defect",
        "fld_azione": "Corrective Action", "fld_azione_d": "Description of the planned corrective action",
        "fld_stato": "Status", "fld_stato_d": "Current status (Open, In Progress, Closed)",
        "reclami_note": "NOTE: Complaints are visible to all users, but only the quality manager can modify and close them.",
        "reclami_warn": "WARNING: A closed complaint cannot be reopened.",
        "ordini_title": "Orders Management",
        "ordini_subtitle": "Guide to production orders management",
        "ordini_desc": "The Orders module allows you to manage production orders from creation to completion.",
        "ordini_steps_title": "Step-by-step procedure",
        "ordini_step1_t": "1. View Orders", "ordini_step1": "The main screen shows the list of active orders.",
        "ordini_step2_t": "2. Order Details", "ordini_step2": "Double-click on the order for complete details.",
        "ordini_step3_t": "3. Update Status", "ordini_step3": "The order status is automatically updated based on production.",
        "ordini_step4_t": "4. Order Reports", "ordini_step4": "Generate reports with filters by period, customer or product.",
        "ordini_fields_title": "Main Fields",
        "fld_codice": "Order Code *", "fld_codice_d": "Unique order code",
        "fld_prod_ord": "Product *", "fld_prod_ord_d": "Product associated with the order",
        "fld_qty": "Quantity *", "fld_qty_d": "Total quantity ordered",
        "fld_data_cons": "Delivery Date *", "fld_data_cons_d": "Expected delivery date",
        "fld_cliente_ord": "Customer", "fld_cliente_ord_d": "Customer who issued the order",
        "fld_stato_ord": "Status", "fld_stato_ord_d": "Order status (New, In Production, Completed, Shipped)",
        "ordini_note": "NOTE: Completed orders remain visible in the history.",
        "ordini_warn": "WARNING: Modifying the quantity of an order in production requires approval.",
        "footer": "TraceabilityRS - Operations",
    },
    "de": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "field": "Feld", "description": "Beschreibung", "button": "Schaltflaeche",
        "reclami_title": "Reklamationsmanagement",
        "reclami_subtitle": "Anleitung zur Verwaltung von Kundenreklamationen",
        "reclami_desc": "Dieses Modul ermoeglicht die Registrierung, Verfolgung und Verwaltung von Kundenreklamationen.",
        "reclami_steps_title": "Schritt-fuer-Schritt-Anleitung",
        "reclami_step1_t": "1. Neue Reklamation", "reclami_step1": "Klicken Sie auf 'Neue Reklamation', um das Eingabeformular zu oeffnen.",
        "reclami_step2_t": "2. Zuweisung und Analyse", "reclami_step2": "Die Reklamation wird automatisch dem Qualitaetsverantwortlichen zugewiesen.",
        "reclami_step3_t": "3. Korrekturmassnahmen", "reclami_step3": "Definieren Sie die notwendigen Korrekturmassnahmen mit Fristen.",
        "reclami_step4_t": "4. Reklamation schliessen", "reclami_step4": "Nach Abschluss aller Korrekturmassnahmen kann die Reklamation geschlossen werden.",
        "reclami_fields_title": "Hauptfelder",
        "fld_cliente": "Kunde *", "fld_cliente_d": "Name des Kunden",
        "fld_prodotto": "Produkt *", "fld_prodotto_d": "Betroffenes Produkt",
        "fld_data": "Reklamationsdatum *", "fld_data_d": "Eingangsdatum der Reklamation",
        "fld_desc": "Beschreibung *", "fld_desc_d": "Detaillierte Beschreibung des Problems",
        "fld_causa": "Hauptursache", "fld_causa_d": "Kategorie der Grundursache",
        "fld_azione": "Korrekturmassnahme", "fld_azione_d": "Beschreibung der geplanten Korrekturmassnahme",
        "fld_stato": "Status", "fld_stato_d": "Aktueller Status (Offen, In Bearbeitung, Geschlossen)",
        "reclami_note": "HINWEIS: Reklamationen sind fuer alle Benutzer sichtbar.",
        "reclami_warn": "ACHTUNG: Eine geschlossene Reklamation kann nicht wieder geoeffnet werden.",
        "ordini_title": "Auftragsverwaltung",
        "ordini_subtitle": "Anleitung zur Verwaltung von Produktionsauftraegen",
        "ordini_desc": "Das Auftragsmodul ermoeglicht die Verwaltung von Produktionsauftraegen.",
        "ordini_steps_title": "Schritt-fuer-Schritt-Anleitung",
        "ordini_step1_t": "1. Auftraege anzeigen", "ordini_step1": "Der Hauptbildschirm zeigt die Liste der aktiven Auftraege.",
        "ordini_step2_t": "2. Auftragsdetails", "ordini_step2": "Doppelklicken Sie auf den Auftrag fuer vollstaendige Details.",
        "ordini_step3_t": "3. Status aktualisieren", "ordini_step3": "Der Auftragsstatus wird automatisch aktualisiert.",
        "ordini_step4_t": "4. Auftragsberichte", "ordini_step4": "Erstellen Sie Berichte mit Filtern.",
        "ordini_fields_title": "Hauptfelder",
        "fld_codice": "Auftragscode *", "fld_codice_d": "Eindeutiger Auftragscode",
        "fld_prod_ord": "Produkt *", "fld_prod_ord_d": "Zugeordnetes Produkt",
        "fld_qty": "Menge *", "fld_qty_d": "Bestellte Gesamtmenge",
        "fld_data_cons": "Lieferdatum *", "fld_data_cons_d": "Voraussichtliches Lieferdatum",
        "fld_cliente_ord": "Kunde", "fld_cliente_ord_d": "Kunde, der den Auftrag erteilt hat",
        "fld_stato_ord": "Status", "fld_stato_ord_d": "Auftragsstatus (Neu, In Produktion, Abgeschlossen, Versendet)",
        "ordini_note": "HINWEIS: Abgeschlossene Auftraege bleiben im Verlauf sichtbar.",
        "ordini_warn": "ACHTUNG: Die Aenderung der Menge erfordert eine Genehmigung.",
        "footer": "TraceabilityRS - Operationen",
    },
    "sv": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "field": "Faelt", "description": "Beskrivning", "button": "Knapp",
        "reclami_title": "Reklamationshantering",
        "reclami_subtitle": "Guide foer hantering av kundreklamationer",
        "reclami_desc": "Denna modul goer det moejligt att registrera, spoera och hantera kundreklamationer.",
        "reclami_steps_title": "Steg-foer-steg-procedur",
        "reclami_step1_t": "1. Ny reklamation", "reclami_step1": "Klicka poe 'Ny reklamation' foer att oeppna formulaeret.",
        "reclami_step2_t": "2. Tilldelning och analys", "reclami_step2": "Reklamationen tilldelas automatiskt kvalitetsansvarig.",
        "reclami_step3_t": "3. Korrigerande oetgaerder", "reclami_step3": "Definiera noedvaendiga korrigerande oetgaerder med tidsfrister.",
        "reclami_step4_t": "4. Staeng reklamation", "reclami_step4": "Naer alla korrigerande oetgaerder aer klara kan reklamationen staengas.",
        "reclami_fields_title": "Huvudfaelt",
        "fld_cliente": "Kund *", "fld_cliente_d": "Kundens namn",
        "fld_prodotto": "Produkt *", "fld_prodotto_d": "Beroerd produkt",
        "fld_data": "Reklamationsdatum *", "fld_data_d": "Datum foer mottagande",
        "fld_desc": "Beskrivning *", "fld_desc_d": "Detaljerad beskrivning av problemet",
        "fld_causa": "Grundorsak", "fld_causa_d": "Kategori foer grundorsaken",
        "fld_azione": "Korrigerande oetgaerd", "fld_azione_d": "Beskrivning av planerad oetgaerd",
        "fld_stato": "Status", "fld_stato_d": "Aktuell status (Oeppen, Pagoer, Staengd)",
        "reclami_note": "NOTERA: Reklamationer aer synliga foer alla anvaendare.",
        "reclami_warn": "VARNING: En staengd reklamation kan inte oeppnas igen.",
        "ordini_title": "Orderhantering",
        "ordini_subtitle": "Guide foer hantering av produktionsordrar",
        "ordini_desc": "Ordermodulen goer det moejligt att hantera produktionsordrar froen skapande till slutfoerande.",
        "ordini_steps_title": "Steg-foer-steg-procedur",
        "ordini_step1_t": "1. Visa ordrar", "ordini_step1": "Huvudskaermen visar listan oevar aktiva ordrar.",
        "ordini_step2_t": "2. Orderdetaljer", "ordini_step2": "Dubbelklicka poe ordern foer fullstaendiga detaljer.",
        "ordini_step3_t": "3. Uppdatera status", "ordini_step3": "Orderstatus uppdateras automatiskt baserat poe produktion.",
        "ordini_step4_t": "4. Orderrapporter", "ordini_step4": "Generera rapporter med filter.",
        "ordini_fields_title": "Huvudfaelt",
        "fld_codice": "Orderkod *", "fld_codice_d": "Unik orderkod",
        "fld_prod_ord": "Produkt *", "fld_prod_ord_d": "Tillhoerande produkt",
        "fld_qty": "Kvantitet *", "fld_qty_d": "Total bestaelld kvantitet",
        "fld_data_cons": "Leveransdatum *", "fld_data_cons_d": "Foervaentat leveransdatum",
        "fld_cliente_ord": "Kund", "fld_cliente_ord_d": "Kund som lade bestaellningen",
        "fld_stato_ord": "Status", "fld_stato_ord_d": "Orderstatus (Ny, I Produktion, Klar, Skickad)",
        "ordini_note": "NOTERA: Slutfoerda ordrar foerblir synliga i historiken.",
        "ordini_warn": "VARNING: Aendring av kvantitet kraever godkaennande.",
        "footer": "TraceabilityRS - Operationer",
    },
}


def _cover(story, T, W):
    story.append(sp(20))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=50*mm, height=50*mm))
        story.append(sp(6))
    story.append(Paragraph(T["app"], title_style))
    story.append(Paragraph(T["ver"], sub_style))


def build_reclami(lang, T):
    out = os.path.join(BASE_DIR, lang, "operazioni_gestione_reclami.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)
    W = A4[0] - 30*mm
    story = []
    _cover(story, T, W)
    story.append(Paragraph(T["reclami_title"], title_style))
    story.append(Paragraph(T["reclami_subtitle"], sub_style))
    story.append(hr())
    story.append(Paragraph(T["reclami_desc"], body))
    story.append(sp(4))
    story.append(Paragraph(T["reclami_steps_title"], h1))
    for i in range(1, 5):
        story.append(Paragraph(T[f"reclami_step{i}_t"], h2))
        story.append(Paragraph(T[f"reclami_step{i}"], body))
    story.append(hr())
    story.append(Paragraph(T["reclami_fields_title"], h1))
    rows = []
    for k in ["fld_cliente", "fld_prodotto", "fld_data", "fld_desc", "fld_causa", "fld_azione", "fld_stato"]:
        rows.append([Paragraph(T[k], body), Paragraph(T[k+"_d"], body)])
    story.append(make_table([Paragraph(T["field"], body), Paragraph(T["description"], body)], rows, W))
    story.append(sp(4))
    story.append(Paragraph(T["reclami_note"], note))
    story.append(Paragraph(T["reclami_warn"], warn))
    doc.build(story, onFirstPage=lambda c,d: on_page(c,d,T["footer"]),
              onLaterPages=lambda c,d: on_page(c,d,T["footer"]))
    print(f"  -> {out}")


def build_ordini(lang, T):
    out = os.path.join(BASE_DIR, lang, "operazioni_ordini.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)
    W = A4[0] - 30*mm
    story = []
    _cover(story, T, W)
    story.append(Paragraph(T["ordini_title"], title_style))
    story.append(Paragraph(T["ordini_subtitle"], sub_style))
    story.append(hr())
    story.append(Paragraph(T["ordini_desc"], body))
    story.append(sp(4))
    story.append(Paragraph(T["ordini_steps_title"], h1))
    for i in range(1, 5):
        story.append(Paragraph(T[f"ordini_step{i}_t"], h2))
        story.append(Paragraph(T[f"ordini_step{i}"], body))
    story.append(hr())
    story.append(Paragraph(T["ordini_fields_title"], h1))
    rows = []
    for k in ["fld_codice", "fld_prod_ord", "fld_qty", "fld_data_cons", "fld_cliente_ord", "fld_stato_ord"]:
        rows.append([Paragraph(T[k], body), Paragraph(T[k+"_d"], body)])
    story.append(make_table([Paragraph(T["field"], body), Paragraph(T["description"], body)], rows, W))
    story.append(sp(4))
    story.append(Paragraph(T["ordini_note"], note))
    story.append(Paragraph(T["ordini_warn"], warn))
    doc.build(story, onFirstPage=lambda c,d: on_page(c,d,T["footer"]),
              onLaterPages=lambda c,d: on_page(c,d,T["footer"]))
    print(f"  -> {out}")


if __name__ == "__main__":
    for lang in ("it", "ro", "en", "de", "sv"):
        d = os.path.join(BASE_DIR, lang)
        os.makedirs(d, exist_ok=True)
        T = TEXTS[lang]
        print(f"[{lang}]")
        build_reclami(lang, T)
        build_ordini(lang, T)
    print("\nDone! 10 PDF generati.")
