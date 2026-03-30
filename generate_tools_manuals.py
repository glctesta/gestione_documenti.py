# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Strumenti' in 5 lingue.
Produce: manuals/{lang}/strumenti_autorizzazioni.pdf
         manuals/{lang}/strumenti_materiali.pdf
         manuals/{lang}/strumenti_room_booking.pdf
         manuals/{lang}/strumenti_tipi_scrap.pdf
         manuals/{lang}/strumenti_produttori.pdf
         manuals/{lang}/strumenti_traduzioni.pdf
         manuals/{lang}/strumenti_settings_email.pdf
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
    ("strumenti_autorizzazioni", "auth"),
    ("strumenti_materiali", "mat"),
    ("strumenti_room_booking", "room"),
    ("strumenti_tipi_scrap", "scrap"),
    ("strumenti_produttori", "prod"),
    ("strumenti_traduzioni", "trad"),
    ("strumenti_settings_email", "email"),
]

TEXTS = {}
for lang, (footer, field_l, desc_l, titles, subtitles, descs, steps, fields, notes, warns) in {
    "it": ("TraceabilityRS - Strumenti", "Campo", "Descrizione",
        {"auth":"Autorizzazioni","mat":"Gestione Materiali","room":"Room Booking","scrap":"Tipi Scrap","prod":"Gestione Produttori","trad":"Gestione Traduzioni","email":"Impostazioni Email"},
        {"auth":"Gestione delle autorizzazioni utente","mat":"Gestione dei materiali di consumo","room":"Prenotazione sale riunioni","scrap":"Gestione delle tipologie di scarto","prod":"Gestione dei produttori/fornitori","trad":"Gestione delle traduzioni dell'interfaccia","email":"Configurazione delle impostazioni email"},
        {"auth":"Il modulo Autorizzazioni consente di gestire i permessi e i ruoli degli utenti all'interno del sistema. "
               "Ogni funzione dell'applicazione puo' essere protetta da specifici permessi assegnabili ai singoli utenti o gruppi.",
         "mat":"Il modulo Materiali permette di gestire i materiali di consumo utilizzati in produzione. "
               "Include la gestione dell'inventario, le richieste di materiale e il monitoraggio dei consumi.",
         "room":"Il modulo Room Booking consente di prenotare le sale riunioni aziendali. "
                "Visualizza la disponibilita' in tempo reale e invia conferme automatiche via email.",
         "scrap":"Il modulo Tipi Scrap gestisce le categorie di scarti di produzione. "
                 "Permette di definire e organizzare le tipologie di difetti per l'analisi statistica.",
         "prod":"Il modulo Produttori gestisce l'anagrafica dei fornitori e produttori. "
                "Include informazioni di contatto, certificazioni e valutazioni qualita'.",
         "trad":"Il modulo Traduzioni consente di gestire le traduzioni dell'interfaccia utente per le diverse lingue supportate. "
                "Ogni etichetta, messaggio e voce di menu puo' essere tradotta direttamente dall'interfaccia.",
         "email":"Il modulo Impostazioni Email consente di configurare i parametri per l'invio delle email automatiche del sistema. "
                 "Include la gestione dei template email, dei destinatari e delle regole di invio."},
        {"auth":["1. Lista Utenti / Visualizzare la lista degli utenti con i loro ruoli attuali.",
                 "2. Assegna Permessi / Selezionare un utente e assegnare o revocare permessi specifici.",
                 "3. Gestione Ruoli / Creare e modificare ruoli predefiniti con set di permessi.",
                 "4. Audit Log / Consultare il registro delle modifiche ai permessi."],
         "mat":["1. Inventario / Visualizzare l'inventario corrente dei materiali.",
                "2. Richiesta Materiale / Creare una nuova richiesta di materiale.",
                "3. Approvazione / Approvare o rifiutare le richieste di materiale.",
                "4. Report Consumi / Generare report sui consumi per periodo."],
         "room":["1. Calendario / Visualizzare il calendario delle sale con disponibilita'.",
                 "2. Nuova Prenotazione / Selezionare sala, data/ora e creare la prenotazione.",
                 "3. Partecipanti / Aggiungere i partecipanti alla riunione.",
                 "4. Modifica/Cancella / Modificare o cancellare una prenotazione esistente."],
         "scrap":["1. Lista Tipologie / Visualizzare le tipologie di scarto definite.",
                  "2. Nuova Tipologia / Creare una nuova categoria di scarto.",
                  "3. Modifica / Modificare la descrizione o la classificazione di un tipo scrap.",
                  "4. Statistiche / Visualizzare le statistiche per tipologia di scarto."],
         "prod":["1. Anagrafica / Visualizzare l'elenco dei produttori registrati.",
                 "2. Nuovo Produttore / Registrare un nuovo produttore con tutti i dati.",
                 "3. Valutazione / Inserire la valutazione qualita' del produttore.",
                 "4. Documenti / Allegare certificazioni e documenti del produttore."],
         "trad":["1. Seleziona Lingua / Selezionare la lingua da tradurre.",
                 "2. Cerca Chiave / Cercare la chiave di traduzione da modificare.",
                 "3. Modifica Traduzione / Modificare il testo della traduzione.",
                 "4. Salva / Salvare le modifiche. Le traduzioni sono immediatamente attive."],
         "email":["1. Server SMTP / Configurare i parametri del server SMTP.",
                  "2. Template / Gestire i template delle email automatiche.",
                  "3. Destinatari / Configurare le liste di destinatari per tipo di notifica.",
                  "4. Test / Inviare un'email di test per verificare la configurazione."]},
        {"auth":[("Utente *","Nome utente da configurare"),("Ruolo *","Ruolo assegnato"),("Permessi","Lista dei permessi specifici"),("Attivo","Stato dell'utente (attivo/disattivo)"),("Ultimo Accesso","Data dell'ultimo accesso")],
         "mat":[("Codice *","Codice del materiale"),("Descrizione *","Descrizione del materiale"),("Quantita' *","Quantita' richiesta/disponibile"),("Unita' di Misura","Unita' di misura"),("Ubicazione","Ubicazione nel magazzino")],
         "room":[("Sala *","Sala da prenotare"),("Data *","Data della riunione"),("Ora Inizio *","Ora di inizio"),("Ora Fine *","Ora di fine"),("Oggetto","Oggetto della riunione")],
         "scrap":[("Codice *","Codice della tipologia"),("Descrizione *","Descrizione del tipo scarto"),("Categoria","Categoria (Qualita', Processo, Materiale)"),("Gravita'","Livello di gravita'"),("Attivo","Stato (attivo/disattivo)")],
         "prod":[("Ragione Sociale *","Nome del produttore"),("Codice *","Codice fornitore"),("Contatto","Referente principale"),("Email","Email di contatto"),("Valutazione","Valutazione qualita' (1-5)")],
         "trad":[("Lingua *","Lingua di destinazione"),("Chiave *","Chiave di traduzione"),("Testo Originale","Testo nella lingua base"),("Traduzione *","Testo tradotto"),("Contesto","Contesto d'uso della traduzione")],
         "email":[("Server SMTP *","Indirizzo del server SMTP"),("Porta *","Porta del server"),("Utente *","Nome utente per l'autenticazione"),("Da *","Indirizzo mittente"),("Template","Template email da utilizzare")]},
        {"auth":"NOTA: Le modifiche ai permessi sono immediatamente attive dopo il salvataggio.","mat":"NOTA: Le richieste di materiale generano una notifica al magazzino.","room":"NOTA: Le prenotazioni confermano automaticamente via email ai partecipanti.","scrap":"NOTA: Le tipologie di scarto sono utilizzate per l'analisi Pareto.","prod":"NOTA: Le valutazioni dei produttori sono visibili nel report qualita' fornitori.","trad":"NOTA: Le traduzioni mancanti vengono visualizzate nella lingua base (italiano).","email":"NOTA: Le email di test non vengono inviate ai destinatari reali."},
        {"auth":"ATTENZIONE: La rimozione di permessi puo' impedire l'accesso a funzioni critiche.","mat":"ATTENZIONE: La modifica dell'inventario richiede la riconciliazione fisica.","room":"ATTENZIONE: La cancellazione di una prenotazione invia una notifica ai partecipanti.","scrap":"ATTENZIONE: L'eliminazione di una tipologia di scarto e' irreversibile.","prod":"ATTENZIONE: La disattivazione di un produttore non elimina lo storico ordini.","trad":"ATTENZIONE: Traduzioni errate possono causare confusione nell'interfaccia.","email":"ATTENZIONE: Configurazioni SMTP errate possono bloccare tutte le notifiche email."}),
    "ro": ("TraceabilityRS - Instrumente", "Camp", "Descriere",
        {"auth":"Autorizatii","mat":"Gestionare Materiale","room":"Rezervare Sali","scrap":"Tipuri Deseuri","prod":"Gestionare Producatori","trad":"Gestionare Traduceri","email":"Setari Email"},
        {"auth":"Gestionarea autorizatiilor utilizatorilor","mat":"Gestionarea materialelor consumabile","room":"Rezervarea salilor de sedinte","scrap":"Gestionarea tipurilor de deseuri","prod":"Gestionarea producatorilor/furnizorilor","trad":"Gestionarea traducerilor interfetei","email":"Configurarea setarilor de email"},
        {"auth":"Modulul Autorizatii permite gestionarea permisiunilor si rolurilor utilizatorilor in sistem.","mat":"Modulul Materiale permite gestionarea materialelor consumabile.","room":"Modulul Rezervare Sali permite rezervarea salilor de sedinte.","scrap":"Modulul Tipuri Deseuri gestioneaza categoriile de deseuri de productie.","prod":"Modulul Producatori gestioneaza datele furnizorilor.","trad":"Modulul Traduceri permite gestionarea traducerilor interfetei.","email":"Modulul Setari Email permite configurarea parametrilor de email."},
        {"auth":["1. Lista Utilizatori / Vizualizati lista utilizatorilor.","2. Atribuire Permisiuni / Atribuiti sau revocati permisiuni.","3. Gestionare Roluri / Creati si modificati roluri.","4. Jurnal Audit / Consultati jurnalul modificarilor."],
         "mat":["1. Inventar / Vizualizati inventarul curent.","2. Cerere Material / Creati o cerere noua.","3. Aprobare / Aprobati sau refuzati cererile.","4. Raport Consum / Generati rapoarte de consum."],
         "room":["1. Calendar / Vizualizati disponibilitatea salilor.","2. Rezervare Noua / Selectati sala, data si ora.","3. Participanti / Adaugati participantii.","4. Modificare/Anulare / Modificati sau anulati o rezervare."],
         "scrap":["1. Lista Tipuri / Vizualizati tipurile definite.","2. Tip Nou / Creati o categorie noua.","3. Modificare / Modificati descrierea sau clasificarea.","4. Statistici / Vizualizati statisticile."],
         "prod":["1. Fisa Producator / Vizualizati lista producatorilor.","2. Producator Nou / Inregistrati un producator nou.","3. Evaluare / Inserati evaluarea de calitate.","4. Documente / Atasati certificari si documente."],
         "trad":["1. Selectati Limba / Selectati limba de tradus.","2. Cautati Cheia / Cautati cheia de tradus.","3. Modificati Traducerea / Modificati textul.","4. Salvati / Salvati modificarile."],
         "email":["1. Server SMTP / Configurati serverul SMTP.","2. Sabloane / Gestionati sabloanele de email.","3. Destinatari / Configurati listele de destinatari.","4. Test / Trimiteti email de test."]},
        {"auth":[("Utilizator *","Utilizatorul de configurat"),("Rol *","Rolul atribuit"),("Permisiuni","Lista permisiunilor"),("Activ","Starea utilizatorului"),("Ultimul Acces","Data ultimului acces")],
         "mat":[("Cod *","Codul materialului"),("Descriere *","Descrierea materialului"),("Cantitate *","Cantitatea"),("Unitate","Unitatea de masura"),("Locatie","Locatia in depozit")],
         "room":[("Sala *","Sala de rezervat"),("Data *","Data sedintei"),("Ora Inceput *","Ora de inceput"),("Ora Sfarsit *","Ora de sfarsit"),("Subiect","Subiectul sedintei")],
         "scrap":[("Cod *","Codul tipului"),("Descriere *","Descrierea tipului"),("Categorie","Categoria"),("Severitate","Nivelul de severitate"),("Activ","Starea")],
         "prod":[("Denumire *","Numele producatorului"),("Cod *","Codul furnizorului"),("Contact","Persoana de contact"),("Email","Email de contact"),("Evaluare","Evaluarea de calitate")],
         "trad":[("Limba *","Limba destinatie"),("Cheie *","Cheia de traducere"),("Text Original","Textul in limba de baza"),("Traducere *","Textul tradus"),("Context","Contextul utilizarii")],
         "email":[("Server SMTP *","Adresa serverului SMTP"),("Port *","Portul serverului"),("Utilizator *","Utilizatorul pentru autentificare"),("De la *","Adresa expeditor"),("Sablon","Sablonul de email")]},
        {"auth":"NOTA: Modificarile permisiunilor sunt imediat active.","mat":"NOTA: Cererile de material genereaza notificare la depozit.","room":"NOTA: Rezervarile confirma automat prin email.","scrap":"NOTA: Tipurile sunt utilizate pentru analiza Pareto.","prod":"NOTA: Evaluarile sunt vizibile in raportul de calitate.","trad":"NOTA: Traducerile lipsa se afiseaza in limba de baza.","email":"NOTA: Emailurile de test nu sunt trimise destinatarilor reali."},
        {"auth":"ATENTIE: Eliminarea permisiunilor poate bloca accesul la functii critice.","mat":"ATENTIE: Modificarea inventarului necesita reconciliere fizica.","room":"ATENTIE: Anularea trimite notificare participantilor.","scrap":"ATENTIE: Stergerea unui tip este ireversibila.","prod":"ATENTIE: Dezactivarea nu sterge istoricul comenzilor.","trad":"ATENTIE: Traducerile eronate pot cauza confuzie.","email":"ATENTIE: Configurari SMTP eronate pot bloca toate notificarile."}),
    "en": ("TraceabilityRS - Tools", "Field", "Description",
        {"auth":"Authorizations","mat":"Materials Management","room":"Room Booking","scrap":"Scrap Types","prod":"Suppliers Management","trad":"Translations Management","email":"Email Settings"},
        {"auth":"User authorization management","mat":"Consumable materials management","room":"Meeting room booking","scrap":"Scrap type management","prod":"Supplier/manufacturer management","trad":"Interface translations management","email":"Email settings configuration"},
        {"auth":"The Authorizations module manages user permissions and roles within the system.","mat":"The Materials module manages consumable materials used in production.","room":"The Room Booking module allows booking meeting rooms with real-time availability.","scrap":"The Scrap Types module manages production scrap categories for statistical analysis.","prod":"The Suppliers module manages supplier and manufacturer master data.","trad":"The Translations module manages user interface translations for all supported languages.","email":"The Email Settings module configures parameters for system automatic emails."},
        {"auth":["1. User List / View users with their current roles.","2. Assign Permissions / Assign or revoke specific permissions.","3. Role Management / Create and modify predefined roles.","4. Audit Log / Browse the permissions change log."],
         "mat":["1. Inventory / View current materials inventory.","2. Material Request / Create a new material request.","3. Approval / Approve or reject material requests.","4. Consumption Report / Generate consumption reports."],
         "room":["1. Calendar / View room availability calendar.","2. New Booking / Select room, date/time and create booking.","3. Participants / Add meeting participants.","4. Edit/Cancel / Modify or cancel an existing booking."],
         "scrap":["1. Type List / View defined scrap types.","2. New Type / Create a new scrap category.","3. Edit / Modify description or classification.","4. Statistics / View statistics by scrap type."],
         "prod":["1. Master Data / View registered suppliers.","2. New Supplier / Register a new supplier.","3. Evaluation / Enter quality evaluation.","4. Documents / Attach certifications and documents."],
         "trad":["1. Select Language / Select the target language.","2. Search Key / Search for the translation key.","3. Edit Translation / Modify the translation text.","4. Save / Save changes. Translations are immediately active."],
         "email":["1. SMTP Server / Configure SMTP server parameters.","2. Templates / Manage automatic email templates.","3. Recipients / Configure recipient lists by notification type.","4. Test / Send a test email to verify configuration."]},
        {"auth":[("User *","User to configure"),("Role *","Assigned role"),("Permissions","Specific permissions list"),("Active","User status"),("Last Access","Last access date")],
         "mat":[("Code *","Material code"),("Description *","Material description"),("Quantity *","Requested/available quantity"),("Unit","Unit of measure"),("Location","Warehouse location")],
         "room":[("Room *","Room to book"),("Date *","Meeting date"),("Start Time *","Start time"),("End Time *","End time"),("Subject","Meeting subject")],
         "scrap":[("Code *","Type code"),("Description *","Scrap type description"),("Category","Category"),("Severity","Severity level"),("Active","Status")],
         "prod":[("Company Name *","Supplier name"),("Code *","Supplier code"),("Contact","Main contact"),("Email","Contact email"),("Rating","Quality rating (1-5)")],
         "trad":[("Language *","Target language"),("Key *","Translation key"),("Original Text","Base language text"),("Translation *","Translated text"),("Context","Usage context")],
         "email":[("SMTP Server *","SMTP server address"),("Port *","Server port"),("User *","Authentication user"),("From *","Sender address"),("Template","Email template")]},
        {"auth":"NOTE: Permission changes are immediately active.","mat":"NOTE: Material requests generate a warehouse notification.","room":"NOTE: Bookings automatically confirm via email.","scrap":"NOTE: Scrap types are used for Pareto analysis.","prod":"NOTE: Supplier evaluations are visible in the quality report.","trad":"NOTE: Missing translations display in the base language.","email":"NOTE: Test emails are not sent to real recipients."},
        {"auth":"WARNING: Removing permissions may block access to critical functions.","mat":"WARNING: Inventory changes require physical reconciliation.","room":"WARNING: Cancellation sends notification to participants.","scrap":"WARNING: Deleting a scrap type is irreversible.","prod":"WARNING: Deactivating a supplier does not delete order history.","trad":"WARNING: Incorrect translations may cause interface confusion.","email":"WARNING: Wrong SMTP settings may block all email notifications."}),
    "de": ("TraceabilityRS - Werkzeuge", "Feld", "Beschreibung",
        {"auth":"Berechtigungen","mat":"Materialverwaltung","room":"Raumbuchung","scrap":"Ausschusstypen","prod":"Lieferantenverwaltung","trad":"Uebersetzungsverwaltung","email":"E-Mail-Einstellungen"},
        {"auth":"Verwaltung der Benutzerberechtigungen","mat":"Verwaltung von Verbrauchsmaterialien","room":"Buchung von Besprechungsraeumen","scrap":"Verwaltung der Ausschusstypen","prod":"Verwaltung der Lieferanten","trad":"Verwaltung der Oberflaechenuebersetzungen","email":"Konfiguration der E-Mail-Einstellungen"},
        {"auth":"Das Berechtigungsmodul verwaltet Benutzerrechte und -rollen im System.","mat":"Das Materialmodul verwaltet Verbrauchsmaterialien fuer die Produktion.","room":"Das Raumbuchungsmodul ermoeglicht die Buchung von Besprechungsraeumen.","scrap":"Das Ausschussmodul verwaltet Ausschusskategorien fuer statistische Analyse.","prod":"Das Lieferantenmodul verwaltet Lieferanten- und Herstellerdaten.","trad":"Das Uebersetzungsmodul verwaltet Oberflaechenuebersetzungen.","email":"Das E-Mail-Modul konfiguriert Parameter fuer automatische System-E-Mails."},
        {"auth":["1. Benutzerliste / Benutzer mit Rollen anzeigen.","2. Berechtigungen zuweisen / Berechtigungen zuweisen oder widerrufen.","3. Rollenverwaltung / Rollen erstellen und aendern.","4. Auditprotokoll / Aenderungsprotokoll durchsuchen."],
         "mat":["1. Inventar / Aktuelles Inventar anzeigen.","2. Materialanforderung / Neue Anforderung erstellen.","3. Genehmigung / Anforderungen genehmigen oder ablehnen.","4. Verbrauchsbericht / Verbrauchsberichte erstellen."],
         "room":["1. Kalender / Raumverfuegbarkeit anzeigen.","2. Neue Buchung / Raum, Datum und Zeit waehlen.","3. Teilnehmer / Teilnehmer hinzufuegen.","4. Aendern/Stornieren / Buchung aendern oder stornieren."],
         "scrap":["1. Typliste / Definierte Typen anzeigen.","2. Neuer Typ / Neue Kategorie erstellen.","3. Bearbeiten / Beschreibung oder Klassifikation aendern.","4. Statistiken / Statistiken nach Typ anzeigen."],
         "prod":["1. Stammdaten / Registrierte Lieferanten anzeigen.","2. Neuer Lieferant / Neuen Lieferanten registrieren.","3. Bewertung / Qualitaetsbewertung eingeben.","4. Dokumente / Zertifizierungen anhaengen."],
         "trad":["1. Sprache waehlen / Zielsprache auswaehlen.","2. Schluessel suchen / Uebersetzungsschluessel suchen.","3. Uebersetzung bearbeiten / Text aendern.","4. Speichern / Aenderungen speichern."],
         "email":["1. SMTP-Server / SMTP-Parameter konfigurieren.","2. Vorlagen / E-Mail-Vorlagen verwalten.","3. Empfaenger / Empfaengerlisten konfigurieren.","4. Test / Test-E-Mail senden."]},
        {"auth":[("Benutzer *","Zu konfigurierender Benutzer"),("Rolle *","Zugewiesene Rolle"),("Berechtigungen","Spezifische Berechtigungen"),("Aktiv","Benutzerstatus"),("Letzter Zugriff","Datum des letzten Zugriffs")],
         "mat":[("Code *","Materialcode"),("Beschreibung *","Materialbeschreibung"),("Menge *","Menge"),("Einheit","Masseinheit"),("Standort","Lagerort")],
         "room":[("Raum *","Zu buchender Raum"),("Datum *","Besprechungsdatum"),("Startzeit *","Startzeit"),("Endzeit *","Endzeit"),("Betreff","Besprechungsbetreff")],
         "scrap":[("Code *","Typcode"),("Beschreibung *","Typbeschreibung"),("Kategorie","Kategorie"),("Schweregrad","Schweregrad"),("Aktiv","Status")],
         "prod":[("Firmenname *","Lieferantenname"),("Code *","Lieferantencode"),("Kontakt","Hauptansprechpartner"),("E-Mail","Kontakt-E-Mail"),("Bewertung","Qualitaetsbewertung")],
         "trad":[("Sprache *","Zielsprache"),("Schluessel *","Uebersetzungsschluessel"),("Originaltext","Text in der Basissprache"),("Uebersetzung *","Uebersetzter Text"),("Kontext","Verwendungskontext")],
         "email":[("SMTP-Server *","SMTP-Serveradresse"),("Port *","Serverport"),("Benutzer *","Authentifizierungsbenutzer"),("Von *","Absenderadresse"),("Vorlage","E-Mail-Vorlage")]},
        {"auth":"HINWEIS: Berechtigungsaenderungen sind sofort aktiv.","mat":"HINWEIS: Materialanforderungen erzeugen eine Lagerbenachrichtigung.","room":"HINWEIS: Buchungen bestaetigen automatisch per E-Mail.","scrap":"HINWEIS: Ausschusstypen werden fuer Pareto-Analysen verwendet.","prod":"HINWEIS: Lieferantenbewertungen sind im Qualitaetsbericht sichtbar.","trad":"HINWEIS: Fehlende Uebersetzungen werden in der Basissprache angezeigt.","email":"HINWEIS: Test-E-Mails werden nicht an echte Empfaenger gesendet."},
        {"auth":"ACHTUNG: Entfernen von Berechtigungen kann den Zugang zu kritischen Funktionen blockieren.","mat":"ACHTUNG: Bestandsaenderungen erfordern physische Abstimmung.","room":"ACHTUNG: Stornierung sendet Benachrichtigung an Teilnehmer.","scrap":"ACHTUNG: Das Loeschen eines Typs ist irreversibel.","prod":"ACHTUNG: Deaktivierung loescht nicht die Bestellhistorie.","trad":"ACHTUNG: Falsche Uebersetzungen koennen Verwirrung verursachen.","email":"ACHTUNG: Falsche SMTP-Einstellungen koennen alle E-Mail-Benachrichtigungen blockieren."}),
    "sv": ("TraceabilityRS - Verktyg", "Faelt", "Beskrivning",
        {"auth":"Behorigheter","mat":"Materialhantering","room":"Rumsbokning","scrap":"Kassationstyper","prod":"Leverantoershantering","trad":"Oeversaettningshantering","email":"E-postinstaellningar"},
        {"auth":"Hantering av anvaendarrbehorigheter","mat":"Hantering av foerbrukningsmaterial","room":"Bokning av moetesrum","scrap":"Hantering av kassationstyper","prod":"Hantering av leverantoerer","trad":"Hantering av graenssnittsoeversaettningar","email":"Konfiguration av e-postinstaellningar"},
        {"auth":"Behorighetsmodulen hanterar anvaendarrbehorigheter och -roller i systemet.","mat":"Materialmodulen hanterar foerbrukningsmaterial foer produktion.","room":"Rumsbokningsmodulen goer det moejligt att boka moetesrum.","scrap":"Kassationsmodulen hanterar kassationskategorier foer statistisk analys.","prod":"Leverantoersmodulen hanterar leverantoers- och tillverkardata.","trad":"Oeversaettningsmodulen hanterar graenssnittsoeversaettningar.","email":"E-postmodulen konfigurerar parametrar foer automatiska system-e-postmeddelanden."},
        {"auth":["1. Anvaendarlista / Visa anvaendare med roller.","2. Tilldela behorigheter / Tilldela eller oeterkalla behorigheter.","3. Rollhantering / Skapa och aendra roller.","4. Granskningslogg / Blaeddra i aendringsloggen."],
         "mat":["1. Inventering / Visa aktuellt inventarium.","2. Materialbegoern / Skapa nytt begoern.","3. Godkaennande / Godkaenn eller avsloe begoeranden.","4. Foerbrukningsrapport / Generera foerbrukningsrapporter."],
         "room":["1. Kalender / Visa rumstillgoeng.","2. Ny bokning / Vaelj rum, datum och tid.","3. Deltagare / Laegg till deltagare.","4. Aendra/Avboka / Aendra eller avboka bokning."],
         "scrap":["1. Typlista / Visa definierade typer.","2. Ny typ / Skapa ny kategori.","3. Redigera / Aendra beskrivning eller klassificering.","4. Statistik / Visa statistik per typ."],
         "prod":["1. Stamdata / Visa registrerade leverantoerer.","2. Ny leverantoer / Registrera ny leverantoer.","3. Utvaerdering / Ange kvalitetsutvaerdering.","4. Dokument / Bifoga certifieringar."],
         "trad":["1. Vaelj sproek / Vaelj moelsproek.","2. Soek nyckel / Soek oeversaettningsnyckel.","3. Redigera oeversaettning / Aendra texten.","4. Spara / Spara aendringar."],
         "email":["1. SMTP-server / Konfigurera SMTP-parametrar.","2. Mallar / Hantera e-postmallar.","3. Mottagare / Konfigurera mottagarlistor.","4. Test / Skicka test-e-post."]},
        {"auth":[("Anvaendare *","Anvaendare att konfigurera"),("Roll *","Tilldelad roll"),("Behorigheter","Specifika behorigheter"),("Aktiv","Status"),("Senaste oetkomst","Datum foer senaste oetkomst")],
         "mat":[("Kod *","Materialkod"),("Beskrivning *","Materialbeskrivning"),("Kvantitet *","Kvantitet"),("Enhet","Moetenhet"),("Plats","Lagerplats")],
         "room":[("Rum *","Rum att boka"),("Datum *","Moetesdatum"),("Starttid *","Starttid"),("Sluttid *","Sluttid"),("Aemne","Moetesaemne")],
         "scrap":[("Kod *","Typkod"),("Beskrivning *","Typbeskrivning"),("Kategori","Kategori"),("Allvarlighet","Allvarlighetsnivoe"),("Aktiv","Status")],
         "prod":[("Foeretag *","Leverantoersnamn"),("Kod *","Leverantoerskod"),("Kontakt","Huvudkontakt"),("E-post","Kontaktens e-post"),("Betyg","Kvalitetsbetyg")],
         "trad":[("Sproek *","Moelsproek"),("Nyckel *","Oeversaettningsnyckel"),("Originaltext","Text poe bassproeket"),("Oeversaettning *","Oeversatt text"),("Kontext","Anvaendningskontext")],
         "email":[("SMTP-server *","SMTP-serveradress"),("Port *","Serverport"),("Anvaendare *","Autentiseringsanvaendare"),("Froen *","Avsaendaradress"),("Mall","E-postmall")]},
        {"auth":"NOTERA: Behoerighetsaendringar aer omedelbart aktiva.","mat":"NOTERA: Materialbegoeranden genererar lagernotifiering.","room":"NOTERA: Bokningar bekraeftar automatiskt via e-post.","scrap":"NOTERA: Kassationstyper anvaends foer Pareto-analys.","prod":"NOTERA: Leverantoersutvaerderingar aer synliga i kvalitetsrapporten.","trad":"NOTERA: Saknade oeversaettningar visas poe bassproeket.","email":"NOTERA: Test-e-post skickas inte till riktiga mottagare."},
        {"auth":"VARNING: Borttagna behorigheter kan blockera oetkomst till kritiska funktioner.","mat":"VARNING: Lageraendringar kraever fysisk avstoemning.","room":"VARNING: Avbokning skickar notifiering till deltagare.","scrap":"VARNING: Borttagning av typ aer irreversibel.","prod":"VARNING: Avaktivering raderar inte orderhistorik.","trad":"VARNING: Felaktiga oeversaettningar kan orsaka foervirring.","email":"VARNING: Felaktiga SMTP-instaellningar kan blockera alla e-postnotifieringar."}),
}.items():
    T = {"app":"TraceabilityRS","ver":"Versione 2.3.6" if lang=="it" else ("Versiunea 2.3.6" if lang=="ro" else "Version 2.3.6"),
         "footer":footer,"field":field_l,"description":desc_l}
    for key in ("auth","mat","room","scrap","prod","trad","email"):
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
