# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Documenti Generali' in 5 lingue.
Un unico manuale per entrambe le modalita' (Modifica + Visualizza)
che spiega la procedura comune a tutte le categorie.

Produce: manuals/{lang}/documenti_generali_modifica.pdf
         manuals/{lang}/documenti_generali_visualizza.pdf
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
tip = ParagraphStyle("TIP", fontName="Arial-Italic", fontSize=9,
    textColor=GREEN_D, spaceAfter=3*mm, spaceBefore=2*mm,
    leftIndent=6*mm, leading=12, backColor=HexColor("#e8f5e9"),
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
TEXTS = {
    "it": {
        "app": "TraceabilityRS", "ver": "Versione 2.3.6",
        # MODIFICA (edit mode)
        "mod_title": "Gestione Documenti Generali",
        "mod_subtitle": "Guida alla gestione (Aggiungi/Modifica/Elimina)",
        "mod_access": "Necessita autenticazione (login)",
        "mod_intro": "Questa sezione permette di gestire documenti di vario tipo, organizzati per categorie. "
                     "Il menu presenta diverse categorie (es. Istruzioni di Lavoro, Procedure Qualita', "
                     "Schede di Sicurezza, ecc.). L'interfaccia e le operazioni disponibili sono "
                     "<b>identiche per ogni categoria</b>: cambia solo l'argomento dei documenti.",
        "mod_categories": "Il menu Documenti Generali contiene diverse categorie, ciascuna con le opzioni "
                          "'Aggiungi/Modifica' e 'Visualizza'. Le categorie sono configurabili dall'amministratore "
                          "e possono variare.",
        "mod_window_title": "La Finestra di Gestione",
        "mod_window_desc": "La finestra mostra una tabella con tutti i documenti della categoria selezionata:",
        "col_title": "Titolo", "col_title_d": "Nome del documento",
        "col_version": "Versione", "col_version_d": "Numero di versione del documento",
        "col_user": "Caricato Da", "col_user_d": "Nome dell'utente che ha caricato il documento",
        "col_date": "Data Caricamento", "col_date_d": "Data e ora di caricamento",
        "mod_add_title": "Aggiungere un Nuovo Documento",
        "mod_add_desc": "Premere il pulsante 'Aggiungi Nuovo'. Si apre un dialogo con i seguenti campi:",
        "fld_title": "Titolo (*)", "fld_title_d": "Nome identificativo del documento (obbligatorio)",
        "fld_desc": "Descrizione", "fld_desc_d": "Descrizione opzionale del contenuto",
        "fld_ver": "Versione", "fld_ver_d": "Numero di versione (opzionale)",
        "fld_file": "File (*)", "fld_file_d": "File da caricare - premere 'Sfoglia...' (obbligatorio)",
        "mod_edit_title": "Modificare un Documento",
        "mod_edit_desc": "Selezionare il documento nella tabella e premere 'Modifica Selezionato'. "
                         "Si apre lo stesso dialogo con i dati pre-compilati. E' possibile modificare "
                         "titolo, descrizione, versione o sostituire il file.",
        "mod_delete_title": "Eliminare un Documento",
        "mod_delete_desc": "Selezionare il documento e premere 'Cancella Selezionato'. "
                           "Il sistema chiedera' conferma prima della cancellazione.",
        "mod_open_title": "Aprire un Documento",
        "mod_open_desc": "Fare doppio clic sulla riga del documento nella tabella per aprirlo "
                         "con l'applicazione predefinita del sistema.",
        "mod_warn": "ATTENZIONE: La cancellazione e' definitiva e irreversibile. "
                    "Assicurarsi di voler eliminare il documento prima di confermare.",
        "mod_note": "NOTA: Tutti i file vengono salvati come dati binari nel database. "
                    "Non e' necessario gestire percorsi di rete o cartelle condivise.",
        "mod_tip": "SUGGERIMENTO: Ogni categoria funziona esattamente allo stesso modo. "
                   "Una volta appresa la procedura per una categoria, si applica a tutte le altre.",
        # VISUALIZZA
        "view_title": "Visualizzazione Documenti Generali",
        "view_subtitle": "Guida alla consultazione (sola lettura)",
        "view_access": "Accesso diretto (senza login)",
        "view_intro": "Questa modalita' permette di consultare i documenti senza possibilita' di modifica. "
                      "E' disponibile per tutti gli utenti senza necessita' di autenticazione.",
        "view_intro2": "Come per la modalita' di gestione, il menu presenta le stesse categorie. "
                       "L'interfaccia e' <b>identica per ogni categoria</b>: cambia solo il contenuto.",
        "view_window_desc": "La finestra mostra la stessa tabella della modalita' gestione, ma senza "
                            "i pulsanti Aggiungi/Modifica/Cancella.",
        "view_open": "Aprire un Documento",
        "view_open_desc": "Fare doppio clic sulla riga del documento per aprirlo con "
                          "l'applicazione predefinita del sistema.",
        "view_note": "NOTA: In questa modalita' non e' possibile aggiungere, modificare o eliminare documenti. "
                     "Per tali operazioni, utilizzare la voce 'Aggiungi/Modifica' dal menu.",
        "field": "Campo", "column": "Colonna", "description": "Descrizione",
        "footer": "TraceabilityRS - Documenti Generali",
    },
    "ro": {
        "app": "TraceabilityRS", "ver": "Versiunea 2.3.6",
        "mod_title": "Gestionare Documente Generale",
        "mod_subtitle": "Ghid de gestionare (Adaugare/Modificare/Stergere)",
        "mod_access": "Necesita autentificare (login)",
        "mod_intro": "Aceasta sectiune permite gestionarea documentelor de diferite tipuri, organizate pe categorii. "
                     "Meniul prezinta diverse categorii (ex: Instructiuni de Lucru, Proceduri Calitate, "
                     "Fise de Securitate etc.). Interfata si operatiunile disponibile sunt "
                     "<b>identice pentru fiecare categorie</b>: difera doar subiectul documentelor.",
        "mod_categories": "Meniul Documente Generale contine mai multe categorii, fiecare cu optiunile "
                          "'Adaugare/Modificare' si 'Vizualizare'. Categoriile sunt configurabile de administrator.",
        "mod_window_title": "Fereastra de Gestionare",
        "mod_window_desc": "Fereastra afiseaza un tabel cu toate documentele din categoria selectata:",
        "col_title": "Titlu", "col_title_d": "Numele documentului",
        "col_version": "Versiune", "col_version_d": "Numarul de versiune al documentului",
        "col_user": "Incarcat De", "col_user_d": "Numele utilizatorului care a incarcat documentul",
        "col_date": "Data Incarcarii", "col_date_d": "Data si ora incarcarii",
        "mod_add_title": "Adaugarea unui Document Nou",
        "mod_add_desc": "Apasati butonul 'Adauga Nou'. Se deschide un dialog cu urmatoarele campuri:",
        "fld_title": "Titlu (*)", "fld_title_d": "Numele identificativ al documentului (obligatoriu)",
        "fld_desc": "Descriere", "fld_desc_d": "Descrierea optionala a continutului",
        "fld_ver": "Versiune", "fld_ver_d": "Numarul de versiune (optional)",
        "fld_file": "Fisier (*)", "fld_file_d": "Fisierul de incarcat - apasati 'Rasfoieste...' (obligatoriu)",
        "mod_edit_title": "Modificarea unui Document",
        "mod_edit_desc": "Selectati documentul in tabel si apasati 'Modifica Selectat'. "
                         "Se deschide acelasi dialog cu datele pre-completate. Puteti modifica "
                         "titlul, descrierea, versiunea sau inlocui fisierul.",
        "mod_delete_title": "Stergerea unui Document",
        "mod_delete_desc": "Selectati documentul si apasati 'Sterge Selectat'. "
                           "Sistemul va solicita confirmarea inainte de stergere.",
        "mod_open_title": "Deschiderea unui Document",
        "mod_open_desc": "Faceti dublu clic pe randul documentului in tabel pentru a-l deschide "
                         "cu aplicatia implicita a sistemului.",
        "mod_warn": "ATENTIE: Stergerea este definitiva si ireversibila. "
                    "Asigurati-va ca doriti sa eliminati documentul inainte de confirmare.",
        "mod_note": "NOTA: Toate fisierele sunt salvate ca date binare in baza de date. "
                    "Nu este necesar sa gestionati cai de retea sau dosare partajate.",
        "mod_tip": "SFAT: Fiecare categorie functioneaza exact in acelasi mod. "
                   "Odata invatata procedura pentru o categorie, se aplica la toate celelalte.",
        "view_title": "Vizualizare Documente Generale",
        "view_subtitle": "Ghid de consultare (doar citire)",
        "view_access": "Acces direct (fara login)",
        "view_intro": "Acest mod permite consultarea documentelor fara posibilitatea de modificare. "
                      "Este disponibil pentru toti utilizatorii fara necesitatea autentificarii.",
        "view_intro2": "Ca si in modul de gestionare, meniul prezinta aceleasi categorii. "
                       "Interfata este <b>identica pentru fiecare categorie</b>: difera doar continutul.",
        "view_window_desc": "Fereastra afiseaza acelasi tabel ca in modul gestionare, dar fara "
                            "butoanele Adauga/Modifica/Sterge.",
        "view_open": "Deschiderea unui Document",
        "view_open_desc": "Faceti dublu clic pe randul documentului pentru a-l deschide cu "
                          "aplicatia implicita a sistemului.",
        "view_note": "NOTA: In acest mod nu puteti adauga, modifica sau sterge documente. "
                     "Pentru astfel de operatiuni, folositi optiunea 'Adaugare/Modificare' din meniu.",
        "field": "Camp", "column": "Coloana", "description": "Descriere",
        "footer": "TraceabilityRS - Documente Generale",
    },
    "en": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "mod_title": "General Documents Management",
        "mod_subtitle": "Management Guide (Add/Edit/Delete)",
        "mod_access": "Requires authentication (login)",
        "mod_intro": "This section allows managing documents of various types, organized by categories. "
                     "The menu presents different categories (e.g., Work Instructions, Quality Procedures, "
                     "Safety Data Sheets, etc.). The interface and available operations are "
                     "<b>identical for every category</b>: only the document subject differs.",
        "mod_categories": "The General Documents menu contains various categories, each with "
                          "'Add/Edit' and 'View' options. Categories are configurable by the administrator.",
        "mod_window_title": "The Management Window",
        "mod_window_desc": "The window displays a table with all documents in the selected category:",
        "col_title": "Title", "col_title_d": "Document name",
        "col_version": "Version", "col_version_d": "Document version number",
        "col_user": "Uploaded By", "col_user_d": "Name of the user who uploaded the document",
        "col_date": "Upload Date", "col_date_d": "Upload date and time",
        "mod_add_title": "Adding a New Document",
        "mod_add_desc": "Press the 'Add New' button. A dialog opens with the following fields:",
        "fld_title": "Title (*)", "fld_title_d": "Document identifier name (required)",
        "fld_desc": "Description", "fld_desc_d": "Optional content description",
        "fld_ver": "Version", "fld_ver_d": "Version number (optional)",
        "fld_file": "File (*)", "fld_file_d": "File to upload - press 'Browse...' (required)",
        "mod_edit_title": "Editing a Document",
        "mod_edit_desc": "Select the document in the table and press 'Edit Selected'. "
                         "The same dialog opens with pre-filled data. You can modify the "
                         "title, description, version, or replace the file.",
        "mod_delete_title": "Deleting a Document",
        "mod_delete_desc": "Select the document and press 'Delete Selected'. "
                           "The system will ask for confirmation before deletion.",
        "mod_open_title": "Opening a Document",
        "mod_open_desc": "Double-click the document row in the table to open it "
                         "with the system's default application.",
        "mod_warn": "WARNING: Deletion is permanent and irreversible. "
                    "Make sure you want to delete the document before confirming.",
        "mod_note": "NOTE: All files are stored as binary data in the database. "
                    "No network paths or shared folders need to be managed.",
        "mod_tip": "TIP: Every category works exactly the same way. "
                   "Once you learn the procedure for one category, it applies to all others.",
        "view_title": "View General Documents",
        "view_subtitle": "Consultation Guide (read-only)",
        "view_access": "Direct access (no login required)",
        "view_intro": "This mode allows consulting documents without the ability to modify them. "
                      "It is available to all users without authentication.",
        "view_intro2": "As with the management mode, the menu presents the same categories. "
                       "The interface is <b>identical for every category</b>: only the content differs.",
        "view_window_desc": "The window shows the same table as management mode, but without "
                            "the Add/Edit/Delete buttons.",
        "view_open": "Opening a Document",
        "view_open_desc": "Double-click the document row to open it with "
                          "the system's default application.",
        "view_note": "NOTE: In this mode you cannot add, edit, or delete documents. "
                     "For such operations, use the 'Add/Edit' option from the menu.",
        "field": "Field", "column": "Column", "description": "Description",
        "footer": "TraceabilityRS - General Documents",
    },
    "de": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "mod_title": "Verwaltung Allgemeiner Dokumente",
        "mod_subtitle": "Verwaltungsanleitung (Hinzufuegen/Bearbeiten/Loeschen)",
        "mod_access": "Erfordert Authentifizierung (Login)",
        "mod_intro": "Dieser Bereich ermoeglicht die Verwaltung verschiedener Dokumenttypen, "
                     "nach Kategorien organisiert. Das Menue zeigt verschiedene Kategorien "
                     "(z.B. Arbeitsanweisungen, Qualitaetsverfahren, Sicherheitsdatenblaetter usw.). "
                     "Die Oberflaeche und verfuegbaren Operationen sind "
                     "<b>fuer jede Kategorie identisch</b>: nur das Thema der Dokumente aendert sich.",
        "mod_categories": "Das Menue Allgemeine Dokumente enthaelt verschiedene Kategorien, "
                          "jeweils mit den Optionen 'Hinzufuegen/Bearbeiten' und 'Anzeigen'.",
        "mod_window_title": "Das Verwaltungsfenster",
        "mod_window_desc": "Das Fenster zeigt eine Tabelle aller Dokumente der gewaehlten Kategorie:",
        "col_title": "Titel", "col_title_d": "Dokumentname",
        "col_version": "Version", "col_version_d": "Versionsnummer des Dokuments",
        "col_user": "Hochgeladen von", "col_user_d": "Name des Benutzers, der das Dokument hochgeladen hat",
        "col_date": "Upload-Datum", "col_date_d": "Datum und Uhrzeit des Uploads",
        "mod_add_title": "Neues Dokument hinzufuegen",
        "mod_add_desc": "Klicken Sie auf 'Neu hinzufuegen'. Ein Dialog mit folgenden Feldern oeffnet sich:",
        "fld_title": "Titel (*)", "fld_title_d": "Dokumentbezeichnung (Pflichtfeld)",
        "fld_desc": "Beschreibung", "fld_desc_d": "Optionale Inhaltsbeschreibung",
        "fld_ver": "Version", "fld_ver_d": "Versionsnummer (optional)",
        "fld_file": "Datei (*)", "fld_file_d": "Datei zum Hochladen - 'Durchsuchen...' (Pflichtfeld)",
        "mod_edit_title": "Dokument bearbeiten",
        "mod_edit_desc": "Dokument in der Tabelle auswaehlen und 'Ausgewaehltes bearbeiten' klicken. "
                         "Der gleiche Dialog oeffnet sich mit vorausgefuellten Daten.",
        "mod_delete_title": "Dokument loeschen",
        "mod_delete_desc": "Dokument auswaehlen und 'Ausgewaehltes loeschen' klicken. "
                           "Das System fragt vor der Loeschung nach Bestaetigung.",
        "mod_open_title": "Dokument oeffnen",
        "mod_open_desc": "Doppelklick auf die Dokumentzeile, um es mit der Standardanwendung zu oeffnen.",
        "mod_warn": "ACHTUNG: Die Loeschung ist endgueltig und unwiderruflich.",
        "mod_note": "HINWEIS: Alle Dateien werden als Binaerdaten in der Datenbank gespeichert.",
        "mod_tip": "TIPP: Jede Kategorie funktioniert genau gleich. "
                   "Einmal erlernt, gilt die Prozedur fuer alle Kategorien.",
        "view_title": "Allgemeine Dokumente Anzeigen",
        "view_subtitle": "Anleitung zur Einsicht (nur lesen)",
        "view_access": "Direkter Zugriff (kein Login erforderlich)",
        "view_intro": "Dieser Modus erlaubt die Einsicht ohne Aenderungsmoeglichkeit.",
        "view_intro2": "Wie im Verwaltungsmodus zeigt das Menue die gleichen Kategorien. "
                       "Die Oberflaeche ist <b>fuer jede Kategorie identisch</b>.",
        "view_window_desc": "Das Fenster zeigt die gleiche Tabelle, jedoch ohne "
                            "Hinzufuegen/Bearbeiten/Loeschen-Schaltflaechen.",
        "view_open": "Dokument oeffnen",
        "view_open_desc": "Doppelklick auf die Dokumentzeile zum Oeffnen.",
        "view_note": "HINWEIS: In diesem Modus koennen Sie keine Dokumente hinzufuegen, bearbeiten oder loeschen.",
        "field": "Feld", "column": "Spalte", "description": "Beschreibung",
        "footer": "TraceabilityRS - Allgemeine Dokumente",
    },
    "sv": {
        "app": "TraceabilityRS", "ver": "Version 2.3.6",
        "mod_title": "Hantering av Allmanna Dokument",
        "mod_subtitle": "Hanteringsguide (Laegga till/Redigera/Ta bort)",
        "mod_access": "Kraever autentisering (inloggning)",
        "mod_intro": "Denna sektion goer det moejligt att hantera dokument av olika typer, "
                     "organiserade i kategorier. Menyn presenterar olika kategorier. "
                     "Graenssnittet och tillgaengliga operationer aer "
                     "<b>identiska foer varje kategori</b>: bara dokumentaemnet skiljer sig.",
        "mod_categories": "Menyn Allmanna Dokument innehaaller flera kategorier, "
                          "var och en med 'Laegga till/Redigera' och 'Visa'.",
        "mod_window_title": "Hanteringsfoenestret",
        "mod_window_desc": "Foenestret visar en tabell med alla dokument i den valda kategorin:",
        "col_title": "Titel", "col_title_d": "Dokumentnamn",
        "col_version": "Version", "col_version_d": "Dokumentets versionsnummer",
        "col_user": "Uppladdad av", "col_user_d": "Anvaendarnamn",
        "col_date": "Uppladdningsdatum", "col_date_d": "Datum och tid foer uppladdning",
        "mod_add_title": "Laegga till ett nytt dokument",
        "mod_add_desc": "Klicka 'Laegga till ny'. En dialog oeppnas med foeljande faelt:",
        "fld_title": "Titel (*)", "fld_title_d": "Dokumentets identifieringsnamn (obligatoriskt)",
        "fld_desc": "Beskrivning", "fld_desc_d": "Valfri innehaallsbeskrivning",
        "fld_ver": "Version", "fld_ver_d": "Versionsnummer (valfritt)",
        "fld_file": "Fil (*)", "fld_file_d": "Fil att ladda upp - klicka 'Blaeddra...' (obligatoriskt)",
        "mod_edit_title": "Redigera ett dokument",
        "mod_edit_desc": "Vaelj dokumentet och klicka 'Redigera valt'. Samma dialog oeppnas med ifoerda data.",
        "mod_delete_title": "Ta bort ett dokument",
        "mod_delete_desc": "Vaelj dokumentet och klicka 'Ta bort valt'. Systemet fraagar om bekraeftelse.",
        "mod_open_title": "Oeppna ett dokument",
        "mod_open_desc": "Dubbelklicka paa dokumentraden foer att oeppna det med standardprogrammet.",
        "mod_warn": "VARNING: Borttagning aer permanent och oaaaterkallelig.",
        "mod_note": "OBS: Alla filer lagras som binaerdata i databasen.",
        "mod_tip": "TIPS: Varje kategori fungerar exakt likadant. "
                   "Naer du laert dig proceduren foer en kategori, gaeller den foer alla andra.",
        "view_title": "Visa Allmanna Dokument",
        "view_subtitle": "Visningsguide (skrivskyddad)",
        "view_access": "Direkt aatkomst (ingen inloggning kraevs)",
        "view_intro": "Detta laege goer det moejligt att laesa dokument utan aendringsmoejlighet.",
        "view_intro2": "Som i hanteringslaege visar menyn samma kategorier. "
                       "Graenssnittet aer <b>identiskt foer varje kategori</b>.",
        "view_window_desc": "Foenestret visar samma tabell, men utan knappar foer redigering.",
        "view_open": "Oeppna ett Dokument",
        "view_open_desc": "Dubbelklicka paa dokumentraden foer att oeppna det.",
        "view_note": "OBS: I detta laege kan du inte laegga till, redigera eller ta bort dokument.",
        "field": "Faelt", "column": "Kolumn", "description": "Beskrivning",
        "footer": "TraceabilityRS - Allmanna Dokument",
    },
}


def build_modifica_manual(lang, t):
    out_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "documenti_generali_modifica.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    W = A4[0] - 36*mm
    s = []
    ft = t["footer"]

    # Cover
    s.append(sp(15))
    if os.path.exists(LOGO_PATH):
        s.append(Image(LOGO_PATH, width=50*mm, height=25*mm, hAlign="CENTER"))
    s.append(sp(8))
    s.append(Paragraph(t["mod_title"], title_style))
    s.append(Paragraph(t["mod_subtitle"], sub_style))
    s.append(Paragraph("%s - %s" % (t["app"], t["ver"]),
        ParagraphStyle("V", fontName="Arial", fontSize=10, textColor=HexColor("#616161"), alignment=TA_CENTER)))
    s.append(sp(5))
    s.append(hr())

    # Access + intro
    s.append(Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
        '<font name="Arial-Italic" size="9">%s</font>' % t["mod_access"], body))
    s.append(sp(3))
    s.append(Paragraph(t["mod_intro"], body))
    s.append(sp(2))
    s.append(Paragraph(t["mod_tip"], tip))
    s.append(sp(2))
    s.append(Paragraph(t["mod_categories"], body))

    # Table columns
    s.append(Paragraph(t["mod_window_title"], h1))
    s.append(Paragraph(t["mod_window_desc"], body))
    s.append(make_table(
        [t["column"], t["description"]],
        [
            [t["col_title"], t["col_title_d"]],
            [t["col_version"], t["col_version_d"]],
            [t["col_user"], t["col_user_d"]],
            [t["col_date"], t["col_date_d"]],
        ], W))

    # Add
    s.append(Paragraph(t["mod_add_title"], h2))
    s.append(Paragraph(t["mod_add_desc"], body))
    s.append(make_table(
        [t["field"], t["description"]],
        [
            [t["fld_title"], t["fld_title_d"]],
            [t["fld_desc"], t["fld_desc_d"]],
            [t["fld_ver"], t["fld_ver_d"]],
            [t["fld_file"], t["fld_file_d"]],
        ], W))

    # Edit
    s.append(Paragraph(t["mod_edit_title"], h2))
    s.append(Paragraph(t["mod_edit_desc"], body))

    # Delete
    s.append(Paragraph(t["mod_delete_title"], h2))
    s.append(Paragraph(t["mod_delete_desc"], body))

    # Open
    s.append(Paragraph(t["mod_open_title"], h2))
    s.append(Paragraph(t["mod_open_desc"], body))

    # Notes
    s.append(sp(3))
    s.append(Paragraph(t["mod_warn"], warn))
    s.append(Paragraph(t["mod_note"], note))

    doc.build(s,
        onFirstPage=lambda c, d: on_page(c, d, ft),
        onLaterPages=lambda c, d: on_page(c, d, ft))
    print("  [%s] %s" % (lang.upper(), out_path))


def build_visualizza_manual(lang, t):
    out_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "documenti_generali_visualizza.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    W = A4[0] - 36*mm
    s = []
    ft = t["footer"]

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

    # Access + intro
    s.append(Paragraph(
        '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
        '<font name="Arial-Italic" size="9">%s</font>' % t["view_access"], body))
    s.append(sp(3))
    s.append(Paragraph(t["view_intro"], body))
    s.append(Paragraph(t["view_intro2"], body))
    s.append(sp(2))
    s.append(Paragraph(t["mod_tip"], tip))

    # Table columns
    s.append(Paragraph(t["mod_window_title"], h1))
    s.append(Paragraph(t["view_window_desc"], body))
    s.append(make_table(
        [t["column"], t["description"]],
        [
            [t["col_title"], t["col_title_d"]],
            [t["col_version"], t["col_version_d"]],
            [t["col_user"], t["col_user_d"]],
            [t["col_date"], t["col_date_d"]],
        ], W))

    # Open
    s.append(Paragraph(t["view_open"], h2))
    s.append(Paragraph(t["view_open_desc"], body))

    # Note
    s.append(sp(3))
    s.append(Paragraph(t["view_note"], note))

    doc.build(s,
        onFirstPage=lambda c, d: on_page(c, d, ft),
        onLaterPages=lambda c, d: on_page(c, d, ft))
    print("  [%s] %s" % (lang.upper(), out_path))


if __name__ == "__main__":
    print("Generazione manuali 'Documenti Generali'...")
    for lang_code, texts in TEXTS.items():
        build_modifica_manual(lang_code, texts)
        build_visualizza_manual(lang_code, texts)
    print("\nCompletato! 10 PDF generati in manuals/")
